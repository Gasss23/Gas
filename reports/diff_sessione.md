# Diff della sessione — 2026-10-29 — Voce V1 (chat M2, PR #304)

- `modules/voice/server.py` — `cervello_voce()`: «forte …» parlato e `GAS_VOCE_FORTE` → solo cervello forte; messaggio d'uso nuovo.
- `tests/test_unit_voice_server.py` — test V1 (parola chiave, falsi positivi, interruttore, forte fermo); opener senza proxy (R-384-1).
- `tests/test_unit_voice_stt.py` — test dal parlato trascritto al forte; opener senza proxy (R-384-1).
- `reports/roadmap.md` — R8: test stt/tts in CI dalla #229, V1 fatta, limiti dichiarati (R-564-1-M2).
- `reports/stato_progetto.md` — blocco «Voce V1».
- `.claude/agents/memoria_revisore.md` — lezione della review #564-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
