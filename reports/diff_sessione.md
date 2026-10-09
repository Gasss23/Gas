# Diff della sessione — 2026-10-09 — test ermetici (PR #165)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `tests/test_unit_kernel.py` — blocco T81 isola le variabili dei rung e del timeout Ollama; T81d calcolato dentro l'isolamento.
- `tests/test_unit_notte.py` — la fixture `_ermetico` toglie i tetti di tempo della notte dall'ambiente.
- `reports/stato_progetto.md` — nota T81b/T81d chiusa, #164 mergiata.
- `.claude/agents/memoria_revisore.md` — riga review #234 (commit del revisore).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
