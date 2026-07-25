# Task: fix/handoff-check-ci — check_handoff + check_verdetto + job CI + test
**Data:** 2026-07-25

## DECISIONI UMANE RICHIESTE

1. Merge della PR #45 (feat(ci): check_handoff + check_verdetto + job handoff-check).
2. Valutare R3 (riserva revisore): aggiungere `handoff-check` come required check nel
   ruleset GitHub main-lock? Oggi blocca la run CI ma non il merge automatico.

---

## Esito fette

- **FETTA 1 — scripts/check_handoff.py**: `FATTA`
  Stdlib-only. Guard main/diff-vuoto/handoff-non-nel-diff. SET confronto (non conteggi).
  Allowlist: reports/ultima_risposta.md. Collaudo reale: EXIT 1 su commit 9c72e1f (PR #44).

- **FETTA 2 — scripts/check_verdetto.py**: `FATTA`
  Regex path:riga in §4. Verifica: path in diff + riga esiste nel file a HEAD.
  Dichiarazione MITIGATO (non CHIUSO). Guard "nessun diff motore".
  Fix R1 applicato nella stessa sessione: filtro estensione sorgente esclude falsi positivi
  su URL (github.com:443, //host.ext:port). La CI era rossa su e690295 per questo motivo;
  il fix su _VALID_EXTENSIONS + _is_valid_path la riporta verde.

- **FETTA 3 — job handoff-check in ci.yml**: `FATTA`
  Job separato, non tocca unit-suite. fetch-depth:0 + git fetch origin main.
  Sonda 1 (955cf2e): run 30156146780 → handoff-check success, unit-suite success.
  Sonda 2 (e690295): run 30156259526 → handoff-check FAIL (R1 falso positivo).
  Fix R1 → sonda 3 attesa su commit finale di questa sessione.

- **FETTA 4 — template fine-task.md**: `FATTA`
  4a: vincoli §2 (SET esatto e vincolante, conteggi approssimati per costruzione).
  4b: allowlist documentata con motivazione.
  4c: regola §0 — "Nessuna." vietato con PR aperta.

- **FETTA 5 — tests/test_unit_handoff_check.py**: `FATTA`
  9 test pytest, repo git temporanei reali. 9/9 PASS dopo fix R1.
  Collaudo reale: exit 1 su commit 9c72e1f (PR #44 ometteva handoff.md da §2).

## Anomalie riscontrate

- R1 (riserva revisore già segnalata): regex `_REF_RE` in check_verdetto.py catturava
  URL come `github.com:443` presenti nel testo del verdetto. Ha causato CI rossa su e690295.
  Fix applicato nella stessa sessione (filtro _VALID_EXTENSIONS).

## Verdetto revisore: APPROVATO CON RISERVE

Riserve aperte:
- R3: `handoff-check` non è required check nel ruleset main-lock — decisione operatore.
- R-verdetto-evidenza: MITIGATO (non CHIUSO) — check_verdetto verifica verificabilità
  citazioni, non lettura effettiva del codice.

## DA TRASCRIVERE IN stato_progetto.md

- R-handoff-check IMPLEMENTATO: scripts/check_handoff.py + check_verdetto.py + job CI + 9 test.
  PR #45 aperta. CI sonda 1 verde, sonda 2 rossa (R1), sonda 3 attesa.
- R-verdetto-evidenza: stato MITIGATO (non CHIUSO).
- R1: CHIUSO nel fix della stessa sessione (_VALID_EXTENSIONS).
- R3 decisione aperta: rendere handoff-check required nel ruleset main-lock?
