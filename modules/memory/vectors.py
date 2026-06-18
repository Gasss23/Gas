"""Vector store del retrieval semantico di GAS — FASE 2, fetta 1 (storage + embedding).

STANDALONE e ADDITIVO: questo modulo è il SOLO livello di persistenza + embedding
del retrieval semantico. NON è agganciato a `ricorda`/`run_turn`/loop (il cablaggio
è una fetta successiva, solo PROPOSTA nel report). GAS deve girare IDENTICO anche
senza questo layer: per questo ogni import pesante (numpy, fastembed) è protetto e
`available` ne tiene conto — importare `modules.memory` non fallisce mai se le
dipendenze del vector store mancano.

DESIGN (deciso a monte, vedi reports/ultimo_report.md):
  * File SIDECAR `<root>/.gas_vectors.db`, SEPARATO da `.gas_memory.db`. Il `.db`
    sacro della memoria NON si tocca MAI. Il sidecar è una CACHE DERIVATA e
    RICOSTRUIBILE dal diario: NON è fonte di verità, NON va nel backup, è gitignorato.
  * Schema GENERICO multi-source `(id, source, source_ref, testo, ts, vettore, dim,
    model)`. In v1 si popola SOLO `source='diario'` (`source_ref` = id riga diario);
    i campi source/source_ref sono già pronti per source futuri (trascritti vocali,
    RAG) senza migrazione.
  * Embedding LOCALE via fastembed. Il modello (e quindi i prefissi e la dimensione)
    è un parametro: il default è `paraphrase-multilingual-MiniLM-L12-v2` (384-dim,
    multilingue, regge l'italiano; scelta umana esplicita perché `multilingual-e5-small`
    non è nel catalogo fastembed 0.8.0). I prefissi e5 ("query: "/"passage: ") sono
    gestiti QUI nel codice (mai lasciati al chiamante), per-modello: per i non-e5
    valgono "" (applicarli a un non-e5 ne degrada la qualità).
  * Ricerca: brute-force COSINE in numpy (carica i vettori, dot product, top-k +
    soglia minima di similarità). NIENTE sqlite-vec (alpha pre-v1, formato instabile,
    fuori dal percorso critico di un agente h24) e NIENTE ANN: a questi numeri il
    brute-force è sotto i 10ms.
  * Vettori salvati come BLOB float32 NORMALIZZATI a norma 1 in scrittura → la cosine
    similarity diventa un semplice dot product.

"LA MEMORIA NON MENTE": ogni record porta il `ts` dell'evento SORGENTE. Il retrieval
restituisce EVENTI episodici e datati, non verità presenti (lo stato CORRENTE del
lead accanto allo snippet sarà aggiunto dalla fetta di wiring).

Fail-safe (§9 CLAUDE.md), l'intero layer è DEGRADANTE:
  * numpy/fastembed/onnxruntime assenti o pesi del modello non disponibili →
    `available=False`, NESSUN crash: `index`/`ricostruisci_da_diario` → None,
    `search` → [].
  * I pesi del modello si scaricano da HuggingFace al PRIMO uso (evento di RETE).
    In assenza di rete (es. VPS senza pre-provisioning) il caricamento fallisce →
    degrado, non crash. Per il deploy vanno pre-scaricati (vedi report).
  * DB sidecar mancante → creato; corrotto → warning + `available=False` + degrado
    (stesso pattern di MemoryStore).
"""
from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

log = logging.getLogger(__name__)

# Import pesanti PROTETTI: la loro assenza non deve impedire l'import del modulo
# (GAS gira identico senza il vector store). available ne tiene conto.
try:
    import numpy as _np
except Exception as _e:  # pragma: no cover — numpy è dipendenza di fastembed, quasi sempre presente
    _np = None
    log.warning("vector store: numpy non disponibile (%s) — layer degradato", _e)

try:
    from fastembed import TextEmbedding as _TextEmbedding
except Exception as _e:  # pragma: no cover — esercitato simulando l'assenza nei test
    _TextEmbedding = None
    log.warning("vector store: fastembed non disponibile (%s) — layer degradato", _e)


DEFAULT_VECTORS_FILENAME: str = ".gas_vectors.db"

# Modello di default. NB: la spec originale chiedeva `intfloat/multilingual-e5-small`,
# assente dal catalogo di fastembed 0.8.0; su scelta umana esplicita si usa il MiniLM
# multilingue 384-dim (entra nei vincoli RAM del VPS, regge l'italiano). Cambiare
# modello qui implica un rebuild dell'indice (i vettori sono filtrati per model+dim).
EMBED_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBED_DIM: int = 384

