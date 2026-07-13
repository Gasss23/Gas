# Ultimo Report — fix/riserva-44B-groq-prezzi-env

**Data**: 2026-07-13
**Task**: Riserva #44B — prezzi Groq env-overridabili + copertura fallback
**Commit motore**: `290a336`
**Commit test T44d**: `b3c8bb1`
**Branch**: `fix/riserva-44B-groq-prezzi-env`
**PR**: #6
**Stato**: ✅ COMPLETATO

---

## Problema

`gas.py:126` aveva i prezzi Groq hardcoded come literal: `(0.15, 0.60)` nel dict
`_PROVIDER_PRICE_PER_MTok`. I prezzi sono corretti al 2026-07-13 (verificato su
groq.com/pricing), ma in passato erano già cambiati ($0.75→$0.60 su output). Se
cambiano di nuovo, la contabilità mente in silenzio.

## Soluzione

**Due commit** sullo stesso branch:

### Commit 1 — `290a336`: fetta principale

1. **`brains/model_ids.py`** — costanti env-overridabili con fallback + try/except:
   ```python
   try:
       GROQ_PRICE_IN_USD_PER_1M  = float(os.getenv("GAS_GROQ_PRICE_IN",  "0.15"))
       GROQ_PRICE_OUT_USD_PER_1M = float(os.getenv("GAS_GROQ_PRICE_OUT", "0.60"))
   except (TypeError, ValueError):
       GROQ_PRICE_IN_USD_PER_1M  = 0.15
       GROQ_PRICE_OUT_USD_PER_1M = 0.60
   ```

2. **`gas.py`** — usa le costanti nella tabella prezzi invece dei literal.

3. **T44b + T44c** — verifica default (0.15, 0.60) e env-override funzionante.

### Commit 2 — `b3c8bb1`: copertura ramo fallback (osservazione review #46)

4. **T44d** — setta `GAS_GROQ_PRICE_IN="abc"` e `GAS_GROQ_PRICE_OUT="xyz"`;
   verifica nessuna eccezione e costanti a default 0.15/0.60.

## Test (verbatim)

```
--- T44b-T44c: prezzi Groq env-overridabili ---
[PASS] T44b prezzi Groq default: (0.15, 0.60) da model_ids — prezzi=(0.15, 0.6)
[PASS] T44c prezzi Groq env-override: _daily_cost_usd usa i nuovi prezzi — calcolato=3.0000 atteso=3.0000 p_in=1.0 p_out=2.0
--- T44d: fallback env non parsabile ---
[PASS] T44d env non parsabile (abc/xyz) → no crash, default 0.15/0.60 — p_in=0.15 p_out=0.6
=== RIEPILOGO: 220 PASS, 0 FAIL ===
```

## Gate revisore

- **Review #46 — prima passata**: APPROVATO CON RISERVES (mancava try/except)
- **Review #46 — seconda passata**: APPROVATO (solo test → gate non obbligatorio, suite eseguita)

## File modificati (totale branch)

```
 brains/model_ids.py       |  9 +++++++++
 gas.py                    |  3 ++-
 tests/test_unit_kernel.py | 80 ++++++++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 91 insertions(+), 1 deletion(-)
```

## Operativo da subito

Per aggiornare i prezzi Groq sul VPS senza ricompilare:
`GAS_GROQ_PRICE_IN=<nuovo_valore>` e `GAS_GROQ_PRICE_OUT=<nuovo_valore>` nel `.env`, poi riavvio Gas.
Valori non numerici → fallback silenzioso ai default, nessun crash.
