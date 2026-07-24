# /fine-task — Reporting canonico di fine task

Esegui queste operazioni NELL'ORDINE, senza saltare passi.

---

## 0. Raccogli i dati grezzi (PRIMA di scrivere qualsiasi file)

Esegui questi comandi e tieni l'output — lo incolli verbatim nei file sotto:

```bash
# 1. Aggiorna origin/main locale prima di calcolare il merge-base.
#    Senza fetch, origin/main locale può essere stale e il merge-base risale
#    a un fork point vecchio → ${BASE}..HEAD include commit di sessioni precedenti.
git fetch origin

# 2. Calcola la base della sessione = punto di fork del branch corrente da origin/main.
#    Stabile: non si sposta dopo i commit della sessione.
BASE=$(git merge-base origin/main HEAD)
if [ -z "${BASE}" ]; then
  echo "ERRORE: git merge-base origin/main HEAD fallito o ha restituito vuoto — /fine-task si FERMA."
  exit 1
fi
echo "BASE=$BASE"

git diff --stat ${BASE}..HEAD
git log --oneline ${BASE}..HEAD
gh run list -L 3              # se gh disponibile e autenticato; altrimenti "CI NON VERIFICATA (gh assente)"
```

`${BASE}..HEAD` copre SOLO i commit di questa sessione (dal punto di fork da origin/main escluso).
Usa SEMPRE questo range per §2 e §3 — mai `HEAD~N` con N fisso, mai `git log -10`.

**REGOLA FERREA — output git verbatim**: incolla le righe grezze con hash e messaggi.
`"Ultimi 10 commit, tutti docs"` NON è accettabile — vanno le righe vere. Output grezzo o niente.

---

## 1. Scrivi reports/ultimo_report.md

Contenuto obbligatorio:
- Data e titolo del task
- DECISIONI UMANE RICHIESTE (se esistono, in cima al file)
- Esito per ogni fetta/step dello scope — **incluse quelle saltate o differite**:
  `FATTA` / `SALTATA — <motivo>` / `DEFERITA — <motivo>`
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

## §1 SCOPE & ESITO FETTE

Per ogni fetta/task dello scope:
- **Fetta N — <titolo>**: `FATTA` / `SALTATA — <motivo>` / `DEFERITA — <motivo>`
  <1-2 righe di dettaglio se utile>

Tutte le fette devono comparire qui — incluse quelle saltate.

---

## §2 GIT DIFF --STAT (sessione)

```
<output GREZZO di `git diff --stat ${BASE}..HEAD`>
```

## §3 GIT LOG --ONELINE (sessione)

```
<output GREZZO di `git log --oneline ${BASE}..HEAD` — righe con hash e messaggi, nessuna modifica>
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

**Mappatura commit→run OBBLIGATORIA**: per ogni commit di sessione indica la run CI
che lo ha testato, o dichiara esplicitamente "nessuna run su questo SHA". VIETATE le
formule collettive tipo "tutti i commit hanno CI verde": GitHub Actions crea una run
per *push*, non per commit — più commit pushati insieme condividono una sola run, che
testa SOLO l'albero del commit di testa. Un commit intermedio mai testato va dichiarato
tale, anche quando il suo contenuto è incluso nell'albero testato successivamente.

## §7 RISERVE APERTE

<Riserve estratte dai verdetti revisore di questa sessione + finding nuovi emersi.
"Nessuna." se vuoto.>
```

---

## 3. Scrivi reports/diff_sessione.md

Contenuto:
- File toccati in questa sessione (da `git diff --stat ${BASE}..HEAD`)
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

**Check comune (vale per i punti 4 e 5) — esegui UNA sola volta:**
```bash
git diff --stat ${BASE}..HEAD -- reports/handoff.md
```
- Output **vuoto** → `reports/handoff.md` NON è stato rigenerato in questa sessione.
- Output **non vuoto** → `reports/handoff.md` è stato rigenerato in questa sessione.

4. Contenuto integrale di `reports/handoff.md`:
   - Check **vuoto** → scrivi esattamente: `"handoff.md non rigenerato in questa sessione — nessun contenuto da stampare."`
   - Check **non vuoto** → catta il contenuto integrale del file.

   *Motivo: un handoff di sessione precedente stampato come output della sessione corrente è indistinguibile da uno fresco. Il file non mente, mente il contesto in cui viene presentato.*

5. URL dell'handoff — segui l'ordine, non invertibile:

   **Prerequisito**: commit e push del branch già completati (passi 1-2 sopra).

   Usa l'esito del check comune sopra (non rieseguirlo):
   - Check **vuoto** → scrivi esattamente: `"handoff.md non rigenerato in questa sessione"`. Non stampare alcun URL.
   - Check **non vuoto** → prosegui:

   ```bash
   git rev-parse HEAD
   ```
   URL da stampare: `https://raw.githubusercontent.com/Gasss23/Gas/<SHA>/reports/handoff.md`

   **Vincoli (motivo, non decorazione)**:
   - Usa SEMPRE `git rev-parse HEAD`. NON usare `git log -1 ... -- reports/handoff.md`: quel comando restituisce l'ultimo commit che ha toccato il file, che può essere di una sessione precedente. Non fallisce, non dà 404: serve in silenzio un handoff vecchio con URL apparentemente valido (failure mode osservato, micro-finding 2026-07-13).
   - L'URL deve essere pinnato allo SHA. Mai al branch (`/main/` o `/<branch>/`): raw.githubusercontent può servire contenuto stale su ref mobili.
   - Non inventare MAI un URL. Se il check diff --stat è vuoto, l'assenza dell'URL è l'informazione corretta.

---

## INVARIANTE

Non dare MAI a voce un riassunto diverso dal contenuto dei file. Ogni discrepanza tra ciò che dici e ciò che sta nei file è un errore da segnalare.

**INVARIANTE GIT OUTPUT**: mai sostituire l'output di `git log` o `git diff --stat` con prosa o riassunti. "Ultimi 10 commit, tutti docs" NON è accettabile — vanno le righe vere con hash e messaggi. Se l'output è lungo, incollalo comunque intero.
