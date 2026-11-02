# Piano mail di Gas (R6) — senza codice, da decidere

Chat Mani, 2026-11-02, su richiesta di M1. Pezzo di R6 dopo il web: **leggere, preparare
bozze, inviare solo con firma** (roadmap R6; principio dell'autonomia e regola dei
modelli, capitolo 0). Niente codice finché l'operatore non risponde alle domande in fondo.

## Come funzionerebbe

1. **Leggere** — strumento `fetch_email` (sola lettura): elenca e apre i messaggi di una
   casella. Il testo delle mail è **non fidato**: il nome `fetch_email` sta già tra gli
   strumenti che contaminano la finestra (`UNTRUSTED_INPUT_TOOLS` in
   `modules/gate/gate.py`; la contaminazione guarda il NOME, V-1 bot #324: un nome
   diverso non contaminerebbe). Non è però ancora in `GATE_ALLOWLIST`, quindi oggi è
   negato: la fetta 1 lo aggiunge (SAFE come `read_file`), con un test. Dopo una lettura
   ogni azione verso l'esterno UNCERTAIN o IRREVERSIBLE va alla firma. Attenzione: nel
   cancello `notify_telegram` è SAFE (un segnaposto che nessuno strumento usa): la fetta 1
   lo mette a UNCERTAIN o lo toglie, così dopo una lettura nessuna notifica parte senza
   firma (V-2 bot #324). Il testo arriva al modello dentro una
   cornice «dati, non istruzioni», con un tetto di caratteri. Niente allegati nella
   prima versione: solo nome e dimensione.
2. **Bozze** — strumento `prepara_bozza` (da aggiungere al cancello come UNCERTAIN e in
   `_LIBERI_DOPO_LETTURA`, se no a finestra contaminata andrebbe alla firma, con un
   test: un nome che non c'è è negato): è interna e
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
   (F-diario-eco), mai il testo né gli indirizzi. Il testo letto dovrà non conservarsi oltre il
   turno (vedi la proposta qui sotto: il turno mail si toglie o si maschera dalla storia); i contatti presi dalle mail seguono la regola della memoria qui sotto (la
   marcatura «non fidato» decide la firma, non il provider). Base giuridica e conservazione dei dati dei contatti: capitolo 6, decisione
   7 della roadmap, ancora aperta.
   **Requisito del kernel (V-1 bot #324, due giri):** oggi la cronologia
   (`.gas_history.json`) tiene TUTTO il turno, non solo l'output degli strumenti: i
   blocchi role «tool» di `fetch_email`, ma anche le risposte dell'assistente che
   riassumono la mail e gli argomenti delle chiamate `prepara_bozza`/`send_email`
   (destinatari e testo). `_get_window` rimanda tutto ai turni dopo, che di default vanno
   alla cascata gratuita. Quindi la fetta 1 deve cambiare il kernel. **Proposta: il
   turno mail si maschera in OGNI salvataggio della storia** (`_save_history` gira
   anche a metà turno, dopo ogni gruppo di strumenti, e un turno interrotto non arriva
   mai alla fine), così il testo non arriva mai in `.gas_history.json`; e **gli snapshot
   `refs/gas/snapshots/` fatti con un turno mail nella finestra escludono o mascherano
   `.gas_history.json`** (oggi `_snapshot` lo aggiunge sempre prima di `write_file` e
   `run_command`). Gli snapshot restano finché sono tra gli ultimi 100 o hanno meno di 7
   giorni, e gli oggetti restano fino a un `git gc`, che non parte mai da solo (V-1 bot
   #324 su 7346994 e su a48caa0). In più, finché il turno è in corso, **una finestra
   che contiene strumenti mail non va mai ai gratuiti** (aspetta il forte). Se invece
   l'operatore preferisce tenere il turno nella storia, la conservazione (storia e
   snapshot, con quei tempi) va dichiarata nella domanda 7 (V-2 bot #324 su d783938). Lo stesso vale
   per le bozze salvate in Gas: si leggono solo nei turni sul forte. Senza questo, testo
   e indirizzi letti in un turno forte arriverebbero ai gratuiti.
   I percorsi da coprire sono cinque (R-626-1, V-1 bot #324 su 970beca e su d783938):
   - i turni dopo (`run_turn` con `_get_window`);
   - la riflessione di fine task (cascata «complesso» su una finestra di `_get_window`);
   - il riepilogo di compressione, dove il testo degli strumenti diventa un messaggio user
     e il nome dello strumento sparisce: il segno «turno mail» deve sopravvivere;
   - **la memoria**: `_memoria_pin` mette nome e prossima azione dei contatti attivi nel
     messaggio system di OGNI turno (anche sui gratuiti) e `ricorda` li rende leggibili.
     Un contatto o una riga di diario nati da un turno mail vanno segnati con l'origine
     «mail» ed esclusi dal pin e da `ricorda` fuori dal forte. Finché questo non c'è (e
     finché la decisione 7 della roadmap sul GDPR non è presa), dalle mail **non si
     salvano contatti**;
   - **i file**: `write_file` sta in `_LIBERI_DOPO_LETTURA`, quindi a finestra contaminata
     scrive senza firma i .md/.txt/.csv nelle cartelle di lavoro, e `read_file` (SAFE) li
     rilegge in un turno dopo sui gratuiti. Proposta: con `fetch_email` nella finestra,
     `write_file` esce da `_LIBERI_DOPO_LETTURA` e va alla firma (oppure i file scritti
     in un turno mail si segnano e non si leggono fuori dal forte), con un test.
7. **Fail-safe §9**: provider giù, token scaduto o risposta strana → messaggio
   «Operazione negata: …» e il turno va avanti, mai un crash.

## Fette (dopo le risposte)
1. Sola lettura e tetti (`fetch_email` in `GATE_ALLOWLIST` con un test), con server di posta finto nei test, più il requisito del kernel del punto 6 (un turno con strumenti mail mai ai gratuiti, per nessuno dei cinque percorsi: storia, riflessione, compressione, memoria, file scritti con `write_file`; turno mail mascherato in ogni salvataggio della storia, anche a metà turno, e `.gas_history.json` escluso o mascherato negli snapshot fatti con un turno mail nella finestra, con un test per ciascuno) e `notify_telegram` non più SAFE (aggiornando `test_notify_telegram_safe` in `tests/test_unit_gate.py`, V-2 bot #324 su 7346994).
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
   - va bene la proposta del punto 6 (testo delle mail mai salvato nella storia né negli
     snapshot)? Se no, la storia lo terrebbe, e gli snapshot fino agli ultimi 100 o 7
     giorni, più fino a un `git gc` manuale.
