# REPORT — Design FEATURE 1 e FEATURE 2 (hook/fine-task)
**Data:** 2026-09-12
**Branch:** recon/hook-audit-2026-09-12
**Task:** Ricognizione FETTA A + proposta design FETTA B. Nessuna modifica a file di codice, hook, settings o test.

---

## DECISIONI UMANE RICHIESTE

1. **FEATURE 1 — dove vive il check**: proposta sotto è `scripts/check_landing.sh` (testabile, riusabile). Alternativa: bash block inline in fine-task.md (meno indirezione, non testabile con T-hook). Decidere.
2. **FEATURE 1 — comportamento se gh assente**: proposta = skip PR check + warning, gli altri due check (file + HEAD pushed) restano bloccanti. Accettabile o tutti e tre devono essere bloccanti?
3. **FEATURE 2 — trigger handoff**: la proposta controlla che `reports/handoff.md` sia nel diff `BASE..HEAD`. Se il supervisore vuole qualcosa di più forte (es. timestamp di modifica del file vs ultimo commit di sessione), va specificato.
4. **FEATURE 2 — agganciare come secondo Stop hook o come step in SessionEnd?**: Stop hook è più visibile (avviso appare prima della chiusura del turno). SessionEnd è meno rumoroso. La proposta usa Stop. Confermare.

---

## Fetta unica — Ricognizione + design: FATTA

---

# FETTA A — Lettura integrale file

## 1. settings.json

```json
{
  "model": "claude-sonnet-4-6",
  "env": {
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1"
  },
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo '=== REGOLE CRITICHE GAS (post-compact) === (1) REVISORE OBBLIGATORIO: prima di ogni commit che tocca gas.py/brains/modules/tests/, invocare il subagent revisore e attendere il verdetto APPROVATO. (2) SCOPE: fare SOLO lo scope dato — se serve altro, fermati e scrivilo in DECISIONI UMANE RICHIESTE nel report. (3) REPORTING CANONICO: a fine task scrivere reports/ultimo_report.md, committare+pushare, poi stampare: path report + hash commit + cat integrale + git diff --stat. (4) NO OPERAZIONI IRREVERSIBILI nel loop (niente merge/gc/restore/delete non autorizzati).'"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/session_end.sh",
            "timeout": 60,
            "statusMessage": "Auto-commit selettivo (reports/doc/history, motore MAI)..."
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/review_gate.sh",
            "timeout": 15,
            "statusMessage": "Gate review: il commit del motore richiede il revisore..."
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/scrivi_rep.sh",
            "timeout": 30,
            "statusMessage": "scrivi rep: controllo trigger e salvataggio risposta..."
          }
        ]
      }
    ]
  }
}
```

## settings.local.json

```json
{
  "permissions": {
    "allow": [
      "Bash(bwrap --version)",
      "Bash(claude --version)",
      "Bash(git fetch *)",
      "Bash(git checkout *)",
      "Bash(git reset *)",
      "Bash(git grep *)"
    ]
  }
}
```

## 2. ls -la .claude/hooks/

```
total 24
drwxr-xr-x  5 gas  staff   160 10 set 00:20 .
drwxr-xr-x  7 gas  staff   224 10 set 00:34 ..
-rwxr-xr-x  1 gas  staff  3235 10 set 00:20 review_gate.sh
-rwxr-xr-x  1 gas  staff  3093 10 set 00:20 scrivi_rep.sh
-rwxr-xr-x  1 gas  staff  1993 10 set 00:20 session_end.sh
```

**Nota:** non esiste uno script separato per SessionStart — il SessionStart è un `echo` inline in settings.json.

## 2a. scrivi_rep.sh (integrale)

