# Ultimo report — 2026-11-10 — voce: correzioni dell'audit notturno (chat M2)

## DECISIONI UMANE RICHIESTE

1. PR #367: merge con verdetto del bot senza finding ALTA/MEDIA e CI verde (sì dell'operatore riferito da M1: «mergia tutto quello che il bot ha approvato»).

## Esito

- **B1 timeout del socket del server voce (60 s)**: FATTA.
- **B2 «Hey Jarvis, forte: …» al forte (anche parola ripetuta)**: FATTA.
- **B3 risposte rotte di Groq ed ElevenLabs → errore di rete** (sintesi, elenco voci, libreria, aggiunta voce): FATTA.
- **B4 `.env` del proxy del browser con le regole di Gas**: FATTA.
- **B5 JSON di forma sbagliata → 400**: FATTA.
- **Miglioramenti** (413 su corpo e prompt, porta prima del kernel, proxy che segue GAS_VOICE_PORT): FATTA.
- **Sospetti da valutare di M1** («forte» detto durante «Sì, signore?», blocco per IP condiviso su 127.0.0.1, connessione ElevenLabs riusata): DEFERITA — non toccati in questa PR.
- Review #752-M2 APPROVATO CON RISERVE (BASSE), #755-M2 APPROVATO (R-752-2/3 chiuse), merge di main #759-M2 APPROVATO.
- Test: suite voce -k "audit or not browser" 808 passed; voice_server/stt/tts con i test browser 347 passed.

## Anomalie

Nessuna.
