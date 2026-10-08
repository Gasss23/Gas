# DIFF SESSIONE — 2026-10-08 — fix/gate-compressione-contamina (R-203-1)

- `gas.py`: costanti `_RIEPILOGO_SOLO_INTERNO` / `_RIEPILOGO_INPUT_ESTERNO`; `_compress_history_if_needed` marca la prima riga del riepilogo; `_finestra_e_contaminata` considera contaminato un riepilogo non `[SOLO INTERNO]`. Perché: R-203-1, la compressione decontaminava la finestra.
- `tests/test_unit_kernel.py`: T72g (11 check). Kernel 699 PASS / 0 FAIL.
- `reports/design_cancello.md`: §3a, la compressione non decontamina.
- `.claude/agents/memoria_revisore.md`: righe #208, #209.
- `reports/`: stato_progetto (R-203-1 chiusa), ultimo_report, diff_sessione, handoff.
