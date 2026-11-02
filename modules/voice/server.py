"""
HTTP voice endpoint per GAS — FASE 3, Fette 1+2+3.

Endpoint: POST /voice
  Body (testo):  JSON {"prompt": "<testo>"}
  Body (audio):  Content-Type audio/* oppure multipart/form-data con campo 'file'
  Auth:    Header "Authorization: Bearer <token>"

  Output testo (default):
    200:   JSON {"content": "<risposta>"}

  Output audio (se Accept: audio/mpeg o Accept: audio/*):
    200:   byte MP3 grezzi (Content-Type: audio/mpeg)
    502:   JSON {"error": "<msg>"}  — errore ElevenLabs (rete/quota)
    503:   JSON {"error": "<msg>"}  — TTS non disponibile (ELEVENLABS_API_KEY assente)

  Codici errore comuni:
    400:   JSON {"error": "<msg>"}  — prompt mancante/JSON invalido / audio vuoto o invalido
    401:   JSON {"error": "Unauthorized"}
    502:   JSON {"error": "<msg>"}  — errore Groq STT o ElevenLabs TTS (rete/quota)
    503:   JSON {"error": "<msg>"}  — STT/TTS non disponibile (chiave assente)
    500:   JSON {"error": "<msg>"}  — errore pipeline o kernel

Avvio: `python -m modules.voice.server` dalla cartella di Gas (carica il `.env` come la CLI).

Configurazione tramite variabili d'ambiente (da .env o export):
  GAS_VOICE_BIND      — bind address       (default: 127.0.0.1)
  GAS_VOICE_PORT      — porta TCP          (default: 8765)
  GAS_VOICE_TOKEN     — token bearer       OBBLIGATORIO: assente/vuoto → il server non parte
  GROQ_API_KEY        — chiave Groq        OBBLIGATORIO per STT audio; assente → 503
  ELEVENLABS_API_KEY  — chiave ElevenLabs  OBBLIGATORIO per output audio; assente → 503
  ELEVENLABS_VOICE_ID — voice id           (default: JBFqnCBsd6RMkjVDRZzb, George premade)
  GAS_VOICE_MAX_TURNI_ORA — richieste PARLATE al massimo nell'ultima ora (default 60), poi
                        429; conta ogni chiamata alla trascrizione (Groq)
  GAS_VOCE_FORTE      — 1/true/on/yes/si/sì: ogni richiesta della voce va al solo cervello
                        forte (default spento; forte fermo → errore dichiarato, mai i gratuiti)
  GAS_VOICE_STT_LOGPROB_MIN / GAS_VOICE_STT_NO_SPEECH_MAX — soglie della trascrizione
                        incerta (default -1.0 / 0.8): sotto/sopra → «Non ho capito bene, puoi
                        ripetere?» senza turno (V6). Risposte 200 della voce con il campo
                        "capito" = testo trascritto, mostrato dalla pagina.
  GAS_VOICE_STT_ECO_NO_SPEECH — soglia (default 0.9) oltre la quale un'eco corta del
                        prompt di Whisper (2-3 parole contigue, es. «Gas, forte, lead.») è
                        scartata come silenzio; i comandi brevi detti davvero stanno sotto.

Cervello forte dalla voce (V1, chat M2): «/forte <richiesta>» (testo) oppure, nel parlato
trascritto, «forte <richiesta>» / «Gas forte <richiesta>» all'inizio della frase.
«forte» parlato senza richiesta → 200 con l'istruzione d'uso da ascoltare (nessun turno);
«/forte» scritto senza richiesta → 400.

Sicurezza:
  - Nasce chiuso su 127.0.0.1. Aprire all'esterno SOLO settando GAS_VOICE_BIND.
  - Confronto token a TEMPO COSTANTE via hmac.compare_digest (mai ==).
  - Nessun segreto scritto nei log; ogni tentativo fallito viene loggato con IP + esito.
  - I byte audio (ingresso e uscita) non vengono loggati né scritti su disco; le chiavi non compaiono nei log.
  - CAVEAT PRIVACY (STT): l'audio dell'utente viene inviato ai server Groq (terza parte).
  - CAVEAT PRIVACY (TTS): il testo del kernel viene inviato ai server ElevenLabs (terza parte).
    Trade-off dichiarato: per un agente che tocca dati/lead, questo è egress di dati.
  - Kernel GasKernel istanziato UNA VOLTA all'avvio (stateful, storia condivisa).
  - Single-thread nativo: http.server.HTTPServer senza ThreadingMixIn, nessun lock.
  - Fail-safe §9: eccezione in run_turn → 500 + log in gas_debug.log, server vivo.
"""
from __future__ import annotations

import base64
import hmac
import json
import logging
import os
import re
import subprocess
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional

from modules.voice.stt import GroqSTTError, TrascrizioneIncerta, parse_audio_body, transcribe_audio
from modules.voice.tts import DEFAULT_VOICE_ID as _TTS_DEFAULT_VOICE_ID
from modules.voice.tts import (ElevenLabsTTSError, add_shared_voice, list_shared_voices,
                               list_voices, synthesize_speech)
from modules.voice import prova_voci

log = logging.getLogger(__name__)
# V7 (R-614-3-M2): i tempi sono informazione, non un problema: logger dedicato a INFO, che
# finisce nel file gas_debug.log (il terminale resta a WARNING; i tempi sono già nella pagina).
_log_tempi = logging.getLogger("gas.voce.tempi")
_log_tempi.setLevel(logging.INFO)

