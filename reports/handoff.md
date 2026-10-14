# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-14 — G-3 fase 2: blocco del merge automatico col token sbagliato

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #207 (https://github.com/Gasss23/Gas/pull/207): tocca la macchina di controllo, decide l'operatore.
2. Sostituire sul Mac l'alias `gasclaude` con la versione fail-safe (comando fornito in chat).

(`gh` non disponibile nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **`--blocco` in avviso_token_admin.sh**: `FATTA`.
- **`gasmerge --auto` blocca**: `FATTA`.
- **Doc (CLAUDE.md, setup, stato)**: `FATTA`.
- **Bot #207 su 58632e1 V-1 (MEDIA)**: `FATTA` — `OK` inizializzata, test con OK=1 nell'ambiente; V-2 (doc) e V-3 (test script assente) `FATTA`.
- **Verifica esterna #207** ([commento](https://github.com/Gasss23/Gas/pull/207#issuecomment-6173200160), APPROVATO CON RISERVE): V-1 MEDIA = bot V-1, già chiusa; V-2 (BASSA, argomento sconosciuto) `FATTA` (review #341); V-3 (BASSA, blocco solo su `gasmerge --auto`) e V-4 (COSMETICA, messaggio) tracciate.
- **Alias fail-safe**: `DEFERITA` — sul Mac, lo fa l'operatore.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 CLAUDE.md                          |   2 +-
 reports/diff_sessione.md           |  10 ++++++----
 reports/handoff.md                 | 152 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------
 reports/setup_agente_non_admin.md  |   8 ++++----
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  29 ++++++++++++++---------------
 scripts/avviso_token_admin.sh      |  19 ++++++++++++++++---
 scripts/gasmerge.sh                |  10 ++++++++--
 tests/test_unit_gasmerge.py        |  98 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 10 files changed, 266 insertions(+), 71 deletions(-)
```

NB: conteggi di `reports/handoff.md` (e totali) presi prima del proprio commit.

## §3 GIT LOG --ONELINE (sessione)

```
d80da9e fix(g3): messaggio di BLOCCO non attribuisce sempre la causa al token
53915cd chore(revisore): memoria review #342 — APPROVATO
6ac6415 docs(fine-task): report e handoff — verifica esterna #207
08cfd3c fix(g3): argomento sconosciuto di avviso_token_admin.sh → exit 2
ada22dc chore(revisore): memoria review #341 — APPROVATO
d62eb75 docs(fine-task): report e handoff — bot #207 (58632e1)
1e9d44f docs: G-3 fase 2 allineata in CLAUDE.md, setup e stato (bot #207 V-2)
b031722 fix(g3): OK inizializzata — una variabile d'ambiente non apre più il blocco
a9df945 chore(revisore): memoria review #340 — APPROVATO
58632e1 docs(fine-task): conteggio test corretto nell'handoff (PR #207)
a0f39b7 docs(fine-task): report e handoff — G-3 fase 2 (PR #207)
17f40c3 docs: G-3 fase 2 fatta (CLAUDE.md, setup, stato)
0996de7 feat(g3): fase 2 — gasmerge --auto blocca se il token non è quello dell'agente verificato
989fa0c chore(revisore): memoria review #339 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #339 (commit 0996de7) — verdetto integrale

## VERDETTO: APPROVATO

Ho letto CLAUDE.md (§3, §10 G-3), la voce G-3 di stato_progetto.md e la memoria del revisore, poi ho esaminato il diff staged.

Elementi del diff esaminati:
- `scripts/avviso_token_admin.sh:20` — la funzione `esci` esce con 1 solo se `BLOCCO=1` e `${OK:-0}` è diverso da 1, altrimenti esce con 0. Rischio: `set -u` con `OK` non definito. Esito: ok. Il default `:-0` evita l'errore di variabile non impostata, e `OK=1` (riga 42) è impostato solo nel ramo 403/404 con `permissions.admin == true`.
- `scripts/avviso_token_admin.sh:21-49` — tutte le uscite passano da `esci`: gh assente, token che amministra (rc 0), rate limit, 403/404 non verificabile, altri rc. Rischio: fail-closed. Esito: ok. L'unico percorso verso l'exit 0 con `--blocco` è l'OK verificato. Senza flag `BLOCCO=0`, quindi si esce sempre con 0 e il comportamento è identico al precedente.
- `scripts/gasmerge.sh:43-47` — con `--auto` il blocco scatta se lo script manca (`! -r`) oppure se `--blocco` ritorna diverso da 0, e in entrambi i casi stampa «BLOCCO: G-3» ed esce con 1. Rischio: bypass del blocco. Esito: ok. Il blocco avviene prima di qualsiasi `gh pr view` o merge, e `AUTO` è impostato alla riga 19. Senza `--auto` il ramo `elif`/`else` è equivalente al vecchio (`|| true` o avviso). I test di uso errato (`tests/test_unit_gasmerge.py:1440`) non sono toccati.
- `tests/test_unit_gasmerge.py:1115-1123` — lo stub ora risponde 404 su `/keys` e true su `permissions.admin`, con il parametro `token_admin`. Rischio: indebolimento dei test `--auto` esistenti. Esito: ok. Lo stub simula il token corretto dell'agente, che è lo stato che il blocco richiede. I test `--auto` esistenti (righe 1358, 1436) passano ancora e continuano a verificare il merge e i guardrail reali. Il comportamento dei test non-auto è invariato.
- `tests/test_unit_gasmerge.py:1525-1570` — nuovi test per `--blocco` (amministra → 1, non verificabile → 1, OK → 0), gh assente → 1, e `--auto` col token admin → «BLOCCO: G-3» senza `merge_log`. Esito: ok. Coprono sia il blocco sia il caso fail-closed.

Misure riprodotte: `tests/test_unit_gasmerge.py` dà 106 passed.

Rischio escluso: non ho eseguito `gh` reale. Non ho verificato il comportamento con un token vero (alias gasclaude), con SSO o con i fork. Si fida dello stub, che modella 200/404/500. Ho riletto solo la suite gasmerge, non l'intero `pytest tests/` (1376 passed, dichiarato dal chiamante).

Note minori, non bloccanti. Il messaggio di BLOCCO suggerisce «avvia con gasclaude» anche quando la causa è un rate limit o la rete. È solo un messaggio, e il blocco in quel caso è voluto (fail-closed).

Memoria aggiornata: riga #339 aggiunta a `/home/user/Gas/.claude/agents/memoria_revisore.md` e committata con `scripts/commit_memoria_revisore.sh`.

### Review #340 (commit b031722, bot #207 V-1/V-3) — verdetto integrale

## VERDETTO: APPROVATO

Elementi del diff esaminati:
- `scripts/avviso_token_admin.sh:19` — `OK=0` inizializzata in testa, accanto a `BLOCCO=0`. Rischio esaminato: un `OK=1` esportato nell'ambiente apriva `--blocco`. Esito: ok, chiuso.
- `scripts/avviso_token_admin.sh:21` — `esci` ora legge `$OK` senza default. Rischio esaminato: con `set -u` la variabile deve esistere, e ora esiste. Esito: ok.
- `scripts/avviso_token_admin.sh:43` — l'unico punto che pone `OK=1`, raggiunto solo con `RUOLO=true` dopo un 403/404. Esito: ok, unico percorso verso l'exit 0 in modalità blocco.
- `tests/test_unit_gasmerge.py:1546` — OK=1 nell'ambiente, `gh` finto che risponde 0 su /keys, atteso exit 1 e "AMMINISTRA" su stderr. Esito: ok. Il test copre proprio la regressione e, per quanto mi hai riferito, fallisce con lo script di HEAD.
- `tests/test_unit_gasmerge.py:1561` — `gasmerge --auto` con `avviso_token_admin.sh` assente: atteso exit diverso da 0, "BLOCCO: G-3 … assente" e nessun merge registrato. Esito: ok. Corrisponde al controllo in `scripts/gasmerge.sh:44`.
- Contesto: `scripts/gasmerge.sh:44-45` blocca sia se lo script manca sia se `--blocco` esce con codice diverso da 0. Esito: ok.

Altre variabili ereditabili, esaminate staticamente:
- `BLOCCO` è assegnata a riga 18 prima di ogni uso.
- `ERR` e `RC` sono assegnate alle righe 26-27 prima di ogni lettura.
- `RUOLO` è assegnata a riga 40, con fallback `|| RUOLO=""`, prima del test.
- Nessuna di queste può quindi essere influenzata dall'ambiente.

Fail-closed: confermato. Con `--blocco` si esce 0 solo se `OK=1`, e `OK` diventa 1 soltanto a riga 43. Gli altri casi escono 1: gh assente, token che amministra, rate limit, repo non verificabile, rc anomalo, 403/404 senza ruolo admin.

Misure: ho rieseguito la classe `TestAvvisoTokenAdmin` più il test `manca_lo_script`, 20 passed. Non ho rieseguito tutti i 108 test del file.

Rischio escluso, non verificato:
- Un ambiente ostile con funzioni bash esportate (`BASH_FUNC_gh%%`), `BASH_ENV` o `GH_REPO`. Chi controlla l'ambiente del processo ha già il controllo completo, quindi nessuno script di questo tipo può difendersi da solo. Il caso del repo sbagliato (`GH_REPO`) è già coperto dal controllo del ruolo a riga 40.
- Il comportamento con un `gh` e un token reali: non riproducibile in dev.

Memoria: registrata la riga #340 e la lezione sulla #339 (`${OK:-0}` non protegge da una variabile ereditata; i flag che aprono il blocco vanno inizializzati in testa e testati con la variabile nell'ambiente). La memoria è committata con `scripts/commit_memoria_revisore.sh`.

### Review #341 (commit successivo a ada22dc, verifica esterna #207 V-2) — verdetto integrale

## VERDETTO: APPROVATO

Ho letto CLAUDE.md, stato_progetto.md e la memoria del revisore. Il diff è la sola correzione V-2 della verifica esterna #207.

Elementi esaminati:
- `scripts/avviso_token_admin.sh:21` — il `case "$#:${1:-}"` accetta solo 0 argomenti (avviso) oppure esattamente `--blocco` (blocco). Tutto il resto (`--Blocco`, `x --blocco`, `--blocco x`, argomento vuoto) va su «uso:» in stderr con exit 2. Rischio esaminato: un refuso che disattiva il blocco in silenzio. Esito: ok. `BLOCCO=0` e `OK=0` restano inizializzate prima del `case` (lezione #340), quindi l'ambiente ereditato non apre il blocco.
- `scripts/gasmerge.sh:45` (contesto) — `bash "$G3" --blocco || { BLOCCO …; exit 1; }`. Qualsiasi exit diverso da 0 blocca, quindi anche exit 2 blocca. Il blocco resta fail-closed. Esito: ok.
- `scripts/gasmerge.sh:46` e `scripts/fine_task_finale.sh:133` (contesto) — i chiamanti non passano argomenti e usano `|| true`. Il caso `0:` resta nel ramo avviso, con exit 0 invariato. Exit 2 non rompe nessun chiamante. Esito: ok.
- `tests/test_unit_gasmerge.py:1580` — parametrizzato su tre argomenti errati. Verifica exit 2 e «uso:» in stderr, con PATH ridotto in modo che il test non dipenda da `gh`. Esito: ok.

Verifiche eseguite: `tests/test_unit_gasmerge.py` dà 111 passed, riprodotti da me. Non ho toccato i guardrail del motore (`_get_window`, cap 10 iterazioni, cap 8k) e non ho trovato antipattern del Wall of Shame.

Rischio escluso: non ho eseguito `fine_task_finale.sh` né `gasmerge --auto` end-to-end con `gh` reale. Sono in rete e richiedono un token. La compatibilità è stata dedotta dalla lettura delle righe di chiamata, che non passano argomenti o passano esattamente `--blocco`.

Memoria: aggiunta la riga #341 (il massimo esistente era #340) e committata con `scripts/commit_memoria_revisore.sh`. Nessuna lezione nuova.

### Review #342 (commit successivo a 53915cd, messaggio di BLOCCO) — verdetto integrale

## VERDETTO: APPROVATO

Il diff staged è una sola riga, cioè il testo del messaggio di blocco. Non cambia la logica.

Elementi del diff esaminati:
- `scripts/gasmerge.sh:45` — il messaggio del ramo `bash "$G3" --blocco || {…; exit 1; }` ora dice «token gh non verificato o che amministra il repo (vedi l'avviso sopra; per il token sbagliato: avvia Claude Code con gasclaude)».
  - Rischio esaminato: che il testo nuovo cambi il comportamento o nasconda la causa. Il `|| { …; exit 1; }` e il fail-closed (exit 1) sono identici a prima.
  - «Vedi l'avviso sopra» è corretto: `scripts/avviso_token_admin.sh` stampa su stderr l'avviso della causa (gh assente, rate limit, repo non visibile, amministra) prima di uscire con 1.
  - Esito: ok. La riga 44, con lo script assente, resta intatta.
- `tests/test_unit_gasmerge.py:1610` (contesto, non nel diff) — `test_gasmerge_auto_blocca_col_token_admin` cerca solo la sottostringa «BLOCCO: G-3», che il messaggio nuovo conserva. Esito: ok.
- `tests/test_unit_gasmerge.py:1576` (contesto) — il test sullo script assente cerca «BLOCCO: G-3» e «assente», e questo è il messaggio della riga 44, non toccata. Esito: ok.
- `scripts/avviso_token_admin.sh:21` (contesto) — con `--blocco` il rifiuto parte da `esci` (exit 1) per gh assente, rate limit, non verificabile o admin. La riga 45 copre quindi tutti questi casi, e il messaggio nuovo non attribuisce più sempre la causa al token sbagliato. Chiude V-4 (COSMETICA) del bot #207 e della verifica esterna. Esito: ok.

Il diff non tocca CLAUDE.md sez. 5 (`_get_window`, tool simulation), i guardrail del motore né i provider, quindi non c'è nulla da verificare lì.

Rischio escluso: non ho rieseguito `pytest`. Mi fido delle misure che mi hai dato (111 passed in `test_unit_gasmerge.py`, 1381 su `tests/`). Non ho riprodotto nemmeno i 9 failed con gli script di origin/main. Il confronto è solo statico: la sottostringa cercata dai test è presente nel messaggio nuovo.

Memoria aggiornata con la riga #342 e committata con `scripts/commit_memoria_revisore.sh`. Il massimo numerico precedente era 341.

## §5 DELTA TEST DEL MOTORE

tests/test_unit_gasmerge.py: 101 → 111 passed (sulla testa di codice finale). Mutazione: con gli script di origin/main `9 failed, 102 passed`.

pytest `tests/`: `1381 passed in 172.29s (0:02:52)` (sulla testa di codice finale).

## §6 STATO CI

`gh` non disponibile nella sessione cloud: lo stato CI si legge dai check-run della PR via MCP GitHub.

- `989fa0c`, `0996de7`, `17f40c3`: nessuna run su questi SHA (pushati prima dell'apertura della PR #207).
- `a0f39b7` (fine-task precedente): run della PR #207 partita; esito non riportato qui (superato dalla testa nuova).
- `58632e1`: unit-suite e handoff-check sulla PR #207; bot NON approvata (V-1 MEDIA, corretta qui).
- `6ac6415`: run della PR #207 partita; esito non riportato qui (superato dalla testa nuova).
- `d62eb75`: unit-suite in corso alla verifica del bot; bot APPROVATO CON RISERVE (neutral), note V-1 (numeri dei test) e V-2 (messaggio) chiuse qui.
- `d62eb75` (dettaglio): run della PR #207 partita; esito non riportato qui (superato dalla testa nuova).
- `a9df945`, `b031722`, `1e9d44f`, `ada22dc` il fix V-2, `53915cd` e il fix del messaggio: nessuna run su questi SHA (pushati insieme al commit di fine-task).
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna riserva dalle review #340/#341.
- Verifica esterna #207 V-3 (BASSA): il blocco copre solo `gasmerge --auto`, non `gh pr merge` diretto; V-4 (COSMETICA) = nota della #339, CHIUSA (review #342).
- Nota minore della review #339: il messaggio di BLOCCO cita `gasclaude` anche quando la causa è rete o rate limit.
- Alias `gasclaude` non fail-safe se il file del token manca (bot #206 V-1), da cambiare sul Mac.
