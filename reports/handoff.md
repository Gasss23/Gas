# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-17 — CRM clienti: fetta 1 (prima bozza: servizi, registro movimenti, motore delle opportunità, dashboard in tempo reale) e fetta 2 (risposte dell'operatore: follow-up mensile, selezione dei clienti, invii a scaglioni, testi riscritti da Opus, clienti del CRM solo al cervello forte)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #381 (https://github.com/Gasss23/Gas/pull/381), dopo il nuovo giro di bot e verifica esterna. Il merge lo decide l'operatore: restano riserve BASSE aperte, e il check verifica-bot è neutral perché la PR tocca la CI. Oggi è BLOCCATO dal check required `unit-suite`, rosso per 7 test del sandbox del browser che falliscono anche su altri rami (vedi §6). Prima serve una fetta separata su quel problema dei runner.
2. Le 4 domande aperte in `reports/crm/domande.md`:
   - come guadagniamo su ogni servizio, e il capitale minimo;
   - WhatsApp Business: app o API;
   - Opus anche per le risposte di Gas in chat sui clienti (`GAS_MODEL_CLAUDE_FORTE`);
   - collegare le chat tra loro.
3. Prima dei dati veri:
   - consenso dei clienti raccolto davvero;
   - verifica Consob con un consulente;
   - decisione GDPR: anonimizzazione su richiesta (R-803-9), estesa alle copie di sicurezza (R-808-6).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — CRM clienti (modulo, motore, dashboard, test, CI)**: FATTA.
  - Commit 99d82f3f; review #803-CRM BOCCIATO → #804-CRM APPROVATO CON RISERVE.
- **Fetta 1b — gate IP**: FATTA. Il primo `fine_task_finale.sh` si era fermato sugli indirizzi d'esempio di `tests/test_unit_crm.py`.
  - Correzione: marcatore `gasmerge-ip-ok` sulla riga.
  - Commit f1c109a7; review #805-CRM APPROVATO.
- **Fetta 1c — finding del bot e della verifica esterna sulla PR #381**: FATTA.
  - Commit c9daf955, review #806-CRM APPROVATO CON RISERVE.
  - Riserve R-806-1/2/3 chiuse nel commit 72dcc9d2, review #807-CRM APPROVATO.
