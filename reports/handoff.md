# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Mani, fetta 28: `scripts/bot_esito.py` e i caratteri invisibili (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #305 (https://github.com/Gasss23/Gas/pull/305). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5073975831","url":"https://github.com/Gasss23/Gas/pull/305"}`), perché `gh` nel cloud non è autenticato. Tocca la macchina del bot: il check `verifica-bot` sarà neutral e il merge lo decide l'operatore.

---

## §1 SCOPE & ESITO FETTE

- **PR #303**: `FATTA` — mergiata da M1 (8424698) col sì dell'operatore dato a M1. Bot sull'ultimo head APPROVATO CON RISERVE, una BASSA: in handoff §5 il conteggio 247/1 (il mio, voice + lexbor) era attribuito alla review #568, che invece misura 240/1 su un altro insieme. `FATTA` — corretto qui e in stato_progetto.
- **(c) `scripts/bot_esito.py` e i caratteri invisibili**: `FATTA` (PR #305). Gli invisibili (Cf e non Cf del gate) si tolgono prima di decidere; i controlli bidi restano un NO; nella review pubblica ogni invisibile si vede come «<U+XXXX>»; le credenziali spezzate non si pubblicano. Review #569 APPROVATO CON RISERVE (R-569-1 e R-569-2 chiuse nel diff), #570 APPROVATO.
- **Bot su e4559ef (PR #305)**: NO, check verifica-bot failure. V-1 MEDIA (togliere un invisibile tra due parole le incollava e la gravità non si vedeva, «BASSA<U+200B>MEDIA»: regressione del mio 57e927d, riprodotta in locale): `FATTA` in 95249a8 — un invisibile attaccato a una parola di gravità dà NO. V-2 BASSA (categorie del gate mancanti): `FATTA`. V-3 COSMETICA (tetto prima dell'escape): `FATTA`.
- **Verifica esterna su e4559ef (https://github.com/Gasss23/Gas/pull/305#issuecomment-6506076785)**: BOCCIATO. V-1 MEDIA (la stessa, con «ALTA<U+2800>x»): `FATTA` in 95249a8. V-2 BASSA («più severo di prima» non vale per un Cf lontano dalle gravità): `FATTA` — descrizione della PR corretta, il comportamento è voluto. V-3 BASSA (numero del mutante «senza escape»): `SALTATA — osservazione sul numero, nessun difetto`. V-4 COSMETICA: `FATTA` con la V-3 del bot.
- **Review #571 (chat Mani)**: BOCCIATO (due letture fisse non coprivano le combinazioni di invisibili). **Review #572**: APPROVATO CON RISERVE (R-572-1 e R-572-2, BASSE preesistenti, registrate in stato_progetto).
- **(b) libexpat ≥ 2.4 nel doctor**: `DEFERITA — resta a M1 finché il suo ponte voce non è mergiato`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++++
 reports/diff_sessione.md           |  14 +++++++-------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   2 +-
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  36 ++++++++++++++++--------------------
 scripts/bot_esito.py               |  82 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 tests/test_unit_verifica_bot.py    |  93 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
```

NB: base = merge-base con origin/main = 8424698. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
95249a8 fix(bot): un invisibile attaccato a una gravità dà NO (V-1/V-2/V-3 bot #305 e verifica esterna #305, chat Mani)
1b3a7a6 chore(revisore): memoria review #572 — APPROVATO CON RISERVE
0ffffd1 chore(revisore): memoria review #571 — BOCCIATO
e4559ef docs(fine-task): Mani fetta 28, bot_esito.py e i caratteri invisibili (PR #305)
57e927d fix(bot): i caratteri invisibili si tolgono prima di decidere e si mostrano nella review (bot #297, chat Mani)
a056b4c chore(revisore): memoria review #570 — APPROVATO
301e16e chore(revisore): memoria review #569 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

NB: i caratteri invisibili che i verdetti citavano alla lettera sono trascritti come «<U+XXXX>», così il testo è lo stesso ma si vede (il bot di main boccia ancora ogni Cf).

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

Commit 95249a8 (scripts/bot_esito.py, tests/test_unit_verifica_bot.py: note del bot e della verifica esterna su e4559ef). Verdetto integrale della review #571 (chat Mani), sul primo tentativo, poi scartato:

```
## VERDETTO: BOCCIATO

Review #571 (chat Mani). Diff staged su claude/peaceful-lovelace-0w2b7q, PR #305, head e4559ef, macchina del bot. Ho letto CLAUDE.md, reports/stato_progetto.md (le voci su #305, #569 e #570) e la mia memoria. Ho provato a mano tre versioni di scripts/bot_esito.py, caricate da copie: main 8424698, HEAD e4559ef e lo staged. La suite del bot dà 355 passed.

**Motivi bloccanti**

1. **V-1 MEDIA non è chiusa.** La lettura con gli spazi copre un solo invisibile. Con due invisibili di ruolo diverso, uno tra le parole e uno dentro la parola, le due letture fisse mancano tutte e due la gravità.
   - «V-1 (BASSA<U+200B>ME<U+200B>DIA)» con finding BASSA dà APPROVE. La lettura senza invisibili vede «BASSAMEDIA», quella con gli spazi «BASSA ME DIA».
   - Danno APPROVE anche:
     - le varianti U+2800+U+200B e U+034F+U+200B;
     - «ALTA» nuda con invisibili misti;
     - «gra<U+200B><U+200B>ve» minuscolo su una riga V-.
   - Main dava COMMENT su tutti questi casi, HEAD dava APPROVE.

2. **Regressione rispetto a HEAD, portata dalla V-2.** I caratteri che prima restavano nel testo ora si tolgono: se uno di loro faceva da separatore, togliendolo incolla le parole. «V-1 (BASSA<sep>ME<U+200B>DIA)» dà COMMENT a HEAD e APPROVE nello staged per tutti e 9 i separatori provati: \x0b, \x0c, \x1f, \x85, U+2028, U+2029, U+E000, U+E0080, U+F0000. Quindi il delta non è solo più prudente: apre sì sbagliati nuovi.

**Fix suggerito.** Non affidarsi a `\b` sulla lettura senza invisibili. Cercare le gravità (maiuscole e `_GRAVI`, senza limiti di parola) nel testo senza invisibili e dare COMMENT se il match tocca la posizione di un invisibile tolto (una mappa degli indici rimossi). Il falso NO su cose come «multi<U+00AD>mediale» è accettabile, perché sbaglia dal lato prudente. Test: incrociare un separatore (Cf, non Cf, Cc, Zl, Co) con un invisibile dentro la parola, su MEDIA, ALTA e «grave», più un mutante che rifaccia passare il caso a due invisibili.

**Elementi del diff esaminati**

- `scripts/bot_esito.py:334` — calcola `con_spazi` (invisibili come spazio) accanto alla lettura senza invisibili. Rischio: combinazioni che nessuna delle due letture vede. Esito: **blocco**, vedi motivo 1.
- `scripts/bot_esito.py:353` — le gravità si cercano sull'unione delle due letture. Rischio: falso NO su un verdetto normale. Esito: **ok**. L'unione aggiunge solo NO. I casi provati sono tutti dal lato prudente:
  - un id di riserva registrata spezzato («R-203<U+200B>-1 (ALTA)») dà COMMENT;
  - «NON <U+200B>VERIFICATO:», che con lo spazio diventa un doppio spazio e non apre più la coda, dà COMMENT;
  - il bot che cita «BASSA<U+200B>MEDIA» alla lettera dà COMMENT (falso NO anche sulla prossima verifica di questa stessa PR, se la cita così);
  - «alta<U+00AD>mente» su una riga V- dà COMMENT;
  - la riserva registrata normale «R-203-1 (ALTA, preesistente)» resta APPROVE.
- `scripts/bot_esito.py:227` — aggiunge le categorie Cn, Co, Cs, Zl, Zp e i Cc tranne \n \r \t, come le categorie del gate in `modules/gate/gate.py:182`. Rischio: più caratteri tolti incollano parole che prima erano separate. Esito: **blocco**, vedi motivo 2. Sul conteggio delle righe: Python `re` con `re.M` riconosce solo \n come fine riga; provato, `^x` su «a\x0bx\x0cx\x85x
x\nx» trova un solo match. Trattare i Cc come invisibili quindi non cambia le righe viste dalle regex (**ok**).
- `scripts/bot_esito.py:337` — titolo e coincidenza col campo restano sulla lettura senza invisibili. Rischio: un sì sbagliato. Esito: **ok** per il delta. Un secondo titolo nascosto dopo \x0b, U+2028 o \x85 dà APPROVE, ma ora nella review si vede come «<U+000B>» sulla stessa riga, coerente con quello che vede la regex.
- `scripts/bot_esito.py:389` — l'escape «<U+XXXX>» si fa prima del tetto `MAX_TESTO`. Rischio: un recinto del codice aperto o un corpo oltre il limite. Esito: **ok**. 60000 caratteri più l'intestazione stanno sotto `MAX_CORPO`; il taglio può spezzare un «<U+20…» a metà, ma è solo cosmetico.
- `tests/test_unit_verifica_bot.py:165` — `test_invisibile_tra_due_parole`, parametrizzato su 8 caratteri. Rischio: copre un solo invisibile per caso. Esito: **riserva**, va esteso ai casi con due invisibili.
- `tests/test_unit_verifica_bot.py:182` — `test_tetto_dopo_escape`. Esito: **ok**.

**Rischi esplicitamente esclusi**

- Non ho rifatto i mutanti dichiarati (8, 3, 1 e 1 failed): mi sono fidato del numero dato, perché ho provato direttamente i casi avversari.
- Non ho verificato come GitHub mostra un \r singolo dentro il recinto del codice. È preesistente e uguale a main: «CLAIM: x\rVERIFICA ESTERNA #1 — BOCCIATO» dà APPROVE, mentre in GitHub potrebbe comparire su una riga a sé. Lo segnalo come nota BASSA da valutare; non si riproduce senza pubblicare una review vera.
- Non ho controllato il workflow `verifica-bot.yml`, che non è toccato dal diff.

**Memoria.** Ho aggiunto la riga #571 e una lezione (due letture fisse non coprono le combinazioni di invisibili; ogni allargamento di cosa si toglie va provato contro HEAD). È committata con `scripts/commit_memoria_revisore.sh` (commit 0ffffd1, solo `/home/user/Gas/.claude/agents/memoria_revisore.md`).

Le sonde stanno in `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/probe.py` e `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/probe2.py`. Si lanciano con `python3 -I <sonda> /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad`.
```

Verdetto integrale della review #572 (chat Mani), sul diff finale del commit 95249a8:

```
## VERDETTO: APPROVATO CON RISERVE

Review #572 (chat Mani). Ri-review della #571 sul diff STAGED (`scripts/bot_esito.py`, `tests/test_unit_verifica_bot.py`), PR #305, macchina del bot: il merge lo decide l'operatore. Prima della review ho letto CLAUDE.md (sez. 5, 8, 9, 10), le parti di reports/stato_progetto.md e di .claude/agents/memoria_revisore.md che servivano (lezioni #569–#571).

**Elementi del diff esaminati**
- `scripts/bot_esito.py:249`: `_invisibili_su_gravita` si segna dove ha tolto ogni invisibile nel testo pulito e lo confronta con i match di `_GRAVI` cercati senza confini di parola (start ≤ taglio ≤ end). Ho controllato i casi con due invisibili di ruolo diverso e le sovrapposizioni tra parole di gravità: se una parola visibile si sovrappone a un match precedente, il taglio cade dentro quel match (`critico_ALTA<U+2800>x` e `MEDI<U+2800>ALTA` danno COMMENT). Mutanti provati su una copia: senza il controllo 136 failed; con `bisect_right` e `<` 42 failed. Esito: ok, la V-1 è chiusa.
- `scripts/bot_esito.py:356`: il controllo gira dopo quello bidi e prima dello strip, sul testo intero (anche Metodo e CLAIM). Questo allarga i falsi NO a parti del testo dove la gravità non conterebbe. È accettato, perché è nella direzione sicura e scatta solo con un invisibile attaccato a una gravità: il caso #297 lontano dà APPROVE (`tests/test_unit_verifica_bot.py:179`). Esito: ok.
- `scripts/bot_esito.py:228`: categorie Cn/Co/Cs/Zl/Zp più i Cc, esclusi `\n\r\t`, come nel gate. Confronto con HEAD: «non\x0bgrave» era APPROVE (il `\s` valeva come negazione) e ora è COMMENT, quindi blocca di più. Esito: ok, la V-2 è chiusa. Riserva R-572-1 sotto.
- `scripts/bot_esito.py:411`: l'escape avviene prima del tetto `MAX_TESTO`, e il recinto del codice resta chiuso (`tests/test_unit_verifica_bot.py:195`). Il taglio può spezzare un «<U+XXXX>» a metà, ma è solo cosmetico. Esito: ok, la V-3 è chiusa.
- `tests/test_unit_verifica_bot.py:172`: 14 separatori × 3 invisibili dentro la parola × 3 forme. La suite del bot fa 474 passed (rilanciata da me).

**Falsi NO (accettati, vanno nella direzione sicura)**
Danno COMMENT anche se non nascondono nulla:
- «immedia<U+00AD>to»;
- «multimedia<U+200D>»;
- «⚠<U+FE0F>Mediante»;
- «gra<U+200B>vità».

Scattano solo se l'invisibile sta dentro la sottostringa o sul suo bordo. Un invisibile staccato da uno spazio dà APPROVE. Il costo è un commit nuovo, mai un sì sbagliato.

**Vie verso un sì sbagliato che non passano da `_GRAVI` (ho confrontato HEAD e staged)**
- «R-203<U+200B>-1 (ALTA)» e «NON <U+200B>VERIFICATO:» danno APPROVE sia su HEAD sia sullo staged. Sono d'accordo con te: la forma visibile senza invisibile dà lo stesso esito, quindi l'invisibile non dà più potere a chi vuole nascondere una gravità.
- «R<U+200B>-V-2 (ALTA)» dà COMMENT; un titolo «VERIFICA ESTE<U+200B>RNA — BOCCIATO» dà COMMENT; «FINDING:» incollato con U+2028 dà COMMENT.

**Riserve (entrambe BASSA, da tracciare in stato_progetto.md)**
- R-572-1 (chat Mani), BASSA: i separatori di riga Unicode (U+2028, U+2029, NEL `\x85`, `\x0b`) vengono tolti invece di diventare un «a capo».
  - «x<U+2028>V-2 — y — grave» dà APPROVE: la riga V- finisce incollata a quella prima, così le regole sulle righe non la vedono e «grave» minuscolo in mezzo alla riga non conta. Succede uguale su HEAD, quindi è preesistente.
  - «NON VERIFICATO<U+0085>: … MEDIA» diventa un'intestazione: su HEAD dava COMMENT, ora dà APPROVE. Coincide con la lettura visibile, quindi non è sfruttabile.
  - Correzione suggerita: in `_senza_invisibili` mappare Zl/Zp/`\x0b`/`\x0c`/`\x1c`–`\x1e`/`\x85` su «\n» invece che su vuoto.
- R-572-2 (chat Mani), BASSA preesistente: i segni combinanti visibili (U+0323 dentro «MEDIA») e gli omoglifi cirillici danno APPROVE, su HEAD come sullo staged. Sono fuori dal perimetro degli invisibili.

**Rischio escluso**
Non ho verificato il comportamento reale del workflow su GitHub: la pubblicazione della review e la resa di `<U+XXXX>` e U+2028 nel commento. Non si riproduce in locale; ho provato solo `decidi` e `componi_corpo` in-process. Non ho rilanciato le tue probe.py e probe2.py: ho usato sonde mie. Nella copia dei mutanti 29 errori vengono dal file del workflow assente nella copia e non toccano i conteggi.

- Memoria del revisore: aggiunta la riga #572 e una lezione nuova, committate con `scripts/commit_memoria_revisore.sh` (commit 1b3a7a6). Lo staged non è stato toccato.
- File: /home/user/Gas/scripts/bot_esito.py, /home/user/Gas/tests/test_unit_verifica_bot.py, /home/user/Gas/.claude/agents/memoria_revisore.md
- Sonde: /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/p572.py e /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/p572b.py
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. `tests/test_unit_verifica_bot.py`: da 325 (CI su main) a 474 passed in locale; test cambiato `test_caratteri_invisibili` (ora vuole COMMENT per «MEDIA», non per «invisibili»), nuovi `test_invisibili_tra_e_dentro_le_parole` (14 separatori × 3 invisibili dentro la parola × 3 forme), `test_invisibile_lontano_dalle_gravita`, `test_altri_invisibili_mostrati`, `test_tetto_dopo_escape`, `test_controlli_bidi`, `test_invisibili_nel_titolo`, `test_invisibile_citato_dal_bot`, `test_invisibili_nelle_riserve_pubblicate`, `test_credenziali_spezzate_da_invisibili`. Suite completa in locale (Python 3.13): `2639 passed, 2 skipped in 223.01s`. Mutanti presi su 95249a8: senza il controllo «invisibili su gravità» 136 failed, con i soli tagli interni 14, senza le categorie del gate 3; su 57e927d: senza lo strip in decidi 10 failed, senza l'escape 2, senza lo strip nei segreti 3, senza il blocco bidi 4, senza gli intervalli non Cf 6.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 301e16e, a056b4c (memoria del revisore) e 57e927d: pushati insieme prima dell'apertura della PR #305; nessuna run sulla PR per questi SHA.
- e4559ef (fine-task): run CI 40937383734; check `verifica-bot` failure (V-1 MEDIA del bot, vedi §1), definitivo su questo SHA.
- 0ffffd1, 1b3a7a6 (memoria del revisore) e 95249a8: pushati insieme; run CI non letta alla scrittura dell'handoff.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Rischio escluso dalle review #569/#570: resa reale su GitHub di «<U+XXXX>» nel check run e nella review, e rilancio del bot su un verdetto come quello di #297 (si vede solo dal vivo).
- Preesistente (review #570): «nessun finding ALTA o MEDIA» in un verdetto con riserve dà COMMENT (falso positivo già registrato per il bot #191).
- R-572-1 (chat Mani) BASSA preesistente: i separatori di riga Unicode (U+2028/2029, NEL, \x0b) si tolgono invece di diventare un a capo: una riga V- incollata alla precedente non conta come riga di finding.
- R-572-2 (chat Mani) BASSA preesistente: segni combinanti visibili e omoglifi cirillici dentro una gravità passano.
- Review #571, nota preesistente: un \r singolo prima di un secondo titolo «VERIFICA ESTERNA — BOCCIATO» dà APPROVE anche su main (resa su GitHub da verificare).
- (b) libexpat ≥ 2.4 nel doctor: con M1.
- V-3 ve #303 BASSA: selectolax 1.0.2 uscita il 2026-10-22, da decidere dall'operatore prima del `pip install` sul VPS.
- R-518-1 (chat Mani) BASSA: guardia `_nascosti_html` nelle chiusure in scope; per canvas fa perdere testo che il browser mostra (da decidere con l'oracolo).
- R-516-1 (chat Mani) BASSA: titolo perso sulle pagine a frame (verso sicuro).
- R-ve277-5 BASSA PREESISTENTE, parte leggi.py: con la lettura di sempre escono riserva di video/audio, testo di meter/progress, figli «light» di un host shadow.
- V-1 ve/bot #288 BASSA: adoption agency che sposta il template dichiarativo (dichiarata in `shadow()`).
- V-2 BASSA della verifica esterna #296 su 336e67c (https://github.com/Gasss23/Gas/pull/296#issuecomment-6485248441), scelta: entità non dichiarata con DOCTYPE esterno non XHTML, Gas taglia come Firefox.
- V-3 BASSA della verifica esterna #296 su 06bc98e (https://github.com/Gasss23/Gas/pull/296#issuecomment-6498712956), scelta: entità HTML5 fuori dal DTD XHTML 1.0 accettate, come whatwg.
- R-546-1 BASSA: numeri delle review doppi tra le chat.
