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
from concurrent.futures import ThreadPoolExecutor
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

log = logging.getLogger(__name__)

_TELEGRAM_API = "https://api.telegram.org/bot"
# Limite Telegram del testo di sendMessage, contato in unità UTF-16
# (un'emoji fuori dal BMP vale 2). Read-back oltre il limite → niente invio.
TELEGRAM_MAX_CHARS: int = 4096
# C4b-2: callback_data dei bottoni di firma = "ok:<uuid>" / "no:<uuid>" (39 byte,
# limite Telegram 64). Solo UUID canonico minuscolo, come lo genera la coda.
# Da usare SOLO con fullmatch (R-c4b2-4: `$` accetterebbe un "\n" finale).
_CALLBACK_RE = re.compile(
    r"(ok|no):([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})")
# Quanta parte dell'output di un'azione approvata torna all'operatore (UTF-16).
ESITO_OUTPUT_MAX: int = 1500


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


def parse_allowed_ids(raw: str) -> Tuple[Set[int], List[str]]:
    """TELEGRAM_ALLOWED_IDS → (ID interi validi, chunk scartati perché non interi)."""
    allowed: Set[int] = set()
    scartati: List[str] = []
    for chunk in (raw or "").split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            allowed.add(int(chunk))
        except ValueError:
            scartati.append(chunk)
    return allowed, scartati


# ─────────────────────────────────── read-back approvazioni (C4b-1/2) ──
# Testo semplice SENZA parse_mode: Markdown/HTML nel testo di terzi potrebbe
# nascondere contenuto. Bottoni Approva/Rifiuta dal C4b-2.

def lunghezza_telegram(text: str) -> int:
    """Lunghezza come la conta Telegram (unità UTF-16)."""
    return len(text.encode("utf-16-le")) // 2


def componi_read_back(approval: Dict[str, Any]) -> str:
    """Testo del read-back di una richiesta 'pending' (riga di approvals).
    `tool_args_json` INTEGRALE e verbatim, mai troncato (§4c)."""
    scad = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(approval["ts_expiry"]))
    return (
        "GAS chiede la tua firma\n\n"
        f"Azione: {approval['azione_leggibile']}\n"
        f"Tool: {approval['tool_name']}\n\n"
        "ARGOMENTI (testo grezzo, può contenere testo di terzi):\n"
        f"{approval['tool_args_json']}\n\n"
        f"ID approvazione: {approval['id']}\n"
        f"Scadenza: {scad}\n\n"
        "Nessuna azione verrà eseguita senza la tua firma: "
        "usa i bottoni Approva / Rifiuta qui sotto."
    )


# R-263-1: riempitivi Hangul (categoria Lo) che si vedono come spazio vuoto.
_INVISIBILI_EXTRA = frozenset({0x115F, 0x1160, 0x3164, 0xFFA0,
                                0x034F, 0x2800,  # R-264-2: CGJ, braille vuoto
                                0x17B4, 0x17B5, 0x0338, 0xFFFC})  # V-2 verifica esterna #180


def rendi_visibili(testo: str, a_capo: bool = True) -> str:
    """Caratteri invisibili o di controllo (\\r, BOM, larghezza zero, bidi, separatori
    di riga Unicode, C0/C1) resi come <U+XXXX>; \\n e \\t restano (review #262:
    righe diverse non devono sembrare uguali, un nome non deve falsare il messaggio).
    a_capo=False (V-6 verifica esterna #180, per i NOMI di file): anche \\n e \\t
    diventano <U+000A>/<U+0009>, così un nome non può aggiungere righe al messaggio."""
    out = []
    for ch in testo:
        if ch in "\n\t" and a_capo:
            out.append(ch)
        elif (unicodedata.category(ch) in ("Cc", "Cf", "Zl", "Zp", "Co", "Cs", "Cn")
              or (unicodedata.category(ch) == "Zs" and ch != " ")  # R-263-1: NBSP & c.
              or ord(ch) in _INVISIBILI_EXTRA
              or 0xFE00 <= ord(ch) <= 0xFE0F or 0xE0100 <= ord(ch) <= 0xE01EF):
            out.append(f"<U+{ord(ch):04X}>")
        else:
            out.append(ch)
    return "".join(out)


