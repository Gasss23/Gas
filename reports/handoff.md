# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-01 — Mani, fetta 34 (R6): browser senza schermo dentro bwrap (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #316 (https://github.com/Gasss23/Gas/pull/316). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5103647985","url":"https://github.com/Gasss23/Gas/pull/316"}`), perché `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve il sì dell'operatore, anche tramite M1.
2. Fetta di SICUREZZA: secondo passaggio indipendente nella chat claude.ai col link della PR.
3. Il browser resta SPENTO (`GAS_WEB_BROWSER` non impostato). Accenderlo sul VPS è una decisione dell'operatore, dopo una prova dal vero (bwrap e AppArmor del VPS, node, Playwright). Sul Mac non si accende comunque: bwrap non c'è.

---

## §1 SCOPE & ESITO FETTE

- **PR #315 (browser senza schermo)**: `FATTA` — mergiata (0f02868) col sì dell'operatore.
- **Punto 4 del piano (bwrap)**: `FATTA` — `modules/web/browser.py`: node e Chromium in `bwrap --unshare-all --cap-drop ALL --die-with-parent --new-session`; sistema in sola lettura; nascoste (tmpfs da 1 MB) /home /root /run /tmp /var /srv /mnt /media /opt e la cartella di Gas anche nel percorso vero; ri-esposti in sola lettura node, NODE_PATH, i pacchetti playwright/playwright-core e Chromium, rifiutati se scoprirebbero Gas o la home; proxy su socket Unix 0600 nella cartella della lettura e ponte 127.0.0.1 → socket dentro il sandbox; senza bwrap funzionante il browser non parte (sul Mac resta spento, come chiesto da M1).
- **V-1 ve/bot #315 (WebSocket nei worker)**: `FATTA` — Worker spenti nelle pagine e nei frame, routeWebSocket obbligatorio; test con wss:// sulla 443 da un worker (nessun tunnel).
- **iframe about:blank (bot su 25ce2ef)**: `FATTA` — non riprodotto; ora un test lo fissa.
- **R-594-2 (processo che cambia gruppo e ambiente)**: `FATTA` — PID namespace, test con un fuggitivo `env -i setsid`.
- **R-595-1 (pulizia dei test)**: `FATTA`. **R-595-2 (doppia uccisione)**: `FATTA`. **R-598-1 (commento del test)**: `FATTA`.
- **ci.yml**: `SALTATA — non serviva`: in CI bwrap è già installato e abilitato prima del passo web.
- **Review #599 (chat Mani)**: APPROVATO CON RISERVE. R-599-1 MEDIA (socket Unix di altri raggiungibili: una sola lettura non ferma connect): `FATTA`; R-599-2 MEDIA (node in ~/bin ri-esponeva la home, Gas compreso): `FATTA`; R-599-3 BASSA (da root il sandbox teneva le capability e poteva smontare): `FATTA`; R-599-4 BASSA («0» di Playwright): `FATTA`.
- **Review #600**: APPROVATO CON RISERVE. R-600-1 (Gas da un collegamento), R-600-2 (cwd della sonda), R-600-3 (tmpfs senza tetto): `FATTA`.
- **Review #601**: APPROVATO CON RISERVE. R-601-1 e R-601-2 BASSE: `DEFERITA — registrate`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   8 ++++++++
 modules/web/browser.py             | 212 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------
 modules/web/proxy.py               |  24 ++++++++++++++++++++----
 reports/diff_sessione.md           |  21 +++++++++------------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   2 +-
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  35 +++++++++++++++--------------------
 tests/test_unit_web_browser.py     | 187 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
 tests/test_unit_web_proxy.py       |  26 ++++++++++++++++++++++++++
```

NB: base = merge-base con origin/main = 0f02868. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
a8d4b52 feat(web): browser senza schermo dentro bwrap (R6, fetta 34, chat Mani)
ea763c8 chore(revisore): memoria review #601 — APPROVATO CON RISERVE
1d5fc27 chore(revisore): memoria review #600 — APPROVATO CON RISERVE
7860381 chore(revisore): memoria review #599 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit a8d4b52 (modules/web/browser.py, modules/web/proxy.py, tests/test_unit_web_browser.py, tests/test_unit_web_proxy.py). Verdetto integrale della review #599 (chat Mani), sulla prima versione:

```
## VERDETTO: APPROVATO CON RISERVE

