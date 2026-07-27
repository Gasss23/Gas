"""Modulo di memoria persistente di GAS (FASE 2).

Espone il livello di persistenza della memoria (SQLite, file singolo): un DIARIO
append-only (la storia, immutabile) e una RUBRICA contatti (mutabile per natura,
upsert-abile). Da FASE 2 fetta vector-store espone anche `VectorStore`, lo storage
+ embedding del retrieval semantico su un sidecar SEPARATO (`.gas_vectors.db`, cache
ricostruibile): STANDALONE, NON agganciato a run_turn (cablaggio in una fetta
successiva — vedi reports/ultimo_report.md §FINALE). Gli import del vector store sono
fail-safe: `modules.memory` si importa anche senza numpy/fastembed (GAS gira identico).
"""
from .store import (
    MemoryStore,
    ChiaveNormCollisione,
    STATI_CONTATTO,
    STATI_CHIUSI,
    STATO_DEFAULT,
    DEFAULT_DB_FILENAME,
    default_db_path,
    normalizza_chiave,
    normalizza_telefono,
)
from .vectors import (
    VectorStore,
    DEFAULT_VECTORS_FILENAME,
    EMBED_MODEL_NAME,
    EMBED_DIM,
    default_vectors_path,
)

__all__ = [
    "MemoryStore",
    "ChiaveNormCollisione",
    "STATI_CONTATTO",
    "STATI_CHIUSI",
    "STATO_DEFAULT",
    "DEFAULT_DB_FILENAME",
    "default_db_path",
    "normalizza_chiave",
    "normalizza_telefono",
    "VectorStore",
    "DEFAULT_VECTORS_FILENAME",
    "EMBED_MODEL_NAME",
    "EMBED_DIM",
    "default_vectors_path",
]
