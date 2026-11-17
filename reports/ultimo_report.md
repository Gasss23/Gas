# Ultimo report — 2026-11-17 — Voce: filtro sulla voce dell'operatore (M1)

## DECISIONI UMANE RICHIESTE
1. Merge della PR (solo R-804-3 COSMETICA aperta).
2. Dopo il merge registrare la voce sul Mac (circa 5 minuti).

## Esito
- **Causa del «non risponde» (taratura sul Mac del 17/11):** il modello hey_jarvis dà alla voce normale dell'operatore solo 0,37-0,43: nessuna soglia sicura basta.
- **Verificatore della voce:** FATTO. `scripts/voce/registra_voce.py` registra 15 «Hey Jarvis» da posizioni diverse più parlato e TV (solo sul Mac, mai nel repo) e addestra un filtro. Con il filtro, soglia base 0,25 per prendere le chiamate deboli, filtro a 0,5 per scartare TV e altre persone. Senza il file del filtro tutto resta come prima. Review #804 APPROVATO CON RISERVE → #805 APPROVATO.
- **Guida in giro:** `reports/guida_voce_in_giro.md` (Telegram vocali, Comando Rapido iPhone, Siri che legge le risposte).
- **Data e ora nel prompt:** scartato (c'erano già), review #803 BOCCIATO.

## Test
voce_ascolto 346 → 373 passed; voice_server 236.

## Anomalie
Nessuna. Da provare sul Mac.
