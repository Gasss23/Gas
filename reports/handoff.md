# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-12 — check delle PR #184/#185 + fetta T80u5 (il tetto di annidamento non dipende più dalla versione di Python)

---

## §0 DECISIONI UMANE RICHIESTE

1. **La PR #192 è stata mergiata (`af394bc`, da `Gasss23` alle 16:39 del 2026-10-12) MENTRE questa
   sessione stava eseguendo la correzione di V-1 richiesta dall'operatore.** Conseguenza di fatto, non
   un'opinione: il commit `3f59b6e` che corregge V-1 **NON è in `main`** (`git branch -r --contains
   3f59b6e` → vuoto). È stata quindi aperta la **PR #195** (https://github.com/Gasss23/Gas/pull/195),
   numero e URL dall'output reale di `gh pr view --json number,url`:
   `{"number":195,"url":"https://github.com/Gasss23/Gas/pull/195"}`.
2. **Merge della PR #195**: finché il verdetto del bot non è `APPROVATO` secco senza finding, per la
   regola di merge autonomo di CLAUDE.md **decide l'operatore**.
3. **R-gate-worktree-1** (MEDIA, §7): il gate deterministico di review è inerte nelle sessioni che
   girano in un worktree. Decidere se diventa una fetta: l'hook è nel perimetro di review.
4. **`F-ci-una-sola-versione`**: decidere se la CI deve provare più di una versione di Python. Oggi
   pinna solo 3.11, ed è il motivo per cui il FAIL di T80u5 su 3.14 è vissuto invisibile.
5. **Collisione dei numeri di review** con la sessione sorella (§7): piano concordato, serve solo la
   conferma di quale ramo entra prima.

---

## §1 SCOPE & ESITO FETTE

- **Fetta T80u5 — tetto di annidamento deterministico**: `FATTA E GIÀ IN MAIN` — commit `c298d59`,
  entrato con il merge della PR #192 (`af394bc`). Fuori dal diff di questa sessione (la base si è
  spostata ad `a6fa2fd`), quindi non compare in §2/§3.
- **Correzione di V-1 della verifica esterna** (richiesta esplicita dell'operatore «correggi V-1
  prima del merge»): `FATTA MA NON ANCORA IN MAIN` — commit `3f59b6e`, solo il blocco di commento
  sopra il tetto. Review #299, #300 APPROVATO CON RISERVE; **#301 APPROVATO**. Il merge della PR #192
  è avvenuto prima che questa correzione fosse pushata: va in una PR nuova (§0.1).
- **Check delle PR #184/#185**: `FATTO` nella prima parte della sessione, già in main con `7fd062b`.
- **Fetta «budget di byte di `cerca_testo`»**: `DEFERITA — in carico alla sessione sorella`
  (`cerca_testo: il budget di byte non deve mentire`, PR #193).
- **V-2 e V-3 della verifica esterna #192**: `NON FATTE — decisione dell'operatore` (solo V-1 prima
  del merge). Restano aperte come COSMETICHE in §7.
- **R-gate-worktree-1**: `NON FATTA — fuori scope dichiarato`, richiede fetta propria.

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  10 ++++++++++
 gas.py                             |  16 ++++++++++++----
 reports/diff_sessione.md           |  10 +++++++++-
 reports/handoff.md                 | 345 ++++++++++++++++++++++++++++++++++++++++++-----------------
 reports/stato_progetto.md          |  12 +++++++++++-
 reports/ultimo_report.md           |  97 +++++++++++++++++++++++++++++++++++++++++
 6 files changed, 342 insertions(+), 148 deletions(-)
