# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — Chat Motore: R7 R-c4b3-3 (esito della firma recuperato), riserve finali di #241, resoconto di spesa e stato nel messaggio del mattino (R1) — PR #241

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
- **R1 compiti veri nel catalogo (contatti fermi)**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  12 +++++++++++
 gas.py                             |  68 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 modules/notte/notte.py             |  97 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 modules/telegram/bot.py            |  16 +++++++++++++--
 reports/da_mergiare.md             |  31 ++++++++++++++--------------
 reports/diff_sessione.md           |  16 ++++++++-------
 reports/handoff.md                 | 401 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/roadmap.md                 |   8 ++++----
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  39 +++++++++++++----------------------
 tests/test_unit_kernel.py          | 146 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_notte.py           |  73 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 12 files changed, 648 insertions(+), 264 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

Kernel 996 → 1010 PASS (T78l, T78m, T78n, T78o, T78p nuovi); pytest `tests/` 1862 → 1895 passed (3 test nuovi del resoconto, più la web suite arrivata col merge di #242). Nessun FAIL. Correzione dell'handoff di #240: il delta dei test del bot lì dichiarato +9 era +14 (311 → 325).

```
=== RIEPILOGO: 1010 PASS, 0 FAIL ===
1895 passed in 183.36s (0:03:03)
```

## §6 STATO CI

`gh` non autenticato per `gh run list`; run lette via `gh api` REST (ramo `feat/merge-automatico-z1xjx2`):

```
39685338876 verifica-bot eafe6ee completed success
39685329478 verifica-bot eafe6ee completed skipped
39685325511 CI eafe6ee completed success
39685172943 verifica-bot 079c879 completed skipped
39685151985 CI 079c879 completed failure
```

- `eafe6ee` — CI 39685325511 success (unit-suite e handoff-check); verifica-bot 39685338876 success.
- `079c879` — CI 39685151985 failure (pushato senza l'handoff aggiornato: il commit di fine-task `eafe6ee` lo ha corretto); `ad1ab5e`, `d48d453`, `8c4e11c`: nessuna run su questo SHA.
- `ee0b4d7`, `6ab3ee0`, `4fdc3dd`, `c8ac93d`, `c82875f`, `1f0a2e9`, `3b988f6`, `0037522` e il commit di fine-task: run non ancora disponibile alla scrittura dell'handoff (pushati insieme a fine task: sarà testato solo l'albero del commit di testa).

## §7 RISERVE APERTE

- **R-445-3 (chat Motore)** COSMETICA, preesistente: crash tra `_storia_esito_firma` e `registra_esito_esecuzione` → esito NULL nel DB per sempre.
- **R-453-2 (chat Motore)** BASSA, accettata dal revisore: spesa «non letta» se nessun kernel è stato creato.
- **R-454-1 (chat Motore)** BASSA: tabella `approvals` sana ma `contatti` rotta → «Lead attivi: 0».
- Nota COSMETICA #454: `int(conta.get("in_attesa", 0))` fuori dal try.
- Limite dichiarato #452: la guardia T78p è statica (getattr dinamico, importlib, nomi passati per variabile non visti).
