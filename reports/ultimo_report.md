# ULTIMO REPORT — 2026-10-28 — Mani fetta 22: riserve «DA SISTEMARE» di #280, `intero()` del figlio lexbor (R6, chat Mani, PR #285)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #285 (https://github.com/Gasss23/Gas/pull/285): lo faccio io solo con verdetto del bot APPROVATO pulito; con riserve aspetto il tuo OK. Il merge non accende niente.
2. Accensione della lettura con lexbor: serve la chat Motore (vedi RICHIESTE ALLA CHAT MOTORE), poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Shadow DOM dichiarativo (figli «light» di un host con `<template shadowrootmode>`): decisione tua.
4. Poi, una alla volta: cosmetiche aperte (R-ve277-3 con R-529-1, R-ve277-4, R-528-3, R-526-1, R-520-4); R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7.

## Esito
- **PR #280 (fetta 21)**: MERGIATA (b95c3f3). Branch ripartito da main.
- **Riserve «DA SISTEMARE» di #280**:
  - R-bot280-1 (`intero("0")` dava None) → «0», «000», «-0» danno 0 come il browser; senza cifre o con un negativo non zero resta None: FATTA. Esito pratico invariato (`(intero(size) or 1) > 1`).
  - Test `test_intero_come_il_browser`: prende `intero()` dal sorgente del figlio con `ast`, gira anche senza selectolax: FATTA.
  - R-ve280-2, R-ve280-3, R-bot280-2 (numeri datati, numero CI non verificabile, riga ripetuta nell'handoff di #280): FATTA — l'handoff si riscrive a ogni sessione; questo cita solo numeri misurati in sessione.
  - R-ve280-1 (test del figlio non girano nei check required): DEFERITA — serve la chat Motore (selectolax in requirements-dev).
- **Review**: #536 APPROVATO CON RISERVE (R-536-1 COSMETICA, «-0» dava None → FATTA), #537 APPROVATO, #538 APPROVATO.
- **Bot e verifica esterna su 162f5b1**: entrambi APPROVATO CON RISERVE (commento della verifica: https://github.com/Gasss23/Gas/pull/285#issuecomment-6468276114).
  - V-1 ve MEDIA (PR in conflitto con main dopo #283 e #284) → merge di 0cf1d67: tenuti i report della #285, stato_progetto unito a mano, memoria con le righe di tutti e due i lati; niente perimetro, niente review: FATTA.
  - V-2 ve / V-1 bot COSMETICA (commento di `intero()` senza il segno) → commento aggiornato, review #538: FATTA.
  - V-3 ve COSMETICA (numeri dei mutanti del test intermedio) → rifatti sul test finale, sotto: FATTA.
  - V-4 ve COSMETICA (§6 dell'handoff sulla CI di un commit vecchio) → handoff riscritto sulla head nuova: FATTA.
- **Bot e verifica esterna su 116aac3**: entrambi APPROVATO CON RISERVE, niente ALTA/MEDIA (commento della verifica: https://github.com/Gasss23/Gas/pull/285#issuecomment-6468447612).
  - V-1 bot / V-1 ve COSMETICA (riga «Ultimo aggiornamento» di stato_progetto senza #538 e senza il secondo giro) → riga completata, su richiesta dell'operatore («sistema V-1»): FATTA.
  - V-2 ve (§6 e §0 dell'handoff fermi alla scrittura): SALTATA — inevitabile per costruzione dell'handoff, nessun fix richiesto.
  - V-3 ve (numerazione parallela delle review #536/#537 tra le chat): SALTATA — già dichiarata, righe marcate «(chat X)».
- **Ripartenza**: `reports/ripartenza_mani.md` aggiornata (punto a fatto, PR #285): FATTA.

## Prove
- Web suite 521 passed / 1 skipped (Python 3.13.16 con selectolax 1.0.2), prima e dopo il commento di #538.
- File lexbor su Python 3.11 senza selectolax: 20 passed / 60 skipped (il test nuovo gira).
- Mutanti sul test finale (17 casi), tutti presi: ritorno vecchio (7 failed), `letto = True` tolto (8), senza `not (meno and numero)` (1), solo «+» come segno (2).

## RICHIESTE ALLA CHAT MOTORE
1. Per accendere la lettura con lexbor e chiudere R-ve280-1:
   - `selectolax==1.0.2` in `requirements-dev.txt` (in CI girano i test lexbor oggi saltati) e in `requirements.txt` del VPS;
   - `GAS_WEB_LEXBOR=1` nell'ambiente di Gas sul VPS (Linux).

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
- Numeri delle review: in memoria ci sono #536/#537 anche della chat Notte e della chat Motore (numerazione parallela); quelle di questa fetta sono marcate «(chat Mani)».
