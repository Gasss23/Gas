# DIFF SESSIONE — 2026-10-07 — fix/verifica-bot-diagnosi (PR #144)

- `.github/workflows/verifica-bot.yml`: step "Diagnosi (solo se nessun modello ha dato il verdetto)" dopo "Raccogli il verdetto". Stampa subtype/is_error e, solo se is_error, il campo result su una riga e troncato a 400 caratteri. Perché: seconda prova reale su #142, i modelli escono subito con errore nascosto dall'action.
- `tests/test_unit_verifica_bot.py`: test `test_diagnosi_solo_result_e_dopo_i_modelli` (ordine, condizione, troncamento, una riga, solo is_error, niente segreti nell'env). 270 passed.
- `.claude/agents/memoria_revisore.md`: righe #194/#195 (commit del revisore).
- `reports/`: stato_progetto (seconda prova), ultimo_report, diff_sessione, handoff.
