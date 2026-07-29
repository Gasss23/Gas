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

### Sessione 2026-07-21 — chiusura giro item fuori-roadmap

- ✅ **Scrub IP/SSH** (2026-07-20, PR #32 `f2679a4`): IP via da HEAD, verificato su albero mergiato via git grep (esatto+parziale = 0). Stato **MITIGATO** (resta in history pubblica → cura = privatizzazione, roadmap item 0).
- ✅ **Fork = 0** [output `gh repo view`, 2026-07-21]: nessun fork pubblico → l'IP non è uscito su terzi.
- ✅ **ssh-agent → HTTPS** [output WSL]: remote di `~/Gas` GIÀ HTTPS; hook git vivi senza passphrase. NB: riguarda il push GIT, NON la chiave SSH del VPS (che ha passphrase, vedi sotto).
- ✅ **ACCESSO SSH AL VPS RIPRISTINATO** (2026-07-21) [ex-🔴]: root pw resettata a caldo da Cloud Console (nessun reboot da lì). Metodo pubkey-via-gist FALLITO — la console noVNC Hetzner non incolla e mappa `/`→`&`/`?` (mangling sistematico); ripiegato su varco password temporaneo (`00-temp.conf` PasswordAuth yes → `ssh-copy-id` da WSL → varco RICHIUSO). Verifica: `ssh gas@<VPS_IP>` = OK/`gas`; `sshd -T` → `passwordauthentication no`; `passwd -l gas`. Chiave WSL `id_ed25519` ora in `authorized_keys` di `gas`. Fingerprint di riferimento della chiave WSL autorizzata sul VPS: `SHA256:/BJvnyxJIKj00Odj4onGIKszb2W3icqneeLhabKfnoE` (ED25519, `gqual@gas-dev-wsl`) — verificato live con `ssh-keygen -lf ~/.ssh/id_ed25519.pub`.
- ⚠️ **Reboot GAS in prod NON pianificato** (2026-07-21): Ctrl+Alt+Del involontario in console noVNC = reset macchina. GAS ripartito da solo (`Restart=always`), `systemctl is-active gas` = `active`. Downtime breve, nessun danno. Lezione: Ctrl+Alt+Del in console Hetzner riavvia il server.
- 🟡 **2FA Hetzner non attivo** [banner console 2026-07-21]: ancora da abilitare.
- ✅ **Sonda `.venv` VPS FATTA** (2026-07-21) [ex-⛔]: prod usa **`.venv`** (col punto); `ExecStart=…/.venv/bin/python … gas.py telegram`; `.gitignore` della copia VPS ignora solo `venv/`, NON `.venv/`.
- ℹ️ [SUPERATA dalla verifica 2026-07-22 — vedi F7 CHIUSO sotto] **F7 CONFERMATO APERTO SUL VPS** (2026-07-21): il fix `.gitignore` (`.venv/`) è in origin/main ma la copia VPS (`/home/<VPS_USER>/gas/`, fatta a S1 2026-07-04) è STANTIA e non lo ha → ogni snapshot preventivo su prod inghiotte il virtualenv. **Fix minimo (strada 1)**: aggiungere `.venv/` al `.gitignore` della copia VPS. **Fix pulito (strada 2)**: riallineare la copia VPS a origin/main — deploy vero (FASE 5 S2), non a caldo.
- ℹ️ [SUPERATA dalla verifica 2026-07-22 — vedi F7 CHIUSO sotto] **F7 — APERTA e FATTIBILE** (prerequisito SSH soddisfatto, fix non eseguito in sessione): la strada 1 (aggiungere `.venv/` al `.gitignore` della copia VPS via SSH) è ora percorribile, ma è un **tampone dichiarato**, non una chiusura pulita — la cura è la strada 2 (riallineamento copia VPS a origin/main, FASE 5 S2).
- 🟡 **Copia VPS stantia vs origin/main** (nuovo finding, 2026-07-21): la working copy di prod diverge dal repo (emerso da F7). Riallineamento = FASE 5 S2, con revisore + verifica, non a caldo.
- ℹ️ **Chiave SSH del VPS ha passphrase** (2026-07-21): `~/.ssh/id_ed25519` su WSL la richiede → per hook/comandi non-interattivi verso il VPS serve `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519` a inizio sessione. Distinto dal push git (HTTPS, no passphrase).

### Sessione 2026-07-22 — rientro accesso VPS + chiusura F7

- ✅ **F7 CHIUSO**: il VPS usa `/home/gas/gas/.venv` (CON il punto).
  Verificato via ssh, `test -d` diretto. Il `.gitignore` locale (righe 1-2)
  contiene sia `venv/` sia `.venv/` → copertura completa, non più tampone.
  ⚠️ RISERVA DI EVIDENZA: la verifica 2026-07-22 cita "il .gitignore locale (righe 1-2)". Agli atti NON risulta se sia il .gitignore della copia VPS (`/home/gas/gas/.gitignore`) o quello del repo. Se era quello del repo, F7 non è chiuso. Da verificare al prossimo accesso SSH al VPS con: `cat /home/gas/gas/.gitignore | head -5`.

- ✅ **Rilievo FETTA B CHIUSO**: fingerprint
  `SHA256:/BJvnyxJIKj00Odj4onGIKszb2W3icqneeLhabKfnoE` (gqual@gas-dev-wsl)
  verificato presente in `/home/gas/.ssh/authorized_keys` del VPS.

- 🔴→✅ **RETTIFICA — "ACCESSO SSH AL VPS PERSO" era una DIAGNOSI ERRATA.**
  La riga del 2026-07-21 attribuiva il blocco a "chiave non in authorized_keys
  (probabile: autorizzata vecchia chiave Windows poi eliminata)". FALSO.
  Causa reale: `ssh -o BatchMode=yes` + chiave con passphrase e nessun
  ssh-agent caricato → ssh non offre alcuna identità; il server risponde
  "Permission denied (publickey)" che è indistinguibile da "chiave non
  autorizzata". La chiave WSL era autorizzata sul VPS da sempre.
  LEZIONE: "Permission denied (publickey)" NON è evidenza di chiave mancante.
  Prima di qualsiasi diagnosi serve `ssh -v` e `ssh-add -l`.
  NON cancellata la riga 2026-07-21: è corretta nell'esito (accesso ripristinato),
  errata nella causa. La storia degli errori è memoria, non rumore.

- ℹ️ **Chiave `gas-vps`** (SHA256:ZEYaopShkG5R+BhOJ9NhtsGB9Cc2XaS4CB1rtMQmZEU)
  identificata: è la chiave del clone Windows deprecato
  (`C:\Users\gqual\.ssh\id_ed25519`), registrata nell'account Hetzner come
  "gas-vps" (fingerprint MD5 combaciante, creata 23gg fa = setup server S1).
  CON passphrase. Rischio terzi: ESCLUSO.
  RIMOSSA da `authorized_keys` del VPS (ambiente deprecato per policy 2026-07-15).
  Backup lasciato sul VPS: `~/.ssh/authorized_keys.bak.<timestamp>`.
  `authorized_keys` ora contiene UNA sola riga (chiave WSL), verificato con
  connessione NUOVA post-modifica.

- ⚠️ **RESIDUO NON VERIFICATO**: `/root/.ssh/authorized_keys` NON ispezionato.
  Potrebbe contenere ancora la chiave `gas-vps`. `PermitRootLogin no` la rende
  inerte via SSH, ma non è chiuso. Stato: MITIGATO, non chiuso.

- ⚠️ **RESIDUO**: la chiave `gas-vps` resta registrata in Hetzner Security →
  SSH Keys. Ogni server NUOVO creato da quel progetto nascerà autorizzando
  quella chiave. Decisione separata: rimuoverla o tenerla. Non decisa oggi.

- ℹ️ **Azioni transitorie dalla console Hetzner** (nessuna traccia in git):
  dropin `/etc/ssh/sshd_config.d/00-temp.conf` con `PasswordAuthentication yes`,
  creato e POI RIMOSSO; `sshd -T | grep -i passwordauthentication` → `no`
  verificato dopo la rimozione. `passwd gas` impostata poi `passwd -l gas`
  rilockata. `loadkeys it`. Nessun reboot, nessun riavvio di sshd oltre reload.
  COSTO REGISTRATO: finestra di alcuni minuti con `PasswordAuthentication yes`
  su IP pubblico (fail2ban attivo). Superficie di brute force temporanea,
  aperta su una diagnosi che si è poi rivelata sbagliata.

- ⚠️ **CAMBIO DI COMPORTAMENTO**: `passwd -l gas` blocca anche `sudo` con password
  per l'utente gas. Le operazioni admin sul VPS passano ora da root/console.

- ℹ️ **PRECISAZIONE alla nota VPS §7** (evitare che la memoria menta) —
  due cose DIVERSE, non confonderle:
  (a) push git da WSL: remote HTTPS, `gh auth setup-git` → nessun agent
      necessario, hook vivi. Confermato 2026-07-21.
  (b) ssh al VPS: la chiave `~/.ssh/id_ed25519` HA passphrase → serve
      `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519` a ogni sessione.
      Confermato 2026-07-22.

- ✅ **GAS in produzione**: `systemctl is-active gas` → `active`, verificato a
  fine sessione. Il servizio non si è mai fermato.

### ℹ️ Micro-finding di processo — merge su main eseguito da dentro Claude Code (2026-07-22)

**Fatto**: la PR #36 (doc-only) è stata mergiata lanciando `gh pr merge --merge 36`
**dentro la sessione Claude Code**, invece che a mano dall'operatore (browser o
terminale WSL). Merge risultante: `4c63ff3` su main.

