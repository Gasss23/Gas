"""
TTS (Text-to-Speech) via ElevenLabs Flash — FASE 3, Fetta 3.

Funzione pubblica: synthesize_speech()
Zero dipendenze esterne: usa esclusivamente stdlib (http.client, json).
"""
from __future__ import annotations

import http.client
import json
from typing import Callable, Optional

_ELEVENLABS_HOST = "api.elevenlabs.io"
_ELEVENLABS_PATH_TMPL = "/v1/text-to-speech/{voice_id}"
_ELEVENLABS_MODEL = "eleven_flash_v2_5"
DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # George — premade ElevenLabs, sempre disponibile
_TIMEOUT = 30


class ElevenLabsTTSError(Exception):
    """Errore dall'API ElevenLabs (rete o risposta non 200)."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


def synthesize_speech(
    text: str,
    api_key: str,
    voice_id: str,
    *,
    _conn_factory: Optional[Callable[[], http.client.HTTPSConnection]] = None,
) -> bytes:
    """Sintetizza testo in audio MP3 via ElevenLabs Flash. Ritorna i byte MP3 grezzi.

    Raises:
        ElevenLabsTTSError: se ElevenLabs risponde con status != 200
        OSError:            in caso di errore di rete/timeout
    Non logga la chiave API né i byte audio.
    """
    path = _ELEVENLABS_PATH_TMPL.format(voice_id=voice_id)
    body = json.dumps(
        {
            "text": text,
            "model_id": _ELEVENLABS_MODEL,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }
    ).encode("utf-8")

    conn = (
        _conn_factory()
        if _conn_factory is not None
        else http.client.HTTPSConnection(_ELEVENLABS_HOST, timeout=_TIMEOUT)
    )
    try:
        conn.request(
            "POST",
            path,
            body=body,
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json",
                "Content-Length": str(len(body)),
            },
        )
        resp = conn.getresponse()
        resp_bytes = resp.read()
        if resp.status == 200:
            return resp_bytes
        msg = resp_bytes.decode(errors="replace")[:300]
        raise ElevenLabsTTSError(resp.status, f"ElevenLabs {resp.status}: {msg}")
    finally:
        conn.close()
