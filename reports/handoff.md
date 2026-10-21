# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 (dopo il merge di #236) — ultime riserve del bot sulla storia condivisa

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #240 (https://github.com/Gasss23/Gas/pull/240; numero e URL dall'API GitHub): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10).

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #236**: `FATTA` — su richiesta dell'operatore, merge `dec4ce9`.
- **V-1/V-2 bot #236 (5° giro), R-436-1**: `FATTA` — review #438 APPROVATO CON RISERVE.
- **R-438-1 (= V-2 verifica esterna #240)**: `FATTA` — review #439 APPROVATO CON RISERVE (compress-history salva con unione rimandata).
- **R-439-1, V-1 bot #240**: `FATTA` — review #440 APPROVATO CON RISERVE (_save_history dice se ha scritto; T97j controlla i messaggi inviati al provider).
- **R-438-2 (= V-2 bot #240)**: `SALTATA` — limite BASSO dichiarato (scrivere a metà turno senza cambiare la lista rischierebbe duplicati).
- **R7 / R-c4b3-3**: `DEFERITA` — prossima fetta.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 gas.py                             |  40 +++++++++++++++++++++---------
 reports/da_mergiare.md             |  22 ++++++++---------
 reports/diff_sessione.md           |  12 ++++-----
 reports/handoff.md                 | 483 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  27 +++++++-------------
 tests/test_unit_kernel.py          | 105 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 8 files changed, 264 insertions(+), 430 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
28c7f94 fix(storia): _save_history dice se ha scritto; compress-history non dice ok senza salvare (R-439-1); T97j controlla i messaggi inviati al provider (V-1 bot #240)
1f90bc8 chore(revisore): memoria review #440 — APPROVATO CON RISERVE
361400f fix(storia): gas compress-history salva anche con un'unione rimandata, o dice che non ha salvato (R-438-1)
5eb1c1d chore(revisore): memoria review #439 — APPROVATO CON RISERVE
aa7f538 docs(fine-task): report e handoff — ultime riserve del bot sulla storia condivisa (#438)
340326d fix(storia): rinvio a fine turno anche al primo salvataggio, niente duplicati dopo una scrittura fallita, test del finally di run_turn (V-1/V-2 bot #236 5° giro, R-436-1)
012856e chore(revisore): memoria review #438 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #438 (chat Motore) — commit 340326d

## VERDETTO: APPROVATO CON RISERVE

Review #438 (chat Motore). Ho controllato il diff in staging su gas.py e tests/test_unit_kernel.py. Prima ho letto CLAUDE.md, le parti di stato_progetto.md che riguardano la storia e la coda della mia memoria.

**Punti del diff esaminati**
- gas.py:1188 — il rinvio a metà turno («unita is not None and not _turno_chiuso() and not fine_turno») ora vale per entrambi i rami. Rischio esaminato: il rinvio blocca per sempre la scrittura. Ho controllato chi chiama `_save_history`:
  - `_storia_esito_firma` (gas.py:3231) chiude sempre con «Preso atto», senza tool_calls, quindi non viene mai rinviato.
  - Le due chiamate dentro il loop di run_turn (gas.py:4538 e gas.py:4542) e la compressione a inizio turno (gas.py:4318) sono coperte dal finally (gas.py:4578).
  - L'unico chiamante fuori da run_turn è la CLI `compress-history` (vedi R-438-1).
  - Esito: ok.
- gas.py:1176 — il dedupe `suoi = altrui[gia[0]:]` scatta solo se il file dell'altro estende quello già unito (lunghezza e hash). Rischi esaminati:
  - Il ramo 1 dopo un'unione del ramo 2 duplicherebbe i suoi messaggi: è irraggiungibile, perché `nuovi[0]` resta lo stesso messaggio non-user e `nuovi` vuoto porterebbe già al ramo 1.
  - `gia[0] < n_base` non può succedere per costruzione.
  - Esito: ok.
- gas.py:1202 e gas.py:1302 — la base ha il 5° elemento solo dopo un'unione del ramo 2, e `_sync_storia()` lo azzera dopo una scrittura riuscita. Sonda nella copia:
  - lunghezza della base 5 dopo la scrittura fallita, 4 dopo quella riuscita;
  - poi A scrive e B è a metà turno: rinvio attivo, B non vede A2;
  - a fine turno il file è `['B extra','A1','rA1','A2','rA2','B q',None,'7','rB']`, senza duplicati, con flag False.
  - Esito: ok.
- gas.py:952 — l'annotazione `Optional[Tuple[Any, ...]]` è coerente con le tuple da 4 e da 5 elementi. Esito: ok.
- tests/test_unit_kernel.py:7603 — T97j passa davvero dal generatore di run_turn: il bot scrive durante la prima chiamata, poi il provider va giù. Ho rifatto le mutazioni nella copia nello scratchpad:
  - finally tolto → T97j FAIL;
  - rinvio solo nel ramo 2 → T97j FAIL;
  - dedupe tolto → T97k FAIL;
  - 5° elemento mai scritto → T97k FAIL (tests/test_unit_kernel.py:7646).
  - Esito: ok, R-436-1 chiusa.
- tests/test_unit_kernel.py:7489 e tests/test_unit_kernel.py:7655 — T97b e T97g ora chiudono i turni di A con una risposta. È un adeguamento coerente con la nuova regola, non un indebolimento. Esito: ok.

**Suite nella copia:** kernel 993 PASS, 1 FAIL. Il FAIL è T79a ed è dovuto alla copia: senza `git ls-files` trova 0 file. Non dipende dal diff.

**Riserve**
- **R-438-1 BASSA (c'era già prima di questo diff):** `python gas.py compress-history` (gas.py:5230) gira fuori da run_turn. Se la storia finisce a metà turno (turno precedente esaurito) e un altro processo ha scritto, il salvataggio viene rinviato e nessun finally lo recupera. La compressione non viene scritta, ma il comando stampa lo stesso «Compressi N messaggi». Non si perdono dati: sul file resta la storia intera. Il caso c'era già col rinvio del ramo 2 (compressione → nostri non da base → ramo 2). Correzione proposta: chiamare `_save_history(fine_turno=True)` in quel comando, oppure controllare `_storia_rimandata` prima di stampare.
- **R-438-2 (nota, scelta accettabile):** col rinvio anche nel ramo 1, se un altro processo ha scritto, i messaggi del turno in corso restano solo in memoria fino alla fine del turno. Un kill -9 a metà turno li perde, mentre prima venivano scritti a ogni passo dei tool. È il prezzo di «il modello non vede il blocco dell'altro durante il turno»: va dichiarato in stato_progetto.md.

**Cosa NON ho verificato:** due processi reali in parallelo con il lock vero su VPS e il bot Telegram vivo, perché in dev non si riproduce (le prove usano due kernel nello stesso processo). Non ho rilanciato pytest tests/ (1816): ho girato solo la suite kernel e le mutazioni.

La riga #438 è stata scritta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con scripts/commit_memoria_revisore.sh. Lo staging di gas.py e tests/test_unit_kernel.py è intatto.

### Review #439 (chat Motore) — commit 361400f

## VERDETTO: APPROVATO CON RISERVE

Review #439 (chat Motore). Prima di revisionare ho letto CLAUDE.md, la riga di R-438-1 in reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md. Nella copia nello scratchpad (/tmp/claude-0/-home-user-Gas/6049a349-3e7f-5be2-83ac-5dc6a4b4ff3d/scratchpad/c439) la suite del kernel dà **995 PASS 0 FAIL**.

**Cosa ho esaminato nel diff**
- `gas.py:5231` — se l'unione è stata rimandata, il comando chiama `_save_history(fine_turno=True)`. Rischio esaminato: che la scrittura non avvenga perché il comando sta fuori da `run_turn`. Ho tolto la chiamata nella copia (mutazione): la storia resta di 67 messaggi e T97l va in FAIL. Esito: **ok**.
- `gas.py:5234` — se l'unione resta rimandata, stampa «✗ compress-history: compressione NON salvata» e restituisce 1. Rischio esaminato: un falso «✓ Compressi». Ho fatto una sonda in cui la scrittura fallisce solo per il kernel principale, dopo che l'«altro» ha già scritto: rc 1 con il messaggio ✗. Esito: **ok**.
- `tests/test_unit_kernel.py:7649` — T97l. Hai chiesto se la patch di `GasKernel.__init__` viene sempre ripristinata: sì.
  - L'assegnazione sta dentro il `try` e il `finally` rimette l'originale anche se `__init__` solleva un'eccezione.
  - L'«altro» kernel è costruito con `_orig_init97l`, quindi non c'è ricorsione; in più c'è la guardia `fatto`.
  - Dopo la mia sonda `GasKernel.__init__.__name__` è tornato `__init__`.
  - Esito: **ok**.
- Hai chiesto anche dell'ordine del blocco della firma dopo una storia compressa che finisce con un tool. Il file finale finisce così: `user, assistant(tool_calls t1), tool t1, user(notifica firma), assistant(tool_calls firma_), tool, assistant(Preso atto)`.
  - Ogni tool ha la sua chiamata, quindi non ci sono tool orfani e il controllo di `doctor` resta verde.
  - Un messaggio user dopo un tool è accettato dai provider compatibili con OpenAI.
  - È la stessa forma che produce già il `finally` di `run_turn` quando si raggiunge il tetto di iterazioni (nel contesto: `gas.py:1188`, ramo «turno chiuso o storia compressa» di `_unisci_storia_altrui`).
  - Esito: **ok**.
- `gas.py:1303` (contesto) — `_storia_rimandata` torna False solo se la scrittura riesce, ed è questo che rende corretto il secondo controllo a `gas.py:5234`. Esito: **ok**.

**Riserva**
- **R-439-1 (chat Motore), BASSA, preesistente.** Senza rinvio, se la scrittura fallisce (`_salva_storia_su_file` restituisce False) `_storia_rimandata` resta False. Il comando stampa «✓ Compressi 42» con rc 0, ma il file resta di 63 messaggi: l'ho riprodotto con una sonda. È lo stesso tipo di falso «ok» di R-438-1, su un ramo diverso.
  - Correzione: far restituire a `_save_history` l'esito della scrittura e usarlo in `compress_history_cmd`.
  - Va tracciata in stato_progetto.md.

**Cosa non ho verificato**
- Non ho verificato su un'API reale (Gemini nativo) che la sequenza tool→user venga accettata: non era riproducibile qui senza chiavi e senza consumare token. Mi baso sul fatto che la stessa forma esiste già nel `finally` di `run_turn`.
- Non ho verificato la concorrenza reale tra due processi (il test la simula nello stesso processo).

**Memoria**
- Ho aggiunto la riga #439 in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (commit 5eb1c1d, `scripts/commit_memoria_revisore.sh`); nessuna lezione nuova.
- Lo staging è intatto: restano staged solo `gas.py` e `tests/test_unit_kernel.py`.

### Review #440 (chat Motore) — commit 28c7f94

## VERDETTO: APPROVATO CON RISERVE

Review #440 (chat Motore) del diff staged, cioè gas.py e tests/test_unit_kernel.py. Ho letto prima CLAUDE.md (sez. 5), stato_progetto.md (riga R-c4b3-4) e la mia memoria.

**Elementi esaminati**
- `gas.py:1292` — `_save_history` ora restituisce un bool. `return True` arriva solo dopo che `_salva_storia_su_file` è riuscito. Il `return False` sta dopo il try/finally, quindi copre i casi «unione rimandata», «scrittura fallita» ed «eccezione». Il lock si rilascia sempre nel finally. Ho controllato il rischio di rompere chi chiama la funzione: gli altri chiamanti (`gas.py:1412`, `gas.py:3233`, `gas.py:4540`, `gas.py:4544`, `gas.py:4581`) ignorano il valore di ritorno. Con grep non risulta nessun uso in modules/ né in tests/. Esito: ok.
- `gas.py:5235` — `compress_history_cmd` salva sempre con `fine_turno=True` e restituisce 1 con «✗ NON salvata» se il salvataggio fallisce. Ho guardato la doppia scrittura: la compressione salva già una volta da sola (`gas.py:1412`). Il secondo salvataggio riscrive lo stesso contenuto, oppure unisce un turno di un altro processo arrivato nel frattempo, cosa corretta. Costa solo una scrittura atomica in più. Esito: ok, con una riserva cosmetica (R-440-1, sotto).
- `tests/test_unit_kernel.py:7622` — T97j registra i messaggi che il provider finto riceve davvero. La patch di `ScriptedCompletions.create` è applicata prima del try e il ripristino sta nel finally, quindi viene rimesso a posto anche se `run_turn_scriptato` solleva. In quel caso l'eccezione risale poi al file di test, come negli altri test del file. `_Esplodi97j` solleva dentro `__iter__`, cioè dopo `create`: la seconda chiamata viene quindi registrata e la condizione `len >= 2` è sensata. Esito: ok.
- `tests/test_unit_kernel.py:7689` — T97l2 ripristina la storia, forza `_salva_storia_su_file` a restituire False (in try/finally) e verifica rc 1, «NON salvata» e l'assenza di «Compressi». È proprio il caso di R-439-1, cioè scrittura fallita senza unione rimandata. Esito: ok.

**Prove su una copia nello scratchpad** (/tmp/claude-0/-home-user-Gas/6049a349-3e7f-5be2-83ac-5dc6a4b4ff3d/scratchpad/c440)
- Suite del kernel: 995 PASS, 1 FAIL. Il FAIL è T79a, dovuto all'ambiente: la copia non è un repo git, quindi `git ls-files` non trova file. Era successo uguale nella #438.
- Mutazione «ripristino del vecchio codice di compress-history»: T97l2 FAIL.
- Mutazione «`return True` al posto del `return False` finale»: T97l2 FAIL.
- Mutazione «rinvio dell'unione tolto»: T97h, T97i e T97j FAIL.
- Stessa mutazione, ma togliendo dal test la clausola `_visto97j`: T97j fallisce comunque, sulla sola clausola dei messaggi inviati. Quindi la correzione V-1 del bot su PR #240 controlla davvero qualcosa.

**Riserve**
- **R-440-1 (chat Motore), COSMETICA**: se il primo salvataggio (quello dentro la compressione) riesce e il secondo fallisce, il comando dà rc 1 e «NON salvata» anche se il file è già compresso. È l'errore nella direzione prudente.
- **R-438-2 / V-2 bot #240, BASSA**: non corretta, resta un limite dichiarato. Se un altro processo ha scritto, i messaggi del turno stanno solo in memoria fino a fine turno e un kill -9 li perde. Va tenuta in stato_progetto.md.

**Rischio escluso**: non ho riprodotto un fallimento reale del filesystem (disco pieno, permessi) durante compress-history: l'ho simulato con la patch di `_salva_storia_su_file`. Non ho rilanciato pytest su tutti i 1816 test: mi baso sul vostro risultato, e nessun altro file usa il valore di ritorno.

**Memoria del revisore**: riga #440 aggiunta e committata con `scripts/commit_memoria_revisore.sh` (commit 1f90bc8, non pushato). Lo staging è intatto: 2 file, +31 −8. Nessuna lezione nuova.

File rilevanti: /home/user/Gas/gas.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/.claude/agents/memoria_revisore.md

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py: 992 → 996 PASS, 0 FAIL in locale (T97j, T97k, T97l, T97l2; in CI +2 per il sandbox bwrap: main 994 → 998 attesi). Blocco reale: `=== RIEPILOGO: 996 PASS, 0 FAIL ===`.
pytest `tests/`: 1816 passed.

## §6 STATO CI

- dec4ce9 (merge di #236 su main): CI di main non letta da qui.
- aa7f538 (con 012856e, 340326d): unit-suite (996 PASS in CI), handoff-check success; verifica-bot SUCCESS (APPROVATO CON RISERVE, 2 BASSE + 1 COSMETICA: decide l'operatore).
- 5eb1c1d, 361400f, 1f90bc8, 28c7f94: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-438-1, R-439-1: chiuse in #439/#440.
- R-440-1 (COSMETICA): compress-history può dire «NON salvata» se solo il secondo salvataggio fallisce (direzione prudente).
- R-438-2 (nota dichiarata): con un altro processo che ha scritto, i messaggi del turno in corso restano in memoria fino alla fine del turno; un kill -9 a metà turno li perde.
- Riserve precedenti: vedi `reports/stato_progetto.md`.
