# Report — Chiusura riserve A e C della review #44

**Data:** 2026-07-13
**Branch:** fix/review44-riserve-AC
**PR:** #4 — https://github.com/Gasss23/Gas/pull/4
**Commit motore:** abc0894
**Commit report:** 030cf21
**Review revisore:** #45 — APPROVATO (nessuna riserva)

---

## DECISIONI UMANE RICHIESTE

- Merge PR #4 (dopo CI verde — già SUCCESS su entrambi i commit di sessione).
- Riserva B (prezzi Groq $0.15/$0.60): verificare sulla pricing page di Groq al deploy VPS. Fuori scope di questa sessione.

---

## Esito fette

- **Fetta A — commento inline reasoning_effort**: `FATTA`
  Aggiunto commento in `brains/groq_brain.py`, `brains/claude_brain.py`, `brains/gemini_brain.py`.

- **Fetta B — verifica prezzi Groq**: `SALTATA — esplicitamente fuori scope per istruzione operatore`
  Riserva B resta aperta in stato_progetto.md.

- **Fetta C — T36c usa costante MODEL_GROQ**: `FATTA`
  Sostituito literal `"openai/gpt-oss-120b"` con `MODEL_GROQ` in T36c; aggiunto import top-level.

---

## Suite test

**217 PASS, 0 FAIL**
Ambiente: Codespace. I test bwrap (T9a/T9c, T13a-T13e) non sono validabili localmente — verifica bwrap reale demandata a CI/WSL.

---

## Anomalie / note

Nessuna anomalia. Il grep ha rivelato che `reasoning_effort: "low"` è presente in tre file (groq_brain.py, claude_brain.py, gemini_brain.py) — non solo nel brain principale. Commentati tutti e tre per coerenza.
