"""
V6 (chat M2, «capire meglio»): i turni a voce vedono la conversazione.

Test di integrazione SENZA token LLM: server della voce vero + GasKernel vero, con il
cervello forte (`claude -p`) e il cervello normale finti al confine (runner del
subprocess / client OpenAI). Si verifica che al secondo turno parlato il cervello riceva
anche il primo scambio (domanda trascritta e risposta), non solo l'ultima frase.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
from http.server import HTTPServer
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import gas  # noqa: E402
from brains.claude_cli import ClaudeCliClient  # noqa: E402
from modules.voice.server import VoiceHandler  # noqa: E402

_TOKEN = "tok-contesto-v6"
_AUTH = {"Authorization": f"Bearer {_TOKEN}"}
_ENV_PULITO = ("GEMINI_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY", "GAS_OLLAMA_URL",
               "GAS_CLAUDE_CLI", "GAS_VOCE_FORTE", "ELEVENLABS_API_KEY", "GAS_VOICE_MAX_TURNI_ORA",
               "ANTHROPIC_API_KEY", "GAS_CWD")


@pytest.fixture
def ambiente():
    salvate = {k: os.environ.get(k) for k in _ENV_PULITO}
    for k in _ENV_PULITO:
        os.environ.pop(k, None)
    tmp = tempfile.mkdtemp(prefix="gas_test_voce_ctx_")
    subprocess.run(["git", "init", "-q", tmp], check=True, capture_output=True)
    os.environ["GAS_CWD"] = tmp
    try:
        yield tmp
    finally:
        for k, v in salvate.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def _server(kernel: Any) -> tuple[HTTPServer, int]:
    class _H(VoiceHandler):
        pass
    _H.kernel = kernel
    _H.token = _TOKEN
    srv = HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def _parla(port: int) -> Dict[str, Any]:
    import urllib.request
    wav = b"RIFF" + bytes(60)
    req = urllib.request.Request(f"http://127.0.0.1:{port}/voice", data=wav, method="POST",
                                 headers={**_AUTH, "Content-Type": "audio/wav"})
    with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=30) as r:
        return json.loads(r.read())


def test_v6_il_forte_riceve_la_conversazione_a_voce(ambiente):
    """Con GAS_VOCE_FORTE=1 il secondo turno parlato manda a `claude -p` anche la prima
    domanda e la prima risposta: il «sì» ha il suo contesto."""
    stdin_visti: List[str] = []
    risposte = iter(["Ho trovato 3 lead nuovi. Preparo le bozze?", "Fatto: 3 bozze pronte."])

    def _run(cmd, stdin, cwd, env, timeout):
        stdin_visti.append(stdin)
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps({
            "type": "result", "subtype": "success", "is_error": False,
            "structured_output": {"testo": next(risposte), "chiamate": []},
            "usage": {"input_tokens": 10, "output_tokens": 3}}), stderr="")

    os.environ.update({"GAS_CLAUDE_CLI": "1", "GAS_VOCE_FORTE": "1", "GROQ_API_KEY": "k"})
    kernel = gas.GasKernel(root_dir=ambiente)
    srv, port = _server(kernel)
    finto = lambda timeout=None: ClaudeCliClient(timeout=timeout, binario="claude", runner=_run)  # noqa: E731
    try:
        with patch.object(gas, "ClaudeCliClient", finto), \
             patch("modules.voice.server.transcribe_audio",
                   side_effect=["Gas, ci sono lead nuovi oggi?", "sì"]):
            primo = _parla(port)
            secondo = _parla(port)
    finally:
        srv.shutdown()
        srv.server_close()
    assert primo["content"] == "Ho trovato 3 lead nuovi. Preparo le bozze?"
    assert secondo["content"] == "Fatto: 3 bozze pronte."
    assert len(stdin_visti) == 2
    assert "ci sono lead nuovi oggi?" in stdin_visti[1]
    assert "Preparo le bozze?" in stdin_visti[1]
    assert stdin_visti[1].rstrip().count("<utente_") >= 2


def test_v6_il_cervello_normale_riceve_la_conversazione_a_voce(ambiente):
    """Senza il forte: anche il cervello normale (qui Gemini finto) riceve la storia."""
    visti: List[List[Dict[str, Any]]] = []
    risposte = iter(["Domani alle 10 hai la call con Rossi.", "Sì, alle 10 in punto."])

    class _Comp:
        def create(self, model=None, messages=None, tools=None, tool_choice=None, **kw):
            visti.append(messages)
            msg = SimpleNamespace(content=next(risposte), tool_calls=None, role="assistant")
            return SimpleNamespace(choices=[SimpleNamespace(message=msg, finish_reason="stop")],
                                   usage=None, model=model)

    class _OpenAI:
        def __init__(self, *a, **kw):
            self.chat = SimpleNamespace(completions=_Comp())

    os.environ.update({"GEMINI_API_KEY": "dummy-for-test", "GROQ_API_KEY": "k"})
    kernel = gas.GasKernel(root_dir=ambiente)
    srv, port = _server(kernel)
    try:
        with patch.object(gas, "OpenAI", _OpenAI), \
             patch("modules.voice.server.transcribe_audio",
                   side_effect=["cosa ho domani?", "a che ora?"]):
            primo = _parla(port)
            secondo = _parla(port)
    finally:
        srv.shutdown()
        srv.server_close()
    assert primo["content"].startswith("Domani alle 10")
    assert secondo["content"] == "Sì, alle 10 in punto."
    ultimo = visti[-1]
    testi = [str(m.get("content")) for m in ultimo if m.get("role") != "system"]
    assert "cosa ho domani?" in testi and "a che ora?" in testi
    assert any("call con Rossi" in t for t in testi)
    assert ultimo[0]["role"] == "system"
