"""Azioni fisse di manutenzione per Gas (terminale, opzione A — chat M2, 9 novembre 2026).

Decisione dell'operatore (9/11, via M1): Gas non riceve una shell ma poche azioni con nome,
scritte qui, senza argomenti liberi. Quelle che cambiano qualcosa passano SEMPRE dalla firma
dell'operatore su Telegram (cancello: IRREVERSIBILE), mai a voce né di notte (lo strumento
non è offerto in quei turni: vedi gas.py). Proposta: reports/proposta_terminale_A.md.

Regole del modulo:
- nessun testo del modello diventa un comando: argv fissi, subprocess senza shell, cartella
  di Gas, tempo massimo, output tagliato;
- un'azione che cambia qualcosa senza firma è negata anche qui (difesa in profondità);
- FAIL-SAFE §9: mai eccezioni verso il kernel, sempre un testo d'esito.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

AZIONI_LETTURA = ("stato_gas", "log_voce")
AZIONI_FIRMA = ("aggiorna_gas", "riavvia_voce")
AZIONI = AZIONI_LETTURA + AZIONI_FIRMA

RIGHE_OUTPUT = 40          # righe finali restituite al modello
RIGHE_LOG_VOCE = 40        # righe «tempi voce» restituite da log_voce
LOG_LETTURA_BYTE = 512 * 1024  # coda del log letta per log_voce
# Servizi launchd della voce (scripts/voce/*.plist): prima il server, poi l'ascolto H24
SERVIZI_VOCE = ("com.gas.voce.server", "com.gas.ascolto")
TIMEOUT_DOCTOR = 120
TIMEOUT_GIT = 120
TIMEOUT_PIP = 900
TIMEOUT_LAUNCHCTL = 30

# Una riga dei tempi della voce (modules/voice/server.py, _chiudi_tempi): solo codice HTTP e
# numeri «nome=1.23s». Qualunque altra riga del log, anche se contiene le stesse parole, no.
_RIGA_TEMPI = re.compile(r"tempi voce \(\d{3}\): (?:[a-z_]+=\d+(?:\.\d+)?s ?)+$")

# «Mai di notte» (decisione dell'operatore): nelle ore della notte le azioni che cambiano Gas
# sono negate, sia la richiesta di firma sia l'esecuzione. Ora locale del computer di Gas;
# GAS_MANUTENZIONE_NOTTE="inizio-fine" in ore intere (default 23-7, cioè dalle 23 alle 7).
NOTTE_DEFAULT = (23, 7)


def ore_notte() -> "tuple[int, int]":
    grezzo = os.environ.get("GAS_MANUTENZIONE_NOTTE", "").strip()
    try:
        inizio, fine = (int(x) for x in grezzo.split("-"))
        if 0 <= inizio <= 23 and 0 <= fine <= 23 and inizio != fine:
            return inizio, fine
    except ValueError:
        pass
    return NOTTE_DEFAULT  # vuoto o scritto male: la finestra prudente di default


def e_notte(adesso: Optional[datetime] = None) -> bool:
    ora = (adesso or datetime.now()).hour
    inizio, fine = ore_notte()
    return (inizio <= ora or ora < fine) if inizio > fine else (inizio <= ora < fine)


NOTTE_NEGATA = ("Operazione negata: di notte Gas non si aggiorna e non si riavvia "
                "(decisione dell'operatore). Riprova di giorno.")

# riferimento proprio del modulo: i test sostituiscono solo questo, non subprocess.run di tutti
_run = subprocess.run


def _coda(testo: str, n: int = RIGHE_OUTPUT) -> str:
    righe = (testo or "").strip().splitlines()
    return "\n".join(righe[-n:])


def _esegui(argv: List[str], cwd: Path, timeout: int) -> "tuple[Optional[int], str]":
    """argv fisso, senza shell. Ritorna (codice d'uscita o None se non partito/scaduto, testo).
    git non chiede mai credenziali al terminale (review #736-M2): fallisce subito."""
    try:
        env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
        r = _run(argv, cwd=str(cwd), capture_output=True, text=True, env=env,
                 timeout=timeout, shell=False, stdin=subprocess.DEVNULL)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return None, f"tempo scaduto dopo {timeout} s"
    except (OSError, ValueError) as e:
        return None, f"non partito: {type(e).__name__}"


def _stato_gas(root: Path) -> str:
    codice, out = _esegui([sys.executable, str(root / "gas.py"), "doctor"], root, TIMEOUT_DOCTOR)
    if codice is None:
        return f"[KO] stato_gas: {out}"
    esito = "OK" if codice == 0 else f"FAIL (codice {codice})"
    return f"stato_gas: doctor {esito}.\n{_coda(out)}"


def _log_voce(root: Path) -> str:
    log = root / "gas_debug.log"
    try:
        with open(log, "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - LOG_LETTURA_BYTE))
            testo = f.read().decode("utf-8", errors="replace")
    except FileNotFoundError:
        return "log_voce: nessun gas_debug.log (la voce non ha ancora scritto tempi)."
    except OSError as e:
        return f"[KO] log_voce: log non leggibile ({type(e).__name__})."
    righe = [r for r in testo.splitlines() if _RIGA_TEMPI.search(r.rstrip())]
    if not righe:
        return "log_voce: nessuna riga «tempi voce» recente."
    return "log_voce: ultime righe dei tempi della voce.\n" + "\n".join(righe[-RIGHE_LOG_VOCE:])


def _aggiorna_gas(root: Path) -> str:
    codice, ramo = _esegui(["git", "rev-parse", "--abbrev-ref", "HEAD"], root, TIMEOUT_GIT)
    if codice != 0 or ramo.strip() != "main":
        return ("[KO] aggiorna_gas: Gas non è sul branch main "
                f"({ramo.strip()[:60] or 'sconosciuto'}): aggiornamento non fatto.")
    codice, sporco = _esegui(["git", "status", "--porcelain", "--untracked-files=no"],
                             root, TIMEOUT_GIT)
    if codice != 0:
        return "[KO] aggiorna_gas: stato di git non leggibile: aggiornamento non fatto."
    if sporco.strip():
        return ("[KO] aggiorna_gas: ci sono file modificati a mano nella cartella di Gas: "
                "aggiornamento non fatto (nessuna modifica persa).")
    codice, out = _esegui(["git", "pull", "--ff-only", "origin", "main"], root, TIMEOUT_GIT)
    if codice != 0:
        return f"[KO] aggiorna_gas: git pull non riuscito.\n{_coda(out)}"
    righe = [f"aggiorna_gas: codice aggiornato da main.\n{_coda(out, 10)}"]
    if (root / "requirements.txt").is_file():
        codice, out_pip = _esegui([sys.executable, "-m", "pip", "install", "-q", "-r",
                                   "requirements.txt"], root, TIMEOUT_PIP)
        if codice != 0:
            righe.append(f"[KO] dipendenze non installate (pip).\n{_coda(out_pip, 15)}")
            return "\n".join(righe)
        righe.append("Dipendenze a posto.")
    righe.append("Il codice nuovo vale dal prossimo avvio: per la voce serve riavvia_voce, "
                 "il bot Telegram lo usa dopo il suo riavvio.")
    return "\n".join(righe)


def _riavvia_voce(root: Path) -> str:
    if sys.platform != "darwin":
        return "[KO] riavvia_voce: funziona solo sul Mac (servizio launchd)."
    righe = []
    for servizio in SERVIZI_VOCE:
        bersaglio = f"gui/{os.getuid()}/{servizio}"
        codice, out = _esegui(["launchctl", "kickstart", "-k", bersaglio], root,
                              TIMEOUT_LAUNCHCTL)
        if codice != 0 and servizio == "com.gas.ascolto" and "could not find service" in out.lower():
            # Mani (9/11): con l'ascolto in pausa (pausa.sh o standby fanno bootout) kickstart
            # non trova il servizio: la pausa si rispetta, niente bootstrap da qui.
            righe.append(f"{servizio}: in pausa, non riacceso (per riprendere: "
                         "bash scripts/voce/riprendi.sh).")
        elif codice != 0:
            righe.append(f"[KO] {servizio}: launchctl non riuscito.\n{_coda(out, 5)}")
        else:
            righe.append(f"{servizio}: riavviato.")
    ko = any(r.startswith("[KO]") for r in righe)
    return ("[KO] riavvia_voce: non tutto riavviato.\n" if ko else
            "riavvia_voce: fatto.\n") + "\n".join(righe)


def esegui(azione: object, root: Path, firmata: bool = False) -> str:
    """Esegue un'azione della lista chiusa. Le azioni che cambiano qualcosa SOLO firmate."""
    try:
        if not isinstance(azione, str) or azione not in AZIONI:
            return ("Operazione negata: azione di manutenzione sconosciuta. Possibili: "
                    + ", ".join(AZIONI) + ".")
        if azione in AZIONI_FIRMA and not firmata:
            return ("Operazione negata: questa azione cambia Gas e serve la firma "
                    "dell'operatore su Telegram.")
        if azione in AZIONI_FIRMA and e_notte():
            return NOTTE_NEGATA
        root = Path(root)
        if azione == "stato_gas":
            return _stato_gas(root)
        if azione == "log_voce":
            return _log_voce(root)
        if azione == "aggiorna_gas":
            return _aggiorna_gas(root)
        return _riavvia_voce(root)
    except Exception as e:  # §9: mai eccezioni verso il kernel
        return f"[KO] manutenzione: errore interno ({type(e).__name__})."
