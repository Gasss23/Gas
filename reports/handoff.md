# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-27 — Mani fetta 20 con secondo giro: lettura con lexbor pronta per l'accensione, ancora spenta, chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #277 (https://github.com/Gasss23/Gas/pull/277). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5034496930","url":"https://github.com/Gasss23/Gas/pull/277"}`; `actions_list` riporta `"pull_requests":[277]` sulla run di 0418f37); `gh` nel cloud non è autenticato. Bot e verifica esterna su 0c2a5c8: APPROVATO CON RISERVE, quindi serve l'OK dell'operatore (niente merge autonomo). Il merge non accende niente.
2. Accensione: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt`; poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Poi, una alla volta: R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **Preparazione dell'accensione della lettura con lexbor (richiesta dell'operatore «prepara l'accensione»)**: `FATTA` — lettura ancora spenta per default.
  - Primo giro (ab5eb1d): R-521-1/2/3, R-524-1, V-1/V-2 bot #275, stima dei tempi, select/datalist/rp/hidden/dialog chiusi, R-525-1/2/3: `FATTA`.
  - Secondo giro (0418f37): V-1/V-2/V-3 bot #277 e V-1..V-5 verifica esterna #277 (V-1 ve = merge di main c75f462 in 33e0d42): `FATTA`.
  - R-527-1/2/3/4, R-528-1/2: `FATTA`.
  - R-528-3, R-529-1, R-526-1, R-520-4 (cosmetiche): `DEFERITA — cosmetiche, verso sicuro (mai testo nascosto)`.
- **Accensione vera**: `DEFERITA — serve la chat Motore (requirements, CI, ambiente del VPS)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  12 ++++++++++++
 modules/web/leggi.py               |   7 ++++---
 modules/web/lexbor.py              | 191 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------
 reports/diff_sessione.md           |   9 +++++++--
 reports/handoff.md                 | n/d (commit finale)
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  42 ++++++++++++++++++++++++++++++++++++------
 tests/test_unit_web_lexbor.py      | 156 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat 932ecd6` preso con i report in stage, prima del commit finale. BASE = `git merge-base origin/main HEAD` = 932ecd6 (dopo il merge di main 7e2622f): gas.py, tests/test_unit_kernel.py e reports/coda_notte.md arrivano da main e non sono nel diff.

## §3 GIT LOG --ONELINE (sessione)

```
7e2622f Merge origin/main (932ecd6, PR #276 e #278) in claude/peaceful-lovelace-0w2b7q (PR #277)
0c2a5c8 docs(fine-task): Mani fetta 20 secondo giro — report, handoff, stato (PR #277, review #527-#529)
0418f37 feat(web): fetta 20 secondo giro — select, details, hidden e sonde come il browser (PR #277)
4f30374 chore(revisore): memoria review #529 — APPROVATO CON RISERVE
d4ac3c9 chore(revisore): memoria review #528 — APPROVATO CON RISERVE
3a23c4f chore(revisore): memoria review #527 — APPROVATO CON RISERVE
33e0d42 Merge origin/main (c75f462, PR #274) in claude/peaceful-lovelace-0w2b7q (PR #277)
dbe5efc docs(fine-task): Mani fetta 20 — report, handoff, stato (PR #277, review #525-#526)
ab5eb1d feat(web): lettura con lexbor pronta per l'accensione, ancora spenta (fetta 20 Mani)
ffe99a8 chore(revisore): memoria review #526 — APPROVATO CON RISERVE
88dd43a chore(revisore): memoria review #526 — APPROVATO CON RISERVE
7290177 chore(revisore): memoria review #525 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore ab5eb1d: review #525 sul primo diff e #526 dopo la chiusura di R-525-1/2/3. Commit motore 0418f37: review #527 sul secondo giro, #528 dopo R-527-1..4, #529 dopo R-528-1/2. Il merge 33e0d42 non porta file del perimetro (solo reports/roadmap.md da main): niente review. Il merge 7e2622f porta da main gas.py e tests/test_unit_kernel.py: review #530. Verdetti integrali:

### Review #525 (chat Mani) — primo diff staged

## VERDETTO: APPROVATO CON RISERVE

Review #525 (chat Mani). Ho esaminato il diff staged, che tocca 3 file: `modules/web/leggi.py`, `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py`. Prima ho letto CLAUDE.md (sez. 5), lo stato del progetto (voci delle fette 19 e 20) e le lezioni della mia memoria (lock, sonda «una volta sola», tetti di risorsa).

**Elementi del diff esaminati**
- `modules/web/lexbor.py:103` — lock non bloccante: prima si guarda il tempo di riprova, poi si tenta il lock. Rischi esaminati: deadlock, mancato rilascio, attesa per chi chiama — **ok**. Se il controllo sul tempo è vero, il lock non viene nemmeno preso. Se il lock è occupato, la funzione esce subito senza rilasciare. Il rilascio è in `finally` (`modules/web/lexbor.py:119`), quindi avviene in ogni ramo. `_esegui` intercetta già ogni Exception. Chi arriva mentre gira la sonda non aspetta. Mutante «senza release»: 1 failed.
- `modules/web/lexbor.py:111` — riprova della sonda su `time.monotonic()`. Rischio esaminato: orologio che salta — **ok**. Il tempo monotono non torna mai indietro. Su Linux non avanza durante la sospensione, quindi al massimo la riprova arriva più tardi, mai prima: è il verso sicuro. Il valore di partenza 0.0 è corretto. Ho ripetuto 5 volte i test delle sonde: tutti verdi.
- `modules/web/lexbor.py:82` — controllo dell'attributo `hidden` e dei dialog senza `open` tramite `nodo.attributes`. Rischi esaminati: costo e nodi senza attributi — **riserva**. Il risultato è corretto: un nodo senza attributi dà un dict vuoto; `HIDDEN` maiuscolo viene preso; `hidden=x` dentro svg viene nascosto (verso sicuro); `dialog open=false` resta visibile come nel browser. Ma `attributes` costruisce un dict di tutti gli attributi a ogni elemento. Misure: 20k div con 100 attributi ciascuno 3,31 s, contro 0,99 s con `nodo.attrs` (stessi esiti verificati); 200k p con 3 attributi 1,19 s contro 0,70 s. Con il tempo massimo di 4 s, più pagine finiscono sul ripiego: niente crash, ma +4 s e niente lexbor su quelle pagine.
- `modules/web/lexbor.py:57` — select, datalist e rp nascosti. Rischio esaminato: perdite gravi di testo — **ok**. Un `<select>` non chiuso inghiotte il resto della pagina, perché lexbor segue il select nuovo. Ma anche il browser, nell'aspetto normale, mostra solo l'opzione scelta e non il resto. È comunque il verso sicuro (meno testo, mai testo nascosto). `rp` fuori da ruby è nascosto, come nel foglio di stile standard del browser.
- `modules/web/lexbor.py:132` — `_ultima_riga` porta l'ultima riga dello stderr del figlio nel log. Rischio esaminato: testo della pagina o caratteri pericolosi nel log — **ok**. `splitlines` separa anche su `\r` e U+2028; i caratteri di controllo bidi e quelli a larghezza zero diventano `?`; il taglio è a 200 caratteri e il log usa `%r`. L'ultima riga è il messaggio di un'eccezione, non testo della pagina; anche nel caso peggiore il testo della pagina arriva già al modello come risultato del tool.
- `modules/web/lexbor.py:52` — uscita 3 fuori da Linux. La sonda la tratta come «errore» e spegne la lettura per sempre, con un solo warning — **ok**. Il test sostituisce la stringa e non è vuoto: se la sostituzione non avvenisse, `attivo()` sarebbe True e il test fallirebbe.
- `tests/test_unit_web_lexbor.py:118` — test «una sonda alla volta» — **riserva**. Il mutante `_SONDA.acquire()` bloccante sopravvive (27 passed), perché il test conta solo i lanci e almeno un True; la proprietà «niente attesa per chi chiama» non è fissata.
- `modules/web/leggi.py:33` — stima nella docstring: 12+4+3+4 = circa 23 s — **ok**.

**Mutanti miei** (`modules/web/lexbor.py` ripristinato, il diff staged è intatto):
- Presi: senza release (1 failed), rp visibile (1 failed).
- Sopravvissuti: lock bloccante, senza doppio controllo sotto lock, senza `isprintable`, senza taglio a 200.

**Test**
- lexbor: 27 passed (3.13.16 con selectolax 1.0.2), 2 passed e 25 skipped (3.11 senza selectolax).
- Test web su 3.13: 469 passed, 1 skipped.

**Riserve**
- **R-525-1 (chat Mani) BASSA**: a `modules/web/lexbor.py:82` usare `attributi = nodo.attrs`. È l'oggetto `LexborAttributes`: `in` funziona senza costruire il dict, con gli stessi esiti verificati su HIDDEN, svg e dialog, ed è circa 3 volte più veloce sulle pagine ricche di attributi.
- **R-525-2 (chat Mani) BASSA**: a `tests/test_unit_web_lexbor.py:118` aggiungere `esiti.count(False) >= 1`, così il mutante con lock bloccante viene preso. Con la pausa di 0,3 s nella sonda, gli altri 7 thread arrivano mentre gira.
- **R-525-3 (chat Mani) COSMETICA**: senza test restano la pulizia di `_ultima_riga` (caratteri non stampabili, taglio a 200) e il doppio controllo sotto lock. Il codice è corretto, verificato a mano; il doppio controllo mancante costerebbe al massimo una sonda in più in una finestra stretta.

**Rischi esplicitamente esclusi**
- Comportamento su VPS e sul Mac reale, e il primo avvio a freddo del figlio fuori dall'ambiente di sviluppo: non riproducibili qui.
- `os.fork` con il lock preso: non verificato. Gas non usa fork senza exec; nel caso peggiore il processo figlio non accenderebbe mai lexbor, che è il verso sicuro.
- Oracolo html5lib su 60 mila pagine e le 131 pagine locali: non rifatti, cifre dichiarate dall'autore.

**Memoria**
- Riga contatore #525 e 2 lezioni (lock non bloccante da provare col mutante bloccante; costo di `nodo.attributes` contro `nodo.attrs`) aggiunte a `/home/user/Gas/.claude/agents/memoria_revisore.md`.
- Committate da sole: 7290177. I 3 file del diff restano in stage.
- `reports/stato_progetto.md` era già modificato prima della review, non in stage: non l'ho toccato.

### Review #526 (chat Mani) — sul diff committato in ab5eb1d

## VERDETTO: APPROVATO CON RISERVE

Review #526 (chat Mani): ri-review del diff staged su claude/peaceful-lovelace-0w2b7q dopo la #525. Prima della review ho letto CLAUDE.md (sez. 5), la parte di reports/stato_progetto.md sulla fetta 20 (§ riga 632) e la coda di memoria_revisore.md.

**Cosa ho controllato nel diff**
- `modules/web/lexbor.py:82`: il figlio ora usa `attributi = nodo.attrs` al posto di `nodo.attributes` (chiude R-525-1). Rischio: che cambi l'esito sui casi limite. L'ho confrontato su 14 casi con selectolax 1.0.2, lanciato con `-I`: HIDDEN maiuscolo, hidden="", hidden=false, `<g hidden>` dentro svg, svg HIDDEN, math hidden, dialog senza attributi, dialog open=false, OPEN e open="", data-hidden, xlink:hidden, dialog dentro svg, body e p senza attributi (`len(attrs)==0`, nessuna eccezione). Le due forme danno esiti identici in tutti i casi. Il mutante che rimette `nodo.attributes` passa 28 su 28, come atteso: è equivalente. Esito: ok.
- `tests/test_unit_web_lexbor.py:126`: la nuova asserzione `esiti.count(False) >= 1` (chiude R-525-2). Rischio: test instabile, oppure che non prenda il lock bloccante. Il mutante `_SONDA.acquire()` bloccante dà 1 failed. Il test non dovrebbe essere instabile: il primo thread tiene il lock per 0,3 s mentre gli altri 7 partono subito. 8 ripetizioni tutte verdi. Esito: ok.
- `tests/test_unit_web_lexbor.py:99`: nuovo test di `_ultima_riga` in `modules/web/lexbor.py:132` (chiude in parte R-525-3). Mutanti: senza isprintable 1 failed, senza taglio a 200 1 failed, prima riga invece dell'ultima 2 failed. Il test non porta `@con_lexbor`, quindi gira anche in CI con 3.11 senza selectolax. Esito: ok.
- `modules/web/lexbor.py:106`: il doppio controllo sotto lock non ha ancora un test. L'autore lo dichiara: nel caso peggiore parte una sonda in più in una finestra stretta, verso sicuro. Esito: riserva cosmetica (R-526-1).
- Altri mutanti rifatti: «hidden» ignorato 1 failed, dialog chiuso ignorato 1 failed.
- Dopo ogni mutante ho ripristinato il file con `git checkout --` dall'indice. Lo stage è intatto: M sui 3 file del diff, stato_progetto non in stage.
- Suite: lexbor 28 passed con Python 3.13.16; con 3.11 3 passed e 25 skipped; web (`-k web`) 470 passed e 1 skipped con 3.13. Il 470 al posto del 469 dichiarato dall'autore dipende dalla selezione dei file. Nessuna regressione.

**Wall of Shame e guardrail**: il diff non tocca la history, `_get_window`, il cap delle 10 iterazioni né i provider. Non c'è simulazione dei tool. Gli errori del figlio restano tutti intercettati e finiscono come warning in gas_debug.log, con il ripiego sulla lettura di sempre (§9 ok).

**Riserva**
- R-526-1 COSMETICA: il doppio controllo sotto lock (`modules/web/lexbor.py:106`) resta senza test. È il residuo dichiarato di R-525-3 e va tracciato in reports/stato_progetto.md. In questo momento stato_progetto non contiene ancora le voci R-525-x/R-526-x: vanno aggiunte prima del commit.

**Cosa non ho verificato**: non ho provato il comportamento del ramo acceso fuori da Linux su macOS reale, né la soglia di memoria del figlio su altre build di selectolax. Qui non sono riproducibili (sandbox Linux, una sola build 1.0.2). La sonda dell'uscita 3 è coperta solo dal test che sostituisce il nome della piattaforma.

**Memoria**: ho aggiunto la riga #526 a `/home/user/Gas/.claude/agents/memoria_revisore.md`, nessuna lezione nuova. È committata con `scripts/commit_memoria_revisore.sh` (88dd43a). Un secondo commit, ffe99a8, corregge la riga citata da :105 a :106. I file del diff sotto review sono rimasti in stage.

### Review #527 (chat Mani) — secondo giro, diff staged poi committato in 0418f37

## VERDETTO: APPROVATO CON RISERVE

Review #527 (chat Mani). Diff staged di PR #277, branch claude/peaceful-lovelace-0w2b7q: modules/web/lexbor.py e tests/test_unit_web_lexbor.py. Ho riletto lo stage dopo l'avviso del coordinatore: lo stage non era vuoto quando l'ho letto. Lo SHA-256 di `git diff --cached` è e8485308…1759 sia all'inizio sia alla fine della review, e i file sono ancora in stage. Prima della review ho letto CLAUDE.md §5, reports/stato_progetto.md (fetta 20) e la memoria del revisore.

**Elementi del diff esaminati**
- modules/web/lexbor.py:81 — risalita da opzione a select: scarta se un antenato è nascosto (tag in `nascosti`, select, `hidden`/dialog chiuso). Rischio esaminato: testo nascosto che esce dal ramo delle opzioni. Il codice è corretto: con datalist, svg, object o canvas fra select e opzione esce W2, quella giusta. Però nessun test fissa la guardia sui tag. Il mutante che toglie `sopra.tag in nascosti` passa 38 su 38, e con quel mutante i 4 casi fanno uscire W1 (fuga reale). Esito: **riserva R-527-1**.
- modules/web/lexbor.py:88 — filtro `not nascosto(o)` sull'opzione stessa (attributo `hidden`). Anche questo mutante passa 38 su 38: il test di tests/test_unit_web_lexbor.py:72 prende solo l'antenato `div hidden`. Esito: riserva, dentro R-527-1.
- modules/web/lexbor.py:78 — `visibile_in`, cioè una risalita per ogni opzione trovata da `select.css("option")`. Rischio esaminato: costo. Il costo è opzioni × profondità. `<select multiple>` con 2000 div annidati e 2000 opzioni pesa 50 KB: risalita 3,43 s, figlio oltre i 4 s, si torna alla lettura di sempre. La stessa pagina su HEAD gira in 0,10 s. Su HEAD il ripiego era già forzabile con circa 250 KB di div annidati: non è una classe nuova, ma la soglia scende di circa 5 volte. Pagine reali (10 mila select da 10 opzioni, 1 MB): 0,46 s. Esito: **riserva R-527-2**.
- modules/web/lexbor.py:98 — testo dell'opzione da `label` oppure da `visita(o, dentro_opzione=True)`. Rischio esaminato: script, style, svg, title o `hidden` dentro l'opzione. Sondati: escono solo i testi visibili; `label=''` ricade sul testo come da spec; il title dentro un'opzione diventa il titolo della scheda, coerente con la regola «primo title del documento». Esito: ok.
- modules/web/lexbor.py:90 — `size` letto con `int()` di Python. Rischio esaminato: valori ostili. `size="1_0"` e `size="٣"` (cifra araba) danno la lista intera, mentre il browser mostra la tendina. `size="3abc"` dà la tendina, mentre il browser fa 3 righe. Un numero da 5000 cifre fa ValueError, intercettato: niente crash. Esito: riserva cosmetica, dentro R-527-3.
- modules/web/lexbor.py:95 — scelta dell'opzione mostrata (l'ultima `selected`, altrimenti la prima). Rischio esaminato: coerenza con lo spec. Senza `selected` il browser prende la prima opzione NON disabilitata, Gas la prima in assoluto. Col segnaposto comune `<option hidden selected>Scegli` il browser mostra «Scegli» nel select chiuso, Gas mostra l'opzione dopo. Non esce testo nascosto: sono opzioni che si vedono aprendo la tendina. Esito: **riserva R-527-3**.
- modules/web/lexbor.py:123 — `if not dentro_opzione` e il controllo `sopra.tag == "select"` alla riga 81. Rischio esaminato: select annidati. lexbor non annida mai i select (`<select><div><select>` chiude il primo; `<option>` dentro un'opzione la chiude). Questi rami sono quindi irraggiungibili dal parser, solo difensivi, e i loro mutanti passano 38 su 38. Esito: **riserva R-527-4**.
- modules/web/lexbor.py:78 — confronto fra nodi con `mem_id`. Verificato in selectolax: `o.parent is s` è sempre False (a ogni accesso nasce un involucro nuovo), `mem_id` è un int ed è uguale per lo stesso nodo. Il confronto con `mem_id` è corretto; `is` è ridondante ma innocuo. Il mutante «solo `is`» viene preso. Esito: ok.
- modules/web/lexbor.py:136 — `hidden` su body o html dà testo vuoto, il titolo resta. `hidden=false` nasconde comunque, come il browser. Il mutante «body ignorato» viene preso da tests/test_unit_web_lexbor.py:57. Esito: ok.
- modules/web/lexbor.py:100 — `primo_summary`: solo un summary figlio diretto, che passa comunque dal controllo hidden. Sondati il summary non figlio (testo vuoto; il browser mostrerebbe «Details», perdita accettabile) e un summary `hidden` per primo (testo vuoto). Esito: ok.
- modules/web/lexbor.py:162 — `_SONDE_FALLITE` incrementato solo sotto `_SONDA`, che è un lock non bloccante con doppio controllo su `_RIPROVA_DOPO`; si spegne con `>= MAX_SONDE` alla riga 163. Mutanti presi: `>` invece di `>=`, e `_RIPROVA_DOPO` non impostato (da tests/test_unit_web_lexbor.py:162 e dal test della sonda oltre il tempo). Esito: ok. Effetto dichiarato: dopo 3 sonde fallite, a 600 s una dall'altra, la lettura resta spenta finché il processo vive.
- Contesto: modules/web/leggi.py:1431 — il chiamante passa `_TAG_NASCOSTI`, che contiene canvas, iframe, math, noembed, noframes, noscript, object, script, style, svg e template. Ricorsione limitata a 2 livelli (visita, opzione, visita senza select). Nessuno slicing della history (`scelte[-1:]` e `tutte[:1]` sono liste di opzioni) e nessuna simulazione di tool.

**Riserve da tracciare in stato_progetto**
- **R-527-1 (chat Mani) BASSA**: aggiungere casi parametrizzati per un'opzione `selected` dentro datalist, svg, object o canvas dentro il select, e per un'opzione con l'attributo `hidden` (riga 81 e riga 88). Oggi le guardie antifuga sono giuste ma nessun test le fissa.
- **R-527-2 (chat Mani) BASSA, da chiudere prima dell'accensione**: `visibile_in` è quadratico. Proposta: memorizzare i `mem_id` degli antenati già verificati, oppure raccogliere le opzioni scendendo dall'alto con la stessa visita iterativa.
- **R-527-3 (chat Mani) COSMETICA**: scelta dell'opzione (prima non disabilitata, segnaposto `hidden selected`) e lettura di `size` diverse dallo spec. Fissare la regola o dichiarare la differenza.
- **R-527-4 (chat Mani) COSMETICA**: dichiarare che i rami sui select annidati sono difensivi e irraggiungibili dal parser. Oggi il report dice «dentro un'opzione un select annidato non si legge», come se fosse un caso reale.

**Prove eseguite**: lexbor 38 passed con Python 3.13.16 e selectolax; 3 passed e 35 skipped con 3.11 senza selectolax; suite web con `-k web` 480 passed, 1 skipped. Ho provato 10 mutanti (5 presi, 5 sopravvissuti, descritti sopra) e 22 sonde sui casi limite. Il file modificato per i mutanti è stato ripristinato: SHA dello stage invariato, nessuna modifica fuori stage.

**Rischio escluso**: non ho rifatto l'oracolo html5lib sulle 60 mila pagine né il confronto sulle 131 pagine locali: mi sono fidato delle misure dell'autore. Non ho verificato nel vero Chrome come appaiono le opzioni dentro un details chiuso o un dialog chiuso dentro il select (Gas legge la prima e scarta la seconda, quindi nel peggiore dei casi perde testo, non lo fa uscire). Non ho verificato il comportamento sul VPS: ambiente non disponibile qui.

**Memoria**: riga #527 e 2 lezioni (selectolax: `is` contro `mem_id` e costo delle risalite; guardie su liste di tag da provare col mutante che toglie la lista). Commit atomico 3a23c4f fatto con `commit_memoria_revisore.sh`; i file del diff restano in stage.

File: /home/user/Gas/modules/web/lexbor.py, /home/user/Gas/tests/test_unit_web_lexbor.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #528 (chat Mani) — dopo la chiusura di R-527-1..4

## VERDETTO: APPROVATO CON RISERVE

Review #528 (chat Mani). È la seconda revisione, dopo la #527, del diff in stage (`git diff --cached`) sul branch claude/peaceful-lovelace-0w2b7q (PR #277). Prima della review ho letto CLAUDE.md, le voci di reports/stato_progetto.md su R-527 e lexbor, e la coda di memoria_revisore.md. Il diff non contiene antipattern: niente slicing della history, niente simulazione dei tool. I guardrail (10 iterazioni, `_get_window`, fail-safe §9) non vengono toccati. Se il figlio cade, si torna alla lettura normale di leggi.py.

**Elementi del diff esaminati**
- `modules/web/lexbor.py:78` — `opzioni_visibili` raccoglie le opzioni con una pila di iteratori, senza ricorsione. — Rischio: perdere guardie rispetto alla vecchia `visibile_in`. — **ok**. Le guardie ci sono tutte: tag nascosti, `nascosto()` (hidden e dialog chiuso), select annidati, nessuna discesa dentro le opzioni. Prove:
  - dialog chiuso → D2, dialog aperto → D1;
  - optgroup hidden → H2;
  - template, noscript e math (con il `_TAG_NASCOSTI` vero) → la seconda opzione.
  
  Mutanti presi (1 failed ciascuno): versione quadratica, senza tag nascosti, senza `nascosto`.
- `modules/web/lexbor.py:87` — salta i nodi non elemento. — Rischio: guardia senza test. — **riserva (R-528-1)**. Ho verificato che `attrs` su un commento solleva TypeError («attrs is only available for element nodes»). Il mutante senza questa riga però passa 52/52: il figlio esce con 1, e il ripiego di leggi.py nasconde i commenti lo stesso. Il caso a `tests/test_unit_web_lexbor.py:78` passa da `_componi` e quindi non distingue lexbor dal ripiego.
- `modules/web/lexbor.py:95` — `intero()` legge `size`. — Rischio: divergenze dalle regole HTML degli interi non negativi. — **ok**. Risultati: `+2` → lista; `-2`, `0` e `''` → tendina; `' 2'` e `3abc` → lista; `1_0` e la cifra araba → tendina. Il mutante senza `lstrip` viene preso (1 failed).
- `modules/web/lexbor.py:113` — tendina chiusa: l'ultima `selected`, altrimenti la prima libera. — Rischio: scostamento dallo standard. — **ok per il segnaposto `hidden selected`**: la selectedness esplicita vince anche se l'opzione è hidden o disabled (S1 mostrato); con tutte le opzioni disabled non si mostra niente. **Riserva cosmetica (R-528-2)** sul caso senza `selected`. Mutanti presi: «libere con hidden», «scelte senza hidden», «lista con hidden».
- `tests/test_unit_web_lexbor.py:135` — test di tempo, < 2 s. — Rischio: test instabile. — **ok**. Tempi misurati:
  - a riposo, 8 ripetizioni: 0,43–0,54 s;
  - con 8 processi che consumano CPU su 4 core: 1,0–1,27 s, margine circa 1,6x.
  
  Il mutante quadratico viene preso. In CI il test è saltato perché selectolax non è installato.
- Contesto: `modules/web/leggi.py:1431` — il chiamante passa `_TAG_NASCOSTI` e `_Estrattore._BLOCCHI`. Il diff non lo tocca.

**Riserve**
- **R-528-1 BASSA**: la guardia `is_element_node` a `modules/web/lexbor.py:87` non è fissata da nessun test. Il mutante finisce nel ripiego e passa. Correzione: aggiungere `assert lexbor.testo_visibile("<select><!--W1--><div><!--W2--><option>W3</option></div></select>", frozenset(), frozenset()) is not None` (meglio con il valore esatto).
- **R-528-2 COSMETICA**: con `<select><option hidden>W1<option>W2</select>` lo standard mostra W1 (la selezione automatica prende la prima opzione non disabilitata, hidden non conta); Gas mostra W2.
  - Il commento a `modules/web/lexbor.py:111` dice «la prima non disabilitata», ma il codice a `modules/web/lexbor.py:114` esclude anche le nascoste, e il test lo fissa.
  - Non è una fuga da un contenitore nascosto: W2 si vede nel menu aperto.
  - Da allineare allo standard, oppure da dichiarare come scelta.
- **R-528-3 COSMETICA**: lexbor annida le option una dentro l'altra (`<select><option>A<div><option selected>B` → B dentro A, verificato con `.html`).
  - Oggi si mostra A con il testo «AB». Per quanto ne so è coerente con lo standard, dove le opzioni annidate non entrano nella lista.
  - Però il mutante «scende nelle opzioni» sopravvive: nessun test fissa questo comportamento.
  - Sopravvivono anche i mutanti difensivi `!= "select"` (`modules/web/lexbor.py:91`) e `dentro_opzione` (`modules/web/lexbor.py:144`). Sono equivalenti, come già dichiarato per R-527-4.

**Rischi esclusi**
- Non ho fatto un confronto su un browser reale (Chrome/Firefox) per i casi del segnaposto hidden e delle option annidate: in questo ambiente non c'è un browser. R-528-2 e R-528-3 si basano sulla mia lettura dello standard HTML.
- Non ho rifatto il fuzz con l'oracolo html5lib sulle 60 mila pagine: il dato è dell'autore.
- Non ho rivisto la logica della sonda (`MAX_SONDE`), già approvata nella #527.

**Prove eseguite**
- Lexbor: 52 passed su 3.13.16 con selectolax 1.0.2; 3 passed e 49 skipped su 3.11.
- Web più lexbor: 493 passed, 1 skipped.
- 11 mutanti in tutto, poi file ripristinato: `git diff modules/web/lexbor.py` vuoto, stage intatto.

**Memoria**: aggiunta la riga #528 con una lezione nuova (le guardie del figlio vanno provate con `testo_visibile(...) is not None`, non solo con il testo finale passato da `_componi`). Commit d4ac3c9, fatto con `scripts/commit_memoria_revisore.sh`. I due file del diff restano in stage.

File:
- /home/user/Gas/modules/web/lexbor.py
- /home/user/Gas/tests/test_unit_web_lexbor.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #529 (chat Mani) — dopo la chiusura di R-528-1/2, diff committato in 0418f37

## VERDETTO: APPROVATO CON RISERVE

Review #529 (chat Mani). Fetta 20, terzo giro sulla PR #277. Ho esaminato il diff in stage: `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py`, 195 righe aggiunte e 38 tolte. Lo stage non è stato toccato.

Letture obbligatorie fatte: CLAUDE.md §5, reports/stato_progetto.md (voce fetta 20), memoria_revisore.md (#527, #528 e lezioni).

**Elementi del diff esaminati**
1. `tests/test_unit_web_lexbor.py:136` — nuovo test `test_commenti_nel_select_restano_a_lexbor`. Chiama `testo_visibile` direttamente e verifica sia `is not None` sia il testo esatto `["W3"]`.
   - Rischio: il test passa anche quando il figlio cade e scatta il ripiego (lezione di #528).
   - Prova col mutante che toglie la guardia di `modules/web/lexbor.py:87`: fallisce SOLO questo test (1 fallito, 52 passati). Il caso parametrico gemello passa ancora tramite il ripiego, quindi questo test serve davvero.
   - Esito: ok. **R-528-1 CHIUSA.**
2. `modules/web/lexbor.py:115` — `libere` filtra solo `disabled`, cioè la selezione automatica dello standard (l'attributo hidden non conta). `modules/web/lexbor.py:116` tiene l'ultima opzione con selected, se no la prima libera. `tests/test_unit_web_lexbor.py:83` ora si aspetta W1.
   - Rischio: un'opzione nascosta potrebbe far uscire testo da un contenitore nascosto.
   - Non succede: `opzioni_visibili` (`modules/web/lexbor.py:78`) scarta ancora i sotto-alberi nascosti PRIMA del filtro, e il commento a `modules/web/lexbor.py:111` ora descrive il codice.
   - Esito: ok. **R-528-2 CHIUSA.**
3. `modules/web/lexbor.py:104` — `opzioni()`, verificata con alcune pagine di prova lanciate direttamente.
   - `<select><optgroup disabled><option>A</optgroup><option>B</select>`: Gas mostra A, mentre per lo standard un'opzione dentro un optgroup disabilitato è disabilitata e il browser mostra B.
   - Esito: riserva, vedi R-529-1.

**Mutanti** (su una copia del repo nella scratchpad), tutti presi:
- senza la guardia sui commenti
- `libere` che esclude anche le hidden
- `libere = tutte` (senza filtro disabled)
- prima opzione selected invece dell'ultima
- ultima opzione libera invece della prima
- senza il controllo hidden su html
- sonde spente al primo fallimento

**Test**: lexbor 53 passati; web 495 passati e 1 saltato su Python 3.13.16 con selectolax 1.0.2. Il 495 al posto del vostro 494 viene dal filtro `-k web`, che prende un test in più.

**Riserve**
- R-529-1 (chat Mani), COSMETICA: Gas non considera disabilitate le opzioni dentro `<optgroup disabled>`, quindi nella tendina chiusa sceglie l'opzione sbagliata. Non fa uscire testo nascosto: è solo una differenza dal browser. Si corregge in `modules/web/lexbor.py:115` guardando anche il genitore optgroup.
- R-528-3, COSMETICA (option dentro option): resta dichiarata e non corretta, come da vostra scelta.

**Rischi esclusi**
- Su Python 3.11 non ho rieseguito: lì manca selectolax e i test lexbor vengono saltati.
- Non ho controllato con un browser vero cosa mostrano Chrome e Firefox per una tendina con tutte le opzioni disabilitate: mi baso sul testo dello standard.
- Wall of Shame: nessuno slicing della history né simulazione dei tool. Il diff non tocca kernel e provider.

Memoria aggiornata con la riga #529 (chat Mani) e una lezione (il «disabled» di un'opzione comprende l'optgroup disabilitato che la contiene). Committata da sola nel commit 4f30374: `/home/user/Gas/.claude/agents/memoria_revisore.md`.

Nota: in quel file la riga #528 compare due volte (riga 901 e penultima riga). Non l'ho toccata: va sistemata a mano.

### Review #530 (chat Mani) — merge di origin/main 932ecd6 in 7e2622f

## VERDETTO: APPROVATO

Review #530 (chat Mani): merge di origin/main 932ecd6 (PR #276 e #278) nel branch claude/peaceful-lovelace-0w2b7q (PR #277, HEAD 0c2a5c8, base c75f462). Il merge è ancora in corso (MERGE_HEAD presente).

Letture fatte: CLAUDE.md (sezioni 5, 8 e 9), reports/stato_progetto.md (testata), memoria_revisore.md (coda e lezioni sui merge #444 e #478). Applicata la lezione delle #444/#478: in una review di merge si citano con path:riga solo i file che restano nel diff dopo il merge, cioè l'area web. gas.py esce dal diff di sessione, quindi lo cito a parole.

**Elementi del diff esaminati**
- `modules/web/lexbor.py:198` — `testo_visibile` della fetta 20 lexbor. Rischio: che il merge abbia alterato il codice della PR. Esito: ok. I blob in stage di tutti i file `modules/web/*` e `tests/test_unit_web_*` sono identici a HEAD (0 differenze). `git diff --cached MERGE_HEAD` mostra come file di motore solo `modules/web/leggi.py`, `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py`, cioè esattamente quello che la PR cambia dalla base.
- `tests/test_unit_web_lexbor.py:136` — test diretto di `testo_visibile` con asserzione `is not None` (chiusura R-528-1). Rischio: che sia andato perso o modificato nel merge. Esito: ok, il blob è uguale a HEAD; suite web lexbor+leggi: 494 passati, 1 saltato.
- `modules/web/lexbor.py:63` — l'insieme `nascosti` del figlio. Rischio: che le modifiche di main a gas.py (solo commenti in `_memoria_pin`) tocchino il web. Esito: ok, nessuna dipendenza. main dalla base cambia solo gas.py (+7/-4, commenti), tests/test_unit_kernel.py (+12, test T21b2), coda_notte, memoria e reports.
- Contesto, gas.py (non più nel diff dopo il merge): il blob in indice e nel working tree è uguale a MERGE_HEAD (b822399). Lo stesso vale per tests/test_unit_kernel.py (8885d7b) e per reports/coda_notte.md. Il merge non altera il codice di main. Kernel: 1039 PASS, 1 FAIL (T31g, manca sqlite_vec nell'ambiente, noto); T21b2 PASS.

**Unione dei file in conflitto**
- `.claude/agents/memoria_revisore.md`: unione esatta delle righe di base, nostro lato e main (contate come multinsieme). 0 righe perse, 0 in più. Prima ci sono le nostre #525–#529 Mani, poi #526 Notte con la sua lezione.
- `reports/stato_progetto.md` riga 4: verificata confrontando le stringhe. Risulta voce Mani (fetta 20), poi voce Motore (V-1 ve #273, review #526), poi la coda comune, che è identica sui due lati. Il resto del file viene da main (blocco «Notte — contatti illeggibili», unito senza conflitti).
- 0 marcatori di conflitto nei file in stage.
- handoff, ultimo_report e diff_sessione presi dal nostro lato: corretto, sono log di sessione.

**Rischio escluso**: non ho riprovato la fetta 20 lexbor nel merito (mutanti, comportamento del figlio). È già coperta dalle review #525–#529 e il merge non tocca quei byte. Non ho verificato la suite con sqlite_vec installato (T31g), perché la libreria manca in questo ambiente.

**Note BASSE**
- La voce in stato_progetto.md presa da main dice «chat Motore», mentre la riga in memoria è «#526 (chat Notte)». È un'incongruenza del lato main, non del merge.
- Il numero #526 è usato da due chat (Mani e Notte): accettato dalla regola 4 di lavoro_parallelo.md.

**Memoria**: la riga #530 (chat Mani) è in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, solo nel working tree. Non l'ho messa in stage né committata: lo stato è ora «MM», quindi va aggiunta allo stage (`git add`) prima del commit di merge. Gli altri file in stage non li ho toccati. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati), codice finale 0418f37:
- `python3 -m pytest -q tests/test_unit_web_*.py`: main `463 passed, 1 skipped` → ramo `494 passed, 1 skipped in 30.76s` (3.13.16, con selectolax); `444 passed, 51 skipped in 25.98s` (3.11 locale, senza selectolax). `tests/test_unit_web_lexbor.py` da 22 (main) a 53 test.
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin): `484 passed, 11 skipped in 29.89s`.
- Suite vecchia con `GAS_WEB_LEXBOR=1` (test lexbor esclusi): `11 failed, 430 passed, 1 skipped, 53 deselected in 43.33s` (gli stessi 11 della fetta 19).
- Mutanti di questo giro (uscita di pytest sui test lexbor): senza guardia sui commenti `1 failed, 52 passed in 6.24s`; scelta automatica che salta anche le hidden `1 failed, 52 passed in 6.21s`; scelta automatica senza filtro disabled `1 failed, 52 passed in 5.94s`.
- Dopo il merge 7e2622f: web suite `494 passed, 1 skipped in 31.62s`; `python3 tests/test_unit_kernel.py` → `=== RIEPILOGO: 1039 PASS, 1 FAIL ===` (`FAIL: T31g gate env GAS_VECTORS=1 costruisce il vector store`: sqlite_vec assente nell'ambiente, fallisce identico su main pulito, fuori scope).
- Oracolo html5lib (script nello scratchpad), 60 mila pagine senza template/svg/math: fughe con lexbor 0 + 0 + 0, oggi 48 + 40 + 41; con i casi nuovi (body/html hidden, details, option, dialog) 2 fughe su 60 mila, entrambe `<title>` dentro `<select>` dove html5lib segue il select vecchio. Corpus: 131 pagine, 125 con le stesse parole (le 2 pagine COPYRIGHT di Rust perdono le licenze dentro 2.659 `<details>` chiusi).

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run lette dall'integrazione GitHub (`actions_list`, workflow ci.yml, branch claude/peaceful-lovelace-0w2b7q, evento push). Istantanea al momento della scrittura: lo stato aggiornato è sulla PR.

```
40522410245  CI  push  in_progress  —        7e2622f  2026-10-27T14:34:31Z
40518337629  CI  push  completed    success  0c2a5c8  2026-10-27T14:08:54Z
40517590660  CI  push  completed    success  0418f37  2026-10-27T14:03:56Z
40514061503  CI  push  completed    success  33e0d42  2026-10-27T13:40:05Z
40510534646  CI  push  completed    success  dbe5efc  2026-10-27T13:16:05Z
40510137001  CI  push  completed    failure  ab5eb1d  2026-10-27T13:13:20Z
```

Mappatura commit→run:
- `7290177`, `88dd43a`, `ffe99a8`: nessuna run su questo SHA (pushati insieme a `ab5eb1d`).
- `ab5eb1d` → run 40510137001, failure (pushato prima dell'handoff della fetta: il commit di fine-task successivo è verde).
- `dbe5efc` → run 40510534646, success.
- `33e0d42` → run 40514061503, success.
- `3a23c4f`, `d4ac3c9`, `4f30374`: nessuna run su questo SHA (pushati insieme a `0418f37`).
- `0418f37` → run 40517590660, success.
- `0c2a5c8` → run 40518337629, success.
- `7e2622f` → run 40522410245, in corso alla scrittura dell'handoff.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

Bot e verifica esterna su 0c2a5c8 (commento: https://github.com/Gasss23/Gas/pull/277#issuecomment-6444617794): APPROVATO CON RISERVE. Chiuse: conflitto con main (merge 7e2622f), descrizione della PR. Aperte:
- R-ve277-3 COSMETICA: opzione dentro un sotto-albero `hidden` esce dai candidati della scelta (verso sicuro).
- R-ve277-4 COSMETICA: fuori da Linux 3 sonde a 600 s prima di spegnere; docstring di `test_sonda_oltre_il_tempo_si_riprova` superata.
- R-bot277-4 BASSA: tetto assoluto di 2 s in `test_molte_opzioni_annidate_restano_lineari`, a rischio di falsi rossi quando selectolax entra in CI.
- R-ve277-5 BASSA PREESISTENTE: video/audio, meter/progress e figli «light» di un host shadow escono anche oggi.
- R-529-1 COSMETICA: opzione dentro `<optgroup disabled>` non considerata disabilitata (tendina chiusa: si legge l'opzione sbagliata, mai testo nascosto).
- R-528-3 COSMETICA: option dentro option, comportamento senza test (dichiarato).
- R-526-1 COSMETICA: doppio controllo sotto lock in `attivo()` senza test.
- R-520-4 COSMETICA: un `title` HTML dentro foreignObject si scarta.
- Prima dell'accensione: selectolax in requirements e CI (chat Motore), così i 50 test lexbor oggi saltati girano.
- Restano decisioni dell'operatore: R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s.
