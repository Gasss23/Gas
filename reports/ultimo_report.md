# REPORT — FASE 3 Fetta 4b: Client Vocale Browser HTML5

**Branch**: `feat/voice-client-4b`
**Data**: 2026-09-15
**Stato**: ✅ COMPLETO — FETTA A pulita + FETTA B eseguita

---

## PASSO 0 — Setup

- Branch creato: `feat/voice-client-4b`
- Revisore: `.claude/agents/revisore.md` ✅ presente
- venv `.venv` attivata, Python 3.14.7

---

## FETTA A — SONDA (sola lettura)

### A1 — Avvio server

Comando di avvio:
```bash
python3 -c "from modules.voice.server import run_server; import sys; sys.exit(run_server())"
```

- **Porta**: 8765
- **Bind**: `127.0.0.1` (loopback, confermato da `lsof`: `localhost:ultraseek-http`)
- **Esposizione LAN**: NESSUNA — solo loopback per design del server

Note: `python -m modules.voice.server` NON funziona (nessun blocco `__main__` nel modulo). Il comando corretto è il one-liner sopra, oppure avviare da `gas.py` se integrato.

### A2 — Giro voce REALE

**Test testo → JSON (kernel senza TTS)**:
- POST `http://127.0.0.1:8765/voice` con `Content-Type: application/json`, `Accept: application/json`
- Body: `{"prompt": "Ciao Gas, rispondi in una sola parola: funziona?"}`
- Risposta: `{"content": "Sì."}` — HTTP 200, 19 B, **1.65s**

**Test testo → MP3 (ElevenLabs TTS live)**:
- POST `Accept: audio/mpeg`
- Risposta: HTTP 200, **13.000 B MP3** (ID3 v2.4, MPEG layer III, 128 kbps, 44.1 kHz), **3.83s**

**Test audio WAV → MP3 (Groq STT + kernel + ElevenLabs TTS)**:
- WAV generato: 16kHz mono, 1s, 32.044 B (sine 440Hz)
- Risposta: HTTP 200, **7.149 B MP3** (ID3 v2.4, validato con `file`), **8.47s**
- Conferma pipeline live: Groq `whisper-large-v3` + GasKernel + ElevenLabs Flash

**STOP GATE**: server parte ✅, giro voce reale funziona ✅ → FETTA B autorizzata

### A3 — CORS e approccio serving

Il server NON ha CORS headers né `do_OPTIONS`. Analisi opzioni:

| Approccio | Modifica server.py | Sicurezza | Semplicità |
|---|---|---|---|
| Proxy stdlib in `clients/voice/` | ❌ NO | ✅✅ (token mai in browser) | ✅ un comando |
| CORS headers in server.py | ✅ SÌ | ✅ (origin limitabile) | ✅ ma tocca modules/ |
| Serve HTML dallo stesso server | ✅ SÌ | ✅✅ | ✅ ma tocca modules/ |

**Scelta**: proxy stdlib — zero modifiche a `modules/`, same-origin naturale, token aggiunto dal proxy (mai nel browser).

### A4 — Rotazione GAS_VOICE_TOKEN

Il token precedente era esposto nella conversazione/output. Rigenerato con:
```bash
openssl rand -hex 32
```

Aggiornato in `.env`. **Il nuovo token NON è stampato in questo report né nei log.**

---

## FETTA B — CLIENT BROWSER

### File creati

**`clients/voice/browser_server.py`** (proxy, 140 righe):
- Bind: `127.0.0.1:9000` (non esposto in LAN)
- `GET /` → serve `browser_client.html` (same dir)
- `POST /voice` → proxy verso `http://127.0.0.1:8765/voice`
  - Aggiunge `Authorization: Bearer <token>` (token da env, mai nel browser)
  - Forwarda `Content-Type` e `Accept` originali del browser
- `.env` caricato automaticamente da `_GAS_ROOT` (due livelli su dalla script)
- Config: `GAS_VOICE_URL` (default `:8765`), `GAS_BROWSER_PORT` (default `9000`)
- Zero nuove dipendenze (stdlib: `http.client`, `http.server`, `urllib.parse`)

**`clients/voice/browser_client.html`** (pagina HTML5):
- `getUserMedia({audio:true})` → `MediaRecorder` (webm/opus, fallback webm/ogg/mp4)
- Click "Registra" → avvio rec | Click "Stop e Invia" → stop + POST `/voice`
- Headers inviati: `Content-Type: audio/webm`, `Accept: audio/mpeg`
- Risposta MP3 → `URL.createObjectURL()` → `<audio>.play()`
- Status monospace mostra byte ricevuti + tempo (es. `4.641 B · 1,9s`)
- Shortcut Space per record/stop
- Tema dark/light auto (CSS tokens, `prefers-color-scheme`)
- Font: Figtree (UI) + JetBrains Mono (status) via Google Fonts

### Test E2E programmático (reale)

Voice server avviato su `:8765`, browser server su `:9000`:

| Test | Status | Bytes | Tempo |
|---|---|---|---|
| `GET /` → HTML | 200 | 25+ char | 31ms |
| `POST /voice` JSON → JSON | 200 | 18 B | 1.31s |
| `POST /voice` WAV → MP3 | 200 | **4.641 B** | **1.87s** |

MP3 di risposta validato: `Audio file with ID3 version 2.4.0, MPEG ADTS layer III, 128 kbps, 44.1 kHz, Monaural`.

### Istruzioni uso

```bash
cd ~/Gas && source .venv/bin/activate

# Terminale 1 — voice server
python3 -c "from modules.voice.server import run_server; import sys; sys.exit(run_server())"

# Terminale 2 — browser proxy
python3 clients/voice/browser_server.py

# Browser → http://127.0.0.1:9000
```

---

## GATE DI REVIEW

Il diff di questa sessione tocca SOLO:
- `clients/voice/browser_server.py` (NUOVO)
- `clients/voice/browser_client.html` (NUOVO)
- `.env` (rotazione token)
- `reports/` (questo report + stato_progetto.md)

**Nessun file in `gas.py`, `brains/`, `modules/`, `tests/`** → gate di review obbligatorio NON si attiva.

---

## SCOPE NON TOCCATO

- `modules/voice/server.py` — invariato
- `gas.py` — invariato
- Suite test — invariata (64 PASS precedenti)
- Nessuna nuova dipendenza Python

---

## PROSSIMI PASSI (decisione operatore)

1. **Test browser reale** — aprire http://127.0.0.1:9000 con microfono e parlare
2. **Integrazione avvio** — aggiungere subcommand `gas voice-browser` in gas.py (FASE 4, separata)
3. **macOS audio** — `probe_client_4a.py` usa PulseAudio (Linux/WSL); per Mac nativo serve afrecord/sox o MediaRecorder (già coperto da 4b)
