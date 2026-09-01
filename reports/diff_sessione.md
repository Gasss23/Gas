# Diff sessione — 2026-09-01 (correzione reporting)

Sessione: `sonda/e2e-calcola-gemini-2026-09-01`
Scope: Correzione di reporting/memoria sul finding "kernel rifiuta 7×8". ZERO modifiche al motore.

## File toccati

| File | Cosa è cambiato e perché |
|---|---|
| `reports/stato_progetto.md` | Finding 7×8: stato corretto da ✅ CHIUSO a 🟡 VERIFICATO RISOLTO SU GEMINI con 3 caveat espliciti (causa radice non rimossa, Groq contraddittorio, attribuzione Groq-specifico non provata). Diagnosi storica mantenuta. |
| `reports/ultimo_report.md` | §5 ultima frase: rimosso "il finding era Groq-specifico" come fatto acquisito; sostituito con dichiarazione onesta dei 3 caveat. |
| `reports/handoff.md` | Rigenerato per coprire questa correzione. |
| `reports/diff_sessione.md` | Questo file — riscritto per la correzione di reporting. |

## Note

Zero modifiche a gas.py, brains/, modules/, tests/. Revisore non richiesto (nessun diff motore).
Task precedente sulla sessione (sonda E2E 2 PASS): invariato nel merito, solo il reporting era impreciso.
