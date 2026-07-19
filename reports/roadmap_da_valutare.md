# Roadmap Extra — DA VALUTARE (post roadmap principale)

> **Stato: IN ATTESA** — Da valutare SOLO a completamento della roadmap principale (`reports/roadmap.md`).
> I punti verranno filtrati: quelli compatibili con Gas verranno integrati nella roadmap principale,
> il resto scartato. Nessun item qui va in sviluppo prima di quella revisione.
> Fonte: documento "Blueprint Supremo" ricevuto 2026-07-19.

---

## Fase 1 — Fondamenta, Infrastruttura Core & Telemetria

**Obiettivo:** Scheletro operativo stabile, leggero, asincrono, protetto finanziariamente e monitorato in tempo reale.

- **Architettura Dual-Brain (multi-agente):** Brain principale su DeepSeek R1/V3 per ragionamento complesso; brain secondario Gemini per elaborazioni creative veloci; micro-agenti specializzati ed effimeri coordinati dal core.
- **Deployment containerizzato:** Docker su VPS Hetzner CX33/CX22 con NVMe per isolamento microservizi.
- **Financial Router & Token Budgeting:** Demone isolato che tronca connessioni al superamento soglia; monitoraggio costi API in tempo reale; blocco rigido giornaliero; switch dinamico modelli (commerciali per ragionamento, open-source/cinesi a costo zero per routine).
- **Scratchpad Dinamico (RAM di Stato):** File di stato persistente (`state.json` o Markdown) con roadmap attiva, micro-task del giorno, preferenze utente — letto e sovrascritto istantaneamente dall'agente.
- **Auto-Telemetria Infrastrutturale:** Monitoraggio CPU/RAM/NVMe prima di micro-training o calcoli pesanti per prevenire crash server.

---

## Fase 2 — Memoria Ibrida, Relazionale e Infinita

**Obiettivo:** Superare il limite del contesto volatile. Memoria sconfinata, strutturata, cifrata, disaccoppiata.

- **Short-Term Memory (STM):** Redis in-memory per dati caldi, sessione corrente, informazioni degli ultimi 10-20 minuti.
- **Long-Term Memory (LTM) Vettoriale:** pgvector su PostgreSQL locale (o ChromaDB/Faiss) per indicizzazione semantica e abbattimento consumo token.
- **Topologia "Comodino" isolata:** Ogni sub-agente gestisce una cache locale privata per i suoi task specifici — elimina la contaminazione di contesto tra moduli (es. marketing vs programmazione).
- **Disaccoppiamento Storage (Cloudflare R2 / S3-Compatible):** Log d'archivio, file pesanti e checkpoint LoRA su Object Storage esterno illimitato con zero costi di download. VPS rimane scarica.
- **GraphRAG (Knowledge Graph):** Integrazione NetworkX o Neo4j leggero per mappare concetti come nodi e archi logici — elimina la confusione temporale.
- **Modulo "Doganiere" (I/O Gateway):** Sanificazione degli input (dump corsi, scraping, codice) — estrae fatti crudi e scarta rumore prima del processamento.
- **Hybrid Search Engine:** Algoritmo proprietario che combina ricerca semantica (vettori) e ricerca esatta/temporale (keyword).

---

## Fase 3 — Integrazione Mirage & Virtual File System

**Obiettivo:** Virtualizzare lo storage cloud e abilitare operazioni polimorfiche sul file system.

- **Unified Virtual File System (Mirage / strukto-ai):** Storage cloud (R2, S3, Drive, Google Bucket) visto come una singola cartella locale; sync file `.md` verso Obsidian/Anytype in tempo reale.
- **Polymorphic Bash su ogni formato:** Comandi di sistema standard (`cat`, `grep`, `head`, `wc`) su file cloud remoti di qualsiasi tipo — inclusi `.parquet`, `.csv`, `.json`, `.mp3`, `.wav`.
- **Pipe Across Systems (Multi-Backend):** Piping in stile Unix tra backend eterogenei (S3, Google Drive, GitHub, Slack, Postgres, Redis) in un unico flusso.
- **Two-Layer Cache Engine:** Cache a due livelli (index + file cache) per lookup istantanei e minimizzazione dei costi di banda.

---

## Fase 4 — Metacognizione & Consolidamento Parametrico (God Mode)

**Obiettivo:** Sfruttare l'inattività del server per analizzare se stesso, distillare conoscenza e apprendere dagli errori.

