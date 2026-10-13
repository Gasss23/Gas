#!/usr/bin/env bash
# PreToolUse hook (Bash) — gate di review DETERMINISTICO.
# Blocca (exit 2) un `git commit` il cui diff STAGED tocca il PERIMETRO DI REVIEW
# (.claude/perimetro_review.txt: motore + macchina di controllo — hook, gate,
# revisore, CI; V-1 verifica esterna PR #118) se manca il marcatore .claude/.review_ok
# o se il marcatore non contiene l'hash del diff staged attuale; blocca anche
# se nel working tree ci sono modifiche al motore NON staged o non tracciate
# (R-136-1: `commit -a`, pathspec o `add && commit` le farebbero entrare dopo
# il controllo, che vede solo l'index del momento).
# Costringe a far passare il diff dal subagent `revisore` prima del commit.
#
# R-gate-worktree-1 (chiusa qui): PRIMA questo hook faceva `cd "$CLAUDE_PROJECT_DIR"`
# incondizionato e controllava SOLO quell'indice. La doc di Claude Code dice che
# CLAUDE_PROJECT_DIR "still points at the project root where the session started",
# mentre il campo `cwd` del JSON "follows Claude: ... is the worktree root after
# Claude enters a worktree". Conseguenza: in una sessione che lavora in un worktree
# l'hook ispezionava l'indice del checkout PRINCIPALE e, se quello era pulito,
# usciva 0 SENZA NEMMENO LEGGERE il marcatore → un diff del motore mai revisionato
# poteva entrare. E al contrario un diff staged nel principale bloccava i commit
# (anche di soli report) delle sessioni nei worktree.
# Ora il gate controlla ogni checkout CANDIDATO (non «ogni checkout»: vedi i limiti):
#   1. la radice git di `cwd` (il checkout dove la sessione sta davvero lavorando);
#   2. la radice git di CLAUDE_PROJECT_DIR;
#   3. TUTTI i worktree registrati, quando `cwd` manca o quando il comando contiene
#      costrutti che cambiano directory (`cd`, `pushd`, `git -C`, `--git-dir`,
#      `--work-tree`, `GIT_DIR=`, `GIT_WORK_TREE=`), perche' in quel caso la
#      directory reale del commit NON e' deducibile dal payload.
# Ogni checkout viene giudicato col PROPRIO marcatore e col PROPRIO indice.
#
# Limiti dichiarati (best-effort, per design). Sono di DUE specie e non vanno confuse:
#   (a) limite-COMPORTAMENTO: dice cosa fa il gate in un caso. E' testabile e DEVE avere
#       un test, altrimenti diventa una dichiarazione falsa (in questa fetta CINQUE lo
#       sono state, l'ultima proprio in queste righe). Oggi hanno tutti un lucchetto:
#       il falso positivo di `-C` e' pinnato da wt28/wt29, quello del matcher da wt30.
#   (b) limite-NON-PROMESSA: dice cosa il gate NON garantisce (alias, heredoc esotici,
#       GIT_INDEX_FILE, eval). Non e' un comportamento da pinnare e pretenderne un test
#       produrrebbe un'altra dichiarazione falsa (R-302-3).
#  - Il matcher sul testo del comando NON copre tutte le forme di `git commit`
#    (alias, heredoc esotici): e' una RETE sopra la regola di workflow di
#    CLAUDE.md sez.3, non un sostituto. La barriera primaria resta l'istruzione.
#    In piu' il matcher ha falsi POSITIVI (R-gate-matcher-1): un comando che non
#    committa ma la cui prosa contiene `git` e `commit` viene trattato come commit.
#    Conseguenza voluta: nel dubbio si controlla, mai si lascia passare.
#  - Legge comando e cwd da tool_input.command / .cwd (JSON su stdin).
#  - L'input hook puo' essere un array JSON [{...}] o un oggetto {}: gestito.
#  - `cwd` non e' documentato con una versione minima: se manca, il gate NON
#    si fida di CLAUDE_PROJECT_DIR da solo e spazza tutti i worktree.
#  - La directory del singolo comando Bash non e' nel payload e un `cd` dentro il
#    comando non e' tracciabile: da qui la spazzata di tutti i worktree.
#  - R-299-2: un `cd` dentro una stringa viene TROVATO (il prefisso ammette gli
#    apici) e un bersaglio quotato viene risolto (gli apici si togliono nello stadio
#    di risoluzione). Un bersaglio NON risolvibile — relativo, con variabile, glob,
#    con spazi, apice spaiato O INTERNO — fa scattare la spazzata. Forme piu' esotiche (eval,
#    percorso costruito a pezzi, NOME del comando costruito a pezzi — R-312-2:
#    `c''d`, `cd''`, `c""d`, `c\d`, `x=cd; $x` — o `extglob` attivo nella shell)
#    possono non essere viste affatto: il gate NON
#    promette di intercettare ogni scrittura in un altro checkout, promette di non
#    lasciar passare un checkout che ha ISPEZIONATO.
#  - R-300-1 (specie (b) nella parte che il gate non sa, specie (a) nella mitigazione,
#    che e' pinnata da wt8/wt22/wt27): tutto l'impianto si appoggia a `cwd`, ma `cwd`
#    NON segue il `cd` della
#    shell persistente del tool Bash: se un comando PRECEDENTE ha spostato la shell,
#    la scrittura puo' avvenire in un checkout diverso da `cwd` e il gate non lo sa.
#    Mitigazione per convenzione, non per speranza: ogni comando che scrive NOMINA la
#    propria radice (`cd <radice> && ...`), forma che il gate risolve e che rende
#    `cwd` irrilevante.
#  - Falsi positivi noti e ACCETTATI (direzione sicura): `-C` e' matchato a ogni
#    occorrenza senza verificare che appartenga a git, quindi `-C HEAD` (opzione vera
#    di git) o `grep -C 3` fanno scattare la spazzata. Si preferisce una spazzata di
#    troppo a un'euristica che riapre un buco.
#  - R-299-3: l'altra meta' del difetto NON e' chiusa del tutto. Con `cwd` noto il
#    principale non viene piu' ispezionato di default (quindi il suo lavoro in corso
#    non blocca piu' le sessioni nei worktree), ma ogni volta che si spazza l'insieme
#    torna a includere TUTTI i checkout: in quel caso il lavoro in corso di uno
#    blocca i commit degli altri. E' fail-closed e voluto, non un difetto nascosto.
#  - L'hook gira dal WORKING TREE: un hook modificato e non in stage esegue se
#    stesso. Il controllo del working tree blocca il COMMIT di qualunque file del
#    perimetro fuori stage, ma non può impedire che la versione manomessa giri.
#  - Il marcatore lega il DIFF, non il verdetto: scripts/segna_review_ok.sh si può
#    lanciare senza review (la barriera resta la regola di CLAUDE.md sez.3).
#  - Un indice alternativo (GIT_INDEX_FILE=...) è fuori controllo (R-137-3).

