# 📊 STATO PROGETTO GAS

> Fotografia viva dello stato del progetto. Aggiornata a fine di ogni task.
> **2026-06-15 (task minimo):** i commit della feature `scrivi rep` ora usano il
> prefisso `chore(scrivi-rep):` (era `scrivi rep:`) per filtrarli nel log
> (`git log | grep -v chore`); solo la stringa del messaggio in `scrivi_rep.sh` +
> riga doc in CLAUDE.md §3. Comportamento, path e file (`reports/ultima_risposta.md`,
> versionato per sync multi-device) INVARIATI. Verifica reale in repo usa-e-getta
> (push incluso) OK.
> Ultimo aggiornamento: **2026-06-15** (sessione di CHIUSURA/VERIFICA: A1–A6 superate
> — i tre commit TASK 1/2/3 sono REALI e combaciano, suite **75/75** zero token,
> hook usa-e-getta **9/9** incl. prefix-match dell'invariante; `scrivi_rep.sh`
> verificato load-bearing → **STOP, NON ritirato**, decisione all'umano. Motore e
> hook INVARIATI in questa sessione).
> Storico: TASK 1 hook SessionEnd additivo/condizionale + commit esplicito dei report
> (chiude bug sovrascrittura — revisore APPROVATO); TASK 2 sfoltimento finding chiusi
> → `finding_archiviati.md`; TASK 3 note VPS.

## Stato del motore

- **Manutenzione snapshot ATTIVA** (2026-06-14, FASE 1 — TASK C, review #10
  APPROVATO CON RISERVE): retention dei ref `refs/gas/snapshots/*` passata da
  count-based pura a **IBRIDA** = UNIONE di (ultimi `SNAPSHOT_KEEP=100`) e (più
  giovani di `SNAPSHOT_KEEP_DAYS=7`): i recenti sopravvivono anche a una sessione
  che ruota >100 ref. Helper PURI testabili `_ref_age_epoch` (epoch dal NOME del
  ref; non parsabile → si TIENE, conservativo) e `_snapshot_retention` →
  `(keep, drop)`. **Prudenza (§10):** nessun prune distruttivo né `git gc`
  automatico — i ref oltre policy si rimuovono con `update-ref -d` (oggetto
  RECUPERABILE fino a `git gc`) e la rimozione è LOGGATA riga per riga.
  `reports/snapshots.log` gitignorato + rotazione semplice `.1` al cap
  `SNAPSHOT_LOG_MAX_BYTES`. `doctor` sezione 7 "Snapshot": SOLO REPORT (conteggio
  ref + hint oggetti loose via `count-objects` + dimensione log); gc OPT-IN
  manuale. Test T18a-f (retention pura, zero git) + T11f riadattato al ramo
  count. Suite **75/75**.
- **Integrità paracadute free ATTIVA** (2026-06-14, FASE 2 — TASK B, review #9
  APPROVATO CON RISERVE): `doctor` ora verifica l'ESISTENZA e la CAPACITÀ TOOL
  del modello free OpenRouter, non solo la presenza della chiave. Forma API
  sondata dal vivo prima di progettare: GET `<base>/models/<slug>/endpoints` →
  `{data:{...endpoints:[{supported_parameters:[...]}]}}` (`supported_parameters`
  è PER-ENDPOINT; `tools` nella lista = function calling). Nuova voce
  "Paracadute / modello free" SOLO se `OPENROUTER_API_KEY` presente: 404 → WARN
  (assente/rinominato, VISIBILE); `tools` assente → WARN (degrado a solo-testo);
  presente+tool-capable → OK. Sono GET di METADATI, NESSUNA generazione →
  "doctor non consuma token" intatto. `run_turn`: SOLO osservabilità (sez.9) —
  brain con modello fuori da `TOOL_CAPABLE_MODELS` → `logging.warning` nella
  scatola nera, NESSUN skip, ordine del fallback INVARIATO; rilevamento del
  degrado a runtime RIMANDATO (falsi positivi). Helper `_classify_free_model`
  (3 rami), `_probe_free_model` (`_fetch` mockabile), `_model_tool_capable`.
  Test T17a-e (zero token, mock dei tre rami). Suite 64→69.

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
  **75 PASS, 0 FAIL** (2026-06-14). Dai 61 si aggiungono: 3 T16 (TASK A,
  `_parse_mode` condiviso init/doctor), 5 T17 (TASK B, paracadute free:
  404/no-tools/tools + classify + registro tool-capability), 6 T18 (TASK C,
  retention ibrida pura) con T11f riadattato. Storico: dai 52 i 9 check T14
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

