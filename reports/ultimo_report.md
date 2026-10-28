# ULTIMO REPORT — 2026-10-28 — Mani fetta 23: shadow DOM dichiarativo letto come il browser nel figlio lexbor (R6, chat Mani, PR #288)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #288 (https://github.com/Gasss23/Gas/pull/288): lo faccio io solo con verdetto del bot APPROVATO pulito; con riserve aspetto il tuo OK. Il merge non accende niente.
2. Accensione della lettura con lexbor: serve la chat Motore (`selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt`), poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Poi, una alla volta: cosmetiche aperte (R-ve277-3 con R-529-1, R-ve277-4, R-528-3, R-526-1, R-520-4, R-540-1); R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7.

## Esito
- **PR #285 (fetta 22)**: MERGIATA su richiesta dell'operatore («mergia 285», 297fc22). Branch ripartito da main.
- **Shadow DOM dichiarativo (scelta 3 dell'operatore)**: FATTA nel figlio lexbor.
  - Host con `<template shadowrootmode=open|closed>` (host validi dello standard o custom element, esclusi i nomi riservati): si legge lo shadow; negli slot i figli assegnati (attributo `slot`, testo solo allo slot senza nome, primo slot per nome anche se nascosto), altrimenti la riserva; i figli non assegnati non si vedono: FATTA.
  - Shadow annidati, body come host, slot dentro un'opzione, template e slot dentro svg/math: FATTA.
  - Pagine senza shadow: nessuna ricerca tra i figli (`CON_SHADOW`): FATTA.
  - Lettura di sempre di leggi.py (ripiego): SALTATA — resta com'è, come dichiarato nella scelta.
- **Review**: #541 APPROVATO (merge di main); #539 APPROVATO CON RISERVE (R-539-1 BASSA, `template_fragments()[0]` su template svg; R-539-2 COSMETICA, slot dentro svg, nomi riservati, slot dentro un'opzione → FATTE), #540 APPROVATO (R-540-1 COSMETICA, slot dentro `foreignObject`: DEFERITA — svg è nascosto per scelta).
- **Bot su af8f8ec**: NON approvata per V-1 MEDIA (PR in conflitto con main dopo la #287) → merge di origin/main 0a9ce70: entrano gas.py, brains/claude_cli.py e i loro test identici a main; tenuti i report della #288, stato_progetto unito a mano, memoria con le righe di tutti e due i lati; review #541 APPROVATO: FATTA.
- **Accensione lexbor (punto b)**: DEFERITA — chat Motore; su main selectolax non è ancora in requirements.

## Prove
- Web suite 537 passed / 1 skipped (Python 3.13.16 con selectolax 1.0.2; su main 297fc22: 521 / 1).
- File lexbor su Python 3.11 senza selectolax: 20 passed / 76 skipped.
- Suite vecchia con `GAS_WEB_LEXBOR=1` (`tests/test_unit_web_leggi.py`): 11 failed / 430 passed / 1 skipped, prima e dopo (stessi 11).
- Mutanti (`-k 'shadow or browser'`), tutti presi: shadow spento 11 failed, ultimo slot vince 2, senza lower 1, livello sbagliato 1, ogni tag host 1, senza trattino 2, testo a tutti gli slot 3, non assegnati visibili 9, riserva sempre 7, senza `continue` 1, slot in svg contano 1, riservati host 1, opzione senza giro 1. Sopravvive `CON_SHADOW = True` (cambia solo i tempi).
- Dopo il merge di main 0a9ce70: web + claude_cli 566 passed / 1 skipped; kernel 1056 PASS, 1 FAIL (T31g, sqlite_vec assente nell'ambiente, noto).
- Tempi: 200k span in un div 0,51 s (0,43 su main), 20k div annidati 0,66 s (0,73), 8000 shadow annidati 0,13 s, 8000 slot 0,10 s.

## RICHIESTE ALLA CHAT MOTORE
1. Per accendere la lettura con lexbor e chiudere R-ve280-1:
   - `selectolax==1.0.2` in `requirements-dev.txt` (in CI girano i test lexbor oggi saltati) e in `requirements.txt` del VPS;
   - `GAS_WEB_LEXBOR=1` nell'ambiente di Gas sul VPS (Linux).

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
