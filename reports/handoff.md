# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-17 — CRM clienti, prima bozza (fetta 1): servizi, registro movimenti, motore delle opportunità, dashboard in tempo reale

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #381 (https://github.com/Gasss23/Gas/pull/381), dopo il nuovo giro di bot e verifica esterna. Il merge lo decide l'operatore (riserve BASSE aperte; check verifica-bot neutral perché la PR tocca la CI). Oggi è BLOCCATO dal check required `unit-suite`, rosso per 7 test del sandbox del browser che falliscono anche su altri rami (vedi §6): serve prima una fetta separata su quel problema dei runner.
2. I 4-5 servizi veri (nome, come guadagniamo, capitale minimo): oggi ci sono solo quelli della demo.
3. Invio WhatsApp senza firma: oggi ogni messaggio lo approva l'operatore (principio del 19 ottobre). L'automatico richiede di cambiare quella regola e l'API WhatsApp Business con modelli approvati.
4. Prima dei dati veri: consenso dei clienti raccolto davvero; verifica Consob con un consulente; decisione GDPR (anonimizzazione su richiesta, R-803-9); chiusura di R-803-4 (regola dei modelli).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — CRM clienti (modulo, motore, dashboard, test, CI)**: FATTA — commit 99d82f3f; review #803-CRM BOCCIATO → #804-CRM APPROVATO CON RISERVE. Guida: `reports/crm.md`.
- **Fetta 1b — gate IP**: FATTA — il primo `fine_task_finale.sh` si è fermato sugli indirizzi d'esempio di `tests/test_unit_crm.py` (test che pretende il rifiuto dei bind non locali): marcatore `gasmerge-ip-ok` sulla riga, commit f1c109a7, review #805-CRM APPROVATO.
- **Fetta 1c — finding del bot e della verifica esterna sulla PR #381**: FATTA — verifica esterna V-1 (MEDIA, proposta scartata ricreata subito) e V-2 (BASSA, movimenti incoerenti), bot V-1 (BASSA, testo corretto senza riga STOP) e V-2 (BASSA, STOP non ricontrollato nella transazione d'invio): commit c9daf955, review #806-CRM APPROVATO CON RISERVE; riserve R-806-1 (MEDIA, controlli non atomici), R-806-2, R-806-3 chiuse nel commit 72dcc9d2, review #807-CRM APPROVATO. V-3 (nota sugli importi) in `reports/crm.md`; V-4 (questo §3/§6) aggiornato qui.
- **Invio automatico WhatsApp**: SALTATA — principio del 19 ottobre (firma per ciò che esce); servono numero business e modelli approvati.
- **Strumento CRM per il modello di Gas** (sola lettura, solo cervello forte) e chiusura di R-803-4: DEFERITA — tocca `gas.py`, prossima fetta.
- **Integrazioni (broker, risposte WhatsApp automatiche)**: DEFERITA — `reports/crm.md` §7.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   10 ++++
 .github/workflows/ci.yml           |    8 +++
 .gitignore                         |    4 ++
 modules/crm/__init__.py            |   18 ++++++
 modules/crm/__main__.py            |  353 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/analisi.py             |  389 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/demo.py                |  133 +++++++++++++++++++++++++++++++++++++++++
 modules/crm/messaggi.py            |  129 ++++++++++++++++++++++++++++++++++++++++
 modules/crm/motore.py              |  423 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/server.py              |  839 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/store.py               | 1085 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/web/app.css            |  319 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/web/app.js             |  829 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/web/favicon.svg        |    1 +
 modules/crm/web/index.html         |   17 ++++++
 reports/crm.md                     |  107 +++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |   17 ++++--
 reports/handoff.md                 |  n/d
 reports/roadmap.md                 |    1 +
 reports/stato_progetto.md          |    5 +-
 reports/ultimo_report.md           |   32 +++++++---
 tests/test_unit_crm.py             | 1159 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
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

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. I commit `docs(fine-task)` elencati sono le versioni precedenti di questo handoff (V-4 della verifica esterna #381).

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

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_crm.py` (nuovo): 0 → **101 passed** a 72dcc9d2 (3 giri stabili; 93 al commit 99d82f3f). Ogni test di regressione aggiunto dopo un verdetto fallisce sul codice precedente: 12 dei 13 `test_r803_*` sul primo staged, 5 test (i 4 `*_381` e `test_server_flusso_completo`) su f1c109a7, i 4 `test_r806_*` su c9daf955. I 13 test `test_r803_*` sul codice staged prima delle correzioni: 12 failed, 1 passed (keep-alive normale, che deve passare in entrambi).
- Suite del kernel (`python tests/test_unit_kernel.py`, kernel non toccato):

```
=== RIEPILOGO: 1167 PASS, 0 FAIL ===
```

- Suite pytest completa senza e2e (sulla prima versione del CRM, 80 test CRM): `33 failed, 4103 passed, 2 skipped in 578.16s (0:09:38)`. I 33 FAIL sono tutti in `tests/test_unit_web_browser.py` e fuori scope: identici sul commit di base 01eb9f50 (`33 failed, 11 passed` in una worktree pulita) perché nel container cloud manca `bwrap` (`bwrap: command not found`); la CI lo installa. Dopo le correzioni è cambiato solo `modules/crm` con la sua suite (93 passed).
- mypy su `modules/crm`: `Success: no issues found in 8 source files`.

## §6 STATO CI

`gh run list` non usato (in questa sessione cloud GitHub si interroga con gli strumenti MCP). Run lette con `actions_list` / `list_workflow_jobs` alla scrittura dell'handoff:

```
run 44163799980  CI            push                 99d82f3f  completed / failure  (unit-suite: step «Run web suite» 7 failed, 747 passed; «Run CRM suite» success; handoff-check success)
run 44163850284  verifica-bot  pull_request_target  99d82f3f  completed / skipped  (PR ancora senza l'etichetta «verifica»)
run 44164393490  CI            push                 772f993c  completed / failure  (unit-suite: step «Run web suite» 7 failed, 747 passed; «Run CRM suite» 93 passed; handoff-check success)
run 44164436879  verifica-bot  pull_request_target  772f993c  completed / success  (check verifica-bot: neutral — APPROVATO CON RISERVE, la PR tocca la CI)
run 44155950606  CI            push                 adb0e188  completed / failure  (ALTRO ramo, claude/practical-tesla-ea9a9g, PR #380, senza CRM: stesso step «Run web suite» rosso)
run 43312735169  CI            push (main)          01eb9f50  completed / success  (12 nov: «Run web suite» 754 passed)
```

**Rosso della CI NON causato da questa PR (blocco ambientale, da trattare in una fetta a parte):** i 7 falliti sono tutti in `tests/test_unit_web_browser.py` (sandbox bwrap del browser: tmpfs non scrivibili, processi di prova che non partono) — `test_il_sandbox_non_ha_rete_e_scrive_solo_nei_tmpfs`, `test_tmp_dev_shm_e_profilo_hanno_un_tetto`, `test_gas_e_la_home_dentro_una_cartella_permessa_sono_coperte`, `test_una_permessa_che_e_un_collegamento_non_scopre_gas`, `test_ipc_e_processi_dell_host_non_si_vedono`, `test_morto_bwrap_muore_il_sandbox`, `test_ucciso_bwrap_muore_anche_chi_cambia_gruppo_e_ambiente`. Gli stessi test passavano su main il 12 nov (754 passed); oggi falliscono identici anche sul ramo di un'altra sessione che non contiene il CRM; in questo container, con bubblewrap 0.9.0 installato, l'intera suite web passa. Ipotesi (non dimostrata): cambio dell'immagine ubuntu-latest dei runner tra il 12 e il 17 nov. Finché resta, il check required `unit-suite` è rosso per ogni PR.

Mappatura commit→run:
- `15368710`, `ae5197d0`: nessuna run su questi SHA (pushati insieme a 99d82f3f).
- `99d82f3f` (codice CRM): run CI 44163799980 (sopra).
- `0286192c`, `08b3387b`, `f1c109a7`, `939a2a12`: nessuna run su questi SHA (pushati insieme a 772f993c).
- `772f993c` (fine-task): run CI 44164393490 e verifica-bot 44164436879 (sopra).
- `8fdae653`, `c9daf955`, `83633433`, `72dcc9d2`: mai pushati prima di questo fine-task → nessuna run su questi SHA; il push che porta questo handoff testa solo il commit di testa.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-803-4 (MEDIA)**: il rilevatore della regola dei modelli (`gas.py`, nomi dalla rubrica lead) non conosce i clienti del CRM → condizione prima dei dati veri; si chiude nella fetta «Gas legge il CRM».
- **R-803-9 (BASSA, decide l'operatore)**: GDPR — diario CRM immutabile (oggi senza nomi), anonimizzazione dell'anagrafica su richiesta da decidere.
- **R-803-10 (BASSA)**: la protezione del cancello vale solo per i file `.gas_memory*`; la CLI avvisa se `GAS_CRM_DB` ha un altro nome.
- **R-804-1 (BASSA)**: `GAS_CRM_PORT` nel `.env` ignorata (parser costruito prima di caricare il `.env`); dichiarato in `reports/crm.md`.
- **R-804-2 (BASSA)**: la dashboard ricarica e il motore riscansiona anche alle scritture del kernel nel file condiviso.
- **R-804-3 (BASSA)**: lo stesso CSV importato due volte raddoppia i movimenti.
- **R-804-4 (COSMETICA)**: corpo chunked trattato come vuoto; BrokenPipe in do_POST su stderr.
- Nota minore #807 (non riserva): `anticipa_apertura` con la stessa data scrive un evento inutile (la dashboard lo evita).
- Chiuse in questa sessione: R-803-1/2/3/5/6/7/8/11; V-1/V-2 della verifica esterna #381 e V-1/V-2 del bot #381; R-806-1/2/3.
