# Ultimo report — 2026-11-10 — terminale opzione A: azioni fisse di manutenzione per Gas (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR del terminale A: è un CAMBIO DI SICUREZZA (strumento nuovo `manutenzione`, livello nel cancello, aggancio in gas.py). Resta aperta fino al sì esplicito dell'operatore, anche con verdetto pulito del bot. Consigliato il secondo passaggio nella chat claude.ai col link della PR.
2. R-738-2: i vocali di Telegram arrivano a Gas come turni a testo, quindi lì lo strumento è offerto (le azioni che cambiano Gas restano comunque alla firma). Se «mai a voce» deve valere anche per i vocali di Telegram lo decide l'operatore.

## Esito

- **Terminale opzione A (codice + proposta + test)**: FATTA (e93bd77). Review #736-M2 BOCCIATO, poi #738-M2 e #739-M2 APPROVATO CON RISERVE (riserve di codice corrette prima del commit). Proposta in `reports/proposta_terminale_A.md`.
- **Merge di origin/main (#359 di Mani) nel ramo**: FATTO (32619b5), review #743-M2 APPROVATO CON RISERVE (R-743-1 BASSA: riserve del terminale A non registrate in stato_progetto → registrate ora).
- **Verifica esterna #363**: APPROVATO CON RISERVE. V-1 di gravità media (conflitto con main dopo il merge della #360): CHIUSA col merge di main (d3c490c), review #745-M2 APPROVATO. V-3 BASSA (filtro di `log_voce`): CHIUSA (94bd308, review #748-M2). V-4 BASSA (testo della firma di `aggiorna_gas`) registrata.
- **Merge di main (#362)**: FATTO (ece76a8), solo report e memoria.
- **Test**: kernel 1099 PASS / 1 FAIL (T31g, GAS_VECTORS: ambiente, preesistente); pytest manutenzione + gate + notte 1064 passed.
- **Prova dal vivo di `riavvia_voce` (launchctl) sul Mac**: DEFERITA — si fa dopo il merge.

## Anomalie

- I verdetti integrali di #736/#738/#739-M2 sono stati dati prima di un `/clear` della chat: nell'handoff c'è la loro riga di memoria del revisore, non il testo integrale.
