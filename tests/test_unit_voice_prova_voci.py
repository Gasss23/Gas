"""
V8 (chat M2) — pagina «prova voci»: elenco delle voci, prova con una frase fissa, scelta.

Zero rete e zero token: ElevenLabs e Piper sono sempre finti. I test della pagina nel
browser girano con Node + Playwright (obbligatori in CI con GAS_TEST_BROWSER_OBBLIGATORIO=1).
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.voice import prova_voci  # noqa: E402
from modules.voice.server import VoiceHandler  # noqa: E402
from modules.voice.tts import ElevenLabsTTSError, list_voices  # noqa: E402

_SENZA_PROXY = urllib.request.build_opener(urllib.request.ProxyHandler({}))
_TOKEN = "tok-voci"

_VOCI = [
    {"id": "Allegra0000000001", "nome": "Allegra", "categoria": "premade", "genere": "female",
     "accento": "american", "eta": "young", "descrizione": "upbeat"},
    {"id": "George00000000001", "nome": "George", "categoria": "premade", "genere": "male",
     "accento": "british", "eta": "middle aged", "descrizione": "warm"},
    {"id": "Clone000000000001", "nome": "Io stesso", "categoria": "cloned", "genere": "male",
     "accento": "british", "eta": "middle aged", "descrizione": "calm"},
    {"id": "../../v1/user", "nome": "Strana", "categoria": "premade", "genere": "male",
     "accento": "british", "eta": "old", "descrizione": "calm"},
    {"id": "Brian000000000001", "nome": "Brian", "categoria": "premade", "genere": "male",
     "accento": "american", "eta": "middle aged", "descrizione": "deep"},
    {"id": "Famosa00000000001", "nome": "Attore", "categoria": "famous", "genere": "male",
     "accento": "british", "eta": "old", "descrizione": "calm"},
    {"id": "Nuova000000000001", "nome": "Ignota", "categoria": "nuovacategoria", "genere": "male",
     "accento": "british", "eta": "old", "descrizione": "calm"},
    {"id": "Pro00000000000001", "nome": "Pro", "categoria": "professional", "genere": "female",
     "accento": "italian", "eta": "young", "descrizione": ""},
]


# ── logica pura ──

def test_ordina_voci_candidate_prima_senza_clonate_ne_id_strani():
    """R-624-1-M2: solo categorie ammesse (fuori clonate, «famous» e categorie nuove)."""
    out = prova_voci.ordina_voci(_VOCI, attuale="Brian000000000001")
    assert [v["nome"] for v in out] == ["George", "Brian", "Allegra", "Pro"]
    assert out[0]["candidata"] is True and out[1]["candidata"] is False
    assert [v["attuale"] for v in out] == [False, True, False, False]


@pytest.mark.parametrize("voce, ok", [("JBFqnCBsd6RMkjVDRZzb", True), ("abc", False),
                                      ("../v1/user", False), ("a" * 41, False), (None, False),
                                      ("piper", False)])
def test_voce_valida(voce, ok):
    assert prova_voci.voce_valida(voce) is ok


def test_piper_non_disponibile_senza_modello(monkeypatch, tmp_path):
    monkeypatch.delenv("GAS_PIPER_MODEL", raising=False)
    assert prova_voci.piper_disponibile() is None
    monkeypatch.setenv("GAS_PIPER_MODEL", str(tmp_path / "manca.onnx"))
    assert prova_voci.piper_disponibile() is None


def test_piper_finto_parla(monkeypatch, tmp_path):
    """Piper finto sul PATH: riceve il testo su stdin (mai nella riga di comando) e scrive
    il WAV nel file chiesto."""
    cartella = tmp_path / "bin"
    cartella.mkdir()
    finto = cartella / "piper"
    finto.write_text("#!/bin/sh\n"
                     "out=\"\"; while [ $# -gt 0 ]; do [ \"$1\" = --output_file ] && out=\"$2\"; shift; done\n"
                     "printf 'RIFF' > \"$out\"; cat >> \"$out\"\n")
    finto.chmod(0o755)
    modello = tmp_path / "it.onnx"
    modello.write_bytes(b"x")
    monkeypatch.setenv("PATH", f"{cartella}{os.pathsep}{os.environ.get('PATH', '')}")
    monkeypatch.setenv("GAS_PIPER_MODEL", str(modello))
    assert prova_voci.piper_disponibile() == str(modello)
    assert prova_voci.sintetizza_piper("Ciao.", str(modello)) == b"RIFFCiao."


# ── tts.list_voices ──

class _Resp:
    def __init__(self, status, body):
        self.status, self._b = status, body

    def read(self):
        return self._b


class _Conn:
    def __init__(self, status, body):
        self.r = _Resp(status, body)
        self.richiesta = None

    def request(self, metodo, percorso, headers=None, body=None):
        self.richiesta = (metodo, percorso, headers)

    def getresponse(self):
        return self.r

    def close(self):
        pass


def test_list_voices_campi_utili():
    corpo = json.dumps({"voices": [
        {"voice_id": "George00000000001", "name": "George", "category": "premade",
         "labels": {"gender": "male", "accent": "british", "age": "middle aged",
                    "description": "warm"}},
        {"name": "senza id"}, "rotta"]}).encode()
    conn = _Conn(200, corpo)
    voci = list_voices("k", _conn_factory=lambda: conn)
    assert voci == [{"id": "George00000000001", "nome": "George", "categoria": "premade",
                     "genere": "male", "accento": "british", "eta": "middle aged",
                     "descrizione": "warm"}]
    assert conn.richiesta[:2] == ("GET", "/v1/voices") and conn.richiesta[2]["xi-api-key"] == "k"


@pytest.mark.parametrize("status, corpo", [(401, b'{"detail": "no"}'), (200, b"<html>"),
                                           (200, b'{"voices": 5}'), (200, b"[1, 2]")])
def test_list_voices_errori(status, corpo):
    with pytest.raises(ElevenLabsTTSError):
        list_voices("k", _conn_factory=lambda: _Conn(status, corpo))


# ── server voce: GET /voci/elenco e POST /voci/prova ──

@pytest.fixture
def server():
    class _H(VoiceHandler):
        pass
    _H.kernel = None
    _H.token = _TOKEN
    _H.prove_voci = []
    _H.voci_ammesse = frozenset({"George00000000001"})   # come dopo aver aperto l'elenco
    srv = HTTPServer(("127.0.0.1", 0), _H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        yield srv.server_address[1]
    finally:
        srv.shutdown()
        srv.server_close()


def _chiama(port, metodo, percorso, body=None, token=_TOKEN):
    dati = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"http://127.0.0.1:{port}{percorso}", data=dati, method=metodo,
                                 headers={"Authorization": f"Bearer {token}",
                                          **({"Content-Type": "application/json"} if dati else {})})
    try:
        with _SENZA_PROXY.open(req, timeout=10) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), e.read()


def test_elenco_voci(server, monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    monkeypatch.setenv("ELEVENLABS_VOICE_ID", "Brian000000000001")
    monkeypatch.delenv("GAS_PIPER_MODEL", raising=False)
    with patch("modules.voice.server.list_voices", return_value=_VOCI):
        st, ct, corpo = _chiama(server, "GET", "/voci/elenco")
    dati = json.loads(corpo)
    assert st == 200 and dati["attuale"] == "Brian000000000001" and dati["piper"] is False
    assert [v["nome"] for v in dati["voci"]] == ["George", "Brian", "Allegra", "Pro"]
    assert dati["frasi"] == list(prova_voci.FRASI_PROVA)
    # R-624-1-M2: dopo l'elenco si provano le voci elencate, non le escluse
    with patch("modules.voice.server.synthesize_speech", return_value=b"x") as tts:
        assert _chiama(server, "POST", "/voci/prova", {"voce": "Brian000000000001", "frase": 0})[0] == 200
        assert _chiama(server, "POST", "/voci/prova", {"voce": "Famosa00000000001", "frase": 0})[0] == 409
        assert _chiama(server, "POST", "/voci/prova", {"voce": "Clone000000000001", "frase": 0})[0] == 409
    assert tts.call_count == 1


def test_elenco_senza_token_o_chiave(server, monkeypatch):
    assert _chiama(server, "GET", "/voci/elenco", token="sbagliato")[0] == 401
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    st, _, corpo = _chiama(server, "GET", "/voci/elenco")
    assert st == 200 and "ELEVENLABS_API_KEY" in json.loads(corpo)["errore"]
    assert _chiama(server, "GET", "/altro")[0] == 405


def test_elenco_errore_elevenlabs(server, monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    with patch("modules.voice.server.list_voices", side_effect=OSError("rete")):
        st, _, corpo = _chiama(server, "GET", "/voci/elenco")
    assert st == 200 and json.loads(corpo)["voci"] == [] and "rete" in json.loads(corpo)["errore"]


def test_prova_voce_frase_fissa(server, monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    with patch("modules.voice.server.synthesize_speech", return_value=b"ID3mp3") as tts:
        st, ct, corpo = _chiama(server, "POST", "/voci/prova", {"voce": "George00000000001", "frase": 2})
    assert st == 200 and ct == "audio/mpeg" and corpo == b"ID3mp3"
    assert tts.call_args.args[0] == prova_voci.FRASI_PROVA[2]
    assert tts.call_args.args[2] == "George00000000001"


@pytest.mark.parametrize("body", [{"voce": "../../v1/user", "frase": 0}, {"voce": "George00000000001", "frase": 9},
                                  {"voce": "George00000000001", "frase": True},
                                  {"voce": "George00000000001", "frase": "0"}, {"testo": "dimmi altro"}])
def test_prova_voce_rifiuta_richieste_strane(server, monkeypatch, body):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    with patch("modules.voice.server.synthesize_speech", return_value=b"x") as tts:
        st, _, _ = _chiama(server, "POST", "/voci/prova", body)
    assert st == 400 and tts.call_count == 0


def test_prova_voce_non_elencata_rifiutata(server, monkeypatch):
    """R-624-1-M2: un id valido ma mai mostrato nell'elenco (es. una voce clonata scritta
    a mano) non si prova."""
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    with patch("modules.voice.server.synthesize_speech", return_value=b"x") as tts:
        st, _, corpo = _chiama(server, "POST", "/voci/prova", {"voce": "Scritta0000000001", "frase": 0})
    assert st == 409 and "elenco" in json.loads(corpo)["error"] and tts.call_count == 0


def test_prova_voce_tetto_orario(server, monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    monkeypatch.setenv("GAS_VOICE_MAX_PROVE_ORA", "2")
    with patch("modules.voice.server.synthesize_speech", return_value=b"x") as tts:
        stati = [_chiama(server, "POST", "/voci/prova", {"voce": "George00000000001", "frase": 0})[0]
                 for _ in range(3)]
    assert stati == [200, 200, 429] and tts.call_count == 2


def test_prova_voce_senza_token_o_chiave(server, monkeypatch):
    assert _chiama(server, "POST", "/voci/prova", {"voce": "George00000000001", "frase": 0},
                   token="no")[0] == 401
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    assert _chiama(server, "POST", "/voci/prova", {"voce": "George00000000001", "frase": 0})[0] == 503


def test_prova_voce_errore_elevenlabs(server, monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    with patch("modules.voice.server.synthesize_speech", side_effect=ElevenLabsTTSError(404, "voce assente")):
        st, _, corpo = _chiama(server, "POST", "/voci/prova", {"voce": "George00000000001", "frase": 0})
    assert st == 502 and "voce assente" in json.loads(corpo)["error"]


def test_prova_piper(server, monkeypatch, tmp_path):
    monkeypatch.delenv("GAS_PIPER_MODEL", raising=False)
    assert _chiama(server, "POST", "/voci/prova", {"voce": "piper", "frase": 0})[0] == 503
    with patch("modules.voice.prova_voci.piper_disponibile", return_value="m.onnx"), \
         patch("modules.voice.prova_voci.sintetizza_piper", return_value=b"RIFFwav") as pip:
        st, ct, corpo = _chiama(server, "POST", "/voci/prova", {"voce": "piper", "frase": 1})
    assert st == 200 and ct == "audio/wav" and corpo == b"RIFFwav"
    assert pip.call_args.args[0] == prova_voci.FRASI_PROVA[1]
    with patch("modules.voice.prova_voci.piper_disponibile", return_value="m.onnx"), \
         patch("modules.voice.prova_voci.sintetizza_piper", side_effect=subprocess.CalledProcessError(1, "piper")):
        assert _chiama(server, "POST", "/voci/prova", {"voce": "piper", "frase": 1})[0] == 502


# ── proxy della pagina ──

def _browser_server_module():
    percorso = Path(__file__).parent.parent / "clients" / "voice" / "browser_server.py"
    spec = importlib.util.spec_from_file_location("gas_browser_server_voci", percorso)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def proxy_e_voce():
    """Proxy vero + server voce finto che registra le richieste (col token)."""
    viste = []

    class _Voce(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _rispondi(self, tipo, corpo):
            self.send_response(200)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)

        def do_GET(self):
            viste.append(("GET", self.path, self.headers.get("Authorization"), b""))
            self._rispondi("application/json", json.dumps({
                "voci": [{"id": "George00000000001", "nome": "George <b>x</b>", "genere": "male",
                          "accento": "british", "candidata": True, "attuale": False},
                         {"id": "Brian000000000001", "nome": "Brian", "candidata": False,
                          "attuale": True}],
                "attuale": "Brian000000000001", "frasi": list(prova_voci.FRASI_PROVA),
                "piper": True}).encode())

        def do_POST(self):
            corpo = self.rfile.read(int(self.headers.get("Content-Length", 0) or 0))
            viste.append(("POST", self.path, self.headers.get("Authorization"), corpo))
            self._rispondi("audio/wav", _wav_breve())

    voce = HTTPServer(("127.0.0.1", 0), _Voce)
    threading.Thread(target=voce.serve_forever, daemon=True).start()
    bs = _browser_server_module()

    class _Proxy(bs.BrowserProxyHandler):
        pass
    _Proxy.token = "tok"
    _Proxy.voice_host = "127.0.0.1"
    _Proxy.voice_port = voce.server_address[1]
    proxy = bs.ThreadingHTTPServer(("127.0.0.1", 0), _Proxy)
    threading.Thread(target=proxy.serve_forever, daemon=True).start()
    try:
        yield proxy.server_address[1], viste
    finally:
        proxy.shutdown()
        proxy.server_close()
        voce.shutdown()
        voce.server_close()


@pytest.mark.parametrize("origine, atteso", [(None, 200), ("same", 200),
                                             ("https://sito-cattivo.example", 403)])
def test_proxy_rifiuta_altre_pagine(proxy_e_voce, origine, atteso):
    """R-624-4-M2: una POST mandata da un'altra pagina aperta nel browser (Origin diverso)
    non arriva al server voce; la pagina stessa e i client senza Origin sì."""
    port, viste = proxy_e_voce
    hdrs = {"Content-Type": "application/json"}
    if origine == "same":
        hdrs["Origin"] = f"http://127.0.0.1:{port}"
    elif origine:
        hdrs["Origin"] = origine
    for percorso in ("/voci/prova", "/voice"):
        req = urllib.request.Request(f"http://127.0.0.1:{port}{percorso}", method="POST",
                                     data=b'{"voce": "George00000000001", "frase": 0}', headers=hdrs)
        try:
            with _SENZA_PROXY.open(req, timeout=5) as r:
                st = r.status
        except urllib.error.HTTPError as e:
            st = e.code
        assert st == atteso, (percorso, st)
    if atteso == 403:
        assert viste == []


@pytest.mark.parametrize("host, atteso", [("127.0.0.1", 200), ("localhost", 200),
                                         ("evil.example", 403)])
def test_proxy_solo_host_locale(proxy_e_voce, host, atteso):
    """R-625-1-M2: contro il DNS rebinding il proxy risponde solo se la richiesta nomina
    questo computer (Host 127.0.0.1/localhost con la sua porta), su GET e POST."""
    import http.client as hc
    port, viste = proxy_e_voce
    for metodo, percorso, corpo in (("GET", "/voci", None), ("GET", "/config", None),
                                    ("POST", "/voci/prova", b'{"voce": "George00000000001", "frase": 0}')):
        c = hc.HTTPConnection("127.0.0.1", port, timeout=5)
        c.putrequest(metodo, percorso, skip_host=True)
        c.putheader("Host", f"{host}:{port}")
        c.putheader("Origin", f"http://{host}:{port}")
        if corpo:
            c.putheader("Content-Type", "application/json")
            c.putheader("Content-Length", str(len(corpo)))
        c.endheaders(corpo)
        st = c.getresponse().status
        c.close()
        assert st == atteso, (metodo, percorso, st)
    if atteso == 403:
        assert viste == []


def test_elenco_fallito_azzera_le_voci_ammesse(server, monkeypatch):
    """R-625-2-M2: se l'elenco fallisce non resta valido quello vecchio."""
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    with patch("modules.voice.server.list_voices", side_effect=OSError("rete")):
        _chiama(server, "GET", "/voci/elenco")
    with patch("modules.voice.server.synthesize_speech", return_value=b"x") as tts:
        assert _chiama(server, "POST", "/voci/prova", {"voce": "George00000000001", "frase": 0})[0] == 409
    assert tts.call_count == 0


