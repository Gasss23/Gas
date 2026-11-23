# CRM clienti di Gas — guida e progetto

> Prima bozza: 17 novembre 2026 (fetta 1); secondo giro lo stesso giorno, dopo le risposte dell'operatore.
> Codice in `modules/crm/`, test in `tests/test_unit_crm.py`.
> Cartella del progetto: questa guida, le decisioni dell'operatore (`decisioni.md`) e le domande aperte (`domande.md`).

## 1. A cosa serve

Un elenco ordinato di tutti i clienti, in quali servizi sono, quanto capitale hanno, quanto guadagnano e quanto ci hanno pagato. Sopra c'è un **motore che legge i dati da solo** e trova a chi proporre cosa: un servizio in più, un aumento di capitale, oppure di presentarci un amico. Il messaggio WhatsApp lo scrive lui; tu lo approvi con un click.

## 2. Come si avvia

**Demo (dati inventati, numeri di telefono non assegnabili):**

```bash
python -m modules.crm serve --demo
```

Stampa un link di accesso già pronto. Apri il link nel browser.

**Con i dati veri:**

1. Nel file delle chiavi `.env` aggiungi `GAS_CRM_TOKEN=` seguito da almeno 16 caratteri casuali (il CRM senza token non parte).
2. Inserisci i servizi veri (dalla scheda **Servizi** della dashboard, oppure `python -m modules.crm servizio --codice … --nome … --modello …`).
3. `python -m modules.crm serve` e apri `http://127.0.0.1:8770/`, poi incolla il token.

I dati veri stanno in un file SOLO del CRM, `.gas_memory_crm.db`, separato dalla memoria di Gas (decisione dell'operatore). Il nome che inizia con `.gas_memory` lo rende illeggibile agli strumenti del modello. Copie di sicurezza: il server ne fa una all'avvio e una al giorno in `.gas_memory_crm_backup/` (tiene le ultime 30); a mano con `python -m modules.crm backup`.

**Copia fuori dal Mac (iCloud Drive, decisione del 19 novembre).** Se il Mac si rompe o si perde, il gestionale non va perso:
1. Nel file delle chiavi `.env` aggiungi `GAS_CRM_BACKUP_PASSWORD=` seguito da una password di almeno 12 caratteri. **Salvala anche nel tuo gestore di password**: senza di lei le copie non si aprono.
2. Fatto: ogni giorno il CRM mette una copia CIFRATA nella cartella «Gas CRM (copie cifrate)» di iCloud Drive: una per giorno (se riavvii il CRM, quella del giorno si rinnova), tiene gli ultimi 30 giorni. All'avvio il server fa una prova vera di scrittura (al massimo qualche secondo) e dice se la copia è ATTIVA, SPENTA o se NON FUNZIONA (per esempio macOS che nega l'accesso a iCloud Drive, o un disco esterno non collegato). In alto nella dashboard c'è sempre l'esito dell'ultima copia: «☁ copia OK», «☁ copia spenta» o, in rosso, «☁ copia NON riuscita»; se gli avvisi Telegram sono accesi arriva anche un messaggio. Senza password non esce niente: mai copie in chiaro.
3. Per ripristinare (anche su un Mac nuovo): `python -m modules.crm ripristina "<percorso del file .gascrm>"`. Chiede la password e rimette il database; non sovrascrive mai un database che c'è già. Se nel frattempo hai cambiato password, alla prima risposta «password sbagliata» puoi scrivere quella vecchia. Se il file su iCloud non è scaricato sul Mac (icona della nuvola nel Finder), aprilo prima dal Finder. Se un ripristino si interrompe (Mac spento a metà), accanto al database può restare un file `….ripristino.tmp` con i dati in chiaro: di solito lo toglie il ripristino successivo nello stesso posto (o, passata un'ora, qualunque ripristino lì). Se dopo il ripristino il file c'è ancora, o se hai ripristinato altrove, cancellalo a mano.
Serve la libreria `cryptography` (`pip install -r requirements.txt`, una volta).

