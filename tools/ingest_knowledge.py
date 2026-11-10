#!/usr/bin/env python3
"""
Gas knowledge ingestor — CLI off-loop (K2).

Legge knowledge/sources.yaml → chunking → scrive in .gas_knowledge.db.
Idempotente: stesso contenuto = zero doppioni (confronto SHA-256).
Versioning: se una fonte cambia, inserisce nuova versione e marca la vecchia
            'superseded' senza mai cancellarla.

NON tocca .gas_memory.db. NON interagisce con gas.py o run_turn.
È uno strumento manuale da riga di comando.

Uso:
    python tools/ingest_knowledge.py
    python tools/ingest_knowledge.py --source test_local
    python tools/ingest_knowledge.py --dry-run
    python tools/ingest_knowledge.py --db /path/custom.db
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# ─────────────────────────────────────────────────────────────────────────────
# Costanti
# ─────────────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent.resolve()
SOURCES_YAML = REPO_ROOT / "knowledge" / "sources.yaml"
KNOWLEDGE_DB = REPO_ROOT / ".gas_knowledge.db"
DEFAULT_CHUNK_CHARS = 1800  # ≈ 500 token (stima 3.6 char/token)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("ingest_knowledge")


# ─────────────────────────────────────────────────────────────────────────────
# Schema DB (K1)
# ─────────────────────────────────────────────────────────────────────────────
_DDL = [
    """
    CREATE TABLE IF NOT EXISTS knowledge (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        source_name    TEXT    NOT NULL,
        chunk_ref      TEXT    NOT NULL,
        testo          TEXT    NOT NULL,
        hash_contenuto TEXT    NOT NULL,
        ts_source      TEXT,
        ts_ingested    TEXT    NOT NULL,
        origine_uri    TEXT,
        versione       INTEGER NOT NULL DEFAULT 1,
        stato          TEXT    NOT NULL DEFAULT 'active'
    )
    """,
    # Partial unique index: al massimo un record 'active' per (source_name, chunk_ref)
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_knowledge_active
        ON knowledge(source_name, chunk_ref) WHERE stato = 'active'
    """,
    "CREATE INDEX IF NOT EXISTS idx_knowledge_source ON knowledge(source_name)",
    "CREATE INDEX IF NOT EXISTS idx_knowledge_hash   ON knowledge(hash_contenuto)",
]


def open_db(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    for stmt in _DDL:
        conn.execute(stmt)
    conn.commit()
    _init_fts(conn)
    return conn


def _init_fts(conn: sqlite3.Connection) -> None:
    """Crea tabella FTS5 e trigger di sync per la knowledge base.
    Idempotente (IF NOT EXISTS). Backfill dei chunk preesistenti via 'rebuild'.
    Fail-safe: SQLite senza FTS5 → solo warning, il DB resta usabile."""
    try:
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts "
            "USING fts5(testo, content='knowledge', content_rowid='id')"
        )
        conn.execute(
            "CREATE TRIGGER IF NOT EXISTS knowledge_fts_ai "
            "AFTER INSERT ON knowledge "
            "BEGIN INSERT INTO knowledge_fts(rowid, testo) VALUES (new.id, new.testo); END"
        )
        # Backfill idempotente: indicizza chunk preesistenti (DB legacy o chunk
        # scritti prima che la virtual table esistesse).
        conn.execute("INSERT INTO knowledge_fts(knowledge_fts) VALUES('rebuild')")
        conn.commit()
    except sqlite3.Error as e:
        log.warning("FTS5 non disponibile o errore init (%s) — knowledge_fts assente", e)


# ─────────────────────────────────────────────────────────────────────────────
# Chunking
# ─────────────────────────────────────────────────────────────────────────────
def chunk_text(text: str, chunk_chars: int) -> list[str]:
    """Divide il testo in chunk da ≤ chunk_chars char, spezzando ai capoversi.
    Audit 2026-11-10 B2: un capoverso più lungo del tetto (testo incollato senza
    righe vuote) si spezza in pezzi ≤ chunk_chars, possibilmente a uno spazio:
    prima diventava un chunk unico di qualunque lunghezza."""
    chunk_chars = max(1, chunk_chars)
    paragraphs: list[str] = []
    for p in (p.strip() for p in text.split("\n\n")):
        while len(p) > chunk_chars:
            taglio = p.rfind(" ", 0, chunk_chars + 1)
            if taglio < chunk_chars // 2:
                taglio = chunk_chars  # niente spazio utile: taglio netto
            paragraphs.append(p[:taglio].rstrip())
            p = p[taglio:].lstrip()
        if p:
            paragraphs.append(p)
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        # Se aggiungere questo para supera il limite E c'è già roba → scarica
        if current_len + len(para) > chunk_chars and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = len(para)
        else:
            current.append(para)
            current_len += len(para) + 2  # +2 per "\n\n"

    if current:
        chunks.append("\n\n".join(current))

    return chunks


