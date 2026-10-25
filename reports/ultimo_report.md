# ULTIMO REPORT — 2026-10-25 — Mani fetta 17: R-ve261-4 chiusa col verso sicuro (R6, chat Mani, PR #270)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #270 (https://github.com/Gasss23/Gas/pull/270): mergio da solo solo con APPROVATO pulito del bot sull'head, altrimenti serve il tuo OK.
2. Prossime decisioni, una alla volta: R-ve261-2 MEDIA (noscript come testo grezzo), R-ve246-5 MEDIA, R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

## Esito
- **PR #268 (fetta 16)** — MERGIATA (85a109b). Il bot sull'head 3f4568f ha dato APPROVATO senza finding, CI verde, nessun conflitto. La verifica esterna bis ha dato APPROVATO CON RISERVE:
  - V-1 BASSA (descrizione del frameset ancora troppo larga): superata da questa fetta, ora la descrizione giusta è in `stato_progetto`;
  - V-2 COSMETICA (#514 mancante in `stato_progetto`): FATTA;
  - V-3 COSMETICA (§6 stantio): solo istantanea, nessuna azione.
- **R-ve261-4 (frameset)** — FATTA, verso sicuro per decisione dell'operatore. Dopo un `<frameset>` il resto della pagina si nasconde, sia nel parser (`_Estrattore._frameset`) sia nel ripiego, con una riga nella scatola nera.
  - Motivo: il browser mostra il frameset al posto del testo quando prima non c'è testo vero né un elemento che spegne il flag frameset-ok (br, img, hr, table, li, dd, pre, button, select, textarea, iframe, object, embed, input non hidden…). In quei casi Gas mostrava il testo.
  - Costo dichiarato: si perde testo anche dove il browser lo mostrerebbe (es. `<p>W0</p><frameset><template><svg></template>W1` perde W1).

## Prove
- Web suite: 423 (main) → 432 passed, 1 skipped, su Python 3.13.16 e 3.11. Col parser vecchio forzato: 423 passed, 10 skipped.
- Mutazioni: 7, tutte prese. Elenco reale:
  - flag mai acceso nel parser: 9 FAIL;
  - `handle_data` che lo ignora: 9;
  - prefisso invece del nome nel parser: 1;
  - ripiego senza taglio: 7;
  - prefisso nel ripiego: 1;
  - niente log nel parser: 7, sul gruppo `-k frameset`;
  - niente log nel ripiego: 7, sul gruppo `-k frameset`.
- Differenziale contro main (85a109b) e lexbor (selectolax, noscript→noembed): 180 mila pagine casuali (seed 1-3, 60 mila ciascuno) × parser e ripiego. Atomi usati: frameset in più grafie, frame, noframes, template, noscript, svg/math, br, img, table, script, commenti, attributi. Risultato: 0 fughe nuove; testo perso solo nelle pagine che contengono «frameset».

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
