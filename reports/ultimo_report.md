# ULTIMO REPORT — 2026-10-25 — Mani fetta 16: riserve di #261 (R6, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #268 (https://github.com/Gasss23/Gas/pull/268): mergio da solo solo con APPROVATO pulito del bot, altrimenti serve il tuo OK.
2. R-ve261-4 (frameset): proposta di accettarla (vedi sotto). Poi, una alla volta: R-ve261-2 MEDIA, R-ve246-5 MEDIA, R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

## Esito
- **R-ve261-3** — FATTA. In `test_chiusura_del_template_sopra_svg_math` ci sono due pagine con `<NOSCRIPT>` e `<NoScript>`; il mutante senza `re.IGNORECASE` ora fa 2 FAIL.
- **R-ve261-6** — FATTA.
  - `con_noscript` si calcola una volta in `_componi` sul testo intero e passa al costruttore di `_Estrattore`; tolto l'override di `feed`.
  - Il default è `True`, cioè il verso sicuro (R-511-1 del revisore). Lo fissa un test nuovo (R-512-1).
  - Docstring di `_Contesto` aggiornata.
  - Due pagine con `</template>` in più a pila vuota: il mutante senza la guardia `and self._template_fuori` fa 2 FAIL.
  - Riga di test doppia: SALTATA — su main non c'è, compare una sola volta (V-4(b) della verifica esterna #261 era un falso positivo, confermato dal revisore #511).
- **R-ve261-4** — FATTA la sonda, decisione all'operatore.
  - `<p>W0</p><frameset><template><svg></template>W1` dà W0 W1 sia in Gas sia in lexbor: dopo il testo W0 il browser ignora `<frameset>`. Non è una fuga.
  - La classe resta solo con `<frameset>` prima di ogni testo: `<frameset>W1` in lexbor non mostra niente, Gas mostra W1 (anche su main).
  - Proposta: accettarla. Le pagine con frameset sono obsolete e il testo della pagina Gas lo tratta già come non fidato. Chi scrive la pagina può mettere lo stesso testo in chiaro, quindi non guadagna nessuna capacità nuova.
- **R-ve261-5** — FATTA. Le frasi giuste per #261 sono:
  - fughe: «0 fughe nuove fuori dalla classe R-ve246-5» (non «0 fughe nuove (4 casi R-ve246-5)»);
  - mutazioni: «prese tutte tranne quella senza `re.IGNORECASE` su `_NOSCRIPT`» (chiusa ora da R-ve261-3).
  - In questa fetta valgono le frasi esatte qui sotto.

## Prove (codice finale)
- Web suite: 416 → 421 passed, 1 skipped, su Python 3.13.16 e 3.11. Col parser vecchio forzato (`_PARSER_AGGIORNATO=False`): 411 passed, 10 skipped.
- Mutazioni, tutte prese (elenco reale, FAIL per mutante):
  - senza `re.IGNORECASE`: 2;
  - senza guardia a pila vuota: 2;
  - flag non passato da `_componi`: 8;
  - flag ignorato nel costruttore: 11;
  - flag spento nel ripiego: 11;
  - senza `con_noscript` in `chiudi`: 11;
  - default `False`: 1.
- Oracolo contro main: testo identico a main su 600 mila pagine casuali (300 mila sul codice finale, 300 mila sul primo diff, prima del default `True`), parser e ripiego, con noscript in più grafie, template, svg/math, canvas/object, frameset e `&#0;`: 0 differenze. Quindi, sulle pagine provate, 0 fughe nuove e 0 perdite nuove rispetto a main, senza eccezioni.
- I casi nuovi danno lo stesso testo di lexbor (selectolax, con noscript sostituito da noembed).
- Review: #511 APPROVATO CON RISERVE (R-511-1), #512 APPROVATO CON RISERVE (R-512-1), #513 APPROVATO. Le due riserve sono chiuse in questa PR.

## Anomalie
- `gh` non autenticato nel cloud (GH_TOKEN rifiutato): PR, etichetta e stato CI passano dall'integrazione GitHub.
