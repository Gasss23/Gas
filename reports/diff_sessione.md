# Diff della sessione — 2026-10-28 (chat Motore, PR #287)

- `brains/claude_cli.py`: messaggio «`claude` non trovato» con il consiglio GAS_CLAUDE_BIN; nuovo caso PermissionError → «non eseguibile».
- `gas.py`: `_motivo_forte` (motivo vero del forte nella riga «Pipeline esausta»); `_claude_solo_nel_terminale` e nuovo WARN del doctor.
- `tests/test_unit_kernel.py`: T99s–T99v.
- `tests/test_unit_claude_cli.py`: caso PermissionError.
- `.claude/agents/memoria_revisore.md`: review #538 e #539 (chat Motore).
- `reports/stato_progetto.md`: «Ultimo aggiornamento» (unita con la voce Mani della #285), punto 3 della ripartenza Motore, riserve di revisore, bot e verifica esterna.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.
- Merge di origin/main (PR #285): porta `modules/web/lexbor.py`, `tests/test_unit_web_lexbor.py`, `reports/ripartenza_mani.md` identici a main (fuori dal diff della sessione rispetto alla base).

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