: "${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}"
INPUT=$(cat)

# Parser JSON a cascata: jq -> python3 (se funziona) -> python -> perl
# Usiamo test di esecuzione reale (non solo command -v) perche' su Windows
# python3 puo' essere uno stub Microsoft Store che esiste ma exit != 0.
# $1 = percorso del campo da estrarre: "command" (in tool_input) o "cwd" (radice).
_parse_campo() {
  local campo="$1"
  if command -v jq >/dev/null 2>&1; then
    # NB: NON usare `(.[0] // .)`: su un oggetto `.[0]` e' un ERRORE (non null) e
    # jq 1.7 non lo sopprime con `//` → parse fallito → gate inerte (fail-open,
    # misurato 2026-10-03 su jq-1.7.1-apple con l'input oggetto di Claude Code).
    if [ "$campo" = "cwd" ]; then
      jq -r 'if type == "array" then .[0] else . end | .cwd // empty'
    else
      jq -r 'if type == "array" then .[0] else . end | .tool_input.command // empty'
    fi
  elif python3 -c "import sys" >/dev/null 2>&1; then
    # Campo passato per ARGV, non interpolato nel sorgente (R-299-6): in una
    # macchina di sicurezza il codice non deve dipendere dal quoting di una variabile.
    python3 -c '
import json,sys
c=sys.argv[1]
d=json.load(sys.stdin); o=d[0] if isinstance(d,list) else d
print(o.get("cwd","") if c=="cwd" else o.get("tool_input",{}).get("command",""))' "$campo"
  elif python -c "import sys" >/dev/null 2>&1; then
    python -c '
import json,sys
c=sys.argv[1]
d=json.load(sys.stdin); o=d[0] if isinstance(d,list) else d
print(o.get("cwd","") if c=="cwd" else o.get("tool_input",{}).get("command",""))' "$campo"
  else
    perl -MJSON::PP -e 'my $c=shift; my $d=JSON::PP->new->decode(do{local$/;<STDIN>}); my $o=ref($d)eq"ARRAY"?$d->[0]:$d; print(($c eq "cwd") ? ($o->{cwd}//"") : ($o->{tool_input}{command}//""))' "$campo"
  fi
}

