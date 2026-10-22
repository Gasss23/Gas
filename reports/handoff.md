# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-22 — Chat Mani, fetta 9: nodo corrente dentro svg/math come i browser (R6)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #245 (chiesto dall'operatore): aspetta che GitHub sincronizzi la PR sul nuovo head e che il bot riporti. Finché non è mergiata, la PR di questa fetta contiene anche i commit della fetta 8.
2. Merge della PR di questa fetta: vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore.
3. Sul Mac e sulla VPS, dalla cartella di Gas: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` deve dire True.
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

---

## §1 SCOPE & ESITO FETTE

- **R-463-1 (CDATA nei punti di integrazione)**: `FATTA`
- **R-450-1, V-2 ve #243 (uscita da svg/math)**: `FATTA`
- **R-ve245-1 (XHTML con prefissi)**: `FATTA`
- **R-456-1 (`<svg><noembed/>`)**: `FATTA`
- **B-467-1, B-467-2, R-467-1, R-468-1, R-468-2 (dalle review)**: `FATTA`
- **R-467-2, R-469-1, tabelle**: `DEFERITA — BASSE, registrate in stato_progetto`

---

## §2 GIT DIFF --STAT (sessione)

Verso main: finché la #245 non è mergiata comprende anche la fetta 8.

```
 .claude/agents/memoria_revisore.md |  15 +
 modules/web/leggi.py               | 360 +++++++++++++++++++----
 reports/diff_sessione.md           |  11 +-
 reports/handoff.md                 | 564 ++++++++++++++++---------------------
 reports/stato_progetto.md          |   4 +
 reports/ultimo_report.md           |  47 ++--
 tests/test_unit_web_leggi.py       | 259 ++++++++++++++++-
 7 files changed, 849 insertions(+), 411 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
6ed47c3 fix(web): fetta 9 chat Mani — nodo corrente dentro svg/math come i browser (R6)
b50139b chore(revisore): memoria review #469 — APPROVATO CON RISERVE
07a7932 chore(revisore): memoria review #468 — APPROVATO CON RISERVE
06a6f45 chore(revisore): memoria review #467 — BOCCIATO
ca131fa Merge remote-tracking branch 'origin/feat/mani-web-fetta8' into feat/mani-web-fetta9
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit (l'elenco dei file è esatto). L'ultima riga è il merge del ramo della fetta 8 (solo report).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Tre verdetti, incollati integralmente: #467 (BOCCIATO), #468 e #469 (chat Mani) sul diff staged della fetta 9, cresciuto da una review all'altra e committato in `6ed47c3` dopo la #469 (memorie in `06a6f45`, `07a7932`, `b50139b`, fatte dal revisore). Le righe citate nelle #467 e #468 si riferiscono al diff di allora.

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

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 239 → 264 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «264 passed» su Python 3.13.16 e 3.11.17, venv).
- Fuzz con oracolo html5lib contro l'head della fetta 8 (fuzz9: 2×30k su 3.13, 20k su 3.11; r467/fz.py del revisore: 5×20k; fz_noenc): 0 fughe del ripiego; 0 casi in cui il nuovo mostra un testo che html5lib nasconde, salvo 2 casi con `</template>` dove html5lib sbaglia (lo standard chiude il template).
- fuzz5/5b/5x (ripiego contro parser): 0 fughe.
- Mutazioni del revisore in copie: vedi i verdetti #467–#469.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

Mappatura commit→run:
- `f2c4be1` (head della PR #246 all'apertura): verifica-bot **failure** per V-1 MEDIA = nessuna run di ci.yml (né unit-suite né handoff-check). Dalle 15:15 UTC GitHub non elabora i push di questa sessione: ref aggiornati, ma nessuna run `push` e head delle PR ferme (#245 su `649f441`, #246 su `f2c4be1`); `c4954c2` (riserva V-2 del bot) e questo commit non hanno fatto partire niente alla scrittura. Blocco spiegato nel [commento](https://github.com/Gasss23/Gas/pull/246#issuecomment-6346702736).

## §7 RISERVE APERTE

- Di questa fetta: **R-vb246-2** BASSA (`</p>`/`</br>` nel contenuto estraneo non fanno uscire: si nasconde di più); **R-467-2 (chat Mani)** BASSA (`<font>` con attributi in svg); **R-469-1 (chat Mani)** BASSA preesistente (`</template>` attraverso un punto di integrazione: si perde testo, verso sicuro); tabelle (`<object><table></object>X`) BASSA preesistente.
- Restano: R-466-1, R-466-2, R-ve245-2…5, R-ve245b-4, R-454-2, R-453-2, R-456-2, R-447-1(b), V-2 ve #242, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…9».
