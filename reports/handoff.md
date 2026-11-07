# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-07 — Sottofondo: seconda fetta di riserve BASSE (bot #346) (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: per decisione dell'operatore (via M1, 7 nov, operatore assente ~4 ore) le PR nuove si mergiano da sole solo con verdetto APPROVATO pulito; con riserve restano aperte e le decide l'operatore al rientro.
2. Prova sul Mac (dalla #345): a voce un compito lungo → «ci lavoro» e poi avviso su Telegram.

---

## §1 SCOPE & ESITO FETTE

- **PR #346** (prima fetta BASSE del sottofondo): `MERGIATA` (c523a04) col sì dell'operatore via M1, dopo due merge di main nel branch (#341 e #347 di Mani, conflitti solo in report e memoria; review #704-M2 e #705-M2 APPROVATO).
- **Seconda fetta BASSE del sottofondo**: `FATTA` — compito appena riuscito non riscritto «ko» e niente avviso «non è finito» (bot #346 V-1 su 3ee02dd e 0c836f9); riga nel prompt del processo in sottofondo «avvisa_operatore qui non esiste» (bot #346 V-1 su 2d0977e, V-4 su 0c836f9); pulizia dei compiti vecchi anche da `controlla()`, al massimo una volta l'ora (bot #346 V-3 su 2d0977e); test «data futura + processo estraneo» (R-703-1-M2). Review #706-M2 APPROVATO CON RISERVE (R-706-1/2-M2 BASSE).
- **Correzioni dopo bot #349 e review #706** (commit 1dc10bc): `FATTE` — avviso anche se la riscrittura del compito fallisce (bot #349 V-1 BASSA); niente «errore interno» dopo un compito già chiuso (R-706-2-M2). Review #707-M2 APPROVATO CON RISERVE (R-707-1-M2 BASSA, R-707-2-M2 COSMETICA). Verifica esterna #349 su 2f3fe95: APPROVATO CON RISERVE (solo BASSE).
- **Bot #349 su 147d6c8**: NON approvata solo per «riga del verdetto fuori formato» (problema del parser del bot); nel merito APPROVATO CON RISERVE con V-1 BASSA (se l'unlink del posto falliva, nessun avviso finale) `CORRETTA` in 0e5b2b0. Review #708-M2 APPROVATO CON RISERVE (R-708-1-M2 BASSA). Verifica esterna su 147d6c8: APPROVATO CON RISERVE (solo BASSE/cosmetiche).
- **Fetta 3.2** (lettura a voce dei compiti finiti alla prossima attivazione): `PRONTA, NON IN QUESTA PR` — per decisione di M1 va in una PR separata dopo la decisione dell'operatore sulla #349 (questa sessione pusha solo su feat/voce-v12-m2).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +
 gas.py                             |   4 +
 modules/sottofondo/__init__.py     |  46 +++++--
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_kernel.py          |   4 +-
 tests/test_unit_sottofondo.py      | 152 +++++++++++++++++++++++
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main c523a04 (merge della #346).

## §3 GIT LOG --ONELINE (sessione)

```
0e5b2b0 fix(sottofondo): posto non tolto non blocca l'avviso finale del compito (bot #349 su 147d6c8 V-1)
faacaf1 chore(revisore): memoria review #708 — APPROVATO CON RISERVE
147d6c8 docs(voce): report — correzioni bot #349 e R-706-2 (review #707-M2); fetta 3.2 rimandata a PR separata (chat M2)
1dc10bc fix(sottofondo): avviso anche se la scrittura del compito fallisce (bot #349 V-1); niente «errore interno» dopo un compito già chiuso (R-706-2-M2)
4b21b78 chore(revisore): memoria review #707 — APPROVATO CON RISERVE
2f3fe95 docs(voce): report di fine task — seconda fetta BASSE del sottofondo; PR #346 mergiata (chat M2)
135535e fix(sottofondo): compito riuscito non diventa «ko», prompt del figlio senza avvisa_operatore, pulizia anche da controlla(), test R-703-1 (bot #346 V-1/V-3) (sì dell'operatore via M1)
0898dd1 chore(revisore): memoria review #706 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #706-M2 sul commit 135535e (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #706-M2: diff in staging (`git diff --cached`) su feat/voce-v12-m2, HEAD 0c836f9, 4 file, +112/−7. Ho letto CLAUDE.md (già nel contesto), le voci del sottofondo in `reports/stato_progetto.md` e le lezioni recenti della mia memoria. Niente git stash: per i mutanti ho usato un worktree nello scratchpad, poi rimosso.

**Cosa ho guardato nel diff:**
- `modules/sottofondo/__init__.py:345`: ora `annulla` mette «ko» solo ai compiti ancora in_coda o in_corso e ritorna True se li ha chiusi. Il posto in coda si libera comunque se è dello stesso id. Rischio esaminato: un compito «ok» che resta con la coda bloccata. Non succede, lo sblocco del posto non dipende dallo stato. Esito: ok.
- `modules/sottofondo/__init__.py:190`: `_ripulisci` avvisa solo se `annulla` ha chiuso il compito. Rischio esaminato: avvisi persi quando il file del compito manca. Il comportamento è lo stesso di prima: niente file del compito, niente avviso. Esito: ok.
- `modules/sottofondo/__init__.py:269`: `controlla` lancia `_pulisci_vecchi` al massimo una volta l'ora per processo, solo se la cartella esiste, dentro il try/except già presente (§9 rispettato). La prima chiamata pulisce subito: costa un solo elenco della cartella. Esito: ok.
- `gas.py:4582`: la riga «SEI UN COMPITO IN SOTTOFONDO» viene aggiunta a `system_prompt`. Rischio esaminato: che il prompt venga ricostruito e la riga si perda. Non succede: `system_prompt` si assegna solo in `__init__` (gas.py:1120) e si usa a gas.py:5036. Non tocca `_get_window` né la finestra della storia. Esito: ok.
- `tests/test_unit_kernel.py:11934` e `tests/test_unit_kernel.py:11948`: T106a controlla che la riga ci sia nel processo in sottofondo, T106c che manchi nei turni normali. Esito: ok.
- `tests/test_unit_sottofondo.py:640`: la corsa è simulata col monkeypatch su `sf.annulla`. Funziona perché `_ripulisci` cerca `annulla` nel modulo a ogni chiamata. Esito: ok.

**Contesto (file non toccati):** gli altri chiamanti di `annulla` sono `modules/sottofondo/__init__.py:394`, `modules/sottofondo/__init__.py:413` e `gas.py:4619`. Ignorano il valore di ritorno, ed è corretto.

**Prove eseguite:**
- `tests/test_unit_sottofondo.py`: 67 passed.
- Mutante «annulla senza il controllo sullo stato»: 3 test falliti, preso.
- Mutante «pulizia a ogni chiamata, senza il limite di un'ora»: 1 test fallito, preso.
- Wall of Shame: nessun taglio diretto della storia, nessuna simulazione di tool. Cap 10 iterazioni e cap 8k non toccati.

**Riserve:**
- R-706-1-M2 BASSA: la corsa in `annulla` è ridotta ma non chiusa. Il file viene letto e poi riscritto senza lock: se il figlio scrive «ok» fra `_leggi` e `_scrivi_privato`, viene ancora sovrascritto con «ko». Basta dichiararlo; un lock su file sarebbe sproporzionato per una riserva BASSA.
- R-706-2-M2 BASSA: in `esegui` (`modules/sottofondo/__init__.py:394`), un'eccezione arrivata dopo che `_esegui` ha già scritto «ok» (per esempio un OSError diverso da FileNotFoundError durante l'unlink) ora lascia il compito «ok». Però all'operatore parte lo stesso «si è interrotto per un errore interno», in contraddizione con lo stato. Rimedio possibile: in quel ramo avvisare solo se `annulla` ha ritornato True.

**Non verificato:**
- La corsa vera fra due processi (figlio reale contro `controlla` del kernel): l'ho controllata solo con la simulazione via monkeypatch, perché una corsa fra processi in dev non si riproduce in modo deterministico.
- La suite completa del kernel (1100 PASS dichiarati): non l'ho rilanciata, ho letto solo T106a/c.
- Il comportamento sul Mac o sulla VPS.

**Memoria:** ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga contatore #706-M2 e una lezione (un «controlla lo stato prima di sovrascrivere» senza lock restringe la corsa ma non la chiude; verificare i chiamanti che ignorano il nuovo valore di ritorno). Commit 0774cd7 fatto con `commit_memoria_revisore.sh`; il diff in staging è rimasto com'era (4 file, +112/−7).

Review #707-M2 sul commit 1dc10bc (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md (sez. 5, 8, 9), `reports/stato_progetto.md` (voce sottofondo, riga 615) e la memoria del revisore (ultime voci #705-M2 e #706-M2). Il diff staged (`git diff --cached`) tocca 2 file, +62/−6. Non ho usato git stash: per i mutanti ho lavorato in un worktree separato, poi rimosso.

**Elementi del diff esaminati**
- `modules/sottofondo/__init__.py:355` — `chiuso = True` ora si imposta appena il compito risulta in_coda/in_corso, prima di `_scrivi_privato`.
  - Rischio esaminato: con il disco pieno, `_ripulisci` (`modules/sottofondo/__init__.py:182-192`) toglieva il posto senza avvisare. Ho controllato anche gli altri chiamanti di `annulla` (`gas.py:4619` e `modules/sottofondo/__init__.py:420`): ignorano il valore di ritorno, quindi la nuova semantica non li tocca. L'eccezione resta intercettata e finisce nel log (§9).
  - Esito: ok. Il mutante «chiuso dopo la scrittura» fa fallire `test_scrittura_fallita_avvisa_lo_stesso`.
- `modules/sottofondo/__init__.py:400-404` — in `esegui`, l'avviso «errore interno» parte solo se `chiuso` è vero, oppure se il file del compito manca o non è già ok/ko.
  - Rischio esaminato: due casi. Primo, nessun doppio avviso quando `_esegui` ha già scritto ok/ko. Secondo, un file illeggibile deve avvisare comunque. Se la scrittura fallisce, il file resta in_corso e l'avviso parte (una volta sola).
  - Esito: ok. Ho provato quattro mutanti e ognuno fa fallire un test:
    - «avviso sempre»: fallisce `test_eccezione_dopo_ok_niente_avviso_di_errore`
    - «senza chiuso»: fallisce `test_eccezione_dopo_ok_niente_avviso_di_errore`
    - «solo chiuso»: fallisce `test_eccezione_interna_avvisa`
    - «senza `or not dopo`»: fallisce `test_eccezione_interna_avvisa`
- `tests/test_unit_sottofondo.py:665` — il nuovo test copre sia «eccezione dopo ok → nessun avviso» sia «eccezione prima → un avviso e stato ko».
  - Rischio esaminato: che il test sia tautologico.
  - Esito: ok, perché i mutanti qui sopra lo fanno fallire.
- `tests/test_unit_sottofondo.py:694` — `test_scrittura_fallita_avvisa_lo_stesso` simula il disco pieno solo sul file del compito.
  - Esito: ok.
- Guardrail: questo diff non tocca la history né `_get_window`, non simula output di tool e non modifica il tetto delle iterazioni.

**Riserve**
- **R-707-1-M2 BASSA**: se la scrittura fallisce, `modules/sottofondo/__init__.py:355` fa partire l'avviso e il posto viene tolto, ma il file del compito resta «in_corso» per sempre. Nessuna ripulitura successiva lo rivede, perché il posto non c'è più. Lo stato su disco resta quindi incoerente; è accettabile perché l'operatore è stato avvisato.
- **R-707-2-M2 COSMETICA**: ci sono tre righe vuote prima del nuovo test (`tests/test_unit_sottofondo.py:662-664`, PEP8 E303).
- Resta aperta **R-706-1-M2** (corsa in `annulla` senza lock): questo diff non la tocca.

**Test**: sottofondo 69 passed con l'index.

**Cosa non ho verificato**: il comportamento reale con il disco pieno sul Mac o sulla VPS (non riproducibile in dev, l'ho solo simulato con un monkeypatch) e la consegna effettiva dell'avviso Telegram (nei test `avvisa` è finto). Non ho rilanciato la suite completa, solo `tests/test_unit_sottofondo.py`.

**Memoria**: ho aggiunto la riga #707-M2 e l'ho committata con `scripts/commit_memoria_revisore.sh` (commit 4b21b78). Nessuna lezione nuova.

File: /home/user/Gas/modules/sottofondo/__init__.py, /home/user/Gas/tests/test_unit_sottofondo.py, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #708-M2 sul commit 0e5b2b0 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #708-M2: la modifica di 2 file in staging (+23 righe) sul branch feat/voce-v12-m2 (HEAD 147d6c8, PR #349) chiude il finding V-1 del bot #349 ed è passata. Resta una riserva BASSA (R-708-1-M2): la correzione è giusta, ma il posto in coda si libera da solo solo se l'errore è temporaneo.

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 9), reports/stato_progetto.md (voce Fetta 3 sottofondo, riga 615) e la memoria del revisore. Nessun taglio della cronologia e nessuna simulazione di tool: il diff non tocca né la cronologia né i tool.

**Elementi del diff esaminati**
- `modules/sottofondo/__init__.py:461` — `except OSError` dopo `except FileNotFoundError` sulla rimozione di attivo.json, con warning nel log. Rischi esaminati:
  - Ordine delle eccezioni: FileNotFoundError è una sottoclasse di OSError, quindi va prima, ed è così.
  - Esito già scritto: lo stato ok/ko è scritto prima (`modules/sottofondo/__init__.py:455`), quindi dopo l'errore l'avviso finale parte col testo giusto.
  - Rispetto del §9: errore intercettato e loggato, il processo prosegue.
  - Esito: ok.
- `tests/test_unit_sottofondo.py:714` — test `test_posto_non_tolto_avviso_finale_parte_lo_stesso`: forza un PermissionError sulla rimozione del solo attivo.json e controlla tre cose: esegui restituisce 0, parte un solo avviso «Ho finito», sul disco lo stato è «ok». Rischio esaminato: il test potrebbe passare anche col codice vecchio. Verificato: ho messo il test in staging in un worktree con il modulo di HEAD e fallisce (1 failed); con la correzione passa. Suite sottofondo 70 passed. Esito: ok.
- Contesto, `modules/sottofondo/__init__.py:186` — `_ripulisci` toglie il posto con un `except FileNotFoundError` soltanto. Rischio esaminato: il commento del fix dice «il posto si libera da solo», e questo regge solo se l'errore era temporaneo. Esito: riserva (R-708-1-M2).
- Contesto, `gas.py:4609` — il tool in_sottofondo chiama `accoda` dentro un `try/except Exception` che logga e risponde «non accodato». Rischio esaminato: crash se `_ripulisci` solleva da dentro `accoda`. Esito: ok, l'errore resta contenuto (§9 rispettato).

**Riserve**
- R-708-1-M2 BASSA: se l'errore sulla rimozione è persistente (permessi della cartella), anche `_ripulisci` (`modules/sottofondo/__init__.py:186`) solleva a ogni passaggio.
  - Le eccezioni non escono: le contengono `controlla` (riga 270) e il try in `gas.py:4609`.
  - Però il posto resta occupato per sempre e ogni nuovo compito viene rifiutato con «compito in sottofondo non accodato», senza un avviso esplicito all'operatore. Nella riga di memoria ho scritto «occupato»: il testo esatto è «non accodato».
  - Rimedio possibile: in `_ripulisci` intercettare OSError e avvisare una volta.
  - Il percorso esisteva già prima di questo diff, che lo rende solo più probabile.
- Restano aperte, invariate: R-706-1-M2 (corsa in annulla senza lock) e R-707-1-M2 (file fermo su «in_corso» se la scrittura fallisce).

**Rischio escluso**: non ho verificato un errore di permessi vero sul filesystem (macOS/VPS), perché il test simula PermissionError con un monkeypatch su `Path.unlink`. Non ho controllato nemmeno la corsa tra due processi sullo stesso attivo.json (già coperta da R-706-1-M2).

**Memoria**: ho aggiunto la riga #708-M2 e una lezione nuova («quando una correzione rimanda la pulizia a un passaggio successivo, verificare che quel passaggio gestisca lo stesso errore»). L'ho committata da sola con `scripts/commit_memoria_revisore.sh` (commit faacaf1). Il diff in staging non è stato toccato.

File:
- /home/user/Gas/modules/sottofondo/__init__.py
- /home/user/Gas/tests/test_unit_sottofondo.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_kernel.py` T106a ora controlla anche la riga «SEI UN COMPITO IN SOTTOFONDO» nel prompt del processo in sottofondo (round-trip §7: chiamata negata, risposta finale), T106c che manchi nei turni normali. Suite kernel `=== RIEPILOGO: 1100 PASS, 0 FAIL ===`. `tests/test_unit_sottofondo.py`: 70 passed (prima 62; +1 in 0e5b2b0: posto non tolto, avviso finale parte; +2 in 1dc10bc: scrittura fallita avvisa lo stesso, eccezione dopo «ok» senza avviso di errore): compito appena riuscito resta «ok» senza avviso, `annulla` chiude solo compiti aperti, corsa simulata (figlio che finisce durante la pulizia), pulizia da `controlla` una volta l'ora, data futura + processo estraneo. Con il modulo di prima i test nuovi danno 3 failed; mutante «avviso sul compito letto prima» → 1 failed.

## §6 STATO CI

`gh` non autenticato nel cloud. Su 147d6c8: handoff-check verde; verifica-bot failure per verdetto fuori formato (nel merito solo BASSE); unit-suite in corso. I commit nuovi sono pushati insieme a questo report: run non ancora disponibile alla scrittura.

## §7 RISERVE APERTE

- R-706-1-M2 BASSA: la corsa in `annulla` è ristretta ma non chiusa (lettura e riscrittura senza lock).
- R-706-2-M2: CHIUSA in 1dc10bc.
- R-708-1-M2 BASSA: se l'errore sull'unlink del posto è persistente (permessi), anche `_ripulisci` fallisce a ogni passaggio: posto occupato per sempre e nuovi compiti «non accodato», senza avviso esplicito.
- R-707-1-M2 BASSA: se la riscrittura del compito fallisce, l'avviso parte ma il file resta «in_corso» per sempre. R-707-2-M2 COSMETICA: righe vuote in più nel test.
- Bot #349 V-2 COSMETICA: `_ultima_pulizia` è per processo, non per cartella, e risente dei salti dell'orologio.
- R-701-3-M2 BASSA / bot #346 V-3 (0c836f9): con un compito in corso ogni turno lancia `ps`; due processi che controllano insieme un figlio morto possono mandare due avvisi.
- R-703-2-M2 / bot #346 V-2 (0c836f9) BASSA: con «creato» nel futuro e identità ignota la durata massima non vale finché l'orologio non raggiunge quella data.
- R-696-1-M2, ve #345 V-2, bot #345 V-3: BASSE, invariate.
- Non verificato in dev: processo vero con `claude -p`, avviso Telegram vero, `ps -ww` su macOS.
