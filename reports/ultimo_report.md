# R-wire-1 — Soglia semantica `VEC_MIN_SIM` configurabile via env

**Data:** 2026-06-21
**Task:** chiudere la parte azionabile dell'item aperto #1 (R-wire-1): rendere la soglia di
similarità coseno `VEC_MIN_SIM` ri-tarabile al deploy senza ricompilare, via variabile d'ambiente,
con lo stesso pattern già usato per `VEC_CATCHUP_MAX` (`GAS_VECTORS_CATCHUP_MAX`).
**Review:** #28 — **APPROVATO** (subagent `revisore`, protocollo `.claude/agents/revisore.md`).

---

## COSA È STATO FATTO

### `gas.py`

1. **Nuovo helper PURO `_env_float`** (accanto a `_env_int`/`_env_flag`):
   ```python
   def _env_float(name: str, default: float, min_val: float = 0.0,
                  max_val: float = 1.0) -> float:
   ```
   Fail-safe (§9):
   - env assente → `default`;
   - non parsabile → `default` + `logging.warning` nella scatola nera;
   - fuori range → clamp a `[min_val, max_val]` via `min(max_val, max(min_val, float(raw)))`.
   - `max_val=1.0` di default perché la similarità coseno di embedding normalizzati a norma 1 è ≤ 1.

2. **Risoluzione in `__init__`** (stesso schema di `VEC_CATCHUP_MAX`):
   ```python
   self.VEC_MIN_SIM = _env_float("GAS_VECTORS_MIN_SIM", GasKernel.VEC_MIN_SIM)
   ```
   L'attributo d'istanza shadowa il default di classe ed è realmente consumato dal call-site del
   retrieval semantico (`min_sim=self.VEC_MIN_SIM`) → l'override NON è inerte.

3. **Default di classe `VEC_MIN_SIM = 0.30` INVARIATO** + commento aggiornato (override env
   `GAS_VECTORS_MIN_SIM`, risolto in `__init__`). Con env assente il comportamento resta
   bit-identico a prima.

### `tests/test_unit_kernel.py`

- **Nuovo test T22f2**: copre i 5 casi —
  1. env assente → default (a livello helper),
  2. valore presente → parse a livello helper (`0.7`),
  3. valido → `0.45` via `kernel_tmp()` (path reale del kernel),
  4. sporco (`"abc"`) → default di classe,
  5. clamp alto (`"5.0"`) → `1.0`, clamp basso (`"-1"`) → `0.0`.
  Ripristina lo stato dell'env nel `finally`.
- **Ridondanza minore corretta in sessione** (nota non bloccante del revisore): la seconda
  asserzione, in origine duplicato identico della prima (`assente→default`), è stata sostituita
  da un controllo distinto e utile: parse a livello helper di un valore *presente*.

---

## REVIEW (protocollo `revisore.md`)

Eseguito da agente general-purpose che ha seguito alla lettera il protocollo: lette le 3 fonti
obbligatorie (CLAUDE.md sez.5, `reports/stato_progetto.md`, `.claude/agents/memoria_revisore.md`),
esaminato il diff, verificato dal vivo.

**Verdetto: APPROVATO.** Riserve: nessuna bloccante. Note minori:
- la ridondanza in T22f2 (corretta in sessione, vedi sopra);
- la ri-taratura effettiva del valore sul primo diario reale del VPS resta lavoro futuro
  (deploy-dependent): questo task chiude la sola parte "configurabilità via env".

Memoria revisore: NON aggiornata (nessuna lezione nuova; `_env_float` è già coperto dalla lezione
del 2026-06-16 su `_env_int` e lo shadow degli attributi d'istanza).

---

## VERIFICA REALE (suite, eseguita nel venv del progetto su Windows)

```
PYTHONUTF8=1  .\venv\Scripts\python.exe tests/test_unit_kernel.py
```

| Stato | PASS | FAIL | Totale |
|-------|------|------|--------|
| HEAD pulito (modifiche in stash) | 157 | 9 | 166 |
| Working tree (con R-wire-1) | **158** | **9** | 167 |

- **T22f2 → PASS** (`valid=True dirty=True hi=True lo=True`).
- I **9 FAIL sono TUTTI pre-esistenti e ambientali su Windows**, VERIFICATO identici su HEAD
  pulito (stash + re-run): sandbox bwrap assente (T11c2, T11e, T12a, T12c, T12e, T13d2),
  env API/storia (T9a, T9c), WinError32 rotazione backup (T26b). Sul VPS Linux non si presentano.
- R-wire-1 aggiunge esattamente **+1 PASS (T22f2) e 0 regressioni**.
- NB: il "158/8" dei report precedenti era un conteggio leggermente datato dei FAIL ambientali
  Windows (un test snapshot flippa PASS↔FAIL a seconda dello stato git accumulato, non per codice).

Invarianti motore (`_get_window`/`_cap_window_chars`/`for _ in range(10)`/sandbox/snapshot/pin)
INTATTE; nessun antipattern del Wall of Shame (§5).

---

## STATO FINALE

- **R-wire-1 (parte azionabile): CHIUSO.** `VEC_MIN_SIM` è ri-tarabile via `GAS_VECTORS_MIN_SIM`
  senza redeploy.
- **Residuo aperto:** ri-taratura del valore sul primo diario reale del VPS → voce CHECKLIST
  pre-deploy VPS (FASE 5), non eseguibile ora (richiede il diario reale).
- **Segnalazione fuori scope:** l'item aperto #2 di CLAUDE.md (R-crm-norm-2) risulta già CHIUSO
  il 2026-06-20 (review #27) — la lista item aperti è stale su quel punto; non toccata in questo
  task (decisione umana).
