# Diff della sessione — 2026-11-07 — Sottofondo: riserve BASSE (chat M2)

- `modules/sottofondo/__init__.py` — `_identita` (sì/no/non so) al posto del solo `_e_nostro`; `attivo()` libera il posto con pid estraneo; `_creato` robusto (non numerico, non finito, futuro); `controlla()` per il kernel; «fermato» solo se killpg riesce; `_pulisci_vecchi` (GAS_SOTTOFONDO_GIORNI); `_numero_env` con isfinite.
- `gas.py` — `GasKernel.per_sottofondo` (senza avvisa_operatore: offerta, dispatch, cancello); `controlla` a inizio turno; `gas.py sottofondo <id>` usa il nuovo costruttore.
- `tests/test_unit_sottofondo.py` (59), `tests/test_unit_kernel.py` (T106a-d).
- `.claude/agents/memoria_revisore.md` — review #701/#702.
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