def tronca_visibile(testo: Any, n: int) -> str:
    """rendi_visibili su una riga e taglio a `n` caratteri con «…», senza spezzare
    una sequenza «<U+XXXX>» (al massimo 10 caratteri): il «<» si cerca SOLO in coda
    (R-383-1: un «<» letterale prima non deve cancellare il resto del valore)."""
    t = rendi_visibili(str(testo), a_capo=False)
    if len(t) <= n:
        return t
    t = t[:n]
    k = t.rfind("<", max(0, len(t) - 10))
    if k != -1 and ">" not in t[k:]:
        t = t[:k]
    return t + "…"


def tronca_visibile_coda(testo: Any, n: int) -> str:
    """Come tronca_visibile ma tiene la CODA (V-1 bot #230: in un percorso lungo deve
    restare visibile il nome del file): «…» + ultimi n caratteri, senza iniziare a
    metà di una sequenza «<U+XXXX>» (cercata solo nei primi 10 caratteri)."""
    t = rendi_visibili(str(testo), a_capo=False)
    if len(t) <= n:
        return t
    if n <= 0:  # R-388-2: t[-0:] prenderebbe tutto
        return "…"
    t = t[-n:]
    k = t.find(">", 0, 10)
    if k != -1 and "<" not in t[:k]:
        t = t[k + 1:]
    return "…" + t


def _blocco_modello(testo: str) -> str:
    """Testo del modello rientrato con "│ " su ogni riga: non può imitare le
    intestazioni del messaggio (review #262), invisibili resi visibili."""
    return "\n".join("│ " + r for r in rendi_visibili(testo).split("\n"))


def componi_read_back_codice(approval: Dict[str, Any], diff: str) -> str:
    """Read-back di un write_file di LIVELLO 2 (schema 1A: file delicato). Al posto
    del contenuto integrale mostra il DIFF REALE generato dal kernel rispetto al file
    attuale, la cui impronta (base) e il percorso RISOLTO sono negli argomenti firmati:
    se il file cambia prima dell'esecuzione la scrittura viene rifiutata, quindi il
    diff è esattamente ciò che verrà applicato. Ordine (review #262): prima il file
    vero e il diff, poi pro e contro (testo del modello, rientrato, non verificato).
    Tutti gli argomenti ammessi sono mostrati (il kernel rifiuta chiavi extra)."""
    args = json.loads(approval["tool_args_json"])
    scad = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(approval["ts_expiry"]))
    base = str(args.get("_base_sha256", ""))
    stato_base = ("file NUOVO (oggi non esiste)" if base == "assente"
                  else f"modifica del file attuale (impronta {base[:12]}…)")
    nome = rendi_visibili(str(args["relative_path"]), a_capo=False)
    reale = rendi_visibili(str(args.get("_file_reale", "")), a_capo=False)
    via = f" (chiesto come «{nome}»)" if nome != reale else ""
    return (
        "GAS chiede la tua firma — FILE DELICATO (codice/configurazione)\n\n"
        f"File: {reale}{via}\n"
        f"Tipo: {stato_base}. Se il file cambia prima della firma, la modifica NON "
        "viene applicata.\n\n"
        "DIFF REALE (calcolato da Gas sul file, righe - tolte, + aggiunte):\n"
        f"{diff}\n"
        "PRO (scritti dal modello, non verificati):\n"
        f"{_blocco_modello(str(args['pro']))}\n\n"
        "CONTRO (scritti dal modello, non verificati):\n"
        f"{_blocco_modello(str(args['contro']))}\n\n"
        f"ID approvazione: {approval['id']}\n"
        f"Scadenza: {scad}\n\n"
        "Nessuna modifica verrà applicata senza la tua firma: "
        "usa i bottoni Approva / Rifiuta qui sotto."
    )


