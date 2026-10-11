# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — Gas legge gas.py, brains/, modules/ (scrittura solo con firma) — PR #181

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #181 (https://github.com/Gasss23/Gas/pull/181). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"id":"4819779241","url":"https://github.com/Gasss23/Gas/pull/181"}`): `gh` nel container non è autenticato. Fetta di sicurezza sul cancello: il merge lo decide l'operatore.
2. Sul Mac: `main` è occupato dal worktree `.claude/worktrees/gate-ip-ottetti` (errore «'main' is already used by worktree»): controllare `git -C .claude/worktrees/gate-ip-ottetti status --short`; se vuoto `git worktree remove .claude/worktrees/gate-ip-ottetti`, poi `git checkout main && git pull`.
3. Livello 3 per il codice consigliato dal secondo passaggio claude.ai su #180: l'operatore ha deciso livello 2 (con firma); cambia solo se lo dice l'operatore.
4. Repo GitHub pubblico: se non voluto, renderlo privato (operatore).

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #180**: FATTA su richiesta esplicita dell'operatore nella sessione («Merja PR 180»), con CI verde sull'head `e627769` (unit-suite success, handoff-check success, verifica-bot neutral) e `mergeable_state: clean`. Merge commit `6e93b10`.
- **Fetta — Gas legge il codice, scrittura solo con firma** (decisione operatore: «Gas può leggere i file ma non toccarli … modificarli solo … con la mia approvazione … deve creare una copia»): FATTA. Commit `2e3e110`. Review #269 APPROVATO CON RISERVE → #270 BOCCIATO → #271 BOCCIATO → #272 BOCCIATO → #273 APPROVATO CON RISERVE.
- **Note basse del secondo passaggio claude.ai su #180**: DEFERITE (una PR per scopo), tracciate in `reports/stato_progetto.md`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   9 ++++++
 gas.py                             | 163 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 modules/gate/gate.py               |  38 ++++++++++++++++++-----
 reports/design_cancello.md         |  18 ++++++-----
 reports/diff_sessione.md           |  28 +++++------------
 reports/handoff.md                 | 589 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |  11 +++++--
 reports/ultimo_report.md           |  31 ++++++++-----------
 tests/test_unit_gate.py            |  42 ++++++++++++++++++--------
 tests/test_unit_kernel.py          | 116 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 10 files changed, 561 insertions(+), 484 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
2e3e110 feat(cancello): Gas legge gas.py, brains/, modules/ (scrittura solo con firma)
8ee8d6a chore(revisore): memoria review #273 — APPROVATO CON RISERVE
95b6b63 chore(revisore): memoria review #272 — BOCCIATO
5dc9779 chore(revisore): memoria review #271 — BOCCIATO
bb981ed chore(revisore): memoria review #270 — BOCCIATO
4f71953 chore(revisore): memoria review #269 — APPROVATO CON RISERVE
bd75789 chore(revisore): memoria review #269 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Cinque verdetti, incollati integralmente nell'ordine. Unica trasformazione: nelle notifiche i caratteri `<`, `>` e `&` arrivano come entità HTML e qui sono riportati come caratteri.

### Review #269

## VERDETTO: APPROVATO CON RISERVE

**In breve.** Questo diff non rende leggibile nessun file del livello 3 (i file che Gas non deve mai toccare: segreti, git, .claude, memoria, venv). Ho confrontato il cancello vecchio con quello nuovo su 25 comandi avversari: nessun diniego è andato perso. Il nuovo controllo di read_file sul percorso risolto funziona, e se lo spengo due test falliscono. Resta però un buco **già presente prima** di questo diff, che ho riprodotto: `run_command` riesce comunque a leggere `.env` per due strade indirette. La documentazione nuova invece dice che non può.

**Elementi del diff esaminati**

