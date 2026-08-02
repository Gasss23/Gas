# Sonda Fattibilità Client Voce Windows ↔ GAS (WSL) — F0 completata + /fine-task

**Branch:** `feature/voice-probe`
**Data:** 2026-08-02
**Task:** Sonda F0 6/6 gambe verde + doc di sessione canonico (/fine-task).

---

## DECISIONI UMANE RICHIESTE

1. **D1-ter (APERTA):** IP WSL non stabile tra reboot → scegliere `networkingMode=mirrored` in `.wslconfig` (cambia rete intera WSL, da ri-sondare) OPPURE client che risolve IP a runtime. Da decidere PRIMA dell'endpoint Fetta 1.
2. **D2-audio (APERTA, Fetta 2):** (a) client deve usare `load_dotenv(override=True)` o torna il "402-fantasma"; (b) policy device output: default sistema vs esplicito con fallback (rischio device virtuali → audio muto).
3. **AZIONE SICUREZZA:** Rigenerare chiave ElevenLabs esposta in chat a fine validazione + aggiornare `.env` (valore MAI nei file versionati).
4. **Merge PR:** la PR di sessione su `feature/voice-probe` non è ancora mergiata su main — da fare dopo verifica CI verde.

---

## §SCOPE & ESITO FETTE

| Fetta | Stato | Note |
|-------|-------|------|
| Branch `feature/voice-probe` | **FATTA** | Commit `1907fa2` |
| Script Windows 4x (`win_*.py`) | **FATTA** | `clients/voice/probe/` — commit `1907fa2` |
| Server WSL bridge (`probe_bridge_server.py`) | **FATTA** | Testato su `127.0.0.1` e `172.20.137.213:8765` — commit `1907fa2` |
| Script WSL probe API (`probe_apis.py`) | **FATTA** | STT OK; TTS 402 (voice library) risolto in sessione — commit `1907fa2` |
| Gambe Windows eseguite (mic, wakeword, playback, bridge) | **FATTA** | Eseguite in PowerShell con venv `.venv-win` |
| TTS ElevenLabs risolto (voice_id Roger + `load_dotenv(override=True)`) | **FATTA** | HTTP 200, mp3 ~40KB |
| Doc di sessione (handoff + ultimo_report + diff_sessione) | **FATTA** | Questo commit |
| Fetta 1 endpoint WSL + token auth | **DEFERITA** | Dopo decisione D1-ter |

---

## §ESITO SONDA F0

**6/6 verde.** Architettura Windows↔WSL tecnicamente fattibile.

| Gamba | Risultato |
|-------|-----------|
| STT Groq Whisper | HTTP 200 — `whisper-large-v3-turbo` — "Grazie." |
| TTS ElevenLabs Flash v2.5 | HTTP 200 — voce Roger (`CwhRBWXzGAHq8TQ4Fs17`) — mp3 ~40KB |
| Bridge WSL↔Windows | IP `172.20.137.213:8765` — ~20ms (localhost = 2050ms, inutilizzabile) |
| Mic Realtek idx1 | RMS 1428 — segnale vocale OK |
| Playback | Voce sentita dall'altoparlante |
| Wakeword `hey_jarvis` | Score 0.538/0.610 — zero falsi positivi in 60s |

---

## §NOTE OPERATIVE (per non ripetere gli intoppi)

**Dove gira cosa:**
- `win_*.py` → PowerShell Windows, venv `.venv-win` attivo (`.\.venv-win\Scripts\Activate.ps1`).
- `probe_bridge_server.py`, `probe_apis.py` → WSL, venv WSL attivo.
- Se PowerShell nuova: ri-attiva il venv o `where.exe python` darà Hermes come prima riga.

**Path da Windows (UNC WSL):**
```
\\wsl$\Ubuntu-24.04\home\gqual\Gas\clients\voice\probe\
```

**"402-fantasma" ElevenLabs:** `ELEVENLABS_VOICE_ID` esportata in shell WSL scavalcava il `.env`. Fix: `load_dotenv(override=True)` + voice_id premade free-tier (`CwhRBWXzGAHq8TQ4Fs17` = Roger).

**localhost vs IP WSL:** localhost da Windows = 2050ms (muro strutturale forwarding TCP). Usare sempre IP da `hostname -I`.

**openWakeWord:** modelli ONNX già scaricati. Script forzano `inference_framework="onnx"` (TensorFlow assente → ImportError senza questo flag).

**Sicurezza:** chiave ElevenLabs esposta in chat → rigenerare su elevenlabs.io/app/settings/api-keys + aggiornare `.env` locale.
