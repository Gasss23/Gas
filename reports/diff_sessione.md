# DIFF SESSIONE — 2026-08-19 — fix/quotepath-non-ascii

File toccati in questa sessione (`git diff --stat BASE..HEAD`):

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `.claude/agents/memoria_revisore.md` | Aggiunta riga contatore #85 (APPROVATO) dopo review pre-commit del fix. |
| `reports/stato_progetto.md` | Aggiornato header + aggiunta entry fix core.quotePath (#85) + chiusura riserva #84. |
| `reports/ultimo_report.md` | Report di sessione: sonda, fix, test reali, verdetto #85 INTEGRALE, nota di processo R2-vaglio B2. |
| `scripts/check_handoff.py` | Fix bug: aggiunto `-c core.quotePath=false` a `_diff_names` (riga 48) — path non-ASCII quotati da git causavano falso mismatch. |
| `scripts/check_verdetto.py` | Fix bug: aggiunto `-c core.quotePath=false` a `_session_files` (riga 67) — stesso bug simmetrico. |
| `tests/test_unit_handoff_check.py` | 2 test reali aggiunti: `test_nonascii_filename_check_handoff` e `test_nonascii_filename_check_verdetto`. Repo git temporanei reali, verifica fallisce senza fix. |

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
