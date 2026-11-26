"""Mani alla voce, fetta F3 (2026-11-26, piano in reports/mani_voce_piano.md §3 e §4bis):
Gas sul Mac e la «cassetta delle lettere» delle richieste di sviluppo.

Tre cose, tutte col token DEDICATO delle richieste (`modules/sviluppo/richieste.py`):

1. `avviso_accodata`: il testo dell'avviso che parte SUBITO quando una richiesta viene
   accodata (al posto della firma a voce, rifiutata dall'operatore il 26/11): numero, titolo,
   e il comando per annullarla.
2. `annulla(numero)`: «annulla richiesta N» da Telegram. Chiude la issue con l'etichetta
   `annullata`, SOLO se è una issue aperta con l'etichetta `da-gas` nel repo privato.
   L'esecutore (F5) non tocca issue chiuse né `annullata`.
3. `controlla_esiti()`: ogni pochi minuti (dal loop del bot Telegram) legge i commenti nuovi
   del repo delle richieste e, per ogni commento ESITO valido (formato fisso di
   `modules/sviluppo/esiti.py`) scritto da un autore AMMESSO (`GAS_RICHIESTE_AUTORI`,
   elenco di login separati da virgole: senza elenco non legge niente) su una issue `da-gas`,
   manda all'operatore la frase di `frase_esito`. Ricorda, per ogni richiesta, la PR per cui
   la domanda di merge è stata fatta davvero (R-873MV-1: F4 accetterà «mergia N» solo per
   quella). Stato in `.gas_richieste_esiti.json` (0600): commenti già visti, ultimo controllo,
   domande aperte.

Fail-safe §9: nessuna eccezione esce; ogni errore è un testo «Operazione negata: …» o un
controllo saltato, scritto in gas_debug.log (mai il token). Un commento scartato si scrive nel
log (cosmetica 5 di #409).

Regola per l'esecutore (F5, bot #412 V-1): un ESITO è sempre un commento NUOVO. Un commento già
letto e poi modificato non viene riletto. Consegna: al più una volta (lo stato si scrive prima
dell'invio).
"""
from __future__ import annotations

import json
import logging
import os
import re
import secrets
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from modules.sviluppo import esiti
from modules.sviluppo.richieste import API, ETICHETTA, Http, _REPO_RE, _http, _token

log = logging.getLogger(__name__)

ETICHETTA_ANNULLATA = "annullata"
STATO_FILENAME = ".gas_richieste_esiti.json"
VISTI_MAX = 1000            # id di commenti ricordati
PAGINA = 100                # commenti letti per controllo (per_page dell'API)
MARGINE_S = 120             # «since» un po' indietro: orologi diversi, commenti in ritardo
INTERVALLO_MIN_DEFAULT = 5  # GAS_RICHIESTE_CONTROLLO_MIN
ATTESA_ESECUTORE_MIN = 30   # finestra per annullare prima che l'esecutore parta (F5)
# login GitHub, anche di una GitHub App («nome[bot]», per F5: R-879MV-5)
_LOGIN_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})(?:\[bot\])?$")
_ISO_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
ESITI_PER_CONTROLLO = 5       # avvisi di esito al massimo per controllo (R-879MV-2)
ESITI_GIORNO_DEFAULT = 20     # GAS_RICHIESTE_ESITI_GIORNO
SOSPESI_MAX = 20              # esiti di autori non (ancora) ammessi, riprovati
PAGINE_MAX = 50               # pagine lette con lo stesso «since» (5000 commenti) prima di ripartire
_AVVISATO_SENZA_AUTORI = False
# «annulla richiesta 12», «annulla la richiesta #12»: frase intera, solo ASCII (come «mergia N»)
_ANNULLA_RE = re.compile(r"^\s*annulla\s+(?:la\s+)?richiesta\s+#?([1-9][0-9]{0,6})\s*[.!]?\s*$",
                         re.IGNORECASE | re.ASCII)

Invia = Callable[[str], Tuple[bool, str]]


# ---------------------------------------------------------------- configurazione

