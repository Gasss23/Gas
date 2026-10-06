# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-06 — F-mac-3: pytest senza target raccoglie l'intero repo (sessione cloud)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #139 (https://github.com/Gasss23/Gas/pull/139). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4762287334","url":"https://github.com/Gasss23/Gas/pull/139"}`): `gh` non è autenticato in questo container.

---

## §1 SCOPE & ESITO FETTE

- **F-mac-3**: `FATTA`.
- **Prova su macOS/Windows**: `SALTATA — nessun Mac/Windows nel container`.
- **Verifica esterna §4quater**: `SALTATA — solo configurazione della collection di pytest e un test; nessun cambiamento al motore né ai gate (dosaggio: decide l'operatore se lanciarla)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 clients/voice/probe/conftest.py    |   6 ++++++
 reports/diff_sessione.md           |  17 ++++++-----------
 reports/handoff.md                 | 332 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  16 ++++++----------
 tests/conftest.py                  |   6 ++++++
 tests/test_unit_voice_server.py    |  20 ++++++++++++++++++++
 8 files changed, 145 insertions(+), 257 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
bb81ae8 docs(f-mac-3): fine-task — report, handoff con verdetti #190/#191, diff sessione
5f5a22a fix(test): F-mac-3 — pytest senza target raccoglie l'intero repo (probe Windows e script del kernel esclusi) — review #190/#191
5d34e91 chore(revisore): memoria review #191 — APPROVATO CON RISERVE
89f0e58 chore(revisore): memoria review #190 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetto INTEGRALE del diff committato. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-mic/`) resi relativi alla radice del repo. La review #190 (BOCCIATO) riguarda una versione precedente, MAI committata (modifica a `win_mic_test.py`, poi tolta): è riportata integrale in §8, fuori da §4 perché cita file che non sono nel diff.

### Review #191 — diff committato (`5f5a22a`)

## VERDETTO: APPROVATO CON RISERVE

Questa è la ri-review #191 del nuovo diff staged in /home/user/wt-mic. R-190-1 e R-190-2 sono chiuse: `pytest` lanciato senza target ora raccoglie l'intero repo con exit code 0. `win_mic_test.py` è identico a HEAD (`git diff HEAD` vuoto).

### Elementi del diff esaminati
- **`clients/voice/probe/conftest.py:6`** — `collect_ignore_glob = ["win_*_test.py"]` toglie dalla collection i 4 probe manuali Windows.
  - Rischio esaminato: che il glob lasci fuori un probe o escluda un test vero. In `git ls-files` gli unici `*_test.py`/`test_*.py` fuori da `tests/` sono i 4 `win_*_test.py`, quindi il glob li copre tutti e non tocca altro.
  - Mutation: tolto questo conftest, il test strutturale fallisce (riprodotto).
  - Esito: **ok**.
- **`tests/conftest.py:6`** — `collect_ignore = ["test_unit_kernel.py"]`.
  - Rischio esaminato: che si perda la suite del kernel in CI. La CI (`ci.yml:97`) la lancia come script con `python tests/test_unit_kernel.py`, che non legge i conftest; gli altri passi passano i file per nome.
  - Mutation: senza questo conftest la collection importa il file, esegue tutta la suite del kernel (17 s) e il test strutturale fallisce (riprodotto).
  - Esito: **ok**.
- **`tests/test_unit_voice_server.py:357-370`** — lancia in subprocess `python -m pytest --collect-only -q -p no:cacheprovider` dalla radice e accetta solo exit code 0 o 5.
  - Rischi esaminati:
    - Ricorsione: con `--collect-only` nessun test viene eseguito, quindi non c'è.
    - Effetti collaterali: `git status` è invariato dopo la collection e `cacheprovider` è disattivato.
    - Dipendenze mancanti in CI: `test_unit_voice_stt.py`, `test_unit_voice_tts.py` e `modules/voice/stt.py`/`tts.py` importano a livello di modulo solo la stdlib e `modules.voice`, che sono già coperti.
    - Durata: circa 0,5 s, con timeout a 300 s.
  - Conta l'exit code, non l'ultima riga dell'output: è la lezione di #190.
  - `test_unit_voice_server.py`: 20 passed (pytest 9.1.1, la stessa versione pinnata in `requirements-dev.txt`).
  - Esito: **ok** (vedi R-191-1).
