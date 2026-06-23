# ARCHIVIO STATO PROGETTO GAS

> Storico sessioni, dettaglio componenti del motore, finding chiusi.
> NON viene ricaricato in sessione — consultare solo quando serve il contesto storico.
> File vivo: `reports/stato_progetto.md`
> Archiviato il: 2026-06-23 (split anti-costo-token)

---

## Changelog sessioni (cronologico)

> **2026-06-23 (CI — run auto-verificabile / job summary + gate sandbox — SOLO-WORKFLOW,
> niente revisore):** chiusa la lacuna di osservabilità emersa verificando la run precedente
> (`4f8d014`): l'esito bwrap e il conteggio PASS/FAIL/SKIP stavano SOLO nel log dietro auth
> (`/logs` → HTTP 403, `gh` assente), e lo smoke-test `|| echo BWRAP_FAIL` rendeva lo step
> sempre "success" nascondendo il fallimento del sandbox → impossibile distinguere "sandbox
> attivo + 2 FAIL attesi (T9a/T9c)" da "BWRAP_FAIL + 7 FAIL" senza scaricare lo zip. `ci.yml`
> (`5dab394`): smoke-test esposto come output (`smoke1`/`smoke2` in `$GITHUB_OUTPUT`); step
> **Job summary** (`if: always`, `set +e`) che scrive in `$GITHUB_STEP_SUMMARY` (pagina della
> run, niente zip/auth) esito bwrap + riga RIEPILOGO + SKIP + lista FAIL; step **Gate — sandbox
> OS attivo** (`if: always`, per ultimo) che va rosso con `::error::` SOLO se `smoke2 != BWRAP_OK`
> → distingue "rosso da sandbox" (STOP GATE → micro-task skip-on-CI, tocca `tests/`, con revisore)
> da "rosso da T9a/T9c" (atteso); suite con `tee` + `pipefail` → exit code NATIVO preservato, il
> verdetto NON è mai mascherato (niente allowlist di test nel workflow = niente parsing fragile).
> YAML validato in locale (PyYAML, 7 step). `tests/`/`gas.py` INVARIATI. ZERO token LLM. NUOVA
> riserva CI-4: il job resta rosso finché T9a/T9c (env) sono rossi anche col sandbox attivo →
> verde pieno = micro-task su `tests/`, fuori scope solo-workflow. **VERIFICATO (run `cd46d0f`,
> API pubblica): step "Gate — sandbox OS attivo" = SUCCESS → BWRAP_OK → il sandbox OS si attiva
> sul runner GitHub. Obiettivo "sandbox OS esercitabile in CI" RAGGIUNTO; job ancora rosso per i
> soli T9a/T9c attesi. Conteggio esatto nel Job Summary della run (senza zip).**
> **2026-06-23 (CI — abilitazione del sandbox OS / bubblewrap nel runner — SOLO-WORKFLOW,
> niente revisore):** la prima run CI era 160 PASS / 7 FAIL / 4 SKIP su Linux; 5 FAIL da
> ASSENZA bwrap (T11c2/T11e/T12a/T12c/T12e: `os_strict` + runner senza bwrap → `run_command`
> negato fail-closed) + 4 SKIP (T13a/b/c/e, mai girati in automatico). FASE 0 sonda (sola
> lettura) su `tests/test_unit_kernel.py`: T13a/b/c/e gated da `_probe_os_sandbox()` reale
> (righe 380/391+) → girano con bwrap; T11c2/.../T12e dipendono dall'esecuzione di run_command;
> **PIVOT T13d/T13d2 FORZANO `os_sandbox_available=False` sull'istanza (righe 434/443), NON
> dipendono dall'ambiente reale** → installare bwrap NON li flippa. Nessun test PASS dipende
> dall'assenza reale → VIA LIBERA solo-workflow. FETTA 1 (`919f677`): step nuovo in `ci.yml`
> prima della suite — `apt-get install bubblewrap` + smoke-test esplicito (BWRAP_OK/FAIL nel
> log) + rilassamento unprivileged userns via sysctl (ubuntu-24.04 li restringe via AppArmor;
> benigno sul runner EFFIMERO, NON tocca `os_strict` del VPS) + re-smoke-test; suite invariata.
> `tests/`/`gas.py` INVARIATI. ZERO token LLM. **DECISIONE UMANA:** verificare la run post-push
> (smoke-test BWRAP_OK/FAIL; 5 bwrap + 4 T13 col sandbox; conteggio finale). STOP GATE: se
> BWRAP_FAIL persiste dopo sysctl → micro-task 2 (skip-on-CI, tocca `tests/`, con revisore),
> NON fatto qui. T9a/T9c (env API/storia) restano fuori scope → micro-task 2.
> **2026-06-23 (Infrastruttura di osservabilità di fine sessione — CI + handoff — task
> NON-motore, niente revisore):** due fette di sola infrastruttura/doc, motore INTATTO.
> FETTA 1: `.github/workflows/ci.yml` (NUOVO) — `on: push`, ubuntu-latest, Python 3.11
> (= venv 3.11.9), installa `requirements.txt`, lancia `tests/test_unit_kernel.py`.
> Verde/rosso OGGETTIVO via **exit code nativo** del runner (`sys.exit(1 if FAIL else 0)`,
> CONFERMATO in sonda: exit=1 con 9 FAIL) → nessun parsing, nessuna modifica a `tests/`.
> ZERO token LLM: niente API key/secrets/provider/`gas doctor`. bubblewrap NON installato
> in v1 di proposito (comportamento dei test OS-specifici in CI da decidere dalla PRIMA RUN).
> `requirements.txt`: aggiunto `onnxruntime>=1.17` esplicito (backend fastembed) per non far
> saltare i blocchi vettoriali T30/T31/T32 in CI (R-reidx-deps). FETTA 2: `reports/handoff.md`
> (NUOVO, istituzione D) — dossier di fine sessione compilato su questa sessione come primo
> esempio reale; AGGREGA `ultimo_report.md` senza sostituirlo + aggiunge lo stato CI. CLAUDE.md
> §3: istituzione D + "tre"→"quattro". **DECISIONE UMANA APERTA:** verificare la PRIMA RUN CI
> su GitHub Actions (verde/rosso + PASS/FAIL/SKIP); WSL2 NON accessibile (nessuna distro) →
> la prima run è l'unica sonda Linux. Se FAIL ambientali (bwrap/env) persistono su Linux,
> gestirli è TASK SEPARATO che tocca `tests/` (→ revisore), NON fatto qui. Suite Windows in
> sonda invariata: 158/9 (9 FAIL ambientali noti). Commit: `0eb5322` (CI), `d135bc7` (handoff).
> **2026-06-21 (R-wire-1 — soglia semantica `VEC_MIN_SIM` env-configurabile — review #28
> APPROVATO):** chiusa la parte AZIONABILE dell'item aperto #1. `gas.py`: nuovo helper PURO
> `_env_float(name, default, min_val=0.0, max_val=1.0)` fail-safe come `_env_int`/`_env_flag`
> (assente→default; non parsabile→default + `logging.warning` §9; fuori range→clamp a
> [min_val,max_val]; default `max_val=1.0` perché il coseno di vettori normalizzati è ≤1).
> `__init__` risolve `self.VEC_MIN_SIM = _env_float("GAS_VECTORS_MIN_SIM", GasKernel.VEC_MIN_SIM)`,
> stesso pattern di `VEC_CATCHUP_MAX`; il call-site del retrieval semantico (`min_sim=self.VEC_MIN_SIM`)
> usa l'attributo d'istanza → override NON inerte. Default di classe `VEC_MIN_SIM = 0.30` INVARIATO
> → con env assente comportamento bit-identico. NON serve redeploy per ri-tarare. Resta SOLO la
> ri-taratura del valore sul primo diario reale (deploy-dependent) → CHECKLIST pre-deploy VPS.
> Test T22f2 (assente→default, valido→0.45 via kernel reale, sporco→default classe, clamp alto→1.0,
> clamp basso→0.0; ripristino env nel `finally`); ridondanza minore segnalata dal revisore corretta
> in sessione (la seconda asserzione duplicata sostituita da un parse a livello helper su valore
> presente). Invarianti motore intatte; nessun antipattern §5. **Suite Windows (venv): 158 PASS,
> 9 FAIL** — i 9 FAIL sono TUTTI pre-esistenti/ambientali (bwrap T11/T12/T13d2, env API/storia
> T9a/T9c, WinError32 backup T26b): VERIFICATO su HEAD pulito (stash) = 157 PASS / **stessi 9 FAIL**,
> quindi R-wire-1 aggiunge esattamente +1 PASS (T22f2) e 0 regressioni. NB il "158/8" dei report
> precedenti era un conteggio leggermente datato dei FAIL ambientali Windows (un test snapshot
> flippa per stato git accumulato, NON per codice).
> **2026-06-20 (Backup off-machine + doctor memoria rumoroso — review #26/#27 APPROVATI
> CON RISERVE, commit motore `56a6dc3`, suite 158/8 FAIL pre-esistenti Windows):**
> TASK A: nuovo `backup_offsite_auto()` in `store.py` (throttle SEPARATO, cintura integrita',
> fail-safe sec.9); `backup_cmd()` SOLO-CLI in `gas.py` (`gas backup`, NON in tools_schema);
> `_memoria_backup_auto()` esteso col blocco off-site condizionale; doctor sez.8 check off-site
> dir+eta' indipendente da `mem.available`. Env: `GAS_MEMORY_BACKUP_OFFSITE_DIR/_EVERY_SEC/_KEEP`.
> Riserve R26-1 (exit-code best-effort off-site) e R26-2 (manca T33i kernel-aggancio), non bloccanti.
> TASK B: doctor sez.8 fallimento memoria RUMOROSO: collisione chiave_norm -> FAIL esplicito coi
> gruppi; corruzione generica -> FAIL esplicito (invece del vecchio silenzio). Vector store
> visibility senza download modello (VectorStore.__init__ lazy). Chiude **R-crm-norm-2**.
> Riserva R27-1 (alias _dvp) corretta prima del commit. Test: T33a-h + T34a-e, tutti PASS.
> **2026-06-19 (Comando CLI `gas reindex` — review #25 APPROVATO CON RISERVE, fix R-reidx-2
> incluso, commit motore vedi `reports/ultimo_report.md`):** aggiunto il comando di
> MANUTENZIONE UMANA `gas reindex` (gas.py: funzione `reindex()` + dispatch in `main()`)
> che RICOSTRUISCE da zero l'indice vettoriale `.gas_vectors.db` dal diario. È l'operazione
> umana dietro al catch-up automatico: serve dopo un cambio di modello di embedding (vettori
> vecchi incompatibili per modello/dim), per indicizzare in un colpo un diario già grosso, o
> se si sospetta un indice incoerente. SICURO: tocca SOLO la cache derivata, MAI il
> diario/`.gas_memory.db`; `ricostruisci_da_diario` calcola tutti gli embedding PRIMA di
> svuotare → un fallimento NON distrugge l'indice buono. ESPLICITO/on-demand: costruisce il
> vector store a prescindere da `GAS_VECTORS`. Exit code 0 OK / 1 in degrado; ZERO token LLM
> (solo embedding locali). **CONFERMATO solo-CLI:** `reindex` NON è in `tools_schema`
> (gas.py:337-344) né nel dispatcher `execute_tool_call` (gas.py:1079-1180, ogni nome ignoto
> → "Tool non trovato.") → fuori dalla mano del modello, stessa classe di `unisci_contatti`/
> restore/`git gc` (operazione irreversibile = manutenzione umana). Test T32a-c (ricostruzione
> dal diario, idempotenza svuota+ripopola, fail-safe vector store degradato → rc=1 senza crash).
> **R-reidx-2 CHIUSA in sessione:** corretto il commento di T32c (parte da sidecar GIÀ
> corrotto → si ferma al check `vs.available`, NON esercita "calcola gli embedding prima di
> svuotare"; quella barriera è coperta da T30c). **VERIFICA DAL VIVO con dipendenze reali:**
> numpy 2.4.6 + fastembed 0.8.0 installati nel venv (onnxruntime 1.27.0 wheel OK su x86_64),
> suite COMPLETA **152→155, 0 FAIL** coi blocchi T30/T31/T32 girati DAVVERO (prima saltati per
> `ModuleNotFoundError: numpy`). Modello del progetto: `paraphrase-multilingual-MiniLM-L12-v2`
> (qdrant onnx-Q), cache ~241MB su disco; cold embed reale ~1.83s (primo embed, include load
> lazy). NB fastembed avvisa che il modello ora usa **mean pooling invece di CLS** → cambio di
> comportamento dell'embedding tra versioni: caso d'uso tipico di `gas reindex`.
> **2026-06-18 (Vector store WIRING — retrieval semantico AGGANCIATO al kernel, review
> #24 APPROVATO CON RISERVE, commit motore vedi `reports/ultimo_report.md`).**
> **2026-06-18 (Vector store FETTA 1 — storage + embedding STANDALONE, review #23
> APPROVATO CON RISERVE, commit motore vedi `reports/ultimo_report.md`).**
> **2026-06-18 (R-crm-1 RIFATTO — identità su `chiave_norm` separata + NFKC, review
> #22 APPROVATO CON RISERVE, commit `ca08df7`).**
> **2026-06-17 (CHIUSURA FASE 2 memoria — declassamento `unisci_contatti`, review #21
> APPROVATO, commit `0240161`).**
> **2026-06-17 (doctor 402 onesto — review #20 APPROVATO, commit `7220c28`).**
> **2026-06-17 (Backup automatico del DB — review #19 APPROVATO, commit `cb99d1c`).**
> **2026-06-17 (fusione lead R-crm-1b CHIUSA + Vector DB Strato A — review #17/#18).**
> **2026-06-17 (normalizzazione chiavi lead — R-crm-1 CHIUSA, review #16 APPROVATO).**
> **2026-06-15 (diagnosi snapshot — CHIUSA, non-bug).**
> **2026-06-15 (task minimo: prefix `chore(scrivi-rep):` per feature scrivi rep).**
> Storico: TASK 1 hook SessionEnd additivo/condizionale + commit esplicito dei report
> (chiude bug sovrascrittura — revisore APPROVATO); TASK 2 sfoltimento finding chiusi
> → `finding_archiviati.md`; TASK 3 note VPS.

---

## Stato del motore — dettaglio storico (FASE 1 + FASE 2)

### VEC_MIN_SIM env-configurabile (review #28, 2026-06-21)
Nuovo helper PURO `_env_float(name, default, min_val=0.0, max_val=1.0)` fail-safe.
`__init__` risolve `self.VEC_MIN_SIM = _env_float("GAS_VECTORS_MIN_SIM", GasKernel.VEC_MIN_SIM)`.
Default 0.30 INVARIATO. Override via `GAS_VECTORS_MIN_SIM` senza redeploy.
Test T22f2. Suite Windows 158/9 (9 FAIL pre-esistenti ambientali).

### Backup OFF-MACHINE + doctor rumoroso (review #26/#27, 2026-06-20)
TASK A: `backup_offsite_auto()` in `store.py` (throttle SEPARATO, cintura integrità, fail-safe).
`backup_cmd()` SOLO-CLI in `gas.py` (`gas backup`). Env: `GAS_MEMORY_BACKUP_OFFSITE_DIR/_EVERY_SEC/_KEEP`.
TASK B: doctor sez.8 distingue collisione chiave_norm (FAIL esplicito) da corruzione generica.
VectorStore init lazy (nessun download al doctor). Test T33a-h + T34a-e.

### Vector store WIRING (review #24, 2026-06-18)
`self.vectors` gated da `GAS_VECTORS` (default OFF), doppia cintura fail-safe.
`_vettori_catchup()` indicizza righe nuove del diario, bounded a `VEC_CATCHUP_MAX`, UNA volta per turno.
`_ricorda(query)` cascata NON regressiva: FTS5 base → semantico riempie posti liberi (dedup) → substring.
Snippet via `_fmt_evento_datato` (ts + stato corrente lead). DEVIAZIONE dal design: FTS autorità, semantico supplemento. Test T31a-g.

### Vector store FETTA 1 storage+embedding (review #23, 2026-06-18)
NUOVO modulo `modules/memory/vectors.py` (VectorStore). Sidecar `.gas_vectors.db` SEPARATO dal sacro `.gas_memory.db` (cache derivata/ricostruibile, NON nel backup, gitignorata). Schema `(id, source, source_ref, testo, ts, vettore BLOB, dim, model)` UNIQUE(source,source_ref,model). Embedding locale fastembed `paraphrase-multilingual-MiniLM-L12-v2` (384-dim, ~504MB). Brute-force cosine numpy (float32 normalizzati). NIENTE sqlite-vec/ANN. Test T30a-f.

### R-crm-1 refactor chiave_norm (review #22, 2026-06-18)
`chiave` conserva l'as-entered, identità su colonna derivata `chiave_norm` UNIQUE + NFKC.
`normalizza_chiave` guadagna NFKC prima di collapse-whitespace/lower. `upsert_contatto` usa `ON CONFLICT(chiave_norm)`. Migrazione ADDITIVA: ALTER ADD + backfill + rilevamento collisioni → `ChiaveNormCollisione` se due righe storiche collassano → available=False. Test T29a-d.

### Fusione lead declassata a manutenzione umana (review #21, 2026-06-17)
Rimossi `unisci_contatti` da `tools_schema` e dispatcher. Handler e meccanismo nello store intatti (solo umani). Test T28a-c.

### Doctor 402 onesto (review #20, 2026-06-17)
Helper `_classify_provider_error` (429→QUOTA; 402 opzionale→WARN; 402 obbligatorio→KO; resto→KO). Test T27a-d.

### Backup automatico del DB (review #19, 2026-06-17)
`backup_auto(min_interval_sec)` THROTTLED in `store.py` (copia solo se integrità OK). `_memoria_backup_auto()` fail-safe in `run_turn`. Doctor sez.8. Test T26a-e.

### Vector DB Strato A FTS5 (review #18, 2026-06-17)
Tabella virtuale FTS5 external-content `diario_fts` + trigger AFTER INSERT + backfill idempotente. `cerca_diario` con `_fts_match` (sanifica input). Opzionale/fail-safe, cascata FTS→substring. Test T25a-e.

### Fusione lead cross-formato (review #17, 2026-06-17) — poi declassata (#21)
`merged_into` (NULL=vivo, valorizzato=lapide), `MemoryStore.unisci_contatti` completa anagrafica canonico (COALESCE). Diario IMMUTABILE preservato. Test T24a-f.

### Normalizzazione chiavi lead R-crm-1 (review #16, 2026-06-17)
`normalizza_chiave` (trim/collasso-whitespace/lower, pura+idempotente) in `store.py`. Applicata in `upsert_contatto` e `get_contatto_per_chiave`. Test T23a-d.

### CRM dal loop (review #15, 2026-06-16)
`salva_contatto` e `imposta_stato_contatto` in `tools_schema` + `execute_tool_call`. Scrittura IN-PROCESS (codice fidato, bypassa sandbox). Test T22a-h (round-trip CRM completo T22h).

### Memoria FASE 2 fetta 2b lettura/iniezione (review #14, 2026-06-16)
`_memoria_pin()` always-on (lead ATTIVI + poche azioni significative) nel system message. `MEMORY_PIN_CHAR_CAP=3000`. Tool `ricorda()` SOLA LETTURA. Test T21a-h.

### Memoria FASE 2 fetta 2a aggancio scrittura (review #13, 2026-06-16)
`self.memory = MemoryStore(...)` con doppia cintura fail-safe. Per ogni tool call nel loop: riga diario in-process. Helper `_riassumi_args`, `_esito_sintetico`, `_diario_log`. Test T20a-e.

### Memoria FASE 2 fetta 1 fondamenta (review #12, 2026-06-15)
Modulo `modules/memory/` (`store.py`). DB SQLite `.gas_memory.db` file singolo. `diario` IMMUTABILE (trigger BEFORE UPDATE/DELETE → ABORT). `contatti` upsert-abile. Test T19a-j.

### Manutenzione snapshot (review #10, 2026-06-14)
Retention ibrida (ultimi `SNAPSHOT_KEEP=100` ∪ più giovani di `SNAPSHOT_KEEP_DAYS=7`). Helper `_ref_age_epoch`, `_snapshot_retention`. `reports/snapshots.log` con rotazione. Doctor sez.7 SOLO report. Test T18a-f.

### Integrità paracadute free (review #9, 2026-06-14)
Doctor verifica esistenza e tool-capability del modello free OpenRouter. GET metadati, zero generazione. Test T17a-e.

### WINDOW_CHAR_CAP (review #7/#8, 2026-06-14)
`WINDOW_CHAR_CAP=24000`. `_cap_window_chars` + `_msg_chars`. Scarto messaggi INTERI (MAI slicing). Riallineamento a role:user. Test T14 (9 check).

### Sandbox OS bwrap (review #6, 2026-06-14)
`--unshare-net --unshare-pid --ro-bind / / --tmpfs /home --tmpfs /root --tmpfs /run + --clearenv`. `GAS_SANDBOX_MODE`: os_strict (fail-closed) / os_with_fallback. Doctor sez. "Sandbox OS". Test T13a-e.

### Scudo gratuito paracadute (review #5, 2026-06-13)
Rung 4 openrouter free + rung 5 ollama (gated su GAS_OLLAMA_URL) in cascata.

### Sicurezza commit (2026-06-13)
Hook SessionEnd additivo/condizionale. Gate PreToolUse deterministico (review_gate.sh, marcatore .review_ok).

### Sandbox applicativo run_command (review #4, 2026-06-12)
No shell=True. Vetting fail-closed: shlex.split + allowlist + _safe_path. Env sanificata. GAS_SHELL_MODE: guarded/dry_run. Test T11-T12.

### Snapshot preventivo (review #3, 2026-06-11)
`_snapshot(trigger, target)` prima di ogni write_file/run_command. commit-tree + ref refs/gas/snapshots/. Fail-closed. Retention ultimi 100.

### Fix T10 path traversal (review #2, 2026-06-11)
`_safe_path` (resolve + is_relative_to) su write_file e read_file.

### Fix _get_window (review #1, 2026-06-11)
Ricerca all'indietro senza cap.

---

## Suite test — storico conteggi

| Data | PASS | FAIL | Note |
|------|------|------|------|
| 2026-06-11 | 61 | 0 | base |
| 2026-06-13 | 46 | 0 | +paracadute gratuito |
| 2026-06-14 | 75 | 0 | +T13/T14/T17/T18 |
| 2026-06-15 | 85 | 0 | +T19 memoria fetta 1 |
| 2026-06-16 | 106 | 0 | +T20/T21/T22 memoria loop/CRM |
| 2026-06-17 | 135 | 0 | +T23-T28 CRM/FTS5/backup |
| 2026-06-18 | 152 | 0 | +T29/T30/T31 vector store |
| 2026-06-19 | 155 | 0 | +T32 gas reindex (con numpy/fastembed reali) |
| 2026-06-20 | 158 | 8* | +T33/T34; *FAIL ambientali Windows pre-esistenti |
| 2026-06-21 | 158 | 9* | +T22f2 VEC_MIN_SIM; *9 FAIL ambientali |
| 2026-06-23 CI Linux | 160 | 7→2* | bwrap installato; *T9a/T9c env attesi |

---

## Finding chiusi (archiviati)

- ✅ **R-vec-1** (review #23, 2026-06-18): `_search_vec` ora avvolge vstack/from_blob/matmul e cattura ValueError. T30f morde.
- ✅ **R-reidx-1** (review #25, 2026-06-19): numpy/fastembed installati nel venv, suite 155/0.
- ✅ **R-reidx-2** (review #25, 2026-06-19): commento T32c corretto.
- ✅ **Riserve 2b R1/R2/R3** (review #15, 2026-06-16): match contatto, override env pin, scan bounded.
- ✅ **R-crm-1 parte case/whitespace** (review #16, poi rifatta come chiave_norm review #22).
- ✅ **R-crm-norm-2** (review #27, 2026-06-20): doctor sez.8 distingue collisione/corruzione con FAIL esplicito.
- ✅ **R-crm-norm-1** (review #21, 2026-06-17): messaggi di successo con chiave canonica.

---

## Istituzioni di processo — dettaglio review

**Subagent revisore** (#28 review completate, ultima #28 VEC_MIN_SIM 2026-06-21):
#1 fix _get_window, #2 fix T10, #3 snapshot, #3-bis fix R1, #4 sandbox applicativo,
#5 paracadute gratuito, #6 sandbox OS bwrap, #7 WINDOW_CHAR_CAP, #8 copertura T14,
#9 integrità paracadute free, #10 manutenzione snapshot, review hook SessionEnd 2026-06-15,
#12 memoria fetta 1, #13 fetta 2a, #14 fetta 2b, #15 CRM contatti dal loop,
#16 normalizzazione chiavi, #17 fusione lead (RESPINTO poi APPROVATO), #18 FTS5,
#19 backup DB, #20 doctor 402, #21 declassamento unisci_contatti, #22 chiave_norm+NFKC,
#23 vector store fetta 1, #24 wiring kernel, #25 gas reindex, #26 backup off-machine,
#27 doctor rumoroso + vector visibility, #28 VEC_MIN_SIM env-config.
Lezioni in `.claude/agents/memoria_revisore.md`.

---

## Prossimi passi obsoleti (già fatti o sostituiti)

- ~~Vector store Strato B: fatte fetta 1 (#23) + wiring (#24) + reindex (#25)~~
- ~~VEC_MIN_SIM configurabile via env: fatto review #28~~
- ~~Rilevamento provider free: fatto review #9~~
- ~~Backup auto del DB: fatto review #19~~
- ~~FTS5 sul diario: fatto review #18~~
