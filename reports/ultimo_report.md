# Ultimo report — 2026-11-02 — Voce V9: rumore (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #327 (https://github.com/Gasss23/Gas/pull/327), secondo la regola di merge di CLAUDE.md §10.
2. Sul Mac, dopo il merge: parlare a Gas con ventola o TV accesa. Se Gas si zittisce da solo mentre parla, mettere `GAS_VOICE_AGC=0` nel `.env` (guida in `reports/prova_voce_mac.md`).

## Esito delle fette

- **V9 — rumore**: `FATTA` — microfono con noiseSuppression, echoCancellation e AGC (spegnibile con `GAS_VOICE_AGC=0`, letto dalla pagina in `/config`), soglia della voce che segue il rumore di fondo (non solo i primi 300 ms), grazia di 500 ms prima che Gas si lasci interrompere. R-584-1-M2 mitigata. Review #630-M2 CON RISERVE (chiuse in parte), #631-M2 APPROVATO.
- **Merge di main** (V6, V7a #322, V7b #325, V8 #326, #319–#323): `FATTA` — test nel browser con i modi «guasto» e «rumore_costante» insieme; review #657-M2 APPROVATO.
- Test: voice_server + voice_stt + voice_prova_voci 243 passed (browser obbligatorio).

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
- Il microfono dei test è finto (da file): rumore e voce veri si provano solo sul Mac.
