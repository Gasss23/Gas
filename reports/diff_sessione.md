# Diff sessione — 2026-08-19 — fix/r2-riserve-86 (handoff rigenerato)

File toccati in questa sessione (`git diff --stat origin/main...HEAD`):

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `.claude/agents/memoria_revisore.md` | Aggiunto verdetto #87 APPROVATO (chiusura riserve R-r2-1 e R-r2-2) |
| `reports/diff_sessione.md` | Questo file — riscritto per la sessione corrente |
| `reports/handoff.md` | Rigenerato con canonici reali (git log 4 commit, CI 32301097271, verdetto #87 verbatim) |
| `reports/stato_progetto.md` | Aggiornato con esito sessione e riserve chiuse |
| `reports/ultimo_report.md` | Report di fine task aggiornato |
| `scripts/commit_memoria_revisore.sh` | Forma atomica `if ! var=$(cmd)` (chiude R-r2-1, lezione #51) |
| `tests/test_unit_hooks.py` | Aggiunto T-R2-e: copre "file presente + non-git → WARN + exit 0" (chiude R-r2-2) |

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
