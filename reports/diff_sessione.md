# Diff della sessione — 2026-11-04 — Voce V12 (chat M2)

- `modules/voice/server.py` — `_sintesi_a_testo()` e tetto orario anche per le richieste a testo con risposta a voce (solo se c'è la chiave ElevenLabs); `frasi_voce` non perde la parola al tetto; docstring (1500 + avviso, tetto).
- `tests/test_unit_voice_server.py` — test V12 (parola al tetto, `audio+pezzi` senza chiave, tetto per il testo con sintesi); docstring dell'helper `_voce_a_pezzi` corretto.
- `.claude/agents/memoria_revisore.md` — review #665–#666-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
