# Diff sessione — 2026-06-25 (due task: env-config sprint + stima costi token)

> Si riscrive a ogni sessione. La storia completa sta in git.

## File toccati

| File | Cosa |
|---|---|
| `gas.py` | env-config sprint (MEMORY_PIN_SCAN, WINDOW_CHAR_CAP, GAS_VECTORS_DB, GAS_EMBED_MODEL, doctor sez.9 Config) + stima costi (`_PROVIDER_PRICE_PER_MTok`, `tokens_cmd` aggiornato) |
| `tests/test_unit_kernel.py` | T37a-T37e (env-config) + T38a-T38c (stima costi) — 8 nuovi test |
| `reports/stato_progetto.md` | finding chiusi (R-vec-2, WINDOW_CHAR_CAP, MEMORY_PIN_SCAN), review 30→32, suite 163→171 |
| `.claude/agents/memoria_revisore.md` | lezioni review #31 e #32 |
| `reports/ultimo_report.md` | report task corrente (stima costi) |
| `reports/diff_sessione.md` | questo file |

## Cosa è cambiato e perché

**Task 1 — Env-configurabilità sprint (review #31):** 3 finding aperti chiusi:
`GAS_WINDOW_CHAR_CAP`, `GAS_MEMORY_PIN_SCAN`, `GAS_VECTORS_DB`, `GAS_EMBED_MODEL` —
stesso pattern `_env_int` esistente. `gas doctor` aggiornato con sezione 9 "Config".

**Task 2 — Stima costi token (review #32):** `gas tokens` ora mostra una colonna
"Costo (★ USD)" con la stima per-provider calcolata da `_PROVIDER_PRICE_PER_MTok`
(prezzi appross. 2025-06). Provider ignoto → costo 0.0 senza nota. Loop protetto da
try/except su record JSONL malformati (§9). TOTALE aggiunto alla sezione "recenti".
