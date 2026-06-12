# 📊 STATO PROGETTO GAS

> Fotografia viva dello stato del progetto. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-06-12** (sandbox run_command: allowlist no-shell + dry-run)

## Stato del motore

- **Kernel validato end-to-end**: test di integrazione 6/6 protezioni in un
  unico turno reale (2026-06-10), incluso fallback a metà turno
  Gemini→Groq con catena tool aperta.
- **Suite unit test a zero token** (`tests/test_unit_kernel.py`):
  **44 PASS, 0 FAIL** (2026-06-12). Copre `_get_window`, cap output 8k,
  guardrail anti-memoria, errori tool senza crash, storia corrotta, cap 10
  iterazioni per provider, 5 check anti-traversal, 8 check sullo snapshot
  preventivo (T11a–T11g) e da oggi **10 check sul sandbox di run_command**
  (T12a–T12j), più T11c2 rinforzato.
- **Sandbox run_command ATTIVO** (2026-06-12, roadmap ALTA "dry-run" — CHIUSO):
  `run_command` non usa più una shell. Vetting fail-closed in `_vet_command`
  con tre barriere: (1) `shlex.split` senza shell — pipe, redirezioni,
  `;`/`&&`, `$(...)` diventano testo o rompono il parse; (2) allowlist di
  binari di SOLA lettura (`ls`, `cat`, `grep`, `wc`, `diff`…), niente
  interpreti né wrapper; (3) ogni argomento ripassa `_safe_path` (stesso
  guardrail di T10) e deve restare in root. Env del figlio **ripulita dai
  segreti** (KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL/AUTH). Ordine:
  **vetting → dry-run → snapshot → esecuzione** (i comandi negati non
  consumano snapshot, mitiga R2 della review #3). Modalità `GAS_SHELL_MODE`:
  `guarded` (default) / `dry_run` (anteprima fedele, kill-switch); valore
  ignoto → fallback fail-safe su `guarded` con warning.
  Review #4 → **APPROVATO CON RISERVE** (R1 type hint chiusa in sessione;
  R2/R3 tracciate sotto come finding).
- **Snapshot preventivo ATTIVO** (2026-06-11, roadmap ALTA punto 1 — CHIUSO):
  `_snapshot(trigger, target)` fotografa il repo PRIMA di ogni `write_file`
  e `run_command` via indice git temporaneo + ref
  `refs/gas/snapshots/<ts-ns>-<sha8>`. Fail-closed, retention 100,
  ripristino SOLO umano (README "Macchina del tempo"). Review #3 →
  APPROVATO CON RISERVE; #3-bis sul fix R1 → APPROVATO.
- **Fix T10 — path traversal BLOCCATO** (2026-06-11): `_safe_path`
  (`.resolve()` + `is_relative_to(self.root)`) su `write_file` e
  `read_file`. Review #2 → APPROVATO CON RISERVE.
- **Fix `_get_window`** (ricerca all'indietro senza cap): review #1
  retroattiva → APPROVATO CON RISERVE.

## Pipeline provider (paracadute)

1. `gemini-2.5-flash-lite` → 2. `gemini-2.5-flash` → 3. `groq/llama-3.3-70b-versatile`
- Gemini free tier: 20 req/giorno. Fallback mid-turn verificato funzionante.

## Finding aperti

- 🟡 **Esfiltrazione via shell RIDOTTA, non chiusa** (era 🟠, declassato il
  2026-06-12): il sandbox no-shell+allowlist chiude l'esfiltrazione naïve
  diretta (`cat /etc/passwd`, pipe verso la rete), ma è una recinzione
  applicativa, non un confinamento OS. Il muro definitivo è a livello
  sistema (`bwrap`/`unshare`, rete chiusa) sul VPS, con check in `gas doctor`.
- 🟡 **Valori attaccati ai flag superano il vetting per-token** (riserva R2,
  review #4): `grep -f/etc/passwd` o `--file=/etc/passwd` iniziano con `-`,
  quindi `_safe_path` non li vede, mentre il binario interpreta il path
  esterno. Con l'allowlist attuale NON esiste esfiltrazione attiva
  (verificato), ma è una divergenza vetting/binario: RIVERIFICARE prima di
  allargare `SHELL_ALLOWLIST`. Difesa candidata: rifiutare token che
  iniziano con `-` e contengono `/` o `=`.
- 🟡 **Falsi positivi del path-check su argomenti non-path** (riserva R3,
  review #4): un pattern grep tipo `"/etc/cron"` viene risolto come path
  assoluto e il comando negato. Fail-closed (lato sicuro), ma limite di
  usabilità da conoscere.
- 🟡 **Retention snapshot count-based consuma slot anche sui comandi
  read-only** (riserva R2, review #3), ora MITIGATA: il vetting gira prima
  dello snapshot, quindi i comandi negati e il dry-run non consumano slot.
  Resta il consumo dei comandi leciti: valutare KEEP più alto o count+età.
- 🟡 **Manutenzione snapshot residua** (riserva R3, review #3): (a) oggetti
  dei ref potati restano finché non gira `git gc` (candidato per
  `gas doctor`); (b) `reports/snapshots.log` append-only senza rotazione.
- 🟡 **Nessun cap rigido sulla finestra** (review #1): rimedio proposto
  `WINDOW_CHAR_CAP` a granularità di messaggio (mai slicing).
- ✅ ~~Sandbox/dry-run per run_command~~ — **CHIUSO** il 2026-06-12.
- ✅ ~~Snapshot preventivo dei file~~ — **CHIUSO** il 2026-06-11.
- ✅ ~~T10 path traversal~~ — **CHIUSO** il 2026-06-11.

## Istituzioni di processo (attive dal 2026-06-11)

- **A — `reports/stato_progetto.md`**: questo file, aggiornato a fine task.
- **B — `reports/diff_sessione.md`**: riepilogo del diff a fine sessione.
- **C — Subagent revisore** (`.claude/agents/revisore.md`): 5 review
  completate (#1, #2, #3, #3-bis, #4), 13 lezioni in
  `.claude/agents/memoria_revisore.md`.

## Prossimi passi (in ordine di priorità)

1. **`WINDOW_CHAR_CAP`** sulla finestra (rimedio proposto in review #1).
2. **Manutenzione snapshot in `gas doctor`** (riserve R2/R3 review #3:
   conteggio ref, gc oggetti orfani, dimensione snapshots.log).
3. **Confinamento OS per run_command** (`bwrap`/`unshare`, rete chiusa) in
   vista del deploy VPS — chiude definitivamente il finding esfiltrazione.
4. Valutare cap output dedicato (più alto) per la futura pipeline Whisper.
