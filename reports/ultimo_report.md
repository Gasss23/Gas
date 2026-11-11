# Ultimo report — 2026-11-10 — Decisioni dell'operatore: avviso Flash-lite, tetto di 10 chiamate per turno, nomi dei lead mai ai modelli non forti (M1)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #370 (https://github.com/Gasss23/Gas/pull/370).
2. R-753-M1-A: i risultati di `ricorda`/`salva_contatto` già nella storia, il testo dell'operatore `recap_pin` e la riflessione di fine task (ve #370 V-1) possono contenere nomi di clienti e arrivano ancora ai modelli non forti. Estendere il blocco anche lì? sì/no

## Esito
- **(a) Primo cervello non configurato = ripiego dichiarato** (sì dell'operatore): FATTA — nessun cambio di codice, test T113a4 lo fissa.
- **(b) Flash-lite dichiarato** (sì): FATTA — `RUNG_VERSIONE_LEGGERA`, riga «↪ risposta da … (versione leggera scelta per un compito semplice)» in CLI e testo Telegram, mai a voce.
- **Tetto di 10 chiamate al modello per turno** (sì): FATTA — `MAX_CHIAMATE_TURNO`, contatore unico fra i cervelli; `for _ in range(10)` resta come barriera per cervello (§8).
- **Nomi dei lead mai ai modelli non forti** (sì): FATTA per il pin della memoria — variante piena solo a claude-cli, anonima agli altri. DEFERITA la storia/recap (R-753-M1-A, decisione dell'operatore).
- **Bot #370 5° giro V-1 (MEDIA)**: pin anonimo fail-closed se la lettura dei contatti fallisce — FATTA (T114f2, review #765-M1coord APPROVATO CON RISERVE, R-765-1-M1coord BASSA).
- Review #753-M1: 1° giro APPROVATO CON RISERVE, 2° giro APPROVATO.

## Test
Kernel 1119 → 1134 PASS / 0 FAIL; pytest telegram_voce+notte+sottofondo+gate+manutenzione+voice_server (-k "not browser") 1448 passed.

## Anomalie
Nessuna.
