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
- Alta: Snapshot preventivo dei file (anti-autodistruzione), comando gas doctor, modalità dry-run.
- Media: Integrazione ElevenLabs (Voce), Modulo Meta Ads, Ragionamento avanzato (o1/DeepSeek), Wrapper vocale per Claude Code (Whisper STT → input terminale + TTS per output) per dare comandi a mani libere durante lo sviluppo.
- Lunga: Deploy VPS h24, automazione canali brand.
