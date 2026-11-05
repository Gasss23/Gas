#!/usr/bin/env python3
"""
clients/voice/ascolto.py — voce H24 sul Mac (R8, chat Mani).

Gas sempre in ascolto: microfono aperto, parola di attivazione in LOCALE con
openWakeWord (per ora il modello pronto «hey_jarvis»: «Ehi Gas» va addestrato in una
fetta a parte), poi bip, registrazione fino al silenzio, invio al server voce già
esistente (modules/voice/server.py, POST /voice) e risposta riprodotta: con la risposta
«a pezzi» del server (righe JSON, formato audio+pezzi) la prima frase suona appena arriva e le altre in
fila, mentre il server sintetizza le successive (fetta 39). Dopo la risposta
resta una finestra di ascolto (GAS_VOICE_FINESTRA, 12 s) per continuare senza ripetere
la parola, fino a GAS_VOICE_MAX_TURNI turni di fila.
Mentre Gas parla si può interromperlo dicendo di nuovo la parola di attivazione (fetta
41): la frase si ferma, quelle in fila si scartano e si registra la nuova richiesta.
Grilletto SOLO la parola, con una soglia più alta (GAS_ASCOLTO_SOGLIA_INTERRUZIONE): con
le casse del Mac il microfono sente la voce di Gas, e il volume da solo la scambierebbe
per una domanda.

Uso (dalla root ~/Gas, venv attivo, dipendenze di clients/voice/requirements-ascolto.txt):
    python clients/voice/ascolto.py
Di solito parte da solo con launchd: vedi scripts/voce/LEGGIMI.md.

Privacy:
  - Prima della parola di attivazione l'audio resta SOLO in memoria e lo legge solo
    openWakeWord, in locale: niente rete, niente disco.
  - La richiesta registrata resta in memoria e va solo al server voce. Non si salva
    nessuna registrazione.
  - La risposta di Gas (la sua voce, non la tua) passa da un file temporaneo 0600 per
    afplay, uno per frase, cancellato subito dopo.
  - Nel log dell'ascolto solo gli eventi (attivazione, invio, codici di errore), mai l'audio né il
    token.

Variabili d'ambiente (lette anche da .env nella root di Gas):
    GAS_VOICE_TOKEN        — token bearer del server voce  OBBLIGATORIO
    GAS_VOICE_URL          — URL del server voce (default http://127.0.0.1:<GAS_VOICE_PORT o
                             8765>, la porta del server voce). Fuori
                             dal Mac (host non locale) solo https, altrimenti non parte.
    GAS_VOICE_TIMEOUT      — secondi di attesa della risposta (default 600)
    GAS_VOICE_FINESTRA     — secondi di ascolto dopo la risposta (default 12)
    GAS_VOICE_MAX_TURNI    — turni di fila senza parola di attivazione (default 5)
    GAS_ASCOLTO_MODELLO    — modello di openWakeWord (default hey_jarvis)
    GAS_ASCOLTO_SOGLIA     — soglia della parola di attivazione, 0-1 (default 0.5)
    GAS_ASCOLTO_VOCE_RMS   — energia sopra cui c'è voce (default 200, campioni int16)
    GAS_ASCOLTO_SILENZIO   — secondi di silenzio che chiudono la richiesta (default 0.8)
    GAS_ASCOLTO_INTERRUZIONE — 0 = la parola non interrompe Gas mentre parla (default 1)
    GAS_ASCOLTO_SOGLIA_INTERRUZIONE — soglia della parola mentre Gas parla, 0-1 (default 0.7)
    GAS_ASCOLTO_FORMATO    — formato della risposta chiesto al server (default
                             audio+pezzi, le frasi in fila; vuoto = un solo MP3)

Fail-safe §9: server giù o errore → bip di errore e si torna in ascolto; microfono che
cade → nuovo tentativo dopo qualche secondo; nessuna eccezione esce dal ciclo.
"""
from __future__ import annotations

import array
import base64
import io
import json
import logging
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import wave
from pathlib import Path
from typing import Callable, Iterable, Iterator, List, Optional, Sequence, Tuple, Union

log = logging.getLogger("gas.ascolto")

_HERE = Path(__file__).resolve().parent
_GAS_ROOT = _HERE.parent.parent