- **`reports/stato_progetto.md:171`** — la chiusura di F-mac-3 ora corrisponde ai fatti che ho riprodotto: collection intera con exit code 0. Esito: **ok**.

Wall of Shame: nessun file del kernel o dei provider toccato, nessuno slicing della history, nessuna simulazione di tool.

### Riserve
- **R-191-1 (cosmetica):** il test sulla collection dell'intero repo sta in `test_unit_voice_server.py`. Si capisce la scelta, perché è un file che la CI esegue, ma nome e posizione ingannano. Meglio spostarlo in un file dedicato più avanti, ricordandosi di aggiungerlo a `ci.yml`.

### Rischio escluso
Non ho rieseguito le cifre complete date nel messaggio: i 612 passed della suite CI con `GAS_TEST_LOCALE_UTF8_ATTESO=1` e i 653 PASS di `python tests/test_unit_kernel.py`. Il diff non tocca codice del motore e lo script del kernel non legge i conftest. Ho riverificato solo `test_unit_voice_server.py` (20 passed), la collection intera (exit code 0) e le due mutation. Non ho verificato la collection su Windows o macOS.

La memoria ha la riga #191, committata da sola con `scripts/commit_memoria_revisore.sh` (5d34e91). Il diff staged è intatto e non l'ho committato.

File rilevanti:
- clients/voice/probe/conftest.py
- tests/conftest.py
- tests/test_unit_voice_server.py
- reports/stato_progetto.md
- .claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules.

```
python -m pytest --collect-only -q (radice)  → rc 0, 663 tests collected   (prima: rc 3, INTERNALERROR)
GAS_TEST_LOCALE_UTF8_ATTESO=1 pytest (6 file CI) → 612 passed
python tests/test_unit_kernel.py              → === RIEPILOGO: 653 PASS, 0 FAIL ===
```

## §6 STATO CI

`gh` non autenticato (CI NON VERIFICATA con la CLI). Mappatura commit → run:
- `89f0e58`, `5d34e91`, `5f5a22a`: pushati insieme, run CI sul push di `5f5a22a` — esito non letto alla scrittura dell'handoff (atteso handoff-check rosso, prima del fine-task).
- commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-191-1** (cosmetica): il test strutturale sta in `test_unit_voice_server.py`; spostarlo in un file dedicato (e aggiungerlo a ci.yml) più avanti.
- Collection non verificata su macOS/Windows.

## §8 REVIEW #190 (BOCCIATO) — versione mai committata, verdetto integrale