# Prefissi di embedding PER-MODELLO (gestiti nel codice, non dal chiamante).
# I modelli e5 richiedono "query: "/"passage: "; i non-e5 NON li vogliono → ("","").
# Aggiungere un modello e5 significa aggiungere QUI la sua coppia di prefissi.
_MODEL_PREFIXES: Dict[str, Tuple[str, str]] = {
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2": ("", ""),
    "intfloat/multilingual-e5-small": ("query: ", "passage: "),
    "intfloat/multilingual-e5-large": ("query: ", "passage: "),
}

# Tipo della funzione di embedding iniettabile (seam di test / DI): da una lista di
# testi a una matrice (n, dim) di vettori RAW (non normalizzati), o None in degrado.
EmbedFn = Callable[[List[str]], Optional["_np.ndarray"]]


def default_vectors_path(root: Union[str, Path]) -> Path:
    """Path di default del sidecar vettoriale: <root>/.gas_vectors.db (fuori da git,
    cache ricostruibile — separato dal .gas_memory.db sacro)."""
    return Path(root) / DEFAULT_VECTORS_FILENAME


# Schema idempotente del sidecar. UNIQUE(source, source_ref, model): un evento
# sorgente ha un solo vettore PER modello → `index` è idempotente (INSERT OR REPLACE)
# e un cambio di modello convive (vettori filtrati per model+dim in ricerca).
_SCHEMA: Tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS vettori (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        source     TEXT    NOT NULL,            -- 'diario' in v1; aperto a futuri source
        source_ref TEXT    NOT NULL,            -- id (come testo) della riga sorgente
        testo      TEXT    NOT NULL,            -- testo ORIGINALE (senza prefisso e5)
        ts         TEXT,                        -- ts dell'evento SORGENTE (la memoria non mente)
        vettore    BLOB    NOT NULL,            -- float32 normalizzato a norma 1
        dim        INTEGER NOT NULL,            -- lunghezza del vettore
        model      TEXT    NOT NULL,            -- modello che ha prodotto il vettore
        UNIQUE(source, source_ref, model)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_vettori_source ON vettori(source)",
    "CREATE INDEX IF NOT EXISTS idx_vettori_model ON vettori(model, dim)",
)


