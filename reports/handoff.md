# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-23 — Chat Mani, fetta 13: riserve minori della #252, titolo XHTML annidato (R6)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 13: solo con verdetto del bot APPROVATO puro sull'head finale e CI verde, oppure con il tuo ok.
2. **R-ve252-2 (BASSA, preesistente)**: estendere «il resto della pagina se ne va» a tutto l'XHTML malformato (più sicuro, si perde testo)? Decidi tu.
3. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; serve un vero costruttore HTML5 (es. lexbor): decidi tu.
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

---

## §1 SCOPE & ESITO FETTE

- **V-2 bot #252 / V-4 ve #252** (avviso del parser vecchio): `FATTA`
- **V-1 ve #252 quater** (test sulle virgolette nel DOCTYPE): `FATTA`
- **R-456-2** (commento): `FATTA`
- **R-ve245-5** (titolo XHTML annidato): `FATTA`
- **Secondo giro, bot #255 su 2dd08b6 APPROVATO CON RISERVE**: V-1 BASSA (contatore del titolo anche in HTML) `FATTA`; V-2 COSMETICA (commento dei test) `FATTA`
- **Verifica esterna #255 APPROVATO CON RISERVE**: V-1 BASSA (= V-1 bot) `FATTA`; V-2 BASSA (test dell'avviso in parallelo) `FATTA`; V-3 COSMETICA `FATTA`; V-4 COSMETICA voluto

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +
 modules/web/leggi.py               |  26 +++---
 reports/diff_sessione.md           |  11 ++-
 reports/handoff.md                 | 173 ++++++++++++++++++++++++++++++++-----
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  27 ++++--
 tests/test_unit_web_leggi.py       |  50 ++++++++++-
 7 files changed, 246 insertions(+), 47 deletions(-)
