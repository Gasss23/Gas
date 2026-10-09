# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-09 — merge #162 + riserve V-1/V-2/V-3 del bot su #162

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #163 (https://github.com/Gasss23/Gas/pull/163). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"url":"https://github.com/Gasss23/Gas/pull/163"}`): `gh` nel container non è autenticato. Merge autonomo dell'agente solo con verdetto testuale del bot `APPROVATO` senza finding V-x; altrimenti decide l'operatore.
2. Sul Mac (se non già fatto): `cd ~/Gas && git fetch origin && git switch --detach origin/main`, poi `reports/setup_notte.md`.

---

## §1 SCOPE & ESITO FETTE

- **Merge di #162**: `FATTA` — su richiesta esplicita dell'operatore, merge commit `7995658` (= BASE di questa sessione).
- **Fetta 1 — V-2 bot #162, un solo tentativo extra dell'SDK** (`gas.py`): `FATTA` — `PROVIDER_MAX_RETRIES = 1`, override `GAS_PROVIDER_MAX_RETRIES` (min 0), passato a `run_turn` e `rifletti`.
- **Fetta 2 — V-1 bot #162, docstring di `modules/notte/notte.py`**: `FATTA` — caso peggiore ~36 min con la formula; `reports/setup_notte.md` allineato; chiude R-227-2.
- **Fetta 3 — V-3 bot #162, sintesi dello stat**: `FATTA` — nota sotto il blocco §2.
- **Fetta 4 — test**: `FATTA` — T81e, T81f; kernel 711 → 713 PASS.
- **R-228-1, R-228-2**: `FATTA` (stessa fetta).
- **Fetta 5 — finding della verifica esterna (agente) e del bot su `653a625`**: `FATTA` in `f3ff0c6` — T81g su `rifletti` (R-229-1, V-1 agente, V-2 bot), commento di `PROVIDER_TIMEOUT_SEC` (V-2 agente, V-1 bot), ~36 min come ordine di grandezza (V-3 agente, R-230-1); frase di `stato_progetto.md` sulla sintesi dello stat corretta nel commit di fine-task (V-1 bot). Kernel 713 → 714 PASS.
- **V-4 verifica esterna (agente)**: `DEFERITA` — COSMETICA (voce 6 di `stato_progetto.md` troppo lunga, §11).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 gas.py                             |  16 +++++++++++++---
 modules/notte/notte.py             |   9 +++++++--
 reports/diff_sessione.md           |  16 ++++++++--------
 reports/handoff.md                 | 272 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------------------------------
 reports/setup_notte.md             |   6 ++++--
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  31 +++++++++++++++++++------------
 tests/test_unit_kernel.py          |  57 +++++++++++++++++++++++++++++++++++++++++++++------------
 tests/test_unit_notte.py           |   2 +-
 10 files changed, 277 insertions(+), 139 deletions(-)
