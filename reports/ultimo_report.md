# Report — Sonda bug "phantom PR" in /fine-task

**Data:** 2026-08-22  
**Task:** SONDA ZERO-MODIFICA — individuazione della logica che produce "Merge PR #NN" fantomatica  
**Branch:** `sonda/phantom-pr-bug`

---

## DECISIONI UMANE RICHIESTE

1. **Approvare il fix proposto** e autorizzare l'implementazione in una fetta successiva (snippet completo in §4 di questo report).

---

## Fette / punti scope

### Punto 1 — Dove è definito /fine-task

**FATTO.**

File: `/home/gqual/Gas/.claude/commands/fine-task.md` (238 righe)  
È l'unica definizione: sia il custom slash command del progetto sia il skill `fine-task` puntano a questo file.

---

### Punto 2 — Logica esatta che produce "Merge PR #NN"

**FATTO.** Stringa trovata verbatim:

**File:** `.claude/commands/fine-task.md`  
**Riga 65:**
```
"1. Merge della PR #<numero> (<titolo-breve>)."
```

**Contesto (righe 62-66):**
```
**REGOLA §0**: "Nessuna." è ammesso SOLO se la sessione non lascia nulla in mano
all'operatore. Se la PR di sessione non è ancora mergiata, §0 deve contenere almeno:
"1. Merge della PR #<numero> (<titolo-breve>)."
Scrivere "Nessuna." con una PR aperta è un errore — nasconde lavoro umano richiesto.
```

**Root cause:**  
Il template istruisce l'AI su *cosa scrivere* ("Merge della PR #<numero>") ma **non contiene nessuna istruzione** a eseguire `gh pr list --head <branch>` per verificare se una PR esiste davvero. Dopo aver pushato un branch, l'AI:

1. Legge REGOLA §0: `"Nessuna." è un errore se c'è una PR aperta`
2. Sa di aver appena pushato un branch
3. Inferisce (erroneamente) che "deve esserci una PR" e **allucinates un numero**
4. Nessun check meccanico la smentisce → phantom PR stampata nel report

La pressione è bidirezionale: la regola **punisce** `"Nessuna."` quando una PR esiste, ma **non richiede alcuna verifica** prima di scrivere un numero. Il risultato è che l'AI preferisce allucinare un numero piuttosto che rischiare di scrivere "Nessuna." sbagliato.

---

### Punto 3 — Sonda ambiente (output REALE)

**FATTO.**

**`gh --version`:**
```
gh version 2.96.0 (2026-07-02)
https://github.com/cli/cli/releases/tag/v2.96.0
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
(branch remoto esistente, nessuna PR aperta → output `[]` corretto)

**`gh pr list --json number,url,headRefName,state -L 5`:**
```
[]
```
(nessuna PR aperta in questo momento)

**Conclusione ambiente:** `gh` è disponibile, autenticato, e funziona correttamente. Il comando ritorna `[]` quando nessuna PR esiste. Il fix è fattibile senza dipendenze nuove.

---

### Punto 4 — Fix proposto (NON implementato)

**FATTO — proposta solo testuale.**

**Dove inserire il fix:** nel passo 0 di `/fine-task.md`, dopo il calcolo di `BASE` e prima di scrivere qualsiasi file.

**Snippet bash da aggiungere:**

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

**Riscrittura REGOLA §0** (da sostituire alle righe 62-66):

```
**REGOLA §0**: Prima di scrivere questa sezione, esegui il blocco bash di verifica PR
(passo 0 sotto). USA SOLO i valori restituiti da quel comando — mai un numero inventato.

- Se `$PR_NUMBER` è VUOTO → scrivi esattamente: "Nessuna."
- Se `$PR_NUMBER` è valorizzato → scrivi: "1. Merge della PR #${PR_NUMBER} — ${PR_URL}"

Scrivere "Nessuna." quando `$PR_NUMBER` è vuoto è CORRETTO (nessuna PR esiste).
Scrivere un numero non proveniente dall'output del comando è un errore critico (phantom PR).
```

**Perché funziona:** la regola attuale ha due difetti gemelli — punisce `"Nessuna."` senza dare un modo meccanico per sapere se è giustificata, e fornisce un placeholder `#<numero>` che invita all'allucinazione. Il fix elimina entrambi: la variabile `$PR_NUMBER` è la fonte di verità (vuota = nessuna PR, valorizzata = PR reale), e la regola riscritta rimuove la penalità su `"Nessuna."` quando è corretta.

---

## Anomalie

- Nessuna anomalia tecnica nell'ambiente.
- Confermato: il bug è **puramente nel template** (fine-task.md), non in gh né nel sistema git/GitHub.
- Nessuna modifica al codice in questa sessione.
