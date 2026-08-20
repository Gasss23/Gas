"""
Test suite STT — FASE 3, Fetta 2.

Copre:
  - Routing audio vs JSON in VoiceHandler.do_POST (TVA-route-*)
  - Parsing multipart e audio raw (TVA-parse-*)
  - transcribe_audio con transport iniettato (TVA-transcribe-*)
  - Tutti i rami d'errore (chiave assente, audio vuoto, Groq 400/5xx/429, rete)

Zero chiamate di rete reali: il transport HTTP è sempre iniettato.
Zero token LLM: il kernel è sempre un mock.
"""
from __future__ import annotations

import http.client
import json
import os
import struct
import sys
import threading
from http.server import HTTPServer
from io import BytesIO
from pathlib import Path
from typing import Any, Generator, List, Optional
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.voice.server import VoiceHandler, _token_ok
from modules.voice.stt import (
    GroqSTTError,
    _parse_multipart_file,
    parse_audio_body,
    transcribe_audio,
)


# ─────────────────────────────── helpers comuni ──────────────────────────────

class _MockKernel:
    def __init__(self, events=None):
        self._events = events or [{"type": "final", "content": "ok kernel"}]

    def run_turn(self, prompt: str) -> Generator[dict, None, None]:
        yield from self._events


def _make_server(kernel: Any, token: str) -> tuple[HTTPServer, int]:
    class _H(VoiceHandler):
        pass
    _H.kernel = kernel
    _H.token = token
    srv = HTTPServer(("127.0.0.1", 0), _H)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv, port


def _post_raw(port: int, body: bytes, headers: dict) -> tuple[int, dict]:
    import urllib.error
    import urllib.request
    url = f"http://127.0.0.1:{port}/voice"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


_TOKEN = "test-token-stt-abc"
_AUTH = {"Authorization": f"Bearer {_TOKEN}"}


def _wav_header(data_size: int = 0) -> bytes:
    """Genera un header WAV minimale valido (44 byte)."""
    return (
        b"RIFF" + struct.pack("<I", 36 + data_size) + b"WAVE"
        + b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, 16000, 32000, 2, 16)
        + b"data" + struct.pack("<I", data_size)
    )


def _fake_wav(n_samples: int = 100) -> bytes:
    """WAV sintetico minimo con dati."""
    samples = bytes(n_samples * 2)  # silenzio PCM
    return _wav_header(len(samples)) + samples


# ─────────────────── Fake transport per transcribe_audio ─────────────────────

class _FakeResponse:
    def __init__(self, status: int, body: str | bytes):
        self.status = status
        self._body = body.encode() if isinstance(body, str) else body

    def read(self) -> bytes:
        return self._body


class _FakeConn:
    """Sostituisce http.client.HTTPSConnection nei test."""

    def __init__(self, status: int = 200, body: str = '{"text": "trascrizione di test"}'):
        self._resp = _FakeResponse(status, body)
        self.last_kwargs: dict = {}

    def request(self, method, path, body=None, headers=None):
        self.last_kwargs = {"method": method, "path": path, "body": body, "headers": headers}

    def getresponse(self) -> _FakeResponse:
        return self._resp

    def close(self) -> None:
        pass


def _factory(conn: _FakeConn):
    return lambda: conn


# ═══════════════════════════════════════════════════════════════════════════════
# TVA-transcribe-*: test di transcribe_audio con transport iniettato
# ═══════════════════════════════════════════════════════════════════════════════

class TestTranscribeAudio:

    def test_success_returns_text(self):
        conn = _FakeConn(200, '{"text": "ciao mondo"}')
        result = transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert result == "ciao mondo"

    def test_sends_to_correct_endpoint(self):
        conn = _FakeConn()
        transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert conn.last_kwargs["path"] == "/openai/v1/audio/transcriptions"
        assert conn.last_kwargs["method"] == "POST"

    def test_sends_bearer_auth(self):
        conn = _FakeConn()
        transcribe_audio(_fake_wav(), "audio.wav", "my-secret-key", _conn_factory=_factory(conn))
        assert conn.last_kwargs["headers"]["Authorization"] == "Bearer my-secret-key"

    def test_groq_400_raises_groq_error(self):
        conn = _FakeConn(400, '{"error": "formato invalido"}')
        with pytest.raises(GroqSTTError) as exc_info:
            transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert exc_info.value.status == 400

    def test_groq_429_raises_groq_error(self):
        conn = _FakeConn(429, '{"error": "quota"}')
        with pytest.raises(GroqSTTError) as exc_info:
            transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert exc_info.value.status == 429

    def test_groq_500_raises_groq_error(self):
        conn = _FakeConn(500, '{"error": "server error"}')
        with pytest.raises(GroqSTTError) as exc_info:
            transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert exc_info.value.status == 500

    def test_network_error_raises_oserror(self):
        class _BrokenConn:
            def request(self, *a, **kw): raise OSError("connection refused")
            def close(self): pass

        with pytest.raises(OSError):
            transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=lambda: _BrokenConn())

    def test_empty_text_in_response(self):
        conn = _FakeConn(200, '{"text": ""}')
        result = transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert result == ""

    def test_text_stripped(self):
        conn = _FakeConn(200, '{"text": "  ciao  "}')
        result = transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert result == "ciao"

    def test_groq_200_non_json_body_raises_groq_error(self):
        """R-stt-1: Groq 200 con body non-JSON → GroqSTTError (non JSONDecodeError nuda)."""
        conn = _FakeConn(200, b"<html>Cloudflare error</html>")
        with pytest.raises(GroqSTTError) as exc_info:
            transcribe_audio(_fake_wav(), "audio.wav", "key-test", _conn_factory=_factory(conn))
        assert exc_info.value.status == 200
        assert "non JSON" in exc_info.value.message


