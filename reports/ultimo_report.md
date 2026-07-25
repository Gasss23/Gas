# Task: fix/handoff-check-ci — check_handoff + check_verdetto + job CI + test
**Data:** 2026-07-25

## DECISIONI UMANE RICHIESTE

1. Merge della PR #45 (feat(ci): check_handoff + check_verdetto + job handoff-check).
2. Valutare R3 (riserva revisore): aggiungere `handoff-check` come required check nel ruleset GitHub main-lock? Oggi il job è informativo — blocca la run CI ma non blocca il merge. Decisione operatore.

---

## Esito fette

- **FETTA 1 — scripts/check_handoff.py**: `FATTA`
  Stdlib-only. Guard main/diff-vuoto/handoff-non-nel-diff. SET confronto (non conteggi).
  Allowlist: reports/ultima_risposta.md. Collaudo reale: EXIT 1 su 9c72e1f/PR#44.

- **FETTA 2 — scripts/check_verdetto.py**: `FATTA`
  Regex path:riga in §4. Verifica: path in diff + riga esiste in file a HEAD.
  Dichiarazione MITIGATO (non CHIUSO) nell'output. Guard "nessun diff motore".

- **FETTA 3 — job handoff-check in ci.yml**: `FATTA`
  Job separato, non tocca unit-suite. fetch-depth:0 + git fetch origin main.
  Sonda eseguita: run 30156146780 → handoff-check success, unit-suite success.

- **FETTA 4 — template fine-task.md**: `FATTA`
  4a: vincoli §2 (SET esatto e vincolante, conteggi approssimati per costruzione).
  4b: allowlist documentata con motivazione.
  4c: regola §0 — "Nessuna." vietato con PR aperta.

- **FETTA 5 — tests/test_unit_handoff_check.py**: `FATTA`
  9 test pytest, repo git temporanei reali. Tutti PASS.
  Collaudo reale: exit 1 su commit 9c72e1f (merge PR #44 ometteva handoff.md).

## Verdetto revisore: APPROVATO CON RISERVE

R1: regex `_REF_RE` in check_verdetto può fare falsi positivi su URL nel verdetto.
R3: `handoff-check` non è required check nel ruleset main-lock — decisione operatore.

## DA TRASCRIVERE IN stato_progetto.md

- R-handoff-check IMPLEMENTATO: scripts/check_handoff.py + check_verdetto.py + job CI + 9 test.
  PR #45 aperta, CI verde (run 30156146780), sonda superata.
- R-verdetto-evidenza: stato MITIGATO (non CHIUSO) — check_verdetto.py verifica
  che le citazioni path:riga siano verificabili, non che il revisore abbia letto il codice.
- R1 riserva aperta: regex _REF_RE falsi positivi su URL — da raffinare.
- R3 decisione aperta: rendere handoff-check required nel ruleset main-lock?
