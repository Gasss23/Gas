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
- Le quattro istituzioni di processo (A/B/C attive dal 2026-06-11, D dal 2026-06-23):
  - A) reports/stato_progetto.md — fotografia viva dello stato del progetto (motore, finding aperti, prossimi passi). Va aggiornata a fine di ogni task.
  - B) reports/diff_sessione.md — a fine sessione, riepilogo del diff della sessione: file toccati, cosa è cambiato e perché. Si riscrive a ogni sessione (fotografia dell'ultima sessione, la storia completa sta in git).
  - C) Subagent revisore (.claude/agents/revisore.md) — revisiona ogni modifica al motore prima del commit, per correttezza tecnica E coerenza col progetto. PRIMA di ogni review legge obbligatoriamente CLAUDE.md (sez. 5), reports/stato_progetto.md e la sua memoria persistente .claude/agents/memoria_revisore.md; DOPO ogni review aggiunge a quella memoria le eventuali lezioni nuove (1-3 righe, datate).
  - D) reports/handoff.md — a fine sessione Claude Code produce questo dossier autocontenuto secondo il template, in quest'ordine: §DECISIONI UMANE RICHIESTE in cima, esito della sonda, `git diff --stat` REALE della sessione, `git log` dei commit della sessione, delta test del motore, verdetto INTEGRALE del revisore (incollato, NON riassunto), stato/esito dell'ultima run CI (FETTA 1, .github/workflows/ci.yml). NON sostituisce reports/ultimo_report.md (che resta la fonte di verità del singolo task): l'handoff lo AGGREGA per la revisione e ci aggiunge lo stato CI. Si riscrive a ogni sessione (la storia completa sta in git).

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

## 11. DISCIPLINA TOKEN (attiva dal 2026-06-23)

Spesa rilevata 20€ in 2 giorni (22–23 giu 2026): 100% costo di sviluppo Claude Code su Opus 4.8, GAS runtime = 0€.

- **Modello**: default Sonnet 4.6 (esecuzione). Opus SOLO on-demand via `/model opus` per strategia/architettura — mai automatico.
- **`/clear`** tra task non correlati per non trascinare contesto inutile.
- **Non ri-leggere file grandi senza motivo**: preferire Read mirato con offset/limit, o Grep. In particolare `reports/stato_progetto.md` va letto selettivamente (Grep per la sezione che serve).
- **Tenere `stato_progetto.md` snello** (~100 righe): lo storico va in `reports/stato_storico.md`. NON spostare storico nell'attivo.
- **Monitoraggio**: `/cost` in sessione; console Anthropic → Usage per vedere il breakdown per modello.

## 10. ROADMAP — SOMMARIO

- FASE 1 — Blindatura & Sicurezza — ✅ CHIUSA (sandbox bwrap, WINDOW_CHAR_CAP, snapshot)
- FASE 2 — Cervello & Memoria Low-Cost — ✅ CHIUSA (SQLite diario+CRM, FTS5, vector store, backup)
- FASE 2.5 — Summarizzazione cronologia (compressione .gas_history.json h24) — futura
- FASE 3 — Interfaccia Vocale (Whisper STT + ElevenLabs TTS) — futura
- FASE 4 — Moduli di Business (Meta Ads, lead gen) — futura
- FASE 5 — Deploy VPS Hetzner h24 + backup off-machine + process management (systemd + self-healing) — futura

**Item aperti TOP:**
1. 🔴 Controllo spesa token (DIAGNOSI: sviluppo vs runtime, cap giornaliero, routing cheap-by-default)
2. 📱 Accesso Claude Code da telefono (claude.ai/code, bridge bot Telegram, SSH tmux)
3. R-wire-1 residuo: ri-taratura VEC_MIN_SIM su diario reale VPS (env già configurabile)
4. 🤖 Task scheduler autonomo (catalogo task notturni — prerequisito Jarvis reale su VPS)

Dettaglio completo, completati storici e priorità: reports/roadmap.md
