# Memoria FASE 2 — Backup automatico del DB (anti auto-corruzione)

**Data:** 2026-06-17
**Commit motore:** `cb99d1c` (revisore #19 — APPROVATO senza riserve bloccanti)
**Commit doc:** vedi sotto (stampato a fine task)
**Suite:** **128/128, 0 FAIL** (era 123)
**Scope:** rete di sicurezza del dato più prezioso del sistema (`.gas_memory.db`).
Item di roadmap CLAUDE.md §10 FASE 2 ("Backup della memoria").

---

## COSA È STATO FATTO

Il DB di memoria è il dato MENO rimpiazzabile di Gas (mesi di relazioni coi lead,
non ricostruibili come il codice) e la "macchina del tempo" snapshot NON lo copre
(fotografa solo git; il DB è gitignorato di proposito). Mancava una difesa
automatica dall'**auto-corruzione**. Aggiunta ora.

### `modules/memory/store.py`
- **`integrity_check() -> (bool, str)`**: verifica via `PRAGMA quick_check`.
  Fail-safe §9: è una diagnosi, NON solleva mai (try/except su `sqlite3.Error`/
  `OSError`).
- **`backup()` esteso**: dopo la copia nativa coerente (`src.backup(dst)`) applica
  la **rotazione** (tiene gli ultimi `keep`, default `DEFAULT_BACKUP_KEEP=10`) in
  un try/except SEPARATO (un fallimento della rotazione non invalida la copia
  appena fatta). Timestamp con **microsecondi** (`%H%M%S_%fZ`) → niente collisioni
  tra copie ravvicinate.
- **`_backup_retention(files, keep) -> (tieni, scarta)`**: politica PURA e
  testabile, con guardia `keep<=0` (kill-switch, stessa classe di `SNAPSHOT_KEEP`).
- **`_backup_files` / `ultimo_backup`**: elenco ordinato + copia più recente, per
  diagnosi e throttling.
- **`backup_auto(min_interval_sec)` THROTTLED**: copia SOLO se l'ultimo backup è più
  vecchio di `min_interval_sec` **E** l'integrità è OK. Un DB corrotto NON viene mai
  copiato sopra i backup buoni (così la rotazione non sfagocita le copie sane).

### `gas.py`
- **`_memoria_backup_auto()`**: fail-safe §9 (memoria `None` → return;
  `except Exception` → warning nella scatola nera, il turno PROSEGUE). Chiamato
  **UNA volta per turno** in `run_turn` dopo `_memoria_pin()`, FUORI dal
  `for _ in range(10)`. Codice fidato in-process → niente sandbox/snapshot.
- **Override env**: `GAS_MEMORY_BACKUP_EVERY_SEC` (default 6h) e
  `GAS_MEMORY_BACKUP_KEEP` (default 10), via `_env_int` con `min_val=0` (kill-switch).
- **`doctor` sezione 8 "Memoria"**: integrità (`quick_check`) + stato FTS5 + età/
  numero dei backup. Apre il DB SOLO se esiste (non lo crea come effetto collaterale
  della diagnosi). **ZERO token** (solo SQLite/glob/stat locali).

### `tests/test_unit_kernel.py` — T26a-e (zero token)
- **T26a** integrità: DB sano → `(True,'ok')`; file corrotto su disco → `(False,det)`
  senza crash.
- **T26b** backup: copia LEGGIBILE + rotazione tiene le ultime N + retention pura.
- **T26c** `backup_auto` throttled: crea, poi salta (non è ora), intervallo 0 ricrea.
- **T26d** `backup_auto` salta se l'integrità è KO (non propaga la corruzione).
- **T26e** kernel `_memoria_backup_auto`: crea il backup + memoria `None` senza crash.

---

## VERIFICHE (eseguite e dimostrate)

### A. Suite completa
`python tests/test_unit_kernel.py` → **`=== RIEPILOGO: 128 PASS, 0 FAIL ===`** (era 123).

### B. Diff del commit motore
```
 gas.py                    | 62 +++++++++++++++++++
 modules/memory/store.py   | 97 +++++++++++++++++++++++++++++---
 tests/test_unit_kernel.py | 71 ++++++++++++++++++++++
 3 files changed, 225 insertions(+), 5 deletions(-)
```

### C. Invarianti motore
`_get_window` / `_cap_window_chars` / `for _ in range(10)` / sandbox bwrap / snapshot
NON compaiono nel diff (verificato anche dal revisore via grep). Il backup è una
copia in-process di un file locale (codice fidato) → correttamente fuori dal sandbox.

---

## PROCESSO
- **Gate di review §3**: il diff tocca `gas.py`/`modules/`/`tests/` → subagent
  **revisore** invocato sul diff staged PRIMA del commit → **APPROVATO** (review #19),
  validato dal vivo (integrità OK, FTS5 attiva, doctor senza crash). Due note minori
  cosmetiche (re-import di `MemoryStore` in doctor; accesso a `_backup_files` da fuori),
  non bloccanti, chiudibili al prossimo passaggio su `gas.py`.
- Hook deterministico onorato (`.claude/.review_ok` creato per il commit, rimosso subito dopo).
- `stato_progetto.md` e `diff_sessione.md` aggiornati.

---

## §FINALE — Fuori da questo task
- **Backup OFF-MACHINE** (vera protezione anti-disastro: copia su volume/host esterno):
  resta a FASE 5 / deploy VPS. Questo backup protegge dall'AUTO-CORRUZIONE, non dalla
  morte del disco.
- **Note cosmetiche del revisore** (re-import doctor, incapsulamento `_backup_files`):
  da chiudere al prossimo intervento su `gas.py`, nessun impatto su correttezza/sicurezza.
- **Strato B del Vector DB** (embedding semantici locali + sqlite-vec): prossimo passo
  grosso di FASE 2, dietro gate umano sulle dipendenze.
