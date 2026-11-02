# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Voce V6 «capire meglio» (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #318 (https://github.com/Gasss23/Gas/pull/318). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5113212832","url":"https://github.com/Gasss23/Gas/pull/318"}`); `gh` nel cloud non è autenticato. La mergia M1 se il bot dà APPROVATO pulito; con riserve aspetta il sì dell'operatore.
2. Dopo il merge, prova sul Mac (`reports/prova_voce_mac.md`): riga «Ho capito: …»; se Gas dice spesso «Non ho capito bene» parlando chiaro, `GAS_VOICE_STT_LOGPROB_MIN=-1.3` nel `.env`.

---

## §1 SCOPE & ESITO FETTE

- **V6.1 — trascrizione** (lingua, prompt, modello, scarto delle trascrizioni incerte): `FATTA` — il modello era già whisper-large-v3.
- **V6.2 — «Ho capito: …» nella pagina**: `FATTA`.
- **V6.3 — risposte e contesto**: `FATTA` — la storia c'era già; ora la prova `tests/test_unit_voice_contesto.py`; istruzione voce che tiene il filo.
- **V6.4 — tasto «non hai capito» con modello più grande**: `SALTATA — usiamo già il modello più grande di Groq`.
- **Riserve bot #314** V-1 (Groq 500 conta nel tetto) e V-2 (conteggi §2): `FATTA`.
- **Prova sul Mac della V5 passata** registrata in stato_progetto: `FATTA`.
- gas.py / brains/: non toccati.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 .github/workflows/ci.yml           |   5 +++--
 clients/voice/browser_client.html  |  15 ++++++++++++++-
 modules/voice/server.py            |  63 +++++++++++++++++++++++++++++++++++++++++++++++++++------------
 modules/voice/stt.py               | 112 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           |  20 +++++++++++---------
 reports/handoff.md                 | n/d
 reports/prova_voce_mac.md          |   5 ++++-
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  34 ++++++++++++++++------------------
 tests/test_unit_voice_contesto.py  | 143 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voice_server.py    |  12 ++++++++++--
 tests/test_unit_voice_stt.py       | 166 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
62803f7 feat(voce): V6 «capire meglio» — Whisper in italiano col vocabolario di Gas, «non ho capito» invece di rispondere a caso, «Ho capito: …» nella pagina (chat M2)
9e8b69e chore(revisore): memoria review #613 — APPROVATO
2fc86cf chore(revisore): memoria review #612 — APPROVATO CON RISERVE
fa188bc chore(revisore): memoria review #611 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit 62803f7 è stato rivisto in tre passaggi sullo stesso diff staged (tra un passaggio e l'altro cambiano solo `modules/voice/stt.py` e `tests/test_unit_voice_stt.py`, per chiudere le riserve; le righe citate dai primi due verdetti si riferiscono alla copia di allora). Verdetti integrali:

Review #611-M2 (primo passaggio):

## VERDETTO: APPROVATO CON RISERVE

Review #611-M2 (il contatore della memoria era a #610). Ho esaminato il diff staged di feat/voce-v6-m2 (7 file, +441/−22, base b472fe1). Ho letto CLAUDE.md, la memoria del revisore (le lezioni sulla voce M2 da #581 a #587) e la parte di stato_progetto che riguarda la voce.

