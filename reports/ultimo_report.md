# Report fine task — F1 R-crm-diario-rr (2026-07-16)

## DECISIONI UMANE RICHIESTE

1. **Merge PR #18** (`fix/diario-recursive-triggers` → main): CI verde ✅ — revisiona diff e approva il merge.

## Scope

F1 — chiusura varco INSERT OR REPLACE sul diario (`recursive_triggers`).  
Fetta unica: 1 riga in `modules/memory/store.py` + test T19f-rr in `tests/test_unit_kernel.py`.

## Esito fette

| Fetta | Descrizione | Esito |
|-------|-------------|-------|
| Unica — fix + test | `PRAGMA recursive_triggers = ON` in `_connect()` + T19f-rr | FATTA |

## Modifiche applicate

### 1. `modules/memory/store.py` — `MemoryStore._connect()` (riga 231)

```python
con.execute("PRAGMA recursive_triggers = ON")
```

Con il default SQLite (`recursive_triggers = OFF`), un `INSERT OR REPLACE` sulla PK del diario
eseguiva un DELETE implicito che NON attivava `diario_no_delete` → la riga veniva riscritta
silenziosamente (violazione "la memoria non mente", CLAUDE.md §6). Con ON, il DELETE implicito
attiva il trigger RAISE(ABORT) e l'operazione viene rigettata.

### 2. `tests/test_unit_kernel.py` — test T19f-rr (dopo T19f, riga 738)

Nuovo test che:
- usa `m._connect()` (NON connessione raw con pragma manuale): rimuovere il PRAGMA da
  `_connect()` farebbe fallire il test — la barriera è verificabile
- tenta `INSERT OR REPLACE INTO diario` su una PK esistente
- verifica ABORT (`sqlite3.IntegrityError: diario immutabile: DELETE vietato`)
- verifica che la riga originale sia rimasta intatta (contenuto invariato)

## Ricontrollo OR REPLACE sul diario (punto 3 scope — solo lettura)

- `unisci_contatti` (store.py:429): nessun INSERT sul diario (solo UPDATE su contatti). ✅
- `unisci_contatti_con_snapshot` (store.py:534–548): usa `INSERT INTO diario` puro, nessun OR REPLACE. ✅
- OR REPLACE nei moduli: SOLO in `modules/memory/vectors.py` su `metadata` e `vettori` (DB separato, nessun trigger di immutabilità coinvolto). ✅

**Nessun OR REPLACE sul diario trovato — nessun blocco DECISIONE UMANA RICHIESTA da questo ricontrollo.**

## Verdetto revisore (review #49) — INTEGRALE

> **APPROVATO CON RISERVE.** La fix di produzione è corretta e sicura. Una riserva non bloccante: il test che copre questa fix usa una connessione "artigianale" invece di passare per il metodo di produzione `_connect()`. Se qualcuno in futuro rimuovesse la riga di fix, il test non se ne accorgerebbe. Suggerisce di correggere il test nella stessa sessione (cambiando 3 righe).

**Riserva risolta in-session**: il test è stato aggiornato a usare `m._connect()` anziché una
connessione raw con pragma manuale. Il revisore ha anche verificato:
- PRAGMA sicuro per connessioni read-only (`backup_auto` usa `_connect()` ma non scrive sul diario) ✅
- OR REPLACE su `vettori`/`metadata` in `vectors.py` (DB separato, senza trigger) ✅
- FTS trigger `diario_fts_ai` (AFTER INSERT, non coinvolto dalla replace sulla PK) ✅

## git diff --stat (BASE=e7b4486)

```
 modules/memory/store.py   |   1 +
 reports/stato_progetto.md |   2 +-
 reports/ultimo_report.md  | 124 ++++++++++++++++++++++------------------------
 tests/test_unit_kernel.py |  30 +++++++++++
 4 files changed, 91 insertions(+), 66 deletions(-)
```

## Delta test suite

- PRE-fetta T19a–T19f: 6 PASS, 0 FAIL
- POST-fetta T19a–T19f-rr: **7 PASS, 0 FAIL** — delta +1 test (T19f-rr) ✅
- Nota: test bwrap strutturalmente rossi in Codespace — gate valido è la CI su GitHub.

## CI

- Run ID `29479725766` — **completed SUCCESS** su `fix/diario-recursive-triggers` (commit `894eb06`, 2026-07-16T07:22:51Z)
- Run ID `29479792397` — **completed SUCCESS** su `fix/diario-recursive-triggers` (commit `690c4e0`, 2026-07-16T07:24:02Z)

## Commit e PR

- Commit motore: `894eb06` (`fix(memory): chiude varco INSERT OR REPLACE sul diario (recursive_triggers)`)
- Commit doc: `690c4e0` (`docs(report): fine task F1 R-crm-diario-rr — recursive_triggers chiuso, PR #18`)
- Branch: `fix/diario-recursive-triggers`
- PR: https://github.com/Gasss23/Gas/pull/18

## Chiude

- **R-crm-diario-rr** (riserva R1 store.py commento riga 15, registrata 2026-07-14) ✅

## Proposte fuori scope

- **F6 — atomicità `.gas_history.json`**: scrittura JSON non atomica (individuata in sessione precedente). Candidata prossima fetta.
- **Hardening ulteriore diario**: retention, GDPR, archiviazione — in PARK in stato_progetto.md.
