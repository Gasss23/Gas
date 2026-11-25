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
- **Fetta 4 — Riserve del bot #407**: FATTA.
  - I modelli pronti passano col nome esatto, anche quello del file con la versione (alexa_v0.1): chiude V-1 e R-866-1.
  - L'avviso di ripiego compare una volta sola (R-864-2).
  - Docstring e LEGGIMI aggiornati (V-2).
  - Il test controlla il nome passato al rilevatore (V-3).
- Test: `tests/test_unit_voce_ascolto.py` da 391 a 395 passed.
- Review: #864–#867, APPROVATO CON RISERVE.

## Riserve aperte
- R-867-1 BASSA, che c'era già prima: un modello pronto non scaricato (es. alexa) fa uscire l'ascolto invece di ripiegare.
- R-854-3 BASSA: interruzione col modello italiano non misurata.
- Ripiego su hey_jarvis con la soglia 0,5: aperta, BASSA.
