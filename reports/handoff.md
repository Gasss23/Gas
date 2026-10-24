# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-24 — Chat Motore: R2 via B fetta 3 (note BASSE del cervello forte chiuse, ancora spento)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #262 (https://github.com/Gasss23/Gas/pull/262): tocca motore e template fine-task; ultima review #503 APPROVATO.
2. Prima di accendere il forte: prova sul Mac di `claude -p` col login Max di Gas (R-496-3).
3. Testo nuovo dell'attività di notte da chiedere nella sessione fissa; 3 lezioni da approvare sul Mac.

---

## §1 SCOPE & ESITO FETTE

- **Costo su ogni errore (R-497-1)**: `FATTA`.
- **Prezzo per famiglia e pavimento (V-1 bot/ve #258)**: `FATTA`.
- **Conto sotto lucchetto, attesa limitata, forte fermo se il consumo non si registra (R-496-2, R-502-1/2)**: `FATTA`.
- **Costi non finiti (V-4 ve #258)**: `FATTA`.
- **Doctor «Cervello forte» (R-497-2)**: `FATTA`.
- **Messaggio dei file protetti (R-498-1), deroga n/d nel template (R-501-1)**: `FATTA`.
- **Campo `cervello: forte` nel catalogo notturno, setup del Mac**: `DEFERITA — dopo la prova del login`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 .claude/commands/fine-task.md      |   4 ++--
 .gitignore                         |   1 +
 brains/claude_cli.py               | 122 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------
 gas.py                             | 132 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------
 reports/diff_sessione.md           |  14 ++++++++------
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   4 ++--
 reports/ultimo_report.md           |  25 +++++++++++++------------
 tests/test_unit_claude_cli.py      |  68 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 tests/test_unit_kernel.py          |  44 ++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — la riga di `reports/handoff.md` è n/d e la riga di totale è tolta; le altre righe sono prese con i report già in stage.

## §3 GIT LOG --ONELINE (sessione)

```
9161425 feat(r2): fetta 3 del cervello forte — costo su ogni errore, conto sotto lucchetto, doctor
a779e43 chore(revisore): memoria review #503 — APPROVATO
c1409f7 chore(revisore): memoria review #502 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare nel log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore: 9161425 `feat(r2): fetta 3 del cervello forte`. Due review sullo stesso diff, in ordine.

### Review #502 (APPROVATO CON RISERVE, riserve corrette prima del commit)

## VERDETTO: APPROVATO CON RISERVE

Review #502 (chat Motore). Diff staged in /home/user/Gas: R2 via B fetta 3, con il cervello forte ancora spento. Prima della review ho letto CLAUDE.md (sez. 5, 8, 9, 10), le voci R2 di reports/stato_progetto.md (R-496-2, R-497-1/2, R-498-1) e la memoria. Ho applicato la lezione #496/#498: ogni nuovo file di stato va nella denylist e va provato col kernel reale.

**Elementi del diff esaminati**
- `brains/claude_cli.py:308`: ramo `except RuntimeError` / `except Exception` attorno a `_risposta`. Rischio: che cambi la classificazione QUOTA o il fallback. I RuntimeError escono con il messaggio originale e il «429 » resta in testa. Il costo si aggiunge solo se manca. Solo le eccezioni impreviste vengono avvolte in «risposta non valida», che non è un limite. In `run_turn` il ramo `except` resta uguale: registra il costo e poi `raise`, quindi il fallback non cambia. **ok**
- `brains/claude_cli.py:299`: un JSON che non è un oggetto e un'uscita non JSON portano `stima_minima`, calcolata una sola volta prima del runner. Il prefisso `_prefisso_limite` resta. **ok**
- `brains/claude_cli.py:189`: `_costo_equivalente` usa il prezzo della famiglia del modello. Una famiglia sconosciuta prende 15/75, cioè fail-closed; il pavimento vale anche su `total_cost_usd`. Prove dirette: `_prezzo("x")=(15,75)`; 1e-9 su sonnet dà 0.0015; nessun valore negativo passa. **ok**
- `brains/claude_cli.py:206`: `_token` con `usage` non numerico. Prova diretta: `"abc"` e `inf` danno (0,0) senza eccezioni, perché OverflowError è intercettato. **ok**
- `gas.py:1650`: flock sul file `.lock` attorno a lettura, somma e scrittura. Prova con 4 processi × 50 registrazioni da 0.01: il risultato è 2.0 esatto, nessun aggiornamento perso. Il fail-closed resta: con conto illeggibile la funzione esce sotto lucchetto senza scrivere. **riserva R-502-1**: il `LOCK_EX` è bloccante e senza timeout. La sezione critica è breve e un crash libera il lucchetto, ma un detentore fermo (SIGSTOP, disco lento) blocca il turno all'infinito. Nel repo c'è già la convenzione `LOCK_NB` a `gas.py:1319`.
- `gas.py:1646`: costi infiniti o negativi ignorati con warning; T99m PASS. **ok**
- `.gitignore:55`: lockfile aggiunto. Prova col kernel reale (`execute_tool_call`): `write_file` e `read_file` sono negati su `.gas_claude_cli_uso.json.lock`, `.GAS-claude-cli-uso.json.lock` e `sub/.gas_claude_cli_uso.json.lock`. Lo nega il prefisso esistente a `gas.py:1903`, e lo stesso prefisso c'è nel cancello `modules/gate/gate.py:104`. **ok**
- `gas.py:4887`: sezione «Cervello forte» del doctor. Usa solo `_env_flag`, `shutil.which` e `_leggi_uso_claude_cli`: nessuna chiamata a `claude`, nessun token consumato. Il tetto ha lo stesso default e gli stessi limiti di `_tetto_claude_cli_superato`. T99n PASS e l'ambiente viene ripristinato da `_saved99`. **ok**
- `gas.py:2507`: messaggio di diniego (R-498-1). **ok**
- `.claude/commands/fine-task.md:131`: il segnaposto del §2 e il commento di 4bis citano la regola «n/d»; chiude R-501-1. **ok**

**Controlli generali**
- §5 (Wall of Shame): nessuno slicing della history, nessun output di tool simulato. I test usano runner finti iniettati per la CLI, non risultati di tool inventati.
- §9: le eccezioni restano intercettate. `_registra_uso_claude_cli` non solleva mai e scrive un warning nel log.
- Cap 10 iterazioni: non toccato.

**Test rieseguiti da me**
- `tests/test_unit_claude_cli.py`: 20 passed.
- `tests/test_unit_kernel.py`: 1037 PASS, 0 FAIL.

**Riserve, da tracciare in reports/stato_progetto.md prima di accendere `GAS_CLAUDE_CLI`**
- **R-502-1 BASSA**: `fcntl.flock(..., LOCK_EX)` a `gas.py:1653` è senza timeout dentro il turno. Usare `LOCK_NB` con tentativi limitati: se il lucchetto non arriva, il turno va fermato o il consumo scritto lo stesso, mai un'attesa infinita.
- **R-502-2 BASSA**: se il lockfile non si apre, il lucchetto non si prende o la scrittura fallisce, c'è solo un warning e il consumo non entra nel conto. È fail-open sul tetto (il problema c'era già per `os.replace`; ora si aggiunge il caso del lockfile). Da valutare un fermo del forte quando la registrazione fallisce.
- **R-502-3 COSMETICA**: il ramo `except Exception` generico (`brains/claude_cli.py:308`) non ha un test, e il lockfile manca dalla lista `_TARGETS_68s` (`tests/test_unit_kernel.py:4399`). La protezione l'ho verificata solo a mano.

**Rischi esclusi**
- La CLI `claude` vera non è stata chiamata: il forte è spento e consumerebbe l'abbonamento. Il formato reale di `total_cost_usd` e `usage` resta quello dei test.
- Il lucchetto su macOS e su file system di rete (NFS) non è stato verificato: qui c'è solo Linux locale.
- La suite pytest completa (2141 passed) non l'ho rieseguita io: ho eseguito le due suite toccate.

Riga #502 e una lezione nuova (lucchetti nel turno solo con `LOCK_NB` o timeout) aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md e committate con `scripts/commit_memoria_revisore.sh` (commit c1409f7).

### Review #503 (verdetto finale sul diff committato)

## VERDETTO: APPROVATO

Ho letto prima CLAUDE.md (sez. 5, 8, 9 e 10), poi le righe R2 di reports/stato_progetto.md e infine la memoria del revisore. Questa è la review #503: l'ultima in memoria era la #502.

**Cosa ho controllato nel diff**
- `gas.py:1659` — il lucchetto sul conto ora si prende con `LOCK_EX | LOCK_NB`, riprovando ogni 0,05 s fino a `LOCK_STORIA_SEC` (5 s, `gas.py:1284`, la stessa regola del lucchetto della storia). Scaduto il tempo parte un `TimeoutError` dentro il `with`: il file si chiude e l'errore lo prende l'`except Exception`. Il rischio era che il turno restasse bloccato: non succede. Esito: ok, R-502-1 chiusa.
- `gas.py:1679` — il blocco `finally` accende `_forte_senza_conto` solo se il consumo non è stato registrato e il conto non era già fermo. Rischio esaminato: il flag acceso per sbaglio nei casi normali. Nel percorso normale si arriva sempre a `registrato=True`, anche quando il costo è 0, non numerico, infinito o negativo (diventa 0.0 e si scrive comunque). Nel ramo «conto già illeggibile» il `return` dentro il `with` passa dal `finally` con `fermo_gia=True`, quindi il flag resta spento ed è corretto, perché il forte lo ferma già `_uso_claude_cli`. Se arriva un `KeyboardInterrupt` il flag si accende e l'interruzione prosegue: va bene. Esito: ok.
- `gas.py:1688` — `_tetto_claude_cli_superato` legge il flag con `getattr` (non serve inizializzarlo nel costruttore) e restituisce `(None, tetto)`: il forte si ferma fino al riavvio, cioè fail-closed. La chiamata sta dentro `if name == "claude-cli"` (`gas.py:4668`), quindi gli altri provider non cambiano. Il messaggio di `_errore_tetto_forte` ora parla anche dell'aggiornamento non riuscito e del riavvio. Esito: ok, R-502-2 chiusa.
- Windows (`fcntl` None, contesto `gas.py:12`): si fa solo l'`open(..., "a")` del lockfile, senza attesa e senza lucchetto; lettura, somma e scrittura avvengono come prima. Niente si rompe. Esito: ok.
- §9 (eccezioni intercettate e loggate): `_registra_uso_claude_cli` intercetta tutto e logga come warning («scrittura fallita … — forte fermo»). Il flag non solleva mai e i due punti di chiamata (`gas.py:4686`, `gas.py:4718`) non cambiano. Nel ramo `except` della create, il `raise` nudo arriva dopo la registrazione: il fallback degli altri provider e il retry di Gemini restano come prima. Esito: ok.
- `tests/test_unit_kernel.py:4408` — il lockfile è nella lista T68s (scrittura negata al modello). `tests/test_unit_kernel.py:10952` — in T99o un altro fd tiene il lucchetto: misurati 0,20 s di attesa, conto fermo a 0.25, tetto `(None, 4.60)`; poi il flag e `LOCK_STORIA_SEC` vengono ripristinati. Esito: ok.
- `brains/claude_cli.py:308` — il ramo `except Exception` generico ora ha un test: l'eccezione diventa «claude-cli: risposta non valida» col costo. Esito: ok, R-502-3 chiusa.
- `.claude/commands/fine-task.md:131` — il segnaposto «output GREZZO» e il commento di 4bis ora citano la regola «n/d». Esito: ok, chiude anche R-501-1 (cosmetica).
- `.gitignore`: aggiunto `.gas_claude_cli_uso.json.lock`. Esito: ok.

**Prove rieseguite da me**
- claude_cli: 21 passed.
- kernel: 1038 PASS, 0 FAIL (T99o e T68s PASS).

**Nota di design (non è una riserva)**: in un processo che resta acceso a lungo (il bot) basta un solo errore passeggero di disco o di lucchetto per fermare il forte fino al riavvio, senza che si rimetta in moto da solo. È voluto (meglio fermo che consumare senza conto) e il messaggio dice di riavviare. Il doctor non vede questo flag, perché vive solo dentro il processo.

**Cosa NON ho verificato**
- Il comportamento vero su Windows: niente ambiente Windows qui, l'ho valutato leggendo il codice.
- Il flock su filesystem di rete (NFS, dove può dare `ENOLCK`): non riproducibile qui. Leggendo il codice, finirebbe in `except` e fermerebbe il forte (fail-closed).
- Non ho rieseguito il pytest completo (dichiarato 2142 passed, 1 skipped) né fatto una prova con un mutante sul flag.

**Memoria**
- Riga #503 aggiunta in `/home/user/Gas/.claude/agents/memoria_revisore.md`, nessuna lezione nuova.
- Committata da sola con `scripts/commit_memoria_revisore.sh` (commit a779e43). Il resto dello stage non è stato toccato.

## §5 DELTA TEST DEL MOTORE

- `python tests/test_unit_kernel.py`: 1035 → 1038 PASS (T99m, T99n, T99o nuovi; lockfile in T68s), 0 FAIL.
  `=== RIEPILOGO: 1038 PASS, 0 FAIL ===`
- `pytest tests/test_unit_claude_cli.py`: 19 → 21 passed.
- `pytest tests/` completo: `2142 passed, 1 skipped in 194.63s (0:03:14)`.

## §6 STATO CI

`gh run list -L 3` alle 21:27 UTC:

```
queued		feat(r2): fetta 3 del cervello forte — costo su ogni errore, conto so…	CI	feat/merge-automatico-z1xjx2	push	40134300964	1s	2026-10-24T21:27:35Z
completed	success	Merge pull request #260 from Gasss23/feat/merge-automatico-z1xjx2	CI	feat/merge-automatico-z1xjx2	push	40130653007	3m6s	2026-10-24T20:38:01Z
completed	success	Merge pull request #260 from Gasss23/feat/merge-automatico-z1xjx2	CI	main	push	40130634370	2m39s	2026-10-24T20:37:46Z
```

Mappatura: c1409f7, a779e43 e 9161425 pushati insieme: una run sulla testa 9161425; i commit di memoria non hanno run propria. Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-496-3** (BASSA): login vero col portachiavi del Mac (e `CLAUDE_CODE_OAUTH_TOKEN` sulla VPS) da provare con l'ambiente ridotto.
- Prezzi di riferimento per famiglia da ritarare con l'uso vero (dichiarato nel codice).
- Comportamento dichiarato (nota di design #503): un errore di registrazione del consumo ferma il forte fino al riavvio; il doctor non vede questo fermo.
- **R-498-2** (BASSA, preesistente): alcuni log scrivibili dal modello a finestra pulita.
