# 📊 STATO PROGETTO GAS

> Fotografia viva dello stato del progetto. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-06-14** (test T14 per WINDOW_CHAR_CAP — review #8, suite 61/61)

## Stato del motore

- **WINDOW_CHAR_CAP + riordino R1 #6 ATTIVI** (2026-06-14, FASE 1 — review #7):
  (1) tetto RIGIDO di caratteri sulla finestra inviata ai provider
  (`WINDOW_CHAR_CAP = 24000`, ~6-7k token) a granularità di MESSAGGIO: nuovo
  `_cap_window_chars` (+ helper `_msg_chars`) in coda a `_get_window`. Scarto di
  messaggi INTERI dal più recente all'indietro quando si sfora il budget (MAI
  slicing dentro un messaggio, Wall of Shame §5), poi riallineamento dell'inizio
  a un `role:user` coerente (no tool orfani → niente Gemini 400). Casi limite
  collaudati: ultimo msg > cap tenuto intero, scarto-di-tutti-gli-user → fallback
  all'ultimo user, finestra vuota. Si compone col cap a 10 messaggi e
  TOOL_OUTPUT_CAP (rimedio incidente 2026-06-10 Groq 413). (2) Riordino R1 #6:
  check sandbox OS spostato PRIMA dello snapshot nel ramo `run_command`
  (os_strict); ortogonalità §6.3 e fail-closed os_strict INTATTI, non si spreca
  più uno slot di snapshot quando il sandbox manca. Review #7 → **APPROVATO CON
  RISERVE**; copertura test R1 #7 chiusa in review #8 (**APPROVATO**, blocco
  T14). Suite **61/61**.
- **Sandbox a livello OS (bwrap) ATTIVO** (2026-06-14, FASE 1 punto 1 — CHIUSO):
  `run_command`, dove l'host concede i namespace, gira dentro un sandbox bwrap.
  Profilo (§6.1): `--unshare-net` (rete isolata, solo loopback) `--unshare-pid
  --proc /proc` `--new-session --die-with-parent` `--ro-bind / /` (fs read-only)
  `--tmpfs /home --tmpfs /root --tmpfs /run` (MASCHERANO le home: chiavi, token,
  ~/.ssh, ~/.config) + `--ro-bind <project_root> <project_root>` PER ULTIMO
  (ri-espone in RO la sola root, anche se sta sotto /home: caso VPS) + `--clearenv`
  e `--setenv` di ogni variabile GIÀ sanificata. Due modalità ORTOGONALI a
  `GAS_SHELL_MODE` (§6.3) via `GAS_SANDBOX_MODE`: `os_strict` (default; sandbox
  assente → `run_command` NEGATO, fail-closed, la prod è protetta di default) e
  `os_with_fallback` (sandbox assente → degrado alla sola sandbox applicativa).
  Valore ignoto → fail-safe su `os_strict`. Ordine: vetting → dry_run? → snapshot
  → check sandbox (per mode) → exec in bwrap. `gas doctor`: nuova riga "Sandbox
  OS" che sonda SEMPRE (presenza bwrap + sonda namespace REALE), FAIL se
  os_strict+assente, WARN se os_with_fallback+assente. Sonda preliminare
  dell'ambiente eseguita PRIMA di progettare (roadmap): Codespace = bwrap 0.9.0,
  namespace concessi. Review #6 → **APPROVATO CON RISERVE** (R1/R2/R3 sotto,
  nessuna indebolisce i guardrail). Suite **52/52**.
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
  **61 PASS, 0 FAIL** (2026-06-14). Dai 52 si aggiungono i 9 check T14
  (WINDOW_CHAR_CAP: `_msg_chars`, finestra vuota, sotto-cap invariata,
  ultimo-msg>cap intero, scarto interi mai-slicing, riallineamento a user,
  fallback scarto-tutti-user, componibilità con `_get_window`). Prima, i 6 T13
  (sandbox OS: T13a rete chiusa, T13b fs read-only, T13c segreto mascherato,
  T13d/d2 fallback per mode, T13e lecito dentro bwrap + snapshot). T13a/b/c
  esercitano `_bwrap_prefix` direttamente (l'allowlist read-only non ha binari
  di rete/scrittura) e si auto-skippano con `[SKIP]` se l'host non concede i
  namespace (in Codespace NON si skippano).

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