def _repo() -> Optional[str]:
    repo = (os.environ.get("GAS_RICHIESTE_REPO") or "").strip()
    return repo if _REPO_RE.fullmatch(repo) else None


def autori_ammessi() -> frozenset:
    """Login GitHub da cui si accettano gli ESITO (minuscoli). Vuoto = nessuno (fail-closed)."""
    grezzo = os.environ.get("GAS_RICHIESTE_AUTORI") or ""
    return frozenset(x.strip().lower() for x in grezzo.split(",")
                     if _LOGIN_RE.fullmatch(x.strip()))


def intervallo_s() -> float:
    try:
        minuti = float(os.environ.get("GAS_RICHIESTE_CONTROLLO_MIN", INTERVALLO_MIN_DEFAULT))
    except ValueError:
        minuti = INTERVALLO_MIN_DEFAULT
    if not (minuti == minuti) or minuti < 1:  # NaN o troppo spesso
        minuti = INTERVALLO_MIN_DEFAULT
    return min(minuti, 24 * 60) * 60


# ---------------------------------------------------------------- 1. avviso alla creazione

def avviso_accodata(numero: int, titolo: Any, da_voce: bool) -> str:
    """Il testo dell'avviso subito dopo la creazione della issue (§4bis del piano)."""
    origine = "Arrivata a voce." if da_voce else "Arrivata da Telegram o dal terminale."
    return (f"📨 Richiesta di sviluppo #{int(numero)} accodata: «{esiti._citato(titolo, 120)}». "
            f"{origine} L'esecutore non la prende prima di {ATTESA_ESECUTORE_MIN} minuti. "
            f"Se non è tua, rispondi «annulla richiesta {int(numero)}».")


# ---------------------------------------------------------------- 2. annullo

def comando_annulla(testo: Any) -> Optional[int]:
    """«annulla richiesta N» → N; altro → None. Solo frasi intere e corte."""
    try:
        if not isinstance(testo, str) or len(testo) > 60:
            return None
        m = _ANNULLA_RE.match(testo)
        return int(m.group(1)) if m else None
    except Exception:  # §9
        return None


def _privato(repo: str, token: str, http: Http) -> Optional[str]:
    """None se il repo è privato e raggiungibile, altrimenti il motivo (fail-closed)."""
    codice, info = http("GET", f"{API}/repos/{repo}", token, None)
    if codice != 200 or not isinstance(info, dict):
        return f"repo delle richieste non raggiungibile (HTTP {codice})"
    if info.get("private") is not True:
        return "il repo delle richieste non è PRIVATO"
    return None


def _etichette(issue: Dict[str, Any]) -> List[str]:
    return [e.get("name") for e in issue.get("labels") or [] if isinstance(e, dict)]


def annulla(numero: Any, root: Path, http: Optional[Http] = None) -> str:
    """Chiude la richiesta #numero con l'etichetta `annullata`. Solo issue (non PR) aperte
    con l'etichetta `da-gas`, nel repo privato. Testo per l'operatore, mai eccezioni."""
    http = http or _http
    try:
        if isinstance(numero, bool) or not isinstance(numero, int) or not 0 < numero <= esiti.PR_MAX:
            return "Operazione negata: numero di richiesta non valido."
        repo, token = _repo(), _token()
        if not repo or not token:
            return "Operazione negata: repo o token delle richieste non configurati."
        motivo = _privato(repo, token, http)
        if motivo:
            return f"Operazione negata: {motivo}."
        codice, issue = http("GET", f"{API}/repos/{repo}/issues/{numero}", token, None)
        if codice != 200 or not isinstance(issue, dict):
            return f"Operazione negata: richiesta #{numero} non trovata (HTTP {codice})."
        if issue.get("pull_request") is not None or ETICHETTA not in _etichette(issue):
            return f"Operazione negata: la #{numero} non è una richiesta di sviluppo di Gas."
        if issue.get("state") != "open":
            return f"La richiesta #{numero} era già chiusa: niente da annullare."
        codice, _ = http("POST", f"{API}/repos/{repo}/issues/{numero}/labels", token,
                         {"labels": [ETICHETTA_ANNULLATA]})
        if codice != 200:
            return (f"Operazione negata: etichetta «{ETICHETTA_ANNULLATA}» non messa "
                    f"(HTTP {codice}): la richiesta #{numero} NON è annullata.")
        codice, chiusa = http("PATCH", f"{API}/repos/{repo}/issues/{numero}", token,
                              {"state": "closed", "state_reason": "not_planned"})
        if codice != 200 or not isinstance(chiusa, dict) or chiusa.get("state") != "closed":
            # l'etichetta c'è già: l'esecutore la salta lo stesso, ma lo si dice
            return (f"Richiesta #{numero} segnata «{ETICHETTA_ANNULLATA}» ma non chiusa "
                    f"(HTTP {codice}): l'esecutore non la prende; chiudila a mano se vuoi.")
        return f"Richiesta #{numero} annullata: l'esecutore non la prenderà."
    except Exception as e:  # §9
        log.warning("cassetta: annullo non riuscito (%s)", type(e).__name__)
        return "Operazione negata: annullo non riuscito (errore interno, dettagli nel log)."


