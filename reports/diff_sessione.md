# DIFF SESSIONE — 2026-10-21 (dopo il merge di #233: ripresa dei compiti dopo un crash, spesa incrementale)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/notte/notte.py` — registro `in_corso.json`, `_ordina_riprese`, NOTA_RIPRESA, exit 1 sul salto, potatura solo con catalogo letto bene; registro tolto prima della riflessione (`al_termine`).
- `gas.py` — `_daily_cost_usd` incrementale con `_COSTI_CACHE` e `_costo_riga`.
- `modules/gate/gate.py` — read_file nega un nome vuoto/root; docstring di `_normalize_path`.
- `tests/test_unit_kernel.py`, `tests/test_unit_notte.py`, `tests/test_unit_gate.py` — casi nuovi; test del lock con LOCK_SH.
- `.claude/agents/memoria_revisore.md` — righe #406-#411.
- `reports/da_mergiare.md`, `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report.
