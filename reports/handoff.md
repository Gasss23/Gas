# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-25 — Mani alla voce: piano + formato fisso dei commenti ESITO/COMANDO (F2) + correzione dopo bot/verifica esterna, PR #409

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #409 (https://github.com/Gasss23/Gas/pull/409). Revisore #866 APPROVATO sull'ultima correzione, ma verifica esterna APPROVATO CON RISERVE (solo BASSE) e bot da rifare sul nuovo head: il merge lo decide l'operatore (CLAUDE.md §10).
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
- **F1 — firma a voce per `richiedi_sviluppo`**: `DEFERITA — aspetta il via dell'operatore`.
- **F3 — Gas legge gli esiti dalle issue**: `DEFERITA — aspetta il via dell'operatore`.
- **F4 — «mergia N» da Telegram**: `DEFERITA — aspetta il via dell'operatore`.
- **F5 — esecutore come scheduled task cloud**: `DEFERITA — spesa ricorrente e credenziali, aspetta il via`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/sviluppo/esiti.py          | 216 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  19 +++++++---------
 reports/handoff.md                 | n/d
 reports/mani_voce_piano.md         | 123 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  67 +++++++++++++++----------------------------------------
 tests/test_unit_esiti.py           | 145 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
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

Commit motore 81c751fa: verdetto integrale del secondo giro (#865), che copre il codice di quel commit (il primo giro #864 era su una versione precedente, poi corretta; le sue citazioni di riga non esistono più). Commit motore 3f7a0075: verdetto #866, riemesso dal revisore con gli escape scritti come testo (la prima emissione conteneva un carattere U+202E vero che avrebbe fatto fallire il bot); stessa sostanza ed esito. Le righe citate da #865 si riferiscono al file di 81c751fa: dopo 3f7a0075 alcune sono slittate di qualche riga.

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

## §5 DELTA TEST DEL MOTORE

- File nuovo `tests/test_unit_esiti.py`: 0 → 46 test (81c751fa) → 55 test (3f7a0075), tutti passati (`python -m pytest -q tests/test_unit_esiti.py` → `55 passed in 0.12s`).
- `tests/test_unit_sottofondo.py` + `tests/test_unit_richieste.py`: `154 passed in 6.14s` (dopo `pip install -r requirements.txt`; prima 3 rossi per `openai` mancante nel container).
- Suite completa locale, `python -m pytest -q -x tests` (lanciata prima delle correzioni):

```
FAILED tests/test_unit_web_browser.py::test_testo_scritto_dal_javascript - as...
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 3648 passed in 551.59s (0:09:11)
```

  Il FAIL è fuori scope: test del browser (JavaScript nel Chromium del container), file non toccati da questa sessione. Con `-x` la suite si è fermata lì: fa fede la CI (`unit-suite`).

## §6 STATO CI

```
ec8a1d7a verifica-bot completed success
ec8a1d7a verifica-bot completed skipped
ec8a1d7a CI in_progress null
81c751fa verifica-bot completed skipped
81c751fa CI in_progress null
93090a56 CI completed success
```
(da `gh api repos/Gasss23/Gas/actions/runs?branch=claude/mani-voce-piano`: `gh run list` non è disponibile qui)

- 93090a56: run CI success.
- 0656fc0d, 62a1adcc: nessuna run su questo SHA (pushati insieme a 81c751fa).
- 81c751fa: run CI in corso alla scrittura.
- ec8a1d7a: run CI in corso alla scrittura; handoff-check success; check `verifica-bot` failure (verdetto del bot APPROVATO CON RISERVE, ma «controlli bidi nel testo: verdetto ambiguo», causato dai caratteri U+202E veri nel file di test, corretti in 3f7a0075). Il workflow run del bot risulta «success», il check sulla PR «failure».
- a8ab5efd, 3f7a0075 e il commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-864-3 BASSA — un riassunto può contenere «mergia 999»: in F4/F5 MERGIA deve valere solo per la PR aperta dall'esecutore per quella issue (confermata anche da verifica esterna #409 V-3).
- Verifica esterna #409 V-2 BASSA — la domanda di merge compare anche con bot APPROVATO CON RISERVE e riserve ALTA/MEDIA: da rivedere in F4 (il merge lo decide comunque §10).
- Cosmetica 5 — i commenti scartati non lasciano traccia nel log (da fare in F3).
- Cosmetica (#865) — U+200D tolto: le emoji composte escono spezzate.
- Chiuse con 3f7a0075 (#866): R-865-1, bot #409 V-1…V-4, verifica esterna #409 V-1.
- Fuori scope: `tests/test_unit_web_browser.py::test_testo_scritto_dal_javascript` rosso nel container.
