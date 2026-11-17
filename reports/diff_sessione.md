# Diff della sessione — 2026-11-17 — voce: parola di attivazione tolta (M1)

Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/voice/server.py`: `_NOME_JARVIS` (storpiature), `_PAROLA_IN_TESTA`, `togli_parola_in_testa()` nei turni parlati non di seguito.
- `tests/test_unit_voice_server.py`: test della funzione, delle storpiature, del giro completo e del seguito; l'helper `_voce_a_pezzi` registra anche il prompt.
- `.claude/agents/memoria_revisore.md`, `reports/*`.
