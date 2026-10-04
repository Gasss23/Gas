# /fine-task — Reporting canonico di fine task

Esegui queste operazioni NELL'ORDINE, senza saltare passi.

---

## 0. Calcola BASE (PRIMA di scrivere qualsiasi file — i blocchi git si raccolgono in 4bis)

Esegui questi comandi. BASE è stabile e si calcola ora; i blocchi git di §2/§3/§6 si generano nel passo 4bis, dopo lo stage dei report.

```bash
# 1. Aggiorna origin/main locale prima di calcolare il merge-base.
#    Senza fetch, origin/main locale può essere stale e il merge-base risale
#    a un fork point vecchio → ${BASE}..HEAD include commit di sessioni precedenti.
git fetch origin

# 2. Calcola la base della sessione = punto di fork del branch corrente da origin/main.
#    Stabile: non si sposta dopo i commit della sessione.
BASE=$(git merge-base refs/remotes/origin/main HEAD)
if [ -z "${BASE}" ]; then
  echo "ERRORE: git merge-base refs/remotes/origin/main HEAD fallito o ha restituito vuoto — /fine-task si FERMA."
  exit 1
fi
echo "BASE=$BASE"
```

`${BASE}..HEAD` copre SOLO i commit di questa sessione (dal punto di fork da origin/main escluso). Usa SEMPRE questo range in 4bis per §2, §3 e §6 — mai `HEAD~N` con N fisso, mai `git log -10`.

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

**REGOLA §0 — GATE PR OBBLIGATORIO (numero e URL sempre da `gh`, mai inventati)**:

`§0` va completata DOPO il `git push` del branch (al passo 4bis, dopo push e prima del
`git add reports/handoff.md` finale). Esegui questa procedura e usa SOLO l'output reale:

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
# Guardia: BRANCH vuoto o "main" → gate bloccante
if [ -z "$BRANCH" ] || [ "$BRANCH" = "main" ]; then
  echo "GATE §0 BLOCCATO: BRANCH='$BRANCH' non valido."
  # → scrivi in §0: "PR NON verificata/creata: BRANCH non valido ($BRANCH)."
  # → il task è INCOMPLETO (gate bloccante, non silenzioso)
  exit 1
fi

PR_JSON=$(gh pr list --head "$BRANCH" --base main --json number,url 2>&1)
GH_EXIT=$?
if [ $GH_EXIT -ne 0 ]; then
  # → scrivi in §0: "PR NON verificata/creata: gh pr list exit $GH_EXIT — $PR_JSON"
  # → il task è INCOMPLETO
elif [ "$PR_JSON" = "[]" ] || [ -z "$PR_JSON" ]; then
  # Nessuna PR esistente: crea non-interattiva (no editor, no merge)
  CREATE_OUT=$(gh pr create --base main --head "$BRANCH" --fill 2>&1)
  CREATE_EXIT=$?
  if [ $CREATE_EXIT -ne 0 ]; then
    # → scrivi in §0: "PR NON verificata/creata: gh pr create exit $CREATE_EXIT — $CREATE_OUT"
    # → il task è INCOMPLETO
  else
    VIEW_JSON=$(gh pr view "$BRANCH" --json number,url 2>&1)
    VIEW_EXIT=$?
    if [ $VIEW_EXIT -ne 0 ]; then
      # → scrivi in §0: "PR NON verificata/creata: gh pr view exit $VIEW_EXIT — $VIEW_JSON"
      # → il task è INCOMPLETO
    else
      PR_NUMBER=$(echo "$VIEW_JSON" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['number'])")
      PR_URL=$(echo "$VIEW_JSON" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['url'])")
      # → scrivi in §0: "1. Merge della PR #$PR_NUMBER ($PR_URL)."
    fi
  fi
else
  # PR già esistente: leggi numero e URL dal JSON
  PR_NUMBER=$(echo "$PR_JSON" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[0]['number'])")
  PR_URL=$(echo "$PR_JSON" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[0]['url'])")
  # → scrivi in §0: "1. Merge della PR #$PR_NUMBER ($PR_URL)."
