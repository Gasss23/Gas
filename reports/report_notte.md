# Report del turno di notte — 2026-10-27

Ramo `notte/2026-10-27`, PR #273 (https://github.com/Gasss23/Gas/pull/273). Nessun merge (regola del turno).
La voce 4 risulta fatta (PR #271 ancora aperta). Al massimo UNA voce del motore a notte: presa la voce 5. La voce 6 (cambio di schema del DB) resta alla prossima notte; in coda non ci sono voci solo-documenti.

## Voce 5 — Contatti illeggibili mai «0 lead» — FATTA
- **Cosa**: nuova lettura dei contatti `leggi_contatti` (`modules/memory/store.py`) che dà «nessun risultato» (None) se il database non risponde, invece di una lista vuota. La usano il resoconto del mattino e `ricorda fermi`: se la lettura fallisce scrivono «Lead attivi: non letti» / «Elenco dei lead NON letto», mai «0 lead» o «nessun lead attivo».
- **Perché / cosa migliora**: con il database bloccato per un attimo fra due letture il messaggio del mattino diceva «Lead attivi: 0», un falso rassicurante (R-454-1 / V-2 bot #241).
- **Controlli**: test nuovi (tabella dei contatti illeggibile su un DB vero con le firme ancora leggibili; un giro notturno completo; un round-trip con `ricorda`) che falliscono sul codice di prima. kernel 1037 → 1039 PASS 0 FAIL; pytest 2241 → 2243 passed. Review #520 APPROVATO CON RISERVE.
- **Rischi**: bassi. Gli altri usi di `lista_contatti` (pin, duplicati, ricerca) non cambiano. Resta R-520-1: `gas fida-contatto` senza argomenti ha ancora lo stesso difetto (fuori da questa voce). Non provato un vero blocco del DB fra due processi.

## Cosa deve decidere l'operatore
1. Merge della PR #273 (il turno di notte non mergia). Anche la PR #271 (voce 4) è ancora aperta: entrambe toccano «Fatte» di `coda_notte.md` e `stato_progetto.md`, quindi la seconda che entra avrà un conflitto da risolvere (tenere entrambe le righe).
2. Se mettere in coda R-520-1 (`gas fida-contatto` con lettura fallita).
3. Il testo dell'attività programmata è ancora quello vecchio: se lo vuoi cambiare, chiedilo in questa sessione.
