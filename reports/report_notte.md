# Report del turno di notte — 2026-10-26

Ramo `notte/2026-10-26`, PR #271 (https://github.com/Gasss23/Gas/pull/271). Nessun merge (regola del turno).
Al massimo UNA voce del motore a notte: presa la voce 4. La voce 5 tocca anche lei il motore e resta alla prossima notte; in coda non ci sono voci solo-documenti.

## Voce 4 — `righe_stato_mattino` mai «$nan» — FATTA
- **Cosa**: in `modules/notte/notte.py` il resoconto del mattino passa spesa e tetto per un controllo nuovo (`_dollari`): un valore non finito (nan, inf) o non numerico non viene più stampato. Spesa illeggibile → «Spesa ultime 24 ore: non letta»; tetto illeggibile → «(tetto non letto)», mai «(nessun tetto)».
- **Perché / cosa migliora**: il messaggio del mattino su Telegram non mostra più «$nan» e non fa credere che il tetto di spesa sia spento quando non si legge (V-1 verifica esterna #241).
- **Controlli**: 18 casi nel test parametrico + un giro vero col tetto forzato a nan; i test nuovi falliscono sul codice di main (10 su 13 al primo giro). pytest 2199 → 2218 passed; kernel 1036 PASS 0 FAIL. Review #515 APPROVATO CON RISERVE (due BASSE, corrette), #516 APPROVATO CON RISERVE (resta una COSMETICA solo teorica).
- **Rischi**: minimi. Il testo cambia solo nei casi rotti; nei casi normali le righe sono identiche a prima.

## Cosa deve decidere l'operatore
1. Merge della PR #271 (il turno di notte non mergia).
2. Il testo dell'attività programmata è ancora quello vecchio (la chat Motore ne ha chiesto il cambio il 24 ottobre): se lo vuoi cambiare, chiedilo in questa sessione.
