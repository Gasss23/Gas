# DIFF SESSIONE — 2026-10-19 (fetta di pulizia, PR #217)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/gate/gate.py` — `_COPIA_PREFISSO` accetta anche il punto (R-bot210-3).
- `modules/notte/notte.py` — `_lezioni_in_attesa(kernel)`; «Lezioni da approvare» con tutte le lezioni in attesa, `max` con quelle del giro (R-345-3, R-359-1).
- `tests/test_unit_gate.py` — casi `old.keys/`, `backup.keys/`, `copy.tokens/` e falsi positivi.
- `tests/test_unit_notte.py` — `test_telegram_conta_tutte_le_lezioni_in_attesa`, `test_telegram_solo_lezioni_vecchie`.
- `tests/test_unit_kernel.py` — T92d3 nel `finally`, T92d4, T91d denominatore; tolta un'assegnazione morta.
- `reports/stato_progetto.md` — terza prova sul Mac, note di #216, R-345-3 e R-bot210-3 chiuse.
- `reports/roadmap_sintesi.md` — nuova: roadmap in una pagina.
- `.claude/agents/memoria_revisore.md` — righe #359–#360.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
