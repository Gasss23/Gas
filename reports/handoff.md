# HANDOFF — Dossier di fine sessione

**Sessione:** 25 novembre 2026 — R7 fetta 4 bis: tetto di tempo duro del giro di notte (sotto-chat di M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR # (https://github.com/Gasss23/Gas/pull/), etichetta «verifica». Tocca il motore: merge autonomo solo con verdetto testuale del bot APPROVATO senza finding V-x, CI verde e niente conflitti; con riserve la PR resta aperta e il «mergia» lo chiede M1 all'operatore.
2. Merge della PR #402 (fetta 4, sottofondo): pronta, stesso flusso.

Numero della PR preso dall'output di `gh api repos/Gasss23/Gas/pulls` (POST, creazione): `` (`gh pr` non disponibile in questo ambiente, solo REST).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 4 bis R7 — tetto di tempo duro del giro di notte**: FATTA. Timer a GAS_NOTTE_MAX_SEC_GIRO + 300 s: avviso «INTERROTTO» e arresto del processo; un solo avviso tra timer e fine giro; nome del compito appeso nel log; attesa limitata a 30 giorni. Review #866-R7 → #867-R7.
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA — prossima PR.

---

## §2 GIT DIFF --STAT (sessione)

```
.claude/agents/memoria_revisore.md |   3 +++
 modules/notte/notte.py             |  78 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  15 +++++----------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  60 +++++++++++-------------------------------------------------
 tests/test_unit_notte.py           | 110 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
76655c0a feat(notte): R7 fetta 4 bis — tetto di tempo duro del giro di notte
336e9064 chore(revisore): memoria review #867 — APPROVATO CON RISERVE
8b7bea3b chore(revisore): memoria review #866 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 76655c0a (motore): review #866-R7 sul primo staged e #867-R7 dopo le correzioni di R-866R7-2/3/4. Incollati integrali.

### Review #866-R7

## VERDETTO: APPROVATO CON RISERVE

Review #866-R7. Branch `claude/r7-tetto-duro-notte`, diff staged sopra b7182a7c: 2 file, +109/−0, sha256 del diff fe1bd29b. Ho letto CLAUDE.md, la memoria del revisore (comprese le riserve #852-R7 e #853-R7 della PR #402, gemella sul sottofondo) e lo stato del progetto, quest'ultimo solo nelle parti su R7.

**Cosa ho provato**
- **Suite**: `pytest tests/test_unit_notte.py` dà 235 passed.
- **Prova reale**: l'ho fatta in un processo separato. Ho messo MIN_SEC e MARGINE_DURO_S a 1 e GAS_NOTTE_MAX_SEC_GIRO=2, con un kernel finto che resta appeso e lancia due `sleep`.
  - Esito: rc 1 in 3 s.
  - Il messaggio «Giro notturno interrotto: tetto di tempo duro…» esce a schermo e nel log.
  - Il lock viene liberato: il giro successivo è partito subito.
  - Il compito appeso resta in `.gas_notte/in_corso.json` con tentativi 1, e il giro dopo lo riprende per primo.

**Elementi del diff esaminati**
1. `modules/notte/notte.py:993` — `_arma_tetto_giro`: `threading.Timer` demone. Rischio esaminato: overflow del timeout. Esito: riserva (R-866R7-3).
2. `modules/notte/notte.py:1008` — `_giro_scaduto`: log, avviso Telegram «INTERROTTO» col testo fisso, poi `_termina_giro` nel finally. Rischi esaminati: un'eccezione nell'avviso non deve impedire l'arresto (ok, provato dal test `tests/test_unit_notte.py:2898`); testo del modello nel messaggio (ok: solo la costante TETTO_DURO_NOTTE).
3. `modules/notte/notte.py:1105` — il timer si arma dopo `max_giro`, a max_giro + 300 s. Rischio esaminato: le fasi prima del ciclo restano scoperte. Esito: ok, sono trascurabili (catalogo e riprese, niente modello).
4. `modules/notte/notte.py:1189` — `cancel()` nel finally, prima di chiudere il lock e prima del riepilogo Telegram. Rischio esaminato: corsa con la fine normale. Esito: riserva (R-866R7-2).
5. `modules/notte/notte.py:1001` — `_termina_giro` = `os._exit(1)`. Rischi esaminati:
   - flock: ok, provato.
   - in_corso.json: ok, la scrittura è atomica con tmp + replace.
   - figli: riserva (R-866R7-1).
6. `tests/test_unit_notte.py:2873` e `tests/test_unit_notte.py:2885` — il timer viene tolto sia a fine giro sia nel giro che si rompe. `tests/test_unit_notte.py:2919` prova un timer vero. Esito: ok.

**Finding**
- **R-866R7-1 BASSA — i figli sopravvivono a `os._exit`.** L'ho provato: sia `sleep` nello stesso gruppo sia `sleep` con sessione propria restano vivi.
  - Sotto launchd il gruppo del job dovrebbe morire alla chiusura (non verificato sul Mac). Però `claude -p` (`brains/claude_cli.py:428`) e il browser (`modules/web/browser.py:496`) hanno una sessione propria e sopravvivono comunque.
  - Un `claude -p` rimasto orfano può sovrapporsi al giro successivo, perché il lock è già libero.
  - La docstring di `_termina_giro` non lo dice. Va dichiarato, oppure va fatto un killpg dei gruppi noti.
- **R-866R7-2 BASSA — nessuna mutua esclusione tra il timer e la fine normale.** È la stessa riserva R-852R7-2 della PR #402.
  - Se il timer scatta tra la fine del ciclo e il `cancel` (`modules/notte/notte.py:1189`), arrivano sia «INTERROTTO» sia il riepilogo, oppure `os._exit` cade a metà riepilogo.
  - `cancel()` non ferma un timer che è già dentro l'invio Telegram (fino a 15 s per ID). Il thread principale può quindi chiudere e mandare anche il riepilogo normale.
  - La finestra è stretta.
- **R-866R7-3 BASSA — tetto duro spento in silenzio con valori enormi.** È la stessa riserva R-852R7-3.
  - Con GAS_NOTTE_MAX_SEC_GIRO ≥ ~9,2e9 il thread del Timer va in OverflowError e il tetto duro si spegne senza dirlo. L'ho provato: 9,0e9 regge, 9,3e9 muore con «timestamp out of range».
  - `_env_secondi` (`modules/notte/notte.py:248`) non ha un tetto alto.
  - Correzione: `min(secondi, limite)` in `_arma_tetto_giro`. Attenzione a R-853R7-1: se si tronca il tempo, il messaggio non deve diventare falso.
- **R-866R7-4 BASSA — il tetto per compito resta morbido, e i compiti ripresi partono per primi.**
  - Un compito che si appende sempre brucia l'intera notte (2 h 05) per MAX_TENTATIVI = 3 notti di fila. Gli altri compiti in quelle notti non girano.
  - Né il messaggio «INTERROTTO» né la riga di log nominano il compito appeso. Il nome viene dal catalogo dell'operatore, non dal modello, quindi si può almeno scrivere nel log.
  - Il limite è dichiarato come tetto morbido, ma l'effetto «3 notti perse» non è scritto da nessuna parte.
- **COSMETICA**: l'invio Telegram dentro il timer non ha un tetto proprio. Il timeout di urlopen è per singola fase e non copre il DNS, quindi un avviso appeso ritarda `os._exit`. Correzione possibile: un secondo timer di sicurezza su `os._exit`.

**Cosa NON ho verificato**
- Il comportamento sotto launchd sul Mac (se il gruppo del job viene ucciso quando il job finisce): da qui non si riproduce.
- L'invio Telegram vero: l'ho spento con GAS_NOTTE_TELEGRAM=0 e mi sono affidato al test con `invia_notifica` finto.
- Nessun mutante sui test nuovi, per tempo.

**Memoria**: riga #866-R7 e una lezione nuova aggiunte in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole (8b7bea3b). Lo staging del diff è intatto.

**Note per te**
- Le riserve 1-3 coincidono con quelle già aperte sulla PR #402: conviene chiuderle insieme nelle due fette.
- Vanno tracciate in `reports/stato_progetto.md`.
- Il marcatore della review non l'ho creato io: lo crei tu con `bash scripts/segna_review_ok.sh`.

### Review #867-R7

## VERDETTO: APPROVATO CON RISERVE

Review #867-R7: secondo giro di #866-R7. Il diff staged è su `claude/r7-tetto-duro-notte`, sopra 8b7bea3b: 2 file, +188/−0, sha256 del diff f5efbcf6. Tre riserve su quattro sono chiuse e la quarta è dichiarata nel codice; resta aperta una riserva BASSA nuova.

**Riserve di #866-R7**

| Riserva | Esito | Dove |
|---|---|---|
| R-866R7-2 | chiusa | `modules/notte/notte.py:1014`, `modules/notte/notte.py:1020`, `modules/notte/notte.py:1222` |
| R-866R7-3 | chiusa | `modules/notte/notte.py:994`, `modules/notte/notte.py:122` |
| R-866R7-4 | chiusa per il log; limite delle 3 notti dichiarato | `modules/notte/notte.py:1155` |
| R-866R7-1 | dichiarata (figli non fermati) | docstring di `_termina_giro` |

**Cosa ho rifatto io**
- **Suite:** `pytest tests/test_unit_notte.py` passa (238 passed).
- **Prova reale**, in un processo separato con kernel appeso e Telegram spento:
  - rc 1 in 3 s;
  - nel log compare «tetto di tempo duro del giro superato: processo fermato (compito in corso: appeso)».
- **Mutanti: 4 su 4 uccisi** (lo staging è intatto). Ciascuno fa fallire un test r7f4:
  - `da_notificare` non azzerato nel finally;
  - il finally non prende il flag;
  - il timer ignora il flag;
  - il tetto dei 30 giorni tolto.

**Elementi del diff esaminati**
1. `modules/notte/notte.py:994` — `_arma_tetto_giro` limita l'attesa a `min(max(0, s), 30 giorni)`. Rischio esaminato: OverflowError nel thread del Timer. Esito: ok; lo prova `tests/test_unit_notte.py:2961` con 1e12.
2. `modules/notte/notte.py:1020` — `_giro_scaduto` controlla e alza il flag sotto lock prima di avvisare e chiudere. Rischio esaminato: un timer in ritardo dopo la fine del giro. Esito: ok, esce senza fermare il processo (seconda parte di `tests/test_unit_notte.py:2927`).
3. `modules/notte/notte.py:1222` — il finally fa `cancel`, poi prende il flag sotto lock. Se il timer è già partito, non manda il riepilogo e aspetta con `tetto_duro.join(60)` (`modules/notte/notte.py:1227`).
   - Rischio esaminato: corsa fra `cancel` e un timer già in attesa del lock. Esito: ok, chi prende il lock per primo vince.
   - Rischio esaminato: l'invio dell'avviso dura più dell'attesa. Esito: riserva R-867R7-1.
4. `modules/notte/notte.py:1155` — il nome del compito viene salvato nella guardia prima di segnarlo in in_corso.json. Rischio esaminato: testo non fidato nel log. Esito: ok, il nome viene dal catalogo dell'operatore. Vedi però la COSMETICA sul nome che resta dopo il ciclo.
5. `tests/test_unit_notte.py:2927` — il timer scatta mentre il compito gira: arriva un solo avviso, «INTERROTTO», e niente riepilogo. Poi un giro normale con un timer tardivo: il processo non si ferma. Esito: ok, e uccide i mutanti 1-3.

**Riserve nuove**
- **R-867R7-1 BASSA:** succede quando il timer ha già preso il flag e l'invio Telegram nel thread del timer dura più di 60 s (`tetto_duro.join(60)`, `modules/notte/notte.py:1227`; per esempio DNS appeso: il timeout di urlopen non lo copre).
  - Effetto: il finally ritorna con l'esito calcolato, anche rc 0, e lo spegnimento dell'interprete congela il thread demone.
  - Risultato: né «INTERROTTO» né riepilogo, cioè proprio il silenzio che V-1 bot #169 voleva evitare.
  - La finestra è stretta: serve lo scatto nella fase finale più Telegram lento.
  - Correzione possibile: dopo il join scaduto, rc 1 e `_termina_giro()` direttamente, oppure un join senza limite.
- **COSMETICA:** `guardia["compito"]` resta sull'ultimo compito anche dopo il ciclo. Se il blocco è nella fase finale (firme, stato del mattino), il log dice «compito in corso: X» con X già finito.
- **COSMETICA:** con GAS_NOTTE_MAX_SEC_GIRO oltre 30 giorni, «tetto duro superato» arriva a 30 giorni, cioè prima del tetto vero (analoga a R-853R7-1).

**Rischi non verificati**
- Il comportamento sotto launchd sul Mac (figli in sessione propria): non riproducibile qui.
- L'invio Telegram vero: provato solo con `_notifica_telegram` finto e GAS_NOTTE_TELEGRAM=0.
- La corsa reale fra due thread, con il timer che scatta durante il finally: verificata leggendo il codice e con il test sincrono, non con thread veri.

**Memoria:** ho aggiunto la riga #867-R7 a `/home/user/Gas/.claude/agents/memoria_revisore.md` e l'ho committata da sola (336e9064); nessuna lezione nuova.

**Cosa resta a te**
- Tracciare R-867R7-1 e le COSMETICHE in `reports/stato_progetto.md`.
- Creare il marcatore con `bash scripts/segna_review_ok.sh`: io non l'ho creato.

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_notte.py`: 230 → 238 (8 test nuovi), tutti verdi in locale: `238 passed in 5.22s`.
- `tests/test_unit_kernel.py` non rieseguito: il diff tocca solo `modules/notte/notte.py` e i suoi test. Il revisore ha fatto una prova reale con processo separato e kernel appeso (rc 1 in 3 s, messaggio nel log, lock liberato, compito in in_corso.json).

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura:

```
in_progress		feat(notte): R7 fetta 4 bis — tetto di tempo duro del giro di notte	CI	claude/r7-tetto-duro-notte	push	45651971850	58s	2026-11-25T16:14:02Z
completed	success	Voce: log chiari sul turno scartato e nome del modello sicuro	verifica-bot	fix/voce-log-e-modello	pull_request_target	45651349588	4m13s	2026-11-25T16:08:47Z
in_progress		docs(fine-task): report con le riserve del bot #407 chiuse (review #8…	CI	fix/voce-log-e-modello	push	45651347053	6m14s	2026-11-25T16:08:46Z
```

Run di questo branch (`gh api .../actions/runs?branch=claude/r7-tetto-duro-notte`, output reale):

```
45651971850 76655c0a CI push in_progress/null
```

Mappatura commit→run: 76655c0a è il commit di testa del primo push (run con head 76655c0a sopra, se presenti; verifica-bot parte con l'etichetta, messa dopo questo commit). 8b7bea3b e 336e9064 (memoria): nessuna run propria (pushati insieme). Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-867R7-1 BASSA — timer già partito e invio Telegram oltre 60 s (es. DNS appeso): il giro può finire senza «INTERROTTO» né riepilogo. Aperta.
- COSMETICHE #867-R7: il nome del compito resta dopo il ciclo (log «compito in corso» sbagliato se il blocco è nella fase finale); con GAS_NOTTE_MAX_SEC_GIRO oltre 30 giorni il tetto scatta a 30 giorni. Aperte.
- R-866R7-1 BASSA (dichiarata nel codice): figli `claude -p` e browser non fermati. Limite dichiarato: un compito sempre appeso consuma il giro per 3 notti. R-866R7-2/3/4: CHIUSE.
- PR #402 (sottofondo): riserve nel suo handoff e in `reports/stato_progetto.md`.
