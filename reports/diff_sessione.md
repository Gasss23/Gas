# Diff della sessione — 2026-11-09 notte — Voce: cache delle frasi fisse (chat M2)

- `modules/voice/server.py` — `sintesi()` con cache delle frasi fisse; `_finiti_jobs` azzerato a inizio richiesta; funzione al posto della lambda; parentesi nella condizione del segno.
- `tests/test_unit_voice_server.py`, `tests/test_unit_sottofondo.py`.
- `.claude/agents/memoria_revisore.md` — review #715.
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