# ---------------------------------------------------------------- 3. lettura degli esiti

def _leggi_stato(root: Path) -> Dict[str, Any]:
    p = Path(root) / STATO_FILENAME
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(d, dict):
            return d
    except FileNotFoundError:
        pass
    except Exception as e:
        log.warning("cassetta: stato illeggibile (%s), riparto da adesso", type(e).__name__)
    return {}


def _scrivi_stato(root: Path, stato: Dict[str, Any]) -> bool:
    p = Path(root) / STATO_FILENAME
    tmp = p.with_suffix(f".tmp.{os.getpid()}.{secrets.token_hex(4)}")
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(stato, f, ensure_ascii=False)
        os.replace(tmp, p)
        return True
    except Exception as e:
        log.warning("cassetta: stato non scritto (%s)", type(e).__name__)
        try:
            tmp.unlink()
        except Exception:
            pass
        return False


def _iso(t: datetime) -> str:
    return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _numero_issue(commento: Dict[str, Any], repo: str) -> Optional[int]:
    url = commento.get("issue_url")
    prefisso = f"{API}/repos/{repo}/issues/".lower()  # R-879MV-3: GitHub ignora le maiuscole
    if not isinstance(url, str) or not url.lower().startswith(prefisso):
        return None
    coda = url[len(prefisso):]
    return int(coda) if coda.isdigit() and 0 < int(coda) <= esiti.PR_MAX else None


def _invia_default(testo: str) -> Tuple[bool, str]:
    from modules.telegram import bot
    return bot.invia_notifica(testo)


def domanda_aperta(root: Path, numero_richiesta: int) -> Optional[int]:
    """La PR per cui Gas ha chiesto davvero «vuoi che la mergi?» sulla richiesta, o None.
    Per F4 (R-873MV-1). Mai eccezioni."""
    try:
        voce = (_leggi_stato(root).get("domande") or {}).get(str(int(numero_richiesta)))
        pr = voce.get("pr") if isinstance(voce, dict) else voce
        return pr if isinstance(pr, int) and not isinstance(pr, bool) else None
    except Exception:
        return None


def _tetto_giorno() -> int:
    """Avvisi di esito al giorno (GAS_RICHIESTE_ESITI_GIORNO, default 20, tetto 100)."""
    try:
        n = int(os.environ.get("GAS_RICHIESTE_ESITI_GIORNO", ESITI_GIORNO_DEFAULT))
    except ValueError:
        n = ESITI_GIORNO_DEFAULT
    return max(1, min(n, 100))


def _quando(c: Dict[str, Any]) -> Optional[str]:
    """La data più recente del commento (GitHub filtra «since» sulla modifica): R-879MV-4."""
    date = [c.get(k) for k in ("updated_at", "created_at")
            if isinstance(c.get(k), str) and _ISO_RE.fullmatch(c.get(k))]
    return max(date) if date else None


