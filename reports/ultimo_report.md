# Report FASE 3 Fetta 3 — TTS output ElevenLabs su POST /voice

**Data:** 2026-08-20  
**Branch:** feat/voice-tts-output  
**Commit motore:** 4380f65

---

## DECISIONI UMANE RICHIESTE

1. **Push branch**: `git push -u origin feat/voice-tts-output` — il push è stato bloccato dal classifier in auto mode; eseguire manualmente.
2. **Merge PR**: aprire PR da `feat/voice-tts-output` → `main` e fare merge con `gasmerge` (NON `gh pr merge` da Claude Code).
3. **Rotazione chiave ElevenLabs**: la chiave risulta esposta in chat (2026-08-06) — rotazione da eseguire prima del deploy VPS.  

---

## §1 — SONDA (pre-implementazione)

### Come server.py costruiva la risposta testo (pre-fetta 3)

In `modules/voice/server.py`, dopo il loop `kernel.run_turn(prompt)`, il server raccoglieva l'evento `final` e inviava sempre:
```python
self._send_json(200, {"content": result_content})
```
Nessun path audio in output. Input audio (STT) già presente da Fetta 2; output era sempre JSON.

### ELEVENLABS_API_KEY in env

Presente nel `.env` del progetto — confermato da `grep ELEVENLABS .env`.

### Endpoint ElevenLabs verificato alla fonte

