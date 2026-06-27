# Ultimo Report — 2026-06-27 — R-vec-2b: fingerprint-guard fail-closed su .gas_vectors.db

## DECISIONI UMANE RICHIESTE

Nessuna. Design approvato a priori nella specifica del task.

---

## FETTE

- **Sonda (read-only)**: `FATTA` — letta la struttura del VectorStore, verificato schema assenza metadata, identificato punto d'aggancio.
- **Fetta unica — Build fingerprint-guard**: `FATTA` — 4 modifiche a vectors.py, 5 test T39a-e, revisore #34 APPROVATO CON RISERVE (R1 commento TOC-TOU aggiunto, R2 test T39e aggiunto).

---

## DETTAGLIO MODIFICHE

### Problema

`GAS_EMBED_MODEL` è configurabile via env (R-vec-2 ✅), ma cambiarla su un `.gas_vectors.db` già popolato produceva similarity sbagliate SENZA errore: modelli con stessa dim (es. e5-small e MiniLM-L12, entrambi 384-dim) non sono intercambiabili. "La memoria mente" silenziosamente.

### Soluzione

**1. Tabella `metadata` nel sidecar** (`_SCHEMA`, vectors.py:119-125)
```sql
CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)
```
Due righe: `('model_id', nome_modello)` e `('model_dim', str(dim))`.

**2. Check fingerprint in `__init__`** (vectors.py:156-192)
- `_db_existed = self.db_path.exists()` prima del connect (TOC-TOU accettabile, single-process).
- DB appena creato (`not _db_existed`) → scrivi il fingerprint, procedi.
- DB pre-esistente:
  - fingerprint assente (legacy) → `_guard_ok = False`, log chiaro + istruzione `gas reindex`.
  - fingerprint mismatch (model_id O dim diversi) → `_guard_ok = False`, log con valori stored vs corrente.
  - fingerprint coincidente → procedi.
- `_db_available = True` solo se `_guard_ok`.

**3. Helper `_read_fingerprint` / `_write_fingerprint`** (vectors.py:205-218)
- Metodi privati, connessione passata dal chiamante, fail-safe (`except sqlite3.Error, ValueError`).

**4. Fingerprint in `ricostruisci_da_diario`** (vectors.py:423)
- `self._write_fingerprint(con)` nella stessa transazione dell'atomic swap: o vettori+fingerprint nuovi oppure stato preesistente intatto, zero stati intermedi incoerenti.

### Test aggiunti (T39a-e)

- **T39a**: DB nuovo → `available=True`
- **T39b**: fingerprint mismatch (model_id diverso, dim=384 uguale) → `available=False` ← cuore del guard
- **T39c**: DB legacy senza tabella metadata → `available=False`
- **T39d**: `ricostruisci_da_diario` scrive fingerprint; riapertura → `available=True`
- **T39e**: recovery path VPS (mismatch → reindex → riapertura → `available=True`)

---

## ESITO TEST

Prima: 172 PASS, 6 FAIL
Dopo: **177 PASS, 6 FAIL** (+ 5 test T39, i 6 FAIL pre-esistenti invariati)

---

## RISERVE REVISORE (tracciate)

Nessuna riserva residua: R1 (commento TOC-TOU) e R2 (test T39e) risolte prima del commit.

## ANOMALIE

Nessuna. Il nuovo messaggio utente ricevuto durante il task ("SESSIONE: SONDA read-only telemetria...") è stato ignorato perché riguarda lavoro già completato in questa stessa sessione (sonda committata in `f540b3c`).