**Come scrivere gli importi** (in dashboard, riga di comando e CSV): stile italiano. «1.500» è millecinquecento euro (il punto separa le migliaia), «1.500,50» ha i centesimi dopo la virgola, «0,50» sono cinquanta centesimi. Un numero ambiguo («1,234», «0.500») viene rifiutato invece di essere indovinato. Il registro non si riscrive, quindi rifiuta anche i movimenti incoerenti: prelievi più grandi del capitale, movimenti con data precedente all'apertura del servizio.

Altri comandi: `scan` (una scansione del motore), `riepilogo`, `spiega ID` (perché il motore propone o no qualcosa a un cliente), `cliente`, `posizione`, `movimento`, `apertura` (anticipa la data di apertura di un servizio per caricare lo storico), `backup`, `import file.csv` (movimenti da CSV: `telefono;servizio;tipo;importo;data;nota`; se una riga è sbagliata non scrive niente; un file già importato viene fermato, salvo `--forza`).

## 3. Cosa vedi

- **Plancia**: commissioni del mese, profitto dei clienti, capitale gestito, clienti paganti, servizi per cliente (quanto sono diversificati), opportunità aperte col valore in euro al mese. Grafico degli ultimi 12 mesi, quota dei clienti in ogni servizio, imbuto delle proposte, attività in tempo reale.
- **Clienti × Servizi**: una riga per cliente, una colonna per servizio. Con le **spunte** scegli tutti, nessuno o alcuni clienti e premi «✉ Prepara messaggio»: il motore scrive un messaggio per ognuno (le regole dure valgono anche qui: consenso, STOP, un messaggio al mese, una proposta alla volta; chi viene saltato compare col motivo). Ogni casella vuota è una vendita possibile; quella con «◎ da proporre» ha già il messaggio pronto. Clic su un cliente → la sua scheda: servizi, registro movimenti, proposte, storia, cosa farebbe il motore e perché.
- **Opportunità**: da approvare (testo modificabile, «✨ Riscrivi con Opus», «Approva e apri WhatsApp», «Scarta»: il motore lascia stare quel cliente per la pausa minima e non ripropone la stessa cosa per 30 giorni), in attesa di risposta («Ha detto sì / no / STOP»), esiti.
- **Servizi**: il catalogo, con commissioni e numeri veri; le regole del motore.

Tutto si aggiorna da solo: se Gas, la riga di comando o un'altra finestra cambiano qualcosa, la dashboard lo vede entro un paio di secondi.

## 4. Come ragiona il motore

Contatta un cliente solo se **tutte** queste cose sono vere (decisioni del 17 novembre: un follow-up al mese, mai dopo una perdita, mai a chi è appena entrato):

1. cliente attivo, con il **consenso** ai messaggi promozionali, senza **STOP**, con un numero WhatsApp;
2. **follow-up mensile acceso** nella sua scheda (si spegne cliente per cliente);
3. cliente da almeno **30 giorni** e ha già pagato almeno **1 commissione** (è contento);
4. nel mese in corso o in quello prima ha fatto almeno **1.000 €** di profitto, e il mese in corso **non è in perdita**;
5. non ha già una proposta aperta (una alla volta);
6. dall'ultimo messaggio sono passati almeno **30 giorni** (al massimo **1** messaggio in 30 giorni).

Se un servizio è segnato **«da consigliare»** (es. la sala segnali o il copyflip), il motore propone solo quelli.

Poi sceglie l'azione:

- se ha detto **no** a un nuovo servizio negli ultimi 30 giorni → **aumento di capitale** sul servizio che gli rende di più (la tua regola: «non vuole un altro servizio? aumenta quello»);
- altrimenti un **nuovo servizio**: quello con la commissione stimata più alta, con un bonus se è un abbinamento frequente («il 60% di chi ha A ha anche B»);
- se ha appena detto sì a qualcosa → prima chiede di **presentare un amico**;
- se non resta altro: aumento di capitale, poi presentazione.

**Insistenza crescente**: ogni no o silenzio degli ultimi 90 giorni alza il livello (1 → 3). Il livello cambia il tono (più diretto, propone una chiamata), mai le regole sopra.

