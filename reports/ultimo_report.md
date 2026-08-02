# Sonda Fattibilità Client Voce Windows ↔ GAS (WSL) — F0 completata

**Branch:** `feature/voice-probe`
**Data:** 2026-08-02
**Task:** Completamento sonda F0 (6/6 gambe) + doc di sessione. Nessun file motore toccato.

---

## §SCOPE & ESITO FETTE

| Fetta | Stato | Note |
|-------|-------|------|
| Branch `feature/voice-probe` | **FATTA** | Commit `1907fa2` (sessione precedente) |
| Script Windows 4x (`win_*.py`) | **FATTA** | Scritti in `clients/voice/probe/` (sessione precedente) |
| Server WSL bridge (`probe_bridge_server.py`) | **FATTA** | Sessione precedente; testato su `127.0.0.1` e `172.20.137.213:8765` |
| Script WSL probe API (`probe_apis.py`) | **FATTA** | STT OK; TTS 402 in sessione precedente (voice library → risolto sotto) |
| Gambe Windows eseguite | **FATTA** | Eseguite in questa sessione (PowerShell + venv .venv-win) |
| TTS ElevenLabs risolto | **FATTA** | voice_id Roger free-tier + `load_dotenv(override=True)` → HTTP 200, mp3 40KB |
| Doc di sessione (handoff + report) | **FATTA** | Questo commit |
| Fetta 1 endpoint + token auth | **DEFERITA** | Dopo decisione D1-ter (IP stabile) |

---

## §ESITO SONDA F0

**6/6 verde.** La sonda è tecnicamente conclusa; l'architettura Windows↔WSL è fattibile.

| Gamba | Risultato |
|-------|-----------|
| STT Groq Whisper | HTTP 200 — `whisper-large-v3-turbo` — risposta: "Grazie." |
| TTS ElevenLabs Flash v2.5 | HTTP 200 — voce Roger (`CwhRBWXzGAHq8TQ4Fs17`) — mp3 ~40KB |
| Bridge WSL↔Windows | IP `172.20.137.213:8765` — ~20ms (localhost = 2050ms, inutilizzabile) |
| Mic Realtek idx1 | RMS 1428 — segnale vocale OK |
| Playback | Voce sentita dall'altoparlante |
| Wakeword `hey_jarvis` | Score 0.538/0.610 — zero falsi positivi in 60s |

---

## §NOTE OPERATIVE (per non ripetere gli intoppi)

### Dove gira cosa

- **Script `win_*.py`** → PowerShell su Windows, con venv `.venv-win` attivo.
- **Script `probe_bridge_server.py`, `probe_apis.py`** → WSL, con `venv` WSL attivo.

### Attivare il venv Windows (non dimenticare in ogni PowerShell nuova)

```powershell
# Se sei nella dir Gas su Windows:
.\.venv-win\Scripts\Activate.ps1

# Verifica: deve comparire (.venv-win) nel prompt
# Se `where.exe python` dà Hermes come prima riga, il venv non è attivo → riattivarlo.
# Hermes (venv globale Windows) ha i pacchetti ma potrebbe avere versioni diverse.
```

### Path degli script da Windows (UNC WSL)

```
\\wsl$\Ubuntu-24.04\home\gqual\Gas\clients\voice\probe\win_mic_test.py
\\wsl$\Ubuntu-24.04\home\gqual\Gas\clients\voice\probe\win_wakeword_test.py
\\wsl$\Ubuntu-24.04\home\gqual\Gas\clients\voice\probe\win_playback_test.py
\\wsl$\Ubuntu-24.04\home\gqual\Gas\clients\voice\probe\win_bridge_test.py
```

Oppure clonare/mappare il path su un drive Windows per comodità.

### Intoppo ElevenLabs (il "402-fantasma")

Il 402 in sessione precedente era causato da `ELEVENLABS_VOICE_ID` esportata nella shell WSL (da un test precedente con voice library) che scavalcava il valore nel `.env`.
**Fix obbligatorio:** usare `load_dotenv(override=True)` nel client, e usare `voice_id` di voce premade free-tier (`CwhRBWXzGAHq8TQ4Fs17` = Roger).

### Intoppo localhost vs IP WSL

`localhost` da Windows → WSL2 = **2050ms costanti** (10/10 ping) — muro strutturale del forwarding TCP, non un glitch.
Usare sempre l'IP `hostname -I` (WSL). L'IP cambia tra reboot: vedi D1-ter in handoff.md per la decisione pending.

### openWakeWord — modelli già scaricati

I modelli ONNX sono stati scaricati al primo avvio (`hey_jarvis`). Gli script forzano `inference_framework="onnx"` per evitare il fallback su TensorFlow (non installato, causerebbe ImportError).

### Sicurezza

La chiave ElevenLabs è stata esposta in chat durante la sessione di debug → rigenerarla a fine validazione su https://elevenlabs.io/app/settings/api-keys e aggiornare `.env` locale (il valore non va mai in file versionati).
