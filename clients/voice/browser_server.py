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
"""
from __future__ import annotations

import http.client
import json
import logging
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
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

    def log_message(self, fmt: str, *args: object) -> None:
        log.info(fmt, *args)

    def do_GET(self) -> None:
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
                },
            )
            resp = conn.getresponse()
            resp_body = resp.read()
            resp_ct = resp.getheader("Content-Type", "application/octet-stream")
            resp_status = resp.status
        except TimeoutError:
            # V2: scaduto il tempo, Gas può star ancora lavorando: dirlo, non «non raggiungibile»
            self._send_error_json(504, f"Gas non ha risposto entro {self.voice_timeout} s: il lavoro "
                                       "può essere ancora in corso, guarda il terminale del server voce.")
            return
        except (ConnectionRefusedError, OSError) as exc:
            self._send_error_json(502, f"Voice server non raggiungibile: {exc}")
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

    if not _HTML_FILE.exists():
        print(f"✗ browser_client.html non trovato in {_HERE}")
        return 1

    BrowserProxyHandler.token = token
    BrowserProxyHandler.voice_host = voice_host
    BrowserProxyHandler.voice_port = voice_port
    BrowserProxyHandler.voice_timeout = timeout

    server = HTTPServer(("127.0.0.1", browser_port), BrowserProxyHandler)
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
