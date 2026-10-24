# ULTIMO REPORT — 2026-10-24 — R2 via B, fetta 3: note BASSE del cervello forte chiuse

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta (vedi §0 dell'handoff): tocca il motore e il template fine-task. L'ultima review (#503) è APPROVATO; il merge autonomo vale solo se anche il bot dà APPROVATO senza riserve.
2. Prima di accendere il forte: provare sul Mac `claude -p` col login Max di Gas (R-496-3).
3. Ancora aperti da prima: testo nuovo dell'attività di notte da chiedere direttamente nella sessione fissa; 3 lezioni da approvare sul Mac.

## Esito

- **Costo su ogni errore dopo una risposta della CLI (R-497-1)**: `FATTA`. Uscita non JSON, JSON non oggetto, chiamate o argomenti non validi su una risposta pagata, eccezioni impreviste; `usage` non numerico non solleva più.
- **Prezzo per famiglia del modello e pavimento per chiamata (V-1 bot/ve #258)**: `FATTA`. Haiku 1/5, Sonnet 3/15, Opus 15/75 $/M, famiglia sconosciuta = la più cara; nessuna chiamata conta meno di 500 token d'ingresso.
- **Conto sotto lucchetto (R-496-2, R-502-1/2)**: `FATTA`. Attesa massima 5 s; se il consumo non si registra il forte si ferma fino al riavvio del processo.
- **Costi non finiti o negativi ignorati (V-4 ve #258)**: `FATTA`.
- **Doctor «Cervello forte» (R-497-2)**: `FATTA`. Spento/acceso, comando presente, conto di oggi contro il tetto, conto illeggibile o con data futura = WARN; nessuna chiamata a `claude`.
- **Messaggio dei file protetti (R-498-1)** e **deroga n/d nel template (R-501-1)**: `FATTA`.
- **Review**: #502 APPROVATO CON RISERVE (R-502-1/2/3) → corrette → #503 APPROVATO.
- **Test**: `tests/test_unit_claude_cli.py` 21 passed; kernel 1038 PASS 0 FAIL (T99m/n/o nuovi, lockfile in T68s); pytest completo 2142 passed, 1 skipped.
- **Campo `cervello: forte` nel catalogo notturno e setup del Mac**: `DEFERITA — prossima fetta, dopo la prova del login`.

## Anomalie

- Nessuna.
