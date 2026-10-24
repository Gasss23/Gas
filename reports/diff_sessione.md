# DIFF SESSIONE — 2026-10-25 (turno di notte)

- `modules/telegram/bot.py`: comando `/clear` (comando_clear, righe_riflessione, messaggi_recap, esegui_clear, ramo in _handle_update) — voce 3 della coda; poi solo da messaggio nuovo, a capo come separatore, recap vuoto (note su #263).
- `tests/test_unit_notte.py`: 19 test di `/clear` (round-trip col kernel vero, riflessione vera, testo del modello reso visibile, recap intero in pezzi).
- `.claude/agents/memoria_revisore.md`: righe delle review #502, #503 e #504 (commit del revisore).
- `reports/coda_notte.md`: voce 3 in «Fatte» (PR #263).
- `reports/stato_progetto.md`: intestazione e blocco della notte con le riserve R-503-1/2.
- `reports/report_notte.md`: report del turno.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
