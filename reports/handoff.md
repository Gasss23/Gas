# HANDOFF — Dossier di fine sessione

**Sessione:** 25 novembre 2026 — R7 fetta 4 bis: tetto di tempo duro del giro di notte (sotto-chat di M1) — terzo giro: merge di main dopo la #410, via al merge dell'operatore

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #408 (https://github.com/Gasss23/Gas/pull/408), etichetta «verifica». L'operatore ha detto «mergia 408» (riferito da M1): dopo CI e bot verdi sull'head nuovo, senza finding ALTA/MEDIA nuovi, la mergia l'agente.
2. PR #402 (fetta 4, sottofondo): mergiata da M1 col «mergia» dell'operatore (25/11).

Numero della PR preso dall'output di `gh api repos/Gasss23/Gas/pulls` (POST, creazione): `408` (il primo tentativo di creazione nello script non aveva restituito il numero; ricreata a mano) (`gh pr` non disponibile in questo ambiente, solo REST).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 4 bis R7 — tetto di tempo duro del giro di notte**: FATTA. Timer a GAS_NOTTE_MAX_SEC_GIRO + 300 s: avviso «INTERROTTO» e arresto del processo; un solo avviso tra timer e fine giro; nome del compito appeso nel log; attesa limitata a 30 giorni. Review #866-R7 → #867-R7.
- **Merge di origin/main dopo la #402 (secondo giro)**: FATTO (fa2fc877), conflitti solo nei report (regola 3). Review #868-MERGE-R7 APPROVATO. notte + sottofondo: 375 passed.
- **Merge di origin/main dopo la #410 (terzo giro)**: FATTO (6d5adc51), conflitti solo nei report (regola 3). Review #869-MERGE-R7 APPROVATO CON RISERVE: R-869M-1 MEDIA (voce «R7 fetta 4» doppia in `stato_progetto.md`) corretta prima del commit del merge. notte + sottofondo + crm: 586 passed.
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA — prossima PR.

---

## §2 GIT DIFF --STAT (sessione)