FREQ = 16000                 # Hz, mono, int16: il formato di openWakeWord
BLOCCO = 1280                # campioni per blocco (80 ms)
SEC_BLOCCO = BLOCCO / FREQ
REGISTRAZIONE_MAX_S = 30.0   # una richiesta non dura più di così
ATTESA_VOCE_S = 5.0          # dopo la parola, se non parli entro questo tempo si torna in attesa
INIZIO_VOCE_S = 0.24         # voce continua che apre un turno nella finestra (3 blocchi)
MICROFONO_MUTO_S = 10.0      # tutto a zero per così tanto → avviso (permesso del microfono?)
RIPROVA_MICROFONO_S = 5.0
PAUSA_ERRORI_MAX_S = 60.0    # pausa massima fra due tentativi col rilevatore in errore
# Volume (RMS, int16) sopra cui un blocco conta come voce. Era 500: sul MacBook Air
# dell'operatore (prova del 2026-11-05) dopo il bip la voce non passava («torno ad
# aspettare»); con 200 sì. In una stanza rumorosa si alza dal .env.
VOCE_RMS_PREDEFINITO = 200.0
# Fetta 41: soglia della parola di attivazione mentre Gas parla. Più alta di quella
# normale (0.5) perché il microfono sente anche la voce di Gas dalle casse.
SOGLIA_INTERRUZIONE_PREDEFINITA = 0.7
RIPRODUZIONE_MAX_S = 600.0   # una frase non suona più di così (come il vecchio timeout di afplay)
BUONI_PER_AZZERARE = 125     # blocchi buoni di fila (10 s) prima di dire «di nuovo a posto»
_BIP_OK = "/System/Library/Sounds/Tink.aiff"
_BIP_ERRORE = "/System/Library/Sounds/Basso.aiff"
_HOST_LOCALI = ("127.0.0.1", "localhost", "::1")

# Fetta 39 (chat Mani, richiesta di M1): risposta «a pezzi» del server voce (righe JSON
# della V7b): la prima frase suona appena arriva, le altre in fila mentre il server
# sintetizza. «audio+pezzi» è il formato di M2 per chi non ha uno schermo (istruzione
# della voce senza schermo, tutto il parlato diviso in frasi). Un server che non lo
# conosce risponde con un solo MP3, che si suona come prima.
# Il nome del formato si può cambiare con GAS_ASCOLTO_FORMATO (vuoto = un solo MP3, come prima).
FORMATO_PEZZI = "audio+pezzi"   # M2: senza schermo, tutto il parlato a frasi
RIGA_MAX = 8 * 1024 * 1024   # una riga NDJSON (una frase in MP3 base64) non supera questo

Blocco = Sequence[int]       # BLOCCO campioni int16
Risposta = Union[bytes, Iterable[bytes]]   # un MP3 intero, oppure gli MP3 delle frasi in fila
Invia = Callable[[bytes], Tuple[bool, Optional[Risposta], str]]


# ─────────────────────────────────────────── configurazione ──

def _carica_dotenv(root: Path) -> None:
    """Carica il .env con le STESSE regole del server voce e della CLI
    (gas._carica_dotenv: commenti in linea, virgolette, BOM, GAS_NO_DOTENV, la shell
    vince), così client e server leggono lo stesso token e la stessa porta (V-1 bot
    #323). Se gas.py non si importa, ripiego su un parser semplice."""
    try:
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from gas import _carica_dotenv as carica_come_gas
        carica_come_gas(root / ".env")
        return
    except Exception as e:  # §9: si prosegue col ripiego
        log.warning(".env: caricamento di gas.py non riuscito (%s), uso il ripiego",
                    type(e).__name__)
    _carica_dotenv_ripiego(root)


def _carica_dotenv_ripiego(root: Path) -> None:
    """Ripiego: .env dalla root senza sovrascrivere le variabili già presenti."""
    if os.environ.get("GAS_NO_DOTENV", "").strip().lower() in ("1", "true", "yes", "on"):
        return
    p = root / ".env"
    try:
        righe = p.read_text(encoding="utf-8-sig").splitlines()
    except OSError:
        return
    for riga in righe:
        riga = riga.strip()
        if not riga or riga.startswith("#") or "=" not in riga:
            continue
        k, _, v = riga.partition("=")
        k = k.strip()
        if k.startswith("export "):
            k = k[len("export "):].strip()
        v = v.strip()
        tra_virgolette = re.fullmatch(r"""(['"])(.*?)\1(?:\s+#.*)?""", v)
        if tra_virgolette:
            v = tra_virgolette.group(2)
        else:
            v = re.split(r"\s+#", v, maxsplit=1)[0].rstrip()
        if k and k not in os.environ:
            os.environ[k] = v


