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
- **F3 — avviso subito, annullo, lettura degli esiti**: `DEFERITA — prossima fetta`.
- **F4 — «mergia N» / «no N» da Telegram**: `DEFERITA — dopo F3`.
- **F5 — esecutore nel cloud**: `DEFERITA — dopo F4`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 ++
 modules/sviluppo/esiti.py          | 92 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------
 reports/diff_sessione.md           | 13 ++++++-------
 reports/handoff.md                 | n/d
 reports/mani_voce_piano.md         | 60 +++++++++++++++++++++++++++++++++++++++++++++++-------------
 reports/stato_progetto.md          |  4 ++--
 reports/ultimo_report.md           | 29 ++++++++---------------------
 tests/test_unit_esiti.py           | 65 ++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
40decd9b docs(mani-voce): decisioni dell'operatore del 26/11 nel piano; F1 rifiutata e compensazioni (avviso subito, annullo con 30 minuti, tetto di 2 al giorno)
887fcc0d fix(sviluppo): riserve basse di F2 chiuse prima di F3 (mani alla voce F2-bis)
a853b27f chore(revisore): memoria review #874 — APPROVATO
03d3f4c3 chore(revisore): memoria review #873 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore 887fcc0d: verdetti integrali #873-MV (primo giro) e #874-MV (secondo giro, dopo la correzione di R-873MV-2 nello stesso diff staged).

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

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_esiti.py`: 63 → 79 test, tutti passati (`python -m pytest -q tests/test_unit_esiti.py` → `79 passed in 0.17s`). Il file gira in CI nel passo «Run esiti suite» di `unit-suite`.
- Nessun altro file del motore toccato: il modulo non è collegato a nulla.

## §6 STATO CI

- 03d3f4c3, a853b27f, 887fcc0d, 40decd9b: nessuna run su questi SHA (pushati insieme al commit di fine-task).
- commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

CI non ancora verificata su questo ramo alla scrittura (`gh run list` non è disponibile qui; si legge con `gh api` dopo il push).

## §7 RISERVE APERTE

- R-873MV-1 BASSA — a voce le «» non si sentono: un riassunto ostile può farsi sentire come domanda di merge. In F3 «mergia N» vale solo per la PR di un esito con la domanda vera sulla stessa issue.
- R-870M-1 BASSA — numeri di review doppi fra chat parallele: da qui le review di questa chat hanno il suffisso -MV.
- Cosmetica #874-MV — con `numero_richiesta=True` il ripiego stampa «#True» (chiamante fidato).
- Cosmetica 5 — commenti scartati senza log (in F3). Cosmetica U+200D — emoji composte spezzate.
