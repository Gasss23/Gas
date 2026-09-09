# Report task: docs/migrazione-mac-2026-09-09

**Data:** 2026-09-09  
**Branch:** docs/migrazione-mac-2026-09-09  
**Tipo:** DOC-ONLY (nessuna modifica al motore)

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #86 (https://github.com/Gasss23/Gas/pull/86).

---

## Esito fette

**Fetta 1 — Crea branch docs/migrazione-mac-2026-09-09**: FATTA.

**Fetta 2 — Aggiorna reports/stato_progetto.md (voce migrazione 2026-09-09)**: FATTA.
- Header "Ultimo aggiornamento" aggiornato a 2026-09-09.
- Nuova sezione `### Migrazione Windows/WSL → MacBook Air M2 (2026-09-09)` con: file reimportati dal kit di trasloco, verifiche gas doctor + pytest (290 PASS / 5 FAIL bwrap-only), setup Mac (Python 3.14, venv .venv, chiavi da ~/.zshrc, gasmerge symlink R10, Claude Code 2.1.267).

**Fetta 3 — Registra F-mac-1, F-mac-2, F-mac-3 come finding aperti**: FATTA.
- F-mac-1: test T11c2/T11e/T12a/T12c/T12e FAIL su macOS (bwrap assente) → devono SKIP come T13d. Fix test-only.
- F-mac-2: `modules/memory/store.py:204` SyntaxWarning regex `\+` → usare raw string `r"\+"`. Fix minore.
- F-mac-3: `clients/voice/probe/win_mic_test.py` sys.exit(1) all'import senza sounddevice → rompe collection pytest. Fix robustezza.

**Fetta 4 — Apri PR**: FATTA. PR #86 — https://github.com/Gasss23/Gas/pull/86

---

## Gate di stop verificato

- ✅ DOC-ONLY: gas.py, brains/, modules/, tests/ non toccati.
- ✅ Finding registrati ma NON risolti (scope rispettato).
- ✅ Nessuna review del revisore necessaria (commit doc-only).
