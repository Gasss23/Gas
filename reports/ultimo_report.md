# Ultimo report — 2026-11-06 — Fetta 3 voce: compiti lunghi in sottofondo (chat M2)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #345 (con riserve BASSE: sì via M1).
2. Prova sul Mac: a voce un compito lungo → «ci lavoro» e poi avviso su Telegram.

## Esito delle fette

- **PR #344** (rifiuto di --effort + proposta): `MERGIATA` (44dbe2d).
- **Fetta 3 (PR #345)**: `FATTA` — `in_sottofondo` solo a voce, processo separato, solo forte, avviso Telegram; review #695-M2 + #696-M2 APPROVATO CON RISERVE.
- **Correzioni dopo bot e verifica esterna (c19e9df)**: `FATTE` — bot V-1 MEDIA (avviso promesso anche se Telegram non può) chiusa con diniego; posto `attivo.json` preso in modo atomico (R-697-1 MEDIA chiusa); killpg solo se il processo è nostro (R-698-1 chiusa); review #697 riserve, #698 BOCCIATO, #699-M2 APPROVATO CON RISERVE (R-699-1/2-M2 BASSE).
- **CI rossa su e323b60**: `CORRETTA` (b865195, `ps -ww`; review #700-M2 APPROVATO).
- **Fette 3.2 e 3.3**: `DEFERITE`.
- Test: kernel 1096 PASS 0 FAIL; sottofondo 34 passed.

## Anomalie

- Nessuna.
