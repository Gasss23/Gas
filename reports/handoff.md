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