```bash
#!/usr/bin/env bash
# Stop hook ON-DEMAND — zero token LLM. Autorizzato esplicitamente dall'utente
# (pusha sul branch corrente) il 2026-06-13.
# Salva in reports/ultima_risposta.md l'ultima risposta SOSTANZIALE di Claude,
# ma SOLO quando l'utente l'ha chiesto con il trigger "scrivi rep" nel suo ultimo
# messaggio. Senza trigger non scrive nulla (non gira "ogni volta").
# Salva la risposta che PRECEDE il messaggio "scrivi rep", non la replica al trigger.

: "${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}"
INPUT=$(cat)

# Estrai transcript_path senza dipendere da jq (hook payload è JSON a riga singola)
TP=$(printf '%s' "$INPUT" | sed -n 's/.*"transcript_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -n "$TP" ] && [ -f "$TP" ] || exit 0

# Pre-filtro trigger senza jq: esce silenzioso se "scrivi rep" non è nel transcript
grep -qi "scrivi rep" "$TP" 2>/dev/null || exit 0

# Trigger rilevato: jq è necessario per l'estrazione — fail-loud se assente o non funzionante
if ! jq --version >/dev/null 2>&1; then
    echo "scrivi_rep: jq non trovato — dipendenza mancante, feature scrivi rep inerte." >&2
    exit 0
fi

# 1) indice dell'ultimo messaggio UTENTE (stringa) col trigger "scrivi rep"
# 2) testo dell'ultimo messaggio ASSISTANT con blocco "text" PRIMA di quell'indice
OUT=$(jq -rs '
  to_entries as $e
  | ([ $e[]
        | select(.value.type=="user"
            and (.value.message.content | type == "string")
            and (.value.message.content | ascii_downcase | test("scrivi rep")))
        | .key ] | last) as $idx
  | if $idx == null then empty
    else ([ $e[]
            | select(.key < $idx
                and .value.type=="assistant"
                and (any(.value.message.content[]?; .type=="text"))) ] | last
          | .value.message.content[] | select(.type=="text") | .text)
    end
' "$TP" 2>/dev/null)

# Niente trigger o nessun testo trovato -> non toccare il file (fail-safe)
[ -n "$OUT" ] || exit 0

# Root del repo: GAS_REPO_DIR (override per test) oppure parent dello script
REPO_DIR="${GAS_REPO_DIR:-$CLAUDE_PROJECT_DIR}"
DEST="$REPO_DIR/reports/ultima_risposta.md"
printf '%s\n' "$OUT" > "$DEST"

# Auto-push: rende il file visibile su Claude Web senza copia-incolla.
# Tutto fail-safe: qualunque errore git NON deve mai bloccare la chiusura del turno.
(
  cd "$REPO_DIR" 2>/dev/null || exit 0
  if ! _cur_branch="$(git symbolic-ref --short HEAD 2>/dev/null)" || [ "$_cur_branch" = "main" ]; then
    echo "scrivi_rep: HEAD su main o detached, push saltato — main-lock." >&2
    exit 0
  fi
  git add reports/ultima_risposta.md
  if ! git diff --cached --quiet reports/ultima_risposta.md 2>/dev/null; then
    if ! git commit -q -m "chore(scrivi-rep): ultima risposta salvata"; then
      echo "scrivi_rep: git commit fallito su branch '$_cur_branch'." >&2
      exit 0
    fi
    git push -q origin HEAD:"refs/heads/$_cur_branch"
    _push_rc=$?
    if [ "$_push_rc" -ne 0 ]; then
      echo "scrivi_rep: git push fallito su branch '$_cur_branch' (exit code $_push_rc)." >&2
    fi
  fi
) || true

exit 0
```

## 2b. session_end.sh (integrale)