def controlla_esiti(root: Path, http: Optional[Http] = None, invia: Optional[Invia] = None,
                    adesso: Optional[datetime] = None) -> int:
    """Un controllo: legge i commenti nuovi e avvisa l'operatore per ogni ESITO valido.
    Ritorna quanti avvisi sono partiti. Mai eccezioni (§9).
    - R-879MV-2: al massimo ESITI_PER_CONTROLLO avvisi a controllo e _tetto_giorno() al giorno;
      oltre, i commenti restano per i controlli dopo (non si perdono).
    - R-879MV-3: un ESITO scartato per un motivo di CONFIGURAZIONE (autore non nell'elenco)
      non si perde: resta «in sospeso» (al massimo SOSPESI_MAX) e si riprova a ogni controllo,
      così aggiungere l'autore a GAS_RICHIESTE_AUTORI lo recupera.
    - R-879MV-4 e R-880MV-1: con la pagina piena «since» resta e si legge la pagina dopo; con
      la pagina non piena «since» avanza alla data più recente letta (meno un margine). Così la
      lettura non si blocca e niente si perde."""
    http = http or _http
    invia = invia or _invia_default
    global _AVVISATO_SENZA_AUTORI
    try:
        repo, token, ammessi = _repo(), _token(), autori_ammessi()
        if not repo or not token:
            return 0
        if not ammessi:
            if not _AVVISATO_SENZA_AUTORI:  # R-879MV-5: una volta per processo, non ogni 5 min
                log.warning("cassetta: GAS_RICHIESTE_AUTORI vuoto: nessun esito letto")
                _AVVISATO_SENZA_AUTORI = True
            return 0
        root = Path(root)
        motivo_repo = _privato(repo, token, http)  # ve #412 V-4: come annulla, fail-closed
        if motivo_repo:
            log.warning("cassetta: esiti non letti: %s", motivo_repo)
            return 0
        ora = adesso or datetime.now(timezone.utc)
        oggi = ora.date().isoformat()
        stato = _leggi_stato(root)
        visti: List[int] = [x for x in stato.get("visti") or [] if isinstance(x, int)]
        sospesi: List[int] = [x for x in stato.get("sospesi") or [] if isinstance(x, int)]
        domande: Dict[str, Any] = {k: v for k, v in (stato.get("domande") or {}).items()
                                   if isinstance(k, str) and isinstance(v, (int, dict))}
        uso = stato.get("uso") if isinstance(stato.get("uso"), dict) else {}
        n_oggi = uso.get("n") if uso.get("giorno") == oggi and isinstance(uso.get("n"), int) else 0
        since = stato.get("since")
        if not isinstance(since, str) or not _ISO_RE.fullmatch(since):
            # primo controllo: si parte da adesso, niente valanga di esiti vecchi
            stato.update(since=_iso(ora - timedelta(seconds=MARGINE_S)), visti=visti,
                         sospesi=sospesi, domande=domande)
            _scrivi_stato(root, stato)
            return 0
        pagina = stato.get("pagina")
        pagina = pagina if isinstance(pagina, int) and not isinstance(pagina, bool) and \
            1 <= pagina <= PAGINE_MAX else 1
        codice, commenti = http(
            "GET", f"{API}/repos/{repo}/issues/comments?sort=created&direction=asc"
                   f"&per_page={PAGINA}&page={pagina}&since={since}", token, None)
        if codice != 200 or not isinstance(commenti, list):
            log.warning("cassetta: commenti non letti (HTTP %s)", codice)
            return 0
        pagina_piena = len(commenti) >= PAGINA
        # i sospesi si rileggono uno per uno (pochi): forse ora l'autore è ammesso
        da_vedere: List[Any] = []
        for cid in list(sospesi):
            cs, c = http("GET", f"{API}/repos/{repo}/issues/comments/{cid}", token, None)
            if cs == 200 and isinstance(c, dict):
                da_vedere.append(c)
            elif cs == 404:
                sospesi.remove(cid)  # commento cancellato
        da_vedere += commenti
        inviati = 0
        ultimo = since
        titoli: Dict[int, Optional[Tuple[str, bool]]] = {}
        gia = set(visti)
        for c in da_vedere:
            if not isinstance(c, dict) or not isinstance(c.get("id"), int):
                continue
            cid = c["id"]
            quando = _quando(c)
            if quando and cid not in sospesi:
                ultimo = max(ultimo, quando)
            if cid in gia:
                continue
            corpo = c.get("body")
            if not (isinstance(corpo, str) and esiti.MARCA_ESITO in corpo):
                visti.append(cid); gia.add(cid)  # commento qualunque (anche i COMANDO di Gas)
                continue
            autore = str((c.get("user") or {}).get("login") or "").lower()
            numero = _numero_issue(c, repo)
            esito = esiti.leggi_esito(corpo)
            if numero is None or esito is None:
                log.warning("cassetta: commento %s scartato (%s)", cid,
                            "issue non riconosciuta" if numero is None else "formato non valido")
                visti.append(cid); gia.add(cid)
                continue
            if autore not in ammessi:
                if cid not in sospesi:
                    log.warning("cassetta: esito %s di «%s», autore non in GAS_RICHIESTE_AUTORI: "
                                "in sospeso", cid, autore[:39])
                    sospesi.append(cid)
                continue
            if inviati >= ESITI_PER_CONTROLLO or n_oggi >= _tetto_giorno():
                log.warning("cassetta: tetto degli avvisi di esito raggiunto: il resto al prossimo "
                            "controllo")
                break
            if numero not in titoli:
                ci, issue = http("GET", f"{API}/repos/{repo}/issues/{numero}", token, None)
                titoli[numero] = ((str(issue.get("title") or ""),
                                   ETICHETTA in _etichette(issue)
                                   and issue.get("pull_request") is None)
                                  if ci == 200 and isinstance(issue, dict)
                                  else ("", False) if ci in (404, 410) else None)
            info = titoli[numero]
            if info is None:
                break  # errore transitorio (rete, 5xx, 403): si riprova al prossimo controllo
            # ve #412 V-2: issue sparita (404/410) = scarto definitivo, non blocca la fila
            titolo, nostra = info
            if not nostra:
                log.warning("cassetta: commento %s su #%s scartato (issue sparita o non da-gas)",
                            cid, numero)
                visti.append(cid); gia.add(cid)
                continue
            # ve #412 V-1 (gravità media): PRIMA si scrive lo stato con il commento già visto, il
            # conto del giorno e la domanda nuova, POI si invia. Se lo stato non si scrive non si
            # invia niente: con il file non scrivibile niente avvisi ripetuti (al più una
            # consegna: un crash fra scrittura e invio perde l'avviso invece di duplicarlo).
            # bot #412 V-3 e R-882MV-1/2: la domanda ricordata cambia solo per un esito PIÙ
            # RECENTE; un esito senza domanda lascia una «lapide» con la data (pr None), così un
            # esito vecchio recuperato dopo non la riapre; e la domanda va nello stato insieme al
            # segno di visto, prima dell'invio.
            creato = c.get("created_at") if isinstance(c.get("created_at"), str) else ""
            voce = domande.get(str(numero))
            prec = voce.get("quando") if isinstance(voce, dict) else None
            vecchio = isinstance(prec, str) and bool(prec) and (not creato or creato < prec)
            domande_prima = dict(domande)
            if not vecchio:
                domande[str(numero)] = {"pr": esito["pr"] if esiti.propone_merge(esito) else None,
                                        "quando": creato}
            visti.append(cid); gia.add(cid)
            n_oggi += 1
            prima = {k: stato.get(k) for k in ("visti", "uso", "domande")}
            stato["visti"] = visti[-VISTI_MAX:]
            stato["uso"] = {"giorno": oggi, "n": n_oggi}
            stato["domande"] = domande
            if not _scrivi_stato(root, stato):
                log.warning("cassetta: stato non scrivibile: esito %s NON avvisato (niente "
                            "ripetizioni)", cid)
                visti.pop(); gia.discard(cid); n_oggi -= 1
                domande.clear(); domande.update(domande_prima)
                stato.update(prima)
                return inviati
            ok, motivo = invia(esiti.frase_esito(numero, titolo, esito))
            if not ok:
                log.warning("cassetta: avviso dell'esito %s non partito (%s): riprovo", cid, motivo)
                visti.pop(); gia.discard(cid); n_oggi -= 1
                domande.clear(); domande.update(domande_prima)
                break  # in ordine: questo e i successivi al prossimo controllo
            inviati += 1
            if cid in sospesi:
                sospesi.remove(cid)
        else:
            # pagina letta tutta (R-879MV-4, R-880MV-1). L'API filtra su updated_at e ordina per
            # created_at: con la pagina piena «since» NON si tocca e la prossima volta si legge
            # la pagina dopo (un commento vecchio modificato di recente non fa saltare niente);
            # con la pagina non piena si è visto tutto da «since»: si avanza alla data più
            # recente letta, meno il margine, e si torna alla pagina 1.
            if pagina_piena and pagina < PAGINE_MAX:
                stato["pagina"] = pagina + 1
            else:
                if pagina_piena:
                    log.warning("cassetta: più di %s pagine di commenti nuovi: riparto da adesso",
                                PAGINE_MAX)
                    ultimo = max(ultimo, _iso(ora))
                stato["pagina"] = 1
                if ultimo != since:
                    try:
                        t = datetime.strptime(ultimo, "%Y-%m-%dT%H:%M:%SZ").replace(
                            tzinfo=timezone.utc)
                        stato["since"] = _iso(min(t, ora) - timedelta(seconds=MARGINE_S))
                    except ValueError:
                        pass
        stato["visti"] = visti[-VISTI_MAX:]
        if len(sospesi) > SOSPESI_MAX:  # ve #412 V-3: il taglio lascia traccia
            log.warning("cassetta: %s esiti in sospeso scartati (oltre %s)",
                        len(sospesi) - SOSPESI_MAX, SOSPESI_MAX)
        stato["sospesi"] = sospesi[-SOSPESI_MAX:]
        stato["domande"] = domande
        stato["uso"] = {"giorno": oggi, "n": n_oggi}
        _scrivi_stato(root, stato)
        return inviati
    except Exception as e:  # §9
        log.warning("cassetta: controllo degli esiti non riuscito (%s)", type(e).__name__)
        return 0


