# DIFF SESSIONE — 2026-10-08 — FASE 4.5 fetta 1 (`gas notte`)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/notte/__init__.py`, `modules/notte/notte.py` — nuovo modulo: catalogo YAML fuori dalla root, giro dei compiti su kernel nuovi con cronologia propria, diario solo metadati, riepilogo, lock.
- `gas.py` — comando CLI `notte` (`notte_cmd`), unica modifica al kernel.
- `tests/test_unit_notte.py` — 20 test (round-trip agentico §7, isolamento, cancello, lock, catalogo).
- `.github/workflows/ci.yml` — passo CI per la nuova suite.
- `.gitignore` — `.gas_notte/` (file di runtime).
- `scripts/notte/com.gas.notte.plist`, `scripts/notte/catalogo_esempio.yaml` — timer launchd e catalogo di partenza per il Mac.
- `reports/setup_notte.md` — guida operatore (5 passi) e limiti dichiarati.
- `.claude/agents/memoria_revisore.md` — lezione della review #220.
- `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.