def bottoni_firma(approval_id: str) -> Dict[str, Any]:
    """Tastiera inline [✅ Approva] [❌ Rifiuta] per una richiesta (§4b passo 3)."""
    return {"inline_keyboard": [[
        {"text": "✅ Approva", "callback_data": f"ok:{approval_id}"},
        {"text": "❌ Rifiuta", "callback_data": f"no:{approval_id}"},
    ]]}


# R-c4b1-3: invio a tutti i destinatari IN PARALLELO, così il turno che chiede una
# firma resta fermo al massimo ~15 s in tutto (non 15 s per destinatario).
INVIO_TIMEOUT_SECS = 15
_INVIO_MAX_THREAD = 8


def _invia_a_tutti(base_url: str, ids: Set[int], payload: Dict[str, Any],
                   etichetta: str) -> int:
    """sendMessage di `payload` (+ chat_id) a ogni ID, in parallelo. Ritorna quanti
    l'hanno ricevuto (risposta ok=True). Un destinatario che fallisce o solleva
    conta come non consegnato; il dettaglio va solo nel log (niente token)."""
    def _uno(chat_id: int) -> bool:
        try:
            resp = _tg_post(base_url, "sendMessage", {"chat_id": chat_id, **payload},
                            timeout=INVIO_TIMEOUT_SECS)
            return isinstance(resp, dict) and resp.get("ok") is True
        except Exception as e:
            log.warning("%s: errore di invio a chat_id %d: %s", etichetta, chat_id,
                        type(e).__name__)
            return False

    ordinati = sorted(ids)
    with ThreadPoolExecutor(max_workers=max(1, min(len(ordinati), _INVIO_MAX_THREAD))) as ex:
        esiti = list(ex.map(_uno, ordinati))
    for chat_id, ok in zip(ordinati, esiti):
        if not ok:
            log.warning("%s: invio a chat_id %d fallito", etichetta, chat_id)
    return sum(esiti)


def invia_read_back(text: str, approval_id: Optional[str] = None) -> Tuple[bool, str]:
    """Invia `text` (senza parse_mode, senza anteprima link) con i bottoni di firma
    di `approval_id` a ogni ID in TELEGRAM_ALLOWED_IDS. Senza un ID valido niente
    invio: una richiesta senza bottoni non sarebbe firmabile (fail-closed).
    (True, '') se ALMENO un destinatario l'ha ricevuto (risposta ok=True);
    altrimenti (False, motivo). Mai troncamento: testo oltre TELEGRAM_MAX_CHARS
    → (False, ...) senza invio. Fail-safe §9: nessuna eccezione propagata."""
    try:
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            return False, "TELEGRAM_BOT_TOKEN mancante"
        allowed, _ = parse_allowed_ids(os.environ.get("TELEGRAM_ALLOWED_IDS", ""))
        if not allowed:
            return False, "TELEGRAM_ALLOWED_IDS mancante o senza ID validi"
        if lunghezza_telegram(text) > TELEGRAM_MAX_CHARS:
            return False, "testo oltre il limite Telegram"
        if not isinstance(approval_id, str) or not _CALLBACK_RE.fullmatch(f"ok:{approval_id}"):
            return False, "ID approvazione non valido"
        base_url = f"{_TELEGRAM_API}{token}"
        consegnati = _invia_a_tutti(base_url, allowed,
                                    {"text": text,
                                     # R-c4b1-2: niente anteprima: un URL di terzi negli
                                     # args non deve diventare una card nel messaggio.
                                     "link_preview_options": {"is_disabled": True},
                                     "reply_markup": bottoni_firma(approval_id)},
                                    "read-back")
        if consegnati == 0:
            return False, "invio fallito verso tutti i destinatari"
        return True, ""
    except Exception as e:
        # Il dettaglio resta nella scatola nera: non torna al chiamante (può
        # contenere l'URL dell'API, cioè il token).
        log.warning("read-back: errore di invio: %s", e)
        return False, "errore di invio"


