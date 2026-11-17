# Ultimo report — 2026-11-17 — Presentazione clienti: prima bozza del PDF dell'ecosistema

## DECISIONI UMANE RICHIESTE
1. Prima di usare il PDF con i clienti farlo vedere a un legale: in Italia proporre al pubblico un «fondo» o rendimenti «garantiti» richiede autorizzazioni (CONSOB / Banca d'Italia). Nel PDF il servizio 1 si chiama «Rendimento Contrattuale» e la garanzia rimanda sempre al contratto.
2. PR #380 (https://github.com/Gasss23/Gas/pull/380): NON mergiare finché la presentazione non ha i dati reali, salvo decisione dell'operatore.
3. Mandare all'agente: PDF d'esempio, nome azienda/logo/contatti, dati dei servizi 1-3 (durata, ingresso minimo, pagamenti, durata del ciclo, storico mensile del copy trading e sua fonte), descrizione del servizio 4.

## Esito
- **Fetta 1 — prima bozza del PDF (15 pagine, 16:9)**: FATTA — 83511a47. Copertina, chi siamo, ecosistema, confronto, 2 pagine per i servizi 1 e 2, 3 pagine per il servizio 3 (meccanismo, numeri e rischio, storico segnaposto), servizio 4 segnaposto, come iniziare, avvertenze, contatti. Grafici: crescita di 10.000 € al 20%, scaglioni da 3.000 €, schema illustrativo del ritorno alla media, righello del rischio (17% drawdown storico, equity stop 30%). Palette blu/verde acqua/oro validata con lo script della skill dataviz (tutti i controlli PASS). Pagine controllate a vista una per una.
- **Fetta 2 — dati reali nel PDF**: DEFERITA — l'operatore deve ancora mandarli (bozza richiesta come «prova»).
- **Fetta 3 — revisore / verifica esterna**: SALTATA — nessun diff nel perimetro di review (motore o macchina di controllo), né di sicurezza.
- **reports/stato_progetto.md**: non aggiornato — il task è fuori dal motore di Gas.

## Test
Nessuna modifica a gas.py/tests: suite del motore non rilanciata. Verifica del PDF: pdfinfo (15 pagine, 960x540 pt) + render a immagine di ogni pagina con pdftoppm.

## Anomalie
- Il testo con riempimento sfumato (background-clip:text e <text> SVG sfumato) veniva reso come riquadri/rettangoli nel PDF: sostituito con tracciati vettoriali generati da fonttools+uharfbuzz (cache in `presentazione_clienti/titoli_svg.json`, così il build gira anche senza quelle librerie).
- Il comando per pulire le anteprime con `rm -f $P/*` è stato bloccato dal controllo di sicurezza; rifatto con path letterale, nessuna cancellazione nel repo.