def _numero(nome: str, default: float, minimo: float, massimo: float) -> float:
    try:
        x = float(os.environ.get(nome, "") or default)
    except ValueError:
        return default
    if not math.isfinite(x):
        return default
    return min(max(x, minimo), massimo)


def url_del_server() -> str:
    """GAS_VOICE_URL, oppure il server sul Mac alla porta GAS_VOICE_PORT (la stessa che
    usano il server voce e installa.sh: R-616-1), default 8765."""
    url = (os.environ.get("GAS_VOICE_URL") or "").strip().rstrip("/")
    if url:
        return url
    porta = "".join(c for c in os.environ.get("GAS_VOICE_PORT", "") if c.isdigit())
    return f"http://127.0.0.1:{porta or '8765'}"


def formato_richiesto() -> str:
    """GAS_ASCOLTO_FORMATO (default FORMATO_PEZZI). Solo lettere minuscole e «+», al
    massimo 40 caratteri; un valore diverso torna al default. Vuoto = niente formato (un
    solo MP3 con Accept: audio/mpeg, come prima della fetta 39)."""
    valore = os.environ.get("GAS_ASCOLTO_FORMATO")
    if valore is None:
        return FORMATO_PEZZI
    valore = valore.strip().lower()
    if re.fullmatch(r"[a-z+]{0,40}", valore):
        return valore
    log.warning("GAS_ASCOLTO_FORMATO non valido: uso %s", FORMATO_PEZZI)
    return FORMATO_PEZZI


def soglia_interruzione() -> Optional[float]:
    """Fetta 41: soglia della parola mentre Gas parla, o None se GAS_ASCOLTO_INTERRUZIONE
    è «0» (la parola allora non interrompe)."""
    if os.environ.get("GAS_ASCOLTO_INTERRUZIONE", "").strip() == "0":
        return None
    return _numero("GAS_ASCOLTO_SOGLIA_INTERRUZIONE", SOGLIA_INTERRUZIONE_PREDEFINITA,
                   0.05, 1.0)


def url_valido(url: str) -> Optional[str]:
    """Motivo se l'URL del server voce non va bene: il token viaggia in chiaro solo
    verso il Mac stesso; fuori serve https."""
    try:
        u = urllib.parse.urlsplit(url)
    except ValueError:
        return "URL non valido"
    if u.scheme not in ("http", "https") or not u.hostname:
        return "URL non valido (serve http:// o https://)"
    if u.scheme == "http" and u.hostname not in _HOST_LOCALI:
        return "fuori dal Mac serve https (il token non viaggia in chiaro)"
    return None


# ─────────────────────────────────────────── audio puro ──

def blocchi_per(secondi: float) -> int:
    """Quanti blocchi da 80 ms fanno `secondi` (conto intero: niente errori di somma)."""
    return max(1, int(round(secondi / SEC_BLOCCO)))


def rms(blocco: Blocco) -> float:
    """Energia media del blocco (radice della media dei quadrati)."""
    n = len(blocco)
    if not n:
        return 0.0
    return math.sqrt(sum(int(c) * int(c) for c in blocco) / n)


def in_wav(blocchi: List[Blocco]) -> bytes:
    """WAV in memoria (16 kHz, mono, 16 bit). Niente disco."""
    campioni = array.array("h", (int(c) for b in blocchi for c in b))
    if sys.byteorder != "little":
        campioni.byteswap()  # il WAV è little-endian
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(FREQ)
        w.writeframes(campioni.tobytes())
    return buf.getvalue()


# ─────────────────────────────────────────── ciclo ──