CMD=$(printf '%s' "$INPUT" | _parse_campo command 2>/dev/null)
PARSE_RC=$?
if [ "$PARSE_RC" -ne 0 ]; then
  # Parser fallito: non sappiamo se e' un commit. FAIL-CLOSED: il controllo
  # "e' un git commit?" si fa sul testo GREZZO dell'input, cosi' un commit non
  # sfugge al gate per un JSON inatteso (i comandi non-commit restano liberi).
  CMD="$INPUT"
fi
[ -n "$CMD" ] || exit 0

# Non e' un git commit -> non interferire
printf '%s' "$CMD" | grep -Eq 'git[[:space:]].*commit' || exit 0

# cwd: il checkout dove la sessione sta davvero lavorando (segue i worktree).
# Un parse fallito o un valore vuoto NON e' fatale: fa scattare la spazzata.
CWD=$(printf '%s' "$INPUT" | _parse_campo cwd 2>/dev/null) || CWD=""

# Radice git di una directory ("" se non e' un repo o la dir non esiste).
_radice() {
  [ -n "$1" ] && [ -d "$1" ] || return 1
  git -C "$1" rev-parse --show-toplevel 2>/dev/null
}

# --- Insieme dei checkout da controllare -------------------------------------
REPOS=()
_aggiungi_repo() {
  local r="$1" esistente
  [ -n "$r" ] || return 0
  for esistente in ${REPOS[@]+"${REPOS[@]}"}; do
    [ "$esistente" = "$r" ] && return 0
  done
  REPOS+=("$r")
}

RADICE_PROGETTO=$(_radice "$CLAUDE_PROJECT_DIR")
if [ -z "$RADICE_PROGETTO" ]; then
  echo "BLOCCATO (gate review): CLAUDE_PROJECT_DIR ('$CLAUDE_PROJECT_DIR') non e' un repo git — impossibile verificare il diff motore, fail-closed." >&2
  exit 2
fi
RADICE_CWD=""
if [ -n "$CWD" ]; then
  RADICE_CWD=$(_radice "$CWD")
  if [ -z "$RADICE_CWD" ]; then
    echo "BLOCCATO (gate review): cwd ('$CWD') non e' un repo git — impossibile sapere dove avviene il commit, fail-closed." >&2
    exit 2
  fi
  _aggiungi_repo "$RADICE_CWD"
fi

