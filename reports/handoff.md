# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-25 — Mani alla voce: piano + formato fisso dei commenti ESITO/COMANDO (F2) + due correzioni dopo bot/verifica esterna + merge di main, PR #409

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #409 (https://github.com/Gasss23/Gas/pull/409). Revisore #868 APPROVATO sull'ultima correzione, ma verifica esterna APPROVATO CON RISERVE (solo BASSE) e bot sul head 0b039727 APPROVATO CON RISERVE (check success, solo BASSE/COSMETICHE); dopo il merge di main servono di nuovo CI e bot sul nuovo head: il merge lo decide l'operatore (CLAUDE.md §10).
2. F1: a voce `richiedi_sviluppo` passa dalla firma su Telegram? (proposta: sì).
3. Canale dell'avviso: commenti sulla issue letti da Gas sul Mac (proposta) oppure Telegram diretto dal cloud.
4. F5: frequenza e ore della scheduled task (proposta: ogni ora, 8-20, feriali), massimo 2 richieste al giorno, modello.
5. Con `MERGIA #N` mergia l'esecutore (proposta) oppure resta M1.

---

## §1 SCOPE & ESITO FETTE

- **Piano (`reports/mani_voce_piano.md`)**: `FATTA` — cosa esiste, cosa manca, fette F1-F5, rischi, decisioni. Inviato in sintesi a M1.
- **Punto 4 — compiti non di sviluppo a voce**: `FATTA` (verifica senza modifiche) — percorso coperto da `tests/test_unit_sottofondo.py`; manca la prova sul Mac.
- **F2 — formato fisso ESITO/COMANDO**: `FATTA` — `modules/sviluppo/esiti.py` + `tests/test_unit_esiti.py` (46 test), revisore #864 → #865 APPROVATO CON RISERVE.
- **Correzione dopo bot e verifica esterna**: `FATTA` — caratteri bidi veri tolti dai test (causa del bot rosso), VERIFICA_ESTERNA a valori fissi, riempitivi vuoti tolti (R-865-1), piano corretto; revisore #866 APPROVATO.
- **Seconda correzione dopo il bot (finding MEDIA sul head 35c67d25)**: `FATTA` — domanda di merge solo con PR valida, CI verde, bot APPROVATO/APPROVATO CON RISERVE e verifica esterna nell'elenco e non BOCCIATO; riserve vuote scartate e in più contate; revisore #867 → #868 APPROVATO. 61 test.
- **Merge di main (PR #402, R7 fetta 4)**: `FATTA` — conflitti solo nei report e nella memoria, risolti con la regola 3 di `reports/lavoro_parallelo.md`; revisore #869-MERGE APPROVATO.
- **F1 — firma a voce per `richiedi_sviluppo`**: `DEFERITA — aspetta il via dell'operatore`.
- **F3 — Gas legge gli esiti dalle issue**: `DEFERITA — aspetta il via dell'operatore`.
- **F4 — «mergia N» da Telegram**: `DEFERITA — aspetta il via dell'operatore`.
- **F5 — esecutore come scheduled task cloud**: `DEFERITA — spesa ricorrente e credenziali, aspetta il via`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   8 ++++++++
 modules/sviluppo/esiti.py          | 233 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  14 ++++++++------
 reports/handoff.md                 | n/d
 reports/mani_voce_piano.md         | 123 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  32 ++++++++++++++++++++------------
 tests/test_unit_esiti.py           | 181 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
08875514 merge: origin/main (PR #402, R7 fetta 4) in claude/mani-voce-piano
0b039727 docs(fine-task): report e handoff — seconda correzione dopo il bot (PR #409)
13eaa1a2 fix(sviluppo): domanda di merge solo con tutti i controlli buoni, riserve vuote scartate e in più contate (bot #409-bis, R-867-1/2)
4606d48c chore(revisore): memoria review #868 — APPROVATO
edb5de4f chore(revisore): memoria review #867 — APPROVATO CON RISERVE
35c67d25 docs(fine-task): report e handoff aggiornati — correzione dopo bot e verifica esterna (PR #409)
3f7a0075 fix(sviluppo): niente caratteri bidi veri nei test, VERIFICA_ESTERNA a valori fissi, riempitivi vuoti tolti (bot #409, R-865-1)
a8ab5efd chore(revisore): memoria review #866 — APPROVATO
ec8a1d7a docs(fine-task): report e handoff — mani alla voce, piano + F2 (PR #409)
81c751fa feat(sviluppo): formato fisso dei commenti ESITO/COMANDO sulle issue delle richieste (mani alla voce F2)
62a1adcc chore(revisore): memoria review #865 — APPROVATO CON RISERVE
0656fc0d chore(revisore): memoria review #864 — APPROVATO CON RISERVE
93090a56 docs(mani-voce): piano per dare le mani alla voce (esecutore richieste, avvisi, merge)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore 81c751fa: verdetto integrale del secondo giro (#865), che copre il codice di quel commit (il primo giro #864 era su una versione precedente, poi corretta). Commit motore 3f7a0075: verdetto #866, riemesso dal revisore con gli escape scritti come testo (la prima emissione conteneva un carattere U+202E vero che avrebbe fatto fallire il bot); stessa sostanza ed esito. Commit motore 13eaa1a2: verdetti #867 (APPROVATO CON RISERVE, con R-867-1 e R-867-2) e #868 (APPROVATO, dopo la correzione di quelle due riserve nello stesso diff staged). Le righe citate dai verdetti più vecchi si riferiscono al file del loro commit: dopo i commit successivi alcune sono slittate.

## VERDETTO: APPROVATO CON RISERVE

**Cosa ho rivisto.** È il secondo giro della review #864, sul diff ora in staging nel ramo claude/mani-voce-piano: 2 file, +326 righe. Le impronte (sha256) coincidono con quelle che mi hai dato:
- diff in staging: 3f81f5d911221204ddfb7492e2b3529eedd566b94feafebb5a24a939d57a2587
- `modules/sviluppo/esiti.py` in staging: 497c743794eea4f6fd89d5cffa27c58a750638c157756167373184a569eeaace
- `tests/test_unit_esiti.py` in staging: 3c7d40cc36951117b2dcb6a1d9185525a456aba84cb7138e74ee99d9e5ea65dc

Ho fatto girare i test su una copia esatta dei file in staging: 46 passed.

**Mutanti** (piccole modifiche al codice per vedere se i test se ne accorgono): 4 su 4 presi.
- Filtro ridotto da tutte le categorie C* ai soli caratteri di controllo (Cc): 6 test falliti.
- «assente» tolto dalla condizione del merge: 1 fallito.
- Controllo della CI tolto: 2 falliti.
- Righe vuote scartate dopo il taglio a 5 invece che prima: 1 fallito.

Nessun taglio della storia dei messaggi con `[-N:]` nel diff.

**Elementi del diff esaminati**
- `modules/sviluppo/esiti.py:53` — `_pulisci` sostituisce con uno spazio ogni carattere di categoria Unicode C*, come `scripts/bot_esito.py:303`. Rischio esaminato: invisibili che nascondono testo. U+FEFF, U+2060, U+00AD, il carattere «tag» U+E0041, U+202E e U+200D vengono tolti, e U+2028 diventa spazio. Esito: ok, **R-864-1 chiusa**.
- `modules/sviluppo/esiti.py:166` — la domanda «Vuoi che la mergi?» compare solo con CI verde e bot né BOCCIATO né assente; negli altri casi la frase dice «Controlli non verdi: niente merge per ora.». Provato: CI verde con bot BOCCIATO dà «niente merge», CI verde con bot APPROVATO fa la domanda. Esito: ok, **R-864-2 chiusa**.
- `modules/sviluppo/esiti.py:136` — `riserve` deve essere una lista, altrimenti `ValueError`. Le righe vuote si scartano prima del taglio a 5. Esito: ok, **cosmetica 4 chiusa**.
- `tests/test_unit_esiti.py` (parte aggiunta, test parametrizzato sui caratteri e test sul BOM e sulla chiave minuscola) — coprono U+FEFF, U+2060, U+00AD, il tag, U+202E, \x07, il BOM prima del marcatore e la chiave minuscola. Il mutante C*→Cc li fa fallire, quindi tengono davvero. Esito: ok.

**Finding**
1. **R-864-3 BASSA (resta aperta, come da piano)** — Un riassunto può contenere «rispondi mergia 999». La difesa nel codice va messa in F4/F5: MERGIA vale solo per una PR aperta dall'esecutore per quella issue.
2. **Cosmetica 5 (resta aperta)** — I commenti scartati non lasciano traccia: la F3 dovrà scriverlo in gas_debug.log.
3. **R-865-1 BASSA (nuova)** — Alcuni caratteri che si vedono come vuoti non sono di categoria C* e quindi passano: U+3164 (riempitivo Hangul), U+2800 (braille vuoto) e i selettori di variante. Così un riassunto può sembrare vuoto pur superando il controllo `not riassunto`. Non è un rischio di iniezione: è testo che si vede male. Correzione possibile: togliere anche questi tre casi, come i caratteri provati nella review #574 su `bot_esito`.
4. **COSMETICA (nuova)** — Il carattere U+200D (unione fra emoji, categoria Cf) viene tolto, quindi le emoji composte nei testi liberi escono spezzate in pezzi separati da spazi.

**Coerenza col progetto.** Ogni lettore ha ancora `try/except` e restituisce None (§9). Gli scrittori danno `ValueError` per scelta dichiarata. Type hints presenti. Nessuna rete, nessun file, nessuna credenziale. Il modulo non è collegato a nulla.

**Cosa NON ho verificato.**
- La suite completa e la CI: ho fatto girare solo il file di test nuovo.
- Come GitHub restituisce il corpo dei commenti via API: la F3 non esiste ancora.

**Memoria.** Ho aggiunto la riga #865 a `/home/user/Gas/.claude/agents/memoria_revisore.md` e l'ho committata da sola (62a1adc). Anche la #864 risulta committata (0656fc0). Il diff in staging è intatto, quindi puoi lanciare `segna_review_ok.sh`. In `reports/stato_progetto.md` vanno scritte R-864-3, R-865-1 e la cosmetica 5.

## VERDETTO: APPROVATO

Verdetto #866 riemesso: stessa sostanza, solo testo ASCII per gli escape e nessun carattere invisibile vero. Nell'elemento 1 il carattere è scritto come sequenza di testo: backslash, u, 202e.

Ho letto: CLAUDE.md (sezioni 1, 4, 5, 8, 9, 10), la voce «Mani alla voce» di `reports/stato_progetto.md` (riga 393) e la coda di `.claude/agents/memoria_revisore.md` (#864, #865). Ho esaminato il diff staged: 2 file, +49/-14, inizio dello sha256 del diff `bcdf8ee5`. Ho lanciato i test su una copia dell'indice (cioè sui file così come sono in staging): **55 passed**.

**Elementi del diff esaminati**
1. `tests/test_unit_esiti.py:60` — i caratteri U+202E scritti direttamente nel file (righe 60 e 63) ora sono l'escape di testo backslash-u-202e. Rischio esaminato: il controllo del bot «controlli bidi nel testo» che risultava fallito. Ho cercato nei due file i caratteri invisibili veri (categorie Cf, Co, Cn, più i riempitivi): nessuno trovato. Esito: **ok**.
2. `tests/test_unit_esiti.py:141` — nuovo test che fallisce se nei due file ricompare un carattere Cf vero. Rischio esaminato: che il problema torni senza che nessuno se ne accorga. Copre solo Cf e non Co/Cn, che però il bot non segnala. Esito: **ok**.
3. `modules/sviluppo/esiti.py:116` — in lettura VERIFICA_ESTERNA accetta solo i valori fissi: un valore libero, o anche APPROVATO seguito da U+FE0F, porta a None (provato). `modules/sviluppo/esiti.py:132` — in scrittura il valore non ammesso dà ValueError, il default è «assente» e la riga viene sempre scritta. Rischio esaminato: rompere chi oggi produce o legge commenti ESITO. Nel repo nessun file .py, .sh o .yml fuori dai due file usa `scrivi_esito`, `leggi_esito` o `VERIFICA_ESTERNA`: il modulo non è collegato a nulla, quindi il cambio di formato non tocca nessuno. Esito: **ok**.
4. `modules/sviluppo/esiti.py:176` — con verifica esterna BOCCIATO Gas non chiede più il merge. Ho provato che con APPROVATO CON RISERVE la domanda resta, ed è giusto, perché decide comunque la regola di merge di CLAUDE.md §10. Il nuovo test copre il caso BOCCIATO con bot APPROVATO, e anche il caso «assente», dove la verifica esterna non compare nella frase. Esito: **ok**.
5. `modules/sviluppo/esiti.py:40` — R-865-1 chiusa: l'insieme `_VUOTI` contiene U+115F, U+1160, U+3164, U+FFA0, U+2800, FE00-FE0F e E0100-E01EF, ed è scritto con escape (nessun carattere letterale). Provato: `_pulisci` sulla stringa con escape di testo a, backslash-U-000E01EF, b, backslash-U-000E01F0, c, backslash-u-fe00, d, backslash-u-200d, e dà `'a b c d e'`. U+E01F0 non è assegnato (categoria Cn), quindi lo toglie già la regola sulle categorie C*. Effetto collaterale accettabile: le emoji perdono il selettore FE0F e si vedono nella forma testo. Esito: **ok**.
6. `modules/sviluppo/esiti.py:23` — la docstring ora dice il vero: i lettori non sollevano eccezioni e restituiscono None, gli scrittori danno ValueError per un valore non ammesso. Esito: **ok**.

**Finding**
- Nessun finding nuovo.
- Resta aperta R-864-3, **BASSA**: un RIASSUNTO può contenere il testo «mergia 999». La difesa va fissata in F4/F5: «mergia» vale solo per la PR aperta dall'esecutore per quella issue. È già tracciata in `reports/stato_progetto.md`.
- Resta aperta la cosmetica 5 (commenti scartati senza log), da fare in F3.
- Va aggiornata la riga 393 di `reports/stato_progetto.md`: togliere R-865-1 dalle «Aperte».

**Controlli del progetto**: il diff non tocca la storia dei messaggi né `_get_window()`, non simula output dei tool e non tocca il tetto di 10 iterazioni. Fail-safe §9 rispettato: i lettori restano dentro try e danno None, gli scrittori sollevano di proposito per non scrivere un commento che Gas poi ignorerebbe.

**Cosa non ho verificato**: l'esito del controllo verifica-bot rifatto sul nuovo head della PR (gira su GitHub, non da qui), e la modifica a `reports/mani_voce_piano.md`, che è fuori dal perimetro di review.

**Memoria**: la riga #866 è già in `/home/user/Gas/.claude/agents/memoria_revisore.md` (nessuna lezione nuova); come richiesto non l'ho toccata di nuovo.

## VERDETTO: APPROVATO CON RISERVE

Review #867, la quarta sulla PR #409 dopo il bot #409-bis (head 35c67d25). Ho esaminato il diff staged in /home/user/Gas, ramo claude/mani-voce-piano: `modules/sviluppo/esiti.py` e `tests/test_unit_esiti.py`, +53/−13.

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), la parte di stato_progetto.md che riguarda la PR, la mia memoria e il verdetto integrale del bot (check-run 139352802811).

Elementi del diff esaminati:
1. `modules/sviluppo/esiti.py:191` — la domanda di merge compare solo con PR valida, CI «verde», bot «APPROVATO» o «APPROVATO CON RISERVE» e verifica esterna diversa da BOCCIATO. Rischio esaminato: una riga BOT o CI mancante (None) faceva comparire la domanda (V-1 MEDIA). L'ho provato sulla copia dell'indice: senza riga BOT e con bot «assente» esce «niente merge»; con pr=True esce «PR mancante» e niente «mergia». Esito: ok, V-1 chiusa.
2. `modules/sviluppo/esiti.py:184` — `pr_ok` esclude i bool e i valori fuori da 1..PR_MAX, e senza PR la frase dice «PR mancante». Rischio esaminato: «mergia None» o «mergia True». Esito: ok.
3. `modules/sviluppo/esiti.py:94` — in lettura la riga RISERVA prima si pulisce, poi si scarta se è vuota; dalla sesta in poi le riserve si contano in `riserve_altre`. Rischio esaminato: una riserva fatta solo di invisibili che occupa un posto. Provato con U+FEFF, U+2060 e U+3164: vengono scartate. Esito: ok, V-2 chiusa.
4. `modules/sviluppo/esiti.py:179` — le riserve escono come «riserve: …» a parte, con «+N altre». Rischio esaminato: le riserve attaccate a «bot:». Esito: ok, V-4 chiusa.
5. `tests/test_unit_esiti.py:148` — test parametrizzato senza BOT e senza CI, più i test «PR mancante» e «invisibili/+N altre». Sulla copia dell'indice passano tutti e 59. Ho provato 6 mutanti e i test ne fermano 5. Il sesto sopravvive: togliere `or "assente"` da ci non cambia nulla, perché l'elenco dei valori buoni scarta comunque None. Esito: ok.
6. Contesto, file non toccato da questo giro: `modules/sviluppo/esiti.py:154` — vedi R-867-1.

Finding:
- **R-867-1 (BASSA)**: V-3 è chiusa solo in lettura. Il bot diceva «in lettura e in scrittura», ma `scrivi_esito` (`modules/sviluppo/esiti.py:154`) taglia ancora a RISERVE_MAX senza avvisare. L'ho provato: 8 riserve scritte, 5 rilette, nessun `riserve_altre`. Correzione: scrivere tutte le righe RISERVA (il commento resta comunque sotto COMMENTO_MAX) e lasciarle contare al lettore. Va aggiunto un test che fa andata e ritorno con più di 5 riserve.
- **R-867-2 (BASSA)**: in `modules/sviluppo/esiti.py:192` la verifica esterna resta controllata con l'elenco dei valori cattivi (`== "BOCCIATO"`), mentre CI e bot sono passati all'elenco dei buoni. Inoltre `riserve` e `riserve_altre` non vengono ripulite in `frase_esito`. Con un dizionario fatto a mano e verifica «boh» compare la domanda di merge (provato). Passando da `leggi_esito` non può succedere, perché lì i valori sono fissi. Correzione: `verifica not in VERIFICA or verifica == "BOCCIATO"`, oppure un elenco dei valori buoni.

Rischi esclusi, cioè non verificati:
- Suite completa e CI sul nuovo head: ho fatto girare solo `tests/test_unit_esiti.py` sulla copia dell'indice. Il modulo non è collegato a nulla, quindi il resto del motore non è toccato.
- Il collegamento con Telegram e la voce (F3) non esiste ancora, quindi non è verificabile.
- La scansione byte per byte dei caratteri invisibili l'ha fatta il test anti-Cf già presente. Non l'ho ripetuta a mano.

Memoria: ho aggiunto la riga #867 e una lezione in /home/user/Gas/.claude/agents/memoria_revisore.md. La lezione: quando un finding dice «in lettura e in scrittura», controllare tutti e due i lati, e passare all'elenco dei valori buoni su tutti i campi della stessa condizione. Il file è committato da solo (edb5de4f). Il diff staged è rimasto intatto.

## VERDETTO: APPROVATO

Review #868, il quinto giro sulla PR #409: ho rivisto per intero il diff staged su claude/mani-voce-piano, cioè `modules/sviluppo/esiti.py` e `tests/test_unit_esiti.py` (+67/−14). I 61 test passano sulla copia dell'indice. Nei due file non ci sono caratteri invisibili veri: zero caratteri di categoria C* a parte a capo e tabulazione.

Elementi del diff esaminati:
1. `modules/sviluppo/esiti.py:156` — `scrivi_esito` ora scrive tutte le riserve; chi legge ne tiene 5 e conta le altre in `riserve_altre`. Rischio esaminato: riserve oltre la quinta perse senza avviso in scrittura (R-867-1). Il test a `tests/test_unit_esiti.py:173` scrive 8 riserve e rilegge 5 tenute più 3 contate. Ho anche provato 30 riserve da 300 caratteri: il commento supera COMMENTO_MAX e `scrivi_esito` solleva ValueError, quindi blocca invece di scrivere un commento rotto. Esito: ok, R-867-1 chiusa.
2. `modules/sviluppo/esiti.py:194` — una verifica esterna con un valore fuori elenco toglie la domanda di merge. Rischio esaminato: un dizionario fatto a mano con verifica «boh» chiedeva il merge (R-867-2). Coperto dal test a `tests/test_unit_esiti.py:178`. L'ho provato: con BOCCIATO esce «niente merge», con APPROVATO esce la domanda. Esito: ok, R-867-2 chiusa.
3. `modules/sviluppo/esiti.py:191` — restano valide le correzioni già approvate in #867: chiusi i finding del bot V-1 (riga BOT mancante, PR mancante), V-2 (riserva fatta di soli invisibili), V-3 (lato lettura) e V-4 (riserve a parte). Esito: ok.

Note cosmetiche, nessuna blocca:
- C-1: con troppe riserve il ValueError dice «manca il riassunto o la PR» (`modules/sviluppo/esiti.py:160`), un messaggio che porta fuori strada.
- C-2: se `frase_esito` riceve un dizionario fatto a mano, `riserve` e `riserve_altre` non vengono ripulite dagli invisibili. Se il dizionario viene da `leggi_esito`, lo sono già.

Rischio escluso: non ho lanciato la suite completa né la CI sul nuovo head, solo `tests/test_unit_esiti.py`. Il modulo non è ancora collegato a nulla, quindi il resto del motore non è toccato. Il collegamento con Telegram e la voce (F3) non esiste ancora e non è verificabile.

Memoria: ho aggiunto la riga #868 («nessuna lezione nuova») in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (4606d48c). Il diff staged è rimasto intatto.

## §4bis VERDETTO DEL REVISORE SUL MERGE DI MAIN (08875514)

Merge di origin/main (PR #402, R7 fetta 4) nel ramo: verdetto integrale #869-MERGE.

## VERDETTO: APPROVATO

Review #869-MERGE: merge in corso di origin/main (PR #402, R7 fetta 4) nel ramo claude/mani-voce-piano (PR #409), visto con `git diff --cached HEAD` e `git diff --cached MERGE_HEAD`.

**Cosa ho controllato nel diff:**
1. `modules/sottofondo/__init__.py:883` — `_scaduto` del tetto di tempo, arrivato da main (con `modules/sottofondo/__init__.py:815`, il Timer col tetto `TETTO_TIMER_S`, e `modules/sottofondo/__init__.py:933`, il ramo `gia_chiuso`). Rischio esaminato: una risoluzione del conflitto che altera il codice di R7. Esito: ok. Il diff contro MERGE_HEAD è vuoto, quindi il file è identico a origin/main.
2. `tests/test_unit_sottofondo.py:1433` — test `test_tetto_scaduto_ferma_il_compito_con_avviso` (con i vicini a `tests/test_unit_sottofondo.py:1426` e `tests/test_unit_sottofondo.py:1453`). Rischio esaminato: test persi o mescolati. Esito: ok. Anche qui il diff contro MERGE_HEAD è vuoto.
3. `.claude/agents/memoria_revisore.md:1762` — righe di main inserite dopo #863-MERGE (#852-R7 alla riga 1762, #853-R7 alla 1764, #864-MERGE-R7 alla 1766), poi le nostre #864..#868 (righe 1767-1773). Rischio esaminato: righe perse in una delle due parti. Esito: ok. Sia il diff contro HEAD sia quello contro MERGE_HEAD contengono solo aggiunte (5 righe di main, 7 nostre), nessuna riga tolta. Ci sono 5 caratteri invisibili, ma sono già presenti in entrambe le versioni (sono le citazioni delle lezioni), quindi non li ha introdotti il merge.
4. `reports/stato_progetto.md:406` — voce R7 fetta 4 con R-852R7-1/4 dichiarate e le riserve aperte R-853R7-1, R-853R7-2 e R-853R7-3. Esito: ok. Le riserve di R7 di main sono tracciate. La voce «Mani alla voce» è alla `reports/stato_progetto.md:393`. La testata di `reports/stato_progetto.md:4` è quella di main e contiene per intero la nostra (controllato con un confronto di sottostringa).
5. File di sessione: `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md` hanno diff vuoto contro HEAD, quindi è tenuto il nostro lato come dice la regola 3 di `reports/lavoro_parallelo.md`. Esito: ok.

Non c'è nessun marcatore di conflitto e `git ls-files -u` è vuoto. `python -m pytest -q tests/test_unit_sottofondo.py tests/test_unit_esiti.py` dà 198 passed.

Nota COSMETICA: la testata presa da main dice «PR #402 ancora aperta», che non è più vero dopo questo merge. Conviene aggiornarla al prossimo giro dei report.

**Cosa non ho verificato:** non ho rieseguito la suite completa del motore, ma solo le due suite toccate. Il codice di R7 è identico a main e lì è già stato revisionato (#852-R7, #853-R7, #864-MERGE-R7). Non ho rifatto la review di merito di `modules/sviluppo/esiti.py`, che il merge non tocca (giri #864..#868).

**Memoria:** ho aggiunto la riga contatore #869-MERGE in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, senza lezioni nuove. È NON committata e NON in staging: lo stato è `MM` e va aggiunta al commit di merge.

## §5 DELTA TEST DEL MOTORE

- File nuovo `tests/test_unit_esiti.py`: 0 → 46 test (81c751fa) → 55 test (3f7a0075) → 61 test (13eaa1a2), tutti passati (`python -m pytest -q tests/test_unit_esiti.py` → `61 passed in 0.11s`).
- `tests/test_unit_sottofondo.py` + `tests/test_unit_richieste.py`: `154 passed in 6.14s` (dopo `pip install -r requirements.txt`; prima 3 rossi per `openai` mancante nel container).
- Suite completa locale, `python -m pytest -q -x tests` (lanciata prima delle correzioni):

```
FAILED tests/test_unit_web_browser.py::test_testo_scritto_dal_javascript - as...
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 3648 passed in 551.59s (0:09:11)
```

  Il FAIL è fuori scope: test del browser (JavaScript nel Chromium del container), file non toccati da questa sessione. Con `-x` la suite si è fermata lì: fa fede la CI (`unit-suite`).

## §6 STATO CI

Check run per SHA (da `gh api repos/Gasss23/Gas/commits/<sha>/check-runs`; `gh run list` non è disponibile qui):

```
0b039727: verifica-bot completed success | esito completed success | verifica completed success | smista completed success | handoff-check completed success | unit-suite completed success
35c67d25: verifica-bot completed failure | handoff-check completed success
ec8a1d7a: unit-suite completed success | verifica-bot completed failure
```

- 93090a56: run CI success.
- 0656fc0d, 62a1adcc: nessuna run su questo SHA (pushati insieme a 81c751fa).
- 81c751fa: run CI avviata; esito non riletto (superata da ec8a1d7a, stesso codice motore).
- ec8a1d7a: unit-suite success; verifica-bot failure («controlli bidi nel testo», corretto in 3f7a0075).
- a8ab5efd, 3f7a0075: nessuna run su questi SHA (pushati insieme a 35c67d25).
- 35c67d25: handoff-check success; verifica-bot failure (finding MEDIA, corretto in 13eaa1a2).
- edb5de4f, 4606d48c, 13eaa1a2: nessuna run su questi SHA (pushati insieme a 0b039727).
- 0b039727: unit-suite success, handoff-check success, verifica-bot success (APPROVATO CON RISERVE, solo BASSE/COSMETICHE).
- 08875514 (merge di main) e il commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-864-3 BASSA — un riassunto può contenere «mergia 999»: in F4/F5 MERGIA deve valere solo per la PR aperta dall'esecutore per quella issue (confermata anche da verifica esterna #409 V-3).
- Verifica esterna #409 V-2 BASSA — la domanda di merge compare anche con bot APPROVATO CON RISERVE e riserve ALTA/MEDIA: da rivedere in F4 (il merge lo decide comunque §10).
- Verifica esterna #409-bis V-4 COSMETICA — `comando_operatore` accetta uno spazio speciale (U+00A0) fra azione e numero; innocuo.
- Cosmetica 5 — i commenti scartati non lasciano traccia nel log (da fare in F3).
- Cosmetica (#865) — U+200D tolto: le emoji composte escono spezzate.
- Cosmetiche #868: C-1 messaggio di ValueError fuorviante con troppe riserve; C-2 `frase_esito` non ripulisce le riserve di un dizionario fatto a mano.
- Bot sul head 0b039727 V-1 BASSA — altri invisibili Default_Ignorable (U+034F, U+17B4, U+17B5, U+180B-180D, U+180F) passano `_pulisci`; V-2 COSMETICA — commenti vecchi in esiti.py (righe 14 e 42); V-3 COSMETICA — descrizione della PR (aggiornata).
- Verifica esterna #409-ter V-1 BASSA — `frase_esito` non ripulisce un dict fatto a mano; V-4 COSMETICA — doppio spazio con riassunto vuoto.
- Revisore #869-MERGE COSMETICA — testata di stato_progetto «PR #402 ancora aperta»: corretta in questo giro.
- Chiuse: R-865-1, bot #409 V-1…V-4 (3f7a0075); bot #409-bis V-1 MEDIA, V-2…V-4, R-867-1, R-867-2, verifica esterna #409-bis V-1 (13eaa1a2).
- Fuori scope: `tests/test_unit_web_browser.py::test_testo_scritto_dal_javascript` rosso nel container.