class Ascolto:
    """Il ciclo dell'ascolto, con le parti esterne iniettate (microfono, rilevatore,
    invio, riproduzione, bip): nei test sono finte, nessun audio vero."""

    def __init__(self, blocchi: Iterator[Blocco], rilevatore: Callable[[Blocco], float],
                 invia: Invia, riproduci: Callable[[bytes], Optional[object]],
                 bip: Callable[[str], None], *,
                 svuota: Callable[[], None] = lambda: None,
                 azzera_rilevatore: Callable[[], None] = lambda: None,
                 soglia: float = 0.5, voce_rms: float = VOCE_RMS_PREDEFINITO, silenzio_s: float = 0.8,
                 finestra_s: float = 12.0, max_turni: int = 5,
                 soglia_interruzione: Optional[float] = SOGLIA_INTERRUZIONE_PREDEFINITA,
                 dorme: Callable[[float], None] = time.sleep) -> None:
        self.blocchi = blocchi
        self.rilevatore = rilevatore
        self.invia = invia
        self.riproduci = riproduci
        self.bip = bip
        self.svuota = svuota
        self.azzera_rilevatore = azzera_rilevatore
        self.soglia = soglia
        self.voce_rms = voce_rms
        self.silenzio_s = silenzio_s
        self.finestra_s = finestra_s
        self.max_turni = max(1, int(max_turni))
        # None = la parola non interrompe Gas mentre parla (GAS_ASCOLTO_INTERRUZIONE=0)
        self.soglia_interruzione = soglia_interruzione
        self.dorme = dorme
        self.interrotto = False   # l'ultimo turno è stato interrotto dalla parola
        self._errori_rilevatore = 0
        self._buoni_di_fila = 0
        self._muti = 0

    def _prossimo(self) -> Optional[Blocco]:
        try:
            b = next(self.blocchi)
        except StopIteration:
            return None
        # Microfono tutto a zero a lungo: di solito manca il permesso di macOS.
        if len(b) and not any(b):
            self._muti += 1
            if self._muti == blocchi_per(MICROFONO_MUTO_S):
                log.warning("microfono: solo silenzio assoluto da %d s — permesso del "
                            "microfono negato? (Impostazioni → Privacy → Microfono)",
                            int(MICROFONO_MUTO_S))
        else:
            self._muti = 0
        return b

    def aspetta_parola(self) -> bool:
        """Legge blocchi finché il rilevatore supera la soglia. False a fine flusso."""
        while True:
            b = self._prossimo()
            if b is None:
                return False
            try:
                punteggio = float(self.rilevatore(b))
            except Exception as e:  # §9: un errore del modello non ferma l'ascolto
                self._errore_rilevatore(e)
                continue
            if self._errori_rilevatore:
                # V-1 ve #328: il conto si azzera solo dopo BUONI_PER_AZZERARE blocchi buoni
                # di fila, così un rilevatore che sbaglia a intermittenza non scrive due
                # righe per blocco e prende comunque le pause.
                self._buoni_di_fila += 1
                if self._buoni_di_fila >= BUONI_PER_AZZERARE:
                    log.warning("rilevatore: di nuovo a posto dopo %d errori",
                                self._errori_rilevatore)
                    self._errori_rilevatore = 0
                    self._buoni_di_fila = 0
            if punteggio >= self.soglia:
                return True

    def _errore_rilevatore(self, e: Exception) -> None:
        """V-1 ve #323: un rilevatore che fallisce non deve scrivere una riga per blocco
        (12,5 al secondo, log senza rotazione). Si scrive al 1°, 2°, 4°, 8°… errore, e dal
        3° si fa una pausa crescente (0,5 s, 1 s, 2 s… fino a PAUSA_ERRORI_MAX_S) prima di
        riprovare, buttando l'audio arrivato nel frattempo. Gli errori si contano finché
        non passano BUONI_PER_AZZERARE blocchi buoni di fila (V-1 ve #328: anche a
        intermittenza)."""
        self._errori_rilevatore += 1
        self._buoni_di_fila = 0
        n = self._errori_rilevatore
        if n & (n - 1) == 0:  # potenza di 2
            log.warning("rilevatore: errore (%s), %d recenti", type(e).__name__, n)
        if n >= 3:
            try:
                # R-624-1: esponente limitato (2**1024 non entra in un float)
                self.dorme(min(PAUSA_ERRORI_MAX_S, 0.5 * 2 ** min(n - 3, 7)))
            except Exception as e2:  # §9
                log.warning("pausa del rilevatore fallita (%s)", type(e2).__name__)
            self._svuota()

    def registra(self, iniziali: Optional[List[Blocco]] = None,
                 attesa_s: float = ATTESA_VOCE_S) -> Optional[List[Blocco]]:
        """Registra in memoria finché, dopo la voce, c'è `silenzio_s` di silenzio
        (massimo REGISTRAZIONE_MAX_S). None se la voce non arriva entro `attesa_s` o
        se il flusso finisce prima della voce."""
        presi: List[Blocco] = list(iniziali or [])
        voce = len(presi) >= blocchi_per(INIZIO_VOCE_S)
        if not voce:
            presi = []
        silenzio = attesa = 0
        max_silenzio, max_attesa = blocchi_per(self.silenzio_s), blocchi_per(attesa_s)
        while len(presi) < blocchi_per(REGISTRAZIONE_MAX_S):
            b = self._prossimo()
            if b is None:
                break
            forte = rms(b) >= self.voce_rms
            if not voce:
                # R-615-6: la voce comincia con INIZIO_VOCE_S di fila, come nella finestra
                # (un clic non apre una richiesta); il silenzio prima non si manda.
                presi = presi + [b] if forte else []
                if len(presi) >= blocchi_per(INIZIO_VOCE_S):
                    voce = True
                    continue
                attesa += 1  # R-616-2: l'attesa conta ogni blocco, anche i rumori brevi
                if attesa >= max_attesa:
                    return None
                continue
            presi.append(b)
            if forte:
                silenzio = 0
                continue
            silenzio += 1
            if silenzio >= max_silenzio:
                break
        return presi if voce else None

    def aspetta_voce(self) -> Optional[List[Blocco]]:
        """Finestra dopo la risposta: blocchi di inizio voce se parli entro
        `finestra_s` (INIZIO_VOCE_S di voce continua), altrimenti None."""
        if self.finestra_s <= 0:
            return None
        di_fila: List[Blocco] = []
        for _ in range(blocchi_per(self.finestra_s)):
            b = self._prossimo()
            if b is None:
                return None
            if rms(b) >= self.voce_rms:
                di_fila.append(b)
                if len(di_fila) >= blocchi_per(INIZIO_VOCE_S):
                    return di_fila
            else:
                di_fila = []
        return None

    def turno(self, blocchi: List[Blocco]) -> bool:
        """Invia la richiesta e riproduce la risposta: un MP3 intero, oppure (fetta 39)
        le frasi una dopo l'altra, ciascuna appena arriva. True se almeno un pezzo è
        stato suonato. Se la parola di attivazione arriva mentre Gas parla (fetta 41) la
        frase si ferma, la risposta si chiude (le frasi in fila si scartano e il server
        smette di sintetizzarle) e `self.interrotto` diventa True."""
        self.interrotto = False
        try:
            ok, risposta, motivo = self.invia(in_wav(blocchi))
        except Exception as e:  # §9
            ok, risposta, motivo = False, None, f"errore ({type(e).__name__})"
        if not ok or not risposta:
            log.warning("turno non riuscito: %s", motivo)
            self._bip("errore")
            self._svuota()  # V-3 bot #323: il bip e l'audio rimasto non vanno al rilevatore
            return False
        pezzi = iter([risposta] if isinstance(risposta, (bytes, bytearray)) else risposta)
        suonati = 0
        self._azzera()  # il rilevatore riparte pulito: ascolterà mentre Gas parla
        try:
            while True:
                try:
                    audio = next(pezzi)
                except StopIteration:
                    break
                except Exception as e:  # §9: risposta interrotta a metà
                    log.warning("risposta interrotta (%s)", type(e).__name__)
                    break
                if not audio:
                    continue
                suonati += 1
                try:
                    in_corso = self.riproduci(audio)
                except Exception as e:  # §9
                    log.warning("riproduzione fallita (%s)", type(e).__name__)
                    continue
                if self._ascolta_mentre_suona(in_corso):
                    self.interrotto = True
                    log.info("interrotto: parola di attivazione mentre Gas parlava")
                    break
        finally:
            chiudi = getattr(pezzi, "close", None)
            if chiudi is not None:  # la connessione si chiude: il server smette di sintetizzare
                try:
                    chiudi()
                except Exception as e:  # §9
                    log.warning("chiusura della risposta fallita (%s)", type(e).__name__)
            # Quello che il microfono ha sentito mentre Gas parlava è la sua voce:
            # non deve aprire un turno né attivare la parola.
            self._svuota()
        if suonati == 0:
            log.warning("turno non riuscito: risposta senza voce")
            self._bip("errore")
            self._svuota()
            return False
        return True

    def _ascolta_mentre_suona(self, in_corso: object) -> bool:
        """Fetta 41: mentre la frase suona legge il microfono e cerca SOLO la parola di
        attivazione, con `soglia_interruzione`. True = parola sentita (frase fermata).
        `in_corso` è quello che dà `riproduci`: None se ha già suonato tutto (riproduzione
        bloccante), altrimenti un oggetto con `finita()` e `ferma()`. La frase si ferma
        sempre all'uscita (anche per un'eccezione), così afplay non resta acceso."""
        if in_corso is None:
            return False
        errori = 0
        try:
            while True:
                try:
                    if in_corso.finita():  # type: ignore[attr-defined]
                        return False
                except Exception as e:  # §9: stato sconosciuto → la frase si ferma
                    log.warning("riproduzione: stato illeggibile (%s)", type(e).__name__)
                    return False
                b = self._prossimo()
                if b is None:
                    return False
                if self.soglia_interruzione is None:
                    continue
                try:
                    punteggio = float(self.rilevatore(b))
                except Exception as e:  # §9: senza rilevatore Gas finisce di parlare
                    errori += 1
                    if errori == 1:
                        log.warning("rilevatore in errore mentre Gas parla (%s)",
                                    type(e).__name__)
                    continue
                if punteggio >= self.soglia_interruzione:
                    return True
        finally:
            try:
                in_corso.ferma()  # type: ignore[attr-defined]
            except Exception as e:  # §9
                log.warning("arresto della riproduzione fallito (%s)", type(e).__name__)

    def _bip(self, tipo: str) -> None:
        try:
            self.bip(tipo)
        except Exception as e:  # §9
            log.warning("bip fallito (%s)", type(e).__name__)

    def _svuota(self) -> None:
        try:
            self.svuota()
        except Exception as e:  # §9
            log.warning("svuotamento del microfono fallito (%s)", type(e).__name__)

    def _azzera(self) -> None:
        try:
            self.azzera_rilevatore()
        except Exception as e:  # §9
            log.warning("azzeramento del rilevatore fallito (%s)", type(e).__name__)

    def conversazione(self) -> None:
        """Dopo la parola: bip, richiesta, risposta, poi la finestra per continuare."""
        log.info("parola di attivazione")
        self._bip("ok")
        self._svuota()  # il bip non deve finire nella richiesta
        richiesta = self.registra()
        turni = 0
        while richiesta is not None:
            turni += 1
            log.info("richiesta registrata (%.1f s), invio", len(richiesta) * SEC_BLOCCO)
            riuscito = self.turno(richiesta)
            if self.interrotto:
                # Fetta 41: come una parola nuova — bip, poi la nuova richiesta. I turni
                # NON ripartono da zero (R-668-1): se la voce di Gas dalle casse facesse
                # scattare la parola, le interruzioni di fila restano sotto max_turni.
                if turni >= self.max_turni:
                    break
                self._azzera()
                self._bip("ok")
                self._svuota()
                richiesta = self.registra()
                continue
            if not riuscito or turni >= self.max_turni:
                break
            inizio = self.aspetta_voce()
            if inizio is None:
                break
            richiesta = self.registra(inizio)
        self._azzera()
        log.info("torno ad aspettare la parola di attivazione")

    def gira(self) -> None:
        """Ciclo principale: torna quando il flusso dei blocchi finisce."""
        while self.aspetta_parola():
            try:
                self.conversazione()
            except Exception as e:  # §9: un turno rotto non spegne l'ascolto
                log.warning("conversazione interrotta (%s)", type(e).__name__)


