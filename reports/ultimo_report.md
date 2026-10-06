# ULTIMO REPORT — 2026-10-06 — F-mac-3: pytest senza target raccoglie l'intero repo

## Decisioni umane richieste

1. Merge della PR #139 (https://github.com/Gasss23/Gas/pull/139) — rischio basso, solo test/configurazione di pytest.

## Esito per fette

- **F-mac-3**: FATTA — i 4 probe `clients/voice/probe/win_*_test.py` (sys.exit all'import) e lo script `tests/test_unit_kernel.py` esclusi dalla collection con due `conftest.py`; test strutturale (collection dell'intero repo rc 0/5). Collection intera: rc 3 → rc 0 (663 test).
- **Prove**: senza l'uno o l'altro conftest il test strutturale fallisce; suite CI 612 passed; kernel 653/0.
- **Review**: #190 BOCCIATO (la prima versione sistemava solo `win_mic_test.py`) → #191 APPROVATO CON RISERVE (R-191-1 cosmetica).
- **Prova su macOS/Windows**: NON VERIFICATA.

## Anomalie

- Nessuna. `gh` non autenticato: PR via connettore GitHub.