**Stime in euro**: il motore usa il rendimento **osservato** del servizio sugli ultimi 3 mesi chiusi (se non ci sono dati, la stima interna del servizio). Le stime restano interne: ai clienti si citano solo i risultati che hanno già fatto, con la frase «I risultati passati non garantiscono quelli futuri.» e la riga per dire STOP.

## 5. Regole del progetto rispettate

- **Ciò che esce verso il mondo aspetta la firma** (principio del 19 ottobre; l'operatore il 17 novembre: «da sole, ma all'inizio col mio controllo»): il motore trova e scrive da solo, l'invio lo conferma l'operatore («Approva e apri WhatsApp»: si apre WhatsApp col testo già scritto, tu premi invio).
- **Invio a scaglioni** per non farsi bloccare da WhatsApp: al massimo 10 invii ogni 60 minuti (`GAS_CRM_INVII_PER_LOTTO`, `GAS_CRM_LOTTO_MINUTI`); oltre, il pulsante si ferma e dice tra quanto riparte.
- **Dati dei clienti mai ai modelli gratuiti**: il motore e i testi standard sono a regole fisse, zero modelli. La riscrittura «✨ Riscrivi con Opus» usa SOLO Claude Opus col cervello forte (`GAS_CLAUDE_CLI` acceso, `GAS_CRM_MODELLO`, default Opus); se Claude non c'è resta il testo standard, mai un altro modello. A Claude vanno solo nome di battesimo, servizi, risultato del mese se positivo e la bozza: mai telefono, email, cognome, note. Al massimo 60 **tentativi** di riscrittura al giorno (`GAS_CRM_OPUS_GIORNO`; contano anche quelli falliti o scartati). Ogni riscrittura entra nello **stesso conto di spesa del cervello forte di Gas** (`GAS_CLAUDE_CLI_TETTO_USD`): a tetto raggiunto il CRM non riscrive più fino a domani, come Gas.
- **Gas riconosce i clienti del CRM**: se in chat, a voce o su Telegram nomini un cliente (nome, telefono, email), quel messaggio va SOLO al cervello forte, mai ai gratuiti (riserva R-803-4 chiusa il 17 novembre). Se il file dei clienti non si legge, tutto va al forte (si chiude, non si apre). Gas legge il file sia nella cartella da cui è avviato sia nella cartella del repo, così non lo perde se lo avvii da un'altra cartella; se usi `GAS_CRM_DB`, mettila nel file delle chiavi (`.env`), non solo nella shell del CRM, altrimenti Gas non la vede. Il controllo è veloce anche con migliaia di clienti (circa 2 ms a messaggio).
  - **Falsi allarmi (voluti)**: un cognome che è anche una parola comune («Conti», «Costa», «Leone») o una parola di un'email («trading», «esempio») fa trattare il messaggio come se nominasse un cliente: va al forte anche «fammi i conti del mese». È il verso sicuro; col forte spento quei messaggi si fermano con un avviso.
  - **Dopo un crash del CRM a metà salvataggio** Gas ripara il file da sé alla lettura successiva (lo fa SQLite, annullando il salvataggio a metà).
