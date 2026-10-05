# ULTIMO REPORT — 2026-10-05 — V-B vera, fetta B1: bot di verifica esterna su GitHub (+ correzioni delle due verifiche esterne #130)

## Decisioni umane richieste

1. Merge della PR #130 (https://github.com/Gasss23/Gas/pull/130) — variante A: `gasmerge 130`, digiti tu il numero.
2. Setup del bot (dopo il merge): passi numerati in `reports/setup_verifica_bot.md` — token dell'abbonamento, GitHub App `gas-verificatore`, environment `verifica-bot`. Serve prima del test di convalida (fetta B2).
3. **R-161-2**: con `scripts/` nella macchina del bot (V-5), la PR della fetta B2 (`gasmerge --auto`) il bot non la approverà mai; per provare un APPROVE automatico serve poi una PR fuori dalla macchina (es. una piccola fetta del motore).
4. **Terza verifica esterna non lanciata** (dosaggio): la seconda ha trovato una sola MEDIA con correzione proposta e provata da lei, applicata e revisionata (#162). Se la vuoi prima del merge, dimmelo.
5. **R-158-5**: il bot su GitHub è di sola lettura (non esegue test). In variante B la verifica esterna locale (§4quater, che i test li esegue) resta obbligatoria accanto al bot? Consiglio: sì, per le fette che toccano il perimetro di review.

## Esito per fette

- **Fetta B1 — workflow `verifica-bot.yml` + `scripts/bot_esito.py` + test (126, poi 164)**: FATTA. Bot su `pull_request_target` (definizione da main), Claude in sola lettura con `--setting-sources user`, cascata Fable 5.1 → Opus 5.5 → Opus 4.8 col token dell'abbonamento, approvazione con GitHub App dedicata legata allo SHA verificato. Decisione deterministica: APPROVE solo senza finding ALTA/MEDIA; PR che toccano la macchina del bot mai approvate; PR solo `reports/` approvate senza LLM (dosaggio); parte solo con l'etichetta `verifica`.
- **Riserve delle review #158/#159**: FATTA — R-158-1..4, cosmetica, R-159-1..4 chiuse con test prima del commit (soglia "sicurezza alta" dell'operatore).
- **Verifica esterna #130 (APPROVATO CON RISERVE, 2 MEDIA)**: FATTA — V-1 (il bot poteva scrivere file via `git --output`: tolto git), V-2 (un token nei finding finiva nella review pubblica: controllo su tutto il verdetto), V-3, V-4 (chiude anche R-160-2), V-5 (macchina del bot allargata a scripts/ e alla macchina di controllo; doc-only solo .md), V-6 (ordine del setup) chiuse prima del merge; commit `43f84fb`, review #161; 164 test, mutation 72/73.
- **Seconda verifica esterna #130 (APPROVATO CON RISERVE, 1 MEDIA)**: FATTA — V-1 (Grep/Glob leggevano fuori cartella: limitati a `./**` + scrub dell'ambiente), V-3, V-4, V-5 (etichetta nel setup), V-6 chiuse; commit `c215635`, review #162; 174 test, mutation mirata 10/10.
- **Riserve BASSE aperte (V-2 seconda verifica, R-161-1, R-162-1, R-162-2)**: DEFERITA — fetta B2 (le basse passano ma si aggiustano dopo).
- **Fetta B2 — `gasmerge --auto` + V-3 #127 + test di convalida**: DEFERITA — richiede B1 su main e il setup dell'operatore (la PR di B2 sarà la prima verificata dal bot).
- **Ruleset (1 approvazione, dismiss stale, last push approval)**: DEFERITA — dopo il test di convalida, altrimenti bloccherebbe ogni merge.
- **Verifica esterna §4quater**: FATTA due volte (handoff §8 e §9); la terza NON lanciata (vedi decisione 4).

## Anomalie

- Il workflow non può girare prima del merge (`pull_request_target` usa la definizione di main): nessuna run reale verificata; actionlint non installato.
- Durante la prima sweep di mutation il mio harness si è fermato a metà lasciando `scripts/bot_esito.py` mutato (non in stage); ripristinato subito dal backup e confermato con `cmp`; harness rifatto con try/finally.
- La CI di GitHub stasera ha runner in coda: due job sono stati cancellati dopo l'attesa (`unit-suite` su 43f84fb, `handoff-check` su 8e11aa5), nessun test fallito.
- Il token dell'abbonamento consuma la stessa quota dello sviluppo: il dosaggio (etichetta, doc-only senza LLM, cascata solo su errore) è nel workflow.
