# Diff sessione — 2026-09-21

## File toccati

| File | Delta | Perché |
|------|-------|--------|
| `.claude/agents/memoria_revisore.md` | +1 | Revisore #100: aggiunta riga memoria |
| `gas.py` | +1 -1 | Regola lingua rafforzata in `_GAS_SYSTEM_PROMPT_BASE` (gas.py:48) |
| `gas_identity.md` | +2 | Regola lingua aggiunta in cima (priorità massima nel system prompt) |
| `tests/test_unit_kernel.py` | +37 | Test T63a/b/c/d: verifica strutturale regola di lingua |
| `reports/stato_progetto.md` | +1 -1 | Item 5 aggiornato a ✅ COMPLETATO |
| `reports/ultimo_report.md` | riscritta | Report canonico del task |
| `reports/handoff.md` | riscritta | Dossier fine-sessione canonico |
| `reports/diff_sessione.md` | riscritta | Questo file |

## Cosa è cambiato e perché

GAS rispondeva in inglese nel test vocale 4b (PR #90). La regola di lingua nel system prompt era debole ("Rispondi sempre in italiano") e assente da `gas_identity.md` (che ha precedenza nel system prompt quando esiste). Soluzione minima: rafforzamento in entrambi i file con "dal primo messaggio, anche se l'utente scrive in un'altra lingua". Ridondanza difensiva approvata (revisore #100).

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
