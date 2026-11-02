"""Voce H24 (R8, chat Mani): clients/voice/ascolto.py con microfono, rilevatore e server
finti (nessun audio vero), più i file di scripts/voce/."""
import http.server
import io
import json
import logging
import os
import plistlib
import stat
import subprocess
import sys
import threading
import wave
from pathlib import Path

import pytest

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RADICE))
from clients.voice import ascolto as a  # noqa: E402

TOKEN = "tok-SEGRETO-ascolto-123"
SILENZIO = [10] * a.BLOCCO           # rumore di fondo, sotto la soglia della voce
VOCE = [2000] * a.BLOCCO             # voce
PAROLA = "PAROLA"                    # blocco che il rilevatore finto riconosce


def _blocchi(*pezzi):
    """Sequenza di blocchi: (blocco, quante volte) o un blocco singolo."""
    for p in pezzi:
        b, n = p if isinstance(p, tuple) else (p, 1)
        for _ in range(n):
            yield b


def _sec(s):
    return int(round(s / a.SEC_BLOCCO))


class Finti:
    def __init__(self, esito=(True, b"MP3", "")):
        self.inviati, self.riprodotti, self.bip, self.svuotati, self.azzerati = [], [], [], 0, 0
        self.esito = esito

    def rilevatore(self, b):
        return 1.0 if b == PAROLA else 0.0

    def invia(self, wav):
        self.inviati.append(wav)
        return self.esito

    def riproduci(self, audio):
        self.riprodotti.append(audio)

    def suona(self, tipo):
        self.bip.append(tipo)

    def svuota(self):
        self.svuotati += 1

    def azzera(self):
        self.azzerati += 1

    def ascolto(self, blocchi, **k):
        return a.Ascolto(iter(blocchi), self.rilevatore, self.invia, self.riproduci, self.suona,
                         svuota=self.svuota, azzera_rilevatore=self.azzera, **k)


def _campioni(wav):
    with wave.open(io.BytesIO(wav)) as w:
        assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, a.FREQ)
        return w.getnframes()


# ── privacy: prima della parola niente esce ──

def test_senza_parola_niente_invio():
    f = Finti()
    f.ascolto(_blocchi((VOCE, 500), (SILENZIO, 50))).gira()
    assert f.inviati == [] and f.riprodotti == [] and f.bip == []


def test_parola_bip_registrazione_e_risposta():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (SILENZIO, 3), (VOCE, 20), (SILENZIO, 30)),
              finestra_s=0).gira()
    assert f.bip == ["ok"] and f.riprodotti == [b"MP3"] and len(f.inviati) == 1
    # niente silenzio prima della voce; dopo, il silenzio che chiude la richiesta (0,8 s)
    assert _campioni(f.inviati[0]) == (20 + _sec(0.8)) * a.BLOCCO
    assert f.svuotati >= 2 and f.azzerati == 1  # svuota dopo bip e risposta; azzera a fine


def test_se_non_parli_dopo_la_parola_non_si_invia():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (SILENZIO, _sec(a.ATTESA_VOCE_S) + 5), (VOCE, 30))).gira()
    assert f.bip == ["ok"] and f.inviati == []


def test_un_clic_dopo_la_parola_non_apre_una_richiesta():
    """R-615-6: dopo la parola la voce comincia con 3 blocchi di fila, come nella
    finestra: un clic (un blocco) non manda niente."""
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (SILENZIO, 3), VOCE, (SILENZIO, 3), VOCE, VOCE,
                       (SILENZIO, _sec(a.ATTESA_VOCE_S) + 5))).gira()
    assert f.inviati == []


def test_l_attesa_dopo_la_parola_conta_anche_i_rumori():
    """R-616-2: rumori brevi (forte-forte-debole) non allungano l'attesa oltre i 5 s:
    dopo ATTESA_VOCE_S la voce vera non apre più una richiesta."""
    f = Finti()
    rumore = [VOCE, VOCE, SILENZIO]
    n = _sec(a.ATTESA_VOCE_S) // 3 + 2
    f.ascolto(_blocchi(PAROLA, *(rumore * n), (VOCE, 10), (SILENZIO, 10))).gira()
    assert f.inviati == []


def test_l_inizio_della_voce_resta_nella_richiesta():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, VOCE, (SILENZIO, 2), (VOCE, 5), (SILENZIO, 10)),
              finestra_s=0).gira()
    assert _campioni(f.inviati[0]) == (5 + 10) * a.BLOCCO


def test_registrazione_al_massimo_30_secondi():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE, _sec(60))), finestra_s=0).gira()
    assert _campioni(f.inviati[0]) == _sec(a.REGISTRAZIONE_MAX_S) * a.BLOCCO


# ── finestra di 12 s dopo la risposta ──

def test_finestra_continua_senza_parola():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE, 10), (SILENZIO, 10),
                       (SILENZIO, _sec(5)), (VOCE, 10), (SILENZIO, 10),
                       (SILENZIO, _sec(20))), finestra_s=12).gira()
    assert len(f.inviati) == 2 and f.bip == ["ok"]
    assert _campioni(f.inviati[1]) == (10 + 10) * a.BLOCCO


