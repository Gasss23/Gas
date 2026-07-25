# Diff sessione — fix/handoff-check-ci (2026-07-25)

> Riscritto a ogni sessione. La storia completa sta in git.

File toccati (da `git diff --stat de2f2f5..HEAD`):

- `.claude/agents/memoria_revisore.md` — aggiornato dal revisore con lezioni della review
- `.claude/commands/fine-task.md` — regola §0 PR aperta; vincoli §2 verificati CI; allowlist documentata
- `.github/workflows/ci.yml` — aggiunto job handoff-check (separato da unit-suite)
- `scripts/check_handoff.py` — nuovo: verifica SET file §2 vs diff reale; allowlist ultima_risposta.md
- `scripts/check_verdetto.py` — nuovo: verifica riferimenti path:riga §4; dichiara MITIGATO
- `tests/test_unit_handoff_check.py` — nuovo: 9 test pytest con repo git temporanei reali

Nota: questa sessione NON tocca gas.py, brains/, modules/.
