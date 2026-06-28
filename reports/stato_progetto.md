# STATO PROGETTO GAS

> Fotografia viva dello stato. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-06-28** (fix R-comp-1 — boundary piegato nel summary, review #40)
> Storico sessioni, dettaglio componenti, finding chiusi: `reports/stato_storico.md`

## Stato motore

FASE 1 ✅, FASE 2 ✅ e **FASE 2.5** ✅ chiuse. **40 review** completate. Suite: **196 PASS, 7 FAIL** (Windows locale, pre-esistenti bwrap/WinError32).
CI GitHub Actions: run #28307518983 su `cde4d94` — **SUCCESS** ✅.

**✅ FASE 2.5 compressione history** (2026-06-27, review #39, commit 65c4c7b).
**✅ R-comp-1** — boundary piegato nel summary (2026-06-28, review #40, commit cde4d94). Caso degenere no-user coperto da T54.

**Stato item roadmap (review #38, commit a8c6d53) — stato reale:**
- 🔴 **Item 1 — Controllo spesa token**: `_daily_cost_usd()` + kill-switch `GAS_DAILY_TOKEN_BUDGET` committati. Agiscono sul runtime GAS (Gemini/Groq free tier, costo ~0€). La spesa problematica (Claude Code dev su Opus) NON è tracciata in `.gas_tokens.jsonl` e NON viene intercettata. → **APERTO**: la disciplina dev (sez. 11 CLAUDE.md) resta l'unica leva reale.
- 🟡 **Item 2 — Accesso da telefono**: `gas telegram` committato — interfaccia RUNTIME (GAS risponde all'utente via Telegram bot). L'accesso al dev tooling (Claude Code / repo da telefono via claude.ai/code o SSH+tmux) NON è stato implementato. → **APERTO** (il bridge runtime è una FASE 5 anticipata utile; l'item originale dev tooling resta aperto).
- 🟡 **Item 3 — R-wire-1 VEC_MIN_SIM**: `gas calibrate-vectors` committato — strumento di misura su diario reale (distribuzione score coseno, suggerisce soglia). La taratura effettiva richiede esecuzione sul VPS con diario reale. → **APERTO** (strumento pronto, taratura da fare al deploy).
- 🟡 **Item 4 — eval e5-small**: `gas eval-vectors` committato — espone statistiche vector store e ricerca semantica interattiva, documenta e5-small come alternativa configurabile. Valutazione comparativa e migrazione del modello NON effettuate. → **APERTO**.
- 🟡 **Item 5 — R-reidx-3 picco RAM**: batch paginati già introdotti in review #30 (2026-06-25). Non toccato in review #38. → **APERTO** (ridotto, chiusura definitiva al deploy VPS).

Componenti attive:
- Snapshot preventivo anti-autodistruzione (fail-closed, refs/gas/snapshots/)
- Sandbox applicativo `run_command` (no-shell + allowlist + env sanificata)
- Sandbox OS bwrap (`GAS_SANDBOX_MODE=os_strict` default: rete isolata + fs read-only)
- `WINDOW_CHAR_CAP=24000` + `_cap_window_chars` (no slicing, scarto messaggi interi)
- Memoria SQLite `.gas_memory.db`: diario IMMUTABILE + rubrica contatti + FTS5 + backup auto
- Vector store `.gas_vectors.db` opt-in `GAS_VECTORS` (MiniLM 384-dim, cosine brute-force)
- CRM dal loop: tool `salva_contatto`/`imposta_stato_contatto`, identità su `chiave_norm` NFKC
- Iniezione always-on `_memoria_pin` (system msg) + tool `ricorda` (sola lettura)
- CLI `gas doctor` / `gas reindex` / `gas backup` / `gas tokens [N]` (contabilità token + stima USD + fallthrough)
- **Budget cap** (review #38): `_daily_cost_usd()` + kill-switch `GAS_DAILY_TOKEN_BUDGET` in `run_turn`
- **Telegram bridge** (review #38): `gas telegram` → `modules/telegram/bot.py` (long polling, `TELEGRAM_BOT_TOKEN` + `TELEGRAM_ALLOWED_IDS`)
- **CLI vettori** (review #38): `gas calibrate-vectors` (distribuzione score → suggerisce min_sim) + `gas eval-vectors [query]` (ricerca semantica interattiva)
- **Compressione history** (review #39, FASE 2.5): `_compress_history_if_needed()` auto-trigger in `run_turn`; `gas compress-history` CLI. Env: `GAS_HISTORY_MAX_MSGS` (default 100), `GAS_HISTORY_KEEP_MSGS` (default 20). Zero token LLM.
- Telemetria fallthrough (review #33): `_log_tokens` con `event`/`reason`; doctor sez.10
- `VectorStore.disable_reason` (review #35/36): motivo disable propagato a `gas doctor`

## Pipeline provider (paracadute)

1. `gemini-2.5-flash-lite` → 2. `gemini-2.5-flash` → 3. `groq/llama-3.3-70b-versatile`
   → 4. `openrouter` free (`meta-llama/llama-3.3-70b-instruct:free`)
   → 5. `ollama` offline (`qwen2.5:7b-instruct`, solo se `GAS_OLLAMA_URL` settata)

## Finding aperti (🟡 attivi)

> Chiusi in `reports/stato_storico.md` e `reports/finding_archiviati.md`.

- ✅ **R-reidx-deps** — CHIUSO (2026-06-29): requirements.txt pinnato == (openai 2.43.0, requests 2.34.2, numpy 2.4.6, onnxruntime 1.27.0, fastembed 0.8.0); requests era il diretto mancante (crash deploy fresh); coppia numpy/onnxruntime pinnata insieme (ABI numpy 2.x); wheel manylinux x86_64 verificate disponibili (pip download, zero build). Runtime al deploy.
- 🟡 **R-reidx-3** — picco RAM `reindex` su diario grande: **RIDOTTO** (review #30, 2026-06-25): `ricostruisci_da_diario` ora usa batch paginati (`diario_dopo`) — numpy transitori per batch (~400KB), accumulo blob proporzionale all'intero diario (~1.5KB/riga). Su CX22 4GB il picco totale è gestibile; chiusura definitiva rinviata a ri-taratura su diario reale VPS.
- ✅ **R-vec-2** — `GAS_VECTORS_DB` + `GAS_EMBED_MODEL` configurabili via env (review #31, 2026-06-25).
- ✅ **R-vec-2b** — fingerprint-guard fail-closed: mismatch model_id (anche stessa dim) o DB legacy → layer disabilitato, istruisce `gas reindex`; fingerprint scritto alla creazione e nel reindex (review #34, 2026-06-27).
- 🟡 **R-vec-3** — RIDOTTO (2026-06-29): wheel x86_64 installabili confermate (manylinux_2_28, pip download OK); resta da provare import+embedding a runtime sul CX22 (FASE 5).
- 🟡 **R-wire-1** (RESIDUO) — `VEC_MIN_SIM=0.30` tarata su esempi sintetici: ri-tarare sul diario reale del VPS. Env-config già fatto (review #28).
- 🟡 **R-wire-2** — qualità semantica MiniLM limitata su query corte IT: limite di potenza, non correttezza. Legato a R-vec-3.
- 🟡 **Esfiltrazione** — chiusa in `os_strict` con bwrap; in `os_with_fallback` resta 🟡.
- ✅ **WINDOW_CHAR_CAP non env-configurabile** — `GAS_WINDOW_CHAR_CAP` configurabile via env, min_val=1000 (review #31, 2026-06-25).
- 🟡 **Degrado a solo-testo per-turno non rilevato** (R2 review #5): cold doctor (`sez.8`) già copre tutti i rami a freddo — sonda 2026-06-29 confermata, nessun gap. Il per-turno resta SILENZIOSO (warning in `gas_debug.log`, fail-safe §9). Rimandato per falsi positivi.
- 🟡 **R-crm-1b** — identità cross-formato non prevenuta (es. `anna@ex.com` vs `Anna`): meccanismo merge manuale disponibile (`unisci_contatti`), policy chiave canonica non presa.
- ✅ **MEMORY_PIN_SCAN hardcoded** — `GAS_MEMORY_PIN_SCAN` configurabile via env, min_val=10 (review #31, 2026-06-25).
- 🟡 **R-ci-openrouter** — T9a fragile se OPENROUTER_API_KEY è presente: il test la poppava prima del turno T9 ma la tolleranza alla presenza di OPENROUTER non è garantita formalmente (revisore CI-4, 2026-06-24).
- ✅ **CI-4** — risolto (2026-06-24): T9a/T9c skip condizionale su assenza API key live, CI verde.
- ✅ **R-tel-1** (chiuso review #37, 2026-06-27) — `_free_names` derivato da `FREE_RUNGS`; `name not in _free_names` come flag `obbligatoria`; `reason` nel JSONL = livello ("WARN"/"KO"). T40/T40b confermano. Riserve cosmetiche #37: (1) `reason` perde il testo descrittivo (→ `detail` futuro); (2) ollama non assertito in T40 (GAS_OLLAMA_URL assente → skip).
- ✅ **Riserve review #35** (chiuse review #36, 2026-06-27) — T39b-reason/T39c-reason aggiungono assert su `disable_reason`; T39f (ramo `sqlite3.Error`) e T39g (ramo embedder assenti) coprono i 4 rami. Tutti PASS.
- 🟡 **Riserve minori** (non bloccanti, dettaglio in archivio): R-test-1 cap_window_chars, R2 #6 chdir trap, R3 #4 falsi positivi path-check, riserve snapshot TASK C, riserve hook SessionEnd, riserve R-mem2a, riserve R-mem, R26-1/R26-2 backup.

## Prossimi passi (in ordine di priorità)

1. ~~**FASE 2.5**~~ ✅ chiusa (review #39, 2026-06-27).
2. **🔴 Spesa token dev**: item 1 roadmap — il budget cap runtime è inerte sul free tier. La leva reale è la disciplina dev (sez. 11): `/clear` tra task, Sonnet default, Opus on-demand.
3. **📱 Accesso dev tooling da telefono**: item 2 roadmap — claude.ai/code o SSH+tmux. `gas telegram` (runtime bot) è già disponibile ma non è questo.
4. **FASE 3 — Interfaccia vocale**: Whisper STT + ElevenLabs TTS.
5. **FASE 4.5 — Task scheduler autonomo**: catalogo YAML task notturni (item 4 roadmap, prerequisito Jarvis).
6. **FASE 5 — Deploy VPS Hetzner**: al deploy → `gas telegram` daemon (systemd), `gas calibrate-vectors` (item 3), checklist R-vec-3 (import+embedding runtime) / R-wire-1 / R-reidx-3 (item 5). [R-reidx-deps ✅ chiuso]
7. **Riserve review #38** (non bloccanti): R-tel-budget-perf (scan JSONL crescente), R-tel-tool_res (cosmetic).

### PARK — registrati, nessun impegno
- Retention del diario (archiviazione/export, MAI DELETE — quando il volume lo richiederà).
- GDPR / dati personali lead: da guardare a FASE 4.

## Istituzioni di processo

- **A** — `reports/stato_progetto.md` (questo file): stato vivo, aggiornato a fine task.
- **A-arch** — `reports/stato_storico.md`: storico sessioni + finding chiusi + dettaglio motore.
- **B** — `reports/diff_sessione.md`: diff della sessione corrente (riscritto a ogni sessione).
- **C** — `.claude/agents/revisore.md`: gate obbligatorio pre-commit motore. **40 review**. Ultima: **#40** (R-comp-1 fix boundary, 2026-06-28). Lezioni in `.claude/agents/memoria_revisore.md`.
- **D** — `reports/handoff.md`: dossier di fine sessione (DECISIONI UMANE + diff stat + log + delta test + verdetto revisore + stato CI).
- **D-cmd** — `.claude/commands/fine-task.md`: template `/fine-task`. BASE dinamico da last handoff commit (`${BASE}..HEAD`); §1 SCOPE & ESITO FETTE obbligatorio (FATTA/SALTATA/DEFERITA).

## Note operative VPS — non per oggi

> Registrate il 2026-06-15 per il deploy (FASE 5).

1. **Snapshot**: 0 ref in dev è ATTESO (il runtime GAS non gira qui). Sul VPS gli snapshot nasceranno da `run_command`/`write_file` → se doctor sez.7 mostrasse 0 ref sul VPS sarebbe anomalo. ~4427 oggetti loose = detrito git (stash/churn), non snapshot; `git gc` OPT-IN li riassorbe.
2. **OpenRouter free ~28s**: rung lento, paracadute non piano operativo. VPS va dimensionato per `qwen2.5:7b-instruct` (ollama locale = pavimento rapido a costo zero).
