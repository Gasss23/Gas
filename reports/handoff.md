# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-23 — Gas usa il CRM: comandi da Telegram e voce, con firma e solo Opus

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #397 (https://github.com/Gasss23/Gas/pull/397). Fetta di sicurezza (cancello delle firme, scelta del modello): secondo controllo su claude.ai col link della PR.
2. **R-840-2 (MEDIA), falsi allarmi del filtro «solo Opus»**: un messaggio con «clienti», «commissione», «versato», «deposito» o un numero lungo che inizia con 0 o 3 va solo a Opus; col cervello forte spento o al tetto quel turno, e quello dopo, si fermano con «contiene dati di clienti». Scelte: tenere così (privacy prima), togliere qualche parola, o un messaggio più chiaro.
3. Privacy, da sapere e confermare: le conversazioni con Gas sui clienti restano nella storia di Gas (`.gas_history.json`), le richieste di firma nella sua memoria (`.gas_memory.db`); i messaggi passano da Telegram come la chat di oggi; a voce i dati passano da Groq (trascrizione) ed ElevenLabs (voce). Nel diario di Gas non vanno nomi né cifre dei clienti.
4. Restano dalle fette prima: lista delle commissioni per servizio; sul Mac password delle copie nel `.env`, `pip install -r requirements.txt`, `pwd` della cartella di Gas, prova della copia e del ripristino; secondo controllo su claude.ai delle PR #387, #388, #389 e #391; decisione sulle parole di gravità del bot («alto», «severo», «serio», «elevato»).
5. Ereditata dalla chat Voce: rifare la registrazione della voce sul Mac con lo script corretto e incollare il riepilogo.

---

## §1 SCOPE & ESITO FETTE

- **Decisione 18 e bacheca**: FATTA. Richiesta dell'operatore («posso usare il mio agente IA e dargli comandi per utilizzare il crm? aggiungere, togliere, ricordarmi»), proposta scelta «Sì, fallo tu qui», in `reports/crm/decisioni.md` punto 18; notizia in `reports/bacheca.md`.
- **Tappa 1, lato CRM** (f7a4c12c): FATTA, review #839-CRM APPROVATO CON RISERVE. Promemoria nello store, `modules/crm/agente.py` (consulta, prepara, applica).
- **Tappa 2, aggancio a Gas + riserve #839** (c8d4f977): FATTA, review #840-CRM APPROVATO CON RISERVE. Strumenti `crm_consulta`/`crm_modifica`, cancello, solo Opus, importi dal messaggio del turno, promemoria su Telegram.
- **Riserve #840** (0afc1a79): FATTA. Review #841-CRM BOCCIATO (R-841-1 ALTA: il nuovo controllo dei telefoni scattava dentro gli UUID delle firme) → corretto → #842-CRM APPROVATO CON RISERVE.
- **Riserve #842** (070e7ad3): FATTA, review #843-CRM APPROVATO CON RISERVE (resta R-843-1 BASSA).
- **R-840-2**: DEFERITA — decisione dell'operatore (§0 punto 2).
- **Prova su Mac, Telegram e `claude -p` veri**: SALTATA — non raggiungibili da qui; provato con client finti.
- **Anomalia durante il fine-task**: un primo tentativo di scrivere questo file con un heredoc non quotato ha fatto eseguire alla shell i testi tra apici inversi della prosa (tra cui `pip install -r requirements.txt` nel container, la suite del kernel e `claude -p` senza input, che ha dato errore). Il file non è stato scritto; nel repo nessun commit, nessun push, cambiati solo log e cache ignorati da git. Riscritto con file temporanei e heredoc quotato.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  15 +++++++
 gas.py                             | 173 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 modules/crm/agente.py              | 776 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/store.py               | 187 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 modules/gate/gate.py               |   7 ++++
 modules/telegram/bot.py            |  49 +++++++++++++++++++++++
 reports/bacheca.md                 |   1 +
 reports/crm/decisioni.md           |   4 ++
 reports/crm/guida.md               |  13 +++++-
 reports/diff_sessione.md           |  17 ++++----
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 +-
 reports/ultimo_report.md           |  39 +++++++++---------
 tests/test_unit_crm.py             | 304 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_kernel.py          | 297 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
