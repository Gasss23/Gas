# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-04 — V-A: handoff-check davvero vincolante, branch `fix/handoff-check-vincolante`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #120 (https://github.com/Gasss23/Gas/pull/120), dopo la verifica esterna. Variante A: l'agente lancia `gasmerge 120`, l'operatore conferma digitando `120`.

---

## §1 SCOPE & ESITO FETTE

- **V-A — handoff-check required ma saltabile (verifica esterna PR #119, ALTA)**: `FATTA`.
- **R-141-1 — git diff fallito → insieme vuoto → "non applicabile"**: `FATTA`.
- **Correzione V-3 nei report** (era "CHIUSA", in realtà MITIGATA): `FATTA`.
- **Cosmetica #140 — commento duplicato nell'hook**: `FATTA`.
- **V-B / V-C / V-D (verifica esterna PR #119)**: `DEFERITA — tracciate in stato_progetto`.
- **Docstring check_handoff (cosmetica #142)**: `DEFERITA — riserva cosmetica`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +
 .claude/hooks/review_gate.sh       |   2 -
 reports/diff_sessione.md           |  21 +--
 reports/handoff.md                 | 350 ++++++++++++++-----------------------
 reports/stato_progetto.md          |   6 +-
 reports/ultimo_report.md           |  32 ++--
 scripts/check_handoff.py           |  40 ++++-
 scripts/check_verdetto.py          |  48 +++--
 tests/test_unit_handoff_check.py   |  66 +++++++
 9 files changed, 284 insertions(+), 284 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
501ab76 fix(handoff-check): vincolante quando la sessione tocca il perimetro (V-A) — review #141/#142 APPROVATO CON RISERVE
7649d6b chore(revisore): memoria review #142 — APPROVATO CON RISERVE
c7b6139 chore(revisore): memoria review #141 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `501ab76`: la #141 sul diff e la #142 sul delta che chiude R-141-1. Entrambe sono incollate per intero.

### Review 141

## VERDETTO: APPROVATO CON RISERVE

**Review #141**: branch `fix/handoff-check-vincolante`, diff staged di 4 file. Ho fatto le tre letture obbligatorie: CLAUDE.md, `reports/stato_progetto.md` e `.claude/agents/memoria_revisore.md`.

### Elementi del diff esaminati
- `scripts/check_handoff.py:103` — se il merge-base fallisce lo script esce con 1 (prima usciva con 0). Rischio esaminato: che il post-merge su main diventi rosso. Esito: **ok**. Sonde S1, S1b e S2, descritte sotto.
- `scripts/check_handoff.py:116` — se la sessione tocca il perimetro e l'handoff non è nel diff, esce con 1. Il perimetro unisce file, voci cablate e versione alla base. Esito: **ok**. Il test `test_va_perimeter_session_without_handoff_fails_both` fallisce con gli script di main. Sonda S6: un rename di `gas.py` fuori dal perimetro, senza handoff, dà 1/1, perché `--no-renames` conta anche il path di origine.
- `scripts/check_handoff.py:20` — importa `_carica_perimetro`, `_nel_perimetro` e `_session_files` da check_verdetto. Rischio (c): shadowing, import rotto, bytecode stantio. Esito: **ok**.
  - Gli import della libreria standard sono già in cache prima di `sys.path.insert`.
  - `scripts/` non contiene moduli con nomi della libreria standard.
  - Un ImportError produce un traceback con rc=1, quindi fail-closed.
  - `scripts/__pycache__/` è ignorato da `.gitignore:3`.
  - python3 di sistema è la 3.14, compatibile con `str | None`.
  - Il legame con funzioni private (`_`) è fragile ma visibile: un rinomina rompe l'import in modo rumoroso.
- `scripts/check_verdetto.py:218` — l'ordine è invertito: base, sessione e perimetro vengono prima dei controlli sull'handoff; merge-base fallito dà 1. Esito: **ok**.
- `scripts/check_verdetto.py:235` — `_manca()` dà 1 con il perimetro toccato in tre casi: handoff non nel diff, file inesistente, §4 non trovata. Esito: **ok**.
  - Sonda S4 (handoff cancellato): 1/1.
  - Sonda S5 (§4 col titolo giusto ma vuota): 1, per «0 citazioni».
  - Il ramo "non esiste" di check_verdetto non ha un test proprio, ma nello stesso job lo copre già check_handoff (rc=1).
- `scripts/check_handoff.py:56` + `scripts/check_verdetto.py:89` (`_diff_names`, `_session_files`) — se `git diff BASE..HEAD` fallisce, restituiscono `set()`. Esito: **riserva R-141-1**, dettagli sotto.
- `.claude/hooks/review_gate.sh:111` — tolto solo il commento duplicato. La spiegazione di PIPESTATUS resta a riga 108 e il codice è invariato. Esito: **ok**: la suite hook passa.
- `tests/test_unit_handoff_check.py:598`–`:634` — 4 test V-A nuovi. Esito: **ok**.
  - Controprova riprodotta con gli script di main copiati nello scratchpad e `-k test_va`: 3 failed, 2 passed. I tre che falliscono sono perimetro senza handoff, §4 rinominata e merge-base.
  - Il test doc-only tiene il caso inverso (un fail-closed indiscriminato verrebbe preso).

### Misure riprodotte
- `pytest tests/ --ignore=tests/test_unit_kernel.py`: **270 passed**.
- `test_unit_handoff_check.py`: 35 passed.

### Risposte alle domande
**(a) CI.** Il workflow ha solo `on: push`.

Post-merge su main, ho simulato due casi:
- **S1**, HEAD detached sulla punta di origin/main dopo un merge che tocca `gas.py`: base = HEAD, risultato **0/0**.
- **S1b**, branch locale `main`: **0/0** già dalla guardia "HEAD su main".

Quindi il post-merge non diventa rosso in nessuno dei due modi in cui actions/checkout può lasciare il repo. **S2**, la race in cui origin/main va avanti tra il push e il `git fetch origin main`: HEAD è antenato, base = HEAD, risultato **0/0**.

Push intermedio prima del fine-task: diventa rosso. **È accettabile, anzi corretto**: il check required si valuta sullo SHA di testa della PR, e il rosso intermedio dice il vero, cioè che il fine-task manca. I commit di scrivi-rep successivi restano verdi: l'handoff resta nel diff cumulativo e `ultima_risposta.md` è in ALLOWLIST.

**(b) Altri percorsi verso "non applicabile" con il perimetro toccato.**
- **R-141-1 (minore)**: con un `git diff BASE..HEAD` fallito, entrambi gli helper restituiscono `set()`.
  - Sonda S3, base override di 40 caratteri esadecimali ma inesistente: **0/0**. check_handoff stampa «diff vuoto», check_verdetto «non applicabile».
  - Controllo con la base corretta: 1/1.
  - Oggi in CI non ci si arriva, perché non si passa un override e il merge-base fallisce prima. È però lo stesso schema fail-open che V-A chiude un passo sopra.
  - Correzione: gli helper restituiscono `None` sull'errore e `main` esce con 1.
- **Guardia `branch == "main"`**: in CI scatta solo sul push a main, che `main-lock` impedisce se non tramite merge. Non sfruttabile.
- Il resto (§4 vuota, cancellata o rinominata, rename) chiude con 1, come da sonde.

**(c) Import tra script.** Come sopra: nessun rischio bloccante. Un ImportError fa uscire lo script con rc=1, quindi blocca invece di lasciar passare. Il messaggio di STOP di `fine_task_finale.sh:48` («Correggi §2») in quel caso sarebbe fuorviante, ma è cosmetico.

### Riserve (da tracciare in stato_progetto.md)
- **R-141-1 (minore)**: fail-open quando `git diff` fallisce, descritto sopra.
- **R-141-2 (strutturale, già implicita)**: la CI esegue la versione **della PR** di `check_*.py` e di `ci.yml`. Una PR che modifica questi file può neutralizzare `handoff-check` mantenendone il nome. Le barriere sono il gate locale (i file sono nel perimetro) e la verifica esterna, non la CI.
- **Docstring (cosmetica)**: `scripts/check_handoff.py:5-11` lega "§2 mancante / file mancante" al perimetro, ma sono errori anche fuori perimetro (comportamento già presente prima). Inoltre ora "perimetro assente" dà 1 anche nelle sessioni doc-only con diff non vuoto, e non è documentato.

### Rischio escluso
- **Comportamento reale di actions/checkout v4 sul runner**: non verificato. Non ho consultato i log delle run GitHub. Ho simulato in locale entrambe le forme possibili, detached e branch `main`, ed entrambe danno 0.
- **Suite kernel `test_unit_kernel.py`**: non eseguita, perché il diff non tocca il motore runtime.

### Memoria
- Riga contatore #141 e una lezione nuova aggiunte in `/Users/gas/Gas/.claude/agents/memoria_revisore.md`. La lezione: dopo un fail-closed, seguire gli helper che su errore restituiscono un insieme vuoto.
- File salvato da solo con `scripts/commit_memoria_revisore.sh`: commit `c7b6139`. L'index della review è rimasto intatto (4 file staged).

File rilevanti:
- /Users/gas/Gas/scripts/check_handoff.py
- /Users/gas/Gas/scripts/check_verdetto.py
- /Users/gas/Gas/tests/test_unit_handoff_check.py
- /Users/gas/Gas/.claude/hooks/review_gate.sh
- /Users/gas/Gas/.github/workflows/ci.yml
- Sonde: /private/tmp/claude-501/-Users-gas-Gas/ae22c9c4-87ee-4a13-a7c3-81c489eb3034/scratchpad/sonde141.py

### Review 142

## VERDETTO: APPROVATO CON RISERVE

**Review #142**: delta sulla #141. Il fix chiude R-141-1: un `git diff` fallito ora dà exit 1 in entrambi gli script. Le riserve rimaste sono cosmetiche più R-141-2, che è strutturale. Diff staged di 4 file, l'index è rimasto intatto dopo il salvataggio della memoria. Letture obbligatorie già fatte nella #141.

### Elementi del diff esaminati
- `scripts/check_verdetto.py:89` — `_session_files` restituisce `None` se `git diff` fallisce, invece di un `set()`. Rischio: altri chiamanti che si aspettano un set. Esito: **ok**.
  - Chiamanti: `scripts/check_verdetto.py:226`, `scripts/check_handoff.py:112` e il test a riga 579, che usa un diff valido.
  - Nessun chiamante itera su `None`.
- `scripts/check_verdetto.py:226` — se `session is None`, esce con 1 e stampa "git diff BASE..HEAD fallito". Esito: **ok**.
  - Sonda S3, base inesistente di 40 caratteri esadecimali con perimetro toccato: ora **1/1** con "fallito" (nella #141 era 0/0).
  - Controllo con la base corretta: 1/1 (V-A).
- `scripts/check_handoff.py:111` — calcola `all_changed` e `session`; se uno dei due è `None`, esce con 1. `nel_perimetro` riusa `session` senza una seconda chiamata. Esito: **ok**, con una nota sulla mutation B più sotto.
- `tests/test_unit_handoff_check.py:637` — `test_r141_1_git_diff_failure_fails_closed`, che verifica rc 1 e "fallito" in stderr per entrambi gli script. Esito: **ok**.
  - **Mutation A** (`_session_files` torna a `set()`): il test fallisce, quindi è mordace.
  - **Mutation B** (solo `_diff_names` torna a `set()`): sopravvive. Quel controllo è ridondante, non portante: i due `git diff` usano lo stesso intervallo `BASE..HEAD` e falliscono insieme. Non è un difetto.
- `scripts/check_handoff.py:7` — docstring. Esito: **riserva cosmetica**.
  - Mette "perimetro assente o vuoto" tra gli exit 1 "SEMPRE (qualunque sessione)". Ma con un diff vuoto lo script esce con 0 a riga 119, prima di caricare il perimetro.
  - La riga 12 "Exit 1: set incoerente…" ripete quanto già detto a riga 8.

### Misure riprodotte
- `pytest tests/ --ignore=tests/test_unit_kernel.py`: **271 passed**.
- Sonde post-merge rilanciate sul codice nuovo, nessuna regressione:
  - S1, HEAD detached sulla punta di main: 0/0.
  - S1b, branch `main`: 0/0.
  - S2, race con origin/main più avanti: 0/0.

### Riserve (da tracciare in stato_progetto.md)
- **Docstring** di `check_handoff.py:7-12`: imprecisione sul perimetro assente e riga duplicata. Cosmetica.
- **R-141-2**, strutturale, resta aperta: la CI esegue la versione della PR di `check_*.py` e di `ci.yml`. Le barriere sono il gate locale e la verifica esterna.

### Rischio escluso
- **Comportamento reale di actions/checkout v4 sul runner GitHub**: non verificato dai log delle run. Ho simulato in locale entrambe le forme possibili (HEAD detached e branch `main`), ed entrambe danno 0.
- **Suite kernel**: non eseguita, perché il delta non tocca il motore runtime.

### Memoria
- Riga contatore **#142** aggiunta in `/Users/gas/Gas/.claude/agents/memoria_revisore.md`. Nessuna lezione nuova: quella sui passi che su errore "degradano a vuoto" è già stata scritta nella #141.
- File salvato da solo con `scripts/commit_memoria_revisore.sh`: commit **`7649d6b`**. Il salvataggio della #141 era `c7b6139`.

File rilevanti:
- /Users/gas/Gas/scripts/check_handoff.py
- /Users/gas/Gas/scripts/check_verdetto.py
- /Users/gas/Gas/tests/test_unit_handoff_check.py
- /Users/gas/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py, brains/ o modules/: la suite kernel non è stata rilanciata. Test in tests/ (gate): `pytest tests --ignore=tests/test_unit_kernel.py` **266 → 271 passed**, tutti verdi.

## §6 STATO CI

```
completed	failure	fix(handoff-check): vincolante quando la sessione tocca il perimetro …	CI	fix/handoff-check-vincolante	push	37202038518	1m11s	2026-10-04T12:25:18Z
completed	success	Merge pull request #119 from Gasss23/fix/gate-autoprotezione	CI	main	push	37201274295	1m11s	2026-10-04T12:11:50Z
completed	success	docs(gate-auto): fine-task — il gate protegge se stesso + verifica es…	CI	fix/gate-autoprotezione	push	37159096561	1m2s	2026-10-03T22:37:56Z
```

Mappatura commit→run:
- `501ab76` (codice V-A, pushato prima del fine-task): run **37202038518**. Esito `unit-suite: success`, `handoff-check: failure`. Il rosso è ATTESO: il push conteneva il codice nel perimetro ma non ancora l'handoff, e questa è la prova dal vivo di V-A.
- `c7b6139`, `7649d6b` (memoria revisore): nessuna run su questi SHA. Sono commit intermedi dello stesso push, inclusi nell'albero testato da 37202038518.
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff. Deve tornare verde su entrambi i check.

## §7 RISERVE APERTE

- **R-141-2** (strutturale): la CI esegue la versione della PR dei check, quindi una PR può neutralizzarli. Barriere: il gate locale (i file sono nel perimetro) e la verifica esterna.
- **V-B** (MEDIA): il gate B prova le citazioni, non che la review sia avvenuta.
- **V-C** (MEDIA): l'hook non intercetta merge, cherry-pick e alias.
- **V-D / R-138-5**: perimetro più largo (gas_identity.md).
- **R-139-1**: formati alternativi del verdetto (mitigata).
- Cosmetica: docstring di check_handoff (#142).
- Da C4b-3: R-c4b3-3, R-c4b3-4, **R-c4b3-5** (prossima fetta motore).