```bash
#!/usr/bin/env bash
# SessionEnd hook — RETE DI SICUREZZA SOLO PER IL PUSH (dal 2026-08-19).
#
# Contratto:
#  - NON committa mai. Il commit di fine sessione è responsabilità ESCLUSIVA
#    del flusso esplicito di fine-task (CLAUDE.md sez.3 + /fine-task).
#    /fine-task include nel suo git add: reports/ + .claude/agents/memoria_revisore.md
#    + .gas_history.json (set completo — nessun residuo per l'hook).
#  - Copre il solo caso edge: agente ha committato (via /fine-task) ma la
#    sessione è terminata prima del push. In quel caso pusha il branch corrente.
#  - Se HEAD == origin/<branch> (già sincronizzato), non fa nulla.
#  - Se il branch non esiste ancora su origin (ramo nuovo), pusha comunque.
#
# GAS_REPO_DIR sovrascrivibile SOLO per i test usa-e-getta; default = prod.

set -uo pipefail

REPO="${GAS_REPO_DIR:-${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}}"
cd "$REPO" 2>/dev/null || exit 0

# 0) GUARD MAIN-LOCK / DETACHED HEAD — BLOCCANTE.
# Su main o HEAD detached non pushare mai.
if ! _cur_branch="$(git symbolic-ref --short HEAD 2>/dev/null)"; then
  echo "session_end: HEAD detached, push skip — main-lock. Committare a mano su un branch." >&2
  exit 0
fi
if [ "$_cur_branch" = "main" ]; then
  echo "session_end: HEAD su main, push skip — main-lock. Committare a mano su un branch." >&2
  exit 0
fi

# 1) Push fail-safe: esegui solo se HEAD è avanti di origin (o branch non ancora su origin).
#    NON committa — il commit è responsabilità esclusiva del flusso /fine-task.
_remote_sha=$(git rev-parse "refs/remotes/origin/$_cur_branch" 2>/dev/null || true)
_local_sha=$(git rev-parse HEAD 2>/dev/null || true)
if [ -n "$_local_sha" ] && { [ -z "$_remote_sha" ] || [ "$_local_sha" != "$_remote_sha" ]; }; then
  git push -q origin HEAD:"refs/heads/$_cur_branch"
  _push_rc=$?
  if [ "$_push_rc" -ne 0 ]; then
    echo "session_end: push fail-safe fallito su branch '$_cur_branch' (exit code $_push_rc)." >&2
  fi
fi
exit 0
```

## 2c. review_gate.sh (integrale)

```bash
#!/usr/bin/env bash
# PreToolUse hook (Bash) — gate di review DETERMINISTICO.
# Blocca (exit 2) un `git commit` il cui diff STAGED tocca il motore
# (gas.py, brains/, modules/, tests/) se manca il marcatore .claude/.review_ok.

: "${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}"
INPUT=$(cat)

_parse_cmd() {
  if command -v jq >/dev/null 2>&1; then
    jq -r '(.[0] // .) | .tool_input.command // empty'
  elif python3 -c "import sys" >/dev/null 2>&1; then
    python3 -c "import json,sys; d=json.load(sys.stdin); o=d[0] if isinstance(d,list) else d; print(o.get('tool_input',{}).get('command',''))"
  elif python -c "import sys" >/dev/null 2>&1; then
    python -c "import json,sys; d=json.load(sys.stdin); o=d[0] if isinstance(d,list) else d; print(o.get('tool_input',{}).get('command',''))"
  else
    perl -MJSON::PP -e 'my $d=JSON::PP->new->decode(do{local$/;<STDIN>}); my $o=ref($d)eq"ARRAY"?$d->[0]:$d; print $o->{tool_input}{command}//"" if $o->{tool_input}'
  fi
}

CMD=$(printf '%s' "$INPUT" | _parse_cmd 2>/dev/null)
[ -n "$CMD" ] || exit 0
printf '%s' "$CMD" | grep -Eq 'git[[:space:]].*commit' || exit 0

cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || {
  echo "BLOCCATO (gate review): cd in CLAUDE_PROJECT_DIR ('$CLAUDE_PROJECT_DIR') fallito — fail-closed." >&2
  exit 2
}

DIFF_OUT=$(git diff --cached --name-only 2>/dev/null)
GIT_RC=$?
if [ "$GIT_RC" -ne 0 ]; then
  echo "BLOCCATO (gate review): 'git diff --cached' fallito (exit $GIT_RC) — impossibile verificare il diff motore, fail-closed." >&2
  exit 2
fi
if ! printf '%s\n' "$DIFF_OUT" | grep -qE '^(gas\.py|brains/|modules/|tests/)'; then
  exit 0
fi

[ -f .claude/.review_ok ] && exit 0

echo "BLOCCATO (gate review): il diff staged tocca il motore (gas.py/brains/modules/tests) ma manca .claude/.review_ok. Fai revisionare il diff dal subagent 'revisore'; se APPROVATO crea il marcatore (touch .claude/.review_ok) e ricommitta, poi rimuovilo." >&2
exit 2
```

