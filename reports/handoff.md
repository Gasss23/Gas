# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-24 — Chat Mani, fetta 15: </template> sopra svg/math come il browser (R6)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 15: solo con verdetto del bot APPROVATO puro sull'head finale e CI verde, oppure con il tuo ok.
2. **R-ve252-2 e R-ve255-1 (BASSE, XHTML malformato)**: estendere «il resto della pagina se ne va» a tutto l'XHTML malformato? Decidi tu.
3. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; serve un vero costruttore HTML5 (es. lexbor): decidi tu. Con questa fetta si vede anche dopo un template chiuso.
3b. **R-ve261-2 (MEDIA, già presente, nuova riserva)**: Gas legge i tag dentro noscript, il browser con gli script attivi no; chiuderla vuol dire leggere noscript come testo grezzo (cambia cosa si vede delle pagine con noscript): decidi tu se farlo nella prossima fetta.
4. Rete a 12 s invece di 15 (fetta 14): confermi?
5. **R-ve235-7**: proposta di chiuderla come compromesso accettato (il DNS di sistema non si può interrompere; al massimo 4 risoluzioni appese).
6. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

---

## §1 SCOPE & ESITO FETTE

- **R-469-1** (`</template>` sopra svg/math): `FATTA`, con **B-500-1** (ALTA, dal revisore): `FATTA`
- **V-1 ve #257** (test dei redirect rotti): `FATTA`
- **V-1 bot / V-2 ve #257** (commento di TIMEOUT_TOTALE): `FATTA`
- **Secondo giro, bot e verifica esterna #261 BOCCIATO**: V-1 ALTA (noscript fuori dalla pila, forme a e b) `FATTA`; V-2 ve MEDIA preesistente registrata come R-ve261-2; V-3/V-4 ve BASSE `FATTA`
- **Terzo giro, seconda verifica esterna #261 BOCCIATO**: V-1 ALTA (classe noscript) `FATTA` a livello di pagina; V-2 BASSA (test) `FATTA`; V-3/V-4 `FATTA`; bot #261 su c16487c APPROVATO CON RISERVE (note corrette)

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   8 +
 modules/web/leggi.py               |  36 ++++-
 reports/diff_sessione.md           |  11 +-
 reports/handoff.md                 | 315 ++++++++++++++++++++++++-------------
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  32 ++--
 tests/test_unit_web_leggi.py       |  69 ++++++++
 7 files changed, 345 insertions(+), 128 deletions(-)
