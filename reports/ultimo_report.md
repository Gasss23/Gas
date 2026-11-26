# Ultimo report — 2026-11-26 — Mani alla voce F3: avviso, annullo, esiti su Telegram

Sotto-chat di M1 (session_01FgYcG4uNEqggobeJsbmE93), ramo `claude/mani-voce-f3-avvisi` (sopra `claude/mani-voce-f3`, PR #411, in attesa del «mergia» dell'operatore).

## DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta (dopo la #411): revisore APPROVATO CON RISERVE (R-881MV-1 bassa), quindi decide l'operatore (CLAUDE.md §10).
2. Sul Mac, dopo il merge: nel `.env` mettere `GAS_RICHIESTE_AUTORI=` con il login GitHub di chi scriverà gli esiti (l'account con cui lavora l'esecutore; per ora il proprio, es. `Gasss23`). Senza, Gas non legge nessun esito (è voluto: fail-closed). Opzionali: `GAS_RICHIESTE_CONTROLLO_MIN` (default 5), `GAS_RICHIESTE_ESITI_GIORNO` (default 20). Poi riavviare il bot Telegram.

## Esito per fetta

- **F3 — Gas avvisa e legge gli esiti**: FATTA (6fce9e43).
  - Avviso su Telegram APPENA una richiesta di sviluppo è accodata, con «annulla richiesta N» (al posto della firma a voce rifiutata dall'operatore il 26/11). Se l'avviso non parte, la richiesta resta e il modello lo dice.
  - «annulla richiesta N» dal bot Telegram, prima del modello, solo da messaggio nuovo: chiude la issue con l'etichetta `annullata` (solo issue aperte `da-gas` nel repo privato).
  - Ogni 5 minuti il bot legge i commenti nuovi del repo delle richieste e manda all'operatore la frase degli ESITO validi di autori ammessi su issue `da-gas`; tetto 5 per controllo e 20 al giorno; paginazione; esiti di autori non (ancora) ammessi tenuti in sospeso; ricorda la PR per cui la domanda di merge è stata fatta davvero (R-873MV-1, per F4). Il thread sta in `cassetta.py`, non nel bot (guardia T78p rispettata).
  - Chiuse anche la V-1 della verifica esterna #411 (tutte le virgolette Pi/Pf) e la cosmetica 5 (commenti scartati nel log).
  - Test: `tests/test_unit_cassetta.py` (71) + esiti + richieste = 197 passati; kernel 1210 PASS 0 FAIL (T100c/T100d: round-trip con l'avviso). Nuovo passo CI «Run cassetta suite».
  - Revisore #879-MV APPROVATO CON RISERVE → #880-MV BOCCIATO (perdita di esiti con la pagina piena, vera) → #881-MV APPROVATO CON RISERVE.
- **Correzione dopo verifica esterna e bot sulla #412**: FATTA (9f4650d6). Verifica esterna V-1 (gravità media, vera): con il file di stato non scrivibile lo stesso esito tornava a ogni controllo; ora lo stato si scrive prima dell'invio e senza scrittura non si invia. Più: issue sparita (404/410) non blocca la fila, repo privato controllato anche in lettura, domanda di merge cambiata solo da esiti più recenti (lapide). 206 test, kernel 1210 PASS. Revisore #882-MV → #883-MV APPROVATO CON RISERVE (R-883MV-1 bassa, per F4).
- **F3b — esiti letti a voce**: DEFERITA — prossima fetta piccola.
- **F4, F5**: DEFERITE — dopo.

## Anomalie

- Il lavoro di F3 è stato messo da parte (copia nello scratchpad, mai `git stash`) per committare la correzione della #411 dalla worktree `/home/user/Gas-411`, perché il gate guarda sempre la cartella principale; poi rimesso e riallineato sulla #411.
- Riserve aperte: R-883MV-1 BASSA (per F4), R-881MV-1 BASSA, R-881MV-2 COSMETICA, R-873MV-1 BASSA (per F4), R-877MV-2 COSMETICA.
