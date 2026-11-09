# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-09 notte — chat Mani: voce via Telegram, fetta 3 (turno parlato, niente formattazione a voce, tempi della voce più corti)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #357 (https://github.com/Gasss23/Gas/pull/357): decide l'operatore. La verifica esterna #357 ha dato una V-1 MEDIA di processo: il merge autonomo notturno non è scritto in CLAUDE.md §10.
2. Opzioni per la voce del bot in un thread (decisione di sicurezza, R-717-4): (a) lasciare com'è (un solo thread, voce a 15 s, polling fermo circa 30 s per vocale); (b) un thread SOLO per sintesi e invio della voce, che non tocca mai update né firme, con la guardia T78p allargata in modo mirato e un test che lo vieta (consigliata); (c) la voce mandata da un processo separato tramite una coda su file (non tocca il bot, più complessa).

---

## §1 SCOPE & ESITO FETTE

- **PR #355 (fetta 2)**: `FATTA` — mergiata (b827447).
- **Fetta 3, turno parlato e pulizia della voce (V-1 bot #355)**: `FATTA`.
- **Fetta 3, tempi della voce più corti (V-1 ve #355, R-717-4 in parte)**: `FATTA`.
- **V-3 della verifica esterna #357 e R-723-1 (dettagli detti a voce con a capo non standard)**: `FATTA` — review #723/#724.
- **Voce consegnata in un thread**: `DEFERITA — tocca la guardia T78p delle firme (review #720 BOCCIATO); decide l'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 +++++++
 modules/telegram/bot.py            |  50 ++++++++++++++++++++++++++++++++++++++++++--------
 reports/diff_sessione.md           |  11 +++++------
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  36 ++++++++++++------------------------
 tests/test_unit_telegram_voce.py   |  84 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main b827447 (dopo il merge della PR #355).

## §3 GIT LOG --ONELINE (sessione)

```
363cd72 fix(telegram): a voce niente dettagli anche con a capo non standard (V-3 ve #357, R-723-1) — review #723/#724
d27b040 docs(fine-task): verdetto #720 riemesso per il gate B
fee3311 docs(fine-task): voce via Telegram fetta 3 chat Mani — review #720/#721
792b365 feat(telegram): voce via Telegram, fetta 3 — istruzione del parlato, niente formattazione a voce, tempi della voce più corti (riserve #355) — review #720/#721
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push. Il codice è stato scritto e revisionato nel worktree locale /tmp/claude-0/wt48 sulla stessa base, poi portato qui in fast-forward.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #720 (prima versione, con il thread), verdetto integrale RIEMESSO per il gate B. Stesso esito e contenuto; cambiano solo le citazioni, perché quelle originali puntavano a righe del test poi tolte. L'originale è nella storia git di questo file, commit fee3311:

## VERDETTO: BOCCIATO

Riemesso per il gate B: verdetto #720, stesso esito e stesso contenuto, ho cambiato solo le citazioni. Ora puntano a righe che esistono a HEAD fee3311 in /home/user/Gas; il codice del thread e i test tolti nella ri-review sono citati a parole. Non ho toccato memoria e repo.

Review #720 (chat Mani). Diff staged in /tmp/claude-0/wt48 (branch mani/telegram3, base b827447). Ho letto CLAUDE.md (sez. 5), le parti di reports/stato_progetto.md su Telegram e voce, e la memoria del revisore (il numero più alto era #719).

**Motivo del blocco**
La suite del motore diventa rossa. Ho lanciato `python tests/test_unit_kernel.py` su una copia dell'index (non è pytest: è quello che la CI esegue nel job `unit-suite`).
- Copia dell'index: 1098 PASS, 2 FAIL.
- Base b827447: 1099 PASS, 1 FAIL. Il FAIL è T31g, legato all'ambiente e presente anche sulla base.
- **T78p è una regressione nuova**: `[] ['_invia_a_tutti', '_consegna_voce']`. La guardia statica tests/test_unit_kernel.py:8389 protegge la firma con i bottoni, «un click alla volta». Vuole un solo `ThreadPoolExecutor` nel bot, quello in `_invia_a_tutti` (modules/telegram/bot.py:368).
- Il diff aggiungeva un secondo pool: il `ThreadPoolExecutor(max_workers=1)` creato in modo lazy dentro `_consegna_voce`, accanto alla variabile di modulo `_voce_in_coda` (codice poi tolto, quindi lo cito a parole). Così la CI sarebbe stata rossa e la PR non mergiabile.
- Nel merito la regola della firma non era violata: il thread eseguiva solo `_invia_risposta_vocale`, mai i gestori degli update.
- Correzione possibile: allargare T78p in modo mirato. Però quella guardia protegge la firma, quindi è un cambio di sicurezza: fuori dalla regola notturna, serve il sì dell'operatore.

**Elementi esaminati (righe a HEAD)**
- modules/telegram/bot.py:933 — `run_turn(text, **kw)`; per i messaggi di testo `kw` è vuoto. Rischio: cambiano i testi normali. Esito ok: la chiamata equivale a `run_turn(text)`; `cervello=forte` si aggiunge solo se richiesto (modules/telegram/bot.py:932).
- modules/telegram/bot.py:973 — `_voce_accesa()` si legge una sola volta; l'istruzione del parlato si importa dentro un try (modules/telegram/bot.py:980). Rischi: istruzione con la voce spenta, crash se l'import fallisce. Esito ok: i test tests/test_unit_telegram_voce.py:431 e tests/test_unit_telegram_voce.py:439 lo coprono; il log riporta solo il tipo dell'eccezione (§9).
- Consegna della voce (a parole: la chiamata a `_consegna_voce` dopo l'invio del testo, oggi sostituita da modules/telegram/bot.py:987). Rischio: la voce arriva prima del testo. Esito ok: il testo veniva inviato prima, in modo sincrono.
- `_consegna_voce` e il suo pool (a parole: codice tolto). Rischi esaminati:
  - Thread safety: ok. `_tg_post`, `_send_text` e `_tg_post_file` fanno ognuno una richiesta urllib a sé, senza stato condiviso. Il pool lazy veniva creato solo dal thread del polling.
  - Ordine e una consegna alla volta: ok.
  - Errore in `submit`: ok, finiva solo nel log.
  - **BLOCCO**: rompe T78p.
- Spegnimento del pool (a parole). Riserva BASSA:
  - I worker non erano daemon e Python li aspetta all'uscita (atexit). Dopo Ctrl-C il processo avrebbe atteso i vocali in coda: al massimo 30 all'ora, circa 60 s ciascuno. Un secondo Ctrl-C lo chiude.
  - Con SIGTERM e il gestore di default l'uscita è immediata.
  - Non è un crash.
- modules/telegram/bot.py:995 — `testo_da_dire`. Rischio privacy verso ElevenLabs. Esito ok:
  - La fonte resta sempre `finale` e il testo viene solo ridotto: URL sostituiti con «link», tolti i segni di formattazione, poi `parte_parlata`.
  - Le regex con `[ \t]` (modules/telegram/bot.py:990) lasciano la riga vuota, quindi il dettaglio resta solo nel testo (tests/test_unit_telegram_voce.py:454).
  - La chiamata sta dentro il try di modules/telegram/bot.py:1043, quindi anche un ImportError è coperto (§9).
- modules/telegram/bot.py:992 — `_URL` con `\S+`. COSMETICA: si mangia anche la punteggiatura finale. Anche `__` toglie gli underscore da nomi come `__init__`.
- Test (a parole: righe tolte nella ri-review):
  - Il fixture `tg` (tests/test_unit_telegram_voce.py:27) rendeva sincrona la consegna: ok.
  - Il test del pool vero (ordine, una consegna alla volta, ritorno immediato) era deterministico: Event con timeout di 5 s. Il «1 failed» non l'ho riprodotto: 30 esecuzioni su 30 e 40 su 40 verdi.
  - `git diff --cached --check` segnalava una riga vuota in fondo a tests/test_unit_telegram_voce.py. COSMETICA.

**Altri controlli**
- pytest su telegram_voce, voice_server, voce_ascolto e notte: 682 passed. Nessuno stash.
- Wall of Shame pulito: niente tagli diretti della cronologia, niente simulazione degli strumenti.
- Il tetto di 10 iterazioni e `_get_window` non sono toccati.

**Non verificato**
- sendVoice ed ElevenLabs dal vivo, e lo spegnimento sotto systemd: non riproducibili qui.
- Non ho fatto mutation testing mio.

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

Review #723, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #723 (chat Mani): diff staged su claude/peaceful-lovelace-0w2b7q, HEAD d27b040, PR #357, correzione della V-3 della verifica esterna #357.

Nota di processo: al primo esame `git diff --staged` era vuoto, perché le modifiche erano solo nel working tree. Dopo il tuo avviso ho ricontrollato `git diff --cached`: modules/telegram/bot.py +3 e tests/test_unit_telegram_voce.py +8, uguali a quelle che avevo già letto nel working tree.

Elementi del diff esaminati:
- modules/telegram/bot.py:1002 — dentro `testo_da_dire`, «\r\n» e poi «\r» diventano «\n» prima di `_MARKDOWN`/`_URL` e di `parte_parlata`. Rischi esaminati:
  - l'ordine delle due sostituzioni: «\r\n» viene trattato per primo, quindi non nasce un «\n\n» spurio;
  - la regex `_MARKDOWN` con `^` MULTILINE resta corretta;
  - la variabile è locale, quindi l'oggetto del chiamante non cambia.
  Esito: ok.
- modules/telegram/bot.py:985 — il testo mandato a Telegram è `risposta` (da `_turno_con_finale`) e non passa per `testo_da_dire`. Quindi la normalizzazione vale solo per il testo da dire. Esito: ok.
- modules/telegram/bot.py:1046 — è l'unico punto che manda testo a ElevenLabs: `synthesize_speech(testo_da_dire(finale), …)`. Sta dentro try/except con log.warning e un avviso breve all'operatore (§9). Ho cercato con grep `parte_parlata` e `testo_da_dire` in modules/ e gas.py: nessun altro percorso del bot porta dettagli alla voce. L'altro uso, modules/voice/server.py:799, è la voce di casa e non è toccato dal diff. Esito: ok.
- tests/test_unit_telegram_voce.py:486 — test parametrico con 3 casi: «\r\n\r\n», «\r\r», misto «\n\r\n». Esito: ok. Sulla copia dell'index (`git checkout-index`, niente stash) ho ottenuto:
  - 62 passed;
  - mutante con la riga 1002 sostituita da `pass`: 3 failed, 59 passed;
  - `git diff --cached --check` pulito.
- modules/voice/server.py:234 (contesto, file non toccato) — `_PARAGRAFO = r"\n[ \t]*\n"`. Esito: riserva, vedi sotto.

Riserve:
- R-723-1 BASSA: la correzione chiude il caso «\r» ma non tutta la classe di errori. L'ho provato su queste tre forme:
  - «Fatto.  dettaglio segreto» → «Fatto. dettaglio segreto»;
  - «Fatto.\n\xa0\ndettaglio segreto» (riga di solo NBSP, lo spazio non separabile) → «Fatto. dettaglio segreto»;
  - «Fatto.\x0c\x0cdettaglio segreto» → «Fatto. dettaglio segreto».

  In tutti e tre i casi il dettaglio va ancora a ElevenLabs. Il motivo: `str.split()` tratta questi caratteri come spazi, mentre la regex `[ \t]` no. Sono casi rari nell'output dei modelli. Va tracciata in stato_progetto.md. La correzione possibile è normalizzare anche ` `, ` `, `\f`, `\v` e allargare `[ \t]` a `[^\S\n]`, dentro `testo_da_dire` o in `_PARAGRAFO`. Quest'ultima scelta tocca anche la voce di casa.

Rischi esclusi (non verificati):
- Il runner a script `python tests/test_unit_kernel.py` non l'ho lanciato. Il diff non aggiunge thread né pool e non tocca le firme, quindi la guardia T78p non è coinvolta. La conferma resta alla CI `unit-suite`.
- Non ho verificato la sintesi reale con ElevenLabs e l'invio a Telegram: richiedono chiavi e rete.

Memoria: la riga #723 e una lezione sono in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, nel working tree e NON committate, come richiesto. Il numero più alto che ho trovato nel repo era #721, quindi ho usato #723 come indicato.

File rilevanti:
- /home/user/Gas/modules/telegram/bot.py
- /home/user/Gas/tests/test_unit_telegram_voce.py
- /home/user/Gas/modules/voice/server.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

Review #724, verdetto integrale:

## VERDETTO: APPROVATO

Review #724 (chat Mani): ri-esame della #723 sul diff staged in claude/peaceful-lovelace-0w2b7q (HEAD d27b040, PR #357). La riserva R-723-1 (a capo non standard che portavano il dettaglio a ElevenLabs) è chiusa e non ci sono riserve nuove.

Elementi del diff esaminati:
- modules/telegram/bot.py:1003. Cosa fa: `splitlines()` più `"\n".join`, e una riga fatta solo di spazi diventa vuota. Rischi esaminati:
  - **Caratteri persi dal testo da dire:** nessuno oltre agli a capo e agli spazi delle righe vuote. Ho fatto una prova a caso su 20000 stringhe con \r,  , \x85, \f, NBSP e tab: la sequenza dei caratteri che non sono spazi resta identica.
  - **Testo con contenuto:** le righe che contengono testo restano intatte, spazi iniziali compresi.
  - **A capo finale:** viene perso, ma è innocuo, perché `parte_parlata` fa comunque `strip()` e poi `" ".join(split())`.
  - **Dove agisce:** la variabile è locale. `_PARAGRAFO` (modules/voice/server.py:234) e la voce di casa non sono toccati.
  - Esito: ok.
- modules/telegram/bot.py:985. Il testo mandato a Telegram è `risposta`, non `finale`, e non passa da `testo_da_dire`: non viene toccato. Esito: ok.
- modules/telegram/bot.py:1047. È l'unico invio a ElevenLabs, `synthesize_speech(testo_da_dire(finale), …)`, ed è dentro un try/except con log.warning e avviso all'operatore (§9). Nessun altro percorso del bot porta dettagli alla voce. Esito: ok.
- tests/test_unit_telegram_voce.py:486. Il test parametrico ha 7 casi: \r\n, \r, misto, U+2028, NBSP, \f, e spazio/tab/U+3000. Sulla copia dell'index (`checkout-index`, niente stash) ho ottenuto:
  - 66 passed;
  - il mutante col vecchio `.replace` viene preso: 4 failed;
  - `git diff --cached --check` è pulito.
  Esito: ok.

Nota non bloccante, senza codice di riserva: una riga fatta solo di U+200B (spazio a larghezza zero) non conta come spazio per `str.strip()`. Quindi non diventa vuota e il dettaglio verrebbe detto: «Fatto.\n​\ndettaglio segreto» diventa «Fatto. ​ dettaglio segreto». È un caso praticamente assente nell'output dei modelli.

Cosa non ho verificato:
- Il runner a script `tests/test_unit_kernel.py`: il diff non aggiunge concorrenza né tocca firme, quindi T78p non è coinvolta. La conferma la dà la CI `unit-suite`.
- La sintesi reale con ElevenLabs e l'invio a Telegram: servono chiavi e rete.

Memoria: la riga #724 è in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, nel working tree e NON committata.

File:
- /home/user/Gas/modules/telegram/bot.py
- /home/user/Gas/tests/test_unit_telegram_voce.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_telegram_voce.py`: da 51 a 66 casi.

```
66 passed in 0.12s
```

`python tests/test_unit_kernel.py` sull'albero della fetta: 1099 PASS, 1 FAIL. Il FAIL è T31g: vector store assente nell'ambiente, presente anche sulla base. T78p è PASS.

Mutanti presi:
- niente istruzione del parlato;
- niente pulizia del markdown;
- sintesi senza testo_da_dire;
- tempi da 30 s, sia per la sintesi sia per l'invio.

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP). d27b040: handoff-check success. Verifica esterna APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/357#issuecomment-6730508364). Per 363cd72 e per il commit di fine-task che contiene questo file la run non è ancora disponibile alla scrittura dell'handoff. La PR #355 su ef0e038 aveva unit-suite e handoff-check success ed è stata mergiata.

## §7 RISERVE APERTE

- Verifica esterna #357:
  - V-1 MEDIA di processo: decide l'operatore.
  - V-2 BASSA: 15 s possono dare più avvisi su rete lenta.
  - V-3: corretta.
  - V-4 COSMETICA.
  - V-5 COSMETICA.
- R-721-1 BASSA: R-717-4 è chiusa solo in parte; il polling resta fermo fino a circa 30 s per vocale.
- R-721-2 BASSA: il timeout vale per ogni attesa sul socket, non per l'operazione intera.
- R-721-3 COSMETICA: la regex degli URL si mangia la punteggiatura finale.
- R-717-3 BASSA: l'MP3 su sendVoice non è ancora provato dal vivo.
- Le altre riserve sono in `reports/stato_progetto.md`.