```

NB: preso dall'index con tutti i report in stage, dopo aver scritto questo handoff; solo la riga di `reports/handoff.md` può differire di poche righe, perché lo stat è dentro il file stesso.

---

## §3 GIT LOG --ONELINE (sessione)

```
955607c fix(web): fetta 15 — regola del template spenta nelle pagine con noscript (V-1/V-2 ve #261 bis)
f55b732 chore(revisore): memoria review #504 — APPROVATO
c16487c docs(reports): fetta 15 chat Mani, secondo giro — report, handoff, stato
837fcd1 fix(web): fetta 15 — noscript e </template> (V-1 bot #261, V-1 ve #261)
faf29a1 chore(revisore): memoria review #503 — APPROVATO
9efd6b1 chore(revisore): memoria review #502 — APPROVATO
3b50ee1 docs(reports): fine fetta 15 chat Mani — report, handoff, stato
a2a8ef2 feat(web): fetta 15 — </template> sopra svg/math come il browser, redirect rotti di rete (R6)
e6ebab8 chore(revisore): memoria review #501 — APPROVATO
ec744dd chore(revisore): memoria review #500 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Cinque verdetti, incollati integralmente (chat Mani): #500 (BOCCIATO, B-500-1) e #501 (APPROVATO) sul diff della fetta 15 committato in `a2a8ef2`; #502 e #503 (APPROVATO) sul secondo giro (noscript, V-1 bot e verifica esterna #261) committato in `837fcd1`; #504 (APPROVATO) sul terzo giro (noscript a livello di pagina) committato in `955607c`. La #504 sostituisce i controlli della #502 e della #503. Le righe citate nella #500 si riferiscono al diff di allora.

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

### Review #502 (chat Mani) — verdetto integrale (V-1 ALTA bot #261, forma a)

## VERDETTO: APPROVATO

Review #502 (chat Mani), sul delta in stage della PR #261 (head 3b50ee1) per V-1 ALTA del bot #261. La fuga è chiusa: con un noscript aperto la pila torna incerta e il resto si nasconde, come su main. Il numero #502 era libero: il più alto in memoria era #501.

Lo segnalo: nella #501 ho approvato senza provare un nascosto HTML che sta fra il template e la pila. È proprio la fuga che il bot ha trovato. Ho aggiunto in memoria la lezione corrispondente.

**Cosa ho esaminato**
- `modules/web/leggi.py:397`, `_chiudi_template`: ora rende la pila incerta se c'è un qualsiasi noscript aperto (`aperti["noscript"]`), nella pila o fuori. Il controllo su `_nascosti_html` è tolto.
  - Rischi esaminati: un noscript in ciascuna delle tre posizioni (sopra la pila, fra il template e la pila, sotto il template), e cosa cambia togliendo `_nascosti_html`.
  - Esito ok. Sonde sul codice in stage, sia parser sia ripiego:
    - `<template><noscript><svg></template></noscript>LEAK` → «A»;
    - la variante con SEGRETO dentro il noscript → «A»;
    - `<noscript><template><svg></template>SEGRETO` → «A»;
    - `<template><svg><foreignObject><noscript></template>SEGRETO` → «A».
    - Tutti come main 172c2d7.
  - Il noscript già chiuso (`<template><noscript></noscript><svg></template>VIS`) dà «A VIS»: il conteggio torna a 0 e non blocca più.
  - Togliere `_nascosti_html` non apre fughe:
    - con gli script attivi, noscript è l'unico elemento della pila il cui contenuto è testo grezzo nel browser ma non in html.parser, ed è coperto dal conteggio;
    - object e canvas nella pila il browser li chiude insieme al template: `<template><svg><foreignObject><object></template>VIS` dà «A VIS»;
    - gli altri elementi a testo grezzo (style, script, iframe…) html.parser li legge già come testo, quindi `</template>` non arriva mai a `chiudi`.
  - Un conteggio di noscript gonfiato da un noscript svg porta solo a pila incerta e testo nascosto: verso sicuro.
- `tests/test_unit_web_leggi.py:1004`–`tests/test_unit_web_leggi.py:1008`: la sonda del bot, la variante, il noscript sotto il template e il noscript già chiuso.
  - Rischio esaminato: che la fuga possa tornare senza che un test se ne accorga. Esito ok.
  - La mutazione «senza noscript» (3 FAIL) l'hai fatta tu: non l'ho rifatta.
- B-500-1 resta chiusa: `<svg><foreignObject><svg><template><div></template>SEGRETO` dà «A».
- Suite web: 409 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Cosa non ho verificato**
- I casi noscript con un oracolo: lexbor ha gli script spenti. La sicurezza qui si basa sul ragionamento (con noscript aperto la pila diventa incerta, come su main), non su un confronto.
- Le enumerazioni lexbor con prefissi: le cifre sono tue.
- La suite col parser vecchio (400 passed e 10 skipped).
- `<template><object><svg></template>VIS` dà solo «A», mentre il browser mostrerebbe VIS: testo perso, non nascosto che esce. Era già dichiarato.

**Memoria**: aggiunte la riga #502 e una lezione (sondare i nascosti in tre posizioni: nella pila, fra il contenitore e la pila, sotto il contenitore). Committate con `scripts/commit_memoria_revisore.sh` (commit 9efd6b1). Lo stage non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev500/sonde4.py

### Review #503 (chat Mani) — verdetto integrale (V-1 ALTA verifica esterna #261, forma b)

## VERDETTO: APPROVATO

Review #503 (chat Mani), sul delta in stage della PR #261 per la verifica esterna #261. Il numero #503 era libero: il più alto in memoria era #502. Le due forme di V-1 ALTA sono chiuse: tutte le sonde danno lo stesso testo di main, salvo il caso base, che ora mostra VIS come il browser.

**Cosa ho esaminato**
- `modules/web/leggi.py:343`, in `apri` a pila vuota: un `<template>` non entra più in `_template_fuori` se c'è un noscript aperto.
  - Rischio esaminato: la forma (b) di V-1, cioè un template scritto dentro un noscript, che per il browser è testo, contato come vero e poi chiuso dalla regola.
  - Esito ok. Contare un template in meno può solo rendere la pila incerta più spesso, quindi va nel verso sicuro.
  - Sonde, sia parser sia ripiego, tutte uguali a main 172c2d7:
    - la sonda della verifica `<p>T0</p><noscript>T1<template>T2</noscript>T3…<svg>T7</template>T8` → «T0»;
    - `<noscript><template></noscript><svg></template>SEGRETO` → «A»;
    - `<template><noscript><template></noscript>B</template><svg></template>SEGRETO` → «A». Il template interno, scritto nel noscript, non si conta; il `</template>` a pila vuota scala quello esterno; poi la regola non scatta.
    - `<template><noscript></template></noscript><svg></template>X` → «A». Gas perde X, il browser lo mostrerebbe: testo perso, non nascosto che esce.
- `_chiudi_template`, cioè il delta della #502 (pila incerta con un noscript aperto): invariato e ancora in stage.
  - Rischio esaminato: la forma (a) di V-1. Esito ok: `<template><noscript><svg></template></noscript>LEAK` → «A».
  - Il caso base `<template><svg></template>VIS` dà «A VIS». B-500-1 resta chiusa.
- `tests/test_unit_web_leggi.py:1008`: le due forme della verifica sono nei test. La mutazione «template contato anche dentro noscript» (1 FAIL) l'hai fatta tu.
- Suite web: 411 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Riserve già note che restano aperte**
- **V-2 della verifica, preesistente (R-ve261-2)**: Gas legge i tag dentro un noscript, il browser no. Per esempio `<template><noscript></template>T1</noscript>T2` mostra T2. Va tenuta in stato_progetto.
- **La «regressione» canvas più template del tuo fuzz**: è la classe R-ve246-5. La stessa uscita c'è già su main senza svg, quindi non dà niente di nuovo a chi scrive la pagina.

**Cosa non ho verificato**
- Il fuzz con noscript sostituito da noembed nell'oracolo: le cifre sono tue (1,5 milioni di pagine).
- La suite col parser vecchio (402 passed e 10 skipped).
- Le pagine con frameset: lì il browser ignora tutto, e Gas mostra comunque il testo. È un problema preesistente e più generale, non legato al template.

**Memoria**: aggiunta la riga #503, nessuna lezione nuova: è un'applicazione di quella della #502 (noscript sotto il contenitore). Committata con `scripts/commit_memoria_revisore.sh` (commit faf29a1). Lo stage non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev500/sonde5.py

### Review #504 (chat Mani) — verdetto integrale (noscript a livello di pagina, seconda verifica esterna #261)

## VERDETTO: APPROVATO

Review #504 (chat Mani), sul delta in stage della PR #261 (head c16487c) per la seconda verifica esterna #261. Il numero #504 era libero: il più alto in memoria era #503. La regola su `</template>` ora si spegne in tutte le pagine che contengono `<noscript`, quindi lì Gas segue riga per riga il percorso di main. Questo chiude la classe trovata dalla verifica, non solo le sue sonde.

**Cosa ho esaminato**
- `modules/web/leggi.py:414`: la regola in `chiudi` scatta solo se `not self.con_noscript`.
  - Rischio esaminato: V-1 ALTA. I controlli puntuali della #502 e della #503 lasciavano passare una classe di pagine con noscript; la verifica ne ha trovate 82.
  - Esito ok:
    - con noscript nella pagina `_chiudi_template` non viene mai chiamata e il percorso è quello di main;
    - senza noscript il codice è quello approvato nella #501;
    - `apri` e `_chiudi_template` sono tornati come nella #501.
  - Sonde, sia parser sia ripiego, tutte con lo stesso testo di main 172c2d7:
    - P2 `<template><svg></template><template><noscript></template></noscript>T6x` → «T0x»;
    - P1 → «A»;
    - V-2 `<template>T1<svg>T2<template>T3</template>T4` → «A»;
    - `<NOSCRIPT>` maiuscolo → «A»;
    - `<!-- <noscript -->` in un commento → «A». È una perdita voluta: la regola si spegne anche se noscript compare solo in un commento.
    - B-500-1 resta chiusa.
  - Senza noscript il caso base `<template><svg></template>VIS` dà ancora «A VIS».
- Dove si accende il flag: `modules/web/leggi.py:959` nel parser (`feed`) e `modules/web/leggi.py:1124` nel ripiego. Sui rischi che chiedevi:
  - **`feed` chiamato più volte**: in Gas avviene una volta sola, con la pagina intera, quindi un `<noscript` non può restare spezzato fra due chiamate. `close()` non passa da `feed` ma non ne ha bisogno.
  - **XHTML**: `_Contesto.apri` e `chiudi` si usano solo se la pagina non è XHTML, sia nel parser sia nel ripiego. Quindi il testo già passato da `_commenti_e_cdata_xml` non conta per questa regola.
  - **`<noscript` dentro commenti o attributi**: accende il flag e porta solo a più testo nascosto, mai meno.
  - **Maiuscole e minuscole**: `re.IGNORECASE` senza ASCII riconosce più forme di quelle che il browser considera noscript (per esempio `noſcript`, con la s lunga). Anche questo porta solo a nascondere di più. Il contrario non può succedere: ogni noscript vero si scrive `<noscript` con lettere ASCII, e la regex lo trova sempre.
- Test nuovi: P1, P2 e P3, le 2 pagine di V-2, e il caso «noscript già chiuso», che ora si aspetta la perdita come su main.
- Suite web: 416 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Cosa non ho verificato**
- Le mutazioni di run2.py e l'enumerazione esaustiva enumnos.py (1.126.358 pagine): le cifre sono tue. Io ho rifatto solo le sonde mirate.
- La suite col parser vecchio (407 passed e 10 skipped).
- I casi noscript con un oracolo: lexbor ha gli script spenti. La sicurezza qui si basa sul ragionamento: con noscript nella pagina il percorso è quello di main.

**Memoria**: aggiunte la riga #504 e una lezione (quando Gas legge un elemento in modo diverso dal browser, una regola che allenta il nascondimento va spenta a livello di pagina, non rattoppata sulle singole sonde). Committate con `scripts/commit_memoria_revisore.sh` (commit f55b732). Lo stage non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev500/sonde6.py

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 388 → 416 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «416 passed, 1 skipped» su Python 3.13 e 3.11; lo skip è il test d'allarme che gira solo in CI). Col html.parser non patchato di CPython 3.12.3 caricato da plugin: 407 passed, 10 skipped.
- Oracolo lexbor (scripting spento, quindi niente noscript negli atomi), nuovo contro main 172c2d7, parser e ripiego, 29 atomi: enumerazione esaustiva a 4 atomi senza prefisso (707.281 pagine) e con 6 prefissi fissi (707.281 ciascuno), campione a 6 atomi (600.000): 0 perdite nuove; 0 regressioni salvo 4 casi col prefisso `<template><svg><foreignObject>`, tutti della classe R-ve246-5 (canvas/object con un div dentro), identici su main senza prefisso; perdite tolte: oltre 67.000.
- Noscript (l'oracolo lexbor ha gli script spenti, si usa noembed al suo posto nell'oracolo: stesso testo grezzo per lo standard): con `<noscript` nella pagina la regola non si usa e il percorso è quello di main; enumerazione esaustiva come quella della seconda verifica esterna (6 atomi template, /template, noscript, /noscript, svg, b, lunghezza 1–8, pagine con template e /template, parser e ripiego; scratchpad/f15/enumnos.py): 1.126.358 pagine, 0 fughe nuove, 0 perdite nuove (sul codice del secondo giro la verifica ne contava 82).
- Mutazioni in copie isolate (scratchpad/mut15/run2.py): senza regola 6 FAIL, senza con_noscript 9 FAIL, senza il controllo `_posizioni` 2 FAIL, flag non acceso nel ripiego 9 FAIL, flag non acceso nel parser 9 FAIL, regola che conta `aperti` (codice della #500) 4 FAIL, contatore che non scende a pila vuota 1 FAIL, che non scende chiudendo 1 FAIL, flag di rete spento subito dopo `_scarica` 2 FAIL.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

- `3b50ee1` (apertura della PR #261): unit-suite e handoff-check success; verifica-bot **failure** (BOCCIATO, V-1 ALTA noscript, chiusa in `837fcd1`); verifica esterna #261 BOCCIATO (stessa V-1, forme a e b; V-2 MEDIA preesistente → R-ve261-2; V-3/V-4 BASSE).
- `c16487c` (secondo giro): unit-suite, handoff-check e verifica-bot success; bot APPROVATO CON RISERVE (V-1 BASSA numero, V-2 COSMETICA descrizione: corrette); seconda verifica esterna #261 BOCCIATO (V-1 ALTA classe noscript, chiusa in `955607c`; V-2 BASSA test; V-3/V-4).
- `955607c` e il commit di fine-task con questo handoff: run non ancora disponibili alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Restano: **R-ve261-2** MEDIA preesistente (tag letti dentro noscript), **R-ve252-2** e **R-ve255-1** BASSE (XHTML malformato, da decidere), **R-ve246-5** MEDIA preesistente (canvas/object, decisione sul costruttore HTML5), R-ve235-7 (proposta: accettata), R-ve245-2…4, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…15».
