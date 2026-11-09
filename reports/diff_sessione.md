# Diff della sessione — 2026-11-09 notte — chat Mani, voce via Telegram fetta 3

File toccati (base main b827447, dopo il merge della PR #355):
- `modules/telegram/bot.py`: istruzione del turno parlato per i vocali (`_turno_con_finale(**extra)`), `testo_da_dire`, `VOCE_TIMEOUT_S` = 15 per sintesi e invio.
- `tests/test_unit_telegram_voce.py`: test dell'istruzione, della pulizia del parlato e dei tempi (da 51 a 59).
- `.claude/agents/memoria_revisore.md`: righe delle review #720 e #721.
- `reports/*`: report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
