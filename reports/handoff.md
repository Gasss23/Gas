# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-27 — Mani fetta 20: lettura con lexbor pronta per l'accensione, ancora spenta, chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #277 (https://github.com/Gasss23/Gas/pull/277). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5034496930","url":"https://github.com/Gasss23/Gas/pull/277"}`); `gh` nel cloud non è autenticato. Merge da solo solo con APPROVATO pulito del bot sull'head. Il merge non accende niente.
2. Accensione: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt`; poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Poi, una alla volta: R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **Preparazione dell'accensione della lettura con lexbor (richiesta dell'operatore «prepara l'accensione»)**: `FATTA` — lettura ancora spenta per default.
  - R-521-1 (lock della sonda), R-521-2 (riprova dopo timeout): `FATTA`.
  - V-1 bot #275 (solo Linux), V-2 bot #275 (stderr nel warning), stima con la sonda: `FATTA`.
  - R-521-3, R-524-1 (cosmetiche): `FATTA`.
  - Casi con `<select>` → nascosti select, datalist, rp, attributo `hidden`, dialog chiusi: `FATTA`.
  - R-525-1/2/3 (review #525): `FATTA`.
  - R-526-1 COSMETICA (doppio controllo sotto lock senza test), R-520-4 COSMETICA: `DEFERITA — cosmetiche, verso sicuro`.
- **Accensione vera**: `DEFERITA — serve la chat Motore (requirements, CI, ambiente del VPS)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/web/leggi.py               |   7 ++++---
 modules/web/lexbor.py              |  83 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------
 reports/diff_sessione.md           |  12 ++++++------
 reports/handoff.md                 | n/d (commit finale)
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  84 ++++++++++++++++++++++++++++++++++++++----------------------------------------------
 tests/test_unit_web_lexbor.py      |  75 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat` preso con i report in stage, prima del commit finale.

## §3 GIT LOG --ONELINE (sessione)

```
ab5eb1d feat(web): lettura con lexbor pronta per l'accensione, ancora spenta (fetta 20 Mani)
ffe99a8 chore(revisore): memoria review #526 — APPROVATO CON RISERVE
88dd43a chore(revisore): memoria review #526 — APPROVATO CON RISERVE
7290177 chore(revisore): memoria review #525 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore ab5eb1d: review #525 sul primo diff e #526 dopo la chiusura di R-525-1/2/3. Verdetti integrali:

### Review #525 (chat Mani) — primo diff staged

## VERDETTO: APPROVATO CON RISERVE

Review #525 (chat Mani). Ho esaminato il diff staged, che tocca 3 file: `modules/web/leggi.py`, `modules/web/lexbor.py` e `tests/test_unit_web_lexbor.py`. Prima ho letto CLAUDE.md (sez. 5), lo stato del progetto (voci delle fette 19 e 20) e le lezioni della mia memoria (lock, sonda «una volta sola», tetti di risorsa).

