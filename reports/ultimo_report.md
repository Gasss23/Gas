# ULTIMO REPORT — Ritocchi finali del funnel dopo la prova dell'operatore

**Data:** 23 novembre 2026
**Branch:** claude/ritocchi-simulazione

## DECISIONI UMANE RICHIESTE

1. **Merge della PR di questa sessione** (vedi handoff §0). Solo documenti del funnel + report.
2. **Consegnare il pacchetto allo sviluppatore del bot** (su main dopo il merge): `reports/funnel/tasto_collaboratori.md`, `reports/funnel/funnel_v2.md`, `reports/funnel/simulazione_funnel.html`. La simulazione pubblica su claude.ai è già aggiornata coi ritocchi.
3. **Ripristinare nel bot «Inizia Ora · Accesso» lo stato dell'operatore** (test del 21/11: portato a «Candidato — pronto per la VIP»): bottoni «Conto aperto» / «In VIP» sulla scheda.

**Ancora aperte da altre sessioni**: in `reports/stato_progetto.md` (sessione CRM PR #397, chat Voce).

## Esito fette

- **Fetta unica — Tre ritocchi chiesti dall'operatore il 23/11 dopo la prova della simulazione** (percorso completo e link agente «ok»/«perfetti», con tre richieste): FATTA.
  1. **Via la domanda «Da quale community arrivi?»** dal percorso completo (fase 1): il bot parte dalla domanda della lingua (che porta la conferma dei 18 anni). Scritto in `funnel_v2.md` (prima regola comune + i due rimandi «fase 1 resta com'è») e nella simulazione.
  2. **Percorso diretto: solo nome e cognome.** Niente più domanda della lingua né bottoni del consenso: messaggio unico (con rischio e compenso), poi un solo campo «Scrivimi nome e cognome» con la riga «Inviando confermi di avere almeno 18 anni e ci autorizzi a risponderti qui» (testo steso dall'agente su mandato dell'operatore), poi [Scrivi a {agente}]. Il consenso aggiornamenti NON si chiede nel diretto: senza un sì, niente promozione (lo raccoglie l'agente in chat se serve); i solleciti del caso B non sono promozione. Aggiornati `tasto_collaboratori.md` §3.1 e §4.5 e la simulazione (funzione `ctaConConsenso` rimossa).
  3. **Requisito Pannello blu**: la voce «I miei link», le card e i link dell'agente si aprono DENTRO il Pannello esistente (bottone blu «Pannello» nella chat del bot, confermato dall'operatore su screenshot) — nessuna app o pagina nuova. Scritto in `tasto_collaboratori.md` §4.6 e nella scheda agente della simulazione.
- **Fetta 2 — Correzioni del 1° verdetto del bot sulla PR #401 («Sistema prima» dell'operatore)**: FATTA. Lingua del diretto dichiarata (quella del Telegram del lead, IT/EN, altrimenti italiano — anche per la riga dei 18 anni); §3/§6 dell'handoff coi commit reali; card del diretto «solo nome e cognome»; rimando all'eccezione del diretto nella regola del consenso di `funnel_v2.md`. Simulazione ripubblicata.
- Simulazione ripubblicata sulla pagina pubblica claude.ai e PROVATA dal vivo nel browser dopo la ripubblicazione: percorso completo parte dalla lingua; diretto mostra messaggio unico → campo nome con la riga dei 18 anni → reazione calda → CTA; scheda agente con la nota del Pannello blu.

## Anomalie / cose da sapere

- `reports/stato_progetto.md`: aggiornata la voce Funnel (PR #396 mergiata, ritocchi, cosa resta).
- Riserva ereditata dalla PR #396 (3° verdetto, V-1 COSMETICA): nei log di quella sessione la prima fetta si chiamava «Fetta unica» accanto a «Fetta 2/3» — superata: i report sono stati riscritti per questa sessione.
- Letta `reports/bacheca.md` prima del giro: nessuna notizia bloccante; niente da aggiungere (toccati solo file del funnel e report canonici).
