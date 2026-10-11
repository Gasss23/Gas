# Diff della sessione — 2026-10-11 — strumenti nativi di sola lettura (PR #184)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `gas.py` — 5 tool nativi (`elenca_cartella`, `leggi_righe`, `cerca_testo`, `conta_file`, `data_ora`), controllo unico `_risolvi_lettura` (usato anche da read_file), tetti `GAS_LETTURA_MAX_*`, diario a soli conteggi, prompt di sistema e messaggio di troncamento aggiornati.
- `modules/gate/gate.py` — i 5 tool SAFE; i 4 di lettura in `UNTRUSTED_INPUT_TOOLS`; stesso controllo per nome di read_file (`TOOL_LETTURA_PERCORSO`).
- `gas_identity.md` — elenco dei 12 tool.
- `tests/test_unit_kernel.py` — T84 (round-trip, percorsi vietati, link, tetti, profondità dichiarata, nomi con a-capo, binari, FIFO, R-277-1).
- `.claude/agents/memoria_revisore.md` — righe review #282–#285.
- `reports/stato_progetto.md` — PR #184 e riserve R-283-x.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
