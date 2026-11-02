# Piano mail di Gas (R6) — senza codice, da decidere

Chat Mani, 2026-11-02, su richiesta di M1. Pezzo di R6 dopo il web: **leggere, preparare
bozze, inviare solo con firma** (roadmap R6; principio dell'autonomia e regola dei
modelli, capitolo 0). Niente codice finché l'operatore non risponde alle domande in fondo.

## Come funzionerebbe

1. **Leggere** — strumento `fetch_email` (sola lettura): elenca e apre i messaggi di una
   casella. Il testo delle mail è **non fidato**: il nome `fetch_email` sta già tra gli
   strumenti che contaminano la finestra (`UNTRUSTED_INPUT_TOOLS` in
   `modules/gate/gate.py`; la contaminazione guarda il NOME, V-1 bot #324: un nome
   diverso non contaminerebbe). Dopo una lettura
   ogni azione verso l'esterno va alla firma. Il testo arriva al modello dentro una
   cornice «dati, non istruzioni», con un tetto di caratteri. Niente allegati nella
   prima versione: solo nome e dimensione.
2. **Bozze** — strumento `prepara_bozza` (da aggiungere al cancello come UNCERTAIN e
   libero dopo una lettura, con un test: un nome che non c'è è negato): è interna e
   reversibile, quindi **libera**
   anche dopo una lettura (principio del 19 ottobre). La bozza resta in Gas (memoria) e
   l'operatore la vede quando vuole. Proposta: nella prima versione la bozza non va
   nemmeno nella casella, così il token di lettura non scrive niente.
3. **Inviare** — strumento `send_email(bozza)`: **sempre alla firma** su Telegram
   (il nome `send_email` è già IRREVERSIBLE nel cancello). Il messaggio di firma mostra il
   destinatario, l'oggetto e il testo integrale. Si manda solo la bozza firmata, mai un
   testo rigenerato. Un invio per firma.
4. **Credenziali separate** (proposta). Con Gmail i permessi si possono dividere:
   `gmail.readonly` per leggere, `gmail.send` solo per inviare. Il token di invio lo usa
   soltanto l'azione firmata. Attenzione: con IMAP e la password per app la stessa
   credenziale legge **e** invia (SMTP), quindi la separazione la fa solo il codice e non
   la credenziale.
5. **Tetti** (proposta, tutti configurabili, conto su file come le notifiche):
   - 100 messaggi letti al giorno;
   - 20 bozze al giorno;
   - 10 invii al giorno;
   - al massimo 5 destinatari per mail, niente CCN.
   Conto rotto → niente invio.
6. **Regola dei modelli e GDPR**: le mail contengono dati di persone. Gli strumenti mail
   si offrono **solo nei turni sul cervello forte**. Se il forte non c'è, il lavoro
   aspetta in coda e non passa mai ai modelli gratuiti. Nel diario vanno solo conteggi
   (F-diario-eco), mai il testo né gli indirizzi. Il testo letto non si conserva oltre il
   turno, salvo ciò che finisce in un contatto (già marcato «non fidato» dopo una
   lettura). Base giuridica e conservazione dei dati dei contatti: capitolo 6, decisione
   7 della roadmap, ancora aperta.
   **Requisito del kernel (V-1 bot #324):** oggi l'output degli strumenti resta nella
   cronologia (`.gas_history.json`, blocchi role «tool») e `_get_window` lo rimanda ai
   turni dopo, che di default vanno alla cascata gratuita. Quindi la fetta 1 deve anche
   cambiare il kernel: a fine turno l'output di `fetch_email` si toglie o si maschera
   nella storia, oppure una finestra che lo contiene non va mai ai gratuiti. Senza
   questo, testo e indirizzi letti in un turno forte arriverebbero ai gratuiti.
7. **Fail-safe §9**: provider giù, token scaduto o risposta strana → messaggio
   «Operazione negata: …» e il turno va avanti, mai un crash.

## Fette (dopo le risposte)
1. Sola lettura e tetti, con server di posta finto nei test, più il requisito del kernel del punto 6 (output delle mail mai ai gratuiti, nemmeno dalla storia).
2. Bozze in Gas.
3. Invio con firma e token separato.
4. Prova dal vero su una casella di prova, poi su quella vera.

## Domande per l'operatore

1. **Casella e provider**: quale indirizzo (una casella nuova solo per Gas, oppure la
   tua)? Gmail, Google Workspace o un altro provider?
2. **Accesso**:
   - **OAuth** (consigliato con Gmail): permessi separati per leggere e inviare, revocabili
     dall'account Google. Serve un progetto Google Cloud. Con l'app in «test», il token
     scade ogni 7 giorni e va rinnovato a mano: da verificare sulla pagina ufficiale prima
     di costruirlo.
   - **IMAP e SMTP con password per app**: più semplice. Serve la verifica in due passaggi.
     Una credenziale sola legge e invia.
3. **Dove sta la credenziale**: come gli altri token, in `~/.config/gas/` (es.
   `mail_lettura_token` e `mail_invio_token`, permessi 0600), mai nel repo né nel `.env`
   versionato. Va bene? Sul VPS lo stesso percorso.
4. **Cosa senza firma**: solo leggere e preparare bozze? O preferisci che anche la
   lettura chieda il tuo ok, almeno all'inizio?
5. **Tetti**: vanno bene i numeri del punto 5 (100 letti, 20 bozze, 10 invii al giorno,
   5 destinatari)?
6. **Testo delle mail non fidato**: confermi che dopo una lettura ogni azione verso
   l'esterno (mail, notifiche, messaggi) va alla firma, anche se la richiesta l'hai
   fatta tu?
7. **GDPR e regola dei modelli**:
   - confermi «mail solo col cervello forte, altrimenti si aspetta»?
   - per quanto tempo si conservano i dati dei contatti presi dalle mail, e chi li può
     cancellare?
