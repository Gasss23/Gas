# Report — 2026-07-15 — fix §0 fine-task: git fetch + guard errore merge-base

**Branch:** fix/fine-task-base-mergebase
**Scope:** fetta unica, doc-only — modifica SOLO .claude/commands/fine-task.md

---

## DECISIONI UMANE RICHIESTE

Nessuna.

---

## Esito fette

- **Fetta unica — aggiorna §0 di fine-task.md**: `FATTA`
  - Aggiunto `git fetch origin` prima di `git merge-base`, con motivazione esplicita nel file.
  - Rimosso residuo vecchio approccio: commento `(a differenza di git log -- reports/handoff.md)`.
  - Aggiunto guard di errore: se `git merge-base` restituisce vuoto, `/fine-task` si FERMA con messaggio esplicito.

---

## diff --stat reale (file modificato in questa fetta)

```
 .claude/commands/fine-task.md | 12 +++++++++---
 1 file changed, 9 insertions(+), 3 deletions(-)
```

---

## Hash merge-base live (`git fetch origin && git merge-base origin/main HEAD`)

```
ce9ae5e39f0932b74f3d70d3c7235931b470079e
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

## Stop gate

Nessun altro file toccato. reports/stato_progetto.md, CLAUDE.md e qualsiasi altro file fuori scope NON sono stati modificati.
