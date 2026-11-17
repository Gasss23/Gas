# Ultimo report — 2026-11-17 — Presentazione clienti: PDF dell'ecosistema con i dati reali del copy trading Forex

## DECISIONI UMANE RICHIESTE
1. Prima di usare il PDF con i clienti farlo vedere a un legale: in Italia proporre al pubblico un «fondo» o rendimenti «garantiti» richiede autorizzazioni (CONSOB / Banca d'Italia). Nel PDF il servizio 1 si chiama «Rendimento Contrattuale» e la garanzia rimanda sempre al contratto.
2. PR #380 (https://github.com/Gasss23/Gas/pull/380): NON mergiare finché la presentazione non è completa, salvo decisione dell'operatore. In più oggi non è mergiabile: la CI è rossa per un problema dell'ambiente (vedi Anomalie).
3. Confermare due differenze tra quanto detto a voce e il catalogo: lo storico verificato del copy trading è di 23 mesi (16.12.2024 – 09.11.2026), non 4 anni; lo stop sull'equity è 10% al livello del copy (1 su 10) e 30% al livello 3 del conto da cui vengono i numeri. Nel PDF ho usato i dati del catalogo.
4. Decidere se nel PDF va il nome del fornitore della strategia («The Source Finance» / «TSF Forex Algo»): per ora non c'è.
5. Mandare all'agente i dati ancora mancanti: nome azienda, logo e contatti; servizio 1 (durata, ingresso minimo, pagamenti); servizio 2 (durata del ciclo); capitale minimo e orizzonte del copy trading; servizio 4.

## Esito
- **Fetta 1 — prima bozza del PDF (15 pagine, 16:9)**: FATTA — 83511a47. Stile chiaro e neutro, palette blu/verde acqua/oro validata con lo script della skill dataviz.
- **Fetta 2 — dati reali del copy trading Forex**: FATTA — 03466aae. Fonte: catalogo «The Source Finance – Catalogo servizi pre-lancio» (TSF-CAT-2026-0001), servizio 01 «TSF Forex Algo», che l'operatore usa oggi. Tenuti tutti i numeri: rendimento +165,12% in 23 mesi, max drawdown 17,92%, media mensile +4,31%, win rate 75,5%, profit factor 2,18, rendimento/DD 9,2x, 1.230 operazioni, durata media 11h 45m, rendimenti mensili 2025 (+70,35%) e 2026 (+55,59%), scheda (10 cross, TMGM, livello copy 1, livello dati 3, stop 10%/30%), condizioni (accesso gratuito, profit share 35% con high-water mark, calcolo settimanale), fonte (Myfxbook, Darwinex, 1:200, 100.000 $). Pagine nuove: numeri + curva (16 pagine in tutto), mese per mese + scheda + condizioni, rischio (livelli 1-10, righello del drawdown). Schema del meccanismo riscritto: riavvicinamento tra cross correlati. Avvertenze estese con «differenze tra conti» e «natura del copy trading». Curva di crescita calcolata dai rendimenti mensili (dà +165,1%, coerente col +165,12% Myfxbook).
- **Fetta 3 — dati dei servizi 1, 2 e 4**: DEFERITA — l'operatore deve ancora mandarli.
- **Fetta 4 — revisore / verifica esterna**: SALTATA — nessun diff nel perimetro di review né di sicurezza.
- **reports/stato_progetto.md**: non aggiornato — il task è fuori dal motore di Gas.

## Test
Nessuna modifica a gas.py/tests: suite del motore non rilanciata. Verifica del PDF: pdfinfo (16 pagine) + render a immagine di ogni pagina modificata con pdftoppm, controllate a vista.

## Anomalie
- **CI rossa per l'ambiente, non per il branch**: run 44155605928 e 44155950606, job `unit-suite`, step «web suite»: 7 failed / 747 passed, tutti test del sandbox bwrap in `tests/test_unit_web_browser.py` (es. «bwrap: execvp sleep: No such file or directory»). Il branch non tocca codice; l'ultima CI verde su main è del 12/11 → probabile cambio dell'immagine del runner GitHub. Proposta all'operatore un'attività separata per sistemarla (tocca modules/ e tests/, serve il revisore).
- Il testo con riempimento sfumato veniva reso come riquadri nel PDF: sostituito con tracciati vettoriali (fonttools + uharfbuzz, cache in `presentazione_clienti/titoli_svg.json`).
