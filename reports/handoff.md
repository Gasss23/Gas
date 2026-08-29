# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-08-29 — Diagnosi bug "kernel rifiuta 7×8 in text-only mode"

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #77 (https://github.com/Gasss23/Gas/pull/77).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Verifica subagent revisore**: `FATTA` — `revisore.md` e `memoria_revisore.md` presenti in `.claude/agents/`.
- **Fetta 2 — Riproduzione bug con input reale**: `FATTA` — bug riprodotto due volte (`7×8` e `sette per otto`) con `venv/bin/python3` + chiavi da `.env`. Output verbatim catturato.
- **Fetta 3 — Isolamento causa radice**: `FATTA` — causa radice identificata: tensione system-prompt `gas.py:50-55` vs SHELL_ALLOWLIST `gas.py:874-878` (nessun tool aritmetico). Zero tool call tentate dal modello. Pipeline funzionante, bug semantico.
- **Fetta 4 — Fix**: `SALTATA — out-of-scope per design`. Task era diagnosi read-only. Tre opzioni di fix proposte in `reports/ultimo_report.md §4`; decisione all'operatore.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md  |  19 +--
 reports/handoff.md        |  48 +++----
 reports/stato_progetto.md |  34 ++++-
 reports/ultimo_report.md  | 312 +++++++++++++++-------------------------------
 4 files changed, 153 insertions(+), 260 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
e0afbd1 docs(diagnosi): bug kernel-rifiuta-7x8 — causa radice isolata (system-prompt vs allowlist)
b0dde4c docs(fine-task): handoff + diff_sessione sonda VPS 2026-08-26 — PR #77
b7ab347 docs(sonda-vps): fotografia deploy GAS 2026-08-26 — VPS stabile, 391 commit dietro origin/main
cab1352 docs(sonda-vps): §0 handoff — PR #77 e istruzioni sblocco SSH
3cde16b docs(sonda-vps): report sonda VPS 2026-08-26 — task SALTATA (SSH non configurato)
```

NB: il commit di fine-task (questo handoff) non compare qui per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore (gas.py, brains/, modules/, tests/ non toccati). Revisore non richiesto.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

---

## §6 STATO CI

```
completed	success	docs(diagnosi): bug kernel-rifiuta-7x8 — causa radice isolata (system…	CI	sonda/vps-stato-2026-08-26	push	33255140643	54s	2026-08-29T13:29:25Z
completed	success	docs(fine-task): handoff + diff_sessione sonda VPS 2026-08-26 — PR #77	CI	sonda/vps-stato-2026-08-26	push	33020640833	52s	2026-08-26T22:44:35Z
completed	failure	docs(sonda-vps): fotografia deploy GAS 2026-08-26 — VPS stabile, 391 …	CI	sonda/vps-stato-2026-08-26	push	33018077555	46s	2026-08-26T22:04:14Z
```

**Mappatura commit→run:**
- `e0afbd1` (docs(diagnosi): bug kernel-rifiuta-7x8…) → run `33255140643` — **SUCCESS** ✅ (push singolo, testa questo commit)
- `b0dde4c` (docs(fine-task): handoff…) → run `33020640833` — **SUCCESS** ✅
- `b7ab347`, `cab1352`, `3cde16b` → run `33018077555` — **FAILURE** ❌ (sessione precedente)
- Commit di fine-task corrente → nessuna run ancora disponibile alla scrittura dell'handoff

---

## §7 RISERVE APERTE

- **kernel rifiuta 7×8** (diagnosticato questa sessione): causa radice isolata — system prompt `gas.py:50-55` forza run_command per calcoli; SHELL_ALLOWLIST `gas.py:874-878` priva di tool aritmetici. Tre opzioni di fix in `reports/ultimo_report.md §4`. Decisione e fetta di fix all'operatore.
- **R-finegat-1** (portata da sessione precedente): `PR_JSON=$(gh pr list ... 2>&1)` — stderr misto produce testo non-JSON con exit 0.
- **R-finegat-2** (portata da sessione precedente): pattern `GH_EXIT=$?; if [ $GH_EXIT -ne 0 ]` non-atomico.
