# DIFF SESSIONE — 2026-10-03 — fix/gate-b-verdetto

| File | Cosa è cambiato e perché |
|---|---|
| `scripts/check_verdetto.py` | Esenzione dal diff reale (R-135-4); ≥2 citazioni del diff per ogni verdetto (R-135-1/2). |
| `scripts/hash_diff_staged.sh` | Nuovo: SHA-256 del diff staged, indipendente dalla config git (R-136-4). |
| `scripts/segna_review_ok.sh` | Nuovo: scrive il marcatore `.review_ok` con l'hash, dopo il verdetto. |
| `.claude/hooks/review_gate.sh` | Accetta solo il marcatore con l'hash del diff attuale; blocca il motore non in stage (R-136-1). |
| `.claude/agents/revisore.md` | Regola delle citazioni (R-135-3) e riga `## VERDETTO:` obbligatoria (R-136-2). |
| `CLAUDE.md` | Riga sul nuovo marcatore. |
| `tests/test_unit_handoff_check.py` | Fixture con un file motore; test R-135-1/2/4 e report che non contano. |
| `tests/test_unit_hooks.py` | Marcatore con hash vero; test B2-B6 (residuo, vuoto, non in stage, non tracciato, commit -a). |
| `.claude/agents/memoria_revisore.md` | Memoria delle review #136 e #137. |
| `reports/stato_progetto.md` | Voce della fetta; R-135-* chiuse; riserve R-136-*/R-137-*. |
| `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` | Report di fine task. |

La storia completa sta in git.
