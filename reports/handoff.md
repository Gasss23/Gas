# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-30/31 — Mani, fetta 32 (R6): proxy filtrante per il browser senza schermo (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. La PR era in conflitto con main dopo la #313 (voce V4): main portato nel branch (826a9b1, review #592 APPROVATO), quindi CI e bot ripartono su questo commit. L'operatore ha detto «mergia #312» (riferito da M1, che fa il merge appena la CI è verde). Merge della PR #312 (https://github.com/Gasss23/Gas/pull/312). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5088535610","url":"https://github.com/Gasss23/Gas/pull/312"}`), perché `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve il sì dell'operatore, anche tramite M1.
2. Fetta di SICUREZZA: secondo passaggio indipendente nella chat claude.ai col link della PR.

---

## §1 SCOPE & ESITO FETTE

- **PR #310**: `FATTA` — mergiata (15c4da8). V-1 bot #310 BASSA (test https sulla porta 80): `FATTA`.
- **Proxy filtrante** (`modules/web/proxy.py`, prima fetta del browser senza schermo, piano approvato dall'operatore tramite M1): `FATTA` (PR #312).
- **Review #585 (chat Mani)**: BOCCIATO. B-585-1 MEDIA (tunnel verso la 80 con «:80/:443»): `FATTA`. R-585-2, R-585-3, R-585-6: `FATTA`. R-585-4 e R-585-5: `DEFERITA — fetta del browser`.
- **Review #586**: APPROVATO CON RISERVE. R-586-1 BASSA (timeout della testa rimasto sul tunnel): `FATTA`. **Review #587**: APPROVATO.
- **Verifica esterna su 6ebecba (https://github.com/Gasss23/Gas/pull/312#issuecomment-6529640125)**: APPROVATO CON RISERVE, nessun bypass dei filtri. V-1 BASSA (§6 diceva «nessuna run»: c'era la run 41100200600 su 07ea587, con handoff-check rosso intermedio): `FATTA` — §6 corretto qui. V-2 BASSA (PR in conflitto con main dopo #311): `FATTA` — merge di main 1e8aff8, review #588. V-3 BASSA (client muto tenuto 10 s invece della scadenza del proxy, mutante sopravvissuto): `FATTA` — test nuovo, review #589. V-4 COSMETICA (controllo `porta != 443` irraggiungibile, difesa in profondità): `SALTATA — voluto`.
- **Check `smista` del bot su 6ebecba**: failure, con la PR in conflitto con main; superato dal merge di main.
- **Merge di origin/main 1e8aff8 (PR #311 di M2, voce V3)**: `FATTA` — conflitti solo nei report e nella memoria. Review #588 (chat Mani) APPROVATO CON RISERVE (R-588-1: conteggi dell'handoff, rifatti qui). Review #589 APPROVATO (test V-3).
- **Bot su eea0ea0 (PR #312)**: APPROVATO CON RISERVE, check success. V-1 BASSA (a tetto dei byte superato, una richiesta nuova usciva ancora con URL e intestazioni): `FATTA` in b838f4d. V-2 BASSA (invii con timeout propri, oltre la scadenza del proxy): `FATTA` in b838f4d. V-3 COSMETICA (conteggi dei test nella descrizione): `FATTA` — descrizione e §5 aggiornati. V-4 COSMETICA (hop-by-hop nominati in «Connection» non tolti; non è un bypass): `DEFERITA — registrata`.
- **Review #590 (chat Mani)**: APPROVATO CON RISERVE (R-590-1 COSMETICA motivo del timeout, R-590-2 BASSA testa contata dopo l'apertura): `FATTA` tutte e due. **Review #591**: APPROVATO.
- **Bot su 805b4d8 (PR #312)**: APPROVATO CON RISERVE, check success; CI verde su 805b4d8. V-1 BASSA (CI ancora in corso alla verifica): `FATTA` — poi verde. V-2 COSMETICA (testa del CONNECT e risposta 200 non contate nel tetto dei byte, mentre il docstring dice «nei due versi»): `DEFERITA — registrata`.
- **Merge di origin/main 3a38e75 (PR #313 di M2, voce V4)**: `FATTA` in 826a9b1 — conflitti solo nei log di sessione (tenuta la versione del branch) e nella memoria (unione). Review #592 (chat Mani) APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  11 ++++++++++
 modules/web/proxy.py               | 326 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  17 ++++++++-------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   2 +-
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  35 ++++++++++++++-----------------
 tests/test_unit_web_leggi.py       |  13 ++++++++++++
 tests/test_unit_web_proxy.py       | 411 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: base = merge-base con origin/main = 3a38e75. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
f5f3380 chore(revisore): memoria review #592 — APPROVATO
826a9b1 Merge origin/main (3a38e75, PR #313 di M2) in claude/peaceful-lovelace-0w2b7q (PR #312)
805b4d8 docs(fine-task): PR #312 dopo le note del bot su eea0ea0, review #590/#591
b838f4d fix(web): proxy, a tetto dei byte superato nessuna richiesta esce; invii fino alla scadenza (V-1/V-2 bot #312, chat Mani)
2f84376 chore(revisore): memoria review #591 — APPROVATO
a5c92e4 chore(revisore): memoria review #590 — APPROVATO CON RISERVE
eea0ea0 docs(fine-task): PR #312 dopo la verifica esterna su 6ebecba, merge di main (#311), review #588/#589
d2a10d5 test(web): client muto chiuso alla scadenza del proxy (V-3 verifica esterna #312, chat Mani)
3fe0c43 chore(revisore): memoria review #589 — APPROVATO
eb6c01c Merge origin/main (1e8aff8, PR #311 di M2) in claude/peaceful-lovelace-0w2b7q (PR #312)
6ebecba docs(fine-task): Mani fetta 32, proxy filtrante (PR #312), review #585–#587
07ea587 feat(web): proxy filtrante per il browser senza schermo (R6, fetta 32, chat Mani)
1b0cce6 chore(revisore): memoria review #587 — APPROVATO
87d0777 chore(revisore): memoria review #586 — APPROVATO CON RISERVE
8339cf0 chore(revisore): memoria review #585 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 07ea587 (modules/web/proxy.py, tests/test_unit_web_proxy.py, tests/test_unit_web_leggi.py). Verdetto integrale della review #585 (chat Mani), sulla prima versione:

```
## VERDETTO: BOCCIATO

**Review #585 (chat Mani)**: diff staged su claude/peaceful-lovelace-0w2b7q, R6 fetta 32, proxy filtrante. Prima della review ho letto CLAUDE.md (sezione 5, 8, 9 e roadmap), le parti di reports/stato_progetto.md che riguardano R6 e la memoria del revisore (lezioni su proxy e rete). Ho riprodotto i test web: 679 passed, 2 skipped. Le prove le ho lanciate sul codice in staging (il working tree è uguale all'index), con script nella cartella temporanea della sessione.

### Motivo bloccante
**B-585-1 (MEDIA): la regola «CONNECT solo verso la porta 443» si aggira. L'ho riprodotto.**
- **Dove e perché:** `modules/web/proxy.py:160` controlla la porta sul testo che sta dopo l'ultimo «:». `modules/web/proxy.py:165` però apre il tunnel sulla porta che restituisce `_valida_url`, cioè quella letta da urlsplit: sono due letture diverse dello stesso bersaglio.
- **Prova:** con `CONNECT sito.test:80/:443`, `CONNECT sito.test:80?:443` e `CONNECT sito.test:80#:443` la risposta è `200 Connection established` e il connettore viene chiamato con (IP, 80). Il server dietro risponde dalla porta 80.
- **Effetto:** si apre un tunnel grezzo verso la porta 80 di qualunque host pubblico. Passano quindi anche POST e corpi diretti a server http, cosa che la regola «solo GET e HEAD, niente corpo» sulla porta 80 dovrebbe impedire.
- **Chi può farlo:** un browser non produce questi bersagli, quindi oggi può farlo solo un processo locale. Resta però una regola di sicurezza dichiarata (docstring, `modules/web/proxy.py:9`) che risulta falsa, e il test `tests/test_unit_web_proxy.py:174` («sito.test:80») dà una falsa sicurezza.
- **Correzione (una riga):** dopo `_valida_url`, rifiutare se `porta != 443`, oppure rifiutare «/», «?», «#» nel bersaglio. Aggiungere un test con le tre forme e verificare con il mutante.

### Elementi del diff esaminati
- `modules/web/proxy.py:176` — `_leggi_richiesta`: testa fino a 16 KB, byte dopo la testa rifiutati, nomi delle intestazioni validati, caratteri di controllo nei valori rifiutati. Rischi: smuggling, intestazioni ripiegate, CR/LF. Respinte tutte le prove: `\r` o `\n` nudi nel valore, riga ripiegata (obs-fold), NUL nel nome, `transfer-encoding` in minuscolo, una seconda richiesta nello stesso pacchetto, CR nel bersaglio. Due `Content-Length: 0` passano, ed è innocuo. — **ok**
- `modules/web/proxy.py:203` — `_apri`: il DNS lo risolve il proxy, `indirizzo_interno` controlla tutti gli IP e la connessione va a ips[0]. Rischio: DNS rebinding. Va bene. Le forme strane di CONNECT sono tutte gestite bene: `[fe80::1%25eth0]`, `[::ffff:127.0.0.1]` e `2001:db8::1:443` senza parentesi danno 403; `SITO.TEST.` e `:0443` vanno su sito.test:443. — **ok**
- `modules/web/proxy.py:233` — `_conta_byte` viene chiamato prima di `sendall`. Rischio: byte oltre il tetto che arrivano lo stesso. Sono contati prima dell'invio; lo conferma il test `tests/test_unit_web_proxy.py:235`. — **ok**
- `modules/web/proxy.py:107` — semaforo non bloccante dentro il thread del gestore, quindi dopo l'accept. Rischio: esaurimento di thread. Con 300 connessioni mute i thread salgono a 19 (16 posti più quelli dei 503, che escono subito) e tornano a 3 alla chiusura. ThreadingTCPServer crea comunque un thread per ogni accept: è accettabile, perché chi riceve il 503 esce subito. — **ok**
- `modules/web/proxy.py:160` — vedi B-585-1. — **blocco**
- `modules/web/proxy.py:181` — la lettura della testa non ha un tetto di durata: ogni `recv` fa ripartire i 10 s. Prova: con durata=1 la connessione era ancora aperta dopo 4,5 s inviando un byte ogni 0,1 s. Il limite teorico è 16 KB × 10 s, e continua anche dopo `ferma()`. — **riserva BASSA (R-585-2)**
- `modules/web/proxy.py:91` — `ferma()` ferma solo il listener: un tunnel già aperto continua a passare dati (provato: «dopo-ferma» rimandato dall'eco) fino alla scadenza della DURATA. — **riserva BASSA (R-585-3)**: la prossima fetta deve chiudere il browser insieme a `ferma()`, oppure `ferma()` deve chiudere le connessioni attive.
- `tests/test_unit_web_leggi.py:379` — `test_https_sulla_porta_80` (V-1 del bot su #310): coerente con `_valida_url`, che accetta lo schema incrociato. — **ok**

### Altre riserve e punti chiesti
- **R-585-4 (BASSA, per la fetta del browser):** la risposta del server passa senza controllo dei confini. Un server ha mandato «ok» seguito da una seconda risposta HTTP completa («EVIL») e il browser l'ha ricevuta così com'era. Non è un problema solo se il browser non riusa una connessione al proxy che ha dati in sospeso: da verificare con Chromium.
- **R-585-5 (BASSA, per la fetta del browser):** il ragionamento sul redirect è corretto (il browser rifà la richiesta e passa di nuovo dal proxy), ma vale solo se TUTTO il traffico del browser passa dal proxy. Chromium con `--proxy-server` salta il proxy per l'indirizzo locale (loopback) senza dirlo. Servono `--proxy-bypass-list=<-loopback>` e lo spegnimento di QUIC, WebRTC e del prefetch DNS.
- **R-585-6 (COSMETICA):** se la testa non arriva entro il tempo, il proxy scrive un warning «errore TimeoutError» e risponde 502, invece di un 403 «connessione inattiva».
- **Limite di progetto da dichiarare:** «solo GET e HEAD, niente corpo» protegge solo l'http in chiaro. Il tunnel verso 443 trasporta qualsiasi cosa verso qualunque host pubblico. Il proxy filtra le destinazioni (contro gli accessi a indirizzi interni), non l'esfiltrazione dei dati: va scritto in stato_progetto.
- **Altri processi locali:** il proxy su 127.0.0.1 è senza autenticazione. La sandbox di `run_command` usa `--unshare-net` (`gas.py:2225`), quindi il suo loopback è separato e non raggiunge il proxy. Gli altri processi dell'host hanno già la rete diretta: nessuna capacità nuova. Su una VPS con più utenti, un altro utente potrebbe usarlo per i 60 s di vita: rischio da dichiarare, basso.
- **select:** su Linux e Mac un descrittore oltre FD_SETSIZE (1024) fa sollevare ValueError, che viene intercettato e diventa un 502. Su Windows `select` funziona sui socket.

### Rischi esclusi (cosa NON ho verificato)
- `select` su Windows e Mac non l'ho eseguito: l'ambiente è solo Linux.
- Il comportamento reale di Chromium (riuso della connessione con dati in sospeso, scavalcamento del loopback): il browser non c'è ancora in questa fetta.
- Rete e DNS veri: tutte le prove usano DNS e connettore finti.
- Il fix di B-585-1 non l'ho provato su una copia: spetta all'agente, con il mutante.

### Memoria
Ho scritto la riga #585 e una lezione nuova: il doppio parsing, cioè un controllo sul testo seguito da un altro parser, si prova con «/», «?» e «#». Committate in 8339cf0 (`/home/user/Gas/.claude/agents/memoria_revisore.md`). Il resto dell'index non è stato toccato.

Script delle prove (riusabili per la ri-review):
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/sonde.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/sonde2.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/sonde3.py
```

Verdetto integrale della review #586 (chat Mani), dopo le correzioni di B-585-1 e R-585-2/3/6:

```
## VERDETTO: APPROVATO CON RISERVE

Ho rifatto la review #586 (chat Mani) sul diff staged, sha256 d5e0ce9d…, provandolo su una copia dell'index: /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/idx. Il motivo di blocco della #585 è risolto: commit consentito, con la riserva R-586-1 da registrare in stato_progetto.

**Parti del diff esaminate**
- `modules/web/proxy.py:180`: rifiuta un bersaglio CONNECT che contiene «/», «?», «#» o «\». Rischio guardato: B-585-1, cioè il controllo fatto sul testo mentre la connessione usa un parser diverso. Ho provato anche altre forme: «sito.test:80:443», «[sito.test:80]:443», «sito.test:80@x:443», «:80;:443», «:80%2f:443», un tab nell'host o prima di «:443», un NUL. Tutte danno 403 e nessuna connessione parte. Con «:0443», le maiuscole e il punto finale il tunnel si apre, ma sempre e solo verso la porta 443. Mutante senza i due controlli: 4 failed, con connessione aperta. Esito: ok.
- `modules/web/proxy.py:186`: dopo `_valida_url` controlla che la porta letta da urlsplit sia 443. Rischio guardato: che sia solo di facciata. urlsplit legge la porta dopo il PRIMO «:», quindi con il controllo del testo e i caratteri vietati nessun input ci arriva. Il mutante che lo toglie sopravvive (49 passed). È difesa in profondità, oggi irraggiungibile. Esito: ok (nota).
- `modules/web/proxy.py:211`: in `_leggi_richiesta` imposta `client.settimeout(rimasto)` prima di ogni recv. Rischio guardato: R-585-2, la testa mandata un byte alla volta. Mutante senza tempo totale: 1 failed. Esito: **riserva**, vedi R-586-1.
- `modules/web/proxy.py:108`: `ferma()` fa lo shutdown di tutte le connessioni registrate. Rischi guardati: socket persi e thread che esplodono. Prova: 10 tunnel aperti più 3 teste a metà, poi `ferma()`. Ritorna in 6 ms, 13 client su 13 ricevono EOF o un rifiuto, `_aperte` resta vuoto, nessuna eccezione nei thread (ho agganciato `threading.excepthook`), nessun file descriptor in più, i thread tornano a 2. Con 30 tunnel, uno su tre col guasto `ConnectionRefused`, non si perde nessun socket. Mutante senza shutdown: 1 failed. Esito: ok.
- `modules/web/proxy.py:248` (in `_apri` la registrazione viene dopo `_connetti`). Rischio guardato: un socket remoto aperto e mai tolto. Fra connect e registrazione c'è solo `settimeout`, che su un socket nuovo non solleva: oggi nessuna strada perde il socket. C'è però una gara se `ferma()` fotografa le connessioni prima che il remoto venga registrato: quel remoto non riceve lo shutdown. Non è un problema, perché `_pompa` esce subito con la scadenza a 0 (`modules/web/proxy.py:258`) e il `finally` lo chiude. Esito: ok.
- `tests/test_unit_web_proxy.py:183`, `tests/test_unit_web_proxy.py:275` e `tests/test_unit_web_proxy.py:295`: sono i test nuovi per B-585-1, R-585-2 e R-585-3. Ognuno fa fallire il mutante corrispondente. Esito: ok.

**Riserva**
- **R-586-1 (BASSA)**, `modules/web/proxy.py:211`: il timeout rimasto dalla lettura della testa non viene ripristinato e vale per tutto il tunnel o il GET. Prova (sonda2.py, percorso sotto): testa mandata a pezzi vicino alla scadenza, timeout rimasto sul client 0,0999 s; il browser si ferma 0,6 s e riceve 2,9 MB su 8. Nel log resta solo «errore TimeoutError», senza motivo in `rifiuti`. Con la testa in un pezzo solo arrivano tutti gli 8 MB. È BASSA perché un browser vero manda la testa subito e tutta insieme. Correzione: `client.settimeout(TIMEOUT_INATTIVITA)` subito dopo il ciclo della testa, più un test che controlli `gettimeout()` o la risposta grande.

**Prove**: proxy 49 passed in tre run di fila, nessun ResourceWarning. Web 686 passed e 2 skipped (con `-k web` sul working tree, che coincide con l'index); tu ne hai contate 685, la differenza viene dalla selezione. Mutanti rifatti su una copia, file ripristinato e verificato con cmp.

**Rischi esclusi**: la gara teorica fra lo shutdown di `ferma()` e la close dello stesso socket in un altro thread, con il numero del file riusato, non l'ho riprodotta perché la finestra è di pochi microsecondi. Non ho verificato il comportamento con un Chromium vero né su VPS: la fetta del browser non esiste ancora.

**Memoria**: riga #586 e una lezione nuova (un timeout messo dentro un ciclo di lettura resta sul socket anche dopo) aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md e committate da sole (87d0777). Lo staging del proxy è intatto.

Sonde in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/s586/sonda.py e /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/s586/sonda2.py.
```

Verdetto integrale della review #587 (chat Mani), sul diff finale del commit 07ea587:

```
## VERDETTO: APPROVATO

Review #587 (chat Mani): R-586-1 è chiusa e il commit è consentito. Ho provato il diff staged (sha256 bf58d7b6…) su una copia dell'index, in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/idx587.

**Parti del diff esaminate**
- `modules/web/proxy.py:219`: `client.settimeout(TIMEOUT_INATTIVITA)` subito dopo il ciclo della testa. Rischio guardato: che sia nel posto sbagliato. La riga sta fuori dal while e prima dei controlli sulla testa, quindi vale sia per il tunnel sia per il GET. Ho rifatto la sonda della #586 (sonda2.py): ora il timeout rimasto sul client è 2.0 (prima 0,0999) e arrivano 8 MB su 8 (prima 2,9 MB). Esito: ok.
- `tests/test_unit_web_proxy.py:295`: il test `test_timeout_della_testa_non_resta_sul_tunnel` legge `gettimeout()` con una spia su `_tunnel` e vuole TIMEOUT_INATTIVITA. Rischio guardato: che non morda. Il mutante senza la riga, rifatto da me su una copia, dà 1 failed. Esito: ok.
- `modules/web/proxy.py:108`: lo shutdown in `ferma()` è invariato. Ho riprovato perché il resto del diff resta lo stesso: 13 client su 13 ricevono EOF o un rifiuto, nessuna eccezione nei thread, nessun file descriptor in più, `_aperte` vuoto. Esito: ok.

Confronto con la #586: fra i due export cambiano solo le due aggiunte qui sopra; `tests/test_unit_web_leggi.py` è identico.

**Prove**: proxy 50 passed in tre run di fila; web 687 passed e 2 skipped.

**Rischio escluso**: il test si regge sul fatto che il tempo rimasto sia strettamente minore di 10 s. Se due letture di monotonic restituissero lo stesso valore, il mutante potrebbe passare per caso; al codice corretto non cambia nulla, quindi non l'ho indagato oltre. Comportamento con un Chromium vero e su VPS non verificato: la fetta del browser non esiste ancora.

**Memoria**: riga #587 («nessuna lezione nuova») aggiunta a /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (1b0cce6). Lo staging del proxy è intatto.
```

Commit eb6c01c (merge di origin/main 1e8aff8: entrano gas.py, clients/voice/*, modules/voice/server.py e i test della voce e del kernel di M2). Verdetto integrale della review #588 (chat Mani):

```
## VERDETTO: APPROVATO CON RISERVE

Review #588 (chat Mani): è il merge di origin/main 1e8aff8 (PR #311, M2, voce V3) nel branch claude/peaceful-lovelace-0w2b7q (PR #312). Il merge è in corso e non è ancora committato.

Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (solo le parti che servivano) e le lezioni sui merge in .claude/agents/memoria_revisore.md (#497, #502, #514, #531, #715).

**Il merge non perde niente**
- L'indice confrontato con MERGE_HEAD (cioè main) differisce solo nei file della fetta 32: proxy.py, i due test web, ripartenza_mani, i report e la memoria.
- L'indice confrontato con HEAD (il tuo branch) differisce solo nei file di main: gas.py, clients/voice/*, modules/voice/server.py, i test della voce e del kernel, roadmap e stato. Le due direzioni sono complementari.
- `git diff --cached --quiet` conferma che modules/web, test_unit_web_proxy e test_unit_web_leggi sono identici a HEAD.
- Con lo stesso controllo, gas.py, clients, modules/voice, i test della voce e del kernel e roadmap.md sono identici a main.
- Memoria: 0 righe tolte rispetto a HEAD e 0 rispetto a main. Le righe #574-M2…#578-M2 stanno fra #582 e #583, la #579-M2 in coda: le righe di entrambi i lati ci sono tutte.
- stato_progetto: 0 righe tolte. Dal lato di main entra solo la riga «Voce V3», che non dice aperto niente di quello che chiude la fetta 32.
- handoff, ultimo_report e diff_sessione sono identici a HEAD.
- Nessun marcatore di conflitto, `git diff --cached --check` pulito.

**Test su una copia esportata dell'indice**
- Web + voce (inclusi lexbor e tts): 815 passed, 2 skipped. Il tuo 791 non comprendeva probabilmente tutti i file.
- Kernel (`python tests/test_unit_kernel.py`): 1062 PASS, 1 FAIL (T31g, GAS_VECTORS). Lo stesso FAIL c'è su una copia di origin/main, quindi esisteva già e il merge non lo introduce.

**Citazioni**
- `modules/web/proxy.py:186` — ricontrolla che la porta del tunnel letta da urlsplit sia 443 — rischio: il merge altera la correzione B-585-1 — ok, identico a HEAD (file uguale per `diff --quiet`).
- `modules/web/proxy.py:219` — rimette `client.settimeout(TIMEOUT_INATTIVITA)` dopo la lettura della testa — rischio: R-586-1 che si riapre col merge — ok, la riga c'è nell'indice.
- `tests/test_unit_web_proxy.py:295` — test con spia su _tunnel per R-586-1 — rischio: test perso o cambiato — ok, presente, e la suite web passa sull'export dell'indice.
- Contesto, file non più nel diff di sessione dopo il merge: in gas.py, riga 4726, `istruzione_turno` di V3 è identico a main.

**Riserve**
- **R-588-1 BASSA (solo report):** il §2 di reports/handoff.md conta ancora le righe sulla base vecchia.
  - Contro origin/main oggi: diff_sessione 14 → 18, ultimo_report 20 → 30, memoria 5 → 6 con la mia riga.
  - La nota «base = merge-base con origin/main = 15c4da8» diventa falsa con il commit di merge: la nuova base sarà 1e8aff8.
  - Il gate check_handoff controlla solo i path, che sono giusti, quindi non blocca niente. Va però corretto prima di chiudere (lezione #502).
  - Nell'handoff non c'è nessuna menzione dell'arrivo di #311 nel branch: conviene una riga.

**Cosa non ho verificato**
- Il comportamento reale della voce V3 nel browser e del proxy con un browser vero: in questa sessione non posso riprodurli. Mi affido alle review M2 #574–#579 e alla mia #587.
- La CI su GitHub non l'ho guardata: il merge non è ancora committato né pushato.

**Memoria**
Ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga «#588 (chat Mani) — 2026-10-30 — APPROVATO CON RISERVE — …», con R-588-1 e «Nessuna lezione nuova».
- Prima ho controllato che il numero #588 non sia usato in nessun ref remoto.
- Non l'ho committata né messa in stage: lo stato del file è MM, mettila in stage tu.
- Dopo che l'hai messa in stage, nel §2 la memoria va contata +6.
```

Commit d2a10d5 (tests/test_unit_web_proxy.py: V-3 verifica esterna #312). Verdetto integrale della review #589 (chat Mani):

```
## VERDETTO: APPROVATO

Review #589 (chat Mani): il nuovo test chiude la V-3 della verifica esterna su PR #312 (il caso del client muto che non manda niente). La modifica è solo un test, il motore non cambia, e non ho riserve. Era in stage soltanto tests/test_unit_web_proxy.py (+13 righe) sopra eb6c01c. `git diff --cached --check` è pulito.

Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (solo le parti che servivano) e la memoria del revisore.

**Citazioni**
- `tests/test_unit_web_proxy.py:295` — `test_client_muto_chiuso_alla_scadenza_del_proxy`: proxy con durata=1, il client si connette e resta zitto, e il test chiede un 403 «tempo massimo del proxy superato» entro 2,5 s.
  - Rischio esaminato: un test che non morde, oppure instabile sui tempi.
  - Esito: ok.
  - Ho controllato che il corpo del 403 sia esattamente il motivo (`_rifiuta` a `modules/web/proxy.py:300` scrive `corpo = motivo`), quindi `endswith` è corretto.
  - Il proxy manda una sola risposta di circa 150 byte su loopback, quindi un solo `recv(4096)` basta.
- `modules/web/proxy.py:211` — `client.settimeout(rimasto)` nel ciclo di `_leggi_richiesta`.
  - Rischio esaminato: un mutante che sopravvive.
  - Esito: ok.
  - Su una copia esportata dell'indice ho sostituito la riga con `pass`: 1 failed, 50 passed. Fallisce proprio il test nuovo.
  - Il motivo: senza quella riga il `recv` eredita i 10 s di `TIMEOUT_INATTIVITA` (fissati in `_gestisci`, `modules/web/proxy.py:127`) e il client va in timeout a 3 s.
- `modules/web/proxy.py:202` (contesto) — il motivo «tempo massimo del proxy superato» viene scelto solo quando la scadenza del proxy viene prima dei 10 s di inattività.
  - Con durata=1 è così, quindi il test controlla il ramo giusto e non il ramo «connessione inattiva».
  - Esito: ok.

**Test**
- tests/test_unit_web_proxy.py: 51 passed, 3 volte su 3.
- Il test nuovo da solo: 10 su 10, circa 1,55 s.
- Lo stesso test 5 volte in parallelo con 8 processi che occupano la CPU su 4 core: 5 su 5, circa 1,7 s. Resta un margine di circa 0,8 s sotto il tetto di 2,5 s.

**Cosa non ho verificato**
- La scadenza del proxy parte da `avvia()`, non dalla connessione: il test regge solo perché si connette subito dopo l'avvio. Su un runner CI molto lento il margine si riduce. Non ho provato la CI su GitHub.
- La suite web completa e quella del kernel non le ho rilanciate su questo delta: tocca solo un file di test, e le ho già passate sull'export della #588.

**Memoria**
- Ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga «#589 (chat Mani) — 2026-10-30 — APPROVATO — … Nessuna lezione nuova».
- L'ho committata da sola con scripts/commit_memoria_revisore.sh nel commit 3fe0c43.
- Il test resta in stage e non l'ho toccato, quindi lo SHA del diff revisionato non cambia.
```

Commit b838f4d (modules/web/proxy.py, tests/test_unit_web_proxy.py: V-1/V-2 bot su eea0ea0). Verdetto integrale della review #590 (chat Mani), sul primo giro:

```
## VERDETTO: APPROVATO CON RISERVE

Review #590 (chat Mani). Riguarda il diff staged nel branch claude/peaceful-lovelace-0w2b7q (PR #312, base eea0ea0), con sha256 ab2570af. L'ho provato su un export dell'index in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/exp. Le letture obbligatorie sono fatte: CLAUDE.md §5/§8/§9, stato_progetto.md (testa e parte proxy), memoria_revisore.md (lezioni sul proxy #585–#589, compresa quella sul settimeout che resta sul socket).

**Elementi del diff esaminati**

- `modules/web/proxy.py:300` — Se `self.byte >= self.max_byte`, `_conta_richiesta` rifiuta «troppi byte» prima di `_apri`.
  - Rischio esaminato: la richiesta nuova esce lo stesso quando il tetto è già pieno.
  - Esito: ok. Il test `tests/test_unit_web_proxy.py:240` (`connessi == 1`, 403 «troppi byte») fallisce se tolgo il controllo: 1 failed.
- `modules/web/proxy.py:171` — La testa inoltrata entra nel conteggio dei byte prima di `_invia`.
  - Rischio esaminato: un falso «troppi byte» nel caso normale.
  - Esito: ok. La testa al massimo è circa 16 KB contro un tetto di 20 MB, e scatta solo vicino al tetto. Il test esatto `tests/test_unit_web_proxy.py:251` fallisce se la testa non viene contata: 1 failed.
  - Sonda «testa al limite»: con byte < tetto < byte+testa l'origine non riceve la seconda testa (1 richiesta all'origine). A HEAD la riceveva (2).
- `modules/web/proxy.py:274` — `_invia` usa `settimeout(min(TIMEOUT_INATTIVITA, rimasto))` e trasforma il timeout in «connessione inattiva». Se la scadenza è già passata, rifiuta subito.
  - Rischio esaminato (la tua domanda): un client lento ma legittimo. Il timeout impostato sul client resta anche per il recv di `_pompa`, ma lì il recv parte solo dopo che `select` dice che ci sono dati (`modules/web/proxy.py:264`), quindi non blocca. `sendall`, da Python 3.5, ha un tempo totale: lo stesso valore che aveva prima (10 s), ora solo ridotto alla scadenza.
  - Sonda con socket veri, client lento nel tunnel (100 ms fra un pezzo e l'altro): 120000/120000 byte in 3,01 s, 0 rifiuti → ok.
  - Sonda con un client che non legge nel tunnel e durata 2,5 s: chiuso a 2,51 s. A HEAD: 10,23 s, poi ConnectionResetError → la correzione funziona.
  - Il mutante senza `min(…, rimasto)` fa fallire `tests/test_unit_web_proxy.py:350` (1 failed).
- `tests/test_unit_web_proxy.py:350` — Il test usa un socket finto che non legge. È un sostituto di test, non una simulazione di output di tool (§5) → ok.

**Riserve (da tracciare in stato_progetto.md)**

- **R-590-1 (COSMETICA)**: `_invia` (`modules/web/proxy.py:282`) scrive «connessione inattiva» anche quando a chiudere è la scadenza del proxy. Nella sonda del tunnel risultava `rifiuti == ['connessione inattiva']` a 2,51 s con durata 2,5 s. Il test `tests/test_unit_web_proxy.py:368` lo rende definitivo.
  - Rimedio: scegliere il motivo come fa `_leggi_richiesta` (`modules/web/proxy.py:204`), cioè «tempo massimo del proxy superato» quando ha vinto `rimasto`.
- **R-590-2 (BASSA)**: la testa viene contata DOPO `_apri` (`modules/web/proxy.py:161`). Nel caso byte < tetto < byte+testa il proxy risolve il DNS e apre la connessione TCP verso l'host (sonda: `connessi == 2`), senza mandare URL né intestazioni.
  - Rimedio: host e porta sono già noti prima di `_apri`, quindi si possono costruire e contare la testa prima di aprire. URL e intestazioni non escono più: V-1 è chiusa nella sostanza.

**Altre verifiche**

- §9: OSError e BrokenPipe in `_invia` arrivano all'`except Exception` di `_gestisci` (`modules/web/proxy.py:135`), che logga e risponde 502 se non ha ancora risposto. Il proxy non va mai in crash.
- Wall of Shame: nessuno slicing della history, nessuna simulazione di tool. Il motore (gas.py, brains/) non è toccato.

**Prove**

- Proxy: 53 passed, ripetuto 3 volte.
- Web (`-k web`): 690 passed, 2 skipped.
- I 3 mutanti dichiarati (tetto senza min, testa non contata, niente controllo in `_conta_richiesta`) danno 1 failed ciascuno.

**Rischio escluso**: non ho verificato il comportamento con un browser vero senza schermo e un sito reale in TLS (la fetta del browser non esiste ancora e qui non c'è rete vera). Ho provato solo con i server finti locali dei test, il fake DNS e il connettore finto. Non ho nemmeno verificato le note V-3 e V-4 del bot, che dichiari di sistemare nei report.

**Memoria**: riga #590 e una lezione nuova (motivo di un timeout min(inattività, scadenza); contare i costi prima di aprire la connessione) aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md e committate da sole (a5c92e4). Il diff staged sotto review è rimasto intatto.

File: /home/user/Gas/modules/web/proxy.py, /home/user/Gas/tests/test_unit_web_proxy.py, sonda /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/sonde/test_sonda590.py
```

Verdetto integrale della review #591 (chat Mani), sul diff finale del commit b838f4d:

```
## VERDETTO: APPROVATO

Review #591 (chat Mani), ri-review della #590 sul diff staged (sha256 13326b37), PR #312, branch claude/peaceful-lovelace-0w2b7q. Ho fatto le prove su un export dell'index; il diff staged non l'ho toccato.

**Elementi del diff esaminati**

- `modules/web/proxy.py:170` — Il proxy costruisce la testa e la conta prima di `_apri` (`modules/web/proxy.py:171`). Rischio esaminato: con un tetto sforato si apre lo stesso la connessione verso l'host. Esito: ok.
  - Nella sonda «testa al limite» (byte < tetto < byte+testa) ora `connessi == 1` e l'origine riceve 1 richiesta. Nella #590 erano 2 connessioni.
  - Il mutante con il conteggio rimesso dopo `_apri` dà 1 failed. Lo cattura `tests/test_unit_web_proxy.py:350` (`max_byte=40`, 403 «troppi byte», `connessi == []`).
- `modules/web/proxy.py:284` — Il motivo del rifiuto ora dice chi ha chiuso: «tempo massimo del proxy superato» se `rimasto < TIMEOUT_INATTIVITA`, altrimenti «connessione inattiva». Rischio esaminato: il registro dei rifiuti dice il falso, come in R-590-1. Esito: ok.
  - Nella sonda con socket veri, un client che non legge nel tunnel con durata 2,5 s viene chiuso a 2,51 s con `rifiuti == ['tempo massimo del proxy superato']`.
  - Ho provato il mutante del motivo in tutti e due i sensi: 1 failed ciascuno. I test che li prendono sono `test_invio_bloccato_si_ferma_alla_scadenza` e `test_invio_bloccato_inattivo`, che usa `TIMEOUT_INATTIVITA` = 0,3 con monkeypatch. `_invia` legge il valore globale del modulo, quindi la patch ha effetto.
- `modules/web/proxy.py:280` — `settimeout(min(…))` è invariato rispetto alla #590. Ho rifatto la sonda del client lento ma legittimo nel tunnel: 120000/120000 byte in 3,01 s, 0 rifiuti. Il recv di `_pompa` parte solo dopo `select`. Esito: ok.
- §9: un rifiuto per «troppi byte» prima di `_apri` arriva a `_gestisci` con `risposto` ancora False, quindi il browser riceve un 403 col motivo. Nessuna eccezione esce dal proxy.

**Prove**

- Proxy: 55 passed, ripetuto 3 volte.
- Web (`-k web`): 692 passed, 2 skipped. Tu riporti 691: la differenza viene dal filtro `-k`.

**Nota non bloccante**: ora la testa si conta prima di `_apri`, quindi consuma budget anche quando `_apri` poi rifiuta (DNS fallito, indirizzo interno). Si tratta al massimo di circa 16 KB per richiesta. Va nella direzione prudente, quindi non apro una riserva.

**Rischio escluso**: non ho verificato il comportamento con un browser senza schermo vero e un sito TLS reale. Qui non c'è rete vera e la fetta del browser non esiste ancora: ho provato solo con i server finti locali dei test.

**Memoria**: ho aggiunto la riga #591 (nessuna lezione nuova) a /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (2f84376).

File: /home/user/Gas/modules/web/proxy.py, /home/user/Gas/tests/test_unit_web_proxy.py, sonda /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/sonde/test_sonda590.py
```

Commit 826a9b1 (merge di origin/main 3a38e75: entrano .github/workflows/ci.yml, clients/voice/*, modules/voice/server.py, i test della voce e la roadmap di M2). Verdetto integrale della review #592 (chat Mani):

```
## VERDETTO: APPROVATO

Review #592 (chat Mani), 2026-10-31. Oggetto: merge in corso di origin/main 3a38e75 (PR #313 di M2, voce V4) nel branch claude/peaceful-lovelace-0w2b7q (PR #312, proxy filtrante). Ho controllato il diff staged in /home/user/Gas, con MERGE_HEAD uguale a origin/main 3a38e75 e base comune 1e8aff8. Prima della review ho letto CLAUDE.md (sezioni 5, 8, 10), le sezioni di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `.github/workflows/ci.yml:122` — imposta `GAS_TEST_BROWSER_OBBLIGATORIO: "1"` nella suite voce e fissa `playwright@1.63.0` a `.github/workflows/ci.yml:111`. Rischio esaminato: che il merge perda o alteri il lato main della CI, oppure che compaia un `paths-ignore`. Esito: ok. Il file è identico a MERGE_HEAD, i passi della suite web restano e non c'è nessun `paths-ignore`.
- `modules/voice/server.py:265` — controlla il tetto orario dei turni a voce prima della trascrizione (STT) e risponde 429 senza spendere Groq. Rischio esaminato: una risoluzione dei conflitti che mescoli il codice voce col branch. Esito: ok. Il file è identico a MERGE_HEAD, e lo sono anche `clients/voice/browser_client.html:433` (`sogliaDaCampioni`), `clients/voice/browser_server.py`, `tests/test_unit_voice_server.py`, `tests/test_unit_voice_stt.py`, `reports/roadmap.md` e `gas.py`.
- `modules/web/proxy.py:185` — rifiuta i tunnel CONNECT diretti a una porta diversa da 443 (ricontrollo a `modules/web/proxy.py:189`). Rischio esaminato: che il merge annulli la fetta 32. Esito: ok. Sono identici a HEAD anche `tests/test_unit_web_proxy.py`, `tests/test_unit_web_leggi.py`, `reports/ripartenza_mani.md` e i tre log di sessione tenuti dal lato branch.
- Insiemi di file. Indice confrontato con MERGE_HEAD: ci sono solo i 9 file della fetta 32 (proxy, test web, ripartenza_mani, diff_sessione, handoff, ultimo_report, stato, memoria). Indice confrontato con HEAD: ci sono solo i 9 file di main (ci.yml, i due file di clients/voice, modules/voice/server.py, i due test voce, roadmap, stato con 1 riga in più, memoria con 9 righe in più). I file toccati da main coincidono con l'elenco del confronto con HEAD, tranne i tre log di sessione: lì tieni la versione del branch, come dichiari e come nel merge della #588. Esito: ok.
- Righe perse. Nella memoria nessuna riga tolta, né rispetto a HEAD né rispetto a MERGE_HEAD. Ordine: #588–#591 della chat Mani, poi #580-M2–#584-M2. In `reports/stato_progetto.md` manca 1 sola riga di main: è l'intestazione «Ultimo aggiornamento» (riga 4), aggiornata dal branch. Main non l'aveva toccata (identica alla base), quindi non si perde contenuto. La riga V4 di main c'è. Esito: ok.
- Pulizia. `git diff --cached --check` è pulito e nell'indice non ci sono marcatori di conflitto (`<<<<<<<`, `=======`, `>>>>>>>`). Esito: ok.

**Test sull'indice esportato (checkout-index in /tmp/rev592)**
- Web (proxy più leggi): 557 passed, 1 skipped.
- `pytest -k voice tests/`: 138 passed.
- Test del browser con `GAS_TEST_BROWSER_OBBLIGATORIO=1`: 16 passed (Chromium presente, nessuno saltato).
- Hook: 211 passed.
- Kernel (`tests/test_unit_kernel.py`): 1062 PASS, 1 FAIL. Il FAIL è T31g (`GAS_VECTORS=1`), lo stesso già annotato in #588 come presente anche su origin/main. T101a/b passano: istruzione_turno resta nel system e fuori dalla cronologia.

Questo merge non tocca `_get_window` né il tetto delle 10 iterazioni (gas.py identico a main). Non c'è slicing della history e non c'è simulazione di tool.

**Rischi esclusi (non verificati)**
- Non ho rifatto il FAIL di T31g su un export di origin/main. Mi baso su #588, perché il merge non tocca né gas.py né modules/memory. Va confermato dalla CI.
- Non ho verificato che la CI su GitHub installi davvero Playwright 1.63.0 e Chromium col passo nuovo. In locale Chromium c'era già (`NODE_PATH` globale), quindi l'ambiente del runner non si riproduce qui.

**Note (non riserve)**
- Dopo il commit di merge, handoff, diff_sessione e ultimo_report vanno riscritti sulla base nuova 3a38e75, come dichiari: conteggi del §2 e nota «base = …». È lo stesso tipo di problema di R-588-1.
- Memoria: la riga contatore #592 è aggiunta in fondo a `/home/user/Gas/.claude/agents/memoria_revisore.md` e lasciata fuori dallo stage (lo stage resta 9 file, come richiesto). `scripts/commit_memoria_revisore.sh` non è partito: l'hook `review_gate.sh` ha bloccato il comando perché `.claude/.review_ok` non corrisponde al diff staged, e durante un merge un commit della sola memoria non va comunque fatto. La riga entra col tuo flusso dopo il merge.
- Per committare il merge devi rigenerare il marcatore con `bash scripts/segna_review_ok.sh`.

Riga contatore scritta:
`#592 (chat Mani) — 2026-10-31 — APPROVATO — merge di origin/main 3a38e75 (PR #313 M2, V4 voce) in claude/peaceful-lovelace-0w2b7q (PR #312) … Nessuna lezione nuova.`
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. Nuovo `tests/test_unit_web_proxy.py`: 55 test. Web 691 passed, 2 skipped (692 con `-k web`). `tests/test_unit_web_leggi.py`: `test_https_sulla_porta_80`. Web 687 passed, 2 skipped. Suite completa in locale (Python 3.13), prima del merge di main: `2779 passed, 2 skipped in 220.09s`; dopo il merge (review #588): web e voce 815 passed, 2 skipped; kernel 1062 PASS / 1 FAIL (T31g, GAS_VECTORS, identico su main: dipende dall'ambiente). Mutanti presi: IP interni, tunnel su ogni porta e «:80/:443», upgrade, metodi, tetto dei byte, https in chiaro, Proxy-*, tempo della testa, `ferma()`, timeout rimasto.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 8339cf0, 87d0777, 1b0cce6 (memoria del revisore) e 07ea587: pushati insieme prima dell'apertura della PR #312. Run push 41100200600 su 07ea587: `handoff-check` failure (intermedio: l'handoff non era ancora nel diff), superato dal commit di fine-task.
- 6ebecba (fine-task): run 41100831063 ancora in coda alla verifica esterna; check `smista` del bot failure con la PR in conflitto con main.
- eb6c01c (merge di main), 3fe0c43 (memoria del revisore), d2a10d5 ed eea0ea0 (fine-task): CI verde su eea0ea0 (check suite completata senza fallimenti); check `verifica-bot` success, review del bot APPROVATO CON RISERVE (vedi §1).
- a5c92e4, 2f84376 (memoria del revisore), b838f4d, 805b4d8 (fine-task): CI verde su 805b4d8 (unit-suite, handoff-check success); check `verifica-bot` success, bot APPROVATO CON RISERVE (vedi §1).
- 826a9b1 (merge di main 3a38e75), il commit della memoria #592 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- V-2 bot #312 su 805b4d8 COSMETICA: la testa del CONNECT e la risposta 200 non entrano in `MAX_BYTE_TOTALI`; allineare docstring o conteggio.
- V-4 bot #312 COSMETICA: le intestazioni hop-by-hop nominate dentro «Connection» non vengono tolte (non è un bypass: Upgrade è rifiutato a parte e la testa è ricostruita).
- R-585-4 (chat Mani) BASSA, per la fetta del browser: i confini della risposta non sono controllati (riuso della connessione da verificare con Chromium).
- R-585-5 (chat Mani) BASSA, per la fetta del browser: Chromium salta il proxy per il loopback; servono `--proxy-bypass-list=<-loopback>` e QUIC, WebRTC e prefetch spenti.
- Limiti dichiarati del proxy: filtra le destinazioni, non i dati; niente autenticazione per gli altri processi locali.
- V-1 bot #309 BASSA (limite): verdetto che cita alla lettera un caso di prova di credenziale spezzata non pubblicato.
- R-582-1 BASSA, R-582-2 COSMETICA, R-580-2 BASSA (limiti del bot); V-1/V-2 bot e ve #306.
- R-572-1, R-572-2, R-575-1 BASSE e R-575-2 COSMETICA (chat Mani), preesistenti.
- (b) libexpat ≥ 2.4 nel doctor: con M1.
- V-3 ve #303 BASSA: selectolax 1.0.2 uscita il 2026-10-22, da decidere dall'operatore prima del `pip install` sul VPS.
- R-518-1, R-516-1, R-ve277-5, V-1 ve/bot #288, V-2/V-3 ve #296, R-546-1: BASSE della chat Mani, invariate.
