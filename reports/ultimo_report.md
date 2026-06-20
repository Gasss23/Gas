# ULTIMO REPORT — Backup off-machine + doctor memoria rumoroso (review #26/#27)

**Data:** 2026-06-20
**Esito:** COMMIT ESEGUITO (56a6dc3) — revisore #26 e #27 APPROVATI CON RISERVE, suite 158 PASS, 8 FAIL pre-esistenti Windows. T33a-h + T34a-e tutti PASS.

---

## Cosa e' stato fatto

### TASK A (review #26) — Backup off-machine del DB memoria

1. **`modules/memory/store.py`**: nuovo metodo `backup_offsite_auto(offsite_dir, min_interval_sec, keep)`:
   - Backup THROTTLED su dir esterna configurabile (anti-disastro disco).
   - Throttle SEPARATO da `backup_auto` (la dir esterna puo' essere lenta/NFS).
   - Cintura integrita': `integrity_check` prima di ogni copia (DB corrotto NON viene mai copiato offsite).
   - Riusa `backup()` e `integrity_check()` senza reimplementarli.
   - Fail-safe sec. 9: cattura `(sqlite3.Error, OSError)`, mai crash.

2. **`gas.py`**:
   - Costanti di classe `MEMORY_BACKUP_OFFSITE_EVERY_SEC=86400` e `MEMORY_BACKUP_OFFSITE_KEEP=10`.
   - `__init__`: override env `GAS_MEMORY_BACKUP_OFFSITE_DIR/_EVERY_SEC/_KEEP` (via `_env_int`/env var).
   - `_memoria_backup_auto()`: blocco off-site condizionale (solo se dir configurata), fail-safe separato.
   - Nuova funzione `backup_cmd()` **SOLO-CLI**: controlla integrita', esegue backup locale + opzionalmente off-site, exit 0/1. NON in `tools_schema` e NON nel dispatcher (fuori dalla mano del modello, stessa classe di `reindex`/`unisci_contatti`).
   - Dispatch `gas backup` in `main()`.
   - Doctor sez.8: check off-site dir+eta' ultimo backup, INDIPENDENTE da `mem.available` (check puramente filesystem; `mem` ora dichiarata `None` prima del blocco if/else).

3. **`tests/test_unit_kernel.py`**: T33a-h (tutti PASS):
   - T33a: `backup_offsite_auto` scrive file SQLite integro nella dir esterna.
   - T33b: cintura integrita' — sorgente corrotta -> skip, nessun crash.
   - T33c: rotazione via `_backup_retention` (funzione pura, 5 file finti, OS-agnostica per evitare WinError 32).
   - T33d: throttle — seconda chiamata entro intervallo -> None.
   - T33e: fail-safe — file al posto della dir -> OSError -> None, nessun crash.
   - T33f: default OFF — env non settata -> `MEMORY_BACKUP_OFFSITE_DIR is None`.
   - T33g: `gas backup` CLI exit 0 + stampa path backup locale.
   - T33h: `gas backup` CLI con sorgente non disponibile -> exit 1.

### TASK B (review #27) — Doctor fallimento silenzioso della memoria reso RUMOROSO

4. **`gas.py`** (solo `doctor()` sez.8):
   - Quando `mem.available` e' False, il doctor distingue due casi **rumorosi** invece del vecchio silenzio:
     - `mem.collisione_chiave_norm` valorizzato -> `FAIL` esplicito coi gruppi duplicati (es. "migrazione chiave_norm bloccata: duplicati storici sulla stessa chiave normalizzata, da fondere MANUALMENTE ('anna' -> righe 1,2)").
     - altrimenti -> `FAIL` esplicito "DB non apribile, schema non inizializzabile o corruzione all'init".
   - In entrambi i casi exit code == 1 (FAIL nel report doctor). Chiude **R-crm-norm-2**.
   - Vector store visibility: dopo il check off-site, il doctor controlla `GAS_VECTORS` e riporta:
     - `OK` se abilitato e sidecar apribile.
     - `WARN` se abilitato ma non disponibile (deps assenti o sidecar corrotto).
     - `OK` "disabilitato" se non settata.
   - Zero download del modello: `VectorStore.__init__` e' lazy (il modello si carica solo al primo `index_batch`/`search`). Verificato: T34d con sidecar corrotto finisce in WARN senza nessun download, in millisecondi.

5. **`tests/test_unit_kernel.py`**: T34a-e (tutti PASS):
   - T34a: DB con collisione chiave_norm -> `available=False`, `collisione_chiave_norm` valorizzato, doctor exit=1, "collisione" in stdout.
   - T34b: DB corrotto -> doctor exit=1 con "FAIL" in stdout, nessun crash.
   - T34c: DB sano vuoto -> NESSUN "FAIL" nelle righe Memoria "apertura"/"integrita" (no regressione).
   - T34d: `GAS_VECTORS=1` + sidecar corrotto -> "WARN" e "vector store" in stdout, nessun download.
   - T34e: `GAS_VECTORS` non settata -> "disabilitato" in stdout.

---

## Suite

```
158 PASS, 8 FAIL
```

I FAIL sono TUTTI pre-esistenti su Windows:
- T9a, T9c: dipendenti da env API non settate.
- T11c2, T11e, T12a, T12c, T12e: bwrap/namespace non disponibili su Windows.
- T26b: WinError 32 (file locking Windows su SQLite backup) — pre-esistente, benigno su Linux/VPS.

I 15 nuovi test (T33a-h + T34a-e) sono tutti PASS.

NB: la suite su Windows richiede `PYTHONUTF8=1` per il carattere `approx` in T18f (pre-esistente cp1252 issue); non e' un nuovo FAIL.

---

## Riserve aperte post-review

**R26-1** (review #26, minore): `backup_cmd()` ritorna exit 0 anche quando il backup off-site fallisce (solo il locale e' garantito). Comportamento difendibile (off-site e' best-effort), ma da documentare: uno script `gas backup && rclone sync` sul VPS non deve aspettarsi exit 1 sul fallimento off-site.

**R26-2** (review #26, minore): manca un test kernel-level che verifichi l'aggancio di `_memoria_backup_auto` col blocco off-site ATTIVO (candidato T33i in sessione futura; T33a/f coprono implicitamente il comportamento).

**R27-1** (review #27, riserva cosmetica): alias `_dvp` importato ma inutilizzato a riga 1555 — CORRETTO prima del commit (rimosso l'alias, usa il nome importato a livello di modulo).

---

## VERDETTI INTEGRALI DEI REVISORI

### Review #26 (TASK A) — APPROVATO CON RISERVE

"La review #26 (TASK A — Backup OFF-MACHINE del DB memoria) e' approvata. Il codice e' corretto, il fail-safe sec. 9 e' rispettato in tutti i path, la cintura d'integrita' e' implementata correttamente, il throttle e' separato da quello locale, `backup_cmd` e' fuori da `tools_schema` e dal dispatcher, il doctor gestisce correttamente `mem=None`, le invarianti motore sono intatte e i test T33a-h coprono i casi rilevanti con buona mordacita'."

Riserve non bloccanti: R26-1 (exit-code backup_cmd best-effort off-site), R26-2 (manca T33i kernel-aggancio).

### Review #27 (TASK B) — APPROVATO CON RISERVE

"Si — e' esattamente cio' che R-crm-norm-2 richiedeva. Il ramo `collisione_chiave_norm` stampa il dettaglio dei gruppi duplicati [...], mentre il ramo generico 'DB non apribile, schema non inizializzabile o corruzione all'init' e' onesto sui casi residui. La distinzione e' utile operativamente: l'operatore sul VPS capisce immediatamente se deve fare un merge manuale dei contatti o indagare una corruzione. [...] La modifica e' confinata alla funzione `doctor()`. `run_turn`, il loop a 10 iterazioni, `_get_window`/`_cap_window_chars`, provider, finestra, sandbox, snapshot e pin sono INVARIATI."

Riserva non bloccante: R27-1 (alias `_dvp` inutilizzato — corretta prima del commit).

Chiude: **R-crm-norm-2** (dal finding aperto di review #22).

---

## Note di processo

- Commit motore: `56a6dc3` (review #26 + #27 insieme, entrambi approvati).
- I report off-machine (remoto reale: rclone/rsync/volume montato) non sono testabili in dev: dichiarati FASE 5/deploy VPS.
- Invarianti motore intatte: `_get_window`/`_cap_window_chars`/`for _ in range(10)`/sandbox/snapshot/`_memoria_pin` non toccati.
- T18f crash cp1252 (pre-esistente, carattere `approx` nella stringa di dettaglio): la suite completa richiede `PYTHONUTF8=1` su Windows; sul VPS Linux gira identica.
