# REPORT — Sonda E2E calcola() comportamentale

**Data:** 2026-08-29
**Branch:** sonda/e2e-calcola-2026-08-29
**Tipo task:** Sonda / prova comportamentale (nessuna modifica al motore)
**Stop gate:** rispettato — 0 righe di codice motore toccate.
**Review revisore:** non richiesta (nessun diff motore).

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR su `sonda/e2e-calcola-2026-08-29` → main (vedi §0 handoff).
2. (Opzionale) Se si vuole isolare il bug 7×8 su Gemini: occorre `GEMINI_API_KEY` nel `.env` e un test mirato. Decisione all'operatore.

---

## Scope

### Fetta 1 — Verifica precondizioni
`FATTA` — revisore presente, `GROQ_API_KEY` disponibile in `.env`, kernel importabile.

### Fetta 2 — Test E2E "sette per otto"
`FATTA` — `calcola({"expr":"7*8"})` → `56`. PASS.

### Fetta 3 — Test E2E "radice quadrata di 144"
`FATTA` — `calcola({"expr":"math.sqrt(144)"})` → `12.0`. PASS.

### Fetta 4 — Analisi comportamentale e report
`FATTA` — nessun fix necessario. Stop gate rispettato.

---

## Risultati

### TEST 1 — "sette per otto"

```
INPUT: 'sette per otto'
[TOOL RESULT] '56'
[FINAL] '56'
[TOOL CHIAMATO] calcola  args={"expr":"7*8"}
```

- Tool invocato: **`calcola`** ✅
- Argomento: `{"expr":"7*8"}` ✅
- Risultato: `'56'` ✅
- Risposta finale: `'56'` ✅
- **PASS**

### TEST 2 — "radice quadrata di 144"

```
INPUT: 'radice quadrata di 144'
[TOOL RESULT] '12.0'
[FINAL] '12.0'
[TOOL CHIAMATO] calcola  args={"expr":"math.sqrt(144)"}
```

- Tool invocato: **`calcola`** ✅
- Argomento: `{"expr":"math.sqrt(144)"}` ✅
- Risultato: `'12.0'` (float Python — corretto) ✅
- Risposta finale: `'12.0'` ✅
- **PASS**

---

## Sintesi comportamentale

| Domanda | Risposta |
|---------|----------|
| Il modello ha invocato `calcola`? | **Sì, in entrambi i casi** |
| Con argomenti corretti? | **Sì** (`7*8` e `math.sqrt(144)`) |
| La risposta finale è corretta? | **Sì** (`56` e `12.0`) |
| L'instradamento è sistematico? | **Sì** — moltiplicazione + radice, entrambi via `calcola` |
| Fix applicati? | **Nessuno** — stop gate rispettato |

---

## Anomalie riscontrate

**Il kernel non carica `.env` automaticamente**: legge solo `os.environ`. Per eseguire test manuali in subprocess Python serve `set -a && source .env && set +a` prima di invocare Python. Senza questo, la pipeline risulta esausta (nessun provider trova la chiave). Non è un bug — è comportamento intenzionale — ma vale la pena documentarlo per i prossimi test manuali.

**`GEMINI_API_KEY` assente**: il test è stato eseguito solo su Groq. Il bug 7×8 (se legato a Gemini in certi contesti) non è stato investigato.

---

## Bug 7×8 — stato

Non riproducibile con Groq. Il kernel, con la pipeline corrente, chiama correttamente `calcola`. Se il bug era legato a Gemini, rimane non investigato (manca la chiave).
