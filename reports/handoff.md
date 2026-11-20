# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-19/20 — CRM fetta 6: copia di sicurezza cifrata su iCloud Drive e ripristino, giro del motore 2 volte al giorno, parole vietate più ampie

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #386 (https://github.com/Gasss23/Gas/pull/386), aperta dopo il push del commit 4cec29d0, con l'etichetta «verifica». Riserve: R-816-1 COSMETICA. Il merge lo decide l'operatore.
   - È una fetta di sicurezza (cifratura dei dati dei clienti): secondo passaggio nella chat claude.ai col link della PR.
2. Password delle copie cifrate: nel `.env` del Mac `GAS_CRM_BACKUP_PASSWORD` (almeno 12 caratteri), salvata anche nel gestore di password.
3. Verificare che la cartella di Gas sia `~/Gas`, fuori da Scrivania e Documenti sincronizzate con iCloud.
4. Server gratuito per il CRM (Tailscale col Mac acceso, oppure Oracle Cloud «Always Free»): da decidere.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 6a — copia cifrata fuori dal Mac (iCloud Drive) e ripristino**: FATTA, commit 32282b6f. Review #815-CRM APPROVATO CON RISERVE (R-815-1 MEDIA) → #816-CRM APPROVATO CON RISERVE (R-816-1 COSMETICA).
- **Fetta 6b — giro del motore 2 volte al giorno**: FATTA (stesso commit).
- **Fetta 6c — parole vietate più ampie e docstring** (note del bot e della verifica esterna #381 rimandate il 19-11): FATTA (stesso commit).
- **Server per il CRM**: DEFERITA. Niente spese per un server solo per il CRM (decisione dell'operatore); alternative gratuite da decidere.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 modules/crm/__init__.py            |   6 ++++--
 modules/crm/__main__.py            |  49 +++++++++++++++++++++++++++++++++++++++++++++----
 modules/crm/copia_cifrata.py       | 176 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/crm/scrittore.py           |  11 +++++++----
 modules/crm/server.py              |  18 ++++++++++++++++--
 reports/crm/decisioni.md           |   6 ++++++
 reports/crm/guida.md               |  12 ++++++++++--
 reports/diff_sessione.md           |  21 +++++++++++----------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  37 +++++++++++++++++++++++++++----------
 requirements.txt                   |   2 ++
 tests/conftest.py                  |   4 ++++
 tests/test_unit_crm.py             | 140 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base della sessione: c4c8c31f (origin/main, dopo il merge della PR #381).

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_crm.py`:** 118 test su main c4c8c31f (quelli che passano anche col codice vecchio) → 125 passed.
  - Con il codice di main falliscono i 6 test nuovi o cambiati: `test_v1_ve381_parole_vietate_non_si_aggirano`, `test_nota_tolta_senza_doppi_spazi`, `test_copia_cifrata_fuori_dal_mac`, `test_copia_cifrata_mai_in_chiaro_senza_libreria`, `test_giro_automatico_due_volte_al_giorno`, `test_scrittore_opus`.
  - `test_r815_ripristino_sicuro_dopo_un_crash` fallisce col `copia_cifrata.py` del giro #815 e passa ora.
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato.
- **Suite che usano `tests/conftest.py`:** `pytest tests/test_unit_notte.py tests/test_unit_voice_contesto.py tests/test_unit_manutenzione.py tests/test_unit_hooks.py` → `468 passed in 86.11s (0:01:26)`.
- **mypy:** 0 errori in `modules/crm`. **`node --check`** su `modules/crm/web/app.js`: ok (file non toccato).

## §6 STATO CI

`gh run list` non usato: in questa sessione cloud GitHub si interroga con gli strumenti MCP.
- Sul ramo ripartito da main questa è la prima fetta. Ultima run del ramo prima della ripartenza: 44598878073 su 1a177291 (PR #381), success.
- Mappatura commit→run:
  - `be656bb7`, `f40aa49f`, `32282b6f`: run non ancora disponibile alla scrittura dell'handoff. Saranno pushati insieme al commit di fine-task che contiene questo file, e la run testerà solo l'albero di quel commit.
  - `4cec29d0` (primo fine-task della fetta): run appena partita al push, esito non ancora disponibile alla scrittura dell'handoff.
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-816-1 (COSMETICA):**
  - la password digitata con getpass in `ripristina` non viene ripulita dagli spazi ai bordi;
  - il ripiego senza collegamenti fisici (`open(dest, "xb")`) non ha un test, e con disco pieno può lasciare un file incompleto, segnalato come «non usarlo».
- **Chiuse in questa fetta:**
  - R-815-1 (MEDIA, file di lavoro rimasto accanto al database da ripristinare);
  - R-815-2 (sovrascrittura durante il ripristino);
  - R-815-3 (parametri di scrypt);
  - R-815-4 (cartella di rete appesa nel guardiano).
  - Dalla PR #381: parole vietate (V-1 della verifica esterna, 5° giro, e V-1 del bot su f537d231), docstring (V-1 del bot su 1a177291), nota minore #813.
- **Ancora aperte da prima:** R-810-2, R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4 (vedi `reports/stato_progetto.md`).
