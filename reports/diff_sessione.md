# DIFF SESSIONE — 2026-10-06 — fix/gate-ip-read-locale

> Si riscrive a ogni sessione; la storia completa sta in git.

- `scripts/gasmerge.sh` — `IFS= LC_ALL=C read` nel filtro loopback del gate IP e nel ciclo ENGINE_DIFF (R-167-1).
- `scripts/fine_task_finale.sh` — `IFS= LC_ALL=C read` nel filtro loopback del gate IP.
- `tests/test_unit_gasmerge.py` — `_locale_utf8()`, test byte attaccato all'IP in locale UTF-8, test path non UTF-8 nel promemoria.
- `tests/test_unit_hooks.py` — `_locale_utf8()`, test 4f-bis (byte attaccato all'IP in locale UTF-8).
- `reports/stato_progetto.md` — residuo latin1 CHIUSO, bug e R-167-x annotati.
- `.claude/agents/memoria_revisore.md` — righe #167 e #170.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
