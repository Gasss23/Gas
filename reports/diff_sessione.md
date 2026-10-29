# Diff della sessione — 2026-10-29 — Voce V1 (chat M2, PR #304)

- `modules/voice/server.py` — `cervello_voce()`: «forte …» parlato (anche dopo un saluto prima di «Gas») e `GAS_VOCE_FORTE` → solo cervello forte; richiesta vuota → uso; `run_server` carica il `.env` (V-1 bot #304) e si avvia con `python -m`.
- `tests/test_unit_voice_server.py` — test V1 (parola chiave, saluti, falsi positivi, interruttore, forte fermo, `.env` caricato all'avvio); opener senza proxy (R-384-1).
- `tests/test_unit_voice_stt.py` — test dal parlato trascritto al forte; opener senza proxy (R-384-1).
- `reports/roadmap.md` — R8: test stt/tts in CI dalla #229, V1 fatta, limiti dichiarati (R-564-1-M2).
- `reports/stato_progetto.md` — blocco «Voce V1».
- `.claude/agents/memoria_revisore.md` — lezioni delle review #564-M2, #565-M2, #566-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
