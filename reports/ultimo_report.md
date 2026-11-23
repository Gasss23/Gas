# ULTIMO REPORT — R7 fetta 4: tetto di tempo duro del compito in sottofondo

**Data:** 23 novembre 2026
**Branch:** claude/r7-tetti-di-tempo (sotto-chat di M1)

## DECISIONI UMANE RICHIESTE

1. **Merge della PR #402** (vedi handoff §0): tocca il motore; con verdetto del bot con riserve la PR resta aperta e il merge lo chiede M1 all'operatore.

## Esito fette

- **Fetta 4 R7 — tetti di tempo duri (parte sottofondo)**: FATTA. Il processo in sottofondo arma un timer col tempo rimasto (contato dalla prima creazione): alla scadenza il compito diventa «ko» («oltre la durata massima, fermato»), parte l'avviso su Telegram e il gruppo di processi si ferma. Tempo già finito alla partenza → «ko» senza eseguire. Un solo esito tra timer e fine del turno (lock). Attesa del timer limitata a 30 giorni. Limite dichiarato: `claude -p` e il browser stanno in un gruppo proprio e finiscono la richiesta in corso. 8 test nuovi (137). Review #852-R7 → #853-R7 APPROVATO CON RISERVE (solo BASSE).
- **Tetto duro del compito del giro di notte**: DEFERITA — oggi il tetto per compito è controllato tra un evento e l'altro; serve un altro meccanismo (il giro gira nel processo principale). Prossima PR.
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA.
- **PR #398 e #399 (fette 2 e 3)**: mergiate da M1 col via dell'operatore. Il merge della #399 da questa sessione era stato negato dal controllo dei permessi (via arrivato da un'altra sessione).

## Anomalie / cose da sapere

- Letta `reports/bacheca.md`: niente che blocchi questa fetta.
