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
- **Bot su e4559ef (PR #305)**: NO, check verifica-bot failure. V-1 MEDIA (togliere un invisibile tra due parole le incollava e la gravità non si vedeva: regressione del mio 57e927d, riprodotta): FATTA in 95249a8 — un invisibile attaccato a una parola di gravità dà NO. V-2 BASSA (le categorie del gate non c'erano): FATTA. V-3 COSMETICA (tetto prima dell'escape): FATTA.
- **Verifica esterna su e4559ef (https://github.com/Gasss23/Gas/pull/305#issuecomment-6506076785)**: BOCCIATO. V-1 MEDIA (la stessa del bot, con «ALTA<U+2800>x»): FATTA in 95249a8. V-2 BASSA («più severo di prima» non è vero per un Cf lontano dalle gravità): FATTA — descrizione corretta, il comportamento è voluto. V-3 BASSA (il mutante «senza escape» dipende da come si muta): SALTATA — solo un'osservazione sul numero. V-4 COSMETICA: FATTA con la V-3 del bot.
- **Review #571 (chat Mani)**: BOCCIATO — due letture fisse (invisibili tolti / come spazio) non coprivano due invisibili insieme, e togliere più categorie incollava nuovi separatori. **Review #572**: APPROVATO CON RISERVE con R-572-1 e R-572-2, BASSE preesistenti (vedi stato_progetto).
- **Bot su 95249a8 (PR #305)**: NO, failure dato in automatico dal bot_esito.py di main perché il bot ha scritto un Cf nel verdetto (lo stesso difetto che questa PR corregge). Finding veri, riprodotti: V-1 MEDIA (credenziali spezzate da un controllo C0: json.dumps le scrive come «\u001b» e lo strip non le vedeva): FATTA in aec5c39 — ricerca anche su ogni stringa ripulita, chiavi comprese. V-2 BASSA (togliere un invisibile toglieva un confine di parola fuori dalle gravità, «V-1<U+200B>x (alta)»): FATTA in aec5c39 — gravità anche sul testo grezzo. V-3 MEDIA (handoff fermo a 57e927d): FATTA — vera solo su 95249a8, superata da d672021.
- **Bot su d672021 (PR #305)**: BOCCIATO. V-1 MEDIA («R-9-1<inv>V-1 (ALTA)»: tolto l'invisibile diventava la citazione di una riserva registrata e l'ALTA spariva): FATTA in aec5c39 (lettura grezza), test in ca222c6.
- **Verifica esterna su d672021 (https://github.com/Gasss23/Gas/pull/305#issuecomment-6506619129)**: BOCCIATO. V-1 MEDIA (la stessa del bot, più «V-1<U+200B>b — grave», «è<U+2800>F-1(media)»): FATTA in aec5c39, provata su ca222c6 (tutti NO). V-2 MEDIA (credenziali C0): FATTA in aec5c39. V-3 BASSA (falsi NO prudenti): SALTATA — voluti, verso sicuro. V-4 BASSA (§6 non diceva il failure su 95249a8): FATTA — qui. V-5 COSMETICA (tempo su 1 MB di invisibili; «<U+200B>» scritto a mano dal bot si confonde con un vero U+200B): SALTATA — irrilevante per verdetti normali.
- **Review #573 (chat Mani)**: BOCCIATO (ricostruendo il dict, due chiavi ripulite si fondevano e la credenziale spariva). **#574**: APPROVATO CON RISERVE (R-574-1 BASSA ricorsione → FATTA in ca222c6; R-574-2 COSMETICA: il mutante «senza stringa per stringa» dà 6 failed, non 5 → FATTA, corretto qui). **#575**: APPROVATO CON RISERVE (R-575-1 BASSA preesistente, R-575-2 COSMETICA: registrate in stato_progetto).
- **(b) libexpat ≥ 2.4 nel doctor (gas.py)**: DEFERITA — resta a M1 finché il suo ponte voce non è mergiato.

## Prove
- `tests/test_unit_verifica_bot.py`: 500 passed; suite completa 2665 passed, 2 skipped (su ca222c6).
- Mutanti, tutti presi: su ca222c6 senza RecursionError 1 failed, senza la lettura grezza 14 sul test nuovo; su aec5c39 senza il controllo stringa per stringa 6 (misura del revisore #574), senza le chiavi 1; su 95249a8 senza il controllo «invisibili su gravità» 136 failed; con i soli tagli interni 14; senza le categorie del gate 3; e quelli di 57e927d (senza lo strip in decidi 10; senza l'escape 2; senza lo strip in contiene_segreti 3; senza il blocco bidi 4; senza gli intervalli non Cf 6).
- Nei due file, 0 caratteri Cf scritti in chiaro.

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
