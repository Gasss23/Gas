"""
Test suite per modules/voice/server.py — FASE 3, Fetta 1.

Zero token LLM: il kernel è sempre un mock iniettato.
Gira pytest standalone: python -m pytest tests/test_unit_voice_server.py -v
"""
from __future__ import annotations

import http.client
import json
import logging
import os
import sys
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Generator, List

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.voice.server import VoiceHandler, _token_ok, run_server


# ────────────────────────────────── helpers ──────────────────────────────────

class _MockKernel:
    """Kernel finto: emette eventi controllati, conta le istanziazioni."""

    instances: List["_MockKernel"] = []

    def __init__(self, events: List[dict] | None = None, raise_exc: Exception | None = None):
        _MockKernel.instances.append(self)
        self._events = events or [{"type": "final", "content": "risposta di test"}]
        self._raise = raise_exc

    def run_turn(self, prompt: str) -> Generator[dict, None, None]:
        if self._raise is not None:
            raise self._raise
        yield from self._events


def _make_server(kernel: Any, token: str, port: int = 0) -> tuple[HTTPServer, int]:
    """Crea un HTTPServer su porta casuale (port=0) con kernel e token iniettati."""

    class _Handler(VoiceHandler):
        pass

    _Handler.kernel = kernel
    _Handler.token = token

    server = HTTPServer(("127.0.0.1", port), _Handler)
    actual_port = server.server_address[1]
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server, actual_port


def _post(port: int, body: dict | None, headers: dict | None = None) -> tuple[int, dict]:
    """Esegue una POST /voice e ritorna (status_code, json_body)."""
    url = f"http://127.0.0.1:{port}/voice"
    raw = json.dumps(body or {}).encode("utf-8")
    hdrs = {"Content-Type": "application/json", "Content-Length": str(len(raw))}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=raw, headers=hdrs, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


# ─────────────────────────────────── TV1 ─────────────────────────────────────
# TV1: Avvio senza GAS_VOICE_TOKEN → run_server ritorna 1, non parte.

def test_tv1_no_token_refuses_start(monkeypatch, capsys):
    monkeypatch.delenv("GAS_VOICE_TOKEN", raising=False)
    code = run_server(root_dir="/tmp")
    assert code == 1, "run_server deve ritornare 1 se GAS_VOICE_TOKEN manca"
    captured = capsys.readouterr()
    assert "GAS_VOICE_TOKEN" in captured.out


# ─────────────────────────────────── TV2 ─────────────────────────────────────
# TV2: Richiesta senza header Authorization → 401, kernel NON invocato.

class TestTV2NoAuth:
    def setup_method(self):
        _MockKernel.instances.clear()
        self.kernel = _MockKernel()
        self.server, self.port = _make_server(self.kernel, token="corretto123")

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def test_no_auth_returns_401(self):
        status, body = _post(self.port, {"prompt": "ciao"}, headers={})
        assert status == 401
        assert "error" in body

    def test_no_auth_kernel_not_invoked(self, monkeypatch):
        # Sostituiamo run_turn con un tracciante — non deve mai essere chiamato.
        called = []
        self.kernel.run_turn = lambda p: called.append(p) or iter([])
        _post(self.port, {"prompt": "ciao"}, headers={})
        assert called == [], "run_turn NON deve essere invocato su richiesta non autenticata"


# ─────────────────────────────────── TV3 ─────────────────────────────────────
# TV3: Token errato → 401 + log del tentativo; il token ricevuto NON deve comparire nel log.

