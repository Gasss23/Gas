# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — Chat Motore: R7 R-c4b3-3 (esito della firma recuperato), riserve finali di #241, resoconto di spesa e stato nel messaggio del mattino (R1), contatti fermi in `ricorda` (R1) — PR #241

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #241 (https://github.com/Gasss23/Gas/pull/241; numero e URL dall'esito reale di `create_pull_request` via MCP GitHub, `gh` non autenticato nella sessione cloud): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10).
2. Fetta che tocca la firma: secondo passaggio nella chat claude.ai con il link della PR.
3. Cose dell'operatore messe da parte: `reports/da_mergiare.md`, sezione «Da fare domattina».

---

## §1 SCOPE & ESITO FETTE

- **R-c4b3-3 (roadmap R7)**: `FATTA` — review #445/#446 APPROVATO CON RISERVE, #447 APPROVATO.
- **Merge di main (PR #242 chat Mani)**: `FATTA` — review #449 APPROVATO.
- **Riserve di #241 (V-1 bot, V-1/V-2 verifica esterna)**: `FATTA` — review #450/#451 APPROVATO CON RISERVE (chiuse), #452 APPROVATO.
- **R1 resoconto di spesa e stato**: `FATTA` — review #453/#454 APPROVATO CON RISERVE.
- **R-445-3**: `DEFERITA — COSMETICA, preesistente, fetta successiva`.
- **R1 contatti fermi (`ricorda fermi=true`, catalogo d'esempio)**: `FATTA` — review #455 APPROVATO CON RISERVE, #456 APPROVATO.
- **Merge di main (PR #243 chat Mani, conflitto segnalato dalla verifica esterna 2° giro, V-0)**: `FATTA` — review #457 APPROVATO.
- **V-1 verifica esterna #241 2° giro (`fermi` normalizzato anche dentro `_ricorda`)**: `FATTA` — review #458 APPROVATO.
- **Riserve del bot su 5f4c524 (V-1 righe rotte del log solo nelle 24 ore, V-5 testo dell'esito incerto)**: `FATTA` — review #459 APPROVATO CON RISERVE (chiuse), #460 APPROVATO. V-2 (segno nel DB al posto della scansione della storia): `DEFERITA — cambio di schema`.
- **V-1/V-2 verifica esterna e bot #241 (spesa del mattino a log rotto, tetto mostrato)**: `FATTA` — nella stessa fetta (#455/#456); descrizione della PR aggiornata (V-2 bot).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |  20 +++++++++++++
 gas.py                              | 131 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 modules/notte/notte.py              | 167 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
 modules/telegram/bot.py             |  16 ++++++++--
 reports/da_mergiare.md              |  32 ++++++++++----------
 reports/diff_sessione.md            |  17 ++++++-----
 reports/handoff.md                  | 589 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------
 reports/roadmap.md                  |   8 ++---
 reports/stato_progetto.md           |   5 ++--
 reports/ultimo_report.md            |  42 +++++++++++---------------
 scripts/notte/catalogo_esempio.yaml |   5 ++--
 tests/test_unit_kernel.py           | 210 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_notte.py            | 126 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 13 files changed, 1118 insertions(+), 250 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
801532b fix(notte): righe rotte del log contate solo nelle 24 ore; testo dell'esito incerto (V-1/V-5 bot #241)
6726ee7 chore(revisore): memoria review #460 — APPROVATO
a965355 chore(revisore): memoria review #459 — APPROVATO CON RISERVE
a57a16a docs(fine-task): report e handoff — merge di main #243 e V-1 verifica esterna (#241)
b0c5566 fix(memoria): fermi normalizzato anche dentro _ricorda (V-1 verifica esterna #241, 2° giro)
e7ccb22 chore(revisore): memoria review #458 — APPROVATO
03488e4 Merge remote-tracking branch 'origin/main' into feat/merge-automatico-z1xjx2
5f4c524 docs(fine-task): report e handoff — contatti fermi in ricorda, spesa del mattino onesta (#241)
3c136d4 feat(memoria): ricorda fermi=true — lead attivi dal più fermo (R1); spesa del mattino onesta
ebaf9f3 chore(revisore): memoria review #456 — APPROVATO
e8e7fc8 chore(revisore): memoria review #455 — APPROVATO CON RISERVE
075e323 docs(fine-task): report e handoff — riserve di #241 e resoconto del mattino R1 (#241)
0037522 feat(notte): resoconto di spesa e stato nel riepilogo del mattino (R1)
3b988f6 chore(revisore): memoria review #454 — APPROVATO CON RISERVE
1f0a2e9 chore(revisore): memoria review #453 — APPROVATO CON RISERVE
c82875f fix(firma): riserve finali di #241 — testo del recupero, log, guardia «un click alla volta»
c8ac93d chore(revisore): memoria review #452 — APPROVATO
4fdc3dd chore(revisore): memoria review #451 — APPROVATO CON RISERVE
6ab3ee0 chore(revisore): memoria review #450 — APPROVATO CON RISERVE
ee0b4d7 Merge remote-tracking branch 'origin/main' into feat/merge-automatico-z1xjx2
eafe6ee docs(fine-task): report e handoff — R7 R-c4b3-3 esito della firma recuperato (#241)
079c879 fix(firma): esito recuperato in storia dopo un'interruzione tra reclamo e storia (R7, R-c4b3-3)
ad1ab5e chore(revisore): memoria review #447 — APPROVATO
d48d453 chore(revisore): memoria review #446 — APPROVATO CON RISERVE
8c4e11c chore(revisore): memoria review #445 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #445 (chat Motore)

## VERDETTO: APPROVATO CON RISERVE

Review #445 (chat Motore). Diff in staging su feat/merge-automatico-z1xjx2: gas.py, modules/telegram/bot.py, tests/test_unit_kernel.py. Ho letto CLAUDE.md, lo stato del progetto (R-c4b3-3 alla riga 407) e la mia memoria. Ho rieseguito la suite del kernel: **1006 PASS, 0 FAIL**.

**Elementi del diff esaminati**
- `gas.py:3373` — `recupera_esito_firma`. Rischio esaminato: una seconda esecuzione. La funzione non chiama mai `reclama_esecuzione` né `execute_tool_call`: legge il DB e scrive la storia, nient'altro. In memoria il blocco aggiunto è `user` + `assistant` senza tool_call e senza argomenti. La sonda con `write_file` e argomenti `SEGRETO`/`PAYLOAD` mostra che nessuno dei due finisce nella storia. Non viene simulato nessun output di tool (Wall of Shame rispettato) e `_get_window` non viene toccato. Esito: ok.
- `gas.py:3394` — esito NULL (crash a metà): scrive `[KO] interrotta dopo il reclamo: esito incerto` (la scrittura avviene solo se l'esito è ancora vuoto) e poi rilegge il DB. Rischio esaminato: sovrascrivere un esito già scritto da altri. Non succede, perché la UPDATE ha `esito IS NULL` (modules/memory/store.py:1929). Se l'eccezione arriva dopo la scrittura nel DB ma prima della storia, il click successivo ripete il recupero e lo classifica di nuovo INCERTO: comportamento idempotente. Esito: ok.
- `gas.py:3400` — la mappatura esito → stato guarda solo il prefisso `[KO]` e la parola «incert». Rischio esaminato: divergenza da `applica_firma`. **Sonda**: con l'esito `[OK] (non eseguito)`, cioè `run_command` in dry-run (gas.py:2295), il recupero restituisce `stato='finita', eseguita=True`. L'operatore riceverebbe «✅ Approvata ed eseguita» e il modello leggerebbe «il kernel l'ha eseguita», mentre `applica_firma` aveva detto non_partita. Esito: **riserva R-445-1**.
- `modules/telegram/bot.py:694` — se il reclamo c'è già, il bot chiama `recupera_esito_firma` attraverso `getattr`/`callable`; se il recupero restituisce None il comportamento resta identico a prima («Nessuna modifica»). Rischio esaminato: crash su un kernel senza il metodo. Il try/except esterno resta. Esito: ok.
- `tests/test_unit_kernel.py:8086` (T78l) — simula il crash con un kernel riavviato, poi verifica: nessuna esecuzione, esito INCERTO nel DB, blocco anche su disco, messaggio ⚠️, nessun duplicato al secondo click, round-trip §7 al turno dopo. Il test non è vacuo: il testo ⚠️ arriva solo dal nuovo ramo. Esito: ok.
- `tests/test_unit_kernel.py:8122` (T78m/T78n) — coprono i casi OK, KO, errore interno → incerta e i tre casi che restituiscono None. Esito: ok. Manca il caso dry-run: vedi R-445-1.

**Finding**
- **R-445-1 (chat Motore) BASSA**: con `[OK] (non eseguito)` (dry-run di run_command) `gas.py:3400` risponde «finita/eseguita». Si verifica solo se l'esito è nel DB ma non in storia: storia persa per un salvataggio fallito seguito da riavvio, oppure storia azzerata o compressa più un ri-click. Non provoca esecuzioni, ma l'informazione all'operatore e al modello è falsa. Correzione proposta: trattare `(non eseguito)` come non_partita, oppure salvare lo `stato` nel DB, più un test.
- **R-445-2 (chat Motore) BASSA**: l'ipotesi «il bridge gestisce un click alla volta» oggi è vera (`gestisci_callback` è sincrono, `applica_firma` ha un solo chiamante, modules/telegram/bot.py:756), ma sta solo nel docstring. Se domani arrivasse un handler concorrente, il recupero chiuderebbe come INCERTO un'esecuzione ancora in corso. L'esito vero perderebbe sia il DB (vince la prima scrittura) sia la storia (lo scarta il dedup). Non porta mai a una seconda esecuzione. Proposta: una riga di commento o un test di guardia accanto a `gestisci_callback`.
- **R-445-3 (chat Motore) COSMETICA, preesistente**: se il crash avviene dopo `_storia_esito_firma` ma prima di `registra_esito_esecuzione`, la storia contiene il blocco, il recupero restituisce None e l'esito nel DB resta NULL per sempre.

Nota di contesto: dopo un crash i bottoni sono già stati tolti (`editMessageReplyMarkup` arriva prima del reclamo). Quindi il percorso reale del ri-click è la riconsegna dell'update da parte di Telegram, il cui offset non era stato confermato. Il ramo nuovo serve davvero a questo.

**Rischi esclusi (non verificati)**
- Riconsegna reale dell'update da parte di Telegram dopo un crash: non riproducibile senza bot e token veri. L'ho ragionata, non provata.
- Due processi kernel/bot sulla stessa `.gas_history.json` (un problema già esistente e fuori da questa fetta).
- La mutazione del ramo nel bot l'ho valutata leggendo il codice, non eseguendola.

Memoria: riga #445 più una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md e committate da sole (commit 8c4e11c).

### Review #446 (chat Motore)

## VERDETTO: APPROVATO CON RISERVE

Review #446 (chat Motore): ri-review della #445 sul diff aggiornato in staging. La suite del kernel l'ho rieseguita io: **1007 PASS, 0 FAIL**.

**Elementi del diff esaminati**
- `gas.py:3401`: un esito che contiene «(non eseguito)» ora viene classificato non_partita e non più finita. Ho controllato se il caso dry-run viene ancora indicato come «eseguita». Non succede più: R-445-1 è chiusa. Ho poi controllato se la regola scatta su esiti di altri tool. Il controllo cerca il testo come **sottostringa** (`"(non eseguito)" not in esito`). Per i tool diversi da run_command l'esito è `[OK] <primi 160 caratteri dell'output>` (gas.py:2262). Prova eseguita: `_esito_diario("write_file", "File scritto: (non eseguito).txt")` restituisce `[OK] File scritto: (non eseguito).txt`, che il recupero classificherebbe «NON eseguita» anche se il file è stato scritto. Esito: **riserva R-446-1**.
- `modules/telegram/bot.py:754`: commento che fissa l'ipotesi «un click alla volta, niente thread qui» accanto a `gestisci_callback`, con l'avviso che un handler concorrente richiede di rivedere il recupero. Ho controllato se l'ipotesi è vera oggi: lo è, il chiamante è sincrono. R-445-2 è chiusa. Esito: ok.
- `tests/test_unit_kernel.py:8149`: T78m con dry-run, dove `[OK] (non eseguito)` dà non_partita e mai «eseguita». Il test non è vacuo: con il codice della #445 fallirebbe, come mostra la sonda della review #445. Esito: ok.
- `gas.py:3373`: `recupera_esito_firma` non ha altre modifiche. Valgono le conclusioni della #445: nessuna esecuzione, nessun argomento né output nel messaggio user, nessuna tool_call simulata, `_get_window` non toccato. Esito: ok.

**Finding**
- **R-446-1 (chat Motore) BASSA**: il confronto per sottostringa a `gas.py:3401` classifica «non eseguita» un'azione eseguita quando il testo dell'output (per esempio un path) contiene «(non eseguito)». Sbaglia nel verso meno sicuro: l'operatore potrebbe ripetere l'azione. Correzione proposta: `esito == "[OK] (non eseguito)"`, oppure tenere la regola solo per `tool == "run_command"`, più un test con write_file.
- **R-445-3 (chat Motore) COSMETICA**: resta aperta (problema che c'era già prima): se Gas si interrompe dopo aver scritto la storia ma prima di `registra_esito_esecuzione`, nel DB l'esito resta NULL per sempre.

**Rischi esclusi (non verificati)**
- Non ho provato una riconsegna reale dell'update da parte di Telegram dopo un crash: servono il bot e il token veri.
- Non ho cercato esiti reali di altri tool parcheggiabili che contengano davvero «(non eseguito)». La sonda con un path costruito apposta mostra che il caso è possibile, non quanto sia frequente.

Memoria: ho aggiunto la riga #446 con una lezione in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (commit d48d453).

### Review #447 (chat Motore)

## VERDETTO: APPROVATO

Review #447 (chat Motore). Ricontrollo della #446 sul diff in staging aggiornato: gas.py, modules/telegram/bot.py, tests/test_unit_kernel.py. Ho rieseguito io la suite del kernel: **1008 PASS, 0 FAIL**.

**Elementi del diff esaminati**
- `gas.py:3401` — la regola ora confronta l'esito per uguaglianza esatta: `esito != "[OK] (non eseguito)"`. Rischio esaminato: che un esito `[OK] <snippet>` di un altro tool venga scambiato per un'anteprima dry-run. Non succede più, perché l'unica stringa riconosciuta è quella che `_esito_diario` produce per run_command senza esecuzione (`gas.py:2295`). R-446-1 chiusa. Esito: ok.
- `tests/test_unit_kernel.py:8158` — T78m con write_file il cui esito `[OK] scritto (non eseguito).txt` resta finita/eseguita. Rischio esaminato: test che passa anche col codice sbagliato. Con il controllo per sottostringa della #446 questo test fallirebbe. Esito: ok.
- `tests/test_unit_kernel.py:8149` — T78m con dry-run `[OK] (non eseguito)`: deve dare non_partita, mai «eseguita». Rischio esaminato: tornare a R-445-1. Il test passa. Esito: ok.
- `gas.py:3373` — `recupera_esito_firma`, il resto è invariato. Rischi esaminati: seconda esecuzione, argomenti o output di terzi nel messaggio user, tool_call simulata, finestra della storia. Nessuna seconda esecuzione: non chiama mai il reclamo né `execute_tool_call`. Il blocco è user + assistant senza tool_call e senza argomenti: nessun output di tool simulato. `_get_window` non è toccato. Fail-safe §9: un'eccezione viene loggata e la funzione ritorna None. Esito: ok.
- `modules/telegram/bot.py:694` — se il reclamo c'è già, il bot chiama il recupero tramite `getattr` protetto. A `modules/telegram/bot.py:754` c'è il commento che fissa l'ipotesi «un click alla volta» (R-445-2 chiusa nella #446). Rischio esaminato: crash con un kernel senza il metodo. Esito: ok.

**Riserve aperte**
- **R-445-3 (chat Motore) COSMETICA**, già presente prima di questa fetta: se Gas si ferma dopo aver scritto la storia ma prima di `registra_esito_esecuzione`, l'esito nel DB resta NULL per sempre.
- Residuo teorico che accetto, senza aprire una riserva: se l'output di un tool diverso da run_command fosse esattamente «(non eseguito)», l'esito diventerebbe `[OK] (non eseguito)` e verrebbe classificato non_partita. Gli output di quei tool sono testo del kernel, quindi non è realistico.

**Rischi esclusi (non verificati)**
- Non ho provato la riconsegna reale dell'update da parte di Telegram dopo un crash, cioè il percorso vero del nuovo click: servono il bot e il token veri. L'ho ragionata e simulata solo coi test (T78l).
- Non ho controllato due processi kernel o bot sulla stessa `.gas_history.json`: è un problema che esisteva già ed è fuori da questa fetta.

Memoria: riga #447 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (commit ad1ab5e). Lezione nuova: nessuna.

### Review #449 (chat Motore)

## VERDETTO: APPROVATO

**Esito:** il merge è corretto. Non ho trovato righe perse, né differenze rispetto a main nei file del motore.

Review #449 (chat Motore). Merge di origin/main e3ffc0a (PR #242, chat Mani, fetta 5 web) dentro feat/merge-automatico-z1xjx2, con HEAD eafe6ee. La base comune è 739dfa8.

**Elementi esaminati.** Le citazioni sono prese dal diff di sessione dopo il merge (base = e3ffc0a), come da lezione #444.
- `gas.py:3401` — è la condizione che riconosce il dry-run per uguaglianza esatta (R-446-1). Rischio esaminato: che il merge alteri il lavoro del motore già revisionato. `git diff --cached HEAD` su gas.py è vuoto, quindi resta identico a HEAD. Esito: ok.
- `tests/test_unit_kernel.py:8149` — è T78m (dry-run → non_partita). Rischio esaminato: che il merge alteri o perda i test di R-c4b3-3. È identico a HEAD, nessun marcatore di conflitto. Esito: ok.
- `modules/telegram/bot.py:694` — è il recupero dell'esito via getattr quando l'esecuzione è già reclamata. Rischio esaminato: che main tocchi il bridge Telegram. È identico a HEAD, e main non lo tocca. Esito: ok.
- `modules/web/leggi.py` e `tests/test_unit_web_leggi.py` (file portati da main, nominati senza riga perché escono dal diff di sessione). Rischio esaminato: differenze introdotte nella risoluzione. `git diff --cached e3ffc0a` dà 0 righe, e il worktree coincide con l'index. `pytest tests/test_unit_web_leggi.py` sul tree unito dà 167 passed. Esito: ok.
- `.claude/agents/memoria_revisore.md` e `reports/stato_progetto.md`. Rischio esaminato: righe perse o duplicate nella risoluzione per unione. Ho fatto un confronto a multinsieme fra base, ours e theirs contro l'index: 0 righe mancanti, 0 righe in più, nessun marcatore. In stato_progetto ci sono sia R-c4b3-3 CHIUSA (chat Motore) sia la fetta 5 Mani con la parte (a) di R-447-1 chiusa (R-448-2). Esito: ok.
- Il diff di sessione rispetto a main contiene solo gas.py, modules/telegram/bot.py, tests/test_unit_kernel.py e reports/. È il lavoro già revisionato nelle #445-#447 (chat Motore). Nessun antipattern del Wall of Shame introdotto: il merge non aggiunge codice nuovo.

**Rischio escluso:**
- Non ho rieseguito la suite del kernel: ho preso per buono il tuo 1008 PASS. gas.py, bot.py e test_unit_kernel.py sono identici a HEAD, già verificati nella #447.
- Non ho verificato il contenuto dei report di sessione (ultimo_report, handoff, diff_sessione) tenuti nella versione del ramo, perché si riscrivono a fine task.

**Memoria — attenzione:** la riga contatore #449 (chat Motore) è scritta in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` ma NON è committata. Lo script `scripts/commit_memoria_revisore.sh` ha fallito con exit 0, e in gas_debug.log c'è il warning «fatal: cannot do a partial commit during a merge». Lo staging del merge è intatto: la memoria compare come `MM`, cioè la versione unita è nello staging e la riga #449 solo nel worktree. Dopo il commit del merge, fai `git add` del file (o rilancia lo script) per committare la riga.

### Review #450 (chat Motore)

## VERDETTO: APPROVATO CON RISERVE

Review #450 (chat Motore). Ho letto CLAUDE.md, le voci di reports/stato_progetto.md su R-c4b3-3 e R-445-3 e la coda di .claude/agents/memoria_revisore.md. Ho esaminato il diff staged su 3 file.

**Elementi esaminati**
- `gas.py:3404` — in `recupera_esito_firma`, la notizia del ramo «finita» non dà più per certa la causa: ora dice «interruzione o errore interno». Ho controllato che la logica dei rami (finita / incerta / non partita) e il flag `eseguita` non cambino: cambia solo il testo, e nessun test cerca la vecchia frase. — ok
- `modules/telegram/bot.py:696` — in `_riprova_orfana`, se il kernel non ha `recupera_esito_firma` ora scrive un `log.warning` e restituisce `(None, motivo)`, come prima. Il comportamento resta lo stesso e l'eccezione è ancora gestita dal try/except esterno (§9). Prova di mutazione in una copia del repo: tolto il log, T78o fallisce (1009 PASS, 1 FAIL), quindi il test morde. — ok
- `tests/test_unit_kernel.py:8187` — T78p, controllo sull'AST di bot.py. Ho provato 8 varianti di bot.py nella copia. Il controllo fallisce, come deve, con: `threading.Thread(target=_handle_update)`, `ThreadPoolExecutor().submit(_handle_update, …)`, pool con lambda, Thread con lambda, `asyncio.to_thread(_handle_update, …)` e un pool dentro `_handle_update` per `gestisci_callback`. Sul codice attuale passa: `[] ['_invia_a_tutti']`. — riserva (vedi R-450-1)
- `modules/telegram/bot.py:445` (contesto) — il ciclo di polling chiama `_handle_update` direttamente, uno alla volta: l'ipotesi «un click alla volta» oggi è vera. — ok

**Riserve**
- **R-450-1 BASSA** — Il controllo T78p non vede un pool creato a livello di modulo (es. `_POOL = ThreadPoolExecutor(4)` vicino agli import) e poi usato così: `_POOL.submit(lambda: _handle_update(...))`. Con questa variante il test PASSA. Motivo: `_pool78p` cerca i costruttori di thread solo dentro le `FunctionDef`. Correzione: cercare i costruttori in tutto il modulo e richiedere che compaiano solo dentro `_invia_a_tutti`.
- **R-450-2 COSMETICA** — Il tag «V-1 bot #241» (`gas.py:3405`) sta DENTRO la stringa della notizia, che finisce in storia e arriva al modello. Va spostato in un commento.
- La riga `gas.py:3404` è lunga 107 caratteri. Nel file ce ne sono già altre oltre 100, quindi è solo una nota.

**Wall of Shame**: nessuno slicing della history, nessuna simulazione di output dei tool. `_get_window`, il cap di 10 iterazioni e il cap degli 8k non sono toccati.

**Prove**: suite del kernel 1010 PASS, 0 FAIL (T78o e T78p PASS). Mutazioni come sopra.

**Rischio escluso**: non ho rilanciato `pytest tests/` per intero (1892 passed lo dichiari tu). Non ho verificato il comportamento reale su Telegram/VPS con callback concorrenti: non si riproduce in dev, e T78p è solo un controllo statico. R-445-3 resta deferita, fuori dal diff.

**Memoria**: aggiunte la riga contatore #450 e una lezione in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole con 6ab3ee0. Il diff staged non è stato toccato.

### Review #451 (chat Motore)

## VERDETTO: APPROVATO CON RISERVE

Review #451 (chat Motore). È la ri-review della #450 sullo stesso diff staged (gas.py, modules/telegram/bot.py, tests/test_unit_kernel.py). Prima della review ho letto CLAUDE.md, la parte di reports/stato_progetto.md che riguarda queste riserve e la coda di .claude/agents/memoria_revisore.md.

Elementi del diff esaminati:
- gas.py:3403 — il tag «V-1 bot #241» è passato in un commento sopra la notizia, nel ramo 'finita' di recupera_esito_firma. Rischio esaminato: tag di processo dentro una stringa che finisce in storia e arriva al modello. La stringa in gas.py:3404 adesso è pulita. Ho controllato anche l'altra notizia «finita» in gas.py:3343: non ha tag. Esito: ok, R-450-2 chiusa.
- tests/test_unit_kernel.py:8197 — T78p ora cerca i costruttori di thread e pool in tutto il modulo. Li attribuisce alla funzione che li contiene, oppure a "<modulo>" se sono fuori da ogni funzione, e conta anche to_thread e run_in_executor. Rischio esaminato: un pool a livello di modulo che non viene visto. Ho rifatto la guardia in uno script a parte e l'ho mutata:
  - pool a livello di modulo con submit(lambda: _handle_update(u)): FAIL (['<modulo>', '_invia_a_tutti']);
  - pool dentro una funzione annidata: FAIL;
  - functools.partial(_handle_update, u): FAIL.
  Il codice attuale passa. Esito: ok, R-450-1 chiusa.
- modules/telegram/bot.py:696 — quando il kernel non ha recupera_esito_firma ora c'è un log.warning, poi la funzione restituisce (None, motivo) come prima. Rischio esaminato: un ritorno muto o un cambio di comportamento. Esito: ok. T78o lo copre in tests/test_unit_kernel.py:8171.
- Prova diretta: tests/test_unit_kernel.py ha dato 1010 PASS, 0 FAIL.

Riserve:
- R-451-1 BASSA: T78p non vede `threading.Timer(0, lambda: _handle_update(u))` (Timer è una sottoclasse di Thread ma ha un altro nome). Non vede nemmeno un import con alias, `from concurrent.futures import ThreadPoolExecutor as TPE` seguito da `TPE(2).submit(lambda: _handle_update(u))`. Con queste due mutazioni il test resta verde. Correzione suggerita:
  - aggiungere "Timer" all'elenco;
  - leggere gli asname degli ImportFrom e aggiungere gli alias ai nomi cercati.
  Va tracciata in stato_progetto.md.

Rischio escluso: non ho verificato a runtime che gli update Telegram arrivino davvero uno alla volta sul bot reale in esecuzione (polling sulla VPS), perché in dev non si riproduce. La garanzia resta solo statica (guardia AST), con il limite di R-451-1.

Memoria: riga #451 più una lezione aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md e committate (4fdc3dd). Script delle mutazioni: /tmp/claude-0/-home-user-Gas/6049a349-3e7f-5be2-83ac-5dc6a4b4ff3d/scratchpad/m.py

### Review #452 (chat Motore)

## VERDETTO: APPROVATO

Review #452 (chat Motore). Ho riguardato il diff staged #451: `gas.py`, `modules/telegram/bot.py` e `tests/test_unit_kernel.py`. Ho letto prima CLAUDE.md, lo stato del progetto (letto selettivamente) e la memoria del revisore.

**Elementi esaminati**
- `tests/test_unit_kernel.py:8206` — La guardia T78p ora aggiunge all'elenco dei nomi cercati gli alias d'import (`asname` di Import/ImportFrom il cui ultimo pezzo è uno dei nomi), insieme a `Timer`. Rischio esaminato: la guardia non vedeva Timer e gli alias (R-451-1). Ho rifatto le mutazioni con lo script `/tmp/claude-0/-home-user-Gas/6049a349-3e7f-5be2-83ac-5dc6a4b4ff3d/scratchpad/m452.py`, che copia la guardia nuova. Falliscono tutte, come devono: Timer+lambda, alias TPE, alias di Timer, alias di Thread, `import concurrent.futures as cf` con `cf.ThreadPoolExecutor`, pool a livello di modulo + lambda, pool in funzione annidata, `functools.partial`. Un alias innocuo (`import json as js`) non dà falsi positivi. Esito: **ok, R-451-1 chiusa**.
- `tests/test_unit_kernel.py:8209` — Collega i costruttori trovati alla funzione che li contiene. Ho fatto una mutazione reale del modulo: aggiunto in coda a `modules/telegram/bot.py` il codice `from threading import Timer as _T452` più `_T452(0, lambda: _handle_update(u))`. Con la suite vera il kernel dà 1009 PASS e 1 FAIL: è T78p, con `['_invia_a_tutti', '_x452']`. Ho ripristinato il file dalla copia e la suite torna a **1010 PASS, 0 FAIL**. Il worktree di bot.py è di nuovo uguale all'index. Esito: **ok**.
- `modules/telegram/bot.py:696` — Se il kernel non ha `recupera_esito_firma`: `log.warning` e risposta `(None, motivo)`. È lo stesso codice già approvato in #450/#451. Esito: **ok**.
- `gas.py:3403` — Il tag «V-1 bot #241» sta in un commento, la stringa della notizia è pulita. Invariato rispetto alla #451. Esito: **ok**.

**Rischio esplicitamente escluso**
Le evasioni dinamiche non sono coperte, perché la guardia è statica. Sono `getattr(threading, "Tim"+"er")`, `importlib.import_module` dentro una funzione e un nome passato per variabile. Come da tua indicazione li considero un limite noto da dichiarare nel report, non una riserva. Non ho verificato il comportamento reale su Telegram (nessun token nel container).

**Memoria**
Riga #452 scritta e committata da `scripts/commit_memoria_revisore.sh` (commit c8ac93d). Nessuna lezione nuova.

### Review #453 (chat Motore)

## VERDETTO: APPROVATO CON RISERVE

Review #453 (chat Motore). Ho letto prima CLAUDE.md (sezioni 5, 8, 9 e 10), poi `reports/stato_progetto.md` (testa) e `.claude/agents/memoria_revisore.md` (ultime voci). Nessun antipattern del Wall of Shame: il diff non taglia la storia, non simula tool e non tocca i guardrail (10 iterazioni, tetto 8k, `_get_window`).

**Elementi esaminati nel diff**
- `modules/notte/notte.py:424` — `stato_mattino`: ha tre blocchi try indipendenti (spesa, lead, firme), ognuno logga solo il nome del tipo d'eccezione con `logging.warning`. `_env_budget()` non solleva mai. Rischi controllati: kernel None o senza `memory`, voci che sollevano eccezioni, scritture nascoste. Esito ok: con `kernel` None `getattr` restituisce None e la funzione esce subito; legge soltanto (`lista_contatti`, `conta_approvazioni`, `_daily_cost_usd`) e non scrive nulla nel diario. È coerente con la regola sulle eccezioni (sezione 9).
- `modules/notte/notte.py:412` — `_giorni_fa`: data mancante, illeggibile o senza fuso orario viene trattata come UTC, oppure dà None, e None conta come «fermo». Rischio controllato: confronto tra data con fuso e data senza fuso, eccezioni impreviste. Esito ok: il formato scritto dal DB (`_now_iso_da`, UTC con microsecondi) si legge con `fromisoformat`, e una data nel futuro dà un numero negativo, quindi non conta come fermo.
- `modules/notte/notte.py:799` — `stato = stato_mattino(kernel)` sta dentro il `try` del giro, prima che venga creato `da_notificare`. Rischio controllato: un'eccezione dentro il `finally`. Esito ok: nel ramo d'eccezione la tupla ha 4 elementi, quindi `stato=None` e `righe_stato_mattino(None)` restituisce `[]`: il messaggio resta uguale a prima. `_notifica_telegram` resta protetta dal suo try.
- `modules/notte/notte.py:369` — `componi_messaggio_telegram`: le 3 righe dello stato vanno sia nel messaggio completo sia in quello ridotto (`solo_conteggi`). Rischio controllato: dati personali su Telegram. Esito ok: le righe contengono solo numeri e costanti, mai campi testuali dei contatti.
- `tests/test_unit_notte.py:1897` — il test di fine giro usa un DB vero con nomi ed email fittizi e verifica che `NOMESEGRETO` e `@x.it` non compaiano né nel messaggio Telegram né nel riepilogo. Rischio controllato: un test che non controlla davvero. Esito ok: i numeri attesi (3 attivi, 2 fermi, 1 firma, tetto predefinito $1.00) dimostrano che il tetto viene letto a fine giro, dopo l'impostazione predefinita notturna.
- `tests/test_unit_notte.py:739` — il limite finto passa da 230 a 330. Rischio controllato: il test potrebbe aver perso il suo scopo. Esito ok: l'asserzione `len(inviati) == 2` e il testo ridotto restano, e il messaggio completo (~375 caratteri) supera ancora il limite.

Prova mia: `pytest tests/test_unit_notte.py` dà 133 passed.

**Riserve (da tracciare in stato_progetto.md)**
- **R-453-1 BASSA**: `modules/memory/store.py:1215` `lista_contatti` restituisce `[]` anche quando il DB è rotto. Con la memoria degradata il messaggio del mattino dice «Lead attivi: 0 (fermi da 7+ giorni: 0)», cioè rassicura il falso, mentre le firme (che in quel caso danno None) dicono correttamente «non lette». Va contro il principio «nel dubbio si segnala» scritto nella stessa funzione. Correzione: usare un segnale di salute della memoria per scrivere «non letti».
- **R-453-2 BASSA**: se nessun kernel è stato creato (catalogo vuoto oppure tutti i kernel falliti), anche la spesa risulta «non letta», benché il log dei token si possa leggere senza kernel. Pesa poco, ma rende il resoconto vuoto proprio nella notte in cui serve di più.

**Cosa NON ho verificato**: non ho lanciato la suite completa (1895) né la suite del kernel (1010 PASS): mi fido delle prove dichiarate, perché il diff tocca solo `modules/notte` e non `gas.py`. Non ho verificato l'invio reale su Telegram né la resa del messaggio sul telefono: non è riproducibile in sviluppo.

**Memoria**: riga #453 e una lezione aggiunte in `/home/user/Gas/.claude/agents/memoria_revisore.md`. Ho lanciato `scripts/commit_memoria_revisore.sh`, che non ha stampato nulla: controlla con `git log -1 -- .claude/agents/memoria_revisore.md` che il commit ci sia, e altrimenti guarda il warning in `gas_debug.log`.

### Review #454 (chat Motore)

## VERDETTO: APPROVATO CON RISERVE

Ri-review #454 della #453, sul diff staged di modules/notte/notte.py e tests/test_unit_notte.py.

**Elementi del diff esaminati**
- `modules/notte/notte.py:444`: `stato_mattino` chiama `conta_approvazioni` dentro un try. Prima c'è il ritorno anticipato a riga 441, che scatta se la memoria è None o ha `available` False. Rischio esaminato: il DB rotto produceva «0 lead». Nel codice vero `MemoryStore.conta_approvazioni` (`modules/memory/store.py:2019`) restituisce None su `sqlite3.Error`/`OSError` e `lista_contatti` è sullo stesso file DB, quindi il segnale di salute è adatto. Esito: ok, R-453-1 chiusa.
- `modules/notte/notte.py:448`: con `if conta is None: return stato` lead e firme restano None e vengono mostrati come «non letti». Le firme si leggono prima dei lead. Ho provato una mutazione: tolto il ritorno, le firme restano condizionate e i lead tornano a «0». Risultato: `test_stato_mattino_fail_safe` FALLISCE (`assert 0 is None`). Dopo il ripristino: 133 passed, e il file è identico allo staged. Esito: ok.
- `tests/test_unit_notte.py:1893`: copre il caso del DB rotto (`lista_contatti` dà `[]`, `conta_approvazioni` dà None, quindi lead None) e il caso a riga 1897 della memoria spenta (`available=False` con conteggi validi, quindi lead None). Esito: ok, i test intercettano la regressione.
- `modules/notte/notte.py:804` (contesto, invariato rispetto alla #453): `stato_mattino` viene chiamata dentro il try del giro. Esito: ok.

**R-453-2 (spesa «non letta» se nessun kernel è stato creato)**: la accetto come residuo BASSO dichiarato. «Non letta» è un'informazione onesta, non una falsa rassicurazione. Duplicare `_daily_cost_usd` oppure chiamarla su un oggetto finto sarebbe peggio (logica doppia che può andare fuori sincronia). Va tracciata in stato_progetto.md come residuo.

**Riserve**
- R-454-1 BASSA: se la tabella `approvals` è sana ma la tabella `contatti` è rotta, `conta_approvazioni` restituisce un dict e `lista_contatti` restituisce `[]`. In quel caso il resoconto dice «Lead attivi: 0». Il caso è stretto (stesso file DB, e lo schema è verificato quando `available` vale True), quindi non blocca.
- Nota cosmetica: `int(conta.get("in_attesa", 0))` a riga 449 sta fuori dal try. Con il contratto reale (dict o None) non solleva. Una memoria alternativa che restituisse un tipo diverso farebbe salire l'eccezione al try del giro. Non blocca.

**Rischio escluso**: non ho verificato il comportamento reale del giro notturno su VPS né l'invio effettivo su Telegram, perché in dev non si riproducono. Mi sono basato sui test con Telegram finto e sulla mutazione. Non ho riletto l'intero `esegui_notte` oltre il punto di chiamata, già esaminato nella #453.

**Wall of Shame**: nessuno slicing della history, nessuna simulazione dell'output dei tool, nessun guardrail indebolito. Fail-safe §9 rispettato.

Riga contatore #454 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md. Ho lanciato `scripts/commit_memoria_revisore.sh` per committarla, ma non ha stampato nulla e non ho controllato il log git: verifica che il commit esista.

### Review #455 (chat Motore)

## VERDETTO: APPROVATO CON RISERVE

Review #455 (chat Motore). Ho letto CLAUDE.md (sez. 5, 8 e 9), le voci rilevanti di reports/stato_progetto.md (R1, R-453/454, contaminazione) e la memoria del revisore. Ho esaminato il diff staged su 5 file. Nessuno slicing della storia, nessuna simulazione dei tool, `_get_window` e il tetto di 10 iterazioni non sono toccati.

**Elementi del diff esaminati**
- `gas.py:101` — `_vero()`: un booleano del modello vale vero solo per valori veri espliciti. Rischio esaminato: la stringa "false" attiva l'elenco. Esito: ok. Ho messo `bool()` al posto di `_vero` e T98d fallisce; T98e copre la tabella dei valori.
- `gas.py:4352` — passaggio di `fermi` a `_ricorda`, con la guardia `isinstance(args, dict)`. Rischio esaminato: argomenti che non sono un dizionario fanno crashare il programma. Esito: ok.
- `gas.py:3994` — `_lead_fermi`: lead attivi senza STATI_CHIUSI, data illeggibile in testa, `max(0, …)` per le date future, date senza fuso trattate come UTC. Rischi esaminati: ordine sbagliato e lead chiusi inclusi. Esito: ok. Mettere la data illeggibile in coda fa fallire T98a; togliere il filtro dei chiusi fa fallire T98a, T98b e T98c. Le righe entrano nelle stesse `parti`, quindi passano da `_sanitize_memory_text` e finiscono nel blocco `<memoria_dati>`.
- `gas.py:3974` — `and not fermi` esclude gli ultimi eventi del diario. Rischio esaminato: il comportamento di ricorda senza fermi cambia. Esito: ok, con fermi falso la condizione è identica a prima. Riserva sul test: se tolgo `and not fermi` i test passano lo stesso (1016/0). Il motivo è che nel fixture il diario è vuoto, quindi le righe del diario che ricompaiono non si vedono.
- `gas.py:2261` — nel diario la descrizione di ricorda aggiunge « fermi=True». Rischio esaminato: nella riga del diario entra testo di terzi. Esito: ok, aggiunge solo una costante.
- `modules/gate/gate.py:83` (contesto) — ricorda resta in UNTRUSTED_INPUT_TOOLS, quindi il suo output contamina ancora la finestra. Esito: ok. La regola dei modelli per i dati personali è la stessa di `ricorda contatto=…`, quindi non c'è una nuova esposizione.
- `modules/notte/notte.py:426` — `_tetto_applicato` usa `gas._env_float` con gli stessi limiti di `_budget_superato` (`gas.py:1571`). Rischio esaminato: tetto mostrato diverso da quello applicato. Esito: ok. Se rimetto `_env_budget` il test della notte fallisce; con NaN il tetto vale 0, con inf viene limitato a 100000, come nel kernel.
- `modules/notte/notte.py:436` — `_righe_illeggibili_log`: legge solo gli ultimi 64 KB, in sola lettura, senza mai sollevare eccezioni. Un byte UTF-8 non valido dà UnicodeDecodeError, che è una sottoclasse di ValueError, quindi la riga conta come rotta. Un log che è una cartella dà -1. Esito: ok. Se cambio -1 in 0, o tolgo il controllo che la riga sia un dizionario, il test fallisce.
- `modules/notte/notte.py:453` — salto della prima riga tagliata quando il log supera 64 KB. Esito: riserva. Se tolgo questa riga i test passano (134 passed): non c'è un test con un log più grande di 64 KB, e senza il salto comparirebbe un avviso falso di 1 riga illeggibile.
- `scripts/notte/catalogo_esempio.yaml:9` — il compito punto_lead usa fermi=true. Esito: ok.

**Riserve (da tracciare in stato_progetto.md)**
- R-455-1 BASSA: con la memoria degradata (`available=False`), `lista_contatti` restituisce [] e ricorda con fermi scrive «(nessun lead attivo)». È una falsa rassicurazione, lo stesso schema di R-454-1. Il compito notturno punto_lead la vedrebbe come «nessuno è fermo».
- R-455-2 BASSA (test): mancano due test che fermino le due mutazioni sopravvissute, cioè la riga `gas.py:3974` senza `and not fermi` (serve un fixture con il diario non vuoto) e il salto della prima riga a `modules/notte/notte.py:453` (serve un log più grande di 64 KB).
- R-455-3 COSMETICA: in `_lead_fermi` nome e prossima_azione non passano da `_campo_pin`. Un a-capo crea righe finte dentro `<memoria_dati>`. Il ramo `contatto=` fa già lo stesso, quindi non è una regressione. Le righe finte non gonfiano `_ricorda_n`, che conta gli elementi di `parti` e non le righe del testo.

**Prove mie**: kernel 1016 PASS 0 FAIL, notte 134 passed. Ho fatto 8 mutazioni, poi ho ripristinato i file; l'albero di lavoro ha di nuovo solo il diff staged. 6 mutazioni fanno fallire i test, 2 sopravvivono (le due di R-455-2).

**Rischio escluso**: non ho verificato il comportamento sulla VPS durante un giro notturno vero, con il log dei token scritto da un altro processo mentre il resoconto lo legge. Un'ultima riga a metà scrittura conterebbe come illeggibile e darebbe un avviso falso, cioè prudente. Non è riproducibile in dev. Non ho rilanciato nemmeno l'intera `pytest tests/` (1896): ho rilanciato solo le suite toccate.

Memoria: riga #455 e una lezione (mutazione inversa sui parametri che escludono un ramo di default) aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md e già committate (e8e7fc8).

### Review #456 (chat Motore)

## VERDETTO: APPROVATO

Ri-review #456 (chat Motore) della #455, sullo stesso diff staged: gas.py, modules/notte/notte.py, scripts/notte/catalogo_esempio.yaml, tests/test_unit_kernel.py, tests/test_unit_notte.py.

**Cosa ho controllato nel diff**
- `gas.py:3998` — `_lead_fermi` restituisce «Elenco dei lead NON letto: memoria degradata» se `available` è False (l'attributo esiste davvero, `modules/memory/store.py:546`) o se `conta_approvazioni()` dà None. Rischio: «nessun lead attivo» mostrato a DB rotto, cioè un falso via libera. Ho tolto la guardia in una copia e T98h fallisce. Esito: ok, R-455-1 chiusa.
- `gas.py:4022` — nome e prossima_azione passano da `_campo_pin`, come nel pin (`gas.py:3534`). Rischio: un a capo nel nome crea una riga finta «- [nuovo] …» nel blocco. Ho tolto `_campo_pin` dal nome e T98i fallisce. Esito: ok, R-455-3 chiusa.
- `gas.py:3974` — `and not fermi` esclude il diario di default. Il nuovo test (`tests/test_unit_kernel.py:10732`) scrive un evento nel diario. Ho rifatto la mutazione M4 sopravvissuta nella #455 (tolto `and not fermi`): ora T98b (conteggio 5) e T98g falliscono. Esito: ok, R-455-2 chiusa per il kernel.
- `modules/notte/notte.py:453` — `righe[1:]` salta la prima riga tagliata della coda. Il test `tests/test_unit_notte.py:1945` usa righe da 141 byte e 514 ripetizioni: il taglio cade 29 byte dentro una riga, quindi il test non passa per caso. Ho rifatto la mutazione N1 sopravvissuta (tolto `righe[1:]`) e il test fallisce. Esito: ok, R-455-2 chiusa per notte.
- `gas.py:4357` — la chiamata passa `fermi` con `_vero`; i valori «false», 0 e None non attivano l'elenco (T98d/T98e). Esito: ok.

**Prove (in una copia dell'index nello scratchpad)**: kernel 1019 PASS, 0 FAIL; tests/test_unit_notte.py 135 passed. Ognuna delle 4 mutazioni fa fallire almeno un test.

**Cosa NON ho verificato**
- Il caso stretto con la tabella approvals sana e la tabella contatti rotta: `lista_contatti` dà [] e l'elenco dice «nessun lead attivo». È lo stesso residuo BASSO già accettato come R-454-1. Non l'ho sondato: serve rompere una sola tabella dello stesso file DB.
- Il comportamento reale del modello con il nuovo prompt in `scripts/notte/catalogo_esempio.yaml`: serve un provider vivo, non riproducibile in dev.
- Non ho rilanciato `pytest tests/` per intero: 1897 passed è la tua cifra, io ho girato solo kernel e notte.

**Memoria**: riga #456 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (commit ebaf9f3). Nessuna lezione nuova.

### Review #457 (chat Motore)

## VERDETTO: APPROVATO

Review #457 (chat Motore): merge di origin/main 5698cd3 (PR #243, chat Mani, fetta 6 web) dentro feat/merge-automatico-z1xjx2 (HEAD 5f4c524). Base comune: e3ffc0a.

**Elementi del diff esaminati** (citazioni prese dal diff di sessione dopo il merge, base = origin/main, come chiede la lezione #444):
- modules/web/leggi.py:127 — `_TITOLO_VUOTO_IN`, cioè la parte di main portata dentro dal merge. Rischio esaminato: che il merge l'avesse cambiata. Il file nell'index ha 0 righe di differenza da MERGE_HEAD e il worktree è uguale all'index. Esito: ok.
- tests/test_unit_web_leggi.py:877 — i test della fetta 6. Stessa verifica: 0 righe di differenza da main. Ho rilanciato la suite sul tree unito: 174 passed. Esito: ok.
- gas.py:3998 — `_lead_fermi` con memoria degradata, già approvato nella review #456. Rischio esaminato: che il merge avesse toccato i file del motore. gas.py, modules/notte/notte.py, modules/telegram/bot.py, tests/test_unit_kernel.py e tests/test_unit_notte.py hanno 0 righe di differenza tra index e HEAD. Rispetto a main, il diff di sessione contiene solo il lavoro già revisionato nelle review #449-#456 (chat Motore). Esito: ok.
- tests/test_unit_notte.py:1945 — il test del log oltre 64 KB, già revisionato nella #456: è nel diff di sessione ed è invariato rispetto a HEAD. Esito: ok.
- .claude/agents/memoria_revisore.md:737 — l'inizio del blocco chat Mani, che segue il blocco chat Motore (righe da 725 a 736). Rischio esaminato: righe perse o duplicate nel conflitto. Ho confrontato il multinsieme delle righe di base, ramo e main: 0 righe perse, 0 in più, nessun marcatore di conflitto, e l'ordine è quello dichiarato. Esito: ok.
- reports/stato_progetto.md:606 — la nota della fetta 6 Mani entrata col merge automatico. Stessa verifica sul multinsieme: 0 righe perse, 0 in più, nessun marcatore. Esito: ok.

**Report di sessione:** diff_sessione.md, handoff.md e ultimo_report.md restano nella versione del ramo. È corretto, sono log di sessione. Le versioni di main restano nella storia di git, al commit 5698cd3.

**Rischio escluso:** non ho rilanciato la suite del kernel (1019/0) né quella di notte. Mi sono fidato delle tue prove, perché quei file sono identici a HEAD, che è già stato verificato nella review #456. Non ho controllato neanche la CI del commit di merge, che non esiste ancora.

**Riga di memoria:** ho scritto la riga #457 (chat Motore) in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. NON è committata: con il merge in corso non ho lanciato commit_memoria_revisore.sh. Il file ora risulta `MM`: la riga è nel worktree ma non nell'index. Prima del commit di merge esegui `git add .claude/agents/memoria_revisore.md`, così la riga entra in quel commit. Ricorda che lo SHA del diff staged cambia: rigenera il marcatore con segna_review_ok.sh dopo l'add.

Nessuna lezione nuova.

### Review #458 (chat Motore)

## VERDETTO: APPROVATO

Review #458 (chat Motore). Ho letto il diff staged: 1 riga in gas.py e 2 in tests/test_unit_kernel.py. Ho controllato il contesto delle regole (CLAUDE.md sez. 5, lo stato del progetto e la mia memoria).

Elementi esaminati:
- `gas.py:3903`: `fermi = _vero(fermi)` sta in testa a `_ricorda`, dopo l'azzeramento di `_ricorda_n` e prima del ramo «memoria None».
  - Rischio esaminato: un valore non booleano (es. la stringa "false") poteva arrivare a `if fermi:` (`gas.py:3972`) e alla condizione del diario di default (`gas.py:3975`).
  - Ora quel valore viene convertito in booleano prima di entrambi i punti. `_vero` (`gas.py:101`) restituisce True solo per true/1/"true"/"sì"/"yes" e non solleva eccezioni con nessun tipo.
  - Esito: ok.
- `gas.py:4359`: execute_tool_call continua ad applicare `_vero` prima della chiamata.
  - Rischio esaminato: una doppia conversione che dà risultati diversi.
  - La doppia applicazione non cambia il risultato (`_vero(True)` è True, `_vero(False)` è False), quindi è innocua. Anche la riga del diario a `gas.py:2261` usa `_vero` per conto suo e resta coerente.
  - Esito: ok.
- `tests/test_unit_kernel.py:10777`: T98j chiama direttamente `_ricorda(None, None, 10, fermi="false")` e controlla che «dal più fermo» non compaia.
  - Rischio esaminato: un controllo «non contiene» che passa sempre, anche senza la correzione.
  - Mutazione fatta come richiesto, in una copia ricavata dall'index e messa nello scratchpad. Ho tolto la riga di `gas.py:3903`:
    - con la riga: **1020 PASS, 0 FAIL** (Python 3.13.16);
    - senza la riga: **1019 PASS, 1 FAIL**, e fallisce solo T98j.
  - Il test regge davvero la correzione. Esito: ok.

Note COSMETICHE (non bloccanti, non serve tracciarle):
- T98j sta tra il calcolo di `_s98i` e il check T98i: l'ordine di lettura è strano. Non interferisce, perché la chiamata non scrive nel DB.
- T98j non ha l'argomento di dettaglio. In caso di FAIL non mostra l'output.
- Il type hint `fermi: bool` ora riceve di fatto `Any`.

Rischi esclusi:
- Non ho rieseguito la suite sotto Python 3.11 (versione della CI) né pytest: qui c'è solo 3.13.16, e la modifica non dipende dalla versione.
- Non ho controllato altri chiamanti diretti di `_ricorda` fuori da gas.py e dai test.

Guardrail e regole del progetto: nessuno slicing della history, nessuna simulazione di output dei tool, nessuna modifica al cap di 10 iterazioni né a `_get_window`. La regola «zero crash» (fail-safe) è rispettata.

Memoria: riga #458 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (commit e7ccb22). Nessuna lezione nuova.

### Review #459 (chat Motore)

## VERDETTO: APPROVATO CON RISERVE

Review #459 (chat Motore). Diff staged: gas.py, modules/notte/notte.py, tests/test_unit_notte.py. Worktree uguale all'index. Prima della review ho letto CLAUDE.md (sezioni 1, 5, 8 e 10), le voci di reports/stato_progetto.md su #241 e la mia memoria. Nel diff non ci sono slicing della history né simulazioni di tool, e nessun guardrail è indebolito.

**Cosa ho controllato nel diff**
- modules/notte/notte.py:456 — `righe = righe[:-1]` scarta l'ultimo pezzo senza a capo, cioè una riga ancora in scrittura. Rischio esaminato: l'ordine rispetto a `righe[1:]` quando la coda supera 64 KB, e una riga unica più lunga di 64 KB. Esito: ok, in entrambi i casi il conteggio dà 0 e non va in errore.
- modules/notte/notte.py:459 — la soglia usa lo stesso formato e la stessa finestra di 24 ore di gas.py:1478 (`_daily_cost_usd_bloccato`). Rischio esaminato: un disallineamento tra le due finestre. Esito: ok.
- modules/notte/notte.py:471 — una riga valida più vecchia della soglia azzera le righe rotte contate prima. Rischio esaminato: valori di ts anomali, provati con sonde. Esito: riserva R-459-3.
  - Rotta tra una riga vecchia e una nuova: 1. Rotta dopo una riga nuova: 1. ts null: 1. ts con "Z": 1.
  - Solo una riga rotta senza a capo: 0. Righe fuori ordine: 0, accettabile.
- tests/test_unit_notte.py:1956 — test nuovo. Esito: ok.
  - Ho provato due mutazioni su una copia dall'index: tolto l'azzeramento, e tolto `[:-1]`. Ciascuna fa fallire 1 test.
  - Le prove su notte: 136 passed.
- tests/test_unit_notte.py:1925 — commento aggiunto «niente ts: nella finestra». Esito: riserva R-459-1.
- gas.py:3422 — testo del ramo 'incerta' di `recupera_esito_firma`. Rischio esaminato: se un test controlla il vecchio testo («si è interrotto»). Esito: nessun test lo controlla; riserva R-459-2.
- Contesto (file non nel diff): gas.py:4269 conferma che un comando scaduto (`TimeoutExpired`) lascia davvero l'esito incerto.

**Riserve, da tracciare in stato_progetto.md**
- **R-459-1 COSMETICA** — tests/test_unit_notte.py:1925: il commento è falso.
  - Un dict senza ts dà `""`, che è minore della soglia: la riga è trattata come VECCHIA e azzera il conteggio.
  - Il test passa solo perché `{"ok": 1}` è la prima riga. Correggere il commento.
- **R-459-2 COSMETICA** — gas.py:3422: «crash di Gas o comando scaduto» non copre tutte le cause di esito incerto.
  - Restano fuori l'errore interno dopo il reclamo (gas.py:3379) e l'output che non è testo (gas.py:4269).
  - Suggerimento: «per esempio crash di Gas o comando scaduto».
- **R-459-3 BASSA** — modules/notte/notte.py:471: un dict valido senza ts (o con ts "") che segue righe rotte le azzera.
  - Sonda: `rotta\n{"ok":1}\n` dà 0.
  - Nel log reale ogni riga ha il ts (gas.py:1441), quindi il caso è teorico. Basta dichiararlo o trattare il ts assente come «dentro la finestra».

**V-2 bot #241 (perdita del tag dopo una doppia compressione)**: sono d'accordo a lasciarla come residuo, perché la correzione vera richiede un segno nel DB, cioè un cambio di schema. Va però scritta in stato_progetto.md come residuo aperto con il motivo; non basta citarla nel report.

**Cosa non ho verificato**
- Non ho rieseguito la suite del kernel (1020) né `pytest tests/` (1905). La modifica a gas.py cambia solo una stringa e nessun test la controlla, quindi mi fido delle tue prove.
- Non ho verificato il comportamento con più di 64 KB di log nelle 24 ore su VPS: è il limite che dichiari nella docstring, e in dev non si riproduce in modo realistico.

**Memoria**: ho scritto la riga #459 più una lezione (ts assente o "" trattato come «più vecchio di tutto» in un confronto tra stringhe). Committata da sola nel commit a965355.

### Review #460 (chat Motore)

## VERDETTO: APPROVATO

Ho fatto la ri-review #460 (chat Motore) della #459 sullo stesso diff staged: gas.py, modules/notte/notte.py, tests/test_unit_notte.py. Ho letto le parti che servivano: CLAUDE.md sez. 5, reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md con la riga della #459.

Elementi esaminati:
- modules/notte/notte.py:471 — `elif d.get("ts") and str(d["ts"]) < soglia:` azzera le rotte solo se la riga ha un ts presente e più vecchio della soglia. Rischio esaminato: un ts assente, vuoto o nullo che azzera le righe rotte senza avvisare (R-459-3). Ho controllato con una sonda: dopo una riga rotta, `{"ts": null}`, `{"ts": ""}` e `{"ts": "abc"}` danno 1; `{"ts": "1999-01-01T00:00:00"}` dà 0, come deve. Esito: ok, R-459-3 chiusa.
- tests/test_unit_notte.py:1969 — nuovo caso `rotta\n{"ok": 1}\n`, che deve dare 1. Rischio esaminato: un test che non scatta se si rimette la logica vecchia. Mutazione in una copia presa dall'index: condizione vecchia `str(d.get("ts", "")) < soglia` → 1 FAIL (test_log_token_righe_rotte_solo_nella_finestra_di_24_ore), 135 passed. Esito: ok.
- tests/test_unit_notte.py:1925 — il commento ora dice «righe senza ts: dentro la finestra», e con il codice nuovo è vero. Esito: ok, R-459-1 chiusa.
- gas.py:3422 — la notizia ora dice «(per esempio crash di Gas o comando scaduto)»: le cause non sono più presentate come un elenco completo. Esito: ok, R-459-2 chiusa.
- modules/notte/notte.py:456 e modules/notte/notte.py:460 — `righe[:-1]` e la soglia a 24 ore sono rimasti uguali a quelli approvati nella #459. Niente slicing della cronologia (qui si taglia una lista di righe del log, non la storia dei messaggi), nessun guardrail indebolito, fallback FAIL-SAFE con logging.warning intatto. Esito: ok.

Prove: tests/test_unit_notte.py → 136 passed sul diff staged.

Nota non bloccante, non è una riserva: un ts numerico (es. `{"ts": 1}`) diventa la stringa "1", che è minore della soglia, quindi azzera le rotte. Nel log reale non succede, perché gas.py scrive sempre il ts come stringa ISO.

Rischio escluso: non ho rieseguito la suite del kernel (1020 PASS 0 FAIL è il risultato dichiarato da chi mi ha chiamato). Sul kernel il diff cambia solo il testo di una stringa in gas.py:3422, che i test non controllano parola per parola. Non ho verificato il comportamento sul Mac o sulla VPS.

Memoria: ho aggiunto la riga contatore #460 in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, senza lezioni nuove, e ho lanciato scripts/commit_memoria_revisore.sh, che non ha stampato errori.

## §5 DELTA TEST DEL MOTORE

Kernel 996 → 1020 PASS (T78l-T78p, T98a-T98j nuovi); pytest `tests/` 1862 → 1905 passed (7 test nuovi del resoconto, più la web suite arrivata col merge di #242). Nessun FAIL. Correzione dell'handoff di #240: il delta dei test del bot lì dichiarato +9 era +14 (311 → 325).

```
=== RIEPILOGO: 1020 PASS, 0 FAIL ===
1905 passed in 178.83s (0:02:58)
```

## §6 STATO CI

`gh run list` non autenticato; run lette via `gh api` REST (ramo `feat/merge-automatico-z1xjx2`):

```
39698877745 verifica-bot a57a16a completed success
39698875797 CI a57a16a completed success
39698000744 verifica-bot 5f4c524 completed success
39697998856 CI 5f4c524 completed success
```

- `a57a16a` — CI 39698875797 success (unit-suite, handoff-check); verifica-bot 39698877745 success, esito «neutral: decide l'operatore», verdetto APPROVATO CON RISERVE senza ALTA/MEDIA.
- `5f4c524` — CI 39697998856 success; verifica-bot 39698000744 success (nel check run: failure per il conflitto con main, chiuso in `03488e4`).
- `075e323` — CI 39695260138 success; `eafe6ee` — CI 39685325511 success; `079c879` — CI 39685151985 failure (handoff non aggiornato, corretto da `eafe6ee`).
- Gli altri commit della sessione: nessuna run su questo SHA (pushati insieme, testati solo nell'albero del commit di testa di ogni push).
- `a965355`, `6726ee7`, `801532b` e il commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-445-3 (chat Motore)** COSMETICA, preesistente: crash tra `_storia_esito_firma` e `registra_esito_esecuzione` → esito NULL nel DB per sempre.
- **R-453-2 (chat Motore)** BASSA, accettata dal revisore: spesa «non letta» se nessun kernel è stato creato.
- **V-3 verifica esterna #241** COSMETICA: «NON è stata eseguita» anche per un [KO] da errore del tool (coerente con applica_firma).
- **R-454-1 (chat Motore)** BASSA: tabella `approvals` sana ma `contatti` rotta → «Lead attivi: 0» (stesso residuo in `ricorda fermi`, #456).
- V-2 verifica esterna #241 2° giro BASSA: l'ordinamento per età di `ricorda fermi` non è stato riprodotto in sonda (coperto da T98a).
- Note COSMETICHE #458: posizione di T98j, nessun dettaglio in caso di FAIL, type hint `fermi: bool`.
- **V-2 bot #241 (5f4c524) / V-1 bot #241 (a57a16a)** BASSA, deferita: il recupero decide «non in storia» scandendo la storia; dopo `/reset` o due compressioni il tag sparisce e un click tardivo scrive una notizia falsa (mai una nuova esecuzione). Fix: segno nel DB, cambio di schema.
- **V-2 bot #241 (a57a16a)** BASSA: un «database is locked» tra `conta_approvazioni` e `lista_contatti` dà ancora «Lead attivi: 0» (stesso schema di R-454-1).
- **V-3 bot #241 (a57a16a)** BASSA: il controllo del log dei token è parziale (ultimi 64 KB; righe JSON valide scartate da `_costo_riga` non contano).
- Nota COSMETICA #454: `int(conta.get("in_attesa", 0))` fuori dal try.
- Limite dichiarato #452: la guardia T78p è statica (getattr dinamico, importlib, nomi passati per variabile non visti).
