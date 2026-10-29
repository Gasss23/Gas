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
- **Accensione lexbor (punto b)**: `DEFERITA — chat Motore`.
- **Tempo di rete 12 s, R-ve235-7**: `DEFERITA — una alla volta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   8 ++++++++
 modules/web/leggi.py               |  99 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  18 ++++++++++--------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   6 +++---
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  40 ++++++++++++++++++++++++++++------------
 tests/test_unit_web_leggi.py       | 137 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------
 tests/test_unit_web_lexbor.py      |   8 ++++++++
```

NB: base = merge-base con origin/main = 4e8eb9f (dopo il merge di main). Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
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

Commit motore f7bb599: review #550 e #551. Merge eaa0642: review #552. Commit motore 0d5c258: review #553 e #554. Merge 7cf7f19: review #555. Nota: i verdetti #550 e #551 incollati nel commit e9606d8 contenevano un BOM invisibile (U+FEFF), che fa bocciare il bot; il revisore li ha riemessi con lo stesso esito e la stessa sostanza, il BOM scritto in chiaro: fanno fede questi, gli originali restano nella storia di e9606d8. Verdetti integrali:

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

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py; toccati `modules/web/leggi.py`, `tests/test_unit_web_leggi.py`, `tests/test_unit_web_lexbor.py`.
- Web suite (`tests/test_unit_web_*.py`, Python 3.13.16 con selectolax 1.0.2): prima 566 passed / 1 skipped (main 03dc898) → dopo 606 passed / 1 skipped (+40).
- Su Python 3.11 senza selectolax: 494 passed / 113 skipped in locale; in CI un test in più (`test_parser_aggiornato_rilevato` gira solo con CI=true).
- Suite vecchia con `GAS_WEB_LEXBOR=1`: gli stessi 11 FAIL di main, confrontati per nome.
- Dopo il merge di main 4e8eb9f: web + dotenv + claude_cli 652 passed / 1 skipped; kernel 1058 PASS, 1 FAIL (T31g, sqlite_vec assente nell'ambiente, noto; in CI 0 FAIL).
- Mutanti: elenco in `reports/ultimo_report.md`; difese equivalenti dichiarate.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub sulla PR #296.
- f7bb599: run 40794722150, `unit-suite` success, `handoff-check` failure (atteso: handoff di main).
- e9606d8: run 40795325706, `unit-suite` success (kernel 1065 PASS / 0 FAIL, web 488 / 112), `handoff-check` success; `verifica-bot` failure (caratteri invisibili nei verdetti incollati: corretto in 54fc5da/9837d0d).
- 9837d0d: `unit-suite` success, `handoff-check` success (run 40796099462); `verifica-bot` success, APPROVATO CON RISERVE (riserve chiuse in 0d5c258).

Mappatura commit→run:
- 78de08e, fa715d8: nessuna run (pushati con f7bb599). eaa0642: nessuna run (pushato con e9606d8). 54fc5da: nessuna run (pushato con 9837d0d).
- e5f4a62, e1fa7c1, 0d5c258, 7cf7f19 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo l'albero del commit di testa).

## §7 RISERVE APERTE

- R-551-2 COSMETICA: con DTD XHTML un'entità sconosciuta resta come testo «&Unknown;» prima del taglio (niente contenuto nascosto).
- R-ve280-1 BASSA: i test lexbor con selectolax non girano nei check required. Chat Motore.
- R-546-1 BASSA: numeri delle review doppi tra le chat (anche #547–#553).
- Sul VPS serve libexpat ≥ 2.4 perché il taglio dell'XHTML sia attivo (sotto si legge come prima, R-550-2); nessun controllo nel doctor (V-5 ve #296).
