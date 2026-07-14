# Report — Sfoltita finding aperti (docs/sfoltita-finding)
**Data:** 2026-07-14
**Branch:** docs/sfoltita-finding (da docs/gh-chiuso)
**Scope:** doc-only — nessun file motore toccato (gas.py, brains/, modules/, tests/)

---

## git diff --stat REALE

```
 reports/finding_archiviati.md | 15 +++++++++++++
 reports/stato_progetto.md     | 51 +++++++++++++++++++------------------------
 2 files changed, 37 insertions(+), 29 deletions(-)
```

---

## PUNTO 1 — Spot-check per ogni candidato ✅

| Item | Esito | Prova |
|------|-------|-------|
| **R-reidx-deps** | VERIFICATO | `requirements.txt`: openai==2.43.0, requests==2.34.2, numpy==2.4.6, onnxruntime==1.27.0, fastembed==0.8.0 |
| **R-vec-2** | VERIFICATO | `gas.py:374,376` legge `GAS_VECTORS_DB` e `GAS_EMBED_MODEL` da env |
| **R-vec-2b** | VERIFICATO | test T39b/T39c/T39f/T39g presenti in `tests/test_unit_kernel.py` |
| **R-vec-3** | VERIFICATO | testo dice esplicitamente "NON prova qualità semantica" — R-wire-2 residuo 🟡 non toccato |
| **R-vec-pool** | VERIFICATO | test T39h-T39k presenti; `fastembed_version` nel fingerprint confermato |
| **WINDOW_CHAR_CAP** | VERIFICATO | `gas.py:352` — `self.WINDOW_CHAR_CAP = _env_int("GAS_WINDOW_CHAR_CAP", ..., min_val=1000)` |
| **R-groq-slash** | VERIFICATO | commit `f028e51` in git log — nota lasciata com'è (singola run, non garanzia perpetua) |
| **R-groq-dup** | VERIFICATO | merge `eb0509f` in git log |
| **MEMORY_PIN_SCAN** | VERIFICATO | `gas.py:351` — `self.MEMORY_PIN_SCAN = _env_int("GAS_MEMORY_PIN_SCAN", ..., min_val=10)` |
| **CI-4** | VERIFICATO | T9a/T9c skip condizionale in `tests/test_unit_kernel.py:149,153,159,162` |
| **R-tel-1** | VERIFICATO | `gas.py:1446` — `_free_names = {r[0] for r in FREE_RUNGS}` |
| **Riserve #35** | VERIFICATO | T39b-reason, T39c-reason, T39f, T39g presenti nei test |
| **Riserve #44 A e C** | VERIFICATO | merge PR #4 hash `3836111` in git log |
| **Riserva #44B** | VERIFICATO | `brains/model_ids.py:11-16` — `float(os.getenv(...))` con try/except (env-overridabile) |
| **Hardening token Claude Code** | VERIFICATO | commit `72c2040` in git log; curl su ruleset id 18805824 => 404/403 confermato |

**Nessun RETROCESSO**: tutti i 15 candidati hanno prova verificabile e vengono archiviati.

---

## PUNTO 2 — Finding archiviati

15 item spostati da `reports/stato_progetto.md` a `reports/finding_archiviati.md` (compressi a una riga datata):

- CI-4 (2026-06-24)
- R-reidx-deps, R-vec-2, WINDOW_CHAR_CAP, MEMORY_PIN_SCAN (2026-06-25)
- R-vec-2b, R-tel-1, Riserve #35 (2026-06-27)
- R-vec-3 (2026-07-02)
- R-vec-pool (2026-07-03)
- R-groq-dup (2026-07-07), R-groq-slash (2026-07-08)
- Riserve #44 A+C, Riserva #44B, Hardening token Claude Code (2026-07-13)

---

## PUNTO 3 — Riclassifica 🟡 aperti

**Restano in Finding aperti come 🟡 attivi (5 item):**
- Esfiltrazione os_with_fallback
- Degrado solo-testo per-turno
- R-crm-1b
- R-ci-openrouter
- Riserve minori

**Nuova subsection "### DEPLOY VPS — da tarare su dati reali" (3 item):**
- R-reidx-3 (picco RAM reindex, chiusura definitiva rinviata a VPS)
- R-wire-1 (VEC_MIN_SIM=0.30, ri-tarare su diario reale)
- RAM a regime del singolo modello (MemoryHigh/Max da affinare dopo misura VPS)

**Nuova subsection "### Limiti noti (non-finding)" (1 item):**
- R-wire-2 (qualità semantica MiniLM, limite di potenza non correttezza)

**Nuova subsection "### Debito latente" (1 item):**
- R-legacy-slice (brains/claude_brain.py slicing inerte, non wired al kernel)

**TPM burst gpt-oss-120b:** degradato da item a nota ℹ️ inline (comportamento atteso, non regressione).

---

## PUNTO 4 — Contatore review

Numero reale letto da `.claude/agents/memoria_revisore.md`: ultima entry = 2026-07-13 (review #46).

`stato_progetto.md` già riportava **46** in entrambe le occorrenze (riga 9 e sezione Istituzioni).
**Nessuna modifica necessaria** al contatore.

---

## Conteggio righe "Finding aperti" prima/dopo

| | Righe non-vuote |
|---|---|
| **Prima** | ~30 (26 sezione main + 4 Riserve #44 A/B/C in Note VPS) |
| **Dopo** | 16 |

Riduzione ~46%. Struttura ora semantica: attivi / VPS / limiti / debito / nota.

---

## Divieti rispettati

- Nessun ✅ nuovo aggiunto
- Motore non toccato (gas.py, brains/, modules/, tests/)
- CLAUDE.md, roadmap.md non toccati
- Nessun push su main
