# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-27 — Mani fetta 21: riserve basse di #277 chiuse, lettura con lexbor sempre spenta, chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #280 (https://github.com/Gasss23/Gas/pull/280). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5037069764","url":"https://github.com/Gasss23/Gas/pull/280"}`); `gh` nel cloud non è autenticato. Merge da solo solo con APPROVATO pulito del bot sull'head. Il merge non accende niente.
2. Accensione: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt`; poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Shadow DOM dichiarativo: nascondere i figli «light» di un host con `<template shadowrootmode>` toglierebbe anche il contenuto negli slot delle pagine vere. Decisione dell'operatore.
4. Poi, una alla volta: R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7. Prompt per ripartire: `reports/ripartenza_mani.md`.

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #277**: `FATTA` — richiesta dell'operatore («mergia»), merge fb1f54b.
- **Riserve basse di #277 (fetta 21)**: `FATTA`.
  - V-1 ve #277 su 6a58806 (`size` enorme), V-3 ve (test mancanti), R-bot277-4 (soglia in secondi), R-ve277-5 parte lexbor (video/audio/meter/progress), V-2 bot (docstring), docstring di R-ve277-4: `FATTA`.
  - R-531-1, R-531-2 (cosmetiche della review #531): `FATTA`.
  - Shadow DOM dichiarativo: `DEFERITA — decisione dell'operatore`.
  - Bot V-1 (test del figlio saltati in CI): `DEFERITA — serve la chat Motore (requirements-dev)`.
  - Cosmetiche R-ve277-3, R-ve277-4 (`sys.platform`), R-529-1, R-528-3, R-526-1, R-520-4: `DEFERITA — cosmetiche, verso sicuro`.
