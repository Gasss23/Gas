# REPORT — docs/sanitize-post-pr21
**Data:** 2026-07-17
**Branch:** docs/sanitize-post-pr21
**Obiettivo:** Sanitizzazione stato post-merge PR #21 e PR #19 su main.

---

## §F0 — Verifica merge (hash confermati dall'operatore)

Output verbatim di `git log origin/main --merges --oneline -5`:

```
8f9cf7b Merge pull request #21 from Gasss23/fix/hook-push-ref
fbf8246 Merge pull request #20 from Gasss23/docs/hook-guard-session-end
9a9278e Merge pull request #19 from Gasss23/feature/f6-history-atomica
fe0e476 Merge pull request #18 from Gasss23/fix/diario-recursive-triggers
e7b4486 Merge pull request #17 from Gasss23/chore/fondamenta-registro-pulizia
```

Hash confermati dall'operatore:
- PR #21 (fix/hook-push-ref) → merge `8f9cf7b` ✅
- PR #19 (feature/f6-history-atomica) → merge `9a9278e` ✅

---

## §F1 — Ispezione ci.yml (SOLA LETTURA)

File: `.github/workflows/ci.yml` — letto integralmente, nessuna modifica.

**Stato:** nessun problema rilevato. Il file è coerente con la documentazione interna (commenti inline) e con le run CI recenti (tutte SUCCESS). Struttura:
- Job `unit-suite` su `ubuntu-latest` Python 3.11
- Step: checkout → setup-python → install deps → enable bwrap → run suite → job summary → gate sandbox
- Il gate finale (`Gate — sandbox OS attivo`) esegue `if: always()` e distingue "rosso da sandbox" da "rosso da test"
- Nessun `paths-ignore` (coerente con lucchetto main CLAUDE.md §10: il check required deve riportare su ogni PR incluse le doc-only)

**Nessuna azione richiesta su F1.**

---

## §F2 — Aggiornamento reports/stato_progetto.md

Modifiche applicate (tutte in `reports/stato_progetto.md`, nessun altro file):

| Campo aggiornato | Prima | Dopo |
|---|---|---|
| Header `Ultimo aggiornamento` | 2026-07-16, fix/hook-push-ref | 2026-07-17, sanitize-post-pr21; PR #21 + PR #19 mergeate |
| Riga CI state | "Ultimo run su main: 29031945029 su 87ad26f (2026-07-09)" | Lista run PR #18–#21 tutte SUCCESS |
| F6-history-atomica (finding ✅) | "Merge PR #19 pendente (umano)" | "Mergeata → 9a9278e su main ✅ (2026-07-16, CI run 29484338680)" |
| Hook push (nota di processo) | "merge PENDENTE" | "merge 8f9cf7b su main ✅ (2026-07-16, CI run 29505642515)" |
| git add fragile (nota di processo) | "merge PENDENTE" | idem sopra |

**Run CI su main (da `gh run list --branch main --limit 5`) — tutte ✅ SUCCESS:**
```
29505642515  Merge PR #21  8f9cf7b  2026-07-16
29487631549  Merge PR #20  fbf8246  2026-07-16
29484338680  Merge PR #19  9a9278e  2026-07-16
29481225884  Merge PR #18  fe0e476  2026-07-16
```

---

## §STOP GATE — Nulla da proporre

Nessuna modifica oltre il perimetro F1 (sola lettura) + F2 (solo `stato_progetto.md`).
Nessun finding in ci.yml che richieda azione.
Riserve aperte da review #52–#54 (backfill memoria_revisore.md #48–#50, pattern `_cur_branch` fragile,
test mancante su `scrivi_rep.sh`) rimangono in stato_progetto.md come già registrate — non toccate qui.

---

## §ESITO

- F0: ✅ hash confermati dall'operatore
- F1: ✅ ci.yml ispezionato, nessuna azione
- F2: ✅ stato_progetto.md aggiornato (5 edit)
- Commit di report: questo file — nessun altro file in staging
