# ULTIMO REPORT — 2026-10-07 — FASE 2.6 fetta 1: Gas riflette a fine task

## Riassunto

Gas ora sa "riflettere" a fine task: con `gas rifletti` scrive un riassunto denso di cosa ha
fatto (che rilegge da solo al turno dopo) e propone fino a 3 lezioni, che però entrano nel suo
cervello solo se le approvi tu. Il revisore l'ha bocciata due volte per buchi di sicurezza
reali, ora chiusi; terzo giro approvato con riserve. Tutto è nella PR #149, non mergiata.

## DECISIONI UMANE RICHIESTE

1. **Merge della PR #149** (https://github.com/Gasss23/Gas/pull/149) — dopo CI verde e sì del bot.
2. **Provarla con un modello vero** sul Mac (qui non ci sono chiavi API): fai un piccolo task, poi
   `python gas.py rifletti`, guarda il recap stampato e decidi le lezioni con
   `gas lezioni approva <id>` / `gas lezioni rifiuta <id>`.
3. **Fetta 2 — quando riflettere da solo?** Oggi solo su comando. Opzioni: a ogni `clear`, a fine
   sessione, ogni N turni. Ogni riflessione costa una chiamata LLM in più.
4. **R-200-2 (ALTA, vecchia, riguarda il cancello)**: dopo un `run_command cat` il cancello non
   considera la conversazione "contaminata". Serve una fetta dedicata: decidi se farla subito.

## Esito per fetta

- **Fetta 1 — riflessione su richiesta (A recap + B lezioni)**: FATTA — commit `890cb51`, review
  #199 BOCCIATO → #200 BOCCIATO → #201 APPROVATO CON RISERVE.
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
8. Test: suite del kernel da 653 a 682 PASS, 0 FAIL (+29 test T80).

## Cosa NON ho fatto da solo

- Nessun merge, nessuna impostazione GitHub toccata.
- Nessuna prova con modello reale (mancano le chiavi qui).
- R-200-2 (cancello) non toccata: cambia la sicurezza del cancello, merita una fetta sua.

## Riserve aperte (dettaglio in reports/stato_progetto.md)

- R-201-1 (MEDIA): un'istruzione letta da file e ripetuta per 20+ turni esce dalla finestra
  controllata e può finire in un recap "fidato". Mitigazione: `GAS_RECAP_PIN_CHARS=0`.
- R-201-2 (BASSA): a schermo il recap è troncato a 1500 caratteri, se ne iniettano fino a 4000.
- R-199-3 (BASSA): il recap non scade.
- R-200-2 (ALTA, preesistente): `run_command` non conta come input non fidato per il cancello.
- F-args-pin (BASSA, preesistente): gli argomenti delle tool call compaiono in `<memoria_dati>`.

## Anomalie

- Gli hook di stop chiedevano `/fine-task` mentre la revisione era in corso: ho aspettato il
  verdetto (il gate di review vieta il commit del motore senza verdetto).
- `gh` nel cloud non può usare GraphQL: PR creata via API GitHub (MCP).
