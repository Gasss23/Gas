# DIFF SESSIONE — 2026-10-06 — fix/kernel-skip-senza-bwrap (F-mac-1)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `tests/test_unit_kernel.py` — helper `senza_sandbox_os_usa_fallback` su T11c2/T11d-e/T12; check T12-modo; check T13-atteso con `GAS_TEST_SANDBOX_OS_ATTESO=1`.
- `.github/workflows/ci.yml` — `GAS_TEST_SANDBOX_OS_ATTESO: "1"` nello step "Run unit suite".
- `reports/stato_progetto.md` — F-mac-1 CHIUSA, soluzione descritta.
- `.claude/agents/memoria_revisore.md` — righe #173 e #175.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
