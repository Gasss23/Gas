# REPORT — Ricognizione hook/sessione Claude Code
**Data:** 2026-09-12
**Task:** Sonda read-only del setup hook/sessione di Claude Code nel repo Gas. Nessuna modifica al codice, hook, settings o .claude/.

---

## DECISIONI UMANE RICHIESTE

1. **SessionStart matcher "compact" vs ogni sessione**: il SessionStart hook (regole critiche) si attiva SOLO sugli eventi `compact`, NON all'apertura di ogni sessione nuova. Se l'intenzione era ricordare le regole ad ogni sessione (non solo post-compressione), il matcher va rimosso o cambiato. Valutare.
2. **scrivi_rep.sh non ha `|| true` sull'exit del blocco jq** — se jq mancasse e il pre-filtro `grep` avesse già trovato "scrivi rep", lo script esce con errore silenzioso. Già documentato in CLAUDE.md ma nessuna action aperta formale. Valutare se aprire un finding.

---

## Fetta unica — Ricognizione read-only: FATTA

---

## 1. Versione Claude Code

```
2.1.269 (Claude Code)
```

(La migrazione Mac del 2026-09-09 registrava 2.1.267 — aggiornamento automatico avvenuto nel frattempo.)

**Hook events supportati in questa versione (confermati da settings.json attivo):**
- `SessionStart` — attivo (matcher: "compact")
- `SessionEnd` — attivo (no matcher)
- `PreToolUse` — attivo (matcher: "Bash")
- `Stop` — attivo (no matcher)

---

## 2. settings.json — contenuto integrale

File: `.claude/settings.json`

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
            "command": "echo '=== REGOLE CRITICHE GAS (post-compact) === ...'"
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

