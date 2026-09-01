# STATO PROGETTO GAS

> Fotografia viva dello stato. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-09-01** (sonda/e2e-calcola-gemini-2026-09-01 — run 2: sonda E2E calcola() Gemini **2 PASS** confermati su run fresca. `calcola(7*8)→56`, `calcola(math.sqrt(144))→12.0`. Brain: `gemini-2.5-flash-lite` (rung 1). Zero codice toccato. Report: `reports/ultimo_report.md`.) — Precedente: run 1 stessa sessione 2 PASS.
> Storico sessioni, dettaglio componenti, finding chiusi: `reports/stato_storico.md`

## Stato motore

FASE 1 ✅, FASE 2 ✅ e **FASE 2.5** ✅ chiuse. **94 review** completate (ultime: #94 = calcola() anti-DoS APPROVATO; #93 = prompt hardening + calcola() APPROVATO CON RISERVE; #92 = R-phantom-pr-1 APPROVATO CON RISERVE; #91 = Fetta 4a client vocale APPROVATO CON RISERVE; #90 = BOCCIATO). Suite WSL locale (2026-08-29): **299 PASS, 0 FAIL** (+7 nuovi T62l-T62p anti-DoS). Hook suite: **14 PASS**. Voice suite: **19 PASS**. ⚠️ **ERRORE DICHIARATO**: la riga "Suite WSL locale (2026-07-19): 247 PASS, 0 FAIL, 2 SKIP" era FALSA — al 2026-07-19 il venv WSL conteneva SOLO pytest e la suite kernel NON era eseguibile su WSL (dipendenze motore assenti; vedi §7). Il falso accertato è che NON venivano da WSL; l'origine di quei numeri è NON VERIFICATA (ipotesi CI/Codespace, mai confermata da un artefatto). Corretta con dati reali di oggi.
**✅ FASE 3 Fetta 1 — endpoint HTTP voice** (2026-08-13, review #76+#77 APPROVATO, branch `fase3/voice-endpoint`, PR #62 — atterrata su main già con PR #63 loopback exemption): `modules/voice/server.py` — `POST /voice`, auth bearer `hmac.compare_digest`, fail-closed su token assente, kernel singleton, fail-safe §9. Suite: **18 PASS**. Zero nuove dipendenze. Stop gate rispettati (gas.py non toccato).
**✅ FASE 3 Fetta 2 — STT server-side Groq Whisper** (2026-08-20, review #88 APPROVATO CON RISERVE, branch `feat/voice-stt-input`): `modules/voice/stt.py` (nuovo) + `modules/voice/server.py` (routing audio). POST /voice ora accetta `audio/*` e `multipart/form-data` — trascrizione via Groq `whisper-large-v3`, zero nuove dipendenze (http.client stdlib). Retrocompatibilità JSON invariata. Fail-closed: chiave assente → 503, audio vuoto → 400, Groq 400 → 400, Groq 4xx/5xx → 502, rete → 502. Test end-to-end reale: `probe_tts_output.mp3` → `"Ciao, sono Gus, il tuo assistente vocale."`. Suite: **47 PASS** (+28 nuovi TVA). R-stt-1 risolta prima del commit (json.JSONDecodeError avvolto in GroqSTTError). CAVEAT: audio utente esce verso Groq (terza parte) — egress dati vocali dichiarato in docstring server.py.
**🔍 SONDA ambiente client vocale FASE 3 (2026-08-21, branch `sonda/voice-client-env`)**: ricognizione pura Giulia/WSL. Audio: WSLg v1.0.73 build 2 attivo, socket `unix:/mnt/wslg/PulseServer`, play→Windows testato con ffmpeg (exit 0). Librerie: zero Python audio libs nel venv; ffmpeg 6.1.1 (`--enable-libpulse`) unica via senza installazioni. D1-ter: IP WSL dinamico; `localhost:8765` stabile via WSL2 forwarding (default). Design client fette 4a (script WSL+ffmpeg) e 4b (HTML5 browser) proposto in reports/ultimo_report.md — nessun codice scritto, decisione fetta all'operatore.
**✅ FASE 3 Fetta 4a — client vocale di prova (2026-08-21, review #91 APPROVATO CON RISERVE, branch `feat/voice-client-4a`)**: `clients/voice/probe_client_4a.py` (203 righe) — pipeline mic (PulseAudio) → ffmpeg WAV → POST /voice (auth bearer) → MP3 → ffmpeg playback. Due modalità: audio (default, Accept: audio/mpeg) e `--text-only` (debug, Accept: application/json). Stdlib + subprocess ffmpeg, zero nuove dipendenze. Test E2E reale Giulia/WSL: mic → 157-174 KB WAV → Groq Whisper STT → GasKernel → ElevenLabs TTS → 281 KB MP3 → PulseAudioRDPSink (exit 0, audio uscito dagli altoparlanti). Stop gate rispettato (gas.py/modules/ non toccati). Riserva aperta: R-client4a-1 (eccezioni di rete non gestite in main(), non bloccante per usa-e-getta).
**⭐ ATTESTATO DAL SUPERVISORE (2026-08-22) — prova a VOCE UMANA REALE superata (WSL)**: mic→STT→kernel→TTS→casse. text-only: STT ha reso `'sette per otto'` → `'7×8'`. audio: `200 audio/mpeg`, MP3 riprodotto, giro completo. Debito 4a "Gas capisce il parlato" CHIUSO. Gate per 4b APERTO. (Test manuale fuori repo, non verificato da Claude Code.)
**✅ FASE 3 Fetta 3 — TTS output ElevenLabs** (2026-08-20, review #89 APPROVATO CON RISERVE, branch `feat/voice-tts-output`): `modules/voice/tts.py` (nuovo) + `modules/voice/server.py` (output audio). POST /voice con `Accept: audio/mpeg` (o `audio/*`) risponde con byte MP3 ElevenLabs Flash; senza header → JSON invariato. Env: `ELEVENLABS_API_KEY` (obbligatoria), `ELEVENLABS_VOICE_ID` (default: `JBFqnCBsd6RMkjVDRZzb` George premade). Fail-closed: chiave assente → 503, testo vuoto → JSON 200 senza chiamata, ElevenLabs error → 502, rete → 502. Zero nuove dipendenze (stdlib). Suite: **64 PASS** (+17 TVT). E2E reale: 88.2 KB MP3 (ID3 v2.4, MPEG layer III, 128 kbps, 44.1 kHz). R-tts-1 tracciata (cap testo implicito). CAVEAT: testo kernel esce verso ElevenLabs (terza parte) — egress dichiarato.
**✅ Design fix session-end (2026-08-19, review #82 APPROVATO CON RISERVE, branch `fase4/check-verdetto-fail-closed`, PR #64)**: `session_end.sh` non committa più — solo push fail-safe condizionale. `fine-task.md` passo 4 include ora `memoria_revisore.md` + `.gas_history.json`. Suite hook: **14 PASS**. Trade-off dichiarato (senza etichetta R2 — R2 = memoria revisore, CHIUSO da PR #66+#87): sessione interrotta prima di `/fine-task` non persiste `.gas_history.json`. Vedi finding autonomo in §Finding aperti.
**✅ fix core.quotePath non-ASCII — check_handoff + check_verdetto (2026-08-19, review #85 APPROVATO, branch `fix/quotepath-non-ascii`)**: `check_handoff.py:_diff_names` e `check_verdetto.py:_session_files` usano ora `git -c core.quotePath=false diff --name-only`. Fix per-invocazione (non globale). 2 test reali nuovi (`test_nonascii_filename_check_handoff`, `test_nonascii_filename_check_verdetto`) su repo temporanei reali. 11 PASS. Chiude riserva #84.
**✅ R2 durabilità memoria revisore — ricostruzione pulita (2026-08-19, review #86 APPROVATO CON RISERVE, branch `fix/r2-durabilita-memoria-clean`)**: `scripts/commit_memoria_revisore.sh` — commit path-scoped `git commit -o` di SOLO `memoria_revisore.md`, fail-safe §9 (WARN in gas_debug.log, exit 0 sempre). Cablaggio in `.claude/agents/revisore.md`. 4 test R2 in `tests/test_unit_hooks.py` (T-R2-a/b/c/d). STOP gate confermato: file quotePath identici a main. Riserve minori: R-r2-1 forma `$?` (fragile), R-r2-2 path "file presente + non-git" non coperto da T-R2-d. → **Riserve chiuse in fix/r2-riserve-86 (review #87 APPROVATO).**
**✅ Chiusura riserve R-r2-1 e R-r2-2 (2026-08-19, review #87 APPROVATO, branch `fix/r2-riserve-86`)**: R-r2-1 → forma atomica `if ! REPO_ROOT=$(cmd)` (lezione #51). R-r2-2 → test T-R2-e "mem PRESENTE + repo NON-git → git commit fallisce → WARN + exit 0" (copre path riga ~75 dello script). 19/19 PASS.
CI GitHub Actions — ultimi run su main (tutti ✅ SUCCESS; storico PR #23–#43 → `reports/stato_storico.md` § CI storica): PR #49 merge `64ff011` (2026-07-27, CI `30302270332`) · PR #48 merge `32a9a41` (2026-07-27, CI `30301777849`) · PR #47 merge `d67b12a` (2026-07-27, CI `30282530884`) · PR #46 merge `6f303cf` (2026-07-26, CI `30223085074`) · PR #45 merge `c7f6fac` (2026-07-25, CI `30160569148`) · PR #44 merge `de2f2f5` (2026-07-24, CI `30116369695`).

**✅ FASE 2.5 compressione history** (2026-06-27, review #39, commit 65c4c7b).
**✅ R-comp-1** — boundary piegato nel summary (2026-06-28, review #40, commit cde4d94). Caso degenere no-user coperto da T54.
**✅ gas version 0.2.0** (2026-07-01, review #41 APPROVATO, commit d992c47 → merge 2326404): `gas version` → stampa versione + Python, zero token LLM. Test T55. Nessuna lezione nuova per memoria_revisore.md.
**✅ Config-drift stringhe modello — CHIUSO** (2026-07-07, review #43, branch `refactor/model-ids-fonte-unica`: merge `eb0509f`, commit `160543a`): `brains/model_ids.py` = fonte unica dei 5 ID modello della cascata, env-overridabili (`GAS_MODEL_*`). Suite della sessione: **217 PASS incluso T56**. **Caveat suite**: quei 217 PASS sono stati ottenuti in Codespace, dove i test bwrap NON sono validabili (comportamento noto); la verifica bwrap reale resta demandata a CI/postazione WSL locale. **CI sul merge**: run ID **28874912495** (run n. 85, evento push su `eb0509f`, 2026-07-07) — **SUCCESS** ✅.

**Stato item roadmap (review #38, commit a8c6d53) — stato reale:**
- 🔴 **Item 1 — Controllo spesa token**: `_daily_cost_usd()` + kill-switch `GAS_DAILY_TOKEN_BUDGET` committati. Agiscono sul runtime GAS (Gemini/Groq free tier, costo ~0€). La spesa problematica (Claude Code dev su Opus) NON è tracciata in `.gas_tokens.jsonl` e NON viene intercettata. → **APERTO**: la disciplina dev (sez. 11 CLAUDE.md) resta l'unica leva reale.
- ✅ **Item 2 — Accesso da telefono**: `gas telegram` committato — interfaccia RUNTIME (GAS risponde all'utente via Telegram bot). Accesso al dev tooling da telefono risolto via Remote Control (`/rc`): sessione locale su Giulia/WSL raggiunta da telefono, lettura file reale del repo confermata, nessun bridge custom necessario. → **CHIUSO (2026-07-15)**.
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
- CLI `gas doctor` / `gas reindex` / `gas backup` / `gas tokens [N]` (contabilità token + stima USD + fallthrough) / `gas duplicati` (lista coppie CRM sospette, sola lettura)
- **Endpoint HTTP voice + TTS + client** (FASE 3 Fette 1+2+3+4a): `modules/voice/server.py` — `POST /voice`, bearer auth, kernel singleton, fail-closed; `modules/voice/stt.py` — STT Groq Whisper, routing audio/JSON; `modules/voice/tts.py` — TTS ElevenLabs Flash, risposta MP3; `clients/voice/probe_client_4a.py` — client prova mic→ffmpeg WAV→POST /voice→MP3→playback. ⭐ ATTESTATO DAL SUPERVISORE (2026-08-22): giro completo voce umana reale superato su WSL.
- **Budget cap** (review #38): `_daily_cost_usd()` + kill-switch `GAS_DAILY_TOKEN_BUDGET` in `run_turn`
- **Telegram bridge** (review #38): `gas telegram` → `modules/telegram/bot.py` (long polling, `TELEGRAM_BOT_TOKEN` + `TELEGRAM_ALLOWED_IDS`)
- **CLI vettori** (review #38): `gas calibrate-vectors` (distribuzione score → suggerisce min_sim) + `gas eval-vectors [query]` (ricerca semantica interattiva)
- **Compressione history** (review #39, FASE 2.5): `_compress_history_if_needed()` auto-trigger in `run_turn`; `gas compress-history` CLI. Env: `GAS_HISTORY_MAX_MSGS` (default 100), `GAS_HISTORY_KEEP_MSGS` (default 20). Zero token LLM.
- Telemetria fallthrough (review #33): `_log_tokens` con `event`/`reason`; doctor sez.10
- `VectorStore.disable_reason` (review #35/36): motivo disable propagato a `gas doctor`

## Pipeline provider (paracadute)

1. `gemini-2.5-flash-lite` → 2. `gemini-2.5-flash` → 3. `groq/openai/gpt-oss-120b`
   → 4. `openrouter` free (`meta-llama/llama-3.3-70b-instruct:free`)
   → 5. `ollama` offline (`qwen2.5:7b-instruct`, solo se `GAS_OLLAMA_URL` settata)

## Finding aperti (🟡 attivi)

> Chiusi in `reports/stato_storico.md` e `reports/finding_archiviati.md`.

- ✅ **R-phantom-pr-1 CHIUSO** (2026-08-22, sonda/phantom-pr-bug, review #92 APPROVATO CON RISERVE, PR #74): REGOLA §0 in `.claude/commands/fine-task.md` riscritta con gate bash obbligatorio — `gh pr list --head "$BRANCH" --base main --json number,url` eseguito dopo il push; PR assente → `gh pr create --fill`; gh exit non-zero → "PR NON verificata/creata" + task INCOMPLETO. Numero PR in §0 proveniente ESCLUSIVAMENTE da output JSON di `gh`. Riserve non bloccanti: R-finegat-1 (stderr misto nel JSON capture), R-finegat-2 (pattern non-atomico GH_EXIT).
- 🟡 **R-finegat-1** (2026-08-22, review #92): `PR_JSON=$(gh pr list ... 2>&1)` — warning stderr con exit 0 produce testo misto non-JSON; python3 lancia `json.JSONDecodeError` non catturata → §0 malformato senza segnale. Fix: `2>/dev/null` nella capture + try/except in python3.
- 🟡 **R-finegat-2** (2026-08-22, review #92): pattern `GH_EXIT=$?; if [ $GH_EXIT -ne 0 ]` non-atomico (lezione #51); sicuro nel contesto ma da allineare alla forma `if ! PR_JSON=$(gh pr list ...); then`.
- 🟡 **Esfiltrazione** — chiusa in `os_strict` con bwrap; in `os_with_fallback` resta 🟡.
- 🟡 **Degrado a solo-testo per-turno non rilevato** (R2 review #5): cold doctor (`sez.8`) già copre tutti i rami a freddo — sonda 2026-06-29 confermata, nessun gap. Il per-turno resta SILENZIOSO (warning in `gas_debug.log`, fail-safe §9). Rimandato per falsi positivi.
- **Riserve aperte residue (R-crm-1b archiviato)** — corpo completo archiviato in `reports/stato_storico.md` (§ Finding chiusi archiviati).
  - **R1** `int(r["id"])` fuori try/except (fetta 3, #67); **R2** ramo `chiave_norm` non coperto da T60 (#67); **R3** commento `# 11 CRM` fuori sequenza in gas.py (cosmetico, #68); **R4** T61d `or "Duplicati"` sempre vera — non asserisce strettamente "non disponibile" (#68).
- ℹ️ **Lezione T9b (2026-07-24)**: fino a questa sessione, in CI T9b era verde a vuoto. Senza chiavi, `if not os.environ.get(env): continue` in `run_turn` costruisce ZERO rung → il turno emette comunque "Pipeline esausta.": T9b passava testando "nessun provider configurato" (cascata a 0 rung), NON l'esaurimento del loop a 10 iterazioni. Con le chiavi fittizie iniettate per T9a/T9c, T9b diventa un test reale (3 provider × 10 iterazioni = 30 tool_res). **Principio**: un test verde non dimostra ciò che dichiara finché non si verifica quale ramo ha percorso.
- 🟡 **Riserve minori** (non bloccanti, dettaglio in archivio): R-test-1 cap_window_chars, R2 #6 chdir trap, R3 #4 falsi positivi path-check, riserve snapshot TASK C, riserve hook SessionEnd, riserve R-mem2a, riserve R-mem, R26-1/R26-2 backup.
- ✅ **R-voice-1** (review #76→#77): Content-Length non numerico → 400 — CHIUSA (fix applicata prima del commit: try/except ValueError in server.py:85-89).
- ✅ **R-voice-2** (review #76→#77): dead code in test_tv1 — CHIUSA (codice ripulito prima del commit).
- ✅ **R-voice-3** (2026-08-19, review #81 APPROVATO): test esplicito `Content-Length: abc → 400` aggiunto in `TestTVExtra.test_invalid_content_length_returns_400` — usa `http.client` direttamente per controllo totale degli header. CHIUSA.
- ✅ **R-stt-1** (review #88): `json.JSONDecodeError` avvolto in `GroqSTTError` — CHIUSA prima del commit.
- 🟡 **R-client4a-1** (review #91, non bloccante): in `probe_client_4a.py:main()`, eccezioni di rete (`ConnectionRefusedError`, `OSError`, `http.client.HTTPException`) non catturate → traceback non gestito se server offline. Accettabile per usa-e-getta; fix: aggiungere `except (OSError, http.client.HTTPException)` nel blocco finale di `main()`. Da valutare se lo script diventa permanente o template per 4b.
- 🟡 **R-tts-1** (review #89, non bloccante): nessun cap esplicito sul testo inviato a ElevenLabs. Il fail-safe regge (ElevenLabs 4xx/5xx → `ElevenLabsTTSError` → 502 controllato), ma il comportamento su testi lunghissimi è implicito. Da valutare in una fetta successiva o al deploy VPS.
- 🟡 **Rotazione chiave ElevenLabs prima del VPS** (ATTESTATO DAL SUPERVISORE, 2026-08-22): la chiave attuale è stata usata in sviluppo su WSL/chat di sessione. Prima del deploy VPS ruotare la chiave e usare solo quella nuova in produzione. Non bloccante sullo sviluppo WSL corrente; obbligatorio prima di S2. Cross-ref: sicurezza chiave esposta in chat 2026-08-02 (rischio accettato dall'operatore, ma rotazione-pre-VPS rimane azione obbligatoria separata).
- ✅ **kernel rifiuta 7×8 — CHIUSO per Gemini (sonda E2E 2026-09-01)**: con `GEMINI_API_KEY` presente, Gemini (`gemini-2.5-flash-lite`, rung 1) chiama `calcola(expr="7*8")` → 56 e `calcola(expr="math.sqrt(144)")` → 12.0 correttamente. Il finding era **Groq-specifico**: Groq non seguiva il system prompt per i calcoli aritmetici; Gemini lo segue. Sonda E2E 2 PASS su 2. Rif: `reports/ultimo_report.md` (2026-09-01). — Finding APERTO RESIDUO: comportamento Groq su `calcola()` resta non verificato; fix (se necessario) delegato all'operatore.
- 🟡 **R-verdetto-evidenza** — l'obbligo di citare ≥2 elementi del diff è verificabile solo a occhio; un verdetto può citare path:riga plausibili senza averli letti. Fix strutturale: check meccanico che i path:riga citati esistano nel diff sotto review. Non impegnato. **Cross-ref (stessa classe D)**: barriera solo disciplinare in attesa di enforcement strutturale/meccanico — identica alla famiglia dei gate "regola di forma" del progetto (main-lock rete = structural; revisore.md obbligo-evidenza = disciplinare). Il check specifico mancante: verificare automaticamente che ogni path:riga dichiarato nel verdetto esista davvero nel diff sottoposto.
- 🟡 **.gas_history.json runtime** — non persiste se la sessione muore prima di `/fine-task`. RUNTIME (kernel aggiorna il file a ogni turno sul VPS, mai auto-committato in prod); il revisore non lo tocca (non è codice motore). Competenza: `_take_snapshot` + decisione operativa (cron push/backup) da tarare al deploy VPS. NON chiuso da R2 (R2 = durabilità `memoria_revisore.md`, CHIUSO da PR #66+#87).
- **Riserve aperte residue (R-gasmerge-failopen archiviato)** — corpo completo archiviato in `reports/stato_storico.md` (§ Finding chiusi archiviati).
  - ✅ **#65-R1** (chiuso 2026-07-30, PR #56): guard `[ -n "$NEW_HEAD" ]` aggiunto post-conferma. Il guard HEAD_SHA (prima cattura) era già in place; il caso NEW_HEAD post-prompt era il missing piece.
  - ✅ **#65-R2** (chiuso da main PR #57 + review #69/#70): `--match-head-commit` test positivo end-to-end aggiunto in `TestTOCTOUPositive`. Il fix era su main prima del rebase di fix/gasmerge-hardening.
  - ✅ **#65-R3** (chiuso 2026-07-30, PR #56 + rebase): `mktemp /tmp/gaspr.XXXXXX.json` per-run + `export GASPR_JSON` + `trap EXIT`. Stub ereditano la variabile. Rebase: stub `_make_stub_gh_recording_merge` di PR #57 convertito da `/tmp/gaspr.json` hardcoded a `"$GASPR_JSON"` (revisione #71).
  - ✅ **#63-R1** (chiuso 2026-07-30, PR #56): `shutil.which("git")` in Python risolve il git reale prima che fake_bin sia preposta a PATH.

### DEPLOY VPS — fotografia sonda 2026-08-26

**Sonda read-only eseguita 2026-08-26.** Dati verbatim in `reports/ultimo_report.md`.

| Metrica | Valore |
|---|---|
| Servizio | `gas.service` active (running), enabled |
| Uptime attuale | dal 2026-08-25 17:00:04 UTC (riavvio post-boot) |
| PID | 853 — `gas.py telegram` |
| RAM service | 123.9 MB (peak 124.6 MB) vs limite 1.4/1.9 GB |
| RAM sistema | 502 MB / 7.6 GiB (7%) |
| Swap | 2 GiB, 0 usata |
| Disco | 4.9 GB / 75 GB (7%) |
| Python VPS | 3.12.3 |
| Commit VPS | `f3a8acc` (2026-06-29) |
| origin/main HEAD | `8a946c6` (2026-08-25) |
| Commit totali dietro | 391 |
| Commit motore dietro | 17 (FASE 3 completa mancante) |
| `.gas_memory.db` | 53248 bytes, aggiornato 2026-08-25 17:01 |
| `.gas_history.json` | 124 righe, fermo a 2026-07-06 (nessun turno reale) |
| Errori log | Solo timeout Telegram (long-polling normale) |

**Nota**: il VPS gira stabile su codice FASE 2 completa + fix pre-voice. FASE 3 (voice endpoint, STT, TTS, client 4a) non è deployata — da portare a S2.

### DEPLOY VPS — da tarare su dati reali

- 🟡 **R-reidx-3** — picco RAM `reindex` su diario grande: **RIDOTTO** (review #30, 2026-06-25): `ricostruisci_da_diario` usa batch paginati (`diario_dopo`) — numpy transitori per batch (~400KB), accumulo blob proporzionale all'intero diario (~1.5KB/riga). Su CX33 8GB gestibile; chiusura definitiva rinviata a ri-taratura su diario reale VPS.
- 🟡 **R-wire-1** (RESIDUO) — `VEC_MIN_SIM=0.30` tarata su esempi sintetici: ri-tarare sul diario reale del VPS. Env-config già fatto (review #28).
- 🟡 **RAM a regime del singolo modello** — `MemoryHigh=1500M`/`MemoryMax=2000M` in `gas.service` (S1b, 2026-07-04): misura reale non ancora registrata. Da rilevare su VPS con diario attivo prima di affinare i limiti systemd.
- ✅ **Verifica riserva evidenza F7 — CHIUSA (sonda 2026-08-26)**: `cat /home/gas/gas/.gitignore | head -5` eseguito su VPS — contiene `venv/`, `__pycache__/`, `*.pyc`, `logs/`, `*.bak`. NO `.venv/`. Il fix (`.venv/` gitignorato) è nel commit `1b03adc` su origin/main ma NON è deployato sul VPS (VPS stantio al 2026-06-29). `.venv/` appare come untracked (`?? .venv/`) nel git status VPS: comportamento atteso per VPS stantio, nessuna anomalia. F7 chiusa: evidenza raccolta, situazione nota e accettata fino a S2.

### Limiti noti (non-finding)

- **R-wire-2** — qualità semantica MiniLM limitata su query corte IT: limite di potenza, non correttezza. Legato a R-vec-3 (chiuso).

### Debito latente

- **Note minori — revisione Fable-5 (2026-07-15, nessuna azione impegnata)**: (a) logging su path RELATIVO `gas_debug.log` (segue la cwd, non la root: ok sotto systemd, log vagante se lanciato da altra dir); (b) messaggi di `_cap_tool_output` suggeriscono `sed -n` che l'allowlist nega (F4); (c) `classifica_compito`: ogni messaggio ≥60 char = "complesso" → salta spesso flash-lite (costo ~0 oggi); (d) il bot Telegram processa anche `edited_message` (ri-editare un vecchio messaggio lo ri-esegue; innocuo con whitelist); (e) commento prezzi Gemini in gas.py datato 2025-06 (allineare alla prossima occasione); (f) CLAUDE.md sez.2 descriveva cascata e Core Files non più reali (corretto nella fetta 2 di questa PR).

> ℹ️ **TPM burst gpt-oss-120b** — limite TPM 8K (vs 12K del precedente llama-3.3-70b-versatile). Fallthrough a OpenRouter più frequente in caso di burst = comportamento atteso, non regressione.

### Decisione bancata — Cerebras zai-glm-4.7 free (sonda 2026-07-13)

NO-GO come rung-4. Due limiti bloccanti per paracadute h24 non presidiato:
1. Cap contesto free tier = **8192 token** misurato live (doc dichiara 64k — falso). Insufficiente per system + pin + schema + window.
2. Coda free satura — 429 queue_exceeded a orari diversi. Disponibilità non garantita.
Rung-4 resta OpenRouter. Ri-valutabile solo su tier a pagamento (131k, no coda) = decisione di budget separata.
Prossimo candidato eventuale: Mistral (sonda data-policy prima dei lead CRM).
## Prossimi passi (in ordine di priorità)

1. ~~**FASE 2.5**~~ ✅ chiusa (review #39, 2026-06-27).
2. **🔴 Spesa token dev**: item 1 roadmap — il budget cap runtime è inerte sul free tier. La leva reale è la disciplina dev (sez. 11): `/clear` tra task, Sonnet default, Opus on-demand.
3. **✅ Accesso dev tooling da telefono**: item 2 roadmap — CHIUSO (2026-07-15) via Remote Control (`/rc`): sonda su Giulia/WSL verificata live, nessun bridge custom necessario.
4. **FASE 3 — Interfaccia vocale**: Fette 1+2+3+4a ✅ su main. ⭐ ATTESTATO DAL SUPERVISORE (2026-08-22): prova vocale umana reale superata su WSL. Gate per fetta 4b APERTO (client browser HTML5 — decisione operatore).
   - ✅ **Sonda F0 atterrata su main (2026-08-02, PR #59, merge 5323b9b)**: 6 script in `clients/voice/probe/` (client Windows↔WSL).
   - ✅ **Fette 1+2+3+4a chiuse**: pipeline mic→STT Groq→kernel→TTS ElevenLabs→MP3 completa e testata E2E su WSL. Vedi Stato motore §FASE 3 per dettaglio.
   - 🟡 **Fetta 4b** (client browser HTML5): non impegnata — decisione operatore.
5. **FASE 4.5 — Task scheduler autonomo**: catalogo YAML task notturni (item 4 roadmap, prerequisito Jarvis).
6. **FASE 5 S1 ✅ e S1b ✅ completati (2026-07-04)** → prossimo S2 (decide operatore)
7. **Riserve review #38** (non bloccanti): R-tel-budget-perf (scan JSONL crescente), R-tel-tool_res (cosmetic).

### PARK — registrati, nessun impegno
- Retention del diario (archiviazione/export, MAI DELETE — quando il volume lo richiederà).
- GDPR / dati personali lead: da guardare a FASE 4.
- SSH + tmux come via di accesso al dev tooling da telefono (item 2 roadmap): registrato come alternativa a Dispatch, nessun impegno. Da riprendere SOLO se la sonda Dispatch fallisce. Caveat di sicurezza da valutare prima di qualsiasi implementazione: esporre una sessione tmux con Claude Code = superficie RCE sulla box di sviluppo/repo; richiede design a fiducia mono-direzionale e autenticazione separata.

## Istituzioni di processo

- **A** — `reports/stato_progetto.md` (questo file): stato vivo, aggiornato a fine task.
- **A-arch** — `reports/stato_storico.md`: storico sessioni + finding chiusi + dettaglio motore.
- **B** — `reports/diff_sessione.md`: diff della sessione corrente (riscritto a ogni sessione).
- **C** — `.claude/agents/revisore.md`: gate obbligatorio pre-commit motore. **92 review**. Ultima: **#92** (R-phantom-pr-1 APPROVATO CON RISERVE — 2026-08-22). **#91** = Fetta 4a client vocale APPROVATO CON RISERVE (2026-08-21). **#90** = BOCCIATO (2026-08-20). **#89** = TTS ElevenLabs APPROVATO CON RISERVE (2026-08-20). **#88** = STT Groq Whisper APPROVATO CON RISERVE (2026-08-20). Fonte contatore: numero più alto citato in `.claude/agents/memoria_revisore.md`. ⚠️ Il file NON è un registro completo per-review: l'obbligo "una riga per ogni review" è in vigore solo dal 2026-07-16 (#51). Conseguenza: NESSUN conteggio automatico è difendibile — metodi diversi danno risultati diversi. Gli unici dati verificabili sono: numero più alto citato = `#77`; entries contigue SOLO da `#51` a `#77`. Sotto `#51` il file è un log di lezioni, non un registro. Il conteggio "77 review" è ereditato dallo storico e NON è ricostruibile dal file: contare per validarlo è un metodo INVALIDO. Lezioni in `.claude/agents/memoria_revisore.md`. ✅ Backfill #48–#50 ESEGUITO (2026-07-18, PR #24). ℹ️ **Collisione #62 riconciliata** (2026-07-26): sessioni parallele avevano prodotto due entry #62 da #61; riconciliate al merge con branch #62/#63 intatti e main #62 rinumerata in #64. ℹ️ **Collisione #69 riconciliata** (2026-07-31): branch fix/gasmerge-hardening aveva aggiunto #69 (gasmerge.sh hardening) collidendo con #69/#70 di main; rinumerata in #71 al rebase. ℹ️ **Collisione #74+#75 riconciliata** (2026-08-19): branch fase3/voice-endpoint e main avevano usato in modo indipendente i numeri #74 e #75; le review voice rinumerate #76+#77 al merge.
- **D** — `reports/handoff.md`: dossier di fine sessione (DECISIONI UMANE + diff stat + log + delta test + verdetto revisore + stato CI).
- **D-cmd** — `.claude/commands/fine-task.md`: template `/fine-task`. **BASE = `git merge-base origin/main HEAD`** (non più “last handoff commit”), preceduto da `git fetch origin` obbligatorio e con guard bloccante se il merge-base è vuoto (fix 2026-07-15, branch `fix/fine-task-base-mergebase`). §1 SCOPE & ESITO FETTE obbligatorio (FATTA/SALTATA/DEFERITA). **Caveat residuo**: la correttezza di `${BASE}` dipende dalla freschezza di `origin/main` — il `git fetch` copre il caso normale, ma se la PR viene mergiata sul remoto DOPO il fetch, `${BASE}..HEAD` può ancora includere commit non di sessione. Non chiuso al 100%: mitigato.

## Regole operative vive

> Estratte dal testo delle sessioni. Per merito e contesto completo, vedi la sezione d'origine citata.

- **R1** (2026-07-22) — Esegui il merge su main SEMPRE a mano da WSL con `gasmerge <PR>`; MAI `gh pr merge` da dentro una sessione Claude Code. Vale anche per i doc-only.
  Origine: `### ℹ️ Micro-finding di processo — merge su main eseguito da dentro Claude Code (2026-07-22)`, riga "Regola dal 2026-07-22"; confermato `### Sessione 2026-07-23`, sezione SEQUENZA DI MERGE OBBLIGATORIA.

- **R2** (2026-07-22, rettificata 2026-07-23) — Rispetta la SEQUENZA DI MERGE OBBLIGATORIA: 1) apri la PR; 2) `/fine-task` nella STESSA sessione; 3) chiudi la sessione (Ctrl+D); 4) revisiona l'`handoff.md` PRIMA del merge (scope e merito li verifica solo l'operatore); 5) solo allora: `gasmerge <numero-PR>` in WSL.
  Origine: `### Sessione 2026-07-23 — allineamento canonici`, sezione "SEQUENZA DI MERGE OBBLIGATORIA".

- **R3** (2026-07-24) — Lancia SEMPRE `cd ~/Gas && claude`. La sessione eredita la cwd: da altra directory `.claude/agents/` non viene scoperto e il subagent revisore non esiste.
  Origine: `### Sessione 2026-07-24 — sanare venv`, sezione "Deviazione di gate — subagent revisore non invocato nativamente"; confermato nota VPS §6 e `### Sessione 2026-07-24 (p2)`.

- **R4** (2026-07-16) — Incolla il verdetto del revisore VERBATIM in `ultimo_report.md` e `handoff.md`. Se applichi una modifica richiesta dal revisore, RI-INVOCA il revisore e riporta ENTRAMBI i verdetti verbatim.
  Origine: micro-finding "verdetto revisore parafrasato sotto etichetta 'INTEGRALE'" + micro-finding "test modificato post-review senza ri-review" (entrambi 2026-07-16).

- **R5** (rilevato 2026-07-13, fix strutturale 2026-07-24) — In `handoff.md`, rigenera SEMPRE `git diff --stat` con `git diff --cached --stat ${BASE}` DOPO `git add`; non riciclarlo da sessione precedente.
  Origine: micro-finding "handoff diff --stat riciclato" (2026-07-13); fix strutturale `### Sessione 2026-07-24 (p2)`.

- **R6** (2026-07-22) — La cancellazione di branch remoti è azione UMANA, MAI da sessione agente.
  Origine: `### DA FARE — sviluppo/processo`, riga ⛔ nella sezione "Bonifica branch remoti ESEGUITA".

- **R7** (2026-07-21) — Per SSH al VPS: esegui `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519` a inizio sessione (la chiave HA passphrase). Distinto dal push git (HTTPS, no passphrase).
  Origine: `### Sessione 2026-07-21`, ℹ️ "Chiave SSH del VPS ha passphrase"; confermato `### Sessione 2026-07-22`.

- **R8** (2026-07-22) — `Permission denied (publickey)` NON è evidenza di chiave mancante. Prima di qualsiasi diagnosi: `ssh -v` e `ssh-add -l`.
  Origine: `### Sessione 2026-07-22`, rettifica "ACCESSO SSH AL VPS PERSO era una DIAGNOSI ERRATA".

- **R9** (2026-07-22) — `passwd -l gas` blocca anche `sudo` con password per l'utente gas. Le operazioni admin sul VPS passano da root/console.
  Origine: `### Sessione 2026-07-22`, ⚠️ "CAMBIO DI COMPORTAMENTO".

- **R10** (2026-07-24) — `~/bin/gasmerge` DEVE essere un symlink a `scripts/gasmerge.sh` (verifica con `ls -l`). Una copia divergente significa che il gate versionato non è quello che gira.
  Origine: `### Sessione 2026-07-24 (p2)`, 🔴→✅ "~/bin/gasmerge NON era un symlink"; ℹ️ "gasmerge portato in scripts/gasmerge.sh".

## Note operative VPS — non per oggi

> Registrate il 2026-06-15 (aggiornate 2026-07-02, sonda S0 + allineamento canonici + correttivo post-a15ff61: R-vec-3 ✅ chiuso, no-swap finding, req non-root specifico).

**Hardware confermato (sonda diretta 2026-07-02):** Hetzner **CX33** Helsinki — x86_64, 4 core, 7.6Gi RAM usabile (7.1Gi disponibile a vuoto), 70Gi disco liberi (NON CX22/4GB come da nota precedente errata).

🔴 **FINDING no-swap (sonda 2026-07-02):** il box NON ha swap (default Hetzner). Su 7.6Gi condivisi da OS + GAS+embedder + ollama 3B + bot trading demo, un picco = OOM killer SECCO (nessun cuscinetto) su macchina h24 non presidiata → viola "zero crash". Conseguenze:
- (a) La unit systemd di S1b DEVE settare `MemoryHigh`/`MemoryMax` su GAS (ordine di grandezza: `MemoryHigh ~1.5Gi`, `MemoryMax ~2Gi` — GAS+embedder stanno <1Gi a regime, il margine copre i picchi di reindex; da affinare a S1b con misura reale). Scopo: se qualcosa sfonda, GAS degrada/riparte in modo prevedibile via `Restart=always` invece di innescare un OOM che colpisce il bot trading.
- (b) Ollama "3B always-on" da RIVALUTARE → probabile on-demand (spawn quando la cascata arriva a ollama, unload dopo) o modello 1-1.5B se always-on, causa RAM limitata + no-swap. Decisione a S3, qui solo registrata come aperta.
- (c) ✅ **SUPERATA — ESEGUITA a S1b (2026-07-04)**: swap file **2GiB** attivo sul VPS
  (vedi punto 9 di questa sezione). L'opzione era "da valutare" al 2026-07-02; la
  decisione è stata presa e applicata. Riga riconciliata il 2026-07-28 (era rimasta
  "Non decisa" per 24 giorni dopo l'esecuzione).

1. **Snapshot**: 0 ref in dev è ATTESO (il runtime GAS non gira qui). Sul VPS gli snapshot nasceranno da `run_command`/`write_file` → se doctor sez.7 mostrasse 0 ref sul VPS sarebbe anomalo. ~4427 oggetti loose = detrito git (stash/churn), non snapshot; `git gc` OPT-IN li riassorbe.
2. **OpenRouter free ~28s**: rung lento, paracadute non piano operativo. Ollama locale = pavimento rapido a costo zero. **Modello ollama per VPS: 3B (es. `qwen2.5:3b-instruct`), NON 7B** — gli 8 GB sono condivisi da GAS + embedder fastembed (~500 MB model cache) + bot trading demo coabitante; un 7B esaurisce la RAM.
3. **Contesto sicurezza OBBLIGATORIO per S1** (bot trading demo coabitante): (a) `GAS_SANDBOX_MODE=os_strict` OBBLIGATORIO finché il bot trading coabita — chiavi exchange sulla stessa macchina di un'AI che esegue codice = superficie di esfiltrazione non accettabile in os_with_fallback; (b) utente runtime **non-root** è requisito di sicurezza RAFFORZATO (non solo best practice): processo AI con accesso codice + chiavi exchange dello stesso utente root = game over in caso di exploit; (c) **Requisito esplicito S1**: creare utente runtime dedicato non-root e spostare working dir + model cache + `.gas_*.db` fuori da `/root`, di proprietà di quell'utente. Evidenza sonda S0: `VECTORS_DB /root/gas/.gas_vectors.db` — runtime e cache/db girano attualmente sotto `/root` come root.
4. **Decisione systemd ratificata**: `gas doctor` NON deve essere ExecStartPre/gate di avvio — esce 1 anche su sole API key assenti (semantica dichiarata in CLAUDE.md sez.3). Comportamento corretto: `Restart=always` + `RestartSec=10` + notifica Telegram al primo turno se degradato (doctor come check post-avvio, non blocco pre-avvio).
5. **R-vec-pool ✅ (2026-07-03)**: fingerprint ora include `fastembed_version`. Upgrade fastembed → mismatch versione → guard spegne il layer e obbliga a `gas reindex` (fail-closed). Il reindex non è più affidato alla memoria dell operatore ma forzato dal codice.
6.  **Confine sviluppo da telefono** (Claude Code cloud, sondato 2026-07-01): loop telefono→cloud→revisore→CI validato su evidenza reale (revisore+hook scattano nel cloud; CI verde run #50 su `d992c47`). CONFINE DURO: `bwrap` ASSENTE nel sandbox cloud → test sandbox/`run_command`/snapshot strutturalmente rossi lì, NON validabili da telefono (solo CI). Nessuna credenziale LLM nel cloud → runtime GAS non eseguibile lì. Fattibile da telefono: doc-only + motore leggero non-sandbox verificabile da CI. Da sondare a parte: claude remote-control (ambiente reale, claim non verificato). Limite accertato 2026-07-02: Claude Code cloud pusha SOLO sul branch di sessione, NON crea branch → i task cloud si stratificano, serve estrai-e-cancella a valle.
   - ✅ Remote Control locale verificato (2026-07-15): `cd ~/Gas && claude` + `/rc` → QR → app. CAVEAT OPERATIVO: la sessione eredita la cwd del lancio — lanciare SEMPRE da ~/Gas. CAVEAT SESSIONI: in app, ☁️ = Claude Code cloud (no bwrap, non canonico), icona computer+verde = Giulia locale. Non confonderle: un task bwrap in cloud dà falso verde. Confine invariato: da telefono solo doc-only + motore non-sandbox; bwrap solo locale/CI.
7. **✅ AGGIORNATA 2026-07-24 — postazione locale WSL**: dipendenze del motore installate con `pip install -r requirements.txt -r requirements-dev.txt` (2026-07-24, senza traccia in git). Versioni rilevate: openai 2.43.0, fastembed 0.8.0, numpy 2.4.6, onnxruntime 1.27.0, requests 2.34.2, pytest 9.1.1. Suite kernel: **250 PASS, 0 FAIL, 0 SKIP** eseguita su WSL con Python 3.12.3. ℹ️ **Divergenza Python APERTA (non sanata)**: il venv WSL usa Python 3.12.3, la CI usa `python-version: "3.11"` (dichiarato in ci.yml, commento corretto in questa sessione). La divergenza esiste e non viene sanata: non cambia `python-version` della CI né il Python del venv. Solo dichiarata. jq: 1.7 (installato a mano 2026-07-17, senza traccia in git). Push git: HTTPS, hook vivi senza passphrase (gh auth setup-git). Storia precedente: venv era assente al 2026-07-17, ricreato con Python 3.12.3; conteneva SOLO pytest fino al 2026-07-24; le "247 PASS WSL 2026-07-19" erano false (suite non eseguibile su WSL in quel momento — vedi errore dichiarato in riga 9).
8. **✅ S1 ESEGUITO (2026-07-04):** hardening SSH + utente runtime completati sul VPS CX33.
   ⚠️ SCRUB IP/SSH (2026-07-20): dato rimosso dai file HEAD. Stato = MITIGATO, NON chiuso: l'IP resta nella history git pubblica finché il repo non diventa privato. Cura vera = privatizzazione (vedi roadmap).
   - unattended-upgrades: attivo (running)
   - fail2ban: attivo, jail sshd, backend=auto, 4 IP bannati al reboot
   - Utente `<VPS_USER>` (uid=1000): creato, `/home/<VPS_USER>/gas/` copia working dir, `/home/<VPS_USER>/.cache/` model cache fastembed
   - sshd hardening: `PasswordAuthentication no`, `PermitRootLogin no`, `PubkeyAuthentication yes` (dropin `/etc/ssh/sshd_config.d/<SSH_DROPIN>`)
   - Kernel aggiornato: 6.8.0-134-generic (reboot post-S1 ok)
   - `/root/gas/` INTATTO (non cancellare fino a S1b confermato)
   - Accesso SSH: solo `<VPS_USER>@<VPS_IP>` via chiave `<KEY_TYPE>`. Login root SSH disabilitato.
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
- ✅ **Backfill memoria_revisore.md #48–#50 ESEGUITO** (2026-07-18, PR #24 `docs/backfill-revisore-48-50`): il canonico precedente era ERRATO — #48/#49 NON vivevano solo in `92a08ba`, erano anche in `83ae3e4` (recuperati verbatim da lì). Solo #50 viveva solo in `92a08ba`, diventato orfano e raccolto dal gc dopo il riallineamento WSL 2026-07-15 → NON recuperabile, inserita riga-segnaposto con merito reale (PR #19), ricostruzione a memoria vietata. Buco #48–#50 chiuso.

> Sessione 2026-07-24 archiviata in `reports/stato_storico.md`.
> Sessione 2026-07-24 (p2) archiviata in `reports/stato_storico.md`.
### DA FARE — sviluppo/processo (aperti dal 2026-07-09)
- ✅ **gh CLI installato su Giulia** — 2026-07-14: v2.96.0, git protocol HTTPS, account Gasss23, scopes repo+workflow. Verificato: `gh repo view Gasss23/Gas` OK, branch main visto. CHIUSO.
- ✅ **WSL locale riallineato a origin/main** — 2026-07-15: eseguito a mano da terminale WSL (`git fetch` + `checkout main` + `merge --ff-only`), `/home/gqual/Gas` ora a `9cbab56`; branch locale esaurito `docs/roadmap-item2-chiuso` cancellato (`-d` accettato = già dentro main). Registrato qui perché un allineamento manuale NON lascia traccia in git. CHIUSO.
- ℹ️ **Nomenclatura ambienti — clone Windows eliminato** (2026-07-15): esisteva un SECONDO clone del repo su `C:\Users\gqual\Gas` (PowerShell) oltre a quello WSL, in contraddizione con la regola "non esiste un locale separato dal WSL". Ha già prodotto un incidente: un allineamento eseguito sul clone sbagliato da un branch morto (`docs/cerebras-no-go`) scambiato per main. Deciso ed eseguito: clone Windows RIMOSSO, `~/Gas` su WSL (`/home/gqual/Gas`) è l'UNICO locale canonico. Se ricompare un clone Windows, è un errore da rimuovere: due cloni divergono in silenzio e la memoria comincia a mentire.
- ✅ **Debito Codespace CHIUSO — Codespace deprecato** (2026-07-19): sviluppo ora SOLO su WSL locale (`~/Gas`). Il Codespace era dirty su `fix/ci-hook-tests` (sessione interrotta); nessun branch remoto omonimo (mergiato in PR #23, `2f1e015`) → dirt solo locale al Codespace, cruft. Bonifica: Codespace **cancellato** (azione umana, `gh codespace delete`). Codespace non è più un ambiente attivo del progetto. // ex-ℹ️ debito 2026-07-18.
- ✅ **R-encoding CHIUSO** (2026-07-22, branch `fix/encoding-stato-progetto`): mojibake
  UTF-8 (testo UTF-8 letto come cp1252) riparato su 37 righe di `reports/stato_progetto.md`.
  Metodo deterministico, zero dipendenze: riscrittura di una riga SOLO se il round-trip
  inverso `nuova.encode('utf-8').decode(cp1252|latin-1)` restituisce esattamente la
  vecchia — gate che rende strutturalmente impossibile una modifica semantica.
  1 riga non riparata (questo item stesso, che citava le sequenze mojibake come esempi):
  esclusa correttamente dal gate. Conteggio righe invariato, invariante IP verificata.
- 🟡 **2FA Hetzner**: da attivare; recovery code da salvare OFFLINE prima di confermare.
- 🟡 **Ispezionare `/root/.ssh/authorized_keys` sul VPS** (residuo gas-vps): `PermitRootLogin no` mitiga ma non è chiuso.
- 🟡 **Decidere se rimuovere `gas-vps` da Hetzner Security → SSH Keys**: ogni server nuovo creato da quel progetto eredita quella chiave.
- 🟡 **Bonifica branch remoti — audit 2026-08-25** (branch `chore/audit-branch-remoti`): totale head = **10** (main + 9). Audit read-only eseguito — vedere `reports/ultimo_report.md` per evidenza verbatim completa. Risultato:
  - ✅ **SAFE-DA-CANCELLARE** (rc=0, tip già su main): `docs/scollega-gashistory-r2-v2`, `fix/r2-durabilita-memoria-clean`, `fix/r2-riserve-86`.
  - ⛔ **DA-GIUDICARE-A-MANO** (rc≠1, commit non su main): `claude/phone-gas-development-10svqc` (7 commit, tocca brains/), `docs/scollega-gashistory-da-r2` (1 commit, reports/), `fix/crm-idemp-diario` (1 commit, reports/), `fix/nonascii-cd-tests` (4 commit, scripts/+tests/), `fix/r2-durabilita-memoria` (9 commit, scripts/+tests/), `fix/review44-riserve-AC` (2 commit, reports/).
  - Storico precedente: da **27 head a 4** (bonifica 2026-07-22/07-28). I nuovi 6 branch non-main sono stati aperti nelle sessioni 2026-08-xx post-bonifica e non ancora cancellati. ⛔ CANCELLAZIONE = azione umana, MAI da sessione agente (R6).
  ⚠️ **Lezione push --delete (2026-07-28)**: `git push origin --delete <branch>` NON ha la rete di sicurezza di `git branch -d` — non rifiuta un branch non-fully-merged. Ha funzionato per `feature/crm-dup-detect` per esito (contenuto superato da rewrite PR #47), non per meccanismo: il comando non verifica il merge, cancella e basta. **REGOLA**: prima di cancellare un branch remoto, verificare a mano che il contenuto sia su main (`git branch --merged origin/main` oppure grep del codice chiave sul branch). Mai affidarsi a "sembrava superato".
- ℹ️ **Setting GitHub "Automatically delete head branches" — valutato e NON attivato** (2026-07-22): decisione consapevole, non una dimenticanza. Motivo: la cancellazione automatica al merge toglie la finestra di verifica manuale su un branch appena mergiato. La bonifica resta manuale e deliberata.
- ✅ **R-crm-1b fetta 3 (telefono) — CHIUSA su main** (2026-07-27): risolta con RISCRITTURA PULITA (branch `feature/crm-dup-telefono`, review #67, merge PR #47 `d67b12a`), NON col recupero da `feature/crm-dup-detect`. `normalizza_telefono()` + `rileva_duplicati_telefono()` ora su main. Vecchia strada `feature/crm-dup-detect` (`1d32819`, review #49) ABBANDONATA → branch superato. ⛔ precedente REVOCATO. Chiusura completa R-crm-1b: vedi finding ✅ sopra.
- ℹ️ **Micro-finding di processo — branch di sessione mai promosso a PR** (rilevato
  2026-07-28): il branch `docs/stato-roadmap-hygiene` (`409ad54`) è rimasto **2 commit
  avanti su main, 0 indietro, senza PR aperta** dalla sessione hygiene. Lavoro completo
  (`/fine-task` eseguito, handoff presente, hook che ha pushato il branch) ma **mai
  atterrato su main**, e **non registrato in nessun canonico**: per giorni i canonici
  hanno descritto uno stato "post-merge hygiene" che non esisteva. Classe NUOVA: non è
  gate saltato né scope creep, è **lavoro fatto che non atterra e sparisce dal radar**.
  La memoria ha mentito per OMISSIONE. Recuperato con PR dedicata il 2026-07-28.
  **Contromisura minima (disciplinare, non strutturale)**: a fine di ogni giro,
  `git ls-remote --heads origin` e confronto col numero di head atteso; ogni head in
  più va spiegata o chiusa. Fix strutturale possibile, NON impegnato: uno step in
  `/fine-task` che stampi `gh pr list --head <branch>` e FERMI se è vuoto.
- 🟡 **Copia VPS stantia vs origin/main** (2026-07-21, `### Sessione 2026-07-21`): la working copy di prod diverge dal repo (emerso da F7). Riallineamento = FASE 5 S2, con revisore + verifica, non a caldo.
- ⚠️ **Decisione APERTA — Secondo account GitHub** (2026-07-22, `### ℹ️ Micro-finding merge su main`): machine user per sessioni agente + `main-lock` con 1 approvazione richiesta — GitHub vieta l'auto-approvazione, l'agente non potrebbe chiudere la PR da solo. Da valutare insieme alla privatizzazione del repo (roadmap item 0).
- ⚠️ **Decisione APERTA — Trailer `Co-Authored-By`** (2026-07-23, `### Sessione 2026-07-23`): per distinguere in `git log` i commit d'agente da quelli scritti a mano. Non impegnata — il responsabile è l'operatore in entrambi i casi.

- ⚠️ **Scope-creep PR #59 (2026-08-02)**: branch `feature/voice-probe` ha mescolato due task distinti — sonda voce F0 (`clients/voice/probe/`) e allowlist gasmerge-ip. Recidiva della stessa classe registrata il 2026-07-08. Scope = decisione operatore.
- ⚠️ **Sonda F0 "6/6 verde" non verificata in dossier (2026-08-02)**: l'esito "6/6 verde" è dichiarato SOLO nel subject del commit `4056c97`, NON nel §1 del handoff canonico. Esito NON verificato-in-dossier. Da confermare rieseguendo la sonda prima di dichiararla base solida per Fetta 1 di FASE 3.
- ⚠️ **Decisione APERTA — D1-ter: IP WSL instabile tra reboot (2026-08-02, da handoff #59)**: l'IP del client Windows/WSL cambia tra un reboot e l'altro; l'allowlist statica nella sonda va aggiornata manualmente. Da risolvere prima di costruire la pipeline vocale permanente.
- ⚠️ **Decisione APERTA — D2-audio: load_dotenv override + policy device output (2026-08-02, da handoff #59)**: `load_dotenv()` nel client sonda può sovrascrivere variabili già in env; il device audio di output non è configurabile senza modificare il codice. Da decidere/documentare prima di Fetta 1.
- ⚠️ **Audit system prompt — 4 finding aperti (2026-08-29, audit READ-ONLY, branch `sonda/vps-stato-2026-08-26`)**: nessuna modifica al motore; ogni fix richiede scope dall'operatore. Findings:
  - **F1 CRITICO** `gas.py:46-48`: `"Per conteggi, misure e calcoli esatti usa SEMPRE run_command"` — SHELL_ALLOWLIST non contiene calcolatori (`bc`, `expr`, `awk`, `python` assenti). Ordine impossibile da eseguire per aritmetica. Stessa classe del bug 7×8.
  - **F2 ALTO** `gas_identity.md:3`: cita solo 3 tool (`read_file, write_file, run_command`); il kernel ne espone 6 (`ricorda, salva_contatto, imposta_stato_contatto` omessi). Gas potrebbe non usarli spontaneamente.
  - **F3 ALTO** `gas.py:42`: stessa lista incompleta nelle REGOLE TASSATIVE del base prompt.
  - **F4 MEDIO** `gas.py:42-44`: conflitto strutturale tra "non bloccarti" e "non simulare" — nessun path d'uscita esplicito per tool failure generica (il workaround "dichiara l'incertezza" è scoped solo ai conteggi numerici).
  - F5/F6 minori: doppia auto-presentazione (identity + base) e "echo" classificato come "sola lettura" (innocui).
- 🟡 **SICUREZZA — chiave ElevenLabs esposta in chat (2026-08-02, da handoff #59; decisione operatore 2026-08-06)**: la chiave API è comparsa nella chat di sessione. `git grep` su tutta la history del repo (2026-08-02) trova SOLO riferimenti a variabile d'ambiente (`os.environ.get("ELEVENLABS_API_KEY")`), NESSUNA chiave in chiaro committata. Rotazione NON eseguita: scelta consapevole dell'operatore, rischio residuo ACCETTATO. NB onesto: una chiave esposta resta compromessa a prescindere dal repo — questa è accettazione del rischio, non chiusura.

> Sessione 2026-07-21 archiviata in `reports/stato_storico.md`.
> Sessione 2026-07-22 archiviata in `reports/stato_storico.md`.
> Sessione 2026-07-22 (ℹ️ micro-finding processo — merge su main) archiviata in `reports/stato_storico.md`.
> Sessione 2026-07-23 archiviata in `reports/stato_storico.md`.
