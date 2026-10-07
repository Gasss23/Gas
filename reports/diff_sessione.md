# DIFF SESSIONE — 2026-10-07 — fix/verifica-bot-strumenti (PR #146)

- `.github/workflows/verifica-bot.yml`: schema con campo obbligatorio `strumenti_ok` (boolean); PROMPT: true solo se letti gh pr diff e gh pr checks. Perché: R-196-1, verdetto alla cieca nella terza prova su #142.
- `scripts/bot_esito.py`: `_decidi_verdetto` dà RIPROVA se `strumenti_ok` non è esattamente true; docstring aggiornata.
- `tests/test_unit_verifica_bot.py`: fixture con strumenti_ok; nuovi test (valori non true, assente, macchina bot, doc-only, schema e prompt). 283 passed.
- `reports/setup_verifica_bot.md`: nuovo caso di `cancelled` (R-198-2).
- `.claude/agents/memoria_revisore.md`: riga #198.
- `reports/`: stato_progetto (quarta prova, bot convalidato, R-196-1 chiusa), ultimo_report, diff_sessione, handoff.
