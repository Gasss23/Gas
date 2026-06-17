# 📊 STATO PROGETTO GAS

> Fotografia viva dello stato del progetto. Aggiornata a fine di ogni task.
> **2026-06-17 (CHIUSURA FASE 2 memoria — declassamento `unisci_contatti`, review #21
> APPROVATO, commit `0240161`):** il merge di lead è mutante e IRREVERSIBILE, quindi
> NON è più un tool autopilot ma **MANUTENZIONE UMANA** (rimosso da `tools_schema` e
> dal dispatcher; l'handler `_unisci_contatti` e il meccanismo nello store restano
> intatti). Stessa classe di restore-snapshot/`git gc` (solo umani). Di conseguenza
> il finding **R-crm-1b** scende da ✅CHIUSA a **🟡 MITIGATA** (il dedup cross-formato
> non è prevenuto; difesa preventiva "chiave canonica" non presa). Igiene: PUNTO 2
> coerenza whitespace in `_trova_contatto` (collasso su entrambi i lati del substring);
> PUNTO 3 chiude **R-crm-norm-1** (messaggi di successo con chiave canonica). **Strato B
> Vector DB ❄️ CONGELATO** (FTS5 basta); un-merge non necessario col merge manuale.
> Suite **132→135**. NESSUNA modifica a store.py.
> **2026-06-17 (doctor 402 onesto — review #20 APPROVATO, commit `7220c28`):**
> Il `doctor` mostrava `[KO]` allarmante per OpenRouter coi crediti esauriti (HTTP
> `402`), ma è un rung OPZIONALE gratuito (paracadute): stato benigno atteso. Nuovo
> helper PURO `_classify_provider_error` (429→QUOTA; 402 su rung opzionale→WARN; 402
> su rung obbligatorio→KO; resto→KO troncato 60 char) e il `doctor` ci delega.
> **A runtime nessuna modifica**: `run_turn` GIÀ scala da sé al rung successivo sul 402
> (§9, verificato dal vivo). Exit code del doctor INVARIATO (WARN/KO erano già
> "avvisi", non FAIL); zero token. Test T27a-d. Suite **128→132**.
> **2026-06-17 (Backup automatico del DB — review #19 APPROVATO, commit `cb99d1c`):**
> Rete di sicurezza per il dato più prezioso e meno rimpiazzabile del sistema
> (`.gas_memory.db`, che la "macchina del tempo" snapshot NON copre): difesa
> automatica dall'**auto-corruzione**. `backup_auto(min_interval_sec)` THROTTLED in
> `store.py` (copia SOLO se è passato l'intervallo E l'integrità `quick_check` è OK →
> un DB corrotto non viene mai copiato sopra i backup buoni) + rotazione pura
> (`keep=10`) + `integrity_check`. In `gas.py` `_memoria_backup_auto()` fail-safe §9
> chiamato UNA volta per turno (fuori dal loop) + override env
> `GAS_MEMORY_BACKUP_EVERY_SEC/_KEEP` + `doctor` sezione 8 "Memoria" (integrità/FTS5/
> backup, zero token). Backup OFF-MACHINE resta a FASE 5. Suite **123→128**.
> **2026-06-17 (fusione lead R-crm-1b CHIUSA + Vector DB Strato A — review #17/#18):**
> Due fette di FASE 2 in una sessione. (1) **R-crm-1b CHIUSA** via tool
> `unisci_contatti` + colonna `merged_into` (merge a lapide deterministico, niente
> fuzzy): lo stesso lead salvato con chiavi diverse (`'Anna'` vs `'anna@ex.com'`) si
> fonde senza perdere la storia (diario IMMUTABILE preservato: nessun UPDATE/DELETE).
> Review #17 RESPINTO (bug ordine ALTER/CREATE INDEX su DB legacy) → fix → APPROVATO
> (commit `956f367`). (2) **Vector DB Strato A FATTO** (commit `977148d`, review #18
> APPROVATO): ricerca testuale FTS5 sul diario, dentro lo STESSO `.gas_memory.db`
> (file singolo intatto), ZERO dipendenze, opzionale e fail-safe (build senza FTS5 →
> fallback substring). **Strato B (embedding semantici locali + sqlite-vec)
> deliberatamente RIMANDATO** al gate umano sulle dipendenze. Suite **112→123**.
> **2026-06-17 (normalizzazione chiavi lead — R-crm-1 CHIUSA, review #16 APPROVATO):**
> `normalizza_chiave` (trim/collasso-whitespace/lower, pura+idempotente, fail-safe) in
> `modules/memory/store.py`, applicata in `upsert_contatto` e `get_contatto_per_chiave`
> → niente più doppioni silenziosi del CRM. gas.py INVARIATO; invarianti motore intatte;
> DB dev vuoto (nessuna migrazione). Suite **106→110** 0 FAIL. Tracciati: residui R2/R3
> di 2b (`MEMORY_PIN_SCAN=200` hardcoded/numero magico) tra i finding 🟡; stato Vector DB
> (prossimo passo grosso FASE 2, NON avviato) nei Prossimi passi.
> **2026-06-15 (diagnosi snapshot — CHIUSA, non-bug):** verificato DAL VIVO che
> `_snapshot()` scrive ref PERSISTENTI (`commit-tree`+`update-ref`): chiamandolo a
> mano è nato `refs/gas/snapshots/...` su `.git/refs/gas/snapshots/`, poi rimosso
> con `update-ref -d` per ripristinare la baseline. Lo 0 ref in dev è ATTESO (qui
> si pilota Claude Code, non il runtime agentico che chiama `_snapshot`); i ~4427
> loose sono detrito git (stash + churn), NON snapshot recuperabili. La "macchina
> del tempo" è sana: era un check di pre-deploy VPS, non un difetto. Dettaglio in
> `reports/ultimo_report.md` (commit 57c050d).
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

- **Memoria FASE 2 — Backup automatico del DB ATTIVO (anti auto-corruzione)**
  (2026-06-17, review #19 APPROVATO, commit `cb99d1c`): difesa automatica del dato
  MENO rimpiazzabile del sistema (`.gas_memory.db`, NON coperto dagli snapshot git).
  `store.py`: `backup_auto(min_interval_sec)` THROTTLED (copia SOLO se passato
  l'intervallo E `integrity_check`/`quick_check` OK → un DB corrotto NON viene mai
  copiato sopra i backup buoni) + `backup()` esteso con rotazione pura
  (`_backup_retention`, `keep=DEFAULT_BACKUP_KEEP=10`, guardia `keep<=0` kill-switch)
  + timestamp con microsecondi (niente collisioni) + `_backup_files`/`ultimo_backup`.
  Copia nativa coerente (`src.backup(dst)`), file singolo / niente WAL INVARIATI.
  `gas.py`: `_memoria_backup_auto()` fail-safe §9 (memoria None/errore → turno
  prosegue) chiamato UNA volta per turno in `run_turn` dopo `_memoria_pin()`, FUORI
  dal `for _ in range(10)`; override env `GAS_MEMORY_BACKUP_EVERY_SEC` (default 6h) /
  `_KEEP` (default 10); `doctor` sezione 8 "Memoria" (integrità + FTS5 + età/numero
  backup, apre il DB solo se esiste, ZERO token). Backup = codice fidato in-process →
  niente sandbox/snapshot. Invarianti motore (`_get_window`/`_cap_window_chars`/
  `for _ in range(10)`/sandbox/snapshot) INVARIATE. Backup OFF-MACHINE (anti-disastro
  disco) resta a FASE 5. Test T26a-e. Suite **123→128**.
- **Memoria FASE 2 — Vector DB Strato A (ricerca FTS5 sul diario) ATTIVA**
  (2026-06-17, review #18 APPROVATO, commit `977148d`): primo strato del Vector DB
  di FASE 2. Tabella virtuale **FTS5 external-content** `diario_fts` + trigger
  `AFTER INSERT` (il diario è append-only → basta l'insert, immutabilità intatta) +
  backfill idempotente (`'rebuild'`) per il diario preesistente, tutto DENTRO lo
  stesso `.gas_memory.db` (invariante file singolo / backup banale preservato).
  ZERO dipendenze nuove. `cerca_diario` (ranking BM25) con `_fts_match` che sanifica
  l'input (token `\w+` quotati con prefix `*`) → niente crash di sintassi su query
  arbitraria. **OPZIONALE/fail-safe §9**: `_init_fts` in try/except SEPARATO dopo il
  commit dello schema → un build senza FTS5 lascia `fts_available=False` senza
  degradare `self.available`; `_ricorda(query)` prova FTS e RICADE sul substring
  storico (cascata). **Strato B (embedding semantici locali + sqlite-vec)
  RIMANDATO** al gate umano sulle dipendenze. Invarianti motore
  (`_get_window`/`_cap_window_chars`/`for _ in range(10)`/sandbox/snapshot) INVARIATE.
  Test T25a-e. Suite **118→123**.
- **Memoria FASE 2 — Fusione lead cross-formato: MECCANISMO ATTIVO, ma è
  MANUTENZIONE UMANA (non più tool autopilot)** (declassato il 2026-06-17, review
  #21 APPROVATO, commit `0240161`; meccanismo introdotto da review #17, commit
  `956f367`). Il merge di due schede dello STESSO lead salvato con chiavi
  semanticamente diverse (es. `'Anna'` vs `'anna@ex.com'`, che `normalizza_chiave`
  non unisce e non deve) è un **MERGE A LAPIDE** deterministico (niente fuzzy):
  colonna `merged_into` (NULL=vivo, valorizzato=lapide→canonico), migrazione
  idempotente `_ensure_columns` (ALTER ADD COLUMN + indice DOPO la colonna),
  `MemoryStore.unisci_contatti` completa l'anagrafica del canonico (COALESCE),
  ri-punta le lapidi (catena ≤1), marca il doppione. **NESSUN UPDATE/DELETE sul
  diario** (immutabilità preservata via `diario_di_contatto`); `lista_contatti`
  (→ pin/substring) esclude le lapidi; lo STATO del funnel NON si tocca.
  **DECLASSAMENTO (2026-06-17):** il merge è mutante e IRREVERSIBILE (lossy,
  COALESCE senza inverso pulito), quindi NON è più esposto al modello — rimossi
  l'entry da `tools_schema` e il ramo dal dispatcher; un modello in autopilot h24
  su VPS non deve poterlo invocare da sé (stessa classe del restore di snapshot e
  del `git gc`, solo umani: il dedup mancato è recuperabile, un merge errato no).
  Il MECCANISMO nello store resta INTATTO; l'handler `_unisci_contatti` resta
  richiamabile a mano. Test T24a-f (meccanismo, ora via store/handler) + T28a
  (tool fuori da schema+dispatcher). Suite **132→135**.
- **Memoria FASE 2 — Normalizzazione chiavi lead ATTIVA (chiude R-crm-1)**
  (2026-06-17, review #16 APPROVATO): la rubrica deduplicava solo a chiave ESATTA
  (UNIQUE), quindi col CRM autopilot `'anna@ex.com'` vs `'Anna '` diventavano due
  lead distinti (doppioni silenziosi → memoria che mente). Nuova funzione PURA
  `normalizza_chiave(Optional[str]) -> str` in `modules/memory/store.py` (coercizione
  a str + collasso whitespace via `str.split()` + `lower()`; idempotente; fail-safe
  §9: None/non-stringa → `""`). Applicata in UN unico punto logico ma nei DUE punti di
  confronto-esatto: `upsert_contatto` (scrittura, prima di INSERT/SELECT) e
  `get_contatto_per_chiave` (lookup per chiave). NIENTE fuzzy/euristica/merge: solo
  canonicalizzazione deterministica. L'asimmetria scrittura-esatto/lettura-substring
  resta INTATTA (`_trova_contatto` substring non toccato). `update_stato_contatto`
  lavora per id (già risolto via `get_contatto_per_chiave`) → coperto a monte.
  **gas.py INVARIATO**; `_get_window`/`_cap_window_chars`/`for _ in range(10)`/sandbox/
  snapshot/trigger-immutabilità del diario/schema fetta 1 INVARIATI. DB di sviluppo
  VUOTO → nessuna migrazione necessaria (se in futuro esistessero chiavi non
  normalizzate: script idempotente una-tantum, decisione umana — NON distruttivo).
  Test T23a-d (equivalenza chiavi/no-doppione, update con chiave non normalizzata,
  fail-safe None/vuota/non-str, idempotenza). Suite **106→110**.
- **Memoria FASE 2 — Scrittura CONTATTI dal loop (CRM autopilot) ATTIVA + riserve
  2b R1/R2/R3 CHIUSE** (2026-06-16, review #15 APPROVATO CON RISERVE): completa il
  ciclo della memoria — i lead ora si popolano DAL loop agentico, per via
  controllata (il modello NON scrive SQL grezzo). (A) `store.py`: aggiunto il solo
  lookup `get_contatto_per_chiave` (esatto su indice UNIQUE); schema/trigger/diario/
  upsert/update della fetta 1 INVARIATI. (B) `gas.py`: due tool in `tools_schema` +
  rami in `execute_tool_call`: `salva_contatto` (→ `upsert_contatto`, anagrafica,
  NON tocca lo stato) e `imposta_stato_contatto` (match ESATTO sulla chiave + valida
  lo stato contro `STATI_CONTATTO` prima del DB; lead inesistente/stato invalido →
  diniego, mai crash). Scrittura IN-PROCESS (codice fidato → niente sandbox/snapshot);
  ogni tool call resta tracciata nel diario (fetta 2a); `_riassumi_args` con casi
  dedicati. Fail-safe §9 ovunque. (C) Riserve 2b chiuse: **R1** → `_trova_contatto`
  (match esatto prioritario, nota di ambiguità sui match multipli invece di scegliere
  in silenzio; `imposta_stato_contatto` usa solo match esatto); **R2** → helper
  `_env_int` fail-safe + override env `GAS_MEMORY_PIN_CHARS/CONTACTS/EVENTS` (attributi
  d'istanza che shadowano i default di classe); **R3** → `MEMORY_PIN_SCAN=200`
  (finestra ampia e bounded) al posto dell'euristica `*5`. Test T22a-h (salva/aggiorna,
  dinieghi, lookup, R1/R2/R3, **round-trip CRM completo T22h**: rubrica popolata dal
  loop + diario + pin coerente). Invarianti motore (`_get_window`/`_cap_window_chars`/
  `_snapshot`/`_vet_command`/`providers`/payload/`for _ in range(10)`) INVARIATE.
  Suite **98→106**.
- **Memoria FASE 2 fetta 2b (lettura/iniezione) ATTIVA** (2026-06-16, review #14
  APPROVATO CON RISERVE): realizzata la proposta §FINALE della 2a. (1) **Iniezione
  always-on**: nuovo `_memoria_pin()` costruisce un blocco compatto (lead ATTIVI
  non in `STATI_CHIUSI` + poche azioni "significative", escluso il rumore di
  lettura `read_file`/`run_command`/`ricorda`) e lo appende AL MESSAGGIO SYSTEM in
  `run_turn` (`self.system_prompt + mem_pin`). Calcolato **UNA volta per turno**
  (no eco delle azioni in corso, no query ripetute nel loop a 10 iter). Il pin
  vive NEL system message, **FUORI dalla finestra** → `_get_window`/
  `_cap_window_chars` INVARIATI (unica modifica: `system_prompt` →
  `system_prompt + mem_pin`). Cap dedicato `MEMORY_PIN_CHAR_CAP=3000` che tronca
  il **TESTO** con marker (come `_cap_tool_output`), NON sequenze di messaggi
  (niente slicing, §5). (2) **Tool `ricorda()` di SOLA LETTURA** in `tools_schema`
  + ramo in `execute_tool_call`: pesca diario/contatti on-demand in-process
  (codice fidato, niente FS/rete → niente sandbox, niente snapshot), output capato
  da `_cap_tool_output`. (3) **Fail-safe §9**: memoria None/degradata → pin "" e
  turno prosegue, `_ricorda` → messaggio gentile, mai crash. Test T21a-h (filtro
  attivi/rumore, pin vuoto, ricorda per contatto/query/default, **iniezione nel
  payload REALE con finestra che parte da user — T21f**, fail-safe, cap del pin).
  Diff motore: l'unica riga della finestra cambiata è il payload. Suite **90→98**.
- **Memoria FASE 2 fetta 2a (aggancio scrittura) ATTIVA** (2026-06-16, review #13
  APPROVATO CON RISERVE): il diario della memoria è ora AGGANCIATO al loop di
  `run_turn`, **SOLO LATO SCRITTURA**. (1) `GasKernel.__init__`:
  `self.memory = MemoryStore(default_db_path(self.root))` con DOPPIA cintura
  fail-safe — `MemoryStore` degrada da sé (`available=False`) e un errore remoto
  all'avvio mette `self.memory=None`; il kernel non crasha mai. (2) Nel loop, per
  OGNI tool call, DOPO l'esecuzione (per catturare l'esito, **negativo incluso**),
  una riga di diario in-process via `MemoryStore.append_diario` — scrittura
  **IN-PROCESS** (codice fidato del kernel, **bypassa correttamente il sandbox
  bwrap** che vale solo per `run_command`). (3) Helper puri `_riassumi_args`
  (sintesi argomenti per tool), `_esito_sintetico` (`[OK]`/`[KO]` dal prefisso
  dell'output) e `_diario_log` (fail-safe §9: memoria None/degradata → warning
  nella scatola nera, il turno **CONTINUA**). Il `for _ in range(10)` (§8) è
  INVARIATO, l'ordine delle fasi pure. **VINCOLI rispettati:** CONTATTI NON
  toccati dal loop (solo diario); NESSUNA iniezione nel contesto
  (`_get_window`/`_cap_window_chars`/finestra INVARIATI); schema memoria fetta 1
  (`store.py`) INVARIATO. **Lato lettura/iniezione (fetta 2b) NON implementato:
  solo PROPOSTO** nel report §FINALE (cosa entra nell'iniezione, comporre il
  messaggio pinnato con `WINDOW_CHAR_CAP`, tool `ricorda()`, rischi sul
  round-trip). Test T20a-e (round-trip REALE zero token: multi-tool in ordine,
  esito KO + turno non interrotto, memoria corrotta e memoria None → round-trip
  OK). Diff motore: **167 inserzioni, 0 cancellazioni** (solo aggiunte). Suite
  **85→90**.
  - **Decisioni di design dell'aggancio** (registrate per la fetta 2b):
    - **A) Diario = log di OGNI tool call, esito incluso.** Il loop scrive
      indiscriminatamente (anche `read_file`/`ls`): il filtro del rumore di
      lettura è una scelta del LATO LETTURA (2b), non della scrittura — non si
      perde informazione a monte. I CONTATTI NON vengono scritti dal loop: la
      rubrica si popola altrove (tool dedicati / fetta successiva), il loop tocca
      solo il diario.
    - **B) Iniezione always-on (PROPOSTA 2b)** = contatti ATTIVI + pochi eventi
      diario RECENTI filtrati (escluso il rumore di lettura). Budget ~3000 char
      DENTRO `WINDOW_CHAR_CAP=24000`, via messaggio PINNATO; il diario profondo
      si pesca on-demand col tool di sola lettura `ricorda()` per non gonfiare la
      finestra. Da progettare con cura il punto d'inserimento rispetto a
      `_get_window`/`_cap_window_chars` (vedi report §FINALE).
- **Memoria FASE 2 fetta 1 (fondamenta storage) ATTIVA** (2026-06-15, review #12
  APPROVATO CON RISERVE): nuovo modulo `modules/memory/` (`__init__.py` + `store.py`),
  SOLO livello di persistenza, **NON agganciato a run_turn** (cablaggio solo PROPOSTO
  nel report §FINALE). DB SQLite **FILE SINGOLO** (`<root>/.gas_memory.db`, fuori da git,
  gitignorato con `-wal`/`-shm`), **niente WAL** per tenere il backup = copia del file.
  Due tabelle: `diario` append-only **IMMUTABILE** (trigger DB `BEFORE UPDATE`/`BEFORE
  DELETE` → `RAISE(ABORT)`, T19f) e `contatti` upsert-abile con `stato` mutabile
  (`nuovo..rifiutato/chiuso`, `STATI_CHIUSI` = invalidati). Invariante separazione ruoli:
  `upsert_contatto` non tocca lo stato (solo anagrafica), la transizione passa SOLO da
  `update_stato_contatto`. Scritture IN-PROCESS via `sqlite3` (bypassano correttamente il
  sandbox bwrap: memoria = codice fidato del kernel). Fail-safe §9: DB mancante creato,
  DB corrotto → warning + degrado, mai crash. `backup()` nativo timestampato. Estensibile
  (schema = tupla di DDL idempotenti). Test T19a-j zero token. Suite **75→85**.
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
  **135 PASS, 0 FAIL** (2026-06-17). Dai 132 si aggiungono i 3 T28 (declassamento
  `unisci_contatti`: T28a fuori da schema+dispatcher con meccanismo manuale intatto,
  T28b coerenza whitespace in `_trova_contatto`, T28c chiave canonica nei messaggi);
  i T24a/c/d migrati da `execute_tool_call` all'handler `_unisci_contatti` (stesso
  output, restano verdi). Dai 128 si aggiungono i 4 T27 (classificazione
  errori provider nel doctor: 429→QUOTA via status/testo, 402 opzionale→WARN, 402
  obbligatorio→KO, generico→KO troncato a 60). Dai 123 si aggiungono i 5 T26 (backup memoria:
  integrità sano/corrotto, backup+rotazione+retention pura, throttling, skip su
  corruzione, kernel fail-safe + memoria None). Dai 118 si aggiungono i 5 T25 (Vector DB
  Strato A / FTS5: match per radice + query ostile senza crash, ranking BM25,
  backfill su diario legacy, integrazione `ricorda(query)` coi vincoli T21d
  preservati + diario immutabile con indice attivo, fallback substring se FTS
  assente). Dai 112 i 6 T24 (fusione lead R-crm-1b: lapide+vecchia chiave→canonico,
  storia preservata, fail-safe/idempotenza, pin senza lapidi, catena ≤1, migrazione
  DB legacy). Storico: dai 110 si aggiungono i 2 T23e/f
  (coerenza scrittura-normalizzata ↔ lettura-substring: il lead salvato con chiave
  non normalizzata resta trovabile via `ricorda` con varianti case/spazi — T23e; e
  onestà sul limite APERTO R-crm-1b: la normalizzazione NON fonde identità
  cross-formato, due record restano due — T23f). Prima, dai 106 i 4 T23a-d
  (normalizzazione chiavi lead R-crm-1: equivalenza chiavi/no-doppione, update con
  chiave non normalizzata, fail-safe None/vuota/non-str, idempotenza). Storico: dai 98 gli 8 T22 (scrittura
  contatti dal loop + chiusura R1/R2/R3: salva/aggiorna, dinieghi, lookup store,
  match esatto+ambiguità, override env+fail-safe, scan robusto del rumore,
  round-trip CRM completo con diario+pin). Storico dai 90 → 98: gli 8 T21 (lato lettura
  fetta 2b: pin filtra attivi/rumore, pin vuoto, `ricorda` per contatto/query/
  default, iniezione nel payload reale con finestra che parte da user, fail-safe,
  cap del pin). Dai 85 → 90: i 5 T20 (aggancio diario a `run_turn`,
  round-trip REALE: T20a multi-tool in ordine, T20b esiti `[OK]`, T20c tool
  fallito → `[KO]` + turno non interrotto, T20d memoria corrotta → round-trip OK,
  T20e memoria None → nessun crash). Dai 75 → 85: i 10 T19 (memoria fetta 1). Dai
  61 si aggiungono: 3 T16 (TASK A,
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

- ✅ **Riserve Memoria FASE 2 fetta 2b — R1/R2/R3 CHIUSE** (review #15, 2026-06-16):
  R1 (match contatto ambiguo) → `_trova_contatto` con priorità al match esatto e nota
  di ambiguità; R2 (costanti hardcoded) → override env `GAS_MEMORY_PIN_*` via `_env_int`
  fail-safe; R3 (euristica `*5`) → `MEMORY_PIN_SCAN=200` bounded. `DIARIO_NOISE_TIPI`
  resta hardcoded di proposito (non un tetto numerico). Dettaglio nella voce CRM sopra.
- ✅ **R-crm-1 (parte case/whitespace) — CHIUSA** (2026-06-17, `cdf764a`, review #16):
  chiavi che differiscono solo per maiuscole/whitespace della STESSA stringa
  (`"Anna"` / `" ANNA "` → un record) risolvono allo stesso contatto via
  `normalizza_chiave` (trim/collasso-whitespace/lower, pura+idempotente, fail-safe),
  applicata sia in `upsert_contatto` sia in `get_contatto_per_chiave` (T23a/b). La
  lettura substring resta coerente con la scrittura normalizzata (T23e). Niente
  fuzzy/merge (fuori scope di proposito). Dettaglio nella voce motore in cima.
- 🟡 **R-crm-1b (identità cross-formato) — MITIGATA, non prevenuta** (declassata da
  ✅CHIUSA il 2026-06-17, `0240161`, review #21; meccanismo da `956f367`/review #17):
  lo stesso lead con chiavi semanticamente DIVERSE (es. `anna@ex.com` vs `Anna`) —
  che `normalizza_chiave` non unisce e non deve (T23f presidia il confine: la
  normalizzazione lessicale non indovina mai) — NON è **prevenuto**: il dedup
  cross-formato a runtime può ancora accadere (a volte solo nome, a volte solo
  email per la stessa persona). Esiste un **meccanismo di merge a lapide**
  (`MemoryStore.unisci_contatti` + `merged_into`, non distruttivo, immutabilità del
  diario preservata) ma è **MANUTENZIONE UMANA**: il modello NON lo invoca più in
  autopilot (rimosso da `tools_schema`/dispatcher), perché il merge è mutante e
  irreversibile (un merge errato non si annulla; il dedup mancato sì). La difesa
  PREVENTIVA candidata — **policy di chiave canonica** (preferire SEMPRE l'email
  quando disponibile) — resta NON presa (scelta umana). Finché il merge è manuale,
  un **un-merge non è necessario** (registrato, nessun impegno).
- 🟡 **Riserve CRM contatti dal loop** (R-mem-crm, review #15, minori non bloccanti):
  (R-crm-2) `int(c["id"])` in `_imposta_stato_contatto` assume id convertibile (sempre
  vero con PK INTEGER SQLite, e protetto dal try/except globale) — cosmetico.
  (R-crm-norm-1 — ✅ **CHIUSA** il 2026-06-17, `0240161`, review #21) l'eco testuale
  della chiave nei messaggi di successo di `_salva_contatto`/`_imposta_stato_contatto`
  ora mostra la forma CANONICA persistita (`normalizza_chiave`), così schermo e DB
  coincidono (T28c). Era puramente cosmetico (il dato nel DB era già corretto).
- 🟡 **Costanti del pin memoria: residuo `MEMORY_PIN_SCAN`** (R2 di 2b, residuo dopo
  review #15): le tre costanti principali del pin (`MEMORY_PIN_CHAR_CAP/CONTACTS/
  EVENTS`) sono GIÀ overridabili via env (`GAS_MEMORY_PIN_*`, chiuse in #15), ma
  `MEMORY_PIN_SCAN=200` resta HARDCODED senza override env — stessa classe di
  `WINDOW_CHAR_CAP`/`SNAPSHOT_KEEP`. Valutare un `GAS_MEMORY_PIN_SCAN` (fail-safe via
  `_env_int`) al deploy VPS. Non bloccante. NB: `DIARIO_NOISE_TIPI` resta hardcoded di
  proposito (non è un tetto numerico).
- 🟡 **Euristica della finestra di scansione del pin** (R3 di 2b, residuo dopo review
  #15): l'euristica originale `MEMORY_PIN_EVENTS*5` è stata SOSTITUITA in #15 da
  `MEMORY_PIN_SCAN=200` (finestra ampia e bounded), ma 200 resta un **numero magico**
  scelto a priori, da tarare con dati reali quando il diario avrà volume (oggi il
  diario è piccolo, la scelta è conservativa). Non bloccante.
- 🟡 **Riserve Memoria FASE 2 fetta 2a** (R-mem2a, review #13, minori non
  bloccanti): (R1) `_esito_sintetico` inferisce `[OK]`/`[KO]` dal PREFISSO
  testuale dell'output (`Errore eseguendo`/`Operazione negata`): un tool a esito
  POSITIVO che stampasse contenuto iniziante con quelle stringhe verrebbe
  mis-etichettato `[KO]`. Imprecisione SOLO sull'etichetta del diario, NON sulla
  logica del kernel (la storia inviata ai provider è intatta). Difesa candidata:
  marcatore d'esito strutturato restituito da `execute_tool_call`, non parsing del
  testo. (R2) una riga di diario per OGNI tool call dentro il loop → verbosità che
  cresce coi turni a molte tool call; coerente con la nota PARK "Retention del
  diario" già registrata (quando il volume lo richiederà: archiviazione/export,
  MAI DELETE).
- 🟡 **Riserve Memoria FASE 2 fetta 1** (R-mem, review #12, minori non bloccanti):
  (R1) i trigger di immutabilità del `diario` coprono UPDATE/DELETE ma NON
  `INSERT OR REPLACE` sulla PK con i default SQLite (`recursive_triggers` OFF): il
  DELETE implicito di REPLACE non li attiva. Portata reale limitata — `append_diario`
  fa solo INSERT puro; il buco si apre solo a chi ha già accesso diretto al file `.db`.
  Docstring precisata col caveat. Da chiudere alla passata di hardening (terzo trigger
  `BEFORE INSERT` che vieta id già esistente, oppure `recursive_triggers ON`). (R2)
  costanti hardcoded (`DEFAULT_DB_FILENAME`, `timeout=10`, `n=20` di `diario_recente`),
  come `WINDOW_CHAR_CAP`/`SNAPSHOT_KEEP`; valutare override `GAS_MEMORY_DB` (path del DB
  su volume persistente) al cablaggio su VPS.

### PARK — Memoria FASE 2 (registrati, NON urgenti, nessun impegno)
1. **Retention del diario**: cresce per sempre (stessa classe della retention snapshot).
   Quando il volume lo richiederà: archiviazione/export + rotazione del file storico —
   MAI `DELETE` (violerebbe l'immutabilità).
2. **GDPR / dati personali dei lead** (UE): terreno legale da guardare a **FASE 4** (lead
   generation). Consenso, diritto all'oblio (in tensione con l'immutabilità del diario),
   minimizzazione. Non risolto ora, solo registrato.

## Istituzioni di processo (attive dal 2026-06-11)

- **A — `reports/stato_progetto.md`**: questo file, aggiornato a fine task.
- **B — `reports/diff_sessione.md`**: riepilogo del diff a fine sessione.
- **C — Subagent revisore** (`.claude/agents/revisore.md`): **21 review completate**,
  ultima la **#21** (declassamento `unisci_contatti` a manutenzione umana, 2026-06-17,
  APPROVATO). Elenco in ordine: #1, #2, #3, #3-bis, #4, #5, #6, #7, #8, #9 (TASK B),
  #10 (TASK C), review hook SessionEnd TASK 1 (2026-06-15, APPROVATO), #12 Memoria
  FASE 2 fetta 1 (APPROVATO CON RISERVE), #13 fetta 2a (APPROVATO CON RISERVE),
  #14 fetta 2b (APPROVATO CON RISERVE), #15 CRM contatti dal loop + chiusura R1/R2/R3
  (APPROVATO CON RISERVE), #16 normalizzazione chiavi lead / chiusura R-crm-1
  (APPROVATO), #17 fusione lead R-crm-1b (RESPINTO per bug d'ordine ALTER/CREATE INDEX
  su DB legacy → APPROVATO dopo fix + T24f), #18 Vector DB Strato A / FTS5 (APPROVATO),
  #19 backup automatico del DB (APPROVATO, 2 note cosmetiche), #20 doctor 402→WARN sui
  rung free (APPROVATO), #21 declassamento `unisci_contatti` (APPROVATO, 1 nota
  cosmetica). Lezioni datate in `.claude/agents/memoria_revisore.md`.

## Prossimi passi (in ordine di priorità)

0. **Vector DB — STRATO A FATTO, STRATO B ❄️ CONGELATO (non "prossimo passo").**
   Deciso il 2026-06-17 (chiusura FASE 2 memoria): la keyword search FTS5 (Strato A,
   `977148d`, dentro lo stesso `.db`, zero dipendenze) **copre i bisogni attuali**.
   Lo **Strato B** (embedding semantici LOCALI `fastembed`/ONNX + `sqlite-vec`, con
   FTS5 come fallback) **NON è in coda di lavoro**: si rivaluta SOLO se il funnel reale
   dimostra che la ricerca lessicale non basta. È anche l'unica parte che aggiunge
   DIPENDENZE → comunque dietro **OK umano esplicito** (CLAUDE.md §10, "robustezza
   prima della potenza"). Scartati: embedding via API (contro zero-token/offline) e
   store separati Chroma/FAISS (romperebbero il file singolo). NB: un **un-merge** dei
   lead è **NON necessario** finché il merge è MANUALE (registrato, nessun impegno).
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

1. **Snapshot: 0 ref permanenti + ~4427 oggetti loose** (da `gas doctor` sez.7) —
   **check di pre-deploy VPS, NON un bug** (diagnosi 2026-06-15, commit 57c050d).
   (a) `git gc` OPT-IN (vedi Prossimo passo #3) per riassorbire i loose accumulati;
   resta utile, ma i loose sono detrito git (stash + churn dev), non snapshot da
   salvare. (b) La domanda "gli snapshot vengono davvero creati/persistiti?" è
   **RISOLTA**: il meccanismo scrive ref PERSISTENTI su `.git/refs/gas/snapshots/`
   (provato dal vivo: ref nato e poi rimosso con `update-ref -d`). Lo 0 ref in dev
   è ATTESO perché qui si pilota Claude Code, non il runtime agentico che invoca
   `_snapshot` (solo `run_command`/`write_file` lo fanno). **Sul VPS** il kernel
   eseguirà davvero quei tool → gli snapshot nasceranno e resteranno: lì `gas
   doctor` sez.7 con 0 ref + molti loose diventa un segnale ANOMALO da rivalutare
   (in dev no). Da tenere come voce di checklist pre-deploy, non come difetto.
2. **OpenRouter free risponde in ~28 s** (4° rung, modalità degradata, osservato
   in `gas doctor`). Conferma che il rung free remoto è un paracadute lento, non
   un piano operativo. Rafforza il piano **ollama-su-VPS** (5° rung, pavimento
   offline): il VPS va **dimensionato per `qwen2.5:7b-instruct`** (RAM/CPU
   sufficienti a tenere il modello in locale) così da avere un fallback rapido e
   a costo zero senza dipendere dalla latenza di OpenRouter.
