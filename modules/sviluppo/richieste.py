"""Richieste di sviluppo come issue GitHub in un repo PRIVATO (ponte A, 2026-10-29).

Gas non tocca il codice: scrive solo la richiesta, già chiarita con l'operatore. La
chat di coordinamento (Claude Code, M1) legge le issue con l'etichetta `da-gas` e
assegna il lavoro; revisore, CI e firme restano quelli di sempre.

Regole:
- Repo e token SOLO da configurazione: `GAS_RICHIESTE_REPO` («proprietario/nome») e il
  token in `GAS_RICHIESTE_TOKEN`, oppure nel file indicato da `GAS_RICHIESTE_TOKEN_FILE`
  (default `~/.config/gas/richieste_token`). Il token deve essere DEDICATO (solo Issues
  sul repo delle richieste), mai quello dello sviluppo che scrive sul codice (R-557-1,
  roadmap R10: il runtime non ha le credenziali della macchina di sviluppo). Il token
  non finisce mai nel log né nel testo restituito; i redirect non si seguono (R-557-3).
- Il repo deve essere PRIVATO (il repo del codice è pubblico): prima di scrivere si
  controlla `private` via API e, se non lo è, NON si scrive (fail-closed).
- Tetto giornaliero `GAS_RICHIESTE_MAX_GIORNO` (default 20) in `.gas_richieste_uso.json`;
  il posto si PRENOTA prima della scrittura (R-557-2): conto illeggibile o non
  scrivibile → niente richiesta (fail-closed).
- Fail-safe §9: nessuna eccezione esce; errori → messaggio «Operazione negata: …».
"""
from __future__ import annotations

import json
import logging
import os
import re
import tempfile
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

log = logging.getLogger(__name__)

API = "https://api.github.com"
ETICHETTA = "da-gas"
USO_FILENAME = ".gas_richieste_uso.json"
TITOLO_MAX = 120
DESCRIZIONE_MAX = 4000
TIMEOUT_SEC = 15
_REPO_RE = re.compile(r"[A-Za-z0-9-]{1,39}/[A-Za-z0-9._-]{1,100}")
_TOKEN_FILE_DEFAULT = "~/.config/gas/richieste_token"

# (metodo, url, token, corpo) → (codice HTTP, JSON o None). Sostituibile nei test.
Http = Callable[[str, str, str, Optional[Dict[str, Any]]], Tuple[int, Optional[Any]]]


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """R-557-3: nessun redirect, così l'intestazione col token non va mai altrove."""
    def redirect_request(self, *a: Any, **k: Any) -> None:
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def _http(metodo: str, url: str, token: str,
          corpo: Optional[Dict[str, Any]] = None) -> Tuple[int, Optional[Any]]:
    """Chiamata all'API GitHub via urllib. Mai eccezioni: rete giù → (0, None)."""
    dati = json.dumps(corpo).encode("utf-8") if corpo is not None else None
    req = urllib.request.Request(url, data=dati, method=metodo, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "gas-richieste",
    })
    try:
        with _OPENER.open(req, timeout=TIMEOUT_SEC) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        e.close()  # V-3 bot #307
        return e.code, None
    except Exception as e:  # rete, JSON, timeout
        log.warning("richieste: chiamata GitHub fallita (%s)", type(e).__name__)
        return 0, None


def _token() -> Optional[str]:
    """Token da env o da file; None se manca. Mai nel log."""
    t = (os.environ.get("GAS_RICHIESTE_TOKEN") or "").strip()
    if t:
        return t
    percorso = os.environ.get("GAS_RICHIESTE_TOKEN_FILE") or _TOKEN_FILE_DEFAULT
    try:
        t = Path(percorso).expanduser().read_text(encoding="utf-8").strip()
    except Exception:
        return None
    return t or None


def _max_giorno() -> int:
    try:
        return max(1, int(os.environ.get("GAS_RICHIESTE_MAX_GIORNO", "20")))
    except ValueError:
        return 20


