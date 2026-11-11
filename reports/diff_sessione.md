# Diff di sessione — 2026-11-10 — voce: allucinazioni di Whisper (chat M2)

- `modules/voice/stt.py` — elenco delle allucinazioni allargato, funzione `allucinazione`, eccezione `TrascrizioneAllucinata` (sottoclasse di `TrascrizioneIncerta`).
- `modules/voice/server.py` — allucinazione o trascrizione vuota → risposta vuota «fine», nessun turno, log senza testo.
- `tests/test_unit_voice_stt.py` — test del filtro, di `transcribe_audio` e del server; test esistenti aggiornati (vuota = silenzio).
- `.claude/agents/memoria_revisore.md` — righe #761, #762-M2.
- `reports/*` — report di fine task e stato.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
