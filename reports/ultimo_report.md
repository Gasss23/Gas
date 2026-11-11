# Ultimo report — 2026-11-11 — voce: filtro 2, più allucinazioni di Whisper scartate (chat M2)

## DECISIONI UMANE RICHIESTE

1. PR #373: con riserve BASSE resta pronta per il «mergia» del mattino (con verdetto del bot APPROVATO pulito e CI verde la mergia la chat).
2. R-764-2-M2: un vocale Telegram «Grazie di cuore» riceve «Non ho capito bene il vocale». Va bene?
3. R-774-1-M2: «Scarica i sottotitoli a cura di Rai, grazie mille.» viene scartata in silenzio. Accettabile?

## Esito

- **Filtro 2** (varianti dei saluti, composte frase per frase, parti note solo su frasi corte, intercalari nel seguito): FATTO (438704b).
- **V-1 del bot #373** (crediti + «, grazie per la visione» o senza punteggiatura passavano al cervello): CORRETTA (789ade7) — divisione anche su , ; : e crediti che finiscono con una chiusura lunga a parola intera.
- Merge di origin/main (#370): fatto, review #777-M2 APPROVATO.
- **V-1 del bot #373 su 4559e23** («Niente.» nel seguito scartato, regressione): CORRETTA (48b605f, review #780-M2 APPROVATO).
- Review #774/#775-M2 APPROVATO CON RISERVE (BASSE/COSMETICHE), #777-M2 APPROVATO.
- Test: stt+telegram 255 passed; kernel 1134 PASS, 1 FAIL T31g (fastembed assente, come su main).

## Anomalie

Nessuna.
