# Diff sessione — 2026-10-01 (feat/cancello-c2)

Questo file si riscrive a ogni sessione; la storia completa sta in git.

## File toccati

| File | Modifiche | Motivo |
|---|---|---|
| `gas.py` | +99/-19 | C2 + R-nw-1 |
| `modules/gate/gate.py` | +6 | UNTRUSTED_INPUT_TOOLS |
| `tests/test_unit_kernel.py` | +183 | T71a-T71h + T72a-T72e |
| `.claude/agents/memoria_revisore.md` | +5 | review #118 + #119 |
| `reports/ultimo_report.md` | aggiornato | fine-task |
| `reports/handoff.md` | aggiornato | fine-task |
| `reports/diff_sessione.md` | aggiornato | fine-task |
| `reports/stato_progetto.md` | aggiornato | R-nw-1 CHIUSO, F-controlli-auto, riserve C2 |

## Cosa è cambiato e perché

**modules/gate/gate.py**: aggiunta `UNTRUSTED_INPUT_TOOLS` — frozenset dei tool il cui output contamina la finestra conversazionale (§3b design).

**gas.py — `_safe_path` (R-nw-1)**: riscritta con `resolve(strict=False)`, confinamento su `is_relative_to(root_resolved)` PRIMA della denylist, check denylist su `path.relative_to(root_resolved).parts` (fix R-c2-1), casefold + normalizzazione trattini, fail-closed con log eccezione. Rimosso check inline write_file.

**gas.py — `_finestra_e_contaminata`**: metodo statico puro (R-c2-3) — testabile direttamente, usato in run_turn.

**gas.py — `run_turn` (C2)**: calcola `_finestra_contaminata` dalla window ad ogni iterazione; gate check (DENY/stub/normale) prima di ogni tool call.

**tests/test_unit_kernel.py**: +23 test T71a-T71h (R-nw-1) + T72a-T72e (C2). Suite: 423 PASS, 5 FAIL F-mac-1 invariati.

## Stato suite

- Kernel: 423 PASS, 5 FAIL F-mac-1 (bwrap macOS, invariati)
- Gate pytest: 74 PASS