_ENDPOINT = "/voice"

# V1 (chat M2): la barra di «/forte» non si detta e Whisper scrive «Forte, …»: la parola
# «forte» all'inizio del parlato (anche dopo «Gas», o «Gus» come lo trascrive Whisper)
# vale «/forte», anche dopo un saluto prima di «Gas» («Ehi Gas, forte …», V-2 ve #304).
# Parola intera: «fortemente…» o «forte» a metà frase restano testo normale. Limiti
# dichiarati: «Forte!» esclamazione, «forte-forte», «forte: …» vanno al forte (direzione
# sicura, costa budget: R-564-1-M2, V-1 ve #304); «Gas e forte …» o un saluto non in
# elenco restano normali (con GAS_VOCE_FORTE=1 vanno comunque al forte).
_PAROLA_FORTE = re.compile(
    r"^[^\w/]*(?:(?:(?:ehi|ehy|hey|ok|okay|ciao|senti)\W+)?(?:gas|gus)\b\W*)?forte(?!\w)(.*)$",
    re.IGNORECASE | re.DOTALL)
_USO_FORTE = "Uso: /forte <richiesta> (a voce: «forte <richiesta>»)"
# V2 (V-2 ve #304): a chi PARLA l'istruzione d'uso arriva come risposta da ascoltare
# (200, sintetizzata se il client vuole audio), non come errore 400. Nessun turno parte.
_USO_FORTE_PARLATO = ("Dopo «forte» dimmi cosa fare, per esempio: «Gas, forte: riassumi i lead "
                      "di oggi». Non ho avviato nessun lavoro.")
# V6: trascrizione incerta (stt.TrascrizioneIncerta) → si chiede di ripetere, nessun turno
_NON_HO_CAPITO = "Non ho capito bene, puoi ripetere?"


# V3 (chat M2): con «X-Gas-Formato: audio+testo» (pagina del browser) la risposta è JSON
# con il testo intero (a schermo) e l'audio della sola parte parlata, corta: le prime
# frasi, entro _PARLATO_MAX_CHAR. Il resto si legge.
_FORMATO_AUDIO_TESTO = "audio+testo"
# V7b (chat M2): come «audio+testo», ma la risposta arriva a righe JSON (NDJSON) mentre la
# voce viene sintetizzata frase per frase: la pagina comincia a parlare dopo la prima frase.
_FORMATO_PEZZI = "audio+testo+pezzi"
_PARLATO_MAX_FRASI = 3
_PARLATO_MAX_CHAR = 400
_PARLATO_RESTO = " Il resto è a schermo."
_FINE_FRASE = re.compile(r"(?<=[.!?…])\s+")
_ABBREVIAZIONE = re.compile(r"(?:^|\s)(?:dott|dr|sig|sigg|sig\.ra|ing|avv|prof|arch|geom|"
                            r"rag|ecc|es|pag|n|nr|tel|art|cap|vs)\.$", re.IGNORECASE)


# V6 (chat M2, «capire meglio»): le frasi brevi non devono perdere il filo, e la richiesta
# è una trascrizione che può storpiare qualche parola.
_CONTESTO_VOCE = (
    "Brevità non vuol dire perdere il filo: rispondi a quello che l'operatore intende, "
    "tenendo conto di quello che vi siete detti prima in questa conversazione. La sua "
    "frase arriva da una trascrizione vocale e può avere parole storpiate (per esempio "
    "«Gus» per «Gas»): se una parola non torna, interpretala dal contesto; se la "
    "richiesta resta ambigua, fai una sola domanda per chiarire invece di indovinare.")
# V3: istruzione per i soli turni PARLATI (gas.py `run_turn(istruzione_turno=...)`: vale per
# quel turno, nel messaggio system, fuori dalla cronologia). Il testo scritto resta com'è.
ISTRUZIONE_VOCE = (
    "Stai parlando a voce con l'operatore, in una conversazione rapida. Rispondi in 1-3 "
    "frasi brevi, senza elenchi né formattazione. Dai subito un parere o una proposta "
    "concreta (anche «no, meglio così»). Se serve una decisione chiudi con una domanda "
    "secca a cui si risponde sì o no. Se il risultato è lungo, riassumilo in una frase."
    + " " + _CONTESTO_VOCE)
# V4 (V-1 bot #311): con la pagina del browser c'è uno schermo: prima le frasi da dire,
# poi, dopo una riga vuota, il dettaglio da leggere (non viene detto a voce).
ISTRUZIONE_VOCE_SCHERMO = (
    "Stai parlando a voce con l'operatore, in una conversazione rapida, e lui ha anche uno "
    "schermo. Apri con 1-3 frasi brevi da dire a voce, senza elenchi né formattazione: "
    "dai subito un parere o una proposta concreta (anche «no, meglio così») e, se serve "
    "una decisione, chiudi con una domanda secca a cui si risponde sì o no. Se servono "
    "dettagli (dati, elenchi, analisi, testo lungo), scrivili DOPO una riga vuota: quella "
    "parte non viene letta a voce, l'operatore la legge a schermo."
    + " " + _CONTESTO_VOCE)
_PARAGRAFO = re.compile(r"\n[ \t]*\n")


def _dividi_frasi(testo: str) -> List[str]:
    """Frasi di un testo già su una riga; «Dott. Rossi» non è una fine frase (R-574-4-M2)."""
    frasi: List[str] = []
    for pezzo in (f for f in _FINE_FRASE.split(testo) if f):
        if frasi and _ABBREVIAZIONE.search(frasi[-1]):
            frasi[-1] = f"{frasi[-1]} {pezzo}"
        else:
            frasi.append(pezzo)
    return frasi


