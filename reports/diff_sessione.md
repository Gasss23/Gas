# Diff della sessione — 2026-11-02 — Cervello forte non-bare (chat M2)

- `brains/claude_cli.py` — docstring sul futuro default `--bare`; nuova `stato_abbonamento()` per il doctor.
- `gas.py` — 3 righe nel doctor: riga «Cervello forte · login» (autorizzate da M1).
- `tests/test_unit_claude_cli.py` — figlio senza chiavi API né modalità bare; casi di `stato_abbonamento`.
- `tests/test_unit_dotenv.py` — doctor con CLI finta: riga «login» OK/WARN con la versione.
- `tests/test_unit_kernel.py` — la suite non lancia mai il `claude` vero dal doctor (finto in `_doc99`, interruttore tolto in testa).
- `.claude/agents/memoria_revisore.md` — review #632–#636-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