def invia_notifica(text: str) -> Tuple[bool, str]:
    """Messaggio solo informativo (niente bottoni, niente parse_mode, niente
    anteprima dei link) a ogni ID in TELEGRAM_ALLOWED_IDS. Usato dal giro
    notturno per il riepilogo del mattino (FASE 4.5 fetta 2). Stesse regole di
    invia_read_back: (True, '') se almeno un destinatario l'ha ricevuto,
    altrimenti (False, motivo); oltre TELEGRAM_MAX_CHARS niente invio.
    Fail-safe §9: nessuna eccezione propagata."""
    try:
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            return False, "TELEGRAM_BOT_TOKEN mancante"
        allowed, _ = parse_allowed_ids(os.environ.get("TELEGRAM_ALLOWED_IDS", ""))
        if not allowed:
            return False, "TELEGRAM_ALLOWED_IDS mancante o senza ID validi"
        if lunghezza_telegram(text) > TELEGRAM_MAX_CHARS:
            return False, "testo oltre il limite Telegram"
        base_url = f"{_TELEGRAM_API}{token}"
        consegnati = _invia_a_tutti(base_url, allowed,
                                    {"text": text,
                                     "link_preview_options": {"is_disabled": True}},
                                    "notifica")
        if consegnati == 0:
            return False, "invio fallito verso tutti i destinatari"
        return True, ""
    except Exception as e:
        # Come in invia_read_back: il dettaglio può contenere l'URL con il token.
        log.warning("notifica: errore di invio: %s", e)
        return False, "errore di invio"


MAX_SCADUTE_ELENCATE = 10


def componi_avviso_scadute(righe: List[Dict[str, Any]]) -> str:
    """C5: testo dell'avviso «richieste di firma scadute» (solo informativo). Le
    azioni sono rese visibili su una riga e troncate; al massimo
    MAX_SCADUTE_ELENCATE voci, le altre contate."""
    testo = [f"⌛ {len(righe)} richiesta/e di firma scaduta/e senza risposta: "
             "NON eseguite. Se servono, Gas deve richiederle."]
    for r in righe[:MAX_SCADUTE_ELENCATE]:
        azione = tronca_visibile(r.get("azione_leggibile") or "", 120)
        tool = tronca_visibile(r.get("tool_name") or "", 60)
        testo.append(f"- {azione} ({tool}) — ID {str(r.get('id') or '')[:8]}")
    if len(righe) > MAX_SCADUTE_ELENCATE:
        testo.append(f"… e altre {len(righe) - MAX_SCADUTE_ELENCATE}.")
    return "\n".join(testo)


def avvisa_firme_scadute(memory: Any) -> int:
    """C5: chiude le richieste di firma scadute (memory.scadi_approvazioni) e ne avvisa
    l'operatore su Telegram una volta sola. Ritorna quante ne ha chiuse. Fail-safe §9:
    nessuna eccezione propagata; invio fallito → warning (le righe restano chiuse:
    l'avviso non si ripete, il conteggio resta in gas doctor e nel diario delle firme)."""
    try:
        if memory is None:
            return 0
        righe = memory.scadi_approvazioni()
        if not righe:
            return 0
        inviato, motivo = invia_notifica(componi_avviso_scadute(righe))
        if not inviato:
            log.warning("firme scadute: avviso non inviato (%s)", motivo)
        return len(righe)
    except Exception as e:
        log.warning("firme scadute: controllo fallito: %s", e)
        return 0


# ─────────────────────────────────────────── entry point ──

