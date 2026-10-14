# DIFF SESSIONE — 2026-10-14 (D2)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/gate/gate.py` — `_CHIAVE_PRIVATA_RE`: nuovi nomi di credenziali vietati in lettura e scrittura (fetta D2, secondo passaggio claude.ai su #198), separatore anche con lo spazio (R-329-1).
- `tests/test_unit_gate.py` — nomi negati nuovi (D2 + casi con lo spazio) e falsi positivi leggibili; `dati/key.txt` passa da leggibile a negato (punto 1 del prompt).
- `.claude/agents/memoria_revisore.md` — righe delle review #329 e #330.
- `reports/stato_progetto.md` — D2 segnata FATTA; riserve R-329-2/3/4.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
