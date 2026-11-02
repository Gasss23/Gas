# Diff della sessione — 2026-11-02 — Voce V6 «capire meglio» (chat M2)

- `modules/voice/stt.py` — Whisper con lingua italiana, temperatura 0, prompt col vocabolario di Gas, verbose_json; `TrascrizioneIncerta` per le trascrizioni da non usare.
- `modules/voice/server.py` — «Non ho capito bene, puoi ripetere?» senza turno; campo «capito»; istruzione voce che tiene il filo.
- `clients/voice/browser_client.html` — riga «Ho capito: …» sopra la risposta.
- `tests/test_unit_voice_stt.py` — test di soglie, eco del prompt, «non ho capito», «capito», Groq 500 nel tetto (V-1 bot #314).
- `tests/test_unit_voice_server.py` — la pagina nel browser mostra «Ho capito» come testo.
- `tests/test_unit_voice_contesto.py` — nuovo: i turni a voce vedono la conversazione (kernel vero, forte e normale).
- `.github/workflows/ci.yml` — il nuovo test nella voice suite.
- `.claude/agents/memoria_revisore.md` — righe delle review #611–#614-M2 e #617-M2.
- Dopo bot e verifica esterna: `stt.py` (eco corta, NaN), `server.py` (`capito` azzerato, «non ho capito» senza TTS), test (`tmp_path`, nuovi casi).
- `reports/prova_voce_mac.md` — «Ho capito», «Non ho capito», come tarare la soglia.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
