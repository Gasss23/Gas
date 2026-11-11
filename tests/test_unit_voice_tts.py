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
from modules.voice.tts import DEFAULT_VOICE_ID, ElevenLabsTTSError, _cap_text, synthesize_speech


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


# ─────────────────────────── TVT-cap-* (R-tts-1) ────────────────────────────
# Test del cap deterministico GAS_TTS_MAX_CHARS su _cap_text().

_CAP = 50  # limite piccolo per i test; override via GAS_TTS_MAX_CHARS


class TestCapText:
    def test_below_limit_passes_intact(self, monkeypatch):
        """Testo ≤ limite: ritornato intatto, nessun log WARNING."""
        monkeypatch.setenv("GAS_TTS_MAX_CHARS", str(_CAP))
        text = "Ciao. Come stai?"  # 16 char
        assert _cap_text(text) == text

    def test_above_limit_truncates_at_sentence_boundary(self, monkeypatch, caplog):
        """Testo > limite con frase: troncato all'ultimo '.' ≤ limite."""
        monkeypatch.setenv("GAS_TTS_MAX_CHARS", str(_CAP))
        import logging

        # "Frase uno. " = 11 char, "Frase due che è lunga lunga lunga lunga lunga." = 46 char
        # Totale 57 char > 50 — l'ultimo '.' ≤ 50 è a posizione 10 (fine "Frase uno.")
        text = "Frase uno. Frase due che e lunga lunga lunga lunga."
        assert len(text) > _CAP
        with caplog.at_level(logging.WARNING):
            result = _cap_text(text)
        assert len(result) <= _CAP
        assert result.endswith(".")
        # Deve contenere la prima frase completa
        assert result == "Frase uno."
        assert "TTS text cap" in caplog.text

    def test_above_limit_no_punctuation_truncates_at_space(self, monkeypatch, caplog):
        """Testo > limite senza punteggiatura: troncato all'ultimo spazio ≤ limite."""
        monkeypatch.setenv("GAS_TTS_MAX_CHARS", str(_CAP))
        import logging

        # 50 char esatti prima dello spazio, poi altra parola
        text = "parola " * 7 + "extraword"  # "parola " × 7 = 49 char, poi "extraword"
        assert len(text) > _CAP
        with caplog.at_level(logging.WARNING):
            result = _cap_text(text)
        assert len(result) <= _CAP
        assert not result.endswith("extraword")
        assert "TTS text cap" in caplog.text

    def test_above_limit_no_boundary_hard_cuts(self, monkeypatch, caplog):
        """Testo > limite senza spazi né punteggiatura: hard-cut esatto al limite."""
        monkeypatch.setenv("GAS_TTS_MAX_CHARS", str(_CAP))
        import logging

        text = "x" * (_CAP + 20)
        with caplog.at_level(logging.WARNING):
            result = _cap_text(text)
        assert len(result) == _CAP
        assert "TTS text cap" in caplog.text

    def test_env_override_respected(self, monkeypatch):
        """GAS_TTS_MAX_CHARS=10 limita a 10 char."""
        monkeypatch.setenv("GAS_TTS_MAX_CHARS", "10")
        text = "Parola lunga che supera dieci caratteri."
        result = _cap_text(text)
        assert len(result) <= 10

    def test_no_warning_when_below_limit(self, monkeypatch, caplog):
        """Nessun WARNING loggato se il testo è già ≤ limite."""
        monkeypatch.setenv("GAS_TTS_MAX_CHARS", str(_CAP))
        import logging

        text = "Ciao."
        with caplog.at_level(logging.WARNING):
            _cap_text(text)
        assert "TTS text cap" not in caplog.text

    def test_synthesize_never_sends_over_limit(self, monkeypatch):
        """synthesize_speech non invia mai più di GAS_TTS_MAX_CHARS char a ElevenLabs."""
        monkeypatch.setenv("GAS_TTS_MAX_CHARS", str(_CAP))
        long_text = "Parola " * 100  # >> 50 char
        captured: list[str] = []

        class _CapturingConn:
            def request(self, method, path, body=None, headers=None):
                payload = json.loads(body)
                captured.append(payload["text"])

            def getresponse(self):
                resp = MagicMock()
                resp.status = 200
                resp.read.return_value = _FAKE_MP3
                return resp

            def close(self):
                pass

        synthesize_speech(long_text, "k", "v", _conn_factory=_CapturingConn)
        assert len(captured) == 1
        assert len(captured[0]) <= _CAP


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


def test_audit_b3_risposta_rotta_diventa_oserror():
    """B3: IncompleteRead di ElevenLabs → OSError, preso dai rami di sintesi del server."""
    import http.client

    class _Rotta(_FakeConn):
        def getresponse(self):
            resp = MagicMock()
            resp.read.side_effect = http.client.IncompleteRead(b"x", 10)
            return resp
    with pytest.raises(OSError, match="IncompleteRead"):
        synthesize_speech("ciao", "k", "v", _conn_factory=lambda: _Rotta(200, b""))


