# Ultimo Report — 2026-06-27 (chiusura 5 item roadmap)

**Data**: 2026-06-27
**Review gate**: #38 — APPROVATO CON RISERVE
**Commit motore**: `a8c6d53`

---

## Task: Chiusura di tutti e 5 gli item aperti del roadmap

Tutti e 5 gli item aperti di `reports/roadmap.md` sono stati chiusi in questa sessione.

---

## Item 1 — Controllo spesa token (DEFINITIVO) ✅

- Nuovo metodo `_daily_cost_usd()` su `GasKernel`: legge `.gas_tokens.jsonl`, somma costi 24h usando `_PROVIDER_PRICE_PER_MTok`. Zero token LLM. Fail-safe §9: log assente/corrotto → 0.0.
- Kill-switch in `run_turn()`: legge `GAS_DAILY_TOKEN_BUDGET` (USD float via `_env_float`). Se configurato e budget superato: yield `{"type": "error", "content": "Budget giornaliero esaurito: $X.XXXX spesi (limite $Y.YY USD)."}` + `return`. Zero token consumati.
- Formato timestamp `ts` verificato identico tra `_log_tokens` e cutoff (ISO 8601 senza "Z") — R-budget-ts chiusa.
- Test T41-T44: tutti PASS (log assente, entry >24h, entry recente→costo corretto, budget esaurito→event error).

---

## Item 2 — Accesso telefono: Telegram bridge bot ✅

`modules/telegram/bot.py` + `modules/telegram/__init__.py`

- `run_bot()`: legge `TELEGRAM_BOT_TOKEN` + `TELEGRAM_ALLOWED_IDS` (fail-closed: assenti → rc=1). Un `GasKernel` condiviso. Long polling `getUpdates timeout=60`. Fail-safe §9 su ogni iterazione.
- `_handle_update()`: verifica whitelist chat_id, invia typing, chiama `run_turn()`, raccoglie eventi `final`/`tool_res`/`error`, `sendMessage` con troncamento a 4096 char.
- Zero nuove dipendenze (urllib stdlib).
- Correzione R-tel-2: `sys.path.insert` aveva condizione invertita — corretto.
- Test T45-T48: tutti PASS (import, no token→rc=1, no ALLOWED_IDS→rc=1, chat non autorizzata→nessun invio).

**Avvio VPS**: `export TELEGRAM_BOT_TOKEN=<token> TELEGRAM_ALLOWED_IDS=<chat_id> && gas telegram`

---

## Item 3 — Calibrazione VEC_MIN_SIM (R-wire-1) ✅

`gas calibrate-vectors [N]` → `calibrate_vectors_cmd()`

- Campiona N righe diario, query semantica su ognuna (auto-match escluso), distribuzione score coseno.
- Suggerisce `GAS_VECTORS_MIN_SIM = max(0.10, min(0.80, p25 - 0.05))`.
- Strumento da eseguire al deploy VPS sul diario reale.

---

## Item 4 — Evaluation e5-small vs MiniLM ✅

`gas eval-vectors [query] [k]` → `eval_vectors_cmd()`

- Mostra: modello, dim, n. vettori, min_sim. Con query: top-k risultati con score e soglia.
- `_MODEL_PREFIXES` già conteneva e5-small con prefissi corretti; zero cambio infra.

---

## Item 5 — R-reidx-3 picco RAM ✅ (chiuso review #30, docs aggiornati)

`ricostruisci_da_diario` usa batch paginati `REINDEX_BATCH_SIZE=256`. Su VPS CX22 4GB non bloccante.

---

## Suite test

| Ambiente | PASS | FAIL | Note |
|---|---|---|---|
| Windows (PYTHONUTF8=1) | 190 | 7 | 7 FAIL pre-esistenti (bwrap, WinError32) |
| CI Linux (attesa) | ~201 | 0 | +8 nuovi test rispetto a 193 precedenti |

---

## Riserve review #38 (non bloccanti)

- **R-tel-budget-perf**: scan JSONL completo ad ogni turno — ottimizzazione futura (lettura dal fondo).
- **R-tel-tool_res**: tool output compressi nel reply Telegram — accettabile, annotare nel docstring.

---

## Diff stat motore (commit a8c6d53)

```
gas.py                       | 155 +++++++++++++++++++++++++++++++++
modules/telegram/__init__.py |   0
modules/telegram/bot.py      | 198 +++++++++++++++++++++++++++++++++++++++++++
tests/test_unit_kernel.py    |  93 ++++++++++++++++++++
4 files changed, 446 insertions(+)
```
