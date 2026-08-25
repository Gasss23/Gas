# Audit read-only branch remoti — 2026-08-25

**Task**: classificazione di tutti i branch remoti ≠ main.
**Metodo**: read-only puro — zero cancellazioni, zero modifiche motore.
**Branch di lavoro**: `chore/audit-branch-remoti`

---

## Riepilogo esecutivo

| Branch | behind | ahead | rc | Classificazione |
|--------|-------:|------:|:--:|-----------------|
| `docs/scollega-gashistory-r2-v2` | 29 | 0 | 0 | ✅ SAFE-DA-CANCELLARE |
| `fix/r2-durabilita-memoria-clean` | 39 | 0 | 0 | ✅ SAFE-DA-CANCELLARE |
| `fix/r2-riserve-86` | 31 | 0 | 0 | ✅ SAFE-DA-CANCELLARE |
| `claude/phone-gas-development-10svqc` | 386 | 7 | 1 | ⛔ DA-GIUDICARE-A-MANO |
| `docs/scollega-gashistory-da-r2` | 38 | 1 | 1 | ⛔ DA-GIUDICARE-A-MANO |
| `fix/crm-idemp-diario` | 225 | 1 | 1 | ⛔ DA-GIUDICARE-A-MANO |
| `fix/nonascii-cd-tests` | 45 | 4 | 1 | ⛔ DA-GIUDICARE-A-MANO |
| `fix/r2-durabilita-memoria` | 45 | 9 | 1 | ⛔ DA-GIUDICARE-A-MANO |
| `fix/review44-riserve-AC` | 328 | 2 | 1 | ⛔ DA-GIUDICARE-A-MANO |

Legenda colonne: `behind` = commit in main NON nel branch; `ahead` = commit nel branch NON su main; `rc` = exit code di `git merge-base --is-ancestor origin/<b> origin/main` (rc=0 → tip già su main = contenuto interamente mergiato).

---

## Evidenza verbatim per branch

### git fetch --prune output

```
$ git remote update --prune
$ git branch -r | grep -v HEAD | sort
  origin/claude/phone-gas-development-10svqc
  origin/docs/scollega-gashistory-da-r2
  origin/docs/scollega-gashistory-r2-v2
  origin/fix/crm-idemp-diario
  origin/fix/nonascii-cd-tests
  origin/fix/r2-durabilita-memoria
  origin/fix/r2-durabilita-memoria-clean
  origin/fix/r2-riserve-86
  origin/fix/review44-riserve-AC
  origin/main
```

---

### ✅ docs/scollega-gashistory-r2-v2

```
$ git rev-list --left-right --count origin/main...origin/docs/scollega-gashistory-r2-v2
29	0
$ git merge-base --is-ancestor origin/docs/scollega-gashistory-r2-v2 origin/main; echo "rc=$?"
rc=0
```

**Conclusione**: tip già su main. SAFE-DA-CANCELLARE.

---

### ✅ fix/r2-durabilita-memoria-clean

```
$ git rev-list --left-right --count origin/main...origin/fix/r2-durabilita-memoria-clean
39	0
$ git merge-base --is-ancestor origin/fix/r2-durabilita-memoria-clean origin/main; echo "rc=$?"
rc=0
```

**Conclusione**: tip già su main. SAFE-DA-CANCELLARE.

---

### ✅ fix/r2-riserve-86

```
$ git rev-list --left-right --count origin/main...origin/fix/r2-riserve-86
31	0
$ git merge-base --is-ancestor origin/fix/r2-riserve-86 origin/main; echo "rc=$?"
rc=0
```

**Conclusione**: tip già su main. SAFE-DA-CANCELLARE.

---

### ⛔ claude/phone-gas-development-10svqc

