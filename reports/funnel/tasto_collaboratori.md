# Tasto «I miei link» nel Pannello — specifica pronta da applicare

> 21 novembre 2026, seconda stesura dopo la decisione dell'operatore: il tasto vive nel PANNELLO
> (il bottone blu in basso a sinistra nella chat del bot «Inizia Ora · Accesso»), più /linkmiei come scorciatoia in chat.
> Tutto riusa ciò che il bot ha già: codice agente, tracking «Entrato da», scheda lead, pannello.

## 1. Cosa vede il collaboratore nel Pannello

Nuova voce/scheda **«🔗 I miei link»** (in cima o accanto a «I tuoi lead»). Dentro, due blocchi:

**🧲 Percorso completo** — *per chi è freddo: domande + scheda completa*
`https://t.me/<bot>?start=<codice_agente>`
[Copia] [Inoltra la card]

**⚡ Sala segnali diretto** — *per chi è già caldo: niente domande, subito l'ultimo passo*
`https://t.me/<bot>?start=<codice_agente>-vip`
[Copia] [Inoltra la card]

Sotto: contatore per link («Completo: N lead · Diretto: M lead»), così ogni agente vede quale rende.

«Inoltra la card» manda nella chat del bot un messaggio già pronto che l'agente INOLTRA al contatto (zero testi da scrivere):

- Card COMPLETO: «🎯 Vuoi entrare nella VIP di Inizia Ora? Candidati qui, ci vuole 1 minuto:» + bottone [Candidati ora] → link completo
- Card DIRETTO: «⚡ Accesso diretto alla sala segnali di Inizia Ora — segnali completi ogni giorno, gestiti in diretta:» + bottone [Entra nella sala] → link diretto
- In coda a ENTRAMBE: «⚠ Il trading comporta un rischio reale di perdere il capitale. L'accesso si attiva aprendo un conto col broker partner, che ci riconosce un compenso.»

## 2. /linkmiei (scorciatoia in chat, stesso contenuto)

Risponde SOLO agli agenti registrati (agli altri: «Questo comando è per i collaboratori»). Stesso testo dei due blocchi + le due card. Aggiungere una riga alla /guida: «4bis. I tuoi due link: /linkmiei o Pannello → I miei link».

## 3. Cosa fa il link diretto (`start=<codice>-vip`)

1. Stessi passi di oggi fino alla lingua/18 anni (obbligatori), POI NIENTE domande: un solo messaggio breve —
   > «⚡ Benvenuto, {nome}. Sala segnali VIP: ogni giorno i segnali completi — dove entrare, dove fermarti, dove incassare — gestiti in diretta. Non paghi nessun abbonamento: l'accesso si attiva aprendo il conto dal nostro link col broker partner (è così che veniamo pagati). I soldi restano sul tuo conto. ⚠ Il trading comporta un rischio reale di perdere il capitale. Ultimo passo: scrivi a {agente}, ti attiva lui.»
   > [💬 Scrivi a {agente}] e, sotto, «Ti va di ricevere qui aggiornamenti della community?» [Sì, volentieri] [No grazie]
2. La scheda lead arriva all'agente COME OGGI, con etichetta «⚡ accesso diretto» e i campi non raccolti segnati «da chiedere in chat».
3. L'accesso alla sala lo dà sempre lo staff come oggi («Conto aperto» / «In VIP»): il suffisso -vip NON attiva nulla da solo.

## 4. Regole d'innesto (per chi implementa)

1. Il link completo è QUELLO DI OGGI: nessun cambiamento per i link già in giro; il diretto è solo un suffisso in più sullo stesso parametro `start`.
2. Ogni lead resta legato all'agente del link, qualunque dei due usi; «Entrato da: {codice}» come oggi, più il flag completo/diretto per i contatori.
3. Se non preme «Scrivi a {agente}», partono i 2 solleciti del **caso B** di `funnel_v2.md` (regole comuni): «Ti manca solo l'ultimo passo…» a +24 h, «Vuoi fare l'ultimo passo o chiudo qui?» a +72 h. Il diretto ha solo quel caso (non c'è una candidatura da completare).
4. Niente altri schermi nuovi: la voce del Pannello è una lista con 2 link e 2 bottoni d'inoltro.
5. Le tutele valgono ANCHE nel percorso diretto (V-1 verifica esterna #392, secondo giro): conferma 18 anni e lingua restano obbligatorie (passo 3.1), la riga sul rischio e quella sul compenso del broker stanno nel messaggio unico, il consenso aggiornamenti resta coi bottoni Sì/No. Il link diretto accorcia le domande, MAI le tutele.

## 5. Perché due link

Il collaboratore oggi ha solo il percorso completo: con un contatto già caldo (amico, cliente da una chiamata) le domande sono un ostacolo inutile. Il diretto è l'equivalente dell'«ENTRA ORA → scrivi all'umano» dei competitor, ma tracciato e con scheda.
