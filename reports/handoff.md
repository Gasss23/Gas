# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-02 — Fix IP-gate: sblocco branch chore/hook-fine-task-obbligatorio per gasmerge

---

## §0 DECISIONI UMANE RICHIESTE

_[da completare dopo il push — vedi procedura §0 GATE PR]_

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — `memoria_revisore.md:179`: sostituzione IP con `<IP-fittizio>`**: FATTA  
  Sostituito IP fittizio alla riga #122. Nient'altro toccato nel file.

- **Fetta 2 — `test_unit_hooks.py:1696`: aggiunta `# gasmerge-ip-ok`**: FATTA  
  Token aggiunto come commento Python fuori dalla stringa. Comportamento del test invariato.

- **Fetta 3 — `fine_task_finale.sh` Gate IP allineato a `gasmerge.sh`**: FATTA  
  Full-tree (HEAD), regex word-boundary identica, loopback-first via sed per-riga, allowlist gasmerge-ip-ok.

- **Fetta 4 — Test aggiornati**: FATTA  
  T-finale-4 assertion aggiornata; T-finale-4b e T-finale-4c aggiunti. Suite: 51/51 PASS.

- **Fetta 5 — Simulazione invariante gasmerge**: FATTA  
  Zero blocchi sull'albero di lavoro con logica gasmerge completa (printf-based, no echo).

- **Fetta 6 — Revisore Opus #124**: FATTA  
  APPROVATO CON RISERVE. R-finale-1 (media): set -e attivo dopo gate IP. R-finale-2 (bassa/nota): allowlist per riga condivisa con gasmerge.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 +
 .claude/commands/fine-task.md      |  62 ++---
 .claude/hooks/promemoria_end.sh    |  61 ++++-
 CLAUDE.md                          |   2 +-
 reports/diff_sessione.md           |  47 ++--
 reports/handoff.md                 | 194 +++++++---------
 reports/stato_progetto.md          |   4 +-
 reports/ultimo_report.md           | 111 ++-------
 scripts/fine_task_finale.sh        | 141 +++++++++++
 tests/test_unit_hooks.py           | 465 ++++++++++++++++++++++++++++++++++++-
 10 files changed, 835 insertions(+), 258 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
fa78fb5 fix(ip-gate): allinea fine_task_finale.sh a gasmerge.sh (full-tree, token, fix fixture)
ade4c1a chore(revisore): memoria review #124 — APPROVATO CON RISERVE
0accbb7 docs(hook-fine-task-obbligatorio): aggiorna §6 handoff con esito CI (SUCCESS)
0bb3743 docs(hook-fine-task-obbligatorio): fix §4 handoff — citazioni file:line corrette
bfb8dee docs(hook-fine-task-obbligatorio): report fine-task + handoff + diff_sessione
9863352 chore(hook-fine-task): script deterministico + contatore per sessione + test
ac51ccf chore(revisore): memoria review #123 — APPROVATO
c644990 chore(revisore): memoria review #122 — BOCCIATO
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

**Review #124 — 2026-10-02 — APPROVATO CON RISERVE**

Diff tocca `tests/test_unit_hooks.py` e `scripts/fine_task_finale.sh`: gate revisore applicato.

