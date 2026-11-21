# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-21 — CRM: note minori dopo le PR #388 e #389

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #391 (https://github.com/Gasss23/Gas/pull/391), aperta dopo il push di ef51e72b con l'etichetta «verifica». L'operatore ha detto in chat «sì, mergia la #391». Su 1d29e7b6 CI verde, bot neutral (APPROVATO CON RISERVE), verifica esterna APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/391#issuecomment-7067488956); poi conflitto coi report di main dopo la PR #392 (funnel, solo documenti), risolto col merge ba074391. L'operatore ha chiesto «sistema anche le note minori». Il test del bot tocca la macchina del bot: verifica-bot sarà neutral e il merge lo decide l'operatore.
2. Da decidere: aggiungere a `_GRAVI` del bot anche «alto», «severo», «serio», «elevato» (nota del revisore #831).

---

## §1 SCOPE & ESITO FETTE

- **Note minori**: FATTA, commit cd46a249 (review #834 APPROVATO CON RISERVE, riserve corrette nello stesso diff e riviste in #835 APPROVATO CON RISERVE) e f126fbd5 (R-835-1, review #836 APPROVATO CON RISERVE).
  - R-830-1 (bot #388 cfa0156a V-1): resto in chiaro di prima dell'ultimo avvio tolto anche col PID riusato.
  - Verifica esterna #388 (71137d27) V-1: pulizia prima della password documentata; V-2: file da ripristinare illeggibile → ErroreCRM con un messaggio chiaro (il CLI prendeva già OSError: il guadagno è il testo).
  - Bot #388 (71137d27) V-3: motivo «errore durante la copia cifrata (X)», avviso senza «riuscita» doppio. V-2 (nota del revisore superata nell'handoff): l'handoff si riscrive a ogni sessione.
  - R-832-1: test del bot per «Non: grave» e «Non, grave».
- **Merge di main (PR #392, solo documenti del funnel) nel ramo**: FATTO, commit ba074391. Conflitti solo nei report: tenuti quelli del ramo, memoria del revisore unita. Nessun file del perimetro di review toccato dal merge.
- **Non fatte**: R-836-1 COSMETICA (messaggio d'errore del test meno chiaro); verifica esterna #387/#388 V-4 (thread della prova vivo dopo il tempo massimo: innocuo, non si può fermare una chiamata di sistema bloccata) — DEFERITE.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 modules/crm/copia_cifrata.py       |  64 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           |  18 ++++++------------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  42 ++++++++++++++++++------------------------
 tests/test_unit_crm.py             |  92 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 tests/test_unit_verifica_bot.py    |   3 +++
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base: 7cf52359 (origin/main dopo il merge della PR #392, entrato nel ramo col merge ba074391); i file della #392 escono quindi dal diff.

## §3 GIT LOG --ONELINE (sessione)

```
ba074391 Merge origin/main (PR #392, funnel: solo documenti) nel ramo della PR #391 — conflitti dei report risolti
1d29e7b6 docs(fine-task): handoff — PR #391 aperta con l'etichetta verifica
ef51e72b docs(fine-task): CRM note minori chiuse (review #834–#836); PR #388 e #389 mergiate
f126fbd5 test(crm): il finto sysctl controlla anche uscita catturata, testo e tempo massimo (R-835-1) — review #836 APPROVATO CON RISERVE
3dbbf34d chore(revisore): memoria review #836 — APPROVATO CON RISERVE
cd46a249 fix(crm): note minori — resto in chiaro di prima del riavvio tolto anche col PID riusato, messaggio chiaro se il file da ripristinare non si legge, avviso senza «riuscita» doppio; test del bot per «Non: grave» — review #834 e #835 APPROVATO CON RISERVE
07c8cedf chore(revisore): memoria review #835 — APPROVATO CON RISERVE
cad98727 chore(revisore): memoria review #834 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #834 (diff poi committato in cd46a249, con le correzioni riviste in #835)

## VERDETTO: APPROVATO CON RISERVE

Review #834. Ho controllato il diff STAGED con `git diff --cached`: 3 file, +109/−7 sopra f75e09a2 (= origin/main), sha256 del diff 6f208bc1…. Prima della review ho letto CLAUDE.md §5/§8/§10, stato_progetto.md (le parti sul CRM) e la mia memoria (#824–#833). Il diff non tocca la history, `_get_window`, il tetto di 10 iterazioni né il tetto di 8k.

**Elementi del diff esaminati**
- `modules/crm/copia_cifrata.py:347` — `subprocess.run(["sysctl","-n","kern.boottime"], capture_output, text, timeout=2, check=False)`. Rischi controllati: shell, iniezione, blocco, eccezioni. Gli argomenti sono fissi e non c'è shell. L'eccezione è presa da `except Exception` e la funzione ritorna None. Ho provato con un `sysctl` finto che si blocca: None in 2,0 s. Con un sysctl finto nel formato macOS il valore torna giusto. Su Linux senza /proc, il sysctl vero scrive l'errore su stderr (catturato), stdout resta vuoto e la funzione dà None. Senza sysctl nel PATH, None. — **ok**
- `modules/crm/copia_cifrata.py:386` — regola dell'avvio, letta solo se serve e una volta sola (`avvio_letto`). Rischio controllato: togliere il temporaneo di un ripristino IN CORSO. La regola aggiunge cancellazioni solo nei primi ~59 minuti dopo l'avvio, e solo per file con mtime più vecchio di 60 s rispetto all'avvio. Un ripristino in corso può avere un mtime così solo se l'orologio salta avanti oltre (uptime al momento della scrittura + 60 s), oppure se il file sta su un disco di rete con l'orologio indietro. In più servono due ripristini contemporanei sullo stesso dest. Anche allora il danno è solo un ripristino fallito: il .gascrm resta intatto. Prova completa sul ramo macOS (sysctl finto, /proc nascosto): resto di 120 s prima dell'avvio con PID vivo → tolto; 30 s prima → resta (margine); file nuovo → resta; PID morto → tolto. Con l'avvio sconosciuto si decide come prima. — **ok**
- `modules/crm/copia_cifrata.py:439` — read_bytes in try, `ErroreCRM(...) from None`. Rischio: la premessa di V-2. Il CLI prendeva GIÀ OSError a `modules/crm/__main__.py:217`. Ho rieseguito il comando a HEAD: stampa «STOP: [Errno 2] No such file or directory…», rc=1, nessun traceback. Nell'indice: «STOP: non riesco a leggere … controlla il percorso», rc=1. La modifica è innocua e il messaggio migliora. — **riserva cosmetica** (R-834-2a)
- `modules/crm/copia_cifrata.py:292` — motivo «errore durante la copia cifrata (X)». Rischi: testi che dipendono dalla vecchia frase, dashboard. L'avviso Telegram (`modules/crm/server.py:292`) ora contiene «riuscita» una sola volta. Anche il titolo in `modules/crm/web/app.js:238` torna coerente. Nessun altro uso della vecchia frase in modules/ e tests/. — **ok**
- `tests/test_unit_crm.py:1997` — `assert avvio is None or 0 < avvio <= time.time()`. Rischio: la lettura vera dell'ora di avvio non è difesa da nessun test. Mutanti: «_avvio_sistema ritorna sempre None» → 139 passed; «senza ramo /proc» → 139 passed. — **riserva** (R-834-1)
- `tests/test_unit_crm.py:1982` — `prima` tolto e `dopo` lasciato. Mutanti sulla regola dell'avvio: «regola tolta» → failed; «None = cancella» → failed (`tests/test_unit_crm.py:1990`). Gli altri mutanti uccisi: «V-2 tolto» → failed; «V-3 rimesso com'era» → failed. Sopravvivono «margine col segno sbagliato» e «margine a 0», e anche «avvio letto sempre», che riguarda solo i tempi ed è accettabile. — **riserva cosmetica** (R-834-2b)
- `tests/test_unit_verifica_bot.py:734` — casi «Non: grave» e «Non, grave». Mutanti su `scripts/bot_esito.py:180`: `[\s:,]+` → 2 failed; `\W+` → 2 failed; `[\s:]+` → 1 failed; `[\s,]+` → 1 failed. R-832-1 è CHIUSA. — **ok**

**Esecuzioni** (su copia dell'indice, Python 3.13)
- Suite CRM + verifica_bot: 771 passed.
- Con la copia_cifrata di HEAD: 3 failed / 136 passed (test_ve386, test_r825_2, test_note_minori_388).
- mypy su modules/crm: 0 errori, come a HEAD.
- Nessuna riga aggiunta supera i 100 caratteri.

**Riserve** (da tracciare in stato_progetto.md)
- **R-834-1 BASSA**: nessun test controlla la lettura vera dell'ora di avvio. Se `_avvio_sistema` si rompe e dà sempre None, la suite resta verde e sul Mac la correzione R-830-1 sparisce senza segnali. Rimedio:
  - su Linux con /proc/stat leggibile, pretendere `avvio is not None`;
  - provare il ramo macOS con un `sysctl` finto in un PATH di tmp_path e `open("/proc/stat")` che solleva (l'ho provato: funziona).
- **R-834-2 COSMETICA**:
  - (a) il commento a `modules/crm/copia_cifrata.py:440` e la docstring del test dicono «niente traceback», ma il traceback non c'era. Nei report scrivere «messaggio più chiaro», NON «il CLI prendeva solo ErroreCRM». La premessa del brief e di V-2 è falsa: la verifica esterna citava la riga 419 del `main()` di modules/crm/__main__.py, non `cmd_ripristina`.
  - (b) il margine di 60 s non è difeso da un test: basterebbe un caso con mtime = avvio − 30 che deve restare.
  - (c) ci sono 3 righe vuote prima di `test_note_minori_388` (`tests/test_unit_crm.py:1963`) e 1 sola dopo (PEP8 E303/E302).

**Nota, non riserva**: manca un controllo «0 < avvio ≤ adesso». Un sysctl finto che dà un'ora nel futuro toglie anche il temporaneo di un ripristino in corso (provato), ma serve il controllo del PATH, che equivale già a poter eseguire codice. Con `/usr/sbin/sysctl` scritto per intero sparirebbe anche la dipendenza dal PATH.

**Rischio escluso**: non ho verificato l'output vero di `sysctl -n kern.boottime` su un Mac, né se kern.boottime resta stabile dopo sospensione o cambio d'ora: qui è un container Linux, senza macOS. Ho provato il parser e il ramo con un binario finto nel formato documentato. Non ho rieseguito su 3.11/3.12, che qui non hanno pytest. Il test del bot tocca la macchina del bot, quindi verifica-bot sarà neutral e il merge lo decide l'operatore.

**Esito**: commit consentito con riserve R-834-1 (BASSA) e R-834-2 (COSMETICA). Come richiesto, non ho creato `.claude/.review_ok` e non ho committato il diff.

Memoria: riga #834 e 2 lezioni aggiunte a /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola con `scripts/commit_memoria_revisore.sh` (cad98727). L'indice staged non è cambiato: lo sha256 è ancora 6f208bc1….

### Review #835 (commit cd46a249)

## VERDETTO: APPROVATO CON RISERVE

Review #835. Ho esaminato il diff staged: 3 file, +150/−7, sopra cad98727, sha256 del diff 1cdf136b. È il secondo giro della #834. Letti CLAUDE.md (sez. 1, 4, 5, 8, 9), reports/stato_progetto.md (in parte) e la mia memoria fino alla #834.

**Elementi del diff esaminati**
1. `modules/crm/copia_cifrata.py:357` — un'ora di avvio fuori da (0, adesso] diventa None. Rischio esaminato: un'ora di avvio nel futuro, che toglierebbe anche un ripristino ancora in corso. Il mutante senza «≤ adesso» fa fallire 1 test. Il mutante senza «0 <» è equivalente: con avvio = 0 il resto non si toglie mai. **ok**
2. `modules/crm/copia_cifrata.py:352` — sysctl chiamato col percorso completo `/usr/sbin/sysctl`, senza shell e con timeout di 2 s. Rischio esaminato: dipendenza dal PATH. Il mutante con «sysctl» senza percorso fa fallire 1 test. Però gli argomenti con nome non sono controllati (vedi R-835-1). **riserva**
3. `modules/crm/copia_cifrata.py:397` — un resto con PID vivo e recente si toglie solo se mtime < avvio − 60 s. Rischio esaminato: margine nullo o col segno sbagliato. Margine a 0, segno invertito e regola dell'avvio tolta fanno fallire 1 test ciascuno. L'ora di avvio si legge una volta per chiamata e solo se serve (`modules/crm/copia_cifrata.py:395`). **ok**
4. `tests/test_unit_crm.py:2004` — su Linux con /proc/stat il test pretende `0 < avvio ≤ adesso`. Rischio esaminato: R-834-1, cioè una correzione che sparisce in silenzio. I mutanti «sempre None» e «senza /proc» fanno fallire 1 test ciascuno. **ok, R-834-1 chiusa**
5. `tests/test_unit_crm.py:1980` — un resto con mtime = avvio − 30 s resta. Chiude R-834-2b. **ok**
6. `tests/test_unit_crm.py:2012` — il ramo macOS usa un `subprocess.run` finto. Controlla la lista degli argomenti (`tests/test_unit_crm.py:2021`) ma non i `**kw`. **riserva**
7. `modules/crm/copia_cifrata.py:449` — sorgente che non si legge: ErroreCRM con un messaggio che dice cosa controllare. Il testo non dice più «niente traceback» (R-834-2a chiusa). Il chiamante `modules/crm/__main__.py:217` prende già ErroreCRM e OSError. Il mutante «solo FileNotFoundError» sopravvive, ma l'effetto è solo sul testo del messaggio. **ok**
8. `modules/crm/copia_cifrata.py:292` — motivo «errore durante la copia cifrata (…)». Con l'avviso di `modules/crm/server.py:292`, «riuscita» compare una volta sola (`tests/test_unit_crm.py:2045`). Il mutante col messaggio vecchio fa fallire 3 test. **ok**
9. `tests/test_unit_verifica_bot.py:734` — aggiunti «Non: grave» e «Non, grave». Mutanti su `scripts/bot_esito.py:180`: `[\s:]+` e `[\s,]+` fanno fallire 1 test, `[\s:,]+` ne fa fallire 2. **ok, R-832-1 chiusa**
10. `tests/test_unit_crm.py:1814` (contesto) — il test #830 usa l'ora di avvio vera. Rischio esaminato: un runner CI appena avviato rende il test instabile. Escluso: il file `vivo` è scritto durante il test, quindi mtime ≥ avvio. **ok**

**Prove rieseguite da me** su una copia dell'indice (albero di lavoro uguale all'indice):
- test CRM e bot: 771 passed;
- tutti i mutanti dichiarati dal chiamante falliscono (rieseguiti uno per uno);
- mypy: 0 errori in modules/crm (i 78 errori segnalati sono in altri file importati);
- `git diff --cached --check` pulito;
- nessuno slicing della history; il kernel non è toccato (`_get_window`, tetto delle 10 iterazioni e test di round-trip non si applicano);
- il sysctl finto è un sostituto di un binario di sistema in un test, non una simulazione dei tool del modello;
- le righe vuote attorno a `test_note_minori_388` sono corrette.

**Riserve**
- **R-835-1 COSMETICA**: gli argomenti con nome di `subprocess.run` (`capture_output`, `text`, `timeout`) non sono controllati dal test. I tre mutanti che li tolgono restano a 139 passed. Conseguenze sul Mac: senza `capture_output` o `text` l'ora di avvio torna None in silenzio (si ritorna alla vecchia regola); senza `timeout` un sysctl bloccato blocca il ripristino. Rimedio: in `sysctl_finto` aggiungere `assert kw.get("capture_output") and kw.get("text") and kw.get("timeout") == 2`.

**Rischi esplicitamente esclusi**
- Comportamento reale su macOS non verificato, perché qui non c'è un Mac: presenza di `/usr/sbin/sysctl`, formato di `kern.boottime` e il suo aggiornamento quando l'orologio cambia.
- Resti su cartelle di rete con l'orologio del server sfasato di oltre 60 s: non provato, è un caso limite.

**Memoria**: riga #835-CRM e una lezione (con un `subprocess.run` finto si controllano anche gli argomenti con nome) committate solo in `/home/user/Gas/.claude/agents/memoria_revisore.md`, commit 07c8cedf. Non ho creato `.claude/.review_ok`; il diff resta in staging e non è committato.

### Review #836 (commit f126fbd5)

## VERDETTO: APPROVATO CON RISERVE

Review #836 del diff in staging (`git diff --cached`, 1 file: tests/test_unit_crm.py, +2/−0, sha256 del diff 98312c7f, sopra cd46a249). Ho letto prima CLAUDE.md (sez. 5), reports/stato_progetto.md (solo le parti che servono) e .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**

- `tests/test_unit_crm.py:2014` — dentro `sysctl_finto` controlla che `subprocess.run` riceva `capture_output`, `text` e `timeout == 2`.
  - Rischio esaminato: che i mutanti di R-835-1 sopravvivano ancora.
  - Esito: ok. Ho rieseguito tutto su una copia dell'indice. Con i quattro mutanti (senza `capture_output`, senza `text`, senza `timeout`, `timeout=5`) fallisce 1 test ciascuno. Il mutante `check=True` sopravvive, ma è equivalente: se sysctl fallisce, `_avvio_sistema` restituisce None in entrambi i casi.
- `tests/test_unit_crm.py:2022` — è la riga che fallisce davvero quando il controllo dei parametri non passa.
  - Rischio esaminato: un messaggio di errore che porta fuori strada.
  - Esito: riserva R-836-1 COSMETICA (sotto).
- `tests/test_unit_crm.py:2013` — commento «R-835-1: …».
  - Esito: ok. La riga è lunga 92 caratteri. Nel repo non c'è configurazione di lint e il file ha già 56 righe oltre i 100 caratteri.
- Contesto, file non toccato: `modules/crm/copia_cifrata.py:352` — la chiamata vera, `subprocess.run(["/usr/sbin/sysctl", ...], capture_output=True, text=True, timeout=2, check=False)`. Ora è bloccata nei tre parametri con nome che contano.
- Contesto, file non toccato: `modules/crm/copia_cifrata.py:354` — `except Exception: valore = None` (regola §9). È il blocco che inghiotte l'`AssertionError` del finto.

**Suite:** tests/test_unit_crm.py 139 passed su una copia dell'indice nello scratchpad (rieseguito da me).

**Riserva R-836-1 COSMETICA**
- L'assert sta dentro il finto, che il codice di produzione chiama dentro il `try/except Exception` di `_avvio_sistema`. Quando il controllo fallisce, l'`AssertionError` viene inghiottito e il test fallisce solo dopo, con `assert None == 1732000000.0` alla riga `tests/test_unit_crm.py:2022`. Il messaggio non dice quale parametro manca: chi lo legge può pensare che si sia rotta la lettura dell'ora di avvio.
- Il blocco dei parametri funziona comunque: i mutanti muoiono.
- Rimedio: nel finto salvare `kw` in una lista e asserire su `capture_output`, `text` e `timeout` dopo la chiamata a `_avvio_sistema()`.
- È la stessa lezione già in memoria dal 2026-11-05 («usare k.get e asserire dopo»).

**Wall of Shame:** niente da segnalare. Il diff tocca solo un test: nessun taglio diretto della cronologia, nessun output di tool simulato (`subprocess.run` finto in un test unitario, come già accettato in #835). Guardrail (10 iterazioni, 8k di output, `_get_window`) non toccati.

**Rischio escluso:** non ho verificato il comportamento su un Mac vero (`/usr/sbin/sysctl -n kern.boottime` e il suo formato reale). Non si può riprodurre in questo ambiente Linux. Il test prova solo che gli argomenti passati sono quelli giusti e che il formato atteso viene letto, non che macOS risponda in quel formato.

**Memoria:** riga `#836-CRM` aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e committata con `scripts/commit_memoria_revisore.sh` (commit 3dbbf34d, solo quel file). Il diff in staging è rimasto intatto (tests/test_unit_crm.py +2). Nessuna lezione nuova.

Come richiesto, non ho creato `.claude/.review_ok` e non ho committato il diff sotto review.

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_crm.py`:** 138 su main f75e09a2 → 139 passed (`test_note_minori_388`). Col `modules/crm` di main falliscono 3 test (il nuovo e 2 per il testo del motivo).
- **`tests/test_unit_verifica_bot.py`:** 630 → 632 passed (casi «Non: grave», «Non, grave»; il mutante `\b[Nn]on[\s:,]+` li fa fallire).
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato. **mypy:** 0 errori in `modules/crm`.

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST.
- Mappatura commit→run:
  - `cad98727`, `07c8cedf`, `cd46a249`, `3dbbf34d`, `f126fbd5`: nessuna run su questi SHA (pushati insieme a ef51e72b).
  - `ef51e72b`: run CI del push (superata da 1d29e7b6); verifica-bot annullato.
  - `1d29e7b6`: unit-suite success, handoff-check success, verifica-bot neutral (APPROVATO CON RISERVE).
  - `ba074391` (merge di main): run non ancora disponibile alla scrittura dell'handoff.
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-836-1 (COSMETICA):** l'assert del sysctl finto sta dentro il try di `_avvio_sistema`: se manca un parametro il test fallisce comunque, ma con un messaggio meno chiaro.
- **Rischi esclusi (revisori #834–#836):** formato vero di `sysctl -n kern.boottime` e presenza di `/usr/sbin/sysctl` su un Mac; resti su cartelle di rete con l'orologio sfasato.
- **Chiuse in questa sessione:** R-830-1, R-832-1, R-834-1, R-834-2, R-835-1; verifica esterna #388 V-1/V-2; bot #388 (71137d27) V-2/V-3.
- **Ancora aperte da prima:** R-810-2, R-810-3, R-808-5, R-808-6, R-803-9, R-803-10, R-804-2, R-804-4 (vedi `reports/stato_progetto.md`).
