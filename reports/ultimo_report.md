# ULTIMO REPORT — 2026-10-28 — Mani fetta 24: riserve cosmetiche di lexbor con i namespace come il parser (R6, chat Mani, PR #294)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #294 (https://github.com/Gasss23/Gas/pull/294): lo faccio io solo con verdetto del bot APPROVATO pulito; con riserve aspetto il tuo OK. Il merge non accende niente.
2. Accensione della lettura con lexbor: serve la chat Motore (`selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt`), poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Poi, una alla volta: R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7.

## Esito
- **PR #288 (fetta 23)**: MERGIATA su richiesta dell'operatore («mergia 288», d4b39ca). Branch ripartito da main.
- **Fetta 24 — riserve cosmetiche di lexbor**:
  - R-ve277-3 e R-529-1 (scelta della tendina): FATTA — «list of options» dello standard, optgroup disabled più vicino, solo opzioni HTML.
  - R-520-4 (title HTML in foreignObject): FATTA — primo title HTML con una discesa lineare.
  - R-540-1 (slot in foreignObject): FATTA.
  - R-ve277-4 (sonde fuori da Linux): FATTA — `attivo()` spenta subito.
  - R-526-1 (doppio controllo sotto lock) e R-528-3 (option in option): FATTA — test.
  - R-543-1 (commento su HOST): FATTA.
  - Bot #288 su 759edea (shadow vuoto): FATTA — test (testo vuoto).
  - V-1 bot e ve #288 su 6627250 (adoption agency): FATTA come limite dichiarato (commento di `shadow()` e test che fissa l'esito di oggi); il comportamento del browser non è riprodotto.
- **Review**: #547 BOCCIATO (B-547-1 MEDIA: punti d'integrazione dal solo nome, un title di svg o math poteva finire nel titolo) → namespace dedotto come il parser; #548 APPROVATO CON RISERVE (R-548-1 test, R-548-2 commento → FATTE); #549 APPROVATO.
- **Accensione lexbor (punto b)**: DEFERITA — chat Motore.

## Prove
- Web suite 566 passed / 1 skipped (Python 3.13.16 con selectolax 1.0.2; su main d4b39ca: 546 / 1).
- File lexbor su Python 3.11 senza selectolax: 22 passed / 103 skipped.
- Suite vecchia con `GAS_WEB_LEXBOR=1` (`tests/test_unit_web_leggi.py`): 11 failed / 430 passed / 1 skipped (stessi 11 di sempre).
- Mutanti presi (1 o più failed ciascuno): nascosti fuori dalla lista, optgroup disabled ignorato, optgroup annidati, lista senza visibile, linux non controllato, senza doppio controllo, integrazione senza namespace, mi anche in svg, mglyph html, svg in annotation-xml math, annotation-xml sempre html, ns ignorato nello straniero, opzione straniera contata, slot straniero contato, scorciatoia senza svg sempre, «testo» tolto, salto senza html. Equivalente noto: `continue` → `return None` su `template_fragments()` vuoto.
- Fuzz del titolo contro html5lib (1500 pagine con svg/math e punti d'integrazione, senza select e template): 3 differenze, tutte da forma diversa dell'albero tra lexbor e html5lib sugli end tag nello straniero.
- Tempi: svg con 1000 g e 10000 title 0,08 s (prima oltre 4 s, ripiego); select con 50k opzioni sotto 2000 div 1,1 s; 200k span 0,67 s.

## RICHIESTE ALLA CHAT MOTORE
1. Per accendere la lettura con lexbor e chiudere R-ve280-1:
   - `selectolax==1.0.2` in `requirements-dev.txt` (in CI girano i test lexbor oggi saltati) e in `requirements.txt` del VPS;
   - `GAS_WEB_LEXBOR=1` nell'ambiente di Gas sul VPS (Linux).
2. R-546-1: le review hanno numeri doppi tra le chat (#540–#542); dalla #547 la chat Mani usa numeri nuovi.

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
