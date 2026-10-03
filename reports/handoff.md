# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-03 — Fetta C3 cancello: chiusura R-c3-1 + nuova review #126 (feat/cancello-c3)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #111 (https://github.com/Gasss23/Gas/pull/111). NB: il merge NON attiva il cancello — la coda non è collegata al loop, lo stub C2 resta attivo fino a C4.
2. PR #109: superata da #110, da chiudere SENZA merge (la chiude l'operatore).
3. C4 (proposta, non eseguita): collegamento coda↔loop e rimozione stub C2, canale umano Telegram, read-back, esito "in attesa"; R-c3-1b da chiudere prima o dentro C4.

---

## §1 SCOPE & ESITO FETTE

**Stato reale:** C3 = coda approvazioni pronta in `modules/memory/store.py`, **NON collegata al loop**. Lo stub C2 è ancora attivo: oggi le azioni da approvare partono **SENZA blocco**. Collegamento al loop, canale umano, read-back ed esito "in attesa" = C4. Conflitto spec/prompt risolto dall'operatore con "C3 come da spec".

- **C3 — coda approvazioni SQLite (2026-10-02)**: `FATTA` — store.py + T73a-g, review #125 (superata da #126).
- **Invarianti 1, 5, 6 (canale umano) e 8 del prompt C3**: `DEFERITA — a C4 (richiedono il collegamento al loop / canale umano)`.
- **A) R-c3-1 — righe con tipi errati → diniego fail-closed**: `FATTA` — commit `20dcadb`, `_approval_row_valida()` in get/resolve/pending + WARN; test T73h (INSERT grezzo). Controprova: pre-fix T73h fallisce con AttributeError.
- **R-c3-2..5**: `SALTATA — fuori mandato (decisione operatore: solo R-c3-1)`.
- **B) Nuova review Opus sul diff completo**: `FATTA` — #126 APPROVATO CON RISERVE (§4); #125 verbatim in §4-bis.
- **C) Onestà nei canonici**: `FATTA` — stato_progetto.md, ultimo_report.md, questo §1.
- **D) Suite prima/dopo**: `FATTA` — vedi §5.
- **Fine-task**: `FATTA` — push branch + PR #111.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +
 modules/memory/store.py            | 331 +++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  30 ++--
 reports/handoff.md                 | 249 +++++++++++++---------------
 reports/stato_progetto.md          |   7 +-
 reports/ultimo_report.md           |  51 +++---
 tests/test_unit_kernel.py          | 308 ++++++++++++++++++++++++++++++++++
 7 files changed, 805 insertions(+), 175 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
