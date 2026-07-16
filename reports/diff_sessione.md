# Diff sessione — 2026-07-16 (F1 R-crm-diario-rr)

> Fotografia dell'ultima sessione. La storia completa sta in git.

## File toccati (git diff --stat BASE=e7b4486..HEAD)

| File | Modifica | Perché |
|------|----------|--------|
| `modules/memory/store.py` | +1 riga | `PRAGMA recursive_triggers = ON` in `_connect()` — chiude il varco che consentiva INSERT OR REPLACE di riscrivere righe del diario aggirando i trigger di immutabilità |
| `tests/test_unit_kernel.py` | +30 righe | Nuovo test T19f-rr: verifica ABORT su INSERT OR REPLACE sulla PK del diario + riga originale intatta; usa `m._connect()` per rilevare future rimozioni del PRAGMA |
| `reports/stato_progetto.md` | -1/+1 | Chiude riserva R-crm-diario-rr (CHIUSO con PR #18) |
| `reports/ultimo_report.md` | riscritto | Report canonico fine task F1 |
| `reports/handoff.md` | riscritto | Dossier di fine sessione |
| `reports/diff_sessione.md` | riscritto | Questo file |

## Nota sessione

- Branch: `fix/diario-recursive-triggers` (da `origin/main` = `e7b4486`)
- PR #18 aperta, CI SUCCESS su entrambi i commit motore (`894eb06`) e doc (`690c4e0`)
