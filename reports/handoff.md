# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-25 — Dashboard del CRM anche dal telefono (decisione 21)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: tocca `scripts/` e il codice del CRM, quindi il bot dà `neutral` e il merge lo decide l'operatore. Fetta di sicurezza: secondo passaggio consigliato nella chat claude.ai.
2. Sul Mac, dopo il merge: app **Tailscale** (Mac App Store) con accesso; sul telefono la stessa app con lo **stesso account**; poi `cd ~/Gas && git pull && bash scripts/crm/telefono.sh`. La prima volta Tailscale può stampare un link per attivare HTTPS: aprirlo, premere «Enable» e rilanciare. Sul telefono aprire l'indirizzo stampato, inserire il token, salvarlo nella schermata Home.
3. Dalla fetta precedente: `bash scripts/crm/installa.sh` sul Mac (se non già fatto) e il controllo del `.env` della voce (`GAS_ASCOLTO_SOGLIA_INTERRUZIONE`).

---

## §1 SCOPE & ESITO FETTE

- **Dashboard anche dal telefono** (richiesta dell'operatore: «sì fallo, voglio vederla anche dal telefono. magari qua sul mac mettimi pure un collegamento diretto al desktop»; decisione 21): FATTA (e970daef, review #860 e #861 APPROVATO CON RISERVE). `scripts/crm/telefono.sh` con `tailscale serve`; il server accetta solo il nome `*.ts.net` del Mac sulla 443 e rifiuta il funnel; cookie `Secure`; `spegni.sh` spegne anche il telefono. R-860-1 MEDIA (funnel accettato) e R-860-2..5 chiuse in e970daef.
- **R-861-1 e R-861-2** (spegni che diceva «OK» con il collegamento ancora attivo; test sui collegamenti di altri servizi): FATTE in 23773556 (review #862).
- **Collegamento sulla Scrivania del Mac**: c'era già (icona «CRM Gas» creata da `installa.sh`); nessuna modifica.
- **Prova con un Tailscale vero, launchd vero e bash 3.2 del Mac**: SALTATA — il Mac non è raggiungibile da qui; comandi della CLI controllati sul sorgente di Tailscale v1.106.1 e provati con un Tailscale finto.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   8 +
 modules/crm/__main__.py            |   6 +-
 modules/crm/server.py              |  50 +++++-
 reports/crm/decisioni.md           |   4 +
 reports/crm/guida.md               |   9 ++
 reports/diff_sessione.md           |  21 ++-
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 +-
 reports/ultimo_report.md           |  37 ++---
 scripts/crm/spegni.sh              |   7 +
 scripts/crm/telefono.sh            | 277 ++++++++++++++++++++++++++++++++
 tests/test_unit_crm.py             | 312 +++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale. Base: main b100f8d4.

## §3 GIT LOG --ONELINE (sessione)

```
e970daef feat(crm): dashboard anche dal telefono, solo nella rete privata Tailscale (decisione 21) — nome *.ts.net ammesso solo sulla 443, richieste dal funnel rifiutate, cookie Secure, scripts/crm/telefono.sh (review #860, #861)
23773556 fix(crm): telefono.sh spegni non dice «OK» se qualcosa resta acceso (uscita 2, riavvio anche senza porta), test sui collegamenti di altri servizi (R-861-1, R-861-2; review #862)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Commit e970daef — review #860 (verdetto integrale, primo giro)

## VERDETTO: APPROVATO CON RISERVE

Review #860. Ho controllato il diff staged del ramo claude/nifty-galileo-3k7kbm sopra b100f8d4: 6 file, +451/−5, sha256 57f581755f05…, ricalcolato e identico al tuo prima e dopo la review. Ho letto CLAUDE.md (sez. 1, 5, 8, 9 e 10), le parti di `reports/stato_progetto.md` sul CRM e le lezioni della memoria su Host, CSRF, `.env`, `set -e`/pipefail e installer. Nella memoria ho aggiunto la riga #860 e due lezioni: il file è fuori dallo stage e non è committato, come hai chiesto. Non ho creato `.claude/.review_ok`. Non ho trovato violazioni del Wall of Shame: il kernel non è toccato, non c'è slicing della history e non c'è simulazione di tool. Le eccezioni del server finiscono in gas_debug.log come prima, e un nome non valido viene scartato con un warning, senza crash.

**Elementi del diff esaminati**
- `modules/crm/server.py:450` — ammette il nome Tailscale solo se è uguale, carattere per carattere, a quello dichiarato. Rischio esaminato: DNS rebinding e nomi vicini. Ho fatto la prova sul server staged. Danno 403: `x.NOME`, `NOME.evil.example`, `tail1234.ts.net`, `ts.net`, `NOME.` (col punto finale), `NOME:1:2`. Le maiuscole vengono ridotte e il nome passa. Il bind resta solo loopback (`modules/crm/server.py:936`, invariato). Una richiesta con Origin di un'altra macchina della stessa tailnet riceve 403. — **ok**, salvo la porta e il funnel (R-860-1).
- `modules/crm/server.py:78` — `nome_tailscale_da_env`: regex completa, lunghezza massima 253, minuscolo, punto finale tolto; un nome non valido dà None e un warning senza valori. Rischio esaminato: un dominio pubblico o una regex lenta. Le etichette non contengono punti, quindi la regex non torna indietro all'infinito. Il `.env` viene caricato prima (`modules/crm/__main__.py:121`, dopo `_carica_chiavi` in `main`). — **ok**
- `modules/crm/server.py:464` — mette `; Secure` sul cookie di login e di logout solo quando l'Host è il nome Tailscale. Rischio esaminato: cookie in chiaro. Il mutante «Secure sempre» viene preso dai test; sul Mac, in loopback, il cookie resta come prima. — **ok**
- `scripts/crm/telefono.sh:160` — controlla il funnel solo all'accensione, solo sulla porta 443 e solo nella configurazione `--bg` principale. Rischio esaminato: che il funnel resti acceso. — **riserva** R-860-1.
- `scripts/crm/telefono.sh:144` — il ramo `spegni`. Rischio esaminato: «spegni» che non spegne. — **riserva** R-860-2.
- `scripts/crm/telefono.sh:74` — `stato_serve`: se la lettura del JSON fallisce, la risposta diventa «libero». — **riserva** R-860-5.
- `scripts/crm/telefono.sh:94` — `scrivi_env`. Segue il symlink con realpath, scrive prima un file temporaneo con permessi 0600, poi applica i permessi originali, toglie anche le righe `export`. Rischi esaminati: segreti, permessi, symlink. Provato: il token non compare mai in output né nel registro (anche il test lo controlla). — **ok** con note cosmetiche.
- `scripts/crm/telefono.sh:180` — dopo `serve` rilegge la configurazione e, se non è quella attesa, toglie tutto. È l'unica protezione nel caso reale in cui la CLI esce con codice 0 senza applicare nulla. — **ok** come codice, ma senza test (R-860-4).
- `tests/test_unit_crm.py:3000` e `tests/test_unit_crm.py:3094` — coprono nomi ammessi e rifiutati, Host estranei, Secure, accendi/stato/spegni e `.env` collegato. Sulla CI Ubuntu i comandi finti sono nel PATH e il python è indicato con percorso assoluto, senza rete né attese vere: niente di fragile. — **ok**
- Contesto, file non toccato: `scripts/crm/spegni.sh:6` toglie il servizio ma non tocca `tailscale serve`. — **riserva** R-860-3.

**Riserve**
- **R-860-1 MEDIA** — Il server accetta il nome Tailscale anche dal traffico funnel, cioè da internet, su qualsiasi porta. Provato: Host `NOME:8443` con `Tailscale-Funnel-Request: ?1` dà login 200 e `/api/stato` 200. Prima di questo diff qualunque funnel verso il CRM prendeva 403 sull'Host. Lo script vede solo `AllowFunnel["NOME:443"]` in `--bg`, e solo al momento dell'accensione: non vede un `tailscale funnel 8770` lanciato in primo piano (che è il comportamento normale della CLI e finisce in `Foreground`), né i funnel su altre porte o accesi dopo. Resterebbe solo il token, con il limite tentativi condiviso: chiunque da internet potrebbe bloccare l'operatore per 15 minuti. Correzione da una riga, da fare in questa fetta prima del merge: 403 e log per ogni richiesta che porta l'header `Tailscale-Funnel-Request`, più un test. tailscaled mette quell'header su ogni richiesta funnel e cancella quelli finti, varianti con `_` comprese (l'ho verificato nel sorgente v1.106.1, `ipn/ipnlocal/serve.go`, righe 1162-1175). Facoltativo: accettare il nome solo senza porta o con `:443`. Resterebbe scoperto il funnel TCP grezzo (`--tcp`): va dichiarato nella guida.
- **R-860-2 BASSA** — `spegni` è fragile, in tre modi:
  - (a) Prima di fare qualsiasi cosa vuole Tailscale acceso, collegato e col nome valido. Provato con `TS_STATO=Stopped`: rc 1 e la riga resta nel `.env`, mentre la configurazione `--bg` resta salvata in Tailscale e torna attiva al login successivo.
  - (b) `nostro)` non riconosce lo stato `nostro pubblico`. Provato: serve e funnel restano accesi e lo script stampa «OK: accesso dal telefono spento». I dati restano protetti solo perché, dopo il riavvio, il CRM rifiuta l'Host.
  - (c) Se `serve ... off` fallisce, con `set -e` lo script esce senza messaggio e senza togliere la riga.
  - Correzione: togliere sempre la riga e riavviare comunque, usare il pattern `nostro*`, mettere `|| echo ATTENZIONE`.
- **R-860-3 BASSA** — `scripts/crm/spegni.sh` lascia sia `tailscale serve` (che punta alla porta del CRM in loopback) sia la riga nel `.env`. Qualunque programma ascolti dopo su quella porta (la demo, un `serve` lanciato a mano, un altro programma) diventa visibile alla tailnet, e la guida non lo dice.
- **R-860-4 BASSA** — Manca il test per il primo avvio reale: con HTTPS non attivo e `!ShouldWait`, la CLI stampa il link ed esce 0 senza applicare nulla (sorgente: `serve_legacy.go`, righe 829-834). L'ho provato: rollback corretto, ma il mutante che toglie il controllo di `scripts/crm/telefono.sh:180` sopravvive (21 passed). Inoltre il messaggio «non è quella attesa (libero)» non dice di attivare HTTPS e rilanciare, mentre la guida promette «prosegue da solo».
- **R-860-5 BASSA** — Se il JSON di `serve status` non si legge, il risultato è «libero» invece di «errore», quindi il controllo sul funnel lascia passare. Provato con un testo di prova davanti al JSON: rc 0 e `serve --bg` eseguito. Il danno è attenuato perché il vero `serve --https=443` toglie il funnel su quella porta (`serve_v2.go`, righe 1369-1381).
- **COSMETICHE**
  - Il filtro del `.env` è più stretto del caricatore del kernel: provato, una riga `GAS_CRM_NOME_TAILSCALE = x` sopravvive a `spegni`, e col «vince la prima riga» batterebbe quella aggiunta.
  - Nessun fsync prima di `os.replace` sul file che contiene tutti i segreti.
  - `spegni` senza `.env` ne crea uno vuoto.
  - Il mutante «senza chmod» sopravvive: lo 0600 di mkstemp va nella direzione sicura.
  - `curl | grep -q` con pipefail alla riga 190 (lezione R-615-7): al massimo dà un falso ATTENZIONE.
  - Col nome Tailscale è ammesso anche un Origin `http://`: il CSRF resta bloccato da X-Gas-CRM e dall'assenza di risposta a OPTIONS.
  - Se ts.net è nella Public Suffix List, le macchine della tailnet sono lo stesso «sito»: SameSite=Strict non le separa, la difesa sono Origin e X-Gas-CRM (provato 403); un'altra macchina potrebbe coprire il cookie di sessione, cioè impedire di restare collegati, senza rubare nulla.
  - La guida potrebbe citare Tailnet Lock, perché chi entra nella tailnet lo decide il server di coordinamento di Tailscale.

Le tue affermazioni sul sorgente Tailscale v1.106.1 le ho verificate tutte: Host conservato (`serve.go:1008`), X-Forwarded-Proto, `serve status --json` che stampa la ServeConfig, `serve` e `off` che tolgono il funnel su quella porta. Ho rieseguito io: 184 passed (186 con le mie 2 sonde), `bash -n` ok, mypy 0 errori in `modules/crm` (77 in tutto, come a HEAD). Mutanti: 6 su 8 uccisi.

**Rischi esplicitamente esclusi**
- Lo script non l'ho eseguito con bash 3.2 di macOS (`#!/bin/bash` sul Mac): qui c'è solo bash 5.2. Lo stesso costrutto heredoc dentro `$( )` è già in `scripts/crm/installa.sh`.
- Non ho usato un Tailscale reale né `launchctl kickstart -k` vero (i tempi del riavvio): ho solo il sorgente e i comandi finti.
- Non ho verificato che ts.net sia nella Public Suffix List.
- Non ho potuto controllare dove la CLI stampa l'avviso di versione diversa (stdout o stderr), che riguarda R-860-5: il sorgente scaricato contiene solo `cmd/` e `ipn/`.

File utili:
- /home/user/Gas/.claude/agents/memoria_revisore.md (riga #860 in coda, non nello stage)
- /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/r860/test_sonde_860.py (sonde su Host, funnel, CSRF e blocco tentativi)
- /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/r860/test_sonde_script_860.py (sonde su HTTPS non attivo, spegni con funnel o con Tailscale spento, JSON illeggibile, forma `CHIAVE = v`)
- /tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/r860/mutanti.sh (gli 8 mutanti, girati su una copia dell'indice)

### Commit e970daef — review #861 (verdetto integrale, secondo giro sullo stesso commit)

## VERDETTO: APPROVATO CON RISERVE

Review #861. Ramo claude/nifty-galileo-3k7kbm sopra b100f8d4, diff in stage: 7 file, +611/−6, sha256 ea7d48d4… (ricontrollato a fine review, invariato). Prima della review ho letto CLAUDE.md, le parti di reports/stato_progetto.md che riguardano la fetta e la memoria del revisore (lezioni su pipefail e set -e, #860).

Le correzioni di R-860-1…5 ci sono e sono provate. I rilievi rimasti sono tutti BASSI: niente si apre a internet, l'esposizione residua resta dentro la rete Tailscale e il token resta necessario. Le due riserve riguardano lo spegnimento, che in alcuni casi lascia il collegamento attivo e stampa lo stesso «OK».

### Elementi del diff esaminati
- `modules/crm/server.py:441` — rifiuta ogni richiesta che ha l'header `Tailscale-Funnel-Request`, prima del controllo dell'Host. Rischio esaminato: traffico funnel con Host falsificato (nome Tailscale, loopback, IP). Ho controllato che `headers.get` non distingue maiuscole e minuscole e che un valore vuoto viene rifiutato. I test provano il 403 sia col nome sia con loopback. — ok
- `modules/crm/server.py:457` — accetta il nome Tailscale solo senza porta o con `:443`. Rischio esaminato: il nome servito su un'altra porta (`:8443` → 403, testato) e il cookie `Secure` collegato al nome. — ok
- `scripts/crm/telefono.sh:191` — `leggi_nome || case $? in …`. Rischio esaminato: che `$?` sia davvero quello di `leggi_nome`. L'ho provato a parte sotto `set -euo pipefail` (i codici 3, 5 e gli altri finiscono in rami distinti, 141 in «altro»). Il mutante «`return 2` al posto di `return $?`» viene ucciso. Dentro le funzioni chiamate in `if` o `||` errexit è spento: ogni passo di `leggi_nome` (`scripts/crm/telefono.sh:80`) e di `leggi_porta` ha il suo `|| return` esplicito. `local j` è separato dall'assegnazione, quindi l'exit code non si perde. — ok
- `scripts/crm/telefono.sh:160` — `spegni` con la porta illeggibile. Rischio esaminato: CRM che resta acceso col nome e collegamento lasciato. Provato coi comandi finti (python che esce 4 su `import gas`): la riga del .env viene tolta, ma il CRM non viene riavviato (kickstart 0, anche se `kickstart -k` non ha bisogno della porta) e il collegamento resta. Lo script stampa «ATTENZIONE: non riesco a leggere la porta», poi «OK: accesso dal telefono spento» ed esce 0. — riserva (R-861-1)
- `scripts/crm/telefono.sh:180` — `serve off` che fallisce. Provato: stampa ATTENZIONE, poi lo stesso «OK…» ed esce 0, col collegamento ancora attivo. Stesso esito con `errore` (`scripts/crm/telefono.sh:182`). `scripts/crm/spegni.sh:14` si basa sull'exit code e quindi non avvisa. — riserva (R-861-1)
- `scripts/crm/telefono.sh:134` — riconosce il collegamento «nostro» (`bool(dest)`, un solo gestore `/`, Proxy uguale alla destinazione). Rischio esaminato: che lo spegnimento tolga un collegamento non del CRM. Con il codice com'è, provato coi finti: un'altra porta, il nostro più un secondo gestore, la porta come prefisso (87700), un sotto-percorso e `https+insecure` non vengono toccati. Anche un gestore di testo con la porta illeggibile viene lasciato. — ok nel comportamento; riserva sui test (R-861-2)
- `scripts/crm/telefono.sh:129` — `pubblico` controlla AllowFunnel su ogni porta del nome, anche nelle configurazioni Foreground. Il JSON illeggibile o non oggetto dà «errore» (`scripts/crm/telefono.sh:121`). Rischio esaminato: tipi annidati sbagliati, per esempio `Web` come lista non vuota. In quel caso Python va in traceback e `set -e` ferma lo script. All'accensione (`scripts/crm/telefono.sh:214`) si ferma prima di toccare qualcosa; con un tailscaled vero non può succedere. — ok (cosmetica)
- `scripts/crm/telefono.sh:54` — il filtro del .env toglie anche le forme `export ` e `CHIAVE = v`. L'ho confrontato con `gas.py:984` (`_carica_dotenv`): le regole coincidono. fsync e `os.replace` ok, il .env collegato resta collegato, senza .env non ne crea uno. — ok
- `scripts/crm/telefono.sh:238` — se dopo `serve` la configurazione non è la nostra, toglie tutto e dice di rilanciare (R-860-4); il test è `tests/test_unit_crm.py:3231`. Il ramo «nostro pubblico» (`scripts/crm/telefono.sh:240`) è senza test: il mutante sopravvive, ma il caso si presenta solo se qualcosa cambia la configurazione fra due letture ravvicinate. — ok (cosmetica)
- `scripts/crm/spegni.sh:12` — dopo il bootout chiama `telefono.sh spegni` se nel .env c'è la riga o se Tailscale è installato; il test è `tests/test_unit_crm.py:3241`. — ok
- Codice vero di `leggi_porta` (nei test è sostituito dal python finto): eseguito su questa macchina con `env -i`, stampa solo «8770» e nient'altro su stdout. — ok

### Riserve
- **R-861-1 BASSA** — `spegni` stampa «OK: accesso dal telefono spento» ed esce 0 anche quando il collegamento resta: `serve off` fallito, configurazione illeggibile, porta illeggibile. Con la porta illeggibile il CRM non viene nemmeno riavviato, quindi tiene il nome in memoria finché non riparte. Correzione proposta:
  1. con la porta illeggibile fare comunque `launchctl kickstart -k`;
  2. in quei casi niente «OK» finale ed exit diverso da 0, così `spegni.sh` avvisa.
- **R-861-2 BASSA** — la condizione `bool(dest)` (`scripts/crm/telefono.sh:134`) è proprio quella che impedisce a `spegni`, con la porta illeggibile, di togliere un collegamento di un altro servizio. Non ha test. Mutante provato: con «senza `bool(dest)`» e un gestore di solo testo `off` viene chiamato e la configurazione dell'altro sparisce, eppure i 28 test di telefono.sh restano verdi. Restano vivi anche i mutanti «`"/" in gestori`» e «`startswith` al posto di `==`». Serve un test con porta illeggibile e gestore senza Proxy, più un caso con due gestori.

### Note cosmetiche
- `spegni` non avvisa quando sulla 443 c'è un altro servizio, nemmeno se è un vecchio collegamento del CRM a una porta poi cambiata.
- Con un nome non `ts.net` dice «Tailscale è spento».
- Dopo un cambio di nome del Mac il collegamento sotto il vecchio nome resta, con «OK». È innocuo: il vecchio nome non risolve più e il CRM non lo accetta.
- `stato` dice «Acceso» anche dopo uno `spegni` fatto con Tailscale spento (.env già pulito, il CRM risponde 403).
- Lanciato da `spegni.sh`, il messaggio parla dell'icona «CRM Gas» appena tolta.
- Attraverso `serve` un dispositivo della rete Tailscale che usa curl può mettere un IP nell'Host e superare quel controllo, che protegge dal DNS rebinding e non dagli accessi. Restano il token e il limite ai tentativi; il messaggio «il CRM rifiuta già il telefono» vale per il browser.

### Altri controlli
- `python3 -m pytest -q tests/test_unit_crm.py`: 191 passed.
- `bash -n` ok su telefono.sh e spegni.sh.
- mypy: 0 errori in modules/crm (i 77 segnalati stanno in altri file e c'erano già).
- Miei mutanti su copie degli script, con un controllo letale che li ha confermati validi: uccisi «return 2», «spegni senza riavvio», «spegni senza off»; vivi M3 `bool(dest)`, M6 un solo gestore, M7 uguale→startswith, M11 rollback di «nostro pubblico» dopo `serve`.

### Rischio esplicitamente escluso
Non ho verificato:
- **Tailscale vero sul Mac**: app del Mac App Store, formato reale di `serve status --json` sulla versione dell'operatore, link per attivare HTTPS, certificato, curl dal Mac verso il proprio nome. Qui non è riproducibile: solo comandi finti.
- **La bash 3.2 di macOS**: qui c'è solo la 5.2. Il rischio è attenuato perché si usano gli stessi costrutti di `scripts/crm/installa.sh` (heredoc dentro `$( )`, regex senza virgolette).
- **launchd vero.**
- **Il sorgente di tailscaled**: non l'ho riletto. Che l'header funnel venga tolto dalle richieste non funnel e che l'Host resti quello originale lo prendo dalla lettura di #860.

### Memoria
- Riga #861 e due lezioni aggiunte in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, fuori stage.
- NON ho committato, come richiesto, quindi `scripts/commit_memoria_revisore.sh` non è stato eseguito.
- Nessun `.claude/.review_ok` creato.

File di prova usati: `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/prove.py`, `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/mutanti.sh`, `/tmp/claude-0/-home-user-Gas/16f9e0da-27ed-55e3-a7eb-e49dca6663b0/scratchpad/prova_m3.py`.

### Commit 23773556 — review #862 (verdetto integrale)

## VERDETTO: APPROVATO CON RISERVE

Review #862: secondo giro della #861 sul ramo claude/nifty-galileo-3k7kbm, sopra e970daef. Il diff staged è quello indicato: 2 file, +68/−20, sha256 6a42d4d3, ricontrollato prima e dopo la review. Prima della review ho letto CLAUDE.md (sezioni 5, 8 e 10), la voce «Dashboard del CRM anche dal telefono» di reports/stato_progetto.md e le lezioni della mia memoria sugli script shell, `set -e` e gli spegnimenti.

**Prove fatte**
- Su una copia dell'indice (checkout-index nello scratchpad): `pytest tests/test_unit_crm.py` dà 195 passed; `bash -n` ok.
- 12 mutanti eseguiti, più un mutante di controllo noto letale (ucciso). Ne è sopravvissuto uno solo (vedi R-862-1).
- Sonde a mano con i comandi finti dei test: spegni.sh con Tailscale spento e con il telefono acceso, spegni senza Tailscale, porta illeggibile con o senza Tailscale, configurazione illeggibile, «nostro pubblico», tipi errati nel JSON, porta illeggibile con il CRM non installato, kickstart fallito.

**Elementi del diff esaminati**
- `scripts/crm/telefono.sh:159` — `PARZIALE=no` in testa al ramo spegni e uscita 2 a scripts/crm/telefono.sh:200. Rischio: un «OK» detto quando qualcosa resta acceso. PARZIALE viene alzato in sei punti: porta illeggibile, `serve off` fallito, configurazione illeggibile, funnel, Tailscale spento o senza accesso, nome non ts.net. Mutanti uccisi: «PARZIALE tolto» su porta, off, funnel e Tailscale spento; «exit 2 → 0»; «PARZIALE=si iniziale». — ok
- `scripts/crm/telefono.sh:169` — senza porta: avviso, PARZIALE e `launchctl kickstart -k` con `|| echo` (scripts/crm/telefono.sh:171), senza attendere la porta. Rischio: `set -e` che ferma lo script, oppure un riavvio mancato. Provato: kickstart fallito → due avvisi e uscita 2; CRM non installato → nessun kickstart e uscita 2. Il mutante «senza kickstart» è ucciso dal test. — ok
- `scripts/crm/telefono.sh:184` — ramo `errore` (configurazione di Tailscale illeggibile) che alza PARZIALE. Rischio: ramo senza test. Il mutante «errore senza PARZIALE» resta VIVO (34 passed). A mano il comportamento è giusto: avviso e uscita 2. — riserva (R-862-1)
- `scripts/crm/telefono.sh:202` — il nuovo messaggio OK finale dà l'indirizzo locale invece dell'icona. Rischio: messaggio falso. Nel flusso di spegni.sh è falso: provato, stampa «la dashboard resta su …:8770/» e subito dopo spegni.sh scrive «OK: CRM spento e tolto dall'avvio». — riserva cosmetica
- `tests/test_unit_crm.py:3077` — il python finto esce 4 sulla lettura della porta se esiste `$HOME/porta_ko`. Rischio: un'altra chiamata intercettata per errore. scrivi_env non contiene «import gas», stato_serve e leggi_nome usano `-c`, e HOME passa a leggi_porta con `env -i HOME=`. — ok
- `tests/test_unit_crm.py:3257` — test con tre casi (gestore di testo con porta illeggibile; nostro più un secondo gestore; porta 87700 come prefisso). Rischio: guardie senza test. Uccisi «senza bool(dest)», «"/" in gestori» e «startswith». I casi 2 e 3 però non controllano il codice di uscita (atteso 0). — ok, con nota cosmetica
- `tests/test_unit_crm.py:3276` — test con `serve off` fallito. Rischio: test che passa a vuoto se la sostituzione nel finto non combacia. Non succede: in quel caso l'off riesce, l'uscita è 0 e il test diventa rosso. Il mutante «off fallito senza PARZIALE» è ucciso. — ok
- `tests/test_unit_crm.py:3191` e `tests/test_unit_crm.py:3204` — test esistenti aggiornati da uscita 0 a uscita 2 (Tailscale spento; funnel). Sono i soli rami cambiati di proposito. Gli altri casi già approvati restano a 0: tests/test_unit_crm.py:3122 (spegni dopo l'accensione), tests/test_unit_crm.py:3212 (senza .env), tests/test_unit_crm.py:3251 (spegni.sh). Provato anche il caso senza Tailscale con porta leggibile: uscita 0. — ok
- Contesto, file non toccato: `scripts/crm/spegni.sh:14` — `set -uo pipefail` senza `-e` (scripts/crm/spegni.sh:4), poi `telefono.sh spegni || echo ATTENZIONE`. Provato con Tailscale spento: telefono.sh esce 2, spegni.sh stampa «ATTENZIONE: accesso dal telefono non spento», poi l'OK del CRM, e chiude con uscita 0. Reagisce bene. — ok

**Riserve**
- R-862-1 BASSA: il ramo `errore` dello spegni (scripts/crm/telefono.sh:184) non ha test; il mutante che toglie il PARZIALE sopravvive. Correzione: un caso di spegni con il contenuto `"Warning\n{}"` in `registro.txt.serve` che si aspetti uscita 2 e «non riesco a leggere la configurazione».
- COSMETICA (la cosmetica dell'icona della #861 resta aperta in altra forma): l'OK di scripts/crm/telefono.sh:202 dice che la dashboard resta sull'indirizzo locale anche quando lo lancia spegni.sh, che ha appena spento il CRM. Correzione: dirlo solo se `crm_installato`.
- COSMETICA: con Tailscale installato ma spento, spegni.sh dà sempre tre avvisi («il collegamento resta salvato», «SOLO IN PARTE», «non spento»), anche se il telefono non è mai stato acceso. La prudenza è giusta perché lo script non può saperlo, ma il testo afferma invece di dire «se c'è».
- COSMETICA: con «nostro pubblico» e il funnel solo sulla 443, dopo `serve off` lo script avvisa comunque del funnel ed esce 2. Nel finto la configurazione dopo l'off è `null`; il fatto che off tolga anche il funnel di quella porta l'avevo ricavato dal sorgente di Tailscale nella #860. È un falso allarme nella direzione prudente; correzione: rileggere `stato_serve` dopo l'off.
- COSMETICA, già nella #861: con tipi annidati errati nel JSON (es. `Handlers` lista) esce un traceback, uscita 1 senza «SOLO IN PARTE». spegni.sh avvisa comunque, e la riga del .env è già tolta.

**Rischio escluso**: Tailscale vero e la bash 3.2 del Mac non sono provati, perché l'ambiente è Linux con comandi finti. Rispetto alla #861 non entrano costrutti nuovi di bash 4: solo `if !`, `case` annidati e `||`. Non ho riletto modules/crm/server.py, che non è nel diff.

Nessun antipattern del Wall of Shame (né slicing della storia né simulazione di tool). Gas.py, i provider e i guardrail non sono toccati.

Memoria: in coda a /home/user/Gas/.claude/agents/memoria_revisore.md ho aggiunto la riga contatore #862 e una lezione nuova (il messaggio finale di uno script richiamato da un altro va provato nell'output combinato). Il file è fuori stage e NON committato, come hai chiesto. Lo stage è invariato (sha256 6a42d4d3). Non ho creato .claude/.review_ok e non ci sono IP letterali né qui né nella memoria.

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_crm.py`: 173 → 195 passed. Nuovi: nomi Tailscale ammessi e rifiutati, Host del funnel e su porte diverse da 443 rifiutati, cookie `Secure`, e 20 casi di `telefono.sh`/`spegni.sh` con comandi finti (accendi, stato, spegni, funnel, altri servizi, JSON illeggibile, HTTPS da attivare, serve fallito, .env collegato, porta illeggibile).
- Suite del kernel non toccata (gas.py e test del kernel invariati).

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST.
- Mappatura commit→run:
  - Commit della sessione e commit di fine-task: run non ancora disponibile alla scrittura dell'handoff (il ramo si pusha col commit di fine-task).
- Ultima run nota su main b100f8d4 (merge della #404): CI verde al merge.

## §7 RISERVE APERTE

- R-862-1 BASSA: nessun test per il ramo «configurazione illeggibile» dello spegni.
- COSMETICHE #860/#861/#862: in `reports/stato_progetto.md`.
- Dalla PR #404: V-1/V-2 BASSE e V-3 COSMETICA del bot, V-1 BASSA della 3ª verifica esterna, R-859-1 BASSA, R-859-2 COSMETICA, R-854-2 BASSA: in `reports/stato_progetto.md`.
- R-852M-1 BASSA (voce) e riserve della #401 (funnel): in `reports/stato_progetto.md`.
- Script non provati con un Tailscale vero, launchd vero e bash 3.2.