- **Riassunto e ripartenza dopo il `/clear`** (richiesta dell'operatore): `FATTA` — `reports/ripartenza_mani.md`, strumento di misura in `reports/strumenti_mani/misura_web.py`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md   |   3 +++
 modules/web/leggi.py                 |   5 +++--
 modules/web/lexbor.py                |  21 +++++++++++++--------
 reports/diff_sessione.md             |  15 ++++++++-------
 reports/handoff.md                   | n/d (commit finale)
 reports/ripartenza_mani.md           |  31 +++++++++++++++++++++++++++++++
 reports/stato_progetto.md            |   4 +++-
 reports/strumenti_mani/misura_web.py | 137 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/ultimo_report.md             |  49 +++++++++++++++++++++----------------------------
 tests/test_unit_web_lexbor.py        |  35 +++++++++++++++++++++++++++++++----
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat fb1f54b` preso con i report in stage, prima del commit finale. BASE = `git merge-base origin/main HEAD` = fb1f54b (merge della PR #277): il branch è ripartito da main dopo il merge.

## §3 GIT LOG --ONELINE (sessione)

```
c5b69f3 fix(web): riserve basse di #277 — size enorme, test mancanti, video/audio/meter/progress (fetta 21 Mani)
a2518f1 chore(revisore): memoria review #532 — APPROVATO
8a0d0d5 chore(revisore): memoria review #531 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore c5b69f3: review #531 sul primo diff e #532 dopo la chiusura di R-531-1/2. Verdetti integrali:

### Review #531 (chat Mani) — primo diff staged

## VERDETTO: APPROVATO CON RISERVE

Review #531 (chat Mani), fetta 21 lexbor: chiude le riserve BASSE della PR #277. Diff in stage: modules/web/lexbor.py, modules/web/leggi.py, tests/test_unit_web_lexbor.py. Prima della review ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md (le voci su lexbor) e la mia memoria.

**Elementi del diff esaminati**
- `modules/web/lexbor.py:97` — `intero()` tiene al massimo 11 cifre significative, salta gli zeri in testa e accetta il valore solo se è sotto 2**31. Rischio esaminato: il figlio cade (era il ValueError di int() con più di 4300 cifre), un valore oltre il tetto viene preso per valido, il ciclo diventa lento. Prove con valori limite fatte da me: 21474836470 e 2147483648 danno la tendina; 2147483647, `+0003` e `   +12x` danno la lista; 0 e 00 danno la tendina; 2 milioni di zeri prima di un 5 vengono letti in 0,23 s (lineare). Ogni numero con 11 o più cifre significative supera 2**31-1, quindi il troncamento è corretto. — ok
- `modules/web/lexbor.py:65` — video, audio, meter e progress aggiunti ai tag nascosti del figlio. Rischio esaminato: si nasconde testo che il browser mostra. Il browser non disegna mai il contenuto di riserva di video e audio né l'interno di meter e progress. Lo stesso insieme vale in `opzioni_visibili`, cosa innocua. Mutanti presi: tutti e quattro tolti (1 failed), solo video tolto (1), solo meter tolto (1). La lettura di sempre resta diversa ed è dichiarato. — ok
- `modules/web/lexbor.py:178` — ritorno anticipato di `attivo()` quando la sonda è già riuscita. Il test `tests/test_unit_web_lexbor.py:169` lo fissa tenendo il lock preso. Rischio esaminato: il test non prende il mutante, oppure lascia sporco lo stato globale. Col mutante che toglie il ritorno anticipato: 1 failed. `_FIGLIO_OK` è ripristinato dal monkeypatch del fixture `acceso` e il lock viene rilasciato nel `finally`. — ok
- `tests/test_unit_web_lexbor.py:162` — il test del size enorme chiama `testo_visibile` direttamente e controlla il valore esatto. Così non può passare grazie al ripiego, e la lezione della review #528 è applicata. Mutanti: senza tetto sulle cifre 2 failed, senza tetto 2**31 2 failed, tetto 2**40 2 failed, senza togliere il «+» 1 failed, zeri in testa contati 1 failed. — ok
- `tests/test_unit_web_lexbor.py:153` — tolta la soglia di 2 s, resta `is not None`. Rischio esaminato: il test non prende più la risalita quadratica. Ho riscritto io il mutante quadratico (`css("option")` più risalita agli antenati): 1 failed, perché supera TEMPO_MAX e il figlio restituisce None. — ok
- `modules/web/leggi.py:34` — la docstring ora descrive le sonde ripetute. Confrontata con MAX_SONDE=3 e RIPROVA_SONDA=600 di modules/web/lexbor.py: torna. — ok

**Riserve (entrambe COSMETICHE, da tracciare in stato_progetto)**
- R-531-1 (chat Mani): il mutante «tetto a 10 cifre» (`len(cifre) > 9`) SOPRAVVIVE con 60 passed. Con quel mutante `size=21474836470` verrebbe troncato a 2147483647 e letto come lista. Manca un caso parametrico a 11 cifre con le prime 10 sotto 2**31 (per esempio `size=21474836470` deve dare la tendina). Il codice di oggi è corretto: l'ho verificato con le prove sopra.
- R-531-2 (chat Mani): il commento in testa al codice del figlio (`modules/web/lexbor.py:52`) elenca ancora solo «datalist e rp» fra le cose che il browser non mostra. Video, audio, meter e progress sono spiegati solo accanto alla riga 65.

**Prove rifatte da me**
- Lexbor: 60 passed su 3.13 con selectolax 1.0.2; 3 passed e 57 skipped su 3.11 (senza selectolax).
- Test web (`-k web`): 502 passed, 1 skipped su 3.13. Il riepilogo diceva 501; la differenza è con ogni probabilità nel filtro `-k`.
- Wall of Shame: niente slicing della history, niente simulazione di tool, cap e `_get_window` non toccati, lettura con lexbor sempre spenta per default.

**Rischi esclusi (non verificati)**
- Il comportamento esatto di Chrome e Firefox al confine 2**31 (overflow uguale a valore non valido, quindi size di default) l'ho preso dalla conoscenza dei sorgenti di Blink, non l'ho verificato in un browser: qui non è riproducibile.
- La suite vecchia con GAS_WEB_LEXBOR=1 (11 failed, dichiarati uguali a prima) e il parser vecchio forzato (491/11) non li ho rifatti.
- Il caso dello shadow DOM dichiarativo resta aperto, come dichiarato.

**Memoria**
- Riga #531 (chat Mani) aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, insieme a una lezione nuova: un tetto sulla lunghezza delle cifre va provato col mutante «tetto meno uno».
- Committata da sola con lo script: commit 8a0d0d5. Lo stage non è stato toccato: restano i 3 file, 42 righe aggiunte e 11 tolte.

### Review #532 (chat Mani) — diff committato in c5b69f3

## VERDETTO: APPROVATO

Ri-review #532 (chat Mani): fetta 21 lexbor dopo la #531. Ho letto CLAUDE.md, stato_progetto e la mia memoria. Diff in stage: `git diff --cached`, 3 file, +47/-14.

Elementi del diff esaminati:
- `tests/test_unit_web_lexbor.py:99`: è il nuovo caso `<select size=21474836470>`, che deve dare la tendina (W1 visibile, W2 no). Rischio esaminato: il mutante «tetto meno uno» sopravviveva (R-531-1). Ho applicato il mutante `len(cifre) > 9` a `modules/web/lexbor.py:103`: 1 failed, 60 passed. Poi ho ripristinato il file (`git diff` non in stage è vuoto). Esito: ok, R-531-1 chiusa.
- `modules/web/lexbor.py:103`: `intero()` tiene al massimo 11 cifre significative, salta gli zeri in testa e accetta solo valori < 2**31. Rischio esaminato: le 11 cifre sono esattamente quelle che servono per distinguere 2147483647|0 dal massimo. Esito: ok.
- `modules/web/lexbor.py:52`: il commento in testa al figlio ora elenca anche video, audio, meter e progress, come l'insieme `nascosti` del figlio. Rischio esaminato: commento non allineato al codice (R-531-2). Le righe 48-55 sono tutte da 95 caratteri o meno. Esito: ok, R-531-2 chiusa.
- `modules/web/leggi.py:34`: la docstring dice che la sonda riparte «al più altre 2 volte a 600 s l'una dall'altra». Rischio esaminato: incoerenza con le costanti. Ho controllato con `modules/web/lexbor.py:38` (RIPROVA_SONDA=600.0) e `modules/web/lexbor.py:39` (MAX_SONDE=3, cioè la prima più altre 2). Esito: ok.

Prove che ho rifatto io:
- lexbor: 61 passed (Python 3.13);
- tutta la suite web: 502 passed, 1 skipped (3.13);
- mutante tetto-1: 1 failed, 60 passed.

Rischi esclusi:
- Non ho rifatto la suite su Python 3.11 (444/59 dichiarato dall'agente): selectolax c'è solo su 3.13, quindi su 3.11 i test lexbor sono quasi tutti skippati e non provano nulla di nuovo.
- Il comportamento sul VPS non è verificato: non è riproducibile in dev.
- Nota COSMETICA, non è una riserva: la riga `modules/web/lexbor.py:66` (insieme `nascosti` nel codice del figlio) è lunga 114 caratteri. Viene dalla fetta già vista nella #531.

Memoria: ho aggiunto la riga #532 (chat Mani) in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola con lo script (commit a2518f1). Lo stage non l'ho toccato: resta 3 file, +47/-14.

## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati), codice c5b69f3:
- `python3 -m pytest -q tests/test_unit_web_*.py`: main fb1f54b `494 passed, 1 skipped` → ramo `502 passed, 1 skipped in 33.43s` (3.13.16, con selectolax); `444 passed, 59 skipped in 26.07s` (3.11 locale, senza selectolax). `tests/test_unit_web_lexbor.py` da 53 a 61 test (`61 passed in 6.71s`).
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin), prima dell'ultimo caso a 11 cifre: `491 passed, 11 skipped in 31.16s`.
- Suite vecchia con `GAS_WEB_LEXBOR=1` (test lexbor esclusi): `11 failed, 430 passed, 1 skipped, 60 deselected in 43.49s` (gli stessi 11 di prima).
- Mutanti (uscita di pytest sui test lexbor): senza tetto alle cifre `2 failed, 58 passed`; senza tetto 2**31 `2 failed, 58 passed`; senza removeprefix `1 failed, 59 passed`; zeri in testa contati `1 failed, 59 passed`; hidden=false visibile `1 failed, 59 passed`; senza ritorno anticipato in attivo() `1 failed, 59 passed`; video/audio/meter/progress visibili `1 failed, 59 passed`; risalita quadratica `1 failed, 59 passed`; tetto meno uno (dopo R-531-1) `1 failed, 60 passed`.

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run lette dall'integrazione GitHub (`actions_list`, workflow ci.yml, branch claude/peaceful-lovelace-0w2b7q, evento push). Istantanea al momento della scrittura: lo stato aggiornato è sulla PR.

```
40536717337  CI  push  in_progress  —  c5b69f3  2026-10-27T16:00:58Z
```

Mappatura commit→run:
- `8a0d0d5`, `a2518f1`: nessuna run su questo SHA (pushati insieme a `c5b69f3`).
- `c5b69f3` → run 40536717337, in corso alla scrittura dell'handoff.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Shadow DOM dichiarativo (figli «light» di un host con `<template shadowrootmode>`): decisione dell'operatore.
- Bot V-1 #277: test del figlio saltati in CI finché selectolax non è in requirements-dev (chat Motore).
- R-ve277-3 COSMETICA (con R-529-1): opzione dentro un sotto-albero `hidden` o un `optgroup disabled` nella scelta automatica.
- R-ve277-4 COSMETICA: fuori da Linux 3 sonde prima di spegnere (`sys.platform` in `attivo()`).
- R-528-3, R-526-1, R-520-4 COSMETICHE.
- Nota cosmetica del revisore #532 (non riserva): la riga dell'insieme `nascosti` del figlio è lunga 114 caratteri.
- Restano decisioni dell'operatore: R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s.
