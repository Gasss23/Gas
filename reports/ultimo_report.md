# Report — docs/fine-task-url-handoff

**Data:** 2026-07-15
**Branch:** docs/fine-task-url-handoff
**Scope:** DOC-ONLY — aggiunta regola URL handoff in .claude/commands/fine-task.md

---

## Esito fetta unica

| Fetta | Stato |
|-------|-------|
| Aggiunta regola URL handoff in fine-task.md | **FATTA** |

---

## Dettaglio modifica

Aggiunta nella sezione `## 5. Stampa a terminale ESATTAMENTE` come punto 5 della lista.

Sostanza invariata rispetto alle istruzioni ricevute:
- Ordine obbligatorio: commit → push → verifica diff stat → SHA → URL
- Check `git diff --stat ${BASE}..HEAD -- reports/handoff.md`: se vuoto → nessun URL, scrivi la frase esatta
- Comando corretto: `git rev-parse HEAD` (non `git log -1 -- reports/handoff.md`)
- Vincoli documentati con motivo: failure mode 2026-07-13, stale cache su ref mobili

Forma adattata allo stile del file: lista numerata con sotto-passi, code block bash, grassetto per i vincoli.

---

## git diff --stat REALE

```
.claude/commands/fine-task.md | 20 ++++++++++++++++++++
 1 file changed, 20 insertions(+)
```

---

## Stop gate

- Nessun file di motore toccato (gas.py, brains/, modules/, tests/): OK
- Nessuna review revisore invocata (commit doc-only): OK
- Nessun altro file toccato oltre a .claude/commands/fine-task.md e reports/ultimo_report.md: OK

---

## URL handoff

`git diff --stat ${BASE}..HEAD -- reports/handoff.md` → vuoto.

**handoff.md non rigenerato in questa sessione.**
