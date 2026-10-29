# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Voce V1: cervello forte dalla voce (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #304 (https://github.com/Gasss23/Gas/pull/304). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5073160064","url":"https://github.com/Gasss23/Gas/pull/304"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve decide l'operatore (tramite M1).
2. Facoltativo: `GAS_VOCE_FORTE=1` nel `.env` del Mac per mandare tutta la voce al cervello forte (spento di default); server voce avviato con `python -m modules.voice.server` dalla cartella di Gas, lo conferma a schermo.

---

## §1 SCOPE & ESITO FETTE

- **V1.1 — verifica del giro vocale e proposta a M1**: `FATTA` — il forte passava solo con «/forte», che a voce non si detta; M1 ha scelto parola chiave + interruttore.
- **V1.2 — parola chiave parlata «forte …» / «Gas forte …»**: `FATTA` — `cervello_voce()` in `modules/voice/server.py`, solo sul testo trascritto, fail-closed («uso» → 400).
- **V1.3 — `GAS_VOCE_FORTE`**: `FATTA` — tutta la voce al forte; forte fermo → errore dichiarato, mai i gratuiti.
- **V1.4 — test di trascrizione e sintesi nei test automatici**: `FATTA` — già in CI dalla PR #229 (riga R8 corretta); chiusa R-384-1 (test indipendenti dal proxy).
- **V1.5 — bot #304 su 274f131 NON approvata, V-1 MEDIA (il server voce non caricava il `.env`)**: `FATTA` — `run_server` carica il `.env` come la CLI prima di leggere la configurazione, riga a schermo con l'interruttore acceso, avvio `python -m modules.voice.server`; provato con un `.env` vero temporaneo (poi cancellato).
- **V1.6 — verifica esterna #304 (APPROVATO CON RISERVE, [commento](https://github.com/Gasss23/Gas/pull/304#issuecomment-6504683688))**: V-2 BASSA (saluto prima di «Gas») `FATTA`; V-3 COSMETICA (richiesta vuota → «uso») `FATTA`; V-1 BASSA (falsi positivi «forte-forte», «forte: …») `FATTA` come limite dichiarato (commento della regex e roadmap); V-4 COSMETICA (26 vs 25 falliti sul codice vecchio) `SALTATA — numero dipendente dall'ambiente (qui 26 con http_proxy e no_proxy vuoti), il fatto R-384-1 è confermato dalla verifica`.
- **Review #565-M2 APPROVATO CON RISERVE**: R-565-1-M2 BASSA e nota «sì» `FATTA`, rivisto in #566-M2 APPROVATO.
- **V1.7 — bot #304 su 06cd1ed: APPROVATA (APPROVATO CON RISERVE)**: V-1 BASSA (un test lasciava «/» in testa a `sys.path` per il resto di pytest) `FATTA` — i tre test che chiamano `run_server` ripristinano `sys.path` (review #567-M2, commit 1b02e72); V-2 COSMETICA `FATTA` — chiarito: la prova col `.env` vero è MANUALE, non in CI (in CI il test sostituisce `_carica_dotenv` e prova l'ordine: prima il `.env`, poi il token).
- **V1.8 — verifica esterna #304 su 06cd1ed (APPROVATO CON RISERVE, [commento](https://github.com/Gasss23/Gas/pull/304#issuecomment-6505016808))**: V-1/V-2 BASSE (falsi positivi di «forte»; 400 d'uso a voce) e V-3/V-4 COSMETICHE («sì»; 26 vs 25) già dichiarate o accettate, nessun fix richiesto.
- **gas.py / brains/ / doctor**: `SALTATA — fuori dal mandato di M1`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/voice/server.py            |  80 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 reports/diff_sessione.md           |  11 +++++++----
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |   3 ++-
 reports/stato_progetto.md          |   3 ++-
 reports/ultimo_report.md           |  40 +++++++++++++++++++---------------------
 tests/test_unit_voice_server.py    | 166 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 tests/test_unit_voice_stt.py       |  38 +++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
