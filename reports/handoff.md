# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-22 — Chat Mani, fetta 9: nodo corrente dentro svg/math come i browser (R6, PR #246), con il secondo giro dopo la verifica esterna #246

---

## §0 DECISIONI UMANE RICHIESTE

1. **R-ve246-5 (MEDIA, già presente su main)**: un elemento HTML speciale dentro `<canvas>`/`<object>` fa arrivare al modello testo nascosto ai browser. Chiuderla bene richiede un vero costruttore dell'albero HTML5 (es. lexbor via selectolax): dipendenza nuova, decide l'operatore.
2. Merge della PR #246 (https://github.com/Gasss23/Gas/pull/246): chiesto dall'operatore «quando il bot approva».
3. Sul Mac e sulla VPS, dalla cartella di Gas: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` deve dire True.
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

---

## §1 SCOPE & ESITO FETTE

- **R-463-1, R-450-1, V-2 ve #243, R-ve245-1, R-456-1 (primo giro)**: `FATTA`
- **B-467-1, B-467-2, R-467-1, R-468-1, R-468-2**: `FATTA`
- **V-1, V-2, V-3 ve #246 (ALTE), R-vb246-2**: `FATTA`
- **B-470-1, R-470-1, R-470-2, R-471-1, R-471-2**: `FATTA`
- **R-ve246-5 (MEDIA preesistente)**: `DEFERITA — decisione dell'operatore`
- **R-469-1 (BASSA preesistente)**: `DEFERITA — registrata`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   9 +
 modules/web/leggi.py               | 419 +++++++++++++++++++++++++++++++------
 reports/diff_sessione.md           |  12 +-
 reports/handoff.md                 | 385 +++++++++++++---------------------
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  44 ++--
 tests/test_unit_web_leggi.py       | 196 ++++++++++++++++-
 7 files changed, 723 insertions(+), 344 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
