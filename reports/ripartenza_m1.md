# Ripartenza M1 (chat «Co-Work», coordinamento) — 3 novembre 2026

## Chi sono e come lavoro
- Sono **M1**: l'operatore parla solo con me. Coordino le altre chat, prendo le decisioni con lui e gli riporto riassunti brevissimi.
- Chat attive (si raggiungono con `send_message`):
  - **M2**, «sviluppo voce»: `session_01NNEhCrUBQWWRfz7P8CQAPQ`. Si occupa di `modules/voice/`, `clients/voice/browser_*` e `ci.yml`.
  - **Mani**, «chat parallela»: `session_01Am58FXJuf8rxY8JbKts9Ey`. Si occupa di `clients/voice/ascolto*`, `scripts/voce/`, web, Telegram e mail.
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
