# Ultimo report — 2026-11-11 — voce più veloce: connessione verso ElevenLabs riusata (chat M2)

## DECISIONI UMANE RICHIESTE

1. PR #372: la verifica esterna dà APPROVATO CON RISERVE (solo BASSE/COSMETICHE, chiuse con questo giro): resta pronta per il «mergia» dell'operatore, salvo un verdetto del bot APPROVATO pulito con CI verde (allora la mergia la chat).

## Esito

- **Connessione HTTPS verso ElevenLabs tenuta aperta fra le frasi della risposta a voce**: FATTA. Una per thread; buttata dopo 20 s ferma o se il server l'ha già chiusa (select a 0 s); nuovo tentativo SOLO se la connessione riusata cade durante l'invio (niente doppio addebito); `GAS_TTS_KEEPALIVE=0` la spegne.
- Review #765, #768, #770 (con riserve, chiuse), #771, #772, #776 (merge di main) APPROVATO.
- V-1 del bot #372 e V-1 della verifica esterna #372: chiuse.
- Test: tts 40 passed; tts+stt dopo il merge 180 passed; kernel 1134 PASS, 1 FAIL T31g (fastembed assente, come su main).
- **Misura del guadagno reale sul Mac** (`gas.voce.tempi`): DEFERITA — serve la rete vera.

## Anomalie

Nessuna.
