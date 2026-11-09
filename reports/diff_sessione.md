# Diff della sessione — 2026-11-09 notte — chat Mani, voce via Telegram fetta 3

File toccati (base main 69d76b9, dopo il merge della PR #356):
- `modules/telegram/bot.py`: istruzione del turno parlato per i vocali (`_turno_con_finale(**extra)`), `testo_da_dire`, `VOCE_TIMEOUT_S` = 15 per sintesi e invio.
- `tests/test_unit_telegram_voce.py`: test dell'istruzione, della pulizia del parlato e dei tempi (da 51 a 59).
- `.claude/agents/memoria_revisore.md`: righe delle review #720, #721, #723, #724 e #726.
- `reports/*`: report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
