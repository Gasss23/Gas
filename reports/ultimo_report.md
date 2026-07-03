# Report R-vec-pool — Aggiunta fastembed_version al fingerprint (2026-07-03)

## Task
Fetta unica di R-vec-pool: aggiungere `fastembed.__version__` al fingerprint del vector
store, estendendo il guard esistente (R-vec-2b). Scope: SOLO il campo versione. Introspezione
pooling reale = fuori scope (decisione umana).

## Precheck
`fastembed.__version__` == `"0.8.0"` — accessibile in modo stabile e affidabile.

## Modifiche — modules/memory/vectors.py

### 1. Cattura versione a livello modulo (righe 68-73)
```python
try:
    import fastembed as _fastembed_mod
    _FASTEMBED_VERSION: str = str(_fastembed_mod.__version__)
except Exception as _e_fev:
    _FASTEMBED_VERSION = "unknown"
    log.warning("vector store: fastembed.__version__ non accessibile (%s) — fingerprint usa 'unknown'", _e_fev)
```
Fail-safe: se `__version__` non fosse accessibile, fingerprint usa `"unknown"` e il guard
degraderebbe ugualmente in modo corretto (confronto stringa).

### 2. Attributo istanza `self._fastembed_version`
Aggiunto in `__init__` dopo `self._embedder = None`. Fisso per tutta la vita dell'istanza.

### 3. `_read_fingerprint` — tipo restituito aggiornato
`Optional[Tuple[str, int]]` → `Optional[Tuple[str, int, Optional[str]]]`

La terza componente è `None` se `fastembed_version` è assente dalla tabella `metadata`
(DB scritto prima di questa modifica). `None` ≠ stringa vuota: distinzione intenzionale.

### 4. `_write_fingerprint` — scrive anche `fastembed_version`
Aggiunto `INSERT OR REPLACE INTO metadata ('fastembed_version', ?)` con `self._fastembed_version`.
Chiamato SIA alla creazione del DB SIA nel `ricostruisci_da_diario` (reindex).

### 5. Logica di confronto in `__init__`
Tre rami fail-closed (dopo unpack `stored_model, stored_dim, stored_fe_ver = fp`):

1. **`stored_fe_ver is None`** → "DB legacy: fastembed_version assente — esegui 'gas reindex'"
2. **model_id ≠ OR dim ≠ OR fastembed_version ≠** → "fingerprint mismatch ..."
   - Se solo fastembed_version diversa: `"fingerprint mismatch: DB fastembed='X' != 'Y' — esegui 'gas reindex'"`
   - Se model_id diverso: `"fingerprint mismatch: DB 'model_A' != configurato 'model_B' — esegui 'gas reindex'"`
3. **Tutto coincide** → guard OK, layer disponibile.

## Modifiche — tests/test_unit_kernel.py

### T39b e T39e aggiornati
I DB manuali ora includono `fastembed_version = '0.0.0-test-fake'` per avere un fingerprint
completo (senza, cadrebbero nel path "legacy" invece di "mismatch").

### T39h-T39k aggiunti (4 nuovi test)
- **T39h**: fingerprint scritto include la versione fastembed corrente.
- **T39i**: fastembed_version='0.0.0-test-fake' (model_id/dim corretti) → guard scatta,
  disable_reason contiene 'mismatch' e 'reindex'.
- **T39j**: DB legacy senza campo fastembed_version (model_id/dim corretti) → guard scatta,
  disable_reason contiene 'legacy' e 'reindex'.
- **T39k**: fingerprint completo e coincidente → available=True, nessun falso positivo.

## Verdetto revisore
**APPROVATO CON RISERVE** (review #42). Riserve risolte nello stesso commit:
1. `log.warning` nell'`except` del blocco `_FASTEMBED_VERSION` → applicato.
2. Commento schema SQL aggiornato a `(model_id, model_dim, fastembed_version)` → applicato.

## Risultati test
```
=== RIEPILOGO: 216 PASS, 0 FAIL ===
```

## Stato R-vec-pool
**CHIUSO**. Il guard copre ora: model_id + model_dim + fastembed_version.
Introspezione pooling reale = fuori scope (decisione umana).
Dopo ogni upgrade fastembed sul VPS: `gas reindex` (prassi obbligatoria, ora rafforzata dal guard).
