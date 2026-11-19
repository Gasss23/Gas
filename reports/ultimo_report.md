# Ultimo report — 2026-11-19 — Presentazione clienti tolta dal repo

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa sessione (toglie `presentazione_clienti/`; nessun file del motore).

## Esito
- **Togliere da GitHub il PDF clienti (richiesta dell'operatore)**: FATTA — 5e006dd2. Cartella `presentazione_clienti/` tolta dal repo (PDF, generatore, script). Prima della rimozione l'operatore ha ricevuto in chat lo zip con sorgenti e PDF, da tenere sul Mac: per modifiche future (es. il sito) vanno chiesti a lui. I file locali con i contatti nel container sono stati cancellati.
- **Revisione legale del PDF**: fatta dall'operatore (19/11); pag. 4 lasciata com'è (decisione dell'operatore).
- **Repo privato**: NON fatto — l'operatore ha scelto di togliere il PDF invece di rendere privato il repo.

## Test
Nessuna modifica a gas.py, modules/ o tests/.

## Anomalie
Le versioni precedenti della presentazione (PR #380 e #384) restano nella storia di git di main; quella pubblicata con #384 non contiene contatti.
