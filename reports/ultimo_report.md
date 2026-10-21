# ULTIMO REPORT — 2026-10-21 — Chat Mani, fetta 5: riserve rimaste della lettura web (R6)

Ramo `feat/mani-web-fetta5` da main dopo il merge di #239. Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. Fetta di sicurezza. PR #242. Operatore: «procedi con la fetta 5».

## DECISIONI UMANE RICHIESTE

1. Merge della PR #242 (https://github.com/Gasss23/Gas/pull/242): vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

## Esito

- **R-442-1 / R-431-3 (contenuto dei nascosti non grezzi, annidamento)**: `FATTA` — contatore unico come `_Estrattore`: dentro svg, math, noscript, template, object, canvas si leggono i tag, quindi «</svg>» in un attributo o in un commento non chiude.
- **R-442-2 (commenti fasulli)**: `FATTA` — `<!x`, `<?`, `</` senza lettera finiscono al primo «>», `<![CDATA[` a «]]>», in un'unica ricerca lineare. Tolta la regex finale `<[^<>]*>`: cancellava solo testo vero («a < b»).
- **V-1 bot #239 (`<svg/>` autochiuso)**: `FATTA` — svg e math autochiusi non aprono; la «/» di un valore senza virgolette (`<svg a=x/>`) non conta. Senza gruppi di cattura: in Python 3.11 dentro una ripetizione possessiva danno SystemError.
- **V-1 bot #239 2° giro (virgolette nella chiusura)**: `FATTA` — anche il tag di chiusura finisce al suo «>» fuori dalle virgolette.
- **R-445-1 (grezzi del parser)**: `FATTA` — textarea, xmp, noembed, noframes, plaintext grezzi come in html.parser; un grezzo autochiuso fra i nascosti conta come apertura.
- **R-446-1 (percorso normale)**: `FATTA` — `<script/>` e gli altri nascosti autochiusi (non svg/math) aprono come nei browser: prima html.parser li trattava come vuoti e il testo dopo (codice invisibile nel browser) arrivava al modello.
- **R-432-1 / V-3 ve #239 / V-2 bot #239 2° giro**: `FATTA` — ramo morto tolto, test «a<script», docstring e commento dei test corretti.
- **Test**: web suite 137 → 167 (166 al primo giro) (Python 3.13 e 3.11, anche con rete e DNS veri bloccati), con un test di confronto col parser su 4000 pagine casuali. Fuzz differenziale: 0 fughe su 500k pagine (3.13) e 300k (3.11). Mutazioni in copie isolate: tutte prese.
- **Review**: #445 → #446 → #447 (chat Mani), APPROVATO CON RISERVE (ciascuna ha chiuso la riserva della precedente).
- **V-1 bot #242 / V-1 verifica esterna #242 (contatore unico)**: `FATTA` — contatore per nome nel parser e nel ripiego: una chiusura scala solo un'apertura con lo stesso nome (in `<svg>X</script>Y` Y è invisibile per i browser e non arriva più al modello); chiude anche la parte (a) di R-447-1. Test 166 → 167. Review #448 (chat Mani) APPROVATO CON RISERVE (R-448-1 COSMETICA, R-448-2 di registro).
- **Bot #242**: APPROVATO CON RISERVE (verifica-bot success), solo V-1 BASSA, chiusa sopra. **Verifica esterna #242**: APPROVATO CON RISERVE: V-1 = V-1 bot; V-2 BASSA (commenti vuoti su 3.11) registrata; V-3 COSMETICA (SystemError dei gruppi di cattura su 3.11 non riprodotto dal verificatore: l'agente l'ha visto sul pattern vero, il commento resta); V-4 COSMETICA §6 aggiornato.
- Restano **R-447-1** parte (b) BASSA e **R-448-1** COSMETICA, dichiarate in `reports/stato_progetto.md`.

## Anomalie

- Nessuna. Nota: html.parser di Python 3.11 non riconosce i commenti vuoti `<!-->`/`<!--->` (i browser e il 3.13 sì): il test di confronto esclude quelle pagine.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…5»): aggancio di `leggi_pagina` con al modello solo `testo`, firma a finestra contaminata, tetto di chiamate, diario senza il testo della pagina, fiducia solo nei marcatori con il codice di quella chiamata.
