# Ultimo report — 2026-11-10 — voce: allucinazioni di Whisper scartate in silenzio (chat M2)

## DECISIONI UMANE RICHIESTE

1. PR #369: merge con verdetto del bot senza finding ALTA/MEDIA e CI verde («mergia» dell'operatore via M1).
2. R-761-1: su Telegram un vocale «Grazie» ora riceve «Non ho capito bene il vocale» (prima arrivava al cervello). Va bene così o serve un messaggio diverso? (file della chat Mani)

## Esito

- **Allucinazioni note di Whisper («Grazie.», «Grazie mille», «Sottotitoli…», solo punteggiatura) scartate in silenzio, con o senza parola di attivazione**: FATTA. Niente turno né memoria; log INFO solo con l'esito.
- **Trascrizione vuota → silenzio anche con la parola di attivazione** (prima errore 400): FATTA.
- Review #761-M2 APPROVATO CON RISERVE, #762-M2 APPROVATO (R-761-3 apostrofo tipografico chiusa).
- Test: stt 140 passed; voce + telegram_voce + voce_ascolto 724 passed; browser 28 passed.
- **Prova sul Mac** (parlare senza chiamare Gas, audio corti): DEFERITA — dal vero.

## Anomalie

Nessuna.
