# DA MERGIARE — coda della chat Motore

> Decisione dell'operatore (2026-10-21): la chat Motore lavora di fila sulla roadmap; qui si accumula ciò che è pronto, una voce per fetta, con i pro e i contro del merge. L'operatore passa 1-2 volte al giorno, legge questa pagina e scrive «mergia #N» oppure «no». Le voci mergiate si tolgono.

> **C6 deciso (2026-10-21):** l'operatore ha scelto (a) «lasciamo così»: una firma per ogni azione, niente «Modifica» né firme a gruppi.

## PR aperta del ramo `feat/merge-automatico-z1xjx2` (nuova, dopo il merge di #236)

### 1. Storia condivisa tra bot e terminale: ultime riserve del bot (roadmap R7, R-c4b3-4)
- **Cosa:** quando il bot Telegram e il terminale scrivono la stessa storia, durante un turno il modello non vede mai i messaggi dell'altro processo (prima succedeva al primo salvataggio del turno); se un salvataggio fallisce, i messaggi dell'altro non finiscono doppi.
- **Pro:** chiude le riserve rimaste dopo il merge di #236; un test passa dal turno vero (provider giù, nessuna risposta finale).
- **Contro:** se un altro processo ha scritto, i messaggi del turno in corso restano solo in memoria fino alla fine del turno (un kill -9 a metà li perde, R-438-2).
- **Controlli:** revisore #438 (chat Motore) APPROVATO CON RISERVE; kernel 994 PASS, pytest 1816 passed. Bot V-B: success con riserve basse.

### 2. `gas compress-history` onesto (R-438-1, R-439-1)
- **Cosa:** il comando di compressione della storia ora salva anche quando un altro processo ha scritto nel frattempo, e dice «Compressi» solo se la storia compressa è davvero su disco (altrimenti «NON salvata» ed exit 1).
- **Pro:** niente più falso «ok» su un'operazione manuale.
- **Contro:** nessuno di rilievo (al più un «NON salvata» prudente se fallisce solo il secondo salvataggio, R-440-1).
- **Controlli:** revisori #439, #440 APPROVATO CON RISERVE; kernel 996 PASS.

### 3. Regola «grave» del bot di verifica (macchina del bot, autorizzata dall'operatore)
- **Cosa:** il bot non blocca più per una frase come «non la considero più grave»; continua a bloccare «non mitigato: grave», «non è la più grave», ecc.
- **Pro:** toglie il falso rosso che bloccava la #240.
- **Contro:** tocca la macchina del bot (il check sarà «neutral»: decide l'operatore).
- **Controlli:** revisori #441 (BOCCIATO, corretto), #442, #443 APPROVATO; suite del bot 325 passed.