```

**La BASE di questa sessione si è SPOSTATA durante il lavoro**, e questo blocco è calcolato sulla
base nuova: `git -c core.quotePath=false diff --cached --stat=400 a6fa2fd`. Motivo: il merge della PR
#192 ha portato in `main` i commit fino ad `a6fa2fd`, quindi
`git merge-base refs/remotes/origin/main HEAD` non è più `f6396ba` ma **`a6fa2fd`**. Di conseguenza
`gas.py` qui conta **16 righe** (solo il commento di `3f59b6e`) e `tests/test_unit_kernel.py` **non
compare più**: i test T80u6/T80u7 sono già in main. Un §2 calcolato sulla base vecchia dichiarava 7
file e `check_handoff` lo ha correttamente respinto come incoerente (file fantasma
`tests/test_unit_kernel.py`). Il set di 6 path qui sopra è quello reale.

## §3 GIT LOG --ONELINE (sessione)

```
696a37e docs(fine-task): report e handoff dopo la correzione di V-1 (review #299-#301) e R-gate-worktree-1
3f59b6e fix(riflessione): la misura nel commento del tetto non sovrastima più (V-1 verifica esterna #192)
8f040f0 chore(revisore): memoria review #301 — APPROVATO
675a574 chore(revisore): memoria review #300 — APPROVATO CON RISERVE
035c2d8 chore(revisore): memoria review #299 — APPROVATO CON RISERVE
```

`git log --oneline a6fa2fd..HEAD`. Il commit `696a37e` è il fine-task del giro precedente e viene
riscritto (amend) da questo stesso giro, quindi il suo hash cambierà: l'hash finale sta nel log del
branch dopo il push. I commit della prima parte della sessione (`06636d5`, `6f6f370`, `4017ee5`,
`c298d59`, `7fd062b`, `a6fa2fd`) sono **in main** e fuori da questo range per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore **di questo giro**: uno solo, `3f59b6e` — solo `gas.py`, **solo il blocco di
commento** sopra il tetto (correzione di V-1 della verifica esterna, su richiesta esplicita
dell'operatore). Il revisore ha provato **meccanicamente** che il codice eseguibile è bit-identico al
commit precedente: 29593 token non-COMMENT, sha del flusso `f49b717979008a2a` su entrambe le
versioni, docstring incluse.

L'altro commit di motore della sessione, `c298d59` (il tetto e i test T80u5/u6/u7, verdetti #297 e
#298), è **già in main** con il merge della PR #192 e fuori dal diff di questa sessione: il suo
verdetto di gate è nell'handoff pinnato a `a6fa2fd`, non qui.

La fetta ha avuto **cinque** giri di review in tutto: #297/#298 sul primo commit, #299/#300/#301 sul
secondo. I giri #299 e #300 riguardano diff poi **superati** e le loro citazioni puntano a righe non
più valide, quindi NON sono verdetti di gate e non sono incollati qui (sintesi in §7). Il verdetto di
gate per `3f59b6e`, emesso sul diff effettivamente committato, è il **#301**, l'unico `APPROVATO`
secco della serie, incollato INTEGRALE:

```
VERDETTO: APPROVATO

Review #301 (riga contatore scritta e committata: 8f040f0). Diff staged riletto con
git diff --cached: solo gas.py, 12 inserimenti / 4 rimozioni, tutto dentro il blocco di commento.
R-300-1 chiusa. Nessuna riserva sul codice; una sola osservazione, cosmetica e sul testo del
report, non sul diff.

1. Grep di controllo — nessuna claim residua piu' larga della misura

- grep -n "da 3.14 le parsa|fino a 3.12|le parsa|solo a 118k|100k dict|120k" gas.py -> rc=1,
  nessuna riga: sparite tutte le formulazioni dei giri precedenti, compresa «solo a 118k» di
  R-300-1.
- La parola «solo» sopravvive in UNA sola riga del blocco, gas.py:620 («non solo dalla versione»),
  dove e' legittima e non asserisce confini. Esito: ok.
- Numeri residui nel blocco, estratti meccanicamente: 116k, 117k, 200k, 50k, 512, 5_000_000, 50,
  piu' data/versione. Sono tutti misurati da me, nessuno ereditato.

2. Elementi del diff esaminati

- gas.py:622 — «ne parsa 116k livelli». Rischio: confine spostato in avanti rispetto alla misura.
  Riprodotto in un processo nuovo: 114k PARSED, 116k PARSED. Esito: ok.
- gas.py:624 — «e a 117k solleva RecursionError: il confine cade fra quei due valori ADIACENTI».
  Riprodotto: 117k RecursionError. Insieme alle 3+3 ripetizioni del mio giro #300 (115k/116k
  PARSED x3, 117k/118k RecursionError x3) e alla tua griglia da mille, pass e fail sono adiacenti e
  stabili su ripetizioni indipendenti: la claim e' ora esattamente larga quanto la misura.
  Esito: ok, R-300-1 chiusa.
- gas.py:625 — «ADIACENTI, 3 ripetizioni per punto (R-300-1)»: la claim dichiara il proprio metodo
  (griglia + ripetizioni), che e' la forma che impedisce la recidiva. Esito: ok.
- gas.py:621 — «sulle versioni precedenti … (non misurato qui)»: tenuta, con la motivazione giusta
  (il bersaglio e' un VPS con un Python che non e' questo). Esito: ok.
- gas.py:623 — «costruendo (inutilmente) altrettanti dict annidati, poi scartati per "recap
  mancante"»: il taglio dell'inciso e' riuscito, il concetto di lavoro sprecato resta in una parola.
  Esito: ok (controfattuale gia' verificato da me a 100k e 115k nei giri #299/#300; a 116k non l'ho
  rifatto — il motivo di scarto non dipende dalla profondita').
- gas.py:631 — _RIFLESSIONE_MAX_PROFONDITA = 50: invariato. Esito: ok.

3. Prova meccanica sui token non-COMMENT — codice bit-identico, confermato

  token non-commento HEAD: 29593 STAGED: 29593
  IDENTICI: True
  sha codice HEAD  : f49b717979008a2a
  sha codice STAGED: f49b717979008a2a

Esattamente i valori attesi. Ho inoltre riconfermato che HEAD:gas.py e' sempre lo stesso file dei
giri #299/#300 (sha256 014676d31b5fa75d8f26f6f2…), cosi' lo sha del flusso e' confrontabile fra i
tre giri. Il confronto include i token STRING -> docstring identiche. Conseguenza: _troppo_annidato
(gas.py:634), la guardia prima del parser (gas.py:679) -> json.loads (gas.py:683) -> rete
except RecursionError (gas.py:684) e il tetto 50 sono intatti; nessun gate toccato, nessuno slicing
di history, nessuna simulazione di tool. Nota: le righe della funzione sono scalate di +1 rispetto
al giro #300 perche' il blocco di commento e' cresciuto di una riga.

R-301-1 (COSMETICA) — claim nel report, non nel codice

«il blocco non e' cresciuto malgrado la riga in piu'» e' falso: le righe di commento sono
4 (HEAD) -> 11 (#299) -> 13 (#300) -> 14 (#301), misurate con awk. La compressione dell'inciso ha
recuperato una riga, la correzione di R-300-1 ne ha aggiunte due: netto +1. Non c'e' niente da
cambiare in gas.py (confermo il giudizio del giro #300: a 14 righe il blocco e' ancora difendibile,
perche' nessun test sorveglia queste claim e il commento e' l'unico registro della misura). Da
correggere e' la riga nell'handoff/report: la legge il verificatore esterno, ed e' la stessa classe
di claim non misurata che questa fetta sta chiudendo. Per lo stesso motivo tengo ferma
l'avvertenza: oltre ~15 righe, il posto giusto e' un file in reports/ con due righe di puntatore
nel codice.

R-gate-worktree-1 — registrato in memoria, con il confine di cio' che ho verificato

Preso in carico e scritto in memoria come lezione, non come riserva di questa fetta (l'hook e' nel
perimetro e vuole una fetta propria). Ho verificato NEL CODICE la meccanica descritta:
.claude/hooks/review_gate.sh:59 fa cd "$CLAUDE_PROJECT_DIR" incondizionato (attenzione: la riga e'
la 59, non la 58) e .claude/hooks/review_gate.sh:133 fa exit 0 appena il diff staged di quel
checkout non intercetta il perimetro, quindi senza mai leggere il marcatore. L'hook e' identico a
HEAD. Quello che NON ho verificato: il valore reale di CLAUDE_PROJECT_DIR in una sessione avviata
dentro un worktree — questa sessione gira nel checkout principale. Quindi l'inerzia del gate nei
worktree resta affermata dall'altra sessione e plausibile dal codice, non misurata da me. La
conseguenza che mi riguarda l'ho scritta in memoria: nelle sessioni in worktree i commit che ho
revisionato erano protetti dalla barriera primaria (l'agente che mi invoca), non dalla rete
deterministica — in worktree pretendero' la prova del giro di review, non l'esistenza del
marcatore.

Suite

Kernel 821 PASS, 0 FAIL rieseguito da me al giro #300 sullo stesso flusso di token (identico a
questo) e gia' verificato che i due soli test che leggono il sorgente come testo —
tests/test_unit_kernel.py:5752 (T74g, grep dei marcatori stub) e tests/test_unit_kernel.py:7242
(T79a, compile() di tutti i .py tracciati) — non sono scalfiti dal commento nuovo. In questo giro
non l'ho rieseguita: il codice e' bit-identico e il testo del commento non contiene i marcatori
vietati ne' escape.

Rischio esplicitamente escluso

(a) Python 3.11/3.12/3.13: non verificati, sulla macchina c'e' solo 3.14.7 — gas.py:621 resta
dichiaratamente non misurata e io non l'ho misurata. (b) VPS: la soglia dipende dallo stack del
thread principale e li' sara' un altro numero; irrilevante per la correttezza (il tetto 50 esiste
per questo), e la data/macchina sono ora scritte nel commento. (c) Suite kernel non rieseguita in
questo giro (motivo sopra); non ho rieseguito notte/voice/pytest completo in nessun giro.
(d) CLAUDE_PROJECT_DIR in un worktree: non riproducibile da questa sessione (vedi sopra).
(e) Non ho esaminato reports/* modificati in working tree ma non in stage: fuori dal perimetro e
fuori da questo diff.

Memoria aggiornata

.claude/agents/memoria_revisore.md — riga contatore #301 — 2026-10-12 — APPROVATO — … + 3 lezioni
nuove (il gate ancorato a CLAUDE_PROJECT_DIR e' inerte nei worktree e cosa pretendere li';
misurare le righe di un commento che cresce a ogni giro invece di fidarsi del «l'ho compresso»;
piu' la chiusura del confine adiacente). Committata da scripts/commit_memoria_revisore.sh ->
8f040f0, diff staged di gas.py lasciato intatto nell'index.

Verdetti nulli di questo giro: nessuno.
```

**R-301-1 è stata corretta nei report** (le righe di commento sono 4 → 11 → 13 → 14, non «non
cresciute»), insieme alla citazione `review_gate.sh:59` (avevo scritto :58) e alla separazione fra
ciò che ho misurato io e ciò che poggia sul report dell'altra sessione su R-gate-worktree-1.

## §5 DELTA TEST DEL MOTORE

Il commit di motore di questo giro (`3f59b6e`) cambia **solo un blocco di commento**: nessun delta
atteso, e nessuno misurato.

```
=== RIEPILOGO: 821 PASS, 0 FAIL ===
```

Il revisore ha provato **meccanicamente** che il codice eseguibile è bit-identico al commit
precedente: 29593 token non-COMMENT, sha del flusso `f49b717979008a2a` su entrambe le versioni,
docstring incluse. Ha inoltre verificato che i due soli test che leggono il sorgente **come testo**
(`tests/test_unit_kernel.py:5752` T74g, `tests/test_unit_kernel.py:7242` T79a) non siano scalfiti —
controllo che va fatto e non assunto, perché un commento può far cadere un grep-test.

Per riferimento, il delta della fetta completa (già in main con la PR #192): kernel **818 PASS /
1 FAIL → 821 PASS / 0 FAIL**, `pytest` **1031 passed, 1 skipped** invariato.

**FAIL fuori scope**: nessuno.

**NON VERIFICATO**: Python **3.11/3.12/3.13** — nessuno di quegli interpreti è installato su questa
macchina (solo `.venv` = 3.14.7). Lo dichiarano anche il revisore e la verifica esterna. La prova è
il solo job CI pinnato 3.11. Idem il **VPS**: la soglia di `json.loads` dipende dallo stack del
thread principale e lì sarà un altro numero — irrilevante per la correttezza, che è precisamente il
motivo per cui il tetto esplicito esiste.

## §6 STATO CI

`gh run list --branch fix/test-t80u5-portabile` (reale, mappato per SHA):

```
38277005239 a6fa2fd verifica-bot pull_request_target -> success
38277003024 a6fa2fd CI           push                -> success
38276929440 7fd062b verifica-bot pull_request_target -> cancelled
38276867649 7fd062b verifica-bot pull_request_target -> skipped
38276828217 7fd062b CI           push                -> success
```

**Mappatura commit→run OBBLIGATORIA** (una run per *push*, non per commit):

- `035c2d8`, `675a574`, `8f040f0`, `3f59b6e`, `696a37e`: **nessuna run su questi SHA alla scrittura
  dell'handoff** — non ancora pushati. `3f59b6e` è il commit di motore di questo giro.
- `a6fa2fd` e `7fd062b`: run elencate sopra, tutte success per CI; **appartengono alla parte della
  sessione già mergiata in main** con la PR #192, non a questo giro.
- Il commit di fine-task che contiene questo file: **run non ancora disponibile alla scrittura
  dell'handoff** (il suo hash non è noto mentre lo scrivo).

Avvertenza: i tre check required del ruleset `main-lock` (`unit-suite`, `handoff-check`,
`verifica-bot`) erano verdi su `a6fa2fd`, cioè sul contenuto **già mergiato**, e **non** sul commit
di questo giro. La copertura pre-merge della PR nuova è garantita da `gasmerge`
(`gh pr checks --watch`), non da questo campo.

## §7 RISERVE APERTE

**Di questa fetta — CHIUSE prima del commit** (elencate per tracciabilità):

- ✅ R-297-1 (BASSA) CHIUSA — input degenere ora CHIUSO (200k livelli, 1,2 MB), si cronometra la
  chiamata e non la costruzione della stringa: misurato **0,007 ms** con il motivo del tetto.
- ✅ R-297-2 (BASSA) CHIUSA — **T80u7** esercita la rete `except RecursionError` con un monkeypatch
  di `gas.json.loads`, e asserisce che il messaggio resti distinto da quello del tetto.
- ✅ R-297-3 (BASSA) CHIUSA — precondizione `str` dichiarata nella docstring di `_troppo_annidato`,
  con il chiamante che la garantisce. Scelta dichiarata: nessun `isinstance` interno.
- ✅ R-297-4 (COSMETICA) CHIUSA — claim sul costo reso esatto, commento stale di T80u5 corretto.
- ✅ R-298-1 (COSMETICA) CHIUSA — un commento dichiarava «2,2 MB» per un input di **1.200.001
  caratteri**: misura falsa in un commento, corretta nel test e in tutti i report.

**Di questa fetta — APERTE (COSMETICHE, non bloccanti):**

- 🟡 **R-298-2** (COSMETICA) — `tests/test_unit_kernel.py:7189`: `gas.json.loads = ...` non è un patch
  locale (`gas.json is sys.modules["json"]`), quindi per la durata della finestra ogni `json.loads`
  del processo è falsificato. Innocuo qui (una sola chiamata sincrona, `finally` + asserzione `is`),
  ma la forma pulita è `gas.json = finto` oppure `unittest.mock.patch.object`.
- 🟡 **R-298-3** (COSMETICA) — `tests/test_unit_kernel.py:7190`: se la rete `except RecursionError`
  venisse cancellata, l'eccezione uscirebbe dal `try/finally` del blocco T80 e ucciderebbe lo script
  (exit 1 e traceback: CI rossa, guasto NON silenzioso) ma senza riga RIEPILOGO e senza che T80u7
  compaia come FAIL. Catturare `BaseException` lo renderebbe un FAIL leggibile.

**Dal secondo giro (correzione di V-1, richiesta dell'operatore) — CHIUSE:**

- ✅ **R-299-1** (BASSA, l'osservazione più utile della fetta): il commento **citava verbatim** la
  frase falsa appena corretta; da PR #181/#184 Gas legge il proprio sorgente, quindi era testo
  ripescabile **senza la riga che la nega**. Chiusa: resta solo il puntatore, `grep` a zero.
- ✅ **R-299-2 / R-299-3** (COSMETICHE): claim ereditata dichiarata tale («sulle versioni precedenti
  … non misurato qui», tenuta perché il bersaglio è un VPS) e numeri ancorati a data, OS e versione.
- ✅ **R-300-1** (BASSA): «solleva RecursionError **solo** a 118k» era un'implicazione falsa (117k
  falla già). Chiusa stringendo la griglia finché pass e fail sono **adiacenti**: 116k parsa, 117k
  solleva, 3 ripetizioni per punto.
- ✅ **R-301-1** (COSMETICA, su un report e non sul codice): avevo scritto che il blocco di commento
  «non è cresciuto». Falso e misurato: **4 → 11 → 13 → 14 righe**. Corretta nei report.

**Finding NUOVO fuori scope, nome condiviso con la sessione sorella — CONTARLO UNA VOLTA SOLA:**

- 🔴 **R-gate-worktree-1** (MEDIA): in una sessione che gira in un **worktree** il gate
  deterministico di review è **inerte**. `.claude/hooks/review_gate.sh:59` fa
  `cd "$CLAUDE_PROJECT_DIR"` incondizionato e `review_gate.sh:133` fa `exit 0` appena il diff staged
  di *quel* checkout non intercetta il perimetro, **senza mai leggere il marcatore**; ogni worktree
  ha un proprio `.claude/.review_ok` mai consultato. **Confini della prova**: la struttura dell'hook
  e i marcatori per-worktree li ho misurati io e il revisore (#301) li ha confermati; che
  `CLAUDE_PROJECT_DIR` valga il checkout principale **anche dentro un worktree** NON è misurato da
  nessuno dei due (entrambi giriamo nel principale) e poggia sul report della sessione sorella più
  sul sintomo osservato. Conseguenza dichiarata: il commit di motore della PR #193 è passato per
  indice pulito, **non** per approvazione del gate; i commit di questa PR sì, perché questa sessione
  lavora nel principale. CLAUDE.md §3 dice che il gate deve proteggere se stesso: qui non lo fa.
  **Non corretto**: l'hook è nel perimetro e richiede fetta propria, review e verifica esterna.
- ⚠️ **Collisione dei numeri di review con la sessione sorella**: `origin/main` arriva a #296, questo
  ramo usa **#297–#301**, il ramo della sorella **#297–#300**. Non rinumerato di proposito: i numeri
  sono già in messaggi di commit pushati e riscriverli dentro i verdetti sarebbe ritoccare il testo
  del revisore (F-verdetto-ritoccato). Piano concordato fra le due sessioni: **chi mergia secondo
  rinumera le proprie righe** (le sue vanno spostate di **+5**, o rinumerate da #302, se entra prima
  questa PR) e il conflitto su `.claude/agents/memoria_revisore.md` si risolve **appendendo entrambe
  le serie**, non scegliendone una.

**Finding nuovi emersi in questa sessione, NON implementati:**

- 🟡 **F-ci-una-sola-versione** (BASSA, nuovo): la CI prova **una sola** versione di Python (3.11),
  quindi una divergenza come quella di T80u5 resta invisibile fino a quando qualcuno lancia la suite
  in locale. Il commento a `.github/workflows/ci.yml:44` («venv WSL è 3.12.3») è **stale**: il
  `.venv` di questa macchina è 3.14.7. Proposta: matrice `3.11` + la versione del venv dell'operatore.
- 🟡 **F-token-suffisso** (BASSA, nuovo, dal check della PR #184): `token*.json` con suffisso NON è
  coperto da `_CHIAVE_PRIVATA_RE` — `token_cache.json` è leggibile perché la regex vuole il punto
  subito dopo `token`. `tokenizer.py` resta correttamente leggibile.
- 🟡 **R-297-4-bis** (COSMETICA, segnalata dal revisore, fuori dal diff): `rifletti()` chiama
  `create` senza `max_tokens` (`gas.py:2786`), quindi la lunghezza della risposta grezza dipende dal
  default del provider.
- 🟡 **R-282-1 / R-283-1** (dal check): il budget di byte di `cerca_testo` mente — in carico alla
  sessione sorella, non a questa fetta.
- 🟡 **R-291-1 e bot #188 (2° giro)** (BASSE, preesistenti): `kubeconfig` senza punto, `mywallet.dat`,
  `.vault-token`, `.dockercfg`, `_netrc`, `clientsecret.json`, `*.gpg/*.asc`, `.config/gh/hosts.yml`
  restano leggibili.
- 🟡 **R-277-1** (BASSA, preesistente): `prod.environment` resta leggibile (compromesso dichiarato).
