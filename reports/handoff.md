# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Mani fetta 26: XHTML, entità che Gas non sa espandere, avviso nel testo, token enormi (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #298 (https://github.com/Gasss23/Gas/pull/298). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5069479872","url":"https://github.com/Gasss23/Gas/pull/298"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve l'OK dell'operatore.
2. Accensione della lettura con lexbor: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (R-ve280-1); poi `GAS_WEB_LEXBOR=1` sul VPS.
3. Poi, una alla volta: tempo di rete 12 s, R-ve235-7.

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #296 (fetta 25)**: `FATTA` — richiesta dell'operatore («mergia 296»), merge f8b35ae. Bot su 06bc98e APPROVATO CON RISERVE (V-1 e V-2 BASSE: chiuse qui). Verifica esterna su 06bc98e arrivata dopo il merge, APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/296#issuecomment-6498712956): V-1 e V-2: `FATTA`; V-3 (entità HTML5 fuori dal DTD XHTML 1.0 accettate): `SALTATA — Gas segue lo standard whatwg`; V-4: `SALTATA — difese equivalenti già dichiarate`.
- **Fetta 26 — «sistema il resto» (operatore)**: `FATTA`.
  - V-1 bot #296 su 6a3ef69 e R-551-2 (entità della pagina o sconosciute mostrate come «&nome;»): `FATTA`.
  - V-1 bot #296 su 06bc98e (entità generale esterna col pubblico XHTML, senza test): `FATTA`.
  - V-3 ve #296 (token di qualche MB perdeva il resto): `FATTA`.
  - V-2 bot / V-1 ve #296 su 06bc98e (taglio senza segnale nel testo): `FATTA`.
  - V-2 ve / V-1 bot #296 (DOCTYPE esterno non XHTML: Firefox taglia, Chrome no): `SALTATA — scelta prudente già dichiarata`.
