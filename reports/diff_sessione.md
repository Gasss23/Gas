# Diff Sessione — 2026-08-02

Sessione: sonda fattibilità client voce Windows ↔ GAS (WSL) — F0 completata.

---

## File toccati (da `git diff --stat BASE..HEAD`)

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `clients/voice/probe/probe_apis.py` | Nuovo script WSL: sonda Groq Whisper STT + ElevenLabs Flash TTS. Fix incluso: `load_dotenv(override=True)` per evitare il "402-fantasma" da variabile shell. |
| `clients/voice/probe/probe_bridge_server.py` | Nuovo script WSL: server HTTP `/ping` su `0.0.0.0:8765` per testare il canale TCP WSL↔Windows. |
| `clients/voice/probe/win_bridge_test.py` | Nuovo script Windows: POST `/ping` al server WSL, misura latenza. Conferma che IP WSL (~20ms) è l'unica opzione (localhost = 2050ms). |
| `clients/voice/probe/win_mic_test.py` | Nuovo script Windows: registra 3s da microfono, misura RMS (Realtek idx1 = 1428). |
| `clients/voice/probe/win_playback_test.py` | Nuovo script Windows: riproduce WAV/MP3 dal device scelto. |
| `clients/voice/probe/win_wakeword_test.py` | Nuovo script Windows: detection `hey_jarvis` via openWakeWord ONNX. Score 0.538/0.610, zero falsi positivi. |
| `reports/diff_sessione.md` | Questo file — riepilogo sessione (si riscrive a ogni sessione). |
| `reports/handoff.md` | Dossier sessione con template canonico corretto (§2 GIT DIFF --STAT nel formato atteso da `check_handoff.py`). Sessione precedente usava `§STATO REPO` non riconosciuto dalla CI. |
| `reports/ultimo_report.md` | Report canonico task: scope, esito F0, note operative per non ripetere intoppi. |

---

## Note

- Nessun file motore (`gas.py`, `brains/`, `modules/`, `tests/`) toccato — revisore non richiesto.
- La CI `handoff-check` aveva fallito sul commit `4056c97` (sessione precedente) perché handoff.md mancava del template `## §2 GIT DIFF --STAT` con fence code. Corretto in questo commit.
- La storia completa sta in git; questo file è fotografia dell'ultima sessione.
