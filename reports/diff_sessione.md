# Diff di sessione — 2026-11-10 — voce: correzioni dell'audit notturno (chat M2)

- `modules/voice/server.py` — timeout del socket (B1), `_PAROLA_FORTE` con jarvis e ripetizione (B2), 400 al JSON di forma sbagliata (B5), tetti 413 su corpo e prompt, porta aperta prima del kernel con messaggio chiaro.
- `modules/voice/stt.py`, `modules/voice/tts.py` — HTTPException → OSError (B3), anche in elenco voci, libreria e aggiunta voce.
- `clients/voice/browser_server.py` — `.env` con le regole di Gas (B4); senza GAS_VOICE_URL segue GAS_VOICE_PORT.
- `tests/test_unit_voice_server.py`, `tests/test_unit_voice_stt.py`, `tests/test_unit_voice_tts.py` — un test per ogni correzione; test dell'avvio con rete privata adattato (server finto).
- `.claude/agents/memoria_revisore.md` — righe #752, #755, #759-M2.
- `reports/*` — report di fine task e stato.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
