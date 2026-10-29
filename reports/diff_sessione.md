# DIFF SESSIONE — 2026-10-28 (chat Motore: interruttore del forte tra shell e .env, PR #293)

- `gas.py`: `_DOTENV_SCAVALCATE` (nomi delle variabili del `.env` scavalcate dalla shell con un valore diverso); con lo stesso valore il nome va in `_DOTENV_CARICATE` (V-1 bot #293); due WARN del doctor su `GAS_CLAUDE_CLI`.
- `tests/test_unit_kernel.py`: T99w e T99x.
- `tests/test_unit_dotenv.py`: test di `_DOTENV_SCAVALCATE`.
- `.claude/agents/memoria_revisore.md`: righe delle review #547 (già #543 nel ramo), #548 (merge di main con la PR #288), #549 e #550 (merge di main con la PR #294).
- `reports/stato_progetto.md`: punto 3 della RIPARTENZA (PR #290 chiusa, PR #293, R-543-1 e R-543-2) e «Ultimo aggiornamento».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
