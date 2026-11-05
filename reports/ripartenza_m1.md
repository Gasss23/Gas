# Ripartenza M1 (chat «Co-Work», coordinamento) — 3 novembre 2026

## Chi sono e come lavoro
- Sono **M1**: l'operatore parla solo con me. Coordino le altre chat, prendo le decisioni con lui e gli riporto riassunti brevissimi.
- Chat attive (si raggiungono con `send_message`):
  - **M2**, «sviluppo voce»: `session_01NNEhCqH77rouMxjiz51336 (nuova dal 4 nov; la vecchia era session_01NNEhCrUBQWWRfz7P8CQAPQ, archiviata)`. Si occupa di `modules/voice/`, `clients/voice/browser_*` e `ci.yml`.
  - **Mani**, «chat parallela»: `session_01NNEhCp31GsAtPmtpTkGGRf (nuova dal 4 nov; la vecchia era session_01Am58FXJuf8rxY8JbKts9Ey, archiviata)`. Si occupa di `clients/voice/ascolto*`, `scripts/voce/`, web, Telegram e mail.
- Regole di merge:
  - con un APPROVATO pulito del bot mergio io;
  - con riserve serve il sì dell'operatore, poi mergio io (o lo inoltro alla chat proprietaria);
  - basta giri di correzione per le riserve BASSE/COSMETICHE: si registrano e si va avanti.
- Comandi per l'operatore: SEMPRE in riquadri ``` da copiare.
- Accesso al Mac (Remote Control): ancora bloccato. La cartella Gas risulta «not_available» e `confirm_repository_trust` viene negato in automatico. Si lavora con comandi da copiare.

