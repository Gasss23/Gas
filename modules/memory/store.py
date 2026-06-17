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
import re
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
        aggiornato_il   TEXT    NOT NULL,
        -- merged_into: se valorizzato, questa scheda è una LAPIDE che punta al
        -- lead canonico (stesso lead salvato con un'altra chiave; vedi R-crm-1b).
        -- NULL = lead vivo. Le letture seguono il puntatore; il diario resta
        -- IMMUTABILE (nessun UPDATE/DELETE: gli eventi della lapide confluiscono
        -- nella storia del canonico via diario_di_contatto).
        merged_into     INTEGER REFERENCES contatti(id)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_contatti_stato ON contatti(stato)",
    # NB: l'indice su merged_into NON sta qui ma in _ensure_columns, DOPO che la
    # migrazione ha garantito la colonna: su un DB legacy (tabella contatti senza
    # merged_into) crearlo qui solleverebbe "no such column" e manderebbe l'init in
    # degrado proprio sui DB che la migrazione deve salvare.
)


def default_db_path(root: Union[str, Path]) -> Path:
    """Path di default del DB di memoria: <root>/.gas_memory.db (fuori da git)."""
    return Path(root) / DEFAULT_DB_FILENAME


def _now_iso() -> str:
    """Timestamp ISO8601 in UTC (ordinabile lessicograficamente)."""
    return datetime.now(timezone.utc).isoformat()


def normalizza_chiave(chiave: Optional[str]) -> str:
    """Canonicalizzazione DETERMINISTICA e PURA della chiave di un contatto, così
    che la STESSA chiave logica risolva SEMPRE allo stesso record ('Anna ' e
    'anna' = lo stesso lead). È la difesa contro i doppioni silenziosi del CRM
    autopilot (la rubrica deduplica solo a parità di chiave ESATTA via UNIQUE).

    SOLO trasformazioni prevedibili, NIENTE fuzzy / euristica / merge:
      * coercizione a str (robustezza ai tipi non-stringa);
      * collasso di ogni sequenza di whitespace — anche tab/newline — in un
        singolo spazio + trim esterno (tramite ``str.split()``);
      * lower-case, coerente col confronto substring case-insensitive di lettura.

    Funzione PURA e IDEMPOTENTE: ``normalizza(normalizza(x)) == normalizza(x)``.
    Fail-safe (§9 CLAUDE.md): ``None`` o valore non convertibile → ``""`` (mai
    un'eccezione). La chiave vuota viene poi rifiutata a monte (salva_contatto),
    quindi un input malformato degrada in modo sicuro senza creare un record
    spurio. NB: si applica al CONFRONTO esatto (scrittura + lookup per chiave),
    NON trasforma il substring di lettura in altro (l'asimmetria resta intatta)."""
    if chiave is None:
        return ""
    try:
        testo = str(chiave)
    except Exception:  # pragma: no cover — coercizione difensiva, mai un crash
        return ""
    return " ".join(testo.split()).lower()


