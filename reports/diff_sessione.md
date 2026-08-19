# DIFF SESSIONE — 2026-08-19
## Fetta A + Fetta B — cd fail-closed test + core.quotePath non-ASCII

Questo file si riscrive a ogni sessione. Storia completa in git.

---

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `tests/test_unit_hooks.py` | Aggiunto `test_gate_e_cd_fails_blocks` (T-gate-E): copre il caso `cd "$CLAUDE_PROJECT_DIR"` fallisce (path inesistente → exit 2) in `review_gate.sh`. |
| `scripts/check_handoff.py` | `_diff_names()`: aggiunto `-c core.quotePath=false` alla chiamata `git diff --name-only` — path non-ASCII escono raw (UTF-8) invece di essere escapati tra virgolette. |
| `scripts/check_verdetto.py` | `_session_files()`: stesso fix `core.quotePath=false` per coerenza con `check_handoff.py`. |
| `tests/test_unit_handoff_check.py` | Aggiunta classe `TestNonAsciiPath` con `test_nonascii_filename_check_handoff`: repo git reale, file `répertoire_été.md`, verifica che `check_handoff.py` non rompa il set comparison. |
| `.claude/agents/memoria_revisore.md` | Aggiunte righe #83 (Fetta A, APPROVATO) e #84 (Fetta B, APPROVATO CON RISERVE). |
| `reports/stato_progetto.md` | Aggiornato header + entry per Fette A e B + riserva #84 nei finding aperti. |
| `reports/ultimo_report.md` | Report canonico di questa sessione. |
