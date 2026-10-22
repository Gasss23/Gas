# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-22 — Chat Mani, fetta 12: script a doppio escape, DOCTYPE e PI in XHTML, parser vecchi (R6)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 12: solo con verdetto del bot APPROVATO puro sull'head finale e CI verde, oppure con il tuo ok.
2. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; chiuderla bene richiede un vero costruttore HTML5 (es. lexbor): decidi tu.
3. Sul Mac e sulla VPS, dalla cartella di Gas: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` deve dire True (se dice False Gas lo scrive ora anche in gas_debug.log).
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

---

## §1 SCOPE & ESITO FETTE

- **R-454-2**: `FATTA`
- **R-453-2** (con B-482-1 e B-483-1 ALTE): `FATTA`
- **V-2 ve #242**: `FATTA`
- **R-466-1, R-466-2, R-ve245b-4**: `FATTA`
- **R-482-1**: `FATTA`

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +
 modules/web/leggi.py               | 167 +++++++++++++++++++--
 reports/diff_sessione.md           |  10 +-
 reports/handoff.md                 | 298 +------------------------------------
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  27 ++--
 tests/test_unit_web_leggi.py       | 139 ++++++++++++++++-
 7 files changed, 321 insertions(+), 327 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
621da82 feat(web): fetta 12 — script a doppio escape, DOCTYPE e PI in XHTML, parser vecchi (R6)
d1fff5f chore(revisore): memoria review #484 — APPROVATO
6e8872b chore(revisore): memoria review #483 — BOCCIATO
5dbbe9a chore(revisore): memoria review #482 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; il §2 è preso dall'index con i report già in stage, quindi l'elenco dei file è esatto e i numeri dei report possono differire di poco.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Tre verdetti, incollati integralmente (chat Mani), tutti sul diff staged della fetta 12 poi committato in `621da82`: #482 (BOCCIATO, B-482-1) sulla prima versione, #483 (BOCCIATO, B-483-1) sul primo rimedio, #484 (APPROVATO) sulla versione finale. Le righe citate nelle review intermedie si riferiscono al diff di allora.

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

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 321 → 351 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «351 passed, 1 skipped» su Python 3.13 e 3.11; lo skip è il test d'allarme che gira solo in CI). Col html.parser non patchato di CPython 3.12.3 caricato da plugin: 343 passed, 9 skipped (i test che vogliono il parser).
- Oracolo lexbor, nuovo contro main 7af0c48: fuzz degli script (stati di escape) su 3.11 e 3.13, 0 fughe del nuovo contro 114–199 di main, 0 regressioni; enumerazione a 4 atomi (2,3 M pagine): 0 regressioni, 0 perdite nuove.
- Mutazioni in copie isolate: `_fine_script`, `_FineScriptTrovata`, `parse_comment`, `_fine_doctype` (virgolette, testa, `<` libero, `]` in dichiarazione, commenti, PI): ognuna fa fallire almeno un test.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

- Commit della fetta e commit di fine-task con questo handoff: run non ancora disponibili alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Restano: **R-ve246-5** MEDIA preesistente (canvas/object, decisione sul costruttore HTML5), R-469-1, R-ve245-2…5, R-456-2, R-447-1(b), R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…12».
