# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-06-27 — Sonda telemetria runtime per-provider (read-only)

---

## §0 DECISIONI UMANE RICHIESTE

**PROPOSTA AGGANCIO TELEMETRIA** (non implementata oggi — va discussa prima del build):

Il punto naturale è la coppia (successo / fallthrough) già presente in `run_turn` (gas.py:1317-1395). La proposta minimale:

1. **Nuovo file JSONL** `.gas_provider_stats.jsonl` — separato da `.gas_tokens.jsonl` per non mischiare semantica (token consumati vs eventi di routing).
2. **Schema record**:
   ```json
   {"ts": "ISO8601", "provider": "string", "event": "success|fallthrough", "motivo": "string"}
   ```
   `motivo` = stringa dell'eccezione troncata (già disponibile come `str(e)[:120]` in riga 1393); per i successi può essere `""`.
3. **Due soli punch point** in `run_turn` — nessun'altra modifica al motore:
   - **Successo** (riga 1378, dopo `yield {"type": "final", ...}`): log `success`
   - **Fallthrough** (riga 1393, dopo `logging.warning(...)`): log `fallthrough` + motivo raw
4. **`gas doctor`**: aggiungere una sezione "Telemetria" che legge `.gas_provider_stats.jsonl` e mostra per provider: `calls_ok`, `fallthrough`, `last_motivo`, `last_ts` — si innesta nel formato tabellare esistente senza rompere nulla.
5. **`gas tokens`** rimane invariato (è solo token/costo, non eventi di routing).

Nota: la distinzione quota/429 vs altri errori è fattibile usando `_classify_provider_error()` (già esistente a gas.py:189) applicata a `getattr(e, "status_code", None)` + `str(e)` — quella funzione è già testata e restituisce `"QUOTA"|"KO"`.

**Decidere prima del build:**
- File separato `.gas_provider_stats.jsonl` o campo aggiuntivo in `.gas_tokens.jsonl`?
- Successo = solo la `final` response, o anche ogni round-trip dentro il loop agentico?
- Esporre in `gas tokens` o solo in `gas doctor`?

---

## §1 SCOPE & ESITO FETTE

- **FETTA UNICA — Sonda read-only (5 domande)**: `FATTA`
  Nessuna modifica al motore. Nessun commit di file motore. Evidenza per ogni risposta.

---

## §2 GIT DIFF --STAT (sessione)

```
BASE=4a87bca
 .claude/commands/fine-task.md | 28 +++++++++++++++++++---------
 reports/diff_sessione.md      |  3 ++-
 reports/handoff.md            | 62 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/ultimo_report.md      |  8 ++++++++
 4 files changed, 92 insertions(+), 9 deletions(-)
```

(Nota: include anche il commit a845b28 della sessione precedente — BASE è 4a87bca = last handoff pre-sessione.)

---

## §3 GIT LOG --ONELINE (sessione)

```
46edca4 docs(stato): aggiornamento 2026-06-27 — fine-task range dinamico, opusplan→Sonnet default
a845b28 docs(fine-task): range sessione dinamico + esito fette + verifica FETTA 2
```

(Nota: il commit di questo handoff aggiungerà un terzo hash — visibile nel prossimo `git log` post-push.)

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore (gas.py/brains/modules/tests/ non toccati). Revisore non richiesto.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

---

## §6 STATO CI

```
completed	success	docs(handoff): sessione 2026-06-25 — env-config sprint + stima costi …	CI	main	push	28203924283	42s	2026-06-25T22:15:29Z
completed	success	﻿feat(tokens-cost): stima costi USD per provider in gas tokens	CI	main	push	28187957333	36s	2026-06-25T17:19:02Z
completed	success	feat(env-config): GAS_WINDOW_CHAR_CAP + GAS_MEMORY_PIN_SCAN + GAS_VEC…	CI	main	push	28187405067	40s	2026-06-25T17:09:18Z
```

Commit di questa sessione sono doc-only → CI non triggerata (nessun file motore). Ultimo run: success.

---

## §7 RISERVE APERTE

Nessuna.

---

## REFERTO SONDA — Risposte alle 5 domande

### D1. `gas tokens`: cosa persiste e DOVE?

**File:** `.gas_tokens.jsonl` (costante `TOKEN_LOG_FILENAME`, gas.py:113)

**Schema per-record** (gas.py:412-418):
```json
{"ts": "2026-06-27T10:00:00", "provider": "gemini-flash-lite", "model": "gemini-2.5-flash-lite", "in": 1234, "out": 56}
```
Campi: `ts` (ISO8601 UTC), `provider` (chiave del dizionario prezzi), `model` (slug modello), `in` (prompt tokens), `out` (completion tokens).

**Scritto da** `_log_tokens()` (gas.py:407) dopo ogni round-trip API con `usage != None` (gas.py:1351-1355), DENTRO il loop agentico a 10 iter → una riga per chiamata API, non per turno.