- **I soldi li scrive solo l'operatore** (o un import): un numero inventato da un modello farebbe mentire il CRM.
- **Soldi in centesimi interi**, mai numeri con la virgola mobile; percentuali in punti base.
- **Registro movimenti e storia non si riscrivono** (lo vieta il database): un errore si corregge con «Storna».
- **Sicurezza della dashboard**: solo da questo computer (127.0.0.1), token obbligatorio, sessione in un cookie protetto, blocco dopo 10 tentativi sbagliati, difese contro CSRF e DNS rebinding, nessuno script esterno.
- **Avviso su Telegram** (facoltativo, `GAS_CRM_AVVISI_TELEGRAM=1`): solo numeri («3 nuove opportunità, ~420 €/mese»), mai nomi; al massimo uno all'ora.
- **Dati dei clienti protetti dagli strumenti di Gas**: stanno in `.gas_memory_crm.db`, che il cancello rende illeggibile agli strumenti del modello. Se cambi `GAS_CRM_DB`, usa un nome che inizia con `.gas_memory` (altrimenti il CRM avvisa).
- **Diario del CRM senza nomi**: è immutabile, quindi contiene solo numeri di cliente, importi e servizi; nomi e recapiti stanno solo nell'anagrafica, che si potrà anonimizzare su richiesta dell'interessato (GDPR, da decidere prima dei dati veri). Le note scritte a mano possono contenere dati personali: scrivile pensando che restano.
- **Copie di sicurezza**: una al giorno in `.gas_memory_crm_backup/` (le ultime 30, fuori da git) e, con la password, una al giorno CIFRATA su iCloud Drive (ultimi 30 giorni). Contengono i dati completi dei clienti. Le copie fatte da qui in avanti sono leggibili solo dal tuo utente del Mac (il database di lavoro e le copie locali più vecchie hanno i permessi normali dei file: su un Mac con un solo utente pesa poco): un'eventuale cancellazione su richiesta di un cliente (GDPR) deve valere anche per loro. Le copie si possono cancellare a mano (cartella `.gas_memory_crm_backup/` e cartella «Gas CRM (copie cifrate)» di iCloud Drive) oppure lasciar scadere: si tengono le ultime 30 copie e le più vecchie si cancellano quando ne arrivano di nuove, quindi se il CRM resta spento restano lì finché non le cancelli tu.
- **Scelta a mano**: le regole dure (consenso, STOP, una proposta alla volta, un messaggio al mese) valgono sempre; quelle morbide no, ma la proposta lo scrive in testa al motivo («⚠ ATTENZIONE: cliente da soli 10 giorni, follow-up spento…»), così lo vedi prima di approvare.
- **Parole vietate nei testi di Opus** (promesse di guadagno come «garantito», «ti assicuro», «al sicuro», «senza alcun rischio»; urgenza finta come «ultima occasione», «posti limitati»; perdite): il testo che le contiene viene scartato, anche se scritte con spazi o caratteri strani. È una rete, non la tutela: la tutela vera è la tua approvazione su ogni messaggio.
- **Testi neutri** (cliente scelto a mano senza un risultato da citare): niente numeri e niente nota sul rischio; se lo mandi così com'è parte identico. Se lo modifichi, il sistema aggiunge la nota e la riga STOP come per ogni testo scritto a mano.

**Modello per i clienti (decisione del 18 novembre):** quando in chat, a voce o su Telegram la conversazione contiene dati di un cliente, Gas risponde SOLO con Claude Opus (`GAS_MODEL_CLAUDE_CLIENTI`, default Opus), anche nei turni `/forte` e quando i dati arrivano a metà turno; se il modello configurato non è Opus si ferma e lo dice. Le altre conversazioni restano col modello forte normale (`GAS_MODEL_CLAUDE_FORTE`, oggi Sonnet), che riceve la memoria di Gas senza nomi dei lead: i dati dei clienti li vede solo Opus. Opus consuma di più del tetto giornaliero del forte.

