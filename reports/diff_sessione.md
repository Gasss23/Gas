# Diff sessione — 2026-08-19
## Task: check_verdetto fail-closed + R-voice-3

> Questo file si riscrive a ogni sessione. La storia completa sta in git.

## File toccati

| File | Cosa è cambiato | Perché |
|---|---|---|
| `.claude/hooks/review_gate.sh` | `cd` failure → exit 2; `git diff` catturato fuori pipeline con `GIT_RC` esplicito → exit 2 se non-zero | Era fail-open: pipeline bash usava exit code di grep, non di git; cd fallito → exit 0 |
| `tests/test_unit_hooks.py` | Aggiunta classe `TestReviewGateFailClosed` con T-gate-A/B/C/D | Copertura del fix fail-closed con test reali su repo git temporanei |
| `tests/test_unit_voice_server.py` | Aggiunto `import http.client` + `test_invalid_content_length_returns_400` in `TestTVExtra` | R-voice-3: test mancante per Content-Length:abc→400 |
| `reports/stato_progetto.md` | Aggiornati contatori review (→81), suite (hook→14, voice→19), R-voice-3 chiusa, update header | Fine task |
| `reports/ultimo_report.md` | Riscritto con DECISIONI UMANE RICHIESTE, esiti fette, contatori | Fine task |
| `reports/handoff.md` | Riscritto con dossier sessione completo | Fine task |
| `reports/diff_sessione.md` | Questo file | Fine task |
