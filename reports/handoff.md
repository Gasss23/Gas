# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — Cancello: note basse #181 (`--` in run_command, date posizionale, file *.env) — PR #182

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #182 (https://github.com/Gasss23/Gas/pull/182). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"id":"4819906976","url":"https://github.com/Gasss23/Gas/pull/182"}`): `gh` nel container non è autenticato. Fetta di sicurezza sul cancello: il merge lo decide l'operatore.
2. Proposta: sostituire i comandi di sistema di `run_command` con poche funzioni di lettura scritte in Gas (prossima fetta?).
3. Sul Mac: sbloccare `main` dal worktree `.claude/worktrees/gate-ip-ottetti`, poi `git pull`.

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #181**: FATTA su richiesta esplicita dell'operatore («mergia la PR 181 quando è verde»): unit-suite e handoff-check success, verifica-bot neutral (APPROVATO CON RISERVE, solo note BASSE), `mergeable_state: clean`. Merge commit `bc604ae`.
- **Fetta — note basse #181** (V-1/V-2 di verifica-bot #181; V-1/V-2 della verifica esterna #181, commento https://github.com/Gasss23/Gas/pull/181#issuecomment-6110131014): FATTA. Commit `744ed4a`. Review #274 → #275 → #276 APPROVATO CON RISERVE.
- **Fetta — finding bassi di verifica-bot #182 (V-1 test) e verifica esterna #182 (V-1 numeri, V-2 `prod.envbak`; commento https://github.com/Gasss23/Gas/pull/182#issuecomment-6110282507)**: FATTA. Commit `a6502d5`. Review #277 APPROVATO CON RISERVE.
- **R-274-2** (falsi positivi con `--` in grep/diff): DEFERITA, direzione sicura.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 gas.py                             |  25 ++++++++++++++++++++++++-
 modules/gate/gate.py               |  20 +++++++++++++++++++-
 reports/design_cancello.md         |   2 +-
 reports/diff_sessione.md           |  16 ++++++++--------
 reports/handoff.md                 | 363 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   8 +++++++-
 reports/ultimo_report.md           |  24 +++++++++++-------------
 tests/test_unit_gate.py            |  21 +++++++++++++++++++++
 tests/test_unit_kernel.py          |  23 +++++++++++++++++++++++
 10 files changed, 259 insertions(+), 249 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
a6502d5 fix(cancello): finding bassi #182 — copie .env*, test T83m più severo
0254533 chore(revisore): memoria review #277 — APPROVATO CON RISERVE
0e8463e docs(fine-task): report, stato e handoff PR #182 (note basse #181, review #274–#276)
744ed4a fix(cancello): note basse #181 — `--` in run_command, date posizionale, file *.env
53650be chore(revisore): memoria review #276 — APPROVATO CON RISERVE
f39d5f4 chore(revisore): memoria review #275 — APPROVATO CON RISERVE
53707e2 chore(revisore): memoria review #274 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Quattro verdetti, incollati integralmente nell'ordine.

### Review #274

## VERDETTO: APPROVATO CON RISERVE

**Elementi del diff esaminati**

