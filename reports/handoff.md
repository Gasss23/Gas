# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-12 — check delle PR #184/#185 + fetta T80u5 (il tetto di annidamento non dipende più dalla versione di Python)

---

## §0 DECISIONI UMANE RICHIESTE

1. **Merge della PR #192** (https://github.com/Gasss23/Gas/pull/192) — numero e URL dall'output reale
   di `gh pr view --json number,url`: `{"number":192,"url":"https://github.com/Gasss23/Gas/pull/192"}`.
   Il verdetto del bot non è ancora noto: finché non è `APPROVATO` secco senza finding, per la regola
   di merge autonomo di CLAUDE.md **decide l'operatore**. Etichetta `verifica` applicata.
   Stato al momento della scrittura (`ccd_pr get_status`): `MERGEABLE`, `mergeStateStatus: BLOCKED`,
   check 1 passing / 0 failing / 2 pending / 2 skipped.
2. **Conflitto di merge annunciato** (conseguenza, non errore): la sessione sorella
   `cerca_testo: il budget di byte non deve mentire` lavora sullo stesso `tests/test_unit_kernel.py`
   e sullo stesso `.claude/agents/memoria_revisore.md` in un altro worktree. Il **secondo** dei due
   merge avrà un conflitto da risolvere a mano. Decide l'operatore quale ramo mergiare prima.
3. **PR #184 è stata mergiata fuori dalla regola di merge autonomo** (bot `APPROVATO CON RISERVE`,
   non `APPROVATO` secco). L'handoff di #184 dichiarava un'autorizzazione esplicita dell'operatore
   in chat del 2026-10-11, che è l'eccezione prevista: annotato qui su richiesta dell'operatore.
4. **`F-ci-una-sola-versione`**: decidere se la CI deve provare più di una versione di Python. Oggi
   pinna solo 3.11, e per questo il FAIL di T80u5 su 3.14 è vissuto invisibile fino a una run locale.

## §1 SCOPE & ESITO FETTE

- **Check delle PR #184 e #185** (richiesto dall'operatore): `FATTO` — su cloni usa-e-getta nella
  scratchpad, repo reale non toccato. Esiti provati:
  - entrambe le PR erano **già mergiate** (2026-10-11); tutti i check verdi sui due SHA pinnati
    (#184 `verifica-bot` success, #185 `neutral` perché tocca `scripts/`): dichiarato correttamente
    nei rispettivi handoff;
  - il punto «credenziali illeggibili» del brief dell'operatore era **già in produzione** (PR #188,
    `_CHIAVE_PRIVATA_RE` in `modules/gate/gate.py`): rifarlo sarebbe stato lavoro duplicato;
  - il punto «budget di byte di `cerca_testo`» è **reale e aperto**, riprodotto: con un
    `gas_debug.log` da 4,5 MB, `cerca_testo "def gate_classify"` dalla root dà «0 righe trovate in 13
    file; 64 file oltre il tetto di byte saltati» e NON trova `modules/gate/gate.py`; togliendo il
    log lo trova (77 file). Causa: lo skip per-file confronta col budget RESIDUO;
  - **buco nuovo nella denylist credenziali**, non tracciato altrove: `token*.json` con suffisso
    (`token_cache.json` è leggibile, la regex vuole il punto subito dopo `token`).
- **Fetta T80u5 — tetto di annidamento deterministico**: `FATTA` — commit `c298d59`, review #297 e
  #298 APPROVATO CON RISERVE, tutte le riserve bloccanti o fattuali chiuse prima del commit.
- **Fetta «budget di byte di `cerca_testo`»**: `DEFERITA — affidata alla sessione sorella`
  (`cerca_testo: il budget di byte non deve mentire`), che al momento attende il proprio revisore.
- **Punto 2 del brief dell'operatore (credenziali illeggibili)**: `SALTATA — già in main con la PR
  #188`; i buchi residui sono proposti, non implementati (§7).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 gas.py                             |  47 ++++++++++++++++++++++++++++++++++++++++++-
 reports/diff_sessione.md           |  40 ++++++++++++++++++++++++++++--------
 reports/handoff.md                 | 397 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------
 reports/stato_progetto.md          |  18 ++++++++++++++++-
 reports/ultimo_report.md           |  90 +++++++++++++++++++++++++++++++++++++++++++++++++++------------
 tests/test_unit_kernel.py          |  56 ++++++++++++++++++++++++++++++++++++++++++++++++---
 7 files changed, 459 insertions(+), 195 deletions(-)
