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
- **CI su fc318cf**: unit-suite ROSSA — sul runner (non root) tre test del sandbox fallivano per l'ambiente, non per una fuga: la home del runner contiene Chromium e i moduli di Node (ri-esposti apposta), `find /` sul disco del runner superava i 30 s, da non root non si crea una cartella in /usr/local. `FATTA` in 9b6b83e: test riscritti (segno nella home + mountinfo con lista scritta nel test, /usr fuori dal find, cartella vera in /var/tmp) e un caso vero emerso: una voce nascosta che è un collegamento.
- **Bot su fc318cf (https://github.com/Gasss23/Gas/pull/316#pullrequestreview-5726127323)**: BOCCIATO. V-1 ALTA (unit-suite rossa, i test di isolamento non provavano nulla in CI): `FATTA` in 9b6b83e. V-2 MEDIA (report «745 passed» contro la CI rossa): `FATTA` — questo handoff dichiara la CI rossa su fc318cf.
- **Review #602 (chat Mani)**: BOCCIATO. ALTA: saltare i collegamenti riapriva R-600-1 per le voci di `_NASCOSTE` (es. /home → /data/home): `FATTA` — si nasconde il percorso vero di ogni voce, test con una voce collegamento. MEDIA: test della home indebolito: `FATTA` — mountinfo con lista scritta nel test. MEDIA: `_di_un_altro_pytest` non si fermava al proprio pid: `FATTA`.
- **Review #603**: APPROVATO CON RISERVE. R-603-1/2/3 BASSE: `DEFERITA — registrate`.
- **Bot su e3a59ee (https://github.com/Gasss23/Gas/pull/316#pullrequestreview-5726200713)**: APPROVATO CON RISERVE, check success, CI verde. V-1 BASSA (i discendenti della home sono ri-esposti per intero, es. node in ~/.local/bin ri-espone ~/.local): `DEFERITA — prossima fetta`. V-2 COSMETICA (frase sui Worker invertita): `FATTA` in 366a0d5. V-3 COSMETICA (descrizione della PR): `FATTA` — descrizione aggiornata.
- **Verifica esterna su fc318cf (https://github.com/Gasss23/Gas/pull/316#issuecomment-6552825234)**: BOCCIATO. V-1 ALTA (CI rossa) e V-2 MEDIA (report contro la CI): `FATTA` in 9b6b83e (CI verde su e3a59ee). V-3 MEDIA (mutanti del sandbox senza test: ri-esposte scrivibili, IPC, /proc, --die-with-parent, SPEGNI ridotto): `FATTA` in 366a0d5 — test nuovi, mutanti presi; `--new-session` senza test (serve un TTY): `SALTATA — dichiarata`. V-4 BASSA (scrittura senza tetto sul disco): `FATTA` in 366a0d5 — casa in sola lettura, profilo in un tmpfs da 256 MB. V-5 BASSA (processi di un altro pytest): `FATTA` in 9b6b83e. V-6 BASSA (/etc e /usr leggibili): `DEFERITA — limite dichiarato`. V-7 COSMETICA (R-601-1/2 confermate): `DEFERITA`.
- **Bot su 30cd0a8 (https://github.com/Gasss23/Gas/pull/316#pullrequestreview-5726280373)**: APPROVATO CON RISERVE, check success, CI verde. V-1 BASSA (descrizione della PR non allineata): `FATTA` — riscritta. V-2 BASSA (cartelle fuori dall'elenco delle nascoste leggibili, es. /data): `DEFERITA — fetta «tmpfs su / con elenco di cartelle permesse»`, condizione per accendere il browser scritta in reports/roadmap.md (M1).
- **Verifica esterna su 30cd0a8 (https://github.com/Gasss23/Gas/pull/316#issuecomment-6553120584)**: APPROVATO CON RISERVE, test riprodotti anche da nobody. V-1 MEDIA (comportamenti senza test): a) home fuori dalle nascoste e b) tetto del profilo `FATTA` (test nuovi, review #606); c) serviceWorkers 'block' e d) routeWebSocket → connectToServer `SALTATA — dichiarati in §7` (il netns e il proxy fermano comunque il traffico); XDG_* sulla casa `SALTATA — dichiarato`. V-2 BASSA (descrizione al commit pinnato): `FATTA` — riscritta dopo. V-3 BASSA e V-4 COSMETICA: già registrate (riserve #604, R-605-1). Nota: la verifica ha lasciato due cartelle di prova fuori dalla scratchpad (/home/runnerx, /data/gashome) nel container di sviluppo; la rimozione l'ha bloccata un controllo di sicurezza.
- **R-605-2**: `FATTA` (ProcessLookupError nel finally del test).
- **Review #604 (chat Mani)**: BOCCIATO. Il test di --die-with-parent uccideva il bwrap esterno prima che partisse il figlio (corsa): `FATTA` — si aspetta il vero «sleep»; docstring corretto. **Review #605**: APPROVATO CON RISERVE. R-605-1 COSMETICA e R-605-2 BASSA: `DEFERITA — registrate`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  18 ++++++++++++++++++
 modules/web/browser.py             | 225 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------
 modules/web/proxy.py               |  24 ++++++++++++++++++++----
 reports/diff_sessione.md           |  21 +++++++++------------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   2 +-
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  41 +++++++++++++++++++++--------------------
 tests/test_unit_web_browser.py     | 333 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------
 tests/test_unit_web_proxy.py       |  26 ++++++++++++++++++++++++++
```

NB: base = merge-base con origin/main = 0f02868. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
636b5cb test(web): home fuori dalle nascoste e tetto del profilo tenuti da test (V-1 ve #316 su 30cd0a8, review #606)
175c0ba chore(revisore): memoria review #606 — APPROVATO
30cd0a8 docs(fine-task): handoff con il verdetto #604 riemesso per il gate B
77bdc2a docs(fine-task): fetta 34, PR #316, V-3/V-4 della verifica esterna, review #604/#605
366a0d5 fix(web): profilo del browser in un tmpfs con tetto, casa in sola lettura, test dei mutanti del sandbox (V-3/V-4 ve #316, review #604/#605)
a3cd94b chore(revisore): memoria review #605 — APPROVATO CON RISERVE
a6d5288 chore(revisore): memoria review #604 — BOCCIATO
e3a59ee docs(fine-task): fetta 34, PR #316, CI rossa corretta, review #602/#603
9b6b83e fix(web): test del sandbox validi anche sul runner non root, percorso vero di ogni cartella nascosta (CI #316, review #602/#603)
fee8985 chore(revisore): memoria review #603 — APPROVATO CON RISERVE
5d7a8c1 chore(revisore): memoria review #602 — BOCCIATO
fc318cf docs(fine-task): fetta 34 browser dentro bwrap, PR #316, review #599-#601
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

Commit 9b6b83e (modules/web/browser.py, tests/test_unit_web_browser.py: CI rossa su fc318cf). Verdetto integrale della review #602 (chat Mani), sulla prima correzione:

```
## VERDETTO: BOCCIATO

Review #602 (chat Mani). Oggetto: la correzione della CI rossa sulla PR #316, cioè il diff staged sopra fc318cf, che tocca modules/web/browser.py e tests/test_unit_web_browser.py.

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9, 10), la voce «fetta 34» di reports/stato_progetto.md e la memoria del revisore (lezioni R-600-1: un percorso da nascondere si risolve con realpath). Nel diff non ci sono antipattern del Wall of Shame (nessuno slicing della history, nessun output di tool simulato). Il kernel non è toccato.

**Motivi bloccanti**

- modules/web/browser.py:242 — Il codice salta le voci da nascondere che sono collegamenti (`os.path.islink`). Il rischio è che un caso prima chiuso diventi una fuga. **Esito: blocco (ALTA, fetta di sicurezza).** Lo skip va bene per `_GAS` e per la home, di cui si aggiunge anche il percorso vero. Ma la stessa riga filtra anche le voci di `_NASCOSTE`, e lì il percorso vero NON viene aggiunto: oggi solo la riga modules/web/browser.py:248, che costruisce `protetti`, applica realpath alle voci di `_NASCOSTE`. Se una voce di `_NASCOSTE` è un collegamento (caso realistico sul VPS: `/home → /data/home` su un volume aggiunto), a HEAD bwrap falliva e il browser restava spento. Col diff la voce viene saltata e la cartella vera diventa leggibile. Riprodotto da root (con `_NASCOSTE` modificato a mano, `/var` tolto e un collegamento sotto /var/tmp verso una cartella in /usr/local): HEAD dà `rc 1 … Can't mount tmpfs on /newroot/var/tmp/rev602-home`, il diff dà `rc 0 out ['SEGRETO-ALTRO', 'FINE']`. È una variante di R-600-1 riaperta. Correzione provata su una copia: `for nascosta in dict.fromkeys(os.path.realpath(n) for n in nascoste):`. Così il caso del collegamento resta nascosto (`out ['FINE']`) e i 7 test di isolamento passano. Serve un test con una voce di `_NASCOSTE` che sia un collegamento.

- tests/test_unit_web_browser.py:355 (dentro tests/test_unit_web_browser.py:352) — Il test ora controlla un solo file segno nella home dell'utente al posto di `find /home` e `find /root`. Il rischio è che il test sia più debole del necessario. **Esito: riserva MEDIA** (rientra nel bocciato perché la stessa fetta va comunque rifatta). Il mutante che toglie `"/home"` e `"/root"` da `_NASCOSTE` sopravvive al test nuovo: 7 passed sui test di isolamento. Il test di HEAD lo prendeva (1 failed: in /home ci sono anche claude e ubuntu). Le home degli altri utenti e /root, quando non si è root, non le controlla più nessuno. Proposta che non dipende dal contenuto della home del runner: dentro il sandbox leggere `/proc/self/mountinfo` e pretendere `tmpfs` su ogni voce di `_NASCOSTE` (risolta con realpath) e su `_GAS`. L'ho provato qui e dà tmpfs su tutte e 10. Questo controllo va aggiunto al file segno, non al suo posto.

- tests/test_unit_web_browser.py:203 (dentro tests/test_unit_web_browser.py:194) — `_di_un_altro_pytest` risale i genitori e, arrivato al proprio pid, invece di fermarsi prosegue. Il rischio è che il controllo sugli orfani dei test smetta di contare qualcosa. **Esito: riserva MEDIA.** Se pytest parte da una shell che ha «pytest» nel cmdline, tutti i browser della suite vengono scartati come «di un altro pytest». È il caso del Bash di Claude Code (`bash -c '… python -m pytest …'`), di `timeout 600 python -m pytest` e quindi anche delle verifiche esterne. A quel punto gli `assert _processi_del_browser() == []` (righe 223, 294, 303) non controllano niente. Sonda con un `sleep` figlio della suite e col segno: lanciata da `bash -c` dà 1 failed (processo nostro non contato), lanciata da uno script dà 1 passed. In CI non succede, perché il passo `run:` gira da un file temporaneo. Ma le prove locali dichiarate («browser 37 passed») avevano questa guardia vuota. Correzione: `if pid == os.getpid(): return False` prima del controllo sul cmdline.

**Note non bloccanti**

- tests/test_unit_web_browser.py:382 — Saltare /usr nel `find` dei socket. Rischio: un socket o una FIFO sotto /usr resterebbe invisibile al test. **Esito: ok, nota BASSA.** Qui `find /usr -type s -o -type p` trova zero voci; /run, /tmp, /var e la home restano coperti dal test. La scelta è da dichiarare come limite nel report.
- tests/test_unit_web_browser.py:397 — Il test toglie `/var` dalle nascoste con monkeypatch per stare in /var/tmp senza essere root. **Esito: ok.** Il monkeypatch ha effetto solo in questo test e il caso reale emerso è giusto. Ma proprio questo test ha portato al filtro sui collegamenti, che va cambiato come detto sopra.

**Prove fatte**: la suite del browser da script (senza la guardia vuota) dà 37 passed. Ho provato 3 mutanti su una copia del repo (l'uccisione dei processi ridotta, `_NASCOSTE` senza /home e /root, lo skip dei collegamenti contro realpath) e la sonda dei processi. Lo staging non è stato toccato.

**Rischio escluso**: non ho rifatto la prova da utente non root (nobody) né le prove sul runner GitHub, perché non avevo tempo e la CI non è riproducibile qui. Il fallimento della #316 in CI e l'esito «browser 37 passed da nobody» li prendo dal mandato senza averli verificati. Non ho verificato nemmeno la versione di bwrap sul VPS (R-601-2 resta aperta).

**Cosa serve per approvare**:
1. In modules/web/browser.py:242, realpath su ogni voce al posto dello skip dei collegamenti, con un test su una voce di `_NASCOSTE` che sia un collegamento.
2. Il controllo su mountinfo nel test della home.
3. Lo stop al proprio pid in `_di_un_altro_pytest`.

Riga contatore #602 aggiunta a /home/user/Gas/.claude/agents/memoria_revisore.md insieme a 3 lezioni, e committata (5d7a8c1).
```

Verdetto integrale della review #603 (chat Mani), sul diff finale del commit 9b6b83e:

```
## VERDETTO: APPROVATO CON RISERVE

Review #603 (chat Mani). Ri-review della #602 (che era BOCCIATO), PR #316, fetta 34. Diff staged sopra fc318cf. I tre punti bloccanti o di peso MEDIA della #602 sono chiusi e li ho provati da me.

Elementi del diff esaminati:
- `modules/web/browser.py:242`: ora nasconde il percorso vero (realpath) di ogni voce, senza doppioni, invece di saltare i collegamenti. Rischio esaminato: la fuga della #602 e l'ordine dei montaggi annidati. Mutante che salta i collegamenti: 1 failed. Codice a HEAD contro i test nuovi: 2 failed, perché bwrap rifiuta il collegamento (fail-closed, cioè si blocca invece di lasciar passare). Ho provato anche una voce annidata: `/var` nascosta prima e poi un collegamento verso `/var/tmp/…`. Risultato: rc 0, chiave non letta. Esito: ok.
- `tests/test_unit_web_browser.py:401`: nuovo test con una voce di `_NASCOSTE` che è un collegamento verso `/var/tmp/gas-veroh-…` (con `/var` tolto). Rischio esaminato: un test che passerebbe anche col mutante. Esito: ok, perché fallisce col mutante e anche a HEAD.
- `tests/test_unit_web_browser.py:374`: il test controlla in `/proc/self/mountinfo` che ci sia un tmpfs su una lista scritta nel test stesso, oltre al file segno nella home. Rischio esaminato: una lista presa dal codice, che un mutante accorcerebbe. Mutante senza `/home` e `/root` in `_NASCOSTE`: 1 failed. Esito: ok, con una riserva (R1).
- `tests/test_unit_web_browser.py:198`: `_di_un_altro_pytest` si ferma quando arriva al proprio pid. Sonda lanciata da `bash -c '…; echo pytest'`: False. Lo stesso col mutante senza lo stop: True. Esito: ok, con una riserva (R2).
- Contesto, `modules/web/browser.py:248`: la guardia `protetti`/`_copre` impedisce di rendere di nuovo visibili Gas, la home e le cartelle nascoste. Esito: ok, è lei a coprire R1.

Wall of Shame: nessun taglio della cronologia, nessun output dei tool simulato. Provider e guardrail non toccati. Suite del browser: 38 passed (lanciata da me, come root).

Riserve, tutte BASSE (da tracciare in `stato_progetto.md`):
- R-603-1: il controllo su mountinfo prova che il tmpfs c'è, non che sia il montaggio in cima. Un bind successivo sullo stesso percorso lo coprirebbe e il test passerebbe lo stesso. Oggi lo coprono la guardia `_copre` e il file segno, ma solo per la home: per `/home` di altri utenti non c'è più un controllo sul contenuto.
- R-603-2: `_di_un_altro_pytest` cerca "pytest" come pezzo di testo nel cmdline dei processi intermedi (bwrap, sh). Se `TMPDIR` sta sotto `/tmp/pytest-of-…`, il cmdline di bwrap contiene "pytest" e il rilevatore ignora i browser della propria suite. Basterebbe confrontare argv[0] o il modulo invece del testo libero.
- R-603-3: `/usr` è stato tolto dal `find` dei socket e delle FIFO (`tests/test_unit_web_browser.py:389`): lì la copertura si perde. È accettabile, perché `/usr` è montato in sola lettura dal sistema e non ci dovrebbero stare socket.

Cosa NON ho verificato:
- La corsa da utente nobody (38 passed) e la suite web completa (746 passed): le ho prese dalla tua dichiarazione, non le ho rilanciate.
- Il comportamento sul VPS con un `/home` che è davvero un collegamento: non è riproducibile qui, l'ho solo simulato con un collegamento sotto `/var/tmp`.
- La CI di GitHub su PR #316: non l'ho controllata.

Memoria: aggiunte la riga #603 e una lezione su mountinfo in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate in fee8985. Il diff staged è intatto e il working tree è tornato com'era dopo i mutanti.
```

Commit 366a0d5 (modules/web/browser.py, tests/test_unit_web_browser.py: V-3/V-4 della verifica esterna). Verdetto integrale della review #604 (chat Mani), sulla prima versione — RIEMESSO dal revisore per il gate B (l'originale citava modules/web/browser.py alla riga 416, oltre la fine del file a HEAD; esito e contenuto invariati, cambiano solo i numeri di riga; l'originale è nel transcript della review):

```
Riemesso per il gate B: citazioni allineate a HEAD 366a0d5, esito e contenuto invariati.
(HEAD oggi è 77bdc2a, un commit di soli report sopra 366a0d5. Tra i due commit modules/web/browser.py e tests/test_unit_web_browser.py sono identici, quindi i numeri di riga valgono su entrambi. Non ho toccato né il repo né la memoria.)

## VERDETTO: BOCCIATO

Review #604 (chat Mani). È il delta sulla PR #316 (fetta 34, browser dentro bwrap), cioè il diff che allora era staged sopra e3a59ee: modules/web/browser.py e tests/test_unit_web_browser.py. Prima ho letto CLAUDE.md (sez. 5, 8, 9), reports/stato_progetto.md e la memoria del revisore. La riga #604 è committata con lo script, commit a6d5288.

Questa riemissione cambia solo i numeri di riga. I punti 3 e 8 descrivono il codice com'era al momento della review. Dopo, la correzione in 366a0d5 ha cambiato quelle righe (docstring corretta, attesa con `_sleep_vivi`). L'esito di questa review non cambia.

**Motivo bloccante, uno solo.** `test_morto_bwrap_muore_il_sandbox` non è deterministico. Fallisce sul codice giusto e qualche volta lascia passare il mutante.
- Causa: l'attesa «il figlio è partito» cercava `\0sleep\x0033.271\0` nel cmdline. Lo trovava subito nel processo bwrap ESTERNO, perché nel suo cmdline c'è già `-- sleep 33.271`. La sonda lo conferma: al primo riscontro c'era un solo pid, con comm `bwrap`, ed era proprio `proc.pid`. Così il SIGKILL arrivava prima che il bwrap interno avesse messo il segnale di morte col padre (PDEATHSIG). Il bwrap interno e `sleep` sopravvivevano.
- Prova sul codice giusto: il test da solo (`-k morto`, da root) dava 5 failed su 5, con `assert [21688, 21689] == []`. Nel file intero passava (41 passed): dipendeva dai tempi.
- Prova sul mutante senza `--die-with-parent`: il test passava 1 volta su 15. Quindi il «mutante preso» di V-3 per `--die-with-parent` era fortuna, non una prova.
- Correzione provata, da rimettere al revisore: prima del kill aspettare un pid dei `_pid_con(...)` con `/proc/<pid>/comm == "sleep"`. Risultato: codice giusto 8 pass su 8, mutante 8 fail su 8.

Elementi del diff esaminati:
1. modules/web/browser.py:264-266 — la casa è montata `--ro-bind` e il profilo è un tmpfs `--size MEMORIA_PROFILO` (256 MB), con la chdir dentro. Il punto di montaggio lo crea `os.makedirs` sull'host. Rischi esaminati:
   - Il socket del proxy dentro una casa in sola lettura: connect funziona, perché il kernel non applica la sola lettura del montaggio ai socket. Lo confermano i test che passano.
   - Il punto di montaggio deve esistere prima di bwrap: lo crea `os.makedirs`.
   - `os.makedirs` che fallisce: lo prende l'`except Exception` di leggi_con_browser (modules/web/browser.py:410), quindi nessun crash (§9).
   - L'ordine dei montaggi è come prima: l'ex `--bind` era nella stessa posizione.
   - Il disco dell'host non si riempie più. Al suo posto si usa al massimo 256 MB di RAM in più, sopra i 256 di /dev/shm: compromesso accettabile.
   — ok.
2. modules/web/browser.py:337-338 — HOME, TMPDIR, XDG_CONFIG_HOME e XDG_CACHE_HOME puntano al profilo. Il segno resta sulla casa. Rischio esaminato: Playwright o Chromium che scrivono fuori dal profilo. Il programma figlio è passato inline con `-e`, quindi non c'è nessun file nella casa — ok.
3. modules/web/browser.py:236-238 — la docstring di `_comando_bwrap` diceva ancora «e scrivibile la cartella della lettura», che dopo V-4 è falso — riserva COSMETICA.
4. tests/test_unit_web_browser.py:370-376 — controlla SCRIVE-CASA e che `os.listdir(casa) == ["profilo"]` con il profilo vuoto. Rischio esaminato: un mutante con la casa scrivibile. Il controllo è strutturale e sul contenuto — ok.
5. tests/test_unit_web_browser.py:251 — il titolo è confrontato riga per riga in modo esatto, e i 5 nomi nuovi si trovano in SPEGNI (modules/web/browser.py:120-121). Rischio esaminato: un marcatore aggiunto che passa come sottostringa. Ora fa fallire il test — ok.
6. tests/test_unit_web_browser.py:482 — sola lettura delle cartelle ri-esposte (prefisso di node e la sua bin). Il test è valido solo se l'utente che lo lancia può scrivere in quelle cartelle sull'host. Da utente nobody o su un runner senza permessi il `touch` fallisce comunque, quindi il test passa a vuoto. Il nome dice «e la casa», ma la casa la controlla il test di tests/test_unit_web_browser.py:370 — riserva BASSA.
7. tests/test_unit_web_browser.py:494-498 — IPC namespace e `/proc` con meno di 10 processi. Rischio esaminato: `test -e /proc/<pid di pytest>` dentro un PID namespace nuovo. Se pytest ha un pid basso (container in cui pytest è il processo 1 o uno dei primi) quel percorso esiste anche nel sandbox: falso VEDE-PYTEST. Il conteggio sotto 10 copre già il caso — riserva BASSA.
8. tests/test_unit_web_browser.py:517-537 — `--die-with-parent`: è il blocco descritto sopra.

Rischi esplicitamente esclusi:
- Il comportamento sul runner CI non root non l'ho riprodotto: qui gira solo da root. La corsa dipende dai tempi, e sul runner potrebbe uscire rossa o verde a caso.
- Non ho rifatto i 6 mutanti dichiarati, salvo `--die-with-parent`. Non ho lanciato l'intera suite web (749 test): ho lanciato solo il file del browser (41 passed).
- `--new-session` senza test (serve un TTY): dichiarato dall'agente, d'accordo.
- Restano fuori da questo delta, come dichiarato: V-1 bot e3a59ee, V-6 ve, R-601-1/2, R-603-1/2/3.
- Nota a margine, non da correggere qui: la stessa corsa vale anche in produzione. Se Gas muore nei primi millisecondi dopo l'avvio di bwrap, il sandbox sopravvive orfano.

V-2 COSMETICA del bot («Una pagina che usa i Worker…», modules/web/browser.py:47): chiusa.

Cosa serviva per l'approvazione: la correzione dell'attesa sul comm `sleep` nel test di tests/test_unit_web_browser.py:517 (più, se vuoi, la docstring di modules/web/browser.py:236), poi di nuovo il revisore sul nuovo diff staged. Il resto del delta è approvabile.

File:
- /home/user/Gas/modules/web/browser.py
- /home/user/Gas/tests/test_unit_web_browser.py
- /home/user/Gas/.claude/agents/memoria_revisore.md
```

Verdetto integrale della review #605 (chat Mani), sul diff finale del commit 366a0d5:

```
## VERDETTO: APPROVATO CON RISERVE

Review #605 (chat Mani). Ri-review della #604 sul delta V-3/V-4 della verifica esterna di #316. Base e3a59ee, diff staged con sha256 08f9e2d1.

**Elementi del diff esaminati**
- `tests/test_unit_web_browser.py:504` — `_sleep_vivi` prende i pid da `_pid_con`, che cerca nel cmdline il pezzo `\0sleep\033.271\0`, e tiene solo quelli con `comm == "sleep"`. Rischio esaminato: che trovi di nuovo il bwrap esterno, il cui cmdline contiene anche lui «sleep 33.271». Esito: ok, il bwrap ha `comm` bwrap e viene scartato.
- `tests/test_unit_web_browser.py:517` — `test_morto_bwrap_muore_il_sandbox`: aspetta che parta lo sleep vero, poi `os.kill(proc.pid)` (riga 531), poi controlla di nuovo con lo stesso helper. Rischio esaminato: il test non deterministico della #604. Esito: ok. L'ho riprodotto io, da root:
  - test da solo (`-k`): 5 su 5 passati;
  - mutante senza `--die-with-parent`: 6 su 6 falliti;
  - dopo i mutanti non resta nessuno sleep orfano (`pgrep`).
  R-604 è chiusa.
- `tests/test_unit_web_browser.py:517` (blocco `finally`) — `os.kill(pid)` sugli sleep ancora vivi. Rischio esaminato: `ProcessLookupError` se lo sleep muore tra la lista e il kill. Esito: **riserva R-605-2 BASSA**. È una corsa rara, solo nel test, e trasformerebbe una pulizia in un errore. Basta un `try/except ProcessLookupError`.
- `modules/web/browser.py:238` — docstring di `_comando_bwrap`: «scrivibile solo il profilo». Rischio esaminato: è una promessa falsa, come già R-600-3. Esito: **riserva R-605-1 COSMETICA**. Riprodotto: nel sandbox `touch /tmp/x`, `/var/x` e `/dev/shm/x` riescono. Hanno un tetto (1 MB per le cartelle nascoste, 256 MB per /dev/shm), quindi non è una fuga. Ma la frase va corretta, per esempio: «sul disco dell'host non si scrive; nel sandbox solo tmpfs con tetto (profilo, /dev/shm, nascoste)».
- `modules/web/browser.py:262` — la casa è montata in sola lettura con `--ro-bind`, il profilo è un tmpfs da 256 MB. È invariato dalla #604, dove era già stato provato. Esito: ok.

**Prove riprodotte**: web `python -m pytest tests/test_unit_web_*.py` 749 passed, 2 skipped (root). Browser 41 passed da nobody.

**Rischi esclusi (non verificati)**
- Comportamento sul runner della CI e sul VPS: qui c'è bwrap 0.9.0 da root, quindi non è riproducibile in questo ambiente.
- Le riserve BASSE della #604 restano come le hai registrate tu: sola lettura delle cartelle ri-esposte non provabile da nobody, pid basso di pytest. Non le ho riesaminate.

**Wall of Shame**: niente slicing della history e niente output di tool simulati. Il diff tocca solo il browser e i suoi test. Nessun guardrail indebolito: `--die-with-parent` ora ha un test che fallisce davvero se lo si toglie.

Riga contatore #605 scritta in `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata (a3cd94b). Nessuna lezione nuova.

Da tracciare in `stato_progetto.md`: R-605-1 COSMETICA (docstring alla riga 238) e R-605-2 BASSA (`ProcessLookupError` nel `finally` del test).
```

Commit (solo tests/test_unit_web_browser.py: V-1 a/b della verifica esterna su 30cd0a8, R-605-2). Verdetto integrale della review #606 (chat Mani):

```
## VERDETTO: APPROVATO

Review #606 (chat Mani). Delta di soli test sulla PR #316: il diff staged sopra 30cd0a8 tocca solo `tests/test_unit_web_browser.py` (+25/-1).

Elementi esaminati:
- `tests/test_unit_web_browser.py:443` — test V-1 a): mette la home in /var/tmp e toglie /var da `_NASCOSTE` con monkeypatch. Rischio esaminato: un test che passa per un altro motivo, cioè bwrap che non parte o un `HOME` che altera `_nel_sandbox`. Non succede: `returncode == 0` è richiesto e `_nel_sandbox` sovrascrive `HOME` col profilo, quindi il monkeypatch agisce solo su `expanduser` dentro `_comando_bwrap`. Ho provato il mutante senza `realpath(casa_utente)` fra le nascoste (`modules/web/browser.py:244`): 1 failed. Le cartelle temporanee si puliscono (nessuna gas-home rimasta in /var/tmp). Esito: ok.
- `tests/test_unit_web_browser.py:456` — test V-1 b): scrive `MEMORIA_PROFILO` + 8 MB nel profilo. Rischio esaminato: un falso verde se non si scrive niente. È escluso: c'è `0 <` e uno stdout vuoto dà errore. Ho provato il mutante con il tmpfs del profilo a 64 GiB e `MEMORIA_PROFILO` a 300 MB (`modules/web/browser.py:266`): 1 failed per asserzione, in 1 s. Esito: ok.
- `tests/test_unit_web_browser.py:561` — R-605-2: `ProcessLookupError` ignorato nel `finally`. `proc.kill()` su un processo già morto non solleva. Esito: ok, R-605-2 chiusa.

Prove riprodotte da root: file browser 43 passed; i due test nuovi passano 3 volte su 3 da soli (-k). Il modulo è stato ripristinato dopo i mutanti (`git status` pulito, a parte il file staged).

RAM in CI: 256 MB accettabili. È tmpfs in memoria per circa 1 s, liberato quando esce il namespace di bwrap. I runner GitHub hanno 7–16 GB; qui 16 GB, 15 GB disponibili.

Non verificato:
- La prova da nobody: mi fido dei vostri 43 passed.
- La prova sul runner CI vero: il delta non ha ancora girato in CI. La differenza di layout (Chromium sotto ~/.cache della home vera mentre `HOME` è spostata) l'ho ragionata, non provata: la home vera resta nascosta da /home e `_copre` non scatta.
- La suite web completa (751): non rilanciata.

Nota BASSA, non bloccante: se /var/tmp non esiste, il test a) dà errore invece di essere saltato. Va bene così, è un fallimento rumoroso.

Nessuna lezione nuova. La riga contatore #606 è committata (175c0ba, `.claude/agents/memoria_revisore.md`).
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. `tests/test_unit_web_browser.py`: da 25 a 43 test (obbligatori in CI). `tests/test_unit_web_proxy.py`: da 71 a 72. Web con il comando della CI (`python -m pytest tests/test_unit_web_*.py`), con node, playwright e bwrap, da root: 751 passed, 2 skipped; browser da utente nobody (come il runner): 43 passed. ATTENZIONE: su fc318cf la CI era ROSSA (3 test del sandbox, vedi §1 e §6); i numeri locali di allora erano da root e non coprivano il runner non root. Mutanti presi (1 o 2 failed ciascuno): senza Worker spento, senza `--unshare-all`, Gas visibile fuori da /home, senza PID namespace, senza `process.exit`, sonda sempre vera, senza `--cap-drop`, solo home/root/tmp nascoste, senza controllo degli antenati, senza percorso vero, senza tetto dei tmpfs. Dopo la #602 presi anche: lo skip dei collegamenti, `_NASCOSTE` senza /home e /root. Dopo la verifica esterna (366a0d5): ri-esposte scrivibili, casa scrivibile senza tmpfs del profilo, senza --proc, senza --die-with-parent (6 su 6), SPEGNI ridotto, senza unshare-ipc; poi home non nascosta, profilo senza tetto vero. Non presi (R-601-1): senza cwd="/" nella sonda di Playwright, /dev/shm senza `--size`.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 7860381, 1d5fc27, ea763c8 (memoria del revisore), a8d4b52 (fetta 34): pushati insieme; run su a8d4b52 (job 124726382253): unit-suite FAILURE (3 test del sandbox).
- fc318cf (fine-task): run 41265278907, unit-suite FAILURE (stessi 3 test); handoff-check success; verifica-bot failure (bot BOCCIATO per la CI rossa).
- 5d7a8c1, fee8985 (memoria del revisore), 9b6b83e (correzione), e3a59ee (fine-task): pushati insieme; run 41267528825 su e3a59ee success (unit-suite, handoff-check); verifica-bot success (bot APPROVATO CON RISERVE). I commit intermedi non hanno una run propria.
- a6d5288, a3cd94b (memoria del revisore), 366a0d5 (V-3/V-4), 77bdc2a e 30cd0a8 (fine-task): pushati insieme; run 41270078918 su 30cd0a8 success (unit-suite, handoff-check); verifica-bot success (bot APPROVATO CON RISERVE). I commit intermedi non hanno una run propria.
- I commit della review #606 (memoria e test) e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- V-1 bot #316 su e3a59ee BASSA: i discendenti della home sono ri-esposti per intero (es. node in ~/.local/bin ri-espone ~/.local); Gas resta coperto.
- V-6 ve #316 BASSA (limite): /etc, /usr e il resto non nascosto restano leggibili; un file d'ambiente di Gas sotto /etc sarebbe leggibile da un renderer compromesso.
- `--new-session` senza test (serve un TTY).
- V-1 c/d ve #316 su 30cd0a8 (BASSE, dichiarate): `serviceWorkers: 'block'` e `routeWebSocket(…ws.close())` non hanno un test che li tenga (difesa in profondità: il netns e il proxy fermano comunque il traffico); XDG_* puntati alla casa invece che al profilo passerebbero i test.
- V-2 bot #316 su 30cd0a8 BASSA: le cartelle in cima al disco fuori dall'elenco (es. /data, /backup) restano leggibili; prossima fetta «tmpfs su / con elenco di cartelle permesse», condizione per accendere il browser (reports/roadmap.md).
- R-605-1 (chat Mani) COSMETICA: il docstring di `_comando_bwrap` dice «scrivibile solo il profilo»; sono scrivibili anche /tmp, /var e /dev/shm del sandbox (tmpfs con tetto).
- R-605-2 (chat Mani) BASSA: nel `finally` di `test_morto_bwrap_muore_il_sandbox` un `os.kill` può dare ProcessLookupError se lo sleep muore nel frattempo.
- Riserve BASSE della #604: la sola lettura delle ri-esposte non si prova da un utente che non può scriverci; con un pid basso di pytest il controllo VEDE-PYTEST darebbe un falso positivo (lo copre il conteggio sotto 10).
- R-603-1 (chat Mani) BASSA: il controllo su mountinfo prova che il tmpfs c'è, non che sia il montaggio in cima (oggi lo coprono `_copre` e il segno nella home).
- R-603-2 (chat Mani) BASSA: `_di_un_altro_pytest` cerca «pytest» come testo nel cmdline: con TMPDIR sotto /tmp/pytest-of-… ignorerebbe i browser della propria suite.
- R-603-3 (chat Mani) BASSA: /usr fuori dal find di socket e FIFO (sola lettura, nessun socket atteso).
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