Review #599 (chat Mani). Fetta 34 (R6, SICUREZZA): bwrap per il browser senza schermo. Ho esaminato il diff staged su base 0f02868, branch claude/peaceful-lovelace-0w2b7q. Ho letto CLAUDE.md (sez. 1, 5, 8, 9, 10), reports/stato_progetto.md (voce fetta 33, riserve R-594-2/R-595-1/R-595-2/R-598-1) e la memoria (lezioni bwrap del 2026-06-14, #593–#598).

**Wall of Shame**: nessuna violazione. Niente slicing della history, niente output di tool simulato. gas.py non è toccato, e nemmeno `_get_window`, il cap di 10 iterazioni e il cap di 8k. I rami d'errore restano fail-safe §9: rifiuto oppure `{"ok": False}` con log, mai un crash.

### Elementi del diff esaminati
- `modules/web/browser.py:195` — `_comando_bwrap`: `--unshare-all`, `--ro-bind / /`, tmpfs su /home /root /run /tmp e sulla cartella di Gas. Rischi esaminati: rete, file, /proc, /dev. Esito **ok** su questi. Dentro c'è solo `lo`; in /proc ci sono 4 PID; /dev è minimale; touch fuori dalla casa fallisce. Mutanti uccisi, uno per uno (1 failed ciascuno): senza `--unshare-all`, senza il tmpfs su `_GAS`.
- `modules/web/browser.py:70` — `_NASCOSTE` = /home /root /run /tmp. Rischio esaminato: socket Unix di altri. Esito **riserva R-599-1 MEDIA**. Un `--ro-bind` non ferma `connect()` su un socket Unix (EROFS vale solo per file, cartelle e link), e lo stesso vale per una FIFO aperta in scrittura. Riprodotto: socket in /var/tmp con permessi 0777, da utente nobody dentro il sandbox → «RAGGIUNTO». Quindi «l'unica uscita del sandbox» (`modules/web/browser.py:15`) è falso. Lo è anche «vede in sola lettura il resto del sistema» (`modules/web/browser.py:34`). Su un VPS i socket fuori da /run esistono, per esempio sotto /var/snap o /var/spool. Correzione provata: aggiungere `--tmpfs` su /var /srv /mnt /media; la suite browser passa (31 passed). Serve anche un test: `find / -type s -o -type p` dentro il sandbox deve restare vuoto.
- `modules/web/browser.py:200` — il prefisso di node è preso due livelli sopra il realpath. Rischio esaminato: node sotto la home (il tuo caso del VPS). Esito **riserva R-599-2 MEDIA**. Con nvm, volta o fnm il prefisso resta dentro la cartella dello strumento: ok. Con node copiato in `~/bin/node` invece il bind diventa `/home/user` e la cartella di Gas torna visibile in sola lettura (riprodotto: `ls` mostra .git, .claude…). Lo stesso vale per PLAYWRIGHT_BROWSERS_PATH e NODE_PATH presi dall'ambiente. Correzione: se un percorso da ri-esporre è uguale o antenato di `_GAS`, della home o di una cartella nascosta, rifiutare (il browser non parte).
- `modules/web/browser.py:195` (stesso comando) — esecuzione da root. Esito **riserva R-599-3 BASSA**. Da root il sandbox tiene tutte le capability (CapEff 000001fffeffffff) e `umount /home/user/Gas` riesce: Gas e /home tornano visibili. Il VPS gira come uid 1000 (stato_progetto.md:793), quindi in produzione oggi non succede. Succede invece nei container di sviluppo e in un eventuale avvio da root. Correzione provata: `--cap-drop ALL` porta CapEff a 0, umount viene rifiutato e la suite browser passa (31 passed).
- `modules/web/browser.py:275` — realpath su PLAYWRIGHT_BROWSERS_PATH. Esito **riserva R-599-4 BASSA**: il valore speciale `0` di Playwright diventa un percorso assoluto e il browser non parte. È fail-closed.
- `modules/web/browser.py:106` e `modules/web/browser.py:128` — Worker spento e routeWebSocket obbligatorio (V-1 ve/bot #315). Esito **ok**. Il mutante senza `'Worker'` fa fallire 1 test; l'iframe about:blank è coperto dal test.
- `modules/web/browser.py:154` — `process.exit(0)`. Rischio esaminato: troncamento di stdout su pipe. Esito **ok**: con una pagina di 60 000 «è» + U+2028 arriva un JSON intero, `troncato` = True.
- `modules/web/browser.py:293` — R-595-2, una sola uccisione: **ok**. `modules/web/browser.py:332`: senza bwrap niente browser, coperto da test: **ok**.
- `modules/web/proxy.py:128` e `modules/web/proxy.py:129` — socket Unix, chmod 0600 dopo bind e listen. Rischio esaminato: corsa sul socket. Esito **ok**. La cartella della lettura è 0700 (mkdtemp) e il connect chiede comunque la scrittura, che con l'umask normale gli altri non hanno. Un processo dello stesso utente arriva comunque al proxy, ma è filtrato e non guadagna nulla. `modules/web/proxy.py:148`: unlink fail-safe; se il sandbox sostituisce il file, si cancella solo il nuovo: ok.
- `tests/test_unit_web_browser.py:333`, `tests/test_unit_web_browser.py:353` e `tests/test_unit_web_browser.py:382` — rete e home, Gas fuori da /home, R-594-2 col PID namespace. `tests/test_unit_web_proxy.py:542`: socket 0600. Esito **ok**. Manca solo il test per R-599-1.

Prove riprodotte: web `tests/test_unit_web_*.py` **739 passed, 2 skipped**. Browser + proxy 103 passed.

Note cosmetiche (non numerate): il docstring dice «Playwright la toglie da root», ma Playwright passa `--no-sandbox` per default anche da non-root (chromiumSandbox=false): da verificare. La sonda non ha `force=True` (lezione 2026-06-14).

**Condizione**: il commit è consentito. Chiudere R-599-1, R-599-2 e R-599-3 in questa stessa PR: le correzioni sono di poche righe e le ho già provate. Se restano aperte, vanno tracciate in reports/stato_progetto.md con «NON accendere GAS_WEB_BROWSER sul VPS» e il docstring (`modules/web/browser.py:15`, `modules/web/browser.py:34`) va corretto.

### Rischi esclusi (non verificati)
- Comportamento sul VPS reale non verificato (Ubuntu, utente non root, node installato non so come). Su Ubuntu 24.04 AppArmor può negare i namespace a bwrap: in quel caso la sonda spegne il browser (fail-closed), ma non l'ho provato.
- Non ho provato un vero exploit di Chromium: l'analisi è strutturale (cosa vede e cosa raggiunge un processo dentro il sandbox).
- Suite kernel e CI non eseguite: gas.py e ci.yml non sono toccati.

Memoria aggiornata: riga #599 più 2 lezioni (ro-bind e socket/FIFO; bwrap da root e `--cap-drop ALL`, prefissi antenati), committata con lo script (7860381). Il diff staged è rimasto intatto.

File rilevanti:
- /home/user/Gas/modules/web/browser.py
- /home/user/Gas/modules/web/proxy.py
- /home/user/Gas/tests/test_unit_web_browser.py
- /home/user/Gas/tests/test_unit_web_proxy.py
- /home/user/Gas/.claude/agents/memoria_revisore.md
- Sonde e plugin dei mutanti (fuori dal repo): /tmp/rev599/
```

Verdetto integrale della review #600 (chat Mani), dopo le correzioni della #599:

```
## VERDETTO: APPROVATO CON RISERVE

Review #600 (chat Mani). È la ri-review della #599 sulla fetta 34 (bwrap per il browser). Diff staged sha256 bb9077f7…, base 0f02868, branch claude/peaceful-lovelace-0w2b7q. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (letto in modo mirato) e la mia memoria.

**Cosa ho controllato nel diff**
- `modules/web/browser.py:77`: `_NASCOSTE` ora contiene 9 cartelle. Rischio esaminato: socket Unix ancora raggiungibili (R-599-1) e Chromium che si rompe senza /var, /run e /opt. Esito ok. Il mutante con solo home, root e tmp fa 1 failed. Dentro il sandbox `fc-match sans` risponde (Inter). /etc/resolv.conf resta leggibile, anche se il DNS non serve perché lo fa il proxy. I tempi di due letture sono uguali (3,2 s) con o senza le cartelle nascoste nuove. /var/cache/fontconfig nascosta non dà problemi visibili.
- `modules/web/browser.py:221`: `_copre` rifiuta un percorso uguale o antenato di una cartella protetta. Rischio esaminato: ri-esporre Gas o la home (R-599-2). Esito ok. «/» viene preso (`"".rstrip+"/"`). Le uscite di `_cartelle_di_playwright` passano dallo stesso controllo (`modules/web/browser.py:237`), quindi anche un «/» restituito da node verrebbe rifiutato. Mutante `if False:` → 2 failed (`tests/test_unit_web_browser.py:370`).
- `modules/web/browser.py:201`: `_cartelle_di_playwright`. Rischio esaminato: che ri-esponga troppo. Su questa macchina ri-espone `/opt/node-tools/node_modules` (due volte, cosa innocua), in sola lettura: tutti i pacchetti globali di quella cartella, non solo playwright. Lo accetto. Ho trovato però una riserva, vedi R-600-2.
- `modules/web/browser.py:230`: `--cap-drop ALL`. Esito ok. `tests/test_unit_web_browser.py:362` controlla che CapEff sia 0.
- `modules/web/browser.py:315`: il valore «0» di PLAYWRIGHT_BROWSERS_PATH non passa più da realpath (R-599-4). Esito ok.
- `modules/web/proxy.py:128`: socket Unix con chmod 0600 subito dopo il bind. La finestra prima del chmod è dentro una cartella 0700 (TemporaryDirectory), e il file viene cancellato in `ferma()`. Esito ok.
- `tests/test_unit_web_browser.py:353`: il test con `find /` di socket e FIFO esclude /proc, /sys, /dev e la casa. Esito ok: prende il mutante.

Prove rifatte: browser 35 passed, web `python -m pytest tests/test_unit_web_*.py` 743 passed, 2 skipped (i numeri dichiarati sono confermati). Dopo ogni mutante il file è stato ripristinato e `git diff` è vuoto.

**Riserve (da tracciare in stato_progetto.md)**
- **R-600-1 BASSA**: il tmpfs che nasconde Gas usa `_GAS` senza risolvere i collegamenti (`modules/web/browser.py:232`, con `modules/web/browser.py:78` che usa abspath). Se Gas si raggiunge da un collegamento e la cartella vera sta fuori dalle nascoste, la cartella vera resta leggibile. Riprodotto: collegamento `/var/tmp/gaslink-prova` → `/usr/local/gasreale-prova`, e dentro il sandbox `cat .env` restituisce «SEGRETO». Lo stesso vale, per ragionamento, per una home fuori da /home e /root: oggi la home viene solo controllata, non nascosta. Correzione: aggiungere `--tmpfs` anche su `realpath(_GAS)` e su `realpath(~)`.
- **R-600-2 BASSA**: `_cartelle_di_playwright` lancia node con la cwd del processo di Gas, mentre dentro il sandbox la cwd è la casa. La cache usa come chiave solo (node, NODE_PATH). Riprodotto: con la cwd su una cartella che contiene `node_modules/playwright` finto, viene ri-esposta `/var/tmp/cwdprova-…/node_modules`, che dentro il sandbox non serve, e playwright-core potrebbe non coincidere. Correzione: `cwd="/"` (o la casa) nella sonda.
- **R-600-3 BASSA**: i tmpfs che nascondono le cartelle sono scrivibili. `touch /var/x /run/x /opt/x /tmp/x` riesce, e ognuno può arrivare a 7,9 GB di RAM. La frase della docstring «scrivibile solo la cartella della lettura» (`modules/web/browser.py:16`) è falsa, e un renderer compromesso può riempire la RAM. Correzione: `--size` piccolo prima di ogni `--tmpfs`, oppure `--remount-ro` dopo i bind (bwrap 0.9.0 ha entrambe le opzioni). Va riprovato che Chromium parta lo stesso: fontconfig da root ha scritto in /var/cache.

**Cosa NON ho verificato**
- Non ho rifatto la prova da utente non root (nobody) per cap-drop, find e uccisione: qui giro da root e non ho preparato un utente con accesso al repo. Mi fido della prova dichiarata.
- Non ho provato il comportamento sul VPS con molti font o con un'altra disposizione di node (nvm in ~/.nvm, pnpm). Lì `_copre` lascia passare i discendenti della home: corretto per ragionamento, ma non provato.
- Non ho misurato un timeout reale della sonda node (10 s dentro i 25 s della lettura). In caso di errore il risultato vuoto resta in cache e il browser resta spento fino al riavvio: fail-closed, lo annoto e basta.

Memoria aggiornata (riga #600 e 2 lezioni) e committata: 1d5fc27. File: /home/user/Gas/.claude/agents/memoria_revisore.md, /home/user/Gas/modules/web/browser.py, /home/user/Gas/modules/web/proxy.py, /home/user/Gas/tests/test_unit_web_browser.py, /home/user/Gas/tests/test_unit_web_proxy.py.
```

Verdetto integrale della review #601 (chat Mani), sul diff finale del commit a8d4b52:

```
## VERDETTO: APPROVATO CON RISERVE

Review **#601** (chat Mani). È la ri-review della #600 sulla fetta 34 (browser dentro bwrap). Diff staged sha256 9c797744, base 0f02868, branch claude/peaceful-lovelace-0w2b7q. Riga della memoria committata in ea763c8. Le altre modifiche staged restano dov'erano.

Letture fatte: CLAUDE.md, reports/stato_progetto.md (per grep, sulle parti che servono) e la memoria del revisore (lezioni della #599 e della #600 applicate).

**Riprodotto da me**
- Test del browser: 37 passed.
- Tutti i test web: 745 passed, 2 skipped.
- Mutante «solo _GAS» (niente percorsi veri): 1 failed. Mutante «tmpfs senza --size»: 1 failed.

**Elementi del diff esaminati**
1. `modules/web/browser.py:240` — nasconde anche il percorso vero di Gas e della home, senza doppioni. Rischi esaminati: ordine dei tmpfs, punti di montaggio da creare dentro il tmpfs da 1 MB, home uguale a «/». Esito: ok. Con HOME=/ il tmpfs copre tutto e il browser semplicemente non parte (fail-safe, nessuna fuga). Il test `tests/test_unit_web_browser.py:369` regge il mutante.
2. `modules/web/browser.py:241` — tetto da 1 MB su ogni tmpfs che nasconde. Rischio esaminato: tmpfs pieni di dati in RAM. Esito: ok. Il test `tests/test_unit_web_browser.py:362` lascia al più 1 MB su 3 MB scritti; il docstring «scrivibile senza tetto solo la cartella della lettura» ora è vero.
3. `modules/web/browser.py:217` — la sonda di Playwright gira con cwd="/". Rischio esaminato: un node_modules finto nella cwd ri-esposto nel sandbox. Esito: ok. Riprodotto: con un falso playwright nella cwd la sonda risponde sempre /opt/node-tools/node_modules. Riserva: nessun test lo tiene (R-601-1).
4. `modules/web/browser.py:236` — /dev/shm da 256 MB. Rischio esaminato: Chromium a corto di memoria condivisa sulle pagine normali. Esito: ok. Misurato DENTRO il sandbox con df ogni 0,1 s su una pagina pesante: 40 canvas FullHD, 20 immagini 2000x2000, 1,2 milioni di caratteri, 60 scroll. Pagina letta tutta, picco di /dev/shm 0 KB. 256 MB bastano con ampio margine. Riserva: nessun test tiene il --size (R-601-1).
5. Resto del diff rispetto alla #600: confrontato browser.py con una copia salvata dall'agente stamattina alle 02:15 (che presumo sia la versione della #600). Le differenze sono solo le tre correzioni R-600, le due costanti e il docstring. Il conteggio torna: 35 test più i 2 nuovi = 37.

**Riserve (entrambe BASSE, da tracciare in stato_progetto.md)**
- **R-601-1**: due mutanti sopravvivono, «senza cwd="/"» e «/dev/shm senza --size» (37 passed su entrambi). Le correzioni ci sono ma nessun test le protegge.
- **R-601-2**: bwrap accetta `--size` solo dalle versioni recenti. Qui c'è 0.9.0; per mia memoria serve almeno la 0.7.0, non verificato. La sonda `modules/web/browser.py:185` (`_bwrap_funziona`) non usa né `--size` né `--cap-drop`. Con un bwrap vecchio sul VPS dice OK e poi ogni lettura fallisce in silenzio: fail-safe, non è una fuga. Basta aggiungere alla sonda le stesse opzioni del comando vero.

**Non verificato**
- Il diff di `modules/web/proxy.py` e `tests/test_unit_web_proxy.py`, e la parte vecchia del test del browser, contro la #600: non c'è una copia della #600 con cui confrontarli. L'agente dice che il delta tocca solo browser.py, e il diff di proxy.py non contiene niente di R-600.
- La versione di bwrap e il comportamento sul VPS: non riproducibili qui.
- La memoria condivisa su pagine reali con video o WebGL: niente rete esterna; misurato solo su pagina locale.

File: /home/user/Gas/modules/web/browser.py, /home/user/Gas/tests/test_unit_web_browser.py, /home/user/Gas/.claude/agents/memoria_revisore.md
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. `tests/test_unit_web_browser.py`: da 25 a 37 test (obbligatori in CI). `tests/test_unit_web_proxy.py`: da 71 a 72. Web con il comando della CI (`python -m pytest tests/test_unit_web_*.py`), con node, playwright e bwrap: 745 passed, 2 skipped. Mutanti presi (1 o 2 failed ciascuno): senza Worker spento, senza `--unshare-all`, Gas visibile fuori da /home, senza PID namespace, senza `process.exit`, sonda sempre vera, senza `--cap-drop`, solo home/root/tmp nascoste, senza controllo degli antenati, senza percorso vero, senza tetto dei tmpfs. Non presi (R-601-1): senza cwd="/" nella sonda di Playwright, /dev/shm senza `--size`.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 7860381, 1d5fc27, ea763c8 (memoria del revisore), a8d4b52 (fetta 34): pushati insieme prima dell'apertura della PR #316; nessuna run su questi SHA (la CI parte sulla PR).
- Il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-601-1 (chat Mani) BASSA: cwd="/" della sonda di Playwright e `--size` di /dev/shm senza un test che li tenga.
- R-601-2 (chat Mani) BASSA: la sonda `_bwrap_funziona` non usa `--size` e `--cap-drop`; con un bwrap vecchio dice OK e ogni lettura fallisce (fail-safe, non una fuga).
- Limiti dichiarati del browser: Chromium senza la sua sandbox; dentro bwrap vede in sola lettura /usr, /etc e il resto non nascosto; il proxy filtra le destinazioni, non i dati; niente regola https→http e pagina riscaricata (R-593-6); X-Gas-Proxy dentro i tunnel https non si toglie (R-593-3); una pagina che usa i Worker può non funzionare; sul Mac il browser resta spento.
- Nota BASSA (review #593): un'intestazione «Nome : valore» fa rifiutare la pagina dal proxy.
- V-1 bot #309 BASSA (limite): verdetto che cita alla lettera un caso di prova di credenziale spezzata non pubblicato.
- R-582-1 BASSA, R-582-2 COSMETICA, R-580-2 BASSA (limiti del bot); V-1/V-2 bot e ve #306.
- R-572-1, R-572-2, R-575-1 BASSE e R-575-2 COSMETICA (chat Mani), preesistenti.
- (b) libexpat ≥ 2.4 nel doctor: con M1.
- V-3 ve #303 BASSA: selectolax 1.0.2 uscita il 2026-10-22, da decidere dall'operatore prima del `pip install` sul VPS.
- R-518-1, R-516-1, R-ve277-5, V-1 ve/bot #288, V-2/V-3 ve #296, R-546-1: BASSE della chat Mani, invariate.
