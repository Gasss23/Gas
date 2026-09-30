# Diff sessione: feat/gate-c1 fix C1 (2026-10-01)

## File toccati

```
modules/gate/gate.py               — NFC→NFKC (R-gate-1); substring check run_command (R-gate-2); docstring aggiornato
tests/test_unit_gate.py            — +9 test: TestRunCommand ×6 (R-gate-2), TestNFKC ×3 (R-gate-1)
.github/workflows/ci.yml           — step "Run gate suite" + gate nel job summary (R-gate-3)
scripts/commit_memoria_revisore.sh — fix: grep '^#[0-9]+' invece di tail -1 (FIX-4)
tests/test_unit_hooks.py           — +1 test T-R2-f (verifica #116 estratto, non #12)
reports/stato_progetto.md          — header aggiornato, entry C1 + nota commit errati
.claude/agents/memoria_revisore.md — #117 APPROVATO CON RISERVE aggiunto dal revisore
reports/ultimo_report.md           — report canonico sessione
reports/handoff.md                 — handoff sessione
reports/diff_sessione.md           — questo file
```

## Cosa è cambiato e perché

### `modules/gate/gate.py`
- Riga 91: `NFC` → `NFKC`. FULLWIDTH FULL STOP U+FF0E non ridotto da NFC, bypassava la denylist. NFKC lo riduce ad ASCII '.'.
- Righe 206-212: aggiunto substring check belt-and-suspenders sull'intera stringa comando (NFKC+casefold). Copre `--flag=.env.prod` e `-f.env` dove il token non è un path normalizzabile.

### `tests/test_unit_gate.py`
- 6 test TestRunCommand: coprono i casi R-gate-2 (flag_eq_env_prod, short_flag_env, traversal_to_env, uppercase_gas_memory, dotslash_modules, normal_command_not_denied).
- 3 test TestNFKC: coprono R-gate-1 (fullwidth write/read con U+FF0E).

### `.github/workflows/ci.yml`
- Step "Run gate suite (pytest, zero token LLM)" aggiunto dopo voice suite (stesso stile).
- Gate output aggiunto al job summary (griep + FAIL gate).

### `scripts/commit_memoria_revisore.sh`
- Bug: `tail -1` sul file intero prendeva l'ultima riga (una nota lezione contenente "(lezione #12)") → `grep -oE '#[0-9]+' | head -1` estraeva #12.
- Fix: `grep -E '^#[0-9]+' ... | tail -1` cerca solo le righe che iniziano con `^#NNN`.
- `grep -oE '^#[0-9]+'` (ancorato a inizio riga) per REVIEW_NUM, eliminando ambiguità.

### `tests/test_unit_hooks.py`
- T-R2-f: file con #12 + #116 + nota lezione contenente "#12" → subject atteso "#116 — APPROVATO CON RISERVE".

## Cosa NON è cambiato

- `gas.py` — invariato ✅
- `brains/` — invariato ✅
- Qualsiasi altro file motore — invariato ✅
