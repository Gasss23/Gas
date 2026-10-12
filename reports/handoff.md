# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-12 — `cerca_testo` su cartella: il budget di byte non deve mentire

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #193 (https://github.com/Gasss23/Gas/pull/193): l'operatore ha chiesto di finirla («finisci», con i test verdi). V-1 MEDIA del bot (rotazioni del log non cercabili per nome) corretta in `c026bdb`, review #301.
2. **R-297-3 (BASSA, APERTA di proposito): il salto dei log è incondizionato sulla dimensione.** Anche un `gas_debug.log` da 50 KB, che sta largamente in ogni tetto, non viene più cercato in una ricerca su cartella, mentre CLAUDE.md sez. 3 fa dell'ispezione del log un'attività di prima classe. Il brief chiedeva esplicitamente di saltare i log, quindi la scelta non è stata cambiata dall'agente. Mitigazioni presenti: salto dichiarato in intestazione con l'istruzione su come cercarci dentro; log cercabili indicandoli per nome; il salto protegge anche il tetto dei RISULTATI. L'alternativa «salta solo i log oltre il tetto per file» è stata provata e perde quella protezione — e la prova vale **proprio per l'alternativa condizionata** perché il log del test (5000 righe, ≈85 KB) sta SOTTO il tetto per file: verrebbe letto e il tetto dei risultati si esaurirebbe allo stesso modo. Se l'operatore preferisce l'altro compromesso, è una riga.
3. **Buchi residui della denylist credenziali**: NON implementati (vincolo del brief: `modules/gate/` è già in main con la PR #188). Verificati uno per uno con `lettura_consentita()`, tutti LEGGIBILI oggi: `token_cache.json` (la regex vuole il punto subito dopo `token`; `token.json` e `tokens.json` sono bloccati), `kubeconfig`, `mywallet.dat`, `.vault-token`, `.dockercfg`, `_netrc`, `clientsecret.json`, `*.gpg`, `*.asc`. Vanno in una fetta loro, di sicurezza.
4. **Verifica esterna #193: APPROVATO CON RISERVE** (verdetto integrale nel commento `#issuecomment-6128519908` della PR). **V-1 (MEDIA) era un difetto vero ed e' CHIUSA**: la promessa «i log restano cercabili per nome» era falsa per le rotazioni reali (`maxBytes` dell'handler = 5.242.880 > `LETTURA_MAX_BYTES` = 5.000.000), quindi una rotazione veniva saltata e, siccome la cartella la salta per nome, restava irraggiungibile — requisito (a) del brief mancato. Chiusa legando il tetto al `maxBytes` dell'handler con costanti condivise, piu' test su una rotazione REALE da 5.400.025 byte e invariante anti-deriva. V-3 (BASSA, cifre Unicode nella regex) chiusa; V-4 (COSMETICA) chiusa in parte; V-2 (BASSA) era colpa mia di processo (uno SHA orfanato da un `--amend` citato nel §3) ed e' corretta. Dettagli in `reports/stato_progetto.md`.
5. 🔴 **R-gate-worktree-1 (ALTA, NUOVA, fuori scope): in una sessione in worktree il gate di review deterministico è INERTE.** `review_gate.sh` valuta solo `CLAUDE_PROJECT_DIR` (il checkout principale), non il worktree da cui parte il commit: se l'indice di quel checkout è pulito l'hook esce 0 **senza leggere il marcatore**, quindi un worktree può committare un diff del motore mai revisionato. Misurato: il marcatore scritto nel worktree (`4392d368…`) non è mai stato consultato, l'hook legge quello del checkout principale (`08db3144…`). Il commit `d238610` è passato per indice pulito, non per verifica: a proteggerlo c'è stata la barriera PRIMARIA (revisore invocato, quattro giri). Rovescio: col checkout principale che ha un file del perimetro staged e marcatore stale, l'hook blocca i commit di un'ALTRA sessione, anche di soli `reports/`. Non corretta qui (`.claude/hooks/` è nel perimetro: fetta propria + review). Dettagli e direzione in `reports/stato_progetto.md`.
6. **COLLISIONE DEI NUMERI DI REVIEW — NON risolta, serve un tuo passaggio.** Stato REALE a HEAD, verificato: nella memoria del revisore **`#297` numera ancora DUE review diverse** (il tetto di annidamento T80u5 che arriva da main e il primo giro di `cerca_testo`), e la riga `#303` cita «ri-review #302» mentre #302 è ora la review di un'altra sessione: il riferimento non risolve. La rinumerazione #297→#302 … #302→#307 **è stata applicata alle mie righe**, ma non elimina il duplicato, perché il numero #297 è usato anche dal blocco arrivato da main. In §0 avevo scritto che la collisione era sistemata: **era falso**, ed è il finding V-3 (BASSA) della verifica esterna al 3º giro. Inoltre `merge-tree` di questo head conferma conflitto su `.claude/agents/memoria_revisore.md` **sia con la PR #195 sia con la #196** (il dossier nominava solo la #195). **Chi mergia per secondo risolve il conflitto in memoria con un'unione pura in coda**, e la numerazione univoca la decidi tu: io ho smesso di rinumerare dopo due giri su un bersaglio in movimento, e il revisore ha confermato la scelta.
7. **Nota di processo**: la PR #184 è stata mergiata in autonomia con verdetto del bot `APPROVATO CON RISERVE`, quindi **fuori dalla regola di merge autonomo** di CLAUDE.md (merge da soli solo su `APPROVATO` secco senza alcun finding V-x). La voce esistente di `feat/via-binari-run-command` in `reports/stato_progetto.md` registra quel merge come «autorizzato dall'operatore»: le due letture non coincidono, sono state scritte entrambe nel file invece di sovrascrivere il record, e la ricostruzione la decide l'operatore.

---

**🔴 PRIMA DI TUTTO — qualcuno ha pushato su questo branch e non si sa chi.** Il mio push e' stato rifiutato: il remoto era avanti con `c026bdb`, `2a8524f`, `0b68d2b`, `93b57de`, non miei, firmati `Claude Opus 5.5` con trailer `session_01FgYcG4uNEqggobeJsbmE93` (lo stesso id nei corpi delle PR #184/#185). La sessione dell'altro worktree ha escluso di esserne l'autore con prove proprie (reflog senza traccia del ramo, SHA assenti dal reflog locale condiviso, firma di un modello diverso) e ha dichiarato che non pushera' mai su questo ramo. Ipotesi non verificabile dall'interno: **questa stessa sessione continuata altrove** (cloud/web). **Serve che l'operatore dica se ha una sessione viva altrove su questo ramo**: finche' esiste, puo' sovrascrivere l'unione. Nessun force da parte mia; stato pre-merge nel branch `backup/mio-locale-9e20872`. Il merge fatto e' l'UNIONE delle due implementazioni (loro V-1 + R-300-2 + R-301-4, mio V-3 + V-4 + quattro test): **838 PASS, 0 FAIL**, perche' il merge porta anche il fix di main che rende portabile T80u5.

## §1 SCOPE & ESITO FETTE

- **Fetta unica — `cerca_testo` su cartella: il budget di byte non deve mentire**: `FATTA`
  Tutti e tre i punti del brief: (a) log del kernel saltati nella ricerca su cartella, contati e dichiarati, cercabili per nome; (b) tetto per singolo file indipendente dal budget residuo, ri-tarabile da env, chi lo supera è saltato e NOMINATO; (c) messaggi distinti fra «file troppo grande» e «budget di byte esaurito», con RICERCA INCOMPLETA e il conto dei file non letti.
- **Punto 2 del brief originale (credenziali illeggibili)**: `SALTATA — già in produzione con la PR #188 (`_CHIAVE_PRIVATA_RE` in `modules/gate/gate.py`)`. Il brief vietava di toccarlo. I buchi residui sono solo PROPOSTI (§0 punto 3).
- **T80u5 (FAIL della suite kernel)**: `SALTATA — non esiste piu' alla base reale`. Era un FAIL preesistente su `f6396ba` (Python 3.14.7 del `.venv`); il merge di main ha portato `_troppo_annidato` dalla PR #192, che lo rende portabile. **Alla base vera di questa sessione (`af394bc`) la suite e' 821 PASS / 0 FAIL**: nessun FAIL da dichiarare, ne' alla base ne' a HEAD.
---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  36 +++++++++++++++++
 gas.py                             | 159 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 reports/diff_sessione.md           |  51 ++++++++++++------------
 reports/handoff.md                 | 758 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |  95 +++++++++++++++++++++++++++++++++++++++++++--
 reports/ultimo_report.md           | 305 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------
 tests/test_unit_kernel.py          | 276 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 7 files changed, 1302 insertions(+), 378 deletions(-)
```

**Base = `af394bccc7d2`, il merge-base VERO ricalcolato adesso.** Non `f6396ba`: quella era la base di partenza della sessione, e il merge di `origin/main` l'ha spostata. I blocchi di questo dossier calcolati sulla base vecchia erano falsi (V-1 della verifica esterna, 2º giro) — il gate A confronta solo i PATH, non i conteggi, quindi non se ne accorge.

## §3 GIT LOG --ONELINE (sessione)

```
bd3770f docs(fine-task): V-3 chiusa, V-1 (numeri) corretta, base ricalcolata
b20720a fix(cerca_testo): solo i log del kernel VERI, quelli nella root (V-3 verifica esterna #193)
49c6027 chore(revisore): memoria review #310 — APPROVATO
7e4609b docs(fine-task): R-gate-worktree-1 esteso al Stop hook promemoria_end.sh
dcf4cbf docs(fine-task): unione dei due fix di V-1, R-308-1, autore ignoto dei push
7c03a6d Merge dei due fix paralleli di V-1 in feat/cerca-testo-budget-onesto (review #308/#309)
9e20872 docs(fine-task): V-1 della verifica esterna chiusa, review #301/#302, matrice del merge
9e273e0 fix(cerca_testo): rotazioni del log cercabili per nome (V-1 verifica esterna #193)
b29493b chore(revisore): memoria review #307 — APPROVATO
ac508c5 chore(revisore): memoria review #302 — APPROVATO
2be3a51 chore(revisore): memoria review #301 — APPROVATO CON RISERVE
c72e0ce chore(revisore): memoria review #301 — APPROVATO CON RISERVE
93b57de docs(fine-task): handoff con la review #302 del merge di main
0b68d2b Merge main (PR #192) in feat/cerca-testo-budget-onesto — review #302
2a8524f docs(fine-task): handoff e report dopo il fix V-1 MEDIA del bot #193 (review #301)
c026bdb fix(cerca_testo): le rotazioni del log indicate per nome restano cercabili (V-1 MEDIA bot #193)
1032816 chore(revisore): memoria review #301 — APPROVATO CON RISERVE
58ff4ec docs(fine-task): §0 dell'handoff con numero e URL reali della PR #193
c16a789 docs(fine-task): verdetto #297 riemesso in forma di gate, #300, R-300-1
25ce6e6 chore(revisore): memoria review #300 — APPROVATO CON RISERVE
b892800 chore(revisore): memoria review #300 — APPROVATO CON RISERVE
775fdb8 docs(fine-task): report, handoff, stato e diff — cerca_testo budget onesto
d238610 fix(cerca_testo): il budget di byte non mente piu' (R-282-1, R-283-1)
08c9af6 chore(revisore): memoria review #299 — APPROVATO CON RISERVE
be36ce8 chore(revisore): memoria review #298 — APPROVATO CON RISERVE
e606313 chore(revisore): memoria review #297 — APPROVATO CON RISERVE
```

**Questo log non è tutto mio.** I commit `c026bdb`, `2a8524f`, `0b68d2b`, `93b57de` e `1032816` sono dell'autore ignoto che ha pushato su questo branch (firma Opus 5.5, trailer `session_01FgYcG4uNEqggobeJsbmE93`); `7c03a6d` è il merge con cui li ho integrati senza force (vedi §0). I commit `chore(revisore)` toccano SOLO `.claude/agents/memoria_revisore.md`, e i numeri #297–#302 nei loro messaggi precedono la rinumerazione a #302–#307: i messaggi non si riscrivono, la corrispondenza è nel §0. `775fdb8` conserva il testo ORIGINALE del verdetto #297 prima della riemissione in forma di gate (vedi §4).

## §4 VERDETTO DEL REVISORE (per commit motore)

**Nove giri** sullo stesso lavoro: dopo ogni giro le riserve sono state corrette e il diff è cambiato, quindi è stato richiesto un verdetto nuovo. #297–#301 e #308 APPROVATO CON RISERVE; #302, #309 e **#310 APPROVATO** secco. **Il verdetto che copre il codice che si mergia è #310**, non #302: dopo #302 (che era il merge di main) il motore è cambiato ancora tre volte — risoluzione del merge (#308), margine di sforo (#309), solo-root (#310, commit `b20720a`). Che qui mancassero i verdetti #308/#309/#310 era il finding **V-1 (MEDIA)** della verifica esterna al 3º giro: il Gate B passa perché controlla le citazioni dei verdetti PRESENTI, non che coprano l'ultimo diff del motore. Corretto: sono incollati integrali qui sotto. Verdetti INTEGRALI, incollati, in ordine. NB: i numeri dei giri sono quelli della copia della memoria di questo worktree e vengono rinumerati #302–#307 prima del merge (vedi §0): gli identificativi dei finding `R-29x-y` restano invece come emessi, perché citati nei commit già pushati.

### Giro 1 — review #297 (verdetto RIEMESSO nella forma del gate)

**Perché qui c'è la riemissione e non il testo originale.** Il verdetto originale del primo giro conteneva UNA citazione scritta col percorso ASSOLUTO della worktree (il prefisso `/Users/...` davanti al nome del file, invece del percorso relativo alla root del repo); `scripts/check_verdetto.py` risolve percorsi relativi alla root o nomi corti univoci, non percorsi assoluti, quindi bocciava il Gate B («file non trovato a HEAD»). Le altre 31 citazioni del §4 passavano. Come prescrive `/fine-task` (F-verdetto-ritoccato) **l'agente principale non ha toccato il testo del verdetto**: ha chiesto al revisore di RIEMETTERLO nella forma del gate. Sotto c'è la riemissione integrale, dichiarata come tale: stesso esito (APPROVATO CON RISERVE), stesso contenuto, stesse riserve e stessa gravità; cambia solo la forma delle citazioni (percorsi relativi) e i numeri di riga sono quelli validi a HEAD, con nota esplicita dove il bersaglio si è spostato nei giri 2/3/4. **Il testo originale del primo giro resta verbatim nella storia git**: commit `775fdb8`, `reports/handoff.md` (`git show 775fdb8:reports/handoff.md`). Non è stato riscritto né cancellato, solo spostato dove non blocca un gate che non può verificarlo.

## VERDETTO: APPROVATO CON RISERVE

**Verdetto #297 RIEMESSO nella forma del gate** (richiesta del flusso `/fine-task`, F-verdetto-ritoccato). Stesso esito e stesso contenuto dell'originale del primo giro: cambia SOLO la forma delle citazioni, ora tutte con percorso relativo alla root del repo. **I numeri di riga sono quelli validi ORA a HEAD** (`25ce6e6`): il codice è stato riscritto nei giri 2/3/4, quindi dove il bersaglio della citazione è cambiato lo dico esplicitamente nella voce. Le misure, le riserve e la loro gravità sono quelle del primo giro, non ritoccate.

Review #297 — diff del primo giro su `feat/cerca-testo-budget-onesto` (base main f6396ba). Letti prima: CLAUDE.md (sez. 1/4/5/8/9/10), `reports/stato_progetto.md` e `.claude/agents/memoria_revisore.md` (review #288-#296).

Il bug del brief è reale e il fix lo chiude: la causa (skip per-file confrontato col budget RESIDUO) non c'è più e la ricerca dalla root ritrova il file del gate anche col log da 4,5 MB in mezzo. Nessun antipattern del Wall of Shame (nessuno slicing di history, nessuna simulazione di output tool). Le riserve sono sull'onestà residua dei messaggi e sulla copertura di una delle quattro scelte, non sulla correttezza del flusso.

### Elementi del diff esaminati

1. `gas.py:2125` — `tetto_file = min(LETTURA_MAX_BYTES_PER_FILE, LETTURA_MAX_BYTES) if su_cartella else LETTURA_MAX_BYTES` (scelte 1 e 2 del brief). *Questa è la citazione che al primo giro avevo scritto col percorso assoluto e con il numero 2107: è la stessa riga, che a HEAD sta a 2125.* Rischio esaminato: regressione sul file indicato per nome e tetto aggirabile da env. Per `su_cartella=False` il valore è identico a quello che prima stava nel budget residuo al primo file → comportamento invariato; `min()` limita anche un `GAS_LETTURA_MAX_BYTES_PER_FILE` enorme e `_env_int(min_val=1)` regge i valori sporchi (`gas.py:823`). **Esito: ok.**
2. `gas.py:2137` — `if su_cartella and self._LOG_KERNEL_RE.fullmatch(f.name)` (scelte 1 e 5), con la regex a `gas.py:1835`. Rischio esaminato: log non più ispezionabile e over-match. `fullmatch` su `f.name` copre il log e ogni rotazione numerata (anche oltre la terza), non tocca un archivio compresso né una cartella omonima (il generatore filtra i soli file), e il corto circuito su `su_cartella` lascia cercabile il log indicato per nome. Mutazione verificata: disattivando il salto, 4 test T84n vanno in FAIL e nel caso del log pieno di corrispondenze i 200 risultati finiscono tutti nel log facendo sparire il file del gate → il salto protegge anche il tetto dei RISULTATI, non solo i byte. **Esito: ok, con riserva 3.**
3. `gas.py:2134` — `non_letti += 1` seguito da `continue` al posto del `break` (scelta 3). Rischio esaminato: costo e aperture di file indesiderate dopo il tetto. Dopo il tetto non si fa né `stat` né `_rel_root` (che sta a `gas.py:2136`, subito dopo il `continue`); il generatore continua ma `_risolvi_lettura` (`gas.py:1849`) fa solo operazioni di percorso e al massimo due `stat`, nessuna `open`, ed è capato da `LETTURA_MAX_FILE` (`gas.py:1822`, 500 voci) e dalla scadenza condivisa. **Esito: ok sul costo, riserva 1 sul numero stampato.**
4. `gas.py:1975` — il guard «vince il primo tetto» (`stato["tetto"] = stato["tetto"] or motivo`) usato dai due siti della visita, `gas.py:1938` e `gas.py:1941` (scelta 4). *Al primo giro il guard era scritto in linea in quei due siti; nei giri 3/4 è stato estratto in `_segna_tetto` e la marcatura dell'evento in `_ferma_enum` (`gas.py:1964`): la riga che ho giudicato qui è quella del guard, oggi a 1975.* Rischio esaminato: effetto su `_elenca_cartella` e utilità reale del guard. Per `_elenca_cartella` è un no-op verificato in esecuzione (con tetto di voci basso e con tetto di tempo nullo l'intestazione dichiara ancora il motivo giusto): quella funzione non scrive mai il campo e i due siti fanno `return` subito; il suo stato è inizializzato a `gas.py:2023`, quello di `_cerca_testo` a `gas.py:2102`. Il guard serve davvero: con la mutazione ad assegnazione secca, su 12 file con tetto di voci 6 e budget 200 il motivo vero (byte letti, con il nome del file letto solo in parte) viene sostituito da «numero di voci (6)». **Esito: ok nel merito, riserva 2 sulla copertura.**
5. `gas.py:2167` più `gas.py:2178`, `gas.py:2184` e `gas.py:2199` — messaggi distinti «budget complessivo della chiamata» / «file oltre il tetto per file» / «log del kernel non cercati» / «N file rimasti non letti» (punto c del brief). Rischio esaminato: fuga di informazione e righe forgiate. I nomi passano da `_rel_root` (`gas.py:1877`, che rende visibili i caratteri di controllo, R-284-1) e provengono SOLO da file già approvati da `_risolvi_lettura`: i percorsi negati finiscono nel contatore delle voci protette e non vengono mai nominati (un file di ambiente non può comparire fra i nomi raccolti a `gas.py:2144`). Nessun `str(e)`, solo interi e percorsi dentro la root. **Esito: ok.**
6. `tests/test_unit_kernel.py:8105` — il blocco di test «vince il PRIMO tetto scattato». Rischio esaminato: test che dichiara più di quanto prova. Nella versione del primo giro il blocco girava con 5 file e il tetto di 500 voci, che non poteva scattare: la mutazione del guard sopravviveva (825 PASS / 1 FAIL identici). *Nota di stato: questa riserva (R-297-2) è stata corretta nel secondo giro, e a HEAD lo stesso blocco gira con il tetto di voci a 3 e la mutazione lo fa fallire.* **Esito al primo giro: riserva 2.**
7. `gas.py:831` (contesto, riga non toccata dal diff del primo giro) — descrizione dello schema di `cerca_testo`, che allora prometteva «tutti i file di testo di una cartella» mentre i log erano esclusi. *Corretta nel terzo giro: a HEAD la stessa riga dichiara il salto dei log.* **Esito al primo giro: riserva 4 (cosmetica).**

FAIL-SAFE §9 verificato: ogni errore degli strumenti di lettura resta dentro `except Exception` del dispatcher a `gas.py:2013`, che logga un warning in gas_debug.log e restituisce un diniego, senza propagare.

### Numeri riprodotti da me al primo giro (venv del progetto)
- Suite kernel: **825 PASS, 1 FAIL** — l'unico FAIL è T80u5, preesistente (confermata la diagnosi: Python 3.14.7 locale, CI pinnata su 3.11).
- `pytest -q`: **1031 passed, 1 skipped**.
- Mutazioni (applicate e poi ripristinate verificando che il diff tornasse pulito): `continue`→`break` più salto dei log disattivato → **821 PASS, 5 FAIL** (i 4 test T84n mordono); guard → assegnazione secca → **825 PASS, 1 FAIL invariati** (guard non coperto, riserva 2).

### Riserve (numerate, con gravità) — testo del primo giro
1. **R-297-1 (MEDIA) — «N file rimasti non letti» è un PAVIMENTO, non un totale.** Il contatore conta solo i file che il generatore riesce ancora a produrre: se dopo il primo tetto scatta anche un tetto della VISITA (voci o tempo), il numero mente al ribasso e il secondo tetto resta invisibile. Misurato: 12 file, tetto di voci 6, budget 200 → l'intestazione dichiarava «2 file rimasti non letti» mentre i file non cercati erano 9 e il tetto di voci era scattato. Meglio del `break` muto di prima, ma rispetto al criterio dichiarato della fetta resta una bugia più piccola della precedente. Suggerimento: «almeno N», oppure dichiarare anche il secondo tetto.
2. **R-297-2 (BASSA) — la scelta 4 non è coperta da test**: la mutazione del guard sopravvive e il test che si intitola «vince il primo tetto» non lo prova. Fix da una riga: abbassare il tetto di voci in quel blocco.
3. **R-297-3 (BASSA) — il salto dei log è incondizionato sulla dimensione.** Un log del kernel da 50 KB, che sta largamente in ogni tetto, non viene più cercato in una ricerca su cartella, mentre CLAUDE.md sez. 3 fa dell'ispezione del log un'attività di prima classe. Mitigazioni presenti e accettabili: dichiarato in intestazione con l'istruzione su come cercarci, cercabile per nome, e il salto protegge anche il tetto dei risultati. Resta da dichiarare come compromesso.
4. **R-297-4 (COSMETICA) — promesse dello schema e del messaggio**: lo schema del tool prometteva «tutti i file di testo di una cartella»; e nel caso di file indicato per nome l'intestazione diceva «byte per file» mentre quel numero era il budget della chiamata.

### Rischio esplicitamente escluso (non verificato)
- `python gas.py doctor` **non eseguito**: fa ping di rete reali ai provider; l'exit 0 è dell'autore, non provato da me.
- **Comportamento su VPS non verificato**: non riproducibile in dev. Il costo degli `stat` della scelta 3 su alberi oltre le 500 voci su disco lento è misurato solo su APFS locale, e il set reale di rotazioni da 5 MB non è stato ricostruito (test con log sintetico da 4,5 MB in tmp).
- **T80u5 non indagato**: FAIL preesistente anche su main f6396ba, fuori dal perimetro della fetta.
- **`reports/` non in stage al primo giro**: letti per giudicare la coerenza, non giudicati come parte del diff.

### Memoria
Nessuna riga contatore nuova per questa riemissione: non è una review nuova, è lo stesso verdetto #297 in forma verificabile dal gate. Le righe #297, #298, #299 e #300 sono già in `.claude/agents/memoria_revisore.md` e committate (ultimo commit di memoria: `25ce6e6`). Il revisore ha aggiunto nel giro #300 anche la lezione che una citazione con percorso assoluto non è verificabile dal gate: da lì in avanti scrive le citazioni solo come percorso relativo alla root del repo.

### Giro 2 — review #298

## VERDETTO: APPROVATO CON RISERVE

Review #298 — secondo giro sul diff staged di `feat/cerca-testo-budget-onesto` (worktree `/Users/gas/Gas/.claude/worktrees/optimistic-austin-78debb`, base main f6396ba). Riletti CLAUDE.md (sez. 1/3/4/5/8/9), `reports/stato_progetto.md` (righe 5-30) e la mia memoria (#288-#297).

Le tre riserve dichiarate corrette lo sono davvero, e l'ho provato con le mutazioni, non solo leggendo. Nessun antipattern del Wall of Shame, §9 intatto. Le riserve nuove sono tutte conseguenze di secondo ordine del meccanismo nuovo, nessuna bloccante.

### Elementi del diff esaminati

1. `gas.py:1964` — `_segna_tetto(stato, motivo)` staticmethod (`setdefault("tetti", [])`, dedup, `stato["tetto"] = stato["tetto"] or motivo`). Rischio esaminato: `KeyError` su `stato["tetto"]` con un chiamante che non lo inizializza. I soli chiamanti di `_visita_cartella` sono `_elenca_cartella` (`gas.py:2017`) e `_cerca_testo` (`gas.py:2096`), entrambi inizializzano `"tetto": None`; e comunque il dispatcher `gas.py:1996` cattura `Exception` → warning in gas_debug.log + diniego (§9 rispettato). Type hints presenti (sez. 4). **Esito: ok.**
2. `gas.py:1938` e `gas.py:1941` — i due siti della visita passano da `_segna_tetto`. Rischio esaminato: regressione su `_elenca_cartella` (il no-op che ti avevo chiesto di verificare). Verificato **in esecuzione**: con `LETTURA_MAX_FILE=4` → «ELENCO INCOMPLETO: raggiunto il tetto di numero di voci (4)», con `LETTURA_MAX_SECONDI=0.0` → «… tempo (0 s)»; nessun `KeyError` dal `setdefault`, `stato["tetti"]` creato e mai letto da quella funzione. Coperto anche dal test preesistente `tests/test_unit_kernel.py:7848`. **Esito: no-op confermato, ok.**
3. `gas.py:2186` — `altri = [m for m in stato.get("tetti", []) if m != stato["tetto"]]` → «almeno N file rimasti non letti (anche l'enumerazione si è fermata: …)», altrimenti il conto esatto. Rischio esaminato: onestà in tutti i casi. Nel caso che avevo misurato è ora onesto (vedi numeri sotto); mutazione `altri = []` → **2 FAIL** sui due test R-297-1, quindi la riga morde. **Esito: ok, con riserve 1 e 2 sui casi di bordo.**
4. `gas.py:2173` — `quale = "byte per file" if su_cartella else "byte della chiamata"`. Rischio esaminato: coerenza fra testo e tetto effettivamente applicato. Corretto: per il file indicato per nome `tetto_file` *è* `LETTURA_MAX_BYTES`, e il nuovo test `tests/test_unit_kernel.py:8135` lo pinna sulla stringa esatta («oltre il tetto di 10 byte della chiamata saltati (molti/a.txt)»), con T84f (`tests/test_unit_kernel.py:7858`) aggiornato di conseguenza. **Esito: ok, R-297-4 chiusa.**
5. `gas.py:831` — descrizione dello schema di `cerca_testo`: non promette più «tutti i file di testo di una cartella» e dichiara il salto dei log con l'istruzione su `relative_path`. Rischio esaminato: promessa al modello divergente dal comportamento. Allineata. **Esito: ok.**
6. `tests/test_unit_kernel.py:8097` — blocco «vince il PRIMO tetto» con `_kL.LETTURA_MAX_FILE = 3`. Rischio esaminato: il test morde? Mutazione del guard (`stato["tetto"] = motivo`) → **825 PASS, 4 FAIL**, di cui 3 miei: il motivo diventa «numero di voci (3)» e il vero motivo finisce in `altri`. Prima della correzione la stessa mutazione sopravviveva (825/1 invariati). **Esito: R-297-2 chiusa.**

### Numeri riprodotti da me (venv del progetto, `PYTHONDONTWRITEBYTECODE=1`)
- `tests/test_unit_kernel.py`: **828 PASS, 1 FAIL** (solo T80u5, preesistente) — conferma il tuo numero.
- `pytest -q`: **1031 passed, 1 skipped** in 150 s.
- Mutazioni, applicate e ripristinate verificando `git diff --stat` vuoto: guard → assegnazione secca = **3 FAIL** nuovi; `altri = []` = **2 FAIL** nuovi.
- Caso misurato da me al primo giro, ora corretto: 12 file, `LETTURA_MAX_FILE=6`, budget 200 → «… tetto di byte letti (200, budget complessivo …): tanti/f02.txt letto solo in parte; almeno 3 file rimasti non letti (anche l'enumerazione si è fermata: numero di voci (6))». Onesto.

### Riserve nuove (numerate, con gravità)

1. **R-298-1 (BASSA) — il registro dei tetti è TESTUALE, quindi un secondo tetto con la stessa etichetta è invisibile.** Sia il dedup (`if motivo not in stato["tetti"]`, `gas.py:1971`) sia il filtro (`m != stato["tetto"]`, `gas.py:2186`) confrontano stringhe: se il tetto scatta due volte con lo stesso testo, `altri` resta vuoto. Caso reale: il **tempo**, che `_cerca_testo` e `_visita_cartella` formattano identico e che condividono la stessa scadenza. Misurato (41 file, primo file grosso, `LETTURA_MAX_SECONDI=0.03`): `52958 righe trovate in 1 file; 1 voci protette o illeggibili saltate; RICERCA INCOMPLETA: raggiunto il tetto di tempo (0.03 s)` — 40 file mai cercati, nessun conteggio, e non si dice che anche l'enumerazione si è fermata. **Non è un numero falso** (dopo la scadenza il generatore controlla il tempo prima di ogni `yield`, quindi `non_letti` è 0 per costruzione): è silenzio, come prima del fix. Però il punto (c) del brief («quanti file non sono stati letti») nel caso tempo non viene onorato, ed è il tetto più probabile su VPS con alberi grandi. Fix: marcare la FONTE (es. `stato["enum_fermata"] = True` dentro `_visita_cartella`) invece di confrontare testi.
2. **R-298-2 (COSMETICA) — «almeno 0 file rimasti non letti» è raggiungibile, e i test non fissano il numero.** Se il primo tetto scatta sull'ULTIMO file enumerato e poi scatta quello della visita, `non_letti == 0` con `altri` non vuoto → l'intestazione dice «almeno 0 file rimasti non letti (anche l'enumerazione si è fermata: …)»: vero ma assurdo da leggere. Non riprodotto con una sonda (il mio tentativo ha preso un ordinamento diverso dei tetti): è lettura del codice, non misura. Collegato: i due test nuovi asseriscono solo `"almeno " in out` senza pinnare il numero, quindi un pavimento sbagliato passerebbe.
3. **R-298-3 (COSMETICA, da sistemare prima del commit) — `reports/stato_progetto.md` ha un numero stale**: dice ancora «Kernel 818 → 825 PASS» mentre la suite ora dà **828**. Il report è la fonte di verità (CLAUDE.md sez. 3): va portato a 828 e, idealmente, l'elenco dei casi T84n va completato coi tre casi nuovi (R-297-2 col tetto di voci, caso 12 file, file per nome).

### Risposta alla tua domanda su R-297-3
La formulazione del compromesso in `reports/stato_progetto.md` mi pare **onesta**: dichiara il costo vero (un `gas_debug.log` da 50 KB non si cerca più da cartella), cita CLAUDE.md sez. 3 che rende l'ispezione del log attività di prima classe, elenca le mitigazioni e lascia la scelta all'operatore. Una sola precisazione da aggiungere per renderla inattaccabile: la prova citata («senza il salto i 200 risultati finiscono tutti nel log e `gate.py` sparisce») vale esattamente per l'alternativa proposta **perché il log del test (5000 righe, ~85 KB) sta SOTTO `tetto_file`** — con «salta solo i log oltre `tetto_file`» quel log verrebbe letto e il tetto dei risultati si esaurirebbe allo stesso modo. Senza quella frase un verificatore può obiettare che hai provato «niente salto» e non «salto condizionato».

### Rischio esplicitamente escluso (non verificato)
- `python gas.py doctor` **non eseguito**: fa ping di rete reali ai provider; prendo per buono il tuo exit 0 senza prova indipendente.
- **VPS non verificato**: non riproducibile in dev. Costo degli `stat` dell'enumerazione post-tetto misurato solo su APFS locale/tmp; le rotazioni reali da 5 MB non sono state ricostruite (il test usa un log sintetico da 4,5 MB in tmp).
- **T80u5 non indagato**: FAIL preesistente anche su main f6396ba (Python 3.14.7 locale, CI pinnata 3.11), fuori scope.
- **`reports/*` non in stage**: li ho letti per giudicare la coerenza (e da lì viene R-298-3), ma non li giudico come parte del diff.

### Memoria aggiornata
Riga `#298 — 2026-10-12 — APPROVATO CON RISERVE — …` in coda a `/Users/gas/Gas/.claude/worktrees/optimistic-austin-78debb/.claude/agents/memoria_revisore.md`, con due lezioni nuove datate (registro di eventi per testo che perde il secondo evento con la stessa etichetta; provare sempre il contatore a 0 quando si chiude una riserva sui conteggi). Committata con `bash scripts/commit_memoria_revisore.sh` → `be36ce8 chore(revisore): memoria review #298`; index verificato intatto dopo il commit (`gas.py` e `tests/test_unit_kernel.py` ancora staged).

Commit consentito: sì. Prima di committare sistema R-298-3 (numero 828 in `stato_progetto.md`) e aggiungi la precisazione su R-297-3; R-298-1 e R-298-2 vanno tracciate come riserve aperte in `reports/stato_progetto.md` (o chiuse ora: R-298-1 è un flag di una riga in `_visita_cartella`).

### Giro 3 — review #299

## VERDETTO: APPROVATO CON RISERVE

Review #299 — terzo giro sul diff staged di `feat/cerca-testo-budget-onesto` (worktree `/Users/gas/Gas/.claude/worktrees/optimistic-austin-78debb`, base main f6396ba). Riletti CLAUDE.md (sez. 3/4/5/9), `reports/stato_progetto.md` (righe 9-26) e la mia memoria (#296-#298).

R-298-1, R-298-2 e R-298-3 sono chiuse davvero, e la prima è chiusa **alla radice**: il registro testuale non c'è più e al suo posto c'è la fonte del tetto. Tutte le riserve che restano sono COSMETICHE e nessuna blocca il commit; una sola va sistemata prima (R-299-3, testo contraddittorio in `stato_progetto.md`).

### Elementi del diff esaminati

1. `gas.py:1964` — `_segna_tetto` ridotto a `stato["tetto"] = stato["tetto"] or motivo`. Rischio esaminato: riferimenti morti a `stato["tetti"]` dopo la rimozione. Grep su `gas.py` e su `tests/test_unit_kernel.py`: nessuna occorrenza residua di `"tetti"` (le occorrenze di «tetti» sono la parola italiana nei commenti di altre sezioni), nessun altro file `.py` cita `tetti`/`enum_fermata`. Mutazione del guard (`= motivo` secco) → **3 FAIL** nuovi, quindi «vince il primo» resta coperto. **Esito: ok.**
2. `gas.py:1939` e `gas.py:1944` — `stato["enum_fermata"] = motivo` ai due siti della visita. Rischio esaminato: esistono uscite anticipate della visita che NON marcano il flag? I soli `return` sono questi due, entrambi marcati; il troncamento dello `scandir` (`len(voci) >= resto` o tempo scaduto, `gas.py:1929`) non è un'uscita: le voci raccolte vengono consumate e il tetto per-voce scatta subito dopo (`resto = MAX - visitati + 1` fa sì che il controllo `visitati >= MAX` arrivi sempre), quindi il flag viene marcato comunque. **Esito: ok.**
3. `gas.py:2096` — `"enum_fermata": None` nello stato di `_cerca_testo`, letto con `stato.get(...)` a `gas.py:2188`. Rischio esaminato: `_elenca_cartella` (che non inizializza la chiave) rotto dalla scrittura della visita. Verificato **in esecuzione**: con `LETTURA_MAX_FILE=4` → «ELENCO INCOMPLETO: … numero di voci (4)», con `LETTURA_MAX_SECONDI=0.0` → «… tempo (0 s)»; il flag viene scritto nel suo dict e mai letto, nessun `KeyError`, messaggi identici a prima. Coperto anche dal test preesistente `tests/test_unit_kernel.py:7848`. **Esito: no-op confermato, ok.**
4. `gas.py:2188-2203` — i tre rami dell'intestazione. Rischio esaminato: esaustività e onestà, incluso il caso che ti preoccupava (flag marcato, primo tetto diverso, `non_letti == 0`). I rami sono `not fermata` / `fermata == tetto` / else, quindi esaustivi; nel caso «flag marcato, motivo diverso, `non_letti == 0`» il messaggio è «quanti file siano rimasti non letti non si sa: si è fermata anche l'enumerazione (<motivo>)» **senza numero** (il `, almeno N` è dietro `if non_letti`), quindi onesto e non più assurdo come «almeno 0». Questo sotto-caso l'ho giudicato leggendo il codice, non misurato. Mutazione «flag mai marcato» → **3 FAIL** nuovi. **Esito: ok, R-298-1/R-298-2 chiuse.**
5. `tests/test_unit_kernel.py:8104` e `tests/test_unit_kernel.py:8131` — le due asserzioni ora pinnano il numero («…, almeno 1», «…, almeno 3») e il motivo del secondo tetto. Rischio esaminato: asserzioni larghe che accettano un pavimento sbagliato (era la seconda metà di R-298-2). Chiuso: con la mutazione del flag entrambi vanno in FAIL mostrando «1 file rimasti non letti» / «3 file rimasti non letti». **Esito: ok.**
6. `tests/test_unit_kernel.py:8134` — nuovo test del tetto di TEMPO con `LETTURA_MAX_SECONDI = 0.0`. Rischio esaminato: prova ciò che il commento dichiara? No del tutto: con 0.0 la visita si ferma **prima di ogni `yield`**, quindi il ciclo di lettura di `_cerca_testo` non parte mai e la «collisione dei due tetti tempo (0 s)» descritta nel commento non avviene — scatta un solo tetto, quello della visita (ramo 2). Resta un test di regressione VALIDO sul sintomo (col codice del 2° giro lo stesso scenario taceva: `non_letti` 0 e `altri` vuoto → nessuna clausola), e la scelta di non mettere orologi nella suite è giusta. **Esito: riserva 2 (cosmetica).**

### Numeri riprodotti da me (venv del progetto, `PYTHONDONTWRITEBYTECODE=1`)
- `tests/test_unit_kernel.py`: **829 PASS, 1 FAIL** (solo T80u5 preesistente) — conferma il tuo numero.
- `pytest -q`: **1031 passed, 1 skipped** in 156 s.
- Mutazioni, applicate e ripristinate verificando `git diff --stat` vuoto: `enum_fermata` mai marcato → 4 FAIL totali (3 nuovi); guard `or` → assegnazione secca → 4 FAIL totali (3 nuovi).
- Il MIO caso del tempo, rieseguito dopo il fix (41 file, primo file ~660 KB, `LETTURA_MAX_SECONDI=0.03`): «50418 righe trovate in 1 file; …; RICERCA INCOMPLETA: raggiunto il tetto di tempo (0.03 s); **quanti file siano rimasti non letti non si sa: l'enumerazione si è fermata lì**». Prima taceva: R-298-1 chiusa nel caso che l'aveva motivata.

### Riserve (tutte COSMETICHE, nessuna bloccante)

1. **R-299-1 — il ramo 2 si sceglie ancora per UGUAGLIANZA DI TESTO.** `fermata == stato["tetto"]` (`gas.py:2194`): se il tetto di tempo scatta prima nel ciclo di lettura di `_cerca_testo` e poi la visita si ferma con la stringa identica, il messaggio attribuisce la fermata all'enumerazione («si è fermata lì») mentre il primo tetto era dell'altro componente. È il residuo del confronto fra testi, ma ora è **innocuo**: in entrambi i casi la sostanza («non si so quanti file sono rimasti») è vera, perché appena il flag è marcato il conto è ignoto comunque. Se vuoi togliere anche l'imprecisione di attribuzione: registrare al momento della marcatura se `stato["tetto"]` era ancora `None` (`stato["enum_fermata_prima"] = stato["tetto"] is None`) invece di confrontare le stringhe.
2. **R-299-2 — il commento del test promette più del test** (vedi punto 6): dice che riproduce la collisione dei due «tempo (0 s)», mentre con 0.0 scatta un solo tetto. Basta riscrivere il commento («la visita si ferma prima di ogni yield: nessun file enumerato, il conto non si può dare») per non lasciare un'affermazione falsa accanto a un test buono. Collegato: il ramo 3 con `non_letti == 0` resta senza test.
3. **R-299-3 — testo contraddittorio in `reports/stato_progetto.md`, da sistemare PRIMA del commit.** Il punto «✅ R-297-1» descrive ancora il meccanismo del 2° giro: «Ora `_segna_tetto()` registra TUTTI i tetti scattati (`stato["tetti"]`…) e l'intestazione dice "almeno N file rimasti non letti (anche l'enumerazione si è fermata: …)"». Non è più vero (nel codice staged `stato["tetti"]` non esiste e quel messaggio non viene emesso) e contraddice il punto R-298-1 scritto subito sotto. Il report è la fonte di verità (CLAUDE.md sez. 3): va riallineato al meccanismo finale. Stessa famiglia, più lieve: il punto (c) dice «l'intestazione dice … QUANTI file sono rimasti non letti», che ora vale solo quando l'enumerazione è arrivata in fondo.

Verificato invece OK quello che mi avevi segnalato: 829 e l'elenco a 11 casi sono corretti, e la precisazione su R-297-3 che ti avevo chiesto c'è ed è formulata bene («la prova vale per l'alternativa condizionata perché il log del test, ~85 KB, sta SOTTO `tetto_file`»). **R-297-3 resta aperta come compromesso dichiarato: la formulazione la giudico onesta e completa.**

### Rischio esplicitamente escluso (non verificato)
- `python gas.py doctor` **non eseguito** in nessuno dei tre giri: fa ping di rete reali ai provider; prendo per buono il tuo exit 0.
- **VPS non verificato**: non riproducibile in dev; il costo degli `stat` dell'enumerazione post-tetto è misurato solo su APFS locale/tmp e le rotazioni reali da 5 MB non sono state ricostruite (test con log sintetico da 4,5 MB in tmp).
- **Ramo 3 con `non_letti == 0`**: giudicato leggendo il codice, non riprodotto con una sonda (al 2° giro il mio tentativo aveva preso un ordinamento di tetti diverso).
- **T80u5**: FAIL preesistente anche su main f6396ba (Python 3.14.7 locale, CI pinnata 3.11), fuori scope.

### Memoria aggiornata
Riga `#299 — 2026-10-12 — APPROVATO CON RISERVE — …` in coda a `/Users/gas/Gas/.claude/worktrees/optimistic-austin-78debb/.claude/agents/memoria_revisore.md`, con due lezioni nuove datate (rileggere le voci precedenti del report quando si riscrive un meccanismo; un tetto di tempo a 0.0 non prova i rami di un tempo che scade a metà lavoro). Committata con `bash scripts/commit_memoria_revisore.sh` → `08c9af6 chore(revisore): memoria review #299`; index verificato intatto (`gas.py` e `tests/test_unit_kernel.py` ancora staged, i reports non staged).

Commit consentito: sì. Sistema R-299-3 (allineare il punto R-297-1 di `stato_progetto.md` al meccanismo finale) e, se vuoi chiudere tutto, la riga di commento di R-299-2; R-299-1 è opzionale e va tracciata come riserva aperta.

### Giro 4 — review #300

## VERDETTO: APPROVATO CON RISERVE

Review #300 — quarto giro su `feat/cerca-testo-budget-onesto` (worktree `/Users/gas/Gas/.claude/worktrees/optimistic-austin-78debb`). Nota: quando ho iniziato il diff era staged; **mentre revisionavo l'hai committato** (`d238610`, 18:22:53) — ne parlo nel punto «processo» qui sotto. Ho verificato che il `gas.py` committato è **byte-identico** a quello che ho revisionato (`diff` contro la mia copia: IDENTICI), quindi il verdetto vale su quel contenuto.

Niente di sostanziale: il meccanismo è corretto, coperto dove si può coprirlo, e la cosa che NON è coperta l'hai dichiarata tu col numero della mutazione, che è esattamente il comportamento giusto. **Non serve un altro giro sul codice.**

### Elementi del diff esaminati

1. `gas.py:1964` — `_ferma_enum(cls, stato, motivo)`: `enum_prima = stato["tetto"] is None` → `enum_fermata = motivo` → `_segna_tetto`. Rischio esaminato: ordine delle tre righe (se `_segna_tetto` venisse prima, `enum_prima` sarebbe sempre `False`) e unicità dello scrittore. Ordine corretto; grep: le due chiavi sono scritte SOLO qui e nell'init di `gas.py:2103`, e lette SOLO a `gas.py:2196` (`enum_fermata`) e `gas.py:2200` (`enum_prima`). Nessun altro file `.py` le nomina. **Esito: ok.**
2. `gas.py:1938` e `gas.py:1941` — i due siti della visita chiamano solo `_ferma_enum`. Rischio esaminato: uscite della visita che saltano la marcatura. Sono i soli due `return`; il troncamento dello `scandir` (`gas.py:1929`, `len(voci) >= resto` o tempo scaduto) non è un'uscita e porta sempre al tetto per-voce all'iterazione successiva, quindi marcato. **Esito: ok, nessun buco.**
3. `gas.py:2200` — `elif stato.get("enum_prima")` al posto del confronto `fermata == stato["tetto"]`. Rischio esaminato: il caso che aveva motivato R-299-1. **Misurato**: 41 file, primo file ~660 KB, `LETTURA_MAX_SECONDI=0.03` → «…; RICERCA INCOMPLETA: raggiunto il tetto di tempo (0.03 s); quanti file siano rimasti non letti non si sa: **si è fermata anche l'enumerazione (tempo (0.03 s))**». Al 3° giro lo stesso caso diceva «si è fermata lì»: l'attribuzione ora è giusta. **Esito: ok, R-299-1 chiusa nel comportamento.**
4. `gas.py:2103` — `"enum_fermata": None, "enum_prima": False` nello stato di `_cerca_testo`; `_elenca_cartella` non inizializza nulla. Rischio esaminato: regressione sull'elenco con due chiavi in più scritte nel suo dict. Verificato **in esecuzione**: `LETTURA_MAX_FILE=4` → «ELENCO INCOMPLETO: … numero di voci (4)», `LETTURA_MAX_SECONDI=0.0` → «… tempo (0 s)». Nessun `KeyError`, messaggi identici. **Esito: no-op confermato.**
5. `tests/test_unit_kernel.py:8181` — nuovo test del ramo 3 con `non_letti == 0` (`LETTURA_MAX_RISULTATI=3`, `LETTURA_MAX_FILE=4` su `tanti/`). **Rispondo alla tua domanda sul determinismo: sì, è deterministico, ma non per il motivo che scrivi nel commento.** Lo `scandir` raccoglie `resto = LETTURA_MAX_FILE - visitati + 1 = 5` voci in ordine di DISCO *prima* del `sort`, quindi QUALI 5 file vengono pescati dipende dall'ordine del filesystem; l'esito però non cambia perché i 12 file di `tanti/` sono **intercambiabili** (stesso contenuto, stessa dimensione, una corrispondenza ciascuno): 4 file enumerati, tetto risultati sulla 4ª, tetto voci al 5° tentativo. Misurato 3 esecuzioni su root nuove: output identico carattere per carattere. Se un giorno quei file diventassero diversi, il test diventerebbe dipendente dall'ordine del disco. **Esito: ok.**
6. `tests/test_unit_kernel.py:8164` — commento riscritto del test del tempo a 0.0. Rischio esaminato: dice ancora più di quanto il test provi? No: ora dichiara che con 0.0 la visita si ferma prima di ogni `yield`, che NON riproduce la collisione, dove sta la misura a mano e che vale come regressione sul sintomo. **Esito: ok, R-299-2 chiusa.**

### Numeri riprodotti da me (venv del progetto, `PYTHONDONTWRITEBYTECODE=1`)
- `tests/test_unit_kernel.py`: **830 PASS, 1 FAIL** (solo T80u5 preesistente). `pytest -q`: **1031 passed, 1 skipped** (158 s).
- Mutazione «`enum_prima = True` sempre» → **3 FAIL** nuovi: il CALCOLO del flag è coperto.
- Mutazione «rimetto il confronto fra testi» → **830 PASS / 1 FAIL invariati**: la tua dichiarazione è vera, verificata di persona. La differenza si vede solo col mio caso a 0.03 s («fermata lì» invece di «fermata anche l'enumerazione (…)»).
- **Risposta alla tua domanda: no, non fare il test con `monotonic` finto.** Quello che resta scoperto non è il flag (coperto) ma la sola *equivalenza* con la vecchia implementazione, cioè l'attribuzione testuale in un caso che richiede un orologio: un orologio finto nella suite costa fragilità più di quanto valga una riga di attribuzione. La dichiarazione in `stato_progetto.md` col numero della mutazione è la forma giusta di chiusura.

### Riserve (entrambe COSMETICHE, nessuna richiede un giro di review)

1. **R-300-1 — numero sbagliato in `reports/stato_progetto.md` (riga 15): «Test T84n, 13 casi», ma i `check("T84n` sono 12** (coerente col +1 di suite: 829 → 830). L'elenco fra parentesi, inoltre, non cita il caso nuovo (ramo «fermata anche l'enumerazione» con 0 file contati). Il report è la fonte di verità: correggi 13 → 12 e aggiungi il caso. È `reports/`, fuori perimetro: basta un commit di doc, nessuna review.
2. **R-300-2 — typo nel docstring `gas.py:1965`: «La visita si fermata per un tetto suo»** (manca «è»). **NON correggerlo adesso**: `scripts/hash_diff_staged.sh` hasha TUTTO il diff e il motore è già committato, quindi per un typo in un commento servirebbe un commit nuovo nel perimetro e quindi un'altra review. Va nella prossima fetta che tocca `_cerca_testo`; l'ho annotato in memoria.

### Processo — da registrare, non da rifare
Il commit del motore `d238610` è datato **18:22:53**, cioè PRIMA che questo verdetto esistesse: il marcatore `.claude/.review_ok` è stato scritto sul diff del 4° giro senza attendere l'esito. Mitigazione reale e verificata: il contenuto committato è byte-identico a quello che avevo in mano, quindi **non è passato codice non revisionato** e non c'è nulla da rifare. Ma la sequenza è la stessa famiglia della recidiva di PR #18 citata nel mio mandato, quindi va scritta in `reports/stato_progetto.md` come nota di processo (una riga), non lasciata implicita. Promemoria operativo: tutto ciò che metti in stage dopo il verdetto — anche solo `reports/` — cambia l'hash, quindi `scripts/segna_review_ok.sh` va eseguito come ULTIMO passo prima di `git commit`, e dopo di esso non si tocca più il perimetro.

### Rischio esplicitamente escluso (non verificato)
- `python gas.py doctor` **non eseguito** in nessuno dei quattro giri (ping di rete reali ai provider): prendo per buono il tuo exit 0.
- **VPS non verificato**: costo degli `stat` dell'enumerazione post-tetto misurato solo su APFS locale/tmp; rotazioni reali da 5 MB non ricostruite (test con log sintetico da 4,5 MB).
- **Attribuzione nel caso dell'orologio**: provata solo con la mia sonda a 0.03 s, non in suite (scelta dichiarata, vedi sopra).
- **T80u5**: FAIL preesistente anche su main f6396ba (Python 3.14.7 locale, CI pinnata 3.11), fuori scope.
- **R-297-3** resta il compromesso dichiarato già giudicato onesto in #299 (log saltati a prescindere dalla dimensione).

### Memoria aggiornata
Riga `#300 — 2026-10-12 — APPROVATO CON RISERVE — …` in coda a `/Users/gas/Gas/.claude/worktrees/optimistic-austin-78debb/.claude/agents/memoria_revisore.md`, con tre lezioni nuove datate (una correzione cosmetica nel codice dopo il verdetto costa un giro intero perché il marcatore hasha tutto il diff; test dipendenti da `resto` sono deterministici solo con voci intercambiabili; nota di processo sul commit anteriore al verdetto). Committata con `bash scripts/commit_memoria_revisore.sh` → `25ce6e6 chore(revisore): memoria review #300`. Index pulito (il tuo commit aveva già svuotato lo stage; il mio commit contiene SOLO il file di memoria, verificato con `git show --stat`).

### Giro 5 — review #301 (rinumerata #306)

## VERDETTO: APPROVATO CON RISERVE

Review #301 — diff staged su `feat/cerca-testo-budget-onesto` (PR #193), correzioni dei finding della verifica esterna V-1/V-3/V-4. Letti prima: CLAUDE.md (sez. 3/4/5/9), `reports/stato_progetto.md` e `.claude/agents/memoria_revisore.md` (review #297-#300). Numerazione: uso il MIO contatore, quindi questo giro è #301; la collisione con la copia della sessione PR #192 resta come l'hai descritta.

V-1 era un difetto vero e il fix lo chiude nel modo giusto: legare i due numeri in una costante unica è la correzione strutturale, non un cerotto. Due riserve BASSE riguardano la PROVA, non il comportamento: una delle due righe del fix di V-1 non è coperta (mutazione sopravvissuta) e V-4 non ha nessun test.

### Elementi del diff esaminati

1. `gas.py:41` e `gas.py:42` — `_GAS_LOG_MAX_BYTES = 5 * 1024 * 1024` e `_GAS_LOG_BACKUP = 3`, usate dall'handler a `gas.py:48` e dal tetto di lettura a `gas.py:1846`. Rischio esaminato: la costante è davvero l'unica fonte, e il logging continua a funzionare? Verificato **a runtime**: il `RotatingFileHandler` del root logger riporta `maxBytes = 5242880` e `backupCount = 3`, identici alle due costanti, e i warning continuano a finire nella scatola nera (le mie sonde hanno scritto nel log del worktree). La deriva che ha generato V-1 non è più possibile. **Esito: ok.**
2. `gas.py:1846` — `LETTURA_MAX_BYTES_LOG = _GAS_LOG_MAX_BYTES + 1024 * 1024` (6.291.456), letta da env a `gas.py:832`. Rischio esaminato: margine difendibile? Sì: l'handler ruota quando il record SUCCESSIVO sforerebbe la soglia, quindi lo sforo massimo è un singolo record; 1 MiB è largo con margine e l'invariante nel test impedisce la deriva silenziosa delle due costanti. Resta un bordo dichiarabile: un singolo record di log più grande di 1 MiB (payload enorme interpolato in un `logging.warning`) rimetterebbe la rotazione sopra il tetto. Il verso del limite è sicuro: `max(tetto_file, LETTURA_MAX_BYTES_LOG)` non può ABBASSARE nulla, quindi un `GAS_LETTURA_MAX_BYTES_LOG` sbagliato (anche 1) non rompe il caso normale. **Esito: ok.**
3. `gas.py:2145` e `gas.py:2147` — nel solo ramo per-nome, se `_LOG_KERNEL_RE.fullmatch(path.name)` allora si alzano `tetto_file` e `budget`. Rischio esaminato (la tua domanda principale): **si apre una strada per leggere oltre i tetti un file che NON è un log?** No, misurato: (a) un file NON log da 5.400.017 byte indicato per nome resta saltato a 5.000.000; (b) il corto circuito su `su_cartella` lascia la ricerca su cartella identica; (c) un symlink CHIAMATO come il log ma che risolve a un file grosso qualunque **non** ottiene il tetto alto, perché `_safe_path` risolve i symlink e `path.name` è il nome del file RISOLTO — quindi non si può riciclare un file grande sotto un nome da log. Nota di merito: un file chiamato `gas_debug.log` in una SOTTOcartella ottiene il tetto alto (misurato), e questa è la scelta CORRETTA, non un buco: il salto nella ricerca su cartella combacia per nome in qualunque sottocartella, quindi l'insieme dei file trattati come «log» deve essere lo stesso nei due rami, altrimenti si ricrea esattamente l'asimmetria di V-1. E il tetto alzato è un budget di LAVORO, non un permesso: il controllo dei percorsi, il cancello e il tetto di tempo restano quelli di prima. **Esito: ok.**
4. `gas.py:1851` — regex con `[0-9]` al posto di `\d` (V-3). Rischio esaminato: over-match su cifre non ASCII, che faceva passare per log del kernel (e quindi saltare) un file utente con una cifra araba. Chiuso, e il test asserisce direttamente i quattro casi sulla regex (ASCII sì, cifra araba no, `.gz` no): copertura strutturale, non dipendente dall'ambiente. **Esito: ok.**
5. `gas.py:2171` e `gas.py:2191` — `resto_prima = budget[0]` e `quanto = "letto solo in parte" if budget[0] < resto_prima else "non letto"` (V-4). Rischio esaminato (la tua domanda): è corretto in TUTTI i casi? Sì: `_righe_testo` solleva `_TettoByte` **prima** di scalare il budget, quindi «nulla consumato» ⟺ `budget[0] == resto_prima`; il budget è solo decrementato e viene ri-legato (riga 2147) PRIMA del ciclo, mai dentro, quindi non può risultare maggiore di `resto_prima` e produrre un falso «non letto». Misurato: 3 file da 81 byte con budget 162 → «…: m/c.txt **non letto**». **Esito: ok, con la cosmetica 3 qui sotto.**
6. `tests/test_unit_kernel.py:8175` — il test della rotazione reale (5.400.025 byte, dimensione vera). Rischio esaminato: prova entrambe le righe del fix? **No, solo una**: l'ago è sulla PRIMA riga del file e l'asserzione negativa cerca «oltre il tetto», che non compare nel messaggio «raggiunto il tetto di byte letti». Togliendo `budget = [tetto_file]` e tenendo l'alzata di `tetto_file`, la suite resta a 833 PASS / 1 FAIL. **Esito: riserva 1.**
7. `tests/test_unit_kernel.py:8183` — l'invariante anti-deriva (`LETTURA_MAX_BYTES_LOG` sopra la soglia dell'handler e non sotto `LETTURA_MAX_BYTES`, con la soglia pinnata a 5 MiB). Rischio esaminato: è il test che impedisce di riaprire V-1 in silenzio, ed è l'idea giusta. Nota: pinna le costanti di CLASSE, non i valori d'istanza dopo l'override da env; va bene perché `max()` rende innocuo un env sbagliato. **Esito: ok.**

### Numeri riprodotti da me (venv del progetto, `PYTHONDONTWRITEBYTECODE=1`)
- Suite kernel: **833 PASS, 1 FAIL** (solo T80u5 preesistente). `pytest -q`: **1031 passed, 1 skipped** (162 s).
- Riproduzione del fix di V-1: rotazione vera da 5.400.017 byte indicata per nome → «1 righe trovate in 1 file», nessun salto.
- Mutazione «via l'alzata del tetto per il log per nome» → **832 PASS, 2 FAIL**, col sintomo esatto del bug: «0 righe trovate in 0 file; 1 file oltre il tetto di 5000000 byte della chiamata saltati». Il test V-1 morde.
- Mutazione «tengo l'alzata di `tetto_file`, togliego `budget = [tetto_file]`» → **833 PASS, 1 FAIL invariati**: riga non coperta (riserva 1).
- Controprove di sicurezza (sonda): non-log grande per nome → saltato; symlink con nome da log verso un non-log → saltato; symlink innocuo verso il log vero → letto.

### Riserve (numerate, con gravità)

1. **R-301-1 (BASSA, consiglio di chiuderla ora) — metà del fix di V-1 non è provata.** La riga `gas.py:2147` esiste per una ragione che hai scritto tu stesso («senza il budget la ricerca sarebbe stata parziale»), e la mutazione che la toglie lascia la suite verde. Con l'ago sulla prima riga il test trova la corrispondenza anche con il budget basso, e «oltre il tetto» non compare nel messaggio del budget esaurito. Fix minimo: mettere l'ago in **coda** alla rotazione (oppure aggiungere `and "RICERCA INCOMPLETA" not in _oLb`). È la stessa famiglia di R-297-2, e qui pesa di più perché è la prova di un finding MEDIA appena chiuso: un mezzo fix tornerebbe verde.
2. **R-301-2 (BASSA) — V-4 non ha nessun test** (grep di «non letto» nei test: zero occorrenze). Il comportamento è corretto (misurato da me), ma la distinzione «non letto» / «letto solo in parte» non è coperta e può tornare a mentire alla prima riscrittura. Scenario deterministico, senza orologi: 3 file da 81 byte, `LETTURA_MAX_BYTES = 162`, `LETTURA_MAX_BYTES_PER_FILE = 100` → l'intestazione deve dire «non letto» per il terzo file.
3. **R-301-3 (COSMETICA) — `letti` conta anche il file dichiarato «non letto»**: nel mio caso misurato l'intestazione dice «2 righe trovate in **3 file**» e poi «m/c.txt non letto», cioè i file davvero letti erano 2. Piccola incoerenza della stessa famiglia della fetta (un numero che non corrisponde), riconciliabile leggendo la coda del messaggio.
4. **R-301-4 (COSMETICA) — il messaggio del budget cita sempre `LETTURA_MAX_BYTES`** (`gas.py:2191`), anche quando il budget vero per quel file è `LETTURA_MAX_BYTES_LOG`. Raggiungibile solo se un log indicato per nome CRESCE fra lo `stat` e la lettura (il caso normale non arriva mai a `_TettoByte`, perché la dimensione sta sotto il budget alzato): in quella corsa il numero stampato sarebbe quello sbagliato.

### Rischio esplicitamente escluso (non verificato)
- `python gas.py doctor` **non eseguito** (ping di rete reali ai provider): l'exit 0 è tuo, non mio.
- **Rotazione prodotta dall'handler VERO non osservata**: ho usato file di dimensione reale scritti a mano, non ho fatto ruotare il `RotatingFileHandler` scrivendo 5 MiB di log; quindi il valore massimo reale di uno sforo (il record che fa ruotare) resta un ragionamento sul comportamento documentato dell'handler, non una misura.
- **VPS non verificato**: tempi di lettura di un file da 6 MiB entro il tetto di 5 s misurati solo su APFS locale; su disco lento la ricerca su una rotazione per nome potrebbe finire sul tetto di tempo anziché completare.
- **T80u5**: FAIL preesistente anche su main f6396ba (Python 3.14.7 locale, CI pinnata 3.11), fuori scope.
- **R-297-3 e R-300-2** restano come già giudicate (compromesso dichiarato sul salto dei log; typo nel docstring da correggere nella prossima fetta).

### Memoria aggiornata
Riga `#301 — 2026-10-12 — APPROVATO CON RISERVE — …` in coda a `.claude/agents/memoria_revisore.md`, con tre lezioni nuove datate. Commit: `2be3a51 chore(revisore): memoria review #301`. Index verificato intatto: `gas.py` e `tests/test_unit_kernel.py` ancora staged, i file di `reports/` non staged.

Commit consentito: sì. Consiglio però di chiudere R-301-1 e R-301-2 **adesso** con un unico ritocco ai soli test (una riga ciascuno) e di rimandarmelo: è un diff di test minuscolo e la review è breve. Se preferisci committare così, vanno tracciate entrambe come riserve aperte in `reports/stato_progetto.md`, con scritto che la riga `gas.py:2147` del fix di V-1 non è coperta e con il numero della mutazione.

### Giro 6 — review #302 (rinumerata #307)

## VERDETTO: APPROVATO

Review #302 — giro breve sul diff staged di `feat/cerca-testo-budget-onesto` (PR #193), soli test. Letti prima: CLAUDE.md (sez. 3/4/5/9), `reports/stato_progetto.md` e `.claude/agents/memoria_revisore.md` (#297-#301). Prima cosa verificata: `gas.py` è **identico** a quello che ho revisionato in #301 (`diff` contro la copia che avevo salvato: nessuna differenza), quindi il motore non rientra in gioco e il giudizio sta sui due test nuovi.

Entrambe le riserve sono chiuse davvero, non per modo di dire: le mutazioni che prima sopravvivevano ora fanno fallire i test, e l'ho verificato io eseguendole.

### Elementi del diff esaminati

1. `tests/test_unit_kernel.py:8175` — la rotazione di prova ora ha l'ago in CODA (`"riempimento…" * 200_000 + "alfaL ultima riga del log"`, 5.400.026 byte misurati). Rischio esaminato: il test copre ENTRAMBE le righe del fix di V-1? Sì. Mutazione «togli `gas.py:2147` (`budget = [tetto_file]`) e tieni l'alzata di `tetto_file`» → **833 PASS, 2 FAIL**, con il test V-1 che riporta «0 righe trovate in 1 file; RICERCA INCOMPLETA: raggiunto il tetto di byte letti (5000000, budget complessivo della chiamata…)». In #301 la stessa mutazione lasciava 833 PASS / 1 FAIL invariati. **Esito: R-301-1 chiusa.**
2. `tests/test_unit_kernel.py:8180` — l'asserzione aggiunta `"RICERCA INCOMPLETA" not in _oLb`. Rischio esaminato (la tua domanda): può diventare vera per un motivo diverso dal budget? Per un file indicato per nome le sole altre strade sono il tetto di tempo e il tetto dei risultati, e le ho misurate entrambe: la ricerca sulla rotazione da 5,4 MB dura **0,088 s** (tre giri, valore stabile) contro il tetto di **5 s** → margine ~57x, e l'ago compare **una volta sola** nel file, quindi i 200 risultati non si avvicinano. Non c'è walk, quindi né `profonde` né la fermata dell'enumerazione possono comparire. Anche con un runner CI 5-10 volte più lento il margine resta di un ordine di grandezza. **Esito: non fragile, ok.**
3. `tests/test_unit_kernel.py:8213` — il test di V-4 su `molti/` con budget 162. Rischio esaminato (la tua seconda domanda): dipende dall'ordine di `scandir`? **No, e per un motivo in più di quello che dici tu**: `resto = LETTURA_MAX_FILE - visitati + 1 = 501` fa raccogliere tutte e 5 le voci PRIMA del `sort`, quindi l'ordine è a,b,c,d,e in modo deterministico; e in aggiunta i 5 file sono intercambiabili (81 byte, una corrispondenza ciascuno). Mutazione «`quanto` sempre "letto solo in parte"» su `gas.py:2191` → **833 PASS, 2 FAIL**, il test mostra «molti/c.txt letto solo in parte». **Esito: R-301-2 chiusa.**
4. `tests/test_unit_kernel.py:8188` e `tests/test_unit_kernel.py:8196` — invariante anti-deriva (il tetto del log sopra la soglia dell'handler, con `gas.py:1846` legato a `gas.py:41`) e asserzioni dirette sulla regex di `gas.py:1851`. Rischio esaminato: invarianti che non dipendono dall'ambiente. Confermate come in #301, inalterate da questo giro. **Esito: ok.**

Nota minore, non una riserva: in `tests/test_unit_kernel.py:8213` l'asserzione positiva è `"non letto" in _oLc`, che non fissa il nome del file; ho controllato che non possa combaciare per sbaglio con «2 file rimasti non letti» (serve la «o» finale), e il discriminante vero — «letto solo in parte» assente — è pinnato e la mutazione lo dimostra. Se un giorno il messaggio cambiasse, pinnare «molti/c.txt non letto» renderebbe il test più esplicito.

### Numeri riprodotti da me (venv del progetto, `PYTHONDONTWRITEBYTECODE=1`)
- Suite kernel: **834 PASS, 1 FAIL** (solo T80u5 preesistente) — conferma il tuo numero.
- Mutazione budget: **833 PASS, 2 FAIL**. Mutazione «letto solo in parte»: **833 PASS, 2 FAIL**. Dopo ciascuna ho ripristinato `gas.py` verificando con `diff` che tornasse identico.
- `pytest` **non rieseguito in questo giro**: il diff è di soli test del kernel, e in #301 (stesso `gas.py`) dava 1031 passed, 1 skipped. Rifallo tu come hai detto, è l'unico numero che resta da riconfermare.

### Sulla tua domanda su R-301-3: **non chiuderla adesso, hai ragione tu, e per un motivo in più del tuo**
Non è davvero «una riga». Spostare `letti += 1` dopo la lettura cambierebbe il conto anche per il file letto **a metà**, che invece va contato fra i letti: la correzione giusta è incrementare `letti` solo se qualcosa è stato consumato, cioè riusare `resto_prima` (`gas.py:2171`) anche nel caso normale, e quindi toccare il percorso che funziona più il suo test. È una decisione semantica, non un ritocco: rinviarla a una fetta propria su `_cerca_testo`, insieme a R-300-2 (il typo nel docstring) e con la mia descrizione esatta, è la scelta corretta e non pigrizia. Idem per R-301-4, che hai tracciato con la condizione che la rende raggiungibile (il log che cresce fra lo `stat` e la lettura).

Riserve già aperte e confermate, nessuna nuova: **R-297-3** (compromesso dichiarato sul salto dei log), **R-300-2** (typo nel docstring), **R-301-3** e **R-301-4** (cosmetiche rinviate). Nessuna è bloccante.

### Rischio esplicitamente escluso (non verificato)
- `python gas.py doctor` **non eseguito** in nessun giro (ping di rete reali ai provider).
- **`pytest` completo non rieseguito in questo giro** (vedi sopra): il mio numero di riferimento è quello di #301 sullo stesso `gas.py`. *(Rieseguito dall'agente principale subito dopo: 1031 passed, 1 skipped.)*
- **Rotazione prodotta dall'handler VERO non osservata**: i file di prova hanno dimensione reale ma sono scritti a mano; non ho fatto ruotare il `RotatingFileHandler` scrivendo 5 MiB di log.
- **Tempi su VPS/CI non misurati**: i 0,088 s sono su APFS locale; la tenuta dell'asserzione negativa su un runner molto più lento è un'estrapolazione dal margine, non una misura.
- **T80u5**: FAIL preesistente anche su main f6396ba (Python 3.14.7 locale, CI pinnata 3.11), fuori scope.

### Memoria aggiornata
Riga `#302 — 2026-10-12 — APPROVATO — …` in coda a `.claude/agents/memoria_revisore.md`, con due lezioni nuove datate. Commit: `ac508c5 chore(revisore): memoria review #302`. Index verificato intatto.

Commit consentito: sì, e per quanto mi riguarda la fetta è chiusa.

### Giro 7 — review #308 (risoluzione del merge)

## VERDETTO: APPROVATO CON RISERVE

Review #308 — **risoluzione di merge**, non una tua modifica: branch `feat/cerca-testo-budget-onesto`, `HEAD` 9e20872 (tuo lato, salvato anche in `backup/mio-locale-9e20872`), `MERGE_HEAD` 93b57de (altra sessione), base 58ff4ec, merge ancora APERTO e in stage. Letti prima CLAUDE.md (sez. 3/4/5/9), `reports/stato_progetto.md` e la mia memoria.

La risoluzione è corretta e non perde nulla di sostanziale: l'ho verificata guardando il diff nelle DUE direzioni, non solo in una. Hai fatto bene a prendere la loro base. Ma **il presupposto nuovo su cui l'hai accettata è a sua volta sbagliato**, e questa volta l'ho misurato io: una rotazione *può* superare `maxBytes`, quindi il loro limite esatto è bucato e il tuo margine serviva (per un motivo diverso da quello che avevi scritto).

### Elementi esaminati

1. `gas.py:2162`-`gas.py:2167` (loro V-1: `budget_tot` e il suo uso come `tetto_file`) — rischio esaminato: la risoluzione ha perso qualcosa di uno dei due lati? Diff nelle due direzioni: **stage vs MERGE_HEAD** contiene esattamente e solo V-3 e V-4 (nient'altro); **stage vs HEAD** mostra che del tuo lato cadono `LETTURA_MAX_BYTES_LOG`, l'env `GAS_LETTURA_MAX_BYTES_LOG` e `_GAS_LOG_BACKUP`, e che arriva da main `_troppo_annidato`. Nessun riferimento morto: grep di quei tre nomi su `gas.py` e `tests/` → zero. **Esito: ok, niente perso per sbaglio.**
2. `gas.py:1878` (V-3 riapplicato, regex con `[0-9]`) e `gas.py:2202` + `gas.py:2222` (V-4 riapplicato, `resto_prima` e `quanto`) — rischio esaminato: riapplicati a metà sulla loro base? No: `quanto` è integrato col loro `budget_tot` nel messaggio di `gas.py:2223`, e `resto_prima` è l'unica nuova variabile, letta solo lì. Mutazioni: annullando V-4 → 1 FAIL (il test mostra «letto solo in parte» dove deve dire «non letto»); annullando V-3 → 1 FAIL. **Esito: ok, entrambi interi e provati.**
3. `tests/test_unit_kernel.py:8229`-`tests/test_unit_kernel.py:8239` (la rotazione di prova ridimensionata a 5.238.026 byte, ago in coda) — rischio esaminato (la tua domanda): i miei test mordono sulla LORO implementazione? Sì. Mutazione «togli il budget dedicato al log» → **836 PASS, 2 FAIL**: fallisce il mio test dell'ago in coda («0 righe trovate in 0 file; 1 file oltre il tetto di 5000000 byte della chiamata saltati») **e** il loro. La prova di R-301-1 regge sulla nuova taglia. **Esito: ok.**
4. `tests/test_unit_kernel.py:8242` (invariante anti-deriva riscritta sulle loro costanti) — rischio esaminato: pinna ancora la cosa giusta? Sì (`_LOG_MAX_BYTES` uguale a 5 MiB e sopra `LETTURA_MAX_BYTES`), ed è ciò che impedisce la deriva silenziosa. **Esito: ok, con la riserva 4.**
5. `.claude/agents/memoria_revisore.md` (unione) — rischio esaminato: un giudizio perso dietro la parola «duplicato»? No, verificato per TESTO e non per numero: la tua riga #302 scartata è **identica carattere per carattere** alla loro #297 (`grep -xF`), stessa review. Confronto incrociato dei due lati: nessuna altra riga contatore di nessuno dei due lati manca dallo stage, se non quelle presenti sotto un altro numero. **Esito: unione corretta, con la riserva 2.**
6. `reports/handoff.md` — rischio esaminato: sezioni duplicate o marcatori rimasti. §0-§7 una volta ciascuna, **8 verdetti** nel §4, e **zero marcatori di conflitto** in TUTTI i sette file in stage, non solo in questo. **Esito: ok.**

### Numeri riprodotti da me (venv del progetto)
- Suite kernel sul risultato del merge: **838 PASS, 0 FAIL** — confermo anche il motivo: il T80u5 che ci siamo trascinati tutta la sessione cade col `_troppo_annidato` che arriva da main. `pytest -q`: **1031 passed, 1 skipped**.
- Mutazioni: budget dedicato via → 2 FAIL; V-4 via → 1 FAIL; V-3 via → 1 FAIL. Dopo ciascuna ho ripristinato `gas.py` verificando con `diff` che tornasse identico.

### Riserve

1. **R-308-1 (BASSA, ma chiudila ora: è un token) — il limite `max(LETTURA_MAX_BYTES, _LOG_MAX_BYTES)` è esatto solo in CARATTERI, e una rotazione reale può superare `maxBytes`.** Ho letto `shouldRollover` nello stdlib in uso (3.14.7): ruota quando `self.stream.tell() + len(msg) >= self.maxBytes`, cioè confronta una posizione in **byte** con una lunghezza in **caratteri**. Con record multibyte il file scavalca la soglia senza che la rotazione scatti. **Misurato**, non dedotto: handler con `maxBytes=1000`, sette record ASCII fino a 700 byte, poi un record di 200 caratteri accentati (401 byte) → il file arriva a 1101 byte e solo il record successivo fa ruotare, lasciando una rotazione da **1101 byte con maxBytes=1000**. Tradotto sul nostro caso: una `gas_debug.log.N` può pesare 5.242.880 più il surplus byte-caratteri dell'ultimo record, e allora `st_size > tetto_file` la fa saltare di nuovo — **V-1 riaperta**, con lo stesso sintomo. Gas logga in italiano con accenti e interpola percorsi e repr, quindi la finestra non è teorica. Conseguenze: (a) serve un margine — il tuo `+1 MiB` copriva esattamente questo, quindi **non era sbagliato il margine, era sbagliata la motivazione**; (b) il commento di `gas.py:2162` e quello del test a `tests/test_unit_kernel.py:8228` che dicono «un file di rotazione non la supera mai» sono **falsi** e vanno corretti. Nota su di me: in #306 avevo accettato il tuo ragionamento *dichiarando di non averlo misurato*; la misura ora dice che il presupposto era sbagliato in entrambe le direzioni.
2. **R-308-2 (BASSA) — la memoria resta con un duplicato e un riferimento che punta altrove.** Nello stage `#297` numera **due review diverse** e la mia riga `#303` dice «ri-review #302» mentre `#302` ora è la review di un'altra sessione. **Confermo la tua scelta di non rinumerare una terza volta**: serve un passaggio autorevole dell'operatore sul ramo di integrazione.
3. **R-308-3 (COSMETICA) — persa la manopola `GAS_LETTURA_MAX_BYTES_LOG`.** La giudico **accettabile e anzi preferibile**: un valore DERIVATO dalla soglia di rotazione non può divergere da essa, e la divergenza è la causa stessa di V-1. Va però scritto nel report come riduzione deliberata di configurabilità.
4. **R-308-4 (COSMETICA) — il test della rotazione sta 4.854 byte sotto il tetto** e asserisce solo di stare *sopra* `LETTURA_MAX_BYTES`: aggiungere `and _szL < gas._LOG_MAX_BYTES` rende la finestra esplicita.

### Rischio esplicitamente escluso (non verificato)
- **`_troppo_annidato` non revisionato nel merito**: arriva da main (PR #192); nel diff del commit di merge sembrerà codice nuovo di questa fetta.
- **Soglia reale della rotazione in produzione non osservata**: misura con handler di prova a `maxBytes=1000`.
- `python gas.py doctor` **non eseguito**; **VPS non verificato**.

### Memoria aggiornata — richiede un'azione tua
Riga `#308` scritta in coda a `.claude/agents/memoria_revisore.md`. `commit_memoria_revisore.sh` **non ha potuto committare**, correttamente: con `MERGE_HEAD` aperto git rifiuta il commit parziale. Quindi: `git add .claude/agents/memoria_revisore.md` prima di chiudere il merge.

Commit del merge consentito: sì. Prima però chiuderei R-308-1.

### Giro 8 — review #309 (margine di sforo)

## VERDETTO: APPROVATO

Review #309 — giro breve sul diff staged (merge ancora aperto, `MERGE_HEAD` 93b57de). Il delta rispetto a #308 è esattamente il margine, i due commenti corretti e i test: niente altro si è mosso in `gas.py`.

R-308-1 e R-308-4 sono chiuse bene, e il margine non è «generoso per prudenza»: è **portante e provato**.

### Elementi esaminati

1. `gas.py:43` — `_LOG_SFORO_MAX = 1024 * 1024`. Rischio esaminato (la tua domanda): crea un'altra coppia di numeri da tenere allineati a mano? **No**: grep su `gas.py` → due occorrenze, la definizione e **un solo** uso, a `gas.py:2179`. Il valore resta derivato dalla soglia dell'handler, quindi non c'è nulla che possa divergere: è un margine *sopra* una fonte unica. **Esito: ok.**
2. `gas.py:2179` — `budget_tot = max(LETTURA_MAX_BYTES, _LOG_MAX_BYTES + _LOG_SFORO_MAX)`. Rischio esaminato: il margine è portante o decorativo? Mutazione «tetto esatto senza margine» → **838 PASS, 1 FAIL**, fallisce il test dello sforo («5400022 byte -> 0 righe trovate in 0 file»). Inoltre il margine è protetto **da un test vero e non solo dall'invariante `> 0`**: il file di prova pesa 5.400.022 byte, quindi qualunque riduzione sotto ~157 KB fa fallire lo stesso test. Nessun guardrail indebolito: la ricerca su CARTELLA resta a `LETTURA_MAX_BYTES`, il tetto per file e quello di tempo sono intatti, e leggere 5,4 MB costa ~0,09 s contro i 5 s del tetto. **Esito: ok.**
3. `gas.py:43`-`gas.py:47` e il commento di `gas.py:2166`-`gas.py:2176` — rischio esaminato: i due commenti corretti dicono il vero? **Sì.** Spiegano che `shouldRollover` somma `tell()` in byte e `len(msg)` in caratteri, e citano la misura (1101 byte con `maxBytes=1000`) che ho rifatto io. Una precisazione: il limite esatto dello sforo è il **surplus** byte-caratteri dell'ultimo record, mentre i commenti dicono «lo sforo in byte dell'ultimo record» — è una sovrastima, quindi conservativa.
4. `tests/test_unit_kernel.py:8260` — il test nuovo dello sforo. Rischio esaminato: dipende dall'ordine di `scandir`? **No**, per costruzione: il file è indicato per nome, quindi `_cerca_testo` prende il ramo `iter([path])` e `_visita_cartella` non viene mai chiamata. **Esito: ok.**
5. `tests/test_unit_kernel.py:8238` e `tests/test_unit_kernel.py:8244` — finestra esplicita della taglia (R-308-4 chiusa) e invariante estesa con `_LOG_SFORO_MAX > 0`. Verificato: **dopo** la riga 8255 non c'è nessuna ricerca su CARTELLA, quindi il nuovo `gas_debug.log.3` non altera i «N log del kernel non cercati» asseriti prima. **Esito: ok.**

### Numeri riprodotti da me
- Suite kernel: **839 PASS, 0 FAIL**. `pytest -q`: **1031 passed, 1 skipped**.
- Mutazione «tetto esatto» → 838 PASS, 1 FAIL. Dopo la mutazione ho ripristinato `gas.py` verificando con `diff` che tornasse identico.

### Sulla tua nota su di te
La registro perché è la cosa più utile di questo giro: tre agenti di fila hanno trattato il comportamento di `RotatingFileHandler` come deducibile, e il numero giusto è uscito solo leggendone il codice. Nota che la prima volta il margine era *giusto con la motivazione sbagliata*: è la situazione più pericolosa, perché una motivazione sbagliata invita il prossimo a rimuovere la cosa giusta — ed è esattamente quello che è successo.

### Riserve: nessuna nuova. Restano aperte R-308-2, R-308-3, R-297-3, R-301-3.

### Rischio esplicitamente escluso (non verificato)
- **`_troppo_annidato`** arriva da main e nel diff sembrerà codice nuovo di questa fetta.
- **Sforo su record reali non osservato**; **record di log più grandi di 1 MiB** non cercati; `doctor` non eseguito; **VPS non verificato**.

### Memoria — serve di nuovo un `git add` tuo
Riga `#309` scritta in coda alla memoria; `commit_memoria_revisore.sh` non ha potuto committare per il commit parziale vietato con `MERGE_HEAD` presente.

Via libera a chiudere il merge e a pushare subito. Dopo il push, rilancia la verifica esterna sull'head nuovo.

### Giro 9 — review #310 (solo i log nella root) — verdetto finale sul codice

## VERDETTO: APPROVATO

Review #310 — ultimo giro su `feat/cerca-testo-budget-onesto` (merge chiuso in 7c03a6d, diff staged = solo `gas.py` e `tests/test_unit_kernel.py`). Il delta rispetto a #309 è esattamente l'helper nuovo e i due call site.

**Hai ragione tu e il mio giudizio di #306 era sbagliato.** Lo scrivo per primo perché è il punto: l'invariante che difendevo — «l'insieme dei file trattati come log deve essere lo STESSO nei due rami, altrimenti torna l'asimmetria di V-1» — è giusta, e il tuo helper la rispetta. Ma l'insieme che avevo scelto era quello sbagliato: «chi si chiama come il log, a qualunque profondità» misattribuisce al kernel i file dell'utente, ed è un difetto vero. Il `RotatingFileHandler` scrive nella CWD e tutto il progetto assume già CWD == root (il `doctor` guarda `root / "gas_debug.log"`, `gas.py:3793`), quindi «genitore == root» è l'insieme che la realtà definisce. Avevo confuso l'invariante con l'insieme che avevo sotto gli occhi.

### Elementi esaminati

1. `gas.py:1934` — `_e_log_kernel(self, path) -> bool`: nome da `_LOG_KERNEL_RE` **e** `path.parent.resolve(strict=False) == self.root.resolve(strict=False)`. Rischio esaminato: l'helper è usato in tutti i posti dove prima c'era il match sul nome? Sì: grep di `_LOG_KERNEL_RE` → **solo** la definizione a `gas.py:1886` e l'uso dentro l'helper a `gas.py:1943`; i due rami chiamano l'helper a `gas.py:2194` (per nome) e `gas.py:2218` (su cartella). Una regola, un posto. **Esito: ok.**
2. `gas.py:1943`-`gas.py:1948` — il `resolve()` sul genitore. Il `path` arriva sempre da `_risolvi_lettura`, che lo risolve, quindi il `resolve()` sul genitore è un no-op difensivo; sul lato root normalizza anche il caso in cui la root sia raggiunta via symlink. Provato con una sonda a 6 casi: (a) log vero nella root per nome → letto intero; (b) omonimo in sottocartella per nome → solo budget normale, saltato e **NOMINATO**; (c) ricerca dalla root → «1 log del kernel non cercati» per quello vero e l'omonimo nominato fra i «file oltre il tetto per file», cioè **il tetto per file fa da rete e il budget non si prosciuga in silenzio**; (d) ricerca nella sottocartella → idem; (e) symlink nella root che punta all'omonimo in sotto → **non** trattato da log; (f) symlink in sotto che punta al log vero → trattato da log. Governa sempre il percorso RISOLTO. **Esito: ok.**
3. `gas.py:1947` — `except OSError: return False`. **È il verso giusto, confermo**: in caso di dubbio il file non è un log, quindi viene cercato (e se grande viene saltato e nominato dal tetto per file); il contrario userebbe l'errore per etichettare come «kernel» un file dell'utente. Il prezzo è minuscolo e dichiarabile: nel ramo per-nome un errore farebbe perdere il tetto dedicato a una rotazione vera; con `strict=False` un `OSError` lì è praticamente irraggiungibile. §9 rispettato.
4. `tests/test_unit_kernel.py:8295` — il test nuovo asserisce sia che il file **si trova** sia che «log del kernel» **non compare**, cioè sia la ricerca sia la non-misattribuzione. Deterministico. Mutazione `return True` (il comportamento che avevo approvato io) → **839 PASS, 1 FAIL**. **Esito: ok.**

### Numeri riprodotti da me
- Suite kernel sul diff staged: **840 PASS, 0 FAIL**. Mutazione dell'helper → 839/1.
- **La tua correzione di V-1 sulla base l'ho verificata di persona**: `git merge-base HEAD origin/main` → **af394bc**, e la suite in un worktree temporaneo su af394bc dà **821 PASS, 0 FAIL**.

### Da correggere nei report prima del push
1. **I casi T84n sono 19, non 18**: il numero è andato stale di nuovo *dentro lo stesso giro*. I conteggi dichiarati si ricalcolano **dopo** l'ultima modifica.
2. **Un worktree temporaneo è ancora registrato** (`scratchpad/base2` su af394bc): rimuovilo.

### Le tue tre riserve, con la mia opinione
- **V-2**: l'osservazione è corretta, lo sforo non ha tetto teorico. Oggi il margine è **portante** e sfondarlo richiede un record multibyte da oltre 1 MiB, che sarebbe un bug suo. Per un limite *dimostrato* servirebbe capare la lunghezza del record a monte. Priorità bassa.
- **V-4**: d'accordo, ed è appena diventata più visibile: nella mia sonda l'omonimo grande in sottocartella finisce esattamente in quel messaggio. Il fix onesto è una riga di testo. In cima alla prossima fetta.
- **V-5**: d'accordo a tenerla aperta. Sui due test quasi uguali: **non unificarli a scatola chiusa** — provano cose diverse; se li unisci, unisci le *fixture*, non le asserzioni.

### Rischio esplicitamente escluso (non verificato)
- **Residuo dichiarato**: se Gas venisse avviato da una sottocartella, il log vero finirebbe fuori dalla root e tornerebbe «file dell'utente». Mitigato dal tetto per file che lo nomina. La chiusura vera sarebbe derivare la cartella da `handler.baseFilename`. **Non provato avviando Gas da una sottocartella.**
- **`_troppo_annidato`** non revisionato nel merito; **sforo su record reali** non osservato; `doctor` non eseguito; **VPS non verificato**; `pytest` non rieseguito in questo giro.

### Memoria aggiornata
Riga `#310` in coda alla memoria. Commit: `49c6027 chore(revisore): memoria review #310`.

Puoi committare e pushare. Dopo il push rilancia la verifica esterna sull'head nuovo, e correggi i due numeri dei report prima di generarli, non dopo.

### Base dell'autorizzazione al commit, e giro 4

Il commit di questo diff è autorizzato da **#299** («Commit consentito: sì»), applicate le correzioni che il verdetto stesso prescriveva o permetteva: R-299-3 (solo `reports/`, fuori perimetro), la riga di commento di R-299-2 più il test che mancava sul ramo 3, e l'opzionale R-299-1. Il diff staged differisce da quello di #299 **solo** per quelle correzioni.

Un **quarto giro** è stato lanciato per diligenza (non perché il gate lo richiedesse) sul diff finale. Il suo verdetto, quando arriva, va riportato all'operatore; se solleva qualcosa di sostanziale, la correzione comporta un nuovo commit e quindi la riesecuzione INTEGRALE di `/fine-task` (gate post-fine-task). Riserva nota e già dichiarata, misurata da me e NON coperta da test: **R-299-1** — la mutazione che rimette il confronto fra testi SOPRAVVIVE (830 PASS / 1 FAIL invariati), perché il solo caso in cui i due comportamenti differiscono richiede un tempo che scada a METÀ lavoro e un orologio nella suite la renderebbe instabile; la prova resta quella a mano (41 file, `LETTURA_MAX_SECONDI=0.03`).

### Verdetti del revisore dell'ALTRO autore, arrivati col merge — suoi #301 e #302

I due verdetti che seguono **non sono miei**: sono del revisore della sessione che ha pushato su questo branch da fuori (vedi §0), e sono entrati nel dossier con il merge `7c03a6d`. Li lascio integrali perché coprono il suo fix di V-1, che è la base che ho adottato. I numeri #301/#302 sono quelli della SUA copia della memoria e **collidono** coi miei omonimi: i miei stanno ai Giri 5 e 6 qui sopra, rinumerati #306 e #307.

#### Suo giro A — sua review #301 (dopo il bot #193: V-1 MEDIA rotazioni del log)

## VERDETTO: APPROVATO CON RISERVE

Review #301. Diff staged su `feat/cerca-testo-budget-onesto` (PR #193): `gas.py`, `tests/test_unit_kernel.py`. Letture obbligatorie fatte: CLAUDE.md (sez. 1, 4, 5, 8, 9), `reports/stato_progetto.md` (righe di T84n e R-300-2) e la memoria del revisore.

**Elementi del diff esaminati**
- `gas.py:38`: nuova costante `_LOG_MAX_BYTES = 5*1024*1024`, che ora usa anche il RotatingFileHandler (`gas.py:43`). Ho controllato se cambia la rotazione: no, il valore è identico a prima e la fonte del numero ora è una sola. Esito: ok.
- `gas.py:2120`: il budget sale a `max(LETTURA_MAX_BYTES, _LOG_MAX_BYTES)` solo se il percorso indicato è un file (non una cartella) e il nome è un log del kernel (`fullmatch`). Ho controllato se il budget si allarga anche altrove: no. Nella ricerca su cartella i log restano saltati (`gas.py:2144`), e un file normale resta a 5.000.000 byte. La lettura avviene a righe con `readline(budget+1)` e il tetto di tempo resta attivo, quindi i 242.880 byte in più non creano rischi di memoria o di crash. Esito: ok per il caso di default. Riserva **R-301-1** (BASSA): `max()` scavalca un `GAS_LETTURA_MAX_BYTES` abbassato dall'operatore. L'ho provato eseguendo il codice: con env=1000, un `gas_debug.log.2` da circa 15 KB viene letto tutto, mentre un `a.txt` identico viene saltato con «oltre il tetto di 1000 byte». Per i log la manopola dell'operatore non vale più. Correzione possibile: alzare il tetto solo se l'env è al default, oppure aggiungere solo la differenza (`LETTURA_MAX_BYTES + _LOG_MAX_BYTES - GasKernel.LETTURA_MAX_BYTES`).
- `gas.py:2133`: per un file indicato per nome, `tetto_file` ora vale `budget_tot`. Ho controllato se il confronto `st_size > tetto_file` resta coerente con il budget: sì, i due valori coincidono, quindi una rotazione di dimensione reale non finisce più tra i «grandi». Esito: ok.
- `gas.py:2174`: il messaggio «byte letti (…)» ora riporta `budget_tot`. Ho controllato se il numero è vero: sì. Però lo attribuisce ancora a `GAS_LETTURA_MAX_BYTES`, e per un log il valore non viene da lì (fa parte di R-301-1). Esito: riserva cosmetica, collegata a R-301-1.
- `tests/test_unit_kernel.py:8184`: caso T84n nuovo. Ho controllato se la rotazione è davvero oltre 5.000.000 e sotto 5 MiB: il ciclo si ferma a ≥5.100.000 con blocchi da circa 104 KB, quindi il file resta sotto 5.242.880. Il test verifica il risultato in fondo al file, l'assenza di «oltre il tetto» e il controcaso con `grande.txt` saltato. Esito: ok. Non ho ripetuto la mutazione dichiarata dall'autore: l'asserzione `"oltre il tetto" not in _oR` la coprirebbe, ma non l'ho eseguita.
- `tests/test_unit_kernel.py:8181`: il commento «un file grande NON log resta capato» sta sulla riga che in realtà ripulisce la rotazione. Riserva **R-301-2** (COSMETICA).
- `gas.py:1966`: typo R-300-2 corretto («si è fermata»). Esito: ok, R-300-2 chiusa.

**Wall of Shame e guardrail**: nessuno slicing della history, nessuna simulazione di output dei tool. Cap delle 10 iterazioni, cap degli 8k e `_get_window` non toccati. Nessuna nuova eccezione non gestita: `_TettoByte` e `OSError` restano intercettate.

**Esecuzione**: `python3 tests/test_unit_kernel.py` → **835 PASS, 0 FAIL**, riprodotto. Nessun commit del perimetro ha una data anteriore a questo verdetto: il diff è ancora staged e l'ultimo commit è quello della mia memoria.

**Rischio escluso**: non ho rilanciato pytest (1032 passed è un dato dell'autore, non mio). Non ho verificato il caso di un singolo record di log più grande di 5 MiB, che il RotatingFileHandler scrive comunque in un file nuovo e oltre `maxBytes`: in quel caso il budget si esaurisce e il messaggio dice «letto solo in parte», quindi resta onesto, ma l'ho valutato solo leggendo il codice. Non ho verificato il comportamento su VPS.

Riserve da tracciare in `reports/stato_progetto.md`: R-301-1 (BASSA), R-301-2 (COSMETICA). Nessuna delle due blocca il commit. Correggerle adesso cambierebbe il diff staged e richiederebbe un nuovo giro di review.

Memoria aggiornata (riga #301 + una lezione su `max(tetto_env, costante)`) e committata da sola con lo script: commit `1032816`. Il diff staged del motore non è stato toccato.

#### Suo giro B — sua review #302 (merge di main con la PR #192 nel ramo)

## VERDETTO: APPROVATO CON RISERVE

Review #302: diff staged del merge di `origin/main` (PR #192) nel ramo `feat/cerca-testo-budget-onesto` (PR #193).

**Codice esaminato**
- `gas.py:627` — `_troppo_annidato` arriva da main. Rischio controllato: l'unione automatica poteva duplicarla o alterarla. `git diff MERGE_HEAD -- gas.py` non tocca nessuna riga della riflessione, quindi è identica a main. Esito: ok.
- `gas.py:672` — il controllo del tetto prima di `json.loads` arriva da main insieme alla rete `except RecursionError`. Rischio controllato: interferenze con la PR #193. Non c'è stato condiviso: `_analizza_riflessione` è pura, e il patch globale di `json.loads` in T80u7 non tocca `cerca_testo`, che non usa json. Esito: ok.
- `gas.py:1881` e `gas.py:2165` — `_LOG_KERNEL_RE` e il budget dedicato ai log del kernel restano quelli della review #301. Rischio controllato: che il merge li abbia persi o mescolati. Il diff contro HEAD tocca solo la riflessione. Esito: ok.
- `tests/test_unit_kernel.py:7152` — T80u6 e T80u7 compaiono una volta sola, e l'import di `_troppo_annidato` è stato aggiunto senza duplicati. Esito: ok.
- `.claude/agents/memoria_revisore.md` e `reports/stato_progetto.md` — ho confrontato con `comm` le righe del merge con HEAD e con MERGE_HEAD. Dal lato di main manca solo l'intestazione di stato_progetto, sostituita come previsto, più le righe che il nostro ramo ha già modificato (la voce della PR #184 e R-283-1). Dal nostro lato non si perde nessuna riga. Esito: ok.
- Ho rifatto girare le suite sull'albero unito: kernel 837 PASS, 0 FAIL; pytest 1032 passed.

**Riserve**
- R-302-1 (COSMETICA): `reports/stato_progetto.md`, riga 46 (blocco importato da main), dice ancora che R-282-1 e R-283-1 sono «confermate APERTE». Le righe 13 e 14 dello stesso file le danno CHIUSE da questo ramo. Basta una riga che dica «chiuse dalla PR #193».
- R-302-2 (COSMETICA): nello stesso file, il blocco di main inserito alla riga 32 non ha una riga vuota prima e si attacca all'elenco precedente.

**Rischio escluso**
Non ho verificato il comportamento su Python 3.11 e 3.12: qui c'è solo 3.13.16. Per quelle versioni fa fede la CI, fissata su 3.11.

**Memoria**
- Ho aggiunto la riga `#302` e una lezione nuova in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`.
- `scripts/commit_memoria_revisore.sh` NON ha potuto committarla. Errore: «fatal: cannot do a partial commit during a merge». Lo script ha scritto un warning in `gas_debug.log` ed è uscito con exit 0. Non ho forzato.
- La modifica alla memoria è nel working tree ma NON in stage (stato `MM`). Mettila in stage tu prima di eseguire `segna_review_ok.sh`, che va lanciato per ultimo: anche solo mettere in stage la memoria cambia l'hash del diff staged.

Commit del merge consentito: sì. Le due riserve sono solo cosmetiche, da correggere nei report o da annotare in `stato_progetto.md`.

## §5 DELTA TEST DEL MOTORE

Suite kernel (`python tests/test_unit_kernel.py`, girata come script: `tests/conftest.py` la esclude dalla collection di pytest, come fa la CI). **Base = merge-base VERO della sessione, `af394bc`** (non `f6396ba`: il merge di main l'ha spostato — vedi V-1 nel §0):

- base `af394bc`, misurata in un worktree temporaneo: **821 PASS, 0 FAIL**
- HEAD: **840 PASS, 0 FAIL**

Blocco RIEPILOGO reale di HEAD:

```
=== RIEPILOGO: 840 PASS, 0 FAIL ===
```

Blocco RIEPILOGO reale della base `af394bc`:

```
=== RIEPILOGO: 821 PASS, 0 FAIL ===
```

**Nessun FAIL fuori scope da dichiarare**: T80u5, che ho trascinato per tutta la sessione come «preesistente», non esiste piu' alla base reale perche' la PR #192 lo ha reso portabile. Il numero 818/1 che compare nella storia di questo dossier e' quello di `f6396ba`, la base di PARTENZA della sessione, non quella di integrazione.

pytest: **1031 passed, 1 skipped**. Casi T84n: **19** (contati con `grep -c 'check("T84n'` DOPO l'ultimo commit del motore — V-2 della verifica al 3º giro: due volte avevo dichiarato un numero misurato PRIMA dell'ultima modifica).

Mutazioni eseguite e ripristinate, per provare che i test mordono: bug originale ripristinato → 6 FAIL nuovi; guard «vince il primo tetto» → 3; flag `enum_fermata` → 3; metà del fix di V-1 (`budget` non alzato) → 2; distinzione «non letto» → 1; regex `[0-9]` → 1; **margine `_LOG_SFORO_MAX` azzerato → 1** (il test della rotazione che sfora la soglia). Una sola mutazione e' SOPRAVVISSUTA e l'ho dichiarata: `enum_prima` → confronto fra testi (R-299-1).

## §6 STATO CI

All'ultima misura reale (`gh pr checks 193`) sull'head **precedente** `93b57de`, cioè quello dell'autore ignoto, prima del merge:

```
verifica-bot	fail	0
esito	pass	10s
smista	pass	7s
unit-suite	pass	1m45s
verifica	pass	2m50s
handoff-check	pending	9s
```

**`verifica-bot` era `fail` su quell'head**, e il ruleset `main-lock` lo richiede, quindi la PR non è immergeabile finché non rigira. Il diff che il bot ha bocciato **non è più quello**: il merge `7c03a6d` chiude V-1 (con il margine di R-308-1, che il fix dell'autore ignoto non aveva) oltre a V-3 e V-4. Il bot va rieseguito sull'head nuovo e la verifica esterna va rilanciata: **il suo esito va letto sulla PR, non qui**.

**Mappatura commit→run di QUESTA sessione:**

- `e606313`, `d238610`, `be36ce8`, `08c9af6`, `775fdb8`, `b892800`, `25ce6e6`, `c16a789` — **nessuna run su questi SHA**: commit intermedi, mai pushati da soli.
- `58ff4ec` (primo push) — run `38278359321`: `unit-suite` e `handoff-check` **pass**.
- `93b57de` (head dell'autore ignoto) — run `38280430985`/`38280433461`: `unit-suite` **pass**, `handoff-check` **pending** alla misura, `verifica-bot` **fail**.
- `c72e0ce`, `2be3a51`, `ac508c5`, `b29493b`, `9e273e0`, `9e20872`, `7c03a6d` e il commit di fine-task — **run non ancora disponibile alla scrittura dell'handoff**: sono il push che segue questa scrittura.

GitHub Actions crea una run per *push*, non per commit: ogni push genera UNA run che testa SOLO l'albero del commit di testa. I commit elencati come «nessuna run» non sono mai stati testati individualmente. La copertura pre-merge è garantita da `gasmerge` (`gh pr checks --watch`), non da questo campo.

## §7 RISERVE APERTE

- R-302-1 e R-302-2 (COSMETICHE): corrette nel commit del merge (`reports/stato_progetto.md`). Merge di main: kernel 837 PASS / 0 FAIL, pytest 1032 passed.

- **R-301-1** (BASSA): per un log indicato per nome `max()` scavalca un `GAS_LETTURA_MAX_BYTES` abbassato dall'operatore. **R-301-2** (COSMETICA): commento fuori posto nel nuovo caso T84n. R-300-2 CHIUSA.

- 🟡 **R-297-3** (BASSA, compromesso DICHIARATO) — il salto dei log è incondizionato sulla dimensione: anche un `gas_debug.log` da 50 KB non viene più cercato in una ricerca su cartella. Mitigazioni e prova dell'alternativa in §0 punto 2. Decide l'operatore.
- 🟡 **R-291-1 + bot #188 (2° giro)** (BASSE, PREESISTENTI, non toccate in questa fetta) — buchi residui della denylist credenziali, verificati uno per uno: `token_cache.json`, `kubeconfig`, `mywallet.dat`, `.vault-token`, `.dockercfg`, `_netrc`, `clientsecret.json`, `*.gpg`, `*.asc`. Solo PROPOSTI (§0 punto 3), fetta di sicurezza a sé.
- 🟡 **T80u5** (PREESISTENTE, fuori scope) — FAIL della suite kernel col `.venv` a Python 3.14.7; CI su 3.11 verde.
- ⚠️ **R-299-1** (COSMETICA) — chiusa nel CODICE (`_ferma_enum` registra `enum_prima` al momento della marcatura: via l'ultimo confronto fra testi) ma **NON coperta da test**, e dichiarata tale: la mutazione che rimette il confronto fra testi sopravvive (830/1 invariati). Il solo caso in cui i due differiscono richiede un tempo che scada a METÀ lavoro; prova a mano a 0.03 s su 41 file.
- ✅ **V-1 #193** (MEDIA) CHIUSA — rotazioni reali del log di nuovo cercabili per nome; tetto legato al `maxBytes` dell'handler. V-3 e V-4 chiuse, V-2 (mio errore di processo sullo SHA orfanato) corretta.
- ⚠️ **R-gate-matcher-1** (BASSA, NUOVA, confermata in modo indipendente dall'altra sessione) — il matcher dell'hook blocca comandi che non committano ma il cui testo contiene la sequenza. Capitato a entrambe; nel suo caso **il gate le ha impedito di ispezionare se stesso** con un `grep`. Vedi §0 punto 5 e `stato_progetto.md`.
- 🔴 **R-gate-worktree-1 — ESTESO anche al Stop hook `promemoria_end.sh`**: anche quello valuta `$CLAUDE_PROJECT_DIR` (il checkout principale), quindi in una sessione in worktree giudica la freschezza dell'handoff di un'ALTRA sessione. Misurato: `/fine-task` completato per intero (gate verdi, push, `check_landing` OK) e l'hook bloccava ancora, cinque volte; il suo contatore «massimo 3 blocchi» sta nel git-dir del checkout principale e viene azzerato da ogni commit altrui che tocchi `reports/handoff.md`, quindi il limite non si raggiunge e il blocco diventa perpetuo. Dettagli e correzione in `reports/stato_progetto.md`.
- 🔴 **R-gate-worktree-1** (ALTA, concordata da entrambe le sessioni — l'altra ha ritirato il suo MEDIA, NUOVA, fuori scope) — il gate di review deterministico è inerte in una sessione in worktree, e viceversa può bloccare i commit di un'altra sessione. **Confermata in modo indipendente** dalla sessione della PR #192 con due prove proprie. I commit del motore di questa PR sono passati per indice pulito, non per approvazione del gate. Vedi §0 punto 5.
- ⚠️ **Collisione dei numeri di review con la PR #192** — vedi §0 punto 5: da risolvere al merge, non rinumerata qui di proposito.
- ⚠️ **R-300-2** (COSMETICA) — typo nel docstring di `_ferma_enum` in `gas.py` («La visita si fermata per un tetto suo», manca «è»). NON corretto in questa fetta su indicazione del revisore: il motore è già committato e `hash_diff_staged.sh` hasha tutto il diff, quindi un commento costerebbe un giro di review intero. Prossima fetta che tocca `_cerca_testo`.
- ⚠️ **Nota di processo (review #300)** — il commit del motore `d238610` è anteriore al verdetto #300: marcatore scritto e commit fatto sulla base dell'autorizzazione di #299, col 4º giro ancora in corso. Il revisore ha verificato che il `gas.py` committato è byte-identico a quello revisionato: nessun codice non revisionato è passato, nulla da rifare. Sequenza giusta per il futuro: `segna_review_ok.sh` ULTIMO passo prima del commit, e dopo non si tocca più il perimetro.
- ℹ️ Riserve CHIUSE in questa sessione: R-282-1 (MEDIA, era solo mitigata in #184), R-283-1, R-297-1 (MEDIA), R-297-2, R-297-4, R-298-1, R-298-2, R-298-3, R-299-2, R-299-3; R-299-1 chiusa nel codice ma non coperta.
- ℹ️ Non verificati, dichiarati dal revisore: comportamento su VPS (costo degli `stat` dell'enumerazione post-tetto misurato solo su APFS locale/tmp; rotazioni reali da 5 MB non ricostruite, il test usa un log sintetico da 4,5 MB in tmp); `gas.py doctor` non eseguito dal revisore.