## 3. .claude/commands/fine-task.md

(Contenuto integrale — vedere il file reale a commit `3919090`; riporto solo la struttura dei passi per evitare duplicazione nel report.)

**Passi del rito (da fine-task.md):**
- §0: `git fetch origin` + `BASE=$(git merge-base origin/main HEAD)` — guard bloccante se BASE vuoto
- §1: scrive `reports/ultimo_report.md`
- §2: scrive `reports/handoff.md` (template con §0–§7)
- §3: scrive `reports/diff_sessione.md`
- §4: `git add reports/ultimo_report.md reports/handoff.md reports/diff_sessione.md .claude/agents/memoria_revisore.md .gas_history.json`
- §4bis: rigenera blocchi git (`git diff --cached --stat ${BASE}`, `git log --oneline ${BASE}..HEAD`, `gh run list -L 3`) → riscrivi §2+§3+§6 in handoff.md → `git add reports/handoff.md` → `git commit` → `git push`
- §0 (completamento post-push): `gh pr list --head "$BRANCH"` → crea PR se assente
- §5: stampa path + hash + cat integrale + controllo handoff.md

## 4. check_handoff.py e check_verdetto.py

**check_handoff.py** — verifica che §2 GIT DIFF --STAT di handoff.md dichiari esattamente i file del diff `BASE..HEAD`. Exit 0 se coerente o non-applicabile; exit 1 se set incoerente. Usato da CI. Allowlist: `reports/ultima_risposta.md` esclusa dal confronto.

**check_verdetto.py** — verifica che i riferimenti `path:riga` in §4 VERDETTO DEL REVISORE di handoff.md siano verificabili (path nel diff, riga ≤ lunghezza file). Exit 0 se tutto verificabile o non-applicabile; exit 1 altrimenti. Usato da CI.

**Valutazione per FEATURE 1**: NESSUNA ESTENSIONE di questi script è appropriata. Entrambi sono check di CONTENUTO del handoff scritto (CI post-commit). FEATURE 1 è un check di STATO LANDING (pre/post-commit, lato agente). Scope diverso, risposta diversa. Dettaglio nella FETTA B.

## 5. test_unit_hooks.py — T-hook esistenti

**Pattern di costruzione repo git temporanei**: ogni test usa `tmp_path` (pytest fixture) come directory base. La funzione `_init_repo(path)` crea un repo git reale con `git init`, branch `main`, `git config user.email/name`, commit iniziale su `README.md`. I test che richiedono un origin usano un secondo repo `bare/` nella stessa `tmp_path`.

**T-hook esistenti:**

