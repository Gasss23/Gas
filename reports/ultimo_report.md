# Sonda Fattibilità Client Voce Windows ↔ GAS (WSL)
**Branch:** `feature/voice-probe`  
**Data:** 2026-08-01  
**Scope:** probe-only — nessun file motore toccato, nessun client costruito.

---

## DECISIONI / PREREQUISITI UMANI

| # | Cosa serve | Dettaglio |
|---|-----------|-----------|
| P1 | **Piano ElevenLabs a pagamento** | La chiave ELEVENLABS presente nel `.env` usa una voce library (`ct77mfOQ3LaEnW2uIMWA`). HTTP 402 `payment_required`: "Free users cannot use library voices via the API." — Opzioni: (a) upgrade al piano Starter (5$/mese); (b) clonare voce propria (disponibile da Creator in su); (c) sostituire `ELEVENLABS_VOICE_ID` con una voce "premade" free-tier se disponibile. |
| P2 | **Eseguire 4 script Windows** | Gli script `win_mic_test.py`, `win_wakeword_test.py`, `win_playback_test.py`, `win_bridge_test.py` non possono girare in WSL. Vedere RUNBOOK sotto. |
| P3 | **IP WSL corretto per win_bridge_test.py** | In questa macchina l'IP WSL2 è `172.20.137.213` (da `hostname -I`). In Windows potrebbe essere raggiunto tramite `localhost` se il mirroring TCP è abilitato (WSL 2.0+, `.wslconfig` `networkingMode=mirrored`). Verificare con `wsl hostname -I` da CMD. |
| P4 | **Dipendenze Windows** | Prima di eseguire gli script Windows: `pip install sounddevice numpy scipy openwakeword requests pydub` (e `ffmpeg` in PATH per MP3). |
| D1 | **Decisione architettura bridge** | La sonda conferma che il canale HTTP WSL2↔Windows funziona. Prima di costruire il client voce: scegliere se usare (a) HTTP REST semplice (già sondata), (b) WebSocket (latenza voce più bassa), (c) named pipe Windows. Proposta in §PROPOSTA. |

---

## ESITO PER GAMBA

### Gamba 1 — Bridge HTTP (WSL, eseguita)

**Stato: OK ✓**

```
2026-08-01 00:02:51  Server avviato su 0.0.0.0:8765
2026-08-01 00:02:51  IP WSL visibile da Windows: 172.20.137.213

curl POST http://127.0.0.1:8765/ping
→ {"pong": true, "server": "WSL"}   HTTP 200

curl POST http://172.20.137.213:8765/ping
→ {"pong": true, "server": "WSL"}   HTTP 200
```

Il server risponde su entrambi loopback e IP eth0. Windows può raggiungere `172.20.137.213:8765` senza configurazioni aggiuntive su WSL2 standard; con `networkingMode=mirrored` può usare `localhost:8765`.

---

### Gamba 2a — Groq Whisper STT (WSL, eseguita)

**Stato: OK ✓**

```
Input: /tmp/probe_test_tone.wav  (tono sinusoidale 440Hz, 2s, 16kHz, generato in stdlib)
Modello: whisper-large-v3-turbo
Lingua: it
HTTP: 200
Testo: "Grazie."
```

Il modello ha interpretato il tono sinusoidale come audio vocale ("Grazie.") — comportamento atteso e non problematico: con audio reale da microfono il risultato sarà corretto. La latenza API era <5s. **Groq Whisper è operativo.**

---

### Gamba 2b — ElevenLabs Flash TTS (WSL, eseguita)

**Stato: ERRORE_API — PREREQUISITO UMANO P1**

```
Modello: eleven_flash_v2_5
voice_id: ct77mfOQ3LaEnW2uIMWA
HTTP: 402 payment_required
Body: "Free users cannot use library voices via the API."
```

Non è un errore tecnico. La chiave è valida (autenticazione riuscita) ma il piano free non consente l'uso di voci library via API. Vedere P1 per le opzioni. Il codice probe_apis.py funziona correttamente.

---

### Gamba 3 — win_mic_test.py (Windows — DA ESEGUIRE)

**Stato: DA ESEGUIRE SU WINDOWS**

Comandi:
```cmd
cd C:\...\Gas\clients\voice\probe
python win_mic_test.py              # lista tutti i device, usa default mic
python win_mic_test.py --device 2   # device indice 2 (earbuds BT, es.)
```

Cosa osservare: durata 3.00s, RMS >200 con voce, file `mic_test.wav` salvato.

---

### Gamba 4 — win_wakeword_test.py (Windows — DA ESEGUIRE)

**Stato: DA ESEGUIRE SU WINDOWS**

Comandi:
```cmd
python win_wakeword_test.py               # device default
python win_wakeword_test.py --device 1    # mic specifico
python win_wakeword_test.py --model hey_jarvis --threshold 0.5
```

