# Diff della sessione — 2026-11-11 notte — voce: «parola quasi sentita» (M1)

Si riscrive a ogni sessione; la storia completa sta in git.

- `clients/voice/ascolto.py`: `SOGLIA_QUASI`/`QUASI_PAUSA_S`, traccia delle salite in `aspetta_parola`, `_segnala_quasi` (riga di log a intervalli), contatore `_blocchi_letti`. Motivo: chiamate vere scartate dalla soglia 0,7×3 blocchi senza traccia nel log.
- `scripts/voce/diagnosi_ascolto.py`: `Quasi`, `leggi_quasi`, `riassunto_quasi`; `main` stampa anche la sezione nuova.
- `scripts/voce/LEGGIMI.md`: spiegazione della riga e della taratura.
- `tests/test_unit_voce_ascolto.py`: 6 test nuovi.
- `.claude/agents/memoria_revisore.md`: riga #791-M1coord.
- `reports/*`: report di fine sessione e riserve.
