# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-25 — Mani fetta 17: R-ve261-4 (frameset) chiusa col verso sicuro, chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #270 (https://github.com/Gasss23/Gas/pull/270). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5009491981","url":"https://github.com/Gasss23/Gas/pull/270"}`); `gh` nel cloud non è autenticato. Merge da solo solo con APPROVATO pulito del bot sull'head.
2. Decisioni ancora aperte, una alla volta: R-ve261-2 MEDIA, R-ve246-5 MEDIA, R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **R-ve261-4 — frameset, verso sicuro (decisione dell'operatore)**: `FATTA` — dopo un `<frameset>` il resto della pagina si nasconde, nel parser (`_Estrattore._frameset`) e nel ripiego, con una riga nella scatola nera. Costo dichiarato: si perde testo anche dove il browser lo mostrerebbe.
- **Riserve della verifica esterna bis su #268** (PR #268 mergiata, 85a109b, bot APPROVATO senza finding sull'head 3f4568f): V-1 BASSA descrizione del frameset → `FATTA` (descrizione esatta in stato_progetto, fetta 17); V-2 COSMETICA #514 mancante in stato_progetto → `FATTA`; V-3 COSMETICA §6 → `SALTATA — istantanea per costruzione, nessuna azione`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 modules/web/leggi.py               |  13 ++++++++++++-
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | n/d (commit finale)
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  64 +++++++++++++++++++++-------------------------------------------
 tests/test_unit_web_leggi.py       |  31 +++++++++++++++++++++++++++++++
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat` preso con i report in stage, prima del commit finale.

## §3 GIT LOG --ONELINE (sessione)

```
60148d7 fix(web): dopo <frameset> il resto della pagina si nasconde (R-ve261-4, verso sicuro)
c2f0607 chore(revisore): memoria review #515 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

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

## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati):
- `python3 -m pytest -q tests/test_unit_web_leggi.py`: main 85a109b `423 passed, 1 skipped` → ramo `432 passed, 1 skipped in 24.89s` (3.13.16) e `432 passed, 1 skipped in 24.10s` (3.11). +9 test (pagine parametrizzate).
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin): `423 passed, 10 skipped in 22.82s` (main 414/10).
- Mutazioni, 7, tutte prese (uscita di pytest): flag mai acceso nel parser → `9 failed, 423 passed`; `handle_data` che lo ignora → `9 failed, 423 passed`; prefisso invece del nome nel parser → `1 failed, 431 passed`; ripiego senza taglio → `7 failed, 425 passed`; prefisso nel ripiego → `1 failed, 431 passed`; niente log nel parser → `7 failed, 2 passed, 424 deselected` (su `-k frameset`); niente log nel ripiego → `7 failed, 2 passed, 424 deselected` (su `-k frameset`).
- Differenziale contro main (worktree 85a109b) e lexbor (selectolax 1.0.2, noscript→noembed), 180 mila pagine casuali × parser e ripiego (atomi: frameset in più grafie, frame, noframes, template, noscript, svg/math, br, img, table, script, commenti, attributi): seed 1 `fughe nuove 0, uscite con perdite 29728`, seed 2 `fughe nuove 0, uscite con perdite 29368`, seed 3 `fughe nuove 0, uscite con perdite 29822`; nessuna perdita su pagine senza «frameset».

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run lette dall'integrazione GitHub (`actions_list`, branch claude/peaceful-lovelace-0w2b7q):

```
40241874461  CI            push                 in_progress  —        60148d7  2026-10-25T22:48:09Z
40241887828  verifica-bot  pull_request_target  completed    skipped  60148d7  2026-10-25T22:48:20Z
```

Mappatura commit→run:
- `c2f0607`: nessuna run su questo SHA (pushato insieme a `60148d7`).
- `60148d7` → run CI 40241874461 (push), in corso alla scrittura dell'handoff; verifica-bot 40241887828 skipped (etichetta `verifica` non ancora messa).
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Dalla review #515: nessuna (una nota cosmetica dichiarata «non serve correggerla»).
- R-ve261-4 CHIUSA da questa fetta.
- Restano decisioni dell'operatore: R-ve261-2 MEDIA, R-ve246-5 MEDIA, R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s.