```

Generato con `git -c core.quotePath=false diff --cached --stat=400 f6396ba` con i report già in stage.
Il **set di file** (7 path) è esatto. I conteggi di riga di `reports/handoff.md` sono approssimati per
costruzione: il file conta se stesso, e questa stessa riscrittura di §2/§3/§6 ne cambia il totale.
La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
c298d59 fix(riflessione): tetto di annidamento deterministico, non più legato alla versione di Python
4017ee5 chore(revisore): memoria review #298 — APPROVATO CON RISERVE
6f6f370 chore(revisore): memoria review #298 — APPROVATO CON RISERVE
06636d5 chore(revisore): memoria review #297 — APPROVATO CON RISERVE
```

NB: `4017ee5` e `6f6f370` hanno lo **stesso messaggio** perché lo script del revisore
(`scripts/commit_memoria_revisore.sh`) è stato eseguito due volte nel giro #298. Riportati verbatim,
non accorpati. Il commit di fine-task che contiene questo file non compare qui, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore della sessione: **`c298d59`** (`gas.py` + `tests/test_unit_kernel.py`).

La fetta ha avuto **due giri** di review. Il giro **#297** (APPROVATO CON RISERVE) riguardava un diff
poi **superato**: le sue quattro riserve R-297-1..4 sono state chiuse e il suo testo cita righe non
più valide, quindi NON è il verdetto di gate e non è incollato qui (sintesi in §7). Il verdetto di
gate, emesso sul diff effettivamente committato, è il **#298**, incollato INTEGRALE:

```
VERDETTO: APPROVATO CON RISERVE

Secondo giro (review #298, memoria aggiornata e committata: 4017ee5). Letture obbligatorie rifatte
prima del giro: CLAUDE.md (sez. 5/8/9), reports/stato_progetto.md, .claude/agents/memoria_revisore.md
(ultima riga #297, mia del giro precedente).

Le quattro riserve sono CHIUSE, tutte con evidenza misurata. Le tre riserve nuove sono COSMETICHE e
non bloccano il commit; una sola ti consiglio di correggerla prima (un numero falso in un commento),
cosi' non serve un terzo giro.

Elementi del diff esaminati

1. tests/test_unit_kernel.py:7163 — _chiuso80 = '{"a":'*200000 + '1' + '}'*200000, cronometro sulla
   CHIAMATA a _troppo_annidato e non sulla costruzione. Rischi esaminati: (a) soglia fragile,
   (b) peso di memoria. Esito: ok, R-297-1 chiusa. Misurato: 20 chiamate consecutive, min 0,0060 ms
   / max 0,0095 ms contro la soglia di 50 ms -> margine ~5000x; il loop non allocca (iterare una str
   ASCII riusa i caratteri in cache) quindi non e' esposto a pause del GC: non e' fragile su un
   runner lento. Memoria: len(_chiuso80) = 1.200.001 caratteri e, verificato, testo.strip() e lo
   slice completo t[0:len(t)] restituiscono lo stesso oggetto (is -> True), quindi
   _analizza_riflessione(_chiuso80) non fa copie: ~1,2 MB in tutto, trascurabile nella suite. Il
   test ora dimostra davvero l'uscita anticipata (dt=0.008ms motivo='JSON annidato oltre il limite
   (50 livelli)' nel PASS) e non cade piu' su j <= i.

2. tests/test_unit_kernel.py:7189 (T80u7) — sostituzione di gas.json.loads con una funzione che
   solleva RecursionError, try/finally, tre asserzioni (messaggio distinto, ripristino con is,
   riflessione normale dopo). Rischi esaminati: (a) colpisce il json giusto, (b) puo' sporcare i
   test successivi. Esito: ok, R-297-2 chiusa, con una nota. Colpisce quello giusto: verificato che
   gas.json is sys.modules["json"] -> True, quindi la funzione globale json usata da
   _analizza_riflessione e' esattamente quella patchata (provato a mano: con il patch attivo
   _analizza_riflessione('{"recap": "ok"}') -> (None, 'JSON annidato oltre il limite di ricorsione')).
   Non sporca i successivi: finally + asserzione is + rilettura valida nello stesso check. La nota e'
   che per lo stesso motivo il patch e' globale al processo (vedi R-298-2).

3. gas.py:627 — docstring con PRECONDIZIONE str (e chi la garantisce) e claim di costo esatto
   (O(limite) solo sul degenere annidato, O(len) sulla stringa lunga e piatta). Rischio esaminato:
   claim ancora piu' larga della realta'. Esito: ok, R-297-3 e R-297-4 chiuse — il testo ora coincide
   con quello che ho misurato nel giro #297 (0,10 s su 5 M caratteri dentro una stringa). Corretto
   anche il commento stale di T80u5 («oltre il tetto»). Codice di _troppo_annidato e
   _analizza_riflessione invariati rispetto al diff che avevo gia' verificato riga per riga sugli
   input ostili: non ho rifatto quella batteria, solo le mutazioni.

Mutazioni rifatte (6, eseguite e ripristinate; gas.py verificato identico a fine giro)

  _troppo_annidato -> return False in testa          : T80u5 + T80u6 FAIL (819/2)
  ingresso in stringa ignorato (if False)            : T80u6 FAIL (820/1)
  confine profondita > limite -> >=                  : T80u6 FAIL (820/1), il confine a 50 morde
  controllo del tetto disattivato (if False and ...)  : T80u5 + T80u6 FAIL (819/2)
  rete except RecursionError rimossa                 : traceback RecursionError, exit 1, nessuna
                                                       riga RIEPILOGO (vedi R-298-3)
  messaggio della rete reso identico a quello del tetto : T80u7 FAIL (820/1)

Suite pulita riprodotta: kernel 821 PASS / 0 FAIL, pytest 1031 passed, 1 skipped (148 s).

Riserve nuove — tutte COSMETICHE, nessuna bloccante

- R-298-1 (COSMETICA, ti consiglio di correggerla ora) — tests/test_unit_kernel.py:7180: il commento
  dice «su 2,2 MB di input», ma _chiuso80 e' 1.200.001 caratteri ~ 1,2 MB ('{"a":' sono 5 caratteri:
  5x200.000 + 1 + 200.000). E' una misura falsa in un commento, cioe' la cosa di cui questo progetto
  e' piu' severo: una riga da cambiare.
- R-298-2 (COSMETICA) — tests/test_unit_kernel.py:7189: gas.json.loads = ... non e' un patch locale:
  gas.json E' il modulo stdlib (gas.json is sys.modules["json"] -> True, e da un import indipendente
  json.loads is boom -> True), quindi per la durata della finestra ogni json.loads del processo e'
  falsificato. Qui e' innocuo (finestra di una sola chiamata sincrona, suite a thread singolo,
  finally + asserzione is), ma la forma pulita e' sostituire il nome nel namespace di gas
  (gas.json = finto) o usare unittest.mock.patch.object.
- R-298-3 (COSMETICA) — tests/test_unit_kernel.py:7190: se un domani la rete viene cancellata, la
  RecursionError esce dal try/finally del blocco T80 e uccide lo script: exit 1 e traceback (quindi
  la CI diventa rossa, il guasto non e' silenzioso), ma nessuna riga RIEPILOGO e T80u7 non compare
  come [FAIL], e tutti i check successivi non girano. Catturare BaseException in _rete80 lo
  trasformerebbe in un FAIL leggibile. Stessa famiglia della lezione del 2026-10-11 su T83.

La tua domanda su R-297-3: precondizione documentata o isinstance interno?

Tieni la precondizione documentata, come hai fatto. Un isinstance interno dovrebbe decidere cosa
ritornare, e per un guardiano l'unico default plausibile (return False) sarebbe fail-open: un input
non-str salterebbe il tetto e finirebbe in json.loads, che solleva TypeError raccolta da gas.py:674
-> «JSON non decodificabile». Oggi innocuo, ma un cancello non deve avere un default permissivo, e un
TypeError rumoroso su una precondizione violata e' preferibile a un False silenzioso. Con un solo
chiamante che garantisce il tipo (isinstance a gas.py:655), documentare e' la scelta giusta. Se un
giorno aggiungi un secondo chiamante, la decisione va rivista in quel momento.

Rischio escluso esplicitamente

Python 3.11/3.12 non verificato in locale: su questa macchina esiste solo .venv (3.14.7), nessun
altro interprete installato. Tutto cio' che riguarda il ramo RecursionError «vero» su <=3.12 resta
non riprodotto e la prova e' solo la CI unit-suite pinnata 3.11 — con l'aggiunta che adesso T80u7
copre quel ramo su ogni versione per iniezione, che e' esattamente il punto di R-297-2. Non ho
inoltre ri-verificato in questo giro la batteria di input ostili su _troppo_annidato (codice identico
al giro #297, dove l'ho misurata) ne' toccato nulla con provider reali o sul VPS.

Nota di procedura

Index intatto: restano staged solo gas.py e tests/test_unit_kernel.py; i reports/ modificati sono
tuoi e non staged. Prima del commit ricalcola il marcatore con bash scripts/segna_review_ok.sh (se
correggi R-298-1 il diff cambia: rifai il marcatore dopo la correzione — e' una riga di commento in
un test, non serve un terzo giro di review).

Memoria: riga #298 in .claude/agents/memoria_revisore.md + 2 lezioni nuove (come si giudica una
soglia di tempo in un test; modulo.sottomodulo.funzione = finto non e' un patch locale),
commit 4017ee5.
```

