# ULTIMO REPORT — 2026-10-23 — R2 via B, fetta 2: protezioni e tetto del cervello forte

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta (vedi §0 dell'handoff): verdetto del revisore APPROVATO CON RISERVE, quindi il merge spetta all'operatore (CLAUDE.md §10).
2. Prima di accendere il forte (`GAS_CLAUDE_CLI=1` sul Mac): decidere se chiudere o accettare R-496-1/2 e fare la prova del login (R-496-3).

## Esito

- **Codice casuale per chiamata nei tag della trascrizione**: `FATTA`. Un file o una pagina non può più fingere un messaggio dell'utente (anche con caratteri sosia o entità) e il contenuto arriva a Claude intatto. Chiude R-494-1 e R-494-2.
- **Solo variabili d'ambiente permesse al processo `claude`**: `FATTA` (V-2 della verifica esterna #256). Passa `CLAUDE_CODE_OAUTH_TOKEN` per il login sulla VPS.
- **Tetto giornaliero del forte**: `FATTA` (V-1 bot #256). `GAS_CLAUDE_CLI_TETTO_USD`, default 4,60 $ «come se fosse API» (`total_cost_usd` della CLI), controllato prima di ogni chiamata; superato → turno fermato dichiarato, mai ai gratuiti; conto illeggibile → forte fermo (fail-closed).
- **Errori**: `FATTA`. Limite in testo semplice → QUOTA (V-2 bot), niente testo di Claude nel log (V-3 bot), argomenti non validi → errore (V-4 bot).
- **Documenti**: `FATTA`. Dicitura del tetto nella via B corretta (V-3 verifica esterna #256): 4,60 $ è una misura indicativa, il limite del piano non è in dollari.
- **Test**: kernel 1035 PASS 0 FAIL (T99d rafforzato, T99g-l nuovi); claude_cli 19 passed; cancello 819 passed; pytest completo 2135 passed, 1 skipped. Prova vera dell'adattatore con l'ambiente ridotto in questo ambiente Linux: risposta «ok», costo equivalente 0,0004 $.
- **Note del bot e della verifica esterna #258**: `FATTA`. Costo 0 non più accettato, conto rovinato → forte fermo, variabili `LC_` per nome, errori e tempo scaduto nel tetto (review #497 APPROVATO CON RISERVE, R-497-1/2 BASSE).
- **V-1 MEDIA bot #258**: `FATTA`. Il modello poteva azzerare il proprio tetto scrivendo il file del conto: ora è al livello 3 del cancello (review #498 APPROVATO CON RISERVE).
- **Fette successive R2**: `DEFERITA` (campo `cervello: forte` nel catalogo notturno e opzione CLI, riga del doctor, setup del Mac).

## Anomalie

- Nessuna. Il login col portachiavi del Mac non è provabile da qui (R-496-3).
