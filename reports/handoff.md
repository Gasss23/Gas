# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-27 — Mani fetta 19: prova della lettura con lexbor (R-ve246-5), spenta per default, più secondo giro (merge di main, test dell'isolamento del figlio), chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #275 (https://github.com/Gasss23/Gas/pull/275). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5026812511","url":"https://github.com/Gasss23/Gas/pull/275"}`); `gh` nel cloud non è autenticato. Merge da solo solo con APPROVATO pulito del bot sull'head. Il merge non accende niente.
2. Accendere la lettura con lexbor? Prima: R-521-1 e R-521-2, un'occhiata ai 5 casi con `<select>`, e la chat Motore (selectolax in requirements e CI, `GAS_WEB_LEXBOR=1` sul VPS).
3. Poi, una alla volta: R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **Prova lexbor (R-ve246-5, decisione dell'operatore «vai con la 2, parti dalla prova»)**: `FATTA` — `modules/web/lexbor.py` (processo figlio con tempo e memoria limitati, spenta per default, sonda del figlio, fail-safe), `leggi.py` con `_testo_e_titolo` estratta senza cambiarla, 20 test nuovi; misure in ultimo_report.
- **R-520-1/2/3 (review #520)**: `FATTA`.
- **R-520-4 COSMETICA, R-521-1/2 BASSE, R-521-3 COSMETICA**: `DEFERITA — da sistemare prima di un'eventuale accensione; la prova è spenta e vanno nel verso sicuro`.
- **Secondo giro (bot e verifica esterna #275, entrambi APPROVATO CON RISERVE)**: V-1 ve conflitto con main → `FATTA` (merge 018c860, review #522 APPROVATO); V-2 ve isolamento del figlio senza test → `FATTA` (95fda3d, review #523 e #524); V-1 bot / V-3 ve selectolax assente in CI → `DEFERITA — richiesta alla chat Motore prima di accendere`; V-2 bot / V-4 ve numeri locali contro CI → `FATTA` (spiegati in ultimo_report); V-5 ve §6 → `FATTA`; R-524-1 COSMETICA → `DEFERITA`.
- **Accensione della lettura con lexbor**: `DEFERITA — decisione dell'operatore e richiesta alla chat Motore (requirements, CI, VPS)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   9 +++++++++
 modules/web/leggi.py               |  75 +++++++++++++++++++++++++++++++++++++++++++++++----------------------------
 modules/web/lexbor.py              | 119 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  11 ++++++-----
 reports/handoff.md                 | n/d (commit finale)
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  58 ++++++++++++++++++++++++++++++++++++++++++++++++++++------
 tests/test_unit_web_lexbor.py      | 166 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat` preso con i report in stage, prima del commit finale.

## §3 GIT LOG --ONELINE (sessione)

```
95fda3d test(web): isolamento del processo figlio di lexbor fissato da test (V-2 ve #275)
f2a9509 chore(revisore): memoria review #524 — APPROVATO CON RISERVE
c3a5292 chore(revisore): memoria review #523 — APPROVATO CON RISERVE
018c860 Merge origin/main (1422021, PR #271 e #273) in claude/peaceful-lovelace-0w2b7q (PR #275)
4557f31 docs(fine-task): Mani fetta 19 — report, handoff, stato (PR #275, review #520-#521)
eb2df98 feat(web): prova della lettura con lexbor in un processo figlio, spenta per default (R-ve246-5, fetta 19 Mani)
14716d9 chore(revisore): memoria review #521 — APPROVATO CON RISERVE
8fe2253 chore(revisore): memoria review #520 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore eb2df98: review #520 sul primo diff e #521 dopo la chiusura di R-520-1/2/3. Merge 018c860 (entrano da main file del perimetro): review #522. Commit motore 95fda3d (test dell'isolamento del figlio): review #523 e #524. Verdetti integrali:

### Review #520 (chat Mani) — primo diff staged

## VERDETTO: APPROVATO CON RISERVE

Review #520 (chat Mani). Diff staged su claude/peaceful-lovelace-0w2b7q: fetta 19, prova di lexbor spenta per default. Ho fatto le tre letture obbligatorie: CLAUDE.md, stato_progetto.md (selettivo, §fetta 19 e fette 1-18) e la memoria (lezioni recenti su leggi.py, oracoli e subprocess).

**Elementi del diff esaminati**

1. `modules/web/leggi.py:1381` — estrae `_testo_e_titolo`, cioè la lettura con html.parser e il ripiego. Rischio: che lo spostamento cambi la logica. Ho confrontato il blocco vecchio (rientro tolto) con quello nuovo e cambiano solo i `return` al posto delle assegnazioni. Nel ripiego il titolo resta `""` come prima: il vecchio `titolo = ""` di `_componi` restava valido perché il ValueError arriva sempre prima che il titolo venga assegnato. Esito: ok.
2. `modules/web/leggi.py:1426` — lexbor entra in gioco solo se `not xhtml and _lexbor.attivo()`, altrimenti si usa la lettura di sempre. Rischio: effetti da spenta e uscita dai delimitatori. Da spenta `selectolax` non viene importato: con `-X importtime` non compare, e `'selectolax' in sys.modules` dà False sia con la variabile accesa sia spenta. Resta solo `find_spec`, che è economico. Sul ramo lexbor ho provato i finti marcatori nel corpo e nel titolo (neutralizzati), il taglio a `MAX_CARATTERI` (troncato=True) e a `MAX_TITOLO` (200 caratteri), i caratteri di controllo e bidi nel titolo (tolti). Il testo resta dentro NON FIDATO. Esito: ok.
3. `modules/web/lexbor.py:88` — processo figlio `sys.executable -I -c`, env vuoto, pagina su stdin, timeout 4 s. Rischi esaminati:
   - zombie: `run()` su timeout fa kill e wait, e ho contato 0 zombie dopo le prove;
   - thread: 8 letture in parallelo, tutte corrette;
   - stdout grande: con `ensure_ascii` l'uscita resta sotto ~12 MB per 2 MB di pagina e viene letta con communicate, quindi niente blocchi;
   - `-I`: implica `-P`, quindi la cwd non entra in `sys.path` e nessun modulo piantato lì viene caricato;
   - pagina su stdin e non in argv: niente iniezione di argomenti;
   - errori e timeout: finiscono tutti in un warning e in None (FAIL-SAFE §9);
   - `KeyboardInterrupt`: non viene catturato, ed è giusto così.

   Esito: ok, con la riserva R-520-3.
4. `modules/web/lexbor.py:48` — esclude i title dentro svg/math. Una sonda: `<svg><foreignObject><title>X</title>` scarta un title HTML che il browser userebbe. È una perdita nel verso sicuro. Esito: riserva cosmetica.
5. `tests/test_unit_web_lexbor.py:52` e `tests/test_unit_web_lexbor.py:23` — casi di R-ve246-5 e test «da spenta non parte». I test passano. Ho però provato due mutanti nel ramo lexbor, su una copia nello scratchpad: «senza `[:MAX_TITOLO]`» sopravvive a tutto; «corpo senza `_pulisci`» fa passare tutti i 18 test nuovi e lo prende solo la suite vecchia accesa (14 FAIL contro gli 11 di base), che nessuno fa girare. Esito: riserva R-520-1.

**Prove rifatte**
- Suite web su 3.13 (con selectolax): 459 passed, 1 skipped. Su 3.11 (senza): 443 passed, 17 skipped.
- Con `GAS_WEB_LEXBOR=1`: 11 FAIL. Sono i 3 test dei log e 8 casi frameset/template.
- Ho controllato a mano che `<p>A</p><frameset/>SEGRETO` lo mostri anche il browser: dopo il testo «A» il `<frameset>` viene ignorato.
- Il perimetro è rispettato: solo `modules/web/` e `tests/test_unit_web_lexbor.py`. Nessun guardrail del motore è toccato.

**Riserve (vanno in stato_progetto.md)**
- **R-520-1 BASSA (test):** i 18 test nuovi non fissano `_pulisci` e `[:MAX_TITOLO]` sul ramo lexbor (i due mutanti del punto 5). Servono un test con un finto marcatore nel corpo e nel titolo e uno con un titolo lungo, a lexbor acceso.
- **R-520-2 BASSA (doc):** la docstring di leggi.py, in `modules/web/leggi.py:28` e nei «Limiti dichiarati», dice ancora «solo stdlib» e ~15 s. Da accesa il caso peggiore è 12 s di rete + 4 s del figlio + fino a 3 s di ripiego, circa 19 s. Va dichiarato.
- **R-520-3 BASSA:** `modules/web/lexbor.py:32` controlla la libreria nel padre con `find_spec`, ma il figlio parte con `-I` ed env vuoto. Ho provato un venv pulito con selectolax raggiungibile solo da PYTHONPATH: il padre la dà per presente, il figlio esce con 1, e ogni pagina paga circa 40 ms più un warning ripetuto. Non crasha, ma prima di accenderla serve un controllo in doctor o una sonda reale del figlio, una volta sola.
- **R-520-4 COSMETICA:** un title HTML dentro foreignObject viene scartato (perdita, verso sicuro).

**Rischi esplicitamente esclusi**
- `RLIMIT_AS` su macOS: non verificato, non riproducibile qui. Se lì `setrlimit` fallisce, il figlio esce con 1 e si torna sempre alla lettura di sempre, senza crash.
- Venv con selectolax installato dentro: non provato (servirebbe pip in rete). Per costruzione `-I` tiene i site-packages del venv.
- Le misure dell'autore con l'oracolo (60 mila pagine, html5lib, 131 pagine di documentazione) non le ho rifatte: sono script fuori dal repo. Ho rifatto solo le sonde puntuali.

Memoria: aggiunte la riga #520 e 2 lezioni, committate da sole con lo script (8fe2253). I file del diff restano in stage, come chiesto. Ora `git status` mostra anche `reports/stato_progetto.md` modificato e non in stage: non l'ho toccato io.

### Review #521 (chat Mani) — sul diff committato in eb2df98

## VERDETTO: APPROVATO CON RISERVE

Review #521 (chat Mani): ri-review del diff in stage su claude/peaceful-lovelace-0w2b7q, dopo la #520. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (le parti sulla fetta 19 e sulle R-520) e .claude/agents/memoria_revisore.md, applicando anche le due lezioni del 2026-10-27.

**Elementi del diff esaminati**
1. `modules/web/lexbor.py:82` — la sonda del figlio in `attivo()` parte una sola volta e il risultato resta in `_FIGLIO_OK`.
   - Rischi esaminati: chiamate da più thread, costo, sonda in timeout, partenza da spenta.
   - Prove rifatte con una spia su `subprocess.run`:
     - da spenta: 0 figli lanciati e `_FIGLIO_OK` resta None;
     - costo: circa 35 ms una volta sola, la seconda chiamata non lancia figli;
     - 8 thread insieme alla prima chiamata: 16 figli, cioè 8 sonde più 8 letture; tutti leggono "VIS", nessun crash, esito finale True;
     - sonda in timeout (TEMPO_MAX=0.001): False, e resta False anche dopo aver rimesso 4 s; nessun processo zombie.
   - Esito: riserva (R-521-1, R-521-2).
2. `modules/web/leggi.py:1431` — lexbor si usa solo se la pagina non è XHTML e `attivo()` è vero; `attivo()` viene valutato prima di `testo_visibile`, quindi da spenta non parte niente. Il ramo lexbor passa da `_pulisci` e dal tetto `MAX_TITOLO`.
   - Rischio esaminato: tetto e pulizia non coperti dai test (era la R-520-1).
   - Mutanti rifatti sui 20 test nuovi: senza `_pulisci` sul corpo 1 failed, senza `[:MAX_TITOLO]` 1 failed.
   - Esito: ok, R-520-1 chiusa.
3. `modules/web/lexbor.py:97` — `testo_visibile` passa il lavoro a `_esegui`, la stessa funzione usata dalla sonda.
   - Mutanti rifatti: sonda ripetuta (`if True:`) 1 failed, acceso sempre (`return True`) 1 failed.
   - Esito: ok, R-520-3 chiusa.
4. `tests/test_unit_web_lexbor.py:66` — il test nuovo usa bidi, spazi doppi, un finto marcatore nel corpo e un titolo di 500 caratteri.
   - Ho controllato che le asserzioni distinguano davvero il codice giusto da quello sbagliato.
   - Esito: ok.
5. `tests/test_unit_web_lexbor.py:85` — la chiamata reale ad `attivo()` dopo `monkeypatch.undo()` scrive `_FIGLIO_OK=True` fuori dal controllo del monkeypatch, quindi il valore resta per i test successivi.
   - Ho controllato l'effetto sugli altri test: nessuno, perché True è il valore giusto quando selectolax c'è.
   - Esito: riserva cosmetica (R-521-3).
6. `modules/web/leggi.py:29` — la docstring ora dice dell'eccezione «in prova, spenta per default» e del caso peggiore da accesa (12 + 4 + 3 s).
   - Esito: ok, R-520-2 chiusa.

**Prove rifatte**
- Suite web su Python 3.13.16 con selectolax 1.0.2: 461 passed, 1 skipped.
- Suite web su Python 3.11 senza selectolax: 443 passed, 19 skipped.
- Coincidono con quelle dell'autore.
- Dopo i mutanti i file sono tornati com'erano e l'index è intatto.

**Riserve**
- R-521-1 BASSA: la sonda non ha un lock. Con N thread alla prima chiamata partono N sonde, e se falliscono il warning esce fino a N volte. «Una volta sola» vale solo in sequenza. Va nel verso sicuro (costa circa 35 ms a sonda, il risultato è lo stesso). Se serve si chiude con un `threading.Lock` attorno alla sonda.
- R-521-2 BASSA: un fallimento passeggero della sonda (per esempio un timeout di 4 s all'avvio a freddo su una VPS carica) spegne la prova per tutta la vita del processo. Va nel verso sicuro e lascia un warning, ma la prova smette di raccogliere misure. Da valutare se distinguere il timeout dall'ImportError, o riprovare dopo un po'.
- R-521-3 COSMETICA: `test_sonda_del_figlio` lascia `_FIGLIO_OK=True` fuori dal monkeypatch (riga 85). La riga 82, prima di `undo()`, non serve.
- Nota COSMETICA: il messaggio «oltre %.0f s» stampa «0 s» quando il tempo massimo è sotto 0,5 s. Succede solo nei test.
- R-520-4 COSMETICA (un `title` dentro foreignObject viene scartato): resta aperta, scritta correttamente in stato_progetto.

**Rischi esplicitamente esclusi**
- Non ho verificato il caso di selectolax visibile solo via PYTHONPATH in un venv pulito: qui la libreria è installata nel sistema. Ho verificato solo che la sonda finta (ImportError) spenga la prova.
- Non ho verificato tempi e memoria della sonda su VPS: non si riproducono in dev.
- Non ho rigirato la suite vecchia da accesa (gli 11 FAIL attesi): mi fido della #520, e quel codice non è cambiato in questo delta.

**Memoria**
- Riga #521 e una lezione nuova (provare le cache «una volta sola» con N thread alla prima chiamata, contando i lanci reali) aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md.
- Committate da sole con `scripts/commit_memoria_revisore.sh` (commit 14716d9).
- I file del diff (modules/web/leggi.py, modules/web/lexbor.py, tests/test_unit_web_lexbor.py) restano in stage. reports/stato_progetto.md resta modificato e fuori stage, come l'ho trovato.

### Review #522 (chat Mani) — merge di origin/main 1422021, commit 018c860

## VERDETTO: APPROVATO

Review #522 (chat Mani). Ho controllato il merge di origin/main 1422021 (PR #271 e #273) nel branch claude/peaceful-lovelace-0w2b7q (PR #275, HEAD 4557f31). Il merge è ancora in corso e la stage è quella di adesso.

Ho letto le tre fonti obbligatorie: CLAUDE.md (sezioni 5, 8 e 9), le sezioni rilevanti di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `gas.py:4126` — `_lead_fermi` legge i lead con `leggi_contatti`; se la lettura dà None risponde «NON letto». Rischio: un blob mescolato fra PR e main. Esito **ok**: il blob in stage è identico a MERGE_HEAD (c1bce57) e la PR non toccava gas.py.
- `modules/memory/store.py:1225` — `leggi_contatti` restituisce None su `sqlite3.Error`/`OSError`, e `lista_contatti` la avvolge. Rischio: eccezione non intercettata (sezione 9). Esito **ok**: il warning finisce nel log e c'è il fallback. Il blob è identico a main (359d0d8). Era già stato revisionato nella #520/#521 della chat Notte.
- `modules/notte/notte.py:545` — lo stato del mattino usa `leggi_contatti`, e None diventa «non letti». Rischio: una mescolanza con l'altra modifica di main (`_dollari`, PR #271). Esito **ok**: il blob è identico a main (c7eafad).
- `tests/test_unit_kernel.py:1` e `tests/test_unit_notte.py:1` — i test della chat Notte. Esito **ok**: blob identici a MERGE_HEAD (67140d2, ff17838).
- `modules/web/lexbor.py:82` (contesto, codice della PR) — esito **ok**. `modules/web/leggi.py`, `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py` non compaiono in `git diff --cached HEAD`, quindi il merge non li tocca e restano quelli della PR. Fra il codice web e quello di contatti/notte non ci sono dipendenze.

**Controlli meccanici**
1. **File del perimetro e report notte:** stanno tutti in stage con il blob di MERGE_HEAD. Vale anche per reports/coda_notte.md e reports/report_notte.md. Nessuna mescolanza.
2. **Report tenuti dalla PR:** reports/handoff.md, reports/ultimo_report.md e reports/diff_sessione.md non compaiono nel diff cached rispetto a HEAD, quindi sono rimasti quelli della PR (--ours).
3. **memoria_revisore.md:** nessuna riga persa né rispetto a HEAD né rispetto a MERGE_HEAD (confronto per righe ordinate). Le righe #520 e #521 di Mani e di Notte ci sono tutte.
4. **stato_progetto.md:**
   - Rispetto a HEAD cambia una sola riga, «Ultimo aggiornamento»: è stata sostituita dalla versione unita, con la voce Mani fetta 19 in testa seguita dalla catena di main (voci Notte #273 e #271 comprese).
   - Rispetto a MERGE_HEAD cambiano due righe: la stessa «Ultimo aggiornamento» e la voce «fetta 18». Quella della fetta 18 arriva dalla PR: nella base è uguale a main (stesso md5) e la PR l'ha cambiata, quindi il merge a tre vie l'ha presa giustamente dalla PR.
5. **Marcatori di conflitto:** nessuno nei file in stage.

**Prove rifatte da me (Python 3.13)**
- **Test web e notte:** `pytest tests/test_unit_web_*.py tests/test_unit_notte.py` dà 655 passed e 1 skipped, come nella prova dell'autore.
- **Test del kernel:** `python3 tests/test_unit_kernel.py` dà 1038 PASS e 1 FAIL. Il FAIL è T31g (GAS_VECTORS=1, `vectors=VectorStore`), un problema dell'ambiente già notato nella #510. Non l'ho riprodotto su un worktree pulito di main: mi sono fidato della prova dell'autore.

**Rischio escluso**
Non ho rifatto la review semantica del codice di PR #271/#273, né i loro mutanti: sono già stati revisionati nella #515/#516 e #520/#521 della chat Notte. Qui ho verificato solo che i blob entrino intatti.
Non ho verificato nemmeno il comportamento in CI e con Python 3.11 dopo il merge, perché in questa sessione ho girato solo con 3.13.

**Wall of Shame**
Nel diff non c'è slicing diretto della history né simulazione dell'output dei tool. Il cap di 10 iterazioni, il cap di 8k e `_get_window` non sono toccati.

**Memoria del revisore**
Ho aggiunto la riga #522 in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, senza lezioni nuove, e l'ho messa in stage con `git add`. Lo script di commit non l'ho usato perché il merge è in corso. La riga segnala che le chat Mani e Notte hanno usato gli stessi numeri #520 e #521, e che il contatore riprende da #522.

### Review #523 (chat Mani) — primo diff staged dei test di isolamento

## VERDETTO: APPROVATO CON RISERVE

Review #523 (chat Mani). Diff in stage: solo tests/test_unit_web_lexbor.py, 29 righe aggiunte, due test nuovi. Chiude V-2 BASSA della verifica esterna #275. Prima ho letto CLAUDE.md (sezioni 1, 5, 8, 10), la sezione fetta 19 di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

**Cosa ho esaminato**

- `tests/test_unit_web_lexbor.py:140` — mette un `resource.py` in tmp_path e fa `monkeypatch.chdir` lì dentro. Controlla che la lettura riesca e che il file spia non venga creato.
  - Rischio esaminato: che il test non prenda la rimozione di `-I`, e che lasci file o cambi la cartella per gli altri test.
  - Esito: ok. Senza `-I` il `resource.py` piantato oscura quello di sistema, quindi `setrlimit` non esiste, il figlio restituisce None e la prima asserzione fallisce. tmp_path lo gestisce pytest, la cwd la ripristina monkeypatch. Dopo la suite `git status` è pulito.
- `tests/test_unit_web_lexbor.py:151` (asserzioni in `tests/test_unit_web_lexbor.py:163` e `tests/test_unit_web_lexbor.py:164`) — spia su `subprocess.run` (argv[1] == "-I", env == {}), poi tetto di 20 MiB e risultato None.
  - Rischio esaminato: che la spia resti attiva dopo il test, visto che `lexbor.subprocess` è il modulo globale di sistema. E che il tetto fallisca per un motivo diverso dalla memoria, o in modo instabile.
  - Esito: riserva. Il patch è globale, ma dura solo il test e monkeypatch lo ripristina; anche `MEMORIA_MAX` viene ripristinato. `_FIGLIO_OK` non viene toccato, perché `testo_visibile` non passa da `attivo()`. Ho misurato la soglia lanciando il vero `_FIGLIO` con `-I` e ambiente vuoto:
    - il figlio riesce da 23 MiB in su;
    - a 22 MiB si ferma con SelectolaxError («Can't parse CSS selector»);
    - a 20 MiB con MemoryError a metà import;
    - da 16 MiB in giù con ImportError «failed to map segment».

    Tutti gli errori vengono dalla memoria e il risultato è stabile qui (5 ripetizioni verdi). Però il margine è di circa 3 MiB, con motivi diversi vicino alla soglia: diventa R-523-1.
- Contesto: `modules/web/lexbor.py:41` (`setrlimit` nel figlio) e `modules/web/lexbor.py:105` (avvio con `-I`, `env={}` a `modules/web/lexbor.py:107`). Il codice di produzione non è toccato: dopo i mutanti ho riportato il file all'originale e `git diff` è vuoto.

**Mutanti rifatti da me** (con selectolax, Python 3.13)
- Senza `-I`: 2 failed.
- Con l'ambiente del padre (`env=dict(os.environ)`): 1 failed.
- Senza `setrlimit`: 1 failed.
- Tetto spostato DOPO l'import di selectolax: sopravvive. Lo considero equivalente, perché il tetto vale comunque sul lavoro di lexbor.

**Suite**
- Web (3.13.16, con selectolax): 464 passed, 1 skipped (l'autore ne riporta 463; differenza dovuta al filtro `-k web`, non indagata).
- tests/test_unit_web_lexbor.py su 3.11.17 (senza selectolax): 2 passed, 20 skipped.

Antipattern della sezione 5: nessuno slicing della history né simulazione dei tool (sono test che lanciano il figlio vero). Guardrail (cap 10 iterazioni, 8k, `_get_window`) non toccati.

**Riserve**
- R-523-1 (chat Mani) BASSA: con 20 MiB il test resta a ~3 MiB dalla soglia di riuscita, e quella soglia dipende dalla build (interprete, glibc, versione di selectolax). Altrove il figlio potrebbe riuscire anche a 20 MiB e il test darebbe un rosso falso; il contrario, un verde falso, non può succedere. Rimedio: un tetto sotto l'ingombro dell'interprete (es. `4 << 20`, il figlio occupa 15,6 MB già all'avvio). Così il motivo è uno solo (la libreria non si carica) e il margine è circa 5 volte.
- R-523-2 (chat Mani) COSMETICA: la fixture `acceso` non serve ai due test, perché `testo_visibile` non passa da `attivo()`.

**Rischi esclusi**
- Comportamento di RLIMIT_AS su macOS non verificato: qui c'è solo Linux. Su Darwin il limite potrebbe non essere applicato, e con selectolax installato sul Mac il test del tetto potrebbe fallire.
- Python 3.12, e 3.11 con selectolax, non verificati: non installati in questo ambiente.

**Memoria**
- Aggiunte in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga contatore #523 e una lezione sui test a tetto di risorsa: misurare la soglia di riuscita e il motivo dell'errore a più valori.
- Committata da sola con `scripts/commit_memoria_revisore.sh` (commit c3a5292).
- `tests/test_unit_web_lexbor.py` resta in stage, intatto.

### Review #524 (chat Mani) — sul diff committato in 95fda3d

## VERDETTO: APPROVATO CON RISERVE

Ho letto per intero, prima della review, CLAUDE.md (sezione 5), reports/stato_progetto.md e la mia memoria.

**Elementi del diff esaminati**
- `tests/test_unit_web_lexbor.py:165`: ora il tetto del test è `4 << 20` (4 MiB) invece di 20 MiB. Il rischio era che il figlio fallisse per motivi diversi, o per un motivo che dipende da come è compilata la libreria. Ho lanciato 20 volte il figlio (`lexbor._FIGLIO`, `-I`, `env={}`) a 4 MiB: 20 volte su 20 esce con codice 1 e sempre per lo stesso motivo. Il motivo è `ImportError: ... selectolax/lexbor.cpython-313-x86_64-linux-gnu.so: failed to map segment from shared object` alla riga 4 del figlio: il limite RLIMIT_AS impedisce di mappare in memoria il .so. Il tetto sta sotto l'ingombro dell'interprete all'avvio (circa 15,6 MB, misurato in #523), quindi il margine dalla soglia di riuscita (23 MiB) è ampio. Esito: ok, R-523-1 chiusa.
- `tests/test_unit_web_lexbor.py:151`: verificato che il mutante resti preso. Ho tolto `setrlimit` da `modules/web/lexbor.py:41`: 1 failed, proprio questo test. Ho dato al figlio l'ambiente del padre (tolto `env={}` in `modules/web/lexbor.py:107`): 1 failed. Ho spostato il tetto DOPO l'import di selectolax: il mutante sopravvive. È lo stesso caso di #523 e lo considero equivalente, perché il tetto vale comunque sulla lettura della pagina. Dopo i mutanti ho ripristinato `modules/web/lexbor.py` (0 diff da HEAD). Esito: ok.
- `tests/test_unit_web_lexbor.py:140` e `tests/test_unit_web_lexbor.py:151`: i due test non usano più la fixture `acceso`. Il rischio era che dipendessero da `GAS_WEB_LEXBOR` o da `_FIGLIO_OK`. Non dipendono: `testo_visibile` (`modules/web/lexbor.py:90`) guarda solo `_DISPONIBILE` e non passa da `attivo()`, e il marcatore `con_lexbor` salta i test se la libreria manca. Nel diff `acceso` compare solo nella riga di contesto di un test vecchio. Esito: ok, R-523-2 chiusa.

**Prove eseguite**
- `tests/test_unit_web_lexbor.py`: 22 passed con Python 3.13.16; 2 passed e 20 skipped con Python 3.11 (selectolax non c'è).
- Il gruppo `-k "tetto or cartella"`, ripetuto 5 volte: sempre 2 passed.
- Nessun Wall of Shame: il diff tocca solo un test, nessun taglio della cronologia, nessun output di tool simulato.

**Riserve**
- R-524-1 COSMETICA: la docstring del test alla riga `tests/test_unit_web_lexbor.py:151` dice che sotto l'ingombro dell'interprete il figlio «non riesce nemmeno a partire». In realtà il figlio parte, esegue `setrlimit` e cade all'import di selectolax. Basta riformulare, ad esempio «non riesce nemmeno a caricare la libreria».

**Rischio escluso**
- Non ho verificato il motivo dell'errore a 4 MiB su altre build o versioni di Python (VPS, CI con selectolax, macOS). Qui la libreria c'è solo per Python 3.13 e la CI la salta. Su macOS il limite RLIMIT_AS viene applicato in modo diverso. Comunque, una build diversa può dare al massimo un falso rosso, mai un falso verde: il mutante senza tetto riesce sempre.

**Memoria**
- Ho aggiunto in fondo a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga contatore #524 (nessuna lezione nuova).
- L'ho committata da sola con `scripts/commit_memoria_revisore.sh` (commit f2a9509).
- `tests/test_unit_web_lexbor.py` resta in stage, non è stato toccato.

## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati):
- `python3 -m pytest -q tests/test_unit_web_*.py`, codice finale 95fda3d: main `441 passed, 1 skipped` → ramo `463 passed, 1 skipped in 26.61s` (3.13.16, con selectolax); `443 passed, 21 skipped in 25.01s` (3.11 locale, senza selectolax; in CI un test che si salta solo in locale gira, quindi la CI dà 1 passed in più e 1 skipped in meno). +22 test in `tests/test_unit_web_lexbor.py`.
- Dopo il merge di main (018c860): `pytest tests/test_unit_web_*.py tests/test_unit_notte.py` `655 passed, 1 skipped in 30.64s`; `python3 tests/test_unit_kernel.py` `=== RIEPILOGO: 1038 PASS, 1 FAIL ===` (T31g, GAS_VECTORS=1, identico su un worktree pulito di origin/main).
- Isolamento del figlio (95fda3d), mutanti: senza `-I` → `2 failed, 20 passed`; con l'ambiente del padre → `1 failed, 21 passed`; senza tetto di memoria → `1 failed, 21 passed`.
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin): `451 passed, 11 skipped in 24.30s`.
- Suite vecchia con `GAS_WEB_LEXBOR=1`: `11 failed, 430 passed, 1 skipped` (3 test dei log del percorso html.parser; 8 casi frameset/template dove il browser mostra il testo, lexbor e html5lib concordi).
- Mutazioni del ramo lexbor (uscita di pytest sui 20 test): corpo senza `_pulisci` → `1 failed, 19 passed`; titolo senza tetto → `1 failed, 19 passed`; senza sonda → `1 failed, 19 passed`; sonda ripetuta → `1 failed, 19 passed`; acceso sempre → `1 failed, 19 passed`; titolo non nascosto → `1 failed, 19 passed`; nascosti ignorati → `5 failed, 15 passed`; script spenti → `1 failed, 19 passed`; titolo di svg accettato → `1 failed, 19 passed`; blocchi senza a capo → `1 failed, 19 passed`; anche in XHTML → `1 failed, 19 passed`.
- Misure della prova (script nello scratchpad): oracolo html5lib su 60 mila pagine senza template/svg/math, seed 7 `FUGHE oggi 48, lexbor 0; PERDITE oggi 2975, lexbor 1860`, seed 8 `FUGHE oggi 40, lexbor 3; PERDITE oggi 2907, lexbor 1765`, seed 9 `FUGHE oggi 41, lexbor 2; PERDITE oggi 2831, lexbor 1764`; corpus `pagine 131, testo identico (parole) 127, diverse 4`, `tempo totale oggi 10.57s, lexbor 15.76s`; robustezza `seed 1: 100000 pagine senza eccezioni né crash`, `seed 2: 100000 pagine senza eccezioni né crash`; lexbor in processo `div 100k 23.00s`, `attr 100k 36.26s`, col figlio `div 100k 4.01s -> None`, `attr 100k 4.01s -> None`.

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run lette dall'integrazione GitHub (`actions_list`, workflow ci.yml, branch claude/peaceful-lovelace-0w2b7q):

```
40430887843  CI  push  in_progress  —        95fda3d  2026-10-27T01:09:31Z
40430137225  CI  push  completed    success  018c860  2026-10-27T01:02:12Z
40428232738  CI  push  completed    success  4557f31  2026-10-27T00:43:46Z
40428033003  CI  push  completed    failure  eb2df98  2026-10-27T00:41:49Z
```

Mappatura commit→run:
- `8fe2253`, `14716d9`: nessuna run su questo SHA (pushati insieme a `eb2df98`).
- `eb2df98` → run CI 40428033003 failure: `handoff-check` allo step «Run check_handoff (versione main)», atteso (il commit motore non conteneva l'handoff); `unit-suite` success (V-5 ve #275).
- `4557f31` → run CI 40428232738 success; verifica-bot success (APPROVATO CON RISERVE).
- `018c860` → run CI 40430137225 success.
- `c3a5292`, `f2a9509`: nessuna run su questo SHA (pushati insieme a `95fda3d`).
- `95fda3d` → run CI 40430887843, in corso alla scrittura dell'handoff.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-520-4 COSMETICA: un `title` HTML dentro foreignObject si scarta (perdita, verso sicuro).
- R-521-1 BASSA: sonda del figlio senza lock (N thread → N sonde).
- R-521-2 BASSA: un fallimento passeggero della sonda spegne la prova per tutta la vita del processo.
- R-521-3 COSMETICA: `test_sonda_del_figlio` lascia `_FIGLIO_OK=True` fuori dal monkeypatch.
- R-524-1 COSMETICA: la docstring del test del tetto dice «non riesce a partire», in realtà il figlio non carica la libreria.
- V-1 bot / V-3 ve #275 BASSA: in CI selectolax manca e 18 test lexbor si saltano: richiesta alla chat Motore prima di accendere.
- 5 casi con `<select>` in cui lexbor e html5lib divergono (standard cambiato di recente): da guardare prima di accendere.
- Restano decisioni dell'operatore: accensione della lettura con lexbor; R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s; R-518-1 e riaccensione di R-469-1 con noscript (superate se si accende lexbor).
