# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-25 — Scheda clienti da leggere offline (decisione 22)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta.
2. Sul Mac, dopo il merge: `cd ~/Gas && git pull && source .venv/bin/activate && pip install -r requirements.txt`; nel `.env` aggiungere `GAS_CRM_SCHEDA_PASSWORD=` con una password NUOVA di almeno 16 caratteri, diversa da quella delle copie, salvata nel gestore di password; poi `python -m modules.crm scheda --forza`.
3. Sull'iPhone: app File → iCloud Drive → «Gas CRM (copie cifrate)» → «Scheda clienti.pdf» → «Mantieni scaricato»; aprirla una volta con la password.
4. Dalla chat Voce (#405, regola 3): scelta del modello, licenza CC BY-NC-SA, prova sul Mac (in `reports/stato_progetto.md`).

---

## §1 SCOPE & ESITO FETTE

- **Scheda clienti da leggere offline** (richiesta dell'operatore: «per forza tailscale? … posso accederci eventualmente offline … mi serve solo un dato al volo»; scelte: «Sì, fai la scheda», «Scheda ora, modifiche col server»; decisione 22): FATTA (36587824, review #864, #865, #866 APPROVATO CON RISERVE). R-864-1 MEDIA (password delle copie riusata) e R-865-1 MEDIA (password cambiata ignorata dal servizio) chiuse prima del commit.
- **Modifiche offline salvate al ritorno della rete**: NON FATTE in questa fetta per scelta dell'operatore («modifiche col server»).
- **Riallineamento a main** (PR #405 Voce e #406): avanzamento veloce, nessun conflitto; riserve dell'ultimo verdetto del bot sulla #405 (V-1, V-2 BASSE) riportate in `reports/stato_progetto.md` (regola 3).
- **Merge di main (PR #402, R7 fetta 4) dopo l'apertura della PR** (3b8737b5; V-1 MEDIA della verifica esterna e V-1 del bot: PR in conflitto): FATTO, review #867-MERGE APPROVATO. Conflitti solo nei report e nella memoria; report del ramo tenuti, stato e memoria uniti, V-1 COSMETICA dell'ultimo verdetto del bot sulla #402 riportata in stato (regola 3). Sottofondo identico a main.
- **Note della verifica esterna e del bot sulla #410** (07b0da7f; verifica: APPROVATO CON RISERVE, https://github.com/Gasss23/Gas/pull/410#issuecomment-7168393340; bot: APPROVATO CON RISERVE, success): V-1 conflitto chiuso dal merge; aperte BASSE V-2 bot (lock solo dentro un processo: CLI e server insieme possono lasciare la scheda vecchia con l'impronta nuova), V-3 bot COSMETICA (a capo fisso a 95 caratteri), V-3 verifica (lunghezza minima ma non entropia della password: consigliata una frase lunga e casuale), V-5 verifica COSMETICA.
- **Prova su iPhone e iCloud veri**: SALTATA — non raggiungibili da qui.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  10 +
 modules/crm/__main__.py            |  16 ++
 modules/crm/scheda.py              | 363 +++++++++++++++++++++++++++++++++++++
 modules/crm/server.py              |  42 +++++
 reports/crm/decisioni.md           |   1 +
 reports/crm/guida.md               |   3 +
 reports/diff_sessione.md           |  17 +-
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   9 +-
 reports/ultimo_report.md           |  35 ++--
 requirements.txt                   |   2 +
 tests/conftest.py                  |   1 +
 tests/test_unit_crm.py             | 356 ++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale. Base: main 86a23f56 (dopo il merge della #402; la sessione era partita da b7182a7c).

## §3 GIT LOG --ONELINE (sessione)

```
36587824 feat(crm): scheda clienti da leggere offline — PDF con password propria (AES-256) su iCloud Drive, rifatta solo quando cambiano i dati, zero token (decisione 22; review #864, #865, #866)
07b0da7f docs(fine-task): scheda clienti offline — report, handoff (review #864–#866), stato con le riserve della #405 (regola 3)
3b8737b5 Merge origin/main (PR #402 R7 fetta 4) nel ramo della PR #410 — report del ramo tenuti, stato e memoria uniti, V-1 del bot sulla #402 in stato (regola 3; review #867-MERGE APPROVATO)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Commit 36587824 — review #864 (verdetto integrale, primo giro)

## VERDETTO: APPROVATO CON RISERVE

Review #864. Diff staged su claude/nifty-galileo-3k7kbm sopra b7182a7c: 7 file, +446, sha256 01cfc6e2 (lo hash era lo stesso prima e dopo la review). Ho letto, nell'ordine, CLAUDE.md (sez. 5, 8, 9 e 10), reports/stato_progetto.md (le parti sul CRM) e la mia memoria (lezioni da #803 a #863-MERGE). Applicate in particolare due lezioni: quella del 2026-11-17 (nessuna scrittura nel DB nel percorso del guardiano) e quella del 2026-10-21 (l'impronta avanza solo dopo una scrittura riuscita), più il precedente R-815-4. Nessuno slicing della history e nessuna simulazione di tool: il diff non tocca il kernel.

**Elementi del diff esaminati**
- modules/crm/scheda.py:183 — il PDF scritto a mano (xref, offset, /Length) — rischio: file illeggibile o lunghezze sbagliate — **ok**. Ho controllato a parte che ogni voce xref sia di 20 byte e punti a «N 0 obj», e che /Length + 1 cada su «\nendstream». pypdf lo legge in `strict=True` senza un avviso.
- modules/crm/scheda.py:138 — escaping di `\ ( )` dopo la codifica cp1252 — rischio: un nome che rompe il PDF — **ok**. Provati: «endstream endobj xref trailer %%EOF», «BT ET Tj /F1 99 Tf», parentesi non bilanciate, `\` finale, NUL e controlli, CR/LF/VT/FF, C1, surrogato isolato, emoji, cinese, ebraico, BOM, U+2028, 500 caratteri senza spazi. Nessun errore, e il testo si estrae uguale.
- modules/crm/scheda.py:195 — cifratura AES-256 — rischio: che sia la R5 deprecata — **ok**: è R6/V5. pypdf 6.17 applica SASLprep. La password sbagliata viene rifiutata.
- modules/crm/scheda.py:242 — temporaneo creato in esclusiva, poi os.replace (modules/crm/scheda.py:243) — rischio: dati in chiaro su iCloud — **ok**: su disco vanno solo byte già cifrati, il chiaro resta in memoria. Nessuna parola del contenuto compare nel file. I nomi dei file non contengono dati. In iCloud, dopo 3 riscritture, c'è solo «Scheda clienti.pdf».
- modules/crm/scheda.py:245 — impronta scritta dopo il replace — rischio: impronta avanzata senza file nuovo — **ok** nel codice, ma il test non lo fissa (vedi R-864-5). L'impronta è 0600, sta accanto al DB e non su iCloud. Il prefisso .gas_memory la nega ai tool del modello (gas.py:2476) ed è coperta da `.gas_memory_crm*` nel .gitignore.
- modules/crm/scheda.py:206 — HMAC con la password come chiave — rischio: l'impronta come oracolo della password — **ok**. Per sfruttarla servono le righe (cioè il DB), e il DB sta sullo stesso Mac del .env, dove la password è già in chiaro: nessun rischio in più.
- modules/crm/scheda.py:88 — filtro dei movimenti stornati — rischio: mostrare un movimento annullato — **ok**: provato con un deposito stornato, che non compare. Però nessun test lo fissa: il mutante che toglie il filtro sopravvive (R-864-5).
- modules/crm/server.py:387 — la scheda nel guardiano — rischio: rallentare o bloccare il server, o un ciclo continuo — **riserva** (R-864-3). La scheda non scrive nel DB: data_version, letto da un'altra connessione, resta uguale dopo 3 forza=True, quindi niente ciclo. Il §9 regge: c'è un try attorno alla chiamata. Tempi: 1000 clienti con 20 movimenti l'uno = 0,25 s (580 KiB); «invariata» = 0,10 s.
- tests/test_unit_crm.py:3299 — la fixture toglie GAS_CRM_SCHEDA_PASSWORD — rischio: test che scrivono nell'iCloud vero — **riserva**: vale solo dentro la fixture (R-864-2).

Prove rieseguite da me: `pytest tests/test_unit_crm.py` sulla copia dell'indice dà 201 passed; mypy non dà errori in modules/crm (i 79 errori riportati sono in altri file). 15 mutanti:
- uccisi (6 più il controllo letale): impronta senza password, senza dest.exists, senza escaping, senza riarmo al cambio, ripiego della password corta, dati non cifrati;
- vivi: vedi R-864-5.

**Riserve**
- **R-864-1 MEDIA** — modules/crm/scheda.py:46: senza GAS_CRM_SCHEDA_PASSWORD la scheda usa la password delle copie .gascrm. Misurato: PDF R6 1,06 ms a tentativo, scrypt 2^17 353 ms a tentativo (modules/crm/copia_cifrata.py:46), circa 330 volte in CPU; su GPU il divario cresce perché scrypt usa molta memoria (non misurato). Chi prende la cartella iCloud indovina la password dal PDF e apre tutte le copie complete del DB: si annulla l'effetto di R-815-3. Correzione: password propria obbligatoria e rifiutata se uguale a quella delle copie, oppure una scelta esplicita dell'operatore scritta nella decisione 22 e nella guida (oggi la guida presenta il ripiego come una comodità). Va chiusa prima del merge, o decisa dall'operatore.
- **R-864-2 BASSA** — tests/conftest.py:38: toglie BACKUP_PASSWORD e CIFRATO_DIR, ma non GAS_CRM_SCHEDA_PASSWORD, e il .env dell'operatore è esportato in ogni terminale. Provato con una HOME finta che ha un iCloud finto e la variabile esportata: un test che chiama `scheda.aggiorna` senza fixture scrive i dati di prova in «Gas CRM (copie cifrate)/Scheda clienti.pdf». Dopo, il server vero confronta la propria impronta, la trova uguale e dice «invariata», quindi la scheda con i clienti finti resta fino al prossimo cambio vero. Oggi nessun test lo fa (suite intera girata così, nessun file scritto). Correzione: una riga `delenv` in conftest.
- **R-864-3 BASSA** — modules/crm/server.py:387: la scheda gira sincrona nel thread del guardiano, mentre la copia esterna da R-815-4 gira in un thread a parte (modules/crm/server.py:344). Con una cartella di rete o un disco esterno appeso (GAS_CRM_BACKUP_CIFRATO_DIR) si fermano gli eventi «cambio» della dashboard, le scansioni e le copie giornaliere. iCloud Drive è un disco locale, quindi non è il caso normale.
- **R-864-4 BASSA** (dati mostrati) — modules/crm/scheda.py:115: «Ultimi movimenti» non scarta i movimenti con data dopo oggi, mentre il capitale li scarta (analisi.costruisci). Provato con l'orologio avanti al momento della registrazione: compare «15/12/2026 deposito 500,00 €» con capitale 1.000,00 € che non lo conta. Inoltre «profitto del mese» (modules/crm/scheda.py:113) non dice di quale mese e, al cambio di mese senza cambi nei dati, resta quello vecchio: il ricalcolo darebbe 0,00 €, il file resta su +70,00 €. La data in testata attenua.
- **R-864-5 BASSA** — mutanti vivi:
  - filtro degli stornati (richiesto esplicitamente);
  - guardia `not stato.demo` (modules/crm/server.py:383): se sparisse, i dati della demo finirebbero nella scheda vera su iCloud;
  - impronta scritta prima del replace;
  - riprova dopo 1 h (modules/crm/server.py:391);
  - MOVIMENTI_PER_CLIENTE = 1;
  - `cmd_scheda` che restituisce sempre 0;
  - `_genitore_assente` tolto (equivale, perché mkdir senza parents fallisce comunque).
- **R-864-6 BASSA** — modules/crm/scheda.py:241: il `.Scheda clienti.pdf.<pid>-<tid>.tmp` lasciato da un kill o da un Mac spento a metà non lo toglie `_pulisci_tmp_vecchi` (modules/crm/copia_cifrata.py:333 guarda solo crm-*.gascrm.*tmp e .prova-*.tmp). È cifrato, ma si accumula su iCloud.
- **R-864-7 BASSA** — modules/crm/__main__.py:139: all'avvio dice «ATTIVA» senza nessuna prova di scrittura, e «(iCloud Drive)» anche se la cartella è un'altra. Un fallimento della scheda si vede solo come warning in gas_debug.log, non in dashboard né in /api/stato.

**Cosmetiche**
- `git diff --staged --check`: riga vuota a fine file in reports/crm/decisioni.md.
- «(chiusa, dal …)» si legge come data di chiusura, ma è la data di apertura.
- Righe da 100 caratteri larghi (maiuscole) escono dal margine.
- /Count delle pagine e /Length degli stream sono in chiaro: lasciano capire all'incirca quanti sono i clienti.
- La scheda vecchia resta su iCloud quando la funzione si spegne o la cartella cambia.
- In `aggiorna` l'assert sta fuori dal try.

**Rischi esclusi**
- Apertura del PDF R6 sull'iPhone (app File e «Mantieni scaricato»): non riproducibile qui, nessun dispositivo iOS.
- Comportamento di iCloud con i file che iniziano con il punto e con le sostituzioni durante la sincronizzazione: non verificabile su Linux.
- SASLprep con pypdf 5.1, il minimo ammesso da requirements: ho verificato solo la 6.17.
- Velocità d'attacco su GPU: non misurata, ho citato solo i tempi CPU.

**Note per il chiamante**
- Contatore: #863 c'è solo come #863-MERGE, sia nel ramo sia su origin/main; ho usato #864.
- La riga #864 e 2 lezioni sono in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, fuori stage e NON committate, come da tua richiesta (non ho lanciato commit_memoria_revisore.sh).
- Non ho creato `.claude/.review_ok`. Ce n'è uno residuo, delle 13:39, con SHA edd64299 diverso dal diff attuale: non apre il gate.
- File principali: /home/user/Gas/modules/crm/scheda.py, /home/user/Gas/modules/crm/server.py, /home/user/Gas/tests/conftest.py.

### Commit 36587824 — review #865 (verdetto integrale, secondo giro)

## VERDETTO: APPROVATO CON RISERVE

Review #865: secondo giro della #864. Diff STAGED sul ramo claude/nifty-galileo-3k7kbm sopra main b7182a7c: 8 file, +591. Lo sha256 del diff è e7239fb6…, ricontrollato prima e dopo la review, ed è invariato. Ho letto CLAUDE.md, reports/stato_progetto.md (le parti sul CRM) e la mia memoria. Non ho committato, non ho creato .claude/.review_ok e la memoria resta fuori dallo stage.

**Cosa ho rieseguito (su una copia dell'indice)**
- `pytest tests/test_unit_crm.py`: 205 passed.
- mypy: 0 errori in modules/crm (79 errori, tutti fuori da modules/crm, per esempio in gas.py).
- `git diff --cached --check`: pulito.
- Nel diff non ci sono IP letterali.

**Elementi del diff esaminati**
1. `modules/crm/scheda.py:49` — `password()` accetta solo `GAS_CRM_SCHEDA_PASSWORD`, normalizzata, di almeno 16 caratteri; il ripiego è tolto. Rischio esaminato: riuso della password delle copie. Esito: ok, R-864-1 chiusa per l'uguaglianza esatta.
2. `modules/crm/scheda.py:56` — confronto a tempo costante con `GAS_CRM_BACKUP_PASSWORD` normalizzata. Esito: ok, con riserva R-865-2.
3. `tests/conftest.py:40` — toglie la variabile nella fixture autouse. Provato con HOME finta, un iCloud finto e la password esportata: la scheda è spenta e nella cartella non viene scritto niente. Esito: ok, R-864-2 chiusa.
4. `modules/crm/server.py:407` — la scheda gira in un thread a parte; se il precedente è ancora vivo, si rimanda (`modules/crm/server.py:408`). L'ho provato col guardiano vero e un `aggiorna` finto lento, con un cambio dei dati mentre la scheda girava: 2 esecuzioni, mai 2 insieme, il cambio è stato ripreso dopo. Esito: ok, nessuna doppia esecuzione e nessuna richiesta persa.
5. `modules/crm/server.py:402` — riprova dopo un esito «non riuscita». Provato con esito fallito e con eccezione: la riprova parte sempre. Esito: ok nel comportamento, con riserva sul registro (R-865-4).
6. `modules/crm/scheda.py:105` — esclude stornati e movimenti datati dopo oggi, con lo stesso filtro di `modules/crm/analisi.py:106`. In `modules/crm/scheda.py:131` il profitto porta il nome del mese. Esito: ok, R-864-4 chiusa.
7. `modules/crm/scheda.py:279` e `modules/crm/scheda.py:281` — prima la sostituzione del file, poi l'impronta. Il mutante che le inverte viene ucciso. `modules/crm/scheda.py:227` toglie i temporanei vecchi; i mutanti «toglili tutti» e «senza pulizia nel finally» vengono uccisi. Esito: ok, R-864-6 chiusa.
8. `modules/crm/scheda.py:224` e `modules/crm/scheda.py:271` — l'impronta è calcolata con la password come chiave, quindi un riavvio con una password nuova riscrive la scheda. Esito: blocco evitato, ma riserva R-865-1 (sotto).

**Riserve**
- **R-865-1 MEDIA** (la tua domanda sul cambio della password). Il servizio launchd legge il `.env` una volta sola, all'avvio (`modules/crm/__main__.py:435`). La riga di comando invece legge la password nuova.
  - Provato: con la password nuova, `scheda --forza` scrive un PDF che si apre con la nuova. Poi il server, con l'ambiente vecchio e senza nessun cambio dei dati, lo riscrive («aggiornata»): ora si apre con la VECCHIA e non con la nuova. Succede al primo giro del server: cambio dei dati, ricontrollo giornaliero o riprova.
  - Alla prima accensione il server resta «spenta» finché non viene riavviato, e il PDF fatto con `--forza` resta vecchio senza nessun avviso.
  - `reports/crm/guida.md:37` non dice di riavviare il CRM dopo aver messo o cambiato la password.
  - Correzione minima: riavvio scritto nella guida, e un avviso da `cmd_scheda` se il CRM è acceso. Meglio ancora: rileggere la password dal `.env` a ogni scrittura. Va chiusa prima del merge.
- **R-865-2 BASSA**. Se `GAS_CRM_BACKUP_PASSWORD` viene portata uguale alla password della scheda, la scheda si spegne ma il PDF già su iCloud resta, e si apre con la password delle copie (provato). Si ricrea così il rischio di R-864-1. Inoltre le varianti (password delle copie più un suffisso) sono ammesse.
- **R-865-3 BASSA**. La logica nuova del guardiano non ha test: R-864-5 è chiusa solo per i mutanti che hai elencato. Mutanti vivi, provati da me (10 passed ciascuno, il controllo letale viene ucciso):
  - senza riprova;
  - senza il controllo del thread vivo;
  - richiesta persa quando il thread è vivo;
  - registro scritto a ogni esito;
  - senza il ricontrollo giornaliero;
  - `>=` invece di `>` (sparirebbero i movimenti di oggi);
  - uguaglianza senza normalizzare la password delle copie.
- **R-865-4 BASSA**. Il commento dice «nel registro solo i cambi di esito», ma `modules/crm/server.py:405` rimette l'esito a «da riprovare», così ogni riprova scrive di nuovo lo stesso avviso (provato: 3 riprove, 3 righe uguali). Sono 1 all'ora, più la riga di scheda.py sulle eccezioni: non è un ciclo stretto. Inoltre «aggiornata» e «spenta» sono INFO e non arrivano mai in gas_debug.log (`modules/crm/__main__.py:433`, livello WARNING), mentre il messaggio d'avvio dice «esito nel registro gas_debug.log» (`modules/crm/__main__.py:140`). R-864-7 resta aperta.
- **Cosmetiche** (3):
  - se iCloud blocca il thread, il guardiano rimanda ogni 120 s per sempre, senza avviso;
  - tre righe vuote prima della sezione nuova dei test (`tests/test_unit_crm.py:3287`);
  - restano quelle già dichiarate: /Count e /Length in chiaro, la scheda vecchia che resta se si spegne.

**Rischi esclusi (non verificati)**
- Cosa fa iCloud della versione vecchia sostituita da `os.replace` (cestino o versioni su iCloud.com) e della copia «Mantieni scaricato» sull'iPhone offline: non si può riprodurre fuori da un Mac con iCloud.
- L'apertura reale del PDF R6 nell'app File di iOS.
- Il ritmo «giornaliero» di `time.monotonic` col Mac in stop: preesistente, è lo stesso timer delle copie.

**Memoria del revisore**
Ho scritto la riga #865 e due lezioni in /home/user/Gas/.claude/agents/memoria_revisore.md. Il file è modificato nel working tree, NON in stage e NON committato, come mi hai chiesto: lo script `commit_memoria_revisore.sh` non è stato lanciato.

File utili:
- /home/user/Gas/modules/crm/scheda.py
- /home/user/Gas/modules/crm/server.py
- /home/user/Gas/modules/crm/__main__.py
- /home/user/Gas/reports/crm/guida.md
- /home/user/Gas/tests/test_unit_crm.py
- le sonde che ho usato: /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/sonde/password.py, /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/sonde/guardiano.py, /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/sonde/mutanti.py

### Commit 36587824 — review #866 (verdetto integrale, terzo giro)

## VERDETTO: APPROVATO CON RISERVE

Review #866: il diff staged sul ramo claude/nifty-galileo-3k7kbm sopra b7182a7c. 8 file, +784 righe; lo sha256 del diff inizia con 5729e0c2 e coincide con quello dichiarato. Prima di cominciare ho letto CLAUDE.md, stato_progetto e la mia memoria. La riga #866 è in coda a `.claude/agents/memoria_revisore.md`, fuori dallo stage e non committata, come hai chiesto. Non ho creato `.claude/.review_ok`. Wall of Shame: il diff non tocca né la storia dei messaggi né `_get_window()`, e non simula output di tool.

**Elementi del diff esaminati**

- `modules/crm/scheda.py:50` — `_leggi_env_file` rilegge il `.env` con le regole del kernel. Rischio: che il parsing diverga da `gas._carica_dotenv`. Ho confrontato i due lettori su 8000 file `.env` generati a caso (BOM, `export`, virgolette, commenti, righe ripetute, CRLF): 0 differenze. Un mutante di controllo («vince l'ultima riga») ne dà 525, quindi il confronto sa vederle. Esito: ok.
- `modules/crm/scheda.py:89` — `_valore`: il `.env` vince sull'ambiente, al contrario del kernel; una chiave venuta dal `.env` all'avvio e poi tolta vale «vuota». Rischio: che la rotazione della password non funzioni (R-865-1). L'ho provata con due processi veri che passano da `_carica_chiavi`. Primo passo: la scheda scritta con la vecchia password. Poi il `.env` cambiato e `scheda --forza` lanciato con la vecchia ancora esportata nell'ambiente: scrive con la nuova. Il «server», che ha ancora la vecchia nell'ambiente, risponde «invariata» e dopo un cambio dei dati riscrive con la nuova. Il PDF finale si apre solo con la nuova. Esito: ok, R-865-1 chiusa.
- `modules/crm/scheda.py:111` — controlla che la password della scheda sia diversa da quella delle copie cifrate. Rischio: che il confronto usi una fonte diversa da quella delle copie. Le copie cifrano con il valore dell'ambiente letto all'avvio (`modules/crm/copia_cifrata.py:78`, contesto). Il confronto invece usa il `.env` di adesso. Esito: riserva R-866-1.
- `modules/crm/scheda.py:283` — `_togli_scheda_vecchia` (R-865-2). La rimozione funziona (mutante L ucciso) e il test con gli spazi ai bordi uccide il mutante M. Ma scrive l'avviso «tolta» anche quando non c'era nessun file: 3 giri, 3 righe, cartella vuota. Esito: ok, con una cosmetica.
- `modules/crm/server.py:404` e `modules/crm/server.py:409` — riprova dopo un errore e controllo che la scheda precedente sia finita; ricontrollo giornaliero a `modules/crm/server.py:401`; avviso solo al cambio d'esito a `modules/crm/server.py:361`. Ho rifatto i tuoi mutanti e sono tutti uccisi: senza riprova, senza controllo del thread vivo, senza ricontrollo giornaliero, avviso a ogni esito, `>=` sulla data di oggi, senza rilettura del `.env`. Esito: ok, R-865-3 chiusa; R-865-4 chiusa per l'avviso del server.
- `tests/test_unit_crm.py:3529` — il test toglie `GAS_NO_DOTENV` e a `tests/test_unit_crm.py:3530` sposta `_RADICE` in una cartella temporanea. Rischio: che i test leggano il `.env` vero dell'operatore. `tests/conftest.py:11` (contesto) accende `GAS_NO_DOTENV` per tutta la suite, e nessun altro test del CRM lo spegne. Ho simulato il Mac: HOME finta con iCloud Drive, un `.env` con password nella radice del checkout, la password esportata nella shell, poi la suite CRM intera. 211 passed e iCloud finto vuoto. Esito: ok.
- `modules/crm/__main__.py:426` (contesto) — `_carica_chiavi` importa `gas` nel thread principale dentro `main()`, prima del parser e del server. Rischio: effetti collaterali dell'`import gas` fatto dal thread della scheda. Nel thread l'import trova il modulo già caricato e non riesegue nulla. Se il kernel non si importa, l'import viene riprovato a ogni lettura; fallisce sugli import iniziali di gas.py, prima che venga aperto il file di log (gas.py:66), quindi produce solo avvisi. Esito: ok.

**Rieseguito sulla copia dell'indice:** 211 passed su `tests/test_unit_crm.py`; mypy 0 errori dentro `modules/crm` (gli errori elencati stanno in gas.py, che mypy legge seguendo gli import); `git diff --cached --check` pulito; nessun IP letterale nel diff.

**Riserve**

- **R-866-1 BASSA** — Il confronto con la password delle copie (`modules/crm/scheda.py:111`) legge il `.env`, mentre le copie cifrano con il valore dell'ambiente all'avvio (`modules/crm/copia_cifrata.py:78`). Provato: ambiente con Z, `.env` cambiato con X, scheda con password Z → la scheda viene scritta con la stessa password che le copie usano davvero. Correzione: rifiutare se la password della scheda è uguale al valore del `.env` oppure a `copia_cifrata.password()`. Pesa poco: serve riusare la vecchia password delle copie, e le copie già fatte con quella restano comunque su iCloud.
- **R-866-2 BASSA** — Restano mutanti vivi:
  - H: senza il controllo di `GAS_NO_DOTENV` dentro `_leggi_env_file`. Sul Mac simulato fa fallire 9 test, quindi si vede; sul CI passa.
  - I: `_RADICE` calcolata con `parents[1]`. In produzione R-865-1 si riaprirebbe senza nessun test rosso. Basta un test che fissi `scheda._RADICE` uguale a `ROOT` di `__main__`.
  - G: chiave presente solo nell'ambiente, con il `.env` presente.
  - K: la riprova rimanda di un'ora un cambio dei dati già in attesa.
  - J è equivalente: il flag `scheda_riprova` non decide mai nulla.

**Cosmetiche**

- L'avviso «scheda clienti tolta» compare in gas_debug.log a ogni giro con le password uguali, anche senza file.
- `modules/crm/scheda.py:355` scrive un avviso a ogni riprova: con la riprova oraria sono 24 righe al giorno. R-865-4 è chiusa solo per l'avviso del server.
- Con il `.env` illeggibile, o con il kernel che non si importa, escono 5 avvisi a ogni giro.
- Da un terminale aperto prima della modifica, `scheda --forza` riscrive la scheda con la password tolta dal `.env` ma ancora esportata (come fa il kernel, ma il server la dà per spenta).
- Nel test l'ordine di ripristino (`delenv` prima di `setattr`) lascia un istante con `GAS_NO_DOTENV` spento e la `_RADICE` vera: va invertito.
- La guida dice che la scheda «viene tolta», ma succede solo al giro successivo (cambio dei dati, giro giornaliero, riavvio o `scheda`).

**Cosa NON ho verificato e perché**

- macOS vero non è riproducibile qui: launchd, accesso a iCloud Drive, e l'app File dell'iPhone che apre il PDF AES-256.
- La concorrenza su `CRMStore` dal thread della scheda non l'ho riprovata: accettata nel giro #865 e non toccata da questo diff.
- La password dentro `EnvironmentVariables` del plist è esclusa: lo script `scripts/crm/installa.sh` non la usa.

**Lezioni nuove in memoria (2)**

1. Un confronto tra due segreti va fatto contro la fonte che il modulo usa davvero (meglio contro entrambe le fonti).
2. Un nuovo lettore del `.env` con la sua barriera per i test va provato su un Mac simulato: sul CI, senza `.env`, il mutante «senza barriera» sopravvive sempre.

**File**
- `/home/user/Gas/.claude/agents/memoria_revisore.md` (riga #866, non staged, non committata)
- Script delle prove: `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/prove/diff_env.py`, `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/prove/mutanti.py`, `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/prove/sonde.py`, `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/prove/mac_finto.sh`

### Commit 3b8737b5 — review #867-MERGE (verdetto integrale)

## VERDETTO: APPROVATO

Review #867-MERGE: il merge in corso di origin/main 86a23f56 (PR #402, tetto di tempo duro del sottofondo) nel ramo claude/nifty-galileo-3k7kbm (PR #410, HEAD 07b0da7f) è a posto. Lo sha256 del diff dell'indice contro HEAD è cb2b2801…: coincide con quello dichiarato e la mia riga in memoria non l'ha cambiato. Indice: 4 file, +205/−1. Letti prima della review: CLAUDE.md (sezione 5, sezione 8, roadmap), la testa di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

**Cosa ho controllato nel diff**
1. `modules/sottofondo/__init__.py:821` — `_termina_processo`, e `modules/sottofondo/__init__.py:880` — `_scaduto` con lock e flag. Rischio esaminato: che la risoluzione abbia alterato il codice di main o mischiato righe del ramo. `git diff --cached MERGE_HEAD -- modules/sottofondo/__init__.py` è vuoto, quindi il file è identico a main. Il modulo non nomina mai «crm» né «scheda» (grep), quindi non tocca il CRM. Esito: ok.
2. `tests/test_unit_sottofondo.py:1493` — `test_tetto_e_fine_turno_un_solo_esito` (con gli altri test del tetto, da riga 1426). Rischio esaminato: test di main persi o tenuti in un modo che li rompe. Il file è identico a main (diff vuoto). Il `tests/conftest.py` del ramo aggiunge solo il delenv di `GAS_CRM_SCHEDA_PASSWORD` e non cambia il comportamento dei test del sottofondo: 348 passed (sottofondo + crm) e 51 passed (manutenzione) su una copia dell'indice estratta con `git checkout-index`. Esito: ok.
3. `.claude/agents/memoria_revisore.md:1762` — inizio delle righe aggiunte. Rischio esaminato: righe perse o duplicate. L'indice contiene le righe comuni (base) + le 5 righe di main + le 9 del ramo, in quest'ordine, confrontato a stringa: 0 righe perse da HEAD, 0 perse da main, 0 righe estranee. Esito: ok.
4. `reports/stato_progetto.md:4` (contesto, file di report).
   - La riga «Ultimo aggiornamento» è il frammento R7 di main, con «ancora aperta» cambiato in «MERGIATA il 25-11, 86a23f56», seguito dalla riga intera del ramo (uguaglianza verificata a stringa). Data e SHA tornano con `git log`.
   - C'è una sola riga `> Ultimo aggiornamento`.
   - Le altre righe di main che sembravano «perse» sono le righe Voce (393) e Dashboard (9), che solo il ramo aveva cambiato rispetto alla base: è giusto che resti la versione del ramo.
   - Esito: ok.
5. `reports/stato_progetto.md:406` (contesto). La riga R7 di main è intatta (933 caratteri, prefisso identico); in coda è aggiunta la V-1 COSMETICA. Ho riscontrato la V-1 nel check-run `verifica-bot` su af6e5078 (APPROVATA, success, una sola riserva COSMETICA sulla docstring). Regola 3 di `reports/lavoro_parallelo.md`:
   - l'unica «decisione umana» del lato main (il merge della #402) è già fatta;
   - le riserve R-852R7-1/2/4 e R-853R7-1/2/3 sono presenti nello stato.
   - Esito: ok.

**Controlli sul resto del merge**
- `git ls-files -u` è vuoto: non restano file in conflitto.
- Nessun marcatore di conflitto nei file staged, e `git diff --cached --check` è pulito.
- Nessun file non tracciato.
- `git diff --cached MERGE_HEAD --name-only`: l'indice differisce da main solo sui file della #410 (modules/crm/__main__.py, scheda.py, server.py, reports/crm/, requirements.txt, tests/conftest.py, tests/test_unit_crm.py), sulla memoria, sullo stato e sui tre log di sessione.
- Tutti i file della #410, compresi handoff/ultimo_report/diff_sessione, sono identici a HEAD. Il comportamento della #410 non cambia.
- Antipattern: il diff non taglia la storia dei messaggi e non simula l'output dei tool. Non indebolisce nessun guardrail (gas.py e brains non sono toccati da nessuno dei due lati).

**Cosa NON ho verificato**
- La suite completa del kernel (tests/test_unit_kernel.py) e le altre suite della CI non le ho rilanciate. gas.py e brains sono identici su entrambi i lati e il sottofondo è uguale a main, che è già passato in CI. Fa fede la CI sul commit di merge.
- La correttezza del tetto duro in sé non l'ho rivista: è stata già revisionata in #852-R7/#853-R7 e il codice arriva da main senza modifiche.
- Il comportamento su Mac o VPS: non riproducibile qui.

**Riserve:** nessuna.

**Memoria:** riga #867-MERGE aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree (fuori stage), nessuna lezione nuova. `scripts/commit_memoria_revisore.sh` NON eseguito, come avete chiesto (merge in corso). Il marcatore .claude/.review_ok NON è stato creato.

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_crm.py`: 195 → 211 passed. Nuovi: 16 test della scheda e del guardiano (cifratura e nessun dato in chiaro, password propria/corta/uguale/cambiata nel `.env`/tolta, riscrittura solo su cambio, file tolto, temporanei vecchi, stornati e movimenti futuri esclusi, ultimi 3 movimenti, mese del profitto, demo che non scrive, comando che esce 1, guardiano con riprova, mai due insieme, ricontrollo giornaliero).
- `tests/conftest.py`: toglie anche `GAS_CRM_SCHEDA_PASSWORD`.
- Suite del kernel non toccata.

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST.
- Mappatura commit→run:
  - `36587824`: nessuna run propria (pushato con 07b0da7f).
  - `07b0da7f`: handoff-check success, verifica-bot success (APPROVATO CON RISERVE, solo BASSE/COSMETICHE), unit-suite in corso alla scrittura; PR poi in conflitto con main.
  - `3b8737b5` (merge di main) e commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.
- Ultima run nota su main b7182a7c (merge della #405): CI verde al merge.

## §7 RISERVE APERTE

- R-866-1 BASSA, R-866-2 BASSA, R-864-7 BASSA, cosmetiche #864–#866: in `reports/stato_progetto.md`.
- Dalla #410: V-2 BASSA del bot (lock solo dentro un processo), V-3 BASSA della verifica (entropia della password), V-3 bot e V-5 verifica COSMETICHE: in `reports/stato_progetto.md`.
- Dalla PR #406 (bot e verifica esterna) e dalle fette precedenti del CRM: in `reports/stato_progetto.md`.
- Dalla chat Voce (#405): V-1/V-2 BASSE dell'ultimo verdetto del bot e le riserve già registrate, in `reports/stato_progetto.md`.
- Scheda non provata su iPhone e iCloud veri.
