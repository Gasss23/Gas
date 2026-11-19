# Ultimo report — 2026-11-19 — Presentazione clienti: tutte le avvertenze del catalogo d'esempio

## DECISIONI UMANE RICHIESTE
1. Merge della PR #384 (presentazione e report; il merge di main nel branch porta codice del motore già revisionato su main).
2. Prima di usare il PDF con i clienti farlo vedere a un legale: in Italia proporre al pubblico un «fondo» o rendimenti «garantiti» richiede autorizzazioni (CONSOB / Banca d'Italia).
3. Dati ancora da inserire nel PDF: nome dell'azienda e logo (oggi «NOME AZIENDA»), contatti della pagina finale.
4. Confermare: storico verificato del copy trading = 23 mesi; stop sull'equity per i clienti = 10%; citare o no «The Source Finance».

## Esito
- **PDF definitivo (18/11)**: FATTA — f6630a72 (schema semplice del matched trading, niente evidenziazioni, servizio 04 «Gruppo Privato», 9 pagine).
- **Tutte le avvertenze del catalogo d'esempio (richiesta del 19/11)**: FATTA. Dal catalogo TSF, adattate ai nostri servizi:
  - in fondo a ogni pagina la frase del catalogo: «Il trading con leva comporta il rischio di perdere il capitale. I risultati passati non sono indicativi di quelli futuri.»;
  - pagina avvertenze «Il rischio, per intero.» con 9 riquadri: perdita del capitale (Forex, oro, criptovalute, CFD con leva), solo somme di cui si può sostenere la perdita totale, risultati passati da conti di riferimento in periodi specifici, la leva amplifica, differenze tra conti (broker, spread, commissioni, swap, latenza, leva, dimensione), natura del servizio (non consulenza né gestione di patrimoni, conto intestato al cliente), conta il contratto (esempi al lordo), soggetti terzi, fonti (Myfxbook, date della pagina 6);
  - panoramica: i servizi sono diversi per natura, conto, broker e periodo, i numeri non vanno confrontati senza leggere le note;
  - numeri reali: il drawdown è «il primo numero da leggere»; copertina e chiusura: «documento riservato».
- **Merge di main nel branch** (conflitti della PR #384): conflitti solo nei report di sessione, risolti con la versione del branch; codice del motore entrato da main (#383) fatto rivedere dal revisore (vedi handoff §4).

## Test
Nessuna modifica del branch a gas.py, modules/ o tests/ (quelle presenti arrivano da main). PDF: 9 pagine; pagine modificate controllate a vista.

## Anomalie
Nessuna.
