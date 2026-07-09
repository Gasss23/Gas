# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-08 — Migrazione Groq gpt-oss-120b: completamento PUNTO 2-4 (round-trip live, revisore, commit)

---

## §0 DECISIONI UMANE RICHIESTE

Nessuna.

---

## §1 SCOPE & ESITO FETTE

- **PUNTO 1 — `reasoning_effort: "low"` nei 3 brain**: `FATTA` (sessione precedente 2026-07-07, già committata al push precedente; confermata in scope da questa sessione)
- **PUNTO 2 — Round-trip reale con tool call live**: `FATTA` — STATUS 200, modello `openai/gpt-oss-120b` accettato, tool_calls parsate, latenza 1138ms, 7 reasoning_tokens
- **PUNTO 3 — Gate revisore (review #44)**: `FATTA` — APPROVATO CON RISERVE (3 riserve non bloccanti)
- **PUNTO 4 — Commit motore + report**: `FATTA` — commit `f028e51` su main, push `b806ddc`

Finding chiusi: **R-groq-slash** ✅, **R-groq-dup** ✅

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  1 +
 brains/claude_brain.py             |  4 +-
 brains/gemini_brain.py             |  3 +-
 brains/groq_brain.py               |  3 +-
 brains/model_ids.py                |  2 +-
 gas.py                             |  2 +-
 reports/stato_progetto.md          | 10 +++--
 reports/ultimo_report.md           | 78 ++++++++++++++++++++++++++------------
 tests/test_unit_kernel.py          |  2 +-
 9 files changed, 70 insertions(+), 35 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
b806ddc docs(report): fine task migrazione gpt-oss-120b — R-groq-slash e R-groq-dup CHIUSI
f028e51 feat(groq): migra a openai/gpt-oss-120b con reasoning_effort: low
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `f028e51` tocca `brains/`, `gas.py`, `tests/` — review #44 eseguita.

**VERDETTO: APPROVATO CON RISERVE**

**Oggetto:** Migrazione Groq model → `openai/gpt-oss-120b` + `reasoning_effort: "low"` su tutti e tre i brain + aggiornamento prezzi

**Corretto:**
- Sorgente unica `MODEL_GROQ` rispettata: tutti e tre i brain file importano già da `brains/model_ids.py` (R-groq-dup CHIUSO).
- Live validation eseguita pre-review: STATUS 200, `openai/gpt-oss-120b` accettato, tool calls parsate, `reasoning_effort: "low"` funzionante (7 reasoning_tokens, 1138 ms). R-groq-slash CHIUSO.
- `reasoning_effort: "low"` aggiunto in modo uniforme nei tre call-site.
- Fail-safe §9 intatto: non-200 → `FakeMsg` / `except Exception: pass`, zero crash in qualsiasi ramo.
- Prezzi aggiornati ($0.15/$0.60), tabella dichiarata "approx" per design.
- Test T36c allineato al nuovo model ID.
- Nessuna violazione WALL OF SHAME (niente slicing storia, niente tool simulation).

**Riserve (non bloccanti):**
- **A** — `reasoning_effort` hardcoded: se `GAS_MODEL_GROQ` sovrascrive con un modello non-reasoning, il rung torna un 4xx silente (fail-safe regge, ma la diagnostica è opaca). Aggiungere commento inline che documenta il vincolo.
- **B** — Prezzi $0.15/$0.60 non verificabili staticamente: confrontare con pricing page Groq al deploy VPS.
- **C** — T36c usa stringa letterale invece della costante importata: aggiornamento manuale necessario alla prossima migrazione modello. Cosmetica.

**Finding chiusi da questo diff:** R-groq-slash, R-groq-dup.

---

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_kernel.py` modificato: T36c — stringa model ID aggiornata `"llama-3.3-70b"` → `"openai/gpt-oss-120b"`.

**Run locale Windows (PYTHONUTF8=1):**

```
=== RIEPILOGO: 204 PASS, 7 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T13d2 os_with_fallback + sandbox assente -> esegue (sandbox applicativa) — Errore eseguendo run_command: [WinError 2] Impossibile trova
  FAIL: T26b backup: copia leggibile + rotazione ultime N + retention pura — rimasti=5 keep=2 drop=3
```

**Fuori scope:** tutti e 7 i FAIL sono pre-esistenti su Windows (bwrap non disponibile, WinError32). Non introdotti da questa modifica. T36c: PASS (non in lista FAIL).

**Baseline canonica (WSL bwrap, 2026-07-03):** 214 PASS, 0 FAIL, 2 SKIP — immutata.

---

## §6 STATO CI

```
completed  success  docs(report): fine task migrazione gpt-oss-120b — R-groq-slash e R-gr…  CI  main  push  28966795128  33s  2026-07-08T18:38:01Z
completed  success  docs(roadmap): PARK item Mirage VFS                                      CI  claude/phone-gas-development-10svqc  push  28953566232  38s  2026-07-08T15:12:24Z
completed  success  docs(fine-task): report sessione 2026-07-07 — fetta groq gpt-oss-120b…  CI  main  push  28900871634  49s  2026-07-07T21:45:30Z
```

Run #28966795128 su commit `b806ddc` (HEAD della sessione, push unico che include `f028e51` + `b806ddc`): **SUCCESS** ✅

---

## §7 RISERVE APERTE

Riserve review #44 (non bloccanti, tracciate in `stato_progetto.md`):

- **A** — `reasoning_effort` hardcoded nei payload Groq: se `GAS_MODEL_GROQ` env sovrascrive con un modello non-reasoning, il parametro causa un 4xx silente. Il fail-safe §9 regge (fallback attivo, zero crash), ma la diagnostica è opaca. Suggerito: commento inline che documenta il vincolo modello.
- **B** — Prezzi Groq ($0.15/$0.60 per MTok): non verificabili staticamente, da confrontare con pricing page Groq al deploy VPS.
- **C** — T36c usa stringa letterale `"openai/gpt-oss-120b"` invece di importare la costante `MODEL_GROQ`. Aggiornamento manuale necessario alla prossima migrazione modello. Cosmetica.

---

## §8 ADDENDUM — sessione cloud 2026-07-09 (doc-only, post-reset branch)

Contesto: il branch `claude/phone-gas-development-10svqc` è stato riallineato a main (`457fabe`); i commit doc della sessione cloud precedente (Dispatch/Cowork/Mirage, `fa212a6` e precedenti) sono rimasti fuori dalla nuova storia. Riapplicati add-only su richiesta umana ("scrivili lo stesso senza sostituire quello che c'è già").

- `reports/roadmap.md` — DA DISCUTERE: aggiunti **Claude Dispatch (candidato accesso dev da telefono, IN VALIDAZIONE)** e **Controllo Telegram unificato (ridimensionato)** con rimando alla spec "🌉 Ponte GAS↔CC human-gated" (che già copre il canale GAS→CC). Ricreata sezione **🅿️ PARK** in coda con **Mirage** e **Claude Cowork**.
- `reports/stato_progetto.md` — Prossimi passi #3: annotata **sonda Dispatch pendente** (se OK, item 2 chiuso senza bridge custom).
- Nessun file motore toccato in questo addendum → gate revisore non applicabile (CLAUDE.md sez.3). Nota per la sessione cloud: la migrazione Groq era stata duplicata qui su branch (review #41, `4137921`) — superata e assorbita da `f028e51` su main (review #44, con validazione live che chiude R-groq41-2/3); nessuna azione residua.
- ⚠️ **Finding encoding**: `reports/stato_progetto.md` (versione da sessione PC) contiene righe con doppia codifica UTF-8 (es. `Ã¨` per `è`, `â€”` per `—`), mischiate a righe corrette. Probabile pipeline Windows senza `PYTHONUTF8=1`/UTF-8. Non corretto in massa: decisione umana (fix meccanico possibile, doc-only).
