# DIFF SESSIONE — 2026-10-28 (turno di notte)

- `modules/memory/store.py`: tabella `approval_esiti_in_storia` (solo inserimenti) e metodi `segna_esito_in_storia` / `esito_in_storia` — voce 6 della coda.
- `gas.py`: segno nel DB in `_esito_firma_in_storia` / `_storia_esito_firma` / `recupera_esito_firma`; esito nel DB prima della storia in `applica_firma`.
- `tests/test_unit_kernel.py`: T78q–T78u.
- `.claude/agents/memoria_revisore.md`: righe delle review #531 e #532 (commit del revisore).
- `reports/coda_notte.md`: voci 0 (PR #279) e 6 (PR #281) in «Fatte».
- `reports/stato_progetto.md`: intestazione e blocco della notte con R-531-3 e R-532-1.
- `reports/report_notte.md`: report del turno.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