20dcadb fix(cancello-c3): R-c3-1 — righe approvals con tipi errati → diniego fail-closed, mai eccezione (review #126 APPROVATO CON RISERVE)
0a9ccc0 chore(revisore): memoria review #126 — APPROVATO CON RISERVE
81086db docs(cancello-c3): report + handoff + diff_sessione — fine-task C3
4f16a65 feat(cancello-c3): coda approvazioni SQLite in store.py (review #125 APPROVATO CON RISERVE)
aa0b0d0 chore(revisore): memoria review #125 — APPROVATO CON RISERVE
```

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore `4f16a65` (C3) + `20dcadb` (fix R-c3-1) — verdetto integrale review #126 sul diff completo di sessione:

## Verdetto review #126: APPROVATO CON RISERVE

Questa review sostituisce la #125 per quanto riguarda il formato: ogni path è completo e ogni numero di riga l'ho controllato con grep -n sul working tree attuale.

Ho fatto le tre letture obbligatorie: CLAUDE.md (il canone è già nel contesto, sez. 5/8/9), reports/stato_progetto.md (letto per sezioni, in particolare il finding C3 alla riga 89) e .claude/agents/memoria_revisore.md (le lezioni da #114 a #125, compresa quella del 2026-10-02 sui tipi dinamici di SQLite).

Diff esaminato: `git diff --cached ce3d3929... -- gas.py brains modules tests`, cioè modules/memory/store.py +331 e tests/test_unit_kernel.py +308. gas.py e brains/ non sono toccati: lo stub C2 resta fino a C4, come da scope. La parte C3 di base era già stata vista nella #125. Qui il controllo si concentra sul fix R-c3-1 in staging.

### Elementi del diff esaminati

1. **modules/memory/store.py:279** (`_approval_row_valida`, con l'helper `_num` a :275)
   - Cosa fa: controlla il tipo di ogni colonna, dove `_num` accetta int/float ed esclude bool.
   - Rischio: falsi negativi su righe sane, o colonne dimenticate.
   - Verifica: copre tutte le colonne dello schema e i nullable sono gestiti. Una riga sana creata da enqueue passa: il check finale di T73h lo conferma, approvazione riuscita.
   - Esito: **ok**.
2. **modules/memory/store.py:1496** (`get_approval`)
   - Cosa fa: se la riga non è valida restituisce None e scrive un WARNING, prima di `hash_args`.
   - Rischio: AttributeError su un BLOB.
   - Esito: **ok**.
3. **modules/memory/store.py:1537** (`resolve_approval`)
   - Cosa fa: il check sta dentro `BEGIN IMMEDIATE`, subito dopo la SELECT \* e prima di qualsiasi UPDATE. In caso di riga non valida fa rollback e restituisce (False, msg) con WARNING.
   - Rischio: scrittura parziale, oppure lock lasciato aperto.
   - Verifica: il rollback è esplicito e non c'è nessuna scrittura (T73h: lo stato nel DB resta 'pending').
   - Esito: **ok**.
4. **modules/memory/store.py:1591** (`get_pending_approvals`)
   - Cosa fa: le righe non valide vengono escluse una per una con WARNING, invece di far fallire tutta la lista.
   - Rischio: una riga corrotta che rende inutilizzabile l'intera coda.
   - Verifica: le righe sane restano visibili.
   - Esito: **ok**.
5. **modules/memory/store.py:1501 / :1573 / :1597** (except estesi a TypeError/ValueError/AttributeError)
   - Cosa fa: rete finale.
   - Rischio: mascherare bug di programmazione.
   - Verifica: è accettabile, perché il ramo restituisce comunque un diniego con WARNING (§9 fail-closed).
   - Esito: **ok**.
6. **tests/test_unit_kernel.py:5270-5325** (T73h)
   - Cosa fa: 3 INSERT grezzi e precondizione `typeof` verificata a :5287. Controlla che get/resolve/pending neghino, che lo stato nel DB sia invariato, che ci siano almeno 7 WARN (:5319) e che la coda resti usabile (:5323).
   - Rischio: test non mordace.
   - Mutation test (patch in memoria, repo intatto): con `_approval_row_valida = lambda d: True` cadono 5 check di T73h (467 PASS / 10 FAIL). Il caso più grave: la riga con `telegram_user_id` TEXT viene **approvata**, perché quella colonna viene scritta e non letta in un'espressione Python, quindi nessun except scatta. Il validatore quindi serve davvero: gli except estesi da soli non bastano.
   - Esito: **ok**.
7. **tests/test_unit_kernel.py:5021** (`import logging`)
   - Rischio: effetti collaterali.
   - Verifica: l'handler viene aggiunto e poi rimosso nel `finally`, e il nome del logger corrisponde a `getLogger(__name__)` (modules/memory/store.py:50).
   - Esito: **ok**.

### Riproduzione
- `python tests/test_unit_kernel.py`: **472 PASS / 5 FAIL**. I 5 falliti sono T11c2, T11e, T12a, T12c, T12e, tutti F-mac-1 (bwrap assente su macOS). Tutti i check di T73h passano.
- pytest sulle 7 suite non-kernel: **227 passed**.
- Il comando generico `pytest tests` va in INTERNALERROR perché test_unit_kernel.py chiama sys.exit. È un limite noto di quella suite, non dipende da questo diff.

### Riserve
- **R-c3-1b (minore, da chiudere prima di C4)**: riguarda la nota che avevi segnalato tu. Una riga con `ts_expiry` non numerico resta 'pending' per sempre. Il motivo: `expire_stale_approvals` (modules/memory/store.py:1601) usa `ts_expiry <= ?`, e in SQLite un TEXT è sempre maggiore di un REAL. Per il contratto fail-closed è **accettabile adesso**: la riga non si legge e non si approva, quindi non ci sono falle di sicurezza. Resta però una riga zombie. Se C4 conta le pending (limiti, dedup, "una per turno") o le mostra all'operatore, potrebbe dare fastidio. Fix suggerito per C4: in expire, marcare 'rejected'/'kernel_revoca' (oppure 'expired') le pending con `typeof(ts_expiry) NOT IN ('integer','real')`, e aggiungere un test.
- R-c3-2..5 restano aperte come da mandato: non le ho contate come difetti di questo fix.

### Rischi esplicitamente esclusi
- Non ho verificato che i WARNING finiscano davvero nel file gas_debug.log. Il test cattura il logger del modulo con un handler in memoria. Che arrivino al file dipende dalla configurazione del root logger in gas.py, che questo diff non tocca.
- Il comportamento su Linux/VPS (CI) non l'ho riprodotto qui. Il diff non tocca codice dipendente dalla piattaforma, quindi lo lascio alla CI `unit-suite`.
- Non ho rifatto la controprova sul codice pre-fix di HEAD. La mutation "validatore → True" la copre in modo equivalente.

### Memoria
- Riga contatore #126 e una lezione aggiunte a /Users/gas/Gas/.claude/agents/memoria_revisore.md. La lezione: mutation "validatore → True" per capire se il validatore serve davvero o se bastano gli except.
- Committate con `bash scripts/commit_memoria_revisore.sh` (commit `0a9ccc0`). Lo staging di modules/memory/store.py e tests/test_unit_kernel.py è intatto.

Gate: commit consentito. La riserva R-c3-1b va registrata in reports/stato_progetto.md.

## §4-bis Verdetto precedente — superato dalla review #126

Motivo: path abbreviati (es. `store.py:…` invece di `modules/memory/store.py:…`) + una citazione errata (store.py:5131). Testo VERBATIM, non ritoccato:

Commit motore `4f16a65` — verdetto integrale review #125:

## Verdetto review #125 — Fetta C3, coda approvazioni SQLite (branch feat/cancello-c3, diff staged)

**ESITO: APPROVATO CON RISERVE**

Prima di iniziare ho letto quanto previsto: CLAUDE.md (sez. 5, 8, 9 e 10), reports/stato_progetto.md (letto in modo mirato), la mia memoria (.claude/agents/memoria_revisore.md, fino alla #124) e le sezioni di design_cancello.md che servivano: §4a–§4f, §C3–§C5 e §8c/§8d.

Ho rilanciato la suite: `tests/test_unit_kernel.py` dà **463 PASS / 5 FAIL**. I 5 FAIL sono quelli già noti di F-mac-1 (T11c2, T11e, T12a, T12c, T12e: manca bwrap su macOS). Tutti i 40 check T73 sono verdi. Le sonde sugli edge case le ho fatte con uno script nello scratchpad, senza toccare il repo.

### Elementi del diff esaminati

1. `modules/memory/store.py:182` (tabella `approvals`) e `:224` (trigger `approvals_payload_immutabile`), più gli altri 3 trigger: una richiesta nasce solo `pending`, la DELETE è vietata, lo stato non cambia più dopo la risoluzione, il payload non cambia mai.
   - Rischi esaminati: aggiramento con SQL grezzo e con `INSERT OR REPLACE`.
   - `recursive_triggers = ON` era già attivo in `_connect` (store.py:421), quindi il percorso REPLACE→DELETE resta bloccato. Questo lo coprono T73c (store.py:5131 non esiste: il test è a tests/test_unit_kernel.py:5131) e T73b.
   - Esito: **ok**.
2. `modules/memory/store.py:1500` (`BEGIN IMMEDIATE` dentro `with self._connect()`), insieme a `WHERE stato='pending'` e al controllo `rowcount != 1`. Le funzioni toccate sono resolve, expire e il ramo di revoca.
   - Rischi esaminati: doppia risoluzione e race tra due callback.
   - Il blocco di scrittura immediato più l'UPDATE condizionato rendono la risoluzione idempotente. Un `return` dentro il `with` va bene: chiude la transazione con commit o rollback.
   - Esito: **ok**.
3. `modules/memory/store.py:1469` (`hash_args(d["tool_args_json"])` in get_approval) e `:1511` (`now >= row["ts_expiry"]` in resolve_approval).
   - Rischio esaminato: coda corrotta, che secondo il contratto deve dare "mai eccezione".
   - **Riprodotto**: se una riga viene inserita con SQL grezzo con `tool_args_json` di tipo BLOB, sia get_approval sia resolve_approval sollevano `AttributeError: 'bytes' object has no attribute 'encode'`. Se `ts_expiry` è TEXT, resolve_approval solleva `TypeError`.
   - Con `ts_expiry` TEXT la riga resta inoltre per sempre in get_pending_approvals (in SQLite TEXT > REAL) e expire_stale_approvals non la fa mai scadere.
   - Gli except prendono solo `(sqlite3.Error, OSError)`.
   - L'esito resta fail-closed (nessuna approvazione concessa), ma l'eccezione arriva al chiamante, cioè al thread del bot in C4.
   - Esito: **riserva R-c3-1**.
4. `modules/memory/store.py:1446` (`now + timeout_secs`).
   - Rischio esaminato: parametro `timeout_secs` non validato.
   - Riprodotto: con `timeout_secs="10"` si ha un `TypeError` non intercettato; con `float("inf")` la richiesta non scade mai.
   - Il parametro lo passa il kernel, non il modello.
   - Esito: **riserva R-c3-2** (minore).
5. `modules/memory/store.py:1490` (whitelist di `risolto_da`).
   - Rischio esaminato: correttezza del dato di audit.
   - Riprodotto: `resolve_approval(id, "approved", 1, risolto_da="kernel_revoca")` restituisce `(True, '')`, cioè un'approvazione registrata come revoca del kernel. In più `rejected` accetta `telegram_user_id="pippo"`, che viene salvato come testo.
   - Esito: **riserve R-c3-3 e R-c3-4** (minori).
6. `tests/test_unit_kernel.py:5203-5204` (T73e: DB corrotto, tabella assente, file sparito) e `:5262` (T73g, round-trip agentico §7).
   - Rischi esaminati: test reali o mockati, e se discriminano davvero.
   - Il DB è un vero SQLite in una directory temporanea, senza alcun mock della coda. T73g esegue 2 tool call reali più la risposta finale e verifica che la richiesta resti `pending`.
   - Nessun test copre le righe con tipo sbagliato (vedi R-c3-1).
   - Esito: **ok**.
7. `tests/test_unit_kernel.py:5247` (T73f) e verifica diretta del codice.
   - Rischio esaminato: un tool di approvazione esposto al modello.
   - `grep approv gas.py` trova solo il commento dello stub C2 (gas.py:1948), che non è nel diff e resta fino a C4 come deciso dall'operatore.
   - Non c'è nessun tool di approvazione in tools_schema né in GATE_ALLOWLIST, e `execute_tool_call` risponde "Tool non trovato.".
   - Esito: **ok**.

Ho controllato il Wall of Shame: il diff non fa slicing della history e non simula output dei tool. Rispetta "zero gas.py", come da scope deciso.

### Riserve (da tracciare in stato_progetto.md)

- **R-c3-1 (media, da chiudere PRIMA di C4)**: va reso vero il contratto "coda corrotta → mai eccezione" per righe con tipi sbagliati (store.py:1469, :1511). Ci sono due strade: aggiungere allo schema `CHECK(typeof(tool_args_json)='text')` e `CHECK(typeof(ts_expiry) IN ('real','integer'))` (la tabella è nuova, quindi non serve migrazione), oppure intercettare `TypeError`/`AttributeError` sui valori letti. Serve anche un test con INSERT grezzo di tipi sbagliati.
- **R-c3-2 (minore)**: validare `timeout_secs` (intero finito; altrimenti default e WARN).
- **R-c3-3 (minore)**: `approved` deve richiedere `risolto_da == "telegram_user"`.
- **R-c3-4 (minore)**: anche `rejected` dovrebbe pretendere `telegram_user_id` intero o None.
- **R-c3-5 (cosmetica)**: get/resolve/pending/expire non controllano `self.available`. Se il file sparisce, `sqlite3.connect` ricrea un `.db` vuoto senza schema (riprodotto). Non porta a crash: l'errore viene intercettato e si ha un diniego.

### Rischi esplicitamente esclusi

- **Concorrenza reale multi-processo** (due processi che risolvono nello stesso istante): non l'ho verificata con un test. La valutazione si basa solo sulla lettura del codice (`BEGIN IMMEDIATE`, `timeout=10`, `WHERE stato='pending'`). Il bot Telegram che la eserciterebbe non esiste ancora (C4).
- **Comportamento su VPS/Linux**: non riproducibile in dev su macOS, lo copre la CI.
- **Limite di read-back Telegram (~4096 caratteri, §4c)**: fuori scope, riguarda C4 come deciso dall'operatore.

### Memoria del revisore

Ho aggiunto in `/Users/gas/Gas/.claude/agents/memoria_revisore.md` la riga contatore #125 e una lezione (except sqlite3.Error non basta con la tipizzazione dinamica di SQLite). Nessun IP letterale. Il file è committato da solo con `scripts/commit_memoria_revisore.sh` (commit `aa0b0d0`). Il diff staged (store.py, stato_progetto.md, test_unit_kernel.py) resta intatto nell'index.

### Correzione nel testo sopra

Al punto 1 ho scritto per errore "store.py:5131": il riferimento giusto è `tests/test_unit_kernel.py:5131`, come indicato lì stesso.

File rilevanti:
- /Users/gas/Gas/modules/memory/store.py
- /Users/gas/Gas/tests/test_unit_kernel.py
- /Users/gas/Gas/reports/design_cancello.md
- /Users/gas/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

Kernel: prima (HEAD `0a9ccc0`, pre-fix) `463 PASS, 5 FAIL` → dopo (`20dcadb`) `472 PASS, 5 FAIL` (+9 check T73h).

Prima:
```
=== RIEPILOGO: 463 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
```

Dopo:
```
=== RIEPILOGO: 472 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
```

I 5 FAIL sono F-mac-1 (bwrap assente su macOS), fuori scope, invariati. pytest (gasmerge, gate, handoff_check, hooks, voice_server, voice_stt, voice_tts): 227 passed prima e dopo.

## §6 STATO CI

```
completed	failure	fix(cancello-c3): R-c3-1 — righe approvals con tipi errati → diniego …	CI	feat/cancello-c3	push	37080174058	56s	2026-10-03T00:00:29Z
completed	failure	docs(cancello-c3): report + handoff + diff_sessione — fine-task C3	CI	feat/cancello-c3	push	37079230353	1m6s	2026-10-02T23:47:39Z
completed	success	Merge pull request #110 from Gasss23/chore/hook-fine-task-obbligatorio	CI	main	push	37056446724	53s	2026-10-02T19:47:55Z
```

- `20dcadb`: run 37080174058 — unit-suite **success**, handoff-check **failure** (handoff a quel SHA conteneva ancora il §4 con il verdetto #125, che fallisce check_verdetto).
- `0a9ccc0`: nessuna run su questo SHA (pushato insieme a `20dcadb`).
- `81086db`: run 37079230353 — unit-suite **success**, handoff-check **failure** (check_verdetto: "citazioni non verificabili in §4", verdetto #125).
- `4f16a65`: nessuna run su questo SHA.
- `aa0b0d0`: nessuna run su questo SHA.
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-c3-1b (minore, prima di C4): riga con `ts_expiry` non numerico resta 'pending' zombie; `expire_stale_approvals` dovrebbe marcarla + test.
- R-c3-2 (minore): validare `timeout_secs`.
- R-c3-3 (minore): `approved` deve richiedere `risolto_da == "telegram_user"`.
- R-c3-4 (minore): `rejected` deve pretendere `telegram_user_id` int o None.
- R-c3-5 (cosmetica): get/resolve/pending/expire non controllano `self.available`.
- Rischio escluso dal revisore: arrivo effettivo dei WARNING in `gas_debug.log` non verificato (test con handler in memoria).
- R-c3-1: CHIUSA (`20dcadb`, review #126).
