# DIFF SESSIONE — 2026-10-23 (chat Motore, R2 via B fetta 1)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `brains/claude_cli.py` (nuovo): adattatore `claude -p` con la forma del client OpenAI usata da `run_turn`; risposta JSON fissa, niente strumenti di Claude, ambiente pulito, trascrizione protetta dall'iniezione di tag.
- `brains/model_ids.py`: `MODEL_CLAUDE_FORTE` (env `GAS_MODEL_CLAUDE_FORTE`).
- `gas.py`: rung `claude-cli` nella cascata «forte», acceso solo da `GAS_CLAUDE_CLI`; `run_turn(..., cervello=None)`; prezzo 0 (abbonamento).
- `tests/test_unit_claude_cli.py` (nuovo): 12 test dell'adattatore (opzioni, ambiente, iniezione, codice intatto, errori/quota).
- `tests/test_unit_kernel.py`: T99a-f (round-trip, diario, cancello, interruttore, nessun ripiego sui gratuiti).
- `.github/workflows/ci.yml`: passo «Run claude-cli suite».
- `.claude/agents/memoria_revisore.md`: righe #492–#494 e lezioni.
- `reports/r2_regole_abbonamento.md`, `reports/roadmap.md`: 4,60 $/giorno, decisione via B.
- `reports/stato_progetto.md`: aggiornamento e riserve R-494-1/2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
- Merge di origin/main (PR #255, web fetta 13 della chat Mani): `modules/web/leggi.py` e `tests/test_unit_web_leggi.py` arrivano identici a main (review #495).
