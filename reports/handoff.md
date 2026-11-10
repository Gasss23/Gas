# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — Analisi notturna di Gas e correzioni dei bug riprodotti (M1, PR #366)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #366 (https://github.com/Gasss23/Gas/pull/366). Numero e URL dall'output di `create_pull_request` dello strumento GitHub (gh assente in questo ambiente). Tocca il messaggio di firma (solo la vista): PR di sicurezza.
2. Kernel B4 (§8): avviso quando risponde un cervello di riserva? sì/no.
3. Tetto delle 10 iterazioni per turno invece che per cervello? sì/no.
4. Nome dei lead nel promemoria della memoria verso i modelli gratuiti: bloccarlo? sì/no.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Merge notturni con il sì dell'operatore**: FATTA — #362, #361, #364 mergiate; #363/#365 affidate a M2 (conflitti dopo #364).
- **Fetta 2 — Analisi notturna (4 agenti)**: FATTA — 19 bug riprodotti, `reports/test_mattina.md`.
- **Fetta 3 — Fix motore/memoria/conoscenza/notte/bot**: FATTA — d9346212, review #744-M1.
- **Fetta 4 — Merge di origin/main (#361, #364)**: FATTA — 81c3c55c, review #748-M1.
- **Fetta 5 — Bot #366 V-1/V-2/V-3**: FATTA — 69c26619 (review #749-M1) + questo handoff.
- **Fetta 6 — Bug della voce B1–B5**: DEFERITA — affidati a M2 (sua area, PR #365 aperta sugli stessi file).
- **Fetta 7 — Kernel B4–B6**: DEFERITA — decisioni dell'operatore (§0).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md      |   4 ++++
 gas.py                                  |  64 +++++++++++++++++++++++++++++++++++++++++++++++++----------
 modules/notte/notte.py                  |   6 +++---
 modules/telegram/bot.py                 |  13 +++++++++---
 reports/diff_sessione.md                |  24 +++++++++++------------
 reports/handoff.md                      | n/d
 reports/proposta_terminale_autonomia.md |  28 ++++++++++++++++++++++++++
 reports/ripartenza_m1.md                |  70 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md               |   2 ++
 reports/test_mattina.md                 | 308 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/test_voce_mattina.md            |  53 +++++++++++++++++++++++++++++++++++++++++++++++++
 reports/ultimo_report.md                |  30 ++++++++++++++--------------
 tests/test_unit_ingest_fonti.py         |  89 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_kernel.py               | 192 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 tests/test_unit_notte.py                |  61 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tools/ingest_knowledge.py               | 104 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
69c26619 fix(ingest): exit 1 se una fonte fallisce (bot #366 V-3) + id review #744-M1/#748-M1 (bot #366 V-2)
81c3c55c merge: origin/main (#361, #364) nel branch dei fix dell'audit notturno (review #748 APPROVATO)
fd6c2425 docs(m1): test del mattino dall'analisi notturna
844e79aa docs(stato): audit 2026-11-10 — kernel B4-B6 annotati, riserve R-744-1..4
d9346212 fix(audit 2026-11-10): kernel, memoria/conoscenza, notte/bot — bug riprodotti dall'audit notturno
aefb15c7 chore(revisore): memoria review #744 — APPROVATO CON RISERVE
39098377 docs(m1): stato notte 10/11 (merge #362, audit notturno)
4d8dcdd6 Merge remote-tracking branch 'origin/main' into feat/merge-automatico-z1xjx2
e8f7a3ec docs(m1): tutte le chat lavorano in parallelo
34eede56 docs(m1): nuove chat M3 (R7) e M4 (R1), lavoro in parallelo
cfb09cb3 docs(m1): ripartenza dopo /clear — stato al 10/11 e regola delle risposte brevi
22e70e44 docs(m1): tolte le copie di sicurezza delle patch di M2 (R8 mergiata in #358)
3fcdd9ec docs(m1): decisioni del 9/11 mattina (#356, #357, thread b, R8, terminale A)
9c770ee0 docs(m1): aggiornamento notturno dei test voce del mattino
f9fd5521 docs(m1): copia di sicurezza della patch velocità di M2
06a3ef78 docs(m1): copia di sicurezza della patch R8 fetta 1 di M2 (lavoro locale non pushabile)
02e7e076 docs(m1): proposta terminale e autonomia (azioni fisse per Gas, poi strada B)
c4250b86 docs(m1): sospesa la regola notturna di merge con riserve (V-1 MEDIA #357)
280b2f95 docs(m1): piano dei test voce del mattino e decisioni della notte del 9/11
e928846e docs(m1): sì a #352/#353, risposta vocale solo su vocale, stato Remote Control
49a26c72 docs(m1): sì a #350 e #351, vocali Telegram opzione A
8d1f6d91 docs(m1): sì dell'operatore a #348, #349 e voce via Telegram (opzione B)
91a4739b docs(m1): decisioni del 7/11 — merge #346/#347, niente «Hey Gas», proposta voce Daniel
abe75db7 docs(m1): ripartenza M1 compatta per /clear (stato 7 nov, decisioni, prossimi passi)
7b901438 docs(m1): promemoria dell'operatore (prova roadmap a voce, accesso al terminale) e stato #339/#341
9400296e docs(m1): pausa a voce come fine conversazione, finestra 40 s, difese contro le risposte per sbaglio
37deeace docs(m1): merge #333/#334/#336 e ordine delle fette voce e bot
1acb9294 docs(m1): decisioni dell'operatore sulla voce (interruzione, velocità, storia unica)
f59c66e2 docs(m1): esito prova Jarvis sul Mac, tempi e misura avvio claude -p
12a494a1 docs(m1): #332 mergiata
2ec42656 docs(m1): stato #332
ac79e75c docs(m1): nuove sessioni M2 e Mani
7f34c387 docs(m1): ripartenza aggiornata (#331)
a72c2fa2 docs(m1): ripartenza aggiornata (#329)
f5e0af34 docs(m1): ripartenza aggiornata (#331)
19cd69bb docs(m1): ripartenza della chat di coordinamento al 3 novembre
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #744-M1 (commit d9346212; numerata «#744» nel testo originale, rinominata per collisione con #744 di M3 — bot #366 V-2)

## VERDETTO: APPROVATO CON RISERVE

Review #744. Ho controllato il diff staged del branch `feat/merge-automatico-z1xjx2`: 7 file di codice e test, nessuno dei file proibiti dal Wall of Shame.

**Cosa ho rifatto io:** ho estratto l'index in una cartella a parte con `git checkout-index`, senza usare stash.
- Suite del kernel: 1109 PASS, 0 FAIL.
- Test di ingest e notte: 212 passed.
- `git diff --staged --check` pulito.
- Ho scritto 3 mutanti miei (versioni del codice col fix tolto) e i test li hanno presi tutti:
  - B3 compressione: torna `start = 0`, fallisce T110c.
  - B4 bot: il controllo del messaggio modificato diventa `if False`, fallisce `test_giro_da_messaggio_modificato_non_parte`.
  - B1 ingest: il «superseded» per i chunk in più non scatta più, fallisce `test_fonte_accorciata_supera_i_chunk_vecchi`.

**Elementi del diff esaminati**
- `gas.py:1582`: per B3, quando negli ultimi messaggi non c'è un user, tiene il turno intero partendo dall'ultimo user di `old`. Rischio esaminato: taglio cieco della storia e tool rimasti orfani. Il taglio avviene su un confine `user`, non su un indice fisso, quindi la finestra parte sempre da un user e il tool resta col suo assistant. Una storia fatta di un solo turno restituisce False. Esito: **ok**.
- `gas.py:1858`: `_utf8_sicuro` (definito a `gas.py:928`) ripulisce contenuto e argomenti delle chiamate, cambiando i surrogati isolati in «?». Rischio: altre strade per scrivere nella storia. Esito: **riserva** (R-744-1).
- `gas.py:935`: `_forma_storia_valida` è usata nel caricamento (`gas.py:1294`), che mette in quarantena e riparte da storia vuota, nell'unione con l'altro processo (`gas.py:1362`) e nel doctor (`gas.py:5447`), che dà FAIL e mette `history = None` così il controllo dei tool orfani viene saltato. Esito: **ok**, con una riserva BASSA (R-744-2).
- `tools/ingest_knowledge.py:237`: i chunk attivi oltre la nuova lunghezza della fonte diventano `superseded` e non vengono mai cancellati, prima del commit della fonte. Esito: **ok**.
- `tools/ingest_knowledge.py:113`: `chunk_text` avanza sempre: la parte tagliata ha almeno 1 carattere e non può essere vuota dopo `strip`, anche con tetto 1. Esito: **ok**.
- `tools/ingest_knowledge.py:272`: `ingest_fonti` fa il rollback di una fonte rotta e passa alla successiva; nel log va solo il tipo dell'eccezione. Esito: **ok**.
- `gas.py:4499`: nella ricerca nella conoscenza `break` diventa `continue`. Il numero di righe resta limitato dal `LIMIT` della query e il tetto di caratteri resta. Esito: **ok**.
- `modules/telegram/bot.py:235`: `rendi_visibili` agisce solo sul testo mostrato, non su hash o argomenti eseguiti (lo conferma T112b). Esito: **ok**.
- `modules/telegram/bot.py:884`: `/notte` e `/compito` da un messaggio modificato vengono rifiutati come `/clear`, prima di `lancia_giro`. Esito: **ok**.
- `modules/notte/notte.py:928`: `_stampa_sicura` non solleva eccezioni. Esito: **ok**.
- `gas.py:118`: `_campo_pin` è capato a 200 caratteri. Un taglio in mezzo a «&lt;» non può creare un tag. Esito: **ok**.

**Finding**
1. **R-744-1, BASSA**: `gas.py:3575`, il blocco aggiunto alla storia dopo una firma (output del tool e argomenti) usa `history.extend` e non passa da `_utf8_sicuro`. `_save_history` usa `ensure_ascii=False`, quindi un surrogato nell'output di un'azione firmata può ancora far fallire il salvataggio. Il fallimento è gestito (§9), ma il bug B1 lì resta aperto.
2. **R-744-2, BASSA**: `_forma_storia_valida` non controlla `tool_calls`. Un elemento che non è un dizionario, o che non ha `id`, fa ancora sollevare `tc["id"]` nel doctor. È un caso più stretto di B2.
3. **R-744-3, BASSA**: una fonte il cui file è sparito o il cui uri viene rifiutato esce prima del passaggio a `superseded`, quindi i suoi chunk vecchi restano attivi.
4. **R-744-4, COSMETICA**: il log «Cronologia compressa» calcola `len(old)+keep_msgs`, che è sbagliato quando B3 sposta il turno da `old` a `recent`.

**Coerenza col progetto:** tutto va nella direzione «zero crash». Nessuna simulazione di tool e nessun taglio della storia con `[-N:]`. `_get_window`, il tetto di 10 iterazioni e il tetto dell'output non sono toccati.

**Cosa NON ho verificato:**
- I 33 test di `tests/test_unit_web_browser.py` e i 5 SKIP del kernel, perché nel container mancano bwrap ed embedding.
- Una `.gas_history.json` reale dell'operatore, che nel container non c'è: non ho potuto provare che una storia vera esistente supera il nuovo controllo di forma, quindi il rischio di quarantena di una storia legittima è escluso solo in teoria.
- L'ingest su una knowledge reale: una sola volta, i paragrafi lunghi già presenti verranno rispezzati e quindi rimarcati `superseded` e reingeriti.

Le riserve vanno tracciate in `reports/stato_progetto.md`. Ho aggiunto la riga #744 e una lezione nuova in `.claude/agents/memoria_revisore.md`, committata da sola (aefb15c7). Nessun altro file è stato modificato.

### Review #748-M1 (merge 81c3c55c; «#748» nel testo originale)

## VERDETTO: APPROVATO

Review #748: merge staged di origin/main eebb7c0 (PR #361 e #364) nel branch feat/merge-automatico-z1xjx2, sopra i fix dell'audit notturno d9346212 (review #744). Il merge è giusto: nessuna riga persa, i due lati convivono e i test passano.

Elementi del diff esaminati:
- `gas.py:928` — `_utf8_sicuro` (fix B1 della #744) e `gas.py:935` `_forma_storia_valida` (fix B2): dopo il merge sono presenti e invariati. Il rischio era che il merge automatico perdesse una parte dei fix o delle modifiche di #364. Ho confrontato le righe aggiunte e tolte nei due sensi:
  - quelle di HEAD rispetto alla base sono uguali a quelle dell'index rispetto a MERGE_HEAD;
  - quelle di MERGE_HEAD rispetto alla base sono uguali a quelle dell'index rispetto a HEAD.
  - Esito: ok, entrambi i lati sono intatti.
- `gas.py:5258` — campo `"nome": tc.function.name` aggiunto all'evento `tool_res` (#364, progressi R7). Il rischio era un'interazione con i filtri della storia della #744. È solo un campo dell'evento: non scrive in `self.history` e non passa dalla finestra. Nessuno slicing della storia, nessun output di tool simulato. Esito: ok.
- `gas.py:6507` — comando `sottofondo-ferma` nel main (bot #364 V-1). È una parte isolata e non entra in conflitto con i fix della #744. Esito: ok.
- `tests/test_unit_kernel.py:1` — test fusi in automatico. Il confronto nei due sensi è pulito: ci sono sia i test T110c/T112b della #744 sia quelli della #364. L'ho rilanciato: 1113 PASS, 0 FAIL. Esito: ok.
- `reports/stato_progetto.md:380` — unione del conflitto:
  - rispetto a MERGE_HEAD nessuna riga tolta;
  - rispetto a HEAD è sparita 1 riga, quella della PR #359. È sostituita dalla versione aggiornata di main («PR #359 MERGIATA 695b759»): sostituzione voluta, non una perdita.
  - Le riserve R-744-1..4 (`reports/stato_progetto.md:379`) e la nota sull'audit (`reports/stato_progetto.md:378`) sono ancora presenti.
  - Esito: ok.
- `.claude/agents/memoria_revisore.md:1437` — unione del conflitto: nessuna riga tolta né rispetto a HEAD né rispetto a MERGE_HEAD. Esito: ok.

Controlli generali:
- Tutti i file che HEAD non tocca (`modules/gate/gate.py`, `modules/sottofondo/__init__.py`, `clients/voice/ascolto.py` e i loro test) nell'index sono identici a MERGE_HEAD.
- `git ls-files -u` è vuoto, non ci sono marcatori di conflitto e `git diff --cached --check` è pulito.
- Ho rilanciato `tests/test_unit_gate.py` e `tests/test_unit_sottofondo.py`: 944 passed.

Rischio escluso: non ho rilanciato da me le suite notte, ingest e telegram_voce (1227 passed secondo l'agente). Il merge non tocca in modo nuovo i loro file: `modules/notte/notte.py`, `modules/telegram/bot.py` e `tools/ingest_knowledge.py` vengono solo da HEAD, già approvati nella #744, e sono uguali a HEAD. Non ho verificato nemmeno il comportamento con processi veri (flock, kill dei figli): già dichiarato non provato in #364 e non riproducibile qui.

Riserve: nessuna nuova. Restano aperte quelle già tracciate in `reports/stato_progetto.md`: R-744-1..4 e quelle della #364.

Memoria: ho aggiunto la riga contatore #748 in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` (nessuna lezione nuova) e l'ho messa in stage con `git add`, senza commit, come richiesto. Durante il merge lo script di commit della memoria non va lanciato: la riga entra nel commit di merge.

### Review #749-M1 (commit 69c26619)

## VERDETTO: APPROVATO CON RISERVE

Review #749-M1. Diff staged sul branch feat/merge-automatico-z1xjx2 (PR #366), 4 file. Ho letto: CLAUDE.md, stato_progetto.md (riga 379) e la coda di memoria_revisore.md.

**Righe del diff controllate**
- `tools/ingest_knowledge.py:361` — quando `totale["errori"] > 0` il programma esce con `sys.exit(1)`. Questo avviene dopo `conn.close()` e dopo il log del TOTALE. Rischi controllati:
  - perdita delle fonti buone: no, `ingest_fonti` (tools/ingest_knowledge.py:272) fa il commit per fonte, e con un errore annulla solo la fonte rotta;
  - chiamanti che si aspettano exit 0: no. `tests/e2e/e2e_k3k4_llm.py:97` controlla il codice 0 su fonti sane, quindi è coerente. `gas.py:4478` cita lo script solo in un commento. La modalità `--dry-run` resta con `return`.
  - Esito: ok.
- `tests/test_unit_ingest_fonti.py:113` — test parametrizzato con due casi: tutte le fonti ok → `main()` finisce senza uscire; c'è una fonte che è una cartella (`knowledge/manca/`) → `SystemExit` con codice 1. Ho provato il mutante da solo: tolto l'exit, il test dà «1 failed, 14 passed». Col fix: 15 passed. File ripristinato, nessuna modifica rimasta fuori dallo stage. Esito: ok.
- `reports/stato_progetto.md:379` — rinomina in #744-M1 e R-744-M1-1..4. Annotate la chiusura di bot #366 V-3 e la riserva ve #366 V-3. Coerente. Esito: ok.
- `.claude/agents/memoria_revisore.md:1437` e `.claude/agents/memoria_revisore.md:1442` — rinomina in #744-M1 e #748-M1. Le voci R-744-1/2 rimaste a `.claude/agents/memoria_revisore.md:1425` e `.claude/agents/memoria_revisore.md:1427` sono di M3, quindi è giusto non toccarle. Esito: ok.

**Riserva**
- R-749-M1-1 (cosmetica): nel caso con la fonte rotta il test non controlla che la fonte «ok» sia davvero nel DB. La promessa «le altre restano caricate» non è verificata da questo test. Basta una query sul DB prima o dopo il `SystemExit`.

**Cosa non ho verificato**
- Non ho lanciato l'e2e `tests/e2e/e2e_k3k4_llm.py`: usa un LLM vero. Ho controllato solo che la sua aspettativa (rc 0) resti valida con fonti sane.
- Non ho controllato il comportamento sulla VPS.

**Memoria**
- Ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga `#749-M1 — 2026-11-10 — APPROVATO CON RISERVE — ...` e l'ho messa in stage con `git add`.
- Come mi hai chiesto, NON ho committato: non ho lanciato `scripts/commit_memoria_revisore.sh`.

## §5 DELTA TEST DEL MOTORE

- Kernel: 1100 PASS / 0 FAIL (main prima dei fix) → 1113 PASS / 0 FAIL (dopo fix + merge di #361/#364). Verifica esterna: i test nuovi sul codice di main danno 1106 PASS / 7 FAIL (T110a, T110b, T110c, T111a, T111b, T111, T112a).
- pytest notte+ingest_fonti+sottofondo+gate+telegram_voce: 1227 passed (`python -m pytest -q tests/test_unit_notte.py tests/test_unit_ingest_fonti.py tests/test_unit_sottofondo.py tests/test_unit_gate.py tests/test_unit_telegram_voce.py`); ingest_fonti 15 passed dopo V-3 (14 passed + 1 failed col mutante).

```
=== RIEPILOGO: 1113 PASS, 0 FAIL ===
```

Fuori scope: 5 SKIP del kernel (T13a/b/c/e, T30e) e i 33 fallimenti di tests/test_unit_web_browser.py nel container (mancano bwrap e il modello di embedding; la CI li installa).

## §6 STATO CI

CI NON VERIFICATA (gh assente) con `gh run list`; check run letti con lo strumento GitHub sulla PR #366:
- 81c3c55c: handoff-check **failure** (handoff mancante: è il bot #366 V-1, chiuso da questo commit); unit-suite in_progress; verifica-bot **failure** (V-1 MEDIA, chiuso qui).
- 69c26619: nessuna run su questo SHA (pushato insieme al commit di fine-task; testato solo dall'albero del commit di testa).
- Commit precedenti della sessione (fd6c2425, 844e79aa, d9346212, aefb15c7, 39098377, 4d8dcdd6 e i docs(m1)): nessuna run propria con PR; il loro contenuto è testato dalla run di 81c3c55c e poi da quella del commit di fine-task.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-744-M1-1 BASSA — `history.extend` dopo una firma non passa da `_utf8_sicuro`.
- R-744-M1-2 BASSA — `_forma_storia_valida` non controlla `tool_calls`.
- R-744-M1-3 BASSA — fonte con file sparito/uri rifiutato tiene attivi i chunk vecchi.
- R-744-M1-4 COSMETICA — log «Cronologia compressa» con conteggio sbagliato.
- R-749-M1-1 COSMETICA — il test di V-3 non controlla che la fonte buona sia nel DB.
- Ve #366 V-3 BASSA — un solo turno lungo (ultimo_user==0) non viene mai compresso.
- Ve #366 V-4 COSMETICA — comando del «1227 passed» ora indicato in §5.
- Kernel B4/B5/B6 non implementati (decisioni in §0).
