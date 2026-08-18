"""
HTTP voice endpoint per GAS — FASE 3, Fetta 1.

Endpoint: POST /voice
  Body:    JSON {"prompt": "<testo>"}
  Auth:    Header "Authorization: Bearer <token>"
  200:     JSON {"content": "<risposta>"}
  400:     JSON {"error": "<msg>"}       — prompt mancante/JSON invalido
  401:     JSON {"error": "Unauthorized"}
  500:     JSON {"error": "<msg>"}       — errore pipeline o kernel

Configurazione tramite variabili d'ambiente (da .env o export):
  GAS_VOICE_BIND   — bind address  (default: 127.0.0.1)
  GAS_VOICE_PORT   — porta TCP     (default: 8765)
  GAS_VOICE_TOKEN  — token bearer  OBBLIGATORIO: assente/vuoto → il server non parte

Sicurezza:
  - Nasce chiuso su 127.0.0.1. Aprire all'esterno SOLO settando GAS_VOICE_BIND.
  - Confronto token a TEMPO COSTANTE via hmac.compare_digest (mai ==).
  - Nessun segreto scritto nei log; ogni tentativo fallito viene loggato con IP + esito.
  - Kernel GasKernel istanziato UNA VOLTA all'avvio (stateful, storia condivisa).
  - Single-thread nativo: http.server.HTTPServer senza ThreadingMixIn, nessun lock.
  - Fail-safe §9: eccezione in run_turn → 500 + log in gas_debug.log, server vivo.
"""
from __future__ import annotations

import hmac
import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, Optional

log = logging.getLogger(__name__)

_ENDPOINT = "/voice"


def _token_ok(received: str, expected: str) -> bool:
    """Confronto a tempo costante. False se uno dei due è vuoto."""
    if not received or not expected:
        return False
    return hmac.compare_digest(received.encode("utf-8"), expected.encode("utf-8"))


class VoiceHandler(BaseHTTPRequestHandler):
    """Handler HTTP per POST /voice. Kernel e token iniettati dal runner prima del bind."""

    kernel: Any = None
    token: str = ""

    def log_message(self, fmt: str, *args: Any) -> None:
        log.info(fmt, *args)

    def _send_json(self, code: int, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _check_auth(self) -> bool:
        """Verifica il token bearer. Logga ogni fallimento con IP; MAI il token ricevuto."""
        hdr = self.headers.get("Authorization", "")
        parts = hdr.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            log.warning("AUTH FAIL ip=%s motivo=header_mancante_o_malformato", self.client_address[0])
            return False
        if not _token_ok(parts[1].strip(), self.token):
            log.warning("AUTH FAIL ip=%s motivo=token_non_valido", self.client_address[0])
            return False
        return True

    def do_POST(self) -> None:
        if self.path != _ENDPOINT:
            self._send_json(404, {"error": "Not Found"})
            return

        if not self._check_auth():
            self._send_json(401, {"error": "Unauthorized"})
            return

        try:
            length = int(self.headers.get("Content-Length", 0) or 0)
        except ValueError:
            self._send_json(400, {"error": "Content-Length non valido"})
            return
        raw = self.rfile.read(length) if length > 0 else b""
        try:
            data: Dict[str, Any] = json.loads(raw) if raw else {}
        except (json.JSONDecodeError, ValueError):
            self._send_json(400, {"error": "Body JSON non valido"})
            return

        prompt = (data.get("prompt") or "").strip()
        if not prompt:
            self._send_json(400, {"error": "Campo 'prompt' mancante o vuoto"})
            return

        try:
            result_content: Optional[str] = None
            for event in self.kernel.run_turn(prompt):
                etype = event.get("type")
                if etype == "final":
                    result_content = event.get("content", "")
                    break
                elif etype == "error":
                    self._send_json(500, {"error": event.get("content", "Errore pipeline")})
                    return
                # type="tool_res": consumato in silenzio
        except Exception as exc:
            log.warning("run_turn eccezione: %s", exc)
            self._send_json(500, {"error": "Errore interno del kernel"})
            return

        if result_content is None:
            self._send_json(500, {"error": "Nessuna risposta dal kernel"})
            return

        self._send_json(200, {"content": result_content})

    def _method_not_allowed(self) -> None:
        self._send_json(405, {"error": "Method Not Allowed"})

    do_GET = _method_not_allowed
    do_PUT = _method_not_allowed
    do_DELETE = _method_not_allowed
    do_PATCH = _method_not_allowed


def run_server(root_dir: Optional[str] = None) -> int:
    """Avvia il server HTTP voice. Blocca fino a KeyboardInterrupt.
    Exit code: 0 = uscita pulita, 1 = configurazione mancante."""

    token = os.environ.get("GAS_VOICE_TOKEN", "").strip()
    if not token:
        print("✗ gas voice: GAS_VOICE_TOKEN non configurato (fail-closed).")
        print("  Genera un token casuale e impostalo: export GAS_VOICE_TOKEN=$(openssl rand -hex 32)")
        return 1

    bind = (os.environ.get("GAS_VOICE_BIND") or "127.0.0.1").strip() or "127.0.0.1"
    try:
        port = int(os.environ.get("GAS_VOICE_PORT") or "8765")
    except ValueError:
        print("✗ gas voice: GAS_VOICE_PORT non è un numero intero valido.")
        return 1

    root = Path(root_dir or os.getcwd()).resolve()

    import sys as _sys
    _sys.path.insert(0, str(root if (root / "gas.py").exists() else root.parent))
    from gas import GasKernel  # import pigro: non richiede gas.py al semplice import del modulo

    kernel = GasKernel(root_dir=str(root))

    VoiceHandler.kernel = kernel
    VoiceHandler.token = token

    server = HTTPServer((bind, port), VoiceHandler)
    print(f"✓ gas voice: in ascolto su http://{bind}:{port}{_ENDPOINT}")
    print("  Ctrl-C per uscire.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ gas voice: interruzione ricevuta, uscita.")
    finally:
        server.server_close()

    return 0
