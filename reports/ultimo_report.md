# SONDA — Client Vocale FASE 3 (Ambiente Giulia/WSL)

**Data**: 2026-08-21  
**Branch**: `sonda/voice-client-env`  
**Scope**: ricognizione pura — nessun codice scritto, nessuna dipendenza installata.

---

## DECISIONI UMANE RICHIESTE

1. **Merge PR `sonda/voice-client-env` (PR #72)** — doc-only, nessun codice motore, nessun revisore richiesto. ✅ IP scrubbing eseguito (2026-08-21): invariante gasmerge PASS — pronto per `gasmerge 72`.
2. **Scelta fetta client vocale**: Fetta 4a (script WSL + ffmpeg, robusto, headless) o Fetta 4b (file HTML5 browser, zero installazioni, prototipo immediato)? Dettaglio in fondo al report.

---

## Esito fette/scope

- **Punto 1 — Device audio Giulia/WSL**: `FATTA` — backend WSLg v1.0.73 build 2, play→Windows testato.
- **Punto 2 — Librerie cattura/play**: `FATTA` — zero Python audio libs; ffmpeg 6.1.1 unica via.
- **Punto 3 — D1-ter IP WSL instabile**: `FATTA` — localhost:8765 via WSL2 forwarding (default attivo).
- **Stop gate — nessun codice scritto**: `RISPETTATO` — solo reports/ modificati.

---

---

## Punto 1 — Device audio su Giulia/WSL

### Backend rilevato: WSLg v1.0.73 build 2

PulseAudio **non gira** come processo Linux (`pulseaudio`/`pipewire`: not running).  
Il server audio è ospitato lato WSLg (Windows Audio ↔ RDP), raggiungibile via:

```
PULSE_SERVER=unix:/mnt/wslg/PulseServer   # socket presente, srwxrwxrwx
```

**Dispositivi rilevati in `/mnt/wslg/`:**

| Dispositivo | Tipo | Stato |
|---|---|---|
| `PulseAudioRDPSink` | Output (speaker Windows) | presente e connesso |
| `PulseAudioRDPSource` | Input (microfono Windows) | presente |
| `PulseServer` | Socket Unix IPC | `srwxrwxrwx`, accessibile |

**Log WSLg confirma connessione attiva:**
```
E: [rdp-sink] module-rdp-sink.c: RDP Sink - Trying to connect to /mnt/wslg/PulseAudioRDPSink
E: [rdp-sink] module-rdp-sink.c: RDP Sink - Connected to fd 20
```

**Variabili ambiente WSLg (già settate nella shell):**
```
DISPLAY=:0
PULSE_SERVER=unix:/mnt/wslg/PulseServer
WAYLAND_DISPLAY=wayland-0
```

### Play audio WSL → Windows speaker: FUNZIONA

Test reale eseguito:
```bash
PULSE_SERVER="unix:/mnt/wslg/PulseServer" \
  ffmpeg -v error -i probe_tts_output.mp3 -f pulse -t 0.1 "test_sink"
# exit 0, output vuoto = nessun errore
```
ffmpeg ha riprodotto 0.1 s di MP3 via PulseAudio RDP sink verso Windows Audio, senza errori.

**Cattura microfono**: tecnicamente possibile via `ffmpeg -f pulse -i default` con lo stesso `PULSE_SERVER`, ma **non testata** (fuori scope sonda). Il `PulseAudioRDPSource` è presente.

---

## Punto 2 — Librerie audio disponibili

### Python (venv Gas)

```
sounddevice  → NOT FOUND
pyaudio      → NOT FOUND
pydub        → NOT FOUND
playsound    → NOT FOUND
```

**Nessuna libreria Python audio è installata nel venv.**

### Tool di sistema

| Tool | Stato | Note |
|---|---|---|
| `ffmpeg` 6.1.1 | ✅ INSTALLATO | `--enable-libpulse`, `--enable-alsa`, `--enable-libjack`, `--enable-sdl2`; sia output (`-f pulse`) che input (`-f pulse -i`) |
| `aplay` / `arecord` | ❌ MANCANTE | `alsa-utils` non installato (disponibile via apt) |
| `sox` | ❌ MANCANTE | — |
| `mpv` | ❌ MANCANTE | — |
| `mplayer` | ❌ MANCANTE | — |

### Conclusione librerie

**ffmpeg è l'unica via funzionante ora, senza installare nulla.**  
- Play MP3 → speaker Windows: `ffmpeg -f pulse "sink" < audio.mp3` via subprocess  
- Record mic → PCM/WAV: `ffmpeg -f pulse -i default -t N output.wav` via subprocess  
- Conversione formato (WAV/WEBM → MP3): ffmpeg nativo  

Per un client Python lo strumento corretto resta `subprocess + ffmpeg` (zero dipendenze extra).

---

## Punto 3 — D1-ter: IP WSL instabile tra reboot

### Stato corrente

```
IP WSL:       <IP-WSL redatto> (dinamico, /20)
Hostname:     Giulia
Gateway/host: <gateway redatto>
DNS/nameserver: <DNS redatto>
/etc/wsl.conf: [boot] systemd=true; [user] default=gqual
```

L'IP cambia a ogni reboot. `avahi-daemon` non installato → nessun mDNS → `Giulia.local` non funziona.

### Opzioni stabili (diagnosi, nessuna implementata)

| Opzione | Funziona? | Requisiti | Raccomandazione |
|---|---|---|---|
| **`localhost:8765`** — Windows WSL2 forwarding | ✅ **Di default attivo** in WSL2 + Win 11 | Nessuno (built-in) | **Preferita per client Windows locale** |
| `networkingMode=mirrored` in `.wslconfig` | ✅ se Win 11 22H2+ | Aggiunta 1 riga in `C:\Users\<user>\.wslconfig` | Alternativa pulita, mirrors tutto il networking |
| Avahi mDNS (`Giulia.local`) | ✅ se installato | `apt install avahi-daemon` + Bonjour su Windows | Utile per client multi-device ma richiede installazione |
| IP fisso in Windows `hosts` | ⚠️ fragile | Aggiornamento manuale a ogni reboot | Da evitare |

**Per il client vocale su Giulia/Windows**: il punto di contatto naturale è `http://localhost:8765` dal lato Windows — il localhost forwarding WSL2 è già attivo per default e l'IP WSL è irrilevante.

**Per deploy VPS** (scenario futuro): serve reverse proxy / tunnel (ngrok, Cloudflare, tailscale) — fuori scope di questa sonda.

---

## Proposta design client vocale — fette (NON implementato)

Stop gate rispettato: nessuna riga di codice scritta. Qui il design proposto per la revisione dell'operatore.

### Scenario target: client leggero su Giulia/Windows

Il voice server GAS è già completo (Fette 1+2+3):
- `POST /voice` + JSON → testo in → MP3 out (TTS ElevenLabs)
- `POST /voice` + audio/* → trascrizione Groq → testo → MP3 out (pipeline completa)

### Fetta 4a — Script Bash/Python su WSL (zero dipendenze Windows)

```
[mic Windows]
    → ffmpeg -f pulse -i default (WSLg PulseAudioRDPSource)
    → WAV/PCM chunk (N secondi)
    → POST http://localhost:8765/voice  (multipart/form-data)
    → risposta MP3
    → ffmpeg -f pulse (WSLg PulseAudioRDPSink) → [speaker Windows]
```

- Tutto gira in WSL con subprocess ffmpeg
- Nessuna dipendenza Python extra
- `PULSE_SERVER` già settato nell'env

### Fetta 4b — Client HTML5 + browser Windows (zero installazioni)

```
[mic Windows]
    → MediaRecorder API (WebM/Opus nel browser)
    → fetch("http://localhost:8765/voice", body=audio)
    → risposta MP3 (blob URL)
    → Audio() Web API → speaker Windows
```

- Gira sul browser Windows, zero installazioni
- Richiede `Content-Type: audio/webm` supportato dal server (già supportato da Fetta 2)
- CORS da abilitare in `server.py` se client è file:// o porta diversa
- Nessun codice lato WSL da aggiungere al motore

### Raccomandazione operatore

Fetta 4b (browser HTML5) è la più semplice da prototipare (un file .html statico), non richiede nulla sul sistema e usa il voice server già deployato. Fetta 4a (script WSL) è più robusta per uso headless/VPS ma richiede gestione thread per capture+play non-blocking.

**Decisione: operatore sceglie quale fetta prioritizzare.**

---

## Riepilogo sonda

| # | Punto | Esito |
|---|---|---|
| 1 | Backend audio | WSLg v1.0.73 build 2, socket PulseServer attivo, play→Windows ✅ testato |
| 2 | Librerie | Solo ffmpeg (con libpulse). Zero Python audio libs. |
| 3 | D1-ter IP | `localhost:8765` stabile via WSL2 forwarding (default) |
| Gate | Nessun codice scritto | ✅ STOP gate rispettato |
