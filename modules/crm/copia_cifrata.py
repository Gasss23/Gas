"""Copia di sicurezza CIFRATA del CRM fuori dal Mac (decisione dell'operatore 2026-11-19).

Il problema: dati e copie del CRM stavano tutti sul Mac; se il Mac si rompe o si perde, si
perde il gestionale. La scelta dell'operatore: una copia al giorno anche su iCloud Drive.

Regole:
- **Mai in chiaro fuori dal Mac.** La copia esce SOLO cifrata (Fernet: AES-128-CBC più HMAC,
  chiave derivata dalla password con scrypt — n=2^17, livello per file attaccabili offline,
  R-815-3 — e un sale casuale per ogni file). Senza password
  (`GAS_CRM_BACKUP_PASSWORD`, almeno PASSWORD_MIN caratteri) o senza la libreria
  `cryptography` la copia esterna resta SPENTA e lo si dice; non si ripiega mai sul chiaro.
- **Dove:** `GAS_CRM_BACKUP_CIFRATO_DIR` se impostata, altrimenti, se esiste, la cartella
  «Gas CRM (copie cifrate)» dentro iCloud Drive del Mac. Una copia al giorno (quella del
  giorno si rinnova a ogni copia), tiene gli ultimi KEEP giorni. File leggibili solo dal
  proprietario (0600).
- **Ripristino:** `python -m modules.crm ripristina FILE` rimette il database da una copia,
  senza mai sovrascrivere un database che c'è già.
- La password sta nel file delle chiavi del Mac: va salvata ANCHE altrove (gestore di
  password), perché senza di lei le copie su iCloud non si aprono.

Funzioni pure o fail-safe (§9): `copia_fuori` non solleva mai, ritorna il motivo.
"""
from __future__ import annotations

import base64
import glob
import logging
import os
import re
import sqlite3
import subprocess
import threading
import time
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

from modules.crm.store import ErroreCRM

log = logging.getLogger(__name__)

MAGIA = b"GASCRM-CIFRATO-1\n"   # intestazione del file cifrato (versione del formato)
SALE_BYTE = 16
PASSWORD_MIN = 12
SCRYPT_N = 2 ** 17       # R-815-3: per file che un attaccante può provare offline (OWASP)
KEEP = 30
ESTENSIONE = ".gascrm"
_NOME_CIFRATA = re.compile(r"crm-[0-9]{8}" + re.escape(ESTENSIONE))  # una al giorno
NOME_CARTELLA = "Gas CRM (copie cifrate)"
ICLOUD_DRIVE = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs"
VOLUMI = Path("/Volumes")  # dischi esterni su macOS


def cartella() -> Optional[Path]:
    """Dove va la copia cifrata: GAS_CRM_BACKUP_CIFRATO_DIR, altrimenti iCloud Drive se
    c'è (Mac con iCloud Drive acceso). None = nessuna cartella esterna disponibile."""
    v = os.environ.get("GAS_CRM_BACKUP_CIFRATO_DIR", "").strip()
    if v:
        try:
            return Path(v).expanduser()
        except RuntimeError:
            # R-825-2: «~utente» che non esiste. Prima il CRM non partiva; ora il percorso
            # resta com'è (non completo) e `_genitore_assente` lo rifiuta: copia in rosso
            return Path(v)
    try:
        if ICLOUD_DRIVE.is_dir():
            return ICLOUD_DRIVE / NOME_CARTELLA
    except OSError:
        # R-825-2: iCloud Drive c'è ma macOS ne nega la lettura (Python 3.11 solleva da
        # is_dir): la copia fallirà e si vedrà in rosso, non «spenta», e il CRM parte
        return ICLOUD_DRIVE / NOME_CARTELLA
    return None


def password() -> Optional[str]:
    """La password senza spazi ai bordi: la stessa misura il minimo e ricava la chiave (R-815-3)."""
    v = _normalizza(os.environ.get("GAS_CRM_BACKUP_PASSWORD", ""))
    return v if len(v) >= PASSWORD_MIN else None


