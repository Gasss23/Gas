# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-08-02 — Sonda fattibilità client voce Windows ↔ GAS (WSL) — F0 completata
**Branch:** feature/voice-probe

---

## §DECISIONI UMANE RICHIESTE

**D1-ter (APERTA):** IP WSL non stabile tra reboot.
Scegliere: (a) `networkingMode=mirrored` in `.wslconfig` (da ri-sondare, può cambiare la rete di tutta la WSL) OPPURE (b) client che risolve l'IP a runtime invece di hardcodarlo.
Da decidere PRIMA dell'endpoint Fetta 1.

**D2-audio (APERTA, Fetta 2):**
- (a) Client DEVE usare `load_dotenv(override=True)` o torna il "402-fantasma": `ELEVENLABS_VOICE_ID` esportata in shell vince sul `.env` e porta al 402 anche con voice_id corretto.
- (b) Policy device output: default di sistema vs esplicito con fallback (rischio: device virtuali → audio in fantoccio muto).

**AZIONE SICUREZZA:** Rigenerare la chiave ElevenLabs esposta in chat a fine validazione + aggiornare `.env` (il valore non va mai nei file versionati).

---

## §ESITO SONDA F0 (6/6 verde — risultati reali)

| Gamba | Esito | Dettaglio |
|-------|-------|-----------|
| STT Groq Whisper | OK | HTTP 200, `whisper-large-v3-turbo`, risposta: "Grazie." |
| TTS ElevenLabs Flash + voce Roger | OK | HTTP 200, voice_id `CwhRBWXzGAHq8TQ4Fs17`, mp3 ~40KB |
| Bridge WSL↔Windows | OK | IP `172.20.137.213:8765`, latenza ~20ms |
| Mic Realtek idx1 | OK | RMS 1428 (con voce) |
| Playback | OK | Voce sentita dall'altoparlante |
| Wakeword `hey_jarvis` | OK | Score 0.538/0.610, zero falsi positivi in 60s |

NB: la sonda ElevenLabs ha richiesto (1) voice_id di voce premade free-tier (`CwhRBWXzGAHq8TQ4Fs17` = Roger, non la voice library che dava 402), (2) `load_dotenv(override=True)` per non farsi scavalcare dalla variabile shell.

---

## §DECISIONI FORZATE DALLA SONDA (entrano in Fetta 1)

**D1-bis (DECISA):** Client → bridge via **IP WSL**, NON localhost.
Numeri: `localhost` = 2050ms costanti (10/10 ping — muro strutturale del forwarding TCP); IP = ~20ms.
L'endpoint Fetta 1 nasce sull'IP.
NB: l'IP osservato oggi era `172.20.137.213` ma è **instabile tra reboot** (vedi D1-ter) → NON è config canonica.

**Token obbligatorio (conseguenza di D1-bis):** Il server binda `0.0.0.0` → raggiungibile da chiunque sulla WiFi di casa. Auth a token = requisito Fetta 1, unica barriera tra LAN e cervello GAS che esegue codice. Non è un extra.

---

## §CAVEAT SICUREZZA

- **Chiave ElevenLabs esposta in chat** → rigenerare a fine validazione (valore MAI nei file versionati).
- **Ambienti estranei sulla macchina** (solo flag, non urgente): venv Hermes nel PATH Windows, seconda distro WSL `OpenClawGateway`, device virtuali Voice Changer/MFDriver. Stesso schema del clone Windows già visto.

---

## §STATO REPO

La sonda era solo esecuzioni; i file `clients/voice/probe/` erano già stati committati nel commit `1907fa2` della sessione precedente. Questo giro riscrive solo i due doc di sessione (`handoff.md`, `ultimo_report.md`). Nessun file nuovo, nessun file motore toccato.

```
git diff --stat HEAD~1..HEAD  (commit di questa sessione — doc-only)
 reports/handoff.md       | riscritta
 reports/ultimo_report.md | riscritta
```

---

## §PROSSIMO PASSO

1. Decidere **D1-ter** (IP stabile vs mirrored networking).
2. Rigenerare chiave ElevenLabs (AZIONE SICUREZZA).
3. Poi: **Fetta 1** — endpoint locale WSL con token auth (`/transcribe`, `/speak`).

---

## §VERDETTO REVISORE

Revisore **NON invocato**: task doc-only, nessun file in `gas.py`, `brains/`, `modules/`, `tests/` toccato in questa sessione. Commit contiene solo `reports/*.md`.

---

## §CI

`ci.yml` non ha `paths-ignore` → la CI gira anche su PR doc-only. Il check `unit-suite` sarà eseguito sul branch al push; nessuna modifica al motore, i test esistenti non dovrebbero rompersi.

Ultimo run CI noto (da sessione precedente):
```
completed  success  Merge pull request #56 from Gasss23/fix/gasmerge-hardening  main  2026-07-31
```
