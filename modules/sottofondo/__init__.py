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
import math
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
GIORNI_CONSERVAZIONE_DEFAULT = 7  # compiti finiti più vecchi: cancellati (GAS_SOTTOFONDO_GIORNI)

StatoAttivo = Optional[Dict[str, Any]]


def _cartella(root: Path) -> Path:
    c = Path(root) / CARTELLA
    c.mkdir(mode=0o700, exist_ok=True)
    return c


def _scrivi_privato(percorso: Path, dati: Dict[str, Any]) -> None:
    """Scrittura atomica, file 0600 (il compito può contenere dati dell'operatore)."""
    # Ve #350 V-3: nome temporaneo unico anche fra thread dello stesso processo (server voce)
    tmp = percorso.with_suffix(f".tmp.{os.getpid()}.{secrets.token_hex(4)}")
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


def _numero_env(nome: str, default: float) -> float:
    """Bot #345 (head 46596b4) V-3: «inf», «nan» o testo non numerico → default."""
    try:
        valore = float(os.environ.get(nome, "") or default)
    except ValueError:
        return default
    return valore if math.isfinite(valore) else default


def _durata_max_s() -> float:
    secondi = _numero_env("GAS_SOTTOFONDO_MAX_MIN", DURATA_MAX_S_DEFAULT / 60) * 60
    # Ve #346 V-2: un valore enorme (1e308) diventa inf dopo la moltiplicazione → default
    return max(60.0, secondi) if math.isfinite(secondi) else float(DURATA_MAX_S_DEFAULT)


def _creato(dati: Dict[str, Any]) -> float:
    """Bot #345 V-4 / ve V-2: «creato» non numerico, non finito o nel futuro vale 0 (posto
    scaduto, quindi ripulito), invece di un ValueError che bloccava la coda per sempre."""
    try:
        valore = float(dati.get("creato", 0) or 0)
    except (TypeError, ValueError):
        return 0.0
    # R-701-2-M2: anche un «creato» nel futuro (file alterato, orologio portato indietro)
    # vale scaduto, invece di tenere la coda occupata fino a quella data. Chi decide se il
    # processo va fermato guarda anche _nel_futuro (ve #346 V-1).
    return valore if math.isfinite(valore) and not _nel_futuro(dati) else 0.0


def _nel_futuro(dati: Dict[str, Any]) -> bool:
    """«creato» numerico finito ma più avanti di adesso + 120 s (orologio portato indietro)."""
    try:
        valore = float(dati.get("creato", 0) or 0)
    except (TypeError, ValueError):
        return False
    return math.isfinite(valore) and valore > time.time() + 120


