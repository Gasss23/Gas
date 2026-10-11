# Verdetti della verifica esterna (agente sonnet, `.claude/verifica_esterna.md`)

> Archivio in sola aggiunta (V-1 bot #172): a ogni verifica esterna l'agente incolla qui il verdetto
> INTEGRALE, così le riserve «verifica esterna #N» citate nei report e chiuse nelle PR successive
> sono provabili da chi legge il repo. Il verdetto del bot di verifica su GitHub resta nella review
> della PR; questo file copre solo il passaggio dell'agente esterno lanciato dalla sessione.
> Unica modifica dell'agente al testo: nessuna (incollato com'è restituito).

---

## PR #171 — head `bbc1cd4` — 2026-10-10

```
VERIFICA ESTERNA PR #171 — APPROVATO CON RISERVE

**Metodo:** ho clonato il repo nella scratchpad e fatto checkout di `bbc1cd4` (head della PR). Ho confrontato con la base `0162e8f`, che è anche il merge-base. Ho letto il diff completo di `modules/` e `tests/`. Ho rilanciato `tests/test_unit_notte.py` alla base e al commit e l'intera suite al commit. Ho fatto due mutazioni sul codice. Ho fatto una sonda con due processi veri. Ho interrogato l'API GitHub in lettura. Il repo reale ha `git status` vuoto.

**CLAIM VERIFICATI**
- §2 `git diff --stat` e §3 `git log`: VERO. I file sono gli stessi 8 (codice: `modules/notte/notte.py`, `tests/test_unit_notte.py`; documenti e memoria: gli altri 6) e i 4 commit coincidono (`117e48c`, `3bd6c8c`, `c459006`, `bbc1cd4`). Le righe differiscono solo per `reports/handoff.md`, che l'handoff dichiara approssimato.
- Test notte 46 alla base e 48 al commit: VERO, rieseguiti.
- Suite completa 799 passed: VERO, rieseguita (103 s). Il 797 alla base non l'ho rieseguito.
- Mutazione 1, tolgo `logging.warning` nel ramo del lock occupato: VERO, fallisce `test_giro_occupato_lascia_traccia_nel_log`.
- Mutazione 2, tolgo `da_notificare = (… GIRO_OCCUPATO)`: VERO, fallisce `test_riepilogo_telegram_con_un_altro_giro_in_corso`. Il claim sulla mutazione nell'handoff regge.
- R-243-1 (nessuna traccia nel log) è CHIUSA: VERO. Con un processo esterno che teneva il lock, `esegui_notte` ha dato rc 2 e ha scritto il WARNING a livello root. Ha tentato l'invio Telegram e non ha avviato il kernel (la factory `1/0` non è stata chiamata). Il fallimento dell'invio, qui dovuto al proxy, è stato solo loggato.
- Il lock non viene rilasciato dal `close()` del descrittore del giro che non è partito: VERO. Il processo esterno ha tenuto il lock fino alla fine. La notifica parte nel `finally` dopo la chiusura, e il codice sta dentro `_notifica_telegram`, protetto da `try`.
- Il testo non contiene dati non fidati: VERO. Usa solo la costante, l'ora locale o `type(e).__name__`.
- Il codice di uscita 2 per il giro non avviato è invariato rispetto alla base: VERO.
- CI sul commit `c459006`: `handoff-check` failure e `unit-suite` success. Lo prevede l'handoff §6 (rosso per costruzione sui commit intermedi): VERO.
- CI sul commit `bbc1cd4` (head della PR): `handoff-check` success. `unit-suite` e `verifica` erano ancora `in_progress` al momento della lettura, quindi la CI finale non è provata.
- Etichetta `verifica` presente sulla PR, che risulta `blocked` in attesa dei check.
- Check required del ruleset `main-lock`: non letti. L'endpoint dei ruleset risponde ma non ho aperto il dettaglio delle regole.

**FINDING**
- V-1 (BASSA) — Doc non allineata. Il commento nel docstring di `esegui_notte` (`modules/notte/notte.py`, intorno a riga 358) e la voce 6 di `reports/stato_progetto.md` sono stati aggiornati. Ho cercato altre affermazioni sul lock con grep e non ho trovato contraddizioni residue. Il docstring dice ancora "2 un altro giro è in corso" senza accennare al nuovo messaggio: è accettabile ma incompleto. Fix: una riga nel docstring.
- V-2 (BASSA) — Il messaggio "NON avviato" parte a ogni avvio col lock occupato, anche per lanci manuali. Il revisore lo ha dichiarato innocuo (al più un messaggio a notte con il timer). Verificato: si spegne con `GAS_NOTTE_TELEGRAM=0`. Non è un difetto di correttezza.
- V-3 (COSMETICA) — Il valore di `interrotto` è una stringa libera: la costante `"giro_occupato"` condivide il canale con i nomi di eccezione. In pratica non collide (minuscolo con underscore contro CamelCase). Il revisore l'ha già notato. Fix possibile: parametro separato.
- V-4 (BASSA, processo) — L'handoff è nel formato richiesto e il revisore ha approvato, ma §6 non riporta la run CI finale: la riempirà la CI. Verificare prima del merge che `unit-suite` e `verifica-bot` diventino verdi.
- Nessun finding ALTA o MEDIA. Il cambiamento non indebolisce alcun gate né tocca la macchina di controllo (hook, workflow, `.claude/*` salvo la memoria del revisore, che è solo testo).

**NON VERIFICATO**
- Invio Telegram reale con token e ID veri, e il timer launchd che parte con un giro ancora in corso su Mac. Qui il proxy rifiuta l'invio. L'handoff lo dichiara già deferito.
- Esito finale di `unit-suite` e `verifica-bot` sull'head `bbc1cd4`: ancora in corso.
- Elenco dei check required nel ruleset `main-lock` via API: non letto in dettaglio.
- Suite completa alla base (797): non rieseguita.

**RACCOMANDAZIONE:** la PR è mergeabile quando `unit-suite` e `verifica-bot` risultano verdi sull'head. Poiché la PR tocca `modules/notte` e il canale verso il telefono, il merge autonomo richiede il verdetto testuale `APPROVATO` del bot senza finding. In caso contrario decide l'operatore. Prima del prossimo lavoro: provare l'invio reale sul Mac e aggiornare il docstring di `esegui_notte` (V-1).
```

Esito delle riserve: V-1 chiusa in PR #172; V-2 e V-3 lasciate così (innocue, già valutate in review #243); V-4 verificata prima del merge (CI verde).

---

## PR #172 — head `4298841` — 2026-10-10

```
VERIFICA ESTERNA PR #172 — APPROVATO

**Metodo**
- Ho lavorato su un clone usa-e-getta nella scratchpad, al commit pinnato 4298841, con base 698c050 (merge di #171). Il repo reale ha `git status` vuoto.
- Ho letto l'handoff dall'URL pinnato e confrontato il diff reale `698c050..4298841`.
- Ho rilanciato `tests/test_unit_notte.py` alla base, al commit e alla base con il solo file di test nuovo.
- Ho rilanciato `pytest tests` intero al commit.
- Ho interrogato via API GitHub la PR, i check-run e il ruleset di main.

**CLAIM VERIFICATI**
1. File toccati (§2): VERO. Gli 8 file coincidono con `git diff --stat` e con i `files` della PR. Il conteggio righe di `reports/handoff.md` (114 dichiarato, 120 reale) differisce, ma l'handoff lo ammette come approssimato.
2. Commit (§3): VERO. Sono 3 sulla PR: 69233e6, 44c5f94 e 4298841. Il terzo è il commit di fine-task, che l'handoff dichiara escluso dal suo log.
3. Notte 48 → 49 passed: VERO. La base dà 48 passed, il commit 49 passed.
4. `tests/` 800 passed: VERO. L'ho rilanciato in 99,99 s, 800 passed.
5. Il test nuovo prova la correzione: VERO. Sul vecchio codice, con il file di test nuovo, `test_lock_fallito_per_altro_motivo_non_dice_giro_in_corso` FALLISCE (1 failed, 48 passed). Con il nuovo codice passa.
6. Un lock davvero occupato resta exit 2: VERO. `test_riepilogo_telegram_con_un_altro_giro_in_corso` e `test_giro_occupato_lascia_traccia_nel_log` usano un lock reale e passano.
7. Un errore di `flock` diverso da `EAGAIN`/`EWOULDBLOCK` finisce nell'`except Exception` esterno. Lì viene loggato come warning, produce exit 1 e un messaggio «INTERROTTO», e il `finally` chiude il file di lock. VERO, letto nel codice e coperto dal test.
8. `skipif(notte.fcntl is None)` è su tutti e 4 i test che usano il lock: VERO. Il riferimento a `notte.fcntl.LOCK_EX` nel corpo della classe è protetto dallo skipif. Su Windows non l'ho eseguito.
9. Docstring e `reports/setup_notte.md` coerenti col codice (exit 1 per lock fallito per altro motivo): VERO.
10. Verdetto del revisore #245 (APPROVATO) coerente con quanto ho riprodotto: VERO.
11. Required checks sul ruleset di main: `unit-suite`, `handoff-check`, `verifica-bot`. VERO, via API.
12. CI sul commit di fine-task:
    - `unit-suite` è success e `handoff-check` è success.
    - Il check `verifica` era ancora `in_progress`, perché il bot non aveva ancora finito.
    - Su 44c5f94 `handoff-check` è failure, come predetto dall'handoff (§6).
13. Stato di PR #171 nello stato progetto («MERGIATA 698c050»): VERO per la base. Non ho verificato la richiesta esplicita dell'operatore.

**FINDING**
- V-1 (COSMETICA): l'handoff (§0.1 e §6) afferma che `gh` non è autenticato nel container. Nel mio ambiente `gh api` funziona. Non è un difetto del codice; l'affermazione può essere specifica della sessione precedente.
- V-2 (BASSA, di design, non regressione): su un disco con `flock` non supportato (`ENOLCK`) il giro ora esce con 1 ogni notte e manda «INTERROTTO … OSError», invece di fingere «un altro giro in corso». Prima usciva con 2 comunque senza lavorare, quindi non c'è regressione. Il giro però resta bloccato per sempre su quel filesystem, invece di partire senza lock. Non ho potuto provarlo su un disco reale. È coerente con la regola «robustezza» (CLAUDE.md §1) solo se il fermarsi è voluto; l'handoff lo dichiara come comportamento previsto.
- Casi avversari: non ho trovato by-pass né regressioni. Nessun gate è indebolito: il diff non tocca hook, CI né revisore. Il file `.claude/agents/memoria_revisore.md` riceve solo una riga di memoria aggiunta in coda.

**NON VERIFICATO**
- Il comportamento su un disco reale senza `flock` (NFS/CIFS con `ENOLCK`): non riproducibile nel container, coperto solo dal `fcntl` finto.
- L'esecuzione su Windows: il container è Linux.
- L'esito finale del check `verifica-bot`: era ancora in corso al momento della mia lettura.
- La richiesta esplicita dell'operatore per il merge di #171.
- L'invio Telegram reale con token e ID veri: lo dice l'handoff stesso (§7), da provare sul Mac.

**RACCOMANDAZIONE**
Il merge può procedere: sul codice non ho trovato difetti bloccanti. Prima di mergiare, attendi che `verifica-bot` chiuda con `success` e leggi il verdetto testuale del bot. Per la regola di merge autonomo serve `APPROVATO` senza finding V-x. Se il bot riporta riserve, la decisione resta all'operatore. Valutare (opzionale) se V-2 debba essere un comportamento «parte senza lock» invece di «si ferma».
```

Esito delle riserve: V-1 è vera per l'ambiente della verifica, ma nel container della sessione `gh` non è autenticato (si usa lo strumento GitHub collegato); V-2 lasciata così (sul Mac il disco è locale e il lock funziona; senza lock due giri potrebbero sovrapporsi), proposta all'operatore.
