# ULTIMO REPORT — 2026-10-05 — V-B vera, fetta B1: bot di verifica esterna su GitHub

## Decisioni umane richieste

1. Merge della PR #130 (https://github.com/Gasss23/Gas/pull/130) — variante A: `gasmerge 130`, digiti tu il numero.
2. Setup del bot (dopo il merge): passi numerati in `reports/setup_verifica_bot.md` — token dell'abbonamento, GitHub App `gas-verificatore`, environment `verifica-bot`. Serve prima del test di convalida (fetta B2).
3. **R-158-5**: il bot su GitHub è di sola lettura (non esegue test). In variante B la verifica esterna locale (§4quater, che i test li esegue) resta obbligatoria accanto al bot? Consiglio: sì, per le fette che toccano il perimetro di review.

## Esito per fette

- **Fetta B1 — workflow `verifica-bot.yml` + `scripts/bot_esito.py` + 126 test**: FATTA. Bot su `pull_request_target` (definizione da main), Claude in sola lettura con `--setting-sources user`, cascata Fable 5.1 → Opus 5.5 → Opus 4.8 col token dell'abbonamento, approvazione con GitHub App dedicata legata allo SHA verificato. Decisione deterministica: APPROVE solo senza finding ALTA/MEDIA; PR che toccano la macchina del bot mai approvate; PR solo `reports/` approvate senza LLM (dosaggio); parte solo con l'etichetta `verifica`.
- **Riserve delle review #158/#159**: FATTA — R-158-1..4, cosmetica, R-159-1..4 chiuse con test prima del commit (soglia "sicurezza alta" dell'operatore).
- **Riserve review #160 (R-160-1, R-160-2, BASSE)**: DEFERITA — nella fetta B2, come da regola dell'operatore (le basse passano ma si aggiustano dopo).
- **Fetta B2 — `gasmerge --auto` + V-3 #127 + test di convalida**: DEFERITA — richiede B1 su main e il setup dell'operatore (la PR di B2 sarà la prima verificata dal bot).
- **Ruleset (1 approvazione, dismiss stale, last push approval)**: DEFERITA — dopo il test di convalida, altrimenti bloccherebbe ogni merge.
- **Verifica esterna §4quater**: lanciata dopo il push (verdetto nel prossimo handoff).

## Anomalie

- Il workflow non può girare prima del merge (`pull_request_target` usa la definizione di main): nessuna run reale verificata; actionlint non installato.
- Durante la prima sweep di mutation il mio harness si è fermato a metà lasciando `scripts/bot_esito.py` mutato (non in stage); ripristinato subito dal backup e confermato con `cmp`; harness rifatto con try/finally.
- Il token dell'abbonamento consuma la stessa quota dello sviluppo: il dosaggio (etichetta, doc-only senza LLM, cascata solo su errore) è nel workflow.
