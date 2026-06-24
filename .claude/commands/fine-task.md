# /fine-task — Reporting canonico di fine task

Esegui queste operazioni NELL'ORDINE, senza saltare passi.

---

## 0. Raccogli i dati grezzi (PRIMA di scrivere qualsiasi file)

Esegui questi comandi e tieni l'output — lo incolli verbatim nei file sotto:

```bash
git log --oneline -15
git diff --stat HEAD~1 HEAD   # aggiusta ~N se hai fatto più commit in questa sessione
```

---

## 1. Scrivi reports/ultimo_report.md

Contenuto obbligatorio:
- Data e titolo del task
- Esito riga-per-riga di ogni fetta/step eseguito
- DECISIONI UMANE RICHIESTE (se esistono, in cima al file)
- Eventuali anomalie riscontrate

---

## 2. Scrivi reports/handoff.md

Template obbligatorio (sezioni in quest'ordine):

```markdown
# HANDOFF — Dossier di fine sessione

**Sessione:** <data> — <titolo task>

---

## §DECISIONI UMANE RICHIESTE

<lista numerata, o "Nessuna." se vuota>

---

## ESITO / CONTESTO

<sintesi tecnica del task: cosa è stato fatto e perché>

---

## GIT LOG --ONELINE (sessione)

```
<output GREZZO di `git log --oneline -15` — nessuna modifica>
```

## GIT DIFF --STAT (sessione)

```
<output GREZZO di `git diff --stat HEAD~N HEAD`>
```

## DELTA TEST DEL MOTORE

<"0. Nessuna modifica a gas.py/tests/" OPPURE esito della suite>

## VERDETTO DEL REVISORE

<verdetto INTEGRALE del revisore se il task ha toccato il motore, altrimenti "Non applicabile — task non-motore.">

## STATO CI

<esito ultima run CI visibile su GitHub Actions, o "Da verificare post-push.">
```

---

## 3. Scrivi reports/diff_sessione.md

Contenuto:
- File toccati in questa sessione (da `git diff --stat`)
- Per ogni file: cosa è cambiato e perché (una riga)
- Nota: questo file si riscrive a ogni sessione; la storia completa sta in git

---

## 4. Committa e pusha

```bash
git add reports/ultimo_report.md reports/handoff.md reports/diff_sessione.md
git commit -m "docs(<descrizione-breve>): <cosa hai fatto>"
git push
```

NON includere nel commit file del motore (gas.py, brains/, modules/, tests/) — quelli richiedono il revisore.

---

## 5. Stampa a terminale ESATTAMENTE (senza riassumere):

1. Path del report: `reports/ultimo_report.md`
2. Hash del commit (output di `git rev-parse HEAD`)
3. Contenuto integrale di `reports/ultimo_report.md`
4. Contenuto integrale di `reports/handoff.md`

---

## INVARIANTE

Non dare MAI a voce un riassunto diverso dal contenuto dei file. Ogni discrepanza tra ciò che dici e ciò che sta nei file è un errore da segnalare.
