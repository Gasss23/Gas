# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-20 (dopo il merge di #222) — README e cartelle di progetto alla firma dopo una lettura, comando `gas fida-contatto`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR: l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10); altrimenti decide l'operatore.

---

## §1 SCOPE & ESITO FETTE

- **R-ve222-4 (file letti dagli agenti alla firma dopo una lettura)**: `FATTA` la parte sui file — review #377; resta aperta la parte su recapito/chiusura di un lead (V-1 bot #224).
- **R-bot222-1 (comando `gas fida-contatto`)**: `FATTA` — review #377.
- **Riserve R-377-1/R-377-2**: `FATTA` — review #378 APPROVATO CON RISERVE (R-378-1 BASSA).
- **V-1 bot #224 (race tra scheda e conferma in fida-contatto)**: `FATTA` — review #379 APPROVATO CON RISERVE (R-379-1 BASSA).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 ++
 gas.py                             |  65 +++++++++++++++++++++++++++++++++++++-
 modules/gate/gate.py               |  18 +++++++++++
 modules/memory/store.py            |  34 ++++++++++++++++++++
 reports/diff_sessione.md           |  16 +++++-----
 reports/handoff.md                 | 617 ++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 ++-
 reports/ultimo_report.md           |  26 ++++++----------
 tests/test_unit_gate.py            |  25 ++++++++++++++-
 tests/test_unit_kernel.py          |  82 ++++++++++++++++++++++++++++++++++++++++++++++++
 10 files changed, 320 insertions(+), 570 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
