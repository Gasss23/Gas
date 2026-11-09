# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-09 notte — Voce: cache della sintesi per le frasi fisse + riserve BASSE della #354 (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. **Merge della #356 (riserve BASSE/COSMETICHE): decide l'operatore.** Per allineamento con M1 (9 nov notte) stanotte nessuno mergia PR con riserve: vale CLAUDE.md §10 (solo APPROVATO pulito). La regola notturna NON è stata scritta nel repo: un agente non si scrive da sé l'autorizzazione a mergiare.
2. Prossima PR di stanotte: server voce reso sicuro (R8) — proposta + codice, resta aperta per l'operatore.

---

## §1 SCOPE & ESITO FETTE

- **PR #354** (riserve BASSE aperte): `MERGIATA` (fa6b1f3) col sì dell'operatore via M1, dopo il merge della #353 di Mani nel branch (review #714-M2).
- **Cache delle frasi fisse** (velocità, decisione dell'operatore via M1): `FATTA` — `sintesi()` in `modules/voice/server.py`: «Dimmi.», «Va bene.», «Non ho capito bene…», «Il resto è a schermo.» ecc. sintetizzate una volta per processo e voce, poi dalla memoria (niente attesa né costo ElevenLabs); solo testi fissi del codice, mai testo del modello o dell'operatore.
- **Riserve BASSE della #354**: `FATTE` — test della pulizia con «in_coda» (bot #354 V-1), `_finiti_jobs` azzerato a inizio richiesta (R-711-3-M2), lambda → funzione, parentesi esplicite nella condizione del segno (ve #354 V-3).
- Review #715-M2 APPROVATO CON RISERVE (R-715-1-M2 COSMETICA, chiusa in e97de50).
- **Bot #356 su 6872080 (BOCCIATO)**: V-1 MEDIA `FATTA` (riga 5 di `reports/ultimo_report.md` diceva ancora «nessuna decisione»: ora «decide l'operatore»), V-2 BASSA `FATTA` (§3 rigenerato con `git log` reale), V-3 BASSA `FATTA` (test che le risposte vere passano dalla cache, 3 mutanti uccisi). Review #721-M2 APPROVATO.
- **Riserve della verifica esterna #356 (68a9c8d)**: V-1 BASSA `FATTA` (test `test_f32c_finiti_jobs_azzerati_a_ogni_richiesta`, mutante ucciso), V-2 COSMETICA `FATTA` (righe vuote), V-3 BASSA `FATTA` (§3 e §6 aggiornati); V-4 BASSA (cache utile solo nei pezzi, `api_key` fuori dalla chiave) registrata. Review #719-M2 APPROVATO.
- **Merge di main (#355 di Mani) nel branch** per togliere il conflitto (MEDIA della verifica esterna sulla #356): `FATTO` (2580889), review #716-M2 APPROVATO; conflitti solo su report e memoria.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  5 ++
 modules/voice/server.py            | 44 +++++++++++++++++++++----
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_sottofondo.py      | 25 +++++++++++----
 tests/test_unit_voice_server.py    | 96 +++++++++++++++++++++++++++++++++++++-
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main b827447 (merge della #355, entrato nel branch col merge 2580889).

## §3 GIT LOG --ONELINE (sessione)

```
a9b220c test(voce): le risposte vere passano dalla cache delle frasi fisse (bot #356 V-3)
31fec47 chore(revisore): memoria review #721 — APPROVATO
6872080 docs(voce): report con le riserve della verifica esterna #356 chiuse (chat M2)
e97de50 test(voce): azzeramento di _finiti_jobs a ogni richiesta provato; righe vuote tolte (ve #356 V-1/V-2)
d722506 chore(revisore): memoria review #719 — APPROVATO
68a9c8d docs(voce): #356 resta per l'operatore; tolta la regola notturna scritta dall'agente (allineamento con M1, chat M2)
8629e79 docs(voce): report dopo il merge di main (#355) e regola di merge notturna R11 (chat M2)
2580889 Merge origin/main (#355, voce via Telegram fetta 2) in feat/voce-v12-m2
84b88f8 docs(voce): report di fine task — cache delle frasi fisse; PR #354 mergiata (chat M2)
b97a570 perf(voce): cache della sintesi per le frasi fisse del server voce; riserve BASSE della #354 (in_coda, _finiti_jobs, parentesi, lambda) (decisione dell'operatore via M1)
9301c2f chore(revisore): memoria review #715 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #715-M2 sul commit b97a570 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #715-M2: diff staged su feat/voce-v12-m2 (base fa6b1f3), 3 file, +106/−15. Ho letto CLAUDE.md (§5, §8, §9 e roadmap), lo stato del progetto e la mia memoria. Ho rieseguito io i test: test_unit_voice_server.py, test_unit_sottofondo.py e test_unit_telegram_voce.py interi danno **243 passed**.

Elementi del diff esaminati:
- `modules/voice/server.py:314` — `_FRASI_FISSE` è un insieme bloccato dei soli testi costanti del codice (Dimmi., Va bene., Per farlo ripetimelo…, Non ho capito…, uso di «forte», C'è altro…, Il resto è a schermo.). Rischio esaminato: privacy, cioè che in cache finisca testo del modello o dell'operatore. La cache si usa solo se la frase è uguale per intero a una costante. Le frasi dei compiti finiti e il parlato unito con `" ".join(...)` in pratica non coincidono mai con una costante, quindi vanno sempre a ElevenLabs. Esito: **ok**.
- `modules/voice/server.py:322` — `sintesi()`. La chiave è (funzione, voce, frase). Un audio vuoto non entra in cache. A 32 voci la cache si svuota. Gli errori `ElevenLabsTTSError` passano al chiamante, che li gestisce come prima (log.warning e errore_voce, §9 invariato). Rischi esaminati:
  - cambio di voce: la voce è nella chiave, quindi ok;
  - modello e impostazioni TTS: in modules/voice/tts.py sono costanti di modulo, non lette dall'ambiente a ogni chiamata, quindi non possono cambiare a server acceso. Ok;
  - api_key fuori dalla chiave: un MP3 già sintetizzato resta valido anche con un'altra chiave. Ok;
  - concorrenza: `HTTPServer` è a un solo thread (`modules/voice/server.py:1252`) e nessun altro punto del codice chiama `sintesi`. Ok.
  Esito: **ok**.
- `modules/voice/server.py:506` — `_finiti_jobs = None` a inizio `do_POST`, così su una connessione keep-alive non restano i compiti della richiesta precedente. Coerente con `_segna_finiti_letti` (:731-732). Esito: **ok**.
- `modules/voice/server.py:819` — la lambda `resto` diventa una funzione con type hint. Il comportamento è identico. Esito: **ok**.
- `modules/voice/server.py:888` — parentesi esplicite nella condizione. L'ordine di valutazione è lo stesso di prima, quindi nessun cambio di comportamento. Esito: **ok**.
- `tests/test_unit_voice_server.py:1988` — il test controlla tre cose: una sola sintesi per frase fissa e voce, il testo libero mai in cache, l'audio vuoto mai in cache. Gli altri due test coprono l'errore (:2011) e il tetto (:2025). Rischio esaminato: test che passano anche col codice rotto. Ho ragionato sui mutanti senza eseguirli: senza il controllo `if audio:` le chiamate per RISPOSTA_PAUSA sarebbero una sola invece di due, e senza la voce nella chiave mancherebbe la chiamata con v2. In entrambi i casi l'assert sulla lista `chiamate` fallirebbe. Esito: **ok**.
- `tests/test_unit_sottofondo.py:826` — il test della pulizia ora gira sia con «in_corso» sia con «in_coda», nei due casi «col posto in coda» e «senza posto» (chiude il V-1 del bot sulla #354). Esito: **ok**.

Riserve:
- **R-715-1-M2 (COSMETICA)**: la fetta dichiara di aver tolto le righe vuote in più (E303), ma ne aggiunge 3 nuove prima dei test nuovi. Si trovano in `tests/test_unit_voice_server.py:1983` (righe 1983-1985, prima di «# ---- Velocità…») e in `tests/test_unit_sottofondo.py:823` (righe 823-825, prima del decoratore a :826). Va tolta una riga vuota in ciascun file.

Cosa non ho verificato:
- La latenza reale guadagnata e il comportamento con ElevenLabs vero: richiedono la chiave e la rete, i test usano mock.
- Lo stile con flake8 o pycodestyle: non sono installati nell'ambiente. Ho controllato le righe vuote a mano con `cat -A`.
- L'effetto della cache sulla memoria del processo: è trascurabile per costruzione (al massimo 32 MP3 brevi) e non l'ho misurato.

Memoria: in coda a /home/user/Gas/.claude/agents/memoria_revisore.md ho aggiunto la riga #715-M2 e una lezione (una pulizia di stile dichiarata va controllata anche sulle righe aggiunte). Le ho committate da sole con lo script (9301c2f, «chore(revisore): memoria review #715 — APPROVATO CON RISERVE»). L'index del diff sotto review è rimasto intatto: ancora 3 file, +106/−15.

File rilevanti: /home/user/Gas/modules/voice/server.py, /home/user/Gas/tests/test_unit_voice_server.py, /home/user/Gas/tests/test_unit_sottofondo.py, /home/user/Gas/.claude/agents/memoria_revisore.md

Review #716-M2 sul merge 2580889 (verdetto integrale):

## VERDETTO: APPROVATO

Review #716-M2: merge in corso di origin/main b827447 (PR #355 della chat Mani, voce via Telegram fetta 2) nel branch feat/voce-v12-m2 (HEAD 84b88f8, PR #356). Base comune fa6b1f3.

Ho letto prima CLAUDE.md (dato nel contesto), la parte utile di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

**Cosa ho controllato nel diff**
- `modules/voice/server.py:322`: è la nuova `sintesi()` di M2, con la cache delle frasi fisse. Rischio esaminato: che il codice di Telegram arrivato dal lato main la usi o dipenda da `synthesize_speech` dentro server.py, che M2 ha sostituito. Esito: ok. `modules/telegram/bot.py:1011` importa `synthesize_speech` da `modules/voice/tts.py`, che M2 non tocca. Le 6 righe tolte da M2 in server.py stanno tutte dentro VoiceHandler: 3 chiamate a synthesize_speech, la lambda e la condizione del segno.
- `modules/voice/server.py:339`: `parte_parlata`, importata da `modules/telegram/bot.py:1010`. Rischio esaminato: firma o comportamento cambiati da M2 dopo la base. Esito: ok. Il diff da fa6b1f3 a HEAD contiene solo gli hunk a :307 (aggiunta pura) e da :503 in poi (VoiceHandler). Anche `cervello_voce` (`modules/voice/server.py:382`) e `_USO_FORTE_PARLATO` (`modules/voice/server.py:111`), usati da `modules/telegram/bot.py:958`, sono invariati.
- `tests/test_unit_voice_server.py:1` e `tests/test_unit_sottofondo.py:1`: rischio esaminato: che il merge abbia alterato i test di M2. Esito: ok. Il blob nell'index è identico a HEAD (710bfac e 0b92db9), e lo stesso vale per `modules/sottofondo/__init__.py` (c7b2b63).
- Lato main: rischio esaminato: contenuto diverso da MERGE_HEAD. Esito: ok. Nell'index i blob di `modules/telegram/bot.py` (c372b6f), `tests/test_unit_telegram_voce.py` (eff6818) e `tests/test_unit_voce_ascolto.py` (665c65b) sono identici a b827447.
- Report: rischio esaminato: righe perse nei file in conflitto. Esito: ok. `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md` sono identici a HEAD. `.claude/agents/memoria_revisore.md` e `reports/stato_progetto.md` sono l'unione dei due lati: le righe aggiunte da HEAD sono 2 e 1, da main 4 e 8, e nessuna manca.
- Pulizia del merge: `git ls-files -u` è vuoto, nessun marcatore di conflitto, `git diff --cached --check` pulito, nessuna modifica fuori dall'index.
- Test sulla copia dell'index (checkout-index nello scratchpad, niente stash): telegram_voce + voce_ascolto + voice_server + sottofondo, 558 passed.

**Cosa NON ho verificato**
- Il comportamento dal vivo di sendVoice e di ElevenLabs. Non si riproduce in dev, e le riserve R-717-3 e R-717-4 della chat Mani restano aperte.
- La suite completa del motore: ho eseguito solo i 4 file toccati dai due lati.

**Memoria**
- Ho aggiunto la riga `#716-M2 — 2026-11-09 — APPROVATO — …` in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, senza lezioni nuove.
- Ho fatto solo `git add .claude/agents/memoria_revisore.md`. Come chiesto, non ho lanciato commit_memoria_revisore.sh, perché il merge è in corso: la memoria entra col commit di merge.

Review #719-M2 sul commit e97de50 (verdetto integrale):

## VERDETTO: APPROVATO

In breve: il nuovo test riconosce davvero il difetto (se si toglie la riga di azzeramento fallisce, con la riga passa). Le due righe vuote tolte sono solo cosmetiche. Il diff tocca solo i test, quindi non indebolisce nessun guardrail.

Ho letto prima CLAUDE.md (già in contesto; il diff non tocca lo slicing della history né la simulazione dei tool), le parti di reports/stato_progetto.md sulla #356 e la coda di .claude/agents/memoria_revisore.md.

Cosa ho esaminato:
- `tests/test_unit_voice_server.py:1985` — il nuovo test `test_f32c_finiti_jobs_azzerati_a_ogni_richiesta`. Mette in `_finiti_jobs` un compito "rimasto" da una richiesta precedente sulla stessa connessione, chiama `do_POST` su un path inesistente (prende il ramo 404, `modules/voice/server.py:524`) e poi `_segna_finiti_letti()`. Controlla che `segna_letti`, sostituito nel test, non venga chiamato.
  - Rischio esaminato: il test potrebbe passare per caso, perché `_segna_finiti_letti` (`modules/voice/server.py:728`) intercetta le eccezioni e una lista vuota si otterrebbe anche se la funzione fallisse in silenzio.
  - Ho rifatto il mutante su una copia dell'index (scratchpad, via `git checkout-index`): con la riga 506 il test passa, senza fallisce. Quindi il test distingue i due casi.
  - Esito: ok.
- `modules/voice/server.py:506` (contesto, non toccato) — l'azzeramento `self._finiti_jobs = None` a inizio `do_POST`. È il comportamento che il test protegge e chiude la V-1 BASSA della verifica esterna #356. Esito: ok.
- `tests/test_unit_sottofondo.py:826` e `tests/test_unit_voice_server.py:1985` — tolte le righe vuote di troppo prima della funzione successiva (R-715-1-M2 COSMETICA). `git diff --cached --check` è pulito. Esito: ok.

Esecuzione: `pytest tests/test_unit_voice_server.py tests/test_unit_sottofondo.py -k "not browser"` dà 192 passed e 21 deselected. Tu dichiari 198 passed: la differenza dipende quasi certamente dal filtro diverso con cui escludi i test browser, non da test che falliscono. Non è una riserva. Nel report scrivi il comando esatto che hai usato.

Cosa NON ho verificato:
- Il caso keep-alive reale, cioè due richieste HTTP sulla stessa connessione socket con un server vivo. Il test lo simula chiamando direttamente `do_POST` su un handler costruito con `__new__`, e non l'ho riprodotto end-to-end.
- I test browser esclusi dal filtro, che il diff non tocca.

Memoria: ho scritto la riga contatore `#719-M2 — 2026-11-09 — APPROVATO — …` (nessuna lezione nuova) e l'ho committata con lo script, commit d722506. Il diff staged dei due test è rimasto intatto nell'index.

File:
- /home/user/Gas/tests/test_unit_voice_server.py
- /home/user/Gas/tests/test_unit_sottofondo.py
- /home/user/Gas/modules/voice/server.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

Review #721-M2 sul commit a9b220c (verdetto integrale):

## VERDETTO: APPROVATO

Review #721-M2. Diff staged su feat/voce-v12-m2 (PR #356): solo /home/user/Gas/tests/test_unit_voice_server.py, 30 righe aggiunte. Chiude la V-3 BASSA del bot.

Ho letto prima: CLAUDE.md (sezione 5), reports/stato_progetto.md (letto in parte, con grep) e la memoria del revisore.

Cosa ho controllato nel diff e nel codice intorno:
- `tests/test_unit_voice_server.py:2027` — test parametrico sui formati «audio+testo+pezzi» e «audio+testo». Usa il server vero tramite `_voce_a_pezzi`, trascrive «Gas.» e controlla che «Dimmi.» finisca nella cache. Rischio guardato: il test potrebbe passare anche senza `sintesi()`. Non succede: la cache viene sostituita con un dizionario nuovo, quindi resta vuota se la sintesi non passa di lì, e l'assert sulla frase in cache fallisce. Il controllo sul contenuto (`k[2]`) va bene, perché la chiave contiene la funzione di sintesi finta, diversa a ogni patch. Esito: ok.
- `tests/test_unit_voice_server.py:2039` — test sull'MP3 diretto: crea l'handler con `__new__`, mette `_tempi` e `_finiti_jobs` a None e chiama `_send_audio` due volte. Rischio guardato: attributi mancanti che farebbero crashare il test. `_segna` (`modules/voice/server.py:438`) non fa niente se `_tempi` è None, e `_segna_finiti_letti` (`modules/voice/server.py:728`) usa getattr ed esce subito senza job. La chiave ELEVENLABS è impostata con monkeypatch, quindi non si finisce nel ramo che risponde 503. Esito: ok.
- Contesto `modules/voice/server.py:322` — `sintesi()` mette in cache solo le frasi fisse. «Dimmi.» lo è, altrimenti il test non passerebbe senza mutanti. Esito: ok.
- Mutanti rifatti da me: ho sostituito `sintesi(` con `synthesize_speech(`, un punto alla volta, a `modules/voice/server.py:833`, `modules/voice/server.py:876` e `modules/voice/server.py:916`. Ogni volta un test fallisce (1 failed). Dopo ho ripristinato il file sorgente: lo staged è invariato e il working tree pulito su server.py.
- Comando dichiarato rieseguito: `pytest -q tests/test_unit_voice_server.py tests/test_unit_sottofondo.py -k "not conversazione_nel_browser"` → 201 passed, 15 deselected. `git diff --staged --check` è pulito.

Nessun antipattern della sezione 5 (niente slicing della history, niente simulazione di tool: lo stub della sintesi nei test è un mock esterno, va bene). Il motore non è toccato.

Cosa NON ho verificato: il comportamento con ElevenLabs vero e il caching con un voice_id diverso da quello di default. Il test sull'MP3 non fissa ELEVENLABS_VOICE_ID, ma il risultato non dipende dalla voce. ElevenLabs vero non si può provare in dev, servono la chiave e la rete. Non ho rifatto la suite completa del kernel: il diff tocca solo questo file di test.

Memoria: aggiunta la riga #721-M2 in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script (commit 31fec47, «chore(revisore): memoria review #721 — APPROVATO»). Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py`: 3 nuovi (cache: una sola sintesi per frase fissa e voce, testo libero mai in cache, audio vuoto mai in cache; errore non in cache; tetto della cache). `tests/test_unit_sottofondo.py`: pulizia parametrica su «in_corso»/«in_coda», con e senza posto. Suite voce server + sottofondo + telegram_voce: 243 passed (intere). `gas.py` non toccato. In più `test_f32c_finiti_jobs_azzerati_a_ogni_richiesta` (ve #356 V-1). Comando dopo e97de50: `pytest -q tests/test_unit_voice_server.py tests/test_unit_sottofondo.py -k "not conversazione_nel_browser"` → 198 passed, 15 deselected. Dopo a9b220c (+3 test della cache sulle risposte): 201 passed, 15 deselected.

## §6 STATO CI

Head 6872080: handoff-check success; verifica-bot failure (BOCCIATO, MEDIA sul report, corretta qui); unit-suite in corso alla scrittura. Nuovo head: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Ve #356 V-4 BASSA: la cache vale solo nelle risposte a pezzi (nel formato unico il parlato unito non è una frase fissa); `api_key` non nella chiave della cache.
- R-713-1-M2 BASSA (in parte): test del client chiuso nei pezzi con schermo e dell'ordine invio→segno.
- R-713-2-M2 BASSA: attivo.json illeggibile + durata > giorni → compito vivo senza file.
- Restano: R-709-1/2-M2, R-708-1-M2, R-706-1-M2, R-701-3-M2, R-703-2-M2, R-696-1-M2.
- Non verificato in dev: guadagno di latenza reale con ElevenLabs.
