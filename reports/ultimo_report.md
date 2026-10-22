# Ultimo report — 2026-10-22 sera (chat Motore)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #249 (solo documenti: decisione porte, coda dei merge svuotata).
2. Prova sul Mac dopo #247: aggiornare a main, riavviare il bot, `clear`, poi «scrivi il file prova_firma.py con dentro print(1)» → deve arrivare subito la firma.

## Esito
- PR #247 mergiata su richiesta dell'operatore («mergia 247»): FATTA — CI verde, bot APPROVATA (riserve cosmetiche: conteggio kernel 1024 in CI contro 1022 in locale, dati vecchi nell'handoff).
- Decisione porte del lettore web «solo 80/443»: FATTA la registrazione in roadmap e stato — DEFERITA la parte nel codice (chat Mani).
- Ramo della PR #141 cancellato e mail di GitHub spente: FATTA (operatore).
- Coda dei merge (`da_mergiare.md`) svuotata: FATTA.

## Anomalie
- Nella serata GitHub ha ritardato gli eventi di push: la CI è partita dopo il bot, che ha bocciato due SHA per «CI assente». Risolto ripushando.
