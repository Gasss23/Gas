# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-26 — Mani alla voce F4: «mergia N» / «no N» dall'operatore su Telegram (ramo `claude/mani-voce-f4`, contiene anche le PR #411, #412 e #414)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #411 (https://github.com/Gasss23/Gas/pull/411), F2-bis: tutta verde, verdetto del bot APPROVATO CON RISERVE (solo note basse): decide l'operatore.
2. Merge della PR #412 (https://github.com/Gasss23/Gas/pull/412), F3, dopo la #411: CI verde, bot neutral (tocca ci.yml), verdetto APPROVATO CON RISERVE: decide l'operatore.
3. Merge della PR #414 (https://github.com/Gasss23/Gas/pull/414), F3b, dopo la #412. Numero e URL dall'output di `gh api repos/Gasss23/Gas/pulls -X POST` (qui `gh pr` non c'è). Revisore #885-MV APPROVATO: con un verdetto del bot pulito mergia l'agente (CLAUDE.md §10), altrimenti l'operatore.
4. Merge della PR di F4 (ramo `claude/mani-voce-f4`), dopo la #414: revisore #889-MV APPROVATO CON RISERVE, quindi decide l'operatore.
5. Da confermare (oggi così): il merge NON vale a voce dal Mac, solo da Telegram; l'annullo a voce NON chiede conferma.
6. Sul Mac, dopo i merge: `GAS_RICHIESTE_AUTORI=<login GitHub di chi scrive gli esiti>` nel `.env`, poi riavvio del bot Telegram e del server voce.

---

## §1 SCOPE & ESITO FETTE

