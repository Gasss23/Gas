# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-09 — Voce, velocità: in cache anche le frasi fisse divise nelle risposte a pezzi (chat M2, coordinata da M1); PR #358 (sicurezza) mergiata

---

## §0 DECISIONI UMANE RICHIESTE

1. Nessuna: l'operatore ha dato il sì al merge della #360 con la nota cosmetica (riferito da M1, 9/11 sera).
2. Restano dalla #358 (mergiata): IPv4 d'esempio nei test costruiti da intero (marcatore `gasmerge-ip-ok` sì/no); limite «rete privata solo dichiarativa» da chiudere prima del VPS.

---

## §1 SCOPE & ESITO FETTE

- **PR #358, server voce più sicuro (R8 fetta 1)**: `MERGIATA` (567beb7) col sì dell'operatore riferito da M1 (bot e verifica esterna senza ALTA/MEDIA).
- **Velocità, frasi fisse divise in cache**: `FATTA` — in `modules/voice/server.py` `_FRASI_FISSE` contiene anche le frasi delle costanti come le divide `_dividi_frasi` (es. l'uso di «forte», due frasi), così anche nelle risposte a pezzi vengono dalla cache; commento del filtro riscritto (guarda il contenuto, non la provenienza). Chiude bot #356 V-1 BASSA e V-2 COSMETICA. Review #725-M2 APPROVATO; riposizionato sopra main dopo la #358 (patch identica), review #735-M2 APPROVATO.
- **Bot #360 V-1 BASSA** (manca un test sul percorso vero «forte» → risposta a pezzi): `FATTA` — `test_sintesi_cache_forte_a_pezzi_dal_server`; review #737-M2 APPROVATO. Bot #360 2° giro (COSMETICA: il test controllava solo la scrittura della cache) `FATTA`: seconda richiesta letta dalla cache; review #740-M2 APPROVATO. Bot #360 3° giro: V-1 BASSA (confronto coi tempi misurati, test instabile) `FATTA`, review #741-M2 APPROVATO. Verifica esterna #360 su 07ea908 (prima dei test aggiunti dopo): APPROVATO (https://github.com/Gasss23/Gas/pull/360#issuecomment-6750706419).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 +
 modules/voice/server.py            |  12 +-
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_voice_server.py    |  47 ++-
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main 695b759 (merge della #359 di Mani, entrato nel branch col merge di questa sessione).

## §3 GIT LOG --ONELINE (sessione)

```
34a0d67 Merge origin/main (#359 di Mani) nella PR #360
ce0cbe4 docs(voce): report #360 allineati al diff (2 test, ripartenza) — bot 4° giro (chat M2)
7de5d6b docs(voce): report #360 — review #741, numeri dei test allineati (chat M2)
8984e81 test(voce): il confronto della seconda richiesta «forte» ignora i tempi misurati (bot #360, 3° giro: test instabile)
dd2d61e chore(revisore): memoria review #741 — APPROVATO
d6af23f docs(voce): report #360 — review #740 (chat M2)
dd0444f test(voce): la seconda richiesta «forte» legge i pezzi dalla cache (bot #360, 2° giro)
a378624 chore(revisore): memoria review #740 — APPROVATO
1e74840 docs(voce): report #360 — test del bot V-1, review #737 (chat M2)
2067dd9 test(voce): la risposta d'uso di «forte» a pezzi passa dalla cache sul percorso vero del server (bot #360 V-1)
8445011 chore(revisore): memoria review #737 — APPROVATO
07ea908 docs(voce): report di fine task — frasi fisse divise in cache; PR #358 mergiata (chat M2)
b660d1c chore(revisore): memoria review #735 — APPROVATO
36adbd9 perf(voce): in cache anche le frasi fisse divise nelle risposte a pezzi; commento del filtro corretto (bot #356 V-1/V-2)
8b95a14 chore(revisore): memoria review #725 — APPROVATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #725-M2 sul commit originale a80e4b8 (verdetto integrale):

## VERDETTO: APPROVATO

Review #725-M2: diff in staging su feat/voce-locale-fila, nella worktree /home/user/Gas-sicura. Tocca 2 file (+26/-4).

**Elementi del diff esaminati**
- `modules/voice/server.py:321` — `_FRASI_FISSE_INTERE` è la tupla delle 7 costanti intere. Ho controllato l'ordine di definizione: `_dividi_frasi` (`modules/voice/server.py:269`) e tutte le costanti sono definite prima di questo punto, quindi non c'è NameError all'import. Esito: ok.
- `modules/voice/server.py:325` — `_FRASI_FISSE` = le costanti intere più i loro pezzi divisi da `_dividi_frasi`. L'ho verificato stampando l'insieme reale. I pezzi nuovi sono solo 2: «Dopo «forte» dimmi cosa fare, per esempio: «Gas, forte: riassumi i lead di oggi».» e «Non ho avviato nessun lavoro.». Le altre 6 costanti sono già di una frase sola. Chiude V-1 BASSA. Esito: ok.
- Il rischio che mi hai chiesto di guardare. Un testo del modello può coincidere solo con «Non ho avviato nessun lavoro.» (pezzo nuovo) o con «Va bene.» / «Dimmi.» (frasi intere che c'erano già prima di questo diff). Il confronto è esatto: la chiave `(synthesize_speech, voice_id, frase)` (`modules/voice/server.py:337`) richiede lo stesso testo e la stessa voce, quindi l'audio restituito è proprio quello del testo richiesto. È innocuo: nessuna fuga di contenuto e nessun audio sbagliato. Il tetto `_CACHE_FRASI_MAX = 32` (`modules/voice/server.py:327`) resta molto sopra le 9 voci per ogni voce. Esito: ok.
- `modules/voice/server.py:315` — il commento ora dice «entra in cache solo un testo IDENTICO a una di queste costanti…», cioè descrive il filtro per contenuto e non più la provenienza. Chiude V-2 COSMETICA. Esito: ok.
- `tests/test_unit_voice_server.py:2080` — `test_sintesi_cache_anche_per_le_frasi_divise`. Controlla che i pezzi vengano sintetizzati una volta sola su due giri, e che un testo diverso («pezzo + Altro.») non vada mai in cache. L'ho eseguito: `-k cache` dà 7 passed. Esito: ok.

**Rischi esclusi**
- Non ho verificato che il test fallisca col codice precedente: mi fido della tua prova, non l'ho rifatta.
- Non ho rieseguito la suite completa da 277 test, solo il sottoinsieme `-k cache`.
- Non ho verificato il comportamento con ElevenLabs reale né sul Mac: non è riproducibile qui.

**Memoria**
- Riga #725-M2 aggiunta in /home/user/Gas-sicura/.claude/agents/memoria_revisore.md e committata nella worktree con lo script (commit bef35b5).
- Nessuna lezione nuova. /home/user/Gas non l'ho toccato.

Review #735-M2 sul riposizionamento 36adbd9 (verdetto integrale):

## VERDETTO: APPROVATO

Il cherry-pick è corretto e non ci sono problemi bloccanti. Ho fatto le tre letture obbligatorie: CLAUDE.md, reports/stato_progetto.md (letto con Grep mirato) e .claude/agents/memoria_revisore.md.

**Elementi esaminati**
1. `modules/voice/server.py:324` — `_FRASI_FISSE_INTERE` e `_FRASI_FISSE`: l'insieme contiene le frasi intere più i pezzi prodotti da `_dividi_frasi`. Rischio esaminato: che il contesto nuovo della R8 fetta 1 interagisca col codice spostato. `_dividi_frasi` è definita prima (`modules/voice/server.py:272`) e le costanti sono già tutte definite. `_host_ammesso` (`modules/voice/server.py:572`) e `_autorizza` (`modules/voice/server.py:597`) non toccano mai `_FRASI_FISSE` né la cache. `sintesi()` viene chiamata solo nei rami di risposta (`modules/voice/server.py:1008`, `modules/voice/server.py:1051`, `modules/voice/server.py:1091`), dopo i controlli R8. Esito: ok.
2. `tests/test_unit_voice_server.py:2081` — `test_sintesi_cache_anche_per_le_frasi_divise`. È l'ultimo test della serie sulla cache di `sintesi`, subito prima del blocco «R8 fetta 1» (`tests/test_unit_voice_server.py:2099`), quindi è nel posto giusto. Da solo passa (1 passed). Esito: ok.
3. `.claude/agents/memoria_revisore.md:1394` — riga #725-M2 riportata col cherry-pick. Rispetto a `origin/main` il diff è +1 e −0. Nessuna riga del vecchio `origin/feat/voce-v12-m2` manca a HEAD (`comm` = 0). Esito: ok.
4. Le righe +/- di `git show a80e4b8` e `git show 36adbd9` sono identiche: il `diff` fra le due è vuoto. Esito: ok.

**Test:** `test_unit_voice_server`, `test_unit_sottofondo` e `test_unit_telegram_voce` con `-k "not browser"` danno 308 passed e 21 deselected. Tu ne dichiari 314: probabilmente hai usato una selezione diversa. Non è bloccante, ma nel report scrivi il comando esatto che hai usato.

**Rischio escluso:** i test con browser e la resa audio reale con ElevenLabs non li ho verificati, perché qui manca il browser e manca la chiave. Non ho rivalutato la parte di sicurezza R8, già approvata nella #734-M2.

**Memoria:** riga #735-M2 aggiunta e committata con lo script in `b660d1c` (`chore(revisore): memoria review #735 — APPROVATO`). Nessuna lezione nuova.

File: /home/user/Gas/modules/voice/server.py, /home/user/Gas/tests/test_unit_voice_server.py, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #737-M2 (verdetto integrale):

## VERDETTO: APPROVATO

Review #737-M2 sulla PR #360, branch feat/voce-v12-m2. Il diff staged contiene solo `tests/test_unit_voice_server.py` (+13 righe).

**Cosa ho controllato nel diff e nel codice**
- `tests/test_unit_voice_server.py:2099`: il nuovo test `test_sintesi_cache_forte_a_pezzi_dal_server` avvia il server vero tramite `_voce_a_pezzi`, con trascrizione «Gas, forte.» e formato audio+testo+pezzi.
  - Rischio esaminato: residui di cache lasciati da altri test (falso verde o falso rosso). La cache è sostituita con un dict nuovo tramite monkeypatch, quindi è isolata.
  - Rischio esaminato: falso verde se il server sintetizza altre frasi. L'asserzione è di uguaglianza esatta: le chiamate a synthesize_speech devono essere proprio `_dividi_frasi(_USO_FORTE_PARLATO)`, cioè 2 pezzi, nell'ordine giusto.
  - Esito: ok.
- `modules/voice/server.py:340`: la chiave della cache è `(synthesize_speech, voice_id, frase)`, quindi `k[2]` nel test è proprio la frase. L'asserzione `sorted(k[2] for k in cache) == sorted(pezzi)` controlla davvero che i pezzi stiano in cache. Esito: ok.
- `modules/voice/server.py:328`: `_FRASI_FISSE` comprende anche i pezzi divisi.
  - Mutante riprodotto da me (`_FRASI_FISSE = frozenset(_FRASI_FISSE_INTERE)`): il test dà 1 failed. Il file è stato ripristinato e `git status` mostra solo il file di test staged.
  - Il mio primo mutante scritto con sed era sbagliato per precedenza degli operatori (`A | B and C` vale `(A|B) and C`). L'ho rifatto: il risultato vale solo per il secondo.
  - Esito: ok.
- Test: `tests/test_unit_voice_server.py`, `tests/test_unit_sottofondo.py` e `tests/test_unit_telegram_voce.py` con `-k "not browser"` danno 309 passed e 21 deselected. Il dato dichiarato era 315: credo dipenda da una selezione diversa dei test (come in #735-M2), non da un fallimento.
- Wall of Shame (gli errori vietati da CLAUDE.md sez. 5): non c'entra. Nessuna storia dei messaggi, nessun output di tool simulato. Il mock di synthesize_speech riguarda un servizio esterno, non un tool del modello.

**Cosa non ho verificato**
- I test della pagina nel browser (`-k "not browser"`): in questo ambiente non c'è Playwright, e il diff non tocca il client.
- La latenza reale con ElevenLabs sul Mac: il test usa una sintesi finta, quindi il guadagno di velocità dal vero resta da provare.

**Dopo la review**
- Ho scritto la riga #737-M2 in `/home/user/Gas/.claude/agents/memoria_revisore.md`, con una lezione: rileggere i mutanti scritti con sed, per via della precedenza tra `|` e `and`.
- Ho committato la memoria con lo script: commit 8445011. Il file di test resta staged e non è committato.
- Non ho toccato `/home/user/Gas-sicura`.

Review #740-M2 (verdetto integrale):

## VERDETTO: APPROVATO

Ho controllato due punti del diff e uno del codice di contesto:
- `tests/test_unit_voice_server.py:1226`: il parametro facoltativo `tts=None` è stato aggiunto all'helper `_voce_a_pezzi`. Ho guardato se cambia il comportamento degli altri test: no. Senza `tts` il ramo è quello di prima, `patch(..., side_effect=sintesi)`, e con `tts` passato si usa `patch(..., new=tts)`. Il nome `tts` viene riassegnato da `as tts`, ma solo dopo che l'argomento `new=tts` è già stato calcolato, quindi non c'è errore. Con `new=` il patch restituisce l'oggetto passato, cioè lo stesso mock. Sugli altri test l'esito è invariato: la suite passa. Esito: ok.
- `tests/test_unit_voice_server.py:2113`: la seconda richiesta «Gas, forte.» usa lo stesso mock; il test controlla `tts2 is tts`, zero chiamate e `righe2 == righe`. Ho controllato se il test passa anche quando la cache non viene letta. La chiave della cache (`modules/voice/server.py:340`) è `(synthesize_speech, voice_id, frase)` ed è identica nelle due richieste, perché la funzione è lo stesso mock. `reset_mock()` conserva il `side_effect`. Mutante «cache mai letta» (`modules/voice/server.py:341` con `audio = None`): 4 test falliti, compreso questo; file rimesso a posto, nessuna modifica rimasta nel codice. Esito: ok.
- `modules/voice/server.py:334` (contesto, file non toccato): `sintesi()` legge la cache solo per le frasi in `_FRASI_FISSE`, quindi la seconda richiesta sulla risposta d'uso di «forte» la usa davvero. Esito: ok.

Test: voice_server + sottofondo + telegram_voce con `-k "not browser"`: 309 passed, 21 deselected. Tu ne dichiari 315: credo che la selezione sia diversa, come nelle review #735 e #737. Nota: il file si chiama `tests/test_unit_sottofondo.py`, non `test_unit_voice_sottofondo`.

Cosa non ho verificato:
- I test che usano il browser: non li ho eseguiti.
- La velocità reale con ElevenLabs: il test usa un mock, quindi non la misura.
- `/home/user/Gas-sicura`: non toccato.

Memoria: riga #740-M2 aggiunta e committata con `scripts/commit_memoria_revisore.sh` (a378624). Il diff staged in `tests/test_unit_voice_server.py` è intatto.

File: /home/user/Gas/tests/test_unit_voice_server.py, /home/user/Gas/modules/voice/server.py, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #741-M2 (verdetto integrale):

## VERDETTO: APPROVATO

La correzione funziona: il test ora ignora solo la chiave «tempi» e confronta ancora tutto il resto.

**Elementi esaminati**
- `tests/test_unit_voice_server.py:2120` — una lambda toglie la chiave «tempi» da ogni riga NDJSON (ogni riga di testo JSON della risposta) prima del confronto.
  - Rischio: che il filtro nasconda altri campi che cambiano fra una richiesta e l'altra, oppure che renda il confronto inutile.
  - Esito: ok. Ho stampato le righe vere della risposta «Gas, forte.». Sono tre:
    - riga 1: `content`, `uso`, `capito`, `pezzi`, `audio`
    - riga 2: `audio`
    - riga 3: `fine`, `tempi`
  - Non ci sono id, istanti né valori casuali. L'audio (base64 della frase) e la riga `{"fine": true}` restano confrontati, quindi il confronto continua a provare che l'audio preso dalla memoria è identico a quello sintetizzato.
- `modules/voice/server.py:1073` (contesto) — la riga finale `{"fine": True, "tempi": …}`. I tempi vengono da `_chiudi_tempi` (`modules/voice/server.py:527`) e da `_segna` (`modules/voice/server.py:519`), misurati con `time.monotonic()` e arrotondati a 0,01 s.
  - Rischio: altri campi che dipendono dal tempo.
  - Esito: ok. «tempi» è l'unico campo legato al tempo nel ramo a pezzi (`modules/voice/server.py:1043-1073`).
- `tests/test_unit_voice_server.py:2117` — `tts.call_count == 0` resta un controllo della lettura dalla cache, indipendente dal confronto delle righe. Esito: ok.
- Il test passa in locale (1 passed). Nel diff ci sono solo cambiamenti al test, nessuna modifica al motore né ai guardrail. Nessun antipattern del Wall of Shame.

**Rischio escluso**
- Il mutante «cache mai letta» non l'ho rieseguito io: mi fido della prova dichiarata e della review #740-M2, che lo aveva già riprodotto.
- Non ho verificato su un runner CI lento: non si riproduce qui.
- Con l'argomento `root` attivo, la prima riga può avere altri campi (i compiti in sottofondo). Non ho verificato se dipendono dal tempo perché questo test non usa `root`.

- Contatore #741-M2 aggiunto in `/home/user/Gas/.claude/agents/memoria_revisore.md` e committato (dd2d61e).

Review #742-M2 sul merge di main (verdetto integrale):

## VERDETTO: APPROVATO

Review #742-M2: merge in corso di origin/main 695b759 (PR #359) dentro feat/voce-v12-m2 (PR #360, head ce0cbe4). Base comune 567beb7.

**Elementi esaminati**
- `modules/voice/server.py:324-329`: la #360 crea `_FRASI_FISSE_INTERE` e `_FRASI_FISSE`, che ora contiene anche le frasi divise da `_dividi_frasi`. Rischio controllato: che la #359 (in `modules/telegram/bot.py`) dipenda da questo blocco o dalla cache di `sintesi()`. Esito: ok. Rispetto alla base, la #360 cambia solo queste righe di `server.py`. Gli oggetti di `server.py` che `bot.py` importa (`_USO_FORTE_PARLATO` a :119, `istruzione_turno_voce` a :266, `parte_parlata` a :351, `cervello_voce` a :456) non sono toccati.
- `modules/telegram/bot.py:1081` (contesto, file in arrivo da main): la voce di Telegram sintetizza con `modules.voice.tts.synthesize_speech`, non con `server.sintesi`. La cache delle frasi fisse quindi non entra in gioco. I punti d'import sono `bot.py:969`, `:984` e `:1035`. Esito: ok. `clients/voice/ascolto.py` non importa nulla da `modules.voice`: cita `server.py` solo nella docstring.
- `tests/test_unit_voice_server.py:2084` e `tests/test_unit_voice_server.py:2102`: sono i test della #360 (frasi divise in cache, «forte» a pezzi dal server). Rischio controllato: che si rompano dopo il merge. Esito: ok, la suite passa.
- `.claude/agents/memoria_revisore.md:1415` (unione dei due lati): dalla versione di HEAD (1398 righe) e da quella di MERGE_HEAD (1410 righe) non manca nessuna riga, verificato con `grep -vxFf` in entrambe le direzioni. Il file risultante ha 1415 righe e zero marcatori di conflitto. Esito: ok.
- I file di codice e test in arrivo (`clients/voice/ascolto.py`, `modules/telegram/bot.py`, `tests/test_unit_kernel.py`, `tests/test_unit_telegram_voce.py`, `tests/test_unit_voce_ascolto.py`) sono identici a 695b759: `git diff --cached MERGE_HEAD` su ciascuno è vuoto.
- `reports/stato_progetto.md`: differisce da main solo nella riga R8, dove resta la versione M2 «✅ PR #358 MERGIATA». È un merge automatico corretto, perché main conservava la riga vecchia della base («🔄 PR aperta»).
- Nessun marcatore di conflitto in `reports/`, `.claude/`, `modules/`, `clients/` e `tests/`. Nessuno slicing della history e nessuna simulazione di tool nel diff.

**Test eseguiti**
- Voice server, voce Telegram, ascolto voce e sottofondo con `-k "not browser"`: 606 passed, 25 deselected. Tu ne avevi dichiarati 616, quasi certamente perché la selezione dei test è diversa.
- Suite del kernel `tests/test_unit_kernel.py` (si lancia come script, non con pytest): 1099 PASS, 1 FAIL. Il FAIL è T31g ed è dovuto all'ambiente: qui manca `sentence_transformers`, quindi il vector store risulta non disponibile. T31g non è toccato da questo merge.

**Cosa NON ho verificato**
- I test browser (deselezionati) e il comportamento reale di Telegram e del server voce sul Mac/VPS: non si possono riprodurre in questo ambiente.
- Il contenuto di handoff, ultimo_report e diff_sessione tenuti dal tuo lato: sono report, fuori dal perimetro tecnico di questa review.

**Memoria**
- Ho aggiunto la riga contatore #742-M2 in `/home/user/Gas/.claude/agents/memoria_revisore.md` e fatto solo `git add` su quel file, come chiesto. Nessuna lezione nuova.
- Non ho lanciato `commit_memoria_revisore.sh`, perché committerebbe durante il merge. La memoria entra nel commit di chiusura del merge.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py`: +2 test — `test_sintesi_cache_forte_a_pezzi_dal_server` (percorso vero «forte» a pezzi, scrittura e seconda lettura della cache) e `test_sintesi_cache_anche_per_le_frasi_divise` (i pezzi di una frase fissa si sintetizzano una volta sola; un testo diverso mai in cache); col codice precedente fallisce. Comando: `pytest -q tests/test_unit_voice_server.py tests/test_unit_sottofondo.py tests/test_unit_telegram_voce.py -k "not conversazione_nel_browser"` → 314 passed, 15 deselected; dopo il test del bot #360 V-1: 315 passed (il revisore con `-k "not browser"` ne deseleziona 21: filtro diverso). `gas.py` non toccato.

## §6 STATO CI

Head ce0cbe4: unit-suite, handoff-check e verifica-bot success (bot: APPROVATO CON RISERVE, 1 COSMETICA accettata dall'operatore). Nuovo head col merge di main (#359): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Dalla #358: R-720-2-M2 (client locale col token vecchio blocca tutti per 15 min), R-720-5-M2 (log per richiesta bloccata), R-726-1-M2, R-730-1/2-M2, R-731-2-M2; limite: con la rete privata non si verifica che l'IPv4 sia del tunnel; client via tunnel con un nome (MagicDNS) → 403.
- Ve #356 V-4 BASSA: `api_key` non nella chiave della cache (innocuo: l'audio dipende da testo e voce).
- Non verificato in dev: guadagno di latenza reale con ElevenLabs.