fi
```

VINCOLO FERREO: il numero PR scritto in §0 proviene ESCLUSIVAMENTE dall'output JSON di `gh`.
Nessun numero hardcoded, nessun placeholder, mai "Merge PR #NN" scritto a prescindere.
Se gh fallisce (exit non-zero) o $BRANCH è vuoto/main: §0 = `"PR NON verificata/creata: <errore reale>"` e il task è INCOMPLETO (gate bloccante).
`"Nessuna."` in §0 è ammesso SOLO se la sessione non ha PR da mergiare.
Usa `--fill` per `gh pr create`, mai aprire editor. NON mergiare (il merge è azione umana da WSL).

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

**VINCOLI VERIFICATI DA CI (job handoff-check):**
- Il **SET di file** dichiarato in questo blocco deve essere esatto e uguale al diff reale.
  La CI confronta i path a sinistra del '|' con `git diff --name-only BASE..HEAD`.
  Un file omesso o fantasma fa fallire il job.
- I **conteggi di righe** (colonna a destra del '|') sono approssimati per costruzione:
  `reports/handoff.md` conta se stesso tra le righe modificate, ma il suo conteggio finale
  è ignoto al momento della scrittura. La CI NON confronta mai i conteggi, solo i path.
- **Allowlist CI**: `reports/ultima_risposta.md` è escluso dal confronto.
  Motivo: quel file viene committato dall'hook `scrivi_rep` DOPO il fine-task, quindi
  la sua assenza dal §2 è strutturale e attesa — non un errore.

## §3 GIT LOG --ONELINE (sessione)

```
<output GREZZO di `git log --oneline ${BASE}..HEAD` — righe con hash e messaggi, nessuna modifica>
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

<Per OGNI commit che tocca gas.py/brains/modules/tests/: verdetto INTEGRALE del revisore,
incollato. Se nessun commit motore: "nessun diff motore, revisore non richiesto.">

## §5 DELTA TEST DEL MOTORE

<"Nessuna modifica a gas.py/tests/" OPPURE: numeri prima→dopo + blocco RIEPILOGO reale
incollato + quali FAIL sono fuori scope e perché>

## §6 STATO CI

<output REALE di `gh run list -L 3` + esito run sul commit di sessione.
Se gh assente o non autenticato: "CI NON VERIFICATA (gh assente)".
VIETATO scrivere "prevista verde" senza output reale.
Se gli ultimi commit non hanno ancora una run CI al momento della scrittura, scrivere esattamente "run non ancora disponibile alla scrittura dell'handoff" per quei SHA. Vietato ometterli in silenzio e vietato attribuirgli la run di un commit precedente. Nota che la copertura pre-merge è garantita altrove da `gasmerge` (gh pr checks --watch), non da questo campo.>

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

## 4. Stage dei file di report (set completo)

```bash
# File di report obbligatori
git add reports/ultimo_report.md reports/handoff.md reports/diff_sessione.md
# Memoria revisore e history — inclusi qui per evitare che l'hook SessionEnd
# li raccolga in un secondo commit separato (design fix 2026-08-19).
git add .claude/agents/memoria_revisore.md 2>/dev/null || true
git add .gas_history.json 2>/dev/null || true
```

NON includere nel commit file del motore (gas.py, brains/, modules/, tests/) — quelli richiedono il revisore.

---

## 4bis. RIGENERA I BLOCCHI GIT (ultimo passo prima del commit)

Esegui ora, con i file di report già in stage:

```bash
git -c core.quotePath=false diff --cached --stat=400 ${BASE}     # ← va in §2 di handoff.md (nomi grezzi, mai troncati: nota b review #143)
git log --oneline ${BASE}..HEAD      # ← va in §3 di handoff.md
gh run list -L 3                     # ← va in §6 di handoff.md (se gh disponibile; altrimenti "CI NON VERIFICATA (gh assente)")
```

**Perché `--cached` contro `${BASE}`**: `git diff --cached --stat ${BASE}` mostra tutto ciò che è in stage rispetto a BASE, inclusi i file di report appena aggiunti (ultimo_report.md, handoff.md, diff_sessione.md). `git diff --stat ${BASE}..HEAD` non li vedrebbe: quei file non esistono ancora in nessun commit HEAD.

Riscrivi §2 e §3 (e §6) nel file `reports/handoff.md` con questi output. Poi re-aggiungi in stage l'handoff aggiornato:

```bash
git add reports/handoff.md
```

**Titoli delle sezioni**: leggi i titoli attesi direttamente dalle regex `re.search(r"##\s*§...` in `scripts/check_handoff.py` e `scripts/check_verdetto.py`. Vietato inventare varianti.

