# STATO PROGETTO GAS

> Fotografia viva dello stato. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-07-18** (FETTA DOC fix/ci-hook-tests: canonici aggiornati post-review #55 — R-hook-jq, R-ci-summary, riserve #52–#54 risolte, stato WSL reale, debito Codespace)
> Storico sessioni, dettaglio componenti, finding chiusi: `reports/stato_storico.md`

## Stato motore

FASE 1 âœ…, FASE 2 âœ… e **FASE 2.5** âœ… chiuse. **54 review** completate (ultima #54, 2026-07-16, Fetta 3 hook scrivi_rep.sh, APPROVATO CON RISERVE). Suite (locale WSL bwrap, sonda 2026-07-03): **220 PASS, 0 FAIL, 2 SKIP** (T9a/T9c no API keys live; T13a-T13e bwrap tutti ✅). +7 T57 + 6 T58 + 5 T59 aggiunti. CI run 29482410951 (2026-07-16, feature/f6-history-atomica): **241 PASS** ✅.
CI GitHub Actions — ultimi run su main (tutti ✅ SUCCESS): PR #22 merge `6ee5c85` (2026-07-18) · PR #21 run `29505642515` su `8f9cf7b` (2026-07-16) · PR #20 run `29487631549` su `fbf8246` (2026-07-16) · PR #19 run `29484338680` su `9a9278e` (2026-07-16) · PR #18 run `29481225884` su `fe0e476` (2026-07-16).

**âœ… FASE 2.5 compressione history** (2026-06-27, review #39, commit 65c4c7b).
**âœ… R-comp-1** â€” boundary piegato nel summary (2026-06-28, review #40, commit cde4d94). Caso degenere no-user coperto da T54.
**âœ… gas version 0.2.0** (2026-07-01, review #41 APPROVATO, commit d992c47 â†’ merge 2326404): `gas version` â†’ stampa versione + Python, zero token LLM. Test T55. Nessuna lezione nuova per memoria_revisore.md.
**✅ Config-drift stringhe modello — CHIUSO** (2026-07-07, review #43, branch `refactor/model-ids-fonte-unica`: merge `eb0509f`, commit `160543a`): `brains/model_ids.py` = fonte unica dei 5 ID modello della cascata, env-overridabili (`GAS_MODEL_*`). Suite della sessione: **217 PASS incluso T56**. **Caveat suite**: quei 217 PASS sono stati ottenuti in Codespace, dove i test bwrap NON sono validabili (comportamento noto); la verifica bwrap reale resta demandata a CI/postazione WSL locale. **CI sul merge**: run ID **28874912495** (run n. 85, evento push su `eb0509f`, 2026-07-07) — **SUCCESS** ✅.

**Stato item roadmap (review #38, commit a8c6d53) â€” stato reale:**
- ðŸ”´ **Item 1 â€” Controllo spesa token**: `_daily_cost_usd()` + kill-switch `GAS_DAILY_TOKEN_BUDGET` committati. Agiscono sul runtime GAS (Gemini/Groq free tier, costo ~0â‚¬). La spesa problematica (Claude Code dev su Opus) NON Ã¨ tracciata in `.gas_tokens.jsonl` e NON viene intercettata. â†’ **APERTO**: la disciplina dev (sez. 11 CLAUDE.md) resta l'unica leva reale.
- ✅ **Item 2 — Accesso da telefono**: `gas telegram` committato — interfaccia RUNTIME (GAS risponde all'utente via Telegram bot). Accesso al dev tooling da telefono risolto via Remote Control (`/rc`): sessione locale su Giulia/WSL raggiunta da telefono, lettura file reale del repo confermata, nessun bridge custom necessario. → **CHIUSO (2026-07-15)**.
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

## Finding aperti (🟡 attivi)

> Chiusi in `reports/stato_storico.md` e `reports/finding_archiviati.md`.

- 🟡 **Esfiltrazione** — chiusa in `os_strict` con bwrap; in `os_with_fallback` resta 🟡.
- 🟡 **Degrado a solo-testo per-turno non rilevato** (R2 review #5): cold doctor (`sez.8`) già copre tutti i rami a freddo — sonda 2026-06-29 confermata, nessun gap. Il per-turno resta SILENZIOSO (warning in `gas_debug.log`, fail-safe §9). Rimandato per falsi positivi.
- 🟡 **R-crm-1b** — Fetta email ✅ + merge umano ✅ (review #47+#48, 2026-07-14): `rileva_duplicati_email()` + CLI `gas check-dups` + `gas merge-contacts <da> <verso>` (preview, conferma y/N, snapshot diario atomico pre-merge, fail-safe §9). Hint `check_dups_cmd` corretto. Resta 🟡 per: idempotenza diario (fetta 2), telefono (fetta 3).
- 🟡 **R-ci-openrouter** — T9a fragile se OPENROUTER_API_KEY è presente: il test la poppava prima del turno T9 ma la tolleranza alla presenza di OPENROUTER non è garantita formalmente (revisore CI-4, 2026-06-24).
- 🟡 **R-ci-hooks** — `tests/test_unit_hooks.py` NON eseguito da CI (sonda 2026-07-17): il job `unit-suite` esegue SOLO `python tests/test_unit_kernel.py` (ci.yml riga 83). Il file `test_unit_hooks.py` esiste in `tests/` (T-hook-a/b/c/d/e/f/g/h, 357 righe) ma non compare in nessun comando del workflow. Il verde copre `tests/test_unit_kernel.py` meno gli SKIP (T9a/T9c su assenza GEMINI/GROQ API key), e NON copre `tests/test_unit_hooks.py`.
  **Implicazione**: I finding hook chiusi con PR #20 (fbf8246) e PR #21 (8f9cf7b) citano "CI run ✅ SUCCESS" come evidenza. Quel verde non ha eseguito alcun test degli hook: `tests/test_unit_hooks.py` non è nel workflow. L'unica evidenza che T-hook-a…g passano è un `pytest tests/test_unit_hooks.py` eseguito in locale e riportato dall'agente — non un artefatto CI. Nessun difetto accertato negli hook; ma la citazione del verde CI accanto a un fix di hook implica una validazione che non è avvenuta. Finché R-ci-hooks è aperto, il verde CI non è evidenza valida per modifiche a `.claude/hooks/`.
  **Stato (2026-07-18)**: MITIGATO SU BRANCH, NON CHIUSO. La CI esegue i test hook dal commit `1ed3524` (run `29591105016` ✅, poi `29592358732` ✅ su HEAD `f6d7a62`); su main il gap resta finché la PR `fix/ci-hook-tests` non è mergiata. Chiusura solo a merge avvenuto, con hash reale.
- 🔴 **R-hook-jq** — `scrivi_rep.sh` (righe 11-12) invoca `jq` con `2>/dev/null`, che sopprime anche "command not found". Con jq assente: TP vuoto → exit 0 silenzioso, nessun file scritto, stderr vuoto. La feature "scrivi rep" è **INERTE IN SILENZIO** su qualunque macchina senza jq — incluso il WSL locale canonico, dove jq mancava fino al 2026-07-17 (installato a mano: jq-1.7). Da quanto fosse inerte: non determinabile. Verde in CI e Codespace perché lì jq è preinstallato → il verde CI NON copre questa classe di difetto. Viola "la memoria non deve mentire": l'utente crede di aver salvato, non ha salvato, nessun errore. Scoperto solo perché T-hook-h asserisce su stderr non vuoto. Fix DEFERITO a task separato: distinguere "nessun trigger" (no-op corretto) da "dipendenza mancante" (fail-loud su stderr, exit 0 per non bloccare il turno) + test T-hook-i con PATH ripulito da jq. Nello STESSO task futuro accodare: (1) il commento riga 3 dell'hook ("incl. auto-push su main") stantio dal main-lock; (2) riserva #55(1) — T-hook-h non copre il caso detached-HEAD per `scrivi_rep.sh` (il codice lo copre, manca il test, analogo a T-hook-c).
- 🟡 **R-ci-summary** (riserva #55(2), cosmetica) — il Job Summary di `ci.yml` cattura via `tee` solo `test_unit_kernel.py`; la hook suite (pytest) non compare nel summary a colpo d'occhio. Il gate resta corretto (rosso su FAIL, exit code nativo pytest), manca solo la visibilità nel riquadro. Non bloccante.
- ✅ **F6-history-atomica CHIUSO** (2026-07-16, review #50 APPROVATO, PR #19, CI run `29482410951` ✅ 241 PASS): `_save_history` usa ora tmp+`os.replace` atomico (fsync); `_load_history` quarantena il file corrotto in `.gas_history.json.corrupt.<ts>` (logging.warning, mai crash). Test T59a/b/c. **Mergeata → 9a9278e su main ✅ (2026-07-16, CI run 29484338680 SUCCESS)**.
- 🟡 **Riserve minori** (non bloccanti, dettaglio in archivio): R-test-1 cap_window_chars, R2 #6 chdir trap, R3 #4 falsi positivi path-check, riserve snapshot TASK C, riserve hook SessionEnd, riserve R-mem2a, riserve R-mem, R26-1/R26-2 backup.

### DEPLOY VPS — da tarare su dati reali

- 🟡 **R-reidx-3** — picco RAM `reindex` su diario grande: **RIDOTTO** (review #30, 2026-06-25): `ricostruisci_da_diario` usa batch paginati (`diario_dopo`) — numpy transitori per batch (~400KB), accumulo blob proporzionale all'intero diario (~1.5KB/riga). Su CX33 8GB gestibile; chiusura definitiva rinviata a ri-taratura su diario reale VPS.
- 🟡 **R-wire-1** (RESIDUO) — `VEC_MIN_SIM=0.30` tarata su esempi sintetici: ri-tarare sul diario reale del VPS. Env-config già fatto (review #28).
- 🟡 **RAM a regime del singolo modello** — `MemoryHigh=1500M`/`MemoryMax=2000M` in `gas.service` (S1b, 2026-07-04): misura reale non ancora registrata. Da rilevare su VPS con diario attivo prima di affinare i limiti systemd.

### Limiti noti (non-finding)

- **R-wire-2** — qualità semantica MiniLM limitata su query corte IT: limite di potenza, non correttezza. Legato a R-vec-3 (chiuso).

### Debito latente

- ✅ **R-legacy-slice CHIUSO** (2026-07-15, questa PR): `brains/claude_brain.py` rimosso con la pulizia F3 — lo slicing `messages[-8:]` è stato eliminato alla radice insieme al file che lo conteneva. Nessun residuo.
- ✅ **R-crm-diario-rr CHIUSO** (2026-07-16, PR #18 `fix/diario-recursive-triggers`): aggiunto `PRAGMA recursive_triggers = ON` in `MemoryStore._connect()` — con ON il DELETE implicito della REPLACE attiva `diario_no_delete` (ABORT). Nuovo test T19f-rr copre il varco via `m._connect()`. Revisore: APPROVATO CON RISERVE (riserva risolta in-session). OR REPLACE sul diario: assente (verificato su `unisci_contatti`, `unisci_contatti_con_snapshot`, tutti i moduli).
- **Note minori — revisione Fable-5 (2026-07-15, nessuna azione impegnata)**: (a) logging su path RELATIVO `gas_debug.log` (segue la cwd, non la root: ok sotto systemd, log vagante se lanciato da altra dir); (b) messaggi di `_cap_tool_output` suggeriscono `sed -n` che l'allowlist nega (F4); (c) `classifica_compito`: ogni messaggio ≥60 char = "complesso" → salta spesso flash-lite (costo ~0 oggi); (d) il bot Telegram processa anche `edited_message` (ri-editare un vecchio messaggio lo ri-esegue; innocuo con whitelist); (e) commento prezzi Gemini in gas.py datato 2025-06 (allineare alla prossima occasione); (f) CLAUDE.md sez.2 descriveva cascata e Core Files non più reali (corretto nella fetta 2 di questa PR).

> ℹ️ **TPM burst gpt-oss-120b** — limite TPM 8K (vs 12K del precedente llama-3.3-70b-versatile). Fallthrough a OpenRouter più frequente in caso di burst = comportamento atteso, non regressione.

### Decisione bancata — Cerebras zai-glm-4.7 free (sonda 2026-07-13)

NO-GO come rung-4. Due limiti bloccanti per paracadute h24 non presidiato:
1. Cap contesto free tier = **8192 token** misurato live (doc dichiara 64k — falso). Insufficiente per system + pin + schema + window.
2. Coda free satura — 429 queue_exceeded a orari diversi. Disponibilità non garantita.
Rung-4 resta OpenRouter. Ri-valutabile solo su tier a pagamento (131k, no coda) = decisione di budget separata.
Prossimo candidato eventuale: Mistral (sonda data-policy prima dei lead CRM).
## Prossimi passi (in ordine di prioritÃ )

1. ~~**FASE 2.5**~~ âœ… chiusa (review #39, 2026-06-27).
2. **ðŸ”´ Spesa token dev**: item 1 roadmap â€” il budget cap runtime Ã¨ inerte sul free tier. La leva reale Ã¨ la disciplina dev (sez. 11): `/clear` tra task, Sonnet default, Opus on-demand.
3. **✅ Accesso dev tooling da telefono**: item 2 roadmap — CHIUSO (2026-07-15) via Remote Control (`/rc`): sonda su Giulia/WSL verificata live, nessun bridge custom necessario.
4. **FASE 3 â€” Interfaccia vocale**: Whisper STT + ElevenLabs TTS.
5. **FASE 4.5 â€” Task scheduler autonomo**: catalogo YAML task notturni (item 4 roadmap, prerequisito Jarvis).
6. **FASE 5 S1 ✅ e S1b ✅ completati (2026-07-04)** → prossimo S2 (decide operatore)
7. **Riserve review #38** (non bloccanti): R-tel-budget-perf (scan JSONL crescente), R-tel-tool_res (cosmetic).

### PARK â€” registrati, nessun impegno
- Retention del diario (archiviazione/export, MAI DELETE â€” quando il volume lo richiederÃ ).
- GDPR / dati personali lead: da guardare a FASE 4.
- SSH + tmux come via di accesso al dev tooling da telefono (item 2 roadmap): registrato come alternativa a Dispatch, nessun impegno. Da riprendere SOLO se la sonda Dispatch fallisce. Caveat di sicurezza da valutare prima di qualsiasi implementazione: esporre una sessione tmux con Claude Code = superficie RCE sulla box di sviluppo/repo; richiede design a fiducia mono-direzionale e autenticazione separata.

## Istituzioni di processo

- **A** â€” `reports/stato_progetto.md` (questo file): stato vivo, aggiornato a fine task.
- **A-arch** â€” `reports/stato_storico.md`: storico sessioni + finding chiusi + dettaglio motore.
- **B** â€” `reports/diff_sessione.md`: diff della sessione corrente (riscritto a ogni sessione).
- **C** — `.claude/agents/revisore.md`: gate obbligatorio pre-commit motore. **55 review**. Ultima: **#55** (fix/ci-hook-tests atomici + T-hook-h, 2026-07-18, APPROVATO CON RISERVE). Lezioni in `.claude/agents/memoria_revisore.md`. ⚠️ Backfill #48–#50 = PENDENTE (richiede WSL locale). Da #51 in poi il file è nel formato canonico `#N — YYYY-MM-DD — verdetto — lezione`. ⚠️ Nota data #55: la riga in `memoria_revisore.md` porta data 2026-07-18 ma la sessione ha lavorato su commit del 2026-07-17 (data di sistema post-mezzanotte); data lasciata com'è nel file per coerenza col contatore, incoerenza segnalata qui.
- **D** â€” `reports/handoff.md`: dossier di fine sessione (DECISIONI UMANE + diff stat + log + delta test + verdetto revisore + stato CI).
- **D-cmd** — `.claude/commands/fine-task.md`: template `/fine-task`. **BASE = `git merge-base origin/main HEAD`** (non più “last handoff commit”), preceduto da `git fetch origin` obbligatorio e con guard bloccante se il merge-base è vuoto (fix 2026-07-15, branch `fix/fine-task-base-mergebase`). §1 SCOPE & ESITO FETTE obbligatorio (FATTA/SALTATA/DEFERITA). **Caveat residuo**: la correttezza di `${BASE}` dipende dalla freschezza di `origin/main` — il `git fetch` copre il caso normale, ma se la PR viene mergiata sul remoto DOPO il fetch, `${BASE}..HEAD` può ancora includere commit non di sessione. Non chiuso al 100%: mitigato.

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
   - ✅ Remote Control locale verificato (2026-07-15): `cd ~/Gas && claude` + `/rc` → QR → app. CAVEAT OPERATIVO: la sessione eredita la cwd del lancio — lanciare SEMPRE da ~/Gas. CAVEAT SESSIONI: in app, ☁️ = Claude Code cloud (no bwrap, non canonico), icona computer+verde = Giulia locale. Non confonderle: un task bwrap in cloud dà falso verde. Confine invariato: da telefono solo doc-only + motore non-sandbox; bwrap solo locale/CI.
7. **⚠️ STANTIA — postazione locale WSL** (aggiornata 2026-07-18): venv era ASSENTE al 2026-07-17, ricreato con `python3 -m venv venv` (Python 3.12.3 — NON 3.11 come dichiarato altrove in CLAUDE.md); contiene SOLO pytest 9.1.1 da `requirements-dev.txt` → dipendenze del motore NON installate, suite kernel su WSL NON eseguibile finché non si fa `pip install -r requirements.txt`. jq era ASSENTE, installato a mano (jq-1.7, 2026-07-17). Chiave SSH `id_ed25519` con PASSPHRASE senza ssh-agent → hook non-interattivi NON possono pushare: auto-push di `session_end.sh`/`scrivi_rep.sh` è INERTE su WSL, il push va fatto a mano. Tutte azioni manuali senza traccia in git: registrate qui.
8. **✅ S1 ESEGUITO (2026-07-04):** hardening SSH + utente runtime completati sul VPS CX33.
   - unattended-upgrades: attivo (running)
   - fail2ban: attivo, jail sshd, backend=auto, 4 IP bannati al reboot
   - Utente `gas` (uid=1000): creato, `/home/gas/gas/` copia working dir, `/home/gas/.cache/` model cache fastembed
   - sshd hardening: `PasswordAuthentication no`, `PermitRootLogin no`, `PubkeyAuthentication yes` (dropin `/etc/ssh/sshd_config.d/99-hardening.conf`)
   - Kernel aggiornato: 6.8.0-134-generic (reboot post-S1 ok)
   - `/root/gas/` INTATTO (non cancellare fino a S1b confermato)
   - Accesso SSH: solo `gas@204.168.251.92` via chiave ed25519. Login root SSH disabilitato.
9. **S1b ✅ (2026-07-04):** swap file 2GiB attivo (cuscinetto anti-OOM, vedi finding no-swap sopra); unit systemd `/etc/systemd/system/gas.service` con `User=gas`, `MemoryHigh=1500M`, `MemoryMax=2000M`, `Restart=always`; `.env.prod` in `/home/gas/gas/.env.prod` con permessi `chmod 600`; servizio attivo confermato. Data di misura RAM a regime del singolo modello: non registrato.



- ⚠️ **Nota di processo — scope creep sessione 2026-07-08**: fetta concordata = migrazione Groq; fuori mandato: (1) chiuso R-groq-dup (era deferito a slice separata), (2) toccato CLAUDE.md, (3) toccato runbook_s1. Esito tecnico corretto (review #44), ma lo scope lo decide l'operatore: registrata recidiva dell'anti-pattern. Mitigazione strutturale: ruleset `main-lock` attivo dal 2026-07-09 (no push diretto su main, CI `unit-suite` required, self-merge).
- ℹ️ **Micro-finding di processo — handoff diff --stat riciclato** (2026-07-13): il `diff --stat` nel handoff era riciclato dalla sessione precedente, non rigenerato — svista di copia; log/conteggio/CI erano coerenti. Nota: Claude Code rigeneri sempre `git diff --stat` reale nel handoff, mai riciclarlo.
- ℹ️ **Micro-finding di processo — PR #14 mergiata senza revisione** (2026-07-15): la PR #14 è arrivata su main senza il passaggio di revisione previsto dal protocollo. CI verde, nessun danno rilevato al contenuto, ma il gate è stato saltato: registrato come recidiva della classe "gate saltato perché il cambio sembrava piccolo". Nessuna azione correttiva sul merito; la lezione è che il gate non si valuta a occhio sulla dimensione del diff.
- ℹ️ **Micro-finding di processo — verdetto revisore parafrasato sotto etichetta 'INTEGRALE'** (2026-07-16, handoff F1 R-crm-diario-rr): il verdetto della review #49 era riportato in discorso indiretto ma marchiato 'INTEGRALE'. Un riassunto etichettato come verbatim è peggio di un riassunto dichiarato: rende non verificabile il gate. Regola dal 2026-07-16: il verdetto del revisore va copia-incollato VERBATIM in ultimo_report.md e in handoff.md.
- ℹ️ **Micro-finding di processo — test modificato post-review senza ri-review** (2026-07-16, PR #18): la review #49 vide il test T19f-rr nella versione con connessione raw (riserva sollevata). Il test fu aggiornato in-session a usare `m._connect()` e committato in `894eb06` senza un secondo verdetto esplicito del revisore. Evidenza: handoff PR #18 riporta un solo verdetto (#49 APPROVATO CON RISERVE); nessun 'APPROVATO' finale post-aggiornamento. Gate formalmente non chiuso sull'aggiornamento. Regola dal 2026-07-16 (già nel prompt di sessione): se si applica una modifica richiesta dal revisore, RI-INVOCARE il revisore sul nuovo diff e riportare ENTRAMBI i verdetti verbatim.
- ℹ️ **Nota di processo — review #49 in commit locale non pushato** (2026-07-16): la lezione di review #49 (2026-07-16) era stata aggiunta a `memoria_revisore.md` dall'hook auto-commit SessionEnd nel commit `92a08ba`, ma quel commit è rimasto solo su `local/main` (main-lock ha bloccato il push diretto). Su `origin/main` il file termina ancora a review #47. Proposta: aggiungere la riga di review #49 a `memoria_revisore.md` nel prossimo commit doc o PR.
- ✅ **R-crm-diario-rr CHIUSO con PR #18** (2026-07-16): confermato da `git log origin/main` — `fe0e476 Merge pull request #18 from Gasss23/fix/diario-recursive-triggers` è su main. Finding chiuso.
- ℹ️ **Guard SessionEnd main-lock/detached HEAD** (2026-07-16, branch `docs/hook-guard-session-end`): aggiunto in cima a `.claude/hooks/session_end.sh` un guard bloccante — se HEAD è su `main` o detached, hook stampa warning su stderr e esce senza commit. Test T-hook-a/b/c su repo git reali: 3/3 PASS. Revisore: APPROVATO (#51). PR #20 su main (fbf8246, CI run 29487631549 ✅).
- ℹ️ **Obbligo riga-per-review in revisore.md** (2026-07-16, stessa PR): sezione "DOPO ogni review" di `.claude/agents/revisore.md` riscritta — obbligo esplicito di aggiungere UNA riga contatore dopo OGNI review (formato `#N — YYYY-MM-DD — verdetto — lezione`), anche se la lezione è "nessuna lezione nuova". Il file è il contatore canonico: un buco lo rende indifendibile.
- ℹ️ **Hook push su branch corrente** (2026-07-16, PR #21 `fix/hook-push-ref`): `session_end.sh` riga 60 e `scrivi_rep.sh` riga 47 pushavano su `main` hardcoded con `2>/dev/null||true`. **RISOLTO → merge 8f9cf7b su main ✅ (2026-07-16, CI run 29505642515 SUCCESS)** (la run CI non esegue i test hook — vedi R-ci-hooks). Fix: push su `HEAD:"refs/heads/$_cur_branch"` + warning esplicito su stderr + exit 0. **CAMBIO DI COMPORTAMENTO**: prima del fix il push era de facto inerte (main-lock respingeva `push origin main`); ora l'hook pusha davvero il branch di sessione su origin a ogni SessionEnd — commit di report/doc che prima morivano in locale ora arrivano su origin e possono innescare run CI sui branch. Revisori: #52 APPROVATO CON RISERVE (Fetta 1), #53 APPROVATO CON RISERVE (Fetta 2), #54 APPROVATO CON RISERVE (Fetta 3).
- ℹ️ **git add fragile su pathspec assenti** (2026-07-16, PR #21 `fix/hook-push-ref`): `git add reports/ '*.md' .gas_history.json` — se `.gas_history.json` assente, git esce 128 e non staggia nulla. **RISOLTO → merge 8f9cf7b su main ✅ (2026-07-16, CI run 29505642515 SUCCESS)** (la run CI non esegue i test hook — vedi R-ci-hooks). Fix: lista dinamica dei pathspec; solo quelli che matchano almeno un file vengono inclusi.
- ✅ **Riserve hook #52–#54 RISOLTE su branch** (chiuse in fix/ci-hook-tests, verdetto #55): (a) pattern `_cur_branch="$(...)"; if [ $? -ne 0 ]` fragile in `scrivi_rep.sh` → RISOLTA in `f6d7a62` (forma atomica su entrambi gli hook, allineata a lezione #51); (b) test guard main-lock mancante su `scrivi_rep.sh` [riserva #54(2)] → RISOLTA in `721ef9f` (T-hook-h). Confermato dal verdetto #55.
- ⚠️ **Backfill memoria_revisore.md #48–#50 PENDENTE** (2026-07-16): il commit `92a08ba` (lezioni #48–#49) è solo su `local/main` (WSL), non pushato, non raggiungibile da Codespace. Ricostruzione a memoria = vietata. Eseguire il backfill dalla postazione WSL locale (cherry-pick o re-aggiunta riga) in una sessione separata con accesso alla macchina locale. Fino ad allora `memoria_revisore.md` su origin/main inizia a #51 (questo branch) dopo una lacuna #48–#50.

### DA FARE — sviluppo/processo (aperti dal 2026-07-09)
- ✅ **gh CLI installato su Giulia** — 2026-07-14: v2.96.0, git protocol HTTPS, account Gasss23, scopes repo+workflow. Verificato: `gh repo view Gasss23/Gas` OK, branch main visto. CHIUSO.
- ✅ **WSL locale riallineato a origin/main** — 2026-07-15: eseguito a mano da terminale WSL (`git fetch` + `checkout main` + `merge --ff-only`), `/home/gqual/Gas` ora a `9cbab56`; branch locale esaurito `docs/roadmap-item2-chiuso` cancellato (`-d` accettato = già dentro main). Registrato qui perché un allineamento manuale NON lascia traccia in git. CHIUSO.
- ℹ️ **Nomenclatura ambienti — clone Windows eliminato** (2026-07-15): esisteva un SECONDO clone del repo su `C:\Users\gqual\Gas` (PowerShell) oltre a quello WSL, in contraddizione con la regola "non esiste un locale separato dal WSL". Ha già prodotto un incidente: un allineamento eseguito sul clone sbagliato da un branch morto (`docs/cerebras-no-go`) scambiato per main. Deciso ed eseguito: clone Windows RIMOSSO, `~/Gas` su WSL (`/home/gqual/Gas`) è l'UNICO locale canonico. Se ricompare un clone Windows, è un errore da rimuovere: due cloni divergono in silenzio e la memoria comincia a mentire.
- ℹ️ **Debito Codespace** (2026-07-18): il Codespace ha lo stesso branch `fix/ci-hook-tests` con lo stato di una sessione interrotta (modifiche sporche mai committate). Due ambienti sullo stesso branch divergono in silenzio (cfr. incidente clone Windows). Bonificare o eliminare in sessione dedicata.
