# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-06 — V-B fetta B2 (PR #131) + arretrati della notte (PR #132–#136): dossier finale di sessione

---

## §0 DECISIONI UMANE RICHIESTE

1. **V-1 verifica esterna #131 (MEDIA, decisione)**: OPERATORE → `neutral` soddisfa il check richiesto: una PR sulla macchina del bot col sì del bot si può mergiare senza `gasmerge`. (a) tenere (decide l'operatore; chiudere con G-3, agente non admin) — consigliato; (b) `action_required`/`failure` (blocca, ma ogni PR sulla macchina richiede un bypass del ruleset).
2. Merge della PR #131 (https://github.com/Gasss23/Gas/pull/131). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4756065630","url":"https://github.com/Gasss23/Gas/pull/131"}`): `gh` non è autenticato in questo container. Merge manuale (tocca la macchina del bot).
3. Le altre PR della notte (#132–#136): riepilogo e consigli in `reports/ultimo_report.md`; ordine consigliato #134, #133, #135, #136, #132, #131.
4. **R-163-2** (NO legato allo SHA, non al tree) e **R-158-5** (§4quater accanto al bot): decisioni.
5. Verdetto INTEGRALE della review #163 non disponibile (sessione locale precedente): §4 riporta la riga della memoria del revisore.

---

## §1 SCOPE & ESITO FETTE

- **B2 primo commit `e51db2e`** (sessione locale): `FATTA` — review #163 APPROVATO CON RISERVE.
- **R-163-1 (MEDIA)**: `FATTA` (`a79cb07`). **R-163-4**: `FATTA`. **R-163-3**: `FATTA` (dichiarata). **R-163-2**: `DEFERITA — decisione umana`.
- **R-164-1/R-164-2**: `FATTA`; **R-164-3**: dichiarata.
- **setup_verifica_bot.md, fine-task.md §4quater, stato_progetto.md**: `FATTA`.
- **Verifica esterna §4quater #131**: `FATTA` — APPROVATO CON RISERVE (§8); V-1 MEDIA → §0.1.
- **Arretrati della notte**: `FATTA` — PR #132 (doc), #133 (R-150-1), #134 (2 fail-open gate IP/review), #135 (F-mac-2), #136 (F-mac-1), ciascuna con review e verifica esterna proprie (§9 riporta la seconda verifica di #134).
- **V-2 #127, R-162-1, R-162-2**: `DEFERITA — toccano file riscritti da B2: dopo il merge di #131`.
- **G-3**: `DEFERITA — fetta separata`.
- **Etichetta `verifica`**: `SALTATA — gh non autenticato e l'etichetta non esiste ancora`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 ++++
 .claude/commands/fine-task.md      |  11 ++++++++
 .github/workflows/verifica-bot.yml |  32 +++++++++++++++-------
 reports/diff_sessione.md           |  24 ++++++++---------
 reports/handoff.md                 | 520 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/setup_verifica_bot.md      |  39 ++++++++++++++++++++-------
 reports/stato_progetto.md          |   6 +++--
 reports/ultimo_report.md           |  47 ++++++++++++++++++++-------------
 scripts/bot_esito.py               | 222 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------
 scripts/gasmerge.sh                | 104 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------
 tests/test_unit_gasmerge.py        | 180 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------
 tests/test_unit_verifica_bot.py    | 320 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------
 12 files changed, 1040 insertions(+), 470 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
7d63b62 docs(merge-automatico): fine-task B2 — report, handoff con verdetti #163 (memoria)/#164/#165, diff sessione
a79cb07 fix(verifica-bot): R-163-1 — un NO sulla macchina del bot resta NO, "non verificabile" mai neutral — review #164/#165
620de66 chore(revisore): memoria review #165 — APPROVATO
a97d992 chore(revisore): memoria review #164 — APPROVATO CON RISERVE
e51db2e feat(merge-automatico): B2 — check run verifica-bot dell'App, NO definitivo per SHA, gasmerge --auto — review #163
793ccc7 chore(revisore): memoria review #163 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti del revisore per i commit di questo branch, INTEGRALI come nel precedente handoff (`7d63b62`).

### Review #163 — commit `e51db2e` (riga di memoria: testo integrale non disponibile)

VERDETTO: APPROVATO CON RISERVE — ATTENZIONE: il testo integrale della review #163 NON è disponibile in questa sessione cloud (è stato dato nella sessione locale precedente e non è stato committato). Riporto verbatim la riga che il revisore ha scritto nella propria memoria (`.claude/agents/memoria_revisore.md:263`), che NON sostituisce il verdetto integrale:

> #163 — 2026-10-06 — APPROVATO CON RISERVE — fetta B2 primo commit (G-1/G-2/G-4/G-5, V-2/R-161-1, V-3 #127): scripts/bot_esito.py:189 OPERATORE→neutral, :162 con_storico, :299 _conclusioni_precedenti (slug validato, filter=all), :213 fullmatch del titolo canonico; scripts/gasmerge.sh:49/:97 head legata al ref, :248-283 --auto (integration_id dal ruleset, any failure = NO, ultimo per id). 320 pytest riprodotti; mutation 28: 25 KILLED, 2 SURVIVED equivalenti (IP_TREE/ENGINE_DIFF di nuovo sul ref: REF==HEAD asserito dopo il secondo fetch), 1 SURVIVED reale (bot_esito.py:151 _APRE_GRAVE: nessun test con id fuori da V/F/R/G, sonda "C-1 (high)"). R-163-1 (MEDIA, da chiudere PRIMA del setup F): decidi() mette OPERATORE davanti al verdetto e cmd_esito tratta ogni MACCHINA_BOT != "false" come macchina → BOCCIATO + un CLAUDE.md/.gitattributes annidato, elenco file vuoto/troncato o output di smista mancante = neutral, che soddisfa il required check (sonda: BOCCIATO+macchina → neutral); neutral solo se il verdetto sarebbe APPROVE, le vie di prudenza → failure/cancelled. R-163-2 (BASSA, decisione): G-2 vale per SHA, un commit vuoto rilancia il dado. R-163-3 (BASSA): gasmerge manuale ora eredita failure/cancelled del bot dal --watch (nessuna via di override via gasmerge; bot oltre 900s = timeout).

(I numeri di riga della #163 si riferiscono a `e51db2e`; a HEAD le righe si sono spostate col commit `a79cb07`.)

### Review #164 — diff staged di `a79cb07` (prima delle correzioni R-164-1/2), verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md (sez. 5, 8, 10), la sezione B2 e le voci R-163 di `reports/stato_progetto.md` e la coda di `.claude/agents/memoria_revisore.md` (#150–#163). Il branch corrente è `feat/merge-automatico-z1xjx2`, come dichiarato. Il diff staged non tocca `_get_window`, il cap del loop né i provider. Non c'è slicing della history né output di tool simulato.

**Elementi del diff esaminati**

1. `scripts/bot_esito.py:199` — `decidi()` ora controlla in quest'ordine: head presente, poi elenco troncato (COMMENT), poi elenco diverso da "ok" (RIPROVA), poi `macchina_bot is None` (RIPROVA). Solo dopo chiama `_decidi_verdetto`, e solo APPROVE più macchina del bot diventa OPERATORE.
   - Rischio esaminato: una via "non verificabile" che arrivi a neutral o success.
   - Per arrivare a OPERATORE serve un APPROVE vero di `_decidi_verdetto`, con head uguali e verdetto valido oppure doc_only. Per doc_only serve un elenco "ok" non vuoto.
   - Sonde e test confermano che BOCCIATO o MEDIA sulla macchina danno COMMENT, mentre verdetto None, head cambiata, elenco "", "OK" o "boh" e macchina None danno RIPROVA.
   - Esito: **ok**, con una riserva sull'ordine (R-164-1, sotto).
2. `scripts/bot_esito.py:178` — `con_storico` ora vale anche per OPERATORE. Il chiamante a `scripts/bot_esito.py:366` lo applica a `("APPROVE", "OPERATORE")`.
   - Rischio esaminato: un esito RIPROVA registrato come failure nello storico.
   - `CONCLUSIONE` associa RIPROVA a cancelled, e `con_storico` cerca solo `"failure"`. Un cancelled precedente quindi non diventa mai un NO definitivo. Uno storico illeggibile (None) dà RIPROVA anche per OPERATORE.
   - Esito: **ok**.
3. `scripts/bot_esito.py:355` — `MACCHINA_BOT` viene letto con la mappa esatta `{"true": True, "false": False}`, e tutto il resto vale None, cioè RIPROVA. Il test parametrizzato copre None, "", "False", "no", "true" e "false" fino alla conclusione pubblicata. Esito: **ok**.
4. `.github/workflows/verifica-bot.yml:62` e `:255` — il workflow passa l'output `elenco` di smista come `ELENCO_FILE` a esito.
   - Rischio esaminato: con `pull_request_target`, una finestra in cui workflow e script vengono da versioni diverse.
   - Entrambi i checkout di "main (script fidati)" sono senza `ref:`, quindi usano `github.sha` dell'evento. Il workflow e lo script vengono dallo stesso commit di base, anche se main si muove fra il job smista e il job esito: nessuna finestra mista.
   - Anche in uno scenario ipotetico (workflow vecchio con script nuovo), `ELENCO_FILE` mancante dà RIPROVA, cioè cancelled: si blocca senza far passare nulla.
   - Se smista fallisce, esito non parte (`needs.smista.result == 'success'`) e il check richiesto resta assente, quindi il merge resta bloccato.
   - Esito: **ok**.
5. `tests/test_unit_verifica_bot.py:380` — test R-163-4 con `C-1 (high)`, `X-2 (grave)` e `C-3 (severe)` e JSON BASSA, che si aspettano COMMENT. Copre il ramo `_APRE_GRAVE` rimasto scoperto nella #163. Esito: **ok**.

**Riproduzioni**
- `pytest tests/test_unit_verifica_bot.py`: 267 passed.
- Mutation fatte da me:

| Mutation | Test falliti | Esito |
|---|---|---|
| `elenco != "ok"` → `== "vuoto"` | 7 | uccisa |
| filtro di `cmd_esito` ridotto a `== "APPROVE"` | 1 (`test_esito_macchina_dopo_un_no_resta_failure`) | uccisa |
| tolto `and evento == "APPROVE"` | 6 | uccisa |

  Dopo le mutation il file è tornato identico a quello dell'index (controllato con `cmp`) e lo staging è intatto.

**Riserve (tutte BASSE, non bloccanti)**
- **R-164-1:** il controllo "troncato" viene prima di quello sull'uguaglianza delle head. Con la head cambiata durante la verifica, `decidi(None, A, B, elenco="troncato")` dà COMMENT: viene scritto un failure definitivo sullo SHA vecchio invece di RIPROVA. Non ha effetto sulla head nuova, ma va contro il principio "il NO definitivo solo sullo SHA ancora attuale". Correzione: spostare il controllo `head_analizzata != head_attuale` prima del ramo troncato. Il test `test_head_prima_di_elenco` copre solo la head assente, non quella cambiata.
- **R-164-2 (costo):** con elenco vuoto o troncato il job `verifica` lancia comunque l'LLM, e poi il risultato viene scartato. Una PR a diff nullo resterebbe cancelled per sempre, e ogni rilancio consuma quota. Correzione: aggiungere `needs.smista.outputs.elenco == 'ok'` all'`if` del job verifica.
- **R-164-3 (si blocca senza far passare nulla):** `MAX_FILE_API` conta anche le righe `previous_filename`. Una PR con molti rename e meno di 3000 file viene giudicata "troncata" e riceve un failure definitivo. È irrealistico oggi; basta dichiararlo.
- **Nota di processo:** `reports/stato_progetto.md` cita già "review #164" e "R-163-1 CHIUSA" prima del verdetto. Ora è coerente, ma va scritto dopo il verdetto, non prima.

**Cosa NON ho verificato**
- Il comportamento reale su GitHub non l'ho provato: non è riproducibile in dev, l'App e il ruleset non sono ancora configurati. In particolare, che cancelled blocchi il required check e neutral no (lo so dalla documentazione GitHub) e che il ruleset leghi `integration_id` alla scelta dell'App.
- Non ho rilanciato la suite del kernel (651) né la suite aggregata da 587: il diff non tocca il motore runtime e mi sono fidato delle evidenze dell'agente.
- Non ho rifatto le 11 mutation dichiarate, solo le 3 sopra.

La memoria è aggiornata con la riga #164 e una lezione nuova: un esito definitivo per SHA va emesso solo dopo aver controllato che quello SHA sia ancora la head, e gli stati "non verificabile" vanno usati anche per non lanciare il lavoro LLM. L'ho committata da sola con lo script atomico (`a97d992`), senza toccare il diff staged.

(I numeri di riga della #164 si riferiscono al diff staged prima delle correzioni R-164-1/2; a HEAD sono spostati di qualche riga.)

### Review #165 — diff staged finale di `a79cb07`, verdetto integrale

## VERDETTO: APPROVATO

Ri-review #165 del diff staged aggiornato. Il branch è `feat/merge-automatico-z1xjx2`, quello dichiarato. Il diff non tocca `_get_window`, il cap del loop né i provider. Non c'è slicing della history né output di tool simulato.

**Elementi del diff esaminati**

1. **`scripts/bot_esito.py:211`** — il controllo "head cambiata" (`head_analizzata != head_attuale` → RIPROVA) ora viene subito dopo quello sulla head assente e prima del ramo troncato.
   - Rischio esaminato: un failure definitivo scritto su uno SHA che non è più la head.
   - Il test `tests/test_unit_verifica_bot.py:384` copre sia la head assente sia la head cambiata, con elenco troncato, e si aspetta RIPROVA.
   - Mutation: ho sostituito quel controllo con `if False`, cioè l'ho disattivato. Risultato: 1 failed, quindi la mutation viene presa.
   - Esito: **ok**. R-164-1 è chiusa.
2. **`.github/workflows/verifica-bot.yml:80`** — il job verifica ora parte solo con `solo_reports == 'false' && elenco == 'ok'`.
   - Rischio esaminato: con verifica saltata, il job esito potrebbe non girare, e allora il check richiesto mancherebbe.
   - L'`if` di esito resta `!cancelled() && needs.smista.result == 'success'`, e un test statico a `tests/test_unit_verifica_bot.py:887` lo fissa. Quando un job usa una funzione di stato esplicita, GitHub non applica il `success()` implicito: esito gira anche se verifica è stata saltata.
   - È lo stesso meccanismo che fa già funzionare il percorso solo log di sessione (doc-only) di B1.
   - Con verifica saltata il verdetto arriva vuoto (None), ma `decidi` valuta l'elenco prima del verdetto: elenco vuoto dà cancelled, elenco troncato con head uguale dà failure. Mai neutral né success.
   - Mutation: ho tolto `&& elenco == 'ok'`. Risultato: 1 failed, presa.
   - Esito: **ok**. R-164-2 è chiusa.
3. **`scripts/bot_esito.py:117`** — R-164-3 è dichiarata nella docstring di `stato_elenco`: i vecchi nomi dei rename contano nel limite dei 3000 file, ma l'errore cade dal lato prudente (NO, mai un sì).
   - Esito: **ok**. Riserva accettata come dichiarata.

**Riproduzioni**
- `pytest tests/test_unit_verifica_bot.py`: 268 passed.
- Dopo le due mutation ho ripristinato i file e controllato con `cmp` che fossero identici all'originale. Lo staging è intatto.

**Cosa NON ho verificato**
- Non ho provato la valutazione reale dell'`if` di esito su GitHub con il job verifica saltato. In dev non si può riprodurre; mi baso sulla semantica documentata delle funzioni di stato e sul percorso doc-only già in uso.
- Non ho rilanciato la suite del kernel né quella aggregata: il delta riguarda solo `bot_esito.py`, il workflow e i test del bot.

La memoria è aggiornata con la riga #165 ("nessuna lezione nuova") e committata da sola (`620de66`). Il diff staged non l'ho committato.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules in questo branch. Esecuzione a `a79cb07` in questo container (bwrap installato):

```
python tests/test_unit_kernel.py
=== RIEPILOGO: 651 PASS, 0 FAIL ===

python -m pytest -q tests/test_unit_hooks.py tests/test_unit_voice_server.py tests/test_unit_handoff_check.py tests/test_unit_gate.py tests/test_unit_gasmerge.py tests/test_unit_verifica_bot.py
588 passed in 88.22s (0:01:28)
```

## §6 STATO CI

Stato dal connettore GitHub (`actions_list`; `gh` non autenticato). Mappatura commit → run:
- `793ccc7`: nessuna run propria (pushato con `e51db2e`).
- `e51db2e`: run 37397491122 (push su `feat/merge-automatico`): unit-suite success, handoff-check failure (handoff non rigenerato in quella sessione).
- `a97d992`, `620de66`, `a79cb07`: pushati insieme → run 37435149767 su `a79cb07`: unit-suite success, handoff-check failure (atteso, prima del fine-task).
- `7d63b62` (primo fine-task): run 37435773427: **success**.
- commit di questo fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **V-1 #131 (MEDIA)**: decisione umana (§0.1).
- **R-163-2** (BASSA, decisione), **R-164-3** (BASSA, dichiarata), **R-162-1**, **R-162-2**, **R-158-5**.
- Verdetto integrale #163 mancante.

## §8 VERIFICA ESTERNA #131 (verdetto integrale)

Lanciata con `Applica .claude/verifica_esterna.md a: <URL_HANDOFF di 7d63b62> <URL_PR>` (agente nuovo, Sonnet). V-1 MEDIA → decisione umana §0.1 (il comportamento neutral = decide l'operatore è quello chiesto dall'operatore). V-2: §2/§6 erano corretti per i rispettivi SHA (il failure di handoff-check era su `a79cb07`, prima del fine-task); il conteggio di righe di §2 è approssimato per costruzione (fine-task §2). V-3 = R-163-2. V-4 = #163 mancante, dichiarato.

VERIFICA ESTERNA #131 — APPROVATO CON RISERVE

**Metodo.** Ho clonato il repo nella scratchpad al commit pinnato 7d63b62 e fatto `git diff --stat` e `git log` dalla base e91ceb4, che è il merge-base con main. Ho rilanciato `pytest` su `test_unit_verifica_bot.py`, `test_unit_gasmerge.py` e `test_unit_handoff_check.py`. Ho letto `scripts/bot_esito.py` (`decidi`, `con_storico`, `cmd_esito`), `scripts/gasmerge.sh` (ramo `--auto`) e il diff di `verifica-bot.yml`. Ho letto lo stato della PR e i check run con il connettore GitHub, e ho lanciato sonde dirette su `decidi()`. Il repo reale non è stato toccato.

**CLAIM VERIFICATI**
- **VERO.** 12 file cambiati e 6 commit: coincidono con l'handoff. Il PR dice 976 insertions e 466 deletions, e `git diff --stat` dà lo stesso totale.
- **PARZIALMENTE FALSO.** Il `--stat` in §2 dell'handoff non è quello reale al commit pinnato. Riporta `handoff.md` a 434 righe contro le 450 reali, e il suo totale è "960 insertions" contro 976. È una fotografia presa prima del commit di fine-task. L'handoff lo ammette solo per §3, non per §2.
- **VERO.** 393 test passati sulle tre suite. Il conteggio di `test_unit_verifica_bot.py` (268) è coerente con la somma di sezione. Non ho rilanciato la suite da 588 né il kernel da 651.
- **VERO.** La base head è e91ceb4, base della PR. Il branch `feat/merge-automatico-z1xjx2` punta a 7d63b62.
- **VERO.** Le chiusure di R-163-1 e R-164-1/2 sono nel codice. `decidi()` controlla la head cambiata prima dell'elenco troncato. Elenco vuoto o `macchina_bot` mancante danno RIPROVA, cioè cancelled. Un APPROVE sulla macchina del bot diventa OPERATORE, cioè neutral. Il job `verifica` parte solo con `elenco == 'ok'`. Sonde: APPROVATO più macchina dà OPERATORE; solo log di sessione più macchina dà OPERATORE; solo log di sessione senza macchina dà APPROVE.
- **FALSO, perché stantio.** §6 dell'handoff dice "handoff-check: failure". Sullo SHA pinnato ora `handoff-check` è success. `unit-suite` era ancora in corso al momento della lettura.
- **VERO.** Il job `verifica-bot` è `skipped` perché la PR non ha l'etichetta `verifica`, come dichiarato.
- **FALSO.** L'handoff è stato scritto prima dell'ultimo giro di CI e non lo dice.

**FINDING**
- **V-1 (MEDIA) — la riga "neutral decide l'operatore" è fuorviante.** Il PR dice "Da NON mergiare in automatico: la PR tocca `scripts/`, quindi il bot la darebbe neutral". Ma `setup_verifica_bot.md:71` ammette che neutral non blocca il ruleset. Su una PR che tocca la macchina del bot, un APPROVE diventa quindi un check required soddisfatto, e solo `gasmerge --auto` lo rifiuta. L'auto-merge nativo di GitHub e un merge manuale dal browser (con 0 approvazioni e self-merge consentito) passano comunque. Il gate che "protegge se stesso" regge solo se l'unico canale di merge è gasmerge. Rischio concreto: un commit che indebolisce il bot può essere approvato dal bot stesso e mergiato senza passare dall'operatore. Fix proposto: per OPERATORE pubblicare cancelled o failure con un motivo esplicito, oppure rendere il ruleset non soddisfatto da neutral, e dichiarare la scelta in §0 dell'handoff.
- **V-2 (BASSA) — handoff stantio (§2, §6).** Il `--stat` e lo stato CI non corrispondono allo stato reale al commit pinnato. Fix: rigenerare §2 e §6 dopo l'ultimo commit, oppure marcarli esplicitamente "prima del fine-task".
- **V-3 (BASSA) — R-163-2 resta aperta.** Il NO del bot è legato allo SHA, non al tree, e un commit vuoto riapre la verifica. L'handoff lo dichiara correttamente, ma resta un by-pass dopo un NO del bot. Mitigazione: serve un commit nuovo e `gasmerge --auto` rilegge lo storico. Non l'ho provato su GitHub.
- **V-4 (COSMETICA).** Il verdetto integrale della review #163 è assente, dichiarato in §0.5 e §4. Resta il fatto che per questa fetta il verdetto più importante, quello con R-163-1 MEDIA, non è ispezionabile.

**NON VERIFICATO**
- Il ruleset reale di main (check required, `integration_id`), perché `gh` non è utilizzabile e non ho provato un'altra via di lettura.
- Il comportamento reale dei check con GitHub: neutral come soddisfatto, skipped del job `esito`, `if: !cancelled()`.
- La suite del kernel da 651 e la suite aggregata da 588, non rilanciate.
- Le mutation dichiarate (12/12 uccise) e la review #163.
- La CI finale di `unit-suite` su 7d63b62, ancora in corso alla lettura.
- Il job `esito` con `verifica` saltata, non riproducibile qui.

**RACCOMANDAZIONE.** Prima di mergiare la PR e di fare altro lavoro: decidere V-1, cioè se neutral su una PR che tocca la macchina del bot debba soddisfare il ruleset. Aggiornare §2 e §6 dell'handoff. Dopo il merge, ripetere la verifica sul comportamento reale del check `verifica-bot` con una PR di prova che tocca la macchina del bot, e controllare che gasmerge sia l'unico canale di merge.

## §9 SECONDA VERIFICA ESTERNA #134 (altra PR della notte, verdetto integrale)

Riportata qui perché arrivata dopo l'ultimo fine-task di #134 (`514869a`): solo finding BASSI, nessuna correzione; il suo handoff (§8) contiene la prima verifica.

VERIFICA ESTERNA PR #134 — APPROVATO CON RISERVE

**Metodo**
- Clone usa-e-getta nella scratchpad, al commit pinnato 514869a. Merge-base con main: e91ceb4.
- Ho confrontato §2 e §3 con `git diff --stat` e `git log` reali.
- Ho riletto il diff reale di `review_gate.sh`, `ci.yml`, `check_verdetto.py`, `gasmerge.sh` e `fine_task_finale.sh`.
- Ho rilanciato gasmerge, hooks, gate e handoff_check con `GAS_TEST_LOCALE_UTF8_ATTESO=1`, sia con `LC_ALL=C` sia con `LC_ALL=C.UTF-8`.
- Ho rifatto la mutation su `review_gate.sh:76` in una copia separata.
- Ho letto check-runs, stato della PR e ruleset dall'API REST pubblica di GitHub.
- Ho cercato con grep altri `read` senza `LC_ALL=C` nel repo.
- `git status` del repo reale (/home/user/Gas) è vuoto.

**CLAIM VERIFICATI**
- **§3 git log: VERO.** I 12 commit da e91ceb4 coincidono con l'elenco. Il commit di fine-task 514869a non è nel §3 e l'handoff lo dichiara.
- **§2 git diff --stat: FALSO, minore.**
  - Dichiara 392 inserzioni e 466 righe per `handoff.md`.
  - Il reale è 416 inserzioni, 322 cancellazioni e 490 righe.
  - L'elenco dei 13 file è corretto.
  - Lo scarto è quasi inevitabile, perché lo stat contiene l'handoff stesso, scritto prima dell'ultimo commit.
- **Delta test: VERO.** 281 passed con `LC_ALL=C` e 281 con `LC_ALL=C.UTF-8`, come dichiarato. Il +8 rispetto a origin/main (273) non l'ho rieseguito alla base.
- **R-177 (`review_gate.sh:76`) chiusa: VERO.** Con `LC_ALL=C` tolto dal `read`, `test_gate_perimetro_byte_non_utf8_in_locale_utf8_blocca` fallisce (exit atteso 2). Con il fix passa.
- **V-3 (locale richiesto in CI): VERO nel codice.** `_esigi_locale_utf8()` fa `pytest.fail` se `GAS_TEST_LOCALE_UTF8_ATTESO=1` e il locale manca. `ci.yml` imposta quella variabile nel job `unit-suite`. Il log del job non l'ho letto (vedi NON VERIFICATO).
- **Nessun `read` rimasto senza `LC_ALL=C`: VERO.** In scripts, hooks e workflow resta solo `scripts/gasmerge.sh:233` (`read -r ANS`), che è la risposta interattiva dell'operatore.
- **I fix non indeboliscono nessun gate: VERO.** I diff dei tre script sono `read` → `LC_ALL=C read`, più il fail-closed su perimetro non UTF-8 in `check_verdetto.py`. Questo rende il gate B più stretto, non più debole.
- **CI sullo SHA 514869a: VERO.** `unit-suite` e `handoff-check` sono `success`; `esito`, `verifica` e `smista` sono `skipped`.
- **PR #134: VERO.** Aperta, non mergiata, head 514869a, `mergeable_state` = clean.
- **Check required: VERO per i nomi attesi.** Il ruleset `main-lock` è attivo e include `non_fast_forward`, `creation`, `pull_request` e `required_status_checks`. L'output l'ho letto troncato a 800 caratteri, quindi i nomi `unit-suite` e `handoff-check` nel ruleset non li ho visti direttamente.

**FINDING**
- **V-1 (BASSA) — il §2 è obsoleto.** Stat e conteggio righe sono fotografati prima dell'ultimo commit. Fix: dichiararlo "pre-quater" oppure rigenerarlo per ultimo. Non incide sul merge.
- **V-2 (BASSA) — il §6 sullo stato CI è incompleto.** Dice "run non ancora disponibile" per l'ultimo giro, ma ora è verde sullo SHA 514869a. Fix: aggiornare dopo il merge, oppure accettarlo come nota datata.
- **V-3 (BASSA) — il verdetto della verifica precedente è incollato nell'handoff.**
  - Il §8 contiene il verdetto di un'altra verifica, su 3fc1e95, e dice di quel verdetto che V-2 e V-3 sono "chiuse".
  - Io ho riprovato la chiusura in modo indipendente (mutation, suite, grep).
  - Non è un errore, ma il §8 riporta il verdetto di un'altra verifica come stato attuale.
- **V-4 (BASSA, ereditata) — la mutation sul `read -r v` annidato di `gasmerge.sh:198` sopravvive.** Le voci del perimetro sono ASCII, quindi l'equivalenza in pratica è plausibile. Non l'ho riprovata.

**NON VERIFICATO**
- Log reali del job `unit-suite`, per vedere che i test locale-dipendenti siano stati eseguiti e non saltati. L'API dei log richiede autenticazione, e `success` da solo non lo prova. La variabile trasforma lo skip in fail, e questo l'ho verificato nel codice.
- Nomi esatti dei check required nel ruleset (output troncato a 800 caratteri).
- macOS (bash 3.2 o bash 5 di homebrew): nessun Mac.
- Esecuzione end-to-end di `gasmerge.sh` e `fine_task_finale.sh`: pushano o toccano GitHub. Il comportamento l'ho coperto solo con i test.
- Mutation su `git grep`, `grep -qE`, `grep -Fx` e sul `read` del filtro loopback: non rifatte. Il revisore dichiara di aver rifatto quelle sul `read` in entrambi gli script.
- Test R-178-1 con codifica locale latin-1: non provato. Al massimo darebbe un falso rosso, mai un fail-open.
- Conflitti di merge con le altre PR della notte (#131 e simili).

**RACCOMANDAZIONE**
Il fix è corretto e dimostrato. Chiude due fail-open reali: il gate IP e il gate di review, in locale UTF-8. I test discriminano, la CI è verde sullo SHA e la PR è mergeabile pulita. Si può fare il merge. Dopo il merge:
1. Aggiornare §2 e §6 dell'handoff, oppure accettarli come fotografia datata.
2. Controllare a mano nel log di una run CI che i test locale-dipendenti non siano saltati.
3. Fetta di sicurezza: fare il secondo passaggio indipendente nella chat claude.ai.
