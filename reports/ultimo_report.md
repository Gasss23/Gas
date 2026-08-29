# REPORT TASK — Fetta A + Fetta B: Prompt hardening + tool calcola()
**Data:** 2026-08-29
**Branch:** sonda/vps-stato-2026-08-26
**Review:** #93 — APPROVATO CON RISERVE

---

## SCOPE ESEGUITO

### Fetta A — Prompt hardening (gas.py + gas_identity.md)

**#1a** — Direttiva run_command ristretta: ora punta SOLO a conteggi/misure su file.
Per i calcoli aritmetici la regola rimanda esplicitamente a `calcola()`.

**#2 + #3** — Tutti e 7 i tool nativi elencati esplicitamente in `_GAS_SYSTEM_PROMPT_BASE`
(lista: `read_file, write_file, run_command, calcola, ricorda, salva_contatto, imposta_stato_contatto`)
e in `gas_identity.md` (sezione tool con bullet list e descrizione per ciascuno).

**#4** — Regola di fallback universale aggiunta: se un tool fallisce o viene negato,
il modello DEVE dichiararlo esplicitamente. Zero simulazione di output, qualunque sia il contesto.

**#5** — Persona unificata: rimossa la self-intro duplicata da `_GAS_SYSTEM_PROMPT_BASE`.
Quando `gas_identity.md` è presente → `_build_system_prompt` restituisce identity + regole (un'unica intro).
Quando assente → fallback minimo `"Sei Gas..."` + regole.

**#6** — Finding echo non toccato (innocuo, come da scope operatore).

### Fetta B — Tool calcola()

Nuovo tool deterministico aritmetico: `_calcola(expr)` + `_calcola_validate()` + `_calcola_validate_func()`.

**Implementazione:**
- Parser AST (`ast.parse` mode=`"eval"`) + validazione ricorsiva whitelist
- Operatori permessi: `+ - * / // % **`
- Funzioni permesse: `abs`, `round`, `pow` (builtin); `math.sqrt/floor/ceil/log/log2/log10/sin/cos/tan/fabs/factorial`
- Costanti permesse: `math.pi`, `math.e`, `math.tau`, `math.inf`
- `eval` con `__builtins__={}` e namespace minimale — ZERO accesso a shell/file
- Rifiuto esplicito di tutto ciò che non è pura aritmetica (nomi non in whitelist, lambda, listcomp, import, call non permesse)

**Schema + dispatch:**
- Aggiunto a `tools_schema` con description e parametro `expr` (required)
- Dispatch in `execute_tool_call`: `elif name == "calcola": out = _calcola(expr)`

---

## TEST REALI ESEGUITI (zero simulazioni)

| Test | Input | Atteso | Esito |
|------|-------|--------|-------|
| T62a | `7*8` | `'56'` | ✅ PASS |
| T62b | `math.sqrt(144)` | `'12.0'` | ✅ PASS |
| T62c | `(3+5)*2` | `'16'` | ✅ PASS |
| T62d | `10//3` | `'3'` | ✅ PASS |
| T62e | `2**10` | `'1024'` | ✅ PASS |
| T62f | `__import__('os')` | Rifiutato | ✅ PASS |
| T62f | `os.system('id')` | Rifiutato | ✅ PASS |
| T62f | `(lambda: 42)()` | Rifiutato | ✅ PASS |
| T62f | `__builtins__` | Rifiutato | ✅ PASS |
| T62f | `[x for x in range(3)]` | Rifiutato | ✅ PASS |
| T62f | `open('/etc/passwd')` | Rifiutato | ✅ PASS |
| T62g | `1/0` | Errore: divisione per zero | ✅ PASS |
| T62h | `""` (vuota) | Errore: espressione vuota | ✅ PASS |
| T62k | `math.factorial(171)` | Bigint, nessun crash | ✅ PASS |
| T62i | execute_tool_call dispatch `7*8` | `'56'` | ✅ PASS |
| T62j | execute_tool_call tool ignoto | `'Tool non trovato.'` | ✅ PASS |

**Suite completa: 292 PASS, 0 FAIL** (da 276 → +16 nuovi T62).

---

## VERDETTO REVISORE #93

**APPROVATO CON RISERVE**

Riserve non bloccanti (tracciate):
- **R-calcola-1**: `math.factorial(171)` → OverflowError non testato (nota: Python bigint non dà OverflowError; aggiunto T62k che verifica nessun crash + risultato numerico).
- **R-calcola-2**: T62f condizione `or _r.startswith("Errore")` accetta "Errore di sintassi" come risposta valida agli exploit (sicurezza reale non impattata).

Rischio dichiarato dal revisore: round-trip agentico con modello LLM reale non verificato (richiede chiavi API live) — da validare al primo deploy VPS.

---

## FILE MODIFICATI

- `gas.py` — imports (`ast`, `math`), `_GAS_SYSTEM_PROMPT_BASE`, `_calcola*`, `_build_system_prompt`, `tools_schema`, `execute_tool_call`
- `gas_identity.md` — lista 7 tool nativi, persona coerente
- `tests/test_unit_kernel.py` — T62a-T62k (+16 test)

## STOP GATE

Scope fisso rispettato: nessun finding extra committato, nessun refactor aggiuntivo.
