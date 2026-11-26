# Ultimo report — 2026-11-26 — Mani alla voce F4: «mergia N» / «no N»

Sotto-chat di M1 (session_01FgYcG4uNEqggobeJsbmE93), ramo `claude/mani-voce-f4` (sopra la PR #414, che sta sopra #412 e #411; nessuna ancora mergiata).

## DECISIONI UMANE RICHIESTE

1. Merge in ordine: #411, #412, #414, poi la PR di questa fetta (revisore APPROVATO CON RISERVE: decide l'operatore).
2. Scelte da confermare (oggi così): il merge NON vale a voce dal Mac (solo Telegram); l'annullo a voce NON chiede conferma (un numero sentito male annulla la richiesta sbagliata, si riapre a mano).
3. Dopo i merge, sul Mac: `GAS_RICHIESTE_AUTORI` nel `.env`, riavvio del bot Telegram e del server voce.

## Esito per fetta

- **F4 — «mergia N» / «no N»**: FATTA (2863bf4c).
  - Su Telegram, scritto o vocale dalla chat dell'operatore, prima del modello e solo da messaggio nuovo.
  - Vale SOLO se N è la PR per cui Gas ha chiesto davvero il merge (R-873MV-1) e la domanda non ha già una risposta; la issue deve essere aperta, `da-gas`, non annullata; il repo privato. Il comando si prenota in locale prima di scriverlo su GitHub (una volta sola, anche con il file rotto).
  - Gas scrive sulla issue il commento `MERGIA #N` / `NO #N` a formato fisso; il merge vero lo farà l'esecutore (F5) rispettando CLAUDE.md §10.
  - Al microfono del Mac: «confermamelo su Telegram» (l'audio della stanza non fa mergiare).
  - R-883MV-1 chiusa: la PR della domanda si ricorda solo dopo che l'avviso è partito.
  - Regola nel prompt: il modello non dice mai di aver annullato, mergiato o rifiutato una richiesta.
  - Chiuse anche le riserve della #414: «annulla richiesta dodici» anche a testo, frase a voce «CI verde, bot …».
  - 121 test di cassetta. Revisore #888-MV → #889-MV APPROVATO CON RISERVE.
- **F5 — esecutore nel cloud**: DEFERITA — prossima fetta (crea una scheduled task: spesa ricorrente; il via c'è dal 26/11).

## Anomalie

- R-889MV-1 BASSA aperta: regola per F5.
