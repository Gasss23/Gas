# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-12 — FETTA 1 cervello forte: budget ricontrollato prima di ogni chiamata (chiude F2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #191 (https://github.com/Gasss23/Gas/pull/191): verdetti APPROVATO CON RISERVE con sole BASSE/COSMETICHE → per la regola di CLAUDE.md decide l'operatore.
2. Al 1° giro il check `verifica-bot` è stato failure (SHA e9d1058) con verdetto testuale APPROVATO CON RISERVE senza ALTA/MEDIA: probabile falso positivo di `scripts/bot_esito.py` (macchina del bot: decide l'operatore). Al 2° giro (SHA 599e301): success.
3. Cervello forte, Fette 2–4: da discutere con l'operatore prima di qualunque codice.

NB: `gh` nel container non è autenticato (GH_TOKEN rifiutato); numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request` (`{"url":"https://github.com/Gasss23/Gas/pull/191"}`).

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #185**: `SALTATA — già mergiata dall'operatore il 2026-10-11 (20:56)`.
- **Fetta 1 — budget ricontrollato prima di ogni chiamata**: `FATTA` — `_budget_superato()` a inizio turno, prima di ogni `create` del ciclo agentico (anche il retry del Gemini 400) e prima di ogni rung di `rifletti()`; `turno_fine` con « ; motivo=budget». Test T88a–j, T88c2.
- **Fix dai verificatori della PR #191** (bot V-1/V-2 di due giri, verifica esterna V-2, revisore R-294-1/R-294-2/R-295-1): `FATTA`.
- **Fette 2–4 cervello forte**: `DEFERITA — l'operatore vuole discuterle prima`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 gas.py                             |  81 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------
 reports/diff_sessione.md           |   8 ++++++--
 reports/handoff.md                 | 198 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |  16 +++++++++++++---
 reports/ultimo_report.md           |  17 +++++++++++++----
 tests/test_unit_kernel.py          | 186 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 8 files changed, 470 insertions(+), 43 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
6cc7b10 fix(budget): stop di budget dichiarato anche sul retry Gemini, tentati onesti, rifletti (verificatori #191, 2° giro)
599e301 docs(fine-task): report e handoff aggiornati dopo i fix del bot #191
bfe0531 fix(budget): retry Gemini 400 sotto budget e motivo=budget nel diario (bot #191 V-1/V-2)
617ccf7 chore(revisore): memoria review #295 — APPROVATO CON RISERVE
d5be7de chore(revisore): memoria review #294 — APPROVATO CON RISERVE
e9d1058 docs(fine-task): report, handoff, stato e roadmap — FETTA 1 budget (PR #191)
8a50aae feat(budget): ricontrollo del budget prima di ogni chiamata (FETTA 1 cervello forte, chiude F2)
2bf657e chore(revisore): memoria review #293 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetto integrale del revisore per il commit `8a50aae` (gas.py, tests/test_unit_kernel.py), incollato:

## VERDETTO: APPROVATO CON RISERVE

Review #293. Ho esaminato il diff staged (gas.py, tests/test_unit_kernel.py) e ho rieseguito in locale tests/test_unit_kernel.py: 815 PASS / 0 FAIL, T88a–d verdi.

**Cosa ho controllato nel diff**
- `gas.py:1031` — nuovo `_budget_superato()`, punto unico del controllo sul budget. Rischio: leggere il log anche quando il budget non è impostato, oppure far nascere un crash. Esito: ok. Con il limite a 0 o non impostato restituisce None prima di chiamare `_daily_cost_usd`, che a sua volta non solleva mai eccezioni (gas.py:1026). Gli import Optional/Tuple sono già presenti (gas.py:18).
- `gas.py:3374` — controllo prima di ogni `chat.completions.create` del ciclo agentico. Rischio: fermare il turno lasciando la storia rotta (una richiesta di tool senza la sua risposta) o senza chiudere il turno. Esito: ok.
  - Il controllo arriva dopo il `_save_history()` dei risultati dei tool (gas.py:3465), quindi la storia finisce con l'ultima risposta del tool (T88b lo verifica).
  - Il `return` dentro il generatore passa dal `finally: _chiudi_turno()` (gas.py:3504).
  - Il ciclo da 10 iterazioni resta com'era, e `_get_window()` resta l'unica fonte della finestra.
  - Nessun taglio diretto della storia e nessuna simulazione di tool.
- `gas.py:3326` — controllo a inizio turno ora fatto tramite l'helper. Rischio: cambiare il comportamento esistente. Esito: ok, messaggio e `return` identici a prima.
- `gas.py:2733` — `rifletti()` ricontrolla il budget prima di ogni provider della cascata. Rischio: cambiare `provider_atteso` quando il budget è già superato all'inizio. Esito: ok. Il controllo sta prima dell'assegnazione, quindi resta None come prima; se il budget scatta prima del secondo provider, vale il primo, ed è corretto.
- `tests/test_unit_kernel.py:8164` — T88a–d. Rischio: test che passano anche senza il controllo nuovo. Esito: ok.
  - T88a pretende una sola chiamata; senza il controllo nel ciclo ce ne sarebbero 2 o più.
  - T88c fa da controprova (30 chiamate quando il budget non è impostato).
  - T88d copre il rung successivo nella riflessione.
  - Ogni test usa una cartella temporanea nuova, quindi il log costi non passa da un test all'altro. Le variabili d'ambiente e `gas.OpenAI` vengono ripristinati nel `finally`.

**Riserve (numerate)**
1. R-293-1 (BASSA, prestazioni) — `gas.py:1031`: quando il budget è impostato, `_daily_cost_usd` rilegge tutto il log JSONL dei costi a ogni iterazione. Sono fino a circa 30 letture per turno (10 iterazioni × 3 provider), più una lettura doppia all'iterazione 0, perché ripete il controllo di inizio turno. Peggiora la riserva già aperta R-tel-budget-perf (log che cresce). Senza budget impostato non costa nulla.
2. R-293-2 (BASSA, da dichiarare) — `gas.py:3374`: lo stop a metà turno blocca anche i provider gratuiti (openrouter/ollama, che costano 0). È coerente con il controllo di inizio turno, ma va scritto in roadmap/stato come scelta voluta.
3. R-293-3 (COSMETICA) — `tests/test_unit_kernel.py:8176`: il commento di `_Client88` dice «≥ 1,5 $» per chiamata, ma su flash-lite il test misura 1,00 $. Il test non cambia esito.

**Cosa NON ho verificato**
- Il comportamento con un provider vero e un log costi di dimensione reale (VPS, mesi di righe): non è riproducibile in dev. Il costo di R-293-1 è stimato, non misurato.
- La semantica del retry singolo del Gemini 400: è fuori dal diff, e ritentare la stessa chiamata senza un nuovo controllo mi sembra accettabile.
- Non ho verificato che `reports/roadmap.md` chiuda davvero la riserva F2: è un aggiornamento dei report, a carico dell'agente.

**Memoria**
Ho aggiunto la riga #293 e una lezione nuova in /home/user/Gas/.claude/agents/memoria_revisore.md. Commit atomico fatto: 2bf657e. Il diff staged del motore è intatto.

Nota dell'agente: R-293-3 corretta prima del commit (commento «≥ 1 $»); il marcatore di review è stato rigenerato sul diff con la correzione.

Verdetto integrale del revisore per il commit `bfe0531` (review #294, sul primo diff dei fix del bot), incollato:

## VERDETTO: APPROVATO CON RISERVE

Ho fatto le tre letture obbligatorie: CLAUDE.md (sez. 5), reports/stato_progetto.md (letto con Grep su budget/FETTA 1) e la mia memoria (ultima review #293). Il diff staged tocca 2 file, +45 righe. La suite kernel l'ho rieseguita io: **818 PASS / 0 FAIL**. T88e, T88c2 e T88f passano.

Elementi del diff esaminati:
- `gas.py:3403` — prima del retry singolo del Gemini 400 adesso si chiama `_budget_superato()`. Se il budget è superato, si scrive un warning nel log e si rilancia l'eccezione originale. Rischi esaminati:
  - Il 400 rilanciato poteva sfuggire al ciclo: no, finisce nello stesso `except` di provider di oggi (§9 rispettato).
  - Il rung successivo poteva partire lo stesso: no, il controllo prima della create dell'iterazione 0 (`gas.py:3377`) ferma il turno con l'errore dichiarato.
  - Il percorso senza budget poteva cambiare: no, `_budget_superato` restituisce None senza leggere il log, quindi è invariato.
  - Esito: ok.
- `gas.py:3290` — `_chiudi_turno` aggiunge « ; motivo=budget» quando `_turno_budget` è vero. Rischi esaminati:
  - La closure legge il valore al momento della chiamata, nel `finally`, e non serve `nonlocal` perché la variabile si legge soltanto: ok.
  - Il flag viene alzato su tutti e due gli stop (`gas.py:3330` inizio turno, `gas.py:3379` metà turno), sempre prima del `return`: ok.
  - Nessuno legge `turno_fine` scomponendolo: ho cercato con grep `classe=`, `tentati=` e `split(" ; ")` in gas.py, modules e scripts, zero risultati. Il suffisso in coda non rompe niente: ok.
- `gas.py:3273` — il flag è inizializzato a False insieme agli altri contatori del turno, prima della definizione della closure — ok.
- `tests/test_unit_kernel.py:8255` — T88f usa la sequenza None (inizio turno), None (iterazione 0), superato (retry). Se tolgo il controllo sul retry, la sequenza produrrebbe 2 create e il test cadrebbe sulla condizione `len(chiamate)==1`, quindi il test morde. Verifica anche un solo evento di errore, cioè nessun doppio messaggio — ok.
- `tests/test_unit_kernel.py:8219` e `tests/test_unit_kernel.py:8231` — T88e e T88c2 sono una coppia prova/controprova. Un flag sempre vero farebbe cadere T88c2, un flag mai alzato farebbe cadere T88e — ok.

Finding:
1. **R-294-1 (BASSA)** — Il retry saltato (`gas.py:3403`) ferma il turno con lo stop dichiarato solo se dopo c'è un rung che arriva al ciclo. Se il rung Gemini è l'ultimo che parte (gli altri sono saltati per chiave mancante o per la classificazione), il turno chiude con «Pipeline esausta» e il motivo «400». `_turno_budget` resta False, quindi niente motivo=budget né nel diario né nel messaggio. Il caso è raro e non rompe nulla, ma la diagnosi esce imprecisa. Come rimedio basterebbe alzare `_turno_budget = True` anche nel ramo del retry saltato. Senza test.
2. **R-294-2 (COSMETICA)** — `tests/test_unit_kernel.py:8252`: T88f rimette a posto `gas.OpenAI = _Client88` fuori da un try/finally. Se `run_turn` lanciasse un'eccezione, i test successivi girerebbero col client finto che fa sempre 400.

Rischio escluso: non ho verificato il comportamento con un vero 400 di Gemini e un budget reale sul log JSONL. Il ramo l'ho provato solo col doppio finto e l'override di `_budget_superato` (T88f): non è riproducibile in dev senza chiavi e senza spesa.

Memoria: ho aggiunto la riga #294 in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata con `scripts/commit_memoria_revisore.sh` (commit d5be7de). Nessuna lezione nuova oltre ai finding.

Riserve da tracciare in reports/stato_progetto.md: R-294-1 e R-294-2.

Verdetto integrale del revisore per il commit `bfe0531` (review #295, ri-review con R-294-1/R-294-2 corrette: è il diff effettivamente committato), incollato:

## VERDETTO: APPROVATO CON RISERVE

Review #295: ri-review della PR #191 sul diff staged (gas.py +12, tests/test_unit_kernel.py +39). Prima della review ho letto CLAUDE.md, la parte di reports/stato_progetto.md che riguarda la PR e la mia memoria (.claude/agents/memoria_revisore.md, fino alla #294).

**Elementi del diff esaminati**
1. `gas.py:3404` — nel retry del Gemini 400 saltato per budget, `_turno_budget = True` viene messo prima del `raise`. Rischio esaminato: il flag potrebbe non arrivare alla chiusura del turno, cioè al diario, perché viene assegnato dentro l'`except` di un generatore. Esito **ok**: l'assegnazione sta nel corpo di `run_turn` (`gas.py:3263`), non in una funzione annidata. Quindi `_chiudi_turno` (`gas.py:3275`) la legge per closure senza bisogno di `nonlocal`. Il budget non torna indietro durante il turno, quindi il flag non può essere falso. Se Gemini è l'ultimo rung, il turno chiude con «Pipeline esausta» e `motivo=budget`: R-294-1 è chiusa per lettura del codice.
2. `gas.py:3290` — aggiunge « ; motivo=budget» a `turno_fine` solo se il flag è vero. Rischio esaminato: falsi positivi su turni senza stop per budget. Esito **ok**: T88c2 lo prova (turno_fine senza motivo, riprodotto).
3. `gas.py:3330` e `gas.py:3379` — il flag viene alzato anche negli altri due punti di stop (inizio turno e metà turno), prima di `yield`/`return`. Esito **ok**: T88e passa e mostra `esito=ko … ; motivo=budget`.
4. `tests/test_unit_kernel.py:8256` — il ripristino di `gas.OpenAI = _Client88` è ora nel `finally`. Rischio esaminato: un'eccezione dentro `run_turn` lascerebbe il client finto attivo e contaminerebbe i test successivi. Esito **ok**: R-294-2 è chiusa.
5. `tests/test_unit_kernel.py:8263` — T88g controlla che `turno_fine` finisca con `motivo=budget` dopo il retry saltato. Esito **riserva** (vedi R-295-1): nello scenario il rung successivo (gemini-flash) alza comunque il flag dalla riga 3379, quindi T88g resterebbe verde anche senza la riga 3404. Copre il percorso dall'inizio alla fine, ma non morde il fix specifico. L'autore lo ha dichiarato onestamente.

**Riserve**
- **R-295-1 (BASSA)**: nessun test con Gemini ultimo rung che riesce a partire, cioè con gli altri rung senza chiave. È l'unico scenario in cui la riga `gas.py:3404` fa la differenza. Da tracciare in stato_progetto.md.

**Verifiche eseguite**
- Kernel riprodotto: **819 PASS / 0 FAIL**. T88a, T88b, T88c, T88c2, T88d, T88e, T88f e T88g tutti PASS.
- Wall of Shame: nessuno slicing della storia e nessuna simulazione di output dei tool nel diff.
- Guardrail: cap di 10 iterazioni e `_get_window` non toccati. Fail-safe §9 rispettato: il `raise` resta dentro il try del provider, quindi si passa al rung successivo.

**Rischio escluso**: non ho fatto la mutation (togliere la riga 3404 e rilanciare la suite) né provato davvero lo scenario «Gemini ultimo rung». Il comportamento del caso R-294-1 è verificato per lettura del codice, non eseguito. Comportamento su VPS e con provider reali non verificato: non riproducibile in dev.

**Memoria**: aggiunta la riga #295 in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola con 617ccf7 tramite scripts/commit_memoria_revisore.sh. Il diff staged del motore non è stato toccato. Nessuna lezione nuova.

Verdetto integrale del revisore per il commit `6cc7b10` (review #296, correzioni del 2° giro dei verificatori), incollato:

## VERDETTO: APPROVATO CON RISERVE

Review #296, PR #191 (FETTA 1 budget, correzioni del 2° giro dei verificatori). Letture fatte prima della review: CLAUDE.md, reports/stato_progetto.md (righe R-293/R-295) e memoria_revisore.md (#293–#295). Kernel rieseguito: 822 PASS / 0 FAIL.

**Elementi esaminati**
1. gas.py:3409 — retry del 400 Gemini con budget superato: ora c'è `yield _errore_budget_meta_turno(_sup)` + `return` al posto del `raise`. Rischi controllati:
   - un `yield` dentro un `except` di un generatore: il `finally` con `_chiudi_turno` gira comunque, anche se il generatore viene chiuso;
   - `_turno_budget` resta True, quindi il diario scrive motivo=budget;
   - nessun «Pipeline esausta … HTTP 400» quando Gemini è l'ultimo rung.

   Esito: ok. Chiude R-295-1 (coperto da T88i; l'autore dichiara che la mutazione fa fallire il test, io non l'ho ripetuta).
2. gas.py:3362 e gas.py:3390 — `_chiamato_rung` riparte da False a ogni rung e diventa True subito prima della prima create. Il pop si fa solo se il rung non ha mai chiamato. Rischio controllato: un pop che toglie il rung sbagliato. Non succede: l'unico append è subito prima, quindi l'ultimo elemento è sempre questo rung. Un rung che ha già fatto una create e viene fermato a un'iterazione successiva resta tra i tentati, come deve. Esito: ok. **Mutazione verificata da me**: con `pop()` sostituito da `pass`, T88h FALLISCE (821/1). File poi ripristinato, working tree pulito.
3. gas.py:3296 — closure `_errore_budget_meta_turno`: testo identico al precedente, type hint presenti. Esito: ok.
4. gas.py:2729 — in `rifletti()` il controllo del budget torna prima del controllo della chiave. Con budget superato e nessuna chiave l'errore torna «budget esaurito»; `provider_atteso` non cambia. Esito: ok (T88j PASS).
5. tests/test_unit_kernel.py:8265 (T88h), tests/test_unit_kernel.py:8295 (T88i), tests/test_unit_kernel.py:8326 (T88j) — `gas.OpenAI` e `GROQ_API_KEY` vengono ripristinati in `finally`. T88j toglie GEMINI/GROQ senza rimetterle, ma lo stesso blocco è già seguito dal `finally` di ripristino generale. Esito: ok.

**Wall of Shame**: nessuno slicing diretto della history, nessuna simulazione dell'output dei tool. Il cap di 10 iterazioni e `_get_window()` non sono toccati.

**Riserve**
- R-296-1 (COSMETICA): in `rifletti()` il budget ora si controlla anche per i rung senza chiave, quindi ci sono letture del log in più. Si somma a R-293-1, impatto trascurabile.

**Rischi esclusi**
- Comportamento con provider reali (Gemini che risponde 400 vero) non verificato: non riproducibile in dev senza consumare quota. Coperto solo dai mock T88f–i.
- La mutazione di T88j (ripristinare il vecchio ordine) non l'ho rieseguita. Verificata per lettura: con l'ordine vecchio il caso senza chiavi salta tutti i rung senza mai controllare il budget, quindi l'errore non sarebbe «budget esaurito».

**Memoria**
- Riga #296 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md.
- `bash scripts/commit_memoria_revisore.sh` NON è partito: l'hook review_gate.sh ha bloccato il comando perché `.claude/.review_ok` non corrisponde al diff staged.
- Cosa deve fare l'agente principale: dopo `bash scripts/segna_review_ok.sh`, lanciare lui lo script di commit della memoria, oppure includere il file nel commit di fine task.

Nota dell'agente: la memoria #296 è inclusa nel commit di fine task. Mutazione di T88i eseguita dall'agente: rimettendo il `raise` nel retry, T88i FALLISCE (821 PASS / 1 FAIL).

## §5 DELTA TEST DEL MOTORE

Kernel (locale) 811 → 822 PASS (+11: T88a–j, T88c2), 0 FAIL. Base 811 riverificata in una copia di lavoro al commit 89a51f3. In CI i numeri assoluti sono +2 (main 89a51f3: 813; 599e301: 821 con 819 locali). pytest locale: `1032 passed in 122.09s (0:02:02)` (eseguito prima dei fix dei verificatori; dopo i fix rieseguita solo la suite kernel).

```
=== RIEPILOGO: 822 PASS, 0 FAIL ===
```

## §6 STATO CI

`gh` non autenticato nel container: stato letto con lo strumento GitHub MCP (`actions_list`) e dai verdetti dei verificatori:

```
CI           run 886          push  8a50aae  completed (handoff-check failure: commit intermedio prima del fine-task)
CI           run 38244165640  push  e9d1058  completed/success (unit-suite ✓ kernel 817/0, handoff-check ✓)
verifica-bot check 114794946156     e9d1058  completed/failure (verdetto testuale APPROVATO CON RISERVE)
CI           run 38245198595  push  599e301  completed/success (unit-suite ✓ kernel 821/0, handoff-check ✓)
verifica-bot run 38245204326        599e301  completed/success (APPROVATO CON RISERVE senza ALTA/MEDIA)
CI           run 885          push  89a51f3  completed/success
```

Mappatura commit→run:
- `8a50aae`: CI run 886 (handoff-check rosso, atteso prima del fine-task).
- `2bf657e`: nessuna run su questo SHA (pushato insieme a 8a50aae).
- `e9d1058`: CI run 38244165640, success.
- `d5be7de`, `617ccf7`, `bfe0531`: nessuna run su questi SHA (pushati insieme a 599e301).
- `599e301`: CI run 38245198595, success.
- `6cc7b10`: run non ancora disponibile alla scrittura dell'handoff.
- commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-293-1 (BASSA): rilettura del log costi a ogni chiamata con budget impostato (cache prima della Fetta 2).
- R-293-2 (BASSA, scelta dichiarata in roadmap): lo stop ferma anche i rung gratuiti.
- R-296-1 (COSMETICA): letture del log in più in `rifletti()` per i rung senza chiave.
- Verifica esterna #191 V-4 (COSMETICA): «a metà turno» anche all'iterazione 0 del rung successivo.
- Note cosmetiche sui numeri dell'handoff (il file si conta da solo).
