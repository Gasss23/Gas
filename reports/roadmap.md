Roadmap e completati storici di GAS — dettaglio integrale. Sommario e stato corrente in CLAUDE.md e reports/stato_progetto.md.

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
1. **🔴 URGENTE — Controllo della spesa token (soluzione DEFINITIVA).** Spesa rilevata ~8€/giorno (22 e 23 giugno 2026): troppo per lo stato attuale di GAS. Intervenire con massima urgenza. **PRIMO PASSO obbligatorio = DIAGNOSI, non tagli alla cieca: distinguere DOVE vanno i token.** Ipotesi forte da verificare insieme: il costo di questi giorni è quasi tutto **lato SVILUPPO (Claude Code / Opus in queste sessioni lunghe)**, NON il runtime di GAS (che non è ancora deployato h24). Le due leve sono diverse:
   - **(A) Costo di sviluppo (Claude Code) — è ciò che ha speso 8€ oggi.** Idee da valutare: usare un modello più economico (Sonnet) per i task meccanici/di routine e riservare Opus alla strategia; ridurre il contesto ricaricato ogni sessione (CLAUDE.md e `reports/stato_progetto.md` ~899 righe/~35k token vengono letti spesso → potare/archiviare lo storico in un file separato fa risparmiare token ad ogni turno); evitare ri-letture di file grandi; sessioni più corte e mirate; `/fast` con criterio.
   - **(B) Costo a runtime (kernel GAS, per quando girerà h24 sul VPS).** Idee: tetto rigido `max_tokens`; preferire SEMPRE i rung gratuiti della cascata (Groq/Gemini/OpenRouter-free/Ollama) e usare Claude SOLO per la strategia; `WINDOW_CHAR_CAP`/pin già aiutano; **contabilità token osservabile** (log per turno/provider, comando tipo `gas tokens`) — "non puoi controllare ciò che non misuri"; **budget giornaliero con kill-switch** fail-safe.
   - Esito atteso della soluzione definitiva: (1) MISURARE la spesa, (2) routing cheap-by-default, (3) cap giornaliero con stop. **Da valutare e scegliere insieme domani.**
2. **📱 Accesso/controllo di Claude Code su GAS da telefono (lavorare in mobilità, anche da assente).** Obiettivo: lanciare comandi a Claude Code per lavorare su GAS quando non sono al PC. Idee da valutare insieme domani (nessun impegno):
   - **Claude Code su web/mobile** (claude.ai/code dal browser del telefono, puntato al repo) — la via più diretta, zero infrastruttura.
   - **Bridge bot (Telegram/WhatsApp) → VPS**: il telefono manda comandi a un bot, il VPS esegue Claude Code headless. Si sposa con l'identità "Jarvis" e con FASE 3 (vocale) + FASE 5 (VPS).
   - **GitHub-centrico**: aprire issue/commenti dal telefono che un Claude Code GitHub Action raccoglie ed esegue (ora che la CI/Actions è in piedi).
   - **SSH dal telefono** (Termius/Blink) in tmux sul VPS — low-effort, tecnico.
   - Naturale da abilitare una volta su VPS (FASE 5); valutare sicurezza/autorizzazione degli accessi remoti.
3. **R-wire-1 (RESIDUO) — ri-taratura di `VEC_MIN_SIM` sul primo diario reale del VPS.** La configurabilità via env è ✅ FATTA (2026-06-21, review #28): helper `_env_float` fail-safe + clamp [0,1], override `GAS_VECTORS_MIN_SIM` risolto in `__init__` come `CATCHUP_MAX`, default di classe 0.30 INVARIATO. Resta SOLO la ri-taratura del valore, che richiede il diario reale (il MiniLM separa debolmente le query corte IT) → voce CHECKLIST pre-deploy VPS, niente redeploy necessario per cambiarlo.
4. **Valutare il modello e5-small al posto di MiniLM** (qualità del retrieval italiano), legato al nodo RAM del VPS (R-vec-3): da decidere insieme al vincolo memoria del deploy.
5. **R-reidx-3 — picco RAM di `gas reindex` su diario grande** (materializza tutti gli embedding prima del DELETE) → voce CHECKLIST pre-deploy VPS (1GB); mitigazione candidata: re-index a scaglioni o swap.
6. **FASE 3 — Interfaccia vocale: Whisper (STT) e successive** (vedi FASE 3 sotto).
7. **FASE 5 — Migrazione/deploy su VPS Hetzner** (target indicato dall'utente; vedi FASE 5 sotto). Include il backup OFF-MACHINE della memoria.

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
