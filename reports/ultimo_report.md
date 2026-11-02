# Ultimo report — 2026-11-02 — Voce V8: pagina «prova voci» e libreria condivisa (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #326 (https://github.com/Gasss23/Gas/pull/326), secondo la regola di merge di CLAUDE.md §10.
2. Sul Mac, dopo il merge: aprire la pagina «prova voci» (guida in `reports/prova_voce_mac.md`), ascoltare le voci con le frasi fisse e scegliere quella di Gas (`ELEVENLABS_VOICE_ID` nel `.env`). Percorsi e costi della libreria condivisa di ElevenLabs sono DA VERIFICARE sul Mac (dal cloud elevenlabs.io è bloccato).

## Esito delle fette

- **V8 — pagina «prova voci»**: `FATTA` — `/voci` (pagina), `GET /voci/elenco`, `POST /voci/prova` con frasi fisse; solo voci premade/generated/professional; tetto 40 prove all'ora; Piper facoltativo (`GAS_PIPER_MODEL`); il proxy della pagina accetta solo host locale e stessa origine. Review #624/#625-M2 (riserve chiuse), #626-M2 APPROVATO.
- **V8b — libreria condivisa**: `FATTA` — `GET /voci/libreria` (migliori 8, solo professional/generated) e `POST /voci/aggiungi` (solo voci dell'ultima ricerca, tetto 5 all'ora), avviso su costi e limiti non verificati. Review #627/#628-M2 (riserve chiuse), #629-M2 APPROVATO.
- **Merge di main** (V6, V7a #322, V7b #325, #319–#323): `FATTA` — conflitto in `do_POST` risolto tenendo il reset di `_capito` prima dei rami `/voci/*`; review #655-M2 APPROVATO.
- Test: prova_voci + voice_server + voice_stt + voice_tts + voice_contesto + voce_ascolto 330 passed (browser obbligatorio).
- **V9**: `DEFERITA` — PR dopo il merge di questa.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
- La documentazione ElevenLabs della libreria condivisa non si legge dal cloud: percorsi, campi e costi da verificare sul Mac.
