# Diff della sessione — 2026-11-08 — chat Mani, voce via Telegram fetta 1

File toccati (base main 3084979, dopo il merge della PR #352):
- `modules/telegram/bot.py`: ramo dei vocali in `_handle_update` (dopo il controllo della chat autorizzata), `_scarica_vocale`, `testo_da_vocale`, tetto orario, `_gestisci_parlato`, `_risposta_del_turno` (estratta, stesso comportamento per i testi).
- `tests/test_unit_telegram_voce.py`: 31 test con Telegram, download e Groq finti.
- `.github/workflows/ci.yml`: il file di test nella voice suite.
- `reports/proposta_voce_telegram.md`: decisioni dell'operatore e correzioni V-1/V-2/V-3 del bot sulla #348.
- `.claude/agents/memoria_revisore.md`: righe delle review #711, #712, #715 e #716.
- `reports/*`: report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
