# TASK: doc/hook — guard SessionEnd + obbligo riga revisore
**Data:** 2026-07-16
**Branch:** docs/hook-guard-session-end
**Sessione:** Codespace

---

## §1 SCOPE & ESITO FETTE

| Fetta | Descrizione | Esito |
|-------|-------------|-------|
| F1 | doc-only: revisore.md obbligo riga-per-review | FATTA |
| F2 | hook: guard main/detached in session_end.sh + test T-hook-a/b/c | FATTA |
| F3 | doc-only: stato_progetto.md aggiornato | FATTA |

**FUORI SCOPE (non toccato):** memoria_revisore.md backfill, cherry-pick 92a08ba, gas.py/brains/modules, CLAUDE.md, merge PR #19.

---

## §2 FETTA 1 — revisore.md: obbligo riga-per-review

**File modificato:** `.claude/agents/revisore.md`

Sezione "DOPO ogni review" riscritta. Prima diceva:
> Se la review non ha prodotto lezioni nuove, NON scrivere nulla.

Ora stabilisce un **obbligo assoluto**: dopo OGNI review, aggiungere UNA riga nel formato canonico:
```
#<numero> — <YYYY-MM-DD> — <verdetto> — <lezione o "nessuna lezione nuova">
```

Motivazione: il file è il contatore canonico di tutte le review. Un buco nel numeratore rende il file indifendibile — non si sa se la review è avvenuta, saltata, o il numero è errato. La riga va scritta SEMPRE.

Le lezioni opzionali si aggiungono come blocco separato dopo la riga contatore; il formato precedente (righe datate con `-`) rimane valido per le lezioni.

**Commit:** `ec4391b` — `docs(revisore): obbligo riga-per-review in memoria_revisore.md`

---

## §3 FETTA 2 — session_end.sh: guard main-lock / detached HEAD

**File modificati:** `.claude/hooks/session_end.sh`, `tests/test_unit_hooks.py`, `.claude/agents/memoria_revisore.md`

### Guard aggiunto

In cima a `session_end.sh`, PRIMA di qualsiasi `git add/commit`:

```bash
_cur_branch="$(git symbolic-ref --short HEAD 2>/dev/null)"
if [ $? -ne 0 ]; then
  echo "session_end: HEAD detached, commit saltato — main-lock. Committare a mano su un branch." >&2
  exit 0
fi
if [ "$_cur_branch" = "main" ]; then
  echo "session_end: HEAD su main, commit saltato — main-lock. Committare a mano su un branch." >&2
  exit 0
fi
```

- HEAD su `main` → warning su stderr, exit 0, zero commit
- HEAD detached → stesso trattamento (commit su HEAD detached è irraggiungibile)
- Il warning è su `stderr` in modo RUMOROSO: uno skip silenzioso è la memoria che mente per omissione
- Il resto dello script rimane **invariato** (allowlist, invariante motore, condizionale no-op, commit + push)

### Test reali

Creato `tests/test_unit_hooks.py` con tre test su repo git temporanei reali (no mock del guard):

| Test | Scenario | Atteso | Esito |
|------|----------|--------|-------|
| T-hook-a | HEAD su main + file allowlist modificato | 0 commit, exit 0, warning stderr | PASS |
| T-hook-b | HEAD su branch normale + file allowlist modificato | 1 commit creato | PASS |
| T-hook-c | HEAD detached + file allowlist modificato | 0 commit, exit 0, warning stderr | PASS |

**Esito suite:** `3 passed in 0.40s`

**Nota tecnica (scoperta durante il test):** `git add reports/ '*.md' .gas_history.json` — se `.gas_history.json` non esiste, git fallisce l'intera aggiunta (exit 128) senza staggiare nulla. In produzione il file esiste sempre; i test creano `.gas_history.json` nel repo temporaneo. Bug latente registrato ma fuori scope.

### Gate revisore

Revisore invocato sul diff staged. Verdetto: **APPROVATO (#51, 2026-07-16)**.

**Testo integrale del verdetto:**

> **Verdetto finale: APPROVATO**
>
> Il guard in `.claude/hooks/session_end.sh` e i tre test in `tests/test_unit_hooks.py` sono approvati per il commit senza modifiche obbligatorie.
>
> Cosa fa il diff: aggiunge un blocco di 15 righe all'inizio di `session_end.sh` (prima di qualsiasi `git add`) che blocca l'hook — con warning su stderr e exit 0 — se HEAD è su `main` o è in modalità detached. I test creano repo git reali ed eseguono l'hook vero, senza mock. Tutti e tre i casi (main / branch normale / detached) passano.
>
> Note non bloccanti da tenere a mente per il futuro:
> 1. In nuovi guard bash analoghi, preferire `if ! var="$(cmd)"; then` al posto del pattern `var="$(cmd)" ; if [ $? -ne 0 ]` per evitare fragilità alla manutenzione.
> 2. La riga pre-esistente `git push -q origin main` (riga 60 dello script, fuori scope) contraddice CLAUDE.md §10: andrebbe corretta in `git push -q origin HEAD` in un ticket separato.

Riga #51 aggiunta a `memoria_revisore.md` dal revisore stesso durante la review.

**Commit:** `11b96ce` — `feat(hook): guard main-lock/detached HEAD in session_end.sh + test T-hook-a/b/c`

---

## §4 FETTA 3 — stato_progetto.md

Aggiornato `reports/stato_progetto.md`:
- Header data aggiornato
- Sezione Istituzioni: contatore review aggiornato a **51**, nota backfill #48-#50 PENDENTE
- Sezione micro-finding/note: 3 nuove note (guard SessionEnd, obbligo riga revisore, backfill pendente)

---

## §5 STATO BACKFILL memoria_revisore.md

PENDENTE — richiede WSL locale.

- Commit `92a08ba` (lezioni review #48-#49) è su `local/main` (WSL), non pushato, non raggiungibile da Codespace
- Ricostruzione a memoria: VIETATA (per decisione esplicita dell'operatore)
- Conseguenza: `memoria_revisore.md` su origin/main ha un buco #48-#50 dopo l'ultima riga pushata (#47)
- Da questa sessione in poi: il file cresce correttamente da #51 con il nuovo formato canonico
- Azione: eseguire cherry-pick o re-aggiunta riga dalla postazione WSL locale in sessione separata

---

## §6 NOTA — git push origin main nell'hook (finding aperto)

Il revisore ha segnalato (nota non bloccante #2) che la riga `git push -q origin main` nella coda di `session_end.sh` contraddice CLAUDE.md §10 ("gli hook non devono MAI tentare push su main"). Fuori scope di questa sessione; da correggere in `git push -q origin HEAD` in un ticket separato.

---

## §7 CI

PR aperta verso main: pendente al momento della scrittura di questo report.
Hash commit Fetta 2: `11b96ce`.
