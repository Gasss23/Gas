"""Fetta 3 (chat M2, 6 nov 2026, sì dell'operatore via M1): compiti lunghi in sottofondo.

A voce il modello chiama lo strumento `in_sottofondo(compito)`: il kernel mette il compito in
coda (`.gas_sottofondo/<id>.json`, permessi 0600, mai negli argomenti visibili con `ps`) e lo
avvia in un PROCESSO SEPARATO (`gas.py sottofondo <id>`) col suo GasKernel: niente thread nel
server voce (un solo kernel, stato condiviso senza lock in memoria). La storia resta una sola:
l'unione fra processi esiste già (`_save_history` con lock su file). Il compito usa SOLO il
cervello forte; alla fine l'operatore riceve un avviso su Telegram (`avvisa_operatore`, col
tetto al giorno). Un compito alla volta. Fail-safe §9: ogni errore diventa uno stato «ko» e
un avviso, mai un crash.
"""
from __future__ import annotations

import json
import logging
import os
import secrets
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

CARTELLA = ".gas_sottofondo"
ATTIVO = "attivo.json"
COMPITO_MAX = 2000          # caratteri del compito
RISPOSTA_AVVISO_MAX = 700   # caratteri della risposta dentro l'avviso Telegram
PREFISSO_TURNO = "Compito in sottofondo (avviato a voce): "

StatoAttivo = Optional[Dict[str, Any]]


def _cartella(root: Path) -> Path:
    c = Path(root) / CARTELLA
    c.mkdir(mode=0o700, exist_ok=True)
    return c


def _scrivi_privato(percorso: Path, dati: Dict[str, Any]) -> None:
    """Scrittura atomica, file 0600 (il compito può contenere dati dell'operatore)."""
    tmp = percorso.with_suffix(f".tmp.{os.getpid()}")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False)
    os.replace(tmp, percorso)


def _leggi(percorso: Path) -> Optional[Dict[str, Any]]:
    try:
        dati = json.loads(percorso.read_text(encoding="utf-8"))
        return dati if isinstance(dati, dict) else None
    except Exception:
        return None


def _vivo(pid: Any) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except Exception:
        return False
    return True


def attivo(root: Path) -> StatoAttivo:
    """Il compito in corso, se c'è ed è vivo (un processo morto non blocca la coda)."""
    dati = _leggi(Path(root) / CARTELLA / ATTIVO)
    if not dati:
        return None
    pid = dati.get("pid")
    if pid is None:  # appena accodato, il processo non ha ancora scritto il pid
        return dati if time.time() - float(dati.get("creato", 0) or 0) < 120 else None
    return dati if _vivo(pid) else None


def accoda(root: Path, compito: Any) -> Tuple[Optional[str], str]:
    """Mette in coda un compito. Ritorna (id, "") oppure (None, motivo del rifiuto)."""
    if not isinstance(compito, str) or not compito.strip():
        return None, "Operazione negata: compito vuoto."
    compito = compito.strip()
    if len(compito) > COMPITO_MAX:
        return None, f"Operazione negata: compito troppo lungo (max {COMPITO_MAX} caratteri)."
    if attivo(root) is not None:
        return None, ("Operazione negata: c'è già un compito in sottofondo. Di' all'operatore "
                      "che ne stai già facendo uno e che lo avviserai quando hai finito.")
    cartella = _cartella(root)
    ident = time.strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3)
    adesso = time.time()
    _scrivi_privato(cartella / f"{ident}.json",
                    {"id": ident, "compito": compito, "stato": "in_coda", "creato": adesso})
    _scrivi_privato(cartella / ATTIVO, {"id": ident, "pid": None, "creato": adesso})
    return ident, ""


def avvia(root: Path, ident: str, popen: Callable[..., Any] = subprocess.Popen) -> None:
    """Avvia il processo separato `gas.py sottofondo <id>` (sessione propria: sopravvive alla
    richiesta HTTP della voce; output scartato, l'esito è nel file del compito)."""
    gas_py = Path(__file__).resolve().parents[2] / "gas.py"
    proc = popen([sys.executable, str(gas_py), "sottofondo", ident], cwd=str(root),
                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                 start_new_session=True)
    # R-695-2-M2: un figlio morto non deve restare zombie (os.kill(pid, 0) lo vedrebbe vivo e
    # la coda resterebbe bloccata): un thread lo raccoglie quando finisce.
    attesa = getattr(proc, "wait", None)
    if callable(attesa):
        threading.Thread(target=attesa, daemon=True).start()


