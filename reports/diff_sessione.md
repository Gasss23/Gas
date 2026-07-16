# Diff sessione — 2026-07-16 (F6 atomicità .gas_history.json)

> Fotografia della sessione corrente. Si riscrive a ogni sessione; la storia completa sta in git.
> BASE: `fe0e476e960fda6f5cca30fb160ca4464cd31f96` (merge PR #18)

## File toccati

| File | Motivo |
|------|--------|
| `gas.py` | F6: `_save_history` resa atomica (tmp+fsync+`os.replace`); `_load_history` con quarantena file corrotto in `.corrupt.*` |
| `tests/test_unit_kernel.py` | Aggiunta blocco T59a/b/c: round-trip, corruzione→quarantena, `os.replace` fail→intatto |
| `reports/stato_progetto.md` | Contatore review 48→50; F6 chiuso ✅; micro-finding processo (c)(f); discrepanza memoria_revisore dichiarata; R-crm-diario-rr confermato CHIUSO |
| `reports/ultimo_report.md` | Report canonico F6 con verdetto #50 VERBATIM, analisi discrepanza contatore, analisi gate review #49 |
| `reports/handoff.md` | Dossier di fine sessione (§0-§7) |
| `reports/diff_sessione.md` | Questo file |

## Commit della sessione

```
77bda38 docs(report): fine task F6 atomicità — report, stato_progetto aggiornato
e9ffee0 fix(kernel): F6 atomicità .gas_history.json — write tmp+rename, quarantena corrotto
```

## Note

- Review #50: APPROVATO (nessuna riserva). Nessuna lezione aggiunta a `memoria_revisore.md`.
- CI: entrambi i commit SUCCESS (run `29482410951` e `29483156128`).
- PR #19 aperta, merge pendente (umano).
- Proposta fuori scope: cherry-pick `92a08ba` per recuperare lezione review #49 su `memoria_revisore.md`.
