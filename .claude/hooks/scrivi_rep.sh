#!/usr/bin/env bash
# Stop hook ON-DEMAND — zero token LLM. Autorizzato esplicitamente dall'utente
# (incl. auto-push su main) il 2026-06-13.
# Salva in reports/ultima_risposta.md l'ultima risposta SOSTANZIALE di Claude,
# ma SOLO quando l'utente l'ha chiesto con il trigger "scrivi rep" nel suo ultimo
# messaggio. Senza trigger non scrive nulla (non gira "ogni volta").
# Salva la risposta che PRECEDE il messaggio "scrivi rep", non la replica al trigger.

: "${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR non settata, hook interrotto}"
INPUT=$(cat)
TP=$(printf '%s' "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null)
[ -n "$TP" ] && [ -f "$TP" ] || exit 0

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
  git add reports/ultima_risposta.md 2>/dev/null
  if ! git diff --cached --quiet reports/ultima_risposta.md 2>/dev/null; then
    git commit -q -m "chore(scrivi-rep): ultima risposta salvata" 2>/dev/null
    git push -q origin main 2>/dev/null
  fi
) || true

exit 0
