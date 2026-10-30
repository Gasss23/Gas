"""Proxy filtrante per il browser senza schermo (modules/web/proxy.py, R6 fetta 32, chat Mani).

Zero rete vera: un server d'origine e un'eco TCP su 127.0.0.1, DNS e connettore finti che
portano gli IP pubblici finti a quei server locali."""
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from modules.web import proxy as px

IP_PUBBLICO = "93.184.216.34"  # gasmerge-ip-ok: IP di esempio dei test, nessuna connessione reale


class _Origine(BaseHTTPRequestHandler):
    richieste: list = []

    def log_message(self, *_: object) -> None:
        pass

    def do_GET(self) -> None:
        _Origine.richieste.append({"percorso": self.path, "headers": dict(self.headers)})
        corpo = b"x" * 50_000 if self.path == "/grande" else b"pagina ok"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    do_HEAD = do_GET


@pytest.fixture(scope="module")
def origine():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _Origine)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield srv.server_address[1]
    srv.shutdown()
    srv.server_close()


@pytest.fixture(scope="module")
def eco():
    """Server TCP che rimanda indietro i byte: fa da «server TLS» dietro un tunnel."""
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    s.listen()

    def _servi() -> None:
        while True:
            try:
                c, _ = s.accept()
            except OSError:
                return

            def _eco(c: socket.socket) -> None:
                with c:
                    while True:
                        dati = c.recv(4096)
                        if not dati:
                            return
                        c.sendall(dati)
            threading.Thread(target=_eco, args=(c,), daemon=True).start()

    threading.Thread(target=_servi, daemon=True).start()
    yield s.getsockname()[1]
    s.close()


class _Rete:
    def __init__(self, porta_http: int, porta_eco: int):
        self.porte = {80: porta_http, 443: porta_eco}
        self.dns = {"sito.test": [IP_PUBBLICO], "interno.test": ["10.0.0.5"],  # gasmerge-ip-ok: IP di esempio dei test, nessuna connessione reale
                    "misto.test": [IP_PUBBLICO, "192.168.1.1"]}  # gasmerge-ip-ok: IP di esempio dei test, nessuna connessione reale
        self.connessi: list = []
        self.guasto = False

    def risolvi(self, host: str, porta: int) -> list:
        if host not in self.dns:
            raise socket.gaierror("nome sconosciuto")
        return self.dns[host]

    def connetti(self, ip: str, porta: int, timeout: float) -> socket.socket:
        self.connessi.append((ip, porta))
        if self.guasto:
            raise ConnectionRefusedError("rifiutata")
        assert ip == IP_PUBBLICO, ip
        return socket.create_connection(("127.0.0.1", self.porte[porta]), timeout=timeout)


@pytest.fixture
def rete(origine, eco):
    _Origine.richieste.clear()
    return _Rete(origine, eco)


def _proxy(rete: _Rete, **kw: object) -> px.ProxyFiltrante:
    return px.ProxyFiltrante(_risolvi=rete.risolvi, _connetti=rete.connetti, **kw)


def _manda(porta: int, richiesta: bytes) -> bytes:
    with socket.create_connection(("127.0.0.1", porta), timeout=5) as s:
        s.sendall(richiesta)
        dati = b""
        while True:
            pezzo = s.recv(65536)
            if not pezzo:
                return dati
            dati += pezzo


def _get(porta: int, url: str, extra: str = "") -> bytes:
    return _manda(porta, f"GET {url} HTTP/1.1\r\nHost: altro.test\r\n{extra}\r\n".encode())


# ───────────────────────────── caso buono ─────────────────────────────

def test_get_in_chiaro_passa_e_pulisce_le_intestazioni(rete):
    with _proxy(rete) as p:
        r = _get(p.porta, "http://sito.test/ok?a=1",
                 "Proxy-Connection: keep-alive\r\nProxy-Authorization: x\r\nProxy-Foo: y\r\n"
                 "Accept: text/html\r\n")
    assert r.startswith(b"HTTP/1.0 200") or r.startswith(b"HTTP/1.1 200")
    assert r.endswith(b"pagina ok")
    h = _Origine.richieste[-1]["headers"]
    assert _Origine.richieste[-1]["percorso"] == "/ok?a=1"
    assert h["Host"] == "sito.test" and h["Connection"] == "close" and h["Accept"] == "text/html"
    assert "Proxy-Connection" not in h and "Proxy-Authorization" not in h and "Proxy-Foo" not in h
    assert rete.connessi == [(IP_PUBBLICO, 80)]
    assert p.richieste == 1 and p.rifiuti == []


