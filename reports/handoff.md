# HANDOFF — cert/mac-migration-2026-09-12 — 2026-09-12

---

## §DECISIONI UMANE RICHIESTE

1. **Merge PR #87** (cert/mac-migration-2026-09-12 → main) — doc-only, CI verde. Nessun codice motore toccato; auto-merge consentito dal ruleset.

2. **F-mac-4: fix IP guard su Mac** — `scripts/gasmerge.sh` usa `git grep -E '\b...\b'`; macOS POSIX ERE non supporta `\b` → IP non rilevati localmente. Fix proposto: `git grep -nP '\b...\b'` (PCRE flag) o grep esterno. Decidere se fixare ora o aspettare il deploy VPS (dove non impatta).

3. **F-mac-1: SKIP bwrap tests su macOS** — T11c2/T11e/T12a/T12c/T12e sono FAIL su Mac ma PASS su CI (Ubuntu). Fix test-only (non urgente, il runtime è corretto).

---

## ESITO SONDA / CERTIFICAZIONE

**MIGRAZIONE CERTIFICATA ✅** — L1+L2+L3 PASS, zero crash, zero danni ai dati.

Vedi `reports/ultimo_report.md` per il dettaglio completo.

---

## `git diff --stat` REALE DELLA SESSIONE

```
 reports/stato_progetto.md |   3 +-
 reports/ultimo_report.md  | 166 +++++++++++++++++++++++++++++++++++++++------
 2 files changed, 148 insertions(+), 21 deletions(-)
```

---

## `git log` DEI COMMIT DELLA SESSIONE

```
1c4f084 docs(cert-mac): certificazione migrazione Win/WSL→Mac — 2026-09-12
```

---

## DELTA TEST DEL MOTORE

Nessuna modifica al motore (gas.py, brains/, modules/, tests/) in questa sessione.  
**Revisore: NON INVOCATO** (doc-only, regola CLAUDE.md §3 — commit di soli reports/ non richiedono review).

Risultati suite osservati durante la certificazione (non da commit, da run reale su Mac):
- `python tests/test_unit_kernel.py`: **290 PASS / 5 FAIL** (tutti bwrap — baseline Mac confermato)
- `pytest tests/` (escluso test_unit_kernel.py): **111 PASS / 10 FAIL** (tutti gasmerge IP-guard — F-mac-4)

---

## VERDETTO INTEGRALE REVISORE

**NON APPLICABILE** — nessuna modifica al codice motore in questa sessione. Commit di soli `reports/`.

---

## STATO / ESITO ULTIMA RUN CI

| Campo | Valore |
|-------|--------|
| Branch | cert/mac-migration-2026-09-12 |
| Trigger | push |
| Run ID | 34658666540 |
| Esito | **success ✅** |
| Durata | 52s |
| Timestamp | 2026-09-11T23:35:58Z |

CI verde: il push doc-only ha superato il check `unit-suite` (corre su Ubuntu, bwrap disponibile).
