# ULTIMO REPORT — 2026-10-29 — Mani fetta 25: XHTML malformato letto fino al primo errore XML (R6, chat Mani, PR #296)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #296 (https://github.com/Gasss23/Gas/pull/296): autorizzato dall'operatore («mergia 296»); lo faccio io appena i check sul nuovo head (merge di main) sono verdi.
2. Accensione della lettura con lexbor: serve la chat Motore (`selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt`), poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Poi, una alla volta: tempo di rete 12 s, R-ve235-7.

## Esito
- **PR #294 (fetta 24)**: MERGIATA su richiesta dell'operatore («mergia 294», 03dc898). Verifica esterna #294 arrivata dopo: APPROVATO CON RISERVE (commento: https://github.com/Gasss23/Gas/pull/294#issuecomment-6484098213); V-1 BASSA (test dei punti d'integrazione) → FATTA qui; V-2 BASSA e V-3 COSMETICA (stato CI nell'handoff, commit doppio della memoria) → FATTA qui (CI riportata), V-4 (merge con riserve): autorizzato dall'operatore.
- **Fetta 25 — XHTML malformato (decisione dell'operatore)**:
  - R-ve252-2 (testo prima della radice, `</html>CODA`, due radici, `<!doctype` minuscolo): FATTA — `_taglio_xml` legge fino al primo errore XML, come il browser.
  - R-ve255-1 (`<svg><title><title>` porta il corpo nella riga del titolo): FATTA — stesso taglio.
  - Entità di HTML solo coi DOCTYPE XHTML dello standard, nessun DTD scaricato, entità sconosciuta = errore; namespace controllati; BOM; pagina troncata da Gas; expat < 2.4: FATTA.
  - Test XHTML vecchi con frammenti senza radice: FATTA — input dentro `<r>…</r>`, asserzioni invariate.
  - Lettura con lexbor: SALTATA — non riguarda l'XHTML (usa sempre la lettura di sempre).
- **Review**: #550 APPROVATO CON RISERVE (R-550-1..4 → FATTE), #551 APPROVATO CON RISERVE (R-551-1 COSMETICA → FATTA in #553; R-551-2 COSMETICA → DEFERITA), #552 APPROVATO (merge di main dc43ad6, PR #292), #553 APPROVATO CON RISERVE (R-553-1 BASSA → FATTA), #554 APPROVATO, #555 APPROVATO (merge di main 4e8eb9f, PR #295).
- **Bot su e9606d8**: NON approvata per caratteri invisibili (U+FEFF) nei verdetti incollati nell'handoff → verdetti #550/#551 riemessi dal revisore: FATTA.
- **Bot su 9837d0d**: APPROVATO CON RISERVE. V-1 BASSA (test dei commenti nascosti dal taglio) → test anche senza taglio: FATTA. V-2 BASSA (DTD riletto a ogni «%p;») → letto una volta per pagina: FATTA. V-3 COSMETICA (numeri): FATTA.
- **Bot su 336e67c**: NON approvata per un carattere invisibile (BOM, Unicode Cf) scritto dal bot stesso citando i casi di test; merito APPROVATO CON RISERVE. Fix: BOM e U+200B nei test e nel codice scritti come `chr(...)`, mai come carattere: FATTA. V-1 BASSA (entità sconosciuta con DTD esterno = errore, come Firefox; Chrome dà solo un avviso) → dichiarata nella docstring di `_taglio_xml`: FATTA.
- **Review #556** APPROVATO CON RISERVE (R-556-1 COSMETICA, R-556-2 BASSA → FATTE; verdetto riemesso senza BOM), **#557** APPROVATO CON RISERVE (R-557-1 COSMETICA a capo della docstring → FATTA), **#558** APPROVATO (diff committato in c6b73cf).
- **Verifica esterna su 336e67c**: APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/296#issuecomment-6485248441). V-1 MEDIA (check del bot rosso) → stesso fix: FATTA. V-2 BASSA (= V-1 bot, Chrome tiene il resto) → dichiarata, resta aperta come scelta. V-3 COSMETICA (token singolo oltre ~2 MB, verso sicuro) → DEFERITA. V-4/V-5 informative.
- **Bot su 6a3ef69**: APPROVATO CON RISERVE (check success). V-1 BASSA (entità dichiarate nel DOCTYPE mostrate come «&foo;», preesistente) → DEFERITA alla prossima fetta, con R-551-2.
- **Verifica esterna su 6a3ef69**: APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/296#issuecomment-6485358590). V-1 BASSA (il bot può ricopiare i Cf delle righe tolte) → SALTATA, bot verde. V-2 BASSA (libexpat e accensione lexbor nei documenti durevoli) → FATTA in stato_progetto. V-3 COSMETICA → DEFERITA.
- **«mergia 296»**: GitHub ha rifiutato il merge (main avanti con la PR #297) → merge di main e106883, review #559 APPROVATO: FATTA.
- **Verifica esterna su e9606d8**: APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/296#issuecomment-6484866647). V-1 MEDIA (i BOM nell'handoff, check rosso) → FATTA. V-2 BASSA (lunghezza esatta del taglio senza test) → FATTA. V-3 COSMETICA (3.11: in CI 1 test in più che gira solo con CI=true) → spiegata. V-4/V-5 informative (R-ve280-1, libexpat sul VPS) → nelle richieste alla chat Motore.

## Prove
- Web suite 606 passed / 1 skipped anche dopo il fix dei caratteri invisibili (Python 3.13.16 con selectolax 1.0.2; su main 03dc898: 566 / 1).
- Su Python 3.11 senza selectolax: 494 passed / 113 skipped (in CI un test in più gira con CI=true).
- Suite vecchia con `GAS_WEB_LEXBOR=1`: gli stessi 11 FAIL di main (confrontati per nome).
- Kernel dopo il merge di main e106883: 1058 PASS, 1 FAIL (T31g, sqlite_vec assente nell'ambiente, noto); web + dotenv + notte 819 passed / 1 skipped.
- Mutanti presi: niente taglio, taglio all'errore senza confine, DTD mai caricato, entità saltate ok, troncato ignorato, encoding del documento, senza namespace, senza controllo versione, senza BOM, senza doppio escape, DTD riletto ogni volta, dalla seconda «%p;» non letto, taglio di un carattere in più; i 9 della verifica esterna #294 sul figlio lexbor. Difese equivalenti: «nessuna radice → 0», «pezzi che coincidono col testo», «commento senza fine tiene il resto» (html.parser lo nasconde comunque).
- Tempi: `_taglio_xml` su 1,6 MB 0,09 s; DTD delle entità costruito una volta (59 KB, 2 ms); bomba di entità fermata da expat 2.6.1.

## RICHIESTE ALLA CHAT MOTORE
1. `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (R-ve280-1), poi `GAS_WEB_LEXBOR=1` sul VPS.
2. R-546-1: numeri delle review doppi tra le chat (anche #547–#551).
3. `scripts/bot_esito.py` boccia il verdetto del bot quando il bot stesso scrive un carattere Cf citando il codice (successo due volte sulla #296): valutare di sostituirli invece di respingere.
4. Sul VPS serve libexpat ≥ 2.4 perché il taglio dell'XHTML sia attivo (sotto si legge come prima).

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
