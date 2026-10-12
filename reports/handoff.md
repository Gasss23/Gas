# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-12 — «Pipeline esausta» dice perché (dopo il giro di notte di prova)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR (tocca `gas.py`): secondo la regola di CLAUDE.md (verdetto testuale del bot APPROVATO senza finding, altrimenti decide l'operatore).
2. Sul Mac il repo è su un HEAD staccato: `git checkout main && git pull` prima di ripetere `python3 gas.py notte`.

---

## §1 SCOPE & ESITO

- **Messaggio «Pipeline esausta»**: `FATTO` — motivo per ogni cervello, mai il testo grezzo dell'errore.
- **Giro di notte di prova**: `FATTO` — cloud (copia usa-e-getta): nessun crash, KO per chiavi assenti; Mac: 1 compito OK (codice vecchio, HEAD staccato).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 gas.py                             |  20 ++++++++++++++++++--
 reports/diff_sessione.md           |   8 ++++----
 reports/handoff.md                 | 146 +++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  10 +++++-----
 tests/test_unit_kernel.py          |  47 ++++++++++++++++++++++++++++++++++++++++++++---
 7 files changed, 104 insertions(+), 132 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
913e6fd fix(kernel): «Pipeline esausta» dice perché ogni cervello non ha risposto
4558b8f chore(revisore): memoria review #292 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE

### Review #292

## VERDETTO: APPROVATO CON RISERVE

Review #292. Diff STAGED esaminato: `gas.py` e `tests/test_unit_kernel.py`. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md e la memoria del revisore.

**Elementi del diff esaminati**
- `gas.py:3331`: dichiara la lista `_motivi: List[str]`, con i type hints. Rischio esaminato: che la lista non si azzeri tra un turno e l'altro. Esito: ok, è locale a `run_turn` e viene ricreata a ogni turno.
- `gas.py:3333`: se manca la chiave registra «<provider>: <VAR> non impostata» e poi fa `continue`. Rischio esaminato: che la variabile esponga un dato sensibile. Esito: ok, compare solo il nome della variabile e mai il suo valore.
- `gas.py:3448`: la risposta vuota registra il motivo prima del `break`. Esito: ok. Il `break` salta l'`else` del ciclo `for`, quindi il motivo non viene registrato due volte.
- `gas.py:3451`: l'`else` del ciclo `for _ in range(10)` registra «10 iterazioni senza risposta finale». Rischio esaminato: che il limite di 10 iterazioni (CLAUDE.md sez. 8) venga indebolito. Esito: ok, il limite non è toccato. Un `return` su risposta finale e un'eccezione non entrano nell'`else`.
- `gas.py:3469`: per un'eccezione registra il livello dato da `_classify_provider_error` più `HTTP <status>` solo se lo status è un intero, altrimenti il nome della classe dell'eccezione. Rischio esaminato: che il testo grezzo dell'errore finisca all'utente o nel diario di notte. Esito: ok. `str(e)` serve solo per classificare internamente, e il KO generico (`err_text[:60]`) resta nella seconda variabile, che viene scartata. La gestione delle eccezioni nella cascata è intatta: log come warning, poi `continue` sul provider successivo.
- `gas.py:3474-3477`: compone il dettaglio con un ripiego («nessun provider in cascata») se la lista è vuota, logga un warning e restituisce il messaggio «Pipeline esausta: nessun cervello ha risposto. …». Rischio esaminato: rompere chi legge questo messaggio. Esito: ok. `tests/test_unit_notte.py:311` e `tests/test_unit_voice_server.py:300` cercano solo la sottostringa «Pipeline esausta», e in tutto il repo nessuno confronta più la stringa esatta.
- `tests/test_unit_kernel.py:208`: T9b richiede ora `startswith("Pipeline esausta:")` e conta 3 volte il motivo «10 iterazioni». Esito: ok, riprodotto.
- `tests/test_unit_kernel.py:8125-8162`: T87 usa un client finto che solleva un 429 con «segreto-nel-testo-87» e chiavi assenti, poi ripristina le variabili d'ambiente e `gas.OpenAI` nel `finally`. Esito: ok. Non simula l'output di un tool: è un'eccezione del provider, un uso legittimo.

**Wall of Shame**: nessuno slicing della history. `_get_window()` non è toccata e non c'è simulazione di output dei tool.

**Riproduzione**: kernel 811 PASS / 0 FAIL (T9b e T87a PASS). `pytest tests/test_unit_notte.py tests/test_unit_voice_server.py` dà 77 passed. La suite pytest completa da 1032 non l'ho rilanciata.

**Riserve**
- R-292-1 (BASSA): due rami nuovi non hanno un test, cioè «risposta vuota» e l'etichetta col nome della classe (eccezione senza `status_code`, per esempio un errore di connessione). Sono semplici da leggere, ma un errore di battitura lì passerebbe inosservato.
- R-292-2 (COSMETICA): con un compito «semplice» la stessa chiave Gemini assente compare due volte (gemini-flash-lite e gemini-flash) e il messaggio si allunga.

**Rischio escluso**: non ho verificato come appare il messaggio, ora più lungo, su Telegram e sull'interfaccia vocale (limiti di lunghezza, lettura TTS) né nel giro di notte reale sul VPS. Non è riproducibile in dev e sui provider reali non ho token. Ho controllato solo che i consumer nel repo usino la sottostringa.

Memoria aggiornata (riga #292 più una lezione) e committata con lo script: commit 4558b8f in /home/user/Gas/.claude/agents/memoria_revisore.md.

## §5 DELTA TEST DEL MOTORE

Kernel 810 → 811 PASS / 0 FAIL in locale (T87a nuovo, T9b aggiornato). pytest completo 1032 passed.

## §6 STATO CI

Run non ancora disponibile alla scrittura dell'handoff (primo push della sessione con questo commit).

## §7 RISERVE APERTE

R-292-1 (BASSA): rami «risposta vuota» ed eccezione senza status_code non testati. R-292-2 (COSMETICA): chiave Gemini ripetuta due volte nel messaggio.
