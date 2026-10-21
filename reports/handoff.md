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
- **R-450-1 (punti di integrazione HTML dentro svg/math)**: `DEFERITA — BASSA preesistente, registrata`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/web/leggi.py               |  21 ++++++++++++++-------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 276 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  30 +++++++++++++-----------------
 tests/test_unit_web_leggi.py       |  24 ++++++++++++++++++++++++
 7 files changed, 141 insertions(+), 228 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
6f13e6e fix(web): fetta 6 chat Mani — <title/> apre il titolo fuori da svg/math, test sul contatore (R6)
354f866 chore(revisore): memoria review #450 — APPROVATO CON RISERVE
a5c33b2 chore(revisore): memoria review #449 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit, quindi le righe di `reports/handoff.md` possono differire di poco (l'elenco dei file è esatto).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Due verdetti, incollati integralmente: #449 e #450 (chat Mani), sul diff del commit `6f13e6e` (la #449 ha chiuso le proprie riserve nello stesso diff; le righe di memoria sono nei commit `a5c33b2`, `354f866` fatti dal revisore).

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

## §5 DELTA TEST DEL MOTORE

- Web suite: 167 → 172 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «172 passed in 19.40s» su Python 3.13; «172 passed in 18.87s» su 3.11 (venv); «172 passed in 18.81s» con rete e DNS veri bloccati via sitecustomize).
- Fuzz differenziale ripiego contro parser: 0 fughe su 200k pagine (3.13) e 100k (3.11).
- Mutazioni in copie isolate, tutte prese: parser `_aperti` che non scala, ripiego `aperti` che non scala, `<title/>` vuoto nel parser, title autochiuso ignorato nel ripiego, title anche dentro svg (parser e ripiego).
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

`gh` non autenticato nella sessione cloud: esiti letti dai check della PR via MCP GitHub. Mappatura commit→run:
- `a5c33b2`, `354f866`, `6f13e6e`: pushati insieme prima di aprire la PR #243; una run di push sulla testa `6f13e6e` può esistere con handoff-check rosso (handoff non ancora aggiornato, come per `f583746` nella fetta 5): non verificata alla scrittura dell'handoff.
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: **R-450-1 (chat Mani)** BASSA preesistente: nei punti di integrazione HTML dentro svg/math (foreignObject, desc, title; mi, mo, mn, ms, mtext) `<title/>` apre un titolo per i browser, mentre parser e ripiego lo trattano come vuoto.
- Restano: R-447-1 parte (b), V-2 ve #242 (commenti vuoti su 3.11), R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…6».