def frasi_parlate(testo: str) -> List[str]:
    """V7b: la parte parlata (vedi parte_parlata) divisa in frasi, da sintetizzare una alla
    volta. Unite di nuovo con uno spazio danno esattamente parte_parlata(testo)."""
    return _dividi_frasi(parte_parlata(testo))


def parte_parlata(testo: str) -> str:
    """Le prime frasi di `testo` da dire a voce (≤ _PARLATO_MAX_FRASI frasi e
    ≤ _PARLATO_MAX_CHAR caratteri); se il testo è più lungo aggiunge «Il resto è a
    schermo.». Testo corto → identico. V4: si dice solo il primo paragrafo (il dettaglio
    dopo la riga vuota, chiesto da ISTRUZIONE_VOCE_SCHERMO, si legge a schermo)."""
    pezzi = _PARAGRAFO.split(testo.strip(), maxsplit=1)
    if len(pezzi) == 2 and pezzi[1].strip():
        primo = parte_parlata(pezzi[0])
        return primo if primo.endswith(_PARLATO_RESTO) else primo + _PARLATO_RESTO
    testo = " ".join(testo.split())  # R-574-4-M2: a capo e spazi doppi non contano
    frasi = _dividi_frasi(testo)
    parlato = ""
    for f in frasi[:_PARLATO_MAX_FRASI]:
        prova = f"{parlato} {f}".strip()
        if len(prova) > _PARLATO_MAX_CHAR:
            break
        parlato = prova
    if not parlato:  # prima frase già troppo lunga: taglio all'ultimo spazio
        parlato = testo[:_PARLATO_MAX_CHAR].rsplit(" ", 1)[0] if len(testo) > _PARLATO_MAX_CHAR else testo
    return parlato if parlato == testo else parlato + _PARLATO_RESTO


# V4 (V-2 ve #311): tetto LATO SERVER alle richieste a voce, oltre a quello della pagina: un
# client diverso o rotto non fa partire turni senza fine. GAS_VOICE_MAX_TURNI_ORA (default
# 60) richieste a voce (chiamate a Groq, V5) nell'ultima ora, poi 429 finché la finestra non scorre.
_MAX_TURNI_ORA_DEFAULT = 60


def _max_turni_ora() -> int:
    try:
        n = int(os.environ.get("GAS_VOICE_MAX_TURNI_ORA") or _MAX_TURNI_ORA_DEFAULT)
    except ValueError:
        log.warning("GAS_VOICE_MAX_TURNI_ORA non numerica: uso %d", _MAX_TURNI_ORA_DEFAULT)
        return _MAX_TURNI_ORA_DEFAULT
    return n if n > 0 else _MAX_TURNI_ORA_DEFAULT


def _voce_tutta_forte() -> bool:
    """GAS_VOCE_FORTE acceso: regole di _env_flag in gas.py (1/true/on/yes/si) più «sì»
    con l'accento (nota #565-M2: scritto in italiano, non deve restare spento in silenzio)."""
    return os.environ.get("GAS_VOCE_FORTE", "").strip().lower() in ("1", "true", "on", "yes", "si", "sì")


def cervello_voce(prompt: str, parlato: bool) -> tuple[Optional[str], str]:
    """(cervello, richiesta) per una richiesta della voce: «forte» solo cervello forte,
    «uso» prefisso senza richiesta (fail-closed: mai ai gratuiti), None turno normale.
    «/forte» vale sempre; la parola parlata solo se `parlato` (testo trascritto)."""
    from brains.router import prefisso_forte
    if not prompt.strip():
        return "uso", ""  # V-3 ve #304: fail-closed anche fuori dal gestore
    cervello, prompt = prefisso_forte(prompt)
    if cervello is None and parlato:
        m = _PAROLA_FORTE.match(prompt)
        if m:
            richiesta = re.sub(r"^\W+", "", m.group(1)).strip()
            if not richiesta:
                return "uso", ""
            cervello, prompt = "forte", richiesta
    if cervello is None and _voce_tutta_forte():
        cervello = "forte"
    return cervello, prompt


def _token_ok(received: str, expected: str) -> bool:
    """Confronto a tempo costante. False se uno dei due è vuoto."""
    if not received or not expected:
        return False
    return hmac.compare_digest(received.encode("utf-8"), expected.encode("utf-8"))


