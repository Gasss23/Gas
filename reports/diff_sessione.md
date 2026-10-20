# DIFF SESSIONE — 2026-10-20 (dopo #222: firma dopo lettura più stretta, `gas fida-contatto`)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/gate/gate.py` — `libero_dopo_lettura`: radice, cartelle di progetto e nomi di istruzioni per agenti alla firma (R-ve222-4, R-377-2).
- `modules/memory/store.py` — `togli_segno_non_fidato` (segno tolto + riga di diario nella stessa transazione, solo se il lead è identico alla scheda mostrata).
- `gas.py` — comando umano `fida-contatto`; tipi di diario delle azioni umane riservati al kernel (R-377-1).
- `tests/test_unit_gate.py`, `tests/test_unit_kernel.py` — casi nuovi e round-trip agentici.
- `.claude/agents/memoria_revisore.md` — righe #377–#379.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report.
