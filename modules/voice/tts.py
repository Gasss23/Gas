"""
TTS (Text-to-Speech) via ElevenLabs Flash — FASE 3, Fetta 3.

Funzione pubblica: synthesize_speech()
Zero dipendenze esterne: usa esclusivamente stdlib (http.client, json).
"""
from __future__ import annotations

import http.client
import json
import logging
import os
from typing import Callable, Optional

_ELEVENLABS_HOST = "api.elevenlabs.io"
_ELEVENLABS_PATH_TMPL = "/v1/text-to-speech/{voice_id}"
_ELEVENLABS_MODEL = "eleven_flash_v2_5"
DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # George — premade ElevenLabs, sempre disponibile
_TIMEOUT = 30

_DEFAULT_TTS_MAX_CHARS = 2000
_SENTENCE_ENDS = frozenset(".!?")


def _cap_text(text: str) -> str:
    """Tronca il testo al limite GAS_TTS_MAX_CHARS prima di inviarlo a ElevenLabs.

    Priorità di troncamento: ultimo confine di frase (., !, ?) ≤ limite;
    poi ultimo spazio ≤ limite; poi hard-cut al limite.
    Garantisce che ElevenLabs non riceva mai più di max_chars caratteri.
    """
    try:
        max_chars = int(os.environ.get("GAS_TTS_MAX_CHARS", _DEFAULT_TTS_MAX_CHARS))
    except ValueError:
        logging.warning("GAS_TTS_MAX_CHARS non numerica, uso default %d", _DEFAULT_TTS_MAX_CHARS)
        max_chars = _DEFAULT_TTS_MAX_CHARS
    if len(text) <= max_chars:
        return text

    original_len = len(text)
    window = text[:max_chars]

    # Cerca l'ultimo confine di frase nel window
    cut = -1
    for i in range(max_chars - 1, -1, -1):
        if window[i] in _SENTENCE_ENDS:
            cut = i + 1
            break

    if cut == -1:
        # Fallback: ultimo spazio
        cut = window.rfind(" ")

    if cut <= 0:
        # Hard-cut: nessun confine trovato
        cut = max_chars

    truncated = text[:cut]
    if len(truncated) > max_chars:
        truncated = truncated[:max_chars]
    logging.warning(
        "TTS text cap: testo originale %d char, troncato a %d char (limite GAS_TTS_MAX_CHARS=%d)",
        original_len,
        len(truncated),
        max_chars,
    )
    return truncated


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
    text = _cap_text(text)
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


# ── V8 (chat M2): elenco delle voci dell'account, per la pagina «prova voci» ──

_ELEVENLABS_VOICES_PATH = "/v1/voices"


def list_voices(
    api_key: str,
    *,
    _conn_factory: Optional[Callable[[], http.client.HTTPSConnection]] = None,
) -> list:
    """Voci disponibili sull'account ElevenLabs (GET /v1/voices), ridotte ai campi utili:
    [{"id", "nome", "categoria", "genere", "accento", "eta", "descrizione"}].

    Raises:
        ElevenLabsTTSError: risposta non 200 o non leggibile
        OSError:            errore di rete/timeout
    Non logga la chiave API."""
    conn = (
        _conn_factory()
        if _conn_factory is not None
        else http.client.HTTPSConnection(_ELEVENLABS_HOST, timeout=_TIMEOUT)
    )
    try:
        conn.request("GET", _ELEVENLABS_VOICES_PATH, headers={"xi-api-key": api_key})
        resp = conn.getresponse()
        corpo = resp.read()
        if resp.status != 200:
            raise ElevenLabsTTSError(resp.status, f"ElevenLabs {resp.status}: "
                                                  f"{corpo.decode(errors='replace')[:300]}")
        try:
            voci = json.loads(corpo).get("voices") or []
        except (ValueError, AttributeError):
            raise ElevenLabsTTSError(resp.status, "elenco voci ElevenLabs non leggibile")
        if not isinstance(voci, list):  # R-624-2-M2: forma inattesa → errore dichiarato
            raise ElevenLabsTTSError(resp.status, "elenco voci ElevenLabs non leggibile")
    finally:
        conn.close()
    out = []
    for v in voci:
        if not isinstance(v, dict) or not isinstance(v.get("voice_id"), str):
            continue
        etichette = v.get("labels") if isinstance(v.get("labels"), dict) else {}
        out.append({
            "id": v["voice_id"],
            "nome": str(v.get("name") or "")[:80],
            "categoria": str(v.get("category") or "")[:40],
            "genere": str(etichette.get("gender") or "")[:40],
            "accento": str(etichette.get("accent") or "")[:40],
            "eta": str(etichette.get("age") or "")[:40],
            "descrizione": str(etichette.get("description") or v.get("description") or "")[:200],
        })
    return out


