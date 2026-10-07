# ULTIMO REPORT — 2026-10-07 — Bot di verifica: bubblewrap prima di Claude

## Riassunto

Il setup del bot fatto dall'operatore funziona (l'App ha risposto sulla PR di prova #142), ma
Claude non partiva: lo scrub dei segreti esige bubblewrap, assente sul runner. Questa PR lo
installa prima dei modelli. Dopo il merge si rilancia la prova su #142.

## Cosa ho fatto

1. PR di prova #142 con etichetta `verifica` — per provare il bot dopo il setup.
2. Letto i log del job — errore "bubblewrap is required for subprocess env scrubbing".
3. Step `sandbox` in verifica-bot.yml (install + prova + exit 1) e m2/m3 legati al suo esito — PR #143.
4. Review #192 → #193 APPROVATO CON RISERVE (R-193-1 diagnosi, R-193-2 cosmetica).

## Cosa NON ho fatto da solo

- Nessun segreto o impostazione toccati; nessun merge.

## Cosa devi fare tu

1. Mergiare la PR #143 (tocca la macchina del bot: decide l'operatore).
2. Poi dirmi di rilanciare la prova su #142 (togliere e rimettere l'etichetta `verifica`).
3. Se il bot dà il suo verdetto: attivare il check obbligatorio `verifica-bot` nel ruleset (§F del setup).
