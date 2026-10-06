# DIFF SESSIONE — 2026-10-06 — V-B fetta B2 (feat/merge-automatico-z1xjx2)

> Si riscrive a ogni sessione; la storia completa sta in git. Range: `merge-base(origin/main, HEAD)..HEAD` (include `e51db2e` della sessione locale precedente, stessa fetta). Gli arretrati della notte stanno nei loro branch (PR #132–#136), ognuno col proprio diff_sessione.

- `scripts/bot_esito.py` — check run `verifica-bot` dell'App (G-1), NO definitivo per SHA (G-2), lista bianca doc-only (G-4), `.gitattributes` (G-5), formato esatto del verdetto (R-161-1); R-163-1: prima il verdetto, solo APPROVE+macchina = OPERATORE, `stato_elenco` separato, "non verificabile" mai neutral; R-164-1 head prima del NO da elenco troncato.
- `.github/workflows/verifica-bot.yml` — token App con checks write, APP_SLUG, formato nel prompt; output `elenco` → `ELENCO_FILE`; job verifica solo con elenco "ok" (R-164-2).
- `scripts/gasmerge.sh` — HEAD_SHA legato al ref (V-3 #127); `--auto N` col check dell'App richiesto dal ruleset.
- `tests/test_unit_verifica_bot.py` — test di G-1/G-2/G-4/G-5/R-161-1 e di R-163-1, R-163-4, R-164-1/2 (268 test).
- `tests/test_unit_gasmerge.py` — test di `--auto` e V-3 #127 (85 test).
- `.claude/commands/fine-task.md` — §4quater: `gh pr edit N --add-label verifica`, etichetta creata dall'operatore.
- `.claude/agents/memoria_revisore.md` — righe #163, #164, #165.
- `reports/setup_verifica_bot.md` — App con Checks R/W, §D etichetta dell'operatore, §F ruleset col check dell'App e significato di neutral, R-163-3.
- `reports/stato_progetto.md` — header, B2, R-160-1 MITIGATA, R-163-2/R-164-3.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task (riepilogo della notte in ultimo_report).
