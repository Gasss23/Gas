# DIFF SESSIONE — 2026-10-08 — `rifletti` logga la risposta scartata

File toccati (rispetto a main `3ab900a`):

- `gas.py` — `_analizza_riflessione` (parser + motivo preciso dello scarto), `_anteprima_log` (inizio 300 + coda 150 char, repr su una riga), warning di scarto in `rifletti()` con motivo/finish_reason/lunghezza/anteprima. Perché: Gemini scartato sul Mac senza diagnosi possibile.
- `tests/test_unit_kernel.py` — T80l2, T80l3, T80u2, T80u3.
- `.claude/agents/memoria_revisore.md` — righe contatore review #210–#214 (+ lezione su `s[-0:]`).
- `reports/stato_progetto.md` — voce 9: logging fatto, prossimo passo sul Mac.
- `reports/ultimo_report.md` — report di questo task.
- `reports/handoff.md` — dossier di fine sessione.
- `reports/diff_sessione.md` — questo file.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
