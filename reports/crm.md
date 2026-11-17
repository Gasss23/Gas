# CRM clienti di Gas — guida e progetto

> Prima bozza: 17 novembre 2026 (fetta 1). Codice in `modules/crm/`, test in `tests/test_unit_crm.py`.

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

I dati veri stanno in `.gas_memory.db` (lo stesso file della memoria di Gas): il backup che c'è già (`gas backup`) copre anche i clienti.

Altri comandi: `scan` (una scansione del motore), `riepilogo`, `spiega ID` (perché il motore propone o no qualcosa a un cliente), `cliente`, `posizione`, `movimento`, `import file.csv` (movimenti da CSV: `telefono;servizio;tipo;importo;data;nota`; se una riga è sbagliata non scrive niente).

## 3. Cosa vedi

- **Plancia**: commissioni del mese, profitto dei clienti, capitale gestito, clienti paganti, servizi per cliente (quanto sono diversificati), opportunità aperte col valore in euro al mese. Grafico degli ultimi 12 mesi, quota dei clienti in ogni servizio, imbuto delle proposte, attività in tempo reale.
- **Clienti × Servizi**: una riga per cliente, una colonna per servizio. Ogni casella vuota è una vendita possibile; quella con «◎ da proporre» ha già il messaggio pronto. Clic su un cliente → la sua scheda: servizi, registro movimenti, proposte, storia, cosa farebbe il motore e perché.
- **Opportunità**: da approvare (testo modificabile, «Approva e apri WhatsApp»), in attesa di risposta («Ha detto sì / no / STOP»), esiti.
- **Servizi**: il catalogo, con commissioni e numeri veri; le regole del motore.

Tutto si aggiorna da solo: se Gas, la riga di comando o un'altra finestra cambiano qualcosa, la dashboard lo vede entro un paio di secondi.

## 4. Come ragiona il motore

Contatta un cliente solo se **tutte** queste cose sono vere:

1. cliente attivo, con il **consenso** ai messaggi promozionali, senza **STOP**, con un numero WhatsApp;
2. ha già pagato almeno **1 commissione** (è contento);
3. nel mese in corso o in quello prima ha fatto almeno **1.000 €** di profitto;
4. non ha già una proposta aperta (una alla volta);
5. dall'ultimo messaggio sono passati almeno **7 giorni** e negli ultimi 30 ne ha ricevuti meno di **4**.

Poi sceglie l'azione:

- se ha detto **no** a un nuovo servizio negli ultimi 30 giorni → **aumento di capitale** sul servizio che gli rende di più (la tua regola: «non vuole un altro servizio? aumenta quello»);
- altrimenti un **nuovo servizio**: quello con la commissione stimata più alta, con un bonus se è un abbinamento frequente («il 60% di chi ha A ha anche B»);
- se ha appena detto sì a qualcosa → prima chiede di **presentare un amico**;
- se non resta altro: aumento di capitale, poi presentazione.

**Insistenza crescente**: ogni no o silenzio degli ultimi 90 giorni alza il livello (1 → 3). Il livello cambia il tono (più diretto, propone una chiamata), mai le regole sopra.

**Stime in euro**: il motore usa il rendimento **osservato** del servizio sugli ultimi 3 mesi chiusi (se non ci sono dati, la stima interna del servizio). Le stime restano interne: ai clienti si citano solo i risultati che hanno già fatto, con la frase «I risultati passati non garantiscono quelli futuri.» e la riga per dire STOP.

## 5. Regole del progetto rispettate

- **Ciò che esce verso il mondo aspetta la firma** (principio del 19 ottobre): il motore trova e scrive da solo, l'invio lo conferma l'operatore («Approva e apri WhatsApp»: si apre WhatsApp col testo già scritto, tu premi invio).
- **Dati dei clienti mai ai modelli gratuiti**: il motore e i messaggi sono a regole fisse, zero modelli, zero token. Nessun dato esce dal computer.
- **I soldi li scrive solo l'operatore** (o un import): un numero inventato da un modello farebbe mentire il CRM.
- **Soldi in centesimi interi**, mai numeri con la virgola mobile; percentuali in punti base.
- **Registro movimenti e storia non si riscrivono** (lo vieta il database): un errore si corregge con «Storna».
- **Sicurezza della dashboard**: solo da questo computer (127.0.0.1), token obbligatorio, sessione in un cookie protetto, blocco dopo 10 tentativi sbagliati, difese contro CSRF e DNS rebinding, nessuno script esterno.
- **Avviso su Telegram** (facoltativo, `GAS_CRM_AVVISI_TELEGRAM=1`): solo numeri («3 nuove opportunità, ~420 €/mese»), mai nomi; al massimo uno all'ora.
- **Dati dei clienti protetti dagli strumenti di Gas**: stanno in `.gas_memory.db`, che il cancello rende illeggibile agli strumenti del modello. Se cambi `GAS_CRM_DB`, usa un nome che inizia con `.gas_memory` (altrimenti il CRM avvisa).
- **Diario del CRM senza nomi**: è immutabile, quindi contiene solo numeri di cliente, importi e servizi; nomi e recapiti stanno solo nell'anagrafica, che si potrà anonimizzare su richiesta dell'interessato (GDPR, da decidere prima dei dati veri). Le note scritte a mano possono contenere dati personali: scrivile pensando che restano.

