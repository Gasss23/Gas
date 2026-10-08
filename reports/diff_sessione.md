# DIFF SESSIONE — 2026-10-08 — FASE 4.5 fetta 1 (`gas notte`) + cancello

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/notte/__init__.py`, `modules/notte/notte.py` — nuovo modulo: catalogo YAML fuori dalla root, giro dei compiti su kernel nuovi con cronologia propria, diario solo metadati, riepilogo con conteggio azioni negate/in attesa, tetto di spesa di default, lock.
- `modules/gate/gate.py` — write_file negato sulla catena di avvio eseguita fuori sandbox (venv, .git, .gas_notte, file di codice/shell, scripts/, CLAUDE.md, .mcp, gas_identity, requirements).
- `gas.py` — comando CLI `notte` (`notte_cmd`).
- `tests/test_unit_notte.py`, `tests/test_unit_gate.py` — test delle due parti.
- `.github/workflows/ci.yml` — passo CI per la suite notte.
- `.gitignore` — `.gas_notte/`.
- `scripts/notte/com.gas.notte.plist`, `scripts/notte/catalogo_esempio.yaml` — timer launchd e catalogo per il Mac.
- `reports/setup_notte.md` — guida operatore (catalogo, tetto di spesa, timer).
- `.claude/agents/memoria_revisore.md` — lezioni review #220–#223.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
