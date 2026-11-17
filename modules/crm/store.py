"""Persistenza del CRM clienti — tabelle `crm_*` in SQLite.

Dove stanno i dati: di default nello STESSO file della memoria di Gas (`.gas_memory.db`),
così il backup esistente (`gas backup`, copia del file) copre anche i clienti. Le tabelle
hanno tutte il prefisso `crm_` e non toccano quelle della memoria.

Invarianti (incise anche nei test):
  * SOLDI IN CENTESIMI INTERI. Mai float: «1.234,56 €» diventa 123456. Le percentuali
    sono in punti base (1 bp = 0,01 %), sempre interi.
  * REGISTRO MOVIMENTI IMMUTABILE. UPDATE e DELETE su `crm_movimenti` li vieta il DB
    (trigger). Un errore si corregge con uno STORNO: una riga nuova che annulla quella
    sbagliata (`storno_di`); i conti escludono la coppia. La storia non si riscrive.
  * DIARIO DEL CRM IMMUTABILE. `crm_eventi` è solo-inserimento, come il diario di Gas.
  * UNA SOLA PROPOSTA APERTA PER CHIAVE (indice unico parziale): il motore può girare
    mille volte senza creare doppioni.
  * I SOLDI LI SCRIVE L'OPERATORE (o un import/integrazione), MAI un modello: un numero
    inventato farebbe mentire il CRM.

Fail-safe (§9 CLAUDE.md): i metodi di LETTURA non sollevano mai (errore → log + vuoto/None).
I metodi di SCRITTURA sollevano `ErroreCRM` con un messaggio leggibile se l'input è
sbagliato (la dashboard lo mostra all'operatore) e loggano gli errori del DB.
"""
from __future__ import annotations

import logging
import re
import sqlite3
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

log = logging.getLogger(__name__)

DEFAULT_DB_FILENAME = ".gas_memory.db"

MODELLI_COMMISSIONE: Tuple[str, ...] = (
    "percentuale_profitto",       # commissione_bp sul profitto netto del mese
    "percentuale_capitale_annua",  # commissione_bp all'anno sul capitale (1/12 al mese)
    "fisso_mensile",              # commissione_fissa_cents al mese
)
STATI_CLIENTE: Tuple[str, ...] = ("attivo", "in_pausa", "perso")
STATI_POSIZIONE: Tuple[str, ...] = ("attiva", "in_pausa", "chiusa")
TIPI_MOVIMENTO: Tuple[str, ...] = ("deposito", "prelievo", "profitto", "perdita", "commissione")
FONTI_MOVIMENTO: Tuple[str, ...] = ("operatore", "import", "api", "demo")
AUTORI: Tuple[str, ...] = ("operatore", "motore", "sistema", "import", "api", "demo")
TIPI_PROPOSTA: Tuple[str, ...] = ("cross_sell", "aumento_capitale", "referral")
STATI_PROPOSTA: Tuple[str, ...] = (
    "da_approvare", "inviata", "accettata", "rifiutata", "senza_risposta",
    "scartata", "superata",
)
STATI_PROPOSTA_APERTI: frozenset = frozenset({"da_approvare", "inviata"})
# Transizioni ammesse. Terminali: accettata, rifiutata, scartata, superata.
TRANSIZIONI_PROPOSTA: Dict[str, frozenset] = {
    "da_approvare": frozenset({"inviata", "scartata", "superata"}),
    "inviata": frozenset({"accettata", "rifiutata", "senza_risposta", "superata"}),
    "senza_risposta": frozenset({"accettata", "rifiutata"}),
    "accettata": frozenset(),
    "rifiutata": frozenset(),
    "scartata": frozenset(),
    "superata": frozenset(),
}

# Tetti di sanità sui valori (anti-errore di battitura, non limiti di business).
IMPORTO_MAX_CENTS = 10_000_000_000  # 100 milioni di euro
BP_MAX = 100_000                    # 1000 %
TESTO_MAX = 2000
NOME_MAX = 120

# solo cifre ASCII: \d accetterebbe anche cifre di altri alfabeti (V-3 #193, R-803-6)
_RE_DATA = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
_RE_CODICE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,39}$")
_RE_EMAIL = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,255}\.[^@\s]{2,}$")


class ErroreCRM(ValueError):
    """Input non valido o operazione non ammessa: il messaggio è per l'operatore."""


def _sql_in(valori: Iterable[str]) -> str:
    return ", ".join(f"'{v}'" for v in valori)


