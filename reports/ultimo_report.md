# Report — 2026-06-24 — CI-4: verifica skip T9a/T9c

## Task

Rendere verde la CI gestendo onestamente T9a/T9c (falliscono in CI per assenza API key
Gemini/Groq sul runner). Fix atteso: skip CONDIZIONALE su assenza env var, con reason esplicita.
NON toccare T11/T12/T13d2 (bwrap) né T26b (WinError32). Invocare revisore sul diff prima del commit.

---

## DECISIONI UMANE RICHIESTE

Nessuna — ma vedere §Stato CI: CI-4 era già chiusa, CI va verificata su GitHub Actions
per confermare che il green sia effettivo dopo `089b061`.

---

## Esito

**Il task CI-4 era già completato in `089b061` (sessione precedente, 2026-06-24 18:51).**

### Verifica codice (ispezione lines 145–161, tests/test_unit_kernel.py)

Il fix è in place dall'inizio di questa sessione:

```python
_has_live_keys = bool(os.environ.get("GEMINI_API_KEY") and os.environ.get("GROQ_API_KEY"))
if _has_live_keys:
    check("T9a ogni provider cappato a 10 iterazioni", ...)
else:
    skip("T9a ogni provider cappato a 10 iterazioni",
         "richiede API key live (GEMINI_API_KEY, GROQ_API_KEY), skip in CI")
...
if _has_live_keys:
    check("T9c storia salvata su disco nella root temporanea", ...)
else:
    skip("T9c storia salvata su disco nella root temporanea",
         "richiede API key live (GEMINI_API_KEY, GROQ_API_KEY), skip in CI")
```

### Verifica suite locale (venv\Scripts\python tests\test_unit_kernel.py)

Output grezzo (righe rilevanti):

```
[SKIP] T9a ogni provider cappato a 10 iterazioni — richiede API key live (GEMINI_API_KEY, GROQ_API_KEY), skip in CI
[PASS] T9b loop infinito assorbito senza crash, pipeline esausta dichiarata — tool_res=0 errori=1
[SKIP] T9c storia salvata su disco nella root temporanea — richiede API key live (GEMINI_API_KEY, GROQ_API_KEY), skip in CI

=== RIEPILOGO: 158 PASS, 7 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed)
  FAIL: T11e run_command fa scattare lo snapshot
  FAIL: T12a comando in allowlist (wc) eseguito, output reale
  FAIL: T12c pipe non interpretata (niente shell)
  FAIL: T12e command substitution non eseguita (resta letterale)
  FAIL: T13d2 os_with_fallback + sandbox assente -> esegue (sandbox applicativa)
  FAIL: T26b backup: copia leggibile + rotazione ultime N + retention pura
```

**Conclusione**: T9a → [SKIP], T9c → [SKIP]. I 7 FAIL rimanenti sono TUTTI fuori scope
(bwrap su Windows: T11c2, T11e, T12a, T12c, T12e; WinError32: T13d2; file locking Windows: T26b).

### Analisi CI (linux + bwrap)

In CI (ubuntu-latest, bwrap disponibile, zero API key):
- T9a: `_has_live_keys = False` → `skip()` → non in FAIL ✓
- T9b: Pipeline esausta con cascade vuota (0 provider) → PASS ✓
- T9c: `_has_live_keys = False` → `skip()` → non in FAIL ✓
- T11c2, T11e, T12a, T12c, T12e: bwrap disponibile su Linux → PASS atteso ✓
- T13d2: `wc` disponibile su Linux, no WinError2 → PASS atteso ✓
- T26b: nessun file locking su Linux → PASS atteso ✓

**CI prevista VERDE dopo `089b061`.**

### Revisore

Non invocato: questa sessione NON modifica tests/, gas.py, brains/, modules/.
Nessun diff di motore su cui invocare il gate.

---

## Anomalie

Il task era già completato ma è stato ri-assegnato come se fosse aperto. Probabile causa:
la sessione precedente non ha potuto verificare direttamente il verde su GitHub Actions
(gh CLI non disponibile) e il task era rimasto nello stato "chiuso per rapporto" ma senza
conferma visiva del verde. **Azione raccomandata**: aprire GitHub Actions sulla repo
Gasss23/Gas e verificare che la run su `089b061` (o successiva) sia verde.