```
$ git rev-list --left-right --count origin/main...origin/claude/phone-gas-development-10svqc
386	7
$ git merge-base --is-ancestor origin/claude/phone-gas-development-10svqc origin/main; echo "rc=$?"
rc=1

$ git log --oneline origin/main..origin/claude/phone-gas-development-10svqc
384f4f5 docs(handoff): sessione 2026-07-09 — migrazione Groq gpt-oss-120b + doc roadmap
fa212a6 docs(roadmap): Dispatch candidato accesso dev telefono, Telegram ridimensionato, PARK Cowork
cec8e9f chore(revisore): lezione #41 in memoria persistente (migrazione modello rung)
4137921 feat(brains): migra rung Groq a openai/gpt-oss-120b con reasoning_effort low
c67137e docs(roadmap): PARK item Mirage VFS
20f3d9b docs: confine telefono + bloccante postazione FASE 5 + raccomandazione repo privato
2da9513 docs(sonda): caratterizzazione ambiente cloud CC da telefono

$ git diff --name-only origin/main...origin/claude/phone-gas-development-10svqc
.claude/agents/memoria_revisore.md
brains/claude_brain.py
brains/gemini_brain.py
brains/groq_brain.py
reports/handoff.md
reports/raccomandazioni_aperte.md
reports/roadmap.md
reports/stato_progetto.md
reports/ultimo_report.md
```

**Nota**: tocca `brains/groq_brain.py` (migrazione modello), `brains/claude_brain.py`, `brains/gemini_brain.py`. Commit `4137921 feat(brains)` è codice motore non mergiato. DA-GIUDICARE-A-MANO.

---

### ⛔ docs/scollega-gashistory-da-r2

```
$ git rev-list --left-right --count origin/main...origin/docs/scollega-gashistory-da-r2
38	1
$ git merge-base --is-ancestor origin/docs/scollega-gashistory-da-r2 origin/main; echo "rc=$?"
rc=1

$ git log --oneline origin/main..origin/docs/scollega-gashistory-da-r2
0ef845c docs(stato): scollega .gas_history.json da etichetta R2 + finding autonomo

$ git diff --name-only origin/main...origin/docs/scollega-gashistory-da-r2
reports/stato_progetto.md
reports/ultimo_report.md
```

