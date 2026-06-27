# ULTIMO REPORT — Sessione autonoma 2026-06-27 (fette B+C)

**Data**: 2026-06-27
**Review**: #36 (FETTA B) + #37 (FETTA C)
**CI finale**: run #28295087523 su `6cfd340` — **193 PASS, 0 FAIL** ✅

---

## DECISIONI UMANE RICHIESTE

Nessuna. Entrambe le fette rientrano nello scope assegnato e sono state approvate
dal revisore prima del commit.

## FETTA A — verifica CI (read-only)
CI su `c8dbe04` (commit di base): run #28293255763 → **SUCCESS**. Stop-gate A superato.

## FETTA B — chiusura riserva #35: test disable_reason tutti e 4 i rami

**Obiettivo**: ciascuno dei 4 rami di `VectorStore.disable_reason` coperto da un test
che asserisce `available=False` + discriminante del ramo nel valore di `disable_reason`.

**Modifiche a `tests/test_unit_kernel.py`:**
- **T39b-reason**: `"mismatch" in _vs39b.disable_reason` (ramo fingerprint mismatch) → PASS
- **T39c-reason**: `"legacy" in _vs39c.disable_reason` (ramo DB legacy) → PASS
- **T39f** (nuovo): `patch.object(VectorStore, '_connect', side_effect=OperationalError)` → `"sidecar" in disable_reason` → PASS
- **T39g** (nuovo): `patch.object(_vecmod, '_np', None)` + `_TextEmbedding=None` → `"deps" in disable_reason` → PASS

**Review #36**: APPROVATO — nessuna riserva.
**Commit**: `fc22295` — CI run #28294893550 → SUCCESS.

## FETTA C — R-tel-1: obbligatoria→WARN sui rung facoltativi

**Obiettivo**: openrouter/ollama (rung 4-5, facoltativi) loggano `reason="WARN"` invece di
`"KO"` nel `.gas_tokens.jsonl` quando falliscono con 402.

**Modifiche a `gas.py`:**
```python
_free_names = {r[0] for r in FREE_RUNGS}  # {"openrouter", "ollama"}
# nell'except block:
_ft_level, _ = _classify_provider_error(
    getattr(e, "status_code", None), str(e), name not in _free_names)
self._log_tokens(name, model, 0, 0, event="fallthrough", reason=_ft_level)
```

**Modifiche a `tests/test_unit_kernel.py`:**
- **T40**: openrouter 402 → `reason="WARN"` → PASS
- **T40b**: gemini-flash-lite 402 → `reason="KO"` → PASS

Output reale T40: `{'gemini-flash-lite': 'KO', 'gemini-flash': 'KO', 'groq': 'KO', 'openrouter': 'WARN'}`

**Review #37**: APPROVATO CON RISERVE (cosmetiche):
1. `reason` perde il testo descrittivo (conservato in gas_debug.log) — campo `detail` futuro
2. Ollama non assertito in T40 (GAS_OLLAMA_URL assente → skip in CI)

**Commit**: `6cfd340` — CI run #28295087523 → **193 PASS, 0 FAIL** ✅

---

## Delta test sessione

| Metrica | Prima | Dopo |
|---------|-------|------|
| Test CI Linux | 187 PASS, 0 FAIL | **193 PASS, 0 FAIL** |
| Test Windows  | 181 PASS, 6 FAIL | **183 PASS, 6 FAIL** |
| Nuovi test (FETTA B) | — | T39b-reason, T39c-reason, T39f, T39g |
| Nuovi test (FETTA C) | — | T40, T40b |

---

## Stato finding

- ✅ **Riserva review #35** — chiusa completamente (review #36)
- ✅ **R-tel-1** — chiuso (review #37)
