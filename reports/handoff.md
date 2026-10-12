# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-12 — `cerca_testo` su cartella: il budget di byte non deve mentire

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR — numero e URL compilati al passo 4bis dopo il push (solo da `gh`).
2. **R-297-3 (BASSA, APERTA di proposito): il salto dei log è incondizionato sulla dimensione.** Anche un `gas_debug.log` da 50 KB, che sta largamente in ogni tetto, non viene più cercato in una ricerca su cartella, mentre CLAUDE.md sez. 3 fa dell'ispezione del log un'attività di prima classe. Il brief chiedeva esplicitamente di saltare i log, quindi la scelta non è stata cambiata dall'agente. Mitigazioni presenti: salto dichiarato in intestazione con l'istruzione su come cercarci dentro; log cercabili indicandoli per nome; il salto protegge anche il tetto dei RISULTATI. L'alternativa «salta solo i log oltre il tetto per file» è stata provata e perde quella protezione — e la prova vale **proprio per l'alternativa condizionata** perché il log del test (5000 righe, ≈85 KB) sta SOTTO il tetto per file: verrebbe letto e il tetto dei risultati si esaurirebbe allo stesso modo. Se l'operatore preferisce l'altro compromesso, è una riga.
3. **Buchi residui della denylist credenziali**: NON implementati (vincolo del brief: `modules/gate/` è già in main con la PR #188). Verificati uno per uno con `lettura_consentita()`, tutti LEGGIBILI oggi: `token_cache.json` (la regex vuole il punto subito dopo `token`; `token.json` e `tokens.json` sono bloccati), `kubeconfig`, `mywallet.dat`, `.vault-token`, `.dockercfg`, `_netrc`, `clientsecret.json`, `*.gpg`, `*.asc`. Vanno in una fetta loro, di sicurezza.
4. **Nota di processo**: la PR #184 è stata mergiata in autonomia con verdetto del bot `APPROVATO CON RISERVE`, quindi **fuori dalla regola di merge autonomo** di CLAUDE.md (merge da soli solo su `APPROVATO` secco senza alcun finding V-x). La voce esistente di `feat/via-binari-run-command` in `reports/stato_progetto.md` registra quel merge come «autorizzato dall'operatore»: le due letture non coincidono, sono state scritte entrambe nel file invece di sovrascrivere il record, e la ricostruzione la decide l'operatore.

---

## §1 SCOPE & ESITO FETTE

- **Fetta unica — `cerca_testo` su cartella: il budget di byte non deve mentire**: `FATTA`
  Tutti e tre i punti del brief: (a) log del kernel saltati nella ricerca su cartella, contati e dichiarati, cercabili per nome; (b) tetto per singolo file indipendente dal budget residuo, ri-tarabile da env, chi lo supera è saltato e NOMINATO; (c) messaggi distinti fra «file troppo grande» e «budget di byte esaurito», con RICERCA INCOMPLETA e il conto dei file non letti.
- **Punto 2 del brief originale (credenziali illeggibili)**: `SALTATA — già in produzione con la PR #188 (`_CHIAVE_PRIVATA_RE` in `modules/gate/gate.py`)`. Il brief vietava di toccarlo. I buchi residui sono solo PROPOSTI (§0 punto 3).
- **T80u5 (FAIL della suite kernel)**: `SALTATA — preesistente e fuori scope`. Presente identico su main `f6396ba`: col `.venv` del progetto (Python 3.14.7) un JSON annidato 100k viene parsato invece di sollevare `RecursionError`. La CI pinna Python 3.11 ed è verde.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   9 +++++++++
 gas.py                             | 115 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------
 reports/diff_sessione.md           |  37 +++++++++++++++++++++++++++++--------
 reports/handoff.md                 | 286 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |  27 ++++++++++++++++++++++++---
 reports/ultimo_report.md           | 157 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------
 tests/test_unit_kernel.py          | 172 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
 7 files changed, 616 insertions(+), 187 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
d238610 fix(cerca_testo): il budget di byte non mente piu' (R-282-1, R-283-1)
08c9af6 chore(revisore): memoria review #299 — APPROVATO CON RISERVE
be36ce8 chore(revisore): memoria review #298 — APPROVATO CON RISERVE
e606313 chore(revisore): memoria review #297 — APPROVATO CON RISERVE
```

## §4 VERDETTO DEL REVISORE (per commit motore)

Tre giri sullo stesso diff staged: dopo ogni giro le riserve sono state corrette e il diff è cambiato, quindi è stato richiesto un verdetto nuovo. Verdetti INTEGRALI, incollati, in ordine.

### Giro 1 — review #297

## VERDETTO: APPROVATO CON RISERVE

Review #297 — diff staged su `feat/cerca-testo-budget-onesto` (base main f6396ba), worktree `/Users/gas/Gas/.claude/worktrees/optimistic-austin-78debb`. Letti prima: CLAUDE.md (sez. 1/4/5/8/9/10), `reports/stato_progetto.md` (righe 4, 9-14, 45-51 via Grep, come da sez. 11), `.claude/agents/memoria_revisore.md` (ultime review #288-#296).

Il bug raccontato nel brief è reale e il fix lo chiude: la causa (skip per-file confrontato col budget RESIDUO) non c'è più e `cerca_testo` dalla root ritrova `modules/gate/gate.py` col log da 4,5 MB in mezzo. Nessun antipattern del Wall of Shame (nessuno slicing di history, nessuna simulazione di output tool). Le riserve sono tutte sulla ONESTÀ RESIDUA dei messaggi e sulla copertura di una delle quattro scelte, non sulla correttezza del flusso.

### Elementi del diff esaminati

1. `/Users/gas/Gas/.claude/worktrees/optimistic-austin-78debb/gas.py:2107` — `tetto_file = min(LETTURA_MAX_BYTES_PER_FILE, LETTURA_MAX_BYTES) if su_cartella else LETTURA_MAX_BYTES` (scelte 1 e 2). Rischio esaminato: regressione sul file indicato per nome, e tetto aggirabile da env. Per `su_cartella=False` il valore è identico a quello che prima stava in `budget[0]` al primo file → comportamento invariato, provato dai test T84f riscritti; `min()` limita anche un `GAS_LETTURA_MAX_BYTES_PER_FILE` enorme, e `_env_int(min_val=1)` regge valori sporchi. **Esito: ok.**
2. `gas.py:2119` — `if su_cartella and self._LOG_KERNEL_RE.fullmatch(f.name)` (scelte 1/5). Rischio esaminato: il log non più ispezionabile, e over-match. `fullmatch` su `f.name` copre `gas_debug.log` e ogni rotazione `.N` (anche oltre `.3`), non tocca `gas_debug.log.gz` né una cartella omonima (il generatore filtra `v.is_file()`), e il corto circuito su `su_cartella` lascia cercabile il log indicato per nome (provato da T84n `_oL3`). Mutazione verificata: disattivando il salto, 4 test T84n vanno in FAIL e nel caso `_oL2` i 200 risultati finiscono tutti nel log facendo sparire `gate.py` → il salto protegge il tetto dei RISULTATI, non solo i byte. **Esito: ok, con riserva 3.**
3. `gas.py:2116` — `non_letti += 1; continue` al posto del `break` (scelta 3). Rischio esaminato: costo e aperture di file indesiderate dopo il tetto. Dopo il tetto non si fa né `stat` né `_rel_root`; il generatore continua ma `_risolvi_lettura` (gas.py:1849) fa solo operazioni di percorso e al massimo 2 `stat`, nessuna `open`, ed è capato da `LETTURA_MAX_FILE = 500` (gas.py:1822) e dalla scadenza di 5 s condivisa. Nessuna apertura, costo limitato. **Esito: ok sul costo, riserva 1 sul numero stampato.**
4. `gas.py:1938/1942` — `stato["tetto"] = (stato["tetto"] or ...)` nella visita (scelta 4). Rischio esaminato: effetto su `_elenca_cartella` e utilità reale del guard. Per `_elenca_cartella` è un no-op verificato in esecuzione (con `LETTURA_MAX_FILE=4` e con `LETTURA_MAX_SECONDI=0.0` l'intestazione dice ancora «ELENCO INCOMPLETO: … numero di voci (4)» / «… tempo (0 s)»): quella funzione non scrive mai `tetto` e i due siti fanno `return` subito. Il guard serve davvero: con la mutazione ad assegnazione secca, su 12 file con `LETTURA_MAX_FILE=6` e budget 200 il motivo vero («byte letti … f02.txt letto solo in parte») viene sostituito da «numero di voci (6)». **Esito: ok nel merito, riserva 2 sulla copertura.**
5. `gas.py:2149` + `gas.py:2163/2170` — messaggi distinti «budget complessivo della chiamata» / «log del kernel non cercati» / «N file rimasti non letti» (punto c). Rischio esaminato: fuga di informazione e righe forgiate. I nomi passano da `_rel_root` (gas.py:1877 → `rendi_visibili(a_capo=False)`, R-284-1) e provengono SOLO da file già approvati da `_risolvi_lettura`: i percorsi negati finiscono in `omessi` e non vengono mai nominati (es. `.env` non può comparire in `nomi_grandi`, gas.py:2126). Nessun `str(e)`, solo interi e percorsi dentro la root. **Esito: ok.**
6. `tests/test_unit_kernel.py:8100` — test «vince il PRIMO tetto scattato». Rischio esaminato: test che dichiara più di quanto prova. Con 5 file in `molti/` il tetto «numero di voci» (500) non può scattare: la mutazione del guard sopravvive (825 PASS / 1 FAIL identici). **Esito: riserva 2.**
7. `gas.py:831` (contesto, riga non toccata dal diff) — descrizione dello schema di `cerca_testo`: «in tutti i file di testo di una cartella». Ora i log sono esclusi. **Esito: riserva 4 (cosmetica).**

### Numeri riprodotti da me (venv del progetto, `PYTHONDONTWRITEBYTECODE=1`)
- `tests/test_unit_kernel.py`: **825 PASS, 1 FAIL** — l'unico FAIL è T80u5, preesistente (confermo la diagnosi: Python 3.14.7 locale, CI pinnata 3.11).
- `pytest -q`: **1031 passed, 1 skipped** in 153 s.
- Mutazioni (applicate e poi ripristinate verificando `git diff --stat` vuoto): `continue`→`break` + salto log disattivato → **821 PASS, 5 FAIL** (i 4 test T84n mordono); `stato["tetto"] or`→assegnazione secca → **825 PASS, 1 FAIL invariati** (guard non coperto).

### Riserve (numerate, con gravità)

1. **R-297-1 (MEDIA) — «N file rimasti non letti» è un PAVIMENTO, non un totale.** `non_letti` conta solo i file che il generatore riesce ancora a produrre: se dopo il primo tetto scatta anche un tetto della VISITA (500 voci o 5 s), il numero mente al ribasso e il secondo tetto resta invisibile per via dell'`or`. Misurato: 12 file, `LETTURA_MAX_FILE=6`, budget 200 → «RICERCA INCOMPLETA: raggiunto il tetto di byte letti (200 …): f02.txt letto solo in parte; **2 file rimasti non letti**», mentre i file non cercati erano 9 e il tetto di voci era scattato. È comunque meglio del `break` muto di prima (che non diceva nulla), ma rispetto al criterio dichiarato della fetta («il budget non deve mentire») resta una bugia più piccola della precedente. Suggerimento minimo: «almeno N file rimasti non letti», oppure dichiarare anche il secondo tetto scattato (es. tenere i motivi in una lista e stamparli tutti).
2. **R-297-2 (BASSA) — scelta 4 non coperta da test.** Vedi sopra: la mutazione sopravvive e il test che si intitola «vince il PRIMO tetto scattato» non prova il guard. Fix da una riga: abbassare `_kL.LETTURA_MAX_FILE` (es. a 3) in quel blocco e asserire che il motivo resta «risultati»; con l'assegnazione secca il test deve fallire.
3. **R-297-3 (BASSA) — il salto dei log è incondizionato sulla dimensione.** Un `gas_debug.log` da 50 KB, che sta largamente in ogni tetto, non viene più cercato in una ricerca su cartella; CLAUDE.md sez. 3 fa dell'ispezione del log un'attività di prima classe. Mitigazioni accettabili e presenti: dichiarato in intestazione con l'istruzione su come cercarci, cercabile per nome, e il salto protegge anche il tetto dei risultati (provato dalla mutazione M3). Resta da dichiarare come compromesso; un'alternativa sarebbe saltare i log solo oltre `tetto_file`, ma perderebbe la protezione sui risultati.
4. **R-297-4 (COSMETICA) — promesse dello schema e del messaggio.** `gas.py:831` dice ancora «tutti i file di testo di una cartella» (ora: esclusi i log del kernel). Inoltre nel caso di file indicato per nome l'intestazione recita «oltre il tetto di 5000000 byte **per file**», mentre quello è il budget della chiamata: la dizione «per file» è fuori registro lì.

### Rischio esplicitamente escluso (non verificato)
- `python gas.py doctor` **non eseguito**: fa ping di rete reali ai provider; prendo per buono l'exit 0 dichiarato dall'autore senza prova indipendente.
- **Comportamento su VPS non verificato**: non riproducibile in dev. In particolare il costo in `stat` della scelta 3 su un albero > 500 voci su disco lento è misurato solo su APFS locale/tmp, e il set reale di rotazioni da 5 MB non è stato ricostruito (il test usa un log sintetico da 4,5 MB in tmp).
- **T80u5 non indagato**: FAIL preesistente anche su main f6396ba, fuori dal perimetro di questa fetta.
- **`reports/stato_progetto.md` non in stage**: ne ho letto il contenuto (righe 9-14 coerenti col diff, R-282-1 e R-283-1 marcate chiuse correttamente) ma non lo giudico come parte del diff sotto review.

### Memoria aggiornata
Riga contatore `#297 — 2026-10-12 — APPROVATO CON RISERVE — …` aggiunta in coda a `/Users/gas/Gas/.claude/worktrees/optimistic-austin-78debb/.claude/agents/memoria_revisore.md`, con due lezioni nuove datate (guard «vince il primo» da provare con due tetti e con la mutazione; contatore ricavato da una fonte a sua volta capata = pavimento). Committata con `bash scripts/commit_memoria_revisore.sh` → `e606313 chore(revisore): memoria review #297`; index verificato intatto dopo il commit (`gas.py` e `tests/test_unit_kernel.py` ancora staged, nient'altro).

Commit consentito: sì, con le 4 riserve tracciate in `reports/stato_progetto.md` (R-297-1 MEDIA resta aperta se non la correggi ora; R-297-2 si chiude con una riga di test).

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

### Base dell'autorizzazione al commit, e giro 4

Il commit di questo diff è autorizzato da **#299** («Commit consentito: sì»), applicate le correzioni che il verdetto stesso prescriveva o permetteva: R-299-3 (solo `reports/`, fuori perimetro), la riga di commento di R-299-2 più il test che mancava sul ramo 3, e l'opzionale R-299-1. Il diff staged differisce da quello di #299 **solo** per quelle correzioni.

Un **quarto giro** è stato lanciato per diligenza (non perché il gate lo richiedesse) sul diff finale. Il suo verdetto, quando arriva, va riportato all'operatore; se solleva qualcosa di sostanziale, la correzione comporta un nuovo commit e quindi la riesecuzione INTEGRALE di `/fine-task` (gate post-fine-task). Riserva nota e già dichiarata, misurata da me e NON coperta da test: **R-299-1** — la mutazione che rimette il confronto fra testi SOPRAVVIVE (830 PASS / 1 FAIL invariati), perché il solo caso in cui i due comportamenti differiscono richiede un tempo che scada a METÀ lavoro e un orologio nella suite la renderebbe instabile; la prova resta quella a mano (41 file, `LETTURA_MAX_SECONDI=0.03`).

## §5 DELTA TEST DEL MOTORE

Suite kernel (`python tests/test_unit_kernel.py`, girata come script: `tests/conftest.py` la esclude dalla collection di pytest, come fa la CI):

- main `f6396ba` (baseline misurata in un worktree temporaneo su quel commit): **818 PASS, 1 FAIL**
- questo ramo: **830 PASS, 1 FAIL**

Blocco RIEPILOGO reale di questo ramo:

```
=== RIEPILOGO: 830 PASS, 1 FAIL ===
  FAIL: T80u5 anteprima/parser robusti su repr che solleva, ricorsione, repr multiriga; secondo repr sempre (testo del modello tra apici)
```

Blocco RIEPILOGO reale della baseline (main `f6396ba`):

```
=== RIEPILOGO: 818 PASS, 1 FAIL ===
  FAIL: T80u5 anteprima/parser robusti su repr che solleva, ricorsione, repr multiriga; secondo repr sempre (testo del modello tra apici)
```

**FAIL fuori scope:** T80u5, PREESISTENTE. È presente identico su main `f6396ba`: col `.venv` del progetto (Python 3.14.7) un JSON annidato 100k viene parsato invece di sollevare `RecursionError`. La CI pinna Python 3.11 ed è verde. Non toccato, come da brief.

pytest: **1031 passed, 1 skipped** (145 s). Identico alla baseline: la sessione non tocca i file raccolti da pytest.

Mutazioni eseguite e poi ripristinate (`git diff` verificato pulito dopo ognuna), per provare che i test mordono:

- tetto per file → `budget[0]` + salto dei log disattivato (= bug originale): **822 PASS, 7 FAIL** (6 nuovi);
- guard «vince il primo tetto» → assegnazione secca: **3 FAIL** nuovi;
- flag `enum_fermata` mai marcato (= bug R-298-1): **3 FAIL** nuovi;
- `enum_prima` → confronto fra testi (= R-299-1): **nessun FAIL, mutazione SOPRAVVISSUTA** (dichiarata, non coperta).

`python gas.py doctor`: exit 0 (i 5 FAIL sono chiavi API e `.env` assenti nel worktree, attesi; il revisore ha dichiarato di non averlo eseguito perché fa ping di rete reali).

## §6 STATO CI

Output REALE di `gh run list -L 3` alla scrittura dell'handoff (prima del push di questo branch):

```
in_progress		fix/test t80u5 portabile	verifica-bot	fix/test-t80u5-portabile	pull_request_target	38276929440	38s	2026-10-12T16:22:22Z
completed	skipped	fix/test t80u5 portabile	verifica-bot	fix/test-t80u5-portabile	pull_request_target	38276867649	2s	2026-10-12T16:21:51Z
in_progress		docs(fine-task): report, handoff, stato e diff — T80u5 tetto di annid…	CI	fix/test-t80u5-portabile	push	38276828217	1m29s	2026-10-12T16:21:31Z
```

Nessuna di queste run riguarda questa sessione: sono tutte del branch `fix/test-t80u5-portabile`, di un'ALTRA sessione in corso (che sta rendendo portabile proprio il test T80u5 che qui risulta FAIL preesistente).

**Mappatura commit→run di QUESTA sessione:**

- `e606313` chore(revisore): memoria review #297 — **nessuna run su questo SHA** (commit intermedio, mai pushato da solo).
- `be36ce8` chore(revisore): memoria review #298 — **nessuna run su questo SHA** (commit intermedio, mai pushato da solo).
- `08c9af6` chore(revisore): memoria review #299 — **nessuna run su questo SHA** (commit intermedio, mai pushato da solo).
- `d238610` fix(cerca_testo): il budget di byte non mente piu' — **run non ancora disponibile alla scrittura dell'handoff**.
- commit di fine-task (reports), non ancora creato alla scrittura di questa sezione — **run non ancora disponibile alla scrittura dell'handoff**.

GitHub Actions crea una run per *push*, non per commit: il push di questa sessione genererà UNA run che testa solo l'albero del commit di testa. I tre commit di memoria del revisore e `d238610` non sono mai stati testati da soli e vanno considerati non testati individualmente, anche se il loro contenuto è incluso nell'albero testato dalla run di testa. La copertura pre-merge è garantita da `gasmerge` (`gh pr checks --watch`), non da questo campo.

## §7 RISERVE APERTE

- 🟡 **R-297-3** (BASSA, compromesso DICHIARATO) — il salto dei log è incondizionato sulla dimensione: anche un `gas_debug.log` da 50 KB non viene più cercato in una ricerca su cartella. Mitigazioni e prova dell'alternativa in §0 punto 2. Decide l'operatore.
- 🟡 **R-291-1 + bot #188 (2° giro)** (BASSE, PREESISTENTI, non toccate in questa fetta) — buchi residui della denylist credenziali, verificati uno per uno: `token_cache.json`, `kubeconfig`, `mywallet.dat`, `.vault-token`, `.dockercfg`, `_netrc`, `clientsecret.json`, `*.gpg`, `*.asc`. Solo PROPOSTI (§0 punto 3), fetta di sicurezza a sé.
- 🟡 **T80u5** (PREESISTENTE, fuori scope) — FAIL della suite kernel col `.venv` a Python 3.14.7; CI su 3.11 verde.
- ⚠️ **R-299-1** (COSMETICA) — chiusa nel CODICE (`_ferma_enum` registra `enum_prima` al momento della marcatura: via l'ultimo confronto fra testi) ma **NON coperta da test**, e dichiarata tale: la mutazione che rimette il confronto fra testi sopravvive (830/1 invariati). Il solo caso in cui i due differiscono richiede un tempo che scada a METÀ lavoro; prova a mano a 0.03 s su 41 file.
- ℹ️ Riserve CHIUSE in questa sessione: R-282-1 (MEDIA, era solo mitigata in #184), R-283-1, R-297-1 (MEDIA), R-297-2, R-297-4, R-298-1, R-298-2, R-298-3, R-299-2, R-299-3; R-299-1 chiusa nel codice ma non coperta.
- ℹ️ Non verificati, dichiarati dal revisore: comportamento su VPS (costo degli `stat` dell'enumerazione post-tetto misurato solo su APFS locale/tmp; rotazioni reali da 5 MB non ricostruite, il test usa un log sintetico da 4,5 MB in tmp); `gas.py doctor` non eseguito dal revisore.
