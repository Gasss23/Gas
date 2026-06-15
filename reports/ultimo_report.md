# Report housekeeping — stash orfano + chiusura domanda VPS

**Data:** 2026-06-15 · **Tipo:** HOUSEKEEPING (nessuna modifica a gas.py/brains/modules/tests; nessun gc/prune/comando distruttivo; nessun drop di stash — decisione umana).

## (a) Stash orfano: contenuto INTEGRALE + classificazione

`git stash list` → un solo stash:
```
stash@{0}: On main: snapshot-autonomo (snapshot_health + T15) -> da riprendere in TASK C
```

`git stash show -p stash@{0}` tocca **2 file**:

### 1. `gas.py`
- Aggiunge due costanti di classe: `SNAPSHOT_GC_HINT = 1000` (oltre N oggetti loose, doctor consiglia `git gc`) e `SNAPSHOT_LOG_MAX = 1024*1024` (oltre 1 MB consiglia rotazione di `reports/snapshots.log`).
- Aggiunge un metodo **`snapshot_health() -> Dict[str, Any]`**: diagnostica READ-ONLY (riserve R2/R3 review #3) per `gas doctor`. Conta i ref `refs/gas/snapshots/*`, gli oggetti git loose (via `count-objects -v`) e la dimensione di `snapshots.log`; fail-safe (`git_ok=False`, mai crash).
- Aggiunge la **sezione 7 di `doctor`** che chiama `snapshot_health()` e stampa i check "Snapshot" (ref, oggetti git, snapshots.log), con i WARN su capacità/gc/rotazione.

### 2. `tests/test_unit_kernel.py`
- Aggiunge il blocco **T15a–f** che collauda `snapshot_health`: repo fresco (0 ref, git_ok), N snapshot → `ref_count=N` + log popolato, `at_capacity` con KEEP basso, soglia di rotazione log, soglia gc sui loose, fail-safe su dir senza repo git.

### Classificazione: **(i) CRUFT — lavoro già incorporato altrove (in altra forma).**

Verificato sul main attuale:
- `grep snapshot_health|SNAPSHOT_GC_HINT|SNAPSHOT_LOG_MAX gas.py` → **nessun riscontro**; `grep T15 tests/` → **nessun riscontro**. Quindi il *codice esatto* dello stash non è in main.
- MA la **funzionalità** sì: la doctor sez.7 "Manutenzione snapshot (TASK C)" è già presente in main **implementata inline** (gas.py:910-947) — stesso intento: conteggio ref + hint oggetti loose via `count-objects` (WARN se `loose>10000`) + dimensione `snapshots.log`. È la versione mergiata in **TASK C, review #10** (vedi `stato_progetto.md` → Stato del motore), che ha SOSTITUITO l'approccio `snapshot_health()` dello stash.

Conclusione: lo stash è un **prototipo precedente e alternativo della stessa feature**, superato dalla versione effettivamente in produzione. Niente di unico/dimenticato a livello funzionale.

**Sfumatura per la TUA decisione di drop (non droppato):** l'unica cosa che lo stash aveva *in più* della versione mergiata sono i **test T15a–f** sul percorso health. La versione in main è "provata dal vivo" ma senza test dedicato — è esattamente la **riserva aperta TASK C #4** (`stato_progetto.md`: "manca test dedicato … per i 3 check di doctor sezione 7"). I T15 NON sono però cherry-pickabili così come sono, perché collaudano il metodo `snapshot_health()` che in main non esiste (la sez.7 è inline). Quindi: come codice è cruft; come *spunto* per chiudere la riserva TASK C #4 varrebbe riscrivere dei test sulla sez.7 inline. Il drop resta tua decisione.

## (b) Chiusura domanda aperta in `reports/stato_progetto.md` — CONFERMATO

Due modifiche applicate (solo doc, nessun tocco al motore):
1. **Header** — aggiunta riga datata **2026-06-15 (diagnosi snapshot — CHIUSA, non-bug)**: registra che `_snapshot()` scrive ref persistenti (verifica dal vivo: ref nato in `.git/refs/gas/snapshots/`, poi rimosso con `update-ref -d`), che lo 0 ref in dev è atteso e che i loose sono detrito git, non snapshot recuperabili.
2. **Note operative VPS, punto 1** — riscritto da *domanda aperta* a **"check di pre-deploy VPS, NON un bug"**: la domanda "(b) gli snapshot vengono davvero creati/persistiti?" è marcata **RISOLTA**; aggiunto che sul VPS il kernel eseguirà `run_command`/`write_file` → gli snapshot nasceranno davvero, e lì `gas doctor` sez.7 con 0 ref + molti loose diventa un segnale anomalo da rivalutare (in dev no). Il punto (a) `git gc` OPT-IN resta come pianificazione, con la precisazione che i loose sono detrito git e non snapshot da salvare.
