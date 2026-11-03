# Ultimo report — 2026-11-03 — Voce V11: «audio+pezzi» a testo solo testo (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #331 (https://github.com/Gasss23/Gas/pull/331) secondo la regola di merge di CLAUDE.md §10.
2. R-663-1-M2 (BASSA): le richieste a testo che chiedono l'audio (`Accept: audio/mpeg`, oppure `audio+testo`/`audio+testo+pezzi`) restano fuori dal tetto orario. Decidere: tetto anche per la sintesi a testo, oppure client a testo dichiarati fidati (serve comunque il token).

## Esito delle fette

- **V11 — V-1 bot #330 su ae3258e**: `FATTA` — con `X-Gas-Formato: audio+pezzi` una richiesta a testo riceve solo il testo (JSON), niente ElevenLabs, anche con `Accept: audio/mpeg`; i percorsi a voce non cambiano. Review #663-M2 APPROVATO CON RISERVE.
- **V-2 COSMETICA bot su ae3258e** (1500+38 caratteri col taglio): `REGISTRATA` in stato_progetto, senza codice.
- **Docstring del test V10** «il client H24 legge sempre NDJSON» (V-1 bot su ef88184): `FATTA`, corretto.
- **ThreadingHTTPServer** (riserva bot #329): `VALUTATA` — sconsigliato ora (kernel unico con storia condivisa, tetti senza lock); nessun codice.
- **Riserve del bot e della verifica esterna su d8f4572**: BASSE/COSMETICHE, `REGISTRATE` senza giro (decisione di M1).
- **Merge di origin/main (#329, fetta 39)**: `FATTA` (review #664-M2 APPROVATO); voce 166 passed.
- Test: `tests/test_unit_voice_server.py` 104 passed (rieseguito dal revisore); test V11 nuovo, mutanti → fallisce.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
