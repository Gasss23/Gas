# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-16 — Cultura generale con le proprie conoscenze; knowledge base assente solo nel log

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #216 (https://github.com/Gasss23/Gas/pull/216) — già autorizzato dall'operatore se CI e test sono verdi.

(`gh` non disponibile nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Merge #215**: `FATTA` — `1a979a8`.
- **Cultura generale / dati dell'utente mai inventati**: `FATTA`.
- **Avviso knowledge_fts solo nel log**: `FATTA`.
- **V-1 bot/verifica #215 (metro anti-doppioni)**: `FATTA`.
- **V-2 bot #215 (now_iso_da pubblico)**: `FATTA`.
- **Note bot #216 V-1/V-2/V-3 e verifica esterna #216 V-1/V-2**: `FATTA` — review #357.
- **Secondo giro #216 (V-1 sources.yaml, V-2 metro nel lotto, V-3 corpo PR)**: `FATTA` — review #358.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 gas.py                             |  57 ++++++++++++++++++++++++++++++++++++++++++++++-----------
 modules/memory/__init__.py         |   2 ++
 modules/memory/store.py            |   4 ++++
 reports/diff_sessione.md           |  11 ++++++-----
 reports/handoff.md                 | 199 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  24 ++++++++++++------------
 tests/test_unit_kernel.py          | 163 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 9 files changed, 346 insertions(+), 122 deletions(-)
```

NB: conteggi di `reports/handoff.md` (e totali) presi prima del proprio commit.

## §3 GIT LOG --ONELINE (sessione)

```
d117708 fix(risposte): sources.yaml assente solo nel log; metro anti-doppioni coerente nel lotto (bot #216)
6eee21c chore(revisore): memoria review #358 — APPROVATO
c17ca73 docs(fine-task): report e handoff — note bot e verifica esterna #216
9693680 fix(risposte): note bot e verifica esterna #216 — metro anti-doppioni, knowledge base, log
3984436 chore(revisore): memoria review #357 — APPROVATO
b70e466 docs(fine-task): report e handoff — cultura generale e knowledge base solo nel log (PR #216)
0f55399 feat(risposte): cultura generale con le proprie conoscenze; base di conoscenza assente solo nel log
018abaa chore(revisore): memoria review #356 — APPROVATO
0b5c899 chore(revisore): memoria review #355 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #355 — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md (sezioni 1, 5, 8 e 10), le sezioni pertinenti di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md (#351–#354, compresa la lezione su stato e provenienza delle lezioni). Ho esaminato il diff staged: 4 file, +141/−11.

**Elementi del diff esaminati**

- `gas.py:57` — crea il logger `gas.knowledge` a livello INFO. Rischio esaminato: che l'INFO arrivi lo stesso a schermo, oppure che non arrivi al file. Il gestore della console (`gas.py:38`) resta a WARNING. Il file handler di basicConfig non ha un livello, quindi riceve l'INFO che risale al logger principale. Il livello WARNING del logger principale non filtra i messaggi che arrivano dai logger figli. Esito: ok.
- `gas.py:3302` — «knowledge DB assente» passa da WARNING a INFO. Rischio esaminato: nascondere un guasto reale. È uno stato atteso: la base di conoscenza non è mai stata creata. La funzione restituisce comunque "" senza crash. Esito: ok.
- `gas.py:3343` — solo «no such table» va a INFO, tutti gli altri errori restano WARNING. Rischio esaminato: che il ramo sia troppo largo. Comprende anche il caso di una base caricata a metà (tabella FTS mancante e tabella sorgente presente), che ora finisce solo nel log. È accettabile: resta tracciato in gas_debug.log, come vuole la sezione 9. Prova: togliendo il ramo, solo T92c fallisce; T92d dimostra che «database is locked» resta visibile a schermo. Esito: ok.
- `gas.py:3113` — `_lezione_simile` non usa più come metro le lezioni `proposta` nate da finestre `:non_fidato`. Rischio esaminato: che il filtro stia solo sullo stato e non sulla provenienza (lezione della #354). Qui li combina entrambi, ed è corretto. Le lezioni aggiunte durante la stessa riflessione vengono aggiunte al catalogo: va bene, hanno la stessa sorgente. Mutazione: togliendo il filtro fallisce solo T92e. Esito: ok.
- `gas.py:3117` — il controllo dei doppioni esatti continua a usare tutto il catalogo (`tutte`). Mutazione: usando `catalogo` al suo posto fallisce solo T92g. Esito: ok.
- `gas.py:100` — nuova regola sulla cultura generale nel system prompt. Rischio esaminato: incoraggiare risposte inventate. Esito: riserva (vedi R-355-1).
- `gas.py:957` — la descrizione del tool `ricorda` esclude la cultura generale. Non c'è simulazione di tool: è solo testo di istruzione. Esito: ok.
- `modules/memory/store.py:395` — l'alias pubblico `now_iso_da` punta a `_now_iso_da`. `modules/memory/__init__.py:22` e `modules/memory/__init__.py:42` lo esportano, `gas.py:21` lo importa. Nessun cambio di formato: T90j resta verde e T92h verifica che sia lo stesso oggetto. Esito: ok.
- `tests/test_unit_kernel.py:4720` — T69-fts-d aggiornato. Esito: riserva cosmetica (vedi R-355-2).

**Verifiche eseguite**

- Suite kernel: 887 PASS, 0 FAIL, riprodotti.
- Tre mutazioni, ognuna colta da un solo test: filtro del catalogo → T92e, doppioni esatti → T92g, ramo «no such table» → T92c. gas.py è stato ripristinato e il diff staged è intatto.
- Wall of Shame: nessuno slicing della history, `_get_window` non è toccato, il limite di 10 iterazioni e quello di 8k sull'output non sono toccati, nessuna simulazione di tool.

**Riserve**

- **R-355-1 BASSA** — `gas.py:100`: la frase «Se ricorda non trova nulla … rispondi con ciò che sai» viene subito dopo «Usa ricorda SOLO per le cose dell'utente». Così il ripiego vale proprio per le domande sui lead e sulle azioni passate, dove «ciò che sai» non esiste: Gas potrebbe inventare dati su un lead, anche se con la frase «non viene dalla memoria». Correzione suggerita: limitare il ripiego alla cultura generale, per esempio «Se ricorda non trova nulla su una domanda di cultura generale…», e per le cose dell'utente dire chiaramente che in memoria non risulta.
- **R-355-2 COSMETICA** — `tests/test_unit_kernel.py:4720`: T69-fts-d ora passa con qualsiasi riga che contenga «knowledge», a qualsiasi livello. Che il messaggio sia INFO e non WARNING lo dimostra solo T92c.

**Rischio escluso:** non ho verificato l'effetto reale del nuovo system prompt sui modelli (Gemini, Groq, OpenRouter, Ollama), cioè se ora rispondono davvero alla domanda sulla fotosintesi senza chiamare `ricorda`. Serve una chiamata LLM reale o la prova sul Mac, che in dev non posso riprodurre. Non ho rilanciato `pytest tests/` (1419 dichiarati): ho riprodotto solo la suite kernel.

**Memoria:** riga #355 aggiunta e committata da sola con lo script (commit 0b5c899 sul branch feat/merge-automatico-z1xjx2). Il diff staged sotto review non è stato toccato.

File rilevanti: /home/user/Gas/gas.py, /home/user/Gas/modules/memory/store.py, /home/user/Gas/modules/memory/__init__.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #356 (ri-review dopo R-355-1/2) — verdetto integrale

## VERDETTO: APPROVATO

Ri-review della #355 sul diff staged completo, 4 file (+146/−12). Le due riserve sono chiuse e il resto del diff è uguale a quello della #355.

**Elementi del diff esaminati**

- `gas.py:102` — «rispondi comunque con ciò che sai, dicendo che non viene dalla memoria» ora vale solo «su una domanda di cultura generale». Rischio esaminato: che il ripiego valga ancora per le domande sui dati dell'utente. Esito: ok, R-355-1 chiusa.
- `gas.py:105` — per le cose dell'utente (lead, contatti, azioni passate) la regola dice «non inventare MAI: se ricorda non trova nulla, di' che in memoria non risulta». Rischio esaminato: risposte inventate su un lead. La regola è esplicita e coerente con la sezione 5 (non inventare dati). Esito: ok.
- `tests/test_unit_kernel.py:8991` — T92a controlla anche «non inventare MAI» e «in memoria non risulta». Rischio esaminato: che la regola nuova non sia coperta da nessun test. Esito: ok.
- `tests/test_unit_kernel.py:4720` — T69-fts-d ora richiede proprio «knowledge base assente» e «knowledge_fts». Rischio esaminato: un test che passa con qualsiasi riga del log. Mutazione: togliendo il ramo «no such table» (`gas.py:3343`), falliscono sia T69-fts-d sia T92c, quindi il test ora distingue il messaggio INFO dal WARNING. Esito: ok, R-355-2 chiusa.
- Contesto già approvato nella #355 e controllato di nuovo: `gas.py:3113` (le proposte `:non_fidato` non fanno da metro per i doppioni simili), `gas.py:57` (logger `gas.knowledge` a INFO) e `modules/memory/store.py:395` (alias pubblico `now_iso_da`). Esito: ok.

**Verifiche eseguite**

- Suite kernel: 887 PASS, 0 FAIL, riprodotti.
- Mutazione su `gas.py:3343`: fallisce come atteso. gas.py è stato ripristinato e il diff staged è intatto.
- Wall of Shame: nessuno slicing della history, `_get_window` non è toccato, i limiti non sono toccati, nessuna simulazione di tool.

**Rischio escluso:** non ho verificato come reagiscono i modelli reali al nuovo testo del prompt, cioè se rispondono alla domanda sulla fotosintesi e dicono «in memoria non risulta» su un lead sconosciuto. Serve una chiamata LLM reale o la prova sul Mac, che in dev non posso riprodurre. Non ho rilanciato `pytest tests/`: ho riprodotto solo la suite kernel.

**Memoria:** riga #356 aggiunta e committata da sola con lo script (commit 018abaa sul branch feat/merge-automatico-z1xjx2). Il diff staged non è stato toccato.

Riferimento: il verdetto precedente #355 (APPROVATO CON RISERVE, R-355-1 BASSA, R-355-2 COSMETICA) va riportato nell'handoff insieme a questo.

File rilevanti: /home/user/Gas/gas.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/modules/memory/store.py, /home/user/Gas/modules/memory/__init__.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #357 (note bot e verifica esterna #216) — verdetto integrale

## VERDETTO: APPROVATO

Il diff staged su feat/merge-automatico-z1xjx2 (gas.py e tests/test_unit_kernel.py) chiude le tre riserve del bot #216, che coincidono con le due della verifica esterna #216.

Elementi del diff esaminati:
- gas.py:3117 — nel metro anti-doppioni di `_lezione_simile` una lezione con `:non_fidato` conta solo se è `approvata`. Le altre (proposte, rifiutate, ritirate) senza `:non_fidato` restano nel metro. Rischio esaminato: una rifiutata non fidata che fa scartare lezioni legittime; una ritirata non fidata che esce dal metro. Esito: ok. Uscire dal metro è coerente: dopo il ritiro quel testo non è più fidato, e i doppioni esatti usano ancora tutto il catalogo (`esistenti` costruito su `tutte`). Prova: se riammetto la rifiutata nel metro, T92e2 FALLISCE (tests/test_unit_kernel.py:9083). T92e3 (tests/test_unit_kernel.py:9092) conferma che un'approvata nata non fidata fa ancora da metro.
- gas.py:3350 — il ramo INFO scatta solo con «no such table: knowledge_fts». Rischio esaminato: il messaggio reale di SQLite potrebbe essere diverso (prefisso `main.`, ordine delle tabelle). Esito: ok. Ho verificato con sqlite3 la stessa query JOIN: DB vuoto → «no such table: knowledge_fts»; c'è solo `knowledge` → «knowledge_fts»; c'è solo `knowledge_fts` → «no such table: knowledge». Quindi un DB rotto resta WARNING. Prova: se rimetto il match generico «no such table», T92d2 FALLISCE (tests/test_unit_kernel.py:9058).
- gas.py:3312 — una query senza token di almeno 3 caratteri ora scrive INFO su `_knowledge_log` invece di un warning. Rischio esaminato: perdere un segnale di guasto. Esito: ok. Non è un guasto, la funzione ritorna comunque `''` (fail-safe §9) e T92d2 controlla che la riga finisca nel file di log e non sulla console.
- gas.py:101 — la regola sulla cultura generale non dice più «senza tool». Ora dice di usare ricorda anche per le conoscenze caricate dall'operatore e di consultarle prima. «Non inventare MAI» e «in memoria non risulta» sulle cose dell'utente restano (chiusura R-355-1 intatta). Rischio esaminato: tornare a spingere il modello a inventare sui lead. Esito: ok. La descrizione di ricorda (gas.py:959) è allineata; T92a e T92b sono aggiornati.

Antipattern: niente slicing della history, niente output dei tool simulati. `_get_window`, il tetto di 10 iterazioni e il tetto di 8k caratteri non sono toccati. Ho rieseguito tests/test_unit_kernel.py: 890 PASS, 0 FAIL. Le mutazioni le ho fatte su una copia nello scratchpad, il working tree è intatto.

Nota cosmetica, non è una riserva: per un'altra review di processo, se è il caso, riguardare `_c92_prima` in tests/test_unit_kernel.py, che viene riassegnato dopo la query corta. T92c (tests/test_unit_kernel.py:9054) ora controlla la console dopo due chiamate e non più dopo una sola. È innocuo, anzi più severo.

Rischio escluso: non ho verificato l'effetto reale della nuova regola sul comportamento dei modelli runtime (Gemini, Groq ecc.), cioè se ora consultano davvero ricorda prima sulle conoscenze caricate. Il test prova solo il testo del prompt; il comportamento si può verificare solo con un LLM vivo, non in dev.

Non ho eseguito `pytest tests/` (1419 passed è un dato dichiarato dall'agente): ho riprodotto solo la suite kernel.

Memoria: ho aggiunto la riga #357 in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata (3984436, «chore(revisore): memoria review #357 — APPROVATO»). Lezione nuova: un match sul testo di un errore SQLite va reso preciso fino al nome della tabella e verificato coi messaggi reali, non a memoria.

### Review #358 (secondo giro note #216) — verdetto integrale

## VERDETTO: APPROVATO

Diff staged esaminato: 2 file, +24 −1. SHA-256 di `git diff --cached`: edfd6a945e8fae3471e2187a308f368354c50147910f985c5f6e56182a2dda42.

**Elementi del diff esaminati**
- `gas.py:3327`: in `_knowledge_search` il ramo `except FileNotFoundError` scrive una riga INFO su `_knowledge_log` (gas.knowledge) e restituisce "". Rischi esaminati:
  - Quest'eccezione potrebbe nascondere guasti veri: no. Cattura solo il file o la cartella `knowledge/` assenti. `IsADirectoryError`, `PermissionError` e gli errori di YAML non sono `FileNotFoundError`, quindi finiscono nel ramo WARNING generico (`gas.py:3331`).
  - L'ordine degli `except` è corretto e il comportamento resta fail-safe (§9): restituisce sempre "" e non crasha mai.
  - Esito: ok.
- `gas.py:3143`: nella riflessione, `catalogo.append` della lezione appena creata avviene solo `if not contaminata`. Rischi esaminati:
  - Coerenza con il filtro del catalogo (`gas.py:3117`): una proposta non fidata non fa da metro, e qui vale la stessa regola.
  - I doppioni esatti restano bloccati, perché `esistenti.add` è ancora incondizionato.
  - Il tetto `RIFLESSIONE_MAX_LEZIONI` limita la crescita dei quasi-doppioni in una finestra ostile, che comunque richiedono l'approvazione umana.
  - Esito: ok. Il trade-off (possibili quasi-doppioni in coda contro un input ostile che fa scartare una lezione legittima) è quello giusto.
- `tests/test_unit_kernel.py:9033`: T92d3 rinomina `sources.yaml` e poi lo ripristina. Controlla che la riga sia nel log e non in console, anche dentro T92c, perché `_c92_prima` viene ricalcolato dopo il passo (2b). Esito: ok, con una nota cosmetica: il ripristino non sta in un `finally`, ma `_knowledge_search` non solleva eccezioni.
- `tests/test_unit_kernel.py:9103`: T92e4 usa una finestra contaminata con `_L6e` e `_L9e` e si aspetta che entrino entrambe. Esito: ok.
- Contesto: `gas.py:57`: il logger gas.knowledge è a livello INFO e propaga al root, quindi la console (a WARNING) non mostra la riga. Esito: ok.

**Verifica eseguita**
- Kernel: 892 PASS, 0 FAIL, riprodotti.
- Mutazioni:
  - Tolto `if not contaminata` (sempre append): fallisce solo T92e4.
  - Tolto il ramo `FileNotFoundError`: falliscono T92c e T92d3.
- Ho ripristinato `gas.py` dopo le mutazioni: il working tree è uguale all'index.
- Wall of Shame: nessuno slicing della history e nessuna simulazione di tool. `_get_window`, il cap di 10 iterazioni e il cap di output non sono toccati.

**Note cosmetiche (non riserve)**
- Nessun test prova che un `sources.yaml` malformato resti WARNING.
- Il rename/ripristino in T92d3 non è in un `finally`.

**Rischi esclusi**
- Non ho rieseguito `pytest tests/` completo (1419 passed dichiarato dall'agente): il diff tocca solo `gas.py` e la suite kernel, che ho riprodotto per intero.
- Non ho verificato il comportamento sul Mac o sul VPS con un `sources.yaml` reale assente: non è riproducibile in dev oltre il test.
- Non ho verificato V-3 (il corpo della PR), che è fuori dal diff.
- Ho accettato V-4 (`gas_identity.md` invariato) sulla parola dell'agente: il file non è nel diff.

**Memoria**: aggiunta la riga #358 in `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata da sola con `scripts/commit_memoria_revisore.sh` (commit 6eee21c). Il diff staged è rimasto intatto. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 879 → 892 PASS, 0 FAIL (T92a–h, T92d2, T92d3, T92e2, T92e3, T92e4; T69-fts-d aggiornato: ora si aspetta la riga INFO). Blocco reale: `=== RIEPILOGO: 892 PASS, 0 FAIL ===`. In CI i conteggi sono +2 (test del profilo sandbox saltati in locale).
pytest `tests/`: `1419 passed in 177.60s (0:02:57)` (sul codice finale, prima del commit).

## §6 STATO CI

`gh` non disponibile nella sessione cloud: lo stato CI si legge dai check-run della PR via MCP GitHub.

- `0b5c899`, `018abaa`, `0f55399`: pushati insieme prima dell'apertura della PR #216; nessuna run su questi SHA singolarmente.
- `b70e466` (primo fine-task): unit-suite, handoff-check e verifica-bot success (bot APPROVATO CON RISERVE, nessuna ALTA/MEDIA); verifica esterna APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/216#issuecomment-6217839029)).
- `3984436`, commit delle note #216, `c17ca73` (secondo fine-task): CI verde, bot APPROVATO CON RISERVE (V-1 BASSA, V-2/V-3 COSMETICHE); verifica esterna APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/216#issuecomment-6218056959)).
- `6eee21c`, commit del secondo giro e commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- COSMETICHE #358: nessun test per sources.yaml malformato; rename in T92d3 senza finally.
- Effetto reale del nuovo prompt sui modelli non verificato: da riprovare sul Mac (fotosintesi; lead inesistente → «in memoria non risulta»).
- Già tracciate: R-ve215-1 (somiglianza per parole), COSMETICHE #353/#354, R-345-3, R-bot210-3, R-bot211-2, R-ve211-1/2, R-ve213-3.
