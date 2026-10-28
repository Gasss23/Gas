# ULTIMO REPORT — 2026-10-28 — Mani fetta 21: riserve basse di #277 chiuse, lettura con lexbor sempre spenta (R6, chat Mani, PR #280)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #280 (https://github.com/Gasss23/Gas/pull/280): AUTORIZZATO dall'operatore il 2026-10-28 («mergia 280»), lo faccio io con CI verde e senza conflitti. Il merge non accende niente.
2. **Accensione**: serve la chat Motore (vedi RICHIESTE ALLA CHAT MOTORE). Dopo, sul VPS (Linux): `GAS_WEB_LEXBOR=1`.
3. Shadow DOM dichiarativo (figli «light» di un host con `<template shadowrootmode>`): nasconderli toglie anche il contenuto negli slot delle pagine vere; decisione tua.
4. Poi, una alla volta: R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7.
5. Per ripartire dopo il `/clear` incolla una riga sola: «Sei la chat Mani di Gas: leggi reports/ripartenza_mani.md e segui le istruzioni.»

## Esito
- **PR #277 (fetta 20)**: MERGIATA su richiesta dell'operatore («mergia», fb1f54b). Bot e verifica esterna su 6a58806: APPROVATO CON RISERVE (solo BASSE e cosmetiche).
- **Riserve basse di #277**: FATTA.
  - V-1 ve (`size` con migliaia di cifre faceva cadere il figlio) → `intero()` con al massimo 11 cifre significative, zeri in testa ignorati, oltre 2**31-1 non vale: FATTA.
  - V-3 ve (test mancanti: `size=+2`, `hidden=false`, sonda già riuscita col lock preso): FATTA.
  - R-bot277-4 (soglia di 2 s in un test di tempo) → tolta, basta stare dentro TEMPO_MAX: FATTA.
  - R-ve277-5 → nel figlio nascosti video, audio, meter, progress: FATTA per lexbor. La lettura di sempre resta com'è (ripiego). Shadow DOM: DEFERITA — decisione dell'operatore.
  - V-2 bot (docstring di leggi.py sulle sonde, commento «In prova») e docstring di R-ve277-4: FATTA.
  - Bot V-1 (in CI i test del figlio si saltano): DEFERITA — serve la chat Motore (requirements-dev).
- **Review**: #531 APPROVATO CON RISERVE (R-531-1 test a 11 cifre, R-531-2 commento del figlio → FATTE), #532 APPROVATO.
- **Bot e verifica esterna su ae588e6**: entrambi APPROVATO CON RISERVE (commento della verifica: https://github.com/Gasss23/Gas/pull/280#issuecomment-6447071730).
  - V-1 ve (MEDIA): PR in conflitto con main → merge di 24ed87d (PR #279: entrano gas.py, tests/test_unit_kernel.py, CLAUDE.md), review #533 APPROVATO CON RISERVE (R-533-1 cosmetica nella riga di stato_progetto → FATTA): FATTA.
  - V-2 ve (confine 2**31 non fissato): casi `size=2147483647` → lista e `size=2147483648` → tendina, review #534: FATTA.
  - V-1 bot (codice morto e stato di `reports/strumenti_mani/misura_web.py`): riga morta tolta, dichiarato fuori dal perimetro di review: FATTA.
  - V-2 bot su c5b69f3 (docstring del file di test «in prova»): FATTA.
  - V-3 ve (test nuovi saltati in CI): DEFERITA — serve la chat Motore (requirements-dev).
  - V-4 ve / V-2 bot (numeri): i test deselezionati con `GAS_WEB_LEXBOR=1` sono 61, non 60; su 3.11 la CI dà 445/58 contro 444/59 in locale (scarto di ambiente): corretti qui sotto.
- **Verdetti finali su d78843f**: bot e verifica esterna APPROVATO CON RISERVE, solo BASSE e cosmetiche (commento della verifica: https://github.com/Gasss23/Gas/pull/280#issuecomment-6447473176). Su richiesta dell'operatore («segna v1,2,3 come da sistemare») sono in stato_progetto come DA SISTEMARE: R-ve280-1 (test del figlio non girano in CI), R-ve280-2 e R-ve280-3 (numeri dell'handoff), R-bot280-1 (`intero("0")`), R-bot280-2 (riga ripetuta nell'handoff).
- **PR di nuovo in conflitto con main** (PR #281 della chat Notte): merge di 52fc615 (entrano gas.py, modules/memory/store.py, tests/test_unit_kernel.py), review #535 APPROVATO CON RISERVE (R-535-1 cosmetica, date della riga di stato_progetto → FATTA): FATTA. Nessun codice nuovo della chat Mani in questo giro: niente verifica esterna nuova, il bot rigira da solo sul nuovo head.
- **Ripartenza**: prompt per la prossima sessione in `reports/ripartenza_mani.md`; strumento di misura in `reports/strumenti_mani/misura_web.py`: FATTA.
- Restano cosmetiche: R-ve277-3 (con R-529-1), R-ve277-4 (`sys.platform` in `attivo()`), R-528-3, R-526-1, R-520-4.

## Prove (codice c5b69f3 più i casi sul confine 2**31)
- Test lexbor 63 passed su 3.13.16 con selectolax 1.0.2. Web suite 504 passed / 1 skipped (3.13); su 3.11 senza selectolax 444 passed / 59 skipped in locale, 445 / 58 nella CI (run su c5b69f3). Parser vecchio forzato: 491 passed / 11 skipped (prima dei casi nuovi). Dopo il merge di main 52fc615: kernel 1052 PASS, 1 FAIL (T31g, sqlite_vec assente nell'ambiente, noto); web 504 passed / 1 skipped.
- Suite vecchia con `GAS_WEB_LEXBOR=1`: 11 failed, 430 passed, 61 deselected (gli stessi 11 di prima).
- Mutanti, tutti presi: senza tetto alle cifre (2 failed), tetto meno uno (1), senza tetto 2**31 (2), confine `<=` (1), confine meno uno (1), senza `removeprefix` (1), zeri in testa contati (1), `hidden=false` visibile (1), senza ritorno anticipato in `attivo()` (1), video/audio/meter/progress visibili (1), risalita quadratica (1).

## RICHIESTE ALLA CHAT MOTORE
1. Per accendere la lettura con lexbor (decisione dell'operatore: «prepara l'accensione»):
   - aggiungere `selectolax==1.0.2` a `requirements-dev.txt`, così in CI girano i test lexbor oggi saltati;
   - aggiungerlo a `requirements.txt` del VPS;
   - mettere `GAS_WEB_LEXBOR=1` nell'ambiente di Gas sul VPS (Linux). Sul Mac resta spenta da sola.

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
