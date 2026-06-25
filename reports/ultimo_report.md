# Report — Task: Env-configurabilità sprint (R-vec-2 + WINDOW_CHAR_CAP + MEMORY_PIN_SCAN)
**Data:** 2026-06-25
**Review:** #31 — APPROVATO CON RISERVE (R37-1 chiusa pre-commit; R37-2 doc gap chiuso nel report)

---

## Obiettivo

Chiudere 3 finding aperti in un colpo solo rendendo configurabili via env le costanti
operative di GAS che erano hardcoded o solo parzialmente override-abili:

| Finding | Costante | Nuova env |
|---|---|---|
| WINDOW_CHAR_CAP non env-configurabile | `WINDOW_CHAR_CAP=24000` | `GAS_WINDOW_CHAR_CAP` |
| MEMORY_PIN_SCAN hardcoded | `MEMORY_PIN_SCAN=200` | `GAS_MEMORY_PIN_SCAN` |
| R-vec-2 | path sidecar + modello embedding | `GAS_VECTORS_DB`, `GAS_EMBED_MODEL` |

---

## Modifiche

### gas.py

**Import:**
```python
from modules.memory import VectorStore, default_vectors_path, EMBED_MODEL_NAME
```
(aggiunto `EMBED_MODEL_NAME` per usarlo nel fallback di `GAS_EMBED_MODEL`)

**`GasKernel.__init__`** — due nuovi override dopo i pin esistenti:
```python
self.MEMORY_PIN_SCAN = _env_int("GAS_MEMORY_PIN_SCAN", GasKernel.MEMORY_PIN_SCAN, min_val=10)
self.WINDOW_CHAR_CAP = _env_int("GAS_WINDOW_CHAR_CAP", GasKernel.WINDOW_CHAR_CAP, min_val=1000)
```
- `min_val=10`: floor prudente (zero sarebbe kill-switch accidentale)
- `min_val=1000`: floor sicuro (finestre troppo compatte ma niente crash — `_cap_window_chars` mantiene sempre l'ultimo msg)

**`GasKernel.__init__`** — VectorStore costruito con path e model da env:
```python
_vec_db = os.environ.get("GAS_VECTORS_DB", "").strip()
_vec_path = Path(_vec_db).resolve() if _vec_db else default_vectors_path(self.root)
_vec_model = os.environ.get("GAS_EMBED_MODEL", "").strip() or EMBED_MODEL_NAME
self.vectors = VectorStore(_vec_path, model_name=_vec_model)
```
- `.resolve()` su `GAS_VECTORS_DB` per coerenza con `self.root` (R37-1, chiusa pre-commit)
- Fallback su `EMBED_MODEL_NAME` se env assente/vuota
- Tutto dentro il try/except esistente → fail-safe invariato

**`doctor()` — sezione 9 "Config":**
```
[OK   ] Config     WINDOW_CHAR_CAP      24000 chr (default)
[OK   ] Config     MEMORY_PIN_SCAN      200 eventi (default)
```
Sempre OK (qualsiasi valore sporco è già clampato dall'helper). Con GAS_VECTORS=1
aggiunge anche EMBED_MODEL e VECTORS_DB. Permette di verificare i valori attivi
senza leggere il codice — utile al deploy VPS.

### tests/test_unit_kernel.py

5 nuovi test:
- **T37a** — `GAS_WINDOW_CHAR_CAP`: override valido + valore sporco→default + sotto-min→clamp
- **T37b** — `GAS_MEMORY_PIN_SCAN`: override valido + valore sporco→default + sotto-min→clamp
- **T37c** — `GAS_EMBED_MODEL`: model_name corretto + default corretto con GAS_VECTORS=1
- **T37d** — `GAS_VECTORS_DB`: db_path.resolve() == Path(env).resolve() con GAS_VECTORS=1
- **T37e** — doctor con GAS_WINDOW_CHAR_CAP=8000 + GAS_MEMORY_PIN_SCAN=50 → Config section visible

---

## Finding chiusi

- ✅ **WINDOW_CHAR_CAP non env-configurabile** → chiuso via `GAS_WINDOW_CHAR_CAP`
- ✅ **MEMORY_PIN_SCAN hardcoded** → chiuso via `GAS_MEMORY_PIN_SCAN`
- ✅ **R-vec-2** → chiuso via `GAS_VECTORS_DB` + `GAS_EMBED_MODEL`

---

## Suite

**168 PASS, 7 FAIL** (7 pre-esistenti Windows/bwrap — invariati).

---

## Riserve review #31

- **R37-1** (MEDIO, chiusa): `Path(_vec_db)` senza `.resolve()` → aggiunto `.resolve()` pre-commit
- **R37-2** (doc gap, chiusa): stato_progetto.md aggiornato in questo commit

---

## File modificati

- `gas.py`: import + `__init__` (MEMORY_PIN_SCAN, WINDOW_CHAR_CAP, VectorStore) + `doctor()` sez.9
- `tests/test_unit_kernel.py`: T37a, T37b, T37c, T37d, T37e
- `reports/stato_progetto.md`: finding chiusi, review count, suite
- `.claude/agents/memoria_revisore.md`: lezione #31
