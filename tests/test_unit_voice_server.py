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