def motivo_spenta() -> Optional[str]:
    """None se la copia cifrata esterna è attiva, altrimenti il motivo (per l'operatore)."""
    if password() is None:
        return (f"manca GAS_CRM_BACKUP_PASSWORD (almeno {PASSWORD_MIN} caratteri) nel file "
                "delle chiavi: senza password nessuna copia esce dal Mac")
    if cartella() is None:
        return ("nessuna cartella esterna: iCloud Drive non trovato e GAS_CRM_BACKUP_CIFRATO_DIR "
                "non impostata")
    try:
        import cryptography  # noqa: F401
    except ImportError:
        return "manca la libreria «cryptography»: pip install -r requirements.txt"
    return None


def _normalizza(pw: str) -> str:
    """V-1 verifica esterna #386: la stessa password con accenti può arrivare in forme Unicode
    diverse (NFC dal .env, NFD digitata altrove): si confronta sempre in NFC, senza spazi ai
    bordi."""
    return unicodedata.normalize("NFC", pw).strip()


def _scrivi_privato(percorso: Path, dati: bytes, esclusivo: bool = False) -> None:
    """Scrive il file leggibile solo dal proprietario (0600): dati dei clienti, anche se
    cifrati (V-4 verifica esterna #386). `esclusivo`: fallisce se il file esiste già."""
    flag = os.O_WRONLY | os.O_CREAT | (os.O_EXCL if esclusivo else os.O_TRUNC)
    fd = os.open(str(percorso), flag, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(dati)
    os.chmod(percorso, 0o600)


def _fernet(pw: str, sale: bytes):  # type: ignore[no-untyped-def]
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    chiave = Scrypt(salt=sale, length=32, n=SCRYPT_N, r=8, p=1).derive(
        _normalizza(pw).encode("utf-8"))
    return Fernet(base64.urlsafe_b64encode(chiave))


def _consiglio_icloud(dest_dir: Path, e: BaseException) -> Optional[str]:
    """V-1 bot #388, R-828-1/2: un permesso negato su iCloud Drive (macOS lo nega all'app che
    non ha l'accesso ai file) dà un motivo che dice cosa fare, sia che fallisca la lettura
    sia la scrittura. None se l'errore non è questo. Mai solleva."""
    try:
        if not isinstance(e, PermissionError):
            return None
        # V-2 bot #388 (7cd7a2f0): percorso risolto e senza badare a maiuscole e minuscole,
        # come `_genitore_assente` (collegamenti simbolici verso iCloud Drive riconosciuti)
        vero = [x.casefold() for x in Path(os.path.realpath(dest_dir)).parts]
        icloud = [x.casefold() for x in Path(os.path.realpath(ICLOUD_DRIVE)).parts]
        if vero[:len(icloud)] != icloud:
            return None
        altrove = ("" if os.environ.get("GAS_CRM_BACKUP_CIFRATO_DIR", "").strip()
                   else ", oppure imposta GAS_CRM_BACKUP_CIFRATO_DIR su un'altra cartella")
        return (f"iCloud Drive non è leggibile o scrivibile ({type(e).__name__}): dai all'app "
                "da cui avvii il CRM (Terminale o simili) l'accesso ai file in Impostazioni di "
                f"Sistema → Privacy e sicurezza{altrove}; nessuna copia fuori dal Mac")
    except Exception:  # §9
        return None


def _genitore_assente(dest_dir: Path) -> Optional[str]:
    """V-1 verifica #386 (3°): la cartella delle copie si crea SOLO se la cartella che la
    contiene esiste già. Con un disco esterno non collegato (/Volumes/…) prima si creava la
    cartella sul disco del Mac e la copia «riusciva» senza uscire dal Mac. Mai solleva
    (V-1 bot #387: un permesso negato su `is_dir` ora è un motivo, non un'eccezione)."""
    # R-826-1: un percorso non completo (es. «~GasCopie» con un utente che non c'è, o
    # «copie») si legge dalla cartella di lavoro, cioè dentro ~/Gas: mai lì le copie
    if not dest_dir.is_absolute():
        return (f"la cartella {dest_dir} non è un percorso completo (deve iniziare con «/» o "
                "«~/»): nessuna copia fuori dal Mac")
    try:
        if not dest_dir.parent.is_dir():
            # V-2 bot #387 (d809f5f1): non sempre è un disco staccato, può essere una
            # cartella mai creata (es. ~/Dropbox/Gas/copie): il motivo dice tutte e due
            return (f"la cartella {dest_dir.parent} non c'è: creala, o collega il disco se è "
                    "su un disco esterno; nessuna copia fuori dal Mac")
        # rischio segnalato dal revisore #821: su macOS un punto di mount vuoto può restare
        # in /Volumes anche a disco staccato; lì la cartella «esiste» ma è sul disco del Mac.
        # Nota #822: si confronta il percorso RISOLTO (collegamenti simbolici) e senza
        # badare a maiuscole e minuscole, come fa il disco del Mac
        vero = Path(os.path.realpath(dest_dir)).parts
        volumi = Path(os.path.realpath(VOLUMI)).parts
        n = len(volumi)
        if len(vero) > n and [x.casefold() for x in vero[:n]] == [x.casefold() for x in volumi]:
            disco = Path(*vero[:n + 1])
            if not os.path.ismount(disco):
                return f"il disco {disco} non è collegato: nessuna copia fuori dal Mac"
        return None
    except OSError as e:
        consiglio = _consiglio_icloud(dest_dir, e)  # V-1 bot #388: dove guardare
        if consiglio:
            return consiglio
        return (f"la cartella {dest_dir.parent} non è accessibile ({type(e).__name__}): "
                "nessuna copia fuori dal Mac")


def prova_scrittura() -> Optional[str]:
    """V-1 bot #386: prova VERA che la copia esterna si può fare (non solo che è configurata):
    crea e toglie un piccolo file nella cartella. None se riesce, altrimenti il motivo.
    Il file di prova contiene byte casuali, mai dati."""
    motivo = motivo_spenta()
    if motivo:
        return motivo
    dest_dir = cartella()
    assert dest_dir is not None
    prova = dest_dir / f".prova-{os.getpid()}-{threading.get_ident()}.tmp"
    assente = _genitore_assente(dest_dir)
    if assente:
        return assente
    try:
        dest_dir.mkdir(exist_ok=True)
        _scrivi_privato(prova, os.urandom(32), esclusivo=True)
        return None
    except Exception as e:  # §9
        return (_consiglio_icloud(dest_dir, e)  # R-828-1
                or f"la cartella {dest_dir} non si può scrivere ({type(e).__name__})")
    finally:
        try:
            prova.unlink(missing_ok=True)
        except OSError:
            pass


PROVA_ATTESA_S = 5.0


def esito_all_avvio(attesa_s: Optional[float] = None) -> str:
    """Riga per l'avvio di `serve`: SPENTA, NON FUNZIONA, NON VERIFICATA o ATTIVA. La prova di
    scrittura gira in un thread con un tempo massimo (R-820-1): una cartella di rete bloccata
    non impedisce più al server di partire."""
    spenta = motivo_spenta()
    if spenta:
        return f"SPENTA ({spenta})"
    # V-1 bot #387: si parte da un esito di FALLIMENTO; solo una prova finita bene lo cambia
    # (prima un'eccezione nel thread lasciava l'esito vuoto e la riga diceva «ATTIVA»)
    esito: dict = {"prova": "prova non conclusa per un errore inatteso"}

    def _prova() -> None:
        try:
            esito["prova"] = prova_scrittura()
        except Exception as e:  # §9
            esito["prova"] = f"prova non riuscita ({type(e).__name__})"

    filo = threading.Thread(target=_prova, name="crm-prova-copia", daemon=True)
    filo.start()
    filo.join(PROVA_ATTESA_S if attesa_s is None else attesa_s)
    if filo.is_alive():
        return ("NON VERIFICATA (la cartella non risponde entro qualche secondo): controlla "
                "l'indicatore in dashboard dopo la prima copia")
    if esito.get("prova"):
        return f"NON FUNZIONA ({esito['prova']}): i dati restano solo sul Mac"
    return f"ATTIVA in {cartella()} (prova di scrittura riuscita)"


def cifra(dati: bytes, pw: str) -> bytes:
    sale = os.urandom(SALE_BYTE)
    return MAGIA + sale + _fernet(pw, sale).encrypt(dati)


def decifra(blob: bytes, pw: str) -> bytes:
    """Solleva ErroreCRM se il file non è una copia cifrata del CRM o la password è sbagliata."""
    if not blob.startswith(MAGIA) or len(blob) < len(MAGIA) + SALE_BYTE + 1:
        raise ErroreCRM("il file non è una copia cifrata del CRM (se sta su iCloud, aprilo prima "
                        "dal Finder perché venga scaricato sul Mac)")
    sale = blob[len(MAGIA):len(MAGIA) + SALE_BYTE]
    from cryptography.fernet import InvalidToken
    try:
        return _fernet(pw, sale).decrypt(blob[len(MAGIA) + SALE_BYTE:])
    except InvalidToken:
        raise ErroreCRM("password sbagliata o file rovinato") from None


def _ruota(dest_dir: Path, dest: Path, keep: int) -> None:
    """Tiene le ultime `keep` copie esterne (una al giorno). R-858-1 (come le copie locali,
    V-1/V-3 #404): contano solo i nomi `crm-AAAAMMGG.gascrm`; la copia appena fatta non si
    cancella mai (orologio tornato indietro); le copie con data oltre domani (orologio andato
    avanti e poi corretto) non contano e non si cancellano, con un avviso nel registro."""
    copie = sorted(c for c in dest_dir.glob("crm-*" + ESTENSIONE) if _NOME_CIFRATA.fullmatch(c.name))
    if _NOME_CIFRATA.fullmatch(dest.name):
        try:
            domani = datetime.strptime(dest.name[4:12], "%Y%m%d") + timedelta(days=1)
        except ValueError:
            domani = None
        if domani is not None:
            limite = f"crm-{domani.strftime('%Y%m%d')}{ESTENSIONE}"
            futuro = [c for c in copie if c.name > limite]
            if futuro:
                log.warning("CRM: %d copie cifrate fuori dal Mac con una data nel futuro "
                            "(orologio del Mac sbagliato?): non contano e non si cancellano",
                            len(futuro))
            copie = [c for c in copie if c.name <= limite]
    for vecchia in copie[:-max(1, keep)]:
        if vecchia != dest:
            vecchia.unlink(missing_ok=True)


def copia_fuori(copia_locale: Path, keep: int = KEEP) -> Tuple[Optional[Path], Optional[str]]:
    """Cifra una copia locale (fatta da CRMStore.backup) e la mette nella cartella esterna.
    Ritorna (percorso, None) se riuscita, (None, motivo) altrimenti. Mai solleva (§9)."""
    motivo = motivo_spenta()
    if motivo:
        return None, motivo
    dest_dir = cartella()
    pw = password()
    assert dest_dir is not None and pw is not None
    tmp: Optional[Path] = None
    try:
        # V-1 bot #387: anche questi controlli dentro il try, «copia_fuori non solleva mai»
        assente = _genitore_assente(dest_dir)
        if assente:
            return None, assente
        # V-5 verifica #386 (3°): una copia locale rovinata non sostituisce la copia buona
        if not _integro(Path(copia_locale)):
            return None, ("la copia locale non è integra: la copia del giorno fuori dal Mac "
                          "resta quella di prima")
        dest_dir.mkdir(exist_ok=True)
        # V-1 bot #386: UNA copia esterna al giorno (quella del giorno si rinnova), così
        # le KEEP copie sono KEEP giorni anche se il CRM si riavvia spesso
        m = re.match(r"crm-\d{8}", Path(copia_locale).stem)
        dest = dest_dir / ((m.group(0) if m else Path(copia_locale).stem) + ESTENSIONE)
        _pulisci_tmp_vecchi(dest_dir)
        # R-817-1: temporaneo UNICO per ogni copia (processo e thread): due copie dello
        # stesso giorno in parallelo (guardiano e `backup` a mano) non si mescolano
        tmp = dest.with_name(f"{dest.name}.{os.getpid()}-{threading.get_ident()}.tmp")
        _scrivi_privato(tmp, cifra(Path(copia_locale).read_bytes(), pw), esclusivo=True)
        os.replace(tmp, dest)
        tmp = None
        _ruota(dest_dir, dest, keep)
        return dest, None
    except Exception as e:  # §9: il CRM continua; nel log solo il tipo, mai dati
        log.warning("CRM: copia cifrata esterna non riuscita: %s", type(e).__name__)
        return None, (_consiglio_icloud(dest_dir, e)  # R-828-1
                      # bot #388 (71137d27) V-3: senza «non riuscita», che l'avviso dice già
                      or f"errore durante la copia cifrata ({type(e).__name__})")
    finally:
        if tmp is not None:  # V-3 bot/verifica #386: niente .tmp lasciati in giro
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass


TMP_VECCHIO_S = 3600.0


def _pulisci_tmp_vecchi(cartella_esterna: Path) -> None:
    """Toglie i `.gascrm.tmp` rimasti da copie interrotte (thread fermato, disco pieno)
    da più di un'ora: cifrati, ma inutili e si accumulerebbero su iCloud."""
    limite = time.time() - TMP_VECCHIO_S
    resti = list(cartella_esterna.glob("crm-*" + ESTENSIONE + ".*tmp"))
    resti += list(cartella_esterna.glob(".prova-*.tmp"))  # verifica #386 (3°): prove interrotte
    for resto in resti:
        try:
            if resto.stat().st_mtime < limite:
                resto.unlink(missing_ok=True)
        except OSError:
            pass


def _processo_vivo(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except (OSError, OverflowError):  # PermissionError: c'è ma è di un altro utente;
        return True  # R-824-1: nel dubbio (anche un PID fuori misura) il file non si tocca
    return True


def _leggi_boottime(testo: str) -> Optional[float]:
    """Secondi dell'avvio da `sysctl -n kern.boottime` di macOS («{ sec = 1700000000, usec =
    … } …»). None se il testo non è in quella forma."""
    m = re.search(r"\{\s*sec\s*=\s*([0-9]{1,12})\b", testo)
    return float(m.group(1)) if m else None


def _avvio_sistema() -> Optional[float]:
    """Ora (epoch) dell'ultimo avvio del sistema, o None se non si sa (allora si decide solo
    col PID e con l'età). Linux: `btime` di /proc/stat; macOS: `sysctl kern.boottime`, con
    un tempo massimo di 2 s. Un valore fuori da (0, adesso] non vale (nota #834: un'ora
    di avvio nel futuro farebbe togliere anche un ripristino in corso). Mai solleva."""
    valore: Optional[float] = None
    try:
        with open("/proc/stat", encoding="ascii") as f:
            for riga in f:
                if riga.startswith("btime "):
                    valore = float(riga.split()[1])
                    break
    except (OSError, ValueError, IndexError):
        pass
    if valore is None:
        try:
            # percorso completo: niente dipendenza dal PATH (nota #834)
            esito = subprocess.run(["/usr/sbin/sysctl", "-n", "kern.boottime"],
                                   capture_output=True, text=True, timeout=2, check=False)
            valore = _leggi_boottime(esito.stdout)
        except Exception:  # §9
            valore = None
    if valore is None or not 0 < valore <= time.time():
        return None
    return valore


MARGINE_AVVIO_S = 60.0


def _pulisci_ripristini_interrotti(dest: Path) -> None:
    """V-1 bot #387 (d809f5f1): un ripristino ucciso a metà (kill -9, Mac spento) lascia
    accanto a `dest` il suo temporaneo IN CHIARO, con un nome unico che nessuno riusa.
    Si tolgono quelli dei processi che non ci sono più; mai un collegamento simbolico, mai
    quelli del processo corrente o di un processo ancora vivo, salvo che siano più vecchi di
    un'ora (V-1 bot #388, 7cd7a2f0: dopo un riavvio il PID può essere di un altro processo;
    un ripristino dura pochi secondi), o salvo che siano di prima dell'ultimo avvio del
    sistema (R-830-1: dopo un riavvio nessun ripristino di prima può essere ancora in corso).
    Gira prima di ogni controllo di `ripristina`, password compresa (verifica esterna #388,
    V-1): toglie solo resti di ripristini finiti male, cosa che chiunque abbia accesso alla
    cartella può già fare. Mai solleva."""
    # R-824-2: solo cifre ASCII, al massimo 10 per il PID
    schema = re.compile(re.escape(dest.name) + r"\.([0-9]{1,10})-[0-9]+\.ripristino\.tmp")
    try:
        resti = list(dest.parent.glob(f"{glob.escape(dest.name)}.*.ripristino.tmp"))
    except OSError:
        return
    avvio: Optional[float] = None
    avvio_letto = False
    for resto in resti:
        m = schema.fullmatch(resto.name)
        if not m:
            continue
        pid = int(m.group(1))
        try:
            if resto.is_symlink():
                continue
            mtime = resto.stat().st_mtime
            vecchio = mtime < time.time() - TMP_VECCHIO_S
            if not vecchio and (pid == os.getpid() or _processo_vivo(pid)):
                if not avvio_letto:  # solo se serve: su macOS è un sysctl
                    avvio, avvio_letto = _avvio_sistema(), True
                if avvio is None or mtime >= avvio - MARGINE_AVVIO_S:
                    continue
            if resto.is_file():
                resto.unlink(missing_ok=True)
                log.warning("CRM: tolto un ripristino interrotto rimasto accanto alla destinazione")
        except OSError:
            pass


_FILE_DI_LAVORO = ("-journal", "-wal", "-shm")


def _integro(percorso: Path) -> bool:
    """Database del CRM integro? In SOLA LETTURA (V-2 bot #387): un percorso che non esiste
    non diventa un file vuoto."""
    try:
        con = sqlite3.connect(Path(percorso).resolve().as_uri() + "?mode=ro", uri=True)
        try:
            ok = con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
            return ok and con.execute("SELECT name FROM sqlite_master WHERE type='table' "
                                      "AND name='crm_clienti'").fetchone() is not None
        finally:
            con.close()
    except sqlite3.Error:
        return False


def ripristina(sorgente: Path, dest: Path, pw: str) -> Path:
    """Decifra `sorgente` in `dest` e controlla che sia un database del CRM integro. Non
    sovrascrive mai: se `dest` esiste solleva ErroreCRM, anche se nasce durante il
    ripristino (R-815-2: creazione esclusiva). Rifiuta se accanto a `dest` è rimasto un file
    di lavoro di SQLite (`-journal`, `-wal`, `-shm`) di un database di prima: SQLite lo
    applicherebbe al file ripristinato rovinandolo (R-815-1). Ritorna `dest`."""
    dest = Path(dest)
    # V-2 bot #388: la pulizia prima di ogni rifiuto. Un ripristino ucciso fra os.link e la
    # cancellazione del temporaneo lascia `dest` (che fermerebbe tutto qui sotto) e il
    # temporaneo IN CHIARO, che così sparisce anche se `dest` esiste ancora
    _pulisci_ripristini_interrotti(dest)
    nome = Path(sorgente).name
    if nome.startswith(".") and nome.endswith(".icloud"):  # V-4 bot #386: segnaposto di iCloud
        raise ErroreCRM("il file è ancora solo su iCloud (segnaposto «.icloud»): aprilo dal "
                        "Finder per scaricarlo sul Mac, poi riprova col file vero")
    if dest.exists() or dest.is_symlink():  # V-2 verifica #386 (2°): anche un collegamento pendente
        raise ErroreCRM(f"{dest} esiste già: non lo sovrascrivo (spostalo o scegli --dest)")
    for suffisso in _FILE_DI_LAVORO:
        resto = dest.with_name(dest.name + suffisso)
        if resto.exists() or resto.is_symlink():  # V-4 verifica #386 (3°)
            raise ErroreCRM(f"accanto a {dest} è rimasto {resto.name}, un file di lavoro del "
                            "database di prima: spostalo insieme al database vecchio, poi riprova")
    try:
        blob = Path(sorgente).read_bytes()
    except OSError as e:  # verifica esterna #388, V-2: un messaggio che dice cosa controllare
        raise ErroreCRM(f"non riesco a leggere {sorgente} ({type(e).__name__}): controlla il "
                        "percorso del file .gascrm") from None
    dati = decifra(blob, pw)
    # V-3 bot/verifica #386 (3°): temporaneo IN CHIARO con nome unico e creazione esclusiva
    # (O_EXCL non segue un collegamento simbolico messo lì): mai scritto dentro un altro file
    tmp = dest.with_name(f"{dest.name}.{os.getpid()}-{threading.get_ident()}.ripristino.tmp")
    creato = False
    tmp_nostro = True
    try:
        # V-1 verifica #386 (2°): la scrittura del temporaneo IN CHIARO sta dentro il
        # try/finally, così un disco pieno a metà non lascia dati parziali dei clienti
        try:
            _scrivi_privato(tmp, dati, esclusivo=True)
        except FileExistsError:
            tmp_nostro = False  # non è nostro: non si tocca
            raise ErroreCRM(f"c'è già un file {tmp.name} accanto alla destinazione: spostalo e "
                            "riprova") from None
        if not _integro(tmp):
            raise ErroreCRM("la copia decifrata non è un database del CRM integro")
        try:
            os.link(tmp, dest)  # fallisce da solo se dest esiste nel frattempo
            creato = True
        except FileExistsError:
            raise ErroreCRM(f"{dest} è comparso durante il ripristino: non lo sovrascrivo") from None
        except OSError:
            # file system senza collegamenti fisici: creazione esclusiva
            try:
                fd = os.open(str(dest), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            except FileExistsError:
                raise ErroreCRM(f"{dest} è comparso durante il ripristino: non lo sovrascrivo") from None
            creato = True  # nota #819: il file è nostro SOLO da qui (creato in esclusiva)
            try:
                with os.fdopen(fd, "wb") as f:
                    f.write(dati)
                os.chmod(dest, 0o600)
            except OSError:
                # V-2 verifica esterna #386 / R-816-1: scrittura interrotta (disco pieno):
                # si toglie il file incompleto creato da noi, così si può riprovare
                dest.unlink(missing_ok=True)
                raise
    finally:
        if tmp_nostro:
            tmp.unlink(missing_ok=True)
    # R-815-1: ricontrollo sul file vero, al suo posto. Se fallisce, il file creato da QUESTO
    # ripristino si toglie (V-2 verifica esterna #386): niente database rovinato lasciato lì
    if not _integro(dest):
        if creato:
            dest.unlink(missing_ok=True)
            for suffisso in _FILE_DI_LAVORO:
                dest.with_name(dest.name + suffisso).unlink(missing_ok=True)
        raise ErroreCRM(f"il database ripristinato in {dest} non risulta integro: l'ho tolto, "
                        "controlla i file accanto e riprova")
    return dest
