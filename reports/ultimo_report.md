# ULTIMO REPORT — 2026-10-29 — Mani fetta 26: XHTML, entità che Gas non sa espandere, avviso nel testo, token enormi (R6, chat Mani, PR #298)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #298 (https://github.com/Gasss23/Gas/pull/298): lo faccio io solo con verdetto del bot APPROVATO pulito; con riserve aspetto il tuo OK.
2. Accensione della lettura con lexbor: serve la chat Motore (`selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt`), poi `GAS_WEB_LEXBOR=1` sul VPS (Linux).
3. Poi, una alla volta: tempo di rete 12 s, R-ve235-7.

## Esito
- **PR #296 (fetta 25)**: MERGIATA su richiesta dell'operatore («mergia 296», f8b35ae). Bot su 06bc98e APPROVATO CON RISERVE (V-1 BASSA entità esterna generale col pubblico XHTML senza test; V-2 BASSA taglio senza segnale nel testo) → FATTE qui. Verifica esterna su 06bc98e arrivata dopo il merge: APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/296#issuecomment-6498712956); V-1 BASSA (= bot V-2) → FATTA; V-2 BASSA (= bot V-1, la parte «-1» non confermata) → FATTA col test; V-3 BASSA (entità HTML5 assenti dal DTD XHTML 1.0 accettate, come lo standard whatwg) → SALTATA — Gas segue lo standard, al più un carattere in più; V-4 COSMETICA (difese equivalenti) → SALTATA — già dichiarate.
- **Fetta 26 — «sistema il resto» (operatore)**:
  - V-1 bot #296 su 6a3ef69 (entità dichiarate nel DOCTYPE mostrate come «&foo;») e R-551-2 («&Unknown;» col DTD XHTML restava nel testo): FATTA — un'entità che html.parser non sa espandere ferma la lettura prima del riferimento; la posizione si prende nel gestore di expat.
  - Entità generale esterna (V-1 bot su 06bc98e): FATTA — ferma sempre la lettura, test dedicati (SYSTEM e pubblico XHTML, anche in un attributo).
  - V-3 ve #296 (token di qualche MB perdeva il resto): FATTA — seconda lettura senza il rinvio di expat 2.6.
  - Avviso nel testo quando l'XHTML si taglia (V-2 bot / V-1 ve su 06bc98e): FATTA.
  - V-2 ve / V-1 bot #296 (entità non dichiarata con DOCTYPE esterno non XHTML: Firefox taglia, Chrome no): SALTATA — scelta prudente già dichiarata, resta come sta.
- **Bot su 6512576 (PR #298)**: APPROVATO CON RISERVE (check success). V-1 BASSA (entità di HTML ridichiarata con lo stesso testo, `<!ENTITY nbsp "&#160;">`: si tagliava, con un avviso falso) → FATTA: conta come di HTML, mai con «<» o «&» nel valore; avviso riscritto, vero anche per le entità.
- **Verifica esterna su 6512576**: APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/298#issuecomment-6499083740). V-1 BASSA (prima lettura non finale col rinvio: token enorme nascondeva l'errore) → FATTA. V-2 BASSA (= V-1 bot) → FATTA. V-3 BASSA (tre test nuovi passano anche sulla base: sono di non regressione) → SALTATA — dichiarato qui. V-4 COSMETICA (V-n ambigui) → FATTA: in §7 dell'handoff l'id del commento accanto. V-5 informativa.
- **R-561-3** (del revisore, BASSA, preesistente: «</html>CODA<p>» faceva perdere tutta la pagina) → FATTA: la seconda lettura tiene i pezzi interi letti fino al suo errore.
- **Review**: #560 APPROVATO; #561 APPROVATO CON RISERVE (R-561-1 BASSA guardia «&» con AMP → FATTA; R-561-2 COSMETICA testo dell'avviso in stato_progetto → FATTA), riemessa APPROVATO sul diff intero; #562 APPROVATO; #563 sul diff di R-561-3.

## Prove
- Web suite 620 passed / 1 skipped (Python 3.13.16 con selectolax 1.0.2; su main f8b35ae: 606 / 1).
- Su Python 3.11 senza selectolax: 508 passed / 113 skipped.
- Mutanti presi: posizione presa dopo l'eccezione, entità esterna generale ignorata, niente DefaultHandler, rinvio acceso, niente avviso, dentro_dtd mai vero, saltata anche sulle entità di parametro, secondo «%p;» non letto (test R-553-1 riscritto con un ATTLIST), senza guardia «<», senza guardia «&», mai come HTML, rinvio acceso nella prima lettura, R-561-3 senza fix. Equivalenti: «la pagina non vince» in `dichiarata` (expat non riporta la dichiarazione doppia) e `valore is not None` (le esterne le ferma già `esterna`).
- Tempi: 2,8 MB 0,12 s; 200 000 «&nbsp;» col DTD 0,25 s.
- Kernel non toccato (nessun file fuori da modules/web e test web).

## RICHIESTE ALLA CHAT MOTORE
1. `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (R-ve280-1), poi `GAS_WEB_LEXBOR=1` sul VPS.
2. R-546-1: numeri delle review doppi tra le chat.
3. `scripts/bot_esito.py` boccia il verdetto quando il bot stesso scrive un carattere Cf citando il codice (successo due volte sulla #296).
4. Sul VPS serve libexpat ≥ 2.4 perché il taglio dell'XHTML sia attivo; un controllo nel doctor.

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
- La verifica esterna su 06bc98e è arrivata dopo il merge (autorizzato dall'operatore con le riserve del bot).
