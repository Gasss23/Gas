# ULTIMO REPORT — 2026-10-04 — Rename nel §2, perimetro più largo, check CI presi da main

Branch `fix/gate-rename-perimetro-ci` · PR #121 · commit `13b7933` · review #143 + #144 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #121 (variante A: `gasmerge 121`), dopo la verifica esterna.
2. Prossima fetta PRIORITARIA, già decisa: V-B "vera", cioè revisione con identità separata su GitHub (bot + segreti). Servirà una chiave API di Claude da inserire nei segreti di GitHub: la inserisce l'operatore, l'agente non la vede mai.

## Esito per step

- **V-3** (un rename rendeva impossibile un §2 onesto): CHIUSA.
- **V-2** (perimetro più largo: gas_identity.md, requirements*.txt, tools/, clients/): CHIUSA.
- **R-141-2** (la CI eseguiva i check della PR stessa): MITIGATA. La CI ora usa i check di `main`. Resta R-143-2: ci.yml viene ancora dalla PR.
- **R-143-1** (un tag "origin/main" poteva dirottare base e check): CHIUSA, con il ref completo in CI, negli script e nel fine-task.
- **R-143-4** (.DS_Store bloccava i commit): CHIUSA.
- **Nota b** (stat troncato o quotato): FATTA in fine-task.
- **V-1 della verifica #120** (V-A sovrastimata): la formulazione in stato_progetto è CORRETTA. Copre l'omissione onesta, non l'aggiramento deliberato.
- **Variante B del merge**: DECISA dall'operatore, ATTIVA solo dopo V-B vera + test di convalida.
- **R-143-2 / R-143-3**: DEFERITE (R-143-2 viene chiusa dalla V-B vera).

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py`: 271 → **275 passed**.
- Controprove: il test del rename fallisce con lo script di main; il test del tag fallisce con il ref abbreviato.
- Simulazione della CI in un clone usa-e-getta: se una PR sabota i propri check, la versione presa da main la blocca comunque (rc=1).
- Kernel non rilanciato: la fetta non tocca gas.py, brains/ o modules/.

## Riserve aperte

R-143-2, R-143-3, R-144-1 (ref abbreviato in gasmerge.sh: prossima fetta), V-B, V-C, R-139-1, R-141-2 (mitigata). Dettaglio in `reports/stato_progetto.md`.

## Anomalie

- Il gate di review ha bloccato un mio commit temporaneo di simulazione: avevo modifiche al perimetro fuori stage. Comportamento corretto. La simulazione l'ho rifatta in un clone usa-e-getta.