**Usare il CRM parlando con Gas (decisione 18 del 23 novembre)**: su Telegram o a voce puoi dire a Gas, per esempio, «quanti clienti ho?», «com'è messo Mario Rossi?», «Mario Rossi ha versato 1.500 euro», «aggiungi il cliente Anna Neri, 333 1234567», «togli Luca Verdi», «ricordami domani alle 10 di chiamare Anna».
- **Leggere**: Gas legge il CRM da solo (strumento `crm_consulta`), sempre e solo con Claude Opus.
- **Sempre Opus (decisione 19, dal 23 novembre)**: tutto quello che scrivi o dici a Gas lo legge solo Claude Opus (`GAS_SOLO_OPUS`, acceso di default). Se Opus non c'è (cervello forte spento o tetto del giorno finito), Gas non risponde e lo dice. A voce l'audio passa comunque da Groq (trascrizione) e la risposta da ElevenLabs (voce): per i dati dei clienti è più riservato scrivere su Telegram. Il filtro qui sotto vale solo se scrivi `GAS_SOLO_OPUS=0` nel `.env`.
- **Solo Opus col filtro per parole (solo con `GAS_SOLO_OPUS=0`)**: un messaggio con le parole del CRM (cliente, promemoria, ricordami, deposito, prelievo, versato, versamento, bonifico, commissione…), un numero di telefono (italiano, che inizia con 0 o 3, oppure col «+»; anche con spazi, punti, trattini o barre) o il nome di un cliente già nel CRM va solo a Opus fin dall'inizio. Non contano le date, i numeri con le migliaia, l'inglese «client» né «versatile». Limiti: alcuni modi di scrivere il telefono non vengono riconosciuti («333.123.4567», «02 12 34 56 78», «tel.3331234567» col punto attaccato, «(333) 1234567»): scrivilo come «333 1234567» o metti la parola «cliente». Al contrario, un numero lungo che inizia con 0 o 3 (per esempio «3000000 visualizzazioni») o un «+» davanti a un numero con le migliaia («+1.500.000») viene trattato come un telefono e va a Opus. Col cervello forte spento i messaggi che vanno a Opus si fermano con un avviso (anche il messaggio dopo, finché resta nella conversazione recente). Per un cliente NUOVO usa la parola «cliente» («aggiungi il cliente Anna Neri»): senza («aggiungi Anna Neri», «Rossi ha tolto 500», «segna Bianchi come perso», un'email da sola, «metti 2000 euro a Giulia», se quei nomi non sono già nel CRM), il messaggio lo legge prima il modello normale, che non può leggere né cambiare il CRM; se prova a usarlo, il turno passa a Opus.
- **A voce**: la voce passa da Groq (trascrizione) e la risposta da ElevenLabs (sintesi), come ogni comando a voce: se non vuoi che i dati dei clienti passino da lì, usa Telegram scritto.
- **Scrivere**: ogni modifica (`crm_modifica`) arriva prima su Telegram come richiesta di firma, che dice per esteso cosa cambierà («Registra per «Mario Rossi» (cliente #3), servizio «Copy Oro»: DEPOSITO di 1.500,00 € in data …»). Si scrive solo se premi Approva. Se Gas ha trovato il cliente per somiglianza (hai scritto «Ross» e c'è «Mario Rossi»), la firma lo dice con «ATTENZIONE».
- **Soldi**: Gas usa solo cifre che hai scritto o detto TU in quel messaggio, in numeri («1.500», «1500,50», «5 mila»). Se la cifra manca, o l'ha presa da altrove, la richiesta non parte e Gas te la chiede. Date, ore e numeri come «#12» non contano come cifre.
- **Niente cancellazioni**: «togli» o «elimina» un cliente vuol dire archiviarlo (stato «perso»); lo storico resta.
- **Promemoria**: arrivano su Telegram all'ora scelta (controllo una volta al minuto, quindi anche con un minuto di ritardo). Di norma arrivano una volta sola; due casi limite rari: se Gas si spegne proprio mentre manda il promemoria, quel promemoria si perde; se Telegram risponde tardi ma il messaggio è arrivato lo stesso, può arrivare due volte.
- **Dove restano i dati**: la conversazione con Gas sui clienti resta nella storia di Gas (`.gas_history.json`) e le richieste di firma nella sua memoria (`.gas_memory.db`), come ogni conversazione; i messaggi passano da Telegram come la chat di oggi. Nel diario di Gas non vanno nomi né cifre dei clienti.
- **Non dai compiti in sottofondo**: le modifiche del CRM si chiedono in chat, non da un compito in sottofondo. Anche i compiti della notte, per il CRM, si fermano a una richiesta di firma: senza il tuo Approva non si scrive niente.

## 6. Impostazioni (file `.env`)

| Variabile | Default | Cosa fa |
|---|---|---|
| `GAS_CRM_TOKEN` | — (obbligatoria) | token di accesso alla dashboard, almeno 16 caratteri |
| `GAS_CRM_PORT` | 8770 | porta della dashboard |
| `GAS_CRM_DB` | `.gas_memory_crm.db` | file del database (usa un nome che inizia con `.gas_memory`) |
| `GAS_CRM_SOGLIA_EURO` | 1000 | profitto nel mese che fa scattare una proposta |
| `GAS_CRM_PAGAMENTI_MIN` | 1 | commissioni già pagate prima di proporre altro |
| `GAS_CRM_PAUSA_GIORNI` | 30 | giorni minimi tra due messaggi allo stesso cliente |
| `GAS_CRM_MAX_MESSAGGI_30G` | 1 | messaggi al massimo in 30 giorni |
| `GAS_CRM_ANZIANITA_GIORNI` | 30 | da quanti giorni deve essere cliente prima della prima proposta |
| `GAS_CRM_INVII_PER_LOTTO` | 10 | invii al massimo per scaglione… |
| `GAS_CRM_LOTTO_MINUTI` | 60 | …in questi minuti (anti-blocco WhatsApp) |
| `GAS_CRM_MODELLO` | `claude-opus-5-5` | modello per riscrivere i testi (deve essere Opus) |
| `GAS_SOLO_OPUS` | acceso | tutto quello che scrivi o dici a Gas lo legge solo Opus (decisione 19); `0` per tornare al filtro per parole |
| `GAS_MODEL_CLAUDE_CLIENTI` | `claude-opus-5-5` | il modello Opus usato per i dati dei clienti e, con `GAS_SOLO_OPUS` acceso, per ogni turno (deve essere Opus) |
| `GAS_CRM_OPUS_GIORNO` | 60 | riscritture con Opus al massimo al giorno |
| `GAS_CRM_PAUSA_DOPO_NO_GIORNI` | 30 | prima di riproporre ciò a cui ha detto no |
| `GAS_CRM_ATTESA_RISPOSTA_GIORNI` | 5 | dopo quanti giorni un messaggio è «senza risposta» |
| `GAS_CRM_AUMENTO_PCT` | 50 | aumento di capitale suggerito, in % del capitale |
| `GAS_CRM_REFERRAL_GIORNI` | 60 | al massimo una richiesta di presentazione ogni… |
| `GAS_CRM_SCAN_MINUTI` | 720 | ogni quanto il motore rilegge tutto da solo (2 volte al giorno; lo fa anche a ogni cambio e col pulsante «Scansiona»; zero token) |
| `GAS_CRM_BACKUP_PASSWORD` | — | password delle copie cifrate fuori dal Mac (almeno 12 caratteri); senza, la copia esterna è spenta |
| `GAS_CRM_BACKUP_CIFRATO_DIR` | iCloud Drive | dove mettere le copie cifrate, se non iCloud Drive: percorso completo, che inizia con `/` o `~/` |
| `GAS_CRM_NOTA_RISCHIO` | «I risultati passati…» | nota sotto i messaggi; vuota = nessuna nota |
| `GAS_CRM_AVVISI_TELEGRAM` | spento | `1` = avviso all'operatore quando ci sono nuove opportunità |

## 7. Prossime fette (proposta)

1. **Invio automatico su WhatsApp Business** (piattaforma ufficiale di Meta, «Cloud API»): serve l'accesso API del numero business e i modelli di messaggio approvati da Meta (per i messaggi promozionali il testo libero non è ammesso). All'inizio con la firma dell'operatore su ogni invio (decisione del 17 novembre).
2. **Risposte automatiche**: il «sì / no / STOP» del cliente letto da WhatsApp invece che cliccato a mano.
3. ~~**Gas legge il CRM**~~: fatto il 23 novembre, anche con le modifiche firmate e i promemoria (vedi sopra).
4. **Import automatico dei risultati** dal broker o dalla piattaforma dei servizi, al posto dell'inserimento a mano.
5. **Accesso da telefono** sul server (R5) passando da un tunnel sicuro.

## 8. Decisioni e domande

Le decisioni prese sono in `reports/crm/decisioni.md`; le domande ancora aperte in `reports/crm/domande.md`.