**Cosa ho esaminato nel diff**
- modules/voice/stt.py:223 — controlla che il JSON di Groq sia un oggetto e chiama `_motivo_incerta` solo se il testo non è vuoto. Rischio esaminato: una risposta che è una lista manderebbe in crash `data.get`. Esito: ok, ora diventa GroqSTTError, che il server trasforma in 502, e c'è il test.
- modules/voice/stt.py:66 — `_motivo_incerta` fa la media dei segmenti pesata per durata (minimo 0,01 s, quindi niente divisione per zero). Se un segmento non è un dizionario o mancano i campi, la trascrizione non viene scartata. Rischio esaminato: scarti a caso se Groq cambia formato. Esito: ok, cade dal lato sicuro.
- modules/voice/stt.py:89 — scarta se la probabilità di silenzio (`no_speech`) supera 0,8, oppure se la confidenza media (`logprob`) è sotto −1,0. Esito: **riserva R-611-1-M2 (MEDIA)**. Whisper considera un pezzo «silenzio» solo se la probabilità di silenzio è alta E la confidenza è bassa. Qui basta la prima. Su whisper-large-v3 la probabilità di silenzio è nota per essere poco affidabile e alta anche su parlato vero, soprattutto sulle parole singole. Quindi un «sì» breve e chiaro può finire in «Non ho capito bene», proprio il caso d'uso che l'operatore ha provato. Nessun test copre un «sì» con silenzio 0,85 e confidenza −0,2. Proposta: scartare per silenzio solo se c'è anche confidenza bassa (per esempio sotto −0,5), oppure tarare sul Mac con la variabile d'ambiente. In ogni caso aggiungere un test che fissi il comportamento scelto.
- modules/voice/stt.py:24 — prompt col vocabolario di Gas. Esito: **riserva R-611-2-M2 (BASSA)**. Sul silenzio Whisper a volte ripete il testo del prompt («Gas, forte, lead, bozza…»). Questo caso non è nell'elenco delle frasi inventate, quindi arriverebbe al kernel come richiesta. In parte lo copre già la soglia di silenzio. Suggerimento: considerare incerta una trascrizione che contiene un pezzo lungo del prompt.
- modules/voice/server.py:292 — salva la trascrizione in `self._capito` prima di togliere «forte». Rischio esaminato: con connessioni HTTP/1.1 che restano aperte, una richiesta scritta potrebbe ricevere il «capito» di una richiesta precedente. Esito: ok. `HTTPServer` usa HTTP/1.0 (nessun `protocol_version` nel repo), quindi ogni richiesta ha la sua istanza. Il test `test_v6_risposta_dice_cosa_ha_capito` controlla che la risposta scritta non abbia «capito».
- modules/voice/server.py:351 — `_rispondi_senza_turno`, usato sia per «uso» sia per «non ho capito». Ha 3 formati: audio+testo, solo audio, JSON. Rischio esaminato: il refactor di «uso» cambia il comportamento? Esito: ok, stessi rami di prima, solo i campi `uso`/`non_capito` e «capito» in più.
- modules/voice/server.py:452 — nel log va solo `exc.motivo`, cioè numeri o la frase fissa, mai il parlato. La registrazione nel tetto orario resta prima di `transcribe_audio`. Esito: ok per la privacy e per la regola sulla gestione degli errori (sez. 9 di CLAUDE.md).
- clients/voice/browser_client.html:630 — mostra «Ho capito» con `textContent` e accetta solo stringhe. Esito: ok. Il test nel browser verifica che `<b>` resti testo e non diventi HTML. Qui la suite browser è stata saltata: mi baso sui vostri 10 passed.
- modules/voice/server.py:113 — `_CONTESTO_VOCE` aggiunto a entrambe le istruzioni vocali. Resta un'istruzione del singolo turno: non entra nella cronologia e non tocca `_get_window`. Esito: ok.
- tests/test_unit_voice_contesto.py:75 — usa il kernel vero, con finto solo il runner di `claude -p` e finto solo il client OpenAI. Esito: ok. Non simula l'output dei tool (nessun antipattern della sez. 5: niente slicing della cronologia, niente tool simulati). Il mutante su `_get_window` riportato da voi è credibile per come sono scritte le asserzioni.
- tests/test_unit_voice_stt.py:538 — **R-611-3-M2 (COSMETICA)**: la docstring dice «anche con forte davanti», ma il test usa «Gas, dimmi i lead» senza «forte».

**Test eseguiti da me**
- test_unit_voice_stt + test_unit_voice_contesto: 54 passed.
- test_unit_voice_server + test_unit_voice_tts: 101 passed (i test nel browser sono stati saltati qui perché non obbligatori in questo ambiente).

**Rischi esplicitamente esclusi**
- Taratura reale delle soglie (−1,0 / 0,8) su audio vero dal Mac, sia per il «sì» brevissimo sia per il rumore della TV: non riproducibile qui senza microfono né Groq vero. Per questo R-611-1-M2 è una riserva e non un blocco.
- Suite browser obbligatoria (Playwright): non eseguita, saltata in questo ambiente.
- Mutanti: non li ho rieseguiti, ho controllato solo che le asserzioni li prenderebbero.
- `_soglia_env` accetta «nan»/«inf» (con nan non scarterebbe mai): impatto trascurabile, non verificato oltre.

**Coerenza col progetto**
- gas.py e brains non sono toccati.
- Fail-safe: le eccezioni sono tutte intercettate e la risposta resta 200 o un errore dichiarato.
- Il tetto orario resta coerente con V-1 bot #314.
- Le riserve vanno tracciate in reports/stato_progetto.md prima del commit.

**Memoria**
Ho scritto la riga #611-M2 e una lezione (confrontare le soglie di scarto con la regola AND di Whisper) in /home/user/Gas/.claude/agents/memoria_revisore.md, committata da sola con commit_memoria_revisore.sh (fa188bc). Il diff staged è intatto (7 file). Non ho fatto altri commit.

