# ULTIMO REPORT — 2026-10-30 — Mani: leggi_pagina solo verso le porte 80 e 443 (R6, fetta 31, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #310 (numero nell'handoff §0): la faccio io solo con verdetto del bot APPROVATO pulito; con riserve serve il sì dell'operatore (anche tramite M1).
2. Piano per il browser senza schermo («leggere il web in un ambiente chiuso», 8 punti) mandato a M1: aspetta il via dell'operatore prima di scrivere codice.

## Esito
- **PR #309**: MERGIATA da M1 (4ffcd80). V-1 bot #309 BASSA (un verdetto che riporta alla lettera un caso di prova di credenziale spezzata da una citazione non viene pubblicato): FATTA — registrata come limite in stato_progetto.
- **Porte 80 e 443** (decisione dell'operatore del 2026-10-22): FATTA (PR #310). `_valida_url` rifiuta ogni altra porta, anche dopo un redirect, prima di DNS e connessione.
- **Review #583 (chat Mani)**: APPROVATO CON RISERVE. R-583-1 COSMETICA (a capo nel docstring): DEFERITA — da correggere alla prossima fetta su leggi.py.
- **Piano del browser senza schermo**: FATTA — mandato a M1, nessun codice.

## Prove
- `tests/test_unit_web_*.py`: 632 passed, 2 skipped. Mutante senza il controllo: 11 failed.

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
