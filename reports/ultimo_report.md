# Report task: feat/gate-c1 — C1 scaffolding gate

**Data**: 2026-09-30  
**Branch**: feat/gate-c1  
**Review**: #116 APPROVATO CON RISERVE  

## Obiettivo

Implementare la Fetta C1 del Cancello: scaffolding puro del classificatore deterministico GAS, zero integrazione con gas.py.

## Cosa è stato fatto

### PASSO 0 — doc-only (commit 8b15b69)
- `reports/stato_progetto.md`: aggiunta `(R-eco-run-1)` al verdetto #115; registrata discrepanza commit b1b5fd9 vs memoria_revisore.md; aggiunto finding `🟡 F-diario-args`.
- `.claude/agents/memoria_revisore.md`: condizione per rettifica NON soddisfatta (riga #115 era già APPROVATO CON RISERVE) → nessuna modifica in passo 0b.

### PASSO 1 — codice (commit d74fed0)
- **`modules/gate/__init__.py`** (4 righe): esporta GateClass, GATE_ALLOWLIST, GATE_DENY_TOOLS, gate_classify.
- **`modules/gate/gate.py`** (214 righe): classificatore completo.
  - `GateClass`: enum SAFE / UNCERTAIN / IRREVERSIBLE / DENY.
  - `GATE_ALLOWLIST`: dict hardcoded 14 tool, nessun override YAML/env.
  - `GATE_DENY_TOOLS`: frozenset {"ssh", "modify_gate", "write_env"}.
  - `_DENY_PREFIXES`: 11 prefissi (.gas_memory, .gas_history, .gas_knowledge, .gas_vectors, .gas_tokens, .env, gas.py, brains, modules, .claude, gate_config).
  - `_normalize_path()`: NFC → strip "./" → normpath → casefold; ValueError su assoluti/traversal.
  - `_in_denylist()`: controlla path intero E ogni componente PurePosixPath.
  - `gate_classify()`: 5 regole; try/except globale → DENY (fail-closed, non solleva mai).
  - §8e: run_command → UNCERTAIN solo se `GAS_SANDBOX_MODE == "os_strict"`, altrimenti IRREVERSIBLE.

### PASSO 2 — test (commit d74fed0)
- **`tests/test_unit_gate.py`** (298 righe, 65 test): TestKnownTools (15), TestInvalidToolName (4), TestWriteFileDenylist (14), TestReadFileDenylist (12), TestMalformedArgs (10), TestRunCommand (9+1 extra).
- **65/65 PASS** locale (`.venv/bin/python3 -m pytest tests/test_unit_gate.py -v`).
- ⚠️ `test_unit_gate.py` NON incluso in `ci.yml` (solo `test_unit_kernel.py`, `test_unit_hooks.py`, `test_unit_voice_server.py` per nome esplicito). Tracciato come R-gate-3; `ci.yml` NON modificato per rispettare lo stop gate.

### PASSO 3 — revisore (commit 83354d8)
Revisore #116: **APPROVATO CON RISERVE** — vedere §Riserve aperte.

## Stop gate verificati

- ZERO modifiche a gas.py ✅
- ZERO modifiche a brains/ ✅
- ZERO modifiche a qualsiasi file motore esistente ✅
- GATE_ALLOWLIST hardcoded, no YAML/env ✅
- `ci.yml` NON modificato ✅

## Riserve aperte

- **R-gate-1** (minore, pre-C3/C4): `_normalize_path` usa `NFC` invece di `NFKC` — FULLWIDTH FULL STOP U+FF0E non ridotto a '.', bypassa denylist. Correggere prima dell'integrazione. File: `modules/gate/gate.py:88`.
- **R-gate-2** (minore, pre-C3/C4): token `--flag=value` in run_command non splittati su '=' — valore dopo '=' non controllato contro denylist. File: `modules/gate/gate.py:195-202`.
- **R-gate-3** (processo): `tests/test_unit_gate.py` escluso da `ci.yml`. Da aggiungere in una prossima fetta (o come PR separata).

## Suite

- Kernel (gas.py): 400 PASS, 5 FAIL F-mac-1 invariati (bwrap macOS).
- Gate (pytest): **65 PASS, 0 FAIL**.
- Kernel non toccato da C1: conteggio invariato.

## File toccati

```
.claude/agents/memoria_revisore.md  +3
modules/gate/__init__.py            +4 (nuovo)
modules/gate/gate.py                +214 (nuovo)
reports/stato_progetto.md           +9/-3
tests/test_unit_gate.py             +298 (nuovo)
```

## Commit sul branch

```
83354d8 chore(revisore): memoria review #12 — ?
d74fed0 feat(gate-c1): scaffolding gate — GateClass, GATE_ALLOWLIST, gate_classify + test
8b15b69 docs(gate-c1): passo 0 — rettifica #115 + finding F-diario-args
```
