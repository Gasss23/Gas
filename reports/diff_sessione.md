# Diff sessione: feat/gate-c1 (2026-09-30)

## File toccati

```
.claude/agents/memoria_revisore.md  +3   (review #116 aggiunta)
modules/gate/__init__.py            +4   (NUOVO — esporta gate module)
modules/gate/gate.py               +214  (NUOVO — classificatore C1)
reports/stato_progetto.md          +9/-3 (aggiornamento header + entry C1 + counter review)
tests/test_unit_gate.py            +298  (NUOVO — 65 test gate)
reports/ultimo_report.md                 (NUOVO — report task)
reports/handoff.md                       (NUOVO — handoff sessione)
reports/diff_sessione.md                 (questo file)
```

## Cosa è cambiato e perché

### `modules/gate/gate.py` (nuovo, 214 righe)
Classificatore deterministico C1. Implementa le 5 regole del design §6:
- GateClass enum (SAFE/UNCERTAIN/IRREVERSIBLE/DENY)
- GATE_ALLOWLIST hardcoded, GATE_DENY_TOOLS frozenset
- Denylist path (NFC+normpath+casefold, 11 prefissi §2b+§5)
- §8e run_command: UNCERTAIN solo se `GAS_SANDBOX_MODE == "os_strict"`
- Fail-closed: nessuna eccezione propagata verso l'esterno

### `modules/gate/__init__.py` (nuovo, 4 righe)
Punto di ingresso del modulo; esporta i 4 simboli pubblici.

### `tests/test_unit_gate.py` (nuovo, 298 righe, 65 test)
Copertura completa del classificatore in isolamento (no GasKernel, no LLM, no DB):
- Tool noti, tool non validi, denylist write_file/read_file, args malformati, run_command sandbox.

### `.claude/agents/memoria_revisore.md`
Revisore ha aggiunto riga #116 (APPROVATO CON RISERVE, R-gate-1/2/3) e 2 lezioni: NFC vs NFKC per path di sicurezza; vettore --flag=value.

### `reports/stato_progetto.md`
- Header aggiornato al task corrente
- Entry feat/gate-c1 aggiunta in cima a Stato motore
- Counter review: 108 → 116
- Suite gate: 65 PASS menzionati

## Cosa NON è cambiato

- `gas.py` — invariato (stop gate C1) ✅
- `brains/` — invariato ✅
- `.github/workflows/ci.yml` — invariato (R-gate-3 tracciata) ✅
- Qualsiasi altro file motore — invariato ✅
