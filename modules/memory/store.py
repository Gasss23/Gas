"""Livello di persistenza della memoria di GAS — SQLite, FILE SINGOLO.

Perché file singolo (vincolo NON negoziabile): la memoria è il dato più
prezioso e meno rimpiazzabile del sistema (mesi di relazioni coi lead, non
ricostruibili come il codice). Tenerla in UN solo file rende il backup una
banale copia del file. Per questo NON si usa il journal WAL (creerebbe file
collaterali `-wal`/`-shm`): si resta sul journal di rollback di default, così
che il `.db` sia davvero autoconsistente per la copia.

INVARIANTE DI DESIGN (incisa qui e nel report):
  * DIARIO = IMMUTABILE. La storia non si riscrive: solo INSERT. UPDATE e
    DELETE sono vietati a livello di DB da due trigger che fanno RAISE(ABORT)
    — barriera che vale anche da SQL grezzo. CAVEAT (riserva R1 review #12):
    con i default SQLite (`recursive_triggers` OFF) un `INSERT OR REPLACE`
    diretto sulla PK aggira i trigger (il DELETE implicito non li attiva); il
    codice applicativo fa solo INSERT puro, quindi il buco si apre solo a chi
    ha già accesso diretto al file .db. Da blindare alla passata di hardening.
  * CONTATTI = MUTABILI per natura. Lo stato di un lead cambia nel tempo
    (nuovo -> contattato -> ... -> rifiutato/chiuso) e i fatti vecchi vengono
    INVALIDATI: quando un lead passa a "rifiutato"/"chiuso" GAS non deve più
    inseguirlo. È questa regola "aggiorna/invalida" che impedisce alla memoria
    di mentire. Per non confondere i due ruoli, l'identità/dati del contatto si
    aggiornano con upsert_contatto, mentre la TRANSIZIONE di stato passa SOLO
    da update_stato_contatto.

Fail-safe (§9 CLAUDE.md): un DB mancante viene creato; un DB corrotto NON deve
mai far crashare GAS — ogni errore SQLite/IO è loggato come warning nella
scatola nera e l'operazione degrada (scritture -> None/False, letture -> []).

Estensibilità: lo schema è una lista di DDL applicate in modo idempotente
(CREATE ... IF NOT EXISTS). Aggiungere in futuro altri registri (lista lavori,
regole fisse, metriche) significa solo aggiungere DDL a _SCHEMA, senza rifare
le fondamenta.
"""
from __future__ import annotations

import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

log = logging.getLogger(__name__)

# Stati ammessi per un contatto. L'ordine riflette il funnel tipico, ma le
# transizioni NON sono vincolate a esso (un lead può tornare indietro).
STATI_CONTATTO: Tuple[str, ...] = (
    "nuovo", "contattato", "risposto", "interessato", "rifiutato", "chiuso",
)
STATO_DEFAULT: str = "nuovo"
# Stati "invalidanti": il lead è fuori dal gioco, GAS non deve più inseguirlo.
STATI_CHIUSI: frozenset = frozenset({"rifiutato", "chiuso"})

DEFAULT_DB_FILENAME: str = ".gas_memory.db"

