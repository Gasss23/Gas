# Ultimo report — 2026-11-20 — Bot di verifica: falso rosso «Non bloccante» corretto

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa correzione: tocca la macchina del bot, quindi il check `verifica-bot` è neutral e il merge lo decide l'operatore. L'operatore ha scelto questa strada in chat («fai quello, sicurezza massima», poi «ok avvisami quando hai mergiato»).
2. Da decidere: aggiungere al bot come gravi anche «alto», «severo», «serio», «elevato» (nota del revisore #831, fuori da questa correzione).
3. Restano quelli della PR #388 (password delle copie, `pip install`, `pwd`, secondo passaggio su claude.ai).

## Esito
- **Correzione del bot**: FATTA (4c982142, review #831 e #832 APPROVATO CON RISERVE).
  - Sulla PR #388 il bot aveva messo il check in rosso con «finding MEDIA», ma il suo verdetto era APPROVATO CON RISERVE con una sola nota BASSA. La frase «Non bloccante:» a inizio frase veniva letta come gravità, perché la negazione valeva solo per «non» minuscolo.
  - Ora vale anche «Non» con l'iniziale maiuscola. «NON» tutto maiuscolo, le gravità maiuscole e quelle tra parentesi restano bloccanti come prima.
  - Prova del revisore: 648.144 frasi generate, nessuna differenza tra «Non …» e «non …».
- **Dopo il merge**: nuovo giro del bot sulla PR #388, che poi si mergia se è verde.

## Test
- `tests/test_unit_verifica_bot.py`: 627 su main → 630 passed. Il test del caso reale fallisce col codice di main; i casi che devono restare bloccati uccidono i mutanti indicati dal revisore.

## Riserve aperte
- R-832-1 COSMETICA: nessun test per «Non: grave» (punteggiatura subito dopo «Non»); oggi il comportamento è giusto.
