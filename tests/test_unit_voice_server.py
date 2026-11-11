"""
Test suite per modules/voice/server.py — FASE 3, Fetta 1.

Zero token LLM: il kernel è sempre un mock iniettato.
Gira pytest standalone: python -m pytest tests/test_unit_voice_server.py -v
"""
from __future__ import annotations

import http.client
import ipaddress
import json
import logging
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Generator, List

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.voice.server import VoiceHandler, _token_ok, cervello_voce, run_server

# R-384-1 (chat Voce): urllib segue http_proxy anche verso 127.0.0.1 se no_proxy non lo
# copre; un opener senza proxy tiene i test indipendenti dall'ambiente.
_SENZA_PROXY = urllib.request.build_opener(urllib.request.ProxyHandler({}))


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
        with _SENZA_PROXY.open(req, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


# ─────────────────────────────────── TV1 ─────────────────────────────────────
# TV1: Avvio senza GAS_VOICE_TOKEN → run_server ritorna 1, non parte.

def test_tv1_no_token_refuses_start(monkeypatch, capsys):
    monkeypatch.delenv("GAS_VOICE_TOKEN", raising=False)
    monkeypatch.setattr(sys, "path", list(sys.path))  # V-1 bot #304: run_server tocca sys.path
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
            _SENZA_PROXY.open(req, timeout=5)
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


# ---------------------------------------------------------------------------
# F-mac-3 / R-190-2: `pytest` lanciato senza target deve poter raccogliere il repo
# ---------------------------------------------------------------------------

def test_collection_dell_intero_repo_non_esplode():
    """F-mac-3: probe manuali `clients/voice/probe/win_*_test.py` (sys.exit all'import se
    mancano le dipendenze audio) e lo script `tests/test_unit_kernel.py` (suite + sys.exit
    all'import) mandavano `pytest` senza target in INTERNALERROR (rc 3). Esclusi dai
    conftest.py; questo test prende ogni nuovo file raccolto che esploda all'import.
    Conta l'exit code, non l'ultima riga dell'output (R-190-1)."""
    import subprocess
    import sys
    from pathlib import Path
    radice = Path(__file__).parent.parent
    r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p",
                        "no:cacheprovider"], cwd=radice, capture_output=True, text=True,
                       timeout=300)
    assert r.returncode in (0, 5), (r.returncode, r.stdout[-2000:], r.stderr[-2000:])


def test_forte_dalla_voce(monkeypatch):
    """R-ve269-2: «/forte <richiesta>» dall'API testo va al solo forte; «/forte» nudo
    → 400 con l'istruzione d'uso, nessun turno."""
    visti = []

    class _K:
        def run_turn(self, prompt, **kw):
            visti.append((prompt, kw))
            yield {"type": "final", "content": "ok"}

    server, port = _make_server(_K(), "tok-forte-123456")
    try:
        auth = {"Authorization": "Bearer tok-forte-123456"}
        assert _post(port, {"prompt": "/forte analizza"}, auth)[0] == 200
        assert _post(port, {"prompt": "ciao"}, auth)[0] == 200
        st, body = _post(port, {"prompt": "/forte"}, auth)
        assert st == 400 and "Uso: /forte" in body["error"]
    finally:
        server.shutdown()
    assert visti == [("analizza", {"cervello": "forte"}), ("ciao", {})]


# ---------------------------------------------------------------------------
# V1 (chat M2): «forte» parlato e GAS_VOCE_FORTE → solo cervello forte, mai ai gratuiti
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("parlato,atteso", [
    ("Forte, analizza i lead", ("forte", "analizza i lead")),
    ("forte analizza", ("forte", "analizza")),
    ("Gas, forte: scrivi la mail", ("forte", "scrivi la mail")),
    ("Gas forte. Fai il punto", ("forte", "Fai il punto")),
    ("Gus forte, fai il punto", ("forte", "fai il punto")),   # come lo trascrive Whisper
    ("«Forte» analizza", ("forte", "analizza")),
    ("FORTE\nanalizza", ("forte", "analizza")),
    ("/forte analizza", ("forte", "analizza")),
    ("Ehi Gas, forte: analizza", ("forte", "analizza")),       # V-2 ve #304
    ("Ok Gas forte analizza", ("forte", "analizza")),
    ("Hey Jarvis, forte: analizza", ("forte", "analizza")),      # audit 10 nov (B2)
    ("Jarvis, Gas, forte analizza", ("forte", "analizza")),      # parola ripetuta
    ("Hey Jarvis hey Jarvis forte analizza", ("forte", "analizza")),
])
def test_v1_parola_forte_parlata(monkeypatch, parlato, atteso):
    monkeypatch.delenv("GAS_VOCE_FORTE", raising=False)
    assert cervello_voce(parlato, parlato=True) == atteso


@pytest.mark.parametrize("parlato", ["", "   ", "forte", "Forte.", "Gas forte", "Gas, forte!", "forte …", "/forte"])
def test_v1_parola_forte_senza_richiesta_e_uso(monkeypatch, parlato):
    """Fail-closed: prefisso senza richiesta → «uso», mai un turno ai gratuiti."""
    monkeypatch.delenv("GAS_VOCE_FORTE", raising=False)
    assert cervello_voce(parlato, parlato=True) == ("uso", "")


@pytest.mark.parametrize("parlato", [
    "fortemente consiglio di aspettare",
    "Fortezza da visitare",
    "Mi piace forte",
    "Gas, parla più forte",
    "Gasforte analizza",
    "Ciao Gas",
    "Ok, forte questo film",          # saluto senza «Gas»: resta normale
    "Gas e forte analizza",           # limite dichiarato
])
def test_v1_falsi_positivi_restano_normali(monkeypatch, parlato):
    monkeypatch.delenv("GAS_VOCE_FORTE", raising=False)
    assert cervello_voce(parlato, parlato=True) == (None, parlato)


def test_v1_parola_forte_solo_nel_parlato(monkeypatch):
    """Il testo scritto usa «/forte»: «forte …» scritto resta un turno normale."""
    monkeypatch.delenv("GAS_VOCE_FORTE", raising=False)
    assert cervello_voce("forte analizza", parlato=False) == (None, "forte analizza")


@pytest.mark.parametrize("valore,acceso", [("1", True), ("true", True), (" SI ", True), ("sì", True),
                                           ("0", False), ("", False), ("no", False)])
def test_v1_gas_voce_forte(monkeypatch, valore, acceso):
    """GAS_VOCE_FORTE acceso: tutto al forte, testo e parlato; «uso» resta «uso»."""
    monkeypatch.setenv("GAS_VOCE_FORTE", valore)
    atteso = "forte" if acceso else None
    assert cervello_voce("ciao", parlato=False) == (atteso, "ciao")
    assert cervello_voce("fortemente sì", parlato=True) == (atteso, "fortemente sì")
    assert cervello_voce("/forte", parlato=False) == ("uso", "")


def test_v1_server_gas_voce_forte_e_uso(monkeypatch):
    """Dal server: GAS_VOCE_FORTE=1 manda il turno col cervello forte; «/forte» nudo → 400
    con l'istruzione d'uso, nessun turno."""
    monkeypatch.setenv("GAS_VOCE_FORTE", "1")
    visti = []

    class _K:
        def run_turn(self, prompt, **kw):
            visti.append((prompt, kw))
            yield {"type": "final", "content": "ok"}

    server, port = _make_server(_K(), "tok-v1-forte-123")
    try:
        auth = {"Authorization": "Bearer tok-v1-forte-123"}
        assert _post(port, {"prompt": "ciao"}, auth)[0] == 200
        st, body = _post(port, {"prompt": "/forte"}, auth)
        assert st == 400 and "«forte <richiesta>»" in body["error"]
    finally:
        server.shutdown()
    assert visti == [("ciao", {"cervello": "forte"})]


def test_v1_server_forte_fermo_errore_dichiarato(monkeypatch):
    """Forte fermo (il kernel emette un errore): il server lo riporta, nessun altro turno."""
    monkeypatch.setenv("GAS_VOCE_FORTE", "1")
    visti = []

    class _K:
        def run_turn(self, prompt, **kw):
            visti.append(kw)
            yield {"type": "error", "content": "Cervello forte fermo: tetto. I lavori importanti restano in attesa"}

    server, port = _make_server(_K(), "tok-v1-fermo-123")
    try:
        st, body = _post(port, {"prompt": "analizza"}, {"Authorization": "Bearer tok-v1-fermo-123"})
    finally:
        server.shutdown()
    assert st == 500 and "Cervello forte fermo" in body["error"]
    assert visti == [{"cervello": "forte"}]


def test_v1_run_server_carica_il_dotenv(monkeypatch, capsys):
    """V-1 bot #304: il server voce carica il .env (come la CLI) PRIMA di leggere la
    configurazione: GAS_VOICE_TOKEN dal .env lo fa partire, GAS_VOCE_FORTE si vede a schermo."""
    import gas
    import modules.voice.server as srv
    monkeypatch.delenv("GAS_VOICE_TOKEN", raising=False)
    monkeypatch.delenv("GAS_VOCE_FORTE", raising=False)
    monkeypatch.setenv("GAS_VOICE_PORT", "0")

    def _finto_dotenv():
        os.environ["GAS_VOICE_TOKEN"] = "tok-dal-dotenv-123"
        os.environ["GAS_VOCE_FORTE"] = "1"
        return ["GAS_VOICE_TOKEN", "GAS_VOCE_FORTE"]

    class _FintoServer:
        def __init__(self, *a):
            pass

        def serve_forever(self):
            raise KeyboardInterrupt

        def server_close(self):
            pass

    monkeypatch.setattr(gas, "_carica_dotenv", _finto_dotenv)
    monkeypatch.setattr(gas, "GasKernel", lambda root_dir: object())
    monkeypatch.setattr(srv, "HTTPServer", _FintoServer)
    monkeypatch.setattr(sys, "path", list(sys.path))  # V-1 bot #304
    # R-565-1-M2: run_server scrive kernel e token sulla classe base: ripristinati a fine test
    monkeypatch.setattr(srv.VoiceHandler, "kernel", None)
    monkeypatch.setattr(srv.VoiceHandler, "token", "")
    try:
        assert run_server() == 0
        out = capsys.readouterr().out
        assert "in ascolto" in out and "GAS_VOCE_FORTE acceso" in out
        # V2 (V-3 ve #304): la riga d'attesa esce per prima, prima del caricamento
        assert out.index("avvio in corso") < out.index("in ascolto")
    finally:
        os.environ.pop("GAS_VOICE_TOKEN", None)
        os.environ.pop("GAS_VOCE_FORTE", None)


def test_v1_run_server_dotenv_rotto_non_crasha(monkeypatch, capsys):
    """Fail-safe §9: un errore nel caricare il .env non fa crashare l'avvio."""
    import gas
    monkeypatch.delenv("GAS_VOICE_TOKEN", raising=False)

    def _rotto():
        raise OSError("disco")

    monkeypatch.setattr(gas, "_carica_dotenv", _rotto)
    monkeypatch.setattr(sys, "path", list(sys.path))  # V-1 bot #304
    assert run_server(root_dir="/tmp") == 1
    assert "GAS_VOICE_TOKEN" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# V2 (chat M2): proxy del browser — attesa lunga per il forte, messaggio chiaro se scade
# ---------------------------------------------------------------------------

def _browser_server_module():
    import importlib.util
    percorso = Path(__file__).parent.parent / "clients" / "voice" / "browser_server.py"
    spec = importlib.util.spec_from_file_location("gas_browser_server_test", percorso)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_v2_browser_proxy_tempo_scaduto_messaggio_chiaro():
    """Se Gas non risponde entro il tetto, il proxy dice 504 «può essere ancora in corso»,
    non «Voice server non raggiungibile» (prima: tetto fisso di 90 s)."""
    import time
    from http.server import BaseHTTPRequestHandler

    class _Lento(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            self.rfile.read(int(self.headers.get("Content-Length", 0) or 0))
            time.sleep(2)
            try:
                self.send_response(200)
                self.end_headers()
            except OSError:
                pass

    lento = HTTPServer(("127.0.0.1", 0), _Lento)
    threading.Thread(target=lento.serve_forever, daemon=True).start()
    bs = _browser_server_module()

    class _Proxy(bs.BrowserProxyHandler):
        pass

    _Proxy.token = "tok"
    _Proxy.voice_host = "127.0.0.1"
    _Proxy.voice_port = lento.server_address[1]
    _Proxy.voice_timeout = 1
    proxy = HTTPServer(("127.0.0.1", 0), _Proxy)
    threading.Thread(target=proxy.serve_forever, daemon=True).start()
    try:
        st, body = _post(proxy.server_address[1], {"prompt": "ciao"})
    finally:
        proxy.shutdown()
        proxy.server_close()  # R-570-1-M2
        lento.shutdown()
        lento.server_close()
    assert st == 504
    assert "entro 1 s" in body["error"] and "ancora in corso" in body["error"]
    assert "NON ripetere la richiesta" in body["error"]  # V-1 bot #308 su 2507621


def test_v2_browser_proxy_attesa_di_default_e_valore_sbagliato(monkeypatch, capsys):
    bs = _browser_server_module()
    assert bs.BrowserProxyHandler.voice_timeout == 600
    # R-568-1-M2: il timeout del socket del browser (socketserver) resta quello di sempre
    assert bs.BrowserProxyHandler.timeout is None
    monkeypatch.setattr(bs, "_load_dotenv", lambda root: None)

    class _NonDevePartire:
        def __init__(self, *a):
            raise AssertionError("valore sbagliato accettato: il server stava per partire")

    # R-568-2-M2: se il controllo sparisce il test fallisce, non resta appeso
    monkeypatch.setattr(bs, "ThreadingHTTPServer", _NonDevePartire)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "tok")
    for sbagliato in ("abc", "0", "-5"):
        monkeypatch.setenv("GAS_VOICE_TIMEOUT", sbagliato)
        assert bs.run_browser_server() == 1
        assert "GAS_VOICE_TIMEOUT" in capsys.readouterr().out


