# HANDOFF — Dossier di fine sessione

**Sessione:** 23 novembre 2026 — R7 fetta 3: stato dei lavori ricorrenti del giro di notte (sotto-chat di M1) — quarto giro: merge di main dopo la #398, via al merge dell'operatore

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #399 (https://github.com/Gasss23/Gas/pull/399), etichetta «verifica». L'operatore ha dato il via («sì, mergia 398 e 399», riferito dal coordinatore M1; la #398 è già mergiata): dopo CI e bot verdi sull'head nuovo il merge lo fa l'agente. Ultimo verdetto del bot (ae2ea9e0): APPROVATO CON RISERVE senza ALTA/MEDIA.

Numero e URL della PR presi dall'output di `gh api repos/Gasss23/Gas/pulls` (POST, creazione): `399`, `https://github.com/Gasss23/Gas/pull/399` (`gh pr` non disponibile in questo ambiente, solo REST).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 3 R7 — lista dei lavori ricorrenti con stato**: FATTA. Registro `.gas_notte/stato_lavori.json` (fatto / in sospeso / fallito / da non ritentare), 3 ko di fila → fermo 7 giorni nei giri completi, rilancio a mano con `gas notte <nome>`, pausa decaduta col prompt cambiato, sezione nel riepilogo, doc in `reports/setup_notte.md`. Review #839-F3 → correzioni R-839-1/R-839-2 → review #842.
- **Correzioni delle riserve sulla PR #399 (secondo giro)**: FATTA. Verifica esterna V-1 BASSA: i guasti esterni (provider giù, budget, cervello forte fermo, dati di clienti senza forte) lasciano «fallito» ma non contano tra i ko di fila. Bot V-1 BASSA: la sezione mostra anche i compiti saltati per crash. Bot V-2 BASSA: l'avviso dice il conto reale; ritmo dopo la prima pausa documentato. 6 test nuovi (215). Review #843.
- **Merge di origin/main (PR #397 della chat CRM) nel ramo (terzo giro)**: FATTO (73277ba0), conflitti dei report risolti come dice `reports/lavoro_parallelo.md` regola 3 (riserve CRM già in `stato_progetto.md`). Review #844-MERGE: R-844M-1 MEDIA (con «Sempre Opus» il testo d'errore «Rispondo solo con Claude Opus…» non era riconosciuto come guasto esterno).
- **Correzioni del terzo giro**: FATTA (87006476). R-844M-1 (prefisso aggiunto + test col kernel vero e GAS_SOLO_OPUS=1); verifica esterna #399 (3b188028) V-1 (dopo 14 guasti esterni di fila pausa di 7 giorni); R-843-1 (un guasto esterno non toglie né allunga una pausa in corso); R-845R7-1/2. Review #845-R7 → #846-R7 APPROVATO. 220 test.
- **V-1 MEDIA del bot su 3b188028**: FATTA (7b05ccf2). «Pipeline esausta» (e gli errori col dettaglio dei motivi, anche con «Sempre Opus») copriva motivi nati dal lavoro: tetto delle chiamate per turno, risposta vuota, 10 iterazioni senza risposta finale. Ora contano come ko veri; test col kernel vero che arriva al tetto e test con i testi veri di «Sempre Opus». Review #847-R7 BOCCIATO (valeva solo con «Sempre Opus» spento) → #848-R7 APPROVATO. 230 test.
- **Merge di origin/main dopo la PR #398 (quarto giro)**: FATTO (bc7d08df), conflitti solo nei report (regola 3). Review #851-MERGE-R7 APPROVATO. notte + sottofondo: 359 passed.
- **Fetta 4 R7 — tetti di tempo duri**: DEFERITA — prossima PR.
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA — dopo la 4.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  14 +++++++++
 modules/notte/notte.py             | 210 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 reports/diff_sessione.md           |  13 ++++----
 reports/handoff.md                 | n/d
 reports/setup_notte.md             |  15 ++++++++++
 reports/stato_progetto.md          |   3 +-
 reports/ultimo_report.md           |  26 ++++++++--------
 tests/test_unit_notte.py           | 372 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso. La CI confronta solo i path. Dopo il merge bc7d08df la base del ramo è il main con la #398 (d13d4342).

## §3 GIT LOG --ONELINE (sessione)

```
bc7d08df Merge origin/main (PR #398 mergiata) nel ramo della PR #399 — review #851-MERGE-R7 APPROVATO
ae2ea9e0 docs(fine-task): PR #399 terzo giro — merge di main, «Sempre Opus», V-1 MEDIA del bot; review #844-MERGE, #845…#848-R7
7b05ccf2 fix(notte): bot #399 V-1 — tetto di chiamate, risposta vuota e iterazioni finite sono ko del lavoro, anche con «Sempre Opus»
f78682bf chore(revisore): memoria review #848 — APPROVATO
26a27136 chore(revisore): memoria review #847 — BOCCIATO
87006476 fix(notte): R-844M-1 «Sempre Opus» è guasto esterno; tetto dei guasti esterni di fila; pausa non tolta né allungata
3599a7d4 chore(revisore): memoria review #846 — APPROVATO
49ce5f74 chore(revisore): memoria review #845 — APPROVATO CON RISERVE
73277ba0 Merge origin/main (PR #397, CRM) nel ramo della PR #399 — review #844-MERGE APPROVATO CON RISERVE
3b188028 docs(fine-task): PR #399 secondo giro — riserve di bot e verifica esterna, review #843
f3a6168e fix(notte): riserve su PR #399 — guasti esterni non contano, sezione con tutti i compiti, avviso col conto reale
ba513ece chore(revisore): memoria review #843 — APPROVATO CON RISERVE
492f7e20 docs(fine-task): R7 fetta 3 — report, handoff con review #839-F3/#842, stato_progetto
b7ae5d42 feat(notte): R7 fetta 3 — stato dei lavori ricorrenti (fatto, in sospeso, fallito, da non ritentare)
2246dd88 chore(revisore): memoria review #842 — APPROVATO CON RISERVE
113a2fde chore(revisore): memoria review #839 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push. 113a2fde porta il numero #839 nella memoria di questo ramo: nei report è «#839-F3» (la #839 della PR #398 è un'altra review).

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit b7ae5d42 (motore): due verdetti sullo stesso diff, #839-F3 sul primo staged e #842 dopo le correzioni di R-839-1 e R-839-2. Commit f3a6168e (motore, riserve di bot e verifica esterna): review #843. Merge 73277ba0: review #844-MERGE. Commit 87006476 (motore): review #845-R7 e #846-R7. Commit 7b05ccf2 (motore): review #847-R7 e #848-R7. Merge bc7d08df: review #851-MERGE-R7. Incollati integrali.

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

### Review #843 (commit f3a6168e)

## VERDETTO: APPROVATO CON RISERVE

Review #843, nuova revisione del diff STAGED sul ramo claude/r7-lavori-ricorrenti (PR #399). Il diff tocca 3 file (+91/−7), sha256 del diff 9f0ee46f.

Prima della review ho letto CLAUDE.md §5, reports/stato_progetto.md (lettura mirata) e la mia memoria (ultime voci #839 e #842 di questo ramo).

**Elementi esaminati**
- `modules/notte/notte.py:889` — nuovo ramo di `_aggiorna_lavoro`: se l'esito non è ok e l'errore viene da fuori del lavoro, lo stato diventa «fallito» con `esterno=True` e `ko_di_fila=ko_prima`.
  - Rischio esaminato: che il modello o l'output di un tool possano falsificare un «guasto esterno» e così evitare la pausa.
  - Verificato: `esito["errore"]` arriva solo dagli eventi `type: error` del kernel (`modules/notte/notte.py:312`); l'output dei tool va in un altro campo (`modules/notte/notte.py:296`).
  - Esito: ok.
- `modules/notte/notte.py:915` — `_ERRORI_ESTERNI` e `_ko_esterno`, con type hints presenti.
  - Rischio esaminato: un prefisso mancante o sbagliato. Ho confrontato i prefissi con tutti e 5 gli eventi d'errore di `run_turn`: `gas.py:5461` («Cervello forte fermo»), `gas.py:5466` («Budget giornaliero esaurito a metà turno», coperto dal prefisso), `gas.py:5563`, `gas.py:5945` («Questa richiesta contiene dati di clienti»), `gas.py:5953` («Pipeline esausta»). Corrispondono tutti.
  - Il caso «dati di clienti» non messo mai in pausa è coerente con la regola dei modelli («aspettano in coda, mai ai gratuiti») e non spende token.
  - `str()` protegge da un errore che non è una stringa.
  - Esito: ok.
- `modules/notte/notte.py:995` — `da_mostrare = list(compiti)` adesso viene calcolato PRIMA di `_ordina_riprese`, quindi la sezione dello stato mostra anche i compiti saltati per crash.
  - Rischio esaminato: che la potatura, che usa ancora il `compiti` filtrato, cancelli lo stato dei compiti saltati. Non succede: il salto aggiunge sempre un avviso (`modules/notte/notte.py:800`), e la potatura gira solo con `not avvisi`.
  - Esito: ok.
- `modules/notte/notte.py:1073` — l'avviso di pausa riporta `ko_di_fila` reale. Coerente con la nuova documentazione in `reports/setup_notte.md:10` (un tentativo a settimana dopo la prima pausa). Esito: ok.
- `tests/test_unit_notte.py:2675`, `tests/test_unit_notte.py:2693`, `tests/test_unit_notte.py:2707` — 6 test nuovi (4 casi parametrizzati più 2).
  - Senza il ramo esterno, il primo test fallirebbe: con 4 guasti dopo un ko vero il conto diventerebbe 5 e il lavoro andrebbe in pausa.
  - Con `da_mostrare` messo dopo `_ordina_riprese`, il secondo fallirebbe: sparisce «lungo: mai eseguito».
  - Mutanti ragionati, non eseguiti.
  - Il kernel finto emette eventi d'errore veri, non output di tool simulati: nessuna violazione del §5.
  - Esito: ok.
- Prova eseguita: **215 passed** in `tests/test_unit_notte.py`, su una copia dell'indice (`git checkout-index`).
- Wall of Shame: nessuno slicing della history e nessuna simulazione di tool. Non vengono toccati `_get_window`, il cap di 10 iterazioni né il cap di output.

**Riserve**
- **R-843-1 BASSA**: un guasto esterno su un lavoro «da non ritentare» toglie la pausa, perché `fino_a` torna a 0 (`modules/notte/notte.py:889`). Succede in due casi:
  - con un rilancio a mano (`gas notte <nome>`) durante la pausa;
  - a pausa scaduta.

  Il conto resta ≥3, quindi al primo ko vero il lavoro torna subito in pausa. Ma finché durano i guasti esterni viene ritentato ogni notte invece che una volta a settimana. Il costo è nullo (i guasti esterni non spendono token) e non c'è rischio di crash. Correzione possibile: nel ramo esterno conservare `stato`/`fino_a` se il lavoro era già `da_non_ritentare`. Va tracciata, non blocca.
- **R-839-3 COSMETICA** (dalle review precedenti): resta aperta, questo diff non la tocca.

**Rischi esplicitamente esclusi**
- Non ho verificato se anche «tempo scaduto» (`modules/notte/notte.py:316`) debba contare come guasto esterno: un provider lento può far scadere il tempo e oggi conta come ko vero. È una scelta di progetto fuori dalle riserve corrette qui; non l'ho riprodotto.
- Non ho verificato il giro su VPS o Mac con provider veri: in dev non si riproduce.
- I mutanti non li ho eseguiti, solo ragionati.

Riga contatore #843 scritta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (ba513ece) con `scripts/commit_memoria_revisore.sh`.

### Review #844-MERGE (merge 73277ba0)

## VERDETTO: APPROVATO CON RISERVE

Review #844-MERGE. Riguarda il merge di `origin/main` (PR #397, «Gas usa il CRM») nel ramo `claude/r7-lavori-ricorrenti` (PR #399). Ho letto quello che è in stage con `git diff --cached HEAD` e l'ho confrontato con `git diff --cached origin/main`.

**Elementi del diff che ho esaminato**

1. `modules/notte/notte.py:915` — `_ERRORI_ESTERNI` elenca gli inizi dei testi d'errore di run_turn che indicano un guasto esterno, cioè un guasto che non va contato contro il lavoro. Ho controllato se è coerente con «Sempre Opus» arrivato con main. Esito: **riserva MEDIA (R-844M-1)**, spiegata sotto.
2. `modules/notte/notte.py:919` — `_ko_esterno` fa un semplice `startswith` su quei prefissi. L'ho provato con `GAS_SOLO_OPUS=1`. Il testo «Rispondo solo con Claude Opus (scelta dell'operatore, GAS_SOLO_OPUS), che ora non è disponibile. Dettagli: …» restituisce **False**. Il vecchio testo «Questa richiesta contiene dati di clienti…» restituisce True. Esito: riserva, fa parte di R-844M-1.
3. `gas.py:6131-6137` (contesto: identico a origin/main) — è il ramo `_solo_forte_lead` di run_turn. Con `_solo_opus_sempre()` acceso produce il nuovo testo, che non comincia con nessuno dei prefissi. `gas.py:403` rende vera `_finestra_ha_dati_lead` per ogni finestra che contiene un messaggio user, quindi anche per il prompt di un compito della notte senza `cervello: forte`. La notizia del 23-11 in `reports/bacheca.md` dice lo stesso («notte … vanno solo a Claude Opus»). Gli altri error event restano coperti: «Cervello forte fermo» (`gas.py:5636`), «Budget giornaliero esaurito» (`gas.py:5640` e `gas.py:5737`), «Pipeline esausta» (`gas.py:6144`).
4. `tests/test_unit_notte.py:2673-2677` — il test che parametrizza i guasti esterni usa una lista di stringhe scritte a mano, senza legame con i testi veri di gas.py. Per questo è rimasto verde (215 passed, rigirato da me) anche se la classificazione si è rotta. In più `tests/conftest.py:15` spegne `GAS_SOLO_OPUS`, quindi nessun test prova la notte nella configurazione di produzione. Esito: riserva, fa parte di R-844M-1.
5. Risoluzione dei conflitti. Esito: **ok**.
   - `gas.py`, `modules/crm/agente.py`, `modules/crm/store.py`, `modules/gate/gate.py`, `modules/telegram/bot.py`, `tests/conftest.py`, `tests/test_unit_crm.py`, `tests/test_unit_kernel.py` e `CLAUDE.md` sono identici a origin/main.
   - Rispetto a main cambiano solo i file della fetta 3 e i report del ramo. handoff, ultimo_report e diff_sessione sono tenuti dal ramo, come vuole la regola 3.
   - `reports/stato_progetto.md:4`: la riga «Ultimo aggiornamento» unisce le due voci. `reports/stato_progetto.md:9` porta la voce CRM di main.
   - `.claude/agents/memoria_revisore.md` è un'unione pulita: tutte le righe di main fino a #848-CRM, più #839, #842 e #843 del ramo in coda, senza perdite né doppioni.

**R-844M-1 MEDIA — da chiudere prima del merge della PR #399**

Con `GAS_SOLO_OPUS` acceso, che è il default in produzione, se Opus è giù o `GAS_CLAUDE_CLI` manca, ogni compito della notte finisce con «Rispondo solo con Claude Opus…». Il testo non è riconosciuto come esterno, quindi:
- dopo 3 notti il lavoro va in `da_non_ritentare` per 7 giorni;
- il riepilogo non dice «guasto esterno».

È esattamente il caso che la fetta 3 (V-1 della verifica esterna #399) voleva evitare. Non c'è conflitto testuale: è un conflitto di significato introdotto dal merge.

Correzione proposta:
- aggiungere `"Rispondo solo con Claude Opus"` a `_ERRORI_ESTERNI`;
- aggiungere un test che produca l'errore VERO con un `GasKernel` reale, `GAS_SOLO_OPUS=1` e il forte assente (monkeypatch dell'env dentro il test), e verifichi `_ko_esterno(...) is True`. Così una prossima modifica ai testi di gas.py non passa in silenzio.

**Nota cosmetica:** in `reports/stato_progetto.md:4` la voce CRM dice «review #839-#843-CRM», ma main è arrivato a #848-CRM. Il testo è ereditato da main.

**Cosa non ho verificato**
- Non ho rigirato `tests/test_unit_kernel.py` (1208 PASS è un dato tuo). Il codice del kernel è identico a origin/main, già revisionato in #839-#848-CRM.
- Non ho provato un giro di notte vero con Opus giù sul Mac: in questo ambiente il forte non è configurato. La riserva viene dalla lettura del codice e dalla prova di `_ko_esterno`.
- Non ho controllato la CI della PR #399 dopo il merge.

**Memoria del revisore**
- Ho scritto la riga contatore `#844-MERGE` e una lezione in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`.
- `scripts/commit_memoria_revisore.sh` è uscito con 0 ma non ha committato: git rifiuta i commit parziali durante un merge («cannot do a partial commit during a merge», avviso scritto in gas_debug.log).
- La modifica è nel working tree e NON è in stage. Fai `git add .claude/agents/memoria_revisore.md` prima di chiudere il merge. Questo cambia lo SHA-256 del diff in stage, quindi rilancia `scripts/segna_review_ok.sh` dopo l'add.

### Review #845-R7 (commit 87006476, primo staged)

## VERDETTO: APPROVATO CON RISERVE

Review #845-R7. Ri-review di claude/r7-lavori-ricorrenti, PR #399, dopo il merge di main 73277ba0. Il diff staged tocca 3 file (+95/−10), sha256 del diff `bcecd14c`. Prima della review ho letto CLAUDE.md (sezione 5), reports/stato_progetto.md (voce R7 fetta 3) e .claude/agents/memoria_revisore.md (#842, #843, #844-MERGE).

**Cosa ho verificato**
- **Test:** 218 passed su `tests/test_unit_notte.py`, eseguiti su una copia dell'indice (`git checkout-index`).
- **Mutanti:** ne ho provati 7, i test ne uccidono 5. Uccisi:
  - M1: tolto il prefisso «Rispondo solo con Claude Opus»;
  - M2: soglia dei 14 disattivata;
  - M3: ramo R-843-1 disattivato;
  - M4: tolta la guardia `fino_a != pausa_prima` sull'avviso;
  - M5: il loader non rilegge `esterni_di_fila`.
- **Simulazione diretta di `_aggiorna_lavoro`:** confermati i casi descritti nei finding.

**Elementi del diff esaminati**
1. `modules/notte/notte.py:928` — aggiunge «Rispondo solo con Claude Opus» ai prefissi di `_ERRORI_ESTERNI`. Rischio esaminato: il testo deve coincidere con quello prodotto da gas.py, «Rispondo solo con Claude Opus (scelta dell'operatore, GAS_SOLO_OPUS)…», in `gas.py:6134`. Coincide, e il mutante M1 viene ucciso da `tests/test_unit_notte.py:2723`. Quel test usa il GasKernel VERO con GAS_SOLO_OPUS=1 e il cervello forte assente: dopo 4 giri il lavoro è ancora «fallito» con ko_di_fila 0 ed esterno True. **R-844M-1 CHIUSA.** Esito: ok.
2. `modules/notte/notte.py:896` e `modules/notte/notte.py:898` — contatore `esterni_di_fila`, che riparte da zero se cambia il prompt. A `ESTERNI_DI_FILA_PAUSA` = 14 (`modules/notte/notte.py:931`) il lavoro va in pausa per 7 giorni. Rischi esaminati:
   - il contatore deve azzerarsi con un ok o con un ko vero: si azzera, perché in quei rami la voce viene ricostruita senza il campo (verificato dal test a `tests/test_unit_notte.py:2741`);
   - la pausa deve ripartire subito dopo la scadenza, come per i ko: succede, coerente con «il conto non si azzera con la pausa».
   **V-1 della verifica esterna #399 CHIUSA.** Esito: ok, con la riserva R-845R7-1.
3. `modules/notte/notte.py:859` — il loader accetta `esterni_di_fila` solo se è un intero tra 1 e 1000, altrimenti lo scarta. Rischio esaminato: un file alterato. Un valore anomalo viene scartato e il contatore riparte da zero, senza eccezioni (mutante M5 ucciso). Esito: ok.
4. `modules/notte/notte.py:902` — un guasto esterno durante una pausa ancora valida, con lo stesso prompt, conserva lo stato e `fino_a`. `modules/notte/notte.py:1098` manda l'avviso solo se `fino_a` è cambiato. Rischio esaminato: avviso duplicato o pausa tolta. Per la pausa nata da ko veri il comportamento è corretto: `_volte` dice «3 volte di fila», verificato in simulazione e dal test a `tests/test_unit_notte.py:2761`. **R-843-1 CHIUSA per la pausa da ko.** Esito: ok.
5. `modules/notte/notte.py:938` — `_volte` sceglie il testo dell'avviso: «N volte di fila per guasti esterni» oppure «N volte di fila». Rischio esaminato: una chiave mancante. `ko_di_fila` è sempre presente, perché il loader e tutti i rami lo scrivono. Esito: ok.
6. `reports/setup_notte.md:14` — la documentazione è coerente con il codice (14 guasti esterni di fila, poi 7 giorni). Esito: ok.

**Finding**
- **R-845R7-1 BASSA.** Caso: la pausa è nata da 14 guasti esterni, l'operatore rilancia il lavoro a mano (`gas.py notte c`) e arriva un altro guasto esterno.
  - Il contatore sale a 15, quindi il primo ramo (`modules/notte/notte.py:898`) prevale su quello di R-843-1 (`modules/notte/notte.py:902`).
  - Effetto: la pausa si ALLUNGA (`fino_a` riparte da adesso; in simulazione +87 s) e l'avviso torna, «fallito 15 volte di fila per guasti esterni».
  - In pratica R-843-1 è chiusa solo per la pausa nata da ko veri.
  - Rimedio: nel caso di pausa ancora valida, controllare il ramo «pausa in corso» prima della soglia.
- **R-845R7-2 BASSA, sui test.** Due mutanti sopravvivono:
  - M6: il contatore NON si azzera al cambio di prompt (`modules/notte/notte.py:896`);
  - M7: un guasto esterno conserva anche una pausa già scaduta (`modules/notte/notte.py:902`), che finirebbe mostrata come «fermo fino al <data passata>», cosa già vista in R-839-3.
  Il codice è corretto, ma nessun test lo protegge.

**Antipattern (sezione 5 di CLAUDE.md)**
- Nessuno slicing della cronologia.
- Il test di R-844M-1 usa il kernel vero, non un errore simulato, come chiedeva la lezione #844-MERGE.
- `_KErrore` negli altri due test è un doppio di prova del kernel, non simula l'output di un tool.
- Il diff non tocca guardrail (tetto delle 10 iterazioni, `_get_window`, tetti di output).

**Cosa NON ho verificato**
- Il comportamento reale sulla VPS: se lì Claude Opus non è configurato per il giro di notte, con GAS_SOLO_OPUS acceso di default ogni lavoro fallirebbe per guasto esterno. Dopo 14 notti finirebbero tutti in pausa, poi un tentativo a settimana. È il comportamento voluto da V-1, ma non è riproducibile in sviluppo, quindi non l'ho provato.
- La suite del kernel (`tests/test_unit_kernel.py`): il diff non tocca gas.py e non l'ho eseguita.

**Riserve da tracciare in stato_progetto.md:** R-845R7-1 e R-845R7-2.

**Memoria del revisore:** riga #845-R7 più una lezione nuova («un secondo motivo di pausa deve ereditare le eccezioni scritte per il primo»), committate in 49ce5f74 tramite scripts/commit_memoria_revisore.sh. Ho usato il suffisso «-R7» perché sulla chat CRM esiste già #845-CRM.

File rilevanti: /home/user/Gas/modules/notte/notte.py, /home/user/Gas/tests/test_unit_notte.py, /home/user/Gas/reports/setup_notte.md, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #846-R7 (commit 87006476)

## VERDETTO: APPROVATO

Review #846-R7, secondo giro della #845-R7 sulla PR #399 (ramo claude/r7-lavori-ricorrenti). Le due riserve del giro precedente sono chiuse e il codice non mostra problemi nuovi. Diff staged: 3 file, +134/−10, sha256 del diff `b397abb4`. Letture obbligatorie già fatte in questa sessione (CLAUDE.md sez. 5, stato_progetto.md, memoria_revisore.md).

**Cosa ho verificato**
- **Test:** 220 passati in tests/test_unit_notte.py, su una copia dell'indice (`git checkout-index`).
- **Mutanti, 8 su 8 uccisi:**
  - M1: tolto il prefisso «Rispondo solo con Claude Opus».
  - M2: soglia dei 14 disattivata.
  - M3: ramo della pausa in corso disattivato (2 test falliscono).
  - M4: tolto il confronto con `pausa_prima` sull'avviso.
  - M5: il caricamento ignora `esterni_di_fila`.
  - M6: il conto non riparte al cambio di prompt. Era sopravvissuto al giro #845-R7, ora è ucciso.
  - M7: tenuta anche una pausa già scaduta. Era sopravvissuto al giro #845-R7, ora è ucciso.
  - M8: ordine dei rami invertito, cioè il codice del giro #845-R7. Ora un test lo ferma.

**Elementi del diff esaminati**
1. `modules/notte/notte.py:898` — il ramo «pausa in corso» (stesso prompt, `fino_a` ancora nel futuro) ora viene controllato PRIMA della soglia (`modules/notte/notte.py:904`).
   - Rischio esaminato: una pausa nata da 14 guasti esterni che si allunga, con l'avviso che torna, dopo un rilancio a mano.
   - Esito: ok. `fino_a` resta quello di prima, quindi `modules/notte/notte.py:1096` vede `pausa_prima` uguale e non rimanda l'avviso. Il conto sale a 15, ed è giusto così: alla scadenza un altro guasto esterno rimette subito in pausa, come per i fallimenti veri. **R-845R7-1 CHIUSA.**
2. `tests/test_unit_notte.py:2787` — test diretto su `_aggiorna_lavoro` con una pausa nata da guasti esterni e `fino_a` nel futuro.
   - Rischio esaminato: che il test non fermi il codice vecchio.
   - Esito: ok. Uccide M8 (l'ordine del giro #845-R7) e controlla che `fino_a` non cambi e che il conto vada a 15.
3. `tests/test_unit_notte.py:2800` — test diretto con due casi: prompt cambiato con 13 guasti esterni registrati (il conto riparte da 1, stato «fallito»); pausa scaduta più un guasto esterno (stato «fallito», `fino_a` 0).
   - Rischio esaminato: le due righe che nel giro precedente nessun test proteggeva (M6 e M7).
   - Esito: ok, entrambi i mutanti ora vengono uccisi. **R-845R7-2 CHIUSA.**
4. `modules/notte/notte.py:930` e `tests/test_unit_notte.py:2723` — non cambiano rispetto al giro #845-R7: R-844M-1 resta chiusa (M1 ucciso, test col GasKernel vero).

**Wall of Shame (CLAUDE.md sez. 5)**
- Nessun taglio diretto della cronologia.
- Nessuna simulazione dell'output dei tool: i due test nuovi costruiscono a mano le voci dello stato e chiamano la funzione vera.
- Nessun guardrail toccato.

**Cosa NON ho verificato**
- Il comportamento sulla VPS con «Sempre Opus» acceso e Opus non configurato, cioè tutti i lavori in pausa dopo 14 notti e poi un tentativo a settimana: non è riproducibile in sviluppo.
- La suite del kernel (tests/test_unit_kernel.py): il diff non tocca gas.py.

**Riserve:** nessuna.

**Memoria del revisore:** aggiunta la riga #846-R7 (nessuna lezione nuova), committata in 3599a7d4 con scripts/commit_memoria_revisore.sh.

**File:**
- /home/user/Gas/modules/notte/notte.py
- /home/user/Gas/tests/test_unit_notte.py
- /home/user/Gas/reports/setup_notte.md
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #847-R7 (commit 7b05ccf2, primo staged)

## VERDETTO: BOCCIATO

Review #847-R7, PR #399, ramo claude/r7-lavori-ricorrenti. Diff staged: 2 file, +39/−1, sha256 del diff `a3b68d9a`. Letture obbligatorie già fatte in questa sessione: CLAUDE.md sez. 5, stato_progetto.md, memoria_revisore.md. Su una copia dell'indice passano 224 test.

**Motivo del blocco:** la correzione chiude V-1 del bot (3b188028) solo con «Sempre Opus» spento, cioè nella configurazione dei test. Con l'impostazione di produzione V-1 resta aperta, quindi il diff non raggiunge lo scopo dichiarato.

**Elementi del diff esaminati**
1. `modules/notte/notte.py:945` — `_ko_esterno` tratta come ko vero un errore solo se **inizia con «Pipeline esausta»** e contiene uno dei `_MOTIVI_DEL_LAVORO`. Rischio esaminato: gli altri errori del kernel che portano lo stesso dettaglio. Esito: **blocco (R-847R7-1)**.
2. `modules/notte/notte.py:939` — i tre motivi coincidono con i testi di gas.py: `gas.py:5771` (tetto, testo spezzato su due righe ma contiguo), `gas.py:5874`, `gas.py:6095` e `gas.py:6098`. Rischio esaminato: un testo copiato che non coincide. Esito: ok.
3. `tests/test_unit_notte.py:2817` — test col kernel vero che arriva al tetto delle chiamate: dopo 3 notti il lavoro è in pausa, senza il segno «esterno». Rischio esaminato: se copre la configurazione di produzione. Gira con `GAS_SOLO_OPUS=0`, che `tests/conftest.py:15` imposta per tutta la suite, e quindi non vede il caso del finding 1. Esito: riserva, legata al blocco.
4. `tests/test_unit_notte.py:2836` — test parametrizzato sui tre motivi più un caso QUOTA che resta esterno. Usa solo testi che iniziano con «Pipeline esausta». Esito: ok, ma ha lo stesso buco del punto 3.

**Finding**
- **R-847R7-1 MEDIA, bloccante.** «Sempre Opus» (GAS_SOLO_OPUS) è acceso di default, `gas.py:385`.
  - Così ogni turno passa al forte e `_solo_forte_lead` vale True (`gas.py:6126`). Quando il turno si esaurisce, run_turn non dà «Pipeline esausta» ma «Rispondo solo con Claude Opus (scelta dell'operatore, GAS_SOLO_OPUS), che ora non è disponibile. Dettagli: …» (`gas.py:6134`).
  - Prova sulla copia dell'indice: `_ko_esterno` restituisce **True** con «…Dettagli: gemini: saltato (…); claude-cli: tetto di 10 chiamate al modello per turno raggiunto.» e con «…Dettagli: claude-cli: 10 iterazioni senza risposta finale.».
  - Effetto: in produzione un lavoro che gira a vuoto conta ancora come guasto esterno. Va in pausa solo dopo 14 notti, non dopo 3. È la stessa trappola di R-844M-1.
  - Rimedio proposto:
    - applicare il controllo sui `_MOTIVI_DEL_LAVORO` a ogni errore che porta il dettaglio dei motivi, cioè anche «Rispondo solo con Claude Opus» e «Questa richiesta contiene dati di clienti», non solo a «Pipeline esausta»;
    - aggiungere lo stesso test col kernel vero con `GAS_SOLO_OPUS=1`, oppure, se il forte non si riesce a simulare, un test parametrizzato con i testi veri di `gas.py:6134`.
- **R-847R7-2 BASSA.** Basta un solo «risposta vuota» in un guasto misto (es. «gemini: risposta vuota; groq: QUOTA (HTTP 429); openrouter: KO (HTTP 503)») perché valga come ko vero (provato: `_ko_esterno` dà False). È un compromesso accettabile, perché servono 3 notti così, ma va dichiarato in reports/setup_notte.md.

**Wall of Shame:** nessun taglio diretto della cronologia, nessuna simulazione dell'output dei tool, nessun guardrail toccato.

**Cosa NON ho verificato**
- Il percorso con claude-cli vero: non è simulabile qui. Il testo dell'errore viene dalla lettura di `gas.py:6126-6137`, e la classificazione l'ho provata chiamando `_ko_esterno` su quei testi.
- Non ho eseguito la suite del kernel: il diff non tocca gas.py.

**Memoria del revisore:** riga #847-R7 più una lezione nuova («conftest spegne GAS_SOLO_OPUS: pretendere la variante con GAS_SOLO_OPUS=1»), committate in 26a27136.

**File:**
- /home/user/Gas/modules/notte/notte.py
- /home/user/Gas/tests/test_unit_notte.py
- /home/user/Gas/tests/conftest.py
- /home/user/Gas/gas.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #848-R7 (commit 7b05ccf2)

## VERDETTO: APPROVATO

Review #848-R7, secondo giro della #847-R7, PR #399, ramo claude/r7-lavori-ricorrenti. Le due riserve della #847-R7 sono chiuse; nessuna riserva aperta. Diff staged: 3 file, +64/−2, sha256 `ed652379`. Letture obbligatorie (CLAUDE.md sez. 5, stato_progetto.md, memoria del revisore) già fatte in questa sessione.

**Prove eseguite**
- `tests/test_unit_notte.py` su una copia dell'indice: 230 passano.
- Mutanti: 3 su 3 uccisi.
  - N1, cioè tornare al controllo solo su «Pipeline esausta» (il codice bocciato in #847-R7): 6 test falliscono.
  - N2, togliere «risposta vuota» dall'elenco dei motivi: 3 test falliscono.
  - N3, spegnere il controllo dei motivi: 10 test falliscono.

**Elementi del diff esaminati**
1. `modules/notte/notte.py:950` — il controllo dei `_MOTIVI_DEL_LAVORO` ora vale per ogni errore, prima del confronto coi prefissi esterni.
   - Rischio esaminato: errori esterni scambiati per ko veri. I tre testi cercati compaiono in gas.py solo nei motivi del turno (`gas.py:5771`, `gas.py:5874`, `gas.py:6095`, `gas.py:6098`). Il «risposta vuota» di `gas.py:1180` sta in `_analizza_riflessione`, che non arriva agli errori del turno. Gli errori «Cervello forte fermo» e «Budget giornaliero esaurito» (`gas.py:5636`, `gas.py:5641`) non contengono quei testi. I messaggi del cervello forte (`_motivo_forte`, `gas.py:781`) vengono da brains/claude_cli.py, dove quei testi non ci sono.
   - Per gli errori che non sono esterni il controllo non cambia niente: erano già ko veri.
   - Esito: ok. **R-847R7-1 CHIUSA.**
2. `tests/test_unit_notte.py:2852` — test parametrizzato (2 inizi di messaggio × 3 motivi) con i testi veri di `gas.py:6134`. Copre il caso di produzione con «Sempre Opus» acceso, che conftest spegne nei test (`tests/conftest.py:15`). Controlla anche che «claude-cli: KO (RuntimeError)» resti un guasto esterno. Rischio esaminato: test che passa anche col codice bocciato. Uccide N1. Esito: ok.
3. `reports/setup_notte.md:18` e il commento a `modules/notte/notte.py:941` dichiarano il compromesso: un guasto misto (un motivo che nasce dal compito, più un guasto di provider) conta come fallimento vero. Esito: ok. **R-847R7-2 CHIUSA** (dichiarata, come chiesto).
4. `tests/test_unit_notte.py:2817` (test col kernel vero, tetto delle chiamate, pausa dopo 3 notti) non è cambiato rispetto a #847-R7. Gira ancora con GAS_SOLO_OPUS=0, ma ora il caso «Sempre Opus» è coperto dal punto 2. Esito: ok.

**Wall of Shame:** nessun taglio diretto della cronologia, nessun output di tool simulato, nessun guardrail toccato.

**Cosa NON ho verificato**
- Il percorso con claude-cli vero (Opus reale che arriva al tetto): qui non è riproducibile. La classificazione è provata sui testi letti in `gas.py:6131-6137`.
- La suite del kernel: il diff non tocca gas.py.
- I testi dei messaggi di Claude CLI li ho controllati solo con una ricerca su brains/. Se in futuro un messaggio del CLI contenesse «risposta vuota», un guasto del forte conterebbe come ko vero. Oggi non succede.

**Memoria:** aggiunta la riga #848-R7 (nessuna lezione nuova), committata in f78682bf.

**File:**
- /home/user/Gas/modules/notte/notte.py
- /home/user/Gas/tests/test_unit_notte.py
- /home/user/Gas/reports/setup_notte.md
- /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #851-MERGE-R7 (merge bc7d08df)

## VERDETTO: APPROVATO

Revisione #851-MERGE-R7: merge in corso di origin/main (PR #398, R7 fetta 2) dentro claude/r7-lavori-ricorrenti (PR #399). Ho confrontato quello che è in stage con HEAD: 7 file, +360/−1, impronta sha256 del diff e0e75617.

**Elementi del diff esaminati**
- `gas.py:7347` — nuovo comando `sottofondo-riprendi` che chiama `riprendi_al_boot`. Rischio esaminato: che venga intercettato da un comando precedente o vada in collisione con `notte` (`gas.py:7340`) o con `sottofondo-ferma` (`gas.py:7342`). Ogni ramo confronta il nome esatto, il nuovo comando sta prima di `sottofondo <id>` (che richiede almeno 2 argomenti) e il file è identico a origin/main. Esito: ok.
- `modules/sottofondo/__init__.py:366` — `riprendi_al_boot`, con i controlli già visti prima di riprendere: compito ancora aperto, cervello forte trovabile (`modules/sottofondo/__init__.py:349`), rete pronta, avvio protetto contro le eccezioni. Rischio esaminato: interferenze con la fetta 3. Il sottofondo usa la cartella `.gas_sottofondo` (`modules/sottofondo/__init__.py:40`) e la notte usa `.gas_notte` (`modules/notte/notte.py:98`). Nessuno dei due moduli cita l'altro (grep incrociato vuoto) e il merge non tocca `modules/notte/notte.py`. Esito: ok.
- `scripts/sottofondo/com.gas.sottofondo.plist:30` — parte solo all'avvio (RunAtLoad), niente riavvio continuo (KeepAlive). File identico a origin/main. Esito: ok.
- `tests/test_unit_sottofondo.py:1` — i test della fetta 2, identici a origin/main. Ho rilanciato insieme `tests/test_unit_notte.py` e `tests/test_unit_sottofondo.py`: **359 passed**. Esito: ok.
- `.claude/perimetro_review.txt:33` — aggiunge `scripts/sottofondo/` al perimetro di review. Lo rafforza, non lo indebolisce. Esito: ok.

**Risoluzione dei conflitti**
1. Il codice è identico a origin/main: il confronto tra stage e origin/main è vuoto per gas.py, modules/sottofondo, plist, test e perimetro. Le uniche differenze rispetto a main sono i file propri del ramo (`modules/notte/notte.py`, `tests/test_unit_notte.py`, report).
2. `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md` sono uguali a HEAD (diff vuoto): tenuti dal ramo come vuole la regola 3.
3. Riga «Ultimo aggiornamento» di `reports/stato_progetto.md` (riga 4): tutte le voci del ramo ci sono. La voce di main sulla fetta 2 c'è anch'essa, solo aggiornata con «PR #398 mergiata». Le voci R7 fetta 3 (riga 401) e R7 fetta 2 (riga 402) sono entrambe presenti; quella della fetta 2 è identica a main.
4. `.claude/agents/memoria_revisore.md`: nessuna riga persa né da main né da HEAD (1694 + 1698 righe confluite in 1707, 1685 in comune). Le righe #839, #840, #841, #849-MERGE-R7 e #850-R7 della fetta 2 compaiono prima di quelle della fetta 3. I numeri #839 ripetuti nei due rami erano già noti (nei report del ramo si chiamano «#839-F3»).
5. Nessun marcatore di conflitto rimasto nei file uniti.

**Rischi esclusi (non verificati)**
- Il comportamento vero all'avvio sul Mac (launchd, PATH ridotto, rete non ancora pronta) non l'ho provato: non si riproduce qui. È coperto solo dai test unitari e dalle review #839-#850-R7.
- Non ho controllato la concorrenza a runtime tra il giro di notte e un compito in sottofondo ripreso nello stesso momento, cioè due kernel attivi insieme. Non dipende da questo merge (le due fette non condividono file) e c'era già prima.
- Non ho rilanciato la suite completa: solo i due file di test indicati.

**Memoria del revisore**: ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga contatore `#851-MERGE-R7 — 2026-11-23 — APPROVATO — … Nessuna lezione nuova.` È solo nel working tree, NON in stage e NON committata, perché il merge è in corso. Va messa in stage o committata dopo il commit di merge, per esempio con `bash scripts/commit_memoria_revisore.sh`. L'impronta del diff in stage non è cambiata (e0e75617 prima e dopo la scrittura).

## §5 DELTA TEST DEL MOTORE

- Dopo il merge bc7d08df: `tests/test_unit_notte.py` + `tests/test_unit_sottofondo.py` 359 passed.
- `tests/test_unit_notte.py`: 200 → 230 (9 della fetta + 6 del 2° giro + 15 del 3° giro), tutti verdi in locale: `230 passed in 5.89s`.
- `tests/test_unit_kernel.py` (round-trip agentico), eseguito in locale DOPO il merge di main (73277ba0, prima dei commit 87006476 e 7b05ccf2 che toccano solo `modules/notte/` e i suoi test), riga reale:

```
=== RIEPILOGO: 1208 PASS, 0 FAIL ===
```

Nessun FAIL.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura:

```
completed	success	R7 fetta 3: stato dei lavori ricorrenti del giro di notte	verifica-bot	claude/r7-lavori-ricorrenti	pull_request_target	45218772891	3m10s	2026-11-23T16:38:24Z
completed	success	docs(fine-task): PR #399 secondo giro — riserve di bot e verifica est…	CI	claude/r7-lavori-ricorrenti	push	45218765483	11m47s	2026-11-23T16:38:22Z
completed	success	Merge pull request #397 from Gasss23/claude/nifty-galileo-3k7kbm — Ga…	CI	claude/nifty-galileo-3k7kbm	push	45217979161	12m8s	2026-11-23T16:34:13Z
```

Run di questo branch (`gh api .../actions/runs?branch=claude/r7-lavori-ricorrenti`, output reale):

```
45218772891 3b188028 verifica-bot pull_request_target completed/success
45218765483 3b188028 CI push completed/success
45217587661 492f7e20 verifica-bot pull_request_target completed/cancelled
45217586568 b7ae5d42 verifica-bot pull_request_target completed/success
45217578563 492f7e20 CI push completed/success
45217179154 b7ae5d42 verifica-bot pull_request_target completed/skipped
45217146013 b7ae5d42 CI push completed/failure
```

Mappatura commit→run:
- b7ae5d42: CI 45217146013 failure (atteso: commit di codice senza handoff aggiornato, handoff-check rosso); verifica-bot 45217179154 skipped.
- 492f7e20: CI 45217578563 success; verifica-bot 45217586568 (registrata con head b7ae5d42) ha pubblicato il check success sul 492f7e20 (1° verdetto, solo BASSE); 45217587661 cancelled.
- 3b188028: CI 45218765483 success; verifica-bot 45218772891: il job è success, ma il check `verifica-bot` pubblicato sullo SHA è failure (2° verdetto, V-1 MEDIA, corretta in 7b05ccf2).
- 113a2fde, 2246dd88, ba513ece, f3a6168e, 73277ba0, 49ce5f74, 3599a7d4, 87006476, 26a27136, f78682bf, 7b05ccf2: nessuna run propria (pushati insieme al commit di testa, o non ancora pushati).
- ae2ea9e0: CI success (unit-suite, handoff-check); check `verifica-bot` success col 3° verdetto APPROVATO CON RISERVE senza ALTA/MEDIA.
- bc7d08df e il commit di fine-task di questo giro: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- V-1 MEDIA del bot su 3b188028 ([review](https://github.com/Gasss23/Gas/pull/399), «Pipeline esausta» copriva motivi del lavoro): CHIUSA (7b05ccf2, #848-R7). R-847R7-1 MEDIA e R-847R7-2 BASSA (compromesso dichiarato in `reports/setup_notte.md`): CHIUSE.
- R-844M-1 MEDIA (#844-MERGE): CHIUSA (87006476, #845-R7). R-843-1 BASSA: CHIUSA. R-845R7-1/2 BASSE: CHIUSE (#846-R7 APPROVATO, nessuna riserva).
- Verifica esterna #399 su 3b188028 ([commento](https://github.com/Gasss23/Gas/pull/399#issuecomment-7107495837)): V-1 BASSA (guasti esterni deterministici ritentati per sempre) CHIUSA con il tetto dei 14; V-2 COSMETICA (rilancio a mano con guasto esterno toglieva la pausa) CHIUSA con R-843-1; V-3 = R-839-3.
- Verdetti precedenti (bot e verifica esterna su 492f7e20; #839-F3, #842, #843): chiusi nel 2° giro, salvo R-839-3.
- R-839-3 COSMETICA — kernel non creato: stato non aggiornato; «fermo fino al» con data passata o 01/01. Aperta.
- Da sapere (non verificato, dalle review #845/#846-R7): sulla VPS con «Sempre Opus» acceso e Opus non configurato, ogni lavoro della notte fallisce per guasto esterno; dopo 14 notti vanno tutti in pausa, poi un tentativo a settimana.
- Bot su ae2ea9e0 (APPROVATO CON RISERVE): V-1 BASSA (un compito tagliato dal tetto di tempo del GIRO conta come fallimento suo) aperta; V-2 COSMETICA (descrizione della PR e §2/§6 dell'handoff non aggiornati) corretta. Verifica esterna su ae2ea9e0 ([commento](https://github.com/Gasss23/Gas/pull/399#issuecomment-7107847945)): V-1 BASSA («ko di fila» non azzerato dai guasti esterni) e V-2 BASSA (filtro per sottostringa) aperte; V-3 COSMETICA (NB triplo) corretta.
- Riserve delle altre chat (CRM, Voce) e della PR #398: in `reports/stato_progetto.md`.
