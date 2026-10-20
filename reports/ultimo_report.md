# ULTIMO REPORT — 2026-10-20 — Allineamento documenti, firma notturna 24 h, autonomia dopo una lettura

Ramo `feat/merge-automatico-z1xjx2`. PR da mergiare SOLO con l'ok dell'operatore (richiesto il 20 ott).

## DECISIONI UMANE RICHIESTE

1. Merge della PR (ok dell'operatore richiesto dopo il riassunto del mattino).
2. Fetta di sicurezza (autonomia): secondo passaggio indipendente nella chat claude.ai, come da CLAUDE.md (istituzione E).

## Esito

- **Documenti allineati alle decisioni del 19 ottobre** (approvate dall'operatore: «applicale tutte») — FATTA. CLAUDE.md §2 (Ollama rimosso dal piano, Claude futuro cervello forte via abbonamento, regola dei modelli) e §3 (tutto nel repo o negli ambienti di Gas); fine-task.md rimanda alla regola di merge di CLAUDE.md §10; gas_identity.md con la cascata del codice; README con cosa fa Gas; roadmap con la scelta A su R2 (nessun freno sulla finestra delle 5 ore); stato con le decisioni; roadmap_sintesi.md tolto. Review #364 APPROVATO CON RISERVE (R-364-1 chiusa), #365 APPROVATO.
- **Firma notturna 24 h** (R1) — FATTA. `GAS_APPROVAL_TIMEOUT_NOTTE_SECS` (default 86400) per i kernel del giro notturno; di giorno 30 min. Review #366 APPROVATO CON RISERVE: R-366-1 BASSA (una richiesta notturna occupa fino a 24 h uno dei 5 posti in attesa) dichiarata in setup_notte.md.
- **Autonomia dopo una lettura** (R1, supera C-d e R-203-2) — FATTA. Dopo una lettura restano liberi rubrica e file normali; restano alla firma `reports/`, `knowledge/`, i file ignorati da git, il codice e tutto ciò che esce. Controllo anche sul file vero (cartella di lavoro, symlink). Review #367 BOCCIATO (R-367-1 MEDIA: file ignorati da git sovrascrivibili senza foto di sicurezza → chiusa), #368 APPROVATO CON RISERVE (R-368-1 chiusa), #369 APPROVATO. Aperta R-367-2 BASSA (iniezione persistente via rubrica, mitigata dal pin sanitizzato).
- **Note di bot e verifica esterna su `cc89588`** — verifica esterna APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/222#issuecomment-6289084417)): V-1 MEDIA (script e file di avvio liberi dopo una lettura) CHIUSA → liberi solo i documenti md/txt/csv (review #370). Bot BOCCIATO: V-1 MEDIA (la contaminazione si ricicla attraverso la memoria) CHIUSA → contatti e righe di diario «non fidati» contaminano il turno che li rivede, anche in un kernel nuovo (review #371 BOCCIATO → #372 APPROVATO CON RISERVE). Riserve: R-370-2 (.csv con formule), R-372-1 (segno di sessione perso se il processo riparte senza `clear`), R-372-2 (cosmetica).
- **Secondo giro su `9f6761c`** — bot APPROVATO CON RISERVE (neutral: decide l'operatore), solo BASSE: R-bot222-1 il segno «non fidato» su un contatto non si toglie mai (serve un comando dell'operatore), R-bot222-2 segno in una transazione separata. Verifica esterna ([commento](https://github.com/Gasss23/Gas/pull/222#issuecomment-6289683155)) APPROVATO CON RISERVE: V-1 MEDIA chiamate parallele nella stessa risposta non contaminate → CHIUSA (review #373); R-ve222-2 BASSA il segno del diario scade quando la riga esce dal pin.
- **Terzo giro su `ee5eaf9`** — bot APPROVATO CON RISERVE (neutral), verifica esterna ([commento](https://github.com/Gasss23/Gas/pull/222#issuecomment-6290018021)) APPROVATO CON RISERVE: nessuna ALTA/MEDIA. Note BASSE: PR in conflitto con main dopo #221 (risolto con un merge di main: conflitti solo nei log di sessione); handoff con numeri presi prima dell'ultimo commit; decisioni del 19-20 ottobre da confermare dall'operatore; dopo una lettura restano liberi anche README/docs/tests in .md e i cambi di recapito o la chiusura di un lead (proposta: avviso su Telegram).
- **Bot su `39401b3`** — APPROVATO CON RISERVE ma check failure per V-1 MEDIA: il segno del diario si autoalimentava (ogni turno sarebbe rimasto contaminato) → CHIUSA: le righe marcate entrano nel pin senza dettagli e senza nome dello strumento (review #374 BOCCIATO → #375 APPROVATO CON RISERVE); V-2 BASSA docstring notte.py aggiornata.
- **Test** — kernel 913 PASS 0 FAIL; pytest tests/ 1497 passed.

## Anomalie

- Durante la review #367 il revisore ha modificato per errore `gas.py` nel working tree (mutazione partita nella cartella sbagliata) e lo ha ripristinato subito dall'index; verificato pulito prima del commit.
