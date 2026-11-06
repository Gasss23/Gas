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
import signal
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
DURATA_MAX_S_DEFAULT = 3600  # oltre: compito considerato bloccato (GAS_SOTTOFONDO_MAX_MIN)

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


def _durata_max_s() -> float:
    try:
        minuti = float(os.environ.get("GAS_SOTTOFONDO_MAX_MIN", "") or DURATA_MAX_S_DEFAULT / 60)
    except ValueError:
        minuti = DURATA_MAX_S_DEFAULT / 60
    return max(60.0, minuti * 60)


def attivo(root: Path) -> StatoAttivo:
    """Il compito in corso, se c'è ed è vivo. Non vivo: pid morto, pid mai scritto dopo 120 s,
    oppure oltre la durata massima (ve #345 V-1/V-2: un pid riusato o un figlio appeso non
    bloccano la coda per sempre)."""
    dati = _leggi(Path(root) / CARTELLA / ATTIVO)
    if not dati:
        return None
    eta = time.time() - float(dati.get("creato", 0) or 0)
    if eta > _durata_max_s():
        return None
    pid = dati.get("pid")
    if pid is None:  # appena accodato, il processo non ha ancora scritto il pid
        return dati if eta < 120 else None
    return dati if _vivo(pid) else None


def _ripulisci(root: Path, avvisa: Optional[Callable[[str, Path], Any]]) -> None:
    """Bot #345 V-3: un compito il cui processo è morto (ucciso, riavvio) o è oltre la durata
    massima diventa «ko» e l'operatore viene avvisato, invece di restare «in_corso» per sempre."""
    cartella = Path(root) / CARTELLA
    posto = cartella / ATTIVO
    dati = _leggi(posto)
    if dati is None:
        # R-697-1-M2: un posto illeggibile (crash fra creazione e scrittura) non blocca la coda
        # per sempre: dopo 120 s si toglie.
        try:
            if posto.exists() and time.time() - posto.stat().st_mtime > 120:
                posto.unlink()
        except OSError:
            pass
        return
    if attivo(root) is not None:
        return
    ident = str(dati.get("id") or "")
    pid = dati.get("pid")
    oltre = time.time() - float(dati.get("creato", 0) or 0) > _durata_max_s()
    if oltre and _vivo(pid) and _e_nostro(pid, ident):
        # R-697-2-M2: un compito oltre la durata massima viene fermato (sessione propria:
        # il gruppo di processi ha lo stesso id del figlio), non lasciato a metà.
        # R-698-1-M2: SOLO se il pid è davvero il nostro figlio; un pid riusato (dopo un
        # riavvio può essere un'app dell'operatore) non si tocca mai.
        try:
            os.killpg(int(pid), signal.SIGTERM)
        except Exception as e:
            logging.warning("sottofondo %s: arresto non riuscito: %s", ident, e)
    job = _leggi(cartella / f"{Path(ident).name}.json") if ident else None
    motivo = ("oltre la durata massima, fermato" if oltre
              else "il processo si è interrotto")
    annulla(root, ident, motivo)
    # R-697-3-M2: si toglie il posto solo se è ancora quello letto (o senza id)
    rilettura = _leggi(posto)
    if rilettura is not None and str(rilettura.get("id") or "") == ident:
        try:
            posto.unlink()
        except FileNotFoundError:
            pass
    if job and job.get("stato") in ("in_coda", "in_corso"):
        _avvisa(root, f"Il compito in sottofondo «{_breve(job.get('compito', ''), 80)}» non è "
                      f"finito: {motivo}.", ident, avvisa)


def _e_nostro(pid: Any, ident: str) -> bool:
    """R-698-1-M2: il pid è il NOSTRO figlio `gas.py sottofondo <ident>`, leader del proprio
    gruppo? Nel dubbio (comando illeggibile, errore) False: meglio non fermare che uccidere un
    processo estraneo. `ps -o command=` funziona su macOS e Linux."""
    try:
        if not isinstance(pid, int) or pid <= 1 or os.getpgid(pid) != pid:
            return False
        r = subprocess.run(["ps", "-o", "command=", "-p", str(pid)], capture_output=True,
                           text=True, timeout=5)
        comando = (r.stdout or "").strip()
        return r.returncode == 0 and comando.endswith(f"sottofondo {ident}") and "gas.py" in comando
    except Exception:
        return False


