#!/usr/bin/env python3
"""
clients/voice/ascolto.py — voce H24 sul Mac (R8, chat Mani).

Gas sempre in ascolto: microfono aperto, parola di attivazione in LOCALE con
openWakeWord (per ora il modello pronto «hey_jarvis»: «Ehi Gas» va addestrato in una
fetta a parte), poi bip, registrazione fino al silenzio, invio al server voce già
esistente (modules/voice/server.py, POST /voice) e risposta riprodotta. Dopo la risposta
resta una finestra di ascolto (GAS_VOICE_FINESTRA, 12 s) per continuare senza ripetere
la parola, fino a GAS_VOICE_MAX_TURNI turni di fila.

Uso (dalla root ~/Gas, venv attivo, dipendenze di clients/voice/requirements-ascolto.txt):
    python clients/voice/ascolto.py
Di solito parte da solo con launchd: vedi scripts/voce/LEGGIMI.md.

Privacy:
  - Prima della parola di attivazione l'audio resta SOLO in memoria e lo legge solo
    openWakeWord, in locale: niente rete, niente disco.
  - La richiesta registrata resta in memoria e va solo al server voce. Non si salva
    nessuna registrazione.
  - La risposta di Gas (la sua voce, non la tua) passa da un file temporaneo 0600 per
    afplay, cancellato subito dopo.
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
    GAS_ASCOLTO_VOCE_RMS   — energia sopra cui c'è voce (default 500, campioni int16)
    GAS_ASCOLTO_SILENZIO   — secondi di silenzio che chiudono la richiesta (default 0.8)

Fail-safe §9: server giù o errore → bip di errore e si torna in ascolto; microfono che
cade → nuovo tentativo dopo qualche secondo; nessuna eccezione esce dal ciclo.
"""
from __future__ import annotations

import array
import io
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
from typing import Callable, Iterator, List, Optional, Sequence, Tuple

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
_BIP_OK = "/System/Library/Sounds/Tink.aiff"
_BIP_ERRORE = "/System/Library/Sounds/Basso.aiff"
_HOST_LOCALI = ("127.0.0.1", "localhost", "::1")

Blocco = Sequence[int]       # BLOCCO campioni int16
Invia = Callable[[bytes], Tuple[bool, Optional[bytes], str]]


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
                 invia: Invia, riproduci: Callable[[bytes], None],
                 bip: Callable[[str], None], *,
                 svuota: Callable[[], None] = lambda: None,
                 azzera_rilevatore: Callable[[], None] = lambda: None,
                 soglia: float = 0.5, voce_rms: float = 500.0, silenzio_s: float = 0.8,
                 finestra_s: float = 12.0, max_turni: int = 5) -> None:
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
                log.warning("rilevatore: errore (%s)", type(e).__name__)
                continue
            if punteggio >= self.soglia:
                return True

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
        """Invia la richiesta e riproduce la risposta. True se è andata bene."""
        try:
            ok, audio, motivo = self.invia(in_wav(blocchi))
        except Exception as e:  # §9
            ok, audio, motivo = False, None, f"errore ({type(e).__name__})"
        if not ok or not audio:
            log.warning("turno non riuscito: %s", motivo)
            self._bip("errore")
            self._svuota()  # V-3 bot #323: il bip e l'audio rimasto non vanno al rilevatore
            return False
        try:
            self.riproduci(audio)
        except Exception as e:  # §9
            log.warning("riproduzione fallita (%s)", type(e).__name__)
        finally:
            # Quello che il microfono ha sentito mentre Gas parlava è la sua voce:
            # non deve aprire un turno né attivare la parola.
            self._svuota()
        return True

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
            if not self.turno(richiesta) or turni >= self.max_turni:
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


def invia_al_server(url: str, token: str, timeout: float) -> Invia:
    """POST /voice col WAV; risposta in audio/mpeg. Mai il token nei log."""
    def _invia(wav: bytes) -> Tuple[bool, Optional[bytes], str]:
        req = urllib.request.Request(f"{url}/voice", data=wav, method="POST", headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "audio/wav",
            "Accept": "audio/mpeg",
        })
        try:
            with _OPENER.open(req, timeout=timeout) as r:
                tipo = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                corpo = r.read()
                if r.status != 200 or not tipo.startswith("audio/"):
                    return False, None, f"risposta inattesa (HTTP {r.status}, {tipo or '?'})"
                return True, corpo, ""
        except urllib.error.HTTPError as e:
            e.close()
            return False, None, f"HTTP {e.code}"
        except Exception as e:  # rete, timeout
            return False, None, f"server voce non raggiungibile ({type(e).__name__})"
    return _invia


def riproduci_afplay(audio: bytes) -> None:
    """Riproduce la risposta di Gas con afplay da un file temporaneo 0600, cancellato
    subito dopo (anche se afplay fallisce)."""
    cartella = tempfile.mkdtemp(prefix="gas-voce-")
    percorso = os.path.join(cartella, "risposta.mp3")
    try:
        fd = os.open(percorso, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(audio)
        subprocess.run(["afplay", percorso], check=False, timeout=600,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        shutil.rmtree(cartella, ignore_errors=True)


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
                    voce_rms=_numero("GAS_ASCOLTO_VOCE_RMS", 500, 10, 30000),
                    silenzio_s=_numero("GAS_ASCOLTO_SILENZIO", 0.8, 0.2, 5),
                    finestra_s=_numero("GAS_VOICE_FINESTRA", 12, 0, 120),
                    max_turni=int(_numero("GAS_VOICE_MAX_TURNI", 5, 1, 50))).gira()
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
