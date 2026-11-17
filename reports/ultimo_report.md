# Ultimo report — 2026-11-17 — Presentazione clienti (versione 3, stile HUD) + CI rossa su Ubuntu 26.04

## DECISIONI UMANE RICHIESTE
1. Prima di usare il PDF con i clienti farlo vedere a un legale: in Italia proporre al pubblico un «fondo» o rendimenti «garantiti» richiede autorizzazioni (CONSOB / Banca d'Italia).
2. PR #380 (https://github.com/Gasss23/Gas/pull/380): contiene sia la correzione della CI (motore: modules/web, tests) sia la presentazione. La correzione va mergiata presto (sblocca la CI di tutte le PR); la presentazione è ancora una bozza con segnaposto. Merge secondo la regola di CLAUDE.md §10 (verdetto del bot di verifica sull'head + CI verde); la PR contiene anche la presentazione in bozza, quindi serve comunque il sì dell'operatore.
3. Confermare: storico verificato del copy trading = 23 mesi (non 4 anni); stop sull'equity 10% al livello del copy (30% solo al livello 3 del conto dei dati).
4. Decidere se citare nel PDF il fornitore della strategia («The Source Finance» / «TSF Forex Algo»).
5. Valutare se fissare in CI `runs-on: ubuntu-26.04` (suggerimento del revisore, tocca ci.yml: decisione dell'operatore).
6. Dati ancora mancanti: nome azienda, logo, contatti; servizio 1 (durata, ingresso minimo); servizio 2 (durata del ciclo); servizio 4.

## Esito
- **Fetta 1 — prima bozza del PDF (15 pagine)**: FATTA — 83511a47.
- **Fetta 2 — dati reali del copy trading Forex (catalogo TSF, servizio 01)**: FATTA — 03466aae.
- **Fetta 3 — versione 3 del PDF: stile HUD «tipo Jarvis», 8 pagine, linguaggio per chi investe la prima volta**: FATTA — b020cbfa. Per ogni servizio prima «cos'è» e «come funziona» in parole semplici (matched trading con lo schema dei due conti; copy trading con l'esempio dell'elastico), poi i numeri. Tutti i numeri del catalogo tenuti (pagina «I numeri reali»: curva, tabella mensile, win rate, profit factor, rendimento/DD, operazioni, fonte e condizioni). Palette HUD: ciano/verde/oro (validatore dataviz: normale ok, daltonismo 7,7 nella fascia ammessa con codifica secondaria — numero e nome del servizio sempre accanto al colore).
- **Fetta 4 — CI rossa (attività «Fix CI web suite: bwrap sandbox tests fail», richiesta dall'operatore in sessione)**: FATTA nel codice, DA CONFERMARE sulla CI vera. Causa: `ubuntu-latest` passato da 24.04 a 26.04 tra il 12 e il 17/11; su 26.04 i coreutils di /usr/bin sono collegamenti a file fuori dalle cartelle permesse del sandbox → 7 test bwrap rossi. Correzione in `modules/web/browser.py` (`_programmi_fuori`) + test. Riprodotto in locale simulando il layout 26.04: prima 7 failed, dopo `tests/test_unit_web_*.py` 642 passed, 114 skipped (selectolax assente in locale) sia sul layout simulato sia su quello normale. Review #803 (chat practical-tesla) APPROVATO CON RISERVE (R-803-1..5 BASSE/COSMETICHE) → riserve applicate → #804 APPROVATO CON RISERVE (R-804-1 MEDIA: due casi del test resi vacui dal nuovo filtro +x; R-804-2 COSMETICA) → corretti → #805 APPROVATO, nessuna riserva aperta (verdetti integrali nell'handoff §4). Commit 605e154c.
- **Fetta 5 — dati dei servizi 1, 2 e 4**: DEFERITA — l'operatore deve ancora mandarli.

## Test
Motore: `tests/test_unit_web_*.py` 640 passed / 114 skipped (prima, layout normale) → 642 passed / 114 skipped (dopo, 2 test nuovi), con GAS_TEST_BROWSER_OBBLIGATORIO=1; sul layout 26.04 simulato 37 passed / 7 failed (prima, solo browser) → 642 passed / 114 skipped (dopo). PDF: 8 pagine, controllate a vista una per una.

## Anomalie
- La correzione è provata su un layout 26.04 simulato, non sul runner vero: la CI va chiusa solo quando lo step «Run web suite» è verde sulla run del branch (condizione del revisore).
- Il testo sfumato del PDF è reso con tracciati vettoriali (fonttools + uharfbuzz installati nella cartella di lavoro temporanea, non nel repo; cache in `presentazione_clienti/titoli_svg.json`).
