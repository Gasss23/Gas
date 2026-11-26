# Ultimo report — 2026-11-26 — Mani alla voce F3b: esiti a voce, annullo a voce

Sotto-chat di M1 (session_01FgYcG4uNEqggobeJsbmE93), ramo `claude/mani-voce-f3b` (sopra la PR #412, che sta sopra la #411; nessuna delle due ancora mergiata).

## DECISIONI UMANE RICHIESTE

1. Merge in ordine: PR #411, poi PR #412, poi la PR di questa fetta. Revisore di F3b #885-MV APPROVATO; il merge di questa PR lo fa l'agente solo con un verdetto del bot pulito, altrimenti decide l'operatore (CLAUDE.md §10).
2. Dopo il merge della #412 (già chiesto): `GAS_RICHIESTE_AUTORI` nel `.env` del Mac e riavvio del bot Telegram. Per F3b serve anche il riavvio del server voce.

## Esito per fetta

- **F3b — esiti detti a voce e annullo a voce**: FATTA (28947ffc).
  - Al primo turno a voce dopo l'arrivo di un esito (anche col solo «Hey Jarvis») Gas dice una frase corta con SOLO parti fisse: numero, stato, PR, controlli, «ti ho chiesto su Telegram se mergiarla» se è pronta. Mai il testo libero dell'esecutore (R-873MV-1, che a voce non si poteva difendere con le «»). Al massimo 2 per turno, ultime 24 ore, segnati detti solo dopo la consegna.
  - «annulla richiesta N» (anche «annulla la richiesta numero N») vale detto al microfono del Mac dopo la parola di attivazione, mai nel seguito (parlato della stanza), e da un vocale Telegram. Risponde il codice, nessun turno del modello.
  - Avviso alla creazione: «scrivimi o dimmi «annulla richiesta N»» (ve #412 V-2).
  - Un esito in sospeso scartato in modo definitivo esce dai sospesi (bot #412 V-1).
  - Revisore #884-MV APPROVATO CON RISERVE (R-884MV-1 di gravità media, vera: server voce e bot scrivevano lo stesso file senza lock) → corretta con un file a parte per i letti a voce → #885-MV APPROVATO.
- **Correzione dopo il bot sulla #414 (BOCCIATO su 8f6787a6)**: FATTA (0338ed09). Due test di cassetta dipendevano dalla data reale (dal 27/11 alle 15:00 UTC sarebbero diventati rossi su main per tutti): ora no. Annullo con lo stesso ordine sul Mac e su Telegram («forte annulla …» non annulla), numero detto in lettere → risposta fissa invece del modello, «n. 12» accettato, frase a voce salvata con lo stato prima dell'invio. 105 test di cassetta. Revisore #886-MV → #887-MV APPROVATO.
- **F4 — «mergia N» / «no N»**: DEFERITA — prossima fetta. Deve chiudere R-883MV-1 (conferma del numero della PR).
- **F5 — esecutore nel cloud**: DEFERITA.

## Anomalie

- Riserve aperte della catena: R-883MV-1 BASSA (F4), R-881MV-1 BASSA, ve #412 V-1 BASSA (un ESITO è sempre un commento nuovo, regola per F5), cosmetiche varie (in `reports/stato_progetto.md`).
