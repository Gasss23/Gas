# ULTIMO REPORT — 2026-10-27 — Mani fetta 21: riserve basse di #277 chiuse, lettura con lexbor sempre spenta (R6, chat Mani, PR #280)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #280 (https://github.com/Gasss23/Gas/pull/280): la mergio da solo solo con APPROVATO pulito del bot sull'head, altrimenti serve il tuo OK. Il merge non accende niente.
2. **Accensione**: serve la chat Motore (vedi RICHIESTE ALLA CHAT MOTORE). Dopo, sul VPS (Linux): `GAS_WEB_LEXBOR=1`.
3. Shadow DOM dichiarativo (figli «light» di un host con `<template shadowrootmode>`): nasconderli toglie anche il contenuto negli slot delle pagine vere; decisione tua.
4. Poi, una alla volta: R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7.
5. Per ripartire dopo il `/clear`: prompt pronto in `reports/ripartenza_mani.md`.

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
- **Ripartenza**: prompt per la prossima sessione in `reports/ripartenza_mani.md`; strumento di misura in `reports/strumenti_mani/misura_web.py`: FATTA.
- Restano cosmetiche: R-ve277-3 (con R-529-1), R-ve277-4 (`sys.platform` in `attivo()`), R-528-3, R-526-1, R-520-4.

## Prove (codice c5b69f3)
- Test lexbor 61 passed su 3.13.16 con selectolax 1.0.2. Web suite 502 passed / 1 skipped (3.13); 444 passed / 59 skipped (3.11 senza selectolax). Parser vecchio forzato: 491 passed / 11 skipped.
- Suite vecchia con `GAS_WEB_LEXBOR=1`: 11 failed, 430 passed (gli stessi 11 di prima).
- Mutanti, tutti presi: senza tetto alle cifre (2 failed), tetto meno uno (1), senza tetto 2**31 (2), senza `removeprefix` (1), zeri in testa contati (1), `hidden=false` visibile (1), senza ritorno anticipato in `attivo()` (1), video/audio/meter/progress visibili (1), risalita quadratica (1).

## RICHIESTE ALLA CHAT MOTORE
1. Per accendere la lettura con lexbor (decisione dell'operatore: «prepara l'accensione»):
   - aggiungere `selectolax==1.0.2` a `requirements-dev.txt`, così in CI girano i 58 test lexbor oggi saltati;
   - aggiungerlo a `requirements.txt` del VPS;
   - mettere `GAS_WEB_LEXBOR=1` nell'ambiente di Gas sul VPS (Linux). Sul Mac resta spenta da sola.

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
