# ULTIMO REPORT — 2026-10-04 — V-A: handoff-check davvero vincolante

Branch `fix/handoff-check-vincolante` · PR #120 · commit `501ab76` · review #141 + #142 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #120 (variante A: `gasmerge 120`), dopo la verifica esterna.

## Esito per step

- **V-A** (verifica esterna PR #119, ALTA: `handoff-check` era required ma si saltava): CHIUSA. Quando la sessione tocca il perimetro di review, `check_handoff` e `check_verdetto` danno ERRORE in questi casi: handoff assente dal diff o dal disco, §4 non trovata. Fuori perimetro restano "non applicabile".
- **R-141-1** (`git diff` fallito → insieme vuoto → "non applicabile"): CHIUSA. Ora merge-base o `git diff` falliti danno sempre exit 1.
- **Correzione V-3** nei report: la dichiarazione "CHIUSA" della fetta precedente era una sovrastima. Era MITIGATA, ed è chiusa da questa fetta.
- **Cosmetica #140** (commento duplicato nell'hook): FATTA.
- **V-B, V-C, V-D** (verifica esterna PR #119): DEFERITE, tracciate in stato_progetto.

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py`: 266 → **271 passed**.
- Controprova: i test di V-A e di R-141-1 falliscono con gli script precedenti.
- Kernel non rilanciato: la fetta non tocca gas.py, brains/ o modules/.

## Riserve aperte

R-141-2 (la CI esegue gli script della PR stessa), V-B, V-C, V-D/R-138-5, R-139-1. Dettaglio in `reports/stato_progetto.md`.

## Anomalie

- Il primo push del branch (commit `501ab76`, senza handoff) ha fatto diventare ROSSO `handoff-check`: V-A che lavora sul serio. Il push di fine-task con l'handoff deve farlo tornare verde.
