# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-22 — Chat Mani, fetta 10: annotation-xml e autochiusi nel contenuto estraneo (R6, correzione dopo la verifica esterna #246)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore. Chiude una fuga ALTA oggi su main (V-1 ve #246 bis).
2. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; serve un costruttore HTML5 vero (es. lexbor): decide l'operatore.
3. Sul Mac e sulla VPS, dalla cartella di Gas: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` deve dire True.
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

---

## §1 SCOPE & ESITO FETTE

- **V-1 ve #246 bis (ALTA) e B-473-1 (ALTA)**: `FATTA`
- **V-2 ve #246 bis (MEDIA preesistente)**: `FATTA`
- **V-4 ve #246 bis (MEDIA, test)**: `FATTA`
- **R-ve246b-5 (BASSA)**: `DEFERITA — registrata`
- **V-1 ve #248 (BASSA, test del ripiego)**: `FATTA`
- **R-ve248-3 (BASSA preesistente)**: `DEFERITA — registrata`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +
 modules/web/leggi.py               |  63 ++++--
 reports/diff_sessione.md           |  10 +-
 reports/handoff.md                 | 384 ++++++++-----------------------------
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  28 ++-
 tests/test_unit_web_leggi.py       |  47 +++++
 7 files changed, 200 insertions(+), 338 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
6e87492 test(web): ripiego con annotation-xml rende la pila incerta — chat Mani fetta 10 (V-1 ve #248)
73a3211 chore(revisore): memoria review #475 — APPROVATO
5a0786f docs(fine-task): handoff con il diff completo — chat Mani fetta 10
7602d3a docs(fine-task): report, stato e handoff — chat Mani fetta 10
1016ef2 fix(web): fetta 10 chat Mani — annotation-xml solo con encoding HTML, autochiusi vuoti nel contenuto estraneo (ve #246 bis)
8d08649 chore(revisore): memoria review #474 — APPROVATO
92dd988 chore(revisore): memoria review #473 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit (l'elenco dei file è esatto).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Tre verdetti, incollati integralmente: #473 (BOCCIATO) e #474 (APPROVATO) (chat Mani) sul diff della fetta 10 committato in `1016ef2`; #475 (APPROVATO) sul test aggiunto dopo la verifica esterna #248, committato in `6e87492` (memorie `92dd988`, `8d08649`, `73a3211`, fatte dal revisore). Le righe citate nella #473 si riferiscono al diff di allora.

### Review #473 (chat Mani) — verdetto integrale

## VERDETTO: BOCCIATO

Review #473 (chat Mani), fetta 10, ramo feat/mani-web-fetta10 creato da main 17c0cfc. Ho rivisto il diff staged; worktree e index coincidono (controllato con cmp). Dopo il commit della memoria lo staging è intatto. Le letture obbligatorie le avevo già fatte in questa sessione.

**In breve:** la correzione di V-1 si aggira con uno spazio nel valore di `encoding`, o con un secondo attributo `encoding`. In quei casi il testo nascosto arriva al modello. Il resto della fetta è a posto.

**Motivo bloccante B-473-1 (ALTA: la correzione di V-1 ve #246 si aggira)**

Dove: modules/web/leggi.py:738, `_html_dentro`. La funzione sbaglia in due punti:
- **`.strip()`.** Lo standard confronta il valore esatto e ignora solo maiuscole e minuscole ASCII. Con `encoding=" text/html "` il browser NON ha un punto di integrazione, Gas sì.
- **`any(...)` su tutti gli attributi.** html.parser restituisce anche i duplicati, mentre i browser tengono solo il primo. Con `encoding="x" encoding="text/html"` il browser NON ha un punto di integrazione, Gas sì.

Pagine di prova, controllate con lexbor (selectolax):
- `<p>A</p><math><annotation-xml encoding=" text/html "></p><svg></math>SEGRETO`
- `<p>A</p><math><annotation-xml encoding="x" encoding="text/html"></p><svg></math>SEGRETO`

In entrambe lexbor esce da math con `</p>` e mette SEGRETO dentro `<svg>`, quindi nascosto. Il parser di Gas restituisce invece «A SEGRETO». Il ripiego è salvo, perché lì la pila diventa incerta.

Con questi due valori Gas si comporta come main, quindi non è una regressione rispetto a main. Ma lascia aperta la fuga ALTA che la fetta deve chiudere. L'enumerazione esaustiva non poteva vederla: gli atomi non hanno attributi.

Rimedio:
- usare solo il PRIMO attributo `encoding`;
- niente strip;
- minuscole solo ASCII (`translate(_MINUSCOLE_ASCII)` al posto di `lower()`: oggi è innocuo, ma è il confronto dello standard);
- test con le due pagine sopra più `encoding="TEXT/HTML"`, che deve restare un punto, come per lexbor.

**Elementi del diff esaminati**

- modules/web/leggi.py:205 — `_cima_punto`: la cima della pila è un punto di integrazione se il suo indice è in `_punti`. Rischio: indici disallineati dopo i pop. Esito: **ok**, `_togli_da` sfoltisce `_punti` insieme alla pila.
- modules/web/leggi.py:246 — `_estranee` per annotation-xml: se è un punto valgono le regole HTML; se non lo è valgono quelle estranee, tranne per `<svg>`. Rischio: divergenze dalla scelta dello standard fra regole HTML ed estranee. Esito: **ok**.
  - Sono le due righe dello standard.
  - L'eccezione mglyph/malignmark resta solo per mi, mo, mn, ms, mtext, come vuole lo standard.
- modules/web/leggi.py:312 — nel ripiego un annotation-xml in math aperto rende la pila incerta. Rischio: il ripiego mostra più del parser. Esito: **ok**, è il verso sicuro.
  - La forma autochiusa non entra in pila e non rende incerto niente, ed è corretto così.
  - Sulle pagine reali il costo è basso: KaTeX e MathJax usano `<annotation>`, non annotation-xml.
- modules/web/leggi.py:383 — nel contenuto estraneo `<x/>` è sempre vuoto, anche per i nascosti (V-2). Rischio: aver tolto una protezione che compensava una pila sbagliata. Esito: **ok**: oggi le divergenze della pila passano da «incerta». Le 3 sonde V-2 sono nei test (tests/test_unit_web_leggi.py:1196 e righe seguenti).
- modules/web/leggi.py:738 — `_html_dentro`. Esito: **blocco** (B-473-1).
- tests/test_unit_web_leggi.py:1261 e tests/test_unit_web_leggi.py:1272 — controprova con encoding text/html e test di tempo (V-4). Esito: **ok**. Il test di tempo non l'ho cronometrato contro una mutazione lineare: prendo per buona la tua misura e quella del verificatore (16 s).

**Riesecuzioni**
- Suite web: 301 passed su 3.13.16 e su 3.11.17.
- Le pagine di B-473-1 le ho provate con lexbor e html5lib. html5lib non implementa l'uscita con `</p>`: per questi casi l'oracolo giusto è lexbor.
- Enumerazione a 4 atomi (0 regressioni, 0 fughe su 1,87 milioni di pagine): dichiarata da te, non rieseguita, e non copre gli attributi.

**Rischi esclusi**
- Browser vero: non provato. Oracoli usati: lexbor e html5lib.
- Enumerazione a 5 atomi: in corso, non valutata.
- Parser vecchio reale (CPython 3.12.3): non riprovato. Lì lavora il ripiego, che rende la pila incerta su annotation-xml.

**V-5 (BASSA):** d'accordo a registrarla così.

**Memoria:** aggiunte la riga #473 e una lezione nuova (come si sondano i valori degli attributi: spazi, maiuscole, entità, duplicati) in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (92dd988).

### Review #474 (chat Mani) — verdetto integrale (diff del commit `1016ef2`)

## VERDETTO: APPROVATO

Review #474 (chat Mani): ri-review della #473 sulla fetta 10. B-473-1 è chiusa e non ho trovato altro da segnalare. Worktree e index coincidono (cmp), e lo staging è rimasto intatto dopo il commit della memoria.

**Elementi del diff esaminati**

- **modules/web/leggi.py:740 — `_html_dentro`.** Ora legge solo il primo attributo `encoding`, confronta il valore esatto senza strip e porta in minuscolo solo l'ASCII.
  - Rischio esaminato: Gas e browser che non concordano sul valore dell'attributo.
  - Esito: **ok**. Ho provato sette pagine contro lexbor e coincidono tutte:
    - `encoding=" text/html "` non è un punto di integrazione: SEGRETO nascosto.
    - `encoding="x" encoding="text/html"` non è un punto: SEGRETO nascosto.
    - `encoding="text/html" encoding="x"` è un punto: X dentro math, nascosto, e VIS visibile.
    - `encoding="text&#47;html"` è un punto: html.parser decodifica l'entità come fanno i browser.
    - `ENCODING=TEXT/HTML` senza virgolette è un punto.
    - `encoding` senza valore non è un punto. Lexbor esce da math e mostra X; Gas nasconde X, quindi nasconde di più (verso sicuro).
    - `encoding="text/html"` con la K del simbolo Kelvin in coda non è un punto: SEGRETO nascosto.
- **tests/test_unit_web_leggi.py:1202** — le pagine di B-473-1 dentro `test_pila_incerta_o_uscita_non_fanno_uscire_testo`.
  - Rischio esaminato: test che non pinnano la correzione.
  - Esito: **ok**. Con mutazioni in copia: rimettere lo strip dà 1 FAIL; tornare ad `any` su tutti gli attributi dà 1 FAIL.
- **tests/test_unit_web_leggi.py:1268** — la controprova sui tre encoding con maiuscole diverse.
  - Esito: **ok**. Togliere il passaggio in minuscolo dà 1 FAIL.

**Riesecuzioni:** suite web 303 passed su 3.13.16 e su 3.11.17.

**Rischi esclusi**
- Browser vero: non provato, ho usato solo lexbor come riferimento.
- Enumerazione a 5 atomi: è ancora in corso e i suoi atomi non hanno attributi, quindi non tocca questa correzione.
- Parser vecchio reale (CPython 3.12.3): non riprovato. Su quelle versioni lavora il ripiego, che con annotation-xml dentro math rende la pila incerta e nasconde il resto della pagina.
- Il resto del diff della fetta 10 l'ho visto alla #473 e qui non l'ho rivisto.

**Memoria:** riga #474 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (8d08649). Nessuna lezione nuova.

### Review #475 (chat Mani) — verdetto integrale (diff del commit `6e87492`)

## VERDETTO: APPROVATO

Review #475 (chat Mani). È un delta di soli test sopra HEAD 5a0786f, che chiude V-1 BASSA della verifica esterna #248. Il test nuovo è giusto e fallisce se si toglie la protezione che deve sorvegliare. Worktree e index coincidono (controllato con cmp); dopo il commit della memoria lo staging è intatto.

**Elementi esaminati**

- **tests/test_unit_web_leggi.py:1276** — nuovo test `test_ripiego_annotation_xml_rende_la_pila_incerta`. Prova che nel ripiego un `annotation-xml` dentro math rende la pila incerta.
  - Rischio esaminato: un test che non distingue la protezione.
  - Mutazione in copia su modules/web/leggi.py:312 (annotation-xml messo in pila come «non punto» invece di rendere la pila incerta): 1 FAIL, come hai dichiarato.
  - Nella pagina, `<svg>` dentro `<math>` è un elemento MathML, perché nel contenuto estraneo l'elemento prende lo spazio del nodo corrente. Quindi l'`annotation-xml` che segue è davvero di math e il test esercita il ramo giusto.
  - Esito: **ok**.
- **tests/test_unit_web_leggi.py:1281** — controlla che MK4 non esca dal ripiego.
  - Rischio esaminato: che l'attesa sia sbagliata.
  - lexbor mette MK4 dentro math, quindi nascosto: l'attesa è corretta.
  - Anche il parser attuale dà solo «A», benché il test controlli solo il ripiego.
  - Esito: **ok**. Il controllo `"A" in r` è debole ma non dà falsi positivi: nessun MKn contiene «A».

**Riesecuzioni:** suite web 304 passed su 3.13.16.

**Rischi esclusi**
- Non ho rieseguito la suite su 3.11: il delta è un test solo, puro Python, senza dipendenze di versione.
- Il codice di modules/web/leggi.py non cambia in questo delta; l'ho visto alla #473 e alla #474.
- Browser vero: non provato, ho usato solo lexbor come riferimento.

**Memoria:** riga #475 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola (73a3211). Nessuna lezione nuova.

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 291 → 304 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «304 passed» su Python 3.13.16; 303 su 3.11.17 prima del test del ripiego).
- Test nuovi contro main: 11 FAILED (le sonde V-1/V-2 e la controprova; il «9» della prima versione era sbagliato, V-2 ve #248); il test di tempo passa anche su main (che ha già O(1)) e fallisce con una scansione lineare (misura del verificatore: 16 s).
- Enumerazione esaustiva con oracolo lexbor (script della verifica esterna, 37 atomi senza attributi, parser e ripiego, nuovo contro main 17c0cfc): 4 atomi, 1.874.161 pagine, 0 regressioni e 0 fughe; 5 atomi: 69.343.957 pagine, 0 regressioni e 0 fughe.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

- `5a0786f` (head all'apertura della PR #248): unit-suite success, handoff-check success, verifica-bot in corso alla scrittura. Verifica esterna #248 APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/248#issuecomment-6349304044)).
- `6e87492` e il commit di fine-task con questo handoff: run non ancora disponibili alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: **R-ve246b-5** BASSA (pila incerta su HTML valido con fine tag omessi in desc/foreignObject: si perde il resto della pagina, frequenza non misurata); **R-ve248-3** BASSA preesistente (`<div a = "x>SEGRETO`: con spazi attorno a «=» e virgolette mai chiuse html.parser chiude il tag, i browser scartano il resto).
- Restano: **R-ve246-5** MEDIA preesistente (canvas/object, decisione sul costruttore HTML5), R-469-1, R-466-1, R-466-2, R-ve245-2…5, R-ve245b-4, R-454-2, R-453-2, R-456-2, R-447-1(b), V-2 ve #242, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…10».
