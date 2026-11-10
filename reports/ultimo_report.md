# Ultimo report — 2026-11-10 — Decisioni dell'operatore: avviso Flash-lite, tetto di 10 chiamate per turno, nomi dei lead mai ai modelli non forti (M1)

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa sessione (numero nel §0 dell'handoff).
2. R-753-M1-A: i risultati di `ricorda`/`salva_contatto` già nella storia, il testo dell'operatore e `recap_pin` possono contenere nomi di clienti e arrivano ancora ai modelli non forti nei turni successivi. Estendere il blocco anche lì? sì/no

## Esito
- **(a) Primo cervello non configurato = ripiego dichiarato** (sì dell'operatore): FATTA — nessun cambio di codice, test T113a4 lo fissa.
- **(b) Flash-lite dichiarato** (sì): FATTA — `RUNG_VERSIONE_LEGGERA`, riga «↪ risposta da … (versione leggera scelta per un compito semplice)» in CLI e testo Telegram, mai a voce.
- **Tetto di 10 chiamate al modello per turno** (sì): FATTA — `MAX_CHIAMATE_TURNO`, contatore unico fra i cervelli; `for _ in range(10)` resta come barriera per cervello (§8).
- **Nomi dei lead mai ai modelli non forti** (sì): FATTA per il pin della memoria — variante piena solo a claude-cli, anonima agli altri. DEFERITA la storia/recap (R-753-M1-A, decisione dell'operatore).
- Review #753-M1: 1° giro APPROVATO CON RISERVE, 2° giro APPROVATO.

## Test
Kernel 1119 → 1134 PASS / 0 FAIL; pytest telegram_voce+notte+sottofondo+gate+manutenzione+voice_server (-k "not browser") 1448 passed.

## Anomalie
Nessuna.
