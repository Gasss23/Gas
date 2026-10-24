# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-24 — Chat Mani, fetta 15: </template> sopra svg/math come il browser (R6)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 15: solo con verdetto del bot APPROVATO puro sull'head finale e CI verde, oppure con il tuo ok.
2. **R-ve252-2 e R-ve255-1 (BASSE, XHTML malformato)**: estendere «il resto della pagina se ne va» a tutto l'XHTML malformato? Decidi tu.
3. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; serve un vero costruttore HTML5 (es. lexbor): decidi tu. Con questa fetta si vede anche dopo un template chiuso.
4. Rete a 12 s invece di 15 (fetta 14): confermi?
5. **R-ve235-7**: proposta di chiuderla come compromesso accettato (il DNS di sistema non si può interrompere; al massimo 4 risoluzioni appese).
6. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

---

## §1 SCOPE & ESITO FETTE

- **R-469-1** (`</template>` sopra svg/math): `FATTA`, con **B-500-1** (ALTA, dal revisore): `FATTA`
- **V-1 ve #257** (test dei redirect rotti): `FATTA`
- **V-1 bot / V-2 ve #257** (commento di TIMEOUT_TOTALE): `FATTA`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +
 modules/web/leggi.py               |  25 ++++-
 reports/diff_sessione.md           |  11 +-
 reports/handoff.md                 | 216 ++++++++++++++++---------------------
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  29 +++--
 tests/test_unit_web_leggi.py       |  50 +++++++++
 7 files changed, 191 insertions(+), 145 deletions(-)
```

NB: preso dall'index con tutti i report in stage, dopo aver scritto questo handoff; solo la riga di `reports/handoff.md` può differire di poche righe, perché lo stat è dentro il file stesso.

---

## §3 GIT LOG --ONELINE (sessione)

```
a2a8ef2 feat(web): fetta 15 — </template> sopra svg/math come il browser, redirect rotti di rete (R6)
e6ebab8 chore(revisore): memoria review #501 — APPROVATO
ec744dd chore(revisore): memoria review #500 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Due verdetti, incollati integralmente (chat Mani), tutti e due sul diff della fetta 15 committato in `a2a8ef2`: #500 (BOCCIATO, B-500-1) sulla prima versione, #501 (APPROVATO) col rimedio. Le righe citate nella #500 si riferiscono al diff di allora.

### Review #500 (chat Mani) — verdetto integrale (fetta 15, prima versione)

## VERDETTO: BOCCIATO

Review #500 (chat Mani), fetta 15 sul ramo feat/mani-web-fetta15 (da main 172c2d7). Il numero #500 era libero: il più alto in memoria era #499. La regola nuova su `</template>` fa uscire testo nascosto che main nascondeva, sia nel parser sia nel ripiego.

**Motivo del blocco: B-500-1 (ALTA, fuga nuova rispetto a main)**
- `modules/web/leggi.py:405`: la regola scatta quando `aperti["template"] > 0`. Quel conteggio però include anche i `<template>` svg/math.
  - `_esci` li toglie dalla pila senza scalarli («restano contati»).
  - Se l'uscita si ferma su un punto di integrazione (foreignObject, desc, mi), la pila non è vuota e non diventa incerta.
  - Di conseguenza `_chiudi_template` (`modules/web/leggi.py:383`, ramo riuscito a `modules/web/leggi.py:394`) chiude un template HTML che il browser non ha: svuota la pila e scala svg e template.
- Sonde sul codice in stage: SEGRETO esce sia dal parser sia dal ripiego. Su main 172c2d7 e con lexbor resta nascosto (danno solo «A»):
  - `<p>A</p><svg><foreignObject><svg><template><div></template>SEGRETO`
  - `<p>A</p><svg><foreignObject><svg><template><p>x</p></template>SEGRETO`
  - `<p>A</p><math><mi><svg><template><div></template>SEGRETO`
  - `<p>A</p><svg><desc><math><template><b>x</b></template>SEGRETO`
