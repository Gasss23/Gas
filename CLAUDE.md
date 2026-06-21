# ⛽ GAS — COMPLETE ARCHITECTURAL SYSTEM MEMORY (10-SECTION CANON)

## 1. PROJECT CONTEXT & VISION
Gas non è un tool di coding, ma un agente AI personale autonomo destinato a girare su VPS (partner strategico di business). L'obiettivo finale è un Jarvis attivo h24 focalizzato su autonomia, interfaccia vocale e marketing. La robustezza (zero crash) conta più della potenza.

## 2. ARCHITECTURE & TECH STACK
- Language: Python 3.11+ gestito in ambiente virtuale (venv).
- Architecture: Pipeline multi-brain con sistema di paracadute (fallback automatico a cascata: Claude per strategia, Gemini per dati, Groq per velocità).
- Core Files: gas.py (Kernel), modules/marketing/ (Funnel).

## 3. CORE COMMANDS & WORKFLOWS
- Esecuzione Kernel / Test: python -c "from gas import GasKernel; ..."
- Auto-diagnosi: python gas.py doctor — check API keys, connettività provider (OK/QUOTA/KO), integrità file e storia, dimensione log. Exit code 0 se OK/WARN, 1 se FAIL. Non consuma token LLM (solo ping minimi max_tokens=1).
- Ispezione Errori: Lettura e analisi chirurgica del file gas_debug.log.
- Convenzione reports/: il report di fine task va scritto in reports/ultimo_report.md ed è l'UNICA fonte di verità sull'esito del task.
- Regola di reporting (OBBLIGATORIA): alla fine di ogni task, dopo aver scritto e pushato reports/ultimo_report.md, stampare a terminale ESATTAMENTE, senza riassumere né parafrasare: (1) il path del report, (2) l'hash del commit che lo contiene, (3) il contenuto integrale del file appena scritto (un cat del file). Mai dare a voce un riassunto diverso dal contenuto del file; ogni discrepanza tra schermo e file è un errore da segnalare.
- Commit ESPLICITO dei report (OBBLIGATORIO dal 2026-06-15): l'agente committa e pusha DA SÉ i propri report/doc (ultimo_report.md, stato_progetto.md, diff_sessione.md) in UN commit a fine task, con messaggio descrittivo. NON delegare questo all'hook SessionEnd: l'hook è solo una rete di sicurezza. Motivo: un commit di report dell'agente (7005517) aveva sovrascritto il report canonico (ripristino manuale 412714f); l'auto-commit dell'hook poteva persistere+pushare quella sovrascrittura senza checkpoint d'intento. Committando i report di propria mano si ripristina il checkpoint e in steady-state l'hook non trova più reports/ da committare.
- Feature "scrivi rep" (Stop hook `.claude/hooks/scrivi_rep.sh`): al trigger `scrivi rep` salva la risposta PRECEDENTE in `reports/ultima_risposta.md`, poi committa e pusha DA SÉ. Dal 2026-06-15 i suoi commit usano il prefisso `chore(scrivi-rep):` per essere riconoscibili/filtrabili nel log (es. `git log | grep -v chore` per nasconderli). Il file `reports/ultima_risposta.md` resta VOLUTAMENTE versionato/committato/pushato: serve per la sync multi-device (si lavora da PC diversi). NON è rumore da eliminare ma una feature autorizzata; cambiarne il comportamento è decisione umana.
- Gate di review OBBLIGATORIO (attivo dal 2026-06-13): PRIMA di ogni `git commit` il cui diff staged tocca gas.py, brains/, modules/ o tests/, l'agente principale DEVE invocare il subagent `revisore` sul diff e attendere il verdetto. Commit consentito solo se APPROVATO o APPROVATO CON RISERVE (riserve tracciate in stato_progetto.md). Commit di soli reports/ o doc (CLAUDE.md, *.md) NON richiedono review. Questa regola e' la barriera PRIMARIA; il hook deterministico PreToolUse (`.claude/hooks/review_gate.sh`, marcatore `.claude/.review_ok`) e' la rete di sicurezza, best-effort, non un sostituto. Mai bypassare via auto-commit: l'hook SessionEnd (`.claude/hooks/session_end.sh`) è puramente ADDITIVO e CONDIZIONALE — fa stage del solo allowlist (reports/, *.md, .gas_history.json), se nulla è in staging ESCE senza commit (niente commit vuoti = niente rumore nel log), non esegue MAI git distruttivi e ha un'invariante che toglie dallo staging eventuali file del motore. Il suo lavoro ricorrente legittimo è persistere .gas_history.json.
- Le tre istituzioni di processo (attive dal 2026-06-11):
  - A) reports/stato_progetto.md — fotografia viva dello stato del progetto (motore, finding aperti, prossimi passi). Va aggiornata a fine di ogni task.
  - B) reports/diff_sessione.md — a fine sessione, riepilogo del diff della sessione: file toccati, cosa è cambiato e perché. Si riscrive a ogni sessione (fotografia dell'ultima sessione, la storia completa sta in git).
  - C) Subagent revisore (.claude/agents/revisore.md) — revisiona ogni modifica al motore prima del commit, per correttezza tecnica E coerenza col progetto. PRIMA di ogni review legge obbligatoriamente CLAUDE.md (sez. 5), reports/stato_progetto.md e la sua memoria persistente .claude/agents/memoria_revisore.md; DOPO ogni review aggiunge a quella memoria le eventuali lezioni nuove (1-3 righe, datate).

