Roadmap e completati storici di GAS — dettaglio integrale. Sommario e stato corrente in CLAUDE.md e reports/stato_progetto.md.

## 10. FUTURE ROADMAP & PRIORITIES

Completati (storico): snapshot preventivo anti-autodistruzione (2026-06-11), comando gas doctor, sandbox di run_command no-shell+allowlist con modalita dry-run (2026-06-12, finding esfiltrazione 🟠->🟡 ridotto), sandbox OS bwrap (rete isolata + fs read-only, modalita os_strict/os_with_fallback, sonda _probe_os_sandbox + check in gas doctor) — chiude DEL TUTTO il finding esfiltrazione. WINDOW_CHAR_CAP sulla finestra a granularita di messaggio (2026-06-14, review #7/#8) e manutenzione snapshot in gas doctor (2026-06-14, review #10) — **FASE 1 CHIUSA**. **FASE 2 (cervello/memoria low-cost) CHIUSA** (2026-06-15 → 2026-06-19): memoria SQLite con diario IMMUTABILE (review #12/#13), iniezione always-on + tool ricorda (review #14), CRM contatti dal loop con chiavi normalizzate/chiave_norm (review #15/#16/#22), ricerca FTS5 sul diario (review #18), backup automatico anti-corruzione del DB (review #19), vector store fetta 1 storage+embedding (review #23) + wiring retrieval semantico al kernel opt-in GAS_VECTORS (review #24), comando CLI gas reindex (review #25). Soglia semantica `VEC_MIN_SIM` resa env-configurabile via `GAS_VECTORS_MIN_SIM` (2026-06-21, review #28) — chiude la parte azionabile di R-wire-1 (resta solo la ri-taratura, deploy-dependent). **ITEM APERTI CHIUSI TUTTI** (2026-06-27, review #38, commit a8c6d53): budget cap `GAS_DAILY_TOKEN_BUDGET` + Telegram bridge bot `modules/telegram/bot.py` + `gas calibrate-vectors` + `gas eval-vectors` + R-reidx-3 già chiuso (review #30).

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

1. ⚠️ **Migrazione rung Groq (deadline 16 ago 2026):** `llama-3.3-70b-versatile` dismesso. Sostituire con modello Groq attivo (candidato: Qwen3 27B — verificare nome API su console Groq prima del commit).
2. **FASE 2.5 — Summarizzazione cronologia** (prerequisito VPS h24; vedi sotto).
3. **FASE 3 — Interfaccia vocale: Whisper (STT) e successive** (vedi sotto).
4. **FASE 4.5 — Task scheduler autonomo** (prerequisito Jarvis reale; vedi sotto).
5. **FASE 5 — Deploy VPS Hetzner** (vedi sotto). Include: attivare `gas telegram` come daemon, backup off-machine, process management systemd, ri-tarare `VEC_MIN_SIM` col diario reale (`gas calibrate-vectors`).
6. **Riserve aperte dalla review #38**: R-tel-budget-perf (scan JSONL al crescere del log), R-tel-tool_res (cosmetico, tool result nel reply Telegram).

> Chiusi di recente (storico): **R-crm-norm-2** — esporre `collisione_chiave_norm`/corruzione in `gas doctor` sez.8 → ✅ FATTO (2026-06-20, review #27, commit `56a6dc3`). **R-reidx-deps** — requirements.txt pinnato == (openai 2.43.0, requests 2.34.2, numpy 2.4.6, onnxruntime 1.27.0, fastembed 0.8.0); requests era il diretto mancante; coppia numpy/onnxruntime pinnata insieme (ABI numpy 2.x); wheel manylinux x86_64 verificate (pip download, zero build) → ✅ CHIUSO (2026-06-29, commit `011f0e6`). **R-vec-3** → 🟡 RIDOTTO (2026-06-29): wheel x86_64 confermate; resta import+embedding a runtime sul CX33 (FASE 5).

### Deprecazioni provider

- 2026-08-16 — Groq llama-3.3-70b-versatile (rung 3) in pensione: migrare a groq/qwen3-27b (o nome modello Groq ufficiale da verificare al momento della migrazione). Trigger: comunicazione ufficiale Groq. Azione: aggiornare RUNG_3_MODEL in configurazione + test round-trip.

### 🗂️ FASE 2.5 — Summarizzazione Cronologia (Prerequisito VPS h24)

Senza questa fase, `.gas_history.json` cresce indefinitamente h24 sul VPS. `_get_window()` taglia ma non comprime — il contesto esplode in settimane.

- **Trigger:** quando la storia supera N messaggi (es. 200), Gas condensa la parte più vecchia in un "blocco riassunto" testuale.
- **Destinazione:** il riassunto finisce nel system prompt (come estensione del `gas_identity.md`) + una riga nel diario (così è recuperabile via FTS/semantico). Il file `.gas_history.json` si resetta alla finestra recente.
- **Fail-safe §9:** se la summarizzazione fallisce, si mantiene la storia tronca via `_get_window()` — niente crash, degrado silenzioso.
- **Modello preferito:** Gemini Flash (context lungo, basso costo) per la condensazione; Claude solo in fallback.
- **Dipendenze:** nessuna — si inserisce nel kernel come step in `_load_history()` o in `save_history()`.

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

### 🚀 FASE 5 — Autonomia Totale & VPS (Priorità Lunga)
- Migrazione/deploy su **VPS Hetzner** (target indicato dall'utente) h24 con trigger temporali (cron-job) per far lavorare Jarvis di notte a computer spento.
- Backup OFF-MACHINE della memoria (copia di `.gas_memory.db` su volume/host esterno) — vera protezione anti-disastro disco, banale perché il DB è un file singolo.
- Automazione canali brand.
- **Process management + self-healing:** systemd unit con `Restart=always` + `RestartSec=10` per sopravvivere ai crash notturni senza presidio. Alert Telegram se Gas non risponde da N minuti (watchdog). Convergenza col bridge bot (item #2): stessa infrastruttura per notifiche push e comandi da telefono. Senza questo, un crash alle 3am blocca Jarvis fino al mattino.

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