Review #612-M2 (dopo le correzioni di R-611-1/2/3-M2):

## VERDETTO: APPROVATO CON RISERVE

Ri-review #612-M2 sulle modifiche fatte dopo la #611-M2 (branch feat/voce-v6-m2, diff staged di 7 file, non committato da me). Ho letto CLAUDE.md, lo stato del progetto (solo con ricerche mirate) e la mia memoria. Ho rifatto i test: stt + contesto **59 passed**. Ho provato tre mutanti e ogni volta ho rimesso stt.py com'era (nessuna modifica non in staging su stt.py).

**Elementi del diff esaminati**
- `modules/voice/stt.py:107` — il silenzio scatta solo se `no_speech > soglia` E `logprob < _LOGPROB_SILENZIO` (-0,5). Rischio: un «sì» breve e chiaro viene scartato. Mutante senza la condizione AND → 1 failed (`test_v6_si_breve_e_chiaro_passa_anche_con_no_speech_alto`). Esito: ok, **R-611-1-M2 chiusa**. Nota: -0,5 è più severo del -1 di Whisper. Va bene, perché sotto -1 scarta comunque la regola della confidenza.
- `modules/voice/stt.py:76` — `_soglia_env` con `math.isfinite`. Rischio: «nan» o «inf» spengono il controllo. Mutante senza isfinite → 1 failed (`test_v6_soglie_da_env`). Esito: ok.
- `modules/voice/stt.py:87` — controllo dell'eco del prompt (almeno 4 parole, almeno l'80% del prompt). Rischio: le richieste vere e brevi vengono scartate. Mutante → 2 failed, come mi hai detto. Esito: **riserva** (vedi R-612-1-M2).
- `tests/test_unit_voice_stt.py:560` — il test del «capito» ora usa «Gas, forte: dimmi i lead», controlla il testo intero e `cervello == "forte"` sui kw salvati prima della richiesta scritta (il kernel finto li registra a `tests/test_unit_voice_stt.py:47`). Esito: ok, **R-611-3-M2 chiusa**.

**Caso limite che mi hai chiesto: il rischio NON è accettabile così com'è**
- **R-612-1-M2 MEDIA**: il controllo dell'eco (`modules/voice/stt.py:87`) guarda le parole come un insieme, non come una sequenza. Il prefisso «Gas, forte» porta già 2 parole del prompt in ogni comando parlato al cervello forte. L'ho verificato con `_motivo_incerta` e confidenza buona: vengono scartate «Gas forte report merge», «Gas forte memoria lead», «firma bozza lead forte» e soprattutto **«Gas, forte, firma la bozza»** (4 parole su 5 = 0,8, proprio sulla soglia).
  - Lo scarto è deterministico: ripetere la frase non serve, bisogna riformularla o scriverla.
  - Passano invece «Claude merge PR» (3 parole), «Gas, forte: dimmi i lead» e «manda il report in Telegram con Claude».
  - Niente crash, e l'operatore vede cosa è stato sentito: per questo resta riserva e non blocco.
  - Correzione proposta: considerarla eco solo se la sequenza di parole è un pezzo contiguo del prompt. Le due eco del test lo sono, i comandi veri no. In alternativa: solo con no_speech non basso.
  - Va aggiunto un test in cui «Gas, forte, firma la bozza» passa.
