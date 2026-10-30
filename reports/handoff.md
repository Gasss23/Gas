# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-30 — Mani, fetta 32 (R6): proxy filtrante per il browser senza schermo (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #312 (https://github.com/Gasss23/Gas/pull/312). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5088535610","url":"https://github.com/Gasss23/Gas/pull/312"}`), perché `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve il sì dell'operatore, anche tramite M1.
2. Fetta di SICUREZZA: secondo passaggio indipendente nella chat claude.ai col link della PR.

---

## §1 SCOPE & ESITO FETTE

- **PR #310**: `FATTA` — mergiata (15c4da8). V-1 bot #310 BASSA (test https sulla porta 80): `FATTA`.
- **Proxy filtrante** (`modules/web/proxy.py`, prima fetta del browser senza schermo, piano approvato dall'operatore tramite M1): `FATTA` (PR #312).
- **Review #585 (chat Mani)**: BOCCIATO. B-585-1 MEDIA (tunnel verso la 80 con «:80/:443»): `FATTA`. R-585-2, R-585-3, R-585-6: `FATTA`. R-585-4 e R-585-5: `DEFERITA — fetta del browser`.
- **Review #586**: APPROVATO CON RISERVE. R-586-1 BASSA (timeout della testa rimasto sul tunnel): `FATTA`. **Review #587**: APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 modules/web/proxy.py               | 308 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  14 +++++++-------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   2 +-
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  20 +++++++++-----------
 tests/test_unit_web_leggi.py       |  13 +++++++++++++
 tests/test_unit_web_proxy.py       | 330 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: base = merge-base con origin/main = 15c4da8. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. Nuovo `tests/test_unit_web_proxy.py`: 50 test. `tests/test_unit_web_leggi.py`: `test_https_sulla_porta_80`. Web 687 passed, 2 skipped. Suite completa in locale (Python 3.13): `2779 passed, 2 skipped in 220.09s`. Mutanti presi: IP interni, tunnel su ogni porta e «:80/:443», upgrade, metodi, tetto dei byte, https in chiaro, Proxy-*, tempo della testa, `ferma()`, timeout rimasto.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 8339cf0, 87d0777, 1b0cce6 (memoria del revisore) e 07ea587: pushati insieme prima dell'apertura della PR #312; nessuna run sulla PR per questi SHA.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-585-4 (chat Mani) BASSA, per la fetta del browser: i confini della risposta non sono controllati (riuso della connessione da verificare con Chromium).
- R-585-5 (chat Mani) BASSA, per la fetta del browser: Chromium salta il proxy per il loopback; servono `--proxy-bypass-list=<-loopback>` e QUIC, WebRTC e prefetch spenti.
- Limiti dichiarati del proxy: filtra le destinazioni, non i dati; niente autenticazione per gli altri processi locali.
- V-1 bot #309 BASSA (limite): verdetto che cita alla lettera un caso di prova di credenziale spezzata non pubblicato.
- R-582-1 BASSA, R-582-2 COSMETICA, R-580-2 BASSA (limiti del bot); V-1/V-2 bot e ve #306.
- R-572-1, R-572-2, R-575-1 BASSE e R-575-2 COSMETICA (chat Mani), preesistenti.
- (b) libexpat ≥ 2.4 nel doctor: con M1.
- V-3 ve #303 BASSA: selectolax 1.0.2 uscita il 2026-10-22, da decidere dall'operatore prima del `pip install` sul VPS.
- R-518-1, R-516-1, R-ve277-5, V-1 ve/bot #288, V-2/V-3 ve #296, R-546-1: BASSE della chat Mani, invariate.
