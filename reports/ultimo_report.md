# Report — FASE 3 Fetta 2: STT server-side Groq Whisper su POST /voice

**Data:** 2026-08-20
**Branch:** feat/voice-stt-input
**Review:** #88 — APPROVATO CON RISERVE

---

## Sonda pre-implementazione

### Come server.py legge il body e invoca il kernel (pre-modifica)
- Legge `Content-Length` → `self.rfile.read(length)` → bytes grezzi
- `json.loads(raw)` → dict → `data.get("prompt")` → stringa
- `self.kernel.run_turn(prompt)` → generator di eventi `{type: "final"|"error"|"tool_res"}`
- Nessun upload su disco, nessun processamento audio: solo testo → kernel → testo

### GROQ_API_KEY già presente nel progetto
- Confermata in `gas.py:1484,1489` (rung Groq cascata provider)
- Letta da `.env` all'avvio del processo → disponibile nell'ambiente del server
- Confermata anche in `tests/test_unit_kernel.py:142` con pattern save/restore

### Endpoint Groq Whisper verificato (fonte: probe_apis.py già nel progetto)
- URL: `https://api.groq.com/openai/v1/audio/transcriptions`
- Modello usato: `whisper-large-v3`
- Formato: `multipart/form-data` con campi `file`, `model`, `response_format`
- Auth: `Authorization: Bearer <key>`
- Risposta 200: `{"text": "<trascrizione>"}`

### Nessun ostacolo rilevato — implementazione proceduta

---

## Implementazione

### Nuovi file

**`modules/voice/stt.py`** — modulo STT standalone, zero dipendenze esterne:
- `GroqSTTError(status, message)` — eccezione tipizzata con status HTTP Groq
- `_build_multipart(audio_bytes, filename)` — costruisce body multipart/form-data con stdlib pura
- `_parse_multipart_file(raw, content_type)` — parser multipart minimale (stdlib, no `cgi` deprecated)
- `parse_audio_body(raw, content_type)` — routing: `audio/*` → bytes raw; `multipart/form-data` → estrae campo `file`
- `transcribe_audio(audio_bytes, filename, api_key, *, _conn_factory=None)` — POST a Groq via `http.client.HTTPSConnection`; `_conn_factory` iniettabile per i test

**`tests/test_unit_voice_stt.py`** — 28 test nuovi (47 totali con i precedenti):
- `TestTranscribeAudio` — 10 test: transport iniettato, tutti i rami errore (400/429/500/rete/non-JSON)
- `TestParseAudioBody` — 7 test: audio raw, mp3, vuoto, multipart valido/invalido, CT non supportato
- `TestVoiceHandlerRouting` — 11 test: routing audio vs JSON, 503 senza chiave, 400 audio vuoto, 400/502 per errori Groq, 502 rete, 400 trascrizione vuota, testo trascritto passato al kernel

### File modificati

**`modules/voice/server.py`**:
- Import top-level `GroqSTTError, parse_audio_body, transcribe_audio` da `modules.voice.stt`
- `do_POST`: rilevamento Content-Type dopo lettura body; routing `is_audio = ct_base.startswith("audio/") or ct_base == "multipart/form-data"`
- Nuovo metodo `_do_stt(raw, content_type) -> Optional[str]`: gestione errori espliciti per ogni scenario; ritorna `None` con risposta HTTP già inviata in caso d'errore
- Path JSON retrocompatibile: INVARIATO
- Docstring aggiornato con nuovi status HTTP (502, 503) e CAVEAT PRIVACY dichiarato

---

## Fail-closed — tabella completa

