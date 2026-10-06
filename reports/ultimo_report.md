# ULTIMO REPORT — 2026-10-06 — Notte cloud: fetta B2 (PR #131) + arretrati (PR #132–#136)

## Riepilogo per l'operatore

- **#131 B2** (check `verifica-bot` dell'App, `gasmerge --auto`, R-163-1/R-163-4 chiuse) — kernel 651/0, pytest 588; review #165 APPROVATO; verifica esterna APPROVATO CON RISERVE con **V-1 MEDIA = decisione tua** (vedi sotto). **Merge: sì, dopo aver deciso V-1** (manuale: tocca `scripts/`).
- **#134 gate IP + gate di review** (`LC_ALL=C read`: in locale UTF-8 un byte non UTF-8 faceva passare un IP e un file del perimetro senza review — 2 fail-open reali su main) — 281 passed in C e C.UTF-8; review #179 APPROVATO; due verifiche esterne APPROVATO CON RISERVE (solo basse). **Merge: sì, PRIORITARIO**; secondo passaggio in chat claude.ai (fetta di sicurezza).
- **#133 R-150-1** (push fallito in fine-task: messaggio ed exit 1) — hooks 103; review #168 APPROVATO; verifica APPROVATO CON RISERVE (basse). **Merge: sì.**
- **#135 F-mac-2** (docstring raw + guardia T79a su tutti i .py, anche su 3.11 della CI) — kernel 652/0 su 3.11 e 3.13; review #176 APPROVATO; verifica APPROVATO CON RISERVE (V-2 chiusa). **Merge: sì.**
- **#136 F-mac-1** (sul Mac la suite kernel passa da 5 FAIL a 0; sandbox esigito in CI) — 653/0 con bwrap, 648/0 senza; review #175 APPROVATO; verifica APPROVATO CON RISERVE (basse). **Merge: sì**, poi conferma sul Mac.
- **#132** (archivia la certificazione Mac della #87, solo doc) — **Merge: sì**, poi chiudi #87. **#109**: superata da `fine_task_finale.sh`, da chiudere (non toccata). Ordine: ogni PR riscrive `reports/` → dopo il primo merge le altre vanno riallineate a main (lo faccio io su richiesta).

## Decisioni umane richieste

1. **V-1 verifica esterna #131 (MEDIA)**: oggi un sì del bot su una PR che tocca la macchina del bot → `neutral`, che **soddisfa** il check richiesto del ruleset: quella PR si può mergiare dal browser (o da chiunque abbia il token) senza `gasmerge`. Opzioni: (a) tenere così (decide l'operatore, come da tua indicazione; il rischio si chiude con G-3, agente non admin); (b) OPERATORE → `action_required`/`failure`: blocca davvero, ma poi ogni PR sulla macchina richiede un bypass del ruleset da parte tua. Consiglio: (a) + G-3 come prossima fetta.
2. Merge delle PR #131–#136 (nessun merge fatto dall'agente), nell'ordine consigliato: #134, #133, #135, #136, #132, #131.
3. **R-163-2** (BASSA): NO del bot legato allo SHA, non al tree. **R-158-5**: §4quater locale resta accanto al bot? Consiglio: sì.
4. Setup del bot (`reports/setup_verifica_bot.md`): App con **Checks R/W**, etichetta `verifica` creata da te a setup finito, §F ruleset col check dell'App.
5. Verdetto integrale della review #163 non disponibile (dato nella sessione locale): in handoff c'è la riga della memoria del revisore.

## Esito per fette

- **B2 — R-163-1 (MEDIA)**: FATTA (`a79cb07`). **R-163-4**: FATTA. **R-163-2**: DEFERITA (decisione umana). **R-163-3**: FATTA (dichiarata). **R-164-1/2**: FATTA; R-164-3 dichiarata.
- **B2 — setup_verifica_bot.md, fine-task §4quater (etichetta), stato_progetto.md**: FATTA.
- **B2 — verifica esterna #131**: FATTA — APPROVATO CON RISERVE (handoff §8): V-1 MEDIA → decisione 1; V-2 (handoff fotografato prima dell'ultimo commit) strutturale; V-3 = R-163-2; V-4 = #163 mancante.
- **Arretrato R-150-1**: FATTA → PR #133.
- **Arretrato V-2 #124/#125 (latin1 su glibc)**: FATTA → ha rivelato 2 fail-open, PR #134 (+ V-2/V-3 della sua verifica, R-177/R-178).
- **Arretrato F-mac-2**: FATTA → PR #135. **F-mac-1**: FATTA → PR #136.
- **PR vecchie #87 e #109**: valutate, non toccate; contenuto della #87 archiviato → PR #132.
- **V-2 #127, R-162-1, R-162-2**: DEFERITA — toccano `gasmerge.sh`/`verifica-bot.yml` riscritti da B2: da fare dopo il merge di #131.
- **F-sessionend-msg** (cosmetico, `settings.json`): DEFERITA — costo review+fine-task sproporzionato.
- **G-3 (agente non admin)**: DEFERITA — fetta separata per tua indicazione.
- **Etichetta `verifica` sulle PR**: SALTATA — `gh` non autenticato e l'etichetta non esiste ancora.

## Anomalie

- `gh` CLI non autenticato nel container: PR, CI e ruleset letti/creati via connettore GitHub.
- Numerazione review: le review sono numerate #163–#179 su branch diversi; la #166 era stata numerata #163 dal revisore e rinumerata (dichiarato nei rispettivi handoff). Al merge le righe di `memoria_revisore.md` confliggono (si tengono tutte).
- `stato_progetto.md` è ~505 righe (CLAUDE.md §11 chiede ~100): snellirlo è una fetta a sé, non fatta.
