# Funnel candidatura VIP — versione 2 (due bozze pronte)

> 21 novembre 2026. Bozze dell'agente su richiesta dell'operatore, basate su `analisi_competitor.md`.
> **DECISIONE DELL'OPERATORE (21/11/2026): si parte con la Bozza B (solo messaggi).** La Bozza A resta qui come riferimento (eventuale test futuro).
> Prima dell'uso: far controllare i testi a qualcuno esperto di promozione finanziaria e privacy (nota della verifica esterna #392).

## Com'è oggi (verificato dal vivo il 21/11)

Il funnel attuale è GIÀ in due fasi: fase 1 community («Da quale community arrivi?», lingua + 18enni, interessi, conto) → scheda lead → fase 2 candidatura VIP (presentazione + 5 passaggi: esperienza, costanza, capitale 500 $ con l'opzione «Li avrò a breve» GIÀ presente, consenso aggiornamenti GIÀ esplicito, nome e cognome) → «ultimo passo» con messaggio precompilato all'agente. Dettaglio completo in `analisi_competitor.md` §1. Le bozze qui sotto cambiano SOLO la fase 2 e aggiungono le regole comuni; la fase 1 resta com'è, tranne la domanda «Da quale community arrivi?», tolta (prima regola comune).

## Regole comuni (valgono per entrambe)

- **Dalla fase 1 si toglie la domanda «Da quale community arrivi?»** (decisione dell'operatore, 23/11/2026, dopo la prova della simulazione): il bot parte direttamente dalla domanda della lingua (che porta anche la conferma dei 18 anni). Il resto della fase 1 resta com'è.
- **Dalla candidatura si tolgono**: esperienza e «costanza». L'esperienza vera la chiede l'AGENTE in DM come fanno i competitor migliori (LEO la chiede a voce); la domanda sulla costanza seleziona ma non recupera. Il consenso aggiornamenti RESTA com'è oggi (esplicito, con bottoni). Risultato: candidatura da 5 passaggi a 3 (capitale, consenso, nome).
- **Dopo ogni risposta il bot reagisce con una riga calda**, come una persona: «Ottima scelta 👌», «Nessun problema: ti guidiamo noi dal primo passo».
- **Spiegazione a prova di principiante** (va detta PRIMA delle domande): «Ogni giorno ricevi un messaggio con tre numeri: dove entrare, dove fermarti se va male, dove incassare. Noi stiamo sul grafico, tu copi.»
- **Follow-up automatici** — DUE trigger, ognuno col suo testo (decisione dell'operatore, 23/11/2026; chiude l'incoerenza segnalata dal 4° verdetto del bot sulla PR #393):
  - **Caso A — il lead si ferma a metà dei passaggi della candidatura:**
    - +24 h: «Ciao {nome} 🤝 Ti mancano 30 secondi di candidatura: riprendiamo da dove eri?» [Riprendi]
    - +72 h: «Vuoi completare la candidatura o la chiudo? Se preferisci, riprendila quando vuoi.» [Riprendila] [Chiudila]
  - **Caso B — il lead non preme «Scrivi a {agente}»** dopo la candidatura accettata (o, nel percorso diretto di `tasto_collaboratori.md`, dopo il messaggio unico: il diretto ha solo questo caso):
    - +24 h: «Ciao {nome} 🤝 Ti manca solo l'ultimo passo: scrivi a {agente} e ti attiva. Lo facciamo ora?» [Riprendi]
    - +72 h: «Vuoi fare l'ultimo passo o chiudo qui? Se preferisci, riprendi quando vuoi.» [Riprendi] [Chiudi]
  - Regole per entrambi i casi: oltre il 2° sollecito, silenzio (mai più di 2); partono SOLO per chi ha iniziato il percorso e riguardano solo il suo completamento — non sono promozione a freddo e non dipendono dal consenso aggiornamenti.
- **Niente scarsità finta** (V-1 verifica esterna #392): frasi come «posti quasi pieni» sono ammesse SOLO se il bot le lega a un numero reale di posti configurato e aggiornato; altrimenti non si scrivono. Vale anche per la prova sociale: nel messaggio di presentazione una riga vera e aggiornabile (es. «Questa settimana sono entrate N persone») — solo numeri veri.
- **Rischio e compenso, sempre detti** (V-2 verifica esterna #392): nella presentazione e nell'«ultimo passo» compare la riga «⚠ Il trading comporta un rischio reale di perdere il capitale: usa solo soldi che puoi permetterti di perdere. I risultati passati non garantiscono quelli futuri.» E al posto del solo «non paghi nessun abbonamento» si dice anche come guadagniamo: «il nostro compenso ce lo riconosce il broker partner quando apri il conto dal nostro link».
- **Consenso esplicito agli aggiornamenti** (V-3 verifica esterna #392): resta ESATTAMENTE come nel bot di oggi — domanda con bottoni «Ti va di ricevere qui aggiornamenti e novità della community?» [Sì, volentieri] [No grazie] — mai consenso presunto. Senza il sì, nessun messaggio promozionale; il sì si revoca scrivendo STOP. Unica eccezione di forma: nel percorso diretto di `tasto_collaboratori.md` il consenso non si chiede affatto e il bot a quei lead non manda MAI promozione (decisione dell'operatore, 24/11/2026) — ogni comunicazione la fa l'agente in chat. Stesso principio: mai consenso presunto. I 2 solleciti (casi A e B qui sopra) riguardano solo il completamento del percorso iniziato, non sono promozione.
- La **scheda per l'agente resta identica** (campi mancanti = «da chiedere in chat»), così il pannello non cambia.

## Bozza A — «prima la voce» (NON scelta; resta come riferimento per un test futuro)

> Nota post-verifica dal vivo: le domande «cosa ti interessa» e «conto» qui sotto stanno già nella fase 1 della community; se un giorno si prova la A, il video va messo in testa alla candidatura VIP e i passaggi restano quelli della Bozza B.

**Passo 0 — /start**: il bot manda UN video-messaggio (o vocale) di Gaspare, registrato una volta, uguale per tutti, 30–45 secondi:

> «Ciao, sono Gaspare 👋 Benvenuto. Ti spiego in trenta secondi come funziona: ogni giorno in sala VIP ricevi i segnali completi — dove entrare, dove mettere lo stop, dove incassare — e li gestiamo in diretta con te. Non ci paghi nessun abbonamento: l'accesso si attiva aprendo un conto dal nostro link col broker partner — è così che veniamo pagati, il compenso ce lo dà il broker — e i soldi restano SUL TUO conto, sempre tuoi. Rispondi a tre domande veloci così so come seguirti, e ci sentiamo di là.»

Sotto il video, testo breve (per chi non ascolta): le stesse 3 righe + «3 domande, 1 minuto».

**Le 3 domande** (risposta a bottoni):
1. «Cosa vuoi dalla VIP?» → 📈 Sale segnali / 🤖 Copy trading automatico / Entrambi
2. «Hai già un conto di trading?» → Sì / No, non ancora → se No: «Perfetto, nessun problema: ti guidiamo noi, è gratis e ci vogliono 10 minuti.»
3. «Come ti chiami? (nome e cognome, così {agente} sa chi sei)» → testo libero

**Ultimo passo** (invariato nella sostanza, più diretto nel tono):
> «✅ Candidatura accettata, {nome}. Ultimo passo: premi qui sotto e manda il messaggio già pronto a {agente} — ti risponde a breve e ti attiva. Intanto segui i segnali gratuiti nel canale. 🔒 {agente} non ti chiede mai soldi: i fondi restano sul tuo conto.
> ⚠ Il trading comporta un rischio reale di perdere il capitale: usa solo soldi che puoi permetterti di perdere.»
> [💬 Scrivi a {agente}]
> «Ti va di ricevere qui aggiornamenti e novità della community?» [Sì, volentieri] [No grazie]

**Perché così**: il vocale crea il rapporto (come LEO/MOMO) e la qualifica vera (esperienza, costanza) la fa l'agente a voce in DM, dove un «non ancora» si recupera invece di restare freddo su una scheda.
**Cosa serve dall'operatore**: UN video-messaggio o vocale registrato da Gaspare (meglio video rotondo, più personale; si registra dal telefono in chat con il bot e si riusa per sempre).

## Bozza B — solo messaggi (SCELTA dall'operatore il 21/11)

La fase 1 (community) resta com'è, meno la domanda della community (regole comuni). Cambia la candidatura VIP:

**Presentazione** (al posto di quella attuale):
> «Ciao {nome} 👋 Questa è la tua candidatura alla sala VIP di Inizia Ora.
> Funziona così: ogni giorno ricevi i segnali completi — un messaggio con tre numeri: dove entrare, dove fermarti, dove incassare — e li gestiamo in diretta con te, con una persona vera al tuo fianco.
> 💶 Non paghi nessun abbonamento: l'accesso si attiva aprendo il conto dal nostro link col broker partner (è così che veniamo pagati: il compenso ce lo riconosce il broker). I soldi restano sul tuo conto, sempre tuoi.
> ⚠ Il trading comporta un rischio reale di perdere il capitale: usa solo soldi che puoi permetterti di perdere. I risultati passati non garantiscono quelli futuri.
> 3 passaggi e ci siamo (1 minuto).» [Iniziamo →]

**I 3 passaggi** (al posto dei 5 attuali — via «esperienza» e «costanza», le chiede {agente} in chat):
1. «💶 Per la sala VIP serve un conto con almeno 500 $, che restano tuoi sul tuo conto al broker. Ce l'hai già?» → [Sì, ce l'ho] [Li avrò a breve] [Non ancora] (come oggi) → reazione calda: con «Li avrò a breve»/«Non ancora»: «Perfetto, nessun problema: intanto completa la candidatura, parti quando sei pronto 👌»
2. «📣 Ti va di ricevere qui aggiornamenti e novità della community?» → [Sì, volentieri] [No grazie] (come oggi)
3. «✍ Ultima cosa: nome e cognome, così {agente} sa chi sei» → testo libero

**Ultimo passo**: come oggi («Candidatura accettata… premi invio» + [💬 Scrivi a {agente}] + «{agente} non ti chiede mai soldi»), con in più la riga sul rischio (regole comuni) e i follow-up del caso B (regole comuni) per chi non preme «Scrivi a {agente}».

**Differenze vs oggi, in sintesi**: candidatura da 5 passaggi a 3; reazioni calde del bot a ogni risposta; rischio e compenso dichiarati; follow-up automatici su chi si ferma; spiegazione «tre numeri» nella presentazione; esperienza e costanza spostate alla chat con l'agente (dove un «prima voglio capire» si recupera parlando).

## Decisione

**Si parte con la Bozza B** (operatore, 21/11), **candidatura a 3 passaggi** (operatore, 21/11, seconda conferma). La Bozza A resta come riferimento per un eventuale test futuro: se si vorrà provarla, basterà aggiungere il video in testa alla candidatura della B, senza cambiare i passaggi.
