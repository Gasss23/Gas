# Diff della sessione — 2026-11-06 — Fetta 3 sottofondo (chat M2)

- `modules/sottofondo/__init__.py` (nuovo) — coda privata, un compito alla volta (posto preso con tmp+`os.link`), avvio del processo separato, esecuzione col forte, avviso Telegram (anche su eccezione), durata massima con killpg solo se il processo è nostro, `notifica_possibile`; fail-safe §9.
- `gas.py` — `STRUMENTO_SOTTOFONDO` (solo turni parlati non effimeri), `_in_sottofondo` (forte, tetto, firma, diniego se l'avviso non è possibile), comando `sottofondo <id>`.
- `modules/gate/gate.py` — `in_sottofondo` UNCERTAIN.
- `.claude/agents/memoria_revisore.md` — lezioni review #695–#699.
- `.github/workflows/ci.yml` — passo «Run sottofondo suite».
- `.gitignore` — `.gas_sottofondo/`.
- `tests/test_unit_sottofondo.py` (nuovo), `tests/test_unit_kernel.py` (T105).
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
