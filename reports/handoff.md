# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Mani fetta 23: shadow DOM dichiarativo letto come il browser nel figlio lexbor ; secondo giro (merge di main) e terzo giro (verifica esterna) (chat Mani)

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
- **Terzo giro — verifica esterna su af8f8ec APPROVATO CON RISERVE** (commento: https://github.com/Gasss23/Gas/pull/288#issuecomment-6476568410); bot su a735e46 APPROVATO CON RISERVE (V-1 cosmetica: §6 vecchio):
  - V-1 ve MEDIA (conflitto con main): `FATTA` col merge 5ff6ad7 (secondo giro).
  - V-2 ve BASSA (`x-a!`, `x-a:b` presi per host): `SALTATA — non accolta`: riletta alla fonte (whatwg/html «valid custom element name», whatwg/dom «valid element local name» e «valid shadow host name»), per lo standard di oggi sono host validi. Il primo fix con la regola vecchia PotentialCustomElementName è stato BOCCIATO (review #542) e tolto; in fe1c9b0 test «ST» e commento con la fonte, review #543 APPROVATO.
  - V-3 ve BASSA (mutante del template dello shadow tra gli assegnati): `FATTA` — non equivalente (con `slot=n` toglieva la riserva); test «R» in fe1c9b0. Parte R-ve280-1: `DEFERITA — chat Motore`.
  - V-4 ve e V-1 bot COSMETICHE (§6 vecchio): `FATTA` — §6 riscritto qui sotto.
  - R-543-1 COSMETICA (commento su HOST: «niente maiuscole» vale solo per A-Z): `DEFERITA — cosmetica`.
- **Accensione lexbor (punto b della ripartenza)**: `DEFERITA — chat Motore, selectolax non ancora in requirements su main`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++++
 modules/web/lexbor.py              |  96 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 reports/diff_sessione.md           |  17 ++++++++---------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   6 +++---
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  45 +++++++++++++++++++++++++++++++++------------
 tests/test_unit_web_lexbor.py      |  52 ++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: base = merge-base con origin/main = 0a9ce70. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
fe1c9b0 fix(web): template dello shadow fuori dagli assegnati fissato da un test; host secondo lo standard di oggi (V-2, V-3 ve #288)
e272522 chore(revisore): memoria review #543 — APPROVATO
212ab4f chore(revisore): memoria review #542 — BOCCIATO
a735e46 docs(fine-task): verdetto #541 riemesso dal revisore per il Gate B (PR #288)
4021d67 docs(fine-task): PR #288 dopo il merge di main 0a9ce70 — handoff e report, review #541
5ff6ad7 Merge origin/main (0a9ce70, PR #287) in claude/peaceful-lovelace-0w2b7q (PR #288)
af8f8ec docs(fine-task): Mani fetta 23 — shadow DOM dichiarativo, handoff e report (PR #288)
16cb6a6 feat(web): shadow DOM dichiarativo letto come il browser nel figlio lexbor (fetta 23 Mani)
484982b chore(revisore): memoria review #540 — APPROVATO
d553ca2 chore(revisore): memoria review #539 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore 16cb6a6: review #539 sul primo diff staged, #540 dopo la chiusura di R-539-1 e R-539-2 (diff committato in 16cb6a6). Merge 5ff6ad7 (da main entrano gas.py, brains/claude_cli.py e i loro test): review #541. Commit motore fe1c9b0: review #542 BOCCIATO sul primo diff (V-2 con la regola vecchia), #543 APPROVATO sul diff corretto. Verdetti integrali:

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

### Review #542 (chat Mani) — primo diff staged per V-2/V-3 ve #288

## VERDETTO: BOCCIATO

Review #542 (chat Mani) sul diff staged del branch claude/peaceful-lovelace-0w2b7q (PR #288, HEAD a735e46). Ho letto CLAUDE.md (sezioni 5, 8 e 10), reports/stato_progetto.md (in modo selettivo) e la mia memoria. Il diff non tocca la history, non simula tool e non indebolisce nessun guardrail. Il blocco riguarda la correttezza rispetto allo standard.

**Motivo bloccante (V-2): il fix applica una regola dello standard che non esiste più.**
- Ho riletto alla fonte lo standard HTML (sorgente di whatwg/html su main, scaricato oggi da raw.githubusercontent.com) e lo standard DOM (whatwg/dom main, dom.bs). La produzione PotentialCustomElementName non c'è più. Oggi un nome è un «valid custom element name» se:
  - è un «valid element local name» del DOM: se inizia con una lettera ASCII, non deve contenere spazi ASCII, NUL, «/» o «>»;
  - inizia con una lettera da a a z;
  - non contiene lettere maiuscole A-Z;
  - contiene un trattino;
  - non è uno degli 8 nomi riservati.
- Lo standard DOM definisce «valid shadow host name» come un valid custom element name oppure uno dei 18 tag della lista. Quindi `x-a!`, `x-a:b` e `x-a😍` oggi sono host validi.
- Il controllo di prima (trattino + iniziale a-z, con il tag che il tokenizer consegna già in minuscolo, senza spazi, «/» o «>» e con NUL sostituito da U+FFFD) coincideva con lo standard attuale. L'ho provato con selectolax 1.0.2: `<x-A>` diventa `x-a`, NUL diventa U+FFFD, `x-a!` e `x-a:b` restano così.
- La verifica esterna #288 aveva scritto nel suo «NON VERIFICATO» di aver citato il nome valido a memoria, senza rileggerlo dalla fonte.
- Correzione da fare: togliere `CUSTOM` e `import re` e tornare al controllo di prima. Il caso `x-a!`/`x-a:b` va tenuto come test con l'esito dello standard attuale («ST», non «LM»), con un commento che rimandi a «valid element local name». Su V-2 della verifica esterna va risposto citando la fonte.

**Elementi del diff esaminati**
- `modules/web/lexbor.py:150` — la regex `CUSTOM` dei caratteri ammessi nel nome. Rischio: intervalli sbagliati. Ho confrontato tutti i code point da 0 a 0x10FFFF con la vecchia lista PCENChar: 0 differenze, quindi gli intervalli sono esatti. Contro lo standard attuale invece divergono 142.472 code point (tutta la punteggiatura ASCII, i controlli, U+F0000 e oltre). — **blocco**
- `modules/web/lexbor.py:179` — la condizione di host, ora `"-" in tag and CUSTOM.fullmatch(tag)`. Rischio: divergere dal browser. Con lo standard attuale, sulla pagina `<x-a!><template shadowrootmode=open>S</template>L</x-a!>` il browser mostra «S» e Gas ora legge «L»: è proprio il verso che la verifica esterna voleva evitare (testo che l'utente non vede dato all'agente, testo visibile tolto all'agente). — **blocco**
- `tests/test_unit_web_lexbor.py:151` — il test che si aspetta «LM» per `x-a!` e `x-a:b`. Rischio: fissare come «browser» un comportamento obsoleto. Per lo standard attuale l'esito giusto è «ST». — **blocco**
- `tests/test_unit_web_lexbor.py:153` — `x.y-é` letto come host («S»). Valido con entrambe le regole. — ok
- `modules/web/lexbor.py:196` con `tests/test_unit_web_lexbor.py:156` — V-3: il template dello shadow non conta tra i figli assegnati agli slot. Per lo standard il template dichiarativo va solo sulla pila del parser («insert a foreign element» con only-add-to-element-stack), non nel DOM, quindi «R» è corretto. Mutante `luce.mem_id != figlio.mem_id` → `True`: 1 failed, poi file ripristinato (nessuna modifica rimasta fuori dallo staging). Commento aggiornato e corretto. — ok
- Prove mie (Python 3.13, selectolax 1.0.2): tests/test_unit_web_lexbor.py dà 99 passed.

**Rischi esplicitamente esclusi**
- Cosa fanno oggi i browser veri (Chromium, Firefox, Safari) con i nomi «larghi»: non l'ho verificato. Non c'è un browser in questo ambiente, html.spec.whatwg.org risponde 403 dal proxy e l'API di ricerca GitHub è limitata al repo, quindi non ho trovato la data del cambio dello standard né lo stato di implementazione. Il giudizio si basa sullo standard vivo letto alla fonte. Se l'operatore preferisce seguire un browser che implementa ancora PCEN, è una decisione sua, ma allora il commento e il test non possono dire «dello standard».
- Non ho rieseguito la suite web completa, la suite vecchia con GAS_WEB_LEXBOR=1, il caso Python 3.11 senza selectolax e la misura dei 50k host: il diff non tocca quei percorsi oltre la riga 179.

**Memoria**: aggiunte la riga #542 e una lezione (rileggere alla fonte un finding che cita lo standard «a memoria»; whatwg/html e whatwg/dom su raw.githubusercontent.com sono raggiungibili dal proxy). Commit 212ab4f fatto con scripts/commit_memoria_revisore.sh; lo staging del diff sotto review non è stato toccato.

File: /home/user/Gas/modules/web/lexbor.py, /home/user/Gas/tests/test_unit_web_lexbor.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #543 (chat Mani) — diff committato in fe1c9b0

## VERDETTO: APPROVATO

Review #543 (chat Mani): la correzione della bocciatura #542 chiude il motivo bloccante. Il controllo del nome host torna a seguire lo standard di oggi e V-3 resta fissato da un test. Il diff non tocca la history, non simula tool e non indebolisce nessun guardrail.

**Elementi del diff esaminati**
- `modules/web/lexbor.py:62` — `import re` tolto insieme a `CUSTOM`. Rischio: un uso di `CUSTOM` rimasto. Grep: nessuna occorrenza. — ok
- `modules/web/lexbor.py:177` — di nuovo trattino + iniziale a-z. Rischio: divergere dal browser. Coincide con lo standard attuale: «valid custom element name» di HTML più «valid element local name» di DOM, riletti alla fonte nella #542. Il tokenizer consegna il tag in minuscolo, senza spazi, «/» o «>», e con NUL già sostituito da U+FFFD. Mutante che ammette nel nome solo lettere, cifre, punto e trattino: 1 failed, poi file ripristinato (nessuna modifica rimasta fuori dallo staging). — ok
- `modules/web/lexbor.py:143` — commento su HOST con la fonte. Rischio: commento impreciso. Dice «niente maiuscole» senza precisare che vale solo per A-Z (le maiuscole non ASCII sono ammesse). — riserva cosmetica, non blocca (R-543-1)
- `tests/test_unit_web_lexbor.py:151` — `x-a!` e `x-a:b` ora si aspettano «ST», l'esito dello standard di oggi. — ok
- `tests/test_unit_web_lexbor.py:156` — V-3: template dello shadow con `slot=n` → «R». Il template dichiarativo non entra nel DOM; il mutante l'avevo già verificato nella #542 (1 failed). — ok

**Prove mie**
- tests/test_unit_web_lexbor.py: 99 passed su Python 3.13 con selectolax; 20 passed / 79 skipped su 3.11 senza selectolax.
- Test web (`-k web`): 541 passed / 1 skipped.

**Rischi esplicitamente esclusi**
- Come si comportano i browser veri con i nomi «larghi»: non verificabile qui (nessun browser, html.spec.whatwg.org risponde 403 dal proxy). Il giudizio si basa sullo standard vivo letto alla fonte.
- Non ho rieseguito la suite vecchia con GAS_WEB_LEXBOR=1 né la misura dei 50k host: rispetto a main il codice di quei percorsi torna identico, salvo i commenti.

**Riserva da tracciare in stato_progetto.md**
- R-543-1 COSMETICA: precisare nel commento su HOST che «niente maiuscole» vale solo per A-Z.

**Memoria**: aggiunta la riga #543 (nessuna lezione nuova), commit e272522 fatto con scripts/commit_memoria_revisore.sh; lo staging del diff sotto review non è stato toccato.

File: /home/user/Gas/modules/web/lexbor.py, /home/user/Gas/tests/test_unit_web_lexbor.py, /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py; toccati solo `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py`.
- Web suite (`tests/test_unit_web_*.py`, Python 3.13.16 con selectolax 1.0.2): prima 521 passed / 1 skipped (main 297fc22) → dopo 537 passed / 1 skipped (+16: 6 casi nel test «come il browser», 10 in `test_shadow_dichiarativo_in_ordine`).
- File lexbor su Python 3.11 senza selectolax (come la CI): 20 passed / 76 skipped.
- Suite vecchia con `GAS_WEB_LEXBOR=1` (`tests/test_unit_web_leggi.py`): 11 failed / 430 passed / 1 skipped prima e dopo, gli stessi 11 (fuori scope: casi dove la lettura di sempre e lexbor differiscono, noti dalla fetta 19).
- Dopo il merge di main 0a9ce70: web + claude_cli 566 passed / 1 skipped; kernel (`tests/test_unit_kernel.py`) 1056 PASS, 1 FAIL — T31g (sqlite_vec assente in questo ambiente, fuori scope, noto).
- Dopo V-2/V-3 (fe1c9b0): web suite 540 passed / 1 skipped (+3 casi); lexbor su 3.11 senza selectolax 20 passed / 79 skipped; suite vecchia con `GAS_WEB_LEXBOR=1` sempre 11 failed / 430 passed; mutante «template tra gli assegnati» ora preso (1 failed).
- Mutanti: tutti presi tranne `CON_SHADOW = True` (cambia solo i tempi); elenco in `reports/ultimo_report.md`.

## §6 STATO CI

CI NON VERIFICATA con `gh` (assente/non autenticato nel cloud). Check run lette dall'integrazione GitHub sulla PR #288:
- Head a735e46: run 40739978887 con `unit-suite` e `handoff-check` success; `verifica-bot` success (verdetto testuale APPROVATO CON RISERVE, V-1 cosmetica = questo §6, riscritto).
- Head af8f8ec: run 40738586125 con `unit-suite` success, `handoff-check` success; `verifica-bot` failure (V-1 MEDIA conflitto, chiusa col merge 5ff6ad7).
- Head 16cb6a6: run 40738191089, `handoff-check` failure atteso (handoff ancora della #285).

Mappatura commit→run:
- d553ca2, 484982b: nessuna run su questo SHA (pushati insieme a 16cb6a6).
- 16cb6a6: run 40738191089.
- af8f8ec: run 40738586125.
- 5ff6ad7, 4021d67: nessuna run su questo SHA (pushati insieme a a735e46).
- a735e46: run 40739978887.
- 212ab4f, e272522, fe1c9b0 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo l'albero del commit di testa).

## §7 RISERVE APERTE

- R-543-1 COSMETICA (review #543): nel commento su HOST «niente maiuscole» vale solo per A-Z.
- R-540-1 COSMETICA (review #540): uno slot dentro `<svg><foreignObject>` nello shadow non reclama il nome; svg è nascosto per scelta.
- R-ve280-1 BASSA (anche V-3 ve #288): i test del figlio lexbor con selectolax non girano nei check required (CI su 3.11 senza selectolax). Chat Motore: `selectolax==1.0.2` in requirements-dev.
- V-2 ve #288: non accolta (standard di oggi riletto alla fonte, vedi §1); da confermare all'operatore.
- Restano quelle delle fette precedenti (stato_progetto, blocchi «Mani — fetta 20/21»): cosmetiche R-ve277-3 con R-529-1, R-ve277-4, R-528-3, R-526-1, R-520-4.
