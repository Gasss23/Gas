# 📊 STATO PROGETTO GAS

> Fotografia viva dello stato del progetto. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-06-11** (sera — snapshot preventivo anti-autodistruzione)

## Stato del motore

- **Kernel validato end-to-end**: test di integrazione 6/6 protezioni in un
  unico turno reale (2026-06-10), incluso fallback a metà turno
  Gemini→Groq con catena tool aperta.
- **Suite unit test a zero token** (`tests/test_unit_kernel.py`):
  **34 PASS, 0 FAIL** (2026-06-11). Copre `_get_window`, cap output 8k,
  guardrail anti-memoria, errori tool senza crash, storia corrotta, cap 10
  iterazioni per provider, 5 check anti-traversal e da oggi **8 check sullo
  snapshot preventivo** (T11a–T11g).
- **Snapshot preventivo ATTIVO** (2026-06-11, roadmap ALTA punto 1 — CHIUSO):
  `_snapshot(trigger, target)` fotografa il repo (tracciati + non tracciati +
  `.gas_history.json` forzata) PRIMA di ogni `write_file` (dopo `_safe_path`)
  e di ogni `run_command`. Meccanismo: indice git temporaneo
  (`GIT_INDEX_FILE`) + `write-tree` + `commit-tree` + ref
  `refs/gas/snapshots/<ts-ns>-<sha8>` — branch e staging dell'utente
  intoccati. **Fail-closed**: snapshot fallito = operazione negata.
  Check `show-toplevel == root` contro root annidate in repo esterni
  (riserva R1 della review #3, chiusa in review #3-bis). Retention: ultimi
  100 ref. Indice leggibile in `reports/snapshots.log`; successi nel log via
  logger dedicato `gas.snapshot` (solo scatola nera, console pulita).
  **Ripristino SOLO umano**: procedura nel README ("Macchina del tempo"),
  nessun tool di restore esposto ai modelli.
  Review #3 → **APPROVATO CON RISERVE**; review #3-bis sul fix R1 →
  **APPROVATO** (R1 depennata).
- **Fix T10 — path traversal BLOCCATO** (2026-06-11): `_safe_path`
  (`.resolve()` + `is_relative_to(self.root)`) su `write_file` e
  `read_file`. Review #2 → APPROVATO CON RISERVE.
- **Fix `_get_window`** (ricerca all'indietro senza cap): review #1
  retroattiva → APPROVATO CON RISERVE.

## Pipeline provider (paracadute)

1. `gemini-2.5-flash-lite` → 2. `gemini-2.5-flash` → 3. `groq/llama-3.3-70b-versatile`
- Gemini free tier: 20 req/giorno. Fallback mid-turn verificato funzionante.

## Finding aperti

- 🟠 **run_command bypassa il guardrail filesystem in LETTURA** (review #2):
  `cat <file fuori root>` esfiltra ancora. Lo snapshot preventivo ora limita
  i danni delle SCRITTURE via shell, ma l'esfiltrazione resta aperta: la
  chiude il sandbox/dry-run di roadmap.
- 🟡 **Retention snapshot count-based consuma slot anche sui comandi
  read-only** (riserva R2, review #3): una sessione shell intensa può ruotare
  i 100 ref e potare gli snapshot pre-disastro. Valutare KEEP più alto o
  regola ibrida (count + età minima protetta).
- 🟡 **Manutenzione snapshot residua** (riserva R3, review #3): (a) gli
  oggetti dei ref potati restano nel database git finché non gira `git gc`
  (candidato naturale per `gas doctor`); (b) `reports/snapshots.log` è
  append-only senza rotazione e non è gitignorato — decidere se è voluto.
- 🟡 **Nessun cap rigido sulla finestra** (review #1): rimedio proposto
  `WINDOW_CHAR_CAP` a granularità di messaggio (mai slicing).
- ✅ ~~Snapshot preventivo dei file~~ — **CHIUSO** il 2026-06-11.
- ✅ ~~T10 path traversal~~ — **CHIUSO** il 2026-06-11.

## Istituzioni di processo (attive dal 2026-06-11)

- **A — `reports/stato_progetto.md`**: questo file, aggiornato a fine task.
- **B — `reports/diff_sessione.md`**: riepilogo del diff a fine sessione.
- **C — Subagent revisore** (`.claude/agents/revisore.md`): **operativo come
  tipo registrato nell'harness** (prima invocazione diretta riuscita il
  2026-06-11, review #3); 4 review completate (#1, #2, #3, #3-bis),
  9 lezioni in `.claude/agents/memoria_revisore.md`.

## Prossimi passi (in ordine di priorità)

1. **Modalità dry-run / sandbox per run_command** — copre il finding 🟠
   (esfiltrazione via shell), roadmap alta.
2. **WINDOW_CHAR_CAP** sulla finestra (rimedio proposto in review #1).
3. **Manutenzione snapshot in `gas doctor`** (riserve R2/R3: conteggio ref,
   gc oggetti orfani, dimensione snapshots.log).
4. Valutare cap output dedicato (più alto) per la futura pipeline Whisper.
