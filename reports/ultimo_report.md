# Report task: Auto-apprendimento Fetta 1 — fonte + turno_id + turno_fine

**Data:** 2026-09-24  
**Branch:** feat/apprendimento-f1-esiti  
**Commit:** eb9f7f1  
**Review:** #103 APPROVATO

---

## Obiettivo

Aggiungere la struttura dati minima per misurare l'esito di ogni turno nel diario:
- colonna `fonte` (chi ha prodotto l'evento) e `turno_id` (UUID del turno) al diario SQLite
- riga `turno_fine` scritta a fine di ogni `run_turn`, con esito deterministico (ok|parziale|ko), conteggio tool, provider usato, classe compito

Nessun LLM, nessuna lezione, solo struttura dati.

---

## Modifiche effettuate

### `modules/memory/store.py`

- `_ensure_columns`: aggiunta migrazione additiva per `fonte TEXT` e `turno_id TEXT` sul diario. I DB legacy vengono migrati al prossimo avvio (ALTER TABLE); le righe preesistenti restano con NULL (no backfill). I trigger di immutabilità (BEFORE UPDATE/DELETE) restano intatti dopo la migrazione.
- `append_diario(...)`: aggiunto `fonte: Optional[str] = None` e `turno_id: Optional[str] = None`; INSERT aggiornato di conseguenza.

### `gas.py`

- `import uuid` aggiunto agli import stdlib.
- `DIARIO_NOISE_TIPI`: aggiunto `"turno_fine"` → non intasa il `_memoria_pin` always-on.
- `_diario_log`: firma estesa con `fonte: Optional[str] = None` e `turno_id: Optional[str] = None`; passa i valori a `append_diario`.
- `run_turn`: wrappato l'intero corpo in `try/finally`. Variabili di tracking aggiunte all'inizio (`_turno_id`, `_turno_tool_n`, `_turno_tool_ko`, `_turno_provider`, `_turno_final`, `_turno_fine_scritto`, `_turno_classe`). Inner function `_chiudi_turno()` scrive esattamente 1 riga `turno_fine` su ogni uscita (normale, budget kill-switch, pipeline esausta, eccezione, GeneratorExit). Ogni `_diario_log` nel loop ora passa `fonte='kernel'` e `turno_id=_turno_id`.

**Regola esito:**
- `ok` = risposta finale prodotta E zero tool KO
- `parziale` = risposta finale prodotta MA ≥1 tool KO
- `ko` = nessuna risposta finale (provider falliti, limite iterazioni, eccezione, GeneratorExit)

---

## Test

**Suite kernel:** `python3 tests/test_unit_kernel.py`

```
318 PASS, 5 FAIL
```

- FAIL: T11c2, T11e, T12a, T12c, T12e — tutti bwrap macOS (F-mac-1, attesi, invariati)
- NUOVI: T64a–T64i tutti PASS (migrazione legacy, ok/parziale/ko-provider/GeneratorExit, memoria None, turno_id coerente, DIARIO_NOISE_TIPI, 2 turni = 2 turno_fine distinti)
- AGGIORNATI: T20a/b/c aggiornati per filtrare `turno_fine` dalle asserzioni sui tool → ora PASS

**E2E reale su COPIA del DB (mai l'originale):**

Turno "quanto fa 6*7" su copia `.gas_memory.db`:

```
{'id': 22, 'ts': '2026-09-24T19:40:34.599185+00:00', 'tipo': 'turno_fine',
 'fonte': 'kernel', 'turno_id': 'c2a8c4fe-d367-4087-bf63-883e9d9d6057',
 'descrizione': 'esito=ok ; tool=1 ; tool_ko=0 ; provider=gemini-flash-lite ; classe=semplice'}
{'id': 21, 'ts': '2026-09-24T19:40:33.570631+00:00', 'tipo': 'calcola',
 'fonte': 'kernel', 'turno_id': 'c2a8c4fe-d367-4087-bf63-883e9d9d6057',
 'descrizione': "expr='6*7' | [OK] 42"}
{'id': 20, 'ts': '2026-09-21T12:04:19.986558+00:00', 'tipo': 'calcola',
 'fonte': None, 'turno_id': None,
 'descrizione': "expr='3+3' | [OK] 6"}
```

Righe id 21–22: stesso `turno_id`, `fonte='kernel'`. Righe id ≤20: `fonte=NULL`, `turno_id=NULL` (nessun backfill, come atteso).

---

## Review #103

**APPROVATO** — punti esaminati:
1. `gas.py:1734-1735` — `finally: _chiudi_turno()` copre tutti i percorsi di uscita incluso GeneratorExit (BaseException, bypassa `except Exception` interno). Flag idempotente previene doppia scrittura. Pattern `nonlocal` corretto.
2. `modules/memory/store.py:391-393` — ALTER TABLE non in `_SCHEMA` (nessun indice su colonne nuove che precede `_ensure_columns`). T64a copre esattamente la trappola lezione #67.
3. `gas.py:1711` — `_turno_final = True` PRIMA di yield: comportamento accettabile in CPython.

---

## Stop gate rispettati

- Contatti/rubrica: NON toccati
- `_memoria_pin`: NON toccato (solo aggiunta di `"turno_fine"` a DIARIO_NOISE_TIPI)
- Tool `ricorda`: NON toccato
- Sanitizzazione anti-injection (riserva R2): NON toccata
- Retrieval/vettori: NON toccati
- Nessuna nuova dipendenza
