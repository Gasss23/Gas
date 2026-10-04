# ULTIMO REPORT — 2026-10-04 — Rami d'errore e loopback del gate IP coperti da test

Branch `test/gate-ip-rami-errore-loopback` · PR #125 · commit `24c8640` (solo test) · review #151 **APPROVATO CON RISERVE** + #152 **APPROVATO**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #125 (variante A: `gasmerge 125`), dopo la verifica esterna.
2. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`? (ancora aperta)
3. V-5 (verifica #121): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review? (ancora aperta)
4. Poi la prossima fetta PRIORITARIA, già decisa: V-B "vera" (bot di revisione su GitHub).

## Esito per step

- **Merge PR #124**: FATTO (`gasmerge 124`, confermato dall'operatore; main `dfb52a5`).
- **V-1 verifica #124** (3 mutation superstiti nel gate IP di fine_task_finale.sh): FATTA. Test 4j (prima git grep rc 128 → STOP prima del push), 4k (riga con solo loopback esente), 4l (filtro allowlist rotto → STOP); gemello `TestIPErroreFiltro` in gasmerge.
- **R-151-1** (review #151: `test_git_grep_error_blocks` non verificava che gasmerge si fermasse al gate): FATTA nella stessa fetta (review #152).
- **V-4 verifica #124** (stato_progetto: frase confusa su R-149-1; "Gate test 65 PASS"): FATTA (riscritta; 74 PASS).
- **V-5 verifica #124** (`_stub_git -> dict`): FATTA (`dict[str, str]`).
- **V-2 verifica #124** (discriminazione del test latin1 su glibc): DEFERITA — non provabile in locale; da chiudere con la V-B o con un job CI di mutation.
- **R-150-1** (ramo PUSH_EXIT morto): DEFERITA, invariata.

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 299 → **303 passed**.
- Mutation uccise (1 failed ciascuna): fine_task_finale.sh (a) `*)` della prima grep → `9999)`, (b) loopback inefficace, (c) senza `exit 1` nel filtro; gasmerge.sh (c) e senza `exit 1` nel ramo `*)` della prima grep (R-151-1).
- Nessuno script modificato: diff solo in tests/.

## Riserve aperte

- V-2 verifica #124 (latin1 su glibc), R-150-1: vedi sopra.

## Anomalie

- Nessuna.
