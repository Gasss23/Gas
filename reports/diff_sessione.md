# Diff della sessione — 2026-10-30 — Voce V3, conversazione filata (chat M2)

- `clients/voice/browser_client.html` — modalità conversazione (ascolto a finestra, inizio/fine frase dal volume, bip di chiusura), frase d'attesa dopo 2 s, testo a schermo, guardie contro turni doppi (riascolto, doppio clic).
- `clients/voice/browser_server.py` — `GET /config` con `GAS_VOICE_FINESTRA`, inoltro di `X-Gas-Formato`, 504 «NON ripetere la richiesta».
- `modules/voice/server.py` — risposta «audio+testo» (testo intero + audio della parte parlata corta), `ISTRUZIONE_VOCE` ai soli turni parlati.
- `gas.py` — `run_turn(istruzione_turno=...)`: istruzione del solo turno nel messaggio system.
- `tests/test_unit_kernel.py` — T101 (round-trip di `istruzione_turno`).
- `tests/test_unit_voice_server.py`, `tests/test_unit_voice_stt.py` — parte parlata, audio+testo, /config, 504, istruzione voce, giro nel browser headless (normale e riascolto).
- `.claude/agents/memoria_revisore.md` — lezioni delle review #574-M2 e #575-M2.
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
