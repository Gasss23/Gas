# DIFF DI SESSIONE — 23 novembre 2026, R7 fetta 3 (stato dei lavori ricorrenti)

Questo file si riscrive a ogni sessione; la storia completa sta in git.

- `modules/notte/notte.py`: registro dello stato dei lavori (lettura difensiva, scrittura atomica, pausa di 7 giorni dopo 3 ko di fila, sezione nel riepilogo, `_giorno` senza eccezioni).
- `tests/test_unit_notte.py`: 9 test (stati, pausa e rilancio a mano, ok che azzera, prompt cambiato, pausa scaduta o assurda, registro rovinato, potatura, data enorme, catalogo in parte rotto).
- `reports/setup_notte.md`: paragrafo sullo stato dei lavori per l'operatore.
- `.claude/agents/memoria_revisore.md`: righe delle review #839-F3 e #842.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
