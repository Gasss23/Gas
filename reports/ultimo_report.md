# ULTIMO REPORT — R-gate-worktree-1: il gate di review non è più inerte nei worktree

> Task del 2026-10-12, su richiesta dell'operatore («fai pure una fetta per il gate worktree»).
> Ramo: **`fix/gate-worktree`** (da `origin/main` = `af394bc`).
> Fetta di **sicurezza**: tocca la macchina di controllo del progetto.

## DECISIONI UMANE RICHIESTE

1. **Ordine di merge e rinumerazione delle review.** Questo ramo parte da `main` (che arriva a
   **#298**) e il revisore ha quindi preso **#299/#300**; ma la **PR #195**, non ancora mergiata, usa
   già **#299–#301**. Due serie identiche, create da me. Si risolve rinumerando le righe contatore di
   questo ramo **dopo** il merge della #195 (ripartendo dal primo numero libero), e risolvendo il
   conflitto su `.claude/agents/memoria_revisore.md` **appendendo** entrambe le serie.
2. **Secondo passaggio nella chat claude.ai** col link della PR: è una fetta di sicurezza
   (CLAUDE.md, istituzione E).
3. **La PR #195 resta bloccata da un bug del bot**, non da un suo difetto: `scripts/bot_esito.py`
   scarta la gravità delle riserve registrate solo se l'id è **numerico**, e `R-gate-worktree-1` non
   combacia. Decide l'operatore, oppure serve una fetta sulla macchina del bot.

## Il difetto (R-gate-worktree-1, gravità ALTA)

`.claude/hooks/review_gate.sh` faceva `cd "$CLAUDE_PROJECT_DIR"` **incondizionato** e giudicava
**solo** quell'indice. La documentazione di Claude Code dice che `CLAUDE_PROJECT_DIR` «still points at
the project root where the session started», mentre il campo `cwd` del payload «follows Claude: … is
the worktree root after Claude enters a worktree».

Conseguenze, entrambe misurate:

- **Falso negativo (il buco grave)**: in una sessione che lavora in un **worktree**, se l'indice del
  checkout principale era pulito il `grep` sul perimetro non matchava e l'hook faceva `exit 0`
  **senza nemmeno aprire il marcatore**. Un diff di `gas.py`/`modules/`/`tests/` **mai revisionato**
  poteva entrare. Ogni worktree ha inoltre un **proprio** `.claude/.review_ok` che non veniva mai
  consultato.
- **Falso positivo**: un diff staged nel principale bloccava i commit delle **altre** sessioni nei
  worktree, anche di soli `reports/`. Osservato dal vivo durante questa sessione.

Gravità: inizialmente l'avevo valutata MEDIA, poi **rivista ad ALTA** accogliendo l'argomento della
sessione sorella — «inerte in un worktree» non è tra i limiti dichiarati dell'hook, i worktree sono
la configurazione normale del progetto, e una rete che fallisce **in silenzio** è peggio di una
assente, perché chi la vede verde si crede coperto.

## Cosa fa il fix

L'hook costruisce l'insieme dei checkout da controllare e applica a **ognuno** il controllo completo
(perimetro, diff staged, working tree, marcatore **proprio**), in subshell:

1. la radice git di **`cwd`** — il checkout dove la sessione lavora davvero;
2. i bersagli **assoluti e letterali** di `cd`/`pushd`/`-C`/`--work-tree=`/`--git-dir=` estratti dal
   comando (ogni occorrenza, anche dentro gli apici);
3. **tutti** i worktree registrati, quando `cwd` manca o quando esiste un costrutto che cambia
   directory che **non si risolve** (percorso relativo, variabile, glob, `popd`, `GIT_DIR=`,
   `GIT_WORK_TREE=`, forme con spazio);
4. la radice di `CLAUDE_PROJECT_DIR` **solo se `cwd` è sconosciuto** — vedi R-299-3.

## Numeri REALI

| Misura | Prima | Dopo |
|---|---|---|
| `tests/test_unit_hooks.py` | 107 | **138** (31 nella classe `TestReviewGateWorktree`) |
| `pytest -q` (tutto) | 1031 | **1062 passed, 1 skipped** |
| Suite kernel | 821 PASS, 0 FAIL | **821 PASS, 0 FAIL** (il diff non tocca il motore) |

**Prova che i test mordono**, non solo che passano:

- contro l'hook di `main` (pre-fix): **8 dei 15** test nuovi FALLISCONO, e `test_gate_wt1` — la
  riproduzione — restituisce **`exit 0` dove serve `2`**: esattamente l'inerzia;
- contro la versione del **primo giro** di questa fetta: FALLISCONO tutti e quattro i test aggiunti
  nel secondo giro (`wt12`–`wt15`);
- mutazione «spazza sempre» (`SPAZZA=1`): FALLISCE solo `wt8`, quindi il raffinamento è sorvegliato;
- mutazione «conteggi ignorati»: FALLISCONO `wt9` e `wt10`.

## Cinque giri di review, due BOCCIATI: la parte riutilizzabile

La fetta ha richiesto **cinque** giri e due dei verdetti sono stati **BOCCIATO**. Vale la pena
scrivere perche', non per cronaca ma perche' il motivo e' trasferibile.

- **#300 BOCCIATO**: chiudendo le riserve del primo giro avevo escluso gli apici dalla classe del
  **bersaglio**. Un percorso quotato non aveva piu' nessun carattere da consumare, quindi il
  costrutto non veniva nemmeno **trovato**: sei forme comuni passavano. Suite **122 su 122 verde**.
- **#301 BOCCIATO**: togliendo gli apici a prescindere, un bersaglio quotato **con uno spazio**
  arrivava **troncato** e la normalizzazione lo rendeva «assoluto e letterale». Se il troncone e' a
  sua volta un repo — basta un nome come `<radice> copia` — il dubbio svaniva e il bersaglio vero
  non veniva mai ispezionato. Suite **130 su 130 verde**.
- **#302 APPROVATO CON RISERVE**: regola «coppia di apici ai **bordi** + ogni residuo e' dubbio».

**Il filo comune dei due BOCCIATI non e' il codice, e' la forma della dimostrazione.** Nei primi tre
giri difendevo il matcher **elencando le forme coperte**; ogni volta ne restava fuori una, e ogni
volta la suite era verde col buco dentro. L'argomento che ha chiuso la questione e' invece
**strutturale**: dopo «coppia ai bordi + rifiuto dei residui», il bersaglio sopravvissuto non
contiene spazi, ne' `;&|)`, ne' apici, ne' `$`, backtick, glob o `~` — e' quindi **una sola parola di
shell senza espansioni**, e per costruzione coincide con cio' che userebbe la shell. Un troncamento
richiederebbe un carattere escluso dalla classe, che adesso **impedisce** la risoluzione invece di
sopravvivere alla normalizzazione.

**Regola che ne esce**: se la dimostrazione di una regola di normalizzazione deve elencare i casi,
quella regola e' un'euristica e prima o poi fabbrica un bersaglio valido. E un corollario sui test:
una forma nuova va provata **anche** nella sua variante con lo **spazio**, perche' e' lo spazio che
tronca.

**Altra regola, sulle righe di «limiti dichiarati»**: sono affermazioni da **provare** come il
codice. In questa fetta **tre** limiti dichiarati si sono rivelati falsi alla misura («il relativo fa
spazzare», «l'apice spaiato fa spazzare», «con spazi resta non risolvibile»). Ora i limiti-
comportamento hanno un test; i limiti-non-promessa (alias, heredoc, `GIT_INDEX_FILE`, eval) sono
dichiarati come tali, perche' pretenderne un test avrebbe prodotto la quarta dichiarazione falsa.

## Riserve del revisore, tutte chiuse

Review **#299 APPROVATO CON RISERVE** con tre MEDIE, **due delle quali falle del meccanismo nuovo**
(non regressioni: l'hook di `main` esce 0 negli stessi casi):

- ✅ **R-299-1** (MEDIA, **fail-open reale introdotto da me**): `-C` era matchato solo attaccato a
  `git`, quindi `git -C <pulito> -C <sporco>` contava **1/1** → nessun dubbio → `exit 0`, mentre git
  applica l'**ultimo** `-C`. CHIUSA: `-C` si matcha a ogni occorrenza. Test `wt12`.
- ✅ **R-299-2** (MEDIA): un `cd` dentro una stringa (`bash -c "cd /altro && …"`) non veniva nemmeno
  **trovato**, perché il prefisso del match non ammetteva gli apici. CHIUSA **invece che dichiarata**:
  gli apici sono nella classe del prefisso. Test `wt13`. Il limite residuo è riscritto onesto: il gate
  non promette di intercettare ogni commit altrove, promette di non lasciar passare un checkout che
  ha **ispezionato**.
- ✅ **R-299-3** (MEDIA): il commento raccontava anche l'altra metà del difetto e poi dichiarava di
  controllare «ogni checkout candidato», ma quella metà non era chiusa. CHIUSA cambiando il progetto:
  con `cwd` noto il principale **non entra più** nell'insieme. Test `wt14`.
- ✅ **R-299-4** (BASSA): un worktree **prunable** (directory rimossa) rendeva ogni comando un vicolo
  cieco sbloccabile solo con `git worktree prune`. CHIUSA: nella spazzata si salta; il fail-closed
  resta pieno per i bersagli **nominati**. Test `wt15`.
- ✅ **R-299-5** (BASSA): `wt7` passava per il motivo **sbagliato** (senza `cd` il worktree non veniva
  mai ispezionato, quindi restava verde anche col worktree sporco). CHIUSA: ora forza la spazzata.
- ✅ **R-299-6** (COSMETICA, tre punti): via l'`export` inutile, campo passato per **argv** anche ai
  rami python, e `if ! WT_LIST=$(…)` al posto del `$?` non atomico.

## Scelta di progetto da sorvegliare

La chiusura di **R-299-3** rompe la proprietà di **sovrainsieme** su cui il revisore si era appoggiato
per non bocciare il primo giro: con `cwd` noto e dentro un worktree, il principale non è più
ispezionato. Il mio argomento è che non è perdita di copertura ma correzione del **bersaglio** — il
gate deve giudicare il checkout dove il commit avviene. È la scelta su cui ho chiesto al revisore di
essere più duro.

## Igiene dei nomi (correzione a me stesso)

**`R-gate-matcher-1` non è un finding nuovo**: è un **terzo nome** per `R-gjq-1` e `R-137-2`, già
registrate in `reports/stato_progetto.md`. Va usato un rimando, non un id nuovo. Il difetto (il
matcher decide «è un commit?» con un `grep` sul **testo** del comando) **non** è corretto qui, su
indicazione del revisore e con il suo argomento: è l'unica modifica che potrebbe trasformare un
fastidio **fail-closed** in un **fail-open**, e metterla nello stesso diff che allarga l'insieme dei
checkout renderebbe impossibile attribuire un eventuale buco. Misura utile per la fetta dedicata: ha
bloccato **cinque** comandi innocui durante questa fetta (tre al revisore, due a me, uno dei quali
mentre **leggevo l'hook stesso**).

## NON VERIFICATO

- Il comportamento con un payload **reale** di Claude Code: i test usano payload sintetici, quindi la
  forma effettiva di `cwd` (assoluto? normalizzato dai symlink? presente in questa versione?) non è
  provata, né il caso di una versione che lo omette in sessione vera.
- **Linux/CI e Windows/WSL**: tutto misurato su macOS con bash 3.2 di sistema.
- Fail-open **preesistenti** non introdotti da questo diff e non chiusi qui: `grep` assente →
  `|| exit 0` (`R-gjq-3`), `INPUT` vuoto → `exit 0`, `PERIM_RE` non valida → `exit 0`.
