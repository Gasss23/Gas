# DIFF SESSIONE — 2026-10-04 — fix/gate-rename-perimetro-ci

| File | Cosa è cambiato e perché |
|---|---|
| `scripts/check_handoff.py` | `--no-renames -z` ed espansione dei rename del §2 (V-3); merge-base col ref completo (R-143-1). |
| `scripts/check_verdetto.py` | Merge-base col ref completo (R-143-1). |
| `.claude/perimetro_review.txt` | + gas_identity.md, requirements*.txt, tools/, clients/ (V-2). |
| `.github/workflows/ci.yml` | handoff-check esegue i check presi da `refs/remotes/origin/main` (R-141-2, R-143-1). |
| `.claude/commands/fine-task.md` | BASE col ref completo; §2 generato con quotePath=false e --stat=400. |
| `scripts/fine_task_finale.sh` | BASE col ref completo. |
| `.gitignore` | `.DS_Store` (R-143-4). |
| `tests/test_unit_handoff_check.py` | Rename incollato onestamente, forme di espansione, voci del perimetro, tag "origin/main". |
| `.claude/agents/memoria_revisore.md` | Memoria delle review #143 e #144. |
| `reports/*` | Report di fine task; riformulazione di V-A; V-B vera come priorità. |

La storia completa sta in git.
