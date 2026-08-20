"""
Test suite TTS — FASE 3, Fetta 3.

Copre:
  - Routing testo vs audio nel server (TVT-route-*)
  - synthesize_speech con transport iniettato (TVT-synth-*)
  - Tutti i rami d'errore: chiave assente, testo vuoto, 4xx/5xx ElevenLabs, rete
  - Retrocompatibilità JSON invariata senza Accept header

Zero chiamate di rete reali: il transport HTTP è sempre iniettato.
Zero token LLM: il kernel è sempre un mock.
"""
from __future__ import annotations

import http.client
import io
import json
import os
import sys
import threading
from http.server import HTTPServer
from io import BytesIO
from pathlib import Path
from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.voice.server import VoiceHandler
from modules.voice.tts import DEFAULT_VOICE_ID, ElevenLabsTTSError, synthesize_speech


# ─────────────────────────────── helpers comuni ──────────────────────────────

_FAKE_MP3 = b"\xff\xfb\x90\x00" + b"\x00" * 128  # header MP3 minimo


class _MockKernel:
    def __init__(self, reply: str = "Ciao, sono Gas."):
        self._reply = reply

    def run_turn(self, prompt: str) -> Generator[dict, None, None]:
        yield {"type": "final", "content": self._reply}


def _make_server(kernel: Any, token: str) -> tuple[HTTPServer, int]:
    class _H(VoiceHandler):
        pass

    _H.kernel = kernel
    _H.token = token
    srv = HTTPServer(("127.0.0.1", 0), _H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, port


def _post_raw(port: int, body: bytes, headers: dict) -> tuple[int, bytes, str]:
    """POST /voice → (status, raw_body, content_type)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    conn.request("POST", "/voice", body=body, headers=headers)
    resp = conn.getresponse()
    raw = resp.read()
    ct = resp.getheader("Content-Type", "")
    code = resp.status
    conn.close()
    return code, raw, ct


def _post_json(port: int, payload: dict, extra_headers: dict | None = None) -> tuple[int, dict]:
    body = json.dumps(payload).encode()
    hdrs = {
        "Content-Type": "application/json",
        "Content-Length": str(len(body)),
    }
    if extra_headers:
        hdrs.update(extra_headers)
    code, raw, _ = _post_raw(port, body, hdrs)
    return code, json.loads(raw)


# ─────────────────────────────── TVT-route-* ─────────────────────────────────
# Routing: Accept header determina testo vs audio.

class TestTVTRoute:
    TOKEN = "token_tts_route"

    def setup_method(self):
        self.kernel = _MockKernel("Risposta parlata.")
        self.server, self.port = _make_server(self.kernel, self.TOKEN)

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def test_no_accept_returns_json(self, monkeypatch):
        """Senza Accept header → risposta JSON (retrocompatibilità)."""
        monkeypatch.setenv("ELEVENLABS_API_KEY", "fakekey")
        code, body = _post_json(self.port, {"prompt": "ciao"}, {"Authorization": f"Bearer {self.TOKEN}"})
        assert code == 200
        assert "content" in body

    def test_accept_audio_mpeg_routes_to_tts(self, monkeypatch):
        """Accept: audio/mpeg → chiama ElevenLabs (qui patchato)."""
        monkeypatch.setenv("ELEVENLABS_API_KEY", "fakekey")
        monkeypatch.setenv("ELEVENLABS_VOICE_ID", "voiceid123")

        with patch("modules.voice.server.synthesize_speech", return_value=_FAKE_MP3):
            body_raw = json.dumps({"prompt": "parlami"}).encode()
            hdrs = {
                "Authorization": f"Bearer {self.TOKEN}",
                "Content-Type": "application/json",
                "Content-Length": str(len(body_raw)),
                "Accept": "audio/mpeg",
            }
            code, raw, ct = _post_raw(self.port, body_raw, hdrs)

        assert code == 200
        assert "audio/mpeg" in ct
        assert raw == _FAKE_MP3

    def test_accept_audio_wildcard_routes_to_tts(self, monkeypatch):
        """Accept: audio/* → chiama ElevenLabs (qui patchato)."""
        monkeypatch.setenv("ELEVENLABS_API_KEY", "fakekey")
        monkeypatch.setenv("ELEVENLABS_VOICE_ID", "voiceid123")

        with patch("modules.voice.server.synthesize_speech", return_value=_FAKE_MP3):
            body_raw = json.dumps({"prompt": "parlami"}).encode()
            hdrs = {
                "Authorization": f"Bearer {self.TOKEN}",
                "Content-Type": "application/json",
                "Content-Length": str(len(body_raw)),
                "Accept": "audio/*",
            }
            code, raw, ct = _post_raw(self.port, body_raw, hdrs)

        assert code == 200
        assert "audio/mpeg" in ct

    def test_accept_json_returns_json(self, monkeypatch):
        """Accept: application/json → risposta JSON (non TTS)."""
        monkeypatch.setenv("ELEVENLABS_API_KEY", "fakekey")
        body_raw = json.dumps({"prompt": "ciao"}).encode()
        hdrs = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
            "Content-Length": str(len(body_raw)),
            "Accept": "application/json",
        }
        code, raw, ct = _post_raw(self.port, body_raw, hdrs)
        assert code == 200
        assert "application/json" in ct


# ─────────────────────────────── TVT-err-* ───────────────────────────────────
# Rami d'errore nel server.

class TestTVTErrors:
    TOKEN = "token_tts_err"

    def setup_method(self):
        self.kernel = _MockKernel("Risposta di test.")
        self.server, self.port = _make_server(self.kernel, self.TOKEN)

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def _post_audio_accept(self, prompt: str = "ciao") -> tuple[int, dict]:
        body_raw = json.dumps({"prompt": prompt}).encode()
        hdrs = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json",
            "Content-Length": str(len(body_raw)),
            "Accept": "audio/mpeg",
        }
        code, raw, _ = _post_raw(self.port, body_raw, hdrs)
        return code, json.loads(raw)

    def test_no_key_returns_503(self, monkeypatch):
        """ELEVENLABS_API_KEY assente → 503."""
        monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
        code, body = self._post_audio_accept()
        assert code == 503
        assert "ELEVENLABS_API_KEY" in body["error"]

    def test_empty_text_returns_json_200(self, monkeypatch):
        """Kernel risponde stringa vuota → NON chiama ElevenLabs → 200 JSON."""
        monkeypatch.setenv("ELEVENLABS_API_KEY", "fakekey")
        self.kernel._reply = ""

        called = []
        with patch("modules.voice.server.synthesize_speech", side_effect=lambda *a, **k: called.append(a)):
            code, body = self._post_audio_accept()

        assert code == 200
        assert called == [], "synthesize_speech NON deve essere chiamato su testo vuoto"

    def test_elevenlabs_error_returns_502(self, monkeypatch):
        """ElevenLabsTTSError → 502."""
        monkeypatch.setenv("ELEVENLABS_API_KEY", "fakekey")
        monkeypatch.setenv("ELEVENLABS_VOICE_ID", "vid")

        with patch(
            "modules.voice.server.synthesize_speech",
            side_effect=ElevenLabsTTSError(429, "quota esaurita"),
        ):
            code, body = self._post_audio_accept()

        assert code == 502
        assert "ElevenLabs" in body["error"]

    def test_network_error_returns_502(self, monkeypatch):
        """OSError (rete) → 502."""
        monkeypatch.setenv("ELEVENLABS_API_KEY", "fakekey")
        monkeypatch.setenv("ELEVENLABS_VOICE_ID", "vid")

        with patch(
            "modules.voice.server.synthesize_speech",
            side_effect=OSError("connection refused"),
        ):
            code, body = self._post_audio_accept()

        assert code == 502
        assert "rete" in body["error"].lower() or "ElevenLabs" in body["error"]


# ─────────────────────────────── TVT-synth-* ─────────────────────────────────
# Test unitari di synthesize_speech con transport iniettato.

class _FakeConn:
    """HTTPSConnection fake per iniettare risposte controllate."""

    def __init__(self, status: int, body: bytes, content_type: str = "audio/mpeg"):
        self._status = status
        self._body = body
        self._ct = content_type
        self.requested: list[dict] = []

    def request(self, method, path, body=None, headers=None):
        self.requested.append({"method": method, "path": path, "headers": headers or {}})

    def getresponse(self):
        resp = MagicMock()
        resp.status = self._status
        resp.read.return_value = self._body
        resp.getheader.return_value = self._ct
        return resp

    def close(self):
        pass


def test_synth_ok_returns_bytes():
    """synthesize_speech 200 → ritorna i byte audio."""
    fake = _FakeConn(200, _FAKE_MP3)
    result = synthesize_speech("ciao", "key123", "voice456", _conn_factory=lambda: fake)
    assert result == _FAKE_MP3


def test_synth_sends_correct_headers():
    """synthesize_speech invia xi-api-key e Content-Type: application/json."""
    fake = _FakeConn(200, _FAKE_MP3)
    synthesize_speech("testo", "MYKEY", "MYVOICE", _conn_factory=lambda: fake)
    assert len(fake.requested) == 1
    hdrs = fake.requested[0]["headers"]
    assert hdrs.get("xi-api-key") == "MYKEY"
    assert hdrs.get("Content-Type") == "application/json"


def test_synth_sends_correct_path():
    """Il path contiene il voice_id."""
    fake = _FakeConn(200, _FAKE_MP3)
    synthesize_speech("testo", "k", "VOICE_XYZ", _conn_factory=lambda: fake)
    assert "VOICE_XYZ" in fake.requested[0]["path"]


def test_synth_non200_raises_error():
    """ElevenLabs 422 → ElevenLabsTTSError con status=422."""
    fake = _FakeConn(422, b'{"detail": "testo troppo lungo"}')
    with pytest.raises(ElevenLabsTTSError) as exc_info:
        synthesize_speech("testo", "k", "v", _conn_factory=lambda: fake)
    assert exc_info.value.status == 422


def test_synth_401_raises_error():
    """ElevenLabs 401 (chiave non valida) → ElevenLabsTTSError status=401."""
    fake = _FakeConn(401, b'{"detail": "invalid_api_key"}')
    with pytest.raises(ElevenLabsTTSError) as exc_info:
        synthesize_speech("testo", "k", "v", _conn_factory=lambda: fake)
    assert exc_info.value.status == 401


def test_synth_oserror_propagates():
    """OSError di rete → propagata al chiamante."""
    def _broken():
        c = MagicMock()
        c.request.side_effect = OSError("timeout")
        return c

    with pytest.raises(OSError):
        synthesize_speech("testo", "k", "v", _conn_factory=_broken)


def test_synth_key_not_logged(caplog):
    """La chiave API non compare nei log."""
    import logging
    fake = _FakeConn(200, _FAKE_MP3)
    with caplog.at_level(logging.DEBUG):
        synthesize_speech("testo", "SECRETKEY_DONOT_LOG", "v", _conn_factory=lambda: fake)
    all_logs = " ".join(r.message for r in caplog.records)
    assert "SECRETKEY_DONOT_LOG" not in all_logs


def test_default_voice_id_defined():
    """DEFAULT_VOICE_ID è una stringa non vuota."""
    assert isinstance(DEFAULT_VOICE_ID, str) and len(DEFAULT_VOICE_ID) > 0


def test_server_uses_default_voice_when_env_absent(monkeypatch):
    """ELEVENLABS_VOICE_ID non settata → il server usa DEFAULT_VOICE_ID."""
    monkeypatch.delenv("ELEVENLABS_VOICE_ID", raising=False)
    monkeypatch.setenv("ELEVENLABS_API_KEY", "fakekey")
    kernel = _MockKernel("testo di prova")
    server, port = _make_server(kernel, "tokentest")

    try:
        captured_voice = []

        def _fake_synth(text, api_key, voice_id, **_kw):
            captured_voice.append(voice_id)
            return _FAKE_MP3

        with patch("modules.voice.server.synthesize_speech", side_effect=_fake_synth):
            body_raw = json.dumps({"prompt": "ciao"}).encode()
            hdrs = {
                "Authorization": "Bearer tokentest",
                "Content-Type": "application/json",
                "Content-Length": str(len(body_raw)),
                "Accept": "audio/mpeg",
            }
            _post_raw(port, body_raw, hdrs)

        assert captured_voice == [DEFAULT_VOICE_ID]
    finally:
        server.shutdown()
        server.server_close()