def test_finestra_scaduta_torna_alla_parola():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE, 10), (SILENZIO, 10),
                       (SILENZIO, _sec(13)), (VOCE, 10), (SILENZIO, 10)),
              finestra_s=12).gira()
    assert len(f.inviati) == 1  # la voce dopo 13 s senza parola non parte


def test_voce_breve_nella_finestra_non_apre_un_turno():
    """Un colpo di tosse (un blocco) non è una richiesta."""
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE, 10), (SILENZIO, 10),
                       VOCE, (SILENZIO, _sec(13))), finestra_s=12).gira()
    assert len(f.inviati) == 1


def test_massimo_dei_turni_di_fila():
    f = Finti()
    turno = [(VOCE, 10), (SILENZIO, 10), (SILENZIO, 5)]
    f.ascolto(_blocchi(PAROLA, *(turno * 5)), finestra_s=12, max_turni=2).gira()
    assert len(f.inviati) == 2


def test_dopo_la_finestra_la_parola_riattiva():
    f = Finti()
    f.ascolto(_blocchi(PAROLA, (VOCE, 10), (SILENZIO, 10), (SILENZIO, _sec(13)),
                       PAROLA, (VOCE, 10), (SILENZIO, 10)), finestra_s=12).gira()
    assert len(f.inviati) == 2 and f.bip == ["ok", "ok"]


# ── fail-safe ──

def test_invio_fallito_bip_di_errore_e_niente_finestra():
    f = Finti(esito=(False, None, "HTTP 503"))
    f.ascolto(_blocchi(PAROLA, (VOCE, 10), (SILENZIO, 10), (VOCE, 10), (SILENZIO, 10)),
              finestra_s=12).gira()
    assert f.bip == ["ok", "errore"] and f.riprodotti == [] and len(f.inviati) == 1
    assert f.svuotati == 2  # dopo il bip iniziale e dopo il bip di errore (V-3 bot #323)


def test_eccezioni_delle_parti_non_fermano_l_ascolto():
    class Rotti(Finti):
        def __init__(self):
            super().__init__()
            self.chiamate = 0

        def rilevatore(self, b):
            self.chiamate += 1
            if self.chiamate == 1:
                raise RuntimeError("modello")
            return super().rilevatore(b)

        def invia(self, wav):
            self.inviati.append(wav)
            raise OSError("rete")

        def suona(self, tipo):
            self.bip.append(tipo)
            raise OSError("afplay")

    f = Rotti()
    f.ascolto(_blocchi(SILENZIO, PAROLA, (VOCE, 5), (SILENZIO, 10),
                       PAROLA, (VOCE, 5), (SILENZIO, 10))).gira()
    assert len(f.inviati) == 2 and f.bip == ["ok", "errore", "ok", "errore"]


def test_rilevatore_sempre_in_errore_log_limitato_e_pausa_crescente(caplog):
    """V-1 ve #323: un rilevatore rotto non scrive una riga per blocco e non gira a vuoto:
    log al 1°, 2°, 4°, 8°… errore, pausa crescente fino a 60 s, microfono svuotato."""
    pause = []

    class Rotto(Finti):
        def rilevatore(self, b):
            raise RuntimeError("modello")

    f = Rotto()
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        a.Ascolto(iter(_blocchi((SILENZIO, 1000))), f.rilevatore, f.invia, f.riproduci,
                  f.suona, svuota=f.svuota, dorme=pause.append).gira()
    righe = [r for r in caplog.records if "rilevatore: errore" in r.getMessage()]
    assert len(righe) == 10  # 1, 2, 4, …, 512
    assert pause[:4] == [0.5, 1.0, 2.0, 4.0] and max(pause) == a.PAUSA_ERRORI_MAX_S
    assert len(pause) == 998 and f.svuotati == 998 and f.inviati == []


def test_rilevatore_in_errore_per_giorni_resta_a_60_secondi(caplog):
    """R-624-1: oltre i 1027 errori di fila `2 ** (n - 3)` non entra in un float: la
    pausa deve restare 60 s e il log logaritmico, senza «pausa fallita» a ogni blocco."""
    pause = []

    def rotto(b):
        raise RuntimeError("modello")

    f = Finti()
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        a.Ascolto(iter(_blocchi((SILENZIO, 1200))), rotto, f.invia, f.riproduci, f.suona,
                  svuota=f.svuota, dorme=pause.append).gira()
    testo = [r.getMessage() for r in caplog.records]
    assert not any("pausa del rilevatore fallita" in t for t in testo)
    assert len(pause) == 1198 and pause[-1] == a.PAUSA_ERRORI_MAX_S
    assert sum("rilevatore: errore" in t for t in testo) == 11  # 1, 2, 4, …, 1024


