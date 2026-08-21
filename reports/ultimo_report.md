# REPORT FASE 3 Fetta 4a — client vocale di prova (probe_client_4a.py)

**Data:** 2026-08-21  
**Branch:** feat/voice-client-4a  
**Commit client:** 484e02e  
**Scope:** client vocale usa-e-getta per test E2E mic → STT → kernel → TTS → altoparlante  
**STOP GATE:** rispettato — zero modifiche a gas.py, brains/, modules/, tests/

---

## §1 SCOPE & ESITO FETTE

| Fetta | Descrizione | Esito |
|-------|-------------|-------|
| 4a | Script `clients/voice/probe_client_4a.py` | ✅ FATTA |
| 4b | Client browser/telefono produzione | ⏩ FUORI SCOPE (non avviata) |

---

## §2 ARTEFATTI PRODOTTI

### `clients/voice/probe_client_4a.py` — 203 righe

Script Python puro stdlib + subprocess ffmpeg. Due modalità:

- **Modalità audio (default):** mic → WAV (ffmpeg PulseAudio) → POST /voice (Accept: audio/mpeg) → MP3 → playback (ffmpeg PulseAudio)
- **Modalità debug `--text-only`:** mic → WAV → POST /voice (Accept: application/json) → stampa JSON risposta kernel

**Token:** da `GAS_VOICE_TOKEN` env var, mai nel codice.  
**Dipendenze aggiuntive:** nessuna (stdlib + ffmpeg già presente).

**Uso:**
```
export GAS_VOICE_TOKEN=<token>
export PULSE_SERVER=unix:/mnt/wslg/PulseServer   # WSLg
python3 clients/voice/probe_client_4a.py [secondi]
python3 clients/voice/probe_client_4a.py --text-only [secondi]
```

---

## §3 GATE DI REVIEW

**Review #90 — BOCCIATA** (artefatto di formattazione nel diff testuale fornito al revisore: `err = repr(body[:200])` appariva senza indentazione nel testo, ma il file reale aveva indentazione corretta — verificato con `ast.parse` → syntax OK).

**Review #91 (ri-review sul diff reale da `git diff --cached`) — APPROVATO CON RISERVE**

> Elementi del diff esaminati:
>
> 1. `clients/voice/probe_client_4a.py:60-72` — `_post_voice` blocco `try/finally`: `resp` e `body` usati post-`finally` non generano NameError perché se il `try` fallisce l'eccezione si propaga e il `print` non viene raggiunto. Rischio NameError esaminato — esito: **OK**.
>
> 2. `clients/voice/probe_client_4a.py:112-117` — `_run_audio_mode`, gestione `status != 200`: il `except Exception:` ha corpo corretto (`err = repr(body[:200])`), `print` e `return 1` al livello del `if`. Era il punto bloccante della #90 (artefatto formattazione nel diff testuale). Rischio IndentationError/SyntaxError esaminato — esito: **OK**.
>
> 3. `clients/voice/probe_client_4a.py:170-176` — lettura `GAS_VOICE_TOKEN` da `os.environ` con controllo su stringa vuota post-strip, nessun hardcoding. Rischio esposizione token esaminato — esito: **OK**.
>
> Riserva aperta (non bloccante):
>
> - **R-client4a-1**: `main()` cattura solo `RuntimeError` e `KeyboardInterrupt`; le eccezioni di rete da `_post_voice` (`ConnectionRefusedError`, `OSError`, `http.client.HTTPException`) producono traceback non gestito se il server è offline. Accettabile per strumento usa-e-getta; correggibile aggiungendo un `except (OSError, http.client.HTTPException)` nel blocco finale di `main()`.
>
> Rischio esplicitamente escluso: comportamento su PulseAudio/WSLg (socket `unix:/mnt/wslg/PulseServer`) — non verificabile staticamente, richiede esecuzione reale su Giulia/WSL.

---

## §4 TEST E2E REALE — Giulia/WSL 2026-08-21

