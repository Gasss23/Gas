# ULTIMO REPORT — Simulazione cliccabile del funnel + conteggi vecchi nei report

**Data:** 21 novembre 2026
**Branch:** claude/simulazione-funnel

## DECISIONI UMANE RICHIESTE

1. **Provare la simulazione del funnel** (`reports/funnel/simulazione_funnel.html`): aprirla e cliccare i tre percorsi; ogni modifica ai testi si decide lì sopra prima della consegna allo sviluppatore.
2. **Merge della PR di questa sessione** (vedi handoff §0).
3. **Consegnare il pacchetto allo sviluppatore del bot** (scelta dell'operatore del 21/11, su main): `reports/funnel/tasto_collaboratori.md` (tasto «I miei link» nel Pannello), `reports/funnel/funnel_v2.md` (Bozza B, 3 passaggi) e la simulazione come riferimento visivo.
4. **Far controllare i testi del funnel a un esperto di promozione finanziaria/privacy** prima dell'uso (raccomandazione della verifica esterna #392).
5. **Ripristinare lo stato dell'operatore nel bot** «Inizia Ora · Accesso» (il test dal vivo lo ha portato a «Candidato — pronto per la VIP»): bottoni «Conto aperto» / «In VIP» sulla scheda.

**Ancora aperte dalla sessione CRM (PR #391, mergiata)**: password delle copie nel `.env` del Mac; `pip install -r requirements.txt`; `pwd` della cartella di Gas; secondo controllo su claude.ai; da decidere se aggiungere al bot come gravi «alto», «severo», «serio», «elevato». (Dettagli nel report della #391 in git e in `stato_progetto.md`.)

## Esito fette

- **Fetta 1 — Simulazione cliccabile del funnel (richiesta dell'operatore del 21/11)**: FATTA. `reports/funnel/simulazione_funnel.html`: pagina autonoma (HTML+JS, zero dipendenze, nessun dato inviato) che simula la chat Telegram del bot in tre percorsi — lead col percorso completo (fase 1 di oggi invariata + candidatura Bozza B a 3 passaggi, reazioni calde, follow-up +24 h/+72 h), lead con link diretto `-vip` (tutele incluse), e vista agente del Pannello «I miei link» (2 link, contatori, card da inoltrare). Testi presi dalle fonti (`funnel_v2.md`, `tasto_collaboratori.md` e, per la fase 1 di oggi, `analisi_competitor.md` §1); le poche righe NON fissate dalle specifiche (reazioni calde al passo capitale/consenso, sollecito del percorso diretto, «ultimo passo» ricostruito perché funnel_v2 dice solo «come oggi») sono proposte dell'agente, marcate con * nella pagina stessa (V-2 verifica-bot #393). Provata dal vivo dall'agente: tutti e tre i percorsi funzionano fino in fondo. Copia privata pubblicata come pagina claude.ai per il test comodo dell'operatore (il file nel repo resta la fonte unica).
- **Fetta 2 — Nota bassa del 3° verdetto del bot sulla PR #392 (conteggi vecchi «7 domande»/«4 domande» nei report)**: FATTA/SUPERATA. Mentre questa sessione partiva, la PR #391 (CRM) è stata mergiata e ha riscritto i tre report di sessione su main: i conteggi vecchi su main NON esistono più (verificato con grep su origin/main). I report di QUESTA sessione li sostituiscono di nuovo come fotografia più recente, senza riproporre i testi sbagliati; la descrizione corretta del funnel (due fasi) sta nei file canonici `reports/funnel/analisi_competitor.md` §1 e `funnel_v2.md`.

- **Fetta 3 — Correzioni del 1° verdetto del bot sulla PR #393 (secondo giro)**: FATTA. V-1 BASSA (cambiare scheda o «Ricomincia» durante «sta scrivendo…» mescolava due percorsi): contatore di generazione, ogni helper si ferma se il flusso non è più quello attivo — verificato dal vivo cambiando scheda a metà scrittura. V-2 BASSA (claim «testi alla lettera» sovrastimato): righe proposte dall'agente ora marcate con * nella pagina e dichiarate qui sopra; nel percorso diretto l'ordine ora segue la spec §3.1 ([Scrivi a {agente}] attaccato al messaggio e consenso SOTTO, visibili insieme); il sollecito del diretto non parla più di «candidatura». V-3 COSMETICA (innerHTML sull'input del nome, self-XSS locale): i messaggi usano textContent.

## Anomalie / cose da sapere

- Sessione parallela: la PR #391 (CRM) è andata su main tra il merge della #392 e questa PR; questo branch riparte da main eecf916, nessun conflitto rimasto.
- Nessun file del motore toccato in questa sessione.
