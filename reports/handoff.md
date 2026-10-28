# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Mani fetta 24: riserve cosmetiche di lexbor con i namespace come il parser (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #294 (https://github.com/Gasss23/Gas/pull/294). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5059595040","url":"https://github.com/Gasss23/Gas/pull/294"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve l'OK dell'operatore. Il merge non accende niente.
2. Accensione della lettura con lexbor: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (chiude R-ve280-1); poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Poi, una alla volta: R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #288 (fetta 23)**: `FATTA` — richiesta dell'operatore («mergia 288»), merge d4b39ca, dopo il merge di main 2f35bc6; branch ripartito da main.
- **Fetta 24 — riserve cosmetiche di lexbor (punto d della ripartenza)**: `FATTA`.
  - R-ve277-3 e R-529-1 (scelta della tendina, «list of options» dello standard, optgroup disabled più vicino, solo opzioni HTML): `FATTA`.
  - R-520-4 (title HTML in foreignObject, discesa lineare): `FATTA`.
  - R-540-1 (slot HTML in foreignObject): `FATTA`.
  - R-ve277-4 (`attivo()` spenta fuori da Linux): `FATTA`.
  - R-526-1 e R-528-3 (test): `FATTA`. R-543-1 (commento): `FATTA`.
  - Shadow vuoto (bot #288 su 759edea): `FATTA` (test).
  - V-1 bot e ve #288 su 6627250 (adoption agency): `FATTA` come limite dichiarato (commento e test dell'esito di oggi); comportamento del browser non riprodotto.
  - B-547-1 MEDIA (review #547: punti d'integrazione dal solo nome) → namespace come il parser: `FATTA`, review #548; R-548-1/2: `FATTA`, review #549.
- **Accensione lexbor (punto b)**: `DEFERITA — chat Motore`.
- **Decisioni vecchie (punto e)**: `DEFERITA — una alla volta dopo questa fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/web/lexbor.py              | 130 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------
 reports/diff_sessione.md           |  14 ++++++-------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   6 +++---
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  53 +++++++++++++++++++++----------------------------
 tests/test_unit_web_lexbor.py      |  92 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----
```

NB: base = merge-base con origin/main = d4b39ca. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
ca6f289 fix(web): riserve cosmetiche di lexbor con i namespace come il parser (fetta 24 Mani)
0254e80 chore(revisore): memoria review #549 — APPROVATO
3b8c150 chore(revisore): memoria review #549 — APPROVATO
c1289e7 chore(revisore): memoria review #548 — APPROVATO CON RISERVE
12affec chore(revisore): memoria review #547 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore ca6f289: review #547 BOCCIATO sul primo diff (B-547-1), #548 APPROVATO CON RISERVE sul diff corretto, #549 APPROVATO dopo i test di R-548-1/2 (diff committato in ca6f289). Verdetti integrali:

### Review #547 (chat Mani) — primo diff staged

## VERDETTO: BOCCIATO

Review #547 (chat Mani). Diff staged su claude/peaceful-lovelace-0w2b7q (base d4b39ca): modules/web/lexbor.py e tests/test_unit_web_lexbor.py.

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 10), reports/stato_progetto.md (riga 4 e paragrafi Mani 627-650), .claude/agents/memoria_revisore.md (lezioni lexbor #525-#546, in particolare: rileggere lo standard alla fonte, #938).

**Motivo bloccante, B-547-1 (MEDIA): regressione con fuga nel titolo.** Il diff riconosce i punti d'integrazione dal solo nome del tag. Lo standard però li lega al namespace (whatwg/html main, sorgente righe 145897-145922):
- punti d'integrazione HTML: SVG foreignObject, desc, title e MathML annotation-xml con encoding;
- punti d'integrazione di testo MathML: mi, mo, mn, ms, mtext.

selectolax non espone il namespace. Ho controllato i namespace con html5lib, che fa da oracolo indipendente. Queste quattro pagine ora danno titolo «X», mentre HEAD dava «Y», che è quello del browser:
- `<math><desc><title>X</title></desc></math><title>Y</title>`
- `<svg><mi><title>X</title></mi></svg><title>Y</title>`
- `<svg><math><mi><title>X…` (il math dentro svg è un elemento SVG)
- `<math><mrow><svg><foreignObject><title>X…` (l'svg dentro mrow è un elemento MathML)

In tutti e quattro il title è straniero e il browser non lo usa come titolo. Il testo nascosto entra quindi nella riga «Titolo:». È la stessa classe di V-1 ve #246 bis (annotation-xml preso sempre come punto d'integrazione), allora valutata ALTA. Qui la tengo MEDIA perché lexbor è spenta e le pagine sono costruite apposta. Il rimedio costa poco.

**Elementi del diff esaminati:**
1. `modules/web/lexbor.py:74` — INTEGRAZIONE elenca nomi senza namespace — rischio: punto d'integrazione falso dentro svg o math — **blocco** (B-547-1).
2. `modules/web/lexbor.py:88` — il title vale se la risalita trova `integrazione(sopra)` — rischio: fuga e costo — **blocco** per la regressione sopra. Sul costo: la risalita era già quadratica, ora è circa 2 volte più lenta. Con svg + 1000 `<g>` + 10000 title (163 KB) si passa da 1,68 s a 4,01 s: oltre TEMPO_MAX, quindi si usa la lettura di sempre, nessun crash.
3. `modules/web/lexbor.py:192` — primi_slot esce dallo straniero con `integrazione(nodo)` — stessa causa — **riserva**. `<div><template shadowrootmode=open><svg><mi><slot></slot></mi></svg><slot>Q</slot></template>L</div>` dà «LQ» invece di «L». In produzione svg è nascosto, quindi L si perde.
4. `modules/web/lexbor.py:112` — opzioni_visibili salta tutto svg e math — **riserva** (BASSA/COSMETICA). Lo standard non salta lo straniero. Un'opzione HTML dentro foreignObject o mi è nella list of options (l'albero di lexbor la tiene: `<select><svg><foreignObject><option selected>W1` → oggi W2). Il commento la presenta come regola dello standard, invece è una scelta in più.
5. `modules/web/lexbor.py:112` — sul resto della list of options, riletto alla fonte (sorgente riga 57728): select, hr, option, datalist e optgroup annidato coincidono. «concept-option-disabled» (sorgente riga 58659, antenati dal più vicino) coincide con gruppo_spento. Ultima «selected» poi prima non disabilitata (sorgente righe 57800-57840) coincide. Esito **ok**. Sonde: optgroup disabled con selected → W1; hr, div disabled, optgroup hidden nella lista: tutte giuste.
6. `modules/web/lexbor.py:296` — attivo() spenta fuori da Linux prima delle sonde — **ok**. `tests/test_unit_web_lexbor.py:294` la prova vietando `_esegui`.
7. `tests/test_unit_web_lexbor.py:305` — lock finto che fa finire la sonda «all'altro» — rischio: test che non morde — **ok**. Senza il doppio controllo si chiama `_esegui` e scatta l'AssertionError.
8. `tests/test_unit_web_lexbor.py:106` e `tests/test_unit_web_lexbor.py:185` — allineamento allo standard (opzione in un div hidden scelta dalla tendina) e limite dell'adoption agency fissato a «LX» — **ok**.
9. `tests/test_unit_web_lexbor.py:112`, `tests/test_unit_web_lexbor.py:115` e `tests/test_unit_web_lexbor.py:163` — coprono solo i casi positivi (foreignObject, mi, encoding maiuscolo) — **riserva**: manca un caso negativo per ogni namespace sbagliato.

**Rimedio proposto:**
- Una sola discesa lineare dall'alto (pila di iter, come primi_slot) che porta il namespace corrente:
  - da HTML, `svg` apre SVG e `math` apre MathML;
  - dentro lo straniero ogni elemento resta nel namespace del padre, tranne `svg` figlio di annotation-xml, che è SVG (confermato con html5lib);
  - i figli di un punto d'integrazione del namespace giusto tornano HTML.
- La stessa discesa serve per il primo title HTML (chiude anche il costo quadratico), per primi_slot e per opzioni_visibili (opzione contata solo in HTML).
- Test negativi da aggiungere: le quattro pagine sopra → titolo «Y»; lo slot in `svg mi` → «L»; un test di tempo con 1000 `<g>` e 10000 title entro TEMPO_MAX.

**Prove rifatte:** test lexbor 118 passed, suite web (`-k web`) 560 passed / 1 skipped (3.13 + selectolax 1.0.2). Confronto HEAD/staged eseguendo il modulo di HEAD copiato nello scratchpad.

**Rischi esclusi:**
- Non ho rifatto la suite su 3.11 senza selectolax né la suite vecchia con GAS_WEB_LEXBOR=1 (11 failed / 430 passed): il diff non tocca leggi.py e il dato era già dichiarato.
- Non ho rifatto i mutanti dichiarati dall'agente: il blocco nasce da pagine che nessun test copre, non dalla forza dei test esistenti.
- Il comportamento dei browser reali (Chrome, Firefox) non è verificato: ho usato lo standard e html5lib come oracolo.

Wall of Shame: nessuno slicing di history (`scelte[-1:]` e `libere[:1]` sono liste di opzioni, preesistenti), nessuna simulazione di tool. Fail-safe §9 intatto: un errore o il tempo oltre il tetto nel figlio portano alla lettura di sempre.

Memoria: riga `#547 (chat Mani)` e una lezione nuova (punti d'integrazione per namespace, con le sonde da usare) aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate con lo script (12affec). Il diff staged sotto review è rimasto intatto.

### Review #548 (chat Mani) — diff corretto dopo B-547-1

## VERDETTO: APPROVATO CON RISERVE

Review #548 (chat Mani): correzione della bocciatura B-547-1 (#547), diff staged su claude/peaceful-lovelace-0w2b7q (modules/web/lexbor.py, tests/test_unit_web_lexbor.py). La review #547 era BOCCIATO e resta nel report: punti d'integrazione riconosciuti dal solo nome, con fuga di un title svg o math nel titolo della pagina.

**B-547-1 è chiusa.** Restano due riserve piccole, che non bloccano il commit:
- **R-548-1 (BASSA, test)**: due mutanti miei sopravvivono, ma il codice è giusto. Bastano due righe parametriche.
  - Se si toglie `"testo"` dalla prima tupla di `ns_di`, un svg dentro mi verrebbe preso come HTML. Test da aggiungere: `<math><mi><svg><title>X</title></svg></mi></math><title>Y</title>` → titolo «Y».
  - Se si toglie `html and` dal salto di select/hr/datalist, un datalist svg verrebbe saltato. Test da aggiungere: `<select><svg><datalist><foreignObject><option selected>W1</option></foreignObject></datalist></svg><option>W2</select>` → «W1».
  - Sonde sul codice: «Y» e «W1», giusti. File ripristinato, nessuna modifica residua.
- **R-548-2 (COSMETICA)**: il commento in `tests/test_unit_web_lexbor.py:76` dice «fuori dalla list of options solo datalist e svg». Ora svg non si salta più: solo le sue opzioni non sono HTML.

**Elementi del diff esaminati:**
1. `modules/web/lexbor.py:78` — `ns_figli`: punti d'integrazione solo nel namespace giusto (foreignObject, desc e title in svg; mi, mo, mn, ms, mtext e annotation-xml con encoding HTML in math). Rischio: fuga nel titolo. Confrontato col dispatcher dello standard (whatwg/html main, sorgente righe 145897-145922, già riletto in #547). **ok**
2. `modules/web/lexbor.py:89` — `ns_di`: da HTML, svg e math aprono il loro namespace; dentro mi, mglyph e malignmark restano math e il resto torna HTML; un svg dentro annotation-xml senza encoding diventa svg; nello straniero si resta nel namespace del padre (svg in mrow resta math). Coincide coi namespace di html5lib, provati in #547. **ok**, con R-548-1 sui test.
3. `modules/web/lexbor.py:98` e `modules/web/lexbor.py:114` — discesa lineare per il titolo, più una scorciatoia `css_first("title")` per le pagine senza svg e math. Rischio: costo. Svg con 1000 `<g>` e 10000 title: 4,01 s → 0,06 s. Altre forme: 0,04-0,07 s. **ok**
4. `modules/web/lexbor.py:144` — `opzioni_visibili` conta solo le opzioni HTML ed entra in svg e math. Sonde: opzione in foreignObject o in mi → scelta W1, come lo standard (list of options, sorgente riga 57728); optgroup disabled annidati, hr, div disabled: tutti giusti. Costo: select con 50k opzioni sotto 2000 div, 0,98 s. **ok**
5. `modules/web/lexbor.py:214` — `primi_slot` conta solo gli slot HTML. Sonde: slot in svg>mi → «L»; in svg>desc e math>mi → «LQ» (punti d'integrazione veri). **ok**
6. `tests/test_unit_web_lexbor.py:122`, `tests/test_unit_web_lexbor.py:174` e `tests/test_unit_web_lexbor.py:308` — test negativi coi quattro casi di #547, slot svg>mi, test di tempo. **ok**

**Prove rifatte:**
- Le sonde di #547 ora danno tutte l'esito dello standard (titolo «Y» nei quattro casi).
- Fuzz mio contro html5lib: 1500 pagine casuali di soli tag di apertura (svg, math, foreignObject, desc, mi, mtext, mglyph, malignmark, mrow, annotation-xml con e senza encoding, custom element), 0 differenze sul titolo.
- Test lexbor 123 passed (3.13); su 3.11 senza selectolax 22 passed / 101 skipped.
- Suite web: 565 passed / 1 skipped. L'agente dichiarava 564, un test in più nel mio filtro `-k web`.

Wall of Shame: nessuno slicing di history, nessuna simulazione di tool. Fail-safe intatto: un errore nel processo figlio fa usare la lettura di sempre.

**Rischi esclusi:**
- Fuzz con tag di chiusura e opzioni nei select non rifatto. html5lib usa ancora il parser vecchio dei select, quindi non fa da oracolo. Per i tag di chiusura vale la forma diversa dell'albero tra lexbor e html5lib, già dichiarata dall'agente: sul suo esempio non ho verificato quale albero abbia ragione.
- Suite vecchia con GAS_WEB_LEXBOR=1 (11 failed / 430 passed) non rifatta: leggi.py non è nel diff.
- I mutanti dichiarati dall'agente non li ho rifatti, solo i miei due.

Memoria: riga `#548 (chat Mani)` aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata (c1289e7). Nessuna lezione nuova: quella sui namespace è già in #547 (12affec). Il diff staged è intatto.

### Review #549 (chat Mani) — diff committato in ca6f289

## VERDETTO: APPROVATO

Review #549 (chat Mani): R-548-1 e R-548-2 sono chiuse. Il diff staged su claude/peaceful-lovelace-0w2b7q cambia, rispetto alla #548, solo tests/test_unit_web_lexbor.py. Il codice del processo figlio in modules/web/lexbor.py è identico a quello revisionato in #548: l'ho confrontato con `cmp` sulla versione staged.

**Elementi del diff esaminati:**
1. `tests/test_unit_web_lexbor.py:130`: la pagina `<math><mi><svg><title>W1</title></svg></mi></math><title>W2</title>` deve dare il titolo W2. Rischio verificato: test che non morde. Rifatto il mio mutante su `modules/web/lexbor.py:89` (`"testo"` tolto dalla prima tupla di `ns_di`): 1 failed. **ok**
2. `tests/test_unit_web_lexbor.py:85`: un datalist svg dentro un select, con un'opzione HTML nel suo foreignObject, deve dare W1. Rifatto il mio mutante su `modules/web/lexbor.py:146` (`html and` tolto dal salto di select/hr/datalist): 1 failed. **ok**
3. `tests/test_unit_web_lexbor.py:76`: il commento ora dice che dalla list of options restano fuori le opzioni dentro datalist e quelle non HTML, mentre object e canvas restano dentro. È coerente con lo standard (list of options, sorgente whatwg/html riga 57728). **ok**

Dopo ogni mutante il file è stato ripristinato: working tree uguale allo staged, `git diff` vuoto.

**Prove rifatte:**
- Test lexbor: 125 passed su 3.13; 22 passed / 103 skipped su 3.11 senza selectolax.
- Suite web (`-k web`): 567 passed / 1 skipped. L'agente dichiarava 566: il mio filtro conta un test in più, come già in #548.

Wall of Shame: nessuna violazione, e il codice del motore non cambia rispetto alla #548.

**Rischi esclusi:**
- La suite vecchia con GAS_WEB_LEXBOR=1 non l'ho rifatta: in questo giro il diff tocca solo i test.
- Restano escluse le verifiche dichiarate in #548: fuzz con tag di chiusura e opzioni nei select, per cui html5lib non fa da oracolo.

**Memoria:** riga `#549 (chat Mani)` aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata (3b8c150), nessuna lezione nuova. Nella riga avevo citato una riga sbagliata (145 invece di 146) e l'ho corretta in un secondo commit (0254e80). Il diff staged sotto review è intatto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py; toccati solo `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py`.
- Web suite (`tests/test_unit_web_*.py`, Python 3.13.16 con selectolax 1.0.2): prima 546 passed / 1 skipped (main d4b39ca, misurato dalla verifica esterna #288 e dal revisore) → dopo 566 passed / 1 skipped (+20 casi).
- File lexbor su Python 3.11 senza selectolax (come la CI): 22 passed / 103 skipped.
- Suite vecchia con `GAS_WEB_LEXBOR=1` (`tests/test_unit_web_leggi.py`): 11 failed / 430 passed / 1 skipped, gli stessi 11 di sempre (fuori scope: differenze note tra lettura di sempre e lexbor).
- Mutanti presi; equivalente noto `continue` → `return None` su `template_fragments()` vuoto. Elenco in `reports/ultimo_report.md`.

## §6 STATO CI

CI NON VERIFICATA con `gh` (assente/non autenticato nel cloud). La PR #288 era verde sull'ultima head (run 40787359499: `unit-suite`, `handoff-check` success; `verifica-bot` success).

Mappatura commit→run:
- 12affec, c1289e7, 3b8c150, 0254e80: nessuna run su questo SHA (pushati insieme a ca6f289).
- ca6f289: run del push del codice (non letta alla scrittura).
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- V-1 bot e ve #288 BASSA: adoption agency che sposta il template dichiarativo (l'host perde lo shadow); dichiarata, test dell'esito di oggi.
- R-ve280-1 BASSA: i test del figlio lexbor con selectolax non girano nei check required (CI su 3.11 senza selectolax). Chat Motore.
- R-546-1 BASSA: numerazione doppia delle review tra le chat (#540–#542); dalla #547 numeri nuovi.
- Fuzz con end tag nello straniero: 3 differenze su 1500 tra lexbor e html5lib nella forma dell'albero (non nella deduzione del namespace); non verificato quale dei due segua lo standard di oggi.
