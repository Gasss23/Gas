# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — Chat Mani, fetta 5: riserve rimaste della lettura web (R6)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #242 (https://github.com/Gasss23/Gas/pull/242): vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

(`gh` non autenticato nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **R-442-1 / R-431-3 (contatore unico nel ripiego)**: `FATTA`
- **R-442-2 (commenti fasulli, regex finale tolta)**: `FATTA`
- **V-1 bot #239 (`<svg/>`/`<math/>` autochiusi)**: `FATTA`
- **V-1 bot #239 2° giro (virgolette nel tag di chiusura)**: `FATTA`
- **R-445-1 (grezzi come html.parser, grezzi autochiusi)**: `FATTA`
- **R-446-1 (`<script/>` sul percorso normale)**: `FATTA`
- **R-432-1, V-3 ve #239, V-2 bot #239 2° giro (cosmetiche)**: `FATTA`
- **R-447-1**: `DEFERITA — limite dichiarato (html.parser non entra in modalità grezza dopo «<script/>»); BASSA, nasconde comunque più di prima`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +++
 modules/web/leggi.py               | 104 +++++++++++++++++++++++++++++++++++++++++++++++++++++------------------
 reports/diff_sessione.md           |  11 ++++----
 reports/handoff.md                 | 528 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  33 ++++++++++-------------
 tests/test_unit_web_leggi.py       | 106 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 7 files changed, 344 insertions(+), 444 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
f583746 fix(web): fetta 5 chat Mani — ripiego con contatore come il parser, commenti fasulli, <script/> (R6)
b147ca6 chore(revisore): memoria review #447 — APPROVATO CON RISERVE
980997f chore(revisore): memoria review #446 — APPROVATO CON RISERVE
b49e2a7 chore(revisore): memoria review #445 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit, quindi le righe di `reports/handoff.md` possono differire di poco (l'elenco dei file è esatto).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Tre verdetti, incollati integralmente: #445, #446, #447 (chat Mani), tutti sul diff del commit `f583746` (i giri #445/#446 hanno chiuso le proprie riserve nello stesso diff; le righe di memoria sono nei commit `b49e2a7`, `980997f`, `b147ca6` fatti dal revisore).

### Review #445 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #445 (chat Mani), 2026-10-21. Fetta 5 Mani (R6), ramo feat/mani-web-fetta5, diff staged su `modules/web/leggi.py` e `tests/test_unit_web_leggi.py`. Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), le sezioni Mani di reports/stato_progetto.md e .claude/agents/memoria_revisore.md.

Non ci sono violazioni del Wall of Shame: il diff non tocca la history né `_get_window`, non simula tool e non indebolisce i guardrail. Il modulo resta fail-safe: `_testo_senza_parser` mantiene il try su `html_unescape`.

**Elementi del diff esaminati**
- `modules/web/leggi.py:91` — `_INIZIO_TAG` ora è un'unica alternanza che riconosce anche CDATA e i commenti fasulli `<!x`, `<?`, `</`. Rischio esaminato: ricerca quadratica (la lezione della #442). Esito ok: 1M di `<?`, `<!` o `</` richiede al massimo 0,003 s, e 500k `<?>` sono coperti dal test.
- `modules/web/leggi.py:107` — `_AUTOCHIUSO` senza gruppi di cattura, con la «/» lasciata fuori dal ciclo tramite `/(?!>)` alla `modules/web/leggi.py:104`. Rischi esaminati: una «/» che fa parte di un valore senza virgolette, e il SystemError su 3.11. Esito ok: le sonde `<svg a/>`, `<svg a="x"/>`, `<svg a='>'/>`, `<svg\n/>`, `<svg//>` e `<svg a=x/>` danno lo stesso risultato del parser; 2 MB di `<svg a=x/` richiedono 0,09 s.
- `modules/web/leggi.py:567` e `modules/web/leggi.py:569` — un contatore unico come in `_Estrattore` (`modules/web/leggi.py:436` e `modules/web/leggi.py:444`): scende solo se è maggiore di zero, e i grezzi sono consumati per intero. Rischi esaminati: contatore che va sotto zero, e una chiusura di un grezzo dentro svg (`<svg>x</script>VIS`). Esito ok: si comporta come il parser. L'accesso `basso[m.end()]` è sicuro, perché `fine_tag` esiste solo se dopo c'è un «>».
- `modules/web/leggi.py:498` — `_chiusura` ora finisce il tag di chiusura con `_FINE_TAG`. Rischio esaminato: tempo su chiusure con virgolette aperte. Esito ok: 300k `</svg a="` richiedono 0,05 s, e 100k `<script>x</script a="` sono nel test.
- `modules/web/leggi.py:580` — tolta la regex finale. Rischio esaminato: resti di markup nel testo. Esito ok: `a<1>b` e `<İ>` restano testo come nel parser, perché tutti i tag li toglie già il ciclo.
- `tests/test_unit_web_leggi.py:928` — test di confronto col parser su 4000 pagine casuali. Rischio esaminato: un alfabeto troppo stretto. Esito: riserva R-445-1 (sotto).

**Verifiche fatte (su una copia presa dall'index)**
- Suite: 158 passed su 3.13.16.
- Mutazioni, ciascuna con 1 FAIL (quindi tutte prese): guardia `and salta` tolta, autochiuso ignorato, chiusura al primo «>», CDATA al primo «>», math non autochiudibile, contati trattati come grezzi.
- Fuzz differenziale da 200k stringhe (alfabeto del test più tag composti come `<svg>` e `<svg/>`) su 3.13 e 3.11.17: 0 fughe. Un solo caso «altro», che rientra nella famiglia (b) qui sotto.
- 12 input avversari da circa 2 MB: tutti al massimo 0,54 s.

**Riserva**
- **R-445-1 (chat Mani), BASSA, preesistente (c'è anche a HEAD, non è una regressione).** Ci sono due famiglie in cui il ripiego mostra testo che il parser nasconde. Nessuna delle due è nell'alfabeto del test di confronto.
  - (a) html.parser, sia 3.13.16 sia 3.11.17 con le patch di sicurezza, tratta textarea, xmp, noembed e noframes come testo grezzo (`CDATA_CONTENT_ELEMENTS` e `RCDATA_CONTENT_ELEMENTS`), e plaintext fino alla fine della pagina. Esempio: `<svg><textarea></svg></textarea>SEGRETO</svg>VIS` porta SEGRETO nel ripiego, il parser no. Un fuzz con questi nomi trova circa 3.600 fughe su 200k pagine, su 3.13 e 3.11.
  - (b) Per html.parser `<script/>`, `<style/>`, `<iframe/>` e `<title/>` sono elementi vuoti. Il ripiego invece apre il blocco grezzo e inghiotte le aperture che il parser conta. Esempio: `<script/><svg><noscript></script>SEGRETO</noscript></svg>VIS`, e anche `<script/><!--</script>SEGRETO`.
  - Correzione provata in copia:
    1. aggiungere textarea, xmp, noembed, noframes e plaintext a `_GREZZI_RIPIEGO` (`modules/web/leggi.py:113`); per plaintext `fine = -1`, cioè resto della pagina;
    2. per un grezzo autochiuso (`_AUTOCHIUSO.match`): `salta += 1` se il nome è in `_TAG_NASCOSTI`, altrimenti ignorarlo. Così il contatore del ripiego resta sempre maggiore o uguale a quello del parser.
  - Risultato della copia: 158 passed, 0 fughe su 600k pagine (3.13 e 3.11), tempi uguali o migliori. Aggiungere quei nomi e le forme autochiuse agli atomi di `tests/test_unit_web_leggi.py:933`.
  - Perché BASSA: il ripiego non è raggiungibile con pagine vere, e il testo resta comunque dentro i marcatori NON FIDATO.

**Cosa NON ho verificato**
- Il comportamento con un html.parser di Python senza le patch recenti (per esempio una 3.11 vecchia su una VPS). Lì textarea e title non sono grezzi e la correzione proposta divergerebbe nel verso opposto. Non l'ho riprodotto: in questo ambiente ci sono solo 3.13.16 e 3.11.17, entrambe patchate.
- Non ho rifatto il fuzz da 500k dell'autore né tutte le sue 13 mutazioni: ne ho rifatte 6.

**Memoria del revisore**
- Riga #445 (chat Mani) e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate con scripts/commit_memoria_revisore.sh (commit b49e2a7). Il diff staged del motore resta intatto nell'index.
- Copia di lavoro, sonde, fuzz e prototipo in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r445 (il prototipo è nella sottocartella p).

---

### Review #446 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

**Review #446 (chat Mani), 2026-10-21.** È la ri-review della #445 sul diff staged del ramo `feat/mani-web-fetta5`, che contiene `modules/web/leggi.py` e `tests/test_unit_web_leggi.py` (tutta la fetta 5).

Ho fatto le letture obbligatorie: CLAUDE.md sez. 5, la sezione Mani di `reports/stato_progetto.md` e la memoria del revisore, comprese la lezione della #445 sugli alfabeti del fuzz e quella della #444 sulle citazioni.

**Elementi del diff esaminati**

1. `modules/web/leggi.py:117`: `_GREZZI_RIPIEGO` ora comprende textarea, xmp, noembed, noframes e plaintext.
   - Rischio esaminato: l'insieme deve coincidere con quello del parser di riferimento. Ho confrontato con il sorgente di html.parser 3.13.16: CDATA_CONTENT_ELEMENTS = script, style, xmp, iframe, noembed, noframes; RCDATA = textarea, title; plaintext ha un caso a parte.
   - Esito: **ok**. Insieme identico. noscript resta fra i contati, come nel parser, che lavora senza scripting.
2. `modules/web/leggi.py:570`: un grezzo autochiuso non salta il contenuto; se è fra i nascosti fa `salta += 1`.
   - Rischio esaminato: il contatore del ripiego deve restare sempre maggiore o uguale a quello del parser.
   - Sonde: `<script/>SEGRETO</script>VIS` dà « VIS» (il parser mostra SEGRETO, cioè il ripiego è nella direzione sicura); `<script/ a>` resta grezzo come nel parser; `<SCRIPT/>` e `<iframe/>` si comportano allo stesso modo; `<textarea/>VIS` e `<plaintext/>VIS` sono alla pari col parser.
   - Mutazioni in una copia presa dall'index: con «autochiuso non conta» e con «autochiuso salta il contenuto» fallisce 1 test in ciascun caso.
   - Esito: **ok**.
3. `modules/web/leggi.py:573`: plaintext porta via il resto della pagina.
   - Mutazione «plaintext come grezzo normale»: 1 FAIL, preso da `tests/test_unit_web_leggi.py:928`, che verifica anche una `</plaintext>` che non chiude.
   - Esito: **ok**.
4. `modules/web/leggi.py:580`: una chiusura di un nascosto scala il contatore solo se `salta` è maggiore di zero.
   - Mutazione «senza `and salta`»: 1 FAIL.
   - Esito: **ok**.
5. `modules/web/leggi.py:504`: in `_chiusura` la fine del tag di chiusura ora passa per `_FINE_TAG`, preceduto dal `find(">")`.
   - Rischio esaminato: tempo quadratico.
   - Prove su 2 MB, tutte entro 0,33 s: `<script/>`×N, `<textarea>`×N senza chiusura, coppie `<textarea>x</textarea>`, `<xmp>` + «</xmpx»×N, `<svg><noframes></svg>`×N, `<title/><svg>`×N, `<script/></script a=">">`×N.
   - Esito: **ok**.
6. `tests/test_unit_web_leggi.py:893` e `tests/test_unit_web_leggi.py:898`: le 5 sonde nuove nel parametrize, con `<script/>SEGRETO</script>VIS` come guardia contro la mutazione equivalente al parser.
   - Mutazione «noembed non grezzo»: 1 FAIL.
   - Esito: **ok**.
7. `tests/test_unit_web_leggi.py:940`: il confronto col parser, con gli atomi estesi a `tests/test_unit_web_leggi.py:948`.
   - Rischio esaminato: un test valido solo dentro il suo alfabeto (lezione della #445).
   - Ho scritto un fuzz mio, indipendente, con un alfabeto più ampio: le forme autochiuse di tutti i grezzi e di noscript/math, maiuscole (`SCRIPT`, `Svg`), `&#`, chiusure con spazio, `a=x/`, `<b/`. Risultato: 0 fughe su 150k pagine con 3.13.16 e 0 su 150k con 3.11.17.
   - Esito: **ok**.

Altre verifiche:
- Suite web: 165 passed su 3.13.
- Wall of Shame: il diff non tocca né la storia dei messaggi né `_get_window`. `testo[i:m.start()]` è uno slicing di stringa, non della cronologia.
- Il ripiego non solleva eccezioni, quindi resta fail-safe secondo la sez. 9.

**Riserva**

- **R-446-1 (chat Mani) BASSA, preesistente e fuori dal diff.** Sul percorso NORMALE, `<script/>TESTO</script>` mostra TESTO al modello; lo stesso vale per `<iframe/>…</iframe>` e `<SCRIPT/>`. Il punto di contesto è `modules/web/leggi.py:440`: html.parser chiama `handle_starttag` e subito `handle_endtag`, quindi il contatore torna a zero. I browser invece aprono lo script, per cui quel testo è codice invisibile a chi guarda la pagina: un canale di testo nascosto verso il modello. L'esposizione resta limitata, perché tutto il testo sta già dentro i marcatori NON FIDATO. Correzione suggerita: in `_Estrattore.handle_startendtag`, i nascosti che non sono vuoti (escluse svg e math) contano solo come apertura. Il ripiego di questa fetta lo fa già.

**Rischi esplicitamente esclusi**

- Non ho rieseguito la suite pytest completa su 3.11. Sul 3.11.17 ho girato solo il mio fuzz, che importa e usa il modulo: prova che le ripetizioni possessive compilano e che non ci sono fughe, non che i 165 test passino su 3.11. Mi baso sul vostro dato «165 passed su 3.11 (venv)».
- Non ho verificato il comportamento con pagine vere né su VPS. Il ripiego scatta solo se html.parser solleva un'eccezione, cosa non riproducibile con pagine reali (come già annotato nella fetta 4).

**Memoria:** riga #446 aggiunta in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata con `scripts/commit_memoria_revisore.sh` (commit 980997f, solo quel file). I due file staged sono rimasti intatti. Nessuna lezione nuova.

**File utili:**
- `/home/user/Gas/modules/web/leggi.py`
- `/home/user/Gas/tests/test_unit_web_leggi.py`
- fuzz: `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r446/fz.py`
- mutazioni: `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r446/mut.py`
- tempi e sonde: `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r446/tempi.py`

---

### Review #447 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #447 (chat Mani), 2026-10-21. È la ri-review della #446 sulla fetta 5 Mani, ramo feat/mani-web-fetta5. Ho esaminato il diff staged su modules/web/leggi.py e tests/test_unit_web_leggi.py. Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), reports/stato_progetto.md (in modo mirato) e .claude/agents/memoria_revisore.md.

**R-446-1 è chiusa.**

**Elementi del diff esaminati**
- `modules/web/leggi.py:448`: il nuovo `_Estrattore.handle_startendtag`.
  - Cosa fa: un tag nascosto che non è svg o math, se arriva autochiuso, chiama solo `handle_starttag`. Tutti gli altri tag passano da `super()`, cioè apertura più chiusura.
  - Rischio esaminato: che html.parser abbia altre strade per `<script/>`, che renderebbero l'override inutile. Ho letto `parse_starttag` su 3.13.16 e 3.11.17. Con `/>` chiama sempre `handle_startendtag` e non entra mai in `set_cdata_mode`, quindi questo override è l'unico punto da toccare.
  - Altro rischio: maiuscole e attributi. Le sonde `<SCRIPT SRC=x />`, `<script />`, `<script/ >` e `<script src='x'/>` nascondono tutte SEGRETO.
  - Esito: ok.
- `modules/web/leggi.py:452`: la condizione `tag in self._SALTA and tag not in _AUTOCHIUDIBILI`, con la costante a `modules/web/leggi.py:121`.
  - Rischio esaminato: svg, math, `<br/>` e `<title/>` devono restare come prima.
  - Sonde: `<svg />VIS<math/>VIS2` mostra tutto. `<title/>VIS` e `<br/>VIS` danno «\n\nVIS», come prima.
  - Le varianti autochiuse di style, template, object e canvas nascondono il testo.
  - Esito: ok.
- `modules/web/leggi.py:581`: nel ripiego, un grezzo autochiuso fa `salta += 1`.
  - Rischio esaminato: la parità «il ripiego non mostra niente che il parser nasconde». Adesso parser e ripiego contano `<script/>` allo stesso modo; prima nascondeva solo il ripiego.
  - Ho fatto un fuzz mio, indipendente da fuzz5.py, con le forme autochiuse di tutti i nascosti, `<SCRIPT/>` e «/>» con spazio negli atomi: 0 fughe su 100k pagine (3.13.16) e 0 su 100k (3.11.17).
  - Tempi su 400k `<script/>`: parser 0,9 s, ripiego 0,45 s.
  - Esito: ok.
- `tests/test_unit_web_leggi.py:852`: il test `test_parser_script_autochiuso_apre_lo_script` passa da `_componi`. L'ho verificato con mutazioni (patch del modulo, nessun file toccato):
  - override tolto: il test nuovo fallisce;
  - anche svg apre il blocco: falliscono 2 test (il nuovo e il confronto col parser a `tests/test_unit_web_leggi.py:953`).
  - Il test non è vacuo. Esito: ok.
- Suite: 166 passed su 3.13.16 (la mia run).

**Coerenza col progetto**
- La modifica va nel verso fail-safe: nasconde di più e non tocca guardrail, provider né history.
- Nessuno slicing diretto della history e nessuna simulazione di tool nel diff.

**Riserve**
- **R-447-1 (chat Mani), BASSA, da dichiarare** (ed è la tua domanda: sì, va dichiarata). Il limite ha due facce:
  - Dopo `<script/>` html.parser non entra in modalità testo grezzo, quindi il contatore unico scende alla prima chiusura di un qualsiasi nascosto. `<script/>A</noscript>B</script>C` mostra B al modello, mentre per i browser è codice invisibile. Prima della modifica uscivano sia A sia B, quindi è un miglioramento netto.
  - Nel verso opposto, un `<iframe src=x />` o un `<script/>` senza chiusura nasconde tutto il resto della pagina, e `<script/>A<script>B</script>C</script>D` nasconde C, che il browser mostra. È solo perdita di testo (verso sicuro), coerente coi browser per text/html, ma va scritta nella docstring o in stato_progetto.md come differenza nota.

**Rischi esclusi**
- Pagine servite come application/xhtml+xml, dove `<iframe/>` è davvero vuoto: non verificate, perché `leggi_pagina` non distingue il tipo XHTML. Lì si perde testo, ma non esce niente di nascosto.
- Comportamento su VPS e con le future patch di sicurezza di CPython su html.parser: non verificato, non riproducibile qui. Le versioni provate sono solo 3.13.16 e 3.11.17.

**Memoria**: riga #447 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con `scripts/commit_memoria_revisore.sh` (commit b147ca6). Nessuna lezione nuova. Il diff staged è rimasto intatto.

Script delle sonde e del fuzz: /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/sonde447.py

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 137 → 166 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «166 passed», Python 3.13 e 3.11 (venv); 166 passed anche con rete e DNS veri bloccati via sitecustomize).
- Fuzz differenziale ripiego contro parser: 0 fughe su 500k pagine (3.13) e 300k (3.11, escluse `<!-->`/`<!--->`).
- Mutazioni in copie isolate, tutte prese (22): contatore che non scende o scende sotto zero, svg grezzo, autochiuso ignorato o anche con «/» nel valore, noscript autochiudibile, CDATA al primo «>», fasulli come tag, chiusura senza virgolette, testo dentro i blocchi, regex finale rimessa, confine del nome tolto, grezzi autochiusi (che non contano o che saltano), plaintext con chiusura, textarea/xmp/noframes non grezzi, `handle_startendtag` tolto / anche svg / tutti.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

CI NON VERIFICATA con `gh run list` (gh non autenticato nella sessione cloud). Mappatura commit→run:
- `b49e2a7`, `980997f`, `b147ca6`, `f583746`: nessuna run su questi SHA da soli (pushati insieme al commit di fine-task che contiene questo file): run non ancora disponibile alla scrittura dell'handoff.
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: **R-447-1 (chat Mani)** BASSA dichiarata: dopo `<script/>` html.parser non entra in modalità grezza, quindi il contatore scende alla prima chiusura di un nascosto qualsiasi; un `<script/>` senza chiusura nasconde il resto della pagina (si perde testo).
- Restano: R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5 e R-ve235-7 (limiti dichiarati). Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…5».
