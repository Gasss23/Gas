# ULTIMO REPORT — Simulazione cliccabile del funnel + conteggi vecchi nei report

**Data:** 21 novembre 2026
**Branch:** claude/simulazione-funnel

## DECISIONI UMANE RICHIESTE

1. **Provare la simulazione del funnel** (`reports/funnel/simulazione_funnel.html`): aprirla e cliccare i tre percorsi; ogni modifica ai testi si decide lì sopra prima della consegna allo sviluppatore.
1bis. **Scegliere il trigger unico dei solleciti** (incoerenza nelle fonti scoperta dal 4° verdetto del bot): `funnel_v2.md` dice sia «chi si ferma a metà candidatura» (regole comuni) sia «chi non preme Scrivi a {agente}» (Bozza B). Se il sollecito parte dopo la candidatura accettata, il testo «Ti mancano 30 secondi di candidatura» è incoerente. Proposta dell'agente: entrambi i trigger, con due testi — a metà candidatura il testo attuale; dopo l'accettazione «Ti manca solo l'ultimo passo: scrivi a {agente}» (come nel diretto). Da fissare in `funnel_v2.md` dopo il merge.
2. **Merge della PR di questa sessione** (vedi handoff §0).
3. **Consegnare il pacchetto allo sviluppatore del bot** (scelta dell'operatore del 21/11, su main): `reports/funnel/tasto_collaboratori.md` (tasto «I miei link» nel Pannello), `reports/funnel/funnel_v2.md` (Bozza B, 3 passaggi) e la simulazione come riferimento visivo.
4. **Far controllare i testi del funnel a un esperto di promozione finanziaria/privacy** prima dell'uso (raccomandazione della verifica esterna #392).
5. **Ripristinare lo stato dell'operatore nel bot** «Inizia Ora · Accesso» (il test dal vivo lo ha portato a «Candidato — pronto per la VIP»): bottoni «Conto aperto» / «In VIP» sulla scheda.

**Ancora aperte dalla sessione CRM (PR #391, mergiata)**: password delle copie nel `.env` del Mac; `pip install -r requirements.txt`; `pwd` della cartella di Gas; secondo controllo su claude.ai; da decidere se aggiungere al bot come gravi «alto», «severo», «serio», «elevato». (Dettagli nel report della #391 in git e in `stato_progetto.md`.)

## Esito fette

- **Fetta 1 — Simulazione cliccabile del funnel (richiesta dell'operatore del 21/11)**: FATTA. `reports/funnel/simulazione_funnel.html`: pagina autonoma (HTML+JS, zero dipendenze, nessun dato inviato) che simula la chat Telegram del bot in tre percorsi — lead col percorso completo (fase 1 di oggi invariata + candidatura Bozza B a 3 passaggi, reazioni calde, follow-up +24 h/+72 h), lead con link diretto `-vip` (tutele incluse), e vista agente del Pannello «I miei link» (2 link, contatori, card da inoltrare). Testi presi dalle fonti (`funnel_v2.md`, `tasto_collaboratori.md` e, per la fase 1 di oggi, `analisi_competitor.md` §1); le poche righe NON fissate dalle specifiche (reazioni calde al passo capitale/consenso, sollecito del percorso diretto) sono proposte dell'agente, marcate con * nella pagina stessa; l'«ultimo passo» usa il testo della Bozza A di `funnel_v2.md` più la riga sul rischio (V-2 dei due verdetti bot #393). Provata dal vivo dall'agente: tutti e tre i percorsi funzionano fino in fondo. Copia privata pubblicata come pagina claude.ai per il test comodo dell'operatore (il file nel repo resta la fonte unica).
- **Fetta 2 — Nota bassa del 3° verdetto del bot sulla PR #392 (conteggi vecchi «7 domande»/«4 domande» nei report)**: FATTA/SUPERATA. Mentre questa sessione partiva, la PR #391 (CRM) è stata mergiata e ha riscritto i tre report di sessione su main: i conteggi vecchi su main NON esistono più (verificato con grep su origin/main). I report di QUESTA sessione li sostituiscono di nuovo come fotografia più recente, senza riproporre i testi sbagliati; la descrizione corretta del funnel (due fasi) sta nei file canonici `reports/funnel/analisi_competitor.md` §1 e `funnel_v2.md`.

- **Fetta 3 — Correzioni del 1° verdetto del bot sulla PR #393 (secondo giro)**: FATTA. V-1 BASSA (cambiare scheda o «Ricomincia» durante «sta scrivendo…» mescolava due percorsi): contatore di generazione, ogni helper si ferma se il flusso non è più quello attivo — verificato dal vivo cambiando scheda a metà scrittura. V-2 BASSA (claim «testi alla lettera» sovrastimato): righe proposte dall'agente ora marcate con * nella pagina e dichiarate qui sopra; nel percorso diretto l'ordine ora segue la spec §3.1 ([Scrivi a {agente}] attaccato al messaggio e consenso SOTTO, visibili insieme); il sollecito del diretto non parla più di «candidatura». V-3 COSMETICA (innerHTML sull'input del nome, self-XSS locale): i messaggi usano textContent.

- **Fetta 4 — Correzioni del 2° verdetto del bot + merge di main (terzo giro)**: FATTA. V-1 BASSA (claim «alla lettera» rimasto nell'handoff): allineato. V-2 BASSA («ultimo passo» non marcato): adottato il testo della Bozza A di `funnel_v2.md` + riga sul rischio, come suggerito dal bot. V-3 COSMETICA: bolla del consenso nel diretto sopra la tastiera; `nome` azzerato a ogni `start()` (non trapela tra le schede). In più: merge di origin/main nel branch (la PR #390 fix voce aveva messo la PR in conflitto sui report canonici), risolto tenendo la versione del ramo — review #837-MERGE APPROVATO, perimetro byte-identico a main. Pagina ripubblicata e riverificata.

- **Fetta 5 — Correzioni del 3° verdetto del bot (quarto giro)**: FATTA. V-1 BASSA: anche il sollecito a +72 h del percorso diretto ora ha un testo suo senza «candidatura» (marcato con *, bottoni Riprendi/Chiudi); verificato dal vivo. V-2 COSMETICA: tolti i ritocchi non marcati — via la numerazione «1/3-2/3-3/3» dai passaggi, via l'emoji aggiunta a «Imparare a farlo da solo», «Sei già nella community.» come nella fonte.

- **Fetta 6 — Correzioni del 4° verdetto del bot (quinto giro)**: FATTA. V-1 BASSA (incoerenza dei solleciti del percorso completo dopo la candidatura accettata — difetto che viene dalle FONTI, non dalla pagina): nella pagina ora una nota * dichiara l'incoerenza e rimanda alla decisione dell'operatore (punto 1bis qui sopra); i testi di funnel_v2 restano invariati in attesa della scelta. V-2 COSMETICA (riga superata nella Fetta 3 dell'handoff): riscritta al passato con rimando alla Fetta 4.

## Anomalie / cose da sapere

- Sessioni parallele: le PR #391 (CRM) e #390 (fix voce) sono andate su main durante questa sessione; branch ripartito da eecf916 e poi merge di main (019c6c8) per il conflitto sui report. Nessun conflitto rimasto.
- Nessun file del motore scritto in questa sessione (i file voce/CRM entrano dal merge, byte-identici a main).
