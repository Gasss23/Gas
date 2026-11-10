# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — terminale opzione A: azioni fisse di manutenzione per Gas (chat M2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #363 (https://github.com/Gasss23/Gas/pull/363). È un CAMBIO DI SICUREZZA: resta aperta fino al sì esplicito dell'operatore, anche con verdetto pulito del bot. Consigliato il secondo passaggio nella chat claude.ai col link della PR.
2. R-738-2: «mai a voce» deve valere anche per i vocali di Telegram (che oggi arrivano a Gas come turni a testo)? Decide l'operatore.

NB: `gh` nel cloud non è autenticato; numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — terminale opzione A (strumento `manutenzione`, cancello, divieti in run_turn, test, CI)**: `FATTA` (e93bd77).
- **Merge di origin/main (#359 di Mani) nel ramo**: `FATTA` (32619b5), review #743-M2.
- **Riserve del terminale A registrate in stato_progetto (R-743-1)**: `FATTA` (bcca777).
- **Verifica esterna #363 V-1 di gravità media (conflitto con main dopo il merge della #360)**: `FATTA` — merge di origin/main 447195f (d3c490c), conflitti solo nei report e nella memoria, review #745-M2 APPROVATO.
- **Merge di origin/main 2dd0e8c (#362) nel ramo**: `FATTA` (ece76a8) — conflitti solo nei report e nella memoria; da main arrivano solo `reports/prova_r1_notte.md` e una riga di memoria (fuori dal perimetro di review).
- **Merge di origin/main 3f08352 (#361 di Mani) nel ramo**: `FATTA` — conflitti solo nei report e nella memoria; review #749-M2 APPROVATO (file di main identici a 3f08352, nessuna interazione col terminale A; manutenzione + voce_ascolto 348 passed).
- **Verifica esterna #363 V-3 BASSA (filtro di `log_voce`)**: `FATTA` (94bd308, review #748-M2).
- **Verifica esterna #363 V-4 BASSA (testo della firma di `aggiorna_gas`)**: `DEFERITA` — registrata in §7.
- **Prova dal vivo di `riavvia_voce` / launchctl sul Mac**: `DEFERITA` — dopo il merge.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  12 +++++++++++-
 .github/workflows/ci.yml           |   7 +++++++
 gas.py                             |  55 +++++++
 modules/gate/gate.py               |  20 ++++
 modules/manutenzione/__init__.py   | 191 ++++++++++++++
 reports/diff_sessione.md           |  18 ++++++++++--------
 reports/handoff.md                 | n/d
 reports/proposta_terminale_A.md    |  31 +++++++
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  25 ++++++++++--------
 tests/test_unit_manutenzione.py    | 313 ++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
62de796 Merge origin/main (#361 di Mani) nel terminale A — review #749-M2 APPROVATO (chat M2)
3bf227f docs(fine-task): terminale A — merge di main (#362), V-3 verifica esterna #363 chiusa (review #748-M2), riserve aggiornate (chat M2)
94bd308 fix(manutenzione): filtro di log_voce sulla riga intera di gas_debug.log (fullmatch), chiude V-3 verifica esterna #363 — review #748-M2 APPROVATO CON RISERVE (chat M2)
ece76a8 Merge origin/main (#362) nel terminale A — conflitti solo nei report e nella memoria (chat M2)
860c751 docs(fine-task): terminale A dopo il merge di main (#360) — verifica esterna #363 V-1 chiusa, V-2/V-3/V-4 registrate (chat M2)
d3c490c Merge origin/main (#360) nel terminale A, chiude V-1 verifica esterna #363 (conflitto) — review #745-M2 APPROVATO (chat M2)
bcca777 docs(fine-task): terminale opzione A — report, handoff e riserve in stato_progetto (R-743-1); PR #363 per il sì dell'operatore (chat M2)
32619b5 Merge origin/main (#359 di Mani) nel terminale A — review #743-M2 APPROVATO CON RISERVE (chat M2)
e93bd77 feat(gas): terminale opzione A — azioni fisse di manutenzione (stato_gas, log_voce; aggiorna_gas e riavvia_voce solo con firma), mai a voce né di notte (decisione dell'operatore via M1)
54a6299 chore(revisore): memoria review #739 — APPROVATO CON RISERVE
28c559e chore(revisore): memoria review #738 — APPROVATO CON RISERVE
1ebb897 chore(revisore): memoria review #736 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #749-M2 (merge di main 3f08352, PR #361 di Mani) — verdetto integrale RIEMESSO

Il primo verdetto citava un solo file di codice del diff di sessione e il gate B lo rifiutava: come da regola il revisore l'ha RIEMESSO con la stessa sostanza e le citazioni del lato terminale A. Sotto, prima il verdetto riemesso, poi l'originale (in un blocco, alla lettera).

VERDETTO: APPROVATO

Review #749-M2 (chat M2), riemessa con la stessa sostanza: aggiunte le citazioni del lato terminale A. Diff staged: il merge di origin/main 3f08352 (PR #361 della chat Mani) in feat/terminale-a-m2, con base comune 2dd0e8c.

**File del terminale A esaminati:** con `git diff --cached HEAD --quiet` su gas.py, modules/, .github/ e il test di manutenzione risultano identici a HEAD, quindi il merge non li tocca.
- `gas.py:5174`: è la guardia `_manutenzione_fuori` in run_turn, che nega lo strumento prima del cancello quando il turno è a voce, effimero, in sottofondo o di notte. Il rischio era che il merge alterasse la guardia. Il file è identico a HEAD e la #361 non tocca gas.py. Esito: ok.
- `gas.py:609`: è `_carica_dotenv`, l'unico punto di gas.py usato dal lato main (ascolto.py lo importa). Il rischio era un'interazione tra i due lati. La funzione non compare nel diff 3f08352..HEAD di gas.py. Esito: ok.
- `modules/manutenzione/__init__.py:177`: rifiuta le azioni da firmare se manca la firma; alla riga 180 c'è la finestra notte anche per le azioni firmate. Il rischio era che la risoluzione dei conflitti indebolisse questi blocchi. Il file è identico a HEAD (già revisionato in #739-M2 e #745-M2). Esito: ok.
- `modules/gate/gate.py:777`: classifica come IRREVERSIBLE le azioni di `_MANUTENZIONE_FIRMA`. Il rischio era una regressione del cancello. Il file è identico a HEAD. Esito: ok.
- `.github/workflows/ci.yml:223`: è il passo della CI che lancia la suite di manutenzione. Il rischio era perdere il passo durante la risoluzione. Il file è identico a HEAD. Esito: ok.
- `tests/test_unit_manutenzione.py:260`: è `test_a_voce_nessuna_richiesta_di_firma`. Passa sulla copia dell'index. Esito: ok.

**File di main e altri controlli:**
- `clients/voice/ascolto.py:179`, `tests/test_unit_voce_ascolto.py` e `scripts/voce/LEGGIMI.md`: blob identici a 3f08352 (`git diff --cached 3f08352` vuoto).
- `git diff --cached --stat origin/main` mostra solo il terminale A più report e memoria (11 file).
- `.claude/agents/memoria_revisore.md`: è l'unione dei due lati. Nessuna riga persa né da main né da HEAD, nessuna riga doppia, nessun marcatore; la #742-M2 compare una volta sola.
- `reports/stato_progetto.md`: rispetto a main cambia solo la riga +1 del terminale A.
- `git ls-files -u` è vuoto e `git diff --cached --check` è pulito.
- Test sulla copia dell'index (`checkout-index`), manutenzione più voce_ascolto: **348 passed**.

**Cosa non ho verificato:**
- Il comportamento dal vivo dell'ascolto sul Mac (microfono, parola di attivazione): non si può riprodurre qui.
- Le suite del kernel e del gate non le ho rilanciate: gas.py e il gate sono identici a HEAD e già revisionati in #745-M2.

**Memoria:** la riga #749-M2 è già in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` e in staging. Nessun commit e nessun'altra modifica ai file.

Verdetto originale #749-M2, alla lettera:

```
VERDETTO: APPROVATO

Review #749-M2 (chat M2). Diff staged: il merge di origin/main 3f08352 (PR #361 della chat Mani) nel ramo feat/terminale-a-m2. La base comune è 2dd0e8c.

**Elementi del diff esaminati:**
- `clients/voice/ascolto.py:179`: importa `_carica_dotenv` da gas. Il rischio era un'interazione con il terminale A, che modifica gas.py. Nel diff 3f08352..HEAD di gas.py non compare `_carica_dotenv` (definita in `gas.py:609`). Il blob del file è identico a quello di 3f08352. Esito: ok.
- `tests/test_unit_voce_ascolto.py:1` e `scripts/voce/LEGGIMI.md:1`: il rischio era che la risoluzione dei conflitti avesse alterato i file di main. `git diff --cached 3f08352` su questi due file e su ascolto.py è vuoto. Esito: ok.
- `.claude/agents/memoria_revisore.md:1416`: è l'unione dei due lati. Il rischio era perdere righe o lasciarne di doppie. Nessuna riga persa né rispetto a main né rispetto a HEAD (confronto `comm` sulle righe ordinate), nessuna riga doppia, nessun marcatore di conflitto. La #742-M2 compare una volta sola: è stata spostata, non persa. Esito: ok.
- `reports/stato_progetto.md:617`: rispetto a main cambia solo la riga +1 «Terminale opzione A». Rispetto a HEAD entrano le due righe di Mani (#359 mergiata, #361). Esito: ok.

**Controlli meccanici:**
- `git diff --cached --stat origin/main` mostra 11 file, cioè solo il terminale A più i report e la memoria: gas.py, `modules/gate/gate.py`, `modules/manutenzione/__init__.py`, il test di manutenzione, ci.yml e la proposta, più handoff, ultimo_report, diff_sessione, stato_progetto e memoria.
- Il lato main della base tocca solo ascolto.py, il test di ascolto, LEGGIMI e i report. I due insiemi di codice non si sovrappongono.
- `git ls-files -u` è vuoto e `git diff --cached --check` è pulito.
- Test lanciati sulla copia dell'index (`checkout-index`), manutenzione più voce_ascolto: **348 passed**.

**Cosa non ho verificato:**
- Il comportamento dal vivo dell'ascolto sul Mac (microfono, parola di attivazione): non si può riprodurre in questo ambiente.
- La suite del kernel e quella del gate non le ho rilanciate: il merge non tocca né gas.py né il gate, che sono identici a HEAD, già revisionati in #745-M2.

**Memoria:**
- Ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga «#749-M2 — 2026-11-10 — APPROVATO — … Nessuna lezione nuova» e l'ho messa in staging con `git add`.
- Come mi hai chiesto non ho fatto commit, quindi non ho lanciato nemmeno `commit_memoria_revisore.sh`.
```

### Review #748-M2 (V-3 verifica esterna #363, commit 94bd308) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #748-M2: diff staged su feat/terminale-a-m2 (PR #363). Chiude V-3 BASSA della verifica esterna #363 sul filtro `_RIGA_TEMPI` di `log_voce`.

Letture fatte prima della review: CLAUDE.md §5 (nel diff non c'è slicing della history né simulazione di tool), reports/stato_progetto.md (letto solo a pezzi con grep) e la mia memoria.

**Elementi del diff esaminati**
- `modules/manutenzione/__init__.py:44` — la regex ora richiede la riga intera nel formato «data ora,ms - INFO - tempi voce (NNN): nome=N.NNs …». Rischio esaminato: che il formato non sia quello che il server voce scrive davvero. Ho controllato la catena:
  - `gas.py:69-72`: basicConfig col formato «%(asctime)s - %(levelname)s - %(message)s». Il livello di base è WARNING, ma il file handler non ha un livello suo.
  - `modules/voice/server.py:101-102`: il logger `gas.voce.tempi` ha `setLevel(INFO)`, quindi le sue righe INFO arrivano nel file.
  - `modules/voice/server.py:529`: le righe hanno la forma «tempi voce (%s): k=v:.2fs …».
  - Prova pratica col formatter vero: le righe con le chiavi reali (trascrizione, cervello, voce, voce_tutta, server), i codici 200/413/500, i millisecondi e una sola chiave vengono tutte accettate. Una `\r` finale è tollerata grazie a `rstrip`. Testo in più in coda o in testa viene rifiutato.
  - Esito: ok.
- `modules/manutenzione/__init__.py:115` — si passa da `search` a `fullmatch`. Rischio esaminato: un mutante che torna a `search`. Ho applicato il mutante: il test fallisce (1 failed, 44 passed). Ho poi ripristinato il file, e il worktree è di nuovo identico all'index. Esito: ok, il test morde.
- `tests/test_unit_manutenzione.py:89-95` — le righe di prova ora sono nel formato vero, con due righe ostili (testo arbitrario prima di «tempi voce», e un prefisso arbitrario prima della data). Il controllo `"segreto" not in out` copre tutte e due. Rischio esaminato: un test che passa per il motivo sbagliato. Esito: ok, vedi il mutante sopra.

Suite di manutenzione: 45 passed.

**Riserva R-748-1 (BASSA)** — Se un altro logger registra testo esterno che contiene un a-capo, quel testo può ancora produrre una riga intera valida per il filtro. Una riga così può contenere solo nomi in minuscolo con `_` e numeri scelti da chi la scrive, quindi nessun dato altrui. Va registrata in stato_progetto.md oppure dichiarata come limite.

**Cosa non ho verificato**
- Il comportamento sul Mac o sulla VPS con il server voce avviato davvero e un gas_debug.log reale: in questo ambiente non si riproduce. Ho usato il logger e il formatter veri, in un processo di prova.
- Non ho rieseguito la suite completa del kernel: il diff tocca solo il modulo manutenzione e il suo test.

**Memoria**: ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga `#748-M2 — 2026-11-10 — APPROVATO CON RISERVE — …`, senza lezioni nuove. Il file è aggiunto con `git add` ma non committato, come chiesto: non ho lanciato `commit_memoria_revisore.sh`.

### Review #745-M2 (merge di main 447195f, commit d3c490c) — verdetto integrale

VERDETTO: APPROVATO

Review #745-M2 (chat M2). È il merge staged di origin/main 447195f (PR #360, frasi fisse divise in cache) in feat/terminale-a-m2 (HEAD bcca777, PR #363). Ho letto prima CLAUDE.md, la riga del terminale A in stato_progetto.md e la coda della memoria.

**Elementi del diff esaminati:**
- `modules/voice/server.py:324` — `_FRASI_FISSE_INTERE` diventa una tupla. `_FRASI_FISSE` ora è l'unione delle frasi intere e dei pezzi prodotti da `_dividi_frasi`. Rischio esaminato: che il merge perda parti della #360 o le mescoli col terminale A, e che tocchi la manutenzione. Il blob è identico a MERGE_HEAD (`git diff --cached MERGE_HEAD` vuoto). Nel server la parola «manutenzione» non compare. La #360 cambia solo le righe 324-329. — ok
- `tests/test_unit_voice_server.py:2099` — sono i test della cache sul percorso vero «Gas, forte.» (già revisionati in #737/#740/#741-M2). Rischio esaminato: test persi nel merge. Il blob è identico a 447195f. — ok
- `gas.py:5174` — il DENY `_manutenzione_fuori` in run_turn, prima del cancello. Rischio esaminato: che il merge perda il recinto del terminale A. gas.py, `modules/gate/gate.py`, `modules/manutenzione/__init__.py:176`, `tests/test_unit_manutenzione.py`, ci.yml e la proposta sono identici a HEAD (diff vuoto). — ok
- `reports/stato_progetto.md:617` — conflitto risolto a mano. Contiene la riga R8 di main («✅ #358 MERGIATA 567beb7») e la riga «🔒 Terminale opzione A» del ramo, che contiene anche le riserve R-738-2/3, R-739-1/2 e R-743-1. Non ci sono marcatori di conflitto. — ok
- `.claude/agents/memoria_revisore.md` — è l'unione dei due lati: nessuna riga persa né da HEAD né da MERGE_HEAD. L'ordine è #736–#739-M2, poi #742-M2, poi #743-M2. Non ci sono marcatori. — ok

**Controlli sul merge:**
- `git diff --cached origin/main` contiene 11 file: il terminale A (gas.py, gate.py, manutenzione, test, ci.yml, proposta), i report (handoff, ultimo_report, diff_sessione, stato_progetto) e la memoria. Non c'è nessun file di codice di main.
- handoff, ultimo_report e diff_sessione sono identici a HEAD. ripartenza_m2.md è identico a main.
- `git ls-files -u` è vuoto, `git diff --cached --check` è pulito e nel worktree non ci sono modifiche fuori dall'index.

**Test eseguiti (python3 di sistema):**
- manutenzione + voice_server con -k "not browser": 209 passed, 21 deselected.
- test_unit_gate: 823 passed.
- test_unit_kernel: 1100 PASS e 1 FAIL, solo T31g (noto, dipende dall'ambiente).

**Interazione fra #360 e terminale A:** non ce n'è. La #360 tocca solo l'insieme delle frasi da mettere in cache nella sintesi. Il server voce chiama ancora `run_turn` (modules/voice/server.py:808) con gli stessi argomenti, quindi la guardia della manutenzione per i turni a voce resta quella di gas.py:5174.

**Rischio escluso:** non ho verificato dal vivo la sintesi ElevenLabs né `riavvia_voce` sul Mac, perché in dev non si possono riprodurre. Non ho rilanciato telegram_voce e voce_ascolto: la #360 non tocca bot.py né ascolto.py, e la #743-M2 li aveva già coperti.

**Memoria:** ho aggiunto la riga `#745-M2 — 2026-11-10 — APPROVATO — … Nessuna lezione nuova.` in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho messa in staging con `git add`. Come chiesto, non ho fatto commit e non ho lanciato commit_memoria_revisore.sh, perché il merge è ancora in corso. Il worktree /home/user/Gas-voce non l'ho toccato.

### Review #743-M2 (merge di main, commit 32619b5) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #743-M2. È il merge in staging di origin/main 695b759 (PR #359, voce Telegram) nel ramo feat/terminale-a-m2 (HEAD e93bd77).

**Il merge non perde nulla**
- Ramo e main hanno toccato file diversi a partire dalla base comune 567beb7. L'unico file in comune è la memoria del revisore.
- I 9 file che vengono da main sono identici, blob per blob, a quelli di 695b759: bot.py, ascolto.py, i test kernel, telegram_voce e voce_ascolto, e i 4 report, stato_progetto compreso.
- I 6 file del terminale A sono identici a HEAD: gas.py, gate.py, manutenzione, il suo test, ci.yml e la proposta.
- `git diff --cached origin/main` mostra solo il contenuto del terminale A più la memoria. `git ls-files -u` è vuoto e non restano marcatori di conflitto.

**Elementi esaminati**
- `.claude/agents/memoria_revisore.md:1410` — il conflitto risolto. Rischio: perdere righe di uno dei due lati. Esito ok: dopo la base ci sono tutte le righe di main (da #722 a #735, chat Mani) seguite da quelle del ramo (da #736-M2 a #739-M2), senza buchi.
- `modules/telegram/bot.py:1002` — `_consegna_voce` manda a un thread separato solo `_invia_risposta_vocale`. Rischio: che un'azione firmata del terminale A (aggiorna_gas, riavvia_voce) finisca nel thread della voce, o che la #359 cambi il contesto voce/sottofondo che il kernel usa per la guardia. Esito ok: le firme restano nel ciclo che legge i messaggi, e bot.py non nomina mai la manutenzione. La guardia T78p del test kernel passa.
- `gas.py:5174` — il divieto della manutenzione a voce e di notte in `run_turn`, prima del cancello. È solo contesto: il merge non lo cambia. Esito ok.
- `modules/manutenzione/__init__.py:167` — `esegui`, anche questo solo contesto: blob identico a HEAD. Esito ok.

**Test sull'albero del merge**
- pytest manutenzione + telegram_voce: 116 passed.
- tests/test_unit_kernel.py: fallisce solo T31g (già noto, GAS_VECTORS); T78p passa.

**Riserva**
- R-743-1 BASSA (di processo, non causata dal merge): le riserve R-738-2, R-738-3, R-739-1 e R-739-2 del terminale A non sono in reports/stato_progetto.md, né sul ramo né su main. Vanno aggiunte a fine task, come chiede la regola sulle riserve tracciate.

**Cosa non ho verificato**
- Non ho rifatto la review del contenuto del terminale A (già coperta da #736, #738 e #739-M2) né della #359 (#722–#735).
- Non ho provato dal vivo le interazioni a runtime (Telegram vero, launchctl): non sono riproducibili qui. La verifica è statica più i test.
- In reports/handoff.md ci sono spazi a fine riga che arrivano da main. Sono innocui.

**Memoria**
- Ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga #743-M2 e l'ho messa in staging con `git add`.
- Non ho eseguito `scripts/commit_memoria_revisore.sh`: hai chiesto di non committare e il merge è ancora aperto. In più il primo tentativo è stato bloccato dal gate (il marcatore `.review_ok` non corrisponde al diff in staging) prima di eseguire qualsiasi cosa, quindi la riga l'ho poi aggiunta in un comando separato.
- Ora il diff in staging comprende anche la riga di memoria: prima di committare rigenera il marcatore con `bash scripts/segna_review_ok.sh`.

### Review #736-M2, #738-M2, #739-M2 (commit e93bd77)

I verdetti integrali sono stati emessi prima di un `/clear` di questa chat e non sono più disponibili nel contesto: si riportano alla lettera le righe di memoria del revisore (`.claude/agents/memoria_revisore.md`), non il testo integrale. Il loro contenuto è coperto anche dalla verifica esterna e dal bot su questa PR.

```
#736-M2 — 2026-11-09 — BOCCIATO — terminale opzione A (modules/manutenzione, cancello, kernel), diff STAGED: la guardia del turno sta solo in execute_tool_call (gas.py:4827) ma run_turn manda al cancello prima: aggiorna_gas/riavvia_voce (IRREVERSIBLE, modules/gate/gate.py:777) chiamati da un turno a voce/sottofondo/notte vengono parcheggiati e la richiesta di firma parte lo stesso (riprodotto sulla copia dell'index: test voce → «impossibile notificare la richiesta di firma», cioè accodata). Il fix NON staged (DENY in run_turn prima del cancello) chiude il buco: va messo in staging e ri-revisionato. Riserve: spia del test su enqueue_approval vuota (il parcheggio usa accoda_approvazione), GIT_TERMINAL_PROMPT=0 per git pull, filtro log_voce più stretto.
#738-M2 — 2026-11-09 — APPROVATO CON RISERVE — terminale opzione A, seguito di #736-M2 (diff STAGED, 6 file): _manutenzione_fuori porta a DENY in run_turn PRIMA del cancello (gas.py:5173-5177), test spia accoda_approvazione; mutante senza il DENY → test_a_voce_nessuna_richiesta_di_firma fallisce (provato su copia dell'index), 29 passed. Riserve: R-738-1 MEDIA la proposta (reports/proposta_terminale_A.md:18) promette «azioni con firma negate nelle ore della notte», il codice esclude solo il kernel del giro notturno (carica_storia=False), nessuna finestra oraria; tabella :13 e domanda :24 superate dalla decisione su com.gas.ascolto. R-738-2 BASSA i vocali Telegram (modules/telegram/bot.py:984) sono turni a testo per il kernel (niente voce=True): manutenzione offerta anche lì, da far decidere all'operatore. R-738-3 BASSA l'esecuzione firmata gira nel processo del bot: aggiorna_gas può tenerlo occupato fino a ~19 min (pip 900 s + git), e il bot stesso resta sul codice vecchio senza riavvio.
#739-M2 — 2026-11-09 — APPROVATO CON RISERVE — terminale opzione A, seguito di #738-M2 (diff STAGED, 6 file): R-738-1 chiusa, finestra notte in run_turn prima del cancello (gas.py:5176-5181) e nel modulo anche firmate (modules/manutenzione/__init__.py:176); mutanti provati su copia dell'index: senza controllo del modulo 2 test falliscono, senza quello del kernel 1; 45 passed, gate 823. Riserve: R-739-1 BASSA ora locale della macchina (su VPS in UTC la finestra slitta), R-739-2 BASSA testo «Could not find service» di launchctl non provato dal vivo, R-738-2 (vocali Telegram) resta decisione dell'operatore.
```

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_manutenzione.py` nuovo (CI: passo «manutenzione suite»).
- `python tests/test_unit_kernel.py` sull'albero del merge:

```
=== RIEPILOGO: 1099 PASS, 1 FAIL ===
  FAIL: T31g gate env GAS_VECTORS=1 costruisce il vector store (lazy, no download) — vectors=VectorStore
```

  T31g è fuori scope: dipende dall'ambiente (GAS_VECTORS), fallisce uguale su main.
- `python -m pytest -q tests/test_unit_manutenzione.py tests/test_unit_gate.py tests/test_unit_notte.py`: 1064 passed.
- Dopo 94bd308: `python -m pytest -q tests/test_unit_manutenzione.py`: 45 passed (test di `log_voce` con righe nel formato vero e due righe ostili).

## §6 STATO CI

CI NON VERIFICATA con `gh` (non autenticato nel cloud); esiti letti con lo strumento GitHub MCP:
- 860c751 (head precedente): unit-suite success, handoff-check success, verifica-bot neutral (la PR tocca ci.yml, macchina del bot).
- ece76a8 e 94bd308: nessuna run propria (pushati insieme al commit di fine task 3bf227f).
- 3bf227f: bot APPROVATO CON RISERVE senza finding gravi (neutral); unit-suite non letta a fine run prima del merge successivo.
- Merge di main 3f08352: nessuna run su questo SHA (pushato insieme al commit di fine task).
- Commit di fine task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-738-2 BASSA — vocali di Telegram = turni a testo: lo strumento è offerto anche lì (decisione dell'operatore, §0 punto 2).
- R-738-3 BASSA — l'esecuzione firmata gira nel processo del bot: `aggiorna_gas` può occuparlo fino a ~19 min; il bot resta sul codice vecchio fino al riavvio.
- R-739-1 BASSA — finestra notte in ora locale della macchina: su un VPS in UTC slitta.
- R-739-2 BASSA — il testo «Could not find service» di launchctl non è stato provato dal vivo.
- R-743-1 BASSA — riserve non registrate in stato_progetto: CHIUSA (bcca777, voce «Terminale opzione A»).
- Verifica esterna #363 (commento sulla PR, su bcca777) V-1 di gravità media (PR non mergeabile, conflitto con main): CHIUSA (d3c490c, review #745-M2).
- Verifica esterna #363 V-2 BASSA (CI non conclusa al momento della verifica): da rileggere sulla head nuova.
- Verifica esterna #363 V-3 BASSA (filtro di `log_voce`): CHIUSA (94bd308, review #748-M2).
- R-748-1 BASSA — un altro logger che scrive testo esterno con un a-capo può ancora produrre una riga valida per il filtro (solo nomi minuscoli e numeri: nessun dato altrui).
- Bot su 860c751 V-2 BASSA — le richieste a TESTO del server voce arrivano a run_turn senza voce=True: lì `manutenzione` è offerta (letture senza firma, azioni alla firma). Decide l'operatore insieme a R-738-2.
- Verifica esterna #363 V-4 BASSA — `aggiorna_gas` lancia `pip install -r` su codice appena scaricato da main; l'unica barriera è la firma, e la richiesta di firma dice solo «Esegui manutenzione». Fix proposto: testo della firma più esplicito.
