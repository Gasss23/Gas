# ULTIMO REPORT — 2026-10-29 — Mani: `bot_esito.py` e i caratteri invisibili (fetta 28, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #305 (numero nell'handoff §0). Tocca la macchina del bot: il check `verifica-bot` sarà neutral e il merge lo decide l'operatore (anche tramite M1, che poi lo fa lui).

## Esito
- **PR #303**: MERGIATA da M1 (8424698) col sì dell'operatore dato a M1. Bot sull'ultimo head APPROVATO CON RISERVE, una BASSA (in handoff §5 il conteggio 247/1 era attribuito alla review #568, che invece misura 240/1 su un altro insieme di test): FATTA — corretto qui e in stato_progetto.
- **(c) `scripts/bot_esito.py` e i caratteri invisibili**: FATTA (PR #305).
  - Gli invisibili (categoria Cf e gli invisibili non Cf del gate, `modules/gate/gate.py:171`) si tolgono prima di titolo e gravità: «ME<U+200B>DIA» torna «MEDIA» e blocca; una citazione innocua come quella di #297 non dà più failure.
  - I controlli bidi di override e isolamento restano un NO (R-569-1).
  - Nella review pubblica ogni invisibile si vede come «<U+XXXX>».
  - Le credenziali spezzate da un invisibile non si pubblicano.
  - Review #569 (chat Mani) APPROVATO CON RISERVE (R-569-1 BASSA nuova: un controllo bidi non bloccava più; R-569-2 BASSA preesistente: gli invisibili non Cf passavano), tutte e due chiuse nel diff; review #570 APPROVATO.
- **(b) libexpat ≥ 2.4 nel doctor (gas.py)**: DEFERITA — resta a M1 finché il suo ponte voce non è mergiato.

## Prove
- `tests/test_unit_verifica_bot.py`: 342 passed.
- Mutanti, tutti presi: senza lo strip in decidi 10 failed; senza l'escape nel corpo 2; senza lo strip in contiene_segreti 3; senza il blocco bidi 4; senza gli intervalli non Cf 6.
- Nei due file, 0 caratteri Cf scritti in chiaro.

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
