# Ultimo report — 2026-10-25 — Chat Mani: riserve rimaste dopo il merge di #261 salvate prima del /clear

## DECISIONI UMANE RICHIESTE

1. Merge della PR #267 (solo `reports/`): la mergio da sola la chat Mani se il bot dà APPROVATO pulito; altrimenti serve il tuo OK.
2. PR #263 (chat Notte, `/clear` da Telegram): check tutti verdi, bot APPROVATO CON RISERVE (solo BASSE) → serve il tuo OK esplicito per il merge.
3. Decisioni aperte della mia area (già in `reports/stato_progetto.md`): R-ve261-2 MEDIA (noscript come testo grezzo), R-ve252-2 / R-ve255-1 (XHTML malformato), R-ve246-5 MEDIA (canvas/object, costruttore HTML5), tempo di rete 12 s, R-ve235-7 (proposta: accettarla).

## Esito

- **Salvataggio delle riserve finali di #261**: FATTA. In `reports/stato_progetto.md` un blocco nuovo sotto «Mani — fetta 15» registra con id le riserve del bot #261 sul commit finale 5e704c0 (recensione https://github.com/Gasss23/Gas/pull/261#pullrequestreview-5640696945), che prima stavano solo nella recensione: R-ve261-3 BASSA (test `<NOSCRIPT>` maiuscolo mancante), R-ve261-4 BASSA preesistente (frameset), R-ve261-5 COSMETICA (frasi imprecise in ultimo_report/PR #261), R-ve261-6 COSMETICA (`con_noscript` in `feed`, docstring, test doppio).
- **Secondo giro (bot #267 APPROVATO CON RISERVE)**: FATTA. V-1 BASSA (descrizione della PR imprecisa sui file): descrizione corretta. V-2 COSMETICA: aggiunti a R-ve261-5 il §5 dell'handoff di #261 e a R-ve261-6 il mutante innocuo senza la guardia `_template_fuori` (V-4(c) verifica esterna #261).
- **Chiusura di quelle riserve**: DEFERITA — si fanno nella prossima fetta Mani, quando l'operatore la chiede.
- **Merge della PR #263**: SALTATA — non è della chat Mani e ha riserve: decide l'operatore.

## Anomalie

Nessuna. Codice non toccato; nessun file del perimetro di review nel diff.
