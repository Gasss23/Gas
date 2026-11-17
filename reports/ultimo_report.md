# Ultimo report — 2026-11-17 — Voce: la parola di attivazione non arriva più al cervello (M1)

## DECISIONI UMANE RICHIESTE
1. Merge della PR (riserve BASSE).

## Esito
- Il 17/11 alle 16:28 Whisper ha scritto «Hey Jarvis» come «Jarways» e il cervello forte l'ha cercato in memoria (`ricorda`): un giro in più, ~3 s. Ora il server toglie la parola di attivazione (e le storpiature note) dall'inizio della richiesta, tranne nei seguiti, dove il vocativo dice che la frase è per Gas. «Gas ha detto…» resta com'è.
- Review #806 → #807-M1coord APPROVATO CON RISERVE (R-806-2, R-807-1 BASSE).

## Test
voice_server 236 → 249 passed (mirati dopo l'ultimo delta).

## Anomalie
CI rossa su tutti i branch per i test bwrap (runner ubuntu-26.04): correzione in un'altra chat.
