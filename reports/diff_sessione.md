# 🔀 DIFF DI SESSIONE — 2026-06-18 (R-crm-1 refactor: identità su chiave_norm separata)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni sessione.

## Tema
R-crm-1 RIFATTO: normalizzazione chiavi contatti spostata a colonna `chiave_norm` separata
(identità) con `chiave` = valore as-entered, più NFKC. Scelta esplicita dell'utente dopo che
ho segnalato che R-crm-1 era già chiuso in forma "normalizza-in-place". Review #22 APPROVATO
CON RISERVE.

## File toccati

- **`modules/memory/store.py`** (motore):
  - `import unicodedata`; nuova eccezione `ChiaveNormCollisione`.
  - `normalizza_chiave`: + NFKC prima di collapse-whitespace/lower (idempotente, fail-safe).
  - Schema `contatti`: `chiave` non più UNIQUE (as-entered) + nuova colonna `chiave_norm`.
  - `_ensure_columns`: migrazione additiva `chiave_norm` (ALTER + backfill + rilevamento
    collisioni → `ChiaveNormCollisione` se duplicati storici, altrimenti indice UNIQUE).
  - `__init__`: `self.collisione_chiave_norm`; cattura `ChiaveNormCollisione` → `available=False`.
  - `upsert_contatto`: INSERT chiave (as-entered) + chiave_norm, `ON CONFLICT(chiave_norm)`,
    update non tocca `chiave`.
  - `_risolvi_canonico` / `get_contatto_per_chiave`: lookup su `chiave_norm`.

- **`modules/memory/__init__.py`** (motore): esporta `ChiaveNormCollisione`.

- **`tests/test_unit_kernel.py`** (test): T23a/T23f/T28b aggiornati al nuovo contratto
  (`chiave`→`chiave_norm`); aggiunti T29a-d (NFKC, as-entered, migrazione pulita, migrazione
  con collisione). Suite **135→139, 0 FAIL**.

- **`.claude/agents/memoria_revisore.md`** (doc): 3 lezioni datate 2026-06-18 (revisore).

- **`reports/stato_progetto.md` / `reports/ultimo_report.md` / `reports/diff_sessione.md`**
  (doc): aggiornati a fine task; nuovo finding **R-crm-norm-2**.

## Cosa NON è cambiato
`gas.py` INVARIATO (`_trova_contatto` già normalizzava l'haystack). Invarianti motore
(`_get_window`/`_cap_window_chars`/`for _ in range(10)`/sandbox/snapshot/immutabilità diario)
intatte. Nessun merge/dedup distruttivo: i duplicati storici in collisione fermano la
migrazione (decisione umana).

## Commit della sessione
- `ca08df7` — feat(memory): R-crm-1 identità su chiave_norm separata + NFKC (review #22)
- (doc) — commit dedicato di report + memoria revisore (hash stampato a fine task)