class MemoryStore:
    """Accesso al DB di memoria. Connessioni a vita breve (una per operazione):
    semplice, niente stato condiviso fra thread, e ogni metodo è blindato in
    try/except per non far mai crashare GAS (§9)."""

    def __init__(self, db_path: Union[str, Path]) -> None:
        self.db_path: Path = Path(db_path)
        # available = il DB è apribile e lo schema è a posto. Diagnostico: i
        # metodi degradano comunque da soli, ma `gas doctor` potrà leggerlo.
        self.available: bool = False
        # fts_available = l'indice di ricerca testuale FTS5 (Strato A del Vector
        # DB) è attivo. OPZIONALE: alcuni build di SQLite non hanno FTS5; in tal
        # caso resta False e cerca_diario degrada a [] (ricorda ricade su substring).
        self.fts_available: bool = False
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
        self._ensure_columns(con)
        con.commit()
        # FTS è OPZIONALE e separato: un suo fallimento NON deve mandare in
        # degrado l'intera memoria (la ricerca substring resta come pavimento).
        self._init_fts(con)

    def _init_fts(self, con: sqlite3.Connection) -> None:
        """Indice di ricerca testuale FTS5 sul diario — STRATO A del Vector DB di
        FASE 2: ricerca per parole/radici con ranking BM25, DENTRO lo stesso file
        .db (invariante file singolo: il backup resta una copia del file). È un
        indice DERIVATO external-content (referenzia il diario per rowid, non
        duplica il testo) tenuto in sync da un trigger AFTER INSERT — e basta:
        il diario è append-only, niente UPDATE/DELETE, quindi l'immutabilità resta
        intatta. OPZIONALE e fail-safe: se il build SQLite non espone FTS5,
        fts_available resta False e cerca_diario ritorna [] (ricorda ricade su
        substring). NON solleva: l'errore è confinato qui, l'init principale è già
        committato e self.available NON viene toccato."""
        try:
            con.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS diario_fts USING fts5("
                "descrizione, tipo, content='diario', content_rowid='id')"
            )
            con.execute(
                "CREATE TRIGGER IF NOT EXISTS diario_fts_ai AFTER INSERT ON diario "
                "BEGIN INSERT INTO diario_fts(rowid, descrizione, tipo) "
                "VALUES (new.id, new.descrizione, new.tipo); END"
            )
            # Backfill idempotente: indicizza il diario PREESISTENTE (DB legacy o
            # righe scritte prima che l'indice esistesse). 'rebuild' ricostruisce
            # l'indice external-content dalla tabella sorgente.
            con.execute("INSERT INTO diario_fts(diario_fts) VALUES('rebuild')")
            con.commit()
            self.fts_available = True
        except sqlite3.Error as e:
            log.warning("FTS5 non disponibile su %s (%s) — ricerca substring "
                        "come fallback", self.db_path, e)
            self.fts_available = False

    @staticmethod
    def _ensure_columns(con: sqlite3.Connection) -> None:
        """Migrazione idempotente per DB già esistenti (i DB freschi hanno già le
        colonne dal CREATE TABLE). ALTER ADD COLUMN con default NULL: NON
        distruttivo e compatibile con i foreign key (la colonna nasce NULL).
        Sul DB di sviluppo (vuoto) è un no-op; serve per il futuro su VPS."""
        cols = {r["name"] for r in con.execute("PRAGMA table_info(contatti)")}
        if "merged_into" not in cols:
            con.execute(
                "ALTER TABLE contatti ADD COLUMN merged_into "
                "INTEGER REFERENCES contatti(id)"
            )
        # L'indice si crea QUI, dopo che la colonna esiste di sicuro (sia su DB
        # fresco sia migrato): non può precedere l'ALTER. IF NOT EXISTS → idempotente.
        con.execute(
            "CREATE INDEX IF NOT EXISTS idx_contatti_merged ON contatti(merged_into)"
        )

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
        # Canonicalizza la chiave PRIMA di INSERT e SELECT: 'Anna ' e 'anna'
        # devono finire (e ritrovarsi) nello stesso record (anti-doppioni CRM).
        chiave = normalizza_chiave(chiave)
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

    def unisci_contatti(self, chiave_da: str, chiave_verso: str) -> Optional[int]:
        """Fonde due schede dello STESSO lead salvato con chiavi DIVERSE (R-crm-1b:
        es. 'anna@ex.com' e 'Anna', che normalizza_chiave non unisce e non deve).
        MERGE A LAPIDE, non distruttivo e COMPATIBILE con l'immutabilità del diario:

          1. l'anagrafica MANCANTE del canonico ('verso') viene completata con i
             dati del doppione ('da') — solo i campi NULL, via COALESCE;
          2. eventuali lapidi che puntavano a 'da' vengono ri-puntate al canonico
             (invariante: ogni lapide punta SEMPRE a un canonico vivo, catena
             profonda al più 1);
          3. 'da' viene marcato come lapide (merged_into = id del canonico).

        NESSUN UPDATE/DELETE sul diario: gli eventi di 'da' restano e confluiscono
        nella storia del canonico via diario_di_contatto. Lo STATO del funnel NON
        si tocca (resta quello del canonico): la transizione passa SOLO da
        update_stato_contatto. Idempotente: fondere ciò che è già fuso, o un lead
        in se stesso, è un no-op. Ritorna l'id del lead canonico, o None se una
        delle due chiavi non esiste / in degrado (§9)."""
        try:
            with self._connect() as con:
                verso = self._risolvi_canonico(con, normalizza_chiave(chiave_verso))
                da = self._risolvi_canonico(con, normalizza_chiave(chiave_da))
                if verso is None or da is None:
                    return None
                canonico_id, da_id = int(verso["id"]), int(da["id"])
                if da_id == canonico_id:
                    return canonico_id  # già lo stesso lead: no-op idempotente
                now = _now_iso()
                # 1) completa l'anagrafica del canonico dai campi del doppione
                con.execute(
                    "UPDATE contatti SET "
                    "  nome = COALESCE(nome, ?), "
                    "  contatto = COALESCE(contatto, ?), "
                    "  prossima_azione = COALESCE(prossima_azione, ?), "
                    "  note = COALESCE(note, ?), "
                    "  aggiornato_il = ? "
                    "WHERE id = ?",
                    (da.get("nome"), da.get("contatto"), da.get("prossima_azione"),
                     da.get("note"), now, canonico_id),
                )
                # 2) ri-punta al canonico le lapidi che puntavano al doppione
                con.execute(
                    "UPDATE contatti SET merged_into = ? WHERE merged_into = ?",
                    (canonico_id, da_id),
                )
                # 3) marca il doppione come lapide del canonico
                con.execute(
                    "UPDATE contatti SET merged_into = ?, aggiornato_il = ? "
                    "WHERE id = ?",
                    (canonico_id, now, da_id),
                )
                con.commit()
                return canonico_id
        except (sqlite3.Error, OSError) as e:
            log.warning("unisci_contatti fallita (%s): %s", self.db_path, e)
            return None

    # ---------------------------------------------------------------- letture
    @staticmethod
    def _risolvi_canonico(con: sqlite3.Connection, chiave: str
                          ) -> Optional[Dict[str, Any]]:
        """Risolve una chiave GIÀ normalizzata al record CANONICO, seguendo la
        catena merged_into fino al lead vivo. Bounded da un set di id visti
        (anti-ciclo difensivo, anche se l'invariante tiene la catena a 1). Ritorna
        None se la chiave non esiste."""
        row = con.execute(
            "SELECT * FROM contatti WHERE chiave = ?", (chiave,)
        ).fetchone()
        if row is None:
            return None
        visti = set()
        while row["merged_into"] is not None and int(row["id"]) not in visti:
            visti.add(int(row["id"]))
            nxt = con.execute(
                "SELECT * FROM contatti WHERE id = ?", (row["merged_into"],)
            ).fetchone()
            if nxt is None:
                break
            row = nxt
        return dict(row)

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

    @staticmethod
    def _fts_match(testo: str) -> str:
        """Costruisce una query MATCH FTS5 SICURA da testo libero: estrae i soli
        token alfanumerici (Unicode-aware) e li mette ciascuno tra virgolette con
        suffisso '*' (prefix match: 'ann' trova 'Anna'), in AND implicito. Le
        virgolette neutralizzano i caratteri speciali della sintassi FTS5
        (operatori AND/OR/NOT, parentesi, ecc.) → nessun errore di sintassi su
        input arbitrario dell'utente. '' se non c'è alcun token (→ nessuna ricerca)."""
        token = re.findall(r"\w+", str(testo or "").lower(), flags=re.UNICODE)
        if not token:
            return ""
        return " ".join(f'"{t}"*' for t in token)

    def cerca_diario(self, testo: str, n: int = 10) -> List[Dict[str, Any]]:
        """Ricerca testuale sul diario via FTS5 (Strato A del Vector DB): per
        parole/radici, ordinata per pertinenza (BM25, più pertinente prima).
        Ritorna le righe complete del diario. [] se FTS è assente, la query è
        vuota di token, o in degrado (§9): in tutti questi casi chi chiama
        (ricorda) ricade sulla ricerca substring storica."""
        if not self.fts_available:
            return []
        match = self._fts_match(testo)
        if not match:
            return []
        try:
            with self._connect() as con:
                cur = con.execute(
                    "SELECT d.* FROM diario_fts f JOIN diario d ON d.id = f.rowid "
                    "WHERE diario_fts MATCH ? ORDER BY bm25(diario_fts) LIMIT ?",
                    (match, n),
                )
                return self._rows(cur)
        except (sqlite3.Error, OSError) as e:
            log.warning("cerca_diario fallita (%s): %s", self.db_path, e)
            return []

    def diario_di_contatto(self, contatto_id: int) -> List[Dict[str, Any]]:
        """Tutti gli eventi del diario legati a un contatto, dal più recente."""
        try:
            with self._connect() as con:
                # Include anche gli eventi delle LAPIDI fuse in questo contatto
                # (merge a lapide R-crm-1b): la storia del canonico abbraccia il
                # passato dei doppioni assorbiti, senza toccare il diario immutabile.
                cur = con.execute(
                    "SELECT * FROM diario WHERE contatto_id = ? "
                    "OR contatto_id IN (SELECT id FROM contatti WHERE merged_into = ?) "
                    "ORDER BY id DESC",
                    (contatto_id, contatto_id),
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
        `chiave`: è la via canonica per risolvere chiave -> contatto. La chiave
        viene canonicalizzata (stesso normalizza_chiave dell'upsert) così che il
        lookup risolva alla stessa identità logica con cui è stata scritta. Se la
        chiave appartiene a una LAPIDE (lead fuso, R-crm-1b), segue il puntatore e
        ritorna il lead CANONICO: una vecchia chiave continua a risolvere al lead
        vivo dopo un merge."""
        try:
            chiave = normalizza_chiave(chiave)
            with self._connect() as con:
                return self._risolvi_canonico(con, chiave)
        except (sqlite3.Error, OSError) as e:
            log.warning("get_contatto_per_chiave fallita (%s): %s", self.db_path, e)
            return None

    def lista_contatti(self, filtro_stato: Optional[str] = None
                      ) -> List[Dict[str, Any]]:
        """Elenco contatti VIVI, opzionalmente filtrato per stato (es. solo gli
        attivi). [] in degrado. Ordinati per ultimo aggiornamento decrescente. Le
        LAPIDI (lead fusi, merged_into valorizzato) sono ESCLUSE: l'elenco, il pin
        always-on e la ricerca substring vedono solo i lead canonici, mai i
        doppioni assorbiti."""
        try:
            with self._connect() as con:
                if filtro_stato is not None:
                    cur = con.execute(
                        "SELECT * FROM contatti WHERE stato = ? "
                        "AND merged_into IS NULL "
                        "ORDER BY aggiornato_il DESC", (filtro_stato,),
                    )
                else:
                    cur = con.execute(
                        "SELECT * FROM contatti WHERE merged_into IS NULL "
                        "ORDER BY aggiornato_il DESC"
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
