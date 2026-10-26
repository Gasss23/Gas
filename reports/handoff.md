# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-27 — Turno di notte: contatti illeggibili mai «0 lead» (voce 5 di `reports/coda_notte.md`)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #273 (https://github.com/Gasss23/Gas/pull/273). Numero e URL dalla risposta JSON di `gh api -X POST repos/Gasss23/Gas/pulls` (GraphQL non disponibile). Il turno di notte non mergia mai. Anche la PR #271 è aperta: la seconda delle due che entra avrà un conflitto in `coda_notte.md`/`stato_progetto.md` (tenere entrambe le righe).
2. R-520-1 (`gas fida-contatto` con lettura fallita) in coda: sì/no.
3. Testo dell'attività programmata «Turno di notte Gas»: invariato; se l'operatore lo vuole cambiare, deve chiederlo in questa sessione.

---

## §1 SCOPE & ESITO FETTE

- **Voce 4**: `SALTATA — già fatta, PR #271 ancora aperta`.
- **Fetta 1 — Voce 5, contatti illeggibili mai «0 lead»**: `FATTA` — `leggi_contatti` in `modules/memory/store.py`, usata da `modules/notte/notte.py` e `gas.py`; review #520 APPROVATO CON RISERVE.
- **Voci 6–8**: `SALTATA — toccano il motore o vengono dopo: al massimo una voce del motore a notte`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  1 +
 gas.py                             | 12 ++++++------
 modules/memory/store.py            | 15 ++++++++++++---
 modules/notte/notte.py             | 11 +++++++----
 reports/coda_notte.md              |  4 ++--
 reports/diff_sessione.md           | 23 ++++++++++-------------
 reports/handoff.md                 | n/d (commit finale)
 reports/report_notte.md            | 30 ++++++++++-------------
 reports/stato_progetto.md          |  4 +++-
 reports/ultimo_report.md           | 19 ++++++++-----------
 tests/test_unit_kernel.py          | 23 +++++++++++++++++++++--
 tests/test_unit_notte.py           | 46 ++++++++++++++++++++++++++++++----
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta tutto nel commit finale), quindi «n/d». Gli altri conteggi vengono da `git diff --cached --stat` preso prima del commit finale, con le barre accorciate; il diff reale della PR fa fede.

## §3 GIT LOG --ONELINE (sessione)