def test_audit_b3_altre_funzioni_tts():
    """R-752-2: anche elenco voci, libreria e aggiunta di una voce trasformano una risposta
    rotta in OSError (il server prende ElevenLabsTTSError e OSError)."""
    import http.client
    from modules.voice.tts import add_shared_voice, list_shared_voices, list_voices

    class _Rotta(_FakeConn):
        def getresponse(self):
            raise http.client.IncompleteRead(b"x", 10)
    fab = lambda: _Rotta(200, b"")  # noqa: E731
    for chiamata in (lambda: list_voices("k", _conn_factory=fab),
                     lambda: list_shared_voices("k", _conn_factory=fab),
                     lambda: add_shared_voice("k", "owner", "v", "nome", _conn_factory=fab)):
        with pytest.raises(OSError, match="IncompleteRead"):
            chiamata()


# ── Velocità (11 nov): connessione HTTPS verso ElevenLabs tenuta aperta e riusata ──

class _ConnViva:
    """HTTPSConnection finta che conta richieste e può fallire alla richiesta n."""
    create: list = []

    def __init__(self, host, timeout=None):
        self.host, self.timeout, self.sock = host, timeout, None
        self.richieste = 0
        self.chiusa = False
        self.fallisci = None      # eccezione da alzare alla prossima request
        self.will_close = False
        type(self).create.append(self)

    def request(self, method, path, body=None, headers=None):
        if self.fallisci is not None:
            exc, self.fallisci = self.fallisci, None
            raise exc
        self.richieste += 1

    def getresponse(self):
        resp = MagicMock()
        resp.status = 200
        resp.read.return_value = b"MP3"
        resp.will_close = self.will_close
        return resp

    def close(self):
        self.chiusa = True


@pytest.fixture
def conn_viva(monkeypatch):
    import modules.voice.tts as tts_mod
    _ConnViva.create = []
    tts_mod._chiudi_conn_locale()
    monkeypatch.delenv("GAS_TTS_KEEPALIVE", raising=False)
    monkeypatch.setattr(tts_mod.http.client, "HTTPSConnection", _ConnViva)
    yield tts_mod
    tts_mod._chiudi_conn_locale()


def test_keepalive_riusa_la_connessione(conn_viva):
    for frase in ("Prima frase.", "Seconda frase.", "Terza."):
        assert synthesize_speech(frase, "k", "v") == b"MP3"
    assert len(_ConnViva.create) == 1 and _ConnViva.create[0].richieste == 3


def test_keepalive_riprova_una_volta_se_il_server_ha_chiuso(conn_viva):
    import http.client
    synthesize_speech("Uno.", "k", "v")
    _ConnViva.create[0].fallisci = http.client.RemoteDisconnected("chiusa")
    assert synthesize_speech("Due.", "k", "v") == b"MP3"
    assert len(_ConnViva.create) == 2 and _ConnViva.create[0].chiusa
    assert _ConnViva.create[1].richieste == 1


def test_keepalive_connessione_nuova_che_fallisce_non_riprova(conn_viva):
    """Su una connessione appena aperta l'errore risale come OSError, senza un secondo
    tentativo (niente doppio addebito di caratteri)."""
    import http.client

    class _Rotta(_ConnViva):
        def request(self, *a, **kw):
            raise http.client.RemoteDisconnected("giù")
    conn_viva.http.client.HTTPSConnection = _Rotta
    with pytest.raises(OSError, match="RemoteDisconnected"):
        synthesize_speech("Uno.", "k", "v")
    assert len(_ConnViva.create) == 1


def test_keepalive_errore_http_e_will_close(conn_viva):
    """«Connection: close» del server fa chiudere la connessione (il 4xx è in
    test_keepalive_status_non_200)."""
    synthesize_speech("Uno.", "k", "v")
    _ConnViva.create[0].will_close = True
    synthesize_speech("Due.", "k", "v")
    assert _ConnViva.create[0].chiusa
    synthesize_speech("Tre.", "k", "v")
    assert len(_ConnViva.create) == 2


def test_keepalive_spento(conn_viva, monkeypatch):
    monkeypatch.setenv("GAS_TTS_KEEPALIVE", "0")
    synthesize_speech("Uno.", "k", "v")
    synthesize_speech("Due.", "k", "v")
    assert len(_ConnViva.create) == 2 and all(c.chiusa for c in _ConnViva.create)


def test_keepalive_una_connessione_per_thread(conn_viva):
    import threading
    synthesize_speech("Uno.", "k", "v")
    t = threading.Thread(target=lambda: synthesize_speech("Altro thread.", "k", "v"))
    t.start()
    t.join()
    assert len(_ConnViva.create) == 2


def test_keepalive_status_non_200(conn_viva):
    class _Rifiuto(_ConnViva):
        def getresponse(self):
            resp = MagicMock()
            resp.status = 401
            resp.read.return_value = b'{"detail":"no"}'
            resp.will_close = False
            return resp
    conn_viva.http.client.HTTPSConnection = _Rifiuto
    with pytest.raises(ElevenLabsTTSError) as e:
        synthesize_speech("Uno.", "k", "v")
    assert e.value.status == 401