**Elementi del diff esaminati**
- `modules/web/lexbor.py:103` — lock non bloccante: prima si guarda il tempo di riprova, poi si tenta il lock. Rischi esaminati: deadlock, mancato rilascio, attesa per chi chiama — **ok**. Se il controllo sul tempo è vero, il lock non viene nemmeno preso. Se il lock è occupato, la funzione esce subito senza rilasciare. Il rilascio è in `finally` (`modules/web/lexbor.py:119`), quindi avviene in ogni ramo. `_esegui` intercetta già ogni Exception. Chi arriva mentre gira la sonda non aspetta. Mutante «senza release»: 1 failed.
- `modules/web/lexbor.py:111` — riprova della sonda su `time.monotonic()`. Rischio esaminato: orologio che salta — **ok**. Il tempo monotono non torna mai indietro. Su Linux non avanza durante la sospensione, quindi al massimo la riprova arriva più tardi, mai prima: è il verso sicuro. Il valore di partenza 0.0 è corretto. Ho ripetuto 5 volte i test delle sonde: tutti verdi.
- `modules/web/lexbor.py:82` — controllo dell'attributo `hidden` e dei dialog senza `open` tramite `nodo.attributes`. Rischi esaminati: costo e nodi senza attributi — **riserva**. Il risultato è corretto: un nodo senza attributi dà un dict vuoto; `HIDDEN` maiuscolo viene preso; `hidden=x` dentro svg viene nascosto (verso sicuro); `dialog open=false` resta visibile come nel browser. Ma `attributes` costruisce un dict di tutti gli attributi a ogni elemento. Misure: 20k div con 100 attributi ciascuno 3,31 s, contro 0,99 s con `nodo.attrs` (stessi esiti verificati); 200k p con 3 attributi 1,19 s contro 0,70 s. Con il tempo massimo di 4 s, più pagine finiscono sul ripiego: niente crash, ma +4 s e niente lexbor su quelle pagine.
- `modules/web/lexbor.py:57` — select, datalist e rp nascosti. Rischio esaminato: perdite gravi di testo — **ok**. Un `<select>` non chiuso inghiotte il resto della pagina, perché lexbor segue il select nuovo. Ma anche il browser, nell'aspetto normale, mostra solo l'opzione scelta e non il resto. È comunque il verso sicuro (meno testo, mai testo nascosto). `rp` fuori da ruby è nascosto, come nel foglio di stile standard del browser.
- `modules/web/lexbor.py:132` — `_ultima_riga` porta l'ultima riga dello stderr del figlio nel log. Rischio esaminato: testo della pagina o caratteri pericolosi nel log — **ok**. `splitlines` separa anche su `\r` e U+2028; i caratteri di controllo bidi e quelli a larghezza zero diventano `?`; il taglio è a 200 caratteri e il log usa `%r`. L'ultima riga è il messaggio di un'eccezione, non testo della pagina; anche nel caso peggiore il testo della pagina arriva già al modello come risultato del tool.
- `modules/web/lexbor.py:52` — uscita 3 fuori da Linux. La sonda la tratta come «errore» e spegne la lettura per sempre, con un solo warning — **ok**. Il test sostituisce la stringa e non è vuoto: se la sostituzione non avvenisse, `attivo()` sarebbe True e il test fallirebbe.
- `tests/test_unit_web_lexbor.py:118` — test «una sonda alla volta» — **riserva**. Il mutante `_SONDA.acquire()` bloccante sopravvive (27 passed), perché il test conta solo i lanci e almeno un True; la proprietà «niente attesa per chi chiama» non è fissata.
- `modules/web/leggi.py:33` — stima nella docstring: 12+4+3+4 = circa 23 s — **ok**.

**Mutanti miei** (`modules/web/lexbor.py` ripristinato, il diff staged è intatto):
- Presi: senza release (1 failed), rp visibile (1 failed).
- Sopravvissuti: lock bloccante, senza doppio controllo sotto lock, senza `isprintable`, senza taglio a 200.

**Test**
- lexbor: 27 passed (3.13.16 con selectolax 1.0.2), 2 passed e 25 skipped (3.11 senza selectolax).
- Test web su 3.13: 469 passed, 1 skipped.

**Riserve**
- **R-525-1 (chat Mani) BASSA**: a `modules/web/lexbor.py:82` usare `attributi = nodo.attrs`. È l'oggetto `LexborAttributes`: `in` funziona senza costruire il dict, con gli stessi esiti verificati su HIDDEN, svg e dialog, ed è circa 3 volte più veloce sulle pagine ricche di attributi.
- **R-525-2 (chat Mani) BASSA**: a `tests/test_unit_web_lexbor.py:118` aggiungere `esiti.count(False) >= 1`, così il mutante con lock bloccante viene preso. Con la pausa di 0,3 s nella sonda, gli altri 7 thread arrivano mentre gira.
- **R-525-3 (chat Mani) COSMETICA**: senza test restano la pulizia di `_ultima_riga` (caratteri non stampabili, taglio a 200) e il doppio controllo sotto lock. Il codice è corretto, verificato a mano; il doppio controllo mancante costerebbe al massimo una sonda in più in una finestra stretta.

