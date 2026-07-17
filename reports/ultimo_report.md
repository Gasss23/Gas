# ultimo_report — docs/sanitize-post-pr21 — F0 + F1-bis + F2-bis — 2026-07-17

## §0 DECISIONI UMANE RICHIESTE

1. **R-ci-hooks — task separato (fuori scope)**: `tests/test_unit_hooks.py` (T-hook-a/b/c/d/e/f/g) non è eseguito da CI. Decidere se aggiungere `python tests/test_unit_hooks.py` al job `unit-suite` in `ci.yml`. Tocca `ci.yml` → task separato; non committato qui.
2. **Merge PR docs/sanitize-post-pr21 → main** — solo doc/report, CI run 29570876259 ✅ SUCCESS, self-merge consentito.

---

## §1 SCOPE & ESITO FETTE

- **F0 — Verifica hash merge (PR #21 e PR #19)**: `FATTA` — hash confermati dall'operatore; output verbatim di `git log origin/main --merges --oneline -5` nel report. PR #21 → `8f9cf7b`, PR #19 → `9a9278e`.
- **F1-bis — Sonda CI unit-suite (SOLA LETTURA)**: `FATTA` — contraddizione sciolta: CI usa `python tests/test_unit_kernel.py` (non pytest), exit code reale (`sys.exit(1 if FAIL else 0)` riga 3302, livello modulo). Gap scoperto: `tests/test_unit_hooks.py` non eseguito da CI. Finding R-ci-hooks aperto.
- **F2-bis — Completamento reports/stato_progetto.md**: `FATTA` — 5 punti verificati: (a)(b) da FETTA 2 precedente; (c) blocco discrepanza contatore rimosso; (d) finding R-ci-hooks aggiunto; (e) header aggiornato.

---

## §2 ANOMALIE

- Precedente /fine-task: il handoff non conteneva ci.yml verbatim né le risposte F1-bis puntuali — era un rimando al report. Corretto in questa esecuzione: handoff ora autocontenuto.
- Precedente risposta tabulare: `8b37a4c` indicato come merge PR #17 invece di `e7b4486`. Regola salvata in memoria: output git va sempre incollato verbatim.