> ### REVIEW #124 — branch chore/hook-fine-task-obbligatorio — APPROVATO CON RISERVE
>
> Ho fatto le letture obbligatorie (CLAUDE.md §5/§9, reports/stato_progetto.md, .claude/agents/memoria_revisore.md fino a #123). Il diff non tocca gas.py, brains/ o modules/: non c'è slicing della history, non c'è simulazione di tool e i guardrail runtime (cap 10 iterazioni, `_get_window`) restano intatti.
>
> **Elementi del diff esaminati**
>
> 1. **`scripts/fine_task_finale.sh:67`** — `git grep -nE` sull'albero `HEAD`.
>    - Rischio esaminato: regex diversa da gasmerge.sh:91, oppure ambito ristretto.
>    - Esito: **ok**. La regex è identica byte per byte a quella di gasmerge.sh (riga 91). L'ambito è tutto l'albero: cambia solo il ref (`HEAD` invece di `origin/$BRANCH`), ed è corretto perché il gate gira prima del push. Ho simulato il gate sull'albero staged reale (`git write-tree`): il residuo è vuoto, quindi non blocca la sessione corrente.
>
> 2. **`scripts/fine_task_finale.sh:77-84`** — filtro loopback riga per riga via `sed`.
>    - Rischio esaminato: una riga con sia loopback sia un IP non-loopback che passa il filtro.
>    - Esito: **ok**. La logica è identica a gasmerge.sh (righe 97-110) (si tolgono i 127.x e si ri-testa il residuo). L'ordine è lo stesso di gasmerge: prima il loopback, poi l'allowlist.
>
> 3. **`scripts/fine_task_finale.sh:93-110`** — gestione dei codici di ritorno: rc 1 → OK, rc 0 → STOP, rc diverso da 0/1 → STOP.
>    - Rischio esaminato: fail-open su errore di `git grep` o di `grep -v`.
>    - Esito: **ok**. Tutti i rami non attesi finiscono in `exit 1`.
>
> 4. **`scripts/fine_task_finale.sh:69,84,92`** — `set -e` dopo ogni `set +e`.
>    - Rischio esaminato: lo script nasce con solo `set -uo pipefail` (riga 17), quindi questo toggle attiva errexit per tutto il resto dello script.
>    - Esito: **riserva R1**. L'ho riprodotto con un remoto bare in sola scrittura negata: `git push` (riga 115) fallisce e lo script esce subito, senza mai stampare il messaggio "ERRORE git push fallito" delle righe 117-119. Il codice di uscita è quello di git (qui 1, in altri casi può essere 128), non quello normalizzato. Non è un fail-open, perché si esce comunque con codice diverso da zero senza URL. Però contraddice il contratto della riga 15 ("exit 1 + messaggio chiaro"), e le righe 116-120 diventano codice morto.
>
> 5. **`scripts/fine_task_finale.sh:90`** — allowlist con `grep -v 'gasmerge-ip-ok'` sulla riga intera.
>    - Rischio esaminato: è proprio la lezione di #122 (l'allowlist per riga lascia passare altri IP sulla stessa riga).
>    - Esito: **riserva R2**. È una regressione voluta rispetto al R1 di #122, che filtrava IP per IP. È giustificata: ora il gate guarda tutto l'albero, e deve accettare gli stessi token che accetta gasmerge (per esempio test_unit_kernel.py:4946), altrimenti bloccherebbe righe che il merge consente. Il limite è condiviso con gasmerge, quindi non aggiunge superficie. Va però tracciato.
>
> 6. **`tests/test_unit_hooks.py:1696` e `1706`** — T-finale-4: token come commento Python, assertion portata a "IP trovato".
>    - Rischio esaminato: l'assertion potrebbe essere soddisfatta da messaggi che non riguardano un blocco IP.
>    - Esito: **ok**. Il token `# gasmerge-ip-ok` sta fuori dalla stringa, quindi non finisce nell'handoff di test, che resta bloccato. La sottostringa "IP trovato" compare solo nella riga STOP (riga 96): "0 IP trovati" non la contiene (finisce in "i", non in "o"). Insieme al controllo `returncode == 1`, l'assertion discrimina.
>
> 7. **`tests/test_unit_hooks.py:1727`** — T-finale-4b: la fixture con l'IP sta in `scripts/test_ip.sh` del repo temporaneo, il token sta sulla riga sorgente Python.
>    - Esito: **ok**. Nel file del repo di test l'IP compare senza token. Nel repo reale gasmerge vede il token sulla riga Python.
>    - Mutation test: con l'ambito ristretto a `reports/`, T-4b fallisce, quindi il test morde.
>
> 8. **`tests/test_unit_hooks.py:1739-1773`** — T-finale-4c: IP con token, exit 0 atteso.
>    - Esito: **ok**. Lo stderr mostra Gate A e Gate B "non applicabile", poi il Gate IP. Il push è un no-op perché l'upstream è già impostato (riga 1760). HEAD coincide con `@{u}`. L'handoff non è nel diff, quindi esce con "URL_HANDOFF: non disponibile" ed exit 0.
>    - Mutation test: rimuovendo l'allowlist, T-4c fallisce.
>    - Nota: il revisore cita anche il token `# gasmerge-ip-ok` su test_unit_kernel.py (riga 4946) come esempio di uso precedente dello stesso pattern.
>
> 9. **`.claude/agents/memoria_revisore.md:178`** (riga #122) — sostituzione con `<IP-fittizio>`.
>    - Esito: **ok**. Il word-diff mostra una sola sostituzione: l'IP letterale diventa `<IP-fittizio>`. Il resto del testo storico di #122 è invariato.
>
> **Test eseguiti**
> - `tests/test_unit_hooks.py`: 51 passati su 51.
> - Sottoinsieme `finale`: 7 su 7.
> - Mutazioni (no allowlist; ambito `reports/`): uccise da 4c e da 4b.
>
> **Riserve (da tracciare in stato_progetto.md)**
> - **R1 (media)**: errexit resta attivo dopo il gate IP. Ripristinare lo stato precedente (togliere i `set -e` e lasciare `set +e` fino alla fine, oppure salvare e ripristinare `$-`), così le righe 116-120 tornano raggiungibili e l'uscita torna normalizzata a 1 con messaggio. Conviene aggiungere un test con push fallito che verifichi la presenza di "ERRORE git push fallito" nello stderr.
> - **R2 (bassa, nota)**: l'allowlist per riga rende esente ogni IP presente su una riga che contiene il token. Il limite è condiviso con gasmerge.sh. Annullare il R1 di #122 è stata una scelta consapevole per allinearsi a gasmerge e va dichiarata come limite noto.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py. Modifiche a `tests/test_unit_hooks.py` (gate/hook only):
- Suite hook prima: 48/48 (stimato da sessione precedente)
- Suite hook dopo: **51/51 PASS** (+3 test: T-finale-4b, T-finale-4c, assertion T-finale-4 aggiornata)
- Nessuna modifica a `tests/test_unit_kernel.py`

---

## §6 STATO CI

```
completed	success	docs(hook-fine-task-obbligatorio): aggiorna §6 handoff con esito CI (…	CI	chore/hook-fine-task-obbligatorio	push	37046253217	54s	2026-10-02T18:15:54Z
completed	success	docs(hook-fine-task-obbligatorio): fix §4 handoff — citazioni file:li…	CI	chore/hook-fine-task-obbligatorio	push	37046109893	54s	2026-10-02T18:14:38Z
completed	success	chore(hook-fine-task): script deterministico + contatore per sessione…	CI	chore/hook-fine-task-obbligatorio	push	37045838781	1m3s	2026-10-02T18:12:11Z
```

**Mappatura commit→run:**
- `fa78fb5` fix(ip-gate) — run non ancora disponibile alla scrittura dell'handoff (non ancora pushato)
- `ade4c1a` chore(revisore) memoria #124 — run non ancora disponibile alla scrittura dell'handoff (non ancora pushato)
- `0accbb7` docs — run 37046253217 (SUCCESS, 54s)
- `0bb3743` docs — incluso nel push che ha prodotto run 37046109893 (SUCCESS, testa HEAD `0bb3743`? no — `0accbb7` è HEAD della run 37046253217; `0bb3743` è HEAD della run 37046109893 — SUCCESS)
- `bfb8dee` docs — incluso nel push che ha prodotto run 37045838781 (testa HEAD `9863352`; commit `bfb8dee` mai head di una run, contenuto incluso nell'albero HEAD `9863352`)
- `9863352` chore(hook-fine-task) — HEAD run 37045838781 (SUCCESS)
- `ac51ccf`, `c644990` — commit precedenti a questa sessione, coperti da run precedenti

---

## §7 RISERVE APERTE

Da review #124:
- **R-finale-1 (media)**: `set -e` attivo dopo gate IP in `fine_task_finale.sh` → push fallisce senza messaggio normalizzato; righe 116-120 diventano codice morto. Fix: ripristinare stato `set +e` dopo gate, o avvolgere push in `set +e`. Aggiungere test push-fallito.
- **R-finale-2 (bassa/nota)**: allowlist per riga in Gate IP — limite condiviso con gasmerge.sh, dichiarato consapevolmente.

Riserve ereditate (da stato_progetto.md, non chiuse in questa sessione):
- R-c2-2, R-c2-4, R-c2-5, R-c2-6 residuo, R-c2-8, R-c2-10 (feat/cancello-c2)
- R-fts-1, R-fts-2, R-fts-3, R-e2e-refactor-1, R-e2e-refactor-2 (k3-bis)
