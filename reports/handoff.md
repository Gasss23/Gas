# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-06 — V-B fetta B2: check run `verifica-bot` dell'App, NO definitivo per SHA, `gasmerge --auto` + chiusura R-163-1/R-163-4 (sessione cloud notturna)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #131 (https://github.com/Gasss23/Gas/pull/131). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4756065630","url":"https://github.com/Gasss23/Gas/pull/131"}`): `gh` non è autenticato in questo container (`gh auth status`: "Failed to log in to github.com using token (GH_TOKEN)"). Merge manuale, la PR tocca la macchina del bot.
2. **R-163-2** (BASSA, decisione): il NO del bot è legato allo SHA e non al tree; un commit nuovo con lo stesso contenuto riapre la verifica. Variante B = legarlo al tree.
3. **R-158-5** (da B1): §4quater locale obbligatoria accanto al bot per le fette nel perimetro? Consiglio: sì.
4. Setup del bot aggiornato (`reports/setup_verifica_bot.md`): App con **Checks → Read and write**; etichetta `verifica` da creare a setup finito (§D); §F ruleset col check `verifica-bot` dell'App.
5. Verdetto INTEGRALE della review #163 non disponibile in questa sessione (dato nella sessione locale precedente, mai committato): §4 riporta la riga della memoria del revisore, dichiarata come tale.

---

## §1 SCOPE & ESITO FETTE

- **B2 primo commit (`e51db2e`, sessione locale)**: `FATTA` — G-1/G-2/G-4/G-5, R-161-1, `gasmerge --auto`, V-3 #127; review #163 APPROVATO CON RISERVE.
- **R-163-1 (MEDIA)**: `FATTA` — `a79cb07`: prima il verdetto, solo APPROVE+macchina = OPERATORE; elenco vuoto/troncato e `MACCHINA_BOT`/`ELENCO_FILE` mancanti mai neutral.
- **R-163-4 (BASSA)**: `FATTA` — test sul ramo `_APRE_GRAVE` ("C-1 (high)").
- **R-163-2**: `DEFERITA — decisione umana`.
- **R-163-3**: `FATTA` (dichiarata in setup §F).
- **R-164-1/R-164-2**: `FATTA` nello stesso commit; **R-164-3**: dichiarata.
- **setup_verifica_bot.md, fine-task.md §4quater, stato_progetto.md**: `FATTA`.
- **Etichetta `verifica` sulla PR**: `SALTATA — gh non autenticato e l'etichetta non esiste ancora (la crea l'operatore)`.
- **G-3 (agente non admin)**: `DEFERITA — fetta separata`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 .claude/commands/fine-task.md      |  11 ++++++++++
 .github/workflows/verifica-bot.yml |  32 +++++++++++++++++++--------
 reports/diff_sessione.md           |  24 ++++++++++----------
 reports/handoff.md                 | 434 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/setup_verifica_bot.md      |  39 ++++++++++++++++++++++++--------
 reports/stato_progetto.md          |   6 +++--
 reports/ultimo_report.md           |  49 ++++++++++++++++++++++++++---------------
 scripts/bot_esito.py               | 222 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------
 scripts/gasmerge.sh                | 104 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------
 tests/test_unit_gasmerge.py        | 180 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 tests/test_unit_verifica_bot.py    | 320 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------
 12 files changed, 960 insertions(+), 466 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
a79cb07 fix(verifica-bot): R-163-1 — un NO sulla macchina del bot resta NO, "non verificabile" mai neutral — review #164/#165
620de66 chore(revisore): memoria review #165 — APPROVATO
a97d992 chore(revisore): memoria review #164 — APPROVATO CON RISERVE
e51db2e feat(merge-automatico): B2 — check run verifica-bot dell'App, NO definitivo per SHA, gasmerge --auto — review #163
793ccc7 chore(revisore): memoria review #163 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #163 — commit `e51db2e`

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

Nessuna modifica a gas.py/brains/modules. Test della macchina di controllo cambiati: `tests/test_unit_verifica_bot.py` 235 (a `e51db2e`) → 268 passed.

Esecuzione a HEAD `a79cb07` in questo container (bwrap installato):

```
python tests/test_unit_kernel.py
=== RIEPILOGO: 651 PASS, 0 FAIL ===

python -m pytest -q tests/test_unit_hooks.py tests/test_unit_voice_server.py tests/test_unit_handoff_check.py tests/test_unit_gate.py tests/test_unit_gasmerge.py tests/test_unit_verifica_bot.py
588 passed in 88.22s (0:01:28)
gasmerge: 85 passed | verifica_bot: 268 passed | hooks: 102 passed | handoff_check: 40 passed | gate: 74 passed | voice_server: 19 passed
```

## §6 STATO CI

`gh` non autenticato nel container ("CI NON VERIFICATA (gh assente)" per la CLI); stato letto col connettore GitHub (`actions_list`, branch `feat/merge-automatico-z1xjx2`):

```
CI            run 37397491122  push                 e51db2e  completed  failure  (unit-suite: success; handoff-check: failure — step "Run check_handoff (versione main)")
CI            run 37435149767  push                 a79cb07  completed  failure  (unit-suite: success; handoff-check: failure — step "Run check_handoff (versione main)")
verifica-bot  run 37435179490  pull_request_target  a79cb07  completed  skipped  (PR #131 senza etichetta `verifica`)
```

Mappatura commit → run:
- `793ccc7`: nessuna run su questo SHA (pushato insieme a `e51db2e`).
- `e51db2e`: run 37397491122 (CI, push su `feat/merge-automatico`) — unit-suite success; handoff-check failure (step "Run check_handoff (versione main)": handoff non rigenerato in quella sessione).
- `a97d992`, `620de66`: nessuna run su questi SHA (pushati insieme a `a79cb07`).
- `a79cb07`: run 37435149767 — unit-suite success; handoff-check failure ATTESO (handoff.md non ancora rigenerato prima di questo fine-task).
- commit di fine-task (questo file): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-163-2** (BASSA, decisione umana): NO legato allo SHA, non al tree.
- **R-164-3** (BASSA, dichiarata): i rename contano nel limite dei 3000 file (fail-closed).
- **R-162-1** (BASSA): niente sandbox PID nel job verifica.
- **R-162-2** (BASSA): scrub dell'ambiente legato al pin `cab360f` della action (R-160-1 MITIGATA).
- **R-158-5** (decisione umana): §4quater locale accanto al bot.
- Verdetto integrale #163 mancante (vedi §4).
