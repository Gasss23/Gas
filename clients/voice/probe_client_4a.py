#!/usr/bin/env python3
"""
FASE 3 Fetta 4a — client vocale di prova (usa-e-getta)

Pipeline: mic (PulseAudio) → ffmpeg WAV → POST /voice (STT Groq + kernel + TTS ElevenLabs)
          → MP3 → ffmpeg → altoparlante (PulseAudio)

Variabili d'ambiente richieste:
  GAS_VOICE_TOKEN  — token bearer identico a quello del server (OBBLIGATORIO)
  GAS_VOICE_URL    — URL base server (default: http://localhost:8765)

Uso:
  python probe_client_4a.py [secondi]        # pipeline completa audio→audio
  python probe_client_4a.py --text-only [s]  # audio→JSON (vedi risposta kernel, niente TTS)

Esempi:
  GAS_VOICE_TOKEN=xxx python probe_client_4a.py 5
  GAS_VOICE_TOKEN=xxx python probe_client_4a.py --text-only 5

Dipendenze: stdlib + ffmpeg (libpulse) — NESSUNA libreria Python aggiuntiva.
"""
from __future__ import annotations

import http.client
import os
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

_DEFAULT_URL = "http://localhost:8765"
_ENDPOINT = "/voice"
_DEFAULT_SECS = 5


def _record_wav(seconds: int) -> bytes:
    """Registra dal microfono default di PulseAudio per <seconds> s. Ritorna byte WAV 16kHz mono."""
    print(f"[rec] avvio registrazione {seconds}s (parla ora)...")
    cmd = [
        "ffmpeg", "-loglevel", "warning",
        "-f", "pulse", "-i", "default",
        "-t", str(seconds),
        "-ar", "16000", "-ac", "1",
        "-f", "wav", "pipe:1",
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        stderr = result.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"ffmpeg registrazione fallita (exit {result.returncode}):\n{stderr}")
    if not result.stdout:
        raise RuntimeError("ffmpeg ha prodotto output vuoto (microfono non disponibile?)")
    print(f"[rec] catturati {len(result.stdout):,} byte WAV")
    return result.stdout


def _post_voice(url_base: str, token: str, wav_bytes: bytes, *, want_audio: bool) -> tuple[int, str, bytes]:
    """POST /voice con audio WAV.
    want_audio=True  → Accept: audio/mpeg, ritorna MP3 bytes se 200
    want_audio=False → Accept: application/json, ritorna JSON body
    Ritorna (status_code, content_type, body_bytes).
    """
    parsed = urllib.parse.urlparse(url_base)
    host = parsed.hostname or "localhost"
    port = parsed.port or 8765
    scheme = (parsed.scheme or "http").lower()

    if scheme == "https":
        conn: http.client.HTTPConnection = http.client.HTTPSConnection(host, port, timeout=60)
    else:
        conn = http.client.HTTPConnection(host, port, timeout=60)

    accept = "audio/mpeg" if want_audio else "application/json"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "audio/wav",
        "Content-Length": str(len(wav_bytes)),
        "Accept": accept,
    }

    mode = "audio/mpeg" if want_audio else "JSON"
    print(f"[http] POST {url_base}{_ENDPOINT} — {len(wav_bytes):,} byte WAV, Accept: {accept}...")
    try:
        conn.request("POST", _ENDPOINT, body=wav_bytes, headers=headers)
        resp = conn.getresponse()
        body = resp.read()
        ct = resp.getheader("Content-Type", "")
    finally:
        conn.close()

    print(f"[http] risposta {resp.status} Content-Type: {ct}")
    return resp.status, ct, body


def _play_mp3(mp3_bytes: bytes) -> None:
    """Riproduce byte MP3 su PulseAudio default sink via ffmpeg."""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(mp3_bytes)
        tmp_path = f.name
    print(f"[play] riproduzione {len(mp3_bytes):,} byte MP3 su PulseAudio...")
    try:
        cmd = [
            "ffmpeg", "-loglevel", "warning",
            "-i", tmp_path,
            "-f", "pulse", "default",
        ]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"[WARN] ffmpeg play exit {result.returncode} — audio potrebbe non essere uscito")
        else:
            print("[play] completato.")
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def _run_audio_mode(url_base: str, token: str, seconds: int) -> int:
    """Pipeline completa: mic → WAV → /voice → MP3 → altoparlante."""
    wav = _record_wav(seconds)

    status, ct, body = _post_voice(url_base, token, wav, want_audio=True)

    if status != 200:
        try:
            err = body.decode("utf-8", errors="replace")
        except Exception:
            err = repr(body[:200])
        print(f"ERRORE server {status}: {err}", file=sys.stderr)
        return 1

    if "audio" not in ct:
        print(f"ERRORE: risposta non audio (Content-Type: {ct})", file=sys.stderr)
        print(f"  body: {body[:300].decode(errors='replace')}", file=sys.stderr)
        return 1

    _play_mp3(body)
    print("[ok] pipeline audio completata.")
    return 0


def _run_text_only_mode(url_base: str, token: str, seconds: int) -> int:
    """Modalità debug: mic → WAV → /voice → JSON (mostra risposta kernel, niente TTS)."""
    wav = _record_wav(seconds)

    status, ct, body = _post_voice(url_base, token, wav, want_audio=False)

    try:
        text = body.decode("utf-8", errors="replace")
    except Exception:
        text = repr(body[:500])

    print(f"[resp] status={status} body={text}")

    if status != 200:
        print(f"ERRORE server {status}", file=sys.stderr)
        return 1

    print("[ok] pipeline testo completata (nessun TTS in questa modalità).")
    return 0


def main() -> int:
    args = sys.argv[1:]

    text_only = False
    if args and args[0] == "--text-only":
        text_only = True
        args = args[1:]

    seconds = _DEFAULT_SECS
    if args:
        try:
            seconds = int(args[0])
            if seconds < 1:
                raise ValueError
        except ValueError:
            print(f"ERRORE: secondi deve essere intero ≥ 1, ricevuto: {args[0]!r}", file=sys.stderr)
            return 1

    token = os.environ.get("GAS_VOICE_TOKEN", "").strip()
    if not token:
        print("ERRORE: GAS_VOICE_TOKEN non impostato.", file=sys.stderr)
        print("  export GAS_VOICE_TOKEN=<token>", file=sys.stderr)
        return 1

    url_base = (os.environ.get("GAS_VOICE_URL") or _DEFAULT_URL).rstrip("/")

    print(f"[cfg] server={url_base}  secs={seconds}  mode={'text-only' if text_only else 'audio'}")

    try:
        if text_only:
            return _run_text_only_mode(url_base, token, seconds)
        else:
            return _run_audio_mode(url_base, token, seconds)
    except RuntimeError as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrotto.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