- 🟡 **Esfiltrazione via shell — CHIUSA a livello OS in os_strict** (era 🟠→🟡):
  con il sandbox bwrap attivo e `GAS_SANDBOX_MODE=os_strict` (default) è
  confinamento reale, non più mitigazione applicativa: rete isolata
  (verificato `getent` rc=2), filesystem read-only, segreti on-disk sotto
  /home mascherati (tmpfs), env del figlio sanificata. **Caveat (review #6):**
  la chiusura vale SOLO in os_strict con sandbox disponibile; in
  `os_with_fallback` su host senza namespace si ricade nella sola sandbox
  applicativa e il finding resta 🟡 come prima. Resta 🟡 perché il deploy può
  girare in fallback; sull'host di prod (namespace concessi, os_strict) è di
  fatto chiuso.
- 🟡 **Valori attaccati ai flag superano il vetting per-token** (R2, review #4)
  — **DECLASSATO/neutralizzato in os_strict** (review #6): anche se un token
  tipo `-f/home/...secret` superasse il vetting per-token, il file sotto /home
  è mascherato dalla tmpfs e non leggibile dentro il sandbox (T13c lo
  dimostra), e la rete chiusa impedisce comunque l'esfiltrazione. La divergenza
  vetting/binario perde efficacia esfiltrante. **Caveat:** vale in os_strict +
  sandbox disponibile; in fallback applicativo la divergenza resta come prima.
  Difesa candidata invariata (rifiutare token con `-`+`/`/`=`) se si allarga
  `SHELL_ALLOWLIST` o si gira stabilmente in fallback.
- ✅ ~~**Snapshot sprecato in os_strict quando il sandbox manca** (R1, review #6)~~
  — **RISOLTO** il 2026-06-14 (review #7): il check sandbox OS è stato anticipato
  PRIMA dello snapshot nel ramo `run_command` (os_strict). Un comando lecito al
  vetting ma negato per sandbox assente non consuma più uno slot di snapshot.
  Ortogonalità §6.3 e fail-closed os_strict invariati.
- ✅ ~~**Manca test permanente per `_cap_window_chars`** (R1, review #7)~~ —
  **RISOLTO** il 2026-06-14 (review #8 APPROVATO): blocco **T14** (9 check) in
  `tests/test_unit_kernel.py` con cap abbassato sull'istanza. Copre `_msg_chars`,
  finestra vuota, sotto-cap invariata, ultimo-msg>cap tenuto intero, scarto di
  messaggi INTERI (mai slicing), riallineamento a user, fallback scarto-di-tutti-
  gli-user, componibilità con `_get_window`. Mordacità verificata per MUTAZIONE
  dal revisore. Suite **61/61**.
- 🟡 **Copertura non al 100% di `_cap_window_chars`** (R-test-1, review #8):
  restano scoperti due rami secondari: (a) `return window` su finestra falsy
  non-`[]`; (b) `return capped` finale "nessun user da nessuna parte", morto in
  pratica perché `_get_window` garantisce a monte un user. Non è una lacuna di
  sicurezza, solo copertura righe; non blocca.
- 🟡 **`WINDOW_CHAR_CAP` non configurabile via env** (R2, review #7): attributo di
  classe hardcoded a 24000 (coerente con TOOL_OUTPUT_CAP). Per il deploy VPS /
  pipeline Whisper (prossimi passi: cap output dedicato più alto) valutare un
  override `GAS_WINDOW_CHAR_CAP` con fallback fail-safe. Non urgente.
- 🟡 **Trappola `--chdir` con cwd fuori dalla project root** (R2, review #6):
  se `GAS_CWD` punta a una dir sotto /home (o /root, /run) ma FUORI dalla root
  ri-bindata, la tmpfs la maschera e `--chdir` fallisce → `run_command` negato
  (rc≠0). È fail-closed e non crasha, ma è un limite di usabilità sul VPS:
  documentare che `GAS_CWD` deve stare dentro la project root.
- ✅ ~~**Duplicazione del parse di `GAS_SANDBOX_MODE` in doctor** (R3, review #6)~~
  — **CHIUSO** il 2026-06-14 (TASK A, refactor puro APPROVATO): estratto l'helper
  di modulo `_parse_mode(env_var, allowed, default)`, usato sia da `__init__`
  (GAS_SHELL_MODE, GAS_SANDBOX_MODE) sia da `doctor` (GAS_SANDBOX_MODE). T16c
  certifica che le due strade risolvono lo STESSO mode (incl. ignoto→os_strict).
  Effetto collaterale minore non bloccante: ora anche `doctor` logga il warning
  su mode ignoto (prima no); voci/esiti/exit di doctor invariati.
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
- ✅ ~~**Nessun cap rigido sulla finestra** (review #1)~~ — **CHIUSO** il
  2026-06-14 (review #7): `WINDOW_CHAR_CAP = 24000` a granularità di messaggio
  (`_cap_window_chars`), mai slicing. Resta aperta la sola R1 #7 (test permanente).
- 🟡 **Modello free hardcoded e volatile** (R1, review #5):
  `meta-llama/llama-3.3-70b-instruct:free` può sparire/cambiare lato OpenRouter;
  il fail-safe regge (skip su errore) ma il paracadute diventerebbe
  silenziosamente inerte. `gas doctor` dovrebbe verificare l'ESISTENZA del
  modello, non solo la presenza della chiave.
- 🟡 **Degrado a solo-testo non verificato a runtime** (R2, review #5): se il
  modello free non supporta i tool, il loop agentico perde read_file/write_file;
  oggi è solo dichiarato in commento, non rilevato/loggato a runtime.
- ✅ ~~**Duplicazione costanti provider** (R3, review #5)~~ — **CHIUSO** il
  2026-06-14 (TASK A): URL ed slug dei provider (inclusi i due rung free) estratti
  in costanti di modulo (`GEMINI_URL`, `GROQ_URL`, `OPENROUTER_URL`,
  `GEMINI_FLASH_LITE_MODEL`, `GEMINI_FLASH_MODEL`, `GROQ_MODEL`,
  `OPENROUTER_FREE_MODEL`, `OLLAMA_MODEL`), punto unico per `run_turn` e `doctor`.
  Cascata bit-identica verificata dal revisore.
- ✅ ~~Sandbox/dry-run per run_command~~ — **RIDOTTO** il 2026-06-12 (finding
  declassato da 🟠 a 🟡, chiusura piena rinviata al sandbox OS).
- ✅ ~~Snapshot preventivo dei file~~ — CHIUSO il 2026-06-11.
- ✅ ~~T10 path traversal~~ — CHIUSO il 2026-06-11.

## Istituzioni di processo (attive dal 2026-06-11)

- **A — `reports/stato_progetto.md`**: questo file, aggiornato a fine task.
- **B — `reports/diff_sessione.md`**: riepilogo del diff a fine sessione.
- **C — Subagent revisore** (`.claude/agents/revisore.md`): 8 review completate
  (#1, #2, #3, #3-bis, #4, #5, #6, #7, #8), lezioni datate in
  `.claude/agents/memoria_revisore.md`.

## Prossimi passi (in ordine di priorità)

1. **Manutenzione snapshot in `gas doctor`** (riserve R2/R3: conteggio ref, gc
   oggetti orfani, dimensione snapshots.log; valutare retention ibrida).
2. Valutare cap output dedicato (più alto) per la futura pipeline Whisper
   (collegato a R2 review #7: `GAS_WINDOW_CHAR_CAP` configurabile via env).
