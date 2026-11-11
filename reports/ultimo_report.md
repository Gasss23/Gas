# Ultimo report — 2026-11-11 — voce più veloce: connessione verso ElevenLabs riusata (chat M2)

## DECISIONI UMANE RICHIESTE

1. PR #372: merge con verdetto del bot APPROVATO pulito e CI verde (regola notturna di M1); con riserve resta pronta per il mattino.

## Esito

- **Connessione HTTPS verso ElevenLabs tenuta aperta fra le frasi della risposta a voce**: FATTA. Una per thread; buttata dopo 20 s ferma; nuovo tentativo solo se la connessione riusata risulta chiusa prima della risposta (niente doppio addebito); `GAS_TTS_KEEPALIVE=0` la spegne.
- Review #765-M2 APPROVATO CON RISERVE (R-765-1 MEDIA doppio addebito, R-765-2 MEDIA connessione ferma, R-765-3 BASSA test: tutte chiuse prima del commit), #768-M2 APPROVATO.
- Test: tts 37 passed; voice_server, stt, prova_voci, telegram_voce, contesto 428 passed.
- **Misura del guadagno reale sul Mac** (`gas.voce.tempi`): DEFERITA — serve la rete vera.
- **Latenza del cervello (5-9 s alla prima frase)**: DEFERITA — sta in `brains/` e `gas.py` (streaming della prima frase da `claude -p`): fetta separata, da concordare.

## Anomalie

Nessuna.