**Rischi esplicitamente esclusi**
- Comportamento su VPS e sul Mac reale, e il primo avvio a freddo del figlio fuori dall'ambiente di sviluppo: non riproducibili qui.
- `os.fork` con il lock preso: non verificato. Gas non usa fork senza exec; nel caso peggiore il processo figlio non accenderebbe mai lexbor, che è il verso sicuro.
- Oracolo html5lib su 60 mila pagine e le 131 pagine locali: non rifatti, cifre dichiarate dall'autore.

**Memoria**
- Riga contatore #525 e 2 lezioni (lock non bloccante da provare col mutante bloccante; costo di `nodo.attributes` contro `nodo.attrs`) aggiunte a `/home/user/Gas/.claude/agents/memoria_revisore.md`.
- Committate da sole: 7290177. I 3 file del diff restano in stage.
- `reports/stato_progetto.md` era già modificato prima della review, non in stage: non l'ho toccato.

### Review #526 (chat Mani) — sul diff committato in ab5eb1d

## VERDETTO: APPROVATO CON RISERVE

Review #526 (chat Mani): ri-review del diff staged su claude/peaceful-lovelace-0w2b7q dopo la #525. Prima della review ho letto CLAUDE.md (sez. 5), la parte di reports/stato_progetto.md sulla fetta 20 (§ riga 632) e la coda di memoria_revisore.md.

**Cosa ho controllato nel diff**
- `modules/web/lexbor.py:82`: il figlio ora usa `attributi = nodo.attrs` al posto di `nodo.attributes` (chiude R-525-1). Rischio: che cambi l'esito sui casi limite. L'ho confrontato su 14 casi con selectolax 1.0.2, lanciato con `-I`: HIDDEN maiuscolo, hidden="", hidden=false, `<g hidden>` dentro svg, svg HIDDEN, math hidden, dialog senza attributi, dialog open=false, OPEN e open="", data-hidden, xlink:hidden, dialog dentro svg, body e p senza attributi (`len(attrs)==0`, nessuna eccezione). Le due forme danno esiti identici in tutti i casi. Il mutante che rimette `nodo.attributes` passa 28 su 28, come atteso: è equivalente. Esito: ok.
- `tests/test_unit_web_lexbor.py:126`: la nuova asserzione `esiti.count(False) >= 1` (chiude R-525-2). Rischio: test instabile, oppure che non prenda il lock bloccante. Il mutante `_SONDA.acquire()` bloccante dà 1 failed. Il test non dovrebbe essere instabile: il primo thread tiene il lock per 0,3 s mentre gli altri 7 partono subito. 8 ripetizioni tutte verdi. Esito: ok.
- `tests/test_unit_web_lexbor.py:99`: nuovo test di `_ultima_riga` in `modules/web/lexbor.py:132` (chiude in parte R-525-3). Mutanti: senza isprintable 1 failed, senza taglio a 200 1 failed, prima riga invece dell'ultima 2 failed. Il test non porta `@con_lexbor`, quindi gira anche in CI con 3.11 senza selectolax. Esito: ok.
- `modules/web/lexbor.py:106`: il doppio controllo sotto lock non ha ancora un test. L'autore lo dichiara: nel caso peggiore parte una sonda in più in una finestra stretta, verso sicuro. Esito: riserva cosmetica (R-526-1).
- Altri mutanti rifatti: «hidden» ignorato 1 failed, dialog chiuso ignorato 1 failed.
- Dopo ogni mutante ho ripristinato il file con `git checkout --` dall'indice. Lo stage è intatto: M sui 3 file del diff, stato_progetto non in stage.
- Suite: lexbor 28 passed con Python 3.13.16; con 3.11 3 passed e 25 skipped; web (`-k web`) 470 passed e 1 skipped con 3.13. Il 470 al posto del 469 dichiarato dall'autore dipende dalla selezione dei file. Nessuna regressione.

