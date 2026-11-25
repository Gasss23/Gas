# CRM — decisioni dell'operatore

> Fonte unica delle scelte sul CRM. Ogni voce: data, decisione, cosa cambia nel codice.
> Guida d'uso: `reports/crm/guida.md`. Domande ancora aperte: `reports/crm/domande.md`.

## 17 novembre 2026 — richiesta iniziale

- Un CRM con l'elenco ordinato dei clienti, i servizi in cui sono, quanto hanno guadagnato.
- Obiettivo: monetizzare e diversificare lo stesso cliente su più servizi (o, se non vuole un altro servizio, aumentare il capitale di quello che ha).
- Il CRM «legge se stesso»: trova da solo chi contattare e prepara il messaggio.
- Si propone solo a chi ha già fatto i primi pagamenti (è contento).
- Stile: intuitivo, molto bello, futuristico («tipo Jarvis»: approvato dall'operatore dopo la prima bozza).

## 17 novembre 2026 — risposte dopo la prima bozza

1. **Messaggi a singoli clienti**, con spunte per scegliere tutti, alcuni o nessuno. → selezione nella scheda Clienti e invio controllato.
2. **Niente raffiche**: un solo follow-up al mese per cliente, con un messaggio convincente e ben studiato, di solito dopo un profitto. Il follow-up si può togliere cliente per cliente. I servizi da consigliare saranno uno o due dedicati (probabilmente una «sala segnali» o un «copyflip»). → tetto di 1 messaggio ogni 30 giorni, interruttore «follow-up mensile» nella scheda cliente, servizi segnati «da consigliare».
3. **Nessun avviso ai clienti per drawdown o perdite**: creerebbe ansia inutile; le perdite sono normali nel trading. → il CRM non manda mai messaggi legati alle perdite; le proposte partono solo dopo un profitto.
4. **WhatsApp Business**: l'operatore ce l'ha. → invio a scaglioni per non farsi bloccare; l'invio automatico vero richiede l'API di WhatsApp Business (vedi domande).
5. **File dedicati dentro Gas, un minimo separati**: documenti del progetto in `reports/crm/`, dati dei clienti in un file solo del CRM (`.gas_memory_crm.db`), non più dentro la memoria di Gas.
6. *(Servizi e commissioni: domanda riformulata, vedi `domande.md`.)*
7. **Invio da solo, ma all'inizio con controllo e autorizzazione dell'operatore** per ogni messaggio. → resta il click «Approva»; la modalità automatica si accende dopo, quando l'operatore lo decide.
8. **Le chat devono sapere dei problemi del progetto** (lacuna segnalata: il blocco della CI l'operatore l'ha saputo da un'altra chat). → vedi domande e `reports/stato_progetto.md`.
9. **Massima riservatezza**: i dati dei clienti non devono MAI finire ai modelli gratuiti; i lavori sui clienti solo con modelli almeno Opus. Attenzione a non scrivere a un cliente appena entrato. → Gas riconosce i clienti del CRM e manda quei messaggi solo al cervello forte (R-803-4 chiusa); i testi per i clienti li scrive Claude Opus; anzianità minima prima della prima proposta.

## 18 novembre 2026 — risposta alla domanda 3 e note della verifica esterna

10. **SOLO Opus anche nella chat di Gas** quando si parla di clienti: «SOLO opus in chat, anche se tanto risponderà in modo predefinito, la conversazione completa la lascia a me». → ogni chiamata del cervello forte con dati di clienti nella conversazione usa Claude Opus (`GAS_MODEL_CLAUDE_CLIENTI`, default Opus), anche nei turni `/forte`, quando i dati arrivano a metà turno e nella riflessione di fine conversazione. Se il modello configurato non è Opus, Gas si ferma e lo dice: mai un modello minore. Il resto della chat (senza clienti) resta col modello forte normale (oggi Sonnet), che riceve la memoria di Gas in versione anonima, senza nomi dei lead (R-810-1): i dati dei clienti li vede solo Opus. La conversazione vera col cliente la fa l'operatore.
11. **Note della verifica esterna #381 (3° giro) sistemate subito**: filtro delle parole vietate che non si aggira con spazi o caratteri invisibili; avviso «⚠ ATTENZIONE» quando si sceglie a mano un cliente appena entrato, senza pagamenti, col follow-up spento o nel mese in perdita (non blocca: decide l'operatore); il nome del modello Opus nel file unico dei modelli (`brains/model_ids.py`).

## 19 novembre 2026 — dopo la prima prova sul Mac

12. **Se il Mac si rompe non si deve perdere il gestionale**: copia di sicurezza anche su **iCloud Drive** (scelta dell'operatore). → copia giornaliera CIFRATA con una password dell'operatore (`GAS_CRM_BACKUP_PASSWORD`), mai in chiaro, e comando `ripristina`.
13. **Niente spese per un server solo per il CRM** («non vorrei spendere soldi per un crm»). → per ora resta sul Mac con la copia su iCloud; il CRM andrà sul server di Gas quando arriva (R5, che serve comunque a Gas), senza costi in più. Alternative gratuite valutate: accesso dal telefono con Tailscale (gratis, Mac acceso) o un server gratuito tipo Oracle Cloud «Always Free» (regione europea; da decidere).
14. **Il giro del motore ogni 10 minuti non serve**: basta 1-2 al giorno, più l'aggiornamento a richiesta. → `GAS_CRM_SCAN_MINUTI` di default 720 (2 al giorno); resta il giro subito a ogni cambio e col pulsante «Scansiona». Il giro non usa token.

## 21 novembre 2026 — «pronto all'uso» e risposte alle domande 2 e 3

15. **«Online» voleva dire «pronto all'uso»**: il CRM si usa sul Mac, dal browser del Mac; non va pubblicato su internet. → nessuna modifica; per aprirlo dal telefono la strada gratuita e privata resta Tailscale, da decidere.
16. **WhatsApp Business: l'operatore non sa come avere l'accesso API.** → per ora i messaggi li scrive il CRM e li manda l'operatore a mano, dopo averli approvati (com'era già deciso). L'accesso API di Meta si prepara solo quando si vorrà l'invio automatico, con una guida passo passo.
17. **Bacheca comune tra le chat: sì** («sarebbe veramente utile»). → `reports/bacheca.md`, con la regola in CLAUDE.md §3: ogni chat la legge all'avvio e ci scrive le notizie che toccano anche le altre.

## 23 novembre 2026 — usare il CRM parlando con Gas

18. **L'operatore vuole dare comandi al CRM tramite Gas** (Telegram e voce): aggiungere, togliere, farsi ricordare le cose. Ha scelto la proposta «Sì, fallo tu qui». → Gas può **leggere** il CRM quando serve; **scrive solo dopo il «sì» dell'operatore** (firma su Telegram, che mostra per esteso cosa cambierà). Gli **importi** li prende solo dai messaggi dell'operatore: se la cifra non c'è, Gas la chiede e non la inventa. **Niente cancellazioni**: «togliere» un cliente vuol dire archiviarlo (stato «perso»), i dati restano. I **promemoria** arrivano su Telegram all'ora scelta. I dati dei clienti, anche qui, li vede **solo Opus** (punto 10).
19. **«Sempre Opus»** (scelta dell'operatore fra tre opzioni, dopo la nota V-1 della verifica esterna della PR #397: un cliente nuovo scritto senza le parole del CRM arrivava prima a un modello minore). → tutto quello che l'operatore scrive o dice a Gas (Telegram, voce, terminale, e anche i compiti della notte e in sottofondo) lo legge solo Claude Opus. Interruttore `GAS_SOLO_OPUS`, acceso di default; con `GAS_SOLO_OPUS=0` nel `.env` si torna alla scelta per parole (filtro dei clienti). Limite (review #848-CRM): a voce l'audio passa comunque da Groq (trascrizione) e la risposta da ElevenLabs (voce), come prima. Contro accettati: se Opus non c'è (forte spento o tetto del giorno finito) Gas non risponde finché non torna; a voce può essere un po' più lento; il tetto giornaliero del forte si consuma prima.

## 24 novembre 2026 — CRM sempre acceso e revisione in più

20. **Gli script del CRM passano dal revisore** («ci sta comunque una revisione in più, dato che comunque sono dati personali dei clienti e non dobbiamo fare assolutamente neanche un errore»). → `scripts/crm/` entra nel perimetro di review (`.claude/perimetro_review.txt`), come `scripts/voce/`.

## 25 novembre 2026 — dashboard anche dal telefono

21. **La dashboard si deve vedere anche dal telefono** («sì fallo, voglio vederla anche dal telefono»; scelta dopo la proposta di una rete privata tra i dispositivi; era la domanda aperta del punto 15). → Tailscale con `tailscale serve`: il CRM resta su 127.0.0.1 e non si apre a internet; il telefono entra solo dalla rete privata dell'operatore, in HTTPS, col token. Il server accetta, oltre a `localhost` e agli IP, solo il nome `*.ts.net` del Mac dichiarato in `GAS_CRM_NOME_TAILSCALE`, e da lì il cookie è `Secure`. Mai il funnel (pubblico): `scripts/crm/telefono.sh` si ferma se lo trova. Sul Mac resta l'icona «CRM Gas» della Scrivania (fatta da `installa.sh`).
22. **Un dato del CRM anche senza campo, senza app nuove** («per forza tailscale? … posso accederci eventualmente offline … mi serve solo un dato al volo»; scelte: «Sì, fai la scheda» e «Scheda ora, modifiche col server»). → «Scheda clienti.pdf» protetta da password (AES-256) in iCloud Drive, da aprire con l'app File dell'iPhone anche offline; rifatta solo quando cambiano i dati (e ricontrollata una volta al giorno per il cambio del mese), zero token; password propria `GAS_CRM_SCHEDA_PASSWORD` di almeno 16 caratteri e diversa da quella delle copie cifrate (R-864-1). Le modifiche fatte senza connessione (che l'operatore vuole salvate «al 100% senza errori» quando torna la linea) si costruiscono col server di Gas, sempre acceso: coda sul telefono, invio con identificativo unico (mai due volte), rifiuti mostrati e mai persi. Tailscale resta per la dashboard dal vivo finché il CRM non va sul server.
