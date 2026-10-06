# ULTIMO REPORT — 2026-10-06 — F-mac-1: test di run_command senza sandbox OS + sandbox esigito in CI

## Decisioni umane richieste

1. Merge della PR #136 — consigliato: sul Mac la suite kernel passa da 5 FAIL "attesi" a 0.
2. Dopo il merge, sul Mac: `python tests/test_unit_kernel.py` deve dare 0 FAIL (conferma su macOS reale, non provata qui).
3. Ordine di merge della notte: ogni PR riscrive i report canonici; dopo un merge le altre vanno riallineate a main.

## Esito per fette

- **F-mac-1**: FATTA — helper `senza_sandbox_os_usa_fallback`: senza sandbox OS T11c2/T11e/T12* girano in `os_with_fallback` (niente SKIP); con il sandbox restano `os_strict` (check T12-modo).
- **R-173-1** (CI perdeva l'allarme su una sonda regredita): FATTA — `GAS_TEST_SANDBOX_OS_ATTESO=1` nello step della suite + check T13-atteso.
- **R-173-2** (frase "devono essere SKIP" in stato): FATTA.
- **Prove**: con bwrap 653/0; senza bwrap simulato 648/0 (prima 642/5); sonda regredita in CI → 1 FAIL voluto; mutation dell'helper uccise.
- **Review**: #173 APPROVATO CON RISERVE → #175 APPROVATO.
- **macOS reale**: NON VERIFICATO (simulato pre-impostando la cache della sonda).

## Anomalie

- Nessuna. `gh` non autenticato: PR via connettore GitHub.
