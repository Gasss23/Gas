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
