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
- **Accensione lexbor, tempo di rete 12 s, R-ve235-7**: `DEFERITA — chat Motore / una alla volta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 modules/web/leggi.py               |  55 ++++++++++++++++++++++++++++++++++++-------
 reports/diff_sessione.md           |  15 ++++++------
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         |   6 ++---
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  47 +++++++++++++++---------------------
 tests/test_unit_web_leggi.py       |  42 +++++++++++++++++++++++++++++----
```

NB: base = merge-base con origin/main = f8b35ae. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
4c8c4b2 fix(web): XHTML, le entità che Gas non sa espandere fermano la lettura; avviso nel testo; token enormi (fetta 26 Mani)
517db4a chore(revisore): memoria review #560 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore 4c8c4b2: review #560. Verdetto integrale:

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

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py; toccati `modules/web/leggi.py` e `tests/test_unit_web_leggi.py`.
- Web suite (`tests/test_unit_web_*.py`, Python 3.13.16 con selectolax 1.0.2): prima 606 passed / 1 skipped (main f8b35ae) → dopo 616 passed / 1 skipped (+10).
- Su Python 3.11 senza selectolax: 504 passed / 113 skipped.
- Mutanti: elenco in `reports/ultimo_report.md`; uno equivalente dichiarato.
- Kernel non rilanciato: il diff non tocca gas.py né moduli che il kernel importa per i suoi test (dato della sessione precedente: 1058 PASS, 1 FAIL T31g per sqlite_vec assente; in CI 0 FAIL).

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 517db4a, 4c8c4b2: pushati insieme prima dell'apertura della PR #298; run non ancora disponibile alla scrittura dell'handoff.
- Il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (la run testerà solo l'albero del commit di testa).

## §7 RISERVE APERTE

- V-2 ve / V-1 bot #296 BASSA (scelta): entità non dichiarata con DOCTYPE esterno non XHTML: Gas taglia come Firefox, Chrome mostra il resto.
- V-3 ve #296 su 06bc98e BASSA (scelta): entità HTML5 assenti dal DTD XHTML 1.0 accettate, come lo standard whatwg.
- Nota del revisore #560 (non riserva): negli attributi expat espande le entità della pagina; innocuo, gli attributi XHTML non arrivano al testo.
- R-ve280-1 BASSA: i test lexbor con selectolax non girano nei check required. Chat Motore.
- R-546-1 BASSA: numeri delle review doppi tra le chat.
- Chat Motore: libexpat ≥ 2.4 sul VPS e controllo nel doctor; `scripts/bot_esito.py` boccia i verdetti del bot con caratteri Cf scritti dal bot stesso.
