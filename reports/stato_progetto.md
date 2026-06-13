# 📊 STATO PROGETTO GAS

> Fotografia viva dello stato del progetto. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-06-12** (sera — sandbox di run_command)

## Stato del motore

- **Scudo gratuito del paracadute ATTIVO** (2026-06-13, FASE 2 cervello low-cost):
  due rung gratuiti SEMPRE in coda alla cascata (`run_turn` + `doctor`):
  `openrouter` (free tool-capable `meta-llama/llama-3.3-70b-instruct:free`) e
  `ollama` (pavimento offline `qwen2.5:7b-instruct`, gate su `GAS_OLLAMA_URL`).
  Fail-safe: chiave/endpoint assenti → skip pulito (sez. 9, mai crash). Brain
  legacy `brains/*.py` NON cablati (restano codice morto). `doctor`: i due rung
  opzionali danno WARN (non FAIL) se non configurati. Review **APPROVATO CON
  RISERVE** (R1/R2/R3 sotto, nessuna indebolisce i guardrail). Suite 46/46.
- **Sicurezza commit indurita** (2026-06-13): hook `SessionEnd` disarmato (add
  selettivo di `reports/`, `*.md`, `.gas_history.json`; mai `-A`, mai il motore)
  + gate di review deterministico `PreToolUse` su `git commit` del motore
  (`.claude/hooks/review_gate.sh`, marcatore `.claude/.review_ok`) + regola di
  workflow in CLAUDE.md sez. 3 + `description` revisore imperativa.
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
  snapshot. Review #4 → **APPROVATO CON RISERVE** (R1 chiusa in sessione;
  R2/R3 tracciate sotto come finding 🟡).
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
   → 4. `openrouter` (free, tool-capable: `meta-llama/llama-3.3-70b-instruct:free`)
   → 5. `ollama` (pavimento offline, `qwen2.5:7b-instruct`, solo se `GAS_OLLAMA_URL` settata)
- Fallback mid-turn verificato funzionante. I due rung gratuiti (4–5) sono la rete
  di salvataggio a budget zero: skip pulito se manca chiave/endpoint (sez. 9, mai
  crash). `ollama` NON gira nel Codespace, solo su PC/VPS di deploy.
- NB free tier Gemini: la vecchia nota "20 req/giorno" era **obsoleta** (corretta il
  2026-06-13); oggi il limite giornaliero è molto più alto e varia per modello.

## Finding aperti

- 🟠→🟡 **Esfiltrazione via shell — RIDOTTA, non chiusa** (era finding 🟠):
  il sandbox di `run_command` neutralizza i vettori naïve/diretti (pipe,
  redirezioni, command substitution rese innocue; binari di rete negati;
  chiavi rimosse dall'env del figlio — verificato end-to-end su 4 vettori).
  **Non** è un confinamento a livello OS: gli interpreti restano fuori
  dall'allowlist proprio per non riaprire l'esecuzione di codice arbitrario.
  La chiusura definitiva è il sandbox OS (bwrap/unshare, rete chiusa,
  filesystem read-only sul VPS) — vedi prossimi passi.
- 🟡 **Valori attaccati ai flag superano il vetting per-token** (R2, review
  #4): `grep -f/etc/passwd` o `--file=/etc/passwd` iniziano con `-`, quindi
  `_safe_path` non li vede come path, mentre il binario interpreta il file
  esterno. Con l'allowlist attuale NON esiste esfiltrazione attiva
  (verificato), ma è una divergenza vetting/binario: RIVERIFICARE prima di
  allargare `SHELL_ALLOWLIST`. Difesa candidata: rifiutare token che iniziano
  con `-` e contengono `/` o `=`.
- 🟡 **Falsi positivi del path-check su argomenti non-path** (R3, review #4):
  un pattern grep tipo `/etc/cron` viene risolto come path assoluto e il
  comando negato. Fail-closed (lato sicuro), ma limite di usabilità da
  conoscere.
- 🟡 **Retention snapshot count-based** (R2): una sessione shell intensa può
  ruotare i 100 ref. Mitigato in parte (i comandi negati al vetting non
  scattano più lo snapshot), ma resta: valutare KEEP più alto o count + età
  minima protetta.
- 🟡 **Manutenzione snapshot residua** (R3): (a) oggetti dei ref potati
  restano finché non gira `git gc` (candidato `gas doctor`); (b)
  `reports/snapshots.log` append-only senza rotazione e non gitignorato.
- 🟡 **Nessun cap rigido sulla finestra** (review #1): rimedio proposto
  `WINDOW_CHAR_CAP` a granularità di messaggio (mai slicing).
- 🟡 **Modello free hardcoded e volatile** (R1, review #5):
  `meta-llama/llama-3.3-70b-instruct:free` può sparire/cambiare lato OpenRouter;
  il fail-safe regge (skip su errore) ma il paracadute diventerebbe
  silenziosamente inerte. `gas doctor` dovrebbe verificare l'ESISTENZA del
  modello, non solo la presenza della chiave.
- 🟡 **Degrado a solo-testo non verificato a runtime** (R2, review #5): se il
  modello free non supporta i tool, il loop agentico perde read_file/write_file;
  oggi è solo dichiarato in commento, non rilevato/loggato a runtime.
- 🟡 **Duplicazione costanti provider** (R3, review #5): URL/modelli ripetuti tra
  `run_turn` e `doctor`, ora estesa ai rung free; candidata a estrazione in
  costanti di modulo (manutenibilità, non sicurezza).
- ✅ ~~Sandbox/dry-run per run_command~~ — **RIDOTTO** il 2026-06-12 (finding
  declassato da 🟠 a 🟡, chiusura piena rinviata al sandbox OS).
- ✅ ~~Snapshot preventivo dei file~~ — CHIUSO il 2026-06-11.
- ✅ ~~T10 path traversal~~ — CHIUSO il 2026-06-11.

## Istituzioni di processo (attive dal 2026-06-11)

- **A — `reports/stato_progetto.md`**: questo file, aggiornato a fine task.
- **B — `reports/diff_sessione.md`**: riepilogo del diff a fine sessione.
- **C — Subagent revisore** (`.claude/agents/revisore.md`): 5 review
  completate (#1, #2, #3, #3-bis, #4), 13 lezioni datate in
  `.claude/agents/memoria_revisore.md`.

## Prossimi passi (in ordine di priorità)

1. **Sandbox a livello OS per `run_command`** (bwrap/unshare: namespace di
   rete chiuso + filesystem read-only) — chiusura PIENA del finding ora
   ridotto. Aggiungere un check di disponibilità in `gas doctor`.
2. **WINDOW_CHAR_CAP** sulla finestra (rimedio proposto in review #1).
3. **Manutenzione snapshot in `gas doctor`** (riserve R2/R3: conteggio ref,
   gc oggetti orfani, dimensione snapshots.log; valutare retention ibrida).
4. Valutare cap output dedicato (più alto) per la futura pipeline Whisper.