- `gas.py:1607`: in `_vet_letture`, dopo il primo `--` ogni token conta come un file da controllare anche se inizia con '-'. Per grep, il primo token che non è un'opzione resta il pattern. Il rischio era leggere `.env` tramite `cat -- -x` o `grep … -- -x`, con `-x` link simbolico verso `.env`. Ho fatto girare la stessa sonda, solo controllo e nessuna esecuzione, sul codice di HEAD e su quello in staging. Su HEAD passano tutte queste forme, in staging sono tutte negate: `cat -- -x`, `cat -- --y`, `cat -n -- -x`, `head -n 1 -- -x`, `tail -- -x`, `wc -- -x`, `uniq -- -x`, `file -- -x`, `ls -- -x`, `grep -e S -- -x`, `grep --regexp=S -- -x`, `grep -- S -x`, `grep -A 1 S -- -x`. Anche il caso limite `grep -c -- -- -x` è giusto: il secondo `--` è il pattern, come fa getopt, e `-x` viene controllato. `cat -- note.md` resta permesso. Esito: ok.
- `gas.py:1531`: in `_vet_opzioni`, `date` accetta come operando solo `+formato` o il valore di `-d`/`--date`. Il rischio era cambiare l'orologio con un operando posizionale e bloccare per errore usi legittimi. Negati: `date 0101`, `date -d -- 0101` (il `--` viene preso come valore di `-d`, come fa getopt), `date -d tomorrow 0101`, `date -- -x`, `date 0101+`. Permessi: `date +%s`, `date -- +%Y`, `date -u`, `date -I`, `date -R`, `date --rfc-3339=s`, `date --date=tomorrow`, `date -d 1 -d 2`. Falsi positivi, tutti dalla parte sicura: `date -ud tomorrow` e `date --da tomorrow`. `date -` passa, ma è innocuo: GNU date risponde "invalid date" e non imposta nulla. Dopo il blocco si prosegue con `_OPZIONI_FILE_VIETATE`, quindi `-s`/`-f`/`-r` restano negati. Esito: ok.
- `modules/gate/gate.py:251`: `_nome_da_segreto` nega ogni parte del percorso che finisce in `.env`. Funziona anche con maiuscole e caratteri larghi, perché `_normalize_path` applica NFKC e casefold (`a/prod．env` e `modules/.ENV ` negati). La usano `_check_path_arg` (`modules/gate/gate.py:209`) e `lettura_consentita` (`modules/gate/gate.py:264`), quindi vale anche sul percorso risolto in `_vet_letture`. Su HEAD `lettura_consentita('modules/prod.env')` dava True, ora False. I nomi simili restano leggibili (`modules/envoy.py`, `dati/env.txt`, `modules/x.environment.py`). Esito: **riserva**, vedi R-274-1.
- `tests/test_unit_kernel.py:7667`: T83m chiama solo `_vet_command` e non esegue mai `date`. Il link simbolico `-x` è creato in modo condizionato. Ci sono controlli sia sulle forme negate sia su quelle legittime. `tests/test_unit_gate.py:545` copre le forme `*.env` e i nomi simili. Esito: ok.
- Contesto, file non toccato: `modules/gate/gate.py:384`. Il controllo per sottostringa `.env` sull'intero comando già negava `cat modules/prod.env` in run_command, quindi la falla V-2 stava solo in `read_file`. Il fix la chiude.

**Riserve**

- **R-274-1 (BASSA)**: `read_file` legge ancora `modules/prod.env.local`, `modules/prod.env.bak` e `modules/prod.env~`: verificato, `lettura_consentita` → True e gate → SAFE. run_command le nega grazie alla sottostringa (`modules/gate/gate.py:384`). Proposta: per ogni parte del percorso usare la regex `\.env([.~_-]|$)`, oppure "contiene `.env.`" più "finisce in `.env`/`.env~`". Il fix va provato contro `x.environment.py`, che deve restare leggibile.
- **R-274-2 (BASSA, solo falsi positivi)**: l'allowlist delle opzioni di grep/diff in `_vet_opzioni` non tiene conto di `--`. Per questo `diff -- note.md -x` e `grep -- -r file` vengono negati come opzioni non ammesse. Non apre falle, ma rifiuta comandi legittimi.

**Esiti riprodotti**: pytest 955 passed; test del kernel 762 PASS, 0 FAIL; T83m PASS in entrambi i controlli. L'orologio di sistema non è cambiato: secondi prima e dopo le suite coerenti col tempo trascorso.

**Rischi esclusi esplicitamente**

- Non ho eseguito nessun comando `date` con operandi, per scelta: ho provato solo il controllo, come chiede la lezione #272.
- La versione BSD di `date` (Mac) non è verificata: non è disponibile nel container. Il divieto dell'operando posizionale non dipende dalla piattaforma, ma le opzioni BSD (`-j`, `-v`, `-f` con formato) non le ho provate.
- Windows è fuori dal modello di minaccia (`reports/design_cancello.md`).

