# Report di fine task — 2026-10-12 — «Pipeline esausta» dice perché

## DECISIONI UMANE RICHIESTE

1. Merge della PR (tocca `gas.py`): secondo la regola di CLAUDE.md (verdetto testuale del bot APPROVATO senza finding, altrimenti decide l'operatore).

## Esito

- **Messaggio «Pipeline esausta»**: `FATTO` — ora elenca per ogni cervello il motivo (variabile non impostata, quota/HTTP, risposta vuota, 10 iterazioni senza risposta finale), mai il testo grezzo dell'errore. Revisore #292 APPROVATO CON RISERVE (R-292-1 BASSA: rami «risposta vuota» ed eccezione senza status non testati; R-292-2 COSMETICA: Gemini ripetuto due volte). Kernel 811 PASS / 0 FAIL, pytest 1032 passed.
- Giro di notte di prova (cloud, copia usa-e-getta): nessun crash, compiti KO per assenza di chiavi API (atteso). Giro sul Mac dell'operatore: 1 compito OK.

## Anomalie

- Sul Mac `git pull` non ha aggiornato: il repo è su un HEAD staccato («Attualmente non sei su un branch»), quindi il giro sul Mac ha usato codice vecchio.
