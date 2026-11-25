"""Dashboard del CRM — server HTTP locale, in tempo reale.

Avvio: `python -m modules.crm serve` (vedi `modules/crm/__main__.py`).

Sicurezza (stessa linea del server vocale, R8):
  * ascolta SOLO sul computer stesso (127.0.0.1 / localhost): per usarlo da fuori si passa
    da un tunnel (SSH, Tailscale), mai esponendo la porta;
  * token OBBLIGATORIO `GAS_CRM_TOKEN` (almeno 16 caratteri): senza, il server non parte.
    Il login scambia il token con un cookie di sessione `HttpOnly; SameSite=Strict`
    (12 ore); le integrazioni possono usare `Authorization: Bearer <token>`;
  * confronto del token a tempo costante; tetto ai tentativi sbagliati per IP;
  * header Host solo «localhost», un IP o il nome privato Tailscale del Mac dichiarato in
    `GAS_CRM_NOME_TAILSCALE` (contro il DNS rebinding; dal telefono si entra con `tailscale
    serve`, che resta nella rete privata e fa HTTPS: decisione 21, `scripts/crm/telefono.sh`);
  * ogni POST vuole `Content-Type: application/json` e l'header `X-Gas-CRM: 1` (una
    pagina estranea non può aggiungerlo senza preflight), e un eventuale Origin uguale
    all'Host (contro il CSRF);
  * Content-Security-Policy stretta: niente script o stili in linea, niente risorse esterne;
    la pagina costruisce il DOM solo con textContent (i dati non diventano mai HTML).

Tempo reale: un thread guarda `PRAGMA data_version` ogni secondo; quando il DB cambia
(dalla dashboard, dalla CLI o da Gas) avvisa i browser collegati con Server-Sent Events e
rilancia la scansione del motore (con un attimo di ritardo, per raggruppare i cambi).
"""
from __future__ import annotations

import hmac
import ipaddress
import json
import logging
import os
import re
import secrets
import sqlite3
import threading
import time
from datetime import date, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlsplit

from modules.crm import analisi, copia_cifrata, motore, scrittore
from modules.crm.messaggi import link_whatsapp
from modules.crm.store import (CRMStore, ErroreCRM, normalizza_telefono,
                               parse_importo, parse_percentuale_bp, valida_data)

log = logging.getLogger(__name__)

WEB_DIR = Path(__file__).resolve().parent / "web"
STATICI: Dict[str, Tuple[str, str]] = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/app.css": ("app.css", "text/css; charset=utf-8"),
    "/favicon.svg": ("favicon.svg", "image/svg+xml"),
}
CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
       "connect-src 'self'; font-src 'self'; base-uri 'none'; form-action 'none'; "
       "frame-ancestors 'none'")
COOKIE = "gas_crm"
SESSIONE_S = 12 * 3600
CORPO_MAX = 64 * 1024
TOKEN_MIN = 16
MAX_FALLITI = 10
FALLITI_FINESTRA_S = 600.0
BLOCCO_S = 900.0
MAX_STREAM = 16
AVVISO_MIN_S = 3600.0
BACKUP_OGNI_S = 24 * 3600.0

Invia = Callable[[str], Tuple[bool, str]]