**Aggregazione** (`tokens_cmd`, gas.py:1737): raggruppa per `provider` → `turns` (call count), `in`, `out`, `cost` (USD da `_PROVIDER_PRICE_PER_MTok` statico, gas.py:118-124).

**Tiene già conteggi per-provider?** SÌ per token e call count (`turns`). NO per fallthrough, NO per quota events, NO per errori.

**La stima USD è l'unica superficie "costo"?** SÌ. `_PROVIDER_PRICE_PER_MTok` è un dizionario statico con (price_in, price_out) per milione token. Non c'è nessun'altra superficie di costo (niente budget cap, niente alert, niente quota tracking).

---

### D2. Cascata provider: dov'è e cosa loga al fallthrough?

**Funzione:** `run_turn()`, gas.py:1266. Il loop provider è gas.py:1317-1395.

**Struttura del loop:**
```
for name, env, url, model in providers:   # gas.py:1317
    if not os.environ.get(env): continue  # skip se chiave assente
    try:
        ... # loop agentico a 10 iter
    except Exception as e:
        logging.warning(f"Provider {name} ({model}) fallito: {e}")  # gas.py:1393
        continue  # → prossimo provider
yield {"type": "error", "content": "Pipeline esausta."}  # gas.py:1395
```

**Al fallthrough:** solo `logging.warning` in `gas_debug.log`. Nessun contatore persistente. Nessun campo nel JSONL.

**Segnale 429/quota vs altri errori:** `_classify_provider_error()` esiste (gas.py:189-206) e distingue 429→QUOTA, 402→WARN/KO, resto→KO. MA è usata SOLO dal `doctor` (gas.py:1439). In `run_turn` l'`except Exception` è GENERICA — nessuna discriminazione. Il codice HTTP dell'errore è disponibile via `getattr(e, "status_code", None)` (lo SDK OpenAI lo espone), ma non viene letto.

---

### D3. Punto d'aggancio naturale per la telemetria per-provider

**Due punch point, nessuno tocca diario/memoria:**

**A — Successo** (gas.py:1375-1379):
```python
elif msg.content:
    self._add_to_history("assistant", content=msg.content)
    self._save_history()
    yield {"type": "final", "content": msg.content}
    return  # ← qui: log success per `name`
```

**B — Fallthrough** (gas.py:1382-1394):
```python
except Exception as e:
    ...
    logging.warning(f"Provider {name} ({model}) fallito: {e}")
    continue  # ← qui: log fallthrough per `name` + motivo classificato
```

**Perché NON tocca diario né path memoria:** il diario è scritto da `_diario_log()` (gas.py:1366) per le tool call — è un layer separato. Il log token usa `open(log_path, "a")` diretto. Un terzo file `.gas_provider_stats.jsonl` usa lo stesso pattern, non interferisce.

**`_classify_provider_error()`** può essere riutilizzata al punto B per distinguere QUOTA/KO passando `getattr(e, "status_code", None)` e `str(e)`.

---

### D4. `gas doctor`: espone già qualcosa per-provider?

**SÌ.** Sezione 2 (gas.py:1415-1441): ping reale (`max_tokens=1`) per ciascuno dei 5 provider, con esito `OK|QUOTA|KO|WARN` e dettaglio.

**Formato output tabellare** (gas.py:1651):
```
[ESITO] Sezione    Voce                 Dettaglio
[OK   ] Provider   gemini-flash-lite    123 ms
[OK   ] Provider   gemini-flash         98 ms
[OK   ] Provider   groq                 210 ms
[WARN ] Provider   openrouter           assente (opzionale: rung free non configurato)
[OK   ] Provider   ollama               assente (opzionale...)
```

**Struttura interna:** lista `results` di dict `{sezione, voce, esito, dettaglio}` (gas.py:1402-1405), stampata in loop. Una nuova sezione "Telemetria" può aggiungersi allo stesso `results` senza modificare la struttura.

**Cosa manca per-provider:** call count runtime, fallthrough count, ultimo motivo di fallback, ultima ts di evento.

---

### D5. Qualcosa misura il consumo di quota free-tier?

**NO.** Confermato. `openrouter` e `ollama` sono in `_PROVIDER_PRICE_PER_MTok` con `(0.0, 0.0)` (gas.py:122-123): contribuiscono 0 al costo stimato. Il `doctor` fa un ping reale al provider free (gas.py:1449-1452, `_probe_free_model`) per verificare che il modello esista e supporti i tool — ma non interroga la quota residua. Nessuna API pubblica di OpenRouter espone la quota residua del free tier in modo machine-readable. L'unica proxy osservabile è la frequenza dei 429 nei fallthrough — che è esattamente ciò che la telemetria proposta in D3 cattura indirettamente.
