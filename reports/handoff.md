# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-03 — C4b-3: esito della firma nel contesto del modello, branch `feat/cancello-c4b3`

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #117 (https://github.com/Gasss23/Gas/pull/117). Variante A: l'agente lancia `gasmerge 117`, l'operatore conferma digitando `117`.
2. R-135-3: riscrivere la regola di `.claude/agents/revisore.md` "citare un file non nel diff invalida il verdetto" come "≥2 elementi nel diff, citazioni di contesto ammesse e verificate a HEAD", e allineare il gate (chiuderebbe anche R-135-1/2)? È configurazione: decide l'operatore.
3. Prova reale di un click su Telegram (bot vivo con `gas telegram`, azione innocua): da decidere quando farla. Finora non è stata provata, ed è l'ultimo passo prima di considerare M2 completa.

---

## §1 SCOPE & ESITO FETTE

- **Esito della firma nella storia del modello (`_storia_esito_firma`, R-c4b2-1)**: `FATTA`.
- **Copertura casi (rifiuto, firma non riconosciuta, hash non integro, esito post-reclamo)**: `FATTA`.
- **R-c4b2-9 (dry-run letto come eseguita)**: `FATTA`.
- **R-c4b3-1 ("eseguita" dal segnale del kernel, non dal testo dell'output)**: `FATTA`, chiusa dopo la review #133 e verificata nella #134.
- **R-c4b3-2 (test dedup portante)**: `FATTA`.
- **Notifica di scadenza al modello**: `DEFERITA — C5 da design`.
- **R-c4b3-5 (timeout = "esito incerto")**: `DEFERITA — riserva minore, serve una nuova fetta motore con review`.
- **Click reale su Telegram**: `DEFERITA — decisione operatore (§0.3)`.
- **Gate B `check_verdetto.py`, falso positivo sui file di contesto (F-controlli-auto, parte "path corti")**: `FATTA` (commit `9951563`, review #135), su scelta dell'operatore. Il primo `fine_task_finale.sh` si era fermato su `bot.py:282`/`bot.py:417` del verdetto #133. Il verdetto non è stato ritoccato.
- **R-135-1/R-135-2 (≥2 citazioni nel diff)**: `DEFERITA — dipende dalla decisione R-135-3 (§0.2)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 +
 gas.py                             |  81 +++++++-
 reports/diff_sessione.md           |  14 +-
 reports/handoff.md                 | 374 +++++++++++++++++++++++--------------
 reports/stato_progetto.md          |  12 +-
 reports/ultimo_report.md           |  40 ++--
 scripts/check_verdetto.py          |  35 +++-
 tests/test_unit_handoff_check.py   |  57 ++++++
 tests/test_unit_kernel.py          | 260 ++++++++++++++++++++++++++
 9 files changed, 705 insertions(+), 174 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
9951563 fix(check_verdetto): risolve citazioni di contesto e nomi corti univoci (F-controlli-auto) — review #135 APPROVATO CON RISERVE
8273d10 chore(revisore): memoria review #135 — APPROVATO CON RISERVE
af4b84d docs(c4b3): fine-task — C4b-3 esito della firma nel contesto del modello, handoff (review #133/#134 APPROVATO CON RISERVE)
4065091 feat(c4b3): esito della firma nel contesto del modello — review #133/#134 APPROVATO CON RISERVE
626b44d chore(revisore): memoria review #134 — APPROVATO CON RISERVE
c964d62 chore(revisore): memoria review #133 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. `af4b84d` è il primo giro di fine-task: il gate B l'ha fermato prima del push, ed è stato superato da questo secondo giro.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore `4065091`, con due verdetti in sequenza: la #133 sul primo diff e la #134 sul diff finale, che chiude R-c4b3-1 e R-c4b3-2. Commit `9951563` (tocca tests/): verdetto #135. Tutti e tre sono incollati per intero.

### Verdetto #133

# Review #133: fetta C4b-3 (feat/cancello-c4b3)

## VERDETTO: APPROVATO CON RISERVE

La riserva R-c4b3-1 va chiusa prima del deploy autonomo, che resta vietato.

**Letture fatte prima della review:** CLAUDE.md (sez. 5, 6, 8, 9), stato_progetto.md (grep su C4b/R-c4b2) e memoria_revisore.md, applicata la lezione su "eseguita ≠ effetto avvenuto" (#131/#132).

**Diff esaminato:** `git diff --cached`, cioè gas.py (+64/-2) e tests/test_unit_kernel.py (+224).

## Misure riprodotte
- `.venv/bin/python tests/test_unit_kernel.py`: **635 PASS / 5 FAIL**. I 5 FAIL sono solo F-mac-1 (T11c2, T11e, T12a, T12c, T12e).
- `pytest tests --ignore=tests/test_unit_kernel.py`: **232 passed**.
- **Mutation test** su una copia nello scratchpad, il repo non è stato toccato. Tutte e 7 le mutazioni fanno cadere almeno un test:
  - M1: dedup disattivato. Cade solo T78h.
  - M2: tolto `name` dal messaggio tool. Cadono T78a e T78e (contaminazione).
  - M3: `dry_run=False`. Cade T78g, 2 check.
  - M4: tolto il blocco per il rifiuto. Cade T78d, 2 check.
  - M5: tolto `_save_history`. Cade T78a (disco e riavvio).
  - M6: args inseriti nella notifica. Cade T78a.
  - M7: `eseguita=True` fisso. Cadono T78f e T78g.

## Elementi del diff esaminati
1. **gas.py:1312-1348 `_storia_esito_firma`.** Aggiunge in coda alla storia un blocco che parte da `user`. È costruito per intero e poi aggiunto con `extend` (tutto o niente), salvato con `_save_history`, e ogni errore finisce in un `except` con `logging.warning`.
   - Rischi esaminati: ancora di `_get_window`, tool orfani, crash, uso di LLM.
   - Verifiche: la finestra del turno dopo parte da `user` e non ha orfani (T78b, e l'ho rifatto con una sonda). `history=None` non solleva eccezioni (T78j). `_NoLLM78` conferma che non c'è nessuna chiamata LLM.
   - Esito: **ok**.
2. **gas.py:1326 dedup sul tag.** La scansione con `tag in content` regge a contenuti non stringa senza sollevare eccezioni. Il tag sopravvive anche alla compressione, perché sta nei primi 300 caratteri del riepilogo.
   - Esito: **ok**. Nota: T78c non prova il dedup, vedi R-c4b3-2.
3. **gas.py:1418-1419 R-c4b2-9.** `dry_run = out.lstrip().startswith("[DRY-RUN]")`.
   - Rischio esaminato: il flag si può falsificare con il contenuto dell'output.
   - Esito: **riserva R-c4b3-1**, verificata (dettagli sotto).
4. **gas.py:1381/1393/1400/1427 punti di chiamata.** Il blocco viene scritto per: rifiuto, firma non riconosciuta, hash non integro, esito dopo il reclamo. Non viene scritto per: pending, ID inesistente, store assente, reclamo fallito.
   - Esito: **ok**, coerente con il design §4b passo 9 (T78i conferma che la storia resta invariata).
5. **tests/test_unit_kernel.py:6337 `_disco78[-4:]`.** È l'unico slicing presente nel diff. Confronta una lista letta da disco dentro un test e non costruisce payload per i provider.
   - Esito: **ok**, non è il caso del Wall of Shame.
6. **tests/test_unit_kernel.py:6397 T78e.** Un `read_file` approvato rende contaminata la finestra; `run_command` no, come nel loop (gas.py:942).
   - Esito: **ok**. Con la mutazione M2 il test cade, quindi è portante.

## Giudizio sui 4 punti chiesti
1. **NO Tool Simulation e `_get_window`: coerente.**
   - L'output nel ruolo `tool` è quello reale di `execute_tool_call`.
   - La tool_call ricostruita porta gli args salvati, verificati via hash, cioè quelli che il modello aveva chiesto nel turno A.
   - È dichiarata come atto del kernel dalla notifica `user` che la precede.
   - Non si inventa nessun output. Il precedente del riepilogo di `_compress_history_if_needed` è pertinente.
   - `_get_window` e `_cap_window_chars` non sono stati toccati.
2. **Compatibilità provider: ok.**
   - Lo schema `assistant(tool_calls, senza content) → tool(tool_call_id, name)` è identico a quello di `_add_to_history` del loop (gas.py:738).
   - L'id `firma_<32hex>` è lungo 38 caratteri e usa solo `[A-Za-z0-9_]`.
   - Gemini 2.5 in modalità OpenAI-compat non convalida gli id né le thought signature (solo Gemini 3 le richiede). Groq, Llama su OpenRouter e Ollama accettano id arbitrari.
   - Non verificato dal vivo: vedi i rischi esclusi.
3. **Concorrenza: ok come limite dichiarato.**
   - bot.py:282 e bot.py:417/360 girano nello stesso loop di polling, a thread singolo.
   - Un processo CLI separato con lo stesso root sovrascrive la storia (vince l'ultima scrittura): il limite c'era già e ora il blocco può andare perso. Va tracciato.
4. **`expired` resta fuori dalla storia (C5): coerente.** La revoca per invio fallito arriva già al modello nell'output del turno A.

## Riserve
- **R-c4b3-1 (da chiudere prima del deploy, verificata empiricamente).** Il flag "eseguita" viene ricavato dal prefisso dell'output grezzo.
  - Con una sonda (root con git init, `os_with_fallback`) ho approvato ed eseguito `run_command` con `echo [DRY-RUN] finto`. Risultato: `[OK] exit=0`, ma `eseguita=False`. Il modello riceve "NON è stata eseguita (modalità dry-run)" e l'operatore vede ⚠️.
  - Stesso difetto, già presente da R-c4b2-3, con stdout che inizia per "Operazione negata": il risultato diventa `[KO]` e `eseguita=False`.
  - La novità di C4b-3: questa informazione falsa ora entra nel contesto del modello insieme a "una nuova richiesta richiede una nuova firma". Il modello può chiedere di nuovo un'azione già eseguita, e l'operatore, che l'ha vista "non eseguita", può firmarla due volte.
  - Correzione: ricavare il dry-run da un segnale strutturato del kernel (per `run_command`: `self.shell_mode == "dry_run"` e `_run_command_meta is None`, cioè l'esito "[OK] (non eseguito)"), e il [KO] dai rami di diniego del kernel, non da startswith sull'output. Aggiungere un test con `echo "[DRY-RUN] x"` approvato ed eseguito davvero.
- **R-c4b3-2 (cosmetica, test).** T78c (riga 6367) non prova il dedup: con M1 resta verde, perché sul percorso approvato il reclamo fallito esce prima di arrivare a `_storia_esito_firma`. Il dedup è coperto solo da T78h. Rinominare il test o aggiungere un caso sul rifiuto ripetuto.
- **R-c4b3-3 (minore, affine a R-c4b2-8).** Se il processo cade tra `reclama_esecuzione` e `_storia_esito_firma` (per esempio durante un `run_command` che dura fino a 60 s), il reclamo esiste ma l'esito non entra mai in storia. Il ri-click si ferma su "già eseguita o non reclamabile".
- **R-c4b3-4 (dichiarata).** Il blocco viene sovrascritto se un processo CLI separato salva la storia sullo stesso root (vince l'ultima scrittura, limite già esistente). Va tracciata in stato_progetto.md.

## Rischi esplicitamente esclusi
- **Accettazione reale da parte dei provider** della sequenza con id `firma_<hex>`: non verificata, perché la suite usa provider finti e un ping reale consumerebbe quota. La compatibilità è dedotta dal fatto che lo schema è identico ai messaggi del loop, che oggi i provider accettano.
- **Click reale su Telegram end-to-end:** non riproducibile in un ambiente di sviluppo senza operatore.
- **Comportamento con bwrap su VPS:** il sandbox OS non c'è su Mac (F-mac-1).

## Memoria
- Aggiunta la riga #133 in /Users/gas/Gas/.claude/agents/memoria_revisore.md, più una lezione: "flag di esito da startswith sull'output grezzo è falsificabile dal contenuto; usare un segnale strutturato del kernel".
- Committata con `scripts/commit_memoria_revisore.sh`: commit `c964d62`, solo quel file; l'index con gas.py e i test resta intatto in staging.

Il commit del diff è consentito (APPROVATO CON RISERVE). R-c4b3-1, R-c4b3-2, R-c4b3-3 e R-c4b3-4 vanno tracciate in /Users/gas/Gas/reports/stato_progetto.md.

### Verdetto #134

# Review #134 (seguito della #133): C4b-3, chiusura di R-c4b3-1 e R-c4b3-2

## VERDETTO: APPROVATO CON RISERVE

Il diff si può committare. R-c4b3-1 e R-c4b3-2 sono **chiuse**. Resta una riserva nuova, minore (R-c4b3-5), più R-c4b3-3 e R-c4b3-4 che hai già dichiarato.

Il verdetto #133, già consegnato, resta nella storia. Questo lo segue e copre il diff staged attuale: gas.py +81/-3, tests/test_unit_kernel.py +260.

## Misure riprodotte
- Kernel: **643 PASS / 5 FAIL**, solo F-mac-1 (T11c2, T11e, T12a, T12c, T12e).
- pytest senza test_unit_kernel.py: **232 passed**.

**Mutation test** su una copia nello scratchpad, repo non toccato:

| Mutazione | Esito | Test che la uccide |
|---|---|---|
| N1: `eseguita` di nuovo dal prefisso | uccisa | T78g, 2 check |
| N2: tolto il reset di `_run_command_meta` | uccisa | T78k-bis |
| N3: tolto il ricalcolo dell'esito da meta | uccisa | T78k sul caso "Operazione negata", sia in res sia in approval_esecuzioni (`[('[KO]',)]`) |
| N4: dedup disattivato | uccisa | T78d (nuovo check sul rifiuto ripetuto) e T78h. Il dedup ora è portante (R-c4b3-2 chiusa) |
| N5: `dry_run` senza `meta is None and shell_mode == "dry_run"` | sopravvive, 643/5 | nessuno |

N5 non è un problema: quando meta c'è, `eseguita` è True e l'etichetta dry-run non viene mai mostrata. La condizione è difesa in profondità e non regge nulla da sola. Lo noto, non è una riserva.

## Elementi del diff esaminati
1. **gas.py:1410, `self._run_command_meta = None` subito dopo `reclama_esecuzione`.**
   - Rischio: un meta rimasto da un run_command precedente (turno del loop) fa sembrare eseguito un DENY al ricontrollo.
   - Esito: **ok**. È portante: la mutazione N2 la fa cadere su T78k-bis.
   - Ho verificato che execute_tool_call la azzera di nuovo all'ingresso (gas.py:1894) e la valorizza solo dopo `subprocess.run` (gas.py:1942).
2. **gas.py:1420-1432, ramo `run_command`.** `esito = _esito_diario(tool, "")` quando meta c'è, `eseguita = meta is not None`.
   - Rischio: l'output di terzi che decide l'esito (la sonda #133).
   - Esito: **ok**. T78k usa `echo '[DRY-RUN] finto'` e `echo 'Operazione negata: finto'` eseguiti davvero: entrambi danno [OK] exit=0, ✅ e "— eseguita.".
   - Lasciare `_esito_diario` com'è (gas.py:1199) è la scelta giusta: anteporre il controllo su meta avrebbe trasformato in [OK] i DENY e i parcheggi del loop con meta residuo.
3. **gas.py, ramo `else`: gli altri tool parcheggiabili restano su `not esito.startswith("[KO]")`.**
   - Rischio: il loro output è testo di terzi?
   - Esito: **ok**. write_file, salva_contatto e imposta_stato_contatto restituiscono testo che inizia con una formula fissa del kernel. read_file non arriva al cancello nel flusso reale, ma T78e lo accoda a mano.
4. **tests/test_unit_kernel.py:6387 (T78d, dedup sul rifiuto) e :6458-6465 (T78k-bis).** Sono test nuovi e portanti, confermato da N2 e N4. Esito: **ok**.

## Riserve
- **R-c4b3-5 (nuova, minore, verificata).** Il timeout di `subprocess.run` (60 s) non valorizza meta, quindi `eseguita=False`, esito [KO], e il modello legge "NON è stata eseguita (**diniego interno**)".
  - In realtà il processo è partito ed è stato ucciso a 60 s, quindi può aver prodotto effetti parziali.
  - Sonda (`subprocess.run` monkeypatchato che solleva TimeoutExpired): output "Errore eseguendo run_command: ... timed out", notifica "diniego interno".
  - Il flag `eseguita=False` c'era già prima di C4b-3. L'etichetta "diniego interno" che arriva al modello è nuova.
  - Mitigazione: il messaggio tool che segue dice "timed out".
  - Correzione: distinguere tre casi, cioè non avviata, completata, avviata con esito incerto (timeout o eccezione dopo l'avvio), e dare a operatore e modello la dicitura "esito incerto".
- **R-c4b3-3 e R-c4b3-4:** restano aperte come le hai dichiarate. Vanno tracciate in stato_progetto.md, come hai detto.

## Rischi esplicitamente esclusi
- **Tool non-run_command con output costruito da input di terzi** (es. un messaggio di salva_contatto che inizia con un campo fornito dall'utente): non ho letto ogni formato di ritorno. Ho controllato solo che i rami principali inizino con testo fisso del kernel.
- **Timeout reale di 60 s con bwrap su VPS:** non riproducibile in dev. L'ho simulato con un monkeypatch.
- **Accettazione reale della sequenza da parte dei provider:** fuori scope di questo delta, lo schema è invariato rispetto alla #133.

## Memoria
- Aggiunta la riga #134 in /Users/gas/Gas/.claude/agents/memoria_revisore.md, con una lezione nuova: un segnale "partito davvero" valorizzato dopo la chiamata bloccante vuol dire in realtà "completato"; servono tre stati, e va provato con TimeoutExpired.
- Committata con scripts/commit_memoria_revisore.sh nel commit `626b44d`, che contiene solo quel file. Il diff del motore resta in staging.

### Verdetto #135 (commit `9951563`, scripts/check_verdetto.py + tests/test_unit_handoff_check.py)

# Review #135: F-controlli-auto in scripts/check_verdetto.py

## VERDETTO: APPROVATO CON RISERVE

Puoi committare e pushare. Su `af4b84d` non c'è nulla che blocchi. La correzione del falso positivo funziona. Però il gate allentato ha perso un legame che prima garantiva senza dirlo (R-135-1), e consiglio di ripristinarlo presto.

Diff esaminato: `git diff --cached`, cioè scripts/check_verdetto.py (+35/-5) e tests/test_unit_handoff_check.py (+57).

## Misure riprodotte
- `pytest tests/test_unit_handoff_check.py`: 16 passed.
- pytest senza test_unit_kernel.py: 237 passed.
- `scripts/check_verdetto.py` sull'handoff reale: OK, 16 riferimenti.

## Elementi del diff esaminati
1. **scripts/check_verdetto.py:84-93, `_resolve_path`.** Risolve il path in quest'ordine: diff di sessione, poi path esatto a HEAD, poi nome corto che è suffisso `/<nome>` di un solo file.
   - Rischio esaminato: risoluzione sbagliata o ambigua.
   - Esito: ok. Il nome ambiguo dà exit 1 (test a :415). Se `bot.py` esiste sia nella radice sia in sottocartella vince il path esatto, quindi il risultato è deterministico. Il controllo sul numero di riga a :158 usa il path risolto, corretto.
2. **scripts/check_verdetto.py:86, `if path in session or path in head`.**
   - Rischio esaminato: il gate si allenta.
   - Esito: **riserva R-135-1**, verificata.
3. **scripts/check_verdetto.py:77, `_head_files`.** Usa `ls-tree -r` con quotePath=false, coerente con `_session_files`. Se git fallisce restituisce un insieme vuoto, cioè una citazione di contesto viene rifiutata: è fail-closed.
   - Esito: ok.
4. **tests/test_unit_handoff_check.py:394-427.** I 5 test coprono: path completo, nome corto, riga oltre la fine, nome ambiguo, file inesistente.
   - Esito: ok. Manca il caso degenere "solo file di contesto", vedi R-135-1.

## Il mio giudizio sull'allentamento (la tua domanda)
L'allentamento è giusto nel principio. Citare file di contesto è buona pratica: il mio #133 doveva citare bot.py:282/417 per argomentare sulla concorrenza.

La vecchia regola stretta ("ogni citazione nel diff") però garantiva implicitamente che almeno una citazione stesse nel diff. Adesso questa garanzia è sparita.

- **R-135-1 (verificata con una sonda):** un §4 che contiene solo `modules/telegram/bot.py:3 e bot.py:4`, senza nessun file del diff, ora dà rc=0 ("OK — 2 riferimento/i").
  - Correzione: contare le citazioni il cui path risolto è in `session` e richiedere ≥2, come chiede il formato del verdetto in revisore.md. Le citazioni di contesto restano ammesse in aggiunta.
  - Aggiungere il test "solo contesto → exit 1".
- **R-135-2 (c'era già, verificata, più grave):** un §4 senza alcun `path:riga`, per esempio "APPROVATO — nessuna lezione nuova", dà rc=0 alla riga 150 ("nulla da verificare"). Il gate accetta proprio il verdetto nullo che dovrebbe rifiutare. Si chiude con la stessa correzione di R-135-1 (≥2 citazioni nel diff), tenendo l'eccezione "nessun diff motore".
- **R-135-3 (decisione umana, ammissione mia):** revisore.md dice "citare un file non presente nel diff invalida il verdetto". Letto alla lettera, il mio verdetto #133 non era conforme, perché citava bot.py:282/417/360 come contesto. Conteneva comunque i ≥2 elementi del diff richiesti (gas.py:1312, :1418, test :6337/:6397).
  - Proposta: riscrivere la regola come "≥2 elementi nel diff, citazioni di contesto ammesse e verificate a HEAD", e allineare il gate a quella regola.
  - Non tocco io revisore.md: è configurazione e la decide l'operatore.
  - La NOTA "MITIGATO, non chiuso" resta corretta.

## Rischi esplicitamente esclusi
- **Numeri di riga verificati su HEAD anziché sullo snapshot staged revisionato:** non l'ho verificato. Il disallineamento è possibile se il codice cambia dopo la review, ma è un limite che esisteva già e non è toccato da questo diff.
- **Comportamento di `fine_task_finale.sh` end-to-end con il nuovo gate:** non rilanciato. Ho eseguito solo `check_verdetto.py` sull'handoff reale.

## Memoria
- Aggiunta la riga #135 in /Users/gas/Gas/.claude/agents/memoria_revisore.md, più una lezione: quando si allenta un gate, reintrodurre in modo esplicito la proprietà che la regola stretta garantiva senza dirlo, e provare sempre l'input degenere.
- Committata con `scripts/commit_memoria_revisore.sh` in `8273d10`, solo quel file. L'index con check_verdetto.py e i test resta in staging.

Riserve da tracciare in /Users/gas/Gas/reports/stato_progetto.md: R-135-1, R-135-2, R-135-3.

## §5 DELTA TEST DEL MOTORE

`python tests/test_unit_kernel.py`: **614 → 643 PASS / 5 FAIL** (+29 check T78a-k). Riepilogo reale sul commit `4065091`:

```
=== RIEPILOGO: 643 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
```

I 5 FAIL sono fuori scope: F-mac-1, bwrap assente su macOS, invariati rispetto a main. `pytest tests --ignore=tests/test_unit_kernel.py`: 232 → **237 passed** (5 test nuovi in `tests/test_unit_handoff_check.py`, commit `9951563`).

## §6 STATO CI

```
completed	success	feat(c4b3): esito della firma nel contesto del modello — review #133/…	CI	feat/cancello-c4b3	push	37142066635	57s	2026-10-03T17:51:47Z
completed	success	Merge pull request #116 from Gasss23/feat/cancello-c4b2	CI	main	push	37140766609	1m33s	2026-10-03T17:30:34Z
completed	success	docs(c4b2): fine-task — C4b-2 bottoni di firma + esecuzione post-appr…	CI	feat/cancello-c4b2	push	37140679398	57s	2026-10-03T17:29:15Z
```

Mappatura commit→run:
- `4065091` (motore): run **37142066635**, success. È la testa del push che conteneva anche `c964d62` e `626b44d`.
- `626b44d` (memoria revisore): nessuna run su questo SHA. Era un commit intermedio dello stesso push e il suo contenuto è incluso nell'albero testato da 37142066635.
- `c964d62` (memoria revisore): nessuna run su questo SHA, per lo stesso motivo.
- `af4b84d`, `8273d10`, `9951563`: run non ancora disponibile alla scrittura dell'handoff (non ancora pushati).
- Commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-c4b3-3** (minore): se il processo cade tra il reclamo e la scrittura in storia, l'esito non entra mai in storia.
- **R-c4b3-4** (dichiarata): un processo CLI separato sulla stessa root può sovrascrivere `.gas_history.json` e perdere il blocco.
- **R-c4b3-5** (minore): un timeout di `run_command` viene raccontato come "diniego interno" invece che come "esito incerto".
- **R-135-1** (verificata): un §4 che cita SOLO file di contesto passa il gate B.
- **R-135-2** (preesistente, più grave): un §4 senza alcun `path:riga` passa il gate B ("nulla da verificare").
- **R-135-3** (decisione umana): regola di revisore.md sulle citazioni fuori dal diff (§0.2).
- Ancora aperte da C4b-2: R-c4b2-6, R-c4b2-7, R-c4b2-8, R-c4b2-10.
- Anomalia di processo: il marcatore `.claude/.review_ok` è rimasto da C4b-2 (creato alle 19:26), quindi il gate deterministico era aperto a inizio sessione. Ora è rimosso.
