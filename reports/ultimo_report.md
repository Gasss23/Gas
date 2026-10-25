# ULTIMO REPORT — 2026-10-24 — R2 via B, fetta 4: costi grandi contati

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta (vedi §0 dell'handoff): tocca il motore, review #507 APPROVATO CON RISERVE, decide l'operatore.
2. Prima di accendere il forte: prova del login sul Mac (R-496-3).
3. Ancora aperti: testo nuovo dell'attività di notte da chiedere nella sessione fissa; 3 lezioni da approvare sul Mac.

## Esito

- **Costo grande riportato dalla CLI (V-1 verifica esterna #262, secondo giro)**: `FATTA`. Un `total_cost_usd` ≥ 1000, infinito o enorme conta (massimo 1e6) e fa scattare il tetto, invece di essere sostituito dalla stima.
- **Processi in parallelo sul tetto (V-1 bot #262, secondo giro)**: `FATTA` come limite dichiarato nel codice: sforamento massimo di una chiamata per processo.
- **Review**: #507 APPROVATO CON RISERVE (R-507-1 BASSA, tracciata in `stato_progetto.md`).
- **Merge di main (PR #261 della chat Mani) per il conflitto della PR**: `FATTA` (review #508 APPROVATO).
- **Test**: `tests/test_unit_claude_cli.py` 23 passed; kernel 1039 PASS 0 FAIL; pytest completo 2144 passed, 1 skipped.

## Anomalie

- Nessuna.
