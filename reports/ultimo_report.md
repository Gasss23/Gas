# Ultimo report — 2026-11-25 — Voce: log più chiari e nome del modello sicuro (dopo la PR #405)

## DECISIONI UMANE RICHIESTE
Nessuna nuova. Merge della PR: se il bot dà APPROVATO pulito lo fa l'agente, altrimenti serve il «mergia» dell'operatore.

## Esito
- **Fetta 1 — Log del primo turno scartato**: FATTA.
  - Prova del 25/11 sul Mac: dopo «Hey Jarvis» la richiesta era di 1,0 s, con 0,2 s di voce. Il server l'ha chiusa con «fine» perché la trascrizione era vuota.
  - Il client scriveva «turno di seguito non rivolto a Gas» anche sul primo turno. Ora scrive «richiesta scartata dal server (trascrizione vuota o non chiara…)».
- **Fetta 2 — Nome del modello**: FATTA.
  - Un nome non semplice in `GAS_ASCOLTO_MODELLO` (un percorso, un nome strano) ripiega su hey_jarvis: chiude V-1 del bot #405.
  - In `main` il nome si normalizza: «Hey Jarvis» vale hey_jarvis, filtro della voce compreso (R-864-1).
- **Fetta 3 — Log di avvio**: FATTA. «ascolto pronto» dice il modello davvero in uso: dal file, oppure ripiego (R-855-1).
- Test: `tests/test_unit_voce_ascolto.py` da 391 a 394 passed.
- Review: #864 e #865, APPROVATO CON RISERVE.

## Riserve aperte
- R-864-2 COSMETICA: all'avvio l'avviso di ripiego compare due volte.
- R-854-3 BASSA: interruzione col modello italiano non misurata.
- Ripiego su hey_jarvis con la soglia 0,5: aperta, BASSA.
