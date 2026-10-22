# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — Chat Mani, fetta 6: note rimaste della PR #242 (R6, PR #243)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #243 (https://github.com/Gasss23/Gas/pull/243): l'operatore ha scritto «mergia quando il bot approva»; l'agente mergia con `verifica-bot` success sull'head (niente ALTA/MEDIA), CI verde, nessun conflitto.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

(`gh` non autenticato nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **V-2 ve #242 bis (`<title/>` apre il titolo)**: `FATTA`
- **R-449-1 (`<title/>` vuoto dentro svg/math)**: `FATTA`
- **V-1 ve #242 bis (test della chiusura in più)**: `FATTA`
- **R-449-2, R-448-1, V-3/V-4 ve #242 (cosmetiche)**: `FATTA`
- **Note del bot #242 sull'handoff della fetta 5**: `SALTATA — dossier della fetta 5 superato da questo`
- **V-1 bot #243 (`<title/>` dentro noscript) e R-451-1**: `FATTA`
- **V-1 ve #243 (XHTML: autochiusi vuoti)**: `FATTA`
- **R-450-1, V-2 ve #243 (punti di integrazione e breakout dentro svg/math)**: `DEFERITA — BASSE preesistenti, registrate`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++++
 modules/web/leggi.py               |  44 ++++++++++++++++++++++++++++++--------------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 337 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  33 ++++++++++++++++-----------------
 tests/test_unit_web_leggi.py       |  49 +++++++++++++++++++++++++++++++++++++++++++++++++
 7 files changed, 266 insertions(+), 218 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
c03b994 fix(web): <title/> solo fuori da svg/math/script/noscript, XHTML con autochiusi vuoti (V-1 bot #243, V-1 ve #243)
32e8469 chore(revisore): memoria review #452 — APPROVATO
3cec5f6 chore(revisore): memoria review #451 — APPROVATO CON RISERVE
ceaf517 docs(fine-task): report, stato e handoff — chat Mani fetta 6 (#243)
6f13e6e fix(web): fetta 6 chat Mani — <title/> apre il titolo fuori da svg/math, test sul contatore (R6)
354f866 chore(revisore): memoria review #450 — APPROVATO CON RISERVE
a5c33b2 chore(revisore): memoria review #449 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit, quindi le righe di `reports/handoff.md` possono differire di poco (l'elenco dei file è esatto).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Quattro verdetti, incollati integralmente: #449 e #450 (chat Mani) sul diff del commit `6f13e6e` (la #449 ha chiuso le proprie riserve nello stesso diff; memoria in `a5c33b2`, `354f866`); #451 e #452 (chat Mani) sul diff del commit `c03b994` (la #451 ha chiuso la propria riserva nello stesso diff; memoria in `3cec5f6`, `32e8469`).

### Review #449 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #449 (chat Mani), 2026-10-21. È la fetta 6 Mani, ramo feat/mani-web-fetta6. Ho esaminato il diff staged (modules/web/leggi.py e tests/test_unit_web_leggi.py). Letture obbligatorie fatte: CLAUDE.md sez. 5, reports/stato_progetto.md (voce della fetta 5) e .claude/agents/memoria_revisore.md (#446–#448).

**Wall of Shame**: niente slicing della history, niente simulazione dei tool, `_get_window` non toccato. Il diff non tocca nemmeno il kernel, i provider o i tetti (10 iterazioni, 8k).

**Elementi del diff esaminati**
- `modules/web/leggi.py:458`: `_Estrattore.handle_startendtag` ora passa `<title/>` a `handle_starttag`, che imposta `_nel_titolo`.
  - Rischio esaminato: che del testo nascosto arrivi al modello. `handle_data` controlla `_salta` prima del titolo, e il titolo resta dentro i marcatori NON FIDATO, sulla riga «Titolo:» tagliata a `MAX_TITOLO`.
  - Sonde fatte: `<TITLE/>`, `<title />…</title >`, `<title/><script>X</title>Y` (Y nascosto, verso sicuro), `<title/>A<title>B</title>C</title>D` (il parser mostra C e D come i browser; il ripiego solo D).
  - Esito: **ok** sulla fuga di testo nascosto, **riserva R-449-1** (sotto).
- `modules/web/leggi.py:590`: nel ripiego un title autochiuso conta come apertura per nome. La chiusura `</title>` lo scala in `modules/web/leggi.py:601`.
  - Rischio esaminato: che il ripiego mostri più del parser. In tutte le sonde mostra al massimo quello che mostra il parser.
  - Esito: **ok**, salvo la stessa R-449-1.
- `modules/web/leggi.py:103`: commento sul SystemError.
  - Rischio esaminato: che il commento affermi una cosa falsa. L'ho riprodotto da me: col gruppo `([ \t\n\r\f/])` dentro la ripetizione possessiva, `match` su `<a b="1"="x>` dà «SystemError: The span of capturing group is wrong» su 3.11.17. Su 3.13.16 lo stesso pattern trova la corrispondenza senza errori.
  - Esito: **ok**.
- `modules/web/leggi.py:113`: la riga da 160 caratteri è andata a capo, quindi R-448-1 è chiusa. Esito: **ok**.
- `tests/test_unit_web_leggi.py:861` e `tests/test_unit_web_leggi.py:862`: chiusura in più dopo una coppia, sul percorso normale.
  - Rischio esaminato: che la mutazione non venga presa. In copia, con `self._aperti[tag] -= 1` sostituito da `pass`: 1 FAIL.
  - Esito: **ok**, V-1 ve #242 (bis) chiusa.
- `tests/test_unit_web_leggi.py:869`: `test_parser_title_autochiuso_apre_il_titolo`. In copia, togliendo `or tag == "title"`: 1 FAIL. Esito: **ok**.
- `tests/test_unit_web_leggi.py:925`: `<title/>SEGRETO</title>VIS` nel ripiego. In copia, togliendo `or nome == "title"` in `modules/web/leggi.py:590`: 1 FAIL. Esito: **ok**.
- `tests/test_unit_web_leggi.py:927`: `<svg>SEGRETO</svg>VIS</svg>VIS` nel ripiego. Esito: **riserva R-449-2** (sotto).

**Verifiche mie**: 171 passed su 3.13.16 e 171 passed su 3.11.17 (venv nello scratchpad).

**Riserve**
- **R-449-1 (chat Mani) BASSA, regressione introdotta da questo diff.**
  - Il problema: dentro svg/math (contenuto «foreign») i browser rispettano l'autochiusura, quindi lì `<title/>` è vuoto davvero. Ora invece apre il titolo.
  - Effetto sul parser: con `<svg><title/></svg>CORPO` tutto il corpo che segue finisce nel campo titolo, tagliato a 200 caratteri. Prima della modifica CORPO restava nel corpo.
  - Effetto sul ripiego: nasconde il resto della pagina in attesa di un `</title>` che non arriva.
  - Non esce testo nascosto: si perde testo vero, su pagine legittime con icone SVG che hanno `<title/>` vuoto.
  - Correzione: aprire il titolo solo se non ci sono svg o math aperti, in entrambi i punti:
    - nel parser: `tag == "title" and not any(self._aperti.get(n, 0) for n in _AUTOCHIUDIBILI)`
    - nel ripiego: lo stesso controllo su `aperti`.
  - L'ho provata in copia: 171 passed. `<svg><title/></svg>CORPO` dà CORPO nel corpo sia nel parser sia nel ripiego, e i casi `<title/>` fuori da svg restano come nel diff.
  - Consiglio di chiuderla in questa stessa PR, perché costa due righe: un test `<svg><title/></svg>VIS` e una nuova review. Altrimenti va tracciata in stato_progetto.md.
- **R-449-2 (chat Mani) COSMETICA.** Il caso `tests/test_unit_web_leggi.py:927` non distingue niente: la prima VIS basta all'asserzione `"VIS" in t`. La mutazione «il ripiego non scala `aperti`» sopravvive a questo caso, anche se la prende un altro caso già presente (`<svg><noscript>SEGRETO</svg>…`). Correzione: usare `<svg>SEGRETO</svg></svg>VIS`.

**Rischi esplicitamente esclusi**
- Non ho rifatto il fuzz fuzz5.py a 200k/100k: prendo il dato dell'agente. Ho sondato a mano i casi del title.
- Non ho controllato l'invariante «ripiego ⊆ parser» con la correzione di R-449-1: va fatto quando la si applica.
- Non ho misurato le prestazioni su 2 MB: il diff aggiunge solo un confronto per tag e non cambia la complessità.
- Comportamento su VPS e html.parser di Python diversi da 3.13.16 e 3.11.17 non verificati: non riproducibili qui.

Riga contatore #449 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md, con una lezione nuova: le correzioni «come nei browser» su `<x/>` vanno provate anche dentro svg/math. Committata con scripts/commit_memoria_revisore.sh (a5c33b2). Il diff staged del motore resta intatto nell'index.

Script delle sonde: /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r449.py e /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r449se.py. Copia con la correzione proposta: /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r449c. Lì al momento è attiva la mutazione «il ripiego non scala `aperti`», non la correzione: l'originale è in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r449c_orig.py.

---

### Review #450 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #450 (chat Mani), 2026-10-21. È la ri-review della #449 sulla fetta 6 Mani, ramo feat/mani-web-fetta6. Ho esaminato il diff staged: modules/web/leggi.py e tests/test_unit_web_leggi.py. Prima della review ho letto CLAUDE.md (sezioni 1, 4, 5, 8, 9), reports/stato_progetto.md e la mia memoria. Nessun antipattern del Wall of Shame: il diff non tocca la history, non simula tool e non tocca i provider.

**Elementi del diff esaminati**
- `modules/web/leggi.py:459` — il parser calcola `dentro_svg` dal contatore per nome `_aperti` di svg e math. Rischio esaminato: con svg già chiuso il contatore non torna a zero. Esito: ok, `<svg></svg><title/>TIT</title>VIS` e `<svg/><title/>TIT</title>VIS` danno «Titolo: TIT» e VIS nel corpo.
- `modules/web/leggi.py:460` — `<title/>` apre il titolo solo se non c'è svg o math aperto. Dentro, il ramo va a `super().handle_startendtag`, che apre e chiude subito il titolo, quindi `_nel_titolo` torna False. Rischio esaminato: il titolo resta aperto dentro l'icona. Esito: ok. `<svg><title/></svg>VIS`, `<math><title/></math>VIS`, `<SVG><TITLE/></SVG>VIS`, `<svg><g><title /></g></svg>VIS` e `<math><svg><title/></svg></math>VIS` lasciano VIS nel corpo, senza riga «Titolo:». L'oracolo html5lib 1.1 (installato nello scratchpad) dà lo stesso visibile.
- `modules/web/leggi.py:592` e `modules/web/leggi.py:593` — il ripiego fa la stessa scelta e conta il titolo per nome in `aperti`. Rischio esaminato: l'invariante «ripiego ⊆ parser» si rompe. Esito: ok. Ho scritto un fuzz mio, indipendente da fuzz5.py: 14 nomi (svg, math, title, script, noscript, style, textarea, foreignObject, desc, mi, g, p, maiuscole) in 5 forme, più i commenti. Risultato: 0 fughe «ripiego ⊆ parser» e 0 casi in cui la versione nuova mostra più di HEAD, su 60k pagine con 3.13.16 e 60k con 3.11.17.
- `modules/web/leggi.py:117` — commento aggiornato («o è il titolo»). Corrisponde al codice. Esito: ok.
- `modules/web/leggi.py:103` — il commento sul SystemError è preciso: la #449 l'ha riprodotto su 3.11.17. Esito: ok.
- `tests/test_unit_web_leggi.py:877` — il test nuovo prova svg e math su entrambi i percorsi. Rischio esaminato: test vacuo. Esito: ok. Ho fatto una mutazione in copia (il ripiego apre il titolo anche dentro svg): fallisce solo questo test, 1 FAIL su 172.
- `tests/test_unit_web_leggi.py:937` — `<svg>SEGRETO</svg></svg>VIS` ora discrimina, perché il VIS è uno solo. Esito: ok, R-449-2 chiusa.
- `tests/test_unit_web_leggi.py:869` — `<title/>TITOLO_X</title>` va nel titolo e compare una volta sola. Esito: ok.

Suite web: 172 passed su 3.13.16. Su 3.11 di sistema pytest non c'è: lì ho fatto solo il fuzz e mi fido del vostro run nel venv.

**Riserve**
- **R-450-1 (chat Mani), BASSA, preesistente.** È identica a HEAD, non è una regressione. Dentro il contenuto foreign ci sono dei punti in cui il browser torna alle regole HTML (si chiamano «punti di integrazione HTML»): in svg sono foreignObject, desc e title; in math sono mi, mo, mn, ms e mtext. Lì `<title/>` è un tag HTML: l'autochiusura viene ignorata e apre un titolo. Esempio: `<p>a</p><svg><foreignObject><title/></svg>SEGRETO</title>X`. Per html5lib SEGRETO è testo del titolo, quindi invisibile; parser e ripiego invece lo mostrano nel corpo, sia a HEAD sia ora. Stessa cosa con `<svg><desc><title/>` e `<math><mi><title/>`. È un canale di testo nascosto della stessa classe di R-446-1. Correzione possibile: contare per nome i punti di integrazione aperti (foreignobject, desc, mi, mo, mn, ms, mtext, annotation-xml) e considerare `dentro_svg` falso quando ce n'è uno aperto, in entrambi i punti (`modules/web/leggi.py:459` e `modules/web/leggi.py:592`). Va registrata in stato_progetto.md.

**Rischio escluso**
- Non ho provato browser veri (Chromium, Firefox): ho usato html5lib 1.1 come oracolo conforme allo standard, e può divergere dai browser attuali su casi limite del contenuto foreign.
- Non ho rifatto il run della suite su 3.11 né quello con rete e DNS bloccati: su 3.11 di sistema pytest manca, quindi riporto i vostri dati.
- Non ho controllato i tempi su input avversari grandi: le due righe aggiunte sono un `any` su 2 chiavi per tag autochiuso, costo costante.

**Memoria**
- Riga #450 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, con una lezione nuova: «dentro svg/math» non è uno stato unico, perché nei punti di integrazione valgono di nuovo le regole HTML; ogni eccezione «come nel contenuto foreign» va sondata anche lì, con un oracolo conforme (html5lib).
- Committata con scripts/commit_memoria_revisore.sh: commit 354f866. L'index del diff staged (leggi.py e test) è intatto.

File utili nello scratchpad:
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/fuzz450.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/oracolo.py (confronto HEAD / nuovo / html5lib)

---

### Review #451 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #451 (chat Mani), 2026-10-21. Fetta 6 Mani, PR #243, diff STAGED su head ceaf517. Ho letto prima CLAUDE.md (sezioni 1, 5, 8, 9 e 10), reports/stato_progetto.md (per grep) e la memoria del revisore (lezioni #445-#450, tra cui quella sui punti di integrazione svg/math).

**Elementi del diff esaminati**

1. `modules/web/leggi.py:463` — `<title/>` apre il titolo solo se `not self._salta`. Ho controllato che svg e math restino esentati come prima (sono nel contatore) e che noscript, `<script/>…<TITLE/>` e template non aprano più il titolo. **Esito: riserva (R-451-1, sotto).** Sui casi noscript e `<script/>…<TITLE/>` è corretto: con lo scripting attivo noscript è testo, e il secondo è testo dello script.
2. `modules/web/leggi.py:464` — in XHTML `handle_startendtag` torna al comportamento predefinito di html.parser, che chiama apertura e poi chiusura. Rischio esaminato: contatore sbilanciato. Per i nomi in `_SALTA` `handle_endtag` scala `_aperti`/`_salta` subito dopo l'aumento, quindi il saldo è 0. Per title `_nel_titolo` si accende e si spegne. **Esito: ok.**
3. `modules/web/leggi.py:596` — nel ripiego, in XHTML un grezzo autochiuso non apre niente. In HTML il titolo usa `not salta`, che specchia il parser. **Esito: ok.**
4. `modules/web/leggi.py:604` — nel ripiego i contati autochiusi non aprono niente se `xhtml` oppure se sono svg/math. Questo coincide con il parser, che in XHTML ha saldo 0. **Esito: ok.**
5. `modules/web/leggi.py:636` — `xhtml` viene da `pagina["tipo"]`. Rischio: un tipo con maiuscole o parametri che non combacia. Il tipo arriva già minuscolo e senza `;charset` (vedi `modules/web/leggi.py:393`). Il valore passa sia all'estrattore sia al ripiego (`modules/web/leggi.py:645`). **Esito: ok.**
6. `tests/test_unit_web_leggi.py:877` — il test XHTML copre il percorso normale, il ripiego con `xhtml=True` e anche il verso HTML: in HTML `<script/>` continua ad aprire (`tests/test_unit_web_leggi.py:886`), quindi il test ha senso. **Esito: ok.**
7. `tests/test_unit_web_leggi.py:895` — aggiunto il caso `<template><title/></template>VIS`, con l'attesa che VIS resti nel corpo. **Esito: riserva**, perché fissa nel test il comportamento di R-451-1.

**Verifiche mie**
- `pytest tests/test_unit_web_leggi.py`: 173 passed su Python 3.13.16.
- I fuzz dell'autore, rilanciati con un seme mio (451), danno 0 fughe in entrambi i casi:
  - `fuzz5.py`, HTML: 30k casi.
  - `fuzz5x.py`, XHTML: 30k casi.
- Ho confrontato con l'oracolo html5lib 1.1 (in scratchpad) il codice a HEAD 6f13e6e e il diff staged, con 7 sonde.

**Riserve**

- **R-451-1 (chat Mani) — BASSA.** L'esenzione `not self._salta` (`modules/web/leggi.py:463`, e lo specchio `modules/web/leggi.py:596`) è più larga del necessario.
  - Copre anche template, object e canvas. Lì i browser applicano le regole HTML: `<title/>` apre davvero il titolo, che si porta via il resto fino a `</title>`.
  - Oracolo: `<p>a</p><object><title/></object>VIS` dà come testo visibile solo «a», con title = «</object>VIS». Stesso risultato per canvas e template.
  - A HEAD VIS finiva nella riga «Titolo:», limitata a 200 caratteri: era la stessa resa dei browser. Con il diff esce intero nel corpo, cioè testo che i browser nascondono arriva al modello senza limite. Resta comunque dentro il blocco non fidato, per questo la gravità è BASSA.
  - `tests/test_unit_web_leggi.py:895` fissa il caso template nel verso sbagliato.
  - Correzione provata in una copia (`/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r451/leggi_alt.py`):
    `tag == "title" and not any(self._aperti.get(n, 0) for n in self._SALTA - {"template", "object", "canvas"})`
  - Con questa correzione:
    - restano corretti noscript (VIS nel corpo), `<svg><title/></svg>VIS`, `<script/><TITLE/>X</script>VIS` e `<object><noscript><title/></noscript></object>VIS`;
    - template e object tornano a «Titolo: VIS».
  - Va specchiata nel ripiego con lo stesso insieme, al posto di `not salta`. Poi vanno rifatti il fuzz di parità e il test a `tests/test_unit_web_leggi.py:895` (template: «Titolo:» presente).
  - Conviene chiuderla in questa stessa PR: costa poco.
- **V-2 ve #243 (fuga di `<p>`/`<div>` fuori da svg).** Confermata preesistente: è la stessa classe di R-450-1. Anche `<svg><foreignObject><title/>` mostra VIS sia a HEAD sia nel diff, mentre per i browser è title. Va registrata come dichiarato.

**Rischi esplicitamente esclusi**
- Non ho rifatto la suite su Python 3.11 né il fuzz XHTML su 3.11 (le 22 fughe con `<!-->`). Mi baso sui numeri dichiarati dall'autore. Quella differenza di 3.11 è già nota (V-2 ve #242).
- Non ho rifatto le mutazioni dichiarate dall'autore. Ho fatto solo la variante della correzione di R-451-1.
- L'oracolo html5lib non ha lo scripting attivo, quindi per noscript non rappresenta i browser reali. Su quel caso il giudizio si basa sullo standard (con scripting attivo noscript è testo grezzo), non sull'oracolo.
- La fedeltà XHTML oltre gli autochiusi non è verificata: per esempio il markup dentro `<script>` in XML. È fuori dallo scopo del diff.

Riga #451 aggiunta in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, insieme a una lezione nuova: un'esenzione basata sul contatore globale va sondata per ogni nome contato. Committata con `scripts/commit_memoria_revisore.sh` (commit 3cec5f6, solo quel file). Il diff staged di leggi.py e dei test è rimasto intatto nell'index.

---

### Review #452 (chat Mani)

## VERDETTO: APPROVATO

Review #452 (chat Mani), 2026-10-21. È la ri-review della #451 sul diff STAGED del ramo feat/mani-web-fetta6 (PR #243): modules/web/leggi.py e tests/test_unit_web_leggi.py. Il diff staged contiene anche la parte XHTML e noscript già approvata nella #451, che resta valida.

**Elementi del diff esaminati**
1. `modules/web/leggi.py:127`: introduce `_TITOLO_VUOTO_IN = _TAG_NASCOSTI - {"template", "object", "canvas"}`, cioè script, style, noscript, svg, math e iframe. Rischio esaminato: che l'insieme non corrisponda a quello che fanno i browser. Ho fatto 24 sonde contro l'oracolo html5lib 1.1 (che ho nello scratchpad). Le sonde coprono i 9 nomi nascosti, sia aperti sia autochiusi; i casi annidati template>svg, object>noscript, svg>object e canvas>svg; le maiuscole; `<title />`. Con template, object e canvas il testo dopo va nel titolo (invisibile), come nei browser. Con svg, math, script, style e iframe resta visibile nel corpo. Noscript fa eccezione solo verso html5lib, che lavora con gli script spenti: col modello «script attivi» già scelto in V-1 bot #243 il testo resta visibile, ed è coerente. Esito: ok.
2. `modules/web/leggi.py:466`: nel parser `<title/>` apre il titolo solo se nessun nome di `_TITOLO_VUOTO_IN` è aperto in `_aperti`. Rischio esaminato: un contatore che resta alto. Il conto è per nome, quindi una chiusura con un nome diverso non lo fa scendere. Un nascosto lasciato aperto senza chiusura tiene `_salta` sopra zero, e il testo dopo è comunque nascosto (verso sicuro). Esito: ok.
3. `modules/web/leggi.py:600`: nel ripiego c'è lo stesso controllo, sullo stesso insieme. Rischio esaminato: che parser e ripiego divergano. Ho fatto un fuzz mio con seme 452: 13 nomi (compresi foreignObject, textarea e title) in 4 forme, più i commenti. Risultato: 0 fughe «ripiego ⊆ parser» su 40.000 pagine (Python 3.13). La riga resta entro 110 caratteri. Esito: ok.
4. `tests/test_unit_web_leggi.py:877`: il nuovo test `test_title_autochiuso_dentro_template_object_canvas_apre_il_titolo`. Rischio esaminato: un test che passa anche senza la correzione. Ho fatto tre mutazioni in copie prese dall'index: insieme uguale a tutti i nascosti; noscript tolto dall'insieme; solo il ripiego su tutti i nascosti. Ognuna dà 1 FAIL: la prima e la terza fanno fallire questo test, la seconda fa fallire `tests/test_unit_web_leggi.py:900`. Esito: ok.
5. `tests/test_unit_web_leggi.py:905`: `<script/><title/></script>VIS` sostituisce il caso template, che prima era fissato nel verso sbagliato (R-451-1). Ho verificato con html5lib che VIS è visibile, come chiede il test. Esito: ok.

Suite: 174 passed su 3.13 (`tests/test_unit_web_leggi.py`). Nel diff nessuno slicing della history, nessuna simulazione dell'output dei tool, nessun tocco a `_get_window`, al limite di 10 iterazioni o al limite di 8k caratteri in uscita.

R-451-1 è chiusa.

**Rischi esclusi esplicitamente**
- Non ho rifatto io le prove su 3.11 né quelle con rete e DNS bloccati: la fonte è l'autore. La parte cambiata è logica pura sul contatore, senza dipendenze dalla versione di html.parser, e le altre verifiche su 3.11 le avevo fatte nelle #449 e #450.
- La riserva preesistente R-450-1 (punti di integrazione HTML dentro svg e math, per esempio foreignObject) non è toccata da questo diff e resta aperta.
- Il comportamento dei browser veri non l'ho verificato: l'oracolo è html5lib 1.1, che lavora con gli script spenti.

**Memoria**: ho aggiunto la riga #452 a `/home/user/Gas/.claude/agents/memoria_revisore.md` e l'ho committata con `scripts/commit_memoria_revisore.sh` (commit 32e8469, `chore(revisore): memoria review #452 — APPROVATO`). Nessuna lezione nuova. Il diff staged è rimasto intatto: 2 file, 50 righe aggiunte e 16 tolte.

File utili:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/s452/sonde.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/s452/fuzz.py

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 167 → 174 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «174 passed in 19.91s» su Python 3.13; «174 passed in 19.38s» su 3.11 (venv); «174 passed in 18.83s» con rete e DNS veri bloccati via sitecustomize). Primo giro (`6f13e6e`) 167 → 172, secondo (`c03b994`) 172 → 174.
- Fuzz differenziale ripiego contro parser: 0 fughe su 200k pagine HTML (3.13), 100k (3.11, escluse `<!-->`), 100k XHTML (3.13).
- Mutazioni del secondo giro, tutte prese: esenzione del titolo estesa a tutti i nascosti / solo svg-math / senza script, xhtml ignorato nel parser, nel ripiego (grezzi e contati) e in `_componi`, title aperto ovunque.
- Mutazioni in copie isolate, tutte prese: parser `_aperti` che non scala, ripiego `aperti` che non scala, `<title/>` vuoto nel parser, title autochiuso ignorato nel ripiego, title anche dentro svg (parser e ripiego).
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

`gh` non autenticato nella sessione cloud: esiti letti dai check della PR #243 via MCP GitHub. Mappatura commit→run:
- `a5c33b2`, `354f866`, `6f13e6e`: pushati insieme prima di aprire la PR; run di push sulla testa `6f13e6e` non letta (handoff-check atteso rosso: handoff non ancora aggiornato).
- `ceaf517` (fine-task del primo giro): run 39694284271, unit-suite success, handoff-check success; verifica-bot success (letto dalla verifica esterna #243 e dal check della PR).
- `3cec5f6`, `32e8469`, `c03b994`: nessuna run su questi SHA da soli (pushati col commit di fine-task che contiene questo file).
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: **V-2 ve #243** BASSA preesistente: `<p>`/`<div>` dentro svg fanno uscire dal contenuto foreign per i browser (`<svg><p><title/></svg>X</title>` mostra X), non coperta dalla correzione proposta per R-450-1; **R-450-1 (chat Mani)** BASSA preesistente: nei punti di integrazione HTML dentro svg/math (foreignObject, desc, title; mi, mo, mn, ms, mtext) `<title/>` apre un titolo per i browser, mentre parser e ripiego lo trattano come vuoto.
- Restano: R-447-1 parte (b), V-2 ve #242 (commenti vuoti su 3.11), R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…6».
