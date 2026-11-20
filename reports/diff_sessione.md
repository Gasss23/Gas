# Diff della sessione — 2026-11-20 — Bot di verifica: falso rosso «Non bloccante»

Si riscrive a ogni sessione; la storia completa sta in git. Ramo `claude/fix-bot-non-maiuscolo`, partito da main d03e5bf2 (la PR #388 del CRM è su un altro ramo).

- `scripts/bot_esito.py`: `_GRAVITA_NEGATA` riconosce anche «Non» con l'iniziale maiuscola.
- `tests/test_unit_verifica_bot.py`: il caso reale della PR #388 (deve dare APPROVE) e 8 casi che devono restare bloccati.
- `reports/stato_progetto.md`, report di fine task, `.claude/agents/memoria_revisore.md`.
