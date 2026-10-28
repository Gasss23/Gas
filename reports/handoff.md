# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Mani fetta 22: riserve «DA SISTEMARE» di #280, `intero()` del figlio lexbor legge «0» e «-0» come 0 (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #285 (https://github.com/Gasss23/Gas/pull/285). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5049895154","url":"https://github.com/Gasss23/Gas/pull/285"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve l'OK dell'operatore. Il merge non accende niente.
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
- **Punti b–e della ripartenza** (accensione, shadow DOM, cosmetiche, decisioni vecchie): `DEFERITA — uno alla volta, dopo questa fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 modules/web/lexbor.py              |  11 ++++++++---
 reports/diff_sessione.md           |  20 +++++++++-----------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   6 +++---
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  55 ++++++++++++++++++++-----------------------------------
 tests/test_unit_web_lexbor.py      |  16 ++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
bbbfbbe fix(web): intero() del figlio lexbor legge «0» e «-0» come 0 (R-bot280-1, R-536-1, fetta 22 Mani)
ec86b45 chore(revisore): memoria review #537 — APPROVATO
63e4137 chore(revisore): memoria review #536 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore bbbfbbe: review #536 sul primo diff staged, #537 dopo la chiusura di R-536-1 (diff committato in bbbfbbe). Verdetti integrali:

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

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py; toccati solo `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py`.
- Web suite (`tests/test_unit_web_*.py`, Python 3.13.16 con selectolax 1.0.2): prima 504 passed / 1 skipped (misurato su b95c3f3) → dopo 521 passed / 1 skipped (+17 casi di `test_intero_come_il_browser`).
- File lexbor su Python 3.11 senza selectolax (come la CI): 20 passed / 60 skipped.
- Nessun FAIL.

## §6 STATO CI

CI NON VERIFICATA con `gh` (assente/non autenticato nel cloud). Check run lette dall'integrazione GitHub sulla PR #285, head bbbfbbe, al momento della scrittura:
- `handoff-check`: failure (run 40682120695) — atteso: su bbbfbbe l'handoff era ancora quello della PR #280.
- `unit-suite`: in corso (run 40682120695).
- `verifica-bot` (smista/verifica/esito): skipped (run 40682177501), etichetta `verifica` non ancora messa.

Mappatura commit→run:
- 63e4137, ec86b45: nessuna run su questo SHA (pushati insieme a bbbfbbe, testati solo nell'albero di bbbfbbe).
- bbbfbbe: run 40682120695 (sopra).
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-ve280-1 BASSA: i test del figlio lexbor con selectolax non girano nei check required (CI su 3.11 senza selectolax). Chat Motore: `selectolax==1.0.2` in requirements-dev.
- Restano quelle delle fette precedenti (stato_progetto, blocchi «Mani — fetta 20/21»): shadow DOM dichiarativo (decisione dell'operatore); cosmetiche R-ve277-3 con R-529-1, R-ve277-4, R-528-3, R-526-1, R-520-4.