**R-298-1 è stata corretta prima del commit** (il commento a `tests/test_unit_kernel.py:7180` ora dice
«1,2 MB di input (1.200.001 caratteri)»), marcatore di review rigenerato dopo la correzione e suite
rilanciata: 821 PASS / 0 FAIL. R-298-2 e R-298-3 restano aperte come COSMETICHE (§7).

## §5 DELTA TEST DEL MOTORE

Base della sessione (`f6396ba`), eseguita sul clone usa-e-getta con il `.venv` del progetto
(**Python 3.14.7**):

```
=== RIEPILOGO: 818 PASS, 1 FAIL ===
  FAIL: T80u5 anteprima/parser robusti su repr che solleva, ricorsione, repr multiriga; secondo repr sempre (testo del modello tra apici)
```

Con il diff di questa fetta:

```
[PASS] T80u5 anteprima/parser robusti su repr che solleva, ricorsione, repr multiriga; secondo repr sempre (testo del modello tra apici)
[PASS] T80u6 tetto di annidamento deterministico: in-stringa e escape non contano, confine esatto, uscita immediata sull'input degenere — dt=0.007ms motivo='JSON annidato oltre il limite (50 livelli)'
[PASS] T80u7 rete except RecursionError viva e con messaggio distinto dal tetto — rete=(None, 'JSON annidato oltre il limite di ricorsione')
=== RIEPILOGO: 821 PASS, 0 FAIL ===
```

`pytest -q`: **1031 passed, 1 skipped** sia alla base sia dopo (nessuna regressione).

Mutazione eseguita da me (oltre a quelle del revisore), per provare che i test mordono: `return False`
in testa a `_troppo_annidato` → `819 PASS, 2 FAIL` (T80u5 e T80u6). `gas.py` ripristinato dall'index.

**FAIL fuori scope**: nessuno. Il FAIL alla base (T80u5) è **esattamente** l'oggetto di questa fetta
ed è chiuso.

**NON VERIFICATO**: il comportamento su Python **3.11/3.12** — non sono installati su questa
macchina (`python3.11/3.12/3.13` assenti, `.venv` = 3.14.7). La prova sarà la CI, pinnata 3.11
(`.github/workflows/ci.yml:44`). Il tetto short-circuita prima del parser, quindi l'esito non può
dipendere dalla versione del parser, ma questo è un ragionamento, non una misura.

## §6 STATO CI

`gh run list -L 3` (output reale, al momento della scrittura — **prima** del push di questo branch):

```
completed	success	Merge pull request #191 from Gasss23/feat/merge-automatico-z1xjx2	CI	feat/merge-automatico-z1xjx2	push	38258382161	1m40s	2026-10-12T13:49:14Z
completed	success	Merge pull request #191 from Gasss23/feat/merge-automatico-z1xjx2	CI	main	push	38258328218	1m32s	2026-10-12T13:48:47Z
completed	success	feat(budget): budget ricontrollato prima di ogni chiamata (FETTA 1 cervello forte, chiude F2)	verifica-bot	feat/merge-automatico-z1xjx2	pull_request_target	38246062974	3m35s	2026-10-12T11:58:16Z
```

Le tre run elencate appartengono al branch `feat/merge-automatico-z1xjx2` e a `main`: **nessuna** è
di questa sessione. Sono riportate perché il flusso chiede l'output reale del comando.

**Mappatura commit→run di questa sessione** (obbligatoria, nessuna formula collettiva):

- `06636d5` (memoria revisore #297): **nessuna run su questo SHA** — commit intermedio, mai testato
  da solo; il suo contenuto entra nell'albero di `c298d59`.
- `6f6f370` (memoria revisore #298, 1ª esecuzione): **nessuna run su questo SHA** — idem.
- `4017ee5` (memoria revisore #298, 2ª esecuzione): **nessuna run su questo SHA** — idem.
- `c298d59` (motore, testa del branch al momento del push): **run non ancora disponibile alla
  scrittura dell'handoff**. GitHub Actions crea una run per *push*, non per commit: la run del push
  testerà l'albero di questo commit (o del commit di fine-task, se è lui la testa).
- commit di fine-task (contiene questo file): **run non ancora disponibile alla scrittura
  dell'handoff** — per costruzione il suo hash non è noto mentre lo scrivo.

L'esito reale della run va aggiornato qui dopo il push (`gh run watch`). La copertura pre-merge è
garantita da `gasmerge` (`gh pr checks --watch`), non da questo campo.

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