# Schema idempotente. NB: niente WAL (vedi docstring di modulo) per restare a
# file singolo. I due trigger sul diario sono la barriera di immutabilità.
_STATI_SQL = ", ".join(f"'{s}'" for s in STATI_CONTATTO)
_SCHEMA: Tuple[str, ...] = (
    # --- DIARIO: log append-only di tutto ciò che GAS fa ---
    """
    CREATE TABLE IF NOT EXISTS diario (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        ts          TEXT    NOT NULL,
        tipo        TEXT    NOT NULL,
        descrizione TEXT    NOT NULL,
        contatto_id INTEGER REFERENCES contatti(id)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_diario_ts ON diario(ts)",
    "CREATE INDEX IF NOT EXISTS idx_diario_contatto ON diario(contatto_id)",
    # Immutabilità del diario imposta dal DB: la storia non si riscrive.
    """
    CREATE TRIGGER IF NOT EXISTS diario_no_update
    BEFORE UPDATE ON diario
    BEGIN
        SELECT RAISE(ABORT, 'diario immutabile: UPDATE vietato');
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS diario_no_delete
    BEFORE DELETE ON diario
    BEGIN
        SELECT RAISE(ABORT, 'diario immutabile: DELETE vietato');
    END
    """,
    # --- CONTATTI: una riga per lead, mutabile/upsert-abile ---
    f"""
    CREATE TABLE IF NOT EXISTS contatti (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        chiave          TEXT    NOT NULL UNIQUE,
        nome            TEXT,
        contatto        TEXT,
        stato           TEXT    NOT NULL DEFAULT '{STATO_DEFAULT}'
                                CHECK (stato IN ({_STATI_SQL})),
        ultimo_contatto TEXT,
        prossima_azione TEXT,
        note            TEXT,
        creato_il       TEXT    NOT NULL,
        aggiornato_il   TEXT    NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_contatti_stato ON contatti(stato)",
)


def default_db_path(root: Union[str, Path]) -> Path:
    """Path di default del DB di memoria: <root>/.gas_memory.db (fuori da git)."""
    return Path(root) / DEFAULT_DB_FILENAME


def _now_iso() -> str:
    """Timestamp ISO8601 in UTC (ordinabile lessicograficamente)."""
    return datetime.now(timezone.utc).isoformat()


class MemoryStore:
    """Accesso al DB di memoria. Connessioni a vita breve (una per operazione):
    semplice, niente stato condiviso fra thread, e ogni metodo è blindato in
    try/except per non far mai crashare GAS (§9)."""

    def __init__(self, db_path: Union[str, Path]) -> None:
        self.db_path: Path = Path(db_path)
        # available = il DB è apribile e lo schema è a posto. Diagnostico: i
        # metodi degradano comunque da soli, ma `gas doctor` potrà leggerlo.
        self.available: bool = False
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            with self._connect() as con:
                self._init_schema(con)
            self.available = True
        except (sqlite3.Error, OSError) as e:
            log.warning("MemoryStore: init fallita su %s (%s) — degrado",
                        self.db_path, e)

    # ------------------------------------------------------------------ infra
    def _connect(self) -> sqlite3.Connection:
        """Connessione configurata: foreign key attive, righe come dict-like.
        Timeout per non bloccarsi su un eventuale lock concorrente."""
        con = sqlite3.connect(str(self.db_path), timeout=10)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def _init_schema(self, con: sqlite3.Connection) -> None:
        for ddl in _SCHEMA:
            con.execute(ddl)
        con.commit()

    @staticmethod
    def _rows(cur: sqlite3.Cursor) -> List[Dict[str, Any]]:
        return [dict(r) for r in cur.fetchall()]

    # --------------------------------------------------------------- scritture
    def append_diario(self, tipo: str, descrizione: str,
                      contatto_id: Optional[int] = None) -> Optional[int]:
        """Aggiunge un evento al diario (append-only). Ritorna l'id della riga,
        o None in caso di degrado. MAI UPDATE/DELETE: questo è l'unico ingresso."""
        try:
            with self._connect() as con:
                cur = con.execute(
                    "INSERT INTO diario (ts, tipo, descrizione, contatto_id) "
                    "VALUES (?, ?, ?, ?)",
                    (_now_iso(), tipo, descrizione, contatto_id),
                )
                con.commit()
                return int(cur.lastrowid)
        except (sqlite3.Error, OSError) as e:
            log.warning("append_diario fallita (%s): %s", self.db_path, e)
            return None

    def upsert_contatto(self, chiave: str, nome: Optional[str] = None,
                        contatto: Optional[str] = None,
                        stato: Optional[str] = None,
                        prossima_azione: Optional[str] = None,
                        note: Optional[str] = None) -> Optional[int]:
        """Inserisce o aggiorna un lead, identificato dalla `chiave` (es. handle
        social / email / telefono normalizzato). In INSERT lo stato è quello
        passato o STATO_DEFAULT. In conflitto si aggiornano SOLO i campi
        anagrafici passati (non-None); lo stato NON si tocca qui: la transizione
        passa SOLO da update_stato_contatto (separazione identità vs. ciclo di
        vita). Ritorna l'id del contatto, o None in degrado."""
        if stato is not None and stato not in STATI_CONTATTO:
            raise ValueError(f"stato non valido: {stato!r} (ammessi: {STATI_CONTATTO})")
        now = _now_iso()
        try:
            with self._connect() as con:
                con.execute(
                    "INSERT INTO contatti "
                    "(chiave, nome, contatto, stato, prossima_azione, note, "
                    " creato_il, aggiornato_il) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
                    "ON CONFLICT(chiave) DO UPDATE SET "
                    "  nome = COALESCE(excluded.nome, contatti.nome), "
                    "  contatto = COALESCE(excluded.contatto, contatti.contatto), "
                    "  prossima_azione = COALESCE(excluded.prossima_azione, contatti.prossima_azione), "
                    "  note = COALESCE(excluded.note, contatti.note), "
                    "  aggiornato_il = excluded.aggiornato_il",
                    (chiave, nome, contatto, stato or STATO_DEFAULT,
                     prossima_azione, note, now, now),
                )
                con.commit()
                row = con.execute(
                    "SELECT id FROM contatti WHERE chiave = ?", (chiave,)
                ).fetchone()
                return int(row["id"]) if row else None
        except (sqlite3.Error, OSError) as e:
            log.warning("upsert_contatto fallita (%s): %s", self.db_path, e)
            return None

    def update_stato_contatto(self, contatto_id: int, nuovo_stato: str,
                             prossima_azione: Optional[str] = None) -> bool:
        """Transizione di stato di un lead (regola aggiorna/invalida). Aggiorna
        anche ultimo_contatto e aggiornato_il (un cambio di stato è un'interazione).
        Ritorna True se una riga è stata aggiornata, False altrimenti/in degrado."""
        if nuovo_stato not in STATI_CONTATTO:
            raise ValueError(f"stato non valido: {nuovo_stato!r} (ammessi: {STATI_CONTATTO})")
        now = _now_iso()
        try:
            with self._connect() as con:
                cur = con.execute(
                    "UPDATE contatti SET "
                    "  stato = ?, ultimo_contatto = ?, aggiornato_il = ?, "
                    "  prossima_azione = COALESCE(?, prossima_azione) "
                    "WHERE id = ?",
                    (nuovo_stato, now, now, prossima_azione, contatto_id),
                )
                con.commit()
                return cur.rowcount > 0
        except (sqlite3.Error, OSError) as e:
            log.warning("update_stato_contatto fallita (%s): %s", self.db_path, e)
            return False

    # ---------------------------------------------------------------- letture
    def diario_recente(self, n: int = 20) -> List[Dict[str, Any]]:
        """Ultimi n eventi del diario, dal più recente. [] in degrado."""
        try:
            with self._connect() as con:
                cur = con.execute(
                    "SELECT * FROM diario ORDER BY id DESC LIMIT ?", (n,)
                )
                return self._rows(cur)
        except (sqlite3.Error, OSError) as e:
            log.warning("diario_recente fallita (%s): %s", self.db_path, e)
            return []

    def diario_di_contatto(self, contatto_id: int) -> List[Dict[str, Any]]:
        """Tutti gli eventi del diario legati a un contatto, dal più recente."""
        try:
            with self._connect() as con:
                cur = con.execute(
                    "SELECT * FROM diario WHERE contatto_id = ? ORDER BY id DESC",
                    (contatto_id,),
                )
                return self._rows(cur)
        except (sqlite3.Error, OSError) as e:
            log.warning("diario_di_contatto fallita (%s): %s", self.db_path, e)
            return []

    def get_contatto(self, contatto_id: int) -> Optional[Dict[str, Any]]:
        """Un contatto per id, o None se assente/in degrado."""
        try:
            with self._connect() as con:
                row = con.execute(
                    "SELECT * FROM contatti WHERE id = ?", (contatto_id,)
                ).fetchone()
                return dict(row) if row else None
        except (sqlite3.Error, OSError) as e:
            log.warning("get_contatto fallita (%s): %s", self.db_path, e)
            return None

    def get_contatto_per_chiave(self, chiave: str) -> Optional[Dict[str, Any]]:
        """Un contatto per la sua chiave univoca (es. email/handle normalizzato),
        o None se assente/in degrado. Lookup esatto, sfrutta l'indice UNIQUE su
        `chiave`: è la via canonica per risolvere chiave -> contatto."""
        try:
            with self._connect() as con:
                row = con.execute(
                    "SELECT * FROM contatti WHERE chiave = ?", (chiave,)
                ).fetchone()
                return dict(row) if row else None
        except (sqlite3.Error, OSError) as e:
            log.warning("get_contatto_per_chiave fallita (%s): %s", self.db_path, e)
            return None

    def lista_contatti(self, filtro_stato: Optional[str] = None
                      ) -> List[Dict[str, Any]]:
        """Elenco contatti, opzionalmente filtrato per stato (es. solo gli
        attivi). [] in degrado. Ordinati per ultimo aggiornamento decrescente."""
        try:
            with self._connect() as con:
                if filtro_stato is not None:
                    cur = con.execute(
                        "SELECT * FROM contatti WHERE stato = ? "
                        "ORDER BY aggiornato_il DESC", (filtro_stato,),
                    )
                else:
                    cur = con.execute(
                        "SELECT * FROM contatti ORDER BY aggiornato_il DESC"
                    )
                return self._rows(cur)
        except (sqlite3.Error, OSError) as e:
            log.warning("lista_contatti fallita (%s): %s", self.db_path, e)
            return []

    # ----------------------------------------------------------------- backup
    def backup(self, dest_dir: Optional[Union[str, Path]] = None) -> Optional[Path]:
        """Copia il DB in un file timestampato (banale perché è un file singolo).
        Usa l'API di backup nativa di SQLite per una copia COERENTE anche con
        scritture in volo. Ritorna il path della copia, o None in degrado.
        La copia ha estensione .bak (già gitignorata)."""
        try:
            base = Path(dest_dir) if dest_dir is not None else self.db_path.parent
            base.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            dest = base / f"{self.db_path.stem}.{ts}.bak"
            with self._connect() as src, sqlite3.connect(str(dest)) as dst:
                src.backup(dst)
            return dest
        except (sqlite3.Error, OSError) as e:
            log.warning("backup fallita (%s): %s", self.db_path, e)
            return None
