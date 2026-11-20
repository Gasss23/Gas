# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-19/20 — CRM fetta 6: copia di sicurezza cifrata su iCloud Drive e ripristino, giro del motore 2 volte al giorno, parole vietate più ampie; rifiniture dopo bot e verifica esterna su #386

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #386 (https://github.com/Gasss23/Gas/pull/386), con l'etichetta «verifica». Il merge lo decide l'operatore.
   - Sul commit ee38220c il bot V-B era failure per un finding MEDIA: copia esterna che fallisce senza che nessuno lo veda. È chiuso in e2c6e95a (review #820). La verifica esterna, 2° giro, era APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/386#issuecomment-7026183842), con V-1/V-2 chiuse in 7b652af1 (review #819).
   - Riserva aperta: R-820-1 BASSA.
2. Password delle copie cifrate: nel `.env` del Mac `GAS_CRM_BACKUP_PASSWORD` (almeno 12 caratteri), salvata anche nel gestore di password.
3. Verificare che la cartella di Gas sia `~/Gas`, fuori da Scrivania e Documenti sincronizzate con iCloud.
4. Server gratuito per il CRM (Tailscale col Mac acceso, oppure Oracle Cloud «Always Free»): da decidere.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 6a — copia cifrata fuori dal Mac (iCloud Drive) e ripristino**: FATTA, commit 32282b6f. Review #815-CRM APPROVATO CON RISERVE (R-815-1 MEDIA) → #816-CRM APPROVATO CON RISERVE (R-816-1 COSMETICA).
- **Fetta 6b — giro del motore 2 volte al giorno**: FATTA (stesso commit).
- **Fetta 6c — parole vietate più ampie e docstring** (note del bot e della verifica esterna #381 rimandate il 19-11): FATTA (stesso commit).
- **Fetta 6d — rifiniture dopo bot e verifica esterna su #386** (V-1..V-4 della verifica, V-1..V-3 del bot, R-816-1): FATTA, commit 17aee558.
  - Password in forma NFC.
  - Una copia esterna al giorno, per 30 giorni.
  - File 0600.
  - Nessun temporaneo lasciato, con un nome temporaneo unico per ogni copia.
  - Il ripristino toglie il file se il ricontrollo finale fallisce.
  - Review #817-CRM APPROVATO CON RISERVE (R-817-1 BASSA: temporaneo condiviso fra due copie dello stesso giorno) → #818-CRM APPROVATO.
- **Fetta 6e — note della verifica esterna #386 (2° giro) e del bot V-B su ee38220c**: FATTA.
  - Commit 7b652af1, review #819-CRM APPROVATO: disco pieno nel ripristino senza temporanei in chiaro; collegamento pendente trattato come «esiste già».
  - Commit e2c6e95a, review #820-CRM APPROVATO CON RISERVE (R-820-1 BASSA):
    - prova vera di scrittura all'avvio;
    - esito dell'ultima copia in dashboard e in `/api/stato`, con avviso se fallisce;
    - password di prima nel ripristino;
    - segnaposto `.icloud` spiegato.
- **Server per il CRM**: DEFERITA. Niente spese per un server solo per il CRM (decisione dell'operatore); alternative gratuite da decidere.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   8 +++++++
 modules/crm/__init__.py            |   6 ++++--
 modules/crm/__main__.py            |  60 +++++++++++++++++++++++++++++++++++++++++++++++----
 modules/crm/copia_cifrata.py       | 275 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/scrittore.py           |  11 ++++++----
 modules/crm/server.py              |  39 ++++++++++++++++++++++++++++++---
 modules/crm/store.py               |   1 +
 modules/crm/web/app.css            |   3 +++
 modules/crm/web/app.js             |  10 +++++++++
 reports/crm/decisioni.md           |   6 ++++++
 reports/crm/guida.md               |  14 +++++++++---
 reports/diff_sessione.md           |  23 +++++++++++---------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  49 +++++++++++++++++++++++++++++++++---------
 requirements.txt                   |   2 ++
 tests/conftest.py                  |   4 ++++
 tests/test_unit_crm.py             | 345 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base della sessione: c4c8c31f (origin/main, dopo il merge della PR #381).

## §3 GIT LOG --ONELINE (sessione)

```
e2c6e95a fix(crm): esito della copia su iCloud sempre visibile — prova vera all'avvio, indicatore in dashboard, avviso se fallisce; password di prima nel ripristino; file iCloud non scaricato spiegato
046d87ea chore(revisore): memoria review #820 — APPROVATO CON RISERVE
7b652af1 fix(crm): ripristino con disco pieno senza temporanei in chiaro; collegamento pendente = «esiste già» (V-1/V-2 verifica esterna #386, 2° giro) — review #819 APPROVATO
7b8269ad chore(revisore): memoria review #819 — APPROVATO
ee38220c docs(fine-task): CRM fetta 6 — rifiniture dopo bot e verifica su #386, review #817/#818
17aee558 fix(crm): copie cifrate rifinite — una al giorno, password NFC, file 0600, niente temporanei lasciati, ripristino che toglie il file rovinato
37972ed5 chore(revisore): memoria review #818 — APPROVATO
8b0b5b44 chore(revisore): memoria review #817 — APPROVATO CON RISERVE
ebf645db docs(fine-task): handoff — PR #386 aperta con l'etichetta verifica; §2/§3 rigenerati
4cec29d0 docs(fine-task): CRM fetta 6 — copia cifrata su iCloud, ripristino, giro 720 min; review #815/#816
32282b6f feat(crm): copia di sicurezza CIFRATA su iCloud Drive e ripristino; giro del motore 2 volte al giorno; parole vietate più ampie
f40aa49f chore(revisore): memoria review #816 — APPROVATO CON RISERVE
be656bb7 chore(revisore): memoria review #815 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #815-CRM (1° giro, diff staged della fetta 6)

## VERDETTO: APPROVATO CON RISERVE

Review #815-CRM sul diff staged (8 file, +306/−14), ramo ripartito da main c4c8c31f. Severità piena: la fetta tocca la cifratura dei dati dei clienti.

**Esito in breve:** la cifratura è robusta e nessun dato esce in chiaro dal Mac. C'è però un difetto MEDIO nel ripristino (R-815-1): in un caso realistico produce un database corrotto e lo dichiara riuscito. Va chiuso prima di dire all'operatore che il ripristino è pronto.

**Verifiche rifatte da me:**
- Suite CRM: 124 passed. mypy pulito su modules/crm.
- Test nuovi contro il codice di main (c4c8c31f, con il file di test staged): falliscono esattamente i 6 dichiarati; gli altri 118 passano.
- Kernel e gas.py non toccati. Nessuno slicing della history, nessuna simulazione di tool.
- Prove a mano sulla cifratura e sul ripristino, descritte sotto.

### Riserve

**1. R-815-1 — MEDIA — il ripristino può restituire un database corrotto e dirlo riuscito.**
- **Dove:** `modules/crm/copia_cifrata.py:120`. Il controllo di integrità gira sul file temporaneo, ma nessuno guarda se accanto al percorso di destinazione è rimasto un journal (`-journal`, `-wal`) del database di prima.
- **Riprodotto:**
  1. un DB con 50 clienti va in crash a metà di una scrittura, e resta il suo `-journal`;
  2. l'operatore sposta il DB rotto (il journal è un file nascosto e resta lì);
  3. `ripristina` scrive la copia buona nel posto del DB e risponde «riuscito»;
  4. alla prima apertura SQLite applica il journal VECCHIO al file NUOVO.
- **Risultato:** `integrity_check` fallisce («row 1 missing from index idx_crm_clienti_tel»), dentro ci sono i 50 clienti del DB vecchio invece di quello ripristinato, e il journal sparisce.
- **Quando conta:** proprio dopo un crash o un DB rovinato sullo stesso Mac, cioè uno dei casi in cui si usa il ripristino.
- **Cosa resta salvo:** la copia cifrata non si tocca. Rifare il ripristino dopo aver tolto il journal funziona.
- **Rimedio:**
  - rifiutare il ripristino se esistono `dest-journal`, `dest-wal` o `dest-shm`, dicendolo all'operatore;
  - ricontrollare l'integrità DOPO lo spostamento finale, aprendo il file di destinazione;
  - un test con lo scenario sopra (crash, DB spostato, journal lasciato).

**2. R-815-2 — BASSA — il «non sovrascrive mai» non è garantito fino in fondo.**
- **Dove:** `modules/crm/copia_cifrata.py:124` controlla che la destinazione non esista all'inizio; poi, dopo scrypt, decifratura e controllo, `modules/crm/copia_cifrata.py:142` usa `os.replace`, che sovrascrive.
- **Il caso:** se nel frattempo il file nasce (per esempio `serve` avviato nello stesso momento, che crea il DB all'avvio), viene sovrascritto.
- **Rimedio:** `os.link(tmp, dest)` seguito dalla cancellazione del temporaneo: fallisce da solo se la destinazione esiste.

**3. R-815-3 — BASSA — parametri di scrypt bassi per un file attaccabile offline.**
- **Dove:** `modules/crm/copia_cifrata.py:76` usa n=2^15 (32 MiB, circa 80 ms misurati). È il livello «interattivo»; per file che un attaccante può copiare e provare con calma (un account iCloud violato) OWASP chiede almeno n=2^17.
- **Perché si può alzare:** la copia si fa una volta al giorno, quindi 2^17 o più non pesa.
- **Altro:** i parametri non sono scritti nell'intestazione, quindi cambiarli richiede una versione nuova di `MAGIA`, ed è già previsto con «-1».
- **Minore:** la lunghezza minima della password (`modules/crm/copia_cifrata.py:53`) si misura sul testo senza spazi ai bordi, ma la chiave si ricava dal testo così com'è.

**4. R-815-4 — BASSA — una cartella di rete appesa bloccherebbe il guardiano.**
- **Dove:** `copia_fuori` (`modules/crm/copia_cifrata.py:97`) gira dentro il thread del guardiano (`modules/crm/server.py:302`).
- **iCloud Drive:** è una cartella su disco locale (la sincronizzazione avviene dopo, in background), quindi un iCloud lento NON blocca. Lo stesso vale per la copia locale.
- **Il caso a rischio:** se `GAS_CRM_BACKUP_CIFRATO_DIR` punta a un disco di rete che si appende, il thread si ferma. Il server continua a rispondere, ma si fermano gli aggiornamenti in tempo reale e i giri del motore.
- **Rimedio:** un thread separato per la copia, oppure dichiararlo nella guida.

### Elementi del diff esaminati

- **Cifratura** (`modules/crm/copia_cifrata.py:76`, `modules/crm/copia_cifrata.py:80`, `modules/crm/copia_cifrata.py:85`): Fernet (AES-128-CBC con HMAC-SHA256 su IV e testo cifrato), chiave da 32 byte ricavata con scrypt, sale casuale da 16 byte per file. Provato:
  - nel file cifrato non compaiono né il nome del cliente, né `crm_clienti`, né l'intestazione SQLite;
  - password sbagliata, sale alterato e corpo alterato vengono tutti rifiutati con «password sbagliata o file rovinato».

  L'intestazione non è autenticata, ma alterarla rompe la chiave o il controllo di formato: non c'è un modo di farla accettare. Esito: ok, salvo R-815-3.
- **Nessun dato in chiaro fuori dal Mac, in ogni ramo** (`modules/crm/copia_cifrata.py:110`): si cifra PRIMA di scrivere, quindi se la cifratura fallisce non si scrive nulla. Il `.tmp` nella cartella esterna contiene già il cifrato. Senza password (anche troppo corta), senza cartella o senza `cryptography` la copia resta SPENTA e non si crea nemmeno la cartella (test dedicato). Nel log va solo il tipo d'errore. Esito: ok.
- **Ripristino** (`modules/crm/copia_cifrata.py:120`): decifratura, `integrity_check` e presenza di `crm_clienti` sul temporaneo, che viene cancellato se il controllo fallisce. Con la password sbagliata non resta nessun file. Il temporaneo in chiaro sta accanto alla destinazione (nella cartella del repo è coperto da `.gas_memory_crm*` nel `.gitignore`). Esito: riserve R-815-1 e R-815-2.
- **Isolamento nei test** (`tests/conftest.py:34`): la fixture toglie password e cartella, così le suite col guardiano non scrivono nell'iCloud vero dell'operatore. Sul Mac la cartella iCloud esiste, ma senza password la copia è spenta. Esito: ok.
- **Riga di comando** (`modules/crm/__main__.py:43`, `modules/crm/__main__.py:203`):
  - giro automatico ogni 720 minuti (decisione c); resta il giro a ogni cambio dei dati, ora che il file del CRM è separato e le scritture del kernel non lo fanno scattare;
  - `ripristina` prende la password dall'ambiente o la chiede con getpass, e intercetta ErroreCRM, OSError e la libreria mancante.

  Esito: ok.
- **Filtro delle parole vietate** (`modules/crm/scrittore.py:58`, `modules/crm/scrittore.py:129`): radici più larghe e spazi doppi compressi. La nota sul rischio («…garantiscono…») viene tolta prima del controllo, quindi non fa scattare il filtro. Nuovi falsi allarmi nel verso sicuro: «assicur» prende anche «ti assicuro che ti richiamo», «perder» anche «non vorrei perderti di vista». Già dentro R-810-2. Il test cambiato (`tests/test_unit_crm.py:1345` e `test_scrittore_opus`) fa lo stesso controllo con la radice nuova. Esito: ok.

### Rischi esplicitamente NON verificati

- Comportamento reale di iCloud Drive sul Mac (spazio ottimizzato, sincronizzazione dei `.tmp`): qui non c'è un Mac.
- Che la cartella di Gas o il DB non stiano dentro una cartella sincronizzata da iCloud («Scrivania e Documenti»). In quel caso il DB e le copie locali in chiaro uscirebbero comunque dal Mac. Va chiesto all'operatore.
- Custodia della password: sta nel `.env` del Mac (illeggibile agli strumenti di Gas, e i comandi in sandbox partono con un ambiente ripulito). Che l'operatore la salvi anche altrove, come dice la guida, non è verificabile.
- Documenti fuori stage (guida, decisioni 12–14): non letti.

### Note

- Riserve ancora aperte dai giri precedenti: R-810-2, R-810-3, R-804-2, R-804-4, R-803-9, R-803-10, R-808-5, R-808-6.
- Riga contatore #815-CRM e una lezione (journal rimasto accanto alla destinazione di un ripristino SQLite) aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (commit be656bb7). Il diff staged è intatto (8 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

### Review #816-CRM (2° giro, commit 32282b6f)

## VERDETTO: APPROVATO CON RISERVE

Review #816-CRM sul diff staged (8 file, +392/−14): secondo giro di #815, con severità piena perché tocca la cifratura dei dati dei clienti. Le riserve R-815-1..4 sono tutte chiuse; resta una sola riserva cosmetica (R-816-1).

**Verifiche rifatte da me:**
- Suite CRM: 125 passed. mypy pulito su modules/crm.
- Fail-before: ho ritrovato nel repo il `copia_cifrata.py` revisionato in #815 (blob fe4065e6). Con quello al posto del file nuovo, `test_r815_ripristino_sicuro_dopo_un_crash` fallisce; i due test della copia cifrata passano, come devono.
- Le mie due prove di corsa del giro precedente, sul codice nuovo:
  - il controllo dei file di lavoro e il nuovo controllo finale di integrità bloccano lo scenario del journal rimasto;
  - `ripristina` non sovrascrive un file che nasce mentre decifra (il test lo forza sostituendo `decifra`).
- scrypt con n=2^17: 353 ms misurati, una volta al giorno.
- Una password con spazi ai bordi nell'ambiente viene ripulita.
- Kernel e gas.py non toccati. Nessuno slicing della history, nessuna simulazione di tool.

**Elementi del diff esaminati:**
- `modules/crm/copia_cifrata.py:148` — PRIMA di decifrare, rifiuta se accanto a `dest` sono rimasti `-journal`, `-wal` o `-shm`, con un messaggio chiaro su cosa spostare. Esito: ok.
  - Rischio esaminato: un journal vecchio applicato al database ripristinato (il mio scenario di R-815-1).
  - Il test riproduce crash, database spostato e journal lasciato: rifiuta. Spostato anche il journal, il database ripristinato contiene solo il cliente della copia.
- `modules/crm/copia_cifrata.py:160` — posizionamento con `os.link`, che fallisce se `dest` esiste. Il `.tmp` viene tolto sempre (`modules/crm/copia_cifrata.py:171`). Esito: ok.
  - Rischio esaminato: sovrascrittura di un `dest` nato durante il ripristino. `FileExistsError` diventa ErroreCRM e `dest` resta intatto.
  - Il ripiego per file system senza collegamenti fisici (`modules/crm/copia_cifrata.py:166`) usa la creazione esclusiva «xb»: stesso verso sicuro.
- `modules/crm/copia_cifrata.py:173` — integrità e presenza di `crm_clienti` ricontrollate sul file vero, al suo posto. Esito: ok.
  - Rischio esaminato: un problema che nasce solo dopo il posizionamento. Se il controllo fallisce, il messaggio dice di non usare il file.
- `modules/crm/copia_cifrata.py:37` e `modules/crm/copia_cifrata.py:55` — `SCRYPT_N = 2**17`, il minimo indicato da OWASP; la password ripulita dagli spazi ai bordi si usa sia per il minimo sia per ricavare la chiave. Esito: ok.
  - Il formato «-1» resta invariato: nessuna copia è uscita col formato precedente.
- `modules/crm/server.py:310` — la copia esterna gira in un thread daemon a parte (`_copia_esterna`, `modules/crm/server.py:268`). Esito: ok.
  - Rischio esaminato: una cartella di rete appesa che ferma il guardiano.
  - La copia locale resta nel guardiano, ma è su disco locale.
  - Ogni copia ha un nome diverso (data e ora), quindi due thread che si sovrappongono non si pestano i piedi.
- `tests/test_unit_crm.py:1397` — test con crash vero (sottoprocesso, `cache_size=1`, `os._exit`) e con l'intreccio forzato della creazione di `dest`. Controlla anche che non restino `.tmp`. Esito: ok.

**Riserva:**

**1. R-816-1 — COSMETICA.**
- **Password chiesta a mano:** in `modules/crm/__main__.py:207` la password digitata con getpass non viene ripulita dagli spazi ai bordi, mentre quella dell'ambiente sì. Uno spazio digitato per sbaglio dà «password sbagliata».
- **Ripiego senza collegamenti fisici:** il ramo (`modules/crm/copia_cifrata.py:166`) non ha un test. Se la scrittura si interrompe a metà (disco pieno), lascia un file incompleto al posto di `dest`. Il controllo finale lo segnala («non usarlo»), ma il file resta, e un nuovo ripristino si ferma su «esiste già».
- Il caso normale (destinazione nella cartella del repo, su APFS) passa da `os.link` e non tocca questo ramo.

**Rischi esplicitamente NON verificati:**
- Ripristino su un file system senza collegamenti fisici (chiavetta exFAT, cartella di rete): qui non riproducibile.
- iCloud Drive vero sul Mac e posizione della cartella di Gas: secondo CLAUDE.md è `~/Gas`, fuori da Scrivania e Documenti. La domanda all'operatore annunciata nel riepilogo resta utile.
- Documenti fuori stage (guida, decisioni 12–14): non letti.

**Note:**
- Riserve ancora aperte da giri precedenti: R-810-2, R-810-3, R-804-2, R-804-4, R-803-9, R-803-10, R-808-5, R-808-6.
- Ho aggiunto la riga contatore #816-CRM a /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (commit f40aa49f). Il diff staged è intatto (8 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

### Review #817-CRM (3° giro, diff staged delle rifiniture su #386)

## VERDETTO: APPROVATO CON RISERVE

Review #817-CRM sul diff staged (4 file, +143/−12), sopra ebf645db (head della PR #386). Chiude le note di bot e verifica esterna su #386 e R-816-1. Resta una riserva BASSA nuova (R-817-1), introdotta dal nome «una copia al giorno».

**Verifiche rifatte da me:**
- Suite CRM: 126 passed. mypy pulito su modules/crm.
- Fail-before: con il codice di ebf645db e il file di test nuovo, `test_ve386_copie_cifrate_rifinite` fallisce (1 failed, 125 passed).
- Prova di concorrenza su due copie dello stesso giorno (riserva R-817-1).
- Kernel non toccato. Nessuno slicing della history, nessuna simulazione di tool.

### Riserva

**1. R-817-1 — BASSA — due copie dello stesso giorno in parallelo rovinano la copia del giorno.**
- **Causa:** col nome per giorno (`modules/crm/copia_cifrata.py:137`), due copie dello stesso giorno usano anche lo STESSO file temporaneo `crm-AAAAMMGG.gascrm.tmp` (`modules/crm/copia_cifrata.py:140`), aperto senza esclusività. Prima i nomi avevano data e ora, quindi erano unici.
- **Quando succede:** il thread del guardiano (all'avvio e ogni 24 ore) e il comando `python -m modules.crm backup` lanciato a mano nello stesso momento; oppure due server.
- **Provato con un intreccio forzato:** le due scritture si mescolano. Una delle due risponde «riuscita», l'altra fallisce con FileNotFoundError. Il file del giorno rimasto in iCloud NON si decifra («password sbagliata o file rovinato»).
- **Danno limitato:** le copie dei giorni precedenti restano buone, e la copia successiva sostituisce quella rovinata. La finestra è piccola: circa 0,4 s fra scrypt e scrittura.
- **Rimedio:** un nome temporaneo unico (per esempio con pid e id del thread, o `tempfile.mkstemp` nella stessa cartella), con la pulizia dei `.tmp` vecchi allargata a quei nomi.

### Elementi del diff esaminati

- **Password normalizzata** (`modules/crm/copia_cifrata.py:81`): `_normalizza` (NFC più spazi tolti ai bordi) si usa sia in `password()` sia in `_fernet`, quindi cifratura e decifratura vedono la stessa forma. Il getpass del ripristino ora toglie gli spazi (`modules/crm/__main__.py:207`), che chiude la prima parte di R-816-1. Nessuna copia col formato precedente è uscita. Esito: ok.
- **File leggibili solo dal proprietario** (`modules/crm/copia_cifrata.py:88`): `_scrivi_privato` crea i file con 0600 dall'inizio (`os.open`), più un `chmod`. Vale per il `.tmp` cifrato, il `.ripristino.tmp` in chiaro (`modules/crm/copia_cifrata.py:205`) e il ripiego di `dest`. Il `dest` creato con `os.link` condivide l'inode, quindi è 0600. Le copie locali passano a 0600 (`modules/crm/store.py:1225`). Esito: ok.
  - Nota: il DB vivo `.gas_memory_crm.db` resta coi permessi predefiniti (di solito 0644). Su un Mac con un solo utente pesa poco.
- **Una copia al giorno:** il nome viene dal nome della copia locale; la copia del giorno si rinnova con `os.replace`. La rotazione ordina `crm-AAAAMMGG.gascrm` per data e non prende i `.tmp`. Esito: ok, salvo R-817-1.
- **File temporanei:** il `finally` toglie il `.tmp` se si fallisce prima di `os.replace`; `_pulisci_tmp_vecchi` (`modules/crm/copia_cifrata.py:161`) toglie quelli più vecchi di un'ora. Esito: ok.
- **Ripristino** (`modules/crm/copia_cifrata.py:233`): se il ricontrollo finale fallisce, il file creato DA QUESTO ripristino (`creato`, `modules/crm/copia_cifrata.py:212` e `modules/crm/copia_cifrata.py:219`) viene tolto, insieme ai file di lavoro. Nel ripiego senza collegamenti fisici, una scrittura interrotta toglie il file a metà. L'ordine delle eccezioni è giusto: `FileExistsError` viene preso prima del generico `OSError`. Così si chiude la seconda parte di R-816-1. Esito: ok.
- **Test nuovo** (`tests/test_unit_crm.py:1443`): copre NFC/NFD, due copie nello stesso giorno (in sequenza, non in parallelo), permessi 0600, `os.replace` rotto, `.tmp` vecchio di 2 ore, ripiego senza `os.link`, ricontrollo che fallisce. Esito: ok.

### Rischi esplicitamente NON verificati

- Comportamento di iCloud Drive con `os.replace` sullo stesso nome ogni giorno (versioni, conflitti di sincronizzazione fra dispositivi): qui non riproducibile.
- Il ripiego senza collegamenti fisici su un file system vero (exFAT, cartella di rete): provato solo con `os.link` sostituito nel test.
- Documenti fuori stage (guida con la nota GDPR estesa alle copie iCloud): non letti.

### Note

- La V-4 del bot (falsi allarmi a cavallo di due parole) resta dentro R-810-2, come dichiarato.
- Restano aperte, dai giri precedenti: R-810-2, R-810-3, R-804-2, R-804-4, R-803-9, R-803-10, R-808-5, R-808-6.
- Ho aggiunto la riga contatore #817-CRM e una lezione (temporanei derivati da un nome condiviso) in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (commit 8b0b5b44). Il diff staged è intatto (4 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

### Review #818-CRM (4° giro, commit 17aee558)

## VERDETTO: APPROVATO

Review #818-CRM sul diff staged (4 file, +188/−13; il messaggio diceva +190/−12, conta poco). R-817-1 è chiusa: ora ogni copia scrive il proprio file temporaneo, e due copie dello stesso giorno in parallelo riescono entrambe e producono un file decifrabile.

**Verifiche rifatte da me:**
- Suite CRM: 127 passed. mypy pulito su modules/crm.
- Fail-before: ho ritrovato nel repo il `copia_cifrata.py` del giro #817 (blob 983f246f). Con quello al posto del nuovo, `test_r817_1_due_copie_dello_stesso_giorno_in_parallelo` fallisce (1 failed, 126 passed).
- Ho rifatto la mia prova del giro #817 sul codice nuovo: due copie dello stesso giorno in parallelo, con le scritture intrecciate a metà. Ora riescono entrambe e il file del giorno si decifra in un database SQLite (`b'SQLite format 3'`); prima era indecifrabile.
- Kernel non toccato. Nessuno slicing della history, nessuna simulazione di tool.

**Elementi del diff esaminati:**
- `modules/crm/copia_cifrata.py:143` — il temporaneo ha nome unico per processo e per thread (`{dest.name}.{pid}-{thread_ident}.tmp`); `modules/crm/copia_cifrata.py:144` lo crea in esclusiva (O_EXCL) con permessi 0600.
  - Rischio esaminato: due scritture sullo stesso file temporaneo. Due thread vivi dello stesso processo non hanno mai lo stesso ident, e due processi hanno pid diversi.
  - Se resta un temporaneo con lo stesso nome (thread morto e ident riusato entro un'ora), O_EXCL fa fallire solo quel tentativo, con un avviso nel log; il `finally` toglie il residuo.
  - L'`os.replace` finale sulla copia del giorno è atomico: vince l'ultima, ed entrambe sono complete.
  - Esito: ok.
- `modules/crm/copia_cifrata.py:168` — la pulizia usa il glob `crm-*.gascrm.*tmp`, che prende sia `crm-AAAAMMGG.gascrm.tmp` (nome vecchio) sia i nomi nuovi con pid e thread.
  - Rischio esaminato: cancellare il temporaneo di una copia in corso. Si tolgono solo quelli più vecchi di un'ora.
  - Esito: ok.
- `tests/test_unit_crm.py:1510` — il test sincronizza le due scritture con una Barrier e controlla quattro cose: temporanei diversi, entrambe le copie riuscite, file del giorno decifrabile in SQLite, nessun `.tmp` rimasto.
  - Rischio esaminato: un test che passa per caso. Sul codice di #817 fallisce in modo deterministico, perché i due percorsi coincidono.
  - Esito: ok.

**Rischio esplicitamente NON verificato:** il comportamento di iCloud Drive vero con più file temporanei nella stessa cartella (sincronizzazione dei `.tmp` prima della rinomina). Qui non c'è un Mac; i file sono comunque cifrati e restano 0600.

**Note:**
- Restano aperte, dai giri precedenti: R-810-2, R-810-3, R-804-2, R-804-4, R-803-9, R-803-10, R-808-5, R-808-6. Resta anche la nota di #817: il DB vivo ha i permessi predefiniti (di solito 0644).
- Ho aggiunto la riga contatore #818-CRM in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (commit 37972ed5). Il diff staged è intatto (4 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

### Review #819-CRM (5° giro, commit 7b652af1)

## VERDETTO: APPROVATO

Review #819-CRM sul diff staged (2 file, +33/−2), sopra ee38220c (head della PR #386): chiude V-1 e V-2 della verifica esterna #386, 2° giro, senza riserve nuove.

**Verifiche rifatte da me:**
- Suite CRM: 128 passed. mypy pulito su modules/crm.
- Fail-before: con il codice di ee38220c e il file di test nuovo, `test_ve386b_ripristino_con_disco_pieno_non_lascia_dati_in_chiaro` fallisce (1 failed, 127 passed).
- Kernel non toccato. Nessuno slicing della history, nessuna simulazione di tool.

**Elementi del diff esaminati:**
- `modules/crm/copia_cifrata.py:212` — la scrittura del `.ripristino.tmp` IN CHIARO ora sta dentro il try; il `finally` (`modules/crm/copia_cifrata.py:234`) lo toglie sempre. Esito: ok.
  - Rischio esaminato: un disco pieno a metà scrittura che lascia dati parziali dei clienti in chiaro. Prima la scrittura stava fuori dal try/finally, quindi il temporaneo restava.
  - Il test simula ENOSPC dopo metà dei dati: non restano né il temporaneo né `dest`.
- `modules/crm/copia_cifrata.py:199` — il controllo iniziale è `dest.exists() or dest.is_symlink()`. Esito: ok.
  - Rischio esaminato: un collegamento pendente al posto di `dest`. `exists()` lo dà per assente, mentre `os.link` fallirebbe con un messaggio fuorviante («comparso durante il ripristino»). Ora risponde «esiste già», e il test lo fissa.

**Nota cosmetica, non classificata come riserva:** nel ripiego senza collegamenti fisici (`modules/crm/copia_cifrata.py:230`), il file da togliere dopo una scrittura interrotta si riconosce con `dest.exists()`, non con un segno «l'ho creato io». Solo in un caso estremo (apertura fallita per un motivo diverso da «esiste già» e `dest` creato da altri nello stesso istante) toglierebbe un file non suo. Un flag messo dopo `os.open` lo renderebbe esatto. Lo stesso controllo dei file di lavoro (`-journal` e simili) non vede un collegamento pendente: è un caso solo teorico.

**Rischio esplicitamente NON verificato:** un disco pieno vero su macOS durante il ripristino. Provato solo con l'errore simulato nel test.

**Note:**
- Restano aperte dai giri precedenti: R-810-2, R-810-3, R-804-2, R-804-4, R-803-9, R-803-10, R-808-5, R-808-6.
- Ho aggiunto la riga contatore #819-CRM a /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (commit 7b8269ad). Il diff staged è intatto (2 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

### Review #820-CRM (6° giro, commit e2c6e95a)

## VERDETTO: APPROVATO CON RISERVE

Review #820-CRM sul diff staged (6 file, +156/−14), sopra 7b652af1. Chiude la V-1 MEDIA del bot su #386: una copia fuori dal Mac fallita adesso si vede all'avvio, nella dashboard e, se attivo, su Telegram. Chiude anche le note V-2 e V-4 del bot e la nota cosmetica del mio #819. Resta una sola riserva BASSA (R-820-1).

**Verifiche rifatte da me:**
- Suite CRM: 131 passed.
- mypy pulito su modules/crm; `node --check modules/crm/web/app.js` ok.
- Fail-before: col codice di 7b652af1 e il file di test nuovo falliscono i 3 test nuovi (128 passati).
- Kernel non toccato. Nessuno slicing della history, nessuna simulazione di tool.

### Riserva

**1. R-820-1 — BASSA — una cartella di rete bloccata può impedire l'avvio del server.**
- La prova di scrittura all'avvio (`modules/crm/__main__.py:132`) gira nel thread principale, dentro la callback `pronto`, prima che il server cominci ad accettare connessioni (`serve_forever`).
- Se `GAS_CRM_BACKUP_CIFRATO_DIR` punta a una cartella di rete bloccata, `serve` resta fermo lì e la dashboard non parte. È lo stesso caso di R-815-4: lì è stato risolto per il guardiano, ma non per l'avvio.
- iCloud Drive è su disco locale, quindi nel caso normale non succede. Almeno si vede (il server non parte), invece di fallire in silenzio.
- Rimedio: fare la prova in un thread con un tempo massimo (es. 5 s) e stampare «NON VERIFICATA (cartella lenta)» se scade.

### Elementi del diff esaminati

- **Prova di scrittura** (`modules/crm/copia_cifrata.py:107`): crea in esclusiva (O_EXCL) e con permessi 0600 un file `.prova-<pid>-<thread>.tmp` con 32 byte casuali, mai dati, e lo toglie nel `finally`.
  - Rischio esaminato: avvio che dice ATTIVA guardando solo la configurazione. Ora `serve` distingue SPENTA, NON FUNZIONA (con «i dati restano solo sul Mac») e ATTIVA.
  - Esito: ok, salvo R-820-1.
- **Esito visibile** (`modules/crm/server.py:123`, `modules/crm/server.py:273`, `modules/crm/server.py:537`): `Stato.copia_esterna` parte da `motivo_spenta()`. Il thread lo sostituisce per intero (un'assegnazione unica, quindi niente letture a metà) e chiama `segnala_cambio()`, così la dashboard si aggiorna subito. In `/api/stato` vale None in demo.
  - Esito: ok.
- **Avviso all'operatore** (`modules/crm/server.py:286`): parte solo se l'avviso è configurato, non in demo, e solo per un fallimento vero (non per «spenta»).
  - Il motivo contiene il tipo d'errore e, dalla prova di scrittura, al massimo il percorso della cartella (con il nome utente del Mac dell'operatore): mai dati dei clienti. Il test controlla che «Marco» non ci sia.
  - Le eccezioni dell'invio vengono intercettate e loggate (§9). Non c'è un limite di frequenza, ma le copie avvengono solo all'avvio e una volta al giorno.
  - Esito: ok.
- **Indicatore in testata** (`modules/crm/web/app.js:233`): costruito con `el()`, cioè solo testo, mai HTML dai dati. Il motivo sta nel title; il rosso compare solo per `ok === false`.
  - Esito: ok.
- **Ripristino** (`modules/crm/__main__.py:217`):
  - chiede la password «vecchia» una sola volta, solo su «password sbagliata» e solo se stdin è un terminale. Il primo tentativo fallito non lascia file, perché la decifratura avviene prima di ogni scrittura;
  - il segnaposto `.icloud` di un file non ancora scaricato viene rifiutato con un messaggio chiaro (`modules/crm/copia_cifrata.py:224`);
  - nel ripiego senza collegamenti fisici, il segno «creato» viene messo solo dopo l'apertura in esclusiva riuscita (`modules/crm/copia_cifrata.py:254`), quindi si toglie solo un file creato da noi. Questo chiude la nota del #819.
  - Esito: ok.
- **Test** (`tests/test_unit_crm.py:1581`): coprono la prova su una cartella buona e su una «cartella» che in realtà è un file, la copia riuscita, fallita e spenta (con il conteggio degli avvisi), l'esito in `/api/stato`, la seconda password e il segnaposto.
  - Esito: ok.

### Rischi esplicitamente NON verificati

- Il blocco vero di macOS sull'accesso a `~/Library/Mobile Documents` per un Python lanciato da terminale, e iCloud pieno: qui non riproducibili. La prova di scrittura dovrebbe intercettarli come PermissionError o OSError, ma non l'ho visto su un Mac.
- La prova nel browser dichiarata dal chiamante (indicatore «☁ copia OK»): non rifatta.
- Documenti fuori stage (`reports/crm/guida.md`): non letti.

### Note

- La V-3 del bot (falsi allarmi a cavallo di due parole) resta dentro R-810-2.
- Restano aperte dai giri precedenti: R-810-2, R-810-3, R-804-2, R-804-4, R-803-9, R-803-10, R-808-5, R-808-6.
- Ho aggiunto la riga contatore #820-CRM in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata da sola (commit 046d87ea). Il diff staged è intatto (6 file).
- Non ho creato `.claude/.review_ok` e non ho committato il diff.

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_crm.py`:** 120 test su main c4c8c31f (quelli che passano anche col codice vecchio; prima l'handoff diceva 118 per errore, V-3 della verifica esterna #386 2° giro) → 125 passed a 32282b6f → 127 a 17aee558 → 128 a 7b652af1 → 131 a e2c6e95a.
  - Con il codice di main falliscono i 6 test nuovi o cambiati: `test_v1_ve381_parole_vietate_non_si_aggirano`, `test_nota_tolta_senza_doppi_spazi`, `test_copia_cifrata_fuori_dal_mac`, `test_copia_cifrata_mai_in_chiaro_senza_libreria`, `test_giro_automatico_due_volte_al_giorno`, `test_scrittore_opus`.
  - `test_r815_ripristino_sicuro_dopo_un_crash` fallisce col `copia_cifrata.py` del giro #815 e passa ora.
  - `test_ve386_copie_cifrate_rifinite` fallisce col codice di ebf645db (1 failed, 125 passed).
  - `test_r817_1_due_copie_dello_stesso_giorno_in_parallelo` fallisce col `copia_cifrata.py` del giro #817 (1 failed).
  - `test_ve386b_ripristino_con_disco_pieno_non_lascia_dati_in_chiaro` fallisce col codice di ee38220c (1 failed).
  - `test_v1_bot386_copia_esterna_visibile`, `test_v1_bot386_esito_in_api_stato` e `test_v2_bot386_ripristino_con_la_password_di_prima` falliscono col codice di 7b652af1 (3 failed).
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato.
- **Suite che usano `tests/conftest.py`:** `pytest tests/test_unit_notte.py tests/test_unit_voice_contesto.py tests/test_unit_manutenzione.py tests/test_unit_hooks.py` → `468 passed in 86.11s (0:01:26)`.
- **mypy:** 0 errori in `modules/crm`. **`node --check`** su `modules/crm/web/app.js`: ok (file non toccato).

## §6 STATO CI

`gh run list` non usato: in questa sessione cloud GitHub si interroga con gli strumenti MCP.
- Run della PR #386, lette con gli strumenti MCP:

```
run 44642840640  CI            push                 ebf645db  vista in corso dalla verifica esterna (handoff-check success)
run 44642844757  verifica-bot  pull_request_target  ebf645db  completed / success  (APPROVATO CON RISERVE senza ALTA/MEDIA, modello claude-opus-5-5)
run 44642803000  verifica-bot  pull_request_target  4cec29d0  completed / cancelled  (head cambiata durante la verifica)
```
- Mappatura commit→run:
  - `be656bb7`, `f40aa49f`, `32282b6f`: nessuna run su questi SHA (pushati insieme a 4cec29d0).
  - `4cec29d0`: verifica-bot 44642803000 cancelled (head cambiata); per la CI vale la run di ebf645db, pushato subito dopo.
  - `ebf645db`: CI 44642840640 e verifica-bot 44642844757 (sopra).
  - `8b0b5b44`, `37972ed5`, `17aee558`: nessuna run su questi SHA (pushati insieme a ee38220c).
  - `ee38220c`: CI con handoff-check success (unit-suite vista in corso); verifica-bot FAILURE per il finding MEDIA, chiuso in e2c6e95a.
  - `7b8269ad`, `7b652af1`, `046d87ea`, `e2c6e95a`: run non ancora disponibile alla scrittura dell'handoff. Saranno pushati insieme al commit di fine-task che contiene questo file.
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-820-1 (BASSA):** la prova di scrittura all'avvio gira nel thread principale. Con `GAS_CRM_BACKUP_CIFRATO_DIR` su una cartella di rete bloccata, `serve` non parte. iCloud Drive è su disco locale, quindi nel caso normale non succede.
- **V-3 del bot su ee38220c e V-4 del bot su ebf645db (BASSE/COSMETICHE):** falsi allarmi del filtro a cavallo di due parole. Restano dentro R-810-2: scartano solo la riscrittura.
- **Chiuse in questa fetta:**
  - R-815-1..4, R-816-1, R-817-1;
  - V-1..V-4 della verifica esterna #386 (1° giro), V-1..V-4 (2° giro);
  - V-1..V-3 del bot su ebf645db;
  - V-1 (MEDIA), V-2 e V-4 del bot su ee38220c.
- **V-4 del bot su ebf645db (COSMETICA):** falsi allarmi del filtro a cavallo di due parole («per derivati» → «perder»). Resta dentro R-810-2, dichiarata: scarta solo la riscrittura.
- **Nota di #817/#818 (non riserva):** il DB vivo `.gas_memory_crm.db` ha i permessi predefiniti (di solito 0644). Su un Mac con un solo utente pesa poco.
- **Chiuse anche in questa fetta:** R-815-1 (MEDIA), R-815-2/3/4, e dalla PR #381 le note sulle parole vietate e sulla docstring.
- **Ancora aperte da prima:** R-810-2, R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4 (vedi `reports/stato_progetto.md`).
