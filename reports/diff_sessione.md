# Diff di sessione — 2026-11-11 — voce: connessione ElevenLabs riusata (chat M2)

- `modules/voice/tts.py` — `_post_riusando`: connessione HTTPS per thread tenuta aperta, nuovo tentativo solo prima dello stato, soglia di inattività di 20 s, chiusura su ogni errore e su «Connection: close», `GAS_TTS_KEEPALIVE`.
- `tests/test_unit_voice_tts.py` — 11 test del riuso.
- `.claude/agents/memoria_revisore.md` — righe #765, #768-M2.
- `reports/*` — report di fine task e stato.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