- **F2-bis (PR #411)**: `FATTA` — 887fcc0d, 93f7650f, 80d1e2b5; revisore #873-MV … #878-MV.
- **F3 (PR #412)**: `FATTA` — 6fce9e43, 9f4650d6; revisore #879-MV … #883-MV.
- **F3b — esiti a voce e annullo a voce**: `FATTA` — 28947ffc; revisore #884-MV → #885-MV APPROVATO.
- **F4 — «mergia N» / «no N»**: `FATTA` — 2863bf4c; revisore #888-MV → #889-MV APPROVATO CON RISERVE (chiude R-883MV-1).
- **F5 — esecutore nel cloud**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  27 +
 .github/workflows/ci.yml           |   8 +
 .gitignore                         |   6 +
 gas.py                             |  26 +-
 modules/sviluppo/cassetta.py       | 720 +++++++++++++++++++++++++++
 modules/sviluppo/esiti.py          | 151 ++++--
 modules/sviluppo/richieste.py      |  20 +-
 modules/telegram/bot.py            |  46 ++
 modules/voice/server.py            |  62 ++-
 reports/diff_sessione.md           |  21 +-
 reports/handoff.md                 | n/d
 reports/mani_voce_piano.md         |  78 ++-
 reports/stato_progetto.md          |   4 +-
 reports/ultimo_report.md           |  35 +-
 tests/test_unit_cassetta.py        | 989 +++++++++++++++++++++++++++++++++++++
 tests/test_unit_esiti.py           | 125 ++++-
 tests/test_unit_kernel.py          |  29 ++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
2863bf4c feat(sviluppo): mani alla voce F4 — «mergia N» / «no N» dall'operatore su Telegram, solo per la PR della domanda vera
a0a88e87 chore(revisore): memoria review #889 — APPROVATO CON RISERVE
e8ce313f chore(revisore): memoria review #888 — APPROVATO CON RISERVE
10bd0bd6 docs(fine-task): report e handoff dopo la correzione del bot sulla #414
0338ed09 fix(sviluppo): test di cassetta indipendenti dalla data, annullo con lo stesso ordine sul Mac e su Telegram, frase a voce salvata con lo stato (bot #414)
d99f9ad4 chore(revisore): memoria review #887 — APPROVATO
46422736 chore(revisore): memoria review #886 — APPROVATO CON RISERVE
8f6787a6 docs(fine-task): report e handoff — mani alla voce F3b (PR #414)
28947ffc feat(voce): mani alla voce F3b — esiti detti a voce (solo parti fisse), «annulla richiesta N» anche a voce
cb31b806 chore(revisore): memoria review #885 — APPROVATO
2edfc3fb chore(revisore): memoria review #884 — APPROVATO CON RISERVE
179cde04 docs(fine-task): report e handoff dopo la correzione della #412
9f4650d6 fix(sviluppo): stato scritto prima dell'invio, issue sparita non blocca, repo privato anche in lettura, domanda di merge solo da esiti più recenti (ve/bot #412)
5b2c904a chore(revisore): memoria review #883 — APPROVATO CON RISERVE
816716c7 chore(revisore): memoria review #882 — APPROVATO CON RISERVE
45f739d8 docs(fine-task): report e handoff — mani alla voce F3 (PR #412)
6fce9e43 feat(sviluppo): mani alla voce F3 — avviso subito alla richiesta, «annulla richiesta N», esiti dalle issue su Telegram
a518d9e5 chore(revisore): memoria review #881 — APPROVATO CON RISERVE
f692ce6d chore(revisore): memoria review #880 — BOCCIATO
020059f7 chore(revisore): memoria review #879 — APPROVATO CON RISERVE
5af3680e docs(fine-task): report e handoff dopo la correzione del bot (PR #411)
80d1e2b5 fix(sviluppo): propone_merge unica e fail-closed anche a mano, virgolette simili a «», niente parole di gravità nei testi (bot #411 su e6d30207)
02592fd1 chore(revisore): memoria review #878 — APPROVATO CON RISERVE
2f99753e chore(revisore): memoria review #877 — APPROVATO CON RISERVE
e6d30207 docs(fine-task): handoff — dichiarato l'invisibile reso come testo nel verdetto #876-MV (PR #411)
2ee37f96 docs(fine-task): report e handoff dopo la correzione della verifica esterna (PR #411)
93f7650f fix(sviluppo): ogni riga RISERVA conta, anche illeggibile o vuota (ve #411 V-1, R-875MV-1)
1382ec22 chore(revisore): memoria review #876 — APPROVATO
89e57942 chore(revisore): memoria review #875 — APPROVATO CON RISERVE
e01e0c55 docs(fine-task): report e handoff — mani alla voce F2-bis (PR #411)
40decd9b docs(mani-voce): decisioni dell'operatore del 26/11 nel piano; F1 rifiutata e compensazioni (avviso subito, annullo con 30 minuti, tetto di 2 al giorno)
887fcc0d fix(sviluppo): riserve basse di F2 chiuse prima di F3 (mani alla voce F2-bis)
a853b27f chore(revisore): memoria review #874 — APPROVATO
03d3f4c3 chore(revisore): memoria review #873 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore 887fcc0d: verdetti integrali #873-MV (primo giro) e #874-MV (secondo giro, dopo la correzione di R-873MV-2 nello stesso diff staged). Commit motore 93f7650f (dopo la verifica esterna #411 V-1): verdetti #875-MV e #876-MV, in fondo a questa sezione. Commit motore 80d1e2b5 (dopo il bot su e6d30207): verdetti #877-MV e #878-MV, dopo #876-MV. Commit motore 6fce9e43 (F3): verdetti #879-MV, #880-MV (BOCCIATO) e #881-MV, in fondo a questa sezione. Commit motore 9f4650d6 (dopo verifica esterna e bot sulla #412): verdetti #882-MV e #883-MV, dopo #881-MV. Commit motore 28947ffc (F3b): verdetti #884-MV e #885-MV, dopo #883-MV. Commit motore 0338ed09 (dopo il bot sulla #414): verdetti #886-MV e #887-MV, dopo #885-MV. Commit motore 2863bf4c (F4): verdetti #888-MV (primo giro) e #889-MV (secondo giro, dopo la correzione di R-888MV-1/2 nello stesso diff staged), in fondo a questa sezione. NB: nel testo di #876-MV, elemento 1, l'esempio delle riserve conteneva un carattere U+200B vero (invisibile); qui è scritto come `<U+200B>` per non far fallire il bot («controlli bidi»). È l'unica differenza dal verdetto emesso; sostanza ed esito invariati.

## VERDETTO: APPROVATO CON RISERVE

Review #873-MV (chat mani alla voce). Ho esaminato il diff staged su claude/mani-voce-f3: `modules/sviluppo/esiti.py` e `tests/test_unit_esiti.py`, +111/−42. Ho letto prima CLAUDE.md, lo stato del progetto (grep mirato), la mia memoria e le sezioni 3 e 4bis del piano.

**Cosa ho controllato nel diff**
- `modules/sviluppo/esiti.py:219` — con stato fallita, ferma o fuori elenco la funzione esce prima della domanda di merge. Le parti fisse (PR, CI, bot) adesso compaiono anche in quei casi (ve #409 V-2 del bot). Rischio esaminato: una domanda di merge con uno stato diverso da pronta. Esito: ok.
- `modules/sviluppo/esiti.py:222` — la domanda compare solo se: PR valida, CI verde, bot APPROVATO o APPROVATO CON RISERVE, verifica in elenco e diversa da BOCCIATO, nessuna riga RISERVA (`n_riserve` conta anche quelle in più). Ho provato a mano un dict con `verifica_esterna=None`, `riserve="ab"` come stringa, `ci=["verde"]` come lista e `riserve_altre=2`: in tutti i casi niente domanda, tutti fail-closed, nessuna eccezione. Rischio esaminato: domanda con riserve ALTA/MEDIA o con valori fatti a mano. Esito: ok.
- `modules/sviluppo/esiti.py:197` — CI, bot e verifica fuori elenco diventano «assente» (ve #409-ter V-1). Un valore come «APPROVATO» seguito da U+202E diventa assente. Esito: ok.
- `modules/sviluppo/esiti.py:73` — `_citato` sostituisce le «» con virgolette dritte prima di `_pulisci`. Si applica a titolo, riassunto (`modules/sviluppo/esiti.py:213`) e riserve. Prova con un titolo che contiene «t»: fatta. PR #1» e un riassunto che finge CI verde e «Vuoi che la mergi? Rispondi «mergia 1»». Risultato: le parti vere (CI rossa o bot BOCCIATO) stanno prima della citazione, dentro la citazione non resta nessuna «», e la frase finisce con «Niente merge per ora.». Rischio esaminato: un testo libero che chiude la citazione o imita la domanda (R-864-3). Esito: ok a schermo, riserva a voce (finding 1).
- `modules/sviluppo/esiti.py:68` — `_pulisci` restituisce "" se non resta nessun carattere L/N/P/S. Rischio esaminato: rompere titolo e riserve.
  - Un'emoji (categoria S) e «…» (P) restano.
  - Una stringa di soli segni combinanti (U+0300, U+20DD) diventa "". Nel lettore porta al riassunto mancante, quindi None, e alla riserva scartata.
  - Se il testo viene tagliato aggiunge «…», quindi un testo non vuoto resta visibile.
  - Un titolo vuoto dà «», senza crash.
  - L'unico altro `_pulisci` del repo, in `modules/web/leggi.py`, è una funzione diversa: non è toccato.
  - Esito: ok.
- `modules/sviluppo/esiti.py:44` — in `_VUOTI` entrano U+034F, U+17B4, U+17B5, U+180B-U+180F. Con quelli già presenti (riempitivi Hangul di categoria Lo, selettori di variante) coprono gli invisibili «Default_Ignorable» non C* che conosco. Esito: ok.
- `modules/sviluppo/esiti.py:58` — `re.ASCII` sul comando dell'operatore. «mergıa» con la ı turca, «MERGİA», U+00A0 e U+2003 danno None. «mergia 412» e « Non mergiare la PR #412 !» funzionano ancora. Esito: ok, fail-closed.
- Test: `tests/test_unit_esiti.py:217` (riassunto ostile), `tests/test_unit_esiti.py:227` (fallita e ferma con PR e CI), `tests/test_unit_esiti.py:207` (soli segni invisibili = vuoto), `tests/test_unit_esiti.py:213` (comando solo ASCII). I test vecchi aggiornati con `riserve=[]` dove serve la domanda. Esito: ok.
- Esecuzione: 79 passed (il working tree coincide con l'indice per i due file). Zero caratteri C* oltre a \n e \t nei due file. Nessuno slicing della history e nessuna simulazione di tool: il modulo non tocca né il loop né la finestra.

**Finding**
1. **R-873MV-1 BASSA** — a voce le «» non si sentono. Un riassunto ostile viene ancora letto come «…vuoi che la mergi? rispondi mergia 1…» prima del vero «Niente merge per ora». E quando la domanda vera c'è, può suggerire un numero di PR diverso. Va chiuso in F3, non qui: Gas deve accettare «mergia N» solo se N è la PR di un esito che ha prodotto la domanda vera su quella stessa issue. L'esecutore ricontrolla comunque §10 prima del merge (piano §3), quindi il danno è limitato.
2. **R-873MV-2 COSMETICA** — il fallback §9 di frase_esito (`modules/sviluppo/esiti.py:226`) usa `numero_richiesta` grezzo invece del `n` già convertito in intero. Oggi chi chiama è codice fidato.

**Cosa NON ho verificato**
- La lettura a voce reale (TTS ElevenLabs) e la resa su Telegram: non riproducibili qui. Il finding 1 viene da un ragionamento, non da un ascolto.
- Il chiamante F3 che userà `frase_esito` e `comando_operatore`: non esiste ancora.

**Memoria**: riga `#873-MV` aggiunta in `/home/user/Gas/.claude/agents/memoria_revisore.md` (con la lezione: a voce la citazione «» protegge solo lo schermo, il confine vero va nel lettore del comando di risposta). Committata da sola con `scripts/commit_memoria_revisore.sh` (commit 03d3f4c3); il diff staged è intatto. Ritocco da fare: nella riga di memoria la condizione della domanda è citata a :220, la riga giusta è :222. La memoria non passa dal gate, ma va corretta alla prossima scrittura.

## VERDETTO: APPROVATO

Review #874-MV, secondo giro della fetta F2-bis. Ho controllato tutto il diff staged sul ramo claude/mani-voce-f3: `modules/sviluppo/esiti.py` e `tests/test_unit_esiti.py`, +114/−43. Rispetto alla #873-MV è cambiato solo il ripiego di emergenza (§9) di `frase_esito`.

**Cosa ho controllato nel diff**
- `modules/sviluppo/esiti.py:225` — il ripiego §9 adesso mostra il numero solo se è un intero, altrimenti 0. Rischio esaminato: un valore grezzo nel testo per l'operatore (era R-873MV-2). Prova a mano: con `"<b>x"` e esito None esce «Richiesta di sviluppo #0: c'è un esito, guardalo sulla issue.», senza eccezioni. Esito: ok, R-873MV-2 chiusa.
- `modules/sviluppo/esiti.py:222` — la condizione della domanda di merge non è cambiata dalla #873-MV: PR valida, CI verde, bot ok, verifica in elenco e diversa da BOCCIATO, zero riserve. Rischio esaminato: una regressione nel nuovo giro. Esito: ok.
- `modules/sviluppo/esiti.py:73` — `_citato` e `_pulisci` (`modules/sviluppo/esiti.py:68`) sono invariati. Restano valide le prove della #873-MV con titolo e riassunto ostili: nessuna «» chiudibile dal testo libero, e senza tutte le condizioni la frase finisce con «Niente merge per ora.». Esito: ok.
- `tests/test_unit_esiti.py:217` e `tests/test_unit_esiti.py:227` — invariati. 79 passed. I due file non contengono caratteri C* oltre a \n e \t. Esito: ok.

**Note**
- COSMETICA, non bloccante: siccome `isinstance(True, int)` è vero, con `numero_richiesta=True` il ripiego stampa «#True». Il chiamante è codice fidato.
- R-873MV-1 BASSA resta aperta per F3. A voce le «» non si sentono, quindi un riassunto ostile può ancora farsi sentire come una domanda di merge. In F3 Gas deve accettare «mergia N» solo se N è la PR di un esito con la domanda vera sulla stessa issue.

**Cosa NON ho verificato**
- La lettura a voce reale (sintesi ElevenLabs) e la resa su Telegram: qui non si riproducono.
- Il chiamante F3: non esiste ancora.

**Memoria**: corretto nella riga #873-MV il riferimento da `:220` a `:222`. Aggiunta la riga #874-MV in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committata da sola con `scripts/commit_memoria_revisore.sh` (commit a853b27f). Il diff staged è intatto.

## VERDETTO: APPROVATO CON RISERVE

Review #875-MV. È il 3° giro della F2-bis dopo la verifica esterna sulla #411 (V-1). Diff staged sul ramo claude/mani-voce-f3: modules/sviluppo/esiti.py e tests/test_unit_esiti.py, +21/−2. Prima della review ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md (voce «Mani alla voce», riga 394) e la memoria del revisore.

**Elementi del diff esaminati**
- modules/sviluppo/esiti.py:111 — `elif pulita or valore:` conta in riserve_altre una riga RISERVA che non è vuota ma diventa vuota dopo la pulizia. Rischi esaminati: fail-open, doppio conteggio con le riserve oltre RISERVE_MAX, crash. Esito **ok**: la riga illeggibile non entra nella lista ma alza n_riserve, e frase_esito risponde «Niente merge per ora». Il ramo oltre RISERVE_MAX non cambia, l'eccezione resta catturata dal §9 alla riga 148. Rispetta il principio «robustezza prima di tutto»: nel dubbio, si ferma.
- tests/test_unit_esiti.py:244 — test parametrizzato su U+200B, U+0300 doppio e U+3164. Verifica `riserve == []`, `riserve_altre == 1`, nessun «mergia» e la frase «riserve ALTA/MEDIA: 1». Esito **ok**.
- tests/test_unit_esiti.py:253 — una riga «RISERVA:» vuota non conta e il merge viene proposto. Esito **riserva**: vedi R-875MV-1.
- tests/test_unit_esiti.py:167 — il test esistente passa da `riserve_altre == 2` a `== 3`. L'aggiornamento è coerente con la nuova regola. Esito **ok**.

**Caccia ad altri casi fail-open (richiesta del chiamante)**
- ESITO, PR, CI, BOT e VERIFICA_ESTERNA accettano solo valori fissi, quindi un valore illeggibile fa scartare tutto il commento (None). Provato a mano con VERIFICA_ESTERNA fatta solo di U+200B: risultato None. **Chiude bene.**
- Un RIASSUNTO illeggibile diventa vuoto dopo la pulizia, e la riga 143 scarta il commento (None). Provato a mano. **Chiude bene.**
- **R-875MV-1 BASSA (residuo della stessa classe)**: alla riga 103 c'è `valore = m.group(2).strip()`, e lo strip() di Python toglie anche gli spazi Unicode.
  - Quindi una riga RISERVA seguita solo da U+00A0, U+3000, U+2003, \x0b o U+2028 arriva come stringa vuota: non conta, e frase_esito propone il merge. Provato a mano: `riserve_altre=0` e «mergia» presente in tutti e cinque i casi.
  - È coerente con la scelta «RISERVA: vuota non conta», ma è la scelta stessa a essere fail-open: scrivi_esito non scrive mai una RISERVA vuota (filtra prima), quindi una riga RISERVA vuota in un commento vuol dire qualcosa di anomalo.
  - Contraddice anche la docstring di frase_esito («NESSUNA riga RISERVA»).
  - Proposta: contare OGNI riga RISERVA, anche vuota (`else:` al posto di `elif pulita or valore:`), e invertire il test alla riga 253. Impatto basso: il merge vero lo decide comunque CLAUDE.md §10, con il bot e la CI.
- Le righe fuori formato (minuscole, «RISERVA :») non corrispondono a `_RIGA`, quindi il commento viene scartato (None). **Chiude bene.**

**Verifiche eseguite**: 83 passed su tests/test_unit_esiti.py; zero caratteri di categoria C* (esclusi \n e \t) nei due file; prove a mano sui casi elencati sopra.

**Rischio escluso**: non ho verificato il comportamento in F3, cioè il lettore dei commenti della issue con il controllo dell'autore e il comando «mergia N». Non esiste ancora; R-873MV-1 resta aperta per quella fetta.

**Memoria**: aggiunta la riga #875-MV, con la riserva e una lezione (guardare cosa toglie lo strip() prima del controllo «vuoto»). Committata da sola con scripts/commit_memoria_revisore.sh (commit 89e57942); il diff staged sotto review è rimasto intatto. File: /home/user/Gas/.claude/agents/memoria_revisore.md

R-875MV-1 va registrata in /home/user/Gas/reports/stato_progetto.md (voce «Mani alla voce»), oppure chiusa subito con la modifica di una riga indicata sopra e una nuova review.

## VERDETTO: APPROVATO

Review #876-MV. È il 4° giro della F2-bis sul ramo claude/mani-voce-f3 (PR #411). Il diff staged completo tocca modules/sviluppo/esiti.py e tests/test_unit_esiti.py, +23/−2. Questo verdetto sostituisce #875-MV (APPROVATO CON RISERVE): R-875MV-1 è chiusa.

**Finding:** nessuno.

**Elementi del diff esaminati**
1. modules/sviluppo/esiti.py:111 — `else:` al posto di `elif pulita:`: ogni riga RISERVA che non entra nella lista conta in riserve_altre, che sia piena oltre RISERVE_MAX, illeggibile, vuota o fatta solo di spazi Unicode tolti dallo strip(). Rischi esaminati: fail-open, falso blocco di un commento valido, crash. Esito **ok**.
   - Fail-open chiuso: n_riserve > 0, quindi frase_esito risponde «Niente merge per ora».
   - Nessun falso blocco: scrivi_esito scarta le riserve che diventano vuote dopo la pulizia, quindi non scrive mai una RISERVA vuota. Provato a mano: con riserve `['<U+200B>', '  ']` il commento ha 0 righe RISERVA e il merge viene proposto.
   - Nessun crash: resta il §9 alla riga 148.
   - Ora è vera la docstring di frase_esito alla riga 188 («NESSUNA riga RISERVA»).
2. tests/test_unit_esiti.py:253 — test parametrizzato su "", U+00A0, U+3000, U+2003, \x0b e U+2028. Per ognuno verifica `riserve_altre == 1` e che non ci sia «mergia». Copre proprio i casi della riserva #875-MV, provati a mano in quella review. Esito **ok**.
3. tests/test_unit_esiti.py:243 — test parametrizzato su U+200B, U+0300 doppio e U+3164: riga illeggibile contata, domanda di merge bloccata. Esito **ok**.
4. tests/test_unit_esiti.py:167 — il test esistente passa da `riserve_altre == 2` a `== 3`, coerente con la nuova regola. Esito **ok**.

**Altre chiavi (già verificate in #875-MV, codice invariato)**
- ESITO, PR, CI, BOT e VERIFICA_ESTERNA accettano solo valori fissi: un valore illeggibile fa scartare tutto il commento (None).
- Un RIASSUNTO illeggibile diventa vuoto e la riga 143 scarta il commento (None).
- Le righe fuori formato non corrispondono a `_RIGA` e il commento viene scartato (None).
- Non resta nessun caso fail-open noto in leggi_esito.

**Verifiche eseguite:** 88 passed su tests/test_unit_esiti.py; 0 caratteri di categoria C* (esclusi \n e \t) nei due file. Nessun antipattern della sezione 5 di CLAUDE.md: niente history né tool toccati.

**Rischio escluso:** non ho verificato il comportamento in F3, cioè il lettore dei commenti della issue con il controllo dell'autore e il comando «mergia N». Non esiste ancora; R-873MV-1 resta aperta per quella fetta.

**Memoria:** aggiunta la riga #876-MV (nessuna lezione nuova), committata da sola con scripts/commit_memoria_revisore.sh (commit 1382ec22). La memoria di #875-MV era già nel commit 89e57942. Il diff staged è rimasto intatto (esiti.py e il test ancora in staging). File: /home/user/Gas/.claude/agents/memoria_revisore.md

In /home/user/Gas/reports/stato_progetto.md (riga 394) R-875MV-1 va segnata come chiusa e la review aggiornata a #876-MV APPROVATO.

## VERDETTO: APPROVATO CON RISERVE

Review #877-MV. È il 5° giro di F2-bis, sul diff staged in /home/user/Gas-411, ramo claude/mani-voce-f3, PR #411. Il diff tocca modules/sviluppo/esiti.py e tests/test_unit_esiti.py (+89/−17). Prima della review ho letto CLAUDE.md sez. 5, reports/stato_progetto.md (in modo mirato) e la memoria del revisore.

Ho confermato il falso rosso: nel verdetto del bot su e6d30207 l'unica parola di gravità bloccante sta dentro V-1, che è BASSA. Lì il bot cita tra virgolette la vecchia asserzione del test. Gli altri finding sono V-2 BASSA, V-3 e V-4 COSMETICHE.

Elementi del diff esaminati:
1. modules/sviluppo/esiti.py:244 — `propone_merge` è la regola unica della domanda di merge. Rischio esaminato: che la frase e la regola non vadano d'accordo sui dizionari fatti a mano. Ho fatto una prova a mano su 14580 combinazioni (riserve None/[]/()/""/["a"]/["U+200B"]/"ab"/{}/[None], riserve_altre assente/0/None/1/True/False/"0"/0.0/-1, verifica, pr, ci, esito): 0 casi in cui la frase chiede il merge e la funzione dice di no, o il contrario. Ogni eccezione dà False. — ok
2. modules/sviluppo/esiti.py:218 — ora conta tutti gli elementi di riserve, anche quelli illeggibili; una riserva che non è una lista vale come un elemento. Rischio esaminato: falsi blocchi sul percorso normale. leggi_esito con zero riserve continua a proporre il merge (lo verifica il test a tests/test_unit_esiti.py:278). Una tupla vuota o una stringa vuota toglie la domanda senza contare riserve: è prudente. — ok
3. modules/sviluppo/esiti.py:235 — frase_esito ora chiama propone_merge al posto della vecchia condizione scritta dentro la funzione. Rischio esaminato: perdere il controllo che la verifica esterna sia in elenco. Il controllo è stato spostato a riga 263 e nei dintorni (verifica in VERIFICA e diversa da BOCCIATO), e il ripiego §9 non è cambiato. — ok
4. modules/sviluppo/esiti.py:74 — la tabella che sostituisce le virgolette simili a «» (≪≫ 《》 〈〉 ‹› ⟨⟩ ⟪⟫, comprese U+2329/U+232A). Rischio esaminato: virgolette simili che restano fuori. Restano fuori ︽︾ (U+FE3D/FE3E), ⸨⸩ e << >> in ASCII (provato a mano). Non c'è nessuna normalizzazione NFKC che le trasformi dopo. — riserva cosmetica (R-877MV-2)
5. modules/sviluppo/esiti.py:42 — commento su U+180E. Ho verificato con unicodedata: U+180B-U+180D e U+180F sono Mn, U+180E è Cf. — ok (riga oltre i 100 caratteri, cosmetico)
6. tests/test_unit_esiti.py:273 e tests/test_unit_esiti.py:290 — test parametrizzati per bot #411 V-1 e V-2. Coprono gli stessi casi descritti dal bot. — ok
7. tests/test_unit_esiti.py:241 — il test che prima diceva che una riserva illeggibile non conta ora dice che conta come 1, in linea con il lettore. — ok

Riserve:
- R-877MV-1 BASSA: la fixture a tests/test_unit_esiti.py:14 contiene ancora una parola di gravità media scritta in maiuscolo, nel testo della riserva d'esempio «V-1 …». Se il bot la cita, il classificatore può dare di nuovo un falso rosso. Il punto debole vero è in scripts/bot_esito.py, funzione `_gravita_nel_testo`, che legge le parole di gravità anche dentro citazioni lunghe. È fuori da questo diff e fa parte della macchina del bot, quindi decide l'operatore. Va tracciata in stato_progetto.md.
- R-877MV-2 COSMETICA: l'elenco delle virgolette simili non le copre tutte (vedi punto 4). Il confine vero resta il lettore del comando in F3, come previsto da R-873MV-1, che resta aperta.

Wall of Shame: nessuno slicing della history e nessuna simulazione dei tool. Il diff non tocca il kernel, il cap di 10 iterazioni, il cap di 8k né `_get_window`. Il §9 è rispettato: propone_merge non lancia mai eccezioni.

Verifiche fatte: 101 passed su una copia dell'indice staged (checkout-index nella scratchpad); 0 caratteri C* (esclusi a capo e tab) nei due file.

Cosa non ho verificato: non ho rilanciato il bot né eseguito scripts/bot_esito.py sul nuovo testo, quindi non so se il prossimo giro del bot sarà verde. Ho solo letto il codice del classificatore, non l'ho cambiato né provato. Non ho eseguito la suite completa né la CI, solo tests/test_unit_esiti.py.

Memoria: ho aggiunto la riga #877-MV con la lezione (nel codice e nei testi che il bot cita, evitare le parole di gravità in maiuscolo) a /home/user/Gas-411/.claude/agents/memoria_revisore.md e l'ho committata (2f99753e). Il diff staged è rimasto com'era.

## VERDETTO: APPROVATO CON RISERVE

Review #878-MV, verdetto finale sul diff staged completo in /home/user/Gas-411 (ramo claude/mani-voce-f3, PR #411): modules/sviluppo/esiti.py e tests/test_unit_esiti.py, +91/−19. R-877MV-1 è chiusa. Resta una sola riserva, cosmetica.

Elementi del diff esaminati:
1. tests/test_unit_esiti.py:14 — la riserva d'esempio della fixture ora è «V-1 manca un test». Rischio esaminato: che il bot la citi e il classificatore dia di nuovo un falso rosso. Ho cercato con grep le parole di gravità in maiuscolo (le quattro del vocabolario e le varianti inglesi) in tests/test_unit_esiti.py e in modules/sviluppo/esiti.py: nessuna. — ok
2. tests/test_unit_esiti.py:22 e tests/test_unit_esiti.py:30 — l'andata e ritorno e la frase usano lo stesso testo nuovo, e l'asserzione dice «riserve aperte: 1». Rischio esaminato: un test rimasto disallineato. Passano tutti e 101. — ok
3. modules/sviluppo/esiti.py:244 — propone_merge, la regola unica della domanda di merge. Rispetto a #877-MV, dove ho trovato 0 differenze tra frase e regola su 14580 dizionari fatti a mano, la parte di esiti.py non è cambiata. Rischio esaminato: una regressione nascosta in staging. Il diff è identico, tocca solo il test. — ok
4. modules/sviluppo/esiti.py:74 — la tabella delle virgolette simili a «». — riserva cosmetica (sotto)

Riserve:
- R-877MV-2 COSMETICA (resta aperta, da scrivere in stato_progetto.md): l'elenco delle virgolette simili non le copre tutte. Passano ancora ︽︾ (U+FE3D/FE3E), ⸨⸩ e << >> in ASCII. Il confine vero resta il lettore del comando in F3, insieme a R-873MV-1.
- Fuori dal diff: la fragilità vera è nel classificatore del bot (scripts/bot_esito.py, `_gravita_nel_testo`), che legge le parole di gravità anche dentro le citazioni lunghe. È la macchina del bot, quindi decide l'operatore.

Wall of Shame: nessuno slicing della history e nessuna simulazione dei tool. Il diff non tocca kernel, cap delle iterazioni, cap di 8k, `_get_window` né guardrail. Il §9 è rispettato.

Verifiche: 101 passed su una copia dell'indice staged; 0 caratteri invisibili o di controllo (esclusi a capo e tab) nei due file.

Cosa non ho verificato: non ho eseguito il classificatore del bot sul nuovo head, quindi non so se il prossimo giro del bot sarà verde. Ho eseguito solo tests/test_unit_esiti.py, non la suite completa né la CI.

Memoria: ho aggiunto la riga #878-MV a /home/user/Gas-411/.claude/agents/memoria_revisore.md e l'ho committata (02592fd1). Il diff staged è rimasto com'era.

## VERDETTO: APPROVATO CON RISERVE

Review #879-MV. Ho guardato il diff staged su claude/mani-voce-f3-avvisi: 7 file, +823/−4. Ho letto prima CLAUDE.md (§5, §8, §9), reports/stato_progetto.md, la memoria del revisore e reports/mani_voce_piano.md (§3, §4bis, riga F3).

Elementi del diff esaminati:
- gas.py:5264 — `_avvisa_richiesta_accodata` manda l'avviso con `invia_notifica`, fuori dal tetto di avvisa_operatore. Controllato: eccezioni, flag della voce, numero di avvisi. Esito ok: ogni eccezione finisce in un warning e torna False, il flag `_turno_voce` viene letto con getattr, e gli avvisi sono limitati da GAS_RICHIESTE_MAX_GIORNO (20 al giorno). Il collegamento è a gas.py:5494.
- modules/sviluppo/richieste.py:186 — chiama `avvisa` dopo che la issue esiste. Se l'avviso fallisce, la richiesta resta creata e il testo lo dice al modello; un'eccezione nella callback viene presa sul posto. Se manca l'etichetta (successo parziale) non parte nessun avviso, ed è giusto: l'esecutore quella issue non la vede. Esito ok.
- modules/telegram/bot.py:979 — «annulla richiesta N» viene intercettato prima del modello. Viene dopo il controllo della chat ammessa e dopo i comandi giro e clear, vale solo da un messaggio nuovo, e un vocale non lo raggiunge (passa da `_gestisci_parlato`). Esito ok. Nota minore: ogni testo ora importa `cassetta`, quindi se quell'import si rompe tutti i messaggi di testo vengono ignorati, senza crash (è lo stesso schema dell'import di `brains.router` subito sotto).
- modules/telegram/bot.py:594 e modules/telegram/bot.py:626 — il loop chiama il controllo una volta al minuto, protetto da try/except. Esito ok.
- modules/sviluppo/cassetta.py:346 — il thread demone ha try/finally e rimette `in_corso` a False; la partenza è protetta e il cronometro viene toccato solo dal thread principale. Le chiamate GitHub hanno un timeout (TIMEOUT_SEC), quindi il thread non può restare appeso. Esito ok.
- Guardia T78p, valutazione richiesta: secondo me rispetta lo scopo della guardia, non la aggira. La guardia serve a gestire «un click alla volta» update e firme; il thread non vede update, firme né kernel, e invia solo tramite `invia_notifica`, che passa da `_invia_a_tutti`, il pool già ammesso dalla guardia. T78p PASS.
- modules/sviluppo/cassetta.py:268 — sicurezza in caso di errore su autori, issue e formato. Elenco autori vuoto: non legge niente (modules/sviluppo/cassetta.py:227). Login con regex, confronto in minuscolo. Commenti di issue non da-gas o di PR vengono scartati e scritti nel log. Esito ok, salvo R-879MV-3.
- modules/sviluppo/cassetta.py:119 — `annulla`: numero tra 1 e PR_MAX (bool escluso), repo privato, solo issue con da-gas e non PR, issue già chiusa trattata a parte; se l'etichetta c'è ma la chiusura fallisce, il testo dice il vero. Esito ok.
- Token: un `controlla_esiti` vero con il token "tok-SEGRETO" non lo scrive mai in gas_debug.log (provato). L'unico `%s e` nuovo, in bot.py:626, riceve un'eccezione che non contiene mai il token. Esito ok.
- Lunghezza: il caso peggiore di `frase_esito` (titolo, riassunto e 5 riserve tutte di emoji) vale 3980 unità UTF-16 contro un limite di 4096. Quindi «testo oltre il limite» non può bloccare la coda per sempre. Esito ok, ma il margine è stretto e nessun test lo fissa.
- tests/test_unit_kernel.py:11697 — T100c e T100d fanno il giro completo (§7) con avviso riuscito e fallito. Esito ok.

Test eseguiti su una copia dell'indice:
- cassetta, esiti e richieste: 177 passed. La suite cassetta ne conta 51, non 53.
- tests/test_unit_kernel.py: 1210 PASS, 0 FAIL (T78p, T100c e T100d PASS).
- Caratteri invisibili veri: 0 nei 5 file toccati.

Finding:
1. R-879MV-1 BASSA: modules/sviluppo/cassetta.py:44 — `.gas_richieste_esiti.json` e i suoi file temporanei NON sono in .gitignore (`git check-ignore` dà rc=1). Il file fratello `.gas_richieste_uso.json` invece sì (.gitignore:58). Sul Mac comparirebbe come file non tracciato nella radice. Basta aggiungere le due righe come per il fratello.
2. R-879MV-2 BASSA: modules/sviluppo/cassetta.py:290 — gli esiti partono con `invia_notifica` senza nessun tetto. reports/mani_voce_piano.md:109 dice invece che il tetto giornaliero di avvisa_operatore vale anche qui. Un esecutore ammesso che va fuori controllo può mandare fino a 100 avvisi a ogni controllo. Serve una delle due cose: un tetto per controllo o al giorno, oppure correggere il piano.
3. R-879MV-3 BASSA: modules/sviluppo/cassetta.py:193 — `_numero_issue` confronta il prefisso del repo distinguendo maiuscole e minuscole. Se GAS_RICHIESTE_REPO ha maiuscole diverse dal nome vero, tutti gli esiti vengono scartati come «issue non riconosciuta» e messi tra i visti, quindi restano persi anche dopo aver corretto la configurazione (provato: `{'visti': [1]}`, 0 avvisi). Lo stesso vale per un esito scritto da un autore dimenticato nell'elenco. Va confrontato in minuscolo.
4. R-879MV-4 BASSA: modules/sviluppo/cassetta.py:258 — un commento già visto non fa avanzare `ultimo`. In più `since` di GitHub filtra per data di modifica (updated_at), mentre l'ordine è per data di creazione. Se una pagina contiene 100 commenti già visti (finestra di 120 s molto piena, o vecchi commenti modificati), `since` non si muove più e la lettura si blocca. Probabilità bassa.
5. R-879MV-5 COSMETICA: il conteggio dei test è 51, non 53. Il filtro dei login (modules/sviluppo/cassetta.py:50) rifiuta i login «nome[bot]»: se in F5 l'esecutore scrive come GitHub App, non sarà ammissibile (nota per F5). Con GAS_RICHIESTE_AUTORI vuoto c'è un warning ogni 5 minuti, circa 288 righe al giorno nel log.

Rischi esclusi:
- Non ho verificato le API GitHub reali: che il POST `/labels` crei da solo l'etichetta `annullata` con un token fine-grained «solo Issues», e che `since` si comporti come ho descritto sopra. Questa sandbox non ha il repo privato né il token.
- Non ho verificato il comportamento sul Mac con il bot vivo (thread insieme al polling reale).
- Non ho controllato il percorso a voce (F3b non c'è ancora).

Memoria: ho aggiunto la riga #879-MV e due lezioni (scarti dovuti alla configurazione che si perdono tra i visti; file di stato nuovi da confrontare con .gitignore) in /home/user/Gas/.claude/agents/memoria_revisore.md, committata con lo script in 020059f7. Il diff staged del motore è intatto (7 file).

## VERDETTO: BOCCIATO

Review #880-MV, secondo giro di F3 sul diff staged di claude/mani-voce-f3-avvisi (9 file, +982/−6; ora ci sono anche .gitignore e modules/sviluppo/esiti.py). Il motivo è uno solo: la correzione di R-879MV-4 introduce una perdita silenziosa degli esiti, e l'ho riprodotta.

Elementi del diff esaminati:
- modules/sviluppo/cassetta.py:363 — con la pagina piena, «since» passa al massimo delle date della pagina senza margine. Rischio esaminato: commenti saltati. **Blocco**, vedi il finding 1.
- modules/sviluppo/cassetta.py:201 — `_numero_issue` ora confronta in minuscolo, quindi un repo scritto con maiuscole diverse non scarta più gli esiti. Esito ok: R-879MV-3, parte sul repo, chiusa.
- modules/sviluppo/cassetta.py:320 — un esito di un autore che non è nell'elenco resta «in sospeso» e non entra tra i visti. Viene riletto a ogni controllo (modules/sviluppo/cassetta.py:288), al massimo 20, e un commento cancellato (404) esce dalla lista. Il rischio è lo spam da parte di un collaboratore del repo privato: al massimo 20 letture GitHub a controllo. Esito ok. Il più vecchio oltre i 20 si perde, ma intanto è finito nel log.
- modules/sviluppo/cassetta.py:326 — tetto di 5 avvisi a controllo e di 20 al giorno (massimo 100). Quando scatta, il ciclo si ferma e «since» non avanza, quindi i commenti restano per i controlli dopo. Il conto del giorno sta nello stato. Esito ok: R-879MV-2 chiusa, ora coerente con il piano §4.
- modules/sviluppo/cassetta.py:51 — i login «nome[bot]» sono ammessi; il warning per l'elenco autori vuoto esce una volta per processo (modules/sviluppo/cassetta.py:258). Esito ok: R-879MV-5 chiusa.
- .gitignore:60 — coperti .gas_richieste_esiti.json e i suoi .tmp.*, e un test lo prova con git check-ignore (tests/test_unit_cassetta.py:365). Esito ok: R-879MV-1 chiusa.
- modules/sviluppo/esiti.py:79 — `_virgolette_simili`: i caratteri Pi/Pf, i Ps/Pe non ASCII e U+FF02 diventano virgolette dritte; unicodedata è già importato. Esito ok: ve #411 V-1 chiusa. Resta una nota cosmetica (finding 2).

Prove eseguite su una copia dell'indice:
- cassetta, esiti e richieste: 194 passed (cassetta 68).
- tests/test_unit_kernel.py: 1210 PASS, 0 FAIL.
- Caratteri invisibili veri nei tre file toccati: 0.

Finding:
1. R-880MV-1, motivo del blocco: perdita silenziosa di esiti, in modules/sviluppo/cassetta.py:363 insieme a modules/sviluppo/cassetta.py:305.
   - Il problema: l'API filtra `since` per data di modifica (updated_at), ma `sort=created` ordina per data di creazione. Con la pagina piena, «since» diventa il massimo di max(updated_at, created_at) di tutta la pagina. Se uno dei primi 100 commenti è vecchio ma modificato di recente, «since» salta oltre la data di creazione dei commenti dal 101° in poi, e quelli non tornano mai più.
   - Prova: GitHub finto con 150 commenti dal 20/11, il primo modificato il 26/11 alle 12:00, un ESITO valido al 131°. Dopo 4 controlli: since=2026-11-26T12:00:00Z e 0 avvisi.
   - Quando succede: Gas spento per giorni (più di 100 commenti accumulati) e un commento modificato. È proprio il caso «l'esito arriva alla riaccensione» del piano.
   - Correzione: con la pagina piena usare il created_at dell'ultimo elemento della pagina (è sicuro perché updated_at ≥ created_at; i doppioni dello stesso secondo li toglie l'elenco dei visti). Il massimo delle date con margine resta solo per la pagina non piena.
   - Test da aggiungere: proprio lo scenario sopra. Oggi tests/test_unit_cassetta.py:419 prova solo che la lettura non si blocca, non che non si perde niente.
2. R-880MV-2, cosmetica: modules/sviluppo/esiti.py:79 cambia anche l'apostrofo tipografico U+2019 (Pf, molto comune dalle tastiere del telefono) e le parentesi larghe: «l’operatore （nota）» diventa «l"operatore "nota"». Proposta: mappare Pi/Pf di tipo singolo su «'» e lasciare le parentesi, che non somigliano a «».

Rischi esclusi:
- Il comportamento reale di `since` e `sort` sull'API GitHub (pagine, ordine a parità di secondo) non l'ho verificato: mi baso sulla documentazione e su un GitHub finto, perché qui non ho il repo privato né il token.
- Non ho verificato il thread con il bot vivo sul Mac.

Memoria: ho aggiunto la riga #880-MV e una lezione (con la pagina piena l'unico punto di ripresa sicuro è il created_at dell'ultimo elemento) in /home/user/Gas/.claude/agents/memoria_revisore.md, committata con lo script in f692ce6d. Il diff staged del motore è intatto.

## VERDETTO: APPROVATO CON RISERVE

Review #881-MV, terzo giro di F3 sul diff staged completo di claude/mani-voce-f3-avvisi (9 file, +1058/−7). La perdita di esiti segnalata in #880 non c'è più; restano una riserva bassa e due note cosmetiche, nessuna blocca il commit.

Elementi del diff esaminati:
- modules/sviluppo/cassetta.py:368 — paginazione. Con la pagina piena «since» resta fermo e si legge la pagina dopo; con la pagina non piena «since» avanza al massimo delle date lette meno il margine e la pagina torna a 1; oltre PAGINE_MAX si riparte da adesso con un warning. Rischi esaminati: commenti saltati e lettura bloccata. Esito ok, con la riserva R-881MV-1.
  - Lo scenario di #880 l'ho rifatto a mano con un GitHub finto che filtra su updated_at, ordina per created_at e pagina (250 commenti, il primo modificato il 26/11, ESITO al 131°): l'avviso arriva e alla fine si ha since=2026-11-26T11:58:00Z, pagina 1.
  - Un «since» più basso del necessario è sempre sicuro, e la pagina non piena usa il massimo delle date lette meno il margine.
  - Le modifiche di commenti vecchi fatte durante la paginazione spostano gli elementi a destra, quindi danno solo doppioni, che i visti tolgono.
- modules/sviluppo/cassetta.py:281 — una pagina salvata non valida torna a 1. Con lo stato azzerato (since non valido) la pagina resta quella vecchia, ma una pagina vuota rimette pagina a 1 senza far avanzare since, quindi non si perde niente. Esito ok.
- modules/sviluppo/cassetta.py:331 — tetto per controllo e al giorno. Quando scatta, il giro si interrompe e pagina e since restano come sono. Esito ok.
- modules/sviluppo/esiti.py:88 — gli apostrofi singoli (U+2018, U+2019, U+201A, U+201B) diventano «'», le altre Pi/Pf «"», e le parentesi generiche restano (provato: «l’op» diventa «l'op», le parentesi larghe restano; ‹› e 「」 diventano «"»). Esito ok: R-880MV-2 chiusa.
- tests/test_unit_cassetta.py:449 — test dello scenario di #880. tests/test_unit_cassetta.py:486 — test delle troppe pagine. Esito ok.

Prove su una copia dell'indice:
- cassetta, esiti e richieste: 197 passed.
- tests/test_unit_kernel.py: 1210 PASS, 0 FAIL.
- Caratteri invisibili veri nei 4 file toccati di modules/sviluppo e tests: 0.

Finding:
1. R-881MV-1 BASSA: se un commento più vecchio viene cancellato tra la lettura della pagina N e quella della N+1, tutta la lista scorre di uno verso sinistra. Il primo commento della pagina N+1 finisce in coda alla pagina N, che è già stata letta, e non viene mai letto (modules/sviluppo/cassetta.py:369). L'ho provato: 250 commenti, uno cancellato dopo la prima pagina, l'ESITO al 101° non arriva mai. Serve un arretrato di più pagine più una cancellazione, quindi è raro. Due strade: (a) dichiararlo nel docstring e nel piano; (b) quando una pagina piena si chiude senza interruzioni, rileggere al giro dopo l'ultima pagina piena oltre a quella nuova. Così uno slittamento di un elemento torna nella finestra, e i visti tolgono i doppioni.
2. R-881MV-2 COSMETICA, due note:
   - Con un numero di commenti multiplo esatto di 100 e nessun commento nuovo, la pagina 2 è vuota, «since» non avanza e ogni due controlli si rilegge la pagina 1. Nessuna perdita, solo letture inutili, finché non arriva un commento nuovo (provato).
   - L'elenco delle virgolette simili a «» non è ancora completo: passano ⪡⪢ (U+2AA1/U+2AA2) e ⋘⋙. Il confine vero resta nelle parti fisse e in F4 (R-873MV-1), come già detto per R-877MV-2.

Rischi esclusi:
- Il comportamento reale dell'API GitHub su `page`, `since` e `sort=created` (ordine a parità di secondo, limiti di paginazione) non l'ho verificato: qui non ho il repo privato né il token, quindi ho usato solo un GitHub finto costruito secondo la documentazione.
- Non ho verificato il thread con il bot vivo sul Mac.

Memoria: ho aggiunto la riga #881-MV e una lezione (la paginazione per numero di pagina perde un elemento a ogni cancellazione tra due letture) in /home/user/Gas/.claude/agents/memoria_revisore.md, committata con lo script in a518d9e5. Il diff staged del motore è intatto.

## VERDETTO: APPROVATO CON RISERVE

Review #882-MV. È il 4° giro di F3 (le «mani alla voce»: Gas avvisa l'operatore su Telegram quando arriva l'esito di una richiesta), dopo la verifica esterna e il bot sulla #412 (head 45f739d8). Ho guardato il diff staged su claude/mani-voce-f3-avvisi: modules/sviluppo/cassetta.py e tests/test_unit_cassetta.py, +100/−11. Ho letto CLAUDE.md, lo stato del progetto (la parte su F3) e la mia memoria (lezioni #877-#881).

**Le quattro verifiche che mi hai chiesto**
- **Stato non scrivibile, nessun avviso ripetuto: confermato.** Con il file di stato non scrivibile non parte mai niente; il test fa 4 controlli e non esce nessun testo.
- **Invio fallito, l'esito non si perde: confermato.** Si annulla il segno di «già visto» e si riprova al controllo dopo. Resta un caso, dichiarato nel docstring: se fallisce anche la scrittura finale, l'avviso si perde (consegna al più una volta).
- **since e pagina non rotti dall'uscita anticipata: confermato.** Sia l'uscita per stato non scrivibile sia quella per invio fallito saltano l'aggiornamento di since e pagina, quindi al giro dopo si rilegge la stessa pagina. Nessuna perdita e nessun doppione.
- **Le domande non regrediscono: solo in parte.** Due casi le fanno ancora regredire, provati con test scritti apposta (R-882MV-1 e R-882MV-2 sotto).

**Elementi del diff esaminati**
1. modules/sviluppo/cassetta.py:369 — lo stato si scrive prima dell'invio; se la scrittura fallisce si ripristinano visti e conto del giorno e si esce senza inviare. Rischio esaminato: avviso ripetuto a ogni controllo. Esito: ok.
2. modules/sviluppo/cassetta.py:376 — se l'invio fallisce si annulla il segno e si esce dal ciclo, senza aggiornare since e pagina. Rischio esaminato: esito perso o tetto consumato. Esito: ok (test tests/test_unit_cassetta.py:546).
3. modules/sviluppo/cassetta.py:350 — issue sparita (404/410) scartata; gli altri errori fermano il ciclo e si riprova. Rischio esaminato: la fila si blocca. Esito: ok (test tests/test_unit_cassetta.py:512).
4. modules/sviluppo/cassetta.py:270 — gli esiti si leggono solo se il repo è privato, e se il controllo non riesce non si leggono (fail-closed). Rischio esaminato: lettura da un repo pubblico. Esito: ok. Costa una chiamata HTTP in più a ogni controllo.
5. modules/sviluppo/cassetta.py:390 — un esito più recente senza proposta di merge cancella la domanda. Rischio esaminato: regressione delle domande. Esito: riserva (R-882MV-1).
6. modules/sviluppo/cassetta.py:223 — domanda_aperta legge sia il formato nuovo {"pr","quando"} sia il vecchio (numero intero). Esito: ok.

**Finding**
- **R-882MV-1 BASSA (va chiusa prima di F4, che oggi non esiste).** La correzione per il bot V-3 copre solo metà dei casi. Quando l'esito più recente non propone il merge, la domanda viene cancellata e con lei la data «quando». Poi un esito vecchio recuperato dai sospesi la riapre. Provato: esito vecchio con PR 400 in sospeso, poi un esito più recente con CI rossa chiude la domanda, poi si aggiunge l'autore e domanda_aperta torna 400. Correzione: invece di cancellare, salvare una lapide `{"pr": None, "quando": creato}`; domanda_aperta già ritorna None in quel caso.
- **R-882MV-2 BASSA.** Se lo stato diventa non scrivibile a metà controllo (uscita a modules/sviluppo/cassetta.py:374), oppure se c'è un crash tra invio e scrittura finale, la domanda degli esiti già inviati non si salva. Provato: l'operatore riceve l'avviso per la PR 500, ma domanda_aperta resta 400 finché un giro sano non la aggiorna. Correzione per F4: togliere la domanda di quella richiesta già nella scrittura prima dell'invio (fail-closed), oppure salvare comunque le domande prima di uscire.
- **R-882MV-3 COSMETICA.**
  - In modules/sviluppo/cassetta.py:360 il commento contiene una parola di gravità in maiuscolo (quella dopo «ve #412 V-1»). Il bot può citarla e ridare il falso rosso, come in #877: meglio scriverla in minuscolo.
  - Per una issue sparita il log dice «issue non da-gas», che è fuorviante.
  - Con il repo non privato o irraggiungibile esce un warning a ogni controllo, cioè ogni 5 minuti.

**Altri controlli**
- 203 test passati (cassetta, esiti e richieste; cassetta da sola 77).
- 0 caratteri invisibili nel diff.
- Nessun taglio della cronologia: visti[-VISTI_MAX:] taglia una lista di id di commenti, non la history dei messaggi.

**Cosa NON ho verificato**
- **La suite completa:** l'ho lanciata ma non è finita entro i tempi; vale solo il risultato sui tre moduli toccati.
- **GitHub vero:** come si comporta quando una issue viene trasferita (risposta 301) e la rete reale non sono provati, perché il GitHub dei test è finto.
- **Il piano:** reports/mani_voce_piano.md è modificato solo nel working tree, fuori dal perimetro di review, e non l'ho letto.

La memoria è committata: 816716c7, con riga contatore e una lezione nuova. Il diff staged è rimasto com'era.

## VERDETTO: APPROVATO CON RISERVE

Review #883-MV, 5° giro di F3 su claude/mani-voce-f3-avvisi. Ho guardato il diff staged: modules/sviluppo/cassetta.py e tests/test_unit_cassetta.py, +150/−12, uguali al working tree. R-882MV-1, R-882MV-2 e le cosmetiche sono chiuse. I miei test di riproduzione R1 e R2 ora passano. Ne resta uno nuovo, basso, da tenere per F4.

**Riserve aperte**
1. **R-883MV-1 BASSA (per F4).** Oggi la domanda nuova si scrive già nella scrittura prima dell'invio. Se poi l'avviso non arriva, sul disco resta una domanda fantasma. Succede in due casi: un crash tra scrittura e invio, oppure l'invio che fallisce e subito dopo fallisce anche la scrittura finale. Provato con il test R3 nello scratchpad: domanda_aperta dà 500 senza che l'avviso della 500 sia mai partito. In questi casi l'esito si perde, come dichiarato («al più una volta»). Il rischio vero è un «sì» dell'operatore dato alla domanda vecchia (PR 400) e applicato alla 500. Due modi di chiuderlo:
   - nella scrittura prima dell'invio mettere la lapide (pr None) e scrivere la PR solo dopo l'invio riuscito;
   - oppure far confermare a F4 il numero della PR.
2. **COSMETICA.** Le lapidi restano per sempre, una per richiesta: crescita piccola, limitata dal numero di richieste.
- Il warning ogni 5 minuti con il repo non privato lo lasci così: accetto la motivazione, è un guasto vero e conviene che si veda.

**Elementi del diff esaminati**
- modules/sviluppo/cassetta.py:372 — un esito è «vecchio» se c'è già una data e la sua è più vecchia o manca. Rischio: la domanda regredisce. Esito: ok. Nella riproduzione R1 la domanda resta None dopo il recupero del sospeso.
- modules/sviluppo/cassetta.py:375 — un esito senza domanda lascia la lapide; domanda_aperta (modules/sviluppo/cassetta.py:223) la legge come None. Rischio: un esito vecchio riapre la domanda. Esito: ok.
- modules/sviluppo/cassetta.py:383 — la domanda si scrive insieme al segno di visto prima dell'invio; se la scrittura fallisce si ripristinano visti, conto e domande. Rischio: domanda vecchia dopo un avviso nuovo. Esito: ok. Nella riproduzione R2 domanda_aperta dà 500 subito dopo l'avviso della 500.
- modules/sviluppo/cassetta.py:394 — invio fallito: le domande tornano come prima in memoria. Rischio: domanda fantasma. Esito: riserva (R-883MV-1).
- modules/sviluppo/cassetta.py:357 — il log ora dice «issue sparita o non da-gas». Esito: ok.

**Controlli fatti**
- 206 test passati (cassetta, esiti, richieste).
- 0 caratteri invisibili e nessuna parola di gravità maiuscola nel diff.
- Nessun taglio della cronologia: visti[-VISTI_MAX:] taglia una lista di id, non la history dei messaggi.

**Cosa NON ho verificato**
- La suite completa del kernel: non è stata rilanciata in questo giro.
- Il comportamento di GitHub vero (301 sulle issue trasferite, rete reale): nei test GitHub è finto.
- Il piano: reports/mani_voce_piano.md è fuori dal perimetro di review e non l'ho letto.

La memoria è committata (5b2c904a, con riga contatore e una lezione nuova). Il diff staged è rimasto com'era.

## VERDETTO: APPROVATO CON RISERVE

Review #884-MV sul diff staged del ramo claude/mani-voce-f3b: 4 file, +270/−14. Ho letto CLAUDE.md, la riga F3b di reports/mani_voce_piano.md, la voce «Mani alla voce» di reports/stato_progetto.md e la mia memoria. Test: cassetta + voice_server + telegram_voce danno 416 passati. Nel diff non ci sono caratteri invisibili, parole di gravità maiuscole, slicing della history né simulazione di tool.

**Elementi esaminati**
1. modules/sviluppo/cassetta.py:493 — `frase_voce` usa solo il numero (int), lo stato (confrontato, mai interpolato), la PR (int e non bool) e testi fissi. Rischio: testo libero dell'esecutore a voce (R-873MV-1). Il ramo else e l'eccezione danno frasi fisse. Esito: ok.
2. modules/voice/server.py:986 — l'annullo è dentro `if not self._seguito():`, dopo `togli_parola_in_testa`. Rischio: annullo dal parlato della stanza. Nel seguito non è raggiungibile. `_annulla_richiesta` mette tutto in try e restituisce None, quindi il turno parte normale. La risposta passa da `_rispondi_senza_turno` senza prefisso: con `_esiti_voce` azzerato in do_POST non segna niente. Esito: ok.
3. modules/telegram/bot.py:1070 — vocale Telegram intercettato senza turno, con try e None in caso di errore. Rischio: chat non autorizzate o messaggi modificati. Il chiamante modules/telegram/bot.py:925 accetta solo vocali nuovi, e la chat autorizzata è controllata prima della trascrizione. Esito: ok.
4. modules/voice/server.py:1220 — segna detti gli esiti solo nei punti di consegna già esistenti (JSON, MP3, pezzi). Gli errori del kernel (risposta 500) non li segnano. L'errore della cassetta in `_compiti_finiti` è isolato e i compiti in sottofondo si dicono lo stesso. La doppia chiamata in modules/voice/server.py:1086 riscrive in modo coerente. Esito: ok.
5. modules/sviluppo/cassetta.py:407 — `da_leggere` si aggiorna dopo un invio riuscito. Va su disco solo con la scrittura successiva. Esito: riserva (vedi R-884MV-1 e la cosmetica).
6. modules/sviluppo/cassetta.py:336 — uno scarto definitivo esce dai sospesi (bot #412 V-1), anche per la issue sparita. Esito: ok.

**Finding**
- **R-884MV-1 MEDIA** — Due processi diversi scrivono lo stesso file `.gas_richieste_esiti.json` senza lock: `segna_letti_voce` (server voce) e `controlla_esiti` (thread del bot). Il controllo tiene lo stato in memoria per tutta la sua durata. L'ho provato con script nello scratchpad:
  - (a) segno di lettura dato durante il GET dei commenti: la scrittura finale del controllo rimette l'esito, che si **ridice a voce**. Script: /tmp/claude-0/-home-user-Gas/bbb95bff-21f7-5fb1-9612-e74ec6e464ca/scratchpad/race.py
  - (b) controllo che scrive in mezzo al segno: `visti` si perde e il **Telegram ripete l'avviso** dell'esito 2 (3 avvisi invece di 2). Tornano indietro anche la domanda ricordata (`domande`) e il conto del giorno. Script: /tmp/claude-0/-home-user-Gas/bbb95bff-21f7-5fb1-9612-e74ec6e464ca/scratchpad/race_b.py
  - Le finestre sono strette: (a) dura quanto il controllo ogni 5 minuti, (b) pochi millisecondi. Però (b) riapre il «niente avvisi ripetuti» di ve #412 V-1 e tocca lo stato che userà F4.
  - Correzione consigliata in questa fetta, che costa poco: un file a scrittore unico per i «letti», scritto solo dal server voce, con `da_leggere_voce` che filtra. In alternativa un lock condiviso.
- **R-884MV-2 BASSA** — Nessun test prova che «annulla richiesta N» detto nel seguito vada al turno normale. Il codice è giusto, ma senza test una regressione passerebbe.
- **COSMETICA** — Se l'invio riesce ma la scrittura finale fallisce, o c'è un crash dopo l'invio, la frase a voce si perde. L'avviso su Telegram arriva comunque.

**Cosa non ho verificato**: il comportamento dal vero sul Mac (STT Groq che trascrive «annulla richiesta numero 12», client `clients/voice/ascolto.py`): non si riproduce qui. Ho solo controllato che clients/voice/ascolto.py e scripts/voce/ non siano nel diff. Non ho verificato neanche due richieste a voce in parallelo che leggono gli stessi esiti: è lo stesso limite già accettato per i compiti in sottofondo.

Memoria aggiornata (riga #884-MV più una lezione) e committata: commit 2edfc3fb, file /home/user/Gas/.claude/agents/memoria_revisore.md.

## VERDETTO: APPROVATO

Review #885-MV, secondo giro di F3b sul diff staged del ramo claude/mani-voce-f3b (5 file, +335/−14). Le due riserve della #884-MV sono chiuse. Ho rifatto i due script della corsa e nessuno dei due riproduce più il problema. Restano solo due note cosmetiche, nessun finding numerato aperto.

- `- verdetto precedente: #884-MV APPROVATO CON RISERVE (R-884MV-1 MEDIA, R-884MV-2 BASSA), ora superato.`

**Elementi esaminati**
1. modules/sviluppo/cassetta.py:548 — `segna_letti_voce` scrive solo `.gas_richieste_letti_voce.json` (permessi 0600, file temporaneo e poi `os.replace`, eccezioni prese e messe nel log), mai lo stato del bot. Rischio: la scrittura persa fra i due processi (R-884MV-1). Ogni file ha ora un solo scrittore. Esito: ok.
2. modules/sviluppo/cassetta.py:541 — `da_leggere_voce` toglie i già detti leggendo il file dei letti, senza scrivere niente. Rischio: ripetere o perdere esiti a voce. I letti ricordati sono al massimo 100, molto più dei 5 esiti in attesa, quindi un esito in lista non viene dimenticato. Esito: ok.
3. tests/test_unit_cassetta.py:748 — controllo statico sul codice di do_POST: esiste una sola chiamata a `_annulla_richiesta` e sta dentro `if not self._seguito():`. Rischio: annullo dal parlato della stanza (R-884MV-2). Il controllo guarda solo il ramo vero, non l'else, quindi è corretto. Esito: ok.
4. .gitignore:62 — il file nuovo e i suoi temporanei sono ignorati. Esito: ok.

**Riprove**
- Lo script race.py ora dà 0 esiti da ridire (prima 1). Path: /tmp/claude-0/-home-user-Gas/bbb95bff-21f7-5fb1-9612-e74ec6e464ca/scratchpad/race.py
- race_b.py non regge più: modificava `_leggi_stato`, che il segno di lettura a voce non usa più. L'ho riscritto come race_b2.py, che fa scrivere il bot nel mezzo della lettura del file dei letti. Dà 2 avvisi Telegram, cioè nessun avviso ripetuto (prima 3). Path: /tmp/claude-0/-home-user-Gas/bbb95bff-21f7-5fb1-9612-e74ec6e464ca/scratchpad/race_b2.py
- tests/test_unit_cassetta.py: 95 passati.

**Note cosmetiche** (non bloccano)
- Due richieste a voce in parallelo sullo stesso server possono perdere un segno di lettura: quell'esito si ridice una volta.
- Se il file dei letti è illeggibile, si ridicono al massimo 5 esiti delle ultime 24 ore. L'errore va verso la ripetizione, non verso la perdita.

**Cosa non ho verificato**
- In questo giro non ho rilanciato test_unit_voice_server.py e test_unit_telegram_voce.py (servono circa 5 minuti): le stat di modules/voice/server.py e modules/telegram/bot.py non sono cambiate e nel giro #884 passavano 416 test. Conviene rilanciarli prima del commit.
- Il comportamento dal vero sul Mac (trascrizione Groq, client di ascolto) non si può riprodurre qui.

Memoria aggiornata con la riga #885-MV e committata (cb31b806): /home/user/Gas/.claude/agents/memoria_revisore.md

## VERDETTO: APPROVATO CON RISERVE

Review #886-MV. Ramo claude/mani-voce-f3b, PR #414, diff staged su `modules/sviluppo/cassetta.py`, `modules/telegram/bot.py` e `tests/test_unit_cassetta.py` (+78/−17). Prima della review ho letto CLAUDE.md (§5), lo stato del progetto e la memoria del revisore.

**Elementi del diff esaminati**
- `tests/test_unit_cassetta.py:704` — l'accodo ora usa datetime.now prima di `_compiti_finiti` e di `da_leggere_voce` chiamati senza data. Rischio cercato: altri test che accodano con una data fissa e poi leggono con l'orologio vero. Ho elencato tutte le chiamate senza `adesso=`: restano solo le righe 708-742, tutte dopo un accodo fatto con l'ora vera. Le altre chiamate a `controlla_esiti` e `da_leggere_voce` passano la data fissa da entrambi i lati. Il test con la data futura (`tests/test_unit_cassetta.py:773`) passa. — ok, bot V-1 chiusa.
- `modules/sviluppo/cassetta.py:396` — la frase da dire a voce entra nello stato prima della scrittura che precede l'invio. Ho verificato il ripristino:
  - lo stato di partenza include ora `da_leggere`, ed è la lista vecchia (la nuova è un oggetto distinto, quindi la copia non viene toccata);
  - se la scrittura fallisce, il ripristino rimette la lista vecchia;
  - se l'invio fallisce (`modules/sviluppo/cassetta.py:416`) la lista vecchia torna in memoria, e la scrittura finale dopo il `break` (`modules/sviluppo/cassetta.py:449`) la riporta sul disco.

  Il test che lascia riuscire solo la prima scrittura (`tests/test_unit_cassetta.py:807`) prova che la frase sopravvive anche se la scrittura finale fallisce. — ok, bot V-3 chiusa.
- `modules/telegram/bot.py:1067` — nei vocali l'annullo si controlla su tutto il trascritto, PRIMA di `cervello_voce`, come sul Mac (`modules/voice/server.py:1172`, contesto). Rischio cercato: «forte annulla richiesta 7» che annulla davvero. Non annulla (`tests/test_unit_cassetta.py:790`), e il caso positivo resta coperto (`tests/test_unit_cassetta.py:674`). — ok, bot V-2 chiusa.
- `modules/sviluppo/cassetta.py:73` — la regex per «annulla richiesta» senza numero. L'ho provata su frasi vere. Prende come previsto «annulla richiesta dodici» e «annulla la richiesta numero dodici per favore». Non prende «annullare la richiesta», «annulla richieste», «annulla richiesta 12 e 13» e «annulla richiesta n. 12» (le ultime due vanno al modello). Prende però anche frasi normali. — riserva (finding 1).

**Finding**
1. R-886MV-1 (gravità bassa): la regex scatta su ogni frase che comincia con «annulla (la) richiesta» e non contiene cifre, fino a 80 caratteri. Esempi provati: «annulla la richiesta che ti ho fatto prima», «Annulla la richiesta di ferie per domani mattina.». Queste frasi ricevono la risposta fissa («mi serve il numero in cifre») invece del turno del modello. Il danno è nullo (va nel verso sicuro), ma è fastidioso, e su Telegram vale per tutti i vocali. Proposta: scattare solo se dopo «richiesta» c'è al più «numero» più una o due parole, oppure con un elenco dei numeri scritti in lettere.
2. Nota minore: la risposta fissa non dice «richiesta di sviluppo», quindi chi intendeva un'altra cosa non capisce il motivo.
3. Nota minore: «annulla richiesta n. 12» (forma possibile nella trascrizione) va ancora al modello.
4. Nota minore: il test «forte» controlla solo che l'annullo non sia partito, non che il turno parta davvero (il commento nel test lo dice).
5. Nota minore, stessa famiglia di R-883MV-1: con un crash fra la scrittura e l'invio, sul disco resta una frase a voce che rimanda a un avviso Telegram mai arrivato.

Wall of Shame: nessun taglio della cronologia dei messaggi (`da_voce[-LETTURE_MAX:]` è una lista di stato, non la cronologia della chat) e nessun output dei tool simulato. Le eccezioni restano intercettate (§9): `annulla_parlato` dentro il try, e nel bot l'annullo è in try con il log e il turno normale come ripiego.

**Esecuzione**
- 101 passed in `tests/test_unit_cassetta.py`.
- 424 passed su cassetta, voice_server e telegram_voce insieme (circa 5 minuti).
- 0 caratteri invisibili (categorie Cf/Cc) e 0 parole di gravità maiuscole nel diff.

**Cosa non ho verificato**
- I test con l'orologio davvero spostato (faketime): non installato. L'indipendenza dalla data l'ho verificata leggendo tutte le chiamate senza `adesso=`.
- La trascrizione reale di Groq per «annulla richiesta dodici» o «n. 12»: serve un audio vero, non riproducibile qui.

La riga contatore #886-MV e una lezione sono in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole con `scripts/commit_memoria_revisore.sh` (commit 46422736).

## VERDETTO: APPROVATO

Review #887-MV: rivisto tutto il diff staged sul ramo claude/mani-voce-f3b (PR #414), +97/−18. Prima della review ho letto CLAUDE.md (§5), lo stato del progetto e la memoria del revisore. R-886MV-1 e le note 2 e 3 della #886-MV sono chiuse; nessun finding bloccante.

**Elementi del diff esaminati**
- `modules/sviluppo/cassetta.py:75` — la nuova regex del caso «senza numero»: dopo «annulla (la) richiesta (numero)» ammette al più due parole di sole lettere ASCII. Rischio esaminato: che prenda ancora frasi normali. Ho provato 13 frasi:
  - vanno al modello: «annulla la richiesta che ti ho fatto prima» (troppe parole), «Annulla la richiesta di ferie per domani mattina.», «annulla la richiesta di ferie» (c'è «di»), «annulla la richiesta più vecchia» («più» non è ASCII);
  - ricevono la risposta fissa: «annulla richiesta dodici», «annulla la richiesta numero dodici», «annulla richiesta ventidue.».
  — ok, R-886MV-1 chiusa.
- `modules/sviluppo/cassetta.py:583` — il controllo delle parole di legame (di, che, per, ecc.) e il limite di 60 caratteri. La risposta ora dice «una richiesta di sviluppo». Il blocco resta dentro il try con il log (regola §9). — ok, nota 2 chiusa.
- `modules/sviluppo/cassetta.py:79` — la regex del comando accetta ora «n. 12» e «n.12». Rischio esaminato: si allarga anche l'annullo da messaggio di testo su Telegram, perché lì si usa la stessa funzione (`modules/telegram/bot.py:979`, contesto). La frase deve restare intera, in ASCII, con un numero da 1 a 7 cifre: allargamento accettabile. — ok, nota 3 chiusa.
- `tests/test_unit_cassetta.py:826` e `tests/test_unit_cassetta.py:830` — test nuovi: le tre frasi normali vanno al modello e c'è il caso «n. 12». — ok.
- Le correzioni del giro precedente sono invariate: frase a voce scritta prima dell'invio e tolta se l'invio fallisce (`modules/sviluppo/cassetta.py:400`, `modules/sviluppo/cassetta.py:420`); annullo dei vocali prima di cervello_voce (`modules/telegram/bot.py:1067`); test che non dipendono dalla data (`tests/test_unit_cassetta.py:704`). — ok.

**Note minori (non bloccano)**
- «annulla la richiesta numero dodici per favore» va al modello per via di «per»: il caso del bot V-2 (il modello che potrebbe dire di aver annullato) resta aperto solo per questa forma.
- «annulla la richiesta prima» e «annulla la richiesta di.» ricevono la risposta fissa: «di.» col punto attaccato sfugge al controllo, perché le parole si separano solo sugli spazi. Il danno è nullo.

**Esecuzione e controlli**
- 105 passed in `tests/test_unit_cassetta.py`, 74 passed in `tests/test_unit_telegram_voce.py`.
- 0 caratteri invisibili e 0 parole di gravità maiuscole nel diff.
- Wall of Shame: nessun taglio della cronologia e nessun output dei tool simulato.

**Cosa non ho verificato**
- Il file `tests/test_unit_voice_server.py` non l'ho rilanciato: il server voce non è nel diff e chiama la stessa funzione già provata qui (424 passed nella #886-MV).
- Le trascrizioni reali di Groq: servono audio veri, non riproducibili qui.

Ho aggiunto la riga #887-MV in `/home/user/Gas/.claude/agents/memoria_revisore.md` e l'ho committata da sola (commit d99f9ad4).

## VERDETTO: APPROVATO CON RISERVE

Review #888-MV. Ho esaminato il diff staged sul ramo claude/mani-voce-f4 (+259/−11, 6 file).

**Elementi del diff esaminati**
- `modules/sviluppo/cassetta.py:398` — prima dell'invio nello stato va solo la lapide (pr None). Rischio: che resti una domanda fantasma se l'avviso non parte. Esito: ok. Sull'invio fallito si torna a `domande_prima`. Se la scrittura finale fallisce resta la lapide, quindi il «mergia» viene rifiutato (il test modificato in tests/test_unit_cassetta.py:588 lo prova).
- `modules/sviluppo/cassetta.py:425` — la PR viene ricordata solo dopo `inviati += 1`, sullo stesso dizionario `domande` che finisce in `stato["domande"]` nella scrittura finale. Rischio: perdita della PR per un `return` anticipato al giro dopo. Esito: ok, e si perde in modo sicuro (domanda rifiutata, mai inventata).
- `modules/sviluppo/cassetta.py:663` — `richiesta_della_pr` confronta la PR con le domande vere e scarta le coppie (richiesta, quando) che hanno già una risposta. Rischio: merge di una PR mai proposta, oppure di una domanda superata da un esito più recente. Esito: ok. Una lapide (pr None) non corrisponde mai e un esito nuovo cambia «quando», quindi riapre la domanda in modo corretto. Riserva R-888MV-1 qui sotto.
- `modules/sviluppo/cassetta.py:682` — il comando viene ricordato in locale solo dopo il POST 201; se la scrittura fallisce resta solo un warning nel log. Rischio: comando ripetuto. Esito: riserva R-888MV-2.
- `modules/sviluppo/cassetta.py:608` — `_comandi` legge un file illeggibile come lista vuota. Rischio: è fail-open rispetto al vincolo «una volta sola». Esito: riserva R-888MV-2.
- `modules/telegram/bot.py:988` — annullo e merge passano prima del modello, e un messaggio modificato viene rifiutato prima di qualsiasi azione. Rischio: che un messaggio modificato faccia scattare il comando. Esito: ok. Su un messaggio modificato `annulla_parlato` arriva solo al ramo senza numero, che dà la risposta fissa e non fa niente.
- `modules/telegram/bot.py:1072` — il merge vale anche nei vocali Telegram, che passano dopo il controllo della chat ammessa. Esito: ok. Il comando si usa una volta sola, quindi un vocale rielaborato riceve «già risposto».
- `modules/voice/server.py:1172` — al microfono del Mac «mergia/no N» riceve RISPOSTA_SOLO_TELEGRAM prima di `annulla_parlato` e non fa nessuna chiamata HTTP né scrittura. Esito: ok.
- `gas.py:436` — la regola nel prompt di base. Il prompt di base si aggiunge sempre, anche quando gas_identity.md c'è. Rischio: rompere i test del kernel. Esito: ok, `import gas` funziona e l'unico test che legge il prompt (tests/test_unit_kernel.py:8818) cerca altre stringhe.
- Concorrenza: `rispondi_merge` legge lo stato del bot, che il thread di controllo scrive con `os.replace` atomico, quindi non può leggere un file a metà. Il file dei comandi lo scrive solo il thread principale del bot, perché anche i vocali passano da `_handle_update`. Il server voce non lo tocca. Esito: ok.

Prove: 117 passed in tests/test_unit_cassetta.py, 74 passed in tests/test_unit_telegram_voce.py, 0 caratteri invisibili nel diff.

**Riserve**
1. **R-888MV-1 BASSA** — `rispondi_merge` non controlla che la issue sia ancora aperta, con l'etichetta da-gas e senza `annullata`. Dopo «annulla richiesta 7», un «mergia 412» scrive comunque il comando MERGIA sulla issue chiusa: GitHub accetta commenti sulle issue chiuse. In più le domande non scadono mai: una domanda di mesi fa resta valida finché non arriva un esito più recente. La protezione oggi c'è solo in F5 (l'esecutore salta le annullate e ricontrolla §10). Basterebbe la stessa GET che fa `annulla` (stato open, etichette) prima del POST.
2. **R-888MV-2 BASSA** — il vincolo «una volta sola» vive solo in `.gas_richieste_comandi.json`. Se il file è corrotto viene letto come vuoto e tutte le domande aperte tornano rispondibili; se la scrittura fallisce dopo il POST, la stessa domanda accetta un secondo comando, anche un NO dopo un MERGIA, cioè due comandi contraddittori sulla issue. Correzione possibile: rifiutare quando il file c'è ma non si legge (solo FileNotFoundError vale come vuoto). Regola per F5: vale solo il primo COMANDO dopo l'ultimo ESITO.

**Note cosmetiche**: un «mergia N» mandato subito dopo l'avviso viene rifiutato finché il thread di controllo non fa la scrittura finale (si perde in modo sicuro, basta riprovare). «no 3» scritto come risposta qualunque viene intercettato con «Non ti ho chiesto il merge della PR #3». Un `pr: true` scritto a mano nello stato corrisponderebbe a «mergia 1», perché a differenza di `domanda_aperta` qui non c'è la guardia sul bool.

**Rischi esclusi**: non ho lanciato le suite complete del kernel e del server voce, perché sono già in corso in background dall'agente principale; della regola nel prompt ho verificato solo l'import e il test che legge il prompt. Il comportamento vero con GitHub, cioè un POST su una issue chiusa o bloccata e la lettura dei COMANDO da parte dell'esecutore, non l'ho verificato: senza rete e senza repo delle richieste qui non si può riprodurre, e quella parte è di F5.

La memoria è aggiornata (riga #888-MV più una lezione) e committata in e8ce313f.

## VERDETTO: APPROVATO CON RISERVE

Review #889-MV, secondo giro di F4: diff staged completo sul ramo claude/mani-voce-f4 (+311/−11, 6 file). R-888MV-1 e R-888MV-2 sono chiuse e la guardia sul bool c'è. Resta un caso raro e una riserva BASSA, sotto.

Risultati: 195 test passati (tests/test_unit_cassetta.py e tests/test_unit_telegram_voce.py), 0 caratteri invisibili nel diff.

**Punti del diff controllati**
- `modules/sviluppo/cassetta.py:682` — prima del POST ora c'è una GET sulla issue: deve essere aperta, con l'etichetta da-gas, senza `annullata` e non una PR. Se la GET fallisce o la issue non va bene, non parte niente. Il rischio era il «mergia» dopo un «annulla richiesta». Esito: ok, R-888MV-1 chiusa, la prova il nuovo test della richiesta annullata o chiusa.
- `modules/sviluppo/cassetta.py:691` — il comando si prenota in locale prima del POST; se la prenotazione non si scrive non si fa niente. Un file c'è ma non si legge dà None, e allora nessun comando nuovo (`modules/sviluppo/cassetta.py:646` in `richiesta_della_pr`, ripetuto a :694). Il rischio era il doppio comando con il file corrotto o non scritto. Esito: ok, R-888MV-2 chiusa.
- `modules/sviluppo/cassetta.py:702` — se il POST non risponde 201 la prenotazione si toglie, così l'operatore può riprovare. Il rischio è che non si sappia se il commento è stato scritto davvero. `_http` (modules/sviluppo/richieste.py:58) non solleva mai eccezioni e dà 0 su rete giù o timeout. Esito: riserva R-889MV-1.
- `modules/sviluppo/cassetta.py:650` — un `pr` booleano nello stato non corrisponde più a «mergia 1». Esito: ok.
- Le parti non cambiate dal giro #888 restano ok: niente merge al microfono del Mac (`modules/voice/server.py:1172`), il bot che intercetta merge e annullo prima del modello e rifiuta i messaggi modificati (`modules/telegram/bot.py:988`), la regola nel prompt (`gas.py:436`).
- Concorrenza: invariata. Il file dei comandi lo scrive solo il thread principale del bot; lo stato del bot qui si legge soltanto, e la scrittura è atomica con `os.replace`. Esito: ok.

**Riserve**
1. R-889MV-1 BASSA: se il POST va a buon fine ma la risposta si perde (timeout, codice 0), la prenotazione viene tolta. La stessa domanda può allora ricevere un secondo comando, anche opposto (un NO dopo un MERGIA già scritto). Due rimedi possibili:
   - regola per F5: vale solo il primo COMANDO dopo l'ultimo ESITO sulla issue;
   - oppure tenere la prenotazione quando il codice è 0.

**Note cosmetiche**: con il file dei comandi illeggibile l'operatore riceve «non ti ho chiesto / già risposto» invece di «elenco illeggibile», perché `richiesta_della_pr` esce prima. Oltre COMANDI_MAX (200) le risposte più vecchie si dimenticano, cosa irrilevante in pratica. La scelta di non dare una scadenza alle domande è accettabile: ogni esito nuovo le riapre o le chiude, e F5 ricontrolla §10.

**Rischio escluso**: non ho lanciato le suite complete del kernel e del server voce, che l'agente principale ha in corso in background. Non ho verificato il comportamento reale di GitHub (commenti su issue bloccate, lettura dei COMANDO da parte dell'esecutore) perché qui non c'è il repo delle richieste: è materia di F5.

Memoria aggiornata (riga #889-MV più una lezione) e committata in a0a88e87.

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_esiti.py`: 63 → 101 test (PR #411 e F3; verifica esterna #414 V-1: prima avevo scritto 103).
- `tests/test_unit_cassetta.py`: nuovo, 71 (6fce9e43) → 80 (9f4650d6) → 95 (28947ffc) → 105 (0338ed09) → 121 (2863bf4c).
- voice_server + telegram_voce + cassetta + esiti + richieste sul commit 28947ffc: `544 passed in 293.19s`.
- `tests/test_unit_kernel.py` (script): `=== RIEPILOGO: 1210 PASS, 0 FAIL ===` su 28947ffc.
- Su 2863bf4c (F4): voice_server + telegram_voce + cassetta + esiti + richieste `566 passed in 301.01s`; kernel rilanciato in background (F4 tocca solo il prompt di base in gas.py; `import gas` e il test che legge il prompt ok nel revisore).

## §6 STATO CI

- Commit della PR #411 (fino a 5af3680e): sul head 5af3680e unit-suite, handoff-check e verifica-bot success.
- Commit della PR #412 (fino a 179cde04): sul head 179cde04 unit-suite e handoff-check success, verifica-bot neutral (la PR tocca ci.yml).
- 2edfc3fb, cb31b806, 28947ffc: nessuna run su questi SHA (pushati insieme a 8f6787a6).
- 8f6787a6: handoff-check success; verifica-bot failure (BOCCIATO: test dipendenti dalla data, gravità media vera, corretta in 0338ed09).
- 46422736, d99f9ad4, 0338ed09, 10bd0bd6: run della PR #414 (head 10bd0bd6).
- e8ce313f, a0a88e87, 2863bf4c e il commit di fine-task: ramo nuovo, run non ancora disponibile alla scrittura dell'handoff (`gh run list` non è disponibile qui; si legge con `gh api`).

## §7 RISERVE APERTE

- R-889MV-1 BASSA — se la risposta del POST del comando si perde (codice 0) la prenotazione si toglie e un secondo comando, anche opposto, è possibile: regola per F5, vale solo il primo COMANDO dopo l'ultimo ESITO.
- Cosmetiche #888/#889-MV: «mergia» subito dopo l'avviso rifiutato finché il controllo non scrive lo stato (basta riprovare); «no 3» intercettato; file dei comandi illeggibile → «non ti ho chiesto / già risposto»; COMANDI_MAX 200.
- Chiuse da F4: R-883MV-1 (PR ricordata solo dopo l'avviso), R-873MV-1 (merge solo per la PR della domanda), R-888MV-1/2.

- Limite dichiarato (verifica esterna #414 V-2): un numero sentito male a voce annulla la richiesta sbagliata, senza conferma (si riapre a mano togliendo `annullata`).
- Verifica esterna #414 V-4 COSMETICA: gli esiti si credono sulla parola dell'autore ammesso; il merge vero lo decide §10 (F4/F5).
- Note minori #887-MV: «annulla la richiesta numero dodici per favore» va al modello; «annulla la richiesta di.» riceve la risposta fissa.
- Chiuse da F3b: R-873MV-1 per la voce (frase solo con parti fisse), R-884MV-1 (file dei letti a voce con un solo scrittore), R-884MV-2 (test), ve #412 V-2 (avviso «scrivimi o dimmi», annullo dai vocali), bot #412 V-1 (sospesi scartati tolti).
- Cosmetiche #885-MV: due richieste a voce in parallelo possono ridire un esito una volta; file dei letti illeggibile → si ridicono al massimo 5 esiti.

- Verifica esterna #412 V-1 BASSA del bot (commento modificato non riletto): regola per F5, un ESITO è sempre un commento nuovo (nel docstring).
- R-881MV-1 BASSA — un commento cancellato fra la lettura della pagina N e della N+1 fa perdere il primo della pagina N+1 (serve un arretrato di più pagine: raro).
- R-881MV-2 COSMETICA — rilettura inutile con commenti multipli esatti di 100; ⪡⪢ ⋘⋙ non coperte nelle citazioni.
- R-877MV-2 COSMETICA — virgolette simili non tutte coperte (in parte chiusa da F3).
- Bot della #411: V-1 BASSA (§0 del suo handoff fermo a #874-MV), V-2 COSMETICA (descrizione, aggiornata).
- Classificatore del bot (`scripts/bot_esito.py` `_gravita_nel_testo`): falso rosso sulla #411 per una parola di gravità dentro una citazione; macchina del bot, decide l'operatore.
- R-870M-1 BASSA — numeri di review doppi fra chat (da qui suffisso -MV).
- Cosmetica U+200D — emoji composte spezzate.
