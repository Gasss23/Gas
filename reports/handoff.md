# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — Chat Mani, fetta 4: note delle PR #238 e #239 (R6, PR #239)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #239 (https://github.com/Gasss23/Gas/pull/239): l'operatore ha scritto «a, correggi e mergia quando il bot approva»; l'agente mergia quando `verifica-bot` è success sull'head (niente ALTA/MEDIA), CI verde, nessun conflitto.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

(`gh` non autenticato nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Nome del tag intero (V-1 bot #238, R-431-1)**: `FATTA`
- **Ripiego alla pari col parser (V-2 ve #238)**: `FATTA` (annidamento non contato, dichiarato)
- **`embed` fuori dai tag con contenuto (R-431-2)**: `FATTA`
- **Test mancanti (V-1/V-4 ve #238, V-2/V-3 bot #238)**: `FATTA`
- **Note bot e verifica esterna #239 (fine del tag fuori dalle virgolette, titolo, «/» dopo il nome, tag senza fine, math/object, commenti vuoti e «--!>», «<» negli attributi)**: `FATTA`
- **R-439-1, R-440-1, R-441-1 (fine del tag come il tokenizzatore HTML), R-439-2, R-439-3**: `FATTA`
- **R-442-1, R-442-2 (contenuto dei blocchi nascosti non grezzi, commenti fasulli `<!`/`<?`/CDATA nel ripiego)**: `DEFERITA — famiglia diversa (contenuto dei blocchi, non il tag di apertura), richiede un contatore come il parser: fetta successiva; BASSE, il ripiego non si attiva con pagine vere`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  12 ++++++++
 modules/web/leggi.py               | 107 ++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------
 reports/diff_sessione.md           |  14 ++++-----
 reports/handoff.md                 | 574 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 ++-
 reports/ultimo_report.md           |  39 ++++++++++++++++---------
 tests/test_unit_web_leggi.py       | 109 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 7 files changed, 591 insertions(+), 268 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
33be621 Merge origin/main in feat/mani-web-fetta4
4f9ff13 docs(fine-task): report, stato e handoff — chat Mani fetta 4, secondo giro (#239)
3e0fe70 fix(web): fetta 4 chat Mani — fine del tag come il tokenizzatore HTML (R-439-1, R-440-1, R-441-1)
e72a96a chore(revisore): memoria review #442 — APPROVATO CON RISERVE
f7a3a05 chore(revisore): memoria review #441 — APPROVATO CON RISERVE
c43a59e chore(revisore): memoria review #440 — APPROVATO CON RISERVE
71bd77e docs(fine-task): report, stato e handoff — chat Mani fetta 4 (#239)
befc78e Merge origin/main in feat/mani-web-fetta4
12f7f71 fix(web): fetta 4 chat Mani — ripiego alla pari col parser, nomi dei tag interi, embed
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit, quindi le righe di `reports/handoff.md` possono differire di poco (l'elenco dei file è esatto). I commit di main portati dai merge non sono della sessione; il merge `33be621` porta la PR #240 (chat Motore).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Otto verdetti, incollati integralmente: #431 (chat Mani), #432 (chat Mani), #438 (chat Mani, merge di main) per `12f7f71`/`befc78e`; #439, #440, #441, #442 (chat Mani) per `3e0fe70` (i giri #439-#441 hanno chiuso le proprie riserve nello stesso diff, il commit porta il diff approvato dalla #442; le righe di memoria sono nei commit `c43a59e`, `f7a3a05`, `e72a96a` fatti dal revisore); #444 (chat Mani) per il merge di main `33be621` (PR #240 della chat Motore).

### Review #431 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #431 (chat Mani). Diff staged su feat/mani-web-fetta4: `modules/web/leggi.py` e `tests/test_unit_web_leggi.py`. Prima della review ho letto CLAUDE.md (sezioni 5, 8 e 9), le voci «Mani — fetta 1/2/3» di `reports/stato_progetto.md` e le lezioni della memoria (#409, #410, #429, #430). Nel diff non ci sono slicing della history né output dei tool simulati. Il cap di 10 iterazioni e `_get_window` non vengono toccati.

**Elementi del diff esaminati**
- `modules/web/leggi.py:87` — `_INIZIO_TAG` prende il nome intero. Rischio esaminato: che la regex torni costosa. Esito: ok. Dopo la ripetizione non c'è nulla, quindi non può tornare indietro a riprovare. Misure su 2 MB: nome lungo 2 MB 0,02 s; «<a»×N 0,31 s; «<!-»×N 0,05 s; «</»×N 0,07 s.
- `modules/web/leggi.py:460` — `_chiusura`. Rischio esaminato: tempo quadratico con chiusure finte. Esito: ok. Ogni `find` va solo avanti e la ricerca di «>» avviene una volta per blocco. Misure su 2 MB: blocchi con 5 «</scriptx» finti 0,08 s; «</scriptx» ripetuto in un solo blocco 0,07 s; «</script» senza «>» 0,10 s; «<script></script\t» senza «>» 0,15 s.
- `modules/web/leggi.py:474` — `_togli_blocchi_nascosti`. Rischio esaminato: linearità con commenti e blocchi. Esito: ok. Commenti annidati 0,004 s; commenti non chiusi 0,004 s; «<!---->»×N 0,16 s; «İ»×2M 0,33 s.
- `modules/web/leggi.py:393` — `_SALTA = _TAG_NASCOSTI`. Rischio esaminato: che il percorso normale cambi. Esito: ok. L'insieme è identico a quello di HEAD (riga 385 di HEAD). Diventa un frozenset, e `_SALTA` si usa solo con `in` (`modules/web/leggi.py:408` e `modules/web/leggi.py:416`). `_BLOCCHI_NASCOSTI` non ha più chiamanti.
- `modules/web/leggi.py:494` — l'apertura di un tag nascosto. Esito: riserva R-431-1, sotto.
- `tests/test_unit_web_leggi.py:604` — test del ripiego con SEGRETO_* per tutti i tag e per il commento. Rischio esaminato: mutazioni che sopravvivono. Esito: ok. Ho rifatto io 4 mutazioni in copie isolate: svg tolto dall'insieme, apertura per prefisso, confine della chiusura tolto, commenti ignorati. Ognuna produce 1 FAIL.
- `tests/test_unit_web_leggi.py:625` — unescape che solleva. Esito: ok. Il monkeypatch agisce sul globale `html_unescape` (`modules/web/leggi.py:42`), letto a `modules/web/leggi.py:510` al momento della chiamata.
- `tests/test_unit_web_leggi.py:705` — `_entro` con l'assert sul returncode e lo stderr. Esito: ok. Il timeout dà ancora False e un figlio che si schianta ora mostra il motivo.
- `tests/test_unit_web_leggi.py:750` — attesa dei thread «gas-web-dns» (`modules/web/leggi.py:187`). Esito: ok, con un limite: un join(10) per thread non dà garanzie se il DNS resta appeso oltre 10 s. Mi sembra accettabile.
- Suite web: 106 passed su Python 3.13.16.

**Riserve**
- **R-431-1 (chat Mani), BASSA**: la correzione V-1 bot #238 è solo a metà. In apertura il confronto è ancora per prefisso quando dopo il nome c'è un carattere fuori da `[a-z0-9:-]`. Con «a<script_x>VIS</script_x>DOPO», «<style.x>» e «<script\x00>» il ripiego nasconde tutto il resto della pagina, mentre il parser li mostra (misurato). La direzione è prudente (si perde testo, non esce contenuto nascosto). Correzione: a `modules/web/leggi.py:494` richiedere che dopo `m.end()` venga un carattere di `_FINE_NOME` o la fine del testo, come già fa la chiusura, e aggiungere un test con «<script_x>».
- **R-431-2 (chat Mani), BASSA, preesistente dalla fetta 1, ora anche nel ripiego**: `embed` è un elemento vuoto, senza chiusura. Con «a<embed src=x>VIS_DOPO_EMBED» sia il parser (percorso normale) sia il ripiego restituiscono solo «a»: il contatore `_salta` non torna mai a zero. Correzione: togliere embed dall'insieme dei tag con contenuto (o trattarlo come elemento vuoto) e aggiungere un test.
- **R-431-3 (chat Mani), COSMETICA**:
  - il ripiego non gestisce l'annidamento: «<svg><svg></svg>SEGRETO</svg>VIS» mostra SEGRETO, il parser no. La frase «alla pari col parser» vale per l'insieme dei tag e per i commenti, non per la profondità;
  - nessun test vede gli attributi della chiusura: la mutazione `return ... dopo` al posto di `g + 1` a `modules/web/leggi.py:471` resta verde.

**Verifica da avversario: differenze rispetto a html.parser**
- `<script>` dentro un commento: uguale al parser.
- `</script` dentro una stringa JS: chiude alla prima occorrenza come il parser e il browser. È parità, non una fuga.
- CDATA: il ripiego lascia frammenti come «<![CDATA[ x». Viene da `<[^<>]*>` ed era già così prima; è una fuga di markup, non di contenuto di script.
- `<!-->`, `--!>`, «<!--» dentro un attributo, `<svg/>`: il ripiego nasconde più del parser. Direzione prudente.

**Rischi esclusi**
- Python 3.11 non verificato da me (qui c'è solo 3.13); mi baso sul vostro «106 passed su 3.11».
- Comportamento con pagine reali e rete vera non verificato: le sonde sono solo su stringhe sintetiche.
- Margine CI dei test a tempo non rimisurato su un runner lento (carichi locali ≤0,34 s contro 10 s).

**Memoria**: aggiunta la riga «#431 (chat Mani) — 2026-10-21 — APPROVATO CON RISERVE — …», con una lezione, in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. Il file è modificato ma non in staging. Non ho committato e non ho lanciato `scripts/commit_memoria_revisore.sh`, come mi hai chiesto: il commit spetta a te.

File di sonda (fuori dal repo):
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/sonde.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/parita.py

### Review #432 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Ri-review #432 (chat Mani). Diff STAGED su feat/mani-web-fetta4: modules/web/leggi.py, tests/test_unit_web_leggi.py e la riga #431 in memoria. Ho letto prima CLAUDE.md, reports/stato_progetto.md (sezioni Mani) e .claude/agents/memoria_revisore.md. Il diff non tocca la history, i tool, `_get_window`, i tetti né i provider.

Elementi esaminati:
- `modules/web/leggi.py:497` — l'apertura di un tag nascosto vale solo se dopo il nome viene un carattere di `_FINE_NOME` oppure la fine del testo. Rischio esaminato: lettura oltre la fine del testo. L'`or` si ferma prima di leggere `basso[m.end()]` quando `m.end() >= len(basso)`. L'ho provato con «a<script», «a<svg», «x<!--» e con 200.000 stringhe casuali fatte di pezzi come «<», «</», script, embed, «!--», «İ», \x00: nessuna eccezione. «<script_x>», «<SCRIPT_X>», «<scriptx>» e «<script\x00>» restano visibili, come fa html.parser. Esito: ok, R-431-1 chiusa.
- `modules/web/leggi.py:84` — «embed» tolto da `_TAG_NASCOSTI`. Rischio esaminato: che esca contenuto nascosto. embed è un elemento vuoto e non ha testo suo. In «a<embed src=x>B</embed>C» sia il parser sia il ripiego mostrano B, come i browser. `src` è un attributo e non diventa mai testo. In «<object><embed>FALLBACK</object>» il fallback resta nascosto da object. Esito: ok, R-431-2 chiusa.
- `modules/web/leggi.py:395` — `_SALTA = _TAG_NASCOSTI`. Rischio esaminato: altri cambi nel percorso normale. Rispetto a HEAD cambia solo il tipo (da set a frozenset) e manca embed. Nessuno modifica `_SALTA`: a `modules/web/leggi.py:410` e `modules/web/leggi.py:418` c'è solo il test `in`. Esito: ok.
- `modules/web/leggi.py:470` — `_chiusura` riconosce la chiusura solo col nome intero e finisce al suo «>». Stesso rischio dell'indice, stessa protezione. Esito: ok.
- `tests/test_unit_web_leggi.py:832` — il test su embed controlla tutti e due i percorsi (parser e ripiego). Esito: ok.
- `tests/test_unit_web_leggi.py:626` — la chiusura con attributi `</script data-x=1>`. Esito: ok, R-431-3 chiusa (la docstring dichiara anche che il ripiego non conta l'annidamento).

Mutazioni rifatte da me su una copia presa dall'index (poi cancellata). Ognuna fa fallire 1 test:
- apertura per prefisso;
- embed rimesso nell'insieme;
- `return dopo`;
- confine della chiusura tolto;
- commenti ignorati;
- svg tolto.

Test: 107 passed su 3.13 e 107 passed su 3.11 (via uv).

Tempi: 2 MB di «<script», «<script_», «<embed>», «</script», «<style.x>» o «<script x» stanno sotto 0,20 s ciascuno.

Riserve:
- R-432-1 (chat Mani), COSMETICA: la mutazione che toglie il caso «fine del testo» dall'apertura (`m.end() < len and …`) passa lo stesso, 107/0. Effetto: «<script» in fondo alla pagina resterebbe come testo letterale. Basta un assert sul ripiego di «a<script».
- Nota, non è una riserva: con «<script/>B</script>» il ripiego nasconde B, mentre il parser lo mostra (preesistente). I browser lo nascondono, quindi il ripiego sbaglia nella direzione sicura.

Rischio escluso: non ho confrontato tutto il ripiego con html.parser su HTML reale preso dalla rete (sandbox senza siti veri). Ho verificato solo i casi sintetici sopra e il fuzz.

Memoria: ho aggiunto la riga «#432 (chat Mani) — 2026-10-21 — APPROVATO CON RISERVE — …» in fondo a /home/user/Gas/.claude/agents/memoria_revisore.md. Non è in staging (stato `MM`) e, come mi hai chiesto, non ho committato né lanciato `scripts/commit_memoria_revisore.sh`: se vuoi includerla, fai tu `git add`. Nessuna lezione nuova.

File: /home/user/Gas/modules/web/leggi.py, /home/user/Gas/tests/test_unit_web_leggi.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #438 (chat Mani)

## VERDETTO: APPROVATO

Review #438 (chat Mani). Ho controllato il merge in corso di origin/main (dec4ce9, uguale a MERGE_HEAD) nel ramo feat/mani-web-fetta4 (HEAD 12f7f71, merge-base eb8e246). Prima ho letto CLAUDE.md (sezione 5), l'inizio di reports/stato_progetto.md e la parte finale della memoria.

**Punto 1, perimetro.** `git diff --cached origin/main` tocca solo 3 file: modules/web/leggi.py, tests/test_unit_web_leggi.py e .claude/agents/memoria_revisore.md (+2 righe).
- Il diff dei due file web contro origin/main è identico byte per byte a `git diff eb8e246 HEAD` sugli stessi file.
- I blob nell'index coincidono con quelli di HEAD.
- Main non tocca quei file dalla merge-base.
- gas.py, modules/telegram/bot.py e tests/test_unit_kernel.py nell'index sono uguali a origin/main (si vedono nello stato solo perché arrivano dal merge).
- Albero di lavoro pulito, nessun file non tracciato.

**Punto 2, memoria.**
- Versione staged: 697 righe, cioè le 695 di main più le 2 righe #431/#432 (chat Mani). Stanno alle righe 695 e 696, subito prima di #437 (chat Motore).
- Nessuna riga di HEAD o di main va persa.
- Nessun duplicato, nessuna riga inventata, nessun marcatore `<<<<<<<`, `=======` o `>>>>>>>`.

**Punto 3, chiamanti.** git grep su `leggi_pagina`, `modules.web` e `modules/web` (esclusi modules/web, il suo test, reports/ e la memoria) trova solo un commento in .github/workflows/ci.yml:114. Nessun uso in gas.py né negli altri moduli: l'aggancio non è ancora fatto.

Citazioni:
- modules/web/leggi.py:497 — apertura del tag confrontata col nome intero (_FINE_NOME o fine del testo). Rischio: il merge perde o altera la correzione R-431-1. Ok: il blob nell'index è uguale a HEAD 12f7f71.
- modules/web/leggi.py:84 — `_TAG_NASCOSTI` senza «embed», usato in modules/web/leggi.py:395 come `_SALTA`. Rischio: main reintroduce o cambia l'insieme. Ok: main non tocca il file dalla eb8e246.
- tests/test_unit_web_leggi.py:832 — test «embed non nasconde il resto della pagina». Rischio: un test della fetta 4 perso nel merge. Ok: è presente e passa (web 107 passed).
- tests/test_unit_web_leggi.py:626 — controllo sugli attributi della chiusura (R-431-3). Rischio: lo stesso. Ok.
- .claude/agents/memoria_revisore.md:695-696 — le righe #431/#432 (chat Mani) messe a mano. Rischio: righe perse, duplicate o marcatori rimasti. Ok, verificato con diff e comm contro HEAD e main.
- .github/workflows/ci.yml:114 (contesto) — unico riferimento a modules/web fuori dal modulo, ed è un commento. Ok.

Suite sull'albero fuso (Python 3.13):
- web: 107 passed;
- gate + notte: 947 passed;
- kernel: 987 PASS e 1 FAIL. Il FAIL è T31g e dipende dall'ambiente: `import sqlite_vec` dà ModuleNotFoundError. gas.py e il test kernel sono identici a origin/main, quindi non viene da questo merge (stesso esito già registrato nella #428 chat Mani);
- `pytest --co tests`: 1818 test raccolti, senza errori.

Wall of Shame: il merge non porta codice nuovo del motore, quindi nessuno slicing della history e nessuna simulazione di tool introdotti.

**Rischio escluso.** Non ho rifatto in modo indipendente la review del contenuto dei 27 commit della chat Motore (gas.py e il resto), già revisionati e mergiati su main. Mi sono limitato a verificare che nell'index siano uguali a origin/main. Non ho verificato T31g con sqlite_vec installato: qui il pacchetto non c'è.

**Memoria.** Ho aggiunto la riga «#438 (chat Mani) — 2026-10-21 — APPROVATO — …» in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, ora riga 698. La modifica non è nell'index né committata, come chiesto; commit_memoria_revisore.sh non l'ho lanciato. Prima del commit di merge va aggiunta all'index con git add; dopo il git add il marcatore va rigenerato con `bash scripts/segna_review_ok.sh`.

Nota: il mio primo tentativo di scrivere la riga con un heredoc in Bash è stato bloccato dall'hook review_gate.sh. Il testo conteneva parole come «commit» e «--cached» e l'hook l'ha preso per un comando git di scrittura (il marcatore non corrisponde ancora al diff staged). L'ho scritta con lo strumento Edit. Il gate ha bloccato, quindi ha funzionato; è un falso positivo del filtro che riconosce i comandi, non un buco.

---

---

### Review #439 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #439 (chat Mani). Riguarda il diff staged del ramo feat/mani-web-fetta4 (PR #239), che chiude le note di bot e verifica esterna #239 nel ripiego senza parser di `modules/web/leggi.py`.

Ho letto prima CLAUDE.md (sez. 1, 4, 5, 8, 9, 10), `reports/stato_progetto.md` (le sezioni Mani, :605 e seguenti) e la mia memoria (lezioni sulle regex e sul ripiego, #429–#438).

**Elementi del diff esaminati**
- `modules/web/leggi.py:94` — `_FINE_TAG`, il «>» fuori dalle virgolette. Rischio ReDoS: ok. Le tre alternative partono da caratteri diversi e nessuna ripetizione è annidata. Misure su 2 MB, tutte entro 0,42 s:
  - apici alterni `"'`×1M seguiti da «>»;
  - `<title "` + «"»×2M + «>»;
  - `<a "x>`×N;
  - `<a b="c" d='e' f=g>`×N;
  - script con `</script>` nell'attributo ×N;
  - `<a "`×N senza «>» (in questo caso il `find(">")` alla `modules/web/leggi.py:526` evita la regex).
- `modules/web/leggi.py:94` — completezza della chiusura di V-1 ve #239: **riserva R-439-1**, vedi sotto.
- `modules/web/leggi.py:482` — `_fine_commento` con la cache `prossimi`. Rischi: ordine «-->»/«--!>», reset, posizioni vecchie. Esito ok:
  - fuzz differenziale contro una versione senza cache, 300k pagine casuali (commenti, «-->», «--!>», «<!-->», «<!--->», script, virgolette): uscite identiche;
  - una posizione salvata è usata solo se ≥ da, quindi è davvero la prossima; «-1» non viene mai ricercato; i tratti cercati sono disgiunti, quindi la ricerca resta lineare.
- `modules/web/leggi.py:497` — `min(fini)`. Rischio: mutazione non presa da nessun test. Esito: riserva R-439-2.
- `modules/web/leggi.py:529` e `modules/web/leggi.py:96` — `title` aggiunto solo nel ripiego, col confine del nome sempre in apertura. Ok: `<title a="</title>">SEGRETO</title>VIS` → il ripiego dà « VIS»; il parser mette SEGRETO nel campo Titolo, non nel testo.
- `modules/web/leggi.py:401` (contesto) — `_SALTA = _TAG_NASCOSTI` è invariato. Il diff non tocca `_Estrattore` né `_TAG_NASCOSTI`, quindi il percorso normale non cambia: ok.
- `tests/test_unit_web_leggi.py:859` — test parametrico su attributi e commenti. Ok, però manca il caso della virgoletta in posizione non di valore (R-439-1).
- `tests/test_unit_web_leggi.py:869` — test a tempo in sottoprocesso con `_entro` (`tests/test_unit_web_leggi.py:710`). Ok.
- `tests/test_unit_web_leggi.py:841` — math e object sul percorso del parser. Ok. È tolta anche la fixture `rete` inutile dal test su embed.
- `modules/web/leggi.py:563` (contesto, `_componi`) — il ripiego parte solo su ValueError di html.parser. Su 200k pagine casuali di metacaratteri e sui casi noti (`<![foo[`, DOCTYPE con sottoinsieme interno, «&#» con migliaia di cifre) il ripiego non è mai partito e non è uscita nessuna eccezione. Per questo le riserve restano BASSE.

Test: 121 passed su 3.13 e 121 passed su 3.11 (uv), con index uguale al working tree.

**Riserve**
- **R-439-1 (chat Mani) BASSA — V-1 ve #239 è chiusa solo in parte.** `_FINE_TAG` (`modules/web/leggi.py:94`) accoppia tutte le virgolette, ma in HTML5 (e in html.parser) una virgoletta apre un valore solo dopo «=».
  - Una virgoletta nel nome di un attributo, o dentro un valore senza virgolette, apre un finto valore. Questo si chiude sull'apertura del valore vero, quindi il tag finisce prima del dovuto. A quel punto il `</script>` dentro il valore vero chiude il blocco.
  - Sonde (il parser mostra «VIS», il ripiego mostra SEGRETO):
    - `<script x"y z="w></script>">SEGRETO</script>VIS` → « ">SEGRETO VIS»
    - `<script x'y z='w></script>'>SEGRETO</script>VIS` → stesso esito con l'apice singolo
    - `<script a=b"c d="e></script>">SEGRETO</script>VIS` → stesso esito
    - `<iframe a=b"c d="e></iframe>">SEGRETO</iframe>VIS` → stesso esito
    - `<a x"y z="w>ATTR_SEGRETO">VIS` → il valore dell'attributo esce nel testo
  - Correzione che ho provato in una copia isolata (`git checkout-index`, la tua copia di lavoro non è toccata):
    ```
    _FINE_TAG = re.compile(r"""(?:[^>=]|=[ \t\n\r\f]*+(?:"[^"]*"|'[^']*'|(?!["'])))*+>""")
    ```
    Risultato: 121 passed, tutte le sonde danno « VIS», tempi sui 2 MB uguali o migliori (≤0,32 s). Anche un valore fra virgolette mai chiuso (`<script a="></script>SEGRETO`) porta via il resto, come nel browser. I quantificatori possessivi richiedono Python 3.11+, che è il minimo del progetto e la versione della CI (.github/workflows/ci.yml:44).
  - Consiglio di farla in questa PR, con un test sulla prima sonda: è lo stesso finding che la PR dichiara chiuso.
- **R-439-2 (chat Mani) COSMETICA:** la mutazione `min(fini)` → `max(fini)` alla `modules/web/leggi.py:497` sopravvive (121/0). Nessun test ha «-->» e «--!>» nella stessa pagina. Test suggerito: `a<!--x-->VIS<!--y--!>b`.
- **R-439-3 (chat Mani) COSMETICA:**
  - la chiusura (`modules/web/leggi.py:477`) non guarda le virgolette: `<script>SEGRETO</script x=">">VIS` → «">VIS». Restano pezzi di markup, ma non esce contenuto nascosto;
  - `prossimi: dict` (`modules/web/leggi.py:482`, `modules/web/leggi.py:512`) andrebbe tipizzato `dict[str, int]` (CLAUDE.md sez. 4).

**Cose che NON ho verificato o che ho escluso**
- Il caso del doppio escape dentro script (`<script><!--<script>…</script>STILL--></script>`), che il browser nasconde: «STILL» esce sia dal parser sia dal ripiego. È un limite di html.parser già presente prima del diff e fuori da questa fetta.
- Il CDATA (`<![CDATA[`) e i commenti finti (`<?…>`): il ripiego tutt'al più nasconde di più, cioè va nella direzione sicura.
- Il backtick non è una virgoletta per HTML5, quindi il comportamento è coerente col parser (`<a href=\`x>\`>VIS` → entrambi danno «`>VIS»).
- Non ho controllato un parser con versioni di html.parser diverse da 3.11 e 3.13. Non ho controllato il comportamento dei browser veri: ho confrontato solo con le regole HTML5 e con html.parser 3.13.

**Memoria**
- Ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga «#439 (chat Mani) — 2026-10-21 — APPROVATO CON RISERVE — …» e una lezione: le virgolette aprono un valore solo dopo «=», quindi va sempre sondato `<script x"y z="w></script>">SEGRETO`.
- Su tua richiesta non ho committato e non ho eseguito `scripts/commit_memoria_revisore.sh`: il file risulta modificato e non in staging.

Le sonde stanno in `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/` (sonda1.py, sonda2.py, tempi.py, diff_cache.py). Le copie isolate sono `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/copia` (mutazione min→max) e `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/copia2` (correzione proposta).

---

### Review #440 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #440 (chat Mani), 2026-10-21, ramo feat/mani-web-fetta4 (PR #239), diff staged. Ho letto CLAUDE.md (sez. 5, 8, 9, 10), le parti utili di reports/stato_progetto.md e la memoria del revisore.

**Elementi del diff esaminati**
- `modules/web/leggi.py:96` — `_FINE_TAG` con la regex proposta nella #439 (le virgolette aprono un valore solo dopo «=», ripetizioni possessive). Rischio esaminato: le sonde della R-439-1 e la linearità. Esito: **ok** per le sonde dichiarate. `<script x"y z="w></script>">SEGRETO</script>VIS` dà «VIS» sia nel ripiego sia nel parser. Ho provato 11 input avversari da 2 MB, col «>» finale perché altrimenti il `find` a `modules/web/leggi.py:528` li scarta prima della regex: tutti sotto 0,23 s. Con la mutazione «apici singoli tolti» falliscono 2 test.
- `modules/web/leggi.py:499` — `min(fini)` tra «-->» e «--!>». Rischio esaminato: la mutazione min→max, che nella #439 sopravviveva. Esito: **ok**, ora `tests/test_unit_web_leggi.py:869` fallisce (R-439-2 chiusa).
- `modules/web/leggi.py:484` e `modules/web/leggi.py:514` — `prossimi: dict[str, int]`. Esito: **ok** (R-439-3 chiusa; la parte sulle virgolette nella chiusura resta una differenza dichiarata, che non fa uscire contenuto nascosto).
- `tests/test_unit_web_leggi.py:858`, `tests/test_unit_web_leggi.py:879`, `tests/test_unit_web_leggi.py:882` — le nuove sonde: valore mai chiuso e linearità in sottoprocesso con 3 casi in più. Esito: **ok**. Con Python 3.13 risultano 127 passed.
- `modules/web/leggi.py:96` — **riserva R-440-1 (chat Mani), BASSA**: resta un caso della stessa famiglia. La regex tratta OGNI «=» come inizio di un valore. Per HTML5 (e per html.parser di Python 3.13) invece un «=» è un carattere normale in questi casi: dentro un valore senza virgolette, subito dopo un valore fra virgolette, all'inizio di un nome, oppure ripetuto. In quei casi il tag del ripiego finisce DOPO quello vero e si mangia l'apertura dello script. Sonde verificate sullo staged (il ripiego mostra «SEGRETO VIS», il parser solo «VIS»):
  `<a b=="x><script>">SEGRETO</script>VIS`
  `<a b=c="x><script>">SEGRETO</script>VIS`
  `<a ="x><script>">SEGRETO</script>VIS`
  `<a b="1"="x><script>">SEGRETO</script>VIS`
  `<a b = = "x><script>">SEGRETO</script>VIS`
  Correzione provata in una copia isolata, poi cancellata:
  `_FINE_TAG = re.compile(r"""(?:[ \t\n\r\f/]|[^ \t\n\r\f/>][^ \t\n\r\f/>=]*+(?:[ \t\n\r\f]*+=[ \t\n\r\f]*+(?:"[^"]*+"?|'[^']*+'?|[^ \t\n\r\f>]*+))?)*+>""")`
  Funziona così: prima viene il nome dell'attributo, poi un «=» conta solo dopo un nome. Un valore senza virgolette si prende anche «=» e virgolette. Una virgoletta mai chiusa arriva fino in fondo, quindi niente match e il resto si perde, come nello standard. Risultato: 127 passed, le 7 sonde danno lo stesso risultato del parser (anche `<script a=b="x></script>">SEGRETO</script>VIS`, dove il parser MOSTRA `">SEGRETO`) e i tempi sui 11 input avversari sono gli stessi (≤0,31 s). Gravità BASSA perché il ripiego si raggiunge solo se html.parser solleva un'eccezione (nella #439 nessuna di 200k pagine casuali ci è arrivata). La fuga però è reale, nello stesso verso della R-439-1.

**Rischi esclusi (non verificati)**
- La suite con Python 3.11 non l'ho rieseguita: qui python3.11 non ha pytest. Mi fido del tuo 127 passed su 3.11 (venv). Le regex possessive compilano su 3.11.
- Le sonde le ho confrontate con html.parser 3.13 e con le regole del tokenizzatore HTML5 lette a memoria, non con un browser vero: in questo ambiente non c'è html5lib né un browser.
- Rete e DNS bloccati (sitecustomize) non li ho riprovati.

Il diff non tocca gas.py, la history, `_get_window`, il tetto di 10 iterazioni né i provider. Nessun Wall of Shame.

**Note per l'agente principale**
- Memoria: ho aggiunto la riga #440 e una lezione in `/home/user/Gas/.claude/agents/memoria_revisore.md` e le ho committate con `scripts/commit_memoria_revisore.sh` (commit c43a59e). Quel commit include anche la tua riga #439, che era staged. Ora lo staged contiene solo `modules/web/leggi.py` e `tests/test_unit_web_leggi.py`, quindi `segna_review_ok.sh` va lanciato sullo staged attuale.
- R-440-1 va tracciata in stato_progetto.md, oppure chiusa con la regex qui sopra, aggiungendo le 5 sonde al parametrize di `test_ripiego_attributi_e_commenti`.

---

### Review #441 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #441 (chat Mani), 2026-10-21. Ramo feat/mani-web-fetta4 (PR #239). Ho esaminato il diff STAGED (solo modules/web/leggi.py e tests/test_unit_web_leggi.py). Index e worktree sono identici. Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 9 e 10), reports/stato_progetto.md (blocchi Mani, fette 1-4) e .claude/agents/memoria_revisore.md (fino alla #440).

Wall of Shame: in questo diff non c'è nessuno slicing della history, nessuna simulazione di tool, nessun contatto con il kernel. È tutto codice puro del modulo web, senza rete.

### Elementi del diff esaminati

1. modules/web/leggi.py:98 — `_FINE_TAG`, la regex degli attributi spezzata su due stringhe raw. Rischio: che non sia identica a quella proposta nella #440, o che sia rotta dalla concatenazione con triple virgolette. Esito: **ok**. Ho confrontato in modo programmatico la stringa del pattern con quella della #440: è identica (True). Il fuzz differenziale contro html.parser sulla fine del tag (900k tag casuali, 3 seed) non trova nessuna differenza quando la regex trova il «>» e il nome sta nella classe di `_INIZIO_TAG`. Tutte le differenze rimaste sono «la regex dà -1» su una virgoletta mai chiusa. È il caso dichiarato nel commento: il resto della pagina si perde, ma non esce contenuto nascosto.
2. modules/web/leggi.py:532 — prima un `find(">")`, poi `_FINE_TAG.match`. Rischio: costo quadratico su tanti tag. Esito: **ok**. Il find si ferma al primo «>», che sta sempre entro la fine della regex. Se la regex fallisce si esce subito con break. Ripetizioni possessive, nessuna ripetizione vuota.
3. tests/test_unit_web_leggi.py:868 — sonda `<a b=c=="x><script>">SEGRETO</script>VIS`, nel parametrize di `test_ripiego_attributi_e_commenti` (tests/test_unit_web_leggi.py:870). Rischio: test che non morde. Esito: **ok**. Ho rifatto io due mutazioni in una copia isolata: «nome che accetta =» → 5 FAIL; «valore senza virgolette che si ferma a = e alle virgolette» → 1 FAIL. Risultato: 133 passed (Python 3.13).
4. modules/web/leggi.py:89 — `_INIZIO_TAG` con il nome `[a-z0-9:-]*` (contesto: la riga non è cambiata, ma ora fa da confine con `_FINE_TAG`). Rischio: che la regex degli attributi parta a metà nome. Esito: **riserva**, è la R-441-1 qui sotto.

### Riserve

- **R-441-1 (chat Mani) BASSA**, stessa famiglia di R-439-1 e R-440-1, spostata sul NOME DEL TAG. In HTML5 (e in html.parser) il nome del tag continua fino a uno spazio, «/» o «>». `_INIZIO_TAG` invece prende solo `[a-z0-9:-]`. Quindi `_FINE_TAG` comincia a metà nome e legge «"», «'» e «=» come attributi.
  - Sonde confermate (il ripiego mostra SEGRETO, il parser no): `<a=b="><script>">SEGRETO</script>VIS`, `<a"="><script>">SEGRETO</script>VIS`, `<ax=="><script>">…`, `</a"="><script>">…`, `<div'='><style>'>SEGRETO</style>VIS`, `<a.="><script>">…`.
  - Fuzz sul codice staged: 50 casi su 100k.
  - Correzione provata in copia: aggiungere `[^ \t\n\r\f/>]*+` in testa a `_FINE_TAG` (il resto del nome del tag). Risultato: 133 passed, 0 casi su 300k, 0 differenze di fine tag contro html.parser, input avversari da 2 MB in ≤0,014 s.
  - Il controllo del nome intero sui tag nascosti non cambia, perché lì il carattere dopo il nome è già in `_FINE_NOME`.
  - Test suggerito: aggiungere al parametrize `<a=b="><script>">SEGRETO</script>VIS` e `<a"="><script>">SEGRETO</script>VIS`.
  - Gravità bassa: il ripiego non si raggiunge con pagine vere (vedi la nota della fetta 4 in stato_progetto). Ma è un intervento di un solo token: consiglio di chiuderla prima del commit.
- Nota COSMETICA: in `test_embed_non_nasconde_il_resto_della_pagina` è stata tolta la fixture `rete`. È corretto, perché `_componi` non usa la rete.

### Rischi esplicitamente esclusi

- Non ho rifatto le esecuzioni su Python 3.11 (venv) né quelle con rete e DNS bloccati che dichiari: qui ho solo 3.13. Della tua lista di mutazioni ne ho ripetute solo 2 su 6.
- Non ho verificato il comportamento dei browser veri. Il riferimento è html.parser 3.13 più le regole del tokenizzatore HTML5 lette a mano.
- Non ho valutato se aspettarsi un'altra iterazione della stessa famiglia (tokenizzatore imitato a pezzi): il fuzz copriva tag e attributi con un alfabeto ridotto (lettere, = " ' spazi / > < . _).

### Memoria

Ho aggiunto la riga `#441 (chat Mani) — 2026-10-21 — APPROVATO CON RISERVE — …` e una lezione nuova (fuzz differenziale anche con nomi di tag «sporchi»; il confine fra regex del nome e regex degli attributi deve usare la classe di HTML5). Sono in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole con scripts/commit_memoria_revisore.sh (commit f7a3a05). L'index del diff sotto review è rimasto intatto (i due file restano staged).

Copia isolata usata per mutazioni e correzione (fuori dal repo): /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/copia

---

### Review #442 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #442 (chat Mani), 2026-10-21. Ramo feat/mani-web-fetta4 (PR #239). Ho esaminato il diff STAGED: solo modules/web/leggi.py e tests/test_unit_web_leggi.py. L'albero di lavoro è identico allo staged. Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), la sezione Mani di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- modules/web/leggi.py:99 — `_FINE_TAG` ha ora in testa `[^ \t\n\r\f/>]*+`, cioè il resto del nome del tag secondo HTML5. È identico alla correzione proposta nella #441. Rischi esaminati:
  - Tempi: su 6 input avversari da circa 2 MB con nomi sporchi (`<a` + 2M «=», `"=` ripetuti, `</a` ripetuti, `<a"=` senza «>» e simili) il tempo massimo è 0,011 s.
  - Python 3.11: i quantificatori possessivi compilano su 3.11.17.
  - Esito: ok.
- tests/test_unit_web_leggi.py:869 — le 4 sonde nuove: `<a=b=">`, `<a"=">`, `</a"=">`, `<div'='>`. Rischio esaminato: che i test non colgano un ritorno indietro. Ho rifatto la mutazione «senza il resto del nome» in una copia isolata: falliscono tutte e 4. Esito: ok, R-441-1 chiusa.
- modules/web/leggi.py:475 — `_chiusura` (funzione non toccata, ma chiamata dal codice nuovo a modules/web/leggi.py:537) cerca «</nome» senza tener conto di virgolette e commenti. Rischio esaminato: un «</nome» dentro un attributo o un commento, all'interno di un blocco nascosto NON grezzo. Esito: **riserva R-442-1**.
- modules/web/leggi.py:510 — la docstring di `_togli_blocchi_nascosti` dice che «<» o «</script>» dentro un attributo «non contano». Vale solo per il tag di apertura, non per il contenuto dei blocchi nascosti non grezzi. Esito: riserva, è la stessa R-442-1.
- modules/web/leggi.py:89 — `_INIZIO_TAG` riconosce solo `<!--` e `<lettera` / `</lettera`. Rischio esaminato: costrutti che il parser chiude al primo «>» e il ripiego no. Esito: **riserva R-442-2**.

**Verifiche fatte da me**
- 137 passed su Python 3.13.16. Su 3.11 non c'è pytest: lì ho controllato solo che le regex compilino.
- Fuzz differenziale contro `_Estrattore`/html.parser, su 300k stringhe con alfabeto ampio: nomi di tag sporchi, `<!`, `<?`, `<![`, `\x00`, «İ», `\f`, `\r`, «&», tag grezzi e non grezzi. Conto come «fuga» ogni parola visibile nel ripiego e assente sia dal corpo sia dal titolo del parser.
- La famiglia R-439/440/441 (fine del tag di apertura) non dà più differenze. Restano due famiglie diverse, descritte sotto.

**Riserve**
- **R-442-1 (chat Mani) BASSA** — Dentro i blocchi nascosti NON grezzi (svg, math, noscript, template, object, canvas) html.parser legge i tag. Quindi un «</svg>» dentro un attributo o un commento non chiude il blocco. Il ripiego invece lo chiude subito e mostra quello che segue.
  - Riprodotto su tutti e sei:
    - `<svg><a title="</svg>">SEGRETO</a></svg>VIS`: parser `'VIS'`, ripiego `' ">SEGRETO  VIS'`.
    - Lo stesso con noscript, template, object, canvas, e con math usando gli apici singoli.
    - Lo stesso con un commento: `<svg><!--</svg>-->SEGRETO</svg>VIS`.
  - Per script e iframe il comportamento è già alla pari, perché il parser li tratta come grezzi.
  - È la stessa famiglia di V-1 ve #239, spostata dal tag di apertura al contenuto del blocco.
- **R-442-2 (chat Mani) BASSA** — Per il parser sono commenti fasulli, che finiscono al primo «>», questi costrutti: `<!x…`, `<?…`, `</` seguito da un carattere che non è una lettera. `<![CDATA[` finisce invece a «]]>».
  - Nel ripiego la regex finale `<[^<>]*>` si ferma a un «<» interno, e i costrutti non chiusi a fine pagina restano interi. Quindi il loro contenuto resta nel testo.
  - Esempi: `<!Q <?\f>V`, `a<![CDATA[ > Q ]]>b`.
  - Frequenza: circa il 12% delle stringhe casuali, per lo più code non chiuse a fine pagina.
  - Non riesce a far saltare l'apertura di uno script: il ripiego vede più tag del parser, non meno.

Le due riserve sono BASSE perché il ripiego scatta solo se html.parser solleva un errore. Le 60.000 pagine casuali della verifica esterna #238 non l'hanno mai attivato.

**Correzione provata in copia isolata** (non nel tuo albero), che chiude R-442-1, R-442-2 e anche R-431-3:
- Un'unica regex di ricerca: `<(!--|/?[a-z][a-z0-9:-]*|!\[cdata\[|[!?/])`.
- I casi `!`, `?`, `/` finiscono al primo «>»; `![cdata[` finisce a «]]>».
- `_chiusura` resta solo per i tag grezzi: script, style, iframe, title.
- Per gli altri nascosti, un contatore come quello di `_Estrattore`: +1 all'apertura, −1 alla chiusura se è sopra 0. I pezzi di testo si aggiungono solo quando il contatore è a 0.
- Risultati: 137 passed, 0 differenze su 250k stringhe del fuzz, 2 MB avversari in al massimo 0,42 s.
- Attenzione: una prima versione con due `search` separate partendo da `pos` era quadratica (40k «<?>» = 28,6 s, e due test a tempo fallivano). Serve un'unica alternanza, oppure tenere la posizione in cache.

**Wall of Shame e guardrail**: questo diff non tocca la history, `_get_window`, il tetto delle 10 iterazioni, i tetti di output né i provider. Nessuna simulazione di output dei tool. Il ripiego resta fail-safe: `html_unescape` è protetto da try/except e nel ciclo non ci sono eccezioni nuove.

**Rischio escluso**
- Non ho eseguito la suite su Python 3.11, perché in questo ambiente pytest c'è solo su 3.13. Su 3.11.17 ho controllato soltanto che le regex compilino e che l'html.parser installato abbia gli stessi elementi grezzi/RCDATA di 3.13.16.
- Non ho verificato il comportamento con versioni più vecchie di html.parser (senza le patch che rendono grezzo iframe), come quelle che potrebbero esserci sul VPS o sul Mac: in questo ambiente non sono riproducibili.
- Non ho verificato su pagine reali, solo sul fuzz.

**Memoria**: riga #442 e una lezione aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md, committate da me con `scripts/commit_memoria_revisore.sh` (commit e72a96a). L'index del diff sotto review è intatto.

File utili:
- Script di fuzz: /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/fuzz442.py e /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/fuzz442b.py
- Prototipo della correzione: /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/proto/modules/web/leggi.py

---

### Review #444 (chat Mani) — verdetto RIEMESSO dal revisore

Il primo testo citava `gas.py` e `scripts/bot_esito.py`, che dopo il merge non sono più nel diff di sessione: il gate B lo rifiutava (0 citazioni di file del diff). Come vuole /fine-task, il revisore ha riemesso il verdetto (stesso esito e sostanza); sotto il testo riemesso, poi l'originale integrale dentro un blocco di codice (non conteggiato dal gate).

## VERDETTO: APPROVATO

Review #444 (chat Mani), 2026-10-21, riemessa. L'esito e la sostanza non cambiano. Oggetto: il merge di origin/main 7897f97 (PR #240, chat Motore) nel ramo feat/mani-web-fetta4, committato come 33be621 (genitori 4f9ff13 e 7897f97, base comune dec4ce9). Ho riletto CLAUDE.md (sez. 5), reports/stato_progetto.md (blocco «Mani — fetta 4», riga 605) e .claude/agents/memoria_revisore.md.

**Perché la riemissione.** Dopo il merge il diff di sessione è `git diff 7897f97..HEAD`. I suoi file di codice sono solo modules/web/leggi.py e tests/test_unit_web_leggi.py, quindi le citazioni del primo testo (gas.py, scripts/bot_esito.py) non contano più per il gate B.

**Metodo.** Ho fatto quattro controlli:
- `git diff 4f9ff13 33be621 -- modules/web tests/test_unit_web_leggi.py` dà 0 righe: il merge lascia l'area Mani identica al commit prima del merge.
- `git diff dec4ce9 7897f97 -- modules/web tests/test_unit_web_leggi.py` è vuoto: main non tocca l'area Mani.
- `git diff 7897f97 33be621 -- gas.py scripts/bot_esito.py tests/test_unit_kernel.py tests/test_unit_verifica_bot.py reports/da_mergiare.md` è vuoto: i file di main sono arrivati identici.
- gas.py non importa modules.web (grep vuoto), quindi tra i due lati non c'è legame nel codice.

**Elementi del diff esaminati**
- `modules/web/leggi.py:99`: `_FINE_TAG`, la fine del tag nel ripiego secondo il tokenizzatore HTML (resto del nome, virgolette solo dopo «=», ripetizioni possessive). Rischio: che il merge abbia alterato o perso le correzioni R-439-1/R-440-1/R-441-1 del secondo giro. È identico a 4f9ff13 (0 righe di diff sull'area Mani). Esito: ok.
- `modules/web/leggi.py:508`: `_togli_blocchi_nascosti`, la ricerca lineare che usa `_FINE_TAG` (alla riga 533 c'è un find di «>» prima della regex). Rischio: un'unione automatica con righe perse o duplicate dentro la funzione. Identica a 4f9ff13, e main non tocca modules/web dalla base dec4ce9. Esito: ok.
- `tests/test_unit_web_leggi.py:849`: la parametrizzazione di `test_ripiego_attributi_e_commenti` con i casi R-439-1, R-440-1 e R-441-1. Rischio: test del secondo giro persi nel merge, che darebbero una suite verde ma vuota. Il file è identico a 4f9ff13. Sull'albero 33be621 la suite gira con «137 passed in 17.40s», lo stesso conteggio dichiarato per 4f9ff13. Esito: ok.
- `tests/test_unit_web_leggi.py:892`: `test_ripiego_lineare_su_attributi_e_commenti` (tetto di 10 s sulle pagine patologiche). Rischio: perdita della garanzia di linearità. È presente e passa nella stessa esecuzione. Esito: ok.
- Contesto, già verificato nel primo testo e invariato: `.claude/agents/memoria_revisore.md:698` e `reports/stato_progetto.md:605`. Sono unioni a multinsieme base/ours/theirs con 0 righe perse, 0 in più e nessun marcatore di conflitto. reports/handoff.md, ultimo_report.md e diff_sessione.md sono la versione Mani, come prescrive lavoro_parallelo.md. Nota non bloccante, sempre valida: con numeri sovrapposti l'ordine «per numero» non cresce sempre fra i blocchi delle due chat. È accettato dalla regola 4 di lavoro_parallelo.md.

**Esecuzione.** Sull'albero 33be621 tests/test_unit_web_leggi.py dà 137 passed. Nel primo passaggio tests/test_unit_web_leggi.py + tests/test_unit_verifica_bot.py davano 462 passed. La suite kernel (991 PASS / 1 FAIL T31g, sqlite_vec assente) non l'ho rieseguita: mi fido del dato del chiamante, coerente con main.

**Rischio escluso.** Non ho rivisto nel merito la logica di unione della storia in gas.py, né le regole di gravità in scripts/bot_esito.py. È codice di main già revisionato dalla chat Motore (#438-#443), e il merge non lo altera: questa review verifica solo che la risoluzione sia fedele. Non ho verificato il fallimento di T31g (sqlite_vec manca in questo ambiente) né il commit di fine-task successivo a 33be621, che al momento della review non esiste ancora (HEAD = 33be621, reports/ modificati in staging).

**Antipattern.** Il merge non introduce slicing della history né simulazione di tool. Il cap delle 10 iterazioni e `_get_window` non sono toccati dal lato Mani.

**Memoria.** In coda a /home/user/Gas/.claude/agents/memoria_revisore.md ho aggiunto una riga datata sulla riemissione: in una review di merge le citazioni vanno prese dai file del diff di sessione dopo il merge. Nessuna nuova riga contatore, perché la #444 c'è già. Non ho committato e non ho toccato reports/: il file risulta modificato (` M`) e va incluso nel commit di fine-task.

Nota per il chiamante: `python3 scripts/check_verdetto.py` sul handoff attuale dà ancora «verdetto 8: 0 citazioni»: il testo nel §4 va sostituito con questo verdetto riemesso, poi rilanciato il gate B.

#### Testo originale della review #444 (prima della riemissione)

```text
## VERDETTO: APPROVATO

Review #444 (chat Mani), 2026-10-21. Oggetto: il merge di origin/main 7897f97 (PR #240, chat Motore) nel ramo feat/mani-web-fetta4. HEAD è 4f9ff13 e il merge non è ancora committato. Ho letto prima CLAUDE.md (sez. 5), reports/stato_progetto.md, .claude/agents/memoria_revisore.md e reports/lavoro_parallelo.md (regole 3 e 4).

**Metodo.** Ho confrontato ogni file staged con i due genitori (HEAD e MERGE_HEAD) e con la base comune dec4ce9. Per memoria e stato ho fatto un controllo a multinsieme: atteso = base + righe aggiunte da ciascun lato − righe tolte da ciascun lato.

**Elementi del diff esaminati**
- `gas.py:1175`: aggiunge `gia = sync[4]`, così i messaggi già uniti a un salvataggio fallito non si accodano due volte. Rischio esaminato: la risoluzione del merge altera il codice del Motore, oppure c'è uno slicing della history verso i provider. Il gas.py staged è identico byte per byte a MERGE_HEAD (0 righe di diff). Le fette `altrui[:gia[0]]` e `self.history[n_base:]` servono all'unione su disco e all'impronta, non alla finestra mandata ai provider. Le aveva già revisionate la chat Motore (#438-#443). Esito: ok.
- `gas.py:1188`: il rinvio dell'unione a metà turno vale ora per entrambi i rami. Stesso rischio, stessa verifica (identico a main). `py_compile` passa. Esito: ok.
- `scripts/bot_esito.py:109`: nuove righe sulla gravità nel testo del verdetto del bot. Rischio: righe di main perse o duplicate. Identico a MERGE_HEAD (0 righe di diff); tests/test_unit_verifica_bot.py e tests/test_unit_kernel.py sono anch'essi identici a main. Esito: ok.
- `.claude/agents/memoria_revisore.md:698`: Mani #438-#442, poi Motore #438-#443 da `.claude/agents/memoria_revisore.md:707`. Rischio: righe perse o doppie nell'unione manuale. Contro l'unione attesa mancano 0 righe e ce ne sono 0 in più, nessuna riga non vuota duplicata, nessun marcatore di conflitto. Esito: ok.
  - Nota non bloccante: con numeri sovrapposti la sequenza non cresce sempre fra i due blocchi (la Mani #442 viene prima della Motore #438). È accettato dalla regola 4 di lavoro_parallelo.md. Mescolare le righe delle due chat sarebbe solo un'alternativa, non una correzione dovuta.
- `reports/stato_progetto.md:409`: la riga R-c4b3-4 nella versione di main. `reports/stato_progetto.md:605`: il blocco «Mani — fetta 4» col secondo giro, incluse R-439/440/441-1 CHIUSE e R-442-1/R-442-2 (chat Mani) aperte. Rischio: unione automatica che perde una delle due parti. Il controllo a multinsieme dà 0 mancanti e 0 in più. L'unico duplicato («Riserve aperte:», 5 volte) è identico in base, ours e theirs, quindi non nasce dal merge. Esito: ok.
- `reports/da_mergiare.md` è identico a main. reports/handoff.md, ultimo_report.md e diff_sessione.md sono identici a HEAD (versione Mani), come prescrive lavoro_parallelo.md:23. Esito: ok.
- Area Mani: `git diff base..MERGE_HEAD -- modules/web tests/test_unit_web_leggi.py` è vuoto, quindi main non tocca l'area Mani. gas.py non importa modules.web, quindi tra i due lati non c'è legame nel codice.

**Esecuzione.** tests/test_unit_web_leggi.py + tests/test_unit_verifica_bot.py sull'albero unito: 462 passed. La suite kernel (991 PASS / 1 FAIL T31g, sqlite_vec assente) non l'ho rieseguita: mi fido del dato del chiamante, coerente con main.

**Rischio escluso.** Non ho rivisto nel merito la logica di unione della storia in gas.py, né le nuove regole di gravità in scripts/bot_esito.py. Sono codice di main già revisionato dalla chat Motore (#438-#443), e il merge non le altera. Questa review verifica solo che la risoluzione sia fedele. Non ho verificato nemmeno il fallimento di T31g (sqlite_vec manca in questo ambiente).

**Memoria.** Ho aggiunto la riga «#444 (chat Mani) — 2026-10-21 — APPROVATO — …» in coda a /home/user/Gas/.claude/agents/memoria_revisore.md (lezione: nessuna nuova, solo la nota sull'ordine non monotono). Il file risulta modificato ma non in staging, quindi va aggiunto con `git add` prima del commit di merge. Come richiesto, NON ho lanciato commit_memoria_revisore.sh.
```

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 105 → 137 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «137 passed in 17.42s», Python 3.13 e 3.11 (venv): «137 passed in 16.94s»; con rete e DNS veri bloccati via sitecustomize: «137 passed in 16.81s»). Primo giro (`12f7f71`) 105 → 107, secondo giro (`3e0fe70`) 107 → 137.
- Mutazioni del secondo giro, in copia isolata, ciascuna presa da almeno un test: senza il resto del nome del tag, nome dell'attributo che accetta «=», valore senza virgolette senza «=» e virgolette, chiusura della virgoletta obbligatoria, niente spazi prima/dopo «=», niente apici, min→max fra «-->» e «--!>».
- Mutazioni eseguite in copie isolate (1 FAIL ciascuna): commenti ignorati, insieme a 4 tag, confine della chiusura tolto, apertura per prefisso, except di unescape tolto, embed rimesso, chiusura senza «>».
- Sull'albero unito col secondo merge (review #444): web suite 137 passed; kernel 991 PASS / 1 FAIL (T31g, stessa causa); verifica_bot + gate + notte 1272 passed.
- Sull'albero fuso (review #438): gate + notte 947 passed; kernel 987 PASS / 1 FAIL (T31g: manca `sqlite_vec` in questo ambiente, uguale su origin/main).

## §6 STATO CI

CI NON VERIFICATA con `gh run list` (gh non autenticato nella sessione cloud). Mappatura commit→run:
- `12f7f71`: pushato da solo prima del merge di main; run di push non verificata in questa sessione.
- `befc78e` (merge di main) e `71bd77e` (fine-task del primo giro): pushati insieme, run sulla testa `71bd77e`; esito letto dai check della PR #239 via MCP, non da `gh`.
- `c43a59e`, `f7a3a05`, `e72a96a`, `3e0fe70`: nessuna run su questi SHA da soli (pushati insieme a `4f9ff13`, che li contiene).
- `4f9ff13` (fine-task del secondo giro, testa con `c43a59e`…`3e0fe70`): run 39678458664, unit-suite success, handoff-check success; verifica-bot success (letti dai check della PR via MCP).
- `33be621` (merge di main): nessuna run su questo SHA da solo (pushato col commit di fine-task che contiene questo file).
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: **R-442-1 (chat Mani)** BASSA dentro i blocchi nascosti non grezzi (svg, math, noscript, template, object, canvas) il ripiego chiude al primo «</nome» anche dentro un attributo o un commento; **R-442-2 (chat Mani)** BASSA commenti fasulli `<!x`, `<?`, `</` non lettera e `<![CDATA[` nel ripiego (vede più tag del parser, non meno); R-431-3 (annidamento non contato, ora parte di R-442-1); R-432-1 (COSMETICA). Il revisore ha un prototipo che le chiude (contatore come il parser), da portare in una fetta successiva. **V-1 bot #239** BASSA `<svg/>`/`<math/>` autochiusi aprono un blocco nel ripiego (si perde testo, non esce nulla), stessa fetta; V-2 bot #239 COSMETICA: corpo della PR aggiornato, resta il commento del test che cita R-431-3.
- Restano: R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5 e R-ve235-7 (limiti dichiarati). Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1/2/3/4».