**Merito**: nessun danno. PR doc-only; CI `29940124532` ✅ SUCCESS **prima** del
merge; scope verificato sull'handoff; invariante IP verificata prima del merge
(`git grep "204\.168"` sul branch = 0 match); la decisione di mergiare era già
stata presa dall'operatore.

**Classe**: parente di "PR #14 mergiata senza revisione" (2026-07-15), ma è una
variante diversa e va detta con precisione, altrimenti la memoria mente:
- lo STOP gate del prompt diceva "NON mergiare la PR" e **ha funzionato**:
  l'agente non ha mergiato di propria iniziativa;
- è stato l'operatore a consegnargli il comando.
Il gate umano non è stato saltato — è stato **eseguito dal canale sbagliato**.

**Perché conta comunque**: il merge umano è l'ultima barriera contro scope creep e
auto-promozione dell'agente su main. Se `gh pr merge` passa abitualmente per la
mano dell'agente, quella barriera torna **disciplinare** — e il progetto ha già
stabilito (ruleset `main-lock`, 2026-07-09) che le barriere disciplinari non
reggono quando l'agente gira con le credenziali dell'owner.

**Regola dal 2026-07-22**: il merge su main si esegue SEMPRE a mano (browser o
terminale WSL), MAI da dentro una sessione Claude Code. Vale anche per i doc-only.

