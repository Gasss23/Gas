# Diff sessione — 2026-10-03 — Fix gate di review inerte (fix/gate-review-jq)

> Si riscrive a ogni sessione; la storia completa sta in git.

| File | Cosa è cambiato e perché |
|---|---|
| `.claude/hooks/review_gate.sh` | Parser jq corretto per l'input oggetto (prima andava in errore → exit 0, gate inerte); parse fallito → controllo "git commit" sul testo grezzo (fail-closed). |
| `tests/test_unit_hooks.py` | Nuovi T-gate-E..I con input oggetto; `_run` con parametro `stdin` opzionale. |
| `.claude/agents/memoria_revisore.md` | Riga #129 e lezione del revisore. |
| `reports/stato_progetto.md` | Stato della fetta, F-gate-inerte chiuso, riserve R-gjq-1..3. |
| `reports/ultimo_report.md` | Report del task. |
| `reports/handoff.md` | Dossier di fine sessione. |
| `reports/diff_sessione.md` | Questo file. |
