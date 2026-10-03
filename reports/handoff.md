# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-03 — C4b-2: bottoni di firma Telegram + esecuzione post-approvazione, branch `feat/cancello-c4b2`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #116 (https://github.com/Gasss23/Gas/pull/116) — variante A: l'agente lancia `gasmerge 116`, l'operatore conferma digitando `116`.
2. Prova reale di un click su Telegram (bot vivo con `gas telegram`, azione innocua): da decidere quando farla. Finora il click reale non è stato provato.

---

## §1 SCOPE & ESITO FETTE

- **Registrazione C4b-1 verificato dal vivo**: `FATTA`.
- **Bottoni Approva/Rifiuta sul read-back**: `FATTA`.
- **Callback nel bridge (whitelist mittente+chat, firma via resolve_approval, ripresa orfane)**: `FATTA`.
- **Esecuzione post-approvazione (`applica_firma`, reclamo `approval_esecuzioni`, ricontrollo DENY, args salvati)**: `FATTA`.
- **F-c4a-eco**: `FATTA` (T77b).
- **Esito della firma nel contesto del modello**: `DEFERITA — C4b-3 (R-c4b2-1)`.
- **Notifica passiva di scadenza**: `DEFERITA — C5 da design`.
- **Click reale su Telegram**: `DEFERITA — decisione operatore (§0.2)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +
 gas.py                             |  68 ++++++-
 modules/memory/store.py            | 102 +++++++++++
 modules/telegram/bot.py            | 172 +++++++++++++++++-
 reports/diff_sessione.md           |  20 +-
 reports/handoff.md                 | 184 ++++++++++++-------
 reports/stato_progetto.md          |  14 +-
 reports/ultimo_report.md           |  88 +++------
 tests/test_unit_kernel.py          | 363 ++++++++++++++++++++++++++++++++++++-
 9 files changed, 858 insertions(+), 158 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
3258094 feat(c4b2): bottoni di firma + esecuzione post-approvazione — review #131/#132 APPROVATO CON RISERVE
ce31985 chore(revisore): memoria review #132 — APPROVATO CON RISERVE
224353e chore(revisore): memoria review #131 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `3258094`: review #131 (diff iniziale) e #132 (delta con i fix R-c4b2-2/3/4/5). Entrambi i verdetti sono incollati INTEGRALI qui sotto.

Nota (dell'agente principale, fuori dal verdetto): è la **riemissione** del revisore secondo il precedente della #129/#130. Tre citazioni avevano il solo nome del file, forma che `check_verdetto.py` scarta. Il revisore ha cambiato solo quella forma; esito, elementi e riserve sono invariati. Il testo NON è stato ritoccato dall'agente principale. Il revisore segnala che `modules/telegram/bot.py:149` (#131) puntava alla validazione nel diff di allora: dopo il delta della #132 la stessa riga è la 150.

### Verdetto review #131

## Review #131: C4b-2, bottoni di firma ed esecuzione dopo l'approvazione (branch feat/cancello-c4b2, diff staged)

**Esito: APPROVATO CON RISERVE**

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9), `reports/stato_progetto.md` (cercando C4b, R-c4b1, F-c4a-eco, F-mac), `.claude/agents/memoria_revisore.md` e `reports/design_cancello.md` (§4b, §4e, Fetta C4).

### Verifiche rifatte da me
- **Suite del motore:** `python tests/test_unit_kernel.py` dà **607 PASS / 5 FAIL**. I 5 FAIL sono T11c2, T11e, T12a, T12c e T12e: sono F-mac-1 (bwrap non esiste su macOS) e non sono cambiati.
- **Altri test:** `pytest tests --ignore=tests/test_unit_kernel.py` dà **232 passed**.
- **Mutation test** su una copia nello scratchpad: ho tolto un controllo alla volta per vedere se i test se ne accorgono. Tutte e 5 le mutazioni fanno cadere almeno un test:
  - M1, niente ricontrollo della whitelist nel kernel: cade T77j.
  - M2, niente ricontrollo DENY: cade T77k, e il file `.env` viene davvero scritto.
  - M3, niente controllo dell'hash nel kernel: cade T77l, e il comando manomesso viene eseguito.
  - M4, niente reclamo: cadono T77b, T77c, T77d e T77k.
  - M5, niente controllo della chat nel bridge: cadono T77g e T77h.
- **Wall of Shame:** nessuno slicing della cronologia. L'unico `[-1:]` nel diff è su `_tg77i.chiamate`, la lista delle chiamate al finto Telegram. Nessuna simulazione dell'output dei tool: T77b esegue `run_command` davvero, in os_with_fallback. Il cap di 10 iterazioni e `_get_window` non sono toccati.

### Elementi del diff esaminati
1. `gas.py:1312` (`applica_firma`): legge lo stato e non approva mai. Rischio esaminato: un'esecuzione partita senza firma valida, eseguita due volte o con argomenti manomessi. Esito **ok**: whitelist, `hash_ok`, reclamo e ricontrollo DENY reggono tutti (M1–M4). In più `gas.py` non chiama `resolve_approval` (T73f/T77n), e qualunque eccezione viene catturata e loggata come warning. **Riserva R-c4b2-3** (sotto).
2. `modules/memory/store.py:1732` (`reclama_esecuzione`) e lo schema a `modules/memory/store.py:247-279`: la chiave primaria sull'ID fa da reclamo, con BEGIN IMMEDIATE, controllo di stato approved e risolto_da telegram_user, e trigger che bloccano INSERT su richieste non approvate, DELETE e una seconda scrittura dell'esito. Rischio esaminato: doppia esecuzione per doppio click o due processi, e crash durante l'esecuzione. Esito **ok**: il crash lascia l'esito vuoto e l'azione non viene mai rieseguita (fail-closed). I trigger valgono anche da SQL grezzo (T77m).
3. `modules/telegram/bot.py:346` (`gestisci_callback`): mittente intero e non booleano dentro TELEGRAM_ALLOWED_IDS, chat dentro la whitelist, altrimenti silenzio totale. Rischio esaminato: firma da un estraneo o da un gruppo. Esito **ok** (M5). Il `chat_id` mancante viene accettato solo se il mittente è autorizzato: va bene, perché il bot non usa messaggi inline.
4. `modules/telegram/bot.py:42` (`_CALLBACK_RE`) e `modules/telegram/bot.py:149` (validazione in `invia_read_back`): **riserva R-c4b2-4**.
5. `modules/telegram/bot.py:232-235` (`allowed_updates` con callback_query): esito **ok**, coperto da T77q.

### Riserve
- **R-c4b2-1 (minore, dichiarata):** l'esito della firma non entra nel contesto del modello, mentre il design §4b dice che "il risultato entra come nuovo turno". Effetto pratico: il modello può chiedere di nuovo la stessa azione, che diventa una nuova richiesta da firmare. Accettabile perché la firma umana resta obbligatoria. Va chiusa in C4b-3 prima di considerare M2 completa.
- **R-c4b2-2 (minore, verificata):** può restare un'approvazione "orfana". Se `resolve_approval` riesce ma `applica_firma` non arriva mai (crash del processo tra le due), la richiesta resta approved senza reclamo per sempre. Un nuovo click, o la riconsegna dello stesso update, risponde "Già risolta (stato 'approved'): nessuna modifica": l'operatore crede che l'azione sia stata fatta. Correzione proposta: quando lo stato è approved e il reclamo non c'è, il bridge richiama `applica_firma` (che non può eseguire due volte grazie al reclamo), oppure manda un messaggio esplicito "approvata ma mai eseguita".
- **R-c4b2-3 (minore, verificata):** `res["eseguita"]=True` e l'intestazione "✅ Approvata ed eseguita" compaiono anche quando `execute_tool_call` restituisce "Operazione negata" (sandbox OS assente, oppure diniego di `_vet_command`). Riprodotto su macOS con os_strict: eseguita=True ed esito "[KO]". All'operatore va mostrato "eseguita" solo quando l'esito non è [KO].
- **R-c4b2-4 (cosmetica, verificata):** `_CALLBACK_RE` finisce con `$`, che in Python accetta anche un `\n` finale. Di conseguenza `invia_read_back(..., approval_id=uuid+"\n")` passa la validazione e invia il messaggio. Non è sfruttabile, perché l'ID lo genera il kernel. Basta usare `fullmatch` oppure `\Z`.
- **R-c4b2-5 (minore, UX):** `answerCallbackQuery` e la rimozione dei bottoni avvengono dopo l'esecuzione sincrona, che può durare fino a 60 s. In quel tempo l'operatore vede la rotella e i bottoni ancora attivi; l'errore "query too old" è possibile ma non l'ho verificato. Conviene rispondere alla callback e togliere i bottoni prima di eseguire. Il vero blocco contro il doppio click resta comunque il DB.
- **R-c4b2-6 (dichiarate):** durante l'esecuzione il polling è fermo (coerente con il "no threading" del design), e i bottoni degli altri destinatari non vengono rimossi. Vanno tracciate in `stato_progetto.md`.

### Cosa NON ho verificato
- **Telegram reale:** nessun click con bot vivo. Quindi non ho verificato il comportamento di `answerCallbackQuery` dopo 60 s né la risposta reale di `editMessageReplyMarkup`: in review non c'è un bot attivo, e i test sostituiscono solo lo strato HTTP.
- **Percorso bwrap su Linux** di `run_command` dopo la firma: non riproducibile su macOS (F-mac-1), resta alla CI.

### Memoria
Ho aggiunto la riga contatore #131 e due lezioni in `/Users/gas/Gas/.claude/agents/memoria_revisore.md`, committate in `224353e`. Il commit contiene solo quel file: il diff staged del motore è ancora nell'index.

Va bene committare, a condizione che le riserve R-c4b2-1…6 vengano tracciate in `/Users/gas/Gas/reports/stato_progetto.md`.

### Verdetto review #132

## Review #132: delta di C4b-2 dopo la #131 (branch feat/cancello-c4b2, diff staged)

**Esito: APPROVATO CON RISERVE**

R-c4b2-2, R-c4b2-3, R-c4b2-4 e R-c4b2-5 sono chiuse nel codice, e i test che le coprono cadono davvero se si toglie il fix. Restano aperte R-c4b2-1 e R-c4b2-6, come dichiarato. Le sonde hanno trovato 3 problemi nuovi minori e uno cosmetico: nessuno blocca il commit.

Ho riusato le letture obbligatorie già fatte in questa sessione per la #131 (CLAUDE.md sez. 5/8/9, `stato_progetto.md` cercando C4b, la memoria aggiornata fino alla #131, design §4b/§4e).

### Verifiche rifatte da me
- **Suite del motore:** `python tests/test_unit_kernel.py` dà **614 PASS / 5 FAIL**. I 5 FAIL sono T11c2, T11e, T12a, T12c e T12e: F-mac-1 (bwrap assente su macOS), invariati. Il numero di pytest (232) l'ho misurato nella #131: il delta non tocca quei test e non l'ho rilanciato.
- **Mutation test** su una copia nello scratchpad: ho annullato ogni fix uno alla volta. Tutte e 5 le mutazioni fanno cadere almeno un test.

| Mutazione | Test che cadono |
|---|---|
| N1 — scadenza dell'orfana ignorata | T77s |
| N2 — `eseguita = True` sempre | T77t, T77k |
| N3 — `.match` al posto di `fullmatch` | 5 casi di T77h |
| N4 — niente nuovo tentativo sull'orfana | T77r (4 check), T77s |
| N5 — niente controllo `get_esecuzione` | T77c, T77r |

  Con N5 cadono solo i messaggi: la seconda esecuzione resta comunque bloccata dal reclamo. Quindi `get_esecuzione` serve all'esattezza del messaggio, non alla sicurezza.
- **Wall of Shame:** nessuno slicing della cronologia nel delta e nessuna simulazione dell'output dei tool (T77r/T77t eseguono davvero). Il cap di 10 iterazioni e `_get_window` non sono toccati.

### Elementi del diff esaminati
1. `modules/telegram/bot.py` (`_riprova_orfana`, chiamata da `gestisci_callback` solo con azione "ok"): rilegge la riga e richiama `applica_firma` solo se la richiesta è approved, senza esecuzione registrata e non scaduta. Rischio esaminato: una seconda esecuzione, o un'esecuzione dopo la scadenza. Esito **ok**:
   - il reclamo resta la barriera (N5);
   - la scadenza è portante (N1);
   - Rifiuta su una richiesta approved non ha effetti (T77r);
   - in più, la riconsegna dell'update dopo un crash ora recupera da sola l'orfana.
2. `modules/memory/store.py:1781` (`get_esecuzione`): sola lettura, UUID validato, in caso di errore restituisce None. Rischio esaminato: un errore del DB scambiato per "nessun reclamo", che farebbe ripartire `applica_firma`. Esito **ok**: `reclama_esecuzione` fallisce comunque sulla chiave primaria (fail-closed).
3. `gas.py:1367` (`res["eseguita"] = not esito.startswith("[KO]")`). Rischio esaminato: un diniego interno mostrato all'operatore come esecuzione. Esito **ok** per vetting, sandbox e DENY (T77t, T77k). **Riserva R-c4b2-9** per il dry-run.
4. `modules/telegram/bot.py:150` e `modules/telegram/bot.py:388` (`_CALLBACK_RE.fullmatch`): rischio esaminato, un `\n` finale accettato. Esito **ok** (T77o con UUID+"\n", T77h, N3).
5. `bot.py`, `gestisci_callback`: `answerCallbackQuery` ("Firma ricevuta.") ed `editMessageReplyMarkup` partono prima di resolve ed esecuzione (T77r lo misura). Esito **ok** per R-c4b2-5. **Riserva R-c4b2-7.**

### Riserve
- **R-c4b2-1 (aperta, dichiarata):** l'esito della firma non entra nel contesto del modello. Va fatto in C4b-3.
- **R-c4b2-6 (aperta, dichiarata):** il polling resta fermo durante l'esecuzione, e i bottoni degli altri destinatari non vengono rimossi.
- **R-c4b2-7 (minore, verificata):** il fix di R-c4b2-5 toglie i bottoni prima di `resolve_approval`. Se resolve fallisce per un errore transitorio (ho simulato un `OperationalError` "database is locked"), la richiesta resta pending ma senza bottoni: l'operatore riceve "Nessuna modifica…: errore interno" e non può più firmarla da Telegram fino alla scadenza. È fail-closed (nessuna esecuzione), ma la richiesta resta bloccata. Correzione proposta: se dopo resolve lo stato è ancora pending, rimettere i bottoni con `bottoni_firma(aid)`, oppure dirlo esplicitamente nel messaggio.
- **R-c4b2-8 (cosmetica, verificata):** se il processo si ferma a metà esecuzione, il reclamo c'è ma l'esito è vuoto. A un nuovo click il messaggio dice "Già risolta (stato 'approved'): nessuna modifica" invece di "esecuzione iniziata, esito ignoto".
- **R-c4b2-9 (minore, verificata):** la R-c4b2-3 ha un residuo in dry-run. Con `shell_mode="dry_run"`, `_esito_diario` dà "[OK] (non eseguito)", quindi `eseguita=True` e l'operatore legge "✅ Approvata ed eseguita". Succede solo con quella configurazione; va trattato anche "(non eseguito)" o il prefisso "[DRY-RUN]".
- **R-c4b2-10 (cosmetica, test):** in T77s, enqueue e resolve devono stare entro 0,3 s. Su una CI lenta resolve può arrivare dopo la scadenza: la richiesta diventa expired e il test cade (rischio di test instabile).

### Cosa NON ho verificato
- **Telegram reale:** nessun click con bot vivo. In particolare non ho verificato che `answerCallbackQuery` anticipata eviti davvero l'errore "query too old": in review non c'è un bot attivo, i test sostituiscono solo lo strato HTTP.
- **Percorso bwrap su Linux** (T77r/T77b con sandbox vera): non riproducibile su macOS (F-mac-1), resta alla CI.

### Memoria
Ho aggiunto la riga contatore #132 e una lezione in `/Users/gas/Gas/.claude/agents/memoria_revisore.md`, committate in `ce31985`. Il commit contiene solo quel file; il diff staged del motore (4 file, +693/−12) è ancora nell'index.

Va bene committare, a condizione che R-c4b2-1, 6, 7, 8, 9 e 10 vengano tracciate in `/Users/gas/Gas/reports/stato_progetto.md`.

## §5 DELTA TEST DEL MOTORE

`python tests/test_unit_kernel.py`: **558 → 614 PASS**, FAIL 5 → 5. `pytest tests --ignore=tests/test_unit_kernel.py`: 232 → 232 passed.

```
=== RIEPILOGO: 614 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
```

I 5 FAIL sono fuori scope: F-mac-1, cioè bwrap assente su macOS. Sono invariati e in CI (Linux con bwrap) passano.

## §6 STATO CI

```
completed	success	feat(c4b2): bottoni di firma + esecuzione post-approvazione — review …	CI	feat/cancello-c4b2	push	37140519481	1m10s	2026-10-03T17:26:40Z
completed	success	Merge pull request #115 from Gasss23/fix/c4b1-suite-ermetica	CI	main	push	37114771701	1m38s	2026-10-03T09:57:18Z
completed	success	docs(c4b1-ermetica): fine-task — test di parità app/terminale, suite …	CI	fix/c4b1-suite-ermetica	push	37114633812	1m38s	2026-10-03T09:54:46Z
```

Mappatura commit→run:
- `3258094` (testa al push): run 37140519481 — **completed success** (Linux con bwrap; testa l'albero di `3258094`).
- `ce31985`: nessuna run su questo SHA (pushato insieme a `3258094`, il suo contenuto è nell'albero testato).
- `224353e`: nessuna run su questo SHA (stesso push, contenuto incluso nell'albero testato).
- Commit di fine-task (questo file): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-c4b2-1 — l'esito della firma non entra nel contesto del modello → C4b-3.
- R-c4b2-6 — il polling è fermo durante l'esecuzione; i bottoni degli altri destinatari non vengono rimossi.
- R-c4b2-7 — se resolve fallisce in modo transitorio, la richiesta resta pending senza bottoni.
- R-c4b2-8 — con reclamo presente ed esito vuoto, il messaggio è impreciso.
- R-c4b2-9 — in dry-run l'operatore legge "eseguita".
- R-c4b2-10 — T77s ha una soglia di 0,3 s, rischio di test instabile su CI lenta.
- Aperte da prima: R-c4b1-3, R-c4b1-4, R-erm-1, R-erm-2, F-env-app (vedi stato_progetto).
