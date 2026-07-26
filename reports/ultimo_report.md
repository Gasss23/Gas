# REPORT FINE TASK — fix/gasmerge-failopen (sessione 2026-07-26)

**Data:** 2026-07-26  
**Branch:** fix/gasmerge-failopen (PR #46)  
**Scope:** FETTE 0–4 (nuovi fix R-gasmerge-failopen: invariante IP + TOCTOU + test)

---

## DECISIONI UMANE RICHIESTE

### D1 — Risoluzione conflitti di merge (BLOCCANTE)

Il `git merge --no-edit origin/main` sul branch `fix/gasmerge-failopen` ha prodotto conflitti su 4 file doc:

```
.claude/agents/memoria_revisore.md
reports/diff_sessione.md
reports/handoff.md
reports/ultimo_report.md
```

Le istruzioni di sessione mandano a **FERMARSI** e non risolvere a occhio.

**Opzioni proposte:**

1. **Risolvi manualmente** — apri i 4 file, tieni la versione preferita, poi `git merge --continue`.
2. **`git merge -X theirs origin/main`** — accetta la versione di main per tutti i conflitti doc (nessun conflitto tocca gasmerge.sh o i test → zero rischio motore). Raccomandato.
3. **Branch fresco** — `git checkout -b fix/gasmerge-failopen-v2 origin/main` + cherry-pick dei 4 commit di lavoro.

---

## ESITO FETTE

- **FETTA 0 — allineamento branch**: `STOP` — conflitti merge su 4 file doc, come da istruzioni nessuna risoluzione autonoma effettuata. Il merge è stato abortito (`git merge --abort`), branch è allo stato pulito `origin/fix/gasmerge-failopen`.

- **FETTA 1 — invariante IP**: `NON INIZIATA` — bloccata da FETTA 0.

- **FETTA 2 — TOCTOU**: `NON INIZIATA` — bloccata da FETTA 0.

- **FETTA 3 — test**: `NON INIZIATA` — bloccata da FETTA 0.

- **FETTA 4 — registrazione stato_progetto.md**: `NON INIZIATA` — bloccata da FETTA 0.

---

## NOTE

- Il branch `fix/gasmerge-failopen` è **pulito** e punta a `origin/fix/gasmerge-failopen` (ultima sessione 2026-07-25).
- I conflitti sono **tutti su file doc/report**, nessun conflitto su `scripts/gasmerge.sh` o `tests/test_unit_gasmerge.py`.
- La causa: PR #45 (mergiata in main il 2026-07-25) aveva aggiornato gli stessi file doc che il branch aveva modificato indipendentemente.
