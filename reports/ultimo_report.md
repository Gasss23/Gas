# Ultimo report — 2026-11-05 — Voce V14: «Sì, signore?» (GET /voce/conferma) e filtro «Dimmi.» rivisto (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #335 (https://github.com/Gasss23/Gas/pull/335), secondo la regola di merge di CLAUDE.md §10.

## Esito delle fette

- **V14.1 — `GET /voce/conferma`** (decisione dell'operatore, contratto con la chat Mani via M1): `FATTA` — «Sì, signore?» in audio/mpeg con la voce attuale; cache in memoria con l'id della voce (un giro su ElevenLabs per voce); 503 senza chiave, 502 su errore o audio vuoto, mai in cache.
- **V14.2 — V-1 bot #334** (togliere ok/okay dal filtro «Dimmi.»): `FATTA`.
- **V14.3 — R-668-2-M2** («Hey Jarvis» ripetuto): `FATTA`.
- **Proposta sulla velocità della voce** (solo documento, chiesta da M1): `DEFERITA — dopo questa fetta`, come da ordine di M1.
- Client H24 (`clients/voice/ascolto.py`): `SALTATA — fuori perimetro`, lo fa la chat Mani.
- Test: 2 nuovi V14 in voice_prova_voci, casi del filtro aggiornati in voice_stt; 3 mutanti uccisi; suite voce 284 passed (prima del filtro rivisto), revisore 148 passed su voice_prova_voci + voice_stt dopo.
- Review #669-M2 APPROVATO CON RISERVE (R-669-1 BASSA, R-669-2 COSMETICA).
- **Merge di main nel branch** (PR #335 in conflitto dopo la PR #333 della chat Mani, soglia della voce 200): `FATTA` — conflitti solo nei report e nella memoria del revisore; review #670-M2 APPROVATO (suite voce 284 passed, voce_ascolto 154 passed).
- **Verifica esterna #335**: APPROVATO CON RISERVE (V-1 BASSA = R-669-1; V-2 BASSA «Jarvis Gas» ora sola attivazione, caso negativo tolto senza dichiararlo; V-3/V-4 COSMETICHE). **Bot**: verdetto scritto (APPROVATO CON RISERVE: V-1 BASSA «Jarvis Gas», V-2 COSMETICA query string → 405) ma check `verifica-bot` annullato due volte: GitHub scartava l'output perché conteneva una parola uguale a un secret del repo. Corretto nella PR #337 (verdetto compresso fra i job), mergiata.
- **Secondo merge di main nel branch** (dopo la PR #337 e la fetta 41 della chat Mani): `FATTA` — conflitti solo nei report e nella memoria; review #674-M2 APPROVATO (1039 test passati fra bot, voce e ascolto). Il push rilancia il bot sulla #335 una volta.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
