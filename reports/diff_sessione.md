# Diff sessione — 2026-09-21

## File toccati

| File | Delta | Perché |
|------|-------|--------|
| `gas.py` | +1 -1 | Regola di lingua rafforzata in `_GAS_SYSTEM_PROMPT_BASE` |
| `gas_identity.md` | +2 | Regola di lingua aggiunta in cima (posizione di massima priorità) |
| `tests/test_unit_kernel.py` | +37 | Test T63a/b/c/d verifica strutturale regola di lingua |

## Cosa è cambiato e perché

GAS rispondeva in inglese nel test vocale 4b. La regola di lingua era debole (solo "Rispondi sempre in italiano") e assente da `gas_identity.md` (che ha precedenza nel system prompt).

Soluzione minima: rafforzamento della frase con "dal primo messaggio, anche se l'utente scrive in un'altra lingua" in entrambi i file. Ridondanza difensiva intenzionale (approvata revisore #100).
