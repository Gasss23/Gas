# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-08-20 — FASE 3 Fetta 3 — TTS output ElevenLabs su POST /voice

---

## §0 DECISIONI UMANE RICHIESTE

1. **Push branch**: `git push -u origin feat/voice-tts-output` — il push è stato bloccato dal classifier in auto mode durante la sessione; eseguire manualmente.
2. **Merge PR**: aprire PR da `feat/voice-tts-output` → `main` e fare merge con `gasmerge` (NON `gh pr merge` da Claude Code — CLAUDE.md §10 main-lock).
3. **Rotazione chiave ElevenLabs**: la chiave risulta esposta in chat (2026-08-06) e non ruotata. Rotazione da eseguire prima del deploy VPS.

---

## §1 SCOPE & ESITO FETTE

- **Sonda pre-implementazione**: `FATTA` — server.py costruiva risposta JSON invariata; ELEVENLABS_API_KEY presente in .env; endpoint ElevenLabs verificato (`/v1/text-to-speech/{voice_id}`, risposta byte MP3); voice_id configurabile via env con default `JBFqnCBsd6RMkjVDRZzb` (George premade).

- **Fetta 3a — modulo TTS**: `FATTA` — `modules/voice/tts.py` (nuovo): `synthesize_speech()` + `ElevenLabsTTSError`, stdlib `http.client`, zero nuove dipendenze, `_conn_factory` iniettabile per test.