- **Ciclo "Sleep & Reflect":** Cron job notturno — sub-agente di riflessione analizza i log della giornata e distilla conoscenza.
- **Context Distillation (Global Workspace):** Compressione in tempo reale del flusso di chat per ottimizzare token, mantenendo vivi solo i concetti chiave.
- **Circuito di Feedback Negativo (Veto Learning):** Su correzione/veto dell'utente, analisi post-mortem dell'errore in fase "Sleep" e generazione di un "Tabù Cognitivo" nello Scratchpad — previene la ripetizione dello stesso errore concettuale.
- **Dynamic LoRA Swapping (Memoria Parametrica):** Micro-training locale notturno automatizzato sui log puliti; Gas genera un file LoRA leggero con nuovi pesi neurali e lo carica al risveglio. L'IA non consulta la memoria, *diventa* la memoria.
- **Autogestione dei Prompt:** Gas aggiorna le sue euristiche e riscrive autonomamente i System Prompt integrando nuovi vincoli e preferenze riscontrate.

---

## Fase 5 — Architettura Morfica, Sandbox & Singolarità (Overlord Mode)

**Obiettivo:** Trasformare la memoria da archivio passivo a codice sorgente capace di mutare la struttura del software a runtime.

- **Self-Code Generation & Autocompilazione:** Gas rileva task ripetitivi senza tool dedicato, progetta/scrive/testa script Python funzionanti e li integra nel core runtime in autonomia.
- **IDE Workspace Watcher (VS Code Link):** File-watcher sul workspace — rileva modifiche al codice in tempo reale e invia metadati a Gas in background per azzerare i gap di contesto.
- **Crono-Prefetching Predittivo:** Basandosi su Workspace Watcher e analisi temporale, Gas anticipa le intenzioni del dev e pre-carica in RAM i vettori del task successivo.
- **Calcolo Iperdimensionale (HDC — Memoria Olografica):** Transizione a vettori ultra-ampi (dim > 10.000) in RAM; concetti fusi via operazioni logiche bit-level (XOR): `V_nuovo = V_gas ⊗ V_tg`. Recupero ricordi a livello hardware, latenza zero.
- **Darwinismo Cognitivo (Memory Swarm):** Ogni input genera micro-agenti cognitivi in background che competono via algoritmi genetici; le logiche funzionali si riproducono, i concetti obsoleti vanno in garbage collection evolutiva.
- **Portable Workspace via Mirage:** L'intero stato del workspace si sposta tra host/container come un singolo `.tar`; mini-bot creati da Gas saltano tra macchine senza riavvii.
- **Versioned Snapshot & Rollback:** Gestione workspace in stile Git — istantanee dello stato del codice a ogni step di test nella Sandbox; roll-back temporali e clonazione flussi paralleli su crash critici.

---

## Fase 6 — Moduli Verticali (Marketing UGC & Trading Pilot)

**Obiettivo:** Bracci operativi per generazione di cassa e estrazione dati commerciali.

- **Modulo "De-Boner":** Scarica e trascrive video esterni (Reels, corsi, link); "spolpa" i contenuti estraendo concetti chiave e rielaborandoli per nuove idee di business.
- **UGC Marketing Engine:** Generatore predittivo di script video con copywriting a risposta diretta, pattern interrupt psicologici, trigger per automazioni DM (es. "Commenta SALA").
- **AI Avatar & Virtual Influencer Engine:** Framework per avatar IA e cloni digitali (visivi/vocali) per campagne pubblicitarie automatizzate sui social 24/7 senza presenza fisica.
- **Trading Pilot Core ("Paziente Zero"):** Connessione al canale Telegram dei segnali via Bot API (read-only admin) per intercettare messaggi in tempo reale, eludendo legalmente blocchi copia/inoltro.
- **Regex Parser Module:** Filtro Python puro su espressioni regolari fisse — estrae chirurgicamente Symbol, Action, Entry, Stop Loss e Take Profit dal testo; zero allucinazioni AI.
- **MetaAPI.cloud Execution:** Integrazione con le API cloud MetaAPI per inviare dati estratti al conto MetaTrader 5 (MT5) direttamente da Linux.

---

## Fase 7 — Framework di Sicurezza Immutabile & Governance

**Obiettivo:** Infrastruttura inattaccabile dall'esterno, governata dal controllo umano.

- **Immutabilità del Core (Read-Only):** Kernel di Gas, moduli di cifratura e guardrail in porzione file system protetta senza permessi di scrittura per l'AI.
- **Cifratura Zero-Knowledge a Riposo:** DB vettoriale, storage R2/S3 e grafo delle relazioni cifrati con chiavi locali — indecifrabili in caso di violazione della VPS.
- **Isolamento Sandbox Docker:** Ogni codice o tool generato dall'AI confinato in sandbox isolata dal SO principale; validazione tramite unit test interni prima del deploy.
- **Gateway di Veto Umano (HITL — Human-in-the-Loop):** Modifiche strutturali, nuovi tool stabili e azioni ad alto rischio entrano in produzione solo dopo approvazione esplicita via Telegram. Il rifiuto alimenta il circuito di feedback negativo (Tabù Cognitivo).
- **Git Auto-Commit & Disaster Recovery:** Ogni modifica autorizzata genera un commit su Git; hot-backup notturno crittografato su Cloudflare R2 per ripristino flash totale da zero.
