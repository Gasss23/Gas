# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-12 — FETTA 1 cervello forte: budget ricontrollato prima di ogni chiamata (chiude F2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #191 (https://github.com/Gasss23/Gas/pull/191), secondo la regola di merge di CLAUDE.md (verdetto testuale del bot + CI verde).
2. Cervello forte, Fette 2–4: da discutere con l'operatore prima di qualunque codice.

NB: `gh` nel container non è autenticato (GH_TOKEN rifiutato); numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request` (`{"url":"https://github.com/Gasss23/Gas/pull/191"}`).

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #185**: `SALTATA — già mergiata dall'operatore il 2026-10-11 (20:56)`.
- **Fetta 1 — budget ricontrollato prima di ogni chiamata**: `FATTA` — `_budget_superato()` a inizio turno, prima di ogni `create` del ciclo agentico e prima di ogni rung di `rifletti()`. Test T88a–d.
- **Fette 2–4 cervello forte**: `DEFERITA — l'operatore vuole discuterle prima`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 ++
 gas.py                             | 58 ++++++++++++++++++++++++++++++++++++++++++----------------
 reports/diff_sessione.md           |  8 ++++++--
 reports/handoff.md                 | 84 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------
 reports/roadmap.md                 |  2 +-
 reports/stato_progetto.md          | 11 ++++++++---
 reports/ultimo_report.md           | 14 ++++++++++----
 tests/test_unit_kernel.py          | 86 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 8 files changed, 222 insertions(+), 43 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
8a50aae feat(budget): ricontrollo del budget prima di ogni chiamata (FETTA 1 cervello forte, chiude F2)
2bf657e chore(revisore): memoria review #293 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetto integrale del revisore per il commit `8a50aae` (gas.py, tests/test_unit_kernel.py), incollato:

## VERDETTO: APPROVATO CON RISERVE

Review #293. Ho esaminato il diff staged (gas.py, tests/test_unit_kernel.py) e ho rieseguito in locale tests/test_unit_kernel.py: 815 PASS / 0 FAIL, T88a–d verdi.

**Cosa ho controllato nel diff**
- `gas.py:1031` — nuovo `_budget_superato()`, punto unico del controllo sul budget. Rischio: leggere il log anche quando il budget non è impostato, oppure far nascere un crash. Esito: ok. Con il limite a 0 o non impostato restituisce None prima di chiamare `_daily_cost_usd`, che a sua volta non solleva mai eccezioni (gas.py:1026). Gli import Optional/Tuple sono già presenti (gas.py:18).
- `gas.py:3374` — controllo prima di ogni `chat.completions.create` del ciclo agentico. Rischio: fermare il turno lasciando la storia rotta (una richiesta di tool senza la sua risposta) o senza chiudere il turno. Esito: ok.
  - Il controllo arriva dopo il `_save_history()` dei risultati dei tool (gas.py:3465), quindi la storia finisce con l'ultima risposta del tool (T88b lo verifica).
  - Il `return` dentro il generatore passa dal `finally: _chiudi_turno()` (gas.py:3504).
  - Il ciclo da 10 iterazioni resta com'era, e `_get_window()` resta l'unica fonte della finestra.
  - Nessun taglio diretto della storia e nessuna simulazione di tool.
- `gas.py:3326` — controllo a inizio turno ora fatto tramite l'helper. Rischio: cambiare il comportamento esistente. Esito: ok, messaggio e `return` identici a prima.
- `gas.py:2733` — `rifletti()` ricontrolla il budget prima di ogni provider della cascata. Rischio: cambiare `provider_atteso` quando il budget è già superato all'inizio. Esito: ok. Il controllo sta prima dell'assegnazione, quindi resta None come prima; se il budget scatta prima del secondo provider, vale il primo, ed è corretto.
- `tests/test_unit_kernel.py:8164` — T88a–d. Rischio: test che passano anche senza il controllo nuovo. Esito: ok.
  - T88a pretende una sola chiamata; senza il controllo nel ciclo ce ne sarebbero 2 o più.
  - T88c fa da controprova (30 chiamate quando il budget non è impostato).
  - T88d copre il rung successivo nella riflessione.
  - Ogni test usa una cartella temporanea nuova, quindi il log costi non passa da un test all'altro. Le variabili d'ambiente e `gas.OpenAI` vengono ripristinati nel `finally`.

**Riserve (numerate)**
1. R-293-1 (BASSA, prestazioni) — `gas.py:1031`: quando il budget è impostato, `_daily_cost_usd` rilegge tutto il log JSONL dei costi a ogni iterazione. Sono fino a circa 30 letture per turno (10 iterazioni × 3 provider), più una lettura doppia all'iterazione 0, perché ripete il controllo di inizio turno. Peggiora la riserva già aperta R-tel-budget-perf (log che cresce). Senza budget impostato non costa nulla.
2. R-293-2 (BASSA, da dichiarare) — `gas.py:3374`: lo stop a metà turno blocca anche i provider gratuiti (openrouter/ollama, che costano 0). È coerente con il controllo di inizio turno, ma va scritto in roadmap/stato come scelta voluta.
3. R-293-3 (COSMETICA) — `tests/test_unit_kernel.py:8176`: il commento di `_Client88` dice «≥ 1,5 $» per chiamata, ma su flash-lite il test misura 1,00 $. Il test non cambia esito.

**Cosa NON ho verificato**
- Il comportamento con un provider vero e un log costi di dimensione reale (VPS, mesi di righe): non è riproducibile in dev. Il costo di R-293-1 è stimato, non misurato.
- La semantica del retry singolo del Gemini 400: è fuori dal diff, e ritentare la stessa chiamata senza un nuovo controllo mi sembra accettabile.
- Non ho verificato che `reports/roadmap.md` chiuda davvero la riserva F2: è un aggiornamento dei report, a carico dell'agente.

**Memoria**
Ho aggiunto la riga #293 e una lezione nuova in /home/user/Gas/.claude/agents/memoria_revisore.md. Commit atomico fatto: 2bf657e. Il diff staged del motore è intatto.

Nota dell'agente: R-293-3 corretta prima del commit (commento «≥ 1 $»); il marcatore di review è stato rigenerato sul diff con la correzione.

## §5 DELTA TEST DEL MOTORE

Kernel 811 → 815 PASS (+4: T88a–d), 0 FAIL. pytest: `1032 passed in 122.09s (0:02:02)`.

```
=== RIEPILOGO: 815 PASS, 0 FAIL ===
```

## §6 STATO CI

`gh` non autenticato nel container: stato letto con lo strumento GitHub MCP (`actions_list`, branch feat/merge-automatico-z1xjx2):

```
CI           run 886  push               8a50aae  in_progress
verifica-bot run 203  pull_request_target 8a50aae  completed/skipped (manca l'etichetta verifica)
CI           run 885  push               89a51f3  completed/success
```

Mappatura commit→run:
- `8a50aae` (feat budget): CI run 886, in corso alla scrittura dell'handoff.
- `2bf657e` (memoria revisore): nessuna run su questo SHA (pushato insieme a 8a50aae; il suo albero è incluso in quello testato da run 886).
- commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-293-1 (BASSA): rilettura del log costi a ogni iterazione con budget impostato.
- R-293-2 (BASSA, scelta dichiarata): lo stop a metà turno ferma anche i rung gratuiti.