1b02e72 test(voce): sys.path ripristinato nei test che chiamano run_server (V-1 bot #304 su 06cd1ed)
1f6735a chore(revisore): memoria review #567 — APPROVATO
06cd1ed docs(voce-v1): report dopo il bot #304 (V-1 chiusa) e la verifica esterna, review #565/#566-M2
e0f3f01 fix(voce): il server voce carica il .env e si avvia con python -m (V-1 bot #304)
4b086c9 chore(revisore): memoria review #566 — APPROVATO
e6c913a chore(revisore): memoria review #565 — APPROVATO CON RISERVE
274f131 docs(voce-v1): report di fine task, roadmap R8 e stato (PR #304, review #564-M2)
aa7c3b1 feat(voce): cervello forte dalla voce — «forte …» parlato e GAS_VOCE_FORTE (V1, chat M2)
f2e68c7 chore(revisore): memoria review #564 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit aa7c3b1 — review #564-M2, verdetto integrale:

VERDETTO: APPROVATO CON RISERVE

Review #564-M2 sul diff staged di feat/voce-v1-m2 (4 file, +182/-9). Prima della review ho letto CLAUDE.md (sez. 5, 8, 9 e la regola dei modelli in sez. 2), le voci M2 e R-384-1 di reports/stato_progetto.md e la mia memoria.

**Elementi del diff esaminati**
- `modules/voice/server.py:71` — regex `_PAROLA_FORTE`, ancorata all'inizio, con «gas»/«gus» opzionale seguito da `\b`, e «forte» come parola intera (il controllo `(?!\w)` vieta lettere subito dopo). Rischio esaminato: falsi positivi e negativi. Prove fatte su una copia dell'index:
  - Restano turni normali: «fortemente…», «Fortezza», «Gasforte», «Ok Gas, forte…», «Gas, Gas forte», «forte_x», «fortè», «Fort/Forti…» (forme storpiate da Whisper: vanno ai gratuiti, stesso limite di «/frote» già dichiarato).
  - Vanno al forte: « Forte, …» con spazio iniziale, «Gas. Forte. …», «Gas-forte x», «...forte x», «Gas forte» con spazio non separabile (NBSP).
  - Mutante senza `(?!\w)` → 8 test falliti.
  - Esito: ok, salvo la riserva R-564-1-M2.
- `modules/voice/server.py:82` — `cervello_voce`. Ordine: prima `prefisso_forte` (invariato), poi la parola «forte» solo se `parlato`; se manca la richiesta → «uso»; `GAS_VOCE_FORTE` vale solo se il cervello è ancora None. Rischio esaminato: un ramo che porti un lavoro «forte» ai gratuiti. Non ce n'è nessuno: «uso» esce sempre con 400 e nessun turno, «forte» passa sempre `cervello="forte"` al kernel, e l'interruttore non trasforma mai «uso» in un turno. `_voce_tutta_forte` usa gli stessi valori di `_env_flag` in gas.py:573. Esito: ok.
- `modules/voice/server.py:185` — il gestore chiama `cervello_voce(prompt, parlato=is_audio)`: la parola parlata vale solo per l'audio; il testo JSON richiede ancora «/forte», coperto da `test_v1_parola_forte_solo_nel_parlato`. Esito: ok.
- `tests/test_unit_voice_server.py:29` e `tests/test_unit_voice_stt.py:68` — client urllib senza proxy (opener con `ProxyHandler({})`). Rischio esaminato: la chiusura di R-384-1 (chat Voce) è reale? Sì. Con il vecchio test stt, `http_proxy` impostato e `no_proxy` vuoto → 11 test falliti. Con il diff: 104 passed sia senza proxy sia con `http_proxy=http://127.0.0.1:9` e `no_proxy` vuoto. Esito: ok.
- `tests/test_unit_voice_server.py:476` — test con forte fermo: il kernel finto emette un errore, il server risponde 500 con il messaggio dichiarato e c'è una sola chiamata, con `cervello="forte"`. Esito: ok.
- Contesto, non nel diff: `gas.py:4703` — con `cervello == "forte"` il compito è forzato a «forte». È l'invariante R2 esistente; gas.py e brains/ non sono toccati, come deciso da M1.

**Riserve**
- **R-564-1-M2 BASSA**: in italiano «Forte!» a inizio frase è anche un'interiezione («che bello!»).
  - «Forte! Che bello.» → turno al forte con richiesta «Che bello.».
  - «Forte e chiaro, ti sento» → al forte.
  - «Forte.» da solo → 400 con l'istruzione d'uso.

  La direzione è sicura (mai ai gratuiti, rispetta la regola dei modelli), ma consuma il budget del forte e dà una risposta d'uso inattesa. Il limite non è dichiarato né nella docstring né in reports/roadmap.md, che cita solo «Ok Gas, forte…». Da dichiarare, oppure da gestire in seguito.

**Rischi esplicitamente esclusi**
- Trascrizioni reali di Whisper non verificate: nessun audio vero né chiave Groq in dev; ho usato solo stringhe simulate al posto di `transcribe_audio`.
- Il comportamento del kernel con il forte fermo (tetto, CLI assente) non è stato riverificato: è codice di gas.py fuori dal diff, coperto dalle sue review.
- La correttezza della riga della roadmap sulla PR #229 non è stata verificata su GitHub; si appoggia alla review #384 (chat Voce) in memoria.

**Test**: `python -m pytest tests/test_unit_voice_server.py tests/test_unit_voice_stt.py tests/test_unit_voice_tts.py -q` → 104 passed, sia senza proxy sia con un proxy finto nell'ambiente.

**Memoria**: riga contatore #564-M2 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, con la lezione: per una parola chiave parlata, provare anche gli usi comuni della parola come interiezione, non solo i composti. Già committata con lo script di memoria (commit f2e68c7, solo quel file); l'index staged del diff è rimasto invariato (4 file). Nota: il messaggio di commit generato dallo script dice «#564» senza il suffisso -M2.

Commit e0f3f01 — review #565-M2, verdetto integrale:

VERDETTO: APPROVATO CON RISERVE

Review #565-M2, PR #304, branch feat/voce-v1-m2, diff staged (`modules/voice/server.py`, `tests/test_unit_voice_server.py`). Ho fatto le prove su un export dell'index (`git checkout-index`), non sulla cartella di lavoro. Ho letto: CLAUDE.md (§5, §8, §9), reports/stato_progetto.md (le parti sulla voce, con grep) e la coda di memoria_revisore.md (lezioni #562–#564-M2).

**Elementi del diff esaminati**
- `modules/voice/server.py:317`: `_carica_env()` viene chiamata in testa a `run_server`, prima di leggere GAS_VOICE_TOKEN, BIND e PORT, e dopo aver impostato sys.path (spostato da sotto a sopra).
  - Rischio esaminato: ordine sbagliato e effetti collaterali di `import gas` prima del controllo del token.
  - Cosa succede all'import: `import gas` apre gas_debug.log accanto a gas.py e chiama `logging.basicConfig`. Prima succedeva solo con il token presente, ora anche quando manca. È un effetto innocuo: il RotatingFileHandler è già protetto da OSError.
  - test_tv1 con root_dir=/tmp: `gas` è già in sys.modules, e `tests/conftest.py:11` imposta GAS_NO_DOTENV=1, quindi il `.env` reale dell'operatore non entra mai nella suite.
  - Mutanti: chiamata tolta → 1 failed; chiamata spostata dopo il controllo del token → 1 failed.
  - Esito: ok.
- `modules/voice/server.py:306`: `except Exception` con log.warning (solo il nome del tipo di errore, mai valori) e si prosegue con l'ambiente così com'è. Rispetta il fail-safe §9.
  - Mutante `except ImportError` → 1 failed su `tests/test_unit_voice_server.py:536`.
  - Esito: ok.
- `modules/voice/server.py:77`: `_PAROLA_FORTE` accetta un saluto (ehi/ehy/hey/ok/okay/ciao/senti) solo davanti a «gas/gus».
  - Rischio esaminato: un lavoro «forte» che finisce ai modelli gratuiti, e falsi positivi.
  - Sonde:
    - «Ehi, Gas, forte analizza», «Hey Gas! Forte: analizza», «Okay Gas forte x» e la variante con spazi NBSP → forte.
    - «Senti Gas forte» → uso.
    - «Ehi Gas fortemente x», «Ehi forte x», «Ehi Gas, parla forte» → normale.
    - «Ehi ehi Gas forte x» → normale: è il limite dichiarato «saluto non in elenco».
  - Nessun ramo che riconosce «forte» porta ai gratuiti. I mancati riconoscimenti restano limiti dichiarati nel commento e sono coperti da GAS_VOCE_FORTE=1.
  - Mutante senza il gruppo del saluto → 2 failed.
  - Esito: ok.
- `modules/voice/server.py:93`: prompt vuoto o di soli spazi → «uso», anche con GAS_VOCE_FORTE=1 (verificato con parlato True e False). Il gestore filtra già prima il vuoto, sia JSON che trascrizione, quindi i messaggi 400 esistenti non cambiano.
  - Mutante → 2 failed.
  - Esito: ok.
- `modules/voice/server.py:342`: riga d'avvio quando GAS_VOCE_FORTE è acceso.
  - Mutante → 1 failed.
  - Esito: ok.
- `modules/voice/server.py:355`: avvio con `python -m`. Prima del merge non c'era nessun percorso di avvio documentato. `modules/voice/__init__.py` non importa server, quindi il modulo non viene caricato due volte.
  - Esito: ok.
- `tests/test_unit_voice_server.py:525`: GasKernel e `_carica_dotenv` sostituiti con `monkeypatch.setattr`, quindi ripristinati a fine test: nessuna perdita verso altri test. Le variabili d'ambiente scritte dal finto dotenv sono tolte nel `finally`.
  - Riserva: il test fa partire il `run_server` vero, che imposta `VoiceHandler.kernel = object()` e `VoiceHandler.token = "tok-dal-dotenv-123"` sulla classe base (`modules/voice/server.py:337`), e nessuno li ripristina. Oggi è innocuo: tutti gli altri test usano sottoclassi con attributi propri.
  - Esito: riserva.

**Prove eseguite**
- `tests/test_unit_voice_server.py`: 58 passed.
- Suite voce + dotenv (`tests/test_unit_voice_*.py` e `tests/test_unit_dotenv.py`): 129 passed.
- 6 mutanti, tutti uccisi.
- gas.py e brains/ non sono toccati. Cap delle iterazioni, `_get_window` e cronologia non toccati. Nessuno slicing della history e nessuna simulazione di tool.

**Riserve**
- R-565-1-M2 BASSA: `tests/test_unit_voice_server.py:500` lascia impostati VoiceHandler.kernel e VoiceHandler.token dopo il test. Correzione: aggiungere `monkeypatch.setattr(srv.VoiceHandler, "kernel", None)` e `monkeypatch.setattr(srv.VoiceHandler, "token", "")` prima di chiamare `run_server()`.
- Nota COSMETICA: GAS_VOCE_FORTE=«sì» con l'accento non viene riconosciuto (`_voce_tutta_forte` accetta «si»). È un comportamento che c'era già prima e oggi la riga d'avvio non segnala nulla in quel caso. Basta dichiararlo, oppure aggiungere «sì».

**Rischi esclusi (non verificati)**
- Avvio vero sul Mac con launchd o systemd e cartella di lavoro diversa da quella di Gas: non riproducibile qui. Mi fido della prova manuale dichiarata dall'agente (`.env` temporaneo con la stampa «GAS_VOCE_FORTE acceso»).
- Trascrizioni reali di Whisper con saluti diversi da quelli in elenco: senza audio non si possono provare.
- Il totale di 112 della suite, dichiarato dall'agente, non l'ho rifatto per intero: ho rifatto solo il sottoinsieme voce + dotenv (129).

**Memoria**: riga #565-M2 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md, con una lezione nuova (gli attributi di classe del gestore scritti da `run_server` vanno ripristinati con monkeypatch), e committata da sola dallo script in e6c913a.

NB: le citazioni di #565-M2 si riferiscono al diff staged prima della correzione di R-565-1-M2 (due righe in più nel test e la docstring di `_voce_tutta_forte`): alcune righe di `tests/test_unit_voice_server.py` e di `modules/voice/server.py` a HEAD sono spostate di poche righe. Il diff committato (e0f3f01) è quello rivisto in #566-M2, qui sotto.

Commit e0f3f01 — review #566-M2 (diff finale committato), verdetto integrale:

VERDETTO: APPROVATO

Review #566-M2 sul diff staged di feat/voce-v1-m2 (PR #304). Ho letto prima, in quest'ordine, CLAUDE.md, reports/stato_progetto.md (solo le parti che servivano) e .claude/agents/memoria_revisore.md, dove ci sono le righe di #564-M2 e #565-M2.

Elementi del diff esaminati:

- `tests/test_unit_voice_server.py:528` — Cosa fa: `monkeypatch.setattr(srv.VoiceHandler, "kernel", None)` e, alla riga dopo, `(..., "token", "")`, prima di `run_server()`. Rischio esaminato: che la riserva R-565-1-M2 sia chiusa davvero, cioè che gli attributi di CLASSE scritti da `modules/voice/server.py:337` (`VoiceHandler.kernel = kernel`) non restino sporchi dopo il test. `setattr` non fallisce perché i due attributi esistono sulla classe (`modules/voice/server.py:119`, `kernel: Any = None`, e la riga 120, `token: str = ""`). Prova: ho lanciato solo questo test e poi letto la classe. Risultato: `kernel` vale `None` e `token` vale `''`. Con il mutante senza le due righe il test passa lo stesso, ma la classe resta sporca (`kernel=<object ...>`, `token='tok-dal-dotenv-123'`). Quindi le due righe sono proprio quelle che fanno il ripristino. — ok
- `modules/voice/server.py:86` — Cosa fa: `_voce_tutta_forte` accetta anche «sì» con l'accento, dopo `strip().lower()`. Rischio esaminato: maiuscole e spazi, e la coerenza della docstring. Prova diretta: `GAS_VOCE_FORTE='Sì '` dà True. La docstring (riga 84) e la docstring del modulo (riga 33, «1/true/on/yes/si/sì») sono aggiornate. — ok
- `tests/test_unit_voice_server.py:448` — Cosa fa: aggiunge il caso parametrico `("sì", True)` a `test_v1_gas_voce_forte`. Rischio esaminato: che il caso esista e venga eseguito. Esito: incluso nella suite voce, che passa. — ok
- `modules/voice/server.py:318` — Cosa fa: chiama `_carica_env()` prima di leggere GAS_VOICE_TOKEN (riga 320). L'avevo già approvato in #565-M2 e l'ho ricontrollato solo per vedere che non fosse cambiato: ordine invariato, e l'eccezione è intercettata e loggata alla riga 307 (fail-safe §9). — ok
- Contesto (file fuori dal diff): nessuno slicing della history e nessuna simulazione di output dei tool nel diff. Cap delle iterazioni e `_get_window` non toccati.

Suite voce (`-k "voice or voce"`): 116 passed, 2375 deselected. Il chiamante dice 113: la differenza dipende da un filtro più largo, non è un segnale di rottura.

Rischio escluso: non ho potuto confrontare byte per byte con il diff approvato in #565-M2, perché quel diff era solo nell'index e nessuno lo ha salvato (HEAD è ancora aa7c3b1 più i commit di doc e memoria). Ho controllato che il resto del diff (saluto davanti a «gas/gus», prompt vuoto → «uso», `_carica_env`, `__main__`, messaggio a schermo di GAS_VOCE_FORTE) corrisponda alla descrizione di #565-M2 nella memoria. Che non sia cambiato altro, quindi, è verificato rispetto a quella descrizione, non al byte. Non ho verificato nemmeno un «sì» scritto in forma Unicode decomposta (NFD, accento come carattere separato): sarebbe ancora letto come spento, ma da tastiera è improbabile.

Note (nessuna bloccante):
- COSMETICA: adesso `GAS_VOCE_FORTE` accetta «sì» mentre `_env_flag` in gas.py, per quanto dice la docstring, no. È un'asimmetria voluta e dichiarata nella docstring. Allineare gas.py è una fetta a parte, se serve.

Memoria: aggiunta la riga #566-M2 in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola dallo script (commit 4b086c9). Nessuna lezione nuova. L'index del diff sotto review è intatto (2 file staged). Per committare il diff devi ancora eseguire `bash scripts/segna_review_ok.sh` (marcatore della review).


Commit 1b02e72 — review #567-M2, verdetto integrale:

VERDETTO: APPROVATO

Review #567-M2 su feat/voce-v1-m2 (PR #304). Diff staged dopo `git add tests/test_unit_voice_server.py`: 1 file, 3 righe aggiunte, solo test. Prima della review ho letto CLAUDE.md (sez. 5), lo stato del progetto (in modo mirato) e la memoria del revisore.

Elementi del diff esaminati:
- `tests/test_unit_voice_server.py:86` — `monkeypatch.setattr(sys, "path", list(sys.path))` prima di `run_server(root_dir="/tmp")` in test_tv1_no_token_refuses_start. Rischio esaminato: `run_server` modifica `sys.path` prima di controllare il token (vedi contesto sotto), quindi nel ramo che restituisce 1 restava `/` in cima a `sys.path` per il resto del processo pytest. Esito: ok. L'ho provato in-process con pytest.main sui 3 test: col file di HEAD, dopo i test `sys.path[0] == "/"`; col file staged `/` non c'è più (`sys.path[0]` è la radice del repo, che aggiunge pytest stesso).
- `tests/test_unit_voice_server.py:528` — stessa riga in test_v1_run_server_carica_il_dotenv. È messa prima di `run_server()` e accanto ai monkeypatch di R-565-1-M2 su VoiceHandler.kernel/token. Rischio esaminato: ordine dei monkeypatch e copertura del ramo che restituisce 0. Esito: ok. Si annulla a fine test, prima delle altre fixture.
- `tests/test_unit_voice_server.py:550` — stessa riga in test_v1_run_server_dotenv_rotto_non_crasha, prima di `run_server(root_dir="/tmp") == 1`. Esito: ok.
- Contesto, file non toccato: `modules/voice/server.py:317` — `_sys.path.insert(0, ...)` viene prima della lettura di GAS_VOICE_TOKEN (`modules/voice/server.py:320`). Conferma che la causa indicata dal bot è reale.
- `sys` è già importato in cima al file del test (riga 13).

Prove eseguite:
- `pytest tests/test_unit_voice_server.py`: 59 passed.
- Controllo in-process di `sys.path`: con HEAD sporco, con il diff staged pulito.
- Il working tree del file di test, dopo lo scambio temporaneo, coincide di nuovo con l'index (verificato con `git diff --stat`).

Antipattern: nessuno. Non c'è slicing della history, non c'è simulazione di tool e i guardrail non sono toccati.

Rischio escluso: non ho rilanciato tutta la suite voce da 113 test (ho eseguito solo questo file, 59 passed). Non ho verificato nemmeno l'isolamento di `sys.modules` o di altro stato globale che `run_server` potrebbe toccare oltre a `sys.path`, perché non fa parte del finding V-1.

Memoria del revisore: aggiunta la riga contatore #567-M2 con una lezione (isolare lo stato globale del processo anche nei rami d'errore precoci). Committata con lo script: commit 1f6735a, «chore(revisore): memoria review #567 — APPROVATO». L'index resta col solo diff del test staged. Nel working tree c'è anche una modifica non staged a `reports/ultimo_report.md`, che non ho toccato.

File: /home/user/Gas/tests/test_unit_voice_server.py, /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

gas.py non toccato. Voice suite (pytest, servizi finti): 73 → 113 test (+40, tutti V1), `113 passed in 22.79s` sulla cartella finale; con `http_proxy=http://127.0.0.1:9` e `no_proxy` vuoto 112/112 prima dell'ultimo caso «sì». Prima del diff, con quel proxy, qui: `26 failed, 47 passed` (R-384-1; la verifica esterna ne misura 25). Nessun FAIL.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- f2e68c7: nessuna run su questo SHA (pushato insieme ad aa7c3b1).
- aa7c3b1: pushato prima dell'apertura della PR #304; `handoff-check` failure (handoff non ancora aggiornato, atteso), nessuna run della PR.
- 274f131: run CI 40927897667 (`unit-suite` e `handoff-check` success); check `verifica-bot` failure — bot NON approvata (V-1 MEDIA, chiusa in e0f3f01).
- e6c913a, 4b086c9, e0f3f01: nessuna run su questi SHA (pushati insieme a 06cd1ed).
- 06cd1ed (fine-task): run CI 40930420811 (`unit-suite` e `handoff-check` success); check `verifica-bot` success — bot APPROVATA, verdetto APPROVATO CON RISERVE (V-1 BASSA chiusa in 1b02e72, V-2 COSMETICA chiarita).
- 1f6735a, 1b02e72 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (pushati insieme; la run testa solo la testa).

## §7 RISERVE APERTE

- **R-564-1-M2** BASSA — «Forte!» esclamazione a inizio frase va al forte (direzione sicura, consuma budget): dichiarata in `reports/roadmap.md` (R8), nel commento della regex e in stato_progetto.
- **V-1 ve #304** BASSA — altri falsi positivi («forte-forte», «forte: …», «Forte e chiaro»): dichiarati come sopra.
- **V-4 ve #304** COSMETICA — 26 vs 25 test falliti prima del fix: dipende dall'ambiente.
- **Nota #566-M2** COSMETICA — `GAS_VOCE_FORTE` accetta «sì», `_env_flag` di gas.py no (asimmetria dichiarata).
- **R-384-2 (chat Voce)** COSMETICA — commento in `ci.yml`: fuori da questa fetta.
- **V-2 ve #304 (06cd1ed)** BASSA — «Gas, forte» senza richiesta dà 400 d'uso a chi parla: fail-closed accettato.
- Prova dal vero col microfono sul Mac non fatta.