_SCHEMA: Tuple[str, ...] = (
    f"""
    CREATE TABLE IF NOT EXISTS crm_servizi (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        codice                  TEXT    NOT NULL UNIQUE,
        nome                    TEXT    NOT NULL,
        descrizione             TEXT,
        modello_commissione     TEXT    NOT NULL
                                CHECK (modello_commissione IN ({_sql_in(MODELLI_COMMISSIONE)})),
        commissione_bp          INTEGER NOT NULL DEFAULT 0
                                CHECK (commissione_bp BETWEEN 0 AND {BP_MAX}),
        commissione_fissa_cents INTEGER NOT NULL DEFAULT 0
                                CHECK (commissione_fissa_cents BETWEEN 0 AND {IMPORTO_MAX_CENTS}),
        capitale_minimo_cents   INTEGER NOT NULL DEFAULT 0
                                CHECK (capitale_minimo_cents BETWEEN 0 AND {IMPORTO_MAX_CENTS}),
        -- stima INTERNA del rendimento mensile, usata solo finché non ci sono dati veri
        -- (mai mostrata al cliente, mai una promessa)
        rendimento_stimato_bp   INTEGER NOT NULL DEFAULT 0
                                CHECK (rendimento_stimato_bp BETWEEN 0 AND {BP_MAX}),
        priorita                INTEGER NOT NULL DEFAULT 100,
        attivo                  INTEGER NOT NULL DEFAULT 1 CHECK (attivo IN (0, 1)),
        creato_il               TEXT    NOT NULL,
        aggiornato_il           TEXT    NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS crm_clienti (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        nome                TEXT    NOT NULL,
        telefono            TEXT,
        email               TEXT,
        stato               TEXT    NOT NULL DEFAULT 'attivo'
                            CHECK (stato IN ({_sql_in(STATI_CLIENTE)})),
        consenso_marketing  INTEGER NOT NULL DEFAULT 0 CHECK (consenso_marketing IN (0, 1)),
        consenso_il         TEXT,
        opt_out             INTEGER NOT NULL DEFAULT 0 CHECK (opt_out IN (0, 1)),
        opt_out_il          TEXT,
        presentato_da       INTEGER REFERENCES crm_clienti(id),
        -- id della scheda nella rubrica lead di Gas (tabella contatti), se viene da lì.
        -- Niente FOREIGN KEY: il CRM deve funzionare anche in un file senza la memoria.
        contatto_id         INTEGER,
        note                TEXT,
        creato_il           TEXT    NOT NULL,
        aggiornato_il       TEXT    NOT NULL
    )
    """,
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_crm_clienti_tel ON crm_clienti(telefono) "
    "WHERE telefono IS NOT NULL",
    # R-803-5: un lead della rubrica diventa cliente una volta sola (anche in concorrenza)
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_crm_clienti_lead ON crm_clienti(contatto_id) "
    "WHERE contatto_id IS NOT NULL",
    f"""
    CREATE TABLE IF NOT EXISTS crm_posizioni (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id      INTEGER NOT NULL REFERENCES crm_clienti(id),
        servizio_id     INTEGER NOT NULL REFERENCES crm_servizi(id),
        stato           TEXT    NOT NULL DEFAULT 'attiva'
                        CHECK (stato IN ({_sql_in(STATI_POSIZIONE)})),
        aperta_il       TEXT    NOT NULL,
        chiusa_il       TEXT,
        creato_il       TEXT    NOT NULL,
        aggiornato_il   TEXT    NOT NULL,
        UNIQUE (cliente_id, servizio_id)
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS crm_movimenti (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        posizione_id    INTEGER NOT NULL REFERENCES crm_posizioni(id),
        tipo            TEXT    NOT NULL CHECK (tipo IN ({_sql_in(TIPI_MOVIMENTO)})),
        importo_cents   INTEGER NOT NULL
                        CHECK (importo_cents > 0 AND importo_cents <= {IMPORTO_MAX_CENTS}),
        data            TEXT    NOT NULL,
        fonte           TEXT    NOT NULL CHECK (fonte IN ({_sql_in(FONTI_MOVIMENTO)})),
        nota            TEXT,
        storno_di       INTEGER REFERENCES crm_movimenti(id),
        registrato_il   TEXT    NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_crm_mov_pos ON crm_movimenti(posizione_id)",
    "CREATE INDEX IF NOT EXISTS idx_crm_mov_data ON crm_movimenti(data)",
    # un movimento si storna una volta sola
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_crm_mov_storno ON crm_movimenti(storno_di) "
    "WHERE storno_di IS NOT NULL",
    """
    CREATE TRIGGER IF NOT EXISTS crm_movimenti_no_update
    BEFORE UPDATE ON crm_movimenti
    BEGIN
        SELECT RAISE(ABORT, 'registro movimenti immutabile: UPDATE vietato (usa uno storno)');
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS crm_movimenti_no_delete
    BEFORE DELETE ON crm_movimenti
    BEGIN
        SELECT RAISE(ABORT, 'registro movimenti immutabile: DELETE vietato (usa uno storno)');
    END
    """,
    f"""
    CREATE TABLE IF NOT EXISTS crm_proposte (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id              INTEGER NOT NULL REFERENCES crm_clienti(id),
        tipo                    TEXT    NOT NULL CHECK (tipo IN ({_sql_in(TIPI_PROPOSTA)})),
        servizio_id             INTEGER REFERENCES crm_servizi(id),
        posizione_id            INTEGER REFERENCES crm_posizioni(id),
        stato                   TEXT    NOT NULL DEFAULT 'da_approvare'
                                CHECK (stato IN ({_sql_in(STATI_PROPOSTA)})),
        livello                 INTEGER NOT NULL DEFAULT 1 CHECK (livello BETWEEN 1 AND 3),
        motivo                  TEXT    NOT NULL,
        messaggio               TEXT    NOT NULL,
        valore_stimato_cents    INTEGER NOT NULL DEFAULT 0 CHECK (valore_stimato_cents >= 0),
        chiave                  TEXT    NOT NULL,
        canale                  TEXT,
        creata_il               TEXT    NOT NULL,
        aggiornata_il           TEXT    NOT NULL,
        inviata_il              TEXT,
        esito_il                TEXT
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_crm_prop_cliente ON crm_proposte(cliente_id)",
    # anti-doppione: al massimo una proposta APERTA per chiave (tipo:cliente:obiettivo)
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_crm_prop_aperta ON crm_proposte(chiave) "
    "WHERE stato IN ('da_approvare', 'inviata')",
    f"""
    CREATE TABLE IF NOT EXISTS crm_eventi (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        ts          TEXT    NOT NULL,
        cliente_id  INTEGER REFERENCES crm_clienti(id),
        tipo        TEXT    NOT NULL,
        descrizione TEXT    NOT NULL,
        autore      TEXT    NOT NULL CHECK (autore IN ({_sql_in(AUTORI)}))
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_crm_eventi_cliente ON crm_eventi(cliente_id)",
    """
    CREATE TRIGGER IF NOT EXISTS crm_eventi_no_update
    BEFORE UPDATE ON crm_eventi
    BEGIN
        SELECT RAISE(ABORT, 'diario CRM immutabile: UPDATE vietato');
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS crm_eventi_no_delete
    BEFORE DELETE ON crm_eventi
    BEGIN
        SELECT RAISE(ABORT, 'diario CRM immutabile: DELETE vietato');
    END
    """,
)


# ---------------------------------------------------------------------- utilità pure
def adesso_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def oggi_iso() -> str:
    return date.today().isoformat()


def valida_data(valore: Any, campo: str = "data") -> str:
    """Data «AAAA-MM-GG» reale (niente 31 febbraio). Solleva ErroreCRM."""
    if not isinstance(valore, str) or not _RE_DATA.match(valore.strip()):
        raise ErroreCRM(f"{campo}: serve una data nel formato AAAA-MM-GG")
    v = valore.strip()
    try:
        date.fromisoformat(v)
    except ValueError:
        raise ErroreCRM(f"{campo}: data inesistente ({v})") from None
    return v


def parse_importo(valore: Any) -> int:
    """Importo in euro scritto da una persona → centesimi interi, senza float.

    Accetta «1234», «1234,5», «1.234,56», «1234.56», «1,234.56», «€ 1.234», interi
    Python (euro interi). Regola dei separatori: se compaiono sia «.» sia «,», l'ultimo
    è quello dei decimali; con la sola virgola è decimale; col solo punto è separatore
    delle migliaia se il numero ha la forma «1.234» / «1.234.567», altrimenti decimale.
    Al massimo 2 decimali; niente negativi (il segno lo dà il tipo di movimento); niente
    zero. Solleva ErroreCRM."""
    if isinstance(valore, bool):
        raise ErroreCRM("importo non valido")
    if isinstance(valore, int):
        testo = str(valore)
    elif isinstance(valore, str):
        testo = valore
    else:
        raise ErroreCRM("importo: scrivilo come testo, es. 1.234,56")
    t = testo.strip().replace("€", "").replace(" ", "").replace(" ", "").replace("'", "")
    if not t or len(t) > 24:
        raise ErroreCRM("importo mancante")
    if t.startswith(("-", "+")):
        raise ErroreCRM("importo: niente segno, il verso lo dice il tipo di movimento")
    if not re.fullmatch(r"[0-9.,]+", t):
        raise ErroreCRM(f"importo non valido: {testo!r}")
    if "." in t and "," in t:
        dec = "." if t.rfind(".") > t.rfind(",") else ","
        mig = "," if dec == "." else "."
        intero, _, frazione = t.rpartition(dec)
        # R-803-7: le migliaia non iniziano con 0 («0.500,25» è un errore, non 500 €)
        if dec in intero or not re.fullmatch(r"[1-9][0-9]{0,2}(" + re.escape(mig) + r"[0-9]{3})+", intero):
            raise ErroreCRM(f"importo non valido: {testo!r}")
        intero = intero.replace(mig, "")
    elif "," in t:
        if t.count(",") > 1:
            raise ErroreCRM(f"importo non valido: {testo!r}")
        intero, _, frazione = t.partition(",")
    elif "." in t:
        # R-803-7: «0.500» non è cinquecento euro; col primo gruppo 0 resta un decimale
        if re.fullmatch(r"[1-9][0-9]{0,2}(\.[0-9]{3})+", t):
            intero, frazione = t.replace(".", ""), ""
        elif t.count(".") == 1:
            intero, _, frazione = t.partition(".")
        else:
            raise ErroreCRM(f"importo non valido: {testo!r}")
    else:
        intero, frazione = t, ""
    if not intero:
        intero = "0"
    if not re.fullmatch(r"[0-9]+", intero) or (frazione and not re.fullmatch(r"[0-9]+", frazione)):
        raise ErroreCRM(f"importo non valido: {testo!r}")
    if len(frazione) > 2:
        raise ErroreCRM("importo: al massimo 2 decimali (centesimi)")
    try:
        cents = int(Decimal(intero) * 100 + Decimal(frazione.ljust(2, "0") or "0"))
    except InvalidOperation:
        raise ErroreCRM(f"importo non valido: {testo!r}") from None
    if cents <= 0:
        raise ErroreCRM("importo: deve essere maggiore di zero")
    if cents > IMPORTO_MAX_CENTS:
        raise ErroreCRM("importo troppo grande: controlla le cifre")
    return cents


def parse_percentuale_bp(valore: Any) -> int:
    """«20», «20%», «2,5», «0.75» → punti base interi (20 % = 2000 bp). Solleva ErroreCRM."""
    if isinstance(valore, bool):
        raise ErroreCRM("percentuale non valida")
    if isinstance(valore, int):
        t = str(valore)
    elif isinstance(valore, str):
        t = valore.strip().replace("%", "").replace(" ", "").replace(",", ".")
    else:
        raise ErroreCRM("percentuale: scrivila come testo, es. 20 o 2,5")
    if t == "":
        return 0
    if not re.fullmatch(r"[0-9]{1,4}(\.[0-9]{1,2})?", t):
        raise ErroreCRM(f"percentuale non valida: {valore!r} (al massimo 2 decimali)")
    bp = int(Decimal(t) * 100)
    if bp > BP_MAX:
        raise ErroreCRM("percentuale troppo grande")
    return bp


def formatta_euro(cents: int, segno: bool = False) -> str:
    """123456 → «1.234,56 €» (stile italiano). Con segno=True: «+1.234,56 €»."""
    neg = cents < 0
    a = abs(int(cents))
    intero, dec = divmod(a, 100)
    gruppi = f"{intero:,}".replace(",", ".")
    s = f"{gruppi},{dec:02d} €"
    if neg:
        return "−" + s
    return ("+" + s) if (segno and a > 0) else s


def formatta_euro_tondo(cents: int) -> str:
    """Euro senza decimali, arrotondati a metà verso l'alto: 123456 → «1.235 €»."""
    neg = cents < 0
    a = (abs(int(cents)) + 50) // 100
    s = f"{a:,}".replace(",", ".") + " €"
    return ("−" + s) if neg and a else s


def normalizza_telefono(valore: Optional[str], prefisso_default: str = "+39") -> Optional[str]:
    """Numero in formato internazionale «+393331234567», o None se vuoto.

    Toglie spazi, trattini, punti, parentesi; «0039…» diventa «+39…»; un numero senza
    prefisso prende `prefisso_default` (Italia). Da 8 a 15 cifre (E.164). Solleva
    ErroreCRM se non è un numero."""
    if valore is None:
        return None
    t = str(valore).strip()
    if not t:
        return None
    t = re.sub(r"[\s\-./()]", "", t)
    if t.startswith("00"):
        t = "+" + t[2:]
    if not t.startswith("+"):
        if not re.fullmatch(r"[0-9]+", t):
            raise ErroreCRM("telefono non valido")
        t = prefisso_default + t
    cifre = t[1:]
    # solo cifre ASCII (R-803-6): «³³³» o cifre arabe sfuggirebbero all'indice unico
    if not re.fullmatch(r"[0-9]{8,15}", cifre):
        raise ErroreCRM("telefono non valido: servono da 8 a 15 cifre col prefisso")
    if cifre[0] == "0":
        raise ErroreCRM("telefono non valido: il prefisso internazionale non inizia con 0")
    return "+" + cifre


def _testo(valore: Any, campo: str, massimo: int = TESTO_MAX,
           obbligatorio: bool = False) -> Optional[str]:
    if valore is None:
        if obbligatorio:
            raise ErroreCRM(f"{campo}: obbligatorio")
        return None
    if not isinstance(valore, str):
        raise ErroreCRM(f"{campo}: deve essere testo")
    v = valore.strip()
    if not v:
        if obbligatorio:
            raise ErroreCRM(f"{campo}: obbligatorio")
        return None
    if len(v) > massimo:
        raise ErroreCRM(f"{campo}: troppo lungo (max {massimo} caratteri)")
    # niente caratteri di controllo (tranne a capo e tab) nei testi salvati
    if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", v):
        raise ErroreCRM(f"{campo}: contiene caratteri non ammessi")
    return v


def _bool01(valore: Any, campo: str) -> int:
    if isinstance(valore, bool):
        return int(valore)
    if valore in (0, 1):
        return int(valore)
    raise ErroreCRM(f"{campo}: deve essere vero o falso")


def _intero(valore: Any, campo: str, minimo: int = 0, massimo: int = IMPORTO_MAX_CENTS) -> int:
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise ErroreCRM(f"{campo}: deve essere un numero intero")
    if not minimo <= valore <= massimo:
        raise ErroreCRM(f"{campo}: fuori dai limiti ({minimo}…{massimo})")
    return valore


# ---------------------------------------------------------------------- store
class CRMStore:
    """Accesso al CRM. Una connessione per operazione (thread-safe per costruzione:
    il server della dashboard serve più richieste insieme)."""

    def __init__(self, db_path: Union[str, Path],
                 orologio: Optional[Callable[[], datetime]] = None) -> None:
        self.db_path = Path(db_path)
        # orologio iniettabile: i test fissano «adesso» e provano pause e scadenze
        self._orologio: Callable[[], datetime] = orologio or (lambda: datetime.now().astimezone())
        self.available = False
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            with self._connect() as con:
                for ddl in _SCHEMA:
                    con.execute(ddl)
                con.commit()
            self.available = True
        except (sqlite3.Error, OSError) as e:
            log.warning("CRM: init fallita su %s (%s) — degrado", self.db_path, e)

    def _connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(str(self.db_path), timeout=10)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    @staticmethod
    def _rows(cur: sqlite3.Cursor) -> List[Dict[str, Any]]:
        return [dict(r) for r in cur.fetchall()]

    def _leggi(self, sql: str, args: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
        """Lettura che non solleva mai: errore → log + []."""
        try:
            with self._connect() as con:
                return self._rows(con.execute(sql, args))
        except (sqlite3.Error, OSError) as e:
            log.warning("CRM: lettura fallita (%s): %s", self.db_path, e)
            return []

    def _ts(self) -> str:
        return self._orologio().isoformat(timespec="seconds")

    def _oggi(self) -> str:
        return self._orologio().date().isoformat()

    def oggi(self) -> date:
        """Il giorno di oggi secondo l'orologio dello store (quello vero, o quello dei test)."""
        return self._orologio().date()

    def _evento(self, con: sqlite3.Connection, cliente_id: Optional[int], tipo: str,
                descrizione: str, autore: str) -> None:
        if autore not in AUTORI:
            raise ErroreCRM(f"autore non valido: {autore!r}")
        con.execute(
            "INSERT INTO crm_eventi (ts, cliente_id, tipo, descrizione, autore) "
            "VALUES (?, ?, ?, ?, ?)",
            (self._ts(), cliente_id, tipo, descrizione[:TESTO_MAX], autore),
        )

    def _scrivi(self, fn: Any) -> Any:
        """Esegue `fn(con)` in una transazione; traduce gli errori del DB in ErroreCRM.

        R-806-1: la transazione si apre SUBITO con `BEGIN IMMEDIATE` (lucchetto di
        scrittura preso prima dei controlli). Il sqlite3 di Python, da solo, la aprirebbe
        solo alla prima INSERT/UPDATE: i controlli fatti prima (capitale, STOP, consenso)
        girerebbero fuori e una scrittura concorrente potrebbe infilarsi in mezzo. Chi
        scrive nello stesso momento aspetta (timeout della connessione) e poi vede i dati
        aggiornati."""
        try:
            with self._connect() as con:
                con.execute("BEGIN IMMEDIATE")
                out = fn(con)
                con.commit()
                return out
        except ErroreCRM:
            raise
        except sqlite3.IntegrityError as e:
            log.warning("CRM: vincolo violato (%s): %s", self.db_path, e)
            raise ErroreCRM(_spiega_integrity(str(e))) from None
        except (sqlite3.Error, OSError) as e:
            log.warning("CRM: scrittura fallita (%s): %s", self.db_path, e)
            raise ErroreCRM("database non disponibile: riprova tra poco") from None

    # ------------------------------------------------------------------ servizi
    def aggiungi_servizio(self, codice: str, nome: str, modello_commissione: str,
                          commissione_bp: int = 0, commissione_fissa_cents: int = 0,
                          capitale_minimo_cents: int = 0, rendimento_stimato_bp: int = 0,
                          priorita: int = 100, descrizione: Optional[str] = None,
                          autore: str = "operatore") -> int:
        cod = _testo(codice, "codice", 40, obbligatorio=True)
        assert cod is not None
        cod = cod.lower()
        if not _RE_CODICE.match(cod):
            raise ErroreCRM("codice: solo lettere minuscole, cifre, - e _ (es. copy-oro)")
        nom = _testo(nome, "nome", NOME_MAX, obbligatorio=True)
        if modello_commissione not in MODELLI_COMMISSIONE:
            raise ErroreCRM(f"modello di commissione non valido (ammessi: {', '.join(MODELLI_COMMISSIONE)})")
        valori = (
            _intero(commissione_bp, "commissione_bp", 0, BP_MAX),
            _intero(commissione_fissa_cents, "commissione_fissa_cents"),
            _intero(capitale_minimo_cents, "capitale_minimo_cents"),
            _intero(rendimento_stimato_bp, "rendimento_stimato_bp", 0, BP_MAX),
            _intero(priorita, "priorita", 0, 10_000),
        )
        desc = _testo(descrizione, "descrizione")
        ora = self._ts()

        def _fn(con: sqlite3.Connection) -> int:
            cur = con.execute(
                "INSERT INTO crm_servizi (codice, nome, descrizione, modello_commissione, "
                "commissione_bp, commissione_fissa_cents, capitale_minimo_cents, "
                "rendimento_stimato_bp, priorita, attivo, creato_il, aggiornato_il) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)",
                (cod, nom, desc, modello_commissione, *valori, ora, ora),
            )
            self._evento(con, None, "servizio", f"Nuovo servizio: {nom}", autore)
            return _nuovo_id(cur)
        return self._scrivi(_fn)

    _CAMPI_SERVIZIO = ("nome", "descrizione", "modello_commissione", "commissione_bp",
                       "commissione_fissa_cents", "capitale_minimo_cents",
                       "rendimento_stimato_bp", "priorita", "attivo")

    def aggiorna_servizio(self, servizio_id: int, autore: str = "operatore",
                          **campi: Any) -> None:
        sid = _intero(servizio_id, "servizio_id", 1, 2**62)
        sets: List[str] = []
        args: List[Any] = []
        for k, v in campi.items():
            if k not in self._CAMPI_SERVIZIO:
                raise ErroreCRM(f"campo non modificabile: {k}")
            if k == "nome":
                v = _testo(v, "nome", NOME_MAX, obbligatorio=True)
            elif k == "descrizione":
                v = _testo(v, "descrizione")
            elif k == "modello_commissione":
                if v not in MODELLI_COMMISSIONE:
                    raise ErroreCRM("modello di commissione non valido")
            elif k == "attivo":
                v = _bool01(v, "attivo")
            elif k in ("commissione_bp", "rendimento_stimato_bp"):
                v = _intero(v, k, 0, BP_MAX)
            elif k == "priorita":
                v = _intero(v, k, 0, 10_000)
            else:
                v = _intero(v, k)
            sets.append(f"{k} = ?")
            args.append(v)
        if not sets:
            return

        def _fn(con: sqlite3.Connection) -> None:
            cur = con.execute(
                f"UPDATE crm_servizi SET {', '.join(sets)}, aggiornato_il = ? WHERE id = ?",
                (*args, self._ts(), sid),
            )
            if cur.rowcount != 1:
                raise ErroreCRM("servizio inesistente")
            self._evento(con, None, "servizio",
                         f"Servizio #{sid} aggiornato ({', '.join(campi)})", autore)
        self._scrivi(_fn)

    def servizi(self, solo_attivi: bool = False) -> List[Dict[str, Any]]:
        dove = "WHERE attivo = 1 " if solo_attivi else ""
        return self._leggi(f"SELECT * FROM crm_servizi {dove}ORDER BY priorita, id")

    # ------------------------------------------------------------------ clienti
    def aggiungi_cliente(self, nome: str, telefono: Optional[str] = None,
                         email: Optional[str] = None, consenso_marketing: bool = False,
                         presentato_da: Optional[int] = None,
                         contatto_id: Optional[int] = None, note: Optional[str] = None,
                         autore: str = "operatore") -> int:
        nom = _testo(nome, "nome", NOME_MAX, obbligatorio=True)
        tel = normalizza_telefono(telefono)
        mail = _testo(email, "email", 320)
        if mail is not None and not _RE_EMAIL.match(mail):
            raise ErroreCRM("email non valida")
        cons = _bool01(consenso_marketing, "consenso_marketing")
        nota = _testo(note, "note")
        pres = None if presentato_da is None else _intero(presentato_da, "presentato_da", 1, 2**62)
        cid = None if contatto_id is None else _intero(contatto_id, "contatto_id", 1, 2**62)
        ora = self._ts()

        def _fn(con: sqlite3.Connection) -> int:
            cur = con.execute(
                "INSERT INTO crm_clienti (nome, telefono, email, stato, consenso_marketing, "
                "consenso_il, opt_out, presentato_da, contatto_id, note, creato_il, aggiornato_il) "
                "VALUES (?, ?, ?, 'attivo', ?, ?, 0, ?, ?, ?, ?, ?)",
                (nom, tel, mail, cons, ora if cons else None, pres, cid, nota, ora, ora),
            )
            nuovo = _nuovo_id(cur)
            # R-803-9: il diario del CRM è immutabile, quindi niente nomi né recapiti nel
            # testo: basta l'id (la dashboard mostra il nome leggendo l'anagrafica, che si
            # può anonimizzare su richiesta dell'interessato)
            self._evento(con, nuovo, "cliente", f"Nuovo cliente #{nuovo}", autore)
            if pres is not None:
                self._evento(con, pres, "referral",
                             f"Ha presentato il nuovo cliente #{nuovo}", autore)
            return nuovo
        return self._scrivi(_fn)

    def aggiorna_cliente(self, cliente_id: int, autore: str = "operatore",
                         **campi: Any) -> None:
        """Aggiorna anagrafica e permessi. Consenso e «STOP» hanno la loro data e finiscono
        nel diario del CRM: sono la prova di cosa si poteva fare e quando."""
        cid = _intero(cliente_id, "cliente_id", 1, 2**62)
        sets: List[str] = []
        args: List[Any] = []
        note_diario: List[str] = []
        ora = self._ts()
        for k, v in campi.items():
            if k == "nome":
                v = _testo(v, "nome", NOME_MAX, obbligatorio=True)
            elif k == "telefono":
                v = normalizza_telefono(v)
            elif k == "email":
                v = _testo(v, "email", 320)
                if v is not None and not _RE_EMAIL.match(v):
                    raise ErroreCRM("email non valida")
            elif k == "note":
                v = _testo(v, "note")
            elif k == "stato":
                if v not in STATI_CLIENTE:
                    raise ErroreCRM(f"stato non valido (ammessi: {', '.join(STATI_CLIENTE)})")
                note_diario.append(f"stato → {v}")
            elif k == "consenso_marketing":
                v = _bool01(v, k)
                sets.append("consenso_il = ?")
                args.append(ora if v else None)
                note_diario.append("consenso marketing " + ("DATO" if v else "TOLTO"))
            elif k == "opt_out":
                v = _bool01(v, k)
                sets.append("opt_out_il = ?")
                args.append(ora if v else None)
                note_diario.append("STOP ai messaggi" if v else "STOP revocato dal cliente")
            elif k == "presentato_da":
                v = None if v is None else _intero(v, k, 1, 2**62)
                if v == cid:
                    raise ErroreCRM("un cliente non può presentare se stesso")
            else:
                raise ErroreCRM(f"campo non modificabile: {k}")
            sets.append(f"{k} = ?")
            args.append(v)
        if not sets:
            return

        def _fn(con: sqlite3.Connection) -> None:
            cur = con.execute(
                f"UPDATE crm_clienti SET {', '.join(sets)}, aggiornato_il = ? WHERE id = ?",
                (*args, ora, cid),
            )
            if cur.rowcount != 1:
                raise ErroreCRM("cliente inesistente")
            desc = "; ".join(note_diario) or f"anagrafica aggiornata ({', '.join(campi)})"
            self._evento(con, cid, "cliente", desc, autore)
        self._scrivi(_fn)

    def cliente(self, cliente_id: int) -> Optional[Dict[str, Any]]:
        righe = self._leggi("SELECT * FROM crm_clienti WHERE id = ?", (cliente_id,))
        return righe[0] if righe else None

    def clienti(self) -> List[Dict[str, Any]]:
        return self._leggi("SELECT * FROM crm_clienti ORDER BY nome COLLATE NOCASE, id")

    # ------------------------------------------------------------------ posizioni
    def apri_posizione(self, cliente_id: int, servizio_id: int, data: Optional[str] = None,
                       autore: str = "operatore") -> int:
        """Mette il cliente in un servizio (o lo riattiva se c'era già stato)."""
        cid = _intero(cliente_id, "cliente_id", 1, 2**62)
        sid = _intero(servizio_id, "servizio_id", 1, 2**62)
        giorno = valida_data(data or self._oggi(), "data di apertura")
        ora = self._ts()

        def _fn(con: sqlite3.Connection) -> int:
            srv = con.execute("SELECT nome FROM crm_servizi WHERE id = ?", (sid,)).fetchone()
            cli = con.execute("SELECT id FROM crm_clienti WHERE id = ?", (cid,)).fetchone()
            if srv is None or cli is None:
                raise ErroreCRM("cliente o servizio inesistente")
            esiste = con.execute(
                "SELECT id, stato FROM crm_posizioni WHERE cliente_id = ? AND servizio_id = ?",
                (cid, sid),
            ).fetchone()
            if esiste is not None:
                if esiste["stato"] == "attiva":
                    raise ErroreCRM("il cliente è già in questo servizio")
                con.execute(
                    "UPDATE crm_posizioni SET stato = 'attiva', chiusa_il = NULL, "
                    "aggiornato_il = ? WHERE id = ?", (ora, esiste["id"]),
                )
                self._evento(con, cid, "servizio", f"Riattivato nel servizio {srv['nome']}", autore)
                return int(esiste["id"])
            cur = con.execute(
                "INSERT INTO crm_posizioni (cliente_id, servizio_id, stato, aperta_il, "
                "creato_il, aggiornato_il) VALUES (?, ?, 'attiva', ?, ?, ?)",
                (cid, sid, giorno, ora, ora),
            )
            self._evento(con, cid, "servizio", f"Entrato nel servizio {srv['nome']}", autore)
            return _nuovo_id(cur)
        return self._scrivi(_fn)

    def cambia_stato_posizione(self, posizione_id: int, stato: str,
                               data: Optional[str] = None, autore: str = "operatore") -> None:
        pid = _intero(posizione_id, "posizione_id", 1, 2**62)
        if stato not in STATI_POSIZIONE:
            raise ErroreCRM(f"stato non valido (ammessi: {', '.join(STATI_POSIZIONE)})")
        giorno = valida_data(data or self._oggi())
        ora = self._ts()

        def _fn(con: sqlite3.Connection) -> None:
            r = con.execute(
                "SELECT p.cliente_id, s.nome FROM crm_posizioni p "
                "JOIN crm_servizi s ON s.id = p.servizio_id WHERE p.id = ?", (pid,),
            ).fetchone()
            if r is None:
                raise ErroreCRM("posizione inesistente")
            con.execute(
                "UPDATE crm_posizioni SET stato = ?, chiusa_il = ?, aggiornato_il = ? WHERE id = ?",
                (stato, giorno if stato == "chiusa" else None, ora, pid),
            )
            self._evento(con, r["cliente_id"], "servizio", f"{r['nome']}: posizione {stato}", autore)
        self._scrivi(_fn)

    def anticipa_apertura(self, posizione_id: int, data: str, autore: str = "operatore") -> None:
        """Sposta INDIETRO la data di apertura di una posizione (R-806-2): serve quando il
        servizio è stato aperto con la data sbagliata e lo storico, più vecchio, verrebbe
        rifiutato. Solo indietro: i movimenti già registrati restano tutti dopo l'apertura."""
        pid = _intero(posizione_id, "posizione_id", 1, 2**62)
        giorno = valida_data(data, "data di apertura")
        if giorno > self._oggi():
            raise ErroreCRM("data di apertura nel futuro")

        def _fn(con: sqlite3.Connection) -> None:
            r = con.execute(
                "SELECT p.cliente_id, p.aperta_il, s.nome FROM crm_posizioni p "
                "JOIN crm_servizi s ON s.id = p.servizio_id WHERE p.id = ?", (pid,),
            ).fetchone()
            if r is None:
                raise ErroreCRM("posizione inesistente")
            if giorno > str(r["aperta_il"]):
                raise ErroreCRM("la data di apertura si sposta solo indietro "
                                f"(oggi è {r['aperta_il']})")
            con.execute("UPDATE crm_posizioni SET aperta_il = ?, aggiornato_il = ? WHERE id = ?",
                        (giorno, self._ts(), pid))
            self._evento(con, r["cliente_id"], "servizio",
                         f"{r['nome']}: apertura anticipata dal {r['aperta_il']} al {giorno}", autore)
        self._scrivi(_fn)

    def posizioni(self, cliente_id: Optional[int] = None) -> List[Dict[str, Any]]:
        if cliente_id is None:
            return self._leggi("SELECT * FROM crm_posizioni ORDER BY id")
        return self._leggi("SELECT * FROM crm_posizioni WHERE cliente_id = ? ORDER BY id",
                           (cliente_id,))

    # ------------------------------------------------------------------ movimenti
    def valida_movimento(self, posizione_id: int, tipo: str, importo_cents: int,
                         data: Optional[str] = None, fonte: str = "operatore",
                         nota: Optional[str] = None
                         ) -> Tuple[int, str, int, str, str, Optional[str]]:
        """Controlli di un movimento SENZA scrivere (li usa anche l'import, R-803-3).
        Ritorna i valori normalizzati; solleva ErroreCRM."""
        pid = _intero(posizione_id, "posizione_id", 1, 2**62)
        if tipo not in TIPI_MOVIMENTO:
            raise ErroreCRM(f"tipo di movimento non valido (ammessi: {', '.join(TIPI_MOVIMENTO)})")
        imp = _intero(importo_cents, "importo", 1, IMPORTO_MAX_CENTS)
        if fonte not in FONTI_MOVIMENTO:
            raise ErroreCRM("fonte non valida")
        giorno = valida_data(data or self._oggi())
        if giorno > self._oggi():
            raise ErroreCRM("data nel futuro: i movimenti si registrano a cose fatte")
        return pid, tipo, imp, giorno, fonte, _testo(nota, "nota", 500)

    def _inserisci_movimento(self, con: sqlite3.Connection,
                             valori: Tuple[int, str, int, str, str, Optional[str]]) -> int:
        pid, tipo, imp, giorno, fonte, testo_nota = valori
        r = con.execute(
            "SELECT p.cliente_id, p.aperta_il, s.nome FROM crm_posizioni p "
            "JOIN crm_servizi s ON s.id = p.servizio_id WHERE p.id = ?", (pid,),
        ).fetchone()
        if r is None:
            raise ErroreCRM("posizione inesistente")
        # V-2 verifica esterna #381: il registro non si corregge, quindi niente movimenti
        # incoerenti (prima dell'apertura del servizio, o prelievi oltre il capitale)
        if giorno < str(r["aperta_il"]):
            raise ErroreCRM(f"data {giorno} prima dell'apertura del servizio ({r['aperta_il']})")
        if tipo == "prelievo":
            capitale = self._capitale(con, pid)
            if imp > capitale:
                raise ErroreCRM(f"prelievo di {formatta_euro(imp)} maggiore del capitale "
                                f"({formatta_euro(capitale)})")
        cur = con.execute(
            "INSERT INTO crm_movimenti (posizione_id, tipo, importo_cents, data, fonte, "
            "nota, storno_di, registrato_il) VALUES (?, ?, ?, ?, ?, ?, NULL, ?)",
            (pid, tipo, imp, giorno, fonte, testo_nota, self._ts()),
        )
        autore = fonte if fonte in AUTORI else "operatore"
        self._evento(con, r["cliente_id"], "movimento",
                     f"{r['nome']}: {tipo} {formatta_euro(imp)} ({giorno})", autore)
        return _nuovo_id(cur)

    @staticmethod
    def _capitale(con: sqlite3.Connection, posizione_id: int) -> int:
        """Capitale di una posizione: depositi − prelievi validi. Chiamato dentro `_scrivi`,
        cioè col lucchetto di scrittura già preso (R-806-1)."""
        r = con.execute(
            "SELECT COALESCE(SUM(CASE m.tipo WHEN 'deposito' THEN m.importo_cents "
            "WHEN 'prelievo' THEN -m.importo_cents ELSE 0 END), 0) FROM crm_movimenti m "
            "WHERE m.posizione_id = ? AND m.storno_di IS NULL "
            "AND NOT EXISTS (SELECT 1 FROM crm_movimenti s WHERE s.storno_di = m.id)",
            (posizione_id,),
        ).fetchone()
        return int(r[0])

    def registra_movimento(self, posizione_id: int, tipo: str, importo_cents: int,
                           data: Optional[str] = None, fonte: str = "operatore",
                           nota: Optional[str] = None) -> int:
        valori = self.valida_movimento(posizione_id, tipo, importo_cents, data, fonte, nota)
        return self._scrivi(lambda con: self._inserisci_movimento(con, valori))

    def registra_movimenti(self, righe: List[Tuple[int, str, int, Optional[str], Optional[str]]],
                           fonte: str = "import") -> List[int]:
        """Più movimenti TUTTI O NESSUNO (R-803-3): prima si controllano tutte le righe,
        poi si scrivono in una sola transazione. Righe: (posizione_id, tipo, importo_cents,
        data, nota). Solleva ErroreCRM con l'elenco delle righe sbagliate («riga N: …»)."""
        if not righe:
            return []
        valide = []
        errori: List[str] = []
        for i, (pid, tipo, cents, data, nota) in enumerate(righe, start=1):
            try:
                valide.append(self.valida_movimento(pid, tipo, cents, data, fonte, nota))
            except ErroreCRM as e:
                errori.append(f"riga {i}: {e}")
        if errori:
            raise ErroreCRM("; ".join(errori[:20]) + (" …" if len(errori) > 20 else ""))

        def _fn(con: sqlite3.Connection) -> List[int]:
            ids = []
            for i, v in enumerate(valide, start=1):
                try:
                    ids.append(self._inserisci_movimento(con, v))
                except ErroreCRM as e:  # rollback di tutto il lotto (context manager)
                    raise ErroreCRM(f"riga {i}: {e}") from None
            return ids
        return self._scrivi(_fn)

    def storna_movimento(self, movimento_id: int, fonte: str = "operatore",
                         nota: Optional[str] = None) -> int:
        """Annulla un movimento sbagliato aggiungendo il suo storno (il registro non si
        riscrive). Uno storno non si storna: si registra di nuovo il movimento giusto."""
        mid = _intero(movimento_id, "movimento_id", 1, 2**62)
        if fonte not in FONTI_MOVIMENTO:
            raise ErroreCRM("fonte non valida")
        testo_nota = _testo(nota, "nota", 500)

        def _fn(con: sqlite3.Connection) -> int:
            m = con.execute(
                "SELECT m.*, p.cliente_id FROM crm_movimenti m "
                "JOIN crm_posizioni p ON p.id = m.posizione_id WHERE m.id = ?", (mid,),
            ).fetchone()
            if m is None:
                raise ErroreCRM("movimento inesistente")
            if m["storno_di"] is not None:
                raise ErroreCRM("questo è già uno storno: registra di nuovo il movimento giusto")
            if m["tipo"] == "deposito" and self._capitale(con, m["posizione_id"]) < m["importo_cents"]:
                raise ErroreCRM("lo storno lascerebbe il capitale negativo: storna prima i prelievi")
            cur = con.execute(
                "INSERT INTO crm_movimenti (posizione_id, tipo, importo_cents, data, fonte, "
                "nota, storno_di, registrato_il) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (m["posizione_id"], m["tipo"], m["importo_cents"], m["data"], fonte,
                 testo_nota or f"storno del movimento #{mid}", mid, self._ts()),
            )
            autore = fonte if fonte in AUTORI else "operatore"
            self._evento(con, m["cliente_id"], "movimento",
                         f"Stornato il movimento #{mid} ({m['tipo']} "
                         f"{formatta_euro(m['importo_cents'])})", autore)
            return _nuovo_id(cur)
        return self._scrivi(_fn)

    def movimenti(self, cliente_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Tutti i movimenti (storni compresi), con `stornato` = 1 se annullato."""
        base = (
            "SELECT m.*, p.cliente_id, p.servizio_id, "
            "EXISTS (SELECT 1 FROM crm_movimenti s WHERE s.storno_di = m.id) AS stornato "
            "FROM crm_movimenti m JOIN crm_posizioni p ON p.id = m.posizione_id "
        )
        if cliente_id is None:
            return self._leggi(base + "ORDER BY m.data, m.id")
        return self._leggi(base + "WHERE p.cliente_id = ? ORDER BY m.data, m.id", (cliente_id,))

    # ------------------------------------------------------------------ proposte
    def crea_proposta(self, cliente_id: int, tipo: str, chiave: str, motivo: str,
                      messaggio: str, valore_stimato_cents: int = 0, livello: int = 1,
                      servizio_id: Optional[int] = None,
                      posizione_id: Optional[int] = None,
                      autore: str = "motore") -> Optional[int]:
        """Nuova proposta «da approvare». None se ce n'è già una aperta con la stessa
        chiave (il motore è idempotente). Solleva ErroreCRM sugli input sbagliati."""
        if tipo not in TIPI_PROPOSTA:
            raise ErroreCRM("tipo di proposta non valido")
        mot = _testo(motivo, "motivo", 500, obbligatorio=True)
        msg = _testo(messaggio, "messaggio", TESTO_MAX, obbligatorio=True)
        val = _intero(valore_stimato_cents, "valore_stimato_cents")
        liv = _intero(livello, "livello", 1, 3)
        ora = self._ts()
        try:
            with self._connect() as con:
                cur = con.execute(
                    "INSERT INTO crm_proposte (cliente_id, tipo, servizio_id, posizione_id, "
                    "stato, livello, motivo, messaggio, valore_stimato_cents, chiave, "
                    "creata_il, aggiornata_il) "
                    "VALUES (?, ?, ?, ?, 'da_approvare', ?, ?, ?, ?, ?, ?, ?)",
                    (cliente_id, tipo, servizio_id, posizione_id, liv, mot, msg, val,
                     chiave, ora, ora),
                )
                self._evento(con, cliente_id, "proposta",
                             f"Nuova opportunità ({tipo}, livello {liv}): {mot}", autore)
                con.commit()
                return _nuovo_id(cur)
        except sqlite3.IntegrityError as e:
            if "crm_proposte.chiave" in str(e) or "idx_crm_prop_aperta" in str(e):
                return None
            log.warning("CRM: proposta rifiutata dal DB: %s", e)
            raise ErroreCRM(_spiega_integrity(str(e))) from None
        except (sqlite3.Error, OSError) as e:
            log.warning("CRM: crea_proposta fallita (%s): %s", self.db_path, e)
            raise ErroreCRM("database non disponibile: riprova tra poco") from None

    def transiziona_proposta(self, proposta_id: int, nuovo_stato: str,
                             autore: str = "operatore", messaggio: Optional[str] = None,
                             canale: Optional[str] = None) -> Dict[str, Any]:
        """Cambia lo stato di una proposta secondo TRANSIZIONI_PROPOSTA. `messaggio`
        (solo da «da_approvare») salva il testo corretto dall'operatore prima dell'invio.
        Ritorna la proposta aggiornata; solleva ErroreCRM se la transizione non è ammessa."""
        pid = _intero(proposta_id, "proposta_id", 1, 2**62)
        if nuovo_stato not in STATI_PROPOSTA:
            raise ErroreCRM("stato non valido")
        msg = _testo(messaggio, "messaggio", TESTO_MAX)
        can = _testo(canale, "canale", 40)
        ora = self._ts()

        def _fn(con: sqlite3.Connection) -> Dict[str, Any]:
            p = con.execute("SELECT * FROM crm_proposte WHERE id = ?", (pid,)).fetchone()
            if p is None:
                raise ErroreCRM("proposta inesistente")
            attuale = p["stato"]
            if nuovo_stato not in TRANSIZIONI_PROPOSTA[attuale]:
                raise ErroreCRM(f"passaggio non ammesso: {attuale} → {nuovo_stato}")
            if msg is not None and attuale != "da_approvare":
                raise ErroreCRM("il testo si cambia solo prima dell'invio")
            if nuovo_stato == "inviata":
                # V-2 bot #381: STOP e consenso si ricontrollano DENTRO la transazione che
                # segna l'invio (uno STOP arrivato un attimo prima, da un'altra scheda o dalla
                # riga di comando, deve bloccarlo)
                c = con.execute("SELECT stato, opt_out, consenso_marketing, telefono "
                                "FROM crm_clienti WHERE id = ?", (p["cliente_id"],)).fetchone()
                if c is None or c["stato"] != "attivo":
                    raise ErroreCRM("non si può inviare: cliente non attivo")
                if c["opt_out"]:
                    raise ErroreCRM("non si può inviare: il cliente ha chiesto STOP")
                if not c["consenso_marketing"]:
                    raise ErroreCRM("non si può inviare: manca il consenso ai messaggi promozionali")
                if not c["telefono"]:
                    raise ErroreCRM("non si può inviare: manca il numero WhatsApp")
            sets = ["stato = ?", "aggiornata_il = ?"]
            args: List[Any] = [nuovo_stato, ora]
            if msg is not None:
                sets.append("messaggio = ?")
                args.append(msg)
            if nuovo_stato == "inviata":
                sets += ["inviata_il = ?", "canale = ?"]
                args += [ora, can or "whatsapp"]
            if nuovo_stato in ("accettata", "rifiutata", "senza_risposta", "scartata", "superata"):
                sets.append("esito_il = ?")
                args.append(ora)
            # condizione sullo stato letto: due click concorrenti non passano entrambi
            cur = con.execute(
                f"UPDATE crm_proposte SET {', '.join(sets)} WHERE id = ? AND stato = ?",
                (*args, pid, attuale),
            )
            if cur.rowcount != 1:
                raise ErroreCRM("la proposta è cambiata nel frattempo: ricarica")
            self._evento(con, p["cliente_id"], "proposta",
                         f"Proposta #{pid} ({p['tipo']}): {attuale} → {nuovo_stato}", autore)
            nuova = con.execute("SELECT * FROM crm_proposte WHERE id = ?", (pid,)).fetchone()
            return dict(nuova)
        return self._scrivi(_fn)

    def proposte(self, cliente_id: Optional[int] = None) -> List[Dict[str, Any]]:
        if cliente_id is None:
            return self._leggi("SELECT * FROM crm_proposte ORDER BY id")
        return self._leggi("SELECT * FROM crm_proposte WHERE cliente_id = ? ORDER BY id",
                           (cliente_id,))

    def proposta(self, proposta_id: int) -> Optional[Dict[str, Any]]:
        r = self._leggi("SELECT * FROM crm_proposte WHERE id = ?", (proposta_id,))
        return r[0] if r else None

    # ------------------------------------------------------------------ diario
    def annota(self, cliente_id: Optional[int], descrizione: str,
               autore: str = "operatore", tipo: str = "nota") -> None:
        desc = _testo(descrizione, "nota", 1000, obbligatorio=True)
        assert desc is not None
        if tipo not in ("nota", "sistema", "scansione"):
            raise ErroreCRM("tipo di nota non valido")
        self._scrivi(lambda con: self._evento(con, cliente_id, tipo, desc, autore))

    def eventi(self, cliente_id: Optional[int] = None, n: int = 50) -> List[Dict[str, Any]]:
        n = max(1, min(int(n), 500))
        if cliente_id is None:
            return self._leggi("SELECT * FROM crm_eventi ORDER BY id DESC LIMIT ?", (n,))
        return self._leggi("SELECT * FROM crm_eventi WHERE cliente_id = ? ORDER BY id DESC LIMIT ?",
                           (cliente_id, n))

    # ------------------------------------------------------------------ fotografia
    def fotografia(self) -> Optional[Dict[str, List[Dict[str, Any]]]]:
        """Tutte le tabelle lette in UNA transazione (vista coerente anche se Gas o la CLI
        scrivono nel frattempo). None se il DB non risponde: chi conta non deve scambiare
        un errore per «zero clienti»."""
        try:
            with self._connect() as con:
                con.execute("BEGIN")
                out = {
                    "servizi": self._rows(con.execute("SELECT * FROM crm_servizi ORDER BY priorita, id")),
                    "clienti": self._rows(con.execute("SELECT * FROM crm_clienti ORDER BY id")),
                    "posizioni": self._rows(con.execute("SELECT * FROM crm_posizioni ORDER BY id")),
                    "movimenti": self._rows(con.execute(
                        "SELECT m.*, EXISTS (SELECT 1 FROM crm_movimenti s WHERE s.storno_di = m.id) "
                        "AS stornato FROM crm_movimenti m ORDER BY m.data, m.id")),
                    "proposte": self._rows(con.execute("SELECT * FROM crm_proposte ORDER BY id")),
                }
                con.execute("COMMIT")
                return out
        except (sqlite3.Error, OSError) as e:
            log.warning("CRM: fotografia fallita (%s): %s", self.db_path, e)
            return None


def _nuovo_id(cur: sqlite3.Cursor) -> int:
    """Id della riga appena inserita (sempre presente dopo un INSERT riuscito)."""
    if cur.lastrowid is None:
        raise ErroreCRM("inserimento non riuscito")
    return int(cur.lastrowid)


def _spiega_integrity(msg: str) -> str:
    if "idx_crm_clienti_lead" in msg or "crm_clienti.contatto_id" in msg:
        return "questo lead è già un cliente"
    if "idx_crm_clienti_tel" in msg or "crm_clienti.telefono" in msg:
        return "esiste già un cliente con questo numero di telefono"
    if "crm_servizi.codice" in msg:
        return "esiste già un servizio con questo codice"
    if "idx_crm_mov_storno" in msg or "crm_movimenti.storno_di" in msg:
        return "questo movimento è già stato stornato"
    if "FOREIGN KEY" in msg:
        return "riferimento inesistente (cliente, servizio o posizione)"
    if "crm_posizioni.cliente_id, crm_posizioni.servizio_id" in msg:
        return "il cliente è già in questo servizio"
    return "dato non valido per il database"


def default_db_path(root: Union[str, Path]) -> Path:
    return Path(root) / DEFAULT_DB_FILENAME
