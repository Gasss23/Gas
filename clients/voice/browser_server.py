#!/usr/bin/env python3
"""
clients/voice/browser_server.py — FASE 3 Fetta 4b

Proxy HTTP locale: serve browser_client.html e forwarda POST /voice
al voice server locale (porta 8765). Zero dipendenze esterne (solo stdlib).

Uso (dalla root ~/Gas, con venv attivata):
    # assicurarsi che il voice server sia in ascolto su :8765 prima di questo
    python clients/voice/browser_server.py
    # poi aprire http://127.0.0.1:9000 nel browser

Variabili d'ambiente (lette da .env nella root Gas se presenti):
    GAS_VOICE_TOKEN    — token bearer  OBBLIGATORIO
    GAS_VOICE_URL      — URL base voice server  (default: http://127.0.0.1:8765)
    GAS_BROWSER_PORT   — porta questo server    (default: 9000)
    GAS_VOICE_TIMEOUT  — secondi di attesa della risposta di Gas (default: 600; una
                         chiamata del cervello forte può durare fino a 300 s)
    GAS_VOICE_FINESTRA — secondi di microfono aperto dopo la risposta, in modalità
                         conversazione (default: 12)
    GAS_VOICE_MAX_TURNI — turni di fila in modalità conversazione, contando quello
                         avviato dal clic; poi serve un clic (default: 5; argine
                         a rumori di fondo)
    GAS_VOICE_INTERRUZIONE — 0/false/no/off: mentre Gas parla la tua voce NON lo
                         interrompe (default: acceso)
"""
from __future__ import annotations

import http.client
import json
import logging
import os
import socket
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)

_HERE = Path(__file__).parent
_GAS_ROOT = _HERE.parent.parent
_HTML_FILE = _HERE / "browser_client.html"
_HTML_VOCI = _HERE / "prova_voci.html"   # V8: pagina «prova voci»
_CONNECT_TIMEOUT = 10  # secondi per collegarsi al voice server (non per la risposta)


def _load_dotenv(root: Path) -> None:
    """Carica .env dalla root senza sovrascrivere vars già nell'ambiente."""
    env_path = root / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip()


