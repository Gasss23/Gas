# ULTIMO REPORT — 2026-10-25 — R2 via B, fetta 5: ultime note sul costo chiuse

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta (vedi §0 dell'handoff): tocca il motore. Review #509 APPROVATO senza riserve: se anche il bot dà APPROVATO senza riserve, la regola di merge autonomo permette il merge da solo.
2. Prima di accendere il forte: prova del login sul Mac (R-496-3).
3. Ancora aperti: testo nuovo dell'attività di notte da chiedere nella sessione fissa; 3 lezioni da approvare sul Mac.

## Esito

- **R-507-1 (negativo enorme contato come 1e6)**: `FATTA`, ora è scartato come gli altri negativi.
- **V-2 bot #264, primo giro (il massimo valeva per la stima solo grazie ai limiti attuali)**: `FATTA`, `min(..., _COSTO_MASSIMO)` esplicito.
- **V-2 bot #264, secondo giro (nessun test della catena completa)**: `FATTA`, T99q.
- **Test**: `tests/test_unit_claude_cli.py` 24 passed; kernel 1040 PASS 0 FAIL; pytest completo 2173 passed, 1 skipped.

## Anomalie

- Nessuna.