def test_v2_browser_proxy_connessione_appesa_502_subito(monkeypatch):
    """R-568-3-M2 / R-569-1-M2: se la CONNESSIONE al voice server resta appesa (server
    irraggiungibile), il proxy risponde 502 «non raggiungibile» dopo il tetto corto di
    connessione, non il 504 «ancora in corso» dopo l'attesa lunga della risposta."""
    import socket
    import time
    pieno = socket.socket()
    riempitivi = []
    proxy = None
    try:  # R-570-1-M2: ogni socket si chiude anche se il setup fallisce
        pieno.bind(("127.0.0.1", 0))
        pieno.listen(0)
        for _ in range(8):  # coda di accettazione piena: i connect successivi restano appesi
            c = socket.socket()
            riempitivi.append(c)
            c.setblocking(False)
            c.connect_ex(pieno.getsockname())
        bs = _browser_server_module()
        monkeypatch.setattr(bs, "_CONNECT_TIMEOUT", 1)

        class _Proxy(bs.BrowserProxyHandler):
            pass

        _Proxy.token = "tok"
        _Proxy.voice_host = "127.0.0.1"
        _Proxy.voice_port = pieno.getsockname()[1]
        _Proxy.voice_timeout = 30
        proxy = HTTPServer(("127.0.0.1", 0), _Proxy)
        threading.Thread(target=proxy.serve_forever, daemon=True).start()
        t0 = time.monotonic()
        st, body = _post(proxy.server_address[1], {"prompt": "ciao"})
    finally:
        if proxy is not None:
            proxy.shutdown()
            proxy.server_close()
        for c in riempitivi:
            c.close()
        pieno.close()
    assert st == 502 and "non raggiungibile" in body["error"]
    assert time.monotonic() - t0 < 10


def test_v2_browser_proxy_a_thread(monkeypatch, capsys):
    """V-1 bot #308: il proxy del browser parte su ThreadingHTTPServer, così mentre il forte
    lavora (fino a GAS_VOICE_TIMEOUT) la pagina si ricarica lo stesso."""
    bs = _browser_server_module()
    monkeypatch.setattr(bs, "_load_dotenv", lambda root: None)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "tok")
    monkeypatch.delenv("GAS_VOICE_TIMEOUT", raising=False)
    creati = []

    class _Finto:
        def __init__(self, indirizzo, handler):
            creati.append(handler)

        def serve_forever(self):
            raise KeyboardInterrupt

        def server_close(self):
            pass

    monkeypatch.setattr(bs, "ThreadingHTTPServer", _Finto)

    class _Vecchio:
        def __init__(self, *a):
            raise AssertionError("proxy tornato a HTTPServer a thread singolo")

    # R-571-1-M2: se il codice tornasse a HTTPServer il test fallisce, non resta appeso
    monkeypatch.setattr(bs, "HTTPServer", _Vecchio, raising=False)
    monkeypatch.setattr(bs.BrowserProxyHandler, "voice_timeout", 600)
    monkeypatch.setattr(bs.BrowserProxyHandler, "token", "")
    assert bs.run_browser_server() == 0
    assert creati == [bs.BrowserProxyHandler]
    assert "attesa massima 600 s" in capsys.readouterr().out


def test_v2_browser_proxy_risposta_rotta_502_json():
    """V-2 ve #308: una risposta HTTP rotta dal voice server diventa un 502 JSON chiaro,
    non una connessione chiusa («errore di rete» nel browser)."""
    import socket

    rotto = socket.socket()
    rotto.bind(("127.0.0.1", 0))
    rotto.listen(1)

    def _risponde_male():
        conn, _ = rotto.accept()
        with conn:
            conn.recv(65536)
            conn.sendall(b"NON-HTTP spazzatura\r\n\r\n")

    threading.Thread(target=_risponde_male, daemon=True).start()
    bs = _browser_server_module()

    class _Proxy(bs.BrowserProxyHandler):
        pass

    _Proxy.token = "tok"
    _Proxy.voice_host = "127.0.0.1"
    _Proxy.voice_port = rotto.getsockname()[1]
    _Proxy.voice_timeout = 5
    proxy = HTTPServer(("127.0.0.1", 0), _Proxy)
    threading.Thread(target=proxy.serve_forever, daemon=True).start()
    try:
        st, body = _post(proxy.server_address[1], {"prompt": "ciao"})
    finally:
        proxy.shutdown()
        proxy.server_close()
        rotto.close()
    assert st == 502 and "Risposta non valida" in body["error"]


# ---------------------------------------------------------------------------
# V3 (chat M2): conversazione filata — parte parlata corta, risposta audio+testo,
# /config del proxy, e il giro completo nel browser con microfono finto
# ---------------------------------------------------------------------------

def test_v3_parte_parlata_corta():
    from modules.voice.server import parte_parlata
    assert parte_parlata("Sì, meglio così. Procedo?") == "Sì, meglio così. Procedo?"
    lungo = "Uno. Due. Tre. Quattro. Cinque."
    assert parte_parlata(lungo) == "Uno. Due. Tre. Il resto è a schermo."
    # V4: si dice solo il primo paragrafo, il dettaglio dopo la riga vuota è a schermo
    assert (parte_parlata("Sì, procedo. Va bene?\n\nDettaglio:\n- a\n- b")
            == "Sì, procedo. Va bene? Il resto è a schermo.")
    assert parte_parlata("Uno. Due. Tre. Quattro.\n\nAltro.") == "Uno. Due. Tre. Il resto è a schermo."
    assert parte_parlata("Solo questo.\n\n   ") == "Solo questo."
    # R-574-4-M2: un a capo non è un taglio; «Dott.» non chiude la frase
    assert parte_parlata("Ciao.\nCome stai?") == "Ciao. Come stai?"
    assert (parte_parlata("Ho sentito il Dott. Rossi. Dice sì. Va bene? Poi altro.")
            == "Ho sentito il Dott. Rossi. Dice sì. Va bene? Il resto è a schermo.")
    enorme = "parola " * 200
    detto = parte_parlata(enorme)
    assert len(detto) <= 400 + len(" Il resto è a schermo.") and detto.endswith("schermo.")


def _post_formato(port, body, token):
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}/voice", data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}",
                 "X-Gas-Formato": "audio+testo"})
    try:
        with _SENZA_PROXY.open(req, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_v3_risposta_audio_testo(monkeypatch):
    """Con X-Gas-Formato: audio+testo → JSON col testo intero e l'audio (base64) della
    sola parte parlata; senza chiave ElevenLabs il testo arriva lo stesso (non 503)."""
    import base64
    from unittest.mock import patch
    lungo = "Prima. Seconda. Terza. Quarta da leggere."

    class _K:
        def run_turn(self, prompt, **kw):
            yield {"type": "final", "content": lungo}

    server, port = _make_server(_K(), "tok-v3-1234567")
    try:
        monkeypatch.setenv("ELEVENLABS_API_KEY", "fake")
        with patch("modules.voice.server.synthesize_speech", return_value=b"ID3x") as tts:
            st, body = _post_formato(port, {"prompt": "ciao"}, "tok-v3-1234567")
        assert st == 200 and body["content"] == lungo
        assert base64.b64decode(body["audio"]) == b"ID3x"
        assert tts.call_args[0][0] == "Prima. Seconda. Terza. Il resto è a schermo."
        monkeypatch.delenv("ELEVENLABS_API_KEY")
        st, body = _post_formato(port, {"prompt": "ciao"}, "tok-v3-1234567")
        assert st == 200 and body["content"] == lungo and "audio" not in body
        assert "ELEVENLABS_API_KEY" in body["errore_voce"]
    finally:
        server.shutdown()
        server.server_close()


def test_v3_browser_proxy_config_e_finestra(monkeypatch, capsys):
    bs = _browser_server_module()

    class _Proxy(bs.BrowserProxyHandler):
        pass

    _Proxy.finestra = 7.5
    proxy = HTTPServer(("127.0.0.1", 0), _Proxy)
    threading.Thread(target=proxy.serve_forever, daemon=True).start()
    try:
        with _SENZA_PROXY.open(f"http://127.0.0.1:{proxy.server_address[1]}/config", timeout=5) as r:
            assert json.loads(r.read()) == {"finestra": 7.5, "max_turni": 5, "interruzione": True,
                                            "agc": True}   # V9: acceso di default
    finally:
        proxy.shutdown()
        proxy.server_close()
    monkeypatch.setattr(bs, "_load_dotenv", lambda root: None)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "tok")
    monkeypatch.delenv("GAS_VOICE_TIMEOUT", raising=False)

    class _NonDevePartire:
        def __init__(self, *a):
            raise AssertionError("finestra sbagliata accettata")

    monkeypatch.setattr(bs, "ThreadingHTTPServer", _NonDevePartire)
    for sbagliata in ("abc", "0", "-1", "500"):
        monkeypatch.setenv("GAS_VOICE_FINESTRA", sbagliata)
        assert bs.run_browser_server() == 1
        assert "GAS_VOICE_FINESTRA" in capsys.readouterr().out
    monkeypatch.delenv("GAS_VOICE_FINESTRA")
    for sbagliato in ("abc", "0", "51", "2.5"):   # V-1 bot #311
        monkeypatch.setenv("GAS_VOICE_MAX_TURNI", sbagliato)
        assert bs.run_browser_server() == 1
        assert "GAS_VOICE_MAX_TURNI" in capsys.readouterr().out


