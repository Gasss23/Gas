"""Strumento `avvisa_operatore`: Gas manda un messaggio all'operatore su Telegram (R6).

Regole:
- Destinatari: SOLO gli ID di TELEGRAM_ALLOWED_IDS (la chat dell'operatore), tramite
  `invia_notifica` di modules/telegram/bot.py (testo semplice: niente bottoni, niente
  formattazione, niente anteprime dei link). Il modello non sceglie il destinatario:
  lo strumento non ha un campo per farlo.
- Prefisso fisso `PREFISSO`: l'avviso non si confonde con una richiesta di firma.
- Testo al massimo `TESTO_MAX` caratteri. I caratteri invisibili o di controllo (bidi,
  larghezza zero, separatori di riga Unicode, NBSP, riempitivi…) si mostrano come
  <U+XXXX> con `rendi_visibili` del bot, lo stesso standard dei read-back (R-611-3).
- Tetto giornaliero `GAS_NOTIFICHE_GIORNO` (default 5; 0 = strumento spento) in
  `.gas_notifiche_uso.json`
  (il cancello vieta al modello di scriverlo). Il posto si PRENOTA prima dell'invio,
  come per le richieste di sviluppo (R-557-2): conto illeggibile o non scrivibile →
  niente invio (fail-closed). Un invio fallito consuma comunque il posto.
- Il tetto per turno (una notifica) lo tiene il kernel: conta ogni chiamata che ha
  prenotato un posto, anche se l'invio poi fallisce (R-611-4).
- Fail-safe §9: nessuna eccezione esce; errori → «Operazione negata: …».
"""
from __future__ import annotations

import json
import logging
import os
import tempfile
from datetime import date
from pathlib import Path
from typing import Any, Callable, Optional, Tuple

log = logging.getLogger(__name__)

USO_FILENAME = ".gas_notifiche_uso.json"
PREFISSO = "📣 Gas (notifica automatica):\n"
TESTO_MAX = 1000
MAX_GIORNO_DEFAULT = 5

# testo → (consegnato, motivo). Sostituibile nei test.
Invia = Callable[[str], Tuple[bool, str]]


def _max_giorno() -> int:
    """Tetto al giorno; 0 (o negativo) = notifiche spente (V-3 ve #319)."""
    try:
        return max(0, int(os.environ.get("GAS_NOTIFICHE_GIORNO", str(MAX_GIORNO_DEFAULT))))
    except ValueError:
        return MAX_GIORNO_DEFAULT


def _uso_oggi(p: Path) -> Optional[int]:
    """Notifiche di oggi; 0 se il file manca o è di un altro giorno; None se rotto."""
    if not p.exists():
        return 0
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(d, dict):
            return None
        n = d.get("n")
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            return None
        return n if d.get("giorno") == date.today().isoformat() else 0
    except Exception:
        return None


def _registra_uso(p: Path, n: int) -> bool:
    try:
        fd, tmp = tempfile.mkstemp(prefix=p.name + ".", suffix=".tmp", dir=str(p.parent))
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"giorno": date.today().isoformat(), "n": n}, f)
        os.replace(tmp, p)
        return True
    except Exception as e:
        log.warning("avviso: conto non aggiornato (%s)", type(e).__name__)
        return False


def pulisci(testo: Any) -> str:
    """Testo da inviare: invisibili e controlli resi visibili come <U+XXXX> (a-capo e
    tabulazione restano). Vuoto se il testo non ha nessun carattere visibile."""
    from modules.telegram.bot import rendi_visibili
    s = str(testo if testo is not None else "").replace("\r\n", "\n").strip()
    if not "".join(c for c in s if rendi_visibili(c) == c).strip():
        return ""
    return rendi_visibili(s, a_capo=True)


def _manca_configurazione() -> Optional[str]:
    """Motivo se Telegram non è configurato (prima di prenotare il posto)."""
    from modules.telegram.bot import parse_allowed_ids
    if not os.environ.get("TELEGRAM_BOT_TOKEN", "").strip():
        return "TELEGRAM_BOT_TOKEN mancante"
    if not parse_allowed_ids(os.environ.get("TELEGRAM_ALLOWED_IDS", ""))[0]:
        return "TELEGRAM_ALLOWED_IDS mancante o senza ID validi"
    return None


def _invia_default(testo: str) -> Tuple[bool, str]:
    from modules.telegram.bot import invia_notifica
    return invia_notifica(testo)


def avvisa_operatore(testo: Any, root: Path, invia: Optional[Invia] = None) -> str:
    """Manda `PREFISSO + testo` all'operatore. Ritorna il testo per il modello:
    «Successo: …» oppure «Operazione negata: …»."""
    return avvisa_operatore_esito(testo, root, invia)[0]


def rifiuto_senza_costi(testo: Any) -> Optional[str]:
    """I controlli che non costano niente (tipo e lunghezza del testo, strumento spento):
    il kernel li ripete PRIMA di mandare la notifica alla firma (R-613-1), così un testo
    sbagliato o lo strumento spento non producono una richiesta di firma. None = ok."""
    if testo is not None and not isinstance(testo, str):  # V-2 ve #319: niente repr
        return "Operazione negata: 'testo' deve essere una stringa."
    corpo = pulisci(testo)
    if not corpo:
        return "Operazione negata: serve un 'testo' non vuoto."
    if len(corpo) > TESTO_MAX:
        return f"Operazione negata: testo oltre {TESTO_MAX} caratteri, riassumilo."
    if _max_giorno() == 0:
        return "Operazione negata: notifiche spente (GAS_NOTIFICHE_GIORNO a 0 o meno)."
    return None


def avvisa_operatore_esito(testo: Any, root: Path,
                           invia: Optional[Invia] = None) -> Tuple[str, bool]:
    """Come avvisa_operatore, più True se è stato prenotato un posto del giorno
    (l'invio è partito, riuscito o no): serve al tetto per turno del kernel."""
    invia = invia or _invia_default
    prenotato = False
    try:
        rifiuto = rifiuto_senza_costi(testo)
        if rifiuto:
            return rifiuto, False
        corpo = pulisci(testo)
        manca = _manca_configurazione()
        if manca:
            return f"Operazione negata: Telegram non configurato ({manca}).", False
        uso = Path(root) / USO_FILENAME
        fatte = _uso_oggi(uso)
        if fatte is None:
            return (f"Operazione negata: conto delle notifiche ({USO_FILENAME}) "
                    "illeggibile: controllalo o cancellalo."), False
        tetto = _max_giorno()
        if fatte >= tetto:
            return (f"Operazione negata: tetto di {tetto} notifiche al giorno "
                    "raggiunto (GAS_NOTIFICHE_GIORNO). Riprova domani."), False
        if not _registra_uso(uso, fatte + 1):  # prenota il posto, fail-closed
            return ("Operazione negata: conto delle notifiche non scrivibile, "
                    "notifica non inviata."), False
        prenotato = True
        ok, motivo = invia(PREFISSO + corpo)
        if not ok:
            log.warning("avviso: notifica non consegnata (%s)", motivo)
            return f"Operazione negata: notifica non consegnata ({motivo}).", True
        return (f"Successo: notifica inviata all'operatore "
                f"({fatte + 1}/{tetto} oggi)."), True
    except Exception as e:
        log.warning("avviso: errore inatteso (%s)", type(e).__name__)
        return ("Operazione negata: notifica non inviata (errore interno, dettagli nel "
                "log)."), prenotato
