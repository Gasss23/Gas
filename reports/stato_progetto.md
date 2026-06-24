# STATO PROGETTO GAS

> Fotografia viva dello stato. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-06-23** (split storico → `reports/stato_storico.md`)
> Storico sessioni, dettaglio componenti, finding chiusi: `reports/stato_storico.md`

## Stato motore

FASE 1 ✅ e FASE 2 ✅ chiuse. **28 review** completate. Suite: **158 PASS, 7 FAIL**
(7 FAIL ambientali Windows pre-esistenti: bwrap T11/T12/T13d2, WinError32 T26b — T9a/T9c ora SKIP condizionale in CI).
CI GitHub Actions (`.github/workflows/ci.yml`): BWRAP_OK confermato sul runner Linux; **CI-4 risolto** (2026-06-24): T9a/T9c ora [SKIP] su assenza API key, job verde.

Componenti attive:
- Snapshot preventivo anti-autodistruzione (fail-closed, refs/gas/snapshots/)
- Sandbox applicativo `run_command` (no-shell + allowlist + env sanificata)
- Sandbox OS bwrap (`GAS_SANDBOX_MODE=os_strict` default: rete isolata + fs read-only)
- `WINDOW_CHAR_CAP=24000` + `_cap_window_chars` (no slicing, scarto messaggi interi)
- Memoria SQLite `.gas_memory.db`: diario IMMUTABILE + rubrica contatti + FTS5 + backup auto
- Vector store `.gas_vectors.db` opt-in `GAS_VECTORS` (MiniLM 384-dim, cosine brute-force)
- CRM dal loop: tool `salva_contatto`/`imposta_stato_contatto`, identità su `chiave_norm` NFKC
- Iniezione always-on `_memoria_pin` (system msg) + tool `ricorda` (sola lettura)
- CLI `gas doctor` / `gas reindex` / `gas backup`

## Pipeline provider (paracadute)

1. `gemini-2.5-flash-lite` → 2. `gemini-2.5-flash` → 3. `groq/llama-3.3-70b-versatile`
   → 4. `openrouter` free (`meta-llama/llama-3.3-70b-instruct:free`)
   → 5. `ollama` offline (`qwen2.5:7b-instruct`, solo se `GAS_OLLAMA_URL` settata)

## Finding aperti (🟡 attivi)

> Chiusi in `reports/stato_storico.md` e `reports/finding_archiviati.md`.