070e7ad3 test(gas): R-842-1 — casi limite del filtro dei telefoni provati; limiti R-842-2/3 dichiarati (review #843-CRM)
0afc1a79 fix(gas): riserve #840-CRM e BOCCIATO #841-CRM — filtro delle richieste del CRM senza falsi telefoni negli UUID (review #842-CRM)
c8d4f977 feat(gas): Gas usa il CRM, tappa 2 — crm_consulta e crm_modifica con firma, solo Opus, promemoria su Telegram (review #840-CRM)
a7f74ff8 docs(stato): tappa 1 del CRM in Gas e riserve della review #839-CRM
f7a4c12c feat(crm): comandi del CRM per Gas, tappa 1 — promemoria e modulo agente (review #839-CRM)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #839-CRM, commit f7a4c12c (verdetto integrale incollato):

## VERDETTO: APPROVATO CON RISERVE

Review **#839-CRM**: diff staged sul ramo `claude/nifty-galileo-3k7kbm`, 5 file, +1070/−16, sha256 del diff e60ad812, sopra bf428441. Il diff staged non l'ho toccato (lo sha256 è uguale prima e dopo la review).

Letture obbligatorie fatte: CLAUDE.md §5 (con §1, §8, §10), `reports/stato_progetto.md` (letto a pezzi) e le lezioni di `memoria_revisore.md` (in particolare quelle sul CRM e sui mutanti per ramo).

### Prove rieseguite da me
- **CRM**: `pytest tests/test_unit_crm.py` dà 149 passed.
- **Kernel**: `python tests/test_unit_kernel.py` dà 1191 PASS, 0 FAIL.
- **Test di mutazione**: 19 mutanti provati in un worktree nella cartella temporanea, già tolto. 12 sono stati uccisi, 7 sopravvivono a tutta la suite CRM (vedi R-839-2).
- **mypy** su `agente.py` e `store.py`: 3 errori, tutti in `agente.py`.

### Elementi del diff esaminati
- `modules/crm/agente.py:266`: prepara accetta solo le chiavi che il modello può passare. Rischio (1), cioè il modello che passa da sé id e centesimi: chiuso a prepara, perché `{"v":1, "cliente_id", "importo_cents"}` è rifiutato e il mutante che toglie il controllo viene ucciso. Esito: ok.
- `modules/crm/agente.py:506`: applica controlla solo la FORMA canonica, non da dove viene. Una canonica costruita a mano e ben fatta passa. L'affermazione del docstring (righe 14-15, «il modello non può saltare i controlli») vale solo se nella tappa 2 il kernel passa ad applica l'oggetto salvato da prepara. Esito: riserva R-839-5.
- `modules/crm/agente.py:347` e `modules/crm/agente.py:360`: il controllo dell'importo detto dall'operatore c'è sia in apri_servizio sia in movimento. Nessun mutante sopravvive su movimento; su apri_servizio il mutante che toglie il controllo SOPRAVVIVE, quindi una delle due strade del denaro non è fissata da nessun test. Esito: riserva R-839-2.
- `modules/crm/agente.py:87` (importi_nel_testo): conta come «detto» qualunque numero del testo. Prove mie:
  - «oggi 20/06» fa accettare 20,00 €;
  - «alle 15:30» fa accettare 30,00 €;
  - «#12» vale 12 €;
  - il test a `tests/test_unit_crm.py:2304` fissa proprio «23/11» come 23 € e 11 €.

  La vera barriera resta la firma, ma il limite non è dichiarato da nessuna parte. Esito: riserva R-839-4.
- Rischio (2), prepara che scrive: escluso con una mia sonda. Dopo 9 chiamate a prepara (tutte le azioni, successi ed errori) e 6 a consulta, `PRAGMA data_version` letto da un'altra connessione è invariato e l'hash del file .db è identico. Il mutante «testo nel diario» viene ucciso. Esito: ok.
- Rischio (3), differenze tra prepara e lo store. Ci sono due casi in cui l'azione firmata fallisce DOPO la firma, entrambi riprodotti:
  - un prelievo da 5.000 € su 1.000 € di capitale passa prepara; applica poi lo rifiuta col controllo di `modules/crm/store.py:895`;
  - la riattivazione di una posizione chiusa: la firma dice «dal 2026-03-01 con DEPOSITO di 200 €», applica fallisce con «data prima dell'apertura» (2026-04-01); con una data valida la firma dice «dal 2026-06-10» ma `aperta_il` resta 2026-04-01 (`modules/crm/store.py:781`).

  In entrambi i casi non viene scritto niente. Esito: riserva R-839-3.
- Rischio (4), ricerca per nome (`modules/crm/agente.py:159`): il pezzo di nome viene cercato anche DENTRO una parola. Prova mia: con «Anna» il deposito di 300 € va su «Marianna Verdi (cliente #1)», senza nessun avviso nella firma. Il test a `tests/test_unit_crm.py:2381` dice «il nome uguale vince sul pezzo di nome», ma non lo prova: il mutante «solo pezzo di nome» sopravvive. Esito: riserva R-839-1 MEDIA.
- Rischio (5), reclamo e rilascio dei promemoria (`modules/crm/store.py:1302`, `modules/crm/store.py:1318`):
  - l'UPDATE condizionato è atomico: 8 giri concorrenti, ognuno col suo CRMStore, si dividono 30 promemoria scaduti, 30 reclami vinti e nessun doppione;
  - un promemoria annullato e poi rilasciato resta fuori dalla coda;
  - il mutante che toglie la condizione dal reclamo viene ucciso; quello che toglie solo `annullato_il IS NULL` sopravvive (corsa tra annullo e reclamo non testata).

  Esito: ok, con nota in R-839-2.
- Rischio (6), refactor dell'anagrafica (`modules/crm/store.py:443`, `modules/crm/store.py:669`, `modules/crm/store.py:707`): confrontato lo `store.py` di HEAD con quello dell'indice su 1344 casi (un campo strano alla volta e coppie di campi, per aggiungi e aggiorna): 0 differenze, né di esito né di messaggio d'errore. Esito: ok.
- Wall of Shame, `modules/crm/agente.py:672`: lo slicing `store.movimenti(cid)[-10:]` taglia righe del registro CRM ordinate per data, NON la cronologia dei messaggi, quindi non è l'antipattern. Nessuna simulazione di output dei tool. consulta intercetta ogni eccezione e la logga (§9). Esito: ok.

### Riserve
1. **R-839-1 (MEDIA)**: il pezzo di nome dentro una parola sceglie un'altra persona senza avviso (Anna dentro Marianna, Lia dentro Giulia). Va contro la linea «niente ricerche approssimate sull'identità» delle fette CRM precedenti, e scrive in un registro che non si corregge. Correzione: cercare il pezzo solo a inizio parola e, quando il nome non è uguale, scrivere nella firma «ATTENZIONE: hai scritto «X», trovato per somiglianza». Da chiudere prima della tappa 2, cioè prima che lo strumento sia raggiungibile dal modello.
2. **R-839-2 (BASSA)**: 7 mutanti sopravvivono a tutta la suite CRM:
   - controllo dell'importo detto in apri_servizio;
   - «nome uguale vince»;
   - telefono già usato, controllato in aggiorna_cliente;
   - telefono del cliente stesso non escluso dal controllo;
   - avviso degli omonimi;
   - consenso marketing ignorato da applica in nuovo_cliente;
   - reclamo di un promemoria annullato.

   I primi due sono quelli importanti: costano un test ciascuno.
3. **R-839-3 (BASSA)**: errori che arrivano dopo la firma:
   - per il prelievo, anticipare in sola lettura il controllo del saldo dentro prepara (`_saldo_minimo_da` è statico);
   - per la riattivazione, scrivere nella firma «riattiva (aperta dal …)» e controllare in prepara la data rispetto alla vecchia `aperta_il`.
4. **R-839-4 (BASSA)**: importi_nel_testo conta anche date, ore e #id. Va dichiarato nel docstring, oppure vanno esclusi date, ore e `#n`.
5. **R-839-5 (BASSA)**, contratto da rispettare nella tappa 2, con test:
   - applica riceve solo l'oggetto canonico salvato da prepara lato kernel, mai gli argomenti del modello;
   - `testo_operatore` contiene solo i messaggi dell'operatore, mai i risultati di crm_consulta (che contengono cifre in €) né testo del modello;
   - l'invio dei promemoria va dichiarato «al più una volta»: un crash tra reclamo e invio perde il promemoria in silenzio, e un rilascio dopo un invio andato in timeout ma consegnato lo manda due volte.
6. **R-839-6 (BASSA)**: un id intero ≥ 2^63 come cliente (`modules/crm/agente.py:134`, senza tetto) fa uscire da prepara e da applica un OverflowError, non un ErroreCRM, e il contratto «Solleva ErroreCRM» si rompe. consulta lo intercetta. Correzione: tetto 2**62 in `_rif_id` e in `intero()`.
7. **R-839-7 (BASSA)**: aggiorna_cliente su `note` SOSTITUISCE tutta la nota, ma la firma (`modules/crm/agente.py:412`) mostra solo il testo nuovo. «Aggiungi una nota: ha chiamato» cancella la nota vecchia senza che l'operatore lo veda, contro lo spirito di «niente cancellazioni». Mostrare nella firma «prima: «…»» per nome, telefono, email e note.
- **COSMETICHE**:
  - 3 errori mypy in `agente.py` (righe 332, 380, 396), contro i type hints rigorosi di §4;
  - `reclama_promemoria(True)` reclama il #1 per via di `int(True)`;
  - in `_valida_canonico` un `campi` che non è un dizionario dà TypeError prima del controllo di tipo (`modules/crm/agente.py:439` viene prima di `modules/crm/agente.py:453`; succede solo con canoniche costruite a mano);
  - il controllo degli omonimi non toglie gli accenti (Nicolò e Nicolo non vengono segnalati).

### Rischi esclusi (non verificati)
- **Tappa 2 nel suo insieme**: aggancio in gas.py, cancello delle firme, «solo Opus» per consulta, invio su Telegram. Non verificabile: il codice non esiste ancora, e nessuno strumento è oggi raggiungibile dal modello.
- **Orari dei promemoria al cambio dell'ora legale** sul Mac: non riprodotti. Ragionando sul confronto fra stringhe, un'ora che non esiste parte al minuto dopo e una doppia parte la prima volta.
- **Contenuto dei documenti** (`reports/bacheca.md`, `reports/crm/decisioni.md`): letto e coerente col codice, salvo il limite di R-839-4. È fuori perimetro.

### Memoria
- Ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga contatore #839-CRM e 3 lezioni nuove: pezzo di nome dentro una parola; controlli fatti nella transazione da anticipare in prepara; numeri di date, ore e id letti come importi.
- **Il commit della memoria NON è stato fatto**: tu hai chiesto di non committare e il permesso per `scripts/commit_memoria_revisore.sh` mi è stato negato. Il file è modificato ma non in staging: va incluso nel tuo commit.
- `.claude/.review_ok` non l'ho creato.

---

Review #840-CRM, commit c8d4f977 (verdetto integrale incollato):

## VERDETTO: APPROVATO CON RISERVE

Review #840-CRM. Diff staged sul ramo claude/nifty-galileo-3k7kbm sopra a7f74ff8: 8 file, +601/−48, sha256 del diff de0fb4ab (prima e dopo la mia review). Ho letto CLAUDE.md §5, la riga «Stato motore» di reports/stato_progetto.md e la mia memoria (#839-CRM).

**Test rieseguiti da me su una copia dell'indice**: kernel 1201 PASS / 0 FAIL, CRM 150 passed, mypy pulito su modules/crm (le 3 cosmetiche mypy di #839 sono chiuse). Mutanti: 21 sul CRM (17 uccisi), 15 sul kernel e sul bot (5 uccisi). Ho anche lanciato sonde dentro run_turn, con modelli finti, solo nella copia.

**Elementi del diff esaminati**
- `gas.py:3849` — crm_modifica al cancello passa da _prepara_crm e si parcheggia la forma canonica. Rischio: scrittura senza firma o con argomenti del modello. Esito **ok**. L'unico chiamante con firmata=True è applica_firma (`gas.py:4055`), che usa gli argomenti salvati con l'hash. Dal ciclo crm_modifica dà sempre «Operazione negata» (`gas.py:5465`).
- `gas.py:5546` — il testo dell'operatore è solo user_prompt del turno, None in sottofondo. Rischio: cifre lette nel CRM o nella storia contate come «dette». Esito **ok**: il mutante «testo = tutta la storia» fa fallire T118c2 (`tests/test_unit_kernel.py:13732`).
- `gas.py:5832` — `_chiamata_opus` viene impostato prima di ogni chiamata e azzerato all'inizio del turno e nel finally (`gas.py:6099`). Rischio (3): il flag resta vero quando non deve. Esito **ok**: applica_firma non lo usa, il server voce lavora in un solo thread e il bot ha un kernel per processo. I mutanti «= True» e «senza e_modello_opus» però passano 1201 PASS: R-840-3.
- `gas.py:5454` — crm_consulta senza Opus dà un diniego che porta lo strumento nella finestra. Rischio (1). Esito **ok** dalla sonda P1: /forte con Sonnet viene negato, la chiamata dopo è Opus e l'output arriva solo a Opus.
- `gas.py:361` — la regex delle parole del CRM vale sui soli messaggi user. Rischio (4). Esito **riserva**: R-840-1 e R-840-2.
- `gas.py:6012` e `gas.py:2896` — progressi e diario senza dati. Rischio (5). Esito **ok** nei fatti (sonda P4: diario «crm-negata | [KO]»). Non è pinnato: R-840-4.
- `modules/gate/gate.py:83` — crm_consulta SAFE, crm_modifica IRREVERSIBLE; `modules/gate/gate.py:106` mette crm_consulta tra le letture non fidate. Rischio (6), regressioni. Esito **ok**: solo aggiunte, e dopo una lettura del CRM gli strumenti che scrivono fuori vanno alla firma.
- `modules/telegram/bot.py:494` — promemoria: reclamo, invio, rilascio se fallisce. Esito **riserva**: R-840-6.
- `modules/crm/agente.py:147`, `modules/crm/agente.py:440`, `modules/crm/agente.py:90`, `modules/crm/agente.py:160`, `modules/crm/agente.py:491` — chiusura di R-839-1/3/4/6/7. Esito **ok**: i mutanti (`in` al posto dell'inizio di parola, avviso tolto, nome uguale che non vince, niente accenti, controllo del capitale, data della riattivazione, date/ore/ISO, ID_MAX, nota vecchia) fanno fallire la suite. R-839-2 chiusa: importo detto in apri_servizio, consenso, telefono in aggiorna e reclamo di un annullato ora uccisi. R-839-5 è dichiarata nel docstring di `modules/crm/store.py:1313` e nella guida.
- Test adattati, T80 (`tests/test_unit_kernel.py:8752`) e T116h (`tests/test_unit_kernel.py:13480`): **coerenti**, non indeboliscono niente. T80 prova la riflessione coi cervelli normali, e con «cliente» oggi andrebbe giustamente a Opus. In T116h «ricordami» chiuderebbe la ricerca al primo messaggio e la prova di velocità non misurerebbe più il caso peggiore.
- Contesto: `gas.py:1966`, la compressione porta l'output degli strumenti (300 caratteri) in un messaggio user e cancella il messaggio tool. Ho provato i 6 tipi di consultazione: ogni output con dati di clienti resta riconoscibile da parole o nomi. «servizi» non ha dati di clienti. **ok**.

**Riserve**
- **R-840-1 MEDIA**, falsi negativi della regex (rischio 1, lato ingresso). Un messaggio con i dati di un cliente NUOVO senza le parole della lista va prima a un modello gratuito. Nella sonda P2 Gemini riceve «Paolo Neri, 5 mila»; poi arriva il diniego e il turno passa a Opus. Non prese: «ha depositato», «ha prelevato», «versamento», «bonifico», «aggiungi Anna Neri, 333 1234567». Non è una regressione rispetto alla fetta 3, ma la decisione 18 dice «solo Opus». Rimedi poco costosi: radici più larghe (`deposit\w*`, `prele?v\w*`, `versament\w*`), un numero di telefono (7 o più cifre) contato come dato personale, e il limite scritto nella guida («per un cliente nuovo usa la parola cliente»). Attenzione: allargare la lista aumenta R-840-2.
- **R-840-2 MEDIA, decide l'operatore**: falsi positivi. «clienti», «commissione», «versato», «deposito» sono comuni nel lavoro di marketing e mandano il turno a Opus. Col forte spento o al tetto il turno si ferma con «Questa richiesta contiene dati di clienti» (falso). Si ferma anche il turno dopo: sonda P3, «che ore sono?» bloccato. Gas resta muto finché il messaggio è nella finestra (10 messaggi). Il commento a `gas.py:145` dichiara solo il costo. Opzioni: tenere così (privacy prima), togliere parole, o un messaggio che dica «parole del CRM».
- **R-840-3 BASSA**: il calcolo del flag nel ciclo non è pinnato. T118d imposta `_chiamata_opus` a mano (`tests/test_unit_kernel.py:13740`). Servono due test di run_turn: /forte con Sonnet che chiede crm_consulta → negato, poi Opus; turno sui gratuiti con crm_modifica → negato, nessuna firma.
- **R-840-4 BASSA**: privacy non pinnata. Sopravvivono questi mutanti:
  - via la riga crm_consulta di _riassumi_args: il diario riceverebbe `cliente='Mario Rossi'` dal riassunto generico (`gas.py:2905`). T118c2 chiama crm_consulta col nome ma non guarda il diario;
  - crm_consulta tolto dalle letture non fidate;
  - via rendi_visibili dalla descrizione in _prepara_crm. È l'unico filtro: il read-back non pulisce azione_leggibile (`modules/telegram/bot.py:232`).
- **R-840-5 BASSA**, voce: la guida invita a dare i comandi del CRM a voce, ma non dice che l'audio va a Groq (trascrizione) e la risposta a ElevenLabs. È un rischio accettato il 6 novembre per la voce in generale; per i dati dei clienti va dichiarato all'operatore.
- **R-840-6 BASSA**: un promemoria che supera il limite di Telegram (500 caratteri invisibili + nome lungo = 4166 > 4096, provato) viene rilasciato e riprovato a ogni giro. Col `break` (`modules/telegram/bot.py:513`) blocca per sempre la coda: «normale» non parte mai, e c'è un warning ogni minuto. Inoltre i mutanti break→continue, senza tetto di 10 e senza rendi_visibili in componi_promemoria sopravvivono.

**COSMETICHE**
- Il test di `reclama_promemoria(True)` usa un #1 annullato, quindi il mutante sopravvive (`tests/test_unit_crm.py:2583`).
- «(prima: …)» per i campi diversi dalla nota non è pinnato, e nemmeno capitale None / capitale_minimo_dal in errore.
- Nei progressi lo scambio a Opus appare come «CRM: consultazione non riuscita.».
- La guida dice «mai da un compito lungo», ma i compiti della notte (che non sono «sottofondo») possono preparare modifiche.
- Nomi con apostrofo o trattino: «Amico» non trova «D'Amico».
- Il bot crea un `.gas_memory_crm.db` vuoto sulle macchine senza CRM. Il file è ignorato da git e la riapertura non scrive (hash e data_version invariati, provato).
- Il mutante che toglie l'azzeramento nel finally sopravvive: è equivalente, c'è già l'azzeramento a inizio turno.

**Rischi esplicitamente esclusi**
- Comportamento con la vera `claude -p` e con Telegram reale: non verificato, provato solo con client finti, il Mac non è raggiungibile da qui.
- Trascrizione reale delle cifre a voce (Whisper che scrive «1.500» oppure «millecinquecento»): non verificata.
- Lezioni o recap scritti da Opus dopo una conversazione sul CRM che riportano cifre senza nomi, poi dati in forma anonima ai gratuiti: meccanismo della fetta 3, non toccato da questo diff, non provato.
- Le altre suite della CI: non eseguite da me.

**Memoria**: aggiunta la riga #840-CRM e 3 lezioni in /home/user/Gas/.claude/agents/memoria_revisore.md (file non in staging). Non ho eseguito il commit né commit_memoria_revisore.sh, come mi hai chiesto: lo committi tu. Non ho creato .claude/.review_ok. Le sonde e lo script dei mutanti sono in /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/tools/.

---

Review #841-CRM sul primo diff delle riserve #840 (non committato; corretto e riesaminato in #842-CRM), verdetto integrale incollato:

## VERDETTO: BOCCIATO

Review #841-CRM, 2026-11-23. Diff staged: 6 file, +114/−11, sopra c8d4f977, sha256 del diff 60648b1d. Ho rieseguito tutto su una copia dell'indice: kernel 1205 PASS, CRM 150 passed, mypy pulito su modules/crm/agente.py. Ho provato 17 mutanti e misurato a parte gli UUID.

**Motivo bloccante**

**R-841-1 ALTA, regressione introdotta da questo diff.** Il ramo "telefono" della regex scatta dentro gli UUID delle firme.
- Dove: gas.py:154 (il ramo `(?<![0-9/\-])\+?[0-9](?:[ .]?[0-9]){6,14}(?![0-9/\-])`). I confini escludono solo cifre, `/` e `-`, non le lettere: 7 cifre di fila dentro un UUID esadecimale bastano (es. `…-622b2625969b` → trova `2625969`).
- Perché conta: la notifica del kernel dopo ogni firma è un messaggio in ruolo user che contiene l'UUID (gas.py:3964). `_finestra_ha_dati_lead` la conta quindi come richiesta del CRM.
- Misura: 1671 UUID su 20.000 (8,4%).
- Effetto a runtime, per qualunque firma (anche run_command):
  - nei turni dopo, finché la notifica resta nella finestra, la conversazione va solo a Opus;
  - col forte spento o al tetto, il turno si ferma con «Questa richiesta contiene dati di clienti», che è falso.
- Effetto sulla CI: la unit-suite è un check required e diventa instabile.
  - Con UUID forzati ad avere 7 cifre falliscono T78b (3 check), T78d, T78l e T78r: 6 FAIL.
  - Nelle mie 15 run dalla stessa base è fallita due volte da sola: T78r nella run del mutante M6 e T78d nella run del mutante M14, mutanti che non c'entrano.
  - Stima: circa 1 run su 4-7 rossa a caso.
- Rimedio provato: confini di parola `(?<![\w/\-])…(?![\w/\-])`. 0 UUID su 20.000 scattano; «333 1234567», «+39 333 123 4567», «tel:3331234567», «02.1234567» e «(02) 12345678» vengono ancora presi.
- Va aggiunto un caso negativo in T118e con una notifica di firma (UUID) o con un hash.

**Riserve (da sistemare nello stesso giro o da tracciare)**

- **R-841-2 MEDIA, falsi positivi nuovi oltre le parole decise dall'operatore** (R-840-2 copre la scelta delle parole, non questi). Provati, scattano tutti:
  - `client\w*` prende l'inglese «client»: «il client voce sul Mac non parte», «client.chat.completions»;
  - `versa\w*` prende «un copy versatile», «il versante nord», «versa l'acqua»;
  - date col punto «17.11.2026» e «17 11 2026», anche se il commento dice «non date»;
  - numeri grandi «1.000.000 di visualizzazioni», l'IP «192.168.1.10», il timestamp «1732000000».
  - Col forte spento questi messaggi fermano il turno e i successivi. Proposta: `client[ei]\w*` (prende cliente, clienti, clientela, non l'inglese) e forme precise di «versare». Altrimenti questi esempi vanno nelle DECISIONI UMANE accanto a R-840-2.
- **R-841-3 BASSA, chiusure non provate dai test.**
  - Il taglio a 1500 di modules/telegram/bot.py:489 non è pinnato: il mutante che torna a `rendi_visibili` senza taglio passa (1205 PASS). Il testo del test, tests/test_unit_kernel.py:13852, è `"x‮" * 250` = 500 caratteri, che diventano 2250 dopo `rendi_visibili`: resta sotto 4096 anche senza taglio. Usare `"‮" * 500`, che è al massimo consentito e fa circa 4180 senza taglio.
  - Mutanti vivi anche per i lookaround del ramo telefono (il caso negativo con «15:30» non li esercita; servirebbe «17/11/2026 15.30»), per `bonific\w*` da solo e per `versa\w*` da solo (T118e li ha nella stessa frase).
- **R-841-4 BASSA**: i telefoni col trattino o la barra («333-1234567», «333/1234567») non contano. La guida (reports/crm/guida.md:96) parla di «un numero di telefono» senza questo limite. Va gestito (le date hanno al massimo 8 cifre) oppure dichiarato.

**COSMETICHE (una riga)**: `tronca_visibile` usa `a_capo=False`, quindi gli a capo di un promemoria ora escono come `<U+000A>` (prima restavano); «CRM: passo a Claude Opus.» compare anche quando il turno poi si ferma col forte spento; restano vivi lo split di `cerca` solo a spazi (agente.py:152) e la riga crm_modifica di `_riassumi_args` (non dichiarata).

**Elementi del diff esaminati**

- gas.py:154 — ramo telefono della regex — falsi positivi su UUID, hash e date (sonda su 40 frasi e 20.000 UUID) — **blocco** (R-841-1).
- gas.py:5839 — calcolo di `_chiamata_opus` — mutanti «= True» e «senza e_modello_opus» uccisi da T118g — ok, R-840-3 chiusa.
- gas.py:6018 — progressi «CRM: passo a Claude Opus.» — mutante che toglie il ramo ucciso da T118g — ok.
- gas.py:2903 e gas.py:3825 — riga crm_consulta del diario e `rendi_visibili` della firma — mutanti uccisi da T118c2 e T118d — ok, R-840-4 chiusa.
- modules/telegram/bot.py:489 — taglio a 1500 — il limite regge (al massimo circa 3300 unità UTF-16 anche con emoji), ma il test non lo prova — riserva (R-841-3).
- modules/telegram/bot.py:514 — break al primo invio fallito, più il tetto di 10 per giro — mutanti uccisi da T118f2 — ok.
- modules/crm/agente.py:151 — split anche su apostrofi e trattini («amico» → «D'Amico», con avviso) — mutante ucciso (tests/test_unit_crm.py:2540) — ok.
- reports/crm/guida.md:97 — voce via Groq ed ElevenLabs dichiarata — ok, R-840-5 chiusa.
- Contesto: gas.py:3964 — notifica della firma in ruolo user con l'UUID — è il punto d'ingresso del falso positivo.

**Rischi esclusi (non verificati)**

- Le altre suite della CI: non le ho girate, stanno girando dal chiamante.
- Il comportamento reale sul Mac con `claude -p`: non riproducibile qui, Opus è finto nei test.
- La frequenza esatta dei fallimenti casuali in CI: è una stima (circa 8% per ognuna delle 4 firme dei T78), non una misura su GitHub.

**Note per il chiamante**

- Non ho creato `.claude/.review_ok`. Ne esiste uno vecchio (03:05, hash 6b1a601c…) che non corrisponde al diff attuale (60648b1d…), quindi non apre il cancello.
- Memoria aggiornata: riga #841-CRM e 2 lezioni in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nell'albero di lavoro. Come hai chiesto non ho committato (né il commit della memoria né altro) e non ho toccato l'indice: lo sha256 del diff staged è ancora 60648b1d.
- Le mie sonde sono in /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/: mut.py (mutanti), uuid_probe.py (misura sugli UUID), run_uuid_cifre.py (suite con UUID a 7 cifre), fix_probe.py (rimedio).

---

Review #842-CRM, commit 0afc1a79 (verdetto integrale incollato):

## VERDETTO: APPROVATO CON RISERVE

Review #842-CRM: secondo giro della #841-CRM, che era stata BOCCIATA. Diff staged: 6 file, +153/−11, sopra c8d4f977, sha256 cd86b081. Prima della review ho letto CLAUDE.md §5/§8/§10, la voce CRM di reports/stato_progetto.md e la memoria (#839, #840 e #841, con le lezioni). Ho controllato che i file di lavoro siano identici all'indice.

**Cosa ho rieseguito io**
- Suite del kernel: 1206 PASS, 0 FAIL.
- Suite del kernel con i tuoi UUID forzati ad avere 7 cifre di fila (run_uuid_cifre.py): 1206 PASS, 0 FAIL.
- Suite del CRM: 150 passed.
- Sonda sull'espressione regolare con 100.000 uuid4, 20.000 UUID di sole cifre e 20.000 sha256: 0 falsi in tutti e tre i campioni.
- Prestazioni: 1,6 MB di testo e 4 testi costruiti per farla rallentare restano sotto 0,15 s, nessun rallentamento esponenziale.

**Elementi del diff esaminati**
- `gas.py:156` — il nuovo `_RE_TELEFONO` (confini di parola, esclusione di date e migliaia, rami italiano, «+» e «(0…)»). Rischio: il ritorno di R-841-1 (falsi telefoni dentro gli UUID delle firme e negli hash). Gli UUID non possono più scattare per costruzione: un pezzo di cifre dentro l'UUID è sempre preceduto o seguito da lettere o trattini. Esito: **ok**, R-841-1 chiusa nel codice.
- `tests/test_unit_kernel.py:13795` — T118e2, i casi negativi che dovrebbero proteggere R-841-1. Rischio: un test che non arriva al ramo che dovrebbe proteggere. Nell'UUID del test le 7 cifre sono «2625969» (iniziano con 2), nell'hash sono «1234567» (iniziano con 1). Il ramo `[03]` li scarta comunque, quindi non mettono alla prova i confini. Esito: **riserva R-842-1 MEDIA**. Mutanti che sopravvivono a T118e2 e al resto dei test:
  - senza il controllo di fine parola: ritornano 358 UUID su 50.000 (0,7%) e 35 sha256 su 5.000;
  - controllo di fine parola senza il trattino: 226 UUID su 50.000;
  - controllo di inizio parola senza il trattino, o ridotto a sole lettere e cifre: 30 UUID su 50.000;
  - senza l'esclusione delle migliaia: «1.000.000» e «3.500.000» non arrivano mai al ramo, per cui la nuova regola non viene mai provata;
  - senza il ramo «+»: «+39» passa comunque dal ramo che inizia con 3;
  - con la soglia abbassata da 7 a 6 cifre.

  Rimedio da pochi minuti: aggiungere come casi negativi gli UUID `34581227-a1dd-4359-908c-8e4b2c260fea` e `7ef47c36-9a54-4687-9715-069192094992`, poi «30.000.000» e «350000 euro»; come caso positivo «+44 20 7946 0958».
- `gas.py:164` — `_RE_RICHIESTA_CRM` con `client[ei]\w*` e `vers(?:at[oaie]|ament[oi]|are|erà|eranno)`. Rischio: i falsi positivi di R-841-2. I mutanti `client\w*`, `vers\w*`, «senza bonific», `preliev`, `deposit[oi]` e «senza ament» sono tutti presi. Esito: **ok**, R-841-2 chiusa.
- `gas.py:381` (contesto, il chiamante `_finestra_ha_dati_lead`) e `gas.py:2010` (contesto, il riepilogo della compressione in ruolo user). Rischio: testi del kernel in ruolo user. Righe di output di free, df, ls -l e ps contano come «telefono». Però il riepilogo sta all'indice 0 e la finestra è di 10 messaggi, quindi ci entra solo con lunghe catene di strumenti. Esito: **riserva R-842-3 BASSA**, sotto.
- `modules/telegram/bot.py:489` — il taglio del promemoria a 1500 caratteri senza spezzare «<U+…>». Rischio: messaggio oltre il limite di Telegram. Caso peggiore misurato: 3360 unità UTF-16 su 4096. I mutanti «niente taglio», «niente confine» e «senza …» sono presi. Esito: **ok**, R-841-3 chiusa. Il mutante «taglio a 3000» sopravvive perché il test usa un carattere da 1 unità; con le emoji arriverebbe a 6360 (cosmetica).
- `modules/crm/agente.py:151` — nome e ricerca divisi su apostrofi e trattini. Entrambi i mutanti (divisione solo a spazi) fanno fallire `test_agente_riserve_839`. Esito: **ok**.
- `gas.py:6031` — «CRM: passo a Claude Opus.» compare solo se l'output contiene `_CRM_SOLO_OPUS`. Esito: **ok**. Resta la cosmetica della #841: compare anche quando il turno poi si ferma.
- `reports/crm/guida.md:96` — la guida dice «anche con spazi, punti, trattini o barre». È vero solo in parte (R-842-2, sotto).

**Riserve (da tracciare in stato_progetto.md)**
- **R-842-1 MEDIA** — il test di regressione di R-841-1 non protegge la correzione (dettaglio sopra). Consiglio di chiuderla prima del merge.
- **R-842-2 BASSA** — telefoni non più riconosciuti, e né la guida né un test lo dicono. Sono messaggi che vanno al modello normale invece che solo a Opus:
  - «333.123.4567»: preso per un numero con le migliaia;
  - «02 12 34 56 78» e «06 12 34 5678»: presi per una data;
  - «tel.3331234567», «cell.333 1234567» e «Anna,3331234567»: punto o virgola attaccati al numero;
  - doppio spazio, «(333) 1234567», «+1 (555) 123-4567».
- **R-842-3 BASSA** — falsi positivi non dichiarati: numeri di 7-12 cifre che iniziano con 0 o 3. Esempi: «PID 3012345», «3000000 visualizzazioni», le coordinate «38.1156879», la memoria (`free`) di un VPS da 4 GB in KiB, il `df -k`, gli hash corti di sole cifre (0,4-0,7% di quelli da 7-8 caratteri). Col forte spento questi turni si fermano.

**Cosmetiche**: «a capo che restano» nel promemoria non protetto da un test (il mutante `a_capo=False` sopravvive); il taglio duplica `tronca_visibile` (bastava un parametro `a_capo`); `\b` iniziale non protetto (c'era già prima).

**Rischi esclusi (non verificati)**
- Comportamento reale su Telegram e voce, sul Mac o sul VPS: non riproducibile qui.
- Testi user da compiti notturni o pianificati con formati di numero diversi da quelli provati.
- I falsi positivi del ramo delle parole dentro il riepilogo della compressione: c'erano già dalla #840.
- mypy: non ci sono errori nuovi su agente.py e bot.py. Gli errori su gas.py:6020-6036 sono il solito `tc.function` sull'union e c'erano già.

**Note**
- Esiste un `.claude/.review_ok` residuo, delle 03:05, con hash 6b1a601c diverso da quello del diff attuale (cd86b081): non apre il gate. Non l'ho creato né toccato.
- Memoria aggiornata con la riga #842-CRM e una lezione in `/home/user/Gas/.claude/agents/memoria_revisore.md`. Commit della memoria NON eseguito, come hai chiesto: nel file restano non committate anche le righe #839, #840 e #841.
- Sonde in `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/sonda/` (`mut_re.py`, `mut_uuid.py`, `mut_bot.py`, `probe_re.py`, `riep.py`).

---

Review #843-CRM, commit 070e7ad3 (verdetto integrale incollato):

## VERDETTO: APPROVATO CON RISERVE

Review #843-CRM. Diff staged: 3 file, +14/−2, sopra 0afc1a79. sha256 di `git diff --cached`: d00006ad…; hash del gate (`scripts/hash_diff_staged.sh`): a7a287a0…. Prima ho letto CLAUDE.md §5, la riga 9 di stato_progetto e le voci #841-CRM e #842-CRM della mia memoria.

**Elementi del diff esaminati**
- `tests/test_unit_kernel.py:13799` — nuovi casi negativi di T118e2: due UUID con le cifre attaccate al trattino («34581227-…» e «…-069192094992»), «30.000.000» e «350000». Rischio esaminato: R-842-1, cioè confini, migliaia e soglia non provati. Ho rifatto io 30 mutanti di `_RE_TELEFONO` sulle liste del test, con la funzione vera `_finestra_ha_dati_lead`. Uccisi: fine senza lookahead, fine senza trattino, fine senza \w, inizio senza lookbehind, inizio senza trattino, inizio solo \w, inizio senza \w, senza date, senza migliaia, senza ramo «+», senza ramo parentesi, soglia 6, [03] cambiato in [0-9], [3] o [0], e i quattro separatori. Tutti i mutanti che ti avevo elencato in #842 muoiono. Esito: ok, R-842-1 chiusa.
- `tests/test_unit_kernel.py:13795` — «+44 20 7946 0958» tra i positivi. Rischio esaminato: il ramo «+» restava vivo perché «+39 333…» era già preso dal ramo [03]. Il mutante senza ramo «+» ora è ucciso. Esito: ok.
- `tests/test_unit_kernel.py:13894` — T118f2 controlla che gli a capo del promemoria restino. Ho provato il mutante `rendi_visibili(..., a_capo=False)` in `modules/telegram/bot.py:484`: la suite dà 1205 PASS e 1 FAIL (T118f2). Esito: ok, nota cosmetica di #841/#842 chiusa.
- `gas.py:156` — commento con i limiti dichiarati R-842-2/3, solo commento (il codice della regex non cambia). Rischio esaminato: testo falso rispetto a quello che la regex fa davvero. Ho provato 9 casi e sono tutti come scritto: non presi «333.123.4567», «02 12 34 56 78», «tel.3331234567», «tel,3331234567», «(333) 1234567»; presi «3000000 visualizzazioni», «PID 3141592», una riga di free con «3012345». Esito: ok. La stessa frase sta nella guida (`reports/crm/guida.md:96`), coerente col commento.
- `gas.py:163` (contesto, regex non toccata dal diff) — l'esclusione delle migliaia è un lookahead che inizia con `[0-9]`, quindi non vale per il ramo «+». Esito: riserva R-843-1, sotto.

**Riserve (da tracciare in stato_progetto.md)**
- **R-843-1 BASSA** (c'era già, non la introduce questo diff; non l'avevo vista in #842). Un «+» seguito da un numero con le migliaia viene preso come telefono: «+1.500.000 euro di fatturato», «crescita +3.000.000», «+30.000.000 di visualizzazioni», e anche «+03.11.2026». La guida invece dice «non contano i numeri con le migliaia», e questi casi mancano dall'elenco dei falsi positivi appena aggiunto. Effetto: una chiamata a Opus in più, oppure il turno fermo col forte spento. Mai un dato a un modello minore. Due strade:
  - dichiararlo nella guida e nel commento;
  - usare `(?!\+?[0-9]{1,3}(?:[.,][0-9]{3})+(?![0-9]))`. L'ho provato: «+1.500.000» e «+30.000.000» non sono più presi, «+39 333 123 4567», «+44 20 7946 0958» e «+393331234567» sì. Costo: «+39.333.123.4567» non viene più preso, la stessa classe già dichiarata in R-842-2.

**Cosmetiche (mutanti ancora vivi, fuori da quanto chiedeva R-842-1)**
- Soglia 8: manca un telefono positivo di 7 cifre, quindi la soglia è provata solo dal basso.
- Inizio senza punto, senza virgola o senza barra: nessun «0.3333333», «1,0333333» o «/proc/3123456» tra i negativi.
- Restano vivi anche: fine senza barra, migliaia solo col punto, soglie del ramo «+», spazio obbligatorio dopo la parentesi.

**Altri controlli**
- Suite del kernel su una copia dell'indice: 1206 PASS, 0 FAIL.
- `git diff --cached --check` pulito.
- Wall of Shame: niente slicing della history, niente output simulato di strumenti (il test chiama `componi_promemoria`, una funzione pura).
- Guardrail (10 iterazioni, `_get_window`, limiti di output) non toccati.

**Rischio escluso esplicitamente**
- Non ho rieseguito le suite pytest della CI (3512 secondo te). Il diff in gas.py è solo un commento, e nessun test o script legge `reports/crm/guida.md` (unico riferimento trovato: `netrc_guida.md`, che non c'entra).
- Il comportamento reale su Telegram, sul VPS e con Opus vero non è verificato: non si riproduce in dev.

**Note per te**
- In `.claude/.review_ok` c'è un marcatore delle 03:48 (165aafb4…) che non ho scritto io. È del diff precedente e non coincide con quello attuale (a7a287a0…), quindi non apre il gate. Non ho creato marcatori.
- Memoria aggiornata in `/home/user/Gas/.claude/agents/memoria_revisore.md`: la riga contatore #843-CRM e una lezione (un'esclusione messa in testa a un'alternanza viene saltata dai rami con un prefisso diverso). Non l'ho committata, come hai chiesto: nel file restano non committate anche le voci #839-#842.
- Script dei mutanti: `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/tools/mutanti.py`.

## §5 DELTA TEST DEL MOTORE

- `python tests/test_unit_kernel.py`: 1191 PASS → 1206 PASS, 0 FAIL. Nuovi T118a, T118b, T118c, T118c2, T118d, T118e, T118e2, T118f, T118f2, T118g. Adattati alla regola nuova T80 (testo «per il cliente Rossi» → «per Rossi») e T116h («ricordami» → «poi sistemo»); il revisore (#840-CRM) li giudica coerenti.

```
=== RIEPILOGO: 1206 PASS, 0 FAIL ===
```

- Con gli UUID delle firme forzati ad avere 7 cifre di fila (script del revisore `run_uuid_cifre.py`): 1206 PASS, 0 FAIL.
- `pytest tests/test_unit_crm.py`: 139 → 150 passed.
- Altre suite pytest della CI sull'albero di 0afc1a79: 3512 passed. 070e7ad3 cambia solo un commento in `gas.py`, test del kernel e guida.

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST (check-runs per SHA).
- Mappatura commit→run:
  - `f7a4c12c`: nessuna run su questo SHA (pushato insieme ad a7f74ff8).
  - `a7f74ff8`: unit-suite success; handoff-check failure (l'handoff era ancora quello della sessione prima: si chiude con questo commit di fine-task).
  - `c8d4f977`: unit-suite success; handoff-check failure (stesso motivo).
  - `0afc1a79`: unit-suite in corso alla scrittura dell'handoff; handoff-check failure (stesso motivo).
  - `070e7ad3`: unit-suite in corso alla scrittura dell'handoff; handoff-check failure (stesso motivo); verifica-bot non partito (l'etichetta «verifica» si mette dopo questo commit di fine-task).
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-840-2 MEDIA, decide l'operatore**: falsi allarmi del filtro «solo Opus» (§0 punto 2).
- **R-842-2 BASSA** (dichiarata in guida e commento): formati di telefono non riconosciuti («333.123.4567», «02 12 34 56 78», «tel.3331234567», «(333) 1234567»).
- **R-842-3 BASSA** (dichiarata): numeri di 7-12 cifre che iniziano con 0 o 3 presi per telefoni (PID, «3000000 visualizzazioni», righe di free/df).
- **R-843-1 BASSA** (non dichiarata nella guida): «+» seguito da un numero con le migliaia («+1.500.000») preso per telefono; effetto una chiamata a Opus in più, mai un dato a un modello minore.
- COSMETICHE dei verdetti #842/#843: mutanti vivi sui bordi del filtro dei telefoni, «CRM: passo a Claude Opus.» anche quando il turno poi si ferma, il taglio del promemoria duplica `tronca_visibile`, `.gas_memory_crm.db` vuoto creato dal bot dove il CRM non c'è.
- Non verificato: Telegram, voce e `claude -p` veri (solo client finti).
- Dal CRM: R-836-1 COSMETICA.
- Ereditate dalla chat Voce (in `reports/stato_progetto.md`): R-813M1-1 BASSA, note basse del bot #390 (V-1/V-2/V-3), R-810M1-2 BASSA attenuata, note basse #382 V-1/V-2 e #383 V-2/V-3, punteggi della voce da lontano non verificati.
