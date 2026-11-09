# Diff della sessione — 2026-11-09 — chat Mani, voce via Telegram fetta 2

File toccati (base main fa6b1f3, dopo il merge della PR #354):
- `modules/telegram/bot.py`: `_turno_con_finale`, risposta a voce dopo un vocale (`_invia_risposta_vocale`, `_tg_post_file`, GAS_TELEGRAM_VOCE), import di stt protetto, una sola lettura del tetto orario, docstring.
- `tests/test_unit_telegram_voce.py`: test della fetta 2 e delle riserve della #353 (da 31 a 51).
- `tests/test_unit_voce_ascolto.py`: test esatto del «log ogni 100» e test di inf/nan (riserve della #351).
- `.claude/agents/memoria_revisore.md`: righe delle review #717, #718 e #719.
- `reports/*`: report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