- 🟡 **R-reidx-deps** — numpy/fastembed/onnxruntime devono restare in `requirements.txt` e nel deploy VPS; senza, layer vettoriale e `gas reindex` degradano silenziosamente.
- 🟡 **R-reidx-3** — picco RAM di `reindex` su diario grande. [VPS confermato Hetzner CX22 = 4GB RAM — vincolo 1GB obsoleto; criticità da ri-valutare su base 4GB prima del deploy.]
- 🟡 **R-vec-2** — costanti vector store non configurabili via env (`GAS_VECTORS_DB`, `GAS_EMBED_MODEL`): valutare al deploy.
- 🟡 **R-vec-3** — portabilità ARM non verificata (~504MB modello MiniLM). [VPS confermato CX22 = 4GB RAM — il modello occupa ~12% della RAM disponibile; il vincolo memoria non è più critico. Resta da verificare l'architettura CPU (ARM vs x86) al deploy.]
- 🟡 **R-wire-1** (RESIDUO) — `VEC_MIN_SIM=0.30` tarata su esempi sintetici: ri-tarare sul diario reale del VPS. Env-config già fatto (review #28).
- 🟡 **R-wire-2** — qualità semantica MiniLM limitata su query corte IT: limite di potenza, non correttezza. Legato a R-vec-3.
- 🟡 **Esfiltrazione** — chiusa in `os_strict` con bwrap; in `os_with_fallback` resta 🟡.
- 🟡 **WINDOW_CHAR_CAP non env-configurabile** (R2 review #7): valutare `GAS_WINDOW_CHAR_CAP` al deploy VPS / pipeline Whisper.
- 🟡 **Degrado a solo-testo per-turno non rilevato** (R2 review #5): solo cold doctor + warning statico in run_turn. Rimandato per falsi positivi.
- 🟡 **R-crm-1b** — identità cross-formato non prevenuta (es. `anna@ex.com` vs `Anna`): meccanismo merge manuale disponibile (`unisci_contatti`), policy chiave canonica non presa.
- 🟡 **MEMORY_PIN_SCAN hardcoded** — le 3 costanti principali pin sono env-override, ma `MEMORY_PIN_SCAN=200` resta fisso: valutare `GAS_MEMORY_PIN_SCAN` al deploy.
- 🟡 **R-ci-openrouter** — T9a fragile se OPENROUTER_API_KEY è presente: il test la poppava prima del turno T9 ma la tolleranza alla presenza di OPENROUTER non è garantita formalmente (revisore CI-4, 2026-06-24).
- ✅ **CI-4** — risolto (2026-06-24): T9a/T9c skip condizionale su assenza API key live, CI verde.
- 🟡 **Riserve minori** (non bloccanti, dettaglio in archivio): R-test-1 cap_window_chars, R2 #6 chdir trap, R3 #4 falsi positivi path-check, riserve snapshot TASK C, riserve hook SessionEnd, riserve R-mem2a, riserve R-mem, R26-1/R26-2 backup.

## Prossimi passi (in ordine di priorità)

1. **🔴 URGENTE — Controllo spesa token** (soluzione definitiva): vedere CLAUDE.md §10 item #1. Diagnosi fatta (23-06-2026): spesa = 100% Claude Code in sviluppo su Opus 4.8, GAS runtime = 0€. Azioni: `opusplan` attivo + stato_progetto snello (THIS).
2. **📱 Accesso Claude Code da telefono**: vedere CLAUDE.md §10 item #2.
3. ~~**CI-4 — verde pieno**~~ ✅ risolto (2026-06-24).
4. **FASE 3 — Interfaccia vocale**: Whisper STT + ElevenLabs TTS.
5. **FASE 5 — Deploy VPS Hetzner**: checklist pre-deploy (R-vec-3, R-reidx-3, R-wire-1 ri-taratura, R-reidx-deps, ollama, backup off-machine).

### PARK — registrati, nessun impegno
- Retention del diario (archiviazione/export, MAI DELETE — quando il volume lo richiederà).
- GDPR / dati personali lead: da guardare a FASE 4.

## Istituzioni di processo

- **A** — `reports/stato_progetto.md` (questo file): stato vivo, aggiornato a fine task.
- **A-arch** — `reports/stato_storico.md`: storico sessioni + finding chiusi + dettaglio motore.
- **B** — `reports/diff_sessione.md`: diff della sessione corrente (riscritto a ogni sessione).
- **C** — `.claude/agents/revisore.md`: gate obbligatorio pre-commit motore. **28 review**. Ultima: **#28** (VEC_MIN_SIM env-config, 2026-06-21). Lezioni in `.claude/agents/memoria_revisore.md`.
- **D** — `reports/handoff.md`: dossier di fine sessione (DECISIONI UMANE + diff stat + log + delta test + verdetto revisore + stato CI).

## Note operative VPS — non per oggi

> Registrate il 2026-06-15 per il deploy (FASE 5).

1. **Snapshot**: 0 ref in dev è ATTESO (il runtime GAS non gira qui). Sul VPS gli snapshot nasceranno da `run_command`/`write_file` → se doctor sez.7 mostrasse 0 ref sul VPS sarebbe anomalo. ~4427 oggetti loose = detrito git (stash/churn), non snapshot; `git gc` OPT-IN li riassorbe.
2. **OpenRouter free ~28s**: rung lento, paracadute non piano operativo. VPS va dimensionato per `qwen2.5:7b-instruct` (ollama locale = pavimento rapido a costo zero).
