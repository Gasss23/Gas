# ULTIMO REPORT — 2026-10-26 — Mani fetta 18: noscript testo grezzo, R-ve261-2 chiusa (R6, chat Mani, PR #272)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #272 (https://github.com/Gasss23/Gas/pull/272): la mergio da solo solo con APPROVATO pulito del bot sull'head, altrimenti serve il tuo OK.
2. Prossime decisioni, una alla volta: R-ve246-5 MEDIA (canvas/object, costruttore HTML5), R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7 (proposta: accettarla). Più, da valutare con l'oracolo: R-518-1 (guardia `_nascosti_html`) e la riaccensione della regola R-469-1 nelle pagine con noscript.

## Esito
- **PR #270 (fetta 17)** — MERGIATA dall'operatore («mergia», 9924438) con il bot APPROVATO CON RISERVE (V-1 BASSA: test mancante; V-2 COSMETICA: descrizione della PR, aggiornata prima del merge). Il titolo della PR, troncato dall'integrazione (`<frameset>` tolto come HTML), è stato corretto prima del merge.
- **R-ve261-2 (noscript)** — FATTA:
  - `<noscript>` è testo grezzo fino a `</noscript>`, nel parser (`_modo_grezzo`) e nel ripiego (`_GREZZI_RIPIEGO`), come nel browser con gli script attivi. In XHTML e dentro svg/math resta un elemento.
  - Prudenza concordata: la protezione `con_noscript` resta accesa.
  - Esempio: `<template><noscript></template>T1</noscript>T2` ora nasconde T2, come il browser.
  - Chiusa anche una fuga di main: `<p>W0</p><object><noscript></object>W1</noscript>W2</object>W3` mostrava W2.
  - Tre test codificavano il vecchio verso sicuro: ora mostrano il testo che il browser con gli script attivi mostra (verificato con lexbor).
  - Costo noto: `<p>W0</p><svg><font color=r><noscript></svg>W1</noscript>W2` ora perde W2, che lexbor mostra (la stessa perdita c'è già senza `</svg>`).
- **V-1 bot #270 (test del titolo quando «frameset» non è un tag)** — FATTA.
- **Review**:
  - #517 APPROVATO CON RISERVE: R-517-1 COSMETICA (commento della guardia `_nascosti_html`) → FATTA.
  - #518 APPROVATO CON RISERVE: **R-518-1** BASSA → DEFERITA. La guardia `_nascosti_html` per canvas fa perdere testo che il browser mostra e nessun test la fissa. Va decisa con l'oracolo; tracciata in `stato_progetto`.

## Prove
- Web suite: 433 (main) → 441 passed, 1 skipped, su Python 3.13.16 e 3.11. Col parser vecchio forzato: 431 passed, 11 skipped.
- Mutazioni, tutte prese (FAIL su 441):
  - parser senza noscript grezzo: 7;
  - grezzo anche in svg/XHTML (`HTMLParser.set_cdata_mode` diretto): 2;
  - ripiego senza noscript grezzo: 7;
  - titolo scartato per sottostringa «frameset» (mutante del bot #270): 1.
- Differenziale contro main (9924438) e lexbor (selectolax, noscript→noembed): 180 mila pagine casuali (seed 1-3) × parser e ripiego. Atomi usati: noscript in più grafie, template, svg/math, script, commenti, textarea, title, object, attributo con «</noscript>», frameset, table.
  - Oracolo corretto: niente atomi noembed, che si confondono col proxy; textarea visibile; riga Titolo esclusa.
  - Risultato: 0 fughe nuove. Perdite in 40 uscite su 360 mila, di cui 38 tolgono testo che anche lexbor nasconde.

## Anomalie
- Un primo giro del differenziale aveva dato «fughe» che erano artefatti dell'oracolo (atomi `</noembed>` dentro il noscript sostituito, textarea e titolo contati come nascosti); corretto e rifatto, 0 fughe.
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