# ─────────────────────────────────────────────────────────────────────────────
# Ingest singola fonte
# ─────────────────────────────────────────────────────────────────────────────
def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ingest_file_source(conn: sqlite3.Connection, source: dict) -> dict[str, int | str]:
    nome: str = source["nome"]
    uri: str = source["uri"]
    chunk_max: int = int(source.get("chunk_max", 100))
    chunk_chars: int = int(source.get("chunk_chars", DEFAULT_CHUNK_CHARS))

    abs_path = REPO_ROOT / uri
    # V-1 bot #228: le fonti di tipo file stanno SOLO dentro knowledge/, l'unica
    # cartella protetta dalla firma (gate.py, _LIVELLO2_TOP). Fuori, o risalendo con
    # «..» o un symlink, Gas potrebbe riscrivere la fonte: fonte rifiutata.
    cartella = (REPO_ROOT / "knowledge").resolve()
    try:
        abs_path.resolve().relative_to(cartella)
    except (ValueError, OSError):
        log.error("[%s] uri fuori da knowledge/: %s — fonte rifiutata", nome, uri)
        return {"source": nome, "error": "uri fuori da knowledge/", "ingested": 0, "skipped": 0}
    if not abs_path.exists():
        log.error("[%s] file non trovato: %s", nome, abs_path)
        return {"source": nome, "error": "file not found", "ingested": 0, "skipped": 0}

    ts_source = datetime.fromtimestamp(
        abs_path.stat().st_mtime, tz=timezone.utc
    ).isoformat()
    text = abs_path.read_text(encoding="utf-8")
    chunks = chunk_text(text, chunk_chars)

    if len(chunks) > chunk_max:
        log.warning(
            "[%s] %d chunk > chunk_max=%d — troncato a %d",
            nome, len(chunks), chunk_max, chunk_max,
        )
        chunks = chunks[:chunk_max]

    now = datetime.now(tz=timezone.utc).isoformat()
    stats: dict[str, int] = {"ingested": 0, "skipped": 0, "superseded": 0}

    for idx, chunk in enumerate(chunks):
        chunk_ref = f"chunk_{idx:04d}"
        h = _sha256(chunk)

        existing = conn.execute(
            "SELECT id, hash_contenuto, versione FROM knowledge "
            "WHERE source_name = ? AND chunk_ref = ? AND stato = 'active'",
            (nome, chunk_ref),
        ).fetchone()

        if existing:
            if existing["hash_contenuto"] == h:
                log.debug("[%s] %s — hash identico, skip", nome, chunk_ref)
                stats["skipped"] += 1
                continue
            # Contenuto cambiato: supersede il vecchio e inserisce il nuovo
            conn.execute(
                "UPDATE knowledge SET stato = 'superseded' WHERE id = ?",
                (existing["id"],),
            )
            new_ver: int = existing["versione"] + 1
            log.info(
                "[%s] %s — contenuto cambiato, v%d → v%d",
                nome, chunk_ref, existing["versione"], new_ver,
            )
            stats["superseded"] += 1
        else:
            new_ver = 1

        conn.execute(
            """INSERT INTO knowledge
               (source_name, chunk_ref, testo, hash_contenuto,
                ts_source, ts_ingested, origine_uri, versione, stato)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active')""",
            (nome, chunk_ref, chunk, h, ts_source, now, str(abs_path), new_ver),
        )
        log.info(
            "[%s] %s v%d ingerito (%d chars)", nome, chunk_ref, new_ver, len(chunk)
        )
        stats["ingested"] += 1

    # Audit 2026-11-10 B1: i chunk oltre la nuova lunghezza della fonte (fonte
    # accorciata, o troncata a chunk_max) non esistono più → superseded, mai
    # cancellati (stessa regola del versioning). Prima restavano attivi e Gas
    # continuava a pescare testo tolto dalla fonte.
    attuali = {f"chunk_{i:04d}" for i in range(len(chunks))}
    for vecchio in conn.execute(
            "SELECT id, chunk_ref FROM knowledge WHERE source_name = ? AND stato = 'active'",
            (nome,)).fetchall():
        if vecchio["chunk_ref"] not in attuali:
            conn.execute("UPDATE knowledge SET stato = 'superseded' WHERE id = ?",
                         (vecchio["id"],))
            log.info("[%s] %s — non più nella fonte, superseded", nome, vecchio["chunk_ref"])
            stats["superseded"] += 1

    conn.commit()
    log.info(
        "[%s] completato — ingested=%d skipped=%d superseded=%d",
        nome, stats["ingested"], stats["skipped"], stats["superseded"],
    )
    return {"source": nome, **stats}


