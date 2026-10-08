# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-08 — R-220-3: tetti di tempo per `gas notte` + timeout HTTP dei provider (PR #162)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #162 (https://github.com/Gasss23/Gas/pull/162). Tocca il motore: l'agente la mergia da solo SOLO se il bot dà `APPROVATO` testuale senza finding V-x, CI verde e nessun conflitto; altrimenti decide l'operatore. (Numero e URL dall'output dello strumento GitHub collegato: `gh` nel container non è autenticato.)
2. Sul Mac (se non già fatto): `cd ~/Gas && git fetch origin && git switch --detach origin/main`, poi installare il timer notturno seguendo `reports/setup_notte.md` (§2c: tetti di tempo).
3. Ancora aperte da sessioni precedenti: lezioni #4, #5, #6; firma `fab385e4…`.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — timeout HTTP dei provider in `run_turn`/`rifletti`** (`2146233`): `FATTA` — 120s, Ollama 600s, override env.
- **Fetta 2 — tetti di tempo per compito/giro in `gas notte`** (`2146233`): `FATTA` — cooperativi, generatore chiuso, compiti saltati con exit 1.
- **Fetta 3 — test** (`2146233`): `FATTA` — kernel 707 → 711, notte 26 → 35.
- **Fetta 4 — doc operatore `reports/setup_notte.md` §2c**: `FATTA` (caso peggiore ~55 min).
- **R-226-4, R-227-1, docstring R-227-2**: `DEFERITE` — riserve BASSE, candidate per GAS di notte.
- **FASE 4.5 fetta 2 (riepilogo del giro su Telegram)**: `DEFERITA` — prossima fetta.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 gas.py                             |  23 +++++++++++++++++++++--
 modules/notte/notte.py             |  67 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
 reports/diff_sessione.md           |  19 ++++++++++---------
 reports/handoff.md                 | 200 ++++++++++++-------
 reports/setup_notte.md             |  11 +++++++++--
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  34 +++++++++++++++-------------------
 tests/test_unit_kernel.py          |  77 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------
 tests/test_unit_notte.py           | 129 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 9 files changed, 316 insertions(+), 52 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
2146233 feat(fase-4.5): tetti di tempo per gas notte + timeout HTTP dei provider (R-220-3)
1d67b29 chore(revisore): memoria review #227 — APPROVATO CON RISERVE
4449488 chore(revisore): memoria review #226 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit `2146233` — review #226 (diff iniziale) e review #227 (diff con le correzioni, quello committato). Incollati integralmente.

### Review #226

## VERDETTO: APPROVATO CON RISERVE

In breve: la fetta chiude R-220-3 come promesso. Interrompere un turno a metà lascia lo stato coerente, verificato anche sul kernel vero e non solo sui test finti. Il fallback tra provider resta invariato e il tetto di 10 iterazioni non è toccato. Le riserve riguardano l'effetto del timeout di 120 secondi fuori dalla notte, e il tetto reale, che è più alto di quanto dice la documentazione.

**Elementi del diff esaminati**

1. `gas.py:1008` e `gas.py:696` — nuova costante `PROVIDER_TIMEOUT_SEC = 120`, modificabile con la variabile d'ambiente tramite `_env_int` (minimo 5). Rischio: un valore sporco o troppo basso. T81c copre i tre casi: 45 viene accettato, 1 diventa 5, "abc" torna a 120. **ok**
2. `gas.py:2530` (run_turn) e `gas.py:1958` (rifletti) — il timeout viene passato a `OpenAI(...)`. Rischio: che cambi il fallback. Con l'SDK 2.43.0 la chiamata scaduta solleva un'eccezione `APITimeoutError`. Viene catturata dall'except del provider a `gas.py:2614`, finisce nel log ed entra nella classificazione degli errori. Il messaggio non contiene "400", quindi non attiva il retry speciale di Gemini. Il §9 resta intatto. Mutation "timeout tolto in run_turn": T81a FAIL, 709/1. **ok**
3. `modules/notte/notte.py:203` — `gen.close()` nel `finally`. Rischio: stato incoerente dopo l'interruzione. **Sonda mia sul run_turn reale**: risposta con 2 tool call, chiusura dopo il primo `tool_res`. Risultati:
   - nessun `RuntimeError`, perché l'except di run_turn intercetta solo `Exception` e non `GeneratorExit`;
   - il `finally` di run_turn (`_chiudi_turno`) scrive comunque `turno_fine esito=ko`;
   - il diario contiene solo il tool già eseguito, eseguito per intero;
   - in memoria la history ha `assistant(tool_calls=2)` e un solo `tool`, quindi è sbilanciata, ma `_save_history` (`gas.py:2603`) non viene raggiunto e su disco resta l'ultimo stato coerente. Il kernel viene buttato a ogni compito (`kernel_factory` dentro il ciclo) e `history=[]` viene riazzerata, quindi la cosa è innocua;
   - una firma parcheggiata prima della chiusura resta valida, come deve.
   
   Esito **ok**.
