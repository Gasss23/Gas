# Diff sessione — 2026-08-01

Task: Sonda fattibilità client voce Windows ↔ GAS (WSL) — `feature/voice-probe`

## File toccati

| File | Cosa | Perché |
|------|------|--------|
| `clients/voice/probe/win_mic_test.py` | Nuovo — script Windows registrazione mic | Sonda gamma mic: 3s, salva WAV, stampa RMS, device selezionabile |
| `clients/voice/probe/win_wakeword_test.py` | Nuovo — script Windows wake-word | Sonda openWakeWord pretrained (hey_jarvis), detection con timestamp |
| `clients/voice/probe/win_playback_test.py` | Nuovo — script Windows playback | Sonda riproduzione WAV/MP3 su device scelto |
| `clients/voice/probe/win_bridge_test.py` | Nuovo — script Windows bridge test | POST /ping → WSL per verificare forwarding TCP WSL2→Windows |
| `clients/voice/probe/probe_bridge_server.py` | Nuovo — server HTTP WSL | Server stdlib (no deps) con endpoint POST /ping; testato con curl, OK su 127.0.0.1 e 172.20.137.213:8765 |
| `clients/voice/probe/probe_apis.py` | Nuovo — probe API WSL | Groq Whisper STT (OK, HTTP 200) + ElevenLabs Flash TTS (ERRORE_API 402 piano free) |
| `reports/ultimo_report.md` | Sovrascritto — report sonda | Report canonico con decisioni umane, esiti per gamba, runbook Windows completo |

## Cosa NON è stato toccato

- `gas.py`, `brains/`, `modules/`, `tests/` — nessuna modifica al motore
- Il revisore non è stato invocato (corretto: perimetro non interessato)
