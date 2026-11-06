# Diff della sessione — 2026-11-06 — Fetta 3 sottofondo (chat M2)

- `modules/sottofondo/__init__.py` (nuovo) — coda privata, un compito alla volta, avvio del processo separato, esecuzione col forte, avviso Telegram, annullamento; fail-safe §9.
- `gas.py` — `STRUMENTO_SOTTOFONDO` (solo turni parlati non effimeri), `_in_sottofondo` (forte, tetto, firma), comando `sottofondo <id>`.
- `modules/gate/gate.py` — `in_sottofondo` UNCERTAIN.
- `.github/workflows/ci.yml` — passo «Run sottofondo suite».
- `.gitignore` — `.gas_sottofondo/`.
- `tests/test_unit_sottofondo.py` (nuovo), `tests/test_unit_kernel.py` (T105).
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
