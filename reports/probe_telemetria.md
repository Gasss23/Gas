# Probe: telemetria provider + observability gas doctor
**Data:** 2026-06-27  
**Scope:** READ-ONLY — nessuna modifica al motore. Solo mappatura del codice reale.  
**Ground truth git:** `adc7701` (HEAD — docs(revisore): lezioni sessione 2026-06-27)

---

## §DECISIONI UMANE RICHIESTE

**D1 — Bug probe vector store in doctor (B2):**  
`gas doctor` usa `default_vectors_path(root)` hardcoded per il probe del vector store (gas.py:1628), ignorando `GAS_VECTORS_DB` env. Se sul VPS si setta un path custom, il probe guarda un DB diverso da quello runtime → potenziale falso OK. Proposta: usare lo stesso path che usa `GasKernel.__init__` (gas.py:368-369). Fuori scope di questa sonda: richiede modifica a doctor.

**D2 — Motivo fingerprint-guard non visibile in doctor (B2):**  
Quando il guard disabilita il layer, il WARN di doctor è generico (`"deps assenti o sidecar corrotto"`). Il motivo specifico (mismatch modello, DB legacy, deps) è solo in `gas_debug.log`. Se si vuole visibilità fuori dal log (utile h24 unattended), serve propagare il `disable_reason` da VectorStore a doctor. Fuori scope di questa sonda: richiede modifica a VectorStore + doctor.

**D3 — Degrado solo-testo per-turno mai rilevato a runtime (B3):**  
Il finding R2 #5 è documentato come "rimandato" (gas.py:128). Non esiste oggi nessun punto nel runtime che si accorga se un turno produce risposta testuale quando ci sarebbero dovuti essere tool_calls. Da valutare se e quando implementare.

---

## ASSE A — gas tokens & telemetria provider

### A1. Cosa persiste `gas tokens` e dove?

**File:** `.gas_tokens.jsonl` — `TOKEN_LOG_FILENAME = ".gas_tokens.jsonl"` (gas.py:113)  
**Formato:** JSONL append-only, una riga per round-trip API (NON per turno utente).

**Schema (gas.py:415-424):**
```python
record = {
    "ts": "2026-06-27T12:00:00",  # UTC ISO 8601
    "provider": "gemini-flash-lite",  # nome provider nella cascata
    "model": "gemini-2.0-flash-lite",  # modello effettivo
    "in": 1200,   # token di input (int)
    "out": 300,   # token di output (int)
    "event": "call",  # "call" = risposta ricevuta; "fallthrough" = provider fallito
    "reason": "...",  # OPZIONALE, solo su event="fallthrough"
}
```

**`gas tokens` aggrega (gas.py:1818-1887):**
- Per `event="call"`: calls/turns, token in, token out, costo USD (tabella `_PROVIDER_PRICE_PER_MTok` gas.py:117-124, 5 provider)
- Per `event="fallthrough"`: count totale + count ultimi N giorni + last_reason
- Finestra temporale: default 7 giorni (override `gas tokens N`)

**`gas doctor` sezione Telemetria (gas.py:1658-1694):** legge lo stesso file e riporta per-provider `calls` + `fallthrough` count + ultimo motivo.

---

### A2. Dove vive la logica fallthrough della cascade e quando è osservabile?

**Funzione:** `GasKernel.run_turn()`, gas.py:1272  
**Punto unico** del fallthrough: gas.py:1388-1404

```python
# gas.py:1388-1404
except Exception as e:
    if name.startswith("gemini") and "400" in str(e)[:120]:
        # log diagnostico della sequenza payload
        ...
    logging.warning(f"Provider {name} ({model}) fallito: {e}")
    _, _ft_reason = _classify_provider_error(
        getattr(e, "status_code", None), str(e), True)
    self._log_tokens(name, model, 0, 0,
                     event="fallthrough", reason=_ft_reason)
    continue  # → prossimo provider nella cascade
```