class VoiceHandler(BaseHTTPRequestHandler):
    """Handler HTTP per POST /voice. Kernel e token iniettati dal runner prima del bind."""

    kernel: Any = None
    token: str = ""
    _capito: Optional[str] = None  # V6: trascrizione della richiesta in corso (per istanza)
    _tempi: Optional[Dict[str, float]] = None  # V7: secondi per pezzo della richiesta in corso
    _t0: float = 0.0
    turni_parlati: List[float] = []  # V4/V5: istanti delle chiamate a Groq (tetto orario)
    prove_voci: List[float] = []  # V8: istanti delle prove di voce ElevenLabs (tetto orario)
    # V8 (R-624-1-M2): id delle voci mostrate dall'ultimo elenco (già filtrate: niente
    # cloni); la prova accetta solo queste, non un id qualunque scritto a mano
    voci_ammesse: frozenset = frozenset()
    # V8b: voci della libreria mostrate dall'ultima ricerca {id: (proprietario, nome)};
    # si aggiungono all'account solo queste
    libreria_ammesse: Dict[str, Any] = {}
    aggiunte_voci: List[float] = []  # V8b: istanti delle aggiunte all'account (tetto orario)

    def log_message(self, fmt: str, *args: Any) -> None:
        log.info(fmt, *args)

    def _segna(self, pezzo: str, inizio: float) -> None:
        """V7: secondi spesi in un pezzo della richiesta (trascrizione, cervello, voce)."""
        if self._tempi is not None:
            self._tempi[pezzo] = round(time.monotonic() - inizio, 2)

    def _chiudi_tempi(self, code: int) -> Optional[Dict[str, float]]:
        """V7: tempi della richiesta + totale nel server; una riga INFO nel solo
        gas_debug.log (logger gas.voce.tempi) per ogni richiesta che ha speso qualcosa.
        Solo numeri."""
        if self._tempi is None or not self._tempi:
            return None
        tempi = dict(self._tempi, server=round(time.monotonic() - self._t0, 2))
        self._tempi = None  # una sola volta per richiesta
        _log_tempi.info("tempi voce (%s): %s", code,
                        " ".join(f"{k}={v:.2f}s" for k, v in tempi.items()))
        return tempi

    def _send_json(self, code: int, payload: Dict[str, Any]) -> None:
        tempi = self._chiudi_tempi(code)
        if tempi is not None:
            payload = dict(payload, tempi=tempi)
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_audio(self, data: bytes, tipo: str = "audio/mpeg") -> None:
        tempi = self._chiudi_tempi(200)
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        if tempi is not None:  # V7: con l'MP3 grezzo i tempi viaggiano in un'intestazione
            self.send_header("X-Gas-Tempi", ";".join(f"{k}={v}" for k, v in tempi.items()))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _wants_audio(self) -> bool:
        """True se il client dichiara Accept: audio/mpeg o audio/* (non audio generico */*).
        Retrocompatibile: senza header (o Accept: application/json) → False → risposta JSON."""
        accept = self.headers.get("Accept", "")
        return "audio/mpeg" in accept or "audio/*" in accept

    def _check_auth(self) -> bool:
        """Verifica il token bearer. Logga ogni fallimento con IP; MAI il token ricevuto."""
        hdr = self.headers.get("Authorization", "")
        parts = hdr.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            log.warning("AUTH FAIL ip=%s motivo=header_mancante_o_malformato", self.client_address[0])
            return False
        if not _token_ok(parts[1].strip(), self.token):
            log.warning("AUTH FAIL ip=%s motivo=token_non_valido", self.client_address[0])
            return False
        return True

    def do_POST(self) -> None:
        self._t0 = time.monotonic()
        self._tempi = {}
        self._capito = None  # V-3 bot #318: mai il «capito» di un'altra richiesta (keep-alive)
        if self.path in ("/voci/prova", "/voci/aggiungi"):  # V8/V8b: prova o aggiunta di una voce
            if not self._check_auth():
                self._send_json(401, {"error": "Unauthorized"})
                return
            try:
                n = int(self.headers.get("Content-Length", 0) or 0)
            except ValueError:
                n = -1
            if not 0 <= n <= 4096:
                self._send_json(400, {"error": "Content-Length non valido"})
                return
            self._tempi = None
            corpo = self.rfile.read(n) if n else b""
            (self._prova_voce if self.path == "/voci/prova" else self._aggiungi_voce)(corpo)
            return
        if self.path != _ENDPOINT:
            self._send_json(404, {"error": "Not Found"})
            return

        if not self._check_auth():
            self._send_json(401, {"error": "Unauthorized"})
            return

        try:
            length = int(self.headers.get("Content-Length", 0) or 0)
        except ValueError:
            self._send_json(400, {"error": "Content-Length non valido"})
            return
        raw = self.rfile.read(length) if length > 0 else b""
        # V-2 bot #322: il caricamento dell'audio dalla pagina è «rete», non tempo del server
        self._t0 = time.monotonic()

        content_type = self.headers.get("Content-Type", "")
        ct_base = content_type.split(";")[0].strip().lower()
        is_audio = ct_base.startswith("audio/") or ct_base == "multipart/form-data"

        if is_audio:
            # V4 (V-2 ve #311, R-580-2-M2): tetto orario delle richieste a voce controllato PRIMA
            # della trascrizione, così oltre il tetto non si spende nemmeno Groq
            tetto = _max_turni_ora()
            if len(self._turni_recenti()) >= tetto:
                self._send_json(429, {"error": (
                    f"Troppe richieste a voce nell'ultima ora ({tetto}, GAS_VOICE_MAX_TURNI_ORA): "
                    "nessun lavoro avviato. Riprova più tardi o scrivi.")})
                return
            prompt = self._do_stt(raw, content_type)
            if prompt is None:
                return  # risposta (errore o «non ho capito») già inviata
            self._capito = prompt  # V6: la pagina mostra «Ho capito: …»
        else:
            try:
                data: Dict[str, Any] = json.loads(raw) if raw else {}
            except (json.JSONDecodeError, ValueError):
                self._send_json(400, {"error": "Body JSON non valido"})
                return

            prompt = (data.get("prompt") or "").strip()
            if not prompt:
                self._send_json(400, {"error": "Campo 'prompt' mancante o vuoto"})
                return

        # R-ve269-2 + V1: «/forte», «forte …» parlato o GAS_VOCE_FORTE → solo forte, mai ai gratuiti
        cervello, prompt = cervello_voce(prompt, parlato=is_audio)
        if cervello == "uso":
            if not is_audio:
                self._send_json(400, {"error": _USO_FORTE})
            else:
                self._rispondi_senza_turno(_USO_FORTE_PARLATO, "uso")
            return

        t_cervello: Optional[float] = None
        try:
            result_content: Optional[str] = None
            kw: Dict[str, Any] = {}
            if cervello == "forte":
                kw["cervello"] = "forte"
            if is_audio:  # V3/V4: risposte a voce corte, col dettaglio a schermo se c'è
                kw["istruzione_turno"] = (ISTRUZIONE_VOCE_SCHERMO if self._vuole_audio_testo()
                                          else ISTRUZIONE_VOCE)
            t_cervello = time.monotonic()
            turno = self.kernel.run_turn(prompt, **kw)
            for event in turno:
                etype = event.get("type")
                if etype == "final":
                    result_content = event.get("content", "")
                    self._segna("cervello", t_cervello)
                    break
                elif etype == "error":
                    self._segna("cervello", t_cervello)
                    self._send_json(500, {"error": event.get("content", "Errore pipeline")})
                    return
                # type="tool_res": consumato in silenzio
        except Exception as exc:
            if t_cervello is not None:  # R-614-1-M2: anche un cervello che si rompe ha un tempo
                self._segna("cervello", t_cervello)
            log.warning("run_turn eccezione: %s", exc)
            self._send_json(500, {"error": "Errore interno del kernel"})
            return

        if result_content is None:
            if t_cervello is not None:  # V-2 ve #322: turno finito senza final né error (V-3 bot: tipo)
                self._segna("cervello", t_cervello)
            self._send_json(500, {"error": "Nessuna risposta dal kernel"})
            return

        if self._vuole_audio_testo():
            self._do_audio_testo_response(result_content)
        elif self._wants_audio():
            self._do_tts_response(result_content)
        else:
            out: Dict[str, Any] = {"content": result_content}
            if self._capito is not None:
                out["capito"] = self._capito
            self._send_json(200, out)

    def _rispondi_senza_turno(self, testo: str, segno: str) -> None:
        """Risposta parlata fissa senza lavoro del kernel («uso», «non ho capito»), nel
        formato chiesto dal client; `segno` è il campo JSON che la distingue."""
        if self._vuole_audio_testo():
            self._do_audio_testo_response(testo, {segno: True})
        elif self._wants_audio() and os.environ.get("ELEVENLABS_API_KEY", "").strip():
            self._do_tts_response(testo)
        else:  # V-2 bot #318: senza TTS il messaggio arriva lo stesso, come testo (mai un 503)
            out: Dict[str, Any] = {"content": testo, segno: True}
            if self._capito is not None:
                out["capito"] = self._capito
            self._send_json(200, out)

    def _turni_recenti(self) -> List[float]:
        """Istanti delle richieste a voce (chiamate a Groq) dell'ultima ora (tetto GAS_VOICE_MAX_TURNI_ORA)."""
        adesso = time.monotonic()
        return [t for t in self.turni_parlati if adesso - t < 3600]

    def _formato(self) -> str:
        return self.headers.get("X-Gas-Formato", "").strip().lower()

    def _vuole_audio_testo(self) -> bool:
        return self._formato() in (_FORMATO_AUDIO_TESTO, _FORMATO_PEZZI)

    def _do_audio_testo_response(self, text: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """V3: JSON {"content": testo intero, "audio": base64 MP3 della parte parlata}.
        Senza chiave ElevenLabs o con errore TTS la risposta arriva lo stesso, solo testo
        (+ "errore_voce"): a schermo si legge, mai un 503 al posto della risposta."""
        out: Dict[str, Any] = {"content": text, **(extra or {})}
        if self._capito is not None:  # V6: quello che Whisper ha sentito, per la pagina
            out["capito"] = self._capito
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not text.strip():
            pass
        elif not api_key:
            out["errore_voce"] = "TTS non disponibile: ELEVENLABS_API_KEY non configurata"
        else:
            voice_id = (os.environ.get("ELEVENLABS_VOICE_ID") or _TTS_DEFAULT_VOICE_ID).strip() or _TTS_DEFAULT_VOICE_ID
            if self._formato() == _FORMATO_PEZZI:
                self._do_pezzi_response(out, frasi_parlate(text), api_key, voice_id)
                return
            t = time.monotonic()
            try:
                out["audio"] = base64.b64encode(
                    synthesize_speech(parte_parlata(text), api_key, voice_id)).decode("ascii")
            except ElevenLabsTTSError as exc:
                log.warning("ElevenLabs TTS error status=%s: %s", exc.status, exc.message)
                out["errore_voce"] = f"Errore TTS ElevenLabs: {exc.message}"
            except OSError as exc:
                log.warning("ElevenLabs TTS network error: %s", exc)
                out["errore_voce"] = "Errore di rete verso ElevenLabs TTS"
            finally:  # R-614-1-M2: anche un TTS fallito o in timeout ha il suo tempo
                self._segna("voce", t)
        self._send_json(200, out)

    def _do_pezzi_response(self, primo: Dict[str, Any], frasi: List[str], api_key: str,
                           voice_id: str) -> None:
        """V7b: risposta a righe JSON (NDJSON), una sintesi per frase.
        Riga 1: `primo` (content, capito, …) + "audio" della prima frase + "pezzi" (frasi
        totali). Poi una riga {"audio": …} per ogni frase successiva, appena pronta. Ultima
        riga {"fine": true, "tempi": …}. Un errore TTS a metà → riga {"errore_voce": …} e
        stop (il testo è già a schermo). Il client che chiude la connessione ferma la
        sintesi (niente spesa per frasi che nessuno ascolta)."""
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
        self.end_headers()  # HTTP/1.0: niente Content-Length, la fine è la chiusura

        def riga(obj: Dict[str, Any]) -> bool:
            try:
                self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8") + b"\n")
                self.wfile.flush()
                return True
            except OSError as exc:  # pagina chiusa o interrotta: si smette di sintetizzare
                log.warning("voce a pezzi: client chiuso (%s)", type(exc).__name__)
                return False

        t_tutta = time.monotonic()
        aperto = True
        for i, frase in enumerate(frasi):
            uscita: Dict[str, Any] = dict(primo, pezzi=len(frasi)) if i == 0 else {}
            t = time.monotonic()
            errore: Optional[str] = None
            try:
                uscita["audio"] = base64.b64encode(
                    synthesize_speech(frase, api_key, voice_id)).decode("ascii")
            except ElevenLabsTTSError as exc:
                log.warning("ElevenLabs TTS error status=%s: %s", exc.status, exc.message)
                errore = f"Errore TTS ElevenLabs: {exc.message}"
            except OSError as exc:
                log.warning("ElevenLabs TTS network error: %s", exc)
                errore = "Errore di rete verso ElevenLabs TTS"
            if i == 0:
                self._segna("voce", t)  # tempo fino alla prima frase: quello che si sente
            if errore is not None:
                uscita["errore_voce"] = errore
            aperto = riga(uscita)
            if errore is not None or not aperto:
                break
        self._segna("voce_tutta", t_tutta)
        tempi = self._chiudi_tempi(200)
        if aperto:
            riga({"fine": True, **({"tempi": tempi} if tempi else {})})

    def _do_tts_response(self, text: str) -> None:
        """Sintetizza text via ElevenLabs e invia i byte MP3. Invia l'errore HTTP se fallisce.
        Se text è vuoto salta la chiamata ElevenLabs e risponde JSON vuoto (mai crash)."""
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "TTS non disponibile: ELEVENLABS_API_KEY non configurata"})
            return

        if not text:
            self._send_json(200, {"content": ""})
            return

        voice_id = (os.environ.get("ELEVENLABS_VOICE_ID") or _TTS_DEFAULT_VOICE_ID).strip() or _TTS_DEFAULT_VOICE_ID

        t = time.monotonic()
        try:
            audio = synthesize_speech(text, api_key, voice_id)
            self._segna("voce", t)
        except ElevenLabsTTSError as exc:
            self._segna("voce", t)  # R-614-1-M2
            log.warning("ElevenLabs TTS error status=%s: %s", exc.status, exc.message)
            self._send_json(502, {"error": f"Errore TTS ElevenLabs: {exc.message}"})
            return
        except OSError as exc:
            self._segna("voce", t)  # R-614-1-M2
            log.warning("ElevenLabs TTS network error: %s", exc)
            self._send_json(502, {"error": "Errore di rete verso ElevenLabs TTS"})
            return

        self._send_audio(audio)

    def _do_stt(self, raw: bytes, content_type: str) -> Optional[str]:
        """Trascrive audio → testo via Groq Whisper.
        Invia la risposta HTTP di errore e ritorna None se qualcosa va storto."""
        api_key = os.environ.get("GROQ_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "STT non disponibile: GROQ_API_KEY non configurata"})
            return None

        if not raw:
            self._send_json(400, {"error": "Audio vuoto"})
            return None

        try:
            audio_bytes, filename = parse_audio_body(raw, content_type)
        except ValueError as exc:
            self._send_json(400, {"error": f"Audio non valido: {exc}"})
            return None

        # V5 (R-581-2-M2, R-585-1-M2): conta per GAS_VOICE_MAX_TURNI_ORA ogni chiamata a Groq,
        # subito prima di farla: anche «forte» senza richiesta e le trascrizioni vuote o
        # fallite spendono, quindi contano; i rifiuti locali (chiave assente, audio vuoto o
        # non valido) no, così l'errore utile (503/400) resta visibile.
        type(self).turni_parlati = self._turni_recenti() + [time.monotonic()]
        t = time.monotonic()
        try:
            text = transcribe_audio(audio_bytes, filename, api_key)
        except TrascrizioneIncerta as exc:
            self._segna("trascrizione", t)
            # V6: Groq ha risposto ma il testo è probabilmente sbagliato: si chiede di
            # ripetere invece di rispondere a caso. Nel log solo il motivo, mai il parlato.
            log.info("trascrizione scartata: %s", exc.motivo)
            self._capito = exc.testo
            self._rispondi_senza_turno(_NON_HO_CAPITO, "non_capito")
            return None
        except GroqSTTError as exc:
            self._segna("trascrizione", t)
            if exc.status == 400:
                self._send_json(400, {"error": f"Formato audio non accettato da Groq: {exc.message}"})
            else:
                self._send_json(502, {"error": f"Errore Groq STT: {exc.message}"})
            return None
        except OSError as exc:
            self._segna("trascrizione", t)
            log.warning("Groq STT network error: %s", exc)
            self._send_json(502, {"error": "Errore di rete verso Groq STT"})
            return None

        self._segna("trascrizione", t)
        if not text:
            self._send_json(400, {"error": "Trascrizione vuota (silenzio o formato non supportato)"})
            return None

        return text

    def _method_not_allowed(self) -> None:
        self._send_json(405, {"error": "Method Not Allowed"})

    # ── V8 (chat M2): «prova voci» — elenco delle voci e prova con una frase fissa ──

    def do_GET(self) -> None:
        self._t0 = time.monotonic()
        self._tempi = None
        if self.path not in ("/voci/elenco", "/voci/libreria"):
            self._method_not_allowed()
            return
        if not self._check_auth():
            self._send_json(401, {"error": "Unauthorized"})
            return
        if self.path == "/voci/libreria":
            self._libreria()
            return
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        attuale = (os.environ.get("ELEVENLABS_VOICE_ID") or _TTS_DEFAULT_VOICE_ID).strip() or _TTS_DEFAULT_VOICE_ID
        out: Dict[str, Any] = {"voci": [], "attuale": attuale, "frasi": list(prova_voci.FRASI_PROVA),
                               "piper": prova_voci.piper_disponibile() is not None}
        type(self).voci_ammesse = frozenset()  # R-625-2-M2: valgono solo le voci di questo elenco
        if not api_key:
            out["errore"] = "ELEVENLABS_API_KEY non configurata: niente voci ElevenLabs"
        else:
            try:
                out["voci"] = prova_voci.ordina_voci(list_voices(api_key), attuale)
                type(self).voci_ammesse = frozenset(v["id"] for v in out["voci"])
            except ElevenLabsTTSError as exc:
                log.warning("ElevenLabs elenco voci status=%s: %s", exc.status, exc.message)
                out["errore"] = f"Elenco voci ElevenLabs non disponibile: {exc.message}"
            except OSError as exc:
                log.warning("ElevenLabs elenco voci rete: %s", exc)
                out["errore"] = "Errore di rete verso ElevenLabs"
        self._send_json(200, out)

    def _libreria(self) -> None:
        """V8b: GET /voci/libreria — le migliori voci della libreria condivisa (da aggiungere
        all'account per provarle in italiano), con l'anteprima pubblica e l'avviso su costi e
        limiti. Un errore (piano senza libreria, API diversa) torna nel JSON, mai un crash."""
        type(self).libreria_ammesse = {}
        out: Dict[str, Any] = {"voci": [], "avviso": prova_voci.AVVISO_LIBRERIA}
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            out["errore"] = "ELEVENLABS_API_KEY non configurata"
            self._send_json(200, out)
            return
        try:
            voci = prova_voci.ordina_libreria(list_shared_voices(api_key, prova_voci.FILTRI_LIBRERIA))
        except ElevenLabsTTSError as exc:
            log.warning("ElevenLabs libreria status=%s: %s", exc.status, exc.message)
            out["errore"] = (f"Libreria ElevenLabs non disponibile ({exc.message}). Se il messaggio "
                             "parla di piano o permessi, il tuo piano non la include.")
            self._send_json(200, out)
            return
        except OSError as exc:
            log.warning("ElevenLabs libreria rete: %s", exc)
            out["errore"] = "Errore di rete verso ElevenLabs"
            self._send_json(200, out)
            return
        type(self).libreria_ammesse = {v["id"]: (v["proprietario"], v["nome"]) for v in voci}
        out["voci"] = voci
        self._send_json(200, out)

    def _aggiungi_voce(self, raw: bytes) -> None:
        """V8b: POST /voci/aggiungi {"voce": id} — aggiunge all'account una voce della
        libreria appena mostrata (mai un id qualunque). Tetto 5 aggiunte/ora: ogni aggiunta
        cambia l'account (e probabilmente occupa uno spazio voce: da verificare)."""
        try:
            voce = (json.loads(raw) if raw else {}).get("voce")
        except (ValueError, AttributeError):
            self._send_json(400, {"error": "Body JSON non valido"})
            return
        voce_info = type(self).libreria_ammesse.get(voce) if isinstance(voce, str) else None
        if voce_info is None:
            self._send_json(409, {"error": "Voce non nella libreria mostrata: ricarica la pagina"})
            return
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "ELEVENLABS_API_KEY non configurata"})
            return
        adesso = time.monotonic()
        recenti = [t for t in type(self).aggiunte_voci if adesso - t < 3600]
        if len(recenti) >= 5:
            self._send_json(429, {"error": "Troppe voci aggiunte nell'ultima ora (5): riprova più tardi."})
            return
        type(self).aggiunte_voci = recenti + [adesso]
        proprietario, nome = voce_info
        try:
            nuovo = add_shared_voice(api_key, proprietario, voce, f"Gas - {nome}")
        except ElevenLabsTTSError as exc:
            log.warning("ElevenLabs aggiunta voce status=%s: %s", exc.status, exc.message)
            self._send_json(502, {"error": f"ElevenLabs non ha aggiunto la voce: {exc.message}"})
            return
        except OSError as exc:
            log.warning("ElevenLabs aggiunta voce rete: %s", exc)
            self._send_json(502, {"error": "Errore di rete verso ElevenLabs"})
            return
        self._send_json(200, {"id": nuovo, "nome": nome})

    def _prova_voce(self, raw: bytes) -> None:
        """POST /voci/prova {"voce": id | "piper", "frase": 0..N-1} → audio della frase
        fissa con quella voce. Tetto proprio (GAS_VOICE_MAX_PROVE_ORA, default 40/ora):
        ogni prova spende caratteri ElevenLabs."""
        try:
            data = json.loads(raw) if raw else {}
            voce = data.get("voce")
            frase = data.get("frase", 0)
        except (ValueError, AttributeError):
            self._send_json(400, {"error": "Body JSON non valido"})
            return
        if not isinstance(frase, int) or isinstance(frase, bool) or not 0 <= frase < len(prova_voci.FRASI_PROVA):
            self._send_json(400, {"error": "Frase di prova non valida"})
            return
        if voce != prova_voci.PIPER and not prova_voci.voce_valida(voce):
            self._send_json(400, {"error": "Voce non valida"})
            return
        if voce != prova_voci.PIPER and voce not in type(self).voci_ammesse:
            self._send_json(409, {"error": "Voce non nell'elenco: ricarica la pagina «prova voci» "
                                           "(si provano solo le voci elencate, mai cloni)"})
            return
        adesso = time.monotonic()
        recenti = [t for t in type(self).prove_voci if adesso - t < 3600]
        try:
            tetto = max(1, int(os.environ.get("GAS_VOICE_MAX_PROVE_ORA", "") or 40))
        except ValueError:
            tetto = 40
        if len(recenti) >= tetto:
            self._send_json(429, {"error": f"Troppe prove di voce nell'ultima ora ({tetto}, "
                                           "GAS_VOICE_MAX_PROVE_ORA). Riprova più tardi."})
            return
        testo = prova_voci.FRASI_PROVA[frase]
        if voce == prova_voci.PIPER:
            modello = prova_voci.piper_disponibile()
            if modello is None:
                self._send_json(503, {"error": "Piper non disponibile: servono il comando "
                                               "«piper» e GAS_PIPER_MODEL nel .env"})
                return
            try:
                audio = prova_voci.sintetizza_piper(testo, modello)
            except (OSError, subprocess.SubprocessError) as exc:
                log.warning("Piper errore: %s", type(exc).__name__)
                self._send_json(502, {"error": "Piper non è riuscito a parlare"})
                return
            self._send_audio(audio, "audio/wav")
            return
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "TTS non disponibile: ELEVENLABS_API_KEY non configurata"})
            return
        type(self).prove_voci = recenti + [adesso]
        try:
            audio = synthesize_speech(testo, api_key, voce)
        except ElevenLabsTTSError as exc:
            log.warning("ElevenLabs prova voce status=%s: %s", exc.status, exc.message)
            self._send_json(502, {"error": f"Errore TTS ElevenLabs: {exc.message}"})
            return
        except OSError as exc:
            log.warning("ElevenLabs prova voce rete: %s", exc)
            self._send_json(502, {"error": "Errore di rete verso ElevenLabs TTS"})
            return
        self._send_audio(audio)

    do_PUT = _method_not_allowed
    do_DELETE = _method_not_allowed
    do_PATCH = _method_not_allowed


