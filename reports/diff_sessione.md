# Diff sessione — feat/cancello-c4a — 2026-10-03

## Sommario

Sessione C4a: R-c3-1b (fix expire_stale_approvals) + collegamento coda al loop.

## git diff --stat (main → feat/cancello-c4a)

```
.claude/agents/memoria_revisore.md |   2 +
gas.py                             |  48 +++++--
modules/memory/store.py            |  19 ++-
tests/test_unit_kernel.py          | 267 ++++++++++++++++++++++++++++++++++---
4 files changed, 304 insertions(+), 32 deletions(-)
```

## File toccati e motivo

### gas.py (+48, -7)
- **Stub C2 sostituito** (riga ~1942): blocco `elif IRREVERSIBLE / UNCERTAIN+contaminated` non chiama più `execute_tool_call`. Invece chiama `enqueue_approval` con fail-closed a 3 livelli.
- **Variabile `_gate_pending_id`** inizializzata a `None` prima del gate per il ternario diario.
- **Diario**: branch pending scrive `pending id=<uuid>` senza args (F-diario-eco/args).
- DENY e SAFE invariati.

### modules/memory/store.py (+19, -4)
- **`expire_stale_approvals`**: aggiunto primo UPDATE per `typeof(ts_expiry) NOT IN ('real','integer')` + WARN + conteggio sommato. Fix R-c3-1b.

### tests/test_unit_kernel.py (+267, -25)
- **T73h-bis** (7 check): R-c3-1b — INSERT grezzo con ts_expiry TEXT, controprova pre-fix, verifica via SQL grezzo.
- **T74a-g** (29 check): C4a loop — IRREVERSIBLE, UNCERTAIN+contaminata, UNCERTAIN pulita, DENY, enqueue lancia, store=None, grep stub.
- **F-c4a-dedup** (1 check): finding misurabile — 3 enqueue identici → 3 UUID distinti.
- **T70f/T70g aggiornati** (-15, +8): run_command ora parcheggiato (IRREVERSIBLE), test aggiornati al nuovo comportamento.

### .claude/agents/memoria_revisore.md (+2)
- Entry review #127 aggiunta dal revisore (commit cce2211).

## Risultati test

- **python3 tests/test_unit_kernel.py**: 501 PASS, 5 FAIL (F-mac-1, invariati)
- **pytest tests/ --ignore=tests/test_unit_kernel.py**: 227/227 PASS
- Baseline pre-sessione: 472 PASS, 5 FAIL → delta +29 PASS
