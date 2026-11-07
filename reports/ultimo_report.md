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

## Sì dell'operatore e merge della #345

- 2026-11-07, tramite M1: l'operatore dice sì alla #341 e ACCETTA il rischio di privacy R-694-1/R-695-2: un falso «Hey Jarvis» nella finestra fa passare circa 2 s di parlato della stanza senza il filtro. Questo chiude la V-2 MEDIA della verifica esterna su a269c12.
- Su a269c12: CI verde; bot APPROVATO CON RISERVE con 2 BASSE nuove (GAS_VOICE_FINESTRA condivisa col browser_server; turni con la parola contati in max_turni), da chiudere nella fetta 44.
- Merge rifiutato per conflitti con la PR #345 di M2 (fetta 3 sottofondo). Ho unito main (769f91c): conflitti solo nei report e nella memoria. Review #701 APPROVATO; 398 test della voce e del sottofondo passati.

## Giro su 7e4a7d3 e merge della #344

- 7e4a7d3: CI verde; bot e verifica esterna APPROVATO CON RISERVE, nessuna ALTA o MEDIA. Riserve nuove: bot V-1 BASSA (tetto di seguito e pausa finale), V-2 COSMETICA (bip nel LEGGIMI); registrate in stato_progetto.
- Il merge su GitHub è stato rifiutato per conflitti con la PR #344 di M2 (fix di claude-cli), arrivata in main poco prima. Ho unito main (b874179): conflitti solo nei report e nella memoria del revisore. Review #697 APPROVATO; 316 test passed (claude_cli + ascolto).
- Da far accettare all'operatore: il rischio di privacy R-694-1/R-695-2 (falso «Hey Jarvis» nella finestra).

## Verifica esterna su 562f137 e merge della #343

- La verifica esterna (BASSE) ha riprodotto un caso che il bot avrebbe alzato a MEDIA: una parola sentita molto prima della voce. Corretto in 165a9a4: la parola scade dopo 2 s. Review #695 APPROVATO CON RISERVE (R-695-1/2 BASSE).
- La #343 di M2 (voce rapida) è entrata in main: l'ho unita in 8c31f6e. Review #696 APPROVATO CON RISERVE, con il client provato contro il server (R-696-1/2 BASSE, per M2).
- Suite ascolto: 257 passed.

## Bot su 23d9c1c: R-693-2 alzata a MEDIA e corretta

- Il bot ha alzato a MEDIA la parola a metà del seguito. Corretta in 01b1089: si tengono solo gli ultimi 1,5 s prima della parola e il dopo.
- Review #694 APPROVATO CON RISERVE. Riserve BASSE: R-694-1 (residuo da far accettare all'operatore) e R-694-2 (da provare sul Mac).
- Suite ascolto: 255 passed.

## Merge della #342 e verdetti su bdc79ce

- Su bdc79ce la CI è verde. Bot e verifica esterna danno APPROVATO CON RISERVE, senza ALTA o MEDIA.
- La #342 di M2 (parser del bot) è entrata in main: l'ho unita in 7296f39. Review #693 APPROVATO CON RISERVE: R-693-1 COSMETICA; R-693-2 BASSA, che è la V-1 del bot.
- (Superato: corretto in 01b1089, vedi sopra.) **Era da dire all'operatore (V-1 bot / R-693-2).** Se «Hey Jarvis» si sente a metà di una frase detta senza la parola, tutta la frase va come richiesta normale, compreso il parlato di prima (fino a circa 15 s). Va corretto nella fetta successiva tagliando l'audio dalla parola, oppure accettato.

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