```
.claude/agents/memoria_revisore.md |   6 ++++++
 modules/notte/notte.py             |  78 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  17 ++++++----------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  34 +++++++++++++------------------
 tests/test_unit_notte.py           | 110 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
6d5adc51 Merge origin/main (PR #410, CRM) nel ramo della PR #408 — review #869-MERGE-R7 APPROVATO CON RISERVE (voce doppia in stato_progetto tolta)
2cd5c14a docs(fine-task): PR #408 secondo giro — merge di main dopo la #402, review #868-MERGE-R7, verifica esterna
fa2fc877 Merge origin/main (PR #402 mergiata) nel ramo della PR #408 — review #868-MERGE-R7 APPROVATO
aa8e56ce docs(fine-task): R7 fetta 4 bis — numero della PR #408 nei report (lo script di creazione non l'aveva restituito)
adfe10a3 docs(fine-task): R7 fetta 4 bis — report, handoff con review #866-R7/#867-R7, stato_progetto
76655c0a feat(notte): R7 fetta 4 bis — tetto di tempo duro del giro di notte
336e9064 chore(revisore): memoria review #867 — APPROVATO CON RISERVE
8b7bea3b chore(revisore): memoria review #866 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 76655c0a (motore): review #866-R7 sul primo staged e #867-R7 dopo le correzioni di R-866R7-2/3/4. Merge fa2fc877: review #868-MERGE-R7. Merge 6d5adc51: review #869-MERGE-R7. Incollati integrali.

### Review #866-R7

## VERDETTO: APPROVATO CON RISERVE

Review #866-R7. Branch `claude/r7-tetto-duro-notte`, diff staged sopra b7182a7c: 2 file, +109/−0, sha256 del diff fe1bd29b. Ho letto CLAUDE.md, la memoria del revisore (comprese le riserve #852-R7 e #853-R7 della PR #402, gemella sul sottofondo) e lo stato del progetto, quest'ultimo solo nelle parti su R7.

**Cosa ho provato**
- **Suite**: `pytest tests/test_unit_notte.py` dà 235 passed.
- **Prova reale**: l'ho fatta in un processo separato. Ho messo MIN_SEC e MARGINE_DURO_S a 1 e GAS_NOTTE_MAX_SEC_GIRO=2, con un kernel finto che resta appeso e lancia due `sleep`.
  - Esito: rc 1 in 3 s.
  - Il messaggio «Giro notturno interrotto: tetto di tempo duro…» esce a schermo e nel log.
  - Il lock viene liberato: il giro successivo è partito subito.
  - Il compito appeso resta in `.gas_notte/in_corso.json` con tentativi 1, e il giro dopo lo riprende per primo.

**Elementi del diff esaminati**
1. `modules/notte/notte.py:993` — `_arma_tetto_giro`: `threading.Timer` demone. Rischio esaminato: overflow del timeout. Esito: riserva (R-866R7-3).
2. `modules/notte/notte.py:1008` — `_giro_scaduto`: log, avviso Telegram «INTERROTTO» col testo fisso, poi `_termina_giro` nel finally. Rischi esaminati: un'eccezione nell'avviso non deve impedire l'arresto (ok, provato dal test `tests/test_unit_notte.py:2898`); testo del modello nel messaggio (ok: solo la costante TETTO_DURO_NOTTE).
3. `modules/notte/notte.py:1105` — il timer si arma dopo `max_giro`, a max_giro + 300 s. Rischio esaminato: le fasi prima del ciclo restano scoperte. Esito: ok, sono trascurabili (catalogo e riprese, niente modello).
4. `modules/notte/notte.py:1189` — `cancel()` nel finally, prima di chiudere il lock e prima del riepilogo Telegram. Rischio esaminato: corsa con la fine normale. Esito: riserva (R-866R7-2).
5. `modules/notte/notte.py:1001` — `_termina_giro` = `os._exit(1)`. Rischi esaminati:
   - flock: ok, provato.
   - in_corso.json: ok, la scrittura è atomica con tmp + replace.
   - figli: riserva (R-866R7-1).
6. `tests/test_unit_notte.py:2873` e `tests/test_unit_notte.py:2885` — il timer viene tolto sia a fine giro sia nel giro che si rompe. `tests/test_unit_notte.py:2919` prova un timer vero. Esito: ok.

**Finding**
- **R-866R7-1 BASSA — i figli sopravvivono a `os._exit`.** L'ho provato: sia `sleep` nello stesso gruppo sia `sleep` con sessione propria restano vivi.
  - Sotto launchd il gruppo del job dovrebbe morire alla chiusura (non verificato sul Mac). Però `claude -p` (`brains/claude_cli.py:428`) e il browser (`modules/web/browser.py:496`) hanno una sessione propria e sopravvivono comunque.
  - Un `claude -p` rimasto orfano può sovrapporsi al giro successivo, perché il lock è già libero.
  - La docstring di `_termina_giro` non lo dice. Va dichiarato, oppure va fatto un killpg dei gruppi noti.
- **R-866R7-2 BASSA — nessuna mutua esclusione tra il timer e la fine normale.** È la stessa riserva R-852R7-2 della PR #402.
  - Se il timer scatta tra la fine del ciclo e il `cancel` (`modules/notte/notte.py:1189`), arrivano sia «INTERROTTO» sia il riepilogo, oppure `os._exit` cade a metà riepilogo.
  - `cancel()` non ferma un timer che è già dentro l'invio Telegram (fino a 15 s per ID). Il thread principale può quindi chiudere e mandare anche il riepilogo normale.
  - La finestra è stretta.
- **R-866R7-3 BASSA — tetto duro spento in silenzio con valori enormi.** È la stessa riserva R-852R7-3.
  - Con GAS_NOTTE_MAX_SEC_GIRO ≥ ~9,2e9 il thread del Timer va in OverflowError e il tetto duro si spegne senza dirlo. L'ho provato: 9,0e9 regge, 9,3e9 muore con «timestamp out of range».
  - `_env_secondi` (`modules/notte/notte.py:248`) non ha un tetto alto.
  - Correzione: `min(secondi, limite)` in `_arma_tetto_giro`. Attenzione a R-853R7-1: se si tronca il tempo, il messaggio non deve diventare falso.
- **R-866R7-4 BASSA — il tetto per compito resta morbido, e i compiti ripresi partono per primi.**
  - Un compito che si appende sempre brucia l'intera notte (2 h 05) per MAX_TENTATIVI = 3 notti di fila. Gli altri compiti in quelle notti non girano.
  - Né il messaggio «INTERROTTO» né la riga di log nominano il compito appeso. Il nome viene dal catalogo dell'operatore, non dal modello, quindi si può almeno scrivere nel log.
  - Il limite è dichiarato come tetto morbido, ma l'effetto «3 notti perse» non è scritto da nessuna parte.
- **COSMETICA**: l'invio Telegram dentro il timer non ha un tetto proprio. Il timeout di urlopen è per singola fase e non copre il DNS, quindi un avviso appeso ritarda `os._exit`. Correzione possibile: un secondo timer di sicurezza su `os._exit`.

**Cosa NON ho verificato**
- Il comportamento sotto launchd sul Mac (se il gruppo del job viene ucciso quando il job finisce): da qui non si riproduce.
- L'invio Telegram vero: l'ho spento con GAS_NOTTE_TELEGRAM=0 e mi sono affidato al test con `invia_notifica` finto.
- Nessun mutante sui test nuovi, per tempo.

**Memoria**: riga #866-R7 e una lezione nuova aggiunte in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole (8b7bea3b). Lo staging del diff è intatto.

**Note per te**
- Le riserve 1-3 coincidono con quelle già aperte sulla PR #402: conviene chiuderle insieme nelle due fette.
- Vanno tracciate in `reports/stato_progetto.md`.
- Il marcatore della review non l'ho creato io: lo crei tu con `bash scripts/segna_review_ok.sh`.

### Review #867-R7

## VERDETTO: APPROVATO CON RISERVE

Review #867-R7: secondo giro di #866-R7. Il diff staged è su `claude/r7-tetto-duro-notte`, sopra 8b7bea3b: 2 file, +188/−0, sha256 del diff f5efbcf6. Tre riserve su quattro sono chiuse e la quarta è dichiarata nel codice; resta aperta una riserva BASSA nuova.

**Riserve di #866-R7**

| Riserva | Esito | Dove |
|---|---|---|
| R-866R7-2 | chiusa | `modules/notte/notte.py:1014`, `modules/notte/notte.py:1020`, `modules/notte/notte.py:1222` |
| R-866R7-3 | chiusa | `modules/notte/notte.py:994`, `modules/notte/notte.py:122` |
| R-866R7-4 | chiusa per il log; limite delle 3 notti dichiarato | `modules/notte/notte.py:1155` |
| R-866R7-1 | dichiarata (figli non fermati) | docstring di `_termina_giro` |

**Cosa ho rifatto io**
- **Suite:** `pytest tests/test_unit_notte.py` passa (238 passed).
- **Prova reale**, in un processo separato con kernel appeso e Telegram spento:
  - rc 1 in 3 s;
  - nel log compare «tetto di tempo duro del giro superato: processo fermato (compito in corso: appeso)».
- **Mutanti: 4 su 4 uccisi** (lo staging è intatto). Ciascuno fa fallire un test r7f4:
  - `da_notificare` non azzerato nel finally;
  - il finally non prende il flag;
  - il timer ignora il flag;
  - il tetto dei 30 giorni tolto.

**Elementi del diff esaminati**
1. `modules/notte/notte.py:994` — `_arma_tetto_giro` limita l'attesa a `min(max(0, s), 30 giorni)`. Rischio esaminato: OverflowError nel thread del Timer. Esito: ok; lo prova `tests/test_unit_notte.py:2961` con 1e12.
2. `modules/notte/notte.py:1020` — `_giro_scaduto` controlla e alza il flag sotto lock prima di avvisare e chiudere. Rischio esaminato: un timer in ritardo dopo la fine del giro. Esito: ok, esce senza fermare il processo (seconda parte di `tests/test_unit_notte.py:2927`).
3. `modules/notte/notte.py:1222` — il finally fa `cancel`, poi prende il flag sotto lock. Se il timer è già partito, non manda il riepilogo e aspetta con `tetto_duro.join(60)` (`modules/notte/notte.py:1227`).
   - Rischio esaminato: corsa fra `cancel` e un timer già in attesa del lock. Esito: ok, chi prende il lock per primo vince.
   - Rischio esaminato: l'invio dell'avviso dura più dell'attesa. Esito: riserva R-867R7-1.
4. `modules/notte/notte.py:1155` — il nome del compito viene salvato nella guardia prima di segnarlo in in_corso.json. Rischio esaminato: testo non fidato nel log. Esito: ok, il nome viene dal catalogo dell'operatore. Vedi però la COSMETICA sul nome che resta dopo il ciclo.
5. `tests/test_unit_notte.py:2927` — il timer scatta mentre il compito gira: arriva un solo avviso, «INTERROTTO», e niente riepilogo. Poi un giro normale con un timer tardivo: il processo non si ferma. Esito: ok, e uccide i mutanti 1-3.

**Riserve nuove**
- **R-867R7-1 BASSA:** succede quando il timer ha già preso il flag e l'invio Telegram nel thread del timer dura più di 60 s (`tetto_duro.join(60)`, `modules/notte/notte.py:1227`; per esempio DNS appeso: il timeout di urlopen non lo copre).
  - Effetto: il finally ritorna con l'esito calcolato, anche rc 0, e lo spegnimento dell'interprete congela il thread demone.
  - Risultato: né «INTERROTTO» né riepilogo, cioè proprio il silenzio che V-1 bot #169 voleva evitare.
  - La finestra è stretta: serve lo scatto nella fase finale più Telegram lento.
  - Correzione possibile: dopo il join scaduto, rc 1 e `_termina_giro()` direttamente, oppure un join senza limite.
- **COSMETICA:** `guardia["compito"]` resta sull'ultimo compito anche dopo il ciclo. Se il blocco è nella fase finale (firme, stato del mattino), il log dice «compito in corso: X» con X già finito.
- **COSMETICA:** con GAS_NOTTE_MAX_SEC_GIRO oltre 30 giorni, «tetto duro superato» arriva a 30 giorni, cioè prima del tetto vero (analoga a R-853R7-1).

**Rischi non verificati**
- Il comportamento sotto launchd sul Mac (figli in sessione propria): non riproducibile qui.
- L'invio Telegram vero: provato solo con `_notifica_telegram` finto e GAS_NOTTE_TELEGRAM=0.
- La corsa reale fra due thread, con il timer che scatta durante il finally: verificata leggendo il codice e con il test sincrono, non con thread veri.

**Memoria:** ho aggiunto la riga #867-R7 a `/home/user/Gas/.claude/agents/memoria_revisore.md` e l'ho committata da sola (336e9064); nessuna lezione nuova.

**Cosa resta a te**
- Tracciare R-867R7-1 e le COSMETICHE in `reports/stato_progetto.md`.
- Creare il marcatore con `bash scripts/segna_review_ok.sh`: io non l'ho creato.

### Review #868-MERGE-R7 (merge fa2fc877)

## VERDETTO: APPROVATO

Revisione del merge in corso di origin/main (porta la PR #402, R7 fetta 4: tetto duro del sottofondo) nel ramo claude/r7-tetto-duro-notte (PR #408). Rispetto a HEAD sono in stage 4 file, +206/−2.

**Elementi esaminati**
- `modules/notte/notte.py:994` — `_arma_tetto_giro`, il timer demone del tetto duro del giro, con attesa limitata a 30 giorni (R-866R7-3). Rischio: che il merge abbia toccato o alterato la fetta 4 bis. Il diff staged contro HEAD su modules/notte, gas.py e brains è vuoto, quindi il codice è identico a quello revisionato in #867-R7. Esito: ok.
- `modules/notte/notte.py:1003` — `_termina_giro` (os._exit, docstring con i limiti R-866R7-1/4) e `_nuova_guardia` alla riga 1014. Rischio: che il sottofondo portato da main la condivida o la richiami. Un grep incrociato non trova riferimenti a «notte» in modules/sottofondo/__init__.py né a «sottofondo» in notte.py: sono due timer indipendenti, in processi diversi. Esito: ok.
- `tests/test_unit_notte.py:2898` — `test_r7f4_tetto_duro_scaduto_avvisa_e_ferma`, con le altre prove r7f4 alle righe 2873 e 2885. Rischio: che il merge abbia perso dei test. tests/test_unit_notte.py coincide con HEAD; notte + sottofondo danno 375 passed. Esito: ok.
- Contesto, `modules/sottofondo/__init__.py:880` e `tests/test_unit_sottofondo.py` — il codice portato dalla PR #402. Rischio: una divergenza da main. Il diff staged contro origin/main su questi due file è vuoto, quindi sono identici a main, già revisionato in #852-R7, #853-R7 e #864-MERGE-R7. Esito: ok.

**Conflitti**
- Nessun file ancora in conflitto (`git ls-files -u` vuoto) e 0 marcatori di conflitto in stato_progetto, memoria e handoff.
- handoff, ultimo_report e diff_sessione: diff staged contro HEAD vuoto, quindi tenuti dal ramo (regola 3).
- reports/stato_progetto.md: c'è una sola riga «Ultimo aggiornamento», nell'ordine fetta 4 bis (PR #408), poi fetta 4 «PR #402 mergiata», poi il resto di main. «Ancora aperta» è stato aggiornato in «mergiata», il che è corretto. Le voci della fetta 4 e della 4 bis ci sono entrambe. Contro origin/main l'unica differenza è la voce 4 bis più la riga di aggiornamento.
- Memoria del revisore: è l'unione delle due versioni. Non manca nessuna riga di HEAD né di main e non ce ne sono di estranee.

**Rischio escluso**: non ho rifatto prove reali in processi separati (timer, os._exit, figli) né mutanti, perché il codice è identico byte per byte a quello già provato in #852-R7, #853-R7, #866-R7 e #867-R7. Restano aperte le riserve già tracciate (R-852R7-1, R-853R7-1/2/3, R-866R7-1/4, R-867R7-1).

**Memoria**: ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga `#868-MERGE-R7 — 2026-11-25 — APPROVATO — … Nessuna lezione nuova.` Il numero 868 è il primo libero dopo #867-R7. La riga è solo nel working tree, NON in stage e NON committata. Non ho lanciato commit_memoria_revisore.sh, come hai chiesto. Nota: la versione della memoria già in stage (quella unita) resta nell'index, mentre la nuova riga è solo su disco. Prima di committare il merge va fatto `git add` della memoria.

