# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-06 — Gate IP: read in C (fail-open con byte non UTF-8) + discriminazione latin1 su glibc (sessione cloud notturna, arretrati)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #134 (https://github.com/Gasss23/Gas/pull/134) — prioritario: chiude DUE fail-open già su main (gate IP e gate di review, in locale UTF-8). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4756657361","url":"https://github.com/Gasss23/Gas/pull/134"}`): `gh` non è autenticato in questo container.
2. Ordine di merge della notte: i report canonici sono riscritti da ogni PR; dopo un merge le altre vanno riallineate a main.

---

## §1 SCOPE & ESITO FETTE

- **V-2 #124/#125 discriminazione latin1 su glibc**: `FATTA`.
- **Fail-open del gate IP (read in UTF-8)**: `FATTA`.
- **R-167-1 / R-167-2**: `FATTA`.
- **Verifica su macOS**: `SALTATA — nessun Mac nel container; ragionamento del revisore in §4`.
- **Etichetta `verifica`**: `SALTATA — gh non autenticato e l'etichetta non esiste ancora`.
- **Marcatori `gasmerge-ip-ok` sui due assert nuovi** (il gate IP di fine-task li ha fermati al primo giro): `FATTA` — review #172.
- **Verifica esterna §4quater #134**: `FATTA` — APPROVATO CON RISERVE (§8).
- **V-2 #134 — stesso difetto in `review_gate.sh:76` (fail-open del gate di review, provato: exit 0)**: `FATTA`.
- **V-3 #134 — test locale-dipendenti saltabili in CI**: `FATTA` (`GAS_TEST_LOCALE_UTF8_ATTESO=1`).
- **R-177-1 / R-177-2 / R-178-1**: `FATTA`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   8 +++++++
 .claude/hooks/review_gate.sh       |   2 +-
 .github/workflows/ci.yml           |   7 +++++-
 reports/diff_sessione.md           |  25 ++++++++++----------
 reports/handoff.md                 | 466 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  31 ++++++++++--------------
 scripts/check_verdetto.py          |  12 ++++++----
 scripts/fine_task_finale.sh        |   5 +++-
 scripts/gasmerge.sh                |  11 ++++++---
 tests/test_unit_gasmerge.py        |  56 +++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_handoff_check.py   |  26 ++++++++++++++++++++
 tests/test_unit_hooks.py           |  61 +++++++++++++++++++++++++++++++++++++++++++++++
 13 files changed, 392 insertions(+), 322 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
f450766 fix(gate-review): read in C anche nel perimetro di review_gate.sh (fail-open), locale UTF-8 esigito in CI, check_verdetto fail-closed su perimetro non UTF-8 — review #177/#178/#179
ccc2f27 chore(revisore): memoria review #179 — APPROVATO
09cf060 chore(revisore): memoria review #178 — APPROVATO CON RISERVE
f0bc429 chore(revisore): memoria review #177 — APPROVATO CON RISERVE
3fc1e95 docs(gate-ip-read-locale): fine-task ter — marcatori IP sulle righe dei verdetti, hash del primo fine-task corretto
4e5d6db docs(gate-ip-read-locale): fine-task bis — handoff con verdetto #172 e report redatto (gate IP)
a167949 test(gate-ip): marcatore gasmerge-ip-ok sui due assert nuovi con IP — review #172
f7c1208 chore(revisore): memoria review #172 — APPROVATO
bd2aa79 docs(gate-ip-read-locale): fine-task — report, handoff con verdetti #167/#170, diff sessione
26af320 fix(gate-ip): read in C nel filtro loopback — un byte non UTF-8 attaccato all'IP lo faceva passare (fail-open) — review #167/#170
4b120b1 chore(revisore): memoria review #170 — APPROVATO
3733a52 chore(revisore): memoria review #167 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Trasformazioni meccaniche, nient'altro: (1) i path assoluti del worktree (`/home/user/wt-latin/`) resi relativi alla radice del repo, perché il gate B li risolva; (2) sulle righe che citano un IP è stato aggiunto in coda il commento HTML `<!-- gasmerge-ip-ok -->`, perché il gate IP non fermi l'handoff.

