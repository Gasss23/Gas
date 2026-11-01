# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-01 — Mani, fetta 35 (R6): sandbox del browser con radice vuota ed elenco di cartelle permesse (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #317 (https://github.com/Gasss23/Gas/pull/317). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5112440398","url":"https://github.com/Gasss23/Gas/pull/317"}`), perché `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve il sì dell'operatore, anche tramite M1.
2. Fetta di SICUREZZA: secondo passaggio indipendente nella chat claude.ai col link della PR.
3. Il browser resta SPENTO. Per accenderlo sul VPS manca la seconda condizione della roadmap: una prova dal vero sul VPS (bwrap con --size, AppArmor, node, Playwright, HTTPS senza /etc/ssl).

---

## §1 SCOPE & ESITO FETTE

- **PR #316 (bwrap per il browser)**: `FATTA` — mergiata (87f576c) col sì dell'operatore.
- **Radice vuota ed elenco di cartelle permesse** (prima condizione della roadmap, assegnata da M1): `FATTA` — `_comando_bwrap`: radice = tmpfs vuoto rimontato in sola lettura; visibili solo `_PERMESSE` (/usr/bin, /usr/lib/<arch>, /usr/lib64, caricatore, font, /etc/fonts, /etc/ld.so.cache, /etc/localtime), /bin /lib… rifatti, il solo file di node, i soli pacchetti playwright e playwright-core, Chromium al percorso vero, la casa; scrivibili solo /tmp, /dev/shm e il profilo, con tetto; Gas e home coperte se dentro una permessa; rifiuti se node/Playwright mancano o se un ri-esposto scoprirebbe Gas o la home. Prototipo provato prima del codice.
- **V-6 ve e V-2 bot #316** (cartelle non nascoste leggibili): `FATTA`. **V-1 bot #316** (~/.local): `FATTA` — non si ri-espone più il prefisso di node.
- **R-605-1** (docstring): `FATTA`. **R-601-1** (cwd della sonda e tetto di /dev/shm senza test): `FATTA`. **R-601-2** (sonda senza le opzioni vere): `FATTA`.
- **R-603-1** (mountinfo non provava il montaggio in cima) e **R-603-3** (/usr fuori dal find): `FATTA` — un test elenca OGNI file visibile nel sandbox contro un elenco scritto nel test, senza escludere /usr, e vuole zero socket e FIFO. **R-603-2** (rilevatore di pytest): `FATTA` — argv.
- **V-1 d ve #316** (routeWebSocket senza test): `FATTA`. **V-1 c ve #316** (serviceWorkers 'block' senza test): `SALTATA — nella prova la pagina non diventa sicura (navigator.serviceWorker assente anche con --unsafely-treat-insecure-origin-as-secure), il test passerebbe a vuoto; resta dichiarata`.
- **Review #607 (chat Mani)**: APPROVATO CON RISERVE. R-607-1 MEDIA (il test accettava tutto /gas/: due mutanti sopravvivevano), R-607-2 BASSA (fallimento della sonda in cache), R-607-3 BASSA (aarch64 e /usr non unito): `FATTA`. **Review #608**: APPROVATO.
- **Bot su 427e57d (https://github.com/Gasss23/Gas/pull/317#pullrequestreview-5730697074)**: APPROVATO CON RISERVE, check success, CI verde. V-1 BASSA (permessa che è un collegamento: la copertura di Gas finiva sul percorso vero, non dove la cartella si vede): `FATTA` in 505479f.
- **Verifica esterna su 427e57d (https://github.com/Gasss23/Gas/pull/317#issuecomment-6565285968)**: APPROVATO CON RISERVE. V-1 MEDIA (/dev del sandbox scrivibile senza tetto): `FATTA` in 505479f — --remount-ro /dev più test. V-2 BASSA (lo stesso punto del bot): `FATTA`. V-3 BASSA (in CI il test «ogni file» non monta Chromium: PLAYWRIGHT_BROWSERS_PATH non impostata): `SALTATA — dichiarata` (lo coprono i test end-to-end). V-4 COSMETICA (prefisso senza «/» nel test): `FATTA`.
- **Review #609 (chat Mani)**: APPROVATO CON RISERVE. R-609-1 BASSA (il ramo dei collegamenti guarda solo l'ultimo pezzo del percorso) e R-609-2 COSMETICA (la sonda non porta --remount-ro /dev): `DEFERITA — registrate`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/web/browser.py             | 159 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------
 reports/diff_sessione.md           |  16 +++++++--------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   2 +-
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  34 ++++++++++++-------------------
 tests/test_unit_web_browser.py     | 252 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------
```

NB: base = merge-base con origin/main = 87f576c. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
505479f fix(web): /dev del sandbox in sola lettura, permesse-collegamento rifatte come collegamenti (V-1/V-2 ve e V-1 bot #317, review #609)
d3c3d22 chore(revisore): memoria review #609 — APPROVATO CON RISERVE
427e57d docs(fine-task): fetta 35 sandbox con elenco di cartelle permesse, PR #317, review #607/#608
a26a8a9 feat(web): sandbox del browser con radice vuota ed elenco di cartelle permesse (R6, fetta 35, chat Mani)
fb8b0c0 chore(revisore): memoria review #608 — APPROVATO
9494a95 chore(revisore): memoria review #607 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit a26a8a9 (modules/web/browser.py, tests/test_unit_web_browser.py). Verdetto integrale della review #607 (chat Mani), sulla prima versione:

```
## VERDETTO: APPROVATO CON RISERVE

Review #607 (chat Mani). Fetta 35, R6, SICUREZZA: il sandbox del browser ora parte da una radice tmpfs vuota e mostra solo l'elenco `_PERMESSE`. Ho revisionato il diff staged (sha256 `ba9ca8a5…`, base 87f576c, branch claude/peaceful-lovelace-0w2b7q). Tutte le prove le ho fatte su un export dell'index, non sulla cartella di lavoro.

Letture fatte prima della review: CLAUDE.md (sez. 1, 5, 8, 9, 10), reports/stato_progetto.md (voce fetta 34 e riserve aperte), reports/roadmap.md (la condizione per accendere il browser sul VPS), memoria_revisore.md (le lezioni su bwrap e mutanti, #599–#606). Wall of Shame: nessuno slicing della history e nessuna simulazione di tool (non c'entrano con questo diff). gas.py e ci.yml non sono toccati.

### Elementi del diff esaminati

- `modules/web/browser.py:90` — `_PERMESSE`, l'elenco in sola lettura. Rischio esaminato: espone segreti o sblocca privilegi? Ho controllato `/usr/bin`, `/usr/lib/x86_64-linux-gnu`, `/usr/lib64`, i font e `/etc/fonts`: nessun file di chiavi, token o .env. Ci sono binari setuid (sudo, su, mount), ma dentro il montaggio è nosuid e `NoNewPrivs: 1`, quindi non servono a niente. — **ok**
- `modules/web/browser.py:304` — `--remount-ro /` alla fine. Rischio: radice scrivibile o tmpfs scrivibili senza tetto. Visto da dentro con mountinfo: `/` è tmpfs ro; scrivibili solo `/tmp` (1 MB), `/dev/shm` (256 MB) e il profilo (256 MB); CapEff tutto a 0. — **ok**
- `modules/web/browser.py:283` — `esposti`: node in `/gas/bin/node`, i due pacchetti in `/gas/node/...`. Rischio: si ri-espone di più di quanto dichiarato. Il codice è giusto: dentro `/gas/node` ci sono solo playwright e playwright-core. Però nessun test lo tiene, vedi R-607-1. — **riserva**
- `modules/web/browser.py:296` — copertura di Gas e della home dentro una cartella permessa. Mutante «protetti senza realpath» → 1 failed. — **ok**
- `modules/web/browser.py:239` — la cache di `_cartelle_di_playwright` salva anche il fallimento (`[]`). Un timeout passeggero della sonda node (10 s) spegne il browser fino al riavvio di Gas. — **riserva BASSA (R-607-2)**
- `modules/web/browser.py:204` — la sonda `_bwrap_funziona` ora usa --cap-drop, --size, --remount-ro e le permesse (R-601-2 chiusa). — **ok**
- `modules/web/browser.py:305` — `PATH=/usr/bin` dentro. Sui sistemi con `/usr` non unito (/bin/sh fuori da /usr/bin) il comando fallisce. È fail-closed: niente fuga. — **riserva BASSA (in R-607-3)**
- `tests/test_unit_web_browser.py:406` — l'elenco del test «ogni file visibile» accetta `"/gas/"` per prefisso intero. — **riserva MEDIA (R-607-1)**
- `tests/test_unit_web_browser.py:415` — come il test legge gli errori di find (virgolette ASCII). Rischio: in CI con LANG=C.UTF-8 find userebbe le virgolette ‘ ’ e il test cadrebbe. Verificato: nel sandbox il locale C.UTF-8 non si carica, find torna alle virgolette ASCII, e il test passa da nobody anche con LANG=C.UTF-8. — **ok**
- `tests/test_unit_web_browser.py:266` — `test_routewebsocket_chiude_anche_senza_lo_script`. Esercita il ramo giusto: senza routeWebSocket ci sarebbe un CONNECT sulla 443. — **ok**
- `tests/test_unit_web_browser.py:468` — test dei rifiuti. Mutante «senza rifiuto degli esposti» → 1 failed. Nota COSMETICA: il test controlla solo il prefisso «browser non isolabile», quindi in un ambiente senza Playwright passerebbe a vuoto per il rifiuto sbagliato. In CI Playwright c'è.

### Riprodotto

- browser: 41 passed da root; 41 passed da nobody, sia senza LANG sia con LANG=C.UTF-8;
- web: `tests/test_unit_web_*.py` 749 passed, 2 skipped;
- mutanti presi (1 failed ciascuno): senza rifiuto degli esposti, protetti senza realpath, `/usr/lib` intera al posto di `/usr/lib/<arch>`.

### Riserve

- **R-607-1 MEDIA** — il test di `tests/test_unit_web_browser.py:406` non tiene la chiusura di V-1 bot #316.
  - Due mutanti sopravvivono (41 passed):
    - «tutta la node_modules in /gas/node», cioè proprio la regressione di V-1 bot #316 (nell'ambiente di prova espone eslint, claude, npm, …);
    - «la cartella bin di node in /gas/bin», che con node in ~/bin riaprirebbe un caso alla R-599-2.
  - Correzione provata: in `permessi` sostituire `"/gas/"` con `"/gas/node/playwright/", "/gas/node/playwright-core/"` e aggiungere `"/gas/bin/node"` a `esatti`. Con questa il test passa sul codice giusto e prende entrambi i mutanti (1 failed ciascuno).
  - Consiglio di chiuderla in questa fetta, prima del commit, con una ri-review: la verifica esterna la segnalerebbe come V-3 ve.
- **R-607-2 BASSA** — `modules/web/browser.py:239`: non mettere in cache il risultato vuoto.
- **R-607-3 BASSA (portabilità, fail-closed)** — due casi in cui il browser resta spento senza un motivo chiaro:
  - su aarch64 l'interprete `/lib/ld-linux-aarch64.so.1` sta in `/usr/lib/`, che non è montata: ogni programma dinamico fallisce, la sonda dice «bwrap non funziona» e il browser resta spento con un motivo fuorviante;
  - su `/usr` non unito vale lo stesso per PATH=/usr/bin.
  - Il VPS scelto (Netcup, x86, Ubuntu probabile) non ne è toccato. Volta e asdf (node come «shim») cadono anche loro chiusi; nvm funziona, perché node è un file binario vero.

Valuto **V-1 c ve** (serviceWorkers 'block' senza test) giustamente lasciata aperta e dichiarata: un test che passa a vuoto è peggio di nessun test.

### Rischi esplicitamente esclusi

- HTTPS reale di Chromium nel sandbox, senza /etc/ssl: non l'ho verificato perché qui non c'è uscita diretta verso internet. Il rischio è basso (Chromium ha la Chrome Root Store compilata dentro), ma va coperto dalla prova dal vero sul VPS già prevista in roadmap, insieme a bwrap con --size, AppArmor e node.
- aarch64 e `/usr` non unito: analizzati sul codice, non eseguiti (questo host è x86_64 con `/usr` unito).
- CI GitHub: non ho lanciato i test lì. La prova da nobody è l'approssimazione più vicina.

### Memoria

- Riga contatore #607 e una lezione nuova scritte in /home/user/Gas/.claude/agents/memoria_revisore.md;
- committate da sole con `scripts/commit_memoria_revisore.sh` (commit 9494a95). Il diff staged sotto review è rimasto intatto.
```

Verdetto integrale della review #608 (chat Mani), sul diff finale del commit a26a8a9:

```
## VERDETTO: APPROVATO

Review #608 (chat Mani). È la ri-review della #607 sulla fetta 35. Il diff staged ha sha256 25eec683…, base 87f576c, e dopo i mutanti è intatto (sha rimasto uguale, working tree pulito).

Elementi esaminati:
- `modules/web/browser.py:243` — se la sonda non trova i due pacchetti restituisce [] e non mette niente in cache (R-607-2). Rischio esaminato: un timeout passeggero che spegne il browser fino al riavvio di Gas. Ho provato il mutante che rimette in cache il fallimento: 1 failed. **Esito: ok.**
- `modules/web/browser.py:91` — in `_PERMESSE` ora c'è anche `glob("/usr/lib/ld-linux*")`, cioè il caricatore dei programmi (R-607-3). Rischi esaminati:
  - il caricatore aarch64 mancante: su /usr unito, /lib è un collegamento rifatto verso usr/lib, quindi /lib/ld-linux-aarch64.so.1 arriva al file montato;
  - il caso con `_ARCH` vuota: le voci sono doppioni dentro /usr/lib, innocui;
  - l'esposizione di Gas o della home: la voce è un file, `_copre` resta corretto.

  Qui la lista è vuota (verificato con `ls`). **Esito: ok.**
- `modules/web/browser.py:311` — dentro il sandbox PATH vale /usr/bin:/bin. Rischio esaminato: /bin/sh mancante su /usr non unito. /bin arriva da `_radice()`, come collegamento rifatto o come cartella in sola lettura, quindi il doppione su /usr unito è innocuo. **Esito: ok.**
- `tests/test_unit_web_browser.py:406` — l'elenco permesso non contiene più «/gas/» intero: restano solo /gas/node/playwright/ e /gas/node/playwright-core/, e /gas/bin/node è fra gli esatti (R-607-1). Ho riprovato i due mutanti, e ciascuno dà 1 failed per la ragione giusta:
  - cartella bin di node intera in /gas/bin: 41 file fuori elenco (`/gas/bin/ts-script`…);
  - node_modules intero in /gas/node: 6003 file fuori elenco (`/gas/node/.bin/…`).

  Senza mutanti il test passa. **Esito: ok.**
- `tests/test_unit_web_browser.py:509` — test nuovo: con NODE_PATH=/nessuno la sonda restituisce [] e `_MODULI` resta vuoto. **Esito: ok.**

Riprodotto: `tests/test_unit_web_browser.py` dà 42 passed da root.

Rischi esclusi (non verificati):
- **aarch64 e /usr non unito non provati davvero**: qui non posso riprodurli (host x86_64 con /usr unito); il ragionamento è solo sul codice. Se lì manca qualcosa, il sandbox fallisce chiuso: il browser resta spento, Gas non crasha.
- **Il test di :509 dipende dall'host**: se Playwright fosse installato in una cartella globale di node (es. ~/.node_modules) darebbe un falso rosso. Sarebbe visibile, non un falso verde.
- **Non ho rilanciato** la suite web completa né le prove da nobody: mi fido dei vostri 750 passed / 2 skipped e dei 42 passed da nobody.

Memoria: riga #608 scritta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (fb8b0c0). Nessuna lezione nuova.
```

Commit 505479f (modules/web/browser.py, tests/test_unit_web_browser.py: V-1/V-2 ve e V-1 bot su 427e57d). Verdetto integrale della review #609 (chat Mani):

```
## VERDETTO: APPROVATO CON RISERVE

Review #609 (chat Mani). È il delta sulla PR #317, fetta 35, sopra 427e57d. Il diff staged ha sha256 17cfa0a8…, rimasto uguale dopo i mutanti.

Letture fatte: CLAUDE.md (sez. 5, 8, 9, 10), stato_progetto.md (solo la parte sul sandbox) e la memoria fino alla #608.

**Elementi esaminati**
- `modules/web/browser.py:289`: `--remount-ro /dev` sta subito dopo `--dev /dev` e prima del tmpfs `/dev/shm`, che ha il tetto. Rischio esaminato: Chromium che si rompe e /dev/null non scrivibile. Su un fs in sola lettura i device a caratteri restano scrivibili, e i test end-to-end col Chromium vero passano. Mutante senza remount: 1 failed, con l'uscita `SCRIVE-DEV`. Esito: ok.
- `modules/web/browser.py:277`: una permessa che è un collegamento a una cartella diventa `--ro-bind vero vero` più `--symlink readlink permessa`. Così il tmpfs messo su realpath(Gas) e realpath(home) copre anche quello che si vede dal collegamento. Rischi esaminati:
  - un `readlink` relativo (es. `lib`) si risolve bene dentro il sandbox;
  - quanto si vede non aumenta: prima la cartella vera era già visibile intera, sotto il nome del collegamento.

  Mutante con il ramo nuovo tolto: 1 failed, con l'uscita `VISIBILESEGRETO`. Esito: ok, con la riserva R-609-1.
- `tests/test_unit_web_browser.py:382`: il test controlla che `touch /dev/x` fallisca e che `echo > /dev/null` funzioni. Rischio esaminato: un test troppo largo. Pretende la sequenza esatta `DEVNULL PROFILO TMP NORETE`. Esito: ok.
- `tests/test_unit_web_browser.py:467`: il test nuovo legge `.env` da tre strade: il collegamento, il percorso vero e un file libero. Rischi esaminati: la pulizia (unlink nel finally, nessun residuo `gas-perm*` in /var/tmp) e la ragione per cui fallisce col mutante. Esito: ok.
- `tests/test_unit_web_browser.py:413`: il prefisso `/usr/lib/ld-linux` senza «/» è sostituito dal glob negli esatti, lo stesso di `modules/web/browser.py:96`. Esito: ok, V-4 chiusa.

**Prove riprodotte**
- browser: 43 passed da root e 43 passed da nobody.
- web (`-k web`): 752 passed, 2 skipped. Voi ne dichiarate 751: probabilmente la selezione è diversa, non è un problema.

**Riserve**
- **R-609-1 BASSA**: il ramo nuovo guarda solo l'ultimo pezzo del percorso (`islink(permessa)`). Se è un collegamento una cartella più in alto (vero diverso da permessa ma permessa non è un link), si monta ancora vero→permessa e il tmpfs sul percorso vero non copre. È teorico sulle distribuzioni note. La correzione possibile: condizione `vero != permessa and isdir(vero)` con `--symlink vero permessa` assoluto.
- **R-609-2 COSMETICA**: la sonda `_bwrap_funziona` non porta `--remount-ro /dev`. L'opzione `--remount-ro` è comunque già provata nella sonda su «/».

**Rischi esplicitamente esclusi**
- Arch e aarch64 veri, dove `/usr/lib64` è un collegamento: non provati, perché qui `/usr/lib64` è una cartella vera. Il ramo nuovo l'ha provato solo il test con il collegamento finto.
- V-3 BASSA (in CI il test «ogni file» non monta Chromium): presa come dichiarata, non l'ho verificata in CI.

Memoria: riga #609 scritta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata (d3c3d22).
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. `tests/test_unit_web_browser.py`: da 43 a 43 test (test di isolamento riscritti per il modello nuovo; tolti quelli legati a `_NASCOSTE`, aggiunti l'elenco di ogni file visibile, i tetti di /tmp e /dev/shm, Gas e home dentro una permessa, rifiuti, sonde, routeWebSocket, cache). Web con il comando della CI (`python -m pytest tests/test_unit_web_*.py`), da root: 751 passed, 2 skipped; browser da utente nobody: 43 passed. Mutanti presi (1 failed ciascuno): /etc intera, radice scrivibile, Gas dentro una permessa non coperta, prefisso di node ri-esposto, tutta node_modules, cartella bin di node, /tmp senza tetto, /dev/shm senza tetto, sonda senza cwd, fallimento in cache, routeWebSocket→connectToServer, rifiuto degli esposti tolto, /dev scrivibile, permessa-collegamento montata come prima. Non preso: `--new-session` (serve un TTY).

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 9494a95, fb8b0c0 (memoria del revisore), a26a8a9 (fetta 35): pushati insieme prima dell'apertura della PR #317; nessuna run su questi SHA prima della PR.
- 427e57d (fine-task): run su 427e57d success (unit-suite, handoff-check); verifica-bot success (bot APPROVATO CON RISERVE).
- d3c3d22 (memoria #609), 505479f (correzioni) e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- V-1 c ve #316 BASSA: `serviceWorkers: 'block'` senza test (nella prova la pagina non diventa sicura); `--new-session` senza test (serve un TTY).
- R-609-1 (chat Mani) BASSA: il ramo delle permesse-collegamento guarda solo l'ultimo pezzo del percorso (un collegamento più in alto non è coperto; teorico sulle distribuzioni note). R-609-2 (chat Mani) COSMETICA: la sonda di bwrap non porta --remount-ro /dev.
- V-3 ve #317 BASSA: in CI il test «ogni file visibile» non monta Chromium (PLAYWRIGHT_BROWSERS_PATH non impostata); lo coprono i test end-to-end.
- aarch64 e /usr non unito: analizzati sul codice, non provati (fail-closed: il browser resta spento).
- HTTPS reale di Chromium senza /etc/ssl, bwrap con --size e AppArmor sul VPS: da provare sul VPS (seconda condizione della roadmap per accendere il browser).
- Limiti dichiarati del browser: Chromium senza la sua sandbox; il proxy filtra le destinazioni, non i dati; niente regola https→http e pagina riscaricata (R-593-6); X-Gas-Proxy dentro i tunnel https non si toglie (R-593-3); una pagina che usa i Worker può non funzionare.
- Riserve BASSE della #604: la sola lettura dei ri-esposti non si prova da un utente che non può scriverci; pid basso di pytest.
- Nota BASSA (review #593): un'intestazione «Nome : valore» fa rifiutare la pagina dal proxy.
- V-1 bot #309 BASSA (limite); R-582-1 BASSA, R-582-2 COSMETICA, R-580-2 BASSA (limiti del bot); V-1/V-2 bot e ve #306; R-572-1, R-572-2, R-575-1 BASSE e R-575-2 COSMETICA; (b) libexpat ≥ 2.4 nel doctor con M1; V-3 ve #303 (selectolax 1.0.2, decisione dell'operatore); R-518-1, R-516-1, R-ve277-5, V-1 ve/bot #288, V-2/V-3 ve #296, R-546-1: invariate.
