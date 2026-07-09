# REPORT — 2026-07-09 — TASK DOC-ONLY: allineamento canonici a git reale (3 fix)

## DECISIONI UMANE RICHIESTE

Nessuna.

---

## Scope

Task doc-only: toccati SOLO `reports/roadmap.md`, `reports/stato_progetto.md`,
`reports/ultimo_report.md`. Zero file di motore. Nessuna review revisore.
Push diretto su main (policy doc-only).

---

## Esito per punto

### Fix 1 — roadmap.md §PROSSIMI PASSI item 8 "Config-drift stringhe modello"

**FATTA.** Da `Stato: APERTO` a:

> ✅ **Config-drift stringhe modello** — `brains/model_ids.py` = fonte unica dei
> 5 ID cascata, env-overridabili (`GAS_MODEL_*`). Merge `eb0509f`, commit
> `160543a`, review #43, 2026-07-07. **CHIUSO**.

### Fix 2 — roadmap.md §PROSSIMI PASSI item 1 + §Deprecazioni primo bullet

**FATTA.**

Item 1 da `validazione live: PENDING` a:

> ✅ **Migrazione rung Groq** — `llama-3.3-70b-versatile` → `openai/gpt-oss-120b`.
> Validazione live OK (STATUS 200, tool_calls parsate, `reasoning_effort: "low"`,
> latenza 1138ms). Commit `f028e51`, review #44 APPROVATO CON RISERVE, 2026-07-08.
> **COMPLETATA**.

§Deprecazioni primo bullet da `PENDING` a:

> ✅ 2026-07-08 — Groq llama-3.3-70b-versatile → openai/gpt-oss-120b:
> **COMPLETATA**. Commit `f028e51`, review #44 APPROVATO CON RISERVE,
> validazione live OK (STATUS 200, tool_calls parsate, `reasoning_effort: "low"`).
> R-groq-slash e R-groq-dup CHIUSI. $0.15/$0.60 per MTok.

### Fix 3 — stato_progetto.md §Stato motore riga CI

**FATTA.** Run ID letto da `gh run list --branch main --limit 5` (NON da memoria).

Ultimo run SUCCESS su main al momento del task: **run #29031945029** su `87ad26f`
("docs(report): verifica re-esecuzione task doc-only 2026-07-07"), 2026-07-09T16:03:15Z.

Sostituito:

> `CI GitHub Actions: run #28665577327 su `51f9e1e` [mojibake] **SUCCESS** [mojibake] (ultimo run pre-sonda).`

con:

> `CI GitHub Actions: run #29031945029 su `87ad26f` ✅ **SUCCESS** ✅ (ultimo run su main, 2026-07-09).`

Nota tecnica: la riga originale conteneva checkmark mojibake (doppia codifica
UTF-8, con U+0085 NEL incorporato) che impediva la sostituzione testuale standard.
Risolto con sostituzione byte-level in PowerShell.

---

## Note operative

- Zero token LLM runtime; run CI letto via `gh` (metadati).
- File toccati: `reports/roadmap.md`, `reports/stato_progetto.md`,
  `reports/ultimo_report.md`.
