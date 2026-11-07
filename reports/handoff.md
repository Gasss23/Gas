# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-07 — Sottofondo: chiusura delle riserve BASSE di bot e verifica esterna #345 (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta (con riserve BASSE: sì dell'operatore via M1, CLAUDE.md §10). Sì alla fetta dato dall'operatore via M1 il 7 nov.
2. Prova sul Mac (resta da fare dalla #345): a voce un compito lungo → «ci lavoro» e poi avviso su Telegram.

---

## §1 SCOPE & ESITO FETTE

- **PR #345** (fetta 3, compiti lunghi in sottofondo): `MERGIATA` (5c79886) col sì dell'operatore via M1.
- **Fetta BASSE del sottofondo**: `FATTA` — pid riusato non blocca la coda (ve #345 V-1); «creato» non numerico/non finito/nel futuro non blocca (bot V-4, ve V-2, R-701-2); `sottofondo.controlla` a ogni turno: avviso al crash alla prima interazione (bot V-1 e323b60); processo in sottofondo senza `avvisa_operatore` (bot V-2 e323b60); «fermato» solo se fermato davvero (R-699-1, ve V-3); pulizia dei compiti finiti oltre 7 giorni (bot V-2 46596b4); inf/nan nelle variabili → default (bot V-3 46596b4). Review #701-M2 e #702-M2 APPROVATO CON RISERVE.
- **Verifica esterna #346 su 2d0977e** (APPROVATO CON RISERVE): V-1 BASSA (regressione: orologio portato indietro → compito vero fermato e secondo compito in parallelo) e V-2 COSMETICA (1e308 → inf) `CORRETTE` in fb620f5. Review #703-M2 APPROVATO CON RISERVE (R-703-1/2-M2 BASSE).
- **Bot #346 su 8134ff3**: NON approvata per V-1 MEDIA «PR in conflitto con main» (dopo il merge della #341 di Mani): `RISOLTA` con il merge 643da99 — conflitti solo in report (tenuti quelli di M2) e memoria del revisore (righe di entrambi); codice del motore di M2 identico. Review #704-M2 APPROVATO.
- **Fetta 3.2** (lettura a voce dei compiti finiti): `DEFERITA`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +
 gas.py                             |  31 ++-
 modules/sottofondo/__init__.py     | 164 ++++++++++--
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_kernel.py          |  70 +++++
 tests/test_unit_sottofondo.py      | 207 +++++++++++++-
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main c1a4503 (merge della #341 di Mani, unito nel branch con 643da99).

## §3 GIT LOG --ONELINE (sessione)

```
643da99 Merge origin/main (PR #341, fetta 43 parte 2 di Mani) nella PR #346 — conflitti solo in report e memoria del revisore (bot #346 V-1 MEDIA); review #704-M2 APPROVATO
8134ff3 docs(voce): report — verifica esterna #346 V-1/V-2 corrette (chat M2)
fb620f5 fix(sottofondo): orologio portato indietro non ferma il compito vero né ne fa partire un secondo (ve #346 V-1, R-702-1-M2); 1e308 nelle variabili → default (ve #346 V-2)
9173c62 chore(revisore): memoria review #703 — APPROVATO CON RISERVE
2d0977e docs(voce): report di fine task — riserve BASSE del sottofondo chiuse (chat M2)
256c1e0 fix(sottofondo): chiude le riserve BASSE di bot e verifica esterna #345 (pid riusato, «creato», avviso al crash, ultimo avviso del giorno, «fermato», pulizia, inf/nan) (sì dell'operatore via M1)
f0f21ce chore(revisore): memoria review #702 — APPROVATO CON RISERVE
e2d04d0 chore(revisore): memoria review #701 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #701-M2 sul primo stage di 256c1e0 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #701-M2. Ho revisionato il diff staged (`git diff --cached`) su feat/voce-v12-m2, base 5c79886: 4 file, +371/−30. Non ho usato `git stash`: i mutanti li ho lanciati in un `git worktree` nello scratchpad, poi rimosso.

Prima della review ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md (voce sottofondo, riga 615) e la mia memoria (lezioni #695–#700).

**Parti del diff esaminate**
- `modules/sottofondo/__init__.py:116` — `attivo()` libera il posto solo se `_identita(...)` dà False. Se dà None (manca `ps`) il posto resta occupato.
  - Rischio esaminato: un nostro figlio vivo visto come estraneo per errore, con il compito che diventa ko mentre gira ancora.
  - Cosa ho controllato: il figlio è leader del proprio gruppo (`start_new_session`) e la riga di comando non viene troncata (`-ww`). Lo zombie: sonda con un Popen vero → identità False, mentre `_vivo` dà True; ora la coda si libera (migliora R-695-2). Se il primo figlio finisce in ritardo, vede «ko» ed esce senza secondo esito.
  - Esito: ok.
- `modules/sottofondo/__init__.py:150` — la parola «fermato» compare solo dopo un `killpg` riuscito. Con identità ignota il messaggio dice «forse ancora in esecuzione» e scrive un warning nel log; se `killpg` fallisce resta «oltre la durata massima» più il warning.
  - Esito: ok, R-699-1-M2 chiusa.
  - Mutante (motivo «fermato» sempre) → ucciso.
- `modules/sottofondo/__init__.py:205` — `_pulisci_vecchi` cancella solo i `.json` con stato ok/ko e i temporanei `.posto.*`/`.tmp.*`. Salta `attivo.json`, i compiti in corso e i file non leggibili.
  - Esito: ok.
  - Mutante (cancella qualsiasi json leggibile) → ucciso.
- `modules/sottofondo/__init__.py:88` — `_creato` con `math.isfinite`.
  - Esito: **riserva**. Mutante (`isfinite` tolto) → **sopravvive** (vedi R-701-1-M2).
- `gas.py:4877` — `sottofondo.controlla(self.root)` a inizio turno, saltata quando `nel_sottofondo` è vero, dentro try con warning (§9). `controlla` non lancia mai eccezioni (`modules/sottofondo/__init__.py:230`).
  - Esito: ok. T106c/T106d coprono la chiamata e l'errore.
- `gas.py:4926` — l'offerta del figlio è senza `avvisa_operatore`; il dispatch e il cancello lo negano (`_AVVISO_NEL_SOTTOFONDO`), quindi non si può nemmeno chiedere la firma per un avviso. Il costruttore è `per_sottofondo` (`gas.py:4577`) ed è usato da `main()`. L'override sta prima del ramo `effimero`, quindi non cambia i turni effimeri.
  - Esito: ok. T106a è un round-trip vero (§7): chiamata, diniego, risposta finale.
- Wall of Shame: nessuno slicing della history e nessun output dei tool simulato. Cap di 10 iterazioni e `_get_window` non toccati.

**Test rilanciati da me**
- tests/test_unit_sottofondo.py: 52 passed.
- Kernel: `=== RIEPILOGO: 1099 PASS, 1 FAIL ===`. Il FAIL è T31g (`GAS_VECTORS=1`, vector store) e fallisce identico anche a HEAD senza il diff (1095 PASS, 1 FAIL). Dipende dal mio ambiente, che non ha il vector store; non è una regressione. Il conto torna con 1095 + T106a-d = 1099. Il tuo 1100/0 viene da un ambiente col vector store.

**Riserve (tutte BASSE)**
- **R-701-1-M2**: `tests/test_unit_sottofondo.py:430` usa `pid=os.getpid()`. Il processo di pytest non è leader del gruppo, quindi l'identità dà False e libera il posto comunque: il test non controlla davvero il ramo `isfinite`. Con `pid: None` e «creato» = «inf» il mutante bloccherebbe la coda per sempre senza che nessun test se ne accorga. Correzione: aggiungere il caso `pid: None` al parametrico.
- **R-701-2-M2**: un «creato» finito ma nel futuro con `pid: None` blocca la coda finché il futuro non arriva. Sonda: con 1e18 `accoda` dice «c'è già un compito»; succede anche con l'orologio portato indietro sulla VPS. È la stessa classe di V-4 ed esisteva già prima. Correzione: trattare come scaduto un «creato» più avanti di adesso + 120 s.
- **R-701-3-M2**: con un compito in corso, ogni turno (voce e Telegram) lancia un `ps`. Di solito sono pochi millisecondi, ma nel caso peggiore il timeout è di 5 s, sul percorso della voce. Inoltre due processi che chiamano `controlla` nello stesso istante su un figlio morto possono mandare due avvisi, perché leggono entrambi il job «in_corso» prima di `annulla`; la finestra è minima.

**Rischio escluso (non verificato)**: il comportamento su macOS (Python framework, `ps` BSD) e sulla VPS non l'ho riprodotto, perché qui ho solo Linux/procps. Non ho verificato con processi reali la corsa fra voce e Telegram (R-701-3-M2): l'ho solo ragionata.

**Memoria**: riga #701-M2 e una lezione (test parametrici in cui un altro ramo rende vero l'esito da solo) scritte e committate in `/home/user/Gas/.claude/agents/memoria_revisore.md` (commit e2d04d0, solo quel file). Il diff staged è intatto.

Review #702-M2 sullo stage finale di 256c1e0 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #702-M2 (bis di #701-M2, branch feat/voce-v12-m2, base 5c79886). Ho esaminato solo il delta, con il diff staged intatto (senza `git stash`; i mutanti li ho provati in un worktree separato nello scratchpad, poi rimosso). Letture obbligatorie fatte: CLAUDE.md, le riserve R-701 in stato_progetto e la memoria del revisore.

**Elementi del diff esaminati**
- modules/sottofondo/__init__.py:97 — `_creato()` ora tratta come 0 (posto scaduto) un «creato» più avanti di adesso + 120 s. Rischio esaminato: un «creato» nel futuro che tiene occupata la coda per sempre (R-701-2-M2). Esito: ok, chiusa. `isfinite` è ormai ridondante: inf e nan non passano già il confronto `<=`, e -inf dà un'età infinita, quindi scaduto. Il mutante senza `isfinite` sopravvive ma il comportamento è equivalente: non è un buco del test.
- tests/test_unit_sottofondo.py:429 — test parametrico su pid (None / pid proprio) × creato (abc, nan, inf, [1], {"a":1}, 1e18). Rischio esaminato: che un altro ramo decida l'esito da solo (R-701-1-M2), e segnali inviati a pytest. Esito: ok, chiusa.
  - `_identita` è forzato a True, quindi l'esito dipende solo da «creato».
  - `os.killpg` è neutralizzato alla riga 436, quindi nessun segnale arriva a pytest. `_vivo` usa solo `os.kill(pid, 0)`, che non manda segnali.
  - Mutante «controllo del futuro tolto» → 2 failed (1e18 con pid None e con pid proprio). Suite sottofondo: 59 passed.
- Contesto: modules/sottofondo/__init__.py:107 — `attivo()` usa `_creato`: con creato scaduto rende None e il turno passa alla pulizia. Esito: ok.

**Riserve**
- R-701-3-M2 BASSA, resta aperta: con un compito in corso ogni turno lancia un `ps`, e due processi che controllano insieme possono mandare due avvisi.
- R-702-1-M2 BASSA, nuova: se l'orologio viene portato indietro di oltre 2 minuti mentre un compito vero gira, il suo «creato» finisce nel futuro e vale scaduto. La pulizia allora vede «oltre la durata», `_identita` dice True e `killpg` ferma il NOSTRO figlio legittimo, con l'avviso «oltre la durata massima, fermato». Prima della modifica il posto restava solo occupato. È raro (salto dell'orologio NTP, cioè l'ora corretta di colpo), quindi accettabile. Fix possibile: nel ramo del futuro non chiamare `killpg`, oppure usare un orologio monotono (che non torna mai indietro) o il controllo d'identità come unico criterio.

**Non verificato**
- La suite del kernel non l'ho rilanciata: il delta tocca solo modules/sottofondo e il suo test, e in #701 dava 1099 PASS e 1 FAIL ambientale (T31g, manca il vector store).
- Il comportamento reale con un salto dell'orologio NTP (R-702-1-M2) l'ho ricavato leggendo il codice, non riprodotto.

**Memoria**: aggiunte la riga #702-M2 e una lezione (timestamp nel futuro che decide un kill, salto all'indietro dell'orologio) in /home/user/Gas/.claude/agents/memoria_revisore.md, committate con commit atomico f0f21ce. Il diff staged è intatto (4 file, +379/−30).

Review #703-M2 sul commit fb620f5 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #703-M2: correzione di ve #346 V-1 e V-2. È stato esaminato solo il diff staged (feat/voce-v12-m2, base 2d0977e, 2 file, +69/−8). Non ho usato `git stash`. Ho provato i mutanti in un `git worktree` nello scratchpad, poi l'ho rimosso.

**Elementi del diff esaminati**
- `modules/sottofondo/__init__.py:120`: in `attivo()`, se «creato» è nel futuro la data viene ignorata. Senza pid o con pid morto il posto è libero. Con pid vivo il posto si libera solo se `_identita` è False, altrimenti (True o None) resta occupato. Rischio esaminato: un salto indietro dell'orologio (NTP) con un compito vero in corso, e un file alterato senza processo (R-701-2-M2). **Esito: ok.** R-702-1-M2 è chiusa: il nostro figlio non viene più fermato e non parte un secondo compito. R-701-2-M2 resta chiusa per il caso senza processo. L'ordine dei controlli è identico al ramo normale, quindi niente regressioni sul pid riusato (R-698-1).
- `modules/sottofondo/__init__.py:160`: `oltre = not _nel_futuro(dati) and ...`. Rischio esaminato: killpg con una data futura. **Esito: ok.** Il ramo è solo difensivo. Con identità True o None `attivo()` ritorna prima, e con identità False il kill non avviene comunque. Il mutante che toglie la guardia sopravvive. È accettabile così, ma va dichiarato.
- `modules/sottofondo/__init__.py:87` e `modules/sottofondo/__init__.py:226`: il controllo `isfinite` ora si fa dopo la moltiplicazione (×60 e ×86400). Rischio esaminato: con 1e308 il valore diventava inf, cioè durata infinita oppure nessuna pulizia. **Esito: ok.** V-2 è chiusa e 1e308 è aggiunto ai test parametrici.
- `tests/test_unit_sottofondo.py:546`: crea un figlio finto vero, `python -c sleep ... gas.py sottofondo <id>`, leader di sessione, con creato = adesso+600. Controlla che il posto resti occupato, che il processo non venga ucciso, che non parta nessun avviso e che il secondo compito sia negato. Rischio esaminato: che il test passi per un ramo diverso da quello voluto. **Esito: ok.** Senza `ps` l'identità sarebbe None, il posto resterebbe occupato e il test passerebbe lo stesso: è coerente col codice.
- `tests/test_unit_sottofondo.py:441`: il caso 1e18 con pid proprio ora si aspetta il posto occupato. **Esito: ok.** Il pid di pytest non è leader del gruppo, ma `_identita` è forzata a True dal monkeypatch del parametrico (R-701-1).
- `tests/test_unit_sottofondo.py:570`: data futura con pid None o morto, la coda si libera. **Esito: ok.**

**Controlli rilanciati**
- 62 passed, anche con COLUMNS=20.
- Codice di HEAD con i test nuovi: 4 failed (il caso del figlio vero, il caso 1e18 con pid proprio, i due 1e308). Tu ne avevi dichiarati 2: la differenza è solo nel conteggio.
- Mutante «identità ignorata nel solo ramo futuro» (`return dati` se il pid è vivo): **sopravvive**, 62 passed.

**Riserve**
- **R-703-1-M2 BASSA**: nessun test copre «creato» nel futuro con un pid vivo ma estraneo (leader con un comando diverso, identità False, quindi posto libero). Il mutante qui sopra lo dimostra. Va aggiunto un test con `sleep` in `start_new_session=True` e creato = adesso+600: il test deve verificare che il posto sia libero e che il processo estraneo non venga toccato.
- **R-703-2-M2 BASSA (trade-off da dichiarare)**: con «creato» nel futuro la durata massima non vale finché l'orologio non raggiunge quella data. Con un salto naturale di X minuti il caso peggiore è durata + X. Ma con il file alterato a 1e18 e il nostro figlio appeso, la coda resta occupata per tutta la vita del figlio: il figlio non ha un tetto di tempo proprio (in gas.py non ho trovato timeout o alarm per il sottofondo). A HEAD invece quel figlio veniva fermato. Basta dichiararlo in stato_progetto.md, oppure, se si vuole chiuderlo, usare un tetto basato sull'mtime di attivo.json.
- R-701-3-M2 resta aperta (fuori da questo diff).

**Rischio escluso**: non ho verificato il comportamento con un vero salto NTP su macOS o sulla VPS, perché in dev non si riproduce: la data futura è stata simulata scrivendo «creato». Non ho rilanciato la suite del kernel, perché il diff non tocca gas.py.

**Memoria**: aggiunte la riga #703-M2 e una lezione (lanciare il mutante del solo ramo nuovo quando un controllo viene duplicato) in /home/user/Gas/.claude/agents/memoria_revisore.md. Ho lanciato `scripts/commit_memoria_revisore.sh`. Il diff staged è rimasto intatto (2 file, +69/−8).

File rilevanti: /home/user/Gas/modules/sottofondo/__init__.py, /home/user/Gas/tests/test_unit_sottofondo.py, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #704-M2 sul merge 643da99 (verdetto integrale):

## VERDETTO: APPROVATO

Review #704-M2: merge di origin/main c1a4503 (PR #341, chat Mani) in feat/voce-v12-m2 (PR #346, HEAD 8134ff3). Il merge è ancora in corso e io ho solo fatto `git add` della memoria.

Letture fatte prima della review: CLAUDE.md (sez. 5), il §stato di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

**Controlli meccanici sulla risoluzione**
- `git ls-files -u` è vuoto, quindi non resta nessun conflitto aperto.
- `git diff --cached --check HEAD` è pulito.
- Nessun marcatore `<<<<<<<`/`=======`/`>>>>>>>` nei file toccati (memoria, reports/*.md, ascolto.py, test, LEGGIMI).
- Index contro il tree di main c1a4503: la differenza riguarda SOLO i 10 file che M2 ha toccato dopo il merge-base 5c79886: gas.py, modules/sottofondo/__init__.py, tests/test_unit_kernel.py, tests/test_unit_sottofondo.py, i 3 report di sessione, reports/ripartenza_m2.md, stato_progetto e memoria. Index contro HEAD: la differenza riguarda SOLO i 5 file che arrivano da main. Quindi il motore di M2 è identico a HEAD e il merge non introduce codice nuovo.

**Elementi del diff esaminati**
1. `clients/voice/ascolto.py:654` — `_azzera()` del rilevatore tra le fasi (codice della fetta 43 parte 2, PR #341). Rischio: che la risoluzione abbia mischiato la versione del branch (blob 91e3d55) con quella di main. Esito ok: il blob nell'index è fd8b3e3, uguale a MERGE_HEAD.
2. `tests/test_unit_voce_ascolto.py:244` — il finto rilevatore con punteggio QUASI=0.6 usato dai test della finestra. Rischio: test persi o duplicati nel merge. Esito ok: il blob nell'index è 14f4b5e, uguale a MERGE_HEAD.
3. `reports/stato_progetto.md:4` — riga «Ultimo aggiornamento». Rischio: che si perda una delle due catene di date. Esito ok: c'è la riga di main (chat Mani, review #701). Rispetto a main l'unico delta è la riga di M2 su «Fetta 3 sottofondo» (`reports/stato_progetto.md:615`), che arriva da HEAD. Nota marginale: la storia «prima: 2026-11-05 (chat M2 … PR #339)» resta più giù nella catena di main e non è persa.
4. `.claude/agents/memoria_revisore.md:1311` — righe #701-M2..#703-M2. Rischio: righe perse nell'unione. Esito ok: rispetto a HEAD si aggiungono solo le righe Mani #676..#701, rispetto a main solo le #701..#703-M2 con le loro lezioni. La riga #701 Mani sta alla 1317. Unione senza perdite.

**Test**
- `pytest tests/test_unit_sottofondo.py tests/test_unit_voce_ascolto.py`: 319 passed.
- `python tests/test_unit_kernel.py`: 1099 PASS e 1 FAIL (T31g, GAS_VECTORS). Lo stesso FAIL esce anche a HEAD 8134ff3, provato in un worktree separato senza toccare l'index. Dipende dall'ambiente, non dal merge.

**Rischio escluso**: non ho riletto da capo la parte semantica di ascolto.py e dei suoi test, perché sono già stati revisionati e mergiati con la PR #341 (review #676–#701 della chat Mani). Ho verificato solo che i blob siano identici a MERGE_HEAD. Non ho verificato la CI remota né il comportamento sul Mac: in questo ambiente non sono riproducibili.

**Riserve**: nessuna.

**Memoria**: aggiunta la riga `#704-M2 — 2026-11-07 — APPROVATO — …` in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` (nessuna lezione nuova) e fatto `git add` del file. NON ho lanciato commit_memoria_revisore.sh, come richiesto: la riga entra nel commit di merge. Index degli altri file non toccato, nessuno stash.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_kernel.py` T106a (processo in sottofondo: avvisa_operatore non offerto e negato, risposta finale — round-trip §7), T106b (niente avviso alla firma), T106c (turno normale: `controlla` chiamata, avvisa_operatore offerto), T106d (`controlla` in errore: il turno prosegue). Suite kernel `=== RIEPILOGO: 1100 PASS, 0 FAIL ===` (prima 1096; il revisore, senza vector store, ha 1099 PASS + T31g ambientale). `tests/test_unit_sottofondo.py`: 62 passed (prima 34; anche con COLUMNS=20): orologio portato indietro con figlio vero (posto occupato, nessun kill), data futura senza processo (libero), 1e308; pid riusato con processo vero, identità ignota, `ps` assente, «creato» parametrico × pid, inf/nan, «fermato», pulizia, `controlla`. Mutanti: «isfinite/futuro tolto» → 5 failed; gate + voce server + avvisa_operatore: 975 passed.

## §6 STATO CI

`gh` non autenticato nel cloud. Su 8134ff3: unit-suite e handoff-check verdi; verifica-bot failure solo per il conflitto con main (V-1 MEDIA), ora risolto col merge 643da99. Bot su 2d0977e: APPROVATO CON RISERVE (BASSE: prompt del figlio cita avvisa_operatore; latenza una tantum di ~20 s al primo turno dopo un crash; pulizia solo all'accodamento; `_e_nostro` usata solo nei test). I commit nuovi sono pushati insieme a questo report: run non ancora disponibile alla scrittura.

## §7 RISERVE APERTE

- R-701-3-M2 BASSA: con un compito in corso ogni turno lancia un `ps` (timeout 5 s nel caso peggiore, sul percorso della voce); due processi che controllano insieme un figlio morto possono mandare due avvisi.
- R-702-1-M2: CHIUSA in fb620f5 (ve #346 V-1).
- R-703-1-M2 BASSA: nessun test per «creato» nel futuro con pid vivo ma estraneo (posto libero); il mutante «identità ignorata nel ramo futuro» sopravvive. Anche la guardia `not _nel_futuro` in `_ripulisci` è solo difensiva (mutante sopravvive).
- R-703-2-M2 BASSA: con «creato» nel futuro la durata massima non vale finché l'orologio non raggiunge quella data; con file alterato e figlio appeso la coda resta occupata per la vita del figlio (il figlio non ha un tetto di tempo proprio).
- R-696-1-M2 BASSA (dalla #345): finestra contaminata + firma su Telegram.
- Ve #345 V-2 BASSA: posto vuoto recente → «ne sto già facendo uno» per ≤120 s. Bot #345 V-3 BASSA: prova con processi veri sulla storia condivisa.
- Non verificato in dev: processo vero con `claude -p`, avviso Telegram vero, `ps -ww` su macOS.