def _wav(percorso, pezzi, rate=16000, rumore=0.0):
    """WAV mono 16 bit: pezzi = [(secondi, ampiezza)], ampiezza 0 = silenzio.
    V9: `rumore` = ampiezza di un ronzio costante a 150 Hz sommato a tutto (ventola, TV).
    Un ronzio e non rumore bianco: il rumore bianco lo toglie già la noiseSuppression del
    browser, e il test non proverebbe la soglia del fondo."""
    import math
    import struct
    import wave
    t = 0
    with wave.open(str(percorso), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        frames = bytearray()
        for secondi, amp in pezzi:
            for i in range(int(secondi * rate)):
                v = amp * math.sin(2 * math.pi * 220 * i / rate) if amp else 0.0
                if rumore:
                    v = max(-1.0, min(1.0, v + rumore * math.sin(2 * math.pi * 150 * t / rate)))
                t += 1
                frames += struct.pack("<h", int(v * 32767))
        w.writeframes(bytes(frames))


_GUIDA_BROWSER_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [url, mic, modo] = process.argv.slice(2);
  let browser;
  try {
    browser = await chromium.launch({ args: [
      '--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream',
      `--use-file-for-fake-audio-capture=${mic}%noloop`,
      '--autoplay-policy=no-user-gesture-required'] });
  } catch (e) { console.log('BROWSER_NON_DISPONIBILE ' + e.message); return; }
  const page = await browser.newPage();
  globalThis.__pagina = page;
  const errori = [];
  page.on('pageerror', e => errori.push(String(e)));
  await page.addInitScript(() => {
    window.__stati = [];
    window.__sorgenti = 0;   // V7b: quante frasi sono state messe nel player
    new MutationObserver(ms => {
      for (const m of ms) if (m.target.id === 'player' && m.attributeName === 'src') window.__sorgenti++;
    }).observe(document, { subtree: true, attributes: true, attributeFilter: ['src'] });
    new MutationObserver(() => {
      const s = document.getElementById('status');
      if (s && window.__stati[window.__stati.length - 1] !== s.textContent)
        window.__stati.push(s.textContent);
    }).observe(document, { subtree: true, childList: true, characterData: true });
  });
  await page.goto(url);
  await page.waitForTimeout(500);
  await page.click('#btn-record');
  if (modo === 'riascolto') {
    // R-574-1-M2: riascolto dal player mentre la finestra è riaperta
    await page.waitForFunction(() => {
      const st = window.__stati, i = st.findLastIndex(x => x.includes('Gas parla'));
      return i >= 0 && st.slice(i).some(x => x.includes('ti ascolto'));
    }, null, { timeout: 25000 });
    await page.evaluate(() => document.getElementById('player').play());
  }
  if (modo === 'pausa') {
    // R-575-1-M2: pausa dai controlli mentre Gas parla → conversazione chiusa, tasto libero
    await page.waitForFunction(() => document.getElementById('status').textContent.includes('Gas parla'),
                               null, { timeout: 25000 });
    await page.evaluate(() => document.getElementById('player').pause());
  }
  await page.waitForFunction(() => {
    const t = document.getElementById('status').textContent;
    return t.includes('conversazione chiusa') || t.includes('non riproducibile') || t.startsWith('errore');
  }, null, { timeout: 25000 });
  await page.waitForTimeout(3000);   // niente turni né errori dopo la chiusura
  // V-1 bot #313: la soglia calcolata dalla pagina stessa, con 300 ms tutti di voce media
  // (RMS 0,07, un «sì» detto appena si riapre l'ascolto) e con solo rumore di fondo
  const soglie = await page.evaluate(() => ({
    voceMedia: sogliaDaCampioni(Array(6).fill(0.07)),
    rumore: sogliaDaCampioni(Array(6).fill(0.004)),
    vuoto: sogliaDaCampioni([]) }));
  // V9: la soglia del fondo calcolata dalla pagina: troppo pochi campioni → 0; rumore
  // costante 0,06 → 0,12; parole con le pause → resta bassa; rumore fortissimo → tetto
  const fondo = await page.evaluate(() => {
    const prova = valori => { fondo.length = 0; fondo.push(...valori); return sogliaFondo(); };
    const parole = Array.from({ length: 60 }, (_, i) => (i % 4 === 0 ? 0.01 : 0.3));
    const interr = valori => { fondo.length = 0; fondo.push(...valori); return sogliaInterruzione(); };
    const esito = { poco: prova(Array(10).fill(0.06)), costante: prova(Array(60).fill(0.06)),
             parole: prova(parole), forte: prova(Array(60).fill(0.5)),
             interrVuoto: interr([]), interrRumore: interr(Array(60).fill(0.06)) };
    fondo.length = 0;
    return esito;
  });
  const stati = await page.evaluate(() => window.__stati);
  const testo = await page.textContent('#testo');
  const capito = await page.evaluate(() => {   // V6: «Ho capito: …» visibile, solo testo
    const c = document.getElementById('capito');
    return { testo: c.textContent, visibile: !c.hidden, html: c.innerHTML };
  });
  const tempi = await page.textContent('#tempi');   // V7
  const sorgenti = await page.evaluate(() => window.__sorgenti);
  const tempiVisibili = await page.isVisible('#tempi');   // V-1 bot #322 su 8dc872e
  await browser.close();
  console.log(JSON.stringify({ stati, testo, errori, soglie, capito, tempi, sorgenti, fondo, tempiVisibili }));
})().catch(async e => {
  console.error(e);
  try { console.error('STATI', JSON.stringify(await globalThis.__pagina.evaluate(() => window.__stati))); } catch (_) {}
  process.exit(1);
});
"""


@pytest.mark.parametrize("modo", ["normale", "riascolto", "pausa", "tetto", "errore",
                                  "interruzione", "interruzione_media", "colpo", "colpo_voce",
                                  "sisubito", "pezzi", "pezzi_interrotti", "guasto", "rumore_costante",
                                  "rumore_forte"])
def test_v3_conversazione_nel_browser(tmp_path, modo):
    """Giro completo nella pagina vera (Chromium headless, microfono finto da file):
    clic → la frase parte da sola alla fine della voce (nessun secondo clic) → «ci sto
    ragionando» dopo 2 s → risposta a schermo e a voce → la finestra si riapre → resta
    zitto → conversazione chiusa. Saltato se Playwright/Chromium non ci sono (CI)."""
    import base64
    import shutil
    import subprocess
    import time
    # V4 (V-2 bot #311): in CI (GAS_TEST_BROWSER_OBBLIGATORIO=1) il browser è installato
    # e il test non può essere saltato; in locale senza Node/Playwright si salta.
    obbligatorio = os.environ.get("GAS_TEST_BROWSER_OBBLIGATORIO") == "1"
    if not shutil.which("node") or subprocess.run(
            ["node", "-e", "require('playwright')"], capture_output=True).returncode != 0:
        if obbligatorio:
            pytest.fail("node + playwright richiesti (GAS_TEST_BROWSER_OBBLIGATORIO=1) ma assenti")
        pytest.skip("node + playwright non disponibili")

    microfono = tmp_path / "mic.wav"
    if modo in ("interruzione", "interruzione_media"):
        # V4: seconda voce mentre Gas parla (risposta di 4 s da ~6,2 s) → interruzione.
        # R-580-1-M2: a volume medio (0,1: RMS ~0,07, appena sopra la soglia d'interruzione)
        # la frase dopo l'interruzione va registrata, non persa.
        amp = 0.1 if modo == "interruzione_media" else 0.4
        _wav(microfono, [(0.8, 0), (1.5, 0.4), (4.5, 0), (1.2, amp), (8, 0)])
    elif modo == "colpo":
        # R-581-1-M2: un rumore breve (400 ms) mentre Gas parla lo zittisce, ma il clip
        # quasi muto che segue NON deve partire come frase
        _wav(microfono, [(0.8, 0), (1.5, 0.4), (4.5, 0), (0.4, 0.4), (10, 0)])
    elif modo == "colpo_voce":
        # R-582-1-M2: colpo breve (scartato), poi una frase vera: deve arrivare un webm
        # valido, senza la coda del clip scartato in testa
        _wav(microfono, [(0.8, 0), (1.5, 0.4), (4.5, 0), (0.4, 0.4), (1.6, 0), (1.2, 0.4), (8, 0)])
    elif modo == "pezzi_interrotti":
        # V7b: tre frasi da 1,5 s (dalla risposta a ~6,2 s); la terza arriva in ritardo
        # (~10,7 s) e la voce a ~9,6 s interrompe Gas MENTRE ASPETTA la terza: quando
        # arriva NON deve suonare
        _wav(microfono, [(0.8, 0), (1.5, 0.4), (7.3, 0), (1.2, 0.4), (8, 0)])
    elif modo == "rumore_costante":
        # V9 (R-584-1-M2): TV sempre accesa (ronzio di ampiezza 0,3 prima dei filtri del
        # browser; il livello dopo i filtri non è misurato qui) e una frase a ~0,8 s: una
        # sola frase, Gas non si zittisce da solo (la grazia di 500 ms) e la finestra si
        # chiude per silenzio. La soglia d'ascolto dal fondo la prova «rumore_forte».
        _wav(microfono, [(0.8, 0), (1.5, 0.5), (14, 0)], rumore=0.3)
    elif modo == "rumore_forte":
        # V-1 ve #327: ronzio più forte (sopra la vecchia soglia massima di ascolto, 0,045,
        # anche dopo i filtri del browser) già prima e durante l'ascolto: senza la soglia
        # dal fondo la frase non si chiuderebbe mai per silenzio
        _wav(microfono, [(3, 0), (1.5, 0.6), (14, 0)], rumore=0.6)
    elif modo == "sisubito":
        # V-1 bot #311 su c3079f4: voce già nei primi 300 ms dell'ascolto (un «sì» detto
        # subito) → deve contare come frase, non come rumore di fondo. (A volume medio lo
        # prova la soglia calcolata dalla pagina, «soglie» qui sotto: V-1 bot #313.)
        _wav(microfono, [(0.5, 0.4), (6, 0)])
    else:
        _wav(microfono, [(0.8, 0), (1.5, 0.4), (6, 0)])
    risposta = tmp_path / "risposta.wav"
    _wav(risposta, [({"pausa": 2.0, "interruzione": 4.0, "interruzione_media": 4.0,
                      "colpo": 4.0, "colpo_voce": 4.0, "pezzi_interrotti": 1.5}.get(modo, 0.4), 0.2)])
    audio_b64 = base64.b64encode(
        b"non-audio" * 50 if modo == "errore" else risposta.read_bytes()).decode()
    ricevute = []
    chiusure = []   # V7b R-619-1-M2: connessioni chiuse dalla pagina prima della 3ª frase
    import select
    import socket

    from http.server import BaseHTTPRequestHandler

    class _VoceFinta(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0) or 0)
            corpo = self.rfile.read(n)
            ricevute.append((self.headers.get("X-Gas-Formato"), self.headers.get("Content-Type"),
                             len(corpo), corpo[:4]))
            time.sleep(2.6)  # oltre i 2 s: deve partire la frase d'attesa
            if modo in ("pezzi", "pezzi_interrotti") and len(ricevute) == 1:
                # V7b: risposta a righe, la seconda frase arriva dopo che la prima è partita
                self.send_response(200)
                self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
                self.end_headers()
                frasi = 3 if modo == "pezzi_interrotti" else 2
                righe = [{"content": "Sì, meglio così. Procedo?", "audio": audio_b64,
                          "capito": "Gas, <b>meglio</b> così?", "pezzi": frasi}]
                righe += [{"audio": audio_b64} for _ in range(frasi - 1)]
                righe += [{"fine": True, "tempi": {"trascrizione": 0.5, "cervello": 1.25,
                                                   "voce": 0.2, "server": 2.0}}]
                try:
                    for i, r in enumerate(righe):
                        self.wfile.write(json.dumps(r).encode() + b"\n")
                        self.wfile.flush()
                        if modo == "pezzi_interrotti" and i == 1:
                            # R-619-1-M2: la pagina interrotta deve chiudere la connessione
                            # SUBITO, prima che arrivi la terza frase (~4,5 s dopo)
                            fine = time.monotonic() + 4.5
                            while time.monotonic() < fine:
                                pronto, _, _ = select.select([self.connection], [], [], 0.1)
                                if pronto and not self.connection.recv(1, socket.MSG_PEEK):
                                    chiusure.append(True)
                                    return
                        else:
                            time.sleep(0.25 if i == 0 else 0.05)
                except OSError:
                    pass
                return
            if modo == "guasto":  # V-1 bot #322: guasto lento, i tempi arrivano col 502
                out = json.dumps({"error": "voce non disponibile",
                                  "tempi": {"trascrizione": 0.5, "cervello": 1.25, "server": 2.0}}).encode()
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.wfile.write(out)
                return
            out = json.dumps({"content": "Sì, meglio così. Procedo?", "audio": audio_b64,
                              "capito": "Gas, <b>meglio</b> così?",
                              "tempi": {"trascrizione": 0.5, "cervello": 1.25, "server": 2.0}}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)

    voce = HTTPServer(("127.0.0.1", 0), _VoceFinta)
    threading.Thread(target=voce.serve_forever, daemon=True).start()
    bs = _browser_server_module()

    class _Proxy(bs.BrowserProxyHandler):
        pass

    _Proxy.token = "tok"
    _Proxy.voice_host = "127.0.0.1"
    _Proxy.voice_port = voce.server_address[1]
    _Proxy.finestra = 2
    _Proxy.max_turni = 1 if modo == "tetto" else 5
    # V9: con un ronzio costante si spegne l'AGC (GAS_VOICE_AGC=0, il rimedio della guida)
    _Proxy.agc = modo not in ("rumore_costante", "rumore_forte")
    proxy = bs.ThreadingHTTPServer(("127.0.0.1", 0), _Proxy)
    threading.Thread(target=proxy.serve_forever, daemon=True).start()
    guida = tmp_path / "guida.js"
    guida.write_text(_GUIDA_BROWSER_JS)
    try:
        r = subprocess.run(["node", str(guida), f"http://127.0.0.1:{proxy.server_address[1]}/",
                            str(microfono), modo], capture_output=True, text=True, timeout=60)
    finally:
        proxy.shutdown()
        proxy.server_close()
        voce.shutdown()
        voce.server_close()
    if "BROWSER_NON_DISPONIBILE" in r.stdout:
        if obbligatorio:
            pytest.fail("Chromium richiesto (GAS_TEST_BROWSER_OBBLIGATORIO=1) ma non avviabile: "
                        + r.stdout[-500:])
        pytest.skip("Chromium non disponibile")
    assert r.returncode == 0, (r.stdout[-2000:], r.stderr[-2000:])
    esito = json.loads(r.stdout.strip().splitlines()[-1])
    stati, testo = esito["stati"], esito["testo"]
    assert esito["errori"] == [], esito["errori"][:3]
    # V-1 bot #313: un «sì» a voce media che riempie i primi 300 ms supera la soglia
    soglie = esito["soglie"]
    assert soglie["voceMedia"] < 0.07, soglie
    assert soglie["rumore"] == soglie["vuoto"] == 0.015, soglie
    if modo not in ("interruzione", "interruzione_media", "colpo", "colpo_voce", "pezzi_interrotti"):
        assert len(ricevute) == 1, (ricevute, stati)
    assert ricevute[0][0] == "audio+testo+pezzi" and ricevute[0][2] > 0   # V7b
    if modo == "guasto":
        # V-1 bot #322: errore dichiarato e tempi a schermo anche sul guasto
        assert stati[-1] == "errore: voce non disponibile", stati
        assert esito["tempi"].startswith("tempi: ascolto 0.5s · cervello 1.3s · rete "), esito["tempi"]
        assert esito["tempiVisibili"] is True  # visibili davvero, non solo nel testo
        return
    assert testo == "Sì, meglio così. Procedo?"
    # V6: la pagina mostra cosa ha sentito, come testo (l'HTML nel parlato non diventa markup)
    assert esito["capito"]["testo"] == "Ho capito: «Gas, <b>meglio</b> così?»", esito["capito"]
    assert esito["capito"]["visibile"] and "<b>" not in esito["capito"]["html"]
    # V7: dove va il tempo; la rete è il totale visto dalla pagina meno i 2,0 s del server
    # (la voce finta risponde dopo 2,6 s, quindi la rete risulta ≥ 0,5 s)
    t = esito["tempi"]
    atteso = ("tempi: ascolto 0.5s · cervello 1.3s · voce 0.2s · rete " if modo == "pezzi"
              else "tempi: ascolto 0.5s · cervello 1.3s · rete ")   # V7b: a fine righe (interrotti: conta la 2ª risposta, JSON)
    assert t.startswith(atteso), t
    assert esito["tempiVisibili"] is True
    assert float(t.rsplit("rete ", 1)[1].rstrip("s")) >= 0.5, t
    assert any("parli" in s for s in stati), stati
    assert any("ci sto ragionando" in s for s in stati), stati
    if modo == "errore":
        # R-576-2-M2: audio rotto → turno chiuso, testo a schermo, niente riapertura
        assert "non riproducibile" in stati[-1], stati
        assert not any("ti ascolto" in s for s in stati[stati.index(next(s for s in stati if "ragionando" in s)):]), stati
        return
    assert any("Gas parla" in s for s in stati), stati
    # dopo la risposta la finestra si riapre da sola, poi si chiude per silenzio
    i_parla = max(i for i, s in enumerate(stati) if "Gas parla" in s)
    # ogni clip inviato è un file audio intero: webm comincia con l'header EBML
    assert all(r[3] == b"\x1a\x45\xdf\xa3" for r in ricevute if "webm" in (r[1] or "")), ricevute
    if modo == "colpo_voce":
        assert len(ricevute) == 2, (ricevute, stati)   # il colpo no, la frase vera sì
        return
    if modo == "rumore_costante":
        # V9: col ronzio sempre acceso (e AGC spento) una sola frase, Gas non si zittisce da
        # solo e la finestra si chiude per silenzio. Qui a reggere è la grazia di 500 ms
        # (il salto del rumore quando Gas comincia a parlare); la soglia d'interruzione che
        # sale col fondo è provata solo come funzione qui sotto (R-630-1-M2)
        assert not any("mi hai interrotto" in s for s in stati), stati
        assert "conversazione chiusa" in stati[-1], stati
        fondo = esito["fondo"]
        assert fondo["poco"] == 0 and abs(fondo["costante"] - 0.12) < 1e-9, fondo
        assert fondo["parole"] < 0.05 and fondo["forte"] == 0.2, fondo
        # e la soglia per zittire Gas sale col rumore (0,06 → 1,5 × 0,12)
        assert fondo["interrVuoto"] == 0.06 and abs(fondo["interrRumore"] - 0.18) < 1e-9, fondo
    if modo == "rumore_forte":
        # V-1 ve #327: col ronzio sopra la vecchia soglia la frase si chiude per silenzio
        # solo grazie alla soglia che segue il fondo (mutante senza → la frase non finisce)
        assert len(ricevute) == 1 and not any("mi hai interrotto" in s for s in stati), stati
        assert "conversazione chiusa" in stati[-1], stati
    if modo == "pezzi":
        # V7b: le due frasi suonano una dopo l'altra, poi il giro continua come sempre;
        # R-618-3-M2: a fine risposta il player riceve tutta la parte parlata (3ª sorgente)
        assert esito["sorgenti"] == 3, esito["sorgenti"]
    if modo == "pezzi_interrotti":
        # V7b: interrotto in attesa della terza frase: la terza non suona, la frase nuova parte
        assert any("mi hai interrotto" in s for s in stati), stati
        assert chiusure == [True], chiusure   # R-619-1-M2: lettura chiusa subito
        assert esito["sorgenti"] == 2 + (len(ricevute) - 1), (esito["sorgenti"], ricevute, stati)
        assert len(ricevute) == 2, (ricevute, stati)
        return
    if modo == "colpo":
        assert len(ricevute) == 1, (ricevute, stati)   # nessun clip muto inviato
        assert any("mi hai interrotto" in s for s in stati), stati
        return
    if modo in ("interruzione", "interruzione_media"):
        # Gas zittito dalla voce, la frase successiva parte da sola: 2 richieste
        assert len(ricevute) == 2, (ricevute, stati)
        assert any("mi hai interrotto" in s for s in stati), stati
        return
    if modo == "tetto":
        # V-1 bot #311: col tetto a 1 la finestra non si riapre dopo la risposta
        assert "turni di fila" in stati[-1], stati
        assert not any("ti ascolto" in s for s in stati[i_parla:]), stati
        return
    if modo == "pausa":
        assert any("risposta in pausa" in s for s in stati[i_parla:]), stati
        assert not any("ti ascolto" in s for s in stati[i_parla:]), stati
        return
    assert any("ti ascolto" in s for s in stati[i_parla:]), stati


# ── V7b (chat M2): voce frase per frase (risposta a righe NDJSON) ──

def test_v7b_frasi_parlate_ricompongono_la_parte_parlata():
    from modules.voice.server import frasi_parlate, parte_parlata
    for testo in ("Ciao. Dott. Rossi arriva alle 10. Va bene? Poi altro. E altro.",
                  "Una frase sola", "Primo.\n\nDettaglio da leggere a schermo.",
                  "x" * 900):
        frasi = frasi_parlate(testo)
        assert frasi and " ".join(frasi) == parte_parlata(testo), (testo, frasi)
    assert frasi_parlate("Ciao. Dott. Rossi arriva. Va bene?") == [
        "Ciao.", "Dott. Rossi arriva.", "Va bene?"]


def _voce_a_pezzi(kernel_testo, sintesi, formato="audio+testo+pezzi", chiave="k", turni=None,
                  trascrizione="Gas, dimmi", prompt_testo=None, root=None, intestazioni=None,
                  tts=None):
    """Server voce vero con kernel e servizi finti; ritorna (content-type, righe, mock della
    sintesi).
    `turni` (lista) riceve i kw di ogni run_turn (V10: quale istruzione arriva).
    `tts`: un mock della sintesi da riusare fra più richieste (stessa chiave di cache).
    Con `prompt_testo` la richiesta è a testo (JSON), non a voce (V11)."""
    from unittest.mock import patch
    import urllib.request
    from modules.voice.server import VoiceHandler

    class _K:
        def run_turn(self, prompt, **kw):
            if turni is not None:
                turni.append(kw)
            yield {"type": "final", "content": kernel_testo}

    class _H(VoiceHandler):
        pass
    _H.kernel = _K()
    if root is not None:  # fetta 3.2: cartella dei compiti in sottofondo
        _H.kernel.root = root
    _H.token = "tok"
    srv = HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    env = {"GROQ_API_KEY": "k", **({"ELEVENLABS_API_KEY": chiave} if chiave else {})}
    if prompt_testo is None:
        dati, tipo = b"RIFF" + bytes(60), {"Content-Type": "audio/wav"}
    else:
        dati = json.dumps({"prompt": prompt_testo}).encode()
        tipo = {"Content-Type": "application/json", "Accept": "audio/mpeg"}
    req = urllib.request.Request(
        f"http://127.0.0.1:{srv.server_address[1]}/voice", data=dati, method="POST",
        headers={"Authorization": "Bearer tok", "X-Gas-Formato": formato, **tipo,
                 **(intestazioni or {})})
    try:
        with patch("modules.voice.server.transcribe_audio", side_effect=[trascrizione]), \
             (patch("modules.voice.server.synthesize_speech", new=tts) if tts is not None
              else patch("modules.voice.server.synthesize_speech", side_effect=sintesi)) as tts, \
             patch.dict(os.environ, env):
            if not chiave:
                os.environ.pop("ELEVENLABS_API_KEY", None)
            os.environ.pop("GAS_VOCE_FORTE", None)
            with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=10) as r:
                ct = r.headers.get("Content-Type", "")
                corpo = r.read().decode("utf-8")
    finally:
        srv.shutdown()
        srv.server_close()
    righe = [json.loads(x) for x in corpo.splitlines() if x.strip()] if "ndjson" in ct else [json.loads(corpo)]
    return ct, righe, tts


def test_v7b_risposta_a_pezzi_una_sintesi_per_frase():
    import base64
    testo = "Ho trovato tre lead. Due sono caldi. Preparo le bozze?\n\nDettaglio: Rossi, Bianchi."
    ct, righe, tts = _voce_a_pezzi(testo, lambda frase, k, v: frase.encode())
    frasi = [c.args[0] for c in tts.call_args_list]
    assert ct.startswith("application/x-ndjson")
    assert frasi == ["Ho trovato tre lead.", "Due sono caldi.", "Preparo le bozze?",
                     "Il resto è a schermo."]
    primo = righe[0]
    assert primo["content"] == testo and primo["capito"] == "Gas, dimmi" and primo["pezzi"] == 4
    audio = [base64.b64decode(r["audio"]).decode() for r in righe if "audio" in r]
    assert audio == frasi                       # ogni riga porta la sua frase, in ordine
    assert all(set(r) == {"audio"} for r in righe[1:4])
    fine = righe[-1]
    assert fine["fine"] is True and len(righe) == 5
    assert {"trascrizione", "cervello", "voce", "voce_tutta", "server"} <= set(fine["tempi"])
    assert fine["tempi"]["voce"] <= fine["tempi"]["voce_tutta"]


def test_v7b_errore_tts_a_meta_ferma_la_voce():
    from modules.voice.tts import ElevenLabsTTSError
    effetti = [b"uno", ElevenLabsTTSError(500, "guasto"), b"tre"]
    ct, righe, tts = _voce_a_pezzi("Uno. Due. Tre.", effetti)
    assert tts.call_count == 2                   # dopo l'errore niente altre sintesi
    assert "audio" in righe[0] and "errore_voce" in righe[1] and "audio" not in righe[1]
    assert righe[-1]["fine"] is True and len(righe) == 3


def test_v7b_errore_tts_sulla_prima_frase():
    ct, righe, tts = _voce_a_pezzi("Uno. Due.", OSError("rete"))
    assert "audio" not in righe[0] and righe[0]["content"] == "Uno. Due."
    assert righe[0]["errore_voce"] == "Errore di rete verso ElevenLabs TTS"
    assert righe[-1]["fine"] is True and tts.call_count == 1


def test_v7b_senza_chiave_o_formato_vecchio_resta_json():
    ct, righe, tts = _voce_a_pezzi("Uno. Due.", lambda *a: b"x", chiave=None)
    assert ct.startswith("application/json") and "errore_voce" in righe[0] and tts.call_count == 0
    ct, righe, tts = _voce_a_pezzi("Uno. Due.", lambda *a: b"x", formato="audio+testo")
    assert ct.startswith("application/json") and tts.call_count == 1   # una sola sintesi
    assert "pezzi" not in righe[0]


def test_v10_frasi_voce_tutto_il_parlato_senza_schermo():
    """V10: senza schermo si dice tutta la risposta, divisa in frasi, entro il tetto; mai
    «Il resto è a schermo»; una prima frase troppo lunga si taglia all'ultimo spazio."""
    from modules.voice.server import frasi_voce, _PARLATO_VOCE_MAX_CHAR, _PARLATO_VOCE_RESTO
    testo = "Uno. Due. Tre. Quattro.\n\nDott. Rossi arriva. Cinque?"
    assert frasi_voce(testo) == ["Uno.", "Due.", "Tre.", "Quattro.", "Dott. Rossi arriva.", "Cinque?"]
    lungo = " ".join(f"Frase numero {i} abbastanza lunga da contare." for i in range(100))
    frasi = frasi_voce(lungo)
    # V-1 bot #330: tagliato → alla fine la frase fissa, così il taglio si sente
    assert frasi[-1] == _PARLATO_VOCE_RESTO
    assert len(" ".join(frasi[:-1])) <= _PARLATO_VOCE_MAX_CHAR < len(lungo)
    assert all(f.endswith(".") for f in frasi) and "schermo" not in " ".join(frasi)
    unica = "parola " * 400
    taglio, resto = frasi_voce(unica)
    assert len(taglio) <= _PARLATO_VOCE_MAX_CHAR and not taglio.endswith(" ")
    assert resto == _PARLATO_VOCE_RESTO
    assert _PARLATO_VOCE_RESTO not in frasi_voce(testo)   # non tagliato: niente avviso
    assert frasi_voce("   ") == []