- `modules/gate/gate.py:246` — `_LETTURA_NEGATA = _LIVELLO3_PREFISSI`. Rischio: che la lista nuova abbia perso qualche voce oltre a gas.py, brains e modules. Ho confrontato elemento per elemento con `_DENY_PREFIXES` (`modules/gate/gate.py:80`): la differenza è esattamente `gas.py`, `brains`, `modules`. Esito: **ok**.
- `modules/gate/gate.py:370` e `modules/gate/gate.py:376` — controllo dei token e della sottostringa in run_command. Rischio: forme che sfuggono al controllo. Ho caricato il gate vecchio (HEAD) e il nuovo affiancati e provato:
  - flag con `=` e attaccati: `cat --file=.env`, `grep -f.ENV x`;
  - percorsi relativi: `cat ./.env`, `cat a/../.env`, `cat modules/../.env`;
  - caratteri a larghezza piena, normalizzati con NFKC: `．env`, `.ＥＮＶ`, `ｖｅｎｖ/x`;
  - virgolette e maiuscole: `'.e''nv'`, `.GIT/config`, `.Claude/x`, `GATE_CONFIG.yaml`;
  - stato e memoria: `.gas_notte/lock`, `.gas_history.json`.

  Tutti DENY prima e dopo. Cambiano solo le forme che toccano gas.py/brains/modules. Due di queste, `grep -r KEY modules/..` e `diff -r modules .`, ora passano come IRREVERSIBLE (cioè con approvazione umana). Equivalgono però a `grep -r KEY .`, che era già IRREVERSIBLE prima: nessuna capacità nuova. Esito: **ok**.
- `modules/gate/gate.py:249` — `lettura_consentita`. Rischio: eccezioni o input degeneri. Per `None`, stringa vuota, spazi, percorso assoluto e `../x` restituisce False, mai un'eccezione. Esito: **ok**.
- `gas.py:2671` — read_file ricontrolla `lettura_consentita` sul percorso risolto (`_file_rel_root`, `gas.py:1582`). Rischio: un symlink con nome innocuo che porta a `.env`. Ho fatto una mutation: con il controllo spento (`if False and ...`) T83c e T83d falliscono (748 PASS / 2 FAIL) e T83d stampa `SEGRETO=xyz`. Con il controllo attivo l'accesso è negato. Esito: **ok**.
- `gas.py:2698` — il limite di 8000 caratteri (`_cap_tool_output`) vale anche per la lettura del codice. gas.py viene troncato, e il modello può sfogliarlo a pezzi con head/tail/grep -n. Esito: **ok**.
- Finestra contaminata: read_file e run_command sono già tra gli input non fidati (`modules/gate/gate.py:74`). Dopo aver letto il codice, ogni azione UNCERTAIN va all'approvazione. È più attrito, non meno sicurezza. Esito: **ok**.
- `tests/test_unit_kernel.py:7571` — T83 fa un giro completo: legge davvero il codice, la modifica successiva va alla firma e il file resta intatto, `.env` e il symlink sono negati. Esito: **ok**.
- Scrittura: `livello_scrittura` è invariato e il cancello (`modules/gate/`) resta al livello 3. Il livello 2 resta con firma più snapshot preventivo, cioè la «copia» chiesta dall'operatore. Esito: **ok**.

**Riserve (da tracciare in reports/stato_progetto.md)**

- **R-269-1 (MEDIA, preesistente, riprodotta su un kernel reale).** `run_command` legge comunque il livello 3 per due vie indirette:
  1. Symlink: `cat innocuo.txt`, dove `innocuo.txt` punta a `.env`, restituisce `SEGRETO=xyz`.
  2. Ricorsione: `grep -r SEGRETO .` restituisce `./.env:SEGRETO=xyz`.

  Il cancello controlla solo i nomi dei token. `_vet_command` (`gas.py:1441`) controlla solo che il percorso resti dentro la root, e il ricontrollo sul percorso risolto esiste solo per read_file. Entrambi i comandi sono IRREVERSIBLE, quindi serve l'approvazione. Con `GAS_SANDBOX_MODE=os_strict` impostata esplicitamente diventano UNCERTAIN e, a finestra pulita, partono senza approvazione: il contenuto di `.env` finisce al provider LLM.

  Non è una regressione di questo diff, ma `reports/design_cancello.md:352` e il test `tests/test_unit_gate.py:510` affermano «illeggibili anche con run_command». Le soluzioni possibili:
  - correggere la frase del documento;
  - negare `-r`/`-R`/`--recursive` quando un argomento è una cartella antenata del livello 3;
  - risolvere i symlink degli argomenti in `_vet_command` e applicarci `lettura_consentita`.
