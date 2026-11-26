# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-26 — Mani alla voce F3: avviso subito alla richiesta, «annulla richiesta N», esiti dalle issue su Telegram, PR #412 (contiene anche la PR #411, F2-bis)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #411 (https://github.com/Gasss23/Gas/pull/411), F2-bis: CI e bot verdi, verdetto del bot APPROVATO CON RISERVE (V-1 BASSA: §0 del suo handoff fermo a #874-MV, l'ultimo revisore è #878-MV APPROVATO CON RISERVE; V-2 COSMETICA: descrizione, aggiornata): decide l'operatore.
2. Merge della PR #412 (https://github.com/Gasss23/Gas/pull/412), F3, DOPO la #411. Numero e URL dall'output di `gh api repos/Gasss23/Gas/pulls -X POST` (qui `gh pr` non c'è). Revisore #881-MV APPROVATO CON RISERVE: decide l'operatore (CLAUDE.md §10).
3. Sul Mac, dopo il merge della #412: `GAS_RICHIESTE_AUTORI=<login GitHub di chi scrive gli esiti>` nel `.env`, poi riavvio del bot Telegram. Senza, Gas non legge nessun esito (fail-closed).

---

## §1 SCOPE & ESITO FETTE

- **F2-bis (PR #411)**: `FATTA` — commit 887fcc0d, 93f7650f, 80d1e2b5; revisore #873-MV … #878-MV (dettaglio nel §4).
- **F3 — avviso, annullo, esiti su Telegram**: `FATTA` — 6fce9e43; revisore #879-MV → #880-MV BOCCIATO → #881-MV APPROVATO CON RISERVE; 197 test, kernel 1210 PASS.
- **F3b — esiti letti a voce**: `DEFERITA — prossima fetta`.
- **F4 — «mergia N» / «no N» da Telegram**: `DEFERITA — dopo F3b`.
- **F5 — esecutore nel cloud**: `DEFERITA — dopo F4`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  13 ++++++++++
 .github/workflows/ci.yml           |   8 ++++++
 .gitignore                         |   2 ++
 gas.py                             |  22 +++++++++++++++-
 modules/sviluppo/cassetta.py       | 437 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 modules/sviluppo/esiti.py          | 151 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------
 modules/sviluppo/richieste.py      |  20 ++++++++++++---
 modules/telegram/bot.py            |  29 +++++++++++++++++++++
 reports/diff_sessione.md           |  22 +++++++++-------
 reports/handoff.md                 | n/d
 reports/mani_voce_piano.md         |  65 ++++++++++++++++++++++++++++++++++++-----------
 reports/stato_progetto.md          |   4 +--
 reports/ultimo_report.md           |  36 +++++++++++---------------
 tests/test_unit_cassetta.py        | 497 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_esiti.py           | 125 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------
 tests/test_unit_kernel.py          |  29 +++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
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

Commit motore 887fcc0d: verdetti integrali #873-MV (primo giro) e #874-MV (secondo giro, dopo la correzione di R-873MV-2 nello stesso diff staged). Commit motore 93f7650f (dopo la verifica esterna #411 V-1): verdetti #875-MV e #876-MV, in fondo a questa sezione. Commit motore 80d1e2b5 (dopo il bot su e6d30207): verdetti #877-MV e #878-MV, dopo #876-MV. Commit motore 6fce9e43 (F3): verdetti #879-MV, #880-MV (BOCCIATO) e #881-MV, in fondo a questa sezione. NB: nel testo di #876-MV, elemento 1, l'esempio delle riserve conteneva un carattere U+200B vero (invisibile); qui è scritto come `<U+200B>` per non far fallire il bot («controlli bidi»). È l'unica differenza dal verdetto emesso; sostanza ed esito invariati.

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

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_esiti.py`: 63 → 101 (PR #411) → 103 test con F3 (virgolette Pi/Pf e apostrofi).
- `tests/test_unit_cassetta.py`: nuovo, 71 test. Comando: `python -m pytest -q tests/test_unit_cassetta.py tests/test_unit_esiti.py tests/test_unit_richieste.py` → `197 passed in 0.29s`.
- `tests/test_unit_kernel.py` (script): T100c e T100d nuovi (round-trip §7 con l'avviso riuscito e fallito); `=== RIEPILOGO: 1210 PASS, 0 FAIL ===`.
- CI: passo nuovo «Run cassetta suite» in `.github/workflows/ci.yml`.

## §6 STATO CI

- Commit della PR #411 (fino a 5af3680e): sul head 5af3680e unit-suite, handoff-check e verifica-bot success (verdetto del bot APPROVATO CON RISERVE).
- 020059f7, f692ce6d, a518d9e5, 6fce9e43 e il commit di fine-task: run non ancora disponibile alla scrittura dell'handoff (`gh run list` non è disponibile qui; si legge con `gh api`).

## §7 RISERVE APERTE

- R-881MV-1 BASSA — un commento cancellato fra la lettura della pagina N e della N+1 fa perdere il primo della pagina N+1 (serve un arretrato di più pagine: raro).
- R-881MV-2 COSMETICA — rilettura inutile con commenti multipli esatti di 100; ⪡⪢ ⋘⋙ non coperte nelle citazioni.
- R-873MV-1 BASSA — a voce le «» non si sentono: in F4 «mergia N» varrà solo per la PR ricordata da F3 (`cassetta.domanda_aperta`).
- R-877MV-2 COSMETICA — virgolette simili non tutte coperte (in parte chiusa da F3).
- Bot della #411: V-1 BASSA (§0 del suo handoff fermo a #874-MV), V-2 COSMETICA (descrizione, aggiornata).
- Classificatore del bot (`scripts/bot_esito.py` `_gravita_nel_testo`): falso rosso sulla #411 per una parola di gravità dentro una citazione; macchina del bot, decide l'operatore.
- R-870M-1 BASSA — numeri di review doppi fra chat (da qui suffisso -MV).
- Cosmetica U+200D — emoji composte spezzate.