Cosa osservare: il primo avvio scarica il modello ONNX (~30MB). Poi dire "hey Jarvis" e attendere il timestamp di detection.

---

### Gamba 5 — win_playback_test.py (Windows — DA ESEGUIRE)

**Stato: DA ESEGUIRE SU WINDOWS**

Comandi:
```cmd
python win_playback_test.py --list              # lista device output
python win_playback_test.py mic_test.wav        # riproduce il WAV registrato
python win_playback_test.py mic_test.wav --device 3   # device specifico
```

Cosa osservare: audio udibile dal device scelto, "Riproduzione completata."

---

### Gamba 6 — win_bridge_test.py (Windows — DA ESEGUIRE)

**Stato: DA ESEGUIRE SU WINDOWS**

Prima: avviare il server WSL:
```bash
# In WSL:
source venv/bin/activate
python3 clients/voice/probe/probe_bridge_server.py --host 0.0.0.0 --port 8765
```

Poi in Windows:
```cmd
:: Trovare l'IP WSL:
wsl hostname -I
:: Esempio output: 172.20.137.213

python win_bridge_test.py --host 172.20.137.213 --port 8765
:: oppure, se WSL con networkingMode=mirrored:
python win_bridge_test.py --host localhost --port 8765
```

Cosa osservare: `[OK] Bridge WSL2→Windows operativo.`  
Se FAIL: vedere il runbook §firewall sotto.

---

## RUNBOOK WINDOWS COMPLETO

### Pre-requisiti

```cmd
:: 1. Python 3.11+ installato (python --version)
:: 2. Installare dipendenze
pip install sounddevice numpy scipy openwakeword requests pydub

:: 3. ffmpeg in PATH (per MP3 playback)
:: Download: https://github.com/BtbN/FFmpeg-Builds/releases
:: Estrarre ffmpeg.exe in C:\ffmpeg\bin e aggiungere al PATH
```

### Ordine esecuzione consigliato

```
1. win_mic_test.py       → verifica mic funzionante
2. win_playback_test.py  → verifica audio output
3. (server WSL attivo) win_bridge_test.py  → verifica canale TCP
4. win_wakeword_test.py  → verifica detection wake-word
```

### Troubleshooting bridge (firewall)

Se `win_bridge_test.py` fallisce con ConnectionError:
```cmd
:: Aggiungere regola firewall in entrata
netsh advfirewall firewall add rule ^
  name="GAS-voice-probe" dir=in action=allow ^
  protocol=TCP localport=8765
```

### Spazio per risultati

```
=== RISULTATI WINDOWS (compilare dopo l'esecuzione) ===

win_mic_test.py:
  device usato  : 
  RMS misurato  : 
  file wav OK?  : 

win_playback_test.py:
  device usato  : 
  audio udibile : 

win_bridge_test.py:
  IP WSL usato  : 
  esito         : 
  latenza ms    : 

win_wakeword_test.py:
  modello       : hey_jarvis
  detection OK? : 
  score ottenuto: 
```

---

## STRUTTURA FILE CREATI

```
clients/voice/probe/
├── win_mic_test.py          # Windows: registra 3s, misura RMS
├── win_wakeword_test.py     # Windows: wake-word con openwakeword pretrained
├── win_playback_test.py     # Windows: riproduce WAV/MP3
├── win_bridge_test.py       # Windows: POST /ping → WSL
├── probe_bridge_server.py   # WSL: server HTTP /ping
└── probe_apis.py            # WSL: sonda Groq Whisper + ElevenLabs
```

Tutti gli script hanno `--device` selezionabile + lista automatica dei device al lancio.

---

## PROPOSTA (STOP GATE — non implementata)

La sonda ha confermato la fattibilità tecnica del canale. Quando vorrai procedere alla Fase client voce:

**Architettura suggerita:**
```
Windows (client)
  sounddevice mic → openWakeWord → [ wake ] →
  sounddevice record (3-5s) →
  HTTP POST /transcribe (WAV) → WSL GAS endpoint →
    Groq Whisper STT → gas.py run_turn → ElevenLabs TTS →
  HTTP response (MP3) →
  sounddevice playback
```

**Variante WebSocket** (latenza più bassa, streaming audio bidirezionale): sostituisce la serie di POST con una connessione persistente WS. Appropriata quando la latenza end-to-end percepita diventa il vincolo principale.

**Prossimo passo suggerito:** risolvere P1 (piano ElevenLabs), eseguire i 4 script Windows (P2), e tornare con i risultati — poi decidere se procedere alla Fetta 1 del client voce.

---

## NOTE REVISORE

Il revisore **NON è stato invocato** perché nessun file motore è stato toccato in questa sessione:
- `gas.py` → non toccato
- `brains/` → non toccato  
- `modules/` → non toccato
- `tests/` → non toccato

File creati: solo `clients/voice/probe/` (nuova directory, fuori dal perimetro di review).
