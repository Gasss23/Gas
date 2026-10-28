# Diff della sessione — 2026-10-28 (chat Motore, PR #292)

- `gas.py`: `_DOTENV_NEL_FILE: Dict[str, str]` al posto di `_DOTENV_CARICATE` (registrato con `setdefault` per ogni riga valida del `.env`); `_avviso_claude_timer` prende `valore_file` al posto di `da_dotenv` (WARN «altro valore», nome nudo → cartelle, eccezione «claude» solo senza variabile nel `.env`); il doctor passa `_DOTENV_NEL_FILE.get("GAS_CLAUDE_BIN")`.
- `tests/test_unit_kernel.py`: T99s (caso «altro valore»), T99t (nuovi casi, chiamate con `valore_file`, collegamenti tolti dopo l'uso).
- `tests/test_unit_dotenv.py`: test sul dizionario e sulla riga doppia.
- `.claude/agents/memoria_revisore.md`: review #543, #544 (due righe), #545, #547.
- Merge di origin/main (PR #288, chat Mani): conflitti nei report e nella memoria risolti, codice di main identico (fuori dal diff della sessione).
- `reports/stato_progetto.md`: «Ultimo aggiornamento» e punto 3 della ripartenza Motore.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