def annulla(root: Path, ident: str, motivo: str) -> None:
    """R-695-4-M2: avvio fallito → compito «ko» e coda libera (fail-safe, mai eccezioni)."""
    try:
        cartella = Path(root) / CARTELLA
        percorso = cartella / f"{Path(ident).name}.json"
        job = _leggi(percorso)
        if job:
            job.update(stato="ko", fine=time.time(), errore=motivo)
            _scrivi_privato(percorso, job)
        dati = _leggi(cartella / ATTIVO)
        if dati and dati.get("id") == ident:
            (cartella / ATTIVO).unlink()
    except Exception as e:
        logging.warning("sottofondo %s: annullamento non riuscito: %s", ident, e)


def _breve(testo: str, n: int) -> str:
    testo = " ".join(str(testo or "").split())
    return testo if len(testo) <= n else testo[: n - 1].rstrip() + "…"


def esegui(root: Path, ident: str, kernel_factory: Callable[[], Any],
           avvisa: Optional[Callable[[str, Path], Any]] = None) -> int:
    """Corpo del processo separato. 0 = compito finito con una risposta, 1 = ko. Fail-safe §9
    (R-695-4-M2): nessuna eccezione esce, nemmeno da file illeggibili o non scrivibili."""
    try:
        return _esegui(Path(root), ident, kernel_factory, avvisa)
    except Exception as e:
        logging.warning("sottofondo %s: interrotto: %s", ident, e)
        annulla(root, ident, f"interrotto ({type(e).__name__})")
        return 1


def _esegui(root: Path, ident: str, kernel_factory: Callable[[], Any],
            avvisa: Optional[Callable[[str, Path], Any]]) -> int:
    cartella = _cartella(root)
    percorso = cartella / f"{Path(ident).name}.json"
    job = _leggi(percorso)
    if not job or job.get("stato") != "in_coda" or not isinstance(job.get("compito"), str):
        logging.warning("sottofondo %s: compito assente o già eseguito", ident)
        return 1
    _scrivi_privato(cartella / ATTIVO, {"id": ident, "pid": os.getpid(), "creato": job.get("creato")})
    job.update(stato="in_corso", pid=os.getpid(), inizio=time.time())
    _scrivi_privato(percorso, job)
    risposta, errore = "", ""
    turno = None
    try:
        kernel = kernel_factory()
        turno = kernel.run_turn(PREFISSO_TURNO + job["compito"], cervello="forte")
        for ev in turno:
            if ev.get("type") == "final":
                risposta = str(ev.get("content") or "")
                break
            if ev.get("type") == "error":
                errore = str(ev.get("content") or "errore")
                break
    except Exception as e:  # §9: mai crash, il compito finisce «ko»
        errore = f"eccezione {type(e).__name__}"
        logging.warning("sottofondo %s: %s", ident, e)
    finally:
        close = getattr(turno, "close", None)  # R-695-3-M2: il kernel chiude subito il turno
        if callable(close):
            try:
                close()
            except Exception:
                pass
    ok = bool(risposta.strip()) and not errore
    job.update(stato="ok" if ok else "ko", fine=time.time(),
               risposta=risposta if ok else "", errore="" if ok else (errore or "nessuna risposta"))
    _scrivi_privato(percorso, job)
    try:
        (cartella / ATTIVO).unlink()
    except FileNotFoundError:
        pass
    titolo = _breve(job["compito"], 80)
    testo = (f"Ho finito il compito in sottofondo «{titolo}». {_breve(risposta, RISPOSTA_AVVISO_MAX)}"
             if ok else
             f"Il compito in sottofondo «{titolo}» non è riuscito: {_breve(job['errore'], 200)}")
    try:
        if avvisa is None:
            from modules.telegram.avviso import avvisa_operatore_esito
            avvisa = lambda t, r: avvisa_operatore_esito(t, r)  # noqa: E731
        esito = avvisa(testo, root)
        esito = esito[0] if isinstance(esito, tuple) else esito
        if isinstance(esito, str) and esito.startswith("Operazione negata"):
            # R-695-3-M2: l'operatore non saprebbe che il compito è finito
            logging.warning("sottofondo %s: avviso non inviato: %s", ident, esito)
    except Exception as e:  # §9
        logging.warning("sottofondo %s: avviso non inviato: %s", ident, e)
    return 0 if ok else 1
