# REPORT — `cerca_testo` su cartella: il budget di byte non mente più

**Data:** 2026-10-12
**Ramo:** `feat/cerca-testo-budget-onesto` (da main aggiornato `f6396ba`)
**Fetta:** unica. Il punto 2 del brief originale (credenziali illeggibili) NON è stato toccato: è già in main con la PR #188.

---

## DECISIONI UMANE RICHIESTE

1. **Merge della PR** (numero e URL in `reports/handoff.md` §0). NON l'ho mergiata: la regola di merge autonomo di CLAUDE.md ammette il merge da soli solo su `APPROVATO` secco senza alcun finding V-x. Qualsiasi altro verdetto aspetta te.
2. **R-297-3 — il salto dei log è incondizionato sulla dimensione** (riserva del revisore, BASSA, lasciata APERTA di proposito). Anche un `gas_debug.log` da 50 KB, che sta largamente in ogni tetto, non viene più cercato in una ricerca su cartella, mentre CLAUDE.md sez. 3 fa dell'ispezione del log un'attività di prima classe. Il tuo brief chiedeva esplicitamente di saltare i log, quindi non ho cambiato la scelta da solo. Le mitigazioni ci sono tutte (il salto è dichiarato in intestazione con l'istruzione su come cercarci dentro, e i log restano cercabili indicandoli per nome). **L'alternativa — saltare i log solo oltre il tetto per file — l'ho provata e perde qualcosa:** senza il salto incondizionato, un log le cui righe contengono il testo cercato si mangia il tetto dei 200 RISULTATI e `modules/gate/gate.py` sparisce di nuovo, pur avendo il budget di byte intatto. La prova vale **proprio per l'alternativa condizionata**, e non solo per «nessun salto», perché il log del test (5000 righe, circa 85 KB) sta SOTTO il tetto per file: con «salta solo i log oltre il tetto per file» quel log verrebbe letto e il tetto dei risultati si esaurirebbe allo stesso modo. (Precisazione chiesta dal revisore: senza di essa la prova è attaccabile.) Se preferisci l'altro compromesso si cambia in una riga: dimmelo.
3. **Buchi residui della denylist credenziali** (sotto, §Proposte): NON implementati, come da tuo vincolo. Verificati uno per uno con `lettura_consentita()`, non solo riportati.

---

## ESITO

**Fetta unica — `cerca_testo` su cartella, il budget di byte non deve mentire: FATTA.**

### Riproduzione (confermata da me su main `f6396ba` PRIMA del fix)

In una root col repo più un `gas_debug.log` da 4,5 MB di righe innocue, `cerca_testo "def gate_classify"` dalla root dava:

```
0 righe trovate in 15 file; 35 file oltre il tetto di byte saltati (usa leggi_righe su quei file); 2 voci protette o illeggibili saltate; ...
gate.py trovato: False
```

Togliendo il log lo trovava (49 file). I miei numeri (15/35) differiscono da quelli del brief (13/64) solo perché la mia root di prova copia un sottoinsieme del repo: il comportamento è identico e confermato.

**Causa misurata:** in `_cerca_testo` lo skip per-file confrontava `f.stat().st_size` col budget **RESIDUO**, quindi un file da 4,5 MB stava sotto il tetto da 5 MB, veniva letto interamente e consumava il budget; i file successivi venivano tutti saltati e dichiarati «oltre il tetto di byte» — falso — e la ricerca si interrompeva senza dirlo (`break` muto su `stato["tetto"]`).

Dopo il fix, stessa root, stesso comando: `1 righe trovate in 49 file; 1 log del kernel (gas_debug.log) non cercati: indicane uno in relative_path per cercarci dentro; ...` → `modules/gate/gate.py:372: def gate_classify(...)`. Identico al caso senza il log.

### (a) Log del kernel saltati nella ricerca su cartella — FATTA
`_LOG_KERNEL_RE = re.compile(r"gas_debug\.log(\.\d+)?")`, usata con `fullmatch` su `f.name` e **solo** se `su_cartella`. Copre `gas_debug.log` e le rotazioni `.1/.2/.3` (e qualunque `.N`, se `backupCount` cambia). Sono contati e dichiarati nell'intestazione con l'istruzione su come cercarci dentro. Indicati per nome in `relative_path` restano cercabili, e per loro non vale nemmeno il tetto per file.

### (b) Tetto per singolo file, indipendente dal budget residuo — FATTA
`LETTURA_MAX_BYTES_PER_FILE = 1_000_000`, env `GAS_LETTURA_MAX_BYTES_PER_FILE` (convenzione `GAS_LETTURA_MAX_*`), limato con `min(..., LETTURA_MAX_BYTES)`.

**Perché 1 MB:** è 1/5 di `LETTURA_MAX_BYTES`, quindi nessun singolo file può prosciugare il budget da solo (ne servono almeno 5); e il sorgente più grande del progetto, `gas.py`, sta attorno ai 200 KB, quindi tutti i file di codice ci stanno dentro con larghezza.

Chi lo supera è saltato e **NOMINATO** (primi 5 nomi, poi «, ...»): chiude R-283-1. Su un file indicato per nome non si stringe nulla: resta il solo budget della chiamata, come prima — altrimenti un log indicato per nome non sarebbe più cercabile, contro il punto (a).

### (c) Messaggi distinti — FATTA
«N file oltre il tetto di X byte per file saltati (nomi)» non è più «byte letti (X, budget complessivo della chiamata, GAS_LETTURA_MAX_BYTES): <file> letto solo in parte». Nel secondo caso l'intestazione dice **RICERCA INCOMPLETA**, quale file è stato letto solo a metà e **quanti file sono rimasti non letti**: dopo il primo tetto il loop non fa più `break` ma continua a ENUMERARE (solo iterazione del generatore, nessuna apertura di file) per poterli contare.

Due conseguenze, entrambe gestite:
- vince il **PRIMO** tetto scattato: `_visita_cartella` non sovrascrive più il motivo vero col proprio;
- il conto è un **PAVIMENTO**, non un totale (R-297-1, vedi sotto).

---

## Riserve del revisore (review #297, APPROVATO CON RISERVE)

Tre su quattro corrette PRIMA del commit:

- ✅ **R-297-1 (MEDIA)** — «N file rimasti non letti» era un pavimento spacciato per totale: `non_letti` lo conta il generatore, che ha a sua volta un tetto, quindi se dopo il primo tetto scattava anche un tetto della VISITA (voci/tempo) il numero mentiva al ribasso e il secondo tetto restava invisibile per via dell'`or`. Misurato dal revisore: 12 file, `LETTURA_MAX_FILE=6`, budget 200 → dichiarava «2 file rimasti non letti» mentre 9 non erano stati cercati. **Fix:** `GasKernel._segna_tetto()` registra TUTTI i tetti scattati (`stato["tetti"]`, in ordine) e lascia `stato["tetto"]` al primo; l'intestazione dice «almeno N file rimasti non letti (anche l'enumerazione si è fermata: ...)» quando c'è un secondo tetto, e il numero esatto quando non c'è. Era la riserva più grave e andava al cuore della fetta («il budget non deve mentire»), per questo l'ho chiusa invece di tracciarla.
- ✅ **R-297-2 (BASSA)** — il mio test «vince il primo tetto» era vacuo: con 5 file il tetto di 500 voci non poteva scattare e la mutazione del guard sopravviveva. Ora `LETTURA_MAX_FILE=3` in quel blocco, più due casi nuovi.
- ✅ **R-297-4 (COSMETICA)** — lo schema del tool non promette più «tutti i file di testo di una cartella» e dichiara il salto dei log; su un file indicato per nome l'intestazione dice «byte della chiamata», non «byte per file».
- ⚠️ **R-297-3 (BASSA)** — APERTA di proposito: vedi DECISIONE UMANA 2.

Rischi che il revisore ha dichiarato di NON aver verificato: `gas.py doctor` (fa ping di rete reali; exit 0 misurato da me); comportamento su VPS (il costo degli `stat` su alberi oltre 500 voci su disco lento è misurato solo su APFS locale, e il set reale di rotazioni da 5 MB non è stato ricostruito: il test usa un log sintetico da 4,5 MB in tmp); T80u5 (FAIL preesistente, fuori perimetro).

Dopo i fix ho richiamato il revisore sul diff nuovo: **review #298, APPROVATO CON RISERVE**, tre riserve nuove, tutte chiuse PRIMA del commit:

- ✅ **R-298-1 (BASSA)** — la riserva che contava. Il registro dei tetti era **testuale**: dedup e filtro confrontavano stringhe, quindi un secondo tetto con la STESSA etichetta era invisibile. Il caso reale è il **tempo**, che `_cerca_testo` e `_visita_cartella` formattano identico e la cui scadenza è condivisa. Misurato dal revisore (41 file, primo file da 900 KB, `LETTURA_MAX_SECONDI=0.03`): 40 file mai cercati e l'intestazione **taceva**, esattamente come prima del fix. Non era un numero falso — col tetto di tempo `non_letti` è 0 per costruzione, perché il generatore controlla la scadenza prima di ogni `yield` — era silenzio, e il punto (c) del tuo brief («quanti file non sono stati letti») non veniva onorato **proprio sul tetto più probabile su un VPS con alberi grandi**. **Chiusa alla radice:** via il confronto fra testi, la visita marca la FONTE (`stato["enum_fermata"]`); il conto è dichiarato ESATTO solo se l'enumerazione è arrivata in fondo, altrimenti l'intestazione dice che non si sa quanti file siano rimasti. Riprodotto da me lo stesso caso dopo il fix: «51082 righe trovate in 1 file; RICERCA INCOMPLETA: raggiunto il tetto di tempo (0.03 s); quanti file siano rimasti non letti non si sa: l'enumerazione si è fermata lì».
- ✅ **R-298-2 (COSMETICA)** — «almeno 0 file rimasti non letti» era raggiungibile (vero ma assurdo da leggere; l'avevo visto anch'io in una sonda) e i test non pinnavano il numero. Chiusa dalla stessa riscrittura; i due test ora pinnano «almeno 1» e «almeno 3».
- ✅ **R-298-3 (COSMETICA)** — `reports/stato_progetto.md` riportava 825 test mentre la suite dava 828: corretto al numero reale e completato l'elenco dei casi T84n.

Il revisore ha anche chiesto una precisazione sulla prova di R-297-3: l'ho aggiunta sopra (DECISIONE UMANA 2) e in `stato_progetto.md`.

Terzo giro sul diff cambiato: **review #299, APPROVATO CON RISERVE**, tre riserve tutte COSMETICHE, nessuna bloccante. Le ho chiuse tutte e tre perché due erano «un'affermazione che non corrisponde al codice» — proprio il difetto che questa fetta esiste per togliere — e la terza era una riga:

- ✅ **R-299-3 (COSMETICA)** — `reports/stato_progetto.md` descriveva ancora il meccanismo del 2º giro (`stato["tetti"]`) e **contraddiceva** il punto R-298-1 scritto subito sotto. Il report è la fonte di verità (CLAUDE.md sez. 3): riallineato al meccanismo finale, e corretta anche la promessa del punto (c) (il conto è esatto solo a enumerazione completa).
- ✅ **R-299-2 (COSMETICA)** — il commento del test sul tetto di tempo prometteva di riprodurre la COLLISIONE di due tetti «tempo (0 s)», che con `LETTURA_MAX_SECONDI=0.0` non avviene: la visita si ferma prima di ogni `yield`, quindi scatta un solo tetto. Un commento che dichiara più di quello che il test prova è esattamente il genere di cosa che il canone del progetto non tollera: riscritto per dire il vero (è una regressione sul SINTOMO, valida), e aggiunto il test che mancava sul ramo «fermata anche l'enumerazione» con **0** file contati (non stampa nessun numero, non «almeno 0»).
- ⚠️ **R-299-1 (COSMETICA)** — chiusa nel codice, **ma non coperta da test, e lo dichiaro**. Il ramo «l'enumerazione si è fermata lì» si sceglieva ancora per uguaglianza di TESTO, quindi con due tetti di pari etichetta la fermata poteva essere attribuita al componente sbagliato (innocuo: in entrambi i casi il conto è ignoto e la sostanza vera). Ora `_ferma_enum()` registra `enum_prima` al momento della marcatura: via l'ULTIMO confronto fra stringhe. **Ho misurato che la mutazione che rimette il confronto fra testi SOPRAVVIVE** (830 PASS / 1 FAIL invariati): il solo caso in cui i due comportamenti differiscono richiede un tempo che scada a METÀ lavoro, e mettere un orologio nella suite la renderebbe instabile. La prova resta quella a mano (41 file, `LETTURA_MAX_SECONDI=0.03`). Non spaccio per coperto ciò che non lo è.

Il revisore ha confermato che la formulazione del compromesso R-297-3 è «onesta e completa».

Quarto giro (lanciato per diligenza, non perché il gate lo richiedesse): **review #300, APPROVATO CON RISERVE** — «niente di sostanziale: il meccanismo è corretto, coperto dove si può coprirlo, e la cosa che NON è coperta l'hai dichiarata tu col numero della mutazione... **Non serve un altro giro sul codice.**» Ha misurato di persona che R-299-1 è chiusa nel comportamento (stesso caso a 0.03 s: ora dice «si è fermata anche l'enumerazione (tempo (0.03 s))» invece di «si è fermata lì»), e ha risposto no alla mia domanda se valesse la pena un test con l'orologio finto: quello che resta scoperto non è il flag (coperto: mutazione «`enum_prima` sempre True» = 3 FAIL) ma la sola equivalenza con la vecchia attribuzione testuale, e un orologio finto nella suite costerebbe più fragilità di quanto valga. Due riserve, entrambe cosmetiche:

- ✅ **R-300-1 (COSMETICA)** — avevo scritto «13 casi T84n» in `stato_progetto.md`: i `check("T84n` sono **12**. L'avevo contato male includendo T84f, che non è un caso T84n. Verificato da me con `grep -c` e corretto, e aggiunto all'elenco il caso che mancava.
- ⚠️ **R-300-2 (COSMETICA, lasciata APERTA)** — typo in un docstring di `gas.py` («La visita si fermata», manca «è»). **Non l'ho corretto, su indicazione del revisore stesso**: il motore è già committato e `hash_diff_staged.sh` hasha tutto il diff, quindi correggere un commento rimetterebbe il perimetro in gioco e costerebbe un giro di review intero per un accento. Va nella prossima fetta che tocca `_cerca_testo`.

**Osservazione di processo che accetto**, e che ho scritto in `stato_progetto.md` invece di lasciarla implicita: il commit del motore `d238610` è **anteriore al verdetto #300**. Ho scritto il marcatore e committato sulla base dell'autorizzazione esplicita di #299 («Commit consentito: sì») con le correzioni che quel verdetto prescriveva, mentre il quarto giro era ancora in corso. Il revisore ha verificato che il `gas.py` committato è **byte-identico** a quello che aveva in mano, quindi non è passato codice non revisionato e non c'è nulla da rifare — ma la sequenza giusta è `segna_review_ok.sh` come ULTIMO passo prima del commit, e dopo non si tocca più il perimetro.

---

## TEST

Numeri REALI misurati con il `.venv` del progetto (Python 3.14.7), non stimati:

| | kernel | pytest |
|---|---|---|
| main `f6396ba` (baseline, misurata da me in un worktree temporaneo) | **818 PASS, 1 FAIL** | — |
| questo ramo | **830 PASS, 1 FAIL** | **1031 passed, 1 skipped** |

L'unico FAIL è **T80u5, PREESISTENTE e fuori scope**: col `.venv` del progetto (Python 3.14.7) un JSON annidato 100k viene parsato invece di sollevare `RecursionError`. È presente identico su main `f6396ba`. La CI pinna Python 3.11 ed è verde. Non l'ho toccato.

`tests/test_unit_kernel.py` è escluso dalla collection di pytest (`conftest.py`) e girato come script, come fa la CI: le due suite non si sovrappongono.

**Test nuovi (T84n), 12 casi** (contati con `grep -c 'check("T84n'`; il 13º che avevo scritto era T84f, che non è un caso T84n — R-300-1)**, tutti sulla riproduzione reale:**
1. un `gas_debug.log` da 4,5 MB non nasconde più `gate.py`; i log sono saltati, contati e dichiarati;
2. un log da 5000 righe che contengono il testo cercato non esaurisce il tetto dei risultati prima di arrivare a `modules/`;
3. i log indicati per nome restano cercabili, rotazioni comprese;
4. le rotazioni `.N` sono saltate nella ricerca su cartella come il log principale;
5. budget esaurito → messaggio distinto da «file troppo grande», RICERCA INCOMPLETA, conto dei file non letti;
6. `GAS_LETTURA_MAX_BYTES_PER_FILE` ri-tara il tetto;
7. vince il primo tetto scattato, con il tetto della visita che scatta davvero (R-297-2);
8. col secondo tetto il conto è dichiarato pavimento e il secondo tetto non resta invisibile (R-297-1);
9. il caso misurato dal revisore (12 file, cap voci 6, budget 200);
10. il tetto di **TEMPO** non tace sui file mai cercati e dichiara di non sapere quanti sono (R-298-1) — con `LETTURA_MAX_SECONDI=0.0`, quindi senza orologio nel test;
11. il ramo «fermata anche l'enumerazione» con **0** file contati non stampa nessun numero (R-298-2/R-299-2);
12. su un file indicato per nome il tetto è «byte della chiamata» (R-297-4);
Più **T84f aggiornato** al nuovo meccanismo (non è un caso T84n).

T84f aggiornato al nuovo meccanismo (il vecchio test tarava `LETTURA_MAX_BYTES` per provocare lo skip per-file: ora serve anche `LETTURA_MAX_BYTES_PER_FILE`).

**Mutazioni eseguite da me e poi ripristinate** (`git diff` verificato pulito dopo ognuna) — i test mordono davvero:
- tetto per file → `budget[0]` + salto log disattivato (= bug originale): **822 PASS, 7 FAIL**, 6 miei; nel caso del log da 5000 righe l'output torna a «200 righe trovate in 1 file … tetto di risultati (200)» e `gate.py` sparisce;
- guard «vince il primo tetto» → assegnazione secca: **3 FAIL** (prima della correzione di R-297-2 la mutazione sopravviveva: era la riserva del revisore);
- flag `enum_fermata` mai marcato (= bug R-298-1): **3 FAIL**;
- `enum_prima` → confronto fra testi (= R-299-1): **nessun FAIL, mutazione SOPRAVVISSUTA** — dichiarato sopra, non è coperto.

`python gas.py doctor`: exit 0 (i 5 FAIL sono chiavi API e `.env` assenti nel worktree, attesi).

---

## PROPOSTE — NON implementate, serve la tua decisione

### Buchi residui della denylist credenziali (punto 2 del brief: NON toccato, già in main con #188)

Verificati uno per uno con `lettura_consentita()` su questo ramo, **tutti LEGGIBILI oggi**:

| nome | perché passa |
|---|---|
| `token_cache.json` | `_CHIAVE_PRIVATA_RE` vuole il punto subito dopo `token`: `token.json` e `tokens.json` sono bloccati, `token*.json` con suffisso no |
| `kubeconfig` | tracciato in R-291-1: senza punto non matcha |
| `mywallet.dat` | tracciato in R-291-1: `wallet.dat` è bloccato, con prefisso no |
| `.vault-token` | bot #188 (2° giro) |
| `.dockercfg` | bot #188 (2° giro) |
| `_netrc` | bot #188 (2° giro); `.netrc` è bloccato |
| `clientsecret.json` | bot #188 (2° giro) |
| `*.gpg` / `*.asc` | bot #188 (2° giro) |

Sono tutti nel perimetro `modules/gate/` (fetta di sicurezza): vanno in una fetta loro, con review e doppio passaggio di verifica. Non li ho toccati perché il tuo brief lo vietava esplicitamente.

### Niente altro proposto
Non ho trovato altro che valga una fetta. Non ho toccato nulla fuori dallo scope.

---

## ANOMALIE

1. **Nota di processo sulla PR #184.** Come chiesto, ho annotato in `reports/stato_progetto.md` che la PR #184 è stata mergiata in autonomia con verdetto del bot `APPROVATO CON RISERVE`, quindi **fuori dalla regola di merge autonomo** di CLAUDE.md (che ammette il merge da soli solo su `APPROVATO` secco senza alcun finding V-x). Segnalo una discrepanza che non sta a me risolvere: la voce esistente di `feat/via-binari-run-command` in `stato_progetto.md` registra quel merge come «merge autonomo **autorizzato dall'operatore**». Le due letture non coincidono — ho scritto entrambe nel file invece di sovrascrivere il record esistente. La ricostruzione la decidi tu.
2. **Il worktree di questa sessione partiva già da main aggiornato** (`f6396ba`), non dal detached HEAD del checkout principale: ho creato il ramo da lì. Il checkout principale resta in detached HEAD a `63e9fec`, come l'ho trovato — non l'ho toccato.
3. Il revisore ha committato la propria memoria sul ramo (`e606313`), come da protocollo.