## 4. CODE STYLE & CONVENTIONS
- Funzioni pulite, focalizzate e uso rigoroso dei Type Hints di Python.
- Obbligo di aggiornare lo stato e la cronologia in modo atomico dopo ogni operazione andata a buon fine.

## 5. ANTIPATTERNS & "THE WALL OF SHAME" (CRITICAL)
- NO Tool Simulation: Vietato inventare o simulare l'output dei tool. I modelli devono invocare ed eseguire i tool nativi reali (read_file, write_file).
- NO Raw History Slicing: Mai tagliare la cronologia messaggi con [-10:] o simili. Causa il troncamento di sequenze di tool call, mandando in crash le API (es. Gemini 400 Bad Request). Usare SEMPRE l'helper _get_window().

## 6. STATE & MEMORY MANAGEMENT
- Lo stato viene preservato tra le sessioni salvando la cronologia nel file .gas_history.json.
- Prima di inviare la storia ai provider, viene applicata self._get_window() per garantire che la sequenza parta sempre da un messaggio role: user coerente.
- Separazione delle memorie: gas_identity.md = identità runtime di Gas (~200 token, iniettata nel system prompt a ogni chiamata); CLAUDE.md = memoria di sviluppo per Claude Code (Gas la legge on-demand via read_file, non viene iniettata). Se gas_identity.md manca, fallback su _GAS_SYSTEM_PROMPT_BASE.
- Memoria di lungo periodo (DB SQLite `.gas_memory.db`, modulo `modules/memory/`, FASE 2): il kernel scrive da sé nel **diario** (append-only) una riga per ogni tool call dentro `run_turn` (fetta 2a, lato scrittura). In lettura (fetta 2b): `_memoria_pin()` inietta un blocco compatto ALWAYS-ON (lead attivi + poche azioni significative) **nel messaggio system** — `self.system_prompt + mem_pin`, calcolato una volta per turno, FUORI dalla finestra (`_get_window`/`_cap_window_chars` NON toccati), capato a `MEMORY_PIN_CHAR_CAP`. Il tool `ricorda()` (SOLA LETTURA, in-process, niente sandbox/snapshot) pesca diario/contatti on-demand. La **rubrica lead** si popola dal loop con i tool `salva_contatto` (upsert anagrafica, NON tocca lo stato) e `imposta_stato_contatto` (transizione di stato nel funnel, match ESATTO sulla chiave): scrittura in-process parametrizzata (il modello non scrive SQL grezzo), tracciata nel diario. I contatti sono MUTABILI per natura; il diario resta IMMUTABILE. Tutto FAIL-SAFE §9: memoria assente/degradata → pin vuoto/diniego e turno che prosegue, mai crash. Tetti del pin configurabili via env `GAS_MEMORY_PIN_CHARS/CONTACTS/EVENTS`. NB la scrittura della memoria è codice fidato del kernel e bypassa CORRETTAMENTE il sandbox bwrap (che vale solo per `run_command`).

## 7. TESTING & VERIFICATION REQUIREMENTS
- Ogni modifica al motore richiede un test di round-trip agentico per verificare che il ciclo non si interrompa dopo la prima tool call.
- Validazione obbligatoria tramite esecuzione diretta prima di considerare un bug come "risolto".

