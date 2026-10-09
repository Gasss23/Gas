# Diff della sessione — 2026-10-09 — test R-226-4 / R-227-1 (PR #164)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `tests/test_unit_notte.py` — test del tetto per compito col kernel vero: run_turn chiuso a metà, `turno_fine esito=ko` scritto prima della riga `notte` (R-226-4, V-1 bot #164).
- `tests/test_unit_kernel.py` — T81h: rung Ollama in run_turn con timeout 600 e max_retries 1 (R-227-1).
- `.gitignore` — `gas_debug.log.*` (log ruotati dai test).
- `reports/stato_progetto.md` — R-226-4, R-227-1 chiuse; #163 mergiata; nuove note (T81b/T81d non ermetici, V-2 bot #163).
- `.claude/agents/memoria_revisore.md` — lezioni review #232 e #233 (commit del revisore).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
