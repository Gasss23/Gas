# DIFF SESSIONE — 2026-07-13

> Riscritto a ogni sessione. Storia completa: git log.

## Sessione: fix/riserva-44B-groq-prezzi-env

### File toccati

```
 brains/model_ids.py       |  9 +++++++++
 gas.py                    |  3 ++-
 tests/test_unit_kernel.py | 49 +++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/ultimo_report.md  | riscritto
 reports/diff_sessione.md  | riscritto
 reports/stato_progetto.md | riserva (B) marcata CHIUSA
 reports/handoff.md        | riscritto
```

### Cosa è cambiato e perché

**`brains/model_ids.py`**: aggiunte due costanti `GROQ_PRICE_IN_USD_PER_1M` e
`GROQ_PRICE_OUT_USD_PER_1M`, lette da env `GAS_GROQ_PRICE_IN`/`GAS_GROQ_PRICE_OUT`
con fallback a 0.15/0.60 USD/MTok, protette da `try/except` contro valori non
numerici. Fonte dei prezzi: groq.com/pricing, verificato 2026-07-13.

**`gas.py`**: import delle due nuove costanti da model_ids; sostituzione dei due
literal hardcoded `0.15`/`0.60` nel dict `_PROVIDER_PRICE_PER_MTok["groq"]`.

**`tests/test_unit_kernel.py`**: aggiunti T44b (verifica default) e T44c
(verifica env-override con reload del modulo). Suite: 219 PASS, 0 FAIL.

### Motivazione

Chiude la riserva #44B aperta dalla review #44: i prezzi Groq erano literal
hardcoded e in passato erano già cambiati ($0.75→$0.60 su output al lancio).
La soluzione li porta in `brains/model_ids.py` (fonte unica già usata per i
model ID) rendendoli sovrascrivibili via env senza modifiche al codice.
