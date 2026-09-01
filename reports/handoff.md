# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-01 — Correzione reporting finding "kernel rifiuta 7×8"

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #80 (https://github.com/Gasss23/Gas/pull/80).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Correzione stato_progetto.md (finding 7×8)**: `FATTA` — Stato cambiato da ✅ CHIUSO a 🟡 VERIFICATO RISOLTO SU GEMINI. Aggiunti 3 caveat espliciti: (i) causa radice NON rimossa dal motore; (ii) comportamento Groq contraddittorio tra report; (iii) attribuzione "Groq-specifico" non provata (Groq non testato nella run 2026-09-01). Diagnosi storica mantenuta.
- **Fetta 2 — Correzione ultimo_report.md §5**: `FATTA` — Rimossa affermazione "il finding era Groq-specifico" come fatto acquisito; sostituita con dichiarazione onesta dei 3 caveat.
- **Fetta 3 — Fix motore (system prompt / SHELL_ALLOWLIST)**: `DEFERITA — fuori scope dichiarato (solo correzione reporting). Se necessario, task dedicato.`

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md  |  17 +++----
 reports/handoff.md        |  46 ++++++-------------
 reports/stato_progetto.md |   8 +++-
 reports/ultimo_report.md  | 112 +++++++++++++++++++++++++++++++++++-----------
 4 files changed, 114 insertions(+), 69 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
d7e2d35 docs(fine-task): handoff sonda E2E calcola() Gemini run-2 2026-09-01
179fb12 docs(fine-task): handoff sonda E2E calcola() Gemini 2026-09-01 — 2 PASS
6719e9f docs(sonda): E2E calcola() Gemini — 2 PASS 2026-09-01
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/. Suite non rieseguita.

---

## §6 STATO CI

```
completed	success	docs(fine-task): handoff sonda E2E calcola() Gemini run-2 2026-09-01	CI	sonda/e2e-calcola-gemini-2026-09-01	push	33538544336	46s	2026-09-01T17:34:12Z
completed	success	docs(fine-task): handoff sonda E2E calcola() Gemini 2026-09-01 — 2 PASS	CI	sonda/e2e-calcola-gemini-2026-09-01	push	33536737891	50s	2026-09-01T17:15:53Z
completed	success	docs(sonda): E2E calcola() Gemini — 2 PASS 2026-09-01	CI	sonda/e2e-calcola-gemini-2026-09-01	push	33536359930	49s	2026-09-01T17:12:02Z
```

Mappatura commit→run:
- `d7e2d35` → run 33538544336 ✅ SUCCESS (commit di testa al push precedente)
- `179fb12` → nessuna run su questo SHA (commit intermedio, testato nell'albero di `d7e2d35`)
- `6719e9f` → run 33536359930 ✅ SUCCESS (commit di testa al suo push)
- commit di questa sessione → run non ancora disponibile alla scrittura dell'handoff

---

## §7 RISERVE APERTE

Nessuna nuova dalla sessione corrente (nessun diff motore).

Finding pre-esistenti confermati nel reporting (non chiusi da questa sessione):
- 🟡 **F1 CRITICO** — causa radice ancora aperta: `gas.py:46-48` system prompt + SHELL_ALLOWLIST senza calcolatori. Fix motore non impegnato; richiede scope dall'operatore.
- 🟡 **Groq contraddittorio** — diagnosi 2026-08-29 "Groq rifiuta" vs sonda PR #78 "Groq 2 PASS". Da riconciliare prima di qualsiasi dichiarazione definitiva su Groq.
- 🟡 **Attribuzione "Groq-specifico"** — ipotesi non verificata empiricamente. Groq non testato nella sonda 2026-09-01.
