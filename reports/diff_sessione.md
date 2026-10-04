# DIFF SESSIONE — 2026-10-04 — fix/gasmerge-perimetro-gitignore

| File | Cosa è cambiato e perché |
|---|---|
| `scripts/gasmerge.sh` | Gate IP su `refs/remotes/origin/$BRANCH` (verifica esterna #122 V-1). Il promemoria "FILE DI MOTORE" legge il perimetro di review (main ∪ branch), fail-safe se illeggibile; diff con `--no-renames` e `quotePath=false`; ref completi (V-1 #121, R-144-1, R-145-1). |
| `scripts/check_landing.sh` | Check B su `refs/remotes/origin/${BRANCH}` (verifica esterna #122 V-2). |
| `.claude/hooks/promemoria_end.sh` | merge-base su `refs/remotes/origin/main` (R-144-1). |
| `.claude/commands/fine-task.md` | Messaggio d'errore col ref completo (R-144-1). |
| `.gitignore` | `*.wav`, `*.mp3`, output dei client per estensione (V-2 #121, R-145-2). |
| `tests/test_unit_gasmerge.py` | `TestPerimetroPromemoria` (7 test), `TestIPRefCompleto`; stub del diff robusto a `git -c`. |
| `tests/test_unit_hooks.py` | Check B di check_landing con un tag `origin/main` omonimo. |
| `.claude/agents/memoria_revisore.md` | Memoria delle review #145, #146 e #147. |
| `reports/*` | Report di fine task; correzioni R-143-1/R-143-4; V-3, V-5 e R-147-1/2/3 tracciate. |

La storia completa sta in git.
