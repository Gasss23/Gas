# ULTIMO REPORT — 2026-10-06 — R-150-1: push fallito in fine_task_finale.sh esce dal suo ramo

## Decisioni umane richieste

1. Merge della PR di `fix/fine-task-push-exit` (numero nell'handoff §0). Rischio basso: tocca solo il ramo d'errore del push.
2. Nota merge: questo branch riscrive i report canonici come tutte le PR della notte; dopo il merge di un'altra PR serve riportare main nel branch (conflitto solo su `reports/`).

## Esito per fette

- **R-150-1 (bassa, preesistente, review #150)**: FATTA — `PUSH_EXIT=0; git push || PUSH_EXIT=$?` in `scripts/fine_task_finale.sh`: con `set -e` riattivato dal gate IP, un push fallito ora stampa "ERRORE git push fallito" ed esce con 1 (prima: codice di git senza messaggio, ramo morto).
- **Test T-finale-5**: FATTA — remoto bare con `pre-receive` che rifiuta → exit 1, messaggio, nessun URL, nessuna uscita dalla guardia @{u}. Fallisce sul codice vecchio (provato).
- **Review**: #166 APPROVATO CON RISERVE (R-166-1 frase in stato_progetto, R-166-2 assert sulla guardia: entrambe CHIUSE) → #168 APPROVATO. La #166 era stata numerata #163 dal revisore (collisione con la #163 di B2, PR #131): rinumerata in memoria con nota.

## Anomalie

- Nessuna. `gh` non autenticato nel container: PR via connettore GitHub.
