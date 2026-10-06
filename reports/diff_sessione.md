# DIFF SESSIONE — 2026-10-06 — feat/g3-agente-non-admin (G-3 fase 1)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `scripts/avviso_token_admin.sh` — nuovo: avviso se il token gh amministra il repo (mai blocco).
- `scripts/gasmerge.sh` — path dell'avviso via `realpath` prima del `cd` (anche dal symlink); chiamata dopo il fetch.
- `scripts/fine_task_finale.sh` — chiamata dell'avviso prima del push.
- `.claude/perimetro_review.txt` — + `scripts/avviso_token_admin.sh`.
- `tests/test_unit_gasmerge.py` — TestAvvisoTokenAdmin (esiti, gasmerge diretto e via symlink).
- `tests/test_unit_hooks.py` — avviso G-3 in fine-task prima del push, senza bloccare.
- `reports/setup_agente_non_admin.md` — nuovo: passi per il token fine-grained dell'agente.
- `CLAUDE.md` — regola "agente non admin".
- `reports/stato_progetto.md` — voce G-3.
- `.claude/agents/memoria_revisore.md` — righe #186, #187.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