**Nota**: 1 commit doc-only, tocca solo reports/. Il finding su .gas_history.json potrebbe essere già assorbito da main (R2 chiuso in PR #66+#87), ma la decisione spetta all'operatore. DA-GIUDICARE-A-MANO.

---

### ⛔ fix/crm-idemp-diario

```
$ git rev-list --left-right --count origin/main...origin/fix/crm-idemp-diario
225	1
$ git merge-base --is-ancestor origin/fix/crm-idemp-diario origin/main; echo "rc=$?"
rc=1

$ git log --oneline origin/main..origin/fix/crm-idemp-diario
1eff12f docs(stato): registra merge PR #27 su main (21548f74, CI 29695063005)

$ git diff --name-only origin/main...origin/fix/crm-idemp-diario
reports/stato_progetto.md
```

**Nota**: 1 commit doc-only, tocca solo reports/stato_progetto.md. Sembra uno stato-aggiornamento stale (225 commit indietro). DA-GIUDICARE-A-MANO.

---

### ⛔ fix/nonascii-cd-tests

```
$ git rev-list --left-right --count origin/main...origin/fix/nonascii-cd-tests
45	4
$ git merge-base --is-ancestor origin/fix/nonascii-cd-tests origin/main; echo "rc=$?"
rc=1

$ git log --oneline origin/main..origin/fix/nonascii-cd-tests
2c64ad2 docs(fine-task): handoff §2/§3/§6 rigenerati — run 32205642058 success
0186bf8 docs(fine-task): report fette A+B — T-gate-E e core.quotePath non-ASCII
1be14b3 fix(scripts): core.quotePath=false — path non-ASCII in git diff --name-only
7204077 test(hooks): T-gate-E — copre il caso cd fail in review_gate.sh

$ git diff --name-only origin/main...origin/fix/nonascii-cd-tests
.claude/agents/memoria_revisore.md
reports/diff_sessione.md
reports/handoff.md
reports/stato_progetto.md
reports/ultimo_report.md
scripts/check_handoff.py
scripts/check_verdetto.py
tests/test_unit_handoff_check.py
tests/test_unit_hooks.py
```

**Nota**: 4 commit, tocca scripts/ e tests/. Il fix core.quotePath (`1be14b3`) potrebbe essere già su main via PR #66 (`fix/quotepath-non-ascii` menzionato in stato_progetto.md §18). DA-GIUDICARE-A-MANO — verificare sovrapposizione con PR #66 prima di cancellare.

---

### ⛔ fix/r2-durabilita-memoria

```
$ git rev-list --left-right --count origin/main...origin/fix/r2-durabilita-memoria
45	9
$ git merge-base --is-ancestor origin/fix/r2-durabilita-memoria origin/main; echo "rc=$?"
rc=1

$ git log --oneline origin/main..origin/fix/r2-durabilita-memoria
d2b69bf docs(fine-task): handoff §2 corretto — 11 file inclusi revisore.md e commit_memoria_revisore.sh
3c153a1 docs(r2): stato_progetto + ultimo_report — R2 durabilità memoria implementata
7906580 feat(r2): commit atomico memoria_revisore.md — durabilità su interruzione
70d595f chore(revisore): memoria review #85 — APPROVATO CON RISERVE
6fbf300 docs(r2-sonda): sonda durabilità memoria + proposta design commit atomico al verdetto
2c64ad2 docs(fine-task): handoff §2/§3/§6 rigenerati — run 32205642058 success
0186bf8 docs(fine-task): report fette A+B — T-gate-E e core.quotePath non-ASCII
1be14b3 fix(scripts): core.quotePath=false — path non-ASCII in git diff --name-only
7204077 test(hooks): T-gate-E — copre il caso cd fail in review_gate.sh

$ git diff --name-only origin/main...origin/fix/r2-durabilita-memoria
.claude/agents/memoria_revisore.md
.claude/agents/revisore.md
reports/diff_sessione.md
reports/handoff.md
reports/stato_progetto.md
reports/ultimo_report.md
scripts/check_handoff.py
scripts/check_verdetto.py
scripts/commit_memoria_revisore.sh
tests/test_unit_handoff_check.py
tests/test_unit_hooks.py
```

**Nota**: 9 commit, include i 4 di fix/nonascii-cd-tests + 5 ulteriori. Tocca `scripts/commit_memoria_revisore.sh` (commit `7906580 feat(r2)`) — il contenuto di questo script è probabilmente già su main via `fix/r2-durabilita-memoria-clean` (PR #66/#87, ✅ su main). DA-GIUDICARE-A-MANO — la versione "clean" è su main, quella "originale" (questo branch) potrebbe avere delta di reports/docs.

---

### ⛔ fix/review44-riserve-AC

```
$ git rev-list --left-right --count origin/main...origin/fix/review44-riserve-AC
328	2
$ git merge-base --is-ancestor origin/fix/review44-riserve-AC origin/main; echo "rc=$?"
rc=1

$ git log --oneline origin/main..origin/fix/review44-riserve-AC
7e9bd7f docs(fine-task): handoff + ultimo_report + diff_sessione — update stato_progetto ref merge PR #4
ced5e34 docs(stato): chiude riserve #44 A+C con ref merge reale PR #4 (3836111) + CI 29235274026

$ git diff --name-only origin/main...origin/fix/review44-riserve-AC
reports/diff_sessione.md
reports/handoff.md
reports/stato_progetto.md
reports/ultimo_report.md
```

**Nota**: 2 commit doc-only, tocca solo reports/. Sembra uno stato-aggiornamento stale (328 commit indietro). DA-GIUDICARE-A-MANO.

---

## Suggerimento per l'operatore (NON eseguire senza verifica umana)

**Candidati alla cancellazione automaticamente sicuri** (rc=0 verificato):
```bash
# DA ESEGUIRE SOLO A MANO — mai da sessione agente (R6)
git push origin --delete docs/scollega-gashistory-r2-v2
git push origin --delete fix/r2-durabilita-memoria-clean
git push origin --delete fix/r2-riserve-86
```

**Candidati da esaminare prima di decidere**:
- `fix/crm-idemp-diario` (1 commit, 225 dietro): verificare se il contenuto di stato_progetto.md che aggiornava è già su main in forma diversa.
- `fix/review44-riserve-AC` (2 commit, 328 dietro): stesso ragionamento.
- `docs/scollega-gashistory-da-r2` (1 commit, 38 dietro): il finding R2 è chiuso — il commit doc probabilmente è superato.
- `fix/nonascii-cd-tests` / `fix/r2-durabilita-memoria` (9 commit): il codice fix è probabilmente già su main via fix/r2-durabilita-memoria-clean. Verificare con `git diff origin/main scripts/ tests/` prima di cancellare.
- `claude/phone-gas-development-10svqc` (7 commit, tocca brains/): la migrazione Groq rung (`feat(brains)`) potrebbe essere già su main o potrebbe essere una feature abbandonata. **Richiede verifica esplicita del diff brains/ vs main prima di qualsiasi azione**.
