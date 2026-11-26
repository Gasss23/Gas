# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-26 — Mani alla voce: decisioni dell'operatore nel piano + F2-bis (riserve basse di F2), PR #411

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #411 (https://github.com/Gasss23/Gas/pull/411). Numero e URL dall'output di `gh api repos/Gasss23/Gas/pulls -X POST` (qui `gh pr` non è disponibile). Revisore #874-MV APPROVATO: se il bot dà APPROVATO pulito mergia l'agente (CLAUDE.md §10), altrimenti decide l'operatore via M1.

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #409**: `FATTA` — 17cba359, col sì dell'operatore via M1.
- **Decisioni dell'operatore nel piano**: `FATTA` — `reports/mani_voce_piano.md` §4bis e §5 (F1 rifiutata, compensazioni).
- **F2-bis — riserve basse di F2**: `FATTA` — 887fcc0d; revisore #873-MV → #874-MV APPROVATO; 79 test.
- **Correzione dopo la verifica esterna (#411 V-1)**: `FATTA` — 93f7650f, ogni riga RISERVA conta; revisore #875-MV → #876-MV APPROVATO.
- **Correzione dopo il bot (head e6d30207)**: `FATTA` — 80d1e2b5; check del bot falso rosso (parola di gravità della mia frase citata in un finding basso), finding bassi corretti; revisore #877-MV → #878-MV APPROVATO CON RISERVE.
- **F3 — avviso subito, annullo, lettura degli esiti**: `DEFERITA — prossima fetta`.
- **F4 — «mergia N» / «no N» da Telegram**: `DEFERITA — dopo F3`.
- **F5 — esecutore nel cloud**: `DEFERITA — dopo F4`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 ++++++
 modules/sviluppo/esiti.py          | 136 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------
 reports/diff_sessione.md           |  13 ++++++------
 reports/handoff.md                 | n/d
 reports/mani_voce_piano.md         |  64 ++++++++++++++++++++++++++++++++++++++++++++--------------
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  31 ++++++++++-------------------
 tests/test_unit_esiti.py           | 125 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
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

Commit motore 887fcc0d: verdetti integrali #873-MV (primo giro) e #874-MV (secondo giro, dopo la correzione di R-873MV-2 nello stesso diff staged). Commit motore 93f7650f (dopo la verifica esterna #411 V-1): verdetti #875-MV e #876-MV, in fondo a questa sezione. Commit motore 80d1e2b5 (dopo il bot su e6d30207): verdetti #877-MV e #878-MV, dopo #876-MV. NB: nel testo di #876-MV, elemento 1, l'esempio delle riserve conteneva un carattere U+200B vero (invisibile); qui è scritto come `<U+200B>` per non far fallire il bot («controlli bidi»). È l'unica differenza dal verdetto emesso; sostanza ed esito invariati.

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

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_esiti.py`: 63 → 79 test (887fcc0d) → 88 test (93f7650f) → 101 test (80d1e2b5), tutti passati (`python -m pytest -q tests/test_unit_esiti.py` → `101 passed in 0.22s`). Il file gira in CI nel passo «Run esiti suite» di `unit-suite`.
- Nessun altro file del motore toccato: il modulo non è collegato a nulla.

## §6 STATO CI

Da `gh api repos/Gasss23/Gas/commits/<sha>/check-runs` (`gh run list` non è disponibile qui):

- 03d3f4c3, a853b27f, 887fcc0d, 40decd9b: nessuna run su questi SHA (pushati insieme a e01e0c55).
- e01e0c55: verifica-bot failure («controlli bidi»: carattere invisibile vero citato dal bot).
- 89e57942, 1382ec22, 93f7650f, 2ee37f96: nessuna run conclusa su questi SHA (superati da e6d30207; il bot su 2ee37f96 è stato annullato perché la head è cambiata).
- e6d30207: verifica-bot failure, falso rosso del classificatore (verdetto testuale APPROVATO CON RISERVE con soli finding bassi e cosmetici).
- 2f99753e, 02592fd1, 80d1e2b5 e il commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-873MV-1 BASSA — a voce le «» non si sentono: un riassunto ostile può farsi sentire come domanda di merge. In F3 «mergia N» vale solo per la PR di un esito con la domanda vera sulla stessa issue.
- Chiuse in 93f7650f: verifica esterna #411 V-1 BASSA (riga RISERVA illeggibile scartata in silenzio) e R-875MV-1 BASSA (riga RISERVA vuota o di soli spazi Unicode). Verifica esterna #411 V-2 COSMETICA (numero_richiesta=True stampa #1): chiamante fidato.
- R-877MV-2 COSMETICA — virgolette simili a «» non tutte coperte (︽︾, ⸨⸩, << >>); il confine vero è il lettore del comando in F3.
- Classificatore del bot (`scripts/bot_esito.py` `_gravita_nel_testo`): legge le parole di gravità anche dentro citazioni in un finding basso (falso rosso su e6d30207). È la macchina del bot: decide l'operatore.
- R-870M-1 BASSA — numeri di review doppi fra chat parallele: da qui le review di questa chat hanno il suffisso -MV.
- Cosmetica #874-MV — con `numero_richiesta=True` il ripiego stampa «#True» (chiamante fidato).
- Cosmetica 5 — commenti scartati senza log (in F3). Cosmetica U+200D — emoji composte spezzate.
