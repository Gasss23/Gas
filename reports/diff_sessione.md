# Diff della sessione — 2026-11-03 — Voce V10, «audio+pezzi» (chat M2)

- `modules/voice/server.py` — formato `audio+pezzi` (`_FORMATO_PEZZI_VOCE`), `frasi_voce()` (tutta la risposta in frasi, tetto 1500 caratteri), `_vuole_righe_senza_schermo()`; risposta finale e risposte fisse instradate sulle righe NDJSON.
- `tests/test_unit_voice_server.py` — test V10 (frasi, formato con istruzione voce, «non ho capito» a righe); l'helper `_voce_a_pezzi` registra i turni e accetta una trascrizione qualsiasi.
- `.claude/agents/memoria_revisore.md` — review #660-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
