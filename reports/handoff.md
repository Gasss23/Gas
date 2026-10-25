# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-25 sera — Accensione del cervello forte (chat Motore)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #269 (https://github.com/Gasss23/Gas/pull/269). Numero e URL dalla risposta JSON dello strumento GitHub `create_pull_request` (`gh` nel cloud non è autenticato). Merge solo secondo CLAUDE.md §10.
2. Sul Mac: `/login` dell'abbonamento Max di Gas (il login era scaduto), prova del login, `GAS_CLAUDE_CLI=1` nel `.env` (`reports/r2_regole_abbonamento.md`).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 0 — Esito della PR #266**: `FATTA` — già mergiata dall'operatore, bot success, CI verde.
- **Fetta 1 — Prova del login sul Mac (R-496-3)**: `DEFERITA — login scaduto («OAuth session expired»), serve /login dell'operatore`.
- **Fetta 2 — Accensione del forte**: `FATTA` — note di #265 chiuse, login scaduto chiaro, `cervello: forte` nel catalogo, `/forte` nel terminale, setup del Mac.
- **Fette 3–5 — attività di notte, 3 lezioni, backup iCloud**: `DEFERITA — azioni dell'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |  2 ++
 brains/claude_cli.py                | 15 ++++++++++++++-
 gas.py                              |  7 ++++++-
 modules/notte/notte.py              | 14 ++++++++++++--
 reports/diff_sessione.md            | 16 +++++++++-------
 reports/handoff.md                  | n/d
 reports/r2_regole_abbonamento.md    |  8 ++++++++
 reports/stato_progetto.md           |  2 +-
 reports/ultimo_report.md            | 19 ++++++++-----------
 scripts/notte/catalogo_esempio.yaml |  3 +++
 tests/test_unit_claude_cli.py       | 33 +++++++++++++++++++++++++++++----
 tests/test_unit_kernel.py           | 20 ++++++++++++++++++++
 tests/test_unit_notte.py            | 25 +++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile, riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
1717413 feat(R2): accensione del cervello forte — login scaduto chiaro, cervello: forte nel catalogo notturno, /forte nel terminale
c0917bb chore(revisore): memoria review #512 — APPROVATO
861b33a chore(revisore): memoria review #511 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 1717413 — due giri sullo stesso diff staged (il secondo sul delta che chiude le riserve del primo).

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

## §5 DELTA TEST DEL MOTORE

- Kernel: 1040 → 1041 PASS (T99r nuovo), 0 FAIL. Blocco reale: `=== RIEPILOGO: 1041 PASS, 0 FAIL ===`
- `tests/test_unit_claude_cli.py` + `tests/test_unit_notte.py`: 182 passed (2 test nuovi in claude_cli, 1 in notte; 1 modificato).

## §6 STATO CI

CI NON VERIFICATA con `gh` (nel cloud `gh` non è autenticato: «Failed to log in to github.com using token (GH_TOKEN)»). Letto con lo strumento GitHub `actions_list` sul branch:
- 1717413 → run CI 40240897439 (push): `in_progress` alla scrittura dell'handoff; verifica-bot 40240911265: `skipped` (manca l'etichetta `verifica`).
- c0917bb, 861b33a → nessuna run su questi SHA (pushati insieme a 1717413, testati solo nell'albero di testa).
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

Nessuna (R-511-1, R-511-2 e la COSMETICA chiuse in #512).