### Review #167 — diff staged del fix

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md (sez. 5, 8, 9, 10), le voci di `reports/stato_progetto.md` cercate con grep (V-2 #124/#125, latin1) e le ultime voci della memoria. Il diff staged non tocca la history, i provider, `_get_window` né il limite di iterazioni. Il Wall of Shame non si applica.

**Riproduzione (la parte decisiva)**: su bash 5.2.21 con `LC_ALL=C.UTF-8`, il ciclo `printf "x1\xe9\ny2"` stampa un solo "got". Lo stesso ciclo con `IFS= LC_ALL=C read` ne stampa due. Il bug è reale e il fix lo chiude.

Gravità (MEDIA, già sul main):
- Il byte `\xe9` seguito dal newline viene letto come un carattere multibyte e fonde la riga con la successiva.
- Se la riga non è l'ultima, il corpo del ciclo vede il blocco fuso e il grep trova comunque l'IP. Quindi blocca.
- Se la riga fusa è l'ultima dell'output di `git grep`, `read` arriva a EOF e il corpo del ciclo non gira. La riga si perde.
- Il fail-open scatta quando l'unico IP non-loopback sta nell'ultima riga e quella riga finisce con un byte non UTF-8. Chi scrive il branch può ottenerlo apposta: basta il file ultimo in ordine alfabetico.

**Elementi del diff esaminati**:
- `scripts/gasmerge.sh:116` — `while IFS= LC_ALL=C read -r line` nel filtro loopback. Rischio esaminato: l'assegnazione `LC_ALL=C` davanti a un builtin vale davvero solo per `read`, e serve per tutto il ciclo. Ho provato la mutation `LC_ALL=C read`→`read` sotto `LC_ALL=C.UTF-8`: 1 test fallito, quindi la mutation è uccisa. File ripristinato e working tree pulito. — ok
- `scripts/fine_task_finale.sh:87` — stesso fix, con `printf '%s\n'`. Stessa mutation: uccisa. — ok
- `tests/test_unit_gasmerge.py:754` — `test_byte_latin1_attaccato_all_ip_in_locale_utf8`, parametrizzato con il byte prima e dopo l'IP. Rischio esaminato: il test deve discriminare qualunque sia il locale del runner. Il test forza `LC_ALL` con monkeypatch. La mutation di `read` la uccide solo il caso col byte DOPO l'IP; il caso col byte prima copre le mutation su `git grep` e `grep` (lì mi fido delle mutation dichiarate dall'agente). Controlla anche che la riga bloccata sia stampata, il che copre `grep -Fx`. — ok
- `tests/test_unit_hooks.py:2059` — `test_finale_4f_bis_byte_attaccato_locale_utf8`, il gemello per lo script finale. — ok
- `tests/test_unit_gasmerge.py:137` — `_locale_utf8()`. Normalizza `utf8`→`utf-8`, quindi riconosce `C.utf8` di glibc. Se il comando `locale` non c'è, esce con `FileNotFoundError` invece di saltare il test. La funzione è anche duplicata identica in `test_unit_hooks.py:1726`. — riserva minima (R-167-2)
- **Contesto** `scripts/gasmerge.sh:193` (non toccato dal diff) — `while IFS= read -r f` legge `ENGINE_DIFF`, cioè l'output di `diff -z | tr '\0' '\n'`. È la stessa classe di bug. L'ho provato: con `$'a\xe9\ngas.py\nz'` in locale UTF-8 esce la riga `[a\351\ngas.py]`, quindi `gas.py` sparisce dal promemoria "FILE DI MOTORE". — riserva R-167-1

**Prove eseguite**: la suite gasmerge + hooks + gate + handoff_check dà **277 passed** sia con `LC_ALL=C` sia con `LC_ALL=C.UTF-8`. I nuovi test passano.

**Merge con la PR #131 (B2)**: in `gasmerge.sh` gli hunk di B2 arrivano fino alla riga 100 del main, quello di questa PR parte da 110. Nei test, B2 tocca le righe ~557–574 e ~1025–1214, questa PR le righe 134 e ~740. Niente si sovrappone: atteso un merge senza conflitti, non provato con un merge reale.

**macOS** (solo ragionamento, non provato):
- `/bin/bash` 3.2 di sistema: per quanto ne so, `read` legge byte per byte e non ha la lettura multibyte delle versioni più recenti. Quindi probabilmente non è colpito.
- I due script usano `#!/usr/bin/env bash`: con il bash 5 di homebrew primo nel PATH e `LANG=en_US.UTF-8` (il default del Terminale) il bug c'è. Il fix è innocuo anche su 3.2.

**Riserve**:
- **R-167-1 (BASSA, preesistente, stessa classe)**: in `gasmerge.sh:193` (e nel `read -r v` annidato) va messo `LC_ALL=C read` e aggiunto un test con un path che finisce con un byte non UTF-8 seguito da un file di motore. Riguarda solo il promemoria per l'operatore, non il gate IP; va però tracciata in `stato_progetto.md`.
- **R-167-2 (minima)**: se `locale` manca, saltare il test invece di farlo fallire, e mettere `_locale_utf8` in un modulo comune.

**Rischi esclusi**:
- Comportamento su macOS con bash 3.2 o 5 di homebrew: non ho un Mac.
- Le mutation su `git grep` (x2), `grep -qE` e `grep -Fx`, e l'equivalenza di `sed` tra i due locale: non le ho rifatte, ho rifatto solo quella di `read` in entrambi gli script.
- L'esito sul runner CI ubuntu: non l'ho osservato, mi baso sul fatto che glibc ha `C.UTF-8` integrato.
- `review_gate.sh:76`: ha lo stesso tipo di ciclo `read`, ma legge il file del perimetro, che è un file del repo protetto dalla review. Non l'ho approfondito.

La riga contatore #167 e una lezione nuova sono in `.claude/agents/memoria_revisore.md`, committate da sole con lo script atomico (commit `3733a52`). Il diff staged non l'ho committato (5 file, +74/−4).

### Review #170 — diff staged finale

## VERDETTO: APPROVATO

Ri-review #170 del diff staged aggiornato in `/home/user/wt-latin`. Ho controllato il delta rispetto alla #167: le due riserve sono chiuse.

**Elementi del diff esaminati**:
- `scripts/gasmerge.sh:195` — ora c'è `while IFS= LC_ALL=C read -r f` nel ciclo che legge `ENGINE_DIFF`. Rischio esaminato: un path che finisce con un byte non UTF-8 faceva sparire il file di motore successivo dal promemoria. Ho tolto `LC_ALL=C` da questo `read` e `test_path_non_utf8_non_nasconde_il_motore` fallisce, quindi la mutation è uccisa. File ripristinato e working tree pulito. — ok (R-167-1 chiusa)
- `scripts/gasmerge.sh:198` — `while IFS= LC_ALL=C read -r v` sulle voci del perimetro. Ho fatto la stessa mutation e il test passa: la mutation sopravvive. In pratica è equivalente, perché le voci vengono da `perimetro_review.txt`, che è ASCII e passa comunque dal revisore. Lo dichiara anche `stato_progetto.md`. — ok
- `tests/test_unit_gasmerge.py:464` — il test crea il path `"a\udce9"`, che su POSIX diventa il byte 0xE9 nel nome, più `gas.py`. Forza `LC_ALL` a un locale UTF-8 e controlla `"\ngas.py\n"` nella sezione FILE DI MOTORE e l'assenza di "doc-only". Rischio esaminato: il test deve discriminare davvero. Lo fa: la mutation del `read` esterno lo fa fallire. — ok
- `tests/test_unit_hooks.py:1726` e la sua copia in `test_unit_gasmerge.py` — `_locale_utf8()` ora intercetta `OSError` e restituisce None, quindi il test viene saltato invece di andare in errore. La duplicazione resta, con motivazione accettabile. — ok (R-167-2 chiusa)

**Prove eseguite**: i test nuovi danno 3 passed (path non UTF-8 e i due casi del byte attaccato). Ho rifatto io solo le due mutation di `read` in `gasmerge.sh`.

**Rischi esclusi**:
- La suite completa da 278 test nei due locale non l'ho rieseguita. Mi baso sulla dichiarazione dell'agente e sui 277 che avevo verificato nella #167.
- Il merge-tree con `origin/feat/merge-automatico-z1xjx2` non l'ho rifatto.
- macOS resta solo ragionato, come nella #167.

La riga contatore #170 è committata in `.claude/agents/memoria_revisore.md` (commit `4b120b1`). Il diff staged non l'ho committato.

### Review #172 — marcatori gasmerge-ip-ok sui due assert nuovi

## VERDETTO: APPROVATO

Review #172 del diff staged in `/home/user/wt-latin`: 2 file, 2 righe, solo commenti.

**Elementi del diff esaminati**:
- `tests/test_unit_gasmerge.py:789` — aggiunge `# gasmerge-ip-ok` in coda a `assert "8.8.8.8" in result.stdout`. Rischio esaminato: il marcatore potrebbe cambiare la semantica del test, oppure allowlistare più del necessario. Non succede: è un commento Python e vale solo per quella riga, perché il filtro `--and --not` della R-147-1 guarda il solo contenuto della riga. — ok
- `tests/test_unit_hooks.py:2076` — stesso marcatore su `assert b"10.0.0.1" in r.stderr`. Stesso rischio, stesso esito. — ok <!-- gasmerge-ip-ok -->

**Prove eseguite**:
- Ho ricostruito il tree dell'index con `git write-tree` e ci ho passato la stessa `git grep` del gate (`LC_ALL=C`, `--and --not`), poi la rimozione dei 127.x. La regex esatta del gate non trova nessun IP non-loopback non marcato.
  - La regex più larga che ho usato all'inizio segnalava 3 righe. Una è una riga di versioni in `reports/ultimo_report.md`, che con la regex esatta non dà nulla. Le altre due sono i casi `1.2.3.4.5` di `test_unit_gasmerge.py:977` e `test_unit_hooks.py:2198`: per progetto non sono IP, e quei test si aspettano proprio "tutti loopback".
- Con i due marcatori, la PR #134 non dovrebbe più bloccare se stessa al gate.
- Sui test interessati ho avuto 5 passed. I 7 dichiarati dall'agente non li ho contati.

**Rischi esclusi**:
- Non ho eseguito `bash scripts/fine_task_finale.sh` né `gasmerge.sh` per davvero, perché pushano o toccano GitHub. Ho replicato il gate a mano sul tree dell'index.
- L'ordine dei commit locali e il push di 4fe5540 / bd2aa79 non li ho verificati.

**Cosa ho trovato nel worktree**: `reports/ultimo_report.md` risulta modificato e non in staging. Non l'ho toccato io: in questa passata l'ho solo letto. Va controllato prima del commit.

La riga contatore #172, con dentro una lezione, è committata in `.claude/agents/memoria_revisore.md` (commit `f7c1208`). Il diff staged non l'ho committato.

### Review #177 — seguiti della verifica esterna #134

## VERDETTO: APPROVATO CON RISERVE

Review #177 del diff staged in `/home/user/wt-latin`: 5 file, +50/−11. Nasce dalla verifica esterna della PR #134. Il fix chiude un fail-open reale del gate di review, e l'ho riprodotto.

**Elementi del diff esaminati**:
- `.claude/hooks/review_gate.sh:76` — in `_aggiungi_voci` ora c'è `while IFS= LC_ALL=C read -r riga || [ -n "$riga" ]`.
  - Rischio: in locale UTF-8 una voce del perimetro che finisce con un byte non UTF-8 si fonde con la successiva. Lo `tr -d '[:space:]'` toglie il newline e resta `voce\xe9speciale.txt`, quindi la voce `speciale.txt` sparisce. Un file del perimetro poteva così essere committato senza review.
  - Prova: ho tolto `LC_ALL=C` e il test nuovo fallisce; con il fix passa. Hook ripristinato, index invariato. — ok
- `tests/test_unit_hooks.py:674` — `test_gate_perimetro_byte_non_utf8_in_locale_utf8_blocca`. Il perimetro `voce\xe9\nspeciale.txt` è identico in HEAD, index e working tree, quindi l'unione dei perimetri non maschera la fusione. Il test controlla exit 2. Rischio esaminato: il test deve discriminare. Lo fa: la mutation lo uccide. — ok
- `tests/test_unit_hooks.py:1757` e `tests/test_unit_gasmerge.py:151` — `_esigi_locale_utf8()` fa fallire il test con `GAS_TEST_LOCALE_UTF8_ATTESO=1` e lo salta senza la variabile. La chiamata dalla classe a riga 674 alla funzione definita più in basso nel modulo funziona, perché il nome si risolve quando il test gira. Tutti e 4 i test che dipendono dal locale ora la usano. — ok
- `.github/workflows/ci.yml:26` — la variabile `env` è a livello del job `unit-suite`. Non è un segreto né una variabile di provider. Subito dopo però c'è il commento "Nessun `env:` di provider…", che ora segue un blocco `env:`. — ok, riserva cosmetica R-177-2

**Prove eseguite**: il test nuovo dà 1 passed con il fix e 1 failed con la mutation. Una grep su hooks e scripts trova un solo `read` senza `LC_ALL=C`: `scripts/gasmerge.sh:233` `read -r ANS`, che è interattivo e non ha bisogno del fix.

**Riserve**:
- **R-177-1 (BASSA, fail-closed)**: `scripts/check_verdetto.py:133` legge il perimetro con `read_text(encoding="utf-8")` e intercetta solo `OSError`. Un perimetro con un byte non UTF-8 solleva un `UnicodeDecodeError` non gestito. Il gate B andrebbe in crash invece di dare un messaggio controllato, ma senza far passare nulla. Basterebbe intercettare anche `UnicodeDecodeError` (oppure usare `errors="surrogateescape"`) e aggiungere un test.
- **R-177-2 (cosmetica)**: riformulare il commento di `ci.yml` in "nessun env di provider né secrets".

**Rischi esclusi**:
- La suite completa da 279 test con la variabile, nei due locale: non l'ho rieseguita, mi baso sulla dichiarazione dell'agente.
- La prova "senza `locale` nel PATH → fail/skip": non l'ho ripetuta.
- Il conflitto di `ci.yml` con il branch `fix/kernel-skip-senza-bwrap`: non l'ho verificato. Hunk diversi, come dichiarato, ma vicini.
- La prima run CI con la variabile attiva: non l'ho osservata.

La riga contatore #177, con dentro una lezione, è committata in `.claude/agents/memoria_revisore.md` (commit `f0bc429`). Il diff staged non l'ho committato.

### Review #178 — ri-review R-177-1/2

## VERDETTO: APPROVATO CON RISERVE

Ri-review #178 del diff staged in `/home/user/wt-latin`: 7 file, +69/−16. Nel delta rispetto alla #177, R-177-1 e R-177-2 sono chiuse. Resta una riserva bassa: il ramo della versione alla BASE funziona ma non ha un test.

**Elementi del diff esaminati**:
- `scripts/check_verdetto.py:135` — ora intercetta `except (OSError, UnicodeDecodeError): return None` sul perimetro letto dal file dello script. Rischio esaminato: prima un byte non UTF-8 mandava in crash il gate B. Ho rimesso `except OSError` e `test_r177_1_perimetro_non_utf8_fail_closed` fallisce, quindi la mutation è uccisa. File ripristinato e index invariato. — ok
- `scripts/check_verdetto.py:141` — `try/except UnicodeDecodeError` attorno al `git show` della versione alla BASE. `_git` usa `text=True` senza `errors=`, quindi l'eccezione è reale. L'ho provato a mano in scratchpad: repo con perimetro `gas.py\nvoce\xe9` committato, chiamata con `base='HEAD'` → `None`. Il comportamento è corretto, ma questo ramo non ha un test. — riserva R-178-1
- `scripts/check_verdetto.py:238` — il messaggio di errore ora dice "assente, vuoto o non UTF-8". È fail-closed: exit 1. — ok
- `tests/test_unit_handoff_check.py:707` — il test carica il modulo e verifica che un perimetro con `voce\xe9` dia `None`. Discrimina: la mutation lo fa fallire. — ok
- `.github/workflows/ci.yml:30` — commento riformulato. Coerente: nessuna variabile di provider, nessun `secrets:`. — ok (R-177-2 chiusa)

**Prove eseguite**: `tests/test_unit_handoff_check.py` dà 41 passed.

**Riserve**:
- **R-178-1 (BASSA)**: aggiungere un test per il ramo BASE, con un repo dove il perimetro committato alla base contiene un byte non UTF-8 e l'atteso è `None`. Oggi togliere quel `try` non farebbe fallire nessun test.
- **Nota (non bloccante)**: se il perimetro di main diventasse non UTF-8, il gate B bloccherebbe tutte le PR. È lo stesso tipo di stallo della R-143-3. Lo accetto perché il perimetro su main passa comunque dalla review.

**Rischi esclusi**:
- La suite da 280 test con `GAS_TEST_LOCALE_UTF8_ATTESO=1` nei due locale: non l'ho rieseguita, mi baso sulla dichiarazione dell'agente.
- Il comportamento in CI: il job handoff-check esegue `check_verdetto.py` preso da `origin/main` (R-141-2), quindi la modifica conta in CI solo dopo il merge. Non verificabile prima.

La riga contatore #178 è committata in `.claude/agents/memoria_revisore.md` (commit `09cf060`). Il diff staged non l'ho committato.

### Review #179 — ri-review R-178-1

## VERDETTO: APPROVATO

Ri-review #179 del diff staged in `/home/user/wt-latin`. L'unico delta rispetto alla #178 è il test che chiude R-178-1, e ho verificato che discrimina.

**Elementi del diff esaminati**:
- `tests/test_unit_handoff_check.py:716` — `test_r178_1_perimetro_base_non_utf8_fail_closed`. Crea un repo git vero con il perimetro `gas.py\nvoce\xe9` committato, passa un file dello script valido e chiama `_carica_perimetro(path=valido, repo=repo, base="HEAD")`, che deve restituire `None`. Rischio esaminato: il test deve discriminare davvero il ramo BASE. Lo fa (vedi sotto). — ok
- `scripts/check_verdetto.py:141` — il `try/except UnicodeDecodeError` attorno al `git show` della BASE. L'ho tolto con un replace esatto e il test fallisce (1 failed), quindi la mutation è uccisa. Con il file ripristinato, `test_unit_handoff_check.py` dà 42 passed e il working tree è pulito. — ok (R-178-1 chiusa)

**Rischi esclusi**:
- Il test presume che Python decodifichi l'output di `git show` in UTF-8. Su un sistema con codifica locale latin-1 non ci sarebbe nessun `UnicodeDecodeError`, e il test fallirebbe anche con il fix: un falso rosso, non un fail-open. Non l'ho provato. Sul runner ubuntu e con `LC_ALL=C` su Python 3.11 la codifica dovrebbe essere UTF-8 grazie alla coercion del locale C, ma non l'ho verificato.
- La suite completa non l'ho rieseguita, solo il file handoff_check.

La riga contatore #179 è committata in `.claude/agents/memoria_revisore.md` (commit `ccc2f27`). Quella riga dà la coercion UTF-8 come certa, ma io non l'ho verificata. Il diff staged non l'ho committato.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules. Test della macchina di controllo, in questo container (Ubuntu glibc 2.39, bash 5.2.21, git 2.43), con `GAS_TEST_LOCALE_UTF8_ATTESO=1`:

```
LC_ALL=C:       pytest gasmerge+hooks+gate+handoff_check → 281 passed
LC_ALL=C.UTF-8: pytest gasmerge+hooks+gate+handoff_check → 281 passed
```

(origin/main: 273 nelle stesse suite; +8 test.)

## §6 STATO CI

Stato dal connettore GitHub e dalla verifica esterna #134 (`gh` non autenticato qui). Mappatura commit → run:
- `3733a52`, `4b120b1`, `26af320`: pushati insieme → run 37441613564 (CI #661) su `26af320`: **failure** — atteso, handoff non ancora rigenerato.
- `bd2aa79`, `f7c1208`, `a167949`, `3fc1e95` (fine-task bis/ter): pushati insieme → run 37441959792 (CI #664) su `3fc1e95`: **success** (unit-suite e handoff-check).
- commit dei seguiti #177–#179 e di questo fine-task: pushati insieme, run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- macOS (bash 3.2 / bash 5 homebrew) non provato.
- Nota #178: se il perimetro su main diventasse non UTF-8, il gate B bloccherebbe tutte le PR (stallo tipo R-143-3; accettato: il perimetro passa dalla review).
- Rischio escluso #179: con codifica locale latin-1 il test R-178-1 darebbe un falso rosso (non un fail-open).
- V-4 #134: la mutation sul `read -r v` annidato di gasmerge sopravvive (equivalente in pratica, dichiarato).

## §8 VERIFICA ESTERNA #134 (verdetto integrale)

Lanciata con `Applica .claude/verifica_esterna.md a: <URL_HANDOFF di 3fc1e95> <URL_PR>` (agente nuovo, Sonnet). V-2 e V-3 chiuse (review #177–#179); V-1 (stat/CI fotografati prima dell'ultimo commit) strutturale; V-4 dichiarata. Fetta di sicurezza: secondo passaggio consigliato all'operatore nella chat claude.ai.

VERIFICA ESTERNA PR #134 — APPROVATO CON RISERVE

**Metodo**
- Ho lavorato su un clone usa-e-getta nella scratchpad, al commit pinnato 3fc1e95. Merge-base con main: e91ceb4.
- Ho confrontato §2 e §3 dell'handoff con `git diff --stat` e `git log` reali.
- Ho rieseguito le 4 suite toccate (gasmerge, hooks, gate, handoff_check) alla base e al commit, sia con `LC_ALL=C` sia con `LC_ALL=C.UTF-8`.
- Ho rifatto le mutation sui due `read` del filtro loopback.
- Ho letto i check CI reali e il ruleset via API REST di GitHub.
- Il repo reale non è stato toccato: `git status` di /home/user/Gas è vuoto.

**CLAIM VERIFICATI**
- **VERO — §3 (git log).** `git log` da e91ceb4 mostra gli stessi 8 commit del log dell'handoff. Il commit di fine-task 3fc1e95 non è nel §3, e l'handoff lo dichiara.
- **FALSO, minore — §2 (diff --stat).** L'handoff dà 203 inserzioni e un handoff.md di 383 righe. Il diff reale al commit pinnato è 218 inserzioni, 335 cancellazioni e handoff.md a 398 righe. Il §2 è stato scritto prima del commit "ter" ed è obsoleto. I 9 file elencati sono corretti.
- **VERO — delta test.** La base e91ceb4 dà 273 passed con `LC_ALL=C.UTF-8`. Il commit pinnato dà 278 passed con `LC_ALL=C` e 278 con `LC_ALL=C.UTF-8`. Il delta di +5 coincide con quanto dichiarato.
- **VERO — i nuovi test discriminano.**
  - Ho tolto `LC_ALL=C` dal `read` in `gasmerge.sh`: fallisce `test_byte_latin1_attaccato_all_ip_in_locale_utf8[8.8.8.8\xe9\n]`. <!-- gasmerge-ip-ok -->
  - Ho fatto lo stesso in `fine_task_finale.sh`: fallisce `test_finale_4f_bis_byte_attaccato_locale_utf8[10.0.0.1\xe9\n]`. <!-- gasmerge-ip-ok -->
  - Dopo ogni mutation ho ripristinato il file.
- **VERO — CI sullo SHA 3fc1e95.** `unit-suite` e `handoff-check` sono `success`. `esito`, `verifica` e `smista` sono `skipped`.
- **VERO — check required nel ruleset `main-lock`.** Sono `unit-suite` e `handoff-check`, entrambi verdi sullo SHA.
- **VERO — il fix non indebolisce nessun gate.** Il diff dei due script cambia solo `read` in `LC_ALL=C read` (3 occorrenze). Non ci sono altre modifiche logiche.
- **VERO — i marcatori `gasmerge-ip-ok` nell'handoff.** Il file ne contiene 6, e l'handoff-check è verde.

**FINDING**
- **V-1 (BASSA) — §6 dell'handoff dichiara "CI NON VERIFICATA" e il §2 è obsoleto.** La CI sullo SHA era verde e leggibile. Il §2 va rigenerato dopo l'ultimo commit. Fix: rigenerare il §2 come ultima operazione, oppure dichiararlo "pre-ter".
- **V-2 (BASSA) — resta un `read` senza `LC_ALL=C` nel perimetro.** In `.claude/hooks/review_gate.sh:76` c'è `while IFS= read -r riga || [ -n "$riga" ]`. Un byte non UTF-8 in fondo a una riga di `perimetro_review.txt` fonderebbe due voci e farebbe sparire una voce del perimetro, quindi un fail-open del gate di review. Il file è del repo e protetto dal revisore, e l'handoff lo elenca fra le riserve (§7), ma non è coperto da nessun test né da una voce tracciata. Fix: `LC_ALL=C read` più un test gemello.
- **V-3 (BASSA) — il test dipende dal locale del runner.** I test di discriminazione vengono saltati (`pytest.skip`) se `locale -a` non elenca un locale UTF-8. Su questo container `C.utf8` esiste e i test girano. Non ho verificato che sul runner CI ubuntu girino davvero e non siano saltati: la CI è verde, ma "success" non dimostra l'esecuzione. Fix: asserire in CI che i test non siano `skipped`.
- **V-4 (BASSA) — la mutation sul `read` annidato di `gasmerge.sh` sopravvive.** Il `read -r v` annidato ha `LC_ALL=C` ma nessun test lo discrimina. La riserva è dichiarata dal revisore (le voci del perimetro sono ASCII).

**NON VERIFICATO**
- macOS (bash 3.2 o bash 5 di homebrew): nessun Mac disponibile.
- Esecuzione reale di `bash scripts/gasmerge.sh` e `fine_task_finale.sh` end-to-end: pushano o toccano GitHub. Ho coperto il comportamento solo con i test.
- Non ho rifatto le mutation su `git grep` (x2), `grep -qE` e `grep -Fx`, né quelle del `read` esterno e annidato di `gasmerge.sh:193-198`. Ho rifatto solo le due mutation su `read` del filtro loopback.
- Il merge senza conflitti con le altre PR della notte (#131 e simili).
- `gh pr view` non funziona (GraphQL bloccato), quindi non ho letto lo stato di mergeability della PR.

**RACCOMANDAZIONE**
Il fix è corretto e dimostrato: chiude il fail-open reale del gate IP in locale UTF-8, i test discriminano e la CI è verde. Si può fare il merge. Prima di altro lavoro sul perimetro:
1. Tracciare V-2 (`review_gate.sh:76`) in `stato_progetto.md` e chiuderlo con `LC_ALL=C` più un test.
2. Rigenerare il §2 e correggere il §6 dell'handoff.
3. Verificare nei log CI che i test locale-dipendenti non siano `skipped` (V-3).
