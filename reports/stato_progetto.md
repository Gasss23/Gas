# STATO PROGETTO GAS

> Fotografia viva dello stato. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-07-13** (Cerebras zai-glm-4.7 — sonda NO-GO; bancato in finding)
> Storico sessioni, dettaglio componenti, finding chiusi: `reports/stato_storico.md`

## Stato motore

FASE 1 âœ…, FASE 2 âœ… e **FASE 2.5** âœ… chiuse. **44 review** completate (contatore da `.claude/agents/memoria_revisore.md`: ultima #44, 2026-07-08). Suite (locale WSL bwrap, sonda 2026-07-03): **214 PASS, 0 FAIL, 2 SKIP** (T9a/T9c no API keys live; T13a-T13e bwrap tutti â). Con API keys live: 216 PASS.
CI GitHub Actions: run #29031945029 su `87ad26f` ✅ **SUCCESS** ✅ (ultimo run su main, 2026-07-09).

**âœ… FASE 2.5 compressione history** (2026-06-27, review #39, commit 65c4c7b).
**âœ… R-comp-1** â€” boundary piegato nel summary (2026-06-28, review #40, commit cde4d94). Caso degenere no-user coperto da T54.
**âœ… gas version 0.2.0** (2026-07-01, review #41 APPROVATO, commit d992c47 â†’ merge 2326404): `gas version` â†’ stampa versione + Python, zero token LLM. Test T55. Nessuna lezione nuova per memoria_revisore.md.
**✅ Config-drift stringhe modello — CHIUSO** (2026-07-07, review #43, branch `refactor/model-ids-fonte-unica`: merge `eb0509f`, commit `160543a`): `brains/model_ids.py` = fonte unica dei 5 ID modello della cascata, env-overridabili (`GAS_MODEL_*`). Suite della sessione: **217 PASS incluso T56**. **Caveat suite**: quei 217 PASS sono stati ottenuti in Codespace, dove i test bwrap NON sono validabili (comportamento noto); la verifica bwrap reale resta demandata a CI/postazione WSL locale. **CI sul merge**: run ID **28874912495** (run n. 85, evento push su `eb0509f`, 2026-07-07) — **SUCCESS** ✅.

**Stato item roadmap (review #38, commit a8c6d53) â€” stato reale:**
- ðŸ”´ **Item 1 â€” Controllo spesa token**: `_daily_cost_usd()` + kill-switch `GAS_DAILY_TOKEN_BUDGET` committati. Agiscono sul runtime GAS (Gemini/Groq free tier, costo ~0â‚¬). La spesa problematica (Claude Code dev su Opus) NON Ã¨ tracciata in `.gas_tokens.jsonl` e NON viene intercettata. â†’ **APERTO**: la disciplina dev (sez. 11 CLAUDE.md) resta l'unica leva reale.
- ðŸŸ¡ **Item 2 â€” Accesso da telefono**: `gas telegram` committato â€” interfaccia RUNTIME (GAS risponde all'utente via Telegram bot). L'accesso al dev tooling (Claude Code / repo da telefono via claude.ai/code o SSH+tmux) NON Ã¨ stato implementato. â†’ **APERTO** (il bridge runtime Ã¨ una FASE 5 anticipata utile; l'item originale dev tooling resta aperto).
- ðŸŸ¡ **Item 3 â€” R-wire-1 VEC_MIN_SIM**: `gas calibrate-vectors` committato â€” strumento di misura su diario reale (distribuzione score coseno, suggerisce soglia). La taratura effettiva richiede esecuzione sul VPS con diario reale. â†’ **APERTO** (strumento pronto, taratura da fare al deploy).
- ðŸŸ¡ **Item 4 â€” eval e5-small**: `gas eval-vectors` committato â€” espone statistiche vector store e ricerca semantica interattiva, documenta e5-small come alternativa configurabile. Valutazione comparativa e migrazione del modello NON effettuate. â†’ **APERTO**.
- ðŸŸ¡ **Item 5 â€” R-reidx-3 picco RAM**: batch paginati giÃ  introdotti in review #30 (2026-06-25). Non toccato in review #38. â†’ **APERTO** (ridotto, chiusura definitiva al deploy VPS).

Componenti attive:
- Snapshot preventivo anti-autodistruzione (fail-closed, refs/gas/snapshots/)
- Sandbox applicativo `run_command` (no-shell + allowlist + env sanificata)
- Sandbox OS bwrap (`GAS_SANDBOX_MODE=os_strict` default: rete isolata + fs read-only)
- `WINDOW_CHAR_CAP=24000` + `_cap_window_chars` (no slicing, scarto messaggi interi)
- Memoria SQLite `.gas_memory.db`: diario IMMUTABILE + rubrica contatti + FTS5 + backup auto
- Vector store `.gas_vectors.db` opt-in `GAS_VECTORS` (MiniLM 384-dim, cosine brute-force)
- CRM dal loop: tool `salva_contatto`/`imposta_stato_contatto`, identitÃ  su `chiave_norm` NFKC
- Iniezione always-on `_memoria_pin` (system msg) + tool `ricorda` (sola lettura)
- CLI `gas doctor` / `gas reindex` / `gas backup` / `gas tokens [N]` (contabilitÃ  token + stima USD + fallthrough)
- **Budget cap** (review #38): `_daily_cost_usd()` + kill-switch `GAS_DAILY_TOKEN_BUDGET` in `run_turn`
- **Telegram bridge** (review #38): `gas telegram` â†’ `modules/telegram/bot.py` (long polling, `TELEGRAM_BOT_TOKEN` + `TELEGRAM_ALLOWED_IDS`)
- **CLI vettori** (review #38): `gas calibrate-vectors` (distribuzione score â†’ suggerisce min_sim) + `gas eval-vectors [query]` (ricerca semantica interattiva)
- **Compressione history** (review #39, FASE 2.5): `_compress_history_if_needed()` auto-trigger in `run_turn`; `gas compress-history` CLI. Env: `GAS_HISTORY_MAX_MSGS` (default 100), `GAS_HISTORY_KEEP_MSGS` (default 20). Zero token LLM.
- Telemetria fallthrough (review #33): `_log_tokens` con `event`/`reason`; doctor sez.10
- `VectorStore.disable_reason` (review #35/36): motivo disable propagato a `gas doctor`

## Pipeline provider (paracadute)

1. `gemini-2.5-flash-lite` â†’ 2. `gemini-2.5-flash` â†’ 3. `groq/openai/gpt-oss-120b`
   â†’ 4. `openrouter` free (`meta-llama/llama-3.3-70b-instruct:free`)
   â†’ 5. `ollama` offline (`qwen2.5:7b-instruct`, solo se `GAS_OLLAMA_URL` settata)

## Finding aperti (ðŸŸ¡ attivi)

> Chiusi in `reports/stato_storico.md` e `reports/finding_archiviati.md`.

- âœ… **R-reidx-deps** â€” CHIUSO (2026-06-29): requirements.txt pinnato == (openai 2.43.0, requests 2.34.2, numpy 2.4.6, onnxruntime 1.27.0, fastembed 0.8.0); requests era il diretto mancante (crash deploy fresh); coppia numpy/onnxruntime pinnata insieme (ABI numpy 2.x); wheel manylinux x86_64 verificate disponibili (pip download, zero build). Runtime al deploy.
- ðŸŸ¡ **R-reidx-3** â€” picco RAM `reindex` su diario grande: **RIDOTTO** (review #30, 2026-06-25): `ricostruisci_da_diario` ora usa batch paginati (`diario_dopo`) â€” numpy transitori per batch (~400KB), accumulo blob proporzionale all'intero diario (~1.5KB/riga). Su CX33 8GB il picco totale Ã¨ gestibile; chiusura definitiva rinviata a ri-taratura su diario reale VPS.
- âœ… **R-vec-2** â€” `GAS_VECTORS_DB` + `GAS_EMBED_MODEL` configurabili via env (review #31, 2026-06-25).
- âœ… **R-vec-2b** â€” fingerprint-guard fail-closed: mismatch model_id (anche stessa dim) o DB legacy â†’ layer disabilitato, istruisce `gas reindex`; fingerprint scritto alla creazione e nel reindex (review #34, 2026-06-27).
- âœ… **R-vec-3** â€” CHIUSO (2026-07-02, sonda S0 2026-06-30 su CX33): import + embedding a runtime confermati sul box reale â€” BAAI/bge-small-en-v1.5 dims=384 load=3.5s, paraphrase-multilingual-MiniLM-L12-v2 dims=384 load=5.0s. **Boundary esplicito**: prova che l'embedder importa e produce vettori di dim corretta sul box reale; NON prova qualitÃ  semantica (â†’ R-wire-2) nÃ© comportamento sotto carico RAM concorrente (ollama+bot). Picco RSS 697MB a DUE modelli residenti (bge-small + multilingua); produzione carica UN SOLO modello (EMBED_MODEL multilingua) â†’ footprint reale < 697MB; 697 = ceiling conservativo, NON il costo del singolo modello. A S1b resta SOLO la misura RAM a regime del singolo modello.
- âœ… **R-vec-pool** (2026-07-03, review #42): `fastembed.__version__` aggiunto al fingerprint del vector store â€” sia in scrittura (creazione DB + `gas reindex`) sia in lettura (guard). DB legacy senza campo â†’ fail-closed ("DB legacy: fastembed_version assente"). Mismatch versione su stessa model_id+dim â†’ "fingerprint mismatch: DB fastembed=... â‰  ...". Test T39h-T39k (4 casi) aggiunti. Suite: 216 PASS. Introspezione pooling reale = FUORI SCOPE (decisione umana); `fastembed==0.8.0` resta pinnato in requirements.txt.
- ðŸŸ¡ **R-wire-1** (RESIDUO) â€” `VEC_MIN_SIM=0.30` tarata su esempi sintetici: ri-tarare sul diario reale del VPS. Env-config giÃ  fatto (review #28).
- ðŸŸ¡ **R-wire-2** â€” qualitÃ  semantica MiniLM limitata su query corte IT: limite di potenza, non correttezza. Legato a R-vec-3.
- ðŸŸ¡ **Esfiltrazione** â€” chiusa in `os_strict` con bwrap; in `os_with_fallback` resta ðŸŸ¡.
- âœ… **WINDOW_CHAR_CAP non env-configurabile** â€” `GAS_WINDOW_CHAR_CAP` configurabile via env, min_val=1000 (review #31, 2026-06-25).
- ðŸŸ¡ **Degrado a solo-testo per-turno non rilevato** (R2 review #5): cold doctor (`sez.8`) giÃ  copre tutti i rami a freddo â€” sonda 2026-06-29 confermata, nessun gap. Il per-turno resta SILENZIOSO (warning in `gas_debug.log`, fail-safe Â§9). Rimandato per falsi positivi.
- ðŸŸ¡ **R-crm-1b** â€” identitÃ  cross-formato non prevenuta (es. `anna@ex.com` vs `Anna`): meccanismo merge manuale disponibile (`unisci_contatti`), policy chiave canonica non presa.
- ✅ **R-groq-slash** (CHIUSO 2026-07-08) — formato `openai/gpt-oss-120b` accettato: STATUS 200, tool_calls parsate, latenza 1138ms, 7 reasoning_tokens. Validazione live eseguita con `reasoning_effort: "low"` (commit f028e51, review #44).
- ✅ **R-groq-dup** (CHIUSO 2026-07-08) — tutti e tre i brain importano `MODEL_GROQ` da `brains/model_ids.py` (fonte unica). Sorgente già unificata dal merge `model-ids-fonte-unica` (`eb0509f`). Confermato da revisore #44.
- 🟡 **R-legacy-slice** (riserva #1 revisore, review #43 model_ids, registrata 2026-07-09): `brains/claude_brain.py:38` contiene `for m in messages[-8:]` — slicing raw della history, violazione sez. 5 CLAUDE.md. Oggi INERTE: file legacy non wired al kernel attivo, zero copertura test. Diventa bloccante se i brain legacy venissero mai ri-agganciati. Debito tecnico latente, nessuna azione ora.
- ℹ️ **TPM burst gpt-oss-120b** — limite TPM 8K (vs 12K del precedente llama-3.3-70b-versatile). Fallthrough a OpenRouter più frequente in caso di burst = **comportamento atteso, non regressione**. Il paracadute §9 gestisce silenziosamente.
- âœ… **MEMORY_PIN_SCAN hardcoded** â€” `GAS_MEMORY_PIN_SCAN` configurabile via env, min_val=10 (review #31, 2026-06-25).
- ðŸŸ¡ **R-ci-openrouter** â€” T9a fragile se OPENROUTER_API_KEY Ã¨ presente: il test la poppava prima del turno T9 ma la tolleranza alla presenza di OPENROUTER non Ã¨ garantita formalmente (revisore CI-4, 2026-06-24).
- âœ… **CI-4** â€” risolto (2026-06-24): T9a/T9c skip condizionale su assenza API key live, CI verde.
- âœ… **R-tel-1** (chiuso review #37, 2026-06-27) â€” `_free_names` derivato da `FREE_RUNGS`; `name not in _free_names` come flag `obbligatoria`; `reason` nel JSONL = livello ("WARN"/"KO"). T40/T40b confermano. Riserve cosmetiche #37: (1) `reason` perde il testo descrittivo (â†’ `detail` futuro); (2) ollama non assertito in T40 (GAS_OLLAMA_URL assente â†’ skip).
- âœ… **Riserve review #35** (chiuse review #36, 2026-06-27) â€” T39b-reason/T39c-reason aggiungono assert su `disable_reason`; T39f (ramo `sqlite3.Error`) e T39g (ramo embedder assenti) coprono i 4 rami. Tutti PASS.
- ðŸŸ¡ **Riserve minori** (non bloccanti, dettaglio in archivio): R-test-1 cap_window_chars, R2 #6 chdir trap, R3 #4 falsi positivi path-check, riserve snapshot TASK C, riserve hook SessionEnd, riserve R-mem2a, riserve R-mem, R26-1/R26-2 backup.


### Cerebras zai-glm-4.7 free — SCARTATO come rung-4 (sonda live 2026-07-13, Codespace)
NO-GO. Due limiti ambientali misurati live, entrambi bloccanti per un paracadute h24 non presidiato:
1. Cap contesto free tier = 8192 token — MISURATO verbatim dall'API (context_length_exceeded ... limit is 8192).
   La doc ufficiale del modello dichiara 64k ED È FALSA. 8192 non basta per system + memory pin + tool schema
   + window 24k char; e il rung-4 scatta sui turni carichi (window piena) = contesto massimo quando il ceiling
   è più stretto (correlazione cattiva).
2. Coda free satura — 429 queue_exceeded su tentativi ad orari diversi. Disponibilità non garantita fuori dal
   nostro controllo → viola "paracadute affidabile".
Tool call (Gate 2) mai testata (coda satura), ma irrilevante: i due limiti bastano allo scarto.
Rung-4 resta OpenRouter. Motore NON toccato. Ri-valutabile SOLO su tier a pagamento Cerebras (131k, no coda)
= decisione di budget separata.
Sotto-lezioni:
- disable_reasoning su Cerebras DEPRECATO dal 2026-07-21; parametro vivo = reasoning_effort="none".
- Metodo sonde: uno script che segna FAIL su 403/429 è cieco al livello rete/coda. Un "FAIL" della sonda NON è
  fallimento di merito finché non si escludono blocco Cloudflare (403 err 1010 → risolto con User-Agent browser)
  e coda satura (429).
Prossimo candidato rung eventuale = Mistral (sessione a parte, sonda data-policy prima dei lead reali nel CRM).
Valutare anche SE serve un 5° rung (cascata già Gemini×2 + Groq + OpenRouter + Ollama).

## Prossimi passi (in ordine di prioritÃ )

1. ~~**FASE 2.5**~~ âœ… chiusa (review #39, 2026-06-27).
2. **ðŸ”´ Spesa token dev**: item 1 roadmap â€” il budget cap runtime Ã¨ inerte sul free tier. La leva reale Ã¨ la disciplina dev (sez. 11): `/clear` tra task, Sonnet default, Opus on-demand.
3. **ðŸ“± Accesso dev tooling da telefono**: item 2 roadmap â€” claude.ai/code o SSH+tmux. `gas telegram` (runtime bot) Ã¨ giÃ  disponibile ma non Ã¨ questo. **Sonda Dispatch pendente** (pairing QR + task doc-only da telefono; verificare ambiente Win/WSL, hook, modello). Se OK, item 2 chiuso senza bridge custom.
4. **FASE 3 â€” Interfaccia vocale**: Whisper STT + ElevenLabs TTS.
5. **FASE 4.5 â€” Task scheduler autonomo**: catalogo YAML task notturni (item 4 roadmap, prerequisito Jarvis).
6. **FASE 5 S1 ✅ e S1b ✅ completati (2026-07-04)** → prossimo S2 (decide operatore)
7. **Riserve review #38** (non bloccanti): R-tel-budget-perf (scan JSONL crescente), R-tel-tool_res (cosmetic).

### PARK â€” registrati, nessun impegno
- Retention del diario (archiviazione/export, MAI DELETE â€” quando il volume lo richiederÃ ).
- GDPR / dati personali lead: da guardare a FASE 4.

## Istituzioni di processo

- **A** â€” `reports/stato_progetto.md` (questo file): stato vivo, aggiornato a fine task.
- **A-arch** â€” `reports/stato_storico.md`: storico sessioni + finding chiusi + dettaglio motore.
- **B** â€” `reports/diff_sessione.md`: diff della sessione corrente (riscritto a ogni sessione).
- **C** â `.claude/agents/revisore.md`: gate obbligatorio pre-commit motore. **44 review**. Ultima: **#44** (migrazione gpt-oss-120b + reasoning_effort low, 2026-07-08). Lezioni in `.claude/agents/memoria_revisore.md`.
- **D** â€” `reports/handoff.md`: dossier di fine sessione (DECISIONI UMANE + diff stat + log + delta test + verdetto revisore + stato CI).
- **D-cmd** â€” `.claude/commands/fine-task.md`: template `/fine-task`. BASE dinamico da last handoff commit (`${BASE}..HEAD`); Â§1 SCOPE & ESITO FETTE obbligatorio (FATTA/SALTATA/DEFERITA).

## Note operative VPS â€” non per oggi

> Registrate il 2026-06-15 (aggiornate 2026-07-02, sonda S0 + allineamento canonici + correttivo post-a15ff61: R-vec-3 âœ… chiuso, no-swap finding, req non-root specifico).

**Hardware confermato (sonda diretta 2026-07-02):** Hetzner **CX33** Helsinki â€” x86_64, 4 core, 7.6Gi RAM usabile (7.1Gi disponibile a vuoto), 70Gi disco liberi (NON CX22/4GB come da nota precedente errata).

ðŸ”´ **FINDING no-swap (sonda 2026-07-02):** il box NON ha swap (default Hetzner). Su 7.6Gi condivisi da OS + GAS+embedder + ollama 3B + bot trading demo, un picco = OOM killer SECCO (nessun cuscinetto) su macchina h24 non presidiata â†’ viola "zero crash". Conseguenze:
- (a) La unit systemd di S1b DEVE settare `MemoryHigh`/`MemoryMax` su GAS (ordine di grandezza: `MemoryHigh ~1.5Gi`, `MemoryMax ~2Gi` â€” GAS+embedder stanno <1Gi a regime, il margine copre i picchi di reindex; da affinare a S1b con misura reale). Scopo: se qualcosa sfonda, GAS degrada/riparte in modo prevedibile via `Restart=always` invece di innescare un OOM che colpisce il bot trading.
- (b) Ollama "3B always-on" da RIVALUTARE â†’ probabile on-demand (spawn quando la cascata arriva a ollama, unload dopo) o modello 1-1.5B se always-on, causa RAM limitata + no-swap. Decisione a S3, qui solo registrata come aperta.
- (c) OPZIONE S1a da valutare: aggiungere swap file 2-4Gi (costo trascurabile su 70Gi liberi) come cuscinetto per h24 non presidiato. Non decisa, messa sul tavolo.

1. **Snapshot**: 0 ref in dev Ã¨ ATTESO (il runtime GAS non gira qui). Sul VPS gli snapshot nasceranno da `run_command`/`write_file` â†’ se doctor sez.7 mostrasse 0 ref sul VPS sarebbe anomalo. ~4427 oggetti loose = detrito git (stash/churn), non snapshot; `git gc` OPT-IN li riassorbe.
2. **OpenRouter free ~28s**: rung lento, paracadute non piano operativo. Ollama locale = pavimento rapido a costo zero. **Modello ollama per VPS: 3B (es. `qwen2.5:3b-instruct`), NON 7B** â€” gli 8 GB sono condivisi da GAS + embedder fastembed (~500 MB model cache) + bot trading demo coabitante; un 7B esaurisce la RAM.
3. **Contesto sicurezza OBBLIGATORIO per S1** (bot trading demo coabitante): (a) `GAS_SANDBOX_MODE=os_strict` OBBLIGATORIO finchÃ© il bot trading coabita â€” chiavi exchange sulla stessa macchina di un'AI che esegue codice = superficie di esfiltrazione non accettabile in os_with_fallback; (b) utente runtime **non-root** Ã¨ requisito di sicurezza RAFFORZATO (non solo best practice): processo AI con accesso codice + chiavi exchange dello stesso utente root = game over in caso di exploit; (c) **Requisito esplicito S1**: creare utente runtime dedicato non-root e spostare working dir + model cache + `.gas_*.db` fuori da `/root`, di proprietÃ  di quell'utente. Evidenza sonda S0: `VECTORS_DB /root/gas/.gas_vectors.db` â€” runtime e cache/db girano attualmente sotto `/root` come root.
4. **Decisione systemd ratificata**: `gas doctor` NON deve essere ExecStartPre/gate di avvio â€” esce 1 anche su sole API key assenti (semantica dichiarata in CLAUDE.md sez.3). Comportamento corretto: `Restart=always` + `RestartSec=10` + notifica Telegram al primo turno se degradato (doctor come check post-avvio, non blocco pre-avvio).
5. **R-vec-pool ✅ (2026-07-03)**: fingerprint ora include `fastembed_version`. Upgrade fastembed → mismatch versione → guard spegne il layer e obbliga a `gas reindex` (fail-closed). Il reindex non è più affidato alla memoria dell operatore ma forzato dal codice.
6.  **Confine sviluppo da telefono** (Claude Code cloud, sondato 2026-07-01): loop telefonoâ†’cloudâ†’revisoreâ†’CI validato su evidenza reale (revisore+hook scattano nel cloud; CI verde run #50 su `d992c47`). CONFINE DURO: `bwrap` ASSENTE nel sandbox cloud â†’ test sandbox/`run_command`/snapshot strutturalmente rossi lÃ¬, NON validabili da telefono (solo CI). Nessuna credenziale LLM nel cloud â†’ runtime GAS non eseguibile lÃ¬. Fattibile da telefono: doc-only + motore leggero non-sandbox verificabile da CI. Da sondare a parte: claude remote-control (ambiente reale, claim non verificato). Limite accertato 2026-07-02: Claude Code cloud pusha SOLO sul branch di sessione, NON crea branch â†’ i task cloud si stratificano, serve estrai-e-cancella a valle.
7. **â RISOLTO â postazione locale WSL operativa** (sonda 2026-07-03): bubblewrap 0.9.0, suite 214 PASS, T13a-T13e bwrap tutti â. Sviluppo locale pienamente abilitato (clone git + venv + suite + bwrap). La barriera FASE 5 era questa; ora rimossa.
8. **✅ S1 ESEGUITO (2026-07-04):** hardening SSH + utente runtime completati sul VPS CX33.
   - unattended-upgrades: attivo (running)
   - fail2ban: attivo, jail sshd, backend=auto, 4 IP bannati al reboot
   - Utente `gas` (uid=1000): creato, `/home/gas/gas/` copia working dir, `/home/gas/.cache/` model cache fastembed
   - sshd hardening: `PasswordAuthentication no`, `PermitRootLogin no`, `PubkeyAuthentication yes` (dropin `/etc/ssh/sshd_config.d/99-hardening.conf`)
   - Kernel aggiornato: 6.8.0-134-generic (reboot post-S1 ok)
   - `/root/gas/` INTATTO (non cancellare fino a S1b confermato)
   - Accesso SSH: solo `gas@204.168.251.92` via chiave ed25519. Login root SSH disabilitato.
9. **S1b ✅ (2026-07-04):** swap file 2GiB attivo (cuscinetto anti-OOM, vedi finding no-swap sopra); unit systemd `/etc/systemd/system/gas.service` con `User=gas`, `MemoryHigh=1500M`, `MemoryMax=2000M`, `Restart=always`; `.env.prod` in `/home/gas/gas/.env.prod` con permessi `chmod 600`; servizio attivo confermato. Data di misura RAM a regime del singolo modello: non registrato.



- ✅ **Riserve review #44 A e C — CHIUSE** (2026-07-13): commento inline reasoning_effort nei 3 brain (groq_brain.py, claude_brain.py, gemini_brain.py) + T36c legato a MODEL_GROQ (fonte unica). Review #45 APPROVATO. Merge PR #4 su main (3836111), CI run 29235274026 SUCCESS.
  (A) ✅ **CHIUSO** — commento inline aggiunto che documenta il vincolo reasoning_effort="low" e il rischio di override con modello non-reasoning.
  (B) ✅ **CHIUSO** (2026-07-13) — Prezzi Groq ora in `brains/model_ids.py` come costanti env-overridabili `GAS_GROQ_PRICE_IN`/`GAS_GROQ_PRICE_OUT` (fallback 0.15/0.60). Commit `290a336`, PR fix/riserva-44B-groq-prezzi-env. Review #46 APPROVATO.
  (C) ✅ **CHIUSO** — T36c ora usa la costante MODEL_GROQ (import da brains/model_ids.py) invece del literal.
- ⚠️ **Nota di processo — scope creep sessione 2026-07-08**: fetta concordata = migrazione Groq; fuori mandato: (1) chiuso R-groq-dup (era deferito a slice separata), (2) toccato CLAUDE.md, (3) toccato runbook_s1. Esito tecnico corretto (review #44), ma lo scope lo decide l'operatore: registrata recidiva dell'anti-pattern. Mitigazione strutturale: ruleset `main-lock` attivo dal 2026-07-09 (no push diretto su main, CI `unit-suite` required, self-merge).

### DA FARE — sviluppo/processo (aperti dal 2026-07-09)
- ⬜ **Installare `gh` CLI** — comodità, non requisito: il merge PR si fa già da browser o da Codespace (gh preinstallato). Serve solo per merge doc-only da terminale locale. Consigliato `sudo apt install gh`. Non bloccante.
- ✅ **Hardening token Claude Code** — verificato 2026-07-13: token Codespace OAuth (`ghu_*`) non ha Administration per default. Tentativo di scrittura su ruleset `main-lock` (id 18805824) → 404/403 confermato via curl. Lucchetto non aggirabile dal token di Claude Code. CHIUSO.
