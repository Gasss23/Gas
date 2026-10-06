# DIFF SESSIONE — 2026-10-06 — fix/fine-task-push-exit (R-150-1)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `scripts/fine_task_finale.sh` — `git push || PUSH_EXIT=$?`: il ramo del push fallito non è più morto sotto `set -e` (R-150-1).
- `tests/test_unit_hooks.py` — T-finale-5: push rifiutato → exit 1 + messaggio, niente URL, niente guardia @{u}.
- `reports/stato_progetto.md` — R-150-1 CHIUSA, frase corretta (R-166-1).
- `.claude/agents/memoria_revisore.md` — righe #166 (rinumerata da #163) e #168.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
