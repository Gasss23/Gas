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
import logging
import os
import re
import sqlite3
import threading
import time
import unicodedata
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
NOME_CARTELLA = "Gas CRM (copie cifrate)"
ICLOUD_DRIVE = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs"


def cartella() -> Optional[Path]:
    """Dove va la copia cifrata: GAS_CRM_BACKUP_CIFRATO_DIR, altrimenti iCloud Drive se
    c'è (Mac con iCloud Drive acceso). None = nessuna cartella esterna disponibile."""
    v = os.environ.get("GAS_CRM_BACKUP_CIFRATO_DIR", "").strip()
    if v:
        return Path(v).expanduser()
    if ICLOUD_DRIVE.is_dir():
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


def cifra(dati: bytes, pw: str) -> bytes:
    sale = os.urandom(SALE_BYTE)
    return MAGIA + sale + _fernet(pw, sale).encrypt(dati)


def decifra(blob: bytes, pw: str) -> bytes:
    """Solleva ErroreCRM se il file non è una copia cifrata del CRM o la password è sbagliata."""
    if not blob.startswith(MAGIA) or len(blob) < len(MAGIA) + SALE_BYTE + 1:
        raise ErroreCRM("il file non è una copia cifrata del CRM")
    sale = blob[len(MAGIA):len(MAGIA) + SALE_BYTE]
    from cryptography.fernet import InvalidToken
    try:
        return _fernet(pw, sale).decrypt(blob[len(MAGIA) + SALE_BYTE:])
    except InvalidToken:
        raise ErroreCRM("password sbagliata o file rovinato") from None


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
        dest_dir.mkdir(parents=True, exist_ok=True)
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
        for vecchia in sorted(dest_dir.glob("crm-*" + ESTENSIONE))[:-max(1, keep)]:
            vecchia.unlink(missing_ok=True)
        return dest, None
    except Exception as e:  # §9: il CRM continua; nel log solo il tipo, mai dati
        log.warning("CRM: copia cifrata esterna non riuscita: %s", type(e).__name__)
        return None, f"copia cifrata non riuscita ({type(e).__name__})"
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
    for resto in cartella_esterna.glob("crm-*" + ESTENSIONE + ".*tmp"):
        try:
            if resto.stat().st_mtime < limite:
                resto.unlink(missing_ok=True)
        except OSError:
            pass


_FILE_DI_LAVORO = ("-journal", "-wal", "-shm")


def _integro(percorso: Path) -> bool:
    try:
        con = sqlite3.connect(str(percorso))
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
    if dest.exists() or dest.is_symlink():  # V-2 verifica #386 (2°): anche un collegamento pendente
        raise ErroreCRM(f"{dest} esiste già: non lo sovrascrivo (spostalo o scegli --dest)")
    for suffisso in _FILE_DI_LAVORO:
        resto = dest.with_name(dest.name + suffisso)
        if resto.exists():
            raise ErroreCRM(f"accanto a {dest} è rimasto {resto.name}, un file di lavoro del "
                            "database di prima: spostalo insieme al database vecchio, poi riprova")
    dati = decifra(Path(sorgente).read_bytes(), pw)
    tmp = dest.with_name(dest.name + ".ripristino.tmp")
    creato = False
    try:
        # V-1 verifica #386 (2°): la scrittura del temporaneo IN CHIARO sta dentro il
        # try/finally, così un disco pieno a metà non lascia dati parziali dei clienti
        _scrivi_privato(tmp, dati)
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
                _scrivi_privato(dest, dati, esclusivo=True)
                creato = True
            except FileExistsError:
                raise ErroreCRM(f"{dest} è comparso durante il ripristino: non lo sovrascrivo") from None
            except OSError:
                # V-2 verifica esterna #386 / R-816-1: scrittura interrotta (disco pieno):
                # si toglie il file incompleto appena creato, così si può riprovare
                if dest.exists():
                    dest.unlink(missing_ok=True)
                raise
    finally:
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
