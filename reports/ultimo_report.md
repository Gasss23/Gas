# ULTIMO REPORT — T80u5: il tetto di annidamento non dipende più dalla versione di Python

> Task del 2026-10-12, su richiesta dell'operatore («intanto apri una PR per sistemare T80u5»).
> Ramo: **`fix/test-t80u5-portabile`** (da `origin/main` = `f6396ba`).

## Il problema, misurato

Un check della sessione ha rilevato che sulla **main** la suite del kernel dà **818 PASS e 1 FAIL**
(`T80u5`) usando il `.venv` del progetto, che su questa macchina è **Python 3.14.7**.
La CI non lo vedeva perché pinna **Python 3.11** (`.github/workflows/ci.yml:44`, dove il commento
«venv WSL è 3.12.3» è stale rispetto a questa macchina).

`T80u5` asseriva che un JSON annidato 100.000 livelli venisse scartato con il motivo
«JSON annidato oltre il limite di ricorsione». Quell'esito dipendeva dal fatto che `json.loads`
sollevasse `RecursionError`. Misurato su 3.14.7: `json.loads` **parsa senza errore** annidamenti
da 200 fino a 100.000 livelli, quindi:

1. l'`except RecursionError` era **codice morto** su 3.14;
2. `_analizza_riflessione` costruiva **100k dict annidati** (misurati dal revisore: 1,2 MB di input
   → **18,4 MB di picco**, 36 ms) per poi buttarli e scartare l'input con un motivo **falso**
   («recap mancante» invece di «annidato»);
3. il motivo nel `gas_debug.log` **cambiava con la versione di Python**, su un input che arriva
   dal modello.

## Cosa ho cambiato