def test_rilevatore_che_torna_azzera_il_conto(caplog):
    class Ballerino(Finti):
        def __init__(self):
            super().__init__()
            self.n = 0

        def rilevatore(self, b):
            self.n += 1
            if self.n <= 5:
                raise RuntimeError("x")
            return super().rilevatore(b)

    f = Ballerino()
    pause = []
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        a.Ascolto(iter(_blocchi((SILENZIO, 5), SILENZIO, PAROLA, (VOCE, 5), (SILENZIO, 10))),
                  f.rilevatore, f.invia, f.riproduci, f.suona, svuota=f.svuota,
                  dorme=pause.append, finestra_s=0).gira()
    righe = [r.getMessage() for r in caplog.records]
    assert sum("di nuovo a posto" in t for t in righe) == 1  # R-624-2: una volta sola
    assert "di nuovo a posto dopo 5 errori" in " ".join(righe) and len(f.inviati) == 1
    assert pause == [0.5, 1.0, 2.0]


def test_dopo_il_ritorno_le_pause_ripartono_da_mezzo_secondo():
    """R-624-2: il conto si azzera davvero quando il rilevatore torna."""
    errori = iter([True] * 4 + [False] * 3 + [True] * 4 + [False] * 10)
    pause = []

    def ballerino(b):
        if next(errori, False):
            raise RuntimeError("x")
        return 0.0

    f = Finti()
    a.Ascolto(iter(_blocchi((SILENZIO, 21))), ballerino, f.invia, f.riproduci, f.suona,
              svuota=f.svuota, dorme=pause.append).gira()
    assert pause == [0.5, 1.0, 0.5, 1.0]


def test_avviso_se_il_microfono_e_muto(caplog):
    f = Finti()
    with caplog.at_level(logging.WARNING, logger="gas.ascolto"):
        f.ascolto(_blocchi(([0] * a.BLOCCO, _sec(25)))).gira()
    avvisi = [r for r in caplog.records if "silenzio assoluto" in r.getMessage()]
    assert len(avvisi) == 1


def test_log_senza_audio_ne_token(caplog):
    f = Finti(esito=(False, None, "HTTP 401"))
    with caplog.at_level(logging.DEBUG, logger="gas.ascolto"):
        f.ascolto(_blocchi(PAROLA, (VOCE, 5), (SILENZIO, 10))).gira()
    testo = " ".join(r.getMessage() for r in caplog.records)
    assert TOKEN not in testo and "RIFF" not in testo and "2000" not in testo


# ── parti vere: invio, riproduzione, configurazione ──

class _Server(http.server.BaseHTTPRequestHandler):
    risposta = (200, "audio/mpeg", b"ID3-MP3")
    visti = []

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        type(self).visti.append((self.path, dict(self.headers), self.rfile.read(n)))
        codice, tipo, corpo = type(self).risposta
        self.send_response(codice)
        if codice == 302:
            self.send_header("Location", f"http://{self.headers['Host']}/rubato")
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):  # dove porterebbe il redirect: risponde audio, come un server vero
        type(self).visti.append((self.path, dict(self.headers), b""))
        self.send_response(200)
        self.send_header("Content-Type", "audio/mpeg")
        self.send_header("Content-Length", "3")
        self.end_headers()
        self.wfile.write(b"ID3")

    def log_message(self, *x):
        pass


@pytest.fixture
def server():
    _Server.visti = []
    s = http.server.HTTPServer(("127.0.0.1", 0), _Server)
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{s.server_address[1]}"
    s.shutdown()
    s.server_close()


def test_invio_al_server_vero(server):
    _Server.risposta = (200, "audio/mpeg", b"ID3-MP3")
    ok, audio, motivo = a.invia_al_server(server, TOKEN, 5)(b"RIFF-WAV")
    assert (ok, audio, motivo) == (True, b"ID3-MP3", "")
    percorso, intestazioni, corpo = _Server.visti[0]
    assert percorso == "/voice" and corpo == b"RIFF-WAV"
    assert intestazioni["Authorization"] == f"Bearer {TOKEN}"
    assert intestazioni["Content-Type"] == "audio/wav" and intestazioni["Accept"] == "audio/mpeg"


@pytest.mark.parametrize("risposta,atteso", [
    ((401, "application/json", b'{"error": "Unauthorized"}'), "HTTP 401"),
    ((429, "application/json", b'{"error": "troppe"}'), "HTTP 429"),
    ((200, "application/json", b'{"content": "testo"}'), "risposta inattesa"),
])
def test_invio_con_risposte_sbagliate(server, risposta, atteso):
    _Server.risposta = risposta
    ok, audio, motivo = a.invia_al_server(server, TOKEN, 5)(b"x")
    assert not ok and audio is None and atteso in motivo and TOKEN not in motivo


def test_redirect_non_seguito(server):
    """R-615-2: un 302 verso un altro host non si segue (il Bearer non esce)."""
    _Server.risposta = (302, "text/plain", b"")
    ok, audio, motivo = a.invia_al_server(server, TOKEN, 5)(b"x")
    assert not ok and "HTTP 302" in motivo and len(_Server.visti) == 1


