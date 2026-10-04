# ULTIMO REPORT — 2026-10-04 — Test gemelli del gate IP in fine_task_finale e tree unico

Branch `test/gate-ip-gemelli-tree-unico` · PR #124 · commit `7f03488` (solo test) · review #150 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #124 (variante A: `gasmerge 124`), dopo la verifica esterna.
2. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`? (ancora aperta)
3. V-5 (verifica #121): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review? (ancora aperta)
4. Poi la prossima fetta PRIORITARIA, già decisa: V-B "vera" (bot di revisione su GitHub).

## Esito per step

- **Merge PR #123**: FATTO (`gasmerge 123`, confermato dall'operatore; main `b3c6de3`).
- **V-2 verifica #123 = R-149-1** (in fine_task_finale.sh sopravvivevano 7 mutation su 11, non 2): FATTA. Test 4f (latin1), 4g (errore della grep allowlist), 4h (tree non risolvibile), 4i (HEAD spostato fra le grep): uccise tutte le 12 mutation del gate IP.
- **V-1 verifica #123 = R-148-2 senza test**: FATTA. Ref spostato fra le due git grep → BLOCCO in gasmerge; G9 (tree non risolvibile) coperta anche in gasmerge.
- **V-3 verifica #123** (limite UTF-16 del gate IP): FATTA, annotato in stato_progetto come limite noto.
- **V-4 verifica #123** (stato_progetto: "gate suite non in ci.yml"): FATTA, nota corretta.
- **R-150-1** (bassa, preesistente: ramo `PUSH_EXIT` morto in fine_task_finale.sh): DEFERITA, tracciata.

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 293 → **299 passed** (riprodotto dal revisore; il mio 298 intermedio era stato contato prima del test G9).
- Mutation su fine_task_finale.sh F1–F12: tutte uccise. Su gasmerge.sh: tree→ref (TOCTOU) e G9 uccise.
- Nessuno script modificato: diff solo in tests/.

## Riserve aperte

- R-150-1 (bassa): vedi sopra.
- Limite noto del gate IP: cieco a UTF-16 e a IP spezzati o codificati.
- Possibile: su glibc il test latin1 potrebbe non discriminare LC_ALL=C (su macOS sì). Vedi §6 dell'handoff.

## Anomalie

- Nessuna.