**Attenzione prima di caricare clienti veri (R-803-4):** il controllo che manda al cervello forte i messaggi con dati di clienti conosce oggi solo i lead della rubrica, non i clienti del CRM. Finché la prossima fetta non lo collega, non scrivere a Gas (chat, voce, Telegram) nomi e guadagni dei clienti: usa la dashboard.

## 6. Impostazioni (file `.env`)

| Variabile | Default | Cosa fa |
|---|---|---|
| `GAS_CRM_TOKEN` | — (obbligatoria) | token di accesso alla dashboard, almeno 16 caratteri |
| `GAS_CRM_PORT` | 8770 | porta della dashboard (oggi va esportata nella shell o passata con `--porta`: dal `.env` non viene ancora letta, riserva R-804-1) |
| `GAS_CRM_DB` | `.gas_memory.db` | file del database |
| `GAS_CRM_SOGLIA_EURO` | 1000 | profitto nel mese che fa scattare una proposta |
| `GAS_CRM_PAGAMENTI_MIN` | 1 | commissioni già pagate prima di proporre altro |
| `GAS_CRM_PAUSA_GIORNI` | 7 | giorni minimi tra due messaggi allo stesso cliente |
| `GAS_CRM_MAX_MESSAGGI_30G` | 4 | messaggi al massimo in 30 giorni |
| `GAS_CRM_PAUSA_DOPO_NO_GIORNI` | 30 | prima di riproporre ciò a cui ha detto no |
| `GAS_CRM_ATTESA_RISPOSTA_GIORNI` | 5 | dopo quanti giorni un messaggio è «senza risposta» |
| `GAS_CRM_AUMENTO_PCT` | 50 | aumento di capitale suggerito, in % del capitale |
| `GAS_CRM_REFERRAL_GIORNI` | 60 | al massimo una richiesta di presentazione ogni… |
| `GAS_CRM_SCAN_MINUTI` | 10 | ogni quanto il motore rilegge tutto (lo fa anche a ogni cambio) |
| `GAS_CRM_NOTA_RISCHIO` | «I risultati passati…» | nota sotto i messaggi; vuota = nessuna nota |
| `GAS_CRM_AVVISI_TELEGRAM` | spento | `1` = avviso all'operatore quando ci sono nuove opportunità |

## 7. Prossime fette (proposta)

1. **Invio automatico su WhatsApp Business** (API ufficiale di Meta): serve un numero business, i modelli di messaggio approvati da Meta (per i messaggi promozionali il testo libero non è ammesso) e la tua decisione sulla firma (vedi §8).
2. **Risposte automatiche**: il «sì / no / STOP» del cliente letto da WhatsApp invece che cliccato a mano.
3. **Gas legge il CRM** (strumento in sola lettura, solo col cervello forte, regola dei modelli): «Gas, chi devo chiamare oggi?» da voce e Telegram. Nella stessa fetta: i nomi dei clienti del CRM entrano nel controllo che manda al cervello forte i messaggi con dati di clienti (R-803-4).
4. **Import automatico dei risultati** dal broker o dalla piattaforma dei servizi, al posto dell'inserimento a mano.
5. **Accesso da telefono** sul server (R5) passando da un tunnel sicuro.

## 8. Decisioni che spettano all'operatore

1. **I 4-5 servizi veri**: nome, come guadagniamo (percentuale sul profitto, percentuale annua sul capitale, fisso mensile), capitale minimo.
2. **Invio senza firma**: oggi ogni messaggio lo approvi tu (principio del 19 ottobre). Per l'invio completamente automatico va cambiata quella regola, e servono l'API WhatsApp Business e i modelli approvati.
3. **Consenso dei clienti**: il motore scrive solo a chi ha il consenso spuntato. Va raccolto davvero (meglio per iscritto) e registrato nella scheda.
4. **Rischi da conoscere** (una riga ciascuno): WhatsApp blocca i numeri che mandano troppi messaggi promozionali non richiesti; la promozione di servizi di investimento in Italia ha regole sue (Consob): conviene una verifica con un consulente prima dell'uso vero.
