# DIFF SESSIONE — 2026-10-07 — fix/gate-run-command-untrusted (R-200-2)

- `modules/gate/gate.py`: `run_command` in `UNTRUSTED_INPUT_TOOLS`. Perché: R-200-2, dopo un output di run_command i tool UNCERTAIN non andavano in approvazione.
- `tests/test_unit_kernel.py`: T72d, T72e, T72f (round-trip os_strict con controprova), T78e invertito. Kernel 658 PASS / 0 FAIL.
- `.claude/agents/memoria_revisore.md`: riga #203.
- `reports/`: stato_progetto (R-200-2 chiusa, R-203-1/2), ultimo_report, diff_sessione, handoff.
