# Report sonda E2E calcola() — brain Gemini (run 2)

**Data**: 2026-09-01  
**Branch**: `sonda/e2e-calcola-gemini-2026-09-01`  
**Scope**: Sonda comportamentale E2E read-only di `calcola()` su provider Gemini. Seconda run (re-esecuzione fresh). Zero modifiche al motore.

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

Nota: il kernel NON carica `.env` autonomamente — source eseguito prima dell'import (`set -a && source .env && set +a`).

---

## §2 OUTPUT TERMINALE REALE (run fresca 2026-09-01T17:32)

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

## §3 VERIFICA TOOL CALL (da `.gas_history.json`)

```
[user] 'sette per otto'
[assistant] tool_calls: {"name": "calcola", "arguments": "{\"expr\":\"7*8\"}"}
[tool] '56'
[assistant] '56'
[user] 'radice quadrata di 144'
[assistant] tool_calls: {"name": "calcola", "arguments": "{\"expr\":\"math.sqrt(144)\"}"}
[tool] '12.0'
[assistant] '12.0'
```

→ Gemini ha invocato `calcola(expr="7*8")` → `56` e `calcola(expr="math.sqrt(144)")` → `12.0`.
→ Tool call reale verificata — zero simulazione.

---

## §4 MODELLO USATO

Dal log `.gas_tokens.jsonl` (17:32:05):
```
provider: gemini-flash-lite | model: gemini-2.5-flash-lite
```
Rung 1 della cascata.

---

## §5 ESITO SONDA

| Test | Input | Tool chiamato | Args | Output | Esito |
|---|---|---|---|---|---|
| T1 | "sette per otto" | `calcola` | `expr="7*8"` | `56` | ✅ PASS |
| T2 | "radice quadrata di 144" | `calcola` | `expr="math.sqrt(144)"` | `12.0` | ✅ PASS |

**ESITO GLOBALE: ✅ TUTTI PASS**

Il finding "kernel rifiuta 7×8" era Groq-specifico. Gemini segue correttamente il system prompt e invoca `calcola()`. Nessun fix necessario. Zero codice toccato.