- **Fetta 3b — integrazione server**: `FATTA` — `modules/voice/server.py`: `_wants_audio()` (Accept: audio/mpeg | audio/*), `_send_audio()`, `_do_tts_response()`. Fail-closed: chiave assente → 503, testo vuoto → no call, ElevenLabs error → 502, rete → 502. Retrocompatibilità JSON invariata.

- **Fetta 3c — test unitari isolati**: `FATTA` — `tests/test_unit_voice_tts.py`: 17 test (TVT-route: routing Accept, TVT-err: tutti i rami errore, TVT-synth: synthesize_speech unit con transport iniettato). 64 PASS totali voice, 0 FAIL, 0 regressioni.

- **Fetta 3d — E2E reale**: `FATTA` — testo → ElevenLabs reale → 88.2 KB MP3 (ID3 v2.4, MPEG layer III, 128 kbps, 44.1 kHz, Monaural). File salvato `e2e_tts_fetta3.mp3` (non versionato).

- **Revisore pre-commit**: `FATTA` — Review #89 APPROVATO CON RISERVE. R-tts-1 tracciata (non bloccante).

- **Push branch**: `DEFERITA — classifier auto mode ha bloccato il push; richiede esecuzione manuale dall'operatore.`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 modules/voice/server.py            |  87 ++++++++--
 modules/voice/tts.py               |  75 ++++++++
 reports/diff_sessione.md           |  40 +++--
 reports/handoff.md                 | 117 +++++++------
 reports/stato_progetto.md          |   5 +-
 reports/ultimo_report.md           | 202 +++++++++++----------
 tests/test_unit_voice_tts.py       | 348 +++++++++++++++++++++++++++++++++++++
 8 files changed, 702 insertions(+), 173 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
0cf8fb9 docs(fine-task): report FASE 3 Fetta 3 — TTS ElevenLabs output voice
4380f65 feat(voice): FASE 3 Fetta 3 — TTS output via ElevenLabs su POST /voice
20c61c9 chore(revisore): memoria review #89 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

**Commit motore: `4380f65` — feat(voice): FASE 3 Fetta 3 — TTS output via ElevenLabs su POST /voice**

Verdetto Review #89: **APPROVATO CON RISERVE**

Elementi esaminati dal revisore:

1. `modules/voice/tts.py:60-72` — blocco `try/finally` della connessione HTTPS — copre `OSError` e `ElevenLabsTTSError`; nessun `json.loads` su risposta 200 (la risposta è byte MP3, quindi la lezione #88 su `JSONDecodeError` è inapplicabile per costruzione, non per dimenticanza); `finally: conn.close()` garantisce no-leak. **Esito: ok.**

2. `modules/voice/server.py:165-199` — funzione `_do_tts_response` — api_key assente → 503, testo vuoto → JSON 200 senza chiamata ElevenLabs, `ElevenLabsTTSError` → log warning + 502 (senza esporre la chiave), `OSError` → 502. Fail-safe §9 pienamente rispettato. **Esito: ok con riserva minore.**

**Riserva aperta — R-tts-1 (non bloccante):** nessun cap esplicito sul testo inviato a ElevenLabs. Il fail-safe regge (ElevenLabs risponde 4xx → catturato come `ElevenLabsTTSError` → 502 controllato), ma il comportamento su testi lunghi è implicito. Da tracciare in `stato_progetto.md` e considerare in una fetta successiva.

**Rischio escluso:** compatibilità del voice_id default (`JBFqnCBsd6RMkjVDRZzb`, George) con il piano ElevenLabs attivo dell'operatore — non verificabile senza accesso all'account; l'E2E reale ha già prodotto output MP3, quindi era valido al momento del test.

---

## §5 DELTA TEST DEL MOTORE

- Suite voice pre-fetta 3: **47 PASS** (test_unit_voice_server.py + test_unit_voice_stt.py)
- Suite voice post-fetta 3: **64 PASS** (+17 TVT in test_unit_voice_tts.py)
- 0 FAIL, 0 regressioni.
- `gas.py` non toccato → suite kernel invariata.

Riepilogo reale pytest:
```
============================= test session starts ==============================
collected 17 items
tests/test_unit_voice_tts.py .................                           [100%]
17 passed in 4.46s

============================= 47 passed in 13.31s ==============================
(tests/test_unit_voice_server.py + tests/test_unit_voice_stt.py — nessuna regressione)
```

---

## §6 STATO CI

```
completed	success	Merge pull request #70 from Gasss23/feat/voice-stt-input	CI	main	push	32391782059	59s	2026-08-20T16:24:10Z
completed	success	docs(fine-task): handoff e diff_sessione FASE 3 Fetta 2 — STT Groq Wh…	CI	feat/voice-stt-input	push	32389739781	47s	2026-08-20T16:02:46Z
completed	success	feat(voice): FASE 3 Fetta 2 — STT server-side via Groq Whisper su POS…	CI	feat/voice-stt-input	push	32387199582	53s	2026-08-20T15:37:04Z
```

**Mappatura commit→run sessione corrente (feat/voice-tts-output):**

- `20c61c9` (chore(revisore): memoria review #89) — nessuna run su questo SHA: il branch non è stato pushato prima che il classifier bloccasse il push.
- `4380f65` (feat(voice): FASE 3 Fetta 3) — nessuna run su questo SHA: stesso motivo.
- `0cf8fb9` (docs(fine-task): report Fetta 3) — nessuna run su questo SHA: stesso motivo.
- Commit di fine-task (/fine-task) — run non ancora disponibile alla scrittura dell'handoff.

Le ultime 3 run CI mostrate appartengono alla sessione precedente (Fetta 2, branch feat/voice-stt-input). Il branch `feat/voice-tts-output` non è stato pushato durante la sessione — CI su questo branch sarà disponibile dopo il push manuale dell'operatore.

---

## §7 RISERVE APERTE

**Da questa sessione:**
- 🟡 **R-tts-1** (review #89, non bloccante): nessun cap esplicito sul testo inviato a ElevenLabs. Il fail-safe regge (ElevenLabs 4xx/5xx → `ElevenLabsTTSError` → 502 controllato), ma il comportamento su testi lunghissimi è implicito. Da valutare in una fetta successiva o al deploy VPS. Tracciata in `reports/stato_progetto.md`.

**Ereditate (non chiuse in questa sessione):**
- 🟡 **R-verdetto-evidenza** — check meccanico che path:riga citati nel verdetto esistano nel diff. Non impegnato.
- 🟡 **.gas_history.json runtime** — non persiste se sessione muore prima di `/fine-task`.
- 🟡 **Esfiltrazione** — chiusa in os_strict con bwrap; in os_with_fallback resta aperta.
- 🟡 **Degrado a solo-testo per-turno non rilevato** — warning in gas_debug.log, fail-safe §9. Rimandato.
