# Diff sessione — 2026-10-01 (feat/cancello-c2)

## File toccati

| File | Modifiche | Motivo |
|---|---|---|
| `gas.py` | +99/-19 righe | C2 + R-nw-1 |
| `modules/gate/gate.py` | +6 righe | UNTRUSTED_INPUT_TOOLS |
| `tests/test_unit_kernel.py` | +164 righe | T71a-T71h + T72a-T72e |

## Cosa è cambiato e perché

**modules/gate/gate.py**: aggiunta costante `UNTRUSTED_INPUT_TOOLS` (frozenset: ricorda, read_file, browser_scrape, fetch_email). Definisce quali tool result "contaminano" la finestra conversazionale secondo il design §3b.

**gas.py — _safe_path (R-nw-1)**: riscritta con `resolve(strict=False)`, check confinamento su `is_relative_to(root_resolved)` PRIMA della denylist, check denylist su `path.relative_to(root_resolved).parts` (non sui componenti assoluti — fix R-c2-1), casefold + normalizzazione trattini/spazi, fail-closed con log eccezione. Rimosso il check inline nella branch write_file di execute_tool_call (ora unificato in _safe_path).

**gas.py — _finestra_e_contaminata**: aggiunto metodo statico puro che controlla se la window contiene tool result da UNTRUSTED_INPUT_TOOLS. Usato in run_turn, testato direttamente in T72e.

**gas.py — run_turn (C2)**: il loop agentico ora calcola `_finestra_contaminata` dalla window ad ogni iterazione. Aggiunto gate check prima di ogni execute_tool_call: DENY → risposta "Operazione negata" senza crash, IRREVERSIBLE/UNCERTAIN+contaminata → stub approved (coda reale verrà in C3), SAFE/UNCERTAIN pulita → esecuzione normale.

**tests/test_unit_kernel.py**: +23 test. T71a-T71h coprono R-nw-1 (symlink, traversal, case, regressione root con prefisso negato). T72a-T72e coprono C2 (SAFE invariato, DENY senza crash, stub approved, UNTRUSTED_INPUT_TOOLS membership, _finestra_e_contaminata diretto).

## Stato suite

- Kernel: 423 PASS, 5 FAIL F-mac-1 (invariati, bwrap macOS)
- Gate pytest: 74 PASS

## Commit di sessione

```
c388c0f feat(cancello-c2): C2 gate integration + R-nw-1 path hardening
b5b99d6 chore(revisore): memoria review #119 — APPROVATO CON RISERVE
1759355 chore(revisore): memoria review #118 — APPROVATO CON RISERVE
```
