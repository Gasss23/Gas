# DIFF SESSIONE — 2026-09-30 (fix/diario-eco)

## File toccati

| File | Cosa è cambiato e perché |
|---|---|
| `gas.py` | Aggiunto `_esito_diario()`, reset+set `self._ricorda_n` in `_ricorda`, sostituzione `_esito_sintetico→_esito_diario` in `run_turn`. Fix F-diario-eco: diario non registra più testo non fidato. |
| `tests/test_unit_kernel.py` | Aggiunti test T70a–d per verificare che ricorda/read_file scrivano solo conteggi nel diario. |
| `reports/stato_progetto.md` | Aggiunto finding F-diario-eco (chiuso in avanti), aggiornata data. |
| `.claude/agents/memoria_revisore.md` | Riga #114 aggiunta dal revisore dopo review. |

## Nota

Questo file si riscrive a ogni sessione; la storia completa sta in git.
