# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — Chat Motore: R7, esito di un'azione firmata recuperato dopo un'interruzione (R-c4b3-3, PR #241)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #241 (https://github.com/Gasss23/Gas/pull/241; numero e URL dall'esito reale di `create_pull_request` via MCP GitHub, `gh` non autenticato nella sessione cloud): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10).
2. Fetta che tocca la firma: secondo passaggio nella chat claude.ai con il link della PR.
3. Cose dell'operatore messe da parte per domattina: `reports/da_mergiare.md`, sezione «Da fare domattina».

---

## §1 SCOPE & ESITO FETTE

- **Merge in sospeso**: `FATTA` — nessuna PR aperta (#240 e #239 già mergiate).
- **Cose dell'operatore messe da parte**: `FATTA` — `reports/da_mergiare.md`.
- **R-c4b3-3 (roadmap R7)**: `FATTA` — review #445/#446 APPROVATO CON RISERVE, #447 APPROVATO.
- **R-445-1, R-445-2, R-446-1**: `FATTA`.
- **R-445-3**: `DEFERITA — COSMETICA, preesistente, fetta successiva`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 gas.py                             |  67 +++++++++++++++++++++++++++++++++++++++++++++++---
 modules/telegram/bot.py            |  12 +++++++--
 reports/da_mergiare.md             |  27 +++++++++-----------
 reports/diff_sessione.md           |  13 +++++-----
 reports/handoff.md                 | 484 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/roadmap.md                 |   4 +--
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  37 ++++++++++------------------
 tests/test_unit_kernel.py          | 103 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 10 files changed, 295 insertions(+), 457 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
079c879 fix(firma): esito recuperato in storia dopo un'interruzione tra reclamo e storia (R7, R-c4b3-3)
ad1ab5e chore(revisore): memoria review #447 — APPROVATO
d48d453 chore(revisore): memoria review #446 — APPROVATO CON RISERVE
8c4e11c chore(revisore): memoria review #445 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore: `079c879` (gas.py, modules/telegram/bot.py, tests/test_unit_kernel.py). Tre giri sullo stesso diff staged, incollati integralmente.

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

## §5 DELTA TEST DEL MOTORE

Kernel 996 → 1008 PASS (T78l, T78m, T78n nuovi); pytest `tests/` 1816 → 1862 passed (include la web suite arrivata col merge di #239). Nessun FAIL.

```
=== RIEPILOGO: 1008 PASS, 0 FAIL ===
1862 passed in 185.98s (0:03:05)
```

## §6 STATO CI

`gh` non autenticato nella sessione cloud: run lette via MCP GitHub (`list_workflow_runs`, ramo `feat/merge-automatico-z1xjx2`):

- `079c879` — CI run 39685151985 (#1152, push): `in_progress` alla scrittura dell'handoff; verifica-bot run 39685172943: `skipped` (etichetta `verifica` non ancora messa).
- `ad1ab5e`, `d48d453`, `8c4e11c` — nessuna run su questo SHA (pushati insieme a `079c879`, testati solo nell'albero di `079c879`).
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-445-3 (chat Motore)** COSMETICA, preesistente: crash tra `_storia_esito_firma` e `registra_esito_esecuzione` → esito NULL nel DB per sempre.
