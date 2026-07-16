# Report fine task — F1 R-crm-diario-rr (2026-07-16)

## DECISIONI UMANE RICHIESTE

1. **Merge PR #18** (`fix/diario-recursive-triggers` → main): CI deve diventare verde — revisiona diff e approva il merge.

## Scope

F1 — chiusura varco INSERT OR REPLACE sul diario (`recursive_triggers`).  
Fetta unica: 1 riga in `modules/memory/store.py` + test T19f-rr in `tests/test_unit_kernel.py`.

## Esito fetta

**FATTA**

## Modifiche applicate

### 1. `modules/memory/store.py` — `MemoryStore._connect()` (riga 231)

```python
con.execute("PRAGMA recursive_triggers = ON")
```

Aggiunta accanto agli altri PRAGMA di connessione. Con il default SQLite (`recursive_triggers = OFF`),
un `INSERT OR REPLACE` sulla PK del diario eseguiva un DELETE implicito che NON attivava
`diario_no_delete` → la riga veniva riscritta silenziosamente. Con ON, il DELETE implicito attiva
il trigger che fa RAISE(ABORT) e l'operazione viene rigettata.

### 2. `tests/test_unit_kernel.py` — test T19f-rr (dopo T19f, riga 738)

Test nuovo che:
- apre una connessione tramite `m._connect()` (NON una connessione raw con pragma manuale, per garantire
  che rimuovere il PRAGMA da `_connect()` faccia fallire il test)
- tenta `INSERT OR REPLACE INTO diario` su una PK esistente
- verifica ABORT (`sqlite3.IntegrityError: diario immutabile: DELETE vietato`)
- verifica che la riga originale sia rimasta intatta (contenuto invariato)

## Ricontrollo OR REPLACE sul diario (solo lettura)

- `unisci_contatti` (store.py:429): nessun INSERT sul diario (solo UPDATE su contatti). ✅
- `unisci_contatti_con_snapshot` (store.py:534–548): usa `INSERT INTO diario` puro, nessun OR REPLACE. ✅
- OR REPLACE nei moduli: presenti SOLO in `modules/memory/vectors.py` su tabelle `metadata` e `vettori` (non sul diario). ✅

**Nessun OR REPLACE sul diario trovato — nessun blocco DECISIONE UMANA RICHIESTA da questo ricontrollo.**

## Verdetto revisore (review #49) — INTEGRALE

> **APPROVATO CON RISERVE.** La fix di produzione è corretta e sicura. Una riserva non bloccante: il test che copre questa fix usa una connessione "artigianale" invece di passare per il metodo di produzione `_connect()`. Se qualcuno in futuro rimuovesse la riga di fix, il test non se ne accorgerebbe. Suggerisce di correggere il test nella stessa sessione (cambiando 3 righe).

**Riserva risolta in-session**: il test è stato aggiornato a usare `m._connect()` anziché una
connessione raw con pragma manuale. Il revisore ha verificato anche:
- PRAGMA sicuro per connessioni read-only (backup_auto usa `_connect()` ma non scrive sul diario) ✅
- OR REPLACE su `vettori`/`metadata` in `vectors.py` (DB separato, senza trigger) ✅
- FTS trigger `diario_fts_ai` (AFTER INSERT, non coinvolto dalla replace sulla PK) ✅

## git diff --stat reale (BASE=e7b4486)

```
 modules/memory/store.py      |  1 +
 tests/test_unit_kernel.py    | 30 ++++++++++++++++++++++++++++++
 2 files changed, 31 insertions(+)
```

## Delta test suite

- Isolato T19a–T19f-rr: **7 PASS, 0 FAIL** ✅
- Nota ambiente: test bwrap strutturalmente rossi in Codespace — gate valido è la CI su GitHub.

## Commit e PR

- Commit: `894eb06`
- Branch: `fix/diario-recursive-triggers`
- PR: aperta (vedi sezione DECISIONI UMANE RICHIESTE)

## Chiude

- **R-crm-diario-rr** (riserva R1 store.py commento riga 15, registrata 2026-07-14) ✅

## Proposte fuori scope (da valutare separatamente)

- **F6 — atomicità `.gas_history.json`**: scrittura JSON non atomica; è la prossima fetta piccola
  identificata nel último_report precedente.
- **Hardening ulteriore diario**: retention, GDPR, archiviazione — già in PARK in stato_progetto.md.
