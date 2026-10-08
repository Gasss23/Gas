# ULTIMO REPORT — 2026-10-08 — Bot di verifica: niente più falsi NO per riserve già note

## Riassunto

Il bot dava un NO definitivo a PR buone quando nel testo citava un problema grave già noto
del progetto (es. "R-203-1 (ALTA, preesistente)"): è successo due volte alla #149. Ora quelle
citazioni non bloccano più; i problemi veri della PR continuano a bloccare. PR di questa fetta
da mergiare (tocca il bot: decide l'operatore), poi si rilancia il bot sulla #149.

## Cosa ho fatto

1. Trovata la causa: `_gravita_nel_testo` contava ogni ALTA/MEDIA dopo "FINDING:", anche nelle citazioni di riserve vecchie (riserva R-161-1).
2. Correzione mirata in `scripts/bot_esito.py`: dalle citazioni `R-<n>-<n> (...)` si toglie solo la parentesi; tutto il resto conta ancora.
3. Prompt del bot: le riserve vecchie si citano come "R-203-1 (ALTA, preesistente)", mai come finding.
4. Test: 297 passed; i due verdetti reali della #149 ora danno solo BASSA/COSMETICA (quindi sì).
5. Review #205 BOCCIATO (la prima versione nascondeva gravità scritte a parole e dentro parentesi annidate) → corretta → #206 APPROVATO CON RISERVE.

## Cosa NON ho fatto da solo

- Nessun merge: la PR tocca il bot, il bot dirà "decide l'operatore".
- R-205-1 / R-205-2 (basse) solo registrate.

## Cosa devi fare tu

1. Mergiare la PR di questa fetta (o dirmi "mergiala").
2. Poi io aggiorno la #149 con main: il bot la rigiudica e, se dice sì, la mergio.