# R-299-3: il checkout di CLAUDE_PROJECT_DIR entra nell'insieme SOLO se non sappiamo
# dove la sessione sta lavorando. Con `cwd` noto, il commit avviene nel checkout di
# `cwd` (o in un bersaglio esplicito risolto sotto, o nella spazzata): aggiungere
# sempre il principale non aggiunge copertura e reintroduce l'altra metà del difetto
# — un diff staged nel principale che blocca i commit, anche di soli report, delle
# sessioni nei worktree. La radice del principale resta comunque calcolata sopra
# (serve per `git worktree list` e come controllo fail-closed) e rientra
# nell'insieme ogni volta che si spazza.
[ -n "$RADICE_CWD" ] || _aggiungi_repo "$RADICE_PROGETTO"

# La directory reale del commit NON e' nel payload e un `cd` dentro il comando non
# e' tracciabile. Strategia a due livelli, per non trasformare il gate in un freno:
#   - se il comando cambia directory verso un percorso ASSOLUTO e LETTERALE, quel
#     checkout si risolve e si aggiunge all'insieme (preciso, nessun falso positivo);
#   - se c'e' un costrutto che NON si puo' risolvere (percorso relativo, variabile,
#     glob, sostituzione, forme con spazio o via env) oppure `cwd` manca del tutto,
#     si spazzano TUTTI i worktree registrati: nel dubbio si controlla ogni
#     checkout, mai si lascia passare.
# Senza questo secondo livello il gate sarebbe inerte su `cd <altro-worktree> && commit`;
# senza il primo, ogni comando che inizia con `cd <radice>` (la forma piu' comune)
# accoppierebbe la sessione allo stato di lavoro in corso di TUTTE le altre.
SPAZZA=0
[ -n "$RADICE_CWD" ] || SPAZZA=1

# Forme che non si risolvono per costruzione → spazzata diretta.
printf '%s' "$CMD" | grep -Eq '(^|[;&|(){}[:space:]])popd([[:space:]]|$)|GIT_DIR=|GIT_WORK_TREE=|--work-tree[[:space:]]|--git-dir[[:space:]]' && SPAZZA=1
# V-1 bot #196: forme di cambio directory che il matcher dei bersagli non vede
# (`\cd`, `"cd"`/`'cd'`, `env --chdir=`/`--chdir `) → spazzata diretta.
printf '%s' "$CMD" | grep -Eq '\\(cd|pushd)([^[:alnum:]_]|$)|["'"'"'](cd|pushd)["'"'"']|--chdir' && SPAZZA=1
# R-312-1: forma corta attaccata di --chdir (`env -C<dir>`, `env -iC<dir>`): un -C
# seguito subito da altro testo non e' un bersaglio risolvibile → spazzata. I falsi
# positivi (opzioni di altri comandi) vanno nella direzione sicura.
printf '%s' "$CMD" | grep -Eq '(^|[[:space:]])-[[:alpha:]]*C[^[:space:]]' && SPAZZA=1