- Perché le tue prove non lo hanno visto: servono 6 atomi (svg, foreignObject, svg, template, div, /template). L'enumerazione a 4 non poteva arrivarci, e il campione a 6 era troppo rado.
- Rimedio provato in una copia isolata, la cartella rev500/cp:
  - nuovo contatore `_template_fuori` in `_Contesto`, che conta solo i template HTML aperti con la pila vuota;
  - +1 in `apri` quando la pila è vuota e il tag è template;
  - −1 in `chiudi` quando la pila è vuota, prima del `return`, e nel ramo riuscito di `_chiudi_template`;
  - la regola usa `self._template_fuori > 0` al posto di `self._aperti.get("template", 0) > 0`.
  - Risultato: le 4 sonde nascondono SEGRETO, le altre 6 (compresi i rischi che chiedevi) danno lo stesso testo di lexbor, il caso base `<p>A</p><template><svg></template>VIS` dà ancora «A VIS», e la suite resta verde (398 passed su 3.13 e 3.11).
- Da fare: aggiungere le 4 sonde ai test e rifare l'enumerazione con lexbor usando prefissi fissi (`svg foreignObject svg`, `svg desc math`, `math mi svg`) seguiti da template.

**I rischi che chiedevi di guardare**
- Template dentro un punto di integrazione, cioè template HTML nella pila: la regola non scatta e vale il percorso di prima. Ok.
- Svg con un elemento chiamato «template»: sta in `_posizioni`, quindi la regola non scatta, e `</template>` lo chiude per nome come fa il browser. Ok.
- `</p>` e `</br>` che svuotano la pila: svg e math restano contati, quindi il testo resta nascosto come in lexbor (sonda `<svg><template></p><svg></template>SEGRETO` → «A»). Ok, ma solo grazie alla sovrastima di svg: il rimedio lo rende indipendente da questa.
- Il ripiego usa lo stesso `_Contesto`, quindi ha la stessa fuga, e il rimedio vale anche per lui.

