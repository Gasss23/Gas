# DIFF SESSIONE — 2026-09-12
**Branch:** recon/hook-audit-2026-09-12
**Nota:** questo file si riscrive a ogni sessione. La storia completa sta in git.

## File toccati in questa sessione

Da `git diff --stat c237d08..HEAD`:

| File | Cosa è cambiato e perché |
|---|---|
| `.claude/agents/memoria_revisore.md` | Aggiornata dal subagent revisore dopo le due review (commit c258e8f, c3c90c7). |
| `.claude/commands/fine-task.md` | Aggiunto passo 4ter (check_landing) dopo §4bis push e prima di §5. |
| `.claude/hooks/promemoria_end.sh` | Nuovo hook Stop soft: avvisa su stderr se ci sono commit di sessione senza handoff aggiornato. |
| `.claude/settings.json` | Aggiunta seconda entry Stop array (index [1]) per promemoria_end.sh. |
| `reports/diff_sessione.md` | Questo file. |
| `reports/handoff.md` | Dossier fine sessione — fette FEATURE 1 + FEATURE 2. |
| `reports/stato_progetto.md` | Aggiornato header data sessione. |
| `reports/ultima_risposta.md` | Salvata dall'hook scrivi_rep. |
| `reports/ultimo_report.md` | Riscritto con esito implementazione FETTA 1 + FETTA 2. |
| `scripts/check_landing.sh` | Nuovo script pre-merge: Check A (file), B (HEAD pushato), C (PR aperta). |
| `tests/test_unit_hooks.py` | Aggiunti T-prom-1..5 (promemoria_end.sh) e T-land-1..6 (check_landing.sh), costante PROMEMORIA_HOOK, helper _make_git_commit/_init_bare_origin/_run_promemoria/_run_check_landing/_write_required_files/_setup_repo_with_origin_and_files/_make_fake_gh. |
