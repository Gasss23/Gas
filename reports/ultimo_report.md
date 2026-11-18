# Ultimo report — 2026-11-18 — Presentazione clienti: versione definitiva (9 pagine)

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa sessione (solo presentazione e report: nessun file del motore).
2. Prima di usare il PDF con i clienti farlo vedere a un legale: in Italia proporre al pubblico un «fondo» o rendimenti «garantiti» richiede autorizzazioni (CONSOB / Banca d'Italia).
3. Dati ancora da inserire nel PDF: nome dell'azienda e logo (oggi «NOME AZIENDA»), contatti della pagina finale.
4. Confermare: storico verificato del copy trading = 23 mesi; stop sull'equity per i clienti = 10%; citare o no «The Source Finance».

## Esito
- **Separare la correzione della CI in un'altra PR (richiesta dell'operatore)**: SALTATA — non più possibile né necessaria: la PR #380 (correzione della CI + PDF v3) era già stata mergiata dall'operatore il 18/11 alle 17:00. La correzione è in main e lo step «Run web suite» è verde su ubuntu-26.04 vera (run 44187987070). Branch di sessione ripartito da main aggiornato (381f5d3d), come da regola.
- **PDF definitivo**: FATTA.
  - Servizio 02 (matched trading): nuovo schema semplice — 3.000 € → conto A (prop firm, punta sul rialzo) e conto B (broker, punta sul ribasso) → «una delle due vince sempre» → ≈ +500 € in media.
  - Testo evidenziato: tolte le parole in grassetto dentro i paragrafi; i titoli sfumati ora sono tutti ciano (prima metà parola bianca); i segnaposto rimasti (contatti) sono testo tenue, non più riquadri tratteggiati.
  - Servizio 04 «Gruppo Privato» su una sola pagina, come gli altri: gruppo privato dove scriviamo noi cosa, quando e come; il cliente copia in 30 secondi sul suo conto, in autonomia; guida PDF inclusa per chi parte da zero; esempio di messaggio. Aggiunto alla panoramica, alla copertina e alle avvertenze (indicazioni uguali per tutti, non consulenza personalizzata).
  - Servizio 01: tolte le righe «da inserire» (durata, ingresso minimo) al posto delle quali ora ci sono pagamenti e garanzie «scritti nel contratto».
  - 9 pagine, controllate a vista una per una.
- **reports/stato_progetto.md**: la riga della CI rossa ora è CHIUSA, con le note della verifica esterna #380 (V-2 BASSA, V-4 COSMETICA).

## Test
Nessuna modifica a gas.py, modules/ o tests/. PDF: pdfinfo 9 pagine; render a immagine di ogni pagina modificata.

## Anomalie
- La PR #380 è stata mergiata mentre in chat la proponevo di dividere: nessun danno, la correzione della CI era già approvata e verde.
