# Report sonda E2E calcola() — Gemini brain
**Data:** 2026-08-29  
**Branch:** sonda/e2e-calcola-gemini-2026-08-29  
**Scope:** E2E comportamentale calcola() su provider Gemini (solo lettura — STOP GATE attivo)

---

## ESITO: PRECONDIZIONE MANCANTE — TEST NON ESEGUITI

### STOP GATE BLOCCANTE (istruzione operatore)

> "Precondizione: GEMINI_API_KEY presente in .env. Se assente → FERMATI e scrivilo nel report, NON committare codice."

**GEMINI_API_KEY è ASSENTE da `.env`.**

```
$ grep -q "GEMINI_API_KEY" .env && echo "PRESENTE" || echo "ASSENTE"
ASSENTE
```

I test E2E su Gemini **NON sono stati eseguiti**. Nessun codice toccato. Nessun fix proposto.

---

## Cosa è stato verificato (senza consumare token)

| Controllo | Esito |
|---|---|
| `.env` contiene `GEMINI_API_KEY` | ❌ ASSENTE |
| Test eseguiti | ❌ NESSUNO |
| Codice toccato | ✅ NESSUNO |
| Fix proposti | ✅ NESSUNO |

---

## Azione richiesta all'operatore

1. Aggiungere `GEMINI_API_KEY=<valore>` a `.env` sul WSL locale.
2. Ritriggerare la sonda (stessa specifica, stesso branch o nuovo).

---

## Contesto (dai report precedenti)

La sonda identica su **Groq brain** (branch `sonda/e2e-calcola-2026-08-29`, PR #78) ha prodotto:
- Test 1 "sette per otto" → calcola(`7*8`) → **56** — PASS
- Test 2 "radice quadrata di 144" → calcola(`math.sqrt(144)`) → **12.0** — PASS

La sonda Gemini è la naturale prosecuzione per validare il comportamento sul primo rung della pipeline. Bloccata dalla chiave mancante.