# Costrutti con un bersaglio esplicito: ne conto le occorrenze e ne risolvo i
# percorsi. Se anche uno solo non si risolve, spazzo (conteggi diversi = dubbio).
# R-299-1: `-C` si matcha a OGNI occorrenza, non solo quella attaccata a `git`.
# `git -C <pulito> -C <sporco>` applica l'ULTIMO -C: col match legato a `git` il
# secondo bersaglio non veniva nemmeno contato (1/1 → nessuna spazzata → fail-open
# misurato). R-299-2: il prefisso ammette anche gli APICI, cosi' un `cd` dentro una
# stringa (`bash -c "cd /altro && ..."`) viene trovato invece di essere invisibile.
# R-300-BOCCIATO: gli apici stanno nel PREFISSO (merito di R-299-2) ma NON vanno
# toccati nella classe del BERSAGLIO. Escludendoli da lì, un bersaglio che INIZIA con
# un apice non aveva piu' nessun carattere da consumare: il costrutto non veniva
# nemmeno TROVATO (N_TROVATI=0 → nessun dubbio → nessuna spazzata) e sei forme comuni
# passavano — `cd "<wt>"`, `cd '<wt>'`, `cd "../x"`, `-C "<wt>"`,
# `--work-tree="<wt>"`, `pushd "<wt>"` — tutte misurate a 0 dove il giro precedente
# dava 2. Classe LARGA qui, apici tolti nello stadio di risoluzione piu' sotto.
TROVATI=$(printf '%s' "$CMD" | grep -oE '(^|[;&|(){}"'"'"'[:space:]])(cd|pushd)[[:space:]]+[^[:space:];&|)]+|(^|[[:space:]])-C[[:space:]]+[^[:space:];&|)]+|--work-tree=[^[:space:];&|)]+|--git-dir=[^[:space:];&|)]+' 2>/dev/null)
N_TROVATI=0
N_RISOLTI=0
if [ -n "$TROVATI" ]; then
  while IFS= read -r costrutto; do
    [ -n "$costrutto" ] || continue
    N_TROVATI=$((N_TROVATI + 1))
    # Bersaglio = ultimo campo (per --work-tree=/--git-dir= la parte dopo '=').
    bersaglio=$(printf '%s' "$costrutto" | awk '{print $NF}')
    case "$bersaglio" in
      --work-tree=*) bersaglio="${bersaglio#--work-tree=}" ;;
      --git-dir=*)   bersaglio="${bersaglio#--git-dir=}" ;;
    esac
    # Apici tolti QUI, non esclusi dal match (vedi la nota sul bersaglio), ma SOLO
    # se formano una COPPIA ai bordi. Togliere ogni apice a prescindere era un
    # fail-open (3o giro, BOCCIATO): la classe del match si ferma sullo spazio,
    # quindi `cd "/path con spazi"` arriva TRONCATO a `"/path`, e una
    # normalizzazione cieca lo rendeva `/path` — assoluto e letterale — facendo
    # validare un percorso DIVERSO da quello vero e contare il costrutto come
    # risolto. Regola: si normalizza solo una forma COMPLETA e riconoscibile; ogni
    # residuo di apice e' un dubbio, quindi spazzata.
    case "$bersaglio" in
      \"*\") bersaglio=${bersaglio#\"}; bersaglio=${bersaglio%\"} ;;
      \'*\') bersaglio=${bersaglio#\'}; bersaglio=${bersaglio%\'} ;;
    esac
    case "$bersaglio" in
      *\"*|*\'*) continue ;;   # apice spaiato o interno: bersaglio troncato o ambiguo
    esac
    # Solo percorsi assoluti e letterali: tutto il resto e' dubbio.
    case "$bersaglio" in
      /*) : ;;
      *) continue ;;
    esac
    case "$bersaglio" in
      # V-2 bot #196: anche `\\`, `[`, `{` cambiano la parola per la shell (escape,
      # glob, brace): il letterale non e' il percorso vero, quindi e' un dubbio.
      *'$'*|*'`'*|*'*'*|*'?'*|*'~'*|*'\'*|*'['*|*'{'*) continue ;;
    esac
    radice_b=$(_radice "$bersaglio") || radice_b=""
    [ -n "$radice_b" ] || continue
    _aggiungi_repo "$radice_b"
    N_RISOLTI=$((N_RISOLTI + 1))
  done <<< "$TROVATI"
  [ "$N_RISOLTI" -eq "$N_TROVATI" ] || SPAZZA=1
fi
if [ "$SPAZZA" -eq 1 ]; then
  if ! WT_LIST=$(git -C "$RADICE_PROGETTO" worktree list --porcelain 2>/dev/null); then
    echo "BLOCCATO (gate review): 'git worktree list' fallito in '$RADICE_PROGETTO' — impossibile enumerare i checkout, fail-closed." >&2
    exit 2
  fi
  while IFS= read -r riga; do
    case "$riga" in
      worktree\ *)
        wt_dir="${riga#worktree }"
        # R-299-4: un worktree PRUNABLE (directory rimossa, non ancora prunata) non
        # puo' ospitare nessuna scrittura: nella spazzata si salta, altrimenti ogni
        # comando finirebbe in un vicolo cieco («cd fallito») che nessuna review puo'
        # sbloccare, solo `git worktree prune`. Il fail-closed resta pieno per i
        # bersagli NOMINATI (cwd, CLAUDE_PROJECT_DIR, bersaglio di un `cd`).
        [ -d "$wt_dir" ] || continue
        _aggiungi_repo "$wt_dir"
        ;;
    esac
  done <<< "$WT_LIST"
fi

# Script dell'hash: accanto al repo dell'HOOK (non del repo controllato), cosi'
# vale anche nei test su repo temporanei.
HASH_SH="$(dirname "$0")/../../scripts/hash_diff_staged.sh"
PERIM_FILE="$(dirname "$0")/../perimetro_review.txt"
if [ ! -r "$PERIM_FILE" ]; then
  echo "BLOCCATO (gate review): perimetro di review assente ($PERIM_FILE) — fail-closed." >&2
  exit 2
fi

# --- Controllo di UN checkout ------------------------------------------------
# Gira in subshell: il `cd` e gli array restano locali all'iterazione.
_controlla_repo() (
  REPO="$1"
  cd "$REPO" 2>/dev/null || {
    echo "BLOCCATO (gate review): cd in '$REPO' fallito — fail-closed." >&2
    exit 2
  }

  # Perimetro di review: fonte unica .claude/perimetro_review.txt. R-138-1: il
  # perimetro NON può togliersi da solo dalla lista. Le voci sono l'UNIONE di:
  #   (1) voci cablate qui sotto (il perimetro stesso e gli hook: non rimovibili);
  #   (2) il file accanto all'hook (vale anche nei test su repo temporanei);
  #   (3) la versione in stage (`git show :...`) e (4) quella di HEAD.
  # Restringere il perimetro richiede quindi un commit revisionato: finché la riga
  # è in HEAD o nell'index, conta. File dell'hook assente → fail-closed (sopra).
  PERIM_PATHS=()
  PERIM_RE_PARTS=()
  _aggiungi_voci() {
    local riga esc
    while IFS= LC_ALL=C read -r riga || [ -n "$riga" ]; do
      riga="${riga%%#*}"
      riga="$(printf '%s' "$riga" | tr -d '[:space:]')"
      [ -n "$riga" ] || continue
      PERIM_PATHS+=("${riga%/}")
      esc=$(printf '%s' "$riga" | sed 's/[][\.*^$()+?{}|]/\\&/g')
      case "$riga" in
        */) PERIM_RE_PARTS+=("$esc") ;;
        *)  PERIM_RE_PARTS+=("$esc\$") ;;
      esac
    done
  }
  _aggiungi_voci < "$PERIM_FILE"
  if [ "${#PERIM_PATHS[@]}" -eq 0 ]; then
    echo "BLOCCATO (gate review): perimetro di review vuoto ($PERIM_FILE) — fail-closed." >&2
    exit 2
  fi
  _aggiungi_voci <<'VOCI_CABLATE'