def test_tunnel_verso_443(rete):
    with _proxy(rete) as p:
        with socket.create_connection(("127.0.0.1", p.porta), timeout=5) as s:
            s.sendall(b"CONNECT sito.test:443 HTTP/1.1\r\nHost: sito.test:443\r\n\r\n")
            assert s.recv(4096) == b"HTTP/1.1 200 Connection established\r\n\r\n"
            s.sendall(b"ciao tls")
            assert s.recv(4096) == b"ciao tls"
    assert rete.connessi == [(IP_PUBBLICO, 443)]


def test_ascolta_solo_in_locale(rete):
    with _proxy(rete) as p:
        assert p._server.server_address[0] == "127.0.0.1"


# ───────────────────────────── rifiuti ─────────────────────────────

@pytest.mark.parametrize("url,motivo", [
    ("http://interno.test/", "indirizzo interno non permesso"),
    ("http://misto.test/", "indirizzo interno non permesso"),
    ("http://10.0.0.1/", "indirizzo interno non permesso"),  # gasmerge-ip-ok: IP di esempio dei test, nessuna connessione reale
    ("http://127.0.0.1/", "indirizzo interno non permesso"),  # gasmerge-ip-ok: IP di esempio dei test, nessuna connessione reale
    ("http://localhost/", "indirizzo interno non permesso"),
    ("http://sito.test:8080/", "porta non permessa: solo 80 e 443"),
    ("http://utente:pw@sito.test/", "url con credenziali non permesso"),
    ("https://sito.test/", "https solo attraverso CONNECT"),
    ("ftp://sito.test/", "schema non permesso: solo http e https"),
    ("/solo-percorso", "schema non permesso: solo http e https"),
    ("http://nessuno.test/", "nome host non risolto"),
])
def test_get_rifiutati_senza_connessione(rete, url, motivo):
    with _proxy(rete) as p:
        r = _get(p.porta, url)
    assert r.startswith(b"HTTP/1.1 403 Forbidden") and r.endswith(motivo.encode())
    assert rete.connessi == [] and p.rifiuti == [motivo]


@pytest.mark.parametrize("bersaglio,motivo", [
    ("sito.test:80", "tunnel solo verso la porta 443"),
    ("sito.test:8443", "tunnel solo verso la porta 443"),
    ("interno.test:443", "indirizzo interno non permesso"),
    ("10.0.0.5:443", "indirizzo interno non permesso"),  # gasmerge-ip-ok: IP di esempio dei test, nessuna connessione reale
    ("[::1]:443", "indirizzo interno non permesso"),
    ("localhost:443", "indirizzo interno non permesso"),
    ("sito.test", "richiesta non valida"),
    ("sito.test:٤٤٣", "richiesta non valida"),
    # Review #585 (B-585-1): il testo dopo l'ultimo «:» non è la porta che urlsplit legge.
    ("sito.test:80/:443", "richiesta non valida"),
    ("sito.test:80?:443", "richiesta non valida"),
    ("sito.test:80#:443", "richiesta non valida"),
    ("sito.test:80\\:443", "richiesta non valida"),
    ("utente@sito.test:443", "url con credenziali non permesso"),
])
def test_tunnel_rifiutati_senza_connessione(rete, bersaglio, motivo):
    with _proxy(rete) as p:
        r = _manda(p.porta, f"CONNECT {bersaglio} HTTP/1.1\r\n\r\n".encode())
    assert r.startswith(b"HTTP/1.1 403 Forbidden") and r.endswith(motivo.encode())
    assert rete.connessi == []


@pytest.mark.parametrize("richiesta,motivo", [
    (b"POST http://sito.test/ HTTP/1.1\r\n\r\n", "metodo non permesso: solo GET e HEAD"),
    (b"DELETE http://sito.test/ HTTP/1.1\r\n\r\n", "metodo non permesso: solo GET e HEAD"),
    (b"GET http://sito.test/ HTTP/1.1\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n",
     "upgrade non permesso (WebSocket)"),
    (b"CONNECT sito.test:443 HTTP/1.1\r\nUpgrade: websocket\r\n\r\n", "upgrade non permesso (WebSocket)"),
    (b"GET http://sito.test/ HTTP/1.1\r\nContent-Length: 5\r\n\r\n", "corpo della richiesta non permesso"),
    (b"GET http://sito.test/ HTTP/1.1\r\nTransfer-Encoding: chunked\r\n\r\n", "corpo della richiesta non permesso"),
    (b"GET http://sito.test/ HTTP/1.1\r\n\r\nGET http://sito.test/ HTTP/1.1\r\n\r\n",
     "corpo della richiesta non permesso"),
    (b"GET http://sito.test/\r\n\r\n", "richiesta non valida"),
    (b"GET http://sito.test/ SPDY/3\r\n\r\n", "richiesta non valida"),
    (b"GET http://sito.test/ HTTP/1.1\r\nsenza-due-punti\r\n\r\n", "richiesta non valida"),
    (b"GET http://sito.test/ HTTP/1.1\r\nNome Spazio: x\r\n\r\n", "richiesta non valida"),
    (b"GET http://sito.test/ HTTP/1.1\r\nX: a\x00b\r\n\r\n", "richiesta non valida"),
    (b"GET http://sito.test/ HTTP/1.1\r\nX: " + b"a" * 20_000 + b"\r\n\r\n", "richiesta troppo grande"),
])
def test_richieste_non_permesse(rete, richiesta, motivo):
    with _proxy(rete) as p:
        r = _manda(p.porta, richiesta)
    assert r.startswith(b"HTTP/1.1 403 Forbidden") and r.endswith(motivo.encode())
    assert rete.connessi == []


