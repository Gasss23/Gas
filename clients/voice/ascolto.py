#!/usr/bin/env python3
"""
clients/voice/ascolto.py — voce H24 sul Mac (R8, chat Mani).

Gas sempre in ascolto: microfono aperto, parola di attivazione in LOCALE con
openWakeWord (per ora il modello pronto «hey_jarvis»: «Ehi Gas» va addestrato in una
fetta a parte), poi bip, registrazione fino al silenzio, invio al server voce già
esistente (modules/voice/server.py, POST /voice) e risposta riprodotta: con la risposta
«a pezzi» del server (righe JSON, formato audio+pezzi) la prima frase suona appena arriva e le altre in
fila, mentre il server sintetizza le successive (fetta 39). Dopo la risposta
si torna ad aspettare la parola: i turni di seguito senza parola sono spenti di default
(GAS_VOICE_MAX_TURNI=1). Con GAS_VOICE_MAX_TURNI più alto resta una finestra di ascolto
(GAS_VOICE_FINESTRA, 10 s) per continuare senza ripetere la parola, fino a quei turni.
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
    GAS_VOICE_FINESTRA     — secondi di ascolto dopo la risposta (default 10)
    GAS_VOICE_SEGUITO_MAX  — secondi massimi di una richiesta di seguito, senza parola
                             (default 15): chi parla più a lungo non sta parlando a Gas
    GAS_VOICE_MAX_TURNI    — turni dopo la parola, il primo compreso (default 1: nessun seguito)
    GAS_ASCOLTO_MODELLO    — modello di openWakeWord (default hey_jarvis)
    GAS_ASCOLTO_SOGLIA     — soglia della parola di attivazione, 0-1 (default 0.7)
    GAS_ASCOLTO_BLOCCHI_PAROLA — blocchi da 80 ms di fila sopra soglia per la parola, 1-5 (default 3)
    GAS_ASCOLTO_VOCE_RMS   — energia sopra cui c'è voce (default 200, campioni int16)
    GAS_ASCOLTO_SILENZIO   — secondi di silenzio che chiudono la richiesta (default 0.8)
    GAS_ASCOLTO_INTERRUZIONE — 0 = la parola non interrompe Gas mentre parla (default 1)
    GAS_ASCOLTO_CONFERMA   — 0 = dopo la parola solo il bip, senza «Sì, signore?» (default 1)
    GAS_ASCOLTO_SOGLIA_INTERRUZIONE — soglia della parola mentre Gas parla, 0-1 (default 0.8)
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
import threading
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
# Fetta 43 parte 2 (operatore, 5 novembre): nella finestra dopo la risposta il microfono
# catturava la conversazione della stanza (4 richieste di fila da 30 s). Difese:
# - finestra senza voce prima di tornare ad aspettare la parola (era 40 s; ora
#   FINESTRA_PREDEFINITA_S, e i seguiti sono spenti di default: MAX_TURNI_PREDEFINITO);
# - i turni di seguito (senza parola) durano al massimo SEGUITO_MAX_S: una registrazione
#   che ci arriva NON si invia e la conversazione si chiude (quasi sempre è parlato della
#   stanza);
# - i turni di seguito portano «X-Gas-Seguito: 1»: il server (V15 di M2, PR #339) fa
#   decidere al cervello se il parlato è per Gas e, se no, risponde «X-Gas-Comando: fine»
#   senza voce; «X-Gas-Comando: pausa» chiude la conversazione («Va bene.» solo dopo
#   la parola, muta nel seguito);
# - nella finestra il rilevatore resta acceso: «Hey Jarvis, …» è un turno normale (V-1 bot #341);
# - un errore in un turno di seguito chiude la conversazione senza bip (R-675-5-M2).
FINESTRA_PREDEFINITA_S = 10.0
# V-1 bot #341 su 23d9c1c (= R-693-2): se la parola si sente a metà di un turno di seguito,
# della registrazione si tiene solo da poco prima della parola (openWakeWord la segnala a
# fine parola): il parlato della stanza detto prima non parte come richiesta normale.
PRIMA_DELLA_PAROLA_S = 1.5
# V-1 della verifica esterna su 562f137 (= R-680-2): la parola sentita nella finestra conta
# solo se la voce comincia entro questo tempo; una parola (o un falso positivo) sentita molto
# prima non rende «normale» il parlato che arriva dopo.
PAROLA_VALIDA_S = 2.0
SEGUITO_MAX_PREDEFINITO_S = 15.0
# Correzione del 10/11/2026 (log dell'operatore: Jarvis risponde senza essere chiamato):
# al massimo 2 turni di seguito dopo la parola (3 turni in tutto), finestra di 15 s.
# Sera del 10/11 (operatore: «a volte anche mentre parlo per cazzi miei mi risponde»,
# obiettivo zero risposte non richieste): i turni di seguito senza parola sono SPENTI di
# default (1 = solo la richiesta dopo «Hey Jarvis»); si riaccendono con GAS_VOICE_MAX_TURNI.
# La finestra (10 s) resta per chi li riaccende.
MAX_TURNI_PREDEFINITO = 1
# Stessa correzione: soglia predefinita della parola 0,6 (era 0,5) e parola valida solo se il
# rilevatore la sente in BLOCCHI_PAROLA_PREDEFINITO blocchi di fila (un picco isolato di
# 80 ms era la causa dei falsi «Hey Jarvis»). Nella finestra si ignora il primo mezzo
# secondo: è la coda dell'eco della voce di Gas nella stanza.
# Sera del 10/11: più severi (0,7 e 3 blocchi, cioè 240 ms di fila sopra soglia). Se la
# parola vera non scatta più: GAS_ASCOLTO_SOGLIA=0.6 o GAS_ASCOLTO_BLOCCHI_PAROLA=2.
SOGLIA_PREDEFINITA = 0.7
BLOCCHI_PAROLA_PREDEFINITO = 3
CODA_ECO_S = 0.5
# Prova dal vivo del 10/11/2026: 6 volte su 8 «Hey Jarvis, …» detto tutto d'un fiato andava
# perso, perché la richiesta cadeva mentre suonava «Sì, signore?» (audio buttato) e dopo
# restava solo silenzio. Ora, prima della conferma, si ascolta per SUBITO_S: se c'è già
# voce continua per SUBITO_VOCE_S, niente conferma e quei blocchi aprono la richiesta.
# R-753-1-M1: SUBITO_VOCE_S è più lunga della coda di «…vis» (rilevatore che scatta prima
# della fine della parola): una coda seguita da una pausa non salta la conferma.
SUBITO_S = 0.6
SUBITO_VOCE_S = 0.4
COMANDI = ("fine", "pausa")   # valori di X-Gas-Comando che il client conosce
# Riserva della #336 (eco): se la risposta di Gas contiene la parola di attivazione
# («…di' Hey Jarvis…»), le casse la mandano al microfono e Gas si interromperebbe da solo.
# Il testo della risposta arriva con la prima riga a pezzi («content»): se contiene la
# parola, per quella risposta l'interruzione si spegne (resta il Terminale o la fine).
PAROLA_NEL_TESTO = re.compile(r"\bjarvis\b|\b(?:hey|ehi|ehy)\s+gas\b", re.IGNORECASE)
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
# normale (SOGLIA_PREDEFINITA) perché il microfono sente anche la voce di Gas dalle casse.
# Sera del 10/11: 0,8, sempre sopra SOGLIA_PREDEFINITA (che è salita a 0,7).
SOGLIA_INTERRUZIONE_PREDEFINITA = 0.8
# R-757-1-M1: turni ammessi quando si interrompe Gas con la parola, anche se max_turni è
# più basso (1 = seguiti spenti): la richiesta più una interruzione con la nuova domanda.
TURNI_CON_INTERRUZIONE = 2
# Fetta 42: «Sì, signore?» detto da Jarvis dopo la parola, al posto del bip. L'audio lo
# prepara il server voce (GET /voce/conferma, cache per voce lato server, PR #335 di M2);
# il client lo scarica in sottofondo e lo tiene in memoria. Qualsiasi errore → bip.
CONFERMA_PERCORSO = "/voce/conferma"
CONFERMA_MAX_BYTE = 200 * 1024    # «Sì, signore?» è qualche decina di KB (R-671-3)
CONFERMA_TIMEOUT_S = 10.0
CONFERMA_RIPROVA_S = 60.0         # dopo un errore si riprova al più una volta al minuto
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
# (ok, risposta, motivo) oppure, dalla fetta 43 parte 2, (ok, risposta, motivo, comando):
# comando è «fine», «pausa» o "" (X-Gas-Comando del server).
Esito = Union[Tuple[bool, Optional[Risposta], str], Tuple[bool, Optional[Risposta], str, str]]
Invia = Callable[[bytes], Esito]


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


def _finestra_dall_ambiente() -> float:
    """GAS_VOICE_FINESTRA nei limiti 0–120 (V-1 bot su a269c12). Un numero fuori dai limiti
    si corregge con un avviso nel log (V-3 bot #347): la pagina web della voce, che usa la
    stessa variabile, non parte con un valore oltre 120."""
    finestra = _numero("GAS_VOICE_FINESTRA", FINESTRA_PREDEFINITA_S, 0, 120)
    grezzo = (os.environ.get("GAS_VOICE_FINESTRA") or "").strip()
    try:
        x = float(grezzo) if grezzo else finestra
    except ValueError:
        x = finestra
    if math.isfinite(x) and x != finestra:
        log.warning("GAS_VOICE_FINESTRA=%s fuori dai limiti 0–120: uso %g", grezzo, finestra)
    return finestra


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
    invio, riproduzione, bip): nei test sono finte, nessun audio vero.
    I default del costruttore sono quelli dei test (seguiti accesi, soglie basse): i
    valori veri, più severi, li passa sempre `main` (*_PREDEFINITO/A)."""

    def __init__(self, blocchi: Iterator[Blocco], rilevatore: Callable[[Blocco], float],
                 invia: Invia, riproduci: Callable[[bytes], Optional[object]],
                 bip: Callable[[str], None], *,
                 svuota: Callable[[], None] = lambda: None,
                 azzera_rilevatore: Callable[[], None] = lambda: None,
                 soglia: float = 0.5, voce_rms: float = VOCE_RMS_PREDEFINITO, silenzio_s: float = 0.8,
                 finestra_s: float = 15.0, max_turni: int = 3,
                 seguito_max_s: float = SEGUITO_MAX_PREDEFINITO_S,
                 invia_seguito: Optional[Invia] = None,
                 soglia_interruzione: Optional[float] = 0.7,
                 conferma: Callable[[], Optional[bytes]] = lambda: None,
                 dorme: Callable[[float], None] = time.sleep,
                 blocchi_parola: int = 1, coda_eco_s: float = 0.0,
                 subito_s: float = 0.0) -> None:
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
        # blocchi di fila sopra soglia per la parola (main: BLOCCHI_PAROLA_PREDEFINITO; il
        # default 1 del costruttore è quello dei rilevatori finti dei test)
        self.blocchi_parola = max(1, int(blocchi_parola))
        self.coda_eco_s = max(0.0, float(coda_eco_s))
        # quanto si ascolta dopo la parola prima di «Sì, signore?» (main: SUBITO_S; il
        # default 0 del costruttore è quello dei test che si aspettano sempre la conferma)
        self.subito_s = max(0.0, float(subito_s))
        # None = la parola non interrompe Gas mentre parla (GAS_ASCOLTO_INTERRUZIONE=0)
        self.soglia_interruzione = soglia_interruzione
        # Fetta 42: l'audio di «Sì, signore?» (None = non pronto o spento → bip)
        self.conferma = conferma
        self.dorme = dorme
        self.interrotto = False   # l'ultimo turno è stato interrotto dalla parola
        # Fetta 43 parte 2: i turni di seguito vanno al server con X-Gas-Seguito: 1
        self.invia_seguito = invia_seguito or invia
        self.seguito_max_s = seguito_max_s
        self.chiudi = False       # l'ultimo turno chiede di chiudere la conversazione
        self.parola_nella_finestra = False   # la parola è stata detta nella finestra
        self._errori_rilevatore = 0
        self._errori_parola = 0
        # Misura per tarare (solo numeri, mai audio): punteggio massimo della parola che ha
        # appena attivato e quante salite sopra soglia troppo corte sono state scartate
        # dall'attivazione precedente (falsi «Hey Jarvis» fermati dai blocchi di fila).
        self.punteggio_parola = 0.0
        self.picchi_scartati = 0
        self._sopra_finestra = 0   # V-1 ve #361: blocchi di fila sopra soglia nella finestra
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
        """Legge blocchi finché il rilevatore supera la soglia per `blocchi_parola` blocchi
        di fila. False a fine flusso. Un errore del rilevatore azzera il conto.
        Lascia in `punteggio_parola` il punteggio massimo della corsa che ha attivato e in
        `picchi_scartati` le corse sopra soglia troppo corte viste prima."""
        sopra = 0
        massimo = 0.0
        self.picchi_scartati = 0
        while True:
            b = self._prossimo()
            if b is None:
                return False
            try:
                punteggio = float(self.rilevatore(b))
            except Exception as e:  # §9: un errore del modello non ferma l'ascolto
                self._errore_rilevatore(e)
                if sopra:
                    self.picchi_scartati += 1
                sopra = 0
                massimo = 0.0
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
                sopra += 1
                massimo = max(massimo, punteggio)
                if sopra >= self.blocchi_parola:
                    self.punteggio_parola = massimo
                    return True
            else:
                if sopra:
                    self.picchi_scartati += 1
                sopra = 0
                massimo = 0.0

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

    def _parola_nel_blocco(self, b: Blocco) -> bool:
        """V-1 bot #341: nella finestra il rilevatore resta acceso. True se la parola di
        attivazione è nel blocco; un errore del rilevatore vale «no» (§9).
        V-1 ve #361: come in `aspetta_parola`, la parola vale solo dopo `blocchi_parola`
        blocchi di fila sopra soglia (un picco isolato non apre un turno normale); il conto
        si azzera sotto soglia, su errore e quando la parola scatta."""
        try:
            sopra = float(self.rilevatore(b)) >= self.soglia
        except Exception as e:
            self._sopra_finestra = 0
            # R-681-1: l'errore resta «no», ma lascia traccia nel log (il primo e poi uno
            # ogni 100, per non riempirlo a ogni blocco).
            self._errori_parola += 1
            if self._errori_parola % 100 == 1:
                log.warning("rilevatore in errore nella finestra (%s), errori finora: %d",
                            type(e).__name__, self._errori_parola)
            return False
        if not sopra:
            self._sopra_finestra = 0
            return False
        self._sopra_finestra += 1
        if self._sopra_finestra < self.blocchi_parola:
            return False
        self._sopra_finestra = 0
        self.parola_nella_finestra = True
        return True

    def registra(self, iniziali: Optional[List[Blocco]] = None,
                 attesa_s: float = ATTESA_VOCE_S,
                 max_s: float = REGISTRAZIONE_MAX_S,
                 rileva_parola: bool = False,
                 subito: bool = False) -> Optional[List[Blocco]]:
        """Registra in memoria finché, dopo la voce, c'è `silenzio_s` di silenzio
        (massimo `max_s`). None se la voce non arriva entro `attesa_s` o
        se il flusso finisce prima della voce.
        `subito` (V-1 verifica esterna #368): `iniziali` viene da `_voce_subito` e può
        essere solo la coda di «…vis». Come dopo una parola nella finestra si tollera il
        silenzio fino ad `attesa_s`; se dopo quei blocchi non arriva altra voce continua
        (INIZIO_VOCE_S) torna None: niente mezzo secondo di coda a Whisper (risposte
        inventate come «Di niente»); chi chiama ripiega sulla conferma."""
        presi: List[Blocco] = list(iniziali or [])
        voce = len(presi) >= blocchi_per(INIZIO_VOCE_S)
        if not voce:
            presi = []
        silenzio = attesa = 0
        max_silenzio, max_attesa = blocchi_per(self.silenzio_s), blocchi_per(attesa_s)
        # V-1 bot su 179d05c: dopo una parola sentita qui non c'è il bip, quindi chi aspetta
        # un attimo prima di parlare non deve vedersi chiudere la richiesta: finché dopo la
        # parola non c'è voce continua (INIZIO_VOCE_S) si tollera il silenzio fino ad
        # ATTESA_VOCE_S, come dopo la parola fuori dalla finestra.
        # R-702-1: la tolleranza ha un tetto suo (come l'attesa, R-616-2): dopo ATTESA_VOCE_S
        # dalla parola finisce comunque, anche se rumori brevi l'hanno tenuta viva.
        dopo_parola = subito and voce
        confermata = not dopo_parola
        forti_dopo = dal_la_parola = 0
        while len(presi) < blocchi_per(max_s):
            b = self._prossimo()
            if b is None:
                break
            if rileva_parola and self._parola_nel_blocco(b):
                # «Hey Jarvis, …» detto nella finestra: è una richiesta con la parola, il
                # tetto torna quello normale (V-1 bot #341). Si butta il parlato di prima
                # della parola (V-1 bot su 23d9c1c): resta solo la parola e il dopo.
                rileva_parola = False
                max_s = REGISTRAZIONE_MAX_S
                tieni = max(0, blocchi_per(PRIMA_DELLA_PAROLA_S) - 1)
                presi = presi[-tieni:] if tieni else []
                if voce:
                    presi.append(b)
                    silenzio, dopo_parola, forti_dopo, dal_la_parola = 0, True, 0, 0
                    continue
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
            if dopo_parola:
                dal_la_parola += 1
                if dal_la_parola >= max_attesa:
                    dopo_parola = False
            if forte:
                silenzio = 0
                # V-2 ve #368 (2° giro): finché la richiesta non è confermata i blocchi forti
                # si contano anche dopo la tolleranza, così la voce che parte verso la fine
                # dei 5 s conferma la richiesta invece di farla scartare.
                if dopo_parola or not confermata:
                    forti_dopo += 1
                    if forti_dopo >= blocchi_per(INIZIO_VOCE_S):
                        dopo_parola = False
                        confermata = True
                continue
            forti_dopo = 0
            silenzio += 1
            if silenzio >= (max_attesa if dopo_parola else max_silenzio):
                break
        if not confermata:
            return None
        return presi if voce else None

    def aspetta_voce(self) -> Optional[List[Blocco]]:
        """Finestra dopo la risposta: blocchi di inizio voce se parli entro
        `finestra_s` (INIZIO_VOCE_S di voce continua), altrimenti None."""
        if self.finestra_s <= 0:
            return None
        # coda dell'eco: i primi blocchi dopo la voce di Gas non aprono un turno
        for _ in range(blocchi_per(self.coda_eco_s) if self.coda_eco_s > 0 else 0):
            if self._prossimo() is None:
                return None
        self._sopra_finestra = 0   # V-1 ve #361: il conto riparte con la finestra
        di_fila: List[Blocco] = []
        da_parola: Optional[int] = None   # blocchi passati dall'ultima parola sentita
        for _ in range(blocchi_per(self.finestra_s)):
            b = self._prossimo()
            if b is None:
                return None
            if self._parola_nel_blocco(b):  # V-1 bot #341: il rilevatore resta acceso
                da_parola = 0
            elif da_parola is not None:
                da_parola += 1
                if da_parola > blocchi_per(PAROLA_VALIDA_S):
                    # parola troppo lontana dall'inizio della voce: non conta (R-680-2)
                    self.parola_nella_finestra = False
                    da_parola = None
            if rms(b) >= self.voce_rms:
                di_fila.append(b)
                if len(di_fila) >= blocchi_per(INIZIO_VOCE_S):
                    return di_fila
            else:
                di_fila = []
        return None

    def turno(self, blocchi: List[Blocco], seguito: bool = False) -> bool:
        """Invia la richiesta e riproduce la risposta: un MP3 intero, oppure (fetta 39)
        le frasi una dopo l'altra, ciascuna appena arriva. True se almeno un pezzo è
        stato suonato. Se la parola di attivazione arriva mentre Gas parla (fetta 41) la
        frase si ferma, la risposta si chiude (le frasi in fila si scartano e il server
        smette di sintetizzarle) e `self.interrotto` diventa True.
        Fetta 43 parte 2: `seguito` = turno nella finestra, senza parola. Se il server dice
        «fine» o «pausa», o se un turno di seguito non riesce, `self.chiudi` diventa True e
        la conversazione si chiude (senza bip nei turni di seguito)."""
        self.interrotto = False
        self.chiudi = False
        comando = ""
        # Velocità (notte del 9 nov): quanto passa da fine richiesta alla prima frase di Gas
        # (invio, server, prima frase pronta). Solo una riga INFO nel log dell'ascolto, per
        # misurare dal vero sul Mac dove si perde tempo; non cambia il comportamento.
        t0 = time.monotonic()
        try:
            esito = (self.invia_seguito if seguito else self.invia)(in_wav(blocchi))
            ok, risposta, motivo = esito[0], esito[1], esito[2]
            if len(esito) > 3 and esito[3] in COMANDI:
                comando = esito[3]
        except Exception as e:  # §9
            ok, risposta, motivo = False, None, f"errore ({type(e).__name__})"
        if comando == "fine":
            log.info("turno di seguito non rivolto a Gas: chiudo la conversazione")
            self.chiudi = True
            self._svuota()
            return False
        if comando == "pausa":
            log.info("pausa a voce: chiudo la conversazione")
            self.chiudi = True
        if not ok or not risposta:
            if seguito or comando == "pausa":
                # R-675-5-M2: un turno di seguito che non riesce (500 col forte spento, 429…)
                # chiude la conversazione in silenzio, mai bip a ripetizione.
                # R-679-3: la pausa muta (risposta giusta, senza voce) non è un errore ed è già
                # nel log; un errore vero si scrive sempre col suo motivo (R-707-3).
                if not (comando == "pausa" and ok):
                    log.warning("turno di seguito non riuscito: %s; chiudo la conversazione",
                                motivo)
                self.chiudi = True
            else:
                log.warning("turno non riuscito: %s", motivo)
                self._bip("errore")
            self._svuota()  # V-3 bot #323: il bip e l'audio rimasto non vanno al rilevatore
            return False
        pezzi = iter([risposta] if isinstance(risposta, (bytes, bytearray)) else risposta)
        suonati = 0
        interrompibile = True
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
                if interrompibile and PAROLA_NEL_TESTO.search(getattr(pezzi, "testo", "") or ""):
                    interrompibile = False
                    log.info("la risposta contiene la parola di attivazione: niente "
                             "interruzione mentre Gas parla (eco delle casse)")
                suonati += 1
                if suonati == 1:
                    log.info("tempo: prima frase di Gas dopo %.2f s dalla fine della richiesta",
                             time.monotonic() - t0)
                try:
                    in_corso = self.riproduci(audio)
                except Exception as e:  # §9
                    log.warning("riproduzione fallita (%s)", type(e).__name__)
                    continue
                if self._ascolta_mentre_suona(in_corso, interrompibile=interrompibile):
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
            if seguito or comando == "pausa":
                if comando != "pausa":  # la pausa è già nel log
                    log.warning("turno di seguito senza voce: chiudo la conversazione")
                self.chiudi = True
            else:
                log.warning("turno non riuscito: risposta senza voce")
                self._bip("errore")
            self._svuota()
            return False
        return True

    def _ascolta_mentre_suona(self, in_corso: object, interrompibile: bool = True) -> bool:
        """Fetta 41: mentre la frase suona legge il microfono e cerca SOLO la parola di
        attivazione, con `soglia_interruzione`. True = parola sentita (frase fermata).
        `in_corso` è quello che dà `riproduci`: None se ha già suonato tutto (riproduzione
        bloccante), altrimenti un oggetto con `finita()` e `ferma()`. La frase si ferma
        sempre all'uscita (anche per un'eccezione), così afplay non resta acceso."""
        if in_corso is None:
            return False
        errori = 0
        # V-1 bot #371: come fuori, la parola vale solo con `blocchi_parola` blocchi di fila
        # sopra soglia: un picco isolato (voce di Gas o stanza) non interrompe e non apre
        # una richiesta. Il conto si azzera sotto soglia e su errore.
        sopra = 0
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
                if self.soglia_interruzione is None or not interrompibile:
                    continue
                try:
                    punteggio = float(self.rilevatore(b))
                except Exception as e:  # §9: senza rilevatore Gas finisce di parlare
                    errori += 1
                    sopra = 0
                    if errori == 1:
                        log.warning("rilevatore in errore mentre Gas parla (%s)",
                                    type(e).__name__)
                    continue
                if punteggio >= self.soglia_interruzione:
                    sopra += 1
                    if sopra >= self.blocchi_parola:
                        return True
                else:
                    sopra = 0
        finally:
            try:
                in_corso.ferma()  # type: ignore[attr-defined]
            except Exception as e:  # §9
                log.warning("arresto della riproduzione fallito (%s)", type(e).__name__)

    def _voce_subito(self) -> Optional[List[Blocco]]:
        """Dopo la parola ascolta per `subito_s`: se c'è voce continua per SUBITO_VOCE_S
        (chi dice la richiesta d'un fiato) torna i blocchi letti, che aprono la richiesta;
        altrimenti None (si suona la conferma e quei blocchi si buttano).
        R-753-2-M1: se allo scadere la voce è appena partita, si continua a leggere finché
        non si decide (al massimo SUBITO_VOCE_S in più), così la conferma non le suona sopra."""
        if self.subito_s <= 0:
            return None
        servono = blocchi_per(SUBITO_VOCE_S)
        finestra = blocchi_per(self.subito_s)
        letti: List[Blocco] = []
        di_fila = 0
        while len(letti) < finestra or (di_fila and len(letti) < finestra + servono):
            b = self._prossimo()
            if b is None:
                return None
            letti.append(b)
            di_fila = di_fila + 1 if rms(b) >= self.voce_rms else 0
            if di_fila >= servono:
                return letti
        return None

    def _conferma_o_bip(self) -> None:
        """Fetta 42: dopo la parola Jarvis dice «Sì, signore?» (audio del server, in
        memoria); se non è pronto o qualcosa va storto, il bip di sempre. La conferma
        non si interrompe: è breve, e quello che il microfono sente intanto si butta."""
        try:
            audio = self.conferma()
        except Exception as e:  # §9
            log.warning("conferma non disponibile (%s)", type(e).__name__)
            audio = None
        if not audio:
            self._bip("ok")
            return
        try:
            in_corso = self.riproduci(audio)
        except Exception as e:  # §9
            log.warning("conferma non riprodotta (%s): bip", type(e).__name__)
            self._bip("ok")
            return
        self._ascolta_mentre_suona(in_corso, interrompibile=False)

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
        """Dopo la parola: «Sì, signore?» (o il bip), richiesta, risposta, poi la finestra
        per continuare."""
        log.info("parola di attivazione (punteggio %.2f, picchi corti scartati prima: %d)",
                 self.punteggio_parola, self.picchi_scartati)
        subito = self._voce_subito()
        if subito:
            # «Hey Jarvis, che ore sono» d'un fiato: niente conferma (coprirebbe la richiesta
            # e andrebbe buttata), si registra da qui. Non suona niente, quindi niente eco.
            log.info("voce subito dopo la parola: niente conferma, registro")
            richiesta = self.registra(subito, subito=True)
            if richiesta is None:
                # V-1 ve #368 (2° giro): richiesta brevissima («Hey Jarvis, pausa») o solo
                # la coda della parola: niente a Whisper, ma nemmeno silenzio. Si ripiega
                # su «Sì, signore?» e si ascolta di nuovo, così si sa che va ripetuta.
                log.info("dopo la parola solo un attimo di voce: chiedo con la conferma")
                self._conferma_o_bip()
                self._svuota()
                richiesta = self.registra()
        else:
            self._conferma_o_bip()
            self._svuota()  # il bip o la conferma non devono finire nella richiesta
            richiesta = self.registra()
        turni = 0
        seguito = False   # il primo turno viene dalla parola di attivazione
        while richiesta is not None:
            turni += 1
            # solo numeri (durata, voce, volume), mai l'audio: servono a tarare le soglie
            # quando una richiesta arriva corta o debole (prova del 10/11: 1,1 s → Whisper
            # ha capito «grazie»)
            volumi = [rms(b) for b in richiesta]
            forti = [v for v in volumi if v >= self.voce_rms]
            voce_s = len(forti) * SEC_BLOCCO
            picco = max(volumi, default=0.0)
            medio = sum(forti) / len(forti) if forti else 0.0
            # il volume come multiplo della soglia della voce (GAS_ASCOLTO_VOCE_RMS): dice
            # di quanto alzarla o abbassarla, e nel log non finisce nessun valore dell'audio
            log.info("richiesta registrata (%.1f s, voce %.1f s, volume medio %.1f× e max "
                     "%.1f× la soglia), invio%s", len(richiesta) * SEC_BLOCCO, voce_s,
                     medio / self.voce_rms if self.voce_rms > 0 else 0.0,
                     picco / self.voce_rms if self.voce_rms > 0 else 0.0,
                     " (di seguito)" if seguito else "")
            riuscito = self.turno(richiesta, seguito=seguito)
            if self.interrotto:
                # Fetta 41: come una parola nuova — bip, poi la nuova richiesta. I turni
                # NON ripartono da zero (R-668-1): se la voce di Gas dalle casse facesse
                # scattare la parola, le interruzioni di fila restano sotto max_turni.
                # R-757-1-M1: almeno UNA interruzione apre la nuova domanda anche coi turni di
                # seguito spenti (max_turni=1, default di main): «Hey Jarvis» detto mentre
                # Gas parla è la parola vera (soglia 0,8), non il parlato della stanza.
                if turni >= max(self.max_turni, TURNI_CON_INTERRUZIONE):
                    break
                self._azzera()
                self._bip("ok")
                self._svuota()
                seguito = False   # dopo la parola il turno non è «di seguito»
                richiesta = self.registra()
                continue
            if self.chiudi or not riuscito or turni >= self.max_turni:
                break
            self.parola_nella_finestra = False
            # R-680-1: il rilevatore ha appena sentito la voce di Gas (soglia dell'interruzione):
            # si azzera, così nella finestra (soglia normale, più bassa) quei residui non
            # valgono come parola.
            self._azzera()
            inizio = self.aspetta_voce()
            if inizio is None:
                break
            richiesta = self.registra(
                inizio, rileva_parola=not self.parola_nella_finestra,
                max_s=REGISTRAZIONE_MAX_S if self.parola_nella_finestra else self.seguito_max_s)
            # V-1 bot #341: se nella finestra si è sentita la parola, il turno non è «di
            # seguito»: va al server senza X-Gas-Seguito, con gli strumenti e il tetto normale.
            seguito = not self.parola_nella_finestra
            if not seguito:
                log.info("parola di attivazione nella finestra: richiesta normale")
                # V-2 bot su a269c12: max_turni conta i turni «senza ripetere la parola»;
                # chi la ripete nella finestra riparte da zero (si incrementa al giro dopo).
                turni = 0
            if (seguito and richiesta is not None
                    and len(richiesta) >= blocchi_per(self.seguito_max_s)):
                # (a)+(b): parlato lungo senza parola = quasi sempre la stanza: non si invia
                log.info("parlato di %.0f s senza parola di attivazione: non lo invio, "
                         "chiudo la conversazione", self.seguito_max_s)
                break
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


class _Frasi:
    """Fetta 39: le frasi della risposta a pezzi, una alla volta (iteratore con `close`).
    Riserva della #336: `testo` è il testo intero della risposta («content» della prima
    riga), per sapere se Gas sta per dire la parola di attivazione."""

    def __init__(self, r) -> None:
        self.testo = ""
        self._gen = self._leggi(r)

    def __iter__(self) -> "_Frasi":
        return self

    def __next__(self) -> bytes:
        return next(self._gen)

    def close(self) -> None:
        self._gen.close()

    def _leggi(self, r) -> Iterator[bytes]:
        """Legge le righe JSON della risposta a pezzi (V7b) e dà l'MP3 di ogni frase appena
        la sua riga arriva. Si ferma su «fine», su «errore_voce» (il server ha smesso di
        sintetizzare) o a fine connessione. Una riga rotta o troppo lunga alza
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
                if not self.testo and isinstance(dati.get("content"), str):
                    self.testo = dati["content"]
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


def _frasi_ndjson(r) -> _Frasi:
    """Fetta 39: le frasi della risposta a pezzi (vedi `_Frasi`)."""
    return _Frasi(r)


def _comando(r: object) -> str:
    """Fetta 43 parte 2: X-Gas-Comando della risposta, solo se è un comando conosciuto."""
    try:
        valore = (r.headers.get("X-Gas-Comando") or "").strip().lower()  # type: ignore[attr-defined]
    except Exception:
        return ""
    return valore if valore in COMANDI else ""


def invia_al_server(url: str, token: str, timeout: float,
                    formato: Optional[str] = None, seguito: bool = False) -> Invia:
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
    if seguito:  # fetta 43 parte 2: turno nella finestra, senza parola di attivazione
        intestazioni["X-Gas-Seguito"] = "1"

    def _invia(wav: bytes) -> Esito:
        req = urllib.request.Request(f"{url}/voice", data=wav, method="POST",
                                     headers=intestazioni)
        try:
            r = _OPENER.open(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            comando = _comando(e)
            e.close()
            return False, None, f"HTTP {e.code}", comando
        except Exception as e:  # rete, timeout
            return False, None, f"server voce non raggiungibile ({type(e).__name__})", ""
        a_pezzi = False
        comando = _comando(r)
        try:
            tipo = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if r.status != 200:
                return (False, None, f"risposta inattesa (HTTP {r.status}, {tipo or '?'})",
                        comando)
            if comando == "fine":  # V15: niente voce né testo, la conversazione si chiude
                return True, None, "", comando
            if tipo == "application/x-ndjson" and formato:
                a_pezzi = True  # la connessione resta aperta: la chiude _frasi_ndjson
                return True, _frasi_ndjson(r), "", comando
            if tipo.startswith("audio/"):
                return True, r.read(), "", comando
            if tipo == "application/json" and formato:
                dati = json.loads(r.read())
                audio = _audio_da_base64(dati.get("audio")) if isinstance(dati, dict) else None
                if audio:
                    return True, audio, "", comando
                return False, None, "risposta inattesa (senza voce)", comando
            return False, None, f"risposta inattesa (HTTP {r.status}, {tipo or '?'})", comando
        except Exception as e:  # corpo rotto o connessione caduta
            return False, None, f"risposta inattesa ({type(e).__name__})", comando
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


def scarica_conferma(url: str, token: str,
                     timeout: float = CONFERMA_TIMEOUT_S) -> Optional[bytes]:
    """Fetta 42: GET /voce/conferma → MP3 di «Sì, signore?», o None su QUALSIASI errore
    (HTTP 502/503, connessione chiusa dal server, timeout, tipo sbagliato, vuoto o troppo
    grande). Nessun redirect (il Bearer resta sull'host), mai il token nei log."""
    req = urllib.request.Request(f"{url}{CONFERMA_PERCORSO}", method="GET", headers={
        "Authorization": f"Bearer {token}", "Accept": "audio/mpeg"})
    try:
        with _OPENER.open(req, timeout=timeout) as r:
            tipo = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if r.status != 200 or not tipo.startswith("audio/"):
                log.warning("conferma: risposta inattesa (HTTP %s, %s): bip", r.status,
                            tipo or "?")
                return None
            audio = r.read(CONFERMA_MAX_BYTE + 1)
    except urllib.error.HTTPError as e:
        e.close()
        log.warning("conferma: HTTP %s dal server voce: bip", e.code)
        return None
    except Exception as e:  # rete, timeout, connessione chiusa a metà
        log.warning("conferma non scaricata (%s): bip", type(e).__name__)
        return None
    if not audio or len(audio) > CONFERMA_MAX_BYTE:
        log.warning("conferma: audio vuoto o troppo grande: bip")
        return None
    return audio


class Conferma:
    """Fetta 42: tiene in memoria l'audio di «Sì, signore?». Lo scarica in sottofondo
    (all'avvio e, se manca, dopo una richiesta, al più una volta ogni CONFERMA_RIPROVA_S),
    così l'attivazione non aspetta mai la rete: finché non c'è, si usa il bip."""

    def __init__(self, scarica: Callable[[], Optional[bytes]],
                 adesso: Callable[[], float] = time.monotonic,
                 in_sottofondo: bool = True) -> None:
        self._scarica = scarica
        self._adesso = adesso
        self._in_sottofondo = in_sottofondo
        self._audio: Optional[bytes] = None
        self._lock = threading.Lock()
        self._in_corso = False
        self._ultimo: Optional[float] = None
        self._avvia()

    def _avvia(self) -> None:
        with self._lock:
            if self._audio is not None or self._in_corso:
                return
            if self._ultimo is not None and self._adesso() - self._ultimo < CONFERMA_RIPROVA_S:
                return
            self._in_corso = True
            self._ultimo = self._adesso()
        if self._in_sottofondo:
            try:
                threading.Thread(target=self._prendi, name="gas-conferma",
                                 daemon=True).start()
            except Exception as e:  # §9 (R-671-5): si riprova al giro dopo
                log.warning("conferma: thread non avviato (%s)", type(e).__name__)
                with self._lock:
                    self._in_corso = False
        else:
            self._prendi()

    def _prendi(self) -> None:
        try:
            audio = self._scarica()
        except Exception as e:  # §9
            log.warning("conferma non scaricata (%s)", type(e).__name__)
            audio = None
        with self._lock:
            if audio:
                self._audio = audio
            self._in_corso = False

    def __call__(self) -> Optional[bytes]:
        with self._lock:
            audio = self._audio
        if audio is None:
            self._avvia()
        return audio


def conferma_attiva() -> bool:
    """Fetta 42: GAS_ASCOLTO_CONFERMA=0 → dopo la parola solo il bip."""
    return os.environ.get("GAS_ASCOLTO_CONFERMA", "").strip() != "0"


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
    timeout = _numero("GAS_VOICE_TIMEOUT", 600, 5, 3600)
    invia = invia_al_server(url, token, timeout)
    invia_seguito = invia_al_server(url, token, timeout, seguito=True)
    conferma: Callable[[], Optional[bytes]] = lambda: None
    if conferma_attiva():
        try:
            conferma = Conferma(lambda: scarica_conferma(url, token))
        except Exception as e:  # §9 (R-671-5): senza conferma resta il bip
            log.warning("conferma non avviata (%s): solo bip", type(e).__name__)
    log.info("ascolto pronto: parola «%s», server %s", modello, url)
    while True:
        mic = None
        try:
            mic = Microfono()
            Ascolto(mic.blocchi(), punteggio, invia, riproduci_afplay, bip_di_sistema,
                    svuota=mic.svuota, azzera_rilevatore=azzera,
                    soglia=_numero("GAS_ASCOLTO_SOGLIA", SOGLIA_PREDEFINITA, 0.05, 0.99),
                    blocchi_parola=int(_numero("GAS_ASCOLTO_BLOCCHI_PAROLA",
                                               BLOCCHI_PAROLA_PREDEFINITO, 1, 5)),
                    coda_eco_s=CODA_ECO_S, subito_s=SUBITO_S,
                    voce_rms=_numero("GAS_ASCOLTO_VOCE_RMS", VOCE_RMS_PREDEFINITO, 10, 30000),
                    silenzio_s=_numero("GAS_ASCOLTO_SILENZIO", 0.8, 0.2, 5),
                    finestra_s=_finestra_dall_ambiente(),
                    seguito_max_s=_numero("GAS_VOICE_SEGUITO_MAX", SEGUITO_MAX_PREDEFINITO_S,
                                          3, REGISTRAZIONE_MAX_S),
                    invia_seguito=invia_seguito,
                    max_turni=int(_numero("GAS_VOICE_MAX_TURNI", MAX_TURNI_PREDEFINITO, 1, 50)),
                    soglia_interruzione=soglia_interruzione(),
                    conferma=conferma).gira()
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
