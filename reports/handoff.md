# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-24 — Auto-apprendimento Fetta 1: fonte + turno_id + turno_fine nel diario

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #98 (https://github.com/Gasss23/Gas/pull/98).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Migrazione diario (fonte + turno_id)**: `FATTA`
  `_ensure_columns` in `store.py`: ALTER TABLE additivo, nullable, righe vecchie restano NULL, trigger immutabilità intatti.

- **Fetta 1 — append_diario con fonte/turno_id**: `FATTA`
  Firma aggiornata con parametri opzionali; INSERT aggiornato.

- **Fetta 1 — run_turn: turno_id uuid4 per turno**: `FATTA`
  `uuid.uuid4()` generato all'inizio di ogni `run_turn`; passato a ogni `_diario_log`.

- **Fetta 1 — riga turno_fine a fine run_turn**: `FATTA`
  `try/finally` wrappa l'intero corpo di `run_turn`; `_chiudi_turno()` scrive esattamente 1 riga per turno su ogni uscita (normale, eccezione, GeneratorExit, budget kill-switch).

- **Fetta 1 — turno_fine in DIARIO_NOISE_TIPI**: `FATTA`
  Aggiunto `"turno_fine"` al frozenset: non intasa `_memoria_pin`.

- **Fetta 1 — Fail-safe §9**: `FATTA`
  `_chiudi_turno` chiama `_diario_log` che ha early return su `memory=None` e `except Exception`. T64f verifica esplicitamente.

- **Fetta 1 — Test suite**: `FATTA`
  T64a–T64i: 9 nuovi test, tutti PASS. T20a/b/c aggiornati. Baseline: 318 PASS, 5 FAIL bwrap (F-mac-1, attesi).

- **Fetta 1 — E2E reale su copia DB**: `FATTA`
  Turno "quanto fa 6*7" su copia `.gas_memory.db`: righe id 21–22 con `turno_id` e `fonte='kernel'` conformi. Righe vecchie con NULL confermati.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 gas.py                             | 332 +++++++++++++++++++++----------------
 modules/memory/store.py            |  23 ++-
 reports/diff_sessione.md           |  20 ++-
 reports/handoff.md                 | 102 +++++++++---
 reports/stato_progetto.md          |   4 +-
 reports/ultimo_report.md           |  99 ++++++++---
 tests/test_unit_kernel.py          | 231 +++++++++++++++++++++++++-
 8 files changed, 602 insertions(+), 210 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
738b006 docs(fine-task): report auto-apprendimento fetta 1 — fonte+turno_id+turno_fine
eb9f7f1 feat(apprendimento-f1): fonte + turno_id + turno_fine nel diario
4329e72 chore(revisore): memoria review #103 — APPROVATO
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `eb9f7f1` tocca `gas.py`, `modules/memory/store.py`, `tests/test_unit_kernel.py`.

### VERDETTO REVISORE #103 — 2026-09-24

**VERDETTO: APPROVATO**

Elementi concreti esaminati:

1. `gas.py:1734-1735` — `finally: _chiudi_turno()` — Il `try/finally` che avvolge l'intero corpo di `run_turn()` garantisce la scrittura della riga `turno_fine` in TUTTI i percorsi di uscita: normale (`return` dopo yield final, che in un generatore causa `StopIteration` → `finally` prima della propagazione), `GeneratorExit` (consumer chiude il generatore a metà; `GeneratorExit` è `BaseException` e bypassa l'`except Exception` interno a riga 1716 ma il `finally` esterno lo intercetta), budget kill-switch (yield error + return). Il flag `_turno_fine_scritto` con guard idempotente previene doppia scrittura. La closure `_chiudi_turno` usa `nonlocal` SOLO per la variabile che scrive (`_turno_fine_scritto`); le altre variabili sono lette dall'enclosing scope senza `nonlocal` — pattern Python corretto. Esito: **ok**.

