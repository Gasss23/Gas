# DIFF SESSIONE — 2026-10-23 (chat Motore, R2 via B fetta 2)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `brains/claude_cli.py`: codice casuale per chiamata nei tag, lista di variabili permesse, errori senza testo di Claude, limite in testo semplice → QUOTA, argomenti non validi → errore, costo equivalente per chiamata.
- `gas.py`: tetto giornaliero del cervello forte (`.gas_claude_cli_uso.json`, `GAS_CLAUDE_CLI_TETTO_USD`), controllato prima di ogni chiamata del rung.
- `.gitignore`: il conto dell'uso del forte resta fuori dal repo.
- `tests/test_unit_claude_cli.py`: 18 test (codice, iniezione, ambiente, errori, costo).
- `tests/test_unit_kernel.py`: T99d rafforzato, T99g-j (conto, tetto, file illeggibile, altro giorno).
- `.claude/agents/memoria_revisore.md`: riga #496 e lezione.
- `reports/r2_regole_abbonamento.md`, `reports/roadmap.md`: tetto nella via B, stato delle fette.
- `reports/stato_progetto.md`: riserve R-496-1/2/3.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
- Correzioni dopo bot e verifica esterna #258 (`brains/claude_cli.py`, `gas.py`, test, `.gitignore`): costo 0, conto rovinato, LC_*, costo sugli errori.