class TestTV3WrongToken:
    TOKEN_CORRETTO = "tokenvalido_abc123"
    TOKEN_ERRATO = "tokensbagliato_xyz999"

    def setup_method(self):
        _MockKernel.instances.clear()
        self.kernel = _MockKernel()
        self.server, self.port = _make_server(self.kernel, token=self.TOKEN_CORRETTO)

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def test_wrong_token_returns_401(self):
        hdrs = {"Authorization": f"Bearer {self.TOKEN_ERRATO}"}
        status, body = _post(self.port, {"prompt": "ciao"}, headers=hdrs)
        assert status == 401

    def test_wrong_token_logged_without_secret(self, caplog):
        with caplog.at_level(logging.WARNING, logger="modules.voice.server"):
            hdrs = {"Authorization": f"Bearer {self.TOKEN_ERRATO}"}
            _post(self.port, {"prompt": "ciao"}, headers=hdrs)

        # Deve esserci almeno un log di AUTH FAIL
        auth_fails = [r for r in caplog.records if "AUTH FAIL" in r.message]
        assert auth_fails, "Deve essere loggato almeno un AUTH FAIL"

        # Il token ricevuto NON deve comparire in nessun log
        all_log_text = " ".join(r.message for r in caplog.records)
        assert self.TOKEN_ERRATO not in all_log_text, (
            f"Il token errato '{self.TOKEN_ERRATO}' NON deve comparire nei log"
        )
        # Nemmeno il token corretto deve comparire
        assert self.TOKEN_CORRETTO not in all_log_text


# ─────────────────────────────────── TV4 ─────────────────────────────────────
# TV4: Token corretto → 200 + "content" dell'evento "final".

class TestTV4CorrectToken:
    TOKEN = "token_valido_tv4_abc"

    def setup_method(self):
        _MockKernel.instances.clear()
        self.kernel = _MockKernel(events=[
            {"type": "tool_res", "output": "dati intermedi"},
            {"type": "final", "content": "Risposta definitiva di Gas"},
        ])
        self.server, self.port = _make_server(self.kernel, token=self.TOKEN)

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def test_correct_token_200(self):
        hdrs = {"Authorization": f"Bearer {self.TOKEN}"}
        status, body = _post(self.port, {"prompt": "dimmi qualcosa"}, headers=hdrs)
        assert status == 200
        assert body.get("content") == "Risposta definitiva di Gas"

    def test_tool_res_events_silent(self):
        """Gli eventi tool_res non devono comparire nella risposta HTTP."""
        hdrs = {"Authorization": f"Bearer {self.TOKEN}"}
        status, body = _post(self.port, {"prompt": "dimmi qualcosa"}, headers=hdrs)
        assert "dati intermedi" not in json.dumps(body)


# ─────────────────────────────────── TV5 ─────────────────────────────────────
# TV5: Eccezione in run_turn → 500 pulito, server ancora vivo.

class TestTV5KernelException:
    TOKEN = "token_tv5"

    def setup_method(self):
        _MockKernel.instances.clear()
        self.exc_kernel = _MockKernel(raise_exc=RuntimeError("crash kernel simulato"))
        self.ok_kernel = _MockKernel(events=[{"type": "final", "content": "ok dopo crash"}])
        # Il server usa exc_kernel; dopo il crash lo sostituiremo con ok_kernel.
        self.handler_class = None

        class _Handler(VoiceHandler):
            pass

        _Handler.token = self.TOKEN
        _Handler.kernel = self.exc_kernel
        self.handler_class = _Handler

        self.server = HTTPServer(("127.0.0.1", 0), _Handler)
        self.port = self.server.server_address[1]
        t = threading.Thread(target=self.server.serve_forever, daemon=True)
        t.start()

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def test_exception_returns_500(self):
        hdrs = {"Authorization": f"Bearer {self.TOKEN}"}
        status, body = _post(self.port, {"prompt": "crash!"}, headers=hdrs)
        assert status == 500
        assert "error" in body

    def test_server_still_alive_after_exception(self):
        """Dopo un crash di run_turn il server deve rispondere ancora a richieste valide."""
        hdrs = {"Authorization": f"Bearer {self.TOKEN}"}
        # Prima richiesta: crash
        _post(self.port, {"prompt": "crash!"}, headers=hdrs)
        # Sostituiamo kernel con uno funzionante
        self.handler_class.kernel = self.ok_kernel
        # Seconda richiesta: deve rispondere 200
        status, body = _post(self.port, {"prompt": "sei ancora vivo?"}, headers=hdrs)
        assert status == 200
        assert body.get("content") == "ok dopo crash"