def test_proxy_di_sistema_ignorato(monkeypatch):
    """R-615-2: su macOS i proxy di sistema valgono anche per 127.0.0.1. L'opener si
    costruisce all'import: lo si ricostruisce con un proxy nell'ambiente e non deve
    esserci nessun gestore di proxy attivo."""
    import importlib
    import urllib.request
    monkeypatch.setenv("http_proxy", "http://127.0.0.1:9")
    monkeypatch.setenv("https_proxy", "http://127.0.0.1:9")
    try:
        importlib.reload(a)
        attivi = [h for h in a._OPENER.handlers
                  if isinstance(h, urllib.request.ProxyHandler) and h.proxies]
    finally:
        monkeypatch.undo()
        importlib.reload(a)
    assert attivi == []


def test_server_giu():
    ok, audio, motivo = a.invia_al_server("http://127.0.0.1:9", TOKEN, 2)(b"x")
    assert not ok and "non raggiungibile" in motivo and TOKEN not in motivo


def test_riproduzione_da_file_0600_cancellato(monkeypatch, tmp_path):
    monkeypatch.setattr(a.tempfile, "tempdir", str(tmp_path))
    visti = []

    def finto_run(argv, **k):
        p = Path(argv[1])
        visti.append((argv[0], p.read_bytes(), stat.S_IMODE(p.stat().st_mode)))
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(a.subprocess, "run", finto_run)
    a.riproduci_afplay(b"ID3-MP3")
    assert visti == [("afplay", b"ID3-MP3", 0o600)]
    assert list(tmp_path.iterdir()) == []


def test_riproduzione_fallita_cancella_comunque(monkeypatch, tmp_path):
    monkeypatch.setattr(a.tempfile, "tempdir", str(tmp_path))

    def esplode(argv, **k):
        raise OSError("afplay assente")

    monkeypatch.setattr(a.subprocess, "run", esplode)
    with pytest.raises(OSError):
        a.riproduci_afplay(b"x")
    assert list(tmp_path.iterdir()) == []


def test_wav_in_memoria():
    wav = a.in_wav([VOCE, SILENZIO])
    assert wav[:4] == b"RIFF" and _campioni(wav) == 2 * a.BLOCCO


@pytest.mark.parametrize("url,ok", [
    ("http://127.0.0.1:8765", True), ("http://localhost:8765", True),
    ("https://gas.example.org", True), ("http://gas.example.org", False),
    ("ftp://127.0.0.1", False), ("127.0.0.1:8765", False), ("http://", False),
])
def test_url_del_server(url, ok):
    assert (a.url_valido(url) is None) is ok


def test_senza_token_non_parte(monkeypatch, tmp_path, caplog):
    monkeypatch.setattr(a, "_GAS_ROOT", tmp_path)
    monkeypatch.delenv("GAS_VOICE_TOKEN", raising=False)
    monkeypatch.setattr(a, "Microfono", lambda: pytest.fail("microfono aperto senza token"))
    assert a.main() == 1


def test_url_in_chiaro_fuori_dal_mac_non_parte(monkeypatch, tmp_path):
    monkeypatch.setattr(a, "_GAS_ROOT", tmp_path)
    monkeypatch.setenv("GAS_VOICE_TOKEN", TOKEN)
    monkeypatch.setenv("GAS_VOICE_URL", "http://gas.example.org:8765")
    monkeypatch.setattr(a, "Microfono", lambda: pytest.fail("microfono aperto"))
    assert a.main() == 1


@pytest.mark.parametrize("url,porta,atteso", [
    (None, None, "http://127.0.0.1:8765"),
    (None, "9001", "http://127.0.0.1:9001"),
    ("https://gas.example.org/", "9001", "https://gas.example.org"),
])
def test_url_del_server_segue_la_porta(monkeypatch, url, porta, atteso):
    """R-616-1: senza GAS_VOICE_URL il client usa la porta del server voce."""
    for k, v in (("GAS_VOICE_URL", url), ("GAS_VOICE_PORT", porta)):
        if v is None:
            monkeypatch.delenv(k, raising=False)
        else:
            monkeypatch.setenv(k, v)
    assert a.url_del_server() == atteso


def test_main_usa_la_porta_del_server(monkeypatch, tmp_path):
    """R-618-1: `main` costruisce l'invio con url_del_server() (porta del server voce)."""
    monkeypatch.setattr(a, "_GAS_ROOT", tmp_path)
    monkeypatch.setenv("GAS_VOICE_TOKEN", TOKEN)
    monkeypatch.delenv("GAS_VOICE_URL", raising=False)
    monkeypatch.setenv("GAS_VOICE_PORT", "9001")
    visti = []
    monkeypatch.setattr(a, "rilevatore_openwakeword", lambda m: (lambda b: 0.0, lambda: None))
    monkeypatch.setattr(a, "invia_al_server",
                        lambda url, token, timeout: (visti.append(url), lambda wav: (False, None, ""))[1])

    def fermati():
        raise KeyboardInterrupt
    monkeypatch.setattr(a, "Microfono", fermati)
    assert a.main() == 0 and visti == ["http://127.0.0.1:9001"]


