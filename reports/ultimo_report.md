# ULTIMO REPORT — 2026-10-20 — Avviso Telegram sui lead modificati dopo una lettura

Ramo `feat/merge-automatico-z1xjx2`, ripartito da main dopo il merge di #224 (operatore: «mergia 224 e fai l'avviso su telegram»).

## DECISIONI UMANE RICHIESTE

1. Merge della PR (decide l'operatore se il bot non dà un APPROVATO pulito).

## Esito

- **Avviso su Telegram (R-ve222-4, seconda parte)** — FATTA. Dopo che Gas ha letto un testo esterno, se cambia il recapito di un lead già in rubrica o lo chiude, l'operatore riceve un messaggio solo informativo (niente bottoni) con valore vecchio e nuovo, resi visibili su una riga. Lead nuovi o note: nessun avviso. Invio fallito: avviso nella scatola nera, il turno prosegue. Review #380 APPROVATO CON RISERVE: R-380-1 BASSA (recapito cambiato su una chiave vecchia di un lead fuso: nessun avviso), R-380-2 BASSA (con Telegram irraggiungibile il turno aspetta fino a 15 s per destinatario).
- **Test** — kernel 924 → 927 PASS, 0 FAIL; pytest tests/ 1519 passed.
