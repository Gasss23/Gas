# DIFF SESSIONE — 2026-10-29 — Mani, fetta 27: selectolax in requirements

File toccati rispetto a main acd083f (PR #301 mergiata):
- `requirements.txt` — aggiunto `selectolax==1.0.2`, perché i test lexbor girino in CI e la libreria ci sia sul VPS (R-ve280-1). Lexbor resta spenta.
- `tests/test_unit_web_lexbor.py` — nuovo `test_selectolax_in_ci`, che in CI dà l'allarme se selectolax manca; docstring aggiornata.
- `.claude/agents/memoria_revisore.md` — riga della review #564 e una lezione sulle dipendenze native.
- `reports/stato_progetto.md` — blocco «Mani — fetta 27» e riga «Ultimo aggiornamento».
- `reports/ripartenza_mani.md` — punto b) fatto per la parte selectolax; nuovo punto g) con il lavoro passato da M1.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
