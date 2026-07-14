# 🗄️ FINDING ARCHIVIATI (chiusi)

> Cimitero dei finding già CHIUSI/RISOLTI/RIDOTTI, compressi a una riga datata.
> Nessuna informazione distrutta: il dettaglio integrale resta nella history git
> (commit citati) e nei report di sessione. I finding APERTI (🟡/🟠/🔴) restano
> invece in `reports/stato_progetto.md`.
> Creato il 2026-06-15 (TASK 2 — sfoltimento `stato_progetto.md`).

- **2026-06-11** — T10 path traversal su `write_file`/`read_file` BLOCCATO via `_safe_path` (`.resolve()` + `is_relative_to`). CHIUSO. (review #2)
- **2026-06-11** — Snapshot preventivo dei file: `_snapshot` via indice git temporaneo + ref `refs/gas/snapshots/*`, fail-closed. CHIUSO. (review #3, R1 in #3-bis)
- **2026-06-12** — Sandbox/dry-run per `run_command` (shlex no-shell + allowlist read-only + env sanificata): finding esfiltrazione RIDOTTO 🟠→🟡 (chiusura piena rinviata al sandbox OS). (review #4)
- **2026-06-14** — Snapshot sprecato in os_strict quando il sandbox manca (R1 #6): check sandbox OS anticipato PRIMA dello snapshot nel ramo `run_command`. RISOLTO. (review #7)
- **2026-06-14** — Manca test permanente per `_cap_window_chars` (R1 #7): aggiunto blocco T14 (9 check), mordacità verificata per mutazione. RISOLTO. (review #8)
- **2026-06-14** — Nessun cap rigido sulla finestra (review #1): `WINDOW_CHAR_CAP = 24000` a granularità di messaggio (`_cap_window_chars`), mai slicing. CHIUSO. (review #7)
- **2026-06-14** — Modello free hardcoded e volatile (R1 #5): `gas doctor` verifica esistenza (404→WARN) e capacità tool del modello free via GET di metadati. CHIUSO. (TASK B, review #9)
- **2026-06-14** — Duplicazione costanti provider (R3 #5): URL/slug provider estratti in costanti di modulo, punto unico per `run_turn`/`doctor`, cascata bit-identica. CHIUSO. (TASK A)
- **2026-06-14** — Duplicazione del parse di `GAS_SANDBOX_MODE` in doctor (R3 #6): estratto helper `_parse_mode`, init e doctor risolvono lo STESSO mode (T16c). CHIUSO. (TASK A)
- **2026-06-14** — Retention snapshot count-based (R2): passata a IBRIDA = UNIONE di (ultimi `SNAPSHOT_KEEP=100`) e (più giovani di `SNAPSHOT_KEEP_DAYS=7`), certificata dai T18. CHIUSO. (TASK C, review #10)
- **2026-06-14** — Manutenzione snapshot residua (R3): `doctor` sez.7 REPORTA ref/loose/log (gc resta opt-in manuale) + `snapshots.log` gitignorato e ruotato `.1`. CHIUSO/MITIGATO. (TASK C)
- **2026-06-15** — Rumore log + amplificazione sovrascrittura via hook SessionEnd: hook reso additivo+condizionale (script testabile, niente commit vuoti, motore mai committato) + regola "commit esplicito dei report" dell'agente; bug sovrascrittura (7005517→412714f) chiuso, verifica reale 8/8. CHIUSO. (TASK 1, revisore APPROVATO)
- **2026-06-24** — CI-4: T9a/T9c skip condizionale su assenza API key live, CI verde. CHIUSO. (review #29)
- **2026-06-25** — R-reidx-deps: requirements.txt pinnato (`openai==2.43.0`, `requests==2.34.2`, `numpy==2.4.6`, `onnxruntime==1.27.0`, `fastembed==0.8.0`); crash fresh deploy su `requests` mancante eliminato; ABI numpy/onnxruntime copinnata. CHIUSO.
- **2026-06-25** — R-vec-2: `GAS_VECTORS_DB` e `GAS_EMBED_MODEL` configurabili via env. CHIUSO. (review #31)
- **2026-06-25** — WINDOW_CHAR_CAP non env-configurabile: `GAS_WINDOW_CHAR_CAP` configurabile via env, min_val=1000. CHIUSO. (review #31)
- **2026-06-25** — MEMORY_PIN_SCAN hardcoded: `GAS_MEMORY_PIN_SCAN` configurabile via env, min_val=10. CHIUSO. (review #31)
- **2026-06-27** — R-vec-2b: fingerprint-guard fail-closed — mismatch model_id/dim o DB legacy → layer disabilitato + `gas reindex` istruito; fingerprint scritto alla creazione e nel reindex. CHIUSO. (review #34)
- **2026-06-27** — R-tel-1: `_free_names` derivato da `FREE_RUNGS`; flag `obbligatoria` + `reason` nel JSONL = livello ("WARN"/"KO"); T40/T40b confermano. CHIUSO. (review #37)
- **2026-06-27** — Riserve review #35: T39b-reason/T39c-reason assert su `disable_reason`; T39f (ramo sqlite3.Error) e T39g (ramo embedder assenti) coprono i 4 rami. CHIUSE. (review #36)
- **2026-07-02** — R-vec-3: import + embedding runtime confermati su CX33 reale (bge-small + multilingual, dims=384). Boundary esplicito: prova di import/dim, NON di qualità semantica (→ R-wire-2). CHIUSO. (sonda S0 2026-06-30, CX33)
- **2026-07-03** — R-vec-pool: `fastembed.__version__` aggiunto al fingerprint vector store (scrittura + reindex); DB legacy senza campo → fail-closed ("DB legacy: fastembed_version assente"); mismatch versione → "fingerprint mismatch". Test T39h-T39k. CHIUSO. (review #42)
- **2026-07-07** — R-groq-dup: tutti i brain importano `MODEL_GROQ` da `brains/model_ids.py` (fonte unica, merge `eb0509f`). Confermato review #44. CHIUSO.
- **2026-07-08** — R-groq-slash: formato `openai/gpt-oss-120b` accettato da api.groq.com — STATUS 200, tool_calls parsate, latenza 1138ms, 7 reasoning_tokens. Validazione live su singola run (non garanzia perpetua). CHIUSO. (commit f028e51, review #44)
- **2026-07-13** — Riserve review #44 A e C: commento inline `reasoning_effort` nei 3 brain; T36c legato a MODEL_GROQ (fonte unica). CHIUSE. (review #45, merge PR #4 3836111)
- **2026-07-13** — Riserva #44B: prezzi Groq env-overridabili (`GAS_GROQ_PRICE_IN`/`GAS_GROQ_PRICE_OUT`), try/except per valore non parsabile, T44d. CHIUSA. (review #46, merge PR #6)
- **2026-07-13** — Hardening token Claude Code: token Codespace OAuth (`ghu_*`) non ha Administration → lucchetto `main-lock` non aggirabile da Claude Code (verificato via curl, 404/403 su ruleset id 18805824). CHIUSO.
- **2026-07-14** — R-crm-1b CRM dedup completo (4 fette): (1) `rileva_duplicati_email()` + CLI `gas check-dups` (email cross-campo, review #47); (2) `gas merge-contacts <da> <verso>` con snapshot diario atomico pre-merge, fail-safe §9 (review #48); (3) idempotenza diario `_append_sospetto` + tag `[ids:X,Y]` — no gonfiamento con scheduler h24 (review #49); (4) `normalizza_telefono` (pura, +39/0039/locale) + `rileva_duplicati_telefono` (review #49). Fuzzy name matching escluso by design. CHIUSO. (review #47+#48+#49, CI run 29342632131 240 PASS ✅)
