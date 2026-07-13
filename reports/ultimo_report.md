# Report — Chiusura riserve A e C della review #44

**Data:** 2026-07-13
**Branch:** fix/review44-riserve-AC
**PR:** #4 — https://github.com/Gasss23/Gas/pull/4
**Commit motore:** abc0894
**Review revisore:** #45 — APPROVATO (nessuna riserva)

---

## Scope

Chiusura delle riserve A e C della review #44 (2026-07-08).
La riserva B (verifica prezzi Groq) è fuori scope di questa sessione e resta aperta in stato_progetto.md.

---

## Fetta A — Commento inline su reasoning_effort

`reasoning_effort: "low"` era presente in tre file (trovati via grep, non assunti):

- `brains/groq_brain.py` (payload principale Groq)
- `brains/claude_brain.py` (fallback Groq nel rung Claude/OpenRouter)
- `brains/gemini_brain.py` (fallback Groq nel rung Gemini)

Aggiunto commento inline in tutti e tre che documenta:
- perché "low" è obbligatorio: `gpt-oss-120b` è un reasoning model e il parametro è richiesto dall'API;
- cosa succede se `GAS_MODEL_GROQ` viene sovrascritto con un modello non-reasoning: Groq risponde 4xx (silente), il fail-safe §9 regge (fallthrough al rung successivo) ma la diagnostica è opaca.

Nessuna modifica alla logica. Solo commenti.

---

## Fetta C — T36c usa la costante MODEL_GROQ

In `tests/test_unit_kernel.py`:
- Aggiunto `from brains.model_ids import MODEL_GROQ` agli import top-level (riga 18).
- In T36c: `k36c._log_tokens("groq", "openai/gpt-oss-120b", 500, 100)` → `k36c._log_tokens("groq", MODEL_GROQ, 500, 100)`.

Il test continua a verificare la stessa cosa (che il log Groq usi il model ID canonico), ma ora è legato alla fonte unica: alla prossima migrazione il test si aggiorna automaticamente senza toccare il literal.

---

## Suite test

**217 PASS, 0 FAIL**
Ambiente: Codespace. I test bwrap (T9a/T9c, T13a-T13e) non sono validabili localmente — verifica bwrap reale demandata a CI/WSL.

---

## diff --stat reale della sessione

```
 brains/claude_brain.py    | 1 +
 brains/gemini_brain.py    | 1 +
 brains/groq_brain.py      | 3 +++
 tests/test_unit_kernel.py | 3 ++-
 4 files changed, 7 insertions(+), 1 deletion(-)
```

---

## Verdetto revisore #45 (integrale)

> **APPROVATO**
>
> Il diff chiude con precisione le riserve A e C della review #44, non introduce logica nuova, non tocca guardrail, non viola il Wall of Shame. La suite è verde. Nessuna riserva residua da tracciare.
>
> **Fetta A**: I commenti sono accurati e consistenti nei tre file. La posizione (dentro il dict literal) è sintatticamente valida. Il testo identifica il vincolo, documenta il rischio di override, cita §9. Applica direttamente la lezione 2026-07-08 della memoria revisore ("commento inline come mitigazione minima per parametri vincolati a capability del modello").
>
> **Fetta C**: Import posizionato correttamente dopo i top-level import esistenti. `brains/model_ids.py` è standalone, zero import di progetto, nessun rischio di import circolare. La sostituzione è semanticamente equivalente oggi e si aggiorna automaticamente alle future migrazioni. Chiude esattamente la riserva C.
>
> Lezioni nuove: nessuna (la lezione 2026-07-08 è già presente e questa fetta ne è l'applicazione diretta).

---

## Stato riserve review #44 post-sessione

| Riserva | Stato |
|---------|-------|
| A — commento reasoning_effort | CHIUSA (commit abc0894) |
| B — verifica prezzi Groq | APERTA (fuori scope, da fare al deploy VPS) |
| C — T36c literal -> costante | CHIUSA (commit abc0894) |

---

## Prossimi passi

- Merge PR #4 (dopo CI verde su unit-suite).
- Riserva B (prezzi Groq): confrontare $0.15/$0.60 con pricing page al deploy VPS.