> I finding CHIUSI/RISOLTI/RIDOTTI sono stati archiviati in
> `reports/finding_archiviati.md` (una riga datata ciascuno; dettaglio integrale
> nella history git). Qui restano SOLO i finding ATTIVI.

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
- 🟡 **Falsi positivi del path-check su argomenti non-path** (R3, review #4):
  un pattern grep tipo `/etc/cron` viene risolto come path assoluto e il
  comando negato. Fail-closed (lato sicuro), ma limite di usabilità da
  conoscere.
- 🟡 **Riserve TASK C** (R-snap, review #10, minori non bloccanti):
  (1) `SNAPSHOT_KEEP_DAYS`/`SNAPSHOT_LOG_MAX_BYTES` non configurabili via env
  (come `WINDOW_CHAR_CAP`); (2) soglie magiche inline in doctor
  (`loose>10000`, `n_refs>SNAPSHOT_KEEP`), cosmetico; (3) rotazione log a 1 sola
  generazione (`.1` sovrascrive; la storia vera sta nei ref git); (4) manca test
  dedicato per la rotazione `.1` e per i 3 check di doctor sezione 7 (provati
  dal vivo: sezione Snapshot OK, nessun crash). La logica PURA di retention è
  invece coperta dai T18.
- 🟡 **Degrado a solo-testo non verificato a runtime** (R2, review #5) —
  **METÀ DETERMINISTICA CHIUSA** il 2026-06-14 (TASK B): `doctor` rileva a freddo
  la mancanza di `tools` (WARN) e `run_turn` logga un warning se un brain monta un
  modello fuori da `TOOL_CAPABLE_MODELS` (osservabilità sez.9, nessun cambio di
  cascata). RESTA APERTO il rilevamento del degrado PER-TURNO a runtime
  (rimandato di proposito: rischio falsi positivi).
- 🟡 **Riserve TASK B** (R-free, review #9, minori non bloccanti): (1) due rami
  di sicurezza degli helper free senza test dedicato (solo copertura, non
  sicurezza); (2) il warning osservabilità in `run_turn`, se un modello senza
  tool entrasse in cascata, si ripeterebbe fino a 10× per turno nel log
  (de-dup possibile, non urgente — oggi tutti i modelli sono tool-capable).
- 🟡 **Riserve TASK 1** (hook SessionEnd, review revisore 2026-06-15, minori non
  bloccanti): (1) il percorso `/workspaces/Gas` è hardcoded nello script (override
  `GAS_REPO_DIR` solo per i test) — da rendere configurabile al passaggio su VPS;
  (2) l'invariante che toglie il motore dallo staging è una RETE di sicurezza, non
  la difesa primaria (che resta l'allowlist esplicita: l'hook fa `git add` solo di
  reports/, *.md, .gas_history.json, mai del motore).
- 🟡 **Allowlist `git add` dell'hook SessionEnd è all-or-nothing** (verifica
  2026-06-15, minore, fail-safe): `git add reports/ '*.md' .gas_history.json`
  fallisce in blocco (`fatal: pathspec did not match`, rc=128) e non stagia NULLA se
  `.gas_history.json` mancasse. È fail-SAFE (mancato auto-commit, MAI commit
  indesiderato) e il workflow §3 copre i deliverable; in steady-state
  `.gas_history.json` c'è sempre → benigno. Sul VPS, se mai mancasse all'avvio,
  l'auto-commit della history salterebbe silenziosamente: tenerlo a mente.

## Istituzioni di processo (attive dal 2026-06-11)

- **A — `reports/stato_progetto.md`**: questo file, aggiornato a fine task.
- **B — `reports/diff_sessione.md`**: riepilogo del diff a fine sessione.
- **C — Subagent revisore** (`.claude/agents/revisore.md`): 11 review completate
  (#1, #2, #3, #3-bis, #4, #5, #6, #7, #8, #9 TASK B, #10 TASK C, + review hook
  SessionEnd TASK 1 del 2026-06-15 — APPROVATO), lezioni datate in
  `.claude/agents/memoria_revisore.md`.

## Prossimi passi (in ordine di priorità)

1. **Rilevamento PER-TURNO del degrado a solo-testo** (metà aperta di R2 #5):
   oggi solo osservabilità a freddo (doctor) + warning statico (run_turn).
   Rimandato per i falsi positivi: progettare con cura prima di attivare.
2. Valutare cap output dedicato (più alto) per la futura pipeline Whisper
   (collegato a R2 review #7: `GAS_WINDOW_CHAR_CAP` configurabile via env);
   nello stesso giro valutare `GAS_SNAPSHOT_KEEP_DAYS` configurabile (riserva
   TASK C #1).
3. `git gc` OPT-IN dietro flag esplicito in `gas doctor` (oggi solo reportato):
   azione irreversibile, va progettato il consenso umano esplicito.

## Note operative VPS — non per oggi

> Dati operativi osservati il 2026-06-15 (TASK 3). NON agire ora: registrati per
> la pianificazione del deploy su VPS (FASE 5).

1. **Snapshot: 0 ref permanenti + ~4427 oggetti loose** (da `gas doctor` sez.7).
   Due implicazioni da chiarire PRIMA della VPS: (a) pianificare un `git gc`
   OPT-IN (vedi Prossimo passo #3) per riassorbire gli oggetti loose accumulati;
   (b) **VERIFICARE se gli snapshot vengono davvero creati/persistiti**: 0 ref
   permanenti potrebbe significare che la "macchina del tempo" non resta armata
   tra le sessioni (i ref `refs/gas/snapshots/*` sono vivi durante la sessione ma
   poi spariscono?). Da indagare: la rete anti-autodistruzione è effettivamente
   attiva in steady-state o solo intra-sessione?
2. **OpenRouter free risponde in ~28 s** (4° rung, modalità degradata, osservato
   in `gas doctor`). Conferma che il rung free remoto è un paracadute lento, non
   un piano operativo. Rafforza il piano **ollama-su-VPS** (5° rung, pavimento
   offline): il VPS va **dimensionato per `qwen2.5:7b-instruct`** (RAM/CPU
   sufficienti a tenere il modello in locale) così da avere un fallback rapido e
   a costo zero senza dipendere dalla latenza di OpenRouter.
