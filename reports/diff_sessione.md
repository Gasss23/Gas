# Diff della sessione — 2026-11-09 — Sottofondo e voce: riserve BASSE (chat M2)

- `modules/voice/server.py` — segno di lettura dopo `_send_json`; regola unica schermo/senza schermo (`_do_pezzi_response(schermo=)`, `consegnati`).
- `modules/sottofondo/__init__.py` — `_pulisci_vecchi` cancella anche compiti aperti vecchi senza posto; `_ultima_pulizia` con `time.monotonic`.
- `tests/test_unit_voice_server.py` (f32c), `tests/test_unit_sottofondo.py`.
- `.claude/agents/memoria_revisore.md` — review #713.
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