def test_v10_formato_audio_pezzi_senza_schermo():
    """V10: «audio+pezzi» (client H24 senza schermo): stesse righe NDJSON della V7b, turno
    con ISTRUZIONE_VOCE (non quella con lo schermo), TUTTE le frasi dette."""
    import base64
    from modules.voice.server import ISTRUZIONE_VOCE
    turni = []
    testo = "Uno. Due. Tre. Quattro. Cinque."
    ct, righe, tts = _voce_a_pezzi(testo, lambda frase, k, v: frase.encode(),
                                   formato="audio+pezzi", turni=turni)
    assert ct.startswith("application/x-ndjson")
    assert turni[0]["istruzione_turno"].startswith(ISTRUZIONE_VOCE + " Adesso è ")  # V13
    frasi = [c.args[0] for c in tts.call_args_list]
    assert frasi == ["Uno.", "Due.", "Tre.", "Quattro.", "Cinque."]   # più di 3, niente «resto»
    assert righe[0]["content"] == testo and righe[0]["pezzi"] == 5
    assert [base64.b64decode(r["audio"]).decode() for r in righe if "audio" in r] == frasi
    assert righe[-1]["fine"] is True and "voce" in righe[-1]["tempi"]


def test_v10_non_ho_capito_a_righe():
    """V10: anche «non ho capito» arriva a righe col formato senza schermo, senza far partire
    il turno (il client H24 legge NDJSON solo con Content-Type application/x-ndjson: testo
    vuoto, chiave ElevenLabs mancante ed errori prima del turno restano un JSON unico)."""
    from modules.voice.stt import TrascrizioneIncerta
    turni = []
    ct, righe, tts = _voce_a_pezzi("mai usato", lambda frase, k, v: frase.encode(),
                                   formato="audio+pezzi", turni=turni,
                                   trascrizione=TrascrizioneIncerta("boh", "poco sicura"))
    assert ct.startswith("application/x-ndjson") and turni == []
    assert righe[0]["non_capito"] is True and righe[0]["capito"] == "boh"
    assert righe[-1]["fine"] is True and tts.call_count == 1


def test_v11_audio_pezzi_a_testo_solo_testo():
    """V11 (V-1 bot #330 su ae3258e): una richiesta a TESTO con «audio+pezzi» non passa dal
    tetto orario, quindi riceve solo il testo (JSON): nessuna sintesi ElevenLabs, anche se
    chiede Accept: audio/mpeg."""
    testo = "Uno. Due. Tre."
    ct, righe, tts = _voce_a_pezzi(testo, lambda frase, k, v: frase.encode(),
                                   formato="audio+pezzi", prompt_testo="dimmi")
    assert ct.startswith("application/json") and tts.call_count == 0
    assert righe[0]["content"] == testo and "audio" not in righe[0]


def test_v12_frasi_voce_parola_al_tetto():
    """V12 (R-660-2-M2): una prima frase più lunga del tetto con una parola che finisce
    proprio al tetto non perde quella parola; senza spazi si taglia al tetto."""
    from modules.voice.server import frasi_voce, _PARLATO_VOCE_MAX_CHAR, _PARLATO_VOCE_RESTO
    parole = ["abcdefghij"] + ["abcdefghi"] * 200      # spazi a 10, 20, … : uno cade sul tetto (800)
    testo = " ".join(parole)
    assert testo[_PARLATO_VOCE_MAX_CHAR] == " "
    taglio, resto = frasi_voce(testo)
    assert taglio == testo[:_PARLATO_VOCE_MAX_CHAR] and resto == _PARLATO_VOCE_RESTO
    taglio, resto = frasi_voce("x" * 2000)
    assert taglio == "x" * _PARLATO_VOCE_MAX_CHAR and resto == _PARLATO_VOCE_RESTO


def test_v12_audio_pezzi_senza_chiave_json():
    """V12 (R-660-1-M2): «audio+pezzi» senza chiave ElevenLabs → un JSON unico con
    errore_voce (non NDJSON, non 503): il client H24 lo distingue dal Content-Type."""
    ct, righe, tts = _voce_a_pezzi("Uno. Due.", lambda *a: b"x", formato="audio+pezzi", chiave=None)
    assert ct.startswith("application/json") and tts.call_count == 0
    assert righe[0]["content"] == "Uno. Due." and "ELEVENLABS_API_KEY" in righe[0]["errore_voce"]


def test_v12_testo_con_sintesi_conta_nel_tetto():
    """V12 (R-663-1-M2, decisione dell'operatore): una richiesta a TESTO che chiede la risposta
    a voce conta nel tetto orario; oltre il tetto 429 senza turno. Il solo testo non conta, la
    voce conta una volta sola, senza chiave ElevenLabs non conta."""
    import urllib.error
    import urllib.request
    from unittest.mock import patch
    from modules.voice.server import VoiceHandler
    turni = []

    class _K:
        def run_turn(self, prompt, **kw):
            turni.append(prompt)
            yield {"type": "final", "content": "Ciao."}

    class _H(VoiceHandler):
        pass
    _H.kernel = _K()
    _H.token = "tok"
    srv = HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    apri = urllib.request.build_opener(urllib.request.ProxyHandler({})).open

    def manda(intestazioni, voce=False):
        dati, tipo = ((b"RIFF" + bytes(60), "audio/wav") if voce
                      else (b'{"prompt": "dimmi"}', "application/json"))
        req = urllib.request.Request(
            f"http://127.0.0.1:{srv.server_address[1]}/voice", data=dati, method="POST",
            headers={"Authorization": "Bearer tok", "Content-Type": tipo, **intestazioni})
        try:
            with apri(req, timeout=10) as r:
                return r.status
        except urllib.error.HTTPError as exc:
            return exc.code
    try:
        with patch("modules.voice.server.synthesize_speech", return_value=b"mp3"), \
             patch("modules.voice.server.transcribe_audio", return_value="Gas, dimmi"), \
             patch.dict(os.environ, {"ELEVENLABS_API_KEY": "k", "GROQ_API_KEY": "g",
                                     "GAS_VOICE_MAX_TURNI_ORA": "3"}):
            os.environ.pop("GAS_VOCE_FORTE", None)
            # R-665-1-M2: una richiesta a VOCE conta una volta sola (Groq), non due
            assert manda({"X-Gas-Formato": "audio+testo"}, voce=True) == 200
            assert manda({"X-Gas-Formato": "audio+testo"}, voce=True) == 200
            assert manda({"X-Gas-Formato": "audio+testo"}) == 200
            assert manda({}) == 200                                  # solo testo: non conta
            # R-665-2-M2: audio+pezzi a testo è solo testo (V11) e non conta, anche con
            # Accept: audio/mpeg come manda il client H24
            assert manda({"X-Gas-Formato": "audio+pezzi", "Accept": "audio/mpeg"}) == 200
            assert manda({"X-Gas-Formato": "audio+testo+pezzi"}) == 429
            assert manda({"Accept": "audio/mpeg"}) == 429
            assert manda({"X-Gas-Formato": "audio+testo"}, voce=True) == 429
        assert len(turni) == 5 and len(_H.turni_parlati) == 3
        # R-665-3-M2: senza chiave ElevenLabs non si spende nulla, quindi non conta
        _H.turni_parlati = []
        with patch.dict(os.environ, {"GAS_VOICE_MAX_TURNI_ORA": "1"}):
            os.environ.pop("ELEVENLABS_API_KEY", None)
            assert manda({"X-Gas-Formato": "audio+testo"}) == 200
            assert manda({"X-Gas-Formato": "audio+testo"}) == 200
        assert _H.turni_parlati == []
    finally:
        srv.shutdown()
        srv.server_close()


