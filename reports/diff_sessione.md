# Diff della sessione — 2026-11-03 — Voce V11 (chat M2)

- `modules/voice/server.py` — attributo `_parlato` (richiesta a voce); `audio+pezzi` dà righe e sintesi solo alle richieste a voce, a testo solo JSON (V-1 bot #330 su ae3258e).
- `tests/test_unit_voice_server.py` — test V11 (richiesta a testo con `audio+pezzi`: niente sintesi); l'helper `_voce_a_pezzi` accetta `prompt_testo`; docstring del test V10 corretto.
- `.claude/agents/memoria_revisore.md` — review #663-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