```

NB: preso dall'index con tutti i report in stage, dopo aver scritto questo handoff (V-3 ve #252); solo la riga di `reports/handoff.md` può differire di poche righe, perché lo stat è dentro il file stesso.

---

## §3 GIT LOG --ONELINE (sessione)

```
2f903fb docs(reports): fetta 13 chat Mani, terzo giro — report, handoff, stato
95627a4 test(web): fetta 13 — avviso in parallelo davvero, sonde del titolo in svg/math (V-1/V-2 ve #255)
4aea67b chore(revisore): memoria review #494 — APPROVATO
2a0340f docs(reports): fetta 13 chat Mani, secondo giro — report, handoff, stato
58fc102 fix(web): fetta 13 — titolo contato solo in XHTML (V-1/V-2 bot #255)
ed769e1 chore(revisore): memoria review #493 — APPROVATO
2dd08b6 docs(reports): fine fetta 13 chat Mani — report, handoff, stato
60f64b8 feat(web): fetta 13 — riserve minori della #252, titolo XHTML annidato (R6)
208a89c chore(revisore): memoria review #492 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Tre verdetti, incollati integralmente (chat Mani): #492 (APPROVATO) sul diff della fetta 13 committato in `60f64b8`; #493 (APPROVATO) sul secondo giro committato in `58fc102`; #494 (APPROVATO) sui test della verifica esterna committati in `95627a4`.

### Review #492 (chat Mani) — verdetto integrale (fetta 13, diff committato poi in un solo commit)

## VERDETTO: APPROVATO

Review #492 (chat Mani), fetta 13 sul ramo feat/mani-web-fetta13 (da main 0d70e82). Chiude 4 riserve aperte: V-2 bot / V-4 verifica esterna #252 (avviso nel log), V-1 verifica esterna #252 quater (test sulle virgolette), R-456-2 (commento) e R-ve245-5 (titolo annidato in XHTML). Le modifiche sono corrette e nessuna fa uscire testo nascosto.

**Cosa ho esaminato**
- `modules/web/leggi.py:131` e `modules/web/leggi.py:1335`: l'avviso del parser vecchio ora usa un solo `threading.Lock`, preso con `acquire(blocking=False)` e mai rilasciato.
  - Rischi esaminati: l'avviso scritto due volte con letture in parallelo, e cosa succede quando `monkeypatch` sostituisce il lucchetto nei test.
  - Esito ok:
    - la presa senza attesa è atomica, quindi solo la prima lettura scrive il warning;
    - nel test `monkeypatch` mette un `Lock` nuovo e lo ripristina dopo, quindi il lucchetto del modulo resta libero per gli altri test;
    - `caplog` raccoglie anche i log dei thread.
- `modules/web/leggi.py:817` e `modules/web/leggi.py:946`: `_nel_titolo` diventa un contatore, e la chiusura lo diminuisce solo se è maggiore di 0.
  - Rischio esaminato (quello che chiedevi): fughe o perdite in HTML, con title dentro svg o math e con chiusure in più.
  - Esito ok. Il contatore decide solo se un testo va nella riga «Titolo:» o nel corpo, e tutte e due arrivano al modello. Il testo nascosto è già filtrato prima da `_salta`, `incerta` e `_taglia` (in `handle_data`), quindi una fuga nuova non è possibile.
  - Sonde HTML, con risultato identico a main 0d70e82:
    - `<svg><title>a<title>b</title></title></svg>`
    - `<svg><title><title></svg>X</title>Y`
    - `</title></title>` in più
    - `<title/>`
    - `<template><title>`
  - In XHTML `<title>T<title></title>X</title><p>VIS</p>` dà ora «Titolo: T X» con VIS nel corpo, come il ripiego. Su main X finiva nel corpo.
- `tests/test_unit_web_leggi.py:1149`: le 2 pagine con virgolette nel sottoinsieme del DOCTYPE, fuori da una dichiarazione.
  - Rischio esaminato: il mutante «virgolette fuori dichiarazione senza -1» che sopravvive.
  - Esito ok: in una copia isolata dà 2 FAIL.
- `tests/test_unit_web_leggi.py:1232` (test dell'avviso con 8 thread) e `tests/test_unit_web_leggi.py:1316` (titolo annidato): ok.
- Suite web: 380 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.
- Nessuna riga aggiunta supera i 121 caratteri. Il commento di R-456-2 è cosmetico e corretto.

**Cosa non ho verificato**
- La suite col parser vecchio (371 passed e 10 skipped).
- Le mutazioni «titolo booleano» e «avviso sempre scritto» di mut13/run.py: ho rifatto solo quella sulle virgolette.
- La corsa fra thread reali: il test con 8 thread non può provarla in modo deterministico. L'unicità dell'avviso la garantisce `acquire(blocking=False)` per come è fatto, non il test.
- In HTML un title rimasto aperto (es. `<svg><title>` non chiuso) manda ancora il testo dopo nella riga del titolo, che ha un tetto di lunghezza. Era così anche su main: è una possibile perdita, cioè testo che va perso e non testo nascosto che esce.

**Memoria**: aggiunta la riga #492, nessuna lezione nuova. Committata con `scripts/commit_memoria_revisore.sh` (commit 208a89c). Lo stage dei due file non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py

### Review #493 (chat Mani) — verdetto integrale (V-1 e V-2 del bot #255)

## VERDETTO: APPROVATO

Review #493 (chat Mani), sul delta in stage della PR #255 (head 2dd08b6) per il bot #255. Il numero #493 era libero: in memoria il più alto era #492.

In HTML il titolo torna a comportarsi come su main; in XHTML resta il contatore introdotto nella #492.

**Cosa ho esaminato**
- `modules/web/leggi.py:818`: `_nel_titolo` conta le aperture solo in XHTML. In HTML resta a 1 e la chiusura lo riporta a 0, cioè lo stesso comportamento di main con il booleano.
  - Rischio esaminato: V-1 del bot, cioè aperture accumulate dentro svg/math che all'uscita non si scalano.
  - Esito ok:
    - la sonda del bot `<math><title><title></math><title>T</title><p>BODY</p>` dà «Titolo: T» con BODY nel corpo;
    - 6 sonde HTML danno lo stesso testo di main 0d70e82: title annidati in math/svg, `</title>` in più, `<svg><title><title></svg>X</title>Y`, `<math><mi><title>`, `<title/>`.
- `tests/test_unit_web_leggi.py:1315`: test nuovo sulla sonda del bot.
  - Rischio esaminato: che la regressione possa tornare senza che un test se ne accorga.
  - Esito ok: con il mutante «conta anche in HTML» (`+= 1`, cioè il codice della #492) in una copia isolata, la suite dà 1 FAIL.
  - Il test non ha il marcatore del parser aggiornato; col parser vecchio passa dal ripiego, che tiene BODY nel corpo.
- V-2 COSMETICA: il commento «(V-3 ve #252)» ora sta sopra i suoi casi. Ok.
- Suite web: 381 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Una mia mancanza da segnalare**
- Nella #492 le mie sonde non avevano preso questo caso. Quella con svg era nascosta per altri motivi, e non avevo provato il caso «apri due title dentro math, esci, poi un titolo vero fuori». L'ho aggiunto come lezione in memoria.

**Cosa non ho verificato**
- La suite col parser vecchio (372 passed e 10 skipped).
- La mutazione «titolo booleano» della tua run2.py: il test XHTML della #492 la copriva già.
- Il titolo in XHTML quando si esce dal contenuto estraneo: in XHTML le chiusure sono esplicite e Gas non fa uscite implicite da svg/math, ma non l'ho sondato.

**Memoria**: aggiunte la riga #493 e una lezione (un contatore di aperture vale solo dove le chiusure sono garantite). Committate con `scripts/commit_memoria_revisore.sh` (commit ed769e1). Lo stage dei due file non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py

### Review #494 (chat Mani) — verdetto integrale (test per V-1 e V-2 della verifica esterna #255)

## VERDETTO: APPROVATO

Review #494 (chat Mani), sul delta in stage della PR #255 (head 2a0340f). Cambia solo il file di test, per la verifica esterna #255. Il numero #494 era libero: il più alto in memoria era #493.

**Cosa ho esaminato**
- `tests/test_unit_web_leggi.py:1239`: il test dell'avviso ora fa partire 8 letture insieme, sincronizzate con `threading.Barrier(8)` mentre il lucchetto è ancora libero, e poi fa le 3 letture in fila.
  - Rischio esaminato: V-2, cioè che la parte in parallelo non provi niente; e in più che il test resti appeso o dia esiti a caso.
  - Esito ok:
    - in una copia isolata ho scritto un mutante non atomico (`locked()`, poi 20 ms di attesa, poi `acquire`): il test fallisce 3 volte su 3;
    - sul codice vero passa 5 volte su 5;
    - la Barrier non può bloccarsi, perché ogni thread chiama `wait()` prima di qualsiasi lavoro.
- `tests/test_unit_web_leggi.py:1324`: le 2 sonde della verifica esterna, `<svg><title><title>x</title></svg>BODY` e `<math><title>a<title>b</title></math>BODY`, aggiunte come parametri insieme a quella del bot.
  - Rischio esaminato: V-1 che può tornare senza che un test se ne accorga.
  - Esito ok: tutte e 3 passano sul codice approvato nella #493. Il mutante «conta anche in HTML» dà 3 FAIL secondo la tua run3.py; io l'avevo già provato sul caso del bot nella #493.
- Suite web: 383 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Nota cosmetica**
- Se un'eccezione avviene dentro uno dei thread, il test non fallisce: le 3 letture in fila scrivono comunque l'avviso una volta. È un buco minore, non blocca.

**Cosa non ho verificato**
- La suite col parser vecchio (374 passed e 10 skipped).
- Il codice: non è cambiato rispetto alla #493, perché in stage c'è solo `tests/test_unit_web_leggi.py`.
- V-4 (in XHTML un titolo non chiuso si porta dietro il resto): è il comportamento voluto, uguale al ripiego, e non l'ho sondato di nuovo.

**Memoria**: aggiunta la riga #494, nessuna lezione nuova. Committata con `scripts/commit_memoria_revisore.sh` (commit 4aea67b). Lo stage non è stato toccato.

File:
- /home/user/Gas/tests/test_unit_web_leggi.py

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 377 → 383 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «383 passed, 1 skipped» su Python 3.13 e 3.11; lo skip è il test d'allarme che gira solo in CI). Col html.parser non patchato di CPython 3.12.3 caricato da plugin: 374 passed, 10 skipped (i test che vogliono il parser).
- Mutazioni in copie isolate (scratchpad/mut13/run.py): titolo booleano 1 FAIL, conta anche in HTML 3 FAIL, avviso non atomico 1 FAIL su 5 ripetizioni su 5 (scratchpad/mut13/run3.py), avviso sempre scritto 1 FAIL, virgolette fuori dichiarazione nel DOCTYPE 2 FAIL.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

- `2dd08b6` (apertura della PR #255): unit-suite, handoff-check e verifica-bot success; bot APPROVATO CON RISERVE (V-1 BASSA e V-2 COSMETICA, chiuse in `58fc102`).
- Verifica esterna #255 su `2dd08b6`: APPROVATO CON RISERVE (V-1, V-2 BASSE chiuse; V-3, V-4 COSMETICHE).
- `2a0340f` (secondo giro, pushato): run in corso alla scrittura; `95627a4` e il commit di fine-task con questo handoff: run non ancora disponibili alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Restano: **R-ve252-2** BASSA preesistente (XHTML malformato letto come HTML, da decidere), **R-ve246-5** MEDIA preesistente (canvas/object, decisione sul costruttore HTML5), R-469-1, R-447-1(b), R-ve245-2…4, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…13».