```
13b5f1b fix(memoria): contatti illeggibili mai «0 lead» nel resoconto e in ricorda fermi (coda notte voce 5)
d8163d3 chore(revisore): memoria review #520 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #520 (chat Notte) — sul diff committato in 13b5f1b

## VERDETTO: APPROVATO CON RISERVE

Review #520 (chat Notte). Ho esaminato il diff staged su notte/2026-10-27 (5 file, +88 righe, -19). Prima ho letto CLAUDE.md (sez. 5), le voci R-454-1, R-455-1 e V-2 bot #241 in reports/stato_progetto.md e la memoria del revisore.

**Elementi del diff esaminati**
- `modules/memory/store.py:1225` — la nuova `leggi_contatti` restituisce None quando la lettura dà sqlite3.Error o OSError, altrimenti la lista (anche vuota). Rischio esaminato: un cambio di comportamento per i chiamanti di `lista_contatti`. Esito: ok. `modules/memory/store.py:1215` avvolge la nuova funzione e continua a dare [] su errore, quindi pin, duplicati e ricerca restano invariati. Non solleva mai eccezioni, quindi rispetta la regola "zero crash" (§9).
- `modules/notte/notte.py:545` — se la lettura dei contatti dà None, la funzione esce lasciando i lead «non letti»; le firme sono già state contate da `conta_approvazioni`. Rischio esaminato: un DB bloccato fra le due letture mostra «Lead attivi: 0». Esito: ok. Mutante (`lista_contatti` al posto di `leggi_contatti`): 2 test falliscono (`test_stato_mattino_contatti_illeggibili_fra_due_letture` e `test_resoconto_nel_giro_con_contatti_illeggibili`).
- `gas.py:4126` — `_lead_fermi` ora usa come spia d'errore la lettura stessa; con `available=False` risponde «NON letto». Rischio esaminato: memoria a None, cioè AttributeError. Esito: ok, `_ricorda` esce prima quando la memoria è None (controllo `if self.memory is None`). Mutante in `gas.py`: il test T98k fallisce.
- `tests/test_unit_kernel.py:10790` — T98k rinomina la tabella `contatti` su un DB vero, verifica che `conta_approvazioni` continui a funzionare e fa un round-trip con `run_turn_scriptato` (tool_res seguito da final, con «NON letto» nell'output del tool). Rispetta il round-trip agentico richiesto dalla §7. Esito: ok.
- `tests/test_unit_notte.py:2301` — round-trip di un giro notturno vero, con `MemoryStore.leggi_contatti` forzata a None tramite monkeypatch. È un fallimento simulato della lettura del DB, non dell'output di un tool, quindi non viola la regola contro la simulazione dei tool. Esito: ok.

**Misure rifatte**: kernel 1039 PASS, 0 FAIL; `tests/test_unit_notte.py` 175 passed. Dopo i mutanti ho ripristinato i file: nessuna modifica fuori dallo stage.

**Wall of Shame**: nel diff non c'è slicing della history né simulazione dell'output dei tool. Guardrail (10 iterazioni, `_get_window`) non toccati.

**Riserve**
- R-520-1 BASSA (fuori fetta, stessa classe del bug): a `gas.py:5691`, `gas fida-contatto` lanciato senza argomenti usa `lista_contatti` e, se la lettura fallisce, stampa «Nessun lead segnato «non fidato»». È una rassicurazione falsa su un segnale di sicurezza. Fix: passare a `leggi_contatti` e, su None, stampare FAIL o WARN. Va tracciata in stato_progetto.md.

**Rischio escluso**: non ho riprodotto un vero «database is locked» concorrente (due processi con lock in scrittura). Il test usa una tabella rinominata o un monkeypatch. L'equivalenza regge perché entrambi i casi passano dallo stesso `except (sqlite3.Error, OSError)`. Il timeout di 10 secondi di `_connect` con un lock reale non è stato misurato.

Memoria aggiornata con la riga #520 e committata (d8163d3, solo `/home/user/Gas/.claude/agents/memoria_revisore.md`). Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

- `python tests/test_unit_kernel.py`: main `=== RIEPILOGO: 1037 PASS, 0 FAIL ===` → ramo `=== RIEPILOGO: 1039 PASS, 0 FAIL ===` (T98k, T98l nuovi; T98h aggiornato). Con il codice vecchio e lo store nuovo: `1038 PASS, 1 FAIL` (T98k).
- `python -m pytest -q tests/`: main `2241 passed, 1 skipped` → ramo `2243 passed, 1 skipped`. I 2 test notte nuovi falliscono sul codice vecchio. Nessun FAIL.

## §6 STATO CI

```
completed	skipped	Turno di notte 2026-10-27: contatti illeggibili mai «0 lead» (coda voce 5)	verifica-bot	notte/2026-10-27	pull_request_target	40422794561	8s	2026-10-26T23:53:28Z
in_progress		fix(memoria): contatti illeggibili mai «0 lead» nel resoconto e in ri…	CI	notte/2026-10-27	push	40422790431	25s	2026-10-26T23:53:26Z
```

Mappatura commit→run:
- `d8163d3`: nessuna run su questo SHA (pushato insieme a `13b5f1b`).
- `13b5f1b` → run CI 40422790431 (push), in corso alla scrittura dell'handoff.
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-520-1 (chat Notte)** BASSA: `gas fida-contatto` senza argomenti, a lettura fallita, dice «Nessun lead segnato non fidato».
- Non riprodotto un vero blocco del DB fra due processi.
