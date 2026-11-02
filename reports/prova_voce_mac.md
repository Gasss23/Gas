# Prova della voce sul Mac — guida di una pagina

Aggiornata al 2 novembre (V5 provata sul Mac dall'operatore, esito riferito da M1 il 2 novembre: eco, «sì» e TV ok; V6 «capire meglio»).
Serve per provare la conversazione a voce con Gas: tu parli, Gas risponde a voce, e puoi interromperlo.

## Prima volta: cosa deve esserci nel `.env` di Gas

Nel file `~/Gas/.env` servono queste righe (i valori li hai già, non scriverli in chat):

- `GAS_VOICE_TOKEN=...` (una parola segreta qualsiasi, la stessa per server e pagina)
- `GROQ_API_KEY=...` (trascrive la tua voce)
- `ELEVENLABS_API_KEY=...` (fa parlare Gas)
- `GAS_CLAUDE_CLI=1` (solo se vuoi il cervello forte con «Gas, forte: …»)

## Avvio (due finestre del Terminale)

1. **Prima finestra** — il server della voce:
   ```
   cd ~/Gas && git pull origin main && python3 -m modules.voice.server
   ```
   Aspetta la riga «✓ gas voice: in ascolto su …» (all'inizio compare «avvio in corso», ci mette qualche secondo).
2. **Seconda finestra** — la pagina:
   ```
   cd ~/Gas && python3 clients/voice/browser_server.py
   ```
3. Apri **http://127.0.0.1:9000** nel browser (Chrome va bene) e consenti il microfono.
4. Lascia spuntato «conversazione continua», clicca il tasto rotondo (o premi spazio) e parla.

Sopra la risposta c'è la riga «Ho capito: …» con la frase come l'ha sentita Gas: se è sbagliata, l'errore è d'ascolto (non di ragionamento). Se la trascrizione è poco sicura, Gas dice «Non ho capito bene, puoi ripetere?» invece di rispondere a caso.

Come funziona: quando smetti di parlare la frase parte da sola; Gas risponde a voce (la risposta intera è scritta sotto); poi il microfono resta aperto 12 secondi per la tua risposta. Se stai zitto senti un bip e la conversazione si chiude.

## I 3 test

**Test 1 — eco (il più importante, fallo per primo).** Tieni le casse accese, a volume normale. Fai una domanda che porti a una risposta lunga (per esempio «raccontami in tre frasi cosa sai fare») e **resta zitto** mentre Gas parla.
- Va bene se Gas finisce di parlare da solo.
- Non va bene se Gas si zittisce a metà senza che tu abbia parlato (sente la sua stessa voce).

**Test 2 — «sì» a voce normale.** Chiedi qualcosa che finisca con una domanda (per esempio «Gas, preparo una bozza per i lead di oggi?»). Appena Gas ha finito, rispondi subito «sì» a voce normale, senza alzare la voce.
- Va bene se la scritta passa a «parli…» e poi a «invio…».
- Non va bene se la conversazione si chiude «per silenzio» come se non avessi detto niente.

**Test 3 — TV accesa.** Accendi la TV (o un video) a volume normale, poi apri la conversazione e **non parlare**.
- Va bene se dopo 12 secondi senti il bip e la conversazione si chiude.
- Non va bene se Gas «sente» frasi da solo e risponde a cose che non hai detto.

(Facoltativo: mentre Gas parla, parlagli sopra. Deve zittirsi e ascoltarti.)

## Scegliere la voce di Gas (pagina «prova voci»)

Con le due finestre accese, apri **http://127.0.0.1:9000/voci**. In cima ci sono le candidate: voci maschili, calme, con accento britannico, prese dall'elenco del tuo account ElevenLabs. Scegli una frase, premi «ascolta» su ogni voce, poi «scelgo questa»: la pagina ti dà la riga da mettere nel `.env` (`ELEVENLABS_VOICE_ID=…`). Riavvia la prima finestra e Gas parla con la voce nuova. Ogni ascolto spende un po' di caratteri ElevenLabs (al massimo 40 prove all'ora). Se sul Mac c'è Piper (`GAS_PIPER_MODEL` nel `.env`), compare anche una voce locale gratis, per ora solo da ascoltare.

Più in basso c'è **«Dalla libreria di ElevenLabs»**: voci di altri utenti scelte con gli stessi criteri. «anteprima» fa sentire il loro esempio (può non essere in italiano; che sia gratis è da verificare). «aggiungi al mio account» chiede conferma: la voce probabilmente occupa uno spazio voce dell'account (da verificare), e solo dopo si prova con la frase italiana nell'elenco in alto. Costi e limiti del tuo piano Gas non li ha potuti verificare: guarda il link nella pagina prima di aggiungere. Se la sezione dice «Libreria non disponibile», il tuo piano probabilmente non la include.

## Se qualcosa va storto

- **Test 1 non va (Gas si zittisce da solo):** aggiungi `GAS_VOICE_INTERRUZIONE=0` nel `.env`, chiudi e riavvia la seconda finestra (la pagina), ricarica il browser. Così non puoi più interrompere Gas, ma lui non si zittisce più da solo. Dillo a M1.
- **Test 2 non va (il «sì» non conta):** dillo a M1 con una frase su come hai parlato (vicino/lontano dal microfono). Si abbassa la soglia della voce.
- **Test 3 non va (sente frasi dalla TV):** dillo a M1. Intanto, dopo 5 turni di fila Gas si ferma da solo e chiede un clic, e oltre 60 richieste all'ora il server rifiuta: non può andare avanti all'infinito.
- **Con ventilatore o TV accesi Gas si interrompe da solo o «sente» frasi che non hai detto:** aggiungi `GAS_VOICE_AGC=0` nel `.env` (spegne il guadagno automatico del microfono, che nelle pause alza il rumore), riavvia la seconda finestra e ricarica la pagina. La pagina ora stima da sola il rumore di fondo e alza la soglia della voce di conseguenza.
- **«Voice server non raggiungibile»:** la prima finestra non è partita o si è chiusa. Riavviala e aspetta «in ascolto».
- **«Gas non ha risposto entro 600 s»:** il cervello forte ci sta mettendo tanto. NON ripetere la richiesta: guarda la prima finestra, il lavoro può essere ancora in corso.
- **«Troppe richieste a voce nell'ultima ora»:** hai superato il tetto di 60 richieste a voce in un'ora. Aspetta o scrivi.
- **Gas dice spesso «Non ho capito bene» anche quando parli chiaro:** aggiungi `GAS_VOICE_STT_LOGPROB_MIN=-1.3` nel `.env` e riavvia la prima finestra (il server). Se invece risponde a frasi sentite male (la riga «Ho capito» è sbagliata), prova `-0.8`. Dillo a M1.
- **Nessun audio, solo testo:** controlla `ELEVENLABS_API_KEY` nel `.env`.
- **«permesso microfono negato»:** consenti il microfono per 127.0.0.1 nelle impostazioni del browser e ricarica.

Per chiudere: Ctrl-C nelle due finestre.
