# Ultimo report — 2026-11-26 — Mani alla voce: decisioni dell'operatore + F2-bis

Sotto-chat di M1 (session_01FgYcG4uNEqggobeJsbmE93), ramo `claude/mani-voce-f3` (da main 17cba359, dopo la PR #409 mergiata).

## DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: con verdetto pulito del bot la mergio io (CLAUDE.md §10), altrimenti M1 chiede all'operatore.

## Esito per fetta

- **Merge della PR #409**: FATTO il 26/11 (17cba359) col sì dell'operatore via M1, dopo aver ricontrollato PR aperta, nessun conflitto, CI verde, bot neutral senza ALTA/MEDIA.
- **Decisioni dell'operatore nel piano** (`reports/mani_voce_piano.md` §4bis e §5): FATTA. F1 rifiutata; compensazioni: avviso subito alla creazione della richiesta, «annulla richiesta N» con 30 minuti di attesa prima che l'esecutore parta, max 2 richieste lavorate al giorno.
- **F2-bis — riserve basse di F2**: FATTA (887fcc0d). `frase_esito` riscritta: parti fisse prima, testi liberi tra «» con le «» interne tolte (R-864-3), niente domanda di merge con righe RISERVA (ve #409 V-2), PR e CI anche per fallita/ferma, valori fuori elenco = assente; `_pulisci` vuota un testo senza nulla di visibile e toglie altri invisibili; «mergia N» solo ASCII. 79 test. Revisore #873-MV APPROVATO CON RISERVE → #874-MV APPROVATO.
- **F3, F4, F5**: DEFERITE — prossime fette, in quest'ordine.

## Anomalie

- Riserva nuova R-873MV-1 BASSA (a voce le «» non si sentono): da chiudere in F3.
