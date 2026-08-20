# Diff sessione — 2026-08-20 — FASE 3 Fetta 3 TTS ElevenLabs

> Riepilogo dell'ultima sessione. Si riscrive a ogni sessione; storia completa in git.
> BASE: 0ddad1d9e764fe344b3eea699fc7f5453690c0da (merge-base origin/main)

## File toccati

| File | Tipo | Perché |
|------|------|--------|
| `modules/voice/tts.py` | NUOVO | Modulo TTS: `synthesize_speech()` + `ElevenLabsTTSError`, stdlib `http.client`, zero dipendenze esterne, `_conn_factory` iniettabile per test |
| `modules/voice/server.py` | MODIFICATO | Aggiunto path output audio: `_wants_audio()` (Accept header), `_send_audio()`, `_do_tts_response()` con tutti i rami fail-closed; docstring aggiornata |
| `tests/test_unit_voice_tts.py` | NUOVO | 17 test unit con rete isolata: routing, rami errore (503/502), synthesize_speech unit con _FakeConn iniettato |
| `.claude/agents/memoria_revisore.md` | MODIFICATO | Revisore ha aggiunto lezione review #89 |
| `reports/ultimo_report.md` | MODIFICATO | Report canonico FASE 3 Fetta 3 con DECISIONI UMANE, sonda, implementazione, test, verdetto revisore, caveat sicurezza |
| `reports/handoff.md` | MODIFICATO | Dossier di fine sessione: §0–§7 completi |
| `reports/diff_sessione.md` | MODIFICATO | Questo file |
| `reports/stato_progetto.md` | MODIFICATO | Aggiunta entry Fetta 3, R-tts-1 tracciata in Finding aperti, header data aggiornato |

## Commit di sessione

```
0cf8fb9 docs(fine-task): report FASE 3 Fetta 3 — TTS ElevenLabs output voice
4380f65 feat(voice): FASE 3 Fetta 3 — TTS output via ElevenLabs su POST /voice
20c61c9 chore(revisore): memoria review #89 — APPROVATO CON RISERVE
+ commit fine-task (questo file)
```

## Nota push

Il branch `feat/voice-tts-output` non è stato pushato durante la sessione (classifier auto mode ha bloccato `git push`). Push e PR richiedono intervento manuale dell'operatore.
