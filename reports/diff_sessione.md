# DIFF SESSIONE — 2026-10-20 (dopo #228: avviso sui file nuovi delicati, fonti solo dentro knowledge/)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/gate/gate.py` — `sembra_delicato` (solo per l'avviso, non decide il cancello).
- `gas.py` — file nuovi delicati raccolti nel turno, `_invia_avvisi_file` a fine turno.
- `tools/ingest_knowledge.py` — fonti di tipo file solo dentro `knowledge/`.
- `.github/workflows/ci.yml` — step per `tests/test_unit_ingest_fonti.py`.
- `tests/test_unit_kernel.py`, `tests/test_unit_gate.py`, `tests/test_unit_ingest_fonti.py` — test.
- `.claude/agents/memoria_revisore.md` — righe #386–#387.
- `reports/stato_progetto.md`, `reports/roadmap.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report.
