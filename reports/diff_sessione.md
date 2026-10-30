# DIFF SESSIONE — 2026-10-29 (chat M1: ponte voce → sviluppo, PR #307)

- `modules/sviluppo/__init__.py`, `modules/sviluppo/richieste.py`: nuovo modulo del ponte (issue in repo privato, token dedicato, tetto, niente redirect).
- `gas.py`: strumento `richiedi_sviluppo` (schema + dispatch); prompt di riserva con 12 strumenti.
- `modules/gate/gate.py`: `richiedi_sviluppo` UNCERTAIN.
- `gas_identity.md`: 12 strumenti, riga del nuovo strumento.
- `tests/test_unit_richieste.py` (nuovo), `tests/test_unit_kernel.py` (T100a/T100b), `.github/workflows/ci.yml` (step richieste), `.gitignore` (conto).
- `modules/gate/gate.py`, `gas.py`: `.gas_richieste_uso` protetto come `.gas_claude_cli_uso` (V-1 bot #307); `tests/test_unit_gate.py` e T68s.
- `.claude/agents/memoria_revisore.md`: righe #557-M1, #558-M1 e #559-M1.
- `reports/stato_progetto.md`: blocco «COORDINAMENTO DELLE CHAT» e «Ultimo aggiornamento»; `reports/roadmap.md`: voce «Ponte» (strada A).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