**Nota critica — SessionStart**: il matcher è `"compact"`, non vuoto. Questo significa che l'echo delle 4 regole critiche si attiva SOLO quando Claude Code esegue una compressione del contesto (compact), NON all'apertura normale di ogni sessione. La `statusMessage` del SessionEnd recita "Auto-commit selettivo" — statusMessage obsoleto (l'hook non committa più dal 2026-08-19). Non un bug funzionale, solo messaggio ingannevole.

### settings.local.json — contenuto integrale

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

---

## 3. .claude/commands/fine-task.md — file toccati

Il rito `/fine-task` tocca ESATTAMENTE questi file:

| File | Passo | Operazione |
|---|---|---|
| `reports/ultimo_report.md` | §1 + passo 4 git add | Scritto, poi staged |
| `reports/handoff.md` | §2 + passo 4bis re-add | Scritto due volte (draft + regen blocchi git), staged |
| `reports/diff_sessione.md` | §3 + passo 4 git add | Scritto, staged |
| `.claude/agents/memoria_revisore.md` | passo 4 git add | Staged (se presente) |
| `.gas_history.json` | passo 4 git add | Staged (se presente) |

**Pre-passi obbligatori:**
- `git fetch origin` — aggiorna origin/main locale
- `BASE=$(git merge-base origin/main HEAD)` — calcola il fork point della sessione

**Post-passi (passo 4bis):**
- `git diff --cached --stat ${BASE}` → va in §2 handoff.md
- `git log --oneline ${BASE}..HEAD` → va in §3 handoff.md
- `gh run list -L 3` → va in §6 handoff.md

**Gate §0 PR obbligatorio**: dopo il push, `gh pr list --head "$BRANCH"` verifica PR esistente o ne crea una nuova. Numero PR ESCLUSIVAMENTE da output JSON di `gh`.

---

## 4. session_end.sh — contenuto e comportamento attuale

**Agganciato a:** `SessionEnd` (no matcher — ogni SessionEnd)
**Timeout:** 60s

**Contratto dichiarato nel file (righe 1-14):**
- NON committa mai
- Push fail-safe SOLO se HEAD è avanti di `origin/<branch>`
- Guard main-lock: HEAD su `main` o detached → exit 0 silenzioso

**Logica (righe 22-43):**
1. Guard detached HEAD: `git symbolic-ref --short HEAD` fallisce → exit 0
2. Guard main branch: `$_cur_branch == "main"` → exit 0
3. Confronto SHA: local != remote (o remote assente) → `git push -q origin HEAD:"refs/heads/$_cur_branch"`
4. Push fallito → warning su stderr, exit 0 comunque

**Comportamento verificato:** non committa mai, push-only, fail-safe (exit 0 in tutti i casi di errore).

---

## 5. Hook Stop e SessionStart esistenti

### Stop hook — scrivi_rep.sh

**Agganciato a:** `Stop` (no matcher — ogni Stop)
**Timeout:** 30s

**Comportamento:**
- Estrae `transcript_path` dal JSON di input via `sed`
- Pre-filtro: `grep -qi "scrivi rep"` — se assente, exit 0 silenzioso (non scrive nulla)
- Se trigger trovato: usa `jq` (fail-loud se assente) per estrarre l'ultimo messaggio `assistant` con blocco `text` PRIMA dell'indice del messaggio utente con "scrivi rep"
- Scrive il testo estratto in `reports/ultima_risposta.md`
- Auto-commit su branch corrente con prefisso `chore(scrivi-rep):`
- Guard main-lock prima del commit: HEAD su main o detached → push saltato
- Push su `origin HEAD:"refs/heads/$_cur_branch"`

**Dipendenza critica:** `jq` obbligatorio per l'estrazione (fallback fail-loud solo se trigger rilevato).

### SessionStart hook (matcher: "compact")

**Agganciato a:** `SessionStart` con matcher `"compact"` (SOLO su eventi di compressione contesto)

**Comportamento:** esegue un `echo` con 4 regole critiche:
1. REVISORE OBBLIGATORIO prima di ogni commit motore
2. SCOPE: fare solo lo scope dato
3. REPORTING CANONICO: reports/ultimo_report.md + commit + push + cat integrale
4. NO OPERAZIONI IRREVERSIBILI nel loop

**NOTA**: il matcher `"compact"` limita il trigger SOLO agli eventi di compressione — NON ad ogni nuova sessione aperta normalmente. Questo è potenzialmente un gap: le regole non vengono ricordate in una sessione fresca che non subisce compressione.

---

## 6. Subagent revisore — .claude/agents/revisore.md

**Presente:** sì, in `.claude/agents/revisore.md`
**Anche presente:** `.claude/agents/memoria_revisore.md` (memoria persistente)

**Header revisore.md (prime 5 righe):**
```yaml
---
name: revisore
description: USA PROATTIVAMENTE E OBBLIGATORIAMENTE prima di QUALSIASI commit il cui diff tocca gas.py, brains/, modules/ o tests/. Non chiedere il permesso: appena il diff sul motore e' pronto e PRIMA di `git commit`, invoca SUBITO questo revisore sul diff staged. Revisiona correttezza tecnica E coerenza col progetto/roadmap. Ha una memoria persistente in .claude/agents/memoria_revisore.md che consulta e aggiorna a ogni review.
tools: Read, Grep, Glob, Bash, Edit, Write
---
```

**Letture obbligatorie prima di ogni review (in ordine):**
1. CLAUDE.md
2. reports/stato_progetto.md
3. .claude/agents/memoria_revisore.md

---

## Anomalie/finding rilevati

| # | Gravità | Finding | Impatto |
|---|---|---|---|
| A1 | 🟡 | SessionStart matcher `"compact"`: le regole critiche non vengono ricordate ad ogni nuova sessione aperta normalmente, solo dopo compressione contesto. | Se l'agente apre una sessione fresca senza compact, le 4 regole non vengono iniettate. |
| A2 | ℹ️ | `statusMessage` del SessionEnd recita "Auto-commit selettivo (reports/doc/history, motore MAI)..." ma l'hook non committa più dal 2026-08-19. | Solo messaggio ingannevole in UI, zero impatto funzionale. |
| A3 | ℹ️ | `review_gate.sh` ha parser JSON a cascata (jq → python3 → python → perl) — robusto ma ha 4 percorsi diversi di esecuzione. | Se jq manca, il fallback a python3 funziona ma non è testato esplicitamente dagli hook tests. |
| A4 | ℹ️ | `.review_ok` marcatore non viene ripulito automaticamente dopo il commit — l'hook non ha un passo di cleanup. | Rischio basso: il marcatore deve essere ricreato manualmente prima del prossimo commit motore; se rimane da una sessione precedente, il gate è aperto. |

---

## Riepilogo struttura hook attiva

```
SessionStart (compact only)
  └─ echo regole critiche (nessun file scritto)

SessionEnd (sempre)
  └─ session_end.sh: push fail-safe condizionale
      · NON committa mai
      · Guard: main/detached → skip
      · Push solo se HEAD > origin/<branch>

PreToolUse (matcher: Bash)
  └─ review_gate.sh: gate commit motore
      · Blocca (exit 2) git commit su engine files se manca .review_ok
      · Parser JSON cascata (jq→python3→python→perl)

Stop (sempre)
  └─ scrivi_rep.sh: salva ultima risposta
      · Trigger: "scrivi rep" nel transcript
      · Scrive reports/ultima_risposta.md
      · Auto-commit + push su branch corrente
      · Guard: main/detached → push skip
```
