# Gas quando sei in giro (fuori casa o lontano dal Mac)

**Data:** 2026-11-17 · **Chat:** M1 · Richiesta dell'operatore: «lo utilizzerò tantissimo anche mentre sono in giro, in movimento, e in diversi punti della casa».

## Il limite di oggi
«Hey Jarvis» ascolta solo dal microfono del Mac: in casa, finché sei a portata del Mac. Fuori casa il Mac non ti sente. Il server voce ascolta solo dal Mac stesso (127.0.0.1) e non va aperto su internet finché Gas non è sulla VPS (sicurezza).

## Cosa funziona già, fuori casa: i vocali su Telegram
Il bot Telegram di Gas (`gas telegram`) è già in grado di:
- ricevere un **vocale** nella chat del bot;
- trascriverlo (Groq Whisper, come la voce di casa);
- rispondere **anche a voce**, con la voce di ElevenLabs (salvo `GAS_TELEGRAM_VOCE=0`).

Funziona ovunque, perché il bot fa solo connessioni in uscita, ma il Mac deve essere acceso con il bot attivo. Tetto: 30 vocali all'ora (`GAS_TELEGRAM_VOCALI_ORA`).

## A mani libere con l'iPhone (da provare)
1. **Comando Rapido «Jarvis»** (app Comandi):
   - azione «Detta testo» (lingua italiano);
   - poi l'azione di Telegram «Invia messaggio» alla chat del bot di Gas.
   
   Così basta dire «Ehi Siri, Jarvis», parlare, e il messaggio parte.
2. **Ascoltare la risposta senza guardare il telefono:** Impostazioni → Notifiche → «Annuncia notifiche», attivo per Telegram. Con AirPods o CarPlay Siri legge la risposta di Gas.
3. Limite: così il messaggio arriva come **testo** e la risposta torna come testo, letta da Siri. Con un vocale vero (tieni premuto il microfono nella chat) la risposta torna con la voce di Gas.

Da verificare sull'iPhone dell'operatore: il nome esatto delle azioni di Telegram in Comandi può cambiare tra le versioni dell'app.

## Più punti della casa
- Il filtro sulla voce (in sviluppo: registrazioni da più stanze e in movimento) serve a prendere le chiamate deboli da lontano senza far tornare le false attivazioni.
- Se in una stanza il Mac non sente proprio (punteggio sotto 0,25), la strada è un secondo microfono o altoparlante lì (per esempio un vecchio telefono o un Raspberry Pi con lo stesso ascolto). È una fetta futura, da decidere.

## Prossimo passo vero (roadmap)
Gas sulla VPS, con il server voce raggiungibile in HTTPS col token: allora un comando rapido dell'iPhone potrà mandare l'audio direttamente a Gas e ricevere la sua voce, senza passare da Telegram.
