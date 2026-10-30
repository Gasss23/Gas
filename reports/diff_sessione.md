# Diff della sessione — 2026-10-29 — Voce V2 (chat M2)

- `modules/voice/server.py` — «forte» parlato senza richiesta → istruzione d'uso da ascoltare (200, nessun turno); riga «avvio in corso» prima del caricamento.
- `clients/voice/browser_server.py` — attesa della risposta 600 s (`GAS_VOICE_TIMEOUT`), connessione 10 s, 504 chiaro a tempo scaduto (anche in coda), risposta rotta → 502 JSON, proxy a thread (`ThreadingHTTPServer`), errori in `_send_error_json`.
- `tests/test_unit_voice_server.py` — ordine della riga d'avvio; test del proxy del browser (tempo scaduto, valori dell'attesa, connessione appesa, a thread, risposta rotta), socket chiusi.
- `tests/test_unit_voice_stt.py` — istruzione d'uso a voce (JSON, con l'interruttore, audio sintetizzato); `_post_raw` accetta risposte audio.
- `.claude/agents/memoria_revisore.md` — lezioni delle review #568-M2 … #572-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md`, `reports/roadmap.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
