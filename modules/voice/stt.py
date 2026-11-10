"""
STT (Speech-to-Text) via Groq Whisper — FASE 3, Fetta 2.

Funzione pubblica: transcribe_audio()
Zero dipendenze esterne: usa esclusivamente stdlib (http.client, json, os, re).
"""
from __future__ import annotations

import http.client
import json
import math
import os
import re
from typing import Any, Callable, List, Optional, Tuple

_GROQ_HOST = "api.groq.com"
_GROQ_PATH = "/openai/v1/audio/transcriptions"
_GROQ_MODEL = "whisper-large-v3"
_TIMEOUT = 30

# V6 (chat M2, «capire meglio»): Whisper sa che si parla italiano e conosce le parole di Gas
# (il prompt è un aiuto al vocabolario, non un'istruzione), temperatura 0 = niente varianti
# creative. verbose_json dà per ogni segmento la probabilità di silenzio e la confidenza.
_LINGUA = "it"
_PROMPT_GAS = ("Conversazione in italiano con Gas, l'assistente dell'operatore. Parole "
               "frequenti: Gas, forte, lead, bozza, firma, contatto, rubrica, diario, memoria, "
               "funnel, marketing, Telegram, Claude, Groq, ElevenLabs, VPS, report, PR, merge.")
# Soglie della trascrizione incerta (sovrascrivibili via env per tararle sul Mac):
# confidenza media (avg_logprob pesato per durata) sotto il minimo, oppure probabilità
# di silenzio media sopra il massimo → «non ho capito, ripeti?» invece di rispondere a caso.
# R-611-1-M2: come in Whisper, il «silenzio» vale solo se ANCHE la confidenza è bassa
# (sotto _LOGPROB_SILENZIO): su large-v3 no_speech_prob è alto anche su un «sì» breve e
# chiaro, che deve passare.
_LOGPROB_MIN_DEFAULT = -1.0
_NO_SPEECH_MAX_DEFAULT = 0.8
_LOGPROB_SILENZIO = -0.5
# R-611-2-M2 / R-612-1-M2: sul silenzio Whisper può ripetere il prompt: una trascrizione
# che è un PEZZO CONTIGUO del prompt (almeno 4 parole, nello stesso ordine) non è
# l'operatore che parla. Le parole del prompt in un ordine diverso («Gas, forte, firma
# la bozza») sono un comando vero e passano.
_PROMPT_ECO_MIN_PAROLE = 4
# V-1 bot #318: un'eco CORTA del prompt (2-3 parole contigue, es. «Gas, forte, lead.») può
# essere anche un comando vero: si scarta solo se i segmenti dicono «quasi certo silenzio».
# R-614-1-M2: soglia sopra quella di un «Sì.» chiaro su large-v3 (no_speech ~0,85),
# tarabile con GAS_VOICE_STT_ECO_NO_SPEECH.
_PROMPT_ECO_CORTA_MIN_PAROLE = 2
_ECO_CORTA_NO_SPEECH_DEFAULT = 0.9
# Frasi che Whisper inventa sul silenzio o sul rumore (sottotitoli dei video su cui è
# stato addestrato): se la trascrizione le contiene, non è l'operatore che parla.
_ALLUCINAZIONI_PARTI = ("amara.org", "qtss", "sottotitoli creati", "sottotitoli a cura",
                        "sottotitoli e revisione")
_ALLUCINAZIONI_INTERE = ("grazie per la visione", "grazie per l'ascolto",
                         "iscriviti al canale", "grazie a tutti per la visione")