| ID | Classe | Cosa testa |
|---|---|---|
| T-hook-a | TestSessionEndGuard | HEAD su main → 0 commit, warning su stderr |
| T-hook-b | TestSessionEndGuard | HEAD su branch normale → 0 commit (hook non committa) |
| T-hook-c | TestSessionEndGuard | HEAD detached → 0 commit, warning su stderr |
| T-hook-d | TestSessionEndPush | Push su feature branch, NON su main |
| T-hook-e | TestSessionEndPush | Origin inesistente → warning + exit 0 |
| T-hook-f | TestSessionEndPushFallback | HEAD già == origin → nessun push (noop) |
| T-hook-g | TestScriviRepPush | scrivi_rep.sh pusha su feature branch, non main |
| T-hook-h | TestScriviRepPush | scrivi_rep.sh su main → 0 commit, warning |
| T-hook-i | TestScriviRepJq | trigger presente + jq assente → warning + exit 0 |
| T-hook-j | TestScriviRepJq | trigger presente + jq OK + HEAD detached → 0 commit |
| T-gate-A | TestReviewGateFailClosed | diff motore staged + .review_ok assente → exit 2 |
| T-gate-B | TestReviewGateFailClosed | diff motore staged + .review_ok presente → exit 0 |
| T-gate-C | TestReviewGateFailClosed | solo file non-motore staged → exit 0 |
| T-gate-D | TestReviewGateFailClosed | dir non-git → git diff fallisce → exit 2 (fail-closed) |
| T-R2-a | TestCommitMemoriaRevisore | commit -o committa SOLO memoria_revisore.md |
| T-R2-b | TestCommitMemoriaRevisore | add && commit include file motore (dimostra il bug) |
| T-R2-c | TestCommitMemoriaRevisore | noop idempotente se file non cambiato |
| T-R2-d | TestCommitMemoriaRevisore | dir non-git → WARN in log + exit 0 |
| T-R2-e | TestCommitMemoriaRevisore | mem presente + dir non-git → WARN + exit 0 |

## 6. gh CLI disponibile

```
gh version 2.100.0 (2026-09-03)
github.com — Logged in: Gasss23 (keyring) — Active: true
Token scopes: gist, read:org, repo, workflow
```

`gh pr list` è disponibile e autenticato su questo Mac.

---

# FETTA B — Proposta design

## FEATURE 1 — Verifica landing in /fine-task

### Dove vive lo step

**Proposta: nuovo file `scripts/check_landing.sh` + nuovo "passo 4ter" in `fine-task.md`.**

**Motivo per cui NON estendo check_handoff.py o check_verdetto.py:**
- `check_handoff.py` e `check_verdetto.py` sono check di CONTENUTO del handoff scritto, chiamati dalla CI post-commit. Scopo: coerenza del documento rispetto al diff git.
- FEATURE 1 è un check di STATO LANDING: "il branch è in uno stato corretto per considerare il task chiuso?". Non riguarda il contenuto del handoff, ma: PR aperta, file presenti, branch sincronizzato. Scope ortogonale.

**Motivo per `scripts/check_landing.sh` vs inline in fine-task.md:**
- Un file separato è testabile con il pattern T-hook esistente (repo git temporanei reali, `_run(repo)` → `subprocess.run(["bash", str(SCRIPT)])`).
- Il template fine-task.md non è testato unitariamente — è prosa con blocchi bash.
- Coerente con `scripts/commit_memoria_revisore.sh` (stessa famiglia: script bash in scripts/, test in test_unit_hooks.py).

### Cosa controlla e come FERMA

Il check avviene in un nuovo **"passo 4ter"** in fine-task.md, DOPO `git push` (fine di 4bis) e PRIMA di §5 (stampa finale).

```
## 4ter. VERIFICA LANDING (eseguire DOPO git push, PRIMA di §5)

```bash
python3 -m scripts.check_landing 2>&1
# oppure: bash "$CLAUDE_PROJECT_DIR/scripts/check_landing.sh"
# Exit 0 = tutto OK. Exit 1 = STOP — task incompleto.
```
```

**Logica di `scripts/check_landing.sh` (bash):**

