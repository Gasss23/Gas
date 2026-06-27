# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-06-27 — Sonda telemetria per-provider (read-only)

---

## §0 DECISIONI UMANE RICHIESTE

1. **Approvare punto d'aggancio telemetria fallthrough**: estendere `_log_tokens` con campi opzionali `event` + `reason` (retrocompatibili) e loggare il fallthrough nell'`except` di `run_turn` (gas.py:1382-1394). Richiede un commit motore → revisore obbligatorio prima del build.
2. **Opzione A vs B per il file di log**: usare lo stesso `.gas_tokens.jsonl` con campo `event` discriminante (A, raccomandato — reader già esistente, meno file) oppure un file separato `.gas_provider_events.jsonl` (B — più pulito concettualmente, reader separato).

---

## §1 SCOPE & ESITO FETTE

- **FETTA UNICA — Sonda read-only (5 domande)**: `FATTA`
  Tutte le 5 domande risposto con evidenza (path + righe di codice). Nessuna modifica al motore, nessun commit motore, revisore non richiesto.

---

## §2 GIT DIFF --STAT (sessione)

```
(nessun commit di sessione prima della scrittura di questo handoff — sonda read-only)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
(nessun commit di sessione prima della scrittura di questo handoff — sonda read-only)
```

Nota: il commit di questa sessione sarà quello che contiene i tre file di report (ultimo_report.md, handoff.md, diff_sessione.md).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/ in questa sessione.

---

## §6 STATO CI

```
completed	success	docs(handoff): chiusura sessione 2026-06-27 — fix fine-task + stato +…	CI	main	push	28271556910	38s	2026-06-26T23:46:26Z
completed	success	docs(sonda): telemetria per-provider — referto 5 domande + proposta a…	CI	main	push	28270251924	41s	2026-06-26T23:07:40Z
completed	success	docs(stato): aggiornamento 2026-06-27 — fine-task range dinamico, opu…	CI	main	push	28270035841	35s	2026-06-26T23:01:58Z
```

Ultimo run: success. Nessun run di questa sessione (solo report, nessuna modifica al motore).

---

## §7 RISERVE APERTE

Nessuna riserva da revisore (nessuna modifica motore).

**Finding nuovi emersi dalla sonda:**

1. **Distinzione 429 vs altri errori assente a runtime** (gas.py:1382-1394): `_classify_provider_error` esiste ed è corretta, ma è usata solo in `doctor()`. Nel loop `run_turn` tutti gli errori — quota, rete, 400 — finiscono nel `continue` senza distinzione né contatore. Conseguenza: il log `.gas_tokens.jsonl` non registra i fallthrough, quindi `gas tokens` mostra solo il provider che ha effettivamente risposto, non la cascata reale.

2. **Quota free-tier non misurabile** (D5): nessuna superficie espone il consumo rispetto al tetto. Il 429 segnala l'esaurimento ma non lo anticipa. Questo è atteso per ora (quota volatile, non hardcodarla) ma va considerato se si vuole un alert proattivo.

3. **Punto d'aggancio minimale identificato** (D3): l'intervento è chirurgico — due righe nel `except` di `run_turn` + campi opzionali in `_log_tokens`. Non tocca diario, MemoryStore, né schema SQLite. Pronto per il build nella prossima sessione se §0 viene approvato.

---

## §8 RISPOSTE ALLE 5 DOMANDE (verbatim)

### D1 — `gas tokens`: persistenza e schema

**File:** `.gas_tokens.jsonl` (costante `TOKEN_LOG_FILENAME`, gas.py:113)
**Metodo:** `_log_tokens` (gas.py:407-423) — per round-trip API, non per turno (commento gas.py:410).
**Schema JSONL:** `{"ts", "provider", "model", "in", "out"}` — già per-provider (campo `provider` = chiave aggregazione in `tokens_cmd` gas.py:1771-1790).
**Cosa manca:** campo `event` (successo vs fallthrough), campo `reason`. La stima USD è l'unica superficie di costo (gas.py:1793).

### D2 — Cascata provider in run_turn

**Dove:** gas.py:1317-1394, ciclo `for name, env, url, model in providers:`.
**Fallthrough attuale:** solo `logging.warning(f"Provider {name} ({model}) fallito: {e}")` su `gas_debug.log` (gas.py:1393). Nessun contatore strutturato.
**Distinzione 429 vs altri:** ASSENTE a runtime. `_classify_provider_error` (gas.py:189-206) esiste ma è usata solo in `doctor()` (gas.py:1439-1441).

### D3 — Punto d'aggancio

Estendere `_log_tokens` con `event` (default `"call"`) e `reason` (opzionale). Loggare nell'`except` di `run_turn` (gas.py:1393):
```python
self._log_tokens(name, model, 0, 0)  # + event="fallthrough", reason=str(e)[:80]
```
NON tocca diario, MemoryStore, path memoria, schema SQLite.

### D4 — `gas doctor` per-provider

Sì: sezione "Provider" (gas.py:1419-1441), una riga per provider con ping di connettività.
Formato gas.py:1651: `[{esito:<5}] {sezione:<10} {voce:<20} {dettaglio}`.
La telemetria si aggiunge come nuova sezione "Telemetria" che legge `.gas_tokens.jsonl` — zero token, zero ping.

### D5 — Quota free-tier misurata oggi?

No. Confermato: nessuna superficie misura il consumo rispetto al tetto free-tier.
