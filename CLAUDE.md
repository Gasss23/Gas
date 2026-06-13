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
- Gate di review OBBLIGATORIO (attivo dal 2026-06-13): PRIMA di ogni `git commit` il cui diff staged tocca gas.py, brains/, modules/ o tests/, l'agente principale DEVE invocare il subagent `revisore` sul diff e attendere il verdetto. Commit consentito solo se APPROVATO o APPROVATO CON RISERVE (riserve tracciate in stato_progetto.md). Commit di soli reports/ o doc (CLAUDE.md, *.md) NON richiedono review. Questa regola e' la barriera PRIMARIA; il hook deterministico PreToolUse (`.claude/hooks/review_gate.sh`, marcatore `.claude/.review_ok`) e' la rete di sicurezza, best-effort, non un sostituto. Mai bypassare via auto-commit: l'hook SessionEnd committa SOLO reports/doc/.gas_history.json, mai il motore.
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

## 7. TESTING & VERIFICATION REQUIREMENTS
- Ogni modifica al motore richiede un test di round-trip agentico per verificare che il ciclo non si interrompa dopo la prima tool call.
- Validazione obbligatoria tramite esecuzione diretta prima di considerare un bug come "risolto".

## 8. API & EXTERNAL SERVICE GUARDRAILS
- Agentic Loop Cap: La funzione run_turn deve implementare un ciclo while blindato da un massimo di 10 iterazioni (for _ in range(10)) come barriera anti-loop infinito per preservare il budget delle API.
- Model Awareness: Il sistema deve monitorare e dichiarare all'utente i cambi di efficienza o i passaggi a versioni minori (es. Gemini Flash-lite).

## 9. SECURITY & ERROR HANDLING
- Ogni eccezione nei provider deve essere intercettata, loggata come logging.warning nella "scatola nera" (gas_debug.log), attivando immediatamente il fallback sul brain successivo senza far crashare il programma.

## 10. FUTURE ROADMAP & PRIORITIES

Completati (storico): snapshot preventivo anti-autodistruzione (2026-06-11), comando gas doctor, sandbox di run_command no-shell+allowlist con modalita dry-run (2026-06-12, finding esfiltrazione 🟠->🟡 ridotto).

### 🔴 FASE 1 — Blindatura del Terminale & Sicurezza (Priorità Alta)
- Snapshot preventivo anti-autodistruzione — ✅ FATTO (2026-06-11), base della blindatura.
- Sandbox OS per run_command (bwrap/unshare: namespace di rete chiuso + filesystem read-only) — chiude DEL TUTTO il finding esfiltrazione, oggi solo ridotto. Da decidere all'avvio: fail-closed duro vs fallback sul sandbox applicativo se l'ambiente non supporta i namespace. Aggiungere check di disponibilita in gas doctor. NB: verificare PRIMA cosa offre l'ambiente (Codespace e un container, bwrap potrebbe non avere i privilegi) e solo dopo progettare.
- WINDOW_CHAR_CAP sulla finestra, a granularita di messaggio (mai slicing) — blocca lo spreco di token nei messaggi; rimedio proposto in review #1.
- (collegato) Manutenzione snapshot in gas doctor: conteggio ref, gc degli oggetti orfani, rotazione di reports/snapshots.log (riserve R2/R3 review #3).

### 🧠 FASE 2 — Il Cervello di Jarvis & Memoria Low-Cost (Priorità Alta)
- Database locale SQLite per la memorizzazione dei fatti rigidi (gratis, zero token).
- Vector DB locale per i ricordi a lungo termine senza consumo di token di contesto.
- Script revisor.py (API low-cost) per sbloccare il "Claude Council" senza spendere ~10€/giorno. NB: chiarire all'avvio cosa si intende per "Claude Council" — il nome non corrisponde a un prodotto Anthropic noto al 2026-06-13.

### 🎙️ FASE 3 — Interfaccia Vocale (Priorità Media — Core Feature)
- Whisper (STT) per ricevere comandi vocali diretti (input terminale a mani libere durante lo sviluppo).
- ElevenLabs (TTS) per far rispondere GAS a voce alta come un vero assistente personale.

### 📈 FASE 4 — Moduli di Business (Priorità Media)
- Modulo Meta Ads e automazione della lead generation.
- Algoritmi di persuasione locali per il copy e i DM di marketing.

### 🚀 FASE 5 — Autonomia Totale & VPS (Priorità Lunga)
- Deploy su VPS h24 con trigger temporali (cron-job) per far lavorare Jarvis di notte a computer spento.
- Automazione canali brand.