Il `for name, env, url, model in providers:` (gas.py:1323) costruisce la lista ordinata dei provider; il `continue` avanza al successivo. Il blocco except a 1388 è **l'unico punto** in tutto il codebase dove un fallthrough viene registrato e la cascata avanza. Non esiste un secondo hook nascosto.

**Nota implementativa (commit 2eb0e30):** la chiamata `_log_tokens(..., event="fallthrough")` è stata aggiunta in quella posizione, rendendo il punto unico anche il punto unico di observability.

---

### A3. Conteggio per-provider già esistente?

**Sì, già implementato** (commit `2eb0e30`, feat(telemetria): fallthrough per-provider in .gas_tokens.jsonl).

**`gas tokens` (gas.py:1879-1887):**
```
Fallthrough (provider falliti → cascata al successivo):
  Provider             Tot  Ultimi 7gg  Ultimo motivo
  ──────────────────────────────────────────────────
  gemini-flash-lite      3           2  429: quota esaurita
```

**`gas doctor` (gas.py:1686-1691):**
```
[WARN ] Telemetria  gemini-flash-lite    calls=42, fallthrough=3, ultimo: 429: quota esaurita
[OK   ] Telemetria  groq                 calls=15, fallthrough=0
```

**Hook point per aggiunte future** (solo annotazione, non implementato): il punto naturale sarebbe un secondo argomento nella chiamata `_log_tokens` a gas.py:1359, per passare metriche aggiuntive (es. latenza, tentativo di retry) senza toccare la logica della pipeline.

---

### A4. Errori 429/quota distinguibili dagli altri?

**Sì.** La funzione `_classify_provider_error()` (gas.py:189-206) produce il campo `reason` nel JSONL:

```python
# gas.py:202-206
if status_code == 429 or "429" in txt:
    return ("QUOTA", "429: quota esaurita")
if (status_code == 402 or "402" in txt) and not obbligatoria:
    return ("WARN", "402: crediti esauriti (rung free opzionale)")
return ("KO", err_text[:60])
```

Nel JSONL il campo `reason` è il secondo elemento della tupla:
- `"429: quota esaurita"` → quota/rate-limit (distinguibile per prefisso)
- `"402: crediti esauriti (rung free opzionale)"` → crediti esauriti su rung opzionale
- `err_text[:60]` → errore generico (KO), testo libero troncato

**Caveat:** la distinzione è per string-matching sul campo `reason`, non su un campo strutturato separato. Sufficiente per osservabilità umana; da considerare se si costruisce alerting automatico.

---

## ASSE B — cosa espone `gas doctor` oggi

### B1. Sezioni/check completi di `gas doctor`

Elenco completo (gas.py:1407-1699), 11 sezioni:

| # | Sezione | Voci |
|---|---------|------|
| 1 | **API keys** | GEMINI_API_KEY, GROQ_API_KEY, OPENROUTER_API_KEY |
| 2 | **Provider** (ping max_tokens=1) | gemini-flash-lite, gemini-flash, groq, openrouter, ollama |
| 3 | **Paracadute** | modello free (OpenRouter metadata — function calling dichiarato?) |
| 4 | **File** | gas.py, CLAUDE.md, gas_identity.md, .gas_history.json |
| 5 | **Storia** | tool orfani, _get_window (parte da role:user?) |
| 6 | **Log** | gas_debug.log (dimensione, soglia 5 MB) |
| 7 | **Sandbox OS** | bwrap+namespace (esito + mode attivo) |
| 8 | **Snapshot** | ref totali, oggetti loose, snapshots.log |
| 9 | **Memoria** | .gas_memory.db (integrità, FTS5, backup), off-site bak, vector store |
| 10 | **Config** | WINDOW_CHAR_CAP, MEMORY_PIN_SCAN (+ EMBED_MODEL, VECTORS_DB se GAS_VECTORS=1) |
| 11 | **Telemetria** | per-provider da .gas_tokens.jsonl: calls + fallthrough + ultimo motivo |

