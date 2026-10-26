# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-25 sera / 26 — Accensione del cervello forte e chiusura delle note della #269 (chat Motore)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #269 (https://github.com/Gasss23/Gas/pull/269): chiesto esplicitamente dall'operatore in sessione («e mergia 269»). Numero e URL dalla risposta dello strumento GitHub (`merge_pull_request` → 405 «Pull Request has merge conflicts» col main 1212a17); `gh` nel cloud non è autenticato. Conflitti risolti col merge 255218f; il merge lo esegue l'agente a CI e verifica-bot verdi.
2. Sul Mac: `GAS_CLAUDE_CLI=1` nel `.env`, poi `python3 gas.py doctor`.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 0 — Esito della PR #266**: `FATTA` — già mergiata dall'operatore, bot success, CI verde.
- **Fetta 1 — Prova del login sul Mac (R-496-3)**: `FATTA` — 25: login scaduto («OAuth session expired»); 26, dopo `/login` dell'operatore: `ok 0.007764`.
- **Fetta 2 — Accensione del forte**: `FATTA` — note di #265 chiuse, login scaduto chiaro, `cervello: forte` nel catalogo, `/forte` nel terminale, setup del Mac.
- **Fetta 3 — Correzioni della verifica esterna #269**: `FATTA` — merge di main (V-1), V-2, V-3, V-4; review #515.
- **Fetta 4 — Correzioni del bot #269 (verifica-bot failure su 895f329)**: `FATTA` — V-1 MEDIA `/forte` fail-closed (`prefisso_forte`), V-2 login in testo semplice, V-4 test della ripresa; V-5 numero del kernel spiegato in §5; review #516 APPROVATO.
- **Fetta 5 — R-ve269-1, R-ve269-2 e COSMETICA del bot #269 (26 ottobre)**: `FATTA` — `/forte` da Telegram e voce, chiave del catalogo scritta male → compito saltato, doc del login; review #517 → #518 APPROVATO.
- **Fetta 6 — V-1 verifica esterna #269 4° giro + merge di main #272 (26 ottobre)**: `FATTA` — chiave sconosciuta nel catalogo → compito saltato (scelta dell'operatore); review #519 APPROVATO CON RISERVE.
- **Fette 7–9 — attività di notte, 3 lezioni, backup iCloud**: `DEFERITA — azioni dell'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |   7 +++++++
 brains/claude_cli.py                |  30 ++++++++++++++++++++++++++++--
 brains/router.py                    |  21 ++++++++++++++++++++-
 gas.py                              |   7 ++++++-
 modules/notte/notte.py              |  34 ++++++++++++++++++++++++++++++++--
 modules/telegram/bot.py             |  11 ++++++++++-
 modules/voice/server.py             |  11 ++++++++++-
 reports/diff_sessione.md            |  18 +++++++++++++-----
 reports/handoff.md                  | n/d
 reports/r2_regole_abbonamento.md    |   8 ++++++++
 reports/stato_progetto.md           |   6 +++---
 reports/ultimo_report.md            |  39 +++++++++++----------------------------
 scripts/notte/catalogo_esempio.yaml |   4 ++++
 tests/test_unit_claude_cli.py       |  59 ++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 tests/test_unit_kernel.py           |  20 ++++++++++++++++++++
 tests/test_unit_notte.py            | 105 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voice_server.py     |  22 ++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile, riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
255218f Merge origin/main (PR #272) in feat/merge-automatico-z1xjx2 + V-1 ve #269: chiave sconosciuta nel catalogo → compito saltato
0d253e1 docs(fine-task): report della chiusura di V-1/V-2 della verifica esterna #269 e della prova del login
4d09301 fix(R2): /forte anche da Telegram e voce, chiave cervello scritta male fa saltare il compito (ve #269)
384eab4 chore(revisore): memoria review #518 — APPROVATO
ace3ad3 chore(revisore): memoria review #517 — APPROVATO CON RISERVE
5e044f5 docs(fine-task): report dopo le correzioni del bot #269
7e1f520 fix(R2): /forte fail-closed su ogni separatore, login scaduto anche in testo semplice (bot #269)
aa7ce20 chore(revisore): memoria review #516 — APPROVATO
895f329 docs(fine-task): report dopo merge di main e correzioni della verifica esterna #269
26ce319 Merge origin/main in feat/merge-automatico-z1xjx2 (PR #269) + correzioni verifica esterna #269
51d2a6b docs(fine-task): report dell'accensione del cervello forte (PR #269)
1717413 feat(R2): accensione del cervello forte — login scaduto chiaro, cervello: forte nel catalogo notturno, /forte nel terminale
c0917bb chore(revisore): memoria review #512 — APPROVATO
861b33a chore(revisore): memoria review #511 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 1717413 — due giri (#511, #512); commit 26ce319 — review #515; commit 7e1f520 — review #516; commit 4d09301 — review #517 e #518; commit 255218f — review #519 sullo stesso diff staged (il secondo sul delta che chiude le riserve del primo).

### Review #511 (integrale)

## VERDETTO: APPROVATO CON RISERVE

Ho letto le tre fonti obbligatorie: CLAUDE.md (§5, §8, §9), la memoria del revisore (ultima riga #510) e la voce «RIPARTENZA chat Motore (25 ottobre sera)» di reports/stato_progetto.md. La fetta chiude il punto 2 di quella voce. Non c'è slicing della history, non c'è simulazione di output dei tool, il cap di 10 iterazioni e `_get_window` restano intatti. Ho rilanciato `tests/test_unit_claude_cli.py` e `tests/test_unit_notte.py`: 181 passed.

**Elementi del diff esaminati**
- brains/claude_cli.py:339 — se `result` o stderr contengono un segnale di login, l'errore diventa «login dell'abbonamento scaduto o mancante». Rischi esaminati: testo di Claude nel log, falso QUOTA, costo perso. Esito: ok. Il messaggio non contiene testo della CLI, non ha il prefisso 429, e il costo arriva lo stesso perché il ramo `except RuntimeError` mette `_costo_dati`. Riserva R-511-1 sotto.
- brains/claude_cli.py:219 — entrata e uscita vengono limitate a [0, `_TOKEN_MASSIMI`] prima della stima. Rischi esaminati: overflow e valori negativi. Sondato a mano: 10**400 → 90000.0 (≤ `_COSTO_MASSIMO`), -10**400 e 0 → pavimento 0.0075, 10**9+1 → 90000.0. Esito: ok. COSMETICA: il `max(0, …)` alla riga 221 ora è ridondante.
- modules/notte/notte.py:200 — con un valore di `cervello` diverso da `forte`, compreso `""`, il compito viene saltato con un avviso (fail-closed). Un valore `null` vale come campo assente. Esito: ok.
- modules/notte/notte.py:266 — `cervello="forte"` arriva a `run_turn` solo se presente, quindi i kernel finti con `run_turn(prompt)` restano compatibili. Ho controllato la ripresa R7 (cioè il rilancio dei compiti rimasti a metà dopo un crash): `_ordina_riprese` costruisce le voci con `{**c, ...}`, quindi il campo `cervello` non si perde e un compito ripreso non finisce ai modelli gratuiti. Esito: ok.
- gas.py:6021 — prefisso «forte » nel terminale di Gas; `run_turn` accetta `cervello` (gas.py:4515). L'input è già passato da strip, quindi «forte» da solo va come prompt normale. Esito: ok, con la riserva R-511-2.
- tests/test_unit_notte.py:2177 — un caso con `forte`, uno con valore sbagliato e uno senza campo; controlla che a `run_turn` arrivino `{"cervello": "forte"}` e `{}`. Esito: ok.
- tests/test_unit_kernel.py:10966 — T99r fa passare la catena da `run_turn` con una CLI finta che riporta `total_cost_usd` 10**400: il conto va al massimo e il turno dopo viene fermato dal tetto con una sola chiamata alla CLI. Chiude V-1 bot #265. Esito: ok, ma non l'ho eseguito (vedi sotto).

**Riserve**
1. **R-511-1 BASSA**: il controllo del login viene prima di quello del limite, e il segnale `"oauth"` è largo. Un messaggio di limite raggiunto che cita «oauth», o un `result` di errore che riporta una conversazione sull'OAuth, diventerebbe un errore di login (KO) invece di QUOTA. Non manda niente ai modelli gratuiti, ma sbaglia la diagnosi. Correzione proposta: controllare prima `_prefisso_limite`, oppure restringere il segnale a «oauth session»/«oauth token».
2. **R-511-2 BASSA**: il prefisso «forte » prende anche frasi normali («forte questo risultato…») e le manda al cervello forte. Va verso il modello più forte, quindi nessun dato finisce ai gratuiti, ma consuma il tetto giornaliero. Basta dichiararlo nel setup oppure usare un prefisso meno ambiguo (es. «/forte»).

**Cosa NON ho verificato**
- Non ho eseguito la suite kernel (i 1041 PASS e T99r sono dichiarati, non riprodotti da me). T99r l'ho controllato solo leggendolo.
- Non ho verificato il comportamento reale della CLI `claude` col login scaduto: si vede solo sul Mac. Mi baso sulla risposta riportata nel task.
- Doc (`reports/r2_regole_abbonamento.md`, `scripts/notte/catalogo_esempio.yaml`) letta: coerente.

**Memoria**: ho aggiunto la riga #511 (con una lezione sui campi di catalogo da propagare nei percorsi di ripresa) in /home/user/Gas/.claude/agents/memoria_revisore.md. Ho lanciato `scripts/commit_memoria_revisore.sh`, che non ha stampato niente: il commit della memoria non l'ho controllato.

### Review #512 (integrale, ri-review del delta)

## VERDETTO: APPROVATO

Ri-review solo del delta staged dopo la #511: le due riserve BASSE e la COSMETICA sono chiuse, senza riserve nuove. Ho rilanciato claude_cli + notte: 182 passed. Nessun antipattern di CLAUDE.md §5 nel delta.

**Elementi del diff esaminati**
1. brains/claude_cli.py:340 — prima si controlla il limite (`_prefisso_limite`), solo dopo il login. Rischio esaminato: un messaggio di limite raggiunto che cita «oauth» trattato come login scaduto (KO invece di QUOTA). Esito: ok. Con un limite si arriva al raise con «429 », che resta QUOTA. Il messaggio di login continua a non contenere testo di Claude. **R-511-1 chiusa.**
2. brains/claude_cli.py:82 — i segnali di login sono ristretti a «oauth session» e «oauth token». Rischio esaminato: il login scaduto vero non viene più riconosciuto. Esito: ok. Il testo della prova sul Mac contiene sia «failed to authenticate» sia «oauth session», quindi `tests/test_unit_claude_cli.py` resta coerente. Il caso opposto lo copre il nuovo test `tests/test_unit_claude_cli.py:356` (`test_limite_con_oauth_resta_quota`): ok.
3. brains/claude_cli.py:221 — il `max(0, …)` ridondante è tolto dopo il clamp. Rischio esaminato: valori negativi. Esito: ok, il clamp alle righe 219–220 li porta già a 0. **COSMETICA chiusa.**
4. gas.py:6023 — il prefisso nel terminale di Gas ora è «/forte » e si taglia con `[7:]`. Rischi esaminati: frase normale mandata per sbaglio al forte, taglio sbagliato. Esito: ok. «/forte » è lungo 7 caratteri, e la doc in `reports/r2_regole_abbonamento.md` è allineata. **R-511-2 chiusa.**

**Cosa NON ho verificato**
- La suite kernel (1041 PASS) non l'ho rieseguita: il delta non tocca le parti che usa T99r.
- Non ho verificato la forma reale dei messaggi di limite della CLI `claude`: si vede solo sul Mac. I segnali restano un'euristica.

**Memoria**: riga #512 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con `scripts/commit_memoria_revisore.sh` (commit «chore(revisore): memoria review #512 — APPROVATO»). La riga #511 era già committata.

### Review #515 (integrale, merge di main + correzioni ve #269, commit 26ce319)

## VERDETTO: APPROVATO CON RISERVE

Ho letto prima CLAUDE.md (sezioni 1, 5, 8 e 10), reports/stato_progetto.md (in modo mirato) e .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
1. `modules/web/leggi.py:222` e `tests/test_unit_web_leggi.py:1054`: codice entrato da main. Rischio esaminato: una risoluzione del merge che altera il codice di main. Esito: ok. Il contenuto staged dei due file è identico a quello di MERGE_HEAD (stesso blob, `git rev-parse :f` contro `MERGE_HEAD:f`). `git diff MERGE_HEAD --cached --stat` non li elenca.
2. `modules/notte/notte.py:202`: V-2. Il controllo passa da `cervello is not None` a `"cervello" in v`. Così un campo `cervello:` presente ma vuoto o null (anche `~`) fa saltare il compito, invece di essere letto come «nessun vincolo» e finire ai cervelli gratuiti. Rischio esaminato: falsi salti e ordine dei controlli. Il controllo arriva dopo `attivo` e dopo il prompt, `v` è già verificato come dict, e una voce senza la chiave resta valida. Esito: ok. Prova col mutante: rimettendo `is not None`, `tests/test_unit_notte.py:2184` (voce `d` con `cervello:` vuoto) fallisce (1 failed). Ho ripristinato il file e non ci sono modifiche residue.
3. `gas.py:6023`: V-3. Se nel REPL si scrive solo «/forte», compare il messaggio d'uso e il ciclo riparte (`continue`), senza chiamare `run_turn`, quindi niente arriva ai gratuiti. Rischio esaminato: la variante «/forte » con lo spazio finale. Il prompt viene ripulito degli spazi (`.strip()` a `gas.py:6011`), quindi quel caso non può presentarsi. Il confronto ignora maiuscole e minuscole. Esito: ok, con la riserva R-515-1 sotto.
4. `brains/claude_cli.py:343`: V-4. Cambia solo il testo dell'errore di login («scaduto, mancante o non valido»), con la stessa eccezione e lo stesso punto in cui viene lanciata. Il controllo del limite resta prima di quello del login (chiusura di R-511-1 intatta). Esito: ok.
5. Merge, contro HEAD: i file del motore cambiano solo per le tre correzioni (`brains/claude_cli.py` 3 righe aggiunte e 2 tolte, `gas.py` 3 aggiunte, `modules/notte/notte.py` 2 aggiunte e 1 tolta). `tests/test_unit_kernel.py` e `tests/test_unit_claude_cli.py` sono invariati rispetto a HEAD. La memoria del revisore non perde nessuna riga, né rispetto a HEAD né rispetto a MERGE_HEAD. stato_progetto.md non perde righe di main: cambia solo la riga di intestazione, che main aveva aggiornato e il ramo ha unito. Non restano marcatori di conflitto e `git diff --cached --check` è pulito. Esito: ok.

Wall of Shame: nessun taglio diretto della cronologia, nessuna simulazione di output dei tool, nessun guardrail toccato (tetto di 10 iterazioni, `_get_window`).

**Finding**
- **R-515-1 BASSA**: nessun test copre il nuovo ramo del REPL «/forte» da solo (`gas.py:6023`), perché `main()` non è coperto dai test. Se qualcuno tolgo la riga, la regressione passerebbe inosservata. Proposta: un test con `input` finto, oppure spostare il riconoscimento di «/forte» in una piccola funzione testabile.
- **R-515-2 BASSA**: «/forte» seguito da un tab invece che da uno spazio (`gas.py:6026`) non viene riconosciuto e il messaggio, con «/forte» compreso, va alla cascata normale. È un input improbabile da tastiera; si chiude con `prompt.split(maxsplit=1)`.

**Cosa non ho verificato**
- Non ho rilanciato la suite kernel (1041) né l'intero pytest (2202): mi fido dei numeri che mi hai dato. Ho rilanciato solo notte e claude_cli: 182 passed.
- Non ho controllato i testi di reports/handoff.md, ultimo_report.md e diff_sessione.md: li hai presi dal ramo e verranno riscritti a fine task.
- Il comportamento reale di `claude -p` col login scaduto sul computer di Gas non è riproducibile qui.

**Nota operativa**: ho scritto in coda a `.claude/agents/memoria_revisore.md` la riga contatore #515 (chat Motore). `scripts/commit_memoria_revisore.sh` non ha committato perché c'è un merge in corso (`commit -o` non è permesso durante un merge). Lo script ha comunque chiuso con exit 0, come previsto. La riga è quindi modificata ma non in stage: fai `git add .claude/agents/memoria_revisore.md` prima di concludere il merge, e rilancia `bash scripts/segna_review_ok.sh` dopo l'add, così il segno di review corrisponde a quello che è in stage.

### Review #516 — verdetto RIEMESSO per il gate B (commit 7e1f520)

Il testo originale del #516 citava `gas.py` a una riga che non esiste più dopo 4d09301 (funzione spostata in `brains/router.py`); per la regola F-verdetto-ritoccato non è stato ritoccato: il revisore l'ha riemesso con lo stesso esito e citazioni valide. L'originale integrale è nel §4 di `reports/handoff.md` al commit 5e044f5.

## VERDETTO: APPROVATO

Questa è la riemissione del verdetto #516 per il gate B (`scripts/check_verdetto.py`): esito invariato, cambiano solo le citazioni, ora valide a HEAD (989b8fe). Dopo 4d09301 la funzione sta in brains/router.py. Non è una review nuova, quindi non ho aggiunto righe alla memoria.

Elementi esaminati (citazioni ricontrollate sul file attuale):
1. `brains/router.py:23` — `prefisso_forte` divide il testo con `split(None, 1)` (`brains/router.py:34`), quindi NBSP e tab contano come separatori. «/forte:x», «/fortezza x» e «/forte» nudo danno ("uso", ""), mai `run_turn`: è fail-closed. Il mutante `split(" ")` faceva fallire 2 test (NBSP e tab). Esito: ok.
2. `gas.py:6021` — il terminale chiama `prefisso_forte`; con "uso" stampa l'istruzione (`gas.py:6023`) e fa `continue` prima di `run_turn`. Il prompt arriva già ripulito con `strip()`. Chiude R-515-1 e R-515-2. Esito: ok.
3. `brains/claude_cli.py:327` — nel ramo «uscita non JSON» il limite viene controllato prima del login (coerente con R-511-1). Il login scaduto dà `_MSG_LOGIN` e il costo resta registrato (`brains/claude_cli.py:329`). Il ramo JSON usa lo stesso helper (`brains/claude_cli.py:356`). Esito: ok.
4. `tests/test_unit_notte.py:2220` — copre i 4 rami di `_ordina_riprese` e il passaggio fino a `run_turn` con `cervello: forte`. `tests/test_unit_notte.py:2215` fissa i casi del prefisso, con NBSP reale. Esito: ok.
5. `tests/test_unit_claude_cli.py:273` — il vecchio test ora usa stdout «errore inatteso»: il cambio è voluto ed è coperto da `tests/test_unit_claude_cli.py:371`. Esito: ok.

Test (della review originale): claude_cli + notte, 195 passed.

Rischi esclusi:
- Il terminale vero di `main()` con `input()` non l'ho eseguito: l'ho valutato solo leggendo il codice.
- Non ho indagato la differenza tra la suite kernel (1041) e la CI (1043).
- Lo spostamento in brains/router.py e l'uso da Telegram e voce (4d09301) appartengono alle review #517/#518 e non li ho rivalutati qui.

Finding: nessuno.

### Review #517 (integrale, commit 4d09301)

## VERDETTO: APPROVATO CON RISERVE

Review #517, sul diff staged del branch feat/merge-automatico-z1xjx2 (PR #269): 9 file, +124/-20. Le letture obbligatorie sono fatte (CLAUDE.md, stato_progetto per la parte #269, memoria). Lo spostamento di `prefisso_forte` non cambia il comportamento e chiude R-ve269-2. Il blocco nel catalogo è fail-closed e chiude R-ve269-1. Nessun antipattern del Wall of Shame: il diff non tocca la history e non simula tool. Il cap di 10 iterazioni e `_get_window` non sono toccati.

**Elementi esaminati**
- `brains/router.py:23`: `prefisso_forte` spostata dentro il router senza cambiare logica. L'ho provata a mano: «/forte» seguito da NBSP, da a capo o da tab va al forte. «/fortex» e «/forte» seguito solo da spazi danno «uso». «forte x» senza barra non è un prefisso e va come testo normale. Rischio esaminato: regressione o import circolare. Esito: ok (router importa solo typing).
- `gas.py:34`: importa la funzione dal router. `gas.prefisso_forte` resta valido: lo usa ancora `tests/test_unit_notte.py:2215`. `Tuple` serve ancora altrove in gas.py. Esito: ok.
- `modules/telegram/bot.py:753`: il prefisso viene letto dopo i comandi giro e `/clear` e prima del turno. «uso» risponde con l'istruzione e non lancia il turno. Senza prefisso chiama `run_turn(text)` senza argomenti nuovi, quindi i kernel finti dei test restano compatibili. Rischio esaminato: crash del loop. Esito: ok, tutto è dentro il try esterno di `_handle_update` (fail-safe §9). La firma `cervello: Optional[str]` di `run_turn` esiste in `gas.py:4516`.
- `modules/voice/server.py:150`: «uso» risponde 400, «forte» va al solo forte. Esito: riserva cosmetica, vedi R-517-2.
- `modules/notte/notte.py:211`: una chiave sconosciuta che somiglia a «cervello» fa saltare il compito; le altre chiavi danno solo un avviso. La chiave viene convertita con `str(k)` prima del confronto. Ho provato il riconoscimento su chiavi comuni: «cartella», «cancello», «modello», «note», «orario» non sono riconosciute; «cervelo», «servello», «cervo» sì (meglio un falso positivo che salta il compito che un forte perso). Limite: «brain» o «cerebro» non vengono riconosciute e passano con il solo avviso. Esito: ok, fail-closed.
- `brains/claude_cli.py:80`: il commento di `_SEGNALI_LOGIN` ora corrisponde al testo vero di `_MSG_LOGIN` («scaduto, mancante o non valido»). Anche la doc reports/r2_regole_abbonamento.md è allineata. Esito: ok.
- Test mirati notte + voce: 193 passed. Le suite complete dichiarate (kernel 1041 PASS, pytest 2222 passed) non le ho rilanciate.

**Finding**
1. R-517-1 (BASSA): il ramo `startswith("cerv")` di `_somiglia_cervello` (`modules/notte/notte.py:145`) non è coperto dai test. Ho provato a toglierlo e i test passano lo stesso (5 passed), perché difflib da solo prende tutti i casi del test. Basterebbe un caso come «cerv» o «cervo» nel parametrize, dove serve solo `startswith`.
2. R-517-2 (COSMETICA): la voce applica «/forte» anche al testo trascritto dall'audio, non solo all'API testo come dicono il commento e la doc. È innocuo, perché un «/forte» nudo dà 400 e non va ai gratuiti, ma il testo va allineato.
3. Nota (nessuna gravità): il riepilogo parla di un test Telegram con NBSP, ma il test Telegram copre solo «/forte» nudo e «/forte:x». L'NBSP è coperto solo dal test della funzione, `tests/test_unit_notte.py:2209`. Va corretto il riepilogo o aggiunto il caso.

**Rischio escluso**: non ho verificato il comportamento reale su Telegram e sul server voce con il forte attivo (`claude -p` dietro il login dell'abbonamento), perché in dev non si può riprodurre: mancano il Mac e il login. Non ho controllato il commento integrale della verifica esterna su GitHub: mi sono basato sulla descrizione del compito.

Memoria aggiornata: riga #517 in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola (ace3ad3). L'index del diff staged è intatto. Durante la prova sul catalogo ho modificato modules/notte/notte.py nel working tree e l'ho poi ripristinato: nessuna differenza non staged rimasta.

### Review #518 (integrale, ri-review del delta, commit 4d09301)

## VERDETTO: APPROVATO

Review #518, solo sul delta staged rispetto alla #517. Le due riserve sono chiuse e la mia nota 3 era sbagliata.

**Elementi esaminati**
- `tests/test_unit_notte.py:2265`: aggiunto «cervello_forte» ai casi del test. Rischio esaminato: il ramo `startswith("cerv")` di `_somiglia_cervello` (`modules/notte/notte.py:145`) non era coperto. Ho rifatto la prova togliendo quel ramo e ora il test fallisce (1 failed). R-517-1 chiusa, esito ok.
- `modules/voice/server.py:148`: il commento ora dice «testo o trascrizione», e anche reports/r2_regole_abbonamento.md (punto 5) dice «nella voce (testo o trascrizione)». Rischio esaminato: doc diversa da quello che fa il codice. R-517-2 chiusa, esito ok.
- `tests/test_unit_notte.py:2257`: la prima chiamata del test Telegram contiene davvero un NBSP: `cat -A` mostra i byte C2A0 tra «/forte» e «analizza». La nota 3 della #517 era una mia svista: avevo guardato il testo a video, dove l'NBSP sembra uno spazio.
- Test mirati (catalogo e Telegram): 24 passed. Nel working tree ho ripristinato modules/notte/notte.py dopo la prova.

**Rischio escluso**: non ho rilanciato le suite complete del kernel e di pytest, perché il delta riguarda solo un caso di test e due testi. Resta non verificato anche il comportamento reale del forte su Telegram e sulla voce col login dell'abbonamento, che in dev non si può riprodurre.

Nota: nel working tree c'è una modifica non staged a reports/stato_progetto.md (2 righe), che non viene da me.

Memoria: riga #518 in /home/user/Gas/.claude/agents/memoria_revisore.md, committata (384eab4), con una lezione nuova: per i caratteri invisibili (NBSP, tab) controllare i byte, non il testo a video.

### Review #519 (integrale, merge di main + V-1 ve #269, commit 255218f)

## VERDETTO: APPROVATO CON RISERVE

Ho letto le tre fonti obbligatorie: CLAUDE.md (sezione 5), la parte di reports/stato_progetto.md su R2 e #269, e la coda della memoria del revisore (#511–#518).

**Elementi del diff che ho controllato**
- `modules/notte/notte.py:211` — ogni chiave diversa da nome, prompt, attivo e cervello fa saltare il compito. Il suggerimento «forse 'cervello'?» compare solo se la chiave gli somiglia.
  - Rischio controllato: che un vincolo scritto male mandi il compito ai modelli gratuiti, o che una chiave non testuale faccia crashare.
  - Prove che ho fatto: una chiave numerica `1` fa saltare il compito con un avviso, senza eccezioni. `cervello: forte` viene tenuto. Ho tolto il `continue` per controllare che i test se ne accorgano: 6 test falliscono, quindi il cambio è coperto. Poi ho rimesso il file com'era.
  - Esito: ok.
- `tests/test_unit_notte.py:2265` — il test ora copre tre casi: la chiave simile a «cervello» fa saltare il compito col suggerimento; `brain: forte` fa saltare il compito senza «forse»; il compito pulito resta.
  - Rischio controllato: che il test non distingua i due rami dell'avviso.
  - Esito: ok. I test della notte danno 173 passed.
- `scripts/notte/catalogo_esempio.yaml:9` e `reports/r2_regole_abbonamento.md:37` — la documentazione è allineata alle quattro chiavi valide. Esito: ok.
- Merge, controllo di contesto:
  - `git diff MERGE_HEAD --cached --stat` non elenca `modules/web/leggi.py` né `tests/test_unit_web_leggi.py`, quindi sono identici a main (MERGE_HEAD).
  - `git diff HEAD --cached --stat` elenca come file di motore solo notte e test_notte. Le nostre modifiche a brains, gas.py, telegram, voce e ai relativi test sono quindi intatte.
  - Ho confrontato riga per riga la memoria nell'indice con HEAD e con MERGE_HEAD: 0 righe perse da entrambe le parti.
  - Esito: ok.

**Finding**
1. **R-519-1 (COSMETICA):** in `reports/stato_progetto.md`, alla voce 2 di «Prossimi passi», c'è ancora scritto «Resta 👤: rifare `/login` sul Mac, prova del login». La voce 1, appena aggiornata, la dà già riuscita il 26 ottobre (`ok 0.007764`). Basta togliere quelle due parti alla fine del task.
2. **Nota BASSA, preesistente e non bloccante:** nello stesso file la voce aperta «R2 via B» dice ancora «nessun chiamante passa `cervello="forte"`», ma ora lo passano il catalogo notturno e `/forte`. Da allineare quando si aggiorna lo stato.

Non ci sono slicing della cronologia, simulazioni di tool o eccezioni non gestite nei provider. I guardrail non sono toccati.

**Cosa non ho verificato**
- Non ho rilanciato le suite intere (kernel 1041 e pytest 2241); ho eseguito solo i test della notte. Per le suite intere mi baso sui numeri che hai dichiarato.
- Non ho provato un vero giro notturno sul Mac con il report del mattino: non si può riprodurre in dev.
- Un compito con `attivo: false` e una chiave sconosciuta viene ignorato senza avviso. Succedeva già prima e quel compito non gira comunque, quindi va bene.

**Memoria:** ho aggiunto la riga #519 in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` (nessuna lezione nuova). La lascio modificata e non in stage, come mi hai chiesto per via del merge in corso, quindi non ho lanciato `commit_memoria_revisore.sh`.