```
Pseudocodice:

1. Guard main/detached:
   BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null)
   Se vuoto o "main" → echo "check_landing: non applicabile (main o HEAD detached)." + exit 0

2. Check A — File del set presenti:
   Per ciascuno di: reports/ultimo_report.md, reports/handoff.md, reports/diff_sessione.md
     Se il file NON esiste → accumula in MISSING
   Se MISSING non vuoto:
     echo "STOP (check_landing): file mancanti nel set di fine-task: $MISSING" >&2
     exit 1

3. Check B — HEAD pushato su origin:
   LOCAL_SHA = git rev-parse HEAD
   REMOTE_SHA = git rev-parse "refs/remotes/origin/$BRANCH" (fallisce se branch non esiste)
   Se REMOTE_SHA vuoto OR LOCAL_SHA != REMOTE_SHA:
     echo "STOP (check_landing): HEAD non sincronizzato con origin/$BRANCH. Eseguire git push." >&2
     exit 1

4. Check C — PR aperta (fail-safe se gh assente):
   Se !(command -v gh && gh auth status --hostname github.com 2>/dev/null):
     echo "check_landing: gh non disponibile — verifica PR manuale richiesta." >&2
     # NON exit 1: gli altri check sono passati, avviso non bloccante
   Altrimenti:
     PR_JSON=$(gh pr list --head "$BRANCH" --base main --json number,url 2>/dev/null)
     GH_EXIT=$?
     Se GH_EXIT != 0:
       echo "check_landing: gh pr list fallito (exit $GH_EXIT) — verifica PR manuale." >&2
       # NON exit 1: fail-safe
     Altrimenti se PR_JSON == "[]" o vuoto:
       echo "STOP (check_landing): nessuna PR aperta per branch '$BRANCH'. Creare la PR prima di chiudere." >&2
       exit 1
     Altrimenti:
       PR_NUM = estrai .number da PR_JSON
       PR_URL = estrai .url da PR_JSON
       echo "check_landing: OK — PR #$PR_NUM trovata ($PR_URL)."

5. Se tutti i check superati:
   echo "check_landing: OK — file presenti, HEAD pushato, PR presente."
   exit 0
```