def attivo(root: Path) -> StatoAttivo:
    """Il compito in corso, se c'è ed è vivo. Non vivo: pid morto, pid mai scritto dopo 120 s,
    oppure oltre la durata massima (ve #345 V-1/V-2: un pid riusato o un figlio appeso non
    bloccano la coda per sempre)."""
    dati = _leggi(Path(root) / CARTELLA / ATTIVO)
    if not dati:
        return None
    pid = dati.get("pid")
    if _nel_futuro(dati):
        # Ve #346 V-1 / R-702-1-M2: con l'orologio portato indietro la data non dice più
        # niente. Il posto resta del processo se è vivo e non sicuramente estraneo; senza pid
        # (nessun processo ancora) o con pid morto è libero.
        if pid is None or not _vivo(pid):
            return None
        return None if _identita(pid, str(dati.get("id") or "")) is False else dati
    eta = time.time() - _creato(dati)
    if eta > _durata_max_s():
        return None
    if pid is None:  # appena accodato, il processo non ha ancora scritto il pid
        return dati if eta < 120 else None
    if not _vivo(pid):
        return None
    # Ve #345 (head 46596b4) V-1: un pid vivo ma sicuramente di un ALTRO processo (pid riusato
    # dopo un crash o un riavvio) non tiene occupata la coda. Se non si sa (niente `ps`), il
    # posto resta occupato: meglio aspettare che far girare due compiti insieme.
    return None if _identita(pid, str(dati.get("id") or "")) is False else dati


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
    # Ve #346 V-1: con «creato» nel futuro non si è mai «oltre la durata»: niente killpg
    oltre = not _nel_futuro(dati) and time.time() - _creato(dati) > _durata_max_s()
    motivo = "il processo si è interrotto"
    if oltre:
        motivo = "oltre la durata massima"
        nostro = _identita(pid, ident) if _vivo(pid) else False
        if nostro:
            # R-697-2-M2: un compito oltre la durata massima viene fermato (sessione propria:
            # il gruppo di processi ha lo stesso id del figlio), non lasciato a metà.
            # R-698-1-M2: SOLO se il pid è davvero il nostro figlio; un pid riusato (dopo un
            # riavvio può essere un'app dell'operatore) non si tocca mai.
            try:
                os.killpg(int(pid), signal.SIGTERM)
                motivo = "oltre la durata massima, fermato"
            except Exception as e:
                logging.warning("sottofondo %s: arresto non riuscito: %s", ident, e)
        elif nostro is None:
            # R-699-1/2-M2: non si sa se il processo è il nostro (niente `ps`): non si ferma,
            # e l'avviso non dice «fermato».
            motivo = "oltre la durata massima, forse ancora in esecuzione"
            logging.warning("sottofondo %s: oltre la durata, processo %s non verificabile: "
                            "non fermato", ident, pid)
    job = _leggi(cartella / f"{Path(ident).name}.json") if ident else None
    chiuso = annulla(root, ident, motivo)
    # R-697-3-M2: si toglie il posto solo se è ancora quello letto (o senza id)
    rilettura = _leggi(posto)
    if rilettura is not None and str(rilettura.get("id") or "") == ident:
        try:
            posto.unlink()
        except FileNotFoundError:
            pass
    if chiuso and job:  # bot #346 V-1: niente «non è finito» per un compito appena riuscito
        _avvisa(root, f"Il compito in sottofondo «{_breve(job.get('compito', ''), 80)}» non è "
                      f"finito: {motivo}.", ident, avvisa)


def _identita(pid: Any, ident: str) -> Optional[bool]:
    """Il pid è il NOSTRO figlio `gas.py sottofondo <ident>`, leader del proprio gruppo?
    True = sì; False = sicuramente no (pid non valido, non leader, comando diverso);
    None = non si sa (`ps` assente o in errore). `ps -ww -o command=` funziona su macOS e
    Linux; `-ww` evita che la riga venga troncata a COLUMNS (CI #345)."""
    try:
        if not isinstance(pid, int) or pid <= 1:
            return False
        try:
            if os.getpgid(pid) != pid:
                return False
        except ProcessLookupError:
            return False
        r = subprocess.run(["ps", "-ww", "-o", "command=", "-p", str(pid)], capture_output=True,
                           text=True, timeout=5)
        if r.returncode != 0:
            return None
        comando = (r.stdout or "").strip()
        return comando.endswith(f"sottofondo {ident}") and "gas.py" in comando
    except Exception:
        return None


def _e_nostro(pid: Any, ident: str) -> bool:
    """R-698-1-M2: nel dubbio False (meglio non fermare che uccidere un processo estraneo)."""
    return _identita(pid, ident) is True


def _giorni_conservazione() -> float:
    giorni = max(1.0, _numero_env("GAS_SOTTOFONDO_GIORNI", GIORNI_CONSERVAZIONE_DEFAULT))
    # Ve #346 V-2: un valore enorme renderebbe il limite -inf (nessuna pulizia) → default
    return giorni if math.isfinite(giorni * 86400) else float(GIORNI_CONSERVAZIONE_DEFAULT)


