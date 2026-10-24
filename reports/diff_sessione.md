# DIFF SESSIONE — 2026-10-24 (chat Motore, R2 via B fetta 3)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `brains/claude_cli.py`: costo su ogni errore dopo la risposta, prezzo per famiglia, pavimento per chiamata, `usage` robusto, parsing in `_risposta`.
- `gas.py`: `_leggi_uso_claude_cli` di modulo, conto sotto lucchetto con attesa limitata, forte fermo se il consumo non si registra, costi non finiti ignorati, sezione «Cervello forte» nel doctor, messaggio dei file protetti.
- `.gitignore`: lockfile del conto.
- `.claude/commands/fine-task.md`: segnaposto e commento di 4bis citano la deroga n/d.
- `tests/test_unit_claude_cli.py`, `tests/test_unit_kernel.py`: test nuovi (famiglie, pavimento, rami d'errore, eccezione imprevista, T99m/n/o, lockfile in T68s).
- `.claude/agents/memoria_revisore.md`: righe #502, #503.
- `reports/stato_progetto.md`, `reports/roadmap.md`: stato del forte dopo la fetta 3.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
