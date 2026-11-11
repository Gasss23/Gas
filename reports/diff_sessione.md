# Diff di sessione — 2026-11-11 — voce: connessione ElevenLabs riusata (chat M2)

- `modules/voice/tts.py` — `_post_riusando`: connessione HTTPS per thread tenuta aperta; `_conn_caduta` (select a 0 s) prima del riuso; nuovo tentativo solo durante l'invio; soglia di inattività di 20 s; chiusura su ogni errore e su «Connection: close»; `GAS_TTS_KEEPALIVE`.
- `tests/test_unit_voice_tts.py` — 14 test del riuso (soglia a valori fissi 19/21 s).
- `.claude/agents/memoria_revisore.md` — righe #765, #768, #770, #771, #772, #776-M2.
- Merge di origin/main (#370, #369).
- `reports/*` — report di fine task e stato.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