---

### B2. Doctor riporta stato vector layer E motivo del disable?

**Risposta breve: riporta lo stato (available True/False) ma NON il motivo del disable.**

Il check in doctor (gas.py:1623-1639):
```python
# gas.py:1625-1637
if _env_flag("GAS_VECTORS"):
    _vs_probe = _VS(default_vectors_path(root))  # ← path hardcoded, ignora GAS_VECTORS_DB
    if _vs_probe.available:
        check("Memoria", "vector store", "OK",
              "dipendenze ok, sidecar apribile (GAS_VECTORS=1)")
    else:
        check("Memoria", "vector store", "WARN",
              "GAS_VECTORS=1 ma non disponibile (deps assenti o sidecar corrotto)")
```

**Il WARN è generico** — non distingue tra:
- fingerprint mismatch (modello cambiato)
- DB legacy senza fingerprint
- deps mancanti (fastembed/numpy assenti)
- corruzione SQLite

Il motivo specifico è emesso solo da `VectorStore.__init__()` via `log.warning(...)` (vectors.py:175-194), che finisce esclusivamente in `gas_debug.log`. **Fuori da gas_debug.log il disable è un silenzioso "non disponibile".**

**Bug aggiuntivo (D1):** doctor usa `default_vectors_path(root)` (gas.py:1628) invece del path configurato via `GAS_VECTORS_DB`. La sezione Config al punto 10 mostra il path configurato (gas.py:1655), ma il probe al punto 9 non lo usa. Sul VPS con path custom la sezione Config e il probe parlano di DB diversi.

---

### B3. Doctor riporta degrado solo-testo per-turno?

**No.** Il degrado solo-testo per-turno non è osservabile oggi né in doctor né in gas tokens.

Stato attuale (gas.py:126-131):
```python
# "il rilevamento a runtime del degrado a solo-testo è rimandato
# (falsi positivi, TASK B / R2 #5). Tutti i modelli della cascata sono
# oggi tool-capable; il warning è una rete dormiente che si accende se
# in futuro entra in cascata un modello senza tool."
```

Ci sono DUE check parziali:
1. **Check statico all'entrata del provider** (gas.py:1329-1331): `logging.warning` se `model` non è in `TOOL_CAPABLE_MODELS`. Si attiva sul registro statico, non sull'output reale. Va solo in gas_debug.log.
2. **Paracadute free** (gas.py:1453-1462, sezione B doctor): controlla i metadata OpenRouter per il SOLO modello free — verifica capacità DICHIARATA, non comportamento a runtime.

Il rilevamento che manca: controllare a runtime se `msg.content` arriva senza `msg.tool_calls` quando il turno ha già visto tool_calls in precedenza — quello è il "degrado effettivo per-turno" e non è implementato (gas.py:1381-1387 gestisce il `elif msg.content:` come finale legittimo, non come anomalia).

---

## Esito sonda

| ID | Domanda | Evidenza | Stato |
|----|---------|----------|-------|
| A1 | Schema `.gas_tokens.jsonl` | gas.py:113,415-424 | ✅ Chiaro |
| A2 | Punto unico fallthrough | gas.py:1388-1404 | ✅ Unico |
| A3 | Conteggio per-provider | gas.py:1665-1694, 1879-1887 | ✅ Già implementato |
| A4 | 429 distinguibile | gas.py:189-206, field `reason` | ✅ Sì (string prefix) |
| B1 | Sezioni doctor | gas.py:1407-1699 | ✅ 11 sezioni |
| B2 | Motivo disable vector | gas.py:1623-1639, vectors.py:175-191 | ⚠️ WARN generico + bug path |
| B3 | Degrado solo-testo | gas.py:126-131, 1329-1331 | ⚠️ Non implementato |