SOLO ORA committa:

```bash
git commit -m "docs(<descrizione-breve>): <cosa hai fatto>"
```

### Gate + push + URL (script deterministico)

```bash
bash scripts/fine_task_finale.sh
```

Lo script esegue nell'ordine: gate A (check_handoff), gate B (check_verdetto), gate IP (nessun IP in reports/), push del branch (MAI main), guardia HEAD==@{u}, stampa `URL_HANDOFF`. Se qualsiasi gate è rosso → exit 1 + messaggio chiaro, nessun push.

### CI post-push (step manuale)

```bash
# Ottieni il run ID del push appena fatto
gh run list --branch $(git rev-parse --abbrev-ref HEAD) -L 1

# Attendi la run (l'esito REALE va in §6 di handoff.md — mai "prevista verde")
gh run watch <run-id>
```

Aggiorna §6 di handoff.md con l'esito reale, poi ri-stage + ri-committa + ri-esegui `bash scripts/fine_task_finale.sh` **solo se §6 era errato**.

---

## 4ter. Verifica check_landing

Dopo il push di §4bis, esegui:

```bash
CLAUDE_PROJECT_DIR=$(git rev-parse --show-toplevel) bash scripts/check_landing.sh
```

Esiti:
- **Exit 0**: tutti i check superati (o gh assente/non autenticato → Check C skippato)
- **Exit 1**: Check A (file mancante/vuoto), Check B (HEAD non pushato) o Check C (nessuna PR) — **STOP**: correggi il problema prima di andare al §5

---

## 4quater. Verifica esterna (fette che toccano il perimetro di review o la sicurezza)

Lancia un agente NUOVO (contesto vergine a ogni verifica, mai riprendere uno precedente)
con il tool Agent: `subagent_type: general-purpose`, `model: sonnet` (modello diverso
dall'agente principale), in background, con ESATTAMENTE questo prompt, senza aggiunte né
contesto:

```
Applica .claude/verifica_esterna.md a: <URL_HANDOFF> <URL_PR>
```

Il protocollo vive in `.claude/verifica_esterna.md` (lo cambia solo l'operatore). Quando arriva
il verdetto, riportalo all'operatore così com'è (integrale nel prossimo handoff), con i finding
in sintesi in chat. Per le fette di sicurezza (cancello, firma, sandbox, gate) dire anche
all'operatore di fare il secondo passaggio nella chat claude.ai con lo stesso URL.

---

## 5. Stampa a terminale ESATTAMENTE (senza riassumere):

1. Path del report: `reports/ultimo_report.md`
2. Hash del commit (output di `git rev-parse HEAD`)
3. Contenuto integrale di `reports/ultimo_report.md`

4. URL dell'handoff — lo script `fine_task_finale.sh` lo stampa già come `URL_HANDOFF: ...`.
   Riportalo qui (output verbatim dello script).

   **Motivo**: l'URL pinnato allo SHA è il file — il cat integrale è ridondante e introduce
   rischio di discrepanza tra ciò che si incolla e ciò che è committato.
   Se `fine_task_finale.sh` non è stato eseguito (sessione senza handoff rigenerato),
   scrivi esattamente: `"handoff.md non rigenerato in questa sessione — URL non disponibile."`

   **Vincoli (invarianti)**:
   - L'URL deve essere quello stampato da `fine_task_finale.sh` (SHA lungo di HEAD al momento del push).
   - Non inventare MAI un URL.

---

## INVARIANTE

Non dare MAI a voce un riassunto diverso dal contenuto dei file. Ogni discrepanza tra ciò che dici e ciò che sta nei file è un errore da segnalare.

**INVARIANTE GIT OUTPUT**: mai sostituire l'output di `git log` o `git diff --stat` con prosa o riassunti. "Ultimi 10 commit, tutti docs" NON è accettabile — vanno le righe vere con hash e messaggi. Se l'output è lungo, incollalo comunque intero.

---

## GATE POST-FINE-TASK

SE COMMITTI QUALSIASI COSA DOPO /fine-task, DEVI RI-ESEGUIRE /fine-task PER INTERO. Un handoff che non copre l'ultimo commit del branch è un handoff che mente. Nessuna eccezione per "era solo un doc".
