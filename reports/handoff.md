# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Mani, fetta 28: `scripts/bot_esito.py` e i caratteri invisibili (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #305 (https://github.com/Gasss23/Gas/pull/305). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5073975831","url":"https://github.com/Gasss23/Gas/pull/305"}`), perché `gh` nel cloud non è autenticato. Tocca la macchina del bot: il check `verifica-bot` sarà neutral e il merge lo decide l'operatore.

---

## §1 SCOPE & ESITO FETTE

- **PR #303**: `FATTA` — mergiata da M1 (8424698) col sì dell'operatore dato a M1. Bot sull'ultimo head APPROVATO CON RISERVE, una BASSA: in handoff §5 il conteggio 247/1 (il mio, voice + lexbor) era attribuito alla review #568, che invece misura 240/1 su un altro insieme. `FATTA` — corretto qui e in stato_progetto.
- **(c) `scripts/bot_esito.py` e i caratteri invisibili**: `FATTA` (PR #305). Gli invisibili (Cf e non Cf del gate) si tolgono prima di decidere; i controlli bidi restano un NO; nella review pubblica ogni invisibile si vede come «<U+XXXX>»; le credenziali spezzate non si pubblicano. Review #569 APPROVATO CON RISERVE (R-569-1 e R-569-2 chiuse nel diff), #570 APPROVATO.
- **(b) libexpat ≥ 2.4 nel doctor**: `DEFERITA — resta a M1 finché il suo ponte voce non è mergiato`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  3 +++
 reports/diff_sessione.md           | 14 +++++++-------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |  2 +-
 reports/stato_progetto.md          |  3 ++-
 reports/ultimo_report.md           | 33 +++++++++++++--------------------
 scripts/bot_esito.py               | 47 +++++++++++++++++++++++++++++++++++++----------
 tests/test_unit_verifica_bot.py    | 56 ++++++++++++++++++++++++++++++++++++++++++++++++++++++--
```

NB: base = merge-base con origin/main = 8424698. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
57e927d fix(bot): i caratteri invisibili si tolgono prima di decidere e si mostrano nella review (bot #297, chat Mani)
a056b4c chore(revisore): memoria review #570 — APPROVATO
301e16e chore(revisore): memoria review #569 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 57e927d (scripts/bot_esito.py, tests/test_unit_verifica_bot.py). Verdetto integrale della review #569 (chat Mani), sul diff prima della correzione delle riserve:

```
## VERDETTO: APPROVATO CON RISERVE

Review #569 (chat Mani). Ho revisionato il diff staged, cioè `git diff --cached` sul branch claude/peaceful-lovelace-0w2b7q partito da 8424698: due file, la macchina del bot (`scripts/bot_esito.py`) e i suoi test. Prima della review ho letto CLAUDE.md, le parti utili di reports/stato_progetto.md e la memoria del revisore, comprese le lezioni del 2026-10-29 sui Cf scritti in chiaro. Questo verdetto non contiene caratteri Cf.

**Elementi del diff esaminati**
- `scripts/bot_esito.py:305` — `testo = _senza_invisibili(testo)` toglie i Cf prima del controllo sul titolo, della coincidenza col campo `verdetto` e delle gravità. Rischio: che lo strip trasformi un NO in un sì. Esito: ok.
  - Ho provato in-process: «ME + U+200B + DIA» dà COMMENT per MEDIA; «gra + U+200B + ve» dà COMMENT; «APPRO + U+200B + VATO» nel titolo coincide col campo.
  - Un Cf nel campo `verdetto` dà COMMENT («strutturato incompleto»). Un Cf nella gravità strutturata dà COMMENT («gravità non valida»): i campi strutturati non vengono ripuliti e restano fuori dai valori ammessi.
  - Titolo con controlli bidi: «U+202E OTAICCOB» non rispetta più il formato e dà COMMENT. La fullmatch sulla riga intera impedisce di aggiungere «NON» con un riordino.
  - Mutante senza lo strip, provato su una copia nello scratchpad: 6 failed, come dichiarato (i 29 errori di TestWorkflow vengono dalla copia senza .github, non dal mutante).
- `scripts/bot_esito.py:250` — `contiene_segreti` cerca le credenziali anche nel JSON con i Cf tolti. Rischio: falsi negativi o falsi positivi. Esito: ok. Con `ensure_ascii=False` i Cf restano caratteri e non diventano escape, quindi lo strip funziona. L'unico effetto è più severità.
- `scripts/bot_esito.py:360` — `_mostra_invisibili(testo)` viene applicato PRIMA di `.replace("```", ...)`. Rischio: un Cf dentro un triplo backtick che apre il recinto del codice. Esito: ok, perché « `<U+200B>`` » non è più un triplo backtick.
  - La riga 353 copre anche id e descrizione delle riserve minori.
  - È l'unico punto da cui il testo viene pubblicato: `cmd_esito` usa `corpo` sia per il check run sia per la review (scripts/bot_esito.py:433).
- `scripts/bot_esito.py:220` — l'espansione «<U+XXXX>» (8 caratteri) avviene dopo il taglio a MAX_TESTO e prima di quello a MAX_CORPO. Rischio: corpo troppo lungo. Esito: ok. Il taglio finale tiene il corpo sotto il limite; al più chiude a metà un «<U+20», ed è solo estetica.
- `tests/test_unit_verifica_bot.py:169` — il caso bot #297: APPROVE, «<U+200B>» nel corpo e 0 Cf. `tests/test_unit_verifica_bot.py:154` ora vuole COMMENT con «MEDIA», anche con U+00AD. `tests/test_unit_verifica_bot.py:191` copre le credenziali spezzate. Esito: ok. Suite del bot: 333 passed, rilanciata da me. Nei due file staged ci sono 0 Cf scritti in chiaro.
- Contesto: `modules/gate/gate.py:171` (`_INVISIBILI_NON_CF`) — vedi R-569-2.

**Grep sul motivo «caratteri invisibili»**
`_caratteri_invisibili` e il suo motivo non compaiono più da nessuna parte. Lo usavano solo i test, già aggiornati. Nessun documento (workflow, `.claude/verifica_esterna.md`, setup, roadmap) descrive il vecchio comportamento «ogni Cf dà NO».

**Riserve**
- R-569-1 (chat Mani), BASSA, nuova e introdotta da questo diff: con lo strip un controllo bidi non blocca più.
  - Prova: «FINDING: V-1 (U+202E ATLA U+202C) — x», con gravità strutturata BASSA, oggi dà APPROVE; prima dava COMMENT. Un lettore con rendering bidi vede «(ALTA)», la regex vede «ATLA».
  - Perché è BASSA: chi riesce a far scrivere al bot un testo così può fargli omettere la gravità in modo più semplice. Inoltre nella review pubblicata il testo appare come «<U+202E>ATLA<U+202C>», senza riordino.
  - Correzione possibile, senza obbligo: mantenere COMMENT solo per i controlli di override e isolamento bidi (U+202A–U+202E e U+2066–U+2069). Costo: un bot che cita un caso di prova bidi ricadrebbe nel failure definitivo. La scelta spetta all'agente o all'operatore.
- R-569-2 (chat Mani), BASSA, preesistente e non peggiorata: anche gli invisibili che non sono Cf aggirano la regex.
  - Prova: «ME + U+3164 + DIA», e lo stesso con U+115F, U+2800 e U+034F (categoria Mn), danno APPROVE sia prima sia dopo questo diff.
  - Correzione suggerita: togliere in `_senza_invisibili` anche gli intervalli di `modules/gate/gate.py:171` (copiati, perché `bot_esito.py` è autonomo) e mostrarli con l'escape.
  - Va registrata in stato_progetto.md come riserva aperta.

**Rischio escluso**
Non ho verificato il comportamento reale su GitHub: come check run e review mostrano «<U+XXXX>», e se il bot su #297 darebbe davvero success al rilancio. Servirebbe il workflow con la GitHub App, che non si può riprodurre qui. Non ho rifatto i mutanti di `componi_corpo` e di `contiene_segreti` (2 e 3 failed dichiarati): ho rifatto solo quello dello strip in `decidi`.

Memoria: riga #569 (chat Mani) e una lezione aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole in 301e16e. L'index staged sotto review non è stato toccato.
```

Verdetto integrale della review #570 (chat Mani), sul diff finale del commit 57e927d:

```
## VERDETTO: APPROVATO

Review #570 (chat Mani). Ho riletto il diff staged su claude/peaceful-lovelace-0w2b7q, cioè la ri-review di #569 con le due riserve corrette. È la macchina del bot, quindi il merge lo decide l'operatore. Ho fatto le letture obbligatorie: CLAUDE.md, reports/stato_progetto.md (solo le parti mirate) e la memoria. Ho applicato la lezione del 2026-10-29 su «normalizza invece di blocca»: ho provato il caso in cui togliere i caratteri invisibili non ricostruisce quello che l'operatore legge.

**Elementi del diff esaminati**
- `scripts/bot_esito.py:321` — è il controllo dei caratteri bidi (quelli che invertono o isolano la direzione del testo). Gira sul testo grezzo, prima della pulizia a `scripts/bot_esito.py:323`, e dà COMMENT «controlli bidi nel testo». Il rischio che ho guardato era il punto in cui sta il controllo, se prima o dopo la pulizia, e i falsi NO. Ho provato su una copia una variante con l'ordine invertito: falliscono 4 test (`test_controlli_bidi` per U+202A, U+202E, U+2066, U+2069). L'insieme `_BIDI` contiene esattamente U+202A–202E e U+2066–2069, verificato in-process. Falsi NO: un verdetto APPROVATO normale resta APPROVE. Anche LRM e RLM (U+200E, U+200F) dentro il testo o il titolo danno APPROVE: vengono solo tolti, ed è giusto, perché non riordinano le lettere. — **ok**
- `scripts/bot_esito.py:214` — è la copia di `_INVISIBILI_NON_CF`. Il rischio era una copia diversa dall'originale del gate. Il confronto in-process con `modules/gate/gate.py:171` dà `==` True. Ho provato U+FFA0, U+1160 e U+E0101 dentro MEDIA/ALTA, che non sono coperti dai test: danno COMMENT con la gravità ritrovata. Il gate include anche Cc, Zl e Zp, il bot no, ed è voluto. Ho provato U+2028 nella riga del verdetto: dà COMMENT «fuori formato», quindi va nel verso sicuro. — **ok**
- `scripts/bot_esito.py:371` e `scripts/bot_esito.py:378` — nella review pubblicata ogni carattere invisibile diventa «<U+XXXX>», sia nelle riserve minori sia nel verdetto integrale. Il rischio era un carattere bidi solo nella descrizione strutturata, che il controllo a `scripts/bot_esito.py:321` non guarda. L'ho provato: il risultato è APPROVE, ma la descrizione esce pubblicata come «(<U+202E>ATLA<U+202C>)», quindi è visibile. La decisione dipende dal campo gravità, che deve stare nell'elenco esatto: un bidi dentro la gravità dà COMMENT. «<U+202E>» non è un tag HTML valido, quindi su GitHub si vede così com'è. — **ok**
- `tests/test_unit_verifica_bot.py:153` — i test aggiunti coprono i caratteri invisibili non di formato, i controlli bidi, il titolo, le riserve pubblicate e le credenziali spezzate da caratteri invisibili. La suite del bot dà 342 passed, rieseguita da me. Nei due file non c'è nessun carattere di formato scritto in chiaro (contati: 0). — **ok**

**Rischio escluso:** non ho verificato il comportamento reale nel workflow GitHub, cioè la resa del markdown di «<U+XXXX>» dentro e fuori dal blocco di codice, né un run del check `verifica-bot`: in locale non si riproduce. C'è poi un limite che non dipende da questo diff: la frase «nessun finding ALTA o MEDIA» dentro un verdetto con riserve dà COMMENT anche alla base 8424698. È il falso positivo già registrato per il bot #191.

- Memoria: ho aggiunto la riga #570 e l'ho committata in `a056b4c` con `scripts/commit_memoria_revisore.sh`. L'index staged non è cambiato (stessi 2 file).
- File: `/home/user/Gas/scripts/bot_esito.py`, `/home/user/Gas/tests/test_unit_verifica_bot.py`, `/home/user/Gas/.claude/agents/memoria_revisore.md`.
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. `tests/test_unit_verifica_bot.py`: da 325 (CI su main) a 342 passed in locale; test cambiato `test_caratteri_invisibili` (ora vuole COMMENT per «MEDIA», non per «invisibili»), nuovi `test_controlli_bidi`, `test_invisibili_nel_titolo`, `test_invisibile_citato_dal_bot`, `test_invisibili_nelle_riserve_pubblicate`, `test_credenziali_spezzate_da_invisibili`. Suite completa in locale (Python 3.13): `2507 passed, 2 skipped in 226.80s`. Mutanti presi: senza lo strip in decidi 10 failed, senza l'escape 2, senza lo strip nei segreti 3, senza il blocco bidi 4, senza gli intervalli non Cf 6.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 301e16e, a056b4c (memoria del revisore) e 57e927d: pushati insieme prima dell'apertura della PR #305; run CI non letta alla scrittura dell'handoff.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Rischio escluso dalle review #569/#570: resa reale su GitHub di «<U+XXXX>» nel check run e nella review, e rilancio del bot su un verdetto come quello di #297 (si vede solo dal vivo).
- Preesistente (review #570): «nessun finding ALTA o MEDIA» in un verdetto con riserve dà COMMENT (falso positivo già registrato per il bot #191).
- (b) libexpat ≥ 2.4 nel doctor: con M1.
- V-3 ve #303 BASSA: selectolax 1.0.2 uscita il 2026-10-22, da decidere dall'operatore prima del `pip install` sul VPS.
- R-518-1 (chat Mani) BASSA: guardia `_nascosti_html` nelle chiusure in scope; per canvas fa perdere testo che il browser mostra (da decidere con l'oracolo).
- R-516-1 (chat Mani) BASSA: titolo perso sulle pagine a frame (verso sicuro).
- R-ve277-5 BASSA PREESISTENTE, parte leggi.py: con la lettura di sempre escono riserva di video/audio, testo di meter/progress, figli «light» di un host shadow.
- V-1 ve/bot #288 BASSA: adoption agency che sposta il template dichiarativo (dichiarata in `shadow()`).
- V-2 BASSA della verifica esterna #296 su 336e67c (https://github.com/Gasss23/Gas/pull/296#issuecomment-6485248441), scelta: entità non dichiarata con DOCTYPE esterno non XHTML, Gas taglia come Firefox.
- V-3 BASSA della verifica esterna #296 su 06bc98e (https://github.com/Gasss23/Gas/pull/296#issuecomment-6498712956), scelta: entità HTML5 fuori dal DTD XHTML 1.0 accettate, come whatwg.
- R-546-1 BASSA: numeri delle review doppi tra le chat.
