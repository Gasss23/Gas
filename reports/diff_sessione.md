# DIFF SESSIONE — 2026-10-05 — fix/gate-ip-ip-adiacente-punto

| File | Cosa è cambiato e perché |
|---|---|
| `scripts/gasmerge.sh` | Ancore nuove nelle 3 regex del gate IP: un IP adiacente a un punto è un IP (R-155-1). |
| `scripts/fine_task_finale.sh` | Stesse ancore nelle 3 regex del gate IP (R-155-1). |
| `tests/test_unit_gasmerge.py` | IP adiacente a un punto blocca (6 casi); cinque componenti e loopback seguito da punto passano (3 casi). |
| `tests/test_unit_hooks.py` | Test 4p / 4q speculari per fine_task_finale. |
| `.claude/agents/memoria_revisore.md` | Memoria della review #156; riga #155 redatta (IP a fine frase non marcato). |
| `reports/*` | Report di fine task; stato_progetto (R-155-1 chiusa, R-156-1, residui verifica #127). |

La storia completa sta in git.