# ═══════════════════════════════════════════════════════════════════════════════
# TVA-parse-*: test di parse_audio_body
# ═══════════════════════════════════════════════════════════════════════════════

class TestParseAudioBody:

    def test_audio_wav_raw(self):
        raw = _fake_wav()
        audio, fname = parse_audio_body(raw, "audio/wav")
        assert audio == raw
        assert fname == "audio.wav"

    def test_audio_mp3_raw(self):
        raw = b"\xff\xfb\x90\x00" + bytes(100)
        audio, fname = parse_audio_body(raw, "audio/mpeg")
        assert audio == raw
        assert fname == "audio.mpeg"

    def test_audio_raw_empty_raises(self):
        with pytest.raises(ValueError, match="vuoto"):
            parse_audio_body(b"", "audio/wav")

    def test_multipart_extracts_file(self):
        wav = _fake_wav()
        boundary = "testboundary123"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="voce.wav"\r\n'
            f"Content-Type: audio/wav\r\n\r\n"
        ).encode() + wav + (
            f"\r\n--{boundary}--\r\n"
        ).encode()

        audio, fname = parse_audio_body(body, f"multipart/form-data; boundary={boundary}")
        assert audio == wav
        assert fname == "voce.wav"

    def test_multipart_empty_raises(self):
        with pytest.raises(ValueError):
            parse_audio_body(b"", "multipart/form-data; boundary=x")

    def test_multipart_missing_file_field_raises(self):
        boundary = "testboundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="model"\r\n\r\n'
            f"whisper-large-v3\r\n"
            f"--{boundary}--\r\n"
        ).encode()
        with pytest.raises(ValueError, match="non trovato"):
            parse_audio_body(body, f"multipart/form-data; boundary={boundary}")

    def test_unsupported_content_type_raises(self):
        with pytest.raises(ValueError, match="non supportato"):
            parse_audio_body(b"...", "application/json")


# ═══════════════════════════════════════════════════════════════════════════════
# TVA-route-*: test del routing audio vs JSON in VoiceHandler
# ═══════════════════════════════════════════════════════════════════════════════

class TestVoiceHandlerRouting:
    """Verifica che audio e JSON vengano instradati correttamente."""

    def setup_method(self):
        self.kernel = _MockKernel()
        self.server, self.port = _make_server(self.kernel, _TOKEN)

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def test_json_path_unchanged(self):
        """JSON {"prompt": ...} → path attuale, nessuna STT."""
        hdrs = {**_AUTH, "Content-Type": "application/json"}
        body = json.dumps({"prompt": "ciao"}).encode()
        with patch("modules.voice.server.transcribe_audio") as mock_stt:
            status, resp = _post_raw(self.port, body, hdrs)
        mock_stt.assert_not_called()
        assert status == 200
        assert resp.get("content") == "ok kernel"

    def test_audio_wav_routes_to_stt(self):
        """Content-Type audio/wav → transcribe_audio invocata."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", return_value="testo audio") as mock_stt:
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        mock_stt.assert_called_once()
        assert status == 200

    def test_multipart_routes_to_stt(self):
        """Content-Type multipart/form-data → transcribe_audio invocata."""
        wav = _fake_wav()
        boundary = "testbound"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="clip.wav"\r\n'
            f"Content-Type: audio/wav\r\n\r\n"
        ).encode() + wav + f"\r\n--{boundary}--\r\n".encode()
        hdrs = {
            **_AUTH,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        }
        with patch("modules.voice.server.transcribe_audio", return_value="testo multipart") as mock_stt:
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, body, hdrs)
        mock_stt.assert_called_once()
        assert status == 200

    def test_audio_no_key_returns_503(self):
        """GROQ_API_KEY assente → 503 esplicito."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        env_without_key = {k: v for k, v in os.environ.items() if k != "GROQ_API_KEY"}
        with patch.dict(os.environ, env_without_key, clear=True):
            status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 503
        assert "GROQ_API_KEY" in resp.get("error", "")

    def test_audio_empty_body_returns_400(self):
        """Body audio vuoto → 400."""
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": "0"}
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
            status, resp = _post_raw(self.port, b"", hdrs)
        assert status == 400

    def test_groq_400_returns_400(self):
        """Groq risponde 400 → il server ritorna 400 al client."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", side_effect=GroqSTTError(400, "Groq 400: bad audio")):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 400

    def test_groq_429_returns_502(self):
        """Groq risponde 429 → il server ritorna 502."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", side_effect=GroqSTTError(429, "Groq 429: quota")):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 502

    def test_groq_500_returns_502(self):
        """Groq risponde 500 → il server ritorna 502."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", side_effect=GroqSTTError(500, "Groq 500: server error")):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 502

    def test_network_error_returns_502(self):
        """Errore di rete verso Groq → 502."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", side_effect=OSError("connection refused")):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 502

    def test_empty_transcription_returns_400(self):
        """Groq ritorna testo vuoto (silenzio) → 400."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        with patch("modules.voice.server.transcribe_audio", return_value=""):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 400

    def test_transcribed_text_passed_to_kernel(self):
        """Il testo trascritto viene passato al kernel esattamente."""
        wav = _fake_wav()
        hdrs = {**_AUTH, "Content-Type": "audio/wav", "Content-Length": str(len(wav))}
        received_prompts: List[str] = []
        original = self.kernel.run_turn
        self.kernel.run_turn = lambda p: received_prompts.append(p) or original(p)
        with patch("modules.voice.server.transcribe_audio", return_value="prompt trascritto"):
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                status, resp = _post_raw(self.port, wav, hdrs)
        assert status == 200
        assert received_prompts == ["prompt trascritto"]