| Scenario | Codice HTTP | Messaggio |
|---|---|---|
| `GROQ_API_KEY` assente | 503 | "STT non disponibile: GROQ_API_KEY non configurata" |
| Body audio vuoto | 400 | "Audio vuoto" |
| Audio malformato / CT non supportata | 400 | "Audio non valido: ..." |
| Groq risponde 400 (formato non accettato) | 400 | "Formato audio non accettato da Groq: ..." |
| Groq risponde 4xx/5xx (quota, errore) | 502 | "Errore Groq STT: ..." |
| Errore di rete verso Groq | 502 | "Errore di rete verso Groq STT" |
| Groq 200 con body non JSON | 502 (via GroqSTTError) | "risposta Groq non JSON: ..." |
| Trascrizione vuota (silenzio) | 400 | "Trascrizione vuota ..." |
| JSON `{"prompt": ...}` | comportamento attuale | invariato |

---

## Sicurezza

- I byte audio non vengono loggati né scritti su disco in chiaro
- La chiave `GROQ_API_KEY` non compare nei log (`log.warning("... %s", exc)` non la include)
- Audio non persistito: tutto in memoria, GC dopo la risposta HTTP
- **CAVEAT EGRESS DICHIARATO**: l'audio dell'utente viene inviato ai server Groq (terza parte) per la trascrizione. Per un agente che tocca dati/lead, questo è egress di dati vocali. Trade-off: senza API STT di terze parti non c'è alternativa offline senza modello locale (Whisper.cpp su VPS — futura fetta, non in scope). Dichiarato nel docstring di `server.py` e in questo report.

---

## Test

### Test unitari (rete isolata — transport iniettato)

```
tests/test_unit_voice_stt.py   28 test  PASS
tests/test_unit_voice_server.py 19 test  PASS
────────────────────────────────────────────
TOTALE                          47 test  PASS / 0 FAIL
```

Copertura rami d'errore verificata: chiave assente, audio vuoto, CT non supportata, Groq 400/429/500, rete rotta, body non-JSON su 200, trascrizione vuota, routing corretto audio vs JSON, testo trascritto passato verbatim al kernel.

### Test end-to-end reale (Groq live)

- **Input**: `probe_tts_output.mp3` — 40 KB, voce ElevenLabs (generata in sessione precedente con testo "Ciao, sono Gas, il tuo assistente vocale.")
- **Output Groq Whisper large-v3**: `'Ciao, sono Gus, il tuo assistente vocale.'`
- **Esito**: trascrizione corretta ("Gas" → "Gus" per somiglianza fonetica, comportamento normale di Whisper su nome proprio non comune). Pipeline funzionante end-to-end.

---

## Review #88 — Verdetto integrale del revisore

**APPROVATO CON RISERVE**

> **R-stt-1** (minore, non bloccante): `modules/voice/stt.py:149` — `json.loads(resp_body)` su risposta Groq status 200 con body non-JSON solleva `json.JSONDecodeError` non catturata. Fix: avvolgere in `try/except json.JSONDecodeError` e convertire in `GroqSTTError(resp.status, "risposta non JSON: ...")`. Il server non crasha (BaseHTTPRequestHandler la gestisce), ma il client riceve EOF invece di un 502 controllato.

> Commit consentito. Tracciare R-stt-1 in `stato_progetto.md` prima della PR.

**R-stt-1 risolta prima del commit**: il fix è stato applicato in `stt.py` (`try/except json.JSONDecodeError → GroqSTTError`) e coperto dal test `test_groq_200_non_json_body_raises_groq_error`. R-stt-1 chiusa — non tracciata come aperta in `stato_progetto.md`.

---

## File modificati nella sessione

```
modules/voice/stt.py            ← nuovo
modules/voice/server.py         ← modificato (routing + _do_stt)
tests/test_unit_voice_stt.py    ← nuovo
reports/stato_progetto.md       ← aggiornato
reports/ultimo_report.md        ← questo file
```

---

## Prossimi passi (non in scope di questa fetta)

- **TTS output** (Fetta 3): `/voice` risponde con audio invece di JSON testo — ElevenLabs Flash
- **Loopback exemption VPS**: il server ascolta su 127.0.0.1, aprire all'esterno richiede GAS_VOICE_BIND + reverse proxy con TLS
- **Whisper locale** (opzionale, FASE 4+): eliminare egress audio verso Groq con whisper.cpp su VPS
