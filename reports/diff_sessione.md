# DIFF SESSIONE — 2026-10-04 — fix/gate-ip-allowlist-ci-gasmerge

| File | Cosa è cambiato e perché |
|---|---|
| `scripts/gasmerge.sh` | Gate IP: tree risolto una volta, `git grep -a` con `LC_ALL=C`, allowlist sul solo contenuto (`--and --not`); promemoria con `git diff -z` (R-147-1, R-148-2/3, V-3 #122 bis). |
| `scripts/fine_task_finale.sh` | Stesso gate IP di gasmerge.sh (R-147-1, R-148-2/3). |
| `.github/workflows/ci.yml` | Step `pytest tests/test_unit_gasmerge.py` + riga nel summary (V-2 #122 bis, R-147-3). |
| `tests/test_unit_gasmerge.py` | Branch/path avvelenati, errore della grep allowlist, binari, latin1, nome con apice, tag sul perimetro di main; stub gh con head_ref; `errors="replace"`. |
| `tests/test_unit_hooks.py` | fine_task_finale: path avvelenato (4d), binario con IP (4e). |
| `.claude/agents/memoria_revisore.md` | Memoria delle review #148 e #149. |
| `reports/*` | Report di fine task; stato_progetto (R-147/R-148 chiuse, R-149-1, conteggio review). |

La storia completa sta in git.
