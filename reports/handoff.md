# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — chat Motore: interruttore del forte tra shell e `.env` (PR #293), dopo la chiusura della PR #290 come doppione della #291

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #293 (https://github.com/Gasss23/Gas/pull/293): review #547 (già #543 nel ramo) APPROVATO CON RISERVE, quindi decide l'operatore (CLAUDE.md §10). Numero e URL dalla risposta JSON dello strumento GitHub `create_pull_request` (`gh` non autenticato in questo ambiente).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — PR #290**: `FATTA` — chiusa senza merge (doppione della #291) su «ok» dell'operatore; il merge `6e19169` riporta il ramo all'albero di main.
- **Fetta 3 — Merge di main (PR #288) e rinumerazione della review #543 → #547**: `FATTA` — V-1 MEDIA e V-2 BASSA della verifica esterna su #293; review #548 APPROVATO.
- **Fetta 2 — WARN su GAS_CLAUDE_CLI tra shell e .env, in tutti e due i versi**: `FATTA` — V-3 bot #290 e V-1 ve #290; `_DOTENV_SCAVALCATE` con i soli nomi.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 gas.py                             |  17 ++++++++++++++-
 reports/diff_sessione.md           |  17 +++++++--------
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  49 +++++++++----------------------------------
 tests/test_unit_dotenv.py          |  13 ++++++++++++
 tests/test_unit_kernel.py          |  28 +++++++++++++++++++++++++
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d» e niente riga di totale. Conteggi presi con i report in stage.

## §3 GIT LOG --ONELINE (sessione)

```
6393dd8 Merge origin/main (PR #288) in feat/merge-automatico-z1xjx2 (PR #293) — review #548 APPROVATO; review #543 del ramo rinumerata #547 (V-2 ve #293)
6b23e1b docs(fine-task): PR #293 — interruttore del forte tra shell e .env, review #543; PR #290 chiusa
b24bd9f fix(doctor): GAS_CLAUDE_CLI della shell e del .env discordi → WARN in tutti e due i versi (V-3 bot #290, V-1 ve #290)
5a1c9e7 chore(revisore): memoria review #543 — APPROVATO CON RISERVE
6e19169 Merge di main nel ramo dopo la chiusura della PR #290 (doppione della #291): si tiene l'albero di main
a04dd49 docs(fine-task): PR #290 — riserve del punto 3, review #540-#542, V-1..V-3 bot #290
a8cde14 fix(doctor): .env di Gas (DOTENV_PATH), valore diverso nel .env e GAS_CLAUDE_CLI solo nella shell → WARN (V-1..V-3 bot #290)
f530158 chore(revisore): memoria review #542 — APPROVATO CON RISERVE
6771320 fix(doctor): .env con GAS_CLAUDE_BIN vuota o virgolette aperte non conta (V-1 ve #290), test .venv collegato (V-2 ve #290)
ae576f9 chore(revisore): memoria review #541 — APPROVATO
ae66740 docs(fine-task): PR #290 — riserve del punto 3, review #540
cceadcc fix(forte): riserve del punto 3 — WARN se GAS_CLAUDE_BIN sta solo nella shell, motivo senza prefisso ripetuto e non troncato, /usr/local su Linux
e6604cb chore(revisore): memoria review #540 — APPROVATO CON RISERVE
```

NB: base `d4b39ca` (main con la PR #288). I commit da `e6604cb` a `a04dd49` sono quelli della PR #290, chiusa senza merge. Il merge `6e19169` ne annulla il contenuto, perché tiene l'albero di main (`2f35bc6`): il diff della sessione rispetto a main è solo quello del §2, cioè il commit `b24bd9f` e i report. I loro verdetti (#540, #541, #542) sono nell'handoff della #290 (`a04dd49`). Il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #547 (chat Motore; nel ramo numerata #543, rinumerata per V-2 della verifica esterna su #293: #543 c'è già su main, chat Mani) — sul diff di b24bd9f

## VERDETTO: APPROVATO CON RISERVE

Review #543 (chat Motore) sul diff STAGED di feat/merge-automatico-z1xjx2 (gas.py, tests/test_unit_dotenv.py, tests/test_unit_kernel.py; +57/-1). Ho letto CLAUDE.md, le voci di stato_progetto.md su GAS_CLAUDE_CLI e la coda della memoria del revisore.

**Elementi del diff che ho esaminato**
- `gas.py:627` — in `_carica_dotenv`, se la variabile esiste già nella shell, il nome va in `_DOTENV_SCAVALCATE` solo quando il valore del `.env` è DIVERSO, poi `continue` come prima. Rischi controllati: sovrascrittura, fuga di valori, comportamento con stesso valore. Il comportamento resta lo stesso (non sovrascrive mai). Il set contiene solo nomi, nessun valore finisce nei log. Con lo stesso valore il nome non viene registrato. Con `GAS_NO_DOTENV` si esce prima (`gas.py:595`), quindi niente viene registrato. — ok
- `gas.py:575` — dichiarazione del set globale, accanto a `_DOTENV_CARICATE`. Rischio controllato: stato globale che resta da un test all'altro. Nel processo vero viene popolato una sola volta da `main()` (`gas.py:6081`). — ok
- `gas.py:5008` — doctor con il forte spento: se il nome è in `_DOTENV_SCAVALCATE` dà WARN «spento nella shell ma il .env ha un altro valore», altrimenti OK come prima. Rischio controllato: un falso OK nel verso che conta. — ok, salvo la riserva R-543-2
- `gas.py:5015` — doctor con il forte acceso ma `GAS_CLAUDE_CLI` non in `_DOTENV_CARICATE`: dà WARN e poi continua con i controlli del comando e del conto, senza ritorno anticipato. Un WARN non cambia il codice di uscita. — ok, salvo la riserva R-543-1
- `tests/test_unit_dotenv.py:136` — collega la funzione vera al set: monkeypatch di entrambi i set, valore diverso → nel set, valore uguale → fuori, variabile nuova → in CARICATE, valore della shell intatto. Applica la lezione di #540. — ok
- `tests/test_unit_kernel.py:11227` — T99w/T99x: tutti e quattro i casi del doctor. Il `finally` toglie `GAS_CLAUDE_CLI` da entrambi i set e rimette il valore precedente di `GAS_CLAUDE_CLI` (lo toglie se prima non c'era). — ok

**Prove che ho rifatto**
- Suite del kernel: 1063 PASS, 0 FAIL.
- `tests/test_unit_dotenv.py`: 12 passed.
- Mutante 1: confronto `!=` sostituito con `if True` → il test pytest fallisce (1 failed).
- Mutante 2: ramo `_DOTENV_SCAVALCATE` del doctor disattivato → T99x FAIL.
- `gas.py` rimesso com'era (git diff del working tree vuoto) e indice intatto.

**Riserve**
- R-543-1 (BASSA): il confronto è tra stringhe, non tra significati. Shell «1» con `.env` «true» dà un falso WARN «acceso nella shell ma non dal .env… metti GAS_CLAUDE_CLI=1», un consiglio fuorviante perché il `.env` lo accende già. Shell «0» con `.env` «false» dà un falso WARN «altro valore». È il verso prudente, quindi accettabile. Il rimedio sarebbe confrontare con la stessa regola di `_env_flag`.
- R-543-2 (BASSA): con `GAS_NO_DOTENV=1` nella shell e il forte spento, il doctor dà OK anche se il `.env` lo accende per il giro notturno, che non ha `GAS_NO_DOTENV`. Non fa danni: `GAS_NO_DOTENV` si usa solo nella suite, e un forte acceso di notte resta sotto il tetto giornaliero. Va comunque dichiarato.

**Cosa non ho verificato e perché**
- Il comportamento vero del timer launchd sul Mac (il `.env` del Mac, il giro notturno reale): non si può riprodurre in questo container.
- La suite pytest completa: ho eseguito solo `tests/test_unit_dotenv.py` e la suite del kernel.

Il diff non contiene slicing della history né simulazione dell'output dei tool. Non tocca il tetto di 10 iterazioni, il tetto di 8k in uscita, `_get_window` né i provider.

- Riga contatore #543 aggiunta e committata (5a1c9e7) in /home/user/Gas/.claude/agents/memoria_revisore.md. Nessuna lezione nuova: quella su «da dove arriva la variabile» c'è già, da #538.

Riserve da tracciare in /home/user/Gas/reports/stato_progetto.md prima del commit: R-543-1 e R-543-2.

### Review #548 (chat Motore) — sul merge di origin/main (PR #288) in 6393dd8

## VERDETTO: APPROVATO

Il merge è corretto: non si perde nessuna riga da nessuno dei due lati, non resta nessun marcatore di conflitto e il codice è identico ai due lati come deve essere.

Elementi del diff esaminati:
- `modules/web/lexbor.py:172` — figlio lexbor con lo shadow DOM dichiarativo, portato da main. Rischio esaminato: che la risoluzione del merge lo abbia alterato. `git diff --cached origin/main` è vuoto per questo file, per `tests/test_unit_web_lexbor.py` e per `reports/ripartenza_mani.md`. Esito: ok.
- `.claude/agents/memoria_revisore.md:943` — riga #547, cioè la #543 del ramo rinumerata. Rischi esaminati: righe perse o testo cambiato. Verso main il diff è una sola riga aggiunta (la #547), quindi le #539–#546 della chat Mani ci sono tutte. Verso HEAD sparisce solo la riga #543 della chat Motore: tolta l'intestazione, il suo testo coincide byte per byte con quello della #547 (controllato con `diff`). Esito: ok.
- `reports/stato_progetto.md:4` — riga «Ultimo aggiornamento». Rischio esaminato: frasi perse da uno dei lati. Il word-diff verso HEAD toglie solo `#543)` (che diventa `#547)`) e per il resto aggiunge soltanto. Verso main ci sono solo aggiunte. Esito: ok.
- `reports/stato_progetto.md:634` — voce «Mani — fetta 23». Rischio esaminato: voce duplicata. Compare una volta sola nell'indice, come su main. Esito: ok.
- `reports/ultimo_report.md:4` — il riferimento «review #543» diventa «#547 (già #543 nel ramo)». È l'unica modifica rispetto a HEAD. Esito: ok.
- Contesto, file non toccati dal merge: `gas.py`, `brains/`, `tests/test_unit_kernel.py`, `tests/test_unit_dotenv.py`, `reports/handoff.md` e `reports/diff_sessione.md` sono identici a HEAD (`git diff --cached --quiet HEAD` restituisce 0). Il codice della PR #293 resta quello revisionato.

Altre verifiche: nessun marcatore `<<<<<<<` o `>>>>>>>` nei file dell'indice né in handoff e diff_sessione. `pytest tests/test_unit_web_lexbor.py` dà 20 passed e 85 skipped.

Rischio escluso: il comportamento vero di lexbor non è stato verificato, perché 85 test vengono saltati: selectolax non è installato in questo ambiente. È accettabile, dato che quei file sono identici a origin/main, già revisionati e passati in CI con la PR #288.

**Problema operativo da sistemare prima di chiudere il merge:** la riga contatore #548 è scritta nel file `/home/user/Gas/.claude/agents/memoria_revisore.md` ma NON è committata e non è nell'indice. `scripts/commit_memoria_revisore.sh` è fallito senza danni: «fatal: cannot do a partial commit during a merge», con avviso in `/home/user/Gas/gas_debug.log`. L'agente principale deve fare `git add .claude/agents/memoria_revisore.md` prima di `git commit`.

La memoria è cambiata dopo questa review: lo SHA-256 del diff staged non corrisponderà a quello revisionato. Va ricalcolato dopo l'add, con `scripts/segna_review_ok.sh`. L'unica differenza in più è la riga #548.

Riga in memoria: #548 — APPROVATO — nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

Suite kernel: 1061 → 1063 PASS (T99w, T99x nuovi), 0 FAIL. Il valore di main è misurato in un worktree a `2f35bc6`; il merge di main (PR #288) non tocca il kernel.

```
=== RIEPILOGO: 1063 PASS, 0 FAIL ===
```

pytest (tutti i file tranne la suite kernel), sulla testa `b24bd9f`: `2284 passed, 61 skipped in 205.60s (0:03:25)`.

## §6 STATO CI

CI letta con lo strumento GitHub della sessione: `gh run list` non è disponibile (`gh` non autenticato).

Mappatura commit→run:
- `6e19169`, `5a1c9e7`: nessuna run su questi SHA (pushati insieme a `b24bd9f`).
- `b24bd9f`: pushato prima dell'apertura della PR #293; la run del push non l'ho letta.
- `6b23e1b`: `handoff-check` success; `unit-suite` e `verifica-bot` in corso alla lettura della verifica esterna, poi superati dal merge (conflitto con main).
- `6393dd8`: nessuna run su questo SHA (pushato insieme al commit di fine-task).
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-543-1 BASSA: confronto tra stringhe (`1` contro `true` → WARN in più, verso prudente).
- R-543-2 BASSA: con `GAS_NO_DOTENV=1` nella shell il doctor non vede il `.env`.
- V-3 BASSA ve #293: T99n stampa un WARN in più (dipende dal set globale), nessun fallimento.
