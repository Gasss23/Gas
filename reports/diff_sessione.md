# Diff sessione — fix/handoff-check-ci (2026-07-25)

> Riscritto a ogni sessione. La storia completa sta in git.

File toccati (da `git diff --stat BASE..HEAD` dove BASE = de2f2f5):

- `.claude/agents/memoria_revisore.md` — aggiornato dal revisore con lezioni della review
- `.claude/commands/fine-task.md` — regola §0 PR aperta; vincoli §2 verificati CI; allowlist
- `.github/workflows/ci.yml` — aggiunto job handoff-check (separato da unit-suite)
- `reports/diff_sessione.md` — questo file (riscritto per la sessione)
- `reports/handoff.md` — dossier di fine sessione (riscritto)
- `reports/ultimo_report.md` — report di fine task (riscritto)
- `scripts/check_handoff.py` — nuovo: verifica SET file §2 vs diff reale; allowlist
- `scripts/check_verdetto.py` — nuovo + fix R1: verifica path:riga §4; filtro _VALID_EXTENSIONS
- `tests/test_unit_handoff_check.py` — nuovo: 9 test pytest con repo git temporanei reali

Nota: questa sessione NON tocca gas.py, brains/, modules/.
Fix R1 (regex falsi positivi su URL) applicato nella stessa sessione.
