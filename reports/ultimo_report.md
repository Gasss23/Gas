# Report C4a — Collegamento coda al loop

**Branch:** feat/cancello-c4a  
**Data:** 2026-10-03  
**Review:** #127 — APPROVATO CON RISERVE  
**Commit motore:** `766c0ee`  
**Commit revisore:** `cce2211`

---

## STATO ONESTO

- **C4a FATTO**: collegamento coda al loop in gas.py + fix R-c3-1b in store.py
- **C4b NON FATTO**: Telegram, read-back all'operatore, esecuzione post-approvazione
- **Deploy autonomo**: ANCORA VIETATO (manca C4b)

---

## PASSO 0 — Sonda

Nessun conflitto tra §4 del design e il prompt C4a. §4b descrive il turno suddiviso completo (incluso Telegram); C4a implementa solo la prima metà (parking nel DB + esito fisso). Il prompt era chiaro e coerente.

---

## PASSO 1 — R-c3-1b: fix expire_stale_approvals

**File:** `modules/memory/store.py:1601`

**Bug:** `WHERE stato = 'pending' AND ts_expiry <= now` non matcha le righe con `ts_expiry` testuale (es. `'mai'`). In SQLite, TEXT > REAL per ordinamento storage-class, quindi la condizione non scattava mai.

**Fix:** due UPDATE nella stessa transazione:
1. `WHERE stato = 'pending' AND typeof(ts_expiry) NOT IN ('real', 'integer')` → scade le corrotte con WARN
2. `WHERE stato = 'pending' AND ts_expiry <= now` → scade quelle normali

**Controprova:** T73h-bis verifica che con `ts_expiry = 'mai'` la condizione base non matchi (0 righe), poi che expire_stale_approvals restituisca n=1 e il DB riporti `stato='expired', risolto_da='timeout'`.

---

## PASSO 2 — Collegamento gas.py

**File:** `gas.py:1942` (stub C2 → C4a)

**Cambio:** per `IRREVERSIBLE` e `UNCERTAIN+contaminata`, il tool NON viene eseguito. Invece:
1. `enqueue_approval(tool_name, args, turno_id, azione_leggibile)` → UUID o None
2. Se UUID: `out = "Azione in attesa di approvazione umana (ID: <uuid>)."`
3. Se None (store non disponibile, enqueue lancia, o memory=None): diniego fail-closed
4. Diario: `pending id=<uuid>` senza args (regola F-diario-eco/args)

DENY e casi puliti invariati.

---

## TEST T74 (serie completa — SQLite vero, nessun mock)

| Test | Verifica | Esito |
|------|----------|-------|
| T73h-bis | R-c3-1b: ts_expiry TEXT → scaduto da expire | PASS |
| T74a | IRREVERSIBLE → tool non eseguito, pending in DB, "in attesa" | PASS |
| T74b | UNCERTAIN+contaminata → idem (write_file dopo ricorda) | PASS |
| T74c | UNCERTAIN pulita → eseguita come prima (regressione) | PASS |
| T74d | DENY invariato | PASS |
| T74e | enqueue lancia → diniego, tool non eseguito | PASS |
| T74f | store=None → diniego | PASS |
| T74g | grep: nessun residuo stub C2 in gas.py | PASS |
| F-c4a-dedup | finding misurabile: 3x stesso tool → 3 UUID distinti | PASS (misura) |

**T70f/T70g aggiornati:** `run_command` con `os_with_fallback` è IRREVERSIBLE → ora parcheggiato; test aggiornati al nuovo comportamento atteso.

**Suite finale:** 501 PASS, 5 FAIL (solo F-mac-1 bwrap macOS, invariati).  
**Pytest:** 227/227 PASS.

---

## RISERVE (non bloccanti per commit)

- **R-c4a-1** (minore): dedup coda non implementato. Loop 10-iter su IRREVERSIBLE può creare fino a 9 pending identiche per turno. Misurato, fuori scope C4a.
- **R-c4a-2** (cosmetica): UUID doppio nel diario — `pending id=X | [OK] ... (ID: X)`.

---

## FUORI SCOPE — NON FATTO

Telegram, read-back args all'operatore, firma/UUID/hash args, esecuzione post-approvazione, R-c3-2..5, dedup coda.
