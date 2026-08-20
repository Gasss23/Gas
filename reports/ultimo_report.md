# Report — docs/scollega-gashistory-r2-v2

**Data:** 2026-08-20  
**Branch:** docs/scollega-gashistory-r2-v2 (nuovo branch pulito da origin/main)  
**Sostituisce:** docs/scollega-gashistory-da-r2 (conflitti con main aggiornato, abbandonato)

## Obiettivo

Riapplicare due correzioni a `reports/stato_progetto.md` sopra main aggiornato, senza risolvere conflitti a mano.

## STOP gate

✅ SOLO `reports/stato_progetto.md` + `reports/ultimo_report.md`. Nessun codice, nessun CLAUDE.md, nessun altro file. Revisore NON coinvolto (doc-only).

## Modifiche applicate

### a) Review #82 — rimozione etichetta "Riserva R2"

**Prima (su origin/main):**
```
Suite hook: **14 PASS**. Riserva R2 dichiarata: sessione interrotta prima di `/fine-task` non persiste `.gas_history.json` (trade-off accettato).
```

**Dopo:**
```
Suite hook: **14 PASS**. Trade-off dichiarato (senza etichetta R2 — R2 = memoria revisore, CHIUSO da PR #66+#87): sessione interrotta prima di `/fine-task` non persiste `.gas_history.json`. Vedi finding autonomo in §Finding aperti.
```

**Motivazione:** R2 è la label del progetto "durabilità memoria revisore", chiuso da PR #66+#87. Usarla per il trade-off `.gas_history.json` creava confusione semantica. Il trade-off rimane dichiarato ma come affermazione autonoma, non come riserva di un progetto già chiuso.

### b) Aggiunto finding autonomo 🟡 in §Finding aperti

```
- 🟡 **.gas_history.json runtime** — non persiste se la sessione muore prima di `/fine-task`. RUNTIME (kernel aggiorna il file a ogni turno sul VPS, mai auto-committato in prod); il revisore non lo tocca (non è codice motore). Competenza: `_take_snapshot` + decisione operativa (cron push/backup) da tarare al deploy VPS. NON chiuso da R2 (R2 = durabilità `memoria_revisore.md`, CHIUSO da PR #66+#87).
```

**Motivazione:** Il finding è di classe RUNTIME (non codice motore), non coinvolge il revisore, e la sua chiusura dipende da decisioni operative al deploy VPS. Tenerlo visibile in §Finding aperti assicura che non venga dimenticato.

## Verifica diff

```
 reports/stato_progetto.md | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
```

Due righe toccate: una modifica inline (riga review #82) + una aggiunta (finding autonomo). Nessun altro file.
