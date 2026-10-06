# DIFF SESSIONE — 2026-10-06 — fix/gate-ip-read-locale

> Si riscrive a ogni sessione; la storia completa sta in git.

- `scripts/gasmerge.sh` — `IFS= LC_ALL=C read` nel filtro loopback del gate IP e nel ciclo ENGINE_DIFF (R-167-1).
- `scripts/fine_task_finale.sh` — `IFS= LC_ALL=C read` nel filtro loopback del gate IP.
- `tests/test_unit_gasmerge.py` — `_locale_utf8()`, test byte attaccato all'IP in locale UTF-8, test path non UTF-8 nel promemoria.
- `tests/test_unit_hooks.py` — `_locale_utf8()`, test 4f-bis (byte attaccato all'IP in locale UTF-8).
- `.claude/hooks/review_gate.sh` — `IFS= LC_ALL=C read` nella lettura del perimetro (V-2 #134).
- `scripts/check_verdetto.py` — perimetro non UTF-8 (file o BASE) → None fail-closed (R-177-1/R-178-1).
- `.github/workflows/ci.yml` — `GAS_TEST_LOCALE_UTF8_ATTESO: "1"` nel job unit-suite (V-3 #134).
- `tests/test_unit_handoff_check.py` — test R-177-1 e R-178-1.
- `reports/stato_progetto.md` — residuo latin1 CHIUSO, bug e R-167-x annotati.
- `.claude/agents/memoria_revisore.md` — righe #167 e #170.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