def run_bot(root_dir: Optional[str] = None) -> int:
    """Loop principale del bridge bot. Blocca fino a KeyboardInterrupt (Ctrl-C).
    Exit code: 0 = uscita pulita, 1 = configurazione mancante."""
    global _BOT_USERNAME  # R-403-3

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

    allowed, scartati = parse_allowed_ids(raw_ids)
    for chunk in scartati:
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
    username = (me.get("result") or {}).get("username")
    # R-403-2: senza username (None) i comandi con «@…» si accettano come prima.
    _BOT_USERNAME = username if isinstance(username, str) and username else None
    print(f"✓ gas telegram: connesso come @{_BOT_USERNAME or 'bot'}")
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
    ultimo_controllo_scadute = float("-inf")  # R-381-2: primo controllo subito
    while True:
        try:
            # C5: al massimo una volta al minuto chiude le firme scadute e avvisa.
            if time.monotonic() - ultimo_controllo_scadute >= 60:
                ultimo_controllo_scadute = time.monotonic()
                avvisa_firme_scadute(getattr(kernel, "memory", None))
                _raccogli_giri()
            # allowed_updates esplicito: Telegram ricorda l'ultimo valore usato,
            # senza callback_query i bottoni di firma resterebbero muti.
            resp = _tg_post(base_url, "getUpdates",
                            {"offset": offset, "timeout": 60,
                             "allowed_updates": ["message", "edited_message",
                                                 "callback_query"]}, timeout=70)
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


# ─────────────────────────────── giro notturno da Telegram (R1) ──

# R1: `/notte` lancia un giro completo, `/compito <nome>` un solo compito del catalogo.
# Il giro parte in un processo a parte (`gas.py notte [nome]`): il bot resta in
# ascolto, il lock del giro impedisce i doppioni e il riepilogo arriva su Telegram a
# fine giro, come dal timer. Il nome passa come argomento (niente shell) e solo se
# rispetta il formato del catalogo.
# V-3 verifica esterna #233: separatore solo spazio o tab (non spazi Unicode).
# V-1 verifica esterna #233: il nome non inizia con «-» (mai un'opzione per gas.py).
_COMANDO_GIRO_RE = re.compile(r"/(notte|compito)(?:@(\w+))?(?:[ \t]+(.*))?", re.I | re.S)
_NOME_COMPITO_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,39}")
_giri_lanciati: List[Any] = []
# V-3 bot #233: «/notte@AltroBot» non è per Gas. Impostato da run_bot (getMe).
_BOT_USERNAME: Optional[str] = None


def comando_giro(text: Any) -> Optional[Tuple[str, Optional[str]]]:
    """None se il testo non è un comando del giro; altrimenti ('notte', None),
    ('compito', nome) o ('errore', messaggio per l'operatore). Mai eccezioni."""
    try:
        m = _COMANDO_GIRO_RE.fullmatch(text.strip()) if isinstance(text, str) else None
        if not m:
            return None
        destinatario = m.group(2)
        if (destinatario and _BOT_USERNAME
                and destinatario.casefold() != _BOT_USERNAME.casefold()):
            return None  # comando per un altro bot del gruppo
        cmd, arg = m.group(1).lower(), (m.group(3) or "").strip()
        if cmd == "notte":
            if arg:
                return ("errore", "/notte non vuole argomenti. Per un solo compito: /compito <nome>")
            return ("notte", None)
        if not arg:
            return ("errore", "Uso: /compito <nome> (il nome come nel catalogo dei compiti)")
        if not _NOME_COMPITO_RE.fullmatch(arg):
            return ("errore", "Nome del compito non valido: solo a-z 0-9 _ -, max 40.")
        return ("compito", arg)
    except Exception:
        return None


_GAS_PY: Path = Path(__file__).resolve().parents[2] / "gas.py"
# R-392-2: l'uscita del giro lanciato dal bot va qui (come launchd.log per il timer).
LOG_GIRO_TELEGRAM = "telegram_giro.log"


# R-393-1: testo fisso (nessun dato del processo) per un giro morto prima di partire.
TESTO_GIRO_NON_PARTITO = ("✗ Il giro lanciato da Telegram si è fermato prima di partire. "
                          "Dettagli in .gas_notte/" + LOG_GIRO_TELEGRAM)


