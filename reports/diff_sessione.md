# Diff sessione — 2026-09-01

**Branch**: fix/chiusura-f1-calcola-2026-09-01  
**Tipo sessione**: certificazione/verifica (zero modifiche al motore)

## File toccati in questa sessione

| File | Modifica | Perché |
|------|----------|--------|
| `.claude/agents/memoria_revisore.md` | +1 riga | Revisore aggiunge lezione review #95 (attestativa) |
| `reports/stato_progetto.md` | aggiornato | Chiusura finding F1 + caveats (i)/(ii)/(iii); aggiornamento header sessione |
| `reports/ultimo_report.md` | riscritto | Report di sessione: sonda E2E, esiti fette, conclusioni |
| `reports/diff_sessione.md` | riscritto | Questo file |
| `reports/handoff.md` | riscritto | Handoff sessione completo con verdetto revisore #95 |

## Cosa NON è cambiato

- `gas.py` — ZERO modifiche. `git diff main HEAD -- gas.py` = vuoto.
- `SHELL_ALLOWLIST` — invariata (nessun calcolatore).
- Suite tests: 299 PASS, 0 FAIL (invariata).

## Cosa è cambiato concettualmente

Finding F1 CRITICO passato da **APERTO** a **CHIUSO**. Il fix della direttiva calcola() era già in `gas.py:49-50` dal commit `62af5ee` (review #93, 2026-08-29). Questa sessione ha:
1. Verificato il fix presente nel codice
2. Eseguito sonda E2E reale su Gemini e Groq — 4 PASS su 4
3. Riconciliato la contraddizione CAVEAT (ii) (Groq "rifiuta" vs "2 PASS": i due test usavano system prompt diversi)
4. Ottenuto APPROVATO dal revisore (review #95 attestativa)
5. Chiuso il finding e i tre caveats in stato_progetto.md