```

Nota (V-3 bot #162): la riga di sintesi include `reports/handoff.md`, ma i SUOI conteggi sono approssimati per costruzione (lo stat è generato prima dell'ultima scrittura del file stesso). Il set di file è esatto; la CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
f3ff0c6 fix(test,doc): T81g su rifletti + caso peggiore di notte come ordine di grandezza (verifica esterna #163)
a6886a4 chore(revisore): memoria review #231 — APPROVATO
bdebf53 chore(revisore): memoria review #230 — APPROVATO CON RISERVE
653a625 docs(fine-task): report riserve V-1/V-2/V-3 bot #162 (PR #163)
9581ed0 fix(provider): un solo tentativo extra dell'SDK + docstring notte (V-1/V-2 bot #162)
66d4126 chore(revisore): memoria review #229 — APPROVATO CON RISERVE
3d5e5ef chore(revisore): memoria review #228 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE

### Review #228 (diff staged di 9581ed0, prima versione)

VERDETTO: APPROVATO CON RISERVE

In breve: il diff fa quello che deve. `max_retries` è un parametro valido dell'SDK installato, il caso peggiore di ~36 min è giusto e il test nuovo fallisce davvero se si toglie la modifica. Resta una sola riserva bassa (R-228-1) sulla precisione del test. Si può committare.

**Elementi del diff esaminati**

1. `gas.py:1975` — passa `max_retries=self.PROVIDER_MAX_RETRIES` al client OpenAI di `rifletti`.
   - Rischio: un parametro che l'SDK non conosce farebbe fallire tutti i rung.
   - Controllo: l'SDK installato (openai 2.43.0, `/usr/local/lib/python3.13/dist-packages/openai`) ha `max_retries: int = 2` nel costruttore. In `_base_client.py` (riga 1042 dell'SDK) anche `httpx.TimeoutException` viene ritentato, quindi la modifica riduce davvero l'attesa nel caso "risposta lenta".
   - Esito: **ok**.
2. `gas.py:2548` — stessa modifica nel client di `run_turn`, creato una volta per rung e fuori dal `for _ in range(10)`.
   - Rischio: toccare il limite di 10 iterazioni o la cascata di fallback (§9).
   - Controllo: limite, `_get_window` e `except` del rung sono invariati. Nel diff non c'è nessun taglio diretto della cronologia e nessuna simulazione di output dei tool.
   - Esito: **ok**.
3. `gas.py:698` / `gas.py:1020` — costante `PROVIDER_MAX_RETRIES = 1`, sovrascrivibile da `GAS_PROVIDER_MAX_RETRIES` tramite `_env_int`, minimo 0.
   - Rischio: un valore negativo o sporco passato all'SDK.
   - Controllo: T81e dà `(0, 0, 1)` per "0", "-3" e "xyz".
   - Scelta di 1 solo tentativo extra: è sensata. Su un 429 l'SDK aspetta al massimo 60 s (se il provider indica quanto aspettare) e ritenta una volta. Una quota esaurita (per esempio Gemini giornaliera) passa al rung successivo prima di quanto succedeva con 2 tentativi extra, e un errore 5xx momentaneo viene ancora assorbito.
   - Esito: **ok**.
4. `modules/notte/notte.py:37-40` — docstring con la formula del caso peggiore.
   - Rischio: un conto sbagliato, come la vecchia R-227-2.
   - Controllo: ho rifatto il conto su `_cascata_provider("semplice")` (contesto, `gas.py:643`). Sono 4 rung remoti (flash-lite, flash, groq, openrouter) x 2 tentativi x 120 s = 16 min, più Ollama 2 x 600 s = 20 min, totale **36 min**. Tra un tentativo e l'altro, dopo un timeout, l'SDK aspetta circa 0,5 s (`INITIAL_RETRY_DELAY`), quindi è trascurabile. `reports/setup_notte.md` riporta lo stesso numero.
   - Esito: **ok**.
5. `tests/test_unit_kernel.py:7255` — T81e.
   - Rischio: test vacuo.
   - Mutation fatta: ho tolto `max_retries` da `rifletti` e il risultato è `[FAIL] T81e … retries visti: [1, None]`, con suite a 711/1. Ho ripristinato a mano con Edit, senza checkout né stash. `cmp` con la copia salvata dà IDENTICO e `git diff` non mostra modifiche fuori dallo staged.
   - Risultati riprodotti: **712 PASS / 0 FAIL**, pytest **786 passed**.
   - Esito: **riserva**, vedi R-228-1.

**Riserve**

- **R-228-1 (BASSA, test):** T81e confronta il valore arrivato al client solo col valore di classe (`== GasKernel.PROVIDER_MAX_RETRIES == 1`). Non verifica che una sovrascrittura via env arrivi al client: sopravvive la mutation `max_retries=GasKernel.PROVIDER_MAX_RETRIES` (legge la costante di classe invece di `self`). Correzione: impostare `GAS_PROVIDER_MAX_RETRIES=0` prima di una delle chiamate di T81e e aspettarsi `0` nel client.
- **R-228-2 (COSMETICA, doc):** nella voce 6 di `reports/stato_progetto.md` resta il vecchio "caso peggiore ~55 min di sforamento" dentro il paragrafo storico della chiusura di R-220-3. Il valore nuovo (~36 min) compare più avanti nella stessa voce. Il vecchio numero è corretto come storia, ma chi legge in fretta può confondersi.

**Rischi esclusi esplicitamente**

- Non ho provato un vero timeout di rete contro un provider appeso. Non è riproducibile in dev senza rete né chiavi. Il comportamento dell'SDK l'ho dedotto leggendo il suo codice sorgente, non osservandolo.
- Non ho verificato la versione dell'SDK sul Mac o sul VPS. In questo repo non c'è un venv e ho usato l'SDK di sistema. `max_retries` esiste però nel costruttore OpenAI da molte versioni.
- Il client di `doctor` (`gas.py:2690`, timeout 15 s, 2 tentativi extra di default) è fuori dal diff e fuori dal giro notturno, quindi non l'ho considerato.
- V-3 riguarda solo il prossimo `handoff.md`, che non è in questo diff: non verificabile qui.

**Memoria**

- Riga `#228` aggiunta con una lezione nuova: il test di una costante sovrascrivibile da env deve impostare un valore diverso dal default.
- Committata da sola con `scripts/commit_memoria_revisore.sh` (commit `3d5e5ef`).
- Lo staged sotto review è rimasto intatto: 6 file, +50/−20.

