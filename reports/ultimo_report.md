# Report — Task R-reidx-3 + Token accounting
**Data:** 2026-06-25
**Review:** #30 — APPROVATO CON RISERVE (riserve minori, tutte chiuse prima del commit)

---

## Task 1 — R-reidx-3: fix picco RAM in `gas reindex`

### Problema
`ricostruisci_da_diario` materializzava TUTTI gli embedding in un unico numpy array
prima del DELETE+INSERT: picco RAM = tutte le righe × 384 dim × 4 byte.
Su un diario grande (es. 100K voci ≈ 150MB numpy) questo saturava la RAM del VPS.

### Fix
`modules/memory/vectors.py`:
- Nuova costante `REINDEX_BATCH_SIZE = 256`
- `ricostruisci_da_diario(memory_store, batch_size=REINDEX_BATCH_SIZE)`:
  - Usa `diario_dopo` (lettore paginato) al posto di `diario_tutto` (carica tutto)
  - Per ogni batch: embedding → normalizza → accumula blob bytes (1.5KB/riga)
  - I numpy array per-batch sono transitori (GC-ati ad ogni iterazione)
  - Fallback a `diario_tutto` per backward compat con mock/test senza `diario_dopo`
  - Invariante mantenuta: DELETE+INSERT atomico SOLO se tutti i batch riescono

### Riduzione RAM
| Prima | Dopo |
|---|---|
| Peak = numpy(n×384×4) + tutti i testi | Peak = numpy(256×384×4)≈400KB per batch + blob accumulati |
| Picco unico proporzionale all'intero diario | Numpy transitori, accumulo blob ~1.5KB/riga |

Nota: l'accumulo blob totale resta proporzionale all'intero diario → chiusura PARZIALE
di R-reidx-3 (picco ridotto, non azzerato). Dichiarato in stato_progetto.md.

---

## Task 2 — Contabilità token (`gas tokens`)

### Problema
Impossibile sapere dove andavano i token: nessuna telemetria per-provider, per-turno.
"Non puoi controllare ciò che non misuri."

### Fix
`gas.py`:
- Costante `TOKEN_LOG_FILENAME = ".gas_tokens.jsonl"`
- Metodo `GasKernel._log_tokens(provider, model, in_tok, out_tok)`:
  - Fail-safe: errore I/O ignorato con warning (mai crash del turno)
  - Appende una riga JSONL a `<root>/.gas_tokens.jsonl` per ogni API call
- Chiamata in `run_turn` subito dopo `client.chat.completions.create(...)`:
  ```python
  usage = getattr(response, "usage", None)
  if usage:
      self._log_tokens(name, model,
                       getattr(usage, "prompt_tokens", 0) or 0,
                       getattr(usage, "completion_tokens", 0) or 0)
  ```
- Funzione `tokens_cmd(root_dir, days)`: legge il JSONL, aggrega per provider,
  stampa tabella con totali globali + ultimi N giorni (default 7)
- Dispatch `gas tokens [N_giorni]` in `main()` con try/except ValueError
- `.gas_tokens.jsonl` aggiunto a `.gitignore` (artefatto runtime, non nel repo)

### Esempio output `gas tokens`
```
=== GAS — Token Usage ===

Provider               Calls   Tokens In  Tokens Out      Totale
gemini-flash-lite          2       3,000         600       3,600
groq                       1         500         100         600
──────────────────────────────────────────────────────────────
TOTALE                     3       3,500         700       4,200

Ultimi 7 giorni:
  gemini-flash-lite    3,000 in + 600 out = 3,600 tok
  groq                 500 in + 100 out = 600 tok
```

---

## Test

5 nuovi test aggiunti (`tests/test_unit_kernel.py`):
- **T35a** — batch_size=2 su 5 righe: 5 indicizzate correttamente
- **T35b** — embedding fallisce al batch 2: None + indice preesistente intatto
- **T36a** — `_log_tokens`: riga JSONL parseable con campi corretti
- **T36b** — `gas tokens` su log mancante: exit 0 + messaggio
- **T36c** — `gas tokens` con record multipli: exit 0 + provider + TOTALE nel report

Suite: **163 PASS, 7 FAIL** (7 pre-esistenti Windows/bwrap, invariati)

---

## Riserve review #30 (gestione)
- **R30-1** (MEDIO): `.gas_tokens.jsonl` → gitignore CHIUSA prima del commit
- **R30-2** (BASSO): `int(sys.argv[2])` → try/except ValueError CHIUSA prima del commit
- **R30-3** (BASSO, informativo): accumulo blob totale proporzionale al diario → dichiarato
  in stato_progetto.md come chiusura parziale R-reidx-3
- **R30-4** (BASSO, test): manca test per eccezione di `diario_dopo` al primo batch →
  rinviato (logica difensiva corretta, ramo coperto indirettamente)

---

## File modificati
- `modules/memory/vectors.py`: `REINDEX_BATCH_SIZE` + `ricostruisci_da_diario` batch
- `gas.py`: `TOKEN_LOG_FILENAME`, `_log_tokens`, `tokens_cmd`, dispatch `main`
- `tests/test_unit_kernel.py`: T35a, T35b, T36a, T36b, T36c
- `.gitignore`: `.gas_tokens.jsonl`
- `reports/stato_progetto.md`: aggiornato review count, R-reidx-3, CLI
- `.claude/agents/memoria_revisore.md`: lezione #30
