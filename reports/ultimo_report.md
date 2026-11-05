# Ultimo report — 2026-11-05 — Voce V13: ora locale nel turno parlato e risposte a voce più corte (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #334 (https://github.com/Gasss23/Gas/pull/334), secondo la regola di merge di CLAUDE.md §10.

## Esito delle fette

- **V13.1 — ora nel turno parlato** (decisione dell'operatore via M1 dopo la prova sul Mac del 5 novembre): `FATTA` — `ora_per_voce` / `istruzione_turno_voce` in `modules/voice/server.py`: data e ora locali della macchina del server (il Mac) nell'istruzione del turno parlato, così «che ore sono» non richiede lo strumento `data_ora`.
- **V13.2 — risposte a voce più corte**: `FATTA` — `ISTRUZIONE_VOCE` e `ISTRUZIONE_VOCE_SCHERMO` da «1-3 frasi» a «una o due frasi, mai più di due», senza premesse.
- **V13.4 — niente «… sì o no?» in coda** (cronologia della prova sul Mac, da M1): `FATTA` — domanda solo se senza risposta non si può fare quanto chiesto.
- **V13.5 — «Hey Jarvis» da solo** (cronologia della prova, da M1): `FATTA` — trascrizione fatta solo della parola di attivazione → «Dimmi.» senza turno (solo parlato).
- **Note del bot su 8416674**: V-1 BASSA (istruzioni in conflitto con «usa data_ora» di gas.py) `FATTA` (la frase dell'ora dice che vale al posto di data_ora); V-2 COSMETICA («01:30») `FATTA` («ore 1:30»).
- **R-667-1-M2** (test dell'ora cieco con TZ=UTC, confermata da V-1 della verifica esterna): `FATTA` — TZ forzato nel test, mutante ucciso.
- **V13.3 — indagine «Stefano»** (risposta sui lead a «che ore sono»): `DEFERITA — non diagnosticabile dal cloud`: il parlato non va nel log (privacy V6) e la storia `.gas_history.json` sta sul Mac. Riportata a M1 col controllo da fare sul Mac (messaggio utente prima della risposta su Stefano nella storia).
- **Soglia `GAS_ASCOLTO_VOCE_RMS`** (nota a margine di M1): `SALTATA — fuori perimetro`: `clients/voice/ascolto.py` è della chat Mani; segnalato a M1 (default 500, sul Mac funziona 200).
- Test: 3 nuovi V13 in voice_server, 2 in voice_stt; asserzioni V3/V4/V10 e «forte» con `startswith`; suite voce 282 passed (prima della modifica al test del fuso; test mirati passati dopo).
- Review #667-M2 APPROVATO CON RISERVE (R-667-1 chiusa; R-667-2 BASSA e R-667-3 COSMETICA aperte); #668-M2 APPROVATO CON RISERVE (R-668-1/2/3 BASSE); #668-M2 bis APPROVATO.
- Bot su 8416674: APPROVATO CON RISERVE (V-1, V-2 chiuse). Verifica esterna su 8416674: APPROVATO CON RISERVE (V-1 = R-667-1 chiusa; V-2 = R-667-2, aggravata: sul VPS l'istruzione vieta anche data_ora; V-3 BASSA nessun tetto in codice alle frasi; V-4 COSMETICA ora presa a inizio turno).

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
