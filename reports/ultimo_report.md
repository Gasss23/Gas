# Ultimo Report — 2026-06-27 — Sonda telemetria per-provider (read-only)

## DECISIONI UMANE RICHIESTE

1. **Approvare punto d'aggancio telemetria fallthrough**: estendere `_log_tokens` con campi opzionali `event` + `reason` (retrocompatibili) e loggare il fallthrough nell'`except` di `run_turn` (gas.py:1382-1394). Richiede commit motore → revisore obbligatorio prima del build.
2. **Opzione A vs B per il file di log**: usare lo stesso `.gas_tokens.jsonl` con campo `event` discriminante (A, raccomandato) oppure un file separato `.gas_provider_events.jsonl` (B). Raccomando A: meno file, reader già esistente.

---

## FETTE

- **FETTA UNICA — Sonda read-only (5 domande)**: `FATTA`
  Tutte e 5 le domande risposto con evidenza (path + righe). Nessuna modifica al motore. Nessun commit motore.

---

## RISPOSTE ALLE 5 DOMANDE

### D1 — `gas tokens`: cosa persiste e dove?

**File:** `.gas_tokens.jsonl` (costante `TOKEN_LOG_FILENAME`, gas.py:113)

**Metodo di scrittura:** `_log_tokens` (gas.py:407-423) — chiamato a ogni round-trip dentro il loop agentico, non per turno (commento esplicito gas.py:410).

**Schema riga JSONL:**
```json
{"ts": "2025-...T...", "provider": "gemini-flash-lite", "model": "gemini-2.5-flash-lite", "in": 123, "out": 45}
```
Campi: `ts` (UTC ISO-8601), `provider` (chiave aggregazione), `model` (slug), `in` (prompt_tokens), `out` (completion_tokens).

**Già per-provider?** Sì: il campo `provider` è la chiave di aggregazione in `tokens_cmd` (gas.py:1771-1790). Conta: turns (= call count), tokens in, tokens out, costo USD stimato.

**Cosa manca:** nessun campo `event` che distingua successo da fallthrough; nessun campo `reason`; nessun contatore di provider skippati. La stima USD (gas.py:1793) è l'unica superficie di costo.

---

### D2 — Cascata provider (fallback in run_turn)

**Dove:** `run_turn`, gas.py:1266, ciclo `for name, env, url, model in providers:` (gas.py:1317-1394).

**Struttura:** due liste di provider assemblate in base a `classifica_compito` (gas.py:1305-1315), con rung gratuiti sempre in coda. Ogni provider fallisce con `except Exception as e: ... continue` (gas.py:1382-1394).

**Log attuale del fallthrough:** solo `logging.warning(f"Provider {name} ({model}) fallito: {e}")` su `gas_debug.log` (gas.py:1393). Nessun contatore strutturato nel `.gas_tokens.jsonl`.

**Distinzione 429 vs altri errori a runtime:** ASSENTE in `run_turn`. La funzione `_classify_provider_error` (gas.py:189-206) classifica 429→QUOTA, 402→WARN/KO ma è usata SOLO nel `doctor()` (gas.py:1439-1441), non nel loop runtime. A runtime tutti gli errori finiscono indistintamente nel `continue`.

---

### D3 — Punto d'aggancio per {successi, fallthrough, ultimo_motivo}

**Aggancio minimale — senza toccare diario né path della memoria:**

1. Estendere `_log_tokens` (gas.py:407-423) con due campi opzionali retrocompatibili: `event` (default `"call"`) e `reason` (default assente). I record esistenti restano validi — `tokens_cmd` usa già `.get()` fail-safe.

2. Aggiungere log nell'`except` del loop provider (gas.py circa riga 1393):
   ```python
   logging.warning(f"Provider {name} ({model}) fallito: {e}")
   self._log_tokens(name, model, 0, 0)  # + event="fallthrough", reason=str(e)[:80]
   continue
   ```

3. `tokens_cmd` e `doctor` separano i record per `event`: `"call"` → successi, `"fallthrough"` → count + `reason` per l'ultimo motivo.

**NON tocca:** `.gas_memory.db`, `MemoryStore`, path del diario, schema SQLite.

---

### D4 — `gas doctor` espone già qualcosa per-provider?

**Sì.** Sezione "Provider" (gas.py:1419-1441): una riga per provider con esito del ping di connettività.

Formato (gas.py:1651): `[{esito:<5}] {sezione:<10} {voce:<20} {dettaglio}`

Esempio reale:
```
[OK   ] Provider    gemini-flash-lite    150 ms
[QUOTA] Provider    groq                 429: quota esaurita
[WARN ] Provider    openrouter           assente (opzionale: rung free non configurato)
```

**Come ci si incastra la telemetria:** dopo il blocco "Provider" esistente, aggiungere una sezione "Telemetria" che legge `.gas_tokens.jsonl` e mostra per provider: calls totali, fallthrough count, ultimo motivo. Zero token, zero ping — lettura file locale.

---

### D5 — Qualcosa misura il consumo di quota free-tier oggi?

**No.** Né `gas doctor` né `gas tokens` interrogano le API di quota. `doctor` classifica 429 come QUOTA se ricevuto nel ping, ma non sa quanto della quota è stata consumata in precedenza. `tokens_cmd` conta i token ma non li confronta con alcun tetto. Confermato: nessuna misura del consumo free-tier.

---

## ANOMALIE

Nessuna anomalia rilevata. Sonda completamente read-only.
