# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-09 notte — chat Mani: voce via Telegram, fetta 3 (turno parlato, niente formattazione a voce, tempi della voce più corti)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 3 (numero e URL dalla risposta dello strumento GitHub `create_pull_request`). Vale la regola notturna dell'operatore (9/11, via M1): con solo BASSE/COSMETICHE e niente sicurezza l'agente mergia da solo con CI e bot verdi. La review #721 la classifica fuori dalla sicurezza.
2. (Domani, sicurezza) Consegna della voce in un thread: va allargata la guardia T78p delle firme. Decide l'operatore.

---

## §1 SCOPE & ESITO FETTE

- **PR #355 (fetta 2)**: `FATTA` — mergiata (b827447).
- **Fetta 3, turno parlato e pulizia della voce (V-1 bot #355)**: `FATTA`.
- **Fetta 3, tempi della voce più corti (V-1 ve #355, R-717-4 in parte)**: `FATTA`.
- **Voce consegnata in un thread**: `DEFERITA — tocca la guardia T78p delle firme (review #720 BOCCIATO); decide l'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/telegram/bot.py            |  46 ++++++++++++++++++++++++++++++++++++++--------
 reports/diff_sessione.md           |  11 +++++------
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  35 +++++++++++------------------------
 tests/test_unit_telegram_voce.py   |  71 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main b827447 (dopo il merge della PR #355).

## §3 GIT LOG --ONELINE (sessione)

```
792b365 feat(telegram): voce via Telegram, fetta 3 — istruzione del parlato, niente formattazione a voce, tempi della voce più corti (riserve #355) — review #720/#721
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push. Il codice è stato scritto e revisionato nel worktree locale /tmp/claude-0/wt48 sulla stessa base, poi portato qui in fast-forward.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #720 (prima versione, con il thread), verdetto integrale:

## VERDETTO: BOCCIATO

Review #720 (chat Mani). Diff staged in /tmp/claude-0/wt48 (branch mani/telegram3, base b827447). Ho letto CLAUDE.md (sez. 5), le parti di reports/stato_progetto.md che riguardano Telegram e la voce, e la memoria del revisore (il numero più alto era #719, nessun -M2 superiore).

**Motivo del blocco**
La suite principale del motore va in rosso. Ho lanciato `python tests/test_unit_kernel.py` su una copia dell'index (non è pytest: è quello che CI esegue in `unit-suite`).
- Copia dell'index: 1098 PASS, 2 FAIL.
- Base b827447: 1099 PASS, 1 FAIL.
- T31g fallisce anche sulla base: dipende dall'ambiente.
- **T78p è una regressione nuova**: `[] ['_invia_a_tutti', '_consegna_voce']`. La guardia statica in tests/test_unit_kernel.py:8389 (V-2 della verifica esterna #241, R-450-1/R-451-1) protegge la regola della firma con i bottoni, «un click alla volta». Vuole che `ThreadPoolExecutor` compaia nel bot SOLO dentro `_invia_a_tutti`. Il nuovo pool in modules/telegram/bot.py:995 la viola, quindi `unit-suite` in CI sarebbe rossa e la PR immergeabile.
- Nel merito il codice non viola la regola: il thread esegue solo `_invia_risposta_vocale` (sintesi, sendVoice, sendMessage) e mai `_handle_update`, `gestisci_callback` o `_riprova_orfana`.
- Come correggere: allargare la guardia T78p in modo mirato (ammettere `_consegna_voce`, con un commento che spieghi perché) e, magari, controllare che `_lavoro` non chiami i tre gestori.
- **Sicurezza**: quel cambio tocca una guardia della firma. La PR quindi NON rientra nella regola notturna «niente sicurezza». A mio giudizio serve il sì dell'operatore, oppure una ri-review che la classifichi in modo esplicito.

**Elementi esaminati**
- modules/telegram/bot.py:929 — `run_turn(text, **kw)`; `kw` è vuoto per i messaggi di testo (`_risposta_del_turno` non passa extra) — rischio: i testi normali cambiano — ok: la chiamata equivale a `run_turn(text)`, e cervello=forte viene aggiunto solo se richiesto (:928).
- modules/telegram/bot.py:969 — legge `_voce_accesa()` una volta; l'istruzione si importa in un try (:976) — rischio: istruzione con la voce spenta, crash se l'import fallisce — ok: test della voce spenta e test dell'import rotto, log solo col tipo dell'eccezione (§9).
- modules/telegram/bot.py:983 — `_consegna_voce` parte dopo l'invio del testo — rischio: la voce arriva prima del testo — ok: il testo è inviato prima in modo sincrono.
- modules/telegram/bot.py:992 — pool lazy `max_workers=1`; `submit` è in un try (:1003) — rischi:
  - thread safety — ok: `_tg_post`, `_send_text` e `_tg_post_file` fanno una richiesta urllib a sé per chiamata, senza stato condiviso; la creazione lazy del pool avviene solo dal thread del polling;
  - ordine e una consegna alla volta — ok;
  - **blocco**: rompe T78p (vedi sopra).
- modules/telegram/bot.py:995 — shutdown — riserva BASSA: i worker di `ThreadPoolExecutor` non sono daemon e Python li aspetta all'uscita (atexit). Dopo Ctrl-C `run_bot` torna 0, ma il processo attende i vocali in coda: fino a 30 all'ora (`GAS_TELEGRAM_VOCALI_ORA`) per circa 60 s ciascuno; un secondo Ctrl-C lo chiude. Con SIGTERM e il gestore di default il processo esce subito, senza attese. Non è un crash.
- modules/telegram/bot.py:1014 — `testo_da_dire` — rischio privacy (dati nuovi verso ElevenLabs) — ok: la fonte è sempre `finale`; il testo viene solo ridotto (URL diventano «link», tolti i segni di formattazione), poi passa a `parte_parlata`. Le regex con `[ \t]` lasciano la riga vuota, quindi il dettaglio resta solo nel testo (verificato da tests/test_unit_telegram_voce.py:457). La chiamata sta dentro il try di modules/telegram/bot.py:1062, quindi anche un ImportError è coperto (§9).
- modules/telegram/bot.py:1011 — `_URL` con `\S+` — COSMETICA: si mangia anche la punteggiatura finale («…su https://x.it/a.» diventa «…su link», senza il punto). Anche `__` toglie gli underscore da nomi come `__init__`. Per l'ascolto è innocuo.
- tests/test_unit_telegram_voce.py:85 — il fixture rende la consegna sincrona — rischio: il thread vero resta senza test — ok: tests/test_unit_telegram_voce.py:478 prova il pool vero (torna subito, rispetta l'ordine, massimo uno alla volta).
- tests/test_unit_telegram_voce.py:478 — possibile test instabile — ok: è deterministico (Event con timeout di 5 s; si romperebbe solo se `partita.wait(5)` scadesse sotto un carico estremo). Non ho riprodotto il «1 failed»: file intero 30/30 verde, test thread/coda 40/40 verdi. Nessun test senza fixture usa il pool vero, quindi niente job che restano vivi tra un test e l'altro.
- tests/test_unit_telegram_voce.py:525 — COSMETICA: `git diff --cached --check` segnala «new blank line at EOF».

**Altri controlli**
- pytest su telegram_voce, voice_server, voce_ascolto e notte: 682 passed.
- I test li ho fatti su `git checkout-index` copiato nello scratchpad, senza stash.
- Wall of Shame: nessuno slicing della history e nessuna simulazione degli strumenti. Il tetto di 10 iterazioni e `_get_window` non sono toccati.
- `istruzione_turno` contiene solo testo fisso più data e ora; va allo stesso cervello di prima: nessun dato nuovo ai modelli gratuiti.

**Rischi esclusi (non verificati)**
- sendVoice e ElevenLabs dal vivo, e il vero tempo di attesa allo spegnimento con systemd: non riproducibili qui. Resta aperta R-717-3 (MP3 via sendVoice mai provato dal vivo).
- Non ho fatto mutation testing mio: mi sono fidato dei 6 mutanti dichiarati.

**Memoria**
Ho aggiunto in coda a /tmp/claude-0/wt48/.claude/agents/memoria_revisore.md la riga #720 (BOCCIATO) più una lezione: un pool o thread nuovo nel bot rompe T78p, quindi va lanciato `tests/test_unit_kernel.py`, e allargare la guardia è un cambio di sicurezza. NON l'ho committata, come mi hai chiesto: per questo non ho eseguito `scripts/commit_memoria_revisore.sh`.

**Per la ri-review**: guardia T78p corretta in modo mirato, riga vuota in fondo a tests/test_unit_telegram_voce.py tolta, e il runner del kernel con il solo FAIL T31g, uguale alla base.

Review #721 (ri-review, senza thread), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #721 (chat Mani), ri-review della #720 sullo staged di /tmp/claude-0/wt48 (mani/telegram3, base b827447). Il blocco della #720 è risolto: T78p torna verde e la guardia delle firme non è toccata. Secondo me la PR rientra nella regola notturna: restano solo riserve BASSE o COSMETICHE e niente di sicurezza.

**Prove (su una copia dell'index fatta con `git checkout-index`, senza stash)**
- `tests/test_unit_telegram_voce.py`: 59 passed. Con `test_unit_voice_server.py` e `test_unit_voice_tts.py`: 213 passed.
- `python tests/test_unit_kernel.py`: 1099 PASS, 1 FAIL. È solo T31g, legato all'ambiente e presente anche sulla base. T78p è PASS con il pool solo in `_invia_a_tutti`.
- `git diff --cached --check`: pulito, la riga vuota in fondo al file è sparita.

**Elementi esaminati**
- modules/telegram/bot.py:987 — la voce torna in linea nel polling dopo il testo. Rischi: thread e ordine. Esito ok: nel bot non ci sono più `_consegna_voce`, `_voce_in_coda` né un pool nuovo (grep fatto), l'unico `ThreadPoolExecutor` resta a :368 in `_invia_a_tutti`. Il testo parte prima della voce. Il problema di thread safety e quello dello spegnimento sollevati nella #720 non esistono più.
- modules/telegram/bot.py:64 — `VOCE_TIMEOUT_S = 15`, usato a :1043 da `synthesize_speech(..., timeout=)` (modules/voice/tts.py:84 accetta `timeout` keyword-only) e a :1049 da `_tg_post_file(..., timeout=)`. Rischi: firma sbagliata e §9. Esito ok: tutte e due le chiamate stanno dentro i percorsi fail-safe di prima (try generico per la sintesi, `None` → avviso breve per l'invio).
  - Riserva R-721-1 BASSA: R-717-4 è chiusa solo in parte, il polling può restare fermo fino a circa 30 s per vocale.
  - Riserva R-721-2 BASSA: in urllib e http.client il timeout vale per ogni singola attesa sul socket, non per l'operazione intera. I «circa 30 s» sono il caso tipico, non un tetto garantito. Il commento a :61-63 va letto così.
- modules/telegram/bot.py:932 e :980 — `**extra`, `cervello=forte` e l'istruzione del parlato, uguali alla #720. Rischi: i testi normali cambiano, istruzione con voce spenta, import rotto. Esito ok: `_risposta_del_turno` non passa extra, quindi la chiamata equivale a `run_turn(text)`. I test della voce spenta e dell'import rotto passano.
- modules/telegram/bot.py:995 — `testo_da_dire`. Rischio privacy verso ElevenLabs. Esito ok: la fonte è sempre `finale` e il testo viene solo ridotto. La riga vuota resta, quindi i dettagli restano solo nel testo.
  - Riserva R-721-3 COSMETICA: `_URL` (:992) si mangia anche la punteggiatura finale.
- tests/test_unit_telegram_voce.py:475 — `test_voce_con_tempi_corti`: controlla che sintesi e invio ricevano 15. Rischio: il test non prende il valore sbagliato. Esito ok: verifica sia il valore passato sia la costante. I 2 mutanti dichiarati sono plausibili, non li ho rieseguiti.

**Regola notturna**
Il diff tocca solo il ramo dei vocali del bot e i suoi test. Il flusso delle firme e la guardia T78p non sono toccati. Ai modelli non arrivano dati nuovi (l'istruzione è testo fisso più data e ora, e va allo stesso cervello di prima). Verso ElevenLabs va meno testo di prima. Quindi nessun aspetto di sicurezza: il merge autonomo è ammesso se anche il bot dà solo BASSE o COSMETICHE.

**Non verificato**
- sendVoice ed ElevenLabs dal vivo, e i tempi reali con 15 s su rete lenta: non si possono riprodurre qui. R-717-3 resta aperta.
- Non ho rieseguito i mutanti.
- Non ho rifatto la suite notte e voce_ascolto: i file che usano non sono cambiati rispetto alla #720, dove davano 682 passed.

**Memoria**
In /tmp/claude-0/wt48/.claude/agents/memoria_revisore.md ho aggiunto la riga #721 (APPROVATO CON RISERVE, con R-721-1, R-721-2 e R-721-3) e una lezione: un `timeout=` limita ogni attesa sul socket, non la durata totale. Non l'ho committata. In coda al file c'è anche la riga #720 della review precedente, anche quella non committata.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_telegram_voce.py`: da 51 a 59 casi.

```
59 passed in 0.13s
```

`python tests/test_unit_kernel.py` sull'albero della fetta: 1099 PASS, 1 FAIL. Il FAIL è T31g: vector store assente nell'ambiente, presente anche sulla base. T78p è PASS.

Mutanti presi:
- niente istruzione del parlato;
- niente pulizia del markdown;
- sintesi senza testo_da_dire;
- tempi da 30 s, sia per la sintesi sia per l'invio.

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP). Per il commit 792b365 e per il commit di fine-task che contiene questo file la run non è ancora disponibile alla scrittura dell'handoff. La PR #355 su ef0e038 aveva unit-suite e handoff-check success ed è stata mergiata.

## §7 RISERVE APERTE

- R-721-1 BASSA: R-717-4 è chiusa solo in parte; il polling resta fermo fino a circa 30 s per vocale.
- R-721-2 BASSA: il timeout vale per ogni attesa sul socket, non per l'operazione intera.
- R-721-3 COSMETICA: la regex degli URL si mangia la punteggiatura finale.
- R-717-3 BASSA: l'MP3 su sendVoice non è ancora provato dal vivo.
- Le altre riserve sono in `reports/stato_progetto.md`.
