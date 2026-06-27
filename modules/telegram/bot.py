"""
Bridge bot Telegram per GAS — Item 2 roadmap.

Uso:  gas telegram

Configurazione (env):
  TELEGRAM_BOT_TOKEN   — obbligatorio: token del bot (da @BotFather)
  TELEGRAM_ALLOWED_IDS — obbligatorio: chat_id autorizzati, separati da virgola
                         (es. "123456789,987654321"). Senza questa lista nessun
                         messaggio viene elaborato (fail-closed by design).

Sicurezza:
  - Whitelist esplicita: messaggi da ID non in lista vengono silenziosamente
    ignorati (nessuna risposta = nessun fingerprint del bot).
  - Zero apertura di rete IN INGRESSO: solo long-polling outbound (getUpdates).
  - Un GasKernel condiviso per tutti gli ID autorizzati (storia condivisa):
    adatto all'uso personale single-user. Multi-user isolation richiede estensione.

Dipendenze: zero nuove — usa solo urllib.request (stdlib Python).
Fail-safe §9: nessun crash nel loop, errori → log + continuazione.
"""
from __future__ import annotations

import json
import logging
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

log = logging.getLogger(__name__)

_TELEGRAM_API = "https://api.telegram.org/bot"


# ─────────────────────────────────────────── infra HTTP ──

def _tg_post(base_url: str, method: str, payload: Optional[Dict[str, Any]] = None,
             timeout: int = 70) -> Optional[Dict[str, Any]]:
    """HTTP POST minimalista all'API Telegram via urllib (stdlib). Fail-safe §9:
    errori di rete o HTTP → None, mai eccezione propagata."""
    url = f"{base_url}/{method}"
    body = json.dumps(payload or {}).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        log.warning("Telegram %s HTTP %d: %s", method, e.code, e.reason)
        return None
    except urllib.error.URLError as e:
        log.warning("Telegram %s URLError: %s", method, e.reason)
        return None
    except Exception as e:
        log.warning("Telegram %s errore: %s", method, e)
        return None


def _send_text(base_url: str, chat_id: int, text: str) -> None:
    """Invia un messaggio testuale. Tronca a 4096 char (limite Telegram)."""
    if len(text) > 4096:
        text = text[:4090] + "\n…[troncato]"
    _tg_post(base_url, "sendMessage", {"chat_id": chat_id, "text": text})


def _send_typing(base_url: str, chat_id: int) -> None:
    """Mostra l'indicatore 'sta scrivendo…' in Telegram (nessun messaggio)."""
    _tg_post(base_url, "sendChatAction", {"chat_id": chat_id, "action": "typing"})


# ─────────────────────────────────────────── entry point ──

def run_bot(root_dir: Optional[str] = None) -> int:
    """Loop principale del bridge bot. Blocca fino a KeyboardInterrupt (Ctrl-C).
    Exit code: 0 = uscita pulita, 1 = configurazione mancante."""

    # ── Configurazione ──────────────────────────────────────
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("✗ gas telegram: TELEGRAM_BOT_TOKEN non configurato.")
        print("  1. Crea un bot su @BotFather in Telegram.")
        print("  2. Copia il token e imposta: export TELEGRAM_BOT_TOKEN=<token>")
        return 1

    raw_ids = os.environ.get("TELEGRAM_ALLOWED_IDS", "").strip()
    if not raw_ids:
        print("✗ gas telegram: TELEGRAM_ALLOWED_IDS non configurato (fail-closed).")
        print("  Imposta i chat_id autorizzati: export TELEGRAM_ALLOWED_IDS=123456789")
        print("  (per trovare il tuo chat_id manda /start a @userinfobot)")
        return 1

    allowed: Set[int] = set()
    for chunk in raw_ids.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            allowed.add(int(chunk))
        except ValueError:
            print(f"  WARN: '{chunk}' in TELEGRAM_ALLOWED_IDS non è un intero — ignorato")
    if not allowed:
        print("✗ gas telegram: nessun ID autorizzato valido in TELEGRAM_ALLOWED_IDS.")
        return 1

    base_url = f"{_TELEGRAM_API}{token}"

    # ── Verifica connessione ────────────────────────────────
    me = _tg_post(base_url, "getMe")
    if not me or not me.get("ok"):
        print("✗ gas telegram: impossibile connettersi all'API Telegram.")
        print("  Verifica TELEGRAM_BOT_TOKEN e la connessione di rete.")
        return 1
    bot_username = me.get("result", {}).get("username", "bot")
    print(f"✓ gas telegram: connesso come @{bot_username}")
    print(f"  Chat autorizzate: {sorted(allowed)}")
    print("  In ascolto… (Ctrl-C per uscire)\n")

    # ── Kernel GAS condiviso ────────────────────────────────
    root = Path(root_dir or os.getcwd()).resolve()
    # Import pigro per non richiedere gas.py al semplice import del modulo.
    # Aggiunge root se gas.py è lì; altrimenti root.parent (guard per invocazione
    # diretta — in produzione via `gas telegram`, gas è già in sys.modules).
    import sys as _sys
    _sys.path.insert(0, str(root if (root / "gas.py").exists() else root.parent))
    from gas import GasKernel
    kernel = GasKernel(root_dir=str(root))

    # ── Long-polling loop ───────────────────────────────────
    offset = 0
    while True:
        try:
            resp = _tg_post(base_url, "getUpdates",
                            {"offset": offset, "timeout": 60}, timeout=70)
            if resp is None or not resp.get("ok"):
                time.sleep(5)
                continue

            updates: List[Dict[str, Any]] = resp.get("result", [])
            for upd in updates:
                offset = max(offset, int(upd.get("update_id", 0)) + 1)
                _handle_update(base_url, upd, allowed, kernel)

        except KeyboardInterrupt:
            print("\n✓ gas telegram: interruzione ricevuta, uscita.")
            return 0
        except Exception as e:
            log.warning("Errore nel loop di polling: %s — riprendo tra 5s", e)
            time.sleep(5)


# ─────────────────────────────────────────── gestione update ──

def _handle_update(base_url: str, upd: Dict[str, Any],
                   allowed: Set[int], kernel: Any) -> None:
    """Processa un singolo update Telegram. Fail-safe §9: qualunque eccezione
    viene catturata e loggata — il loop esterno NON deve mai crashare."""
    try:
        msg = upd.get("message") or upd.get("edited_message")
        if not msg:
            return

        chat_id: Optional[int] = (msg.get("chat") or {}).get("id")
        text = (msg.get("text") or "").strip()
        if not chat_id or not text:
            return

        if chat_id not in allowed:
            log.warning("Messaggio da chat_id %d non autorizzato — ignorato", chat_id)
            return

        _send_typing(base_url, chat_id)

        parts: List[str] = []
        try:
            for event in kernel.run_turn(text):
                etype = event.get("type")
                if etype == "final":
                    parts.append(event.get("content", ""))
                elif etype == "tool_res":
                    out = (event.get("output") or "").strip()
                    if out:
                        # Tool result compatti: massimo 200 char per non spammare
                        short = out[:200].replace("\n", " ")
                        parts.append(f"[…] {short}")
                elif etype == "error":
                    parts.append(f"✗ {event.get('content', 'errore sconosciuto')}")
        except Exception as e:
            log.warning("run_turn fallita per chat %d: %s", chat_id, e)
            parts.append(f"✗ Errore interno: {str(e)[:120]}")

        reply = "\n\n".join(p for p in parts if p) or "(nessuna risposta)"
        _send_text(base_url, chat_id, reply)

    except Exception as e:
        log.warning("_handle_update fallita: %s", e)
