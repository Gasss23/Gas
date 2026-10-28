# Diff della sessione — 2026-10-28 (chat Motore, PR #291)

- `gas.py`: `_DOTENV_CARICATE` riempito da `_carica_dotenv`; `_motivo_forte` senza prefisso doppio e tetto 240; `_avviso_claude_timer` (sostituisce `_claude_solo_nel_terminale`) e messaggio del doctor; `import sys`.
- `tests/test_unit_kernel.py`: T99s (WARN con GAS_CLAUDE_BIN dalla shell), T99t (casi nuovi: relativo, venv, symlink, Linux), T99u e T99v aggiornati.
- `tests/test_unit_dotenv.py`: test che collega `_carica_dotenv` a `_DOTENV_CARICATE` (R-540-1).
- `.claude/agents/memoria_revisore.md`: review #540 e #541.
- `reports/stato_progetto.md`: «Ultimo aggiornamento» e punto 3 della ripartenza Motore (note chiuse, R-540-3 e R-541-1 aperte).
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

- Merge di origin/main (PR #289, solo documenti): conflitti nei report risolti, nessun file nuovo nel diff della sessione.
- `.claude/agents/memoria_revisore.md`: anche review #542.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