def _wav_breve():
    import io
    import wave
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(bytes(3200))
    return buf.getvalue()


def test_proxy_pagina_elenco_e_prova(proxy_e_voce):
    port, viste = proxy_e_voce
    with _SENZA_PROXY.open(f"http://127.0.0.1:{port}/voci", timeout=5) as r:
        assert r.status == 200 and b"Prova voci" in r.read()
    with _SENZA_PROXY.open(f"http://127.0.0.1:{port}/voci/elenco", timeout=5) as r:
        assert json.loads(r.read())["attuale"] == "Brian000000000001"
    req = urllib.request.Request(f"http://127.0.0.1:{port}/voci/prova", method="POST",
                                 data=b'{"voce": "George00000000001", "frase": 1}',
                                 headers={"Content-Type": "application/json"})
    with _SENZA_PROXY.open(req, timeout=5) as r:
        assert r.headers.get("Content-Type") == "audio/wav" and r.read()[:4] == b"RIFF"
    assert [(m, p, a) for m, p, a, _ in viste] == [("GET", "/voci/elenco", "Bearer tok"),
                                                   ("POST", "/voci/prova", "Bearer tok")]
    assert json.loads(viste[1][3]) == {"voce": "George00000000001", "frase": 1}


_GUIDA_VOCI_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [url] = process.argv.slice(2);
  let browser;
  try {
    browser = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  } catch (e) { console.log('BROWSER_NON_DISPONIBILE ' + e.message); return; }
  const page = await browser.newPage();
  const errori = [];
  page.on('pageerror', e => errori.push(String(e)));
  await page.goto(url);
  await page.waitForSelector('#voci li');
  const righe = await page.$$eval('#voci li', ls => ls.map(l => ({
    testo: l.textContent, candidata: l.classList.contains('candidata'), html: l.innerHTML })));
  await page.selectOption('#frase', '1');
  await page.click('#voci li:first-child button:has-text("ascolta")');
  await page.waitForFunction(() => document.getElementById('stato').textContent.startsWith('parla'));
  await page.click('#voci li:first-child button:has-text("scelgo questa")');
  const scelta = await page.textContent('#riga');
  const visibile = await page.isVisible('#scelta');
  await page.click('#voci li:last-child button:has-text("scelgo questa")');
  const sceltaPiper = await page.textContent('#riga');
  await browser.close();
  console.log(JSON.stringify({ righe, scelta, visibile, sceltaPiper, errori }));
})().catch(e => { console.error(e); process.exit(1); });
"""


def test_pagina_prova_voci_nel_browser(proxy_e_voce, tmp_path):
    obbligatorio = os.environ.get("GAS_TEST_BROWSER_OBBLIGATORIO") == "1"
    if not shutil.which("node") or subprocess.run(
            ["node", "-e", "require('playwright')"], capture_output=True).returncode != 0:
        if obbligatorio:
            pytest.fail("node + playwright richiesti (GAS_TEST_BROWSER_OBBLIGATORIO=1) ma assenti")
        pytest.skip("node + playwright non disponibili")
    port, viste = proxy_e_voce
    guida = tmp_path / "guida_voci.js"
    guida.write_text(_GUIDA_VOCI_JS)
    r = subprocess.run(["node", str(guida), f"http://127.0.0.1:{port}/voci"],
                       capture_output=True, text=True, timeout=60)
    if "BROWSER_NON_DISPONIBILE" in r.stdout:
        if obbligatorio:
            pytest.fail("Chromium richiesto ma non avviabile: " + r.stdout[-300:])
        pytest.skip("Chromium non disponibile")
    assert r.returncode == 0, (r.stdout[-1500:], r.stderr[-1500:])
    esito = json.loads(r.stdout.strip().splitlines()[-1])
    assert esito["errori"] == []
    righe = esito["righe"]
    assert len(righe) == 3 and righe[0]["candidata"] and "Piper" in righe[2]["testo"]
    assert "George <b>x</b>" in righe[0]["testo"] and "<b>x</b>" not in righe[0]["html"]  # solo testo
    assert "in uso" in righe[1]["testo"]
    assert esito["visibile"] and esito["scelta"] == "ELEVENLABS_VOICE_ID=George00000000001"
    assert "Piper" in esito["sceltaPiper"] and "ELEVENLABS_VOICE_ID" not in esito["sceltaPiper"]
    prova = [json.loads(c) for m, p, a, c in viste if m == "POST"]
    assert prova == [{"voce": "George00000000001", "frase": 1}]