@pytest.mark.parametrize("ripiego", [False, True])
def test_dotenv_non_sovrascrive(monkeypatch, tmp_path, ripiego):
    (tmp_path / ".env").write_text('GAS_VOICE_TOKEN="dal-file"\nexport GAS_PROVA_ASCOLTO=x\n',
                                   encoding="utf-8")
    monkeypatch.delenv("GAS_NO_DOTENV", raising=False)  # conftest lo accende per la suite
    if ripiego:
        _senza_gas(monkeypatch)
    monkeypatch.setenv("GAS_VOICE_TOKEN", "dall-ambiente")
    monkeypatch.delenv("GAS_PROVA_ASCOLTO", raising=False)
    a._carica_dotenv(tmp_path)
    assert os.environ["GAS_VOICE_TOKEN"] == "dall-ambiente"
    assert os.environ["GAS_PROVA_ASCOLTO"] == "x"


def _senza_gas(monkeypatch):
    """gas.py non importabile: il client usa il ripiego."""
    import builtins
    vero_import = builtins.__import__

    def finto(nome, *args, **kw):
        if nome == "gas":
            raise ImportError("gas assente")
        return vero_import(nome, *args, **kw)
    monkeypatch.setattr(builtins, "__import__", finto)


@pytest.mark.parametrize("ripiego", [False, True])
def test_dotenv_come_il_server(monkeypatch, tmp_path, ripiego):
    """V-1 bot #323: commento in linea, virgolette con commento e BOM letti come li legge
    il server voce (gas._carica_dotenv), così il token del client è lo stesso."""
    (tmp_path / ".env").write_bytes(
        "\ufeffGAS_VOICE_TOKEN=abc # voce\nGAS_VOICE_PORT=\"9001\" # porta\n".encode())
    monkeypatch.delenv("GAS_NO_DOTENV", raising=False)
    monkeypatch.delenv("GAS_VOICE_TOKEN", raising=False)
    monkeypatch.delenv("GAS_VOICE_PORT", raising=False)
    if ripiego:
        _senza_gas(monkeypatch)
    a._carica_dotenv(tmp_path)
    assert os.environ["GAS_VOICE_TOKEN"] == "abc" and os.environ["GAS_VOICE_PORT"] == "9001"


def test_dotenv_usa_il_caricatore_di_gas(monkeypatch, tmp_path):
    """V-1 bot #323: la strada principale è proprio gas._carica_dotenv (lo stesso del
    server voce), con il .env della cartella di Gas."""
    import gas
    visti = []
    monkeypatch.setattr(gas, "_carica_dotenv", lambda path=None: visti.append(path) or [])
    a._carica_dotenv(tmp_path)
    assert visti == [tmp_path / ".env"]


def test_dotenv_spento_dalla_suite(monkeypatch, tmp_path):
    """GAS_NO_DOTENV=1 vale anche per il client (come per server e CLI)."""
    (tmp_path / ".env").write_text("GAS_PROVA_SPENTO=1\n", encoding="utf-8")
    monkeypatch.setenv("GAS_NO_DOTENV", "1")
    monkeypatch.delenv("GAS_PROVA_SPENTO", raising=False)
    a._carica_dotenv(tmp_path)
    a._carica_dotenv_ripiego(tmp_path)
    assert "GAS_PROVA_SPENTO" not in os.environ


@pytest.mark.parametrize("valore,atteso", [("abc", 12.0), ("nan", 12.0), ("inf", 12.0),
                                           ("-5", 0.0), ("999", 120.0), ("7", 7.0)])
def test_numeri_dall_ambiente(monkeypatch, valore, atteso):
    monkeypatch.setenv("GAS_VOICE_FINESTRA", valore)
    assert a._numero("GAS_VOICE_FINESTRA", 12, 0, 120) == atteso


# ── scripts/voce ──

VOCE_DIR = RADICE / "scripts" / "voce"


@pytest.mark.parametrize("nome,comando", [
    ("com.gas.voce.server", "exec python -m modules.voice.server"),
    ("com.gas.ascolto", "exec python clients/voice/ascolto.py"),
])
def test_plist(nome, comando):
    p = plistlib.loads((VOCE_DIR / f"{nome}.plist").read_bytes())
    assert p["Label"] == nome and p["RunAtLoad"] is True and p["KeepAlive"] is True
    assert p["ThrottleInterval"] >= 10
    assert p["ProgramArguments"][:2] == ["/bin/zsh", "-c"]
    assert comando in p["ProgramArguments"][2] and "CARTELLA_GAS" in p["ProgramArguments"][2]
    assert p["StandardOutPath"].startswith("CARTELLA_GAS/.gas_voce/")


