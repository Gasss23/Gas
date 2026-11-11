# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — voce: allucinazioni di Whisper scartate in silenzio (chat M2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #369 (https://github.com/Gasss23/Gas/pull/369): con verdetto del bot senza finding ALTA/MEDIA e CI verde («mergia» dell'operatore via M1).
2. R-761-1: su Telegram un vocale «Grazie» ora riceve «Non ho capito bene il vocale». Va bene o serve un messaggio diverso? (file della chat Mani)

NB: `gh` nel cloud non è autenticato; numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **Allucinazioni note di Whisper scartate in silenzio (con o senza parola di attivazione)**: `FATTA` (722e7b7).
- **Trascrizione vuota → silenzio anche con la parola di attivazione**: `FATTA` (722e7b7).
- **R-761-3-M2 (apostrofo e virgolette tipografici)**: `FATTA` — chiusa prima del commit, review #762-M2.
- **Merge di origin/main (#368 di Mani) nel ramo**: `FATTA` — conflitti solo nei report e nella memoria; review #763-M2 APPROVATO CON RISERVE (file di main identici; il client di ascolto chiude senza bip anche sul turno con la parola); voice_stt + voice_server + voce_ascolto 639 passed.
- **Bot e verifica esterna su 859d25b**: APPROVATO CON RISERVE, solo BASSE e COSMETICHE (varianti non in elenco come «Grazie, grazie.»; docstring sulla sottoclasse; voce doppia «sottotitoli a cura di»): registrate in §7.
- **Prova sul Mac dal vero**: `DEFERITA` — non riproducibile qui.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 modules/voice/server.py            |  19 ++++++++++++++-----
 modules/voice/stt.py               |  30 ++++++++++++++++++
 reports/diff_sessione.md           |  13 ++++++-------
 reports/handoff.md                 | n/d
 reports/ripartenza_m2.md           |   2 ++
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  17 ++++++++---------
 tests/test_unit_voice_stt.py       |  90 ++++++++++++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
b15a9a4 Merge origin/main (#368 di Mani) nella #369 — review #763-M2 APPROVATO CON RISERVE (chat M2)
859d25b docs(fine-task): voce — allucinazioni di Whisper, PR #369 (chat M2)
722e7b7 fix(voce): le allucinazioni di Whisper («Grazie.», «Sottotitoli…», solo punteggiatura) e le trascrizioni vuote si scartano in silenzio, senza turno — review #761-M2, #762-M2 (chat M2)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #763-M2 (merge di main, PR #368 di Mani) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #763-M2 sul merge di origin/main (#368) in fix/voce-allucinazioni-m2 (PR #369), diff staged in /home/user/Gas-alluc.

**Integrità del merge**
- clients/voice/ascolto.py, tests/test_unit_voce_ascolto.py e scripts/voce/LEGGIMI.md sono identici a origin/main (verificato con `git diff --cached origin/main --quiet`).
- `git diff --cached origin/main --stat` contiene solo la fetta (modules/voice/stt.py, modules/voice/server.py, tests/test_unit_voice_stt.py), i report (handoff, ultimo_report, diff_sessione, ripartenza_m2, stato_progetto con +1 riga) e la memoria (+#761, la lezione, +#762). Non ci sono doppioni.

**Citazioni del diff**
- modules/voice/stt.py:99 — `allucinazione()` normalizza l'apostrofo tipografico (’) e scarta tre casi: testo senza parole, frasi che contengono parti note, frasi intere note. Rischio esaminato: falsi positivi e regressioni di `_motivo_incerta`, che ora la riusa (modules/voice/stt.py:122). Esito: ok.
- modules/voice/stt.py:294 — `TrascrizioneAllucinata` viene sollevata prima di `_motivo_incerta`. È una sottoclasse di `TrascrizioneIncerta`, quindi il bot Telegram la intercetta ancora. Rischio: il bot Telegram la intercetta ancora come `TrascrizioneIncerta`, ma la risposta cambia (già tracciato come R-761-1 BASSA). Esito: ok.
- modules/voice/server.py:1210 — un `except TrascrizioneAllucinata` dedicato, messo prima di quello per `TrascrizioneIncerta`, chiama `_chiudi_seguito()` (risposta 200 `{"content":"","fine":true}` + `X-Gas-Comando: fine`, definita in modules/voice/server.py:1016). A modules/voice/server.py:1243 la trascrizione vuota chiude in silenzio anche con la parola di attivazione. Rischio: ordine degli `except` e nessun turno al kernel. Esito: ok.
- tests/test_unit_voice_stt.py:1260 — test della trascrizione vuota: verifica la risposta «fine» e che il kernel non venga chiamato. Esito: ok.

**Interazione col client aggiornato dalla #368 (citazioni di contesto)**
- clients/voice/ascolto.py:988 — `invia_al_server` riceve «fine» anche sul primo turno, quello con la parola, e restituisce `(True, None, "", "fine")`.
- clients/voice/ascolto.py:609 — `turno()` mette `chiudi=True`, svuota il microfono e restituisce False senza bip d'errore. Il ciclo esce a clients/voice/ascolto.py:833.
- Il caso è già coperto dal test del client tests/test_unit_voce_ascolto.py:761 (`test_fine_anche_dopo_la_parola_chiude_senza_bip`). Si sente solo il bip «ok» della parola. Esito: ok.

**Riserve**
- R-763-1-M2 COSMETICA: sul primo turno con la parola, un'allucinazione o una trascrizione vuota scrivono nel log del client «turno di seguito non rivolto a Gas» (clients/voice/ascolto.py:610). Il messaggio è fuorviante quando si cerca la causa di un problema, ma il comportamento è corretto.
- Restano aperte R-761-1/2-M2 BASSE e R-761-4-M2 COSMETICA.

**Cosa non ho verificato**
- Non ho rilanciato i test: i 639 passed li ha dichiarati il chiamante.
- Comportamento dal vero sul Mac (microfono, parola reale, Groq) non verificato: in questo ambiente non si può riprodurre.

**Memoria**
- Riga #763-M2 aggiunta in coda a /home/user/Gas-alluc/.claude/agents/memoria_revisore.md e messa in staging con `git -C /home/user/Gas-alluc add`. Nessun commit, come richiesto.

### Review #762-M2 (seguito di #761-M2, R-761-3) — verdetto integrale

VERDETTO: APPROVATO

Review #762-M2, seguito della #761-M2: ho controllato solo la correzione aggiunta al diff staged in /home/user/Gas-alluc. Chiude R-761-3-M2, la riserva sull'apostrofo e sulle virgolette tipografiche.

**Righe del diff esaminate**
- modules/voice/stt.py:102 — l'apostrofo tipografico ’ diventa ' prima di ridurre gli spazi. Rischio esaminato: falsi positivi sui nomi con apostrofo. «Dell’Orto, grazie» passa ancora al cervello. Mutante «tolgo la sostituzione dell'apostrofo», provato su una copia dell'index: 1 test fallito (`test_allucinazioni_note[Grazie per l’attenzione.]`), quindi il test se ne accorge. Esito: ok.
- modules/voice/stt.py:107 — la pulizia ai bordi ora toglie anche “ ” ‘ e i trattini - – —. L'apostrofo di chiusura ’ non serve nell'elenco, perché a quel punto è già diventato '. Rischio esaminato: un trattino ai bordi che faccia sembrare un'allucinazione un comando vero. «- no», «Gas-grazie» e «Grazie, ora segna il lead Rossi» passano ancora al cervello; «‘Grazie’» viene scartato, come deve. Esito: ok.
- tests/test_unit_voice_stt.py — tre casi nuovi: “Grazie.”, «Grazie per l’attenzione.», «— Grazie! —». Li ho rieseguiti: 29 passed (`-k allucin`).

**Riserve ancora aperte**, che registri tu:
- R-761-1-M2 BASSA: su Telegram un vocale «Grazie» ora riceve «Non ho capito bene il vocale».
- R-761-2-M2 BASSA: nella pagina browser, una trascrizione vuota fa vedere una risposta vuota invece dell'errore che aiutava a capire il guasto.
- R-761-4-M2 COSMETICA: «grazie» nell'elenco delle risposte brevi del seguito (modules/voice/server.py:190) non viene più raggiunto.

**Cosa non ho verificato**
- Quale apostrofo e quali virgolette scrive davvero Groq: non si riproduce qui senza audio vero.
- Non ho rieseguito tutti i 724 test: il cambio riguarda solo `allucinazione()`, che usano anche `_motivo_incerta` e `transcribe_audio`; quelli li ho già provati nella #761.

**Memoria**: riga #762-M2 aggiunta in /home/user/Gas-alluc/.claude/agents/memoria_revisore.md, nessuna lezione nuova. Il file è in staging con `git -C /home/user/Gas-alluc add`; nessun commit, come chiesto.

### Review #761-M2 — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #761-M2. Diff staged in /home/user/Gas-alluc, branch fix/voce-allucinazioni-m2, base a0c200c. Ho letto CLAUDE.md (sez. 5, 8, 9 e 10), reports/stato_progetto.md (le parti sulla voce) e la memoria del revisore. Questo diff chiude R-744-2-M2, la riserva aperta su «Grazie.» da solo che arrivava al cervello.

**Righe del diff esaminate**
- modules/voice/stt.py:99 — `allucinazione()`: se non c'è nessuna parola (`_PAROLA`) risponde True, poi cerca le parti note e infine la frase intera, tolta la punteggiatura ai bordi. Rischi esaminati:
  - falsi positivi: «Grazie, ora segna…», «Jarvis, grazie.», «Grazie Gas.», «Sì.», «3» passano tutti al cervello;
  - falsi negativi: «“Grazie.”» e «Grazie per l’attenzione.» con l'apostrofo tipografico non vengono scartati (R-761-3-M2);
  - testo in cirillico come «Спасибо.» viene scartato, ed è corretto.
  
  Esito: ok, con una riserva.
- modules/voice/stt.py:293 — `TrascrizioneAllucinata` viene alzata prima di `_motivo_incerta`. Dentro `_motivo_incerta` (modules/voice/stt.py:121) il controllo c'è ancora: è ridondante ma innocuo e lascia la funzione autosufficiente. Esito: ok.
- modules/voice/server.py:1210 — c'è un `except TrascrizioneAllucinata` dedicato prima di `TrascrizioneIncerta`, che chiama `_chiudi_seguito()` con o senza parola di attivazione. Nel log finisce solo l'esito: il test con caplog verifica che il testo non ci sia mai. `_do_stt` si chiama solo per le richieste a voce (modules/voice/server.py:772), quindi «fine» non arriva mai a una richiesta scritta. Esito: ok.
- modules/voice/server.py:1243 — una trascrizione vuota fuori dal seguito ora risponde 200 con «fine» invece di 400. Il conteggio del tetto orario resta invariato (test a tests/test_unit_voice_stt.py:582). Esito: riserva R-761-2-M2 per la pagina browser.
- Contesto, client H24: con «fine» alla parola di attivazione, clients/voice/ascolto.py:917 restituisce (True, None, "", "fine") e clients/voice/ascolto.py:584 chiude la conversazione senza bip. Esito: ok.
- Contesto, bot Telegram: modules/telegram/bot.py:186 prende `TrascrizioneIncerta`, quindi la sottoclasse non rompe niente. Però l'elenco allargato vale anche lì: un vocale «Grazie» prima arrivava al cervello, ora riceve «Non ho capito bene il vocale: puoi ripeterlo o scriverlo?». Il tipo di eccezione è lo stesso, il comportamento no. Esito: riserva R-761-1-M2.
- Contesto, pagina browser: clients/voice/browser_client.html:709 riceve JSON senza audio e mostra «risposta solo testo · Xs» con il testo vuoto. Prima mostrava l'errore «Trascrizione vuota (silenzio o formato non supportato)», che aiutava a capire un microfono o un formato guasto quando si preme il pulsante.

**Test e mutanti**
- Ho rieseguito io i test: 724 passed (tests/test_unit_voice_stt.py, tests/test_unit_voice_server.py, i test Telegram e tests/test_unit_voce_ascolto.py).
- Mutante «tolto l'except dedicato» (su una copia dell'index): 6 test falliti. Muore anche nel caso col seguito, dove la risposta sarebbe identica, perché il test controlla anche la riga di log del percorso: è la lezione #747.
- Mutante «tolto il controllo nessuna parola»: 4 test falliti («…», «...», «.», « ? »).

**Falso positivo accettato**: un «Grazie.» detto davvero dopo una risposta di Gas viene ignorato. Lo ritengo accettabile: nel seguito chiude la conversazione, che è quasi sempre quello che si vuole dopo un grazie, e non si perde nessuna informazione. Detto con la parola di attivazione, l'unico effetto è che Gas non risponde «di niente».

**Wall of Shame e regole**: nessuno slicing della history, nessuna simulazione dei tool. Non nascono eccezioni nuove che si propaghino (§9). Cap del loop e `_get_window` non toccati.

**Riserve**
- R-761-1-M2 BASSA — Telegram: un vocale «Grazie» o «Grazie mille» ora riceve «Non ho capito bene il vocale». Il docstring di modules/voice/stt.py:96 («il bot Telegram non cambia») è vero solo per il tipo di eccezione. Proposta: su Telegram trattare `TrascrizioneAllucinata` come «Nel vocale non ho sentito parole», oppure accettarlo e scriverlo.
- R-761-2-M2 BASSA — pagina browser: col pulsante, una trascrizione vuota o allucinata mostra una «risposta solo testo» vuota invece di un messaggio che spieghi (per esempio «non ho sentito niente»). Si perde la diagnosi del formato o del microfono.
- R-761-3-M2 BASSA — la pulizia ai bordi non toglie “ ” ‘ ’ e il trattino, e il confronto non normalizza l'apostrofo tipografico ’. Così «Grazie per l’attenzione.» e «“Grazie.”» non vengono scartati. Il problema c'era già per «grazie per l'ascolto».
- R-761-4-M2 COSMETICA — «grazie» in `_RISPOSTE_BREVI_SEGUITO` (modules/voice/server.py:190) ora non viene mai raggiunto: va tolto o commentato.

**Cosa non ho verificato**
- Come trascrive Groq sul Mac: se scrive davvero «Grazie.» e con quale apostrofo. Non si riproduce qui senza audio vero e senza la chiave di Groq.
- La pagina browser (clients/voice/browser_client.html) l'ho letta, ma non l'ho eseguita in un browser.
- Non ho eseguito l'intera suite del motore, solo i 4 gruppi di test della voce e di Telegram.

**Memoria**: ho aggiunto in /home/user/Gas-alluc/.claude/agents/memoria_revisore.md la riga #761-M2 e una lezione nuova: allargare una lista condivisa nello strato di trascrizione cambia il comportamento di tutti i canali che la usano, anche se l'eccezione nuova è una sottoclasse. Il file è in staging con `git -C /home/user/Gas-alluc add`, nessun commit come richiesto, quindi non ho lanciato commit_memoria_revisore.sh.

## §5 DELTA TEST DEL MOTORE

- gas.py non toccato. Test nuovi: `test_allucinazioni_note` (16 casi), `test_non_allucinazioni` (6), `test_transcribe_alza_trascrizione_allucinata`, `TestAllucinazioniServer.test_silenzio_senza_turno` (6 combinazioni formato × seguito, con caplog). Aggiornati: `test_v15_seguito_trascrizione_incerta_o_vuota_chiude`, `test_empty_transcription_chiude_in_silenzio` (prima `..._returns_400`), `test_v5_tetto_conta_uso_e_trascrizioni_vuote`.
- `python -m pytest -q tests/test_unit_voice_stt.py`: 140 passed (dopo R-761-3).
- `python -m pytest -q tests/test_unit_voice_stt.py tests/test_unit_voice_server.py tests/test_unit_telegram_voce.py tests/test_unit_voce_ascolto.py tests/test_unit_voice_tts.py -k "audit or not browser"` (prima di R-761-3):

```
724 passed, 25 deselected in 90.42s (0:01:30)
```

- Test col browser (voice_server + stt): 28 passed.

## §6 STATO CI

CI NON VERIFICATA con `gh` (non autenticato nel cloud).
- 859d25b: unit-suite success, handoff-check success, verifica-bot success (APPROVATO CON RISERVE, solo BASSE).
- 722e7b7 e merge di main: nessuna run propria letta.
- Commit di fine task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-761-3-M2 BASSA: CHIUSA (722e7b7, review #762-M2).
- R-744-2-M2 BASSA (preesistente): CHIUSA da questa PR («Grazie.» non arriva più al cervello).
- R-761-1-M2 BASSA: su Telegram un vocale «Grazie» ora riceve «Non ho capito bene il vocale» (decisione dell'operatore, §0 punto 2).
- R-761-2-M2 BASSA: nella pagina browser una trascrizione vuota o allucinata mostra una risposta vuota invece di un messaggio di diagnosi.
- R-761-4-M2 COSMETICA: «grazie» nell'elenco delle risposte brevi del seguito non viene più raggiunto.
- Bot su 859d25b V-1 BASSA: varianti non in elenco («Grazie, grazie.», «Grazie a tutti e alla prossima.», «Grazie mille a tutti.») vanno ancora al cervello — fetta successiva.
- Bot su 859d25b V-2/V-3 COSMETICHE: docstring della sottoclasse («Telegram non cambia» vale solo per il tipo); «sottotitoli a cura di» doppia; allucinazione() chiamata due volte.
- R-763-1-M2 COSMETICA: nel log del client, sul turno con la parola, «turno di seguito non rivolto a Gas» anche per un'allucinazione.
- Non verificato: come scrive davvero Groq (apostrofi, «Grazie.») sul Mac.