**Wall of Shame e guardrail**: il diff non tocca la history, `_get_window`, il cap delle 10 iterazioni né i provider. Non c'è simulazione dei tool. Gli errori del figlio restano tutti intercettati e finiscono come warning in gas_debug.log, con il ripiego sulla lettura di sempre (§9 ok).

**Riserva**
- R-526-1 COSMETICA: il doppio controllo sotto lock (`modules/web/lexbor.py:106`) resta senza test. È il residuo dichiarato di R-525-3 e va tracciato in reports/stato_progetto.md. In questo momento stato_progetto non contiene ancora le voci R-525-x/R-526-x: vanno aggiunte prima del commit.

**Cosa non ho verificato**: non ho provato il comportamento del ramo acceso fuori da Linux su macOS reale, né la soglia di memoria del figlio su altre build di selectolax. Qui non sono riproducibili (sandbox Linux, una sola build 1.0.2). La sonda dell'uscita 3 è coperta solo dal test che sostituisce il nome della piattaforma.

**Memoria**: ho aggiunto la riga #526 a `/home/user/Gas/.claude/agents/memoria_revisore.md`, nessuna lezione nuova. È committata con `scripts/commit_memoria_revisore.sh` (88dd43a). Un secondo commit, ffe99a8, corregge la riga citata da :105 a :106. I file del diff sotto review sono rimasti in stage.

## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati), codice finale ab5eb1d:
- `python3 -m pytest -q tests/test_unit_web_*.py`: main a0bf5c9 `463 passed, 1 skipped` → ramo `469 passed, 1 skipped in 28.81s` (3.13.16, con selectolax); `444 passed, 26 skipped in 26.00s` (3.11 locale, senza selectolax). `tests/test_unit_web_lexbor.py` da 22 a 28 test.
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin): `459 passed, 11 skipped in 28.20s`.
- Suite vecchia con `GAS_WEB_LEXBOR=1`: `11 failed, 430 passed, 1 skipped` (gli stessi della fetta 19).
- Mutazioni (uscita di pytest sui test lexbor): senza lock `1 failed, 26 passed`; timeout che spegne per sempre `1 failed, 26 passed`; risonda subito `1 failed, 26 passed`; anche fuori da Linux `1 failed, 26 passed`; hidden ignorato `1 failed, 26 passed`; dialog chiuso visibile `1 failed, 26 passed`; select visibile `1 failed, 26 passed`; rp visibile `1 failed, 26 passed`; stderr non nel log `2 failed, 25 passed`; lock bloccante `1 failed, 27 passed`; senza isprintable `1 failed, 27 passed`; senza taglio a 200 `1 failed, 27 passed`.
- Oracolo html5lib (script nello scratchpad), 60 mila pagine senza template/svg/math: seed 7 `FUGHE oggi 48, lexbor 0; PERDITE oggi 2975, lexbor 2808`, seed 8 `FUGHE oggi 40, lexbor 0; PERDITE oggi 2907, lexbor 2717`, seed 9 `FUGHE oggi 41, lexbor 0; PERDITE oggi 2831, lexbor 2700`; corpus `pagine 131, testo identico (parole) 127, diverse 4`.

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run lette dall'integrazione GitHub (`actions_list`, workflow ci.yml, branch claude/peaceful-lovelace-0w2b7q). Istantanea al momento della scrittura: lo stato aggiornato è sulla PR.

```
40510137001  CI  push  in_progress  —  ab5eb1d  2026-10-27T13:13:20Z
```

Mappatura commit→run:
- `7290177`, `88dd43a`, `ffe99a8`: nessuna run su questo SHA (pushati insieme a `ab5eb1d`).
- `ab5eb1d` → run CI 40510137001, in corso alla scrittura dell'handoff.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-526-1 COSMETICA: doppio controllo sotto lock in `attivo()` senza test.
- R-520-4 COSMETICA: un `title` HTML dentro foreignObject si scarta.
- Prima dell'accensione: selectolax in requirements e CI (chat Motore), così i 25 test lexbor oggi saltati girano.
- Restano decisioni dell'operatore: R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s.
