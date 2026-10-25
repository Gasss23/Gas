# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-25 sera — Accensione del cervello forte (chat Motore)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #269 (https://github.com/Gasss23/Gas/pull/269). Numero e URL dalla risposta JSON dello strumento GitHub `create_pull_request` (`gh` nel cloud non è autenticato). Merge solo secondo CLAUDE.md §10.
2. Etichetta `verifica` già messa: attendere `verifica-bot` sull'ultimo commit.
3. Sul Mac: `/login` dell'abbonamento Max di Gas (il login era scaduto), prova del login, `GAS_CLAUDE_CLI=1` nel `.env` (`reports/r2_regole_abbonamento.md`).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 0 — Esito della PR #266**: `FATTA` — già mergiata dall'operatore, bot success, CI verde.
- **Fetta 1 — Prova del login sul Mac (R-496-3)**: `DEFERITA — login scaduto («OAuth session expired»), serve /login dell'operatore`.
- **Fetta 2 — Accensione del forte**: `FATTA` — note di #265 chiuse, login scaduto chiaro, `cervello: forte` nel catalogo, `/forte` nel terminale, setup del Mac.
- **Fetta 3 — Correzioni della verifica esterna #269**: `FATTA` — merge di main (V-1), V-2, V-3, V-4; review #515.
- **Fette 4–6 — attività di notte, 3 lezioni, backup iCloud**: `DEFERITA — azioni dell'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |   3 +++
 brains/claude_cli.py                |  16 +++++++++++++++-
 gas.py                              |  10 +++++++++-
 modules/notte/notte.py              |  15 +++++++++++++--
 reports/diff_sessione.md            |  14 +++++++++-----
 reports/handoff.md                  | n/d
 reports/r2_regole_abbonamento.md    |   8 ++++++++
 reports/stato_progetto.md           |   2 +-
 reports/ultimo_report.md            |  54 +++++++++---------------------------------------------
 scripts/notte/catalogo_esempio.yaml |   3 +++
 tests/test_unit_claude_cli.py       |  33 +++++++++++++++++++++++++++++----
 tests/test_unit_kernel.py           |  20 ++++++++++++++++++++
 tests/test_unit_notte.py            |  27 +++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile, riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
26ce319 Merge origin/main in feat/merge-automatico-z1xjx2 (PR #269) + correzioni verifica esterna #269
51d2a6b docs(fine-task): report dell'accensione del cervello forte (PR #269)
1717413 feat(R2): accensione del cervello forte — login scaduto chiaro, cervello: forte nel catalogo notturno, /forte nel terminale
c0917bb chore(revisore): memoria review #512 — APPROVATO
861b33a chore(revisore): memoria review #511 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 1717413 — due giri (#511, #512); commit 26ce319 — review #515 sullo stesso diff staged (il secondo sul delta che chiude le riserve del primo).

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

## §5 DELTA TEST DEL MOTORE

- Kernel: 1040 → 1041 PASS (T99r nuovo), 0 FAIL. Blocco reale: `=== RIEPILOGO: 1041 PASS, 0 FAIL ===`
- `tests/test_unit_claude_cli.py` + `tests/test_unit_notte.py`: 182 passed (2 test nuovi in claude_cli, 1 in notte; 1 modificato).
- Dopo il merge di main e le correzioni: kernel `=== RIEPILOGO: 1041 PASS, 0 FAIL ===`; `python3 -m pytest -q tests`: `2202 passed, 1 skipped in 198.40s (0:03:18)`.

## §6 STATO CI

`gh` nel cloud non è autenticato («Failed to log in to github.com using token (GH_TOKEN)»): CI letta con lo strumento GitHub (check della PR #269).
- 51d2a6b → run CI del push: `unit-suite` success, `handoff-check` success (riportato anche dalla verifica esterna #269).
- 1717413 → run CI 40240897439 (push), non riletta a fine run; contenuto incluso nell'albero di 51d2a6b.
- c0917bb, 861b33a → nessuna run su questi SHA (pushati insieme a 1717413).
- 26ce319 e commit di fine-task → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-515-1** BASSA: nessun test del ramo `/forte` da solo nel terminale (`main()` non testato).
- **R-515-2** BASSA: `/forte` seguito da un tab non riconosciuto.
- V-5 COSMETICA ve #269 (§6 datato): superata da questo handoff.
