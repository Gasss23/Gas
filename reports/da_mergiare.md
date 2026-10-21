# DA MERGIARE — coda della chat Motore

> Decisione dell'operatore (2026-10-21): la chat Motore lavora di fila sulla roadmap; qui si accumula ciò che è pronto, una voce per fetta, con i pro e i contro del merge. L'operatore passa 1-2 volte al giorno, legge questa pagina e scrive «mergia #N» oppure «no». Le voci mergiate si tolgono.

> **Decisione per te (C6, bottone «Modifica» e firme a gruppi):** il 30 settembre avevi deciso «una firma per ogni azione, niente gruppi»; il «Modifica» non ha ancora un disegno. Non lo costruisco finché non dici: (a) lasciamo così, (b) disegnamo il «Modifica» (cosa si può cambiare e come si rifirma), (c) anche le firme a gruppi.

## PR aperta del ramo `feat/merge-automatico-z1xjx2` (nuova, dopo il merge di #233)

### 1. Compiti notturni che riprendono dopo un crash (roadmap R7, missione M3)
- **Cosa:** il giro notturno segna quali compiti ha iniziato; se Gas si spegne a metà (crash, riavvio, corrente), al giro dopo quei compiti ripartono per primi con una nota «controlla cosa è già stato fatto e non ripeterlo». Dopo 3 interruzioni di fila il compito si salta (avviso, exit 1) e il giro dopo riprova da capo; chiesto a mano (`/compito`, `gas notte <nome>`) parte comunque.
- **Pro:** primo pezzo concreto di M3 («un compito lungo interrotto riprende e finisce»); le azioni rischiose restano comunque alla firma.
- **Contro:** si riparte da capo con la nota, non dal punto esatto: azioni libere già fatte (es. aggiungere righe a un file) possono ripetersi se il modello ignora la nota; un catalogo con avvisi fissi non pulisce le voci vecchie (R-408-1, bassa).
- **Controlli:** revisori #406 e #407 (chat Motore) APPROVATO CON RISERVE; notte 118 passed (round-trip col kernel vero sulla ripresa).

### 2. Piccole riserve chiuse
- **Cosa:** un catalogo rotto per un momento non cancella più il registro dei crash; `read_file` nega un nome vuoto o fatto solo di invisibili; il test del giro che falliva 1 volta su 20 è stabile (la causa era l'invio in parallelo della #233).
- **Pro:** chiude R-407-1/2, R-405-1/2, R-404-2; CI più affidabile.
- **Contro:** `read_file` su «.» ora è negato invece di dare «è una cartella» (R-408-2, cosmetica).
- **Controlli:** revisore #408 (chat Motore) APPROVATO CON RISERVE; gate+notte 936 passed, kernel 957 PASS.

### 3. Spesa giornaliera calcolata leggendo solo le righe nuove (roadmap 5.5)
- **Cosa:** il controllo del tetto di spesa (prima di ogni chiamata a pagamento) non rilegge più tutto il registro dei token: legge solo le righe aggiunte. Su 100.000 righe: da ~480 ms a ~12 ms per controllo. Inoltre il registro rovinato (righe non valide, numeri negativi o assurdi) non abbassa più la spesa calcolata; prima una sola riga illeggibile azzerava tutto il conto.
- **Pro:** chiude R-tel-budget-perf; il blocco del budget diventa più affidabile.
- **Contro:** più codice in un punto delicato (il blocco della spesa). Una riscrittura a mano molto particolare del registro non verrebbe vista (limite dichiarato); un numero enorme scritto a mano conta 0 (R-411-2, bassa).
- **Controlli:** revisori #409, #410, #411, #413, #414 (chat Motore) APPROVATO CON RISERVE; sonde del revisore: 2.400 + 18.000 casi uguali alla lettura completa; kernel 964 PASS. Seguito (#413/#414): una riga senza data valida (o con data futura) non tiene più il budget bloccato per sempre; l'ultima riga senza «a capo» si conta; `gas tokens` regge un registro rovinato.

### 4. Ripresa dopo un crash più precisa
- **Cosa:** un compito già finito non viene più ripreso se Gas si spegne durante la riflessione finale; il registro rifiuta numeri strani.
- **Pro:** chiude V-1 del bot e V-4 della verifica esterna su #234.
- **Contro:** nessuno noto.
- **Controlli:** revisore #410 (chat Motore) APPROVATO CON RISERVE; notte 122 passed.

### 5. Tetto alle parole delle ricerche nella memoria (roadmap R7, R-fts-1)
- **Cosa:** quando Gas cerca nel diario o nella conoscenza, usa al massimo 12 parole distinte (ognuna di al massimo 40 caratteri).
- **Pro:** una domanda enorme del modello non diventa una ricerca enorme; chiude R-fts-1.
- **Contro:** in una domanda molto lunga le parole oltre la dodicesima non contano, anche se sono quelle importanti (R-412-1, bassa).
- **Controlli:** revisore #412 (chat Motore) APPROVATO CON RISERVE, review solo letta (disco temporaneo pieno in quel momento); kernel 962 PASS rieseguito.
