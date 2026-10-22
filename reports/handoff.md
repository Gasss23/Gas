# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-22 — Chat Mani, fetta 8: CDATA in HTML e XHTML senza testo grezzo (R6, PR #245)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #245 (https://github.com/Gasss23/Gas/pull/245): vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore.
2. R-463-1 (MEDIA preesistente): fetta dedicata per tracciare il nodo corrente come il browser (chiuderebbe anche R-450-1 e V-2 ve #243)?
3. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

(`gh` non autenticato nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **R-ve244-3 (CDATA in HTML)**: `FATTA` (fuori da svg/math; residuo R-463-1)
- **R-ve244-2 (XHTML senza testo grezzo)**: `FATTA`
- **V-1 bot #244 (limite dichiarato)**: `FATTA`
- **R-463-1, R-463-2**: `DEFERITA — preesistenti, registrate`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/web/leggi.py               |  42 +++++++++++++++++++++++++++++++++---
 reports/diff_sessione.md           |  11 +++++-----
 reports/handoff.md                 | 425 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  33 +++++++++++-----------------
 tests/test_unit_web_leggi.py       |  40 +++++++++++++++++++++++++++++++++-
 7 files changed, 170 insertions(+), 386 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
aa0b4f9 fix(web): fetta 8 chat Mani — CDATA in HTML come i browser, XHTML senza testo grezzo (R6)
96b83f5 chore(revisore): memoria review #463 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit, quindi le righe di `reports/handoff.md` possono differire di poco (l'elenco dei file è esatto).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Un verdetto, incollato integralmente: #463 (chat Mani), sul diff del commit `aa0b4f9` (memoria in `96b83f5`, fatta dal revisore).

### Review #463 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #463 (chat Mani), 2026-10-22. Fetta 8 Mani (R6), diff staged su feat/mani-web-fetta8, base 43a2545. Prima di iniziare ho letto CLAUDE.md (sez. 1, 5, 8, 10), reports/stato_progetto.md (blocco «Mani — fetta 7», dove R-ve244-2 e R-ve244-3 risultano aperte) e le lezioni sul parsing HTML in .claude/agents/memoria_revisore.md (righe 700-752: punti di integrazione, oracolo html5lib, atomi del fuzz).

Il diff non contiene slicing della history né output di tool simulati. Non tocca né i guardrail (cap 10 iterazioni, 8k, `_get_window`) né i provider. Va nel verso «zero crash»: nel parser i casi senza fine restituiscono -1, come fa html.parser.

### Elementi del diff esaminati

- modules/web/leggi.py:507 — override di `parse_html_declaration`. Fuori da svg/math, `<![CDATA[` diventa un commento fasullo fino al primo `>`.
  - Ho letto lo stdlib 3.13.16. Righe citate: Lib/html/parser.py:287 e :390, quindi stdlib e non repo. `goahead` chiama `parse_html_declaration` per ogni `<!` che non è un commento. Con -1 e fine dati arriva al ramo `startswith("<![CDATA[") and self._support_cdata`, quindi `unknown_decl`, quindi testo nascosto. Lo stesso vale per la 3.11.17.
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

### Lezioni nuove in memoria

- Il CDATA dipende dal nodo corrente aggiustato: sondare sempre i punti di integrazione con un elemento HTML aperto.
- L'oracolo html5lib (etree) deve saltare i nodi commento, altrimenti dà falsi positivi. Mi è successo nelle sonde: i commenti fasulli risultavano «visibili».

Riga #463 scritta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola con scripts/commit_memoria_revisore.sh (commit 96b83f5). Il diff staged del motore è rimasto intatto. Sonde e html5lib stanno nello scratchpad, in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/sonda.py.

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 192 → 199 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «199 passed in 21.04s» su Python 3.13; «199 passed in 20.44s» su 3.11 (venv); «199 passed in 19.85s» con rete e DNS veri bloccati via sitecustomize).
- Fuzz differenziale: 0 fughe su 200k HTML (3.13), 100k (3.11), 100k XHTML; fuzz454/fuzz456 con oracolo html5lib contro HEAD: 0/0; fuzz con atomi CDATA (`fuzz_cdata.py`): 1 caso su 30k (3.13) visibile sotto il modello «script attivi», 0 su 15k (3.11).
- Mutazioni in copie isolate, 7/7 prese: senza override CDATA, override anche in svg, cdata_mode attivo in XHTML, ripiego CDATA sempre/mai fino a `]]>`, ripiego XHTML con grezzi non contati / come in HTML.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

`gh` non autenticato nella sessione cloud. Mappatura commit→run:
- `96b83f5`, `aa0b4f9`: pushati insieme prima di aprire la PR #245; run di push sulla testa `aa0b4f9` non letta (handoff-check atteso rosso: handoff non ancora aggiornato).
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: **R-463-1 (chat Mani)** MEDIA preesistente (CDATA nei punti di integrazione con un elemento HTML aperto); **R-463-2 (chat Mani)** BASSA preesistente (ripiego case-insensitive su CDATA dentro svg).
- Restano: R-454-2, R-453-2, R-456-1/2, R-450-1, V-2 ve #243, R-447-1(b), V-2 ve #242, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…8».
