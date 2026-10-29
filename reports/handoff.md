# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Note del bot su #291: il doctor confronta il valore di GAS_CLAUDE_BIN nel .env, nome nudo, collegamenti dei test (chat Motore). Secondo giro: merge di main (PR #288) dopo la V-1 della verifica esterna #292. Terzo giro: note del bot su f94c4a0 (registro del .env solo per GAS_CLAUDE_BIN). Quarto giro: V-1 bot #292 su 67c2bca (vuoto = «claude») e merge di main (PR #294). Quinto giro: merge di main con la PR #293 (altra sessione chat Motore, conflitto nel codice del doctor).

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #292 (https://github.com/Gasss23/Gas/pull/292): già autorizzato dall'operatore il 2026-10-29 («sistema anche questa e poi mergia»), dopo CI verde e bot senza finding ALTA/MEDIA sul nuovo head. Numero e URL dalla risposta JSON di `mcp__github__create_pull_request`. Numero e URL dalla risposta JSON di `mcp__github__create_pull_request` (`gh` nel container non è autenticato).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — V-1 bot #291 + R-543-1 + R-544-1 (valore nel .env)**: `FATTA` — `_DOTENV_NEL_FILE: Dict[str, str]`, WARN «altro valore».
- **Fetta 2 — V-2 bot #291 + R-543-2 (nome nudo)**: `FATTA`.
- **Fetta 3 — R-544-2 (riga doppia)**: `FATTA` — `setdefault`.
- **Fetta 4 — V-3 (R-541-1) e V-4 bot #291**: `FATTA`.
- **Fetta 5 — conflitto con main (V-1 MEDIA verifica esterna #292)**: `FATTA` — merge di origin/main d4b39ca (PR #288), review #547 APPROVATO.
- **Fetta 6 — note del bot su a0872d2 (BOCCIATO per il conflitto) e su f94c4a0 (check rosso)**: `FATTA` — `_DOTENV_VALORI_DA_TENERE`, T99s rimette il registro, BOCCIATO registrato nei report; review #548 APPROVATO CON RISERVE.
- **Fetta 7 — V-1 bot #292 su 67c2bca + R-545-1 + R-548-1**: `FATTA` — vuoto e «claude» uguali nel confronto col `.env`; review #549 APPROVATO.
- **Fetta 8 — merge di main (PR #294)**: `FATTA` — review #550 APPROVATO.
- **Fetta 9 — merge di main con la PR #293 (conflitto in gas.py e nei test)**: `FATTA` — tenuti i due registri del `.env`, rimessa `_DOTENV_CARICATE.update` persa dal merge automatico; review #551 APPROVATO CON RISERVE.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  12 ++++++++++
 gas.py                             |  35 +++++++++++++++++++++++------
 reports/diff_sessione.md           |  19 ++++++++++------
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  34 +++++++++++++++-------------
 tests/test_unit_dotenv.py          |  33 +++++++++++++++++++++++++--
 tests/test_unit_kernel.py          |  54 ++++++++++++++++++++++++++++++--------------
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d», e la riga di totale è tolta. Conteggi presi con i report già in stage.

## §3 GIT LOG --ONELINE (sessione)

```
4cf9d4c Merge origin/main (PR #293) in fix/note-forte-doctor-2 (PR #292): tenuti i due registri del .env — review #551 APPROVATO CON RISERVE
bd6336c docs(fine-task): PR #292 quarto giro — vuoto = «claude», merge di main (PR #294), review #549/#550
b9c1dcd Merge origin/main (PR #294) in fix/note-forte-doctor-2 (PR #292) — review #550 APPROVATO
d03936c fix(forte): vuoto e «claude» sono lo stesso comando nel confronto col .env (V-1 bot #292, R-545-1); commento R-544-2 al posto giusto (R-548-1)
ab985e5 chore(revisore): memoria review #549 — APPROVATO
67c2bca docs(fine-task): PR #292 terzo giro — registro del .env solo per GAS_CLAUDE_BIN, review #548, verdetti del bot registrati
7bf0071 fix(forte): registro del .env solo per GAS_CLAUDE_BIN, niente segreti (V-2 ve #292, V-4 bot #292); T99s rimette il registro
68efe8c chore(revisore): memoria review #548 — APPROVATO CON RISERVE
f94c4a0 docs(fine-task): PR #292 secondo giro — merge di main (PR #288), review #547, verifica esterna
77be957 Merge origin/main (PR #288) in fix/note-forte-doctor-2 (PR #292) — review #547 APPROVATO
a0872d2 docs(fine-task): PR #292 note del bot su #291, review #543–#545
15b6704 fix(forte): note del bot su #291 — doctor guarda il valore di GAS_CLAUDE_BIN nel .env, nome nudo, link dei test
86bd88e chore(revisore): memoria review #545 — APPROVATO CON RISERVE
b402b8c chore(revisore): memoria review #544 — APPROVATO CON RISERVE
5c21e08 chore(revisore): memoria review #544 — APPROVATO CON RISERVE
861cc88 chore(revisore): memoria review #543 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Tre giri sullo stesso diff prima del commit 15b6704: #543 sul primo stato, #544 (fatta due volte in parallelo, stessi finding) dopo le correzioni di R-543-1/2, #545 sul diff finale dopo le correzioni di R-544-1/2. I numeri di riga dei primi giri si riferiscono al diff di quel momento.

### Review #543 (chat Motore) — primo stato del diff

## VERDETTO: APPROVATO CON RISERVE

Review #543 (chat Motore), diff staged su `fix/note-forte-doctor-2`. Prima ho letto CLAUDE.md, i punti di `reports/stato_progetto.md` che riguardano questa fetta (riga 589) e la memoria del revisore.

**Elementi del diff esaminati**

1. `gas.py:626`: `_DOTENV_NEL_FILE.add(chiave)` viene prima del `continue` sui nomi già presenti nella shell, quindi il set contiene ogni nome scritto nel `.env`.
   - Rischio esaminato: effetti su chi usa il set. L'unico lettore è `gas.py:5014` (doctor); nessun altro uso in gas.py, nei test o negli script.
   - Il vecchio `update(caricate)` è stato tolto, ma `caricate` resta il valore di ritorno, quindi chi chiama `_carica_dotenv` non vede cambiamenti. V-1 bot #291 è chiusa.
   - Esito: **riserva** (vedi R-543-1).
2. `gas.py:460`: `if valore_env and "/" in valore_env`. Un nome nudo (`claude`) passa al controllo delle cartelle sul percorso trovato da `shutil.which`; un relativo con «/» (`./claude`, `~/bin/claude`) dà ancora WARN «non è un percorso assoluto». Ho verificato tutti e due a mano.
   - Rischio esaminato: falso OK sul nome nudo. Se il nome è proprio `claude`, il timer lo cerca nel suo PATH e il controllo delle cartelle vale anche per lui: nessun falso OK. V-2 bot #291 è chiusa.
   - Esito: **ok**, con la piccola riserva R-543-2.
3. `tests/test_unit_dotenv.py:127`: il test monkeypatcha il set e controlla `{"GAS_T_FILE", "GAS_T_SHELL"}`.
   - Rischio esaminato: legame tra la funzione vera e il set (lezione #540). Il legame c'è.
   - `GAS_T_SOLO_SHELL` viene messo nell'ambiente ma non è nel file; l'uguaglianza esatta prova che non entra nel set.
   - Esito: **ok**.
4. `tests/test_unit_kernel.py:11253`: unlink di `link99` e `linkroot99`, entrambi creati senza condizioni poco prima (11234-11236). R-541-1 / V-3 bot #291 è chiusa.
   - Esito: **ok**. Anche `Set[str]` con l'import da typing è a posto (V-4).

**Test rifatti da me:** kernel 1057 PASS, 0 FAIL; pytest `test_unit_dotenv` + `test_unit_claude_cli` 40 passed.

**Riserve**

- **R-543-1 MEDIA, falso OK nuovo.** Caso: il `.env` ha `GAS_CLAUDE_BIN=/vecchio/claude` e la shell esporta un `/nuovo/claude` diverso.
  - Il doctor controlla il valore della shell (`_bin_env`, `binario`) e, visto che il nome sta in `_DOTENV_NEL_FILE`, dice OK «presente».
  - Il timer invece usa il valore del file, che può non esistere.
  - Prima di questa modifica qui c'era un WARN (verso prudente). Ora il set di nomi non basta.
  - Rimedio consigliato in questa stessa fetta: ricordare il VALORE letto dal file (`Dict[str, str]`). Poi, nel doctor, passare `da_dotenv` vero solo se il valore del file è uguale a `os.environ["GAS_CLAUDE_BIN"]`, oppure controllare direttamente il valore del file. Aggiungere un test con i due valori diversi che si aspetta WARN.
- **R-543-2 BASSA.** Un nome nudo diverso da `claude` messo solo nella shell (es. `GAS_CLAUDE_BIN=claude-beta`) dà OK. Senza la shell, però, il timer cerca `claude` (`brains/claude_cli.py:284`, contesto). È un caso raro.

**Rischio escluso:** non ho verificato il comportamento reale del timer launchd sul Mac né di un'unità systemd sulla VPS (non riproducibile nel container). Il ragionamento su quale valore legge il timer si basa sul commento di `scripts/notte/com.gas.notte.plist:5` e su `gas.py:6069` (contesto).

Memoria aggiornata con la riga #543 e una lezione nuova, già committata (861cc88) con `scripts/commit_memoria_revisore.sh`.

File rilevanti: `/home/user/Gas/gas.py`, `/home/user/Gas/tests/test_unit_dotenv.py`, `/home/user/Gas/tests/test_unit_kernel.py`, `/home/user/Gas/.claude/agents/memoria_revisore.md`

### Review #544 (chat Motore, primo passaggio) — dopo R-543-1/2

## VERDETTO: APPROVATO CON RISERVE

Review #544 (chat Motore): nuovo diff staged su `fix/note-forte-doctor-2`, che corregge R-543-1 e R-543-2. Ho riletto CLAUDE.md, la riga 589 di `reports/stato_progetto.md` e la memoria del revisore.

**Elementi del diff esaminati**

1. `gas.py:630` `_DOTENV_NEL_FILE[chiave] = valore`: registra nome e valore di ogni riga del `.env`, anche quando vince la shell.
   - Rischio esaminato: effetti su chi usa il registro. L'unico lettore è `gas.py:5018`, e `caricate` non cambia.
   - Esito: **ok**, salvo il caso delle righe doppie (R-544-2).
2. `gas.py:5018` `_DOTENV_NEL_FILE.get("GAS_CLAUDE_BIN") == _bin_env`: ora conta che il valore in uso sia quello scritto nel file.
   - Rischio esaminato: il falso OK di R-543-1 (`.env` con `/vecchio/claude` e shell con un altro valore). Lo copre `tests/test_unit_kernel.py:11211` (`_d99s4` si aspetta WARN).
   - Esito: **ok**, R-543-1 CHIUSA.
3. `gas.py:464` `if not da_dotenv and valore_env != "claude"`: dà WARN se il valore non sta nel `.env`, salvo il nome nudo `claude`.
   - Rischio esaminato: falso OK sui nomi nudi. `claude-beta` solo nella shell dà WARN; `claude-beta` dal `.env` passa al controllo delle cartelle (`tests/test_unit_kernel.py:11248`).
   - Esito: R-543-2 CHIUSA, ma resta una **riserva** (R-544-1).
4. `tests/test_unit_dotenv.py:127`: il test controlla l'intero dizionario `{"GAS_T_FILE": "1", "GAS_T_SHELL": "dal-file"}`, quindi il loader vero resta legato al registro.
   - Esito: **ok**.

**Test rifatti da me:** kernel 1057 PASS, 0 FAIL; pytest dotenv + claude_cli 40 passed.

**Riserve**

- **R-544-1 BASSA, falso OK residuo.** L'eccezione per `claude` non controlla se il `.env` ha un ALTRO valore.
  - Caso provato a mano: `.env` con `GAS_CLAUDE_BIN=/vecchio/claude` e shell con `GAS_CLAUDE_BIN=claude` → `_avviso_claude_timer('claude', '/usr/bin/claude', root, False)` restituisce `None`, ma il timer userà `/vecchio/claude`.
  - Stessa famiglia: una shell che esporta `GAS_CLAUDE_BIN` vuoto vince sul file (`chiave in os.environ`), così il doctor controlla `claude` mentre il timer usa il valore del file.
  - Rimedio: dare WARN ogni volta che `"GAS_CLAUDE_BIN" in _DOTENV_NEL_FILE` e il valore del file è diverso da `_bin_env`, compreso il caso con `_bin_env` vuoto. L'eccezione per `claude` va limitata a quando il `.env` non ha la variabile.
- **R-544-2 COSMETICA.** Con due righe `GAS_CLAUDE_BIN` nel `.env`, il dizionario tiene l'ultima mentre il loader usa la prima. Risultato: falso WARN, nel verso prudente. Si allinea con `setdefault`.

**Rischio escluso:** non ho verificato il timer reale (launchd sul Mac, systemd sulla VPS), che nel container non si riproduce. L'ipotesi «il timer legge solo il `.env`» si basa su `gas.py:6069` e sul commento di `scripts/notte/com.gas.notte.plist:5`, entrambi di contesto.

Memoria aggiornata con la riga #544 e una lezione nuova, già committata (5c21e08). Anche la #543 (verdetto sopra) è già committata (861cc88).

File rilevanti: `/home/user/Gas/gas.py`, `/home/user/Gas/tests/test_unit_kernel.py`, `/home/user/Gas/tests/test_unit_dotenv.py`, `/home/user/Gas/.claude/agents/memoria_revisore.md`

### Review #544 (chat Motore, secondo passaggio) — stesso diff

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md (sezioni 5, 8 e 9), la memoria del revisore fino alla #543 e il diff staged su `fix/note-forte-doctor-2` (3 file). Ho rifatto i test: kernel 1057 PASS e 0 FAIL, pytest su `test_unit_dotenv` e `test_unit_claude_cli` 40 passed. Ho anche riprodotto a mano i casi limite descritti sotto.

**Elementi del diff esaminati**
- `gas.py:630`: `_DOTENV_NEL_FILE[chiave] = valore` registra nome e valore di ogni riga valida del `.env`, prima del controllo «vince la shell». Rischio esaminato: righe malformate o con virgolette non chiuse registrate per errore. Escono prima con `continue`, quindi non entrano. **ok**. Però vedi R-544-2 sulle chiavi duplicate.
- `gas.py:5018`: `da_dotenv = _DOTENV_NEL_FILE.get("GAS_CLAUDE_BIN") == _bin_env`. Rischio esaminato: il falso OK di R-543-1 (file `/vecchio`, shell `/nuovo`). Ora dà WARN, e T99s lo copre (`tests/test_unit_kernel.py:11210`). **ok**, R-543-1 CHIUSA.
- `gas.py:463`-467: l'ordine dei casi è relativo con «/» → WARN, poi non nel `.env` e diverso da «claude» → WARN, poi assoluto → None, poi controllo delle cartelle. Rischio esaminato: un nome nudo diverso da «claude» presente solo nella shell. Ora dà WARN («claude-beta», `tests/test_unit_kernel.py:11248`). **ok**, R-543-2 CHIUSA. L'esenzione per «claude» però apre un falso OK nuovo (R-544-1).
- `tests/test_unit_kernel.py:11260`: `unlink` di link99 e linkroot99 dopo l'ultimo uso (riga 11255). **ok**, R-541-1 CHIUSA.
- `tests/test_unit_dotenv.py:127`: il test lega `_carica_dotenv` al dizionario, compreso il caso «vince la shell» e il nome presente solo nella shell. **ok**. L'unico lettore è `gas.py:5018`, e non restano riferimenti a `_DOTENV_CARICATE`.

**Riserve**
- **R-544-1 BASSA: falso OK nuovo, riprodotto.** Il caso: la shell ha `GAS_CLAUDE_BIN=claude` e il `.env` ha `GAS_CLAUDE_BIN=/vecchio/claude`.
  - Il valore in uso non è quello del file, quindi `da_dotenv` vale False. Ma l'esenzione `valore_env != "claude"` a `gas.py:465` salta il WARN e si passa al controllo delle cartelle.
  - Con `/usr/bin/claude` il risultato è None, cioè OK. Il timer invece userà `/vecchio/claude`. Prima di #543 questo caso dava WARN («non assoluto»).
  - Stessa cosa con la shell vuota (`GAS_CLAUDE_BIN=""`), ma questo succedeva già prima.
  - Correzione: dare l'esenzione per «claude» e per il valore vuoto solo se `"GAS_CLAUDE_BIN" not in _DOTENV_NEL_FILE`. In pratica, passare alla funzione anche «il file ha la chiave con un altro valore».
- **R-544-2 BASSA: precedenza diversa tra dizionario e loader.** Con una chiave duplicata nel `.env`, `_DOTENV_NEL_FILE` tiene l'ultimo valore e `os.environ` il primo. L'ho riprodotto con `/a` e `/b`: environ vale `/a`, il dizionario `/b`.
  - Se la shell ha `/b` e il file ha `/a` seguito da `/b`, il doctor dice OK ma il timer carica `/a`.
  - Correzione: `_DOTENV_NEL_FILE.setdefault(chiave, valore)` a `gas.py:630`. Le chiamate al loader sono una sola (`gas.py:6073`), quindi `setdefault` è sicuro.

Nessun antipattern del Wall of Shame: non tocca la history, non simula output di tool, non indebolisce i guardrail. Il codice nuovo non apre strade a eccezioni non gestite (il dizionario si legge con `.get`).

**Rischio escluso:** non ho verificato il comportamento reale del giro notturno con launchd sul Mac (quale `claude` trova davvero), perché qui non si può riprodurre. Il ragionamento si basa su `brains/claude_cli.py:284` e sul loader `gas.py:584`. Non ho verificato neanche un PATH messo in `~/.zshenv`, già dichiarato nella docstring come falso allarme prudente.

La memoria è aggiornata (riga #544 più una lezione) e committata da sola con `commit_memoria_revisore.sh` (commit b402b8c). Il diff staged è rimasto intatto.

File rilevanti:
- `/home/user/Gas/gas.py`
- `/home/user/Gas/tests/test_unit_kernel.py`
- `/home/user/Gas/tests/test_unit_dotenv.py`
- `/home/user/Gas/.claude/agents/memoria_revisore.md`

### Review #545 (chat Motore) — diff finale di 15b6704

## VERDETTO: APPROVATO CON RISERVE

**Review #545.** Ho letto CLAUDE.md (sezioni 5, 8, 9) e la memoria del revisore, comprese le due righe #544. Ho riletto il diff staged aggiornato. Ho rifatto io i test: kernel 1057 PASS e 0 FAIL, pytest su dotenv e claude_cli 41 passed.

**Cosa ho esaminato nel diff**
- `gas.py:462` — Il primo controllo ora è: se il `.env` ha un valore diverso da quello in uso, il doctor avvisa con WARN. Vale anche con la shell «claude» o vuota.
  - Rischio cercato: il falso OK di R-544-1 (file con `/vecchio/claude`, shell con «claude» o vuota).
  - Esito: ok. T99t ora dà «altro valore» in entrambi i casi. **R-544-1 CHIUSA.**
- `gas.py:466` — L'eccezione per il nome «claude» vale solo con `valore_file is None`. Un nome nudo diverso da «claude» presente solo nella shell continua a dare WARN. Un nome nudo uguale tra shell e file passa al controllo delle cartelle.
  - Esito: ok.
  - Ho controllato anche: `.env` e shell vuoti e uguali, `.env` relativo e `GAS_NO_DOTENV=1`. Il risultato è un WARN prudente oppure lo stesso comportamento di claude_cli (`brains/claude_cli.py:284`). Nessun falso OK nuovo.
- `gas.py:633` — Il registro usa ora `setdefault`, quindi vince la prima riga come nel loader.
  - Esito: ok. Il test `tests/test_unit_dotenv.py:137` controlla che il valore sia `/a` sia nel registro sia in `os.environ`. **R-544-2 CHIUSA.**
- `gas.py:5021` — Il doctor passa al controllo `_DOTENV_NEL_FILE.get("GAS_CLAUDE_BIN")`, che è l'unico punto che legge il registro.
  - Esito: ok.

**Riserva**
- **R-545-1 COSMETICA** — Caso: nel `.env` c'è `GAS_CLAUDE_BIN=` vuoto e nella shell c'è un percorso.
  - Il WARN dice «il giro notturno userà quello». In realtà il timer userà `which("claude")`.
  - Il verso è prudente: è un problema solo del testo del messaggio.

**Cosa non ho verificato:** il comportamento reale di launchd e systemd sul Mac e sul VPS, perché qui non si può riprodurre. Ho solo controllato con grep che né il plist né le unit impostino `GAS_CLAUDE_BIN` scavalcando il `.env`.

Ho aggiunto la riga #545 alla memoria e l'ho committata da sola (commit 86bd88e). Il diff staged è rimasto intatto (3 file).

File:
- `/home/user/Gas/gas.py`
- `/home/user/Gas/tests/test_unit_kernel.py`
- `/home/user/Gas/tests/test_unit_dotenv.py`
- `/home/user/Gas/.claude/agents/memoria_revisore.md`

### Review #547 (chat Motore) — sul merge di origin/main (PR #288) in 77be957

## VERDETTO: APPROVATO

Review #547 (chat Motore). Ho controllato il merge in corso di origin/main d4b39ca (PR #288, chat Mani) dentro fix/note-forte-doctor-2 (PR #292, HEAD a0872d2). Il merge è pulito: nessuna riga persa, nessun marcatore di conflitto, e il codice viene da una sola parte per ciascun file.

**Elementi esaminati**
- `gas.py:633`: `_DOTENV_NEL_FILE.setdefault(...)`, il registro dei valori del `.env` in cui vince la prima riga. Rischio esaminato: che il merge avesse cambiato o perso il fix già revisionato in #545. Esito: ok. Il file nell'indice è identico a HEAD a0872d2, e main non ha toccato gas.py dalla base 2f35bc6 (`git diff --stat 2f35bc6 d4b39ca` non elenca gas.py).
- `gas.py:5021`: passa `_DOTENV_NEL_FILE.get("GAS_CLAUDE_BIN")` al doctor. Rischio esaminato: che fosse rimasta una versione mista fra main e il ramo. Esito: ok, identico a HEAD.
- `tests/test_unit_dotenv.py:138`: test sulla riga doppia nel `.env` (vince la prima). Rischio esaminato: test perso nel merge. Esito: ok. Il file è identico a HEAD e ho rifatto `pytest` su dotenv e web_lexbor: 32 passed, 85 skipped.
- `tests/test_unit_kernel.py:11211`: caso `_d99s4` del test T99s (il `.env` ha un valore diverso da quello in uso → WARN). Esito: ok, identico a HEAD.
- `modules/web/lexbor.py:195` e `tests/test_unit_web_lexbor.py:164`: la parte della PR #288. Rischio esaminato: che fossero diversi da main. Esito: ok, `git diff --cached origin/main` è vuoto per entrambi, e anche per `reports/ripartenza_mani.md`, `brains/` e `modules/`.
- `reports/stato_progetto.md:4`: ho verificato per costruzione (script Python) che la riga sia esattamente la voce #292 del ramo, poi la voce #288 di main, poi la catena di main. Ho controllato anche il secondo cambio rispetto a main, alla riga 589: è la voce di ripartenza della PR #292. Il paragrafo «fetta 23» della chat Mani arriva da main. Esito: ok.
- `.claude/agents/memoria_revisore.md`: 949 righe, cioè base 932 + 10 righe Mani + 7 righe Motore. Confronto riga per riga: 0 righe di base, HEAD o main mancanti e 0 righe inventate. Esito: ok.
- `git diff --cached origin/main --stat`: tocca solo memoria, gas.py, i due test e i report. Coincide con la PR #292. Esito: ok.

**Finding**
- R-547-1 COSMETICA: la numerazione #543–#545 è doppia fra chat Mani e chat Motore. Il suffisso della chat la distingue, ed è la continuazione di R-546-1.

**Antipattern:** nessuno slicing della history e nessuna simulazione di output dei tool. Il merge non tocca `run_turn`, `_get_window` né i provider.

**Cosa non ho verificato**
- Non ho rifatto la suite del kernel (1057/0 è un tuo dato). Il codice del motore è identico byte per byte a HEAD, già revisionato in #543–#545, quindi il rischio è nullo per costruzione.
- Non ho riletto i report che hai preso dal ramo (handoff, ultimo_report, diff_sessione): li riscrive comunque il /fine-task.
- Non ho controllato il comportamento sul Mac.

**Riga contatore:** ho aggiunto la #547 (chat Motore) in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`. Come richiesto non ho lanciato commit_memoria_revisore.sh. La riga è nel working tree ma non è in staging: prima di committare il merge fai `git add .claude/agents/memoria_revisore.md`.

### Review #548 (chat Motore) — sul diff di 7bf0071

## VERDETTO: APPROVATO CON RISERVE

Ho letto le fonti obbligatorie: CLAUDE.md (sezioni 5, 8 e 9), la memoria del revisore fino alla #547 e le voci su dotenv e #292 di reports/stato_progetto.md. Ho poi controllato il diff staged: gas.py, tests/test_unit_dotenv.py e tests/test_unit_kernel.py, 23 righe aggiunte e 3 tolte.

**Elementi esaminati**
- `gas.py:585` — aggiunge `_DOTENV_VALORI_DA_TENERE = frozenset({"GAS_CLAUDE_BIN"})`. Rischio esaminato: che il doctor abbia bisogno di altre chiavi del registro. Il registro ha un solo lettore, `gas.py:5025`, che legge solo `GAS_CLAUDE_BIN`. Esito: **ok**.
- `gas.py:636` — il registro accoglie solo le chiavi della lista, sempre con `setdefault`. Rischi esaminati: che si perda la regola «vince la prima riga» (R-544-2) e che cambi la scrittura in `os.environ`. La regola resta valida, perché il filtro sta prima del `setdefault`. La scrittura in `os.environ` non cambia, quindi le chiavi API continuano ad arrivare al processo. Il nome della lista viene letto a ogni chiamata, quindi i test possono sostituirla. Esito: **ok**.
- `tests/test_unit_dotenv.py:141` — nuovo test: con la lista standard nel registro entra solo `GAS_CLAUDE_BIN`. A `tests/test_unit_dotenv.py:136` una chiave fuori lista (`GAS_T_API_KEY=segreto`) non entra. Ho provato a rompere il codice sostituendo il filtro con `if True` e 2 test falliscono, quindi i test colgono davvero la regressione. Ho poi rimesso il file com'era (nessuna differenza rimasta). Esito: **ok**.
- `tests/test_unit_kernel.py:11206` — il test T99s salva il valore del registro e nel `finally` lo rimette com'era, come fa già per PATH. Il caso «prima non c'era» è gestito con `pop`. Esito: **ok**.

**Esecuzione diretta**
- Test del kernel: 1057 PASS, 0 FAIL; T99s passa.
- tests/test_unit_dotenv.py: 13 passed.

**Finding**
- R-548-1 COSMETICA: in `gas.py:636` il commento «R-544-2: vince la prima riga» ora sta sulla riga dell'`if`, mentre la regola la applica il `setdefault` della riga sotto. Non cambia il comportamento; si può spostare quando capita.

**Antipattern**
- Il diff non taglia la cronologia e non simula l'output dei tool.
- Non tocca `_get_window`, il limite di 10 iterazioni né il limite di 8k sull'output.
- Il loader resta fail-safe: nessuna nuova eccezione può arrivare fino a un crash.

**Rischio escluso**
- Non ho verificato il comportamento reale sulla VPS col timer systemd e un `.env` con segreti veri: in sviluppo non si può riprodurre. Lo copre solo il test con la chiave finta `GAS_T_API_KEY`.
- Non ho verificato neanche V-1 ve #292 (registrare il BOCCIATO del bot su a0872d2): riguarda solo i report e va al fine-task.

**Memoria**: ho aggiunto la riga #548, con la lezione «un registro diagnostico di un loader di segreti va limitato con una lista bianca nel punto in cui si scrive», in /home/user/Gas/.claude/agents/memoria_revisore.md. È committata con lo script dedicato (commit 68efe8c). Il diff staged sotto review non è stato toccato.

### Review #549 (chat Motore) — sul diff di d03936c

## VERDETTO: APPROVATO

Ho letto CLAUDE.md, stato_progetto.md (la riga 589 per le note aperte di #292) e memoria_revisore.md. Ho esaminato il diff staged su fix/note-forte-doctor-2 (HEAD 67c2bca): sono 2 file, 10 righe aggiunte e 4 tolte.

**Elementi del diff esaminati**

1. `gas.py:463`: nel confronto fra il valore del `.env` e quello in uso, un valore vuoto e «claude» ora contano come lo stesso comando. Il rischio era un falso OK nuovo, cioè due valori che sembrano uguali ma che `claude_cli` tratta in modo diverso. Esito ok. In `brains/claude_cli.py:284` (contesto) il comando è `binario or GAS_CLAUDE_BIN or which("claude") or "claude"`: con un valore vuoto e con «claude» il comando si cerca comunque nel PATH, quindi i due casi sono davvero equivalenti. R-544-1 resta chiusa: un `.env` con un percorso diverso dà ancora WARN, sia con la shell vuota sia con «claude» (i test a `tests/test_unit_kernel.py:11255-11256` sono invariati e passano).
2. `gas.py:464-465`: il messaggio ora dice il comando che userà il timer (`«{valore_file or 'claude'}»`). Il rischio era un testo che descrive male il caso «`.env` vuoto e shell con un percorso». Esito ok: in quel caso esce «userà «claude»», che è proprio quello che fa `which`. R-545-1 è chiusa. Il valore del `.env` finisce nel messaggio, ma vale solo per GAS_CLAUDE_BIN, che è nella lista bianca (non è un segreto).
3. `gas.py:639`: il commento «R-544-2» è stato spostato sulla riga del `setdefault`. La riga resta di 103 caratteri, sotto le righe più lunghe già presenti nel file. Esito ok, R-548-1 è chiusa.
4. `tests/test_unit_kernel.py:11258-11260`: tre casi nuovi (shell vuota e `.env` «claude» → None; shell «claude» e `.env` vuoto → None; `.env` vuoto e percorso assoluto nella shell → WARN con «claude»). Il rischio era un test che passa anche col codice vecchio. Esito ok: ho rimesso il vecchio confronto `valore_file != valore_env` e T99t è FAIL; poi ho ripristinato il file e controllato che non restassero differenze.
5. `gas.py:5026` (contesto, chiamante): passa `_DOTENV_NEL_FILE.get("GAS_CLAUDE_BIN")` senza modifiche. Il consiglio «metti GAS_CLAUDE_BIN=… nel .env» resta coerente col nuovo messaggio. Esito ok.

**Test rifatti da me:** kernel 1057 PASS, 0 FAIL; pytest su `test_unit_dotenv.py` e `test_unit_claude_cli.py` 42 passed.

**Wall of Shame:** nel diff non c'è slicing della history né simulazione di output dei tool. I limiti di sicurezza (10 iterazioni, 8k di output, `_get_window`) non sono toccati.

**Finding:** nessuno nuovo (nessun R-549-N). Con questo diff si chiudono V-1 bot #292, R-545-1 e R-548-1. Resta aperta V-3 ve #292 (BASSA, registro non riletto se `_carica_dotenv` gira due volte), che questo diff non tocca.

**Rischio escluso:** non ho verificato il comportamento reale sul Mac. Se `claude`, cercato nel PATH ridotto del timer, sia davvero lo stesso binario che trova la shell non è riproducibile in questo container: lo dirà il giro notturno del 29.

**Memoria:** ho aggiunto la riga contatore #549 in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` e l'ho committata da sola con `commit_memoria_revisore.sh` (commit ab985e5). Il diff staged sotto review è rimasto intatto. Un primo tentativo, che univa scrittura della riga e commit in un solo comando, è stato bloccato dall'hook del gate perché `.review_ok` non corrisponde al diff staged; non è stato eseguito nulla e l'ho rifatto in due passi. Il marcatore va rigenerato dall'agente principale con `bash scripts/segna_review_ok.sh` prima del commit.

### Review #550 (chat Motore) — sul merge di origin/main (PR #294) in b9c1dcd

## VERDETTO: APPROVATO

Review #550 (chat Motore). Ho controllato il merge in corso di origin/main 03dc898 (PR #294) dentro fix/note-forte-doctor-2 (PR #292, HEAD d03936c). Prima di iniziare ho letto CLAUDE.md (sezione 5), reports/stato_progetto.md e la mia memoria.

**Elementi del diff esaminati**
- `gas.py:463`: confronta il valore di GAS_CLAUDE_BIN nel .env con quello della shell, trattando vuoto e «claude» come lo stesso comando. Rischio esaminato: il merge poteva alterare il codice del ramo già rivisto. `git diff --cached --stat HEAD` non elenca gas.py, quindi il codice è identico a quello rivisto alla #549. Esito: ok.
- `gas.py:639`: con `setdefault` il registro tiene la prima riga del .env, come fa il caricatore. Rischio esaminato: la versione di main poteva rientrare nel codice durante la risoluzione. Le differenze rispetto a origin/main sono solo i blocchi della #292 (righe 447, 567, 620, 5008). Esito: ok.
- `tests/test_unit_dotenv.py:150`: con una chiave ripetuta, registro e caricatore tengono lo stesso valore. Rischio esaminato: test perso o duplicato nel merge. Il file è identico a HEAD e il test passa. Esito: ok.
- `tests/test_unit_kernel.py:11246`: casi del controllo sul .env (stesso valore, valore assente dal .env, nome nudo cercato nel PATH del timer). Rischio esaminato: righe perse. Il file è identico a HEAD. Esito: ok.
- `modules/web/lexbor.py:78`: codice della chat Mani. Rischio esaminato: una modifica del ramo poteva finire dentro il codice di main. `git diff --cached origin/main -- modules/web tests/test_unit_web_lexbor.py` dà 0 righe, quindi è identico a main. Esito: ok.
- `reports/stato_progetto.md:4`: le due voci in testa sono unite. Ho controllato via script che la riga sia esattamente «voce Motore» + « — prima: » + la riga 4 di main intera. Esito: ok.

**Altri controlli**
- `git diff --cached origin/main` contiene solo la PR #292: gas.py, i due test, i tre report di sessione, stato_progetto e memoria.
- Ho confrontato i file riga per riga, a ordine ignorato, con entrambi i genitori:
  - In stato_progetto mancano rispetto ai genitori solo la riga 4 (unita) e, rispetto a main, il punto 3 della ripartenza Motore. Quel punto l'ha cambiato il ramo e su main è uguale al punto di partenza comune, quindi la versione del ramo è corretta.
  - Nella memoria non manca nessuna riga di nessuno dei due genitori.
- handoff.md, ultimo_report.md e diff_sessione.md sono la versione del ramo, come dichiarato.
- Non ci sono marcatori di conflitto e `git diff --cached --check` è pulito.
- Ho rilanciato pytest su dotenv e web_lexbor: 35 passed, 103 skipped.

**Finding**
- R-550-1 (cosmetico, solo procedura): ho aggiunto la riga #550 a `.claude/agents/memoria_revisore.md` dopo il tuo staging, quindi ora è una modifica non in staging. Devi fare `git add .claude/agents/memoria_revisore.md` prima del `git commit` che chiude il merge. Inoltre il marcatore del review gate va rigenerato con `bash scripts/segna_review_ok.sh` sul diff staged finale, che ora include questa riga.

**Rischi esclusi**
- La suite kernel (1057 PASS, 0 FAIL) non l'ho rilanciata: mi fido del tuo dato, perché né gas.py né i test del kernel cambiano rispetto a HEAD, già verificato alla #549.
- La CI del commit di merge non è verificabile prima del commit e del push.

La riga contatore #550 è in memoria (/home/user/Gas/.claude/agents/memoria_revisore.md). Come chiesto, non ho lanciato `commit_memoria_revisore.sh`.

### Review #551 (chat Motore) — sul merge di origin/main (PR #293) in 4cf9d4c

## VERDETTO: APPROVATO CON RISERVE

Review #551 (chat Motore). Oggetto: il merge di origin/main a418887 (PR #293) dentro fix/note-forte-doctor-2 (PR #292, HEAD bd6336c). I file sono già unificati e il merge non è ancora committato.

Ho letto prima CLAUDE.md (sez. 5, 8, 9 e 10), poi `reports/stato_progetto.md` (righe 589 e 634-635) e infine la mia memoria (#543–#550 delle due chat Motore). Ho confrontato il diff staged con tutti e due i genitori del merge.

**Elementi del diff esaminati**

- `gas.py:592` e `gas.py:595`: tornano `_DOTENV_CARICATE` e `_DOTENV_SCAVALCATE` di main. Il commento ora dice che servono solo per GAS_CLAUDE_CLI. Ho cercato se qualche logica di uno dei due rami andasse persa. Verso HEAD il diff di gas.py contiene solo le aggiunte di main, verso main solo quelle del ramo, quindi nessuna riga persa da nessuna parte. Esito: ok.
- `gas.py:647-653`: nel loader, per le chiavi in lista bianca, viene prima il `setdefault` del registro dei valori, poi il blocco shell/.env di main (valore diverso → SCAVALCATE, valore uguale → CARICATE, poi `continue`). Ho controllato che la precedenza e il valore di ritorno non cambino. Il `continue` resta dopo tutte e due le scritture, `caricate` è invariato e la lista bianca limita ancora il registro dei valori a GAS_CLAUDE_BIN. Esito: ok.
- `gas.py:657`: `_DOTENV_CARICATE.update(caricate)` ripristinata a mano. Il merge automatico l'aveva persa senza segnalare conflitto, perché il ramo l'aveva tolta e main la usava. Ho provato un mutante (`pass` al posto della riga): pytest dà 2 failed (`test_nomi_caricati_…` e `test_valori_scavalcati_…`). Poi ho rimesso gas.py com'è nell'index e il diff è vuoto. Esito: ok.
- `gas.py:5034` e `gas.py:5040` (WARN su GAS_CLAUDE_CLI da main) e `gas.py:5051` (`_DOTENV_NEL_FILE.get("GAS_CLAUDE_BIN")` del ramo, al posto di `"GAS_CLAUDE_BIN" in _DOTENV_CARICATE`). Ho verificato che non ci sia un falso OK nuovo e che i due registri siano coerenti. Sono gli unici lettori in tutto il repo (controllato con grep). I due registri non si sovrappongono: CARICATE e SCAVALCATE servono solo per CLI, NEL_FILE solo per BIN. Con lo stesso BIN nella shell e nel `.env`, il confronto di valori dà None, come vuole V-1 bot #293. Esito: ok.
- `tests/test_unit_kernel.py:11206-11260` (T99s/T99t del ramo) e `tests/test_unit_kernel.py:11233-11260` (T99w/T99x di main): ho guardato se lo stato globale resta sporco fra un test e l'altro. Ogni blocco rimette a posto il proprio registro nel `finally`. Esito: ok.
- `tests/test_unit_dotenv.py:155-176`: ci sono tutti e due i test di main e i tre del ramo. Esito: riserva cosmetica (R-551-1).

**Prove che ho rilanciato io**: kernel 1059 PASS 0 FAIL (T99s, T99t, T99w e T99x PASS); `tests/test_unit_dotenv.py` 15 passed. Nessun marcatore di conflitto nei 5 file. In memoria e in stato_progetto nessuna riga persa da nessuno dei due genitori: le uniche righe diverse sono la 4 e la 589, unite di proposito, e contengono le voci di entrambe le chat.

**Riserve**
- R-551-1 COSMETICA: in `tests/test_unit_dotenv.py:155` c'è una sola riga vuota prima del `def test_nomi_caricati_…`, PEP 8 ne vuole due. Viene dalla giunzione del merge.

**Cosa non ho verificato**
- Non ho guardato `reports/handoff.md`, `ultimo_report.md` e `diff_sessione.md` riga per riga: sono log di sessione del ramo, fuori dal codice, e il merge li prende dal ramo per scelta dichiarata.
- Non ho verificato il comportamento reale del doctor sul Mac con `.env` e shell veri: in questo ambiente non si può riprodurre, l'ho provato solo coi registri messi a mano nei test.
- Non ho rilanciato il pytest completo: ho fatto solo dotenv e kernel.

Ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga #551, con la lezione: quando un ramo toglie una riga che l'altro usa, il merge automatico la perde senza conflitto. Bisogna confrontare il diff con tutti e due i genitori. Come richiesto non ho lanciato `commit_memoria_revisore.sh`, perché il merge è in corso.

## §5 DELTA TEST DEL MOTORE

Kernel: 1057 → 1057 PASS (nessun check nuovo, più casi dentro T99s e T99t). Conteggi del container locale (la CI ne conta di più).

```
=== RIEPILOGO: 1057 PASS, 0 FAIL ===
```

pytest (`python3 -m pytest -q tests`): `2284 passed, 61 skipped in 189.01s (0:03:09)`. Nessun FAIL.

Dopo il merge di main (77be957): kernel `=== RIEPILOGO: 1057 PASS, 0 FAIL ===`; `python3 -m pytest -q tests/test_unit_dotenv.py tests/test_unit_web_lexbor.py` → `32 passed, 85 skipped in 5.37s`.

Dopo 7bf0071: kernel `=== RIEPILOGO: 1057 PASS, 0 FAIL ===`; `python3 -m pytest -q tests/test_unit_dotenv.py tests/test_unit_claude_cli.py` → `42 passed in 0.92s`.

Dopo d03936c: kernel `=== RIEPILOGO: 1057 PASS, 0 FAIL ===`; pytest dotenv + claude_cli `42 passed in 8.47s`. Dopo il merge di main (b9c1dcd): kernel 1057 PASS, 0 FAIL; `python3 -m pytest -q tests/test_unit_dotenv.py tests/test_unit_web_lexbor.py` → `35 passed, 103 skipped in 0.97s`. Dopo il merge con la PR #293 (4cf9d4c): kernel `=== RIEPILOGO: 1059 PASS, 0 FAIL ===` (T99w e T99x arrivano da main); `python3 -m pytest -q tests` → `2289 passed, 104 skipped in 201.64s (0:03:21)`.

## §6 STATO CI

`gh` nel container non è autenticato: stato letto con gli strumenti GitHub della sessione e con la verifica esterna #292.

Mappatura commit→run:
- 861cc88, 5c21e08, b402b8c, 86bd88e → nessuna run su questi SHA (pushati insieme a 15b6704).
- 15b6704 → CI della push di 15b6704 (handoff-check rosso atteso: l'handoff è arrivato col commit dopo).
- a0872d2 → handoff-check success; unit-suite e verifica-bot in corso alla lettura della verifica esterna #292.
- 77be957 (merge di main) → nessuna run su questo SHA (pushato insieme a f94c4a0).
- f94c4a0 → handoff-check success; verifica-bot failure (APPROVATO CON RISERVE con le note chiuse in 7bf0071); unit-suite in corso alla lettura del bot.
- 68efe8c → nessuna run su questo SHA (pushato insieme a 7bf0071).
- 7bf0071 → nessuna run su questo SHA (pushato insieme a 67c2bca).
- 67c2bca → CI completata senza fallimenti (notifica check_suite.completed delle 23:51), verifica-bot success (APPROVATO CON RISERVE, V-1 BASSA chiusa in d03936c).
- ab985e5, d03936c, b9c1dcd → nessuna run su questi SHA (pushati insieme a bd6336c).
- bd6336c → unit-suite, handoff-check, verifica-bot success (APPROVATO CON RISERVE, una COSMETICA sul §7); il merge è fallito per il conflitto con la PR #293.
- 4cf9d4c → run non ancora disponibile alla scrittura dell'handoff (pushato insieme al commit di fine-task).
- commit di fine-task → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-545-1** (COSMETICA, review #545): CHIUSA in d03936c.
- **R-540-3** (BASSA, review #540, già aperta): su Linux il venv conta come visto dal timer senza un'unità systemd che lo attivi.
- **Verifica esterna #292** ([commento](https://github.com/Gasss23/Gas/pull/292#issuecomment-6483546190)): V-1 MEDIA conflitto con main CHIUSA da 77be957 (review #547); V-2 = R-545-1; **V-3** BASSA `_DOTENV_NEL_FILE` globale con `setdefault`: un secondo `_carica_dotenv` nello stesso processo terrebbe il valore vecchio (oggi una sola chiamata).
- **R-547-1** (COSMETICA, review #547): numeri di review #543–#546 doppi fra chat Mani e chat Motore.
- **Bot #292**: su a0872d2 BOCCIATO per V-1 MEDIA (conflitto con main, chiusa da 77be957); V-3 bot = R-547-1; V-4 bot BASSA (segreti nel registro) CHIUSA in 7bf0071. Su f94c4a0 check rosso: V-1 BASSA (BOCCIATO non registrato) chiusa qui, V-2 BASSA (= V-4 bot) e V-3 COSMETICA (T99s) chiuse in 7bf0071.
- **R-548-1** (COSMETICA, review #548): CHIUSA in d03936c.
- **Bot #292 su 67c2bca**: APPROVATO CON RISERVE; V-1 BASSA (vuoto e «claude») CHIUSA in d03936c insieme a R-545-1; V-2 COSMETICA (conteggi nella descrizione della PR) corretta nella descrizione.
- **R-550-1** (COSMETICA, review #550): solo procedura (memoria rimessa in stage prima del commit di merge), fatto.
- **Bot #292 su bd6336c**: APPROVATO CON RISERVE; V-1 COSMETICA (R-545-1 elencata ancora aperta in una riga di questo §7 e riga doppia nel §6): corretta qui, R-545-1 è CHIUSA in d03936c.
- **R-551-1** (COSMETICA, review #551): una riga vuota in meno prima di un test in tests/test_unit_dotenv.py.
- Restano aperte: V-3 ve #292 BASSA, R-540-3 BASSA, R-547-1 COSMETICA, R-551-1 COSMETICA.
