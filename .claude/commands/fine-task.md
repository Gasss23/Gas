# /fine-task — Reporting canonico di fine task

Esegui queste operazioni NELL'ORDINE, senza saltare passi.

## 1. Scrivi reports/ultimo_report.md

Contenuto obbligatorio:
- Data e titolo del task
- Esito riga-per-riga di ogni fetta/step eseguito
- DECISIONI UMANE RICHIESTE (se esistono, in cima al file)
- Eventuali anomalie riscontrate

## 2. Committa e pusha

```
git add reports/ultimo_report.md [altri file doc toccati in questo task]
git commit -m "docs(<descrizione-breve>): <cosa hai fatto>"
git push
```

NON includere nel commit file del motore (gas.py, brains/, modules/, tests/) — quelli richiedono il revisore.

## 3. Stampa a terminale ESATTAMENTE (senza riassumere):

1. Path del report: `reports/ultimo_report.md`
2. Hash del commit (output di `git rev-parse HEAD`)
3. Contenuto integrale del file (output di `cat reports/ultimo_report.md`)
4. Diff reale della sessione (output di `git diff --stat HEAD~1 HEAD`)

## INVARIANTE

Non dare MAI a voce un riassunto diverso dal contenuto del file. Ogni discrepanza tra ciò che dici e ciò che sta nel file è un errore da segnalare.
