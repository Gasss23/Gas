# Diff di sessione — 2026-11-11 — voce: filtro 2 (chat M2)

- `modules/voice/stt.py` — `_frase_allucinata` (regole di una frase), `allucinazione` frase per frase, saluti di chiusura (`_SALUTI_ALLUCINATI`, `_PAROLE_DEI_SALUTI`), frasi intere senza punteggiatura interna, tetto di 8 parole per le parti note, docstring di `TrascrizioneAllucinata` corretta.
- `modules/voice/server.py` — `_INTERCALARI` e loro uso in `seguito_da_scartare`.
- `tests/test_unit_voice_stt.py`, `tests/test_unit_voice_server.py` — test positivi e negativi.
- `.claude/agents/memoria_revisore.md` — righe #764, #766, #767, #769-M2.
- `reports/*` — report di fine task e stato.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
