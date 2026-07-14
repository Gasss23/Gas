Roadmap e completati storici di GAS — dettaglio integrale. Sommario e stato corrente in reports/roadmap.md (roadmap) + reports/stato_progetto.md (stato vivo). CLAUDE.md sez. 10 è solo un puntatore a questo file.

## 10. FUTURE ROADMAP & PRIORITIES

Completati (storico): snapshot preventivo anti-autodistruzione (2026-06-11), comando gas doctor, sandbox di run_command no-shell+allowlist con modalita dry-run (2026-06-12, finding esfiltrazione 🟠->🟡 ridotto), sandbox OS bwrap (rete isolata + fs read-only, modalita os_strict/os_with_fallback, sonda _probe_os_sandbox + check in gas doctor) — chiude DEL TUTTO il finding esfiltrazione. WINDOW_CHAR_CAP sulla finestra a granularita di messaggio (2026-06-14, review #7/#8) e manutenzione snapshot in gas doctor (2026-06-14, review #10) — **FASE 1 CHIUSA**. **FASE 2 (cervello/memoria low-cost) CHIUSA** (2026-06-15 → 2026-06-19): memoria SQLite con diario IMMUTABILE (review #12/#13), iniezione always-on + tool ricorda (review #14), CRM contatti dal loop con chiavi normalizzate/chiave_norm (review #15/#16/#22), ricerca FTS5 sul diario (review #18), backup automatico anti-corruzione del DB (review #19), vector store fetta 1 storage+embedding (review #23) + wiring retrieval semantico al kernel opt-in GAS_VECTORS (review #24), comando CLI gas reindex (review #25). Soglia semantica `VEC_MIN_SIM` resa env-configurabile via `GAS_VECTORS_MIN_SIM` (2026-06-21, review #28) — chiude la parte azionabile di R-wire-1 (resta solo la ri-taratura, deploy-dependent). **ITEM APERTI CHIUSI TUTTI** (2026-06-27, review #38, commit a8c6d53): budget cap `GAS_DAILY_TOKEN_BUDGET` + Telegram bridge bot `modules/telegram/bot.py` + `gas calibrate-vectors` + `gas eval-vectors` + R-reidx-3 già chiuso (review #30). **FASE 2.5 (compressione history) CHIUSA** (2026-06-27, review #39, commit 65c4c7b): `_compress_history_if_needed()` auto-trigger + `gas compress-history` CLI, zero token LLM. **FASE 5 IN CORSO**: S1 ✅ hardening SSH + utente runtime (2026-07-04), S1b ✅ (2026-07-04), prossimo S2.

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

### ✅ ITEM APERTI CHIUSI (2026-06-27, review #38, commit a8c6d53)

> Tutti e 5 gli item aperti sono stati chiusi in questa sessione.

1. ✅ **Controllo spesa token (DEFINITIVO)** — `_daily_cost_usd()` + kill-switch `GAS_DAILY_TOKEN_BUDGET` in `run_turn`. Misura costi 24h dal log JSONL locale, blocca se superato, fail-safe §9 (log assente → 0.0). La cascata cheap-by-default (Gemini Flash Lite prima per task semplici) era già presente. `gas tokens` già presente. Soluzione definitiva: MISURARE ✅ + routing cheap ✅ + cap giornaliero ✅.
2. ✅ **Accesso telefono — Telegram bridge bot** (`gas telegram`) — `modules/telegram/bot.py`: long polling via urllib stdlib (zero nuove dipendenze), whitelist `TELEGRAM_ALLOWED_IDS` fail-closed, un GasKernel condiviso per uso single-user/Jarvis. Avvio: `export TELEGRAM_BOT_TOKEN=<token> TELEGRAM_ALLOWED_IDS=<chat_id> && gas telegram`. Prerequisito VPS per h24 (FASE 5) ma il codice è pronto al deploy.
3. ✅ **R-wire-1 ri-taratura VEC_MIN_SIM** — `gas calibrate-vectors [N]`: campiona N righe diario come query, mostra distribuzione score coseno, suggerisce valore soglia. Strumento per tarare `GAS_VECTORS_MIN_SIM` sul diario reale VPS. Env-config già implementata (review #28). Il valore 0.30 default rimane fino al deploy reale.
4. ✅ **e5-small evaluation** — `gas eval-vectors [query] [k]`: mostra statistiche vector store (modello, dim, n. vettori, min_sim) e risultati semantici con score. Nota e5-small come alternativa (`GAS_EMBED_MODEL=intfloat/multilingual-e5-small`, stessa infra 384-dim, prefissi già gestiti in `_MODEL_PREFIXES`). Valutazione effettiva avviene a runtime col diario reale.
5. ✅ **R-reidx-3 picco RAM** — Già chiuso (review #30, 2026-06-25): `ricostruisci_da_diario` usa batch paginati (`diario_dopo`, `REINDEX_BATCH_SIZE=256`), numpy transitori per batch (~400KB), accumulo blob ~1.5KB/riga. Su VPS CX33 8GB non bloccante.

### 🟡 PROSSIMI PASSI (in ordine di priorità)

1. ✅ **Migrazione rung Groq** — `llama-3.3-70b-versatile` → `openai/gpt-oss-120b`. Validazione live OK (STATUS 200, tool_calls parsate, `reasoning_effort: "low"`, latenza 1138ms). Commit `f028e51`, review #44 APPROVATO CON RISERVE, 2026-07-08. **COMPLETATA**.
2. ✅ **FASE 2.5 — Summarizzazione cronologia** — CHIUSA (2026-06-27, review #39, commit 65c4c7b).
3. **FASE 3 — Interfaccia vocale: Whisper (STT) e successive** (vedi sotto).
4. **FASE 4.5 — Task scheduler autonomo** (prerequisito Jarvis reale; vedi sotto).
5. **FASE 5 — Deploy VPS Hetzner** — 🟡 IN CORSO (S1 ✅ 2026-07-04, S1b ✅ 2026-07-04, prossimo S2). Include: attivare `gas telegram` come daemon, backup off-machine, process management systemd, ri-tarare `VEC_MIN_SIM` col diario reale (`gas calibrate-vectors`).
6. **Riserve aperte dalla review #38**: R-tel-budget-perf (scan JSONL al crescere del log), R-tel-tool_res (cosmetico, tool result nel reply Telegram).
7. **Rung 4 OpenRouter in degrado** — `meta-llama/llama-3.3-70b-instruct:free` soggetto a rate limit upstream crescenti; diversi modelli free-tier OpenRouter hanno perso l'accesso gratuito a giugno 2026. Da investigare: modello free alternativo stabile o declassare rung 4 a best-effort dichiarato. Stato: APERTO, priorità media.
8. ✅ **Config-drift stringhe modello** — `brains/model_ids.py` = fonte unica dei 5 ID cascata, env-overridabili (`GAS_MODEL_*`). Merge `eb0509f`, commit `160543a`, review #43, 2026-07-07. **CHIUSO**.

> Chiusi di recente (storico): **R-crm-norm-2** — esporre `collisione_chiave_norm`/corruzione in `gas doctor` sez.8 → ✅ FATTO (2026-06-20, review #27, commit `56a6dc3`). **R-reidx-deps** — requirements.txt pinnato == (openai 2.43.0, requests 2.34.2, numpy 2.4.6, onnxruntime 1.27.0, fastembed 0.8.0); requests era il diretto mancante; coppia numpy/onnxruntime pinnata insieme (ABI numpy 2.x); wheel manylinux x86_64 verificate (pip download, zero build) → ✅ CHIUSO (2026-06-29, commit `011f0e6`). **R-vec-3** → 🟡 RIDOTTO (2026-06-29): wheel x86_64 confermate; resta import+embedding a runtime sul CX33 (FASE 5).

### Deprecazioni provider

- ✅ 2026-07-08 — Groq llama-3.3-70b-versatile → openai/gpt-oss-120b: **COMPLETATA**. Commit `f028e51`, review #44 APPROVATO CON RISERVE, validazione live OK (STATUS 200, tool_calls parsate, `reasoning_effort: "low"`). R-groq-slash e R-groq-dup CHIUSI. $0.15/$0.60 per MTok.
- ⚠️ 2026-07-17 — Groq qwen/qwen3-32b in pensione (solo 10 gg dalla scoperta — non usato in GAS; annotato per memoria).

### 🧭 DECISIONI CASCATA PROVIDER — registrate 2026-07-07 (decisioni umane)

**a) ~~DECISO~~ -> SCARTATO/NO-GO — Cerebras `zai-glm-4.7` come rung-4** (sonda live 2026-07-13). Cap contesto free tier = 8192 token (doc ufficiale dichiara 64k, falsa) + coda free satura (429 queue_exceeded). Entrambi bloccanti per paracadute h24. Dettaglio integrale in `reports/stato_progetto.md` § Cerebras zai-glm-4.7 free — SCARTATO come rung-4 (2026-07-13).

**b) CANDIDATO — Rung Mistral API** (tier free "Experiment", ~1B token/mese da fonte terza, limiti esatti da leggere in Admin Console). Fetta SEPARATA, solo DOPO che il rung Cerebras è wired e validato. Stessi gate: sonda limiti reali + round-trip tool-call.

**TRIGGER DATI** (vale per TUTTA la cascata, evento non data): prima che dati di persone reali (lead veri) entrino in diario/CRM → rivedere la policy dati di tutti i provider free (i tier gratuiti possono usare i prompt per training, Gemini e Mistral inclusi) e decidere upgrade a tier no-training.

**c) DECISIONI REGISTRATE 2026-07-07:**
- (i) NO all'espansione della cascata oltre ~6 rung (latenza fallthrough, superficie manutenzione, esaurimento correlato, qualità tool-calling imprevedibile, ToS/dati).
- (ii) NO GitHub Models come rung runtime: tier dichiaratamente di prototipazione (~50 req/giorno high-tier, cap 8K in/4K out, concorrenza 2) + token GitHub sul VPS coabitato col bot trading = superficie credenziali inaccettabile; uso consentito solo come playground dev per confronto modelli.
- (iii) OpenRouter sblocco $10 (50→1000 req/giorno) valutato e RINVIATO ("non ora, GAS non è pronto") — reversibile, azione da console, zero codice.
- (iv) Rung premium futuro = Claude API budget-cappata via GAS_DAILY_TOKEN_BUDGET (Haiku 4.5 $1/$5 MTok riferimento 2026-07-07), distinto da Claude Code che resta SOLO agente di sviluppo.

### 🌉 Ponte GAS↔Claude Code human-gated (Telegram) — NUOVO ITEM (2026-07-07)

Prerequisito: FASE 5 stabile. Nessun impegno di data.

Flusso: GAS genera una proposta come FILE strutturato (titolo,
motivazione, scope, file stimati) → notifica Telegram con ID univoco →
approvazione umana esplicita `/approva <id>` da chat whitelistata →
listener lato DEV (PC/WSL, MAI sul VPS) preleva la proposta approvata e
la passa a Claude Code con gli STOP gate standard → branch, mai main →
report canonico → review umana.
Vincoli di sicurezza (non negoziabili):
1. Direzione della fiducia: il VPS non ottiene MAI credenziali del PC
   dev. Il listener dev fa PULL delle proposte; niente viene mai pushato
   dal VPS verso il PC. No SSH VPS→PC.
2. Bot Telegram SEPARATO dal bot runtime GAS (token e chat diversi):
   compromettere il bot runtime non deve aprire il canale di comando dev.
3. Comandi whitelistati: solo `/approva <id>` e `/rifiuta <id>`. MAI
   testo libero inoltrato a Claude Code — il testo libero è la
   superficie RCE.
4. Approvazione informata: la proposta è un file leggibile prima di
   approvare, non un riassunto.
5. ID monouso + scadenza (es. 24h) contro replay.
6. Rate limit proposte (es. max 3/giorno): GAS non può spammare il
   budget dev.
7. Due budget: Claude Code resta su Sonnet default con cap per proposta;
   budget dev e runtime mai confusi.
8. Audit nel diario: ogni proposta e decisione loggata (la memoria non
   deve mentire).
Aperto da risolvere in fase di design: il ponte funziona solo a PC
acceso; alternativa coda persistente + Claude Code cloud ha confini duri
già accertati (no bwrap nel cloud, push solo su branch di sessione).

### ✅ FASE 2.5 — Summarizzazione Cronologia — CHIUSA (2026-06-27, review #39, commit 65c4c7b)

`_compress_history_if_needed()` auto-trigger in `run_turn`; `gas compress-history` CLI. Env: `GAS_HISTORY_MAX_MSGS` (default 100), `GAS_HISTORY_KEEP_MSGS` (default 20). Zero token LLM. Test T54 copre il caso degenere no-user (R-comp-1, review #40, commit cde4d94).

Per memoria storica — design originale implementato:
- **Trigger:** quando la storia supera N messaggi, Gas condensa la parte più vecchia in un "blocco riassunto" testuale.
- **Destinazione:** il riassunto finisce nel system prompt + una riga nel diario (recuperabile via FTS/semantico). Il file `.gas_history.json` si resetta alla finestra recente.
- **Fail-safe §9:** se la summarizzazione fallisce, storia tronca via `_get_window()` — niente crash, degrado silenzioso.
- **Modello preferito:** Gemini Flash (context lungo, basso costo); Claude solo in fallback.

---

### 🎙️ FASE 3 — Interfaccia Vocale (Priorità Media — Core Feature)
- Whisper (STT) per ricevere comandi vocali diretti (input terminale a mani libere durante lo sviluppo).
- ElevenLabs (TTS) per far rispondere GAS a voce alta come un vero assistente personale.

### 📈 FASE 4 — Moduli di Business (Priorità Media)
- Modulo Meta Ads e automazione della lead generation.
- Algoritmi di persuasione locali per il copy e i DM di marketing.

### 🤖 FASE 4.5 — Task Scheduler Autonomo (Prerequisito Jarvis reale)

Senza questa fase il VPS è solo remote hosting: Gas risponde ma non *agisce* di notte. Prerequisito logico al deploy h24.

- **Catalogo task autonomi:** lista configurabile di intenzioni che Gas esegue su schedule (es. "rassegna stampa lead dal diario", "follow-up DM scaduti da CRM", "report giornaliero token + stato contatti"). Il catalogo è un file YAML/JSON (non codice hard-coded) — l'utente può aggiungere task senza toccare il motore.
- **Loop scheduler:** cron interno (o systemd timer) che a orari configurabili istanzia `GasKernel`, esegue il task dalla lista, salva il risultato nel diario, chiude. Ogni run è atomico e indipendente — un fallimento non blocca il prossimo.
- **Fail-safe §9:** se un task crasha, il loop lo logga in `gas_debug.log`, salta al prossimo, NON va in loop infinito (cap 10 iterazioni già presente).
- **Convergenza col bridge Telegram (item #2):** il bot può triggerare task dal telefono + ricevere l'output — stessa infrastruttura.
- **Dipendenze:** FASE 2.5 (storia non infinita) + FASE 5 (process management) — va implementata insieme al deploy.

---

### 🟡 FASE 5 — Autonomia Totale & VPS — IN CORSO (S1 ✅ 2026-07-04, S1b ✅ 2026-07-04, prossimo S2)
- Migrazione/deploy su **VPS Hetzner** (target indicato dall'utente) h24 con trigger temporali (cron-job) per far lavorare Jarvis di notte a computer spento.
- Backup OFF-MACHINE della memoria (copia di `.gas_memory.db` su volume/host esterno) — vera protezione anti-disastro disco, banale perché il DB è un file singolo.
- Automazione canali brand.
- **Taratura MemoryHigh/MemoryMax di gas.service su misura RAM reale a regime** (GAS + embedder singolo modello). Valori attuali 1500M/2000M conservativi, mai misurati (vedi nota 9 stato_progetto.md: misura "non registrato"). Da eseguire sul VPS insieme a R-wire-1 (VEC_MIN_SIM).
- **Process management + self-healing:** systemd unit con `Restart=always` + `RestartSec=10` per sopravvivere ai crash notturni senza presidio. Alert Telegram se Gas non risponde da N minuti (watchdog). Convergenza col bridge bot (item #2): stessa infrastruttura per notifiche push e comandi da telefono. Senza questo, un crash alle 3am blocca Jarvis fino al mattino.

- **Indagine latenza risposte GAS** (non urgente, segnalato 2026-07-07) — risposte ~5s più lente del solito. Possibili cause da verificare: migrazione a `openai/gpt-oss-120b` su Groq (TTFT diverso), burst TPM 8K → fallthrough OpenRouter (~28s), latenza rete VPS. Da misurare: confronto TTFT `gpt-oss-120b` vs `llama-3.3-70b-versatile` in condizioni analoghe; timing fallthrough registrato nel log (`gas_debug.log`).

### 💡 Idee da valutare (NON prioritarie)

- **Telegram dual-control: GAS + Claude Code insieme** — Il bot `gas telegram` esiste già (FASE 2, item #2). Il passo successivo è espandere il bridge in modo che dal telefono si possano inviare comandi sia a GAS runtime (già funzionante) sia a Claude Code (sessione di sviluppo): es. "controlla CI", "scrivi feature X", "dimmi lo stato del progetto". I due agenti si coordinano: GAS risponde sullo stato runtime, Claude Code agisce sul codice. Architettura da definire (webhook condiviso vs. due bot distinti vs. un orchestratore GAS che inltra a CC). Prerequisito: VPS h24 (FASE 5) per tenere tutto sempre attivo. Dipende da bridge Claude Code → canale Telegram (da esplorare: Claude Code CLI in background su VPS con stdin/stdout rediretto al bot).

- **Video learning — GAS studia e apprende da video** — Capacità di "leggere" un video (YouTube URL o file locale): trascrizione automatica (Whisper STT già in roadmap FASE 3, o API Gemini multimodale che accetta video direttamente), estrazione di concetti chiave, salvataggio compresso nel diario SQLite (memoria long-term FASE 2). GAS può poi rispondere a domande basandosi sui video studiati via FTS/semantico. Use case: studiare webinar di marketing, tutorial tecnici, content dei competitor. Da valutare: Gemini 1.5/2.0 con context video nativo vs. pipeline Whisper + LLM testuale (tradeoff costo/qualità). Convergenza naturale con FASE 3 (Whisper già pianificato) e FASE 2 (memoria già presente).

- Valutare utilizzo o integrazione openclaw (agente IA esterno). NB: prima verificare licenza, dipendenze, qualità e superficie di sicurezza; mai copia-incolla nel motore. Idea parcheggiata, nessun impegno.

### 🗣️ DA DISCUTERE (delta da roadmap alternativa — da valutare se/quando fare)
- **`gas --brain <name>`** — flag CLI esplicito per scegliere il brain sul singolo comando (es. `gas --brain gemini "analizza log"`), con ruoli distinti: Claude = Architetto (strategia/approvazione), Gemini = Memoria (contesti fino a 1-2M token), DeepSeek = Operaio (alta frequenza, basso costo). Oggi la cascata è automatica; questo aggiunge controllo umano diretto.
- **DeepSeek V4 Flash come operaio di default** — alternativa/complemento a Groq per task ad alta frequenza ($0.14 input / $0.28 output per M token + context caching aggressivo). Da valutare rispetto a Groq già integrato: se vale la complessità di un provider in più.
- **"Il Consiglio" — dettaglio implementativo** (espansione della voce già parcheggiata): invocazione automatica dopo N fallimenti di test consecutivi (blocco loop cieco per risparmiare token); sotto-agenti specializzati low-cost (Contrarian del Cloud, First-Principles Thinker, L'Esecutore) che dibattono su DeepSeek V4 Flash; sintesi del log passata a Claude (The Chairman) per verdetto e patch finale. Da discutere: N soglia, costo del consiglio vs costo del loop cieco, integrazione col revisore.
- **`revisore.md` modulare** — scomposizione del profilo del revisore in micro-profili caricati dinamicamente da Gas a seconda del task (es. "review sicurezza", "review CRM", "review memoria"). Obiettivo: abbattere i token fissi iniettati a ogni chiamata. Da valutare impatto reale vs complessità di gestione.
- **Notifiche push sullo smartphone** per monitorare i deploy e i run sul VPS (es. alert se Gas crasha, se la CI diventa rossa, se un job notturno finisce). Da valutare insieme al bridge bot Telegram (già in item #2) — potrebbero essere la stessa cosa.
- **Accesso dev tooling da telefono — Claude Dispatch (candidato).** Soluzione candidata: Claude Dispatch (funzione ufficiale Anthropic in Cowork/Claude Code, lanciata 2026-03-17): pairing QR telefono↔desktop, thread persistente, i task di sviluppo partono come sessioni Claude Code che ereditano CLAUDE.md. Stato: IN VALIDAZIONE — sonda pendente (pairing, task doc-only da telefono, verifica: ambiente Windows vs WSL, hook review_gate/session_end scattati, modello usato). Vincolo: PC acceso e app desktop aperta. Regole di sicurezza vincolanti: modalità 'chiedi prima di agire', accesso SOLO alla cartella repo, computer use OFF, mai pre-autorizzare azioni (il PC dev detiene la chiave SSH della VPS di produzione).
- **Controllo Telegram unificato (ridimensionato).** SUPERATO PER METÀ da Dispatch: il canale tu→Claude Code da telefono lo copre Dispatch (ufficiale, niente bridge custom = niente superficie RCE da costruire e mantenere). Resta valido SOLO il canale GAS→Claude Code human-gated (la VPS propone, l'umano approva via /approva): Dispatch non lo copre — la spec di sicurezza è l'item "🌉 Ponte GAS↔Claude Code human-gated (Telegram)" sopra (listener pull-only, ID monouso 24h, whitelist comandi, max 3 proposte/giorno, audit log). Trade-off accettato: GAS si comanda da Telegram, lo sviluppo dall'app Claude. NB: ridimensiona anche l'idea "Telegram dual-control" in 💡 Idee da valutare (il canale telefono→CC lo coprirebbe Dispatch).

### 🅿️ PARK (parcheggiati — nessun impegno, da rivalutare al momento giusto)
- **Mirage (strukto-ai/mirage) — VFS unificato per AI agents**: valutare a FASE 4 (integrazioni marketing multi-servizio) come alternativa a N SDK separati. Progetto nato 2026-05-06, ~3.3k stelle a luglio 2026, open source, SDK Python in-process (shell bash custom, no subshell host, vede solo i mount). Condizioni vincolanti se mai adottato: mount READ-ONLY + allowlist risorse, MAI write verso cloud in autopilot, incompatibile con coabitazione bot trading (superficie esfiltrazione). Fonte: reel + verifica web 2026-07-08.
- **Claude Cowork**: agente desktop per knowledge work (file locali, report, slide). Non tocca il motore (che passa da Claude Code + revisore + hook). Rivalutare a FASE 4 per materiale marketing e pipeline video-ingestion locale (trascrizione→analisi→nota markdown).
