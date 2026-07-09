# REPORT — 2026-07-09 — TASK DOC-ONLY: registrazione decisioni sessione 2026-07-07

## DECISIONI UMANE RICHIESTE

Nessuna bloccante. Tre proposte di allineamento doc NON eseguite perché fuori
dall'elenco del task (vedi §Proposte, non committate — decisione umana se farle).

---

## Scope rispettato

Task doc-only: toccati SOLO `reports/stato_progetto.md`, `reports/roadmap.md`,
`reports/ultimo_report.md`. NESSUN file di motore (gas.py, brains/, modules/,
tests/ intatti). Nessuna review revisore richiesta (commit doc-only). Push
diretto su `main` (policy doc-only autorizzata nel task).

## Esito per punto

### 1) reports/stato_progetto.md
- **1a `FATTA`** — Registrato il merge su main di `refactor/model-ids-fonte-unica`
  (merge `eb0509f`, commit `160543a`): item roadmap "config-drift stringhe
  modello" **CHIUSO**. `brains/model_ids.py` = fonte unica dei 5 ID cascata,
  env-overridabili (`GAS_MODEL_*`). Suite 217 PASS incluso T56.
  **Contatore review letto dai canonici, non assunto**: `.claude/agents/memoria_revisore.md`
  registra la review model_ids come **#43** (2026-07-07) e l'ultima come **#44**
  (gpt-oss-120b, 2026-07-08) → contatore corretto a **44 review** nello "Stato
  motore" (il valore precedente "42" era stale; la sezione Istituzioni diceva
  già 44, ora coerenti).
- **1b `FATTA`** — Nuovo finding 🟡 **R-legacy-slice** (riserva #1 revisore,
  review #43 model_ids): `brains/claude_brain.py:38` contiene
  `for m in messages[-8:]` — slicing raw della history, violazione sez. 5
  CLAUDE.md. Oggi INERTE (file legacy non wired al kernel attivo, zero
  copertura test); diventa bloccante se i brain legacy venissero ri-agganciati.
  Debito tecnico latente, nessuna azione ora.
- **1c `FATTA`** — Caveat suite registrato: i 217 PASS della sessione model_ids
  sono stati ottenuti in Codespace, dove i test bwrap NON sono validabili
  (comportamento noto); verifica bwrap reale demandata a CI/postazione WSL locale.
- **1d `FATTA`** — Run CI del merge letto dall'API GitHub Actions REALE (non
  stimato): **run ID 28874912495**, run n. 85, evento push su `eb0509f`
  ("Merge branch 'refactor/model-ids-fonte-unica'"), 2026-07-07T14:41:10Z,
  esito **SUCCESS** ✅. Registrato in stato_progetto accanto alla chiusura
  dell'item.

### 2) reports/roadmap.md
Aggiunta sezione **"🧭 DECISIONI CASCATA PROVIDER — registrate 2026-07-07"**:
- **2a `FATTA`** — DECISO: nuovo rung 4 Cerebras `zai-glm-4.7` (free tier 5 RPM,
  30K TPM, 1M token/giorno, doc ufficiale verificata 2026-07-07); entra PRIMA
  di OpenRouter (→ rung 5), Ollama → 6. DUE GATE BLOCCANTI pre-wiring:
  Gate 1 sonda live contesto (possibile cap 8.192 token da fonti terze, prova
  con prompt >9K; se reale → design da rifare, piano B gpt-oss-120b su
  Cerebras); Gate 2 round-trip tool-call con `disable_reasoning: true` dal
  giorno zero + parsing tool_call incluso id duplicati. Motivazione: OpenRouter
  in degrado + NO sblocco $10 → Cerebras è la mitigazione principale.
- **2b `FATTA`** — CANDIDATO: rung Mistral API (free "Experiment", ~1B
  token/mese da fonte terza, limiti da Admin Console), fetta SEPARATA solo dopo
  Cerebras wired+validato, stessi gate. Registrato anche il **TRIGGER DATI**
  (evento, non data): prima che lead veri entrino in diario/CRM → rivedere
  policy dati di TUTTI i provider free e decidere upgrade a tier no-training.
- **2c `FATTA`** — Decisioni registrate 2026-07-07: (i) NO cascata oltre ~6
  rung; (ii) NO GitHub Models come rung runtime (solo playground dev);
  (iii) OpenRouter sblocco $10 RINVIATO ("non ora, GAS non è pronto",
  reversibile da console, zero codice); (iv) rung premium futuro = Claude API
  budget-cappata via GAS_DAILY_TOKEN_BUDGET (Haiku 4.5 $1/$5 MTok rif.
  2026-07-07), distinto da Claude Code (solo agente di sviluppo).
- **2d `FATTA`** — Nuovo item **"🌉 Ponte GAS↔Claude Code human-gated
  (Telegram)"**: testo riportato INTEGRALE come da task (flusso proposta-file →
  Telegram → `/approva <id>` → listener lato DEV → branch mai main → report →
  review umana; 8 vincoli di sicurezza non negoziabili; aperto del PC acceso /
  alternativa cloud con confini duri). Prerequisito FASE 5 stabile, nessuna data.

### 3) Sezione "Pipeline provider" di stato_progetto.md
`NON TOCCATA`, come da istruzione. **Nota di realtà**: il presupposto del task
("migrazione Groq non ancora mergiata") è superato dai fatti — la migrazione è
stata mergiata su main il 2026-07-08 (commit `f028e51`, review #44, validazione
live OK) e la sezione Pipeline su main riflette GIÀ `groq/openai/gpt-oss-120b`.
Quindi la sezione riflette lo stato reale senza intervento. Cerebras
correttamente NON presente (non wired): le decisioni vivono in roadmap, la
realtà in stato.

## Proposte (NON committate — mi sono fermato come da istruzione)

Incoerenze residue trovate durante il task, fuori dall'elenco, da valutare in
un task futuro:
1. `reports/roadmap.md` §PROSSIMI PASSI item 8 "Config-drift stringhe modello"
   risulta ancora "APERTO" — ora è chiuso (merge `eb0509f`); andrebbe marcato ✅.
2. `reports/roadmap.md` §PROSSIMI PASSI item 1 "Migrazione rung Groq …
   validazione live: PENDING" è stale — completata 2026-07-08 (`f028e51`,
   review #44); idem il primo bullet di §Deprecazioni provider ("PENDING").
3. `reports/stato_progetto.md` riga "CI GitHub Actions: run #28665577327 su
   `51f9e1e`" nello Stato motore è più vecchia dei run recenti su main (ultimo:
   #28967120717 su `9187804`, SUCCESS) — non elencata nel task, non toccata.

## Note

- Base del commit: `origin/main` a `9187804` (branch di sessione
  `claude/phone-gas-development-10svqc` NON usato: contiene una linea divergente
  della migrazione Groq, superata dal merge reale su main).
- Zero token LLM runtime consumati; run CI letto via API GitHub (metadati).