4. `modules/notte/notte.py:190` — controllo del tempo tra un evento e l'altro, saltato se l'esito è già ok. Caso "final dopo il tetto": il risultato viene tenuto, ed è corretto perché il lavoro è finito. Caso "error dopo il tetto": il vero errore viene sovrascritto da "tempo scaduto" (riserva 3). Mutation "break tolto": `test_compito_oltre_il_tetto_interrotto` FAIL. **riserva cosmetica**
5. `modules/notte/notte.py:296` e `:311` — tetto del giro controllato prima di ogni compito; ogni compito ha come tetto il minore tra il suo e il tempo rimasto del giro. Exit code 1 a `:320`. Mutation "min tolto": `test_tetto_compito_limitato_dal_tempo_rimasto_del_giro` FAIL. **ok**
6. Coerenza con CLAUDE.md:
   - §5: niente tagli diretti della cronologia; `_get_window` non toccato.
   - §8: il ciclo `range(10)` è invariato.
   - Niente `signal.alarm`: è la scelta giusta per "zero crash".
   
   Esito **ok**.

**Test riprodotti** (con `PYTHONDONTWRITEBYTECODE=1`): `tests/test_unit_kernel.py` 710 PASS, 0 FAIL; `pytest tests/` 785 passed. Dopo le mutation ho ripristinato i file dall'index: lo stato git è pulito.

**Riserve (da tracciare in stato_progetto.md)**

- **R-226-1 (MEDIA)**: il timeout di 120 secondi vale per tutti i turni, anche di giorno (Telegram e CLI), e per il provider di ultima istanza Ollama. Sul VPS gira su CPU senza GPU (stato_progetto: 3B o 7B, forse caricato su richiesta), con un prompt da circa 8k token. Lì la sola lettura del prompt può superare i 120 secondi, quindi il "pavimento offline" rischia di scadere sempre, e dopo 3 tentativi dell'SDK. Proposte: un timeout separato per Ollama, oppure un default più alto per i provider gratuiti, oppure almeno una nota esplicita all'operatore.
- **R-226-2 (BASSA, doc)**: il tetto non è duro. Tra due eventi possono passare circa 5 provider × 3 tentativi (`max_retries=2` di default) × 120s, cioè circa 30 minuti. Un compito da 900 secondi può quindi durare 40 minuti o più, e il giro sforare di altrettanto. `reports/setup_notte.md` dice "timeout di 120s" senza il moltiplicatore: va dichiarato il caso peggiore reale.
- **R-226-3 (COSM.)**: se dopo il tetto arriva un evento `error` (pipeline esausta, budget), il messaggio vero viene sostituito da "tempo scaduto". Meglio controllare il tempo solo sugli eventi non finali, oppure aggiungere il motivo al messaggio invece di sostituirlo.
- **R-226-4 (BASSA, test)**: i 4 test nuovi della notte usano un `_K` finto. Nessun test chiude il `run_turn` reale a metà verificando `turno_fine esito=ko`: la mia sonda lo prova, ma non resta nella suite.

**Rischio escluso**: non ho verificato il comportamento reale dell'SDK con un server che resta appeso (timeout e retry contro un endpoint lento vero), né Ollama sul VPS. Non è riproducibile in dev senza rete e senza il VPS. Il moltiplicatore ×3 viene dalla firma `OpenAI.__init__` (`max_retries=2`) e da come l'SDK si comporta di solito con `APITimeoutError`, non da una misura.

Ho aggiunto la riga contatore #226 e una lezione nuova a `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole (commit 4449488). Il diff staged non l'ho toccato.

File rilevanti:
- `/home/user/Gas/gas.py`
- `/home/user/Gas/modules/notte/notte.py`
- `/home/user/Gas/reports/setup_notte.md`
- `/home/user/Gas/tests/test_unit_kernel.py`
- `/home/user/Gas/tests/test_unit_notte.py`

### Review #227

## VERDETTO: APPROVATO CON RISERVE

Review #227. In breve: le correzioni chiudono davvero R-226-1 e R-226-3 e i test passano. Restano due punti minori. Il test del timeout di Ollama non passa dal punto in cui il timeout viene davvero usato. La stima "circa 30 minuti" di sforamento è ora troppo bassa: dopo questa correzione il caso peggiore è circa 55 minuti.

**Elementi del diff esaminati**

