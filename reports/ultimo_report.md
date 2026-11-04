# Ultimo report — 2026-11-04 — Voce V12: il testo con risposta a voce conta nel tetto orario (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #332 (https://github.com/Gasss23/Gas/pull/332), secondo la regola di merge di CLAUDE.md §10.

## Esito delle fette

- **V12 — R-663-1-M2** (decisione dell'operatore: anche le richieste a testo con sintesi vocale contano nel tetto): `FATTA` — `_sintesi_a_testo()`; 429 prima del turno; solo testo e `audio+pezzi` a testo non contano; senza chiave ElevenLabs non conta; la voce resta contata una volta.
- **R-660-2-M2** (parola persa al tetto in `frasi_voce`): `FATTA`.
- **R-660-1-M2** (test di `audio+pezzi` senza chiave): `FATTA`.
- **V-2 cosmetica bot #330 su ae3258e** (1500+38) e **V-1 cosmetica bot #331** (docstring dell'helper di test): `FATTE`.
- **R-665-1/2/3-M2** (riserve della review #665): `FATTE` nella stessa fetta, review #666-M2 APPROVATO.
- **Tetto sul numero di frasi** (V-1 della verifica esterna su 956a00a): `DEFERITA` — resta entro i 1500 caratteri, non chiesta in questa fetta.
- Test: voice_server + voice_stt 199 passed; 3 test V12 nuovi; 6 mutanti uccisi (revisore).

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
