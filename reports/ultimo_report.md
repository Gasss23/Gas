# Ultimo report — 2026-11-09 — voce via Telegram, fetta 2 (chat Mani): risposta anche a voce

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 2 Telegram: review APPROVATO CON RISERVE (solo BASSE), PR nel perimetro, quindi decide l'operatore via M1.
2. Prova dal vivo (R-717-3): mandare un vocale al bot e controllare che la risposta arrivi anche come nota vocale. Se Telegram rifiuta l'MP3, arriva l'avviso «Risposta vocale non inviata».

## Esito

- **PR #353 (fetta 1)**: MERGIATA (7a9fad4) col sì dell'operatore.
- **Voce via Telegram, fetta 2**: FATTA (decisione dell'operatore del 9/11: risposta a voce SOLO dopo un vocale).
  - Prima arriva il testo, poi la parte parlata della risposta finale (parte_parlata, come la voce di casa), sintetizzata con ElevenLabs e mandata con sendVoice.
  - Gli output degli strumenti non vanno né a voce né a ElevenLabs. Niente voce se il turno è in errore, dopo un testo o con «forte» senza richiesta.
  - GAS_TELEGRAM_VOCE=0 la spegne. Senza chiave, con un errore di sintesi o con l'invio rifiutato arriva un avviso breve.
- **Riserve chiuse**:
  - V-1 bot #353: l'import di stt è protetto;
  - V-1 ve #353: test di read(MAX+1);
  - R-712-2;
  - V-1 bot #351: test esatto «log ogni 100»;
  - V-2 ve #351: test di inf/nan;
  - R-717-1/2: test dell'eccezione e di ok:false.
- Test: telegram_voce da 31 a 51, ascolto 295 passed. Mutanti presi.
- Review #717 e #718 APPROVATO CON RISERVE.
