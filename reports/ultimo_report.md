# Ultimo report — 2026-11-05 — fetta 43 parte 2 (chat Mani): finestra di 40 s e difese contro il parlato della stanza

## DECISIONI UMANE RICHIESTE

1. Merge della PR #341 (https://github.com/Gasss23/Gas/pull/341) SOLO DOPO (o insieme a) la PR #339 di M2: senza il server V15 la finestra di 40 s allunga il tempo in cui il parlato della stanza viene inviato e risposto (V-1 MEDIA della verifica esterna). Review #676 APPROVATO CON RISERVE e PR nel perimetro, quindi decide l'operatore tramite M1.

## Esito

- **PR #340 (fetta 42, «Sì, signore?»)**: MERGIATA (83f3bcd) col sì dell'operatore, a CI verde. Bot e verifica esterna: APPROVATO CON RISERVE, nessuna ALTA o MEDIA; le riserve nuove sono registrate in stato_progetto.
- **Fetta 43 parte 2**: FATTA (PR #341).
  - Finestra di conversazione di 40 s.
  - Turni senza parola con tetto di 15 s: al tetto non si invia e si chiude.
  - Header `X-Gas-Seguito`; comandi «fine» e «pausa» del server (V15 di M2); un errore in un turno di seguito chiude in silenzio.
  - Suite ascolto 248 passed; 15 mutanti presi.
  - Review #676 APPROVATO CON RISERVE (R-676-1/2/3 BASSE; la R-676-3 è sul server di M2 ed è girata a M1).
  - Il commit di merge su main ha un diff identico a quello rivisto.

## Merge della #342 e verdetti su bdc79ce

- Su bdc79ce la CI è verde. Bot e verifica esterna danno APPROVATO CON RISERVE, senza ALTA o MEDIA.
- La #342 di M2 (parser del bot) è entrata in main: l'ho unita in 7296f39. Review #693 APPROVATO CON RISERVE: R-693-1 COSMETICA; R-693-2 BASSA, che è la V-1 del bot.
- **Da dire all'operatore (V-1 bot / R-693-2, BASSA).** Se «Hey Jarvis» si sente a metà di una frase detta senza la parola, tutta la frase va come richiesta normale, compreso il parlato di prima (fino a circa 15 s). Va corretto nella fetta successiva tagliando l'audio dalla parola, oppure accettato.

## Bocciatura del bot su 851a0d1 e correzione

- Bot BOCCIATO per V-1 MEDIA: nella finestra «Hey Jarvis, …» partiva come turno di seguito, e il server rispondeva «ripetimelo». Corretta in 1792ab3: il rilevatore resta acceso nella finestra, azzerato prima per R-680-1.
- LEGGIMI corretto: la pausa nel seguito è muta; i 15 s comprendono la pausa finale.
- Review #680 e #681 APPROVATO CON RISERVE (R-680-2 BASSA, R-681-1 COSMETICA). Suite ascolto 254 passed.

## Merge della #339 e sì dell'operatore

- La #339 di M2 è in main (3cde8a5); l'ho unita nella #341 (ac06f01). Review #679 APPROVATO CON RISERVE: il revisore ha provato il contratto con il client e il VoiceHandler veri, 21 casi passati.
  - R-679-1 BASSA: manca nel repo un test d'integrazione V15.
  - R-679-2 BASSA: il LEGGIMI dice che la «pausa» detta senza la parola risponde «Va bene.», ma è muta.
  - R-679-3 COSMETICA: il log non dice che era una pausa.
  - Le chiudo nella fetta 44.
- Sì dell'operatore alla #341 (via M1): la mergio con CI verde, se bot e verifica esterna non hanno ALTA o MEDIA.

## Verdetti su 43fa6ac (PR #341)

- Verifica esterna: APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/341#issuecomment-6672694572).
  - V-1 MEDIA: l'ordine di merge non era dichiarato. Chiusa dichiarandolo: la #341 si mergia dopo la #339.
  - V-2/V-3/V-4: BASSE, registrate.

## Anomalie

- Funziona del tutto solo quando anche la PR #339 di M2 sarà in main.