**Mitigazione strutturale — CORREZIONE 2026-07-23**: il canonico registrava come possibile
fix "un token `gh` dedicato a scope ridotto (senza permesso di merge)". **VERIFICATO
IMPOSSIBILE**: aprire una PR e mergiarla richiedono lo stesso set di permessi
(Contents:write + Pull requests:write) — non sono separabili su un singolo account. Un
token che può aprire PR può anche mergiarle. La riga precedente era quindi una mitigazione
inesistente registrata come possibile: rimossa.

**Unico fix strutturale reale (decisione APERTA, non impegnata)**: un secondo account
GitHub (machine user) per le sessioni agente + `main-lock` con 1 approvazione richiesta —
GitHub vieta l'auto-approvazione, quindi l'agente potrebbe aprire la PR ma non chiuderla
da solo. Costo: un secondo account da gestire. Da valutare insieme alla privatizzazione
del repo (roadmap item 0), che richiede comunque una revisione dei permessi.

**Nel frattempo la barriera è `gasmerge` + disciplina** (vedi sezione dedicata): il gate
è reale ma resta AGGIRABILE dall'agente, che conserva il permesso tecnico di mergiare.

**Nota**: questo commit è stato scritto a mano, senza sessione Claude Code —
quindi senza `ultimo_report.md` né `handoff.md`. Non è una violazione
dell'istituzione D: non c'è alcun auto-report d'agente da verificare, il diff è
il report.

### Sessione 2026-07-23 — allineamento canonici (azioni senza traccia in git)

- ✅ **`gasmerge` — gate di merge locale** (installato e collaudato 2026-07-22). Vive in
  `~/bin/gasmerge`, **fuori dal repo** (quindi non versionato, non testato da CI, non
  revisionato: se la macchina si perde, si perde lo strumento). Uso: `gasmerge <numero-PR>`
  da WSL. Fa: verifica CI verde (blocca se non lo è), invariante IP, rilevamento file di
  motore nel diff, conferma digitata, merge, delete del branch remoto e locale,
  `pull --ff-only`, prune, stampa hash di main e numero di head.
  **Sostituisce il merge da browser.**
  ⚠️ **CAVEAT — cosa NON fa**: non toglie all'agente il permesso di mergiare. `gh` in WSL
  resta autenticato con l'account owner, quindi una sessione Claude Code può ancora
  eseguire `gh pr merge`. La barriera resta **disciplinare**, non strutturale — la stessa
  classe di barriera che il progetto ha già dichiarato insufficiente quando ha adottato
  `main-lock` (2026-07-09). L'unico fix strutturale è il secondo account (vedi sopra).

