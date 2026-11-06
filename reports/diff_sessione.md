# Diff della sessione — 2026-11-05 — Voce V15 (chat M2)

- `modules/voice/server.py` — `_SOLO_PAUSA` e risposta «Va bene.» con `X-Gas-Comando: pausa`; `_seguito()`, `ISTRUZIONE_SEGUITO`, `_NON_PER_ME` e `X-Gas-Comando: fine` (turni di seguito solo col forte); `end_headers` con `X-Gas-Comando`; conferma con timeout 5 s, errore in cache 60 s, `HTTPException` intercettata; seguito → `effimero=True`, risposta vuota → fine, trascrizione incerta o vuota → fine; il generatore del turno si chiude subito.
- `gas.py` — `run_turn(effimero=True)`: solo forte, nessuno strumento offerto, storia su copia ripristinata nel finally, niente salvataggio (scelta A dell'operatore, R-675-1-M2).
- `tests/test_unit_kernel.py` — T103a-e: turno effimero, round-trip §7, break+close come il server.
- `modules/voice/tts.py` — parametro `timeout` di `synthesize_speech` (default invariato).
- `tests/test_unit_voice_stt.py` — test V15 della pausa e dei turni di seguito; «Jarvis Gas» positivo.
- `tests/test_unit_voice_prova_voci.py` — test V15 della cache degli errori della conferma; IncompleteRead.
- `.claude/agents/memoria_revisore.md` — review #675-M2 (prima, bis, ter), #676-M2, #677-M2 (e bis).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md`, `reports/ripartenza_m2.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
