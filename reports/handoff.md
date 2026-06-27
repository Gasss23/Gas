# Handoff sessione 2026-06-27 (sessione autonoma) — fette B+C: riserva #35 + R-tel-1

---

## §DECISIONI UMANE RICHIESTE

Nessuna. Entrambe le fette rientrano nello scope assegnato.

**Riserve #37 da valutare in futuro (non urgenti):**
1. `reason` nel JSONL = livello puro ("WARN"/"KO"): perde il testo descrittivo dell'errore.
   Il testo sopravvive in `gas_debug.log`. Se si vorrà recuperarlo nel JSONL: aggiungere
   campo `detail` a fianco di `reason` in `_log_tokens`. Non urgente.
2. Ollama non testato in T40 (GAS_OLLAMA_URL assente in CI → skip). La logica è identica
   per derivazione da `_free_names`. Da assertire se/quando CI avrà GAS_OLLAMA_URL.

---

## §ESITO FETTE

| Fetta | Esito | Commit | CI |
|-------|-------|--------|----|
| A — verifica CI base | FATTA ✅ | read-only | run #28293255763 → SUCCESS |
| B — test disable_reason 4 rami | FATTA ✅ | `fc22295` | run #28294893550 → SUCCESS |
| C — R-tel-1 obbligatoria→WARN | FATTA ✅ | `6cfd340` | run #28295087523 → **193 PASS, 0 FAIL** |

---

## §SONDA

Non richiesta in questo task. La sonda della sessione precedente (probe telemetria + D1/D2)
è documentata in `reports/probe_telemetria.md`.

---

## §GIT DIFF --STAT (c8dbe04..HEAD)

```
 .claude/agents/memoria_revisore.md |  3 ++
 gas.py                             |  7 ++--
 tests/test_unit_kernel.py          | 70 ++++++++++++++++++++++++++++++++++++++
 3 files changed, 77 insertions(+), 3 deletions(-)
```

---

## §GIT LOG (commit sessione)

```
6cfd340 fix(runtime): R-tel-1 — obbligatoria→WARN sui rung facoltativi (review #37)
fc22295 test(vectors): disable_reason: chiudi riserva #35 — T39b/c/f/g (review #36)
```

(Base di sessione: `c8dbe04` — docs(stato): aggiornamento 2026-06-27)

---

## §DELTA TEST

| Metrica | Prima | Dopo |
|---------|-------|------|
| CI Linux | 187 PASS, 0 FAIL | **193 PASS, 0 FAIL** (+6) |
| Windows  | 181 PASS, 6 FAIL | **183 PASS, 6 FAIL** (+2 su Windows, +4 solo Linux) |

Nuovi test FETTA B: T39b-reason, T39c-reason, T39f, T39g
Nuovi test FETTA C: T40, T40b

---

## §VERDETTI REVISORE (INTEGRALI)

### Review #36 (FETTA B — tests/test_unit_kernel.py)

**VERDETTO: APPROVATO**

Correttezza tecnica dei discriminanti: verificato contro vectors.py.
- T39b-reason: `"mismatch"` corrisponde a `disable_reason = f"fingerprint mismatch: DB..."`. CORRETTO.
- T39c-reason: `"legacy"` corrisponde a `disable_reason = "DB legacy: fingerprint assente..."`. CORRETTO.
- T39f: `patch.object(VectorStore, '_connect', side_effect=OperationalError)` catturato da `except (sqlite3.Error, OSError)`. `"sidecar"` in `"init sidecar fallita: ..."`. CORRETTO.
- T39g: `patch.object(_vecmod, '_np', None)` e `_TextEmbedding=None` → `_embedder_available=False` → `"deps"` in `"deps embedding assenti..."`. CORRETTO.

Mock robusti: context manager ripristina stato, zero contaminazione. Conforme §5.
Nessuna modifica al codice produzione.

### Review #37 (FETTA C — gas.py + test T40)

**VERDETTO: APPROVATO CON RISERVE**

Fix logicamente corretto e minimale.
- `_free_names = {r[0] for r in FREE_RUNGS}` usa struttura ESISTENTE, zero nuove env/file/astrazione. CORRETTO.
- `name not in _free_names` come flag `obbligatoria`: semanticamente preciso. CORRETTO.
- `_ft_level` loggato come `reason`: T40/T40b PASSANO.

**Riserva 1 (cosmetica)**: `reason` perde il testo descrittivo. Il testo resta in gas_debug.log. Soluzione futura: campo `detail`.
**Riserva 2 (copertura)**: Ollama non assertito in T40 (GAS_OLLAMA_URL assente → skip).

---

## §STATO CI FINALE

**Run**: #28295087523
**Commit**: `6cfd340`
**Esito**: **SUCCESS — 193 PASS, 0 FAIL**

```
[PASS] T39f sqlite3.Error init sidecar → available=False + disable_reason contiene 'sidecar'
[PASS] T39g deps embedding assenti → available=False + disable_reason contiene 'deps'
[PASS] T40 openrouter (facoltativo) 402 → reason='WARN' nel JSONL fallthrough
[PASS] T40b gemini-flash-lite (obbligatorio) 402 → reason='KO' nel JSONL fallthrough
=== RIEPILOGO: 193 PASS, 0 FAIL ===
```