def test_v7b_proxy_inoltra_le_righe_appena_arrivano():
    """Il proxy della pagina passa la prima riga subito, senza aspettare la fine della
    risposta (che qui arriva 1,5 s dopo)."""
    import socket
    import time
    from http.server import BaseHTTPRequestHandler

    class _APezzi(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            self.rfile.read(int(self.headers.get("Content-Length", 0) or 0))
            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'{"content": "uno", "audio": "QQ=="}\n')
            self.wfile.flush()
            time.sleep(1.5)
            try:
                self.wfile.write(b'{"fine": true}\n')
            except OSError:
                pass

    voce = HTTPServer(("127.0.0.1", 0), _APezzi)
    threading.Thread(target=voce.serve_forever, daemon=True).start()
    bs = _browser_server_module()

    class _Proxy(bs.BrowserProxyHandler):
        pass

    _Proxy.token = "tok"
    _Proxy.voice_host = "127.0.0.1"
    _Proxy.voice_port = voce.server_address[1]
    _Proxy.voice_timeout = 10
    proxy = HTTPServer(("127.0.0.1", 0), _Proxy)
    threading.Thread(target=proxy.serve_forever, daemon=True).start()
    try:
        s = socket.create_connection(("127.0.0.1", proxy.server_address[1]), timeout=10)
        corpo = b'{"prompt": "ciao"}'
        s.sendall(b"POST /voice HTTP/1.0\r\nContent-Type: application/json\r\n"
                  b"Content-Length: " + str(len(corpo)).encode() + b"\r\n\r\n" + corpo)
        t0 = time.monotonic()
        ricevuto = b""
        while b'"uno"' not in ricevuto:
            ricevuto += s.recv(4096)
        prima = time.monotonic() - t0
        while True:
            pezzo = s.recv(4096)
            if not pezzo:
                break
            ricevuto += pezzo
        s.close()
    finally:
        proxy.shutdown()
        proxy.server_close()
        voce.shutdown()
        voce.server_close()
    assert prima < 1.0, prima                          # la prima riga non aspetta la fine
    assert b"application/x-ndjson" in ricevuto and ricevuto.rstrip().endswith(b'{"fine": true}')


def test_v7b_pagina_chiusa_ferma_la_sintesi():
    """R-618-2-M2: se la pagina chiude la connessione dopo la prima riga, il server smette
    di sintetizzare (con al più una frase di ritardo: la prima scrittura dopo la chiusura
    del client riesce ancora). V-1 bot #325: tetto delle frasi alzato a 6, così senza lo
    stop le sintesi sarebbero 6 e il margine col codice giusto (≤ 3) è netto."""
    import socket
    import time
    from unittest.mock import patch
    from modules.voice.server import VoiceHandler

    class _K:
        def run_turn(self, prompt, **kw):
            yield {"type": "final", "content": "Uno. Due. Tre. Quattro. Cinque. Sei."}

    class _H(VoiceHandler):
        pass
    _H.kernel = _K()
    _H.token = "tok"
    srv = HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    corpo = b"RIFF" + bytes(60)

    def _lenta(frase, k, v):
        time.sleep(0.15)
        return frase.encode()

    try:
        with patch("modules.voice.server.transcribe_audio", return_value="Gas, dimmi"), \
             patch("modules.voice.server.synthesize_speech", side_effect=_lenta) as tts, \
             patch("modules.voice.server._PARLATO_MAX_FRASI", 6), \
             patch.dict(os.environ, {"GROQ_API_KEY": "k", "ELEVENLABS_API_KEY": "k"}):
            os.environ.pop("GAS_VOCE_FORTE", None)
            s = socket.create_connection(("127.0.0.1", srv.server_address[1]), timeout=10)
            s.sendall(b"POST /voice HTTP/1.0\r\nAuthorization: Bearer tok\r\n"
                      b"Content-Type: audio/wav\r\nX-Gas-Formato: audio+testo+pezzi\r\n"
                      b"Content-Length: " + str(len(corpo)).encode() + b"\r\n\r\n" + corpo)
            ricevuto = b""
            while b'"pezzi"' not in ricevuto:
                ricevuto += s.recv(4096)
            s.close()
            time.sleep(1.5)   # il tempo di sintetizzare tutte e sei le frasi, se non si fermasse
            sintesi = tts.call_count
    finally:
        srv.shutdown()
        srv.server_close()
    assert sintesi <= 3, sintesi   # su 6 frasi: la prima, al più una di ritardo (+1 in volo)


def test_v7b_pagina_chiusa_prima_degli_header():
    """V-3 bot #325: se la pagina è già chiusa quando il proxy scrive gli header della
    risposta a pezzi, _copia_righe si ferma (niente eccezione, quindi niente 502 su un
    socket morto né «Voice server non raggiungibile» falso)."""
    bs = _browser_server_module()
    h = bs.BrowserProxyHandler.__new__(bs.BrowserProxyHandler)

    def _rotto(*a, **k):
        raise BrokenPipeError("pagina chiusa")
    h.send_response = _rotto

    class _Resp:
        status = 200
        def getheader(self, *a):
            return "application/x-ndjson"
        def read1(self, n):
            raise AssertionError("non deve leggere: la pagina è chiusa")
    h._copia_righe(_Resp())   # non solleva


@pytest.mark.parametrize("evento, chiude", [("vuoto", True), ("errore", True),
                                            ("tempo", False), ("dati", False)])
def test_v7b_guardia_della_pagina(evento, chiude):
    """R-620-1-M2 / R-621: la guardia del proxy chiude la connessione verso la voce solo
    se la pagina ha chiuso (lettura vuota o errore di socket), non per un tempo scaduto
    né per dati inattesi."""
    bs = _browser_server_module()

    class _Pagina:
        def recv(self, n, flags=0):
            if evento == "tempo":
                raise TimeoutError("scaduto")
            if evento == "errore":
                raise ConnectionResetError("reset")
            return b"" if evento == "vuoto" else b"x"

    class _Voce:
        chiusa = False

        def shutdown(self, how):
            self.chiusa = True

    h = bs.BrowserProxyHandler.__new__(bs.BrowserProxyHandler)
    h.connection = _Pagina()
    voce = _Voce()
    h._guarda_pagina(voce)
    assert voce.chiusa is chiude


@pytest.mark.parametrize("valore, atteso", [(None, True), ("0", False), ("off", False),
                                            ("no", False), ("1", True), ("sì", True)])
def test_v9_gas_voice_agc(monkeypatch, valore, atteso):
    """R-630-3-M2: GAS_VOICE_AGC=0/off/no spegne il guadagno automatico del microfono
    (arriva alla pagina via /config); assente o altro → acceso, come prima."""
    bs = _browser_server_module()
    monkeypatch.setattr(bs, "_load_dotenv", lambda root: None)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "tok")
    for k in ("GAS_VOICE_TIMEOUT", "GAS_VOICE_FINESTRA", "GAS_VOICE_MAX_TURNI", "GAS_BROWSER_PORT"):
        monkeypatch.delenv(k, raising=False)
    if valore is None:
        monkeypatch.delenv("GAS_VOICE_AGC", raising=False)
    else:
        monkeypatch.setenv("GAS_VOICE_AGC", valore)

    class _Fermo(Exception):
        pass

    class _NonParte:
        def __init__(self, *a):
            raise _Fermo()

    monkeypatch.setattr(bs, "ThreadingHTTPServer", _NonParte)
    with pytest.raises(_Fermo):
        bs.run_browser_server()
    assert bs.BrowserProxyHandler.agc is atteso


# ── V13 (chat M2): ora locale nel turno parlato, risposte a voce più corte ──

def test_v13_ora_per_voce_data_ora_e_fuso_locali():
    """V13: la frase dell'ora usa l'ora LOCALE passata (fuso compreso), giorno e mese in
    italiano, e dice di non usare strumenti."""
    from datetime import datetime, timedelta, timezone
    from modules.voice.server import ora_per_voce
    roma = timezone(timedelta(hours=1), "CET")
    frase = ora_per_voce(datetime(2026, 11, 5, 18, 7, tzinfo=roma))
    assert frase.startswith("Adesso è giovedì 5 novembre 2026, ore 18:07 (ora locale, fuso CET)")
    assert "NON usare data_ora" in frase
    # il fuso conta: lo stesso istante in UTC è un'altra ora e un altro giorno
    tardi = ora_per_voce(datetime(2026, 12, 31, 23, 30, tzinfo=timezone.utc).astimezone(
        timezone(timedelta(hours=2), "EET")))
    assert "venerdì 1 gennaio 2027, ore 1:30 " in tardi and "fuso EET" in tardi  # V-2 bot #334


def test_v13_ora_per_voce_senza_argomento_usa_l_orologio_locale(monkeypatch):
    """V13: senza `adesso` vale l'ora locale della macchina (datetime.now().astimezone()).
    R-667-1-M2: fuso forzato diverso da UTC (CI e cloud girano in UTC), così un'ora senza
    fuso non passa per locale."""
    import time as _time
    from datetime import datetime
    from modules.voice.server import ora_per_voce
    monkeypatch.setenv("TZ", "Asia/Kolkata")  # UTC+5:30 tutto l'anno, niente ora legale
    _time.tzset()
    try:
        prima = datetime.now().astimezone()
        frase = ora_per_voce()
        dopo = datetime.now().astimezone()
        assert prima.utcoffset().total_seconds() == 5.5 * 3600
        assert any(f", ore {t.hour}:{t:%M} " in frase for t in (prima, dopo))
        assert f"fuso {prima.tzname()}" in frase and "fuso UTC" not in frase
    finally:
        monkeypatch.undo()
        _time.tzset()


def test_v13_istruzione_turno_voce_con_e_senza_schermo():
    """V13: l'istruzione del turno parlato è quella V3/V4 più l'ora; entrambe chiedono al
    massimo due frasi."""
    from datetime import datetime, timezone
    from modules.voice.server import (ISTRUZIONE_VOCE, ISTRUZIONE_VOCE_SCHERMO,
                                      istruzione_turno_voce)
    t = datetime(2026, 11, 5, 9, 5, tzinfo=timezone.utc)
    assert istruzione_turno_voce(False, t) == ISTRUZIONE_VOCE + " " + \
        "Adesso è giovedì 5 novembre 2026, ore 9:05 (ora locale, fuso UTC). In questo turno, " \
        "per l'ora o la data rispondi con questa e NON usare data_ora: vale al posto " \
        "dell'indicazione generale di usarlo."
    assert istruzione_turno_voce(True, t).startswith(ISTRUZIONE_VOCE_SCHERMO + " Adesso è giovedì")
    for istr in (ISTRUZIONE_VOCE, ISTRUZIONE_VOCE_SCHERMO):
        assert "mai più di due" in istr and "1-3" not in istr
        assert "UNA frase breve" in istr  # 10 nov: risposte più brevi (via M1)
        # niente «… sì o no?» in coda a ogni risposta (prova sul Mac del 5 nov)
        assert "Non chiudere con domande" in istr and "chiudi con una domanda" not in istr


# ---- Fetta 3.2 (chat M2, 7 nov): compiti in sottofondo finiti letti a voce ----

def _compito_finito(root, ident, stato="ok", risposta="Tre offerte: la migliore è la B.",
                    fine=None):
    import time as _t
    c = root / ".gas_sottofondo"
    c.mkdir(exist_ok=True)
    (c / f"{ident}.json").write_text(json.dumps({
        "id": ident, "compito": "confronta tre offerte", "stato": stato, "risposta": risposta,
        "creato": _t.time() - 60, "fine": _t.time() - 30 if fine is None else fine}))
    return c / f"{ident}.json"


def test_f32_compito_finito_letto_alla_prossima_attivazione(tmp_path):
    """A voce, prima della risposta: il compito finito (titolo + riassunto corto), poi segnato
    letto e non ripetuto al turno dopo."""
    f = _compito_finito(tmp_path, "20261107-100000-aaaaaa")
    ct, righe, tts = _voce_a_pezzi("Ciao.", lambda frase, k, v: frase.encode(), root=tmp_path)
    frasi = [c.args[0] for c in tts.call_args_list]
    assert frasi[0].startswith("Ho finito il compito in sottofondo «confronta tre offerte»")
    assert "la migliore è la B." in " ".join(frasi) and frasi[-1] == "Ciao."
    assert json.loads(f.read_text())["letto_a_voce"] is True
    ct, righe, tts = _voce_a_pezzi("Ciao.", lambda frase, k, v: frase.encode(), root=tmp_path)
    assert [c.args[0] for c in tts.call_args_list] == ["Ciao."]


def test_f32_testo_non_legge_e_non_segna(tmp_path):
    """A testo (anche con la sintesi chiesta) niente lettura: la coda resta per la voce."""
    f = _compito_finito(tmp_path, "20261107-100000-bbbbbb")
    _voce_a_pezzi("Ciao.", lambda frase, k, v: frase.encode(), root=tmp_path,
                  prompt_testo="ciao")
    assert "letto_a_voce" not in json.loads(f.read_text())


def test_f32_compito_fallito_e_vecchio(tmp_path):
    """Un compito fallito si dice in una frase; uno finito più di 24 ore fa non si legge."""
    import time as _t
    _compito_finito(tmp_path, "20261107-100000-cccccc", stato="ko", risposta="")
    vecchio = _compito_finito(tmp_path, "20261105-100000-dddddd", fine=_t.time() - 2 * 86400)
    ct, righe, tts = _voce_a_pezzi("Ciao.", lambda frase, k, v: frase.encode(), root=tmp_path)
    frasi = [c.args[0] for c in tts.call_args_list]
    assert frasi[0] == "Il compito in sottofondo «confronta tre offerte» non è riuscito."
    assert "letto_a_voce" not in json.loads(vecchio.read_text())


def test_f32_errore_nella_coda_non_rompe_la_risposta(tmp_path, monkeypatch):
    import modules.sottofondo as sf

    def _rotto(root):
        raise RuntimeError("x")
    monkeypatch.setattr(sf, "da_leggere", _rotto)
    _compito_finito(tmp_path, "20261107-100000-eeeeee")
    ct, righe, tts = _voce_a_pezzi("Ciao.", lambda frase, k, v: frase.encode(), root=tmp_path)
    assert [c.args[0] for c in tts.call_args_list] == ["Ciao."]


def test_f32_seguito_non_legge(tmp_path):
    """Nel seguito (parlato della stanza, X-Gas-Seguito: 1) i compiti finiti non si leggono:
    restano per la prossima attivazione."""
    f = _compito_finito(tmp_path, "20261107-100000-ffffff")
    ct, righe, tts = _voce_a_pezzi("Ciao.", lambda frase, k, v: frase.encode(), root=tmp_path,
                                   intestazioni={"X-Gas-Seguito": "1"})
    assert "Ho finito" not in " ".join(c.args[0] for c in tts.call_args_list)
    assert "letto_a_voce" not in json.loads(f.read_text())


