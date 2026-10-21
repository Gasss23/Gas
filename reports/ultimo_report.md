# ULTIMO REPORT — 2026-10-21 — Chat Mani, fetta 6: note rimaste della PR #242 (R6, PR #243)

Ramo `feat/mani-web-fetta6` da main dopo il merge di #242. Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. PR #243 (https://github.com/Gasss23/Gas/pull/243). Fetta di sicurezza. Operatore: «procedi con la fetta 6», poi «mergia quando il bot approva».

## DECISIONI UMANE RICHIESTE

1. Merge della PR #243: autorizzato dall'operatore quando il bot approva (`verifica-bot` success sull'head, niente ALTA/MEDIA), con CI verde e senza conflitti.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

## Esito

- **V-2 verifica esterna #242 bis (`<title/>`)**: `FATTA` — `<title/>` apre il titolo nel parser e nel ripiego come nei browser: il testo fino a `</title>` va nella riga «Titolo:», non nel corpo.
- **R-449-1**: `FATTA` — dentro svg/math l'autochiusura vale e `<title/>` resta vuoto (era una regressione del primo giro: sulle icone svg si perdeva il resto della pagina).
- **V-1 verifica esterna #242 bis (test sul contatore)**: `FATTA` — chiusura in più dopo una coppia bilanciata sul percorso normale e nel ripiego.
- **R-449-2, R-448-1, V-3/V-4 verifica esterna #242**: `FATTA` — caso del ripiego che discrimina, riga lunga a capo, commento sul SystemError di Python 3.11 con l'input che lo provoca (riprodotto su 3.11.17: con un gruppo di cattura nella ripetizione possessiva, `<a b="1"="x>` solleva SystemError; altri input no, per questo i verificatori non lo vedevano).
- **Note del bot #242 sull'handoff della fetta 5 (run fallita su `f583746`, righe citate)**: `SALTATA — riguardano il dossier della fetta 5, sostituito da questo`. Nota: la run 39687109665 su `f583746` era fallita (handoff-check) perché l'handoff non era ancora aggiornato, come previsto.
- **R-450-1 (punti di integrazione HTML dentro svg/math)**: `DEFERITA — BASSA preesistente, registrata in stato_progetto`.
- **Test**: web suite 167 → 172 (Python 3.13 e 3.11, anche con rete e DNS veri bloccati). Fuzz differenziale 0 fughe. Mutazioni in copie isolate: tutte prese.
- **Review**: #449 (chat Mani) APPROVATO CON RISERVE (R-449-1 BASSA, R-449-2 COSMETICA, chiuse nello stesso giro) → #450 (chat Mani) APPROVATO CON RISERVE (R-450-1 BASSA preesistente).

## Anomalie

- Nessuna.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…6»): aggancio di `leggi_pagina` con al modello solo `testo`, firma a finestra contaminata, tetto di chiamate, diario senza il testo della pagina, fiducia solo nei marcatori con il codice di quella chiamata.
