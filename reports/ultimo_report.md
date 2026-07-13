# Ultimo Report — fix/riserva-44B-groq-prezzi-env

**Data**: 2026-07-13
**Task**: Riserva #44B — prezzi Groq env-overridabili
**Commit motore**: `290a336`
**Branch**: `fix/riserva-44B-groq-prezzi-env`
**Stato**: ✅ COMPLETATO

---

## Problema

`gas.py:126` aveva i prezzi Groq hardcoded come literal: `(0.15, 0.60)` nel dict
`_PROVIDER_PRICE_PER_MTok`. I prezzi sono corretti al 2026-07-13 (verificato su
groq.com/pricing), ma in passato erano già cambiati ($0.75→$0.60 su output). Se
cambiano di nuovo, la contabilità mente in silenzio.

## Soluzione

**Fetta unica**, nessun refactor multi-provider:

1. **`brains/model_ids.py`** — aggiunte due costanti lette da env con fallback ai
   valori corretti:
   ```python
   try:
       GROQ_PRICE_IN_USD_PER_1M  = float(os.getenv("GAS_GROQ_PRICE_IN",  "0.15"))
       GROQ_PRICE_OUT_USD_PER_1M = float(os.getenv("GAS_GROQ_PRICE_OUT", "0.60"))
   except (TypeError, ValueError):
       GROQ_PRICE_IN_USD_PER_1M  = 0.15
       GROQ_PRICE_OUT_USD_PER_1M = 0.60
   ```
   Il `try/except` protegge da env non numerici (es. `GAS_GROQ_PRICE_IN=abc`)
   senza crashare all'avvio.

2. **`gas.py`** — importa le due costanti e le usa nella tabella prezzi:
   ```python
   "groq": (GROQ_PRICE_IN_USD_PER_1M, GROQ_PRICE_OUT_USD_PER_1M),
   ```

3. **`tests/test_unit_kernel.py`** — aggiunti T44b e T44c:
   - T44b: verifica che i default siano (0.15, 0.60) da model_ids
   - T44c: con env `GAS_GROQ_PRICE_IN=1.00` / `GAS_GROQ_PRICE_OUT=2.00`,
     `_daily_cost_usd()` calcola 3.00 USD su 1M+1M token

## Test

```
=== RIEPILOGO: 219 PASS, 0 FAIL ===
[PASS] T44b prezzi Groq default: (0.15, 0.60) da model_ids — prezzi=(0.15, 0.6)
[PASS] T44c prezzi Groq env-override: _daily_cost_usd usa i nuovi prezzi — calcolato=3.0000 atteso=3.0000 p_in=1.0 p_out=2.0
```

## Gate revisore

- **Review #46 — prima passata**: APPROVATO CON RISERVE (mancava try/except)
- **Review #46 — seconda passata**: APPROVATO

## File modificati

```
 brains/model_ids.py       |  9 +++++++++
 gas.py                    |  3 ++-
 tests/test_unit_kernel.py | 49 +++++++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 60 insertions(+), 1 deletion(-)
```

## Operativo da subito

Nessun cambiamento di comportamento di default. Per aggiornare i prezzi Groq
senza ricompilare: impostare `GAS_GROQ_PRICE_IN` e/o `GAS_GROQ_PRICE_OUT` nel
`.env` del VPS e riavviare Gas.