2. `modules/memory/store.py:391-393` — `ALTER TABLE diario ADD COLUMN fonte/turno_id` in `_ensure_columns` — Verifica della lezione #67 (trappola: `CREATE INDEX` sulla nuova colonna in `_SCHEMA` PRIMA di `_ensure_columns` → DB legacy in degrado). Confermato: `_SCHEMA` non contiene alcun `CREATE INDEX` su `fonte` o `turno_id`. Le colonne esistono solo dopo l'ALTER TABLE in `_ensure_columns`. Il test T64a copre esattamente il caso trappola. Esito: **ok**.

3. `gas.py:1711` (bonus) — `_turno_final = True` PRIMA di `yield {"type": "final", ...}` — Rischio esaminato: se il consumer chiude il generatore dopo il yield ma prima del `return`, `_chiudi_turno()` legge `_turno_final=True` e scrive `esito=ok`. Esito: **accettabile** — in CPython, `GeneratorExit` arriva solo a punti di yield; il flag è correttamente impostato prima dello yield.

Rischio esplicitamente escluso: prestazioni migrazione ALTER TABLE su DB di produzione con >100K righe. La migrazione è additiva e idempotente (guard `if "fonte" not in diario_cols`); prestazioni su DB grandi non misurate.

Guardrail §8: `for _ in range(10)` e `_get_window()` presenti e invariati. Nessun raw history slicing nel diff.

Guardrail §9: `_chiudi_turno()` → `_diario_log()` → early return su `memory=None` + `except Exception`. T64f testa memory=None. ✓

---

## §5 DELTA TEST DEL MOTORE

**Prima:** 294 PASS, 5 FAIL (baseline 2026-09-21 su macOS)
**Dopo:** 318 PASS, 5 FAIL (2026-09-24 su macOS)
**Delta:** +24 PASS, 0 nuovi FAIL

```
=== RIEPILOGO: 318 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed)
  FAIL: T11e run_command fa scattare lo snapshot
  FAIL: T12a comando in allowlist (wc) eseguito, output reale
  FAIL: T12c pipe non interpretata (niente shell)
  FAIL: T12e command substitution non eseguita (resta letterale)
```

I 5 FAIL sono bwrap macOS (F-mac-1): bwrap/namespace non disponibili su macOS. Documentati e attesi. Su Linux/WSL tutti i 323 test passano.

Test aggiornati per fetta 1: T20a, T20b, T20c (filtro turno_fine). Nuovi: T64a–T64i.

---

## §6 STATO CI

```
completed	success	docs(fine-task): report auto-apprendimento fetta 1 — fonte+turno_id+t…	CI	feat/apprendimento-f1-esiti	push	36050326948	50s	2026-09-24T19:45:46Z
completed	success	Merge pull request #97 from Gasss23/sonda/auto-apprendimento-recon	CI	main	push	35977300177	46s	2026-09-24T08:47:20Z
completed	success	docs(fine-task): handoff 2026-09-23 sonda auto-apprendimento	CI	sonda/auto-apprendimento-recon	push	35891353783	52s	2026-09-23T16:49:02Z
```

Mappatura commit → run:
- `738b006` (docs fine-task report) → run 36050326948 ✅ success (push del branch, testa il commit di testa)
- `eb9f7f1` (feat motore) → nessuna run diretta su questo SHA; incluso nell'albero del push successivo testato da run 36050326948
- `4329e72` (chore revisore) → nessuna run diretta su questo SHA; incluso nell'albero del push testato da run 36050326948

Nota: GitHub Actions crea una run per push, non per commit. I commit `eb9f7f1` e `4329e72` erano già stati pushati nel push di cui fa parte il successivo push di `738b006`, quindi l'albero testato da run 36050326948 contiene tutto il codice di sessione.

---

## §7 RISERVE APERTE

- **Rischio VPS (da review #103)**: migrazione ALTER TABLE su DB di produzione con >100K righe non misurata. Additiva e idempotente; rischio basso ma non verificato su grandi volumi.
