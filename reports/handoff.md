# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-22 — Chat Mani, fetta 11: tag con virgolette aperte, annotation-xml speciale, chiusure di blocco in scope (R6)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore.
2. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; serve un costruttore HTML5 vero (es. lexbor): decide l'operatore.
3. Sul Mac e sulla VPS, dalla cartella di Gas: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` deve dire True.
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

---

## §1 SCOPE & ESITO FETTE

- **R-ve248-3 (fuga preesistente)**: `FATTA`
- **V-1 bot #248 (perdita)**: `FATTA`
- **R-ve246b-5 (perdita)**: `FATTA` per le chiusure di blocco in scope
- **B-476-1 (ALTA), R-476-1 (BASSA)**: `FATTA`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +
 modules/web/leggi.py               |  87 ++++++++++++++--
 reports/diff_sessione.md           |  10 +-
 reports/handoff.md                 | 197 +------------------------------------
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  26 ++---
 tests/test_unit_web_leggi.py       |  64 +++++++++++-
 7 files changed, 161 insertions(+), 228 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
a76a646 fix(web): fetta 11 chat Mani — tag con virgolette aperte, annotation-xml speciale, chiusure di blocco in scope (R6)
f9eb918 chore(revisore): memoria review #477 — APPROVATO
c472651 chore(revisore): memoria review #476 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; il §2 è preso dall'index con i report già in stage, quindi l'elenco dei file è esatto e i numeri dei report possono differire di poco.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Due verdetti, incollati integralmente: #476 (BOCCIATO) e #477 (APPROVATO) (chat Mani), sul diff della fetta 11 committato in `a76a646` dopo la #477 (memorie `c472651`, `f9eb918`, fatte dal revisore). Le righe citate nella #476 si riferiscono al diff di allora.

### Review #476 (chat Mani) — verdetto integrale

## VERDETTO: BOCCIATO

La review #476 (chat Mani, fetta 11, diff STAGED su modules/web/leggi.py e tests/test_unit_web_leggi.py) è BOCCIATA per un motivo bloccante: B-476-1, una regressione ALTA che introduce la nuova regola delle chiusure «in scope». Le altre due correzioni sono giuste.

Letture fatte: CLAUDE.md sez. 5, i blocchi «Mani — fetta 9» e «fetta 10» di reports/stato_progetto.md, la coda di .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**

- `modules/web/leggi.py:395` — chiusura di blocco in scope (R-ve246b-5): toglie tutto fino al tag se fra il tag e la cima non ci sono speciali né confini. Rischio esaminato: la pila di Gas resta con un elemento HTML in meno del browser. Esito: **blocco B-476-1** (dettagli sotto).
- `modules/web/leggi.py:852` — `_controlla_tag`: confronta il tag letto da html.parser con la regola del browser (`_RESTO_NOME` più `_FINE_TAG`). Se non coincidono imposta `_taglia` e scrive un warning. Rischio esaminato: fughe e falsi positivi. Fuzz di 60k pagine con oracolo lexbor (sintassi casuale con spazi, `=`, virgolette, `/`, `<`, tab): 0 fughe nel parser e nel ripiego. Esito: ok per le fughe, una riserva sulle perdite (R-476-1).
- `modules/web/leggi.py:870` — `parse_endtag` passa da `_controlla_tag` anche nel ramo dei commenti fasulli, dove lo stdlib chiama parse_bogus_comment (`</` seguito da un carattere che non è una lettera). Lì browser e html.parser finiscono entrambi al primo `>` e ignorano le virgolette. Esito: **riserva R-476-1 BASSA**. Le 55 perdite nuove del fuzz sono tutte di questo tipo, per esempio `</ a="x>VIS` perde VIS. Rimedio: saltare il controllo se il carattere dopo `</` non è una lettera ASCII.
- `modules/web/leggi.py:235` — indice `_speciali` (i punti più ogni annotation-xml). `modules/web/leggi.py:375` lo usa nel ramo R-468-2 e `modules/web/leggi.py:388` nel `fermo`. Rischio esaminato: `_togli_da` deve restare coerente con la pila, e una chiusura non deve attraversare un annotation-xml. I pop sono ammortizzati. Esito: ok (V-1 bot #248).
- `tests/test_unit_web_leggi.py:1239` e `tests/test_unit_web_leggi.py:1288` coprono le chiusure in scope, ma nessun caso ha un elemento di formattazione sopra il tag: per questo la fuga non è emersa. `tests/test_unit_web_leggi.py:1303` copre R-ve248-3 (sei forme, parser e ripiego). Esito: ok, ma manca il caso che motiva il blocco.

Suite web: 314 passed su 3.13.16 e su 3.11.17.

**BLOCCO B-476-1 (ALTA, regressione rispetto a main 2d20ec0)**

- **Il meccanismo.** La regola di `modules/web/leggi.py:395` toglie dalla pila anche gli elementi di formattazione (a, b, big, code, em, font, i, nobr, s, small, strike, strong, tt, u). Il browser li toglie dallo stack ma li lascia nella lista degli elementi di formattazione attivi. Al primo testo o tag d'apertura li ricrea, cioè ricostruisce gli elementi di formattazione attivi.
- **La divergenza.** In cima alla pila di Gas resta foreignObject, desc o mi, nello spazio svg/math. Il browser invece ha in cima un elemento HTML.
- **Su `</svg>`.** Il browser applica la regola «any other end tag», si ferma su foreignObject (elemento speciale) e ignora la chiusura. Gas invece chiude svg.
- **Prove con lexbor (in entrambi i casi lexbor dà solo «A»):**
  - `<p>A</p><svg><foreignObject><div><b>x</div>y</svg>SEGRETO`: con il diff, SEGRETO arriva al modello sia dal parser sia dal ripiego. Su main la pila diventava incerta e il resto si nascondeva.
  - Variante con contenuto di uno script: `<p>A</p><svg><foreignObject><ul><li><a href=x>x</ul>y</foreignObject><script></svg>SEGRETO</script>VIS` fa uscire SEGRETO.
  - Stessa fuga con `<math><mi><div><i>` e con `<svg><desc><section><font>`.
- **Enumerazione esaustiva con oracolo lexbor** (prefisso `<p>W9</p><svg><foreignObject>` più 5 atomi su 16, 1.048.576 pagine, parser e ripiego, script nello scratchpad `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/f12/enum476.py`): **174 regressioni** con il diff attuale.
- **Perché il vostro campione non l'ha vista.** L'enumerazione a 4 atomi e il campione casuale (2 M pagine su circa 3,5 miliardi di sequenze a 6 atomi) non la trovano: servono svg, foreignObject, div, b, `</div>`, testo e `</svg>`.
- **Rimedio provato in copia isolata** (`/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r476/modules/web/leggi.py`):
  - un indice `_formattanti` costruito come `_confini`: push in `_metti` per i nomi di formattazione nello spazio html, pop in `_togli_da`;
  - nella condizione della regola, `and not (self._formattanti and self._formattanti[-1] > in_cima)`: se c'è un formattante sopra il tag, la pila resta «incerta»;
  - l'indice mantiene il costo O(1). Un controllo che scorre la pila sopra il tag senza togliere nulla tornerebbe quadratico (vedi il test di tempo V-4).
  - Risultato sulla stessa enumerazione: 0 regressioni, 0 perdite nuove. I casi `<svg><desc><ul><li>x</ul>…<p>VIS` e `<foreignObject><div><span>x</div>…VIS` restano visibili.
  - Va aggiunto un test che fallisce senza il rimedio, nel parser e nel ripiego.

**Riserve**

- **R-476-1 BASSA**: il ramo dei commenti fasulli in `parse_endtag`, descritto sopra.

**Altri casi «pila con un elemento in meno» cercati e non trovati**

- `<li>`/`<dd>` che chiudono un div saltandolo: la vecchia li resta nella pila di Gas, quindi non si scende allo spazio svg.
- `</li>`, `</dd>`, `</h1>`, adoption agency su `</b>`: finiscono tutti in «incerta».
- Esclusione di p: confermata necessaria.

**Rischi esplicitamente esclusi**

- Pagine vere: non ho misurato quanto testo si recupera o si perde.
- Python senza le patch del 2025: non verificato. In quel caso il parser non si usa e lavora solo il ripiego.
- La mia enumerazione copre solo il contesto foreignObject con 16 atomi. desc e mi li ho provati solo con sonde mirate.
- html5lib non usato come oracolo.

Memoria aggiornata (riga #476 più una lezione sulla ricostruzione degli elementi di formattazione) e committata: c472651.

### Review #477 (chat Mani) — verdetto integrale (diff del commit `a76a646`)

## VERDETTO: APPROVATO

La review #477 (chat Mani, ri-review della #476 sul diff staged completo di modules/web/leggi.py e tests/test_unit_web_leggi.py) è APPROVATA. B-476-1 e R-476-1 sono chiuse, e le prove con l'oracolo lexbor non trovano né regressioni né perdite nuove.

Letture fatte in questa sessione: CLAUDE.md sez. 5, reports/stato_progetto.md (blocchi fetta 9 e 10), memoria del revisore.

**Elementi del diff esaminati**

- `modules/web/leggi.py:407` — la regola delle chiusure in scope ora richiede anche che nessun elemento di formattazione stia sopra il tag. Rischio esaminato: la pila di Gas con un elemento HTML in meno del browser, che ricrea i formattanti al primo testo (B-476-1). Esito: ok. Mutazione in copia isolata che toglie la condizione: 5 FAIL.
- `modules/web/leggi.py:238` — push in `_formattanti` solo per lo spazio html, pop in `_togli_da` come per `_confini`. Rischio esaminato: incoerenza fra l'indice e la pila, e costo quadratico. Gli indici sono O(1) ammortizzati, senza scansioni. Esito: ok.
- `modules/web/leggi.py:885` — `parse_endtag` chiama `_controlla_tag` solo se dopo `</` c'è una lettera ASCII; altrimenti è un commento fasullo fino al primo `>`. Con la slice vuota (`</` a fine dati) il controllo non parte: corretto, perché lì `j` è -1. Esito: ok. Mutazione in copia (`if True:`): 1 FAIL.
- `tests/test_unit_web_leggi.py:1317` — il controllo B-476-1 copre le quattro sonde, sia nel parser sia nel ripiego. Il caso `</ a="x>VIS` sta nel test «virgolette chiuse resta visibile». Esito: ok, con una nota cosmetica: i casi B-476-1 stanno in un test che si chiama «virgolette aperte».

**Prove eseguite da me**

- Suite: 318 passed su 3.13.16 e su 3.11.17.
- Fuzz della sintassi dei tag, 60k pagine con oracolo lexbor: 0 fughe, 0 perdite nuove. Prima erano 55 perdite, tutte su commenti fasulli.
- Enumerazione esaustiva a 5 atomi, oracolo lexbor, parser e ripiego, codice staged contro main 2d20ec0:
  - prefisso svg+foreignObject: 1.048.576 pagine, 0 regressioni, 0 perdite nuove;
  - prefisso svg+desc (17 atomi): 1.419.857 pagine, 0 regressioni, 0 perdite nuove;
  - prefisso math+mi (17 atomi): 1.419.857 pagine, 0 regressioni, 0 perdite nuove.
- Gli script stanno in `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/f12/enum477.py` e `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/f12/enum476.py`.

**Rischi esplicitamente esclusi**

- Quanto testo si recupera o si perde su pagine vere: non misurato, servirebbe un corpus.
- Python senza le patch del 2025: non verificato, lì lavora solo il ripiego.
- Contesti annotation-xml con encoding HTML e template/object: non enumerati con questo insieme di atomi. annotation-xml era nella tua enumerazione a 4 atomi; template/object ricadono comunque nei confini, che rendono la pila incerta.
- La ricostruzione dei formattanti aperti PRIMA di svg/math non l'ho enumerata. L'ho esclusa ragionando sullo standard: il browser li ricostruisce prima del tag `<svg>` e restano sotto la pila di Gas.

Memoria aggiornata (riga #477, nessuna lezione nuova) e committata: f9eb918.

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 304 → 318 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «318 passed» su Python 3.13.16 e 3.11.17, venv).
- Oracolo lexbor, nuovo contro main 2d20ec0, parser e ripiego: enumerazione esaustiva a 4 atomi (39 atomi con ul/li/span/table/td, `<i a = "x>`, annotation-xml; 2.313.441 pagine), campione casuale 5–7 atomi (3 M pagine), enumerazioni del revisore a 5 atomi con prefissi svg+foreignObject, svg+desc, math+mi (3,9 M pagine): 0 fughe nuove, 0 perdite nuove; perdite tolte: 8 nel campione.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

- `a76a646` e il commit di fine-task con questo handoff: pushati all'apertura della PR; run non ancora disponibili alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Restano: **R-ve246-5** MEDIA preesistente (canvas/object, decisione sul costruttore HTML5), R-469-1, R-466-1, R-466-2, R-ve245-2…5, R-ve245b-4, R-454-2, R-453-2, R-456-2, R-447-1(b), V-2 ve #242, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…11».
