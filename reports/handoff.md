# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-06 — F-mac-2: docstring raw in normalizza_telefono + guardia T79a (sessione cloud notturna, arretrati)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #135 (https://github.com/Gasss23/Gas/pull/135). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4756658435","url":"https://github.com/Gasss23/Gas/pull/135"}`): `gh` non è autenticato in questo container.
2. Ordine di merge della notte: i report canonici sono riscritti da ogni PR; dopo un merge le altre vanno riallineate a main.

---

## §1 SCOPE & ESITO FETTE

- **F-mac-2 — escape invalidi nella docstring**: `FATTA`.
- **Guardia T79a (anche su 3.11)**: `FATTA`.
- **Suite su Python 3.14 (Mac)**: `SALTATA — non disponibile nel container (provate 3.11 e 3.13)`.
- **Etichetta `verifica`**: `SALTATA — gh non autenticato e l'etichetta non esiste ancora`.
- **Verifica esterna §4quater #135**: `FATTA` — APPROVATO CON RISERVE (§8); V-2 (T79a solo sul motore) e V-3 (nome del check) CHIUSE con review #174/#176.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 +++++
 modules/memory/store.py            |   2 +-
 reports/diff_sessione.md           |  19 ++++++--------
 reports/handoff.md                 | 492 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  27 +++++++-------------
 tests/test_unit_kernel.py          |  32 ++++++++++++++++++++++++
 7 files changed, 264 insertions(+), 316 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
1b57390 test(memoria): T79a su tutti i .py tracciati, robusto a git assente e file cancellati — review #174/#176
8828338 chore(revisore): memoria review #176 — APPROVATO
aff4ee7 chore(revisore): memoria review #174 — APPROVATO CON RISERVE
13cdb72 docs(store-docstring-escape): fine-task — report, handoff con verdetti #169/#171, diff sessione
598a2e5 fix(memoria): F-mac-2 — docstring raw in normalizza_telefono, T79a compila il motore senza escape invalidi — review #169/#171
da6e759 chore(revisore): memoria review #171 — APPROVATO
e78306d chore(revisore): memoria review #169 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-store/`) resi relativi alla radice del repo, perché il gate B li risolva.

### Review #169 — diff staged del fix

## VERDETTO: APPROVATO CON RISERVE

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10), la voce F-mac-2 in `reports/stato_progetto.md` e la coda di `.claude/agents/memoria_revisore.md`.

**Elementi del diff esaminati**

1. `modules/memory/store.py:440` — la docstring di `normalizza_telefono` diventa `r"""`.
   - **Rischio:** con il prefisso raw un escape valido (`\n`, `\t`) cambierebbe significato e quindi il testo.
   - **Verifica:** ho confrontato con `ast` la versione a HEAD e quella staged. Le docstring sono identiche e anche l'intero `ast.dump` del modulo è identico. I byte eseguibili non cambiano e i guardrail non sono toccati (`_get_window`, cap 10, fail-safe §9).
   - **Esito:** ok.

2. `tests/test_unit_kernel.py:6550` — T79a compila `gas.py`, `brains/**` e `modules/**` (16 file) con SyntaxWarning trattato come errore.
   - **Percorsi:** `Path(__file__).parent.parent` regge. Ho lanciato la suite da `/tmp` e ho ottenuto 652 PASS, 0 FAIL, con T79a PASS sui 16 file.
   - **Encoding:** `encoding="utf-8"` è esplicito e nessun file ha il BOM.
   - **Lista vuota:** il controllo `len(_sorgenti79) > 10` impedisce un PASS con zero file.
   - **Falsi positivi:** nessuno; `compile()` lavora sul sorgente e ignora i `.pyc`.
   - **Esito:** riserva R-169-1, vedi sotto.

3. `reports/stato_progetto.md:166` — la voce F-mac-2 passa a CHIUSA.
   - **Esito:** riserva cosmetica R-169-2.

**Riserve**

