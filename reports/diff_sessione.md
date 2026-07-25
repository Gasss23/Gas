# Diff sessione — fix/gasmerge-failopen — 2026-07-25

> Riscritto a ogni sessione. La storia completa sta in git.

File toccati (da `git diff --stat BASE..HEAD`):

| File | Δ | Motivo |
|------|---|--------|
| `scripts/gasmerge.sh` | +65 -17 | Fix R-gasmerge-failopen fette 1-3: validazione arg, jq functional, GAS_REPO_DIR, fail-closed IP/diff, secondo fetch, TOCTOU --match-head-commit |
| `tests/test_unit_gasmerge.py` | +302 (nuovo) | 7 test per i 6 difetti chiusi; stubs gh+git, repo reali, verifica discriminazione old vs new |
| `reports/stato_progetto.md` | aggiornato | R-gasmerge-failopen da 🟡 a ✅ CHIUSO, 4 riserve, cambio superficie GAS_REPO_DIR |
| `reports/ultimo_report.md` | aggiornato | Report canonico del task |
| `reports/handoff.md` | aggiornato | Dossier di fine sessione |
| `reports/diff_sessione.md` | aggiornato (questo file) | Diff sessione |
| `.claude/agents/memoria_revisore.md` | +2 righe | Contatori review #62 e #63 aggiunti dal revisore |