## 8. API & EXTERNAL SERVICE GUARDRAILS
- Agentic Loop Cap: La funzione run_turn deve implementare un ciclo while blindato da un massimo di 10 iterazioni (for _ in range(10)) come barriera anti-loop infinito per preservare il budget delle API.
- Model Awareness: Il sistema deve monitorare e dichiarare all'utente i cambi di efficienza o i passaggi a versioni minori (es. Gemini Flash-lite).

## 9. SECURITY & ERROR HANDLING
- Ogni eccezione nei provider deve essere intercettata, loggata come logging.warning nella "scatola nera" (gas_debug.log), attivando immediatamente il fallback sul brain successivo senza far crashare il programma.

## 10. FUTURE ROADMAP & PRIORITIES

Completati (storico): snapshot preventivo anti-autodistruzione (2026-06-11), comando gas doctor, sandbox di run_command no-shell+allowlist con modalita dry-run (2026-06-12, finding esfiltrazione 🟠->🟡 ridotto), sandbox OS bwrap (rete isolata + fs read-only, modalita os_strict/os_with_fallback, sonda _probe_os_sandbox + check in gas doctor) — chiude DEL TUTTO il finding esfiltrazione. WINDOW_CHAR_CAP sulla finestra a granularita di messaggio (2026-06-14, review #7/#8) e manutenzione snapshot in gas doctor (2026-06-14, review #10) — **FASE 1 CHIUSA**. **FASE 2 (cervello/memoria low-cost) CHIUSA** (2026-06-15 → 2026-06-19): memoria SQLite con diario IMMUTABILE (review #12/#13), iniezione always-on + tool ricorda (review #14), CRM contatti dal loop con chiavi normalizzate/chiave_norm (review #15/#16/#22), ricerca FTS5 sul diario (review #18), backup automatico anti-corruzione del DB (review #19), vector store fetta 1 storage+embedding (review #23) + wiring retrieval semantico al kernel opt-in GAS_VECTORS (review #24), comando CLI gas reindex (review #25). Soglia semantica `VEC_MIN_SIM` resa env-configurabile via `GAS_VECTORS_MIN_SIM` (2026-06-21, review #28) — chiude la parte azionabile di R-wire-1 (resta solo la ri-taratura, deploy-dependent).

### 🔴 FASE 1 — Blindatura del Terminale & Sicurezza — ✅ CHIUSA
- Snapshot preventivo anti-autodistruzione — ✅ FATTO (2026-06-11), base della blindatura.
- Sandbox OS per run_command (bwrap/unshare: namespace di rete chiuso + filesystem read-only) — ✅ FATTO: chiude DEL TUTTO il finding esfiltrazione. Implementati la sonda reale _probe_os_sandbox (cache di processo), il prefisso _bwrap_prefix (--unshare-net/--unshare-pid + fs read-only) e le due modalita GAS_SANDBOX_MODE: os_strict (fail-closed se bwrap/namespace assenti) e os_with_fallback (degrada alla sola sandbox applicativa). Check di disponibilita presente in gas doctor.
- WINDOW_CHAR_CAP sulla finestra, a granularita di messaggio (mai slicing) — ✅ FATTO (2026-06-14, review #7/#8): tetto rigido 24000 char via _cap_window_chars, scarto di messaggi interi + riallineamento a un role:user (mai slicing, §5).
- Manutenzione snapshot in gas doctor: conteggio ref, gc degli oggetti orfani, rotazione di reports/snapshots.log — ✅ FATTO (2026-06-14, review #10): retention ibrida (count+età), doctor sez.7 di solo report, gc OPT-IN manuale (nessun prune distruttivo automatico, §10).

### 🧠 FASE 2 — Il Cervello di Jarvis & Memoria Low-Cost — ✅ CHIUSA
- Database locale SQLite per i fatti rigidi (gratis, zero token) — ✅ FATTO (2026-06-15, review #12/#13): modulo `modules/memory/`, DB file singolo `.gas_memory.db`, diario append-only IMMUTABILE (trigger BEFORE UPDATE/DELETE → ABORT) + rubrica contatti mutabile. CRM dal loop con tool salva_contatto/imposta_stato_contatto e chiavi normalizzate (chiave_norm UNIQUE + NFKC) — ✅ FATTO (review #15/#16/#22). Iniezione always-on (_memoria_pin) + tool ricorda di sola lettura — ✅ FATTO (review #14). Ricerca FTS5 sul diario (Strato A) — ✅ FATTO (2026-06-17, review #18).
- Vector DB locale per i ricordi a lungo termine senza consumo di token — ✅ FATTO (2026-06-18): fetta 1 storage+embedding semantico locale (fastembed `paraphrase-multilingual-MiniLM-L12-v2`, sidecar `.gas_vectors.db` cache derivata, cosine brute-force, review #23) + wiring al kernel — retrieval semantico opt-in via env `GAS_VECTORS`, catch-up indexing in run_turn + cascata FTS→semantico in ricorda (review #24). Comando CLI di manutenzione `gas reindex` (ricostruisce l'indice dal diario) — ✅ FATTO (2026-06-19, review #25).
- **Backup della memoria** — ✅ FATTO per l'auto-corruzione (2026-06-17, review #19): `MemoryStore.backup()` + `backup_auto()` THROTTLED con integrity-gate (un DB corrotto non viene mai copiato sopra i backup buoni) + rotazione, e check in gas doctor sez.8. Il backup OFF-MACHINE (anti-disastro disco, copia su volume/host esterno) resta a FASE 5 / deploy VPS — vedi item aperti.
- (parcheggiato, NON prioritario) Script revisor.py (API low-cost) per il "Claude Council". NB: chiarire cosa si intende per "Claude Council" — il nome non corrisponde a un prodotto Anthropic noto. Nessun impegno.

### 🟡 ITEM APERTI / PROSSIMI PASSI (in ordine di priorità)
1. **R-wire-1 (RESIDUO) — ri-taratura di `VEC_MIN_SIM` sul primo diario reale del VPS.** La configurabilità via env è ✅ FATTA (2026-06-21, review #28): helper `_env_float` fail-safe + clamp [0,1], override `GAS_VECTORS_MIN_SIM` risolto in `__init__` come `CATCHUP_MAX`, default di classe 0.30 INVARIATO. Resta SOLO la ri-taratura del valore, che richiede il diario reale (il MiniLM separa debolmente le query corte IT) → voce CHECKLIST pre-deploy VPS, niente redeploy necessario per cambiarlo.
2. **Valutare il modello e5-small al posto di MiniLM** (qualità del retrieval italiano), legato al nodo RAM del VPS (R-vec-3): da decidere insieme al vincolo memoria del deploy.
3. **R-reidx-3 — picco RAM di `gas reindex` su diario grande** (materializza tutti gli embedding prima del DELETE) → voce CHECKLIST pre-deploy VPS (1GB); mitigazione candidata: re-index a scaglioni o swap.
4. **FASE 3 — Interfaccia vocale: Whisper (STT) e successive** (vedi FASE 3 sotto).
5. **FASE 5 — Migrazione/deploy su VPS Hetzner** (target indicato dall'utente; vedi FASE 5 sotto). Include il backup OFF-MACHINE della memoria.

> Chiusi di recente (storico): **R-crm-norm-2** — esporre `collisione_chiave_norm`/corruzione in `gas doctor` sez.8 → ✅ FATTO (2026-06-20, review #27, commit `56a6dc3`).

### 🎙️ FASE 3 — Interfaccia Vocale (Priorità Media — Core Feature)
- Whisper (STT) per ricevere comandi vocali diretti (input terminale a mani libere durante lo sviluppo).
- ElevenLabs (TTS) per far rispondere GAS a voce alta come un vero assistente personale.

### 📈 FASE 4 — Moduli di Business (Priorità Media)
- Modulo Meta Ads e automazione della lead generation.
- Algoritmi di persuasione locali per il copy e i DM di marketing.

### 🚀 FASE 5 — Autonomia Totale & VPS (Priorità Lunga)
- Migrazione/deploy su **VPS Hetzner** (target indicato dall'utente) h24 con trigger temporali (cron-job) per far lavorare Jarvis di notte a computer spento.
- Backup OFF-MACHINE della memoria (copia di `.gas_memory.db` su volume/host esterno) — vera protezione anti-disastro disco, banale perché il DB è un file singolo.
- Automazione canali brand.

### 💡 Idee da valutare (NON prioritarie)
- Valutare utilizzo o integrazione openclaw (agente IA esterno). NB: prima verificare licenza, dipendenze, qualità e superficie di sicurezza; mai copia-incolla nel motore. Idea parcheggiata, nessun impegno.
