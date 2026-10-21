# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 (dopo il merge di #236) — ultime riserve del bot sulla storia condivisa

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #240 (https://github.com/Gasss23/Gas/pull/240; numero e URL dall'API GitHub): pro e contro in `reports/da_mergiare.md`; l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10).

---

## §1 SCOPE & ESITO FETTE

- **Merge PR #236**: `FATTA` — su richiesta dell'operatore, merge `dec4ce9`.
- **V-1/V-2 bot #236 (5° giro), R-436-1**: `FATTA` — review #438 APPROVATO CON RISERVE.
- **R-438-1, R7 / R-c4b3-3**: `DEFERITA` — prossime fette.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 gas.py                             |  29 +++++++++++++++---------
 reports/da_mergiare.md             |  18 +++++----------
 reports/diff_sessione.md           |  12 +++++-----
 reports/handoff.md                 | 442 +++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  24 ++++++--------------
 tests/test_unit_kernel.py          |  52 ++++++++++++++++++++++++++++++++++++++++--
 8 files changed, 134 insertions(+), 446 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
340326d fix(storia): rinvio a fine turno anche al primo salvataggio, niente duplicati dopo una scrittura fallita, test del finally di run_turn (V-1/V-2 bot #236 5° giro, R-436-1)
012856e chore(revisore): memoria review #438 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #438 (chat Motore) — commit 340326d

## VERDETTO: APPROVATO CON RISERVE

Review #438 (chat Motore). Ho controllato il diff in staging su gas.py e tests/test_unit_kernel.py. Prima ho letto CLAUDE.md, le parti di stato_progetto.md che riguardano la storia e la coda della mia memoria.

**Punti del diff esaminati**
- gas.py:1188 — il rinvio a metà turno («unita is not None and not _turno_chiuso() and not fine_turno») ora vale per entrambi i rami. Rischio esaminato: il rinvio blocca per sempre la scrittura. Ho controllato chi chiama `_save_history`:
  - `_storia_esito_firma` (gas.py:3231) chiude sempre con «Preso atto», senza tool_calls, quindi non viene mai rinviato.
  - Le due chiamate dentro il loop di run_turn (gas.py:4538 e gas.py:4542) e la compressione a inizio turno (gas.py:4318) sono coperte dal finally (gas.py:4578).
  - L'unico chiamante fuori da run_turn è la CLI `compress-history` (vedi R-438-1).
  - Esito: ok.
- gas.py:1176 — il dedupe `suoi = altrui[gia[0]:]` scatta solo se il file dell'altro estende quello già unito (lunghezza e hash). Rischi esaminati:
  - Il ramo 1 dopo un'unione del ramo 2 duplicherebbe i suoi messaggi: è irraggiungibile, perché `nuovi[0]` resta lo stesso messaggio non-user e `nuovi` vuoto porterebbe già al ramo 1.
  - `gia[0] < n_base` non può succedere per costruzione.
  - Esito: ok.
- gas.py:1202 e gas.py:1302 — la base ha il 5° elemento solo dopo un'unione del ramo 2, e `_sync_storia()` lo azzera dopo una scrittura riuscita. Sonda nella copia:
  - lunghezza della base 5 dopo la scrittura fallita, 4 dopo quella riuscita;
  - poi A scrive e B è a metà turno: rinvio attivo, B non vede A2;
  - a fine turno il file è `['B extra','A1','rA1','A2','rA2','B q',None,'7','rB']`, senza duplicati, con flag False.
  - Esito: ok.
- gas.py:952 — l'annotazione `Optional[Tuple[Any, ...]]` è coerente con le tuple da 4 e da 5 elementi. Esito: ok.
- tests/test_unit_kernel.py:7603 — T97j passa davvero dal generatore di run_turn: il bot scrive durante la prima chiamata, poi il provider va giù. Ho rifatto le mutazioni nella copia nello scratchpad:
  - finally tolto → T97j FAIL;
  - rinvio solo nel ramo 2 → T97j FAIL;
  - dedupe tolto → T97k FAIL;
  - 5° elemento mai scritto → T97k FAIL (tests/test_unit_kernel.py:7646).
  - Esito: ok, R-436-1 chiusa.
- tests/test_unit_kernel.py:7489 e tests/test_unit_kernel.py:7655 — T97b e T97g ora chiudono i turni di A con una risposta. È un adeguamento coerente con la nuova regola, non un indebolimento. Esito: ok.

**Suite nella copia:** kernel 993 PASS, 1 FAIL. Il FAIL è T79a ed è dovuto alla copia: senza `git ls-files` trova 0 file. Non dipende dal diff.

**Riserve**
- **R-438-1 BASSA (c'era già prima di questo diff):** `python gas.py compress-history` (gas.py:5230) gira fuori da run_turn. Se la storia finisce a metà turno (turno precedente esaurito) e un altro processo ha scritto, il salvataggio viene rinviato e nessun finally lo recupera. La compressione non viene scritta, ma il comando stampa lo stesso «Compressi N messaggi». Non si perdono dati: sul file resta la storia intera. Il caso c'era già col rinvio del ramo 2 (compressione → nostri non da base → ramo 2). Correzione proposta: chiamare `_save_history(fine_turno=True)` in quel comando, oppure controllare `_storia_rimandata` prima di stampare.
- **R-438-2 (nota, scelta accettabile):** col rinvio anche nel ramo 1, se un altro processo ha scritto, i messaggi del turno in corso restano solo in memoria fino alla fine del turno. Un kill -9 a metà turno li perde, mentre prima venivano scritti a ogni passo dei tool. È il prezzo di «il modello non vede il blocco dell'altro durante il turno»: va dichiarato in stato_progetto.md.

**Cosa NON ho verificato:** due processi reali in parallelo con il lock vero su VPS e il bot Telegram vivo, perché in dev non si riproduce (le prove usano due kernel nello stesso processo). Non ho rilanciato pytest tests/ (1816): ho girato solo la suite kernel e le mutazioni.

La riga #438 è stata scritta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con scripts/commit_memoria_revisore.sh. Lo staging di gas.py e tests/test_unit_kernel.py è intatto.

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py: 992 → 994 PASS, 0 FAIL (T97j, T97k). Blocco reale: `=== RIEPILOGO: 994 PASS, 0 FAIL ===`.
pytest `tests/`: 1816 passed.

## §6 STATO CI

- dec4ce9 (merge di #236 su main): CI di main non letta da qui.
- 012856e, 340326d: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-438-1 (BASSA): `gas compress-history` con unione rimandata stampa «Compressi» senza scrivere (nessuna perdita).
- R-438-2 (nota dichiarata): con un altro processo che ha scritto, i messaggi del turno in corso restano in memoria fino alla fine del turno; un kill -9 a metà turno li perde.
- Riserve precedenti: vedi `reports/stato_progetto.md`.