04ba26a Merge remote-tracking branch 'origin/main' into feat/mani-web-fetta9
073036d fix(web): fetta 9 chat Mani, secondo giro — pila incerta, </p> e </br>, font, costo lineare (ve #246)
324101e chore(revisore): memoria review #472 — APPROVATO
075036a chore(revisore): memoria review #471 — APPROVATO CON RISERVE
8a1bec0 chore(revisore): memoria review #470 — BOCCIATO
854224a docs(fine-task): handoff con stato CI e riserva V-2 bot #246 — chat Mani fetta 9
c4954c2 docs(stato): riserva V-2 bot #246 registrata — chat Mani fetta 9
f2c4be1 docs(fine-task): report, stato e handoff — chat Mani fetta 9
ca131fa Merge remote-tracking branch 'origin/feat/mani-web-fetta8' into feat/mani-web-fetta9
6ed47c3 fix(web): fetta 9 chat Mani — nodo corrente dentro svg/math come i browser (R6)
b50139b chore(revisore): memoria review #469 — APPROVATO CON RISERVE
07a7932 chore(revisore): memoria review #468 — APPROVATO CON RISERVE
06a6f45 chore(revisore): memoria review #467 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit (l'elenco dei file è esatto).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Sei verdetti, incollati integralmente. #467 (BOCCIATO), #468 e #469 (chat Mani) sul primo giro, committato in `6ed47c3` (memorie `06a6f45`, `07a7932`, `b50139b`). #470 (BOCCIATO), #471 e #472 (chat Mani) sul secondo giro, committato in `073036d` dopo la #472 (memorie `8a1bec0`, `075036a`, `324101e`). Le righe citate nelle review intermedie si riferiscono al diff di allora.

### Review #467 (chat Mani) — verdetto integrale

## VERDETTO: BOCCIATO

Review #467 (chat Mani), fetta 9: tracciare il «nodo corrente aggiustato» dentro svg e math. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (blocchi «Mani — fetta 8») e la memoria del revisore.

**In breve:** le riserve che la fetta doveva chiudere risultano chiuse nelle sonde. Però il diff apre due fughe NUOVE rispetto a HEAD 9782bd9: testo che i browser nascondono (e che html5lib nasconde) arriva al modello. Succede sia nel parser sia nel ripiego. In una fetta di sicurezza R6 questo blocca.

**Motivi bloccanti**

- **B-467-1 (ALTA, regressione).** `annotation-xml` con `encoding="text/html"` (o `application/xhtml+xml`) è un punto di integrazione HTML, ma il codice non lo tratta così.
  - Un tag di uscita lì dentro fa uscire da math (`_esci`) e scala il contatore di math.
  - Sonda: `<p>A</p><math><semantics><mi>x</mi><annotation-xml encoding="text/html"><div>INIEZIONE</div></annotation-xml></semantics></math>VIS`.
  - Risultato: html5lib «A VIS», HEAD «A VIS», nuovo «A INIEZIONE VIS» (parser e ripiego).
  - Nei browser gli elementi di `<semantics>` dopo il primo non si vedono, quindi è iniezione invisibile a portata di mano.
  - Il mio fuzz (alfabeto esteso, oracolo html5lib) ne trova 1–4 ogni 20k, tutti di questa classe.
  - Rimedio suggerito: trattare `annotation-xml` di math SEMPRE come punto di integrazione, in `_esci` e in `_estranee`. Il ripiego non legge gli attributi; senza encoding si nasconde di più, che è il verso sicuro.
- **B-467-2 (ALTA, regressione).** `chiudi` risale la pila attraverso un punto di integrazione (mi, desc, foreignObject…) per chiudere un elemento HTML.
  - Il browser in quel caso ignora la chiusura: appena incontra un nodo HTML applica le regole HTML dal nodo corrente, e lì quei punti fermano la ricerca (sono confini di scope o elementi «speciali»).
  - Gas invece toglie anche il math o svg interno. Un `</svg>`/`</math>` successivo chiude il contenitore esterno, mentre il browser resta dentro.
  - Sonde (html5lib «A», HEAD «A», nuovo «A SEGRETO», parser e ripiego):
    - `<p>A</p><svg><foreignObject><div><math><mi></div></svg>SEGRETO`
    - `<p>A</p><svg><foreignObject><div><svg><desc></div></svg>SEGRETO`
    - `<p>A</p><math><mi><div><svg><desc></div></math>SEGRETO`
  - Controprova corretta: con `<svg><g>` al posto del punto di integrazione il browser chiude davvero, e il nuovo codice coincide.
  - Rimedio suggerito: in `chiudi`, se per arrivare a un nodo HTML si attraversa un punto di integrazione (o `annotation-xml`), la chiusura è ignorata.

**Elementi del diff esaminati**

- modules/web/leggi.py:178 — `_estranee`: decide regole HTML o estranee dal nodo in cima alla pila — rischio: punti di integrazione mancanti — **blocco** (B-467-1, manca `annotation-xml` con encoding html).
- modules/web/leggi.py:196 — `_esci`: esce dal contenuto estraneo e restituisce solo svg/math — rischio: uscita oltre il confine del browser — **blocco** per lo stesso motivo. La scelta di lasciare contati gli altri nascosti va bene: la mutazione «restituisce tutti» dà 0 FAIL, ma il verso è nascondere di più.
- modules/web/leggi.py:241 — `chiudi`: chiude per nome togliendo quello che sta sopra — rischio: attraversare punti di integrazione — **blocco** (B-467-2).
- modules/web/leggi.py:248 — `chiudi`: ignora la chiusura se c'è un elemento HTML in mezzo — rischio: chiusure che il browser esegue — ok, verso «nascondere di più».
- modules/web/leggi.py:192 e modules/web/leggi.py:668 — `cdata_vero` e il suo uso in `parse_html_declaration` — rischio: CDATA vero o commento fasullo deciso male — **ok** nel codice: R-463-1 chiusa, le sonde con `</div>`/`</b>` prima di `</svg>`/`</math>` danno SEGRETO a HEAD e «A» col nuovo.
- tests/test_unit_web_leggi.py:1134 — caso R-463-1 — rischio: test che non distingue la correzione — **riserva R-467-1 (MEDIA)**. Mutazione in copia `cdata_vero` → «pila non vuota»: 0 FAIL, perché qui `</svg>` è già ignorato dal div aperto. Serve la variante `<p>PRIMA</p><svg><foreignObject><div><![CDATA[x><script>]]></div></svg>SEGRETO</script>VIS`: col mutante il ripiego dà SEGRETO.
- modules/web/leggi.py:590 — `_locale` in XHTML — rischio: un prefisso che faccia nascondere meno — **ok**, R-ve245-1 chiusa. Mutazione «locale tolto» → 2 FAIL (tests/test_unit_web_leggi.py:1186).
- modules/web/leggi.py:843 — il ripiego usa lo stesso `_Contesto` — rischio: il ripiego mostra più del parser — **ok**: 0 casi in 85k casi di fuzz. Ma le due fughe sopra stanno anche nel ripiego.
- tests/test_unit_web_leggi.py:1171 — chiusura fermata da un elemento HTML — **ok**. D'accordo anche sui test riscritti (R-445-1 dentro foreignObject, noscript dentro svg): sono la semantica dei browser.

**Riserve non bloccanti**

- **R-467-1 MEDIA:** il test di R-463-1 non distingue la correzione (vedi sopra).
- **R-467-2 BASSA:** `<font>` con color/face/size non fa uscire da svg. Sonda: `<svg><font color=x><title/>X<h1/>TIT</title>VIS`. TIT finisce nel corpo invece che in «Titolo:»; il titolo arriva comunque al modello, quindi non è una fuga di testo nascosto. Mettere sempre `font` fra i tag di uscita sarebbe sbagliato (`<svg><defs><font>` resta in svg): serve leggere gli attributi.

**Caso template:** d'accordo con la tua lettura. Per lo standard `</template>` chiude il template, quindi M3 è visibile; html5lib qui sbaglia.

**Cosa ho rieseguito**

- Suite web: 256 passed su 3.13.16 e su 3.11.17.
- Mutazioni in copia: «uscita tolta da regole_estranee» → 0 FAIL, ma è quasi equivalente (`apri` usa `_estranee` direttamente); «grezzi in svg» → 1 FAIL.
- Il mio fuzz è in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r467/fz.py, insieme a fz_noenc.py e alla sonda or.py. Aggiunge annotation-xml con encoding, font con attributi, semantics e mglyph.

**Rischi esclusi (non verificati)**

- Comportamento su un browser vero: ho usato solo html5lib come oracolo, più la lettura dello standard per B-467-2 e per il template.
- Il «non si vede» di `<semantics>` viene dal foglio di stile MathML Core, citato a memoria e non riprovato.
- Parser vecchio reale (CPython 3.12.3): non riprovato. Con `_PARSER_AGGIORNATO` falso si usa il ripiego, e le fughe ci sono anche lì.

**ATTENZIONE, stato dell'index:** mentre lavoravo qualcuno ha fatto `git stash` e `git stash pop` sul repo (reflog 16:47:21 e 16:47:33). Ora modules/web/leggi.py e tests/test_unit_web_leggi.py NON sono più staged, sono solo modificati nel worktree. Ho controllato con cmp che il worktree coincide byte per byte con il diff che ho revisionato. Non ho toccato quei file.

**Memoria:** riga #467 e una lezione nuova aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (06a6f45, `chore(revisore): memoria review #467 — BOCCIATO`).

### Review #468 (chat Mani) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #468 (chat Mani). Ho riverificato le correzioni di B-467-1, B-467-2 e R-467-1 sul diff staged (fetta 9). Per questa sessione avevo già letto CLAUDE.md, reports/stato_progetto.md e la memoria del revisore. Il worktree coincide con l'index (cmp) e lo staging è intatto anche dopo il commit della memoria.

**Esito in breve:** i due blocchi della #467 sono chiusi. Le sonde che bocciavano danno solo «A», come html5lib e come HEAD. Restano due riserve MEDIA: un buco nei test e un caso che c'era già a HEAD. Nessuna delle due blocca il commit.

**Elementi del diff esaminati**

- modules/web/leggi.py:180 — `_punto`: annotation-xml di math vale sempre come punto di integrazione. Rischio esaminato: ripiego che non legge `encoding`. Esito: **ok**. Il verso è sicuro: senza encoding si nasconde di più. Con la sonda B-467-1 (`<math><semantics>…<annotation-xml encoding="text/html"><div>INIEZIONE`) parser e ripiego danno «A VIS».
- modules/web/leggi.py:185 — `_estranee`: dentro annotation-xml di math si applicano le regole HTML. Rischio esaminato: testo grezzo o CDATA classificati male. Esito: **ok**.
  - Uno `<style>`/`<title/>` grezzo lì dentro nasconde più del browser: va bene.
  - Il CDATA resta vero con annotation-xml in cima, come nello standard (il nodo corrente aggiustato è MathML).
- modules/web/leggi.py:253 — `chiudi`, fase estranea: risale per nome fino al primo elemento HTML. Rischio esaminato: differenze dall'algoritmo dello standard. Esito: **ok**. Mutazione in copia «niente stop all'HTML» → 4 FAIL.
- modules/web/leggi.py:266 — `chiudi`, fase HTML: riparte dal nodo corrente e si ferma a un punto di integrazione o a un elemento HTML diverso. Rischio esaminato: chiudere attraverso un confine di scope (B-467-2). Esito: **ok**.
  - Le tre sonde B-467-2 danno solo «A».
  - Mutazione «fase 2 senza `_punto`» → 3 FAIL.
  - La controprova `<svg><g>` è corretta (tests/test_unit_web_leggi.py:1162).
- tests/test_unit_web_leggi.py:1137 — variante R-467-1 con `</div>` prima di `</svg>`. Rischio esaminato: test che non distingue la correzione. Esito: **ok**, R-467-1 chiusa: il mutante di `cdata_vero` «pila non vuota» → 1 FAIL.
- tests/test_unit_web_leggi.py:1139 — sonda annotation-xml con encoding. Rischio esaminato: copertura di `_punto`. Esito: **riserva** (vedi R-468-1).

**Riserve**

- **R-468-1, MEDIA (test).** La mutazione che toglie annotation-xml da `_punto` non fa fallire nessun test (0 FAIL).
  - Motivo: la clausola esplicita in `_estranee` copre solo il caso con annotation-xml in cima alla pila. La parte di `_punto` usata in profondità, da `_esci` e da `chiudi`, resta senza test.
  - Caso che la distingue: `<p>A</p><math><annotation-xml encoding="text/html"><svg><p>INIEZIONE</p></svg></annotation-xml></math>VIS`. Col mutante parser e ripiego danno INIEZIONE; col codice attuale danno «A VIS», come html5lib.
  - Da aggiungere a `test_nodo_corrente_come_il_browser`.
- **R-468-2, MEDIA preesistente (anche a HEAD).** Un antenato nascosto fuori dalla pila (canvas, object) si chiude attraverso un punto di integrazione.
  - Caso: `<p>A</p><canvas><svg><foreignObject></canvas></svg>SEGRETO` → Gas mostra SEGRETO, html5lib lo nasconde.
  - Nella fase estranea la ricerca arriva in fondo alla pila senza trovare il nome: si chiama `_fine("canvas")` e il contatore di canvas scende. Il browser invece ignora quella chiusura, perché foreignObject è un elemento speciale.
  - Rimedio suggerito: nel ramo `for/else` della fase 1, se nella pila c'è un punto di integrazione, restituire «ignorata». Il verso è sicuro: `</template>` verrebbe ignorato e si nasconderebbe di più.
  - Su questo punto html5lib non è coerente: con `<desc>` al posto di foreignObject mostra SEGRETO.
- **R-467-2, BASSA:** resta aperta (font con attributi, solo titolo nel corpo).

**Cosa ho rieseguito**

- Suite web: 262 passed su 3.13.16 e su 3.11.17.
- Il mio fuzz r467/fz.py, 2×20k su 3.13, più fz_noenc 20k su 3.11: 0 fughe del ripiego e 0 casi in cui il nuovo mostra più di HEAD un testo che html5lib nasconde.
- Il caso template di fuzz9 (`</template>` con math e `<table/>`): d'accordo, è un limite dell'oracolo. Per lo standard `</template>` chiude il template.

**Rischi esclusi**

- Browser vero: non provato. Ho usato html5lib come oracolo più la lettura dello standard.
- Parser vecchio reale (CPython 3.12.3): non riprovato. Lì si usa il ripiego, e le sonde B-467 valgono anche per il ripiego.
- fuzz9, fuzz5/5b/5x e la suite del kernel: dichiarati da te, non rieseguiti.

**Memoria:** riga #468 e una lezione nuova aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (07a7932). Lo staging di modules/web/leggi.py e tests/test_unit_web_leggi.py è intatto.

### Review #469 (chat Mani) — verdetto integrale (diff del commit `6ed47c3`)

## VERDETTO: APPROVATO CON RISERVE

Review #469 (chat Mani): ri-review della #468 sul diff staged della fetta 9. Le letture obbligatorie le avevo già fatte in questa sessione. Prima di iniziare ho controllato con cmp che worktree e index di modules/web/leggi.py e tests/test_unit_web_leggi.py coincidessero. Dopo il commit della memoria i due file risultano ancora staged.

**Esito in breve:** R-468-1 e R-468-2 sono chiuse. Ogni chiusura ha un test che, se la si toglie, fallisce. Le due riserve rimaste sono BASSE e nel verso di nascondere di più.

**Elementi del diff esaminati**

- modules/web/leggi.py:263 — `chiudi`, fase estranea: se il tag non è in pila e non si incontra un elemento HTML, restituisce «ignorata» quando nella pila c'è un punto di integrazione. Rischio esaminato: ignorare chiusure che il browser esegue. Esito: **ok**.
  - Quando la chiusura è ignorata non scende nessun contatore e la pila non cambia. Al massimo si nasconde di più, mai di meno.
  - Sonda `<p>A</p><canvas><svg><foreignObject></canvas></svg>SEGRETO`: «A», come html5lib; HEAD dava SEGRETO.
  - Sonda `<p>A</p><object><math><mi></object></math>SEGRETO`: «A»; HEAD dava SEGRETO.
  - Mutazione in copia che riporta il ramo a `False, []`: 1 FAIL.
- tests/test_unit_web_leggi.py:1146 — sonda annotation-xml con `<svg><p>` sopra. Rischio esaminato: `_punto` non coperto «in profondità». Esito: **ok**. Mutazione «annotation-xml tolto da `_punto`»: ora 1 FAIL (alla #468 erano 0).
- tests/test_unit_web_leggi.py:1148 — sonda canvas. Rischio esaminato: test che non distingue la correzione. Esito: **ok**. Fallisce col ramo della #468, come hai dichiarato.

**Riesecuzioni**

- Suite web: 264 passed su 3.13.16 e su 3.11.17.
- Fuzz r467/fz.py, 2×20k su 3.13: 0 fughe del ripiego, 0 regressioni rispetto a HEAD con html5lib che nasconde.
- fz_noenc, 20k su 3.11: 0.

**Riserve**

- **R-467-2, BASSA:** resta aperta (font con color/face/size).
- **R-469-1, BASSA:** `<p>A</p><template><svg><desc></template>VIS` perde VIS. Per lo standard `</template>` chiude il template senza controllo di scope, quindi VIS sarebbe visibile; html5lib dà «A VIS». Era così anche a HEAD e il verso è sicuro: si perde testo, non ne esce di nascosto.

**Rischi esclusi**

- Browser vero: non provato. Mi sono basato su html5lib e sulla lettura dello standard.
- Parser vecchio reale (CPython 3.12.3): non riprovato; su quelle versioni si usa il ripiego, che ha le stesse sonde.
- fuzz9 e fuzz5: dichiarati da te, non rieseguiti.

**Note**

- In worktree c'è reports/stato_progetto.md modificato e non staged: non è mio e non l'ho toccato.
- Memoria: aggiunta la riga #469 in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola (b50139b). Nessuna lezione nuova.

### Review #470 (chat Mani) — verdetto integrale

## VERDETTO: BOCCIATO

Review #470 (chat Mani): diff staged sopra HEAD 854224a, cioè la correzione della verifica esterna #246. Le letture obbligatorie le avevo già fatte in questa sessione. Worktree e index coincidono (controllato con cmp); dopo il commit della memoria lo staging è intatto.

**In breve:** le correzioni di V-1, V-2, V-3 e V-5 reggono. Il blocco riguarda il ramo, non le righe nuove: una fuga di contenuto di script, entrata con la fetta 9, che alla #467 avevo valutato male.

**Motivo bloccante B-470-1 (ALTA, fuga rispetto a main 9782bd9).** È la mia R-467-2: alla #467 l'avevo data BASSA, ed era una valutazione sbagliata.
- Nel contenuto estraneo `<font>` con color, face o size dovrebbe far uscire da svg/math. Non succede: Gas resta in svg mentre il browser è tornato in HTML.
- Così un `<script>` o `<style>` NON autochiuso diventa un elemento svg. Il `</svg>` che segue chiude svg e lo script, e i conteggi scendono: il contenuto dello script arriva al modello, sia dal parser sia dal ripiego.
- Pagine di prova:
  - `<p>A</p><svg><font size=2><script></svg>SEGRETO</script>VIS`
  - `<p>A</p><math><font face=x><style></math>SEGRETO</style>VIS`
- Gas mostra SEGRETO. main, html5lib e lexbor lo nascondono: l'albero lexbor è `<svg></svg><font size="2"><script></svg>M1</script>…`.
- Senza attributi (`<svg><font><script></svg>X`) X è visibile anche per html5lib, quindi la distinzione per attributo è proprio quella che manca.
- Rimedio suggerito:
  - nel parser, `<font>` con un attributo color/face/size (basta che ci sia, anche senza valore) conta come tag di uscita, anche nella forma `<font color=x/>`;
  - nel ripiego, che non legge gli attributi, un `<font` nel contenuto estraneo rende la pila incerta. È il verso sicuro: i font in svg sono rari.
  - Test: le due pagine sopra, più la variante senza attributi che deve restare visibile.

**Elementi del diff esaminati**

- modules/web/leggi.py:312 — `</p>` e `</br>` con la cima estranea fanno uscire (V-1). Rischio esaminato: uscita senza traccia del contenitore. Esito: **ok**. Se la pila si svuota il browser crea un `p` vuoto e lo chiude subito, quindi non resta aperto nessun elemento speciale. Mutazione in copia (uscita tolta): 1 FAIL.
- modules/web/leggi.py:325 — tag fuori dalla pila, senza HTML né punti di integrazione: se è in `_visti` o in `_IMPLICITI` la pila diventa incerta, altrimenti la chiusura è ignorata (V-2). Rischio esaminato: un antenato chiuso dal browser. Esito: **ok**.
  - Ogni ritorno di questo ramo è «ignorata», quindi al massimo si nasconde di più; «incerta» copre il caso in cui il browser è già tornato all'HTML.
  - L'unica chiusura che salta lo scope è `</template>`, e template resta contato, quindi niente fuga.
  - Mutazione: 5 FAIL.
- modules/web/leggi.py:216 — `_togli_da` / `_metti` (V-3). Rischio esaminato: indici disallineati dalla pila e costo. Esito: **ok**.
  - Ogni push corrisponde a un pop in ordine di pila, quindi `_posizioni`, `_html` e `_punti` restano coerenti con la pila e il costo è ammortizzato.
  - In `apri` la scansione di `aperti` è limitata a 11 nomi.
  - Oltre `PROFONDITA_MAX` la pila diventa incerta, nel verso sicuro.
- modules/web/leggi.py:248 — `cdata()`: con un elemento HTML in cima la pila diventa incerta e il CDATA è trattato come fasullo. Rischio esaminato: CDATA vero per il browser dopo chiusure implicite. Esito: **ok**. Mutazione: 1 FAIL.
- modules/web/leggi.py:283 — un'uscita che svuota la pila con canvas, object o altri contenitori nascosti aperti → incerta (V-5). Esito: **ok**. Mutazione: 3 FAIL.
- modules/web/leggi.py:803 e modules/web/leggi.py:970 — parser e ripiego tagliano il resto della pagina allo stesso modo. Rischio esaminato: un ripiego che mostra più del parser. Esito: **ok**. Mutazione in `handle_data`: 9 FAIL.
- tests/test_unit_web_leggi.py:1174 — iframe in math con CDATA vero. Esito: **ok**, è un caso che distingue la scelta «i grezzi restano elementi».

**Riserve**

- **R-470-1 BASSA:** la mutazione «elemento HTML diverso senza incerta» (modules/web/leggi.py:343) dà 0 FAIL. Non trovo una fuga senza quella protezione: la pila di Gas ha elementi HTML in più, quindi blocca le chiusure. È una protezione in più che nessun test prova; va dichiarata o coperta.
- **R-470-2 BASSA:** quando la pila diventa incerta il resto della pagina sparisce senza lasciare traccia in gas_debug.log (stessa famiglia di R-466-2). Proposta: un warning, una volta per pagina.

**Su cosa chiedevi di valutare**

- Gli inneschi di «incerta» coprono le divergenze della pila che conosco, tranne B-470-1. Quella non è una divergenza della pila: è un tag di uscita non riconosciuto, quindi Gas resta in contenuto estraneo dove il browser è in HTML.
- `_visti` sovrastima, e il verso è sicuro.

**Riesecuzioni**

- Suite web: 281 passed su 3.13.16 e su 3.11.17.
- Mio fuzz con oracolo html5lib, senza gli atomi `</p>`/`</br>` (html5lib non li implementa), con in più font con attributi: 3×20k, 0 fughe del ripiego e 0 regressioni. Il fuzz NON trova B-470-1 (serve la sequenza esatta font con attributo, script, `</svg>`); l'ho trovata con le pagine di prova e l'ho confermata con lexbor.
- Le regressioni del fuzz con `</p>`/`</br>` sono quelle che descrivi: limite di html5lib.

**Rischi esclusi**

- Browser vero: non provato. Oracoli usati: html5lib e lexbor.
- Parser vecchio reale (CPython 3.12.3), fuzz5/5b/5x e fzl con lexbor 4×20k: non rieseguiti, li hai dichiarati tu.
- Quanto testo si perde con «incerta» su pagine vere: non misurato, manca un corpus.

**Memoria:** aggiunte la riga #470 e una lezione che corregge la mia valutazione di R-467-2, in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (8a1bec0).

### Review #471 (chat Mani) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #471 (chat Mani): diff staged sopra 854224a, ri-review della #470. Le letture obbligatorie le avevo già fatte in questa sessione. Worktree e index coincidono (controllato con cmp); dopo il commit della memoria lo staging è intatto.

**Esito in breve:** B-470-1 è chiusa, così come R-470-1 e R-470-2. Resta un buco nei test (R-471-1, MEDIA): il codice è giusto, ma le due scelte nuove «a pila vuota svg e math restano contati» non hanno un test che fallisca se le si toglie. Più una nota BASSA sul log.

**Elementi del diff esaminati**

- modules/web/leggi.py:715 — `_font_esce`: un attributo color, face o size presente, anche senza valore, fa uscire `<font>`. Il valore arriva sia ad `apri` sia a `_esito_autochiuso`. Rischio: attributi scritti in modi diversi. Esito: **ok**.
  - html.parser mette i nomi in minuscolo, quindi `<font COLOR>` funziona.
  - Sonde: `size=2` + script in svg, `face` + style in math, `COLOR` senza valore e `<font color=x/>` danno solo «A».
  - `<font>` senza attributi: il parser mostra X come lexbor, il ripiego lo nasconde.
  - Mutazione in copia (`_font_esce` sempre False): FAIL.
- modules/web/leggi.py:284 — il ripiego non legge gli attributi, quindi un `<font>` nel contenuto estraneo rende la pila incerta. Rischio: il ripiego mostra più del parser. Esito: **ok**: il verso è sicuro. Mutazione (niente incerta): FAIL.
- modules/web/leggi.py:298 — un'uscita in `apri` che svuota la pila non scala svg/math, che restano contati fino alla loro chiusura. Rischio: conteggi chiusi per errore (radice V-5). Esito: **ok** nel codice, **riserva** sui test.
  - Mutazione che li fa scalare di nuovo: 0 FAIL.
  - Col mutante `<p>A</p><canvas><form></canvas><svg><b/>SEGRETO` dà SEGRETO al modello, parser e ripiego. lexbor lo mette dentro canvas, quindi è nascosto.
- modules/web/leggi.py:330 — stessa scelta per `</p>` e `</br>` in `chiudi`. Esito: **ok** nel codice, **riserva** sui test.
  - Mutazione: 0 FAIL.
  - Col mutante `<p>A</p><canvas><form></canvas><svg></p>SEGRETO` dà SEGRETO; idem con `</br>`.
- modules/web/leggi.py:1064 — warning nel log quando la pila del parser è incerta (R-470-2). Esito: **ok**, ma il ripiego non lascia traccia (vedi R-471-2).
- tests/test_unit_web_leggi.py:1213 — test diretto di «chiusura fermata da un elemento HTML → incerta». Esito: **ok**, chiude R-470-1.
- tests/test_unit_web_leggi.py:1186 e tests/test_unit_web_leggi.py:1203 — pagine di B-470-1 e font senza attributi. Esito: **ok**.

**Riserve**

- **R-471-1 MEDIA (test):** aggiungere a `test_pila_incerta_o_uscita_non_fanno_uscire_testo` queste tre pagine:
  - `<p>A</p><canvas><form></canvas><svg><b/>SEGRETO`
  - `<p>A</p><canvas><form></canvas><svg></p>SEGRETO`
  - `<p>A</p><canvas><form></canvas><svg></br>SEGRETO`
  Oggi passano, e falliscono coi due mutanti.
- **R-471-2 BASSA:** il warning in gas_debug.log c'è solo sul percorso del parser. Quando lavora il ripiego (Python senza le patch, o eccezione del parser) la pagina tagliata non lascia traccia.
- **Nota (verso sicuro, va bene):** `<p>A</p><svg><g><font size=1><title/></svg>TIT</title>VIS` ora perde VIS. Svg resta contato e il suo `</svg>` sta dentro il titolo; main mostrava VIS.

**Riesecuzioni**

- Suite web: 288 passed su 3.13.16 e su 3.11.17.
- Mio fuzz con oracolo html5lib (font con attributi, senza `</p>`/`</br>`): 20k su 3.13 e 20k su 3.11, 0 fughe del ripiego e 0 regressioni.
- Pagine di prova confermate con lexbor (selectolax).

**Rischi esclusi**

- Browser vero: non provato.
- fzl con lexbor 4×20k, fuzz5/5b, fuzz9 e parser vecchio reale: non rieseguiti, li hai dichiarati tu.
- Quanto testo si perde con «incerta» su pagine vere: non misurato, manca un corpus.

**Memoria:** aggiunta la riga #471 in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola (075036a). Nessuna lezione nuova.

### Review #472 (chat Mani) — verdetto integrale (diff del commit `073036d`)

## VERDETTO: APPROVATO

Review #472 (chat Mani): ri-review della #471, solo sul delta. R-471-1 e R-471-2 sono chiuse e non resta nessuna riserva aperta su questo delta.

Ho controllato che worktree e index coincidano (cmp). Dopo il commit della memoria lo staging è intatto. Il delta rispetto all'index della #471 contiene solo le due modifiche che hai descritto.

**Elementi del diff esaminati**

- modules/web/leggi.py:991 — il ripiego, se la pila è incerta, scrive un warning e si ferma; solo dopo controlla `fine == -1`. Rischio: un cambio di comportamento dovuto al nuovo ordine dei controlli, o un doppio log. Esito: **ok**.
  - Le due condizioni portano tutte e due a `break`, quindi l'ordine non cambia ciò che arriva al modello.
  - Doppio log impossibile: `_testo_senza_parser` è chiamato solo nel ramo `except ValueError` di `_componi`, cioè quando il parser non ha finito; il warning del parser si scrive solo quando il parser va a buon fine.
  - Mutazione in copia che toglie il warning: 1 FAIL (tests/test_unit_web_leggi.py:1237).
- tests/test_unit_web_leggi.py:1191 — le tre pagine canvas/form (`<b/>`, `</p>`, `</br>`) che chiudono R-471-1. Rischio: test che non distinguono la correzione. Esito: **ok**.
  - Mutazione «uscita a pila vuota che scala svg» in `apri`: 1 FAIL (alla #471 era 0).
  - Mutazione «`</p>`/`</br>` a pila vuota» in `chiudi`: 2 FAIL (alla #471 era 0).

**Riesecuzioni:** suite web 291 passed su 3.13.16 e su 3.11.17.

**Rischi esclusi**
- Il resto del diff l'ho rivisto alla #470 e alla #471 e qui non l'ho riesaminato, come mi hai chiesto.
- Non ho rifatto fuzz (il delta tocca solo il log e i test) né provato il parser vecchio reale o un browser vero.
- Il messaggio del ripiego non contiene l'URL, perché la funzione non lo riceve: per questo uso va bene.

**Memoria:** aggiunta la riga #472 in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola (324101e). Nessuna lezione nuova.

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 239 → 264 (primo giro) → 291 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «291 passed» su Python 3.13.16 e 3.11.17, venv).
- Fuzz con oracolo lexbor (selectolax 1.0.2) contro fetta 8 e main, 8×20k: 0 regressioni; fughe rimaste = R-ve246-5, uguali o meno della fetta 8.
- Fuzz con oracolo html5lib (fuzz9, r467/fz.py): 0 regressioni salvo uscite con `</p>`/`</br>`, dove html5lib non segue lo standard (lexbor conferma il nostro esito).
- fuzz5/5b/5x (ripiego contro parser): 0 fughe. Parser vecchio reale (CPython 3.12.3): 6 fallimenti attesi (titolo perso, rilevatore), nessuna fuga.
- Test nuovi del secondo giro contro il codice del primo giro: 15 FAILED su 16 (il perf da solo oltre 2 minuti).
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

Mappatura commit→run:
- `f2c4be1`, `c4954c2`: nessuna run (GitHub non elaborava i push, 15:15–17:23 UTC).
- `854224a`: unit-suite success, handoff-check success, verifica-bot failure (BOCCIATO: V-1, V-2, V-3 = quelli della verifica esterna, chiusi in `073036d`).
- `073036d`, merge di main e il commit di fine-task con questo handoff: run non ancora disponibili alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: **R-ve246-5** MEDIA preesistente (canvas/object con elementi speciali; serve un costruttore HTML5, decisione dell'operatore); **R-469-1** BASSA preesistente (`</template>` attraverso un punto di integrazione, verso sicuro); quanto testo si perde con «incerta» su pagine vere: non misurato.
- Restano: R-466-1, R-466-2, R-ve245-2…5, R-ve245b-4, R-454-2, R-453-2, R-456-2, R-447-1(b), V-2 ve #242, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…9».