- **R-169-1 (MEDIA): in CI T79a non protegge da nulla.** La CI usa Python 3.11 (`.github/workflows/ci.yml:39`). Su 3.11 un escape invalido produce DeprecationWarning, non SyntaxWarning, quindi il filtro di T79a non lo intercetta. L'ho verificato compilando lo `store.py` vecchio:

  | Interprete | Filtro | Escape rilevato? |
  |---|---|---|
  | 3.11 | solo `SyntaxWarning` | no, lista vuota |
  | 3.11 | `SyntaxWarning` + `DeprecationWarning` | sì, riga 440 |
  | 3.13 | solo `SyntaxWarning` | sì, riga 453 |

  Il test resta valido in locale (3.12+) ma è verde per costruzione nel check richiesto `unit-suite`. Fix di una riga: aggiungere `_w79.simplefilter("error", DeprecationWarning)` e `DeprecationWarning` nell'`except`. Ho provato la variante sui 16 file attuali con 3.11 e 3.13: zero falsi positivi.
  - Conviene correggerla prima del commit. Il delta è una modifica successiva alla review, quindi va rimandato al revisore (lezione PR #18).

- **R-169-2 (cosmetica):** la voce F-mac-2 chiusa riporta ancora `store.py:204` e "in una regex". Il problema reale era nella docstring alle righe 440-453.

**Rischio escluso:** non ho eseguito la suite intera sotto Python 3.11 né 3.14 (la versione dell'operatore su Mac). Ho riprodotto la suite con 3.13 e il solo meccanismo di T79a con 3.11/3.13. Non ho verificato la CI reale perché il diff non è ancora pushato.

**Memoria del revisore:** ho aggiunto la riga #169 con una lezione nuova: un test-guardia sui warning del compilatore va provato con l'interprete della CI. Il commit è `e78306d`, fatto con lo script atomico che include solo la memoria. Il diff staged è intatto e non è stato committato.

File rilevanti:
- modules/memory/store.py
- tests/test_unit_kernel.py
- reports/stato_progetto.md
- .github/workflows/ci.yml
- .claude/agents/memoria_revisore.md

### Review #171 — diff staged finale

## VERDETTO: APPROVATO

Le riserve R-169-1 e R-169-2 sono chiuse e la ri-review non ne apre di nuove. Il diff staged è intatto e non l'ho committato.

**Elementi del diff esaminati**

1. `tests/test_unit_kernel.py:6552` — T79a ora tratta come errore anche DeprecationWarning, sia nel filtro sia nell'`except`.
   - **Rischio:** che T79a resti vacuo in CI (3.11), oppure che il nuovo filtro dia falsi positivi.
   - **Verifica:** ho estratto due copie del diff staged con `git checkout-index`; in una ho rimesso lo `store.py` di origin/main. Ho lanciato tutto da `/tmp`, quindi i percorsi reggono anche da una cartella esterna.

     | Interprete | Cosa ho eseguito | Codice con il fix | `store.py` di origin/main |
     |---|---|---|---|
     | 3.13 | suite intera | 652 PASS, 0 FAIL | 651 PASS, 1 FAIL (T79a, riga 453) |
     | 3.11 | solo il blocco T79a, copiato identico dal file | PASS | FAIL (riga 440) |

     Su 3.11 non ho eseguito la suite intera perché nel Python di sistema mancano le dipendenze. Il guardiano ora scatta anche sulla versione della CI, senza falsi positivi sui 16 file.
   - **Esito:** ok.

2. `reports/stato_progetto.md:166` — la voce F-mac-2 chiusa ora indica il punto vero (la docstring di `normalizza_telefono`, righe 440-453) e cita le review #169/#171.
   - **Rischio:** un'informazione sbagliata nella fotografia del progetto.
   - **Esito:** ok. La voce è un po' prolissa perché conserva il testo originale del finding, ma non è sbagliata.

3. `modules/memory/store.py:440` — la docstring `r"""` non è cambiata rispetto alla #169: l'albero `ast` del modulo resta identico prima e dopo.
   - **Esito:** ok.

**Nota cosmetica, non una riserva:** il nome del check dice ancora "senza SyntaxWarning" anche se ora filtra pure DeprecationWarning. Non ha effetto sul funzionamento.

**Rischio escluso:** non ho eseguito la suite intera sotto 3.11, solo il blocco T79a copiato identico. Il resto della suite non è toccato dal diff. Non ho verificato su Python 3.14 né sulla CI reale, perché il diff non è ancora pushato.

**Memoria del revisore:** riga #171 aggiunta, nessuna lezione nuova. Commit atomico `da6e759`, che contiene solo il file di memoria.

File rilevanti:
- tests/test_unit_kernel.py
- reports/stato_progetto.md
- modules/memory/store.py
- .claude/agents/memoria_revisore.md

### Review #174 — T79a esteso a tutti i .py (dalla verifica esterna #135)

## VERDETTO: APPROVATO CON RISERVE

L'estensione di T79a chiude V-2 e V-3 e il guardiano funziona sui 38 file. Restano due casi limite in cui la suite si interrompe del tutto invece di ripiegare. Il diff staged è intatto e non l'ho committato.

**Elementi del diff esaminati**

1. `tests/test_unit_kernel.py:6548` — T79a prende i file con `git -C <root> ls-files -z '*.py'` e torna alla vecchia lista del motore se git esce con codice diverso da 0.
   - **Rischio:** copertura incompleta, test vacuo, ripiego che non scatta.
   - **Verifica:**
     - `subprocess` è già importato a riga 9.
     - Il pattern `*.py` scende anche nelle sottocartelle: 38 file, con dentro `scripts/`, `tools/`, `clients/` e `tests/`.
     - Non ci sono symlink né submodule.
     - Suite lanciata da `/tmp` con 3.13: 652 PASS, 0 FAIL, T79a "38 file; []".
     - Sonda su un clone in una cartella temporanea, con 3.11: aggiungendo `tools/_p.py` con `x = "\d"`, T79a fallisce su 39 file, con `tools/_p.py` indicato come rotto.
     - Una copia senza `.git` fa uscire git con codice 128, quindi il ripiego scatta.
     - Se la root sta dentro un altro repo dove non è tracciata, la lista viene vuota e il controllo `len > 10` fa fallire il test: non passa a vuoto.
   - **Esito:** riserva R-174-1.

2. `tests/test_unit_kernel.py:6559` — `read_text` più `compile` su ogni file elencato da git.
   - **Rischio:** git legge l'indice, non la cartella di lavoro, quindi può elencare un file che sul disco non c'è più.
   - **Esito:** riserva R-174-2.

3. `reports/stato_progetto.md:166` — la voce F-mac-2 cita l'estensione dopo la verifica esterna #135 e la review #174.
   - **Esito:** ok.

**Riserve**

- **R-174-1 (BASSA): il ripiego non copre git assente.** Il commento dice "Senza git (copia nuda) ripiega sul motore", ma se manca proprio il programma git, `subprocess.run` solleva `FileNotFoundError` e l'intera suite si interrompe. L'ho provato con `PATH=/nonexistent`.
  - Fix: racchiudere la chiamata in `try/except OSError` e passare al ripiego.
- **R-174-2 (BASSA): un file tracciato ma cancellato fa interrompere la suite.** Se un file è stato cancellato dal disco ma non ancora tolto con `git rm` (succede a metà di un refactor), `read_text` solleva `FileNotFoundError`. La suite si ferma senza stampare il riepilogo. L'ho riprodotto cancellando `tools/*.py` nel clone.
  - Fix: saltare i file con `not _f79.is_file()`, oppure intercettare `OSError` e aggiungerli a `_rotti79`.

Entrambi i casi falliscono in modo visibile, cioè con exit diverso da 0: non sono falsi verdi. In CI non si presentano, perché il checkout ha git e la cartella di lavoro coincide con l'indice. Per questo sono riserve e non motivi di bocciatura.

**Rischio escluso:** non ho eseguito la suite intera sotto 3.11, perché nel Python di sistema mancano le dipendenze. Su 3.11 ho eseguito solo il blocco T79a, copiato identico. Il 652/0 su 3.11 lo dichiara il coordinatore e non l'ho riprodotto. Non ho verificato l'esito sulla CI reale: il comportamento di git in CI ("dubious ownership") lo deduco da actions/checkout, che imposta safe.directory, senza averlo osservato.

**Memoria del revisore:** riga #174 aggiunta, con una lezione nuova: quando un test passa da una ricerca sul filesystem a `git ls-files`, va provato con un file tracciato ma cancellato, con git assente e con una copia senza `.git`. Commit atomico `aff4ee7`, che contiene solo il file di memoria.

File rilevanti:
- tests/test_unit_kernel.py
- reports/stato_progetto.md
- .claude/agents/memoria_revisore.md

### Review #176 — ri-review R-174-1/2

## VERDETTO: APPROVATO

R-174-1 e R-174-2 sono chiuse e la ri-review non apre riserve nuove. Il diff staged è intatto e non l'ho committato.

**Elementi del diff esaminati**

1. `tests/test_unit_kernel.py:6550` — la chiamata a `git ls-files` ora sta in un `try/except OSError`. Se git manca o esce con codice diverso da 0, il test ripiega sulla lista dei file del motore.
   - **Rischio:** che senza git la suite si interrompa ancora, oppure che il ripiego controlli troppo poco e passi a vuoto.
   - **Verifica:** ho estratto il blocco T79a identico e l'ho eseguito con 3.11 su un clone in una cartella temporanea, con `PATH=/nonexistent`:
     - senza sonde: PASS su 16 file, nessuna eccezione;
     - con una sonda `modules/_p.py` contenente `"\d"`: FAIL su 17 file, quindi anche il ripiego scatta.
   - **Esito:** ok.

2. `tests/test_unit_kernel.py:6557` — dalla lista di git si tengono solo i file presenti sul disco (`is_file()`).
   - **Rischio:** che il ternario prenda una precedenza sbagliata, e che il filtro nasconda file veri.
   - **Verifica:**
     - Il ternario ha la precedenza più bassa, quindi il ramo `else` è la somma delle tre liste: corretto.
     - Il filtro si applica solo ai file elencati da git, non al ripiego.
     - Esecuzioni, sempre su 3.11 nel clone:

       | Caso | Esito |
       |---|---|
       | normale | PASS, 38 file |
       | `tools/*.py` cancellati dal disco | PASS, 37 file, nessuna eccezione |
       | sonda tracciata `tools/_p.py` | FAIL, 39 file |

     - Suite intera con 3.13, lanciata da `/tmp`: 652 PASS, 0 FAIL, "38 file; []".
   - **Esito:** ok.

**Nota cosmetica, non una riserva:** la voce F-mac-2 in `reports/stato_progetto.md:166` cita le review fino alla #174 e non la #176. È un dettaglio da aggiungere quando rifai il fine-task.

**Rischio escluso:** non ho eseguito la suite intera sotto 3.11, perché nel Python di sistema mancano le dipendenze; su 3.11 ho eseguito solo il blocco T79a, copiato identico. Non ho verificato la CI reale né Python 3.14. Il salto silenzioso di un file tracciato ma cancellato è voluto: nel checkout della CI l'indice coincide con il disco, quindi lì il filtro non toglie nulla.

**Memoria del revisore:** riga #176 aggiunta, nessuna lezione nuova. Commit atomico `8828338`, che contiene solo il file di memoria.

File rilevanti:
- tests/test_unit_kernel.py
- reports/stato_progetto.md
- .claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

`modules/memory/store.py`: solo il prefisso `r` della docstring (byte eseguibili invariati). `tests/test_unit_kernel.py`: +1 check (T79a, su tutti i 38 .py tracciati).

```
python3.11 (venv uv) tests/test_unit_kernel.py  →  === RIEPILOGO: 652 PASS, 0 FAIL ===
python3.13 tests/test_unit_kernel.py            →  === RIEPILOGO: 652 PASS, 0 FAIL ===
con lo store.py di origin/main (3.11 e 3.13)    →  === RIEPILOGO: 651 PASS, 1 FAIL ===  (T79a)
```

origin/main: 651 PASS, 0 FAIL nello stesso container.

## §6 STATO CI

Stato letto col connettore GitHub (`actions_list`, `gh` non autenticato). Mappatura commit → run:
- `e78306d`, `da6e759`, `598a2e5`: pushati insieme → run 37441631276 (CI #662) su `598a2e5`: **failure** — atteso, handoff non ancora rigenerato (handoff-check).
- `13cdb72` (primo fine-task): run 37441813169 (CI #663): **success**.
- `aff4ee7`, `8828338`, `1b57390` e il commit di questo fine-task: pushati insieme, run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Python 3.14 (Mac dell'operatore) non provato (V-4 verifica #135).
- Nessun'altra riserva aperta dalle review #169/#171/#174/#176.

## §8 VERIFICA ESTERNA #135 (verdetto integrale)

Lanciata con `Applica .claude/verifica_esterna.md a: <URL_HANDOFF di 13cdb72> <URL_PR>` (agente nuovo, Sonnet). V-2 e V-3 chiuse in `1b57390` (review #174/#176); V-1 (handoff fotografato prima dell'ultimo commit) è strutturale; V-4 resta (3.14).

VERIFICA ESTERNA PR #135 — APPROVATO CON RISERVE

**Metodo**
- Clone usa-e-getta nella scratchpad, checkout al commit 13cdb725. Il repo reale non è stato toccato: `git status` è vuoto.
- Ho rieseguito la suite con 3.13 di sistema e con un venv 3.11 appena creato da `requirements.txt` e `requirements-dev.txt`.
- Ho fatto una mutation del fix: `store.py` rimesso alla versione di main (e91ceb4).
- Ho compilato tutti i 38 `.py` tracciati con SyntaxWarning e DeprecationWarning come errori, su 3.11 e 3.13.
- Ho letto la PR e i check dall'API GitHub.

**CLAIM VERIFICATI**
- **Il modulo è invariato salvo il prefisso `r`: VERO.** `ast.dump` di `store.py` è identico tra la versione di main e quella della PR. Il diff è un solo carattere alla riga 440.
- **652 PASS / 0 FAIL con il fix su 3.11 e 3.13: VERO.** Li ho riprodotti entrambi, la 3.11 con le dipendenze reali.
- **Con lo `store.py` di main T79a fallisce: VERO su 3.13.** Dà 651 PASS e 1 FAIL, con riga 453 (`\+`). Sulla 3.11, compilando lo `store.py` di main con il filtro di T79a, l'errore è rilevato alla riga 440. Il test dichiarato "fallisce prima, passa dopo" regge su entrambe le versioni.
- **R-169-1 (T79a vacuo in CI su 3.11): CHIUSA, VERO.** Il filtro ora include DeprecationWarning, ed era quello che serviva su 3.11.
- **Nessun falso positivo: VERO.** 38 file su 38 puliti, su 3.11 e su 3.13.
- **Elenco file di §2/§3: VERO.** I quattro commit e i sette file coincidono con `git diff --stat` e `git log` dal merge-base e91ceb4. La PR dichiara +128/-327 e coincide. L'handoff dice +119/-327 ed è antecedente al commit finale (vedi V-1).
- **CI sullo SHA 13cdb725: VERO.** La run CI #663 (push) è conclusa con successo. Il check `handoff-check` è success. `unit-suite` era in corso al momento del check_runs della PR, ma la run complessiva risulta `success`. I job `smista`, `verifica` e `esito` sono skipped.
- **Il motore non cambia nei byte eseguibili: VERO.** Lo dimostra l'ast identico.

**FINDING**
- **V-1 (COSMETICA): §2 e §6 dell'handoff sono datati.**
  - §2 riporta `7 files, 119 insertions` ma include `handoff.md` a 373 righe; il diff reale dalla base è 128 insertions e `handoff.md` a 382.
  - §6 dice "run non ancora disponibile", mentre ora la run c'è ed è verde.
  - Il commit del file stesso non può comparire nel proprio log, quindi è atteso. Non cambia nessuna conclusione.
- **V-2 (BASSA): la guardia T79a copre solo `gas.py`, `brains/` e `modules/`.**
  - Restano fuori `scripts/`, `tools/`, `clients/` e `tests/`. Oggi sono puliti (probe su 38 file), ma un futuro escape invalido lì non verrebbe segnalato.
  - Anche `scripts/` fa parte del perimetro di controllo. Fix: allargare la lista a `git ls-files '*.py'`, o aggiungere `scripts/` e `tools/`.
- **V-3 (COSMETICA): il nome del check T79a dice ancora "senza SyntaxWarning"** ma filtra anche DeprecationWarning. Era già annotato dal revisore #171.
- **V-4 (BASSA): la copertura è per versione di Python.**
  - Sulla 3.14 dell'operatore il test non è stato eseguito da nessuno; l'handoff lo dichiara `SALTATA`.
  - Su 3.11 un escape invalido emette solo DeprecationWarning, quindi il test dipende dal fatto che quel filtro resti attivo. Non l'ho provato su 3.14.

**NON VERIFICATO**
- **I check REQUIRED del ruleset `main-lock`.** Non ho letto il ruleset (non ho usato l'endpoint dei ruleset). Dalle check run vedo `unit-suite` e `handoff-check`, coerenti con CLAUDE.md §10, ma l'elenco dei required resta una dichiarazione del progetto.
- **Python 3.14**, non disponibile qui.
- **La coerenza completa di `reports/*`** (ultimo_report, stato_progetto, diff_sessione) con il diff reale: ho controllato solo handoff §2, §3, §5 e §6. Non ho riletto il testo della voce F-mac-2 in `stato_progetto.md:166`.
- **Autenticità dei verdetti del revisore #169/#171.** Ho riprodotto i loro numeri (3.11 e 3.13), non il loro processo.
- **Il vincolo "agente diverso dal proprio".** Non verificabile da qui; il commit risulta co-firmato Claude Opus 5.5 e io sono Sonnet 5.5.

**RACCOMANDAZIONE**
Si può mergiare. Il fix è a rischio nullo e la guardia funziona davvero su 3.11 e 3.13. Prima di altro lavoro:
1. Allargare T79a a tutti i `.py` tracciati (V-2).
2. Rinominare il check (V-3).
3. Aggiornare §2 e §6 dell'handoff in fase di merge (V-1).

Il punto 1 tocca il perimetro di review (`tests/`), quindi deve passare dal revisore.