Endpoint reale: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`  
Headers richiesti: `xi-api-key: <key>`, `Content-Type: application/json`  
Body JSON: `{"text": "...", "model_id": "eleven_flash_v2_5", "voice_settings": {...}}`  
Risposta 200: byte audio MP3 grezzi (Content-Type: audio/mpeg)  
Errori: 4xx/5xx → JSON di errore  
Verifica alla fonte: già documentata in `clients/voice/probe/probe_apis.py` e confermata dal `probe_tts_output.mp3` presente (41 KB, creato 2026-08-01 da sonda precedente).

### Voice ID decision

Configurabile via env `ELEVENLABS_VOICE_ID`.  
Default hardcoded: `"JBFqnCBsd6RMkjVDRZzb"` (George — voce premade ElevenLabs, sempre disponibile).  
Il valore reale nel `.env` del progetto (`CwhRBWXzGAHq8TQ4Fs17`) ha funzionato nell'E2E.

---

## §2 — IMPLEMENTAZIONE

### File creati/modificati

| File | Tipo | Descrizione |
|------|------|-------------|
| `modules/voice/tts.py` | NUOVO | `synthesize_speech()` + `ElevenLabsTTSError`, stdlib `http.client`, zero nuove dipendenze |
| `modules/voice/server.py` | MODIFICATO | `_wants_audio()`, `_send_audio()`, `_do_tts_response()` — branch output audio |
| `tests/test_unit_voice_tts.py` | NUOVO | 17 test unit con transport iniettato |

### Meccanismo Accept header

Il client segnala di volere audio via header HTTP standard:
- `Accept: audio/mpeg` → route TTS
- `Accept: audio/*` → route TTS
- Assente / `Accept: application/json` / qualsiasi altro → JSON invariato (retrocompatibilità)

Non è stato aggiunto un query param `?audio=1` o simili: l'HTTP `Accept` è il pattern canonico per content negotiation.

### Fail-closed garantiti

| Condizione | Comportamento |
|-----------|---------------|
| `ELEVENLABS_API_KEY` assente | 503 — mai crash |
| `result_content` vuoto (`""`) | 200 JSON `{"content": ""}` senza chiamare ElevenLabs |
| ElevenLabs 4xx/5xx | 502 + log warning (senza chiave nei log) |
| OSError (rete/timeout) | 502 + log warning |
| Nessun header Accept | Risposta JSON invariata (retrocompat) |

### Zero nuove dipendenze

Tutto via stdlib: `http.client`, `json`. Nessun SDK ElevenLabs, nessun `requests`.

---

## §3 — TEST

### Unit test con rete isolata: 17/17 PASS

| Gruppo | Test | Esito |
|--------|------|-------|
| TVT-route | no_accept_returns_json | PASS |
| TVT-route | accept_audio_mpeg_routes_to_tts | PASS |
| TVT-route | accept_audio_wildcard_routes_to_tts | PASS |
| TVT-route | accept_json_returns_json | PASS |
| TVT-err | no_key_returns_503 | PASS |
| TVT-err | empty_text_returns_json_200 | PASS |
| TVT-err | elevenlabs_error_returns_502 | PASS |
| TVT-err | network_error_returns_502 | PASS |
| TVT-synth | synth_ok_returns_bytes | PASS |
| TVT-synth | synth_sends_correct_headers | PASS |
| TVT-synth | synth_sends_correct_path | PASS |
| TVT-synth | synth_non200_raises_error | PASS |
| TVT-synth | synth_401_raises_error | PASS |
| TVT-synth | synth_oserror_propagates | PASS |
| TVT-synth | synth_key_not_logged | PASS |
| TVT-synth | default_voice_id_defined | PASS |
| TVT-synth | server_uses_default_voice_when_env_absent | PASS |

### Suite completa voice (nessuna regressione)

```
tests/test_unit_voice_server.py  — 18 PASS (Fetta 1, invariata)
tests/test_unit_voice_stt.py     — 29 PASS (Fetta 2, invariata; nota: 47 include entrambe)
tests/test_unit_voice_tts.py     — 17 PASS (Fetta 3, nuova)
TOTALE VOICE                        64 PASS, 0 FAIL
```

### End-to-end REALE contro ElevenLabs

**Testo inviato:** `"Ciao, sono Gas, il tuo assistente vocale. Fetta tre: sintesi vocale attiva."`  
**Voice ID usato:** `CwhRBWXzGAHq8TQ4Fs17` (da env `.env`)  
**Esito:** 200 OK  
**Dimensione MP3:** 88.2 KB  
**Formato verificato:** `file e2e_tts_fetta3.mp3` → `Audio file with ID3 version 2.4.0, contains: MPEG ADTS, layer III, v1, 128 kbps, 44.1 kHz, Monaural`  
**header ID3:** True — audio valido e riproducibile.  
File salvato in `e2e_tts_fetta3.mp3` (non versionato).

---

## §4 — REVISORE #89

**Verdetto: APPROVATO CON RISERVE**

Elementi esaminati dal revisore:
1. `modules/voice/tts.py:60-72` — blocco `try/finally` della connessione HTTPS — copre `OSError` e `ElevenLabsTTSError`; nessun `json.loads` su risposta 200 (la risposta è byte MP3, quindi la lezione #88 su `JSONDecodeError` è inapplicabile per costruzione); `finally: conn.close()` garantisce no-leak. **OK.**
2. `modules/voice/server.py:165-199` — funzione `_do_tts_response` — api_key assente → 503, testo vuoto → JSON 200 senza chiamata ElevenLabs, `ElevenLabsTTSError` → log warning + 502 (senza esporre la chiave), `OSError` → 502. Fail-safe §9 pienamente rispettato. **OK con riserva minore.**

**Riserva R-tts-1 (non bloccante):** nessun cap esplicito sul testo inviato a ElevenLabs. Il fail-safe regge (ElevenLabs risponde 4xx → catturato → 502 controllato), ma il comportamento su testi lunghissimi è implicito. Tracciata in `stato_progetto.md` §Finding aperti.

**Re-revisione dopo riserva:** R-tts-1 è non bloccante e non richiede fix immediato → nessuna ri-review (conforme alla lezione R-stt-1: ri-review solo su riserve bloccanti risolte prima del commit).

---

## §5 — CAVEAT SICUREZZA (obbligatorio per spec)

**(a) Egress testo kernel → ElevenLabs (terza parte)**  
Il testo prodotto dal kernel GAS esce verso i server ElevenLabs per la sintesi vocale. Dichiarato in `CAVEAT PRIVACY (TTS)` nella docstring di `modules/voice/server.py`. Per un agente che tocca dati/lead, questo è egress di contenuto: trade-off dichiarato, decisione operatore.

**(b) Chiave ElevenLabs esposta in chat e non ruotata**  
La chiave ElevenLabs risulta esposta in chat (2026-08-06) e non ruotata. Rischio accettato dall'operatore. Resta compromessa a prescindere da questa fetta. **Decisione di rotazione da riprendere prima del deploy VPS.** Questa nota è nel report e non nelle note di codice.

---

## §6 — STOP GATE

- STT (`stt.py`) non toccata ✅
- `gas.py` / kernel internals non toccati ✅
- Cascata provider non toccata ✅
- Auth bearer non toccata ✅
- Scope limitato a output audio su `/voice` ✅
