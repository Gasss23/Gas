# Proposta: voce via Telegram, fuori casa (roadmap R8)

Chat Mani, 7 novembre 2026, su richiesta di M1. Solo documento, nessun codice. Decide l'operatore.

## Cosa fa

1. Mandi un **messaggio vocale** al bot Telegram di Gas.
2. Il bot lo scarica da Telegram (`getFile`, formato OGG/Opus).
3. Lo trascrive con **Groq Whisper**, la stessa funzione della voce di casa (`modules/voice/stt.py`, `transcribe_audio`).
4. Passa il testo a Gas con `kernel.run_turn`, nella **stessa cronologia unica** di Telegram e della voce.
5. Risponde **in testo**, come oggi, e, se l'opzione è accesa, anche **con la voce ElevenLabs** (stessa voce di Jarvis).
6. In cima alla risposta mette la trascrizione («Ho capito: …»), così vedi subito se Whisper ha sentito male.

## Regole (non cambiano)

- **Chi può usarlo**: solo le chat in `TELEGRAM_ALLOWED_IDS`, cioè la tua. Un vocale da altre chat si scarta **prima** di scaricarlo: nessun costo, nessun audio a Groq.
- **Firme**: sempre e solo con i bottoni ✅/❌. Un «sì» detto a voce non firma mai niente: le azioni da firmare arrivano come oggi, col read-back scritto e i bottoni.
- **Regola dei modelli**: il testo trascritto segue le regole del testo scritto su Telegram (router; «forte …» detto all'inizio vale `/forte`, come nella voce di casa). I dati personali vanno solo al forte. L'audio va a Groq per la trascrizione: è lo stesso rischio già accettato per la voce di casa (R-684-2-M2), ma qui è solo la tua voce.
- **Limiti**: vocale al massimo 60 s (Telegram dice la durata prima del download), file al massimo 2 MB, testo da leggere tagliato a `GAS_TTS_MAX_CHARS`. Ogni errore (download, Groq, ElevenLabs) dà un messaggio in chiaro e il bot non cade (§9).

## Costi (stima, da verificare)

- **Trascrizione Groq**: pochi centesimi l'ora di audio. Con l'uso dell'operatore resta quasi sempre nel piano gratuito. *Non verificato oggi sul listino.*
- **Voce ElevenLabs**: consuma i caratteri del piano, come la voce di casa. È il costo vero: una risposta di 500 caratteri sono 500 caratteri del piano.
- **Cervello**: uguale al testo su Telegram.

## Opzioni

| | Cosa | Pro | Contro |
|---|---|---|---|
| **A** | Vocale → trascrizione → risposta **solo testo** | La più semplice; nessun costo ElevenLabs | Niente voce in uscita |
| **B** | Come A, più la **risposta vocale** quando mi scrivi a voce (spegnibile con `GAS_TELEGRAM_VOCE=0`) | Esperienza «Jarvis» anche fuori casa; costi solo quando parli tu | Un po' più di codice; bisogna scegliere il formato del vocale (sotto) |
| **C** | Il bot gira il vocale al **server voce** di casa (`/voice`) | Una sola strada per tutta la voce | Il bot dipende dal server voce acceso; il server porta con sé finestra, seguito e istruzioni «da dire a voce», che fuori casa non servono |

**Raccomandazione: B**, in due fette.
1. Fetta 1: la A (entrata vocale, risposta in testo con la trascrizione in cima).
2. Fetta 2: la risposta vocale.

Il formato del vocale in uscita è da provare:
- **OGG/Opus con `sendVoice`**: compare come «bolla» vocale. Va verificato che ElevenLabs lo dia direttamente.
- **MP3 con `sendAudio`**: oggi funziona già, ma compare come file audio.

## File da toccare

- `modules/telegram/bot.py` (condiviso con M2): in `_handle_update` un ramo nuovo per `msg["voice"]`, prima del controllo `if not text`. Poi tre funzioni piccole: `_scarica_vocale` (getFile + download con tetti), `_trascrivi` (chiama `transcribe_audio`), `_invia_vocale` (sendVoice o sendAudio). Il resto del flusso, dal comando `/forte` a `run_turn` e alla risposta, resta quello di oggi. Da coordinare con M2 prima di toccarlo.
- `modules/voice/tts.py`: solo se serve l'OGG, un parametro `formato` facoltativo in `synthesize_speech` (default MP3 come oggi).
- `modules/voice/stt.py`: probabilmente nulla, il nome del file `.ogg` basta a Groq. Da verificare.
- Test: un file nuovo `tests/test_unit_telegram_voce.py`, con Telegram, Groq ed ElevenLabs finti (chat non autorizzata, vocale troppo lungo, errore di Groq, firma che resta sui bottoni).
- `reports/stato_progetto.md`, roadmap R8.

## Da decidere (operatore)

1. A, B o C? Raccomandata B in due fette.
2. Con B, risposta vocale solo quando mandi un vocale, oppure sempre?
3. Chi tocca `modules/telegram/bot.py`: Mani, con la review di M2, oppure M2.
