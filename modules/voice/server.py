"""
HTTP voice endpoint per GAS — FASE 3, Fette 1+2+3.

Endpoint: POST /voice
  Body (testo):  JSON {"prompt": "<testo>"}
  Body (audio):  Content-Type audio/* oppure multipart/form-data con campo 'file'
  Auth:    Header "Authorization: Bearer <token>"

  Output testo (default):
    200:   JSON {"content": "<risposta>"}

  Output audio (se Accept: audio/mpeg o Accept: audio/*):
    200:   byte MP3 grezzi (Content-Type: audio/mpeg)
    502:   JSON {"error": "<msg>"}  — errore ElevenLabs (rete/quota)
    503:   JSON {"error": "<msg>"}  — TTS non disponibile (ELEVENLABS_API_KEY assente)

  Codici errore comuni:
    400:   JSON {"error": "<msg>"}  — prompt mancante/JSON invalido / audio vuoto o invalido
    401:   JSON {"error": "Unauthorized"}
    502:   JSON {"error": "<msg>"}  — errore Groq STT o ElevenLabs TTS (rete/quota)
    503:   JSON {"error": "<msg>"}  — STT/TTS non disponibile (chiave assente)
    500:   JSON {"error": "<msg>"}  — errore pipeline o kernel

Configurazione tramite variabili d'ambiente (da .env o export):
  GAS_VOICE_BIND      — bind address       (default: 127.0.0.1)
  GAS_VOICE_PORT      — porta TCP          (default: 8765)
  GAS_VOICE_TOKEN     — token bearer       OBBLIGATORIO: assente/vuoto → il server non parte
  GROQ_API_KEY        — chiave Groq        OBBLIGATORIO per STT audio; assente → 503
  ELEVENLABS_API_KEY  — chiave ElevenLabs  OBBLIGATORIO per output audio; assente → 503
  ELEVENLABS_VOICE_ID — voice id           (default: JBFqnCBsd6RMkjVDRZzb, George premade)

Sicurezza:
  - Nasce chiuso su 127.0.0.1. Aprire all'esterno SOLO settando GAS_VOICE_BIND.
  - Confronto token a TEMPO COSTANTE via hmac.compare_digest (mai ==).
  - Nessun segreto scritto nei log; ogni tentativo fallito viene loggato con IP + esito.
  - I byte audio (ingresso e uscita) non vengono loggati né scritti su disco; le chiavi non compaiono nei log.
  - CAVEAT PRIVACY (STT): l'audio dell'utente viene inviato ai server Groq (terza parte).
  - CAVEAT PRIVACY (TTS): il testo del kernel viene inviato ai server ElevenLabs (terza parte).
    Trade-off dichiarato: per un agente che tocca dati/lead, questo è egress di dati.
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

from modules.voice.stt import GroqSTTError, parse_audio_body, transcribe_audio
from modules.voice.tts import DEFAULT_VOICE_ID as _TTS_DEFAULT_VOICE_ID
from modules.voice.tts import ElevenLabsTTSError, synthesize_speech

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

    def _send_audio(self, data: bytes) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "audio/mpeg")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _wants_audio(self) -> bool:
        """True se il client dichiara Accept: audio/mpeg o audio/* (non audio generico */*).
        Retrocompatibile: senza header (o Accept: application/json) → False → risposta JSON."""
        accept = self.headers.get("Accept", "")
        return "audio/mpeg" in accept or "audio/*" in accept

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

        content_type = self.headers.get("Content-Type", "")
        ct_base = content_type.split(";")[0].strip().lower()
        is_audio = ct_base.startswith("audio/") or ct_base == "multipart/form-data"

        if is_audio:
            prompt = self._do_stt(raw, content_type)
            if prompt is None:
                return  # risposta errore già inviata
        else:
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

        if self._wants_audio():
            self._do_tts_response(result_content)
        else:
            self._send_json(200, {"content": result_content})

    def _do_tts_response(self, text: str) -> None:
        """Sintetizza text via ElevenLabs e invia i byte MP3. Invia l'errore HTTP se fallisce.
        Se text è vuoto salta la chiamata ElevenLabs e risponde JSON vuoto (mai crash)."""
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "TTS non disponibile: ELEVENLABS_API_KEY non configurata"})
            return

        if not text:
            self._send_json(200, {"content": ""})
            return

        voice_id = (os.environ.get("ELEVENLABS_VOICE_ID") or _TTS_DEFAULT_VOICE_ID).strip() or _TTS_DEFAULT_VOICE_ID

        try:
            audio = synthesize_speech(text, api_key, voice_id)
        except ElevenLabsTTSError as exc:
            log.warning("ElevenLabs TTS error status=%s: %s", exc.status, exc.message)
            self._send_json(502, {"error": f"Errore TTS ElevenLabs: {exc.message}"})
            return
        except OSError as exc:
            log.warning("ElevenLabs TTS network error: %s", exc)
            self._send_json(502, {"error": "Errore di rete verso ElevenLabs TTS"})
            return

        self._send_audio(audio)

    def _do_stt(self, raw: bytes, content_type: str) -> Optional[str]:
        """Trascrive audio → testo via Groq Whisper.
        Invia la risposta HTTP di errore e ritorna None se qualcosa va storto."""
        api_key = os.environ.get("GROQ_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "STT non disponibile: GROQ_API_KEY non configurata"})
            return None

        if not raw:
            self._send_json(400, {"error": "Audio vuoto"})
            return None

        try:
            audio_bytes, filename = parse_audio_body(raw, content_type)
        except ValueError as exc:
            self._send_json(400, {"error": f"Audio non valido: {exc}"})
            return None

        try:
            text = transcribe_audio(audio_bytes, filename, api_key)
        except GroqSTTError as exc:
            if exc.status == 400:
                self._send_json(400, {"error": f"Formato audio non accettato da Groq: {exc.message}"})
            else:
                self._send_json(502, {"error": f"Errore Groq STT: {exc.message}"})
            return None
        except OSError as exc:
            log.warning("Groq STT network error: %s", exc)
            self._send_json(502, {"error": "Errore di rete verso Groq STT"})
            return None

        if not text:
            self._send_json(400, {"error": "Trascrizione vuota (silenzio o formato non supportato)"})
            return None

        return text

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