class GroqSTTError(Exception):
    """Errore dall'API Groq Whisper (rete o risposta non 200)."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


_PAROLA = re.compile(r"[a-zàèéìòù0-9]+")
_PAROLE_PROMPT = tuple(_PAROLA.findall(_PROMPT_GAS.lower()))


def _pezzo_del_prompt(parole: List[str]) -> bool:
    """True se `parole` compare tale e quale, contigua, dentro le parole del prompt."""
    n = len(parole)
    return any(list(_PAROLE_PROMPT[i:i + n]) == parole
               for i in range(len(_PAROLE_PROMPT) - n + 1))


class TrascrizioneIncerta(Exception):
    """V6: Groq ha risposto, ma la trascrizione è probabilmente sbagliata (bassa
    confidenza, silenzio, frase inventata da Whisper). `testo` è quello che ha sentito."""

    def __init__(self, testo: str, motivo: str) -> None:
        super().__init__(motivo)
        self.testo = testo
        self.motivo = motivo


def _soglia_env(nome: str, default: float) -> float:
    try:
        v = float(os.environ.get(nome, "").strip() or default)
    except ValueError:
        return default
    return v if math.isfinite(v) else default  # R-611: «nan»/«inf» non spengono il controllo


def _motivo_incerta(testo: str, segmenti: Any) -> Optional[str]:
    """Perché la trascrizione è da scartare, o None se va bene. Senza segmenti (risposta
    senza dettagli) decide solo l'elenco delle frasi inventate."""
    norm = " ".join(testo.lower().split())
    if any(p in norm for p in _ALLUCINAZIONI_PARTI) or norm.rstrip(".!") in _ALLUCINAZIONI_INTERE:
        return "frase tipica di Whisper sul silenzio"
    parole = _PAROLA.findall(norm)
    if len(parole) >= _PROMPT_ECO_MIN_PAROLE and _pezzo_del_prompt(parole):
        return "ripete il prompt di Whisper (silenzio)"
    if not isinstance(segmenti, list) or not segmenti:
        return None
    peso = logprob = no_speech = 0.0
    for seg in segmenti:
        if not isinstance(seg, dict):
            continue  # V-1 ve #318 (2ª verifica): segmento malformato saltato, contano gli altri
        try:
            durata = max(float(seg.get("end", 0)) - float(seg.get("start", 0)), 0.01)
            lp = float(seg["avg_logprob"])
            ns = float(seg["no_speech_prob"])
        except (KeyError, TypeError, ValueError):
            continue  # segmento senza i campi attesi: saltato (nessun segmento valido → None)
        if not all(math.isfinite(x) for x in (durata, lp, ns)):
            continue  # V-1 ve #318 / R-614-2-M2: segmento NaN/inf inutile, contano gli altri
        peso += durata
        logprob += lp * durata
        no_speech += ns * durata
    if peso <= 0:
        return None  # nessun segmento con dati validi: non si scarta a caso
    logprob /= peso
    no_speech /= peso
    if (_PROMPT_ECO_CORTA_MIN_PAROLE <= len(parole) < _PROMPT_ECO_MIN_PAROLE
            and _pezzo_del_prompt(parole)
            and no_speech > _soglia_env("GAS_VOICE_STT_ECO_NO_SPEECH", _ECO_CORTA_NO_SPEECH_DEFAULT)):
        return f"eco corta del prompt di Whisper (no_speech={no_speech:.2f})"
    if (no_speech > _soglia_env("GAS_VOICE_STT_NO_SPEECH_MAX", _NO_SPEECH_MAX_DEFAULT)
            and logprob < _LOGPROB_SILENZIO):
        return f"probabilmente silenzio o rumore (no_speech={no_speech:.2f})"
    if logprob < _soglia_env("GAS_VOICE_STT_LOGPROB_MIN", _LOGPROB_MIN_DEFAULT):
        return f"trascrizione poco sicura (avg_logprob={logprob:.2f})"
    return None


def _build_multipart(audio_bytes: bytes, filename: str) -> Tuple[bytes, str]:
    """Costruisce body multipart/form-data per l'endpoint Groq Whisper."""
    boundary = "GasSTTBoundary" + os.urandom(8).hex()

    def _text_field(name: str, value: str) -> bytes:
        return (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
            f"{value}\r\n"
        ).encode()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode() + audio_bytes + b"\r\n"

    body += _text_field("model", _GROQ_MODEL)
    body += _text_field("response_format", "verbose_json")
    body += _text_field("language", _LINGUA)
    body += _text_field("temperature", "0")
    body += _text_field("prompt", _PROMPT_GAS)
    body += f"--{boundary}--\r\n".encode()

    return body, f"multipart/form-data; boundary={boundary}"