def test_keepalive_errore_durante_la_lettura_non_riprova(conn_viva):
    """R-765-1-M2: se la connessione salta mentre arriva l'audio (stato 200 già ricevuto)
    NON si rifà la richiesta: ElevenLabs l'avrebbe già fatta pagare."""
    class _Taglia(_ConnViva):
        def getresponse(self):
            resp = MagicMock()
            resp.status = 200
            resp.read.side_effect = ConnectionResetError("tagliata")
            resp.will_close = False
            return resp
    synthesize_speech("Uno.", "k", "v")          # connessione aperta e riusabile
    conn_viva.http.client.HTTPSConnection = _Taglia
    _ConnViva.create[0].getresponse = _Taglia.getresponse.__get__(_ConnViva.create[0])
    with pytest.raises(OSError, match="ConnectionResetError"):
        synthesize_speech("Due.", "k", "v")
    assert _ConnViva.create[0].richieste == 2 and len(_ConnViva.create) == 1
    assert _ConnViva.create[0].chiusa


def test_keepalive_connessione_ferma_da_troppo_si_butta(conn_viva, monkeypatch):
    """R-765-2-M2: dopo più di _KEEPALIVE_INATTIVA_MAX_S senza uso si apre una nuova."""
    ora = [1000.0]
    monkeypatch.setattr(conn_viva.time, "monotonic", lambda: ora[0])
    synthesize_speech("Uno.", "k", "v")
    ora[0] += 5
    synthesize_speech("Due.", "k", "v")
    assert len(_ConnViva.create) == 1
    ora[0] += conn_viva._KEEPALIVE_INATTIVA_MAX_S + 1
    synthesize_speech("Tre.", "k", "v")
    assert len(_ConnViva.create) == 2 and _ConnViva.create[0].chiusa


def test_keepalive_timeout_aggiornato_sul_socket(conn_viva, monkeypatch):
    """R-765-3-M2: il timeout di ogni chiamata (es. 5 s della conferma) vale anche sul
    socket della connessione riusata."""
    monkeypatch.setattr(conn_viva, "_conn_caduta", lambda conn: False)  # socket finto
    synthesize_speech("Uno.", "k", "v", timeout=30)
    conn = _ConnViva.create[0]
    conn.sock = MagicMock()
    synthesize_speech("Due.", "k", "v", timeout=5)
    assert conn.timeout == 5
    conn.sock.settimeout.assert_called_with(5)


def test_keepalive_eccezione_qualsiasi_chiude(conn_viva):
    """R-765-3-M2: un'eccezione non prevista chiude e scarta la connessione."""
    synthesize_speech("Uno.", "k", "v")
    _ConnViva.create[0].fallisci = KeyboardInterrupt()
    with pytest.raises(KeyboardInterrupt):
        synthesize_speech("Due.", "k", "v")
    assert _ConnViva.create[0].chiusa
    synthesize_speech("Tre.", "k", "v")
    assert len(_ConnViva.create) == 2



def test_keepalive_errore_dopo_l_invio_non_riprova(conn_viva):
    """V-1 bot #372: se la connessione riusata si chiude DOPO l'invio (in getresponse) non
    si rifà la richiesta: ElevenLabs potrebbe averla già fatta pagare."""
    import http.client
    synthesize_speech("Uno.", "k", "v")
    conn = _ConnViva.create[0]

    def _chiusa_dopo_invio():
        raise http.client.RemoteDisconnected("chiusa dopo l'invio")
    conn.getresponse = _chiusa_dopo_invio
    with pytest.raises(OSError, match="RemoteDisconnected"):
        synthesize_speech("Due.", "k", "v")
    assert conn.richieste == 2 and len(_ConnViva.create) == 1 and conn.chiusa


def test_keepalive_connessione_chiusa_dal_server_non_si_riusa(conn_viva):
    """R-770-1-M2: se a riposo il socket è leggibile (il server ha chiuso), si apre una
    connessione nuova PRIMA di inviare, senza consumare il nuovo tentativo."""
    import socket
    a, b = socket.socketpair()
    try:
        synthesize_speech("Una.", "k", "v")
        prima = _ConnViva.create[0]
        prima.sock = a
        b.close()  # il «server» chiude: a diventa leggibile (EOF)
        synthesize_speech("Due.", "k", "v")
        assert len(_ConnViva.create) == 2
        assert prima.chiusa and prima.richieste == 1
        assert _ConnViva.create[1].richieste == 1
    finally:
        a.close()


def test_keepalive_connessione_viva_a_riposo_si_riusa(conn_viva):
    """Socket aperto e senza dati da leggere: la connessione si riusa."""
    import socket
    a, b = socket.socketpair()
    try:
        synthesize_speech("Una.", "k", "v")
        _ConnViva.create[0].sock = a
        synthesize_speech("Due.", "k", "v")
        assert len(_ConnViva.create) == 1
        assert _ConnViva.create[0].richieste == 2
    finally:
        a.close()
        b.close()