# ─────────────────────────────────── TV6 ─────────────────────────────────────
# TV6: Il kernel è istanziato UNA VOLTA, non per richiesta.
# Questo test verifica la proprietà a livello di run_server(). Siccome run_server()
# importa GasKernel e lo blocca su serve_forever(), lo testiamo in modo indiretto:
# il mock_kernel iniettato nella classe handler deve essere LO STESSO oggetto dopo
# N richieste successive (identità Python, non solo uguaglianza).

class TestTV6KernelSingleInstance:
    TOKEN = "token_tv6"

    def setup_method(self):
        _MockKernel.instances.clear()
        self.kernel = _MockKernel()
        self.server, self.port = _make_server(self.kernel, token=self.TOKEN)

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def test_kernel_same_object_across_requests(self):
        """Il kernel non viene re-istanziato tra richieste: è lo stesso oggetto."""
        hdrs = {"Authorization": f"Bearer {self.TOKEN}"}
        kernel_ids: List[int] = []

        original_run_turn = self.kernel.run_turn

        def patched_run_turn(prompt: str):
            kernel_ids.append(id(self.kernel))
            return original_run_turn(prompt)

        self.kernel.run_turn = patched_run_turn

        for _ in range(3):
            _post(self.port, {"prompt": "ping"}, headers=hdrs)

        assert len(kernel_ids) == 3, "run_turn deve essere chiamato una volta per richiesta"
        assert len(set(kernel_ids)) == 1, "Il kernel deve essere lo stesso oggetto per tutte le richieste"


# ─────────────────────────────────── TV-extra ────────────────────────────────
# Test aggiuntivi di robustezza.

class TestTVExtra:
    TOKEN = "token_extra"

    def setup_method(self):
        self.kernel = _MockKernel()
        self.server, self.port = _make_server(self.kernel, token=self.TOKEN)

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def test_missing_prompt_returns_400(self):
        hdrs = {"Authorization": f"Bearer {self.TOKEN}"}
        status, body = _post(self.port, {}, headers=hdrs)
        assert status == 400

    def test_empty_prompt_returns_400(self):
        hdrs = {"Authorization": f"Bearer {self.TOKEN}"}
        status, body = _post(self.port, {"prompt": "   "}, headers=hdrs)
        assert status == 400

    def test_error_event_from_kernel_returns_500(self):
        self.kernel._events = [{"type": "error", "content": "Pipeline esausta."}]
        hdrs = {"Authorization": f"Bearer {self.TOKEN}"}
        status, body = _post(self.port, {"prompt": "test error"}, headers=hdrs)
        assert status == 500
        assert "Pipeline esausta" in body.get("error", "")

    def test_get_not_allowed(self):
        url = f"http://127.0.0.1:{self.port}/voice"
        req = urllib.request.Request(url, method="GET")
        try:
            urllib.request.urlopen(req, timeout=5)
            assert False, "GET deve ritornare 4xx"
        except urllib.error.HTTPError as e:
            assert e.code in (404, 405)

    def test_invalid_content_length_returns_400(self):
        """R-voice-3: Content-Length non numerico (es. 'abc') → 400.

        Usa http.client per controllo diretto degli header: urllib normalizza
        Content-Length internamente e potrebbe non trasmettere 'abc' al server.
        """
        body = b'{"prompt": "ciao"}'
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request(
            "POST", "/voice",
            body=body,
            headers={
                "Authorization": f"Bearer {self.TOKEN}",
                "Content-Type": "application/json",
                "Content-Length": "abc",
            },
        )
        resp = conn.getresponse()
        status = resp.status
        resp_body = json.loads(resp.read())
        conn.close()
        assert status == 400, f"Atteso 400, got {status}; body={resp_body}"
        assert "Content-Length" in resp_body.get("error", ""), (
            f"Messaggio errore deve citare 'Content-Length': {resp_body!r}"
        )


# ─────────────────────────────────── unit _token_ok ──────────────────────────

def test_token_ok_matching():
    assert _token_ok("abc123", "abc123") is True

def test_token_ok_mismatch():
    assert _token_ok("abc123", "xyz999") is False

def test_token_ok_empty_received():
    assert _token_ok("", "abc123") is False

def test_token_ok_empty_expected():
    assert _token_ok("abc123", "") is False