class Cronometro:
    """Per il loop del bot: un controllo alla volta, al massimo ogni intervallo_s()."""

    def __init__(self) -> None:
        self.prossimo = 0.0
        self.in_corso = False

    def tocca(self, ora: Optional[float] = None) -> bool:
        ora = time.monotonic() if ora is None else ora
        if self.in_corso or ora < self.prossimo:
            return False
        self.prossimo = ora + intervallo_s()
        return True


_CRONO = Cronometro()


def controllo_in_sottofondo(root: Path,
                            lavoro: Optional[Callable[[Path], Any]] = None) -> bool:
    """Per il loop del bot Telegram: se è ora (e nessun controllo è in corso) lancia
    controlla_esiti in un thread demone, così una chiamata GitHub lenta non ferma il polling.
    Il thread fa SOLO rete GitHub + invia_notifica + il file di stato: niente update, firme o
    kernel. True se lanciato. Mai eccezioni (§9)."""
    try:
        if not _CRONO.tocca():
            return False
        _CRONO.in_corso = True
        fare = lavoro or controlla_esiti

        def _lavora() -> None:
            try:
                fare(Path(root))
            except Exception as e:  # §9
                log.warning("cassetta: controllo in sottofondo fallito (%s)", type(e).__name__)
            finally:
                _CRONO.in_corso = False

        threading.Thread(target=_lavora, name="esiti-richieste", daemon=True).start()
        return True
    except Exception as e:  # §9
        _CRONO.in_corso = False
        log.warning("cassetta: controllo non avviato (%s)", type(e).__name__)
        return False