## Fatto (PR mergiate dal 30 ottobre al 3 novembre)
- #318–#330 tutte mergiate, tranne la #329. Contenuto:
  - voce che capisce meglio (V6);
  - tempi a schermo (V7a);
  - voce frase per frase (V7b);
  - pagina /voci (V8);
  - filtri per il rumore (V9);
  - formato solo-voce «audio+pezzi» (V10);
  - Telegram `avvisa_operatore` (#319);
  - difesa del forte contro `--bare` (#321);
  - proposta del cervello caldo (#320, solo documento);
  - ascolto H24 «Hey Jarvis» (#323);
  - piano mail (#324, solo documento);
  - fix dell'installazione (#328).
- **#329** (ascolto H24 a frasi in fila): il sì dell'operatore c'è, era in conflitto dopo la #330; la mergia Mani appena la CI è verde.

## Da fare SUBITO con l'operatore: prova di Jarvis sul Mac
1. Aggiornare e installare:
   ```
   cd ~/Gas && git pull origin main && bash scripts/voce/installa.sh && bash scripts/voce/installa.sh
   ```
2. Le 7 domande, ognuna preceduta da «Hey Jarvis»:
   1. «Che ore sono?» (velocità)
   2. «Ho 3 clienti a 200 euro al mese e ne perdo uno: quanto incasso in un anno?» (ragionamento)
   3. «Mi chiamo Gaspare e lavoro nel marketing», poi «Come mi chiamo e che lavoro faccio?» (memoria)
   4. «Spiegami in tre frasi come trovare nuovi clienti online» (risposta lunga)
   5. parlargli sopra mentre risponde alla 4 (interruzione)
   6. «Ti preparo una lista di idee, va bene?» → «sì»
   7. la domanda 1 con la TV accesa (rumore)
3. Tempi:
   ```
   grep "tempi voce" ~/Gas/gas_debug.log | tail -8
   ```
4. Dai tempi si decide la cura della lentezza:
   - se il tempo va quasi tutto nel cervello: misura e strada A di `reports/proposta_cervello_caldo.md`;
   - se va nella voce o nella trascrizione: lo fa M2.

## Aperti e decisioni dell'operatore
- **Voce di Gas stile Jarvis**: da scegliere sulla pagina /voci (V8). Niente cloni di attori. Va in `ELEVENLABS_VOICE_ID` nel .env.
- **Parola di attivazione**: oggi «hey_jarvis» (licenza CC BY-NC-SA, non commerciale). Poi da addestrare «Hey Gas».
- **Piano mail** (`reports/piano_mail.md`): 7 domande per l'operatore.
- **Cervello caldo**: si sceglie dopo la misura.
- **Riserve BASSE da chiudere** in fette piccole:
  - #330: richiesta a testo che salta il tetto orario;
  - #329: server single-thread, da valutare ThreadingHTTPServer (M2);
  - #327: soglia di interruzione / buffer del fondo;
  - #328: lettura del .env.
- **Browser web**: completo ma spento. Si accende solo dopo una prova sul VPS (R5, server non ancora preso).
- Facoltativo: sbloccare `elevenlabs.io` nella rete dell'ambiente cloud, così le chat leggono la documentazione.
- Token `gas-richieste` (repo Gas-richieste) e `GAS_RICHIESTE_REPO` nel .env: ancora da fare sul Mac.

## Aggiornamento 3 novembre, pomeriggio
- **PR #331 (V11, M2)**: le richieste a testo con audio+pezzi ora ricevono solo testo, senza ElevenLabs. È in attesa del bot e del sì dell'operatore.
- **Decisione per l'operatore (R-663-1-M2)**: le richieste a testo devono contare anche loro nel tetto orario, oppure i client a testo sono considerati fidati?
- **ThreadingHTTPServer**: sconsigliato per ora. Servirebbe una fetta dedicata con lock e test di concorrenza.
- **#329 mergiata da Mani (af91da0)**: «Hey Jarvis» ora suona le frasi in fila, la prima dopo circa 0,3 s. Le riserve BASSE di Mani sono in stato_progetto e aspettano la prossima fetta piccola (via di M1 dopo le prove).
- **Possibile difetto del parser del bot**: un verdetto APPROVATO CON RISERVE che conteneva la parola «MEDIA, preesistente» è stato letto come failure. Da guardare se si ripete (si trova in scripts/bot_esito.py, il cosiddetto lato macchina del bot: decide l'operatore).
- **#331 mergiata (9cd1ad5)**. Decisione dell'operatore: anche le richieste a testo con sintesi vocale contano nel tetto orario. Lo fa M2 nella prossima fetta piccola.
- **4 novembre, chat ripartite pulite.**
  - M2 (nuova) riparte da reports/ripartenza_m2.md sul branch feat/voce-v12-m2, con la **PR #332 (V12)** in corso. La #332 fa contare nel tetto anche le richieste a testo con risposta a voce; serve il sì dell'operatore.
  - Mani (nuova) riparte da reports/ripartenza_mani.md sul branch claude/peaceful-lovelace-0w2b7q. Non ha PR aperte e aspetta il via di M1.
- **#332 (V12)**: il bot l'ha approvata con riserve (una BASSA, una COSMETICA). La CI e la verifica esterna sono ancora in corso. Serve il sì dell'operatore.
- **#332 mergiata.** M2 è ferma e aspetta i tempi misurati sul Mac.

## Prova di Jarvis sul Mac — 5 novembre
- **Configurazione sul Mac**: aggiunto `GAS_ASCOLTO_VOCE_RMS=200` nel .env. Con 500 dopo il bip non sentiva la voce («torno ad aspettare» senza «richiesta registrata»). Con 200 risponde.
- **Tempi** (10 richieste): trascrizione 0,4–1,2 s, voce 0,4–1,5 s, **cervello 3,9–16,9 s**. La lentezza sta nel cervello, non nella voce.
- **Misura dell'avvio di `claude -p`** (script della proposta, modello claude-sonnet-5-5): «avvio e resto» 1,3–1,7 s, sotto la soglia di 2 s. La strada A (processo pre-avviato) servirebbe a poco. I turni da 17 s vengono probabilmente dai giri con strumenti (ogni giro rilancia la CLI e ragiona di nuovo).
- **Difetti visti**: a «che ore sono» ha risposto che non trova il contatto Stefano tra i lead (da capire: trascrizione o cervello confuso dal pin dei lead). Per l'ora serve un giro di strumento (`data_ora`), quindi la risposta è più lenta.
- **Proposta di cura, da far decidere all'operatore**: (1) ora e data già scritte nel prompt dei turni a voce, così si salta il giro dello strumento; (2) risposte a voce più corte; (3) capire la risposta su Stefano dai log del turno.
- **Decisioni dell'operatore (5 nov, sera)**:
  - a) SÌ all'interruzione nell'ascolto H24 → Mani, dopo la #333. Insieme, sempre a Mani: «Sì, signore?» alla prima attivazione.
  - b) NO a Haiku per la voce (giudicato troppo debole). M2 deve prima mandare una proposta (solo documento) per un turno parlato più rapido con lo stesso modello, e per i compiti lunghi: «ci lavoro, ti avviso quando ho fatto» con il lavoro in sottofondo e l'avviso alla fine.
  - c) NO alla cronologia separata: voce, Telegram e il resto sono UNA sola Gas. Le risposte fuori tema si curano in un altro modo (dentro la proposta di M2).
- **PR in corso**: #334 (M2, V13: ora nel prompt, voce più corta, niente «sì o no?», «Hey Jarvis» da solo → «Dimmi.»); #333 (Mani, soglia della voce 200). Entrambe col revisore APPROVATO CON RISERVE BASSE, in attesa del bot.
- **Sul Mac (.env)**: `GAS_ASCOLTO_VOCE_RMS=200`; `GAS_ASCOLTO_SOGLIA=0.35` consigliato all'operatore (da confermare che l'abbia aggiunto).
