# Diff della sessione — 2026-11-23 — Voce: 4 fasi, interruzione col filtro, griglia coerente

Si riscrive a ogni sessione; la storia completa sta in git. Ramo fix/voce-fasi-interruzione da main 1b4954e2.

- `clients/voice/ascolto.py`: `rilevatore_openwakeword(..., fasi)` con coda di 2 blocchi e 4 modelli sfalsati; `rilevatore_con_verifica(..., fasi)`; `GAS_ASCOLTO_FASI` in `main`; `_regolazioni`: col filtro attivo l'interruzione usa la soglia della parola su 1 blocco (se il `.env` non dice altro); avviso «più facile» coerente.
- `scripts/voce/registra_voce.py`: `MotoreOWW.blocchi` sulla stessa griglia di `misura`.
- `scripts/voce/taratura_parola.py`: stesse fasi dell'ascolto.
- `scripts/voce/LEGGIMI.md`: `GAS_ASCOLTO_FASI`, interruzione col filtro, vecchia soglia 0.8 da togliere.
- `tests/test_unit_voce_ascolto.py`: test delle fasi, dell'interruzione col filtro, della taratura; test esistenti aggiornati.
- `reports/stato_progetto.md`, report di fine task, `.claude/agents/memoria_revisore.md`.