# ─────────────────────────────────────────── parti vere (Mac) ──

class _NienteRedirect(urllib.request.HTTPRedirectHandler):
    """R-615-2: nessun redirect, così il Bearer non va mai su un altro host."""
    def redirect_request(self, *a, **k):  # type: ignore[override]
        return None


# R-615-2: niente proxy di sistema (su macOS valgono anche per 127.0.0.1) e niente redirect.
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}), _NienteRedirect)


def _audio_da_base64(valore: object) -> Optional[bytes]:
    if not isinstance(valore, str) or not valore:
        return None
    return base64.b64decode(valore, validate=True)


def _frasi_ndjson(r) -> Iterator[bytes]:
    """Fetta 39: legge le righe JSON della risposta a pezzi (V7b) e dà l'MP3 di ogni
    frase appena la sua riga arriva. Si ferma su «fine», su «errore_voce» (il server ha
    smesso di sintetizzare) o a fine connessione. Una riga rotta o troppo lunga alza
    un'eccezione: il turno la prende (§9). La connessione si chiude sempre."""
    try:
        while True:
            riga = r.readline(RIGA_MAX + 1)
            if not riga:
                return
            if len(riga) > RIGA_MAX:
                raise ValueError("riga troppo lunga")
            riga = riga.strip()
            if not riga:
                continue
            dati = json.loads(riga)
            if not isinstance(dati, dict):
                raise ValueError("riga non valida")
            audio = _audio_da_base64(dati.get("audio"))
            if audio:
                yield audio
            if dati.get("errore_voce"):
                log.warning("voce interrotta dal server a metà risposta")
                return
            if dati.get("fine"):
                return
    finally:
        r.close()


