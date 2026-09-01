# Diff sessione — 2026-09-01

**Branch**: fix/chiusura-f1-calcola-2026-09-01  
**Tipo sessione**: certificazione/verifica (zero modifiche al motore)

## File toccati

| File | Tipo modifica | Perché |
|------|---------------|--------|
| `reports/stato_progetto.md` | Aggiornamento | Chiusura finding F1 + caveats (i)/(ii)/(iii); aggiornamento header |
| `reports/ultimo_report.md` | Riscritto | Report di sessione |
| `reports/diff_sessione.md` | Riscritto | Questo file |
| `reports/handoff.md` | Riscritto | Handoff sessione |
| `.claude/agents/memoria_revisore.md` | Aggiornato dal revisore | Lezione review #95 (attestativa) |

## Cosa non è cambiato

- `gas.py` — ZERO modifiche (diff vuoto vs main). Il fix della direttiva calcola() era già in place dal commit `62af5ee` (review #93, 2026-08-29).
- `SHELL_ALLOWLIST` — invariata (verificata dal revisore: nessun calcolatore).
- Suite: 299 PASS, 0 FAIL (invariata rispetto alla sessione precedente).

## Cosa è cambiato concettualmente

Il finding F1 CRITICO (system prompt che ordinava `run_command` per tutti i calcoli, rendendo impossibile l'esecuzione dato che SHELL_ALLOWLIST non contiene calcolatori) è passato da **APERTO** a **CHIUSO**. La chiusura è stata possibile dopo aver:

1. Verificato che il fix era già in `gas.py:49-50` (commit `62af5ee`)
2. Eseguito sonda E2E reale su Gemini e Groq con history temporanea isolata → 4 PASS su 4
3. Riconciliato la contraddizione CAVEAT (ii) (Groq "rifiuta" vs "2 PASS"): i due test usavano system prompt diversi (vecchio vs nuovo)
4. Ottenuto APPROVATO dal revisore (review #95 attestativa)