- R-611-2-M2 (l'eco del prompt) è quindi chiusa nel merito, ma lascia questa riserva nuova.

**Cosa non ho verificato**
- Il comportamento reale di whisper-large-v3 su Groq: no_speech e logprob veri su un «sì» o sul silenzio, e se l'eco reale del prompt è sempre contigua. Serve l'audio vero sul Mac, che qui non è riproducibile. Le soglie restano da tarare con la prova sul Mac.
- Non ho rifatto i test di server, tts e browser: rispetto alla #611 quei file non sono cambiati.

**Memoria**: ho aggiunto la riga #612-M2 e una lezione (provare i filtri per parole chiave con i comandi veri più corti, prefisso «Gas, forte» compreso) in /home/user/Gas/.claude/agents/memoria_revisore.md. Commit 2fc86cf, solo quel file; lo staging del diff resta com'era (7 file).

Review #613-M2 (diff finale committato in 62803f7):

## VERDETTO: APPROVATO

Ho controllato la ri-review #612-M2 sul branch feat/voce-v6-m2: il diff staged ha 7 file e il delta riguarda solo stt.py e il suo test. Ho letto CLAUDE.md (sez. 5), stato_progetto.md (con grep) e memoria_revisore.md, dove le righe #611-M2 e #612-M2 riportano le riserve R-611-* e R-612-1-M2.

Elementi del diff esaminati:
- `modules/voice/stt.py:60` — `_PAROLE_PROMPT` ora è una tupla ordinata delle parole del prompt, 30 in tutto. «l'assistente» si spezza in «l» e «assistente», allo stesso modo per prompt e trascrizione. Rischio esaminato: un ordine non stabile o una tokenizzazione diversa tra i due lati. Esito: ok.
- `modules/voice/stt.py:63` — `_pezzo_del_prompt` cerca la sequenza come finestra contigua. Rischio esaminato: falsi positivi e casi limite (n più lungo del prompt dà un range vuoto, quindi False). Esito: ok. Nota COSMETICA: il tipo è `parole: list` e non `list[str]`.
- `modules/voice/stt.py:95` — l'eco scatta solo se la frase ha almeno 4 parole ed è un pezzo contiguo del prompt; il filtro a insieme con quota 80% è sparito. Le sonde che ho lanciato io: passano «Gas, forte, firma la bozza», «Gas forte report merge», «Gas forte bozza firma contatto», «report PR merge», «con Gas» e «memoria»; vengono scartate «Gas forte lead bozza» e «lead bozza firma contatto». Esito: ok, **R-612-1-M2 chiusa**. Il rischio residuo che hai indicato è reale ma stretto: la frase deve essere solo parole del prompt, nel suo stesso ordine e senza parole in mezzo, e l'operatore vede «Ho capito».
- `tests/test_unit_voice_stt.py:247` e `tests/test_unit_voice_stt.py:258` — i test parametrici scartano le eco e fanno passare le richieste vere con parole del prompt. Ho riprodotto il mutante con la vecchia regola a insieme 80%: 4 failed, 57 passed. Ho poi rimesso il file com'era; l'index staged non è stato toccato. Ho riprodotto anche stt + contesto: 63 passed. Esito: ok.

Nessun antipattern del Wall of Shame: il delta non tocca né slicing della storia né output simulato dei tool. Il fail-safe resta: `TrascrizioneIncerta` viene alzata solo dentro `transcribe_audio`.

Non ho verificato:
- il comportamento reale di Whisper large-v3 su Groq (frequenza delle eco del prompt sul silenzio, quanto sono tarate le soglie). Non si riproduce qui senza audio e chiave; va provato sul Mac (reports/prova_voce_mac.md).
- le suite server e browser: il delta di questa ri-review non le tocca.

Riga contatore `#613-M2` scritta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (commit 9e8b69e, messaggio `chore(revisore): memoria review #613 — APPROVATO`). Nessuna lezione nuova. Il diff della fetta non l'ho committato.

## §5 DELTA TEST DEL MOTORE

gas.py non toccato. Voce: `tests/test_unit_voice_stt.py` 37 → 61 test (V6: parametri a Groq, soglie, media pesata, frasi inventate, eco del prompt, «sì» breve con no_speech alto, comandi veri con parole del prompt, env non numeriche/nan/inf, JSON non oggetto, «non ho capito» senza turno, «capito» nelle risposte, V-1 bot #314); nuovo `tests/test_unit_voice_contesto.py` 2 test (kernel vero, forte e normale ricevono la conversazione); test della pagina nel browser con la riga «Ho capito». Run misurate in sessione: stt + contesto 63 passed; stt+server+tts non-browser 122 passed (prima delle correzioni finali a stt); pagina nel browser con GAS_TEST_BROWSER_OBBLIGATORIO=1: 10 passed. Mutanti presi: `_motivo_incerta` spento → 6 failed; `_get_window` ridotto all'ultimo messaggio → 2 failed; senza AND del silenzio → 1 failed; vecchia regola dell'eco a insieme → 4 failed. Nessun FAIL.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- fa188bc, 2fc86cf, 9e8b69e, 62803f7: pushati insieme prima dell'apertura della PR #318; nessuna run della PR su questi SHA.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Riserve di questa sessione (R-611-1/2/3-M2, R-612-1-M2): tutte chiuse (review #613-M2). Nota COSMETICA #613: tipo `parole: list` invece di `list[str]`.
- Da provare sul Mac: le soglie della trascrizione incerta (-1,0 / 0,8) su audio vero.
- **R-584-1-M2** BASSA (rumore costante ≥ 0,045 RMS preso per voce), **R-583-1-M2** COSMETICA, **R-576-1-M2** BASSA, **R-576-3-M2** COSMETICA (fette precedenti).