- **Fetta 2 — risposte dell'operatore del 17 novembre** (`reports/crm/decisioni.md`): FATTA. Commit aa4bb422; review #808-CRM BOCCIATO → #809-CRM APPROVATO CON RISERVE.
  - Cosa fa:
    - file dedicato `.gas_memory_crm.db` con copie di sicurezza;
    - follow-up mensile spegnibile per cliente; anzianità minima; niente proposte nel mese in perdita; servizi da consigliare;
    - selezione manuale con testi neutri;
    - invii a scaglioni;
    - riscrittura SOLO con Claude Opus, nel conto e nel tetto del forte;
    - i clienti del CRM entrano nel filtro della regola dei modelli (R-803-4 chiusa, `gas.py`).
  - Il primo giro (#808) aveva trovato il filtro lento con molti clienti (R-808-1 ALTA). Ora è una regex unica in cache.
  - Chiuse anche R-808-2/3/4/7 e le riserve BASSE di bot e verifica esterna #381, R-804-1 e R-804-3.
- **Invio automatico WhatsApp**: DEFERITA. Decisione dell'operatore: «da sole, ma all'inizio col mio controllo». Servono l'API WhatsApp Business e i modelli approvati da Meta.
- **Strumento CRM per il modello di Gas** (sola lettura, solo cervello forte): DEFERITA, prossima fetta (`reports/crm/guida.md` §7).
- **Integrazioni (broker, risposte WhatsApp automatiche)**: DEFERITA (`reports/crm/guida.md` §7).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   15 ++++
 .github/workflows/ci.yml           |    8 ++
 .gitignore                         |    5 ++
 gas.py                             |  264 ++++++++++++++++++++++++++++++++++++++++++++++++++--------------
 modules/crm/__init__.py            |   18 +++++
 modules/crm/__main__.py            |  380 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/analisi.py             |  391 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/demo.py                |  135 +++++++++++++++++++++++++++++++++
 modules/crm/messaggi.py            |  152 +++++++++++++++++++++++++++++++++++++
 modules/crm/motore.py              |  525 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/scrittore.py           |  224 ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/server.py              |  876 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/store.py               | 1333 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/web/app.css            |  330 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/web/app.js             |  902 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/web/favicon.svg        |    1 +
 modules/crm/web/index.html         |   17 +++++
 reports/crm/decisioni.md           |   24 ++++++
 reports/crm/domande.md             |    8 ++
 reports/crm/guida.md               |  120 +++++++++++++++++++++++++++++
 reports/diff_sessione.md           |   32 ++++++--
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |    1 +
 reports/stato_progetto.md          |    6 +-
 reports/ultimo_report.md           |   43 ++++++++---
 tests/test_unit_crm.py             | 1486 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_kernel.py          |  154 +++++++++++++++++++++++++++++++++++++
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Gli altri conteggi sono presi con i report già in stage. `reports/crm.md`, creato e poi spostato in `reports/crm/guida.md` nella stessa sessione, non compare nel diff rispetto a BASE.

## §3 GIT LOG --ONELINE (sessione)

```
aa4bb422 feat(crm): fetta 2 — follow-up mensile, selezione clienti, invii a scaglioni, testi riscritti da Opus, clienti del CRM solo al cervello forte
ec2383cd chore(revisore): memoria review #809 — APPROVATO CON RISERVE
2bfbb803 chore(revisore): memoria review #808 — BOCCIATO
48c0f114 docs(fine-task): handoff §6 — handoff-check di 99d82f3f era rosso (V-1 verifica esterna #381, 2° giro), CI e bot di 2ae4b7a7 in corso
2ae4b7a7 docs(fine-task): CRM — finding di bot e verifica esterna #381 chiusi (review #806/#807), CI rossa ambientale documentata
72dcc9d2 fix(crm): controlli e scritture in una sola transazione (BEGIN IMMEDIATE), data di apertura anticipabile, errore chiaro sul testo lungo — review #807 APPROVATO
83633433 chore(revisore): memoria review #807 — APPROVATO
c9daf955 fix(crm): proposta scartata non ricreata, movimenti incoerenti rifiutati, riga STOP sui testi corretti, STOP ricontrollato all'invio — verifica esterna e bot #381, review #806 APPROVATO CON RISERVE
8fdae653 chore(revisore): memoria review #806 — APPROVATO CON RISERVE
772f993c docs(fine-task): handoff — marcatore gasmerge-ip-ok sulle righe d'esempio del verdetto #805
939a2a12 docs(fine-task): handoff con review #805 e gate IP
f1c109a7 test(crm): marcatore gasmerge-ip-ok sugli indirizzi d'esempio del test di bind — review #805 APPROVATO
08b3387b chore(revisore): memoria review #805 — APPROVATO
0286192c docs(fine-task): CRM clienti, prima bozza — report, handoff (review #803/#804), guida reports/crm.md, roadmap R11
99d82f3f feat(crm): CRM clienti, prima bozza — servizi, registro movimenti immutabile in centesimi, motore delle opportunità, dashboard in tempo reale — review #803 BOCCIATO → #804 APPROVATO CON RISERVE
ae5197d0 chore(revisore): memoria review #804 — APPROVATO CON RISERVE
15368710 chore(revisore): memoria review #803 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore 99d82f3f: due giri sullo stesso diff staged; commit motore f1c109a7: terzo giro; commit motore c9daf955: quarto giro; commit motore 72dcc9d2: quinto giro. Verdetti incollati per intero. NB: le citazioni `path:riga` della #803-CRM si riferiscono alla versione staged del primo giro (poi corretta); quelle della #804-CRM al codice committato.

### Review #803-CRM (1° giro)

## VERDETTO: BOCCIATO

Review #803-CRM sul diff staged di claude/nifty-galileo-3k7kbm (15 file, +5052 righe).

**Letture obbligatorie fatte:** CLAUDE.md (sezioni 1, 5, 6, 8, 9 e 10), reports/stato_progetto.md (stato del motore e regole vive), memoria del revisore (lezioni su SQLite e trigger, cifre Unicode, variabili d'ambiente lette con `int()` senza try, server locali).

**Rieseguito da me:** `pytest tests/test_unit_crm.py` dà 80 passed; mypy è pulito.

**Cosa il diff non tocca:** kernel, brains/, memoria e cancello. Nessun antipattern del Wall of Shame: niente slicing della history, niente simulazione di tool (il CRM non usa modelli).

**Perché è bloccato:** il percorso con dati veri (non demo) non è mai stato provato. Ha un difetto, riprodotto, che scrive di continuo nel file della memoria del kernel (R-803-1). In più ci sono due difetti MEDIA, anch'essi riprodotti, da chiudere nello stesso giro perché costano poco (R-803-2 e R-803-3).

### Finding

1. **R-803-1 — ALTA, bloccante — la dashboard con dati veri entra in un ciclo continuo.**
   - **Il meccanismo:** `modules/crm/server.py:210` crea un nuovo `MemoryStore()` a ogni GET /api/stato, dentro `lead_pronti()`. L'avvio della memoria rifà il rebuild dell'indice di ricerca (FTS) del diario e lo salva (`modules/memory/store.py:639`): è una SCRITTURA, e cambia `PRAGMA data_version` (misurato: da 1 a 2 aprendo `MemoryStore()` su un file già pronto).
   - **Il giro:** il guardiano se ne accorge (`modules/crm/server.py:265`) e manda «cambio» via SSE. Dopo 250 ms app.js rilegge /api/stato (`modules/crm/web/app.js:171`), che apre un altro `MemoryStore()` e scrive di nuovo.
   - **La misura:** un client che si comporta come app.js, senza nessuna modifica dell'operatore, riceve 10 eventi «cambio» in 10 s in modalità reale e 0 in demo. In demo `lead_pronti` esce subito, per questo la prova nel browser non l'ha visto.
   - **Gli effetti:** finché una scheda resta aperta (h24 sul VPS), il CRM ricostruisce l'indice FTS di TUTTO il diario del kernel circa una volta al secondo. Ogni volta prende il lock di scrittura sul file della memoria, in concorrenza col kernel. In più la scansione prevista «2 s dopo un cambio» (`modules/crm/server.py:268`) viene rimandata all'infinito. Lo stesso costo c'è in `converti_lead` (`modules/crm/server.py:228`), ma solo a click.
   - **Rimedio:**
     - un solo MemoryStore per processo, creato al primo uso e tenuto in `Stato`, oppure una SELECT di sola lettura su `contatti`;
     - un test non demo che conta gli eventi SSE senza modifiche: deve dare 0 e deve fallire sul codice attuale.

2. **R-803-2 — MEDIA — corpo della richiesta non letto sulle connessioni keep-alive (HTTP/1.1).**
   - **Il difetto:** tre ritorni anticipati di do_POST rispondono senza leggere il corpo e senza chiudere la connessione:
     - `modules/crm/server.py:550` (403);
     - `modules/crm/server.py:569` (401/429);
     - `modules/crm/server.py:384` (413).

     `_errore` passa da `_json`, non da `send_error`, quindi manca `Connection: close`. Il corpo resta sul socket e viene letto come la richiesta successiva.
   - **Riprodotto (a), attacco da pagina estranea:** ho imitato una POST da form cross-site (Content-Type text/plain, Origin estranea, niente X-Gas-CRM), con un corpo che contiene una POST /api/login completa. La 403 esterna parte, poi il login nascosto VIENE ESEGUITO. Dopo 11 giri il log dice «CRM AUTH BLOCCO ip=127.0.0.1 per 900 s». Quindi una pagina aperta dall'operatore può bloccargli il login per 15 minuti, rinnovabili. Le sessioni già aperte restano valide e il token non si indovina, quindi nessun accesso ai dati.
   - **Riprodotto (b), cliente legittimo:** una POST con sessione scaduta riceve 401, e la richiesta seguente sulla stessa connessione riceve 400 in HTML. Effetto: il primo login dopo la scadenza può fallire.
   - **Rimedio:** `self.close_connection = True` in ogni ritorno anticipato di do_POST (oppure scolare il corpo fino a CORPO_MAX), più un test con due richieste sulla stessa connessione.
   - **Nota collegata (BASSA):** con l'ascolto solo su loopback, il blocco «per IP» vale di fatto per tutti.

3. **R-803-3 — MEDIA — l'import CSV non è «tutto o niente».**
   - **Il difetto:** `modules/crm/__main__.py:213` pre-valida solo telefono, servizio e importo. `tipo` e `data` (compreso il divieto di date future) li controlla solo `registra_movimento`, dentro il ciclo di scrittura (`modules/crm/__main__.py:228`).
   - **Riprodotto:** CSV con riga 1 buona, riga 2 col tipo `deposit` e riga 3 con data 2099. Il comando stampa «ERRORE: tipo di movimento non valido» ed esce con 1, ma la riga 1 è GIÀ nel registro immutabile e il messaggio non lo dice. Corretto il file e rilanciato, il deposito risulta registrato due volte (2 movimenti).
   - **Perché pesa:** il registro non ammette UPDATE né DELETE, quindi l'unica correzione sono storni a mano. La docstring promette il contrario.
   - **Rimedio:**
     - pre-validare con gli stessi validatori dello store: tipo in TIPI_MOVIMENTO, `valida_data`, data non futura, nota;
     - scrivere tutte le righe in UNA transazione, con un metodo a lotti nello store;
     - un test con una riga cattiva in mezzo che lascia il registro vuoto.

4. **R-803-4 — MEDIA, non bloccante qui — regola dei modelli (da tracciare in stato_progetto prima di caricare dati veri).**
   - **Il buco:** il rilevatore che manda al forte i turni con dati di clienti prende i nomi solo dalla rubrica lead (`gas.py:174`, usato a `gas.py:4397`). I clienti che esistono solo in `crm_clienti` non ci sono.
   - **Esempio:** se l'operatore scrive a Gas «Marco Bianchi ha fatto +2.000 €, cosa gli propongo?», il turno può andare ai gratuiti.
   - **Il diff in sé:** non manda nulla ai modelli (motore e messaggi sono deterministici, bene), ma introduce l'anagrafica dei clienti senza collegarla al rilevatore.

5. **R-803-5 — BASSA — doppio cliente dallo stesso lead.**
   - **Il difetto:** `modules/crm/server.py:232` controlla «già cliente» e poi inserisce, senza un vincolo nel DB.
   - **Riprodotto:** 4 conversioni concorrenti dello stesso lead senza telefono creano 2 clienti.
   - **Rimedio:** indice unico parziale su `crm_clienti(contatto_id) WHERE contatto_id IS NOT NULL`.

6. **R-803-6 — BASSA — cifre Unicode nel telefono.**
   - **Il difetto:** `modules/crm/store.py:368` e `modules/crm/messaggi.py:113` usano `isdigit()`. «³³³1234567» diventa `+39³³³1234567`, finisce nel link wa.me e sfugge all'indice unico sul telefono. È la stessa famiglia di V-3 #193.
   - **Rimedio:** controllo con `[0-9]` oppure con `isascii()`.

7. **R-803-7 — BASSA — importo moltiplicato per mille.**
   - **Il difetto:** `modules/crm/store.py:288` accetta un primo gruppo che vale «0»: «0.500» diventa 500,00 €, «0.050» diventa 50,00 €, «000.001» diventa 1,00 €.
   - **Rimedio:** regex `[1-9]\d{0,2}(\.\d{3})+` e rifiuto della forma ambigua.

8. **R-803-8 — BASSA — §9 e variabili d'ambiente.**
   - `modules/crm/__main__.py:245` fa `int(GAS_CRM_PORT)` mentre costruisce il parser: un valore non numerico fa crashare OGNI comando con traceback. Lo stesso vale per `GAS_CRM_SCAN_MINUTI` a `modules/crm/__main__.py:88` (lezione #96).
   - `cmd_import` non intercetta `csv.Error`, `OSError` né `UnicodeDecodeError`.
   - `do_GET` (`modules/crm/server.py:399`) non ha il paracadute generico di do_POST: un'eccezione imprevista finisce su stderr tramite socketserver, non in gas_debug.log.

9. **R-803-9 — BASSA, decide l'operatore — dati personali e cancellazione.**
   - **Il problema:** `crm_eventi` è immutabile (`modules/crm/store.py:215`) e la descrizione contiene il nome del cliente in testo libero (`modules/crm/store.py:609`). Una richiesta di cancellazione (GDPR) non si può onorare senza togliere i trigger.
   - **Quando decidere:** prima dei dati veri; stato_progetto rimanda il GDPR alla FASE 4.
   - **Collegato:** `converti_lead` cambia lo stato del lead in `contatti` (`modules/crm/server.py:247`) senza scrivere una riga nel diario di Gas, mentre CLAUDE.md §6 vuole le transizioni del funnel tracciate.

10. **R-803-10 — BASSA — fin dove arriva la protezione del file della memoria.**
    - **Cosa va bene:** mettere le tabelle nel file della memoria è giusto anche per la sicurezza. `.gas_memory*` è illeggibile dagli strumenti di Gas (`modules/gate/gate.py:344`), quindi i dati dei clienti non arrivano ai modelli leggendo file.
    - **Il limite:** `GAS_CRM_DB` (`modules/crm/__main__.py:41`) può puntare a un file qualsiasi, che perde quella protezione. Va dichiarato nella guida, oppure limitato ai nomi `.gas_memory*`.
    - **Il rovescio, accettabile ma da dichiarare:** il server web tiene una connessione in scrittura al file che contiene anche le firme (`approvals`). Non ho trovato SQL costruita con dati dell'utente: solo nomi di colonna presi da liste fisse e costanti.

11. **R-803-11 — COSMETICA.**
    - `CRMStore.data_version()` (`modules/crm/store.py:492`) non è usato. Aprendo ogni volta una connessione nuova restituisce sempre lo stesso numero (misurato: 1, 1, 1), mentre la docstring promette altro.
    - `modules/crm/server.py:455` prepara il link wa.me per tutte le proposte aperte in /api/stato, anche per clienti che hanno appena detto STOP, fino alla scansione successiva. app.js non lo usa: meglio toglierlo, così l'unico link nasce da «invia», dopo il controllo.
    - `modules/crm/__init__.py:12` cita un modulo `whatsapp` che non esiste.
    - Lo stream SSE non si chiude al logout (manda solo numeri di versione).

### Elementi del diff esaminati e trovati corretti

- `modules/crm/store.py:165` — trigger BEFORE UPDATE/DELETE su `crm_movimenti`, e `modules/crm/store.py:215` su `crm_eventi`. Rischio esaminato: aggirarli con INSERT OR REPLACE, che cancella righe senza far scattare i trigger. Cercato in tutto `modules/crm`: nessun REPLACE, ON CONFLICT o DROP; c'è un test che lo verifica davvero — ok.
- `modules/crm/store.py:162` e `modules/crm/store.py:792` — un movimento si storna una volta sola (indice unico) e uno storno non si storna. `modules/crm/analisi.py:106` toglie la coppia dai conti — ok.
- `modules/crm/store.py:201` e `modules/crm/motore.py:383` — al massimo una proposta aperta per cliente, garantita dal DB (indice unico parziale); un doppione restituisce None. Le transizioni sono condizionate sullo stato letto (`modules/crm/store.py:890`), quindi due click concorrenti non passano entrambi. Idempotenza e concorrenza del motore — ok.
- `modules/crm/analisi.py:18` — `_div` arrotonda a metà in su ed è simmetrico sui negativi (verificato: 5/2 dà 3, −5/2 dà −3, 150/100 dà 2). `modules/crm/store.py:252`: `parse_importo` non usa float e passa a Decimal solo cifre ASCII già validate. Le stime delle commissioni arrotondano due volte, con errore al massimo di 1 centesimo — ok, salvo R-803-7.
- Difese del server:
  - `modules/crm/server.py:327`: Host ammesso solo «localhost» o un IP letterale (contro il DNS rebinding);
  - `modules/crm/server.py:71`: ascolto solo su loopback;
  - `modules/crm/server.py:86`: confronto del token a tempo costante;
  - cookie HttpOnly e SameSite=Strict, header custom che obbliga al preflight (non c'è do_OPTIONS), controllo dell'Origin.

  Come progetto è ok; il buco è R-803-2, a valle di questi controlli.
- `modules/crm/server.py:698` — STOP, consenso e stato del cliente vengono ricontrollati AL MOMENTO dell'invio, non solo alla scansione. L'invio resta un click dell'operatore su wa.me (principio del 19 ottobre) — ok.
- `modules/crm/server.py:185` — l'avviso Telegram contiene solo numeri, al massimo uno all'ora, con le eccezioni intercettate e loggate — ok (§9 e regola dei modelli).
- `modules/crm/server.py:244` — la conversione da lead a cliente parte con consenso_marketing falso e porta il lead a «chiuso», uno stato valido e tra gli STATI_CHIUSI (Gas smette di inseguirlo) — semantica ok, con le riserve R-803-5 e R-803-9.

### Rischi esplicitamente NON verificati

- Comportamento sul VPS, sul Mac e attraverso tunnel SSH/Tailscale: non riproducibili qui. Il ciclo di R-803-1 è misurato su un DB temporaneo col diario vuoto; il costo reale del rebuild su un diario grande NON è misurato.
- R-803-2 su browser reali: provato con socket grezzi che imitano il corpo di un form text/plain. Non so se Chrome, col blocco delle richieste verso la rete locale (Private Network Access), lo fermerebbe; Firefox e Safari quel blocco non ce l'hanno.
- Aspetti legali dei messaggi promozionali su servizi finanziari (Consob, consenso, insistenza crescente): fuori dalla mia competenza, li valuti l'operatore.
- app.css e la parte di app.js lontana dai punti sensibili (costruzione del DOM, link, token nel frammento) non letti riga per riga.

### Note per l'agente

- **Memoria:** riga contatore #803-CRM e 3 lezioni aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md e committate da sole (commit 1536871, «chore(revisore): memoria review #803 — BOCCIATO»). Il diff staged è rimasto intatto (15 file).
- **Marcatore e commit:** come chiesto, non ho creato `.claude/.review_ok` e non ho committato il diff.
- **Script delle prove**, riutilizzabili come base per i test che mancano:
  - /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/loop2.py (ciclo SSE; argomento `demo` per il confronto);
  - /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/smug.py (corpo non letto eseguito come login);
  - /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/dv.py (data_version cambiato da MemoryStore).
- **Dopo le correzioni** di R-803-1, R-803-2 e R-803-3, ognuna con un test che fallisce sul codice attuale, serve un nuovo giro di review.

### Review #804-CRM (2° giro, sul diff corretto)

## VERDETTO: APPROVATO CON RISERVE

Review #804-CRM: secondo giro sul diff staged del CRM (15 file, +5400), dopo il BOCCIATO #803-CRM.

**Come ho controllato i cambiamenti:** ho ritrovato nel repo i blob della versione che avevo revisionato al primo giro (`git fsck --unreachable`) e ho fatto il diff esatto riga per riga.
- Cambiati: store, server, `__main__`, messaggi, `__init__` e i test.
- Identici al primo giro: analisi, motore, demo e la cartella web.

**Cosa ho rieseguito io:**
- `pytest tests/test_unit_crm.py`: 93 passed. mypy pulito.
- Le mie tre riproduzioni del primo giro, sul codice nuovo:
  - ciclo SSE con dati veri: 0 eventi in 10 s (prima 10);
  - login nascosto nel corpo: non viene più eseguito (0 tentativi falliti, nessun blocco);
  - `MemoryStore` aperto una sola volta.
- I 13 test `test_r803_*` contro la versione del primo giro (ricostruita in una cartella temporanea, poi cancellata): 12 falliscono e 1 passa (keep-alive normale, che deve passare in entrambe), come dichiarato. Falliscono per il motivo giusto:
  - R-803-1: `data_version` passa da 1 a 2;
  - R-803-2: compare una 401 in più, prodotta dalla richiesta nascosta.

Il kernel, brains/, la memoria e il cancello restano non toccati. Nessuno slicing della history, nessuna simulazione di tool.

### Finding del primo giro: esito

- **R-803-1 (ALTA): CHIUSA.**
  - `modules/crm/server.py:125` apre UN solo `MemoryStore` all'avvio di `Stato`.
  - `lead_pronti` e `converti_lead` usano quello.
  - Nel percorso GET non resta nessuna scrittura: `fotografia` è solo lettura, `leggi_contatti` legge.
- **R-803-2 (MEDIA): CHIUSA.**
  - `modules/crm/server.py:330` manda `Connection: close` e chiude la connessione quando c'è un corpo non letto (Content-Length diverso da 0, oppure Transfer-Encoding).
  - `_corpo_letto` si azzera a ogni richiesta (`modules/crm/server.py:429`, `modules/crm/server.py:598`).
  - Il test parametrizzato copre 403, 401 e 413 e pretende che `falliti` resti vuoto.
- **R-803-3 (MEDIA): CHIUSA.**
  - `modules/crm/store.py:745` (`valida_movimento`) controlla senza scrivere.
  - `modules/crm/store.py:787` (`registra_movimenti`) prima valida tutte le righe, poi le scrive in una sola `_scrivi`. Un errore dentro la transazione fa rollback grazie al context manager.
  - L'import li usa entrambi (`modules/crm/__main__.py:251`, `modules/crm/__main__.py:260`) e intercetta OSError, UnicodeDecodeError e csv.Error.
- **R-803-5: chiusa.** Indice unico parziale (`modules/crm/store.py:133`); il messaggio di errore è tradotto per l'operatore.
- **R-803-6: chiusa.** Solo cifre ASCII nel telefono (`modules/crm/store.py:379`) e nel link (`modules/crm/messaggi.py:114`).
- **R-803-7: chiusa.** Le migliaia non possono più iniziare con 0 (`modules/crm/store.py:294`).
- **R-803-8: chiusa.** `_env_int` per le variabili numeriche; `do_GET` ha il paracadute che risponde 500 e scrive nel log (`modules/crm/server.py:434`).
- **R-803-11: chiusa.** Lo stream SSE si chiude al logout: il predicato gira col lucchetto della Condition già preso (`modules/crm/server.py:567`).
- **R-803-9: chiusa nella parte tecnica.**
  - Niente nomi nel testo di `crm_eventi` (`modules/crm/store.py:610`).
  - La conversione di un lead lascia una riga nel diario di Gas, senza dati personali (`modules/crm/server.py:260`).
  - La decisione GDPR resta all'operatore.
- **R-803-4 (MEDIA) e R-803-10 (BASSA): restano aperte e tracciate.**
  - R-803-4 è in reports/stato_progetto.md e in reports/crm.md, come condizione da soddisfare prima di caricare dati veri.
  - Per R-803-10 la CLI ora avvisa (`modules/crm/__main__.py:59`).

### Riserve nuove (non bloccanti)

1. **R-804-1 — BASSA — la porta scritta nel `.env` viene ignorata.**
   - `GAS_CRM_PORT` è letta mentre si costruisce il parser (`modules/crm/__main__.py:276`), cioè in `parser().parse_args` (`modules/crm/__main__.py:330`), PRIMA di `_carica_chiavi()` (`modules/crm/__main__.py:331`).
   - Eppure la guida la mette proprio nel `.env` (reports/crm.md, tabella delle impostazioni).
   - Provato: `.env` temporaneo con `GAS_CRM_PORT=9123` e la variabile tolta dall'ambiente → serve usa 8770.
   - Rimedio: in `main()`, caricare il `.env` prima di costruire il parser.
   - Il problema c'era già al primo giro e mi era sfuggito.
2. **R-804-2 — BASSA, da dichiarare — la dashboard reagisce anche alle scritture del kernel.**
   - Il guardiano (`modules/crm/server.py:278`) vede OGNI commit sul file condiviso, comprese le righe del diario che il kernel scrive a ogni tool call (provato: un `append_diario` porta `data_version` da 1 a 2).
   - Effetto, con Gas attivo: ogni tool call fa ricaricare /api/stato a tutte le dashboard aperte e lancia una scansione del motore 2 s dopo (`modules/crm/server.py:281`). Se Gas scrive più spesso di una volta ogni 2 s, quella scansione viene rimandata finché non si calma; resta quella periodica.
   - Non è un ciclo (le letture non scrivono più): è un legame non dichiarato.
   - Rimedio: dichiararlo in reports/crm.md, oppure filtrare i cambi guardando un'impronta delle sole tabelle `crm_*`.
3. **R-804-3 — BASSA — l'import non è idempotente tra due esecuzioni.**
   - Lo stesso CSV valido importato due volte raddoppia i movimenti.
   - Il registro non si corregge se non con uno storno per riga, quindi un estratto mensile caricato due volte gonfia profitti e commissioni.
   - Rimedio: un avviso sui doppioni esatti (posizione, tipo, importo, data, nota), oppure un'opzione esplicita per forzare.
4. **R-804-4 — COSMETICA — corpo chunked trattato come vuoto.**
   - `_leggi_json` (`modules/crm/server.py:415`, `modules/crm/server.py:416`) ignora Transfer-Encoding: un corpo chunked diventa `{}` e viene segnato come letto, quindi la connessione resta aperta col corpo ancora sul socket.
   - Provato: una 401 seguita da una 400.
   - Non sfruttabile: serve X-Gas-CRM, che una pagina estranea non può mettere, e la riga con la lunghezza del chunk non forma una richiesta valida. Però contraddice la regola di R-803-2.
   - Rimedio: rifiutare Transfer-Encoding senza segnare il corpo come letto.
   - Collegato: in do_POST una BrokenPipe in scrittura finisce ancora su stderr (socketserver), non in gas_debug.log.

### Elementi del diff esaminati

- `modules/crm/server.py:125` — un solo `MemoryStore` all'avvio. Rischi esaminati: scritture nel percorso GET, accesso da più thread. Esito ok: connessioni brevi, una per operazione; `data_version` invariato dopo 3 GET (test e mia riproduzione).
- `modules/crm/server.py:317` e `modules/crm/server.py:330` — la connessione si chiude se c'è un corpo non letto. Rischio esaminato: corpo eseguito come richiesta successiva. Ok sui casi 403, 401 e 413 e con Content-Length non valido; riserva R-804-4 sul chunked.
- `modules/crm/store.py:787` — scrittura a lotti tutta o niente. Rischio esaminato: rollback parziale. Ok: validazione completa prima, poi una sola transazione; un ErroreCRM interno annulla tutto.
- `modules/crm/store.py:133` — indice unico su `contatto_id`. Rischio esaminato: un DB vecchio con doppioni farebbe fallire l'avvio del CRM (`available` resta False). Accettabile: fail-closed, e oggi non esiste ancora un DB vero.
- `modules/crm/server.py:567` — chiusura dello stream SSE al logout. Rischio esaminato: deadlock rileggendo le sessioni dentro la Condition. Ok: legge `st.sessioni` senza riprendere il lucchetto, e il logout sveglia la Condition (`modules/crm/server.py:627`).
- `modules/crm/server.py:260` — riga nel diario di Gas alla conversione di un lead. Rischio esaminato: dati personali nel diario immutabile. Ok: solo «#id», tipo `crm_conversione`, fonte «utente» (tra le fonti ammesse); se la scrittura fallisce resta un avviso nel log.
- Test cambiati: le sole due asserzioni tolte (link wa.me in /api/stato) sono sostituite da asserzioni più strette (link assente prima di «invia», link esatto dopo). Nessun test indebolito.

### Rischi esplicitamente NON verificati

- Prova su un `.gas_memory.db` vero con un diario grande, sul Mac o sul VPS: non riproducibile qui. La prova con Playwright dichiarata dal chiamante non l'ho rifatta.
- Suite completa (kernel 1167 PASS; pytest con 33 fallimenti in test_unit_web_browser.py per bwrap assente): dichiarata dal chiamante, non rieseguita. Il diff non tocca quei moduli.
- Blocco delle richieste verso la rete locale nei browser veri e aspetti legali dei messaggi promozionali: come al primo giro, fuori da quanto ho potuto verificare.

### Note per l'agente

- **Memoria:** riga contatore #804-CRM e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md e committate da sole (commit ae5197d0). Il diff staged è rimasto intatto (15 file).
- **Marcatore e commit:** non ho creato `.claude/.review_ok` e non ho committato il diff staged.
- **Script delle prove di questo giro**, utili come base per test:
  - /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/te.py (corpo chunked e scrittura del diario del kernel vista dal guardiano);
  - /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/loop2.py (ciclo SSE; argomento `demo` per il confronto);
  - /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/smug.py (login nascosto nel corpo).
- **Da registrare in reports/stato_progetto.md:** le riserve R-804-1, R-804-2, R-804-3 e R-804-4.

### Review #805-CRM (3° giro, commit f1c109a7: solo il marcatore gasmerge-ip-ok)

Unica aggiunta al testo del verdetto: il marcatore `# gasmerge-ip-ok` in fondo alle due righe con gli indirizzi d'esempio, richiesto dal gate IP su reports/ (stessa prassi dell'handoff della PR #126).

## VERDETTO: APPROVATO

Review #805-CRM, terzo giro: l'unica modifica è il commento `# gasmerge-ip-ok`, è legittima e il gate IP passa.

**Controlli fatti:**
- **Il commento è l'unica modifica.** `git diff --staged --numstat` dà `1 1 tests/test_unit_crm.py`: una riga tolta e una aggiunta. L'hunk aggiunge solo `  # gasmerge-ip-ok` in fondo alla riga, il resto è identico.
- **Il commit 99d82f3f contiene il codice approvato in #804.** I blob di `modules/crm/server.py`, `store.py`, `__main__.py`, `messaggi.py` e `tests/test_unit_crm.py` a HEAD coincidono con quelli revisionati al secondo giro (4aa12e30, 5a407469, 3ef55e4e, 4e4b2de3, ea81e0e4).
- **Il gate IP passa.** Ho simulato il gate sull'albero che nascerebbe dall'indice attuale (`git write-tree`), con la stessa regex e lo stesso filtro di loopback e marcatore dello script: 0 righe residue.
- **La suite resta verde.** `test_bind_solo_locale`: 1 passed. Suite CRM: 93 passed.

**Elementi esaminati:**
- `tests/test_unit_crm.py:584` — aggiunge il marcatore sulla riga del test negativo di `bind_locale`.
  - Rischio esaminato: che il marcatore copra un indirizzo reale (di una macchina o di una rete dell'operatore).
  - Esito: ok. I due indirizzi marcati sono input d'esempio che il test pretende siano RIFIUTATI con ValueError:
    - `0.0.0.0` è l'indirizzo che vuol dire «tutte le interfacce»;  # gasmerge-ip-ok
    - `192.168.1.10` è un generico indirizzo di rete privata.  # gasmerge-ip-ok
  - Il marcatore vale solo per quella riga, che contiene anche `127.0.0.1.nip.io` (un nome che inizia come un loopback, comunque esente).
- `modules/crm/server.py:71` — `bind_locale`, il controllo che il test esercita.
  - Rischio esaminato: che il marcatore servisse a nascondere un indebolimento del controllo.
  - Esito: ok. Il file è invariato rispetto al blob approvato in #804 e il test continua a pretendere il rifiuto.
- `scripts/fine_task_finale.sh:73` — la regex del gate (citazione di contesto, file non toccato).
  - Rischio esaminato: che, dopo questa modifica, restino altri IP non marcati nell'albero.
  - Esito: ok. Gli altri indirizzi del CRM sono tutti 127.0.0.1, quindi esenti come loopback.

**Rischio esplicitamente escluso:** non ho eseguito `scripts/fine_task_finale.sh` per intero, perché fa push e merge e non spetta al revisore. Il gate l'ho simulato su un albero ottenuto con `git write-tree`: lo script lo fa invece sul tree di HEAD dopo il commit, quindi l'esito vero lo darà la sua esecuzione.

**Note:**
- Memoria: riga contatore #805-CRM aggiunta e committata da sola (commit 08b3387b). Il diff staged è intatto (1 file, 1/1).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.
- Le riserve aperte restano quelle di #804: R-804-1, R-804-2, R-804-3, R-804-4, più R-803-4, R-803-9 e R-803-10.

### Review #806-CRM (4° giro, commit c9daf955: finding di bot e verifica esterna #381)

## VERDETTO: APPROVATO CON RISERVE

Review #806-CRM, quarto giro. Un solo verdetto sull'insieme del diff staged (5 file, +150/−8): le correzioni V-1/V-2 della verifica esterna #381 più V-1/V-2 del bot #381.

**Riserva principale (MEDIA):** i nuovi controlli su capitale e STOP non sono atomici. Con due operazioni concorrenti si aggirano: provato, due prelievi in parallelo portano il capitale a −1.000 € e uno STOP scritto nel mezzo non ferma l'invio. Si chiude con una riga (`BEGIN IMMEDIATE` in `_scrivi`), dettagli in R-806-1. Il resto delle correzioni è corretto e i test mordono.

**Verifiche rieseguite da me:**
- **Fail-before:** in una cartella con il codice di HEAD (f1c109a7) e il file di test staged, falliscono 5 test (`test_server_flusso_completo`, i due V-1/V-2 della verifica esterna, i due del bot), 92 passano.
- **Codice staged:** 97 passed. mypy pulito.
- **Demo:** si popola ancora con i vincoli nuovi (26 clienti, 456 movimenti).
- **Perimetro:** kernel, brains/, memoria e cancello non toccati.

### Riserve

**R-806-1 — MEDIA — i controlli «dentro la transazione» non lo sono**
- **Il problema.** Il sqlite3 di Python apre la transazione solo prima della prima INSERT/UPDATE (modalità «legacy», predefinita anche su 3.11 e 3.13). Quindi le SELECT di controllo girano in autocommit: `in_transaction` vale False nel momento del controllo, misurato in entrambi i casi sotto.
- **Prova 1, capitale.** Due prelievi concorrenti da 1.000 € su un capitale di 1.000 € passano entrambi: capitale finale −1.000 €. Ho rallentato `_capitale` di 0,3 s per rendere deterministico l'intreccio.
  - Riguarda `modules/crm/store.py:776`, dove la docstring di `_capitale` (`modules/crm/store.py:791`) dice «dentro la transazione».
  - Stesso buco per lo storno di un deposito (`modules/crm/store.py:853`).
- **Prova 2, STOP.** Ho usato una connessione con factory che scrive `opt_out = 1` da un'altra connessione subito prima dell'UPDATE della proposta. La scrittura passa senza attendere nessun lock e la proposta diventa «inviata», col link wa.me, per un cliente che ha appena chiesto STOP. Riguarda `modules/crm/store.py:939` e il controllo di `modules/crm/store.py:943`.
- **Cosa resta valido.** Nel lotto (`registra_movimenti`) le righe dopo la prima girano davvero nella transazione, quindi il caso «i prelievi vedono i depositi delle righe prima» è corretto.
- **Rispetto a prima.** Le correzioni riducono la finestra rispetto a HEAD, ma non la chiudono come dicono i commenti. Il test `test_v2_bot_381_stop_ricontrollato_nella_transazione_di_invio` prova che il controllo esiste, non che sia atomico.
- **Rimedio.** `con.execute("BEGIN IMMEDIATE")` all'inizio di `_scrivi` (`modules/crm/store.py:483`), più un test con la stessa connessione factory: la scrittura concorrente deve aspettare o fallire, l'invio deve essere rifiutato.
- **Perché MEDIA e non bloccante.** Serve un'operazione concorrente: doppio click, oppure dashboard e riga di comando insieme. Non peggiora nulla rispetto a HEAD, dove il controllo mancava del tutto.

**R-806-2 — BASSA — una data di apertura sbagliata non si corregge più**
- **Cosa è successo.** Il nuovo vincolo «data ≥ aperta_il» (`modules/crm/store.py:773`) rifiuta lo storico registrato su una posizione aperta oggi per errore. È il valore predefinito del form (`value: oggiIso()`).
- **Prova.** «data 2026-01-02 prima dell'apertura del servizio (2026-11-17)».
- **Perché è un vicolo cieco.** Non esiste un modo per correggere `aperta_il`: `apri_posizione` riattiva senza cambiare la data e la coppia cliente-servizio è unica. Per quella posizione lo storico non si registra mai, nemmeno con l'import.
- **Rimedio.** Un metodo per spostare `aperta_il` all'indietro (la tabella posizioni non è immutabile), oppure almeno una riga in reports/crm.md: «apri il servizio con la data vera prima di caricare lo storico».

**R-806-3 — COSMETICA — testo che sfora il limite dopo l'aggiunta**
- `completa_testo` (`modules/crm/messaggi.py:111`) aggiunge nota e STOP dopo il testo dell'operatore. Un testo di circa 1.950 caratteri supera così TESTO_MAX e `transiziona_proposta` (`modules/crm/store.py:926`) risponde «troppo lungo (max 2000)», anche se l'operatore non l'ha scritto lungo.

### Elementi del diff esaminati

- **Scarto come «non ora» — ok.** `modules/crm/motore.py:170` ferma il cliente per `pausa_giorni` dopo uno scarto; `modules/crm/motore.py:236` ferma lo stesso obiettivo per `pausa_dopo_no_giorni`.
  - Rischi esaminati: livello di insistenza alzato per errore; proposta ricreata 2 s dopo dal guardiano.
  - Il livello resta basso: `negativi` non conta gli scarti. `esito_il` viene scritto alla transizione «scartata». Il test mostra che dopo la pausa arriva un obiettivo diverso.
- **Data e capitale dentro il lotto — ok, salvo R-806-1 e R-806-2.** `modules/crm/store.py:773` controlla che la data non sia prima dell'apertura (confronto fra stringhe ISO); `modules/crm/store.py:776` che il prelievo non superi il capitale.
  - `_capitale` esclude storni e movimenti stornati, come `analisi.costruisci`.
  - Un errore dentro il lotto diventa «riga N» e annulla tutto (`modules/crm/store.py:831`).
- **Nota e STOP rimessi in fondo — ok, salvo R-806-3.** `modules/crm/messaggi.py:111` (`completa_testo`) è usata dal server in `modules/crm/server.py:757`, che prima rifiuta un messaggio non testo (`modules/crm/server.py:755`).
  - Rischio esaminato: doppioni o nota persa.
  - È idempotente (test); se la nota è vuota per scelta non viene aggiunta; non c'è nessuna strada per inviare senza la riga STOP.
- **Controlli d'invio nello store — ok come controllo, non come atomicità (R-806-1).** `modules/crm/store.py:939` ricontrolla stato, STOP, consenso e telefono anche fuori dal server, quindi vale anche per la riga di comando.
- **Test cambiati — legittimi.** `test_proposte_transizioni_e_doppioni` ora dà il consenso al cliente, che l'invio pretende; `test_server_flusso_completo` pretende prefisso esatto e riga STOP finale, cioè un'asserzione più stretta. Nessun test indebolito.

### Rischi esplicitamente NON verificati

- La corsa di R-806-1 dal browser vero (doppio click sul pulsante): l'ho provata a livello di store con intrecci forzati, non dalla dashboard.
- La demo con un «oggi» diverso dall'orologio reale: con `popola(oggi=2027-02-28)` fallisce per «data nel futuro», ma è un artefatto della mia prova (l'orologio dello store resta quello vero). In uso normale `oggi` è la data di sistema.
- V-3 e V-4 della verifica esterna (reports/, fuori perimetro): non revisionati.

### Note

- **Memoria del revisore:** riga contatore #806-CRM più una lezione su sqlite3 e le transazioni, in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (commit 8fdae653). Il diff staged è intatto (5 file).
- **Marcatore e commit:** non ho creato `.claude/.review_ok` e non ho committato il diff.
- **Script delle prove**, riutilizzabili per il test di R-806-1:
  - /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/v2.py (prelievi concorrenti e posizione aperta oggi);
  - /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/v2bot.py (STOP scritto fra controllo e UPDATE).
- **Da registrare in reports/stato_progetto.md:** R-806-1, R-806-2, R-806-3. Restano aperte anche R-804-1..4, R-803-4, R-803-9 e R-803-10.

### Review #807-CRM (5° giro, commit 72dcc9d2: riserve R-806-1/2/3)

## VERDETTO: APPROVATO

Review #807-CRM, quinto giro: un solo verdetto su tutto il diff staged (5 file, +169/−5) dopo c9daf955. Le tre riserve di #806 sono chiuse, ognuna con un test che fallisce sul codice prima della correzione. Non ho trovato difetti nuovi di sostanza.

**Verifiche rifatte da me:**
- **Test nuovi contro il vecchio codice:** con i file di HEAD c9daf955 e il file di test staged falliscono esattamente i 4 test nuovi (`test_r806_1_stop_concorrente…`, `test_r806_1_prelievi_concorrenti…`, `test_r806_2_apertura…`, `test_r806_3_testo_lungo…`); gli altri 97 passano.
- **Codice staged:** 101 passed, uguale in 3 esecuzioni. mypy pulito. `node --check modules/crm/web/app.js` ok.
- **Le mie riproduzioni del giro #806, rieseguite sul codice nuovo:**
  - STOP scritto fra il controllo e l'UPDATE: ora `in_transaction` vale True, la connessione concorrente trova il lucchetto occupato e l'invio non passa con lo STOP nel mezzo;
  - due prelievi da 1.000 € su 1.000 € di capitale: il secondo viene rifiutato («maggiore del capitale (0,00 €)») e il capitale finale resta 0.
- **Cosa non è toccato:** kernel, brains/, memoria e cancello.

**Elementi del diff esaminati:**
- `modules/crm/store.py:494` — `BEGIN IMMEDIATE` in `_scrivi`, prima di `fn(con)`. Esito: ok.
  - Rischio esaminato: blocchi reciproci, cioè scritture da altre connessioni fatte dentro `fn`. Ho controllato i corpi `_fn`: usano solo la connessione ricevuta (`_evento`, `_capitale`, `_inserisci_movimento`), nessuno apre un'altra connessione per scrivere.
  - Rischio esaminato: effetti sul kernel. Il lucchetto di scrittura sul file condiviso dura quanto la scrittura del CRM; il kernel aspetta col suo timeout di 10 s. Un lucchetto non ottenuto diventa «database non disponibile» (ErroreCRM, §9).
  - Nota: `crea_proposta` resta fuori da `_scrivi`, ma lì non c'è un «controllo e poi scrittura»: decide l'indice unico.
- `modules/crm/store.py:746` — `anticipa_apertura`: rifiuta le date future (`modules/crm/store.py:752`) e gli spostamenti in avanti (`modules/crm/store.py:762`); il cambio va nel diario del CRM (servizio e date, nessun nome). Esito: ok.
  - Rischio esaminato: rompere la regola «nessun movimento prima dell'apertura». Spostando solo indietro, i movimenti già registrati restano tutti dopo l'apertura.
  - Esposta in `modules/crm/server.py:640` (dopo autenticazione e controlli anti-CSRF comuni), nella CLI (`modules/crm/__main__.py:215`) e nel campo «dal» (`modules/crm/web/app.js:716`). Il campo costruisce il DOM con `el()`, niente HTML dai dati.
- `modules/crm/server.py:760` — errore chiaro «accorcialo di N» quando nota più riga STOP fanno superare TESTO_MAX. Esito: ok. Il conteggio coincide con quello di `_testo`, perché `completa_testo` toglie già gli spazi ai bordi.
- `tests/test_unit_crm.py:1085` e `tests/test_unit_crm.py:1107` — connessione spia (factory) che forza l'intreccio. Esito: ok.
  - Rischio esaminato: un test che passa anche senza la correzione. Non succede: su HEAD falliscono entrambi.
  - Nel verso corretto sono deterministici: il secondo scrittore aspetta il lucchetto, non un orologio.

**Nota minore, non classificata come riserva:** `anticipa_apertura` con la stessa data accetta e scrive un evento «dal X al X» inutile. Il campo della dashboard lo evita; da CLI o API resta possibile.

**Rischi esplicitamente NON verificati:**
- Durata del lucchetto di scrittura con un import CSV molto grande (migliaia di righe in una transazione) mentre il kernel scrive in memoria: non misurata. Plausibilmente sotto il secondo, ma non provata.
- Campo «dal» provato solo con `node --check`, non nel browser: mi fido della prova nel browser dichiarata dal chiamante.

**Riserve che restano aperte (da giri precedenti, non toccate qui):** R-804-1, R-804-2, R-804-3, R-804-4, R-803-4, R-803-9, R-803-10.

**Note:**
- Ho aggiunto la riga contatore #807-CRM in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (commit 83633433). Il diff staged è intatto (5 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

### Review #808-CRM (6° giro, diff staged della fetta 2, prima delle correzioni)

## VERDETTO: BOCCIATO

Review #808-CRM del diff staged (14 file, +1090/−103, tocca anche gas.py), con la stessa severità del primo giro.

**Motivo del blocco (R-808-1):** la protezione dei clienti funziona, ma rallenta ogni turno di Gas in proporzione al numero di clienti del CRM. Con 1 solo cliente nei test non si vede, come la demo nascondeva R-803-1. Dettagli e misure nel finding 1.

**Verifiche rifatte da me:**
- Kernel: `tests/test_unit_kernel.py` dà 1179 PASS, 0 FAIL. T116a1–g passano, T116b è il round-trip §7 (strumento → risposta finale).
- CRM: 113 passed. I 14 test nuovi, rieseguiti contro il codice di HEAD 48c0f114, falliscono tutti e 14.
- mypy pulito, `node --check` ok.
- Il fail-before di T116 (6 falliti sul gas.py vecchio, 2 di guardia che passano) l'ho preso dal dato del chiamante, non l'ho rifatto.
- Nessuno slicing della history e nessuna simulazione di tool. Il cap delle 10 iterazioni non è toccato.

### Finding

**1. R-808-1 — ALTA, bloccante — rallentamento del kernel proporzionale ai clienti del CRM.**
- **Causa.** `gas.py:4049` mette tutti i clienti del CRM fra gli identificativi da cercare. `_contiene_identificativo` (`gas.py:205`) fa una `re.search` per ogni identificativo e per ogni testo. Oltre i 512 pattern che il modulo `re` tiene in cache, ogni ricerca ricompila la sua regex.
- **Misura.** Finestra di 30 messaggi normali, senza dati di clienti, cioè il caso più comune:

  | Clienti nel CRM | Identificativi | Tempo per scansione |
  |---|---|---|
  | 50 | 338 | 119 ms |
  | 100 | 640 | 740 ms |
  | 300 | 1769 | circa 2,0 s |
  | 1500 | 8598 | 9,4 s |

  Con 10 messaggi più un'uscita di strumento da 8k caratteri: 0,9 s a 300 clienti. Con la cache di `re` forzata a 100.000 (solo per capire la causa) si scende a 470 ms a 300 clienti. Quindi pesano sia le ricompilazioni sia la scansione lineare.
- **Dove gira.** A ogni turno (`gas.py:5376`); a OGNI iterazione del ciclo per i cervelli non forti (`gas.py:5487`), quindi più volte per turno; nella riflessione (`gas.py:4417`); sulle righe del blocco di memoria (`gas.py:4176`).
  - Con 300 clienti un turno con 2–3 strumenti su un gratuito costa alcuni secondi in più, anche per la voce.
  - Nessun log lo collega al CRM: un rallentamento silenzioso.
- **Rimedio.** Una sola regex compilata per elenco di identificativi (alternanza con gli stessi lookaround), tenuta in cache per turno; telefoni e indirizzi restano come sono. Più un test di tempo con circa 1000–1500 clienti (es. sotto i 100 ms) e i test di semantica esistenti (#789/#790), così il comportamento del filtro non cambia.

**2. R-808-2 — MEDIA — le riscritture con Opus sfuggono al tetto giornaliero del cervello forte.**
- **Il buco.** `modules/crm/scrittore.py:83` chiama `ClaudeCliClient` direttamente. Il costo equivalente che la risposta riporta non viene scritto in `.gas_claude_cli_uso.json` e non viene confrontato con `GAS_CLAUDE_CLI_TETTO_USD` (il tetto del kernel, `gas.py:5883`).
- **Il tetto del CRM non lo sostituisce.** Conta solo le riscritture RIUSCITE (`modules/crm/scrittore.py:168`, l'evento si scrive dopo il successo), quindi i tentativi falliti o scartati non contano. Inoltre fa «controllo e poi chiamata» senza lucchetto.
- **Effetto.** L'abbonamento del forte si consuma senza che il kernel lo veda, e un esaurimento ferma anche i turni con dati di clienti.
- **Rimedio.** Usare lo stesso conto del kernel e contare i tentativi.

**3. R-808-3 — BASSA — dopo un crash del CRM a metà scrittura, tutto va al forte.**
- **Riprodotto.** Se resta un journal (crash del CRM durante una scrittura), `identita_clienti` in `mode=ro` (`modules/crm/store.py:1279`) fallisce con «attempt to write a readonly database» e restituisce None. Risultato: ogni turno va al forte, e col forte spento Gas rifiuta anche «che ore sono».
- **Fino a quando.** Finché qualcuno riapre il file in scrittura: verificato che basta un `CRMStore(...)`, cioè un qualunque comando del CRM.
- **Rimedio.** Recuperare automaticamente (una connessione normale usata solo per leggere ripristina il journal), oppure dirlo chiaramente nel messaggio di rifiuto.

**4. R-808-4 — BASSA — se kernel e CRM guardano percorsi diversi, la protezione sparisce in silenzio.**
- **Il caso.** Il kernel calcola il file dal proprio `self.root` (`gas.py:4049`), che per il terminale interattivo (`gas.py:6993`) è la cartella da cui lo si lancia. La riga di comando del CRM invece usa la cartella del modulo. Lo stesso succede se `GAS_CRM_DB` è esportata solo nella shell del CRM.
- **Effetto.** «File assente → nessun cliente»: niente protezione, e nessun avviso.
- **Rimedio.** Far usare al kernel la stessa radice di `modules/crm` (o il percorso del modulo); oppure avvisare se il file non c'è ma esiste quello predefinito nella cartella del repo.

**5. R-808-5 — BASSA, da dichiarare all'operatore — più falsi allarmi, e col forte spento più turni fermati.**
- **Misurato.** Con clienti dai cognomi comuni, «fammi i conti del mese», «quanto costa il server?» e «il leone ruggisce» vengono trattati come dati di clienti.
- **Anche le email.** Le parole delle email entrano fra gli identificativi: un dominio aziendale come «trading» o «esempio» farebbe scattare il filtro.
- **Conseguenza.** Il limite è già scritto nel codice, ma con il CRM cresce: col forte spento questi turni si fermano. Il verso è sicuro e coerente con la «massima riservatezza», ma va scritto in reports/crm/guida.md.

**6. R-808-6 — BASSA — le 30 copie di sicurezza contengono i dati completi dei clienti.**
- `modules/crm/store.py:1185` salva le copie in `.gas_memory_crm_backup/`. Un'eventuale anonimizzazione o cancellazione su richiesta (R-803-9) deve coprire anche loro. Va dichiarato.

**7. R-808-7 — COSMETICA.**
- I testi neutri nascono di proposito senza la nota sul rischio (`modules/crm/messaggi.py:108`). Ma all'invio `completa_testo` gliela aggiunge comunque, perché app.js manda sempre il testo.
- Il `.gitignore` non copre più `.gas_crm_demo.db`. Un vecchio DB demo rimasto sul Mac diventa un file non tracciato e finisce negli snapshot (`git add -A`). Dati inventati, quindi innocuo.

### Elementi del diff esaminati e trovati corretti

- **Composizione fail-closed del filtro** (`gas.py:4044`, `gas.py:4055`): lettura dei lead None → None; lettura del CRM None o eccezione → None (tutto al forte). Esito: ok.
- **Pseudo-contatti del CRM nel blocco di memoria:** con `merged_into="crm"` sono esclusi dall'elenco dei lead (filtro `merged_into is None`, `gas.py:4126`) ma usati per anonimizzare le righe del diario. T116a1 controlla che «Marco» non compaia in nessuna delle due versioni. Esito: ok.
- **Lettura da parte del kernel** (`modules/crm/store.py:1268`): `identita_clienti` apre in sola lettura, non scrive mai; file assente → [], tabella assente → []. Esito: ok, salvo R-808-3 e R-808-4.
- **File dei dati protetto:**
  - `.gitignore` `.gas_memory_crm*` (verificato con `git check-ignore` su DB, journal, backup e demo): fuori dagli snapshot `git add -A`;
  - il prefisso `.gas_memory` lo rende illeggibile agli strumenti di Gas (`_SAFE_PATH_DENY_PREFIXES` in gas.py e lista di lettura negata del cancello).

  Esito: ok.
- **Tetto degli invii** (`modules/crm/store.py:1090`): controllato dentro la transazione con lucchetto (`BEGIN IMMEDIATE` di #807); `invii_recenti` (`modules/crm/store.py:1023`) confronta datetime veri, non stringhe. Esito: ok.
- **Saldo minimo** (`modules/crm/store.py:885`): `_saldo_minimo_da` guarda il saldo più basso dalla data del prelievo in poi; usato anche per lo storno di un deposito. Esito: ok.
- **Solo Opus, senza strumenti:** `--model` passato davvero alla CLI (`brains/claude_cli.py:574`, con `--tools ""`). `modules/crm/scrittore.py:74` nega se il modello configurato non contiene «opus» o se il forte è spento, senza ripiego su altri provider. A Claude va solo il minimo (`modules/crm/scrittore.py:116`: nome di battesimo, servizi, risultato positivo). Nel log solo il tipo dell'eccezione. Esito: ok, salvo R-808-2.
- **Selezione manuale** (`modules/crm/motore.py:172`, `modules/crm/motore.py:458`): salta soglia, primo pagamento, anzianità e interruttore del follow-up; restano le regole dure e il ritmo. Testo neutro, senza numeri, con profitto ≤ 0 (`modules/crm/messaggi.py:108`). Esito: ok.
- **Altro lato server:**
  - Host vuoto → 403 (`modules/crm/server.py:364`);
  - la memoria di Gas si apre dal suo file (`modules/crm/__main__.py:114`);
  - R-804-1 chiusa: il `.env` si legge prima del parser;
  - R-804-3 chiusa: un CSV già importato si ferma, salvo `--forza`.

  Esito: ok.
- **Test cambiati:** le righe tolte sono sostituite da asserzioni più strette (riga STOP anche dallo store, valori predefiniti mensili), oppure da regole di test esplicite (`Regole(pausa_giorni=7, max_messaggi_30g=4)`). Nessun test indebolito.

### Rischi esplicitamente NON verificati

- Le misure di R-808-1 vengono dal container (Python 3.13) con nomi sintetici, non dal Mac né dal VPS; i valori assoluti cambieranno, l'andamento no. Non so quanti clienti abbia davvero l'operatore.
- Il costo reale di una riscrittura con Opus sull'abbonamento (R-808-2): non misurato, la CLI qui non c'è.
- Flusso nel browser (spunte, riscrittura, indicatore degli invii): non provato da me, mi fido della prova del chiamante.
- Aspetti legali dei testi promozionali scritti da Opus: fuori dalla mia competenza.

### Note

- **Memoria del revisore:** riga contatore #808-CRM più 2 lezioni (filtri a regex con molte voci; `mode=ro` con un journal rimasto), committate da sole (commit 2bfbb803). Il diff staged è rimasto intatto (14 file).
- **Marcatore e commit:** non ho creato `.claude/.review_ok` e non ho committato il diff.
- **Script delle prove**, utili per il test di tempo:
  - /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/perf.py (1500 clienti e parole comuni);
  - /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/perf2.py (0/50/100/300 clienti e diagnosi della cache).
- **Riserve ancora aperte da giri precedenti:** R-804-2, R-804-4, R-803-9, R-803-10. R-804-1 e R-804-3 sono chiuse in questo diff.
- **Per l'approvazione** serve un nuovo giro con R-808-1 chiusa e il test di tempo che fallisca sul codice di questo giro. Le altre riserve possono restare tracciate in stato_progetto.

### Review #809-CRM (7° giro, diff staged della fetta 2 con le correzioni: commit aa4bb422)

## VERDETTO: APPROVATO CON RISERVE

Review #809-CRM: secondo giro dopo il BOCCIATO #808, con la stessa severità. Diff staged: 14 file, +1543/−158, kernel compreso.

**Esito in breve:** il blocco R-808-1 è chiuso, e lo sono anche le riserve R-808-2, 3, 4 e 7. Restano due riserve nuove BASSE (R-809-1, R-809-2), nessuna bloccante.

**Come ho controllato:** ho ritrovato nel repo i blob esatti revisionati in #808 (gas.py 7c694843, store 5be60cf6, scrittore b9ea3d10, test del kernel e del CRM) e ho confrontato riga per riga solo i cambiamenti di questo giro.

### Verifiche rifatte da me

- **Test:**
  - suite del kernel 1184 PASS, 0 FAIL;
  - suite del CRM 116 passed; mypy pulito su modules/crm; `node --check` ok.
- **I test nuovi mordono sul codice di #808:**
  - kernel: T116j, T116h e il blocco T116 falliscono. T116j fallisce proprio con «NON DEVE ARRIVARE» arrivato a un gratuito, cioè la fuga che R-808-4 chiude. T116h misura 9978 / 9858 ms.
  - CRM: falliscono i 4 test nuovi.
  - Un T85 fallito in quella copia era un file mancante nella mia copia parziale, non legato al diff.
- **Prestazioni, con i miei script:**

  | Clienti | Prima (#808) | Ora, a freddo | Ora, in cache |
  |---|---|---|---|
  | 1500 | 9,4 s | 170 ms | 2 ms |
  | 300 | circa 2,0 s | 28 ms | 2 ms |

- **Equivalenza col filtro vecchio:** ho scritto una mia prova con dati realistici, diversi dal test T116i. Nomi accentati e con apostrofi, nomi attaccati o troncati o allungati, email dentro nomi di file, telefoni con trattini o tagliati. 8000 casi (6601 positivi): 0 differenze fra regex unica e ricerche una per una.
- **Journal rimasto dopo un crash (R-808-3):** crash del CRM a metà scrittura riprodotto (`os._exit` durante una transazione). Ora `identita_clienti` riapre il file, SQLite annulla la scrittura interrotta, il cliente viene riconosciuto e il journal sparisce.
- **Perimetro:** nessuno slicing della history, nessuna simulazione di tool, cap delle 10 iterazioni invariato.

### Riserve nuove

1. **R-809-1 — BASSA — attesa doppia quando il CRM tiene il file bloccato.**
   - Il ripiego in lettura (`modules/crm/store.py:1321`) scatta su ogni `OperationalError`, anche «database is locked», non solo sul caso del journal rimasto.
   - Misurato: con un lucchetto esclusivo tenuto, il turno del kernel aspetta 5 + 5 = 10,0 s prima di chiudere (fail-closed).
   - Nell'uso normale accade di rado (le letture convivono con le scritture del CRM fino al commit), ma è un'attesa inutile in un passaggio che sta nel percorso di ogni turno.
   - Rimedio: ripiegare solo sull'errore «readonly database».
2. **R-809-2 — BASSA — tre suite di test leggerebbero i clienti veri.**
   - La suite del kernel isola `_RADICE_REPO` e toglie `GAS_CRM_DB` dall'ambiente. Non lo fanno `tests/test_unit_notte.py`, `tests/test_unit_voice_contesto.py` e `tests/test_unit_manutenzione.py`, che pure costruiscono `GasKernel`.
   - Su una macchina con un `.gas_memory_crm.db` vero nella cartella del repo (il Mac, il VPS) quelle suite leggono i clienti veri. Possibili esiti diversi, se un testo di prova contiene un nome o un cognome, e lettura di dati veri dentro un test.
   - In CI non succede, perché lì il file non c'è.
   - Rimedio: lo stesso isolamento in una fixture comune (`tests/conftest.py`).

### Elementi del diff esaminati

- **`gas.py:206` — `_trie_regex`:** un'alternanza a trie con prefissi in comune, preceduta e seguita dagli stessi lookaround di prima. Esito: ok.
  - Rischi esaminati: esito diverso dalle ricerche una per una (prefissi l'uno dell'altro, lookahead che fallisce sul ramo lungo), backtracking esplosivo, ricorsione troppo profonda.
  - Il backtracking prova tutti i rami e i gruppi opzionali sono greedy, quindi si prova prima il ramo lungo e poi il corto: stesso esito.
  - Nessun quantificatore annidato: costo per posizione limitato alla profondità del trie.
  - La ricorsione avviene solo dove il trie si dirama. `RecursionError` o `re.error` ripiegano sul codice di prima (T116i2).
- **`gas.py:243` — `_confrontatore`:** cache di 4 elenchi, chiave tupla degli identificativi (ordinati, quindi stabile turno dopo turno). Esito: ok.
  - Indirizzi uniti da uno spazio: gli identificativi senza spazi non possono scavalcare due pezzi, quindi stesso esito di «i in tok».
  - Telefoni: per «tel in d» una regex sulle sequenze unite; per «d in tel» l'insieme delle sottostringhe da 7 cifre; i telefoni oltre 32 cifre si confrontano uno per uno.
- **`gas.py:274` — `_contiene_identificativo`:** stesso risultato booleano. Cambia solo l'ordine dei controlli (prima tutte le parole, poi indirizzi, poi telefoni), che non incide sull'esito. Esito: ok.
- **`gas.py:1406` e `gas.py:1418` — tetto e conto del forte diventati funzioni di modulo.** Esito: ok.
  - Il comportamento del kernel resta identico: `_forte_senza_conto` rimane nel metodo; «già fermo» ritorna True come prima nel ramo `return` dentro il `with`.
  - Il limite dichiarato (controllo prima della chiamata e fuori dal lucchetto) vale ora anche per il CRM, come per il bot e il giro di notte.
- **`gas.py:4174` — il kernel legge il CRM sia dalla propria radice sia dalla cartella del repo** (`gas.py:577`), senza doppioni. Esito: ok.
  - Basta un file illeggibile per restituire None, cioè fail-closed.
  - Con `GAS_CRM_DB` impostata il percorso è uno solo.
- **`modules/crm/store.py:1165` — `segna_evento_entro_tetto`:** controllo e scrittura nella stessa transazione con lucchetto (8 thread, tetto 3: ne passano esattamente 3). Esito: ok.
  - Lo scrittore (`modules/crm/scrittore.py:191`, `modules/crm/scrittore.py:201`, `modules/crm/scrittore.py:221`) controlla il tetto del forte e segna il tentativo PRIMA della chiamata, che resta fuori da ogni transazione (nessun lucchetto tenuto durante i 180 s di attesa).
  - Il costo viene registrato nel `finally`, anche quando la chiamata fallisce. I test usano sempre un `root` temporaneo, mai il conto vero del repo.
- **`modules/crm/store.py:1082` — testo rimandato identico a quello salvato:** non viene riscritto, così il testo neutro parte senza nota. Esito: ok.
  - La riga STOP resta sempre: ogni testo salvato nasce da `componi`, `aggiorna_messaggio` o da un testo cambiato, e tutti e tre la contengono.
  - Il controllo di lunghezza avviene sul testo completato anche quando poi non viene usato: innocuo con i testi brevi del motore.

### Rischi esplicitamente NON verificati

- Prestazioni sul Mac e sul VPS e con un numero reale di clienti: misurate solo nel container (Python 3.13) con nomi sintetici.
- Riscrittura con Claude Opus vera e costo reale per chiamata: qui la CLI non c'è, provata solo con il finto client dei test.
- Documentazione di R-808-5 e R-808-6 in reports/crm/guida.md: fuori stage, ho controllato solo che le due voci ci siano (falsi allarmi su «Conti», «Costa», «trading»; copie di sicurezza da includere in un'eventuale cancellazione GDPR).

### Note

- Riserve ancora aperte da giri precedenti: R-804-2, R-804-4, R-803-9, R-803-10, più R-808-5 e R-808-6 (dichiarate in guida.md).
- Memoria: ho aggiunto la riga contatore #809-CRM e una lezione in /home/user/Gas/.claude/agents/memoria_revisore.md e le ho committate da sole (commit ec2383cd). Il diff staged è intatto (14 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.
- Gli script delle prove sono in /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/rev/:
  - perf.py e perf2.py: prestazioni del filtro;
  - fuzz.py: equivalenza con dati realistici.

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_crm.py` (nuovo):** 0 → 116 passed ad aa4bb422.
  - Al commit 99d82f3f: 93; a 72dcc9d2: 101.
  - Ogni test di regressione aggiunto dopo un verdetto fallisce sul codice precedente:
    - 12 dei 13 `test_r803_*` sul primo staged;
    - 5 test su f1c109a7;
    - i 4 `test_r806_*` su c9daf955;
    - i 14 test della fetta 2 su 48c0f114;
    - i 4 test nuovi del giro #809 sullo staged di #808 (`test_testo_neutro_inviato_com_e`, `test_identita_dopo_crash_a_meta_scrittura`, `test_scrittore_opus`, `test_tetto_degli_eventi_atomico`).
- **Suite del kernel** (`python tests/test_unit_kernel.py`): 1167 → 1184 PASS. Il kernel è toccato dalla fetta 2 (blocco T116 nuovo):

```
=== RIEPILOGO: 1184 PASS, 0 FAIL ===
```

  - Sul gas.py senza fetta 2 i T116 danno 6 FAIL (T116a1, b, c, e, f, g).
  - Sul gas.py della review #808: `=== RIEPILOGO: 1180 PASS, 3 FAIL ===`. I 3 FAIL sono T116j, T116h (9855 ms → soglia 150 ms) e il blocco T116 (`_contiene_identificativo_uno_per_uno` assente).
  - T116b è il round-trip §7: strumento → risposta finale col forte.
- **Altre suite che costruiscono il kernel:** `tests/test_unit_claude_cli.py`, `test_unit_notte.py`, `test_unit_manutenzione.py`, `test_unit_sottofondo.py`, `test_unit_telegram_voce.py`, `test_unit_voice_server.py`, `test_unit_richieste.py`, `test_unit_gate.py`: `1607 passed in 309.26s (0:05:09)`.
- **Suite web:** `tests/test_unit_web_browser.py` non rigirata qui, perché nel container manca `bwrap`. In CI è rossa per i 7 test ambientali del §6, uguali anche su altri rami.
- **mypy** su `modules/crm`: 0 errori nel modulo. Le 76 segnalazioni di altri file (gas.py, modules/voice, modules/sottofondo…) sono le stesse di prima: vengono dall'import di `gas`.

## §6 STATO CI

`gh run list` non usato: in questa sessione cloud GitHub si interroga con gli strumenti MCP. Run lette con `actions_list` / `list_workflow_jobs` alla scrittura dell'handoff:

```
run 44163799980  CI            push                 99d82f3f  completed / failure  (unit-suite: step «Run web suite» 7 failed, 747 passed; «Run CRM suite» success; handoff-check FAILURE allo step «Run check_handoff»: atteso, a quel commit l'handoff non era ancora nel diff — V-1 verifica esterna #381, 2° giro)
run 44163850284  verifica-bot  pull_request_target  99d82f3f  completed / skipped  (PR ancora senza l'etichetta «verifica»)
run 44164393490  CI            push                 772f993c  completed / failure  (unit-suite: step «Run web suite» 7 failed, 747 passed; «Run CRM suite» 93 passed; handoff-check success)
run 44164436879  verifica-bot  pull_request_target  772f993c  completed / success
run 44167235199  CI            push                 2ae4b7a7  completed / failure
run 44167242427  verifica-bot  pull_request_target  2ae4b7a7  completed / success
run 44167852645  CI            push                 48c0f114  completed / failure  (unit-suite: unico step rosso «Run web suite»; «Run unit suite», «Run CRM suite» e le altre suite success; handoff-check success)
run 44167861014  verifica-bot  pull_request_target  48c0f114  completed / success
run 44155950606  CI            push                 adb0e188  completed / failure  (ALTRO ramo, claude/practical-tesla-ea9a9g, PR #380, senza CRM: stesso step «Run web suite» rosso)
run 43312735169  CI            push (main)          01eb9f50  completed / success  (12 nov: «Run web suite» 754 passed)
```

**Rosso della CI NON causato da questa PR (blocco ambientale, da trattare in una fetta a parte):**
- I 7 falliti sono tutti in `tests/test_unit_web_browser.py`, cioè il sandbox bwrap del browser: tmpfs non scrivibili, processi di prova che non partono.
- I test:
  - `test_il_sandbox_non_ha_rete_e_scrive_solo_nei_tmpfs`
  - `test_tmp_dev_shm_e_profilo_hanno_un_tetto`
  - `test_gas_e_la_home_dentro_una_cartella_permessa_sono_coperte`
  - `test_una_permessa_che_e_un_collegamento_non_scopre_gas`
  - `test_ipc_e_processi_dell_host_non_si_vedono`
  - `test_morto_bwrap_muore_il_sandbox`
  - `test_ucciso_bwrap_muore_anche_chi_cambia_gruppo_e_ambiente`
- Passavano su main il 12 nov. Oggi falliscono identici anche sul ramo di un'altra sessione, che non contiene il CRM.
- Ipotesi (non dimostrata): cambio dell'immagine ubuntu-latest dei runner.
- Finché resta, il check required `unit-suite` è rosso per ogni PR.

Mappatura commit→run:
- `15368710`, `ae5197d0`: nessuna run su questi SHA (pushati insieme a 99d82f3f).
- `99d82f3f` (codice CRM, fetta 1): run CI 44163799980.
- `0286192c`, `08b3387b`, `f1c109a7`, `939a2a12`: nessuna run su questi SHA (pushati insieme a 772f993c).
- `772f993c`: run CI 44164393490 e verifica-bot 44164436879.
- `8fdae653`, `c9daf955`, `83633433`, `72dcc9d2`: nessuna run su questi SHA (pushati insieme a 2ae4b7a7).
- `2ae4b7a7`: run CI 44167235199 e verifica-bot 44167242427.
- `48c0f114`: run CI 44167852645 e verifica-bot 44167861014.
- `2bfbb803`, `ec2383cd`, `aa4bb422` (codice della fetta 2): run non ancora disponibile alla scrittura dell'handoff. Saranno pushati insieme al commit di fine-task che contiene questo file, e la run testerà solo l'albero di quel commit.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-809-1 (BASSA):** il ripiego di `identita_clienti` scatta anche su «database is locked». Con il CRM che tiene un lucchetto esclusivo, il turno aspetta 10 s prima di chiudere (fail-closed).
- **R-809-2 (BASSA):** `tests/test_unit_notte.py`, `tests/test_unit_voice_contesto.py` e `tests/test_unit_manutenzione.py` costruiscono `GasKernel` senza isolare il CRM vero della cartella del repo. Rischio sul Mac e sul VPS, non in CI. Rimedio: una fixture in `tests/conftest.py`.
- **R-808-5 (BASSA, dichiarata in `reports/crm/guida.md`):** falsi allarmi su cognomi comuni e parole delle email. Il verso è sicuro: quei turni vanno al forte.
- **R-808-6 (BASSA, dichiarata):** le copie di sicurezza contengono i dati completi. Un'eventuale cancellazione GDPR deve coprirle.
- **R-803-9 (BASSA, decide l'operatore):** GDPR. Il diario del CRM è immutabile e senza nomi; l'anonimizzazione dell'anagrafica su richiesta è da decidere.
- **R-803-10 (BASSA):** la protezione del cancello vale solo per i file `.gas_memory*`. La CLI avvisa se `GAS_CRM_DB` ha un altro nome.
- **R-804-2 (BASSA):** la dashboard ricarica e il motore riscansiona anche alle scritture del kernel nel file condiviso (oggi i file sono separati, quindi resta solo per chi punta `GAS_CRM_DB` alla memoria).
- **R-804-4 (COSMETICA):** corpo chunked trattato come vuoto; BrokenPipe in do_POST su stderr.
- **Nota minore #807 (non riserva):** `anticipa_apertura` con la stessa data scrive un evento inutile.
- **Chiuse in questa sessione:**
  - R-803-1/2/3/4/5/6/7/8/11;
  - R-804-1, R-804-3;
  - R-806-1/2/3;
  - R-808-1/2/3/4/7;
  - V-1/V-2 della verifica esterna #381 e V-1/V-2 del bot #381;
  - V-4 della verifica esterna #381, 2° giro (Host vuoto ora rifiutato).
