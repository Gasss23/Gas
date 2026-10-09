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
- **R-228-1, R-228-2**: `FATTA` (stessa fetta). **R-229-1**: `DEFERITA` — BASSA, solo test, tracciata in `stato_progetto.md`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 gas.py                             |  13 +++++++++++--
 modules/notte/notte.py             |   6 ++++--
 reports/diff_sessione.md           |  16 ++++++++--------
 reports/handoff.md                 | 176 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------------------------------------------------------
 reports/setup_notte.md             |   5 +++--
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  24 ++++++++++++------------
 tests/test_unit_kernel.py          |  49 +++++++++++++++++++++++++++++++++++++------------
 tests/test_unit_notte.py           |   2 +-
 10 files changed, 160 insertions(+), 136 deletions(-)
```

Nota (V-3 bot #162): la riga di sintesi include `reports/handoff.md`, ma i SUOI conteggi sono approssimati per costruzione (lo stat è generato prima dell'ultima scrittura del file stesso). Il set di file è esatto; la CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

Kernel 711 → 713 PASS (T81e, T81f nuovi), 0 FAIL. `pytest tests/` 786 passed (invariato: la suite kernel è un file a sé). Blocco reale:

```
[PASS] T81a run_turn costruisce il client col timeout del kernel (default 120s) — timeout visti: [120]
[PASS] T81b rifletti costruisce il client col timeout del kernel — timeout visti: [120]
[PASS] T81d R-226-1: Ollama locale ha il suo timeout (600s), gli altri rung 120s — (600, 120)
[PASS] T81c GAS_PROVIDER_TIMEOUT_SEC: override, minimo 5, valore sporco → default — (45, 5, 120)
[PASS] T81e V-2 bot #162: run_turn e rifletti con 1 solo tentativo extra dell'SDK; GAS_PROVIDER_MAX_RETRIES override, minimo 0, sporco → default — retries visti: [1, 1]; env: (0, 0, 1)
[PASS] T81f R-228-1: GAS_PROVIDER_MAX_RETRIES=0 arriva al client di run_turn — retries visti: [0]
=== RIEPILOGO: 713 PASS, 0 FAIL ===
786 passed in 108.54s (0:01:48)
```

Mutation dell'agente: `max_retries=GasKernel.PROVIDER_MAX_RETRIES` nel client di `run_turn` → `[FAIL] T81f … retries visti: [1]` (712/1); ripristinato, `gas.py` identico allo staged.

## §6 STATO CI

`gh` non autenticato nel container: stato letto dai check della PR #163 con lo strumento GitHub collegato, alla scrittura dell'handoff.

- `9581ed0` (head pushato prima di questo commit di fine-task): run 37915271518 — `handoff-check` **failure** (atteso: sul branch c'era ancora l'handoff della sessione #162, che questo commit sostituisce), `unit-suite` in_progress. Run 37915290053 (verifica-bot): `smista`/`esito`/`verifica` skipped (etichetta `verifica` non ancora messa).
- `66d4126`, `3d5e5ef`: nessuna run su questo SHA (pushati insieme a 9581ed0, testati solo come parte del suo albero).
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-229-1 (BASSA, test)**: manca un controllo con `GAS_PROVIDER_MAX_RETRIES=0` che passi da `rifletti` (oggi la mutation `GasKernel.PROVIDER_MAX_RETRIES` in `rifletti` sopravvive).
- Preesistenti, già tracciate in `stato_progetto.md` voce 6: R-226-4, R-227-1 (BASSE).
