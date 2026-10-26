# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-26 — Mani fetta 18: noscript testo grezzo, R-ve261-2 chiusa, chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #272 (https://github.com/Gasss23/Gas/pull/272). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5019112843","url":"https://github.com/Gasss23/Gas/pull/272"}`); `gh` nel cloud non è autenticato. Merge da solo solo con APPROVATO pulito del bot sull'head.
2. Prossime decisioni, una alla volta: R-ve246-5 MEDIA, R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7; da valutare con l'oracolo: R-518-1 e la riaccensione della regola R-469-1 nelle pagine con noscript.

---

## §1 SCOPE & ESITO FETTE

- **R-ve261-2 — noscript testo grezzo (decisione dell'operatore «vai»)**: `FATTA` — parser (`_modo_grezzo`) e ripiego (`_GREZZI_RIPIEGO`); in XHTML e in svg/math resta un elemento; protezione `con_noscript` lasciata accesa per prudenza (concordato).
- **V-1 bot #270 — test del titolo quando «frameset» non è un tag**: `FATTA` (PR #270 mergiata dall'operatore, 9924438).
- **R-517-1 COSMETICA — commento della guardia `_nascosti_html`**: `FATTA`.
- **R-518-1 BASSA — guardia `_nascosti_html` per canvas/object**: `DEFERITA — da decidere con l'oracolo, tracciata in stato_progetto`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/web/leggi.py               |  23 ++++++++++++++++-------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | n/d (commit finale)
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  55 ++++++++++++++++++++++++++-----------------------------
 tests/test_unit_web_leggi.py       |  37 ++++++++++++++++++++++++++++++++++---
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat` preso con i report in stage, prima del commit finale.

## §3 GIT LOG --ONELINE (sessione)

```
05e956b fix(web): noscript è testo grezzo come nel browser con gli script attivi (R-ve261-2, fetta 18 Mani)
dccf706 chore(revisore): memoria review #518 — APPROVATO CON RISERVE
e3032e2 chore(revisore): memoria review #517 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore 05e956b: review #517 sul primo diff e #518 dopo la correzione del commento (R-517-1). Verdetti integrali:

### Review #517 (chat Mani) — primo diff staged

## VERDETTO: APPROVATO CON RISERVE

Review #517 (chat Mani), fetta 18 Mani: chiude R-ve261-2. Ho letto CLAUDE.md, la voce R-ve261-2 in reports/stato_progetto.md e la mia memoria (in particolare le lezioni #502–#504 su noscript).

**Elementi del diff esaminati**
1. `modules/web/leggi.py:855`: in `handle_starttag` un `noscript` passa al testo grezzo con `_modo_grezzo`, dopo `_contesto.apri`.
   - Rischio esaminato: che diventi grezzo anche dove il browser lo tratta come elemento svg/math. Non succede: l'override di `set_cdata_mode` lo salta in XHTML e quando `estraneo_aperto` è vero.
   - Ho provato le sonde mi, annotation-xml text/html, foreignObject, desc, font color, select, table, head, `</noscriptx>`, `</noscript\t>` e `</noscript/>`: tutte allineate a lexbor.
   - Il mutante che toglie il ramo fa 7 failed.
   - Esito: ok.
2. `modules/web/leggi.py:151`: `noscript` entra in `_GREZZI_RIPIEGO` e quindi anche in `_GREZZI_AUTOCHIUSI`. Di conseguenza `<noscript/>` apre il testo grezzo in HTML, mentre in svg resta vuoto passando per `_esito_autochiuso`.
   - Rischio esaminato: un ripiego che diverge dal parser. Nelle mie sonde il ripiego dà gli stessi token del parser.
   - Esito: ok.
3. `modules/web/leggi.py:242`: il commento di `con_noscript` è aggiornato e la regola R-469-1 resta spenta (scelta prudente concordata con l'operatore).
   - Esito: ok.
4. `tests/test_unit_web_leggi.py:1119`: il nuovo `test_noscript_e_testo_grezzo` copre 9 pagine sia col parser sia col ripiego, più il caso XHTML.
   - `tests/test_unit_web_leggi.py:1072`: il caso frameset dentro noscript ora è visibile.
   - `tests/test_unit_web_leggi.py:1098`: il titolo resta quando «frameset» non è un tag (V-1 bot #270).
   - I tre casi tolti codificavano il vecchio «verso sicuro». Con gli script attivi il browser mostra quel testo (verificato con lexbor), quindi toglierli è giusto.
   - Esito: ok.
5. Contesto: `modules/web/leggi.py:463`. Il commento del ramo con `_nascosti_html` dice ancora che html.parser legge come tag il contenuto di noscript, e non è più vero. La guardia invece resta valida per object e canvas.
   - Esito: riserva R-517-1, cosmetica.

**Prove rifatte**
- Web suite: 441 passed, 1 skipped, sia su 3.13.16 sia su 3.11.
- Fuzz mio, nuovo codice contro main 9924438 e contro lexbor con noscript sostituito da noembed: 120 mila pagine, parser e ripiego, 0 fughe nuove.
  - Un primo giro che conteneva anche gli atomi `<noembed>` e `</noembed>` aveva dato fughe fasulle: venivano dall'oracolo, perché lì `</noembed>` chiude il noscript sostituito. Lezione aggiunta in memoria.
- C'è anche una fuga di main che il fix chiude: `<p>W0</p><object><noscript></object>W1</noscript>W2</object>W3` su main mostrava W2, ora no (come lexbor).

**Il punto che mi hai chiesto di controllare (testo che ora Gas mostra e il browser con script attivi nasconde)**: non ne ho trovati, né nel fuzz né nelle sonde mirate.
- La frase «visibile sia con script attivi sia spenti» però non vale sempre. Esempio: `<noscript><style></noscript>W1</style>`. Con gli script attivi W1 si vede (e Gas lo mostra), con gli script spenti no. Non è una fuga, perché il modello di Gas sono gli script attivi, ma la frase va evitata nei report.

**Riserve**
- R-517-1 (cosmetica): aggiornare il commento in `modules/web/leggi.py:463`, che giustifica la guardia `_nascosti_html` con «html.parser invece lo legge come tag» per noscript, cosa non più vera.
- Nota bassa, solo da annotare: `<p>W0</p><svg><font color=r><noscript></svg>W1</noscript>W2` ora perde W2, che lexbor mostra (main lo mostrava). Non è una classe nuova: la perdita c'è già nella stessa pagina senza `</svg>` (svg resta contato dopo l'uscita con font color). Main mostrava W2 solo perché leggeva `</svg>` dentro noscript. Probabilmente è una delle 2 perdite «vere» dichiarate dall'autore.

**Rischio escluso**: non ho rifatto il differenziale da 180 mila pagine né la corsa col parser vecchio forzato (431/11), né i mutanti XHTML, ripiego e titolo. Ho fatto solo il mutante principale, e per il resto mi fido delle prove dell'autore. L'oracolo con noscript sostituito da noembed non riproduce la differenza head/body con gli script spenti.

Ho preso nota della correzione dell'autore (38 su 40, non 34): non cambia il verdetto.

**Memoria**: riga #517 più una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md e committate da sole (e3032e2). I file del diff restano in stage, intatti.

### Review #518 (chat Mani) — sul diff committato in 05e956b

## VERDETTO: APPROVATO CON RISERVE

Review #518 (chat Mani), ri-review di Mani fetta 18 dopo la #517. Ho controllato il diff in stage (`git diff --cached`) su claude/peaceful-lovelace-0w2b7q. Prima ho letto le tre fonti obbligatorie: CLAUDE.md, le voci R-ve261-2 di reports/stato_progetto.md e la coda di memoria_revisore.md.

**Elementi del diff esaminati**
- `modules/web/leggi.py:463` — commento sulla guardia `_nascosti_html` nel ramo delle chiusure in scope. Rischio: che il commento sia falso, cioè che un noscript HTML possa ancora stare in `_nascosti_html` sopra `in_cima`. Esito: **ok, il commento è vero.**
  - Parser: `handle_starttag` mette noscript in pila (`modules/web/leggi.py:854`) e subito dopo accende il testo grezzo (`modules/web/leggi.py:856`). Da lì html.parser emette solo `</noscript>`, che trova noscript in cima e lo toglie.
  - `<noscript/>`: `_esito_autochiuso` restituisce «grezzo», perché `_GREZZI_AUTOCHIUSI` deriva da `_GREZZI_RIPIEGO` (`modules/web/leggi.py:151`). Vale lo stesso percorso.
  - Ripiego (`modules/web/leggi.py:1139`): `apri` mette noscript in pila e lo stesso passo lo toglie con `contesto.chiudi(tag)`, dopo `_chiusura`.
  - Un noscript dentro svg/math entra in pila col suo spazio (svg/math), non come HTML, quindi non finisce in `_nascosti_html`. In XHTML `_Contesto` non si usa.
  - Prova pratica: ho messo una spia su `chiudi` e generato 60 mila pagine casuali, passate sia al parser sia al ripiego, su 3.13.16 e su 3.11. Casi con un noscript HTML in `_nascosti_html` quando arriva un'altra chiusura: **0**. Con il mutante senza `_modo_grezzo` la spia ne trova 96, quindi è sensibile.
- `modules/web/leggi.py:151` e `modules/web/leggi.py:856` — il resto del diff (noscript fra i grezzi del ripiego e testo grezzo nel parser) e i test (`tests/test_unit_web_leggi.py:1104` e seguenti) sono quelli della #517. Rischio: modifiche al codice eseguibile oltre al commento. Esito: ok. Le righe coincidono con quelle citate nella #517; il commento di `_Contesto` (`modules/web/leggi.py:242`) è testo e basta.
- Suite web: **441 passed, 1 skipped** sia su 3.13.16 sia su 3.11.

**Riserva**
- **R-518-1 BASSA.** Per object e canvas la guardia ora non protegge da fughe:
  - Nessun test la fissa più: il mutante senza guardia lascia la suite a 441/1. Prima la copriva il caso noscript, che adesso non ci arriva.
  - Per canvas causa una perdita di testo rispetto al browser. Con `<p>A</p><svg><foreignObject><ul><li><canvas></ul></foreignObject></svg>Z` il browser mostra «A Z» (`</ul>` chiude canvas) e Gas senza guardia fa lo stesso; con la guardia la pila diventa incerta e il ripiego dà solo «A».
  - Per object la guardia è ridondante: object sta già in `_CONFINI_SCOPE` (`modules/web/leggi.py:193`).
  - Va bene così come scelta di prudenza, ma va tracciata in stato_progetto. Due strade: un test che fissi il comportamento voluto, oppure togliere la guardia dopo un confronto con l'oracolo.

**Rischio escluso.** Non ho confrontato con l'oracolo lexbor il comportamento con e senza guardia sulle pagine con canvas: ho solo ragionato sullo standard (canvas non ferma lo scope). Non ho provato html.parser vecchi senza le patch, che non sono disponibili qui. Su quelli iframe, noembed e noframes potrebbero non essere testo grezzo, e allora la guardia conterebbe anche per loro.

**Memoria.** Ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga #518 e una lezione (rifare il mutante «senza guardia» quando una fetta rende irraggiungibile il caso per cui la guardia era nata). Committata da sola con `scripts/commit_memoria_revisore.sh` (dccf706). In stage restano solo `modules/web/leggi.py` e `tests/test_unit_web_leggi.py`, invariati; `reports/stato_progetto.md` resta modificato fuori stage come prima.

## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati):
- `python3 -m pytest -q tests/test_unit_web_leggi.py`: main 9924438 `433 passed, 1 skipped` → ramo `441 passed, 1 skipped in 24.42s` (3.13.16; dopo il commento di R-517-1) e `441 passed, 1 skipped in 23.93s` (3.11).
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin): `431 passed, 11 skipped in 22.34s` (main 424/10).
- Mutazioni, tutte prese (uscita di pytest): parser senza noscript grezzo → `7 failed, 434 passed`; grezzo anche in svg/XHTML → `2 failed, 439 passed`; ripiego senza noscript grezzo → `7 failed, 434 passed`; titolo scartato per sottostringa «frameset» → `1 failed, 440 passed`.
- Differenziale contro main (worktree 9924438) e lexbor (selectolax 1.0.2, noscript→noembed, senza atomi noembed, textarea visibile, riga Titolo esclusa), × parser e ripiego: seed 1 `fughe nuove 0, uscite con perdite 12` (10 tolgono testo che lexbor nasconde), seed 2 `fughe nuove 0, uscite con perdite 14` (14), seed 3 `fughe nuove 0, uscite con perdite 14` (14); 60 mila pagine ciascuno.

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run lette dall'integrazione GitHub (`actions_list`, branch claude/peaceful-lovelace-0w2b7q):

```
40339701367  verifica-bot  pull_request_target  in_progress  —  05e956b  2026-10-26T14:26:41Z
```

Mappatura commit→run:
- `e3032e2`, `dccf706`: nessuna run su questo SHA (pushati insieme a `05e956b`).
- `05e956b` → verifica-bot 40339701367 in corso; run CI di push non ancora elencata alla scrittura dell'handoff.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-518-1 BASSA (review #518): guardia `_nascosti_html` per canvas/object, da decidere con l'oracolo; tracciata in stato_progetto.
- Restano decisioni dell'operatore: R-ve246-5 MEDIA, R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s; riaccensione della regola R-469-1 nelle pagine con noscript.
