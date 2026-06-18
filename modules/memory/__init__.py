"""Modulo di memoria persistente di GAS (FASE 2 — fetta 1: fondamenta storage).

Espone il solo livello di persistenza (SQLite, file singolo): un DIARIO
append-only (la storia, immutabile) e una RUBRICA contatti (mutabile per
natura, upsert-abile). NON è ancora agganciato a run_turn: il cablaggio al
loop agentico è progettato a parte (vedi reports/ultimo_report.md §FINALE).
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
]
