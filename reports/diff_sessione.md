# Diff della sessione — 2026-11-05 — Voce V13 (chat M2)

- `modules/voice/server.py` — `ora_per_voce` e `istruzione_turno_voce`: data e ora locali nell'istruzione del turno parlato; istruzioni della voce strette a «una o due frasi».
- `tests/test_unit_voice_server.py` — 3 test V13; asserzione V10 con `startswith`.
- `tests/test_unit_voice_stt.py` — asserzioni V3/V4 e «forte» con `startswith` (l'istruzione ora contiene l'ora).
- `.claude/agents/memoria_revisore.md` — review #667-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md`, `reports/ripartenza_m2.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
