# ULTIMO REPORT — 2026-10-29 — chat M1: ponte voce → sviluppo (PR #307) e coordinamento delle chat

## DECISIONI UMANE RICHIESTE
1. Merge della PR #307: la review #558-M1 è APPROVATO CON RISERVE (CLAUDE.md §10).
2. Per attivare il ponte sul Mac:
   - creare un token GitHub fine-grained con solo **Issues: Read and write** sul repo `Gas-richieste`, salvato in `~/.config/gas/richieste_token`;
   - aggiungere `GAS_RICHIESTE_REPO=Gasss23/Gas-richieste` al `.env`.
3. Decidere se `GAS_VOCE_FORTE=1` (tutta la voce al cervello forte).
4. Approvare il permesso Remote Control per M1: la richiesta è in sospeso.

## Esito
- **Ponte voce → sviluppo, strada A**: FATTA, PR #307. Lo strumento `richiedi_sviluppo` scrive una issue nel repo PRIVATO `Gas-richieste`:
  - token dedicato, con tetto giornaliero;
  - nessun redirect seguito;
  - a finestra contaminata la richiesta va alla firma.

  Review #557-M1, poi #558-M1: APPROVATO CON RISERVE, con le riserve MEDIA e BASSE chiuse.
- **Coordinamento delle chat**: FATTA. Le regole sono scritte in `reports/stato_progetto.md`. M2 è stata ricreata («M2 — sviluppo voce»), perché la vecchia rifiuta i messaggi.
- **PR delle altre chat**, mergiate da M1 col sì dell'operatore: #303 e #305 (Mani), #304 (M2).
- **Test**: kernel da 1063 a 1065 PASS, 0 FAIL. pytest completo: 2577 passed.

## Anomalie
- `gh` non è autenticato nel cloud: PR e CI passano dallo strumento GitHub.
- Strada B del ponte (Gas avvia Claude Code da solo) rimandata, come deciso dall'operatore.