.claude/perimetro_review.txt
.claude/hooks/
VOCI_CABLATE
  _aggiungi_voci < <(git show :.claude/perimetro_review.txt 2>/dev/null)
  _aggiungi_voci < <(git show HEAD:.claude/perimetro_review.txt 2>/dev/null)
  PERIM_RE="^($(IFS='|'; printf '%s' "${PERIM_RE_PARTS[*]}"))"

  # Il diff staged tocca il perimetro? — verifica FAIL-CLOSED.
  # In una pipeline bash l'exit code finale e' quello dell'ultimo comando, non di
  # git: un git failure risulterebbe in exit 0 (fail-open, review #80). Il subshell
  # qui sotto esce ESPLICITAMENTE con l'exit code di git (PIPESTATUS[0]), non di `tr`.
  # R-138-2: --no-renames (un rename dal perimetro verso fuori mostra anche il path
  # di origine) e -z (nomi non-ASCII o con virgolette arrivano grezzi, non quotati).
  DIFF_OUT=$(git diff --cached --name-only --no-renames -z 2>/dev/null | tr '\0' '\n'; exit "${PIPESTATUS[0]}")
  GIT_RC=$?
  if [ "$GIT_RC" -ne 0 ]; then
    echo "BLOCCATO (gate review): 'git diff --cached' fallito in '$REPO' (exit $GIT_RC) — impossibile verificare il diff motore, fail-closed." >&2
    exit 2
  fi

  # R-136-1: modifiche al motore fuori dall'index (non staged o non tracciate)
  # possono entrare nel commit DOPO questo controllo (`commit -a`, pathspec,
  # `add && commit`). Fail-closed: il commit si fa solo con il motore tutto in
  # stage (e revisionato) oppure tutto pulito.
  WT_OUT=$(git status --porcelain --no-renames --untracked-files=all -- "${PERIM_PATHS[@]}" 2>/dev/null)
  WT_RC=$?
  if [ "$WT_RC" -ne 0 ]; then
    echo "BLOCCATO (gate review): 'git status' fallito in '$REPO' (exit $WT_RC) — fail-closed." >&2
    exit 2
  fi
  if printf '%s\n' "$WT_OUT" | grep -qE '^(.[^ ]|\?\?) '; then
    echo "BLOCCATO (gate review): in '$REPO' ci sono modifiche NON in stage (o file non tracciati) nel perimetro di review (.claude/perimetro_review.txt). Mettile in stage e falle revisionare, oppure mettile da parte (git stash), poi riprova." >&2
    exit 2
  fi
  if ! printf '%s\n' "$DIFF_OUT" | grep -qE "$PERIM_RE"; then
    exit 0   # nessun file del perimetro in stage in questo checkout
  fi

  # Marcatore di review: contiene lo SHA-256 del diff staged revisionato (scritto da
  # scripts/segna_review_ok.sh DOPO il verdetto), ed e' quello di QUESTO checkout —
  # ogni worktree ha il suo (R-gate-worktree-1). Consentito SOLO se combacia col
  # diff staged attuale: un marcatore residuo di una sessione precedente, vuoto
  # (vecchio `touch`) o di un diff cambiato dopo la review NON apre il gate.
  if [ -f .claude/.review_ok ]; then
    ATTESO=$(head -n 1 .claude/.review_ok | tr -d '[:space:]')
    ATTUALE=$(bash "$HASH_SH" 2>/dev/null)
    if [ -n "$ATTESO" ] && [ -n "$ATTUALE" ] && [ "$ATTESO" = "$ATTUALE" ]; then
      exit 0
    fi
    echo "BLOCCATO (gate review): in '$REPO' .claude/.review_ok non corrisponde al diff staged (marcatore residuo, vuoto o diff cambiato dopo la review). Fai revisionare il diff attuale e rigenera il marcatore con: bash scripts/segna_review_ok.sh" >&2
    exit 2
  fi

  echo "BLOCCATO (gate review): in '$REPO' il diff staged tocca il perimetro di review (.claude/perimetro_review.txt) ma manca .claude/.review_ok. Fai revisionare il diff dal subagent 'revisore'; se APPROVATO crea il marcatore con: bash scripts/segna_review_ok.sh — poi ricommitta." >&2
  exit 2
)

# PERIM_FILE e HASH_SH NON vanno esportate: _controlla_repo e' una subshell
# e eredita anche le variabili non esportate (R-299-6).
for repo in "${REPOS[@]}"; do
  _controlla_repo "$repo" || exit $?
done
exit 0