Diff valutato: lazy import in `clients/voice/probe/win_mic_test.py` + un test. Bocciato perché altri 3 probe e lo script del kernel rompevano comunque la collection; sostituito dalla soluzione con i conftest (review #191).

## VERDETTO: BOCCIATO

**Letture preliminari fatte:** CLAUDE.md (sez. 5, 8, 9 e 10), la voce F-mac-3 in `reports/stato_progetto.md:171`, la coda di `.claude/agents/memoria_revisore.md` (fino alla #189).

**Motivo del blocco (R-190-1).** La modifica a `win_mic_test.py` è corretta, ma `stato_progetto.md` dichiara F-mac-3 chiusa e non lo è. Il finding dice che `pytest` lanciato senza target si rompe durante la collection. Nel worktree, con il diff staged applicato:
- `python -m pytest --collect-only -q` sull'intero repo esce con **rc=3** (INTERNALERROR).
- `python -m pytest --collect-only clients/` esce anch'esso con rc=3: `INTERNALERROR> File ".../clients/voice/probe/win_playback_test.py", line 25 ... SystemExit: 1`.

La riga "no tests collected" che il brief cita come prova compare **dopo** "mainloop: caught unexpected SystemExit!". È l'ultima riga di un run fallito, non un esito pulito: conta l'exit code, non la coda dell'output.

`git ls-files` trova quattro file `*_test.py` fuori da `tests/`, tutti in `clients/voice/probe/`:

| File | Problema | rc della sola collection |
|---|---|---|
| `win_playback_test.py:19-25` | `sys.exit(1)` all'import (sounddevice) | 3 |
| `win_wakeword_test.py:26-37` | due `sys.exit(1)` all'import (sounddevice, openwakeword) | 3 |
| `win_bridge_test.py:25-29` | `sys.exit(1)` all'import se manca requests | 5 qui (requests installato), latente altrove |
| `win_mic_test.py` | sistemato da questo diff | 5 |

### Elementi del diff esaminati
- `clients/voice/probe/win_mic_test.py:22-35` — `sd`/`wav_write` valgono None a livello di modulo; `_carica_dipendenze()` li assegna con `global` e stesso messaggio + `sys.exit(1)`. Rischio guardato: nome globale non riassegnato, cioè NameError o chiamata su None in `list_devices`/`main`. L'assegnazione avviene dopo il try riuscito, e `sd` (righe 43, 67-81) e `wav_write` (riga 84) si usano solo dopo la chiamata. Esito: **ok**.
- `clients/voice/probe/win_mic_test.py:63` — `_carica_dipendenze()` chiamata subito dopo `parse_args()`. Rischio guardato: cambia il comportamento da riga di comando. `--help` ora funziona anche senza dipendenze (miglioramento innocuo); senza dipendenze esce con lo stesso messaggio ed exit 1, riprodotto. Esito: **ok**. Nota cosmetica: manca una riga vuota prima di `DURATION` (riga 37, PEP 8 vuole 2 righe).
- `tests/test_unit_voice_server.py:357-366` — carica il modulo via `importlib` con un nome isolato e verifica che non esca. Rischio guardato: test che passa anche senza il fix. Ho caricato la versione HEAD del file dallo scratchpad e ottengo `SystemExit 1`, quindi la mutation viene uccisa; 20 passed. La CI (`ci.yml:52-53,109`) non installa sounddevice né scipy, quindi lì il test ha senso. Esito: **ok**, con il limite R-190-2.
- `reports/stato_progetto.md:171` — F-mac-3 segnata come CHIUSA. Rischio guardato: chiusura dichiarata ma non provata. Esito: **blocco** (R-190-1).

### Riserve
- **R-190-1 (bloccante):** F-mac-3 non è chiusa. Ci sono due strade:
  - (a) applicare lo stesso pattern di caricamento lazy a `win_playback_test.py`, `win_wakeword_test.py` e `win_bridge_test.py`;
  - (b) preferibile, perché ferma la classe di errore e non il singolo caso: un `clients/voice/probe/conftest.py` con `collect_ignore_glob = ["win_*_test.py"]`, oppure `python_files = test_*.py` nella configurazione pytest alla radice. Sono probe manuali, non test.

  In alternativa si declassa la voce a "parziale" senza CHIUSA.
- **R-190-2:** il test nuovo protegge solo `win_mic_test.py`. Serve un test strutturale che lanci `python -m pytest --collect-only -q` sul repo via subprocess e richieda rc in {0, 5}. Ogni nuovo `*_test.py` con exit all'import verrebbe preso.
- **R-190-3 (cosmetica):** riga 37, 2 righe vuote prima delle costanti.

Wall of Shame: il diff non tocca la history, `_get_window`, il cap a 10 iterazioni né i provider. Nessuno slicing e nessuna simulazione di tool.

### Rischio escluso
Non ho verificato lo script su Windows con sounddevice e scipy installati (registrazione reale): l'hardware audio non è riproducibile in dev. Dal codice letto il percorso felice è invariato, ma non l'ho eseguito.

Memoria aggiornata con la riga #190 e una lezione (verificare tutti i file che combaciano col pattern; leggere l'exit code di pytest, non l'ultima riga). Committata da sola con `scripts/commit_memoria_revisore.sh` (89f0e58). Il diff staged è intatto e non l'ho committato.

File rilevanti:
- clients/voice/probe/win_mic_test.py
- clients/voice/probe/win_playback_test.py
- clients/voice/probe/win_wakeword_test.py
- clients/voice/probe/win_bridge_test.py
- tests/test_unit_voice_server.py
- reports/stato_progetto.md
- .claude/agents/memoria_revisore.md
