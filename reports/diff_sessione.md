# DIFF SESSIONE — 2026-10-25 (chat Motore, R2 via B fetta 5)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `brains/claude_cli.py`: negativo enorme scartato; massimo esplicito sulla stima dai token.
- `tests/test_unit_claude_cli.py`: casi -inf, -10**400; test del massimo sulla stima.
- `tests/test_unit_kernel.py`: T99q (catena costo massimo → conto → tetto).
- `.claude/agents/memoria_revisore.md`: riga #509.
- `reports/stato_progetto.md`: R-507-1 chiusa.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