Memoria aggiornata (#274 più una lezione sulle varianti `.env.local`/`.bak`/`~`) e committata in `53707e2`.

File rilevanti:
- /home/user/Gas/gas.py
- /home/user/Gas/modules/gate/gate.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/tests/test_unit_gate.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #275

## VERDETTO: APPROVATO CON RISERVE

La regex chiude la riserva R-274-1. Resta però leggibile una famiglia di copie con nomi diversi (R-275-1, bassa). Va bene committare, ma conviene tracciarla.

**Elementi del diff esaminati**

- `modules/gate/gate.py:252`: `_SEGRETO_RE = re.compile(r"\.env([.~_-]|$)")` cerca `.env` seguito da fine nome, `.`, `~`, `_` o `-`. L'ho provato con `lettura_consentita`:
  - **Negati come atteso:** `prod.env.local`, `prod.env.bak`, `prod.env~`, `prod.env_old`, `prod.env-vecchio`, `dev.env.example`, `prod.env.`, `prod.env ` (spazio finale), la cartella `x.env/a.py`.
  - **Restano leggibili:** `x.environment.py`, `a.envelope.md`, `envoy.py`, `env.txt`.
  - **Falsi positivi:** `settings.env.py` e `a.env_test.py` vengono negati. Sbagliano dalla parte sicura.
  - **Restano leggibili ma non dovrebbero:** `prod.env copy` (la copia del Finder su Mac), `prod.env(1)` (download doppio dal browser), `prod.env1`, `prod.env#`, `prod.env,bak`. È la riserva R-275-1.
  - Esito: **riserva**.
- `modules/gate/gate.py:260`: `_nome_da_segreto` applica la regex a ogni pezzo del percorso, già normalizzato e minuscolo, dopo aver tolto punti e spazi finali. `re.search` su una stringa non può sollevare eccezioni. Il chiamante `lettura_consentita` (`modules/gate/gate.py:268`) le intercetta comunque e risponde False, quindi una regola che sbaglia nega la lettura invece di permetterla. Esito: ok.
- `tests/test_unit_gate.py:545`: i casi negati e quelli leggibili corrispondono a quello che ho misurato nella sonda. Esito: ok.
- `gas.py:1531` e `gas.py:1607`: invariati dalla review #274 (il diff staged di gas.py è identico). Le prove del verdetto #274 restano valide. Esito: ok.

**Riserve**

- **R-275-1 (BASSA)**: `read_file` legge ancora `modules/prod.env copy`, `modules/prod.env(1)`, `modules/prod.env1`, `modules/prod.env#`, `modules/prod.env,bak`. Con run_command invece sono negate, grazie al controllo sulla sottostringa `.env` (`modules/gate/gate.py:384`). La correzione proposta è un lookahead negativo: `\.env(?![a-z])`. Così è segreto qualunque `.env` non seguito da una lettera, mentre `environment`, `envelope` ed `envoy` restano leggibili.
- **R-274-2 (BASSA, solo falsi positivi)**: resta aperta come dichiarato. In grep/diff, `--` seguito da token che iniziano con `-` viene rifiutato anche quando il comando è legittimo.

**Esiti riprodotti**
- `tests/test_unit_gate.py`: 274 passed.
- Kernel: 762 PASS, 0 FAIL.
- Il 962 passed della suite pytest completa non l'ho rilanciato: ho eseguito solo il file del gate, l'unico cambiato dalla #274 insieme a gate.py.
- L'orologio di sistema non è cambiato.

**Rischi esclusi esplicitamente**
- Nomi con Unicode esotico dopo `.env`, per esempio caratteri che NFKC non riduce e che sembrano un punto: non li ho provati.
- Nessun comando `date` eseguito, come da protocollo.
- La versione BSD dei comandi (Mac) non è verificata, come nella #274.

Memoria aggiornata (#275, più la lezione "lookahead negativo invece di una classe positiva di separatori") e committata in `f39d5f4`.

File rilevanti:
- /home/user/Gas/modules/gate/gate.py
- /home/user/Gas/tests/test_unit_gate.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #276 (commit `744ed4a`)

## VERDETTO: APPROVATO CON RISERVE

La riserva R-275-1 è chiusa e non trovo problemi nuovi. "Con riserve" solo perché resta aperta la R-274-2, a bassa priorità.

**Elementi del diff esaminati**

- **`modules/gate/gate.py:252`, cosa fa:** `_SEGRETO_RE = re.compile(r"\.env(?![a-z])")` segna come segreto ogni `.env` che non sia seguito da una lettera. Il percorso arriva già normalizzato (NFKC, minuscole).
  - Rischio esaminato: copie di segreti ancora leggibili e falsi positivi sui nomi simili.
  - Sonda con `lettura_consentita`, negati: `prod.env copy`, `PROD.ENV COPY`, `prod.env(1)`, `prod.env1`, `prod.env.local`, `prod.env~`.
  - Negati anche `.env` seguito da lettera non ASCII (`prod.envé`, `prod.envı`), da carattere invisibile (`prod.env​`) e la forma a caratteri larghi `prod.ｅｎｖ`. Non sono letture in più, sono sbagli dalla parte sicura.
  - Restano leggibili `x.environment.py`, `a.envelope.md`, `envoy.py`, `env.txt` e `x.envs.py`. `x.envs.py` è accettabile: è un nome diverso.
  - Esito: ok.
- **`modules/gate/gate.py:261`, cosa fa:** applica la regex a ogni pezzo del percorso dopo aver tolto punti e spazi finali. Il docstring è allineato.
  - Rischio esaminato: eccezioni non gestite. `re.search` su `str` non solleva, e `lettura_consentita` in `modules/gate/gate.py:263` intercetta comunque e restituisce False.
  - Esito: ok.
- **`tests/test_unit_gate.py:545`, cosa fa:** i parametri coprono tutte le forme che R-275-1 aveva lasciato fuori, più i nomi simili che devono restare leggibili.
  - Esiti riprodotti: 280 passed. Kernel 762 PASS, 0 FAIL.
  - Esito: ok.
- **`gas.py:1531` e `gas.py:1607`:** non sono cambiati rispetto alla review #274. Le prove fatte lì restano valide.

**Riserve**

- **R-274-2 (BASSA, solo falsi positivi):** resta aperta come tracciata. In grep e diff i token che iniziano con `-` dopo `--` vengono rifiutati anche quando il comando è legittimo. Sbaglia dalla parte sicura.

**Rischi esclusi esplicitamente**

- La suite pytest completa non l'ho rilanciata. Ho eseguito solo `tests/test_unit_gate.py` e la suite del kernel, perché dalla review #275 sono cambiati solo `gate.py` e il suo file di test.
- Non ho eseguito nessun comando `date`.
- Le versioni BSD dei comandi (Mac) non sono verificate.

Memoria aggiornata con la riga #276 e committata in `53650be`.

File rilevanti:
- /home/user/Gas/modules/gate/gate.py
- /home/user/Gas/tests/test_unit_gate.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #277 (finding bassi di verifica-bot e verifica esterna #182, commit `a6502d5`)

## VERDETTO: APPROVATO CON RISERVE

Le due correzioni chiudono i finding segnalati: le copie del `.env` con nomi come `prod.envbak` ora sono illeggibili, e il test T83m fallisce se il link simbolico non si crea. Restano una riserva bassa e due note cosmetiche. Nessuna blocca il commit.

**Elementi del diff esaminati**

- **`modules/gate/gate.py:254` — la nuova regola sui nomi dei segreti.**
  - Cosa fa: `_SEGRETO_RE = re.compile(r"\.env(?!ironment|elope|oy)")` considera segreto `.env` seguito da qualunque cosa, tranne tre parole note: environment, envelope, envoy.
  - Rischi esaminati: copie del segreto ancora leggibili, e nomi innocui bloccati per errore.
  - Prova fatta solo con `lettura_consentita`, senza eseguire nulla:
    - **Negati:** `prod.envbak`, `prod.envi`, `prod.env copy`. Negato anche un carattere invisibile in mezzo (`prod.env​ironment`), perché interrompe la parola esclusa.
    - **Negati per errore, dalla parte sicura:** `x.envs.py` e `os.environ.md` (environ non è nell'elenco delle parole escluse).
    - **Restano leggibili:** `x.environment.py`, `prod.ENVIRONMENT` (il nome viene portato in minuscolo), `a.envelope.md`, `envoy.py`, `env.txt`.
  - Esito: **riserva** (R-277-1).
- **`tests/test_unit_kernel.py:7675` — il test T83m.**
  - Cosa fa: se il link simbolico `-x` non si crea, il test ora fallisce invece di passare provando solo `date`. Ho riprodotto il PASS del prerequisito.
  - Casi aggiunti: `wc -- -x`, `file -- -x`, e `nota2.txt`, un link simbolico verso `modules/prod.env`.
  - `cat nota2.txt` e `grep TOK nota2.txt` sono negati dal controllo sul percorso vero dietro il link: è proprio la nuova regola. Il controllo sulla parola `.env` nel testo del comando non interviene qui, perché `.env` non compare nel comando.
  - Si chiama solo `_vet_command`: nessun comando viene eseguito, `date` compreso.
  - Esito: ok.
- **`tests/test_unit_gate.py:551` — i test del gate.** Aggiunti `prod.envbak`, `prod.envold`, `prod.envcopy` tra i nomi da negare. Riprodotto: 283 passed. Esito: ok.
- **Contesto, file non toccato: `modules/gate/gate.py:384`.** La parola `.env` nel testo del comando continua a negare run_command anche per `prod.environment`.

**Riserve**

- **R-277-1 (BASSA):** l'elenco delle parole escluse funziona come una lista di nomi permessi. Un file di segreti chiamato `prod.environment` o `x.envoy` resta leggibile con `read_file`. Con run_command invece no, grazie al controllo su `.env` nel testo del comando. È il compromesso dichiarato: senza escludere quelle parole, `environment.py` e simili diventerebbero illeggibili.
- **R-277-2 (COSMETICA):**
  - La descrizione di `_nome_da_segreto` in `modules/gate/gate.py:257` dice ancora «NON seguito da una lettera», ma ora la regola è «seguito da qualunque cosa tranne environment, envelope, envoy».
  - In `tests/test_unit_kernel.py:7677` la creazione del link `nota2.txt` non è protetta. Su un filesystem senza link simbolici il blocco T83 si interrompe e finisce nell'`except` di `tests/test_unit_kernel.py:7707`. Il fallimento resta visibile, ma i controlli T83l e T83h successivi non girano più.

**Esiti riprodotti:** gate 283 passed; kernel 763 PASS, 0 FAIL. Non ho rilanciato la suite pytest completa (971): ho eseguito solo il file del gate.

**Rischi esclusi esplicitamente**
- Nessun comando `date` eseguito.
- Le versioni BSD dei comandi (Mac) non sono verificate.
- Non ho controllato i numeri dei test nei report: il coordinatore li corregge nel commit di fine task, fuori da questo diff.

Memoria aggiornata con la riga #277 e committata in `0254533`.

File rilevanti:
- /home/user/Gas/modules/gate/gate.py
- /home/user/Gas/tests/test_unit_gate.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

- Suite kernel: prima (main `bc604ae`) `=== RIEPILOGO: 760 PASS, 0 FAIL ===` → dopo:

```
=== RIEPILOGO: 762 PASS, 0 FAIL ===
```

- pytest: `971 passed in 111.82s` dopo `a6502d5` (prima 947; il «962» scritto in precedenza era stantio: dopo la review #276 erano 968 — V-1 verifica esterna #182). Kernel dopo `a6502d5`: `=== RIEPILOGO: 763 PASS, 0 FAIL ===`. In CI il kernel conta +2 per l'ambiente (es. 764 su `0e8463e`).

Nessun FAIL fuori scope.

## §6 STATO CI

`gh run list -L 3`: CI NON VERIFICATA via `gh` (non autenticato). Strumento GitHub collegato:
- `744ed4a`: run 38148718765 — handoff-check failure (atteso: conteneva l'handoff precedente).
- `0e8463e` (fine-task): run 38148808668 — unit-suite success (kernel «764 PASS, 0 FAIL»), handoff-check success; verifica-bot **neutral** (APPROVATO CON RISERVE, solo finding BASSI).
- `53707e2`, `f39d5f4`, `53650be`: nessuna run su questo SHA (pushati con `744ed4a`).
- `0254533`, `a6502d5` e il commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-274-2** (BASSA, falsi positivi): in grep/diff i token che iniziano con `-` dopo `--` sono rifiutati anche se legittimi.
- **R-277-1** (BASSA): `prod.environment`/`x.envoy` restano leggibili con read_file (compromesso per environment.py); run_command li nega.
- **R-277-2** (COSMETICA): docstring di `_nome_da_segreto` ancora «non seguito da una lettera»; symlink `nota2.txt` nel test non protetto.
- R-273-1/R-273-2 (dalla PR #181): elenco di opzioni vietate per file/wc/date; varianti BSD non provate.
