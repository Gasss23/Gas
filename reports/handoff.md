# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Mani fetta 23: shadow DOM dichiarativo letto come il browser nel figlio lexbor ; secondo giro dopo il bot (merge di main) (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #288 (https://github.com/Gasss23/Gas/pull/288). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5055020609","url":"https://github.com/Gasss23/Gas/pull/288"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve l'OK dell'operatore. Il merge non accende niente.
2. Accensione della lettura con lexbor: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (chiude anche R-ve280-1); poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Poi, una alla volta: cosmetiche aperte (R-ve277-3 con R-529-1, R-ve277-4, R-528-3, R-526-1, R-520-4, R-540-1); R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #285 (fetta 22)**: `FATTA` — richiesta dell'operatore («mergia 285»), merge 297fc22; branch ripartito da main.
- **Fetta 23 — shadow DOM dichiarativo (scelta 3 dell'operatore)**: `FATTA` nel figlio lexbor.
  - Host validi (lista dello standard o custom element, esclusi i nomi riservati), primo template con shadowrootmode open/closed, slot assegnati per nome (testo solo allo slot senza nome), riserva, figli non assegnati nascosti, shadow annidati, body come host: `FATTA`.
  - Pagine senza shadow senza costo in più (`CON_SHADOW`): `FATTA`.
  - R-539-1 BASSA e R-539-2 COSMETICA (review #539): `FATTA`, review #540 APPROVATO.
  - R-540-1 COSMETICA (slot dentro `foreignObject`): `DEFERITA — svg è nascosto per scelta in leggi.py`.
  - Lettura di sempre di leggi.py: `SALTATA — resta com'è, come dichiarato nella scelta 3`.
- **Secondo giro — bot su af8f8ec NON approvata per V-1 MEDIA** (PR in conflitto con main dopo la #287): `FATTA` — merge di origin/main 0a9ce70 in 5ff6ad7; da main entrano gas.py, brains/claude_cli.py, tests/test_unit_kernel.py e tests/test_unit_claude_cli.py identici a main; tenuti handoff/ultimo_report/diff_sessione della #288, stato_progetto unito a mano, memoria con le righe di tutti e due i lati; review #541 APPROVATO.
- **Accensione lexbor (punto b della ripartenza)**: `DEFERITA — chat Motore, selectolax non ancora in requirements su main`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/web/lexbor.py              |  92 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 reports/diff_sessione.md           |  17 ++++++++---------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   6 +++---
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  39 +++++++++++++++++++++++++++------------
 tests/test_unit_web_lexbor.py      |  44 ++++++++++++++++++++++++++++++++++++++++++++
```

NB: base = merge-base con origin/main = 0a9ce70 (dopo il merge di main). Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
4021d67 docs(fine-task): PR #288 dopo il merge di main 0a9ce70 — handoff e report, review #541
5ff6ad7 Merge origin/main (0a9ce70, PR #287) in claude/peaceful-lovelace-0w2b7q (PR #288)
af8f8ec docs(fine-task): Mani fetta 23 — shadow DOM dichiarativo, handoff e report (PR #288)
16cb6a6 feat(web): shadow DOM dichiarativo letto come il browser nel figlio lexbor (fetta 23 Mani)
484982b chore(revisore): memoria review #540 — APPROVATO
d553ca2 chore(revisore): memoria review #539 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore 16cb6a6: review #539 sul primo diff staged, #540 dopo la chiusura di R-539-1 e R-539-2 (diff committato in 16cb6a6). Merge 5ff6ad7 (da main entrano gas.py, brains/claude_cli.py e i loro test): review #541. Verdetti integrali:

### Review #539 (chat Mani) — primo diff staged

## VERDETTO: APPROVATO CON RISERVE

Review #539 (chat Mani), sul diff staged di claude/peaceful-lovelace-0w2b7q partito da main 297fc22. Ho letto CLAUDE.md (sezioni 1, 5, 8, 10), reports/stato_progetto.md (per sezioni, con Grep) e .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `modules/web/lexbor.py:143` — HOST, la lista degli elementi che possono avere uno shadow. Rischio: lista diversa da quella dello standard («valid shadow host name»). Esito: ok. La lista coincide; il trattino con iniziale a-z vale per i custom element; `<X1>` e `<a>` vengono scartati (c'è un test).
- `modules/web/lexbor.py:150` — `shadow()` prende il primo template figlio con open/closed, senza distinguere maiuscole. Rischio: un template con modo non valido che arriva prima, o un secondo template. Esito: ok. Prova: `a<template shadowrootmode=x>T</template>b<template shadowrootmode=closed>S<slot>…c` dà «Sabc», come il browser.
- `modules/web/lexbor.py:160` — `template_fragments()[0]`. Rischio: lista vuota. Esito: **riserva R-539-1**, sotto.
- `modules/web/lexbor.py:164` — primo slot per nome con `frammento.css("slot")`. Rischio: conta anche gli slot dentro template normali o shadow annidati, il che darebbe costo quadratico e assegnazioni sbagliate. Esito: ok. Prova: con uno slot dentro un `<template>` normale nello shadow vince lo slot Q successivo, e si legge «L» come nel browser. Lo slot nascosto reclama comunque il nome (test «Q»). I nomi distinguono le maiuscole: `slot=A` non va a `name=a`, come vuole lo standard.
- `modules/web/lexbor.py:210` e `modules/web/lexbor.py:216` — uno slot dello shadow legge gli assegnati col livello fuori dall'host. Rischio: livello sbagliato con gli shadow annidati. Esito: ok. Prove: «[L]» con slot su slot, slot di riserva annidati («T» oppure «N»), `slot=''` va allo slot senza nome. Mutante mio (`giro` al posto di `fuori` alla riga 216): 1 failed. Ho rimesso il file com'era (0 differenze dall'indice).
- `tests/test_unit_web_lexbor.py:104` e `tests/test_unit_web_lexbor.py:144` — i casi nuovi coprono: host non validi, primo template, testo solo allo slot senza nome, annidamento, body come host. Esito: ok. Risultato: 92 passed su 3.13; 20 passed e 72 skipped su 3.11 senza selectolax.
- Costo — `modules/web/lexbor.py:148` (CON_SHADOW) più una scansione lineare dei figli per ogni host. Rischio: costo quadratico. Esito: ok, cresce in modo lineare. 50k, 100k e 200k figli di un host: 0,19 s, 0,45 s, 0,91 s. 2000, 4000 e 8000 shadow annidati: 0,07 s, 0,10 s, 0,15 s. 8000 slot con nome: 0,09 s.
- Contesto: `modules/web/leggi.py:101` — `_TAG_NASCOSTI` contiene template, svg e math, quindi in produzione il figlio non entra mai nel contenuto svg o math.

**Riserve**
- **R-539-1 (BASSA)**: `<svg><x-a><template shadowrootmode=open>…` passato con nascosti vuoti fa fallire il figlio con `IndexError: list index out of range` (uscita 1). Gas non crasha: c'è il warning in gas_debug.log e si usa la lettura di sempre. Dal chiamante reale (leggi.py) non si può raggiungere, perché svg e math sono nascosti. È però una funzione pubblica che esce in eccezione su un input valido. Correzione proposta: `frammenti = figlio.template_fragments()` e, se la lista è vuota, `continue` o `return None`.
- **R-539-2 (COSMETICA)**: tre casi rari in cui la lettura non segue lo standard:
  - `css("slot")` conta anche un `<slot>` dentro un `<svg>` dello shadow, che non è uno slot HTML. Esempio: `<svg><slot></slot></svg><slot>Q</slot>` più la luce L dà «Q», il browser dà «L».
  - I nomi riservati dei custom element (font-face, annotation-xml, color-profile, missing-glyph…) vengono presi come host. Esempio: `<font-face>` dà «S», il browser dà «L».
  - Uno slot dentro un'opzione di un select nello shadow si legge senza il contesto dello shadow, perché `visita(o, dentro_opzione=True)` riparte da `giro=None`.

**Rischio escluso**: non ho confrontato i risultati con un browser vero (Chromium o Firefox). La fedeltà allo standard l'ho verificata sul testo delle specifiche (WHATWG, cioè lo standard HTML e DOM: «find a slot», «attach a shadow root», parser dei template con shadowrootmode) e con le sonde sul figlio lexbor. Non ho rifatto né la web suite completa né la suite vecchia con GAS_WEB_LEXBOR=1: mi baso sulle tue cifre (533/1, 11 FAIL invariati).

Il mutante «CON_SHADOW = True» che sopravvive è accettabile: cambia solo i tempi.

Memoria: aggiunte la riga #539 (chat Mani) e una lezione (gli `[0]` sulle liste di selectolax vanno provati con nascosti vuoti e foreign content). Committate con lo script in d553ca2: solo /home/user/Gas/.claude/agents/memoria_revisore.md, l'indice staged è intatto. Le riserve vanno scritte in /home/user/Gas/reports/stato_progetto.md.

### Review #540 (chat Mani) — diff committato in 16cb6a6

## VERDETTO: APPROVATO

Review #540 (chat Mani), sul diff staged di claude/peaceful-lovelace-0w2b7q: chiusura di R-539-1 e R-539-2. Ho letto CLAUDE.md, reports/stato_progetto.md (le sezioni che servivano) e .claude/agents/memoria_revisore.md (anche nella review #539 di questa stessa sessione).

**Elementi del diff esaminati**
- `modules/web/lexbor.py:181` — `template_fragments()` vuoto ora porta a `continue`, non più a IndexError. Rischio: il figlio fallisce su un template svg. Esito: ok. La sonda `<svg><x-a><template shadowrootmode=open>S</template>L</x-a></svg>` dà «SL» senza errore. Il mutante `return None` passa i test, ma in pratica cambia nulla: un host svg non ha template HTML dopo quello. R-539-1 CHIUSA.
- `modules/web/lexbor.py:149` e `modules/web/lexbor.py:159` — `primi_slot` scende dall'alto senza ricorsione e salta svg e math. Rischio: costo quadratico, oppure contare slot dentro il contenuto dei template. Esito: ok. Uno slot dentro un `<template>` normale, a sua volta dentro uno slot, non conta (sonda: dà «N»). Con 8000 slot con nome il tempo è 0,10 s.
- `modules/web/lexbor.py:146` — l'insieme RISERVATI (annotation-xml, color-profile, font-face*, missing-glyph) esclude dagli host gli 8 nomi riservati dello standard. Esito: ok. La sonda `<font-face>` dà «L».
- `modules/web/lexbor.py:134` e `modules/web/lexbor.py:222` — `opzioni(select, giro)` e `visita(o, True, giro)`: uno slot dentro un'opzione resta nello shadow. Esito: ok. Una sonda con slot con nome dentro un'opzione dà «AN», come il browser. Mutante mio (`giro` → `None` alla riga 134): 1 failed. Ho rimesso il file com'era (0 differenze dall'indice).
- `tests/test_unit_web_lexbor.py:143` e `tests/test_unit_web_lexbor.py:146` — 4 casi nuovi, uno per R-539-1 e tre per le parti di R-539-2. Risultato: 96 passed su 3.13; 20 passed e 76 skipped su 3.11 senza selectolax.
- Costo: resta lineare. 50k, 100k e 200k figli di un host: 0,21 s, 0,43 s, 0,79 s. 2000, 4000 e 8000 shadow annidati: 0,06 s, 0,10 s, 0,17 s.

**Nota COSMETICA (R-540-1)**: uno slot HTML dentro `<svg><foreignObject>` (o dentro `annotation-xml` di math) nello shadow, nel browser, prende comunque il nome. `primi_slot` lo salta, perché non entra mai in svg. Esempio: browser «LQ», Gas «L». Gas nasconde svg per scelta, quindi la differenza conta poco. Non blocca.

**Rischio escluso**: non ho fatto confronti con un browser vero (Chromium o Firefox); la fedeltà l'ho verificata sul testo delle specifiche e con le sonde sul figlio lexbor. Non ho rifatto né la web suite completa né la suite vecchia con GAS_WEB_LEXBOR=1: mi baso sulle tue cifre (537/1, 11 FAIL invariati).

Memoria: aggiunta la riga #540 (chat Mani), senza lezioni nuove. Committata con lo script in 484982b: solo /home/user/Gas/.claude/agents/memoria_revisore.md, l'indice staged è intatto. In /home/user/Gas/reports/stato_progetto.md vanno segnate R-539-1 e R-539-2 come CHIUSE e R-540-1 come COSMETICA aperta.

### Review #541 (chat Mani) — merge 5ff6ad7

Il verdetto originale (sotto, nel blocco di codice, testo integrale e invariato) citava come `path:riga` soprattutto file entrati da main, che non sono nel diff di sessione (base 0a9ce70 dopo il merge): il Gate B lo ha rifiutato (1 citazione valida su 2). Come da regola il testo non è stato ritoccato: il revisore lo ha riemesso con lo stesso esito e la stessa sostanza, citando i file del diff. Fa fede il verdetto riemesso; l'originale resta qui per tracciabilità.

Verdetto originale:

```
## VERDETTO: APPROVATO

Review #541 (chat Mani). Ho esaminato il merge di origin/main 0a9ce70 (PR #287) in claude/peaceful-lovelace-0w2b7q (PR #288, HEAD af8f8ec). Il merge è in corso e non ancora committato; merge-base 297fc22.

**Elementi del diff esaminati**
- `gas.py:4912`: `_motivo_forte(e)` entra da main nel ramo `except`. Subito dopo c'è `continue` verso il brain successivo, quindi il fallback §9 è intatto. Ho controllato che il merge non perda nulla rispetto a main: `git diff --cached origin/main -- gas.py brains` è vuoto, cioè il file è identico a main (contenuto già revisionato in #538/#539 chat Motore). Esito: ok.
- `brains/claude_cli.py:317`: i `raise` hanno testi fissi con prefisso «claude-cli: », identici a main. Nessuna fuga di dati nel motivo mostrato. Esito: ok.
- `modules/web/lexbor.py:179`: `template_fragments()` vuoto porta a `continue` (chiusura R-539-1). Ho controllato che il lato Mani non venga perso: `git diff --cached af8f8ec -- modules tests/test_unit_web_lexbor.py` è vuoto (0 righe). Esito: ok.
- `tests/test_unit_kernel.py:1` e `tests/test_unit_claude_cli.py:1`: arrivano da main (+50 e +5 righe rispetto a HEAD). Rispetto a origin/main, nella cartella tests differisce solo `tests/test_unit_web_lexbor.py` (lato Mani). Esito: ok.
- `.claude/agents/memoria_revisore.md`: rispetto a main ci sono solo +3 righe aggiunte (#539 Mani, la sua lezione, #540 Mani), nessuna cancellata. Rispetto a HEAD entrano #538 Motore, la sua lezione e #539 Motore. Nessuna perdita. Esito: ok.
- `reports/stato_progetto.md:4`: la catena «Ultimo aggiornamento» è unita senza perdite (Mani fetta 23, poi Motore PR #287, poi Mani fetta 22 e il resto). Ci sono sia la voce RIPARTENZA Motore aggiornata da main sia la voce «Mani — fetta 23». Esito: ok.
- Non ho trovato marcatori di conflitto (`<<<<<<<`, `>>>>>>>`, `=======`) in memoria, reports/ e gas.py. AST di gas.py e lexbor.py ok.

**Prove eseguite da me:** `pytest tests/test_unit_claude_cli.py tests/test_unit_web_lexbor.py` → 125 passed.

**Rischio escluso:** non ho rieseguito la suite kernel completa (1056 PASS / 1 FAIL T31g dichiarato da te, `sqlite_vec` assente: noto) né la suite web completa. Il codice del motore è identico byte per byte a quello già revisionato e testato sui due rami (diff vuoti sopra), quindi rieseguirla aggiunge poco.

**Note fuori perimetro, non bloccanti**
- `reports/handoff.md`: rispetto alla #288 git ha preso in automatico una riga da main (la nota «Il suo hash è nel `git log` del branch dopo il push»). È innocua e si riscrive comunque al fine-task.
- Il doppio #538/#539 nel contatore (chat Mani e chat Motore) resta distinto dal suffisso. È R-539-1 COSMETICA (chat Motore), già tracciata.

**Memoria revisore:** ho aggiunto la riga #541 in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`. Il commit atomico NON è avvenuto: `scripts/commit_memoria_revisore.sh` ha fallito in modo controllato (rc=128, «cannot do a partial commit during a merge», warning in `/home/user/Gas/gas_debug.log`, exit 0). La riga resta nel working tree, non in staging.
**Cosa devi fare:** fai `git add .claude/agents/memoria_revisore.md` prima del commit di merge, così la riga #541 entra col merge. Nota che aggiungere quel file cambia il diff staged: crea il marcatore (`bash scripts/segna_review_ok.sh`) solo dopo quell'add.

Nessuna lezione nuova.
```

Verdetto riemesso:

## VERDETTO: APPROVATO

Review #541 (chat Mani), verdetto riemesso per il gate B. Esito e sostanza sono gli stessi di prima. Ho cambiato solo le citazioni: ora puntano ai file del diff di sessione contro 0a9ce70.

L'oggetto è il merge di origin/main 0a9ce70 (PR #287) in claude/peaceful-lovelace-0w2b7q (PR #288). Le righe citate valgono su HEAD 4021d67, che è il commit di fine-task venuto dopo il merge 5ff6ad7.

**Elementi del diff esaminati**
- `modules/web/lexbor.py:179` — `template_fragments()` legge il contenuto del template shadow. Rischio: perdere la chiusura R-539-1 durante il merge. Verifica: `modules/web/lexbor.py:180` fa ancora `continue` se la lista è vuota, prima di `[0]`. `git diff af8f8ec HEAD -- modules tests/test_unit_web_lexbor.py` è vuoto (0 righe), quindi il lato Mani è intatto. Esito: ok.
- `modules/web/lexbor.py:169` — `shadow()` sceglie il primo template open/closed tra i figli dell'host. `modules/web/lexbor.py:146` contiene `RISERVATI` e `modules/web/lexbor.py:149` contiene `primi_slot`. Rischio: una risoluzione dei conflitti che rovina il codice. Verifica: il file è identico ad af8f8ec, già revisionato in #539/#540, e l'AST è ok. Esito: ok.
- `tests/test_unit_web_lexbor.py:106` — casi dello shadow DOM dichiarativo (open, closed, OPEN con slot nominato). Rischio: perdere i test della fetta 23 nel merge. Verifica: il file è identico ad af8f8ec, e `pytest tests/test_unit_claude_cli.py tests/test_unit_web_lexbor.py` dà 125 passed. Esito: ok.
- Contesto (file non nel diff di sessione) — `gas.py:4912` chiama `_motivo_forte(e)` nel ramo `except`, seguito da `continue` verso il brain successivo: il fallback §9 è intatto. `git diff 0a9ce70 HEAD -- gas.py brains tests/test_unit_kernel.py tests/test_unit_claude_cli.py` è vuoto, cioè questi file sono identici a main (già revisionati in #538/#539 chat Motore). Esito: ok.
- `.claude/agents/memoria_revisore.md` — rispetto a main ci sono solo righe aggiunte: #539 Mani con la sua lezione, #540 Mani, #541. Nessuna riga persa. Esito: ok.
- `reports/stato_progetto.md` — la catena «Ultimo aggiornamento» è unita senza perdite. Ci sono sia la voce RIPARTENZA Motore sia la voce fetta 23 Mani. Non ci sono marcatori di conflitto. Esito: ok.

**Rischio escluso:** non ho rieseguito la suite kernel completa. Tu dichiari 1056 PASS e 1 FAIL (T31g, per `sqlite_vec` assente: noto). Il codice del motore è identico a main già testato, come mostrano i diff vuoti qui sopra. Non ho verificato nemmeno la suite web completa oltre i 125 test indicati sopra.

**Note fuori perimetro, non bloccanti**
- `reports/handoff.md` ha preso una riga da main nel merge automatico. È innocua e si riscrive al fine-task.
- Il doppio numero #538/#539 tra chat Mani e chat Motore è già tracciato come R-539-1 COSMETICA (chat Motore).

**Memoria:** la riga #541 c'è già in `/home/user/Gas/.claude/agents/memoria_revisore.md` (una sola occorrenza). Come mi hai chiesto, non ho aggiunto nulla.

Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py; toccati solo `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py`.
- Web suite (`tests/test_unit_web_*.py`, Python 3.13.16 con selectolax 1.0.2): prima 521 passed / 1 skipped (main 297fc22) → dopo 537 passed / 1 skipped (+16: 6 casi nel test «come il browser», 10 in `test_shadow_dichiarativo_in_ordine`).
- File lexbor su Python 3.11 senza selectolax (come la CI): 20 passed / 76 skipped.
- Suite vecchia con `GAS_WEB_LEXBOR=1` (`tests/test_unit_web_leggi.py`): 11 failed / 430 passed / 1 skipped prima e dopo, gli stessi 11 (fuori scope: casi dove la lettura di sempre e lexbor differiscono, noti dalla fetta 19).
- Dopo il merge di main 0a9ce70: web + claude_cli 566 passed / 1 skipped; kernel (`tests/test_unit_kernel.py`) 1056 PASS, 1 FAIL — T31g (sqlite_vec assente in questo ambiente, fuori scope, noto).
- Mutanti: tutti presi tranne `CON_SHADOW = True` (cambia solo i tempi); elenco in `reports/ultimo_report.md`.

## §6 STATO CI

CI NON VERIFICATA con `gh` (assente/non autenticato nel cloud). Check run lette dall'integrazione GitHub sulla PR #288:
- Head af8f8ec: `handoff-check` success; `verifica-bot` failure (V-1 MEDIA: conflitto con main, chiusa col merge 5ff6ad7); `unit-suite` in corso alla lettura.
- Head 16cb6a6: `handoff-check` failure atteso (run 40738191089: l'handoff era ancora quello della #285).

Mappatura commit→run:
- d553ca2, 484982b: nessuna run su questo SHA (pushati insieme a 16cb6a6).
- 16cb6a6: run 40738191089.
- af8f8ec: run del push del fine-task (check sopra).
- 5ff6ad7, 4021d67 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo l'albero del commit di testa).

## §7 RISERVE APERTE

- R-540-1 COSMETICA (review #540): uno slot dentro `<svg><foreignObject>` nello shadow non reclama il nome; svg è nascosto per scelta.
- R-ve280-1 BASSA: i test del figlio lexbor con selectolax non girano nei check required (CI su 3.11 senza selectolax). Chat Motore: `selectolax==1.0.2` in requirements-dev.
- Restano quelle delle fette precedenti (stato_progetto, blocchi «Mani — fetta 20/21»): cosmetiche R-ve277-3 con R-529-1, R-ve277-4, R-528-3, R-526-1, R-520-4.