- **SEQUENZA DI MERGE OBBLIGATORIA** (dal 2026-07-22, ordine rettificato 2026-07-23):
  1) Claude Code fa il lavoro e apre la PR; 2) `/fine-task` nella STESSA sessione;
  3) **chiudere la sessione (Ctrl+D) — obbligatorio**: l'hook `session_end` pusha il
  branch all'uscita e ricreerebbe un branch appena cancellato, inoltre `gasmerge` fa
  checkout di main nella stessa working dir; 4) **revisione umana dell'`handoff.md`
  PRIMA del merge** — `gasmerge` verifica CI, invariante IP e presenza di file di
  motore, cioè la FORMA: non verifica lo SCOPE concordato né il merito, non sa cosa
  era stato mandato e non riconosce un "CHIUSO" dichiarato su un finding chiuso a
  metà. Quel controllo è umano e va fatto prima, non dopo: dopo il merge si può solo
  constatare; 5) solo con esito positivo: `gasmerge <numero-PR>` in WSL.
  Mai `gh pr merge` da dentro una sessione agente.

- ✅ **Identità git su WSL CORRETTA** (2026-07-23). Rilevato: `~/.gitconfig` **globale**
  conteneva i placeholder letterali `TUO_NOME` / `TUA_EMAIL_GITHUB` — non "configurazione
  mancante" ma valori segnaposto mai sostituiti, validi per **ogni** repo della macchina.
  Conseguenza misurata su `origin/main`: **ogni commit di lavoro** prodotto da WSL/Claude
  Code è firmato `TUO_NOME <TUA_EMAIL_GITHUB>` (es. `01cd95b`, `b695e63`, `a675c56`,
  `33018ba`); solo i merge commit portano l'identità reale, perché li crea GitHub.
  Corretto a: `Gasss23` / `290517909+Gasss23@users.noreply.github.com` (email **noreply**
  di GitHub, non quella reale: il repo è pubblico e l'email reale in chiaro su ogni commit
  è superficie per gli scraper — la reale resta comunque nella history nei merge commit).
  **Il fix vale SOLO IN AVANTI.** La history NON è stata riscritta, deliberatamente:
  cambierebbe tutti gli hash, e i canonici citano hash ovunque (`21548f74`, `2f1e015`,
  `c609e31`, `1510807`…) — si otterrebbe un file che mente su ogni riga per riparare un
  campo cosmetico. I commit vecchi restano firmati placeholder: è un fatto, non un residuo
  da nascondere.
  **Decisione APERTA (non impegnata)**: usare un trailer `Co-Authored-By` per distinguere
  in `git log` i commit d'agente da quelli scritti a mano. Oggi quella distinzione esiste
  solo come nota scritta a mano nei canonici (micro-finding 2026-07-22). Non messa
  nell'author: l'author è chi è responsabile, e il responsabile è l'operatore in entrambi
  i casi — l'agente gira con le sue credenziali.
### Sessione 2026-07-24 — sanare venv, T9a/T9c deterministici

- ℹ️ **Head su origin** (misurato live 2026-07-24 pre-push con `git ls-remote --heads origin | wc -l`): **5** head (main + 4 branch non mergiati). Valore concordante con la bonifica 2026-07-22. Dopo il push di fix/t9a-deterministico diventerà 6.
- ℹ️ **Azioni senza traccia in git** (2026-07-24): `pip install -r requirements.txt -r requirements-dev.txt` nel venv locale WSL. Non tracciabile via git; registrato qui come richiesto dal protocollo.
- ℹ️ CI attribuita a 3 commit su 2 run (PR #42). handoff.md dichiarava 'tutti e 3 i
  commit hanno CI ✅ SUCCESS': FALSO. Le run erano 2 (30054898882 su 0034a17,
  30055128981 su 2a01147). Il commit motore f6b6caa NON ha mai avuto una run propria:
  è coperto solo indirettamente, perché il suo contenuto è nell'albero di 0034a17.
  Copertura sostanziale sì, affermazione letterale no. Regola introdotta in
  .claude/commands/fine-task.md §6.
- ℹ️ gasmerge portato in scripts/gasmerge.sh (versionato). CAMBIO DI
  SUPERFICIE: il gate di merge diventa modificabile da una sessione agente, e col
  symlink un cambio entra in vigore al primo git pull. Mitigazioni: stampa di
  provenienza (SHA + dirty) prima della conferma, scripts/ e .claude/ aggiunti ai file
  sensibili. Resta disciplinare: l'agente conserva il permesso tecnico di mergiare.
