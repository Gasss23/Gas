# Report — 2026-09-23 — Sonda sola lettura: /fine-task incostante

## DECISIONI UMANE RICHIESTE

1. **F3 — causa principale "fine-task incostante"**: questa sessione è iniziata su `main` (clean, senza branch). La procedura `/fine-task §0` blocca con gate INCOMPLETO quando `BRANCH=main`. Se le sessioni vengono aperte senza creare prima un branch, fine-task non può completare. **Azione**: rafforzare il promemoria di inizio sessione (es. aggiungere a SessionStart un guard che avvisa se si è su main) o aggiornare R2/R3 in stato_progetto.md con regola esplicita.

2. **F4 — PR #89 violazione GATE POST-FINE-TASK**: tre commit post-fine-task (db8b624, c52e58b, e1d5dd8) senza ri-esecuzione di /fine-task. L'handoff di quella sessione non copriva l'ultimo commit. **Azione**: nessun fix retroattivo necessario, ma segnalare come finding ricorrente se si ripete.

3. **F1 — promemoria_end.sh non eseguibile**: il file ha `-rw-r--r--` invece di `-rwxr-xr-x`. Inerte in pratica (chiamato con `bash`), ma va allineato per coerenza: `chmod +x .claude/hooks/promemoria_end.sh`. **Azione**: decidere se correggere ora o lasciare.

---

## Scope

**Fetta 1 — Raccolta dati verbatim (sola lettura)**: `FATTA`
- Letti: settings.json, settings.local.json, tutti i 4 hook, fine-task.md, git log -30, gas_debug.log (tail -50 filtrato), claude --version.
- Nessuna modifica a file di codice, hook o settings.

---

## Esito

Sonda completata. Dati raccolti verbatim e riportati nella risposta di sessione. Findings principali:

- **F1**: `promemoria_end.sh` non ha bit eseguibile (`-rw-r--r--`). Non blocca (chiamato via `bash`), ma incongruente.
- **F2**: Nessun hook `SubagentStop` registrato in settings.json. Info.
- **F3** (causa principale): sessioni che iniziano su `main` → `fine-task §0` bloccante (`BRANCH=main`). Questa sessione stessa ne è esempio: partita su main, creato branch solo a fine raccolta dati.
- **F4**: PR #89 ha 3 commit post-fine-task senza ri-esecuzione di /fine-task (violazione GATE POST-FINE-TASK).

`gas_debug.log` (tail 50): nessuna traccia di hook/fine-task/Stop nelle ultime 50 righe — le righe visibili sono tutte WARNING di test memoria e provider 402/429 del 2026-09-21.

Claude Code version: `2.1.280`

---

## Anomalie riscontrate

- Il `promemoria_end.sh` è datato `12 set 23:33` (stessa data degli altri hook, ma permissions diverse) — probabilmente creato senza `chmod +x` in quella sessione.
- `settings.local.json` è correttamente ignorato da `.gitignore:11`.
- Tutti i path hook usano `$CLAUDE_PROJECT_DIR` (non path hardcoded) — corretto.
