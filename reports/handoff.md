# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-06 — Voce rapida, fetta 2: a voce finestra corta, niente recap vecchio, effort basso del forte, «rispondi solo all'ultima» (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 2 (numero e URL nella risposta JSON di `create_pull_request`; `gh` nel cloud non è autenticato). Fetta ordinata dall'operatore via M1 col via su gas.py; merge secondo CLAUDE.md §10 (con riserve: sì dell'operatore via M1).
2. Prova sul Mac: tempi del cervello a voce prima/dopo (log `gas.voce.tempi`, prima 3,9–16,9 s) e controllo che `claude --effort` esista nella versione installata (`claude --help | grep effort`); se manca, Gas riprova senza e la voce funziona lo stesso, ma senza il guadagno.

---

## §1 SCOPE & ESITO FETTE

- **Finestra più corta a voce** (C2): `FATTA` — `run_turn(voce=True)`: `_get_window(6)` (GAS_VOCE_FINESTRA), sempre via `_get_window`.
- **Niente riepilogo vecchio a voce** (A2): `FATTA` — `recap_pin` spento nei turni parlati.
- **Effort più basso** (A3): `FATTA` — `claude -p --effort low` (documentato in `claude --help` 2.1.319; GAS_VOCE_EFFORT, vuoto = nessuno), con ripiego senza l'opzione se la CLI la rifiuta.
- **C1 «rispondi solo all'ultima domanda»**: `FATTA` — `_CONTESTO_VOCE` in modules/voice/server.py.
- **Tempi prima/dopo**: `NON FATTA — serve il Mac` (in dev non c'è il forte vero).
- **Fetta 3 (documento sul sottofondo)**: `DEFERITA — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 brains/claude_cli.py              | 32 ++++++++++++++++++++++++++++----
 gas.py                            | 29 ++++++++++++++++++++++++-----
 modules/voice/server.py           |  7 ++++++-
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_claude_cli.py     | 56 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_kernel.py         | 80 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voice_contesto.py |  2 +-
 tests/test_unit_voice_stt.py      |  4 ++--
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main c131452 (merge della #342). Il commit di codice è stato fatto su un branch locale e portato qui col cherry-pick (stesso diff revisionato).

## §3 GIT LOG --ONELINE (sessione)

```
1be18db feat(kernel+voce): voce rapida fetta 2 — a voce finestra di 6, niente recap vecchio, --effort low del forte con ripiego, «rispondi solo all'ultima» (C1) (ordine dell'operatore via M1) (chat M2)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. La riga di memoria #689-M2 (23c13b8) è entrata in main con la #342.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #689-M2 sul commit della fetta 2 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #689-M2. Ho guardato le modifiche in staging (`git diff --cached`, 7 file) su feat/voce-v12-m2, base bf4a93b. Prima ho letto CLAUDE.md (sez. 5 e 8), le sezioni di reports/stato_progetto.md che servivano e la memoria del revisore (lezioni del 6 nov sul seguito, sul forte e sui gratuiti).

**Test rilanciati da me sull'albero in staging** (venv in scratchpad):
- Kernel: 1089 PASS, 0 FAIL. T104a, T104b e i due casi T104c passano.
- pytest su tests/test_unit_claude_cli.py, tests/test_unit_voice_stt.py e tests/test_unit_voice_contesto.py: 158 passed.

**Elementi del diff esaminati**
- gas.py:4773 — calcola `_n_finestra`: da `GAS_VOCE_FINESTRA` con `_env_int` e minimo 2 se `voce`, altrimenti 10. Rischio esaminato: un valore sporco o troppo piccolo produce una finestra malformata. `_env_int` è fail-safe e `_get_window` riparte sempre da un messaggio user; con n=2 la ricerca all'indietro ritrova il messaggio dell'utente del turno. Esito: ok.
- gas.py:4857 — il controllo «c'è un seguito a voce nella finestra → solo il forte» usa `_get_window(_n_finestra)`. Rischio esaminato: dato che a voce la finestra è 6, un seguito in posizione 7–10 può mandare il turno parlato ai gratuiti. Ho verificato che anche il payload usa la stessa finestra (gas.py:4936). Il messaggio dell'utente viene aggiunto prima del routing, quindi in ogni iterazione la finestra inviata parte dallo stesso punto o più avanti ed è contenuta in quella del routing. Il seguito escluso dal controllo è escluso anche da ciò che arriva al provider: nessuna contaminazione. Il turno a testo successivo (finestra 10) lo rivede e torna solo-forte, come prima. Esito: ok.
- gas.py:4936 — finestra del loop agentico, sempre via `_get_window`. Ho cercato tagli a mano della storia (Wall of Shame): nessuno, il cap di 10 iterazioni è intatto, nessun output degli strumenti viene simulato. Esito: ok.
- gas.py:4873 — `recap_pin = ""` se voce. Rischio esaminato: si perde contesto utile. È una scelta dell'operatore (ordine M1) e il pin di memoria e quello delle lezioni restano. Esito: ok.
- gas.py:4927 — `effort` passato solo a `ClaudeCliClient` e solo se impostato. Il rung OpenAI non lo riceve, e un valore fuori dalla lista dà warning e nessun effort (T104c). Esito: ok.
- brains/claude_cli.py:343 — il ripiego `--effort`. Rischio esaminato: doppio costo o doppio tempo, e il rischio di nascondere errori veri.
  - Il nuovo tentativo è uno solo e solo se `_effort_rifiutato` (brains/claude_cli.py:272): uscita non zero più «--effort» più una parola di rifiuto dell'argomento. Una CLI che rifiuta un'opzione si ferma prima di chiamare il modello, quindi il costo doppio è trascurabile.
  - Il secondo tentativo sta dentro lo stesso try: timeout, FileNotFound e PermissionError restano gestiti. Il suo esito passa per la stessa classificazione (QUOTA, login, ecc.), quindi un errore vero dopo il nuovo tentativo arriva comunque al chiamante.
  - Un errore diverso non provoca nuovi tentativi (test_effort_altro_errore_non_riprova).
  - Esito: riserva R-689-1-M2.
