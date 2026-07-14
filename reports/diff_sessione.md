# diff_sessione — 2026-07-14 (R-crm-1b Fette 2+3)

> Fotografia dell'ultima sessione. La storia completa sta in git.
> BASE: 3987dbe (ultimo commit sessione precedente su handoff.md)

## File toccati (da `git diff --stat 3987dbe..HEAD`)

| File | Delta | Motivo |
|------|-------|--------|
| `modules/memory/store.py` | +143 righe nette | `normalizza_telefono`, `_is_phone`, `_append_sospetto`, modifica `rileva_duplicati_email`, nuovo `rileva_duplicati_telefono` |
| `tests/test_unit_kernel.py` | +122 righe | T59a/b/c (idempotenza email) + T60a-f (telefono) |
| `gas.py` | +27/-7 | `check_dups_cmd` aggiornato per email + telefono |
| `reports/ultimo_report.md` | riscritta | report finale R-crm-1b fette 2+3 |
| `reports/handoff.md` | riscritta | dossier fine sessione con verdetti, CI, delta test |
| `reports/stato_progetto.md` | aggiornata | suite 240 PASS, R-crm-1b rimosso da finding aperti, data aggiornata |
| `reports/finding_archiviati.md` | +1 riga | R-crm-1b archiviato (4 fette, review #47-49) |
| `reports/diff_sessione.md` | riscritta | questo file |
| `modules/memory/__init__.py` | +2 righe | esporta `normalizza_telefono` |
| `.claude/agents/memoria_revisore.md` | +3 righe | lezioni review #49 (fette 2+3) |

## Perché

**Fette 2+3 (motore, commit `1d32819`):** `rileva_duplicati_email` ri-appendeva gli stessi sospetti ad ogni run — problema critico con lo scheduler FASE 4.5 h24. Soluzione fetta 2: `_append_sospetto` con tag `[ids:X,Y]` + check LIKE idempotente. Fetta 3: rilevamento duplicati telefono con normalizzazione forme +39/0039/locale.

**Doc-only (commit `0935efc`):** R-crm-1b completamente chiuso → archiviato. Conteggio CI riconciliato: 240 PASS (non 242 — T9a/T9c con API keys Codespace, comportamento noto).

## Commit sessione

```
0935efc docs(crm-dup-detect): chiusura R-crm-1b — archivia finding, corregge conteggio CI 240 PASS
759d12f docs(crm-dup-detect): handoff — CI run 29342632131 SUCCESS, 242 PASS
83ae3e4 docs(crm-dup-detect): aggiorna report — R-crm-1b fette 2+3, review #49, 242 PASS
1d32819 feat(crm-dup-detect): R-crm-1b Fette 2+3 — idempotenza diario + telefono
7f17c08 auto-commit fine sessione 2026-07-14_14:20 [solo reports/doc/history, motore escluso]
a58757f docs(crm-dup-detect): aggiorna stato_progetto — R-crm-1b fette 1+2, finding R-crm-diario-rr, 48 review, 231 PASS CI
```