### Review #229 (delta: chiusura R-228-1/R-228-2, diff finale di 9581ed0)

VERDETTO: APPROVATO CON RISERVE

Le due riserve della review #228 sono chiuse. Resta una sola riserva, BASSA e di solo test: lo stesso buco di R-228-1 è ancora aperto sul secondo punto di chiamata, `rifletti`.

Prima della review ho letto quello che il protocollo richiede: CLAUDE.md è già nel contesto; `reports/stato_progetto.md` l'ho letto in modo mirato con Grep; della memoria del revisore ho letto le ultime voci, fino alla #228. Tutte le prove le ho fatte su una copia del repo nella cartella di lavoro temporanea, senza `git checkout` né `stash`. Dopo, il repo non ha modifiche fuori dallo staging (`git diff --quiet` su `gas.py` e `tests/` è pulito).

**Elementi del diff esaminati**

1. `tests/test_unit_kernel.py:7223` — `_rt_def81 = list(_retries81)` fotografa i retries visti dal client prima che gli override inquinino la lista. Rischio esaminato: che T81e confronti valori sporcati dai kernel creati dopo. Esito: **ok**. T81e richiede anche `_rt_def81 != []`, quindi non può passare a vuoto.
2. `tests/test_unit_kernel.py:7229-7233` (T81f) — imposta l'env a `"0"`, crea un kernel nuovo, esegue `run_turn` e controlla `_rt_client81 == [0]`. Rischio esaminato: un test vacuo. Esito: **ok**. Ho ripetuto la tua mutation sulla copia: `gas.py:2548` portato a `GasKernel.PROVIDER_MAX_RETRIES` fa fallire T81f con "retries visti: [1]" (712/1). Il controllo è un'uguaglianza esatta, quindi coglie anche una seconda costruzione del client.
3. `tests/test_unit_kernel.py:7235-7238` — il `finally` ripristina `GAS_PROVIDER_MAX_RETRIES`, e la toglie se all'inizio non c'era. Rischio esaminato: che il valore resti impostato per i test successivi (la lezione di #221). Esito: **ok**. Prova fatta: ho inserito una stampa dell'env prima del riepilogo. Senza la variabile esce `None`, con `GAS_PROVIDER_MAX_RETRIES=4` impostata prima esce `4`. In entrambi i casi la suite dà 713/0.
4. `reports/stato_progetto.md` voce 6 — il testo ora dice "caso peggiore allora ~55 min di sforamento, ridotto a ~36 min il 2026-10-09 con V-2 bot #162". Esito: **ok**, coerente con il conto verificato in #228.
5. Contesto: `gas.py:1975` (`rifletti`) — **riserva R-229-1 (BASSA, test)**. Sulla copia ho cambiato solo questa riga in `GasKernel.PROVIDER_MAX_RETRIES`, lasciando corretta la 2548: la suite resta 713 PASS, 0 FAIL, quindi la mutation sopravvive. T81f passa solo da `run_turn`, e T81e vede `rifletti` solo con il valore di default. Correzione: un controllo analogo con l'env a `"0"` che chiami `rifletti`. La riserva va tracciata in `stato_progetto.md`.

Il resto del diff (`gas.py`, `modules/notte/notte.py`, `reports/setup_notte.md`, `tests/test_unit_notte.py`) è quello già visto in #228. Non l'ho riesaminato oltre ai punti indicati.

**Rischio escluso:** non ho rieseguito pytest (786 passed è un dato tuo, non riprodotto); ho eseguito solo la suite del kernel. Non ho verificato il comportamento reale dell'SDK con `max_retries=0` contro un provider vero: in sviluppo non posso riprodurlo senza rete e chiavi, e il test usa un client finto.

**Memoria:** ho aggiunto la riga #229 in `.claude/agents/memoria_revisore.md`, senza lezioni nuove (R-229-1 è un'applicazione della lezione #228). L'ho committata da sola con `scripts/commit_memoria_revisore.sh`: commit `66d4126`.

Possiedi il commit: puoi creare il marcatore con `bash scripts/segna_review_ok.sh` e committare, tracciando R-229-1 in `reports/stato_progetto.md`.

### Review #230 (diff staged di f3ff0c6, prima versione)

VERDETTO: APPROVATO CON RISERVE

Le modifiche chiudono V-1, V-2 e V-3 della verifica esterna su #163. Il nuovo test T81g è nel punto giusto e le frasi sull'SDK sono vere sul codice installato (openai 2.43.0), con un'imprecisione cosmetica: il caso del 429 è citato come unico, ma non lo è.

**Elementi del diff esaminati**

1. `tests/test_unit_kernel.py:7234` — T81g crea un kernel nuovo (`_k81r`), gli dà una history di 2 messaggi e chiama `rifletti()`. Viene subito dopo T81f, quando l'env è ancora `GAS_PROVIDER_MAX_RETRIES="0"` (impostata a :7229), e dopo un `_retries81.clear()`.
   - Rischi esaminati:
     - ordine sbagliato, cioè il test gira con l'env già ripristinata;
     - kernel creato prima dell'override, quindi con la costante di classe;
     - `rifletti` che esce prima di creare il client, lasciando la lista vuota.
   - Tutti e tre esclusi: è tutto dentro il `try`, il kernel nasce dopo l'override e la condizione `_rt_rifl81 != []` respinge la lista vuota. Ho rieseguito la suite: `[PASS] T81g … retries visti: [0]`, `714 PASS, 0 FAIL`.
   - Esito: **ok**.

2. `tests/test_unit_kernel.py:7240` — il `finally` rimette a posto `GAS_PROVIDER_MAX_RETRIES`, cancellandola se prima non c'era. Ripristina anche `gas.OpenAI`, `GAS_PROVIDER_TIMEOUT_SEC` e `GEMINI_API_KEY`.
   - Rischio esaminato: l'env "0" che rimane impostata e sporca i test successivi.
   - Esito: **ok**. Nota non bloccante: se `rifletti` sollevasse un'eccezione, il controllo darebbe `NameError` su `_rt_rifl81`. È lo stesso schema già usato per T81a-f e `rifletti` comunque non solleva (§9).

3. `gas.py:1006` — commento su `PROVIDER_TIMEOUT_SEC`: "x3 coi retry di default dell'SDK; qui x2".
   - Rischio esaminato: un numero sbagliato.
   - Verificato su `openai/_constants.py` (righe 9-10 dell'SDK): `DEFAULT_TIMEOUT` è 600s e `DEFAULT_MAX_RETRIES=2`, cioè 3 tentativi. Qui `PROVIDER_MAX_RETRIES=1`, cioè 2 tentativi.
   - Esito: **ok**. È solo un commento, il codice non cambia.

4. `modules/notte/notte.py:39` e `reports/setup_notte.md` §2 — "Retry-After max 60s per ritentativo; timeout per fase di rete, ordine di grandezza".
   - Verificato su `openai/_base_client.py` (righe 780-782 dell'SDK): Retry-After viene rispettato solo se `0 < x <= 60`. Altrimenti l'SDK aspetta al massimo 8s (`MAX_RETRY_DELAY`, più una piccola variazione casuale).
   - `httpx.Timeout(120)` mette 120s su ognuna delle fasi `connect`/`read`/`write`/`pool`, non sull'intera risposta. Quindi "per fase di rete" è vero.
   - Esito: **riserva cosmetica R-230-1**. Retry-After vale per ogni risposta che l'SDK ritenta (408, 409, 429, 5xx), non solo per i 429 (`_should_retry`, riga 795 dell'SDK). Il testo dovrebbe dire "una risposta con Retry-After (es. 429)". Il conto di fondo non cambia.

5. `reports/stato_progetto.md`, voce 6 — R-229-1 barrata e chiusa, aperta V-4 (cosmetica). È coerente con lo stato reale. Esito: **ok**.

**Controlli del progetto (Wall of Shame e guardrail)**: nessuno slicing diretto della history, nessuna simulazione dell'output dei tool. Il finto `OpenAI` è una sostituzione del client dentro il test, non un output simulato. I guardrail (cap 10 iterazioni, `_get_window`, fallback §9) non sono toccati.

**Rischio esplicitamente escluso**: non ho rifatto la mutation (`max_retries=GasKernel.PROVIDER_MAX_RETRIES` nel client di `rifletti`). Avevi chiesto niente checkout/stash e non volevo modificare file del motore durante la review. Mi baso sul tuo `[FAIL] T81g … retries visti: [1]` e sul ragionamento: con la costante di classe il client vedrebbe 1, e la condizione `all(r == 0)` lo respinge. Non ho rilanciato pytest (786): ho rieseguito solo la suite del kernel.

**Riserva da tracciare in stato_progetto.md**
- R-230-1 (COSMETICA): in `modules/notte/notte.py:39` e `reports/setup_notte.md` §2, "un 429 con Retry-After" va reso generico (Retry-After vale per tutti gli status ritentati dall'SDK).

**Memoria**: aggiunta la riga #230 in `.claude/agents/memoria_revisore.md`, committata da sola con `bdebf53`. Il diff staged è rimasto intatto (5 file, +17/-5).

### Review #231 (delta R-230-1, diff finale di f3ff0c6)

VERDETTO: APPROVATO

Ho ricontrollato le modifiche fatte dopo la review #230: cambia solo il testo dei commenti e della documentazione, il codice eseguibile è lo stesso già revisionato. La riserva R-230-1 (testo che citava solo il caso 429) è chiusa.

Elementi del diff esaminati:

1. `modules/notte/notte.py:39` — il commento ora dice che l'attesa chiesta dal provider (Retry-After) vale per qualunque risposta che l'SDK ritenta (429, 5xx...), fino a 60s per ritentativo. Rischio esaminato: che il testo non corrisponda a cosa fa davvero l'SDK. È coerente con la verifica fatta nella #230 su openai 2.43.0 (`_base_client.py`, riga 781 dell'SDK, attesa accettata solo tra 0 e 60s, per ogni stato ritentato). Il file si analizza ancora senza errori di sintassi (`ast.parse`) e la modifica tocca solo il commento iniziale (docstring). — ok
2. `reports/setup_notte.md:31` — la guida di setup ora dice "un'attesa chiesta dal provider (Retry-After, es. su un 429) aggiunge fino a 60s per ritentativo". Rischio esaminato: che torni a restringere il caso al solo 429. "es." lo presenta come esempio, non come elenco completo, quindi va bene. Da notare solo una parentesi dentro un'altra parentesi: è un dettaglio di stile, non lo apro come riserva. — ok
3. `reports/stato_progetto.md:356` — la voce 6 segna R-230-1 come chiusa e lascia aperta V-4 (voce troppo lunga). Coerente. — ok
4. `gas.py:1006-1008` e `tests/test_unit_kernel.py:7234-7239,7273-7274` — sono identici a quanto approvato nella #230: commento di `PROVIDER_TIMEOUT_SEC` e test T81g. — ok

Cosa NON ho verificato:
- Non ho rilanciato la suite di test: le modifiche nuove sono solo nei commenti, nella documentazione e nel file di stato, mentre il codice e il test T81g sono rimasti uguali a quanto già fatto girare nella #230 (713/0).
- Il comportamento reale di Retry-After con un provider vero non è verificato: servirebbe un vero 429 o 5xx con quell'intestazione, cosa che in sviluppo non posso riprodurre.

Memoria: ho aggiunto la riga `#231` in coda a `.claude/agents/memoria_revisore.md` e l'ho committata con `scripts/commit_memoria_revisore.sh`, che è terminato senza errori.

Nota dell'agente: il "713/0" citato sopra è il dato di #229; dopo T81g la suite del kernel dà 714/0 (§5).

## §5 DELTA TEST DEL MOTORE

Kernel 711 → 714 PASS (T81e, T81f, T81g nuovi), 0 FAIL. `pytest tests/` 786 passed (invariato: la suite kernel è un file a sé). Blocco reale (dopo `f3ff0c6`):

```
[PASS] T81e V-2 bot #162: run_turn e rifletti con 1 solo tentativo extra dell'SDK; GAS_PROVIDER_MAX_RETRIES override, minimo 0, sporco → default — retries visti: [1, 1]; env: (0, 0, 1)
[PASS] T81f R-228-1: GAS_PROVIDER_MAX_RETRIES=0 arriva al client di run_turn — retries visti: [0]
[PASS] T81g R-229-1: GAS_PROVIDER_MAX_RETRIES=0 arriva al client di rifletti — retries visti: [0]
=== RIEPILOGO: 714 PASS, 0 FAIL ===
786 passed in 108.13s (0:01:48)
```

Mutation dell'agente: `max_retries=GasKernel.PROVIDER_MAX_RETRIES` nel client di `run_turn` → `[FAIL] T81f … retries visti: [1]` (712/1); nel client di `rifletti` → `[FAIL] T81g … retries visti: [1]` (713/1). Ripristinato entrambe le volte, `gas.py` identico (cmp).

## §6 STATO CI

`gh` non autenticato nel container: stato letto dai check della PR #163 con lo strumento GitHub collegato, alla scrittura dell'handoff.

- `9581ed0`: run 37915271518 — `handoff-check` failure (sul branch c'era ancora l'handoff della sessione #162), `unit-suite` success (dato della verifica del bot).
- `653a625` (primo fine-task): run 37915500124 — `unit-suite` success, `handoff-check` success. Run 37915508092 (bot): `smista` success, `verifica` success, `esito` success; check `verifica-bot` success (verdetto testuale APPROVATO CON RISERVE, sotto).
- `3d5e5ef`, `66d4126`, `bdebf53`, `a6886a4`: nessuna run su questo SHA (pushati insieme ad altri, testati solo come parte dell'albero della testa).
- `f3ff0c6` e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **V-4 verifica esterna (agente, COSMETICA)**: voce 6 di `stato_progetto.md` è un paragrafo di ~4 KB, contro §11 (stato snello): da spostare nello storico.
- Preesistenti, già tracciate in `stato_progetto.md` voce 6: R-226-4, R-227-1 (BASSE).
- Chiuse in questa sessione: R-228-1, R-228-2, R-229-1, R-230-1; V-1/V-2/V-3 verifica esterna (agente); V-1/V-2 bot su `653a625`.

### Verdetto bot su `653a625` (gas-verificatore, integrale)

```
VERIFICA ESTERNA #163 — APPROVATO CON RISERVE
FINDING:
- V-1 (COSMETICA) — Testo non allineato alla modifica: gas.py:1005-1007 (commento di PROVIDER_TIMEOUT_SEC) dice ancora che senza timeout l'SDK aspetta 600s per tentativo «(x3 coi retry)», mentre otto righe sotto PROVIDER_MAX_RETRIES=1 porta i tentativi a 2; e reports/stato_progetto.md voce 6 scrive «V-3 sintesi dello stat dell'handoff dichiarata senza handoff.md», ma la nota reale di handoff.md §2 dice che la sintesi INCLUDE handoff.md con conteggi approssimati. Sonda: lettura delle righe citate. Fix: «x(1+PROVIDER_MAX_RETRIES) coi retry» nel commento; in stato_progetto «sintesi con handoff.md dichiarato approssimato».
- V-2 (BASSA) — Copertura di test incompleta nata in questa PR (già tracciata come R-229-1): l'override env è provato sul client di run_turn (T81f) ma non su quello di rifletti (gas.py:1975). T81e confronta rifletti solo col default 1, quindi la mutation «max_retries=GasKernel.PROVIDER_MAX_RETRIES» in rifletti sopravvive. Fix: con env "0" chiamare anche rifletti su un kernel nuovo e attendersi [0].
RACCOMANDAZIONE: mergiabile a giudizio dell'operatore: il verdetto è con riserve, quindi per la regola di CLAUDE.md niente merge autonomo dell'agente.
```
(Estratto delle sezioni FINDING e RACCOMANDAZIONE; il testo completo con CLAIM VERIFICATI e NON VERIFICATO è nella review della PR: https://github.com/Gasss23/Gas/pull/163#pullrequestreview-5468693741.) Esito: commento → `f3ff0c6`; frase di stato_progetto → commit di fine-task; V-2 → T81g in `f3ff0c6`.

### Verifica esterna dell'agente (contesto vergine, su `653a625`)

```
VERIFICA ESTERNA PR #163 — APPROVATO CON RISERVE
FINDING
- V-1 (BASSA, test) — È la R-229-1 già dichiarata. Fix proposto: un test con GAS_PROVIDER_MAX_RETRIES=0 che chiami rifletti e controlli [0] nel client finto.
- V-2 (BASSA, doc/commento) — Il commento di gas.py:1007 dice ancora "aspetta fino a 600s per tentativo (x3 coi retry)". Fix: aggiungere "(x2 con PROVIDER_MAX_RETRIES=1)" o riscriverlo.
- V-3 (BASSA, accuratezza del caso peggiore) — Le "~36 min" sono un tetto approssimato, non un limite: il timeout httpx a 120 s vale per singola fase di rete, e un 429 con Retry-After fa attendere l'SDK fino a 60 s per ritentativo. Fix: scrivere "~36 min + eventuali Retry-After (max 60 s per ritentativo)".
- V-4 (COSMETICA) — reports/stato_progetto.md voce 6 è un paragrafo di circa 4 KB su una sola riga, contro la regola §11 di tenere il file snello.
RACCOMANDAZIONE
Il merge è possibile quando unit-suite è verde. Per la regola di merge autonomo, un verdetto testuale APPROVATO CON RISERVE del bot non basta: decide l'operatore. Prima di altro lavoro conviene chiudere V-1 e allineare il commento V-2 e la nota V-3. Sono tutte BASSE e nessuna blocca il merge.
```
(Estratto delle sezioni FINDING e RACCOMANDAZIONE.) Esito: V-1, V-2, V-3 chiuse in `f3ff0c6`; V-4 deferita.
