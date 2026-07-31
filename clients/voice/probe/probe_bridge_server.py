"""
probe_bridge_server.py — WSL / Linux
Server HTTP minimo per testare il forwarding WSL2 → Windows.

Espone POST /ping  →  { "pong": true, "server": "WSL" }
Da usare in coppia con win_bridge_test.py (Windows).

Uso:
    python probe_bridge_server.py             # default 127.0.0.1:8765
    python probe_bridge_server.py --port 9000
    python probe_bridge_server.py --host 0.0.0.0  # accetta da tutti gli IP

Dipendenze: solo stdlib Python (http.server, json).
"""

import argparse
import json
import logging
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s")


class PingHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/ping":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        logging.info("POST /ping  source=%s", payload.get("source", "?"))

        response = json.dumps({"pong": True, "server": "WSL"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, fmt, *args):
        # Sopprimo il log duplicato di BaseHTTPRequestHandler
        pass


def wsl_ip() -> str:
    """Ricava l'IP WSL visibile da Windows tramite 'hostname -I' (primo IP)."""
    import subprocess
    try:
        out = subprocess.check_output(["hostname", "-I"], text=True).strip()
        return out.split()[0] if out.split() else "?"
    except Exception:
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception:
            return "?"


def main():
    parser = argparse.ArgumentParser(description="Server HTTP ping per probe bridge WSL↔Windows")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), PingHandler)
    wsl = wsl_ip()
    logging.info("Server avviato su %s:%d", args.host, args.port)
    logging.info("IP WSL visibile da Windows: %s  (usa --host %s --port %d in win_bridge_test.py)", wsl, wsl, args.port)
    logging.info("Premi Ctrl+C per fermare.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server fermato.")


if __name__ == "__main__":
    main()
