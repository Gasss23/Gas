# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-12 — R-gate-worktree-1: il gate di review non è più inerte nei worktree (fetta di SICUREZZA)

---

## §0 DECISIONI UMANE RICHIESTE

1. **C'È UN TERZO AGENTE CHE SCRIVE SUI RAMI DI QUESTO REPO — va verificato dall'operatore.** Sul
   remoto di `feat/cerca-testo-budget-onesto` (PR #193, ramo di un'altra sessione) ci sono quattro
   commit del 2026-10-12 fra 16:45 e 16:52 — `c026bdb`, `2a8524f`, `0b68d2b`, `93b57de` — firmati
   `Co-Authored-By: Claude Opus 5.5` e col trailer `session_01FgYcG4uNEqggobeJsbmE93`, lo stesso id
   che compare nei corpi delle PR #184 e #185 di ieri.
   **Verificato che non vengono da questa sessione né da questo checkout**: `git reflog show HEAD` in
   `/Users/gas/Gas` ha **zero** occorrenze di `cerca-testo-budget` (il ramo non è mai stato estratto
   qui) e quei quattro SHA **non sono nel reflog del ramo locale**, che è condiviso fra i worktree di
   questo repo — quindi non nascono in nessun checkout di questa macchina. I commit di questa
   sessione sono firmati `Claude Opus 5`.
   **Prudenza dovuta**: quell'id corrisponde anche al titolo di questa sessione, quindi potrebbe
   essere la stessa sessione continuata **altrove** (cloud o web) sotto un altro modello. Dall'interno
   non è possibile leggere il proprio id di sessione, e `ListAgents` non elenca altri peer. Solo
   l'operatore può dirlo.
   **Perché conta**: quell'agente e l'altra sessione hanno corretto **lo stesso finding in due modi
   diversi** e nessuna delle due versioni è completa; finché non si sa chi pusha, l'unione può essere
   sovrascritta.
2. **Merge della PR #196** (https://github.com/Gasss23/Gas/pull/196) — numero e URL dall'output reale
   di `gh pr view --json number,url`: `{"number":196,"url":"https://github.com/Gasss23/Gas/pull/196"}`.
   Finché il verdetto del bot non è `APPROVATO` secco senza finding, **decide l'operatore** (regola di
   merge autonomo, CLAUDE.md). Etichetta `verifica` applicata.
