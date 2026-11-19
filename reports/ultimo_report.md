# Ultimo report — 2026-11-19 — Presentazione clienti tolta dal repo

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa sessione (toglie `presentazione_clienti/`; nessun file del motore).

## Esito
- **Togliere da GitHub il PDF clienti (richiesta dell'operatore)**: FATTA — 5e006dd2. Cartella `presentazione_clienti/` tolta dal repo (PDF, generatore, script). Prima della rimozione l'operatore ha ricevuto in chat lo zip con sorgenti e PDF, da tenere sul Mac: per modifiche future (es. il sito) vanno chiesti a lui. I file locali con i contatti nel container sono stati cancellati.
- **Revisione legale del PDF**: fatta dall'operatore (19/11); pag. 4 lasciata com'è (decisione dell'operatore).
- **Repo privato**: NON fatto — l'operatore ha scelto di togliere il PDF invece di rendere privato il repo.
- **Merge di main (#381 CRM) nel branch** per togliere i conflitti della PR #385: FATTA — review #816 APPROVATO (file del motore identici a main).
- **Riserve del bot #385**: FATTA — `presentazione_clienti/` aggiunta al .gitignore principale (V-1: i sorgenti dello zip con i contatti non possono più finire nel repo per sbaglio); voci chiuse (presentazione tolta, CI rossa 26.04 chiusa con la #380) spostate in stato_storico; intestazione di stato_progetto aggiornata al 19/11; riserva «numeri del PDF non verificati da gate» (agente-#380 V-3, ripresa come bot-#384 V-2) decaduta per il repo: il PDF non c'è più e la revisione legale l'ha fatta l'operatore.

## Test
Nessuna modifica a gas.py, modules/ o tests/.

## Anomalie
Le versioni precedenti della presentazione (PR #380 e #384) restano nella storia di git di main; quella pubblicata con #384 non contiene contatti.
