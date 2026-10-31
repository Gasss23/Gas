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
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)

_HERE = Path(__file__).parent
_GAS_ROOT = _HERE.parent.parent
_HTML_FILE = _HERE / "browser_client.html"
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
        if self.path not in ("/", "/index.html"):
            self._not_found()
            return
        try:
            html = _HTML_FILE.read_bytes()
        except FileNotFoundError:
            self._not_found()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def do_POST(self) -> None:
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
            resp = conn.getresponse()
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
