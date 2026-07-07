# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-07 — Migrazione Groq gpt-oss-120b: fetta unica (4 punti)

---

## §0 DECISIONI UMANE RICHIESTE

1. **GROQ_API_KEY mancante** — Non trovata nell'ambiente (nessun .env nel progetto, nessuna variabile Windows persistente). Richiesta per completare il PUNTO 2 (round-trip live con tool call reale) e sbloccare il gate revisore + commit motore. Fornire con `$env:GROQ_API_KEY = "gsk_..."` in sessione oppure creare un `.env` nel progetto o impostarla come variabile Windows persistente.
2. **R-groq-dup architettura (decisione rimandabile)** — `"openai/gpt-oss-120b"` è ancora hardcoded nei payload Groq di `claude_brain.py` e `gemini_brain.py` (fallback rung). Il refactor mergiato ha introdotto `MODEL_GROQ` in `brains/model_ids.py` — usarlo nei fallback è un import banale ma richiede decisione umana sullo scope della fetta. Deferito, nessun impegno attuale.

---

## §1 SCOPE & ESITO FETTE

- **PUNTO 1 — `reasoning_effort: "low"` nei 3 brain**: `FATTA`
  Aggiunto al payload in `groq_brain.py` (principale), `claude_brain.py` (Groq fallback rung 2), `gemini_brain.py` (Groq fallback rung 3). Temperature e timeout invariati. I brain ora usano `MODEL_GROQ` da `brains/model_ids.py` (post-merge). Uncommitted — attende round-trip + revisore.

- **PUNTO 2 — Round-trip live con tool call reale**: `SALTATA — GROQ_API_KEY assente`
  Nessun .env nel progetto. Variabile non presente né in sessione né in env Windows persistente. Round-trip non eseguito. Conseguenze: R-groq-slash resta APERTO, doc PENDING, revisore non invocato, commit motore bloccato.

- **PUNTO 3 — Doc oneste (roadmap.md, stato_progetto.md)**: `FATTA`
  "✅ CHIUSA (review #43)" rimosso; stato reale "PENDING" scritto. Grep "review #43" → 0 match. Committato: `a1f503b`.

- **PUNTO 4 — Finding in stato_progetto.md**: `FATTA`
  R-groq-slash APERTO PENDING; R-groq-dup aperto (deferito); nota TPM 8K. Committato: `a1f503b`.

- **EXTRA — Latenza GAS**: `FATTA`
  Segnalata dall'utente durante la sessione (~5s più lento). Registrata in roadmap.md come item non urgente. Committato: `2700f1f`.

---

## §2 GIT DIFF --STAT (sessione, de9909c..HEAD)

```
 .claude/agents/memoria_revisore.md | 1 +
 reports/roadmap.md                 | 6 ++++--
 reports/stato_progetto.md          | 6 ++++--
 3 files changed, 9 insertions(+), 4 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione, de9909c..HEAD)

```
2700f1f docs(roadmap): registra indagine latenza GAS (non urgente, 2026-07-07)
a1f503b docs(migrazione-groq): aggiorna doc post-merge refactor/model-ids-fonte-unica
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun commit motore in questa sessione (`brains/`, `gas.py`, `tests/` non in staging). Il revisore non è stato invocato. Motivo: PUNTO 2 (round-trip live) bloccato da GROQ_API_KEY mancante — gate CLAUDE.md sez.3 rispettato.

File motore uncommitted in working tree:
- `brains/groq_brain.py` — `reasoning_effort: "low"` aggiunto
- `brains/claude_brain.py` — `reasoning_effort: "low"` aggiunto
- `brains/gemini_brain.py` — `reasoning_effort: "low"` aggiunto
- `tests/test_unit_kernel.py` — model log string residuo da stash

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a `gas.py/tests/` committata. Baseline suite invariato: **214 PASS, 0 FAIL, 2 SKIP** (sonda 2026-07-03). Le modifiche ai brain (`reasoning_effort: "low"`) sono additive al payload — nessuna logica di parsing toccata, nessuna regressione attesa.

---

## §6 STATO CI

```
completed	success	docs(roadmap): registra indagine latenza GAS (non urgente, 2026-07-07)	CI	main	push	28900092673	34s	2026-07-07T21:31:02Z
completed	success	docs(migrazione-groq): aggiorna doc post-merge refactor/model-ids-fon…	CI	main	push	28900065926	38s	2026-07-07T21:30:35Z
completed	success	Merge branch 'refactor/model-ids-fonte-unica'	CI	main	push	28874912495	42s	2026-07-07T14:41:10Z
```

Ultimi 3 run su `main`: tutti **SUCCESS**. I commit di questa sessione (`a1f503b`, `2700f1f`) sono doc-only → CI verde per definizione (nessun file motore toccato).

---

## §7 RISERVE APERTE

- **R-groq-slash** (2026-07-07, APERTO) — slash-namespace `openai/gpt-oss-120b` non validato su endpoint Groq live con tool call reale. Chiude solo se round-trip live passa. Sblocca revisore + commit motore.
- **R-groq-dup** (2026-07-07, DEFERITO) — `"openai/gpt-oss-120b"` hardcoded nei payload Groq di `claude_brain.py` e `gemini_brain.py`. `MODEL_GROQ` già disponibile in `brains/model_ids.py` — import banale, ma decisione umana richiesta su scope fetta.
- **Latenza GAS** (2026-07-07, non urgente) — risposte ~5s più lente. Possibili cause: TTFT `gpt-oss-120b`, burst TPM 8K → fallthrough OpenRouter (~28s). Da misurare con timing nel log.
- **TPM 8K gpt-oss-120b** — burst limit inferiore a llama (12K): fallthrough OpenRouter più frequente = comportamento atteso, non regressione.
- **Riserve pre-esistenti attive**: R-wire-1, R-wire-2, R-crm-1b, R-reidx-3, Esfiltrazione (os_with_fallback), R-ci-openrouter, Degrado silenzioso per-turno, riserve minori — dettaglio in `stato_progetto.md`.
