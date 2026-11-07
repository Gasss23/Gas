# Diff della sessione — 2026-11-07 — Sottofondo: seconda fetta BASSE (chat M2)

- `modules/sottofondo/__init__.py` — `annulla` chiude solo compiti aperti e dice se ha chiuso; `_ripulisci` avvisa solo in quel caso; `controlla` pulisce i compiti vecchi al massimo una volta l'ora.
- `gas.py` — `GasKernel.per_sottofondo`: riga nel system prompt (avvisa_operatore non esiste nel processo in sottofondo).
- `tests/test_unit_sottofondo.py` (67), `tests/test_unit_kernel.py` (T106a/c).
- `.claude/agents/memoria_revisore.md` — review #706.
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
