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

import json
import logging
import re
import sqlite3
import time
import unicodedata
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
# Quante copie .bak tenere di default (rotazione anti-accumulo, come la retention
# degli snapshot). Il backup locale protegge dall'AUTO-CORRUZIONE; quello
# off-machine è da FASE 5 (deploy VPS). Override via env nel kernel.
DEFAULT_BACKUP_KEEP: int = 10

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
        -- chiave = valore AS-ENTERED (grafia originale, leggibile). NON è più
        -- l'identità: l'unicità sta su chiave_norm (indice UNIQUE in _ensure_columns).
        chiave          TEXT    NOT NULL,
        -- chiave_norm = forma canonica derivata da `chiave` (normalizza_chiave).
        -- È l'IDENTITÀ del lead: due grafie della stessa chiave logica condividono
        -- chiave_norm → un solo record (anti-doppioni R-crm-1). L'indice UNIQUE si
        -- crea in _ensure_columns DOPO il backfill (e solo se zero collisioni).
        chiave_norm     TEXT    NOT NULL,
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


class ChiaveNormCollisione(Exception):
    """Sollevata dalla migrazione R-crm-1 quando due (o più) contatti storici
    collassano sulla STESSA ``chiave_norm``: sono duplicati da fondere a mano.
    La migrazione NON fonde nulla in automatico (il merge dei lead è decisione
    UMANA) — blocca l'init e riporta i gruppi in conflitto. Vedi MemoryStore."""