## §5 DELTA TEST DEL MOTORE

- Kernel: 1040 → 1041 PASS (T99r nuovo), 0 FAIL. Blocco reale: `=== RIEPILOGO: 1041 PASS, 0 FAIL ===`
- `tests/test_unit_claude_cli.py` + `tests/test_unit_notte.py`: 182 passed (2 test nuovi in claude_cli, 1 in notte; 1 modificato).
- Dopo il merge di main e le correzioni: kernel `=== RIEPILOGO: 1041 PASS, 0 FAIL ===`; `python3 -m pytest -q tests`: `2202 passed, 1 skipped in 198.40s (0:03:18)`.
- Dopo le correzioni del bot (7e1f520): kernel `=== RIEPILOGO: 1041 PASS, 0 FAIL ===`; `python3 -m pytest -q tests`: `2215 passed, 1 skipped in 204.14s (0:03:24)`; claude_cli + notte 195 passed.
- Dopo la fetta del 26 (4d09301): kernel `=== RIEPILOGO: 1041 PASS, 0 FAIL ===`; `python3 -m pytest -q tests`: `2222 passed, 1 skipped in 194.31s (0:03:14)`.
- Dopo 255218f: kernel `=== RIEPILOGO: 1041 PASS, 0 FAIL ===`; `python3 -m pytest -q tests`: `2241 passed, 1 skipped in 182.64s (0:03:02)`.
- V-5 bot #269: in CI il kernel conta 1043 PASS (0 FAIL) su 895f329, in locale nel cloud 1041 (0 FAIL): differenza d'ambiente già vista sulla #263, causa non indagata.

