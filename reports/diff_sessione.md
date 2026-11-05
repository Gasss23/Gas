# Diff della sessione — 2026-11-05 — Voce V15 (chat M2)

- `modules/voice/server.py` — `_SOLO_PAUSA` e risposta «Va bene.» con `X-Gas-Comando: pausa`; `_seguito()`, `ISTRUZIONE_SEGUITO`, `_NON_PER_ME` e `X-Gas-Comando: fine` (turni di seguito solo col forte); `end_headers` con `X-Gas-Comando`; conferma con timeout 5 s, errore in cache 60 s, `HTTPException` intercettata.
- `modules/voice/tts.py` — parametro `timeout` di `synthesize_speech` (default invariato).
- `tests/test_unit_voice_stt.py` — test V15 della pausa e dei turni di seguito; «Jarvis Gas» positivo.
- `tests/test_unit_voice_prova_voci.py` — test V15 della cache degli errori della conferma; IncompleteRead.
- `.claude/agents/memoria_revisore.md` — review #675-M2 (prima, bis, ter).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md`, `reports/ripartenza_m2.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