def _pulisci_vecchi(root: Path) -> None:
    """Bot #345 (head 46596b4) V-2: i compiti FINITI (ok/ko) più vecchi di
    GAS_SOTTOFONDO_GIORNI (default 7) si cancellano: contengono dati dell'operatore e non
    devono accumularsi. Anche i file temporanei rimasti da un crash. Fail-safe §9."""
    cartella = Path(root) / CARTELLA
    limite = time.time() - _giorni_conservazione() * 86400
    try:
        voci = list(cartella.iterdir())
    except OSError:
        return
    posto = _leggi(cartella / ATTIVO) or {}
    for f in voci:
        try:
            if f.name == ATTIVO or f.stat().st_mtime > limite:
                continue
            if f.suffix == ".json":
                job = _leggi(f)
                if not job:
                    continue
                # Bot #349 (a9a17a5) V-1 / R-707-1-M2: anche un compito rimasto «in_coda» o
                # «in_corso» (scrittura fallita, crash) oltre il limite si cancella, se il
                # posto in coda non è suo: contiene dati dell'operatore
                aperto = job.get("stato") in ("in_coda", "in_corso")
                if not (job.get("stato") in ("ok", "ko")
                        or aperto and str(posto.get("id") or "") != f.stem):
                    continue
            elif not (f.name.startswith(".posto.") or ".tmp." in f.name):
                continue
            f.unlink()
        except OSError as e:
            logging.warning("sottofondo: pulizia di %s non riuscita: %s", f.name, e)


_ultima_pulizia: Optional[float] = None  # time.monotonic() dell'ultima pulizia


def controlla(root: Path, avvisa: Optional[Callable[[str, Path], Any]] = None) -> None:
    """Bot #345 (head 46596b4) V-1: chiamata dal kernel all'inizio di ogni turno, così un
    compito il cui processo è morto (kill, riavvio) diventa «ko» e l'operatore viene avvisato
    alla prima interazione, non solo alla richiesta del compito successivo. Costa solo un
    controllo di esistenza quando la coda è vuota. Mai eccezioni (§9)."""
    global _ultima_pulizia
    try:
        cartella = Path(root) / CARTELLA
        if (cartella / ATTIVO).exists():
            _ripulisci(root, avvisa)
        # Bot #346 (2d0977e) V-3: la pulizia dei compiti vecchi anche senza compiti nuovi,
        # al massimo una volta l'ora per processo (un elenco della cartella).
        # Bot #349 (a9a17a5) V-2: orologio monotono (un salto dell'ora non ferma la pulizia)
        adesso = time.monotonic()
        if (_ultima_pulizia is None or adesso - _ultima_pulizia > 3600) and cartella.is_dir():
            _ultima_pulizia = adesso
            _pulisci_vecchi(root)
    except Exception as e:
        logging.warning("sottofondo: controllo non riuscito: %s", e)


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
    _pulisci_vecchi(root)
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


def annulla(root: Path, ident: str, motivo: str) -> bool:
    """R-695-4-M2: avvio fallito → compito «ko» e coda libera (fail-safe, mai eccezioni).
    Bot #346 (3ee02dd) V-1: solo un compito ancora in_coda/in_corso diventa «ko»; uno già
    finito (il figlio ha scritto «ok» un attimo prima) resta com'è. True = il compito era aperto
    e qui si è provato a chiuderlo (anche se la scrittura è fallita): va avvisato."""
    chiuso = False
    try:
        cartella = Path(root) / CARTELLA
        percorso = cartella / f"{Path(ident).name}.json"
        job = _leggi(percorso)
        if job and job.get("stato") in ("in_coda", "in_corso"):
            # Bot #349 V-1: True appena si sa che il compito era aperto, anche se la scrittura
            # poi fallisce (disco pieno): l'avviso all'operatore deve partire lo stesso
            chiuso = True
            job.update(stato="ko", fine=time.time(), errore=motivo)
            _scrivi_privato(percorso, job)
        dati = _leggi(cartella / ATTIVO)
        if dati and dati.get("id") == ident:
            (cartella / ATTIVO).unlink()
    except Exception as e:
        logging.warning("sottofondo %s: annullamento non riuscito: %s", ident, e)
    return chiuso


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
        # R-696-2-M2: l'operatore, a cui è stato promesso un avviso, lo riceve anche qui;
        # R-706-2-M2: niente avviso se il compito risulta già chiuso da altri («ok» scritto
        # prima dell'eccezione, o «ko» già avvisato); un file illeggibile non prova niente
        chiuso = annulla(root, ident, f"interrotto ({type(e).__name__})")
        dopo = _leggi(Path(root) / CARTELLA / f"{Path(ident).name}.json")
        if chiuso or not dopo or dopo.get("stato") not in ("ok", "ko"):
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
    except OSError as e:
        # Bot #349 (147d6c8) V-1: il posto non tolto non deve impedire l'avviso finale
        # promesso; il posto si libera da solo (processo morto → ripulito)
        logging.warning("sottofondo %s: posto non tolto: %s", ident, e)
    titolo = _breve(job["compito"], 80)
    testo = (f"Ho finito il compito in sottofondo «{titolo}». {_breve(risposta, RISPOSTA_AVVISO_MAX)}"
             if ok else
             f"Il compito in sottofondo «{titolo}» non è riuscito: {_breve(job['errore'], 200)}")
    _avvisa(root, testo, ident, avvisa)
    return 0 if ok else 1

