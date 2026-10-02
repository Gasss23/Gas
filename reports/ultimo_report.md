# Task: /fine-task robusto — gate pre-commit + post-push
**Data:** 2026-10-02
**Branch:** chore/fine-task-robusto

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR su main (URL da §0 di handoff.md).

---

## Esito fette

**Fetta 0 — SONDA**: `FATTA`
- PR #108 verificata MERGED su main (2026-10-02T15:46:50Z).
- Sezioni rilevanti di fine-task.md lette VERBATIM (URL in §5 già presente ma senza guardia HEAD==@{u} né gh run watch).
- `git log -p --since="10 days ago" -- .claude/commands/fine-task.md`: nessun output = nessuna modifica negli ultimi 10 giorni.

**Fetta 1 — Modifica .claude/commands/fine-task.md**: `FATTA`
- Aggiunto blocco "Gate pre-commit obbligatori" in §4bis, prima del commit:
  - Gate A: `python3 scripts/check_handoff.py`
  - Gate B: `python3 scripts/check_verdetto.py`
  - Gate IP: `git grep -nE '([0-9]{1,3}\.){3}[0-9]{1,3}' -- reports/` con filtri gasmerge-ip-ok e 127.
  - Nota titoli: puntare alle regex degli script, vietato inventare varianti.
- Aggiunto blocco "Post-push obbligatorio" in §4bis, dopo il push:
  - `gh run watch` (esito REALE in §6)
  - Guardia `HEAD == @{u}` prima di stampare URL
  - `echo "URL_HANDOFF: ..."` con SHA lungo — SEMPRE, prima del cat.

**Fetta 2 — Prova reale (gate a–d su questa sessione)**: `FATTA`
- Eseguita durante questo /fine-task (vedi handoff §6 per esito CI e URL_HANDOFF stampato).

**Stop gate**: rispettato — toccato solo `.claude/commands/fine-task.md` e `reports/`.

---

## Anomalie

Nessuna anomalia. Nessun IP trovato nei report.