def carica_fonti(percorso: Path) -> list[dict]:
    """Audit 2026-11-10 B3: sources.yaml vuoto o di forma sbagliata → nessuna fonte
    (con un log), mai AttributeError. Le voci che non sono dizionari si scartano."""
    with open(percorso, encoding="utf-8") as fh:
        catalogo = yaml.safe_load(fh)
    if not isinstance(catalogo, dict):
        if catalogo is not None:
            log.error("sources.yaml: attesa una mappa con 'sources', trovato %s",
                      type(catalogo).__name__)
        return []
    fonti = catalogo.get("sources") or []
    if not isinstance(fonti, list):
        log.error("sources.yaml: 'sources' non è una lista")
        return []
    return [f for f in fonti if isinstance(f, dict)]


def ingest_fonti(conn: sqlite3.Connection, fonti: list[dict]) -> dict[str, int]:
    """Ingerisce le fonti una per una. Audit 2026-11-10 B3: una fonte rotta (file non
    UTF-8, uri che è una cartella, voce senza uri) si salta con un log e le altre
    proseguono; prima un'eccezione fermava l'intero ingest."""
    totale = {"ingested": 0, "skipped": 0, "errori": 0}
    for src in fonti:
        nome = src.get("nome", "?")
        tipo = src.get("tipo", "file")
        if tipo != "file":
            log.warning("[%s] tipo '%s' non supportato in K2, skip", nome, tipo)
            continue
        try:
            result = ingest_file_source(conn, src)
        except (OSError, UnicodeError, KeyError, ValueError, TypeError, sqlite3.Error) as e:
            try:
                conn.rollback()  # niente mezza fonte: o tutta o niente
            except sqlite3.Error:
                pass
            log.error("[%s] fonte saltata: %s", nome, type(e).__name__)
            totale["errori"] += 1
            continue
        if result.get("error"):
            totale["errori"] += 1
        totale["ingested"] += int(result.get("ingested", 0))
        totale["skipped"] += int(result.get("skipped", 0))
    return totale


# ─────────────────────────────────────────────────────────────────────────────
# Entrypoint
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gas knowledge ingestor (off-loop, K2)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Mostra le fonti attive senza scrivere nel DB",
    )
    parser.add_argument(
        "--source", metavar="NOME",
        help="Processa solo questa fonte (slug da sources.yaml)",
    )
    parser.add_argument(
        "--db", metavar="PATH",
        help=f"Path al DB knowledge (default: {KNOWLEDGE_DB})",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Log DEBUG (mostra anche i chunk skippati)",
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    db_path = Path(args.db) if args.db else KNOWLEDGE_DB

    if not SOURCES_YAML.exists():
        log.error("sources.yaml non trovato: %s", SOURCES_YAML)
        sys.exit(1)

    all_sources: list[dict] = carica_fonti(SOURCES_YAML)

    if args.source:
        all_sources = [s for s in all_sources if s.get("nome") == args.source]
        if not all_sources:
            log.error("Fonte '%s' non trovata in sources.yaml", args.source)
            sys.exit(1)

    active = [s for s in all_sources if s.get("attiva", True)]
    log.info("Fonti attive da processare: %d", len(active))

    if args.dry_run:
        for s in active:
            log.info("[DRY RUN] %s (%s) → %s", s.get("nome", "?"), s.get("tipo", "file"),
                     s.get("uri", "?"))
        return

    conn = open_db(db_path)
    log.info("DB: %s", db_path)

    totale = ingest_fonti(conn, active)

    conn.close()
    log.info("=== TOTALE: ingested=%d  skipped=%d  fonti con errori=%d ===",
             totale["ingested"], totale["skipped"], totale["errori"])
    # V-3 bot #366: le altre fonti sono caricate, ma chi lancia l'ingest da script deve
    # vedere che qualcosa è fallito: ora OGNI fonte fallita (anche un file mancante o un
    # uri rifiutato, che prima davano exit 0) fa uscire con 1 (V-1 bot #366)
    if totale["errori"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
