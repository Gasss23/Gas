# Report sonda E2E calcola() — brain Gemini

**Data**: 2026-09-01  
**Branch**: `sonda/e2e-calcola-gemini-2026-09-01`  
**Scope**: Sonda comportamentale E2E read-only di `calcola()` su provider Gemini. Zero modifiche al motore.

---

## §0 DECISIONI UMANE RICHIESTE

Nessuna. La sonda è read-only; entrambi i test sono PASS. Nessun fix proposto, nessuna azione bloccante.

---

## §1 PRECONDIZIONI

| Check | Esito |
|---|---|
| `GEMINI_API_KEY` in `.env` | ✅ PRESENTE (lunghezza 53) |
| Kernel importabile (con venv) | ✅ OK |
| Brain Gemini attivabile | ✅ `gemini-2.5-flash-lite` (rung 1) |

Nota: il kernel NON carica `.env` autonomamente — il source è stato eseguito prima dell'import (`set -a && source .env && set +a`).

---

## §2 OUTPUT TERMINALE REALE

```
=== SONDA E2E calcola() — brain Gemini ===
GEMINI_API_KEY caricata: True

============================================================
TEST: sette per otto → 56
INPUT: 'sette per otto'
ATTESA (substr): '56'
------------------------------------------------------------
[tool_res] '56'
[final]    '56'

Tool calls eseguiti: 1
ESITO: ✅ PASS

============================================================
TEST: radice quadrata di 144 → 12.0
INPUT: 'radice quadrata di 144'
ATTESA (substr): '12.0'
------------------------------------------------------------
[tool_res] '12.0'
[final]    '12.0'

Tool calls eseguiti: 1
ESITO: ✅ PASS

============================================================
RIEPILOGO FINALE
============================================================
✅ PASS — sette per otto → 56
✅ PASS — radice quadrata di 144 → 12.0

ESOTO GLOBALE: ✅ TUTTI PASS
```

---

## §3 VERIFICA TOOL CALL (history)

Dump delle ultime 4 voci di `.gas_history.json` per ciascun test, lette dopo l'esecuzione:

### Test 1 — sette per otto

```
[user] 'sette per otto'
[assistant] tool_calls: [{"id": "function-call-6719629399272158516", "type": "function",
  "function": {"name": "calcola", "arguments": "{\"expr\":\"7*8\"}"}}]
[tool] '56'
[assistant] '56'
```

→ Gemini ha invocato `calcola(expr="7*8")` → risultato `56` → risposta finale `'56'`.

### Test 2 — radice quadrata di 144

```
[user] 'radice quadrata di 144'
[assistant] tool_calls: [{"id": "function-call-17112663409496165998", "type": "function",
  "function": {"name": "calcola", "arguments": "{\"expr\":\"math.sqrt(144)\"}"}}]
[tool] '12.0'
[assistant] '12.0'
```

→ Gemini ha invocato `calcola(expr="math.sqrt(144)")` → risultato `12.0` → risposta finale `'12.0'`.

---

## §4 MODELLO USATO

Dal log `.gas_tokens.jsonl`:

```
provider: gemini-flash-lite | model: gemini-2.5-flash-lite
```

Rung 1 della cascata — il primo provider disponibile con `GEMINI_API_KEY` presente.

---

## §5 CONFRONTO CON SONDA PRECEDENTE (Groq, 2026-08-29)

La sonda del 2026-08-29 su brain Groq aveva prodotto FAIL: il kernel non invocava `calcola`, rispondeva con testo "Non ho a disposizione..." (finding aperto: "🟡 kernel rifiuta 7×8 — DIAGNOSTICATO").

Con Gemini:
- **Comportamento CORRETTO**: Gemini segue il system prompt (`gas.py:49-50`) e invoca `calcola()` per entrambe le domande aritmetiche.
- Il finding "kernel rifiuta 7×8" è **Groq-specifico**, non un bug del sistema. Gemini rispetta le istruzioni correttamente.

---

## §6 ESITO SONDA

| Test | Input | Tool chiamato | Args | Output | Esito |
|---|---|---|---|---|---|
| T1 | "sette per otto" | `calcola` | `expr="7*8"` | `56` | ✅ PASS |
| T2 | "radice quadrata di 144" | `calcola` | `expr="math.sqrt(144)"` | `12.0` | ✅ PASS |

**ESITO GLOBALE: ✅ TUTTI PASS**

Nessun fix necessario. Zero codice toccato.
