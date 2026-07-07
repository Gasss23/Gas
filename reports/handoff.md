# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-07 — Migrazione Groq gpt-oss-120b: fetta unica (4 punti)

---

## §0 DECISIONI UMANE RICHIESTE

1. **GROQ_API_KEY mancante** — Non trovata nell'ambiente (nessun .env nel progetto, nessuna variabile Windows persistente). Richiesta per completare il PUNTO 2 (round-trip live con tool call reale) e sbloccare il gate revisore + commit motore. Fornire con `$env:GROQ_API_KEY = "gsk_..."` in sessione oppure creare un `.env` nel progetto o impostarla come variabile Windows persistente.
2. **R-groq-dup architettura (decisione rimandabile)** — `"openai/gpt-oss-120b"` è hardcoded in 3 file (`groq_brain.py`, `claude_brain.py`, `gemini_brain.py`). Serve fonte unica. Opzioni: (a) env `GAS_GROQ_MODEL` con default in ogni brain; (b) `config.py` separato che espone la costante. NON importare da `gas.py` (circular import). Decisione umana prima di aprire la fetta R-groq-dup.

---

## §1 SCOPE & ESITO FETTE

- **PUNTO 1 — `reasoning_effort: "low"` nei 3 brain**: `FATTA`
  Aggiunto al payload JSON in `brains/groq_brain.py` (payload principale), `brains/claude_brain.py` (Groq fallback rung 2), `brains/gemini_brain.py` (Groq fallback rung 3). Temperature e timeout invariati. Uncommitted — attende round-trip + revisore.

- **PUNTO 2 — Round-trip live con tool call reale**: `SALTATA — GROQ_API_KEY assente`
  Nessun .env nel progetto. Variabile non presente né in sessione né in env Windows persistente. Round-trip non eseguito. Conseguenze: R-groq-slash resta APERTO, doc PENDING, revisore non invocato, commit motore bloccato.

- **PUNTO 3 — Doc oneste (roadmap.md, stato_progetto.md)**: `FATTA`
  "✅ CHIUSA (review #43)" rimosso da entrambi i file (review non ancora avvenuta). Stato reale scritto: "migrazione codice fatta 2026-07-07; validazione live: PENDING". Grep "review #43" → 0 match. Incluso in questo commit di report.

- **PUNTO 4 — Finding in stato_progetto.md**: `FATTA`
  (a) R-groq-slash lasciato APERTO PENDING (condizionale rispettata: chiudere SOLO se punto 2 passa).
  (b) R-groq-dup aperto: hardcoded triplicato, deferito a fetta separata, decisione umana richiesta.
  (c) Nota TPM: burst 8K < 12K llama → fallthrough OpenRouter più frequente = atteso, non regressione.
  Incluso in questo commit di report.

---

## §2 GIT DIFF --STAT (sessione, commit 3f542c1..HEAD)

```
 reports/roadmap.md        | 5 +++--
 reports/stato_progetto.md | 3 ++-
 2 files changed, 5 insertions(+), 3 deletions(-)
```

**Nota**: questa sessione NON ha ancora commitatti file motore. Il diff sopra mostra solo l'auto-commit `5b3c4c0` della sessione precedente. Le modifiche di questa sessione (brains + doc) sono in working tree, uncommitted. Diff working tree vs HEAD (git diff --stat HEAD):

```
 .claude/agents/memoria_revisore.md | 1 +
 brains/claude_brain.py             | 4 ++--
 brains/gemini_brain.py             | 7 ++++---
 brains/groq_brain.py               | 5 +++--
 gas.py                             | 4 ++--
 reports/roadmap.md                 | 4 ++--
 reports/stato_progetto.md          | 6 ++++--
 tests/test_unit_kernel.py          | 2 +-
 8 files changed, 19 insertions(+), 14 deletions(-) [uncommitted]
```

---

## §3 GIT LOG --ONELINE (sessione, commit 3f542c1..HEAD)

```
5b3c4c0 auto-commit fine sessione 2026-07-07_20:19 [solo reports/doc/history, motore escluso]
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

**PENDING** — Il revisore non è stato invocato perché il PUNTO 2 (round-trip live) è bloccato da GROQ_API_KEY mancante. I file motore (`brains/groq_brain.py`, `brains/claude_brain.py`, `brains/gemini_brain.py`, `gas.py`, `tests/test_unit_kernel.py`) sono in working tree, NON committati. Il gate revisore (CLAUDE.md sez. 3) richiede verdetto APPROVATO/CON RISERVE prima del commit motore. Nessun bypass autorizzato.

---

## §5 DELTA TEST DEL MOTORE

Nessun test eseguito in questa sessione. Le modifiche ai brains (aggiunta `reasoning_effort: "low"`) sono formalmente non rompenti (parametro aggiuntivo nel payload, nessuna logica di parsing cambiata). La suite attuale al baseline: **214 PASS, 0 FAIL, 2 SKIP** (sonda 2026-07-03). Il test `test_unit_kernel.py` ha un aggiornamento pre-esistente (nome modello groq in log: `llama-3.3-70b` → `openai/gpt-oss-120b`) — già parte del diff pre-esistente, non introdotto in questa sessione.

---

## §6 STATO CI

```
completed	success	Merge branch 'refactor/model-ids-fonte-unica'	CI	main	push	28874912495	42s	2026-07-07T14:41:10Z
completed	success	chore(scrivi-rep): ultima risposta salvata	CI	main	push	28873830930	46s	2026-07-07T14:25:32Z
completed	success	refactor(brains): fonte unica per gli ID modello della cascata (model…	CI	refactor/model-ids-fonte-unica	push	28873785626	39s	2026-07-07T14:24:53Z
```

Ultimo run su `main`: **SUCCESS** (commit `5b3c4c0` / merge `refactor/model-ids-fonte-unica`, 2026-07-07T14:41:10Z). Nessun commit motore questa sessione → nessun run CI da questa sessione.

---

## §7 RISERVE APERTE

- **R-groq-slash** (2026-07-07) — APERTO PENDING round-trip live. Validare slash-namespace `openai/gpt-oss-120b` e tool_calls sull'endpoint Groq `/v1/chat/completions` con chiamata reale. Sblocca il revisore + commit motore.
- **R-groq-dup** (2026-07-07, DEFERITO) — `"openai/gpt-oss-120b"` hardcoded in 3 brain. Fonte unica richiesta. Decisione umana su dove definire il default prima di aprire la fetta.
- **TPM nota** — burst 8K gpt-oss-120b < 12K llama: fallthrough OpenRouter più frequente = atteso. Monitorare se il fallthrough in produzione crea latenza percepibile (OpenRouter free ~28s).
- **Riserve pre-esistenti attive**: R-wire-1, R-wire-2, R-crm-1b, R-reidx-3, Esfiltrazione (os_with_fallback), R-ci-openrouter, Degrado silenzioso, Riserve minori — dettaglio in `stato_progetto.md`.
