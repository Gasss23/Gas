# ULTIMO REPORT — 2026-10-22 — Chat Mani, fetta 8: CDATA in HTML e XHTML senza testo grezzo (R6, PR #245), secondo giro

Ramo `feat/mani-web-fetta8` da main dopo il merge di #244 (mergiata con l'ok dell'operatore: «mergia 244 e procedi con la fetta 8»). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. PR #245 (https://github.com/Gasss23/Gas/pull/245). Fetta di sicurezza.

## DECISIONI UMANE RICHIESTE

0. Sul Mac e sulla VPS controllare che il Python di Gas abbia le patch del 2025: `cd ~/Gas && .venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` deve dire True (con False Gas legge il web senza titoli, verso sicuro).

1. Merge della PR #245: l'operatore l'ha chiesto («mergia 245 e procedi con la fetta 9»), ma il check obbligatorio verifica-bot era «failure» (V-1 bot #245, MEDIA): corretta qui; il merge aspetta il nuovo giro del bot.
2. R-463-1 (MEDIA preesistente, nodo corrente come il browser) e R-ve245-1 (XHTML con prefissi): in lavorazione nella fetta 9.
3. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

## Esito

- **R-ve244-3 (CDATA in HTML)**: `FATTA` — fuori da svg/math `<![CDATA[` è un commento fasullo fino al primo `>`, come nei browser (override di `_Estrattore.parse_html_declaration`; nel ripiego lo stesso). Residuo nei punti di integrazione con un elemento HTML aperto: **R-463-1**.
- **R-ve244-2 (XHTML, script/style annidati)**: `FATTA` — in XHTML niente testo grezzo: `set_cdata_mode` senza effetto, le aperture si contano per nome; nel ripiego i nascosti e il titolo si contano, gli altri grezzi sono tag normali.
- **V-1 bot #244 (COSMETICA)**: `FATTA` — limite dichiarato nel commento del ramo TypeError.
- **R-463-1, R-463-2**: `DEFERITA — preesistenti, registrate in stato_progetto`.
- **Test**: web suite 192 → 199 (Python 3.13 e 3.11, anche con rete e DNS veri bloccati). Fuzz 0 fughe (HTML, XHTML); fuzz con oracolo html5lib, anche con atomi CDATA: 1 caso su 30k che però è visibile con gli script attivi (modello scelto nella fetta 6; il revisore concorda). Mutazioni in copie isolate: 7/7 prese.
- **Review**: #463 (chat Mani) APPROVATO CON RISERVE.

### Secondo giro (dopo il bot #245)

- **V-1 bot #245 (MEDIA)**: `FATTA` — in HTML ogni `<![` lo gestisce l'override senza super(): sugli html.parser senza le patch del 2025 `<![cdata[`, `<![temp[`, `<![if` arrivavano fino a `]]>` e il testo dello script dopo arrivava al modello. CDATA vero solo dentro svg/math e solo `<![CDATA[` esatto; ripiego allineato (chiude anche **R-463-2**).
- **R-464-1 (MEDIA preesistente, parser vecchi)**: `FATTA` — override di `close()`: un costrutto rimasto aperto a fine pagina non diventa testo.
- **R-464-2 (BASSA)**: `FATTA` — test diretto del ramo «senza fine».
- **R-465-1 (MEDIA preesistente, parser vecchi a metà pagina) e R-464-3**: `FATTA` — un html.parser senza le patch del 2025 si riconosce all'import e lì si usa sempre il ripiego (titolo perso, verso sicuro).
- **R-465-2 (BASSA)**: `FATTA` — casi `</ X`, `</1X`.
- **R-466-1, R-466-2 (BASSE), R-ve245-1…5**: `DEFERITA — registrate in stato_progetto` (R-ve245-1 nella fetta 9).
- **Test**: web suite 199 → 239 (3.13, 3.11, 3.12). Con il html/parser.py reale di CPython 3.12.3 non patchato: nessuna fuga; falliscono solo i test che si aspettano il titolo o il parser (atteso: lì si usa il ripiego). Fuzz con oracolo html5lib contro HEAD: 0 regressioni sul parser moderno.
- **Review**: #464, #465, #466 (chat Mani) APPROVATO CON RISERVE.

## Anomalie

- Un mio caso di test con template era sbagliato (per i browser lì SEGRETO è visibile): sostituito prima del commit.
- Il verdetto #463 citava righe della libreria standard nella forma path:riga e il gate B lo bloccava: il revisore l'ha riemesso (stesso esito). Il testo originale non è incollato nell'handoff perché il gate controlla anche i blocchi di codice: lì è descritto in cosa differiva.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…8» e «fetta 8, secondo giro»): aggancio di `leggi_pagina` con al modello solo `testo`, firma a finestra contaminata, tetto di chiamate, diario senza il testo della pagina, fiducia solo nei marcatori con il codice di quella chiamata; più la richiesta su `scripts/bot_esito.py` (MEDIA preesistenti citate come V-x contate come nuove), vedi blocco «Mani — fetta 7».
