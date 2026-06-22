# STATO PROGETTO GAS

> Fotografia viva dello stato del progetto. Aggiornata a fine di ogni task.
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
> #24 APPROVATO CON RISERVE, commit motore vedi `reports/ultimo_report.md`):** la fetta 1
> (storage+embedding) ora è CABLATA a `run_turn`/`ricorda`. `gas.py`: `self.vectors`
> costruito SOLO se env `GAS_VECTORS` truthy (helper `_env_flag`), doppia cintura fail-safe
> come `self.memory`; **default OFF** di proposito (il modello pesa ~500MB+RAM, R-vec-3 VPS
> 1GB irrisolta; tiene la suite veloce e non impone il layer al deploy base). `_vettori_catchup()`
> indicizza una volta per turno (DOPO `_memoria_backup_auto`, FUORI dal `for _ in range(10)`)
> le righe di diario NUOVE oltre un watermark, BOUNDED a `VEC_CATCHUP_MAX` (env override),
> avanzando il watermark solo se l'index riesce. `_ricorda(query)` diventa una cascata
> **NON regressiva**: FTS5 BASE (precisione lessicale, comportamento odierno preservato) →
> il semantico RIEMPIE i posti liberi fino a n (recall per significato, dedup su id) →
> substring ultimo pavimento. Snippet via `_fmt_evento_datato`: `ts` dell'evento + stato
> CORRENTE del lead (letto live, non denormalizzato). store.py: `diario_dopo`/`get_diario`
> SOLA LETTURA. vectors.py: `index_batch` + `max_source_ref`. **DEVIAZIONE ONESTA dal
> §FINALE** (che diceva "semantico PRIMA"): MISURATO dal vivo che il MiniLM separa
> DEBOLMENTE le query corte italiane (distrattore 'caffè' cos 0.288 batte il pertinente
> 'offerta' 0.237; 'animale domestico'↔'gatto' 0.148) → semantico-prima REGREDIREBBE la
> precisione, quindi invertito a "FTS autorità + semantico riempie", soglia `VEC_MIN_SIM=0.30`.
> Invarianti motore (`_get_window`/`_cap_window_chars`/`for _ in range(10)`/sandbox/snapshot/
> pin) INTATTE; con GAS_VECTORS spento il comportamento è bit-identico a ieri. E2E REALE
> (GAS_VECTORS=1): query 'vendita' (non lessicale) recupera "offerta commerciale ad Anna —
> lead Anna: oggi 'interessato'". Suite **145→152** (T31a-g). Riserve R-wire-1..4 (sotto,
> minori): la principale è la soglia da rendere env-config e ri-tarare sul diario reale.
> **2026-06-18 (Vector store FETTA 1 — storage + embedding STANDALONE, review #23
> APPROVATO CON RISERVE, commit motore vedi `reports/ultimo_report.md`):** primo
> tassello del retrieval semantico (Strato B, prima CONGELATO). NUOVO modulo
> `modules/memory/vectors.py` (`VectorStore`) SOLO storage+embedding, **NON agganciato**
> a `ricorda`/`run_turn`/loop (il wiring è una fetta successiva, solo PROPOSTA nel
> report §FINALE). Sidecar `.gas_vectors.db` **SEPARATO** dal `.gas_memory.db` sacro:
> CACHE DERIVATA e RICOSTRUIBILE dal diario (NON fonte di verità, NON nel backup,
> gitignorata). Schema multi-source `(id, source, source_ref, testo, ts, vettore BLOB,
> dim, model)`; v1 popola solo `source='diario'`. Embedding LOCALE via **fastembed**
> (nuova dipendenza), brute-force COSINE in numpy (vettori float32 normalizzati a norma 1
> in scrittura → dot product); **NIENTE sqlite-vec** (alpha pre-v1, formato instabile,
> fuori dal percorso critico h24) e **NIENTE ANN** (a questi numeri il brute-force è <10ms).
> `ricostruisci_da_diario(memory_store)` = motore del futuro `gas reindex` (qui NON
> cablato a CLI); usa il nuovo lettore SOLA-LETTURA `MemoryStore.diario_tutto()`
> (immutabilità del diario intatta). **DECISIONE UMANA ESPLICITA:** il modello della
> spec `intfloat/multilingual-e5-small` NON è nel catalogo fastembed 0.8.0; l'utente ha
> scelto `paraphrase-multilingual-MiniLM-L12-v2` (384-dim, 0.22GB nominali / ~504MB su
> disco reali, regge l'italiano, entra nei vincoli RAM del VPS). I prefissi e5
> `query:`/`passage:` NON si applicano (mappa per-modello: MiniLM → `("","")`), ma il
> meccanismo resta nel codice pronto per un modello e5. **FAIL-SAFE §9 esteso:** importare
> `modules.memory` NON fallisce se numpy/fastembed mancano (import protetti, GAS gira
> identico); `available=False` → `index`/`ricostruisci`=None, `search`=[]; sidecar
> mancante→creato, corrotto→degrado. **R-vec-1 CHIUSA in sessione** (su prescrizione del
> revisore): il `try/except` di `_search_vec` ora avvolge anche `vstack`/`from_blob`/matmul
> e cattura `ValueError` → una cella BLOB fisicamente corrotta degrada a [] invece di
> crashare (precondizione di sicurezza per il wiring; T30f morde). Suite **139→145**
> (T30a-f). `gas.py` INVARIATO. Riserve nuove **R-vec-2** (env-config) e **R-vec-3**
> (ARM/RAM VPS) sotto. Verifiche dal vivo: embed reale 384-dim norma 1, frasi italiane
> simili cos 0.876 vs diverse 0.113; cold embed ~0.11s dopo init ~7s.
> **2026-06-18 (R-crm-1 RIFATTO — identità su `chiave_norm` separata + NFKC, review
> #22 APPROVATO CON RISERVE, commit `ca08df7`):** su scelta ESPLICITA dell'utente (dopo
> avergli fatto presente che R-crm-1 era GIÀ chiuso in forma "normalizza-in-place" da
> review #16) la normalizzazione chiavi è stata RIFATTA secondo il design originale della
> task: `chiave` ora conserva il valore **AS-ENTERED** (grafia digitata, leggibile) e
> l'IDENTITÀ passa su una colonna derivata **`chiave_norm` UNIQUE**. `normalizza_chiave`
> guadagna **NFKC** (forme di compatibilità Unicode: 'Ａ'→'a', 'ﬁ'→'fi') prima di
> collapse-whitespace/lower; idempotenza preservata. `upsert_contatto` usa
> `ON CONFLICT(chiave_norm)` e in update NON tocca `chiave` (prima grafia stabile); i
> lookup risolvono su `chiave_norm`. **Migrazione ADDITIVA e SICURA** in `_ensure_columns`:
> ALTER ADD `chiave_norm` (nullable) + backfill (scrive SOLO la nuova colonna, anagrafica
> intatta) + **rilevamento collisioni** (`GROUP BY chiave_norm HAVING COUNT>1`): se due
> righe storiche collassano sulla stessa forma canonica → `ChiaveNormCollisione`, **NIENTE
> fusione**, indice UNIQUE NON creato, `available=False` + `collisione_chiave_norm` (il
> merge dei duplicati ESISTENTI è MANUTENZIONE UMANA — STOP GATE rispettato). Il dato
> storico resta INTATTO anche ad abort (verificato dal revisore riaprendo il file). **gas.py
> INVARIATO** (`_trova_contatto` già normalizzava l'haystack al volo). Suite **135→139**
> (T23a/T23f/T28b → `chiave_norm`; +T29a-d NFKC/as-entered/migrazione pulita+collisione).
> NB: la prevenzione dei duplicati FUTURI è fatta; il merge dei duplicati ESISTENTI resta
> migrazione umana (parcheggiato). Riserva nuova **R-crm-norm-2** (sotto). Vector DB Strato
> B resta ❄️ CONGELATO (design in discussione nella chat di strategia, NON in coda).
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

- **Soglia semantica `VEC_MIN_SIM` ENV-CONFIGURABILE** (2026-06-21, review #28 APPROVATO):
  nuovo helper PURO `_env_float(name, default, min_val=0.0, max_val=1.0)` (fail-safe come
  `_env_int`: assente→default, non parsabile→default+`logging.warning`, fuori range→clamp a
  [min_val,max_val]; `max_val=1.0` perché il coseno di vettori normalizzati è ≤1). `__init__`
  risolve `self.VEC_MIN_SIM = _env_float("GAS_VECTORS_MIN_SIM", GasKernel.VEC_MIN_SIM)`, stesso
  pattern di `VEC_CATCHUP_MAX`; usato dal call-site del retrieval semantico (`min_sim=self.VEC_MIN_SIM`).
  Default di classe `0.30` INVARIATO → env assente = comportamento bit-identico. La soglia ora si
  ri-tara al deploy SENZA redeploy. Chiude la parte azionabile di R-wire-1; la ri-taratura del
  valore sul diario reale resta voce CHECKLIST pre-deploy VPS. Test T22f2. Suite Windows 158/9
  (9 FAIL pre-esistenti ambientali, verificati identici su HEAD pulito).
- **Memoria FASE 2 — Backup OFF-MACHINE + doctor rumoroso ATTIVI** (2026-06-20, review #26/#27
  APPROVATI CON RISERVE, commit `56a6dc3`): TASK A: `store.py` aggiunge `backup_offsite_auto()`
  — copia THROTTLED su dir esterna (throttle SEPARATO da backup locale, cintura integrita', fail-safe
  sec.9, riusa `backup()`/`integrity_check()`). `gas.py`: costanti `MEMORY_BACKUP_OFFSITE_EVERY_SEC`
  (86400s) / `_KEEP` (10), override env `GAS_MEMORY_BACKUP_OFFSITE_DIR/_EVERY_SEC/_KEEP`;
  `_memoria_backup_auto()` esteso col blocco off-site condizionale; `backup_cmd()` SOLO-CLI (exit 0/1,
  NON in tools_schema/dispatcher); dispatch `gas backup` in `main()`; doctor sez.8 check off-site
  dir+eta' INDIPENDENTE da `mem.available` (`mem` dichiarata `None` prima del blocco). TASK B:
  doctor sez.8 distingue collisione chiave_norm (FAIL esplicito coi gruppi) da corruzione generica
  (FAIL esplicito "DB non apribile/schema/corruzione") — chiude R-crm-norm-2. Vector store visibility
  senza download: `VectorStore.__init__` e' lazy (modello = solo al primo index/search), fail-safe nel
  try/except del doctor. Riserve aperte: R26-1 (exit-code backup_cmd best-effort off-site, da
  documentare sul VPS); R26-2 (manca T33i aggancio kernel — candidato futuro); R27-1 corretta prima
  del commit. Invarianti motore intatte. Test T33a-h + T34a-e tutti PASS. Suite 158/8.
- **Memoria FASE 2 — Vector store WIRING (retrieval semantico AGGANCIATO) ATTIVO,
  OPT-IN via `GAS_VECTORS`** (2026-06-18, review #24 APPROVATO CON RISERVE): la fetta 1 è
  ora cablata al motore. `gas.py`: `self.vectors` (gated da env `GAS_VECTORS` via `_env_flag`,
  default OFF — il modello pesa ~500MB+RAM, R-vec-3) con doppia cintura fail-safe come
  `self.memory`; `_vettori_catchup()` indicizza nel sidecar le righe di diario NUOVE oltre
  un watermark, UNA volta per turno e BOUNDED a `VEC_CATCHUP_MAX` (env `GAS_VECTORS_CATCHUP_MAX`),
  chiamato in `run_turn` dopo `_memoria_backup_auto` e FUORI dal `for _ in range(10)`,
  avanzando il watermark solo su index riuscito; `_ricorda(query)` cascata NON regressiva
  FTS5(base)→semantico(riempie fino a n, dedup)→substring; snippet `_fmt_evento_datato`
  con `ts` + stato CORRENTE del lead (live). store.py: `diario_dopo`/`get_diario` SOLA
  LETTURA (immutabilità intatta). vectors.py: `index_batch` (embedding in blocco) +
  `max_source_ref` (watermark). DEVIAZIONE ONESTA dal §FINALE motivata da misura reale
  (MiniLM separa debolmente le query corte IT → FTS resta l'autorità, semantico = recall
  additivo, `VEC_MIN_SIM=0.30`). Invarianti motore INTATTE; GAS_VECTORS OFF → comportamento
  bit-identico a ieri. Test T31a-g + E2E reale. Suite **145→152**.
- **Memoria FASE 2 — Vector store FETTA 1 (storage + embedding semantico) ATTIVA,
  ma STANDALONE (NON agganciata)** (2026-06-18, review #23 APPROVATO CON RISERVE):
  primo strato del retrieval semantico, prima congelato. NUOVO modulo
  `modules/memory/vectors.py` (`VectorStore`): SOLO livello di persistenza+embedding,
  NESSUN aggancio a `ricorda`/`run_turn`/loop (wiring = fetta successiva, solo PROPOSTA
  nel report §FINALE). `gas.py` INVARIATO. Sidecar `.gas_vectors.db` SEPARATO dal
  `.gas_memory.db` sacro (CACHE derivata/ricostruibile dal diario, NON fonte di verità,
  NON nel backup, gitignorata con `-wal`/`-shm`). Schema multi-source
  `(id, source, source_ref, testo, ts, vettore BLOB, dim, model)` con
  `UNIQUE(source, source_ref, model)` → `index` idempotente; v1 solo `source='diario'`,
  campi pronti per source futuri (trascritti vocali/RAG) senza migrazione. Embedding
  LOCALE via **fastembed** (`paraphrase-multilingual-MiniLM-L12-v2`, 384-dim — scelta
  umana esplicita perché `multilingual-e5-small` assente dal catalogo 0.8.0); prefissi e5
  gestiti per-modello nel codice (MiniLM → `("","")`). Ricerca brute-force COSINE in numpy
  (vettori float32 NORMALIZZATI a norma 1 in scrittura → dot product), top-k + soglia
  minima; **NIENTE sqlite-vec / NIENTE ANN** (deciso: alpha instabile / non serve a questi
  numeri). `ricostruisci_da_diario` calcola TUTTI gli embedding PRIMA di svuotare l'indice
  (embedding fallito → None, indice buono NON distrutto), poi DELETE+INSERT in una
  transazione; legge via il nuovo `MemoryStore.diario_tutto()` (SOLA LETTURA, immutabilità
  diario intatta). FAIL-SAFE §9: import protetti (numpy/fastembed assenti → `modules.memory`
  importa lo stesso, GAS identico), `available=False`→degrado, sidecar corrotto→degrado,
  cella BLOB corrotta→`search` [] (R-vec-1, T30f). "La memoria non mente": il `ts`
  dell'evento sorgente viaggia col record. Test T30a-f (ranking con vettori finti, soglia,
  ricostruzione+idempotenza, fail-safe fastembed-assente/DB-corrotto, embed reale 384-dim
  SKIPPABILE, cella BLOB corrotta). Suite **139→145**.
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
  **155 PASS, 0 FAIL** (2026-06-19, eseguita DAVVERO con numpy/fastembed installati nel venv —
  i blocchi vettoriali T30/T31/T32 prima si SALTAVANO per `ModuleNotFoundError: numpy`). Dai 152
  si aggiungono i 3 T32 (comando CLI `gas reindex`: T32a ricostruzione dal diario rc=0+vettori,
  T32b idempotenza svuota+ripopola, T32c fail-safe vector store degradato → rc=1 senza crash).
  Storico: dai 145 si aggiungono i 7 T31 (wiring vector store:
  T31a catch-up indicizza il diario nuovo + watermark + idempotente, T31b catch-up bounded
  a scaglioni di VEC_CATCHUP_MAX, T31c snippet datato (ts) + stato corrente del lead, T31d
  semantico RIEMPIE quando FTS è assente (recall/nessun buco), T31e vector store degradato
  → catch-up no-op + ricorda non crasha, T31f GAS_VECTORS spento di default → vectors None,
  T31g gate env GAS_VECTORS=1 costruisce il layer lazy senza download). Storico: dai 139 i 6 T30 (vector store fetta 1:
  T30a index+search ranking con vettori finti deterministici, T30b soglia minima → nessun
  risultato, T30c `ricostruisci_da_diario` coerente + ts sorgente + idempotenza, T30d
  fail-safe fastembed-assente + DB-sidecar-corrotto, T30e embedding REALE 384-dim
  normalizzato + similarità italiana — NON skippato in Codespace, SKIPPABILE in CI senza
  rete, T30f R-vec-1 cella BLOB corrotta → `search` []). Storico: dai 135 i 4 T29 (R-crm-1 refactor
  chiave_norm: T29a NFKC, T29b chiave as-entered conservata + identità su chiave_norm,
  T29c migrazione legacy pulita → backfill + indice UNIQUE, T29d migrazione con collisione
  → rilevata/ABORT/niente fusione/indice non creato); T23a/T23f/T28b aggiornati al nuovo
  contratto (asserivano `chiave`==normalizzata → ora `chiave_norm`). Storico: dai 132 i 3 T28 (declassamento
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

- ✅ **R-vec-1 (fail-safe di `_search_vec` su cella BLOB corrotta) — CHIUSA in sessione**
  (review #23, 2026-06-18): il `try/except` di `_search_vec` ora avvolge anche
  `vstack`/`_from_blob`/matmul e cattura `ValueError` oltre a `(sqlite3.Error, OSError)`.
  Una cella `vettore` fisicamente troncata (header SQLite intatto, BLOB non multiplo di 4)
  faceva propagare `ValueError` FUORI da `search`, contro la promessa "degrado, zero crash"
  del modulo. Era latente (modulo non cablato) ma è precondizione di sicurezza per esporre
  `search` al loop. Chiusa su prescrizione del revisore; T30f morde (riga corrotta dello
  stesso model+dim della query → `search` degrada a []).
- ✅ **R-reidx-1 (verifica dal vivo della suite vettoriale) — CHIUSA** (review #25,
  2026-06-19): la riserva nasceva perché numpy/fastembed non erano installati nel Codespace,
  quindi la suite si fermava a riga ~1612 (`ModuleNotFoundError: numpy`) PRIMA dei blocchi
  T30/T31/T32. Installate le dipendenze nel venv (`venv/bin/pip install numpy fastembed`:
  numpy 2.4.6, fastembed 0.8.0, onnxruntime 1.27.0 — wheel OK su x86_64), la suite COMPLETA
  gira **155 PASS, 0 FAIL** con T30/T31/T32 esercitati DAVVERO (embedding reale 384-dim incluso).
  Conteggio reale verificato, non a memoria.
- 🟡 **R-reidx-deps (la suite vettoriale non girava nel Codespace) — NUOVO** (review #25,
  2026-06-19, da presidiare al deploy): numpy/fastembed NON erano installati nell'ambiente di
  sviluppo → i blocchi T30/T31/T32 venivano saltati silenziosamente prima di questa sessione.
  Ora installati nel venv. **AZIONE:** verificare che numpy + fastembed (+ onnxruntime) restino
  dichiarati in `requirements.txt` e nell'ambiente del deploy VPS, altrimenti il layer vettoriale
  e `gas reindex` degradano a no-op (fail-safe, ma muto) e la CI salterebbe di nuovo i test.
- 🟡 **R-reidx-3 (picco RAM di `reindex` su diario grande) — voce CHECKLIST pre-deploy VPS**
  (review #25, eredita R-vec-3, informativa): `reindex`/`ricostruisci_da_diario` materializza
  TUTTI gli embedding in RAM prima del DELETE+INSERT (necessario per non distruggere l'indice
  buono su errore). Su un diario molto grande e **VPS a 1GB** il picco di memoria va validato;
  mitigazione candidata se stretto: re-index a scaglioni o swap. Non difetto del codice, da
  verificare al deploy.
- 🟡 **R-vec-2 (costanti/path del vector store non configurabili via env)** (review #23,
  minore): `DEFAULT_VECTORS_FILENAME`, `EMBED_MODEL_NAME`, `EMBED_DIM`, `timeout=10`
  hardcoded — stessa classe di `GAS_MEMORY_DB`/`WINDOW_CHAR_CAP`/`SNAPSHOT_KEEP`. Per il
  deploy VPS (sidecar su volume persistente, eventuale modello e5 alternativo) valutare
  `GAS_VECTORS_DB`/`GAS_EMBED_MODEL`. Non urgente, coerente con lo scope storage-only.
- 🟡 **R-vec-3 (portabilità ARM + RAM del VPS non verificabile da qui)** (review #23,
  informativa): la wheel `onnxruntime` per ARM (Oracle Ampere) e il footprint RAM
  (~504MB modello su disco, init ~7s, **VPS a 1GB RAM** da `deploy_vps_bozza.txt`) restano
  un'incognita da validare al deploy. L'arch di sviluppo è x86_64 → NON dato per scontato.
  Dichiarata in `requirements.txt` e nel docstring; voce di CHECKLIST pre-deploy, non
  difetto del codice. Mitigazione candidata se 1GB è stretto: swap, o modello ancora più
  piccolo, o embedding solo on-demand (non per ogni evento).
- 🟡 **R-wire-1 (soglia semantica `VEC_MIN_SIM` tarata su esempi sintetici)** (review #24,
  la principale): 0.30 scelta da misure su pochi esempi x86, NON sul corpus reale. Il MiniLM
  separa DEBOLMENTE le query corte italiane (coseni reali ~0.2-0.6 anche per coppie
  pertinenti, distrattori vicini ai pertinenti) → la soglia va RI-TARATA sul primo diario
  vero del VPS, e meglio se resa configurabile via env `GAS_VECTORS_MIN_SIM` (come
  `CATCHUP_MAX`) per non richiedere redeploy. Mitigato dal design non-regressivo: anche se
  la soglia è imperfetta, il semantico solo RIEMPIE dopo FTS, non sopprime nulla.
- 🟡 **R-wire-2 (qualità semantica del MiniLM limitata sulle query corte IT)** (review #24):
  conseguenza diretta del modello scelto (forzato dall'assenza di e5-small + vincolo RAM
  VPS). Il retrieval per SIGNIFICATO funziona su query-frase ('vendita'→'offerta commerciale')
  ma è inaffidabile su singole parole astratte. È un limite di POTENZA, non di correttezza:
  il valore pieno arriverebbe con un modello e5 (legato alla rivalutazione R-vec-3/RAM VPS).
  Onesto: il semantico è un SUPPLEMENTO di recall opt-in, non una promessa di precisione.
- 🟡 **R-wire-3 (cold-start del primo catch-up)** (review #24, minore): col layer appena
  abilitato, il primo turno con diario arretrato carica il modello (~500MB download se i
  pesi non sono pre-provisionati) e indicizza fino a `VEC_CATCHUP_MAX` righe → picco di
  latenza una-tantum su quel turno. Bounded e fail-safe (non blocca il turno), ma da
  conoscere; mitigato dal pre-provisioning dei pesi (R-vec-3) e dal tetto per-turno.
- 🟡 **R-wire-4 (`_fmt_evento_datato` fa una query per hit)** (review #24, minore/perf):
  per arricchire lo snippet con lo stato corrente del lead, ogni evento con `contatto_id`
  fa un `get_contatto` separato (N piccole query a volumi di `n`≤50). Trascurabile su SQLite
  locale; se mai diventasse caldo, batch per id. Cosmetico.
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
- ✅ **R-crm-1 (parte case/whitespace) — CHIUSA, poi RIFATTA con `chiave_norm` separata**
  (chiusa il 2026-06-17 `cdf764a` review #16; RIDISEGNATA il 2026-06-18 `ca08df7` review
  #22 su scelta utente — vedi blocco datato in cima e voce motore). Forma attuale: `chiave`
  conserva l'as-entered, l'identità è la colonna derivata `chiave_norm` UNIQUE, con NFKC.
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
- ✅ **R-crm-norm-2 (osservabilita' collisione chiave_norm) — CHIUSA** (review #27, 2026-06-20,
  TASK B): il doctor sez.8 ora distingue collisione chiave_norm da corruzione generica con FAIL
  esplicito e messaggio specifico inclusi i gruppi duplicati. Sul VPS l'operatore vede
  immediatamente se deve fare un merge manuale o indagare una corruzione. Test T34a morde il caso.
  Chiude il follow-up aperto dalla review #22.
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
- **D — `reports/handoff.md`** (dal 2026-06-23): dossier autocontenuto di fine sessione
  (§DECISIONI UMANE in cima, esito sonda, `git diff --stat` reale, `git log` dei commit,
  delta test motore, verdetto integrale del revisore, stato ultima run CI). AGGREGA
  `ultimo_report.md` per la revisione e aggiunge lo stato CI; NON lo sostituisce. Affiancato
  dalla CI GitHub Actions (`.github/workflows/ci.yml`, FETTA 1).
- **C — Subagent revisore** (`.claude/agents/revisore.md`): **26 review completate**,
  ultima la **#27** (doctor memoria rumoroso + vector store visibility, 2026-06-20, APPROVATO
  CON RISERVE → R27-1 corretta prima del commit, R-crm-norm-2 CHIUSA). Prima la **#26**
  (backup off-machine, 2026-06-20, APPROVATO CON RISERVE → R26-1 exit-code best-effort,
  R26-2 manca T33i). Prima la **#25** (gas reindex, 2026-06-19, APPROVATO CON RISERVE).
  Elenco in ordine: #1, #2, #3, #3-bis, #4, #5, #6, #7, #8, #9 (TASK B),
  #10 (TASK C), review hook SessionEnd TASK 1 (2026-06-15, APPROVATO), #12 Memoria
  FASE 2 fetta 1 (APPROVATO CON RISERVE), #13 fetta 2a (APPROVATO CON RISERVE),
  #14 fetta 2b (APPROVATO CON RISERVE), #15 CRM contatti dal loop + chiusura R1/R2/R3
  (APPROVATO CON RISERVE), #16 normalizzazione chiavi lead / chiusura R-crm-1
  (APPROVATO), #17 fusione lead R-crm-1b (RESPINTO per bug d'ordine ALTER/CREATE INDEX
  su DB legacy → APPROVATO dopo fix + T24f), #18 Vector DB Strato A / FTS5 (APPROVATO),
  #19 backup automatico del DB (APPROVATO, 2 note cosmetiche), #20 doctor 402→WARN sui
  rung free (APPROVATO), #21 declassamento `unisci_contatti` (APPROVATO, 1 nota
  cosmetica), #22 R-crm-1 refactor a `chiave_norm` separata + NFKC (APPROVATO CON
  RISERVE → R-crm-norm-2 chiusa in #27), #23 vector store fetta 1 (APPROVATO CON
  RISERVE), #24 wiring kernel (APPROVATO CON RISERVE), #25 gas reindex (APPROVATO CON
  RISERVE), #26 backup off-machine (APPROVATO CON RISERVE), #27 doctor rumoroso +
  vector visibility (APPROVATO CON RISERVE). Lezioni datate in `.claude/agents/memoria_revisore.md`.

## Prossimi passi (in ordine di priorità)

0. **Vector store semantico (Strato B) — FETTA 1 + WIRING FATTI (opt-in, default OFF).**
   Aggiornato 2026-06-18: fatta la fetta 1 (`vectors.py`, review #23) E il WIRING al kernel
   (review #24) — `ricorda(query)` ora usa il vector store (cascata FTS→semantico-riempie→
   substring), con catch-up indexing pigro/bounded a inizio turno e snippet datato+stato
   lead. Acceso via env `GAS_VECTORS` (default OFF per R-vec-3: modello ~500MB/RAM). FTS5
   (Strato A) resta l'autorità lessicale. **Prossimi affinamenti (NON urgenti):** (a) R-wire-1
   — rendere `VEC_MIN_SIM` configurabile via env e RI-TARARLA sul diario reale del VPS;
   (b) R-wire-2/R-vec-3 — rivalutare un modello e5 (qualità semantica) quando si scioglie
   il nodo RAM del VPS; (c) un comando `gas reindex` umano che chiami
   `ricostruisci_da_diario` (oggi esposto ma non cablato a CLI). Scartati a monte: `sqlite-vec`
   (alpha instabile), ANN (non serve a questi numeri), embedding via API (contro
   zero-token/offline), store separati Chroma/FAISS (romperebbero il file singolo). NB: un
   **un-merge** dei lead resta **NON necessario** finché il merge è MANUALE (registrato).
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
