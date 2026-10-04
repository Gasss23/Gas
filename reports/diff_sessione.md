# DIFF SESSIONE — 2026-10-04 — test/gate-ip-rami-errore-loopback

| File | Cosa è cambiato e perché |
|---|---|
| `tests/test_unit_hooks.py` | fine_task_finale: prima git grep rc 128 (4j), solo loopback (4k), filtro allowlist rotto (4l); `_stub_git -> dict[str, str]` (V-1 / V-5 verifica #124). |
| `tests/test_unit_gasmerge.py` | `TestIPErroreFiltro`; `test_git_grep_error_blocks` verifica l'arresto al gate (R-151-1). |
| `.claude/agents/memoria_revisore.md` | Memoria delle review #151 e #152. |
| `reports/*` | Report di fine task; stato_progetto (nuova voce, R-149-1 riscritta, gate test 74 PASS, conteggio review). |

La storia completa sta in git.
