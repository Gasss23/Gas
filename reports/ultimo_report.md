# Report — Sonda bug "phantom PR" in /fine-task

**Data:** 2026-08-22  
**Task:** SONDA ZERO-MODIFICA — individuazione della logica che produce "Merge PR #NN" fantomatica  
**Branch:** `sonda/phantom-pr-bug`

---

## DECISIONI UMANE RICHIESTE

1. **Approvare il fix proposto** e autorizzare l'implementazione in una fetta successiva (snippet completo in §Punto 4 di questo report).
2. **Merge della PR** di questo branch (doc-only, nessun gate revisore richiesto).

---

## Esito fette/punti scope

- **Punto 1 — Dove è definito /fine-task**: `FATTA`  
  File: `.claude/commands/fine-task.md` (238 righe). Unica definizione: slash command e skill puntano allo stesso file.

- **Punto 2 — Logica esatta che produce "Merge PR #NN"**: `FATTA`  
  `.claude/commands/fine-task.md:65` — REGOLA §0 istruisce l'AI a scrivere il numero PR senza eseguire `gh pr list`. Root cause: pressione bidirezionale (punisce "Nessuna." ma non richiede verifica). Dettaglio in §Punto 2 sotto.

- **Punto 3 — Sonda ambiente**: `FATTA`  
  `gh` 2.96.0, autenticato Gasss23, `gh pr list` ritorna `[]` (corretto). Dettaglio in §Punto 3 sotto.

- **Punto 4 — Fix proposto**: `FATTA`  
  Snippet bash + riscrittura REGOLA §0 proposti. NON implementato per GATE DI STOP BLOCCANTE.

- **Modifiche al codice**: `SALTATA — GATE DI STOP BLOCCANTE` (scope = solo sonda)

---

## §Punto 2 — Logica esatta che produce "Merge PR #NN"

**File:** `.claude/commands/fine-task.md`  
**Riga 65** (verbatim):
```
"1. Merge della PR #<numero> (<titolo-breve>)."
```

**Contesto righe 62-66** (verbatim):
```
**REGOLA §0**: "Nessuna." è ammesso SOLO se la sessione non lascia nulla in mano
all'operatore. Se la PR di sessione non è ancora mergiata, §0 deve contenere almeno:
"1. Merge della PR #<numero> (<titolo-breve>)."
Scrivere "Nessuna." con una PR aperta è un errore — nasconde lavoro umano richiesto.
```

**Root cause:** Il template istruisce l'AI su *cosa scrivere* ma **non ordina `gh pr list`** per verificare se la PR esiste. Dopo un push, l'AI:
1. Legge REGOLA §0: `"Nessuna."` è punita se c'è PR aperta
2. Sa di aver pushato un branch
3. Inferisce (erroneamente) che esiste una PR → allucinates il numero
4. Nessun check meccanico la smentisce → phantom PR nel report

---

## §Punto 3 — Sonda ambiente (output REALE)

**`gh --version`:**
```
gh version 2.96.0 (2026-07-02)
```

**`gh auth status`** (token redatto):
```
github.com
  ✓ Logged in to github.com account Gasss23
  - Active account: true
  - Git operations protocol: https
  - Token: [REDACTED]
  - Token scopes: 'codespace', 'gist', 'read:org', 'repo', 'workflow'
```

**`gh pr list --head docs/scollega-gashistory-da-r2 --json number,url`:**
```
[]
```

**`gh pr list --json number,url,headRefName,state -L 5`:**
```
[]
```

Conclusione: `gh` disponibile, autenticato, funziona correttamente. Fix fattibile senza dipendenze nuove.

---

## §Punto 4 — Fix proposto (NON implementato)

**Dove inserire:** passo 0 di `fine-task.md`, dopo il calcolo di `BASE`, prima di scrivere qualsiasi file.

**Snippet bash:**
```bash
# Verifica PR reale — OBBLIGATORIO prima di scrivere §0
BRANCH=$(git branch --show-current)
PR_JSON=$(gh pr list --head "$BRANCH" --json number,url,state 2>/dev/null)
PR_NUMBER=$(echo "$PR_JSON" | python3 -c \
  "import sys,json; l=json.load(sys.stdin); print(l[0]['number'] if l else '')" \
  2>/dev/null)
PR_URL=$(echo "$PR_JSON" | python3 -c \
  "import sys,json; l=json.load(sys.stdin); print(l[0]['url'] if l else '')" \
  2>/dev/null)
echo "PR_NUMBER=${PR_NUMBER:-<nessuna PR aperta>}"
echo "PR_URL=${PR_URL:-<nessuna PR aperta>}"
```

**Riscrittura REGOLA §0** (sostituisce righe 62-66 di `fine-task.md`):
- Se `$PR_NUMBER` VUOTO → scrivere esattamente `"Nessuna."` (corretto, nessuna PR esiste)
- Se `$PR_NUMBER` valorizzato → `"1. Merge della PR #${PR_NUMBER} — ${PR_URL}"`
- Scrivere un numero non proveniente dall'output del comando è errore critico (phantom PR).

**Perché funziona:** elimina entrambi i difetti — la penalità su `"Nessuna."` quando è corretta, e il placeholder `#<numero>` che invita all'allucinazione. La variabile `$PR_NUMBER` diventa fonte di verità meccanica.

---

## Anomalie

- Nessuna anomalia tecnica nell'ambiente.
- Il bug è **puramente nel template** (`fine-task.md:65`), non in `gh` né in git/GitHub.
- Nessun codice modificato in questa sessione (GATE DI STOP rispettato).