- modules/voice/server.py:599 — `kw["voce"] = True` per ogni turno audio, anche per il seguito effimero (`effimero` forza comunque il forte; a voce la finestra è 6). C1 è in `_CONTESTO_VOCE` (modules/voice/server.py:206). Esito: ok.
- tests/test_unit_kernel.py:11694 — T104, round-trip §7. Calcolo dell'inizio della finestra: 21 messaggi, cutoff 15, quindi parte da MSG-08-user e MSG-07 resta fuori. Per il turno a testo il cutoff è 11 e la finestra parte da MSG-06. Le asserzioni corrispondono. Esito: ok.

**Riserve**
- R-689-1-M2 BASSA — il flag `_effort_non_supportato` (brains/claude_cli.py:302) vale per tutta la classe e resta acceso finché il processo vive. Si accende anche su un falso positivo, cioè «--effort» e «invalid» in un errore della CLI, per esempio una CLI intermedia che conosce `--effort` ma non accetta xhigh/max. Da lì in poi la voce resta senza effort fino al riavvio del server voce, e lo segnala un solo warning in gas_debug.log. Da dichiarare all'operatore. In alternativa si può limitare la parola «invalid» al caso «argument … is invalid».
- R-689-2-M2 COSMETICA — test_effort_nel_comando_solo_se_chiesto (tests/test_unit_claude_cli.py:494) azzera il flag all'inizio ma non in un `finally`, a differenza degli altri due test.

**Cosa NON ho verificato**
- Il comportamento reale di `claude --effort` sulla CLI installata sul Mac dell'operatore (versione e testo vero dell'errore di commander): qui non si può riprodurre. Il caso di rifiuto l'ho valutato solo sul messaggio simulato nel test.
- Il guadagno di latenza vero (3,9–16,9 s, poi?): serve una prova a voce sul Mac.
- I mutanti dichiarati dall'agente (finestra voce ignorata, recap non spento) non li ho rilanciati; ho rilanciato solo le suite. Un mutante che metta il controllo del seguito a 10 (gas.py:4857) andrebbe nel verso sicuro e nessun test lo uccide, ma non è un rischio.

**Memoria**: riga #689-M2 aggiunta a .claude/agents/memoria_revisore.md e committata da sola con scripts/commit_memoria_revisore.sh (commit 23c13b8). Il diff in staging della fetta è intatto (7 file). Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_kernel.py`: T104a (turno parlato: round-trip §7 con `calcola`, `--effort low`, finestra che parte da MSG-08, niente recap), T104b (turno a testo invariato: finestra 10, recap, niente effort), T104c (effort vuoto o non valido → nessuno). Suite kernel `=== RIEPILOGO: 1089 PASS, 0 FAIL ===` (prima 1085). `tests/test_unit_claude_cli.py` +3 (effort nel comando solo se chiesto; CLI che rifiuta → riprova senza e poi non lo passa più; altro errore → nessun nuovo tentativo): 49 passed. Voce (server, stt, tts, contesto, prova_voci, voce_ascolto) 518 passed. Mutanti: finestra voce ignorata → T104a FAIL; recap non spento → T104a FAIL.

## §6 STATO CI

`gh` non autenticato nel cloud. 1be18db e il commit di fine-task che contiene questo file sono pushati insieme: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-689-1-M2 BASSA: il flag `_effort_non_supportato` vale per tutto il processo; un falso positivo («--effort» e «invalid» in un altro errore) spegne l'effort fino al riavvio del server voce (un warning in gas_debug.log).
- R-689-2-M2 COSMETICA: un test dell'effort azzera il flag senza `finally`.
- Bot #342 (BASSA, registrata): un marcatore d'elenco alfabetico «a) «…»» esenta una citazione; il campo strutturato blocca.
