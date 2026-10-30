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
            assert json.loads(r.read()) == {"finestra": 7.5, "max_turni": 5}
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


def _wav(percorso, pezzi, rate=16000):
    """WAV mono 16 bit: pezzi = [(secondi, ampiezza)], ampiezza 0 = silenzio."""
    import math
    import struct
    import wave
    with wave.open(str(percorso), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        frames = bytearray()
        for secondi, amp in pezzi:
            for i in range(int(secondi * rate)):
                v = amp * math.sin(2 * math.pi * 220 * i / rate) if amp else 0.0
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
    return t.includes('conversazione chiusa') || t.includes('non riproducibile');
  }, null, { timeout: 25000 });
  await page.waitForTimeout(3000);   // niente turni né errori dopo la chiusura
  const stati = await page.evaluate(() => window.__stati);
  const testo = await page.textContent('#testo');
  await browser.close();
  console.log(JSON.stringify({ stati, testo, errori }));
})().catch(async e => {
  console.error(e);
  try { console.error('STATI', JSON.stringify(await globalThis.__pagina.evaluate(() => window.__stati))); } catch (_) {}
  process.exit(1);
});
"""


@pytest.mark.parametrize("modo", ["normale", "riascolto", "pausa", "tetto", "errore"])
def test_v3_conversazione_nel_browser(tmp_path, modo):
    """Giro completo nella pagina vera (Chromium headless, microfono finto da file):
    clic → la frase parte da sola alla fine della voce (nessun secondo clic) → «ci sto
    ragionando» dopo 2 s → risposta a schermo e a voce → la finestra si riapre → resta
    zitto → conversazione chiusa. Saltato se Playwright/Chromium non ci sono (CI)."""
    import base64
    import shutil
    import subprocess
    import time
    if not shutil.which("node") or subprocess.run(
            ["node", "-e", "require('playwright')"], capture_output=True).returncode != 0:
        pytest.skip("node + playwright non disponibili")

    microfono = tmp_path / "mic.wav"
    _wav(microfono, [(0.8, 0), (1.5, 0.4), (6, 0)])
    risposta = tmp_path / "risposta.wav"
    _wav(risposta, [(2.0 if modo == "pausa" else 0.4, 0.2)])
    audio_b64 = base64.b64encode(
        b"non-audio" * 50 if modo == "errore" else risposta.read_bytes()).decode()
    ricevute = []

    from http.server import BaseHTTPRequestHandler

    class _VoceFinta(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0) or 0)
            ricevute.append((self.headers.get("X-Gas-Formato"), self.headers.get("Content-Type"),
                             len(self.rfile.read(n))))
            time.sleep(2.6)  # oltre i 2 s: deve partire la frase d'attesa
            out = json.dumps({"content": "Sì, meglio così. Procedo?", "audio": audio_b64}).encode()
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
        pytest.skip("Chromium non disponibile")
    assert r.returncode == 0, (r.stdout[-2000:], r.stderr[-2000:])
    esito = json.loads(r.stdout.strip().splitlines()[-1])
    stati, testo = esito["stati"], esito["testo"]
    assert esito["errori"] == [], esito["errori"][:3]
    assert len(ricevute) == 1, (ricevute, stati)
    assert ricevute[0][0] == "audio+testo" and ricevute[0][2] > 0
    assert testo == "Sì, meglio così. Procedo?"
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
