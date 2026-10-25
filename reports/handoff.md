# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-25 — Mani fetta 16: riserve di #261 (R-ve261-3, R-ve261-4, R-ve261-5, R-ve261-6) e secondo giro sulle riserve di bot e verifica esterna #268, chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #268 (https://github.com/Gasss23/Gas/pull/268). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5008938487","url":"https://github.com/Gasss23/Gas/pull/268"}`); `gh` nel cloud non è autenticato (GH_TOKEN rifiutato). Merge da solo solo con APPROVATO pulito del bot sull'head.
2. R-ve261-4 (frameset): accettarla o chiuderla, con la descrizione corretta di §1.
3. Decisioni ancora aperte, da portare una alla volta: R-ve261-2 MEDIA, R-ve246-5 MEDIA, R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

Primo giro (fd5184b):
- **R-ve261-3 — test `<NOSCRIPT>`/`<NoScript>`**: `FATTA`.
- **R-ve261-6 — `con_noscript` in `_componi`, docstring, test a pila vuota**: `FATTA` — default sicuro (R-511-1) fissato da un test (R-512-1). Riga di test doppia: `SALTATA — non esiste su main` (falso positivo di V-4(b) ve #261, confermato dal revisore #511).
- **R-ve261-4 — sonda frameset**: `FATTA` (sonda), decisione all'operatore — `<p>W0</p><frameset><template><svg></template>W1` dà W0 W1 in Gas e in lexbor: non è una fuga.
- **R-ve261-5 — frasi giuste**: `FATTA` — per #261: «0 fughe nuove fuori dalla classe R-ve246-5» e «mutazioni prese tutte tranne quella senza `re.IGNORECASE`».

Secondo giro (d6898c7 e questi report), riserve di bot #268 (APPROVATO CON RISERVE) e verifica esterna #268 (APPROVATO CON RISERVE, https://github.com/Gasss23/Gas/pull/268#issuecomment-6403781355):
- **V-1 bot #268 BASSA — default non sicuro in `_Contesto`**: `FATTA` — `_Contesto(aperti, con_noscript=True)`, flag passato al costruttore da `_Estrattore` e dal ripiego, default fissato da un test.
- **V-2 bot #268 COSMETICA — blocco vecchio di stato_progetto**: `FATTA` — annotato con le chiusure.
- **V-1 ve #268 BASSA — numeri stantii**: `FATTA` — numeri di §5 tutti rimisurati sul codice finale.
- **V-2 ve #268 BASSA — descrizione del frameset**: `FATTA` — la classe è `<frameset>` preceduto solo da spazi, commenti e tag senza testo (`<frameset>W1`, `<div></div><frameset>W1`, `<p> </p><frameset>W1`: lexbor niente, Gas W1, anche su main); con un testo non vuoto o br, img, hr, table, li prima, il browser ignora il frameset e lexbor mostra W1 come Gas.
- **V-3 ve #268 BASSA — test sul testo intero**: `FATTA` — pagine con `<noscript class=x>` e con noscript dopo 3000 caratteri.
- **V-4 ve #268 COSMETICA — §6 stantio**: `FATTA` — §6 riscritto.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 modules/web/leggi.py               |  24 ++++++++++++------------
 reports/diff_sessione.md           |  12 +++++-------
 reports/handoff.md                 | n/d (commit finale)
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  56 +++++++++++++++++++++++++++++++++++++++++++++-----------
 tests/test_unit_web_leggi.py       |  33 ++++++++++++++++++++++++++++++++-
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat` preso con i report in stage, prima del commit finale.

## §3 GIT LOG --ONELINE (sessione)

```
d6898c7 fix(web): default sicuro anche in _Contesto, test noscript con attributi e in fondo (PR #268)
fd4b00e chore(revisore): memoria review #514 — APPROVATO
56af27f docs(fine-task): Mani fetta 16 — report, handoff, stato (PR #268, review #511-#513)
fd5184b fix(web): con_noscript calcolato in _componi, test NOSCRIPT e pila vuota (fetta 16 Mani)
903be16 chore(revisore): memoria review #513 — APPROVATO
cb1040c chore(revisore): memoria review #512 — APPROVATO CON RISERVE
1009528 chore(revisore): memoria review #511 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore fd5184b (primo giro): tre review, #511 sul primo diff, #512 dopo il default `True`, #513 dopo il test del default (diff committato). Commit motore d6898c7 (secondo giro, riserve di bot e verifica esterna #268): review #514. Verdetti integrali:

### Review #511 (chat Mani) — primo diff staged

## VERDETTO: APPROVATO CON RISERVE

Review #511 (chat Mani). Ho esaminato il diff in stage di claude/peaceful-lovelace-0w2b7q rispetto alla base origin/main 0dfe330, Mani fetta 16, che chiude R-ve261-3 e R-ve261-6. Prima della review ho letto CLAUDE.md (sez. 5), il blocco «riserve rimaste dopo il merge di #261» in reports/stato_progetto.md e la memoria del revisore.

**Elementi del diff esaminati**
- `modules/web/leggi.py:1372`: `_componi` calcola `con_noscript` con `_NOSCRIPT.search(grezzo)` sul testo intero e lo passa al costruttore. Rischio esaminato: il comportamento cambia rispetto all'override di `feed` tolto? No: l'override cercava sullo stesso `grezzo` passato in un solo `feed`, quindi il risultato è identico. Il ripiego senza parser calcola il flag da sé (`modules/web/leggi.py:1124`, non toccato). Esito: ok.
- `modules/web/leggi.py:800` e `modules/web/leggi.py:812`: nuovo parametro `con_noscript: bool = False`, scritto in `_contesto.con_noscript`. Rischio esaminato: un chiamante che non passa il flag. Oggi l'unico chiamante in produzione è `_componi`. I test che costruiscono `_Estrattore()` senza flag (tests/test_unit_web_leggi.py righe 1156, 1183, 1403, 1654, 1721) usano pagine senza noscript, quindi non cambia niente. Il default però è il valore NON sicuro. Esito: riserva R-511-1.
- `modules/web/leggi.py:209`: la docstring di `_Contesto` ora descrive l'eccezione di `_chiudi_template` (R-469-1) e il caso noscript. Rischio esaminato: che contraddica il codice. È coerente con la guardia `not self.con_noscript` in `modules/web/leggi.py:417`. Esito: ok.
- `tests/test_unit_web_leggi.py:1023` e `tests/test_unit_web_leggi.py:1024`: pagine con `<NOSCRIPT>` e `<NoScript>`. Rischio esaminato: che il mutante senza `re.IGNORECASE` sopravviva ancora. Ho rifatto il mutante a mano e il test FALLISCE, quindi R-ve261-3 è chiusa. Esito: ok.
- `tests/test_unit_web_leggi.py:1027` e `tests/test_unit_web_leggi.py:1028`: `</template>` in più a pila vuota. Rischio esaminato: il mutante senza `and self._template_fuori` in `modules/web/leggi.py:414` (citazione di contesto). Ho rifatto il mutante: il contatore scende a -1, il template successivo non arriva sopra 0 e VIS si perde, quindi il test FALLISCE. Esito: ok.
- `tests/test_unit_web_leggi.py:1995`: il test casuale del ripiego passa il flag in modo esplicito. Senza, perderebbe il caso noscript che prima copriva l'override. Esito: ok.

**Prove rifatte da me**
- Web suite: 420 passed, 1 skipped su Python 3.13.16 e su 3.11.
- Mutanti, tutti presi (FAIL): senza IGNORECASE; senza guardia a pila vuota; flag ignorato nel costruttore; flag non passato da `_componi`.
- Dopo ogni prova il working tree è tornato identico all'index (`git diff --quiet`).
- V-4(b) della verifica esterna #261: confermo che su origin/main non c'è nessuna tupla di test doppia. Le uniche righe uguali sono prefissi di stringhe DOCTYPE con continuazioni diverse (righe 1238, 1244, 1261). Nessuna modifica serve.

**Antipattern (Wall of Shame)**: nessuno slicing della history, nessuna simulazione di tool. Il diff non tocca i guardrail (cap 10 iterazioni, cap 8k, `_get_window`) né il perimetro di ci.yml.

**Riserve**
- **R-511-1 (chat Mani) BASSA**: con default `con_noscript=False`, chi costruisce `_Estrattore` senza flag su una pagina con noscript riattiva la regola R-469-1, cioè la classe di fuga V-1 ve #261 bis. Prima l'override di `feed` lo calcolava da sé per qualunque chiamante. Oggi non è un difetto (l'unico chiamante in produzione passa il flag), ma va contro «verso sicuro / zero crash». Proposta: default `True` (fail-closed). L'ho provato e la suite resta 420 passed 1 skipped, e anche il mutante «flag non passato» verrebbe preso. In alternativa, parametro obbligatorio keyword-only. Va tracciata in stato_progetto.md.

**Cosa NON ho verificato**
- Non ho rifatto il fuzz di identità PR/main su 300 mila pagine né il confronto con lexbor/selectolax sui 4 casi nuovi: è costoso e già dichiarato dall'autore. Per l'equivalenza mi sono basato sull'argomento statico (stesso `grezzo`, un solo `feed`).
- Non ho rifatto la suite col parser vecchio forzato (`_PARSER_AGGIORNATO=False`): quel percorso usa `_testo_senza_parser`, che il diff non tocca.
- Non ho rifatto i mutanti «flag spento nel ripiego» e «senza con_noscript in chiudi».

**Memoria**: riga contatore #511 e una lezione nuova (il default di un parametro che sostituisce un auto-rilevamento deve essere il valore sicuro) aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole con lo script: commit 1009528. I file del diff restano in stage, non toccati.

### Review #512 (chat Mani) — dopo il default `True`

## VERDETTO: APPROVATO CON RISERVE

Review #512 (chat Mani): ri-review del diff STAGED su claude/peaceful-lovelace-0w2b7q dopo la #511. Ho fatto le letture obbligatorie: CLAUDE.md sez. 5/8/9 (era nel contesto), reports/stato_progetto.md con Grep mirato, memoria_revisore.md (coda e lezioni recenti, compresa la lezione della #511 sul default fail-closed).

**Elementi del diff esaminati**
- `modules/web/leggi.py:800`: `_Estrattore.__init__(xhtml: bool = False, con_noscript: bool = True)`. Rischio: un chiamante che dimentica il flag riapre la regola R-469-1. Esito: ok, chiude R-511-1. L'ho provato sul codice: `_Estrattore()` senza flag su `<p>A</p><template><svg></template>SEGRETO` dà la pila incerta e nasconde il resto (va nel verso sicuro).
- `modules/web/leggi.py:1373`: `_componi` passa sempre `con_noscript=_NOSCRIPT.search(grezzo) is not None`, in modo esplicito. Rischio: il nuovo default cambia l'uscita reale. Esito: ok. Su una pagina senza noscript (`<template><svg></template>VIS`) passa False e VIS resta visibile come prima. Il default non arriva mai a `_componi`.
- `modules/web/leggi.py:813`: il commento spiega il perché (R-ve261-6, R-511-1) e il flag viene assegnato al contesto. Esito: ok.
- `modules/web/leggi.py:1125`: (contesto) il ripiego calcola ancora il flag da sé sul testo intero, con la stessa regex `_NOSCRIPT` che ha IGNORECASE (`modules/web/leggi.py:789`). Esito: ok, coerente.
- Test che costruiscono `_Estrattore()` senza flag: `tests/test_unit_web_leggi.py:1156`, `tests/test_unit_web_leggi.py:1183`, `tests/test_unit_web_leggi.py:1315`, `tests/test_unit_web_leggi.py:1323`, `tests/test_unit_web_leggi.py:1403`, `tests/test_unit_web_leggi.py:1654`, `tests/test_unit_web_leggi.py:1721`. Nessuno contiene `</template>`, quindi per loro il default non fa differenza. Il test casuale a `tests/test_unit_web_leggi.py:1995` passa il flag esplicito, calcolato sulla pagina intera. Esito: ok.

**Prove rifatte**
- Web suite: 420 passed, 1 skipped su Python 3.13.16 e su 3.11.
- Mutante «default=False», applicato al diff in un worktree separato: la suite resta 420 passed, 1 skipped, quindi il mutante sopravvive. Da qui la riserva.

**Riserve**
- R-512-1 BASSA: nessun test fissa il default `con_noscript=True`. Il mutante col default opposto passa tutta la suite, quindi il default può tornare a False senza che nessuno se ne accorga. Fix: un test con `_Estrattore()` senza flag su `<p>A</p><template><svg></template>X` che controlla `_contesto.incerta` e che X non compaia nel testo. Va tracciata in stato_progetto.md.

**Rischio esplicitamente escluso**
- Non ho rifatto i mutanti dichiarati dall'autore (senza IGNORECASE, senza guardia a pila vuota, flag non passato o ignorato, flag spento nel ripiego, senza con_noscript in chiudi). Li avevo già verificati nella #511 per i casi principali, e il codice interessato non è cambiato in questa revisione.
- Non ho rifatto la suite col parser vecchio forzato (411/10 dichiarati): il cambio tocca solo il costruttore e `_componi` passa il flag prima di scegliere tra parser e ripiego.
- Comportamento su VPS non verificato: la modifica è puramente locale al parser.

**Memoria**
- Ho aggiunto la riga #512 e una lezione in /home/user/Gas/.claude/agents/memoria_revisore.md (chiudendo una riserva su un default, provare il mutante col default opposto).
- L'ho committata da sola con `scripts/commit_memoria_revisore.sh` (cb1040c). `modules/web/leggi.py` e `tests/test_unit_web_leggi.py` sono ancora in stage, non toccati.
- Il worktree temporaneo del mutante è stato rimosso. Ne resta uno nello scratchpad (`/tmp/claude-0/-home-user-Gas/43e8a462-3a0c-4db5-a7de-fcbdd42c5c23/scratchpad/base`, su 0dfe330): c'era già prima di questa review e non l'ho toccato. Si toglie con `git worktree remove`.

### Review #513 (chat Mani) — sul diff committato in fd5184b

## VERDETTO: APPROVATO

Review #513 (chat Mani). È la ri-review del diff in stage su claude/peaceful-lovelace-0w2b7q dopo la #512. Ho fatto le letture obbligatorie: CLAUDE.md, le voci di reports/stato_progetto.md e la coda di memoria_revisore.md, con le lezioni del 2026-10-25 sul default fail-closed e sul mutante «default opposto».

Elementi del diff esaminati:
- tests/test_unit_web_leggi.py:1038 — `test_estrattore_senza_flag_noscript_va_nel_verso_sicuro`: crea `_Estrattore()` senza flag e gli passa `<p>A</p><template><svg></template>SEGRETO`, poi controlla che `_contesto.incerta` sia vero e che SEGRETO manchi da `pezzi`. Rischio esaminato: un test che non fissa davvero il default (R-512-1). Ho rifatto il mutante `con_noscript: bool = False` in modules/web/leggi.py:800: 1 failed, 420 passed, quindi il mutante viene preso. Gli attributi `incerta` (modules/web/leggi.py:224) e `pezzi` (modules/web/leggi.py:805) esistono, quindi le asserzioni non passano per caso. Esito: ok, **R-512-1 chiusa**.
- tests/test_unit_web_leggi.py:1045 — seconda metà del test: con `_Estrattore(con_noscript=False)` la pila non è incerta e VIS è visibile. Rischio esaminato: che il test passi anche se il parametro viene ignorato e il flag resta sempre True. Ho rifatto il mutante che forza la riga modules/web/leggi.py:813 a `True`: 1 failed, preso. Il test quindi fissa sia il default sia il passaggio del valore esplicito. Esito: ok.
- modules/web/leggi.py:800 — default `con_noscript=True`, invariato rispetto alla #512. Conferma la direzione fail-closed. Esito: ok.

Suite web rifatta da me: 421 passed, 1 skipped su Python 3.13.16 e su 3.11. Dopo ogni mutante ho ripristinato dall'index (`git checkout`); i due file del diff restano in stage come prima. Nessun guardrail toccato: niente `_get_window`, cap del loop, slicing della history o simulazione di tool.

Rischio escluso: il resto del diff (default True, flag calcolato in `_componi`, test NOSCRIPT e pila vuota, ripiego nel test fuzz) non l'ho ri-sondato oltre la suite. È identico a quanto già verificato nella #511 e nella #512, e la sola aggiunta è il test. Comportamento su pagine reali o su VPS non verificato: fuori perimetro per un'aggiunta solo di test.

Memoria: ho aggiunto la riga #513 in /home/user/Gas/.claude/agents/memoria_revisore.md, nessuna lezione nuova. L'ho committata da sola con scripts/commit_memoria_revisore.sh (commit 903be16); modules/web/leggi.py e tests/test_unit_web_leggi.py restano in stage. Nota: il marcatore `.claude/.review_ok` va rigenerato con `bash scripts/segna_review_ok.sh`, perché il gate PreToolUse ora lo considera non corrispondente al diff in stage.

### Review #514 (chat Mani) — secondo giro, sul diff committato in d6898c7

## VERDETTO: APPROVATO

Review #514 (chat Mani). Ho letto il diff staged del branch claude/peaceful-lovelace-0w2b7q (PR #268): 2 file, +16 −6. Prima ho fatto le tre letture obbligatorie: CLAUDE.md, che era già nel contesto; reports/stato_progetto.md, la parte iniziale e la voce della fetta 16; la memoria del revisore, le lezioni e la coda dalla #504 alla #513.

**Elementi del diff esaminati**
- `modules/web/leggi.py:222` — ora si scrive `_Contesto(aperti, con_noscript: bool = True)`. Prima il default stava fisso a `False` dentro `__init__`, ed è il punto V-1 del bot #268. Rischio esaminato: un chiamante che dimentica il flag riapre la regola della chiusura del template (quella introdotta con R-469-1). Esito: ok, il default è il valore sicuro e uguale a quello di `_Estrattore` (`modules/web/leggi.py:801`).
- `modules/web/leggi.py:813` — `_Estrattore` passa il flag al costruttore invece di assegnarlo dopo. Rischio esaminato: un ordine diverso di inizializzazione, o il flag perso per strada. Esito: ok. Il mutante «`_Estrattore` non passa il flag» e il mutante «flag forzato a True in `_Contesto`» fanno fallire entrambi tests/test_unit_web_leggi.py::test_estrattore_senza_flag_noscript_va_nel_verso_sicuro.
- `modules/web/leggi.py:1124` — il ripiego `_togli_blocchi_nascosti` passa `_NOSCRIPT.search(testo) is not None`. Rischio esaminato: il ripiego che finisce sul default o con il flag spento. Esito: ok. Il mutante «non passa il flag» fallisce sulla pagina «</template></template><template><math>…» e il mutante «False fisso» fallisce sulla pagina lunga.
- Contesto: `modules/web/leggi.py:418` è l'unico punto in cui conta `con_noscript`, cioè «</template>» con template fuori dalla pila. Per questo i test diretti `_Contesto({})` di `tests/test_unit_web_leggi.py:1602-1627` (svg/foreignobject/span/b/div/table/annotation-xml, nessun template) non cambiano significato col nuovo default. L'ho provato: col mutante default=False test_chiusura_fermata_da_un_elemento_html_rende_incerta resta verde. Esito: ok.
- `tests/test_unit_web_leggi.py:1054` — il ciclo su `((), True), ((False,), False)` fissa il default di `_Contesto` in entrambi i versi. Ho tracciato i due casi a mano. Col default si va su `_visti` e la pila diventa incerta con `[svg]` ancora dentro. Con False si va su `_chiudi_template`, la pila si svuota e non diventa incerta. L'asserzione `(c.pila == []) is not incerta` è coerente coi due rami. Esito: ok, e il mutante default=False lo fa fallire.
- `tests/test_unit_web_leggi.py:1026` e `tests/test_unit_web_leggi.py:1027` — le due pagine nuove (V-3 della verifica esterna #268). Rischio esaminato: test che non mordono. Esito: ok. Il mutante con la regex `<noscript>` chiusa fa 1 FAIL esattamente su `<noscript class=x>`, e il mutante `_componi` su `grezzo[:1000]` fa 1 FAIL esattamente sulla pagina da 3000 caratteri.

**Prove rifatte da me**
- Suite web: 423 passed, 1 skipped sia su Python 3.13.16 sia su 3.11.
- 7 mutanti su una copia del tree staged nello scratchpad: tutti presi.
  - default False in `_Contesto`
  - `_Estrattore` senza flag
  - ripiego senza flag
  - ripiego con False fisso
  - flag forzato True
  - `_componi` su `[:1000]`
  - regex `<noscript>` chiusa

Non ho rifatto gli altri 5 mutanti dell'autore (IGNORECASE, guardia a pila vuota, ripiego su `testo[:1000]`, `chiudi` senza `con_noscript`, default False in `_Estrattore`). Sono già stati verificati nelle review #511–#513 e il diff non tocca quelle righe.

**Rischi esclusi esplicitamente**
- Non ho rifatto la corsa col parser vecchio forzato (414 passed, 10 skipped secondo l'autore): il diff non tocca il percorso che sceglie il parser, solo il costruttore di `_Contesto`.
- Non ho verificato il comportamento su pagine reali del web: in dev si usano solo pagine sintetiche.
- V-1, V-2 e V-4 della verifica esterna e V-2 del bot: stanno solo nei report, fuori dal diff, quindi non li ho revisionati qui.

Antipattern del Wall of Shame (sezione 5 di CLAUDE.md): nessuno slicing della history né simulazione di tool. Il diff è tutto in modules/web, e i guardrail del motore (cap di 10 iterazioni, cap di 8k, `_get_window`) non sono toccati. Nessuna riserva nuova.

**Memoria**
- Ho aggiunto la riga contatore #514 in /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho committata con lo script: commit fd4b00e «chore(revisore): memoria review #514 — APPROVATO».
- Nessuna lezione nuova.
- In stage restano modules/web/leggi.py e tests/test_unit_web_leggi.py. reports/stato_progetto.md e reports/ultimo_report.md sono modificati ma non in stage, come li ho trovati.


## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati). Tutto misurato sul codice finale (d6898c7):
- `python3 -m pytest -q tests/test_unit_web_leggi.py`: main `416 passed, 1 skipped` → ramo `423 passed, 1 skipped in 24.64s` (3.13.16) e `423 passed, 1 skipped in 24.55s` (3.11). +7 test: 6 pagine parametrizzate e 1 test dei default.
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin): `414 passed, 10 skipped in 22.94s` (main 407/10).
- Mutazioni, 12, tutte prese (uscita di pytest): senza `re.IGNORECASE` → `2 failed, 421 passed`; regex `<noscript>` chiusa → `1 failed, 422 passed`; senza guardia a pila vuota → `2 failed, 421 passed`; flag non passato da `_componi` → `8 failed, 415 passed`; `_componi` su `grezzo[:1000]` → `1 failed, 422 passed`; ripiego su `testo[:1000]` → `1 failed, 422 passed`; flag ignorato in `_Estrattore` → `9 failed, 414 passed`; flag ignorato in `_Contesto` (forzato True) → `9 failed, 414 passed`; flag spento nel ripiego → `13 failed, 410 passed`; senza `con_noscript` in `chiudi` → `14 failed, 409 passed`; default `False` in `_Estrattore` → `1 failed, 422 passed`; default `False` in `_Contesto` → `1 failed, 422 passed`.
- Oracolo contro main: testo identico a main (worktree di origin/main 0dfe330) su pagine casuali, parser e ripiego, con noscript in più grafie, template, svg/math, canvas/object, frameset e `&#0;`: seed 7-9 sul codice finale, 100 mila ciascuno, `differenze PR/main 0` (nei passaggi precedenti seed 1-6, altre 600 mila, 0). Quindi, sulle pagine provate, 0 fughe nuove e 0 perdite nuove rispetto a main.
- Lexbor (selectolax 1.0.2, noscript→noembed): i casi nuovi danno lo stesso testo in Gas, main e lexbor.

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run e job letti dall'integrazione GitHub (`actions_list`, branch claude/peaceful-lovelace-0w2b7q):

```
40238463856  CI            push                 in_progress  —        d6898c7  2026-10-25T22:04:32Z
40238465394  verifica-bot  pull_request_target  in_progress  —        d6898c7  2026-10-25T22:04:34Z
40236338226  CI            push                 completed    success  56af27f  2026-10-25T21:37:14Z
40236351265  verifica-bot  pull_request_target  completed    success  56af27f  2026-10-25T21:37:24Z
40236101471  CI            push                 completed    failure  fd5184b  2026-10-25T21:34:08Z
```

Mappatura commit→run:
- `1009528`, `cb1040c`, `903be16`: nessuna run su questo SHA (pushati insieme a `fd5184b`).
- `fd5184b` → run CI 40236101471: `unit-suite` success (web suite compresa), `handoff-check` failure allo step «Run check_handoff» (atteso: il commit motore non contiene ancora l'handoff della sessione).
- `56af27f` → run CI 40236338226 success (`unit-suite`, `handoff-check`); verifica-bot 40236351265 success (APPROVATO CON RISERVE).
- `fd4b00e`: nessuna run su questo SHA (pushato insieme a `d6898c7`).
- `d6898c7` → run CI 40238463856 e verifica-bot 40238465394, in corso alla scrittura dell'handoff.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Dalle review di questa sessione: R-511-1 e R-512-1 CHIUSE in fd5184b; #513 e #514 senza riserve. Nessuna aperta.
- Bot #268 V-1/V-2 e verifica esterna #268 V-1..V-4: CHIUSE in questo giro (§1).
- R-ve261-4 BASSA preesistente (classe frameset descritta in §1): decisione all'operatore.
- Restano decisioni dell'operatore: R-ve261-2 MEDIA, R-ve246-5 MEDIA, R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s.
