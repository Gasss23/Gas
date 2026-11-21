# Tasto «I miei link» per i collaboratori (B) — specifica

> 21 novembre 2026. Richiesta dell'operatore: ogni collaboratore deve avere, con un click, DUE link già pronti:
> uno per il percorso completo (candidatura con domande) e uno per l'accesso diretto alla sala segnali.
> Il bot «Inizia Ora · Accesso» non è nel repo Gas: questa specifica è da consegnare a chi ne mantiene il codice.

## Cosa vede il collaboratore

Nuovo comando **/linkmiei** (e stesso contenuto dentro il Pannello + riga nella /guida). Il bot risponde:

> 🔗 **I tuoi link, {nome agente}**
>
> 🧲 **Percorso completo** — per chi è freddo: entra, risponde alle domande, ti arriva la scheda completa.
> `https://t.me/<bot>?start=<codice_agente>`
>
> ⚡ **Accesso diretto sala segnali** — per chi è già caldo: niente domande, spiegazione breve e subito l'ultimo passo (apri il conto / scrivimi).
> `https://t.me/<bot>?start=<codice_agente>-vip`
>
> Tieni premuto su un link per copiarlo, oppure inoltra una delle due card qui sotto.

Sotto, **due card già pronte da inoltrare** (una per link), con testo di presentazione e bottone, così il collaboratore non deve scrivere nulla:

- Card 1 (completo): «🎯 Vuoi entrare nella VIP di Inizia Ora? Candidati qui, 1 minuto:» [Candidati ora]
- Card 2 (diretto): «⚡ Accesso diretto alla sala segnali — segnali completi ogni giorno, gestiti in diretta:» [Entra nella sala]
- Entrambe le card portano in coda la riga: «⚠ Il trading comporta un rischio reale di perdere il capitale. L'accesso si attiva aprendo un conto col broker partner, che ci riconosce un compenso.» (V-2 verifica esterna #392: rischio e compenso dichiarati anche nei materiali che girano i collaboratori; testi da far controllare a un esperto di promozione finanziaria prima dell'uso).

## Cosa fa ciascun link

| | 🧲 Completo (`start=<codice>`) | ⚡ Diretto (`start=<codice>-vip`) |
|---|---|---|
| Percorso del lead | presentazione → domande → ultimo passo | spiegazione breve (3 righe: tre numeri, gestione in diretta, conto col broker e soldi tuoi) → SUBITO «ultimo passo»: [💬 Scrivi a {agente}] + [Apri il conto] |
| Scheda all'agente | completa | arriva comunque, campi segnati «da chiedere in chat» + etichetta ⚡ accesso diretto |
| Tracking | «Entrato da: {codice}» | «Entrato da: {codice}» (stesso conteggio nel pannello, colonna separata per capire quale link rende di più) |

## Regole

1. Il link completo è QUELLO DI OGGI: nessun cambiamento per i link già in giro.
2. Il suffisso `-vip` non attiva niente da solo: l'accesso alla sala lo dà sempre lo staff dopo il controllo del conto/deposito (come oggi col bottone «In VIP»).
3. Ogni lead resta legato all'agente del link, qualunque dei due usi.
4. /linkmiei risponde solo agli utenti registrati come agenti; agli altri: «Questo comando è per i collaboratori».
5. Nel pannello: per ogni agente il conteggio diviso per link (completo vs diretto), così si vede quale funziona.

## Perché due link

- Il collaboratore oggi ha solo il percorso completo: con un contatto già caldo (amico, cliente che arriva da una chiamata) le 7 domande sono un ostacolo inutile.
- Il link diretto è l'equivalente del «ENTRA ORA → scrivi all'umano» dei competitor, ma tracciato e con scheda.
