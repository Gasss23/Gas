"""
STT (Speech-to-Text) via Groq Whisper — FASE 3, Fetta 2.

Funzione pubblica: transcribe_audio()
Zero dipendenze esterne: usa esclusivamente stdlib (http.client, json, os, re).
"""
from __future__ import annotations

import http.client
import json
import os
import re
from typing import Callable, Optional, Tuple

_GROQ_HOST = "api.groq.com"
_GROQ_PATH = "/openai/v1/audio/transcriptions"
_GROQ_MODEL = "whisper-large-v3"
_TIMEOUT = 30


class GroqSTTError(Exception):
    """Errore dall'API Groq Whisper (rete o risposta non 200)."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


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
    body += _text_field("response_format", "json")
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
        GroqSTTError: se Groq risponde con status != 200
        OSError:      in caso di errore di rete/timeout
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
        resp = conn.getresponse()
        resp_body = resp.read()
        if resp.status == 200:
            try:
                data = json.loads(resp_body)
            except json.JSONDecodeError:
                raise GroqSTTError(resp.status, f"risposta Groq non JSON: {resp_body[:100].decode(errors='replace')}")
            return (data.get("text") or "").strip()
        msg = resp_body.decode(errors="replace")[:300]
        raise GroqSTTError(resp.status, f"Groq {resp.status}: {msg}")
    finally:
        conn.close()
