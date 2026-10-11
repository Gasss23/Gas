# Diff della sessione — 2026-10-11 — conversazione dell'operatore fuori dagli snapshot notturni (PR #177)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py` — `self.carica_storia` salvato; `_snapshot` fotografa `.gas_history.json` solo se il kernel la carica.
- `modules/notte/notte.py` — docstring delle invarianti aggiornata.
- `reports/setup_notte.md` — una riga sul nuovo comportamento.
- `tests/test_unit_notte.py` — `_giro` con `carica_storia=False`; 3 test nuovi.
- `reports/stato_progetto.md` — #176 mergiata, seguito in PR #177.
- `.claude/agents/memoria_revisore.md` — riga review #254 (commit del revisore).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
