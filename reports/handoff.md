# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-26 — Mani fetta 17: R-ve261-4 (frameset) chiusa col verso sicuro, più secondo giro sulle riserve di bot e verifica esterna #270, chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #270 (https://github.com/Gasss23/Gas/pull/270). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5009491981","url":"https://github.com/Gasss23/Gas/pull/270"}`); `gh` nel cloud non è autenticato. Merge da solo solo con APPROVATO pulito del bot sull'head.
2. R-ve261-2 MEDIA (noscript come testo grezzo): «chiudi» o «accetta» (proposta: chiudi, fetta 18). Poi, una alla volta: R-ve246-5 MEDIA, R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

Primo giro (60148d7):
- **R-ve261-4 — frameset, verso sicuro (decisione dell'operatore)**: `FATTA` — dopo un `<frameset>` il resto della pagina si nasconde, nel parser (`_Estrattore._frameset`) e nel ripiego, con una riga nella scatola nera. Costo dichiarato: si perde testo anche dove il browser lo mostrerebbe.
- **Riserve della verifica esterna bis su #268** (PR #268 mergiata, 85a109b): V-1 BASSA descrizione del frameset → `FATTA`; V-2 COSMETICA #514 → `FATTA`; V-3 COSMETICA §6 → `SALTATA — istantanea per costruzione`.

Secondo giro (c843d3c), bot #270 (https://github.com/Gasss23/Gas/pull/270#pullrequestreview-5645764962) e verifica esterna #270 (https://github.com/Gasss23/Gas/pull/270#issuecomment-6404585200), entrambi APPROVATO CON RISERVE:
- **V-1 BASSA (bot e ve) — titolo prima del frameset**: `FATTA` — con un frameset il titolo si scarta (`<div></div><title>SEGRETO</title><frameset>` dava «Titolo: SEGRETO», preesistente).
- **V-2 BASSA ve — ripiego XHTML senza test**: `FATTA`.
- **V-2 COSMETICA bot / V-4 ve — commento e log**: commento `FATTA`; log del ripiego senza URL `SALTATA — il ripiego non riceve l'URL, come l'altro suo log`.
- **V-3 COSMETICA ve — §6**: `SALTATA — istantanea per costruzione`.
- **R-516-1 BASSA (review #516)**: registrata in stato_progetto come compromesso del verso sicuro (pagina a frame vera: si perde anche il titolo nell'head).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/web/leggi.py               |  20 ++++++++++++++++++--
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | n/d (commit finale)
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  72 +++++++++++++++++++++++++++++-------------------------------------------
 tests/test_unit_web_leggi.py       |  36 ++++++++++++++++++++++++++++++++++++
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat` preso con i report in stage, prima del commit finale.

## §3 GIT LOG --ONELINE (sessione)

```
c843d3c fix(web): con un frameset si scarta anche il titolo, test del ripiego XHTML (PR #270)
59a1ee8 chore(revisore): memoria review #516 — APPROVATO CON RISERVE
f82c847 docs(fine-task): Mani fetta 17 — report, handoff, stato (PR #270, review #515)
60148d7 fix(web): dopo <frameset> il resto della pagina si nasconde (R-ve261-4, verso sicuro)
c2f0607 chore(revisore): memoria review #515 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore 60148d7 (primo giro): review #515. Commit motore c843d3c (secondo giro, riserve di bot e verifica esterna #270): review #516. Verdetti integrali:

### Review #515 (chat Mani) — sul diff committato in 60148d7

## VERDETTO: APPROVATO

Review #515 (chat Mani) sul diff staged del branch claude/peaceful-lovelace-0w2b7q (Mani fetta 17, R-ve261-4 chiusa nel verso sicuro).

**Letture obbligatorie fatte:** CLAUDE.md (sez. 1, 5, 8, 9, 10), reports/stato_progetto.md (righe 621-625 sulle fette Mani), lezioni di .claude/agents/memoria_revisore.md. Applicate in particolare: mutanti anche sui log, sonde sui contenitori in cui il tag non è un tag, e due percorsi (parser e ripiego) provati separatamente.

**Elementi del diff esaminati:**
- `modules/web/leggi.py:853` — `_inizio` accende `_frameset` quando il tag è esattamente `frameset`. Rischio: che `<frameset/>` o la forma XHTML con prefisso sfuggano. Viene chiamato sia da handle_starttag sia da handle_startendtag, dopo `_locale`. Provati `<frameset\t/>`, `<frameset/x>` e XHTML `<h:frameset/>`: resto nascosto. Esito: ok.
- `modules/web/leggi.py:997` — `handle_data` scarta il testo quando il flag è acceso. Rischio: altri canali di uscita. L'unica altra uscita è il titolo, che passa anch'esso da handle_data: dopo il frameset si perde anche il titolo (`<frameset><title>SEGRETO` dà il titolo vuoto), cioè va nel verso sicuro. Esito: ok.
- `modules/web/leggi.py:1209` — nel ripiego `fine = -1` per un'apertura `frameset`, messo dopo la catena degli esiti, quindi vale anche dentro svg, noscript e template e per la forma autochiusa. Rischio: che un `<frameset>` dentro script, testo grezzo, commento o attributo venga preso per un tag (si perderebbe testo per niente). `_chiusura` e `_fine_commento` lo saltano: `<style><frameset></style>VIS`, `<textarea>…`, `<title>…` danno VIS in entrambi i percorsi. Esito: ok.
- `modules/web/leggi.py:1396` — riga nella scatola nera con l'URL tagliato a 200 caratteri, come le righe vicine. Esito: ok.
- `tests/test_unit_web_leggi.py:1062` e `tests/test_unit_web_leggi.py:1076` — test parametrizzato su 9 pagine, che prova parser e ripiego separatamente, i due log e una pagina XHTML. Rischio: un test che non coglie le modifiche sbagliate. Ho rifatto 6 mutanti, tutti presi: handle_data che ignora il flag (9 FAIL), prefisso nel parser (1), prefisso nel ripiego (1), ripiego senza taglio (7), niente log nel parser (7), niente log nel ripiego (7). Esito: ok.

**Sonde avversarie (parser e ripiego):**
- Nascosto, come voluto: `<frameset\n>`, `<frameset a='>'>`, `<svg><foreignObject><frameset/>`, `<math><mi><frameset>`, `<template><frameset>`.
- Non sono tag, quindi il testo resta visibile (come nel browser): `</frameset>`, `<frameset-x>`, `<frame>`, `<frameſet>` (s lunga: nessuno dei due parser la trasforma in minuscola ASCII), `<ｆrameset>` a tutta larghezza, `<\x00frameset>`.

**Prove rifatte:** web suite 432 passed, 1 skipped su Python 3.13.16 e su 3.11. Dopo i mutanti ho ripristinato il file dall'indice: il diff staged è intatto.

**Coerenza col progetto:** è la scelta «verso sicuro» decisa dall'operatore (si perde testo, mai testo nascosto che esce). Non tocca `_get_window`, il tetto di 10 iterazioni, i tetti di output né i provider. Niente slicing della history, niente simulazione di tool. Aggiunge una riga nella scatola nera.

**Rischi esplicitamente esclusi (non verificati):**
- Non ho rifatto il differenziale dell'autore da 180 mila pagine contro main e lexbor: lexbor non è disponibile qui. Per lettura del codice il flag si accende solo con il tag `frameset`, quindi le pagine senza quella parola non cambiano.
- Non ho rifatto la prova col parser vecchio (423 passed, 10 skipped secondo l'autore): serve iniettare il parser.py di una versione CPython non aggiornata.
- Non ho misurato quanto testo si perde sulle pagine reali che hanno un `<frameset>` a metà pagina: la perdita è accettata per decisione dell'operatore.

**Note minime (nessuna riserva):** l'asserzione XHTML viene ripetuta uguale in tutti i 9 casi e non controlla il log. Cosmetica, non serve correggerla.

**Memoria:** aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga `#515 (chat Mani) — 2026-10-25 — APPROVATO — …` (nessuna lezione nuova), committata da sola con scripts/commit_memoria_revisore.sh (commit c2f0607). I file del diff restano in stage. In `reports/stato_progetto.md` c'è una modifica non in stage che non è mia.

### Review #516 (chat Mani) — secondo giro, sul diff committato in c843d3c

## VERDETTO: APPROVATO CON RISERVE

Review #516 (chat Mani), diff STAGED del branch claude/peaceful-lovelace-0w2b7q (PR #270, secondo giro dopo bot e verifica esterna). Letture obbligatorie fatte: CLAUDE.md, reports/stato_progetto.md (voce fetta 17), .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
1. `modules/web/leggi.py:1403` — se `estrattore._frameset` è acceso, il titolo raccolto si scarta (`titolo = ""`). Rischi controllati: (a) il titolo scritto prima del frameset che finiva fuori (V-1 bot e ve); (b) varianti del tag. Sonde rifatte: `<p>A</p><div></div><title>SEGRETO</title><frameset>` dà solo «A», niente riga «Titolo:». `<FRAMESET>`, `<frameset/>`, `<h:frameset>` e `<frameset>` in XHTML: titolo scartato. `<framesets>` e `<!--<frameset>-->`: titolo tenuto, perché non sono tag frameset. Il fix sta dentro il `try` e dopo il calcolo del titolo, quindi nessuna eccezione nuova. Il ripiego perdeva già il titolo prima. Esito: ok.
2. `modules/web/leggi.py:998` — commento di `handle_data` aggiornato con le quattro condizioni (nascosto, pila incerta, `_taglia`, `_frameset`), che corrispondono alla riga `if` sopra. Esito: ok (chiude V-2 bot / V-4 ve).
3. `tests/test_unit_web_leggi.py:1076` — nuovo caso parametrico con il titolo prima del frameset. Ho rifatto il mutante «titolo non svuotato» (riga 1406 cambiata in `pass`): 1 failed, preso. File ripristinato subito dopo; il diff staged è rimasto 2 file, +11/−1. Esito: ok.
4. `tests/test_unit_web_leggi.py:1094` — ripiego XHTML (`_testo_senza_parser(..., True)`) con `<frameset>` e `<h:frameset>`: esce solo «A». Esito: ok (chiude V-2 ve).

**Suite rifatta**: web 433 passed, 1 skipped, sia su Python 3.13.16 sia su 3.11.

**Contesto progetto**: nessuna regola di CLAUDE.md sez. 5 violata (niente taglio diretto della history, niente output di tool simulato). Cap delle 10 iterazioni, `_get_window` e protezioni della memoria non toccati. Il fix va nel verso sicuro deciso dall'operatore per la riserva R-ve261-4.

**Riserva**
- **R-516-1 BASSA**: su una pagina a frame legittima (`<html><head><title>T</title></head><frameset><frame src=x></frameset>`) il browser mostra il titolo T. Gas ora restituisce un'uscita vuota, con la sola riga «Fonte:»; prima del fix restituiva almeno «Titolo: T». È una perdita consapevole del verso sicuro, ma nessun test e nessuna riga di stato la dichiarano in modo esplicito. Il commento dice solo «può non vedersi». Il differenziale dell'autore misura le fughe, non le perdite. Da scrivere in reports/stato_progetto.md come compromesso accettato. Volendo, si può rifinire più avanti: tenere il titolo solo se sta in head.

**Nota COSMETICA (V-2 bot / V-4 ve)**: il log del ripiego resta senza URL. Va bene: è coerente con l'altro log del ripiego («svg/math incerti»), e `_testo_senza_parser` non riceve l'URL.

**Rischio escluso**: non ho rifatto il differenziale contro lexbor (180 mila pagine × 2 percorsi), non riproducibile qui in tempi utili. Non ho rifatto gli altri 8 mutanti né la suite col parser vecchio forzato (424/10): ho ripetuto solo il mutante legato al fix nuovo. Per il resto vale l'evidenza dell'autore.

**Memoria**: riga #516 e una lezione nuova («provare anche il caso legittimo quando un fix verso sicuro scarta un dato») aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md e committate da sole (commit 59a1ee8). I file del diff restano in stage. Resta non staged una modifica a /home/user/Gas/reports/stato_progetto.md che non è mia.


## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati). Tutto sul codice finale c843d3c:
- `python3 -m pytest -q tests/test_unit_web_leggi.py`: main 85a109b `423 passed, 1 skipped` → ramo `433 passed, 1 skipped in 24.89s` (3.13.16) e `433 passed, 1 skipped in 24.60s` (3.11). +10 pagine parametrizzate.
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin): `424 passed, 10 skipped in 22.84s` (main 414/10).
- Mutazioni, 9, tutte prese (uscita di pytest): titolo non svuotato → `1 failed, 432 passed`; ripiego con frameset solo in HTML → `10 failed, 423 passed`; flag mai acceso nel parser → `10 failed, 423 passed`; `handle_data` che lo ignora → `10 failed, 423 passed`; prefisso invece del nome nel parser → `1 failed, 432 passed`; ripiego senza taglio → `10 failed, 423 passed`; prefisso nel ripiego → `1 failed, 432 passed`; niente log nel parser → `8 failed, 425 passed`; niente log nel ripiego → `8 failed, 425 passed`.
- Differenziale contro main (worktree 85a109b) e lexbor (selectolax 1.0.2, noscript→noembed), × parser e ripiego, atomi con frameset in più grafie, frame, noframes, template, noscript, svg/math, br, img, table, script, `<title>`, commenti, attributi: sul codice finale seed 4 `fughe nuove 0, uscite con perdite 29930`, seed 5 `fughe nuove 0, uscite con perdite 29772`, seed 6 `fughe nuove 0, uscite con perdite 29566` (60 mila pagine ciascuno); sul primo giro seed 1-3, altre 180 mila, 0 fughe nuove. Nessuna perdita su pagine senza «frameset».

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run lette dall'integrazione GitHub (`actions_list`, branch claude/peaceful-lovelace-0w2b7q):

```
40248756039  CI            push                 in_progress  —        c843d3c  2026-10-26T00:18:59Z
40248757849  verifica-bot  pull_request_target  in_progress  —        c843d3c  2026-10-26T00:19:00Z
40241977275  CI            push                 completed    success  f82c847  2026-10-25T22:49:35Z
40241985236  verifica-bot  pull_request_target  completed    success  f82c847  2026-10-25T22:49:41Z
```

Mappatura commit→run:
- `c2f0607`: nessuna run su questo SHA (pushato insieme a `60148d7`).
- `60148d7` → run CI 40241874461: `handoff-check` failure (atteso: il commit motore non contiene l'handoff della sessione), `unit-suite` success (V-3 ve #270).
- `f82c847` → run CI 40241977275 success; verifica-bot 40241985236 success (APPROVATO CON RISERVE).
- `59a1ee8`: nessuna run su questo SHA (pushato insieme a `c843d3c`).
- `c843d3c` → run CI 40248756039 e verifica-bot 40248757849, in corso alla scrittura dell'handoff.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-516-1 BASSA (review #516): compromesso del verso sicuro, registrato in stato_progetto (rifinitura possibile: tenere il titolo solo se sta nell'head).
- Riserve di bot e verifica esterna #270: chiuse o motivate in §1.
- Restano decisioni dell'operatore: R-ve261-2 MEDIA, R-ve246-5 MEDIA, R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s.
