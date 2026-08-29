# REPORT TASK — Chiusura riserve calcola(): tetto anti-DoS + test stringenti
**Data:** 2026-08-29
**Branch:** sonda/vps-stato-2026-08-26
**Review:** #94 — APPROVATO

---

## SCOPE ESEGUITO (5 punti)

### 1. Tetto anti-DoS in calcola(): FATTA

Tre strati indipendenti di difesa:

**Strato A — validazione AST (pre-eval, zero costo):**
- Esponente `**` deve essere un letterale `ast.Constant` ≤ `_CALCOLA_MAX_EXP` (1000).
  Cattura: `9**9**9` → outer `**` ha right=`BinOp` (non Constant) → RIFIUTATO in 0.000s.
- `math.factorial(n)` richiede arg letterale Constant ≤ `_CALCOLA_MAX_FACTORIAL` (1000).
  Cattura: `math.factorial(2**100)`, `math.factorial(9**3)` → arg non letterale → RIFIUTATO.
- `pow` rimosso da `_CALCOLA_BUILTIN_FUNCS` e dal namespace eval.
  Cattura: `pow(9, 387420489)` → "Rifiutato: funzione non permessa 'pow'".

**Strato B — namespace eval ripulito:** `__builtins__={}` + whitelist minimale (math, abs, round). `pow` non più presente.

**Strato C — check post-eval:** `len(str(result)) > _CALCOLA_MAX_DIGITS` (500) → RIFIUTATO.
  Cattura: risultati astronomici che passassero la validazione AST.

### 2. Whitelist nodi AST esplicitata in commento: FATTA

Aggiunto blocco commento sopra `_calcola_validate`:
```
# Whitelist nodi AST ammessi:
#   ast.Expression, ast.Constant (int/float),
#   ast.BinOp  (op in Add/Sub/Mult/Div/FloorDiv/Mod/Pow),
#   ast.UnaryOp (op in USub/UAdd),
#   ast.Call   (func validato da _calcola_validate_func),
#   ast.Attribute (solo math.<costante>),
#   ast.Name   (solo "math" o funzione builtin ammessa)
```

### 3. Test end-to-end LLM live: SALTATA — API key assenti

`python3 gas.py doctor` conferma: `GEMINI_API_KEY assente`, `GROQ_API_KEY assente`.
Il test "sette per otto → modello chiama calcola → 56" richiede un provider attivo.
Va eseguito al primo deploy su VPS S2. NON dichiarato passato.

### 4. Fix T62f — rifiuto stringente (R-calcola-2): FATTA

Condizione aggiornata da `_r.startswith("Rifiutato") or _r.startswith("Errore")` a
solo `_r.startswith("Rifiutato")`. Gli input malevoli producono ora SOLO "Rifiutato:"
(per nome non permesso, costrutto non permesso, ecc.) — mai "Errore di sintassi".
Aggiunto `pow(9, 387420489)` alla lista dei bad input.

### 5. Commit hash + conferma branch: FATTA

- **Commit motore #94:** `873220a`
- **Branch:** `sonda/vps-stato-2026-08-26`
  Motivazione branch: questo branch raccoglie l'intera sessione di sonda VPS 2026-08-26,
  che si è estesa su più giorni di lavoro (audit system-prompt, diagnosi bug, prompt
  hardening, calcola). Il nome è immutabile (branch già pushato con PR #77 aperta).

---

## TEST REALI ESEGUITI (zero simulazioni)

| Test | Input | Atteso | Esito |
|------|-------|--------|-------|
| T62f | `pow(9, 387420489)` | Rifiutato | ✅ PASS |
| T62l | `9**9**9` | Rifiutato, elapsed=0.000s | ✅ PASS |
| T62m | `2**1001` | Rifiutato (esponente > 1000) | ✅ PASS |
| T62n | `math.factorial(1001)` | Rifiutato (> limite) | ✅ PASS |
| T62o | `2**1000` | Valido (302 cifre ≤ 500) | ✅ PASS |
| T62p | `math.factorial(9**3)` | Rifiutato (arg non letterale) | ✅ PASS |
| T62k | `math.factorial(171)` | Numerico (310 cifre ≤ 500) | ✅ PASS |
| T62a-T62e | aritmetica base | Risultati corretti | ✅ PASS (tutti) |
| T62f (prev) | 6 exploit noti | Rifiutato (solo "Rifiutato:") | ✅ PASS |

**Suite completa: 299 PASS, 0 FAIL** (da 292 → +7 nuovi T62l-T62p + 1 T62f aggiornato).

---

## VERDETTO REVISORE #94

**APPROVATO**

Elementi verificati: difese anti-DoS su tre strati indipendenti (AST/namespace/post-eval) strutturalmente solide; T62f condizione stringente corretta; Wall of Shame §5 rispettato; nessun guardrail indebolito.

Riserva residua (da #93, non bloccante): R-calcola-1 coperta in ogni caso da `except Exception → stringa errore, zero crash`.

---

## NOTA ANOMALIA

Round-trip LLM live NON eseguibile in questo ambiente (API key assenti). Dichiarato
esplicitamente come richiesto. Da validare su VPS S2 al deploy.

## STOP GATE

Scope fisso rispettato: solo i 5 punti elencati. Nessun refactor aggiuntivo committato.
