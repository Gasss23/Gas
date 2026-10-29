# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Mani fetta 25: XHTML malformato letto fino al primo errore XML, come il browser (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #296 (https://github.com/Gasss23/Gas/pull/296). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5059998967","url":"https://github.com/Gasss23/Gas/pull/296"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve l'OK dell'operatore.
2. Accensione della lettura con lexbor: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (R-ve280-1); poi `GAS_WEB_LEXBOR=1` sul VPS.
3. Poi, una alla volta: tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #294 (fetta 24)**: `FATTA` — richiesta dell'operatore («mergia 294»), merge 03dc898. Verifica esterna #294 arrivata dopo il merge: APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/294#issuecomment-6484098213); V-1 (test dei punti d'integrazione): `FATTA` qui; V-2 (stato CI nell'handoff): `FATTA` (§6 qui sotto con le run reali); V-3 (commit doppio della memoria): `SALTATA — storia già pubblicata, niente riscritture`; V-4 (merge con riserve): autorizzato dall'operatore.
- **Fetta 25 — XHTML malformato (decisione dell'operatore: «vai con XHTML malformato», «sistema anche l'altro»)**: `FATTA`.
  - R-ve252-2 e R-ve255-1: `FATTA` — `_taglio_xml` in leggi.py.
  - R-550-1 (namespace), R-550-2 (expat < 2.4), R-550-3 (BOM), R-550-4 (test): `FATTA`, review #551.
  - R-551-1 e R-551-2 COSMETICHE: `DEFERITA — cosmetiche`.
  - Merge di main dc43ad6 (PR #292): `FATTA`, review #552.
- **Accensione lexbor (punto b)**: `DEFERITA — chat Motore`.
- **Tempo di rete 12 s, R-ve235-7 (punto e)**: `DEFERITA — una alla volta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/web/leggi.py               |  91 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  21 ++++++++-----------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   6 +++---
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  45 +++++++++++++++++++++++-----------------
 tests/test_unit_web_leggi.py       |  98 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 tests/test_unit_web_lexbor.py      |   8 ++++++++
```

NB: base = merge-base con origin/main = dc43ad6 (dopo il merge di main). Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
eaa0642 Merge origin/main (dc43ad6, PR #292) in claude/peaceful-lovelace-0w2b7q (fetta 25 Mani)
f7bb599 fix(web): XHTML malformato letto fino al primo errore XML, come il browser (fetta 25 Mani)
fa715d8 chore(revisore): memoria review #551 — APPROVATO CON RISERVE
78de08e chore(revisore): memoria review #550 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore f7bb599: review #550 sul primo diff, #551 dopo la chiusura di R-550-1..4 (diff committato in f7bb599). Merge eaa0642 (da main entrano gas.py e i test del kernel e di dotenv): review #552. Verdetti integrali:

### Review #550 (chat Mani) — primo diff staged

## VERDETTO: APPROVATO CON RISERVE

Review #550 (chat Mani). Diff staged su claude/peaceful-lovelace-0w2b7q, base main 03dc898, fetta 25 Mani (XHTML malformato, R-ve252-2, R-ve255-1, più V-1 ve #294). Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (in modo mirato) e la memoria. Nessun antipattern del Wall of Shame: il motore (gas.py, la history) non è toccato.

**Elementi esaminati**
- modules/web/leggi.py:1329 — insieme dei pubblici XHTML. Rischio: fedeltà allo standard. Ho scaricato la sorgente whatwg/html da raw.githubusercontent.com: le 11 voci coincidono esattamente con source:152092-152102. Esito: ok.
- modules/web/leggi.py:1372 — `esterna` carica il DTD solo per quei pubblici e risponde 1 per tutto il resto. Rischio: XXE e download. Ho provato un'entità generale `SYSTEM "file:///etc/passwd"`, un'entità di parametro SYSTEM e un'entità generale col pubblico XHTML: nessun file letto, nessuna rete. Nel terzo caso il DTD letto come contenuto dà errore e la pagina si taglia lì (verso sicuro). Questo rispetta «should not attempt to retrieve any other external entity» (source:152105). Esito: ok.
- modules/web/leggi.py:1348 — doppio escape di «<» e «&» nel DTD. Rischio: markup iniettato attraverso le entità. `&LT;b&GT;&AMP;` sotto DOCTYPE Strict dà il testo «<b>&», senza tag. Esito: ok. Il test però manca (vedi R-550-4).
- modules/web/leggi.py:1394 — seconda lettura grezza sul prefisso fino all'errore. Rischio: testo che sfugge dopo l'errore, mezzo tag rimasto. Ho fatto 13 sonde sull'intera `_componi`: script con CDATA o carattere non valido, `</script x x>`, style, template, noscript, svg title, commento, CDATA, script non chiuso. In nessuna SEGRETO esce e non resta mai mezzo tag. CRLF dentro il testo e negli attributi viene conservato dal DefaultHandler, quindi il controllo startswith regge. Esito: ok.
- modules/web/leggi.py:1383 — prima lettura con expat 2.6.1. Rischio: bomba di entità e DoS. La bomba del test si ferma. Ho provato anche `%p;` ripetuto 1000 volte col pubblico XHTML (riparserebbe ogni volta il DTD da 59 KB): expat lo ferma con «limit on input amplification factor», in 0,09 s. Esito: ok, ma la sicurezza dipende dalla versione di expat (R-550-2).
- modules/web/leggi.py:1508 — chiamata in `_componi` con `completo = not troncato`, più warning nella scatola nera. Rischio §9. Un'eccezione inattesa arriva all'`except Exception` di leggi_pagina, che restituisce «errore nella pulizia della pagina», senza crash. Il test tests/test_unit_web_leggi.py:1988 copre il caso troncato. Esito: ok.
- tests/test_unit_web_leggi.py:1518 — `_radice` avvolge i frammenti dei vecchi test. Rischio: test indeboliti. Le asserzioni non cambiano, cambia solo l'input. Esito: ok.
- tests/test_unit_web_lexbor.py:131 — tabella degli 8 punti d'integrazione più malignmark. Esito: ok, passano.

Rifatte da me: tests/test_unit_web_leggi.py più tests/test_unit_web_lexbor.py danno 595 passed e 1 skipped su 3.13, 483 passed e 113 skipped su 3.11 (expat 2.6.1 su entrambi). I tuoi numeri (586/1 e 483/104) vengono da un insieme di 587 test, il mio ne ha 596: va solo allineato il conteggio nel report.

Mutanti miei (poi ripristinato il file, cmp uguale):
- «entità saltata senza errore»: 1 failed, preso.
- «senza startswith»: sopravvive.
- «senza doppio escape»: sopravvive.
- «senza esclusione di amp/lt/gt/quot/apos»: sopravvive, ma è equivalente (il ridichiararle col doppio escape è innocuo).

**Riserve (da tracciare in stato_progetto.md)**
- **R-550-1 BASSA** (testo in più rispetto al browser, non regressione): modules/web/leggi.py:1369 crea expat senza `namespace_separator`, quindi non vede gli errori di namespace. Per lo standard (source:152321) e per Chrome sono fatali. Esempio: `<r><p>A</p><h:script>S</h:script><p>VIS</p></r>` (prefisso h non dichiarato) viene tenuto intero, mentre Chrome si ferma prima di h:script. Con `namespace_separator=" "` expat dà «unbound prefix». Rimedio: un parametro nella prima lettura, compatibile con tests/test_unit_web_leggi.py:1902 (lì i prefissi sono dichiarati).
- **R-550-2 BASSA** (robustezza su VPS): la difesa contro la bomba e contro il DTD ripetuto si appoggia alla protezione da amplificazione di expat, che esiste da 2.4.0. Su Linux CPython usa la libexpat di sistema. Con una versione vecchia, `%p;` ripetuto costa circa 0,5 ms l'uno (misurato: 100 ripetizioni = 0,05 s), quindi una pagina da 2 MB richiede minuti. Rimedio: se `expat.version_info < (2, 4, 0)` niente taglio (comportamento di main), con un test.
- **R-550-3 BASSA** (perdita di testo, verso sicuro): con BOM UTF-8 più un errore la pagina sparisce tutta. `_decodifica` lascia il BOM nella stringa, la seconda lettura non lo riporta, startswith a modules/web/leggi.py:1398 fallisce e il risultato è 0. Esempio: `﻿<html><p>W1</p></html>CODA` diventa testo vuoto, mentre Chrome mostra W1. Il caso BOM in tests/test_unit_web_leggi.py:1979 non ha errore, quindi non lo prende.
- **R-550-4 BASSA** (test): sopravvivono «senza startswith» e «senza doppio escape». Manca un test con `&LT;`/`&AMP;` sotto DOCTYPE XHTML e uno sul ramo di mancata coincidenza (per esempio BOM più errore, dopo R-550-3).
- COSMETICA: le funzioni annidate `esterna`/`saltata` (modules/web/leggi.py:1372 e modules/web/leggi.py:1377) non hanno type hints (CLAUDE.md §4).

**Rischi esplicitamente esclusi**
- Il comportamento reale di Chrome e Firefox non l'ho provato su un browser (non disponibile qui). Mi baso sullo standard e sulla descrizione «rendering up to the first error».
- Il comportamento con una libexpat < 2.4 non l'ho verificato direttamente (qui c'è solo la 2.6.1). Il costo è stimato dalla misura per singola ripetizione.
- Nessun fuzz differenziale contro un parser XML di riferimento (per esempio libxml2): le sonde sono puntuali.
- Il percorso con GAS_WEB_LEXBOR=1 sulla suite vecchia (i tuoi 11 FAIL uguali a main) non l'ho rifatto.

Memoria aggiornata: riga #550 più una lezione (controllo dei namespace; versione di expat). Committata da scripts/commit_memoria_revisore.sh nel commit 78de08e (solo /home/user/Gas/.claude/agents/memoria_revisore.md, l'indice staged è intatto: 3 file, 171 righe aggiunte e 8 tolte).

File rilevanti: /home/user/Gas/modules/web/leggi.py, /home/user/Gas/tests/test_unit_web_leggi.py, /home/user/Gas/tests/test_unit_web_lexbor.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #551 (chat Mani) — diff committato in f7bb599

## VERDETTO: APPROVATO CON RISERVE

Review #551 (chat Mani). Diff staged su claude/peaceful-lovelace-0w2b7q (3 file, 189 righe aggiunte e 8 tolte). Chiude le riserve R-550-1, R-550-2, R-550-3 e R-550-4 della #550. Le riserve rimaste sono solo COSMETICHE.

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
- modules/web/leggi.py:1404 — il BOM in testa si conta a parte (chiude R-550-3). Rischio: un carattere di troppo o di meno. Prove:
  - BOM più CODA tiene `﻿<html><p>W1</p></html>`, cioè 23 caratteri su 27.
  - BOM da solo, BOM più testo prima della radice e doppio BOM danno 0 (verso sicuro).
  - BOM più DOCTYPE XHTML più `&nbsp;` taglia giusto.
  - Il caso a tests/test_unit_web_leggi.py:1980 prende il mutante `bom = 0` (1 failed).

  Esito: ok.
- tests/test_unit_web_leggi.py:1983 — `&LT;`/`&AMP;` sotto DOCTYPE Strict (chiude R-550-4). Il mio mutante «senza doppio escape» dà 1 failed. Esito: ok.
- modules/web/leggi.py:1377 — type hints su `esterna`. Esito: riserva cosmetica, vedi R-551-1.

Il mutante «senza startswith» sopravvive ancora. Lo accetto come difesa verso il sicuro: nelle mie sonde (CRLF, CR da solo, surrogati, caratteri non-BMP, BOM) i pezzi coincidono sempre col testo.

Suite rifatte da me: tests/test_unit_web_leggi.py più tests/test_unit_web_lexbor.py danno 599 passed e 1 skipped su 3.13, 487 passed e 113 skipped su 3.11, uguali ai tuoi numeri. Il file del modulo è stato ripristinato dopo i mutanti (cmp uguale, indice intatto).

**Riserve**
- **R-551-1 COSMETICA**: modules/web/leggi.py:1377 dichiara `contesto: str`, ma per il sottoinsieme esterno del DTD expat passa None. Il tipo giusto è `Optional[str]`.
- **R-551-2 COSMETICA**: con un DTD XHTML letto, un'entità sconosciuta (`&Unknown;`) fa scattare l'errore DOPO il riferimento. Il testo letterale «&Unknown;» resta quindi nel tenuto (124 caratteri su 135, tolti solo `</p></html>`). Non esce nessun contenuto nascosto: è il nome stesso dell'entità. Senza DTD il taglio cade prima del riferimento.

**Rischi esplicitamente esclusi**
- Non ho provato un'expat davvero < 2.4: qui c'è solo la 2.6.1 e il ramo è provato solo col monkeypatch.
- Non ho confrontato il risultato con Chrome reale (non disponibile) né con libxml2 tramite fuzz differenziale: le sonde sono puntuali.
- Non ho rifatto il percorso con GAS_WEB_LEXBOR=1 sulla suite vecchia.

Memoria aggiornata con la riga #551 (nessuna lezione nuova), committata da scripts/commit_memoria_revisore.sh nel commit fa715d8. Il report della #550 era già stato consegnato prima; questo è quello della #551.

File rilevanti: /home/user/Gas/modules/web/leggi.py, /home/user/Gas/tests/test_unit_web_leggi.py, /home/user/Gas/tests/test_unit_web_lexbor.py, /home/user/Gas/.claude/agents/memoria_revisore.md

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

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py; toccati `modules/web/leggi.py`, `tests/test_unit_web_leggi.py`, `tests/test_unit_web_lexbor.py`.
- Web suite (`tests/test_unit_web_*.py`, Python 3.13.16 con selectolax 1.0.2): prima 566 passed / 1 skipped (main 03dc898) → dopo 599 passed / 1 skipped (+33).
- Su Python 3.11 senza selectolax (come la CI): 487 passed / 113 skipped.
- Suite vecchia con `GAS_WEB_LEXBOR=1` (`tests/test_unit_web_leggi.py`): gli stessi 11 FAIL di main, confrontati per nome (fuori scope: differenze note tra lettura di sempre e lexbor).
- Dopo il merge di main dc43ad6: web + dotenv + claude_cli 643 passed / 1 skipped; kernel 1058 PASS, 1 FAIL (T31g, sqlite_vec assente nell'ambiente, noto).
- Mutanti: elenco in `reports/ultimo_report.md`; difese equivalenti dichiarate.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub sulla PR #296.
- Head f7bb599: run 40794722150 con `unit-suite` success e `handoff-check` failure (atteso: l'handoff era ancora quello di main); `verifica-bot` skipped (run 40795130002, etichetta non ancora messa).

Mappatura commit→run:
- 78de08e, fa715d8: nessuna run su questo SHA (pushati insieme a f7bb599).
- f7bb599: run 40794722150 (sopra).
- eaa0642 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo l'albero del commit di testa).

## §7 RISERVE APERTE

- R-551-1 COSMETICA: in `esterna` il tipo di `contesto` dovrebbe essere `Optional[str]`.
- R-551-2 COSMETICA: con DTD XHTML un'entità sconosciuta resta come testo «&Unknown;» prima del taglio (niente contenuto nascosto).
- R-ve280-1 BASSA: i test lexbor con selectolax non girano nei check required. Chat Motore.
- R-546-1 BASSA: numeri delle review doppi tra le chat (anche #547–#551).
- Sul VPS serve libexpat ≥ 2.4 perché il taglio dell'XHTML sia attivo (sotto si legge come prima, R-550-2).
