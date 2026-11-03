# Diff della sessione — 2026-11-03 — Mani: fetta 39, ascolto H24 a frasi in fila

Si riscrive a ogni sessione; la storia completa sta in git.

- `clients/voice/ascolto.py`: formato `audio+pezzi` (righe NDJSON, una frase alla volta) con ripieghi; `Ascolto.turno` suona i pezzi in fila e chiude la risposta; conto degli errori del rilevatore con 10 s di blocchi buoni per azzerarsi; `GAS_ASCOLTO_FORMATO`.
- `scripts/voce/installa.sh`: `valore_env` legge il .env come Gas (token, GAS_CLAUDE_BIN, porta, GAS_VOICE_URL); valori con # e percorsi non assoluti segnalati.
- `scripts/voce/LEGGIMI.md`: frasi in fila, `GAS_ASCOLTO_FORMATO`, frasi sui log corrette.
- `tests/test_unit_voce_ascolto.py`: da 93 a 149 test.
- `.claude/agents/memoria_revisore.md`: riga della review #632.
- `reports/stato_progetto.md`, `reports/roadmap.md`: fetta 39.
- `reports/ultimo_report.md`, `reports/diff_sessione.md`, `reports/handoff.md`: report di fine task.
- Merge di origin/main (PR #327 di M2, voce V9): entrano browser_server.py, browser_client.html, i test del server voce e la memoria del revisore, invariati (review #633).
