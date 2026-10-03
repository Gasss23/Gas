# ULTIMO REPORT — 2026-10-03 — Gate B per-verdetto + marcatore di review legato al diff

Branch `fix/gate-b-verdetto` · PR #118 · commit `a52f92b` · review #136 + #137 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #118 (variante A: `gasmerge 118`, l'operatore conferma digitando il numero).

## Esito per step

- **R-135-4** (la frase "nessun diff motore" bypassava il gate B): CHIUSA. L'esenzione dipende dal diff reale.
- **R-135-1 / R-135-2** (verdetto solo-contesto o vuoto accettato): CHIUSE. Ogni blocco `VERDETTO:` deve avere ≥2 citazioni di file del diff, esclusi reports/ e la memoria del revisore.
- **R-135-3** (regola di revisore.md): CHIUSA, approvata dall'operatore. Ora vale "≥2 nel diff, contesto ammesso e verificato a HEAD"; la prima riga `## VERDETTO: <esito>` è obbligatoria.
- **Marcatore `.review_ok` residuo** (anomalia C4b-3): CHIUSA. Il marcatore contiene lo SHA-256 del diff staged (`bash scripts/segna_review_ok.sh`). Un marcatore residuo o vuoto non apre il gate. Primo uso reale riuscito sul commit `a52f92b`.
- **R-136-1** (`commit -a` / pathspec): CHIUSA. Il gate blocca le modifiche al motore non in stage o non tracciate.
- **R-136-4** (hash dipendente dalla config git): CHIUSA.
- **R-136-2** (verdetto senza riga VERDETTO): MITIGATA con la regola di formato; il controllo incrociato nel gate è DEFERITO.
- **R-c4b3-5** (timeout = "esito incerto"): DEFERITA alla prossima fetta motore.

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py`: 237 → **247 passed**.
- Kernel non rilanciato: la fetta non tocca gas.py, brains/ o modules/.

## Riserve aperte

R-136-2 (mitigata), R-136-3, R-136-5, R-137-1, R-137-2, R-137-3. Dettaglio in `reports/stato_progetto.md`.

## Anomalie

- Il matcher del gate (R-gjq-1) ha bloccato un mio comando che conteneva il testo "git … commit" dentro una patch: l'ho rieseguita da un file.