# ── V8b (chat M2): libreria condivisa di ElevenLabs (voci di altri, da aggiungere) ──
# ATTENZIONE: percorsi, filtri e campi scritti senza poter leggere la documentazione
# ufficiale (rete del cloud bloccata il 2026-11-02): DA VERIFICARE sul Mac. Qualunque
# risposta diversa diventa un errore dichiarato, mai un crash.

_SHARED_VOICES_PATH = "/v1/shared-voices"
_ADD_SHARED_PATH = "/v1/voices/add/{owner}/{voice_id}"


def list_shared_voices(
    api_key: str,
    filtri: Optional[dict] = None,
    *,
    _conn_factory: Optional[Callable[[], http.client.HTTPSConnection]] = None,
) -> list:
    """Voci della libreria condivisa (GET /v1/shared-voices con i filtri dati), ridotte a
    [{"id", "proprietario", "nome", "categoria", "genere", "accento", "eta",
      "descrizione", "anteprima"}]. Raises ElevenLabsTTSError / OSError."""
    import urllib.parse
    query = urllib.parse.urlencode({k: v for k, v in (filtri or {}).items() if v})
    conn = (
        _conn_factory()
        if _conn_factory is not None
        else http.client.HTTPSConnection(_ELEVENLABS_HOST, timeout=_TIMEOUT)
    )
    try:
        conn.request("GET", _SHARED_VOICES_PATH + (f"?{query}" if query else ""),
                     headers={"xi-api-key": api_key})
        resp = conn.getresponse()
        corpo = resp.read()
        if resp.status != 200:
            raise ElevenLabsTTSError(resp.status, f"ElevenLabs {resp.status}: "
                                                  f"{corpo.decode(errors='replace')[:300]}")
        try:
            voci = json.loads(corpo).get("voices")
        except (ValueError, AttributeError):
            raise ElevenLabsTTSError(resp.status, "libreria ElevenLabs non leggibile")
        if not isinstance(voci, list):
            raise ElevenLabsTTSError(resp.status, "libreria ElevenLabs non leggibile")
    finally:
        conn.close()
    out = []
    for v in voci:
        if not isinstance(v, dict) or not isinstance(v.get("voice_id"), str) \
                or not isinstance(v.get("public_owner_id"), str):
            continue
        anteprima = v.get("preview_url")
        out.append({
            "id": v["voice_id"],
            "proprietario": v["public_owner_id"],
            "nome": str(v.get("name") or "")[:80],
            "categoria": str(v.get("category") or "")[:40],
            "genere": str(v.get("gender") or "")[:40],
            "accento": str(v.get("accent") or "")[:40],
            "eta": str(v.get("age") or "")[:40],
            "descrizione": str(v.get("descriptive") or v.get("description") or "")[:200],
            "anteprima": anteprima if isinstance(anteprima, str) and anteprima.startswith("https://") else "",
        })
    return out


def add_shared_voice(
    api_key: str,
    owner: str,
    voice_id: str,
    new_name: str,
    *,
    _conn_factory: Optional[Callable[[], http.client.HTTPSConnection]] = None,
) -> str:
    """Aggiunge una voce della libreria all'account (POST /v1/voices/add/{owner}/{id}).
    Ritorna l'id della voce nell'account. Raises ElevenLabsTTSError / OSError.
    I parametri vanno validati dal chiamante (finiscono nel percorso)."""
    body = json.dumps({"new_name": new_name[:80]}).encode("utf-8")
    conn = (
        _conn_factory()
        if _conn_factory is not None
        else http.client.HTTPSConnection(_ELEVENLABS_HOST, timeout=_TIMEOUT)
    )
    try:
        conn.request("POST", _ADD_SHARED_PATH.format(owner=owner, voice_id=voice_id), body=body,
                     headers={"xi-api-key": api_key, "Content-Type": "application/json",
                              "Content-Length": str(len(body))})
        resp = conn.getresponse()
        corpo = resp.read()
        if resp.status != 200:
            raise ElevenLabsTTSError(resp.status, f"ElevenLabs {resp.status}: "
                                                  f"{corpo.decode(errors='replace')[:300]}")
        try:
            nuovo = json.loads(corpo).get("voice_id")
        except (ValueError, AttributeError):
            nuovo = None
        if not isinstance(nuovo, str):
            raise ElevenLabsTTSError(resp.status, "risposta all'aggiunta della voce non leggibile")
        return nuovo
    finally:
        conn.close()