1. `gas.py:1902-1904` — `_timeout_provider(name)` dà 600 secondi (`OLLAMA_TIMEOUT_SEC`) al rung "ollama" e 120 a tutti gli altri. Valori in `gas.py:1013` e `:697`, modificabili da env con minimo 5. Rischio esaminato: che Ollama, il paracadute locale, scada sempre. 600 secondi è lo stesso default dell'SDK, quindi per Ollama non cambia nulla rispetto a prima della fetta. Esito **ok**.
2. `gas.py:2539` (run_turn) e `gas.py:1967` (rifletti) — l'helper è usato in entrambe le chiamate `OpenAI(...)` e la cascata dei provider è invariata. Ho però ristabilito a mano `self.PROVIDER_TIMEOUT_SEC` in run_turn: la suite resta 711/0. Nessun test passa da questa chiamata con un rung Ollama, perché T81d prova solo l'helper. Esito **riserva** (R-227-1).
3. `modules/notte/notte.py:192` — il controllo del tempo ora vale solo per gli eventi diversi da `final` ed `error`. Rischio esaminato: un evento intermedio dopo il tetto potrebbe non interrompere più il compito. Non succede: `tool_res` continua a far scattare il controllo, e `test_compito_oltre_il_tetto_interrotto` passa. Ho rimesso la condizione vecchia e `test_errore_dopo_il_tetto_conserva_il_messaggio_vero` fallisce come deve. Esito **ok**.
4. `reports/setup_notte.md` §2c e la docstring di `notte.py` dicono "sforamento di circa 30 minuti". Ora il solo rung Ollama vale 600 s × 3 tentativi = 30 minuti, più 4 rung × 3 × 120 s ≈ 24 minuti: il caso peggiore è circa 55 minuti. Esito **riserva** (R-227-2).

**Test riprodotti** (con `PYTHONDONTWRITEBYTECODE=1`): `tests/test_unit_kernel.py` 711 PASS, 0 FAIL; `pytest tests/` 786 passed. Dopo le mutation ho ripristinato i file dall'index: lo stato git è pulito.

**Riserve (da tracciare in stato_progetto.md)**

- **R-227-1 (BASSA, test)**: aggiungere a T81a un rung Ollama (`GAS_OLLAMA_URL` impostata e i rung prima che falliscono) e verificare che il client riceva `timeout=600`. Oggi, se qualcuno rimette il timeout fisso nella chiamata, la regressione di R-226-1 passa senza che nessun test fallisca.
- **R-227-2 (BASSA, doc)**: correggere "~30 min" in "~55 min" (oppure "fino a circa un'ora") nella docstring di `notte.py` e in `setup_notte.md`.
- **R-226-4** resta aperta, come dichiarato.

**Rischio escluso**: non ho misurato tempi reali contro un endpoint appeso, né Ollama sul VPS: non si può riprodurre in dev. I conti del caso peggiore partono dal default `max_retries=2` della firma `OpenAI.__init__` (SDK 2.43.0), non da una misura.

Ho aggiunto in memoria la riga contatore #227 e una lezione nuova, committate da sole (1d67b29). Il diff staged non l'ho toccato.

File rilevanti:
- `/home/user/Gas/gas.py`
- `/home/user/Gas/modules/notte/notte.py`
- `/home/user/Gas/reports/setup_notte.md`
- `/home/user/Gas/tests/test_unit_kernel.py`
- `/home/user/Gas/tests/test_unit_notte.py`
- `/home/user/Gas/.claude/agents/memoria_revisore.md`

## §5 DELTA TEST DEL MOTORE

Kernel: 707 PASS → 711 PASS, 0 FAIL (T81a–T81d nuovi). Notte: 26 → 35 passed. `pytest tests/`: 786 passed.

```
[PASS] T81a run_turn costruisce il client col timeout del kernel (default 120s) — timeout visti: [120]
[PASS] T81b rifletti costruisce il client col timeout del kernel — timeout visti: [120]
[PASS] T81d R-226-1: Ollama locale ha il suo timeout (600s), gli altri rung 120s — (600, 120)
[PASS] T81c GAS_PROVIDER_TIMEOUT_SEC: override, minimo 5, valore sporco → default — (45, 5, 120)
=== RIEPILOGO: 711 PASS, 0 FAIL ===
```

Nessun FAIL fuori scope.

## §6 STATO CI

CI NON VERIFICATA con `gh run list` (gh presente ma non autenticato: "Failed to log in to github.com using token (GH_TOKEN)"). Check run letti con lo strumento GitHub collegato sulla PR #162:

- `4449488`, `1d67b29`: nessuna run su questi SHA (pushati insieme a `2146233`; la run testa solo l'albero di testa).
- `2146233`: run 37860114633 — `handoff-check` **failure** (handoff della sessione non ancora committato: atteso, corretto da questo commit di fine-task), `unit-suite` in_progress alla scrittura; run 37860135072 (verifica-bot) — `smista`/`verifica`/`esito` skipped (etichetta `verifica` non ancora messa).
- commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-226-4 (BASSA, test): nessun test chiude il `run_turn` REALE a metà verificando `turno_fine esito=ko`.
- R-227-1 (BASSA, test): T81d prova solo l'helper; manca un test che passi dal rung Ollama in `run_turn` con `timeout=600`.
- R-227-2 (BASSA, doc): la docstring di `modules/notte/notte.py` dice ~30 min, il caso peggiore è ~55 min (`reports/setup_notte.md` già corretto).
