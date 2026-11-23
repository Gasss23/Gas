# HANDOFF — Dossier di fine sessione

**Sessione:** 23 novembre 2026 — R7 fetta 3: stato dei lavori ricorrenti del giro di notte (sotto-chat di M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #399 (https://github.com/Gasss23/Gas/pull/399), etichetta «verifica». Tocca il motore: merge autonomo solo con verdetto testuale del bot APPROVATO senza finding V-x, CI verde e niente conflitti; altrimenti decide l'operatore.

Numero e URL della PR presi dall'output di `gh api repos/Gasss23/Gas/pulls` (POST, creazione): `399`, `https://github.com/Gasss23/Gas/pull/399` (`gh pr` non disponibile in questo ambiente, solo REST).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 3 R7 — lista dei lavori ricorrenti con stato**: FATTA. Registro `.gas_notte/stato_lavori.json` (fatto / in sospeso / fallito / da non ritentare), 3 ko di fila → fermo 7 giorni nei giri completi, rilancio a mano con `gas notte <nome>`, pausa decaduta col prompt cambiato, sezione nel riepilogo, doc in `reports/setup_notte.md`. Review #839-F3 → correzioni R-839-1/R-839-2 → review #842.
- **Fetta 4 R7 — tetti di tempo duri**: DEFERITA — prossima PR.
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA — dopo la 4.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/notte/notte.py             | 146 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 reports/diff_sessione.md           |  17 +++++++----------
 reports/handoff.md                 | n/d
 reports/setup_notte.md             |   7 +++++++
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  25 ++++++++++---------------
 tests/test_unit_notte.py           | 174 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
b7ae5d42 feat(notte): R7 fetta 3 — stato dei lavori ricorrenti (fatto, in sospeso, fallito, da non ritentare)
2246dd88 chore(revisore): memoria review #842 — APPROVATO CON RISERVE
113a2fde chore(revisore): memoria review #839 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push. 113a2fde porta il numero #839 nella memoria di questo ramo: nei report è «#839-F3» (la #839 della PR #398 è un'altra review).

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit b7ae5d42 (motore). Due verdetti sullo stesso diff: #839-F3 sul primo staged, #842 dopo le correzioni di R-839-1 e R-839-2. Incollati integrali.

### Review #839-F3

## VERDETTO: APPROVATO CON RISERVE

Review #839: fetta 3 della roadmap R7, stato dei lavori ricorrenti del giro di notte.
- Branch: claude/r7-lavori-ricorrenti.
- Diff in staging: 3 file, +279/−2, sha256 58fe3ff7.

Prima della review ho letto CLAUDE.md (§5, §8, §9), lo stato del progetto e la mia memoria.

**Esecuzione dei test.** 207 passed in tests/test_unit_notte.py, eseguito su una copia dell'indice (`git checkout-index`). Due prove in più, riportate nei finding:
- riproduzione del crash del finding 1;
- un mutante sulla potatura (finding 2).

**Elementi del diff esaminati**

1. modules/notte/notte.py:826 — `_leggi_stato_lavori`.
   - Cosa fa: legge il registro, scarta i nomi fuori da `_NOME_RE` e gli stati sconosciuti, riporta `ko_di_fila` e `fino_a` a valori sicuri.
   - Rischio esaminato: file rotto o alterato, path traversal nel nome, bool usato come int.
   - Esito: ok. Il test modules/… tests/test_unit_notte.py:2594 copre JSON rotto, `../x`, `ko_di_fila: True` e `fino_a: "domani"`.
   - Unica eccezione: il controllo di `fino_a` a modules/notte/notte.py:850 accetta qualsiasi numero finito. Vedi finding 1.
2. modules/notte/notte.py:865 — `_in_pausa`.
   - Cosa fa: la pausa vale solo con impronta del prompt uguale e `adesso < fino_a <= adesso + 7 giorni + 60 s`.
   - Rischio esaminato: un lavoro fermo per sempre (orologio portato indietro, file alterato).
   - Esito: ok. Test a tests/test_unit_notte.py:2580 (pausa scaduta e data a 400 giorni).
3. modules/notte/notte.py:875 — `_aggiorna_lavoro`.
   - Cosa fa: esito ok porta a «fatto» o «in_sospeso» e azzera i ko. Esito ko incrementa il conto (azzerato se il prompt è cambiato). A 3 ko il lavoro va «da_non_ritentare» per 7 giorni.
   - Rischio esaminato: un ok che non azzera i ko, conto che si porta dietro un prompt vecchio.
   - Esito: ok. Test a tests/test_unit_notte.py:2557 e tests/test_unit_notte.py:2568.
   - Nota di comportamento, non è un difetto: a pausa scaduta il conto resta a 3. Un altro ko riporta subito il lavoro in pausa per 7 giorni, quindi riprova una volta a settimana. È coerente con «poi riprova da solo» (reports/setup_notte.md:10).
4. modules/notte/notte.py:974 — potatura e filtro dei lavori in pausa in `esegui_notte`.
   - Cosa fa: pota solo con `solo is None and not avvisi`, come R-407-1. Toglie i lavori in pausa solo nei giri completi. Con `gas notte <nome>` il lavoro gira sempre.
   - Rischio esaminato: un lavoro in pausa che conta come ko del giro.
   - Esito: ok. Con tutti i compiti in pausa, `compiti` resta vuoto e il ramo `return 1 if catalogo_ko else 0` dà 0, come verifica tests/test_unit_notte.py:2535.
   - La guardia della potatura però non è coperta dai test. Vedi finding 2.
5. modules/notte/notte.py:1040 — aggiornamento e scrittura atomica del registro dopo ogni compito, con avviso al passaggio a «da non ritentare» (loggato in gas_debug.log).
   - Rischio esaminato: un crash a metà compito.
   - Esito: ok. Il registro dei crash `in_corso.json` resta indipendente e non viene toccato.
   - `_scrivi_stato_lavori` non lancia mai eccezioni (le scrive nel log come warning).

**Finding**

- **R-839-1 MEDIA.** Una `fino_a` finita ma enorme (es. `1e20`) passa la pulizia a modules/notte/notte.py:850.
  - `righe_lavori` la formatta a modules/notte/notte.py:914 con `datetime.fromtimestamp`, che lancia OverflowError, oppure ValueError con valori come 1e12.
  - L'eccezione finisce nell'`except` esterno: il giro viene registrato come «giro interrotto», il riepilogo `ultimo_giro.md` non viene scritto e Telegram riceve «INTERROTTO».
  - Riprodotto: registro con `fino_a: 1e20` più un kernel che non parte. Il ramo «kernel non creato» a modules/notte/notte.py:1014 fa `continue` prima di aggiornare il registro, quindi la voce sbagliata resta e il problema si ripete ogni notte. Stesso risultato se il lavoro viene saltato dal tetto di tempo del giro.
  - In un giro normale la voce viene sovrascritta dopo il compito, quindi serve un file alterato più un secondo guasto. Resta però contro la promessa «registro rotto non ferma il giro» e contro il principio zero crash.
  - Correzione da una riga: limitare `fino_a` a un intervallo plausibile nel loader, oppure mettere la formattazione in un try (lo stesso vale per modules/notte/notte.py:980, oggi protetto da `_in_pausa`).
- **R-839-2 BASSA.** Sopravvive il mutante che toglie `and not avvisi` dalla potatura (modules/notte/notte.py:974): con il mutante applicato i 7 test r7f3 passano.
  - La seconda metà di tests/test_unit_notte.py:2611 usa un catalogo tutto rotto. Nessun compito gira, quindi il registro non viene riscritto e la potatura in memoria non si vede.
  - Serve un catalogo con un compito valido più una voce rotta.
- **R-839-3 COSMETICA.** Se il kernel non viene creato, `esiti` contiene un KO ma lo stato del lavoro non si aggiorna: nella sezione «Lavori ricorrenti (stato)» compare ancora il vecchio «fatto».
  - Non contare un guasto del kernel come ko del lavoro è ragionevole; manca solo un'etichetta coerente.
  - Allo stesso modo, i compiti saltati per crash ripetuti (`saltati_r7`) non compaiono nella sezione.

**Controllo antipattern (CLAUDE.md §5 e §8).**
- Nessuno slicing della history.
- Nessuna simulazione dell'output dei tool: il kernel finto `_KEsito` è uno stub di test, uguale a quelli già esistenti.
- Limite di 10 iterazioni, `_get_window` e provider non toccati.
- Sezione del riepilogo: contiene solo metadati del kernel, mai testo del modello (modules/notte/notte.py:903).

**Rischi esplicitamente esclusi**
- Comportamento reale sul Mac (launchd alle 03:00, fuso orario di `datetime.fromtimestamp` per «fermo fino al gg/mm») non verificato: non riproducibile in questo ambiente.
- Invio vero su Telegram non verificato: nei test `_notifica_telegram` è sostituita da una funzione finta. Ho controllato solo che i nuovi avvisi finiscano in `avvisi` (limite `MAX_AVVISI_TELEGRAM=5`).
- Non ho eseguito l'intera suite di test fuori da tests/test_unit_notte.py: il diff tocca solo modules/notte/notte.py.

**Memoria del revisore.** Riga #839 e due lezioni aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, già committate da `scripts/commit_memoria_revisore.sh` (commit 113a2fde). Le riserve R-839-1/2/3 vanno registrate in reports/stato_progetto.md. Per R-839-1 consiglio la correzione prima del merge (costo minimo).

### Review #842

## VERDETTO: APPROVATO CON RISERVE

Seconda review della fetta 3 di R7 sul branch claude/r7-lavori-ricorrenti. In memoria è la riga **#842**. La prima review compare nei report come «#839-F3».
- Diff in staging: 3 file, +325/−2, sha256 f7718ce8.
- Test: 209 passed in tests/test_unit_notte.py, eseguito su una copia dell'indice (`git checkout-index`).
- Mutanti: ho applicato 3 mutanti e ognuno fa fallire un test r7f3 (1 failed, 8 passed).

**Elementi del diff esaminati**

1. modules/notte/notte.py:852 — il loader accetta `fino_a` solo se finita e dentro `[0, time.time() + GIORNI_PAUSA*86400 + 60]`; fuori da quell'intervallo la porta a 0.0.
   - Rischio esaminato: una data enorme o negativa che arriva a `fromtimestamp` (R-839-1).
   - Esito: ok. Il mutante che toglie il limite viene ucciso da tests/test_unit_notte.py:2626, che prova 1e20, 1e12 e −5 con un kernel che non parte, e verifica che il giro non risulti «interrotto» e che il riepilogo venga scritto.
   - Il limite usa la stessa tolleranza di `_in_pausa` (modules/notte/notte.py:875), quindi una pausa legittima appena scritta non viene scartata.
2. modules/notte/notte.py:899 — `_giorno` intercetta OverflowError, OSError e ValueError e restituisce «?».
   - È usata sia a modules/notte/notte.py:925 (`righe_lavori`) sia a modules/notte/notte.py:991 (avviso di pausa).
   - Rischio esaminato: un'eccezione nella formattazione che manda in «giro interrotto» il giro, dopo che i compiti sono già stati eseguiti.
   - Esito: ok. Il mutante che toglie il try viene ucciso (`assert notte._giorno(1e20) == "?"`). È una seconda difesa, oltre al limite nel loader.
3. tests/test_unit_notte.py:2648 — catalogo con un compito valido e una voce rotta (`- 7`).
   - Il compito «a» gira e il registro viene riscritto, ma la voce «b» resta.
   - Rischio esaminato: il mutante che toglie `and not avvisi` dalla potatura (modules/notte/notte.py:974), che con la versione precedente dei test sopravviveva (R-839-2).
   - Esito: ok, ora il mutante viene ucciso.
4. modules/notte/notte.py:1040 — l'aggiornamento e la scrittura del registro dopo ogni compito non cambiano rispetto alla review precedente.
   - Esito: ok. Nessun nuovo percorso di eccezione.

**Riserva aperta**

- **R-839-3 COSMETICA, allargata.** Se il kernel non viene creato, lo stato del lavoro non si aggiorna. Il caso nuovo: una voce «da_non_ritentare» con `fino_a` azzerata dal loader (0.0) o con la pausa già scaduta mostra nel riepilogo «fermo fino al 01/01», oppure una data già passata (modules/notte/notte.py:925). Il testo è fuorviante ma non fa danni: il lavoro non viene saltato, perché `_in_pausa` è falso. Da tracciare in stato_progetto.md.

**Controllo antipattern (CLAUDE.md §5, §8 e §9)**
- Nessuno slicing della history.
- Nessuna simulazione dell'output dei tool (il kernel finto è solo uno stub di test).
- Limite di 10 iterazioni e `_get_window` non toccati.
- Nessuna nuova eccezione arriva fino all'`except` del giro.

**Rischi esplicitamente esclusi**
- Comportamento sul Mac non verificato (launchd, fuso orario di `fromtimestamp`, invio vero su Telegram): non è riproducibile qui.
- Non ho eseguito la suite di test completa, solo tests/test_unit_notte.py: il diff tocca solo modules/notte/notte.py e i suoi test.
- Non ho riletto reports/setup_notte.md: è invariato rispetto alla review precedente (+7 righe).

**Memoria del revisore.** Riga #842 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da `scripts/commit_memoria_revisore.sh` (commit 2246dd88). Nessuna lezione nuova.
- Su questo ramo la riga della review precedente si chiama ancora «#839». Se il ramo dell'altra PR (#398) porta anch'esso una riga #839, al merge i due numeri si scontrano: va tenuto presente quando si uniscono le memorie.

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_notte.py`: 200 → 209 (9 test nuovi), tutti verdi in locale: `209 passed in 5.63s`.
- `tests/test_unit_kernel.py` (round-trip agentico), eseguito in locale sul ramo di questa PR, riga reale:

```
=== RIEPILOGO: 1187 PASS, 0 FAIL ===
```

Nessun FAIL.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura:

```
completed	skipped	R7 fetta 3: stato dei lavori ricorrenti del giro di notte	verifica-bot	claude/r7-lavori-ricorrenti	pull_request_target	45217179154	8s	2026-11-23T16:29:57Z
in_progress		feat(notte): R7 fetta 3 — stato dei lavori ricorrenti (fatto, in sosp…	CI	claude/r7-lavori-ricorrenti	push	45217146013	1m17s	2026-11-23T16:29:46Z
completed	success	R7 fetta 2: ripresa al boot del compito in sottofondo	verifica-bot	claude/r7-ripresa-al-boot	pull_request_target	45216004004	2m34s	2026-11-23T16:23:44Z
```

Mappatura commit→run:
- b7ae5d42 (motore): run CI 45217146013 in corso alla scrittura (esito non ancora disponibile); verifica-bot 45217179154 skipped (PR senza etichetta: la «verifica» si mette dopo questo commit).
- 2246dd88 e 113a2fde (memoria del revisore): nessuna run su questi SHA (pushati insieme a b7ae5d42, la run testa solo l'albero di testa).
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-839-3 COSMETICA (review #839-F3, allargata dalla #842) — kernel non creato: lo stato del lavoro non si aggiorna; voce «da non ritentare» con pausa azzerata o scaduta mostra «fermo fino al» una data passata o 01/01 (il lavoro non viene saltato). Aperta.
- R-839-1 MEDIA e R-839-2 BASSA della #839-F3: CHIUSE (review #842).
- Riserve delle altre chat e della PR #398: in `reports/stato_progetto.md` e sul ramo della #398.