def _giro_partito(voce: Dict[str, Any]) -> bool:
    """True se il giro ha scritto il marcatore di avvio dopo il lancio, cioè è
    arrivato a `esegui_notte`, che da lì avvisa da sé in ogni caso (riepilogo,
    «INTERROTTO», «NON avviato»: R-394-1). Nel dubbio True: meglio un avviso in
    meno che uno doppio."""
    try:
        from modules.notte.notte import AVVIO, NOTTE_DIR
        marcatore = Path(voce["root"]) / NOTTE_DIR / AVVIO
        return marcatore.stat().st_mtime >= voce["t0"] - 1
    except FileNotFoundError:
        return False
    except Exception:
        return True


def _raccogli_giri() -> int:
    """Toglie dalla lista i giri finiti (niente processi zombie). Ritorna quanti
    sono ancora in corso. R-392-2/R-393-1/R-394-1: un giro morto prima di
    `esegui_notte` (nessun marcatore di avvio scritto dopo il lancio) finisce in
    gas_debug.log e su Telegram. Codice 2 escluso: lock occupato, già notificato."""
    for voce in list(_giri_lanciati):
        try:
            rc = voce["p"].poll()
            if rc is None:
                continue
            if rc != 2 and not _giro_partito(voce):
                log.warning("giro lanciato da Telegram uscito con codice %s senza "
                            "riepilogo (vedi .gas_notte/%s)", rc, LOG_GIRO_TELEGRAM)
                if os.environ.get("GAS_NOTTE_TELEGRAM", "").strip() != "0":
                    invia_notifica(TESTO_GIRO_NON_PARTITO)
        except Exception as e:
            log.warning("raccolta del giro lanciato da Telegram fallita: %s", e)
        _giri_lanciati.remove(voce)
    return len(_giri_lanciati)


def lancia_giro(root: Path, nome: Optional[str] = None) -> str:
    """Avvia `gas.py notte [nome]` in un processo a parte e ritorna la risposta per
    l'operatore. Un solo giro lanciato da qui alla volta. Mai eccezioni."""
    try:
        if _raccogli_giri():
            return "Un giro lanciato da qui è ancora in corso: aspetta il suo riepilogo."
        if nome is not None and not _NOME_COMPITO_RE.fullmatch(nome):
            return "Nome del compito non valido."
        # R-392-1: gas.py è quello accanto a questo modulo, non quello della cartella
        # da cui è partito il bot.
        if not _GAS_PY.is_file():
            log.warning("lancia_giro: gas.py non trovato in %s", _GAS_PY)  # R-393-2
            return "✗ Giro NON avviato: gas.py non trovato (dettagli in gas_debug.log)."
        cmd = [sys.executable, str(_GAS_PY), "notte"] + ([nome] if nome else [])
        cartella = root / ".gas_notte"
        cartella.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        with open(cartella / LOG_GIRO_TELEGRAM, "ab") as out:
            p = subprocess.Popen(cmd, cwd=str(root), stdin=subprocess.DEVNULL,
                                 stdout=out, stderr=subprocess.STDOUT,
                                 start_new_session=True, close_fds=True)
        _giri_lanciati.append({"p": p, "t0": t0, "root": root})
        cosa = f"Compito «{nome}» avviato" if nome else "Giro notturno avviato"
        if os.environ.get("GAS_NOTTE_TELEGRAM", "").strip() == "0":  # V-2 bot #233
            return (f"{cosa}. Riepilogo su Telegram spento (GAS_NOTTE_TELEGRAM=0): "
                    "a fine giro leggilo in .gas_notte/ultimo_giro.md")
        return f"{cosa}: il riepilogo arriva qui a fine giro."
    except Exception as e:
        log.warning("lancia_giro fallita: %s", e)
        return "✗ Giro NON avviato: errore nel lancio (dettagli in gas_debug.log)."


# ─────────────────────────────────────────── gestione update ──

