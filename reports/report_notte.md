# Report del turno di notte — 2026-10-24 (prima notte di prova, R3)

Ramo `notte/2026-10-24`, PR #259 (https://github.com/Gasss23/Gas/pull/259). Nessun merge (regola del turno).
Prima notte: nessun ramo `notte/*` su GitHub e «Fatte» vuota → SOLO le voci 1 e 2, solo documenti.

## Voce 1 — Note cosmetiche del bot su #249 — FATTA
- **Cosa**: in `stato_progetto.md` l'intestazione «Ultimo aggiornamento» ora nomina la sessione «2026-10-22 sera (decisione porte 80/443, PR #249)» (V-2 bot #249); in `da_mergiare.md` il titolo «Da fare domattina … 2026-10-21 sera» diventa «Da fare (operatore) — aperte dal 2026-10-21 sera, sezione rivista il 2026-10-22 e il 2026-10-24» (V-3); nel §2 dell'handoff di stanotte c'è la nota che la riga di `handoff.md` non conta il commit finale (V-1).
- **Perché / cosa migliora**: intestazioni e titoli dicono il vero; chi confronta il §2 col diff della PR non scambia lo scarto per un errore.
- **Rischi**: nessuno (solo documenti). La nota del §2 vale solo per questo handoff: per renderla fissa va messa nel template `.claude/commands/fine-task.md`, che è nel perimetro di review (vedi decisioni).
- **Non fatto**: la parte di V-3 bot #249 su «protezioni del repo» non tracciate in nessun documento non era nella voce: resta da tracciare (vedi decisioni).

## Voce 2 — Prova del 22 ottobre dopo #247 — FATTA
- **Cosa**: nuovo blocco «R1 — seconda prova dal vero dopo #247» in `stato_progetto.md`: Gas compila da solo pro e contro, la firma arriva al primo messaggio, Rifiuta non esegue. Il vecchio 🟡 «Bottone Rifiuta senza effetto» (8 ottobre, voce 9) è segnato superato.
- **Perché / cosa migliora**: il difetto della prima prova (pro e contro chiesti all'utente) risulta chiuso anche dal vero, non solo nei test.
- **Rischi**: l'unica fonte è la voce della coda (resoconto dell'operatore): nel repo non ci sono log della prova. Se il resoconto fosse impreciso, il 🟡 chiuso andrebbe riaperto.

## Verifica del bot su #259
APPROVATO CON RISERVE, CI verde. V-1 BASSA (conteggio di `handoff.md` nel §2 non misurato: ora «n/d») e V-2 COSMETICA (forma delle voci in «Fatte») corrette in un secondo commit.

## Cosa deve decidere l'operatore
1. Merge della PR #259 (il turno di notte non mergia).
2. Se rendere fissa la nota sul conteggio di `handoff.md` nel template `fine-task.md` (perimetro di review: una fetta di giorno o una voce della coda).
3. Dove tracciare «protezioni del repo» (impegno rimandato citato da V-3 bot #249, oggi in nessun documento).
4. Il testo dell'attività programmata va ancora cambiato come scritto in `coda_notte.md` (bot #253, V-2/V-3): il turno di notte non l'ha toccato.