3. **ORDINE DI MERGE — misurato, non previsto** (`git merge-tree`, letto sull'**exit code**):

   | merge | esito |
   |---|---|
   | `main` + ciascuno dei tre rami, preso da solo | **exit 0, pulito** |
   | `fix/test-t80u5-portabile` (#195) + `feat/cerca-testo-budget-onesto` (#193) | **exit 1 — 5 conflitti**: `.claude/agents/memoria_revisore.md` più i 4 file di report |
   | `fix/gate-worktree` + `#193` | **exit 1 — 1 conflitto**: `.claude/agents/memoria_revisore.md` |
   | `#195` + `fix/gate-worktree` | **exit 1 — 1 conflitto**: `.claude/agents/memoria_revisore.md` |

   Chi mergia **primo** passa liscio; gli altri due vanno risolti a mano. Raccomandazione: mergiare
   la **#195 per ultima**, perché è quella che conflitta su cinque file.
   **Correzione a una mia affermazione precedente**: avevo detto che il conflitto avrebbe toccato
   `tests/test_unit_kernel.py`. **Falso, misurato**: su quel file il merge riesce da sé.
   **Avvertenza su come si legge questa misura**: `git merge-tree --write-tree` stampa l'OID
   dell'albero **anche quando fallisce**; chi legge la prima riga invece dell'exit code finisce per
   leggere il blob *con i marcatori di conflitto* e li confonde con duplicati silenziosi. È successo
   due volte in questa sessione, una per parte.
4. **Rinumerazione delle review.** Questo ramo parte da `main` (fino a **#298**) e usa **#299/#300**;
   la **PR #195** usa **#299–#301**; l'altra sessione ha già rinumerato le proprie a **#302–#307**.
   Dopo il merge della #195 le righe contatore di **questo** ramo vanno spostate — ho offerto
   all'altra sessione di assorbire io lo spostamento **oltre** le sue, per non farle toccare niente
   due volte. Si spostano **solo** le righe contatore: verdetti, messaggi dei commit e identificativi
   `R-29x-y` restano come emessi, perché già citati in commit pushati.
5. **Secondo passaggio nella chat claude.ai** col link della PR: fetta di sicurezza (istituzione E).
6. **`R-gjq-1`/`R-137-2` meritano una fetta**: il matcher del gate decide se un comando scrive
   usando un `grep` sul suo **testo**, e ha fermato **otto** comandi innocui fra le due sessioni, su
   tre cause diverse (prosa dei report, comandi diagnostici di sola lettura, e la lettura dell'hook
   stesso). **Non** corretti qui, con l'argomento del revisore: è l'unica modifica che può
   trasformare un fastidio **fail-closed** in un **fail-open**, e nello stesso diff che allarga
   l'insieme dei checkout renderebbe impossibile attribuire un buco.

---

## §1 SCOPE & ESITO FETTE

- **Fetta R-gate-worktree-1 — il gate segue il worktree**: `FATTA` (codice e test; il commit attende
  il verdetto del terzo giro). Sviluppata **nel checkout principale e non in un worktree**, di
  proposito: è l'unico posto dove il gate è vivo, e in un worktree i commit di questa fetta
  sarebbero passati senza che l'hook li guardasse — esattamente il difetto da chiudere.
- **Riserve R-299-1..6 (primo giro)**: `CHIUSE`, due delle quali erano falle del meccanismo nuovo
  introdotte da me.
- **Secondo giro: BOCCIATO** — chiudendo R-299-1/R-299-2 avevo aperto un **fail-open nuovo**.
  `RISOLTO` nel terzo giro, vedi §4/§7.
- **`R-gjq-1`/`R-137-2` (matcher)**: `NON FATTA — fuori scope dichiarato`, §0.6.
- **Fail-open preesistenti dell'hook**: `NON FATTE — preesistenti`, dichiarati in §7.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  15 +++++++++++
 .claude/hooks/review_gate.sh       | 405 ++++++++++++++++++++++++++++++++++-----------
 reports/diff_sessione.md           |  70 ++++++++++++++++++------------
 reports/handoff.md                 | 501 +++++++++++++++++++++++++++++++++++-------------------
 reports/stato_progetto.md          |  20 +++++++++++++
 reports/ultimo_report.md           | 231 +++++++++++++++++++++++++++++++---------
 tests/test_unit_hooks.py           | 434 +++++++++++++++++++++++++++++++++++++++++++++
 7 files changed, 1227 insertions(+), 449 deletions(-)
```

`git -c core.quotePath=false diff --cached --stat=400 af394bc`, con i report in stage. Il **set di 7
path** e' esatto. I conteggi di `reports/handoff.md` sono **circolari** per costruzione — il file
conta se stesso e questa stessa frase lo allunga — quindi gli unici dati non circolari del blocco
sono i path e i conteggi dei file diversi da `handoff.md`.

## §3 GIT LOG --ONELINE (sessione)

```
9b836c6 fix(gate): il gate di review segue il worktree, non piu' solo CLAUDE_PROJECT_DIR (R-gate-worktree-1)
7774ec5 chore(revisore): memoria review #304 — APPROVATO
634f126 chore(revisore): memoria review #303 — APPROVATO CON RISERVE
168cf93 chore(revisore): memoria review #302 — APPROVATO CON RISERVE
f6434c0 chore(revisore): memoria review #301 — BOCCIATO
fabec56 chore(revisore): memoria review #300 — BOCCIATO
edcc45b chore(revisore): memoria review #299 — APPROVATO CON RISERVE
```

`git log --oneline af394bc..HEAD`. Le sei righe `chore(revisore)` sono i commit dello script del
revisore, uno per giro, e **sono la traccia verificabile dei sei giri**: i due `BOCCIATO` stanno nel
log, non solo nel racconto. Il commit di fine-task che contiene questo file non compare qui, per
costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit della macchina di controllo: **`9b836c6`** (`.claude/hooks/review_gate.sh` +
`tests/test_unit_hooks.py`). Il motore (`gas.py`, `brains/`, `modules/`) non e' toccato.

**Sei giri** di review: `#299` APPROVATO CON RISERVE, **`#300` e `#301` BOCCIATO** (due fail-open nel
fix stesso, entrambi con la suite verde), `#302` e `#303` APPROVATO CON RISERVE, **`#304` APPROVATO**.
I giri #299-#303 riguardano diff poi superati e le loro citazioni puntano a righe non piu' valide:
la loro sostanza e' in §7, non sono verdetti di gate. Il verdetto di gate, emesso sul diff
effettivamente committato, e' il **#304**, l'unico APPROVATO secco, incollato INTEGRALE:

```
VERDETTO: APPROVATO

Review #304 (riga contatore scritta e committata da se': 7774ec5; i due file del diff restano in
stage, non li ho toccati). Nessuna riserva aperta: R-303-1 e R-303-2 sono chiuse e non ne nascono
di nuove.

Le due conferme che hai chiesto

Codice eseguibile ancora invariato. Togliendo commenti e righe vuote, le versioni di #302, #303 e
questa danno tutte md5 4f5fe2a8e31719a8c97671655645f11d, 188 righe, diff vuoto.
tests/test_unit_hooks.py e' byte-identico al giro precedente. bash -n ok, 138 passed rilanciati da
me (74 s). Il diff rispetto a #303 tocca solo due aree di commento.

Nessuna sesta dichiarazione falsa. Ho verificato le affermazioni nuove una per una, non a lettura:
1. .claude/hooks/review_gate.sh:31 — «in questa fetta CINQUE lo sono state, l'ultima proprio in
   queste righe». Il conteggio torna col mio registro, e includere se' stesso e' corretto:
   (1) #299, la spazzata dichiarata per ogni `cd` non tracciabile, falsa per le forme quotate;
   (2) #299, «ora il gate controlla OGNI checkout candidato» con l'accoppiamento del principale
   ancora aperto; (3) #300, «con percorso relativo fa scattare la spazzata»; (4) #301, «l'apice
   spaiato … si spazza: fail-closed» piu' il limite «con spazi», smentiti dal troncamento;
   (5) #303, «oggi senza test», smentita dal diff che la conteneva. Esito: ok.
2. Stessa riga — «Oggi hanno tutti un lucchetto: `-C` da wt28/wt29, il matcher da wt30». Regge
   all'audit delle due specie che ho fatto in #303 (nessun limite-comportamento scoperto) e le due
   attribuzioni sono provate dalle mutazioni: `-C` ristretto a `git -C` → wt12/wt28/wt29 rossi;
   matcher ancorato a `^git` → wt30 rosso. Esito: ok.
3. .claude/hooks/review_gate.sh:57 — R-300-1 assegnata a entrambe le specie, con la mitigazione
   pinnata da wt8/wt22/wt27. Verificato che sia un pin reale e non un'attribuzione a parole:
   forzando SPAZZA=1 cadeva solo wt8 (misura del primo giro), quindi e' quel test a dimostrare che
   una radice nominata viene risolta; wt22/wt27 estendono alla forma quotata. Esito: ok.
4. tests/test_unit_hooks.py:2759 (wt28) e :2782 (wt30) — i due lucchetti citati dal commento nuovo:
   li ho ri-verificati in questo giro per coerenza con il testo che li nomina, non solo in #303.
   Esito: ok.

Unico neo, estetico e non una riserva: a .claude/hooks/review_gate.sh:57-59 l'inserimento della
classificazione lascia una riga orfana («NON segue il `cd` della»). Se tocchi il file per altro,
riallinea il paragrafo; non vale un giro.

Rischio esplicitamente escluso (cosa NON ho verificato)
(a) Non ho riesaminato da zero la logica dell'hook: mi sono appoggiato alla prova di identita' del
codice eseguibile (md5 senza commenti, identico su tre versioni) e al banco dei giri #299-#302, dove
quella logica e' stata attaccata con ~40 forme su repo reali. Con un md5 diverso avrei rifatto il
banco. (b) La semantica reale del campo `cwd` di Claude Code (se segua la shell persistente del tool
Bash) resta non verificabile da qui: e' il fondamento dichiarato di R-300-1, mitigato per
convenzione e non provato. (c) Linux/CI e Windows non provati in questo giro (macOS, bash 5;
/bin/bash 3.2.57 provato al giro 3). (d) Suite intera e kernel non rilanciati: il diff tocca solo
commenti dell'hook e un file di test gia' verificato; il tuo «1062 passed, 1 skipped» lo riporto
come tua misura, non come mia.
```

**Il neo estetico segnalato NON e' stato corretto**: riallineare la riga orfana a
`.claude/hooks/review_gate.sh:57-59` avrebbe cambiato il diff staged e richiesto un settimo giro di
review per una questione di impaginazione. Dichiarato qui e da chiudere alla prossima fetta che tocca
quel file, come suggerito dal revisore stesso.

### Review #311 (merge di main con la PR #193 nel ramo)

## VERDETTO: APPROVATO CON RISERVE

Il codice è a posto. Va però corretta una risoluzione di un report prima di chiudere il merge (riserva R-311-1).

**Cosa ho controllato nel diff**

- `gas.py:38` — è il codice della PR #193 (soglia `_LOG_MAX_BYTES` e margine `_LOG_SFORO_MAX` usati da `cerca_testo`). Ho controllato se il merge avesse introdotto differenze rispetto a quanto già revisionato e mergiato. Il file staged è identico a `MERGE_HEAD`: `git diff --cached MERGE_HEAD -- gas.py` è vuoto. Esito: ok.
- `gas.py:2162` — è la validazione del testo cercato in `cerca_testo`, con il tetto `_CERCA_MAX_TESTO` definito a `gas.py:1887`. Rischio esaminato: una regressione dovuta all'unione automatica. Il codice coincide con main, quindi niente da segnalare. Esito: ok.
- `tests/test_unit_kernel.py` — è identico a `MERGE_HEAD`. Non ho rieseguito i 843 test del kernel: ho preso il numero che mi hai dato. Esito: ok.
- `.claude/hooks/review_gate.sh:53` e `tests/test_unit_hooks.py:2759` — file della PR #196. Ho controllato che il merge non li avesse toccati: sono identici a HEAD. Ho rilanciato `tests/test_unit_hooks.py` e ho ottenuto 138 passed. Anche `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md` sono identici a HEAD, come dichiarato. Esito: ok.
- `.claude/agents/memoria_revisore.md` — l'unione è esatta. Entrambi i lati aggiungono solo righe in coda, e il file staged è riga per riga: la base comune, poi le 36 righe di main, poi le 15 del ramo. Non restano marcatori di conflitto. Esito: ok.
- `reports/stato_progetto.md` — **riserva R-311-1 (MEDIA, documentale)**. Avevi dichiarato «intestazione di main, sezioni di entrambi». In realtà il file staged è IDENTICO a main: `git diff --cached MERGE_HEAD -- reports/stato_progetto.md` è vuoto. Mancano 23 righe del ramo, cioè l'intera sezione «R-gate-worktree-1 CHIUSA», che contiene:
  - le chiusure R-299-1…6, R-302-x e R-303-x;
  - **R-301-2 (BASSA, ancora aperta)**, che così non sarebbe più registrata da nessuna parte;
  - l'avviso sulla collisione di numerazione;
  - R-282-1/R-283-1 riprodotte;
  - l'indicazione per la fetta R-gjq-1.

  Dopo il merge, la riga 60 di main direbbe ancora «R-gate-worktree-1 (ALTA, NUOVA…) — il gate è INERTE», cioè uno stato falso. **Prima del commit di merge** vanno rimesse le sezioni del ramo, e la voce della riga 60 va segnata come chiusa o tolta. È un file fuori dal perimetro di review, quindi non serve un'altra review: basta correggerlo prima di committare.

**Nota sulla numerazione (BASSA, già nota):** nella memoria ci sono numeri doppi (#297, #301, #302, #303, #304) per la collisione tra sessioni già segnalata. L'ultima riga fisica è #304 del ramo, ma il massimo numerico è #310 (di main). Per questo ho usato **#311**.

**Cosa non ho verificato**

- Non ho rieseguito le suite complete: kernel 843 PASS e pytest 1063 passed restano dati tuoi. Ho rilanciato solo i test degli hook. Il codice motore staged però coincide byte per byte con versioni già revisionate (#306–#310 per main, #299–#304 per il ramo).
- Il comportamento dell'hook con un payload reale di Claude Code in un worktree non è verificato: è un limite già dichiarato della fetta e non si riproduce con i test sintetici.

**Memoria del revisore**

Ho aggiunto la riga contatore `#311 — 2026-10-12 — APPROVATO CON RISERVE — …` e una lezione in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`. La lezione: una risoluzione «entrambe le parti» va verificata con `git diff --cached MERGE_HEAD`/`HEAD`, e dopo un merge il contatore è il massimo numerico, non l'ultima riga.

**Non l'ho committata e non l'ho messa in staging**: oggi il file risulta `MM` (staged più modifica nel working tree). Fai `git add .claude/agents/memoria_revisore.md` prima di concludere il merge.

> Nota dell'agente: R-311-1 corretta prima del commit di merge `024854e` — sezione del ramo ripristinata in `reports/stato_progetto.md` e la vecchia voce R-gate-worktree-1 marcata CHIUSA.

## §5 DELTA TEST DEL MOTORE

Il diff **non tocca il motore** (`gas.py`, `brains/`, `modules/`): tocca la macchina di controllo
(`.claude/hooks/review_gate.sh`) e i suoi test.

| Misura | Prima | Dopo |
|---|---|---|
| `tests/test_unit_hooks.py` | 107 | **138** (31 nella classe `TestReviewGateWorktree`) |
| `pytest -q` (tutto) | 1031 | **1062 passed, 1 skipped** |
| Suite kernel | 821 PASS, 0 FAIL | **invariata per costruzione** (motore non toccato) |

**Prove che i test MORDONO**, non solo che passano:

- contro l'hook di `main` (pre-fix): **8 dei 15** test del primo blocco FALLISCONO, e
  `test_gate_wt1` — la riproduzione — restituisce **`exit 0` dove serve `2`**;
- contro la versione del **primo giro**: FALLISCONO i quattro test del secondo blocco (`wt12`–`wt15`);
- contro la versione **BOCCIATA**: FALLISCONO **7 degli 8** test dei bersagli quotati
  (`wt16`–`wt23`) — tutte e sei le forme della tabella del revisore più l'apice spaiato. L'ottavo
  (`wt22`, la radice propria quotata) passa su entrambe per costruzione e resta come guardia del
  falso positivo;
- contro la versione **bocciata al terzo giro** (normalizzazione cieca degli apici): `wt24` e
  `wt25` — bersaglio quotato **con spazio**, con il troncone che è a sua volta un repo — danno
  **`exit 0` dove serve `2`**, cioè il fail-open riprodotto. `wt26` e `wt27` passano su entrambe e
  restano come guardie (residuo di apice → dubbio; coppia completa → ancora risolvibile);
- mutazione «spazza sempre»: FALLISCE solo `wt8`; mutazione «conteggi ignorati»: FALLISCONO `wt9` e
  `wt10`.

**Nota sul valore di queste prove**: il primo test che avevo scritto per il buco del terzo giro **non
era discriminante** — il worktree si chiamava «con spazio» e il troncone non esisteva, quindi passava
anche con la normalizzazione cieca. È stato rifatto con `<radice> copia`, così il troncone è
esattamente la radice del principale. Un test che non distingue le due versioni non prova nulla.

**FAIL fuori scope**: nessuno.

## §6 STATO CI

`gh run list --branch fix/gate-worktree` al momento della scrittura: **output vuoto**. Il ramo non e'
ancora pushato, quindi non esiste nessuna run su nessuno dei suoi SHA.

**Mappatura commit→run OBBLIGATORIA** (una run per *push*, non per commit):

- `edcc45b`, `fabec56`, `f6434c0`, `168cf93`, `634f126`, `7774ec5` (le sei righe di memoria del
  revisore) e `9b836c6` (il commit della macchina di controllo): **nessuna run su questi SHA alla
  scrittura dell'handoff**. Entreranno tutti nel primo push insieme al commit di fine-task, e la run
  tester-a' **solo l'albero della testa**: `9b836c6` non sara' mai testato da solo, pur essendo il
  suo contenuto incluso nell'albero testato.
- commit di fine-task che contiene questo file: **run non ancora disponibile alla scrittura
  dell'handoff** (il suo hash non e' noto mentre lo scrivo).

Dato di contorno rilevante, e **misurato**: sulla PR #195 il check **required** `verifica-bot` e'
`failure` per un **bug del bot** e non per un difetto di quella PR — `scripts/bot_esito.py` scarta la
gravita' delle riserve registrate **solo se l'id e' numerico**, e `R-gate-worktree-1` non combacia,
quindi la gravita' viene contata come finding nuovo. **Questa fetta corre lo stesso rischio**, perche'
i suoi report citano `R-gate-worktree-1` con la gravita' accanto. Non si aggira riformulando il testo
dei report: sarebbe come ritoccare un verdetto per far passare un gate. Serve la decisione
dell'operatore o una fetta su `scripts/bot_esito.py`.

## §7 RISERVE APERTE

**Chiuse in questa fetta:**

- ✅ **R-299-1** (MEDIA, **fail-open reale introdotto da me**): `-C` matchato solo attaccato a `git`,
  quindi `-C <pulito> -C <sporco>` contava 1/1 → uscita 0, mentre git applica l'**ultimo** `-C`.
  Chiusa: ogni occorrenza è matchata. Test `wt12`, `wt19`.
- ✅ **R-299-2** (MEDIA): un `cd` dentro una stringa non veniva **trovato**. Chiusa: apici nel
  prefisso. Test `wt13`.
- ✅ **R-299-3** (MEDIA): con `cwd` noto il principale **non entra più** nell'insieme, così il lavoro
  in corso di una sessione non blocca le altre. Test `wt14`.
- ✅ **R-299-4** (BASSA): worktree **prunable** non è più un vicolo cieco. Test `wt15`.
- ✅ **R-299-5** (BASSA): `wt7` passava per il motivo **sbagliato**. Ora forza la spazzata.
- ✅ **R-299-6** (COSMETICA, tre punti): `export` inutile, campo per **argv** nei rami python, `$?`
  non atomico.
- ✅ **Il fail-open del secondo giro (BOCCIATO)**: chiuso con la normalizzazione degli apici nello
  stadio di risoluzione, più **otto** test che coprono una per una le forme quotate.
- ✅ **Il fail-open del terzo giro (BOCCIATO)**: il **troncamento sullo spazio** reso valido dalla
  normalizzazione. Chiuso normalizzando **solo una coppia di apici ai bordi** e trattando ogni
  residuo come dubbio, più quattro test (`wt24`–`wt27`).
- 📌 **Ogni riga di «Limiti dichiarati» è un'affermazione da PROVARE**: in tre giri su questo hook
  **tre** limiti dichiarati erano **falsi alla misura** («il relativo fa spazzare», «l'apice spaiato
  fa spazzare», «con spazi resta non risolvibile»).
  **Correzione alla mia stessa affermazione**: avevo scritto «ora ogni limite dichiarato ha un test».
  Più larga della misura — il revisore (#302) ne ha trovati **due senza**, R-302-1 e R-302-2. La
  formulazione vera è: i limiti smentiti alla misura ora hanno un test; due limiti *accettati* no.

**Aperte / da sorvegliare:**

- ⚠️ **R-300-1** (MEDIA, **dichiarata nell'hook, non chiusa**): tutto l'impianto si appoggia a `cwd`,
  e `cwd` **non segue** il `cd` della shell persistente del tool Bash. Se un comando precedente ha
  spostato la shell, la scrittura può avvenire in un checkout diverso da `cwd` e il gate non lo sa.
  Mitigazione per **convenzione verificabile** e non per speranza: ogni comando che scrive **nomina**
  la propria radice (`cd <radice> && …`), forma che il gate risolve e che rende `cwd` irrilevante.
  Il revisore suggerisce di mettere la regola anche in `.claude/commands/fine-task.md`: **non fatto**
  qui per non allargare un diff di sicurezza.
- ⚠️ **Scelta di progetto da sorvegliare**: la chiusura di `R-299-3` **rompe la proprietà di
  sovrainsieme** su cui il revisore si era appoggiato per non bocciare il primo giro. L'argomento è
  che non è perdita di copertura ma correzione del **bersaglio**: il gate deve giudicare il checkout
  dove la scrittura avviene.
- 🟡 **R-301-2** (BASSA): la mitigazione di `R-300-1` — «ogni comando che scrive **nomina** la
  propria radice» — vive **solo in un commento dentro l'hook**, che nessuno legge mentre scrive il
  comando. Registrata in `reports/stato_progetto.md`; portarla in `.claude/commands/fine-task.md` è
  concordato come **fetta separata** (quel file è nel perimetro).
- 🟡 **Costo accettato e dichiarato**: con la regola «coppia ai bordi», anche un apice **in mezzo**
  al percorso (`/a"b/c`), che la shell risolverebbe, fa scattare la spazzata. Direzione sicura: non
  si inseguono euristiche che riaprirebbero un buco.
- ✅ **R-302-1** (BASSA) **CHIUSA, ed è il lucchetto più importante della fetta**: il limite su `-C`
  matchato a ogni occorrenza ora ha due test — `wt28` (`-C HEAD`, opzione vera di git) e `wt29`
  (`grep -C 3`, `-C` che non appartiene a git). **Provato applicando l'ottimizzazione pericolosa**:
  restringendo il match a `git[[:space:]]+-C` diventano rossi **tre** test, `wt28`, `wt29` e
  soprattutto **`wt12`** — il doppio `-C`, cioè il fail-open del primo giro. Quella direzione non si
  può più prendere in silenzio.
- ✅ **R-302-2** (BASSA) **CHIUSA**: `wt30` pinna la **direzione** del falso positivo del matcher
  (non la sua desiderabilità): un comando di **sola lettura** la cui prosa contiene le due parole,
  con il motore in stage senza marcatore, deve dare **2**. Criterio scritto nella docstring per chi
  lavorerà su `R-gjq-1`: se quel test diventa verde con un `exit 0`, il gate ha smesso di
  **controllare**, non di dare fastidio.
- ✅ **R-302-3** (COSMETICA) **CHIUSA** in due punti: aggiunto «o interno» al testo del limite (il
  costo accettato riguarda anche l'apice in mezzo, non solo lo spaiato), e la sezione «Limiti
  dichiarati» distingue ora le **due specie** — limite-COMPORTAMENTO (testabile, *deve* avere un
  test) e limite-NON-PROMESSA (alias, heredoc, `GIT_INDEX_FILE`, eval: dichiarati e non pinnabili).
  Pretendere un test per una non-promessa avrebbe prodotto la quarta dichiarazione falsa della fetta.
- 🟡 **Falsi positivi noti e ACCETTATI**, scritti nei limiti dell'hook: `-C` è matchato a ogni
  occorrenza senza verificare che appartenga a git. Si preferisce una spazzata di troppo a
  un'euristica che riapre un buco.
- 🟡 **`R-gjq-1` / `R-137-2`**: **non** è un finding nuovo e **non** va chiamato
  «R-gate-matcher-1» — era un terzo nome per riserve già registrate. Otto occorrenze misurate.
- 🟡 **Fail-open PREESISTENTI** dell'hook, non introdotti qui e non chiusi: `grep` assente → uscita 0
  (`R-gjq-3`); `INPUT` vuoto → uscita 0; `PERIM_RE` non valida → uscita 0.
- ⚠️ **NON VERIFICATO**: il comportamento con un payload **reale** di Claude Code — i test usano
  payload sintetici, quindi la forma effettiva di `cwd` e il caso di una versione che lo **omette**
  non sono provati (il fix è progettato per entrambi: `cwd` assente → spazzata). Non verificato
  nemmeno su **Linux/CI o WSL**: tutto misurato su macOS con bash 3.2, inclusa la sostituzione di
  pattern `${var//…}` usata per la normalizzazione.
- 🟡 Riserve ereditate ancora aperte: **R-298-2**, **R-298-3** (COSMETICHE, PR #195), **R-277-1**,
  **R-284-2**, **F-ci-una-sola-versione**, **F-token-suffisso**.
