# Report — 2026-07-15 — fix §0 fine-task: git fetch + guard errore merge-base

**Branch:** fix/fine-task-base-mergebase
**Scope:** fetta unica, doc-only — modifica SOLO .claude/commands/fine-task.md

---

## DECISIONI UMANE RICHIESTE

Nessuna.

---

## Esito fette

- **Fetta unica — aggiorna §0 di fine-task.md**: `FATTA`
  - Aggiunto `git fetch origin` prima di `git merge-base origin/main HEAD`, con motivazione esplicita nel file: "senza fetch, origin/main locale può essere stale e il merge-base risale a un fork point vecchio → ${BASE}..HEAD include commit di sessioni precedenti".
  - Aggiunto guard di errore: se `git merge-base` restituisce vuoto, `/fine-task` si FERMA con messaggio esplicito, nessun fallback silenzioso.
  - Rimosso residuo vecchio approccio: commento `(a differenza di git log -- reports/handoff.md)`.
  - §2, §3, §5 NON toccati: continuano a usare `${BASE}`, semantica invariata.

---

## diff --stat reale (§0, raccolto live)

```
 .claude/commands/fine-task.md | 13 +++++++--
 reports/ultimo_report.md      | 66 +++++++++++++++++++++++++++++--------------
 2 files changed, 56 insertions(+), 23 deletions(-)
```

---

## Grep di verifica

### `grep -n 'handoff commit' .claude/commands/fine-task.md` → vuoto (OK)

```
(nessun output)
```

### `grep -n 'merge-base' .claude/commands/fine-task.md`

```
12:# 1. Aggiorna origin/main locale prima di calcolare il merge-base.
13:#    Senza fetch, origin/main locale può essere stale e il merge-base risale
19:BASE=$(git merge-base origin/main HEAD)
21:  echo "ERRORE: git merge-base origin/main HEAD fallito o ha restituito vuoto — /fine-task si FERMA."
```

---

## Anomalie

Nessuna.

---

## Stop gate

Nessun file fuori scope toccato. reports/stato_progetto.md, CLAUDE.md e qualsiasi altro file non menzionato nel task NON sono stati modificati.
