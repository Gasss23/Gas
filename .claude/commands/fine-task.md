# /fine-task — Reporting canonico di fine task

Esegui queste operazioni NELL'ORDINE, senza saltare passi.

---

## 0. Raccogli i dati grezzi (PRIMA di scrivere qualsiasi file)

Esegui questi comandi e tieni l'output — lo incolli verbatim nei file sotto:

```bash
git log --oneline -10
git diff --stat HEAD~N HEAD   # sostituisci N col numero di commit fatti in questa sessione
gh run list -L 3              # se gh disponibile e autenticato; altrimenti "CI NON VERIFICATA (gh assente)"
```

**REGOLA FERREA — output git verbatim**: incolla le righe grezze con hash e messaggi.
`"Ultimi 10 commit, tutti docs"` NON è accettabile — vanno le righe vere. Output grezzo o niente.

---

## 1. Scrivi reports/ultimo_report.md

Contenuto obbligatorio:
- Data e titolo del task
- Esito riga-per-riga di ogni fetta/step eseguito
- DECISIONI UMANE RICHIESTE (se esistono, in cima al file)
- Eventuali anomalie riscontrate

---

## 2. Scrivi reports/handoff.md

Il dossier deve essere AUTONOMO: un revisore esterno lo legge e ha tutto, zero follow-up.
Tutte le sezioni sono VERBATIM (mai parafrasi, mai riassunti al posto dell'output reale).

Template obbligatorio (sezioni in quest'ordine):

```markdown
# HANDOFF — Dossier di fine sessione

**Sessione:** <data> — <titolo task>

---

## §0 DECISIONI UMANE RICHIESTE

<lista numerata, o "Nessuna." se vuota>

---

## §1 SCOPE

<per ogni prompt/task della sessione: 1-3 righe su cosa chiedeva>

---

## §2 GIT DIFF --STAT (sessione)

```
<output GREZZO di `git diff --stat HEAD~N HEAD`>
```

## §3 GIT LOG --ONELINE (sessione)

```
<output GREZZO di `git log --oneline -10` — righe con hash e messaggi, nessuna modifica>
```

## §4 VERDETTO DEL REVISORE (per commit motore)

<Per OGNI commit che tocca gas.py/brains/modules/tests/: verdetto INTEGRALE del revisore,
incollato. Se nessun commit motore: "nessun diff motore, revisore non richiesto.">

## §5 DELTA TEST DEL MOTORE

<"Nessuna modifica a gas.py/tests/" OPPURE: numeri prima→dopo + blocco RIEPILOGO reale
incollato + quali FAIL sono fuori scope e perché>

## §6 STATO CI

<output REALE di `gh run list -L 3` + esito run sul commit di sessione.
Se gh assente o non autenticato: "CI NON VERIFICATA (gh assente)".
VIETATO scrivere "prevista verde" senza output reale.>

## §7 RISERVE APERTE

<Riserve estratte dai verdetti revisore di questa sessione + finding nuovi emersi.
"Nessuna." se vuoto.>
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

**INVARIANTE GIT OUTPUT**: mai sostituire l'output di `git log` o `git diff --stat` con prosa o riassunti. "Ultimi 10 commit, tutti docs" NON è accettabile — vanno le righe vere con hash e messaggi. Se l'output è lungo, incollalo comunque intero.