def notifica_possibile(root: Path) -> Optional[str]:
    """Bot #345 V-1: motivo per cui l'avviso finale NON potrebbe partire (Telegram non
    configurato, notifiche spente, tetto del giorno già raggiunto), altrimenti None."""
    try:
        from modules.telegram import avviso
        if avviso._max_giorno() <= 0:
            return "notifiche Telegram spente (GAS_NOTIFICHE_GIORNO=0)"
        manca = avviso._manca_configurazione()
        if manca:
            return f"Telegram non configurato ({manca})"
        fatte = avviso._uso_oggi(Path(root) / avviso.USO_FILENAME)
        if fatte is None:
            return "conto delle notifiche illeggibile"
        if fatte >= avviso._max_giorno():
            return "tetto delle notifiche di oggi già raggiunto"
    except Exception as e:  # §9: nel dubbio niente promessa
        return f"controllo delle notifiche non riuscito ({type(e).__name__})"
    return None


def accoda(root: Path, compito: Any,
           avvisa: Optional[Callable[[str, Path], Any]] = None) -> Tuple[Optional[str], str]:
    """Mette in coda un compito. Ritorna (id, "") oppure (None, motivo del rifiuto)."""
    if not isinstance(compito, str) or not compito.strip():
        return None, "Operazione negata: compito vuoto."
    compito = compito.strip()
    if len(compito) > COMPITO_MAX:
        return None, f"Operazione negata: compito troppo lungo (max {COMPITO_MAX} caratteri)."
    cartella = _cartella(root)
    _ripulisci(root, avvisa)
    occupato = ("Operazione negata: c'è già un compito in sottofondo. Di' all'operatore "
                "che ne stai già facendo uno e che lo avviserai quando hai finito.")
    if attivo(root) is not None:
        return None, occupato
    ident = time.strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3)
    adesso = time.time()
    # Bot #345 V-4: il posto si prende in modo atomico ed esclusivo; R-697-1-M2: col contenuto
    # già scritto (file temporaneo + os.link), così un crash non lascia un posto vuoto.
    tmp = cartella / f".posto.{os.getpid()}.{secrets.token_hex(3)}"
    _scrivi_privato(tmp, {"id": ident, "pid": None, "creato": adesso})
    try:
        os.link(tmp, cartella / ATTIVO)
    except FileExistsError:
        return None, occupato
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass
    _scrivi_privato(cartella / f"{ident}.json",
                    {"id": ident, "compito": compito, "stato": "in_coda", "creato": adesso})
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


def _avvisa(root: Path, testo: str, ident: str,
            avvisa: Optional[Callable[[str, Path], Any]]) -> None:
    """Avviso all'operatore su Telegram; un rifiuto o un errore finiscono nel log (§9)."""
    try:
        if avvisa is None:
            from modules.telegram.avviso import avvisa_operatore_esito
            avvisa = lambda t, r: avvisa_operatore_esito(t, r)  # noqa: E731
        esito = avvisa(testo, Path(root))
        esito = esito[0] if isinstance(esito, tuple) else esito
        if isinstance(esito, str) and esito.startswith("Operazione negata"):
            logging.warning("sottofondo %s: avviso non inviato: %s", ident, esito)
    except Exception as e:  # §9
        logging.warning("sottofondo %s: avviso non inviato: %s", ident, e)


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
        # R-696-2-M2: l'operatore, a cui è stato promesso un avviso, lo riceve anche qui
        _avvisa(root, "Un compito in sottofondo si è interrotto per un errore interno.",
                ident, avvisa)
        return 1


def _esegui(root: Path, ident: str, kernel_factory: Callable[[], Any],
            avvisa: Optional[Callable[[str, Path], Any]]) -> int:
    cartella = _cartella(root)
    percorso = cartella / f"{Path(ident).name}.json"
    job = _leggi(percorso)
    if not job or job.get("stato") != "in_coda" or not isinstance(job.get("compito"), str):
        logging.warning("sottofondo %s: compito assente o già eseguito", ident)
        return 1
    posto = _leggi(cartella / ATTIVO)
    if not posto or posto.get("id") != ident:
        # R-697-3-M2: il posto non è (più) di questo compito: non lo si ruba a un altro
        logging.warning("sottofondo %s: posto non suo, compito non eseguito", ident)
        annulla(root, ident, "posto in coda perso")
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
    attuale = _leggi(percorso)
    if attuale and attuale.get("stato") == "ko":
        # R-697-2-M2: il compito è già stato chiuso (oltre la durata massima) e l'operatore
        # avvisato: niente secondo esito né secondo avviso contraddittorio.
        logging.warning("sottofondo %s: già chiuso, esito tardivo ignorato", ident)
        return 1
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
    _avvisa(root, testo, ident, avvisa)
    return 0 if ok else 1
