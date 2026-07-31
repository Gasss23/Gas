# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-08-01 — Sonda fattibilità client voce Windows ↔ GAS (WSL)
**Branch:** feature/voice-probe

---

## §0 DECISIONI UMANE RICHIESTE

1. **Push del branch**: il push `git push -u origin feature/voice-probe` è stato bloccato dal classifier in auto-mode. Eseguire: `! git push -u origin feature/voice-probe`
2. **P1 — Piano ElevenLabs**: la chiave presente usa una voce library non accessibile con piano free (HTTP 402). Opzioni: (a) upgrade Starter ~5$/mese, (b) clonar voce propria, (c) usare voice_id di voce premade free-tier.
3. **P2 — Eseguire 4 script Windows**: `win_mic_test.py`, `win_wakeword_test.py`, `win_playback_test.py`, `win_bridge_test.py` — vedere RUNBOOK in `reports/ultimo_report.md`.
4. **D1 — Decisione architettura bridge**: HTTP REST (già sondato) vs WebSocket vs named pipe. Decidere prima di costruire il client vero.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Branch `feature/voice-probe`**: `FATTA` — branch creato da main, commit 1907fa2.
- **Fetta 2 — Script Windows (4 file)**: `FATTA` — `win_mic_test.py`, `win_wakeword_test.py`, `win_playback_test.py`, `win_bridge_test.py` scritti in `clients/voice/probe/` con `--device` selezionabile e lista automatica device.
- **Fetta 3 — Script WSL bridge server**: `FATTA` — `probe_bridge_server.py` avviato, testato con curl su 127.0.0.1 e 172.20.137.213:8765, risponde `{"pong": true, "server": "WSL"}`.
- **Fetta 4 — Script WSL probe API**: `FATTA` — `probe_apis.py` eseguito: STT Groq Whisper OK (HTTP 200), TTS ElevenLabs ERRORE_API (HTTP 402 piano free).
- **Fetta 5 — Esecuzione gambe Windows**: `SALTATA — eseguibili solo su Windows`; runbook e spazio risultati nel report.
- **Fetta 6 — Push branch**: `SALTATA — bloccata da classifier auto-mode`; da eseguire manualmente (§0 punto 1).
- **STOP GATE**: rispettato — nessun client costruito, nessun file motore toccato.

---

## §2 GIT DIFF --STAT (sessione)

(`git diff --cached --stat BASE` — include file di report in stage)

```
 clients/voice/probe/probe_apis.py          | 160 +++++++++++++++++++
 clients/voice/probe/probe_bridge_server.py |  86 ++++++++++
 clients/voice/probe/win_bridge_test.py     |  91 +++++++++++
 clients/voice/probe/win_mic_test.py        |  90 +++++++++++
 clients/voice/probe/win_playback_test.py   |  94 +++++++++++
 clients/voice/probe/win_wakeword_test.py   | 105 +++++++++++++
 reports/diff_sessione.md                   |  28 ++--
 reports/handoff.md                         | 118 +++++---------
 reports/ultimo_report.md                   | 244 ++++++++++++++++++++++++++---
 9 files changed, 902 insertions(+), 114 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
1907fa2 feat(voice-probe): sonda fattibilità client voce Windows↔WSL
```

NB: il commit di fine-task che contiene handoff.md non compare qui per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore, revisore non richiesto.

Nessun file in `gas.py`, `brains/`, `modules/`, `tests/` è stato toccato in questa sessione. I soli file modificati sono nuovi script in `clients/voice/probe/` (nuova directory) e `reports/ultimo_report.md`.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

---

## §6 STATO CI

```
completed	success	Merge pull request #56 from Gasss23/fix/gasmerge-hardening	CI	main	push	30650167917	59s	2026-07-31T17:11:09Z
completed	success	docs(fine-task): verdetto #73 path completi — fix check_verdetto CI s…	CI	fix/gasmerge-hardening	push	30648688079	1m3s	2026-07-31T16:49:24Z
completed	failure	docs(fine-task): /fine-task rebase fix/gasmerge-hardening — tutte le …	CI	fix/gasmerge-hardening	push	30586610328	49s	2026-07-30T22:17:25Z
```

**Mappatura commit→run:**
- `1907fa2` (feat(voice-probe): sonda fattibilità…) — **nessuna run su questo SHA**: il push del branch è stato bloccato dal classifier auto-mode; il branch non è ancora su origin. Run CI non disponibile.

---

## §7 RISERVE APERTE

- **P1 ElevenLabs**: piano free non consente voci library via API — decisione piano/voice_id richiesta prima di poter testare TTS end-to-end.
- **P3 IP WSL**: `hostname -I` restituisce `172.20.137.213`; se l'utente ha `networkingMode=mirrored` nel `.wslconfig`, `localhost` funziona da Windows senza conoscere l'IP. Da verificare sul lato Windows.
- **Risultati Windows pendenti**: le 4 gambe Windows non sono state eseguite — i risultati reali sono prerequisito per dichiarare la sonda completa.
