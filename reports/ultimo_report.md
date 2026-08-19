# Report task — docs/scollega-gashistory-da-r2

**Data**: 2026-08-20  
**Branch**: `docs/scollega-gashistory-da-r2` (da `origin/main`)  
**Scope**: solo `reports/stato_progetto.md` + `reports/ultimo_report.md` — nessun file di codice/test/script toccato.

## Esito

COMPLETATO. Due modifiche applicate a `reports/stato_progetto.md`:

### Modifica 1 — scollega wording "R2" dal caso .gas_history.json (riga 11)

**Prima:**
> Suite hook: **14 PASS**. Riserva R2 dichiarata: sessione interrotta prima di `/fine-task` non persiste `.gas_history.json` (trade-off accettato).

**Dopo:**
> Suite hook: **14 PASS**. Trade-off dichiarato (senza etichetta R2 — R2 = memoria revisore, CHIUSO da PR #66+#87): sessione interrotta prima di `/fine-task` non persiste `.gas_history.json`. Vedi finding autonomo in §Finding aperti.

**Motivo**: R2 (durabilità `memoria_revisore.md`) è CHIUSO da PR #66 (fix/r2-durabilita-memoria-clean) + PR #87 (fix/r2-riserve-86). Usare "R2" per il caso `.gas_history.json` creava ambiguità terminologica: lo stesso label applicato a un finding chiuso e a uno aperto.

### Modifica 2 — finding autonomo .gas_history.json nei Finding aperti (dopo riga R-verdetto-evidenza)

Aggiunto:
> - 🟡 **.gas_history.json runtime** — non persiste se la sessione muore prima di `/fine-task`. RUNTIME (kernel aggiorna il file a ogni turno sul VPS, mai auto-committato in prod); il revisore non lo tocca (non è codice motore). Competenza: `_take_snapshot` + decisione operativa (cron push/backup) da tarare al deploy VPS. NON chiuso da R2 (R2 = durabilità `memoria_revisore.md`, CHIUSO da PR #66+#87).

**Motivo**: il trade-off esiste ed è reale (VPS, runtime h24). Merita un finding autonomo tracciato, distinto da R2, con la giusta competenza indicata (snapshot + decisione operativa VPS).

## STOP gate

- Nessun file di codice/test/script toccato. ✅
- `CLAUDE.md` non toccato. ✅
- File modificati: `reports/stato_progetto.md`, `reports/ultimo_report.md`. ✅

## Revisore

Non richiesto (commit di soli reports/, nessuna modifica al motore — regola gate CLAUDE.md §3).
