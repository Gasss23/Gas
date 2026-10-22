# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-22 — Chat Mani, fetta 7: note dell'ultimo giro della PR #243 (R6, PR #244)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #244 (https://github.com/Gasss23/Gas/pull/244): vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

(`gh` non autenticato nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **R-453-1 (grezzi autochiusi in testo grezzo) e V-2 ve #243 bis**: `FATTA`
- **R-454-1 (esenzione svg/math solo per i non nascosti)**: `FATTA`
- **V-1 bot #243 (`<title/>` in template)**: `FATTA`
- **V-2 bot #243 (XHTML: commenti e CDATA)**: `FATTA`
- **V-1 ve #243 bis (test propagazione XHTML al ripiego)**: `FATTA`
- **V-3 bot #243 (conteggi dell'handoff), V-3/V-4/V-5 ve #243 bis (dossier della fetta 6)**: `SALTATA — riguardano il dossier della fetta 6, superato da questo`
- **V-1 bot #244 (noembed/noframes fra i nascosti), V-2 bot #244 (docstring)**: `FATTA`
- **R-454-2, R-453-2, R-456-1, R-456-2**: `DEFERITA — BASSE/COSMETICHE, registrate`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   9 +++++++++
 modules/web/leggi.py               |  74 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 392 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  30 +++++++++++++---------------
 tests/test_unit_web_leggi.py       | 136 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 7 files changed, 450 insertions(+), 203 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
6f9bfe7 fix(web): noembed e noframes fra i nascosti (V-1 bot #244)
85b2ac2 chore(revisore): memoria review #456 — APPROVATO CON RISERVE
51f7986 docs(fine-task): report, stato e handoff — chat Mani fetta 7 (#244)
54706c2 fix(web): fetta 7 chat Mani — grezzi autochiusi in testo grezzo, XHTML commenti/CDATA, title in template (R6)
ec14e89 chore(revisore): memoria review #455 — APPROVATO CON RISERVE
a75a310 chore(revisore): memoria review #454 — BOCCIATO
7f28b4c chore(revisore): memoria review #453 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit, quindi le righe di `reports/handoff.md` possono differire di poco (l'elenco dei file è esatto).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Quattro verdetti, incollati integralmente: #453, #454 (BOCCIATO), #455 (chat Mani) sul diff del commit `54706c2` (le riserve e il blocco sono stati chiusi nello stesso diff prima del commit; memoria in `7f28b4c`, `a75a310`, `ec14e89`); #456 (chat Mani) sul commit `6f9bfe7` (memoria in `85b2ac2`).

### Review #453 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #453 (chat Mani), 2026-10-22. Diff staged: modules/web/leggi.py e tests/test_unit_web_leggi.py (ramo feat/mani-web-fetta7). Prima della review ho letto CLAUDE.md (sez. 5, 8, 9, 10), le voci Mani e i finding aperti in reports/stato_progetto.md e le lezioni recenti in .claude/agents/memoria_revisore.md.

**Cosa ho controllato nel diff**

- `modules/web/leggi.py:470`: se un template è aperto, `<title/>` conta come apertura nascosta "title" (sale `_aperti["title"]`, sale `_salta`).
  - Rischio: il conteggio si sbilancia, oppure il testo nascosto arriva nella riga «Titolo:».
  - Esito: ok per quello che la nota V-1 bot #243 chiedeva. Il testo fino a `</title>` non compare più né nel titolo né nel corpo.
  - Riserva: c'è una fuga che esisteva già, vedi R-453-1.
- `modules/web/leggi.py:483`: la chiusura di un tag scala qualsiasi nome presente in `_aperti`.
  - Rischio: una chiave estranea viene scalata per sbaglio.
  - Esito: ok. In `_aperti` scrivono solo `handle_starttag` (nomi in `_SALTA`) e il ramo template ("title"). Un `<title>` vero aperto mentre è aperto un titolo-template fa sbagliare la `</title>` ad azzerare `_nel_titolo`. Il testo del corpo finisce allora nella riga «Titolo:», tagliata a 200 caratteri: si perde testo, ma nel verso sicuro (stessa famiglia di V-2 ve #243 bis).
- `modules/web/leggi.py:628`: nuova `_commenti_e_cdata_xml`.
  - Rischi: costo quadratico; ordine fra commento e CDATA che si annidano; escape.
  - Esito: ok.
    - Ogni ricerca riparte solo dopo che la posizione precedente è stata superata, quindi gli intervalli scansionati non si sovrappongono e il costo è lineare.
    - `-1` resta definitivo.
    - Un CDATA dentro un commento e un commento dentro un CDATA si risolvono bene (provato).
    - `&#0000065;` e `&amp;` dentro un CDATA restano testo letterale.
    - Un attributo con `<!--` (XML non valido) fa perdere testo, verso sicuro.
- `modules/web/leggi.py:678`: il preprocesso XML si applica solo ad application/xhtml+xml e prima delle sostituzioni dei riferimenti. Lo stesso `grezzo` arriva anche al ripiego.
  - Rischi: cambiare il comportamento in HTML; il ripiego che riceve il testo non preprocessato.
  - Esito: ok. Lo coprono `tests/test_unit_web_leggi.py:899` (verso HTML invariato) e `tests/test_unit_web_leggi.py:916` (`feed` che solleva ValueError).
- `tests/test_unit_web_leggi.py:929`: 6 pagine da circa 2 MB eseguite in un sottoprocesso con 10 secondi di tempo massimo.
  - Rischio: non accorgersi di un costo quadratico.
  - Esito: ok. Con circa 2 MB un algoritmo quadratico sta molto oltre i 10 secondi.
- `tests/test_unit_web_leggi.py:894`: il test pretende che VIS sia visibile in `<template><title/></template>SEGRETO</title>VIS`.
  - Rischio: il test fissa un comportamento diverso da quello dei browser.
  - Esito: riserva. Per html5lib 1.1 VIS resta dentro il template, quindi invisibile.

Esecuzione: 178 passed su Python 3.13 (`tests/test_unit_web_leggi.py`). Le sonde (casi mirati) sono state confrontate con html5lib 1.1 e girate sulla copia di HEAD, sull'index e su una copia modificata (mutante).

**Riserve (da registrare in stato_progetto.md)**

- **R-453-1 (chat Mani), MEDIA, esisteva già (stessa uscita a HEAD).**
  - Il problema: in HTML i tag grezzi autochiusi (`<title/>`, `<script/>`) non mettono html.parser in modo testo, mentre per i browser aprono testo grezzo. Così la chiusura di un contenitore nascosto scritta dentro quel testo chiude davvero il contenitore, e quello che segue arriva al modello. Succede sia nel parser sia nel ripiego. Esempi:
    - `<p>a</p><template><title/></template></title>INIEZIONE</template>VIS`: per html5lib si vede «a VIS»; Gas dà «INIEZIONEVIS».
    - `<object><title/></object></title>INIEZIONE</object>`: stessa fuga.
    - `<template><script/></template></script>INIEZIONE</template>`: stessa fuga.
  - Il test `tests/test_unit_web_leggi.py:894` introdotto da questo diff fissa proprio questo verso (VIS visibile).
  - Correzione provata in una copia: chiamare `self.set_cdata_mode("title")` subito dopo l'apertura del titolo autochiuso, in tutti e due i rami di `modules/web/leggi.py:470`. Risultato:
    - chiude i casi template e object;
    - chiude anche V-2 ve #243 bis: `<title/><div a="</title>">VIS` dà `">VIS` visibile, come html5lib;
    - rompe solo `tests/test_unit_web_leggi.py:884` (il titolo diventa «</object>TITOLO_X», come in html5lib) e `tests/test_unit_web_leggi.py:894`.
  - Restano da fare: la stessa cosa per `<script/>` e gli altri grezzi, e lo specchio nel ripiego.
- **R-453-2 (chat Mani), BASSA, esisteva già.**
  - Il problema: in XHTML le istruzioni di elaborazione (PI, `<?x ... ?>`) e il sottoinsieme interno del DOCTYPE non vengono trattati, e possono contenere `</script>` o markup invisibile. Stessa famiglia di V-2 bot #243. Esempi, uguali su 3.13 e 3.11:
    - `<script><?x </script> ?>SEGRETO</script>VIS` dà «?>SEGRETOVIS».
    - `<!DOCTYPE html [<!ENTITY e "<p>SEGRETO</p>">]><p>a</p>VIS` dà «SEGRETO».
  - Correzione possibile: in `_commenti_e_cdata_xml` togliere anche `<?`…`?>` e il sottoinsieme `[`…`]>` del DOCTYPE.

**Cosa NON ho verificato**

- Il comportamento dei browser veri su XHTML malformato (Firefox e Chrome mostrano una pagina d'errore): non riproducibile qui. L'oracolo è solo html5lib, che non fa XML.
- Non ho ripetuto i fuzz da 100-200 mila casi dichiarati dall'autore, né girato la suite su 3.11. Su 3.11 ho girato solo le sonde XHTML.
- Non ho eseguito la suite completa del motore: il diff tocca solo `modules/web/leggi.py` e il suo test, non il ciclo `run_turn`, `_get_window` o i provider.

Wall of Shame: nessun taglio della history, nessuna simulazione di output dei tool. I guardrail (10 iterazioni, 8k, `_get_window`) non sono toccati.

**Memoria del revisore**: riga #453 e due lezioni aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole con `scripts/commit_memoria_revisore.sh` (commit 7f28b4c). L'index con il diff sotto review è rimasto com'era.

---

### Review #454 (chat Mani)

## VERDETTO: BOCCIATO

Review #454 (chat Mani), ri-review della #453. Diff staged: modules/web/leggi.py e tests/test_unit_web_leggi.py, su HEAD 7f28b4c, esaminato in copie dell'index e di HEAD nello scratchpad. Ho letto le tre fonti obbligatorie: CLAUDE.md §5, reports/stato_progetto.md (righe della fetta 6, R-450-1, V-2 ve #243) e la memoria del revisore.

**Elementi del diff esaminati**

- modules/web/leggi.py:478 — un grezzo autochiuso (`<title/>` fuori da `_TITOLO_VUOTO_IN`, `<script/>`, textarea…) chiama `handle_starttag`, poi modules/web/leggi.py:482 chiama `_modo_grezzo`. Rischio esaminato: html.parser che continua a leggere i tag. Con l'oracolo html5lib 1.1, `<template><title/></template></title>INIEZIONE</template>VIS` dà solo VIS: R-453-1 è chiusa. Anche `<title/><div a="</title>">VIS` dà `">VIS` come i browser: V-2 ve #243 bis è chiusa. Su 3.13.16 e 3.11.17 `set_cdata_mode` accetta `escapable` e le liste CDATA/RCDATA sono quelle attese. Mutazione «niente `_modo_grezzo`» in copia: 7 FAIL. Esito: ok.
- modules/web/leggi.py:488 — `_modo_grezzo` ripiega su `set_cdata_mode(tag)` se arriva un TypeError. Rischio: un parser vecchio che fa crashare la lettura. Il test con monkeypatch a tests/test_unit_web_leggi.py:931 copre il caso. Esito: ok.
- modules/web/leggi.py:474 — dentro svg/math (`estraneo`) ogni `<x/>` diventa vuoto, anche per i nascosti. Rischio: i punti di integrazione HTML. Esito: **blocco** (R-454-1, sotto).
- modules/web/leggi.py:624 e modules/web/leggi.py:632 — il ripiego copia la stessa esenzione per i grezzi e per i contati. Stesso rischio, stesso blocco. Su tutto il resto ripiego e parser restano allineati: nel mio fuzz, 0 casi in cui il ripiego mostra più del parser.
- modules/web/leggi.py:126 — `_GREZZI_AUTOCHIUSI` esclude plaintext. Per i browser `<plaintext/>` apre plaintext, ma il testo è visibile in entrambi i casi. Esito: ok.
- tests/test_unit_web_leggi.py:909 — le 4 sonde di R-453-1, controllate su parser e ripiego. Mutazione «il ripiego non salta il grezzo autochiuso»: 12 FAIL. Esito: ok.
- tests/test_unit_web_leggi.py:923 e tests/test_unit_web_leggi.py:927 — fissano `<svg><script/></svg>VIS` e `<svg><noscript/></svg>VIS` come visibili. Questo è proprio il comportamento che apre R-454-1. Esito: riserva, vanno cambiati insieme alla correzione.

**Motivo bloccante**

- **R-454-1 (chat Mani), MEDIA: regressione verso la fuga di testo nascosto.** I browser rispettano l'autochiusura nel contenuto svg/math, ma non nei suoi punti di integrazione HTML (foreignObject, desc, mi, mtext…). Lì `<script/>`, `<style/>` e `<iframe/>` aprono testo grezzo, e un `</svg>` scritto dentro non chiude niente. Confronto con l'oracolo html5lib (il testo è nascosto per i browser in tutti i casi):

| Pagina | HEAD (parser e ripiego) | Staged (parser e ripiego) |
|---|---|---|
| `<svg><foreignObject><script/></svg>SEGRETO</script>VIS` | VIS | SEGRETOVIS |
| `<svg><desc><style/></svg>SEGRETO</style>VIS` | VIS | SEGRETOVIS |
| `<math><mi><iframe/></math>SEGRETO</iframe>VIS` | VIS | SEGRETOVIS |
| `<math><mtext><script/></math>SEGRETO</script>VIS` | VIS | SEGRETOVIS |
| `<svg><foreignObject><noscript/></svg>SEGRETO</noscript>VIS` | VIS | SEGRETOVIS |

  In pratica il diff apre un nuovo canale di testo nascosto verso il modello. Il fuzz dichiarato non lo vede: per arrivarci serve una sequenza ordinata di 4 elementi, e anche il mio fuzz casuale su questo alfabeto non l'ha trovata.

  **Correzione provata in copia (3 righe):**
  - parser: `if self._xhtml or (estraneo and tag not in self._SALTA):`
  - ripiego, grezzi: `(estraneo and nome not in _TAG_NASCOSTI)` al posto di `estraneo`
  - ripiego, contati: torna come in HEAD, `(xhtml or nome in _AUTOCHIUDIBILI)`

  **Esito della prova:**
  - Tutte e 5 le sonde danno «niente».
  - Si chiude anche una fuga che c'era già in HEAD: `<svg><foreignObject><script/></svg></script>SEGRETO`.
  - Suite: 183 passed e 1 FAIL atteso, `test_grezzi_autochiusi_come_i_browser`. `<svg><script/></svg>VIS` torna a nascondere VIS: si perde testo, che è il verso sicuro.
  - Fuzz con oracolo html5lib (16 nomi tra cui foreignObject, desc, mi e mtext): 0 casi in cui il ripiego mostra più del parser, e 0 casi «la correzione mostra più di HEAD un testo che i browser nascondono», su 30k pagine (3.13) e 20k (3.11.17), a parte R-454-2.
  - Alternativa che salva anche VIS: contare i punti di integrazione con una pila (chiuderebbe anche R-450-1). È più grande e non l'ho provata.

**Riserve non bloccanti**

- **R-454-2 (chat Mani), BASSA preesistente.** Script con doppio escape: con `<script><!--<script></script>X` i browser nascondono X, html.parser invece chiude al primo `</script>` e lo mostra. È identico in HEAD per `<script>`; ora vale anche per `<script/>`. È l'unico caso trovato dal fuzz su questo diff.
- **R-453-2**: registrata dall'autore, fuori dalla fetta. D'accordo.

**Altre verifiche**

- 184 passed su 3.13.16 e su 3.11.17.
- Pagine avversarie da 2-3 MB (`<script/>` chiusi, `<title/>` in template, foreignObject con script, `</scriptx>` ripetuti): parser ≤1,5 s, ripiego ≤0,55 s.
- `_commenti_e_cdata_xml` (modules/web/leggi.py:644) è invariato rispetto alla #453.
- Niente slicing della history, nessuna simulazione di tool, nessun tocco a `_get_window` né al cap delle 10 iterazioni.

**Rischi esclusi**

- Fuzz e mutazioni girati solo sul mio alfabeto. Non ho rifatto le 6 mutazioni XHTML della #453, perché quella parte non è cambiata.
- Prove con rete e DNS bloccati non ripetute: il diff non tocca il percorso di rete.
- Comportamento su html.parser davvero vecchio (senza `escapable` e con la vecchia regex di chiusura) non verificato: non è installato. Coperto solo dal monkeypatch.
- Punti di integrazione con svg annidato dentro foreignObject non sondati.

Memoria: riga #454 e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, già committate (a75a310). Il diff staged è rimasto intatto.

File utili: /home/user/Gas/modules/web/leggi.py, /home/user/Gas/tests/test_unit_web_leggi.py, /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r454/fix/modules/web/leggi.py (copia con la correzione), /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r454/fuzz454.py (fuzz con oracolo html5lib).

---

### Review #455 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #455 (chat Mani), 2026-10-22. Ri-review della #454 sul diff staged del ramo feat/mani-web-fetta7, che tocca modules/web/leggi.py e tests/test_unit_web_leggi.py. Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), le parti di reports/stato_progetto.md che riguardano R-45x e la coda di .claude/agents/memoria_revisore.md (lezioni #447-#454).

**Elementi del diff esaminati**
1. `modules/web/leggi.py:475` — nel parser, dentro svg/math restano vuoti solo i tag che non stanno in `_SALTA` (`_SALTA` è `_TAG_NASCOSTI`, modules/web/leggi.py:436). Gli altri nascosti aprono come fuori da svg/math, e i grezzi passano al testo grezzo con `_modo_grezzo` (modules/web/leggi.py:489).
   - Rischio esaminato: la fuga di R-454-1 nei punti di integrazione HTML.
   - Prova con l'oracolo html5lib 1.1 su 12 sonde, tutte in verso fuga: foreignObject+script, mi+style, annotation-xml+script, foreignObject+iframe con markup in mezzo, svg annidato dentro foreignObject, math dentro foreignObject, foreignObject+template, desc+textarea, foreignObject+xmp. Ora SEGRETO non esce più, né dal parser né dal ripiego.
   - `<svg><script/></svg>VIS` resta nascosto. Era nascosto già in HEAD (l'ho verificato), quindi non c'è nessuna perdita nuova rispetto a HEAD.
   - `<svg><title/></svg>VIS` e `<svg><desc><textarea/></svg>T</textarea>VIS` danno lo stesso risultato di HEAD.
   - Esito: ok.
2. `modules/web/leggi.py:625` — nel ripiego, i grezzi autochiusi sono vuoti solo in XHTML, per i tag non nascosti dentro svg/math e per plaintext. Altrimenti si salta con `_chiusura` (modules/web/leggi.py:627). I contati sono tornati come in HEAD.
   - Rischio esaminato: che parser e ripiego divergano sul titolo autochiuso dentro noscript, svg o template.
   - `nome == "title" and not titolo` corrisponde al ramo `else` del parser.
   - Esito: ok.
3. `tests/test_unit_web_leggi.py:941` — 6 sonde nei punti di integrazione, su parser e ripiego. `tests/test_unit_web_leggi.py:925` (svg+textarea) prende la mutazione «parser senza esenzione».
   - Rischio esaminato: test che non distinguono il codice giusto da quello sbagliato.
   - Mutazioni fatte in una copia del repo:
     - parser con esenzione per tutti i tag: 6 FAIL;
     - ripiego con esenzione per tutti: 5 FAIL. Il caso noscript non fallisce, ed è giusto così: noscript è contato, non grezzo;
     - parser senza esenzione: 1 FAIL;
     - ripiego senza esenzione: 1 FAIL.
   - Esito: ok.
4. Contesto: `modules/web/leggi.py:126` — `_GREZZI_AUTOCHIUSI` non cambia rispetto alla #454. Esito: ok.

**Verifiche fatte**
- 190 passed su Python 3.13.16 e su 3.11.17 (venv in scratchpad).
- Il fuzz454 (oracolo html5lib), contro una copia di HEAD rinfrescata:
  - seme 455, 40k casi (3.13): 0 fughe del ripiego, 0 casi «nuovo>HEAD» nascosti ai browser (438 sono «nuovo>HEAD» visibili per i browser);
  - seme 4551, 20k casi (3.11): 0 / 0.
- Nota: la copia «head» che avevo in scratchpad era ferma a una review precedente e non corrispondeva più a HEAD. L'ho rigenerata con `git show HEAD:modules/web/leggi.py` prima dei confronti.
- Wall of Shame: il diff non tocca la history né i tool del kernel e non simula output. Il cap di 10 iterazioni e `_get_window` non sono toccati. Nessuna eccezione nuova che possa propagarsi: il `TypeError` di `set_cdata_mode` è intercettato.

**Riserve**
- R-454-1 è chiusa e R-454-2 (doppio escape `<script><!--<script>`, BASSA, preesistente) resta aperta. Oggi in reports/stato_progetto.md non c'è nessuna voce R-454: vanno scritte entrambe a fine task.
- Restano aperte, fuori dalla fetta: R-453-2 (PI e DOCTYPE in XHTML), R-450-1 e V-2 ve #243 (`<title/>` nei punti di integrazione), R-447-1(b), V-2 ve #242.

**Rischi esclusi**
- La resa reale dei browser sul contenuto di foreignObject non è verificata. L'oracolo tratta come nascosto tutto il contenuto foreign, mentre i browser mostrano il testo di foreignObject. Quindi le «perdite» nel verso sicuro dentro foreignObject sono sottostimate, ma non toccano il verso fuga.
- Il comportamento su VPS e con pagine reali non è verificato, perché questa review non usa la rete.

Memoria aggiornata con la riga #455 e una lezione: controllare che la copia di HEAD sia davvero HEAD prima dei confronti. Il commit è ec14e89, fatto con scripts/commit_memoria_revisore.sh; l'index del diff sotto review è intatto.

File rilevanti:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /home/user/Gas/.claude/agents/memoria_revisore.md
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r455/oracolo.py

---

### Review #456 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #456 (chat Mani), 2026-10-22. Riguarda la PR #244, fetta 7 di Mani, ramo feat/mani-web-fetta7. Ho rivisto il diff staged sopra l'head 51f7986: modules/web/leggi.py +2 e tests/test_unit_web_leggi.py +5/-2. Prima della review ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md (voce fetta 7) e .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- modules/web/leggi.py:88 — aggiunge «noembed» e «noframes» a `_TAG_NASCOSTI`. Questo li mette anche in `_Estrattore._SALTA`, in `_TITOLO_VUOTO_IN` e nell'esenzione svg/math. Rischio esaminato: un'interazione con i contatori (`_aperti`/`_salta`) e con il testo grezzo aperto da `<noembed/>`. Ora `handle_starttag` conta l'apertura e `</noembed>` la scala, quindi niente squilibri. Su 3.13.16 e 3.11.17 html.parser ha già noembed/noframes in `CDATA_CONTENT_ELEMENTS`, quindi il contenuto è grezzo come nei browser. Esito: ok.
- modules/web/leggi.py:125 — `_CONTATI_RIPIEGO = _TAG_NASCOSTI - _GREZZI_RIPIEGO` resta invariato, perché noembed/noframes erano già in `_GREZZI_RIPIEGO`. Rischio esaminato: il ripiego potrebbe contarli due volte, come contenitore e come grezzo. Non succede. Esito: ok.
- modules/web/leggi.py:477 (parser) e modules/web/leggi.py:627 (ripiego) — l'esenzione «dentro svg/math l'autochiusura vale» ora esclude anche noembed/noframes. Rischio esaminato: una regressione nei punti di integrazione HTML, la classe di R-454-1. Con l'oracolo html5lib 1.1, confrontato con una copia di HEAD rigenerata e controllata con diff, la modifica chiude tre fughe che c'erano già a HEAD:
  - `<svg><foreignObject><noembed/></svg>SEGRETO</noembed>VIS`
  - `<math><mi><noframes/></math>SEGRETO</noframes>VIS`
  - `<template><noembed/></template>SEGRETO</noembed>VIS`

  Prima SEGRETO arrivava al modello sia nel parser sia nel ripiego; ora non arriva più. Esito: ok, con la riserva R-456-1.
- tests/test_unit_web_leggi.py:908 e tests/test_unit_web_leggi.py:909 — i due casi nuovi del parametrize controllano sia `_componi` (parser) sia `_testo_senza_parser` (ripiego). Rischio esaminato: test che non mordono. La mutazione «senza noembed» in `_TAG_NASCOSTI`, provata su una copia, fa fallire 2 test. Esito: ok.
- tests/test_unit_web_leggi.py:914 — la docstring dichiara che il caso noscript nasconde più dei browser (V-2 bot #244). Esito: ok.

**Verifiche fatte**
- 192 passed su 3.13.16 e su 3.11.17 (venv nello scratchpad).
- Oracolo html5lib su 11 sonde, tra cui:
  - `<noembed><title/></noembed>VIS`: ora il parser non mostra più `<title/>` come testo.
  - `<noembed><!--</noembed>-->VIS`: coerente con i browser.
  - Nessun caso dove la versione nuova mostra qualcosa che HEAD nascondeva.
- Nota di processo: il fuzz454 citato nella richiesta NON ha noembed/noframes fra gli atomi (r454/fuzz454.py, lista `nomi`), quindi il suo «0 su 30000» non esercitava questa modifica. L'ho rifatto aggiungendo noembed e noframes, più un controllo assoluto sui casi che li contengono:
  - seme 4560, 30k casi su 3.13: 0 fughe nel ripiego, 0 casi «nuovo>HEAD», 0 casi in cui la versione nuova mostra testo che HEAD nascondeva;
  - seme 4561, 10k casi su 3.11: stesso esito.

**Riserve (da tracciare in reports/stato_progetto.md)**
- R-456-1 (chat Mani), BASSA, perdita nel verso sicuro: `<svg><noembed/></svg>VIS` ora nasconde tutto il resto della pagina fino a un `</noembed>`, nel parser e nel ripiego. Per i browser, dentro svg `<noembed/>` è un elemento estraneo vuoto e VIS si vede; HEAD lo mostrava. È la stessa classe, già accettata, di `<svg><script/></svg>VIS`. Non è una fuga: nella pagina reale perdi del contenuto, non lo esponi.
- R-456-2 (chat Mani), COSMETICA: il commento di modules/web/leggi.py:130 (righe 130-132, sopra `_TITOLO_VUOTO_IN`) elenca «script, style, iframe e noscript» ma non noembed/noframes, che ora fanno parte dell'insieme.
- Restano aperte, come prima: R-454-2, R-453-2, R-450-1, R-447-1(b), V-2 ve #242/#243.

**Cosa NON ho verificato**
- Il comportamento di html.parser vecchi senza le patch recenti, dove noembed/noframes non sono in `CDATA_CONTENT_ELEMENTS`. Non ho un interprete così nell'ambiente. Ragionando sul codice, lì il contenuto si legge come tag ma resta dentro il contatore `_salta`, quindi l'errore va nel verso di nascondere di più. È un ragionamento, non una prova.
- Il comportamento nei browser reali con gli script attivi (noscript grezzo): l'oracolo html5lib non ha il flag scripting.

**Wall of Shame**: niente. Il diff non tocca la history né `_get_window`, non simula tool, non tocca provider né il cap delle 10 iterazioni.

**Memoria**: ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga «#456 (chat Mani) — 2026-10-22 — APPROVATO CON RISERVE — …» e una lezione nuova: prima di citare un fuzz riusato come prova, controllare che i suoi atomi contengano i tag toccati dal diff. È committata con scripts/commit_memoria_revisore.sh (commit 85b2ac2). Il diff staged del motore resta intatto nell'index.

File utili nello scratchpad:
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r456/fuzz456.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r456/oracolo.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r456/head/modules/web/leggi.py (copia di HEAD)

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 174 → 192 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «192 passed in 21.57s» su Python 3.13; «192 passed in 21.97s» su 3.11 (venv); «192 passed in 21.31s» con rete e DNS veri bloccati via sitecustomize). Primo giro (`54706c2`) 174 → 190, secondo (`6f9bfe7`) 190 → 192.
- Fuzz differenziale ripiego contro parser: 0 fughe su 200k pagine HTML (3.13), 100k (3.11, escluse `<!-->`), 100k XHTML (3.13). Fuzz con oracolo html5lib (`fuzz454.py` del revisore): «fughe ripiego 0, nuovo>HEAD 326 di cui nascosti per html5lib 0 su 30000».
- Mutazioni in copie isolate, tutte prese: senza `_modo_grezzo`, senza ripiego TypeError, esenzione svg/math per tutti o per nessuno (parser e ripiego), ripiego che ignora i grezzi autochiusi, contati del ripiego con esenzione, `_componi` senza XML, CDATA senza escape, commenti tenuti, cache disattivata (quadratico), ripiego senza xhtml, commento/CDATA senza fine tenuto.
- Secondo giro: fuzz HTML 0 fughe (200k 3.13, 100k 3.11); fuzz454 con oracolo html5lib contro HEAD 51f7986 «nuovo>HEAD 0 di cui nascosti 0 su 30000» (gli atomi non contenevano noembed: il revisore l'ha rifatto con noembed/noframes, 0/0 su 30k + 10k); mutazioni senza noembed / senza noframes prese.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

`gh` non autenticato nella sessione cloud: esiti letti dai check della PR #244 via MCP GitHub. Mappatura commit→run:
- `7f28b4c`, `a75a310`, `ec14e89`, `54706c2`: pushati insieme prima di aprire la PR; run di push sulla testa `54706c2` non letta (handoff-check atteso rosso: handoff non ancora aggiornato).
- `51f7986` (fine-task del primo giro): run 39772940360 success (unit-suite «190 passed» della web suite su 3.11.17, letto dal bot), handoff-check success; verifica-bot success.
- `85b2ac2`, `6f9bfe7`: nessuna run su questi SHA da soli (pushati col commit di fine-task che contiene questo file).
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: **R-456-1 (chat Mani)** BASSA verso sicuro: `<svg><noembed/></svg>VIS` nasconde il resto della pagina; **R-456-2 (chat Mani)** COSMETICA commento di `_TITOLO_VUOTO_IN`; **R-454-2 (chat Mani)** BASSA preesistente: doppio escape negli script (`<script><!--<script></script>X`); **R-453-2 (chat Mani)** BASSA preesistente: PI e DOCTYPE interno in XHTML.
- Restano: R-450-1 e V-2 ve #243, R-447-1(b), V-2 ve #242, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…7».