**Cosa va bene**
- `tests/test_unit_web_leggi.py:439` (V-1 della verifica esterna #257): i redirect rotti restano «errore di rete o di protocollo (…)». Ok.
- `tests/test_unit_web_leggi.py:995`: i casi della regola sono giusti, ma non contengono la sonda del blocco.
- Il commento di TIMEOUT_TOTALE è allineato alla docstring. Ok.
- Suite web: 398 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Cosa non ho verificato**
- I casi con noscript: lexbor ha gli script spenti e non può fare da oracolo. Il controllo su `_nascosti_html` l'ho solo letto.
- La suite col parser vecchio (389 passed e 10 skipped).
- La tua enumerazione completa: le cifre (707 mila pagine a 4 atomi, 600 mila a 6) sono tue.

**Memoria**: aggiunte la riga #500 e una lezione (una regola che toglie il nascondimento non deve fidarsi di `aperti`, che mescola HTML e svg/math e contiene sovrastime). Committate con `scripts/commit_memoria_revisore.sh` (commit ec744dd). Lo stage non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev500/sonde.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev500/sonde2.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev500/cp/modules/web/leggi.py (copia con il rimedio)

### Review #501 (chat Mani) — verdetto integrale (fetta 15 dopo B-500-1)

## VERDETTO: APPROVATO

Review #501 (chat Mani), ri-review della #500 sul diff in stage della fetta 15. B-500-1 è chiusa: le pagine che con la #500 facevano uscire SEGRETO ora lo nascondono, come main e lexbor. Il numero #501 era libero: il più alto in memoria era #500.

**Cosa ho esaminato**
- `modules/web/leggi.py:235` e `modules/web/leggi.py:413`: il contatore `_template_fuori`, che conta solo i template HTML aperti con la pila vuota, e la regola che ora usa quello invece di `aperti`.
  - Rischio esaminato: differenze rispetto al rimedio che avevo provato nella #500.
  - Esito ok: confrontato con la mia copia rev500/cp, cambiano solo il commento e l'ordine di due blocchi indipendenti dentro `apri`.
  - Gli altri due punti del contatore, cioè il −1 a pila vuota (riga 411) e il −1 quando il template si chiude (riga 399), sono come nel rimedio.
- Sonde sul codice in stage, sia parser sia ripiego:
  - le 4 del blocco (`svg>foreignObject>svg`, `math>mi>svg`, `svg>desc>math` con template, più la variante con `<p>`) danno «A», come lexbor;
  - le 6 della #500 hanno lo stesso esito di lexbor, compreso il caso base `<p>A</p><template><svg></template>VIS`, che dà «A VIS».
- I due test sui decrementi.
  - Rischio esaminato: il contatore che resta sbilanciato.
  - Esito ok:
    - `<template></template><svg></template>SEGRETO` dà «A»;
    - `<template><svg></template>VIS<svg></template>SEGRETO` dà «A VIS». Su main dava «A», quindi è una perdita tolta, ed è anche l'esito di lexbor.
- `tests/test_unit_web_leggi.py:993`: la prima sonda del blocco è ora nei test. Le mutazioni le hai fatte tu (mut15/run.py); il mutante «conta `aperti`» è esattamente il codice della #500, che con queste sonde faceva uscire SEGRETO.
- Suite web: 405 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Sulle 4 «regressioni» col prefisso `<template><svg><foreignObject>`**
- Sono della classe già nota R-ve246-5 (canvas con dentro un div), non una fuga nuova.
- Prova: `<p>A</p><canvas> W1 <div> W2 </canvas> W3` mostra W3 già su main 172c2d7, anche senza prefisso.
- Col prefisso, main nascondeva W3 solo perché nascondeva tutto quello che seguiva `</template>`. A chi scrive la pagina il codice nuovo non dà nessuna possibilità in più.
- La riserva R-ve246-5 resta aperta com'era.

**Cosa non ho verificato**
- Le enumerazioni lexbor con i prefissi fissi (707 mila pagine per prefisso): le cifre sono tue, io ho rifatto solo le sonde mirate.
- La suite col parser vecchio (396 passed e 10 skipped).
- I casi con noscript: lexbor ha gli script spenti e non può fare da oracolo.

**Memoria**: aggiunta la riga #501, nessuna lezione nuova. Committata con `scripts/commit_memoria_revisore.sh` (commit e6ebab8). Lo stage non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev500/sonde3.py

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 388 → 405 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «405 passed, 1 skipped» su Python 3.13 e 3.11; lo skip è il test d'allarme che gira solo in CI). Col html.parser non patchato di CPython 3.12.3 caricato da plugin: 396 passed, 10 skipped.
- Oracolo lexbor (scripting spento, quindi niente noscript negli atomi), nuovo contro main 172c2d7, parser e ripiego, 29 atomi: enumerazione esaustiva a 4 atomi senza prefisso (707.281 pagine) e con 6 prefissi fissi (707.281 ciascuno), campione a 6 atomi (600.000): 0 perdite nuove; 0 regressioni salvo 4 casi col prefisso `<template><svg><foreignObject>`, tutti della classe R-ve246-5 (canvas/object con un div dentro), identici su main senza prefisso; perdite tolte: oltre 67.000.
- Mutazioni in copie isolate (scratchpad/mut15/run.py): senza regola 6 FAIL, senza controllo dei nascosti HTML 1 FAIL, regola che conta `aperti` (codice della #500) 4 FAIL, contatore che non scende a pila vuota 1 FAIL, che non scende chiudendo 1 FAIL, flag di rete spento subito dopo `_scarica` 2 FAIL.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

- `a2a8ef2` e il commit di fine-task con questo handoff: run non ancora disponibili alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Restano: **R-ve252-2** e **R-ve255-1** BASSE (XHTML malformato, da decidere), **R-ve246-5** MEDIA preesistente (canvas/object, decisione sul costruttore HTML5), R-ve235-7 (proposta: accettata), R-ve245-2…4, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…15».
