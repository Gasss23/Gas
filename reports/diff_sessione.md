# Diff di sessione — 2026-11-10 — voce: seguito più severo e risposte più brevi (chat M2)

- `modules/voice/server.py` — `ISTRUZIONE_SEGUITO` più severa; `_RISPOSTE_BREVI_SEGUITO` + `seguito_da_scartare` e chiamata nel seguito (prima del cervello); `ISTRUZIONE_VOCE`/`_SCHERMO` «UNA frase breve»; `_PARLATO_VOCE_MAX_CHAR` 800.
- `tests/test_unit_voice_server.py` — test della funzione, dell'istruzione e del tetto 800; commento del test al tetto aggiornato; «UNA frase breve» nelle istruzioni.
- `tests/test_unit_voice_stt.py` — test end-to-end: frammenti chiusi senza turno, risposte brevi al cervello, con attivazione il filtro non vale.
- `.claude/agents/memoria_revisore.md` — righe #744-M2 e #746-M2.
- `reports/stato_progetto.md`, `reports/ripartenza_m2.md` — stato della fetta e riserve (anche quelle del bot sulla #363).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