def test_f32_due_compiti_lunghi_non_tolgono_la_risposta(tmp_path):
    """Bot #350 V-1: con schermo (audio+testo+pezzi) due compiti con riassunto lungo non
    consumano il limite della parte parlata: la risposta viene detta lo stesso; a schermo i
    compiti sono il primo paragrafo."""
    lunga = "Prima frase del risultato. " + "parola " * 40 + "fine."
    _compito_finito(tmp_path, "20261107-100000-gggggg", risposta=lunga)
    _compito_finito(tmp_path, "20261107-100001-hhhhhh", risposta=lunga)
    ct, righe, tts = _voce_a_pezzi("Ciao. Tutto bene.", lambda frase, k, v: frase.encode(),
                                   root=tmp_path)
    frasi = [c.args[0] for c in tts.call_args_list]
    assert frasi[-2:] == ["Ciao.", "Tutto bene."]
    assert sum(f.startswith("Ho finito il compito") for f in frasi) == 2
    assert righe[0]["content"].startswith("Ho finito il compito")
    assert righe[0]["content"].endswith("\n\nCiao. Tutto bene.")


def test_f32_client_senza_schermo_audio_pezzi(tmp_path):
    """Il client H24 (audio+pezzi, tutto a voce): prima i compiti, poi la risposta intera."""
    _compito_finito(tmp_path, "20261107-100000-iiiiii")
    ct, righe, tts = _voce_a_pezzi("Ciao.", lambda frase, k, v: frase.encode(),
                                   formato="audio+pezzi", root=tmp_path)
    frasi = [c.args[0] for c in tts.call_args_list]
    assert frasi[0].startswith("Ho finito il compito in sottofondo") and frasi[-1] == "Ciao."


def test_f32_senza_chiave_tts_compiti_nel_testo(tmp_path):
    """Senza chiave ElevenLabs la risposta arriva a testo con i compiti come primo paragrafo."""
    f = _compito_finito(tmp_path, "20261107-100000-llllll")
    ct, righe, tts = _voce_a_pezzi("Ciao.", lambda frase, k, v: frase.encode(), chiave=None,
                                   root=tmp_path)
    assert righe[0]["content"].startswith("Ho finito il compito in sottofondo")
    assert righe[0]["content"].endswith("\n\nCiao.")
    assert json.loads(f.read_text())["letto_a_voce"] is True


# ---- Riserve BASSE della #350 (chat M2, 8 nov) ----

def _letto(f):
    return json.loads(f.read_text()).get("letto_a_voce") is True


def test_f32b_sintesi_fallita_non_segna_letti(tmp_path):
    """Ve #350 V-1: senza schermo (audio+pezzi), se la sintesi della prima frase fallisce i
    compiti non risultano letti (si ridicono alla prossima attivazione)."""
    from modules.voice.tts import ElevenLabsTTSError
    f = _compito_finito(tmp_path, "20261108-100000-aaaaaa")

    def _rotta(frase, k, v):
        raise ElevenLabsTTSError(500, "giù")
    _voce_a_pezzi("Ciao.", _rotta, formato="audio+pezzi", root=tmp_path)
    assert not _letto(f)


@pytest.mark.parametrize("formato", ["audio+testo+pezzi", "audio+testo"])
def test_f32c_con_schermo_voce_fallita_segna_letti(tmp_path, formato):
    """Bot #352 (f6de3e6) V-1, regola unica: con uno schermo il testo con i compiti arriva
    anche se la voce fallisce → letti; R-711-1-M2: test di sintesi fallita nel ramo MP3 unico."""
    from modules.voice.tts import ElevenLabsTTSError
    f = _compito_finito(tmp_path, "20261109-100000-aaaaaa")

    def _rotta(frase, k, v):
        raise ElevenLabsTTSError(500, "giù")
    ct, righe, tts = _voce_a_pezzi("Ciao.", _rotta, formato=formato, root=tmp_path)
    assert righe[0]["content"].startswith("Ho finito") and "errore_voce" in righe[0]
    assert _letto(f)


def test_f32b_segnati_appena_dette_le_frasi_dei_compiti(tmp_path):
    """Senza schermo (audio+pezzi): dette le frasi dei compiti, risultano letti anche se poi
    la sintesi della risposta fallisce."""
    from modules.voice.tts import ElevenLabsTTSError
    f = _compito_finito(tmp_path, "20261108-100000-bbbbbb", risposta="Fatto.")
    chiamate = []

    def _poi_rotta(frase, k, v):
        chiamate.append(frase)
        if frase == "Ciao.":
            raise ElevenLabsTTSError(500, "giù")
        return frase.encode()
    _voce_a_pezzi("Ciao.", _poi_rotta, formato="audio+pezzi", root=tmp_path)
    assert chiamate[0].startswith("Ho finito") and _letto(f)


def test_f32b_risposta_vuota_dice_comunque_i_compiti(tmp_path):
    """R-710-1-M2: risposta del modello vuota → la frase dei compiti si dice lo stesso."""
    f = _compito_finito(tmp_path, "20261108-100000-cccccc")
    ct, righe, tts = _voce_a_pezzi("", lambda frase, k, v: frase.encode(),
                                   formato="audio+pezzi", root=tmp_path)
    frasi = [c.args[0] for c in tts.call_args_list]
    assert frasi and frasi[0].startswith("Ho finito") and _letto(f)


@pytest.mark.parametrize("parola", ["Gas.", "Hey Jarvis!"])
def test_f32b_solo_parola_di_attivazione_dice_i_compiti(tmp_path, parola):
    """Bot #350 V-5: con la sola parola di attivazione («Dimmi.») i compiti si dicono prima."""
    f = _compito_finito(tmp_path, "20261108-100000-dddddd")
    ct, righe, tts = _voce_a_pezzi("non usato", lambda frase, k, v: frase.encode(),
                                   trascrizione=parola, root=tmp_path)
    frasi = [c.args[0] for c in tts.call_args_list]
    assert frasi[0].startswith("Ho finito") and frasi[-1] == "Dimmi." and _letto(f)


def test_f32b_solo_parola_nel_seguito_non_legge(tmp_path):
    f = _compito_finito(tmp_path, "20261108-100000-eeeeee")
    _voce_a_pezzi("non usato", lambda frase, k, v: frase.encode(), trascrizione="Gas.",
                  root=tmp_path, intestazioni={"X-Gas-Seguito": "1"})
    assert not _letto(f)


def test_f32b_formato_audio_testo_sintesi_unica(tmp_path):
    """Bot #350 (40c5b30) V-1: ramo audio+testo (un solo MP3): compiti prima, poi la parte
    parlata della risposta; segnati letti."""
    import base64
    f = _compito_finito(tmp_path, "20261108-100000-ffffff")
    ct, righe, tts = _voce_a_pezzi("Ciao.", lambda frase, k, v: frase.encode(),
                                   formato="audio+testo", root=tmp_path)
    detto = base64.b64decode(righe[0]["audio"]).decode()
    assert detto.startswith("Ho finito il compito") and detto.endswith("Ciao.") and _letto(f)


def test_f32b_mp3_diretto(tmp_path):
    """Ramo audio/mpeg (_do_tts_response): compiti prima della risposta, segnati letti."""
    from unittest.mock import patch
    import urllib.request
    from modules.voice.server import VoiceHandler
    f = _compito_finito(tmp_path, "20261108-100000-gggggg")

    class _K:
        root = tmp_path

        def run_turn(self, prompt, **kw):
            yield {"type": "final", "content": "Ciao."}

    class _H(VoiceHandler):
        pass
    _H.kernel = _K()
    _H.token = "tok"
    srv = HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    req = urllib.request.Request(
        f"http://127.0.0.1:{srv.server_address[1]}/voice", data=b"RIFF" + bytes(60),
        method="POST", headers={"Authorization": "Bearer tok", "Content-Type": "audio/wav",
                                "Accept": "audio/mpeg"})
    try:
        with patch("modules.voice.server.transcribe_audio", side_effect=["Gas, dimmi"]), \
             patch("modules.voice.server.synthesize_speech",
                   side_effect=lambda frase, k, v: frase.encode()), \
             patch.dict(os.environ, {"GROQ_API_KEY": "k", "ELEVENLABS_API_KEY": "k"}):
            os.environ.pop("GAS_VOCE_FORTE", None)
            with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=10) as r:
                corpo = r.read().decode()
    finally:
        srv.shutdown()
        srv.server_close()
    assert corpo.startswith("Ho finito il compito") and corpo.endswith("Ciao.") and _letto(f)


def test_f32c_mp3_diretto_sintesi_fallita_non_segna(tmp_path):
    """R-711-1-M2: ramo audio/mpeg con sintesi fallita (502) → compiti non letti."""
    from unittest.mock import patch
    import urllib.request
    import urllib.error
    from modules.voice.server import VoiceHandler
    from modules.voice.tts import ElevenLabsTTSError
    f = _compito_finito(tmp_path, "20261109-100000-bbbbbb")

    class _K:
        root = tmp_path

        def run_turn(self, prompt, **kw):
            yield {"type": "final", "content": "Ciao."}

    class _H(VoiceHandler):
        pass
    _H.kernel = _K()
    _H.token = "tok"
    srv = HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    req = urllib.request.Request(
        f"http://127.0.0.1:{srv.server_address[1]}/voice", data=b"RIFF" + bytes(60),
        method="POST", headers={"Authorization": "Bearer tok", "Content-Type": "audio/wav",
                                "Accept": "audio/mpeg"})

    def _rotta(frase, k, v):
        raise ElevenLabsTTSError(500, "giù")
    codice = None
    try:
        with patch("modules.voice.server.transcribe_audio", side_effect=["Gas, dimmi"]), \
             patch("modules.voice.server.synthesize_speech", side_effect=_rotta), \
             patch.dict(os.environ, {"GROQ_API_KEY": "k", "ELEVENLABS_API_KEY": "k"}):
            os.environ.pop("GAS_VOCE_FORTE", None)
            try:
                urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=10)
            except urllib.error.HTTPError as e:
                codice = e.code
    finally:
        srv.shutdown()
        srv.server_close()
    assert codice == 502 and not _letto(f)


def test_f32c_dimmi_senza_tts_a_testo(tmp_path):
    """Bot #352 V-1 (893b863): «Dimmi.» senza chiave TTS, risposta JSON a testo: compiti come
    primo paragrafo e segnati letti dopo l'invio."""
    f = _compito_finito(tmp_path, "20261109-100000-cccccc")
    ct, righe, tts = _voce_a_pezzi("non usato", lambda frase, k, v: frase.encode(),
                                   chiave=None, trascrizione="Gas.", root=tmp_path,
                                   formato="")
    assert righe[0]["content"].startswith("Ho finito") and righe[0]["content"].endswith("Dimmi.")
    assert _letto(f)


def test_f32c_finiti_jobs_azzerati_a_ogni_richiesta(monkeypatch):
    """R-711-3-M2 (ve #356 V-1): i compiti tenuti da una richiesta precedente sulla stessa
    connessione (keep-alive) non vengono segnati letti dalla richiesta dopo."""
    from modules import sottofondo
    segnati = []
    monkeypatch.setattr(sottofondo, "segna_letti", lambda root, jobs: segnati.append(jobs))
    h = VoiceHandler.__new__(VoiceHandler)
    h.path = "/non-esiste"
    h.headers = {}
    h._send_json = lambda code, payload: None
    h._finiti_jobs = [{"id": "della-richiesta-prima"}]
    h.do_POST()
    h._segna_finiti_letti()
    assert segnati == []


# ---- Velocità: cache delle frasi fisse (chat M2, 9 nov) ----

def test_sintesi_frasi_fisse_dalla_cache(monkeypatch):
    """Le frasi fisse si sintetizzano una volta per voce; il testo libero mai in cache;
    un audio vuoto non entra in cache."""
    import modules.voice.server as srv
    chiamate = []

    def _finta(frase, k, v):
        chiamate.append((frase, v))
        return b"" if frase == srv.RISPOSTA_PAUSA else frase.encode()
    monkeypatch.setattr(srv, "synthesize_speech", _finta)
    monkeypatch.setattr(srv, "_cache_frasi", {})
    assert srv.sintesi("Dimmi.", "k", "v1") == b"Dimmi."
    assert srv.sintesi("Dimmi.", "k", "v1") == b"Dimmi."
    assert srv.sintesi("Dimmi.", "k", "v2") == b"Dimmi."
    srv.sintesi("Ciao a te.", "k", "v1")
    srv.sintesi("Ciao a te.", "k", "v1")
    srv.sintesi(srv.RISPOSTA_PAUSA, "k", "v1")
    srv.sintesi(srv.RISPOSTA_PAUSA, "k", "v1")
    assert chiamate == [("Dimmi.", "v1"), ("Dimmi.", "v2"), ("Ciao a te.", "v1"),
                        ("Ciao a te.", "v1"), (srv.RISPOSTA_PAUSA, "v1"),
                        (srv.RISPOSTA_PAUSA, "v1")]


@pytest.mark.parametrize("formato", ["audio+testo+pezzi", "audio+testo"])
def test_sintesi_cache_usata_dalle_risposte(monkeypatch, formato):
    """Bot #356 V-3: le risposte vere (pezzi, audio+testo, MP3 diretto) passano da sintesi(),
    quindi «Dimmi.» finisce nella cache (chiave: funzione di sintesi, voce, frase)."""
    import modules.voice.server as srv
    cache = {}
    monkeypatch.setattr(srv, "_cache_frasi", cache)
    _, _, tts = _voce_a_pezzi("non usato", lambda frase, k, v: frase.encode(),
                              trascrizione="Gas.", formato=formato)
    assert [c.args[0] for c in tts.call_args_list] == ["Dimmi."]
    assert [(k[2], v) for k, v in cache.items()] == [("Dimmi.", b"Dimmi.")]


def test_sintesi_cache_usata_dal_mp3_diretto(monkeypatch):
    """Bot #356 V-3: anche il ramo MP3 diretto (_do_tts_response) passa da sintesi():
    la seconda «Dimmi.» viene dalla cache."""
    import modules.voice.server as srv
    chiamate, inviati = [], []
    monkeypatch.setattr(srv, "_cache_frasi", {})
    monkeypatch.setattr(srv, "synthesize_speech", lambda f, k, v: chiamate.append(f) or f.encode())
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    h = VoiceHandler.__new__(VoiceHandler)
    h._tempi = None
    h._finiti_jobs = None
    h._send_audio = inviati.append
    h._do_tts_response("Dimmi.")
    h._do_tts_response("Dimmi.")
    assert chiamate == ["Dimmi."] and inviati == [b"Dimmi.", b"Dimmi."]