- **R-269-2 (BASSA).** read_file non controlla `st_nlink`: un hard link già presente verso `.env` si legge. Il modello non può crearlo (né write_file né l'allowlist lo permettono), quindi serve un link preesistente. In scrittura il caso è già chiuso (#266).
- **R-269-3 (BASSA, solo test).** `tests/test_unit_gate.py:526` usa `sed -n 1,50p gas.py`, ma `sed` non è nell'allowlist di esecuzione (`gas.py:1387`). Il test prova solo il gate, non un comando che girerebbe davvero: meglio `head -n 50 gas.py`.
- **Nota, non è una riserva.** Ora anche il codice del cancello (`modules/gate/gate.py`) è leggibile, quindi il modello può studiarne le regole. È coerente con la decisione dell'operatore («modules/» compreso). La difesa resta che le regole siano corrette, non che siano segrete.

**Cosa NON ho verificato e perché**

- Il giro notturno reale (launchd sul Mac, systemd sul VPS) con lettura del codice: non riproducibile qui. Ho controllato solo che non ci siano impostazioni `GAS_SANDBOX_MODE` in `scripts/` e `modules/notte/`.
- Il comportamento su filesystem macOS che non distinguono maiuscole/minuscole: ragionato (la normalizzazione porta tutto in minuscolo), non provato.
- Lo spazio di larghezza zero (`.e​nv`) non è un bypass reale: il file `.env` non ha quel nome.

**Riprodotto**: pytest 947 passed; kernel 750 PASS, 0 FAIL. Memoria aggiornata con la riga #269 più una lezione, committata da sola (4f71953).

File rilevanti:
- /home/user/Gas/modules/gate/gate.py
- /home/user/Gas/gas.py
- /home/user/Gas/tests/test_unit_gate.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/reports/design_cancello.md
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #270

## VERDETTO: BOCCIATO

**In breve.** Il diff dichiara chiusa R-269-1 (lettura del livello 3, cioè segreti, git, .claude e memoria, tramite `run_command`), ma non lo è. La forma più semplice, `grep -r SEGRETO` senza indicare una cartella, legge ancora `.env`. Il motivo: grep, se non riceve un percorso, cerca da sé nella cartella corrente, e il nuovo controllo guarda solo i percorsi scritti nel comando. Anche i file passati come valore di un'opzione (`--from-file=…`, `--file=…`, `-if …`) non vengono controllati. Ho riprodotto tutto su un kernel reale con `.env` e un symlink `innocuo.txt` che punta a `.env`.

**Elementi del diff esaminati**

- `gas.py:1493` — `_vet_letture` salta ogni argomento che inizia con `-` e controlla solo i percorsi indicati. Il rischio era la ricorsione senza percorso: si avvera. Tutti questi comandi passano il controllo e restituiscono il contenuto di `.env`:
  - `grep -r SEGRETO` → `.env:SEGRETO=xyz`
  - `grep -rn SEGRETO` → `.env:1:SEGRETO=xyz`
  - `grep -R xyz` → `.env` e anche `innocuo.txt` (segue il symlink)
  - `grep -d recurse SEGRETO` → `.env:SEGRETO=xyz`
  - `grep --directories=recurse xyz` → `.env:SEGRETO=xyz`

  Il gate li classifica IRREVERSIBLE, quindi serve l'approvazione. Con `GAS_SANDBOX_MODE=os_strict` impostata diventano UNCERTAIN e a finestra pulita partono senza approvazione. Esito: **blocco**.
- `gas.py:1493` (stesso salto delle opzioni) — un file passato come valore attaccato a un'opzione non viene mai controllato:
  - `diff --from-file=innocuo.txt note.md` stampa `< SEGRETO=xyz`;
  - `diff note.md --to-file=innocuo.txt` stampa `> SEGRETO=xyz`;
  - `grep -o --file=innocuo.txt note.md` stampa `SEGRETO=xyz`.

  La chiusura via symlink vale quindi solo quando il file è un argomento separato (`cat innocuo.txt` ora è negato correttamente). Esito: **blocco**.
- `gas.py:1489` — per capire se il primo argomento è il pattern, il controllo riconosce `-e`/`-f` solo all'inizio dell'opzione. Se `f` sta dentro un gruppo di opzioni brevi (`-if innocuo.txt note.md`), il file dei pattern viene scambiato per il pattern e saltato. Così grep usa `.env` come file di pattern e ne conferma il contenuto (stampa `ciao SEGRETO=xyz`). Esito: **blocco** (stessa causa del punto precedente).
- `gas.py:2723` — read_file nega un file con più collegamenti (`st_nlink > 1`), dopo il ricontrollo sul percorso risolto. Esito: **ok**, R-269-2 chiusa per read_file. Per run_command la stessa via resta aperta attraverso i valori delle opzioni.
- `tests/test_unit_gate.py:526` — ora usa `head -n 50`, un comando che è nell'allowlist. Esito: **ok**, R-269-3 chiusa.
- `tests/test_unit_kernel.py:7609` — T83e prova solo forme con una cartella o un symlink come argomento separato. Nessun test copre la ricorsione senza percorso né i file passati come valore di un'opzione. Esito: **riserva** (copertura insufficiente).
- Falsi positivi: `grep -n x modules/a.py`, `grep -c modules modules/a.py` (pattern uguale al nome di una cartella) e `diff modules/a.py note.md` funzionano. `ls -R` mostra solo i nomi dei file, senza contenuti, quindi va bene così. `grep -A 3 SEGRETO .` è negato correttamente (il `3` preso per pattern è innocuo). Esito: **ok**.

**Correzione richiesta (proposta)**

1. Per grep, negare qualunque ricorsione:
   - un gruppo di opzioni brevi che contiene `r` o `R`, per esempio `-rn`, `-iR`. Qualche falso positivo come `-er` è accettabile: in dubbio si nega;
   - le opzioni lunghe `--recursive`, `--dereference-recursive`, `-d`/`--directories` in ogni forma.
2. Per i file passati come valore di un'opzione (`--from-file`, `--to-file`, `-f`/`--file`, `-X`/`--exclude-from`), in forma separata, con `=` o attaccati in un gruppo breve: negarli in blocco, oppure estrarre il valore e passarlo dallo stesso controllo usato per gli argomenti. Negare in blocco è più robusto.
3. Aggiungere a T83e tutte le forme elencate sopra, ciascuna con l'asserzione che `SEGRETO` non compare nell'output.

**Cosa NON ho verificato**

- Non ho rieseguito pytest e la suite del kernel su questa versione (l'agente dichiara 947 passed e 754/0). Il verdetto si basa sulle riproduzioni dirette, che non dipendono dalle suite.
- Le varianti di grep non GNU (BSD grep su macOS, dove giriamo di notte): non ho potuto provarle qui. BSD grep accetta comunque `-r`, e senza percorso legge lo standard input (non la cartella corrente), ma `-R` e `--file=` restano da provare sul Mac.
- I binari dell'allowlist diversi da grep e diff (`comm`, `nl`, `cut`, …) con opzioni che leggono file: non li ho analizzati uno per uno, perché nessuno in GNU coreutils ha un'opzione che apre un file come `--from-file`.

Memoria aggiornata (riga #270 più una lezione) e committata da sola (bb981ed).

File rilevanti:
- /home/user/Gas/gas.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/tests/test_unit_gate.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #271

## VERDETTO: BOCCIATO

**In breve.** La lista delle opzioni ammesse per grep e diff chiude tutte le forme della #270: le ho riprodotte e sono negate. Però l'apertura della lettura introduce una regressione grave, che ho riprodotto. `uniq` è nell'allowlist e il suo secondo argomento è un file in cui scrive. Il gate non nega più i nomi `gas.py` e `modules/`, quindi `uniq note.md modules/gate/gate.py` passa. Senza la sandbox bwrap (modalità di ripiego, il caso del Mac) sovrascrive il codice del cancello (livello 3, «mai, nemmeno con firma») e `gas.py`, senza firma né diff.

**Elementi del diff esaminati**

- `gas.py:1389` (contesto: `SHELL_ALLOWLIST`, non toccata) letta insieme alla nuova `modules/gate/gate.py:376`, che ora nega in run_command solo i nomi del livello 3. Rischio esaminato: binari dell'allowlist che scrivono su un loro argomento. Riprodotto su un kernel reale:

  | Comando | Con bwrap (`os_strict`) | Senza bwrap (`os_with_fallback`) |
  |---|---|---|
  | `uniq note.md modules/gate/gate.py` | `Read-only file system`, file intatto | il file passa da `ORIGINALE` a `ciao` |
  | `uniq note.md gas.py` | `Read-only file system`, file intatto | il file passa da `KERNEL` a `ciao` |

  Il gate classifica il comando IRREVERSIBLE: l'operatore approva un «uniq» che sembra un comando di sola lettura, senza vedere diff né sapere che finisce su un file di livello 2 o 3. Prima di questo diff entrambi i comandi erano DENY, perché il gate negava per nome qualsiasi token `gas.py`/`modules`. Esito: **blocco**.
- `gas.py:1484` (`_OPZIONI_CORTE_OK`/`_OPZIONI_LUNGHE_OK`) e `gas.py:1512` (`_vet_opzioni`). Rischio esaminato: ricorsione e file passati come valore di un'opzione. Riprodotti come negati:
  - ricorsione: `grep -rn x`, `grep -hr x`, e `grep --rec SEGRETO`, cioè `--recursive` abbreviato (getopt accetta le abbreviazioni, ma il confronto esatto sulla lista lo nega);
  - file da opzioni: `--file=`, `-if`, `diff --from-file=`.

  Nelle lettere ammesse nessuna opzione apre file o fa ricorsione: per grep `nciwvFEoHhlLsqxABCme`, per diff `uqiwbBEyatcpU`. Esito: **ok**.
- `gas.py:1540` (`_vet_letture`), riconoscimento del pattern di grep. Rischio esaminato: un file vero scambiato per pattern e quindi non controllato. Con `-e` presente ogni argomento viene controllato come percorso: `grep -e innocuo.txt note.md` viene negato. È un falso positivo che va nella direzione prudente, cioè accettabile. Con `-A 3` il `3` viene preso per pattern e il pattern vero viene controllato in più: anche questo va nella direzione prudente. Esito: **ok**.
- `tests/test_unit_kernel.py:7629` (T83i) e `tests/test_unit_kernel.py:7636` (T83j) coprono le forme della #270 e le opzioni innocue. Nessun test copre i binari che scrivono su un loro argomento, né la modalità senza bwrap. Esito: **riserva**.
- Altri binari dell'allowlist con un symlink verso `.env`: `tail -n 1`, `cat --`, `nl`, `comm`, `file`, `stat -L` sono tutti negati sul percorso risolto. `ls -la` mostra solo metadati. Esito: **ok**.

**Correzione richiesta**

1. `uniq` con al più un argomento non-opzione (anche dopo `--`), oppure toglierlo dall'allowlist.
2. Negare `file -C`: compila e scrive `magic.mgc` nella cartella di lavoro.
3. In generale, prima di togliere un nome dalla denylist dei token, controllare quali binari dell'allowlist hanno un argomento di output. Oggi l'ho trovato solo per `uniq` e `file -C`.
4. Aggiungere un test nella modalità senza bwrap (`os_sandbox_available=False`, `os_with_fallback`) che provi che `gas.py` e `modules/gate/gate.py` restano intatti.

**Falsi positivi dichiarati (non bloccanti)**

`grep -rn TODO modules/` e `diff -r` sono negati: per cercare nel codice il modello deve prima elencare i file con `ls -R`, poi usare grep file per file. Anche `grep -P` e `--include` sono negati. È una perdita di comodità accettabile in una fetta di sicurezza. Un'eventuale ricorsione limitata a `brains/`/`modules/` è una scelta futura.

**Cosa NON ho verificato**

- Non ho rieseguito pytest e la suite del kernel su questa versione (l'agente dichiara 947 passed e 756/0). Il blocco si basa su una riproduzione diretta.
- La sovrascrittura l'ho riprodotta qui, su GNU coreutils in modalità senza bwrap simulata. Non l'ho provata sul Mac vero (BSD `uniq`), dove però, per quanto so, la sintassi `uniq IN OUT` è la stessa.
- `date -s` (cambiare l'ora di sistema, preesistente e fuori dal livello 3): non analizzato.

Memoria aggiornata (riga #271 più una lezione) e committata da sola (5dc9779).

File rilevanti:
- /home/user/Gas/gas.py
- /home/user/Gas/modules/gate/gate.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #272

## VERDETTO: BOCCIATO

**In breve.** La correzione di `uniq` funziona. Restano però aperte tutte le opzioni vietate di `file`, `wc` e `date`: il controllo le confronta per nome esatto, mentre questi comandi accettano anche il nome abbreviato (`--se` vale `--set`, `--compil` vale `--compile`). L'ho riprodotto: senza bwrap passano sia scritture sia letture di `.env`.

**Attenzione, effetto collaterale della mia review.** Durante la prova, `date --se=2020-01-01` ha davvero cambiato l'orologio di sistema del container: senza bwrap il comando gira come root. L'ho rimesso a mano a `2026-10-11 14:23 UTC`, l'ultimo orario osservato. Può esserci uno scarto di qualche decina di secondi. Mentre l'orologio era sbagliato nessun commit è stato creato: le date degli ultimi commit (14:08, 14:13, 14:18) sono coerenti. Ho registrato la lezione in memoria: mai eseguire davvero, in review, comandi che cambiano lo stato globale.

**Elementi del diff esaminati**

- `gas.py:1521`, limite di `uniq` a un solo file. Rischio esaminato: un secondo argomento usato come file di output.
  - `uniq note.md -` è negato;
  - `uniq note.md` e `uniq -c note.md` sono permessi;
  - `uniq --- note.md` passa il controllo ma `uniq` lo rifiuta da sé (opzione non riconosciuta).

  Esito: **ok**.
- `gas.py:1515` (`_OPZIONI_SCRIVONO`) e `gas.py:1509` (`_OPZIONI_FILE_VIETATE`). Rischio esaminato: nomi abbreviati delle opzioni lunghe. Riprodotto senza bwrap:

  | Comando | Effetto |
  |---|---|
  | `file --compil` | crea `magic.mgc` (scrittura) |
  | `date --se=2020-01-01` | cambia l'orologio di sistema |
  | `file --magic=innocuo.txt note.md` | stampa `SEGRETO=xyz` nel messaggio d'errore |
  | `file --files=innocuo.txt` | stampa `SEGRETO=xyz` |
  | `wc --files0=innocuo.txt` | stampa `SEGRETO=xyz` |
  | `date --fil=innocuo.txt` | stampa `SEGRETO=xyz` |

  `innocuo.txt` è un symlink verso `.env`. Il controllo non lo intercetta perché il valore attaccato all'opzione non viene mai risolto. Esito: **blocco**.
- `tests/test_unit_kernel.py:7650` (T83k) prova solo i nomi completi: nessuna forma abbreviata. Esito: **riserva**.
- grep e diff non hanno questo problema, perché lì le opzioni lunghe sono una lista di nomi ammessi con confronto esatto: un nome abbreviato non è in lista e viene negato. Già provato nella #271 con `grep --rec`. Esito: **ok**.

**Correzione richiesta**

1. Anche per `file`, `wc` e `date` usare una lista di opzioni lunghe AMMESSE con confronto esatto, come per grep e diff (la soluzione più robusta). In alternativa, negare un'opzione lunga quando la parte prima di `=` è l'inizio di un nome vietato (per esempio `--se` è l'inizio di `--set`).
2. Aggiungere a T83k le forme abbreviate della tabella. Va provato solo il controllo o la modalità dry-run: un test che esegue davvero `date -s` cambierebbe l'orologio della CI.

**Cosa NON ho verificato**

- Non ho rieseguito pytest e la suite del kernel (l'agente dichiara 947 passed e 758/0). Il blocco si basa su riproduzioni dirette.
- La ricerca di altri binari dell'allowlist che scrivono su un argomento l'ho fatta solo a ragionamento sulle versioni GNU (ls, cat, head, tail, cut, tr, nl, comm, seq, printf, rev, stat: nessuno scrive). Non ho controllato le varianti BSD del Mac.
- `tail -f` (comando che resta appeso fino al timeout di 60 secondi, preesistente) non è un problema di sicurezza e non l'ho tracciato.

Memoria aggiornata (riga #272 più una lezione) e committata da sola (95b6b63).

File rilevanti:
- /home/user/Gas/gas.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #273 (commit `2e3e110`)

## VERDETTO: APPROVATO CON RISERVE

**In breve.** Le opzioni lunghe abbreviate di `file`, `wc` e `date` sono ora negate in ogni forma che ho provato. Le opzioni legittime restano permesse. Ho riprodotto le suite (pytest 947 passed, kernel 760 PASS e 0 FAIL). Il test nuovo cattura davvero il problema: se rimetto il confronto esatto dei nomi, T83l fallisce. Come richiesto, ho provato solo il controllo (`_vet_command`), senza eseguire nessun comando che cambi lo stato globale. L'orologio è rimasto coerente per tutta la review (14:26 e poi 14:28 UTC).

**Elementi del diff esaminati**

- `gas.py:1518` (`_lunga_vietata`) — un'opzione lunga è negata se il suo nome, prima di `=`, è l'inizio di un nome vietato. Rischio esaminato: abbreviazioni minime, nome vuoto, forme separate e gruppi di opzioni brevi.
  - Negate: `file --c`, `--co`, `--m=`, `--ma=`, `--files-f=`, `--compile=`; `wc --f=`, `--files0-fro=`; `date --s 2020`, `--se 2020`, `--r=`, `--re`, `--f`, `--=x`; gruppi brevi `date -us`, `-uf`, `-ur` e `file -bC`, `-Cm`.
  - Prova con mutation: se sostituisco il confronto per prefisso con quello esatto, T83l fallisce (759 PASS / 1 FAIL).

  Esito: **ok**.
- `gas.py:1544` e `gas.py:1551` — lo stesso controllo è usato sia per le opzioni che scrivono sia per quelle che leggono file. Rischio esaminato: falsi positivi su usi legittimi. Restano permessi: `wc --lines`, `date --utc`, `--iso-8601`, `--date=tomorrow`, `--rfc-3339=date`, `--debug`, `-d tomorrow`, `file --brief`, `-L`, `wc -l`, `uniq -c`. L'unico falso positivo trovato è `date --r=…`, ambiguo tra `--reference` e `--rfc-*`: viene negato, ed è la direzione prudente. Esito: **ok**.
- `tests/test_unit_kernel.py:7663` (T83l) — prova le forme abbreviate e quelle permesse solo sul controllo, senza eseguirle. Non tocca l'orologio della CI. Esito: **ok**.
- Per contesto, le correzioni delle review precedenti sono tutte coperte da test che passano (riprodotto con le suite):
  - #269: ricontrollo sul percorso risolto e hard link in read_file (`gas.py:2723`);
  - #270: lista delle opzioni ammesse per grep e diff;
  - #271: `uniq` con un solo file e `file -C` negato.

**Riserve (da tracciare in stato_progetto.md)**

- **R-273-1 (BASSA)**: per `file`, `wc` e `date` resta un elenco di opzioni VIETATE. Se una versione futura aggiunge un'opzione che legge o scrive file, non sarebbe coperta. Per grep e diff, invece, c'è un elenco di opzioni ammesse, più robusto. Si può allineare in una fetta successiva.
- **R-273-2 (BASSA)**: le versioni BSD (Mac) di `file`, `date`, `wc` e `uniq` non le ho provate.

**Cosa NON ho verificato**

- Comportamento sul Mac (BSD): non riproducibile qui.
- I comandi pericolosi (`date --se`, `file --compil`) li ho provati solo col controllo e non li ho eseguiti, per non ripetere il danno all'orologio della #272. Che vengano negati prima di partire basta per la sicurezza.
- Il giro notturno reale: non riproducibile in sviluppo.

Memoria aggiornata (riga #273) e committata da sola (8ee8d6a).

File rilevanti:
- /home/user/Gas/gas.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

- Suite kernel: prima (main `6e93b10`) `=== RIEPILOGO: 746 PASS, 0 FAIL ===` → dopo:

```
=== RIEPILOGO: 760 PASS, 0 FAIL ===
```

- pytest: `947 passed in 108.24s` (prima 947: i test nuovi del gate sostituiscono attese esistenti).

Nessun FAIL fuori scope.

## §6 STATO CI

`gh run list -L 3`: CI NON VERIFICATA via `gh` (nel container `gh` non è autenticato). Strumento GitHub collegato: la PR #181 è appena stata aperta sul push di `2e3e110`; esito non ancora letto alla scrittura.

Mappatura commit→run:
- `2e3e110` (testa del primo push, insieme a `bd75789`, `4f71953`, `bb981ed`, `5dc9779`, `95b6b63`, `8ee8d6a`): run non ancora disponibile alla scrittura dell'handoff; i commit intermedi non hanno una run propria.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-273-1** (BASSA): `file`/`wc`/`date` con elenco di opzioni vietate (grep/diff ad allowlist): allineare.
- **R-273-2** (BASSA): varianti BSD (Mac) non provate.
- Dal secondo passaggio claude.ai su #180 (DEFERITE, una PR per scopo): finta riga `+++ b/altro-file` nel diff della firma; `rendi_visibili` a elenco (U+180B); gate B non vede più una citazione finta attaccata a «vedi:».
- Falsi positivi accettati: `grep -r`, `diff -r`, `grep -P`/`--include`, `uniq -f N`, `date --r=` negati.
