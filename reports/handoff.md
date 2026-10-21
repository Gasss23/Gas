# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — Chat Mani, fetta 4: note della PR #238 (R6, PR #239)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #239 (https://github.com/Gasss23/Gas/pull/239): vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo nuova richiesta esplicita dell'operatore.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

(`gh` non autenticato nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Nome del tag intero (V-1 bot #238, R-431-1)**: `FATTA`
- **Ripiego alla pari col parser (V-2 ve #238)**: `FATTA` (annidamento non contato, dichiarato)
- **`embed` fuori dai tag con contenuto (R-431-2)**: `FATTA`
- **Test mancanti (V-1/V-4 ve #238, V-2/V-3 bot #238)**: `FATTA`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/web/leggi.py               |  74 ++++++++++++++++++++++++++++++++++++++-----------------
 reports/diff_sessione.md           |  13 +++++-----
 reports/handoff.md                 | 480 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 ++-
 reports/ultimo_report.md           |  41 +++++++++++++++----------------
 tests/test_unit_web_leggi.py       |  49 +++++++++++++++++++++++++++++++------
 7 files changed, 235 insertions(+), 429 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
befc78e Merge origin/main in feat/mani-web-fetta4
12f7f71 fix(web): fetta 4 chat Mani — ripiego alla pari col parser, nomi dei tag interi, embed
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit, quindi le righe di `reports/handoff.md` possono differire di poco (l'elenco dei file è esatto). I commit di main portati dal merge non sono della sessione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Tre verdetti, incollati integralmente: #431 (chat Mani), #432 (chat Mani), #438 (chat Mani, merge di main).

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

## §5 DELTA TEST DEL MOTORE

- Web suite: 105 → 107 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «107 passed», Python 3.13.16 e 3.11.17; 107 passed anche con rete e DNS veri bloccati via sitecustomize).
- Mutazioni eseguite in copie isolate (1 FAIL ciascuna): commenti ignorati, insieme a 4 tag, confine della chiusura tolto, apertura per prefisso, except di unescape tolto, embed rimesso, chiusura senza «>».
- Sull'albero fuso (review #438): gate + notte 947 passed; kernel 987 PASS / 1 FAIL (T31g: manca `sqlite_vec` in questo ambiente, uguale su origin/main).

## §6 STATO CI

- `12f7f71`: pushato da solo prima del merge di main; run di push non verificata in questa sessione.
- `befc78e` (merge di main): pushato prima dell'apertura della PR; run non verificata in questa sessione. Sui commit intermedi `handoff-check` può essere rosso per costruzione.
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: R-432-1 (COSMETICA), R-431-3 (dichiarata nella docstring), chat Mani.
- Restano: R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5 e R-ve235-7 (limiti dichiarati). Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1/2/3/4».
