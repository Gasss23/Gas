# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — Chat Mani, fetta 1: `leggi_pagina` (R6 «leggere il web», PR #235)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #235 (https://github.com/Gasss23/Gas/pull/235): tocca `.github/workflows/ci.yml` (macchina del bot) → `verifica-bot` neutral, il merge lo decide l'operatore.
2. Porte verso host pubblici oggi libere (1-65535): limitarle è una scelta dell'operatore (R6 della review #391, chat Mani).
3. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

(`gh` non autenticato nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **`leggi_pagina` in `modules/web/`**: `FATTA`
- **Test con server e DNS finti (83)**: `FATTA`
- **Passo «web suite» in CI**: `FATTA`
- **Aggancio come strumento di Gas (gas.py, cancello, diario)**: `SALTATA` — fuori dall'area della chat Mani, richiesto alla chat Motore in `reports/ultimo_report.md`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++
 .github/workflows/ci.yml           |   7 ++++
 modules/web/__init__.py            |   4 ++
 modules/web/leggi.py               | 481 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  17 ++++----
 reports/handoff.md                 | 776 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 +-
 reports/ultimo_report.md           |  57 ++++++++++++++-------------
 tests/test_unit_web_leggi.py       | 539 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 9 files changed, 1285 insertions(+), 605 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
0fbe4f3 test(web): marcatore gasmerge-ip-ok sulle righe con IP di prova (Gate IP)
7925785 Merge origin/main (#233) in feat/mani-web-leggi-pagina
6af7ff0 fix(web): il cane da guardia possiede una copia del descrittore (R-392-1, chat Mani)
b4617d8 feat(web): leggi_pagina — una pagina web in testo pulito, marcato NON FIDATO (R6, chat Mani)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. I commit di main portati dal merge `7925785` non sono della sessione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Cinque verdetti, incollati integralmente nell'ordine: #391 (chat Mani, BOCCIATO), #392 (chat Mani), #393 (chat Mani), #406 (chat Mani, merge di main), #407 (chat Mani, marcatori del Gate IP nei test). Le righe citate dalla #391 si riferiscono alla prima versione del file.

### Review #391 (chat Mani)

## VERDETTO: BOCCIATO

Review #391 (chat Mani). Ho esaminato il diff staged su feat/mani-web-leggi-pagina (da 74e819b): `.github/workflows/ci.yml`, `modules/web/__init__.py`, `modules/web/leggi.py`, `tests/test_unit_web_leggi.py`. Letture obbligatorie fatte: CLAUDE.md (sez. 1, 5, 8, 9, 10), reports/stato_progetto.md (in modo mirato), .claude/agents/memoria_revisore.md (la coda; non c'erano lezioni precedenti su SSRF o redirect).

Il requisito dell'operatore «tempo massimo fisso» si aggira in due modi, entrambi riprodotti. Il primo vale per HTTPS, cioè per quasi tutto il web. In una fetta di sicurezza un requisito esplicito non rispettato blocca. Il resto della difesa (SSRF, rebinding, redirect, cookie) è solido.

### Motivi bloccanti

**B1 (ALTA): su HTTPS il tempo massimo si aggira.**
- `modules/web/leggi.py:226`: il cane da guardia è un `threading.Timer` che fa `_taglia(grezzo)`. Rischio esaminato: una lettura lenta che non finisce mai. Esito: **blocco**.
- `modules/web/leggi.py:234`: `wrap_socket` fa detach del socket grezzo. Ho verificato che dopo il wrap `grezzo.fileno()` vale -1 e che `shutdown` dà `[Errno 9] Bad file descriptor`. `modules/web/leggi.py:201` ingoia l'OSError, quindi il cane non taglia più niente.
- Da quel momento ogni recv ha come timeout il tempo «rimasto» calcolato prima della chiamata. Un server lento in tre punti tiene la chiamata aperta senza limite: riga di stato e intestazioni (`modules/web/leggi.py:249`, `getresponse`), handshake TLS, dimensione dei chunk.
- Riprodotto con un server TLS locale vero (certificato autofirmato, nessuna rete) e `TIMEOUT_TOTALE=2`:
  - intestazioni lente: 60,1 s su 3.13.16 e su 3.11.17;
  - dimensione del chunk lenta: 60,1 s.
  - Lo stesso server in HTTP semplice si ferma a 2,0 s. Con un byte ogni meno di 15 s il limite in pratica non c'è (100 intestazioni da 64 KB).
- Perché i test non lo vedono: `tests/test_unit_web_leggi.py:387` usa un `_TlsFinto` che restituisce lo stesso socket, quindi il detach non avviene mai. Mutazione «`cane.start()` tolto»: **73 passed**. Il cane non è coperto da nessun test (`tests/test_unit_web_leggi.py:345` copre solo il corpo lento in HTTP, già fermato da `_imposta_timeout`).
- Correzione proposta:
  - il cane deve agire sul socket vivo (un contenitore aggiornato dopo il wrap, oppure `sock.shutdown`);
  - test con un TLS finto che fa detach come quello vero, ad esempio `return socket.socket(fileno=sock.detach())`, e un server che manda le intestazioni lentamente;
  - dopo `getresponse` va controllato `_rimasto(scadenza)`.

**B2 (ALTA): la scadenza non copre la decodifica del testo.**
- `modules/web/leggi.py:346-355`: `_decodifica` accetta qualunque codec che `codecs.lookup` riconosce. Con `Content-Type: text/plain; charset=punycode` la decodifica è quadratica.
- Misura su `_componi`: 2 MB = **262,6 s di CPU** (400 KB = 6,5 s). Questo avviene dopo il download, fuori da ogni scadenza e col GIL preso.
- Correzione: lista bianca dei charset (utf-8, us-ascii, iso-8859-*, windows-125x, eventualmente utf-16), altrimenti utf-8. Fuori di sicuro punycode, idna, utf-7, unicode_escape e raw_unicode_escape. Serve un test con `charset=punycode`.

### Riserve (da tracciare, non bloccanti)

- **R3 MEDIA, marcatori finti.** `modules/web/leggi.py:59` e `modules/web/leggi.py:343`: la regex prende solo la forma esatta. Su 8 varianti ne passano 7: parentesi a tutta larghezza `［…］`, «ＦＩＮＥ» a tutta larghezza, O cirillica, «NON-FIDATO», «FINE DEL CONTENUTO», marcatore senza `[`, `&#8203;` (lo spazio a larghezza zero viene tolto e resta «FINECONTENUTO»). Il requisito «sempre marcato NON FIDATO» è rispettato. Però un marcatore di chiusura falso resta facile da scrivere. Proposta: un codice casuale diverso a ogni chiamata dentro i due marcatori (la pagina non può indovinarlo), più NFKC prima della regex.
- **R4 BASSA, site-local IPv6.** `modules/web/leggi.py:93-101`: `fec0::1` (site-local, deprecato) viene accettato su 3.11 e su 3.13. Basta aggiungere `addr.is_site_local`.
- **R5 BASSA, motivo sbagliato.** Se la scadenza arriva durante le intestazioni in HTTP semplice, il motivo restituito è «tipo di contenuto non supportato» invece di «tempo massimo superato». Si chiude insieme alla correzione di B1.
- **R6 BASSA, porte.** `modules/web/leggi.py:165`: verso host pubblici è ammessa qualunque porta da 1 a 65535 (si possono sondare porte di macchine esterne). Limitarle è una decisione dell'operatore.
- **R7 BASSA, riepilogo CI.** La web suite non compare nel «Job summary» di `.github/workflows/ci.yml` (dalla riga 173). Se fallisce, il job diventa comunque rosso. Il riepilogo è fuori dal perimetro assegnato alla chat.
- **Nota per la chat Motore.** Quando la funzione verrà agganciata come strumento, i parametri `_risolvi`, `_connetti` e `_tls` di `modules/web/leggi.py:392` non devono mai arrivare dal modello.

### Elementi verificati e risultati OK

- `modules/web/leggi.py:76-101` (`indirizzo_interno`). Rischio esaminato: IP scritti in forme strane, IPv4 dentro IPv6, NAT64, 6to4, Teredo, differenze tra 3.11 e 3.13. Provate 48 forme, con esiti identici su 3.11.17 e 3.13.16. Esito: **ok**, salvo R4.
- `modules/web/leggi.py:217-224`. Rischio esaminato: DNS rebinding. Tutti gli IP risolti vengono controllati e la connessione va a `ips[0]` senza una seconda risoluzione. La mutazione con una seconda risoluzione viene presa (1 failed). Esito: **ok**.
- `modules/web/leggi.py:411-420`. Rischio esaminato: redirect verso indirizzi interni o altri schemi. A ogni salto c'è un nuovo `_valida_url` e un nuovo controllo dell'IP; il limite è di 5 salti. Esito: **ok**.
- `modules/web/leggi.py:159` e `modules/web/leggi.py:241-246`. Rischio esaminato: credenziali nell'URL, cookie, compressione, proxy d'ambiente. Esito: **ok**. Le mutazioni «@ permesso» e «Cookie inviato» vengono prese.
- `modules/web/leggi.py:422-429`. Rischio esaminato: eccezioni che arrivano a chi chiama e testo del server nel «motivo». Il motivo contiene solo testo scritto nel modulo oppure `type(e).__name__`. Esito: **ok**.
- `.github/workflows/ci.yml:113-118`. Rischio esaminato: modifica agli altri passi. È solo un'aggiunta, con lo stesso schema del passo voce; lo YAML è valido. Esito: **ok**.
- Test: `python3.13 -m pytest tests/test_unit_web_leggi.py -q` dà 73 passed. Mutazioni: M1, M2, M4, M5, M7, M8 e M11 vengono prese. M3 (cane tolto) sopravvive: è la falla B1. M6, M9 e M10 sopravvivono, ma sono equivalenti: senza il ramo esplicito la libreria standard rifiuta comunque quegli indirizzi.

### Rischi esplicitamente esclusi

- La suite pytest su 3.11 non l'ho eseguita: qui `python3.11` non ha pytest. Su 3.11.17 ho eseguito con script diretti l'elenco degli IP, il TLS lento e il punycode.
- Non ho verificato su macOS e sulla VPS se uno `shutdown` lanciato da un altro thread sblocca davvero una recv: non si riproduce in questo ambiente.
- Non ho provato il resolver DNS vero con forme come «127.1» o «2130706433». Il ragionamento è che vengono controllati gli IP già risolti, quindi la forma della stringa conta poco.

### Memoria

Ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga «#391 (chat Mani) — 2026-10-21 — BOCCIATO — …», con la lezione sul detach del socket dopo il wrap TLS e sulla lista bianca dei charset. Come richiesto non ho committato e non ho eseguito `scripts/commit_memoria_revisore.sh`: il file risulta modificato e non è in staging.

Gli script che riproducono i problemi sono in `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/`: `tls_lento.py` (B1), `puny2.py` (B2), `ip.py` (elenco degli IP) e `wt/` (copia per le mutazioni).

### Review #392 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Ri-review #392 (chat Mani) del diff in staging su feat/mani-web-leggi-pagina, cioè la correzione della #391. Letture fatte prima della review: CLAUDE.md, reports/stato_progetto.md (letto a pezzi: non c'è una sezione Mani) e la memoria del revisore (il numero più alto era #391, da qui il #392).

**Cosa ho rifatto io**
- I test danno 81 passed su Python 3.13.16 e su 3.11.17. Restano 81 passed anche con rete e DNS veri bloccati (sitecustomize) e su 3 ripetizioni.
- Lo YAML di ci.yml è valido.
- Ho rilanciato `tls_lento.py header|body|chunk` con TLS vero: dura 2,0 s su entrambe le versioni ed esce con «tempo massimo superato».
- `puny2.py` con punycode su 2 MB: 0,5 s.
- HTML ostile da 2 MB, 18 forme diverse (`<p>`, `&`, `<a\n`, `<!--` non chiuso, ecc.): al massimo 1,9 s, crescita lineare.
- La lista bianca dei charset contiene solo nomi canonici. punycode, idna, utf-7, gli `*_escape`, base64, zlib e hz finiscono su utf-8.
- Mutazioni fatte in una copia isolata (nessuno stash, nessun worktree del repo):
  - cane da guardia spento: 4 FAIL;
  - lista bianca tolta: 1 FAIL;
  - `is_site_local` tolto: 1 FAIL;
  - codice dei marcatori fisso: 2 FAIL;
  - NFKC tolto: 81 passed, nessun test se ne accorge;
  - `_rimasto` dopo getresponse tolto: 81 passed, nessun test se ne accorge.

**Elementi del diff esaminati**
- `modules/web/leggi.py:224` — il cane da guardia prende il numero del descrittore prima del wrap TLS e alla scadenza fa shutdown su `os.dup` (riga 239). Rischio: che dopo il wrap il cane resti inutile come in B1. Esito ok: wrap_socket stacca il socket ma l'SSLSocket tiene lo stesso numero, quindi lo shutdown taglia anche il TLS vero (provato su 3.11 e 3.13).
- `modules/web/leggi.py:249` e `modules/web/leggi.py:332` — `ferma()` sotto lucchetto, chiamato nel finally prima delle chiusure. Rischio: il timer che scatta su un descrittore già chiuso o riusato. Esito: **riserva R-392-1**. Il lucchetto copre solo le chiusure fatte da noi. Con `Connection: close`, http.client chiude davvero il descrittore dentro `read1` a fine corpo (e in getresponse quando c'è un errore), cioè prima di `ferma()`. L'ho sondato con una spia su `ferma()`: nel caso normale, sia HTTP sia HTTPS, su 3.11 e 3.13, il descrittore è già chiuso. Un socketpair aperto in quella finestra riceve lo stesso numero (5) e `_taglia()` gli fa shutdown: l'altro socket va in BrokenPipe. La finestra è di microsecondi alla scadenza, ma nel kernel girano altri thread (Telegram). La docstring della classe, nella frase sul lucchetto, promette proprio il contrario. Correzione: fare `os.dup` una sola volta nel costruttore, fare lo shutdown su quella copia e chiudere la copia in `ferma()` sotto il lucchetto. Così il numero non può essere riusato.
- `modules/web/leggi.py:301` — `_rimasto` dopo getresponse. Rischio: intestazioni arrivate oltre la scadenza. Esito ok sul piano funzionale: senza questo controllo scatterebbero comunque quelli dei passi successivi (riga 320 e il salto di redirect). Riserva in R-392-2: nessun test lo copre.
- `modules/web/leggi.py:404` — lista bianca `_CHARSET_AMMESSI` (riga 68) sul nome canonico. Rischio: un codec quadratico o di trasformazione che passa. Esito ok: 31 alias sondati, tempi lineari anche con byte ostili su utf-16, gb18030, shift_jis, big5 ed euc_jp.
- `modules/web/leggi.py:386` — NFKC prima della pulizia, con la regex di `modules/web/leggi.py:63`. Rischio: finti marcatori. Esito: riserva.
  - **R-392-2**: le forme fullwidth sono neutralizzate (sondato), ma nessun test lo prova.
  - **R-392-3**: la regex resta un elenco di forme. Passano ancora `FINE_CONTENUTO_WEB_NON_FIDATO`, la stessa forma con trattini fra tutte le parole e una «О» cirillica. La difesa vera è il codice casuale (`modules/web/leggi.py:413`), quindi quando il modulo verrà collegato al kernel bisogna dire al modello di fidarsi solo dei marcatori con quel codice.
- `modules/web/leggi.py:117` — `is_site_local` per IPv6. Esito ok (la mutazione lo rivela).
- `tests/test_unit_web_leggi.py:398` — `_TlsCheStacca` fa detach come il TLS vero. `tests/test_unit_web_leggi.py:414` testa /lento, /intestazioni-lente e /chunk-lento in HTTPS. Rischio: un test che non morde, come alla #391. Esito ok: col cane spento fallisce.
- `.github/workflows/ci.yml:113` — passo `pytest tests/test_unit_web_*.py` con `if: always()` e pipefail. Esito ok. Nota: ci.yml fa parte del codice del bot di verifica, quindi sulla PR verifica-bot darà neutral e il merge lo decide l'operatore.

**Riserve (tutte BASSE, nessuna bloccante)**
- **R-392-1 (chat Mani)**: race sul numero del descrittore, spiegata sopra. Da chiudere prima di collegare il modulo al kernel.
- **R-392-2 (chat Mani)**: NFKC e il `_rimasto` dopo getresponse non hanno un test che li copra.
- **R-392-3 (chat Mani)**: la regex dei finti marcatori lavora per elenco di forme; il cablaggio nel kernel deve far valere il codice.

Restano aperte, come dichiarato: R6 (porte, decisione dell'operatore) e R7 (fuori dall'area di questa chat).

**Cosa NON ho verificato**
- Il comportamento su VPS e con un DNS di sistema vero e lento: in sviluppo la rete è bloccata o passa da un proxy.
- La race R-392-1 l'ho dimostrata solo simulando il timer nella finestra con una spia; non l'ho riprodotta con un timer reale, perché la finestra è di microsecondi.
- Python 3.14 non provato.
- Il collegamento al kernel non esiste ancora, quindi non ho fatto il test di round-trip agentico richiesto dalla sezione 7.

**Memoria del revisore**
- Ho aggiunto la riga «#392 (chat Mani) — 2026-10-21 — APPROVATO CON RISERVE — …», con la lezione: un cane da guardia che lavora sul numero di un descrittore deve possederne una copia fatta nel costruttore.
- La riga è nel file `/home/user/Gas/.claude/agents/memoria_revisore.md`, modificato nella cartella di lavoro ma non aggiunto allo staging (stato `MM`).
- Non ho committato: non ho lanciato `scripts/commit_memoria_revisore.sh` perché me l'avevi chiesto tu. Prima del commit va aggiunta allo staging.

**Script di prova** (in `/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/`)
- `race_fd.py`: la spia della race.
- `html_cpu.py`: i tempi sull'HTML ostile.
- `mut/`: la copia isolata delle mutazioni.

### Review #393 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Ri-review #393 (chat Mani) sul diff staged del ramo feat/mani-web-leggi-pagina (HEAD b4617d8). Il diff tocca 2 file: modules/web/leggi.py e tests/test_unit_web_leggi.py.

Prima della review ho letto CLAUDE.md (sezione 5 e guardrail), reports/stato_progetto.md (in modo selettivo) e .claude/agents/memoria_revisore.md (le lezioni in testa e le ultime righe, fino alla #392).

**Elementi del diff esaminati**

1. `modules/web/leggi.py:226` — il costruttore fa `os.dup` una sola volta e la copia diventa un oggetto socket. Rischi esaminati:
   - **Costruttore che fallisce a metà, caso Timer.start in errore.** Sondato con `threading.Timer.start` che solleva RuntimeError. La copia non viene chiusa esplicitamente: la chiude il GC, con ResourceWarning. Il chiamante a `modules/web/leggi.py:271` chiude il socket grezzo, e la funzione esterna restituisce `{"ok": False, "motivo": "errore di rete o di protocollo (RuntimeError)"}` senza crash. Nessun fd perso lato client su 10 chiamate, su 3.13 e 3.11.
   - **Costruttore che fallisce a metà, caso `socket.socket(fileno=)` in errore dopo il dup.** Sondato con un dup finto su /dev/null: +5 fd su 5 tentativi, cioè il descrittore duplicato si perde. Con un socket vero (quello che arriva da create_connection) questo caso non si può verificare.
   - **Flag O_NONBLOCK** (il flag è condiviso tra un descrittore e la sua copia): verificato, la copia non lo altera né alla creazione né alla chiusura.
   - Esito: riserva cosmetica (R-393-2).
2. `modules/web/leggi.py:238` — lo shutdown avviene sull'oggetto copia, sotto lucchetto. Rischi esaminati:
   - **Shutdown sulla copia di un SSLSocket vero**: tls_lento header/body/chunk con TLS vero dura 2,0 s su 3.13.16 e 3.11.17. L'header è il caso che solo il cane da guardia può tagliare, perché il server manda 1 byte ogni 0,3 s.
   - **Mutazione «shutdown tolto»**: 5 test falliscono.
   - Esito: ok.
3. `modules/web/leggi.py:242` — `ferma()` spegne il timer e poi chiude la copia sotto lucchetto; è idempotente. Rischi esaminati:
   - **ferma prima dello scatto, dopo lo scatto, o in concorrenza con `_taglia`**: per analisi l'ordine è corretto (chi prende il lucchetto per primo vince, e `_taglia` esce se `_finito` è vero).
   - **Mutazione «controllo `_finito` tolto»**: 83 passed e nessun danno. Su un oggetto socket chiuso `fileno` vale -1 e lo shutdown dà EBADF senza toccare nessun numero di descrittore: lavorare sull'oggetto, non sul numero, rende innocuo anche un `_taglia` dopo `ferma()`.
   - **race_fd adattato** (spia su `ferma`, in http e https, su 3.13 e 3.11):
     - la copia è ancora aperta quando si arriva a `ferma`;
     - un `_taglia` fatto nella finestra lascia intatto il socketpair nuovo (recv `b'x'`, send ok);
     - la copia risulta chiusa dopo `ferma`;
     - su 21 letture nessun fd perso (5 prima, 5 dopo).
   - Esito: ok.
4. `modules/web/leggi.py:248` — la chiusura della copia in `ferma()`. Rischio esaminato: la copia resta aperta se la chiusura sparisce. Mutazione «`self._copia.close()` tolto»: 83 passed, nessun test se ne accorge. Oggi la copia la chiude comunque il GC, con ResourceWarning. Esito: riserva bassa (R-393-1).
5. `tests/test_unit_web_leggi.py:513` — il test `test_cane_possiede_una_copia_del_descrittore`. Rischio esaminato: un test che non morde. Con il modules/web/leggi.py di HEAD fallisce (1 FAIL). Fallirebbe anche se il numero liberato non venisse riusato, perché con il codice vecchio il dup su un descrittore chiuso darebbe EBADF e `b.recv` andrebbe in timeout. Esito: ok.
6. `tests/test_unit_web_leggi.py:534` — il test sul marcatore a tutta larghezza. Mutazione «NFKC tolto» in modules/web/leggi.py: 1 FAIL mirato. Esito: ok, R-392-2 chiusa per la parte NFKC.

**Riproduzioni**
- tests/test_unit_web_leggi.py: 83 passed su 3.13.16 e su 3.11.17, anche con rete e DNS veri bloccati.
- pytest completo: 1665 passed.
- `git diff --staged --check` pulito.
- modules/web non è ancora cablato nel kernel: lo importa solo `modules/web/__init__.py:2`.
- Le mutazioni le ho fatte in una copia isolata, il ramo non è stato toccato.

**Riserve**
- **R-393-1 (chat Mani) BASSA**: nessun test verifica che `ferma()` chiuda la copia. Basta un `assert cane._copia.fileno() == -1` dopo `cane.ferma()` in `tests/test_unit_web_leggi.py:526`.
- **R-393-2 (chat Mani) COSMETICA**: se il costruttore fallisce a metà, la copia non viene chiusa esplicitamente. Si chiude con un try/except nel costruttore che chiude la copia, o il fd duplicato, prima di rilanciare l'errore. Oggi il caso si raggiunge solo con fallimenti simulati.
- **R-392-3** resta aperta per il cablaggio nel kernel (chat Motore), come dichiarato.

**Rischio escluso**: non ho verificato il comportamento su VPS né sotto carico reale con molti thread (per esempio con il bot Telegram attivo). La finestra di riuso del descrittore l'ho provata solo in modo deterministico con la spia, non con un'esecuzione concorrente vera, perché non si riproduce in modo affidabile in dev. Non ho riverificato nemmeno la parte `_rimasto` di R-392-2, che resta senza test come dichiarato nel report.

**Memoria del revisore**
Ho aggiunto la riga «#393 (chat Mani) — 2026-10-21 — APPROVATO CON RISERVE — …», con la lezione sul lavorare sull'oggetto copia e non sul numero, in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. Il file è modificato ma non in staging, quindi il diff staged sotto review non cambia. Come da tua istruzione «NON committare» non ho lanciato scripts/commit_memoria_revisore.sh: la memoria va committata col commit della fetta, come per #391 e #392.

Script delle sonde, nella cartella /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/:
- race_fd2.py: la versione adattata di race_fd.py;
- ctor_fail.py e ctor_fail2.py: i fallimenti del costruttore;
- tls_lento.py: le prove di lentezza con TLS vero;
- mut393/: la copia isolata delle mutazioni.

### Review #406 (chat Mani)

## VERDETTO: APPROVATO

Review #406 (chat Mani): merge di origin/main 7bd0875 (PR #233) nel ramo feat/mani-web-leggi-pagina (HEAD 6af7ff0, merge-base 74e819b). Prima della review ho letto CLAUDE.md (sez. 5, 8, 10), reports/stato_progetto.md (in modo mirato) e .claude/agents/memoria_revisore.md (la coda e le lezioni sui merge, tra cui la lezione del 2026-10-12 sulle sezioni di stato prese da entrambe le parti).

**Cosa ho controllato nel diff**
- `.github/workflows/ci.yml:113`: il passo «Run web suite» è intatto (`if: always()`, `set -o pipefail`, `tests/test_unit_web_*.py`, tee su `web_output.txt`). Il rischio era che main avesse cambiato altri passi. `git diff 74e819b origin/main -- .github/workflows/ci.yml` è vuoto: main non ha toccato ci.yml dopo la merge-base. Il passo sta tra voice (:105) e handoff/verdetto (:120), e lo YAML si carica senza errori. **Esito: ok.**
- `.claude/agents/memoria_revisore.md:630`, `.claude/agents/memoria_revisore.md:632` e `.claude/agents/memoria_revisore.md:634`: le righe #391, #392 e #393 (chat Mani). Ognuna sta subito dopo la voce della chat Motore con lo stesso numero (:629, :631, :633). Il rischio era perdere righe o lasciare marcatori di conflitto. Ho verificato tre cose:
  - `diff` fra la versione di origin/main e il file fuso mostra solo 3 aggiunte (643 → 646 righe).
  - Le tre righe Mani sono identiche byte per byte a quelle di HEAD.
  - Rispetto a HEAD mancano solo #277, #370 e #390. Main le aveva modificate dopo la merge-base, quindi è giusto prendere la versione di main. La #390 contiene «<U+200B>» scritto in chiaro, come su main, e nel file non c'è nessun carattere U+200B vero.

  Non ci sono marcatori `<<<<<<<`, `=======` o `>>>>>>>`, e `git diff --cached --check` è pulito. **Esito: ok.**

  Una precisazione: su main la #391 della chat Motore è una riga sola (:629), senza una riga di continuazione separata. Non c'era niente da tenere attaccato, e non manca niente.
- `modules/web/__init__.py:2` (contesto: l'import di `leggi_pagina`): ho cercato dipendenze fra il modulo web e il codice cambiato da main (gas.py, gate, notte, telegram). leggi.py importa solo la libreria standard e nessun file di main cita modules.web. **Esito: ok.**

**Punto 1 (identico a main tranne i file Mani)**
`git diff --cached origin/main --stat` mostra esattamente 5 file: ci.yml (+7), modules/web/__init__.py, modules/web/leggi.py, tests/test_unit_web_leggi.py e la memoria (+3). È identico a `git diff 74e819b HEAD --stat`, cioè l'unione è esatta. I report di sessione (handoff, ultimo_report, stato_progetto, ecc.) sono nella versione di main, e questo è corretto perché il ramo Mani non li aveva toccati.

**Test sull'albero fuso** (worktree uguale all'index, diff non staged vuoto)
- Web suite: 83 passed.
- Gate (tests/test_unit_gate.py): 811 passed.
- Notte (tests/test_unit_notte.py): 106 passed.
- Suite unitaria del kernel (tests/test_unit_kernel.py, il passo «unit suite» della CI): 952 PASS, 1 FAIL. Il fallito è T31g (GAS_VECTORS=1 → VectorStore disponibile). Fallisce allo stesso modo su un worktree pulito di origin/main, perché in questo ambiente manca il modulo `sqlite_vec` (e anche `fastembed`). Non dipende dal merge. Il worktree di confronto l'ho già rimosso.

**Cosa NON ho verificato**
- Il merito del codice di main (gas.py, modules/gate/gate.py, modules/notte/notte.py, modules/telegram/bot.py e i relativi test). Arriva già revisionato dalla chat Motore (#390–#405) e mergiato con la PR #233; qui ho controllato solo che arrivi invariato.
- Il merito di modules/web, già approvato nelle #392 e #393 (chat Mani).
- T31g con `sqlite_vec` installato: non è riproducibile qui, va visto sulla CI con le dipendenze complete.

**Memoria e commit**
- Ho aggiunto in fondo a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga «#406 (chat Mani) — 2026-10-21 — APPROVATO — … Nessuna lezione nuova.» (riga 647). Al momento è solo nel working tree, non in staging: devi fare `git add` prima di `segna_review_ok.sh` e del commit di merge.
- NON ho eseguito `scripts/commit_memoria_revisore.sh`, per due motivi: me l'hai chiesto, e durante un merge in corso `git commit -o` (commit parziale) viene rifiutato da git, oppure chiuderebbe il merge al posto tuo.

### Review #407 (chat Mani) — verdetto RIEMESSO

Riemesso dal revisore su richiesta, con lo stesso esito, gli IP in chiaro sostituiti da <IP-redatto> perché il Gate IP blocca il push. Il testo originale, con gli IP, è nel commit `55bd481` della cronologia del ramo.

## VERDETTO: APPROVATO

Ho letto CLAUDE.md (sez. 5, 8, 9, 10), le voci "Mani" di reports/stato_progetto.md (riga 605) e le lezioni sul Gate IP in .claude/agents/memoria_revisore.md (#75, #124, #147-#154, #172).

**Elementi del diff esaminati**
- `tests/test_unit_web_leggi.py:25` — `IP_PUBBLICO` è un IP pubblico di esempio, con il marcatore. Rischio esaminato: che un IP pubblico vero venga contattato davvero. Esito: **ok**. Il connettore finto `tests/test_unit_web_leggi.py:181` registra l'IP e poi apre la connessione solo verso il loopback <IP-redatto>, sulla porta del server locale. Per qualsiasi IP diverso dai due pubblici finti solleva AssertionError. Lo stesso vale per `tests/test_unit_web_leggi.py:26`.
- `tests/test_unit_web_leggi.py:71` — redirect 307 verso l'indirizzo dei metadati cloud <IP-redatto>, con il marcatore. Rischio esaminato: una connessione all'indirizzo dei metadati. Esito: **ok**. `tests/test_unit_web_leggi.py:271` controlla `connessi == [(IP_PUBBLICO, 80)]`, quindi il redirect viene rifiutato senza aprire una seconda connessione.
- `tests/test_unit_web_leggi.py:168` e `tests/test_unit_web_leggi.py:169` — il DNS finto restituisce indirizzi privati <IP-redatto>. Esito: **ok**. Sono indirizzi interni che il test vuole veder rifiutare, e `tests/test_unit_web_leggi.py:264` controlla `connessi == []`.
- `tests/test_unit_web_leggi.py:248` fino a `tests/test_unit_web_leggi.py:253` — URL con indirizzi interni nella lista parametrizzata. Esito: **ok**. Vengono rifiutati senza connessione (`tests/test_unit_web_leggi.py:258`). La riga 251 non è marcata ma contiene solo un IPv6 mappato sul loopback: il gate la tratta come loopback e la regex IPv4 non tocca gli IPv6, quindi va bene così.
- `tests/test_unit_web_leggi.py:277` — un IP di un DNS pubblico e IP_PUBBLICO passati a `web.indirizzo_interno`. Esito: **ok**. È una funzione pura, non apre nessuna connessione.

**I tre controlli richiesti**
1. **Solo commenti.** L'albero sintattico (AST) del file nell'indice è identico a quello in HEAD (`ast.dump` uguale). Ho rieseguito i test: 83 passed in 7.33s.
2. **Uso onesto del marcatore.** Tutte le 11 righe marcate contengono solo IP di prova. Nessuna di queste porta a contattare un host reale: i due IP pubblici finti finiscono sul loopback, e gli altri sono indirizzi interni che il codice deve rifiutare prima di connettersi. Nessun test chiama `leggi_pagina` senza il connettore finto: l'unica chiamata è in `tests/test_unit_web_leggi.py:188`.
3. **Gate IP.** Ho rifatto a mano i tre passi del gate in `scripts/fine_task_finale.sh:73` (ricerca IP, filtro loopback, filtro per marcatore con `--and --not`, confronto `-Fx`) sul tree dell'indice (`git write-tree` = e91c0d3). Risultato: **0 residui** (rc del filtro = 1). Sul tree di HEAD le righe non marcate erano 10, quindi il blocco era reale. Le aggiunte in reports/ ancora fuori dall'indice contengono solo il loopback, che il gate accetta. Lo script non l'ho lanciato.

**Rischi esclusi**
- Lo script vero gira su `HEAD^{tree}` dopo il commit, io ho controllato il tree dell'indice. Se prima del commit vengono messi nell'indice altri file con IP, il risultato cambia.
- Non ho controllato `scripts/gasmerge.sh` sul ref remoto: la logica è la stessa, ma il ramo non è ancora pushato.
- Non ho eseguito la suite del kernel: il diff non tocca il motore.

**Riserve**: nessuna.

---

## §5 DELTA TEST DEL MOTORE

- Web suite (nuova): 0 → 83 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «83 passed», Python 3.13.16 e 3.11.17; 83 passed anche con rete e DNS veri bloccati via sitecustomize).
- Nessuna modifica a `gas.py` né agli altri moduli. Sull'albero fuso il revisore #406 ha rilanciato gate 811 passed, notte 106 passed, kernel 952 PASS / 1 FAIL (T31g: manca `sqlite_vec` in questo ambiente, fallisce uguale su origin/main pulito).

## §6 STATO CI

- `b4617d8`, `6af7ff0`: pushati sul ramo prima dell'apertura della PR; run CI di push non verificate in questa sessione.
- `7925785` (merge di main): run non ancora disponibile alla scrittura dell'handoff.
- Commit dei marcatori del Gate IP: run non ancora disponibile alla scrittura dell'handoff.
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: R-392-3, R-392-2 (parte residua), R-393-1, R-393-2, R6 e R7 della #391 (tutte chat Mani, BASSE/COSMETICHE): dettaglio in `reports/stato_progetto.md`, blocco «Mani — fetta 1».
- Le altre riserve aperte del progetto sono in `reports/stato_progetto.md`.