@pytest.mark.parametrize("script", ["installa.sh", "spegni.sh"])
def test_script_sintassi_e_solo_mac(script):
    percorso = VOCE_DIR / script
    assert subprocess.run(["bash", "-n", str(percorso)]).returncode == 0
    if sys.platform != "darwin":
        r = subprocess.run(["bash", str(percorso)], capture_output=True, text=True, timeout=30)
        assert r.returncode == 1 and "solo per il Mac" in r.stderr


def test_installa_non_stampa_il_token():
    testo = (VOCE_DIR / "installa.sh").read_text(encoding="utf-8")
    assert "grep -Eq" in testo  # il controllo del token è silenzioso
    assert "cat .env" not in testo and "echo $GAS_VOICE_TOKEN" not in testo


def test_dipendenze_del_mac_fissate():
    righe = [r for r in (RADICE / "clients/voice/requirements-ascolto.txt").read_text()
             .splitlines() if r.strip() and not r.startswith("#")]
    assert righe and all("==" in r for r in righe)
    assert any(r.startswith("openwakeword==") for r in righe)


# ── installa.sh fino in fondo, con i comandi del Mac finti (R-615-1) ──

_FINTI = {
    "uname": 'echo Darwin',
    "plutil": 'exit 0',
    # launchctl con lo stato dei servizi (prova dal vero di M1): «$REGISTRO.su.<servizio>»
    # = caricato. Dopo bootout il servizio resta visibile per BOOTOUT_LENTO letture di
    # print (bootout asincrono) e in quel tempo bootstrap fallisce con l'errore 5 vero;
    # BOOTSTRAP_FALLISCE = quanti bootstrap falliscono comunque prima di riuscire.
    "launchctl": ('echo "launchctl $*" >> "$REGISTRO"\n'
                  'case "$1" in\n'
                  '  print) s="${2##*/}"\n'
                  '    if [ -f "$REGISTRO.su.$s" ]; then echo "	state = running"; exit 0; fi\n'
                  '    n=$(cat "$REGISTRO.giu.$s" 2>/dev/null || echo 0)\n'
                  '    if [ "$n" -gt 0 ]; then echo $((n-1)) > "$REGISTRO.giu.$s"\n'
                  '      echo "	state = running"; exit 0; fi\n'
                  '    echo "Could not find service" >&2; exit 113;;\n'
                  '  bootout) s="${2##*/}"; [ -f "$REGISTRO.su.$s" ] || exit 3\n'
                  '    rm -f "$REGISTRO.su.$s"; echo "${BOOTOUT_LENTO:-0}" > "$REGISTRO.giu.$s";;\n'
                  '  bootstrap) s="$(basename "$3" .plist)"\n'
                  '    n=$(cat "$REGISTRO.giu.$s" 2>/dev/null || echo 0)\n'
                  '    f=$(cat "$REGISTRO.bs" 2>/dev/null || echo 0); echo $((f+1)) > "$REGISTRO.bs"\n'
                  '    if [ -f "$REGISTRO.su.$s" ] || [ "$n" -gt 0 ] \\\n'
                  '       || [ "$f" -lt "${BOOTSTRAP_FALLISCE:-0}" ]; then\n'
                  '      echo "Bootstrap failed: 5: Input/output error" >&2; exit 5; fi\n'
                  '    touch "$REGISTRO.su.$s";;\n'
                  'esac\nexit 0'),
    "nc": ('echo "nc $*" >> "$REGISTRO"\n'
           'n=$(cat "$REGISTRO.nc" 2>/dev/null || echo 0); echo $((n+1)) > "$REGISTRO.nc"\n'
           '[ "$((n+1))" -gt "${NC_FALLISCE:-0}" ]'),
    "sleep": 'echo "sleep $*" >> "$REGISTRO"; exit 0',  # R-629-1: le attese si contano
    "python": ('echo "python $*" >> "$REGISTRO"\n'
               'case "$*" in *version_info*) [ -z "$PYTHON_VECCHIO" ];; *) cat > /dev/null;; esac'),
    "python3": 'echo "python3 $*" >> "$REGISTRO"; exit 0',
}


def _gas_finto(tmp_path, nome="Gas", env="GAS_VOICE_TOKEN=segreto-di-prova\n"):
    gas = tmp_path / nome
    (gas / "scripts" / "voce").mkdir(parents=True)
    for f in VOCE_DIR.iterdir():
        (gas / "scripts" / "voce" / f.name).write_bytes(f.read_bytes())
    (gas / "clients" / "voice").mkdir(parents=True)
    (gas / "clients/voice/requirements-ascolto.txt").write_text("")
    (gas / "requirements.txt").write_text("")
    (gas / "gas.py").write_text("")
    (gas / ".env").write_text(env)
    finti = tmp_path / "finti"
    finti.mkdir(exist_ok=True)
    for nome_cmd, corpo in _FINTI.items():
        p = finti / nome_cmd
        p.write_text("#!/bin/bash\n" + corpo + "\n")
        p.chmod(0o755)
    (gas / ".venv" / "bin").mkdir(parents=True)
    (gas / ".venv/bin/activate").write_text(f'export PATH="{finti}:$PATH"\n')
    casa = tmp_path / "casa"
    casa.mkdir(exist_ok=True)
    return gas, finti, casa


