# DIFF SESSIONE — 2026-10-21 (dopo il merge di #236: ultime riserve del bot sulla storia condivisa)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py` — rinvio a fine turno in entrambi i rami di `_unisci_storia_altrui`; quinto elemento della base (`gia`) contro i duplicati dopo una scrittura fallita; `_save_history` restituisce se ha scritto; `compress_history_cmd` salva a fine operazione e dice ok solo se ha scritto.
- `tests/test_unit_kernel.py` — T97j (dal generatore di run_turn, messaggi inviati al provider), T97k (niente duplicati), T97l/T97l2 (compress-history); T97b e T97g con turni chiusi.
- `.claude/agents/memoria_revisore.md` — righe #438-#440.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md`, `reports/da_mergiare.md` — report.