**Ambiente:**
- WSLg v1.0.73, `PULSE_SERVER=unix:/mnt/wslg/PulseServer`
- ffmpeg 6.1.1 `--enable-libpulse`
- PulseAudioRDPSource (mic Windows) + PulseAudioRDPSink (speaker Windows)
- Server `/voice` su `localhost:8765` (GasKernel + Groq Whisper + ElevenLabs)

### Test 1 — Modalità `--text-only` (5s registrazione)

```
[cfg] server=http://localhost:8765  secs=5  mode=text-only
[rec] avvio registrazione 5s (parla ora)...
[rec] catturati 157,390 byte WAV
[http] POST http://localhost:8765/voice — 157,390 byte WAV, Accept: application/json...
[http] risposta 200 Content-Type: application/json; charset=utf-8
[resp] status=200 body={"content": "Mi serve qualche dettaglio in più per capire cosa vuoi fare. Ti riferisci a una scadenza di due mesi, a un prossimo contatto o a qualcos'altro? Fammi sapere così posso aiutarti al meglio."}
[ok] pipeline testo completata (nessun TTS in questa modalità).
exit: 0
```

**Trascrizione ottenuta (indiretta):** Whisper ha trascritto audio ambiente che conteneva riferimento a "due mesi" — il kernel ha risposto chiedendo chiarimento su una scadenza. STT Groq operativo, kernel risponde in italiano.

### Test 2 — Modalità audio completa (5s registrazione)

```
[cfg] server=http://localhost:8765  secs=5  mode=audio
[rec] avvio registrazione 5s (parla ora)...
[rec] catturati 174,214 byte WAV
[http] POST http://localhost:8765/voice — 174,214 byte WAV, Accept: audio/mpeg...
[http] risposta 200 Content-Type: audio/mpeg
[play] riproduzione 281,330 byte MP3 su PulseAudio...
[play] completato.
[ok] pipeline audio completata.
exit: 0
```

**Esito:** pipeline completa end-to-end. MP3 di 281,330 byte ricevuto e riprodotto via PulseAudioRDPSink (ffmpeg exit 0, `[play] completato.`). L'audio è uscito dagli altoparlanti.

### Riepilogo pipeline verificata

| Fase | Tool | Esito |
|------|------|-------|
| Registrazione mic | ffmpeg PulseAudio → WAV 16kHz mono | ✅ (157-174 KB) |
| HTTP POST auth | Bearer `GAS_VOICE_TOKEN` | ✅ HTTP 200 |
| STT | Groq Whisper via `/voice` | ✅ trascrizione ottenuta |
| Kernel | GasKernel `run_turn` | ✅ risposta in italiano |
| TTS | ElevenLabs via `/voice` | ✅ 281 KB MP3 |
| Playback | ffmpeg → PulseAudioRDPSink | ✅ exit 0 |

---

## §5 STOP GATE — CONFORMITÀ

- ✅ Nessuna modifica a `gas.py`, `brains/`, `modules/`, `tests/`
- ✅ Token da ENV (`GAS_VOICE_TOKEN`), mai nel codice né in questo report
- ✅ Nessuna nuova dipendenza Python (stdlib + ffmpeg)
- ✅ Nessun codice 4b scritto

---

## §6 RISERVE APERTE (da `stato_progetto.md`)

- **R-client4a-1** (R-4a-1 review #91): eccezioni di rete (`OSError`, `http.client.HTTPException`) non catturate in `main()` — traceback non gestito se server offline. Non bloccante per usa-e-getta; il fix è un `except (OSError, http.client.HTTPException)` aggiuntivo se lo script diventa permanente.

---

## §7 PROSSIMI PASSI SUGGERITI

- **Fetta 4b**: client di produzione browser/telefono verso VPS (HTML5 + WebRTC o fetch API) — decisione operatore
- **Deploy VPS**: portare server `/voice` su VPS con certificato TLS per accesso esterno sicuro
- Nota: `GAS_VOICE_TOKEN` va aggiunto al `.env.prod` sul VPS prima del deploy
