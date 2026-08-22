# Task — Allineamento voce: stato_progetto.md + ultimo_report.md
**Data:** 2026-08-22
**Branch:** main

---

## Scope

Riallineamento SOLO dei due report (`stato_progetto.md` e `ultimo_report.md`) alla realtà sulla VOCE.
Nessun codice motore toccato. Nessun merge. Scope deciso dal supervisore.

---

## Verifica preliminare (step 0)

File voce confermati presenti nel repo (ls -la):
- `clients/voice/probe_client_4a.py` — 6778 byte, 2026-08-21
- `modules/voice/server.py` — 11704 byte, 2026-08-20
- `modules/voice/stt.py` — 5172 byte, 2026-08-20
- `modules/voice/tts.py` — 2256 byte, 2026-08-20
- `tests/test_unit_voice_server.py` — 14435 byte
- `tests/test_unit_voice_stt.py` — 16383 byte
- `tests/test_unit_voice_tts.py` — 12969 byte

PR chiuse verificate via git log: #73 (feat/voice-client-4a), #72 (sonda/voice-client-env), #71 (feat/voice-tts-output) su main.

---

## Gap rilevati vs realtà

**Già corretto in stato_progetto.md:**
- ✅ FASE 3 Fetta 4a presente come completata
- R-client4a-1 e R-tts-1 già tracciati come 🟡 aperti

**Gap reali corretti in questa sessione:**

1. **Milestone ATTESTATO DAL SUPERVISORE mancante**: aggiunto dopo il blocco Fetta 4a nel §Stato motore, con etichetta esplicita "non verificato da Claude Code".
2. **Finding "kernel rifiuta 7×8" assente**: aggiunto come 🟡 aperto in §Finding aperti.
3. **Finding "rotazione chiave ElevenLabs prima del VPS" assente**: aggiunto come 🟡 aperto in §Finding aperti, con cross-ref al rischio esposizione 2026-08-02.
4. **§Prossimi passi stale**: FASE 3 ancora etichettata "_(pipeline da costruire)_" → aggiornata a "Fette 1+2+3+4a ✅ su main, gate 4b APERTO".
5. **§Componenti attive stale**: citava solo "Fetta 1+2" → aggiornata a "Fette 1+2+3+4a" con TTS + client.

---

## Modifiche apportate

### reports/stato_progetto.md

1. **§Stato motore — dopo Fetta 4a**: aggiunto milestone:
   > **⭐ ATTESTATO DAL SUPERVISORE (2026-08-22) — prova a VOCE UMANA REALE superata (WSL)**: mic→STT→kernel→TTS→casse. text-only: STT ha reso `'sette per otto'` → `'7×8'`. audio: `200 audio/mpeg`, MP3 riprodotto, giro completo. Debito 4a "Gas capisce il parlato" CHIUSO. Gate per 4b APERTO. (Test manuale fuori repo, non verificato da Claude Code.)

2. **§Finding aperti — nuovi 🟡**: 
   - `Rotazione chiave ElevenLabs prima del VPS` (ATTESTATO DAL SUPERVISORE, 2026-08-22)
   - `kernel rifiuta 7×8` (ATTESTATO DAL SUPERVISORE, 2026-08-22)

3. **§Componenti attive**: riga voice endpoint estesa a Fette 1+2+3+4a con TTS e client.

4. **§Prossimi passi**: FASE 3 aggiornata da "pipeline da costruire" a "Fette 1+2+3+4a ✅ su main, gate 4b APERTO".

### reports/ultimo_report.md

Riscritto (questo file) con il report del task corrente.

---

## Anomalie

Nessuna. Tutte le discrepanze erano esclusivamente documentali (zero codice motore toccato).

## Scope superato / proposto / fuori mandato

Nessuno. Toccati SOLO i due report indicati dallo scope. Codice motore, altri file, merge: invariati.

## Riserve aperte da questo task

Nessuna nuova. Le riserve trovate (R-client4a-1, R-tts-1, rotazione ElevenLabs, kernel 7×8) erano già il contenuto da registrare — sono state aggiunte a §Finding aperti come richiesto, NON chiuse.
