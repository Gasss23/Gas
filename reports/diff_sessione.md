# DIFF SESSIONE — 2026-10-27 (turno di notte)

- `modules/memory/store.py`: `leggi_contatti` (None su errore); `lista_contatti` la avvolge — voce 5 della coda.
- `modules/notte/notte.py`: `stato_mattino` conta i lead con `leggi_contatti`; None → «non letti».
- `gas.py`: `_lead_fermi` (ricorda fermi) usa `leggi_contatti` come spia d'errore al posto di `conta_approvazioni`.
- `tests/test_unit_kernel.py`: T98h aggiornato, T98k e T98l nuovi.
- `tests/test_unit_notte.py`: fake aggiornati, test con tabella illeggibile e giro completo.
- `.claude/agents/memoria_revisore.md`: riga della review #520 (commit del revisore).
- `reports/coda_notte.md`: voci 4 e 5 in «Fatte» (PR #271 e #273).
- `reports/stato_progetto.md`: intestazione e blocco della notte con R-520-1.
- `reports/report_notte.md`: report del turno.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