def invia_al_server(url: str, token: str, timeout: float,
                    formato: Optional[str] = None) -> Invia:
    """POST /voice col WAV. Con un formato (default quello a pezzi, fetta 39) la
    risposta può essere a righe JSON (le frasi in fila), JSON con un solo audio, oppure
    audio/mpeg; senza formato solo audio/mpeg, come prima. Mai il token nei log."""
    formato = formato_richiesto() if formato is None else formato
    intestazioni = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "audio/wav",
        "Accept": "audio/mpeg",
    }
    if formato:
        intestazioni["X-Gas-Formato"] = formato

    def _invia(wav: bytes) -> Tuple[bool, Optional[Risposta], str]:
        req = urllib.request.Request(f"{url}/voice", data=wav, method="POST",
                                     headers=intestazioni)
        try:
            r = _OPENER.open(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            e.close()
            return False, None, f"HTTP {e.code}"
        except Exception as e:  # rete, timeout
            return False, None, f"server voce non raggiungibile ({type(e).__name__})"
        a_pezzi = False
        try:
            tipo = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if r.status != 200:
                return False, None, f"risposta inattesa (HTTP {r.status}, {tipo or '?'})"
            if tipo == "application/x-ndjson" and formato:
                a_pezzi = True  # la connessione resta aperta: la chiude _frasi_ndjson
                return True, _frasi_ndjson(r), ""
            if tipo.startswith("audio/"):
                return True, r.read(), ""
            if tipo == "application/json" and formato:
                dati = json.loads(r.read())
                audio = _audio_da_base64(dati.get("audio")) if isinstance(dati, dict) else None
                if audio:
                    return True, audio, ""
                return False, None, "risposta inattesa (senza voce)"
            return False, None, f"risposta inattesa (HTTP {r.status}, {tipo or '?'})"
        except Exception as e:  # corpo rotto o connessione caduta
            return False, None, f"risposta inattesa ({type(e).__name__})"
        finally:
            if not a_pezzi:
                r.close()
    return _invia


class RiproduzioneAfplay:
    """Fetta 41: una frase di Gas che suona con afplay in sottofondo, così intanto si
    ascolta il microfono. File temporaneo 0600 in una cartella propria, cancellato quando
    la frase finisce o si ferma (anche se afplay non parte)."""

    def __init__(self, audio: bytes, adesso: Callable[[], float] = time.monotonic) -> None:
        self._adesso = adesso
        self._cartella = tempfile.mkdtemp(prefix="gas-voce-")
        try:
            percorso = os.path.join(self._cartella, "risposta.mp3")
            fd = os.open(percorso, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "wb") as f:
                f.write(audio)
            self._proc = subprocess.Popen(["afplay", percorso], stdout=subprocess.DEVNULL,
                                          stderr=subprocess.DEVNULL)
        except BaseException:
            shutil.rmtree(self._cartella, ignore_errors=True)
            raise
        self._inizio = adesso()

    def finita(self) -> bool:
        if self._proc.poll() is None and self._adesso() - self._inizio < RIPRODUZIONE_MAX_S:
            return False
        self.ferma()
        return True

    def ferma(self) -> None:
        """Ferma afplay (se suona ancora) e cancella il file. Si può chiamare più volte."""
        try:
            if self._proc.poll() is None:
                self._proc.terminate()
                try:
                    self._proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self._proc.kill()
                    self._proc.wait(timeout=2)
        finally:
            shutil.rmtree(self._cartella, ignore_errors=True)


def riproduci_afplay(audio: bytes) -> RiproduzioneAfplay:
    """Avvia la frase di Gas e torna subito: il ciclo dell'ascolto la segue con `finita()`
    e la ferma con `ferma()` (fetta 41)."""
    return RiproduzioneAfplay(audio)


def bip_di_sistema(tipo: str) -> None:
    suono = _BIP_OK if tipo == "ok" else _BIP_ERRORE
    if os.path.exists(suono):
        subprocess.run(["afplay", suono], check=False, timeout=5,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class Microfono:
    """Microfono con sounddevice (16 kHz, mono, int16, blocchi da 80 ms)."""

    def __init__(self) -> None:
        import sounddevice as sd  # solo sul Mac: clients/voice/requirements-ascolto.txt
        self._sd = sd
        self._stream = sd.InputStream(samplerate=FREQ, channels=1, dtype="int16",
                                      blocksize=BLOCCO)
        self._stream.start()

    def blocchi(self) -> Iterator[Blocco]:
        while True:
            dati, _ = self._stream.read(BLOCCO)
            yield dati[:, 0]

    def svuota(self) -> None:
        n = self._stream.read_available
        if n > 0:
            self._stream.read(n)

    def chiudi(self) -> None:
        try:
            self._stream.stop()
            self._stream.close()
        except Exception:
            pass


def rilevatore_openwakeword(modello: str) -> Tuple[Callable[[Blocco], float],
                                                   Callable[[], None]]:
    """(punteggio del blocco, azzera) col modello pronto di openWakeWord, in locale."""
    import numpy as np
    from openwakeword.model import Model
    m = Model(wakeword_models=[modello], inference_framework="onnx")

    def punteggio(b: Blocco) -> float:
        risultati = m.predict(np.asarray(b, dtype=np.int16))
        return max(risultati.values()) if risultati else 0.0
    return punteggio, m.reset


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    _carica_dotenv(_GAS_ROOT)
    token = os.environ.get("GAS_VOICE_TOKEN", "").strip()
    if not token:
        log.error("GAS_VOICE_TOKEN non configurato (.env): l'ascolto non parte.")
        return 1
    url = url_del_server()
    motivo = url_valido(url)
    if motivo:
        log.error("GAS_VOICE_URL: %s — l'ascolto non parte.", motivo)
        return 1
    modello = (os.environ.get("GAS_ASCOLTO_MODELLO") or "hey_jarvis").strip()
    try:
        punteggio, azzera = rilevatore_openwakeword(modello)
    except Exception as e:
        log.error("openWakeWord non pronto (%s): installa con scripts/voce/installa.sh.",
                  type(e).__name__)
        return 1
    invia = invia_al_server(url, token, _numero("GAS_VOICE_TIMEOUT", 600, 5, 3600))
    log.info("ascolto pronto: parola «%s», server %s", modello, url)
    while True:
        mic = None
        try:
            mic = Microfono()
            Ascolto(mic.blocchi(), punteggio, invia, riproduci_afplay, bip_di_sistema,
                    svuota=mic.svuota, azzera_rilevatore=azzera,
                    soglia=_numero("GAS_ASCOLTO_SOGLIA", 0.5, 0.05, 0.99),
                    voce_rms=_numero("GAS_ASCOLTO_VOCE_RMS", VOCE_RMS_PREDEFINITO, 10, 30000),
                    silenzio_s=_numero("GAS_ASCOLTO_SILENZIO", 0.8, 0.2, 5),
                    finestra_s=_numero("GAS_VOICE_FINESTRA", 12, 0, 120),
                    max_turni=int(_numero("GAS_VOICE_MAX_TURNI", 5, 1, 50)),
                    soglia_interruzione=soglia_interruzione()).gira()
        except KeyboardInterrupt:
            return 0
        except Exception as e:  # §9: microfono staccato o simili → si riprova
            log.warning("microfono non disponibile (%s): riprovo tra %d s",
                        type(e).__name__, int(RIPROVA_MICROFONO_S))
        finally:
            if mic is not None:
                mic.chiudi()
        time.sleep(RIPROVA_MICROFONO_S)


if __name__ == "__main__":
    sys.exit(main())
