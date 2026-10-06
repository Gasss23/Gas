# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-06 — R-150-1: push fallito in fine_task_finale.sh esce dal suo ramo (sessione cloud notturna, arretrati)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #133 (https://github.com/Gasss23/Gas/pull/133). Numero e URL dall'output del connettore GitHub (`create_pull_request` → `{"id":"4756569535","url":"https://github.com/Gasss23/Gas/pull/133"}`): `gh` non è autenticato in questo container.
2. Ordine di merge della notte: i report canonici (`reports/`) sono riscritti da ogni PR; dopo un merge, le altre vanno riallineate a main (conflitto solo su `reports/`).

---

## §1 SCOPE & ESITO FETTE

- **R-150-1 — ramo PUSH_EXIT morto sotto `set -e`**: `FATTA` — `git push || PUSH_EXIT=$?`.
- **Test T-finale-5**: `FATTA` — fallisce sul codice vecchio, passa col fix.
- **R-166-1 / R-166-2** (dalla review #166): `FATTA` nello stesso commit.
- **Etichetta `verifica`**: `SALTATA — gh non autenticato e l'etichetta non esiste ancora`.
- **Verifica esterna §4quater**: `FATTA` — #133 APPROVATO CON RISERVE (§8).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 reports/diff_sessione.md           |  19 +++++++-----------
 reports/handoff.md                 | 390 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  25 +++++++----------------
 scripts/fine_task_finale.sh        |   6 ++++--
 tests/test_unit_hooks.py           |  37 ++++++++++++++++++++++++++++++++++
 7 files changed, 146 insertions(+), 336 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
3e3ca97 docs(fine-task-push-exit): fine-task — report, handoff con verdetti #166/#168, diff sessione
53c1f6d fix(fine-task): R-150-1 — push fallito esce dal suo ramo con messaggio ed exit 1 — review #166/#168
cc49a01 chore(revisore): memoria review #168 — APPROVATO
9345199 chore(revisore): memoria review #168 — APPROVATO
f89a42b chore(revisore): memoria review #163 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

## §4 VERDETTO DEL REVISORE (per commit motore)

Verdetti INTEGRALI. Unica trasformazione meccanica: i path assoluti del worktree (`/home/user/wt-push/`) sono stati resi relativi alla radice del repo, perché il gate B li risolva. La #166 era stata numerata #163 dal revisore (collisione con la #163 della PR #131): il testo è invariato, nel testo le sue riserve si chiamano ancora R-163-1/R-163-2 = R-166-1/R-166-2.

### Review #166 (numerata #163 nel testo) — diff staged del fix

## VERDETTO: APPROVATO CON RISERVE

Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e 10, nel contesto), la voce R-150 in `reports/stato_progetto.md` e la mia memoria (`.claude/agents/memoria_revisore.md`, dalla #150 alla #162).

**Cosa ho guardato nel diff**

1. `scripts/fine_task_finale.sh:133` — `PUSH_EXIT=0; git push || PUSH_EXIT=$?`. Con `set -e` di nuovo attivo, il comando a sinistra di `||` non fa uscire la shell, quindi il ramo di `:135` ("ERRORE git push fallito", exit 1) ora viene raggiunto. Ho controllato che `set -e` resti attivo in tutti i percorsi che arrivano al push: è riattivato a `:76` dopo la prima `git grep`, sia con rc 1 sia con rc 0. Ho controllato anche che non nasconda un push fallito: `PUSH_EXIT` è inizializzato e il `-ne 0` esce comunque. **Esito: ok.**
2. `tests/test_unit_hooks.py:1915` — il nuovo T-finale-5: un repo bare con `pre-receive` (`:1936`) che risponde `exit 1`, e il branch ha già un upstream. Il test controlla exit 1, la presenza del messaggio in stderr e che non esca nessun URL_HANDOFF. Il rischio era che il test passasse anche senza il fix. L'ho provato: con lo script di HEAD rimesso nel worktree, T-finale-5 **fallisce** sull'assert del messaggio (stderr contiene solo `! [remote rejected] ... pre-receive hook declined`, returncode già 1). Poi ho ripristinato il file: lo staged è intatto e il worktree pulito. Con il fix: `pytest tests/test_unit_hooks.py` → **103 passed**, riprodotto. **Esito: ok.**
3. `scripts/fine_task_finale.sh:140` (contesto, non toccato) — la guardia HEAD==@{u} (`git fetch ... || true`, `REMOTE=$(... || true)`, confronto) è identica byte per byte. Il fix cambia solo il percorso di errore del push. **Esito: ok.**
4. `reports/stato_progetto.md:22` — R-150-1 è marcata CHIUSA, con il riferimento al branch e al test. **Esito: riserva (R-163-1).**

**Riserve**
- **R-163-1 (BASSA, doc):** la voce dice ancora che il push fallito "esce con 128". Il caso testato (push rifiutato) esce invece con 1. Il 128 vale solo per i `fatal` di git, come scrivi tu stesso nella descrizione della PR. Va corretta la frase, così il report non contraddice il test.
- **R-163-2 (BASSA, copertura):** ho ragionato sulla mutation che toglie `exit 1` a `:136`, senza eseguirla. Il test la lascerebbe sopravvivere: il messaggio viene stampato lo stesso e poi la guardia @{u} esce con 1 senza URL. Si fermerebbe comunque con errore, quindi va bene, ma il test non prova che l'uscita avvenga proprio in quel ramo. Si chiude asserendo che in stderr non compaia `HEAD (`.

**Coerenza col progetto:** il diff non tocca il motore (gas.py, brains, modules). Rafforza la macchina di controllo ("zero crash", messaggi chiari) senza indebolire nessun gate: i gate A, B e IP e la guardia @{u} sono invariati. Nessun antipattern del Wall of Shame.

**Cosa non ho verificato:**
- Il caso di push fallito per errore di rete o di autenticazione (exit 128) sul remoto GitHub reale. In dev non si riproduce senza toccare il remoto. Il fix non dipende dal codice di uscita, quindi lo copre per costruzione, ma senza un test.
- L'esecuzione in CI.

Riga contatore #163 scritta in `.claude/agents/memoria_revisore.md`, più una lezione: un test di un ramo d'errore deve asserire il messaggio, non solo l'exit code. Committata da sola con lo script atomico (`f89a42b`). Il diff staged NON è stato committato.

### Review #168 — diff staged finale

## VERDETTO: APPROVATO

Ho riletto le voci #150 e #160–#166 della memoria e la voce R-150 di `reports/stato_progetto.md`; CLAUDE.md era nel contesto. Le due riserve della #166 sono chiuse e lo script si comporta come prima.

**Cosa ho esaminato nel diff**

1. `tests/test_unit_hooks.py:1949` — nuova riga `assert "HEAD (" not in result.stderr`.
   - **Rischio:** il test passava anche se lo script usciva dalla guardia @{u} invece che dal ramo del push (R-166-2).
   - **Prova:** ho sostituito `exit 1` con `:` a `scripts/fine_task_finale.sh:136` e T-finale-5 fallisce (1 failed). Anche con lo script di HEAD il test fallisce. Poi ho ripristinato il file: il worktree è pulito e lo staged è intatto.
   - **Esito:** ok.
2. `reports/stato_progetto.md:22` — la frase ora dice "usciva col codice di git (1 se il remoto rifiuta, 128 per i `fatal`)".
   - **Rischio:** che il report contraddica il test (R-166-1).
   - **Esito:** ok, ora corrisponde a quello che ho osservato (rifiuto di `pre-receive` → 1).
3. `scripts/fine_task_finale.sh:133` — `git push || PUSH_EXIT=$?`, invariato rispetto alla #166.
   - **Controllo:** la guardia HEAD==@{u} a `:140` e seguenti è ancora identica.
   - **Esito:** ok.
4. `.claude/agents/memoria_revisore.md` — la mia riga è stata rinumerata da #163 a #166 e le riserve da R-163 a R-166, con una nota che spiega perché.
   - **Esito:** ok, preso atto. Nella memoria manca la #167: non è una review mia, quindi va fatta tornare la continuità del contatore sull'altro branch.

**Test:** `pytest tests/test_unit_hooks.py` → 103 passed, rieseguito da me.

**Cosa non ho verificato:**
- Un push fallito per un `fatal` (exit 128) su GitHub reale: in dev non si riproduce senza toccare il remoto. Il fix non dipende dal codice di uscita, quindi lo copre comunque, ma senza un test dedicato.
- La run in CI.

**Coerenza:** il diff tocca solo la macchina di controllo, non il motore. Nessun gate è indebolito e non ci sono antipattern del Wall of Shame.

**Memoria:** ho aggiunto la riga #168 in `.claude/agents/memoria_revisore.md` e l'ho committata con lo script atomico, in due commit: `9345199`, poi `cc49a01` per correggere un riferimento di riga, da :1947 a :1949. Lo script committa il file intero, quindi questi commit includono anche la tua rinumerazione #163→#166 che era in stage. Il diff staged del task non è stato committato.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules. Test della macchina di controllo: `tests/test_unit_hooks.py` 102 → 103 passed (+T-finale-5), eseguito in questo container (Linux, bwrap presente). Suite kernel non toccata dal diff.

## §6 STATO CI

Stato letto col connettore GitHub (`actions_list`, `gh` non autenticato). Mappatura commit → run:
- `f89a42b`, `9345199`, `cc49a01`, `53c1f6d`: pushati insieme → run 37440692564 (CI #659) su `53c1f6d`: **failure** — atteso, handoff non ancora rigenerato (handoff-check).
- `3e3ca97` (primo fine-task): run 37440758192 (CI #660): **success**.
- commit di questo fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Push fallito per `fatal` (exit 128) su GitHub reale: coperto per costruzione, non testato (#166/#168; V-3 della verifica esterna #133: fattibile con un remote inesistente).
- Contatore delle review fra branch non mergiati (#163/#166/#167…): riallineare al merge (V-4 verifica esterna #133).

## §8 VERIFICA ESTERNA #133 (verdetto integrale)

Lanciata da questo agente con `Applica .claude/verifica_esterna.md a: <URL_HANDOFF di 3e3ca97> <URL_PR>` (agente nuovo, Sonnet). Esito: APPROVATO CON RISERVE, solo BASSE/COSMETICHE; nessuna correzione al codice. V-1/V-2 (handoff con stat e CI fotografati prima dell'ultimo commit) sono strutturali e qui aggiornati.

VERIFICA ESTERNA PR #133 — APPROVATO CON RISERVE

Metodo: clone usa-e-getta nella scratchpad, checkout di 3e3ca97 (commit pinnato dall'URL), merge-base con origin/main = e91ceb4. Ho eseguito:
- `git diff --stat` e `git log` dalla base;
- `pytest tests/test_unit_hooks.py` alla base e al commit;
- due mutation sullo script, più lo script della base rimesso al posto del fix;
- le API GitHub per il ruleset e per i check-run.

`git status` del repo reale è vuoto.

CLAIM VERIFICATI:
- **Fix R-150-1, VERO.** In `scripts/fine_task_finale.sh` il diff è solo `PUSH_EXIT=0; git push || PUSH_EXIT=$?`. Con `set -e` attivo (riattivato dopo il gate IP) il ramo "ERRORE git push fallito"/exit 1 ora è raggiungibile. La guardia HEAD==@{u} e il gate IP sono invariati (letti nel diff e nel sorgente).
- **Delta test, VERO.** `tests/test_unit_hooks.py` passa da 102 passed alla base a 103 passed al commit, riprodotti.
- **T-finale-5 discrimina, VERO.** Con lo script della base fallisce sull'assert del messaggio, e con la mutation `|| PUSH_EXIT=0` fallisce anch'esso. Con il fix passa.
- **Riserve R-166-1 e R-166-2 CHIUSE, VERO.**
  - `stato_progetto.md` ora dice "1 se il remoto rifiuta, 128 per i fatal".
  - La riga `"HEAD (" not in stderr` è presente nel test. Come dichiarato dal revisore, la mutation `exit 1` → `:` è coperta da questo assert. Quella mutation non l'ho rieseguita: la lettura del test non mostra falle.
- **Perimetro, VERO.** `git diff --stat` reale: 7 file (memoria_revisore, diff_sessione, handoff, stato_progetto, ultimo_report, fine_task_finale.sh, test_unit_hooks.py). Il log reale ha i 5 commit dichiarati, 4 più quello di fine-task, come il handoff dice. Il fix non tocca motore né gate; `scripts/fine_task_finale.sh` e `tests/` sono nel perimetro di review e hanno i verdetti #166 e #168.
- **CI, VERO.** Sullo SHA 3e3ca97 `handoff-check` è success e `unit-suite` è completed/success. `verifica`, `esito` e `smista` sono skipped. Il ruleset `main-lock` (attivo) richiede esattamente `unit-suite` e `handoff-check`.
- **PR #133, VERO.** Stato open, head 3e3ca97, base main, 7 file cambiati.

FINDING:
- **V-1 (COSMETICA).** Il §2 del handoff riporta `reports/handoff.md | 362` e un totale di "112 insertions, 342 deletions". Il diff reale a 3e3ca97 è 372 righe per handoff.md e 122 insertions. La differenza dipende dal fatto che il file è autoreferenziale: la stat è presa prima dell'ultima riscrittura. Nessun impatto sostanziale. Fix: ricalcolare la stat dopo l'ultima modifica, oppure dichiarare l'approssimazione.
- **V-2 (BASSA).** Nel §6 del handoff, "CI NON VERIFICATA" era vero alla scrittura. Ora la CI è verde, quindi la riserva sulla CI è chiusa a posteriori.
- **V-3 (BASSA).** La riserva aperta nel §7 (push con `fatal`, exit 128) resta non testata, ma è coperta per costruzione: `|| PUSH_EXIT=$?` non dipende dal codice di uscita. Rischio basso. Un test dedicato è fattibile con un remote inesistente.
- **V-4 (BASSA).** Il contatore del revisore salta la #167 e la #163 è rinumerata in #166. Il handoff e la memoria lo dichiarano, ma resta da riallineare con l'altro branch (la #163 è su feat/merge-automatico-z1xjx2). Il rischio è la collisione di numerazione con la PR #131, e il handoff lo segnala già.

NON VERIFICATO:
- Il push fallito per rete o auth (128) su GitHub reale: non riproducibile senza toccare il remoto.
- L'etichetta `verifica` e il workflow `verifica-bot`: i job risultano skipped e non ho potuto esaminare perché.
- L'ordine di merge e i conflitti con le altre PR notturne su `reports/`: dichiarati dal handoff, non provati.

RACCOMANDAZIONE: la PR si può mergiare. Il fix è corretto, minimale, coperto da un test che discrimina, e i due check required sono verdi. Prima di altro lavoro: riallineare il contatore del revisore (#163/#166/#167) tra i branch, e, se serve, aggiungere un test per il caso 128.
