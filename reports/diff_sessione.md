# Diff della sessione — 2026-11-05 — Voce V13 (chat M2)

- `modules/voice/server.py` — `ora_per_voce` e `istruzione_turno_voce`: data e ora locali nell'istruzione del turno parlato (vale al posto di data_ora, «ore 1:30»); istruzioni della voce strette a «una o due frasi» e senza «sì o no?» in coda; `_SOLO_ATTIVAZIONE`: «Hey Jarvis» da solo → «Dimmi.» senza turno.
- `tests/test_unit_voice_server.py` — 3 test V13 (uno con TZ forzato, R-667-1-M2); asserzione V10 con `startswith`.
- `tests/test_unit_voice_stt.py` — asserzioni V3/V4 e «forte» con `startswith` (l'istruzione ora contiene l'ora); 2 test sulla sola parola di attivazione.
- `.claude/agents/memoria_revisore.md` — review #667-M2, #668-M2, #668-M2 bis.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md`, `reports/ripartenza_m2.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