def _installa(gas, finti, casa, tmp_path, **extra):
    registro = tmp_path / "registro.txt"
    env = {"PATH": f"{finti}:/usr/bin:/bin", "HOME": str(casa), "REGISTRO": str(registro),
           **extra}
    r = subprocess.run(["bash", str(gas / "scripts/voce/installa.sh")], capture_output=True,
                       text=True, timeout=60, env=env)
    return r, registro.read_text() if registro.exists() else ""


def test_installa_arriva_in_fondo_senza_porta_nel_env(tmp_path):
    """R-615-1: senza GAS_VOICE_PORT nel .env (il caso normale) lo script non deve
    fermarsi in silenzio dopo il passo 5."""
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "6/6 tutto acceso" in r.stdout and "nc -z 127.0.0.1 8765" in registro
    assert "segreto-di-prova" not in r.stdout + r.stderr + registro
    for s in ("com.gas.voce.server", "com.gas.ascolto"):
        p = plistlib.loads((casa / "Library/LaunchAgents" / f"{s}.plist").read_bytes())
        assert str(gas) in p["ProgramArguments"][2] and "CARTELLA_GAS" not in str(p)
        assert f"launchctl bootstrap gui/" in registro


def test_installa_usa_la_porta_del_env(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=x\nGAS_VOICE_PORT=9001\n")
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "nc -z 127.0.0.1 9001" in registro.splitlines()


def test_installa_porta_ripetuta_vale_la_prima(tmp_path):
    """V-2 bot #323: come server e ascolto, vale la PRIMA GAS_VOICE_PORT del .env."""
    gas, finti, casa = _gas_finto(
        tmp_path, env="GAS_VOICE_TOKEN=x\nGAS_VOICE_PORT=9001\nGAS_VOICE_PORT=9002\n")
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "nc -z 127.0.0.1 9001" in registro.splitlines()


def test_installa_avvisa_se_c_e_un_url_remoto(tmp_path):
    gas, finti, casa = _gas_finto(
        tmp_path, env="GAS_VOICE_TOKEN=x\nGAS_VOICE_URL=https://gas.example.org\n")
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "AVVISO: nel .env c'è GAS_VOICE_URL" in r.stdout


def test_installa_porta_con_commento_in_linea(tmp_path):
    """R-622-1: le cifre di un commento in linea non finiscono nella porta."""
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=x\nGAS_VOICE_PORT=9001 # era 8765\n")
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "nc -z 127.0.0.1 9001" in registro.splitlines()


def _gia_caricati(tmp_path):
    for s in ("com.gas.voce.server", "com.gas.ascolto"):
        (tmp_path / f"registro.txt.su.{s}").touch()


def test_installa_seconda_volta_aspetta_che_il_vecchio_sparisca(tmp_path):
    """Prova dal vero di M1: alla seconda esecuzione bootout è asincrono e un bootstrap
    subito dopo dà «Bootstrap failed: 5». Lo script aspetta che print fallisca."""
    gas, finti, casa = _gas_finto(tmp_path)
    _gia_caricati(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, BOOTOUT_LENTO="4")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "Bootstrap failed" not in r.stderr
    righe = registro.splitlines()
    for s in ("com.gas.voce.server", "com.gas.ascolto"):
        fuori = righe.index(f"launchctl bootout gui/{os.getuid()}/{s}")
        dentro = next(i for i, x in enumerate(righe) if x.startswith("launchctl bootstrap")
                      and x.endswith(f"/{s}.plist"))
        letture = [x for x in righe[fuori:dentro] if x == f"launchctl print gui/{os.getuid()}/{s}"]
        assert len(letture) == 5  # 4 ancora visibile + 1 sparito


def test_installa_servizio_che_non_si_spegne_si_ferma(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path)
    _gia_caricati(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, BOOTOUT_LENTO="999")
    assert r.returncode == 1 and "non si spegne" in r.stderr
    assert "launchctl bootstrap" not in registro
    assert registro.count("launchctl print gui/") == 50  # al massimo 5 s (50 × 0,1 s)


def test_installa_bootstrap_riprova(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, BOOTSTRAP_FALLISCE="2")
    assert r.returncode == 0, r.stdout + r.stderr
    assert registro.count("launchctl bootstrap") == 4  # 2 falliti + 2 servizi
    assert r.stdout.count("riprovo tra 1 s") == 2  # R-628-3: si dice che riprova


def test_installa_bootstrap_sempre_rotto_si_ferma(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, BOOTSTRAP_FALLISCE="99")
    assert r.returncode == 1 and "3 tentativi" in r.stderr
    assert registro.count("launchctl bootstrap") == 3 and "nc -z" not in registro
    assert r.stdout.count("riprovo tra 1 s") == 2
    assert registro.splitlines().count("sleep 1") == 2  # R-629-1: niente attesa dopo il terzo


def test_installa_aspetta_il_server_lento(tmp_path):
    """V-3 ve #323: il server che ci mette qualche secondo non dà un falso STOP."""
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, NC_FALLISCE="3")
    assert r.returncode == 0 and registro.count("nc -z") == 4


