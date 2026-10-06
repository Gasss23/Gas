# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-06 — Gate IP: read in C (fail-open con byte non UTF-8) + discriminazione latin1 su glibc (sessione cloud notturna, arretrati)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #134 (https://github.com/Gasss23/Gas/pull/134) — prioritario (fail-open del gate IP su main). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4756657361","url":"https://github.com/Gasss23/Gas/pull/134"}`): `gh` non è autenticato in questo container.
2. Ordine di merge della notte: i report canonici sono riscritti da ogni PR; dopo un merge le altre vanno riallineate a main.

---

## §1 SCOPE & ESITO FETTE

- **V-2 #124/#125 discriminazione latin1 su glibc**: `FATTA`.
- **Fail-open del gate IP (read in UTF-8)**: `FATTA`.
- **R-167-1 / R-167-2**: `FATTA`.
- **Verifica su macOS**: `SALTATA — nessun Mac nel container; ragionamento del revisore in §4`.
- **Etichetta `verifica`**: `SALTATA — gh non autenticato e l'etichetta non esiste ancora`.
- **Marcatori `gasmerge-ip-ok` sui due assert nuovi** (il gate IP di fine-task li ha fermati al primo giro): `FATTA` — review #172.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 reports/diff_sessione.md           |  21 +++++++++-----------
 reports/handoff.md                 | 383 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  28 ++++++++++-----------------
 scripts/fine_task_finale.sh        |   5 ++++-
 scripts/gasmerge.sh                |  11 ++++++++---
 tests/test_unit_gasmerge.py        |  48 +++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_hooks.py           |  34 ++++++++++++++++++++++++++++++++
 9 files changed, 203 insertions(+), 335 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
a167949 test(gate-ip): marcatore gasmerge-ip-ok sui due assert nuovi con IP — review #172
f7c1208 chore(revisore): memoria review #172 — APPROVATO
bd2aa79 docs(gate-ip-read-locale): fine-task — report, handoff con verdetti #167/#170, diff sessione
26af320 fix(gate-ip): read in C nel filtro loopback — un byte non UTF-8 attaccato all'IP lo faceva passare (fail-open) — review #167/#170
4b120b1 chore(revisore): memoria review #170 — APPROVATO
3733a52 chore(revisore): memoria review #167 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-latin/`) resi relativi alla radice del repo, perché il gate B li risolva.

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
- `tests/test_unit_hooks.py:2076` — stesso marcatore su `assert b"10.0.0.1" in r.stderr`. Stesso rischio, stesso esito. — ok

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

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules. Test della macchina di controllo, eseguiti in questo container (Ubuntu glibc 2.39, bash 5.2.21, git 2.43):

```
LC_ALL=C:       pytest gasmerge+hooks+gate+handoff_check → 278 passed
LC_ALL=C.UTF-8: pytest gasmerge+hooks+gate+handoff_check → 278 passed
```

(origin/main: 273 nelle stesse suite; +5 test, di cui due parametrizzati.)

## §6 STATO CI

`gh` non autenticato (CI NON VERIFICATA con la CLI). Mappatura commit → run:
- `3733a52`, `4b120b1`, `26af320`: pushati insieme, run CI sul push di `26af320` — esito non letto alla scrittura dell'handoff.
- `4fe5540` (primo fine-task, mai pushato da solo: il gate IP l'ha fermato), `f7c1208`, commit dei marcatori: nessuna run propria, pushati insieme al commit di fine-task.
- commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- macOS (bash 3.2 / bash 5 homebrew) non provato.
- `review_gate.sh:76` ha un ciclo `read` simile ma legge il file del perimetro (protetto da review): non approfondito (dalla #167).
