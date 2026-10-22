# ULTIMO REPORT — 2026-10-22 — Chat Mani, fetta 8: CDATA in HTML e XHTML senza testo grezzo (R6, PR #245)

Ramo `feat/mani-web-fetta8` da main dopo il merge di #244 (mergiata con l'ok dell'operatore: «mergia 244 e procedi con la fetta 8»). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. PR #245 (https://github.com/Gasss23/Gas/pull/245). Fetta di sicurezza.

## DECISIONI UMANE RICHIESTE

1. Merge della PR #245: vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore.
2. R-463-1 (MEDIA preesistente) richiede di tracciare il nodo corrente come il browser (stesso lavoro di R-450-1 e V-2 ve #243): fetta dedicata?
3. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

## Esito

- **R-ve244-3 (CDATA in HTML)**: `FATTA` — fuori da svg/math `<![CDATA[` è un commento fasullo fino al primo `>`, come nei browser (override di `_Estrattore.parse_html_declaration`; nel ripiego lo stesso). Residuo nei punti di integrazione con un elemento HTML aperto: **R-463-1**.
- **R-ve244-2 (XHTML, script/style annidati)**: `FATTA` — in XHTML niente testo grezzo: `set_cdata_mode` senza effetto, le aperture si contano per nome; nel ripiego i nascosti e il titolo si contano, gli altri grezzi sono tag normali.
- **V-1 bot #244 (COSMETICA)**: `FATTA` — limite dichiarato nel commento del ramo TypeError.
- **R-463-1, R-463-2**: `DEFERITA — preesistenti, registrate in stato_progetto`.
- **Test**: web suite 192 → 199 (Python 3.13 e 3.11, anche con rete e DNS veri bloccati). Fuzz 0 fughe (HTML, XHTML); fuzz con oracolo html5lib, anche con atomi CDATA: 1 caso su 30k che però è visibile con gli script attivi (modello scelto nella fetta 6; il revisore concorda). Mutazioni in copie isolate: 7/7 prese.
- **Review**: #463 (chat Mani) APPROVATO CON RISERVE.

## Anomalie

- Un mio caso di test con template era sbagliato (per i browser lì SEGRETO è visibile): sostituito prima del commit.
- Il verdetto #463 citava righe della libreria standard nella forma path:riga e il gate B lo bloccava: il revisore l'ha riemesso (stesso esito). Il testo originale non è incollato nell'handoff perché il gate controlla anche i blocchi di codice: lì è descritto in cosa differiva.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…8»): aggancio di `leggi_pagina` con al modello solo `testo`, firma a finestra contaminata, tetto di chiamate, diario senza il testo della pagina, fiducia solo nei marcatori con il codice di quella chiamata; più la richiesta su `scripts/bot_esito.py` (MEDIA preesistenti citate come V-x contate come nuove), vedi blocco «Mani — fetta 7».