def test_richiesta_troncata_non_esplode(rete):
    with _proxy(rete) as p:
        with socket.create_connection(("127.0.0.1", p.porta), timeout=5) as s:
            s.sendall(b"GET http://sito.test/ HTTP/1.1\r\n")
            s.shutdown(socket.SHUT_WR)
            assert s.recv(4096).startswith(b"HTTP/1.1 403")
        assert _get(p.porta, "http://sito.test/ok").endswith(b"pagina ok")  # il proxy resta vivo


# ───────────────────────────── tetti ─────────────────────────────

def test_tetto_di_richieste(rete):
    with _proxy(rete, max_richieste=2) as p:
        assert _get(p.porta, "http://sito.test/ok").endswith(b"pagina ok")
        assert _get(p.porta, "http://sito.test/ok").endswith(b"pagina ok")
        r = _get(p.porta, "http://sito.test/ok")
    assert r.startswith(b"HTTP/1.1 403") and r.endswith(b"troppe richieste")
    assert len(rete.connessi) == 2


def test_tetto_di_byte(rete):
    with _proxy(rete, max_byte=10_000) as p:
        r = _get(p.porta, "http://sito.test/grande")
        assert len(r) < 10_000 and b"x" * 10_000 not in r  # nulla oltre il tetto arriva al browser
        assert p.rifiuti == ["troppi byte"]
        r = _get(p.porta, "http://sito.test/ok")  # il tetto è per tutta la vita del proxy
    # V-1 bot #312: la seconda richiesta non esce nemmeno, e il browser riceve il motivo.
    assert r.startswith(b"HTTP/1.1 403") and r.endswith(b"troppi byte")
    assert len(rete.connessi) == 1 and p.rifiuti == ["troppi byte", "troppi byte"]


def test_la_testa_inoltrata_conta_nei_byte(rete):
    """V-1 bot #312: i byte della richiesta inoltrata entrano nel tetto."""
    with _proxy(rete) as p:
        r = _get(p.porta, "http://sito.test/ok")
        assert r.endswith(b"pagina ok")
        testa = b"GET /ok HTTP/1.1\r\nHost: sito.test\r\nConnection: close\r\n\r\n"
        assert p.byte == len(r) + len(testa)


def test_durata_scaduta(rete):
    with _proxy(rete, durata=0.2) as p:
        time.sleep(0.3)
        r = _get(p.porta, "http://sito.test/ok")
    assert r.endswith(b"tempo massimo del proxy superato") and rete.connessi == []


def test_errore_di_rete_e_502_e_il_proxy_resta_vivo(rete):
    rete.guasto = True
    with _proxy(rete) as p:
        r = _get(p.porta, "http://sito.test/ok")
        assert r.startswith(b"HTTP/1.1 502") and r.endswith(b"errore di rete o di protocollo")
        rete.guasto = False
        assert _get(p.porta, "http://sito.test/ok").endswith(b"pagina ok")


def test_troppe_connessioni_contemporanee(rete, monkeypatch):
    monkeypatch.setattr(px, "MAX_CONNESSIONI", 1)
    with _proxy(rete) as p:
        with socket.create_connection(("127.0.0.1", p.porta), timeout=5) as primo:
            primo.sendall(b"GET http://sito.test/ok HTTP/1.1\r\n")  # testa incompleta: resta occupato
            time.sleep(0.2)
            r = _get(p.porta, "http://sito.test/ok")
    assert r.startswith(b"HTTP/1.1 503") and r.endswith(b"troppe connessioni contemporanee")


def test_testa_lenta_ha_un_tempo_massimo(rete, monkeypatch):
    """R-585-2: un byte ogni tanto non tiene aperta la connessione oltre il tempo della testa."""
    monkeypatch.setattr(px, "TIMEOUT_INATTIVITA", 0.5)
    with _proxy(rete) as p:
        with socket.create_connection(("127.0.0.1", p.porta), timeout=5) as s:
            s.settimeout(0.05)
            inizio, r = time.monotonic(), b""
            while time.monotonic() - inizio < 3 and not r:
                try:
                    s.sendall(b"G")
                    r = s.recv(4096)
                except socket.timeout:
                    pass
                except OSError:
                    break
            durata = time.monotonic() - inizio
    assert r.startswith(b"HTTP/1.1 403") and r.endswith(b"connessione inattiva")
    assert durata < 1.5  # il tempo è per tutta la testa, non per ogni byte


