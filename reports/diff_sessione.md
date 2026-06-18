# 🔀 DIFF DI SESSIONE — 2026-06-18 (vector store WIRING al kernel)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni sessione.

## Tema
FASE 2 — WIRING del vector store (fetta 1 già in main, review #23) al motore: retrieval
semantico agganciato a `run_turn` (catch-up indexing) e `ricorda` (cascata + snippet
datato). Opt-in via env `GAS_VECTORS` (default OFF).

## File toccati
- **`gas.py`**: `_env_flag` (helper feature-gate); `__init__` costruisce `self.vectors`
  solo se `GAS_VECTORS` truthy (doppia cintura fail-safe come self.memory), default OFF;
  `self._vec_watermark` + `VEC_CATCHUP_MAX` (env override) + `VEC_MIN_SIM`; `_vettori_catchup()`
  (indicizzazione pigra/bounded, una volta per turno fuori dal loop); `_fmt_evento_datato`
  (snippet ts + stato corrente del lead); `_ricorda(query)` cascata NON regressiva
  FTS→semantico-riempie→substring; chiamata a `_vettori_catchup()` in run_turn dopo il backup.
- **`modules/memory/store.py`**: `diario_dopo(after_id, limit)` + `get_diario(id)`, SOLA
  LETTURA (immutabilità diario intatta).
- **`modules/memory/vectors.py`**: `index_batch` (embedding in blocco) + `max_source_ref`
  (watermark).
- **`tests/test_unit_kernel.py`**: T31a-g (wiring). Suite **145→152**, 0 FAIL.

## Decisione di design (deviazione onesta dal §FINALE)
Misurato dal vivo che il MiniLM separa DEBOLMENTE le query corte italiane (distrattore
'caffè' 0.288 > pertinente 'offerta' 0.237). Il §FINALE proponeva "semantico prima": avrebbe
REGREDITO la precisione. Invertito a "FTS autorità + semantico che RIEMPIE", soglia
`VEC_MIN_SIM=0.30`. Robustezza > potenza: il layer nuovo non regredisce il comportamento odierno.

## Processo
- Verifiche dal vivo: suite 152/152; E2E reale (GAS_VECTORS=1) query 'vendita' → recupero
  semantico "offerta commerciale ad Anna — lead Anna: oggi 'interessato'"; misure soglia reali.
- Review #24 (revisore) → APPROVATO CON RISERVE. Invarianti motore intatte, default-OFF
  bit-identico, immutabilità diario verificata. Riserve R-wire-1..4 (minori, non sicurezza)
  tracciate in `stato_progetto.md`.
- `gas.py` toccato ma invarianti (`_get_window`/`_cap_window_chars`/`for _ in range(10)`/
  sandbox/snapshot/pin) INTATTE.