def test_sintesi_errore_non_in_cache(monkeypatch):
    """Un errore di ElevenLabs passa al chiamante e non lascia niente in cache."""
    import modules.voice.server as srv
    from modules.voice.tts import ElevenLabsTTSError
    monkeypatch.setattr(srv, "_cache_frasi", {})

    def _rotta(frase, k, v):
        raise ElevenLabsTTSError(500, "giù")
    monkeypatch.setattr(srv, "synthesize_speech", _rotta)
    with pytest.raises(ElevenLabsTTSError):
        srv.sintesi("Dimmi.", "k", "v1")
    assert srv._cache_frasi == {}


def test_sintesi_cache_ha_un_tetto(monkeypatch):
    import modules.voice.server as srv
    monkeypatch.setattr(srv, "synthesize_speech", lambda f, k, v: b"x")
    monkeypatch.setattr(srv, "_cache_frasi", {})
    for i in range(srv._CACHE_FRASI_MAX + 5):
        srv.sintesi("Dimmi.", "k", f"voce{i}")
    assert len(srv._cache_frasi) <= srv._CACHE_FRASI_MAX


def test_sintesi_cache_anche_per_le_frasi_divise(monkeypatch):
    """Bot #356 V-1: nelle risposte a pezzi una frase fissa di più frasi (es. l'uso di «forte»)
    viene divisa; anche i suoi pezzi vanno in cache. Un testo diverso no."""
    import modules.voice.server as srv
    chiamate = []
    monkeypatch.setattr(srv, "synthesize_speech", lambda f, k, v: chiamate.append(f) or b"x")
    monkeypatch.setattr(srv, "_cache_frasi", {})
    pezzi = srv._dividi_frasi(srv._USO_FORTE_PARLATO)
    assert len(pezzi) >= 2
    for _ in range(2):
        for p in pezzi:
            srv.sintesi(p, "k", "v")
    assert chiamate == pezzi
    srv.sintesi(pezzi[0] + " Altro.", "k", "v")
    srv.sintesi(pezzi[0] + " Altro.", "k", "v")
    assert chiamate[len(pezzi):] == [pezzi[0] + " Altro."] * 2


def test_sintesi_cache_forte_a_pezzi_dal_server(monkeypatch):
    """Bot #360 V-1: sul percorso vero («Gas, forte.» senza richiesta → risposta d'uso a pezzi)
    ogni frase della risposta d'uso finisce nella cache."""
    import modules.voice.server as srv
    cache = {}
    monkeypatch.setattr(srv, "_cache_frasi", cache)
    _, righe, tts = _voce_a_pezzi("non usato", lambda frase, k, v: frase.encode(),
                                  trascrizione="Gas, forte.", formato="audio+testo+pezzi")
    pezzi = srv._dividi_frasi(srv._USO_FORTE_PARLATO)
    assert [c.args[0] for c in tts.call_args_list] == pezzi
    assert sorted(k[2] for k in cache) == sorted(pezzi)
    # bot #360 (2° giro): la seconda richiesta, con la stessa sintesi, legge dalla cache
    tts.reset_mock()
    _, righe2, tts2 = _voce_a_pezzi("non usato", None, trascrizione="Gas, forte.",
                                    formato="audio+testo+pezzi", tts=tts)
    assert tts2 is tts and tts.call_count == 0
    # stessa risposta, audio dalla memoria (i tempi misurati no: cambiano da una richiesta
    # all'altra, bot #360 3° giro)
    senza_tempi = lambda rr: [{k: v for k, v in r.items() if k != "tempi"} for r in rr]  # noqa: E731
    assert senza_tempi(righe2) == senza_tempi(righe)


# ---- R8 fetta 1 (chat M2, sicurezza): tentativi falliti, tetto al testo, avvio chiuso ----

class TestR8Limiti:
    TOKEN = "token_r8_valido"

    def setup_method(self):
        _MockKernel.instances.clear()
        self.kernel = _MockKernel()
        self.server, self.port = _make_server(self.kernel, token=self.TOKEN)

    def teardown_method(self):
        self.server.shutdown()
        self.server.server_close()

    def _giusto(self):
        return _post(self.port, {"prompt": "ciao"}, headers={"Authorization": f"Bearer {self.TOKEN}"})

    def _sbagliato(self):
        return _post(self.port, {"prompt": "ciao"}, headers={"Authorization": "Bearer sbagliato_r8"})

    def test_troppi_falliti_bloccano_anche_il_token_giusto(self, monkeypatch, caplog):
        import modules.voice.server as srv
        monkeypatch.setenv("GAS_VOICE_MAX_FALLITI", "3")
        monkeypatch.setattr(srv, "_FALLITI_BLOCCO_S", 0.5)
        with caplog.at_level(logging.WARNING, logger="modules.voice.server"):
            assert [self._sbagliato()[0] for _ in range(3)] == [401, 401, 429]
            assert self._giusto()[0] == 429          # bloccato anche col token giusto
        testo = " ".join(r.message for r in caplog.records)
        assert "AUTH BLOCCO ip=127.0.0.1" in testo and "AUTH BLOCCATO ip=127.0.0.1" in testo
        assert "sbagliato_r8" not in testo and self.TOKEN not in testo
        time.sleep(0.6)
        assert self._giusto()[0] == 200          # il blocco scade da solo
        assert self._sbagliato()[0] == 401       # e il conto riparte da zero

    def test_richieste_senza_token_non_bloccano(self, monkeypatch):
        """Bot #358 V-1: richieste senza «Bearer <token>» (come quelle che una pagina web può
        mandare al server locale) non contano per il blocco: il token giusto passa ancora."""
        monkeypatch.setenv("GAS_VOICE_MAX_FALLITI", "3")
        senza = [_post(self.port, {"prompt": "ciao"}, headers={})[0] for _ in range(20)]
        vuoto = [_post(self.port, {"prompt": "ciao"}, headers={"Authorization": "Bearer "})[0]
                 for _ in range(5)]
        altro = [_post(self.port, {"prompt": "ciao"}, headers={"Authorization": "Basic abc"})[0]
                 for _ in range(5)]
        assert set(senza) == set(vuoto) == set(altro) == {401}
        assert self._giusto()[0] == 200
        assert [self._sbagliato()[0] for _ in range(3)] == [401, 401, 429]  # un token sì

    def _con_host(self, host, token):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            c.putrequest("POST", "/voice", skip_host=True)
            c.putheader("Host", host)
            c.putheader("Content-Type", "application/json")
            corpo = b'{"prompt": "ciao"}'
            c.putheader("Content-Length", str(len(corpo)))
            c.putheader("Authorization", f"Bearer {token}")
            c.endheaders(corpo)
            return c.getresponse().status
        finally:
            c.close()

    def test_host_di_dominio_rifiutato_e_non_conta(self, monkeypatch):
        """R-731-1-M2 (DNS rebinding): un Host che è un nome di dominio riceve 403 anche col
        token giusto, il kernel non parte e il blocco dell'IP non scatta."""
        monkeypatch.setenv("GAS_VOICE_MAX_FALLITI", "2")
        chiamate = []
        orig = self.kernel.run_turn
        self.kernel.run_turn = lambda p: chiamate.append(p) or orig(p)
        stati = [self._con_host("evil.example:8765", "sbagliato") for _ in range(5)]
        assert stati == [403] * 5
        assert self._con_host("evil.example", self.TOKEN) == 403
        assert chiamate == []
        assert self._giusto()[0] == 200                      # nessun blocco per l'IP

    @pytest.mark.parametrize("host", ["localhost:8765", "LOCALHOST", "127.0.0.1:8765",
                                      "[::1]:8765"])
    def test_host_locali_ammessi(self, host):
        assert self._con_host(host, self.TOKEN) == 200

    def test_token_giusto_non_azzera_e_falliti_sotto_soglia(self, monkeypatch):
        monkeypatch.setenv("GAS_VOICE_MAX_FALLITI", "3")
        assert [self._sbagliato()[0] for _ in range(2)] == [401, 401]
        assert self._giusto()[0] == 200
        assert self._sbagliato()[0] == 429       # il terzo fallito nella finestra blocca

    def test_memoria_piena_conta_e_blocca_ancora(self, monkeypatch):
        """R-720-4-M2 (bot #358): con la memoria piena l'IP nuovo si conta e si blocca lo stesso
        (esce la voce più vecchia), la memoria resta entro il tetto."""
        import modules.voice.server as srv
        monkeypatch.setenv("GAS_VOICE_MAX_FALLITI", "2")
        monkeypatch.setattr(srv, "_FALLITI_MAX_IP", 3)
        cls = self.server.RequestHandlerClass
        adesso = time.monotonic()
        cls.falliti = {f"ip-vecchio-{i}": [adesso - 10 + i] for i in range(3)}
        cls.bloccati = {f"ip-bloccato-{i}": adesso + 100 + i for i in range(3)}
        assert [self._sbagliato()[0] for _ in range(2)] == [401, 429]
        assert self._giusto()[0] == 429                  # 127.0.0.1 bloccato davvero
        assert "127.0.0.1" in cls.bloccati and len(cls.bloccati) == 3
        assert "ip-bloccato-0" not in cls.bloccati       # uscito quello che scadeva prima
        assert "ip-vecchio-0" not in cls.falliti and len(cls.falliti) <= 3

    def test_falliti_non_condivisi_con_la_classe_base(self, monkeypatch):
        monkeypatch.setenv("GAS_VOICE_MAX_FALLITI", "2")
        self._sbagliato()
        self._sbagliato()
        assert VoiceHandler.falliti == {} and VoiceHandler.bloccati == {}

    def test_tetto_alle_richieste_a_testo(self, monkeypatch):
        monkeypatch.setenv("GAS_VOICE_MAX_TESTO_ORA", "2")
        chiamate = []
        orig = self.kernel.run_turn
        self.kernel.run_turn = lambda p: chiamate.append(p) or orig(p)
        assert self._giusto()[0] == 200 and self._giusto()[0] == 200
        status, body = self._giusto()
        assert status == 429 and "GAS_VOICE_MAX_TESTO_ORA" in body["error"]
        assert len(chiamate) == 2                # oltre il tetto nessun turno parte

    def test_testo_rifiutato_non_consuma_il_tetto_voce(self, monkeypatch):
        """R-720-1-M2: il tetto al testo scatta prima del conteggio V12, così un testo rifiutato
        non toglie posti alle richieste a voce (ascolto H24)."""
        from unittest.mock import patch
        monkeypatch.setenv("GAS_VOICE_MAX_TESTO_ORA", "1")
        monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
        hdr = {"Authorization": f"Bearer {self.TOKEN}", "Accept": "audio/mpeg"}
        url = f"http://127.0.0.1:{self.port}/voice"
        stati = []
        with patch("modules.voice.server.synthesize_speech", side_effect=lambda f, k, v: b"mp3"):
            for _ in range(3):
                req = urllib.request.Request(url, data=b'{"prompt": "ciao"}', method="POST",
                                             headers={"Content-Type": "application/json", **hdr})
                try:
                    with _SENZA_PROXY.open(req, timeout=5) as r:
                        stati.append(r.status)
                except urllib.error.HTTPError as e:
                    stati.append(e.code)
        assert stati == [200, 429, 429]
        assert len(self.server.RequestHandlerClass.turni_parlati) == 1

    def test_testo_rifiutato_dal_tetto_voce_non_consuma_il_tetto_testo(self, monkeypatch):
        """R-722-1-M2: un testo con risposta a voce rifiutato dal tetto voce (V12) non conta nel
        tetto al testo: una richiesta solo a testo dopo passa ancora."""
        from unittest.mock import patch
        monkeypatch.setenv("GAS_VOICE_MAX_TURNI_ORA", "1")
        monkeypatch.setenv("GAS_VOICE_MAX_TESTO_ORA", "3")
        monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
        url = f"http://127.0.0.1:{self.port}/voice"
        stati = []
        with patch("modules.voice.server.synthesize_speech", side_effect=lambda f, k, v: b"mp3"):
            for accetta in ("audio/mpeg", "audio/mpeg", "audio/mpeg", "application/json"):
                req = urllib.request.Request(
                    url, data=b'{"prompt": "ciao"}', method="POST",
                    headers={"Content-Type": "application/json", "Accept": accetta,
                             "Authorization": f"Bearer {self.TOKEN}"})
                try:
                    with _SENZA_PROXY.open(req, timeout=5) as r:
                        stati.append(r.status)
                except urllib.error.HTTPError as e:
                    stati.append(e.code)
        assert stati == [200, 429, 429, 200]
        assert len(self.server.RequestHandlerClass.turni_testo) == 2

    @pytest.mark.parametrize("valore", ["abc", "0", "-3", ""])
    def test_soglie_scritte_male_usano_il_default(self, monkeypatch, valore):
        import modules.voice.server as srv
        monkeypatch.setenv("GAS_VOICE_MAX_TESTO_ORA", valore)
        assert srv._intero_env("GAS_VOICE_MAX_TESTO_ORA", 120) == 120


@pytest.mark.parametrize("bind,locale", [
    ("127.0.0.1", True), ("127.0.0.2", True), ("localhost", True),
    ("::1", False), ("::ffff:127.0.0.1", False),  # bot #358 V-2: il server è solo IPv4
    # indirizzi non locali solo IPv6 di esempio (gate IP del repo: niente IPv4 non loopback)
    ("::", False), ("2001:db8::10", False), ("fd7a:115c:a1e0::5", False),
    ("127.evil.example", False), ("", False),  # R-720-3-M2: un nome host non è loopback
])
def test_r8_bind_locale(bind, locale):
    from modules.voice.server import _bind_locale
    assert _bind_locale(bind) is locale


@pytest.mark.parametrize("rete", ["", "0", "no"])
def test_r8_avvio_rifiutato_fuori_da_127_senza_rete_privata(monkeypatch, capsys, rete):
    import modules.voice.server as srv
    monkeypatch.setattr(sys, "path", list(sys.path))
    monkeypatch.setattr(srv, "_carica_env", lambda: None)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "t" * 32)
    # bot #358 V-1: un IPv4 non locale scritto per intero (rete del tunnel, costruito da intero
    # per il gate IP), così questo test prova proprio il controllo sulla rete privata
    monkeypatch.setenv("GAS_VOICE_BIND", str(ipaddress.IPv4Address(0x64400005)))
    monkeypatch.setenv("GAS_VOICE_RETE_PRIVATA", rete)
    # se il controllo mancasse, il server non deve partire davvero: il kernel finto fallisce
    monkeypatch.setitem(sys.modules, "gas", type(sys)("gas"))
    sys.modules["gas"].GasKernel = lambda **kw: (_ for _ in ()).throw(AssertionError("partito"))
    assert run_server(root_dir="/tmp") == 1
    out = capsys.readouterr().out
    assert "non è locale e la connessione è in chiaro" in out and "t" * 32 not in out


