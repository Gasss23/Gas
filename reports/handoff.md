# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-08-21 — Sonda ambiente client vocale FASE 3 (Giulia/WSL)

---

## §0 DECISIONI UMANE RICHIESTE

1. **Merge PR `sonda/voice-client-env`** (doc-only, nessun codice motore, nessun revisore richiesto).
2. **Scelta fetta client vocale**: Fetta 4a (script WSL+ffmpeg) o Fetta 4b (HTML5 browser)?  
   Dettaglio e trade-off in `reports/ultimo_report.md` § Proposta design client vocale.

---

## §1 SCOPE & ESITO FETTE

- **Punto 1 — Device audio Giulia/WSL**: `FATTA` — WSLg 1.0.73.2, socket `/mnt/wslg/PulseServer` attivo, play→Windows testato via ffmpeg (exit 0). Dispositivi: PulseAudioRDPSink (output) + PulseAudioRDPSource (input).
- **Punto 2 — Librerie cattura/play disponibili**: `FATTA` — zero Python audio libs nel venv (sounddevice/pyaudio/pydub/playsound tutti assenti). ffmpeg 6.1.1 installato con `--enable-libpulse`: unica via funzionante senza installazioni.
- **Punto 3 — D1-ter IP WSL instabile**: `FATTA` — IP `172.20.137.213` dinamico; `localhost:8765` raggiungibile da Windows via WSL2 forwarding (default attivo, IP WSL irrilevante per client locale). Opzioni multi-device: `networkingMode=mirrored`, avahi.
- **Stop gate — nessun codice scritto**: `RISPETTATO` — solo `reports/` modificati, nessun file motore toccato.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md  |  35 +++----
 reports/handoff.md        | 100 +++++--------------
 reports/stato_progetto.md |   3 +-
 reports/ultimo_report.md  | 245 ++++++++++++++++++++++++++--------------------
 4 files changed, 177 insertions(+), 206 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
33c42f6 docs(sonda): sonda ambiente client vocale FASE 3 — WSLg audio, librerie, D1-ter IP
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore (nessun commit tocca gas.py/brains/modules/tests/), revisore non richiesto.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/ — suite invariata (64 PASS voice, 276 PASS kernel; valori dalla sessione precedente).

---

## §6 STATO CI

```
completed	success	docs(sonda): sonda ambiente client vocale FASE 3 — WSLg audio, librer…	CI	sonda/voice-client-env	push	32485002607	46s	2026-08-21T13:04:42Z
completed	success	Merge pull request #71 from Gasss23/feat/voice-tts-output	CI	main	push	32397409066	1m10s	2026-08-20T17:24:15Z
completed	success	docs(fine-task): handoff e diff_sessione FASE 3 Fetta 3 — TTS ElevenL…	CI	feat/voice-tts-output	push	32395608545	47s	2026-08-20T17:04:57Z
```

**Mappatura commit→run:**
- `33c42f6` — run CI `32485002607` ✅ SUCCESS (sonda/voice-client-env, push 2026-08-21T13:04:42Z)
- commit fine-task — run non ancora disponibile alla scrittura dell'handoff

---

## §7 RISERVE APERTE

Nessuna riserva nuova da questa sessione (sonda pura, nessun codice).

Riserve aperte portate dalla sessione precedente (non chiuse qui):
- 🟡 R-tts-1: nessun cap esplicito testo → ElevenLabs (non bloccante, valutare in fetta successiva).
- 🟡 R-verdetto-evidenza: check meccanico path:riga nel verdetto revisore non impegnato.
- 🟡 .gas_history.json: non persiste se sessione muore prima di /fine-task (runtime VPS).