### Review #869-MERGE-R7 (merge 6d5adc51)

## VERDETTO: APPROVATO CON RISERVE

Review #869-MERGE-R7 (chat Motore, sotto-chat R7). Ho esaminato il merge in corso di origin/main 5a0f9dbc (PR #410, chat CRM, scheda clienti offline) in claude/r7-tetto-duro-notte (PR #408). Il diff staged rispetto a HEAD tocca 10 file, +799/−3.

**Riserva da correggere PRIMA di `segna_review_ok.sh`**
- **R-869M-1 (MEDIA, documentazione)**: in `reports/stato_progetto.md` la voce «R7 fetta 4 — tetto di tempo duro del compito in sottofondo» compare **due volte**, alle righe 407 e 408 della versione in stage.
  - La riga 407 è quella del ramo (945 caratteri).
  - La riga 408 è quella di main: identica alla 407 più la coda «PR #402 MERGIATA il 25-11 (86a23f56); … V-1 COSMETICA — docstring di `_termina_processo`…».
  - Come correggere: togliere la riga 407 e tenere la 408. Va fatto prima di `segna_review_ok.sh`, perché cambia lo SHA del diff in stage.
  - Il file è fuori dal perimetro e la correzione non tocca codice, quindi non serve un nuovo giro di review se cambia solo questo. Lo SHA però cambia: il marcatore va creato dopo la correzione.

