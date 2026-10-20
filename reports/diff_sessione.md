# DIFF SESSIONE — 2026-10-20 (documenti, firma notturna, autonomia)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `CLAUDE.md`, `README.md`, `gas_identity.md`, `.claude/commands/fine-task.md` — allineati alle decisioni del 19 ottobre.
- `modules/memory/store.py`, `modules/memory/__init__.py`, `gas.py`, `modules/notte/notte.py` — scadenza delle firme notturne a 24 h.
- `modules/gate/gate.py`, `gas.py` — `libero_dopo_lettura`: autonomia dopo una lettura (solo documenti md/txt/csv); contaminazione dalla memoria (`non_fidato`, «[NON FIDATO]», segno di sessione, campi del pin su una riga).
- `modules/memory/store.py` — colonna `contatti.non_fidato`, `marca_contatto_non_fidato`.
- `tests/test_unit_kernel.py`, `tests/test_unit_gate.py`, `tests/test_unit_notte.py` — test nuovi e test del cancello spostati su `reports/`.
- `reports/roadmap.md`, `reports/stato_progetto.md`, `reports/setup_notte.md`, `reports/design_cancello.md` — documenti; `reports/roadmap_sintesi.md` tolto.
- `.claude/agents/memoria_revisore.md` — righe #364–#376.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
