# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-22 — Chat Mani, fetta 12: script a doppio escape, DOCTYPE e PI in XHTML, parser vecchi (R6)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #252: solo con verdetto del bot APPROVATO puro sull'head finale e CI verde, oppure con il tuo ok.
2. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; chiuderla bene richiede un vero costruttore HTML5 (es. lexbor): decidi tu.
3. Sul Mac e sulla VPS, dalla cartella di Gas: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` deve dire True (se dice False Gas lo scrive ora anche in gas_debug.log).
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

---

## §1 SCOPE & ESITO FETTE

- **R-454-2**: `FATTA`
- **R-453-2 (chat Mani)** (con B-482-1 e B-483-1 ALTE): `FATTA`
- **V-2 ve #242**: `FATTA`
- **R-466-1, R-466-2, R-ve245b-4**: `FATTA`
- **R-482-1**: `FATTA`
- **Secondo giro, bot e verifica esterna #252 BOCCIATO su 3cea14e**: V-1 MEDIA `FATTA`; V-2 bot / V-5 ve `FATTA`; V-3 ve e R-485-1 `FATTA`; V-4 ve (merge di main) `FATTA`; V-6 ve `FATTA`; V-2 ve registrata come R-ve252-2 (BASSA preesistente, da decidere)
- **Terzo giro, bot #252 su 3c0be94 APPROVATO CON RISERVE (COSMETICHE) e seconda verifica esterna APPROVATO CON RISERVE**: V-1 ve bis BASSA (PI senza nome) `FATTA` (B-488-1); V-2 ve bis BASSA (test) `FATTA`; V-1 bot COSMETICA (descrizione PR) `FATTA`; V-2 bot COSMETICA (Event+Lock) aperta

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  12 +++
 modules/web/leggi.py               | 199 ++++++++++++++++++++++++++++++++++---
 reports/diff_sessione.md           |  13 ++-
 reports/handoff.md                 |  95 +-----------------
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  33 ++++--
 tests/test_unit_web_leggi.py       | 174 +++++++++++++++++++++++++++++++-
 7 files changed, 403 insertions(+), 125 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
719d3ce fix(web): fetta 12 — PI XHTML solo con nome XML valido, test <scripts> (V-1/V-2 ve #252 bis)
2cf21e5 chore(revisore): memoria review #489 — APPROVATO
9293b9b chore(revisore): memoria review #488 — BOCCIATO
3c0be94 docs(reports): fetta 12 chat Mani, secondo giro — report, handoff, stato
13b7526 Merge origin/main (PR #251) in feat/mani-web-fetta12 (V-4 ve #252)
f644a04 fix(web): fetta 12 — prologo XHTML dopo il DOCTYPE, test dei mutanti (V-1/V-5 bot e ve #252)
42077c0 chore(revisore): memoria review #486 — APPROVATO
e5548a0 chore(revisore): memoria review #485 — APPROVATO CON RISERVE
3cea14e docs(reports): fine fetta 12 chat Mani — report, handoff, stato
621da82 feat(web): fetta 12 — script a doppio escape, DOCTYPE e PI in XHTML, parser vecchi (R6)
d1fff5f chore(revisore): memoria review #484 — APPROVATO
6e8872b chore(revisore): memoria review #483 — BOCCIATO
5dbbe9a chore(revisore): memoria review #482 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; il §2 è preso dall'index con i report già in stage, quindi l'elenco dei file è esatto e i numeri dei report possono differire di poco.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Otto verdetti, incollati integralmente (chat Mani): #482 (BOCCIATO, B-482-1), #483 (BOCCIATO, B-483-1) e #484 (APPROVATO) sul diff della fetta 12 committato in `621da82`; #485 (APPROVATO CON RISERVE) e #486 (APPROVATO) sul secondo giro committato in `f644a04`; #487 (APPROVATO) sul merge di main 2abc23b, commit `13b7526`; #488 (BOCCIATO, B-488-1) e #489 (APPROVATO) sul terzo giro committato in `719d3ce`. Le righe citate nelle review intermedie si riferiscono al diff di allora.

### Review #482 (chat Mani) — verdetto integrale (diff staged della fetta 12, prima del rimedio)

## VERDETTO: BOCCIATO

Review #482 (chat Mani), fetta 12. Diff staged su `modules/web/leggi.py` e `tests/test_unit_web_leggi.py`, ramo feat/mani-web-fetta12, base main 7af0c48. Prima della review ho letto CLAUDE.md, i blocchi «Mani» di `reports/stato_progetto.md` e la mia memoria.

**Motivo del blocco: B-482-1 (ALTA, nuova fuga rispetto a main)**
- `modules/web/leggi.py:1203` — Per il DOCTYPE con sottoinsieme interno il codice cerca «[» e poi `]\s*>` (`modules/web/leggi.py:1170`) senza saltare né i testi tra virgolette né i commenti.
- Il rischio esaminato è una fine del DOCTYPE diversa da quella dell'XML.
- Esito: blocco. Ho provato il codice staged, su Python 3.13, con pagine `application/xhtml+xml`:
  - `<!DOCTYPE html SYSTEM "[">` + `<html xmlns=…><body><script>if(a[0]>1){}SEGRETO</script>VIS…`: il «[» tra virgolette fa cercare `]>` fino a `a[0]>` dentro lo script. Il testo da lì in poi diventa visibile e il modello riceve `1){}SEGRETOVIS`. Su main 7af0c48 SEGRETO era nascosto, quindi è una regressione. Stessa cosa con `SYSTEM '['` e `<style>a[x]>b{}SEGRETO</style>`.
  - `<!DOCTYPE html [<!-- ]>SEGRETO -->]>…`: arriva SEGRETO. Su main era nascosto, perché il commento veniva tolto per primo. Anche questa è una regressione.
  - Due casi lasciano passare SEGRETO anche su main, quindi la fuga era già lì e R-453-2 non è chiusa del tutto: `<!ENTITY x "]>SEGRETO">` e `SYSTEM ">" [<!ENTITY x "<b>SEGRETO</b>">]>`. In più, `<!ENTITY x "<b>SEGRETO</b>">` su main usciva e con il diff è nascosto.
- Rimedio, provato in una copia nella scratchpad: una funzione `_fine_doctype` che salta i testi tra `'…'` e `"…"`; dentro il sottoinsieme salta anche `<!--…-->` e `<?…?>`. Si ferma a «>» fuori dal sottoinsieme, oppure a «]» seguito da spazi e «>». Se qualcosa non si chiude, restituisce -1 e il resto viene scartato. Con questo le 7 sonde XHTML danno 0 SEGRETO e VIS presente, e la suite resta verde (333 passed). Nella versione vera le ricerche di commenti e PI senza fine vanno fatte con `find` e uscita subito a -1. La mia regex di prova con `.*?` può diventare quadratica con tanti `<!--` aperti.
- Servono test per le sonde sopra, con `SYSTEM "["` seguito da `]>` dentro uno script e il commento con `]>` nel sottoinsieme.

**Cosa ho verificato e va bene**
- `modules/web/leggi.py:990`, `_fine_script`: è una macchina a 3 stati.
  - Il rischio esaminato è uno scostamento dagli stati «script data escaped» e «double escaped» dello standard WHATWG.
  - Esito ok:
    - `<!-->` e `<!--->` riportano allo stato 0, perché la regex `<!(?=--)` consuma solo 2 caratteri e lascia trovare `-->`.
    - `<script` porta al doppio escape solo dallo stato 1.
    - `</script` nello stato 2 riporta allo stato 1.
    - Va bene anche con maiuscole e minuscole, e con `<scripts>`.
    - L'insieme dei delimitatori coincide con `_FINE_NOME`, quindi in `_chiusura` (`modules/web/leggi.py:1035`) il ciclo non riparte mai dallo stato 0.
  - 3000 ripetizioni di `<!--<script></script>` danno V come nel browser.
- `modules/web/leggi.py:907`: `interesting` viene sostituito con `_FineScriptTrovata`.
  - Il rischio esaminato è un uso di `interesting` da parte di html.parser diverso da `.search(rawdata, i)`.
  - Esito ok: ho letto html.parser di 3.11.17, 3.12.3 e 3.13.16. Lo usano solo con `.search(rawdata, i)` e `.start()`, e `clear_cdata_mode` lo ripristina.
  - `<script/>` è coperto, perché il controllo viene dopo `super()`.
  - Gli script dentro svg e in XHTML non passano in modalità testo grezzo (CDATA), quindi non vengono toccati.
  - `<p>x</p><script>abc</script  T99` e altri casi a fine pagina danno ok=True su 3.11, 3.12 e 3.13.
- `modules/web/leggi.py:890`, `parse_comment`: il rischio esaminato è una perdita o una fuga su 3.11. Esito ok, e su 3.13 non cambia niente.
- `modules/web/leggi.py:117` e `modules/web/leggi.py:1243`, rilevatore del parser e avviso nel log una sola volta: ok. Se due thread arrivano insieme può uscire un doppio warning, cosa cosmetica.
- Test: `tests/test_unit_web_leggi.py:1086` (doppio escape, parser e ripiego), `tests/test_unit_web_leggi.py:1111`, `tests/test_unit_web_leggi.py:1120`, `tests/test_unit_web_leggi.py:1143` e il marcatore `tests/test_unit_web_leggi.py:32`: ok. `tests/test_unit_web_leggi.py:1103` (XHTML) non contiene i casi del blocco.
- Suite web: 333 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.
- Mutazioni, in una copia isolata:
  - `interesting` non sostituito: 4 FAIL.
  - Ripiego senza `_fine_script`: 4 FAIL.
  - Override di `parse_comment` tolto: 1 FAIL su 3.11.

**Riserva da sistemare insieme al blocco: R-482-1 (BASSA)**
- La mutazione «posizione assoluta invece della distanza dalla fine» in `_FineScriptTrovata` passa tutta la suite (0 FAIL). Su `<p>x</p><script>abc</script  T99` produce l'AssertionError «interesting.search() lied». Il catch-all di `leggi_pagina` evita il crash, ma la pagina viene rifiutata. Va aggiunto un test con questo caso: è il bug che hai trovato col tuo fuzz.

**Cosa non ho verificato**
- Il comportamento sugli html.parser senza le patch del 2025: qui non c'è un Python vecchio. Mi fido del tuo plugin (314 passed, 9 skipped) e del controllo su `_PARSER_AGGIORNATO` che manda al ripiego prima di `feed`.
- La suite completa su 3.12: html.parser l'ho solo letto.
- I browser reali sui DOCTYPE XHTML: ho ragionato sullo standard XML (Firefox usa expat, Chrome libxml2). Non ho rifatto il tuo fuzz sugli script con lexbor né l'enumerazione a 4 atomi.
- Le pagine XHTML malformate in modo diverso (es. `<!doctype` minuscolo, per cui il browser dà errore e Gas mostra il resto) sono fuori da questa fetta.

**Memoria**: riga #482 più una lezione sul DOCTYPE XML, committate con `scripts/commit_memoria_revisore.sh` (commit 5dbbe9a). Il diff staged è rimasto intatto.

File utili:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev482/sonde.py (le sonde, da lanciare passando come argomento la radice del codice da provare)
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev482/cp/modules/web/leggi.py (la copia con il rimedio `_fine_doctype` provato)

### Review #483 (chat Mani) — verdetto integrale (diff staged della fetta 12, primo rimedio a B-482-1)

## VERDETTO: BOCCIATO

Review #483 (chat Mani), seconda review della #482 sul diff staged della fetta 12. Il DOCTYPE scritto correttamente ora è a posto, ma la nuova funzione apre altre 3 fughe che main 7af0c48 non aveva. Restano su DOCTYPE scritti male, cioè XML non valido.

**Motivo del blocco: B-483-1 (ALTA, fuga nuova rispetto a main)**
- `modules/web/leggi.py:1187`: `_fine_doctype` considera una virgoletta come inizio di un testo tra virgolette in qualsiasi punto del DOCTYPE. L'XML la ammette solo dopo SYSTEM o PUBLIC, oppure dentro una dichiarazione `<!…>` del sottoinsieme `[…]`. Una virgoletta fuori posto si chiude con la prossima uguale, anche dentro il corpo. Il DOCTYPE finisce così a un `>` o `]>` di uno script o di uno style, e il resto arriva al modello.
- Rischio esaminato: la fine del DOCTYPE spostata dentro il corpo. Esito: blocco.
- Sonde in XHTML (codice staged, Python 3.13):
  - `<!DOCTYPE x '><html xmlns=…><body><script>'>SEGRETO</script>V` → `SEGRETOV`
  - `<!DOCTYPE x [ ' ]>…<script>'</script><style>a[0]>1 SEGRETO</style>V` → `1 SEGRETOV`
  - `<!DOCTYPE x [ <!ENTITY e 'a'> " ]>…<script>"</script><style>a[0]>SEGRETO</style>V` → `SEGRETOV`
- Su main 7af0c48 tutti e tre nascondono SEGRETO: è una regressione. Il browser su questi XML non validi non mostra niente.
- Rimedio provato in una copia nella scratchpad (rev482/cp2), con la suite verde:
  - l'inizio del DOCTYPE va letto con una regex stretta: nome, poi niente, `SYSTEM "…"` oppure `PUBLIC "…" "…"`, poi `>` oppure `[`; qualsiasi altra cosa dà -1;
  - nel sottoinsieme le virgolette contano solo dentro `<!…>`;
  - nel sottoinsieme un `<` che non apre un commento, una PI (`<?…?>`) o un `<!` dà -1;
  - un `[` o un `]` dentro una dichiarazione dà -1.
  - Risultato: le 8 sonde nuove e le 7 della #482 non fanno uscire SEGRETO; il DOCTYPE PUBLIC standard tiene V. Su Python 3.13 e 3.11: 343 passed, 1 skipped.
- Servono test per le 3 sonde sopra.

**Cosa ho verificato e va bene**
- `modules/web/leggi.py:1187` resta lineare (rischio esaminato: tempi quadratici), esito ok. Ogni ricerca riparte da dove è arrivata la precedente. Un `]` non seguito da `>`, o un costrutto che non si chiude, danno -1 e il resto viene scartato.
- La parte di B-482-1 sui DOCTYPE scritti bene è chiusa: le 7 sonde della #482 non fanno uscire SEGRETO, e `<!ENTITY x "]>SEGRETO">` è nascosto, mentre su main usciva.
- `tests/test_unit_web_leggi.py:1128`: chiude R-482-1, il test che pinna la posizione «dalla fine» in `_FineScriptTrovata` (rischio esaminato: la stessa mutazione di prima ancora senza test). Esito ok: il codice staged lo passa; la mutazione «posizione assoluta» lo fa fallire (1 FAIL nella tua prova, che ho guardato ma non rifatto).
- `tests/test_unit_web_leggi.py:1120`: `test_xhtml_istruzioni_e_doctype`, esito ok per i casi presenti. Mancano le 3 sonde del blocco.
- Suite web: 343 passed, 1 skipped, sia su 3.13.16 sia su 3.11.17.
- Le parti già viste nella #482 (doppio escape degli script, `parse_comment`, rilevatore del parser, warning nel log) non sono cambiate e restano ok.

**Cosa non ho verificato**
- Come i browser veri (expat in Firefox, libxml2 in Chrome) mostrano questi DOCTYPE non validi: mi baso sullo standard XML, che li dichiara errore. Il rimedio scarta il resto, quindi sta dalla parte sicura in entrambi i casi.
- Il plugin del parser vecchio e la tua enumerazione con lexbor: non li ho rifatti. Il delta tocca solo la preparazione del testo XHTML.
- I tempi su pagine di più MB: mi fido della tua misura (0,12–0,43 s).

**Memoria**: aggiunte la riga #483 e una lezione (in un XML non valido non si «indovina» la fine: -1). Committate con `scripts/commit_memoria_revisore.sh`, commit 6e8872b. Lo stage dei due file non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev482/sonde483.py (le sonde; si lancia passando come argomento la radice del codice da provare)
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev482/fix483.py (lo script che applica il rimedio)
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev482/cp2/modules/web/leggi.py (la copia con il rimedio applicato)

### Review #484 (chat Mani) — verdetto integrale (diff staged finale della fetta 12)

## VERDETTO: APPROVATO

Review #484 (chat Mani), seconda review della #483 sul diff staged della fetta 12 (`modules/web/leggi.py` e `tests/test_unit_web_leggi.py`, 295 righe aggiunte e 11 tolte). Il blocco B-483-1 è chiuso e il codice è uguale al rimedio che avevo provato nella copia rev482/cp2.

**Cosa ho esaminato**
- `modules/web/leggi.py:1173`, `_TESTA_DOCTYPE`, l'inizio del DOCTYPE.
  - Cosa fa: accetta il nome, poi niente, `SYSTEM "…"` oppure `PUBLIC "…" "…"`, poi `>` o `[`. Qualsiasi altra cosa dà -1.
  - Rischi esaminati: una virgoletta fuori posto che sposta la fine nel corpo, e lentezza della regex.
  - Esito ok:
    - le 4 sonde di sonde483.py sui DOCTYPE non validi non mostrano niente;
    - i DOCTYPE validi tengono VIS;
    - 2 milioni di spazi si leggono in 0,02 s.
- `modules/web/leggi.py:1203`: nel sottoinsieme `[…]` le virgolette contano solo dentro una dichiarazione `<!…>`.
  - Rischio esaminato: B-483-1.
  - Esito ok: `[ ' ]>…<script>'</script><style>a[0]>1 SEGRETO` non fa uscire SEGRETO.
- `modules/web/leggi.py:1232`: un `[` o un `]` dentro una dichiarazione dà -1.
  - Rischio esaminato: una fine del DOCTYPE messa troppo avanti.
  - Esito ok. Ho tolto la condizione `or dichiarazione` in una copia isolata: la suite dà 1 FAIL, quindi la mutazione viene presa.
- Possibili perdite di testo visibile, provate con un sottoinsieme ben formato e realistico:
  - un riferimento `%p;` (parameter entity);
  - un'entità con `]>` tra virgolette;
  - un commento e una PI (`<?…?>`);
  - un ATTLIST con `"[x]"`.
  - Esito ok: VIS presente, SEGRETO assente.
  - `<!DOCTYPE html>` seguito da `<script>]>SEGRETO` resta nascosto.
- `tests/test_unit_web_leggi.py:1138`, `test_xhtml_istruzioni_e_doctype` con i casi nuovi. Rischio esaminato: test che non bloccano le regressioni. Esito ok, con suite e sonde:
  - suite web: 351 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17;
  - sonde483.py: 8/8 senza SEGRETO;
  - sonde.py della #482: 0 «parser: True».
  - 150 mila ENTITY si leggono in 0,12 s.

**Cosa non ho verificato**
- Come Firefox e Chrome trattano davvero questi DOCTYPE non validi: mi baso sullo standard XML, e la scelta -1 scarta il resto, quindi sta dalla parte sicura.
- Il plugin del parser vecchio (343 passed, 9 skipped), le altre 6 mutazioni di mut482/run3.py e l'enumerazione con lexbor: sono tue prove e non le ho rifatte.
- La suite su Python 3.12.

**Memoria**: aggiunta la riga #484, nessuna lezione nuova. Committata con `scripts/commit_memoria_revisore.sh`, commit d1fff5f. Lo stage dei due file non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev482/sonde483.py

### Review #485 (chat Mani) — verdetto integrale (delta per V-1 e V-2 del bot #252)

## VERDETTO: APPROVATO CON RISERVE

Review #485 (chat Mani), sul delta staged della PR #252 (head 3cea14e), che risponde al BOCCIATO del bot: V-1 MEDIA (`<script>` scritto dentro il DOCTYPE, SEGRETO dopo) e V-2 COSMETICA (avviso nel log non atomico). Il delta chiude V-1 e V-2 senza aprire fughe nuove. Resta un buco nei test (R-485-1).

**Cosa ho esaminato**
- `modules/web/leggi.py:1241` (regex `_DOPO_DOCTYPE`) e `modules/web/leggi.py:1270` (controllo del prologo in `_commenti_e_cdata_xml`).
  - Cosa fa: dopo un DOCTYPE, ogni pezzo tenuto può contenere solo spazi, oppure spazi seguiti da `<` e una lettera, che è l'inizio dell'elemento radice. Commenti e PI (`<?…?>`) sono ammessi; un CDATA fa break, e lo stesso controllo vale per la coda finale.
  - Rischio esaminato: SEGRETO che esce dopo il DOCTYPE, o testo valido perso.
  - Esito ok:
    - le 2 sonde del bot non fanno uscire SEGRETO;
    - nascondono il resto anche un secondo DOCTYPE con `<script>` nel letterale, un DOCTYPE scritto dopo la radice, `</x>` nel prologo e `SEGRETO` da solo dopo il DOCTYPE;
    - un prologo valido (`<?xml?>`, DOCTYPE, commento, PI, a capo, poi la radice) tiene V e il contenuto del CDATA nel corpo;
    - quando un `<lettera` è stato visto il prologo si chiude, quindi le pagine normali non pagano niente.
  - La regex usa `$` invece di `\Z`, ma qui sono equivalenti perché `[ \t\r\n]*` consuma già gli a capo.
- `modules/web/leggi.py:1319`, il lucchetto intorno al controllo e al segno dell'avviso (V-2).
  - Rischio esaminato: avviso scritto due volte, oppure blocco del lucchetto.
  - Esito ok: `primo` viene sempre assegnato e il warning si scrive fuori dal lucchetto.
- Suite web: 357 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.
- sonde483.py: 0 casi con SEGRETO. sonde.py della #482: 0 «parser: True».

**Riserva: R-485-1 (BASSA, test)**
- Ho cambiato in una copia isolata `_DOPO_DOCTYPE` in `[^<]*(?:(<[A-Za-z])|$)`, cioè testo ammesso prima di `<lettera`. Con questo cambio la suite resta tutta verde.
- Il motivo: in tutti i casi nuovi di `tests/test_unit_web_leggi.py:1129` SEGRETO è seguito da `</script>`, quindi il controllo cade comunque su `</`.
- Il codice staged nasconde `<!DOCTYPE x SYSTEM "<script>">SEGRETO<html xmlns=…><body><p>V</p>…`. Con il cambio SEGRETO esce, e su main esce già oggi (è la classe preesistente).
- Da fare: aggiungere quel caso, oppure `<!DOCTYPE html><!-- c -->SEGRETO<html…>`, a `test_xhtml_istruzioni_e_doctype`.

**Nota sulla classe preesistente «XHTML malformato letto come HTML»**
- Rientra anche il testo dopo la radice: `…</html>\nCODA` mostra CODA, mentre il browser si ferma al primo errore.
- Va nella stessa riserva che registri in stato_progetto.md; non è da correggere in questa PR.

**Cosa non ho verificato**
- Come Firefox (expat) e Chrome (libxml2) mostrano davvero un prologo non valido: mi baso sullo standard XML (nel prologo solo spazi, commenti e PI), e la scelta «break» toglie testo, quindi sta dalla parte sicura.
- Il plugin del parser vecchio, le tue mutazioni di run4.py e i tempi su 1,8–3 MB: sono tue prove e non le ho rifatte.
- La suite su Python 3.12.

**Memoria**: aggiunte la riga #485 e una lezione sui mutanti «testo prima della fine ammessa», committate con `scripts/commit_memoria_revisore.sh` (commit e5548a0). Lo stage dei due file non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev482/cp4/modules/web/leggi.py (la copia col mutante `[^<]*` che sopravvive)

### Review #486 (chat Mani) — verdetto integrale (test per R-485-1 e V-3 ve #252)

## VERDETTO: APPROVATO

Review #486 (chat Mani): rispetto alla #485 cambiano solo i test in stage. La riserva della #485 (R-485-1, il mutante `[^<]*` sul prologo che passava tutta la suite) è chiusa, e i mutanti segnalati in V-3 dalla verifica esterna #252 adesso vengono presi.

**Cosa ho esaminato**
- `modules/web/leggi.py:1241`: il codice in stage è identico a quello approvato nella #485. Il confronto con la mia copia cp4 differisce solo nella riga del mutante.
  - Rischio esaminato: una modifica del codice che passa come «solo test».
  - Esito ok.
- `tests/test_unit_web_leggi.py:1139` e la riga successiva: aggiungono i due casi «testo dopo il DOCTYPE, poi la radice» (`SYSTEM "<script>">SEGRETO<html…>` e `<!-- c -->SEGRETO<html…>`).
  - Rischio esaminato: il mutante `[^<]*` della #485 che sopravvive ancora.
  - Esito ok: rimesso il nuovo file di test nella copia mutata, il mutante dà 2 FAIL.
- `tests/test_unit_web_leggi.py:1087` e la riga prima: due casi nuovi sul doppio escape degli script.
  - Rischio esaminato: risultati attesi diversi da quelli del browser.
  - Esito ok. Ho seguito a mano gli stati dello standard WHATWG:
    - `<!--<script></script><script></script>SEGRETO</script>`: dal doppio escape `</script>` torna all'escape, non allo script normale, quindi SEGRETO resta nascosto e VIS esce.
    - `<!--<script><!--</script>SEGRETO</script>`: `<!--` dentro il doppio escape non cambia stato, quindi SEGRETO resta nascosto.
  - Entrambi i casi controllano anche il ripiego.
- I casi `[ > ]`, `[<!ENTITY a <!ENTITY b> ]` e `<!DOCTYPE>` vogliono che il resto della pagina sparisca. Sono coerenti con `_fine_doctype`, che per l'XML non valido restituisce -1.
- Suite web: 364 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Cosa non ho verificato**
- Le singole mutazioni di `scratchpad/mut482/run5.py` per V-3: ho rifatto solo il mio mutante `[^<]*`.
- La suite col parser vecchio (356 passed, 9 skipped) e quella su Python 3.12.
- Il merge di main 2abc23b: lo rivedo a parte come #487.

**Memoria**: aggiunta la riga #486, nessuna lezione nuova. Committata con `scripts/commit_memoria_revisore.sh` (commit 42077c0). Lo stage dei due file non è stato toccato.

File:
- /home/user/Gas/tests/test_unit_web_leggi.py
- /home/user/Gas/modules/web/leggi.py

### Review #487 (chat Mani) — verdetto integrale (merge di main 2abc23b)

## VERDETTO: APPROVATO

Review #487 (chat Mani): merge di origin/main 2abc23b (PR #251, chat Motore) in feat/mani-web-fetta12, ancora da committare. HEAD è f644a04, MERGE_HEAD è 2abc23b e la base comune è 7af0c48. Il merge non tocca il codice e non perde righe.

**Cosa ho esaminato**
- `.claude/agents/memoria_revisore.md:802`: l'unica riga che entra da main è la #482 della chat Motore.
  - Rischio esaminato: righe perse durante la risoluzione del conflitto.
  - Esito ok:
    - ho confrontato le righe del file in stage con HEAD e con MERGE_HEAD: 0 righe perse da ciascun lato, nessuna riga inventata, nessun marcatore di conflitto;
    - le tue righe #482–#486 (`.claude/agents/memoria_revisore.md:801` è la #486) sono intatte.
  - Nota: il numero #482 è stato usato da due chat (Motore e Mani). È la stessa collisione fra chat parallele già vista con la #476; non tocca il merge.
- `modules/web/leggi.py:1241` e `tests/test_unit_web_leggi.py:1139`.
  - Rischio esaminato: il merge che cambia il codice già approvato.
  - Esito ok:
    - `git diff --cached HEAD` su modules, tests, gas.py e brains è vuoto;
    - i due file in stage sono identici a HEAD, cioè al codice approvato in #484–#486;
    - da 7af0c48, main non ha toccato il motore.
- I report.
  - Rischio esaminato: una scelta di lato sbagliata nella risoluzione dei conflitti.
  - Esito ok:
    - `reports/roadmap.md` e `reports/coda_notte.md` sono uguali a main, ed è giusto perché il ramo non li toccava;
    - handoff, ultimo_report e diff_sessione sono uguali a HEAD (`--ours`): sono log di sessione che riscrivi a fine giro;
    - `reports/stato_progetto.md` è uguale a HEAD, e main non l'aveva modificato dalla base.

**Cosa non ho verificato**
- Non ho rilanciato la suite: il codice in stage è identico, byte per byte, a quello già provato nella #486 (364 passed su 3.13 e 3.11).
- Le parti delle versioni di main di handoff, ultimo_report e diff_sessione che vengono scartate: per regola sono fotografie di sessione e la storia resta in git.
- La CI sul commit di merge: non esiste ancora.

**Memoria**: la riga #487 è aggiunta in `.claude/agents/memoria_revisore.md` e messa in stage con `git add`, senza commit perché il merge è in corso. Finisce nel commit di merge. Nessuna lezione nuova. Il resto dello stage non è stato toccato.

File:
- /home/user/Gas/.claude/agents/memoria_revisore.md
- /home/user/Gas/reports/roadmap.md
- /home/user/Gas/reports/coda_notte.md

### Review #488 (chat Mani) — verdetto integrale (V-1 e V-2 della seconda verifica esterna #252, prima versione)

## VERDETTO: BOCCIATO

Review #488 (chat Mani): delta in stage sulla PR #252 (head 3c0be94) per la seconda verifica esterna #252. La fuga V-1 si riapre aggiungendo una sola lettera, quindi su XML non valido resta la regressione rispetto a main. V-2 invece è chiusa.

**Motivo del blocco: B-488-1 (BASSA come V-1, ma il fix non chiude il finding)**
- `modules/web/leggi.py:1244`: `_INIZIO_PI` controlla solo il primo carattere dopo `<?`. In XML però una PI (`<?…?>`) vuole il nome intero, seguito da uno spazio oppure da `?>`.
- Sonde sul codice in stage, in XHTML, tutte con SEGRETO visibile. Su main 7af0c48 tutte e 4 lo nascondono:
  - `<?x<!--?>SEGRETO`
  - `<?a<![CDATA[?>SEGRETO`
  - `<html…><body><p>V</p><?x<!--?><script>x</script>SEGRETO</body></html>`
  - `…<? <!--?>SEGRETO` (`[^\x00-\x7f]` accetta anche caratteri che non possono iniziare un nome XML)
- `modules/web/leggi.py:1282`, il break sulla PI non valida: il punto in cui si fa break è giusto, il problema è solo la regex.
- Rimedio provato in una copia isolata (rev482/cp5):
  - `_INIZIO_PI` controlla il nome XML intero, con gli intervalli NameStartChar e NameChar dello standard, e poi richiede uno spazio oppure `?>`.
  - Risultato su 10 sonde: le 5 con SEGRETO lo nascondono; tengono il testo `<?x <!--?>VISTO`, `<?x?>VISTO`, `<?xml-stylesheet href="a"?>VISTO` e un nome non ASCII valido (`<?é-1.· a?>`).
  - Suite: 369 passed e 1 skipped su 3.13 e 3.11.
- Servono test per `<?x<!--?>SEGRETO` e per il caso con ` `.

**Cosa ho verificato e va bene**
- `tests/test_unit_web_leggi.py:1089` e la riga dopo chiudono V-2 (`</scripts>` e `<scripts>` non sono il tag script).
  - Rischio esaminato: il mutante «niente lookahead» in `_SEGNI_SCRIPT` che sopravvive.
  - Esito ok: in una copia isolata il mutante dà 1 FAIL.
- `tests/test_unit_web_leggi.py:1153`, le sonde della verifica esterna. Esito ok per i casi presenti, ma tutti hanno `<!--` subito dopo `<?`, quindi non provano il nome seguito da caratteri non ammessi.
- Suite web sul codice in stage: 369 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Cosa non ho verificato**
- Come i browser veri trattano una PI senza nome valido: per lo standard XML è un errore, e la scelta break scarta il resto, quindi sta dalla parte sicura.
- La suite col parser vecchio (361 passed e 9 skipped).
- La mutazione «senza il controllo del nome della PI»: è nel tuo run6.py e non l'ho rifatta.
- V-3 è cosmetica e non viene toccata.

**Memoria**: aggiunte la riga #488 e una lezione (validare tutta la produzione XML, non solo il primo carattere), committate con `scripts/commit_memoria_revisore.sh` (commit 9293b9b). Lo stage dei due file non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev482/fix488.py (script che applica il rimedio)
- /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/rev482/cp5/modules/web/leggi.py (copia con il rimedio applicato)

### Review #489 (chat Mani) — verdetto integrale (V-1/V-2 della seconda verifica esterna #252, versione finale)

## VERDETTO: APPROVATO

Review #489 (chat Mani), ri-review della #488 sul delta in stage della PR #252 (head 3c0be94). B-488-1 è chiusa: `<?x<!--?>SEGRETO` e le altre sonde della #488 adesso restano nascoste, e le PI valide tengono il loro testo.

**Cosa ho esaminato**
- `modules/web/leggi.py:1247`, `_INIZIO_PI` (con `_INIZIALE_XML` a `modules/web/leggi.py:1245`).
  - Cosa fa: per aprire una PI (`<?…?>`) vuole il nome XML intero, poi uno spazio oppure `?>`.
  - Rischio esaminato: la nuova scrittura (stringhe raw con escape `\u` per `re`, caratteri singoli invece di intervalli di due) che cambia gli intervalli rispetto alla mia cp5.
  - Esito ok: ho confrontato le due regex su tutti i code point Unicode, sia come carattere iniziale sia come carattere interno al nome, e ho trovato 0 differenze.
- `modules/web/leggi.py:1286`, il break sulla PI non valida.
  - Rischio esaminato: una fuga o una perdita di testo.
  - Esito ok, sulle 10 sonde della #488:
    - le 5 con SEGRETO lo nascondono: `<?x<!--?>`, `<?a<![CDATA[?>`, `<? <!--?>`, `<?<!--?>` e il caso con lo script nel corpo;
    - tengono VISTO: `<?x <!--?>`, `<?x?>`, `<?xml-stylesheet href="a"?>` e `<?é-1.· a?>`;
    - in più ho provato `<?x\t<!--?>VISTO`, che tiene VISTO.
- `tests/test_unit_web_leggi.py:1154` e i casi vicini in `test_xhtml_istruzioni_e_doctype`.
  - Rischio esaminato: il mutante «controllo solo del primo carattere» che sopravvive.
  - Esito ok: il caso `<?x<!--?>SEGRETO` è il controesempio esatto per quel mutante. Secondo la tua prova (run7.py) il mutante dà 2 FAIL.
- Suite web: 375 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.
- sonde483.py e sonde.py della #482: 0 fughe.

**Cosa non ho verificato**
- Le mutazioni di run7.py: non le ho rifatte. Ho però controllato che il controesempio di ciascuna stia nei test.
- La suite col parser vecchio (367 passed e 9 skipped) e quella su Python 3.12.
- I tempi su pagine da 3 MB: mi fido della tua misura. La regex non torna indietro: legge il nome una volta sola e poi guarda un carattere.

**Memoria**: aggiunta la riga #489, nessuna lezione nuova. Committata con `scripts/commit_memoria_revisore.sh` (commit 2cf21e5). Lo stage dei due file non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 321 → 375 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «375 passed, 1 skipped» su Python 3.13 e 3.11; lo skip è il test d'allarme che gira solo in CI). Col html.parser non patchato di CPython 3.12.3 caricato da plugin: 367 passed, 9 skipped (i test che vogliono il parser).
- Oracolo lexbor, nuovo contro main 7af0c48: fuzz degli script (stati di escape) su 3.11 e 3.13, 0 fughe del nuovo contro 114–199 di main, 0 regressioni; enumerazione a 4 atomi (2,3 M pagine): 0 regressioni, 0 perdite nuove.
- Mutazioni in copie isolate, elencate: `_fine_script` (anche i due mutanti di V-3 ve), `_FineScriptTrovata`, `parse_comment`, `_fine_doctype` (virgolette, testa, testa assente, `<` libero, `<` e `]` in dichiarazione, `>` fuori dichiarazione, commenti, PI), prologo dopo il DOCTYPE (assente, `<` qualsiasi, `[^<]*`, CDATA, fine subito), nome della PI (assente, solo il primo carattere, iniziale qualsiasi), `_SEGNI_SCRIPT` senza lookahead: ognuna fa fallire almeno un test.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

- `3cea14e` (head all'apertura della PR #252): unit-suite e handoff-check success; verifica-bot **failure** (BOCCIATO, V-1 MEDIA, chiusa in `f644a04`); verifica esterna #252 BOCCIATO (V-1 MEDIA, V-2/V-3/V-4 BASSE, V-5/V-6 COSMETICHE: vedi §1).
- `3c0be94` (secondo giro): unit-suite, handoff-check e verifica-bot success; bot APPROVATO CON RISERVE (solo COSMETICHE); seconda verifica esterna #252 APPROVATO CON RISERVE (V-1 e V-2 BASSE, chiuse in `719d3ce`).
- `719d3ce` e il commit di fine-task con questo handoff: run non ancora disponibili alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Restano: **R-ve252-2** BASSA preesistente (XHTML malformato letto come HTML, da decidere), **R-ve246-5** MEDIA preesistente (canvas/object, decisione sul costruttore HTML5), R-469-1, R-ve245-2…5, R-456-2, R-447-1(b), R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…12».
