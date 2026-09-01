# Diff sessione — 2026-09-01

Sessione: `sonda/e2e-calcola-gemini-2026-09-01`
Scope: Sonda E2E comportamentale di `calcola()` su brain Gemini. Read-only sul motore.

## File toccati

| File | Cosa è cambiato e perché |
|---|---|
| `reports/ultimo_report.md` | Scritto ex-novo: esito sonda E2E Gemini (2 PASS), output terminale reale, verifica tool call da history. |
| `reports/stato_progetto.md` | Aggiornato header "Ultimo aggiornamento" + finding "kernel rifiuta 7×8" chiuso per Gemini (Groq-specifico). |
| `reports/handoff.md` | Scritto ex-novo: dossier fine sessione. |
| `reports/diff_sessione.md` | Questo file. |

## Note

Zero modifiche al motore (gas.py, brains/, modules/, tests/). Nessun test suite eseguita.
La sonda ha usato il kernel in modalità E2E: `GasKernel().run_turn(input)` consumando il generatore di eventi.
