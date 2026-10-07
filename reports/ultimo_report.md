# ULTIMO REPORT — 2026-10-07 — FASE 2.6 fetta 1 + merge di main (R-200-2 chiusa in #150)

## Aggiornamento (sera 2026-10-07)

Il bot aveva dato un falso NO alla #149 perché il suo testo citava R-200-2 (ALTA, vecchia).
Su decisione dell'operatore R-200-2 è stata chiusa a parte (PR #150, mergiata col sì del bot);
poi ho portato main dentro questa PR (commit bec2238, review #204 APPROVATO CON RISERVE,
kernel 689 PASS / 0 FAIL). Ora il bot rigiudica la #149 sulla versione nuova.

- **Merge di main (PR #150) in #149**: FATTA — conflitti solo su report (versione del branch) e memoria del revisore (unione).
- **R-204-1** (BASSA, test): l'allowlist `_TOOL_OUTPUT_FIDATO` ora è coperta da meno test — tracciata.
- **R-203-1** (compressione della cronologia che "lava" l'input esterno, cancello): aperta, fetta propria.

## Riassunto

Gas ora sa "riflettere" a fine task: con `gas rifletti` scrive un riassunto denso di cosa ha
fatto (che rilegge da solo al turno dopo) e propone fino a 3 lezioni, che però entrano nel suo
cervello solo se le approvi tu. Il revisore l'ha bocciata due volte e la verifica esterna una
volta, sempre per buchi di sicurezza reali, tutti chiusi; ultima review (#202) approvata con
riserve. Tutto è nella PR #149, non mergiata.

## DECISIONI UMANE RICHIESTE

1. **Merge della PR #149** (https://github.com/Gasss23/Gas/pull/149) — dopo CI verde e sì del bot.
   L'etichetta `verifica` ora è applicata; il bot rigiudica la testa del branch.
2. **Provarla con un modello vero** sul Mac (qui non ci sono chiavi API): fai un piccolo task, poi
   `python gas.py rifletti`, guarda il recap stampato e decidi le lezioni con
   `gas lezioni approva <id>` / `gas lezioni rifiuta <id>`.
3. **Fetta 2 — quando riflettere da solo?** Oggi solo su comando. Opzioni: a ogni `clear`, a fine
   sessione, ogni N turni. Ogni riflessione costa una chiamata LLM in più.
4. **R-200-2**: CHIUSA nella PR #150 (mergiata), portata qui col merge di main.

## Esito per fetta

- **Fetta 1 — riflessione su richiesta (A recap + B lezioni)**: FATTA — commit `890cb51` + `30ca64e`,
  review #199 BOCCIATO → #200 BOCCIATO → #201 APPROVATO CON RISERVE → verifica esterna BOCCIATO
  (V-1) → #202 APPROVATO CON RISERVE.
- **Fetta 2 — trigger automatico**: DEFERITA — decisione dell'operatore (costo token).
- **Fetta 3 — recap "della task correlata" + scadenza (R-199-3)**: DEFERITA — oggi si inietta sempre l'ultimo recap fidato.
- **E2E con modello reale**: SALTATA — nessuna chiave API nel container cloud.

## Cosa ho fatto (in ordine)

1. Ho riletto il report di ripartenza e riallineato il branch a main (#148). Ho scoperto che il
   catalogo "lezioni" con approvazione umana esisteva già: mancava la parte in cui Gas riflette.
2. Ho unificato la lista dei provider in una sola funzione (`_cascata_provider`), così turno
   normale e riflessione usano la stessa cascata (PR #149).
3. Ho aggiunto `rifletti()`: una chiamata LLM senza tool che risponde alle due domande della
   roadmap (recap per ripartire con poco contesto + lezioni permanenti) (PR #149).
4. Il recap finisce nel diario e torna nel prompt come DATO; le lezioni vanno in quarantena (PR #149).
5. Correzione dopo #199: il modello poteva falsificare un recap chiamando un tool di nome "recap".
   Chiuso con due difese indipendenti, ognuna col suo test (PR #149).
6. Correzione dopo #200: leggendo un file con `run_command cat` il recap risultava "fidato". Ora la
   fiducia è a lista chiusa: basta un output di tool non garantito e il recap non viene iniettato (PR #149).
7. Il recap viene stampato all'operatore; si avvisa se ha risposto un provider di riserva (PR #149).
8. Correzione dopo la verifica esterna (V-1): la compressione automatica della cronologia nascondeva
   l'output dei tool in un messaggio "utente", e il recap tornava "fidato". Ora la fiducia si
   controlla su tutta la cronologia e una cronologia compressa rende il recap non fidato. Prezzo:
   dopo letture di file/comandi/compressione i recap tornano fidati solo dopo `clear` (PR #149).
9. Test: suite del kernel da 653 a 684 PASS, 0 FAIL (+31 test T80).

## Cosa NON ho fatto da solo

- Nessun merge, nessuna impostazione GitHub toccata.
- Nessuna prova con modello reale (mancano le chiavi qui).
- R-200-2 (cancello) non toccata in questa PR: chiusa a parte nella PR #150 e portata qui col merge di main.

## Riserve aperte (dettaglio in reports/stato_progetto.md)

- R-202-1 (BASSA): note di un contatto scritte in una sessione "contaminata" sopravvivono a `clear`
  e, se Gas le ripete, possono finire in un recap fidato.
- R-202-2 (COSMETICA): il messaggio "recap non fidato" dovrebbe dire "fai `clear`".
- R-201-1 e R-201-2: CHIUSE (review #202).
- R-199-3 (BASSA): il recap non scade.
- R-200-2: CHIUSA (PR #150). R-203-1 (cancello, compressione della cronologia) e R-204-1 (BASSA, test): aperte.
- F-args-pin (BASSA, preesistente): gli argomenti delle tool call compaiono in `<memoria_dati>`.

## Anomalie

- Gli hook di stop chiedevano `/fine-task` mentre la revisione era in corso: ho aspettato il
  verdetto (il gate di review vieta il commit del motore senza verdetto).
- `gh` nel cloud non può usare GraphQL: PR creata via API GitHub (MCP).
- CI sul commit `258c8b6`: `unit-suite` mai partito ("job not acquired", guasto GitHub, nessun
  test eseguito); la ri-esecuzione via API non è ripartita. Il push di questo fine-task crea run nuove.