def _carica_env() -> None:
    """Carica il `.env` accanto a gas.py come fa la CLI di Gas (V-1 bot #304: senza,
    GAS_VOCE_FORTE scritto nel `.env` restava spento senza segnale). Stesse regole di
    gas._carica_dotenv (la shell vince, GAS_NO_DOTENV=1 lo spegne). Fail-safe §9."""
    try:
        from gas import _carica_dotenv
        _carica_dotenv()
    except Exception as exc:  # gas.py assente o rotto: si prosegue con l'ambiente
        log.warning(".env non caricato dal server voce: %s", type(exc).__name__)


def run_server(root_dir: Optional[str] = None) -> int:
    """Avvia il server HTTP voice. Blocca fino a KeyboardInterrupt.
    Exit code: 0 = uscita pulita, 1 = configurazione mancante."""

    # V2 (V-3 ve #304): import e kernel richiedono qualche secondo, prima di ogni altra riga
    print("… gas voice: avvio in corso (carico Gas, qualche secondo)…", flush=True)
    root = Path(root_dir or os.getcwd()).resolve()
    import sys as _sys
    _sys.path.insert(0, str(root if (root / "gas.py").exists() else root.parent))
    _carica_env()

    token = os.environ.get("GAS_VOICE_TOKEN", "").strip()
    if not token:
        print("✗ gas voice: GAS_VOICE_TOKEN non configurato (fail-closed).")
        print("  Genera un token casuale e impostalo: export GAS_VOICE_TOKEN=$(openssl rand -hex 32)")
        return 1

    bind = (os.environ.get("GAS_VOICE_BIND") or "127.0.0.1").strip() or "127.0.0.1"
    try:
        port = int(os.environ.get("GAS_VOICE_PORT") or "8765")
    except ValueError:
        print("✗ gas voice: GAS_VOICE_PORT non è un numero intero valido.")
        return 1

    from gas import GasKernel  # import pigro: non richiede gas.py al semplice import del modulo

    kernel = GasKernel(root_dir=str(root))

    VoiceHandler.kernel = kernel
    VoiceHandler.token = token

    server = HTTPServer((bind, port), VoiceHandler)
    print(f"✓ gas voice: in ascolto su http://{bind}:{port}{_ENDPOINT}")
    if _voce_tutta_forte():
        print("  GAS_VOCE_FORTE acceso: ogni richiesta va al solo cervello forte.")
    print("  Ctrl-C per uscire.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ gas voice: interruzione ricevuta, uscita.")
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":  # avvio: python -m modules.voice.server (dalla cartella di Gas)
    import sys as _sys
    _sys.exit(run_server())
