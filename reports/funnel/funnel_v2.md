# Funnel candidatura VIP — versione 2 (due bozze pronte)

> 21 novembre 2026. Bozze dell'agente su richiesta dell'operatore, basate su `analisi_competitor.md`.
> Decidere: Bozza A (vocale/video), Bozza B (solo messaggi) o test A/B (il bot assegna metà e metà e si confronta la % che arriva a «Scrivi all'agente»).

## Regole comuni (valgono per entrambe)

- **Dal modulo si tolgono**: esperienza (③), «costanza» (④), consenso aggiornamenti (⑥). Esperienza e capitale veri li chiede l'AGENTE in DM come fanno i competitor migliori; la domanda sulla costanza seleziona ma non recupera; il consenso si sposta in una riga sotto l'ultimo passo («ti terremo aggiornato qui, scrivi STOP per non riceverli»).
- **Dopo ogni risposta il bot reagisce con una riga calda**, come una persona: «Ottima scelta 👌», «Nessun problema: ti guidiamo noi dal primo passo».
- **Spiegazione a prova di principiante** (va detta PRIMA delle domande): «Ogni giorno ricevi un messaggio con tre numeri: dove entrare, dove fermarti se va male, dove incassare. Noi stiamo sul grafico, tu copi.»
- **Follow-up automatici** se il lead si ferma (a metà domande o senza premere «Scrivi a …»):
  - +24 h: «Ti ho tenuto il posto 🤝 Ti mancano 30 secondi: riprendiamo da dove eri?» [Riprendi]
  - +72 h: «Chiudo la tua candidatura? Questa settimana gli ingressi sono quasi pieni.» [Riprendila] [Lascia stare]
  - Oltre: silenzio (mai più di 2 solleciti).
- **Prova sociale**: nel messaggio di presentazione una riga vera e aggiornabile (es. «Questa settimana sono entrate N persone») — solo numeri veri.
- La **scheda per l'agente resta identica** (campi mancanti = «da chiedere in chat»), così il pannello non cambia.

## Bozza A — «prima la voce» (consigliata)

**Passo 0 — /start**: il bot manda UN video-messaggio (o vocale) di Gaspare, registrato una volta, uguale per tutti, 30–45 secondi:

> «Ciao, sono Gaspare 👋 Benvenuto. Ti spiego in trenta secondi come funziona: ogni giorno in sala VIP ricevi i segnali completi — dove entrare, dove mettere lo stop, dove incassare — e li gestiamo in diretta con te. Non ci paghi nessun abbonamento: l'accesso si attiva aprendo un conto dal nostro link col broker partner, e i soldi restano SUL TUO conto, sempre tuoi. Rispondi a tre domande veloci così so come seguirti, e ci sentiamo di là.»

Sotto il video, testo breve (per chi non ascolta): le stesse 3 righe + «3 domande, 1 minuto».

**Le 3 domande** (risposta a bottoni):
1. «Cosa vuoi dalla VIP?» → 📈 Sale segnali / 🤖 Copy trading automatico / Entrambi
2. «Hai già un conto di trading?» → Sì / No, non ancora → se No: «Perfetto, nessun problema: ti guidiamo noi, è gratis e ci vogliono 10 minuti.»
3. «Come ti chiami? (nome e cognome, così {agente} sa chi sei)» → testo libero

**Ultimo passo** (invariato nella sostanza, più diretto nel tono):
> «✅ Candidatura accettata, {nome}. Ultimo passo: premi qui sotto e manda il messaggio già pronto a {agente} — ti risponde a breve e ti attiva. Intanto segui i segnali gratuiti nel canale. 🔒 {agente} non ti chiede mai soldi: i fondi restano sul tuo conto.»
> [💬 Scrivi a {agente}]

**Perché così**: il vocale crea il rapporto (come LEO/MOMO), il modulo scende da 7 a 3 passaggi, la qualifica vera (capitale 500 $, esperienza) la fa l'agente a voce in DM, dove un «non ancora» si recupera invece di restare freddo su una scheda.
**Cosa serve dall'operatore**: UN video-messaggio o vocale registrato da Gaspare (meglio video rotondo, più personale; si registra dal telefono in chat con il bot e si riusa per sempre).

## Bozza B — solo messaggi (migliorata)

**Passo 0 — /start**:
> «Ciao {nome} 👋 Questa è la tua candidatura alla sala VIP di Inizia Ora.
> Funziona così: ogni giorno ricevi i segnali completi — un messaggio con tre numeri: dove entrare, dove fermarti, dove incassare — e li gestiamo in diretta con te, con una persona vera al tuo fianco.
> 💶 Non paghi nessun abbonamento: l'accesso si attiva aprendo il conto dal nostro link col broker partner. I soldi restano sul tuo conto, sempre tuoi.
> 4 domande e ci siamo (1 minuto).»

**Le 4 domande**:
1. «Cosa ti interessa?» → 📈 Sale segnali / 🤖 Copy trading automatico / Entrambi
2. «Hai già un conto di trading?» → Sì / No, non ancora (→ riga di rassicurazione come in A)
3. «Per operare bene in sala servono almeno 500 $ sul TUO conto (restano tuoi, al broker). Li hai da parte?» → Sì / Ci arrivo a breve / No → «Ci arrivo a breve» NON scarta: «Perfetto, intanto entra: parti quando sei pronto.»
4. «Nome e cognome, così {agente} sa chi sei» → testo libero

**Ultimo passo**: identico alla Bozza A.

**Differenze vs oggi**: da 7 a 4 passaggi; la domanda sui 500 $ resta (qualifica più dura della A) ma riformulata col «ci arrivo a breve» che tiene dentro i tiepidi; tolte esperienza/costanza/consenso; reazioni calde del bot a ogni risposta.

## Confronto rapido per decidere

| | Bozza A (voce) | Bozza B (messaggi) |
|---|---|---|
| Rapporto umano | ⭐⭐⭐ sente la voce al msg 1 | ⭐ solo testo |
| Attrito | 3 domande | 4 domande |
| Qualifica nel bot | più morbida (500 $ li chiede l'agente) | più dura (500 $ nel modulo) |
| Lavoro per partire | registrare 1 video/vocale | zero |
| Rischio | tono del vocale da azzeccare | resta «un modulo» |

Proposta dell'agente: partire con A; se il bot gestisce i gruppi di prova, A/B per 2 settimane sulla % che preme «Scrivi a {agente}».
