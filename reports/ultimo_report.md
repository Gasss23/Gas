# Ultimo Report — 2026-06-27 (FASE 2.5 + verifica R-budget-tz)

**Data**: 2026-06-27
**Review gate**: #39 — APPROVATO CON RISERVE
**Commit motore**: `65c4c7b`

---

## Task 1: Verifica R-budget-tz (falsa riserva) ✅

Il SE aveva segnalato rischio MEDIO: `_log_tokens` potrebbe scrivere ora locale mentre `_daily_cost_usd` usa UTC.

**Verifica**: `_log_tokens` usa già `datetime.now(timezone.utc).strftime(...)` — stesso formato del cutoff in `_daily_cost_usd`. Entrambi i lati usano UTC esplicito. Nessun fix necessario. R-budget-tz **chiusa come falsa riserva**.

---

## Task 2: FASE 2.5 — Compressione automatica `.gas_history.json` ✅

**Problema**: su VPS h24 la cronologia cresce indefinitamente (2-N messaggi per turno). Dopo settimane di attività la finestra satura i limiti token dei provider.

**Implementazione**:

### `_compress_history_if_needed(force=False)` su GasKernel

Logica:
1. Legge `GAS_HISTORY_MAX_MSGS` (default 100) e `GAS_HISTORY_KEEP_MSGS` (default 20) via `_env_int` fail-safe.
2. Warning se keep > max (misconfiguration, R-comp-2 chiusa).
3. Se `len(history) <= max_msgs` e non `force`: ritorna False (no-op).
4. Costruisce riepilogo deterministico testuale dei messaggi `history[:-keep_msgs]`: role + content[:300] o nomi tool call.
5. Allinea `recent = history[-keep_msgs:]` al primo user (scarta messaggi orfani al confine, R-comp-1 documentata).
6. Sostituisce history con: `[user(riepilogo), assistant(ack)] + recent`.
7. Chiama `_save_history()` e ritorna True.
8. Fail-safe §9: qualsiasi eccezione → history invariata, ritorna False.

**Zero token LLM**. Compressione puramente deterministica.

### Auto-trigger in `run_turn()`

```python
self._compress_history_if_needed()   # FASE 2.5 — no-op se sotto soglia
self._add_to_history("user", content=user_prompt)
```

### CLI `gas compress-history`

Forza la compressione manuale (utile pre-deploy VPS o per reset del contesto).

### Costanti di classe

```python
HISTORY_MAX_MSGS = 100   # trigger auto-compressione
HISTORY_KEEP_MSGS = 20   # messaggi recenti preservati intatti
```

---

## Suite test

| Ambiente | PASS | FAIL | Note |
|---|---|---|---|
| Windows (PYTHONUTF8=1) | 194 | 7 | 7 FAIL pre-esistenti (bwrap, WinError32) |
| CI Linux (attesa) | ~205 | 0 | +4 test rispetto a 201 precedenti |

**Test nuovi (T49-T52)**:
- T49: sotto soglia → False, history invariata
- T50: sopra soglia → True, struttura user(riepilogo)/assistant(ack)/recenti
- T51: force=True → comprime sempre indipendentemente dalla soglia
- T52: persistenza su disco — rilettura coerente

---

## Riserve review #39 (non bloccanti)

- **R-comp-1**: messaggi al confine old→recent scartati dall'allineamento (documentato nel docstring).
- **R-comp-2**: misconfiguration keep>max → warning logging aggiunto.
- **R-comp-3**: test edge-case "nessun user in recent" e misconfiguration — futuri.

---

## Diff stat motore (commit 65c4c7b)

```
gas.py                    | 100 +++++++++++++++++++++++++++
tests/test_unit_kernel.py |  67 ++++++++++++++++++
2 files changed, 167 insertions(+)
```
