# Diff della sessione — 2026-11-08 — Voce: riserve BASSE della #350 (chat M2)

- `modules/voice/server.py` — `_compiti_finiti` non segna più; `_segna_finiti_letti` dopo la consegna (pezzi, MP3 unico, audio/mpeg, JSON); guardia sulla risposta vuota; «Dimmi.» con i compiti (`_rispondi_senza_turno(prefisso=)`).
- `modules/sottofondo/__init__.py` — nome temporaneo unico in `_scrivi_privato`.
- `tests/test_unit_voice_server.py` (f32b), `tests/test_unit_sottofondo.py`.
- `.claude/agents/memoria_revisore.md` — review #711.
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