d6fe921 fix(memoria): fida-contatto toglie il segno solo se il lead è quello mostrato (V-1 bot #224)
382ffbd chore(revisore): memoria review #379 — APPROVATO CON RISERVE
47d83fc docs(fine-task): esiti di bot e verifica esterna #224; R-ve222-4 chiusa solo per i file
b59b2dd docs(fine-task): report e handoff — R-ve222-4 e gas fida-contatto
a2f9d50 fix(cancello): tipi di diario delle azioni umane riservati; AGENT.md e CONVENTIONS.md alla firma (R-377-1, R-377-2)
9037bbb chore(revisore): memoria review #378 — APPROVATO CON RISERVE
a0d6ac1 feat(cancello): README e cartelle di progetto alla firma dopo una lettura; comando gas fida-contatto
56580d9 chore(revisore): memoria review #377 — APPROVATO CON RISERVE
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #377

## VERDETTO: APPROVATO CON RISERVE

Review #377. Letture obbligatorie fatte: CLAUDE.md (sez. 5 Wall of Shame, sez. 8 guardrail, sez. 10 roadmap), le voci R-ve222-4 e R-bot222-1 in reports/stato_progetto.md, e la memoria del revisore. Ho esaminato il diff STAGED su feat/merge-automatico-z1xjx2: 5 file, +179/-1.

**Wall of Shame e guardrail.** Nessuno slicing della cronologia e nessun output di tool simulato. `_get_window`, il tetto di 10 iterazioni e il tetto di 8k caratteri in output non sono toccati. Il nuovo comando non è esposto come strumento dell'agente.

**Elementi del diff esaminati**
- `modules/gate/gate.py:508`: dopo una lettura manda alla firma i file nella radice (`len(parts) < 2`) e le cartelle di progetto (prefisso casefold del primo pezzo). Rischio esaminato: cartelle del repo rimaste scoperte e falsi liberi. Ho confrontato con `ls -a` della radice: tutte le cartelle di primo livello sono coperte (brains, clients, modules, scripts, tests, tools; reports e knowledge dal controllo precedente; .claude e .github dal controllo sui file nascosti). `testsuite/a.md` → firma (sbaglia dal lato sicuro), `documenti/a.md` e `clienti/a.md` → liberi. Esito: ok.
- `modules/gate/gate.py:511`: prefisso del nome per le istruzioni agli agenti. Rischio esaminato: travestimenti Unicode e forme degeneri. `Ｒeadme.md`, `dati/ＲＥＡＤＭＥ.md`, `README` con carattere invisibile (zero-width), `dati/ readme.md` e `dati/x/Claude.local.md` vanno tutti alla firma. `dati/agenda.md` resta libero (nessun falso positivo su «agents»). Esito: riserva cosmetica R-377-2 (sotto).
- `modules/memory/store.py:1162`: `togli_segno_non_fidato` risolve il canonico, scrive la riga di diario `contatto_fidato` e poi fa l'UPDATE nella stessa transazione. Le eccezioni sono intercettate e loggate come warning, con ritorno None. Rischio esaminato: atomicità e lapidi (contatti fusi). Segue il canonico come `get_contatto_per_chiave` (così è coerente con il controllo «già fidato» in gas.py) e il diario resta append-only. Esito: ok.
- `gas.py:4758`: `fida_contatto_cmd`. Rischio esaminato: crash, conferma saltata, testo di terzi mostrato al terminale. EOF e Ctrl-C portano ad «annullata». La conferma è y/N con default no. Con DB assente o in degrado esce con codice 1 senza crash. `_print_record` (`gas.py:4650`) stampa con `!r`, quindi le sequenze ANSI e i ritorni a capo di testo iniettato vengono resi visibili e non possono nascondere istruzioni all'operatore. Esito: ok.
- `gas.py:5080`: aggancio in `main()`, in parallelo a merge-contacts. Esito: ok.
- `tests/test_unit_gate.py:762` e `tests/test_unit_kernel.py:5891`: casi parametrici e round-trip agentico T74b5 (lettura, poi batch con README/tests/dati). `tests/test_unit_kernel.py:5924`: con conferma, segno tolto, pin di nuovo fidato con un kernel nuovo, riga di diario presente. Esito: ok.

**Riproduzioni**
- `tests/test_unit_kernel.py`: 922 PASS, 0 FAIL.
- `tests/test_unit_gate.py`: 689 passed.
- Mutazione 1, controllo radice/progetto disattivato (`if False:`): 6 FAIL nel gate e il round-trip T74b5 R-ve222-4 FAIL nel kernel.
- Mutazione 2, tipo di diario `contatto_fidato` cambiato in `altro`: FAIL solo «T74b5 fida-contatto con conferma».
- Dopo le mutazioni i file sono stati ripristinati: `git status` mostra solo i 5 file staged, nessuna modifica fuori dallo staging.

**Riserve**
- **R-377-1 BASSA**: «contatto_fidato» non è tra i tipi di diario riservati (`gas.py:559`, `_TIPI_DIARIO_KERNEL`). Il diario delle chiamate agli strumenti usa come tipo il nome scelto dal modello. Quindi un modello manipolato che chiama uno strumento inventato di nome «contatto_fidato» scrive una riga dello stesso tipo della traccia dell'operatore: la traccia «chi e quando» si può falsificare. Il segno sul contatto però non cambia, e il test T74b5 controlla solo `any(tipo == ...)`. Rimedio: aggiungere "contatto_fidato" a `_TIPI_DIARIO_KERNEL` (vale anche per "merge_snapshot", già scoperto da prima).
- **R-377-2 COSMETICA**: `dati/AGENT.md` (al singolare, convenzione di alcuni strumenti) e `dati/CONVENTIONS.md` (aider) restano liberi dopo una lettura. Rimedio: prefisso «agent» al posto di «agents» (blocca anche «agente*», ma sbaglia dal lato sicuro) e aggiungere «conventions».

**Rischi esplicitamente esclusi**
- Esecuzione reale di `python gas.py fida-contatto` su un terminale interattivo con il DB vero dell'operatore: non riproducibile qui. Coperta solo dal test con `input` e `sys.argv` sostituiti.
- Lettura dei file scritti nelle sottocartelle di lavoro (dati/…) da parte di strumenti esterni futuri (connettori, R3): non verificabile oggi.
- Non ho rieseguito tutto `pytest tests/` (1517 dichiarati), solo kernel e gate.

**Memoria**: riga #377 con la lezione (un nuovo tipo di diario che traccia un'azione umana va aggiunto ai tipi riservati) aggiunta a /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (56580d9). Il diff staged è intatto.

### Review #378

## VERDETTO: APPROVATO CON RISERVE

Prima della review ho letto CLAUDE.md (sezioni 5, 8 e 10), stato_progetto.md (cercando le voci R-377) e memoria_revisore.md, fino alla riga #377.

**Elementi del diff esaminati**
- `gas.py:560` — aggiunge "contatto_fidato", "merge_snapshot" e "merge_evento" ai tipi di diario riservati al kernel. Rischio esaminato: un tool inventato dal modello scrive una riga di diario uguale alla traccia di un'azione dell'operatore o della CLI. Ho verificato che i tre tipi esistono davvero in `modules/memory/store.py:894`, `modules/memory/store.py:904` e `modules/memory/store.py:1176`. Le righe del kernel non passano dalla rimappatura, che vale solo per le tool call (`gas.py:1920`, confronto con strip e casefold). Esito: ok, R-377-1 chiusa.
- `tests/test_unit_kernel.py:5895` — prova completa con un tool chiamato «Contatto_Fidato» (con le maiuscole, quindi controlla anche il casefold). Rischio esaminato: un test che passa comunque. Il test controlla anche che i tre tipi siano nell'insieme riservato, quindi senza la correzione fallisce. Riprodotto: `[PASS] … ['turno_fine', 'tool_nome_riservato']`, kernel 923 PASS 0 FAIL. Esito: ok.
- `modules/gate/gate.py:479` — sostituisce il prefisso «agents» con «agent» e aggiunge «conventions» in `_FIRMA_DOPO_LETTURA_NOMI`. Rischio esaminato: prefisso troppo largo. Ho provato `libero_dopo_lettura` sui nomi seguenti:
  - AGENT.md, Agents.md e conventions.md → firma richiesta (False);
  - agenda.md e convenzioni.md → restano liberi (True);
  - però anche dati/agente_vendite.md e dati/agenti.md ora chiedono la firma (False).

  Esito: riserva R-378-1.
- `tests/test_unit_gate.py:780` — aggiunge i casi dati/AGENT.md e dati/CONVENTIONS.md. test_unit_gate: 691 passed, riprodotto. Esito: ok.

**Riserve**
- R-378-1 BASSA: il prefisso «agent» prende anche parole italiane comuni nel dominio di Gas («agente», «agenti»). Dopo una lettura, scrivere file come dati/agente_vendite.md chiede la firma. È solo attrito: in caso di dubbio il gate blocca (fail-closed), non è una falla. Correzione possibile, se serve: due voci separate, "agent." e "agents", invece del prefisso nudo. Va scritta in stato_progetto.md.

**Antipattern e guardrail**: nessuno slicing della history, nessuna simulazione di output dei tool, nessun guardrail indebolito. Il diff stringe soltanto.

**Rischio escluso**: non ho rilanciato `pytest tests/` intero (il chiamante dichiara 1519 passed). Ho rieseguito solo le due suite toccate dal diff. Non ho fatto mutazioni oltre a leggere le asserzioni del test.

**Memoria**: riga #378 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata (9037bbb) con scripts/commit_memoria_revisore.sh. Lezione nuova: prima di accorciare un prefisso su nomi inglesi, provarlo contro le parole italiane del dominio.

### Review #379

## VERDETTO: APPROVATO CON RISERVE

Review #379 sul diff in staging di feat/merge-automatico-z1xjx2 (PR #224), che chiude V-1 BASSA del bot su 47d83fc. Prima della review ho letto CLAUDE.md (sezioni 5, 8 e 9), reports/stato_progetto.md (in modo mirato) e la mia memoria.

**Cosa ho esaminato nel diff**
- `modules/memory/store.py:1174`: apre `BEGIN IMMEDIATE` prima di leggere il record canonico e lo confronta con la scheda mostrata (`dict(c) != dict(atteso)`). Se sono diverse annulla la transazione e ritorna None. Rischio esaminato: tra il controllo e la scrittura un altro turno potrebbe scrivere (TOCTOU). Il lock in scrittura viene preso prima della lettura, quindi lettura, scrittura nel diario e UPDATE stanno nella stessa transazione serializzata. Python usa la gestione transazioni di default (non c'è nessun `autocommit` impostato in `_connect`), quindi il BEGIN esplicito funziona. In caso di contesa, l'`OperationalError` dopo il timeout di 10 secondi viene intercettato dall'except già presente: si scrive un warning e si ritorna None, senza crash (§9). Esito: ok.
- `modules/memory/store.py:1177`: c'è un `rollback()` esplicito anche sul ramo «chiave assente», così il lock non resta aperto. Esito: ok.
- `gas.py:4810`: `fida_contatto_cmd` passa `atteso=rec`. `rec` arriva da `get_contatto_per_chiave` e quindi dallo stesso `_risolvi_canonico` (`modules/memory/store.py:944`): stesse chiavi e stessi tipi, il confronto è omogeneo. Ho controllato anche altri due casi. Con `--yes` passa lo stesso `atteso`. Se nel frattempo il lead viene fuso in un altro, cambia l'id canonico, il confronto fallisce e il segno non viene tolto (fail-closed). Esito: ok.
- `tests/test_unit_kernel.py:5938`: T74b5 V-1 bot #224 riscrive il lead dentro il prompt di conferma (`input` sostituito dal test) e verifica tre cose: rc 1, `non_fidato` ancora a 1, nessuna riga `contatto_fidato` nel diario. La riscrittura passa dall'`upsert_contatto` reale, nessun output di tool simulato. Esito: ok.

**Cosa ho riprodotto io**
- Suite del kernel: 924 PASS, 0 FAIL.
- `pytest tests/`: 1519 passed.
- Mutazione su una copia usa e getta (condizione di confronto sostituita da `if False:`): 923 PASS, 1 FAIL. Fallisce solo il T74b5 nuovo, quindi il test protegge davvero il fix.
- Sonda diretta su `MemoryStore`: riscrivere il lead con contenuto identico dopo la stampa dà None (il segno resta); con una scheda presa subito prima dà successo.

**Riserve**
- **R-379-1 (BASSA)**: il confronto è sulla riga intera, `aggiornato_il` compreso. Quindi anche una riscrittura con contenuto identico fa fallire il comando (verificato con la sonda). Inoltre il messaggio mette insieme due cause diverse: «scheda cambiata» e «degrado DB». Blocca per sicurezza (fail-closed), costa solo un po' di attrito: l'operatore rilancia il comando. Se si vuole, si possono separare i due casi di None nel messaggio. Va tracciata in stato_progetto.md.

**Cosa non ho verificato**
- La contesa reale fra due processi (un turno di Gas in background che scrive mentre il comando aspetta la «y»). Il test la simula nello stesso processo, sostituendo `input`. Non ho lanciato due processi con un lock SQLite vero. La correttezza qui si basa sulla semantica documentata di `BEGIN IMMEDIATE`.
- Il comportamento sulla VPS: non riproducibile in sviluppo.

**Antipattern (Wall of Shame)**: nessuno slicing della history, nessuna simulazione dell'output dei tool. Non sono toccati il cap di 10 iterazioni, `_get_window` né i guardrail.

**Memoria**: aggiunta la riga #379 con una lezione (un controllo «conferma su ciò che hai visto» va fatto nella stessa transazione della scrittura, con il lock preso prima della lettura). Committata da `scripts/commit_memoria_revisore.sh` (382ffbd); il diff in staging del motore resta intatto.

**Incidente durante la review**: per sbaglio ho lanciato `git stash push --keep-index`. Ho controllato che lo stash coincidesse con l'index e che il working tree fosse uguale all'index, poi l'ho eliminato: nessuna modifica persa, staging invariato (3 file, +33/-5).

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 916 → 924 PASS, 0 FAIL (T74b5). Blocco reale: `=== RIEPILOGO: 924 PASS, 0 FAIL ===`. In CI i conteggi sono +2 (test del profilo sandbox saltati in locale).
pytest `tests/`: `1519 passed in 187.04s (0:03:07)` (+22 gate).

## §6 STATO CI

- `b59b2dd`: unit-suite e handoff-check success (kernel 925 PASS in CI); verifica-bot neutral (APPROVATO CON RISERVE, nessuna ALTA/MEDIA); verifica esterna APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/224#issuecomment-6292485286)).
- `47d83fc`: unit-suite e handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE, V-1 BASSA race in fida-contatto chiusa in `d6fe921`).
- `d6fe921` e questo handoff: run non ancora disponibile alla scrittura.

## §7 RISERVE APERTE

- R-378-1 (BASSA): il prefisso «agent» manda alla firma, dopo una lettura, anche file come `dati/agente_vendite.md` (solo attrito, fail-closed).
- R-379-1 (BASSA): anche una riscrittura identica del lead fa fallire `fida-contatto` (basta rilanciarlo); il messaggio unisce «scheda cambiata» e «degrado DB».
- R-ve224-2 (BASSA/COSMETICA): un carattere invisibile in testa al nome lascia libero «dati/\u200bAGENTS.md».
- R-ve222-4, parte su recapito/chiusura di un lead dopo una lettura (proposta: avviso su Telegram).
- Restano da #222: R-366-1, R-367-2, R-370-2, R-bot222-2, R-ve222-2, R-373-1, R-375-1, R-372-1 (vedi stato_progetto.md).
