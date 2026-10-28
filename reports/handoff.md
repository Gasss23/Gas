# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Mani fetta 22: riserve «DA SISTEMARE» di #280, `intero()` del figlio lexbor legge «0» e «-0» come 0; secondo giro dopo bot e verifica esterna (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #285 (https://github.com/Gasss23/Gas/pull/285). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5049895154","url":"https://github.com/Gasss23/Gas/pull/285"}`); `gh` nel cloud non è autenticato. Bot e verifica esterna su 162f5b1: APPROVATO CON RISERVE (riserve chiuse in questo giro); il bot rigira sulla head nuova. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve l'OK dell'operatore. Il merge non accende niente.
2. Accensione della lettura con lexbor: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (chiude anche R-ve280-1); poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Shadow DOM dichiarativo (figli «light» di un host con `<template shadowrootmode>`): decisione dell'operatore.
4. Poi, una alla volta: cosmetiche aperte (R-ve277-3 con R-529-1, R-ve277-4, R-528-3, R-526-1, R-520-4); R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **Controllo della PR #280 (fetta 21)**: `FATTA` — mergiata (b95c3f3); branch ripartito da main.
- **Fetta 22 — riserve «DA SISTEMARE» di #280**:
  - R-bot280-1 (`intero("0")` → None): `FATTA` — «0», «000», «-0» danno 0; senza cifre o con un negativo non zero None. Esito pratico invariato.
  - Test diretto di `intero()` (preso dal sorgente del figlio con `ast`, gira senza selectolax): `FATTA`.
  - R-536-1 COSMETICA (review #536: «-0» → None): `FATTA`, review #537 APPROVATO.
  - R-ve280-2, R-ve280-3, R-bot280-2 (numeri e riga ripetuta dell'handoff di #280): `FATTA` — handoff riscritto, solo numeri misurati in sessione.
  - R-ve280-1 (test del figlio non girano nei check required): `DEFERITA — serve la chat Motore (selectolax in requirements-dev)`.
- **Secondo giro — bot e verifica esterna su 162f5b1, APPROVATO CON RISERVE** (commento ve: https://github.com/Gasss23/Gas/pull/285#issuecomment-6468276114):
  - V-1 ve MEDIA (PR in conflitto con main dopo #283 e #284): `FATTA` — merge di 0cf1d67 in 1442468; tenuti handoff/ultimo_report/diff_sessione della #285, stato_progetto unito a mano, memoria con le righe di tutti e due i lati; nessun file del perimetro dal lato di main, niente review.
  - V-2 ve / V-1 bot COSMETICA (commento di `intero()` senza il segno): `FATTA` — 20c0708, review #538 APPROVATO.
  - V-3 ve COSMETICA (numeri dei mutanti del test intermedio): `FATTA` — rifatti sul test finale (ritorno vecchio 7 failed, `letto` tolto 8, negativo 1, solo «+» 2).
  - V-4 ve COSMETICA (§6 sulla CI di un commit vecchio): `FATTA` — §6 riscritto qui sotto.
- **Punti b–e della ripartenza** (accensione, shadow DOM, cosmetiche, decisioni vecchie): `DEFERITA — uno alla volta, dopo questa fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/web/lexbor.py              |  16 +++++++++++-----
 reports/diff_sessione.md           |  15 +++++++++------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   6 +++---
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  35 ++++++++++++++++++++++++++++++-----
 tests/test_unit_web_lexbor.py      |  16 ++++++++++++++++
```

NB: base = merge-base con origin/main = 0cf1d67 (dopo il merge di main). Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
20c0708 docs(web): commento di intero() cita il segno + o - facoltativo (V-2 ve #285, V-1 bot #285)
3704890 chore(revisore): memoria review #538 — APPROVATO
1442468 Merge origin/main (0cf1d67, PR #283 e #284) in claude/peaceful-lovelace-0w2b7q (PR #285)
162f5b1 docs(fine-task): Mani fetta 22 — handoff, report, stato e ripartenza (PR #285)
bbbfbbe fix(web): intero() del figlio lexbor legge «0» e «-0» come 0 (R-bot280-1, R-536-1, fetta 22 Mani)
ec86b45 chore(revisore): memoria review #537 — APPROVATO
63e4137 chore(revisore): memoria review #536 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore bbbfbbe: review #536 sul primo diff staged, #537 dopo la chiusura di R-536-1 (diff committato in bbbfbbe). Merge 1442468: nessun file del perimetro dal lato di main (solo reports/ e memoria), niente review. Commit motore 20c0708 (solo commento): review #538. Verdetti integrali:

### Review #536 (chat Mani) — primo diff staged

## VERDETTO: APPROVATO CON RISERVE

Review #536 (chat Mani). Diff staged su claude/peaceful-lovelace-0w2b7q: modules/web/lexbor.py (+4/-2) e tests/test_unit_web_lexbor.py (+15). Prima della review ho letto CLAUDE.md, la parte di reports/stato_progetto.md su lexbor e R-bot280 e la coda della memoria del revisore.

**Elementi del diff che ho esaminato**
- `modules/web/lexbor.py:101`: il nuovo flag `letto` diventa True alla prima cifra ASCII letta. Rischio esaminato: che una stringa senza cifre (`""`, `None`, `"+"`, `"x0"`, `"-1"`) finisca per valere 0. Esito: ok, tutte danno None e lo verifica il test parametrizzato.
- `modules/web/lexbor.py:109`: il ritorno ora è `int(cifre or "0")` solo se `letto`, con il limite `< 1 << 31` invariato. Rischi esaminati: una regressione sul confine 2147483647/2147483648, e il costo con input lunghissimi (5000 zeri seguiti da "1" danno 1; il taglio `len(cifre) > 10` resta). Esito: ok. Il valore `int(...)` viene calcolato due volte, ma su al massimo 11 cifre: costo irrilevante.
- `modules/web/lexbor.py:114`: è l'unico punto che chiama la funzione (`(intero(size) or 1) > 1`). Rischio esaminato: un cambio di comportamento sulla scelta tra lista e tendina. Esito: ok, il nuovo 0 si comporta come il vecchio None, quindi l'effetto pratico è identico. Il fix è di sola fedeltà al browser.
- `tests/test_unit_web_lexbor.py:171`: il test prende `intero` dal sorgente `_FIGLIO` con `ast`, compila solo quella funzione e la esegue. Rischi esaminati: che il test dipenda da selectolax e che esegua il resto del codice del figlio. Esito: ok. Non porta il marcatore `con_lexbor`, esegue solo il nodo della funzione e non importa nulla dal figlio.

**Prove rifatte da me**
- Lexbor: 75 passed (Python 3.13); il solo test nuovo: 12 passed.
- Mutante «tolgo `letto = True`»: 6 failed, poi file ripristinato e controllato (nessuna differenza rimasta, indice intatto).
- Sonde a mano: `"\t0 "` → 0; `"\x0b5"` → None, corretto perché il tab verticale non è uno spazio per l'HTML; `"00000000002147483647"` → 2147483647; la cifra araba `"٣"` → None, corretto.

**Riserva**
- R-536-1 COSMETICA: `intero("-0")` restituisce None. Il browser lo legge come 0: lo standard HTML ammette "-0" perché vale 0, che non è negativo, e Chromium accetta il segno meno se il valore è 0. È lo stesso tipo di scarto di R-bot280-1, ma l'effetto pratico è nullo perché il chiamante tratta 0 come 1. Va tracciata in stato_progetto.md oppure chiusa con una riga (`"-0"` → 0 nel test).

**Cosa non ho verificato**
- Il comportamento in CI senza selectolax: qui selectolax c'è (75 passed). Che il test nuovo non dipenda da selectolax l'ho dedotto leggendo il codice (nessun marcatore `con_lexbor`, solo `ast` ed `exec`), non da un'esecuzione senza la libreria.
- La suite web completa: ho girato solo il file lexbor. Il diff tocca una sola funzione del figlio, che ha un solo chiamante.

**Memoria**: aggiunta la riga #536 a /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola con lo script (commit 63e4137). I due file staged non sono stati toccati. Nessuna lezione nuova.

### Review #537 (chat Mani) — diff committato in bbbfbbe

## VERDETTO: APPROVATO

Review #537 (chat Mani). Diff staged su claude/peaceful-lovelace-0w2b7q: `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py`. Chiude R-536-1: `intero()` ora accetta un segno + o - in testa, e «-0» vale 0 come nel browser.

**Elementi del diff esaminati**
- `modules/web/lexbor.py:104`: salta un solo segno + o - in testa e poi legge le cifre. Rischio esaminato: segni doppi o misti, segno seguito da spazio, segno da solo. Esito: ok. «--0», «+-1», «-+0», «- 1» e «-» danno tutti None, perché dopo il segno non c'è una cifra e `letto` resta False.
- `modules/web/lexbor.py:112`: restituisce `numero` solo se c'è almeno una cifra, se resta sotto `1 << 31` e se non è un negativo diverso da zero. Rischi esaminati: un negativo che passa, il confine dei 2^31, input lunghissimi. Esito: ok. «-2147483648» e «-» seguito da 5000 nove danno None; «-» seguito da 5000 zeri e «\n-0x» danno 0. Le cifre restano al massimo 11, quindi `int()` è sempre economico. Il tetto `< 1 << 31` non è cambiato.
- `tests/test_unit_web_lexbor.py:174`: 5 casi nuovi nel test parametrizzato già revisionato in #536, che legge `intero` dal sorgente `_FIGLIO` con `ast` (gira anche senza selectolax). Rischio esaminato: test che non distinguono la versione vecchia dalla nuova. Esito: ok, vedi i mutanti qui sotto.
- Contesto: `modules/web/lexbor.py:119` è l'unico chiamante, `(intero(size) or 1) > 1`. Il caso «-0» → 0 lo porta comunque a 1, quindi nella pratica non cambia nulla: è solo fedeltà al browser.

**Prove rifatte da me**
- File lexbor: 80 passed (Python 3.13, con selectolax).
- Mutante senza `not (meno and numero)`: 1 failed. Mutante con solo «+» tra i segni: 2 failed.
- Dopo i mutanti ho ripristinato `modules/web/lexbor.py`: nessuna differenza rimasta e indice intatto.

**Cosa non ho verificato**
- Non ho girato l'intera suite web (521/1) né Python 3.11 senza selectolax (20 passed / 60 skipped): riporto i tuoi numeri. Io ho girato solo il file lexbor su 3.13. Che il test nuovo non dipenda da selectolax lo deduco dal codice (non ha il marcatore `con_lexbor`, usa solo `ast` ed `exec`).
- Nota a margine, non è una riserva: il commento a `modules/web/lexbor.py:99` descrive ancora «spazi, poi le cifre» e non cita il segno. Il commento a `modules/web/lexbor.py:111` lo copre.

**Memoria**: aggiunta la riga #537 a `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata da sola (commit ec86b45); i file staged non sono stati toccati. R-536-1 è chiusa. Nessuna lezione nuova.

### Review #538 (chat Mani) — diff committato in 20c0708

## VERDETTO: APPROVATO

Review #538 (chat Mani). Riguarda il diff staged su claude/peaceful-lovelace-0w2b7q (PR #285): un solo file toccato, modules/web/lexbor.py, con 3 righe aggiunte e 2 tolte.

Letture fatte prima della review: CLAUDE.md (sez. 5), reports/stato_progetto.md (solo le voci lexbor e #285, con Grep), la coda di .claude/agents/memoria_revisore.md.

Elementi del diff esaminati:
- `modules/web/lexbor.py:99` — Il commento in testa a `intero()` ora dice «spazi, un segno + o - facoltativo, poi le cifre ASCII». Rischio esaminato: che il commento descriva un comportamento diverso dal codice. Esito: ok. Il word-diff con `-w` mostra cambi solo dentro le righe `#`, l'AST del file è valido e nessuna istruzione è cambiata.
- `modules/web/lexbor.py:105` — Il ciclo salta un solo segno, `+` oppure `-` (`testo[1:] if testo.startswith(("+", "-"))`). Rischio esaminato: che il commento prometta più segni o solo il «+». Esito: ok, «un segno + o - facoltativo» coincide con il codice.
- `modules/web/lexbor.py:113` — Il ritorno scarta il negativo diverso da zero e i valori oltre il tetto `< 1 << 31`. Rischio esaminato: che il commento nuovo contraddica «interi non negativi». Esito: ok. Il segno meno viene letto ma il negativo non vale, e «-0» dà 0, come dice già il commento a riga 111.
- Contesto: `tests/test_unit_web_lexbor.py:171` estrae `intero()` da `_FIGLIO` con ast, e un cambio che tocca solo i commenti non lo altera. Ho rifatto la prova: lexbor 80 passed (`python3 -m pytest tests/test_unit_web_lexbor.py`).
- Merge precedente 1442468 (origin/main 0cf1d67): rispetto al primo genitore 162f5b1 cambia solo `.claude/agents/memoria_revisore.md`, `reports/coda_notte.md`, `reports/stato_progetto.md` e `reports/ultimo_report.md`. Nessuno di questi è nel perimetro di review (in `.claude/perimetro_review.txt` c'è solo lo script `commit_memoria_revisore.sh`, non il file della memoria). Esito: ok.

Wall of Shame e guardrail: il diff non tocca la history, `_get_window`, i tetti né i provider. Non c'è alcuna simulazione di output dei tool.

Rischio esplicitamente escluso: non ho rifatto la web suite completa (521 passed / 1 skipped con selectolax, prova dell'agente). Ho rifatto solo la suite lexbor (80 passed), perché il cambio riguarda solo un commento e non può alterare il comportamento a runtime. Non ho riletto il contenuto della memoria e di stato_progetto portati dal merge 1442468: sono fuori dal perimetro di review.

Riserve: nessuna. V-2 COSMETICA della verifica esterna #285 e V-1 cosmetica del bot #285 sono chiuse.

Memoria: ho aggiunto la riga `#538 (chat Mani) — 2026-10-28 — APPROVATO — …`, nessuna lezione nuova. È committata da sola con `scripts/commit_memoria_revisore.sh` (commit 3704890). Il diff staged di lexbor.py resta intatto nell'indice.

File rilevanti:
- /home/user/Gas/modules/web/lexbor.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py; toccati solo `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py`.
- Web suite (`tests/test_unit_web_*.py`, Python 3.13.16 con selectolax 1.0.2): prima 504 passed / 1 skipped (misurato su b95c3f3) → dopo 521 passed / 1 skipped (+17 casi di `test_intero_come_il_browser`), uguale prima e dopo il commento di 20c0708.
- File lexbor su Python 3.11 senza selectolax (come la CI): 20 passed / 60 skipped.
- Mutanti sul test finale: ritorno vecchio 7 failed, `letto` tolto 8, senza controllo del negativo 1, solo «+» come segno 2.
- Nessun FAIL.

## §6 STATO CI

CI NON VERIFICATA con `gh` (assente/non autenticato nel cloud). Check run lette dall'integrazione GitHub sulla PR #285:
- Head 162f5b1: `unit-suite` success e `handoff-check` success (run 40682462721); `verifica-bot` success (run 40682482737, verdetto testuale APPROVATO CON RISERVE).
- Head bbbfbbe: `unit-suite` success, `handoff-check` failure atteso (run 40682120695: l'handoff era ancora quello della #280).

Mappatura commit→run:
- 63e4137, ec86b45: nessuna run su questo SHA (pushati insieme a bbbfbbe).
- bbbfbbe: run 40682120695.
- 162f5b1: run 40682462721 (CI) e 40682482737 (bot).
- 1442468, 3704890, 20c0708 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo l'albero del commit di testa).

## §7 RISERVE APERTE

- R-ve280-1 BASSA: i test del figlio lexbor con selectolax non girano nei check required (CI su 3.11 senza selectolax). Chat Motore: `selectolax==1.0.2` in requirements-dev.
- Dalle review e dalle verifiche di questa sessione: nessuna aperta (R-536-1, V-1/V-2/V-3/V-4 ve #285, V-1 bot #285 chiuse).
- Restano quelle delle fette precedenti (stato_progetto, blocchi «Mani — fetta 20/21»): shadow DOM dichiarativo (decisione dell'operatore); cosmetiche R-ve277-3 con R-529-1, R-ve277-4, R-528-3, R-526-1, R-520-4.
