# DIFF SESSIONE — 2026-10-05 — fix/gate-ip-inizio-riga-mktemp

| File | Cosa è cambiato e perché |
|---|---|
| `scripts/gasmerge.sh` | `mktemp` con le X in fondo al nome e guardia esplicita (R-153-2). |
| `tests/test_unit_gasmerge.py` | `TestFileTemporaneo` (nomi casuali, residui letterali, TMPDIR inesistente); IP a inizio riga + `.dominio`. |
| `tests/test_unit_hooks.py` | Casi IP a inizio riga, inizio riga + `.dominio`, file senza newline in 4p (V-1 verifica #128). |
| `.claude/agents/memoria_revisore.md` | Memoria della review #157. |
| `reports/*` | Report di fine task; stato_progetto (R-153-2, V-1 #128, R-156-1 chiuse). |

La storia completa sta in git.
