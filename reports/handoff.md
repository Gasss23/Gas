# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-27 — Mani fetta 19: prova della lettura con lexbor (R-ve246-5), spenta per default, chat Mani

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
- **Accensione della lettura con lexbor**: `DEFERITA — decisione dell'operatore e richiesta alla chat Motore (requirements, CI, VPS)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 modules/web/leggi.py               |  75 +++++++++++++++++++++++++++++++++++++++++++++++----------------------------
 modules/web/lexbor.py              | 119 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  19 ++++++-------------
 reports/handoff.md                 | n/d (commit finale)
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  54 +++++++++++++++++++++++++++++++++++++++++++-----------
 tests/test_unit_web_lexbor.py      | 136 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat` preso con i report in stage, prima del commit finale.

## §3 GIT LOG --ONELINE (sessione)

```
eb2df98 feat(web): prova della lettura con lexbor in un processo figlio, spenta per default (R-ve246-5, fetta 19 Mani)
14716d9 chore(revisore): memoria review #521 — APPROVATO CON RISERVE
8fe2253 chore(revisore): memoria review #520 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore eb2df98: review #520 sul primo diff e #521 dopo la chiusura di R-520-1/2/3. Verdetti integrali:

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

## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati):
- `python3 -m pytest -q tests/test_unit_web_*.py`: main c67ccec `441 passed, 1 skipped` → ramo `461 passed, 1 skipped in 26.68s` (3.13.16, con selectolax); `443 passed, 19 skipped in 23.94s` (3.11, senza selectolax, come la CI). +20 test in `tests/test_unit_web_lexbor.py`.
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin): `451 passed, 11 skipped in 24.30s`.
- Suite vecchia con `GAS_WEB_LEXBOR=1`: `11 failed, 430 passed, 1 skipped` (3 test dei log del percorso html.parser; 8 casi frameset/template dove il browser mostra il testo, lexbor e html5lib concordi).
- Mutazioni del ramo lexbor (uscita di pytest sui 20 test): corpo senza `_pulisci` → `1 failed, 19 passed`; titolo senza tetto → `1 failed, 19 passed`; senza sonda → `1 failed, 19 passed`; sonda ripetuta → `1 failed, 19 passed`; acceso sempre → `1 failed, 19 passed`; titolo non nascosto → `1 failed, 19 passed`; nascosti ignorati → `5 failed, 15 passed`; script spenti → `1 failed, 19 passed`; titolo di svg accettato → `1 failed, 19 passed`; blocchi senza a capo → `1 failed, 19 passed`; anche in XHTML → `1 failed, 19 passed`.
- Misure della prova (script nello scratchpad): oracolo html5lib su 60 mila pagine senza template/svg/math, seed 7 `FUGHE oggi 48, lexbor 0; PERDITE oggi 2975, lexbor 1860`, seed 8 `FUGHE oggi 40, lexbor 3; PERDITE oggi 2907, lexbor 1765`, seed 9 `FUGHE oggi 41, lexbor 2; PERDITE oggi 2831, lexbor 1764`; corpus `pagine 131, testo identico (parole) 127, diverse 4`, `tempo totale oggi 10.57s, lexbor 15.76s`; robustezza `seed 1: 100000 pagine senza eccezioni né crash`, `seed 2: 100000 pagine senza eccezioni né crash`; lexbor in processo `div 100k 23.00s`, `attr 100k 36.26s`, col figlio `div 100k 4.01s -> None`, `attr 100k 4.01s -> None`.

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run lette dall'integrazione GitHub (`actions_list`, branch claude/peaceful-lovelace-0w2b7q):

```
40428033003  CI  push  in_progress  —  eb2df98  2026-10-27T00:41:49Z
```

Mappatura commit→run:
- `8fe2253`, `14716d9`: nessuna run su questo SHA (pushati insieme a `eb2df98`).
- `eb2df98` → run CI 40428033003, in corso alla scrittura dell'handoff.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-520-4 COSMETICA: un `title` HTML dentro foreignObject si scarta (perdita, verso sicuro).
- R-521-1 BASSA: sonda del figlio senza lock (N thread → N sonde).
- R-521-2 BASSA: un fallimento passeggero della sonda spegne la prova per tutta la vita del processo.
- R-521-3 COSMETICA: `test_sonda_del_figlio` lascia `_FIGLIO_OK=True` fuori dal monkeypatch.
- 5 casi con `<select>` in cui lexbor e html5lib divergono (standard cambiato di recente): da guardare prima di accendere.
- Restano decisioni dell'operatore: accensione della lettura con lexbor; R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s; R-518-1 e riaccensione di R-469-1 con noscript (superate se si accende lexbor).