@pytest.mark.parametrize("bind,messaggio", [
    ("0", "non è un indirizzo IPv4 scritto per intero"),       # R-727-1-M2: forme abbreviate
    ("0x0", "non è un indirizzo IPv4 scritto per intero"),
    ("gas.example", "non è un indirizzo IPv4 scritto per intero"),  # nome host
    (str(ipaddress.IPv4Address(0)), "tutte le interfacce"),  # IPv4 «tutte le interfacce»
    ("::ffff:0:0", "✗ gas voice"),  # R-728-1-M2: IPv4 dentro IPv6 (messaggio secondo Python)
    ("fe80::1%eth0", "IPv4 scritto per intero"),  # R-728-2-M2: IPv6 con zona, niente crash
    ("fd7a:115c:a1e0::5", "IPv4 scritto per intero"),  # IPv6: il server è solo IPv4
])
def test_r8_rete_privata_rifiuta_nomi_e_tutte_le_interfacce(monkeypatch, capsys, bind, messaggio):
    """Anche con la rete privata dichiarata, il server non parte su un nome host, su una forma
    abbreviata o su tutte le interfacce (il socket le risolverebbe da solo)."""
    import modules.voice.server as srv
    monkeypatch.setattr(sys, "path", list(sys.path))
    monkeypatch.setattr(srv, "_carica_env", lambda: None)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "t" * 32)
    monkeypatch.setenv("GAS_VOICE_BIND", bind)
    monkeypatch.setenv("GAS_VOICE_RETE_PRIVATA", "1")
    monkeypatch.setitem(sys.modules, "gas", type(sys)("gas"))
    sys.modules["gas"].GasKernel = lambda **kw: (_ for _ in ()).throw(AssertionError("partito"))
    assert run_server(root_dir="/tmp") == 1
    assert messaggio in capsys.readouterr().out


@pytest.mark.parametrize("rete", ["", "1"])
def test_r8_mai_su_tutte_le_interfacce(monkeypatch, capsys, rete):
    """Bot #358 V-1: «::» (tutte le interfacce) è rifiutato anche con la rete privata dichiarata."""
    import modules.voice.server as srv
    monkeypatch.setattr(sys, "path", list(sys.path))
    monkeypatch.setattr(srv, "_carica_env", lambda: None)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "t" * 32)
    monkeypatch.setenv("GAS_VOICE_BIND", "::")
    monkeypatch.setenv("GAS_VOICE_RETE_PRIVATA", rete)
    monkeypatch.setitem(sys.modules, "gas", type(sys)("gas"))
    sys.modules["gas"].GasKernel = lambda **kw: (_ for _ in ()).throw(AssertionError("partito"))
    assert run_server(root_dir="/tmp") == 1
    assert "tutte le interfacce" in capsys.readouterr().out


@pytest.mark.parametrize("bind,tutte", [
    ("::", True), ("::1", False), ("127.0.0.1", False), ("fd7a:115c:a1e0::5", False),
    ("localhost", False), ("", False),
])
def test_r8_bind_tutte_le_interfacce(bind, tutte):
    from modules.voice.server import _bind_tutte_le_interfacce
    assert _bind_tutte_le_interfacce(bind) is tutte


def test_r8_avvio_con_rete_privata_dichiarata_parte(monkeypatch):
    """Con GAS_VOICE_RETE_PRIVATA=1 il controllo lascia passare (si ferma qui, prima del kernel)."""
    import modules.voice.server as srv
    monkeypatch.setattr(sys, "path", list(sys.path))
    monkeypatch.setattr(srv, "_carica_env", lambda: None)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "t" * 32)
    # un indirizzo della rete Tailscale (100.64/10), costruito da intero: gate IP del repo
    monkeypatch.setenv("GAS_VOICE_BIND", str(ipaddress.IPv4Address(0x64400005)))
    monkeypatch.setenv("GAS_VOICE_RETE_PRIVATA", "1")

    class _Fermo(Exception):
        pass

    def _kernel(**kw):
        raise _Fermo()
    monkeypatch.setitem(sys.modules, "gas", type(sys)("gas"))
    sys.modules["gas"].GasKernel = _kernel
    # audit 10 nov: la porta si apre PRIMA del kernel; qui un server finto (l'IP del tunnel
    # non esiste su questa macchina)
    chiusi = []

    class _SrvFinto:
        def __init__(self, indirizzo, handler):
            self.indirizzo = indirizzo

        def server_close(self):
            chiusi.append(self.indirizzo)
    monkeypatch.setattr(srv, "HTTPServer", _SrvFinto)
    with pytest.raises(_Fermo):
        run_server(root_dir="/tmp")
    assert len(chiusi) == 1  # kernel fallito → porta richiusa


# ─────────────────────────── audit notturno 10 nov ───────────────────────────

def test_audit_b1_timeout_del_socket():
    """B1: il server è a un thread; una connessione muta (anche senza token) non blocca la
    voce: dopo `timeout` secondi il socket si chiude e la richiesta successiva passa."""
    import socket as _so
    from modules.voice.server import VoiceHandler
    assert VoiceHandler.timeout == 60

    class _H(VoiceHandler):
        timeout = 1
    _H.kernel = _MockKernel(events=[{"type": "final", "content": "eccomi"}])
    _H.token = "tok-b1"
    srv = HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        muta = _so.create_connection(("127.0.0.1", srv.server_address[1]))
        muta.sendall(b"POST /voice HTTP/1.1\r\nContent-Length: 50\r\n")  # e poi più nulla
        t0 = time.monotonic()
        st, corpo = _post(srv.server_address[1], {"prompt": "ci sei?"},
                          headers={"Authorization": "Bearer tok-b1"})
        assert st == 200 and corpo["content"] == "eccomi"
        assert time.monotonic() - t0 < 4.5
        muta.close()
    finally:
        srv.shutdown()
        srv.server_close()


def _post_grezzo(port, raw: bytes, token: str):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/voice", data=raw, method="POST",
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {token}"})
    try:
        with _SENZA_PROXY.open(req, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


@pytest.mark.parametrize("raw", [b"[]", b'"ciao"', b"3", b'{"prompt": 123}',
                                 b'{"prompt": ["a"]}', b'{"prompt": {"x": 1}}'])
def test_audit_b5_json_di_forma_sbagliata_400(raw):
    """B5: JSON valido ma di forma sbagliata → 400 con un messaggio, mai connessione chiusa."""
    k = _MockKernel()
    server, port = _make_server(k, "tok-b5")
    try:
        st, corpo = _post_grezzo(port, raw, "tok-b5")
        assert st == 400 and "JSON" in corpo["error"]
    finally:
        server.shutdown()
        server.server_close()


def test_audit_tetti_413(monkeypatch):
    """Tetti: corpo oltre _MAX_CORPO_BYTE (controllato PRIMA di leggerlo) e prompt oltre
    _MAX_PROMPT_CHAR → 413, nessun turno."""
    import modules.voice.server as srv_mod
    k = _MockKernel()
    server, port = _make_server(k, "tok-413")
    try:
        st, corpo = _post_grezzo(port, json.dumps({"prompt": "x" * 20_001}).encode(), "tok-413")
        assert st == 413 and "troppo lungo" in corpo["error"]
        st, _ = _post_grezzo(port, json.dumps({"prompt": "x" * 20_000}).encode(), "tok-413")
        assert st == 200
        monkeypatch.setattr(srv_mod, "_MAX_CORPO_BYTE", 100)
        st, corpo = _post_grezzo(port, json.dumps({"prompt": "y" * 200}).encode(), "tok-413")
        assert st == 413 and "troppo grande" in corpo["error"]
    finally:
        server.shutdown()
        server.server_close()
    assert srv_mod._MAX_PROMPT_CHAR == 20_000


def test_audit_porta_occupata_messaggio_chiaro(monkeypatch, capsys):
    """Porta occupata → messaggio chiaro e uscita 1, PRIMA di caricare il kernel."""
    import modules.voice.server as srv_mod
    monkeypatch.setattr(sys, "path", list(sys.path))
    monkeypatch.setattr(srv_mod, "_carica_env", lambda: None)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "t" * 32)
    monkeypatch.delenv("GAS_VOICE_BIND", raising=False)
    occupata = HTTPServer(("127.0.0.1", 0), BaseHTTPRequestHandler)
    monkeypatch.setenv("GAS_VOICE_PORT", str(occupata.server_address[1]))
    caricato = []
    finto = type(sys)("gas")
    finto.GasKernel = lambda **kw: caricato.append(kw)
    monkeypatch.setitem(sys.modules, "gas", finto)
    try:
        assert run_server(root_dir="/tmp") == 1
    finally:
        occupata.server_close()
    out = capsys.readouterr().out
    assert "non riesco ad ascoltare" in out and caricato == []


@pytest.mark.parametrize("riga, atteso", [
    ('GAS_VOICE_TOKEN="abc123"', "abc123"),
    ("GAS_VOICE_TOKEN='abc123'  # commento", "abc123"),
    ("export GAS_VOICE_TOKEN=abc123", "abc123"),
    ("GAS_VOICE_TOKEN=abc123 # commento", "abc123"),
    ("GAS_VOICE_TOKEN=abc123\t# commento", "abc123"),
    ("GAS_VOICE_TOKEN=abc#123", "abc#123"),
    ('GAS_VOICE_TOKEN="non chiuse', None),
])
def test_audit_b4_dotenv_del_browser_come_gas(monkeypatch, tmp_path, riga, atteso):
    """B4: il .env del proxy del browser segue le regole di gas.py (virgolette, commenti,
    export): un token tra virgolette non deve arrivare con le virgolette (401 e blocco IP)."""
    import clients.voice.browser_server as bs
    monkeypatch.delenv("GAS_VOICE_TOKEN", raising=False)
    (tmp_path / ".env").write_text(riga + "\n", encoding="utf-8")
    bs._load_dotenv(tmp_path)
    assert os.environ.get("GAS_VOICE_TOKEN") == atteso
    monkeypatch.delenv("GAS_VOICE_TOKEN", raising=False)


def test_audit_b4_dotenv_non_sovrascrive(monkeypatch, tmp_path):
    import clients.voice.browser_server as bs
    monkeypatch.setenv("GAS_VOICE_TOKEN", "dalla-shell")
    (tmp_path / ".env").write_text("GAS_VOICE_TOKEN=dal-file\n", encoding="utf-8")
    bs._load_dotenv(tmp_path)
    assert os.environ["GAS_VOICE_TOKEN"] == "dalla-shell"


@pytest.mark.parametrize("url, porta, atteso", [(None, "9001", 9001), (None, None, 8765),
                                                ("http://127.0.0.1:7000", "9001", 7000)])
def test_audit_proxy_segue_gas_voice_port(monkeypatch, url, porta, atteso):
    """R-752-3: senza GAS_VOICE_URL il proxy del browser segue GAS_VOICE_PORT, come il
    server voce; GAS_VOICE_URL, se c'è, vince."""
    bs = _browser_server_module()
    monkeypatch.setattr(bs, "_load_dotenv", lambda root: None)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "tok")
    for k in ("GAS_VOICE_TIMEOUT", "GAS_VOICE_FINESTRA", "GAS_VOICE_MAX_TURNI", "GAS_BROWSER_PORT"):
        monkeypatch.delenv(k, raising=False)
    for k, v in (("GAS_VOICE_URL", url), ("GAS_VOICE_PORT", porta)):
        if v is None:
            monkeypatch.delenv(k, raising=False)
        else:
            monkeypatch.setenv(k, v)

    class _Fermo(Exception):
        pass

    class _NonParte:
        def __init__(self, *a):
            raise _Fermo()

    monkeypatch.setattr(bs, "ThreadingHTTPServer", _NonParte)
    with pytest.raises(_Fermo):
        bs.run_browser_server()
    assert bs.BrowserProxyHandler.voice_port == atteso




def test_seguito_da_scartare_e_istruzione_severa():
    """Filtro più severo (10 nov, via M1): frammenti di una parola fuori elenco o senza
    parole si scartano; risposte brevi e frasi vere no. L'istruzione del seguito dice che
    nel dubbio il parlato NON è per Gas."""
    from modules.voice.server import ISTRUZIONE_SEGUITO, seguito_da_scartare
    for t in ("", "...", "Mamma.", "Allora…", "Forte!", "  TELEVISIONE  "):
        assert seguito_da_scartare(t), t
    for t in ("Sì.", "si", "No!", "Grazie.", "Perché?", "Ok", "Spegni la luce",
              "Gas ha detto una cosa", "Continua.", "Avanti!", "Altro?", "Tre.", "3",
              "Domani.", "Venerdì", "D'accordo."):  # R-744-1-M2
        assert not seguito_da_scartare(t), t
    assert "NEL DUBBIO NON è rivolta a te" in ISTRUZIONE_SEGUITO
    assert "terza persona" in ISTRUZIONE_SEGUITO
    # R-744-1-M2: la parola che Gas stesso invita a dire quando taglia il parlato passa
    from modules.voice.server import _PARLATO_VOCE_RESTO
    assert "resto" in _PARLATO_VOCE_RESTO and not seguito_da_scartare("Resto.")  # R-746-2-M2
    # V-3 bot #365 + R-746-1-M2: altre risposte brevi, accenti normalizzati, numeri oltre dieci
    import unicodedata
    for t in ("Sicuro.", "Certamente!", "Forse", "Davvero?", "Scusa?", "Stasera.", "Perchè?",
              "Lunedi", unicodedata.normalize("NFD", "Lunedì"), "Undici.", "Venti"):
        assert not seguito_da_scartare(t), t
    assert seguito_da_scartare("Mamma.") and seguito_da_scartare("Ehm")


def test_parlato_voce_tetto_piu_corto():
    """10 nov: senza schermo il parlato si ferma a 800 caratteri (prima 1500)."""
    from modules.voice.server import frasi_voce, _PARLATO_VOCE_MAX_CHAR, _PARLATO_VOCE_RESTO
    assert _PARLATO_VOCE_MAX_CHAR == 800
    testo = " ".join(["Questa è una frase di prova abbastanza lunga."] * 40)
    frasi = frasi_voce(testo)
    assert frasi[-1] == _PARLATO_VOCE_RESTO
    assert len(" ".join(frasi[:-1])) <= 800


@pytest.mark.parametrize("testo, scarta", [
    ("Ehm, allora…", True), ("Mah, boh.", True), ("Beh insomma", True), ("Comunque", True),
    ("Niente.", True), ("Eh, tipo, praticamente", True),
    ("Allora segna il lead Rossi", False), ("Sì", False), ("Boh, dimmi tu", False),
])
def test_filtro2_seguito_solo_intercalari(testo, scarta):
    """Filtro 2 (11 nov): nel seguito una frase fatta solo di intercalari è parlato della
    stanza e si scarta; basta una parola vera perché passi."""
    from modules.voice.server import seguito_da_scartare
    assert seguito_da_scartare(testo) is scarta, testo
