# Diff della sessione — 2026-11-06 — Rifiuto di --effort + proposta fetta 3 (chat M2)

- `brains/claude_cli.py` — `_RIFIUTO_EFFORT`: il ripiego senza `--effort` scatta solo con «unknown/unrecognized option|argument --effort» su stderr (non più con «invalid» o su stdout); regex lineare.
- `tests/test_unit_claude_cli.py` — casi veri e falsi positivi, tempo lineare, `finally` sul flag.
- `reports/proposta_fetta3_sottofondo.md` — proposta tecnica dei compiti lunghi in sottofondo (solo documento).
- `.claude/agents/memoria_revisore.md` — review #693-M2, #694-M2.
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