def test_client_muto_chiuso_alla_scadenza_del_proxy(rete):
    """V-3 ve #312: con la durata del proxy a 1 s, un client che non manda nulla viene
    chiuso a quella scadenza, non dopo i 10 s di inattività."""
    with _proxy(rete, durata=1.0) as p:
        with socket.create_connection(("127.0.0.1", p.porta), timeout=5) as s:
            s.settimeout(3)
            inizio = time.monotonic()
            r = s.recv(4096)
            durata = time.monotonic() - inizio
    assert r.startswith(b"HTTP/1.1 403") and r.endswith(b"tempo massimo del proxy superato")
    assert durata < 2.5


def test_timeout_della_testa_non_resta_sul_tunnel(rete, monkeypatch):
    """R-586-1: dopo la testa il socket del browser torna a TIMEOUT_INATTIVITA."""
    visti = []
    originale = px.ProxyFiltrante._tunnel

    def _spia(self, client, bersaglio, risposto):
        visti.append(client.gettimeout())
        return originale(self, client, bersaglio, risposto)

    monkeypatch.setattr(px.ProxyFiltrante, "_tunnel", _spia)
    with _proxy(rete) as p:
        with socket.create_connection(("127.0.0.1", p.porta), timeout=5) as s:
            s.sendall(b"CONNECT sito.test:443 HTTP/1.1\r\n\r\n")
            assert s.recv(4096).startswith(b"HTTP/1.1 200")
    assert visti == [px.TIMEOUT_INATTIVITA]


def test_ferma_chiude_i_tunnel_aperti(rete):
    """R-585-3: ferma() chiude subito un tunnel già aperto, senza aspettare l'inattività."""
    p = _proxy(rete)
    p.avvia()
    with socket.create_connection(("127.0.0.1", p.porta), timeout=5) as s:
        s.sendall(b"CONNECT sito.test:443 HTTP/1.1\r\n\r\n")
        assert s.recv(4096).startswith(b"HTTP/1.1 200")
        s.sendall(b"prima")
        assert s.recv(4096) == b"prima"
        p.ferma()
        s.settimeout(2)
        assert s.recv(4096) == b""  # chiuso dal proxy, prima dei 10 s di inattività


def test_testa_che_sfora_il_tetto_non_apre_connessioni(rete):
    """R-590-2: se la testa da inoltrare fa superare il tetto, il proxy non apre nemmeno
    la connessione verso l'host."""
    with _proxy(rete, max_byte=40) as p:
        r = _get(p.porta, "http://sito.test/ok")
    assert r.startswith(b"HTTP/1.1 403") and r.endswith(b"troppi byte")
    assert rete.connessi == []


def test_invio_bloccato_inattivo(rete, monkeypatch):
    """R-590-1: con la scadenza lontana, a chiudere è l'inattività."""
    monkeypatch.setattr(px, "TIMEOUT_INATTIVITA", 0.3)
    p = _proxy(rete)
    p.avvia()
    try:
        class _Muto:
            def settimeout(self, t):
                self.t = t

            def sendall(self, dati):
                time.sleep(self.t)
                raise socket.timeout()

        with pytest.raises(px._leggi._Rifiuto) as e:
            p._invia(_Muto(), b"x")
        assert e.value.motivo == "connessione inattiva"
    finally:
        p.ferma()


def test_invio_bloccato_si_ferma_alla_scadenza(rete, monkeypatch):
    """V-2 bot #312: un invio verso chi non legge non va oltre la scadenza del proxy."""
    p = _proxy(rete, durata=1.0)
    p.avvia()
    try:
        ferma = threading.Event()

        class _Muto:
            def settimeout(self, t):
                self.t = t

            def sendall(self, dati):
                ferma.wait(self.t)
                raise socket.timeout()

        inizio = time.monotonic()
        with pytest.raises(px._leggi._Rifiuto) as e:
            p._invia(_Muto(), b"x")
        assert time.monotonic() - inizio < 2 and e.value.motivo == "tempo massimo del proxy superato"
        time.sleep(1.1)
        with pytest.raises(px._leggi._Rifiuto) as e:
            p._invia(_Muto(), b"x")
        assert e.value.motivo == "tempo massimo del proxy superato"
    finally:
        p.ferma()


def test_ferma_due_volte(rete):
    p = _proxy(rete)
    p.avvia()
    p.ferma()
    p.ferma()
