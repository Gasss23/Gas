# ULTIMO REPORT — R7 fetta 4 bis: tetto di tempo duro del giro di notte

**Data:** 25 novembre 2026
**Branch:** claude/r7-tetto-duro-notte (sotto-chat di M1)

## DECISIONI UMANE RICHIESTE

1. **Merge della PR #408** (vedi handoff §0): tocca il motore; con verdetto del bot con riserve la PR resta aperta e il «mergia» lo chiede M1 all'operatore.
2. **Merge della PR #402** (fetta 4, sottofondo): pronta, CI verde, bot APPROVATO CON RISERVE (una nota cosmetica); stesso flusso.

## Esito fette

- **Fetta 4 bis R7 — tetto di tempo duro del giro di notte**: FATTA. Oltre GAS_NOTTE_MAX_SEC_GIRO + 300 s il giro manda «INTERROTTO» su Telegram e si ferma da solo (prima un compito appeso dentro una chiamata bloccava la notte); il compito a metà resta in in_corso.json e il giro dopo lo riprende o lo salta; un solo avviso tra timer e fine giro; nome del compito appeso nel log; attesa del timer limitata a 30 giorni. 8 test nuovi (238). Review #866-R7 → #867-R7 APPROVATO CON RISERVE (solo BASSE/COSMETICHE).
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA — prossima PR.

## Anomalie / cose da sapere

- Letta `reports/bacheca.md` (main del 25/11): niente che blocchi questa fetta. Non toccati `clients/voice/` né `scripts/voce/` (ci lavora M1).
