# ULTIMO REPORT — Trigger dei solleciti deciso (caso A / caso B) in funnel_v2 e nella simulazione

**Data:** 23 novembre 2026
**Branch:** claude/trigger-solleciti

## DECISIONI UMANE RICHIESTE

1. **Merge della PR di questa sessione** (vedi handoff §0). Solo documenti del funnel + report.
2. **Consegnare il pacchetto allo sviluppatore del bot** (su main dopo il merge): `reports/funnel/tasto_collaboratori.md`, `reports/funnel/funnel_v2.md` (ora con la regola dei solleciti completa) e `reports/funnel/simulazione_funnel.html` come riferimento visivo. La simulazione è condivisa pubblica dall'operatore (pagina claude.ai, 22/11): si aggiorna da sola a ogni ripubblicazione.

3. **Ripristinare nel bot «Inizia Ora · Accesso» lo stato dell'operatore** (il test dal vivo del 21/11 lo ha portato a «Candidato — pronto per la VIP»): bottoni «Conto aperto» / «In VIP» sulla scheda.

**Ancora aperte da altre sessioni** (fonte: ultimo_report della PR #394 e `stato_progetto.md`): lista delle commissioni per servizio (la manda l'operatore); password delle copie nel `.env` del Mac; `pip install -r requirements.txt`; `pwd` della cartella di Gas; prova di copia/ripristino sul Mac; secondo controllo su claude.ai delle PR #387/#388/#389/#391; registrazione della voce da rifare (PR #390).

## Esito fette

- **Fetta unica — Trigger dei solleciti (decisione dell'operatore del 23/11, «ok vai» alla proposta dell'agente)**: FATTA. Chiusa l'incoerenza scoperta dal 4° verdetto del bot sulla PR #393 (le regole comuni di funnel_v2 davano un testo solo per due momenti diversi). Ora `funnel_v2.md`, regole comuni, definisce DUE trigger con testi propri: **caso A** (lead fermo a metà dei passaggi della candidatura) coi testi di prima; **caso B** (candidatura accettata ma «Scrivi a {agente}» non premuto — unico caso del percorso diretto) coi testi nuovi «Ti manca solo l'ultimo passo…» / «Vuoi fare l'ultimo passo o chiudo qui?». Per entrambi: massimo 2 solleciti poi silenzio, partono solo per chi ha iniziato il percorso, niente promozione a freddo. Aggiornati i rimandi (consenso, Bozza B «ultimo passo», percorso diretto). La simulazione ora usa i testi del caso B (l'unico che simula) senza più note di proposta, con una riga che spiega dove vale il caso A; provata dal vivo nel browser e ripubblicata.

- **Fetta 3 — Correzione del 2° verdetto del bot sulla PR #396 (terzo giro, scelta dell'operatore «Sistema prima»)**: FATTA. Unica V-1 BASSA: la mappatura commit→run nel §6 dell'handoff attribuiva a 9549d20 «nessuna run propria completata»; riscritta con le run reali (CI 45099433261 success; verifica-bot skipped/cancelled), come indicato dal bot.

- **Fetta 2 — Correzioni del 1° verdetto del bot sulla PR #396 (secondo giro)**: FATTA. V-1 BASSA: `tasto_collaboratori.md` §4.3 riscritto (rimando esplicito ai 2 solleciti del caso B coi testi) e caso B di `funnel_v2.md` esteso al diretto («dopo il messaggio unico»). V-2 BASSA: `stato_progetto.md` aggiornato (trigger deciso il 23/11, esperto fatto; restano consegna e ripristino stato bot) e la voce sul ripristino riportata qui sopra (punto 3). V-3 COSMETICA: handoff §3 e §7 sistemati.

## Anomalie / cose da sapere

- La pagina della simulazione è diventata PUBBLICA il 22/11 (condivisione fatta dall'operatore per i collaboratori): le ripubblicazioni la aggiornano allo stesso link.
- Nessun file del motore toccato. Letta `reports/bacheca.md` (regola nuova della PR #394) prima del giro: nessuna notizia che blocchi questa fetta; niente da aggiungere in bacheca (nessun file condiviso con altre chat toccato oltre ai report canonici).