def _handle_update(base_url: str, upd: Dict[str, Any],
                   allowed: Set[int], kernel: Any) -> None:
    """Processa un singolo update Telegram. Fail-safe §9: qualunque eccezione
    viene catturata e loggata — il loop esterno NON deve mai crashare."""
    try:
        cq = upd.get("callback_query")
        if cq:
            gestisci_callback(base_url, cq, allowed, kernel)
            return
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

        giro = comando_giro(text)
        if giro is not None:
            tipo, valore = giro
            if tipo == "errore":
                _send_text(base_url, chat_id, valore or "")
            else:
                root = getattr(kernel, "root", None) or Path(os.getcwd()).resolve()
                _send_text(base_url, chat_id, lancia_giro(Path(root), valore))
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


# ─────────────────────────────────── firma via bottoni (C4b-2) ──

def _tronca_utf16(text: str, max_units: int) -> str:
    """Tronca `text` a `max_units` unità UTF-16 senza spezzare una coppia surrogata."""
    if lunghezza_telegram(text) <= max_units:
        return text
    out, n = [], 0
    for ch in text:
        w = 2 if ord(ch) > 0xFFFF else 1
        if n + w > max_units:
            break
        out.append(ch)
        n += w
    return "".join(out)


def _id_intero(v: Any) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def componi_esito_firma(azione: str, approval_id: str, risolta: bool, motivo: str,
                        res: Optional[Dict[str, Any]]) -> str:
    """Messaggio all'operatore dopo un click. Testo semplice; l'output di
    un'azione eseguita è testo grezzo (può contenere testo di terzi), troncato."""
    if not risolta:
        return f"Nessuna modifica per la richiesta {approval_id}: {motivo}"
    res = res or {}
    if azione == "no":
        return f"❌ Rifiutata: azione {res.get('tool') or ''} NON eseguita.\nID: {approval_id}"
    if res.get("eseguita"):
        testo = (f"✅ Approvata ed eseguita: {res.get('tool')}\nID: {approval_id}\n"
                 f"Esito: {res.get('esito')}")
    elif res.get("stato") == "incerta":  # R-c4b3-5: partita ma senza esito
        testo = (f"⚠️ Approvata, ma esito INCERTO: {res.get('tool') or ''} può essere "
                 f"partita e aver fatto solo una parte del lavoro. Controlla prima di "
                 f"ripetere.\nID: {approval_id}\nEsito: {res.get('esito') or 'ignoto'}")
    else:
        testo = (f"⚠️ Firma registrata ma azione {res.get('tool') or ''} NON eseguita: "
                 f"{res.get('esito') or 'motivo ignoto'}\nID: {approval_id}")
    out = (res.get("output") or "").strip()
    if out:
        corto = _tronca_utf16(out, ESITO_OUTPUT_MAX)
        nota = "" if corto == out else " — troncato"
        testo += f"\n\nOUTPUT (testo grezzo, può contenere testo di terzi{nota}):\n{corto}"
    return _tronca_utf16(testo, TELEGRAM_MAX_CHARS)


