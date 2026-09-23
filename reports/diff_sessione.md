# Diff sessione — 2026-09-23

File toccati (da `git diff --stat BASE..HEAD`, BASE=6477ffa):

| File | Cosa è cambiato e perché |
|---|---|
| `.claude/hooks/promemoria_end.sh` | Aggiunta riga grep fallback: quando python3 è assente/fallente, `_SHA` è vuota e il flag `stop_hook_active=true` non veniva rilevato → hook poteva bloccare in anti-loop. Fix: una riga `&&`-chain con grep POSIX. |
| `tests/test_unit_hooks.py` | Aggiunto `extra_env` a `_run_promemoria`, helper `_make_broken_python3_path`, test T-prom-8 e T-prom-8b che coprono il nuovo path con python3 simulato assente. |
| `.claude/agents/memoria_revisore.md` | Aggiornata dal revisore con lezione review #102 (pattern fallback grep per parser python3 monouso in bash). |

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
