# Diff della sessione — 2026-10-10 — «NON avviato» solo col lock davvero occupato (PR #172)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/notte/notte.py` — flock: «NON avviato» solo con EAGAIN/EWOULDBLOCK, altri errori rilanciati (giro interrotto); docstring aggiornate.
- `tests/test_unit_notte.py` — skipif Windows su 3 test del lock; 1 test nuovo (ENOLCK).
- `reports/setup_notte.md` — exit code aggiornati.
- `reports/stato_progetto.md` — #171 mergiata, seguito in PR #172.
- `.claude/agents/memoria_revisore.md` — riga review #245 (commit del revisore).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
