# Diff sessione — 2026-09-24

Branch: feat/apprendimento-f1-esiti  
Scope: Auto-apprendimento Fetta 1 — fonte + turno_id + turno_fine nel diario

## File toccati

| File | Cosa è cambiato | Perché |
|------|----------------|--------|
| `gas.py` | `import uuid`; `DIARIO_NOISE_TIPI` += `"turno_fine"`; `_diario_log` accetta `fonte`/`turno_id`; `run_turn` wrappato in `try/finally` con tracking per-turno e `_chiudi_turno()` | Scrivere una riga `turno_fine` a fine ogni turno con esito deterministico (fetta 1 auto-apprendimento) |
| `modules/memory/store.py` | `_ensure_columns` aggiunge colonne `fonte`/`turno_id` al diario; `append_diario` accetta `fonte`/`turno_id` | Struttura dati per identificare fonte e raggruppare eventi per turno nel diario |
| `tests/test_unit_kernel.py` | T64a–T64i nuovi (24 test); T20a/b/c aggiornati per filtrare `turno_fine` | Copertura migrazione, tutti gli esiti (ok/parziale/ko), GeneratorExit, memoria None, coerenza turno_id |
| `.claude/agents/memoria_revisore.md` | Aggiunta riga contatore review #103 | Aggiornamento memoria del revisore dopo APPROVATO |
| `reports/stato_progetto.md` | Aggiornamento data, contatore review (#103), baseline test (318 PASS) | Fotografia viva dello stato del progetto |
| `reports/ultimo_report.md` | Report completo fetta 1: modifiche, test, E2E, review | Fonte di verità del task |
