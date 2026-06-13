# 📊 STATO PROGETTO GAS

> Fotografia viva dello stato del progetto. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-06-12** (sera — sandbox di run_command)

## Stato del motore

- **Sandbox di `run_command` ATTIVO** (2026-06-12, roadmap ALTA punto 1 —
  CHIUSO): `run_command` non usa più `shell=True`. Ogni comando passa per un
  vetting **fail-closed** ed è eseguito con `shell=False`. Tre barriere:
  (1) `shlex.split` — pipe, redirezioni, `;`/`&&`, `$(...)` perdono potere
  (diventano testo o rompono il parse; virgolette sbilanciate → negato);
  (2) **allowlist** sul binario (`argv[0]`) di soli comandi di sola lettura
  (`ls, cat, head, tail, wc, grep, cut, diff, stat...`) — allowlist e non
  denylist perché i wrapper (`env curl`, `xargs`, `bash -c`) sfondano i
  proibiti; interpreti esclusi di proposito; (3) ricontrollo di ogni
  argomento-path con lo **stesso** `_safe_path` di T10. Env del figlio
  **sanificata** (rimosse le variabili con KEY/TOKEN/SECRET/PASSWORD/PASSWD/
  CREDENTIAL/AUTH nel nome). Due modalità via `GAS_SHELL_MODE`: `guarded`
  (default; valore ignoto → qui, fail-safe) e `dry_run` (vetting sì,
  esecuzione no, nessuno snapshot — collaudo/kill-switch). Ordine
  **vetting → snapshot → esecuzione**: un comando negato non spreca uno
  snapshot. Review #4 → **(verdetto da integrare)**.
- **Snapshot preventivo ATTIVO** (2026-06-11, roadmap ALTA — CHIUSO):
  `_snapshot(trigger, target)` fotografa il repo (tracciati + non tracciati +
  `.gas_history.json` forzata) PRIMA di ogni `write_file` (dopo `_safe_path`)
  e di ogni `run_command`. Meccanismo: indice git temporaneo
  (`GIT_INDEX_FILE`) + `write-tree` + `commit-tree` + ref
  `refs/gas/snapshots/<ts-ns>-<sha8>`. **Fail-closed**: snapshot fallito =
  operazione negata. Check `show-toplevel == root` contro root annidate in
  repo esterni (riserva R1, chiusa). Retention: ultimi 100 ref. Ripristino
  SOLO umano (README "Macchina del tempo"). Review #3 → APPROVATO CON
  RISERVE; review #3-bis sul fix R1 → APPROVATO.
- **Fix T10 — path traversal BLOCCATO** (2026-06-11): `_safe_path`
  (`.resolve()` + `is_relative_to(self.root)`) su `write_file` e `read_file`.
  Review #2 → APPROVATO CON RISERVE.
- **Fix `_get_window`** (ricerca all'indietro senza cap): review #1
  retroattiva → APPROVATO CON RISERVE.
- **Suite unit test a zero token** (`tests/test_unit_kernel.py`):
  **44 PASS, 0 FAIL** (2026-06-12, stabile su 3 run consecutivi). Dai 34
  storici si aggiungono i 10 check T12 (sandbox) + il rinforzo di T11c2.

## Pipeline provider (paracadute)

1. `gemini-2.5-flash-lite` → 2. `gemini-2.5-flash` → 3. `groq/llama-3.3-70b-versatile`
- Gemini free tier: 20 req/giorno. Fallback mid-turn verificato funzionante.

## Finding aperti

- 🟠→🟡 **Esfiltrazione via shell — RIDOTTA, non chiusa** (era finding 🟠):
  il sandbox di `run_command` neutralizza i vettori naïve/diretti (pipe,
  redirezioni, command substitution rese innocue; binari di rete negati;
  chiavi rimosse dall'env del figlio — verificato end-to-end su 4 vettori).
  **Non** è un confinamento a livello OS: gli interpreti restano fuori
  dall'allowlist proprio per non riaprire l'esecuzione di codice arbitrario.
  La chiusura definitiva è il sandbox OS (bwrap/unshare, rete chiusa,
  filesystem read-only sul VPS) — vedi prossimi passi.
- 🟡 **Retention snapshot count-based** (R2): una sessione shell intensa può
  ruotare i 100 ref. Mitigato in parte (i comandi negati al vetting non
  scattano più lo snapshot), ma resta: valutare KEEP più alto o count + età
  minima protetta.
- 🟡 **Manutenzione snapshot residua** (R3): (a) oggetti dei ref potati
  restano finché non gira `git gc` (candidato `gas doctor`); (b)
  `reports/snapshots.log` append-only senza rotazione e non gitignorato.
- 🟡 **Nessun cap rigido sulla finestra** (review #1): rimedio proposto
  `WINDOW_CHAR_CAP` a granularità di messaggio (mai slicing).
- ✅ ~~Sandbox/dry-run per run_command~~ — **RIDOTTO** il 2026-06-12 (finding
  declassato da 🟠 a 🟡, chiusura piena rinviata al sandbox OS).
- ✅ ~~Snapshot preventivo dei file~~ — CHIUSO il 2026-06-11.
- ✅ ~~T10 path traversal~~ — CHIUSO il 2026-06-11.

## Istituzioni di processo (attive dal 2026-06-11)

- **A — `reports/stato_progetto.md`**: questo file, aggiornato a fine task.
- **B — `reports/diff_sessione.md`**: riepilogo del diff a fine sessione.
- **C — Subagent revisore** (`.claude/agents/revisore.md`): operativo;
  review completate #1, #2, #3, #3-bis; review #4 (sandbox run_command) in
  corso. Memoria persistente in `.claude/agents/memoria_revisore.md`.

## Prossimi passi (in ordine di priorità)

1. **Sandbox a livello OS per `run_command`** (bwrap/unshare: namespace di
   rete chiuso + filesystem read-only) — chiusura PIENA del finding ora
   ridotto. Aggiungere un check di disponibilità in `gas doctor`.
2. **WINDOW_CHAR_CAP** sulla finestra (rimedio proposto in review #1).
3. **Manutenzione snapshot in `gas doctor`** (riserve R2/R3: conteggio ref,
   gc oggetti orfani, dimensione snapshots.log; valutare retention ibrida).
4. Valutare cap output dedicato (più alto) per la futura pipeline Whisper.
