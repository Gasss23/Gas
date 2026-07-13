# DIFF SESSIONE — 2026-07-13

> Riscritto a ogni sessione. Storia completa: git log.

**Task:** Chiusura riserve A e C della review #44
**Range:** b2a0a07..HEAD (branch fix/review44-riserve-AC)

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `brains/groq_brain.py` | Aggiunto commento 3 righe sopra `"reasoning_effort": "low"` — documenta il vincolo (gpt-oss-120b reasoning model) e il rischio di override. Fetta A. |
| `brains/claude_brain.py` | Aggiunto commento inline prima della chiamata Groq fallback — stesso razionale. Fetta A. |
| `brains/gemini_brain.py` | Aggiunto commento inline sopra `"reasoning_effort": "low"` nel fallback Groq. Fetta A. |
| `tests/test_unit_kernel.py` | Aggiunto `from brains.model_ids import MODEL_GROQ` top-level; T36c sostituisce literal `"openai/gpt-oss-120b"` con `MODEL_GROQ`. Fetta C. |
| `reports/stato_progetto.md` | Riserve A e C marchiate CHIUSE; riserva B confermata aperta. |
| `reports/ultimo_report.md` | Report del task riscritto. |
| `reports/handoff.md` | Dossier di fine sessione riscritto. |
| `CLAUDE.md` | Modifiche da sessioni precedenti (non di questa sessione). |
| `reports/roadmap.md` | Modifiche da sessioni precedenti (non di questa sessione). |
| `reports/ultima_risposta.md` | Aggiornato da hook scrivi_rep (sessioni precedenti). |
