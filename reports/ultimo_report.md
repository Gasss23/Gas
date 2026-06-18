# R-crm-1 RIFATTO — identità contatti su `chiave_norm` separata + NFKC

**Data:** 2026-06-18
**Commit motore:** `ca08df7` (revisore #22 — APPROVATO CON RISERVE)
**Commit doc:** vedi sotto (stampato a fine task)
**Suite:** **139/139, 0 FAIL** (era 135)
**Scope:** SOLO R-crm-1. `gas.py` INVARIATO. Nessun merge/dedup distruttivo.

---

## PREMESSA — verifica dello stato reale (STOP GATE onorato)

La task chiedeva di IMPLEMENTARE R-crm-1, ma a fonti canoniche (`stato_progetto.md`,
`store.py`) **R-crm-1 risultava GIÀ CHIUSO** dal 2026-06-17 (review #16) in forma
"**normalizza-in-place**": `normalizza_chiave` applicata direttamente alla colonna
`chiave` in `upsert_contatto`/`get_contatto_per_chiave`. Mi sono **FERMATO** e l'ho
segnalato all'utente PRIMA di scrivere codice (come imposto dal mandato). L'utente, messo
di fronte alla scelta, ha **deciso ESPLICITAMENTE** di rifare il design secondo la spec
originale della task: colonna `chiave_norm` separata + `chiave` as-entered. Procedo quindi
con quel refactor.

Differenze del refactor rispetto allo stato pre-esistente:
1. **NFKC** non c'era (solo `split()+lower()`) → aggiunto.
2. La grafia originale NON era conservata (la `chiave` veniva sovrascritta con la forma
   normalizzata) → ora `chiave` = **as-entered**, identità su `chiave_norm`.

---

## COSA È STATO FATTO (solo `modules/memory/` + `tests/`)

### PUNTO 1 — `normalizza_chiave`: + NFKC (pura, idempotente)
`unicodedata.normalize("NFKC", …)` PRIMA del collasso whitespace + lower: unifica le forme
di compatibilità Unicode (fullwidth `Ａ`→`a`, legatura `ﬁ`→`fi`, spazi esotici).
Idempotenza preservata (`norm(norm(x))==norm(x)`), fail-safe §9 (`None`/non-str → `""`).
**Nessuna logica telefono/email in v1** (dichiarata come fetta futura nella docstring).

### PUNTO 2 — Identità su `chiave_norm` UNIQUE, `chiave` = as-entered
- Schema `contatti`: `chiave` perde `UNIQUE` (diventa grafia originale leggibile); nuova
  colonna `chiave_norm TEXT NOT NULL`; l'indice **UNIQUE** su `chiave_norm` si crea in
  `_ensure_columns` (dopo il backfill).
- `upsert_contatto`: INSERT con `chiave` (as-entered) + `chiave_norm`, `ON CONFLICT
  (chiave_norm)`; in **update NON tocca `chiave`** → si conserva la PRIMA grafia vista.
- Lookup: `_risolvi_canonico` e `get_contatto_per_chiave` risolvono su `chiave_norm`.
- `update_stato_contatto` (per id) **INVARIATO**.

### PUNTO 3 — Migrazione ADDITIVA + SICURA (con rilevamento collisioni)
In `_ensure_columns`: `ALTER ADD COLUMN chiave_norm` (nullable) → **backfill** (deriva da
`chiave`, scrive SOLO la nuova colonna, anagrafica intatta) → **rilevamento collisioni**
(`GROUP BY chiave_norm HAVING COUNT>1`):
- **collisioni presenti** → solleva `ChiaveNormCollisione` coi gruppi in conflitto: **NON
  fonde nulla**, **NON crea l'indice**, `__init__` cattura → `available=False` +
  `self.collisione_chiave_norm` (fail-safe §9, mai crash). Il merge dei duplicati
  ESISTENTI è **MANUTENZIONE UMANA** (STOP GATE rispettato: collisione = ferma e riporta).
- **zero collisioni** → crea l'indice UNIQUE. Su DB vuoto è un no-op.

`gas.py` **INVARIATO**: `_trova_contatto` già normalizzava l'haystack al volo, quindi
funziona identico con `chiave` as-entered.

---

## VERIFICHE (eseguite e dimostrate)

### A. Suite completa
`python tests/test_unit_kernel.py` → **`=== RIEPILOGO: 139 PASS, 0 FAIL ===`** (era 135).

### B. `git diff --cached --stat` (commit motore `ca08df7`)
```
 modules/memory/__init__.py |   2 +
 modules/memory/store.py    | 140 +++++++++++++++++++++++++++++++++++++--------
 tests/test_unit_kernel.py  |  95 ++++++++++++++++++++++++++++--
 3 files changed, 207 insertions(+), 30 deletions(-)
```
`gas.py` NON nel diff. Invarianti motore (`_get_window`/`_cap_window_chars`/
`for _ in range(10)`/sandbox/snapshot/immutabilità diario) intatte.

### C. Esito dei nuovi/aggiornati test
```
[PASS] T29a normalizza_chiave applica NFKC (compatibilità Unicode)
[PASS] T29b chiave as-entered conservata + identità su chiave_norm (no doppione)
[PASS] T29c migrazione pulita: backfill + indice UNIQUE, dedup sulla forma canonica
[PASS] T29d migrazione con collisione: rilevata, niente fusione/perdita, indice non creato
[PASS] T23a / T23f / T28b  (aggiornati: chiave==normalizzata → chiave_norm)
```
T29d dimostra dal vivo: `available=False`, `collisione_chiave_norm` valorizzato coi gruppi
(`'mario rossi' → righe 1,2`), DB storico **intatto** (2 righe, `chiave` originali), indice
UNIQUE non creato.

---

## PROCESSO
- **Gate di review §3**: diff su `modules/`+`tests/` → subagent **revisore** invocato sul
  diff staged PRIMA del commit → **APPROVATO CON RISERVE** (review #22). Verifiche del
  revisore: suite 139/139, ispezione a freddo del DB post-abort, idempotenza NFKC su input
  tipografici reali, innocuità provata del vincolo UNIQUE(chiave) legacy.
- Hook deterministico onorato (`.claude/.review_ok` creato per il commit, rimosso subito).
- `stato_progetto.md` e `diff_sessione.md` aggiornati; `memoria_revisore.md` aggiornata dal
  revisore (3 lezioni datate 2026-06-18).

## RISERVE (review #22, non bloccanti — tracciate in `stato_progetto.md`)
- **R-crm-norm-2**: `collisione_chiave_norm` non ancora esposto in `gas doctor` sez. 8
  "Memoria". Follow-up (gas.py invariato in questa fetta).
- **Normalizzazione per-tipo (telefono/email)** non in v1: R-crm-1b (identità cross-formato)
  resta MITIGATA, non chiusa (corretto e onesto; T23f presidia il confine).

---

## §FINALE — Fuori da questo mandato (NON eseguito, scope umano)
- **Merge dei duplicati ESISTENTI**: in caso di collisione la migrazione si ferma; la
  fusione delle schede storiche è operazione UMANA (mai automatica). La prevenzione dei
  duplicati FUTURI è invece attiva.
- **R-crm-norm-2 in doctor** e **normalizzazione per-tipo**: prossime fette, non ora.