def normalizza_chiave(chiave: Optional[str]) -> str:
    """Canonicalizzazione DETERMINISTICA e PURA della chiave di un contatto, così
    che la STESSA chiave logica risolva SEMPRE allo stesso record ('Anna ' e
    'anna' = lo stesso lead). È la difesa contro i doppioni silenziosi del CRM
    autopilot (la rubrica deduplica sulla colonna derivata ``chiave_norm`` UNIQUE).

    SOLO trasformazioni prevedibili, NIENTE fuzzy / euristica / merge:
      * coercizione a str (robustezza ai tipi non-stringa);
      * normalizzazione Unicode NFKC: unifica le forme di compatibilità (larghezza
        piena 'Ａ'→'A', legature 'ﬁ'→'fi', spazi esotici) così che varianti
        tipograficamente diverse della stessa stringa convergano;
      * collasso di ogni sequenza di whitespace — anche tab/newline — in un
        singolo spazio + trim esterno (tramite ``str.split()``);
      * lower-case, coerente col confronto substring case-insensitive di lettura.

    v1: NESSUNA logica speciale per telefono/email (es. strip del '+' iniziale o
    del dominio): è solo canonicalizzazione LESSICALE. La normalizzazione per-tipo
    è una fetta dedicata futura (lasciata come nota, non implementata).

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
    # NFKC PRIMA del collasso/lower: espande i caratteri di compatibilità (alcuni
    # dei quali sono spazi), così che il successivo split()/lower() produca un
    # punto fisso (idempotenza preservata su input tipografici).
    try:
        testo = unicodedata.normalize("NFKC", testo)
    except (TypeError, ValueError):  # pragma: no cover — input esotico, mai crash
        pass
    return " ".join(testo.split()).lower()


_PREFISSO_ITALIA = "39"


def normalizza_telefono(valore: Optional[str]) -> str:
    """Forma canonica di un numero di telefono per il confronto (PURA, IDEMPOTENTE).

    Passi: strip dei separatori (spazi/trattini/punti/parentesi), equivalenza tra
    '+' e '00' iniziali (standard ITU-T), aggiunta automatica del prefisso Italia
    (39) per i numeri locali italiani a 9-10 cifre che iniziano con '0' o '3'.
    Range valido post-normalizzazione: 9-15 cifre (E.164). Ignora valori con '@'
    (sono email, non telefoni).

    Fail-safe (§9): None/non convertibile/fuori range → '' (mai eccezione).
    Idempotente: normalizza_telefono(normalizza_telefono(x)) == normalizza_telefono(x).
    """
    if valore is None:
        return ""
    try:
        s = str(valore).strip()
    except Exception:  # pragma: no cover — coercizione difensiva
        return ""
    if "@" in s:
        return ""  # è un'email, non un telefono
    # Rimuovi tutto tranne cifre e il '+' iniziale
    raw = re.sub(r"[^\d+]", "", s)
    if not raw:
        return ""
    # '+' e '00' iniziali sono equivalenti (ITU-T): normalizza a sole cifre
    if raw.startswith("+"):
        digits = raw[1:]
    elif raw.startswith("00"):
        digits = raw[2:]
    else:
        digits = raw
    # Strip difensivo: rimuove eventuali '+' interni residui da input patologici
    digits = re.sub(r"\D", "", digits)
    # Numero locale italiano (9-10 cifre che inizia con '0' o '3', senza prefisso
    # 39 già presente): aggiunge il prefisso paese. Il controllo su '0'/'3' evita
    # di aggiungere '39' a numeri stranieri brevi.
    if (9 <= len(digits) <= 10
            and (digits.startswith("0") or digits.startswith("3"))
            and not digits.startswith(_PREFISSO_ITALIA)):
        digits = _PREFISSO_ITALIA + digits
    # Valida range E.164: 9-15 cifre totali
    if not (9 <= len(digits) <= 15):
        return ""
    return digits


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
        # Se la migrazione R-crm-1 trova duplicati storici sulla stessa chiave_norm
        # NON fonde nulla: blocca l'init e registra qui il dettaglio dei gruppi in
        # conflitto, perché il merge dei lead è una decisione UMANA (diagnostico
        # leggibile da gas doctor / dall'operatore). None = nessuna collisione.
        self.collisione_chiave_norm: Optional[str] = None
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            with self._connect() as con:
                self._init_schema(con)
            self.available = True
        except ChiaveNormCollisione as e:
            # available resta False: la memoria NON opera su dati ambigui finché un
            # umano non fonde i duplicati (fail-closed sul merge — §9, mai crash).
            self.collisione_chiave_norm = str(e)
            log.error("MemoryStore: %s — memoria NON operativa finché un umano non "
                      "fonde i duplicati storici", e)
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
        Sul DB di sviluppo (vuoto) è un no-op; serve per il futuro su VPS.

        R-crm-1 (identità su chiave_norm): garantisce la colonna ``chiave_norm``,
        la BACKFILLA per le righe storiche (deriva da ``chiave``, non tocca altro)
        e crea l'indice UNIQUE — ma SOLO se non ci sono COLLISIONI. Se due righe
        diverse collassano sulla stessa chiave_norm sono duplicati storici: NON si
        fonde nulla e NON si crea l'indice → ChiaveNormCollisione coi gruppi in
        conflitto, perché il merge dei lead è una decisione UMANA (mai automatica).
        ADDITIVA e SICURA: il backfill scrive SOLO la nuova colonna; `chiave` e i
        dati anagrafici restano intatti anche se la migrazione si ferma."""
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
        # --- R-crm-1: colonna chiave_norm (identità canonica) ---
        if "chiave_norm" not in cols:
            # nullable nell'ALTER (un DB con righe non ammette NOT NULL senza
            # default); il backfill qui sotto la popola subito. I DB freschi ce
            # l'hanno già NOT NULL dal CREATE TABLE: per loro questo ramo non scatta.
            con.execute("ALTER TABLE contatti ADD COLUMN chiave_norm TEXT")
        # Backfill: deriva chiave_norm da `chiave` SOLO per le righe che ne sono
        # prive (NULL). NON tocca nessun altro campo → niente fusione, niente perdita.
        for r in con.execute(
            "SELECT id, chiave FROM contatti WHERE chiave_norm IS NULL"
        ).fetchall():
            con.execute(
                "UPDATE contatti SET chiave_norm = ? WHERE id = ?",
                (normalizza_chiave(r["chiave"]), r["id"]),
            )
        # Rilevamento COLLISIONI prima dell'indice UNIQUE: più righe sulla stessa
        # chiave_norm = duplicati storici da fondere a mano. STOP GATE R-crm-1:
        # non fondere, non creare l'indice, riportare i gruppi e fermarsi.
        collisioni = con.execute(
            "SELECT chiave_norm AS k, COUNT(*) AS c, GROUP_CONCAT(id) AS ids "
            "FROM contatti WHERE chiave_norm IS NOT NULL "
            "GROUP BY chiave_norm HAVING c > 1 ORDER BY k"
        ).fetchall()
        if collisioni:
            dettaglio = "; ".join(
                f"{row['k']!r} → righe {row['ids']}" for row in collisioni
            )
            raise ChiaveNormCollisione(
                "migrazione chiave_norm bloccata: duplicati storici sulla stessa "
                f"chiave normalizzata, da fondere MANUALMENTE ({dettaglio})"
            )
        # Zero collisioni → l'unicità dell'identità è imponibile. IF NOT EXISTS →
        # idempotente (DB fresco e DB migrato pulito passano entrambi di qui).
        con.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_contatti_chiave_norm "
            "ON contatti(chiave_norm)"
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
        # `chiave` resta AS-ENTERED (grafia originale conservata); l'identità è la
        # forma canonica chiave_norm: 'Anna ' e 'anna' condividono chiave_norm →
        # un solo record (anti-doppioni CRM), ma la grafia digitata resta leggibile.
        chiave_in = "" if chiave is None else str(chiave)
        chiave_norm = normalizza_chiave(chiave)
        now = _now_iso()
        try:
            with self._connect() as con:
                # ON CONFLICT(chiave_norm): il conflitto è sull'IDENTITÀ canonica.
                # In update NON si tocca `chiave` → si preserva la PRIMA grafia vista.
                con.execute(
                    "INSERT INTO contatti "
                    "(chiave, chiave_norm, nome, contatto, stato, prossima_azione, "
                    " note, creato_il, aggiornato_il) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) "
                    "ON CONFLICT(chiave_norm) DO UPDATE SET "
                    "  nome = COALESCE(excluded.nome, contatti.nome), "
                    "  contatto = COALESCE(excluded.contatto, contatti.contatto), "
                    "  prossima_azione = COALESCE(excluded.prossima_azione, contatti.prossima_azione), "
                    "  note = COALESCE(excluded.note, contatti.note), "
                    "  aggiornato_il = excluded.aggiornato_il",
                    (chiave_in, chiave_norm, nome, contatto, stato or STATO_DEFAULT,
                     prossima_azione, note, now, now),
                )
                con.commit()
                row = con.execute(
                    "SELECT id FROM contatti WHERE chiave_norm = ?", (chiave_norm,)
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

    def unisci_contatti_con_snapshot(
        self, chiave_da: str, chiave_verso: str
    ) -> Optional[Dict[str, Any]]:
        """Merge atomico con rete di sicurezza (R-crm-1b Fetta 1, comando umano CLI).

        Identico a unisci_contatti (lapide, COALESCE, ri-punta lapidi esistenti) ma
        aggiunge due INSERT nel diario COME PRIMA COSA della stessa transazione:
          - 'merge_snapshot': snapshot integrale JSON del record 'da' (pre-merge);
          - 'merge_evento': riepilogo campi riempiti e conflitti.

        FAIL-SAFE (invariante non opzionale): se i write sul diario falliscono,
        l'intera transazione fa ROLLBACK automatico → rubrica invariata. Garantito
        dal fatto che tutti gli INSERT/UPDATE sono nello stesso 'with con:' SQLite.

        Ritorna un dict {canonico_id, campi_riempiti, conflitti, no_op} oppure None
        in caso di chiave mancante o degrado (§9). 'no_op=True' = lead già identici.
        """
        try:
            with self._connect() as con:
                verso = self._risolvi_canonico(con, normalizza_chiave(chiave_verso))
                da = self._risolvi_canonico(con, normalizza_chiave(chiave_da))
                if verso is None or da is None:
                    return None
                canonico_id, da_id = int(verso["id"]), int(da["id"])
                if da_id == canonico_id:
                    return {"canonico_id": canonico_id, "campi_riempiti": [],
                            "conflitti": [], "no_op": True}

                # Calcola preview (campi da riempire e conflitti)
                campi_testo = ("nome", "contatto", "prossima_azione", "note")
                campi_riempiti: List[Tuple[str, str]] = []
                conflitti: List[Tuple[str, str, str]] = []
                for campo in campi_testo:
                    v_val = verso.get(campo) or ""
                    d_val = da.get(campo) or ""
                    if not v_val and d_val:
                        campi_riempiti.append((campo, d_val))
                    elif v_val and d_val and v_val != d_val:
                        conflitti.append((campo, v_val, d_val))

                now = _now_iso()

                # RETE DI SICUREZZA: snapshot di 'da' NEL DIARIO prima di ogni UPDATE
                snapshot_desc = (
                    f"MERGE SNAPSHOT — lead '{chiave_da}' (id={da_id}) fuso in "
                    f"'{chiave_verso}' (id={canonico_id}). "
                    f"Snapshot: {json.dumps(dict(da), ensure_ascii=False, default=str)}"
                )
                con.execute(
                    "INSERT INTO diario (ts, tipo, descrizione, contatto_id) "
                    "VALUES (?, ?, ?, ?)",
                    (now, "merge_snapshot", snapshot_desc, da_id),
                )
                evento_desc = (
                    f"Merge: '{chiave_da}' → lapide di '{chiave_verso}' "
                    f"(id={canonico_id}). Riempiti: {[c for c, _ in campi_riempiti]}. "
                    f"Conflitti (verso vince): {[(c, v) for c, v, _ in conflitti]}."
                )
                con.execute(
                    "INSERT INTO diario (ts, tipo, descrizione, contatto_id) "
                    "VALUES (?, ?, ?, ?)",
                    (now, "merge_evento", evento_desc, canonico_id),
                )

                # 1) completa anagrafica del canonico dai campi del doppione
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
                return {
                    "canonico_id": canonico_id,
                    "campi_riempiti": campi_riempiti,
                    "conflitti": conflitti,
                    "no_op": False,
                }
        except (sqlite3.Error, OSError) as e:
            log.warning("unisci_contatti_con_snapshot fallita (%s): %s",
                        self.db_path, e)
            return None

    # ---------------------------------------------------------------- letture
    @staticmethod
    def _risolvi_canonico(con: sqlite3.Connection, chiave: str
                          ) -> Optional[Dict[str, Any]]:
        """Risolve una chiave GIÀ normalizzata (confronto su chiave_norm) al record
        CANONICO, seguendo la catena merged_into fino al lead vivo. Bounded da un
        set di id visti (anti-ciclo difensivo, anche se l'invariante tiene la catena
        a 1). Ritorna None se la chiave non esiste."""
        row = con.execute(
            "SELECT * FROM contatti WHERE chiave_norm = ?", (chiave,)
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

    def diario_tutto(self) -> List[Dict[str, Any]]:
        """TUTTE le voci del diario in ordine cronologico (id crescente), in SOLA
        LETTURA. Serve alla RICOSTRUZIONE dell'indice vettoriale (cache derivata,
        modulo vectors.py): legge l'intero diario senza modificarlo, quindi
        l'immutabilità append-only resta INTATTA (nessun UPDATE/DELETE, nessun nuovo
        path di scrittura). [] in degrado. NB: a differenza di diario_recente è
        SENZA LIMIT — pensato per il rebuild batch, non per l'iniezione nel contesto."""
        try:
            with self._connect() as con:
                cur = con.execute("SELECT * FROM diario ORDER BY id ASC")
                return self._rows(cur)
        except (sqlite3.Error, OSError) as e:
            log.warning("diario_tutto fallita (%s): %s", self.db_path, e)
            return []

    def diario_dopo(self, after_id: int, limit: int = 64) -> List[Dict[str, Any]]:
        """Voci del diario con id > after_id, in ordine crescente, fino a `limit`,
        in SOLA LETTURA. È il lettore INCREMENTALE del catch-up indexing vettoriale:
        indicizza solo le righe NUOVE oltre un watermark, senza rileggere tutto il
        diario ad ogni turno. Immutabilità intatta (nessuna scrittura). [] in degrado."""
        try:
            with self._connect() as con:
                cur = con.execute(
                    "SELECT * FROM diario WHERE id > ? ORDER BY id ASC LIMIT ?",
                    (int(after_id), int(limit)),
                )
                return self._rows(cur)
        except (sqlite3.Error, OSError, TypeError, ValueError) as e:
            log.warning("diario_dopo fallita (%s): %s", self.db_path, e)
            return []

    def get_diario(self, diario_id: int) -> Optional[Dict[str, Any]]:
        """Una riga del diario per id (con contatto_id), o None se assente/in degrado.
        SOLA LETTURA. Serve ad arricchire uno snippet di retrieval con lo stato
        CORRENTE del lead collegato (la riga di diario porta il contatto_id)."""
        try:
            with self._connect() as con:
                row = con.execute(
                    "SELECT * FROM diario WHERE id = ?", (int(diario_id),)
                ).fetchone()
                return dict(row) if row else None
        except (sqlite3.Error, OSError, TypeError, ValueError) as e:
            log.warning("get_diario fallita (%s): %s", self.db_path, e)
            return None

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
        """Un contatto per la sua chiave logica (es. email/handle), o None se
        assente/in degrado. Lookup esatto sull'indice UNIQUE `chiave_norm`: è la
        via canonica per risolvere chiave -> contatto. La chiave in input viene
        canonicalizzata (stesso normalizza_chiave dell'upsert) così che il lookup
        risolva alla stessa identità logica con cui è stata scritta, a prescindere
        da maiuscole/spazi/forma Unicode. Se la chiave appartiene a una LAPIDE
        (lead fuso, R-crm-1b), segue il puntatore e ritorna il lead CANONICO: una
        vecchia chiave continua a risolvere al lead vivo dopo un merge."""
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

    # -------------------------------------------------- rilevamento duplicati
    @staticmethod
    def _is_email(valore: Optional[str]) -> bool:
        """Pattern email minimale: almeno un carattere prima di '@', dominio con
        almeno un punto e parte finale non vuota. PURO e FAIL-SAFE: mai solleva."""
        if not valore:
            return False
        s = str(valore).strip()
        at = s.rfind("@")
        if at <= 0:
            return False
        domain = s[at + 1:]
        dot = domain.rfind(".")
        return dot > 0 and bool(domain[dot + 1:].strip())

    @staticmethod
    def _is_phone(valore: Optional[str]) -> bool:
        """Pattern telefono: delegato a normalizza_telefono (non vuoto → valido).
        PURO e FAIL-SAFE: mai solleva."""
        return bool(normalizza_telefono(valore))

    def _append_sospetto(self, tipo: str, descrizione_base: str,
                         id_a: int, id_b: int) -> None:
        """Scrive nel diario una riga di sospetto (tipo: sospetto_duplicato_*)
        SOLO se la coppia non è già segnalata. Tag '[ids:X,Y]' nella descrizione
        permette il check idempotente: LIKE '%[ids:X,Y]%' sulla descrizione. I caratteri
        '[', ']', ',' non sono wildcard in SQLite LIKE → nessun falso positivo.
        FAIL-SAFE (§9): errore nel check → skip + warning. Non solleva mai."""
        lo, hi = min(id_a, id_b), max(id_a, id_b)
        tag = f"[ids:{lo},{hi}]"
        descrizione = f"{descrizione_base} {tag}"
        try:
            with self._connect() as con:
                row = con.execute(
                    "SELECT COUNT(*) FROM diario WHERE tipo = ? AND descrizione LIKE ?",
                    (tipo, f"%{tag}%"),
                ).fetchone()
                if row and int(row[0]) > 0:
                    return  # già nel diario: skip idempotente
                con.execute(
                    "INSERT INTO diario (ts, tipo, descrizione, contatto_id) "
                    "VALUES (?, ?, ?, ?)",
                    (_now_iso(), tipo, descrizione, None),
                )
                con.commit()
        except (sqlite3.Error, OSError) as e:
            log.warning("_append_sospetto: check/write fallito (%s) — skip", e)

    def rileva_duplicati_email(self) -> List[Dict[str, Any]]:
        """SOLA LETTURA sui contatti: trova coppie di schede VIVE che condividono
        la stessa email (confrontando `chiave_norm` e il campo `contatto` di ciascuna,
        normalizzati con normalizza_chiave). Match SOLO su email (pattern '@'+dominio);
        nomi e testo generico non generano segnali. Per ogni coppia trovata scrive
        una riga append-only nel diario (tipo 'sospetto_duplicato_email'), IDEMPOTENTE:
        stesso sospetto già nel diario → nessuna riga aggiuntiva (via _append_sospetto).
        Ritorna la lista delle coppie (dizionari con chiave_a/id_a/chiave_b/id_b/email).
        [] in degrado (§9)."""
        if not self.available:
            return []
        try:
            with self._connect() as con:
                righe = self._rows(con.execute(
                    "SELECT id, chiave, chiave_norm, contatto "
                    "FROM contatti WHERE merged_into IS NULL"
                ))
        except (sqlite3.Error, OSError) as e:
            log.warning("rileva_duplicati_email: lettura contatti fallita (%s): %s",
                        self.db_path, e)
            return []
        # Indice email_norm → {id: {id, chiave}} (dedup per id, ignora sorgente)
        email_idx: Dict[str, Dict[int, Dict[str, Any]]] = {}
        for r in righe:
            for raw in (r.get("chiave_norm"), r.get("contatto")):
                norm = normalizza_chiave(raw)
                if self._is_email(norm):
                    email_idx.setdefault(norm, {})[int(r["id"])] = {
                        "id": int(r["id"]), "chiave": r["chiave"]
                    }
        # Coppie: email con ≥2 contatti distinti
        coppie: List[Dict[str, Any]] = []
        for email, per_id in email_idx.items():
            schede = list(per_id.values())
            if len(schede) < 2:
                continue
            for i in range(len(schede)):
                for j in range(i + 1, len(schede)):
                    a, b = schede[i], schede[j]
                    coppie.append({
                        "chiave_a": a["chiave"], "id_a": a["id"],
                        "chiave_b": b["chiave"], "id_b": b["id"],
                        "email": email,
                    })
                    self._append_sospetto(
                        "sospetto_duplicato_email",
                        f"sospetto duplicato: {a['chiave']!r} ~ {b['chiave']!r}"
                        f" (email {email})",
                        a["id"], b["id"],
                    )
        return coppie

    def rileva_duplicati_telefono(self) -> List[Dict[str, Any]]:
        """SOLA LETTURA sui contatti: trova coppie di schede VIVE che condividono
        lo stesso numero di telefono normalizzato (via normalizza_telefono sul campo
        `chiave_norm` e `contatto`). Match SOLO su valori riconosciuti come telefono
        (9-15 cifre, senza '@'). Per ogni coppia scrive una riga append-only nel
        diario (tipo 'sospetto_duplicato_telefono'), IDEMPOTENTE: stesso sospetto già
        nel diario → nessuna riga aggiuntiva. Ritorna la lista delle coppie (dizionari
        con chiave_a/id_a/chiave_b/id_b/telefono). [] in degrado (§9)."""
        if not self.available:
            return []
        try:
            with self._connect() as con:
                righe = self._rows(con.execute(
                    "SELECT id, chiave, chiave_norm, contatto "
                    "FROM contatti WHERE merged_into IS NULL"
                ))
        except (sqlite3.Error, OSError) as e:
            log.warning("rileva_duplicati_telefono: lettura contatti fallita (%s): %s",
                        self.db_path, e)
            return []
        # Indice tel_norm → {id: {id, chiave}} (dedup per id, ignora sorgente)
        tel_idx: Dict[str, Dict[int, Dict[str, Any]]] = {}
        for r in righe:
            for raw in (r.get("chiave_norm"), r.get("contatto")):
                norm = normalizza_telefono(raw)
                if norm:
                    tel_idx.setdefault(norm, {})[int(r["id"])] = {
                        "id": int(r["id"]), "chiave": r["chiave"]
                    }
        # Coppie: telefono con ≥2 contatti distinti
        coppie: List[Dict[str, Any]] = []
        for tel, per_id in tel_idx.items():
            schede = list(per_id.values())
            if len(schede) < 2:
                continue
            for i in range(len(schede)):
                for j in range(i + 1, len(schede)):
                    a, b = schede[i], schede[j]
                    coppie.append({
                        "chiave_a": a["chiave"], "id_a": a["id"],
                        "chiave_b": b["chiave"], "id_b": b["id"],
                        "telefono": tel,
                    })
                    self._append_sospetto(
                        "sospetto_duplicato_telefono",
                        f"sospetto duplicato: {a['chiave']!r} ~ {b['chiave']!r}"
                        f" (telefono {tel})",
                        a["id"], b["id"],
                    )
        return coppie

    # ------------------------------------------------------------- integrità
    def integrity_check(self) -> Tuple[bool, str]:
        """Verifica l'integrità del DB via `PRAGMA quick_check` (più rapido di
        integrity_check, individua le corruzioni strutturali). Ritorna
        (True, 'ok') se sano, (False, dettaglio) se corrotto o in degrado.
        Mai solleva (§9): è una diagnosi, non deve poter abbattere chi la chiama
        (gas doctor, backup_auto)."""
        try:
            with self._connect() as con:
                row = con.execute("PRAGMA quick_check").fetchone()
            esito = (row[0] if row else "nessun risultato")
            return (esito == "ok", esito)
        except (sqlite3.Error, OSError) as e:
            log.warning("integrity_check fallita (%s): %s", self.db_path, e)
            return (False, f"errore: {e}")

    # ----------------------------------------------------------------- backup
    def _backup_files(self, base: Path) -> List[Path]:
        """Backup esistenti per questo DB, ORDINATI cronologicamente (il timestamp
        nel nome è lessicograficamente ordinabile)."""
        return sorted(base.glob(f"{self.db_path.stem}.*.bak"))

    @staticmethod
    def _backup_retention(files: List[Path], keep: int
                          ) -> Tuple[List[Path], List[Path]]:
        """Politica di rotazione PURA e testabile: dato l'elenco ordinato
        (cronologico) dei backup, ritorna (tieni, scarta) tenendo gli ultimi
        `keep`. keep<=0 → non scarta nulla (rotazione disattivata)."""
        if keep <= 0 or len(files) <= keep:
            return files, []
        return files[-keep:], files[:-keep]

    def ultimo_backup(self, dest_dir: Optional[Union[str, Path]] = None
                      ) -> Optional[Path]:
        """Il backup .bak più recente (per età/diagnosi), o None se non ce ne
        sono / in degrado."""
        try:
            base = Path(dest_dir) if dest_dir is not None else self.db_path.parent
            files = self._backup_files(base)
            return files[-1] if files else None
        except OSError as e:
            log.warning("ultimo_backup fallita (%s): %s", self.db_path, e)
            return None

    def backup(self, dest_dir: Optional[Union[str, Path]] = None,
               keep: Optional[int] = None) -> Optional[Path]:
        """Copia il DB in un file timestampato (banale perché è un file singolo).
        Usa l'API di backup nativa di SQLite per una copia COERENTE anche con
        scritture in volo. Dopo la copia applica la ROTAZIONE (tiene gli ultimi
        `keep`, default DEFAULT_BACKUP_KEEP) per non accumulare .bak all'infinito.
        Ritorna il path della copia, o None in degrado. La copia ha estensione
        .bak (già gitignorata)."""
        try:
            base = Path(dest_dir) if dest_dir is not None else self.db_path.parent
            base.mkdir(parents=True, exist_ok=True)
            # microsecondi nel nome: copie multiple nello stesso secondo non si
            # sovrascrivono (serve per la rotazione e per i backup ravvicinati).
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
            dest = base / f"{self.db_path.stem}.{ts}.bak"
            with self._connect() as src, sqlite3.connect(str(dest)) as dst:
                src.backup(dst)
        except (sqlite3.Error, OSError) as e:
            log.warning("backup fallita (%s): %s", self.db_path, e)
            return None
        # Rotazione best-effort: un suo fallimento NON deve invalidare il backup
        # appena creato (che è il dato che ci interessa salvare).
        try:
            k = DEFAULT_BACKUP_KEEP if keep is None else keep
            _, drop = self._backup_retention(self._backup_files(base), k)
            for f in drop:
                f.unlink(missing_ok=True)
        except OSError as e:
            log.warning("rotazione backup fallita (%s): %s", base, e)
        return dest

    def backup_auto(self, min_interval_sec: int,
                    dest_dir: Optional[Union[str, Path]] = None,
                    keep: Optional[int] = None) -> Optional[Path]:
        """Backup THROTTLED (anti auto-corruzione, §10 FASE 2): crea un backup solo
        se l'ultimo è più vecchio di `min_interval_sec` (o non esiste). PRIMA di
        copiare verifica l'integrità: un DB corrotto NON viene mai copiato sopra i
        backup buoni (così la rotazione non evince le copie sane). Ritorna il path
        del nuovo backup, oppure None se non era ora / DB corrotto / degrado.
        Fail-safe §9: non solleva mai."""
        try:
            last = self.ultimo_backup(dest_dir)
            if last is not None:
                eta = time.time() - last.stat().st_mtime
                if eta < max(0, min_interval_sec):
                    return None  # non ancora ora
            ok, det = self.integrity_check()
            if not ok:
                log.warning("backup_auto saltato: integrità KO su %s (%s)",
                            self.db_path, det)
                return None
            return self.backup(dest_dir, keep=keep)
        except (sqlite3.Error, OSError) as e:
            log.warning("backup_auto fallita (%s): %s", self.db_path, e)
            return None

    def backup_offsite_auto(self, offsite_dir: Union[str, Path],
                            min_interval_sec: int,
                            keep: Optional[int] = None) -> Optional[Path]:
        """Backup THROTTLED off-site (anti-disastro-disco): copia il DB su una
        destinazione ESTERNA configurabile (volume montato / dir sincronizzata).
        Throttle SEPARATO da backup_auto: la dir esterna può essere lenta o remota
        senza interferire con il backup locale. CINTURA D'INTEGRITÀ: verifica la
        SORGENTE prima di copiare (un DB corrotto NON deve avvelenare l'unico
        recupero disponibile sul volume esterno). Riusa backup() (API sqlite nativa,
        mai shutil) e integrity_check() senza reimplementarli. Ritorna il path della
        copia, o None se non era ora / sorgente corrotta / dir non accessibile /
        degrado. Fail-safe §9: non solleva mai."""
        try:
            odir = Path(offsite_dir)
            # Throttle: ricava l'ultimo backup off-site dai file nella dir esterna.
            last = self.ultimo_backup(odir)
            if last is not None:
                eta = time.time() - last.stat().st_mtime
                if eta < max(0, min_interval_sec):
                    return None  # non ancora ora
            # Integrità: mai copiare un DB corrotto sul volume di recupero.
            ok, det = self.integrity_check()
            if not ok:
                log.warning("backup_offsite saltato: integrità KO su %s (%s)",
                            self.db_path, det)
                return None
            return self.backup(odir, keep=keep)
        except (sqlite3.Error, OSError) as e:
            log.warning("backup_offsite_auto fallita (%s -> %s): %s",
                        self.db_path, offsite_dir, e)
            return None
