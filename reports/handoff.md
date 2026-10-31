# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-31 — Mani, fetta 33 (R6): browser senza schermo dietro il proxy filtrante (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #315 (https://github.com/Gasss23/Gas/pull/315). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5099784756","url":"https://github.com/Gasss23/Gas/pull/315"}`), perché `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve il sì dell'operatore, anche tramite M1.
2. Fetta di SICUREZZA: secondo passaggio indipendente nella chat claude.ai col link della PR. Bot e verifica esterna: APPROVATO CON RISERVE (solo V-1 BASSA); `verifica-bot` è neutral perché la PR tocca ci.yml: il merge lo decide l'operatore.
3. Il browser resta SPENTO (`GAS_WEB_BROWSER` non impostato). Accenderlo sul VPS è una decisione dell'operatore, da prendere solo dopo l'isolamento bwrap (punto 4 del piano), perché oggi Chromium gira senza sandbox.

---

## §1 SCOPE & ESITO FETTE

- **PR #312 (proxy filtrante)**: `FATTA` — mergiata (01eba0d) con auto-merge, dopo il sì dell'operatore arrivato tramite M1; prima unito main 3a38e75 (#313), review #592 APPROVATO.
- **Punto 1 del piano (Chromium in un processo figlio)**: `FATTA` — `modules/web/browser.py`: Playwright per Node (`node -e`; in Python non c'è); tempo massimo, ulimit -d per processo, V8 256 MB, profilo temporaneo, niente estensioni né download, env senza chiavi, uccisione di tutti i processi della lettura.
- **Punto 3 (spegnimenti)**: `FATTA` — WebRTC, WebSocket, service worker, notifiche, permessi, popup spenti; JavaScript acceso.
- **Punto 5 (uscita)**: `FATTA` — solo innerText e titolo, con la pulizia di leggi.py e i marcatori NON FIDATO (`_incornicia`, la stessa di leggi_pagina).
- **Punto 6 (spento per default)**: `FATTA` — `GAS_WEB_BROWSER=1`; leggi_pagina lo usa solo per una pagina vuota senza JS. «Lo chiede Gas» (parametro dello strumento in gas.py): `DEFERITA — gas.py lasciato a dopo, decisione di M1`.
- **Punto 7 (test)**: `FATTA` — `tests/test_unit_web_browser.py` (25 test) con origine finta: JS, 127.0.0.1, ::1, porta 8080, IP privati, ws:// (anche da un worker, fermato dal proxy sulla porta 80), popup, redirect vietati, tempo massimo, processi, env.
- **Punto 4 (bwrap)**: `DEFERITA — fuori scope (M1 ha dato i punti 1, 3, 5, 6, 7)`: dichiarato come limite, da fare prima di accendere il browser sul VPS.
- **Riserve del proxy**: R-585-4 (testa della risposta riscritta con `Connection: close`) `FATTA`; R-585-5 (`--proxy-bypass-list=<-loopback>`, QUIC, WebRTC, prefetch) `FATTA`; V-4 bot #312 (intestazioni nominate in Connection) `FATTA`; V-2 bot #312 su 805b4d8 (il «200» del tunnel nel tetto dei byte) `FATTA`; V-2 bot #312 su 3a31a99 (numero vecchio nell'handoff §5) `FATTA` — l'handoff è riscritto da zero.
- **ci.yml**: `FATTA` — solo l'env NODE_PATH e GAS_TEST_BROWSER_OBBLIGATORIO nel passo web, autorizzato da M1.
- **Review #593 (chat Mani)**: APPROVATO CON RISERVE. R-593-1 MEDIA (Chromium vivo dopo il kill del gruppo di node): `FATTA`; R-593-2/3/4/5/6 BASSE: `FATTA` (la 3 su https e la 6 dichiarate come limiti).
- **Review #594**: APPROVATO CON RISERVE. R-594-1 BASSA (test end-to-end debole sul mutante): `FATTA` — test diretto; R-594-2 BASSA: `DEFERITA — dichiarata`; R-594-3 COSMETICA: `FATTA`.
- **Review #595**: APPROVATO CON RISERVE. R-595-1 e R-595-2 BASSE: `DEFERITA — registrate`.
- **Merge di origin/main 9fdbd2b (PR #314 di M2, voce V5)**: `FATTA` — conflitto solo nella memoria del revisore. Review #596 APPROVATO CON RISERVE (R-596-1: riserve nello stato, `FATTA` nei report).
- **Bot su fc91022 (https://github.com/Gasss23/Gas/pull/315#pullrequestreview-5724040424)**: APPROVATO CON RISERVE, check `verifica-bot` neutral (la PR tocca ci.yml, macchina del bot: decide l'operatore). V-1 BASSA (WebSocket dai worker non provati): vedi sotto.
- **Verifica esterna su fc91022 (https://github.com/Gasss23/Gas/pull/315#issuecomment-6546815822)**: APPROVATO CON RISERVE. V-1 BASSA (riprodotta: un Dedicated Worker apre wss:// verso la 443 dal tunnel; lo script iniettato e routeWebSocket non coprono i worker; il report diceva il contrario): `FATTA` la dichiarazione corretta in 7363702 (docstring e commento del test, review #598); `DEFERITA — fetta bwrap` il fix vero (WebSocket spento nei worker, test con wss sulla 443, figlio che fallisce se routeWebSocket manca). V-2 COSMETICA (§6 superato dai fatti): `FATTA` — §6 aggiornato. Nota: R-593-1 non riprodotta con Playwright 1.56.1, il fix resta difensivo.
- **Review #598 (chat Mani)**: APPROVATO CON RISERVE. R-598-1 COSMETICA (il commento del test dice «Upgrade», ma il ws:// lo ferma il controllo CONNECT): `DEFERITA — fetta bwrap`.
- **Gate IP al primo fine-task (6ed1741, non pushato)**: fermo su IP di esempio. `FATTA` — marcatore gasmerge-ip-ok nel test (b64a54e, review #597 APPROVATO) e nella riga #593 della memoria (1db489f); nell'handoff l'indirizzo «tutti zeri» citato nei verdetti #593 e #597 è scritto <IP-redatto>.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  10 ++++++++++
 .github/workflows/ci.yml           |   5 +++++
 modules/web/browser.py             | 273 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/web/leggi.py               |  40 +++++++++++++++++++++++++++++++++++++---
 modules/web/proxy.py               | 114 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------
 reports/diff_sessione.md           |  22 ++++++++++++++--------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   2 +-
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  33 +++++++++++++++++++++++----------
 tests/test_unit_web_browser.py     | 364 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_web_leggi.py       |   4 ++--
 tests/test_unit_web_proxy.py       | 124 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: base = merge-base con origin/main = 9fdbd2b. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
7363702 docs(web): WebSocket spenti solo in pagine e frame, non nei worker (V-1 ve/bot #315, review #598)
a196b6b chore(revisore): memoria review #598 — APPROVATO CON RISERVE
fc91022 docs(fine-task): fetta 33, PR #315, IP di esempio redatti nell'handoff
598aa4e docs(fine-task): fetta 33, PR #315, gate IP e review #597
b64a54e test(web): IP di esempio segnato per il gate IP (review #597)
1db489f chore(revisore): memoria review #597 — APPROVATO
6ed1741 docs(fine-task): fetta 33 browser senza schermo, PR #315, review #593-#596
713f59f chore(revisore): memoria review #596 — APPROVATO CON RISERVE
d313fad Merge origin/main (9fdbd2b, PR #314 di M2) in claude/peaceful-lovelace-0w2b7q (fetta 33)
1895d7c feat(web): browser senza schermo dietro il proxy filtrante (R6, fetta 33, chat Mani)
ce68d35 chore(revisore): memoria review #595 — APPROVATO CON RISERVE
7649991 chore(revisore): memoria review #594 — APPROVATO CON RISERVE
bf07949 chore(revisore): memoria review #593 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 1895d7c (modules/web/browser.py, modules/web/leggi.py, modules/web/proxy.py, test web, .github/workflows/ci.yml). Verdetto integrale della review #593 (chat Mani), sulla prima versione. Unico ritocco, per il gate IP: l'indirizzo «tutti zeri» della lista delle sonde è scritto <IP-redatto>; il resto è identico:

```
## VERDETTO: APPROVATO CON RISERVE

Review #593 (chat Mani). R6 fetta 33, browser senza schermo. Diff staged sha256 3e906242 su base 01eba0d, branch claude/peaceful-lovelace-0w2b7q. Letti prima della review: CLAUDE.md (§1, §5, §8, §9, §10), le parti di reports/stato_progetto.md che riguardano R6 e il proxy, e la memoria del revisore. La riga contatore #593 è nella memoria ed è committata col suo script (bf07949). L'index non è cambiato, quindi l'hash del diff staged resta valido per `segna_review_ok.sh`.

**Elementi del diff esaminati**

- `modules/web/browser.py:55` — `--proxy-bypass-list=<-loopback>` insieme a `--proxy-server` — rischio: uscite in rete che non passano dal proxy — **ok**. Ho caricato una pagina che chiama 127.0.0.1, [::1], localhost, foo.localhost, <IP-redatto>, 127.1, [::ffff:127.0.0.1], 2130706433, più img, sendBeacon, link prefetch, fetch e WebSocket da un Worker: all'origine è arrivata solo «/». Nessun pacchetto UDP verso uno STUN su 127.0.0.1.
- `modules/web/browser.py:99` — script iniettato e routeWebSocket — rischio: aggirarli con un iframe creato al volo — **ok**. Ho provato `iframe.contentWindow.RTCPeerConnection` e `.WebSocket`: entrambi `undefined`, quindi lo script vale anche nell'iframe. Una navigazione JS verso file:///etc/hostname è bloccata da Chromium (il testo resta quello della pagina, Fonte quella di partenza).
- `modules/web/browser.py:144` e `modules/web/browser.py:172` — `_uccidi` con killpg sul gruppo di node — rischio: processi orfani — **riserva (R-593-1, MEDIA)**. Vedi sotto.
- `modules/web/browser.py:173` — `splitlines()` sull'uscita del figlio — rischio: la pagina rompe l'uscita JSON — **riserva (R-593-2, BASSA)**. Una contraffazione dell'esito non è possibile: JSON.stringify fa l'escape delle virgolette, quindi l'ultimo pezzo non diventa mai un oggetto valido. Resta però un rifiuto ingiustificato, riprodotto.
- `modules/web/browser.py:183` — validazione dell'esito e motivi presi solo da `_ERRORI_FIGLIO` — rischio: un motivo scritto dalla pagina — **ok**. I test parametrizzati coprono il caso «obbedisci a questo».
- `modules/web/browser.py:164` — env minimo, cwd e HOME temporanei, `start_new_session` — rischio: chiavi di Gas passate al figlio — **ok** (test con GROQ_API_KEY). Nota BASSA (R-593-5): `preexec_fn` gira mentre i thread del proxy sono attivi, e la documentazione di Python lo dice non sicuro con thread attivi. Un eventuale stallo del figlio è comunque limitato dal timeout più killpg, perché setsid avviene prima di preexec_fn. Alternativa: `prlimit` o un wrapper `sh -c 'ulimit …; exec node'`.
- `modules/web/leggi.py:1684` — riprova nel browser solo se il corpo è vuoto e il tipo non è text/plain — rischio: regressione di leggi_pagina — **ok**. `_estrai` più `_incornicia` (`modules/web/leggi.py:1605`) equivalgono al vecchio `_componi`. `_pulisci` toglie i surrogati (categoria Cs): una pagina con emoji tagliata al confine di MAX_USCITA dà un testo che si codifica senza errori (provato). Un errore del browser lascia la pagina vuota. gas.py non è toccato e non importa modules.web: leggi_pagina non è ancora agganciata al kernel.
- `modules/web/proxy.py:266` — `_risposta`, la testa riscritta con «Connection: close» — rischio: risposta doppia o desync verso un altro sito — **ok**. Mutante su un export dell'index (al posto di `_risposta` solo `risposto[0] = True`): `test_risposte_rifiutate` e gli altri test nuovi falliscono. Le intestazioni nominate in Connection e le Proxy-* sono tolte (`modules/web/proxy.py:81`), il «200» del tunnel viene contato (`modules/web/proxy.py:224`). `_pompa` legge solo dopo select, quindi il timeout lasciato da `_testa_risposta` sul socket remoto non pesa (lezione #586 controllata).
- `modules/web/proxy.py:62` e `modules/web/proxy.py:281` — riga di stato e 1xx — **riserva (R-593-4, BASSA)**.
- `.github/workflows/ci.yml:134` — NODE_PATH più GAS_TEST_BROWSER_OBBLIGATORIO nel passo web — rischio: modifiche fuori da quanto autorizzato da M1 — **ok**. Cambia solo l'env di quel passo. Il Chromium è quello del passo della voce, e `PLAYWRIGHT_BROWSERS_PATH` è ricavato da `~/.cache/ms-playwright` quando HOME cambia.

**Riserve**

- **R-593-1 MEDIA, processi orfani (da chiudere prima di accendere GAS_WEB_BROWSER, meglio in questa fetta).** Playwright avvia Chromium «detached», cioè in una sessione sua. Visto con `ps -eo pid,ppid,pgid,sid` durante una lettura: node ha pgid/sid 12856, headless_shell e i suoi figli 12867. Il killpg di `modules/web/browser.py:144` uccide quindi solo node. Dopo «tempo massimo del browser superato», a +0 s e a +0,5 s c'erano ancora 3 processi Chromium con ppid 1. Spariscono da soli entro circa 2 s, ma solo perché Chromium vede chiudersi la pipe di DevTools, non per merito di Gas. Nel frattempo la TemporaryDirectory del profilo viene cancellata mentre Chromium è vivo: se la cancellazione fallisce, l'OSError sostituirebbe il motivo del timeout. Questo l'ho dedotto dal codice, non l'ho osservato: nelle mie prove la cartella è sparita. Tre punti:
  - Il docstring `modules/web/browser.py:14` («uccisione di tutto il gruppo di processi») e il commento di `modules/web/browser.py:172` sono falsi.
  - L'helper `tests/test_unit_web_browser.py:162` cerca «gas-browser-» nel cmdline e vede solo il processo principale: zygote e renderer non ce l'hanno (verificato).
  - `test_tempo_massimo_uccide_tutto` (`tests/test_unit_web_browser.py:252`) passa per la chiusura spontanea di Chromium, non per il kill.

  Correzione proposta: prima di uscire dalla TemporaryDirectory, uccidere anche i processi il cui `/proc/<pid>/environ` contiene `TMPDIR=<casa>`, e il loro gruppo. Oppure un PID namespace (`unshare --pid --fork --kill-child`, o bwrap del punto 4 con `--unshare-pid --die-with-parent`). Il test dovrebbe cercare per ambiente e controllare subito dopo il ritorno, senza sleep.
- **R-593-2 BASSA.** `modules/web/browser.py:173` usa `splitlines()`, che in Python spezza anche su U+2028, U+2029 e U+0085, caratteri che JSON.stringify lascia nudi. Riprodotto: una pagina con U+2028 nel titolo o nel testo, o con U+0085 nel testo, finisce in `{"ok": False, "motivo": "risposta del browser non valida"}`. Correzione: `uscita.split(b"\n")`.
- **R-593-3 BASSA.** Il proxy non toglie «X-Gas-Proxy» dalle risposte dei server. Riprodotto: arriva al browser invariato, e un sito può far dire «pagina rifiutata dal proxy» alla sua pagina. Su https non si può togliere, quindi va almeno dichiarato; su http va tolto in `_risposta`.
- **R-593-4 BASSA.** `_RIGA_STATO` accetta da 000 a 099, e `modules/web/proxy.py:281` le tratta come 1xx. Riprodotto: «HTTP/1.1 099» viene inoltrata come risposta intermedia. Vanno accettate solo 100-599 e il resto deve dare «risposta del server non valida».
- **R-593-6 BASSA.** Nel browser la regola «redirect da https a http non permesso» di leggi_pagina non vale: il proxy giudica ogni richiesta da sola, e il browser riscarica la pagina, quindi il server può rispondere diversamente. Va dichiarato tra i limiti, insieme a «il proxy filtra le destinazioni, non i dati».
- **Nota BASSA.** Il proxy rifiuta tutta la pagina se il server manda un'intestazione con uno spazio prima dei due punti (riprodotto con «Server : x»). È rigido; non ho verificato se Chromium la tollererebbe.
- **COSMETICA.** Il conteggio dichiarato «web 728 passed, 2 skipped» non torna: io ho 727 passed e 2 skipped su 729 raccolti, con node, playwright e GAS_TEST_BROWSER_OBBLIGATORIO=1.

**Onestà del caso «seconda risposta».** Confermo quanto dichiarato: il test browser non morde il mutante; lo morde il test unitario del proxy.

**Prove eseguite**

- Test del browser: 23 passed. Web completo: 727 passed, 2 skipped.
- Mutante su `_risposta`: preso.
- Sonde con Chromium vero (headless_shell 1194, playwright in /opt/node-tools): loopback, iframe, file://, U+2028, U+0085, surrogati, busy loop, gruppi di processi.
- Sonde con socket grezzi sul proxy: 099, X-Gas-Proxy, «Connection: content-length», «Server : x».
- `git diff --check` pulito. Nessuno slicing della history e nessuna simulazione di tool: il diff non tocca gas.py, `_get_window`, il cap 10 o il cap 8k.

**Coerenza col piano e con §9.** Punti 1, 3, 5, 6 e 7 presenti, spento per default, gas.py non toccato. Il punto 4 (bwrap) è dichiarato come limite in `modules/web/browser.py:20-23`. Ogni eccezione è intercettata, e leggi_con_browser logga un warning su gas.web. Robustezza prima della potenza: rispettata. L'unica garanzia che non regge è l'uccisione dei processi (R-593-1).

**Rischi esplicitamente esclusi**

- Fughe DNS di Chromium (prefetch o resolver con il proxy attivo): non osservabili con DNS e connettore finti, non verificate.
- Run della CI non eseguita: il passo web col Chromium del passo voce l'ho verificato solo leggendo lo YAML.
- Comportamento sul VPS e sul Mac non provato (sul Mac `attivo()` è falso, perché sys.platform non è linux).
- Exploit di Chromium senza sandbox: limite dichiarato, fuori dallo scopo.

File rilevanti: /home/user/Gas/modules/web/browser.py, /home/user/Gas/modules/web/proxy.py, /home/user/Gas/modules/web/leggi.py, /home/user/Gas/tests/test_unit_web_browser.py, /home/user/Gas/tests/test_unit_web_proxy.py, /home/user/Gas/.github/workflows/ci.yml, /home/user/Gas/.claude/agents/memoria_revisore.md. Le sonde sono in /tmp/sonde593/ (sonda.py, gruppi.py, cmd.py, px.py, loop.py).
```

Verdetto integrale della review #594 (chat Mani), dopo le correzioni della #593:

```
## VERDETTO: APPROVATO CON RISERVE

Review #594 (chat Mani). Ri-review della #593, fetta 33, browser senza schermo. Diff staged sha256 74ca71a1… (non è cambiato durante la review), base 01eba0d, branch claude/peaceful-lovelace-0w2b7q. Prima della review ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md e la mia memoria.

**Elementi del diff esaminati**

1. `modules/web/browser.py:179` — `_uccidi_tutti`: uccide il gruppo di node e i gruppi di ogni processo vivo che ha il segno, e ripete fino a 100 giri da 20 ms.
   - Rischio esaminato: un Chromium che resta vivo dopo il tempo massimo (R-593-1).
   - Esito: ok.
   - Prove fatte:
     - Ho fotografato con /proc i processi durante una lettura. node ha un gruppo suo. Il Chromium principale ha il segno e un gruppo suo. Zygote e renderer non hanno il segno ma stanno nel gruppo del principale. Quindi nessun processo di Chromium resta fuori.
     - 12 letture con tempo massimo da 1,2 a 2,4 s, poi 60 tempi massimi precoci (da 0,15 a 0,87 s, durante l'avvio di node e Chromium, dove la corsa fork/setsid è più probabile): sempre 0 processi vivi. L'uccisione dura 25–50 ms (2–3 giri). Il secondo passaggio nel `finally` dura 1–3 ms.
     - Ho ucciso a mano solo il Chromium principale a metà lettura: la risposta è «pagina non caricata» e non resta nessun orfano, né subito né fino a 4 s dopo.
     - Chromium non tiene aperto lo stdout di node (ha socket suoi). Quindi `proc.communicate()` senza tempo, a `modules/web/browser.py:221`, non può restare appeso per colpa sua.

2. `modules/web/browser.py:187` — il controllo `g != mio` e la raccolta dei gruppi col segno.
   - Rischio esaminato: un killpg sul gruppo di Gas stesso.
   - Esito: ok.
   - Prova: ho dato il segno all'ambiente del processo di prova e lanciato un figlio segnato nel suo stesso gruppo. Dopo `_uccidi_tutti` sono vivi tutti e due.
   - Il gruppo `proc.pid` è sempre diverso da quello di Gas grazie a `start_new_session=True`.

3. `modules/web/browser.py:226` — le righe si separano solo su `"\n"` (R-593-2).
   - Esito: ok. Il mutante con `splitlines` fa fallire `tests/test_unit_web_browser.py:205`. `JSON.stringify` scrive `\n` e `\r` come escape, quindi l'unico a capo vero è il separatore.

4. `modules/web/browser.py:146` — `_AVVIO` con ulimit al posto di preexec_fn (R-593-5).
   - Esito: ok. In /proc/<pid>/limits node e ognuno dei 6 headless_shell hanno 2147483648 byte di dati. `/bin/sh` qui è dash. Se ulimit fallisce, sh esce senza output e la risposta è «risposta del browser non valida»: fail-safe.

5. `modules/web/proxy.py:58` — `x-gas-proxy` è tra le intestazioni tolte dalle risposte (R-593-3), e `modules/web/proxy.py:62` — `_RIGA_STATO` accetta solo 100–599 (R-593-4).
   - Esito: ok. I test `tests/test_unit_web_proxy.py:475` e `tests/test_unit_web_proxy.py:498` (099 seguito da 200, e 600) passano.
   - Il caso https e la pagina riscaricata (R-593-6) sono dichiarati nel docstring di `modules/web/browser.py:28`.

6. `tests/test_unit_web_browser.py:267` — `test_tempo_massimo_uccide_tutto`.
   - Esito: **riserva** (vedi R-594-1).

Wall of Shame: nessuno slicing della history (`righe[-1]` e i `[:…]` sono su stringhe e liste di output, non sulla cronologia). Nessuna simulazione dell'output dei tool: i test fingono solo DNS e connessioni. Cap a 10 iterazioni e `_get_window` non toccati.

**Prove eseguite**
- Browser + proxy: 95 passed.
- Suite web, sia nel repo sia su un export dell'indice: **731 passed, 2 skipped (733 raccolti)**. Il report dice 732: va corretto.

**Riserve (da tracciare in stato_progetto.md)**
- **R-594-1 (BASSA)**: il mutante «senza i gruppi del segno» (riga 187 tolta) fa fallire `tests/test_unit_web_browser.py:267` solo **1 volta su 6**. Senza il fix gli orfani di Chromium muoiono quasi sempre da soli, quando si chiude la pipe, prima del controllo. Quindi la frase «il mutante fa fallire il test» è imprecisa e la guardia contro la regressione è debole.
  - Correzione suggerita, già provata: un test diretto di `_uccidi_tutti` con `Popen(["sh","-c","setsid sleep 30 & exec sleep 30"], env=<con il segno>, start_new_session=True)`. Col fix non sopravvive nessuno; col mutante resta sempre 1 processo.
- **R-594-2 (BASSA, da dichiarare)**: l'uccisione trova i processi solo dal segno o dal gruppo di un processo segnato. Un processo che cambia sia gruppo sia ambiente sfugge: per esempio un renderer compromesso, che è già nel limite dichiarato «niente sandbox né bwrap, da non accendere sul VPS».
  - La corsa sui pid riusati è trascurabile: servirebbe un giro completo dei pid tra la scansione e il killpg (≤20 ms). Qui pid_max è 32768; sul VPS di solito è 4194304.
- **R-594-3 (COSMETICA)**:
  - Conteggio della suite web: 731, non 732.
  - Il docstring di `modules/web/leggi.py` dice «con i suoi TEMPO_MAX s in più». Nel caso peggiore al tempo massimo si aggiungono fino a circa 4 s (due chiamate da 100×20 ms); misurati 25–50 ms.
  - Il rifiuto rigido di «Server : x» va dichiarato nei report, come hai detto.

**Rischi esplicitamente esclusi**
- Comportamento sul VPS con systemd come PID 1 (gli zombie vengono raccolti e i pid si liberano davvero): non riproducibile qui, dove il PID 1 non raccoglie gli zombie.
- Comportamento con un `sh` diverso da dash/bash/busybox: non verificato.
- Più letture del browser in parallelo da thread diversi: non provate. In teoria i segni sono distinti, perché la cartella temporanea è unica.

**Memoria**: riga #594 e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate con lo script (7649991, solo quel file; il diff staged non è cambiato). Lezione: un mutante «preso» da un test end-to-end con processi e tempi va rilanciato più volte, e serve un test diretto con un processo che non muore da solo.

File di prova, fuori dal repo: /tmp/sonda593/ (sonda1–7.py e i mutanti m1.py, m2.py; copia dell'indice in /tmp/sonda593/copia).
```

Verdetto integrale della review #595 (chat Mani), sul diff finale del commit 1895d7c:

```
## VERDETTO: APPROVATO CON RISERVE

Review **#595** (chat Mani). È la ri-review della #594 sulla fetta 33 (browser senza schermo). Diff staged sha256 1f0c493f, base 01eba0d, branch claude/peaceful-lovelace-0w2b7q, `git diff --staged --check` pulito.

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 9, 10), reports/stato_progetto.md (letto per parti), .claude/agents/memoria_revisore.md (coda e lezioni #593/#594).

**Elementi del diff esaminati**

1. `tests/test_unit_web_browser.py:276` — test nuovo `test_uccidi_tutti_prende_chi_cambia_sessione`.
   - Cosa fa: lancia `sh -c "setsid sleep 30 & exec sleep 30"` con il segno nell'ambiente e `start_new_session`, chiama `_uccidi_tutti`, poi controlla che non resti vivo nessun processo col segno. Il controllo rifà la ricerca da zero, quindi non si fida dei gruppi calcolati dalla funzione.
   - Rischio esaminato: se il test prende davvero il mutante, e se è fragile.
   - Prove: 5 volte su 5 passa. Mutante senza la riga dei gruppi del segno (su una copia esportata dell'indice): 3 failed su 3.
   - Corsa sui tempi: se `setsid` non è ancora partito entro 0,3 s, il processo è ancora nel gruppo di `proc.pid`. In quel caso il test passa comunque: diventa solo una guardia più debole, non un test che fallisce a caso.
   - Esito: ok.

2. Stesso test, rischio di uccidere processi estranei.
   - Il segno è unico per ogni pid di pytest (`/tmp/gas-browser-prova-<pid>`) e il confronto è esatto sulla voce d'ambiente (`split(b"\0")`).
   - Il gruppo di pytest è escluso (`g != mio`) e i due `sleep` non stanno in gruppi di altri.
   - Dopo la suite web completa: 0 processi `gas-browser-` o `sleep 30` vivi.
   - Esito: ok.

3. `tests/test_unit_web_browser.py:288` — il `finally` del test chiama `proc.kill()` e `proc.wait()`.
   - Rischio esaminato: processi lasciati in giro se il test fallisce.
   - Prova: col mutante, dopo ognuno dei 3 fallimenti è rimasto un `sleep 30` orfano (ppid 1, sessione sua, `ps` mostra pid 830/845/860 che si accumulano). Teneva lo stdout e lo stderr della cattura di pytest (file temporanei, non la pipe del runner). Li ho uccisi a mano.
   - Esito: **riserva R-595-1**.

4. `modules/web/leggi.py:39` — il docstring ora dice anche il costo dell'uccisione dei processi («decine di millisecondi, al più circa 4 s»).
   - Prova: misurato circa 0,9 ms a giro con 79 processi. Il tetto è 100 giri da 20 ms più la scansione, cioè circa 2–3 s anche con molti processi. Per una singola chiamata la frase è corretta.
   - Esito: ok, con la nota di R-595-2.

5. Contesto: `modules/web/browser.py:187` (la riga dei gruppi del segno, invariata dalla #594) e `modules/web/browser.py:220` / `modules/web/browser.py:224`.
   - Nel caso del tempo massimo `_uccidi_tutti` viene chiamata due volte (nell'`except` e nel `finally`). Di solito la seconda chiamata esce subito.
   - Esito: riserva R-595-2.

**Test**: web con il comando della CI (`python -m pytest tests/test_unit_web_*.py`) dà **732 passed, 2 skipped**, cioè 734 test raccolti, con node e playwright presenti. Non è 733+2: il totale di 735 torna solo con `-k web` su tutto `tests/`, che aggiunge `test_unit_gate.py::test_sembra_delicato[dati/l.webloc-True]`. Nei report va scritto il numero giusto insieme al comando usato.

**Riserve (da tracciare in stato_progetto.md)**

- **R-595-1 BASSA**: se il test fallisce, il `finally` in `tests/test_unit_web_browser.py:288` uccide solo `proc.pid`. Il `sleep 30` nella sua sessione resta orfano fino a 30 s (riprodotto 3 volte su 3). Correzione: nel `finally` pulire per segno con un meccanismo che non dipende dalla funzione sotto test, per esempio `for pid in br._vivi(): if br._col_segno(pid, s): os.kill(pid, SIGKILL)`, poi `proc.wait()`.
- **R-595-2 BASSA (solo docstring)**: nel caso patologico di processi che non si lasciano uccidere, le due chiamate in `modules/web/browser.py:220` e `modules/web/browser.py:224` si sommano, fino a circa 8 s. Basta dichiararlo nel docstring oppure saltare la seconda chiamata dopo la prima.
- **BASSA, solo nei report**: il conteggio «733 passed, 2 skipped» va corretto come spiegato sopra.
- R-594-2 (processo che cambia sia gruppo sia ambiente) e il rifiuto rigido di «Server : x»: va bene dichiararli nei report, come hai proposto.

Il test diretto si salta insieme al modulo quando manca il browser, anche se a lui il browser non serve. In CI però è obbligatorio (`GAS_TEST_BROWSER_OBBLIGATORIO=1`), quindi va bene: è una nota cosmetica.

Wall of Shame: nessuno slicing della history, nessuna simulazione di tool. Il ciclo da 10 iterazioni, `_get_window` e il tetto di 8k non sono toccati.

**Rischio escluso**: non ho verificato in modo meccanico che il resto del diff (proxy.py, ci.yml, il resto di browser.py e leggi.py) sia identico a quello della #594 (sha 74ca71a1). Non ho una copia del diff della #594 da confrontare, quindi mi sono fidato del delta dichiarato e ho riletto solo `_uccidi_tutti` ed `_esegui`. Non ho verificato nemmeno il comportamento su VPS o in CI con il carico vero: qui non si può riprodurre.

**Memoria**: aggiunte in `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga #595 e una lezione nuova: il `finally` di un test su una funzione di pulizia non deve affidarsi alla stessa funzione né al solo `proc.kill()` del padre. Committata con `scripts/commit_memoria_revisore.sh` (ce68d35). L'indice staged è intatto: 7 file, 896+/25-.

File rilevanti: `/home/user/Gas/tests/test_unit_web_browser.py`, `/home/user/Gas/modules/web/browser.py`, `/home/user/Gas/modules/web/leggi.py`, `/home/user/Gas/.claude/agents/memoria_revisore.md`.
```

Merge di origin/main 9fdbd2b (entrano modules/voice/server.py, tests/test_unit_voice_stt.py e i report di M2). Verdetto integrale della review #596 (chat Mani):

```
## VERDETTO: APPROVATO CON RISERVE

Review **#596 (chat Mani)**: merge di origin/main 9fdbd2b (PR #314 M2, voce V5) nel branch claude/peaceful-lovelace-0w2b7q (fetta 33, HEAD 1895d7c, base 01eba0d). Il merge non è ancora committato. Ho letto, nell'ordine richiesto, CLAUDE.md (§5, §8, §10), reports/stato_progetto.md (solo le parti che servono) e .claude/agents/memoria_revisore.md.

**Cosa ho verificato**
- **Indice contro MERGE_HEAD**: cambiano solo i file della fetta 33, cioè modules/web/browser.py, modules/web/leggi.py, modules/web/proxy.py, i 3 test web, .github/workflows/ci.yml e la memoria (+6 righe). Ognuno è identico a HEAD. Ho confrontato i blob uno per uno.
- **Indice contro HEAD**: cambiano solo i file di main, cioè modules/voice/server.py, tests/test_unit_voice_stt.py, reports/prova_voce_mac.md (nuovo), stato (+2/-1), i 3 log di sessione e la memoria (+4). Ognuno è identico a MERGE_HEAD.
- **Nessuna riga persa in stato e nei log di sessione**: base..HEAD non tocca né stato_progetto.md né handoff, ultimo_report e diff_sessione. Prendere la versione di main quindi non scarta niente del branch. Nello stato c'è solo il delta di main: la voce V4 con R-581-2-M2 barrata e la nuova voce V5.
- **Memoria**: la versione nell'indice è la base intera (1069 righe), poi il blocco del branch (#593–#595 con le 3 lezioni, identico alle ultime 6 righe di HEAD), poi il blocco di main (#585-M2–#587-M2 con 1 lezione, identico alle ultime 4 righe di MERGE_HEAD). In tutto 1079 righe = 1069+6+4, 0 righe tolte da entrambi i lati. Correzione minore alla tua descrizione: la #592 era già nella base, non arriva dal conflitto.
- **Marcatori e --check**: nessun marcatore di conflitto nei file dell'indice, `git diff --staged --check` pulito (rc 0), `git ls-files -u` vuoto.
- **Test su un export dell'indice** (git checkout-index in una cartella temporanea): `pytest tests/test_unit_web_*.py tests/test_unit_voice_*.py` dà **870 passed, 2 skipped**, uguale al tuo numero.

**Elementi del diff esaminati**
- `modules/voice/server.py:414` — il tetto orario registra il turno subito prima di `transcribe_audio`. Rischio esaminato: che con l'unione la riga si perda o finisca in un'altra posizione. Esito: **ok**, blob uguale a MERGE_HEAD; è il codice già approvato nelle review #586-M2 e #587-M2.
- `tests/test_unit_voice_stt.py:408` — test V5: anche «uso» e le trascrizioni vuote contano per il tetto. Rischio esaminato: test V5 presente ma non eseguito dalla CI del branch, che arriva da HEAD. Esito: **ok**, il comando della CI su `.github/workflows/ci.yml:125` include tests/test_unit_voice_stt.py.
- `.github/workflows/ci.yml:137` — suite web con `GAS_TEST_BROWSER_OBBLIGATORIO=1`. Rischio esaminato: conflitto nascosto con il passo Playwright della voce, che main poteva aver cambiato. Esito: **ok**, base..MERGE_HEAD non tocca ci.yml, quindi il file è quello del branch già revisionato.
- `modules/web/browser.py:187` — uccisione dei gruppi dei processi col segno (chiude R-593-1). Rischio esaminato: regressione portata dal merge. Esito: **ok**, blob uguale a HEAD (review #594 e #595).

**Riserve**
- **R-596-1 BASSA**: le riserve ancora aperte della fetta 33 non sono in reports/stato_progetto.md: R-594-2 (limite da dichiarare), R-595-1 (il cleanup del test lascia un orfano) e R-595-2 (doppia `_uccidi_tutti`, circa 8 s). La riga 4 dello stato è ancora ferma alla fetta 32. La regola del gate vuole le riserve tracciate nello stato: vanno aggiunte con i log di fine task, prima di aprire la PR.

**Cosa NON ho verificato**
- Suite del kernel (gas.py) e degli hook: non le ho lanciate, perché il merge non tocca gas.py, i brains né la macchina di controllo. Stessa impostazione delle review #588 e #592.
- Contenuto dei 3 log di sessione: sono quelli di main e tu li riscrivi a fine task, quindi andranno controllati nella prossima review o nell'handoff.
- Pagina della voce nel browser con Chromium obbligatorio: non l'ho rilanciata a parte. I test del browser web, che ci sono nel giro da 870, sono passati nell'ambiente; la parte della voce è invariata rispetto a main.

**Memoria**
La riga #596 è in coda a /home/user/Gas/.claude/agents/memoria_revisore.md ma è FUORI dallo stage: ho controllato che l'indice sia rimasto a 8 file, +216/-362. Non ho eseguito `commit_memoria_revisore.sh`, perché con il merge in corso un `commit -o` lo concluderebbe con un indice parziale. Va aggiunta allo stage o committata dopo il commit di merge. Nessuna lezione nuova.
```

Commit b64a54e (tests/test_unit_web_browser.py: marcatore del gate IP). Verdetto integrale della review #597 (chat Mani); unico ritocco, per il gate IP: l'indirizzo «tutti zeri» e l'IP privato di esempio del test sono scritti <IP-redatto>:

```
## VERDETTO: APPROVATO

Review #597 (chat Mani). Delta minimo sulla fetta 33 (PR #315, branch claude/peaceful-lovelace-0w2b7q). Il diff staged contiene solo marcatori gasmerge-ip-ok.

Elementi esaminati:
- `tests/test_unit_web_browser.py:48`. Cosa fa: aggiunge un commento JS `//` in coda a `fetch('http://<IP-redatto>/privato').catch(() => {});`, dentro la pagina finta `/fughe` del dizionario `PAGINE`. Rischio esaminato: che il comportamento del test cambi o che il literal `b"""..."""` si rompa. Il commento sta dopo il `;` e arriva fino a fine riga, quindi la fetch resta eseguita com'era. Il testo aggiunto è solo ASCII, quindi il bytes literal resta valido. Nessun test cerca «privato» o il testo della pagina (grep: l'unica occorrenza è la riga 48). È lo stesso marcatore già usato in `tests/test_unit_web_browser.py:20` e `tests/test_unit_web_browser.py:139`. Rilanciato tutto il file: 25 passed. Esito: ok.
- `.claude/agents/memoria_revisore.md:1070`. Cosa fa: aggiunge una nota tra parentesi in coda alla riga #593. Rischio esaminato: che il registro storico venga alterato. Il testo della review resta identico, la riga inizia ancora con `#593` e il contatore non cambia. Esito: ok.
- Contesto, `scripts/fine_task_finale.sh:73`. Ho simulato il gate IP (passi 73-110: regex, `--not -e gasmerge-ip-ok`, filtro loopback per riga) sul tree dell'indice (`git write-tree`). La riga 48 del test e la riga #593 non risultano più. Restano solo 3 righe di `reports/handoff.md` (versione nell'indice, che è quella di HEAD) con <IP-redatto>. È la redazione `<IP-redatto>` che hai dichiarato e che va fatta prima del commit, altrimenti il gate si ferma di nuovo. Esito: ok, con questo passo ancora da fare.

Rischio escluso: non ho verificato la redazione nell'handoff né la dichiarazione nel §4, perché non sono nel diff staged (reports/ è fuori dal perimetro di review). Non ho rilanciato il resto della suite web: il delta tocca solo un commento.

Nota operativa: lo script ha già committato la memoria (`1db489f`, riga #597, che include anche la nota sulla #593). Ora nello stage resta solo `tests/test_unit_web_browser.py`, quindi lo SHA del diff staged è cambiato. Prima del commit devi rilanciare `bash scripts/segna_review_ok.sh`.

File rilevanti: /home/user/Gas/tests/test_unit_web_browser.py, /home/user/Gas/.claude/agents/memoria_revisore.md, /home/user/Gas/reports/handoff.md
```

Commit 7363702 (modules/web/browser.py, tests/test_unit_web_browser.py: solo docstring e commento, V-1 ve/bot #315). Verdetto integrale della review #598 (chat Mani):

```
## VERDETTO: APPROVATO CON RISERVE

Review #598 (chat Mani), delta di soli commenti sulla fetta 33 (PR #315), diff staged.

Ho letto prima: CLAUDE.md (sezione 5 e guardrail), reports/stato_progetto.md (in modo mirato), la mia memoria.

**Cosa ho controllato nel diff**
- `modules/web/browser.py:11` — il docstring adesso dice che WebSocket e il resto sono spenti «nelle pagine e nei frame» e NON nei Dedicated Worker, e che un wss:// partito da un worker passa dal tunnel 443. Rischio: che la frase sia falsa. Esito: ok. `addInitScript` (`modules/web/browser.py:105`) vale per pagine e frame, non per i worker. `routeWebSocket` (`modules/web/browser.py:106`) è nel contesto e i worker non li copre. SharedWorker e service worker sono spenti a parte (`modules/web/browser.py:86` e `modules/web/browser.py:103`). Il tunnel verso la 443 che lascia passare tutto è già un limite dichiarato in `modules/web/proxy.py:25`. Le righe cambiate stanno dentro il docstring del modulo, che si apre alla riga 1: il comportamento non cambia.
- `tests/test_unit_web_browser.py:222` — il commento dice che il ws:// del worker lo ferma il proxy «(porta 80, Upgrade)». Rischio: che il commento indichi il meccanismo sbagliato. Esito: riserva. Ho lanciato il test col log del proxy (`pytest -k fughe -o log_cli=true --log-cli-level=DEBUG`): il ws:// del worker viene rifiutato con «tunnel solo verso la porta 443». Chromium manda i WebSocket attraverso il proxy sempre con CONNECT (qui `sito.test:80`), quindi a fermarlo è il controllo CONNECT di `modules/web/proxy.py:216`, non il controllo Upgrade di `modules/web/proxy.py:179`. «Porta 80» è giusto, «Upgrade» no.
- `tests/test_unit_web_browser.py:225` — le asserzioni non sono cambiate. Ho controllato con grep che il diff abbia solo righe di docstring e di commento. `test_fughe_bloccate`: 1 passed, rilanciato da me.

**Riserve**
- R-598-1 COSMETICA: in `tests/test_unit_web_browser.py:222` sostituire «(porta 80, Upgrade)» con, per esempio, «(CONNECT verso la porta 80: tunnel solo verso la 443)». Si può fare insieme alla fetta bwrap, va tracciata in reports/stato_progetto.md.

**Cosa non ho verificato**
- Non ho rifatto la prova del wss:// da un worker verso la 443. La parte del docstring che lo dichiara si basa sulla riproduzione della verifica esterna (V-1 #315) e sul limite del tunnel già scritto nel proxy. Anche il comportamento con altre versioni di Chromium e Playwright non l'ho verificato: in questo ambiente ce n'è una sola.

**Memoria**
- Ho scritto la riga #598 e una lezione: per capire quale controllo ferma una richiesta, leggere il motivo del rifiuto nel log del proxy, perché i WebSocket passano sempre in CONNECT. È committata in a196b6b (`/home/user/Gas/.claude/agents/memoria_revisore.md`) da sola. Lo stage resta intatto: `modules/web/browser.py` e `tests/test_unit_web_browser.py`.
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. Nuovo `tests/test_unit_web_browser.py`: 25 test (saltati senza node+playwright, obbligatori in CI). `tests/test_unit_web_proxy.py`: da 55 a 71 test. `tests/test_unit_web_leggi.py`: il patch di un test passa da `_componi` a `_estrai`. Web con il comando della CI (`python -m pytest tests/test_unit_web_*.py`), node e playwright presenti: 732 passed, 2 skipped. Web + voce sull'albero unito con main 9fdbd2b: 870 passed, 2 skipped. Mutanti presi: senza `<-loopback>`, senza lo script che spegne WebSocket/RTC, senza il controllo X-Gas-Proxy, senza `.split("\n")`, senza i gruppi col segno (test diretto, 3 su 3). Mutante NON preso dal test con Chromium: senza la riscrittura della risposta (Chromium qui non riusa la connessione); lo prende il test unitario del proxy.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- bf07949, 7649991, ce68d35 (memoria del revisore), 1895d7c (fetta 33): pushati insieme; nessuna run su questi SHA prima dell'apertura della PR (push di un branch senza PR aperta: la CI parte sulla PR).
- d313fad (merge di main 9fdbd2b), 713f59f (memoria #596): pushati prima dell'apertura della PR #315; run non ancora disponibile alla scrittura dell'handoff.
- 6ed1741 (primo fine-task, fermato dal gate IP), 1db489f (memoria #597), b64a54e (test), fc91022 (fine-task): pushati insieme; run 41223882452 su fc91022 success (unit-suite con il passo web a browser obbligatorio, handoff-check); `verifica-bot` neutral. I commit intermedi non hanno una run propria.
- d313fad e 713f59f: nessuna run su questi SHA (pushati prima dell'apertura della PR; l'albero è contenuto in fc91022).
- a196b6b (memoria #598), 7363702 (docstring V-1) e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- V-1 ve/bot #315 BASSA (fetta bwrap): WebSocket non spenti nei Dedicated Worker; wss:// verso un host pubblico passa dal tunnel 443 (dentro il limite «filtra le destinazioni, non i dati»); routeWebSocket non provato da nessun test e saltato in silenzio se manca.
- R-598-1 (chat Mani) COSMETICA (fetta bwrap): commento di `test_fughe_bloccate` dice «Upgrade», a fermare il ws:// è il controllo CONNECT.
- R-594-2 (chat Mani) BASSA: l'uccisione non trova un processo che cambia sia gruppo sia ambiente (per esempio un renderer compromesso; rientra nel limite «senza sandbox»).
- R-595-1 (chat Mani) BASSA: se `test_uccidi_tutti_prende_chi_cambia_sessione` fallisce, resta un `sleep 30` orfano fino a 30 s.
- R-595-2 (chat Mani) BASSA: nel caso patologico le due chiamate di `_uccidi_tutti` (except e finally) arrivano a circa 8 s.
- Nota BASSA (review #593): un'intestazione di risposta con uno spazio prima dei due punti («Server : x») fa rifiutare la pagina dal proxy; rigido, non un bypass.
- Limiti dichiarati del browser: Chromium senza sandbox né bwrap (da non accendere sul VPS prima del punto 4); il proxy filtra le destinazioni, non i dati; niente regola https→http e pagina riscaricata (R-593-6); X-Gas-Proxy dentro i tunnel https non si toglie (R-593-3); fughe DNS di Chromium non verificate (DNS finto nei test).
- V-1 bot #309 BASSA (limite): verdetto che cita alla lettera un caso di prova di credenziale spezzata non pubblicato.
- R-582-1 BASSA, R-582-2 COSMETICA, R-580-2 BASSA (limiti del bot); V-1/V-2 bot e ve #306.
- R-572-1, R-572-2, R-575-1 BASSE e R-575-2 COSMETICA (chat Mani), preesistenti.
- (b) libexpat ≥ 2.4 nel doctor: con M1.
- V-3 ve #303 BASSA: selectolax 1.0.2 uscita il 2026-10-22, da decidere dall'operatore prima del `pip install` sul VPS.
- R-518-1, R-516-1, R-ve277-5, V-1 ve/bot #288, V-2/V-3 ve #296, R-546-1: BASSE della chat Mani, invariate.
