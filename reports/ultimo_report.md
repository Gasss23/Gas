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
- **Review**: #536 APPROVATO CON RISERVE (R-536-1 COSMETICA, «-0» dava None → FATTA), #537 APPROVATO.
- **Ripartenza**: `reports/ripartenza_mani.md` aggiornata (punto a fatto, PR #285): FATTA.

## Prove
- Web suite 521 passed / 1 skipped (Python 3.13.16 con selectolax 1.0.2).
- File lexbor su Python 3.11 senza selectolax: 20 passed / 60 skipped (il test nuovo gira).
- Mutanti, tutti presi: ritorno vecchio (4 failed), `letto = True` tolto (6), senza `not (meno and numero)` (1), solo «+» come segno (2).

## RICHIESTE ALLA CHAT MOTORE
1. Per accendere la lettura con lexbor e chiudere R-ve280-1:
   - `selectolax==1.0.2` in `requirements-dev.txt` (in CI girano i test lexbor oggi saltati) e in `requirements.txt` del VPS;
   - `GAS_WEB_LEXBOR=1` nell'ambiente di Gas sul VPS (Linux).

## Anomalie
- Nessuna.