class BrowserProxyHandler(BaseHTTPRequestHandler):
    """Serve browser_client.html (GET /) e fa da proxy verso il voice server (POST /voice)."""

    token: str = ""
    voice_host: str = "127.0.0.1"
    voice_port: int = 8765
    # V2: il forte (`claude -p`) può metterci minuti; prima era 90 s. Non chiamarlo
    # `timeout`: è un attributo di socketserver (socket del browser, R-568-1-M2).
    voice_timeout: int = 600
    finestra: float = 12.0  # V3: GAS_VOICE_FINESTRA, letta dalla pagina su GET /config
    max_turni: int = 5      # V-1 bot #311: GAS_VOICE_MAX_TURNI
    interruzione: bool = True  # V4: GAS_VOICE_INTERRUZIONE

    def log_message(self, fmt: str, *args: object) -> None:
        log.info(fmt, *args)

    def do_GET(self) -> None:
        if not self._host_locale():   # R-625-1-M2: anche pagina, /config ed elenco voci
            self._send_error_json(403, "Host non locale: rifiutato")
            return
        if self.path == "/config":
            # V3: la pagina legge qui la finestra della conversazione (nessun segreto)
            cfg = json.dumps({"finestra": self.finestra, "max_turni": self.max_turni,
                              "interruzione": self.interruzione}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(cfg)))
            self.end_headers()
            self.wfile.write(cfg)
            return
        if self.path in ("/voci/elenco", "/voci/libreria"):   # V8/V8b: elenchi dal server voce
            self._inoltra_semplice("GET", self.path, b"")
            return
        if self.path not in ("/", "/index.html", "/voci"):
            self._not_found()
            return
        try:
            html = (_HTML_VOCI if self.path == "/voci" else _HTML_FILE).read_bytes()
        except FileNotFoundError:
            self._not_found()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def _host_locale(self) -> bool:
        """R-625-1-M2 (DNS rebinding): la pagina gira solo su questo computer, quindi la
        richiesta deve nominare 127.0.0.1, localhost o ::1 con la porta di questo proxy.
        Un sito esterno fatto risolvere a 127.0.0.1 manda il SUO nome in Host: rifiutato.
        Senza Host (client HTTP/1.0 locali) si lascia passare."""
        host = self.headers.get("Host")
        if not host:
            return True
        porta = self.server.server_address[1]
        return host.lower() in {f"127.0.0.1:{porta}", f"localhost:{porta}", f"[::1]:{porta}"}

    def _stessa_origine(self) -> bool:
        """R-624-4-M2: un'altra pagina aperta nel browser non può far parlare Gas né
        spendere prove di voce. Il browser manda Origin sulle POST: deve essere questa
        pagina (stesso host:porta della richiesta). Senza Origin (curl, client non
        browser) si lascia passare: lì c'è chi ha già accesso al computer."""
        origine = self.headers.get("Origin")
        if not origine:
            return True
        return urllib.parse.urlsplit(origine).netloc == (self.headers.get("Host") or "")

    def do_POST(self) -> None:
        if not self._host_locale():
            self._send_error_json(403, "Host non locale: rifiutato")
            return
        if not self._stessa_origine():
            self._send_error_json(403, "Richiesta da un'altra pagina: rifiutata")
            return
        if self.path in ("/voci/prova", "/voci/aggiungi"):   # V8/V8b: prova o aggiunta di una voce
            try:
                n = int(self.headers.get("Content-Length", 0) or 0)
            except ValueError:
                n = 0
            self._inoltra_semplice("POST", self.path, self.rfile.read(min(max(n, 0), 4096)))
            return
        if self.path != "/voice":
            self._not_found()
            return
        try:
            length = int(self.headers.get("Content-Length", 0) or 0)
        except ValueError:
            length = 0
        body = self.rfile.read(length) if length > 0 else b""
        self._proxy_voice(body)

    def _proxy_voice(self, body: bytes) -> None:
        content_type = self.headers.get("Content-Type", "application/json")
        accept = self.headers.get("Accept", "audio/mpeg")
        formato = self.headers.get("X-Gas-Formato", "")  # V3: «audio+testo»
        conn = http.client.HTTPConnection(self.voice_host, self.voice_port,
                                          timeout=_CONNECT_TIMEOUT)
        try:
            # R-568-3-M2: la connessione ha un tetto corto (server spento o irraggiungibile
            # → 502 subito); solo l'attesa della risposta usa il tetto lungo.
            conn.connect()
            conn.sock.settimeout(self.voice_timeout)
        except OSError as exc:
            conn.close()
            self._send_error_json(502, f"Voice server non raggiungibile: {exc}")
            return
        try:
            conn.request(
                "POST",
                "/voice",
                body=body,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": content_type,
                    "Content-Length": str(len(body)),
                    "Accept": accept,
                    **({"X-Gas-Formato": formato} if formato else {}),
                },
            )
            verso_voce = conn.sock  # V7b: getresponse() lo stacca da conn se la risposta chiude
            resp = conn.getresponse()
            if resp.getheader("Content-Type", "").startswith("application/x-ndjson"):
                self._inoltra_a_pezzi(resp, verso_voce)  # V7b: riga per riga, appena arriva
                return
            resp_body = resp.read()
            resp_ct = resp.getheader("Content-Type", "application/octet-stream")
            resp_status = resp.status
        except TimeoutError:
            # V2: scaduto il tempo, Gas può star ancora lavorando: dirlo, non «non raggiungibile»
            # R-571-2-M2: il tetto conta anche l'attesa in coda dietro un'altra richiesta
            # (il server voce fa un turno alla volta): quel turno può partire più tardi.
            # V-1 bot #308 (su 2507621): il turno continua dietro; ripeterlo ne fa partire un altro
            self._send_error_json(504, f"Gas non ha risposto entro {self.voice_timeout} s: il lavoro "
                                       "può essere ancora in corso (o in coda dietro un'altra "
                                       "richiesta). NON ripetere la richiesta: ne partirebbe una "
                                       "seconda. Guarda il terminale del server voce.")
            return
        except (ConnectionRefusedError, OSError) as exc:
            self._send_error_json(502, f"Voice server non raggiungibile: {exc}")
            return
        except http.client.HTTPException as exc:
            # V-2 ve #308: risposta rotta (BadStatusLine, IncompleteRead) → JSON, non un
            # socket chiuso che il browser mostra come «errore di rete»
            self._send_error_json(502, f"Risposta non valida dal voice server: {type(exc).__name__}")
            return
        finally:
            conn.close()

        self.send_response(resp_status)
        self.send_header("Content-Type", resp_ct)
        self.send_header("Content-Length", str(len(resp_body)))
        self.end_headers()
        self.wfile.write(resp_body)

    def _guarda_pagina(self, verso_voce: socket.socket) -> None:
        """V7b (R-619-1-M2): mentre si aspetta la frase dopo, la pagina può chiudere (Gas
        interrotto). Dalla pagina non arriva più niente dopo la richiesta, quindi una
        lettura che torna vuota vuol dire «chiusa»: si chiude subito anche la connessione
        verso il server voce, che smette di sintetizzare. Thread daemon, uno per risposta:
        se la pagina non chiudesse mai il TCP resterebbe fermo qui, senza altro danno."""
        try:
            if self.connection.recv(1, socket.MSG_PEEK):
                return  # dati inattesi dalla pagina: non è una chiusura
        except TimeoutError:
            return  # R-620-1-M2: un tempo scaduto non è una pagina chiusa
        except OSError:
            pass
        try:
            verso_voce.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

    def _inoltra_a_pezzi(self, resp: http.client.HTTPResponse, verso_voce: socket.socket) -> None:
        """V7b: inoltra la risposta a righe (voce frase per frase) senza aspettarne la
        fine, così la pagina comincia a parlare dopo la prima frase. Se la pagina chiude,
        si chiude anche la connessione col server voce (che smette di sintetizzare)."""
        threading.Thread(target=self._guarda_pagina, args=(verso_voce,), daemon=True).start()
        try:
            self._copia_righe(resp)
        finally:
            resp.close()  # la connessione col server voce non resta appesa

    def _copia_righe(self, resp: http.client.HTTPResponse) -> None:
        self.send_response(resp.status)
        self.send_header("Content-Type", resp.getheader("Content-Type", "application/x-ndjson"))
        self.end_headers()
        while True:
            try:
                pezzo = resp.read1(65536)
            except (OSError, http.client.HTTPException) as exc:
                # a metà risposta non si può più mandare un errore JSON: la pagina vede
                # le righe arrivate e la fine senza «fine» (voce interrotta, testo a schermo)
                log.warning("risposta a pezzi interrotta (%s)", type(exc).__name__)
                return
            if not pezzo:
                return
            try:
                self.wfile.write(pezzo)
                self.wfile.flush()
            except OSError:
                return  # pagina chiusa: il finally di _inoltra_a_pezzi chiude anche il server voce

    def _inoltra_semplice(self, metodo: str, percorso: str, body: bytes) -> None:
        """V8: inoltra una richiesta breve (elenco voci, prova di una voce) al server voce
        col token, e rimanda la risposta così com'è."""
        conn = http.client.HTTPConnection(self.voice_host, self.voice_port, timeout=_CONNECT_TIMEOUT)
        try:
            conn.connect()
            conn.sock.settimeout(120)   # una sintesi o l'elenco: mai minuti
            conn.request(metodo, percorso, body=body if metodo == "POST" else None, headers={
                "Authorization": f"Bearer {self.token}",
                **({"Content-Type": "application/json", "Content-Length": str(len(body))}
                   if metodo == "POST" else {})})
            resp = conn.getresponse()
            corpo = resp.read()
            tipo = resp.getheader("Content-Type", "application/octet-stream")
            stato = resp.status
        except (OSError, http.client.HTTPException) as exc:
            self._send_error_json(502, f"Voice server non raggiungibile: {type(exc).__name__}")
            return
        finally:
            conn.close()
        self.send_response(stato)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _send_error_json(self, code: int, msg: str) -> None:
        err = json.dumps({"error": msg}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(err)))
        self.end_headers()
        self.wfile.write(err)

    def _not_found(self) -> None:
        body = b"Not Found"
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_browser_server() -> int:
    _load_dotenv(_GAS_ROOT)

    token = os.environ.get("GAS_VOICE_TOKEN", "").strip()
    if not token:
        print("✗ GAS_VOICE_TOKEN non configurato. Impostalo in .env o esporta la variabile.")
        print("  Genera un token con: openssl rand -hex 32")
        return 1

    voice_url = (os.environ.get("GAS_VOICE_URL") or "http://127.0.0.1:8765").strip().rstrip("/")
    parsed = urllib.parse.urlparse(voice_url)
    voice_host = parsed.hostname or "127.0.0.1"
    voice_port = parsed.port or 8765

    try:
        browser_port = int(os.environ.get("GAS_BROWSER_PORT") or "9000")
    except ValueError:
        print("✗ GAS_BROWSER_PORT non è un intero valido.")
        return 1

    try:
        timeout = int(os.environ.get("GAS_VOICE_TIMEOUT") or "600")
        if timeout <= 0:
            raise ValueError
    except ValueError:
        print("✗ GAS_VOICE_TIMEOUT non è un intero positivo (secondi).")
        return 1

    try:
        finestra = float(os.environ.get("GAS_VOICE_FINESTRA") or "12")
        if not 0 < finestra <= 120:
            raise ValueError
    except ValueError:
        print("✗ GAS_VOICE_FINESTRA non è un numero di secondi tra 0 e 120.")
        return 1

    try:
        max_turni = int(os.environ.get("GAS_VOICE_MAX_TURNI") or "5")
        if not 1 <= max_turni <= 50:
            raise ValueError
    except ValueError:
        print("✗ GAS_VOICE_MAX_TURNI non è un intero tra 1 e 50.")
        return 1

    if not _HTML_FILE.exists():
        print(f"✗ browser_client.html non trovato in {_HERE}")
        return 1

    BrowserProxyHandler.token = token
    BrowserProxyHandler.voice_host = voice_host
    BrowserProxyHandler.voice_port = voice_port
    BrowserProxyHandler.voice_timeout = timeout
    BrowserProxyHandler.finestra = finestra
    BrowserProxyHandler.max_turni = max_turni
    BrowserProxyHandler.interruzione = (os.environ.get("GAS_VOICE_INTERRUZIONE", "").strip().lower()
                                        not in ("0", "false", "no", "off"))

    # V-1 bot #308: a thread, così mentre il forte lavora (fino a GAS_VOICE_TIMEOUT) la
    # pagina si ricarica lo stesso; il server voce dietro resta a un turno alla volta.
    server = ThreadingHTTPServer(("127.0.0.1", browser_port), BrowserProxyHandler)
    print(f"✓ Gas browser client: http://127.0.0.1:{browser_port}/")
    print(f"  → proxy verso voice server: {voice_url} (attesa massima {timeout} s)")
    print("  Ctrl-C per uscire.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Browser server interrotto.")
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(run_browser_server())
