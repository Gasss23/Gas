# ULTIMO REPORT — 2026-10-04 — Gate IP: allowlist sul solo contenuto, tree unico, binari/non-UTF-8; gasmerge in CI

Branch `fix/gate-ip-allowlist-ci-gasmerge` · PR #123 · commit `09d4005` · review #148 + #149 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #123 (variante A: `gasmerge 123`), dopo la verifica esterna.
2. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`? (ancora aperta)
3. V-5 (verifica #121): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review? (ancora aperta)
4. Poi la prossima fetta PRIORITARIA, già decisa: V-B "vera" (bot di revisione su GitHub).

## Esito per step

- **Merge PR #122**: FATTO (`gasmerge 122`, confermato dall'operatore; main `ee95197`).
- **V-1 verifica #122 bis = R-147-1** (un branch o un path con `gasmerge-ip-ok` aggirava il gate IP): FATTA in gasmerge.sh e fine_task_finale.sh (`git grep --and --not` sul solo contenuto).
- **V-2 verifica #122 bis = R-147-3** (`test_unit_gasmerge.py` non girava in CI): FATTA, nuovo step in ci.yml.
- **Correzione di un'affermazione falsa**: nei report della PR #122 c'era scritto "unit-suite verde su Linux, test non-ASCII compreso". Era FALSO: quel test non girava in CI. Da questa PR gira.
- **V-3 verifica #122 bis** (nomi con apice/tab/backslash sfuggivano al promemoria): FATTA, `git diff -z`.
- **R-147-2** (mutation sopravvissute): FATTA sul perimetro letto da main; `gasmerge.sh:42` (solo visualizzazione) resta senza test, dichiarato.
- **R-148-1 / R-148-2 / R-148-3** (review #148): FATTE nella stessa fetta. R-148-3 era un bypass preesistente: un IP in un file binario o in una riga non UTF-8 sfuggiva al gate.
- **stato_progetto** "116 review" → "149 review": FATTA.
- **R-149-1** (bassa): DEFERITA. Mancano 2 test gemelli per fine_task_finale.sh; il codice è corretto.

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 284 → **293 passed**.
- Controprove: i nuovi test falliscono sugli script di main (avvelenati, apice, binario, latin1, finale 4d/4e). Mutation uccise: ramo d'errore della allowlist, perimetro di main abbreviato, `-a` e `LC_ALL=C` in gasmerge.sh.
- Kernel non rilanciato: la fetta non tocca gas.py, brains/ o modules/.

## Riserve aperte

- R-149-1 (bassa): vedi sopra.
- V-3 / V-5 della verifica #121: decisioni operatore.

## Anomalie

- La verifica esterna bis di #122 ha trovato che un'affermazione dei report di #122 (CI su Linux per il test non-ASCII) era falsa. L'agente l'aveva dedotta da "unit-suite verde" senza controllare quali file girano in CI.