# Nome Tailscale del Mac (es. «mac-di-gas.tail1234.ts.net»): solo nomi della rete privata
_NOME_TS = re.compile(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+ts\.net")


def nome_tailscale_da_env() -> Optional[str]:
    """Decisione 21: il nome con cui il telefono apre la dashboard tramite `tailscale serve`.
    Solo un nome `*.ts.net` (mai un dominio pubblico); altrimenti None e un avviso."""
    grezzo = os.environ.get("GAS_CRM_NOME_TAILSCALE", "").strip().lower().rstrip(".")
    if not grezzo:
        return None
    if len(grezzo) > 253 or not _NOME_TS.fullmatch(grezzo):
        log.warning("CRM: GAS_CRM_NOME_TAILSCALE ignorato: non è un nome Tailscale (*.ts.net)")
        return None
    return grezzo


def bind_locale(bind: str) -> bool:
    """Solo loopback IPv4 o «localhost» (il server è solo IPv4)."""
    b = bind.strip().lower()
    if b == "localhost":
        return True
    try:
        ip = ipaddress.ip_address(b)
    except ValueError:
        return False
    return isinstance(ip, ipaddress.IPv4Address) and ip.is_loopback


def token_ok(ricevuto: str, atteso: str) -> bool:
    if not ricevuto or not atteso:
        return False
    return hmac.compare_digest(ricevuto.encode("utf-8"), atteso.encode("utf-8"))


class Stato:
    """Stato condiviso del server: sessioni, blocchi, versione dei dati, scansioni."""

    def __init__(self, store: CRMStore, token: str, demo: bool = False,
                 regole: Optional[motore.Regole] = None, scan_minuti: int = 10,
                 avvisa: Optional[Invia] = None, memoria_db: Optional[Path] = None,
                 oggi: Optional[Callable[[], date]] = None,
                 nome_tailscale: Optional[str] = None) -> None:
        self.store = store
        self.token = token
        self.nome_tailscale = nome_tailscale  # decisione 21: unico nome non locale ammesso
        self.demo = demo
        self.regole = regole or motore.Regole.da_env()
        self.scan_s = max(1, scan_minuti) * 60.0
        self.avvisa = avvisa
        self.memoria_db = memoria_db
        self.oggi = oggi or store.oggi
        self.lock = threading.Lock()
        self.sessioni: Dict[str, float] = {}
        self.falliti: Dict[str, List[float]] = {}
        self.bloccati: Dict[str, float] = {}
        self.versione = 0
        self.cambio = threading.Condition(self.lock)
        self.stop = threading.Event()
        self.stream_attivi = 0
        self.ultima_scansione: Optional[Dict[str, Any]] = None
        self.ultima_scansione_ts: Optional[float] = None
        self.scan_richiesta = threading.Event()
        self.ultimo_avviso = 0.0
        self.scan_lock = threading.Lock()
        self.ultimo_backup = 0.0  # monotonic: il guardiano fa una copia all'avvio e ogni giorno
        # V-1 bot #386: esito dell'ultima copia CIFRATA fuori dal Mac, visibile in dashboard
        # (prima un fallimento restava solo nel log e l'operatore continuava a credersi coperto)
        spenta = None if demo else copia_cifrata.motivo_spenta()
        self.copia_esterna: Dict[str, Any] = {"spenta": spenta is not None, "motivo": spenta,
                                              "ok": None, "quando": None}
        # R-803-1: UN SOLO MemoryStore per processo. Aprirne uno rifà l'indice di ricerca
        # del diario e lo salva (una scrittura): farlo a ogni lettura della dashboard
        # innescava un ciclo «scrittura → cambio → rilettura → scrittura».
        self.memoria: Any = None
        if not demo and memoria_db is not None:
            try:
                from modules.memory.store import MemoryStore
                mem = MemoryStore(memoria_db)
                self.memoria = mem if mem.available else None
            except Exception as e:  # §9: senza memoria il CRM funziona, senza i lead
                log.warning("CRM: memoria di Gas non apribile: %s", e)

    # ---------------------------------------------------------------- sessioni
    def nuova_sessione(self) -> str:
        sid = secrets.token_urlsafe(32)
        adesso = time.time()
        with self.lock:
            self.sessioni = {k: v for k, v in self.sessioni.items() if v > adesso}
            if len(self.sessioni) >= 64:  # memoria limitata: esce la più vecchia
                del self.sessioni[min(self.sessioni, key=self.sessioni.__getitem__)]
            self.sessioni[sid] = adesso + SESSIONE_S
        return sid

    def sessione_valida(self, sid: str) -> bool:
        if not sid:
            return False
        with self.lock:
            scad = self.sessioni.get(sid)
            if scad is None:
                return False
            if scad < time.time():
                del self.sessioni[sid]
                return False
            return True

    def chiudi_sessione(self, sid: str) -> None:
        with self.lock:
            self.sessioni.pop(sid, None)

    def ip_bloccato(self, ip: str) -> bool:
        with self.lock:
            scad = self.bloccati.get(ip)
            if scad is None:
                return False
            if scad < time.monotonic():
                del self.bloccati[ip]
                return False
            return True

    def registra_fallito(self, ip: str) -> None:
        adesso = time.monotonic()
        with self.lock:
            recenti = [t for t in self.falliti.get(ip, []) if adesso - t < FALLITI_FINESTRA_S]
            recenti.append(adesso)
            if len(recenti) >= MAX_FALLITI:
                self.bloccati[ip] = adesso + BLOCCO_S
                self.falliti.pop(ip, None)
                log.warning("CRM AUTH BLOCCO ip=%s per %d s", ip, int(BLOCCO_S))
            else:
                if len(self.falliti) >= 1024 and ip not in self.falliti:
                    del self.falliti[min(self.falliti, key=lambda k: self.falliti[k][-1])]
                self.falliti[ip] = recenti

    # ---------------------------------------------------------------- dati
    def segnala_cambio(self) -> None:
        with self.cambio:
            self.versione += 1
            self.cambio.notify_all()

    def scansiona(self) -> Dict[str, Any]:
        with self.scan_lock:
            esito = motore.scansiona(self.store, oggi=self.oggi(), regole=self.regole)
            d = esito.come_dict()
            self.ultima_scansione = d
            self.ultima_scansione_ts = time.time()
        if esito.create:
            self._avvisa_operatore(len(esito.create), esito.valore_nuovo_cents)
        return d

    def _avvisa_operatore(self, n: int, valore_cents: int) -> None:
        """Avviso su Telegram all'operatore: SOLO numeri, mai nomi o dati dei clienti."""
        if self.avvisa is None or self.demo:
            return
        adesso = time.time()
        if adesso - self.ultimo_avviso < AVVISO_MIN_S:
            return
        self.ultimo_avviso = adesso
        euro = (valore_cents + 50) // 100
        testo = (f"🎯 CRM Gas: {n} nuove opportunità da approvare "
                 f"(valore stimato ~{euro:,} €/mese di commissioni). "
                 "Aprile dalla dashboard.").replace(",", ".")
        try:
            ok, motivo = self.avvisa(testo)
            if not ok:
                log.warning("CRM: avviso Telegram non consegnato: %s", motivo)
        except Exception as e:  # §9: un avviso fallito non ferma il CRM
            log.warning("CRM: avviso Telegram fallito: %s", e)

    def lead_pronti(self) -> List[Dict[str, Any]]:
        """Lead della rubrica di Gas in stato «interessato»: candidati a diventare clienti."""
        if self.memoria is None:
            return []
        try:
            righe = self.memoria.leggi_contatti("interessato") or []
        except Exception as e:
            log.warning("CRM: lettura dei lead fallita: %s", e)
            return []
        gia = {c.get("contatto_id") for c in self.store.clienti()}
        out = []
        for r in righe[:50]:
            if r.get("id") in gia:
                continue
            out.append({"id": r.get("id"), "chiave": r.get("chiave"), "nome": r.get("nome"),
                        "contatto": r.get("contatto"), "non_fidato": bool(r.get("non_fidato"))})
        return out

    def converti_lead(self, contatto_id: int) -> int:
        if self.memoria is None:
            raise ErroreCRM("conversione dei lead non disponibile (demo o memoria di Gas assente)")
        mem = self.memoria
        lead = mem.get_contatto(contatto_id)
        if not lead:
            raise ErroreCRM("lead inesistente")
        if any(c.get("contatto_id") == contatto_id for c in self.store.clienti()):
            raise ErroreCRM("questo lead è già un cliente")
        recapito = str(lead.get("contatto") or "").strip()
        telefono: Optional[str] = None
        if recapito and re.fullmatch(r"\+?[0-9 ]+", recapito):
            try:
                telefono = normalizza_telefono(recapito)
            except ErroreCRM:
                telefono = None
        email = recapito if "@" in recapito else None
        nuovo = self.store.aggiungi_cliente(
            nome=str(lead.get("nome") or lead.get("chiave")), telefono=telefono, email=email,
            consenso_marketing=False, contatto_id=contatto_id,
            note="Convertito dalla rubrica lead di Gas: raccogliere il consenso ai messaggi.",
        )
        if mem.update_stato_contatto(contatto_id, "chiuso",
                                     prossima_azione=f"diventato cliente CRM #{nuovo}") is False:
            log.warning("CRM: lead %s convertito ma stato non aggiornato", contatto_id)
        # R-803-9: la transizione del funnel resta tracciata anche nel diario di Gas
        if mem.append_diario("crm_conversione", f"Lead convertito in cliente CRM #{nuovo}",
                             contatto_id=contatto_id, fonte="utente") is None:
            log.warning("CRM: conversione del lead %s non scritta nel diario", contatto_id)
        return nuovo


def _segna_copia(stato: "Stato", spenta: Optional[str], riuscita: bool, motivo: Optional[str],
                 locale: bool = False) -> None:
    """Esito della copia in `stato.copia_esterna` (dashboard) e, se fallisce davvero, avviso
    all'operatore (Telegram, se attivo: mai dati dei clienti). `locale`: è fallita già la
    copia sul Mac (il motivo lo dice da sé)."""
    ora = datetime.now().isoformat(timespec="minutes")
    stato.copia_esterna = {"spenta": spenta is not None, "motivo": motivo,
                           "ok": None if spenta is not None else riuscita, "quando": ora}
    stato.segnala_cambio()
    if not riuscita and spenta is None:
        log.warning("CRM: copia cifrata esterna: %s", motivo)
        if stato.avvisa is not None and not stato.demo:
            try:
                # R-824-2, R-825-1 e R-826-2: se è fallita la copia sul Mac l'avviso dice solo
                # il motivo (che lo spiega già), senza «iCloud» fisso né «non è riuscita» doppio
                if locale:
                    testo = (f"⚠️ CRM Gas: {motivo}. Nessuna copia di sicurezza nuova: "
                             "controlla dalla dashboard.")
                else:
                    testo = (f"⚠️ CRM Gas: la copia cifrata fuori dal Mac NON è riuscita "
                             f"({motivo}). I dati sono ancora solo sul Mac: controlla dalla "
                             "dashboard.")
                stato.avvisa(testo)
            except Exception as e:  # §9: un avviso fallito non ferma il CRM
                log.warning("CRM: avviso della copia esterna fallito: %s", type(e).__name__)


def _copia_esterna(stato: "Stato", copia: Any) -> None:
    """Thread: copia cifrata fuori dal Mac e il suo esito (vedi `_segna_copia`)."""
    spenta = copia_cifrata.motivo_spenta()
    fuori, motivo = copia_cifrata.copia_fuori(copia)
    _segna_copia(stato, spenta, fuori is not None, motivo)


def _copia_giornaliera(stato: "Stato") -> None:
    """Copia locale del giorno e, se riesce, quella cifrata fuori dal Mac in un thread a parte
    (R-815-4). V-2 bot #386 (3°): se fallisce già la copia locale, anche l'indicatore della
    copia esterna lo dice (prima restava «copia OK» del giorno prima)."""
    copia = stato.store.backup()
    if copia is None:
        log.warning("CRM: copia di sicurezza automatica non riuscita")
        # R-821-1: fallimento della copia LOCALE sempre in rosso e con avviso, anche quando
        # la copia esterna è spenta (prima l'indicatore restava «copia spenta»)
        # V-2 verifica esterna #387: il motivo non dice «nemmeno quella fuori dal Mac»
        # quando la copia esterna è spenta
        fuori = ("la copia fuori dal Mac è spenta" if copia_cifrata.motivo_spenta()
                 else "quindi nemmeno quella fuori dal Mac")
        _segna_copia(stato, None, False, f"la copia sul Mac non è riuscita, {fuori}", locale=True)
        return
    threading.Thread(target=_copia_esterna, args=(stato, copia), name="crm-copia-cifrata",
                     daemon=True).start()


def _guardiano(stato: Stato) -> None:
    """Thread: si accorge dei cambi nel DB (anche fatti da altri processi) e programma le
    scansioni. Una connessione tenuta aperta: `PRAGMA data_version` cambia quando un'ALTRA
    connessione fa commit."""
    con: Optional[sqlite3.Connection] = None
    ultima_v: Optional[int] = None
    prossima_scan = time.monotonic() + 1.0
    scan_dopo_cambio: Optional[float] = None
    while not stato.stop.is_set():
        try:
            if con is None:
                con = sqlite3.connect(str(stato.store.db_path), timeout=5, check_same_thread=False)
            v = int(con.execute("PRAGMA data_version").fetchone()[0])
            if ultima_v is not None and v != ultima_v:
                stato.segnala_cambio()
                scan_dopo_cambio = time.monotonic() + 2.0
            ultima_v = v
        except sqlite3.Error as e:
            log.warning("CRM: guardiano del DB: %s", e)
            try:
                if con is not None:
                    con.close()
            except sqlite3.Error:
                pass
            con = None
        adesso = time.monotonic()
        if not stato.demo and (stato.ultimo_backup == 0.0 or adesso - stato.ultimo_backup >= BACKUP_OGNI_S):
            stato.ultimo_backup = adesso
            # decisione dell'operatore 2026-11-19: copia locale e copia CIFRATA fuori dal Mac
            _copia_giornaliera(stato)
        dovuta = (adesso >= prossima_scan or stato.scan_richiesta.is_set()
                  or (scan_dopo_cambio is not None and adesso >= scan_dopo_cambio))
        if dovuta:
            stato.scan_richiesta.clear()
            scan_dopo_cambio = None
            prossima_scan = adesso + stato.scan_s
            try:
                stato.scansiona()
            except Exception as e:  # §9
                log.warning("CRM: scansione automatica fallita: %s", e)
        stato.stop.wait(1.0)
    if con is not None:
        con.close()


class CRMHandler(BaseHTTPRequestHandler):
    server_version = "GasCRM/1"
    sys_version = ""
    protocol_version = "HTTP/1.1"
    stato: Stato  # iniettato da crea_server

    def log_message(self, fmt: str, *args: Any) -> None:  # niente log di accesso su stderr
        return

    # ---------------------------------------------------------------- risposte
    def _corpo_in_sospeso(self) -> bool:
        """La richiesta ha un corpo che non è stato letto? (R-803-2)"""
        if getattr(self, "_corpo_letto", False):
            return False
        if self.headers.get("Transfer-Encoding"):
            return True
        lun = (self.headers.get("Content-Length") or "").strip()
        return lun not in ("", "0")

    def _intestazioni_sicurezza(self) -> None:
        # R-803-2: se si risponde senza aver letto il corpo (403/401/413…), la connessione
        # si chiude: altrimenti il corpo, scelto magari da una pagina estranea, verrebbe
        # letto come la richiesta successiva sulla stessa connessione.
        if self._corpo_in_sospeso():
            self.send_header("Connection", "close")
            self.close_connection = True
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cache-Control", "no-store")

    def _json(self, codice: int, corpo: Any, extra: Optional[List[Tuple[str, str]]] = None) -> None:
        dati = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
        self.send_response(codice)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(dati)))
        self._intestazioni_sicurezza()
        for k, v in extra or []:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(dati)

    def _errore(self, codice: int, msg: str) -> None:
        self._json(codice, {"errore": msg})

    # ---------------------------------------------------------------- controlli
    def _host_ammesso(self) -> bool:
        # R-860-1: una richiesta arrivata dal «funnel» di Tailscale viene da INTERNET: mai.
        # tailscaled mette questo header su ogni richiesta funnel e toglie quelli finti.
        if self.headers.get("Tailscale-Funnel-Request") is not None:
            log.warning("CRM: RIFIUTATA richiesta dal funnel di Tailscale (internet)")
            return False
        host = (self.headers.get("Host") or "").strip().lower()
        if not host:
            return False  # V-3 bot #381 (2° giro): niente eccezioni alla difesa dal DNS rebinding
        porta = ""
        if host.startswith("["):
            nome = host[1:host.find("]")] if "]" in host else host
        elif host.count(":") == 1:
            nome, porta = host.split(":", 1)
        else:
            nome = host
        if nome == "localhost":
            return True
        # decisione 21: il nome Tailscale del Mac solo dall'HTTPS di `tailscale serve` (porta 443)
        if self.stato.nome_tailscale and nome == self.stato.nome_tailscale:
            if porta in ("", "443"):
                return True
            log.warning("CRM HOST RIFIUTATO: nome Tailscale su una porta diversa da 443")
            return False
        try:
            ipaddress.ip_address(nome)
            return True
        except ValueError:
            log.warning("CRM HOST RIFIUTATO ip=%s", self.client_address[0])
            return False

    def _da_tailscale(self) -> bool:
        """La richiesta arriva dal nome Tailscale, cioè via HTTPS di `tailscale serve`."""
        nome = (self.headers.get("Host") or "").strip().lower().split(":", 1)[0]
        return bool(self.stato.nome_tailscale) and nome == self.stato.nome_tailscale

    def _attributi_cookie(self) -> str:
        # decisione 21: da HTTPS il cookie viaggia solo cifrato
        return "HttpOnly; SameSite=Strict; Path=/" + ("; Secure" if self._da_tailscale() else "")

    def _cookie(self) -> str:
        grezzo = self.headers.get("Cookie") or ""
        for parte in grezzo.split(";"):
            k, _, v = parte.strip().partition("=")
            if k == COOKIE:
                return v
        return ""

    def _autenticato(self) -> bool:
        if self.stato.sessione_valida(self._cookie()):
            return True
        parti = (self.headers.get("Authorization") or "").split(" ", 1)
        if len(parti) == 2 and parti[0].lower() == "bearer":
            ip = str(self.client_address[0])
            if self.stato.ip_bloccato(ip):
                return False
            if token_ok(parti[1].strip(), self.stato.token):
                return True
            self.stato.registra_fallito(ip)
        return False

    def _post_ammesso(self) -> Optional[str]:
        if (self.headers.get("X-Gas-CRM") or "") != "1":
            return "header X-Gas-CRM mancante"
        if not (self.headers.get("Content-Type") or "").lower().startswith("application/json"):
            return "serve Content-Type: application/json"
        origine = self.headers.get("Origin")
        if origine:
            host = (self.headers.get("Host") or "").strip().lower()
            if origine.strip().lower() not in (f"http://{host}", f"https://{host}"):
                return "origine non ammessa"
        return None

    def _leggi_json(self) -> Optional[Dict[str, Any]]:
        try:
            lun = int(self.headers.get("Content-Length") or "0")
        except ValueError:
            lun = -1
        if lun < 0 or lun > CORPO_MAX:
            self._errore(413, "richiesta troppo grande")
            return None
        grezzo = self.rfile.read(lun) if lun else b"{}"
        self._corpo_letto = True
        try:
            dati = json.loads(grezzo.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._errore(400, "JSON non valido")
            return None
        if not isinstance(dati, dict):
            self._errore(400, "serve un oggetto JSON")
            return None
        return dati

    # ---------------------------------------------------------------- GET
    def do_GET(self) -> None:  # noqa: N802
        self._corpo_letto = False
        try:
            self._get()
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:  # §9 (R-803-8): l'errore va in gas_debug.log, non su stderr
            log.warning("CRM: errore su GET %s: %s", urlsplit(self.path).path, e)
            try:
                self._errore(500, "errore interno (vedi gas_debug.log)")
            except OSError:
                pass

    def _get(self) -> None:
        if not self._host_ammesso():
            return self._errore(403, "Host non ammesso")
        url = urlsplit(self.path)
        if url.path in STATICI:
            return self._statico(*STATICI[url.path])
        if url.path == "/api/sessione":
            return self._json(200, {"autenticato": self._autenticato(), "demo": self.stato.demo})
        if not url.path.startswith("/api/"):
            return self._errore(404, "non trovato")
        if not self._autenticato():
            if self.stato.ip_bloccato(str(self.client_address[0])):
                return self._errore(429, "troppi tentativi: riprova più tardi")
            return self._errore(401, "accesso richiesto")
        q = parse_qs(url.query)
        try:
            if url.path == "/api/stato":
                return self._stato_completo()
            if url.path == "/api/cliente":
                return self._dettaglio_cliente(int((q.get("id") or ["0"])[0]))
            if url.path == "/api/stream":
                return self._stream()
        except ValueError:
            return self._errore(400, "parametro non valido")
        return self._errore(404, "non trovato")

    def _statico(self, nome: str, tipo: str) -> None:
        try:
            dati = (WEB_DIR / nome).read_bytes()
        except OSError:
            return self._errore(404, "non trovato")
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dati)))
        self._intestazioni_sicurezza()
        self.end_headers()
        self.wfile.write(dati)

    def _stato_completo(self) -> None:
        foto = self.stato.store.fotografia()
        if foto is None:
            return self._errore(503, "database non disponibile")
        d = analisi.costruisci(foto, self.stato.oggi())
        corpo = analisi.panoramica(d)
        r = self.stato.regole
        corpo["server"] = {
            "demo": self.stato.demo,
            "versione": self.stato.versione,
            "ultima_scansione": self.stato.ultima_scansione,
            "ultima_scansione_ts": self.stato.ultima_scansione_ts,
            "regole": {"soglia_cents": r.soglia_cents, "pausa_giorni": r.pausa_giorni,
                       "max_messaggi_30g": r.max_messaggi_30g,
                       "pausa_dopo_no_giorni": r.pausa_dopo_no_giorni,
                       "pagamenti_min": r.pagamenti_min, "aumento_pct": r.aumento_pct,
                       "anzianita_min_giorni": r.anzianita_min_giorni,
                       "invii_per_lotto": r.invii_per_lotto, "lotto_minuti": r.lotto_minuti},
            "invii": self._invii(),
            "opus": {"motivo": scrittore.disponibile(), "modello": scrittore.modello()},
            "copia_esterna": None if self.stato.demo else self.stato.copia_esterna,
        }
        corpo["lead_pronti"] = self.stato.lead_pronti()
        corpo["eventi"] = self.stato.store.eventi(n=40)
        return self._json(200, corpo)

    def _invii(self) -> Dict[str, Any]:
        """Scaglioni anti-blocco: invii fatti nella finestra e tra quanto se ne libera uno."""
        r = self.stato.regole
        recenti = self.stato.store.invii_recenti(r.lotto_minuti)
        libero_tra = 0
        if len(recenti) >= r.invii_per_lotto:
            libero = recenti[-r.invii_per_lotto] + timedelta(minutes=r.lotto_minuti)
            libero_tra = max(0, int((libero - self.stato.store._orologio()).total_seconds()))
        return {"fatti": len(recenti), "max": r.invii_per_lotto, "minuti": r.lotto_minuti,
                "libero_tra_s": libero_tra}

    def _dettaglio_cliente(self, cid: int) -> None:
        store = self.stato.store
        foto = store.fotografia()
        if foto is None:
            return self._errore(503, "database non disponibile")
        d = analisi.costruisci(foto, self.stato.oggi())
        if cid not in d.clienti:
            return self._errore(404, "cliente inesistente")
        m = analisi.metriche_cliente(d, cid)
        mesi = analisi.ultimi_mesi(d.mese, 12)
        posizioni = []
        for p in m.posizioni:
            s = d.servizi[p.servizio_id]
            posizioni.append({
                "id": p.id, "servizio_id": p.servizio_id, "servizio_nome": s["nome"],
                "stato": p.stato, "aperta_il": p.aperta_il, "capitale_cents": p.capitale_cents,
                "profitto_mese_cents": p.profitto_per_mese.get(d.mese, 0),
                "profitto_totale_cents": p.profitto_totale_cents,
                "commissioni_totali_cents": p.commissioni_totali_cents,
                "roi_bp": analisi.roi_posizione_bp(p, d.mese),
                "serie_profitto_cents": [p.profitto_per_mese.get(x, 0) for x in mesi],
            })
        nomi_srv = {int(s["id"]): s["nome"] for s in foto["servizi"]}
        pos_srv = {p.id: p.servizio_id for p in m.posizioni}
        movimenti = [dict(x, servizio_nome=nomi_srv.get(pos_srv.get(int(x["posizione_id"]), -1)))
                     for x in store.movimenti(cid)]
        proposte = []
        for riga in store.proposte(cid):
            pr = dict(riga)
            pr["servizio_nome"] = nomi_srv.get(int(pr["servizio_id"])) if pr["servizio_id"] else None
            proposte.append(pr)
        self._json(200, {
            "cliente": d.clienti[cid],
            "metriche": {
                "capitale_cents": m.capitale_cents, "profitto_mese_cents": m.profitto_mese_cents,
                "profitto_mese_prec_cents": m.profitto_mese_prec_cents,
                "profitto_totale_cents": m.profitto_totale_cents,
                "commissioni_totali_cents": m.commissioni_totali_cents,
                "pagamenti": m.pagamenti, "servizi_attivi": m.servizi_attivi,
            },
            "mesi": mesi,
            "posizioni": posizioni,
            "movimenti": list(reversed(movimenti)),
            "proposte": list(reversed(proposte)),
            "eventi": store.eventi(cid, n=100),
            "spiegazione": motore.spiega(store, cid, oggi=self.stato.oggi(), regole=self.stato.regole),
        })

    def _stream(self) -> None:
        st = self.stato
        with st.lock:
            if st.stream_attivi >= MAX_STREAM:
                pieno = True
            else:
                st.stream_attivi += 1
                pieno = False
        if pieno:
            return self._errore(503, "troppe dashboard aperte")
        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Connection", "keep-alive")
            self._intestazioni_sicurezza()
            self.end_headers()
            self.close_connection = True
            sid = self._cookie()

            def sessione_finita() -> bool:
                # letto col lucchetto già preso (dentro la Condition): niente sessione_valida
                scad = st.sessioni.get(sid) if sid else None
                return bool(sid) and (scad is None or scad < time.time())
            with st.cambio:
                visto = st.versione
            self.wfile.write(f"event: pronto\ndata: {visto}\n\n".encode())
            self.wfile.flush()
            inizio = time.monotonic()
            while not st.stop.is_set() and time.monotonic() - inizio < SESSIONE_S:
                with st.cambio:
                    st.cambio.wait_for(lambda: st.versione != visto or st.stop.is_set()
                                       or sessione_finita(), timeout=15)
                    nuova = st.versione
                    finita = sessione_finita()
                if finita:
                    break  # R-803-11: dopo il logout lo stream si chiude
                if nuova != visto:
                    visto = nuova
                    self.wfile.write(f"event: cambio\ndata: {visto}\n\n".encode())
                else:
                    self.wfile.write(b": battito\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            with st.lock:
                st.stream_attivi -= 1

    # ---------------------------------------------------------------- POST
    def do_POST(self) -> None:  # noqa: N802
        self._corpo_letto = False
        if not self._host_ammesso():
            return self._errore(403, "Host non ammesso")
        motivo = self._post_ammesso()
        if motivo:
            return self._errore(403, motivo)
        url = urlsplit(self.path)
        ip = str(self.client_address[0])
        if url.path == "/api/login":
            if self.stato.ip_bloccato(ip):
                return self._errore(429, "troppi tentativi: riprova più tardi")
            dati = self._leggi_json()
            if dati is None:
                return
            if not token_ok(str(dati.get("token") or ""), self.stato.token):
                self.stato.registra_fallito(ip)
                log.warning("CRM AUTH FAIL ip=%s", ip)
                return self._errore(401, "token sbagliato")
            sid = self.stato.nuova_sessione()
            return self._json(200, {"ok": True}, [(
                "Set-Cookie",
                f"{COOKIE}={sid}; {self._attributi_cookie()}; Max-Age={SESSIONE_S}")])
        if not self._autenticato():
            if self.stato.ip_bloccato(ip):
                return self._errore(429, "troppi tentativi: riprova più tardi")
            return self._errore(401, "accesso richiesto")
        if url.path == "/api/logout":
            self.stato.chiudi_sessione(self._cookie())
            with self.stato.cambio:
                self.stato.cambio.notify_all()  # gli stream di quella sessione si chiudono
            return self._json(200, {"ok": True}, [(
                "Set-Cookie", f"{COOKIE}=; {self._attributi_cookie()}; Max-Age=0")])
        dati = self._leggi_json()
        if dati is None:
            return
        azioni: Dict[str, Callable[[Dict[str, Any]], Any]] = {
            "/api/clienti": self._nuovo_cliente,
            "/api/clienti/aggiorna": self._aggiorna_cliente,
            "/api/servizi": self._nuovo_servizio,
            "/api/servizi/aggiorna": self._aggiorna_servizio,
            "/api/posizioni": self._nuova_posizione,
            "/api/posizioni/stato": self._stato_posizione,
            "/api/posizioni/apertura": lambda d: self.stato.store.anticipa_apertura(
                _id(d, "id"), str(d.get("data") or "")),
            "/api/movimenti": self._nuovo_movimento,
            "/api/movimenti/storno": self._storno,
            "/api/proposte/azione": self._azione_proposta,
            "/api/proposte/selezionati": self._prepara_selezionati,
            "/api/proposte/riscrivi": lambda d: {"messaggio": scrittore.riscrivi(
                self.stato.store, _id(d, "id"))["messaggio"]},
            "/api/note": self._nota,
            "/api/scansiona": lambda _d: self.stato.scansiona(),
            "/api/lead/converti": lambda d: {"id": self.stato.converti_lead(_id(d, "contatto_id"))},
        }
        fn = azioni.get(url.path)
        if fn is None:
            return self._errore(404, "non trovato")
        try:
            risultato = fn(dati)
        except ErroreCRM as e:
            return self._errore(400, str(e))
        except Exception as e:  # §9: nessuna eccezione abbatte il server
            log.warning("CRM: errore su %s: %s", url.path, e)
            return self._errore(500, "errore interno (vedi gas_debug.log)")
        return self._json(200, {"ok": True, "risultato": risultato})

    # ---------------------------------------------------------------- azioni
    def _nuovo_cliente(self, d: Dict[str, Any]) -> Dict[str, Any]:
        cid = self.stato.store.aggiungi_cliente(
            nome=str(d.get("nome") or ""), telefono=d.get("telefono") or None, email=d.get("email") or None,
            # V-2 bot #381 (2° giro): il valore grezzo, controllato dallo store («false» non è sì)
            consenso_marketing=d.get("consenso_marketing", False),
            presentato_da=_id_opz(d, "presentato_da"), note=d.get("note") or None,
        )
        return {"id": cid}

    def _aggiorna_cliente(self, d: Dict[str, Any]) -> None:
        campi = {k: d[k] for k in ("nome", "telefono", "email", "stato", "consenso_marketing",
                                   "opt_out", "note", "presentato_da", "followup_attivo") if k in d}
        if "presentato_da" in campi:
            campi["presentato_da"] = _id_opz(d, "presentato_da")
        self.stato.store.aggiorna_cliente(_id(d, "id"), **campi)

    def _campi_servizio(self, d: Dict[str, Any]) -> Dict[str, Any]:
        campi: Dict[str, Any] = {}
        for k in ("nome", "descrizione", "modello_commissione"):
            if k in d:
                campi[k] = d[k]
        if "commissione_pct" in d:
            campi["commissione_bp"] = parse_percentuale_bp(d["commissione_pct"])
        if "rendimento_stimato_pct" in d:
            campi["rendimento_stimato_bp"] = parse_percentuale_bp(d["rendimento_stimato_pct"])
        for k_in, k_out in (("commissione_fissa", "commissione_fissa_cents"),
                            ("capitale_minimo", "capitale_minimo_cents")):
            if k_in in d:
                v = d[k_in]
                campi[k_out] = 0 if v in (None, "", "0", 0) else parse_importo(v)
        if "priorita" in d:
            try:
                campi["priorita"] = int(d["priorita"])
            except (TypeError, ValueError):
                raise ErroreCRM("priorità: serve un numero intero") from None
        for k in ("attivo", "consigliato"):
            if k in d:
                campi[k] = d[k]  # valore grezzo: lo controlla lo store (_bool01)
        return campi

    def _nuovo_servizio(self, d: Dict[str, Any]) -> Dict[str, Any]:
        campi = self._campi_servizio(d)
        sid = self.stato.store.aggiungi_servizio(
            codice=str(d.get("codice") or ""), nome=str(campi.get("nome") or ""),
            modello_commissione=campi.get("modello_commissione", ""),
            commissione_bp=campi.get("commissione_bp", 0),
            commissione_fissa_cents=campi.get("commissione_fissa_cents", 0),
            capitale_minimo_cents=campi.get("capitale_minimo_cents", 0),
            rendimento_stimato_bp=campi.get("rendimento_stimato_bp", 0),
            priorita=campi.get("priorita", 100), descrizione=campi.get("descrizione"),
        )
        return {"id": sid}

    def _aggiorna_servizio(self, d: Dict[str, Any]) -> None:
        self.stato.store.aggiorna_servizio(_id(d, "id"), **self._campi_servizio(d))

    def _nuova_posizione(self, d: Dict[str, Any]) -> Dict[str, Any]:
        # V-3 bot #381 (2° giro): importo controllato PRIMA e posizione + deposito in una
        # sola transazione: un capitale scritto male non lascia una posizione a metà
        capitale = d.get("capitale_iniziale")
        cents = None if capitale in (None, "", 0, "0") else parse_importo(capitale)
        pid = self.stato.store.apri_posizione(_id(d, "cliente_id"), _id(d, "servizio_id"),
                                              data=d.get("data") or None,
                                              capitale_iniziale_cents=cents)
        return {"id": pid}

    def _stato_posizione(self, d: Dict[str, Any]) -> None:
        self.stato.store.cambia_stato_posizione(_id(d, "id"), str(d.get("stato") or ""),
                                                data=d.get("data") or None)

    def _nuovo_movimento(self, d: Dict[str, Any]) -> Dict[str, Any]:
        data = d.get("data") or None
        if data is not None:
            valida_data(data)
        mid = self.stato.store.registra_movimento(
            _id(d, "posizione_id"), str(d.get("tipo") or ""), parse_importo(d.get("importo")),
            data=data, nota=d.get("nota") or None)
        return {"id": mid}

    def _storno(self, d: Dict[str, Any]) -> Dict[str, Any]:
        return {"id": self.stato.store.storna_movimento(_id(d, "id"), nota=d.get("nota") or None)}

    def _azione_proposta(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """invia | scarta | accettata | rifiutata | stop. «invia» la segna inviata e
        ritorna il link wa.me: il messaggio lo manda l'operatore dal suo WhatsApp."""
        st = self.stato.store
        pid = _id(d, "id")
        azione = str(d.get("azione") or "")
        prop = st.proposta(pid)
        if prop is None:
            raise ErroreCRM("proposta inesistente")
        if azione == "invia":
            cliente = st.cliente(int(prop["cliente_id"])) or {}
            if motore.motivo_non_contattabile(cliente):
                raise ErroreCRM(f"non si può inviare: {motore.motivo_non_contattabile(cliente)}")
            testo = d.get("messaggio") or None
            if testo is not None and not isinstance(testo, str):
                raise ErroreCRM("messaggio: deve essere testo")
            # nota, riga STOP, lunghezza e tetto degli invii li controlla lo store, dentro la
            # transazione dell'invio (V-2 bot #381; scaglioni anti-blocco di WhatsApp)
            r = self.stato.regole
            nuova = st.transiziona_proposta(pid, "inviata", messaggio=testo, canale="whatsapp",
                                            tetto_invii=(r.invii_per_lotto, r.lotto_minuti))
            return {"link_whatsapp": link_whatsapp(cliente.get("telefono"), nuova["messaggio"])}
        if azione == "scarta":
            st.transiziona_proposta(pid, "scartata")
        elif azione in ("accettata", "rifiutata"):
            st.transiziona_proposta(pid, azione)
        elif azione == "stop":
            st.aggiorna_cliente(int(prop["cliente_id"]), opt_out=True)
            if prop["stato"] == "da_approvare":
                st.transiziona_proposta(pid, "superata")
            elif prop["stato"] in ("inviata", "senza_risposta"):
                st.transiziona_proposta(pid, "rifiutata")
        else:
            raise ErroreCRM("azione non valida")
        return {}

    def _prepara_selezionati(self, d: Dict[str, Any]) -> Dict[str, Any]:
        ids = d.get("clienti")
        if not isinstance(ids, list) or not ids:
            raise ErroreCRM("nessun cliente selezionato")
        if len(ids) > motore.SELEZIONE_MAX:
            raise ErroreCRM(f"al massimo {motore.SELEZIONE_MAX} clienti per volta")
        esito = motore.prepara_selezionati(self.stato.store, [_id({"x": v}, "x") for v in ids],
                                           regole=self.stato.regole)
        if esito.errore:
            raise ErroreCRM(esito.errore)
        return esito.come_dict()

    def _nota(self, d: Dict[str, Any]) -> None:
        self.stato.store.annota(_id(d, "cliente_id"), str(d.get("testo") or ""))


def _id(d: Dict[str, Any], campo: str) -> int:
    v = d.get(campo)
    if isinstance(v, bool):
        raise ErroreCRM(f"{campo}: non valido")
    try:
        n = int(v)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        raise ErroreCRM(f"{campo}: serve un numero") from None
    if n <= 0:
        raise ErroreCRM(f"{campo}: non valido")
    return n


def _id_opz(d: Dict[str, Any], campo: str) -> Optional[int]:
    v = d.get(campo)
    if v in (None, "", 0, "0"):
        return None
    return _id(d, campo)


class _Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def crea_server(stato: Stato, host: str, porta: int) -> ThreadingHTTPServer:
    """Server pronto (non ancora avviato). Solleva ValueError se l'indirizzo non è locale."""
    if not bind_locale(host):
        raise ValueError("il CRM ascolta solo sul computer stesso (127.0.0.1 o localhost): "
                         "per usarlo da fuori passa da un tunnel")
    handler = type("CRMHandlerLegato", (CRMHandler,), {"stato": stato})
    return _Server((host, porta), handler)


def avvia(stato: Stato, host: str = "127.0.0.1", porta: int = 8770,
          pronto: Optional[Callable[[str], None]] = None) -> None:
    """Avvia server e guardiano; blocca fino a Ctrl+C."""
    server = crea_server(stato, host, porta)
    guardiano = threading.Thread(target=_guardiano, args=(stato,), name="crm-guardiano", daemon=True)
    guardiano.start()
    indirizzo = f"http://{host}:{server.server_address[1]}/"
    if pronto:
        pronto(indirizzo)
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        stato.stop.set()
        with stato.cambio:
            stato.cambio.notify_all()
        server.server_close()


def token_da_env() -> Optional[str]:
    t = os.environ.get("GAS_CRM_TOKEN", "").strip()
    return t if len(t) >= TOKEN_MIN else None
