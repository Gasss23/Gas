# DIFF SESSIONE — 2026-10-04 — fix/handoff-check-vincolante

| File | Cosa è cambiato e perché |
|---|---|
| `scripts/check_handoff.py` | Errore se la sessione tocca il perimetro e l'handoff manca dal diff (V-A); errore se merge-base o git diff falliscono (R-141-1); docstring. |
| `scripts/check_verdetto.py` | Controlli sull'handoff dopo il calcolo del perimetro; errore per handoff o §4 mancanti nel perimetro (V-A); git diff fallito → errore (R-141-1). |
| `.claude/hooks/review_gate.sh` | Tolto il commento duplicato (cosmetica #140). |
| `tests/test_unit_handoff_check.py` | Test V-A (perimetro senza handoff, doc senza handoff, §4 rinominata, merge-base) e R-141-1. |
| `.claude/agents/memoria_revisore.md` | Memoria delle review #141 e #142. |
| `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` | Report di fine task; correzione V-3. |

La storia completa sta in git.
