# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-08 — chat Mani: voce via Telegram, fetta 1 (vocale → trascrizione → risposta in testo; R8, opzione B)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #353 (https://github.com/Gasss23/Gas/pull/353): SÌ dell'operatore del 2026-11-09 via M1, con le riserve. Numero e URL dalla risposta dello strumento GitHub `create_pull_request`.
2. V-2 della verifica esterna #353 (regola dei modelli per i vocali senza «forte»): l'operatore ha scelto l'opzione A in chat con M1 la sera del 7/11. M1 gli ha chiesto di confermarla con un suo commento sulla #353.
3. Fetta 2: risposta vocale SOLO quando l'operatore manda un vocale (opzione A, decisione del 2026-11-09 via M1).

---

## §1 SCOPE & ESITO FETTE

- **PR #351 (fetta 45)**: `FATTA` — mergiata (9bfafdb) col sì dell'operatore.
- **Voce via Telegram, fetta 1 (vocale → testo)**: `FATTA` — review #711/#712, unione #715.
- **Proposta Telegram, decisioni e correzioni del bot #348**: `FATTA`.
- **Voce via Telegram, fetta 2 (risposta in voce)**: `DEFERITA — prossima fetta. Decisione presa: risposta vocale solo dopo un vocale`.
- **Merge di main con la PR #352 di M2**: `FATTA` — review #716 APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 .github/workflows/ci.yml           |   3 ++-
 modules/telegram/bot.py            | 178 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------
 reports/diff_sessione.md           |  16 +++++++++-------
 reports/proposta_voce_telegram.md  |  11 ++++++++---
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  27 ++++++++++++++++-----------
 tests/test_unit_telegram_voce.py   | 241 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main 3084979 (dopo il merge della PR #352).

## §3 GIT LOG --ONELINE (sessione)

```
f24dd28 Merge origin/main (PR #352 di M2) nella PR #353 — review #716 APPROVATO
a08931f docs(fine-task): voce via Telegram fetta 1 chat Mani — review #711/#712/#715, PR #351 mergiata
a5b2d66 Merge voce via Telegram fetta 1 (vocale → testo, R8 opzione B) e decisioni nella proposta — review #711/#712, unione #715 APPROVATO
1684236 feat(telegram): voce via Telegram, fetta 1 — vocale → trascrizione → risposta in testo (R8, opzione B) — review #711/#712
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push. La fetta è stata scritta e revisionata nel worktree locale /tmp/claude-0/wt46 (base f4ece4e), poi unita a main: come verificato nella review #715, main non ha toccato bot.py e ci.yml.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #711, verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #711 (chat Mani). Oggetto: il diff STAGED nel worktree /tmp/claude-0/wt46 (branch mani/telegram1, base f4ece4e). È la voce via Telegram, fetta 1 (roadmap R8, opzione B).

Prima della review ho letto CLAUDE.md (sez. 2, 5, 8 e 9), reports/stato_progetto.md (letto in parte) e .claude/agents/memoria_revisore.md (le ultime voci, fino a #708-M2). L'index l'ho copiato in scratch (/tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/index.bak e staged.diff) e alla fine ho controllato con cmp che il diff staged non sia cambiato. Non ho usato stash.

**Elementi del diff esaminati**
- `modules/telegram/bot.py:815` — controlla la chat autorizzata prima di typing, getFile, download e Groq.
  - Rischio esaminato: una chat estranea che fa spendere Groq o fa scaricare file.
  - Esito: ok. Il test `test_chat_non_autorizzata_niente_download_ne_trascrizione` controlla che non parta nessuna chiamata.
- `modules/telegram/bot.py:811` — `vocale` vale solo se l'update è `message` (un vocale modificato viene ignorato).
  - Rischio esaminato: rielaborare un vocale già gestito.
  - Esito: ok. Per i testi modificati il comportamento resta quello di prima.
- `modules/telegram/bot.py:103` — il percorso di getFile deve essere una stringa non vuota e senza `..`.
  - `modules/telegram/bot.py:110` — l'URL si costruisce come prefisso fisso `/file/bot<token>` più il percorso.
  - Rischio esaminato: path traversal e cambio di host.
  - Esito: ok. Il prefisso con l'host è fisso, quindi `@`, `?` o `#` nel percorso non possono portare il download fuori da api.telegram.org.
- `modules/telegram/bot.py:113` — `r.read(VOCALE_MAX_BYTES + 1)` più il controllo successivo. Insieme a `modules/telegram/bot.py:107` (file_size di getFile) e `modules/telegram/bot.py:133` (file_size del messaggio).
  - Rischio esaminato: memoria e Groq.
  - Esito: ok. In memoria finiscono al massimo circa 2 MB.
- `modules/telegram/bot.py:130` — la durata deve essere un intero e al massimo 60 s, prima del download.
  - Esito: ok, con la riserva R-711-2 sotto. Nota cosmetica: `True` passa come int, ma Telegram non lo manda mai.
- Token e log in `modules/telegram/bot.py:96-120`: sul download si logga solo `type(e).__name__`.
  - In `_tg_post` (`modules/telegram/bot.py:62`, codice non toccato) si loggano metodo ed `e.reason`, mai l'URL.
  - Per Groq si logga lo status, mai il body. Per una trascrizione incerta si logga `e.motivo`, mai il parlato.
  - Esito: ok.
- `modules/telegram/bot.py:872` — `_risposta_del_turno` è il corpo di prima spostato riga per riga (stesso try/except, stessi tetti di 200 e 120 caratteri, stesso «(nessuna risposta)»).
  - `modules/telegram/bot.py:866` lo chiama dopo `_send_typing` come prima.
  - Esito: ok. I messaggi di testo restano identici, e lo prova `test_i_messaggi_di_testo_restano_come_prima`.
- `modules/telegram/bot.py:897` — `_gestisci_parlato` passa il testo a `cervello_voce(…, parlato=True)` di modules/voice/server.py. Con esito «uso» non parte nessun turno (fail-closed). /clear e /notte non vengono interpretati.
  - Rischio esaminato: import pigro e cicli.
  - Esito: ok. Il modulo usa solo stdlib, non importa il bot (nessun ciclo) e l'import costa circa 6 ms.
  - Il turno parte senza voce=True, come chiesto. Le firme passano per lo stesso `kernel.run_turn` dei testi, quindi i bottoni restano invariati.
- `tests/test_unit_telegram_voce.py:82` e `tests/test_unit_telegram_voce.py:95` — test della chat non autorizzata e dei tetti di durata (61, 600, None, "5").
  - Esito: ok. In totale 25 passed, rieseguiti da me.
- `.github/workflows/ci.yml:127` — il nuovo file è aggiunto alla voice suite, e quel passo ha `if: always()`.
  - Esito: ok.

**Prove che ho rieseguito**
- tests/test_unit_telegram_voce.py: 25 passed.
- notte, avvisa_operatore e sottofondo (usano il bot): 308 passed.
- tests/test_unit_kernel.py: 1099 PASS, 1 FAIL. Il fallito è T31g (vector store, problema dell'ambiente), uguale a quanto dichiarato.

§7 (round-trip agentico): il kernel non è toccato e il turno usa `run_turn` così com'è. Non serve un round-trip nuovo, basta il test del bot con un kernel finto.

§9: ogni errore diventa un messaggio all'operatore, e c'è comunque il try esterno di `_handle_update`.

**Riserve (tutte BASSE)**
- R-711-1 BASSA — regola dei modelli (CLAUDE.md §2):
  - L'audio va a Groq e il turno non «forte» va alla cascata che include i gratuiti, esattamente come i testi Telegram di oggi. Quindi non è una regressione.
  - Però a voce è più facile dettare dati di clienti.
  - Inoltre GAS_VOCE_FORTE ora vale anche per i vocali Telegram: va detto all'operatore nel report.
- R-711-2 BASSA — `modules/telegram/bot.py:131`: se la durata manca o non è intera, la risposta è «Vocale troppo lungo», un messaggio fuorviante.
- R-711-3 BASSA — non c'è un tetto orario sui vocali:
  - Se la chat autorizzata è un gruppo, chiunque ci sia dentro può far spendere Groq.
  - Il server voce invece ha GAS_VOICE_MAX_TURNI_ORA.
  - Il polling resta bloccato fino a circa 60 s di rete prima del turno.
- R-711-4 BASSA — `modules/telegram/bot.py:901`: se l'import di modules.voice.server fallisce, c'è solo il log del try esterno. L'operatore ha visto «sta scrivendo…» e poi non riceve nessuna risposta.

**Rischi esplicitamente esclusi**
- Non ho provato un vero vocale Telegram né il vero Groq Whisper con OGG/Opus (.oga dichiarato come vocale.ogg): non c'è rete, né token, né bot in dev.
- Non ho rieseguito i 6 mutanti dichiarati. Ho però controllato che i test corrispondenti esistano e verifichino il punto giusto.
- Non ho verificato il comportamento sulla VPS o sul Mac.

**Memoria**
- Ho aggiunto in coda a /tmp/claude-0/wt46/.claude/agents/memoria_revisore.md la riga «#711 — 2026-11-07 — APPROVATO CON RISERVE — …» e una lezione nuova: quando una funzione di un canale viene riusata da un altro, va verificato e dichiarato quali variabili d'ambiente e tetti seguono il riuso.
- Il file non è committato, come chiesto. Non ho eseguito commit_memoria_revisore.sh.
- Nella memoria di questo worktree non ci sono righe oltre #708-M2, quindi ho usato #711 come indicato.

Review #712 (ri-review), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #712 (chat Mani): ri-controllo della #711 sul diff STAGED in /tmp/claude-0/wt46 (branch mani/telegram1). Le correzioni di R-711-2, R-711-3 e R-711-4 sono giuste. Restano solo riserve basse o cosmetiche.

Prima ho copiato l'index in /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/index712.bak e il diff in staged712.diff, senza stash. Con cmp ho controllato che lo staged sia rimasto uguale fino alla fine.

**Elementi del diff esaminati**
- `modules/telegram/bot.py:155` — se la durata manca, non è un intero o è un bool, la risposta è «✗ Vocale senza durata: non lo trascrivo.». Il messaggio «troppo lungo» resta solo sopra i 60 s (`modules/telegram/bot.py:157`).
  - Rischio esaminato: un bool che passa come int, o un messaggio sbagliato all'operatore.
  - Esito: ok. Il test è parametrizzato e ogni caso controlla il messaggio atteso.
- `modules/telegram/bot.py:136` — `_posto_per_un_vocale`: a ogni vocale toglie dalla lista quelli più vecchi di 3600 s (`time.monotonic`), rifiuta se ce ne sono già N, altrimenti segna subito il vocale.
  - Prestazioni: la lista non supera mai i vocali accettati nell'ultima ora (al massimo N), quindi il costo per vocale è trascurabile.
  - Thread: `_handle_update` ha un solo chiamante, il loop di polling (`modules/telegram/bot.py:542`). Il ThreadPoolExecutor a `modules/telegram/bot.py:353` serve solo all'invio a più chat e non tocca il contatore, quindi non ci sono corse.
  - Esito: ok.
- `modules/telegram/bot.py:127` — `_vocali_ora`: un valore non numerico, 0 o negativo diventa il predefinito 30 (test parametrizzato su "abc", "0" e "-3").
  - Esito: ok, con la nota cosmetica R-712-2.
- `modules/telegram/bot.py:165` — il tetto si controlla dopo la verifica di GROQ_API_KEY e prima del download. Un vocale senza chiave non consuma il posto.
  - Rischio esaminato: un vocale contato e poi scartato.
  - Il posto si consuma anche se il download fallisce, se Groq dà errore o se la trascrizione è incerta. Negli ultimi due casi Groq è stato davvero chiamato, quindi contarli è giusto. Il download fallito invece non costa nulla eppure consuma il posto: è una scelta prudente (R-712-1).
  - Esito: riserva bassa.
- `tests/test_unit_telegram_voce.py:71` (fixture) — il fixture sostituisce `_vocali_recenti` con una lista nuova tramite `monkeypatch.setattr`, ripristinata alla fine. `_posto_per_un_vocale` modifica la lista sul posto (`[:]=`) cercandola nel modulo a ogni chiamata, quindi usa quella del test.
  - Nessun'altra suite manda vocali a `_handle_update` (il T48 del kernel usa solo testo).
  - Due esecuzioni di fila nello stesso processo: 31 passed.
  - Esito: ok.
- `tests/test_unit_telegram_voce.py:212` — `test_tetto_di_vocali_all_ora`: con il tempo finto, il terzo vocale viene rifiutato senza download; passata l'ora (+3601 s) si riparte. Esito: ok.
- `modules/telegram/bot.py:932` — R-711-4: l'import di modules.voice.server è dentro un try. Se fallisce, l'operatore riceve l'eco e «✗ Errore interno: non posso gestire i vocali.», e nel log va solo `type(e).__name__`. Esito: ok.
- `modules/telegram/bot.py:895` — il percorso dei testi è sempre `_send_typing` seguito da `_risposta_del_turno`, invariato rispetto alla #711. Esito: ok.

**Prove che ho rieseguito**
- tests/test_unit_telegram_voce.py: 31 passed.
- notte, avvisa_operatore e sottofondo: 308 passed.
- tests/test_unit_kernel.py: 1099 PASS, 1 FAIL. Il fallito è T31g (vector store, problema dell'ambiente), già visto nella #711.

**Riserve**
- R-712-1 BASSA — un vocale il cui download fallisce consuma lo stesso un posto dell'ora, anche se Groq non viene chiamato. È una scelta prudente: va dichiarata all'operatore, non corretta.
- R-712-2 COSMETICA — `modules/telegram/bot.py:141-142`: quando il tetto è pieno `_vocali_ora()` viene chiamata due volte. Con un valore non numerico il warning compare due volte nel log.
- R-712-3 BASSA — il contatore vive solo nella memoria del processo: un riavvio del bot lo azzera. Per il tetto dei costi è accettabile.
- R-711-1 BASSA resta aperta: va dichiarata all'operatore nel report. Due punti:
  - GAS_VOCE_FORTE vale anche per i vocali Telegram.
  - I turni non «forte» vanno alla cascata che include i gratuiti, come i testi (CLAUDE.md §2).

**Rischi esplicitamente esclusi**
- Non ho rieseguito i 4 mutanti nuovi dichiarati. Ho però controllato che i test corrispondenti esistano e verifichino il punto giusto.
- Non ho provato un vero vocale Telegram né il vero Groq: non c'è rete, né token, né bot in dev.
- Non ho verificato come si comporta il contatore su un bot attivo per molte ore sulla VPS.

**Memoria**
Ho aggiunto in coda a /tmp/claude-0/wt46/.claude/agents/memoria_revisore.md la riga «#712 — 2026-11-07 — APPROVATO CON RISERVE — …». Il file non è committato, come chiesto. Non ho aggiunto lezioni nuove.

Review #715 (unione con main dopo la #351), verdetto integrale:

## VERDETTO: APPROVATO

Review #715 (chat Mani). Oggetto: il merge in stage, non committato, di mani/telegram1 (1684236, voce via Telegram fetta 1) in claude/peaceful-lovelace-0w2b7q, con HEAD 9bfafdb uguale a origin/main. Nello stage c'è anche la modifica di soli documenti a reports/proposta_voce_telegram.md.

Letture fatte prima della review: CLAUDE.md (sez. 5, 8, 10), reports/stato_progetto.md (letto con Grep, solo le voci su Telegram e voce), memoria_revisore.md (coda #711–#714). Il numero più alto in memoria era #714, quindi questa è la #715.

**Elementi del diff esaminati**
- `modules/telegram/bot.py:840` — prende il vocale solo da `upd["message"]`, cioè solo dai messaggi nuovi: un vocale «modificato» viene ignorato. Rischio esaminato: un messaggio modificato rimette in moto download e trascrizione. Esito: ok (lo copre il test `tests/test_unit_telegram_voce.py:91`).
- `modules/telegram/bot.py:844` — controlla `chat_id not in allowed` e fa `return` PRIMA del ramo del vocale (`modules/telegram/bot.py:848`, `if not text:` → `testo_da_vocale`). Rischio esaminato: una chat non autorizzata fa scaricare e trascrivere l'audio, quindi spende Groq. Esito: ok. La proposta corretta («DOPO il controllo delle chat autorizzate») corrisponde al codice.
- `modules/telegram/bot.py:136-145` — tetto orario dei vocali (`GAS_TELEGRAM_VOCALI_ORA`, 30 se non impostato, a `modules/telegram/bot.py:60`), controllato prima del download e dopo la verifica della chiave Groq (`modules/telegram/bot.py:165`). Rischio esaminato: la proposta dichiara «30 vocali all'ora» ma il codice fa altro. Esito: ok, corrispondono.
- `tests/test_unit_telegram_voce.py:84` — chat non autorizzata: zero chiamate, zero download, zero trascrizioni, zero turni. Rischio esaminato: il controllo sull'ordine non è coperto da un test. Esito: ok, il test passa sulla copia dell'index.
- `.github/workflows/ci.yml:127` — il passo «voice suite» aggiunge `tests/test_unit_telegram_voce.py` ai 5 file che c'erano già. Rischio esaminato: un file citato manca su main, e il passo fallisce o non raccoglie test. Esito: ok. Tutti e 6 i file esistono nell'index (`test_unit_voice_server`, `_stt`, `_tts`, `_contesto`, `_prova_voci`, `test_unit_telegram_voce`), e la suite intera dà 337 passed sulla copia dell'index.

**Controlli richiesti**
1. Identità dei file: nell'index, `modules/telegram/bot.py` (05ae407), `tests/test_unit_telegram_voce.py` (56cdaea) e `.github/workflows/ci.yml` (9f5dac1) hanno lo stesso blob di MERGE_HEAD/mani/telegram1. A HEAD 9bfafdb, bot.py e ci.yml hanno lo stesso blob di f4ece4e (188cba3 e d36606a), quindi main non li ha toccati. Il file di test non esiste né a f4ece4e né a HEAD. Il merge-base è f4ece4e. Il diff di mani/telegram1 rispetto a f4ece4e tocca solo questi 3 file più la memoria: è lo stesso diff già revisionato in #711/#712. Nel working tree i tre file sono uguali all'index.
2. Memoria: HEAD ha 1345 righe, l'index 1348. Le 3 righe in più sono #711, la lezione del 2026-11-07 e #712. Righe di HEAD perse: 0. Righe di mani/telegram1 perse: 0.
3. Marcatori: nessun marcatore di conflitto nelle righe aggiunte, `git ls-files -u` vuoto. `git diff --cached --check` segnala solo «new blank line at EOF» in tests/test_unit_telegram_voce.py:241. È cosmetico e c'era già nel diff di #711/#712: lo metto come nota, non come riserva.
4. Proposta e codice: il ramo del vocale viene dopo il controllo della chat autorizzata (V-3). `sendAudio` non compare in nessun file .py, quindi è giusta la frase «Gas oggi non lo usa ancora» (V-1). Le decisioni del 7 e 8 novembre scritte in cima corrispondono al codice: `GAS_VOCE_FORTE` è riusato tramite `_gestisci_parlato` e il tetto è 30 all'ora (V-2). Il file è solo documento, fuori dal perimetro del motore.
5. Test sulla copia dell'index (`git checkout-index -a` nello scratchpad, senza stash):
   - telegram_voce + notte + avvisa_operatore: **269 passed**;
   - voice suite di ci.yml completa: **337 passed** in 5m17s.

**Antipattern (Wall of Shame)**: nel diff non c'è slicing della history né output dei tool simulato. Gli errori dei provider passano da `testo_da_vocale`, che restituisce sempre un messaggio all'operatore e non solleva eccezioni (fail-safe §9, già verificato in #711).

**Rischi esplicitamente esclusi**
- Il comportamento reale con Telegram, Groq ed ElevenLabs veri non l'ho verificato: i test usano servizi finti e qui non ci sono token.
- La suite del kernel completa (`gas.py`) non l'ho rieseguita: il merge non tocca il kernel. In #711/#712 dava 1099 PASS / 1 FAIL T31g, dovuto all'ambiente.
- I test della pagina nel browser con `GAS_TEST_BROWSER_OBBLIGATORIO=1` non li ho forzati: qui non c'è Playwright/Chromium, quindi il loro esito vero lo dà la CI.

**Riserve ancora aperte da #711/#712** (non nuove, sono di sostanza e restano da tracciare in stato_progetto.md):
- R-711-1 BASSA, la regola dei modelli: ora c'è la decisione dell'operatore dell'8 novembre scritta nella proposta, quindi si può considerare dichiarata.
- Verifica esterna #353:
  - V-1 BASSA: il limite passato a r.read() non è provato da nessun test. Si chiude nella fetta 2.
  - V-2 BASSA: la regola dei modelli è confermata solo nei report; si aspetta il commento dell'operatore sulla #353.
  - V-3 COSMETICA.
- R-712-1 BASSA: il posto nel tetto orario si consuma anche se il download fallisce.
- R-712-2 COSMETICA: con un valore non numerico, doppio warning nel log.
- R-712-3 BASSA: il contatore dei vocali si azzera quando il bot riparte.

**Memoria**: ho aggiunto la riga #715 in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, solo nel working tree, NON nello stage e NON committata (come chiesto, non ho lanciato commit_memoria_revisore.sh). Nessuna lezione nuova.

File rilevanti:
- /home/user/Gas/modules/telegram/bot.py
- /home/user/Gas/tests/test_unit_telegram_voce.py
- /home/user/Gas/.github/workflows/ci.yml
- /home/user/Gas/reports/proposta_voce_telegram.md
- /home/user/Gas/.claude/agents/memoria_revisore.md
- copia dell'index usata per i test: /tmp/claude-0/-home-user-Gas/48869dec-0411-5e4c-ab0d-042d43a34667/scratchpad/idx715

Review #716 (unione con main dopo la PR #352 di M2), verdetto integrale:

## VERDETTO: APPROVATO

Review #716 (chat Mani). Oggetto: merge staged, non ancora committato, di origin/main 3084979 (PR #352 di M2, riserve BASSE della #350) nel branch claude/peaceful-lovelace-0w2b7q (HEAD a08931f, PR #353). Repo: /home/user/Gas. Base comune: 9bfafdb.

**Letture obbligatorie fatte:** CLAUDE.md sez. 5, le righe di stato_progetto.md toccate dal merge e la coda della memoria (ultimo numero: #715; #712-M2 ha la sua numerazione).

**Controlli meccanici**
- I file di M2 nell'index sono identici, blob per blob, a MERGE_HEAD: modules/voice/server.py (dc38cfd), modules/sottofondo/__init__.py, tests/test_unit_voice_server.py, tests/test_unit_sottofondo.py e reports/ripartenza_m2.md. In HEAD questi file erano uguali alla base, quindi il diff portato è esattamente quello già revisionato da M2 (#711-M2).
- Sono identici a HEAD:
  - modules/telegram/bot.py (05ae407), tests/test_unit_telegram_voce.py e .github/workflows/ci.yml (9f5dac1);
  - i 3 report presi dal lato HEAD (--ours): ultimo_report, handoff e diff_sessione.
- Memoria e stato_progetto sono l'unione dei due lati. Nessuna riga aggiunta da un lato è andata persa:
  - memoria: HEAD 4 righe aggiunte su 4 presenti, MERGE_HEAD 3 su 3;
  - stato_progetto: HEAD 3 su 3, MERGE_HEAD 1 su 1.
  - L'unica riga sostituita in stato_progetto (la 615) è la versione più recente di M2.
- Nessun marcatore di conflitto. `git ls-files -u` è vuoto e `git diff --cached --check` è pulito.
- Working tree uguale all'index prima della mia riga, niente stash.

**Elementi del diff esaminati**
- `modules/telegram/bot.py:933` — importa in modo pigro `_USO_FORTE_PARLATO` e `cervello_voce` da modules/voice/server.py. Rischio: la #352 cambia firma o comportamento di quei simboli. Esito: ok.
  - Tutti gli hunk della #352 stanno dentro VoiceHandler (il primo parte da modules/voice/server.py:535).
  - Le righe 1-534 di server.py nell'index sono identiche a HEAD: lì vivono `_USO_FORTE_PARLATO` (modules/voice/server.py:111), il controllo di GAS_VOCE_FORTE (modules/voice/server.py:350) e `cervello_voce` (modules/voice/server.py:353).
  - Ho estratto e confrontato `cervello_voce` da sola: identica.
- `modules/telegram/bot.py:938` — `cervello_voce(trascritto, parlato=True)` con il ramo "uso" a modules/telegram/bot.py:939-941. Rischio: «forte» detto, uso e GAS_VOCE_FORTE si comportano in modo diverso dopo il merge. Esito: ok, la funzione è invariata. Lo confermano i test da tests/test_unit_telegram_voce.py:167 («forte» detto all'inizio va al cervello forte) e tests/test_unit_telegram_voce.py:174 (solo «forte» dà l'uso, nessun turno), verdi sulla copia dell'index.
- `.github/workflows/ci.yml:127` — la suite voce comprende tests/test_unit_telegram_voce.py; la suite sottofondo è a .github/workflows/ci.yml:221. Rischio: un test della #352 resta fuori dalla CI. Esito: ok. I due file di test di M2 sono già nelle suite esistenti e ci.yml è identico a HEAD.

**Test** (copia dell'index in scratch con `git checkout-index`, senza stash): test_unit_telegram_voce + test_unit_voice_server + test_unit_sottofondo → 231 passed (277 s).

**Rischi esclusi (non verificati)**
- Suite completa del kernel e CI reale: non lanciate, il merge non tocca gas.py né brains/.
- Comportamento reale con Telegram, Groq e il client voce sul Mac: non riproducibile in dev, i test usano finti.
- Contenuto tecnico della #352: già revisionato da M2 (#711-M2), qui ho verificato solo che sia arrivato intatto.

**Note cosmetiche** (non sono riserve)
- reports/stato_progetto.md:615 (testo di M2) dice ancora «Fetta BASSE della #350 (8 nov, PR aperta)». Dopo questo merge la #352 è mergiata: da aggiornare con i report di fine task.

**Memoria:** riga #716 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md nel working tree, NON committata come richiesto (non ho lanciato commit_memoria_revisore.sh). Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_telegram_voce.py`: nuovo, 31 casi. Riepilogo reale:

```
31 passed in 0.14s
```

Kernel (worktree, prima dell'unione): 1099 PASS, 1 FAIL. Il FAIL è T31g, il vector store che manca nell'ambiente, fuori scope.

Voice suite della CI, sulla copia dell'index della review #715: 337 passed.

Mutanti presi:
- vocale modificato accettato;
- niente tetto di durata;
- `..` nel percorso;
- niente controllo della lunghezza dopo il read (correzione: la verifica esterna #353 V-1 mostra che il limite PASSATO a read() non è provato da nessun test);
- niente eco;
- niente cervello_voce;
- niente tetto orario;
- niente pulizia della lista;
- bool accettato come durata;
- valore ≤0 accettato.

## §6 STATO CI

`gh` non usato: GitHub passa dallo strumento MCP. a08931f (head precedente della #353): handoff-check success. Verifica esterna APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/353#issuecomment-6725550824). Per il merge della #352 e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff. Della PR #351 su cad4291 erano success unit-suite, handoff-check e verifica; il bot era neutral; poi è stata mergiata.

## §7 RISERVE APERTE

- R-711-1 BASSA: regola dei modelli. ACCETTATA dall'operatore l'8 novembre: i vocali senza «forte» seguono le regole dei testi Telegram, GAS_VOCE_FORTE vale anche per i vocali.
- R-712-1 BASSA: un download fallito consuma comunque un posto del tetto orario. È una scelta prudente.
- R-712-2 COSMETICA: con un valore non numerico il warning compare due volte.
- R-712-3 BASSA: il contatore dei vocali si azzera quando il bot si riavvia.
- Bot sulla #351: V-1 BASSA, il test di R-681-1 va reso esatto (count == 2). Da fare nella prossima fetta voce, insieme a V-2 COSMETICA della verifica esterna #351 (inf/nan senza test).
- Le altre riserve sono in `reports/stato_progetto.md`.
