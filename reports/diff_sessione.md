# DIFF SESSIONE — 2026-10-28 (chat Motore: punto 3 della RIPARTENZA, PR #286)

- `brains/claude_cli.py`: nuova `ErroreClaudeCli(RuntimeError)` per tutti gli errori scritti dal client (testi fissi); «non trovato» con il rimedio `GAS_CLAUDE_BIN`.
- `gas.py`: il motivo del «Pipeline esausta» mostra il testo di `ErroreClaudeCli`, così il report della notte dice il perché; `PATH_TIMER_NOTTE` e WARN del doctor «comando claude (notte)».
- `tests/test_unit_kernel.py`: test T99v–T99z (motivo nel messaggio, rimedio, niente testo grezzo per gli altri errori, WARN e assenza del WARN con il percorso intero).
- `.claude/agents/memoria_revisore.md`: riga della review #538.
- `reports/stato_progetto.md`: punto 3 della RIPARTENZA e «Ultimo aggiornamento».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