class VectorStore:
    """Storage + embedding del retrieval semantico. Connessioni a vita breve, ogni
    metodo blindato in try/except per non far mai crashare GAS (§9). `available`
    riflette SIA il sidecar apribile SIA la disponibilità dell'embedding (numpy +
    modello/embed_fn): se uno dei due manca, il layer degrada in modo sicuro."""

    def __init__(self, db_path: Union[str, Path],
                 model_name: str = EMBED_MODEL_NAME,
                 embed_fn: Optional[EmbedFn] = None,
                 model_cache_dir: Optional[Union[str, Path]] = None) -> None:
        self.db_path: Path = Path(db_path)
        self.model_name: str = model_name
        self.dim: int = EMBED_DIM
        self._model_cache_dir = model_cache_dir
        # Prefissi e5 per il modello scelto (gestiti nel codice). Modello ignoto → "".
        self._q_prefix, self._p_prefix = _MODEL_PREFIXES.get(model_name, ("", ""))
        # embed_fn iniettabile (seam di test / futura DI): se presente, si usa al posto
        # di fastembed (utile a verificare il ranking con vettori deterministici).
        self._embed_fn: Optional[EmbedFn] = embed_fn
        self._embedder = None  # istanza fastembed, caricata pigramente al primo uso
        # disponibilità dell'embedding: serve numpy E (una embed_fn iniettata OPPURE
        # fastembed importabile). Il caricamento dei pesi è pigro: un suo fallimento a
        # runtime abbassa questo flag (vedi _embed_raw).
        self._embedder_available: bool = (_np is not None) and (
            embed_fn is not None or _TextEmbedding is not None)
        self._db_available: bool = False
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            with self._connect() as con:
                for ddl in _SCHEMA:
                    con.execute(ddl)
                con.commit()
            self._db_available = True
        except (sqlite3.Error, OSError) as e:
            log.warning("VectorStore: init sidecar fallita su %s (%s) — degrado",
                        self.db_path, e)

    @property
    def available(self) -> bool:
        """True solo se il sidecar è apribile E l'embedding è utilizzabile."""
        return self._db_available and self._embedder_available

    # ------------------------------------------------------------------ infra
    def _connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(str(self.db_path), timeout=10)
        con.row_factory = sqlite3.Row
        return con

    def _get_embedder(self):
        """Carica pigramente il modello fastembed (il primo uso scarica i pesi da
        HuggingFace: evento di RETE). Cache di istanza. None → caricamento non
        possibile (degrado)."""
        if self._embedder is None and _TextEmbedding is not None:
            kw: Dict[str, Any] = {"model_name": self.model_name}
            if self._model_cache_dir is not None:
                kw["cache_dir"] = str(self._model_cache_dir)
            self._embedder = _TextEmbedding(**kw)
        return self._embedder

    def _embed_raw(self, testi: List[str]) -> Optional["_np.ndarray"]:
        """Embedding GREZZO (non normalizzato) di una lista di testi → matrice
        (n, dim) float32, o None in degrado. Usa la embed_fn iniettata se presente,
        altrimenti fastembed (caricamento pigro). Fail-safe §9: un errore di
        import/rete/modello abbassa _embedder_available e ritorna None (mai crash)."""
        if _np is None or not testi:
            return None
        try:
            if self._embed_fn is not None:
                mat = self._embed_fn(testi)
                return None if mat is None else _np.asarray(mat, dtype=_np.float32)
            emb = self._get_embedder()
            if emb is None:
                self._embedder_available = False
                return None
            vettori = list(emb.embed(testi))
            return _np.asarray(vettori, dtype=_np.float32)
        except Exception as e:  # rete/pesi/onnxruntime: degrada, non crasha
            log.warning("VectorStore: embedding fallito (%s) — degrado", e)
            self._embedder_available = False
            return None

    @staticmethod
    def _normalizza(mat: "_np.ndarray") -> "_np.ndarray":
        """Normalizza ogni riga a norma L2 = 1 (così la cosine diventa dot product).
        Le righe a norma nulla restano nulle (guardia anti divisione per zero)."""
        norme = _np.linalg.norm(mat, axis=1, keepdims=True)
        norme[norme == 0] = 1.0
        return (mat / norme).astype(_np.float32)

    @staticmethod
    def _to_blob(vec: "_np.ndarray") -> bytes:
        return _np.asarray(vec, dtype=_np.float32).tobytes()

    @staticmethod
    def _from_blob(blob: bytes) -> "_np.ndarray":
        return _np.frombuffer(blob, dtype=_np.float32)

    # --------------------------------------------------------------- scritture
    def index(self, source: str, source_ref: Union[str, int], testo: str,
              ts: Optional[str] = None) -> Optional[int]:
        """Indicizza UN testo: lo incorpora (prefisso 'passage') normalizzato e lo
        salva. Idempotente per (source, source_ref, model) via INSERT OR REPLACE.
        Ritorna il rowid, o None in degrado (embedding/DB non disponibili)."""
        if not self.available:
            return None
        mat = self._embed_raw([self._p_prefix + str(testo)])
        if mat is None or mat.shape[0] == 0:
            return None
        vec = self._normalizza(mat)[0]
        try:
            with self._connect() as con:
                cur = con.execute(
                    "INSERT OR REPLACE INTO vettori "
                    "(source, source_ref, testo, ts, vettore, dim, model) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (str(source), str(source_ref), str(testo), ts,
                     self._to_blob(vec), int(vec.shape[0]), self.model_name),
                )
                con.commit()
                return int(cur.lastrowid)
        except (sqlite3.Error, OSError) as e:
            log.warning("VectorStore.index fallita (%s): %s", self.db_path, e)
            return None

    def ricostruisci_da_diario(self, memory_store: Any) -> Optional[int]:
        """Svuota i vettori `source='diario'` e li RI-INDICIZZA dal diario di
        `memory_store` (sarà il motore del futuro `gas reindex`; qui NON cablato a
        un comando CLI). Legge TUTTE le voci del diario in SOLA LETTURA (immutabilità
        del diario intatta). Ritorna il numero di righe indicizzate, o None in degrado.

        Ordine SICURO: prima calcola TUTTI gli embedding (se falliscono → None, NON
        si tocca l'indice esistente), poi in UNA transazione svuota e re-inserisce.
        Un indice è una cache ricostruibile: ricostruire da un diario vuoto = indice
        vuoto (operazione esplicita, non un effetto collaterale)."""
        if not self.available or memory_store is None:
            return None
        # Lettore di SOLA LETTURA "tutte le voci"; se assente, degrada senza crash.
        lettore = getattr(memory_store, "diario_tutto", None)
        if not callable(lettore):
            log.warning("VectorStore.ricostruisci: memory_store senza diario_tutto — degrado")
            return None
        try:
            righe = lettore()
        except Exception as e:
            log.warning("VectorStore.ricostruisci: lettura diario fallita (%s)", e)
            return None

        vec_norm = None
        if righe:
            testi = [self._p_prefix + str(r["descrizione"]) for r in righe]
            mat = self._embed_raw(testi)
            if mat is None:
                return None  # embedding non disponibile: NON svuotare l'indice buono
            vec_norm = self._normalizza(mat)
        try:
            with self._connect() as con:
                con.execute("DELETE FROM vettori WHERE source = 'diario'")
                for i, r in enumerate(righe):
                    con.execute(
                        "INSERT OR REPLACE INTO vettori "
                        "(source, source_ref, testo, ts, vettore, dim, model) "
                        "VALUES ('diario', ?, ?, ?, ?, ?, ?)",
                        (str(r["id"]), str(r["descrizione"]), r["ts"],
                         self._to_blob(vec_norm[i]), int(vec_norm[i].shape[0]),
                         self.model_name),
                    )
                con.commit()
            return len(righe)
        except (sqlite3.Error, OSError) as e:
            log.warning("VectorStore.ricostruisci fallita (%s): %s", self.db_path, e)
            return None

    # ----------------------------------------------------------------- ricerca
    def search(self, query: str, k: int = 5, min_sim: float = 0.0,
               source: Optional[str] = None) -> List[Dict[str, Any]]:
        """Ricerca semantica: incorpora la query (prefisso 'query'), normalizza e
        confronta in brute-force cosine (dot product) con i vettori salvati dello
        STESSO modello e dimensione. Ritorna fino a `k` risultati con similarità
        >= `min_sim`, dal più simile. Ogni risultato include `score` (la similarità)
        e il `ts` dell'evento sorgente. [] in degrado o se nessun match supera la
        soglia. `source` opzionale filtra per origine (v1: 'diario')."""
        if not self.available:
            return []
        mat = self._embed_raw([self._q_prefix + str(query)])
        if mat is None or mat.shape[0] == 0:
            return []
        qvec = self._normalizza(mat)[0]
        return self._search_vec(qvec, k=k, min_sim=min_sim, source=source)

    def _search_vec(self, qvec: "_np.ndarray", k: int = 5, min_sim: float = 0.0,
                    source: Optional[str] = None) -> List[Dict[str, Any]]:
        """Cuore brute-force, separato per testabilità: dato un vettore query GIÀ
        normalizzato, carica i candidati (stesso model+dim, eventualmente filtrati
        per source), calcola il dot product e ritorna i top-k sopra soglia."""
        if _np is None:
            return []
        # SQL + decodifica BLOB + matmul nello STESSO try: il WHERE dim=? protegge dal
        # mismatch tra modelli, NON dalla corruzione FISICA di una cella (un BLOB
        # troncato → _from_blob solleva ValueError). Cattura anche ValueError così che
        # un sidecar fisicamente corrotto degradi a [] invece di crashare il turno
        # quando search sarà cablato in run_turn (fail-safe §9, R-vec-1).
        try:
            sql = ("SELECT source, source_ref, testo, ts, vettore FROM vettori "
                   "WHERE model = ? AND dim = ?")
            params: List[Any] = [self.model_name, int(qvec.shape[0])]
            if source is not None:
                sql += " AND source = ?"
                params.append(str(source))
            with self._connect() as con:
                righe = con.execute(sql, params).fetchall()
            if not righe:
                return []
            mat = _np.vstack([self._from_blob(r["vettore"]) for r in righe])
            sims = mat @ qvec  # righe e query normalizzate → dot product = cosine
        except (sqlite3.Error, OSError, ValueError) as e:
            log.warning("VectorStore.search fallita (%s): %s", self.db_path, e)
            return []
        # ordine decrescente di similarità, poi filtro soglia + taglio a k
        ordine = _np.argsort(-sims)
        out: List[Dict[str, Any]] = []
        for idx in ordine:
            score = float(sims[int(idx)])
            if score < min_sim:
                break  # ordinati: i successivi sono ancora più bassi
            r = righe[int(idx)]
            out.append({"source": r["source"], "source_ref": r["source_ref"],
                        "testo": r["testo"], "ts": r["ts"], "score": score})
            if len(out) >= k:
                break
        return out

    # ------------------------------------------------------------- diagnostica
    def conta(self, source: Optional[str] = None) -> int:
        """Numero di vettori indicizzati (totale o per source). 0 in degrado."""
        try:
            with self._connect() as con:
                if source is not None:
                    row = con.execute(
                        "SELECT COUNT(*) FROM vettori WHERE source = ?", (str(source),)
                    ).fetchone()
                else:
                    row = con.execute("SELECT COUNT(*) FROM vettori").fetchone()
                return int(row[0]) if row else 0
        except (sqlite3.Error, OSError) as e:
            log.warning("VectorStore.conta fallita (%s): %s", self.db_path, e)
            return 0
