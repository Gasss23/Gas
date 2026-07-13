# DIFF SESSIONE — 2026-07-13

> Riscritto a ogni sessione. Storia completa: git log.

## Branch: fix/riserva-44B-groq-prezzi-env

## File toccati (da `git diff --stat` rispetto a main)

```
 brains/model_ids.py       |  9 +++++
 gas.py                    |  3 +-
 reports/diff_sessione.md  | 36 +++++++++++++----
 reports/handoff.md        | 98 +++++++++++++++++++++++++++++++++++------------
 reports/stato_progetto.md |  2 +-
 reports/ultimo_report.md  | 80 ++++++++++++++++++++++++++++++--------
 tests/test_unit_kernel.py | 80 ++++++++++++++++++++++++++++++++++++++
 7 files changed, 258 insertions(+), 50 deletions(-)
```

## Dettaglio per file

- **`brains/model_ids.py`**: aggiunte costanti `GROQ_PRICE_IN_USD_PER_1M` / `GROQ_PRICE_OUT_USD_PER_1M` lette da env `GAS_GROQ_PRICE_IN`/`GAS_GROQ_PRICE_OUT` con `try/except` (fallback 0.15/0.60); chiude riserva #44B.
- **`gas.py`**: importa le due nuove costanti da `brains/model_ids`; sostituisce i literal `(0.15, 0.60)` in `_PROVIDER_PRICE_PER_MTok["groq"]`.
- **`tests/test_unit_kernel.py`**: aggiunti T44b (verifica default), T44c (verifica env-override + `_daily_cost_usd`), T44d (verifica fallback anti-crash con env non numerici). Suite: 219→220 PASS.
- **`reports/stato_progetto.md`**: riserva #44B marcata CHIUSA con ref commit e PR.
- **`reports/ultimo_report.md`**: riscritto con esito fette, suite, gate revisore.
- **`reports/handoff.md`**: riscritto con template canonico — diff/log reali, verdetti revisore integrali, stato CI verbatim.
- **`reports/diff_sessione.md`**: questo file — riscritto.