def _uso_oggi(p: Path) -> Optional[int]:
    """Richieste fatte oggi; 0 se il file manca o è di un altro giorno; None se rotto."""
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
        log.warning("richieste: conto non aggiornato (%s)", type(e).__name__)
        return False


def crea_richiesta(titolo: Any, descrizione: Any, root: Path,
                   http: Optional[Http] = None) -> str:
    """Crea la issue con l'etichetta `da-gas`. Ritorna il testo per il modello:
    «Successo: …» col numero della richiesta, oppure «Operazione negata: …»."""
    http = http or _http  # letto a ogni chiamata: i test lo sostituiscono
    try:
        titolo = " ".join(str(titolo or "").split())
        descrizione = str(descrizione or "").strip()
        if not titolo or not descrizione:
            return "Operazione negata: servono sia 'titolo' sia 'descrizione'."
        if len(titolo) > TITOLO_MAX:
            return f"Operazione negata: titolo oltre {TITOLO_MAX} caratteri, accorcialo."
        if len(descrizione) > DESCRIZIONE_MAX:
            return (f"Operazione negata: descrizione oltre {DESCRIZIONE_MAX} caratteri, "
                    "riassumila.")
        repo = (os.environ.get("GAS_RICHIESTE_REPO") or "").strip()
        if not _REPO_RE.fullmatch(repo):
            return ("Operazione negata: repo delle richieste non configurato "
                    "(GAS_RICHIESTE_REPO=proprietario/nome nel .env).")
        token = _token()
        if not token:
            return "Operazione negata: token GitHub per le richieste non trovato."
        uso = root / USO_FILENAME
        fatte = _uso_oggi(uso)
        if fatte is None:
            return (f"Operazione negata: conto delle richieste ({USO_FILENAME}) illeggibile: "
                    "controllalo o cancellalo.")
        if fatte >= _max_giorno():
            return (f"Operazione negata: tetto di {_max_giorno()} richieste di sviluppo "
                    "al giorno raggiunto (GAS_RICHIESTE_MAX_GIORNO). Riprova domani.")
        codice, info = http("GET", f"{API}/repos/{repo}", token, None)
        if codice != 200 or not isinstance(info, dict):
            return (f"Operazione negata: repo delle richieste non raggiungibile "
                    f"(HTTP {codice}).")
        if info.get("private") is not True:
            log.warning("richieste: %s non è privato, richiesta non scritta", repo)
            return ("Operazione negata: il repo delle richieste non è PRIVATO: "
                    "per non pubblicare dati la richiesta non è stata scritta.")
        if not _registra_uso(uso, fatte + 1):  # R-557-2: prenota il posto, fail-closed
            return ("Operazione negata: conto delle richieste non scrivibile, "
                    "richiesta non creata.")
        corpo = {"title": titolo,
                 "body": descrizione + "\n\n---\n_Richiesta scritta da Gas._",
                 "labels": [ETICHETTA]}
        codice, info = http("POST", f"{API}/repos/{repo}/issues", token, corpo)
        if codice != 201 or not isinstance(info, dict) or not isinstance(info.get("number"), int):
            return f"Operazione negata: richiesta non creata (HTTP {codice})."
        etichette = [e.get("name") for e in info.get("labels") or [] if isinstance(e, dict)]
        if ETICHETTA not in etichette:  # V-2 bot #307: senza etichetta la chat non la vede
            log.warning("richieste: #%s creata senza l'etichetta %s", info["number"], ETICHETTA)
            return (f"Successo parziale: richiesta #{info['number']} creata ma SENZA l'etichetta "
                    f"«{ETICHETTA}» (permessi del token?): avvisa l'operatore, la chat di "
                    "sviluppo potrebbe non vederla.")
        return (f"Successo: richiesta di sviluppo #{info['number']} registrata "
                f"(«{titolo}»). La chat di sviluppo la prende in carico.")
    except Exception as e:
        log.warning("richieste: errore inatteso (%s)", type(e).__name__)
        return "Operazione negata: richiesta non creata (errore interno, dettagli nel log)."