**Come FERMA:** `exit 1` dal bash script si propaga come errore del comando Bash nel loop agente. Claude Code vede il fallimento del comando e si ferma (il task rimane nello stato "in progress" e l'agente deve diagnosticare e correggere).

**Comportamento se `gh` assente:** solo warning su stderr, `exit 0` dopo gli altri check. I check A (file) e B (HEAD pushed) restano SEMPRE bloccanti.

**Variante di robustezza per Check B:** usare `git fetch origin --quiet` prima del confronto per non basarsi su ref stale. Però un fetch in fine-task.md è già al §0 (passo -1). Se il push è appena avvenuto in 4bis, la ref locale è già aggiornata. NON serve un secondo fetch.

### Rischi e regressioni previsti

| Rischio | Valutazione |
|---|---|
| Branch recon/audit/sonda non hanno PR → STOP spurio | Basso: questi branch hanno comunque un fine-task che dovrebbe aprire una PR. Se il supervisore non vuole PR su certi branch, aggiungere un opt-out (es. file `.no-pr` o guard sul prefisso branch). |
| `gh pr list` restituisce stderr misto (R-finegat-1) | Mitigato con `2>/dev/null`; rimanente: non bloccante (warning). |
| Check B blocca se il push in 4bis è fallito ma l'agente non se n'è accorto | Desiderato: è esattamente il caso che vogliamo intercettare. |
| Test su CI: gh non autenticato → Check C skip, T-land-5 deve verificare proprio questo | Copertura già prevista (vedi test sotto). |

### Test proposti (T-land-*)

Tutti usano repo git temporanei reali con bare origin; lo stesso pattern di `_init_repo` + `_run(repo)`.

| Nome | Precondizione | Esito atteso |
|---|---|---|
| T-land-1 | branch feature/x, tutti i file presenti, HEAD pushato, PR non richiesta (gh mock restituisce PR) | exit 0 |
| T-land-2 | branch feature/x, tutti i file presenti, HEAD pushato, `gh pr list` restituisce `[]` | exit 1, "nessuna PR" in stderr |
| T-land-3a | reports/ultimo_report.md mancante | exit 1, "file mancanti" in stderr |
| T-land-3b | reports/handoff.md mancante | exit 1, "file mancanti" in stderr |
| T-land-4 | HEAD NON pushato su origin (local ahead) | exit 1, "non sincronizzato" in stderr |
| T-land-5 | gh assente (fake_bin stub che fallisce) | exit 0, warning "gh non disponibile" su stderr |
| T-land-6 | HEAD su main | exit 0, "non applicabile" su stdout |

---

## FEATURE 2 — Stop hook "promemoria soft"

### File hook proposto

**Nuovo file: `.claude/hooks/promemoria_end.sh`**

```
Pseudocodice:

0. Guard main/detached:
   BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null) || exit 0
   [ "$BRANCH" = "main" ] && exit 0

1. Calcola BASE (fail-safe: qualsiasi errore git → WARN in gas_debug.log + exit 0):
   BASE=$(git merge-base origin/main HEAD 2>/dev/null) || {
     printf '%s\n' "$(date -Iseconds) WARN promemoria_end: git merge-base fallito" \
       >> "${CLAUDE_PROJECT_DIR}/gas_debug.log" 2>/dev/null || true
     exit 0
   }
   [ -n "$BASE" ] || exit 0

2. Conta commit di sessione:
   SESSION_COMMITS=$(git log --oneline "${BASE}..HEAD" 2>/dev/null | wc -l | tr -d ' ')
   Se SESSION_COMMITS == 0 → exit 0 silenzioso

3. Controlla handoff aggiornato:
   HANDOFF_IN_DIFF=$(git diff --name-only "${BASE}..HEAD" 2>/dev/null | grep -c '^reports/handoff\.md$' || true)
   Se HANDOFF_IN_DIFF >= 1 → exit 0 silenzioso (handoff aggiornato)

4. Stampa avviso informativo:
   echo "PROMEMORIA SOFT: $SESSION_COMMITS commit di sessione su '$BRANCH', reports/handoff.md non aggiornato." >&2
   echo "Eseguire /fine-task prima di chiudere la sessione. (avviso informativo — sessione chiusa normalmente)" >&2

5. exit 0 SEMPRE (anche nel blocco fail-safe §1)
```

**Contratto assoluto:** `exit 0` in TUTTI i rami (inclusi errori interni). Il blocco fail-safe al passo 1 usa `|| { ... ; exit 0; }` su ogni operazione git potenzialmente bloccante. Nessun `exit 2` è ammesso.

### Come si aggancia in settings.json senza interferire con scrivi_rep.sh

Il blocco `Stop` accetta un **array** di entries, ognuna con il proprio `hooks`. Claude Code le esegue **in ordine**. La proposta aggiunge una seconda entry:

```json
"Stop": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/scrivi_rep.sh",
        "timeout": 30,
        "statusMessage": "scrivi rep: controllo trigger e salvataggio risposta..."
      }
    ]
  },
  {
    "hooks": [
      {
        "type": "command",
        "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/promemoria_end.sh",
        "timeout": 15,
        "statusMessage": "promemoria: check commit di sessione senza handoff..."
      }
    ]
  }
]
```

**Ordine di esecuzione:** scrivi_rep.sh PRIMA (il suo commit cambia HEAD, ma non aggiunge handoff.md). promemoria_end.sh DOPO: vede la situazione reale al momento della chiusura del turno.

**Interferenze:**
- `scrivi_rep.sh` committa `reports/ultima_risposta.md` (non tocca handoff.md) → promemoria_end.sh non viene influenzato dal commit di scrivi_rep.
- `scrivi_rep.sh` può push su origin → promemoria_end.sh legge origin/main solo per il merge-base e non pusha → nessun conflitto.
- `promemoria_end.sh` non scrive file, non committa, non pusha → zero side effects su scrivi_rep.sh.
- **Nessun doppio commit.** promemoria_end.sh non committa nulla.

**Exit code scrivi_rep.sh:** sempre 0 → promemoria_end.sh viene sempre eseguito indipendentemente dall'esito di scrivi_rep.

**Nota importante su `git merge-base origin/main HEAD`:** senza un `git fetch origin` preventivo, la ref `origin/main` usata è quella in cache locale. In uno Stop hook (che si attiva ad ogni chiusura turno) NON eseguire fetch per non rallentare la chiusura e non consumare rete. La ref stale è accettabile: l'avviso è soft e un false negative (nessun avviso quando ce ne sarebbe uno) è preferibile a rallentare ogni chiusura di turno.

### Fail-safe §9 completo

| Condizione | Comportamento |
|---|---|
| `git symbolic-ref` fallisce (HEAD detached) | exit 0 silenzioso |
| HEAD su main | exit 0 silenzioso |
| `git merge-base` fallisce | WARN in gas_debug.log + exit 0 |
| `git log` fallisce | exit 0 silenzioso (fail-open: meglio non avvisare che crashare) |
| `git diff --name-only` fallisce | exit 0 silenzioso |
| `gas_debug.log` non scrivibile | errore silenzioso (`|| true`), exit 0 comunque |
| Qualsiasi altra eccezione bash | `set +e` in cima (NON `set -e`); exit 0 finale garantito |

### Test proposti (T-prom-*)

Stesso pattern T-hook: repo temporanei reali, `_run_promemoria(repo)`.

| Nome | Precondizione | Esito atteso |
|---|---|---|
| T-prom-1 | branch feature/x, BASE..HEAD vuoto (nessun commit di sessione) | exit 0, stderr vuoto |
| T-prom-2 | branch feature/x, N commit di sessione, reports/handoff.md nel diff | exit 0, stderr vuoto |
| T-prom-3 | branch feature/x, N commit di sessione, reports/handoff.md NON nel diff | exit 0, avviso su stderr con N e nome branch |
| T-prom-4 | dir non-git (merge-base fallisce) | exit 0, WARN in gas_debug.log |
| T-prom-5 | HEAD su main | exit 0, stderr vuoto |

**Nota test T-prom-3/4**: il repo di test non ha un origin reale → `git merge-base origin/main HEAD` fallirà sempre se non c'è un bare repo collegato. Per T-prom-2/3 serve un bare repo con commit iniziale su origin/main. Progettare i test con la stessa infrastruttura di T-hook-d/e (bare + work).

---

## Riepilogo rischi/regressioni per entrambe le feature

| Area | Rischio | Mitigazione proposta |
|---|---|---|
| FEATURE 1 — exit 1 in fine-task.md | Se il check fallisce in modo spurio (es. gh bug), il task risulta bloccato | gh fail → warning non bloccante; Check A/B bloccanti solo per condizioni verificabili con git puro |
| FEATURE 1 — hook PreToolUse su `check_landing.sh` | `review_gate.sh` intercetta tutti i Bash. check_landing.sh non committa mai → review_gate esce a exit 0 (nessun diff motore) → nessun conflitto | Nessuna azione richiesta |
| FEATURE 2 — performance Stop | Aggiunge ~50-100ms per git log + git diff su ogni Stop. Accettabile | Timeout 15s in settings.json |
| FEATURE 2 — false negative su origin/main stale | Se origin/main locale è stale, BASE sbagliato → commit NON contati → nessun avviso | Accettabile (avviso soft) |
| FEATURE 2 — compatibilità con sessione cloud | In cloud origin/main può non essere raggiungibile → merge-base fallisce → WARN + exit 0 | Coperto da fail-safe |
| Coesistenza Stop hooks | Entrambi exit 0 sempre → nessun blocco reciproco | Verificato (vedi analisi sopra) |

---

## Conferma esplicita scope

- Zero auto-commit in questa sessione su codice, hook, settings, script o test.
- Zero push di codice (l'unico push è il commit di questo report su `recon/hook-audit-2026-09-12`).
- Coesistenza con gli hook esistenti verificata analiticamente (vedere sezione "Come si aggancia").
- **STOP: implementazione in attesa di approvazione scope dal supervisore.**
