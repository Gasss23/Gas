# ULTIMO REPORT — 2026-10-04 — Passata unica di mutation sul gate IP (66/66 uccise)

Branch `test/gate-ip-passata-mutation` · PR #126 · commit `c2c2d3e` (solo test) · review #153 **APPROVATO CON RISERVE** + #154 **APPROVATO**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #126 (variante A: `gasmerge 126`), dopo la verifica esterna.
2. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`? (ancora aperta)
3. V-5 (verifica #121): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review? (ancora aperta)
4. Poi la prossima fetta PRIORITARIA: V-B "vera" (bot di revisione su GitHub), condizione per il gasmerge completamente automatico (variante B).

## Esito per step

- **Merge PR #125**: FATTO (`gasmerge 125`, confermato dall'operatore; main `eeaaf1b`).
- **Passata unica di mutation sul gate IP** (richiesta dell'operatore): FATTA. Harness sistematico su `gasmerge.sh` e `fine_task_finale.sh`; esito finale 66/66 mutation uccise. Il revisore ha rilanciato in modo indipendente 28/28 con un proprio harness.
- **V-1 verifica #125** (gasmerge: il ramo "IP non allowlistati" stampava BLOCCO ma un mutante arrivava fino al merge): FATTA, il test ora verifica l'arresto.
- **V-2 verifica #125** (sed senza `g`: due loopback sulla stessa riga): FATTA in entrambi gli script.
- **R-153-1** (MEDIA, preesistente; spazi ai bordi, backslash, riga mista loopback+IP): FATTA (review #154).
- **R-153-2** (bassa: `mktemp` di gasmerge su BSD non randomizza il nome): DEFERITA, fail-closed.
- **V-3 verifica #125** (latin1 su glibc): DEFERITA (CI di mutation o V-B).
- **Gasmerge automatico (variante B)**: DEFERITO per decisione dell'operatore del 2026-10-04: richiede prima la V-B chiusa e i test di convalida.

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 303 → **314 passed**.
- Mutation: prima passata 50/51 (l'unica sopravvissuta era equivalente); dopo i test della #153, passata estesa **66/66**.
- Nessuno script modificato: diff solo in tests/.

## Riserve aperte

- R-153-2, latin1 su glibc, R-150-1: vedi stato_progetto.

## Anomalie

- La prima esecuzione del revisore in parallelo ha dato falsi KILLED (collisione di `mktemp`, R-153-2): l'harness va lanciato solo in sequenza.
