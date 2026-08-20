# DIFF SESSIONE — 2026-08-20

> Si riscrive a ogni sessione. La storia completa sta in git.
> Sessione: FASE 3 Fetta 2 — STT server-side Groq Whisper su POST /voice

## File toccati

| File | Cosa è cambiato e perché |
|---|---|
| `modules/voice/stt.py` | **NUOVO** — modulo STT standalone: `transcribe_audio()` via Groq Whisper (stdlib pura, http.client), `parse_audio_body()` routing audio/multipart, `GroqSTTError` tipizzato, parser multipart senza dipendenze deprecate |
| `modules/voice/server.py` | **MODIFICATO** — routing Content-Type in `do_POST` (audio/* e multipart/form-data → STT, altrimenti JSON path invariato), nuovo metodo `_do_stt()` con fail-closed completo (503/400/502), docstring aggiornato con CAVEAT egress |
| `tests/test_unit_voice_stt.py` | **NUOVO** — 28 test: transport iniettato (`_conn_factory`), routing audio vs JSON, tutti i rami d'errore (chiave assente, audio vuoto, Groq 400/429/500, rete, body non-JSON su 200), multipart parsing |
| `.claude/agents/memoria_revisore.md` | **MODIFICATO** — revisore ha aggiunto lezione review #88: catturare `json.JSONDecodeError` dopo `resp.read()` su status 200 in moduli HTTP-client standalone |
| `reports/stato_progetto.md` | **MODIFICATO** — aggiunta entry FASE 3 Fetta 2, aggiornato "Ultimo aggiornamento", aggiornata voce componenti attive |
| `reports/ultimo_report.md` | **MODIFICATO** — report di fine task: sonda, implementazione, fail-closed table, sicurezza/caveat, test, verdetto revisore |
| `reports/handoff.md` | **MODIFICATO** — dossier fine sessione: §0 decisioni umane, §1-7 secondo template |
| `reports/diff_sessione.md` | **MODIFICATO** — questo file |

## Note

- `probe_tts_output.mp3` presente nella working tree (untracked, generato in sessione precedente) — non committato (file binario temporaneo, non pertinente al repo).
- Nessuna modifica a `gas.py`, cascata provider, TTS/ElevenLabs, auth bearer — stop gate rispettati.
