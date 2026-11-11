# Diff di sessione — 2026-11-11 — Audit dell'11 novembre (chat M3)

File toccati (da `git diff --stat BASE..HEAD`, BASE = merge-base con origin/main):
- `scripts/gasmerge.sh` — ripiego senza `timeout` (gtimeout, poi perl padre che uccide il figlio).
- `scripts/bot_esito.py` — `tocca_macchina_bot` senza maiuscole.
- `scripts/check_verdetto.py` — `_nel_perimetro` senza maiuscole.
- `.claude/hooks/review_gate.sh` — perimetro senza maiuscole (grep -i, pathspec icase).
- `.github/workflows/ci.yml` — `permissions: contents: read`.
- `modules/sottofondo/__init__.py` — `ferma()` fuori dalla cartella di Gas: errore che dice dove lanciarlo.
- `tests/test_unit_gasmerge.py`, `tests/test_unit_verifica_bot.py`, `tests/test_unit_handoff_check.py`, `tests/test_unit_hooks.py`, `tests/test_unit_sottofondo.py` — test delle correzioni.
- `.claude/agents/memoria_revisore.md` — righe #766-M1, #767-M1.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