**Elementi esaminati**
- `modules/notte/notte.py:994`: `_arma_tetto_giro` della fetta 4 bis. Rischio: il merge ha toccato il tetto duro o la PR #410 lo usa. Il diff tra stage e HEAD su `modules/notte/notte.py` è vuoto, e `grep crm|scheda` in `modules/notte/` non trova niente. Esito: ok.
- `modules/notte/notte.py:1014`: `_nuova_guardia`, cioè la guardia lock+flag tra il timer e la fine normale. Riguarda R-866R7-2, chiusa in #867-R7. Rischio: la chiusura persa nella risoluzione dei conflitti. Il codice è uguale a HEAD e le righe 1020 (`_giro_scaduto`) e 1222 (`if gia_scaduto:`) sono intatte. Esito: ok.
- `tests/test_unit_notte.py:2898`: `test_r7f4_tetto_duro_scaduto_avvisa_e_ferma`. Rischio: i test della 4 bis persi o alterati, oppure rotti dal nuovo `tests/conftest.py`. Il diff rispetto a HEAD è vuoto e i test passano. Esito: ok.
- `tests/conftest.py`: aggiunge solo `delenv("GAS_CRM_SCHEDA_PASSWORD")` (R-864-2), identico a origin/main. Rischio: effetti sui test di notte e sottofondo. Nessuno, perché toglie una variabile segreta e basta. Esito: ok.
- Codice portato da main: `modules/crm/__main__.py`, `modules/crm/scheda.py`, `modules/crm/server.py`, `requirements.txt`, `tests/test_unit_crm.py`, `reports/crm/decisioni.md`, `reports/crm/guida.md`. Per tutti il diff tra stage e origin/main è vuoto, quindi sono identici a main. `modules/crm/` non nomina `notte`. Esito: ok.