- ℹ️ **Deviazione di gate — subagent revisore non invocato nativamente (2026-07-24,
  sessione chore/hardening-processo)**: la sessione Claude Code è stata lanciata con cwd
  `/home/gqual` invece di `~/Gas`, quindi `.claude/agents/` non è stato scoperto e il
  subagent `revisore` non era esposto. Le review #60 e #61 sono state prodotte da un agente
  `general-purpose` istruito a leggere e seguire `.claude/agents/revisore.md`. Merito
  verificato a campione dall'operatore (citazioni path:riga corrispondenti al codice reale,
  difetto #60 riprodotto con git stash): accettate come valide, NON ri-revisionate.
  Recidiva di un caveat già registrato (nota VPS §6: la sessione eredita la cwd del lancio,
  lanciare SEMPRE da ~/Gas). Regola ribadita: `cd ~/Gas && claude`, mai altrove.

### Sessione 2026-07-24 (p2) — merge PR #43 e registrazioni di processo

- ℹ️ **RECIDIVA — handoff §2/§3/§6 non rigenerati (PR #43)** (2026-07-24): dichiarati 5 commit / 7 file / 403 inserzioni / 67 delezioni; reali 7 commit / 9 file / 611 inserzioni / 108 delezioni. File mancanti da §2: `reports/handoff.md`, `reports/diff_sessione.md`. Commit mancanti da §3: `f5c120c`, `a88c161`. §6 fermo a `4fd0d31`, non copriva gli ultimi due commit. Causa: il template imponeva la raccolta dei blocchi in §0, PRIMA della scrittura dei file di report — i report non potevano comparire in un `git diff --stat ${BASE}..HEAD` calcolato prima della loro esistenza. Stessa famiglia del micro-finding 2026-07-13 (diff --stat riciclato), ma causa DIVERSA: là era copia-incolla manuale, qui è la struttura del template che garantisce la discrepanza. Fix strutturale: fetta A di questa sessione (step 4bis — blocchi rigenerati dopo `git add`, con `git diff --cached --stat ${BASE}`).

- ℹ️ **PR #43 mergiata DA BROWSER, non con gasmerge** (2026-07-24): il gate gasmerge con scrutinio rinforzato su file in `tests/` e `scripts/` NON è scattato. Merito verificato dall'operatore file per file prima del merge; invariante IP verificata a parte su tutto l'albero (non solo `reports/`, 0 match); CI ✅ verde garantita dal required check di main-lock. Nessun danno accertato. Registrato perché il gate è stato aggirato per CANALE, non per merito.

- 🔴→✅ **CHIUSO IN QUESTA SESSIONE — ~/bin/gasmerge NON era un symlink** (rilevato 2026-07-24): `~/bin/gasmerge` = 1747 byte, `scripts/gasmerge.sh` = 4054 byte → due script DIVERSI. Il gate versionato in PR #43 non era quello effettivamente eseguito; girava ancora la vecchia copia non versionata con il difetto noto (`gh pr checks` senza `--watch`). Conseguenza: i fix di R-gasmerge-failopen su `scripts/gasmerge.sh` avrebbero avuto effetto ZERO sul gate reale. Risolto: `ln -sfn ~/Gas/scripts/gasmerge.sh ~/bin/gasmerge`, verificato con `ls -l`. Backup della vecchia copia in `~/bin/gasmerge.vecchio.bak`. AZIONE SENZA TRACCIA IN GIT — registrata qui come richiesto dal protocollo.

- ℹ️ **Deviazione di gate PR #43: review #60/#61 da general-purpose** (2026-07-24): le review #60 e #61 sono state prodotte da un agente `general-purpose` in ruolo revisore, subagent nativo non esposto (sessione lanciata da `/home/gqual`, non da `~/Gas`). Già dichiarata nell'handoff di PR #43; qui tracciata come finding di processo. Regola operativa ribadita: lanciare SEMPRE `cd ~/Gas && claude`.

- ℹ️ **R-gasmerge-failopen — nit punto 6 aggiunto** (2026-07-24): il messaggio d'uso di `scripts/gasmerge.sh` stampa il numero del parametro posizionale (`line 13: 1: uso: gasmerge <numero-PR>`) invece del solo testo. Cosmetico. Aggiunto come punto (6) al finding R-gasmerge-failopen.

- ℹ️ **Head su origin** (misurato live 2026-07-24 con `git ls-remote --heads origin | wc -l`): **5**. CI: PR #43 merge `b3379b7` (2026-07-24, CI `30099181638` ✅ SUCCESS) — aggiornata riga CI di testa.

---

## CI storica (run su main, PR #23–#43)

> Spostata qui da `reports/stato_progetto.md` (A3, 2026-07-28) per tenere la riga CI attiva snella (~PR #44 in poi).

CI GitHub Actions — run su main (tutti ✅ SUCCESS): PR #43 merge `b3379b7` (2026-07-24, CI `30099181638`) · PR #41 merge `55959ef` (2026-07-23, CI `30051234981`) · PR #40 merge `4391c8b` (2026-07-22, CI `29967190300`) · PR #37 merge `cb7ba8b` (2026-07-22, CI `29942831200`) · PR #36 merge `4c63ff3` (2026-07-22, CI `29941994238`) · PR #35 merge `425ba5c` (2026-07-22, CI `29919691907`) · PR #34 merge `45a1708` (2026-07-22, CI `29898591182`) · PR #33 merge `5dae638` (2026-07-21, CI `29848173628`) · PR #32 merge `f2679a4` (2026-07-20, CI `29775144603`) · PR #27 merge `21548f74` (2026-07-19, CI `29695063005`) · PR #25 merge `c609e31` (2026-07-19, CI `29664233791`) · PR #24 merge `fd3d47a` (2026-07-18) · PR #23 merge `2f1e015` (2026-07-18).

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


- ✅ **R-legacy-slice CHIUSO** (2026-07-15, questa PR): `brains/claude_brain.py` rimosso con la pulizia F3 — lo slicing `messages[-8:]` è stato eliminato alla radice insieme al file che lo conteneva. Nessun residuo.
- ✅ **F6-history-atomica CHIUSO** (2026-07-16, review #50 APPROVATO, PR #19, CI run `29482410951` ✅ 241 PASS): `_save_history` usa ora tmp+`os.replace` atomico (fsync); `_load_history` quarantena il file corrotto in `.gas_history.json.corrupt.<ts>` (logging.warning, mai crash). Test T59a/b/c. **Mergeata → 9a9278e su main ✅ (2026-07-16, CI run 29484338680 SUCCESS)**.
- ✅ **R-crm-diario-rr CHIUSO** (2026-07-16, PR #18 `fix/diario-recursive-triggers`): aggiunto `PRAGMA recursive_triggers = ON` in `MemoryStore._connect()` — con ON il DELETE implicito della REPLACE attiva `diario_no_delete` (ABORT). Nuovo test T19f-rr copre il varco via `m._connect()`. Revisore: APPROVATO CON RISERVE (riserva risolta in-session). OR REPLACE sul diario: assente (verificato su `unisci_contatti`, `unisci_contatti_con_snapshot`, tutti i moduli).
- ✅ **R-ci-hooks CHIUSO** (2026-07-18, merge `2f1e015` PR #23, CI run `29645320495` ✅ SUCCESS su main): `tests/test_unit_hooks.py` ora eseguito da CI. Storia del finding sotto. // ex-🟡 — `tests/test_unit_hooks.py` NON eseguito da CI (sonda 2026-07-17): il job `unit-suite` esegue SOLO `python tests/test_unit_kernel.py` (ci.yml riga 83). Il file `test_unit_hooks.py` esiste in `tests/` (T-hook-a/b/c/d/e/f/g/h, 357 righe) ma non compare in nessun comando del workflow. Il verde copre `tests/test_unit_kernel.py` meno gli SKIP (T9a/T9c su assenza GEMINI/GROQ API key), e NON copre `tests/test_unit_hooks.py`.
  **Implicazione**: I finding hook chiusi con PR #20 (fbf8246) e PR #21 (8f9cf7b) citano "CI run ✅ SUCCESS" come evidenza. Quel verde non ha eseguito alcun test degli hook: `tests/test_unit_hooks.py` non è nel workflow. L'unica evidenza che T-hook-a…g passano è un `pytest tests/test_unit_hooks.py` eseguito in locale e riportato dall'agente — non un artefatto CI. Nessun difetto accertato negli hook; ma la citazione del verde CI accanto a un fix di hook implica una validazione che non è avvenuta. Finché R-ci-hooks è aperto, il verde CI non è evidenza valida per modifiche a `.claude/hooks/`.
  **Stato (2026-07-18)**: ✅ CHIUSO. PR `fix/ci-hook-tests` mergiata → merge `2f1e015` (PR #23) su main; CI run `29645320495` ✅ SUCCESS ha eseguito i test hook. Il gap su main è colmato. Da questo punto il verde CI copre anche `.claude/hooks/`.
- ✅ **R-hook-jq CHIUSO** (2026-07-19, fix/hook-jq-failloud → merge PR #25 `c609e31` su main, CI run `29664233791` ✅ SUCCESS): `scrivi_rep.sh` ora fail-loud quando jq è assente/non funzionante (trigger via `grep -qi "scrivi rep"`, poi `if ! jq --version >/dev/null 2>&1; then warn>&2; exit 0; fi`, nessun file/commit). Commento riga 3 corretto (stantio da main-lock). T-hook-i (jq assente) + T-hook-j (detached-HEAD) aggiunti.
  **Flag #1 — CHIUSO per ispezione (2026-07-19):** verificato sul file reale in `main` (`c609e31`), NON dal report dell'agente — il check è **exit-status-based** (`if ! jq --version >/dev/null 2>&1`): copre sia jq assente sia jq non funzionante (fake exit 1). Criterio soddisfatto → chiuso pieno.
  **Merito coperto da CI reale:** R-ci-hooks chiuso (PR #23), quindi il run `29664233791` su `c609e31` ha eseguito `tests/test_unit_hooks.py` (ci.yml riga 93) inclusi T-hook-i/j — artefatto CI reale, supera il "10/10 PASS" locale del report.
  **Flag #2 — micro-finding di processo (registrato, non bloccante):** revisore #56 ha restituito SOLO la riga di memoria (`#56 — APPROVATO — …`), nessuna analisi del diff. Il gate motore si applicava (il diff toccava `tests/`) ma ha prodotto un verdetto degenere: il merito NON è stato validato dal revisore, ma per altra via (ispezione + CI). Stessa classe di PR #14/#18. Nota tecnica: `jq --version` (functional check) anziché `command -v jq` perché `/bin`→`/usr/bin` (symlink) rende impossibile separare jq da bash/grep nel PATH nei test.
  ℹ️ **Flag #3 — verdetto degenere, recidiva (2026-07-24, review #59):** come #56, il revisore ha restituito la sola riga di memoria ('APPROVATO — nessuna lezione nuova') senza analisi del diff, su un diff che toccava tests/. Terza occorrenza della classe (#56, #59, più PR #14/#18). Contromisura: obbligo di evidenza nel verdetto introdotto in .claude/agents/revisore.md il 2026-07-24. Limite dichiarato: è regola di forma, non check meccanico → finding aperto R-verdetto-evidenza.
- ✅ **R-ci-summary CHIUSO** (2026-07-23, PR #41, merge `55959ef`, CI `30051234981` ✅ SUCCESS). Evidenza da ispezione diretta di `.github/workflows/ci.yml` su `origin/main`: step "Run hook suite" con `set -o pipefail` + `tee "$RUNNER_TEMP/hooks_output.txt"`; step "Job summary" legge `hooks_output.txt` e pubblica `hriep` nel riquadro `| Hook suite |`. La hook suite (pytest) ora compare nel Job Summary a colpo d'occhio. // ex-🟡 (riserva #55(2), cosmetica) — il Job Summary di `ci.yml` catturava via `tee` solo `test_unit_kernel.py`; la hook suite (pytest) non compariva nel summary. Mancava solo la visibilità nel riquadro.
- ✅ **R-ci-openrouter CHIUSO** (2026-07-24, fetta 1 commit `f6b6caa`, branch fix/t9a-deterministico, revisore #59 APPROVATO). **Storia degli errori (NON cancellata)**: la formulazione storica "T9a fragile se OPENROUTER_API_KEY è presente" era IMPRECISA — il difetto reale era che il gate `_has_live_keys = bool(GEMINI_API_KEY and GROQ_API_KEY)` rendeva T9a e T9c SEMPRE SKIP in CI (chiavi assenti per design, nessun secrets nel workflow): il cap a 10 iterazioni del loop agentico (CLAUDE.md §8) non ha mai avuto copertura CI dall'introduzione dei test. La radice era nella costruzione dei rung: senza chiavi, `if not os.environ.get(env): continue` in `run_turn` costruisce ZERO rung per Gemini/Groq, quindi anche T9b passava "a vuoto" (cascata a 0 rung, subito esausta) — non esercitava il cap del loop. **Fix**: inject GEMINI_API_KEY e GROQ_API_KEY fittizie nel blocco T9 con save/restore nel finally (stesso pattern di OPENROUTER_API_KEY). Eliminato `_has_live_keys`. 250 PASS, 0 FAIL, 0 SKIP in locale e con socket bloccato.
- ✅ **R-gasmerge-failopen CHIUSO** (2026-07-24, branch `fix/gasmerge-failopen`, review #62 + #63 APPROVATI CON RISERVE):
  (1) ✅ **git diff fail-open** → separato git diff da grep, case rc 0/1/≥2, BLOCCA su errore git (T-gasmerge-g).
  (2) ✅ **git grep fail-open** → set+e/RC/set-e/case, BLOCCA su rc≥2 invece di stampare "0 match OK" (T-gasmerge-e).
  (3) ✅ **TOCTOU** → secondo `git fetch --prune` dopo attesa CI; `HEAD_SHA=$(gh pr view ... --json headRefOid)` + `--match-head-commit "$HEAD_SHA"` su `gh pr merge`.
  (4) ✅ **jq presence-check** → sostituito con `jq --version` functional check, coerente con #56 (T-gasmerge-c).
  (5) ✅ **scope IP solo reports/** → esteso a tutto l'albero del branch; sonda origin/main: 0 match (T-gasmerge-f).
  (6) ✅ **messaggio d'uso con numero parametro** → validazione esplicita, solo testo su stderr, exit 2 (T-gasmerge-a/b).
  Suite: 7 test PASS, 6/7 FAIL su vecchio script (1 PASS = guard preesistente, regressione).
  Riserve aperte (non bloccanti, da monitorare):
  - **#62-R1** → MITIGATO in sessione 2026-07-26 (vedi sotto).
  - **#62-R2** → ereditata come #65-R2 (vedi sotto).
  - **#63-R1**: stub git hardcoda `/usr/bin/git` (non portabile su sistemi con git altrove).
  - **#63-R2** → ereditata come #65-R3 (vedi sotto).
  Cambio di superficie: `GAS_REPO_DIR` rende gasmerge puntabile a repo arbitrario via env — non aggiunge potere reale (chi ha `gh` è già owner), ma dichiarato.
  **Sessione 2026-07-26 — FETTE 1-3 completate (review #65 APPROVATO CON RISERVE):**
  - ✅ **FETTA 1** — invariante IP: marker `gasmerge-ip-ok` + filtro a 2 passi fail-closed. Deny-by-default: un IP senza marker blocca sempre (es. "1.0.0.0" → BLOCCO); con marker sulla stessa riga → allowlistato (`FILTER_RC=1` = tutti OK; `FILTER_RC>=2` = errore filtro → BLOCCO). #62-R1 MITIGATO. # gasmerge-ip-ok
  - ✅ **FETTA 2** — TOCTOU completo: HEAD_SHA catturato dopo tutti i controlli e prima del prompt; ri-fetch + ri-lettura head post-read; BLOCCO "head cambiata durante la conferma". Residuo dichiarato: micro-ms sincroni pre-prompt.
  - ✅ **FETTA 3** — test: 11/11 PASS (erano 7); proof fail-su-vecchio: FAIL su `test_ip_with_marker_passes` e `test_head_changed_during_confirm_blocks` su `/tmp/gasmerge_pre.sh`.
  Riserve da #65 (non bloccanti):
  - **#65-R1** (nuova): guard HEAD_SHA vuoto mancante — se jq produce output vuoto, HEAD_SHA=""; il confronto `"" != ""` è false e si procede con `--match-head-commit ""`. Fail-closed in pratica (gh rifiuta SHA vuoto) ma non nel codice. Fix: `[ -n "$HEAD_SHA" ]` dopo la cattura.
  - **#65-R2** (ereditata #62-R2): `--match-head-commit` senza copertura test positiva end-to-end.
  - **#65-R3** (ereditata #63-R2): `/tmp/gaspr.json` condiviso nel pattern headRefName del nuovo stub TOCTOU — non thread-safe con pytest-xdist.
  **Collisione contatore #62 riconciliata (2026-07-26):** sessioni parallele avevano minato entrambe #62 da #61. main #62 = PR #45 (check_verdetto.py, 07-25); branch #62/#63 = gasmerge failopen + test (07-24). Al merge di origin/main nel branch: branch tiene #62/#63, review PR #45 rinumerata in #64. Nessuna review persa — la memoria non mente.

- ✅ **R-crm-1b CHIUSO** (email+merge+idempotenza+telefono fetta 3 review #67 + esposizione fetta 4 review #68, entrambi APPROVATI CON RISERVE; merge PR #47 `d67b12a` 2026-07-27). Fetta email ✅ + merge umano ✅ + idempotenza diario ✅ + telefono ✅ + **esposizione operatore (fetta 4) ✅**: `gas doctor` sezione CRM (conta email+telefono, WARN se > 0, mai exit 1, fail-safe §9) + comando `gas duplicati` (lista coppie email+telefono, sola lettura, exit 0, fail-safe); 4 nuovi test T61a–T61d; **276 PASS, 0 FAIL**. **DECISIONE APERTA dedup doctor/CLI → CHIUSA**: esposto email+telefono insieme in `gas doctor` (sez. CRM) + `gas duplicati`, sola lettura, nessuna funzione di scrittura esposta al modello. 4 riserve non bloccanti (R1–R4): **R1** `int(r["id"])` fuori try/except (fetta 3, #67); **R2** ramo `chiave_norm` non coperto da T60 (#67); **R3** commento `# 11 CRM` fuori sequenza in gas.py (cosmetico, #68); **R4** T61d `or "Duplicati"` sempre vera — non asserisce strettamente "non disponibile" (#68).
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
