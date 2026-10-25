# ULTIMO REPORT — 2026-10-25 — Mani fetta 16: riserve di #261, secondo giro (R6, chat Mani, PR #268)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #268 (https://github.com/Gasss23/Gas/pull/268): la mergio da solo solo con APPROVATO pulito del bot; altrimenti serve il tuo OK.
2. R-ve261-4 (frameset): accettarla o chiuderla. La descrizione corretta è sotto.
3. Poi, una alla volta: R-ve261-2 MEDIA, R-ve246-5 MEDIA, R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

## Esito
### Primo giro (commit fd5184b)
- **R-ve261-3** — FATTA: test con `<NOSCRIPT>` e `<NoScript>`.
- **R-ve261-6** — FATTA:
  - `con_noscript` si calcola in `_componi` sul testo intero;
  - default sicuro (R-511-1), fissato da un test (R-512-1);
  - docstring di `_Contesto` aggiornata;
  - test a pila vuota.
  - Riga di test doppia: SALTATA, perché non esiste su main.
- **R-ve261-4** — FATTA la sonda. `<p>W0</p><frameset><template><svg></template>W1` dà W0 W1 sia in Gas sia in lexbor: non è una fuga.
- **R-ve261-5** — FATTA. Per #261 le frasi giuste sono:
  - «0 fughe nuove fuori dalla classe R-ve246-5»;
  - «mutazioni prese tutte tranne quella senza `re.IGNORECASE`».

### Secondo giro (riserve di bot e verifica esterna #268)
- **V-1 bot #268** BASSA — FATTA. `_Contesto` ha ora `con_noscript: bool = True` e riceve il flag dal costruttore, sia in `_Estrattore` sia nel ripiego. Il default lo controlla un test.
- **V-2 bot #268** COSMETICA — FATTA. Il blocco «riserve rimaste dopo il merge di #261» di `stato_progetto.md` ora dice quali riserve sono chiuse.
- **V-1 ve #268** BASSA — FATTA. Numeri corretti: quelli del primo giro erano misurati prima dell'ultimo test. I numeri qui sotto sono tutti presi sul codice finale.
- **V-2 ve #268** BASSA — FATTA, descrizione del frameset corretta:
  - quando il browser usa il frameset e non mostra il testo: se `<frameset>` è preceduto solo da spazi, commenti e tag senza testo. Esempi: `<frameset>W1`, `<div></div><frameset>W1`, `<p> </p><frameset>W1`: lexbor non mostra niente, Gas mostra W1 (anche su main);
  - quando lo ignora: se prima c'è un testo non vuoto o un tag come br, img, hr, table, li. Lì lexbor mostra W1 come Gas.
- **V-3 ve #268** BASSA — FATTA: test con `<noscript class=x>` e con noscript dopo 3000 caratteri.
- **V-4 ve #268** COSMETICA — FATTA: §6 dell'handoff riscritto con lo stato reale della CI.

## Prove (tutte sul codice finale)
- Web suite: 416 (main) → 423 passed, 1 skipped, su Python 3.13.16 e 3.11. Col parser vecchio forzato: 414 passed, 10 skipped.
- Mutazioni: 12, tutte prese. Elenco reale (FAIL su 423):
  - senza `re.IGNORECASE`: 2;
  - regex `<noscript>` chiusa: 1;
  - senza guardia a pila vuota: 2;
  - flag non passato da `_componi`: 8;
  - `_componi` solo sui primi 1000 caratteri: 1;
  - ripiego solo sui primi 1000 caratteri: 1;
  - flag ignorato in `_Estrattore`: 9;
  - flag ignorato in `_Contesto`: 9;
  - flag spento nel ripiego: 13;
  - senza `con_noscript` in `chiudi`: 14;
  - default `False` in `_Estrattore`: 1;
  - default `False` in `_Contesto`: 1.
- Oracolo contro main: testo identico a main su 300 mila pagine casuali sul codice finale (seed 7-9), parser e ripiego. Più 600 mila nei passaggi precedenti. Le pagine contengono noscript in più grafie, template, svg/math, canvas/object, frameset e `&#0;`. Differenze: 0. Quindi, sulle pagine provate, 0 fughe nuove e 0 perdite nuove rispetto a main.
- I casi nuovi danno lo stesso testo di lexbor (selectolax, con noscript sostituito da noembed).

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
