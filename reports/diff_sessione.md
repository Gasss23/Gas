# Diff sessione — 2026-06-25 Env-configurabilità sprint

> Si riscrive a ogni sessione. La storia completa sta in git.

## File toccati

| File | Cosa |
|---|---|
| `gas.py` | import `EMBED_MODEL_NAME`; `__init__` MEMORY_PIN_SCAN + WINDOW_CHAR_CAP overrides; VectorStore con `GAS_VECTORS_DB`/`GAS_EMBED_MODEL`; `doctor()` sez.9 Config |
| `tests/test_unit_kernel.py` | T37a, T37b, T37c, T37d, T37e (5 nuovi test) |
| `reports/stato_progetto.md` | finding chiusi, review count 30→31, suite 163→168 |
| `.claude/agents/memoria_revisore.md` | lezione review #31 |
| `reports/ultimo_report.md` | report task corrente |
| `reports/diff_sessione.md` | questo file |

## Cosa è cambiato e perché

**Env-configurabilità sprint:** 3 finding aperti chiusi in un colpo solo. Tutte le
costanti operative rilevanti di GAS ora sono override-abili via env senza ricompilare,
seguendo il pattern `_env_int`/`_env_float`/`_env_flag` già consolidato.

- `GAS_WINDOW_CHAR_CAP` → `WINDOW_CHAR_CAP` (default 24000, min_val=1000)
- `GAS_MEMORY_PIN_SCAN` → `MEMORY_PIN_SCAN` (default 200, min_val=10)
- `GAS_VECTORS_DB` → path sidecar vettoriale (`.resolve()` per coerenza con self.root)
- `GAS_EMBED_MODEL` → modello embedding (fallback su `EMBED_MODEL_NAME`)

`gas doctor` mostra ora una sezione 9 "Config" con i valori effettivi (sempre OK —
qualsiasi valore sporco è già clampato dall'helper), utile al deploy VPS.

**Review #31:** APPROVATO CON RISERVE. R37-1 (`.resolve()`) chiusa pre-commit;
R37-2 (doc gap finding chiusi) chiusa in questo report/commit.
