# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Note del bot su #291: il doctor confronta il valore di GAS_CLAUDE_BIN nel .env, nome nudo, collegamenti dei test (chat Motore)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #292 (https://github.com/Gasss23/Gas/pull/292): review #545 APPROVATO CON RISERVE (COSMETICA); con verdetto pulito del bot la mergia l'agente, con riserve serve il «sì» dell'operatore (CLAUDE.md §10). Numero e URL dalla risposta JSON di `mcp__github__create_pull_request` (`gh` nel container non è autenticato).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — V-1 bot #291 + R-543-1 + R-544-1 (valore nel .env)**: `FATTA` — `_DOTENV_NEL_FILE: Dict[str, str]`, WARN «altro valore».
- **Fetta 2 — V-2 bot #291 + R-543-2 (nome nudo)**: `FATTA`.
- **Fetta 3 — R-544-2 (riga doppia)**: `FATTA` — `setdefault`.
- **Fetta 4 — V-3 (R-541-1) e V-4 bot #291**: `FATTA`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  7 +++++++
 gas.py                             | 30 ++++++++++++++++++++----------
 reports/diff_sessione.md           | 15 ++++++---------
 reports/stato_progetto.md          |  4 ++--
 reports/ultimo_report.md           | 22 +++++++++++-----------
 tests/test_unit_dotenv.py          | 19 ++++++++++++++-----
 tests/test_unit_kernel.py          | 46 ++++++++++++++++++++++++++++++----------------
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d», e la riga di totale è tolta. Conteggi presi con i report già in stage.

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

Kernel: 1057 → 1057 PASS (nessun check nuovo, più casi dentro T99s e T99t). Conteggi del container locale (la CI ne conta di più).

```
=== RIEPILOGO: 1057 PASS, 0 FAIL ===
```

pytest (`python3 -m pytest -q tests`): `2284 passed, 61 skipped in 189.01s (0:03:09)`. Nessun FAIL.

## §6 STATO CI

`gh` nel container non è autenticato: stato letto con gli strumenti GitHub della sessione.

Mappatura commit→run:
- 861cc88, 5c21e08, b402b8c, 86bd88e → nessuna run su questi SHA (pushati insieme a 15b6704).
- 15b6704 → run non ancora disponibile alla scrittura dell'handoff (handoff-check rosso atteso: l'handoff arriva col commit dopo).
- commit di fine-task → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-545-1** (COSMETICA, review #545): con `GAS_CLAUDE_BIN=` vuoto nel `.env` e un percorso nella shell, il WARN dice «userà quello» ma il timer cerca `claude`.
- **R-540-3** (BASSA, review #540, già aperta): su Linux il venv conta come visto dal timer senza un'unità systemd che lo attivi.