## §6 STATO CI

`gh` nel cloud non è autenticato: check letti con lo strumento GitHub sulla PR #269.
- 0d253e1 → `unit-suite` success, `handoff-check` success, `verifica-bot` neutral.
- 5e044f5 → `unit-suite` success, `handoff-check` success, `verifica-bot` neutral (PR sulla macchina del bot: decide l'operatore).
- 895f329 → `unit-suite` success, `handoff-check` success, `verifica-bot` failure (V-1 MEDIA, chiusa in 7e1f520).
- 51d2a6b → `unit-suite` success, `handoff-check` success.
- 7e1f520, aa7ce20, 26ce319, 1717413, c0917bb, 861b33a, ace3ad3, 384eab4 → nessuna run propria letta (pushati insieme ad altri: testati solo nell'albero di testa del push).
- 4d09301 → nessuna run propria (testato nell'albero di 0d253e1).
- 255218f e commit di fine-task → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-515-1/2, R-517-1/2, R-ve269-1/2, V-1 ve #269 4° giro, R-519-1 e la COSMETICA del bot #269: CHIUSE.
- V-1 BASSA bot #269 (ultimo giro): «/forte@NomeBot richiesta» su Telegram non riconosciuto (fail-closed: istruzione d'uso). Aperta.
- V-3 COSMETICA ve #269: «/forte» + solo carattere invisibile va al forte. Aperta.
- V-4 COSMETICA ve #269: differenza kernel 1041 locale / 1043 CI non indagata. Aperta.
- Limite dichiarato: un prefisso scritto male («/frote») va come testo normale.
