# Report task: feat/gate-c1 — fix C1 (NFKC, substring run_command, ci.yml, commit_memoria_revisore)

**Data**: 2026-10-01  
**Branch**: feat/gate-c1  
**Review**: #117 APPROVATO CON RISERVE  

## DECISIONI UMANE RICHIESTE

Nessuna. Tutte le riserve di C1 chiuse. Riserve residue pre-C2:
- **R-nw-1** (minore): controllo puramente lessicale — symlink non risolti. Da gestire in C2 con `Path.resolve()` + root confinement.
- **R-nw-2** (cosmetic): substring check su comando intero può dare false deny su dir che iniziano con prefix deny (es. `brains_backup/` → contiene "brains" → DENY). Fail-closed by design.

## Esito fette

- **FIX 1 — CI (R-gate-3)**: `FATTA` — step "Run gate suite" aggiunto a ci.yml; gate output incluso nel job summary.
- **FIX 2 — run_command substring (R-gate-2)**: `FATTA` — `gate.py:206-212`: NFKC+casefold sull'intera stringa comando; se contiene sottostringa deny → DENY. `grep --file=.env.prod x`, `grep -f.env x` → ora DENY. 6 test nuovi in TestRunCommand.
- **FIX 3 — NFKC (R-gate-1)**: `FATTA` — `gate.py:91`: NFC → NFKC. FULLWIDTH FULL STOP U+FF0E (．) ora ridotto a ASCII '.'. 3 test nuovi in TestNFKC.
- **FIX 4 — commit_memoria_revisore.sh bug**: `FATTA` — `scripts/commit_memoria_revisore.sh:47`: `tail -1` → `grep -E '^#[0-9]+' ... | tail -1`. Il vecchio codice estraeva `#12` da "(lezione #12)" nell'ultima riga; il nuovo cerca solo righe che iniziano con `^#NNN`. 1 test nuovo T-R2-f in TestCommitMemoriaRevisore.

## Suite

- Gate (pytest): **74 PASS, 0 FAIL** (+9: 6 TestRunCommand + 3 TestNFKC)
- Hook (pytest): **37 PASS, 0 FAIL** (+1: T-R2-f)
- Kernel: **400 PASS, 5 FAIL** F-mac-1 bwrap macOS (invariati)
- `.gas_memory.db` SHA256 invariato: `d1c8f0cc2961145a629bf0b57a43d1b0328fe4db1bf5c428a8037c92b756ef11`

## File toccati (questa sessione)

```
modules/gate/gate.py               — NFKC, substring check run_command, docstring
tests/test_unit_gate.py            — +9 test (TestRunCommand ×6, TestNFKC ×3)
.github/workflows/ci.yml           — step gate suite + gate nel job summary
scripts/commit_memoria_revisore.sh — fix grep '^#[0-9]+' invece di tail -1
tests/test_unit_hooks.py           — +1 test T-R2-f
reports/stato_progetto.md          — aggiornamento + nota commit errati 83354d8/a3afcfd
.claude/agents/memoria_revisore.md — #117 da revisore
```

## Nota commit errati (registrata)

`83354d8` ("chore(revisore): memoria review #12 — ?") e `a3afcfd` ("chore(revisore): memoria review #? — ?") hanno subject errati a causa del bug ora corretto in commit_memoria_revisore.sh. I commit NON vengono riscritti; registrati in stato_progetto.md.