# ---- Fetta 3.2 (chat M2, 7 nov): lettura a voce dei compiti finiti ----

LETTI_MAX = 2              # compiti letti a voce per turno
LETTURA_RISPOSTA_MAX = 250  # caratteri della risposta letta a voce (il resto è su Telegram)


def _ore_lettura() -> float:
    ore = max(1.0, _numero_env("GAS_SOTTOFONDO_LEGGI_ORE", 24))
    return ore if math.isfinite(ore * 3600) else 24.0


def da_leggere(root: Path) -> list:
    """Fetta 3.2: compiti finiti (ok/ko) nelle ultime GAS_SOTTOFONDO_LEGGI_ORE (default 24) e
    non ancora letti a voce, i più vecchi prima, al massimo LETTI_MAX. Mai eccezioni (§9)."""
    try:
        cartella = Path(root) / CARTELLA
        if not cartella.is_dir():
            return []
        limite = time.time() - _ore_lettura() * 3600
        finiti = []
        for f in cartella.glob("*.json"):
            if f.name == ATTIVO:
                continue
            job = _leggi(f)
            if (not job or job.get("stato") not in ("ok", "ko") or job.get("letto_a_voce")
                    or not isinstance(job.get("id"), str) or f.stem != job["id"]):
                continue
            try:
                fine = float(job.get("fine") or 0)
            except (TypeError, ValueError):
                continue
            if math.isfinite(fine) and fine >= limite:
                finiti.append((fine, job))
        finiti.sort(key=lambda x: x[0])
        return [job for _, job in finiti[:LETTI_MAX]]
    except Exception as e:
        logging.warning("sottofondo: lettura dei finiti non riuscita: %s", e)
        return []


def frase_finiti(jobs: list) -> str:
    """Le frasi da dire prima della risposta: titolo e un riassunto corto per ogni compito."""
    frasi = []
    for job in jobs:
        titolo = _breve(job.get("compito", ""), 80)
        if job.get("stato") == "ok":
            riassunto = _breve(job.get("risposta", ""), LETTURA_RISPOSTA_MAX)
            # ve #350 V-2: senza risposta niente «:» seguiti dal vuoto
            frasi.append(f"Ho finito il compito in sottofondo «{titolo}»: {riassunto}"
                         if riassunto else f"Ho finito il compito in sottofondo «{titolo}».")
        else:
            frasi.append(f"Il compito in sottofondo «{titolo}» non è riuscito.")
    return " ".join(frasi)


def segna_letti(root: Path, jobs: list) -> None:
    """Segna come letti a voce (così non si ripetono). Mai eccezioni (§9)."""
    for job in jobs:
        try:
            percorso = Path(root) / CARTELLA / f"{Path(str(job.get('id'))).name}.json"
            attuale = _leggi(percorso)
            if attuale and attuale.get("stato") in ("ok", "ko"):
                attuale["letto_a_voce"] = True
                _scrivi_privato(percorso, attuale)
        except Exception as e:
            logging.warning("sottofondo: segno di lettura non scritto: %s", e)