def test_installa_server_che_non_risponde_si_ferma(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, NC_FALLISCE="999")
    assert r.returncode == 1 and "non risponde" in r.stderr and registro.count("nc -z") == 30


def test_installa_python_vecchio_si_ferma_prima_delle_dipendenze(tmp_path):
    """V-3 ve #323: con Python < 3.11 nel .venv lo dice, invece di un pip che fallisce."""
    gas, finti, casa = _gas_finto(tmp_path)
    r, registro = _installa(gas, finti, casa, tmp_path, PYTHON_VECCHIO="1")
    assert r.returncode == 1 and "Python 3.11" in r.stderr and "pip install" not in registro


def test_installa_scrive_gas_claude_bin(tmp_path):
    """V-1 bot #323: con `claude` nel PATH e senza GAS_CLAUDE_BIN nel .env, installa.sh
    lo aggiunge col percorso assoluto (sotto launchd il PATH non lo troverebbe)."""
    gas, finti, casa = _gas_finto(tmp_path)
    (finti / "claude").write_text("#!/bin/bash\nexit 0\n")
    (finti / "claude").chmod(0o755)
    r, _ = _installa(gas, finti, casa, tmp_path)
    env = (gas / ".env").read_text()
    assert r.returncode == 0 and f"GAS_CLAUDE_BIN={finti}/claude" in env.splitlines()
    assert env.startswith("GAS_VOICE_TOKEN=segreto-di-prova\n")


def test_installa_non_tocca_un_gas_claude_bin_esistente(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=x\nGAS_CLAUDE_BIN=/opt/c\n")
    (finti / "claude").write_text("#!/bin/bash\nexit 0\n")
    (finti / "claude").chmod(0o755)
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and (gas / ".env").read_text() == "GAS_VOICE_TOKEN=x\nGAS_CLAUDE_BIN=/opt/c\n"


@pytest.mark.parametrize("riga", ["GAS_CLAUDE_BIN=", "GAS_CLAUDE_BIN= # da mettere"])
def test_installa_gas_claude_bin_vuoto_avvisa_e_non_raddoppia(tmp_path, riga):
    """R-624-3: una riga vuota non si raddoppia (vale la prima) e si avvisa."""
    gas, finti, casa = _gas_finto(tmp_path, env="GAS_VOICE_TOKEN=x\n" + riga + "\n")
    (finti / "claude").write_text("#!/bin/bash\nexit 0\n")
    (finti / "claude").chmod(0o755)
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "GAS_CLAUDE_BIN è vuoto" in r.stdout
    assert (gas / ".env").read_text() == "GAS_VOICE_TOKEN=x\n" + riga + "\n"


def test_installa_avvisa_se_claude_manca(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path)
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0 and "claude` non trovato" in r.stdout
    assert "GAS_CLAUDE_BIN" not in (gas / ".env").read_text()


@pytest.mark.parametrize("riga", ["GAS_VOICE_TOKEN=", "GAS_VOICE_TOKEN= # da mettere",
                                  "GAS_VOICE_TOKEN=\"\"", "GAS_VOICE_TOKEN=   "])
def test_installa_token_vuoto_si_ferma(tmp_path, riga):
    """V-4 bot #323: un token vuoto o col solo commento non passa il controllo."""
    gas, finti, casa = _gas_finto(tmp_path, env=riga + "\n")
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 1 and "GAS_VOICE_TOKEN" in r.stderr and registro == ""


@pytest.mark.parametrize("riga", ["GAS_VOICE_TOKEN=abc", "export GAS_VOICE_TOKEN=\"abc\"",
                                  "GAS_VOICE_TOKEN='abc' # x"])
def test_installa_token_buono_passa(tmp_path, riga):
    gas, finti, casa = _gas_finto(tmp_path, env=riga + "\n")
    r, _ = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 0, r.stderr


def test_installa_senza_token_si_ferma_prima_di_tutto(tmp_path):
    gas, finti, casa = _gas_finto(tmp_path, env="ALTRO=1\n")
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 1 and "GAS_VOICE_TOKEN" in r.stderr
    assert registro == "" and not (casa / "Library").exists()


@pytest.mark.parametrize("nome", ["Gas$(touch PWNED)", "Gas`touch PWNED`", "Ga\\s", "Ga&s",
                                  'Ga"s', "Ga#s", "Ga;s"])
def test_installa_rifiuta_cartelle_con_caratteri_pericolosi(tmp_path, nome):
    """R-615-3: lista bianca dei caratteri della cartella di Gas (finisce nel sed e
    nella shell del plist)."""
    gas, finti, casa = _gas_finto(tmp_path, nome=nome)
    r, registro = _installa(gas, finti, casa, tmp_path)
    assert r.returncode == 1 and "caratteri" in r.stderr
    assert registro == "" and not (tmp_path / "PWNED").exists()
