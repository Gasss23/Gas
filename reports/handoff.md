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
- **Fetta 3.2** (lettura a voce dei compiti finiti): `DEFERITA`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +
 gas.py                             |  31 ++++++-
 modules/sottofondo/__init__.py     | 140 +++++++++++++++++++++++++------
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_kernel.py          |  70 ++++++++++++++++
 tests/test_unit_sottofondo.py      | 168 ++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main 5c79886 (merge della #345).

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_kernel.py` T106a (processo in sottofondo: avvisa_operatore non offerto e negato, risposta finale — round-trip §7), T106b (niente avviso alla firma), T106c (turno normale: `controlla` chiamata, avvisa_operatore offerto), T106d (`controlla` in errore: il turno prosegue). Suite kernel `=== RIEPILOGO: 1100 PASS, 0 FAIL ===` (prima 1096; il revisore, senza vector store, ha 1099 PASS + T31g ambientale). `tests/test_unit_sottofondo.py`: 59 passed (prima 34): pid riusato con processo vero, identità ignota, `ps` assente, «creato» parametrico × pid, inf/nan, «fermato», pulizia, `controlla`. Mutanti: «isfinite/futuro tolto» → 5 failed; gate + voce server + avvisa_operatore: 975 passed.

## §6 STATO CI

`gh` non autenticato nel cloud. I commit sono pushati insieme a questo report: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-701-3-M2 BASSA: con un compito in corso ogni turno lancia un `ps` (timeout 5 s nel caso peggiore, sul percorso della voce); due processi che controllano insieme un figlio morto possono mandare due avvisi.
- R-702-1-M2 BASSA: un salto all'indietro dell'orologio di oltre 2 minuti mentre un compito gira fa vedere il suo «creato» nel futuro → scaduto → il nostro figlio viene fermato.
- R-696-1-M2 BASSA (dalla #345): finestra contaminata + firma su Telegram.
- Ve #345 V-2 BASSA: posto vuoto recente → «ne sto già facendo uno» per ≤120 s. Bot #345 V-3 BASSA: prova con processi veri sulla storia condivisa.
- Non verificato in dev: processo vero con `claude -p`, avviso Telegram vero, `ps -ww` su macOS.
