# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-25 — Mani fetta 16: riserve di #261 (R-ve261-3, R-ve261-4, R-ve261-5, R-ve261-6), chat Mani

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #268 (https://github.com/Gasss23/Gas/pull/268). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5008938487","url":"https://github.com/Gasss23/Gas/pull/268"}`); `gh` nel cloud non è autenticato (GH_TOKEN rifiutato). Merge da solo solo con APPROVATO pulito del bot.
2. R-ve261-4 (frameset): proposta di accettarla (§1).
3. Decisioni ancora aperte, da portare una alla volta: R-ve261-2 MEDIA, R-ve246-5 MEDIA, R-ve252-2 e R-ve255-1, tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **R-ve261-3 — test `<NOSCRIPT>`/`<NoScript>`**: `FATTA` — due pagine in `test_chiusura_del_template_sopra_svg_math`; mutante senza `re.IGNORECASE` 2 FAIL.
- **R-ve261-6 — `con_noscript` in `_componi`, docstring, test a pila vuota**: `FATTA` — flag calcolato in `_componi` e passato al costruttore (default `True`, R-511-1), override di `feed` tolto, docstring di `_Contesto` aggiornata, due pagine con `</template>` in più a pila vuota (mutante senza guardia 2 FAIL), test del default (R-512-1). Riga di test doppia: `SALTATA — non esiste su main` (falso positivo di V-4(b) ve #261, confermato dal revisore #511).
- **R-ve261-4 — sonda frameset**: `FATTA` (sonda), decisione all'operatore — `<p>W0</p><frameset><template><svg></template>W1` dà W0 W1 in Gas e in lexbor (dopo il testo W0 il browser ignora `<frameset>`): non è una fuga. La classe resta solo con `<frameset>` prima di ogni testo (`<frameset>W1`: lexbor niente, Gas W1, anche su main). Proposta: accettarla.
- **R-ve261-5 — frasi giuste**: `FATTA` — per #261: «0 fughe nuove fuori dalla classe R-ve246-5» e «mutazioni prese tutte tranne quella senza `re.IGNORECASE`»; per questa fetta l'elenco reale in §5.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 modules/web/leggi.py               |  15 ++++++++-------
 reports/diff_sessione.md           |  12 +++++-------
 reports/handoff.md                 | n/d (commit finale)
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  44 +++++++++++++++++++++++++++++++++-----------
 tests/test_unit_web_leggi.py       |  22 +++++++++++++++++++++-
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file cambia anche nel commit finale), quindi «n/d», e la riga di totale è tolta. Gli altri conteggi vengono da `git diff --cached --stat` preso con i report in stage, prima del commit finale.

## §3 GIT LOG --ONELINE (sessione)

```
fd5184b fix(web): con_noscript calcolato in _componi, test NOSCRIPT e pila vuota (fetta 16 Mani)
903be16 chore(revisore): memoria review #513 — APPROVATO
cb1040c chore(revisore): memoria review #512 — APPROVATO CON RISERVE
1009528 chore(revisore): memoria review #511 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit motore fd5184b è passato da tre review: #511 sul primo diff, #512 dopo il default `True`, #513 dopo il test del default (diff committato). Verdetti integrali:

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

## §5 DELTA TEST DEL MOTORE

Solo la web suite (gas.py e gli altri test non toccati):
- `python3 -m pytest -q tests/test_unit_web_leggi.py`: main `416 passed, 1 skipped` → ramo `421 passed, 1 skipped in 24.53s` (3.13.16) e `421 passed, 1 skipped in 24.00s` (3.11). +5 test: 4 pagine parametrizzate e 1 test del default.
- Parser vecchio forzato (`_PARSER_AGGIORNATO=False` via plugin): `411 passed, 10 skipped in 23.33s` (era 407/10 su main).
- Mutazioni, tutte prese (elenco reale, uscita di pytest): senza `re.IGNORECASE` → `2 failed, 418 passed`; senza guardia a pila vuota → `2 failed, 418 passed`; flag non passato da `_componi` → `8 failed, 412 passed`; flag ignorato nel costruttore → `11 failed, 409 passed`; flag spento nel ripiego → `11 failed, 409 passed`; senza `con_noscript` in `chiudi` → `11 failed, 409 passed`; default `False` → `1 failed, 420 passed`.
- Oracolo contro main: testo identico a main (worktree di origin/main 0dfe330) su 600 mila pagine casuali, parser e ripiego, con noscript in più grafie, template, svg/math, canvas/object, frameset e `&#0;`. Seed 1-3 (sul primo diff) e 4-6 (sul codice finale), 100 mila ciascuno: `differenze PR/main 0`. Quindi, sulle pagine provate, 0 fughe nuove e 0 perdite nuove rispetto a main, senza eccezioni di classe.
- Lexbor (selectolax 1.0.2, noscript→noembed): i 4 casi nuovi danno lo stesso testo in Gas, main e lexbor.

## §6 STATO CI

`gh run list` non disponibile (gh non autenticato nel cloud); run lette dall'integrazione GitHub (`actions_list`, branch claude/peaceful-lovelace-0w2b7q):

```
40236149815  verifica-bot  pull_request_target  completed  skipped      fd5184b  2026-10-25T21:34:47Z
40236101471  CI            push                 in_progress  —          fd5184b  2026-10-25T21:34:08Z
```

Mappatura commit→run:
- `1009528`, `cb1040c`, `903be16`: nessuna run su questo SHA (pushati insieme a `fd5184b`).
- `fd5184b` → run CI 40236101471 (push), in corso alla scrittura dell'handoff; verifica-bot 40236149815 skipped (etichetta `verifica` non ancora messa).
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Dalle review di questa sessione: R-511-1 e R-512-1 CHIUSE in fd5184b. Nessuna aperta.
- R-ve261-4 BASSA preesistente (ristretta a `<frameset>` prima di ogni testo): proposta di accettarla, decisione all'operatore.
- Restano decisioni dell'operatore: R-ve261-2 MEDIA, R-ve246-5 MEDIA, R-ve252-2, R-ve255-1, R-ve235-7, tempo di rete 12 s.
