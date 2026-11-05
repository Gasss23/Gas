# Ultimo report — 2026-11-05 — Voce V13: ora locale nel turno parlato e risposte a voce più corte (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #334 (https://github.com/Gasss23/Gas/pull/334), secondo la regola di merge di CLAUDE.md §10.

## Esito delle fette

- **V13.1 — ora nel turno parlato** (decisione dell'operatore via M1 dopo la prova sul Mac del 5 novembre): `FATTA` — `ora_per_voce` / `istruzione_turno_voce` in `modules/voice/server.py`: data e ora locali della macchina del server (il Mac) nell'istruzione del turno parlato, così «che ore sono» non richiede lo strumento `data_ora`.
- **V13.2 — risposte a voce più corte**: `FATTA` — `ISTRUZIONE_VOCE` e `ISTRUZIONE_VOCE_SCHERMO` da «1-3 frasi» a «una o due frasi, mai più di due», senza premesse.
- **V13.3 — indagine «Stefano»** (risposta sui lead a «che ore sono»): `DEFERITA — non diagnosticabile dal cloud`: il parlato non va nel log (privacy V6) e la storia `.gas_history.json` sta sul Mac. Riportata a M1 col controllo da fare sul Mac (messaggio utente prima della risposta su Stefano nella storia).
- **Soglia `GAS_ASCOLTO_VOCE_RMS`** (nota a margine di M1): `SALTATA — fuori perimetro`: `clients/voice/ascolto.py` è della chat Mani; segnalato a M1 (default 500, sul Mac funziona 200).
- Test: 3 nuovi V13; asserzioni V3/V4/V10 e «forte» con `startswith`; suite voce 280 passed.
- Review #667-M2: APPROVATO CON RISERVE (R-667-1/2 BASSE, R-667-3 COSMETICA), registrate in stato_progetto.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