**Conflitti**
- `git ls-files -u` è vuoto, non ci sono marcatori di conflitto e `git diff --cached --check` è pulito.
- `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md` sono uguali a HEAD (diff vuoto), come chiede la regola 3.
- Le decisioni e le riserve dell'ultimo_report di main sono già nello stato in stage:
  - `GAS_CRM_SCHEDA_PASSWORD`;
  - `pip install -r requirements.txt`;
  - «Mantieni scaricato» sull'iPhone e `scheda --forza`;
  - `telefono.sh`;
  - R-866-1, R-866-2 e R-864-7;
  - per la Voce #405: R-854-1, la licenza CC BY-NC-SA e la V-1 BASSA `modello_della_parola`.
- C'è una sola riga «Ultimo aggiornamento», unita correttamente: la voce «4 bis» del ramo, poi «PR #402 MERGIATA il 25-11, 86a23f56», poi la scheda clienti (decisione 22) e il resto di main.
- Memoria del revisore: è l'unione dei due lati. Nessuna riga persa né da HEAD né da main, nessuna riga estranea. L'ordine è base, poi le righe di main (#864–#866, #867-MERGE), poi quelle del ramo (#866-R7, #867-R7, #868-MERGE-R7).

**Test**
- `pytest` su `tests/test_unit_notte.py`, `tests/test_unit_sottofondo.py` e `tests/test_unit_crm.py`: 586 passed (375 notte + sottofondo, 211 crm).

**Cosa NON ho verificato**
- Il funzionamento reale della scheda PDF su iCloud e iPhone: non si riproduce in questo ambiente, ed era già escluso nelle review #864–#866 della chat CRM.
- Il codice della #410 non l'ho rivisto nel merito: era già stato revisionato lì. Ho controllato solo che sia identico a origin/main.
- Non ho rilanciato la suite completa: solo le tre suite qui sopra.

**Memoria del revisore**
- Ho aggiunto la riga contatore #869-MERGE-R7, con una lezione nuova: contare le intestazioni delle voci dello stato su HEAD, main e indice per trovare i duplicati da merge ripetuti.
- La memoria è rimasta nel working tree, **non in stage e non committata**, come richiesto durante il merge: va aggiunta allo stage insieme al resto.
- File: /home/user/Gas/.claude/agents/memoria_revisore.md

File rilevanti: /home/user/Gas/reports/stato_progetto.md (righe 407–408 nella versione in stage), /home/user/Gas/modules/notte/notte.py, /home/user/Gas/tests/test_unit_notte.py

## §5 DELTA TEST DEL MOTORE

- Dopo il merge 6d5adc51: notte + sottofondo 375 passed (revisore: + crm, 586 passed).
- Dopo il merge fa2fc877: notte + sottofondo 375 passed.
- `tests/test_unit_notte.py`: 230 → 238 (8 test nuovi), tutti verdi in locale: `238 passed in 5.22s`.
- `tests/test_unit_kernel.py` non rieseguito: il diff tocca solo `modules/notte/notte.py` e i suoi test. Il revisore ha fatto una prova reale con processo separato e kernel appeso (rc 1 in 3 s, messaggio nel log, lock liberato, compito in in_corso.json).

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura:

```
in_progress		Merge pull request #410 from Gasss23/claude/nifty-galileo-3k7kbm	CI	main	push	45669536431	8m32s	2026-11-25T17:53:52Z
completed	success	Mani alla voce: piano + formato fisso dei commenti ESITO/COMANDO (F2)	verifica-bot	claude/mani-voce-piano	pull_request_target	45659374696	3m15s	2026-11-25T16:56:38Z
completed	success	docs(fine-task): report e handoff dopo il merge di main (PR #409)	CI	claude/mani-voce-piano	push	45659361079	10m48s	2026-11-25T16:56:33Z
```

Run di questo branch (`gh api .../actions/runs?branch=claude/r7-tetto-duro-notte`, output reale):

```
45652810690 2cd5c14a verifica-bot pull_request_target completed/success
45652795085 2cd5c14a CI push completed/success
45652195774 aa8e56ce verifica-bot pull_request_target completed/failure
45652195333 aa8e56ce verifica-bot pull_request_target completed/cancelled
45652192077 aa8e56ce CI push completed/success
45652144236 adfe10a3 verifica-bot pull_request_target completed/skipped
45652118621 adfe10a3 CI push completed/success
45651971850 76655c0a CI push completed/failure
```

Mappatura commit→run: le righe sopra danno per ogni SHA le run reali. 2cd5c14a: CI success, verifica-bot success (APPROVATO CON RISERVE, solo BASSE). 6d5adc51: nessuna run propria. Commit di fine-task di questo giro: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Bot su 2cd5c14a (APPROVATO CON RISERVE): V-1 BASSA (docstring in testa a `modules/notte/notte.py` dice ancora «tetto non duro»), V-2 BASSA (se l'invio Telegram del timer si appende il processo non si ferma), V-3 BASSA (manca un test sulla finestra dopo l'ultimo compito). Aperte.
- R-869M-1 MEDIA (voce doppia in `stato_progetto.md`): CHIUSA prima del commit del merge.
- R-867R7-1 BASSA — timer già partito e invio Telegram oltre 60 s (es. DNS appeso): il giro può finire senza «INTERROTTO» né riepilogo. Aperta.
- COSMETICHE #867-R7: il nome del compito resta dopo il ciclo (log «compito in corso» sbagliato se il blocco è nella fase finale); con GAS_NOTTE_MAX_SEC_GIRO oltre 30 giorni il tetto scatta a 30 giorni. Aperte.
- R-866R7-1 BASSA (dichiarata nel codice): figli `claude -p` e browser non fermati. Limite dichiarato: un compito sempre appeso consuma il giro per 3 notti. R-866R7-2/3/4: CHIUSE.
- Verifica esterna su aa8e56ce ([commento](https://github.com/Gasss23/Gas/pull/408#issuecomment-7167771617), pubblicato dall'agente principale: l'agente di verifica aveva 502): V-1 MEDIA di processo (PR in conflitto dopo il merge della #402) CHIUSA col merge fa2fc877; V-2 BASSA (#402 data per aperta) CORRETTA; V-3 BASSA (CI non tutta verde su aa8e56ce) superata dal nuovo head; V-4 BASSA = R-866R7-1.
- PR #402 (sottofondo, mergiata): riserve in `reports/stato_progetto.md`.