- **`gas.py`**: `_RIFLESSIONE_MAX_PROFONDITA = 50` e la funzione pura `_troppo_annidato()`, che conta
  l'annidamento di `{`/`[` **solo fuori dalle stringhe JSON** (gestisce l'escape `\`) ed **esce al
  primo sforamento**. `_analizza_riflessione` controlla il tetto **prima** di `json.loads` e scarta
  con «JSON annidato oltre il limite (50 livelli)». L'`except RecursionError` **resta** come rete di
  sicurezza, con il suo messaggio distinto.
- **`tests/test_unit_kernel.py`**: `T80u5` aggiornata al messaggio nuovo; **T80u6** (confine esatto
  50 vs 51, parentesi dentro le stringhe e dopo un escape non contano, JSON legittimo ancora
  accettato, uscita anticipata su 1,2 MB di input annidato); **T80u7** (la rete `except
  RecursionError` è viva e il suo messaggio resta distinto da quello del tetto).

Il tetto è una **costante di modulo, non configurabile da env di proposito**: una riflessione
legittima è profonda 2, il margine è 25x, e un `GAS_...=0` renderebbe `_troppo_annidato` sempre vera,
cioè **ogni** riflessione rifiutata e la cascata a 4 rung bruciata a ogni turno (verificato dal
revisore con `limite=0/-1/-100`).

## Numeri REALI

| Misura | Base (`f6396ba`) | Dopo |
|---|---|---|
| Suite kernel (`.venv`, Python 3.14.7) | **818 PASS, 1 FAIL** (T80u5) | **821 PASS, 0 FAIL** |
| `pytest -q` | 1031 passed, 1 skipped | **1031 passed, 1 skipped** |

Sonda con `sys.setrecursionlimit(80)`: il tetto scatta prima di `json.loads`, nessuna eccezione
sfugge, messaggio identico.

**NON VERIFICATO**: il comportamento su **Python 3.11/3.12**. Su questa macchina esiste solo il
`.venv` (3.14.7) e non ho installato altri interpreti. La prova è la **CI** (`unit-suite`, pinnata
3.11). Il tetto però short-circuita prima del parser, quindi l'esito non può dipendere dal parser.

## Review

Review **#297 APPROVATO CON RISERVE** → quattro riserve, **tutte corrette prima del commit**:

- **R-297-1** (BASSA) — difetto reale del mio test: l'input degenere `'{"a":'*2000000 + '1'` **non
  arrivava mai** al tetto (senza `}` finale scattava `j <= i`), e il cronometro misurava la
  costruzione della stringa. **CHIUSA**: input ora CHIUSO (200k livelli, 1,2 MB), si cronometra la
  chiamata, misurato **0,007 ms** con il motivo del tetto.
- **R-297-2** (BASSA) — la rete `except RecursionError` restava senza nessun test e sopravviveva solo
  grazie a un commento. **CHIUSA**: T80u7 la esercita forzando `json.loads` a sollevare.
- **R-297-3** (BASSA) — `_troppo_annidato` solleva `TypeError` su input non-`str` ed è documentata
  «PURA». **CHIUSA**: precondizione dichiarata nella docstring, con il chiamante che la garantisce.
- **R-297-4** (COSMETICA) — claim sul costo imprecisa e commento stale di T80u5. **CHIUSA**.

Il revisore ha verificato che i test **mordono**, con due mutazioni su `gas.py`: `return False` in
testa a `_troppo_annidato` → 2 FAIL; ingresso in stringa ignorato → 1 FAIL.

## Secondo giro: verifica esterna #192 e correzione di V-1 (richiesta dell'operatore)

La verifica esterna della PR #192 ha dato **APPROVATO CON RISERVE** con cinque finding tutti
BASSA/COSMETICA, nessun gate indebolito e **nessun bypass del tetto** trovato con una batteria
avversaria. Ha riprodotto in autonomia i numeri dichiarati (818/1 FAIL alla base, 821/0 dopo,
pytest 1031) e la mutazione che fa mordere i test.

**V-1 (BASSA) era un errore mio e l'operatore ha chiesto di correggerlo prima del merge**: il
commento sopra `_RIFLESSIONE_MAX_PROFONDITA` diceva «da 3.14 `json.loads` le parsa», ma a 200k
livelli solleva `RecursionError` anche su 3.14.7. Misura falsa scritta da me, la classe di difetto
di cui questo progetto è più severo.

La correzione ha prodotto la review **#299 APPROVATO CON RISERVE**, con tre riserve **nel fix
stesso**, tutte chiuse nel giro successivo:

- **R-299-1** (BASSA, l'osservazione più importante): il mio commento **citava verbatim la claim
  falsa** dentro `gas.py`. Da PR #181/#184 Gas legge il proprio sorgente con gli strumenti nativi,
  quindi quella frase è testo **ripescabile senza la riga che la nega**. CHIUSA: nel sorgente resta
  solo il puntatore alla verifica, e un grep conferma che non c'è più traccia della frase falsa.
- **R-299-2** (COSMETICA): «fino a 3.12» era una claim ereditata e non misurata, e 3.13 non era
  citata. CHIUSA: «sulle versioni precedenti … (non misurato qui)».
- **R-299-3** (COSMETICA): i numeri non avevano ancoraggio. CHIUSA: «misura del 2026-10-12, macOS
  arm64, Python 3.14.7».

**Misure riprodotte da me, non prese dal revisore** (una delle sue era larga): la soglia non è fra
100k e 120k ma **fra 116k e 117k**, su valori ADIACENTI e con 3 ripetizioni per punto (griglia da
1000: 114k/115k/116k PARSED, 117k/118k `RecursionError`). La prima stesura di questa riga diceva «fra
115k e 118k», che è **non adiacente** e quindi della stessa classe di difetto che la fetta chiude:
trovata da V-1 della verifica esterna #195 e corretta qui. Confermato
nei due sensi che `json` **ignora** `sys.getrecursionlimit()` (limite 50 → 1000 livelli passano;
limite 5.000.000 → 200k no) e segue invece **lo stack C del thread** (`threading.stack_size` a
512 MB → 200k livelli passano; a 1 MB → falliscono anche 50k). È la prova che senza tetto esplicito
il comportamento dipende dalla **macchina**, non solo dalla versione di Python: la giustificazione
del tetto regge sul meccanismo, non sul numero.

Suite invariata dal cambio di commento: kernel **821 PASS, 0 FAIL**.

**Riserve ancora aperte** per decisione dell'operatore (solo V-1 prima del merge): **V-2/R-298-3**
(se la rete `except RecursionError` sparisse, la suite morirebbe senza riga RIEPILOGO: CI rossa,
quindi non silenzioso, ma illeggibile) e **V-3/R-298-2** (`gas.json.loads` falsifica il `json.loads`
di tutto il processo per la durata della finestra; innocuo oggi).

## Terzo e quarto giro: la stessa classe di difetto, altre due volte

Correggere V-1 ha prodotto **altri due** finding della stessa famiglia nel fix stesso. Entrambi
legittimi, entrambi chiusi.

- **R-299-1** (review #299, BASSA): il commento nuovo **citava verbatim** la frase falsa appena
  corretta. Da PR #181/#184 Gas legge il proprio sorgente con gli strumenti nativi, quindi quella
  citazione è testo **ripescabile senza la riga che la nega**. Chiusa: nel codice resta solo il
  puntatore, e un `grep` conferma zero tracce. È l'osservazione più utile dell'intera fetta.
- **R-300-1** (review #300, BASSA): avevo scritto «solleva RecursionError **solo** a 118k». Le due
  affermazioni letterali erano vere, ma «solo» implica che prima di 118k non si fallisca, e **117k
  fallisce già**: la mia griglia di misura era troppo larga. Chiusa: rimisurato con valori
  **adiacenti** e 3 ripetizioni per punto (114k/115k/116k PARSED, 117k/118k RecursionError), il
  confine cade fra 116k e 117k. Il revisore ha dichiarato larga anche la propria stima precedente.

Lezione di metodo, registrata nella memoria del revisore: **una claim di confine è provata solo se
pass e fail sono ADIACENTI nella griglia misurata e la coppia regge su più ripetizioni.** Campionare
115k e 120k e scrivere «fallisce solo a 118k» lascia dentro un «solo» falso.

Il revisore ha inoltre provato **meccanicamente** che si tratta di un cambio di solo commento,
confrontando i token non-COMMENT con HEAD (29593 token, stesso sha del flusso), e ha verificato che i
due test che leggono il sorgente come testo (T74g, T79a) non siano scalfiti — controllo che va fatto
e non assunto, perché un commento può far cadere un grep-test.

- **R-301-1** (review #301, COSMETICA): avevo affermato che il blocco di commento «non è cresciuto»
  malgrado le correzioni. **Falso, e misurato**: le righe di commento sono andate **4 (HEAD) → 11
  (#299) → 13 (#300) → 14 (#301)**. Comprimere un inciso non compensa due righe di correzione
  aggiunte. È la stessa classe di claim non misurata che questa fetta stava correggendo — stavolta in
  un report, non nel codice, cioè in un file che legge anche il verificatore esterno. Corretta qui.

Review **#301 APPROVATO** (secco, nessuna riserva bloccante): confine 116k/117k riprodotto in un
processo nuovo, `grep` di controllo a zero occorrenze delle frasi false dei giri precedenti, e codice
eseguibile ancora bit-identico a HEAD.

## Finding NUOVO fuori scope: il gate di review è inerte nei worktree

**R-gate-worktree-1** (MEDIA, nome condiviso con la sessione sorella — **contarlo una volta sola**).
`.claude/hooks/review_gate.sh:59` fa `cd "$CLAUDE_PROJECT_DIR"` incondizionato, e quello resta il
checkout principale: in una sessione che gira in un **worktree** l'hook ispeziona l'indice sbagliato.
Se l'indice del principale è pulito, `review_gate.sh:133` fa `exit 0` **senza nemmeno leggere il
marcatore**, quindi un worktree può committare un diff di `gas.py`/`modules/`/`tests/` mai
revisionato.

**Confini della prova** (distinzione necessaria, è il tema di questa fetta): ho **misurato io** la
struttura dell'hook (il percorso di `exit 0` prima di ogni lettura del marcatore) e l'esistenza di un
`.claude/.review_ok` **per-worktree** mai consultato, con date diverse. **NON ho misurato** che
`CLAUDE_PROJECT_DIR` valga il checkout principale anche dentro una sessione in worktree: questa
sessione gira nel principale, quindi quel pezzo poggia sul report della sessione sorella e sul
sintomo osservato (il mio `gas.py` in stage che blocca i suoi commit, spiegabile solo così). Il
revisore al giro #301 ha confermato la struttura e ha dichiarato a sua volta di non aver verificato
quel valore. Chi chiude il finding deve misurarlo da dentro un worktree.

Conseguenza dichiarata: il commit del motore della PR #193 è passato **per indice pulito, non per
approvazione del gate**; l'ha protetto la barriera PRIMARIA (invocazione reale del revisore). I
commit della PR #192 **sono** stati protetti, perché questa sessione lavora nel checkout principale.
CLAUDE.md §3 dice che il gate deve proteggere se stesso: qui non lo fa. **NON corretto qui** — l'hook
è nel perimetro di review e richiede fetta propria, review e verifica esterna.

## Proposte NON implementate (fuori perimetro di questa fetta)

1. **`ci.yml:44`**: il commento sulla versione del venv è stale (dice 3.12.3, questa macchina ha
   3.14.7). Soprattutto: **la CI prova una sola versione di Python**, quindi una divergenza come
   questa resta invisibile. Proposta: matrice `3.11` + la versione del venv dell'operatore.
2. **Buchi residui della denylist credenziali** (dal check delle PR #184/#185, non toccati qui):
   `token*.json` con suffisso — `token_cache.json` è leggibile perché la regex vuole il punto subito
   dopo `token` — più i già tracciati `kubeconfig` senza punto, `mywallet.dat`, `.vault-token`,
   `.dockercfg`, `_netrc`, `clientsecret.json`, `*.gpg/*.asc`.
3. **`rifletti()` chiama `create` senza `max_tokens`** (`gas.py:2786`, nota del revisore R-297-4):
   la lunghezza della risposta grezza dipende dal default del provider.