def _riprova_orfana(memory: Any, kernel: Any, aid: str,
                    motivo: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """R-c4b2-2: richiesta 'approved' ma MAI reclamata (crash tra firma ed
    esecuzione). Nuovo click su Approva entro la scadenza → applica_firma (il
    reclamo impedisce comunque una seconda esecuzione); oltre la scadenza →
    nessuna esecuzione e messaggio esplicito. R-c4b3-3: già reclamata ma con
    l'esito mai entrato in storia → recupera_esito_firma (non esegue nulla).
    Altri casi → motivo invariato."""
    try:
        row = memory.get_approval(aid)
        if row is None or row.get("stato") != "approved":
            return None, motivo
        if memory.get_esecuzione(aid):
            recupera = getattr(kernel, "recupera_esito_firma", None)
            if not callable(recupera):  # V-1 verifica esterna #241: niente recupero muto
                log.warning("callback: id=%s già reclamata ma il kernel non sa "
                            "recuperarne l'esito", aid)
                return None, motivo
            return recupera(aid), motivo
        if time.time() < row["ts_expiry"]:
            log.warning("callback: id=%s approvata ma mai eseguita — nuovo tentativo", aid)
            return kernel.applica_firma(aid), motivo
        return None, "approvata ma MAI eseguita, e ormai scaduta: non verrà eseguita."
    except Exception as e:
        log.warning("callback: verifica orfana id=%s eccezione: %s", aid, e)
        return None, motivo


def gestisci_callback(base_url: str, cq: Dict[str, Any], allowed: Set[int],
                      kernel: Any) -> None:
    """Click su [✅ Approva] / [❌ Rifiuta] (§4b passi 5-9, §4e).
    - mittente (from.id) e chat del messaggio devono essere in TELEGRAM_ALLOWED_IDS,
      altrimenti rifiuto SILENZIOSO (nessuna risposta);
    - callback_data rigida "ok|no:<uuid>";
    - la firma la registra QUESTO bridge (resolve_approval: una sola volta, mai
      dopo la scadenza, hash verificato); poi il kernel applica lo stato deciso
      (applica_firma: esegue gli args salvati al massimo una volta).
    Fail-safe §9: nessuna eccezione propagata; errore → nessuna esecuzione."""
    try:
        uid = (cq.get("from") or {}).get("id")
        if not _id_intero(uid) or uid not in allowed:
            log.warning("callback da user_id %r non autorizzato — ignorata", uid)
            return
        msg = cq.get("message") or {}
        chat_id = (msg.get("chat") or {}).get("id")
        if chat_id is not None and (not _id_intero(chat_id) or chat_id not in allowed):
            log.warning("callback da chat %r non autorizzata — ignorata", chat_id)
            return
        cq_id = cq.get("id")
        m = _CALLBACK_RE.fullmatch(cq["data"]) if isinstance(cq.get("data"), str) else None
        if not m:
            _tg_post(base_url, "answerCallbackQuery",
                     {"callback_query_id": cq_id, "text": "Richiesta non valida."}, timeout=15)
            return
        azione, aid = m.group(1), m.group(2)
        stato = "approved" if azione == "ok" else "rejected"
        # R-c4b2-5: risposta al click e via i bottoni PRIMA dell'esecuzione (che può
        # durare fino a 60 s). Il vero blocco contro il doppio click resta il DB.
        _tg_post(base_url, "answerCallbackQuery",
                 {"callback_query_id": cq_id, "text": "Firma ricevuta."}, timeout=15)
        if chat_id is not None and msg.get("message_id") is not None:
            _tg_post(base_url, "editMessageReplyMarkup",
                     {"chat_id": chat_id, "message_id": msg.get("message_id"),
                      "reply_markup": {"inline_keyboard": []}}, timeout=15)

        res: Optional[Dict[str, Any]] = None
        memory = getattr(kernel, "memory", None)
        if memory is None:
            risolta, motivo = False, "memoria non disponibile"
        else:
            try:
                risolta, motivo = memory.resolve_approval(aid, stato, telegram_user_id=uid,
                                                          risolto_da="telegram_user")
            except Exception as e:
                log.warning("callback: resolve_approval id=%s eccezione: %s", aid, e)
                risolta, motivo = False, "errore interno"
        # R-445-2: click gestiti UNO ALLA VOLTA (niente thread qui). recupera_esito_firma
        # in _riprova_orfana conta su questo: un reclamo senza esito non ha
        # un'esecuzione in corso. Un handler concorrente richiede di rivederlo.
        if risolta:
            log.warning("callback: id=%s %s da user_id %d", aid, stato, uid)
            res = kernel.applica_firma(aid)
        elif azione == "ok" and memory is not None:
            res, motivo = _riprova_orfana(memory, kernel, aid, motivo)

        testo = componi_esito_firma(azione, aid, risolta or res is not None, motivo, res)
        dest = chat_id if chat_id is not None else uid
        _tg_post(base_url, "sendMessage",
                 {"chat_id": dest, "text": testo,
                  "link_preview_options": {"is_disabled": True}}, timeout=15)
    except Exception as e:
        log.warning("gestisci_callback fallita: %s", e)