def _parse_multipart_file(raw: bytes, content_type: str) -> Tuple[bytes, str]:
    """Estrae (audio_bytes, filename) dal campo 'file' di un body multipart."""
    boundary = None
    for param in content_type.split(";"):
        param = param.strip()
        if param.lower().startswith("boundary="):
            boundary = param[len("boundary="):].strip().strip('"')
            break
    if not boundary:
        raise ValueError("boundary non trovato nel Content-Type multipart")

    sep = b"--" + boundary.encode()
    parts = raw.split(sep)

    for part in parts[1:]:
        stripped = part.strip()
        if stripped in (b"--", b""):
            continue
        if b"\r\n\r\n" not in part:
            continue
        headers_raw, body = part.split(b"\r\n\r\n", 1)
        if body.endswith(b"\r\n"):
            body = body[:-2]
        headers_str = headers_raw.decode(errors="replace")

        if 'name="file"' not in headers_str and "name=file" not in headers_str:
            continue

        filename = "audio.wav"
        m = re.search(r'filename="?([^";\r\n]+)"?', headers_str, re.IGNORECASE)
        if m:
            filename = m.group(1).strip()

        if not body:
            raise ValueError("campo 'file' nel multipart è vuoto")
        return body, filename

    raise ValueError("campo 'file' non trovato nel multipart")


def parse_audio_body(raw: bytes, content_type: str) -> Tuple[bytes, str]:
    """Estrae (audio_bytes, filename) dal body HTTP in ingresso.

    Supporta:
      - Content-Type: audio/*       → body = raw audio bytes
      - Content-Type: multipart/form-data → estrae il campo 'file'
    Solleva ValueError se il body è vuoto o malformato.
    """
    ct = content_type.split(";")[0].strip().lower()

    if ct.startswith("audio/"):
        if not raw:
            raise ValueError("body audio vuoto")
        ext = ct[len("audio/"):] or "wav"
        return raw, f"audio.{ext}"

    if ct == "multipart/form-data":
        if not raw:
            raise ValueError("body multipart vuoto")
        return _parse_multipart_file(raw, content_type)

    raise ValueError(f"Content-Type non supportato per STT: {content_type!r}")


def transcribe_audio(
    audio_bytes: bytes,
    filename: str,
    api_key: str,
    *,
    _conn_factory: Optional[Callable[[], http.client.HTTPSConnection]] = None,
) -> str:
    """Trascrive audio via Groq Whisper. Ritorna il testo trascritto.

    Raises:
        GroqSTTError:        se Groq risponde con status != 200
        TrascrizioneIncerta: V6, testo probabilmente sbagliato (vedi _motivo_incerta)
        OSError:             in caso di errore di rete/timeout
    Non logga i byte audio né la chiave API.
    """
    body, multipart_ct = _build_multipart(audio_bytes, filename)

    conn = _conn_factory() if _conn_factory is not None else http.client.HTTPSConnection(_GROQ_HOST, timeout=_TIMEOUT)
    try:
        conn.request(
            "POST",
            _GROQ_PATH,
            body=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": multipart_ct,
                "Content-Length": str(len(body)),
            },
        )
        try:
            resp = conn.getresponse()
            resp_body = resp.read()
        except http.client.HTTPException as exc:  # audit 10 nov (B3): IncompleteRead,
            # BadStatusLine… come un errore di rete, così il chiamante risponde al client
            raise OSError(f"risposta rotta ({type(exc).__name__})") from exc
        if resp.status == 200:
            try:
                data = json.loads(resp_body)
            except json.JSONDecodeError:
                raise GroqSTTError(resp.status, f"risposta Groq non JSON: {resp_body[:100].decode(errors='replace')}")
            if not isinstance(data, dict):
                raise GroqSTTError(resp.status, "risposta Groq non è un oggetto JSON")
            testo = (data.get("text") or "").strip()
            motivo = _motivo_incerta(testo, data.get("segments")) if testo else None
            if motivo:
                raise TrascrizioneIncerta(testo, motivo)
            return testo
        msg = resp_body.decode(errors="replace")[:300]
        raise GroqSTTError(resp.status, f"Groq {resp.status}: {msg}")
    finally:
        conn.close()
