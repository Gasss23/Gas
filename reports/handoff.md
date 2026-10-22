# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-22 — Chat Mani, fetta 8: CDATA in HTML e XHTML senza testo grezzo (R6, PR #245), con il secondo giro dopo il bot #245

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #245 (https://github.com/Gasss23/Gas/pull/245): l'operatore l'ha chiesto («mergia 245 e procedi con la fetta 9»); il check obbligatorio verifica-bot sull'head precedente era «failure» (V-1 bot #245, MEDIA, corretta in questo giro): si mergia quando il bot riporta sul nuovo head.
2. Sul Mac e sulla VPS, dalla cartella di Gas: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` deve dire True; con False Gas legge il web col ripiego (niente titoli, verso sicuro).
3. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

(`gh` senza GraphQL nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **R-ve244-3 (CDATA in HTML)**: `FATTA` (fuori da svg/math; residuo R-463-1)
- **R-ve244-2 (XHTML senza testo grezzo)**: `FATTA`
- **V-1 bot #244 (limite dichiarato)**: `FATTA`
- **V-1 bot #245 (ogni `<![` su ogni html.parser)**: `FATTA` (chiude anche R-463-2)
- **R-464-1, R-464-2, R-464-3, R-465-1, R-465-2**: `FATTA`
- **R-463-1, R-466-1, R-466-2, R-ve245-1…5**: `DEFERITA — registrate in stato_progetto` (R-463-1 e R-ve245-1 nella fetta 9)

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  10 +
 modules/web/leggi.py               |  78 ++++++-
 reports/diff_sessione.md           |  11 +-
 reports/handoff.md                 | 436 +++++++------------------------------
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  34 ++-
 tests/test_unit_web_leggi.py       | 163 +++++++++++++-
 7 files changed, 350 insertions(+), 384 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
2ce6f94 fix(web): fetta 8 chat Mani, secondo giro — sezioni <![ e parser vecchi (V-1 bot #245)
a60f7f6 chore(revisore): memoria review #466 — APPROVATO CON RISERVE
7d63885 chore(revisore): memoria review #465 — APPROVATO CON RISERVE
6548b0c chore(revisore): memoria review #464 — APPROVATO CON RISERVE
649f441 docs(fine-task): verdetto #463 riemesso per il gate B — chat Mani fetta 8 (#245)
bef1ef8 docs(fine-task): report, stato e handoff — chat Mani fetta 8 (#245)
aa0b4f9 fix(web): fetta 8 chat Mani — CDATA in HTML come i browser, XHTML senza testo grezzo (R6)
96b83f5 chore(revisore): memoria review #463 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit (l'elenco dei file è esatto).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Quattro verdetti, incollati integralmente: #463 (chat Mani) sul commit `aa0b4f9`; #464, #465 e #466 (chat Mani) sul diff staged del secondo giro, cresciuto da una review all'altra e committato in `2ce6f94` dopo la #466 (memorie in `6548b0c`, `7d63885`, `a60f7f6`, fatte dal revisore).

### Review #463 (chat Mani) — verdetto RIEMESSO dal revisore

Il primo testo citava righe della libreria standard (html/parser.py) nella forma path:riga, che il gate B cerca nel repo: il revisore lo ha riemesso (stesso esito e sostanza). Sotto il testo riemesso integrale; com'era l'originale è descritto subito dopo.

## VERDETTO: APPROVATO CON RISERVE

Review #463 (chat Mani), 2026-10-22, riemessa lo stesso giorno. Fetta 8 Mani (R6), ramo feat/mani-web-fetta8, commit aa0b4f9, base 43a2545. Riemissione: l'esito e la sostanza non cambiano. Cambia solo il modo di citare lo stdlib: il gate B (`scripts/check_verdetto.py`) cercava nel repo le righe di html/parser.py scritte nella forma path:riga. Prima della riemissione ho controllato che le righe citate di modules/web/leggi.py e tests/test_unit_web_leggi.py siano le stesse a HEAD (bef1ef8): fra aa0b4f9 e HEAD quei due file non cambiano.

Prima della review ho letto CLAUDE.md (sez. 1, 5, 8, 10), reports/stato_progetto.md (blocco «Mani — fetta 7», dove R-ve244-2 e R-ve244-3 risultano aperte) e le lezioni sul parsing HTML in .claude/agents/memoria_revisore.md (righe 700-752: punti di integrazione, oracolo html5lib, atomi del fuzz).

Il diff non contiene slicing della history né output di tool simulati. Non tocca né i guardrail (cap 10 iterazioni, 8k, `_get_window`) né i provider. Va nel verso «zero crash»: nel parser i casi senza fine restituiscono -1, come fa html.parser.

### Elementi del diff esaminati

- modules/web/leggi.py:507 — override di `parse_html_declaration`. Fuori da svg/math, `<![CDATA[` diventa un commento fasullo fino al primo `>`.
  - Ho letto lo stdlib di Python 3.13.16: `parse_html_declaration` (riga 287 di html/parser.py) e il ramo di fine dati di `goahead` (riga 390 dello stesso file). `goahead` chiama `parse_html_declaration` per ogni `<!` che non è un commento. Con -1 e fine dati arriva al ramo `startswith("<![CDATA[") and self._support_cdata`, quindi `unknown_decl`, quindi testo nascosto. Lo stesso vale per la 3.11.17.
  - Il confronto è case-sensitive come nello stdlib. Il minuscolo `<![cdata[` va in `parse_bogus_comment`, come nei browser.
  - Sonde su 3.13 e 3.11: `<![CDATA[a><script>]]>SEGRETO</script>VIS` dava SEGRETO nascosto e VIS visibile (a HEAD SEGRETO usciva). Esito: ok.
- modules/web/leggi.py:511 — controllo `estraneo` con il contatore svg/math. Rischio esaminato: i punti di integrazione HTML. Esito: riserva R-463-1 (sotto).
- modules/web/leggi.py:499 — `set_cdata_mode` non fa niente in XHTML.
  - Lo stdlib lo chiama da `parse_starttag` per i grezzi, per RCDATA, per plaintext e per noscript con scripting attivo. Con l'override `cdata_elem` resta None e il parsing resta normale. `**kwargs` assorbe `escapable`.
  - Sonde XHTML: `<textarea><script>SEGRETO</script></textarea>VIS` → a HEAD SEGRETO usciva come `<script>SEGRETO`, ora è nascosto. `<script><![CDATA[ </script> ]]>SEGRETO</script>` → nascosto. Esito: ok.
- modules/web/leggi.py:493 — il commento nel ramo TypeError dichiara il limite (V-1 bot #244). Esito: ok.
- modules/web/leggi.py:633 — nel ripiego, `<![cdata[` va fino a `]]>` in svg/math o in XHTML e fino al primo `>` altrove. In HTML è coerente col parser (stessa posizione di `>`, perché `[cdata[` non contiene `>`). Esito: riserva R-463-2 (sotto).
- modules/web/leggi.py:659 — ripiego XHTML: i nascosti e il titolo si contano per nome, gli altri grezzi (textarea, xmp, plaintext) diventano tag normali.
  - Le chiusure `</script>` passano dal ramo `startswith("/")`, che scala il conteggio. Viene prima il ramo dell'autochiusura, e lì `vuoto = xhtml`, corretto.
  - `<plaintext>VIS</plaintext>VIS2` ora dà VIS VIS2 (a HEAD il ripiego si mangiava il resto). Esito: ok.
- tests/test_unit_web_leggi.py:976, tests/test_unit_web_leggi.py:992 e tests/test_unit_web_leggi.py:1002 — i tre test nuovi controllano sia il parser sia il ripiego.
  - Suite web: 199 passed su 3.13. Su 3.11 non c'è pytest nel sistema: ho rieseguito le sonde dei casi nuovi direttamente con python3.11 e i risultati sono identici.
  - Mutazioni rifatte in copia, partendo dall'index:

    | Mutazione | Test falliti |
    |---|---|
    | override valido anche dentro svg | 1 |
    | ripiego a `]]>` solo in XHTML | 1 |
    | conteggio XHTML tolto | 3 |

  - Esito: ok.
- tests/test_unit_web_leggi.py:1111 — il caso `a<![CDATA[ SEGRETO >VIS` sostituisce il precedente. Con l'oracolo html5lib il vecchio caso mostra SEGRETO come fanno i browser, quindi la sostituzione è corretta. Esito: ok.

### Riserve

**R-463-1 (MEDIA, preesistente, residuo di R-ve244-3).** Il CDATA vero dipende dal «nodo corrente aggiustato», non dal trovarsi dentro svg/math. In un punto di integrazione, se si apre un elemento HTML, per i browser `<![CDATA[` torna a essere un commento fasullo.
- Casi provati: `<p>PRIMA</p><svg><foreignObject><div><![CDATA[x><script>]]></svg>SEGRETO</script>VIS`, e lo stesso con `<math><mi><b>`.
- Qui il CDATA arriva fino a `]]>`, poi `</svg>` chiude e SEGRETO arriva al modello, sia nel parser sia nel ripiego, su 3.13 e 3.11. html5lib invece lo nasconde dentro lo script.
- A HEAD succedeva lo stesso, quindi non è una regressione.
- R-ve244-3 va registrata come «chiusa fuori da svg/math, residuo R-463-1», non come chiusa del tutto.
- Controprova: con `<svg><foreignObject>` senza elemento HTML aperto, html5lib mostra SEGRETO, e il diff fa bene.

**R-463-2 (BASSA, preesistente, solo nel ripiego).** modules/web/leggi.py:633 lavora sul testo in minuscolo (`basso`). Così `<![cdata[` minuscolo dentro svg arriva fino a `]]>`, mentre browser e parser lo chiudono al primo `>`.
- Caso: `<svg><![cdata[ x></svg><script> ]]></svg> SEGRETO </script> VIS` → il ripiego mostra SEGRETO; parser e html5lib no. A HEAD era uguale.
- Correzione possibile: verificare il CDATA sul testo originale, `testo.startswith("<![CDATA[", m.start())`.

### Note (non bloccanti)

- XHTML `<title>T<title></title>X</title>`: il parser mette X nel corpo (come a HEAD), il ripiego lo nasconde. È una differenza minima e riguarda il testo del titolo, che il modello riceve comunque.
- Il caso noscript che mi chiedi: sono d'accordo. Con il modello «scripting attivo» scelto nella fetta 6, noscript è testo grezzo e si chiude al primo `</noscript>`, quindi M5 e M6 sono visibili. A HEAD erano nascosti solo perché il CDATA senza `]]>` si mangiava il resto.

### Cosa non ho verificato

- Il comportamento su html.parser vecchi, senza le patch (niente `_support_cdata`, ramo di fine dati con `handle_data`). Qui ci sono solo 3.13.16 e 3.11.17, entrambe con le patch.
- Il comportamento dei browser veri. Ho usato html5lib 1.1 come oracolo, che lavora con lo scripting spento.
- I fuzz da 100k/200k e fuzz_cdata.py dichiarati non li ho rieseguiti: i file stanno nel tuo scratchpad. Ho fatto sonde mirate.
- Nella riemissione non ho rieseguito suite, sonde né mutazioni: ho solo riscontrato a HEAD le righe citate del repo.

### Lezioni nuove in memoria

- Il CDATA dipende dal nodo corrente aggiustato: sondare sempre i punti di integrazione con un elemento HTML aperto.
- L'oracolo html5lib (etree) deve saltare i nodi commento, altrimenti dà falsi positivi. Mi è successo nelle sonde: i commenti fasulli risultavano «visibili».

Riga #463 in .claude/agents/memoria_revisore.md, committata da sola con scripts/commit_memoria_revisore.sh (commit 96b83f5). Il diff staged del motore è rimasto intatto. Per la riemissione ho aggiunto in memoria una sola riga breve, non committata. Sonde e html5lib stanno nello scratchpad della sessione (file sonda.py).

#### Testo originale della review #463

Non incollato qui: il gate B controlla le citazioni path:riga anche dentro i blocchi di codice, e l'originale citava le righe 287 e 390 del file html/parser.py della libreria standard in quella forma (file fuori dal repo). Per il resto è identico al testo riemesso sopra (stesso esito, stessi elementi esaminati, stesse riserve R-463-1 e R-463-2, stesse note); il riemesso aggiunge solo la frase sulla riemissione e la voce «nella riemissione non ho rieseguito suite, sonde né mutazioni». La riga #463 della memoria del revisore (commit `96b83f5`) riporta lo stesso esito.

### Review #464 (chat Mani) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #464 (chat Mani) sul ramo feat/mani-web-fetta8 (PR #245), diff staged in modules/web/leggi.py e tests/test_unit_web_leggi.py. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (voci «Mani — fetta 7/8») e la mia memoria.

**Elementi del diff esaminati**
- modules/web/leggi.py:516 — in HTML ogni «<![» viene gestito dall'override senza chiamare super(); XHTML e gli altri «<!» passano ancora a super(). Rischio esaminato: in html.parser, moderno e vecchio, goahead chiama parse_html_declaration per ogni «<!» che non è un commento. Il ramo di fine dati (`k < 0`) non si raggiunge più, perché l'override non restituisce mai -1. Ricerca del «>» da i+3: equivale a quella del browser, perché in i+2 c'è sempre «[». — ok
- modules/web/leggi.py:519 — CDATA vero solo dentro svg/math e solo con «<![CDATA[» maiuscolo esatto, fino a «]]>»; tutto il resto è commento fasullo fino al primo «>» (modules/web/leggi.py:525). Rischio esaminato: maiuscole e minuscole, sezioni senza fine, `<![`/`<![>`/`<![ >` vuoti. Sonde con l'oracolo html5lib tutte coerenti. — ok
- modules/web/leggi.py:525 — senza fine restituisce `len(rawdata)`. Rischio esaminato: consumo di una pagina passata a pezzi. In modules/web/leggi.py:753 feed riceve la pagina intera in una sola chiamata, quindi va bene. — ok, con riserva R-464-2 sui test
- modules/web/leggi.py:644 — il ripiego considera CDATA vero solo `testo.startswith("<![CDATA[")` sul testo originale. Rischio esaminato: sfasamento degli indici tra `basso` e `testo`. La translate conserva la lunghezza, quindi gli indici coincidono. Chiude R-463-2 (`<svg><![cdata[x></svg>VIS`: HEAD perdeva VIS, ora c'è). — ok
- tests/test_unit_web_leggi.py:971 — `_dichiarazione_vecchia` copia il parse_html_declaration pre-patch. Rischio esaminato: simula solo il metodo, non goahead. — riserva (R-464-2)
- tests/test_unit_web_leggi.py:996 e tests/test_unit_web_leggi.py:1013 — 6+2 pagine × parser vecchio/nuovo, sia sul parser sia sul ripiego. — ok

**Verifiche rifatte da me**
- Suite web: 215 passed su 3.13.16 e su 3.11.17.
- **Parser vecchio reale**: ho scaricato html/parser.py di CPython v3.12.3, non patchato (gli stdlib locali 3.11/3.12/3.13 hanno tutti la patch), e l'ho messo in `sys.modules["html.parser"]` con un plugin pytest.
  - Codice staged: 214 passed, 1 failed (`test_ripiego_non_mostra_niente_che_il_parser_nasconde`). Lo stesso fallimento c'è a HEAD: il parser vecchio non riconosce «--!>», quindi nasconde di più (verso sicuro). Non dipende dal diff.
  - Codice di HEAD col parser vecchio: SEG arriva al modello su `<![cdata[`/`<![if`; AssertionError su `<![foo bar>`, `<![>`, `<![ >`. La fix chiude anche questi.
- Fuzz differenziale 2×15k, nuovo contro HEAD, con oracolo html5lib (copia di HEAD presa con git archive):
  - parser moderno: 0 casi in cui il nuovo mostra più di HEAD;
  - parser vecchio reale: 9 casi, tutti dovuti a un commento o tag senza fine a fine pagina (HEAD andava in eccezione o si fermava prima) → R-464-1.
- Mutazioni su una copia dell'index:
  - super() di nuovo per i «<![» non CDATA → 1 FAIL col parser moderno, 8 col vecchio reale;
  - ripiego che accetta il minuscolo → 1 FAIL moderno, 2 vecchio;
  - CDATA minuscolo nel parser → 1 FAIL moderno, 2 vecchio;
  - `return -1` al posto di `len(rawdata)` → **0 FAIL** col parser moderno e con la simulazione; 2 FAIL solo col parser vecchio reale.

**Riserve (da tracciare in stato_progetto.md)**
- **R-464-1 (chat Mani), MEDIA, preesistente** (solo html.parser senza le patch 2025): ogni costrutto senza fine a fine pagina diventa testo a close(). Riguarda `<!--`, `<!x`, `</x`, `<a b="`, `<!DOCTYPE`, `<?`. Esempio: `<p>A</p><!--<script>SEG` → SEG al modello, uguale a HEAD; il ripiego lo nasconde. È la stessa classe di V-1 bot #245, ma la fix copre solo «<![». Possibile chiusura: scartare il `rawdata` rimasto prima di close() sui parser vecchi, oppure un override di fine dati.
- **R-464-2 (chat Mani), BASSA**: nessun test della suite protegge il ramo `return len(rawdata)` di modules/web/leggi.py:525 sul parser della CI. Il ramo di fine dati sta in goahead, non nel metodo simulato. Suggerimento: un test diretto, per esempio `e.rawdata = "<p>A</p><![x"; assert e.parse_html_declaration(8) == len(e.rawdata)`, anche per il ramo CDATA in svg.
- **R-464-3 (chat Mani), BASSA, preesistente**: XHTML con parser vecchio, `<![foo bar>` → AssertionError. La intercetta leggi_pagina (l'except generico, §9: log e risposta di errore), quindi la lettura fallisce ma non c'è crash né fuga. In HTML la fix la elimina.
- Restano aperte: R-463-1 (punti di integrazione), R-454-2, R-453-2, R-456-1/2, R-450-1, R-447-1(b), V-2 ve #242.

**Rischi esclusi**
- Non ho verificato quale patch di Python gira sul Mac o sulla VPS: non è visibile dal repo. R-464-1 conta solo se quel Python è anteriore alle patch del 2025.
- Il parser vecchio reale l'ho provato solo con la v3.12.3, non con le 3.9-3.11 non patchate (il codice di goahead è equivalente, ma non l'ho rieseguito).
- L'oracolo html5lib tratta male `template` (contenuto in un frammento): i casi con template li ho esclusi dal conteggio; sono identici fra HEAD e nuovo.
- Non ho rieseguito la suite kernel: il diff non tocca gas.py.

Memoria aggiornata (riga #464 più una lezione sul parser vecchio reale contro la simulazione) e committata con scripts/commit_memoria_revisore.sh (6548b0c), solo /home/user/Gas/.claude/agents/memoria_revisore.md.

Materiale delle prove in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/p464:
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/p464/sonde464t.py (sonde con oracolo)
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/p464/fz464c.py (fuzz)
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/plug464/oldparser464.py (plugin del parser vecchio)
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/old464/html/parser.py (CPython v3.12.3)

NB dell'agente principale: le righe citate da questo verdetto si riferiscono al diff staged di allora; il commit finale (2ce6f94) contiene anche le modifiche delle #465 e #466, quindi in modules/web/leggi.py alcune righe sono scese (l'override sta ora a modules/web/leggi.py:520).

### Review #465 (chat Mani) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #465 (chat Mani): ri-review del diff staged completo di modules/web/leggi.py e tests/test_unit_web_leggi.py. Il diff include la parte già vista nella #464 (verdetto consegnato prima) più la chiusura di R-464-1 e R-464-2. Le letture obbligatorie le avevo già fatte per la #464, nella stessa sessione: CLAUDE.md, reports/stato_progetto.md, memoria.

**Elementi del diff esaminati**
- modules/web/leggi.py:532 — override di `close()`. Fuori dal testo grezzo, se il `rawdata` rimasto apre un costrutto, lo scarta prima di `super().close()`.
  - Rischio esaminato: buttare testo visibile o rompere la fine dati del parser moderno.
  - Il residuo dopo feed comincia sempre al «<» dove goahead si è fermato. Il residuo di solo testo (es. `a &amp`) non corrisponde e resta a super().
  - Parser moderno: 0 differenze in 15k casi di fuzz contro HEAD.
  - Il match è ancorato, quindi costo O(1).
  - — ok
- modules/web/leggi.py:114 — `_COSTRUTTO_APERTO` = «<» seguito da lettera ASCII, «!» o «?», oppure «</» seguito da un carattere qualsiasi. Rischio esaminato: coerenza col tokenizzatore dei browser. `<!`, `<?`, `<a`, `</x`, `</ ` a fine file non danno testo; `<1`, `<` e `</` da soli sì. Coincide col comportamento dei browser. — ok
- modules/web/leggi.py:536 — guardia `not self.cdata_elem`. Rischio esaminato: residuo dentro title/textarea. Togliendola non cambia nessuna sonda (`<title>T</ti` resta «T</ti» come per i browser): è difensiva e non testata. — ok
- modules/web/leggi.py:525 — ramo `len(rawdata)` (parte della #464): ora lo protegge tests/test_unit_web_leggi.py:1023. Mutazioni a `-1` → 1 FAIL sul parser moderno, sia nel ramo HTML sia in quello svg. R-464-2 chiusa. — ok
- tests/test_unit_web_leggi.py:1044 — 7 pagine × `close` vecchio simulato, che emette il rawdata come dato. tests/test_unit_web_leggi.py:1059 controlla che «<» e «</» restino testo. — ok, con la riserva R-465-2

**Verifiche rifatte da me**
- Suite web: 231 passed su 3.13.16 e su 3.11.17.
- Col parser vecchio reale (CPython v3.12.3 via plugin): 230 passed, 1 failed. È `test_ripiego_non_mostra_niente_che_il_parser_nasconde`, il preesistente «--!>» già visto nella #464.
- I test nuovi contro HEAD danno 14 FAILED: sono i 6 della #464 più gli 8 nuovi, coerente con quanto dichiarato.
- Fuzz con oracolo html5lib, 2×15k (fz465, che misura anche le perdite):
  - parser moderno: 0 casi in cui il nuovo mostra più di HEAD, 0 perdite nuove;
  - parser vecchio reale: 6 casi in cui il nuovo mostra più di HEAD. Li ho controllati: sono tutti contenuti di un `<title>` aperto, che finiscono nel campo «Titolo» come sul parser moderno, dove il titolo contiene anche di più. Nessuna fuga nel corpo.
  - parser vecchio reale: 70 perdite nuove, nel verso sicuro. 8 vengono da `<!-->`/`<!--->`, che il parser vecchio non riconosce (classe V-2 ve #242); prima il resto della pagina usciva come testo, ora viene scartato. 59 vengono dal titolo non grezzo del parser vecchio. Le ultime 3 sono noscript/template, uguali al parser moderno.
- Fuzz di parità: stesso codice nuovo, parser vecchio contro moderno, 20k casi con stesso seme. Il vecchio mostra di più in 14 casi, tutti preesistenti e non di fine pagina (vedi R-465-1).
- Mutazioni su una copia dell'index:
  - close tolto → 7 FAIL moderno, 15 vecchio;
  - regex su ogni «<» → 1 FAIL moderno, 2 vecchio;
  - guardia cdata tolta → 0 moderno, 1 vecchio (è solo il preesistente);
  - `/.` → `/[a-zA-Z]` → 0 FAIL moderno, 1 vecchio.

**Riserve (da tracciare in stato_progetto.md)**
- **R-465-1 (chat Mani), MEDIA, preesistente** (solo html.parser senza le patch del 2025): R-464-1 è chiusa per i costrutti aperti a fine pagina, ma il tokenizzatore vecchio fa ancora uscire testo nascosto a metà pagina.
  - `<p>A</p></x a='>SEG` → SEG al modello (identico a HEAD; parser moderno e ripiego lo nascondono).
  - `<p>A</p><template><title></template></template>SEG` → SEG nel campo Titolo: il titolo non è testo grezzo nel parser vecchio.
  - La classe resta aperta finché si correggono i parser vecchi un caso alla volta. Proposta strutturale: rilevare a runtime un html.parser non patchato (per esempio senza `_set_support_cdata`) e usare il ripiego, che in tutte queste sonde è corretto. Oppure dichiarare la versione minima di Python.
- **R-465-2 (chat Mani), BASSA**: due rami di modules/web/leggi.py:114 non sono protetti sul parser di CI: «</» seguito da un carattere che non è una lettera (`</ SEG`, `</1SEG` a fine pagina) e la guardia `cdata_elem`. Basta aggiungere `"<p>PRIMA</p></ SEGRETO"` e `"<p>PRIMA</p></1SEGRETO"` a tests/test_unit_web_leggi.py:1044.
- Nota COSMETICA, nessuna fuga: col parser vecchio `<textarea>X</te` a fine pagina dà «X» invece di «X</te», perché textarea non è testo grezzo nel parser vecchio.
- Restano aperte: R-464-3 (XHTML, `<![foo>` su parser vecchio → AssertionError presa da §9), R-463-1, R-454-2, R-453-2, R-456-1/2, R-450-1, R-447-1(b), V-2 ve #242.

**Rischi esclusi**
- Non ho verificato la versione e la patch di Python sul Mac o sulla VPS: dal repo non si vedono. R-465-1 conta solo se lì gira un html.parser anteriore alle patch del 2025.
- Il parser vecchio reale l'ho provato solo con la v3.12.3.
- L'oracolo html5lib tratta template e noscript diversamente da Gas (Gas assume scripting attivo): quei casi li ho valutati a mano.
- Non ho rieseguito la suite kernel: il diff non tocca gas.py.

Memoria aggiornata (riga #465 più una lezione sul fuzz di parità tra parser vecchio e moderno) e committata solo /home/user/Gas/.claude/agents/memoria_revisore.md (7d63885). Il diff staged sotto review è intatto (modules/web/leggi.py, tests/test_unit_web_leggi.py). reports/ ha modifiche non staged dell'agente principale, che non ho toccato.

Materiale delle prove:
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/p464/fz465.py (fuzz con le perdite)
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/p464/par465.py (parità vecchio/moderno)
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/p464/dbg465.py (residuo dopo feed)
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/plug464/oldparser464.py (plugin del parser vecchio)

### Review #466 (chat Mani) — verdetto integrale (diff del commit `2ce6f94`)

## VERDETTO: APPROVATO CON RISERVE

Review #466 (chat Mani): diff staged completo (modules/web/leggi.py, tests/test_unit_web_leggi.py) = #464 + #465 + il nuovo rilevatore del parser. Letture obbligatorie fatte (CLAUDE.md, stato_progetto.md, memoria) nella stessa sessione.

**Elementi del diff esaminati**
- modules/web/leggi.py:118 — `_PARSER_AGGIORNATO`, calcolato all'import: vale True se HTMLParser ha `_set_support_cdata` e se `set_cdata_mode` ha il parametro `escapable`; con TypeError/ValueError vale False.
  - Rischio esaminato: falso positivo (parser vecchio preso per nuovo) e falso negativo. Ho controllato i sorgenti di html/parser.py sui tag CPython (raw.githubusercontent.com).
  - **False**: 3.9.23, 3.10.18, 3.11.13, 3.12.11, 3.13.5, che non hanno nessuna patch. False anche su 3.13.6 e 3.13.7, che hanno `escapable`, `--!?>` e il nuovo tokenizzatore dei tag ma non `_set_support_cdata`: lì il rilevatore è conservativo e usa il ripiego, verso sicuro.
  - **True**: 3.9.24, 3.10.19, 3.11.14, 3.12.12, 3.13.8, 3.13.9, 3.14.0, main. Tutte hanno anche `--!?>`, `locatetagend` e RCDATA per title, quindi i fix di tokenizzatore di R-465-1.
  - Locali: 3.11.17, 3.12.3 Ubuntu (con backport) e 3.13.16 → True. La CI usa "3.11", quindi 3.11.14 o successiva.
  - Nessuna eccezione possibile all'import su una funzione Python.
  - — ok
- modules/web/leggi.py:774 — con un parser vecchio si alza ValueError dentro il try e si passa al ripiego esistente.
  - Rischio esaminato: un'eccezione che sfugge, o il ripiego che fa uscire testo da solo.
  - Il ValueError è preso dall'except subito sotto.
  - Chiude anche R-464-3: in XHTML non c'è più AssertionError, perché il parser vecchio non viene più usato.
  - — ok
- modules/web/leggi.py:542 e modules/web/leggi.py:124 — `close()` e `_COSTRUTTO_APERTO`, invariati dalla #465. — ok
- tests/test_unit_web_leggi.py:1071 — con il flag a False e `feed` vietato, le sonde R-465-1 non fanno uscire SEGRETO. Mutazione «raise tolto» → 3 FAIL sul parser moderno. — ok
- tests/test_unit_web_leggi.py:1043 e tests/test_unit_web_leggi.py:1044 — casi `</ SEGRETO` e `</1SEGRETO`: R-465-2 chiusa. — ok
- tests/test_unit_web_leggi.py:1061 — controlla che il flag sia True nell'ambiente corrente. Utile come allarme se la CI o il Mac passano a un Python non patchato, ma non prova la logica del rilevatore. — riserva R-466-1

**Verifiche rifatte da me**
- Suite web: 239 passed su 3.13.16 e su 3.11.17.
- Parser vecchio reale (CPython v3.12.3 via plugin): 233 passed, 6 failed, tutti attesi e coerenti con quanto dichiarato:
  - tre test di titolo (titolo perso col ripiego);
  - `test_grezzi_autochiusi_come_i_browser` (textarea nascosta);
  - rilevatore False;
  - il preesistente «--!>».
- Sonde sul parser vecchio:
  - `</x a='>SEG` → «A»;
  - `<template><title></template></template>SEG` → «A»;
  - `<textarea>X</textarea>` → X nascosto: perdita nel verso sicuro, come dichiarato.
- Fuzz con oracolo html5lib, 2×15k (fz465):
  - parser vecchio, dove ora lavora solo il ripiego: 0 casi in cui il nuovo mostra più di HEAD. Solo 3 differenze dall'oracolo, tutte template/noscript (limiti noti dell'oracolo; Gas assume scripting attivo);
  - parser moderno: 0 casi in cui il nuovo mostra più di HEAD e 0 perdite nuove.
- Mutazioni su una copia dell'index:
  - raise tolto → 3 FAIL moderno, 5 vecchio;
  - rilevatore sempre True → 0 FAIL moderno, 1 vecchio;
  - `and` → `or` → 0 FAIL moderno, 6 vecchio.

**Valutazione delle tre domande**
1. **Il rilevatore è affidabile?** Sì, sulle versioni ufficiali CPython controllate. I due marcatori arrivano insieme alle patch del tokenizzatore (gh-135661 e seguenti), salvo 3.13.6 e 3.13.7, dove l'esito è conservativo. Limite: le distribuzioni con backport parziali (Ubuntu, Homebrew, pyenv con patch proprie) sono verificate solo nel caso 3.12.3 Ubuntu.
2. **Il ripiego sempre attivo sui parser vecchi è accettabile?** Sì. Perde il titolo e nasconde le textarea, ma è nel verso sicuro e coerente con «robustezza > potenza». Il ripiego era già il percorso di emergenza fuzzato in tutte le review precedenti.
3. **Il resto del diff** è come nelle #464 e #465: le riserve di allora sono chiuse (R-464-1, R-464-2, R-464-3, R-465-1, R-465-2).

**Riserve (da tracciare in stato_progetto.md)**
- **R-466-1 (chat Mani), BASSA**: la logica del rilevatore non è testata sul parser della CI. Il flag è un'espressione calcolata all'import: le mutazioni «sempre True» e `or` passano tutte e 239 sul parser moderno. Proposta: una funzione pura `_parser_aggiornato(cls)`, provata con classi finte nei casi «nessun marcatore», «solo escapable» (come 3.13.6/7) e «entrambi».
- **R-466-2 (chat Mani), BASSA**: la degradazione è silenziosa. Su un Python vecchio Gas perde sempre il titolo e il testo delle textarea, ma niente lo dice. Proposta: un `logger.warning` una sola volta in gas_debug.log (in linea con §8 Model Awareness e §9), oppure una riga in `python gas.py doctor`.
- Nota COSMETICA: con il ripiego obbligatorio sui parser vecchi, gli override pensati per loro (il ripiego TypeError di `_modo_grezzo`, il ramo «vecchio» di `close`) restano come difesa in profondità. Il commento che li presenta come «valido su ogni versione» potrebbe citare il nuovo instradamento.
- Restano aperte: R-463-1, R-454-2, R-453-2, R-456-1/2, R-450-1, R-447-1(b), V-2 ve #242.

**Rischi esclusi**
- La versione di Python sul Mac e sulla VPS non l'ho verificata: dal repo non si vede. Va controllata con `python3 -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` sulla macchina.
- I backport delle distribuzioni diverse da Ubuntu 3.12.3 non li ho verificati.
- Il parser vecchio reale l'ho provato solo con la v3.12.3. Per le altre versioni ho controllato solo i marcatori nei sorgenti.
- Non ho rieseguito la suite kernel: il diff non tocca gas.py.

Memoria aggiornata (riga #466 più una lezione sui rilevatori di versione) e committata solo /home/user/Gas/.claude/agents/memoria_revisore.md (a60f7f6). Il diff staged è intatto; reports/ ha modifiche non staged dell'agente principale, che non ho toccato.

Sorgenti CPython scaricati in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/vers466; fuzz in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/p464/fz465.py.

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 192 → 199 (primo giro) → 239 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «239 passed» su Python 3.13.16, 3.11.17 e 3.12.3, venv).
- Con il html/parser.py reale di CPython 3.12.3 non patchato (plugin che lo sostituisce): 233 passed, 6 failed attesi (titolo perso col ripiego ×3, textarea nascosta, rilevatore False, il preesistente `--!>`); nessuna fuga.
- Test nuovi del secondo giro contro il codice del primo giro: falliscono (6 per `<![`, 8 per i costrutti aperti a fine pagina).
- Fuzz con oracolo html5lib contro l'head precedente: 0 casi in cui il nuovo mostra di più sul parser moderno (2×30k miei, 2×15k del revisore); sul parser vecchio reale 0 dopo il rilevatore (#466).
- Mutazioni del revisore in copie dell'index: vedi i verdetti #464–#466.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

Mappatura commit→run:
- `649f441` (head precedente): unit-suite success, handoff-check success, verifica-bot **failure** (V-1 bot #245, MEDIA), verifica esterna APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/245#issuecomment-6344406907)).
- `2ce6f94`, `9782bd9`: nessun evento di GitHub al push (PR ferma su `649f441`, nessuna run): rilevato dalla verifica esterna #245 bis ([commento](https://github.com/Gasss23/Gas/pull/245#issuecomment-6346157705), APPROVATO CON RISERVE); il commit che aggiorna questa riga rifà il push.

## §7 RISERVE APERTE

- Di questa fetta: **R-463-1 (chat Mani)** MEDIA preesistente (CDATA nei punti di integrazione con un elemento HTML aperto, fetta 9); **R-466-1** BASSA (rilevatore non testato con classi finte); **R-466-2** BASSA (degradazione silenziosa su Python vecchio); **R-ve245-1** MEDIA preesistente (XHTML con prefissi di namespace, fetta 9); R-ve245-2…5 BASSE/COSMETICHE.
- Restano: R-454-2, R-453-2, R-456-1/2, R-450-1, V-2 ve #243, R-447-1(b), V-2 ve #242, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…8» e «fetta 8, secondo giro».