- **Secondo giro (PR #298, bot e verifica esterna su 6512576, https://github.com/Gasss23/Gas/pull/298#issuecomment-6499083740)**: V-1 bot = V-2 ve (entità di HTML ridichiarata con lo stesso testo tagliata, con un avviso falso): `FATTA`; V-1 ve (prima lettura non finale col rinvio di expat): `FATTA`; V-3 ve (tre test di non regressione): `SALTATA — dichiarato in §5`; V-4 ve (V-n ambigui): `FATTA` in §7; V-5 ve: informativa. R-561-1 (guardia «&» con AMP): `FATTA`; R-561-2 (testo dell'avviso in stato_progetto): `FATTA`; R-561-3 («</html>CODA<p>» perdeva la pagina): `FATTA`.
- **Accensione lexbor, tempo di rete 12 s, R-ve235-7**: `DEFERITA — chat Motore / una alla volta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++
 modules/web/leggi.py               |  70 ++++++++++++++++++++++++++++++++++++++++++-------
 reports/diff_sessione.md           |  15 +++++------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   6 ++---
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  50 ++++++++++++++++-------------------
 tests/test_unit_web_leggi.py       |  55 ++++++++++++++++++++++++++++++++++++---
```

NB: base = merge-base con origin/main = f8b35ae. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
7b84873 fix(web): XHTML, «</html>CODA<p>» non fa più perdere tutta la pagina (R-561-3)
0a33ccf chore(revisore): memoria review #563 — APPROVATO
6d42d67 chore(revisore): memoria review #562 — APPROVATO
7f571ee fix(web): XHTML, entità ridichiarate con lo stesso testo di HTML lette; prima lettura senza rinvio (V-1 bot e V-1 ve #298)
a3d180d chore(revisore): memoria review #561 — APPROVATO
3670472 chore(revisore): memoria review #561 — APPROVATO CON RISERVE
6512576 docs(fine-task): Mani fetta 26 — XHTML, riserve rimaste della #296, handoff e report (PR #298)
4c8c4b2 fix(web): XHTML, le entità che Gas non sa espandere fermano la lettura; avviso nel testo; token enormi (fetta 26 Mani)
517db4a chore(revisore): memoria review #560 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore 4c8c4b2: review #560. Commit motore 7f571ee: review #561 (prima stesura su una parte del diff, poi riemessa sul diff intero: fa fede la riemessa) e #562. Commit motore 7b84873: review #563. Verdetti integrali:

### Review #560 (chat Mani) — diff committato in 4c8c4b2

## VERDETTO: APPROVATO

Review #560 (chat Mani), fetta 26 Mani. Ho esaminato il diff STAGED (`git diff --cached`) su branch claude/peaceful-lovelace-0w2b7q, base f8b35ae. Letture obbligatorie fatte: CLAUDE.md sez. 5/8/9, reports/stato_progetto.md (le voci su XHTML e #296), .claude/agents/memoria_revisore.md (lezioni #550–#559, tra cui quella su ExternalEntityRefHandler e b"").

Elementi del diff esaminati:
1. modules/web/leggi.py:1394 — `ferma()` prende `CurrentByteIndex` dentro il gestore, prima di sollevare l'eccezione. Rischio esaminato: che la posizione cada dopo il riferimento (R-551-2). Expat imposta l'inizio dell'evento all'inizio del token prima di chiamare il gestore, quindi la posizione è il «&». Col mutante «posizione presa dopo l'eccezione» falliscono 4 test. Se `fermo` restasse a -1, `max(errore, 0)` dà 0, cioè non si legge niente (verso sicuro). Esito: ok.
2. modules/web/leggi.py:1426 — DefaultHandler vuoto nella prima lettura. Rischio esaminato: che le entità interne finiscano al gestore di default invece che a SkippedEntityHandler. Nella sorgente di expat (doContent), con l'espansione spenta lo SkippedEntityHandler ha la precedenza sul default. Le cinque entità predefinite restano normali caratteri: la sonda «&amp;&lt;&gt;&quot;&apos;&nbsp;&eacute;» col DTD Strict non taglia. Il freno contro la bomba di entità vale ancora negli attributi, dove expat espande sempre: la bomba in un attributo si ferma in 0,06 s. Col mutante «niente DefaultHandler» falliscono 3 test. Esito: ok.
3. modules/web/leggi.py:1404 — un'entità generale esterna (contesto non None) ferma la lettura prima di qualsiasi parser figlio. Rischio esaminato: che il DTD venga letto come contenuto, oppure che un riferimento a un DTD o a un'entità di parametro (contesto None) venga fermato per sbaglio. Il caso `[%q;]` con DOCTYPE SYSTEM non taglia. Col mutante «contesto ignorato» fallisce 1 test. Esito: ok.
4. modules/web/leggi.py:1415 — `dichiarata`: dentro_dtd separa le entità di HTML da quelle della pagina, e vale la prima dichiarazione. Sonde:
   - un'entità di parametro interna che ridichiara nbsp prima del DTD esterno: la lettura si ferma su &nbsp;;
   - nbsp ridichiarato dalla pagina dopo «%p;»: vale quello di HTML (come in expat e nel browser) e il &foo; successivo ferma.
   Col mutante «dentro_dtd sempre vero» falliscono 4 test. Esito: ok.
5. modules/web/leggi.py:1440 — `SetReparseDeferralEnabled(False)` nella seconda lettura, protetto da hasattr. Rischio esaminato: un token di qualche MB rinviato. Col mutante «rinvio acceso» fallisce 1 test. Esito: ok.
6. modules/web/leggi.py:1588 — l'avviso sta tra il corpo e «[… testo troncato]», dentro il marcatore NON FIDATO, ed esce solo se c'è stato il taglio. tests/test_unit_web_leggi.py:2038 lo verifica anche per HTML e per la pagina troncata da Gas. Esito: ok.
7. tests/test_unit_web_leggi.py:2017 — «&Unknown;» col DTD XHTML taglia esattamente prima del riferimento. tests/test_unit_web_leggi.py:2085 — il nuovo test di R-553-1 usa un ATTLIST con xmlns:h, coerente con la lezione della memoria sulle entità di parametro non lette. Esito: ok.

Prove mie:
- Suite web leggi: 482 passed, 1 skipped su Python 3.13.16 (expat 2.6.1). Test XHTML: 96 passed su 3.11.
- Tempi: 700 000 tag «<b/>» (2,8 MB) in 0,14 s; 200 000 «&nbsp;» in 0,09 s; 3 MB di testo a righe in 0,30 s.
- Zero caratteri Cf nei due file e nella memoria.
- Dopo i mutanti il file è identico all'originale (cmp) e lo SHA del diff staged non è cambiato.

Antipattern: nessuno slicing della history, nessuna simulazione di tool. Il kernel non è toccato.

Osservazione, non riserva: negli attributi expat espande in silenzio le entità della pagina e ignora quelle sconosciute col DTD. Lì quindi la lettura non si ferma, e la docstring di modules/web/leggi.py:1367 vale solo per il testo. È innocuo: in XHTML gli attributi non arrivano al testo per il modello. La sonda `<p title="&foo;">W1</p><p>W3</p>` dà W1 e W3, senza «&foo;».

Rischi esclusi:
- Il ramo senza `SetReparseDeferralEnabled` (expat sotto 2.6) non l'ho eseguito: sia su 3.11 sia su 3.13 qui c'è libexpat 2.6.1. Il codice lo salta con hasattr, quindi al massimo torna il comportamento di prima.
- Il confronto diretto con Firefox e Chrome non l'ho fatto: niente browser in questo ambiente. Mi sono basato sulla sorgente di expat.
- Il mutante «la pagina non vince» lo do per equivalente sulla parola della chat Mani: non l'ho rifatto.

Memoria: aggiunta la riga #560 (chat Mani) in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola con scripts/commit_memoria_revisore.sh (commit 517db4a). L'index del diff è intatto, verificato con lo SHA. Nessuna lezione nuova.

### Review #561 (chat Mani) — prima stesura, su una parte del diff poi committato in 7f571ee

## VERDETTO: APPROVATO CON RISERVE

Review #561 (chat Mani), PR #298, diff staged su HEAD 6512576 (sha256 del diff staged 5acc33b8…, rimasto uguale prima e dopo la review). Ho letto CLAUDE.md, reports/stato_progetto.md (la parte che serviva) e la memoria del revisore.

Elementi del diff esaminati:
- modules/web/leggi.py:1417 — `dichiarata` ora riceve il valore dell'entità. Rischio: il valore potrebbe non essere quello che il browser rilegge. Ho verificato che expat lo passa coi riferimenti numerici già espansi: «&#160;» e «\xa0» letterale danno lo stesso risultato. Le entità esterne, quelle NDATA e le entità di parametro hanno valore None oppure di_parametro vero, quindi restano escluse. — ok
- modules/web/leggi.py:1420 — `come_html` vale solo se il valore è uguale a quello di html5 e non contiene «<» né «&». Rischio: contare come di HTML un'entità che nel browser produce markup o un errore. Sonde lette per intero: nbsp uguale, prima dichiarazione uguale e seconda diversa, NotEqualTilde (2 code point), not, amp/lt/gt predefinite. Sonde tagliate: valore diverso, NBSP maiuscolo, prima dichiarazione diversa e seconda uguale (vale la prima, giusto), entità esterna, NDATA, entità di parametro con lo stesso nome, dichiarazione dopo un «%p;» non letto. — ok
- modules/web/leggi.py:1593 — nuovo testo dell'avviso. Rischio: un avviso falso. Il testo è vero in tutti e due i casi (XML malformato o entità che Gas non sa espandere). Nel codice non resta nessun riferimento al vecchio testo. — ok
- tests/test_unit_web_leggi.py:1998 — nbsp ed eacute ridichiarati senza DTD XHTML, letti per intero. Il mutante «mai come html» dà 1 failed. — ok
- tests/test_unit_web_leggi.py:2022 — nvlt con «&#60;» tagliato. Il mutante «senza guardia <» dà 1 failed. — ok
- tests/test_unit_web_leggi.py:2047 — l'avviso nel test è allineato al nuovo testo. — ok

Riserve:
- R-561-1 BASSA: la guardia su «&» NON è equivalente, al contrario di quanto dice il report. In html5 esistono anche le varianti maiuscole AMP e AMP; (valore «&»), e in XML non sono predefinite. `<!DOCTYPE html [<!ENTITY AMP "&#38;">]><html><p>A&AMP;B</p><p>CODA</p></html>` è un errore XML: ho fatto la prova con expat che espande davvero e dà «unclosed token». Il codice attuale taglia, quindi il comportamento è giusto. Ma col mutante «senza guardia &» il taglio sparisce (letto tutto) e i test restano verdi (98 passed sui test xhtml). Da fare: aggiungere questo caso alla parametrizzazione del taglio vicino a tests/test_unit_web_leggi.py:2022 e correggere la frase sull'equivalenza nel report e nell'handoff.
- R-561-2 COSMETICA: reports/stato_progetto.md:634 cita ancora il vecchio avviso «[pagina XHTML malformata: il resto non si legge, come nel browser]».

Prove mie: tests/test_unit_web_leggi.py 484 passed / 1 skipped su Python 3.13.16 (expat 2.6.1). Tre mutanti fatti da me: «senza <» 1 failed, «mai come html» 1 failed, «senza &» 98 passed (vedi R-561-1). Il file è stato ripristinato (cmp identico al blob staged). Zero caratteri Cf nel diff e nella mia riga di memoria.

Rischio escluso: non ho verificato Python 3.11 e non ho confrontato con un browser reale (Firefox/Chrome). Il confronto col browser l'ho approssimato con un parser expat che espande davvero le entità. Sul 3.11 mi fido del dato dichiarato (506 passed / 113 skipped).

Attenzione, lavoro in parallelo: mentre facevo i mutanti, nella cartella di lavoro sono comparse modifiche non staged a modules/web/leggi.py e a tests/test_unit_web_leggi.py (SetReparseDeferralEnabled nella prima lettura, V-1 della verifica esterna #298). Per un momento c'era anche una riga sbagliata in `_imposta_timeout` (riga 670: `lettore.SetReparseDeferralEnabled(False)` al posto di `pass`), poi tornata a `pass`. Ho ripristinato modules/web/leggi.py tre volte da una copia fatta prima di quelle modifiche, quindi posso aver cancellato una tua modifica fatta nel frattempo: ricontrolla `git diff` (non staged) prima di andare avanti. Queste modifiche non staged NON fanno parte di questa review e vanno revisionate a parte. L'index non l'ho mai toccato.

Memoria: riga #561 aggiunta in .claude/agents/memoria_revisore.md, con una lezione sulle varianti maiuscole delle entità di html5. Committata da sola col commit 3670472 tramite scripts/commit_memoria_revisore.sh, index del diff intatto.

### Review #561 (chat Mani) — riemessa sul diff intero, committato in 7f571ee

## VERDETTO: APPROVATO

Review #561 (chat Mani), PR #298, rifatta con lo stesso numero sul diff staged intero: V-1 del bot #298, V-1 della verifica esterna #298 e il test AMP. Lo sha256 del diff staged è f1cd8f63…, uguale prima e dopo la review. La cartella di lavoro cambiava mentre lavoravo, quindi test e mutanti li ho fatti su un export dell'index (`git checkout-index`, dentro lo scratchpad), con i file verificati uguali allo staged. Questo verdetto sostituisce quello di prima (APPROVATO CON RISERVE): la riserva BASSA R-561-1 è chiusa dal nuovo test, e la COSMETICA R-561-2 (sotto) diventa una nota.

Elementi del diff esaminati (righe del file staged):
- modules/web/leggi.py:1382 — rinvio di expat spento anche nella prima lettura, con hasattr. Rischio 1: lentezza, perché c'è una sola Parse e il rinvio serve solo con tante Parse piccole. 700 000 tag con lettura non finale in 0,27 s; un token da 3 MB troncato a metà in 0,01 s, senza errore. Rischio 2: expat sotto la 2.6, dove il metodo manca, protetto dall'hasattr. Mutante «riga tolta» → 1 failed (tests/test_unit_web_leggi.py:2066). — ok
- modules/web/leggi.py:1424 — `come_html` vale solo se il valore è uguale a quello di html5 e non contiene «<» né «&». Rischio: contare come di HTML un'entità che nel browser produce markup o un errore. Sonde lette per intero: nbsp uguale («&#160;» o letterale), prima dichiarazione uguale, NotEqualTilde, not, amp/lt/gt predefinite. Sonde tagliate: valore diverso, NBSP maiuscolo, prima dichiarazione diversa, entità esterna, NDATA, entità di parametro con lo stesso nome, dichiarazione dopo un «%p;» non letto. — ok
- modules/web/leggi.py:1598 — nuovo testo dell'avviso, vero in tutti e due i casi. — ok
- tests/test_unit_web_leggi.py:2024 — `<!ENTITY AMP "&#38;">` tagliato. Chiude R-561-1: AMP maiuscolo vale «&» in HTML ma in XML non è predefinita, ed expat che espande davvero dà «unclosed token». Mutante «senza guardia &» → 1 failed (prima 98 passed). — ok
- tests/test_unit_web_leggi.py:1998 (nbsp/eacute letti) e tests/test_unit_web_leggi.py:2022 (nvlt tagliato) — mutanti «senza guardia <» e «mai come html» → 1 failed ciascuno (prima stesura). — ok

Prove: tests/test_unit_web_leggi.py 485 passed / 1 skipped su Python 3.13; test xhtml 99 passed su Python 3.11 (expat 2.6.1 in tutti e due). Zero caratteri Cf nel diff e nella memoria.

Rischio escluso: niente confronto con un browser reale (Firefox/Chrome). L'ho approssimato con un parser expat che espande davvero le entità. Su 3.11 non ho rifatto i mutanti, solo i test.

Problema vecchio, non di questo diff (c'è già su origin/main), BASSA, perdita nel verso sicuro: con `<html><p>A</p></html>CODA<p>` `_taglio_xml` restituisce 0 e Gas non legge niente, mentre Chrome mostra «A». Causa: expat segna l'errore al «<» dopo «CODA» (colonna 25). La seconda lettura di `dati[:25]` trova prima la «junk after document element» (colonna 21) e nel ramo `except expat.ExpatError: return 0` butta via i pezzi buoni già letti. Rimedio possibile: in quel ramo tenere i pezzi raccolti. Da tracciare come nuova riserva della tua area.

Nota (era R-561-2, cosmetica): reports/stato_progetto.md:634 cita ancora il vecchio avviso «[pagina XHTML malformata: il resto non si legge, come nel browser]».

Avviso: durante la prima stesura avevo ripristinato modules/web/leggi.py nella cartella di lavoro da una mia copia, mentre tu stavi modificando. Ricontrolla di non aver perso modifiche. Ora git status dice «M » su tutti e due i file del diff, cioè cartella di lavoro uguale all'index.

Memoria: la riga #561 in .claude/agents/memoria_revisore.md è stata riscritta con l'esito nuovo, più una lezione (mutanti solo su un export dell'index quando l'agente lavora in parallelo). Committata da sola col commit a3d180d tramite scripts/commit_memoria_revisore.sh, index del diff intatto.

### Review #562 (chat Mani) — diff committato in 7f571ee

## VERDETTO: APPROVATO

Review #562 (chat Mani), PR #298. Come mi hai chiesto a metà review, l'ho chiusa sul commit 7f571ee e non sull'index. Prima ho controllato che il commit sia proprio il diff revisionato: lo sha256 di `git diff 3670472 7f571ee` sui due file è f1cd8f63, e i due file di 7f571ee sono identici byte per byte alla copia in scratchpad su cui ho provato i mutanti. Le citazioni sono a HEAD.

Elementi del diff esaminati:
- `modules/web/leggi.py:1382` — anche la prima lettura gira senza rinvio (`SetReparseDeferralEnabled(False)`, con hasattr). Rischio esaminato: un token di qualche MB rinviato in una lettura non finale nasconde l'errore che viene dopo; oppure si crea un costo quadratico. Esito ok. Il mutante senza la riga dà 1 failed (3000051 invece di 3000038). Non c'è rischio quadratico perché `Parse` viene chiamata una volta sola su tutti i dati. Sonde: pagina troncata a metà di un attributo da 3 MB, letta tutta in 0,013 s; entità sconosciuta dopo un commento da 3 MB con completo=False, taglio giusto dopo `<p>`.
- `modules/web/leggi.py:1424` — un'entità della pagina conta come di HTML solo se il valore c'è, non contiene «<» né «&», ed è uguale a quello di html5. Rischio esaminato: una guardia rotta che fa leggere il resto della pagina. Esito ok. Mutanti: senza «&» 1 failed (R-561-1 chiusa), senza «<» 1 failed, «mai come html» 1 failed. Il mutante che toglie `valore is not None` resta verde: la guardia è ridondante ma innocua, perché le entità esterne le ferma già il gestore `esterna` e NDATA è un errore XML (sondato: zzz SYSTEM, nbsp SYSTEM e NDATA si fermano tutti a «W1 »).
- `modules/web/leggi.py:1598` — nuovo testo dell'avviso, allineato al test a `tests/test_unit_web_leggi.py:2049`. Esito ok.
- `tests/test_unit_web_leggi.py:2024` — caso `<!ENTITY AMP "&#38;">`: la pagina si taglia. È il test che mancava nella #561 e morde. Esito ok.
- `tests/test_unit_web_leggi.py:2066` — caso completo=False nel test del token enorme. È l'unico test che fa fallire il mutante sulla riga 1382. Esito ok.
- `tests/test_unit_web_leggi.py:1998` — nbsp ed eacute ridichiarati dalla pagina vengono letti. Esito ok.
- Riga 670 di `modules/web/leggi.py` (`_imposta_timeout`): non compare in nessun hunk (gli hunk sono a 1379, 1412 e 1583) e a HEAD è `pass`. Esito ok.

Prove: i test di `tests/test_unit_web_leggi.py` danno 485 passed / 1 skipped sia su Python 3.13 sia su 3.11 (expat 2.6.1 in entrambi). Il diff ha zero caratteri Cf e nessun escape di caratteri invisibili. I mutanti li ho fatti solo sulla copia in scratchpad (/tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/r562), non sulla cartella reale né sull'index.

Nota cosmetica (non è una riserva): la docstring di `test_xhtml_token_enorme_non_perde_il_resto` parla ancora solo della seconda lettura.

Rischio escluso: non ho verificato un Python con expat 2.6 ma senza il metodo `SetReparseDeferralEnabled`. Qui non è riproducibile (sia 3.13 sia 3.11 ce l'hanno). Lì hasattr salta la riga e il nuovo caso a `tests/test_unit_web_leggi.py:2066` fallirebbe. È lo stesso schema già presente per la seconda lettura, quindi non è un rischio nuovo. Non ho riprodotto nemmeno il tuo ambiente 3.11 con 113 skipped.

Note di processo:
- La cartella di lavoro ha di nuovo `modules/web/leggi.py` e `tests/test_unit_web_leggi.py` modificati, non in staging. Come mi hai chiesto non li ho guardati: non fanno parte di questa review.
- 7f571ee è stato committato prima che la #562 finisse, sulla base della #561 riemessa (riga già in memoria). Ora la #562 lo conferma.

Memoria: riga #562 (chat Mani) aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola con `scripts/commit_memoria_revisore.sh` (commit 6d42d67). Index non toccato. Nessuna lezione nuova.

### Review #563 (chat Mani) — diff committato in 7b84873

## VERDETTO: APPROVATO

Review #563 (chat Mani): PR #298, branch claude/peaceful-lovelace-0w2b7q, HEAD 6d42d67, diff staged su modules/web/leggi.py e tests/test_unit_web_leggi.py. Ho fatto le tre letture obbligatorie: CLAUDE.md sez. 5, reports/stato_progetto.md (letto per Grep sulle parti che servivano) e la coda di .claude/agents/memoria_revisore.md. Ho provato il codice su un export dell'index (git checkout-index nello scratchpad). L'export è identico a `git show :modules/web/leggi.py`.

Elementi esaminati:
- modules/web/leggi.py:1453 — quando la seconda lettura grezza dà ExpatError, ora si tengono i pezzi letti fin lì invece di restituire 0. Rischio: tenere testo dopo il primo errore vero, o mezzo tag. Esito: ok.
  - La seconda lettura gira solo su dati[:errore], quindi non va mai oltre l'errore della prima lettura, che fa tutti i controlli (namespace, entità, DTD).
  - Il DefaultHandler di expat riceve solo token interi: il token che dà l'errore, o un tag rimasto a metà, non arriva mai in `pezzi`.
  - Fuzz con 60 000 pagine casuali, ciascuna con completo=True e con completo=False, su Python 3.13 e 3.11 (expat 2.6.1). Ci sono 830 differenze rispetto al vecchio codice, e partono tutte dal vecchio 0.
  - In nessun caso il testo tenuto finisce a metà tag (0 casi).
  - Il testo tenuto, riletto con un parser stretto non finale con i namespace attivi, non dà mai errori (0 casi).
- modules/web/leggi.py:1461 — i controlli che seguono (prefisso del testo, almeno un tag d'apertura, BOM). Rischio: il ramo nuovo li scavalca. Esito: ok.
  - Sonde: «X<html>…» resta 0.
  - «</html><r/>» e «</html>CODA<p>B</p>» danno 21.
  - BOM seguito da «…</html>CODA<p>» dà 22.
  - «<h:p>» con prefisso non dichiarato dà ancora 6; «&foo;» dà ancora 10.
  - DOCTYPE seguito da «</html>CODA<p>» dà 36.
- tests/test_unit_web_leggi.py:2014 — il caso nuovo («<html><p>A</p></html>», «CODA<p>B</p>»). Rischio: un test che passa anche senza il fix. Esito: ok. Il mutante col vecchio «return 0» (su una copia nello scratchpad) dà 1 failed, proprio su quel caso (asserzione a tests/test_unit_web_leggi.py:2034).
- tests/test_unit_web_leggi.py:2061 — docstring di test_xhtml_token_enorme_non_perde_il_resto, che ora cita entrambe le letture. Rischio: nessuno, è solo testo. Esito: ok.

Altre prove:
- Suite web sull'export: 620 passed, 1 skipped (Python 3.13). Il file di leggi da solo: 486 passed, 1 skipped.
- 0 caratteri Cf nei due file e nella memoria; nessun escape di caratteri invisibili nel diff né nel mio testo.
- Nessun antipattern della Wall of Shame: non si tocca la history, non si simulano output dei tool.
- Il modulo resta FAIL-SAFE: un'ExpatError non esce dalla funzione, al massimo il taglio torna 0.

Rischio escluso: non ho confrontato i risultati con Chrome o Firefox veri (nessun browser in questo ambiente). Che il risultato sia «come il browser» poggia sul fatto dichiarato nel task (Chrome mostra «A»), più il controllo con un parser stretto, che dimostra solo che il testo tenuto è un prefisso senza errori. Non ho rifatto la suite web completa su Python 3.11: lì ho fatto girare solo il fuzz.

Memoria: aggiunta la riga #563 (chat Mani) e una lezione (fuzz rispetto al vecchio codice quando un ramo d'errore diventa meno severo). Ho committato solo quel file con scripts/commit_memoria_revisore.sh, commit 0a33ccf. L'index con il diff staged è intatto.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /home/user/Gas/.claude/agents/memoria_revisore.md
- Script del fuzz e delle sonde: /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/sonda.py

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py; toccati `modules/web/leggi.py` e `tests/test_unit_web_leggi.py`.
- Web suite (`tests/test_unit_web_*.py`, Python 3.13.16 con selectolax 1.0.2): prima 606 passed / 1 skipped (main f8b35ae) → dopo 620 passed / 1 skipped (+14).
- Su Python 3.11 senza selectolax: 508 passed / 113 skipped.
- Tre casi nuovi passano anche sulla base (V-3 ve #298): `[%q;]` con DOCTYPE SYSTEM, entità PUBLIC XHTML con `&e;`, `<p a="&e;">`: sono di non regressione, non di chiusura.
- Mutanti: elenco in `reports/ultimo_report.md`; due equivalenti dichiarati.
- Kernel non rilanciato: il diff non tocca gas.py né moduli che il kernel importa per i suoi test (dato della sessione precedente: 1058 PASS, 1 FAIL T31g per sqlite_vec assente; in CI 0 FAIL).

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 517db4a, 4c8c4b2: nessuna run (pushati con 6512576).
- 6512576: run 40888229820, `unit-suite` success, `handoff-check` success; `verifica-bot` success, APPROVATO CON RISERVE (V-1 BASSA: chiusa in 7f571ee).
- 3670472, 7f571ee, a3d180d, 6d42d67, 7b84873, 0a33ccf e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testerà solo l'albero del commit di testa).

## §7 RISERVE APERTE

- V-2 BASSA della verifica esterna #296 su 336e67c (https://github.com/Gasss23/Gas/pull/296#issuecomment-6485248441) = V-1 bot #296 su 336e67c, scelta: entità non dichiarata con DOCTYPE esterno non XHTML: Gas taglia come Firefox, Chrome mostra il resto.
- V-3 BASSA della verifica esterna #296 su 06bc98e (https://github.com/Gasss23/Gas/pull/296#issuecomment-6498712956), scelta: entità HTML5 assenti dal DTD XHTML 1.0 accettate, come lo standard whatwg.
- V-3 BASSA della verifica esterna #298 su 6512576 (https://github.com/Gasss23/Gas/pull/298#issuecomment-6499083740): tre test nuovi sono di non regressione (dichiarato in §5).
- Nota del revisore #560 (non riserva): negli attributi expat espande le entità della pagina; innocuo, gli attributi XHTML non arrivano al testo.
- R-ve280-1 BASSA: i test lexbor con selectolax non girano nei check required. Chat Motore.
- R-546-1 BASSA: numeri delle review doppi tra le chat (anche #560–#563).
- Chat Motore: libexpat ≥ 2.4 sul VPS e controllo nel doctor; `scripts/bot_esito.py` boccia i verdetti del bot con caratteri Cf scritti dal bot stesso.
