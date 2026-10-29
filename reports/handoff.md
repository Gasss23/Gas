# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Mani fetta 25: XHTML malformato letto fino al primo errore XML, come il browser (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #296 (https://github.com/Gasss23/Gas/pull/296). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5059998967","url":"https://github.com/Gasss23/Gas/pull/296"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve l'OK dell'operatore.
2. Accensione della lettura con lexbor: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (R-ve280-1); poi `GAS_WEB_LEXBOR=1` sul VPS.
3. Poi, una alla volta: tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #294 (fetta 24)**: `FATTA` — richiesta dell'operatore («mergia 294»), merge 03dc898. Verifica esterna #294 arrivata dopo: APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/294#issuecomment-6484098213); V-1: `FATTA` qui; V-2: `FATTA` (§6); V-3 (commit doppio della memoria): `SALTATA — storia già pubblicata`; V-4: merge autorizzato dall'operatore.
- **Fetta 25 — XHTML malformato (decisione dell'operatore)**: `FATTA`.
  - R-ve252-2 e R-ve255-1: `FATTA` — `_taglio_xml` in leggi.py.
  - R-550-1..4: `FATTA` (review #551). R-551-1: `FATTA` (review #553). R-551-2 COSMETICA: `DEFERITA — cosmetica`.
  - Bot su e9606d8 (caratteri invisibili nei verdetti incollati): `FATTA` — verdetti #550/#551 riemessi dal revisore.
  - Bot su 9837d0d: V-1 (test dei commenti senza taglio) e V-2 (DTD letto una volta): `FATTA`, review #553 → R-553-1 `FATTA`, review #554; V-3 (numeri): `FATTA`.
  - Verifica esterna su e9606d8 (https://github.com/Gasss23/Gas/pull/296#issuecomment-6484866647): V-1 MEDIA (i BOM): `FATTA`; V-2 BASSA (lunghezza esatta del taglio): `FATTA`; V-3/V-4/V-5: `SALTATA — informative o già dichiarate`.
  - Merge di main dc43ad6 (PR #292, review #552) e 4e8eb9f (PR #295, review #555): `FATTA`.
  - Bot su 336e67c NON approvata per un BOM letterale scritto dal bot stesso citando i casi di test (merito APPROVATO CON RISERVE): `FATTA` — BOM e U+200B nei test e nel codice scritti come `chr(...)`; V-1 BASSA (entità sconosciuta con DTD esterno = errore, come Firefox; Chrome dà solo un avviso): `FATTA` — dichiarata nella docstring di `_taglio_xml`. Review #556 (riemessa senza caratteri invisibili), #557, #558.
  - Bot su 6a3ef69: `verifica-bot` success, APPROVATO CON RISERVE (V-1 BASSA: entità dichiarate nel sottoinsieme interno del DOCTYPE accettate, html.parser mostra «&foo;» letterale; preesistente): `DEFERITA — prossima fetta, con R-551-2`. Verifica esterna su 6a3ef69 APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/296#issuecomment-6485358590): V-1 BASSA (il bot può ricopiare i Cf delle righe tolte): `SALTATA — bot verde su 6a3ef69`; V-2 BASSA (libexpat ≥ 2.4 e accensione lexbor nei documenti durevoli): `FATTA` in stato_progetto; V-3 COSMETICA: `DEFERITA`; V-4: informativa.
  - «mergia 296» dell'operatore: merge rifiutato da GitHub perché main era andato avanti (PR #297) → merge di main e106883, review #559: `FATTA`; merge della PR dopo i check sul nuovo head.
  - Verifica esterna su 336e67c (https://github.com/Gasss23/Gas/pull/296#issuecomment-6485248441): V-1 MEDIA (check `verifica-bot` rosso): `FATTA` (stesso fix, nuovo SHA); V-2 BASSA (= V-1 bot): `FATTA` come scelta dichiarata, tenuta aperta in §7; V-3 COSMETICA (token singolo oltre ~2 MB): `DEFERITA — verso sicuro`; V-4/V-5: `SALTATA — informative`.
- **Accensione lexbor (punto b)**: `DEFERITA — chat Motore`.
- **Tempo di rete 12 s, R-ve235-7**: `DEFERITA — una alla volta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  14 ++++++++++++
 modules/web/leggi.py               | 102 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  18 ++++++++-------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   6 ++---
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  48 ++++++++++++++++++++++++++++-----------
 tests/test_unit_web_leggi.py       | 146 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------
 tests/test_unit_web_lexbor.py      |   8 +++++++
```

NB: base = merge-base con origin/main = e106883 (dopo il merge di main). Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
1739759 docs(fine-task): PR #296 dopo il merge di main e106883 (PR #297), review #559, verdetti su 6a3ef69
bd71498 Merge origin/main (e106883, PR #297) in claude/peaceful-lovelace-0w2b7q (PR #296)
6a3ef69 docs(fine-task): PR #296 dopo il rifiuto del bot per caratteri invisibili e la verifica esterna su 336e67c, review #556–#558
c6b73cf fix(web): niente caratteri invisibili scritti nei test e nel codice, nota su Chrome nel taglio XHTML (bot e ve #296)
54dea9d chore(revisore): memoria review #556 — APPROVATO CON RISERVE
336e67c docs(fine-task): PR #296 dopo le riserve di bot e verifica esterna e il merge di main 4e8eb9f, review #553–#555
7cf7f19 Merge origin/main (4e8eb9f, PR #295) in claude/peaceful-lovelace-0w2b7q (PR #296)
0d5c258 fix(web): DTD delle entità letto una volta per pagina, taglio al carattere giusto (V-1/V-2 bot e V-2 ve #296)
e1fa7c1 chore(revisore): memoria review #554 — APPROVATO
e5f4a62 chore(revisore): memoria review #553 — APPROVATO CON RISERVE
9837d0d docs(fine-task): handoff §3 e §6 aggiornati dopo la riemissione dei verdetti (PR #296)
54fc5da docs(fine-task): verdetti #550 e #551 riemessi senza caratteri invisibili (bot #296)
e9606d8 docs(fine-task): Mani fetta 25 — XHTML malformato, handoff e report (PR #296)
eaa0642 Merge origin/main (dc43ad6, PR #292) in claude/peaceful-lovelace-0w2b7q (fetta 25 Mani)
f7bb599 fix(web): XHTML malformato letto fino al primo errore XML, come il browser (fetta 25 Mani)
fa715d8 chore(revisore): memoria review #551 — APPROVATO CON RISERVE
78de08e chore(revisore): memoria review #550 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore f7bb599: review #550 e #551. Merge eaa0642: review #552. Commit motore 0d5c258: review #553 e #554. Merge 7cf7f19: review #555. Commit motore c6b73cf (caratteri invisibili e V-1 bot): review #556 (riemessa), #557 e #558. Merge bd71498: review #559 (riemessa per il gate B). Nota: i verdetti #550 e #551 incollati nel commit e9606d8 contenevano un BOM invisibile (U+FEFF), che fa bocciare il bot; il revisore li ha riemessi con lo stesso esito e la stessa sostanza, il BOM scritto in chiaro: fanno fede questi, gli originali restano nella storia di e9606d8. Verdetti integrali:

### Review #550 (chat Mani) — primo diff staged (verdetto riemesso)

## VERDETTO: APPROVATO CON RISERVE

Review #550 (chat Mani), riemessa senza caratteri invisibili. Diff staged su claude/peaceful-lovelace-0w2b7q, base main 03dc898, fetta 25 Mani (XHTML malformato, R-ve252-2, R-ve255-1, più V-1 ve #294). Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (in modo mirato) e la memoria. Nessun antipattern del Wall of Shame: il motore (gas.py, la history) non è toccato.

**Elementi esaminati**
- modules/web/leggi.py:1329 — insieme dei pubblici XHTML. Rischio: fedeltà allo standard. Ho scaricato la sorgente whatwg/html da raw.githubusercontent.com: le 11 voci coincidono esattamente con source:152092-152102. Esito: ok.
- modules/web/leggi.py:1372 — `esterna` carica il DTD solo per quei pubblici e risponde 1 per tutto il resto. Rischio: XXE e download. Ho provato un'entità generale `SYSTEM "file:///etc/passwd"`, un'entità di parametro SYSTEM e un'entità generale col pubblico XHTML: nessun file letto, nessuna rete. Nel terzo caso il DTD letto come contenuto dà errore e la pagina si taglia lì (verso sicuro). Questo rispetta «should not attempt to retrieve any other external entity» (source:152105). Esito: ok.
- modules/web/leggi.py:1348 — doppio escape di «<» e «&» nel DTD. Rischio: markup iniettato attraverso le entità. `&LT;b&GT;&AMP;` sotto DOCTYPE Strict dà il testo «<b>&», senza tag. Esito: ok. Il test però manca (vedi R-550-4).
- modules/web/leggi.py:1394 — seconda lettura grezza sul prefisso fino all'errore. Rischio: testo che sfugge dopo l'errore, mezzo tag rimasto. Ho fatto 13 sonde sull'intera `_componi`: script con CDATA o carattere non valido, `</script x x>`, style, template, noscript, svg title, commento, CDATA, script non chiuso. In nessuna SEGRETO esce e non resta mai mezzo tag. CRLF dentro il testo e negli attributi viene conservato dal DefaultHandler, quindi il controllo startswith regge. Esito: ok.
- modules/web/leggi.py:1383 — prima lettura con expat 2.6.1. Rischio: bomba di entità e DoS. La bomba del test si ferma. Ho provato anche `%p;` ripetuto 1000 volte col pubblico XHTML (riparserebbe ogni volta il DTD da 59 KB): expat lo ferma con «limit on input amplification factor», in 0,09 s. Esito: ok, ma la sicurezza dipende dalla versione di expat (R-550-2).
- modules/web/leggi.py:1508 — chiamata in `_componi` con `completo = not troncato`, più warning nella scatola nera. Rischio §9. Un'eccezione inattesa arriva all'`except Exception` di leggi_pagina, che restituisce «errore nella pulizia della pagina», senza crash. Il test tests/test_unit_web_leggi.py:1988 copre il caso troncato. Esito: ok.
- tests/test_unit_web_leggi.py:1518 — `_radice` avvolge i frammenti dei vecchi test. Rischio: test indeboliti. Le asserzioni non cambiano, cambia solo l'input. Esito: ok.
- tests/test_unit_web_lexbor.py:131 — tabella degli 8 punti d'integrazione più malignmark. Esito: ok, passano.

Rifatte da me: tests/test_unit_web_leggi.py più tests/test_unit_web_lexbor.py danno 595 passed e 1 skipped su 3.13, 483 passed e 113 skipped su 3.11 (expat 2.6.1 su entrambi). I numeri dell'agente (586/1 e 483/104) vengono da un insieme di 587 test, il mio ne ha 596: va solo allineato il conteggio nel report.

Mutanti miei (poi ripristinato il file, cmp uguale):
- «entità saltata senza errore»: 1 failed, preso.
- «senza startswith»: sopravvive.
- «senza doppio escape»: sopravvive.
- «senza esclusione di amp/lt/gt/quot/apos»: sopravvive, ma è equivalente (il ridichiararle col doppio escape è innocuo).

**Riserve (da tracciare in stato_progetto.md)**
- **R-550-1 BASSA** (testo in più rispetto al browser, non regressione): modules/web/leggi.py:1369 crea expat senza `namespace_separator`, quindi non vede gli errori di namespace. Per lo standard (source:152321) e per Chrome sono fatali. Esempio: `<r><p>A</p><h:script>S</h:script><p>VIS</p></r>` (prefisso h non dichiarato) viene tenuto intero, mentre Chrome si ferma prima di h:script. Con `namespace_separator=" "` expat dà «unbound prefix». Rimedio: un parametro nella prima lettura, compatibile con tests/test_unit_web_leggi.py:1902 (lì i prefissi sono dichiarati).
- **R-550-2 BASSA** (robustezza su VPS): la difesa contro la bomba e contro il DTD ripetuto si appoggia alla protezione da amplificazione di expat, che esiste da 2.4.0. Su Linux CPython usa la libexpat di sistema. Con una versione vecchia, `%p;` ripetuto costa circa 0,5 ms l'uno (misurato: 100 ripetizioni = 0,05 s), quindi una pagina da 2 MB richiede minuti. Rimedio: se `expat.version_info < (2, 4, 0)` niente taglio (comportamento di main), con un test.
- **R-550-3 BASSA** (perdita di testo, verso sicuro): con il BOM UTF-8 (U+FEFF) più un errore la pagina sparisce tutta. `_decodifica` lascia il BOM nella stringa, la seconda lettura non lo riporta, startswith a modules/web/leggi.py:1398 fallisce e il risultato è 0. Esempio: «<U+FEFF><html><p>W1</p></html>CODA» diventa testo vuoto, mentre Chrome mostra W1. Il caso BOM in tests/test_unit_web_leggi.py:1979 non ha errore, quindi non lo prende.
- **R-550-4 BASSA** (test): sopravvivono «senza startswith» e «senza doppio escape». Manca un test con `&LT;`/`&AMP;` sotto DOCTYPE XHTML e uno sul ramo di mancata coincidenza (per esempio BOM più errore, dopo R-550-3).
- COSMETICA: le funzioni annidate `esterna`/`saltata` (modules/web/leggi.py:1372 e modules/web/leggi.py:1377) non hanno type hints (CLAUDE.md §4).

**Rischi esplicitamente esclusi**
- Il comportamento reale di Chrome e Firefox non l'ho provato su un browser (non disponibile qui). Mi baso sullo standard e sulla descrizione «rendering up to the first error».
- Il comportamento con una libexpat < 2.4 non l'ho verificato direttamente (qui c'è solo la 2.6.1). Il costo è stimato dalla misura per singola ripetizione.
- Nessun fuzz differenziale contro un parser XML di riferimento (per esempio libxml2): le sonde sono puntuali.
- Il percorso con GAS_WEB_LEXBOR=1 sulla suite vecchia (gli 11 FAIL dichiarati uguali a main) non l'ho rifatto.

Memoria: riga #550 più una lezione (controllo dei namespace; versione di expat), commit 78de08e.

### Review #551 (chat Mani) — diff committato in f7bb599 (verdetto riemesso)

## VERDETTO: APPROVATO CON RISERVE

Review #551 (chat Mani), riemessa senza caratteri invisibili. Diff staged su claude/peaceful-lovelace-0w2b7q (3 file, 189 righe aggiunte e 8 tolte). Chiude le riserve R-550-1, R-550-2, R-550-3 e R-550-4 della #550. Le riserve rimaste sono solo COSMETICHE.

**Elementi esaminati**
- modules/web/leggi.py:1374 — la prima lettura usa `namespace_separator=" "` (chiude R-550-1). Rischio: falsi errori su XHTML valido, oppure errori di namespace ancora non visti. Prove:
  - `<r><p>A</p><h:script>S</h:script><p>VIS</p></r>` tiene solo `<r><p>A</p>`.
  - `xmlns:a=""` taglia.
  - Due attributi doppi dopo l'espansione (`a:x`/`b:x` sullo stesso URI) tagliano.
  - Un `xlink:href` non dichiarato taglia.
  - `xmlns` di default più `xml:lang` passano interi, CODA esclusa.
  - Le entità del DTD XHTML funzionano ancora sotto i namespace (`&nbsp;` più CODA tiene «W1&nbsp;»).
  - tests/test_unit_web_leggi.py:1902 ha i prefissi dichiarati e resta verde.

  Esito: ok.
- modules/web/leggi.py:1368 — sotto expat 2.4.0 niente taglio (chiude R-550-2). Rischio: soglia sbagliata o test che non morde. La 2.4.0 è la versione che ha introdotto la protezione dall'amplificazione. Il mutante `if False` dà 1 failed. Anche il mio mutante a soglia 2.3.0 dà 1 failed, perché il test a tests/test_unit_web_leggi.py:2015 forza 2.3.0. Sulla 2.6.1 reale la bomba e `%p;`×1000 col pubblico XHTML si fermano ancora (0,06 s). Esito: ok.
- modules/web/leggi.py:1404 — il BOM (U+FEFF) in testa si conta a parte (chiude R-550-3). Rischio: un carattere di troppo o di meno. Prove:
  - BOM più CODA tiene «<U+FEFF><html><p>W1</p></html>», cioè 23 caratteri su 27.
  - BOM da solo, BOM più testo prima della radice e doppio BOM danno 0 (verso sicuro).
  - BOM più DOCTYPE XHTML più `&nbsp;` taglia giusto.
  - Il caso a tests/test_unit_web_leggi.py:1980 prende il mutante `bom = 0` (1 failed).

  Esito: ok.
- tests/test_unit_web_leggi.py:1983 — `&LT;`/`&AMP;` sotto DOCTYPE Strict (chiude R-550-4). Il mio mutante «senza doppio escape» dà 1 failed. Esito: ok.
- modules/web/leggi.py:1377 — type hints su `esterna`. Esito: riserva cosmetica, vedi R-551-1.

Il mutante «senza startswith» sopravvive ancora. Lo accetto come difesa verso il sicuro: nelle mie sonde (CRLF, CR da solo, surrogati, caratteri non-BMP, BOM) i pezzi coincidono sempre col testo.

Suite rifatte da me: tests/test_unit_web_leggi.py più tests/test_unit_web_lexbor.py danno 599 passed e 1 skipped su 3.13, 487 passed e 113 skipped su 3.11, uguali ai numeri dell'agente. Il file del modulo è stato ripristinato dopo i mutanti (cmp uguale, indice intatto).

**Riserve**
- **R-551-1 COSMETICA**: modules/web/leggi.py:1377 dichiara `contesto: str`, ma per il sottoinsieme esterno del DTD expat passa None. Il tipo giusto è `Optional[str]`.
- **R-551-2 COSMETICA**: con un DTD XHTML letto, un'entità sconosciuta (`&Unknown;`) fa scattare l'errore DOPO il riferimento. Il testo letterale «&Unknown;» resta quindi nel tenuto (124 caratteri su 135, tolti solo `</p></html>`). Non esce nessun contenuto nascosto: è il nome stesso dell'entità. Senza DTD il taglio cade prima del riferimento.

**Rischi esplicitamente esclusi**
- Non ho provato un'expat davvero < 2.4: qui c'è solo la 2.6.1 e il ramo è provato solo col monkeypatch.
- Non ho confrontato il risultato con Chrome reale (non disponibile) né con libxml2 tramite fuzz differenziale: le sonde sono puntuali.
- Non ho rifatto il percorso con GAS_WEB_LEXBOR=1 sulla suite vecchia.

Memoria: riga #551 (nessuna lezione nuova), commit fa715d8.

### Review #552 (chat Mani) — merge eaa0642

## VERDETTO: APPROVATO

Review #552 (chat Mani): merge non ancora committato di origin/main dc43ad6 (PR #292, chat Motore) in claude/peaceful-lovelace-0w2b7q (HEAD f7bb599, fetta 25 Mani).

Letture obbligatorie fatte: CLAUDE.md sez. 5, 6 e 8; reports/stato_progetto.md (solo le parti che servivano, con grep); le ultime voci di .claude/agents/memoria_revisore.md, compresa la lezione #551 Motore: «in un merge confrontare il diff verso ENTRAMBI i genitori».

Elementi esaminati:
- `modules/web/leggi.py:1515` — è la chiamata `_taglio_xml(grezzo, not pagina["troncato"])` dentro `_componi`. Rischio esaminato: il merge altera il codice della fetta 25 o lo mescola con quello di main. Esito ok: `git diff --cached HEAD -- modules tests/test_unit_web_leggi.py tests/test_unit_web_lexbor.py brains` è vuoto, e main non tocca modules/ né i test web dalla base 03dc898.
- `modules/web/leggi.py:1374` — è il parser expat con `namespace_separator` (chiusura di R-550-1, rivista in #551). Rischio esaminato: una regressione portata da main. Esito ok: il file è identico a HEAD e gli insiemi di file dei due rami sono disgiunti dalla base.
- `tests/test_unit_web_leggi.py:1987` — è `test_xhtml_malformato_fino_al_primo_errore`. Rischio esaminato: i test del ramo non passano più sull'albero fuso. Esito ok: ho rilanciato io leggi + lexbor + dotenv sull'albero fuso, 614 passed / 1 skipped.
- `gas.py:595` (contesto) — è `_DOTENV_SCAVALCATE`, che arriva da main. Rischio esaminato: il codice di main cambiato nel merge. Esito ok: `git diff --cached origin/main -- gas.py tests brains modules` mostra solo i 3 file della fetta 25, quindi gas.py e i test kernel e dotenv sono identici a main.
- `.claude/agents/memoria_revisore.md:965` — è la risoluzione del conflitto. Rischio esaminato: righe perse o duplicate. Esito ok: le righe rimosse verso HEAD sono 0 e verso main sono 0. Il conteggio torna: 965 righe = 946 della base + 3 del ramo + 16 di main. Nessuna riga duplicata, nessun marcatore di conflitto, `git diff --cached --check` pulito.
- I report (handoff, ultimo_report, diff_sessione, stato_progetto) — rischio esaminato: righe del ramo perse nella fusione automatica. Esito ok: il ramo non li aveva toccati dalla base (`git diff 03dc898 HEAD --stat` contiene solo leggi.py, i due test web e la memoria), quindi sono la versione di main ed è corretto.

Wall of Shame: il merge non aggiunge codice nuovo, quindi niente slicing della history né output dei tool simulati. Il limite di 10 iterazioni di `run_turn` e `_get_window()` non sono toccati.

Una riserva di processo (non blocca): le riserve COSMETICHE R-551-1 e R-551-2 della chat Mani (review #551) non sono ancora in reports/stato_progetto.md, perché il ramo non lo aggiornava dalla base. Vanno scritte lì al fine-task.

Rischi esclusi:
- Suite kernel non rilanciata da me. Resta il tuo dato (1058 PASS, 1 FAIL T31g per sqlite_vec assente, noto). Il codice del kernel è byte per byte quello di main, già rivisto nelle review #543–#551 Motore.
- I test di claude_cli non li ho rilanciati.
- Il comportamento sul Mac e sulla VPS non è verificabile in dev.

Gate B: il diff di sessione contro dc43ad6 conterrà leggi.py, i due test web, la memoria e i report. Le citazioni sopra su `modules/web/leggi.py` e `tests/test_unit_web_leggi.py` sono file di quel diff, quindi bastano per il gate; `gas.py` è solo contesto.

Memoria:
- Ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga «#552 (chat Mani) — 2026-10-29 — APPROVATO — … Nessuna lezione nuova.»
- `bash scripts/commit_memoria_revisore.sh` è FALLITO, come previsto durante un merge: `fatal: cannot do a partial commit during a merge.` (rc=128). Lo script è uscito con codice 0 e ha scritto il WARN in /home/user/Gas/gas_debug.log; l'index degli altri file è intatto.
- La riga #552 resta nel working tree, non in staging (il file risulta `MM`). Va aggiunta con `git add` prima di chiudere il merge, oppure committata subito dopo.

### Review #553 (chat Mani) — primo diff per le riserve del bot #296

## VERDETTO: APPROVATO CON RISERVE

Review #553 (chat Mani). Ho esaminato il diff staged su claude/peaceful-lovelace-0w2b7q (PR #296, HEAD 9837d0d). Prima ho letto CLAUDE.md, la parte che serviva di reports/stato_progetto.md e la memoria del revisore.

**Elementi del diff esaminati**
- modules/web/leggi.py:1383 — il DTD delle entità si legge una sola volta per pagina (`letto_dtd`). Rischio esaminato: costo del «%p;» ripetuto e mutante «DTD riletto ogni volta». Il mutante fa fallire 1 test (test_xhtml_dtd_letto_una_volta); 300 000 «%p;» passano in 0,13 s. Esito: **riserva** (R-553-1, sotto).
- modules/web/leggi.py:1379 — `contesto: Optional[str]` (chiude R-551-1). Rischio esaminato: nessun cambio di comportamento. Esito: ok.
- tests/test_unit_web_leggi.py:1916 — test parametrizzato con `expat.version_info` finto a (2,3,0). Rischio esaminato: che il caso «vecchio» provi davvero `_commenti_e_cdata_xml`. Mutante mio (la funzione restituisce il testo senza toccarlo): falliscono entrambi i parametri. Il monkeypatch viene ripristinato. Esito: ok.
- tests/test_unit_web_leggi.py:2024 — test_xhtml_dtd_letto_una_volta: conta le letture, controlla che le entità restino valide e che la CODA sia tagliata. Esito: ok.
- tests/test_unit_web_leggi.py:2038 — caso «%p;» × 300 000 dentro `_entro`. Esito: ok. Da solo però non prende il mutante, perché expat ferma comunque l'amplificazione: il controllo vero è il test che conta le letture.

**R-553-1 BASSA (regressione introdotta da questo diff, nel verso sicuro)**
- Alla seconda «%p;» `esterna` restituisce 1 senza creare né far girare il parser esterno.
- Per expat questo vuol dire «entità di parametro non letta». In un documento non standalone expat smette quindi di elaborare le dichiarazioni che seguono nel sottoinsieme interno.
- Prova: `<!DOCTYPE html [<!ENTITY % p PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "x.dtd">%p;%p;<!ENTITY foo "bar">]><html><p>A&foo;B</p></html>`. Prima del diff la pagina veniva tenuta intera; ora viene tagliata a «…<p>A&foo;».
- È una perdita di contenuto, non una fuga, e riguarda pagine rare.
- Con una sola «%p;», o con «%p;» insieme al sottoinsieme esterno PUBLIC XHTML, il comportamento resta corretto (sondato).
- Correzione provata, una riga: a ogni riferimento XHTML fare `lettore.ExternalEntityParserCreate(contesto).Parse(b"" if letto_dtd[0] else _dtd_entita(), True)` e poi `letto_dtd[0] = True`. Con questa le entità successive restano valide (`&foo;&nbsp;` tenuti, CODA tagliata) e 300 000 «%p;» passano in 0,39 s.
- Consiglio di applicarla in questa fetta, con un test su `%p;%p;<!ENTITY foo …>`. Il codice cambia, quindi serve una nuova review prima del commit.

**Prove mie**
- tests/test_unit_web_leggi.py: 467 passed / 1 skipped (3.13).
- Sottoinsieme xhtml: 81 passed.
- Nessun carattere Cf nel diff.
- Worktree ripristinato dopo ogni mutante (diff non staged vuoto, staged invariato).

**Rischio escluso**
- Non ho rilanciato la suite su Python 3.11 senza selectolax né la suite lexbor: mi fido delle prove dell'agente (489p/113s).
- Non ho confrontato Chrome/libxml2 su «%p;» non letto seguito da dichiarazioni: non c'è un browser in questo ambiente.
- Il mutante «commento senza fine tiene il resto» l'ho accettato come equivalente sulla parola dell'agente, senza riprodurlo.

Memoria aggiornata: riga #553 più una lezione su ExternalEntityRefHandler (tornare 1 senza far girare un parser esterno non vale come «letto»). Committata da sola con scripts/commit_memoria_revisore.sh: commit e5f4a62. L'index del diff sotto review è intatto.

File di riferimento: /home/user/Gas/modules/web/leggi.py, /home/user/Gas/tests/test_unit_web_leggi.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #554 (chat Mani) — diff committato in 0d5c258

## VERDETTO: APPROVATO

Review #554 (chat Mani), sul diff staged di claude/peaceful-lovelace-0w2b7q (PR #296). La correzione di R-553-1 funziona e il test nuovo sul taglio coglie davvero l'errore di un carattere. Ho letto prima CLAUDE.md, reports/stato_progetto.md e la memoria del revisore.

**Elementi del diff esaminati**
- modules/web/leggi.py:1386 — a ogni riferimento XHTML crea un parser esterno e gli fa leggere `b""` dalla seconda volta in poi (l'intero DTD solo la prima). Rischio esaminato: che dopo un secondo «%p;» le dichiarazioni successive vengano ignorate (R-553-1), e il costo di 300 000 riferimenti. Ho fatto due prove: «%p;%p;<!ENTITY foo "bar">» con `&foo;&nbsp;` nel corpo, e sottoinsieme esterno PUBLIC XHTML 1.1 più «%p;» con un'entità dichiarata dopo. In entrambe il taglio cade esattamente sulla CODA. 300 000 «%p;» passano in 0,33 s. Esito: ok.
- modules/web/leggi.py:1387 — `letto_dtd[0] = True` dopo la lettura. Rischio esaminato: che una lettura saltata o ripetuta resti senza test. Mutante «dalla seconda non letto» (la versione di #553): 1 failed. Mutante «DTD riletto ogni volta»: 1 failed. Esito: ok.
- tests/test_unit_web_leggi.py:2024 — test_xhtml_dtd_letto_una_volta, ora con un `<!ENTITY foo "W2">` dichiarato dopo 50 «%p;». Controlla che W1 e W3 restino e che la CODA sia tagliata. È questo test a cogliere entrambi i mutanti qui sopra. Esito: ok.
- tests/test_unit_web_leggi.py:2005 — test_xhtml_taglio_al_carattere_giusto, 5 casi con la lunghezza esatta (chiude V-2 della verifica esterna #296). Il BOM è scritto come escape nel sorgente: il controllo sui caratteri invisibili (categoria Cf) del diff è vuoto. Mutante «return bom + len(tenuto) + 1»: 5 failed. Esito: ok.

**Prove mie**
- tests/test_unit_web_leggi.py: 472 passed / 1 skipped (Python 3.13).
- Dopo ogni mutante ho ripristinato il file dall'index: diff non staged vuoto, staged invariato.

**Rischio escluso**
- Non ho rilanciato la suite su Python 3.11 senza selectolax né la suite lexbor: mi fido delle prove dell'agente (494 passed / 113 skipped).
- Non ho confrontato con Chrome/libxml2 il caso «dichiarazioni dopo un riferimento ripetuto»: qui non c'è un browser. La correzione riporta comunque il comportamento di prima del diff #553.

Memoria aggiornata con la riga #554 (nessuna lezione nuova), committata da sola con scripts/commit_memoria_revisore.sh nel commit e1fa7c1. L'index del diff sotto review non è stato toccato.

File: /home/user/Gas/modules/web/leggi.py, /home/user/Gas/tests/test_unit_web_leggi.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #555 (chat Mani) — merge 7cf7f19

## VERDETTO: APPROVATO

Review #555 (chat Mani). Ho esaminato il merge non ancora committato di origin/main 4e8eb9f (PR #295, chat Motore) in claude/peaceful-lovelace-0w2b7q (PR #296). HEAD è 0d5c258, la base comune è dc43ad6. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (riga 4 e blocco «Mani — fetta 25») e .claude/agents/memoria_revisore.md.

**Elementi esaminati:**
- `modules/web/leggi.py:1386` — riferimento a un DTD XHTML: crea un parser esterno a ogni riferimento e passa b"" dalla seconda volta. Rischio esaminato: che il merge alteri il codice rivisto in #554 (il caso R-553-1). Esito: ok. `git diff --cached HEAD` sui tre file web dà 0 righe e `git diff --cached origin/main` sul codice mostra solo modules/web/leggi.py, tests/test_unit_web_leggi.py e tests/test_unit_web_lexbor.py.
- `modules/web/leggi.py:1368` — senza taglio con expat < 2.4. Rischio esaminato: accoppiamento con le modifiche al loader del .env che arrivano da main. Esito: ok. modules/web non importa gas.py e le modifiche di main (contesto: `gas.py:629` insieme `visti`, `gas.py:654` confronto degli interruttori) toccano solo i registri del doctor e il salto delle chiavi ripetute, non il caricamento delle variabili lette dal modulo web.
- `tests/test_unit_web_leggi.py:2036` — test_xhtml_dtd_letto_una_volta. Rischio esaminato: un test perso o duplicato nel merge. Esito: ok. Il file è identico a HEAD e la suite web, dotenv e claude_cli rilanciata dà 652 passed, 1 skipped.
- `tests/test_unit_kernel.py:11206` (contesto, file identico a main) — kernel rilanciato sull'albero unito: 1058 PASS, 1 FAIL (T31g, sqlite_vec assente: problema noto, non è una regressione). Esito: ok.
- `.claude/agents/memoria_revisore.md:965` (contesto) — unione della memoria. Rischio esaminato: righe perse. Esito: ok. Il file ha 974 righe e non manca nessuna riga né di HEAD né di main. Le 4 righe aggiunte sono esattamente quelle che main ha aggiunto dalla base (#551, la lezione, #552, #553 della chat Motore). Nessuna riga duplicata.
- `reports/stato_progetto.md:4` (contesto) — riga «Ultimo aggiornamento». Esito: ok. Contiene la voce Mani (review #550–#555), poi «— prima:» e la riga 4 di main intera (verificato per stringa); la coda di HEAD è inclusa. La riga 589 è quella di main (il ramo non la toccava dalla base). Il blocco «Mani — fetta 25» è presente.
- Pulizia del merge: nessun marcatore di conflitto, `git diff --cached --check` pulito, 0 caratteri Unicode Cf nelle righe aggiunte del diff.

**Rischi esclusi:**
- Non ho rivisto nel merito le modifiche a gas.py e ai test dotenv/kernel della PR #295: sono già rivisti dalla chat Motore (#551–#553), e qui ho verificato solo che entrino identici a main.
- Non ho verificato il comportamento con selectolax o lexbor accesi su Python 3.11, né sul Mac o su una VPS: non riproducibile in questo ambiente.
- Ho controllato i report rigenerati al fine-task (handoff, ultimo_report, diff_sessione) solo come presenza, non come contenuto.

**Nota per il fine-task (non è una riserva sul merge):** il blocco «Mani — fetta 25» in reports/stato_progetto.md dice ancora «aperte R-551-1 (chat Mani)», ma è stata chiusa in #553. Vanno aggiunte anche R-553-1 (chiusa in #554) e le review #553–#555.

**Memoria:** ho aggiunto la riga «#555 (chat Mani) — 2026-10-29 — APPROVATO — … Nessuna lezione nuova.» in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. Lo script /home/user/Gas/scripts/commit_memoria_revisore.sh è uscito con 0, ma **non ha committato**: in gas_debug.log c'è «fatal: cannot do a partial commit during a merge», e l'index degli altri file è rimasto intatto. La riga resta nel working tree e non è in staging (stato MM): va messa in staging (`git add .claude/agents/memoria_revisore.md`) prima di chiudere il merge, così entra nel commit di merge o nel fine-task.

### Review #556 (chat Mani) — primo diff di questo giro (verdetto riemesso)

Il primo testo del #556 conteneva un BOM letterale (U+FEFF) e non si incolla qui: fa fede la riemissione, stesso esito e stessa sostanza.

## VERDETTO: APPROVATO CON RISERVE

Review #556 (chat Mani), riemessa senza caratteri Cf su richiesta del coordinatore. L'esito e la sostanza sono quelli originali. PR #296, branch claude/peaceful-lovelace-0w2b7q, diff staged di allora: 2 file, +14/-7.

**Cosa ho esaminato nel diff**
1. `modules/web/leggi.py:1414` — cambia il controllo del BOM: prima l'escape ASCII di U+FEFF (6 caratteri, già escape a HEAD e non un BOM letterale, verificato con od), ora `chr(0xFEFF)`. Rischio esaminato: un cambio di comportamento. Esito: **ok**, il valore è identico. Il carattere vero lo produceva il bot quando citava il codice: la difesa è sensata.
2. `tests/test_unit_web_leggi.py:1965` — aggiunge la costante `_BOM = chr(0xFEFF)`, usata in `tests/test_unit_web_leggi.py:1989`, `tests/test_unit_web_leggi.py:1990` e `tests/test_unit_web_leggi.py:2008`. Rischio esaminato: che i casi parametrizzati cambino. Esito: **ok**, stesse stringhe. Prove: XHTML 86 passed; leggi + lexbor 606 passed / 1 skipped.
3. `modules/web/leggi.py:1364` — docstring con la V-1 BASSA del bot (entità sconosciuta con DTD esterno = errore). Esito: **riserva** R-556-1. Il comportamento descritto corrisponde al codice: `saltata` solleva `_ErroreXml`; una sonda con DOCTYPE SYSTEM non standard e «&ignota;» dà un taglio a 57 caratteri su 69. Ma la frase «così fanno Firefox ed expat» è imprecisa: provato, expat da solo con un DTD esterno non dà errore, salta l'entità e chiama SkippedEntityHandler.
4. Caratteri Cf: 0 nel diff e 0 nell'intero modules/web/leggi.py. Esito: **ok**.

**Riserve**
- **R-556-1 (chat Mani), COSMETICA**: docstring da precisare con «come Firefox (expat con le entità saltate trattate come errore, qui `saltata`)».
- **R-556-2 (chat Mani), BASSA, preesistente, fuori dal diff**: `tests/test_unit_web_leggi.py:65` e `tests/test_unit_web_leggi.py:232` contenevano U+200B letterali: se citati dal bot, il check torna failure; scriverli come `chr(0x200B)`.

**Cosa NON ho verificato**
- Il comportamento di Chrome/libxml2: nessun browser in dev.
- Che il bot non scriva più caratteri Cf: non si riproduce in dev.
- La suite del kernel: il diff non tocca gas.py.

### Review #557 (chat Mani) — diff dopo R-556-1 e R-556-2

## VERDETTO: APPROVATO CON RISERVE

Review #557 (chat Mani), PR #296, branch claude/peaceful-lovelace-0w2b7q. Diff staged completo: 2 file, +16/-9 (modules/web/leggi.py, tests/test_unit_web_leggi.py). Contiene anche le correzioni R-556-1 e R-556-2.

**Cosa ho esaminato nel diff**
1. `modules/web/leggi.py:1365` — la docstring di `_taglio_xml` dice ora «come Firefox (expat con le entità saltate trattate come errore, qui `saltata`)». Rischio esaminato: che la docstring descriva male il codice. Esito: **ok**. È coerente con la sonda di #556: expat da solo con un DTD esterno salta l'entità, ed è il gestore `saltata` di Gas a sollevare `_ErroreXml`. **R-556-1 chiusa.**
2. `modules/web/leggi.py:1368` — è la stessa modifica, ma la riga risulta lunga 144 caratteri: l'a capo della docstring si è rotto, mentre le righe vicine stanno tra 48 e 92. Rischio esaminato: la leggibilità, non il comportamento (nel repo non c'è un linter della lunghezza; il file ha già 39 righe oltre i 100). Esito: **riserva** R-557-1, COSMETICA.
3. `tests/test_unit_web_leggi.py:65` e `tests/test_unit_web_leggi.py:232` — i due U+200B letterali ora sono `chr(0x200B)`: una concatenazione nel corpo della pagina di prova e una voce della tupla dei vietati. Rischio esaminato: che il test perda il caso del carattere invisibile tolto dal testo. Esito: **ok**. La stringa risultante è identica e test_pagina_html_testo_pulito_e_marcato passa. **R-556-2 chiusa.**
4. `modules/web/leggi.py:1414` e `tests/test_unit_web_leggi.py:1965` — `chr(0xFEFF)` e la costante `_BOM`, già esaminati in #556. Nessun cambio di comportamento. Esito: **ok**.
5. Scansione Cf con unicodedata: 0 caratteri in tutti e due i file del diff. Le righe TOLTE del diff testuale contengono ancora due U+200B (il contenuto vecchio). Va bene in git, ma il diff testuale non va incollato in handoff o report: va bene solo `--stat`.

Prove rilanciate da me: leggi + lexbor 606 passed / 1 skipped. Nessuno slicing della history, nessuna simulazione di tool, nessun guardrail toccato.

**Riserve**
- **R-557-1 (chat Mani), COSMETICA**: rimettere a capo `modules/web/leggi.py:1368` a circa 90 caratteri, come le righe vicine.

**Nota sulla mia memoria**
La riga #556 di `.claude/agents/memoria_revisore.md` (commit 54dea9d) conteneva un U+FEFF letterale. L'ho sostituito con il testo «U+FEFF» e la modifica NON è committata: va inclusa nel tuo commit, altrimenti il bot lo trova nel diff della PR. Ora la memoria ha 0 caratteri Cf.

**Cosa NON ho verificato**
- Il comportamento di Chrome/libxml2 citato nella docstring: non ho un browser in dev.
- Che il bot, sul nuovo head, non introduca da sé caratteri Cf citando altro codice: non si riproduce qui.
- La suite del kernel: il diff non tocca gas.py.

Ho controllato i due testi con unicodedata prima di consegnarli (copia in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/verdetti.md): 0 caratteri Cf, 0 escape con backslash. Nella memoria ho aggiunto la riga #557 e una lezione: il revisore non deve mai scrivere escape di caratteri invisibili, ma «U+XXXX». Il file /home/user/Gas/.claude/agents/memoria_revisore.md è modificato e NON committato, come richiesto: 979 righe, 0 Cf.

### Review #558 (chat Mani) — diff committato in c6b73cf

## VERDETTO: APPROVATO

Review #558 (chat Mani), PR #296, branch claude/peaceful-lovelace-0w2b7q. Diff staged completo: 2 file, +17/-9 (modules/web/leggi.py, tests/test_unit_web_leggi.py).

**Cosa ho esaminato nel diff**
1. `modules/web/leggi.py:1365` — docstring di `_taglio_xml` (righe 1365-1370) rimessa a capo. Rischio esaminato: che nel rifare gli a capo cambi il testo o resti una riga lunga. Esito: **ok**. Le parole sono le stesse di #557 e tutte le righe stanno tra 17 e 92 caratteri, come le vicine. **R-557-1 chiusa.**
2. `modules/web/leggi.py:1415` — il controllo del BOM con `chr(0xFEFF)`, spostato di una riga dalla docstring. Rischio esaminato: un cambio di comportamento. Esito: **ok**, il codice è identico a #557.
3. `tests/test_unit_web_leggi.py:65` e `tests/test_unit_web_leggi.py:232` — U+200B scritto come `chr(0x200B)`. Esito: **ok**, nessun cambio rispetto a #557 (la parte dei test del diff è invariata, +10/-5).
4. `tests/test_unit_web_leggi.py:1965` — la costante `_BOM` usata nei tre casi XHTML. Esito: **ok**, invariata.
5. Scansione Cf con unicodedata: 0 caratteri in modules/web/leggi.py, in tests/test_unit_web_leggi.py e nella memoria del revisore. Resta vera la nota di #557: le righe TOLTE del diff testuale contengono ancora i vecchi U+200B, quindi nei report va solo `--stat`, mai il diff testuale.

Prove rilanciate da me: leggi + lexbor 606 passed / 1 skipped. Nessuno slicing della history, nessuna simulazione di tool, nessun guardrail toccato.

**Cosa NON ho verificato**
- Il comportamento di Chrome/libxml2 citato nella docstring: nessun browser in dev.
- Che il bot, sul nuovo head, non introduca da sé caratteri Cf citando altro codice: non si riproduce qui.
- La suite del kernel: il diff non tocca gas.py.

---

Il testo sopra non contiene caratteri Cf né escape di invisibili. Nella memoria ho aggiunto la riga #558, senza lezioni nuove. Il file /home/user/Gas/.claude/agents/memoria_revisore.md è modificato e NON committato: contiene la correzione U+FEFF della riga #556 e le righe #557 e #558, che vanno nel tuo commit. Ora ha 980 righe e 0 caratteri Cf.

### Review #559 (chat Mani) — merge bd71498 di origin/main e106883 (PR #297) (verdetto riemesso)

Il primo verdetto #559 citava solo file arrivati da main, che con la base nuova e106883 non sono nel diff di sessione: gate B rosso. Il revisore l'ha riemesso con lo stesso esito e la stessa sostanza e le citazioni del codice del diff; fa fede questo. L'originale resta qui sotto in un blocco di codice.

## VERDETTO: APPROVATO

Review #559 (chat Mani), riemessa per il gate B dopo il commit del merge bd71498. L'esito e la sostanza sono quelli di prima; ho solo aggiunto citazioni dei file di codice del diff di sessione, che ora ha base e106883. Il merge riguarda origin/main e106883 (PR #297, chat Motore) dentro claude/peaceful-lovelace-0w2b7q (PR #296, prima del merge HEAD 6a3ef69, base comune 4e8eb9f).

Letture fatte: CLAUDE.md (sezione 5 e regole di gate), reports/stato_progetto.md (righe toccate dal merge), .claude/agents/memoria_revisore.md (coda e lezioni sui caratteri Cf di #556 e #557, applicate).

Elementi del diff di sessione esaminati (codice web, verificato identico al ramo prima e dopo il merge):
- modules/web/leggi.py:1358 — `_taglio_xml`, il taglio dell'XHTML malformato al primo errore XML (fetta 25). Rischio: il merge cambia il codice web del ramo. Prova: `git diff 6a3ef69 HEAD -- modules tests` tocca solo bot.py e i test notte/dotenv di main, quindi `modules/web/leggi.py` è byte per byte uguale al ramo già rivisto in #558. Esito: ok.
- modules/web/leggi.py:1415 — il BOM in testa contato a parte, scritto come chr(0xFEFF) senza carattere U+FEFF letterale. Rischio: un Cf letterale reintrodotto dalla risoluzione del merge, che il bot rifiuterebbe. Scansione con unicodedata dei file in stage: zero Cf. Esito: ok.
- tests/test_unit_web_leggi.py:65 — pagina di prova con il carattere a larghezza zero costruito come chr(0x200B), non letterale. Rischio: un Cf letterale nel test dopo il merge. Il file è identico a 6a3ef69 e l'ho rieseguito: passa. Esito: ok.
- tests/test_unit_web_lexbor.py:131 — casi parametrizzati, uno per ogni punto d'integrazione (V-1 ve #294). Rischio: righe perse o duplicate nella risoluzione. Il file è identico a 6a3ef69 (nessun diff in `git diff 6a3ef69 HEAD`). Esito: ok.

Elementi del merge controllati (contesto, file arrivati da main):
- modules/telegram/bot.py:589 e modules/telegram/bot.py:604 — la regex ancorata per «/forte@NomeBot» e il fail-closed quando il nome di Gas è ignoto. Prima del commit `git diff --cached origin/main` era vuoto su bot.py, tests/test_unit_dotenv.py e tests/test_unit_notte.py: sono identici a main e già rivisti dalla chat Motore in #554–#556. Esito: ok.
- .claude/agents/memoria_revisore.md:980-982 — le righe Motore #554–#556 vengono dopo le righe Mani #550–#558. Confronto con un Counter tra le righe dei due genitori e il risultato: nessuna riga persa. Esito: ok.
- reports/stato_progetto.md:4 — la riga «Ultimo aggiornamento» ha la voce Mani seguita, dopo «— prima:», dalla riga 4 di main intera. Le voci 3 e 4 della ripartenza Motore (reports/stato_progetto.md:589-590) sono uguali a main. Nessun marcatore di conflitto. Esito: ok.

Controlli complessivi:
- Antipattern della sezione 5 (slicing della history, output dei tool simulati): niente di nuovo, il merge non introduce logica.
- Prova eseguita da me: pytest su tests/test_unit_dotenv.py, tests/test_unit_notte.py e tests/test_unit_web_leggi.py, 685 passed / 1 skipped.

Rischi esclusi esplicitamente:
- Non ho rieseguito la suite del kernel (1058 PASS / 1 FAIL T31g). Mi fido dell'esito dichiarato: T31g dipende da sqlite_vec, che manca in questo ambiente, quindi qui non si può riprodurre.
- Non ho eseguito tests/test_unit_web_lexbor.py né provato il bot Telegram dal vivo in un gruppo, che in dev non si può riprodurre.
- Non ho valutato reports/handoff.md, reports/ultimo_report.md e reports/diff_sessione.md, che si riscrivono al fine-task.
- Non ho eseguito scripts/check_verdetto.py, come mi hai indicato.

Memoria: non l'ho toccata. La riga #559 scritta nel primo giro resta com'è. Non ho fatto commit.

File rilevanti:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /home/user/Gas/tests/test_unit_web_lexbor.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

Originale (non conta per il gate):

```
## VERDETTO: APPROVATO

Review #559 (chat Mani): merge non ancora committato di origin/main e106883 (PR #297, chat Motore) in claude/peaceful-lovelace-0w2b7q (PR #296, HEAD 6a3ef69, base comune 4e8eb9f).

Letture fatte: CLAUDE.md (sez. 5 e regole di gate), reports/stato_progetto.md (righe toccate dal merge), .claude/agents/memoria_revisore.md (coda, lezioni Cf di #556 e #557 applicate).

Elementi del diff esaminati:
- modules/telegram/bot.py:589 — regex ancorata `_FORTE_DESTINATARIO_RE` portata da main. Rischio: il merge altera il codice di main. Prova: `git diff --cached origin/main -- modules/telegram/bot.py` è vuoto. Esito: ok.
- modules/telegram/bot.py:604 — con `_BOT_USERNAME` ignoto il testo resta invariato (fail-closed, nessun turno del forte a pagamento). Rischio: guardrail perso nel merge. Il codice è identico a main, già rivisto dalla chat Motore in #556. Esito: ok.
- tests/test_unit_notte.py:2363 — test `/forte@GasBot`, `/forte@AltroBot` e nome ignoto, preso da main. Rischio: test perso o duplicato. Diff contro origin/main vuoto, il test gira. Esito: ok.
- tests/test_unit_dotenv.py:229 — test WARN «il .env lo spegne», preso da main. Diff contro origin/main vuoto. Esito: ok.
- .claude/agents/memoria_revisore.md:980-982 — righe Motore #554–#556 messe dopo le righe Mani #550–#558. Rischio: righe perse da uno dei due genitori. Ho confrontato con un Counter le righe di HEAD e di origin/main con l'index: nessuna riga manca da nessuno dei due. Nessun marcatore di conflitto. Esito: ok.
- reports/stato_progetto.md:4 — riga «Ultimo aggiornamento». Contiene prima la voce Mani e poi, dopo «— prima:», la riga 4 di main intera. Ho controllato con un test di inclusione: l'unica riga «persa» rispetto a main è la vecchia riga 4, che però è contenuta tutta nella nuova. Esito: ok.
- reports/stato_progetto.md:589-590 — voci 3 e 4 della ripartenza Motore. Mancano rispetto a HEAD perché il ramo non le toccava e il merge a 3 vie ha preso la versione di main, come atteso. Sono identiche a main. Esito: ok.

Controlli complessivi:
- Codice web e test web (modules/web/leggi.py, tests/test_unit_web_leggi.py, tests/test_unit_web_lexbor.py) e reports/ripartenza_mani.md contro HEAD: diff vuoto, quindi identici al ramo.
- `git diff --cached HEAD` tocca solo i 5 file attesi.
- Caratteri Unicode Cf: zero nei 5 file staged, controllati con unicodedata.
- Antipattern della sezione 5 (slicing della history, output dei tool simulati): niente di nuovo, il merge non introduce logica.
- Prova eseguita da me: pytest su tests/test_unit_dotenv.py, tests/test_unit_notte.py e tests/test_unit_web_leggi.py, 685 passed / 1 skipped.

Rischi esclusi esplicitamente:
- Non ho rieseguito la suite del kernel (1058 PASS / 1 FAIL T31g). Mi fido dell'esito dichiarato: T31g dipende da sqlite_vec, che manca in questo ambiente, quindi lì non si può riprodurre.
- Non ho verificato tests/test_unit_web_lexbor.py né il comportamento reale del bot Telegram in un gruppo, che in dev non si può riprodurre.
- reports/handoff.md, reports/ultimo_report.md e reports/diff_sessione.md tenuti dal ramo non li ho valutati: si riscrivono al fine-task.

Memoria: aggiunta in coda la riga #559 (chat Mani, APPROVATO, nessuna lezione nuova; zero Cf controllati). File messo in stage con `git add .claude/agents/memoria_revisore.md`, senza commit, come richiesto. Non ho eseguito commit_memoria_revisore.sh perché è incompatibile con l'indicazione «senza committare» su un merge in corso.

File rilevanti:
- /home/user/Gas/.claude/agents/memoria_revisore.md
- /home/user/Gas/reports/stato_progetto.md
- /home/user/Gas/modules/telegram/bot.py
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py; toccati `modules/web/leggi.py`, `tests/test_unit_web_leggi.py`, `tests/test_unit_web_lexbor.py`.
- Web suite (`tests/test_unit_web_*.py`, Python 3.13.16 con selectolax 1.0.2): prima 566 passed / 1 skipped (main 03dc898) → dopo 606 passed / 1 skipped (+40).
- Su Python 3.11 senza selectolax: 494 passed / 113 skipped in locale; in CI un test in più (`test_parser_aggiornato_rilevato` gira solo con CI=true).
- Suite vecchia con `GAS_WEB_LEXBOR=1`: gli stessi 11 FAIL di main, confrontati per nome.
- Dopo il merge di main e106883: web + dotenv + notte 819 passed / 1 skipped; kernel 1058 PASS, 1 FAIL (T31g, sqlite_vec assente nell'ambiente, noto; in CI 0 FAIL).
- Mutanti: elenco in `reports/ultimo_report.md`; difese equivalenti dichiarate.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub sulla PR #296.
- f7bb599: run 40794722150, `unit-suite` success, `handoff-check` failure (atteso: handoff di main).
- e9606d8: run 40795325706, `unit-suite` success (kernel 1065 PASS / 0 FAIL, web 488 / 112), `handoff-check` success; `verifica-bot` failure (caratteri invisibili nei verdetti incollati: corretto in 54fc5da/9837d0d).
- 9837d0d: `unit-suite` success, `handoff-check` success (run 40796099462); `verifica-bot` success, APPROVATO CON RISERVE (riserve chiuse in 0d5c258).
- 336e67c: `unit-suite` success, `handoff-check` success (run 40798502957); `verifica-bot` failure (BOM letterale nel testo del bot: corretto in c6b73cf).
- 6a3ef69: `unit-suite` success, `handoff-check` success (run 40800286577); `verifica-bot` success, APPROVATO CON RISERVE.

Mappatura commit→run:
- 78de08e, fa715d8: nessuna run (pushati con f7bb599). eaa0642: nessuna run (pushato con e9606d8). 54fc5da: nessuna run (pushato con 9837d0d).
- e5f4a62, e1fa7c1, 0d5c258, 7cf7f19: nessuna run (pushati con 336e67c).
- 54dea9d, c6b73cf: nessuna run (pushati con 6a3ef69).
- bd71498, 1739759 (fine-task fermato dal gate B prima del push) e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo l'albero del commit di testa).

## §7 RISERVE APERTE

- V-2 ve #296 / V-1 bot #296 BASSA: con un DOCTYPE a identificativo esterno non XHTML un'entità non dichiarata taglia (come Firefox); Chrome (libxml2) la tratta come avviso e mostra il resto. Verso sicuro, scelta dichiarata in docstring; da decidere insieme a R-551-2.
- V-3 ve #296 COSMETICA: un singolo token oltre ~2 MB fa perdere il resto di una pagina ben formata (solo charset non UTF-8 a 2 byte; verso sicuro, causa da indagare).
- Per la chat Motore: `scripts/bot_esito.py` boccia ogni verdetto del bot che contiene caratteri Cf, anche quando il bot li scrive da sé citando il codice (fuori dal mio perimetro).
- V-1 bot #296 su 6a3ef69 BASSA: entità generali dichiarate nel sottoinsieme interno del DOCTYPE non tagliano; html.parser non le espande e mostra il nome letterale (testo scelto dall'autore della pagina). Preesistente, stessa classe di R-551-2: prossima fetta.
- R-551-2 COSMETICA: con DTD XHTML un'entità sconosciuta resta come testo «&Unknown;» prima del taglio (niente contenuto nascosto).
- R-ve280-1 BASSA: i test lexbor con selectolax non girano nei check required. Chat Motore.
- R-546-1 BASSA: numeri delle review doppi tra le chat (anche #547–#559).
- Sul VPS serve libexpat ≥ 2.4 perché il taglio dell'XHTML sia attivo (sotto si legge come prima, R-550-2); nessun controllo nel doctor (V-5 ve #296).
