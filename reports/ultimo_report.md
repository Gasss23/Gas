# ULTIMO REPORT — 2026-10-06 — Test di R-167-1 su APFS: sonda del filesystem (SKIP sul Mac, FAIL in CI)

## Decisioni umane richieste

1. Merge della PR #137 (https://github.com/Gasss23/Gas/pull/137) — rischio nullo, solo test.
2. Dopo il merge, sul Mac: `python -m pytest tests/test_unit_gasmerge.py -k non_utf8 -rs` → atteso SKIPPED col motivo (APFS), non FAILED.

## Esito per fette

- **F-apfs** (sul Mac `test_path_non_utf8_non_nasconde_il_motore` falliva: APFS rifiuta nomi non UTF-8 con EILSEQ): FATTA — helper `_esigi_nomi_non_utf8`: rifiuto → SKIP col motivo; con `GAS_TEST_LOCALE_UTF8_ATTESO=1` (CI) → FAIL.
- **Prove**: Linux passed; APFS simulato → SKIPPED; APFS simulato + variabile → FAILED; suite gasmerge 88 passed.
- **Review**: #185 APPROVATO.
- **Prova su macOS reale**: NON VERIFICATA (nessun Mac nel container cloud).

## Anomalie

- Nessuna. `gh` non autenticato: PR via connettore GitHub.
