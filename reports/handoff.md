# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 — voce: filtro 2, più allucinazioni di Whisper scartate (chat M2)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #373 (https://github.com/Gasss23/Gas/pull/373): il bot sul head precedente aveva una V-1 di gravità media (corretta qui, review #774/#775-M2 con riserve BASSE) e la verifica esterna #373 era APPROVATO CON RISERVE (BASSE): con riserve resta pronta per il «mergia» del mattino; con verdetto del bot APPROVATO pulito e CI verde la mergia la chat.
2. R-764-2-M2: su Telegram un vocale «Grazie di cuore» ora riceve «Non ho capito bene il vocale». Va bene? (file della chat Mani)
3. R-774-1-M2: una richiesta corta coi crediti seguita da «, grazie mille» («Scarica i sottotitoli a cura di Rai, grazie mille.») viene scartata in silenzio. Gas non gestisce sottotitoli: accettabile?

NB: `gh` nel cloud non è autenticato; numero e URL della PR vengono dalla risposta reale dello strumento GitHub MCP `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **Varianti dei saluti, frasi intere senza punteggiatura interna, allucinazioni composte frase per frase**: `FATTA` (438704b).
- **Parti note solo su frasi corte (V-1 bot #369)**: `FATTA` (438704b).
- **Intercalari nel seguito**: `FATTA` (438704b).
- **R-764-1, R-766-1, R-767-1**: `FATTA` — chiuse prima del commit (review #766, #767, #769-M2).
- **V-1 del bot #373 (crediti + chiusura con virgola o senza punteggiatura passavano)**: `FATTA` (789ade7) — divisione anche su , ; : e crediti che finiscono con una chiusura lunga a parola intera (review #774, #775-M2).
- **Merge di origin/main (#370)**: `FATTA` (7f7933e, review #777-M2).
- **V-1 del bot #373 su 4559e23 (gravità media: «Niente.» nel seguito scartato, regressione)**: `FATTA` (48b605f) — «niente»/«nulla» tolti dagli intercalari (review #780-M2).
- **Prova sul Mac dal vero**: `DEFERITA`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md | 13 +++++++++++++
 modules/voice/server.py            | 15 ++++++++++++++-
 modules/voice/stt.py               | 67 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------
 reports/diff_sessione.md           | n/d
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          | n/d
 reports/ultimo_report.md           | n/d
 tests/test_unit_voice_server.py    | 13 +++++++++++++
 tests/test_unit_voice_stt.py       | 47 +++++++++++++++++++++++++++++++++++++++++++++++
```

NB: confronto con origin/main (e3eb542, dopo il merge). Regola «n/d» — i conteggi dei report riscritti in questo commit di fine-task non sono misurabili mentre li si scrive; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
48b605f fix(voce): «Niente.»/«Nulla.» nel seguito tornano risposte valide, non intercalari (V-1 bot #373 su 4559e23)
4559e23 docs(fine-task): #373 dopo V-1 bot e merge di main — review #774-#777-M2 (chat M2)
7f7933e Merge origin/main (#370) nella #373 — review #777-M2 APPROVATO (chat M2)
789ade7 fix(voce): filtro 2 — crediti seguiti da chiusura con virgola o senza punteggiatura scartati (V-1 bot #373)
2f31b66 docs(fine-task): voce — filtro 2, PR #373 (chat M2)
438704b fix(voce): filtro 2 — varianti dei saluti di Whisper e allucinazioni composte scartate frase per frase, intercalari nel seguito, parti note solo su frasi corte — review #764/#766/#767/#769-M2 (chat M2)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #780-M2 (V-1 bot #373 su 4559e23) — verdetto integrale

## VERDETTO: APPROVATO

Review #780-M2: correzione della V-1 MEDIA del bot sulla PR #373 (head 4559e23). Il diff staged in /home/user/Gas-filtro2 tocca 2 file del motore, più la memoria del revisore.

**Cosa ho controllato nel diff**
- `modules/voice/server.py:223`: «niente» e «nulla» sono stati tolti da `_INTERCALARI`. Il rischio era che una parola stesse sia nell'elenco che scarta sia in quello che accetta. Ho calcolato a runtime l'intersezione tra `_INTERCALARI` e `_RISPOSTE_BREVI_NORM` (`modules/voice/server.py:215`): è vuota. Esito: ok.
- Parità con main per una parola sola. Su origin/main «niente» e «nulla» erano già tra le risposte brevi (origin/main, `modules/voice/server.py` riga 203), e su main una frase lunga passa sempre. Con l'intersezione vuota, su una parola sola il nuovo `seguito_da_scartare` dà lo stesso risultato di main. Verificato eseguendolo: «Niente.», «Nulla.», «Nulla!» e «niente» danno False. «Mai» dà False. «Comunque», «Boh» e «Quindi?» danno True, come su main, perché non sono risposte brevi. Esito: ok.
- `modules/voice/server.py:235`: il filtro 2 (`all(p in _INTERCALARI ...)`) cambia il comportamento solo per le frasi di più parole fatte tutte di intercalari. «Ehm, allora…» e «Mah, boh.» danno ancora True, quindi restano scartate. «Ehm, niente.» e «Niente niente» danno False, cioè passano: è corretto. Esito: ok.
- `tests/test_unit_voice_server.py:2597`: aggiunti i casi ("Niente.", False), ("Nulla!", False), ("Ehm, niente.", False). Il caso «Comunque» True resta. Ho rieseguito `-k seguito`: 14 passed. Esito: ok.
- Le regole del progetto sono rispettate: nessuno slicing della history, nessun output di strumenti simulato, nessuna nuova eccezione.

**Correzione alla mia review #764**: lì avevo scritto «"Niente." da solo era già scartato prima». Era falso: non l'avevo verificato su main. L'ho annotato nella memoria.

**Cosa NON ho verificato**
- La suite completa di `tests/test_unit_voice_server.py`: l'ho lanciata, ma non ha finito entro il tempo. Ho verificato solo il gruppo `-k seguito`. Il resto della suite non è stato rieseguito su questo diff, ma la modifica riguarda solo questo filtro.
- Il comportamento con Whisper reale e il microfono: non si riproduce in dev.

**Memoria del revisore**: ho aggiunto la riga #780-M2 e una lezione. Quando un elenco che scarta parole sta accanto a uno che le accetta, l'intersezione va calcolata e deve essere vuota. Ogni frase del tipo «prima era già così» va provata eseguendo la funzione su origin/main. Il file è in staging insieme al diff, come mi hai chiesto. Non ho eseguito `scripts/commit_memoria_revisore.sh`, per non creare un commit separato sul branch prima del tuo.

File: /home/user/Gas-filtro2/modules/voice/server.py, /home/user/Gas-filtro2/tests/test_unit_voice_server.py, /home/user/Gas-filtro2/.claude/agents/memoria_revisore.md

### Review #777-M2 (merge di origin/main) — verdetto integrale

## VERDETTO: APPROVATO

Review #777-M2: merge di origin/main e3eb542 (con la #370) nella PR #373 (filtro 2 delle allucinazioni di Whisper), staged in /home/user/Gas-filtro2 (HEAD 789ade7).

**Letture obbligatorie fatte**: CLAUDE.md §5, reports/stato_progetto.md (letto per sezioni, voci #369/#373) e la coda di .claude/agents/memoria_revisore.md.

**Controlli meccanici**
- `git ls-files -u` è vuoto e `git diff --cached --check` è pulito. Non ci sono marcatori di conflitto nei file toccati: le righe `=======` che grep trova in reports/e2e_k3bis_output.txt erano già nel file, sono separatori.
- gas.py, modules/telegram/bot.py, tests/test_unit_kernel.py e tests/test_unit_notte.py sono identici a MERGE_HEAD: 0 righe di diff.
- In `.claude/agents/memoria_revisore.md` e `reports/stato_progetto.md` il merge non toglie nessuna riga rispetto a nessuno dei due lati, sono state solo aggiunte. Nella memoria restano due righe doppie (#746 e #747 della chat M3) che c'erano già prima del merge.
- Righe tolte solo in reports/handoff.md, reports/ultimo_report.md e reports/diff_sessione.md: lì è stata tenuta la versione del branch, come dichiarato.

**Elementi del diff esaminati**
- `modules/voice/stt.py:150` — `allucinazione()` controlla frase per frase e scarta solo se ogni frase è un'allucinazione. Rischio esaminato: che la #370 cambi l'ingresso o chi la chiama. La #370 non tocca modules/voice/. Esito: ok.
- `modules/voice/stt.py:113` — `TrascrizioneAllucinata` è una sottoclasse di `TrascrizioneIncerta`. Rischio esaminato: che il bot Telegram, toccato dalla #370, non prenda più l'eccezione. Il vocale passa ancora da `except TrascrizioneIncerta` (`modules/telegram/bot.py:186`). Nella #370, bot.py cambia solo un commento (`modules/telegram/bot.py:951`). Esito: ok.
- `modules/voice/server.py:1221` — l'except dedicato chiude il seguito e scarta in silenzio. Rischio esaminato: che `avviso_ripiego` o `versione_leggera` della #370 finiscano a voce. Nessuna occorrenza in modules/voice/. Esito: ok.
- `tests/test_unit_voice_stt.py:1398` — i casi della divisione in frasi sono ancora nella suite dopo il merge. Esito: ok.

**Test rieseguiti da me**
- test_unit_voice_stt + test_unit_voice_server + test_unit_notte: 599 passed.
- test_unit_telegram_voce: 74 passed.

**Rischi esclusi**
- La suite del kernel (1134 PASS, 1 FAIL T31g perché manca fastembed) non l'ho rieseguita. gas.py è identico a main (diff 0), quindi il risultato dipende solo da main.
- Comportamento dal vivo (Mac, Groq vero) non verificato: non riproducibile qui.

**Memoria**
- Riga `#777-M2` aggiunta in coda a `.claude/agents/memoria_revisore.md` e messa in staging (`git add`), nessuna lezione nuova.
- Non ho lanciato `scripts/commit_memoria_revisore.sh`: il merge è ancora in corso e git non accetta un commit parziale (`-o`) durante un merge. Il file entra col commit di merge.
- Il numero #777 l'ho preso dalla tua richiesta: in coda al file, sul lato M2, l'ultima riga è #775-M2 e non esiste una #776-M2.
- Per la regola R-139-1 non chiudo con un riepilogo «Verdetto finale»: l'esito sta solo nella prima riga.

File rilevanti:
- /home/user/Gas-filtro2/modules/voice/stt.py
- /home/user/Gas-filtro2/modules/voice/server.py
- /home/user/Gas-filtro2/modules/telegram/bot.py
- /home/user/Gas-filtro2/.claude/agents/memoria_revisore.md

### Review #775-M2 (seguito di #774-M2) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #775-M2 su tutto il diff in staging in /home/user/Gas-filtro2 (PR #373). Le due riserve del giro precedente sono chiuse: R-774-2-M2 (la chiusura ora conta solo a parola intera) e R-774-3-M2 (aggiunti test che dipendono solo dalla divisione su virgola e due punti). Nessuna regola del Wall of Shame è violata e nessun guardrail è toccato.

**Elementi del diff esaminati**
- `modules/voice/stt.py:126` — `_CHIUSURE_LUNGHE` mette ora uno spazio davanti a ogni chiusura. Rischio: corrispondenza a metà parola. Esito: ok, il test con «delle disgrazie a voi» passa al cervello. Mutante «spazio tolto dalle chiusure»: 1 failed, ucciso.
- `modules/voice/stt.py:138` — `(" " + " ".join(parole)).endswith(_CHIUSURE_LUNGHE)`. Rischio: chiusure che non combaciano mai. Esito: **riserva**. `_PAROLA` toglie l'apostrofo, quindi «l'ascolto» diventa «l ascolto». Le chiusure scritte con l'apostrofo («grazie per l'ascolto», «grazie per l'attenzione») non combaciano mai in questo controllo: «Sottotitoli creati dalla comunità Amara.org grazie per l'ascolto» passa al cervello (verificato).
- `modules/voice/stt.py:123` — divisione su `, ; :`. Esito: ok. Mutante «virgola tolta»: 2 failed. Mutante «: tolto»: 1 failed. Mutante «; tolto»: sopravvive, perché nessun test dipende dal punto e virgola (cosmetica).
- `tests/test_unit_voice_stt.py:1398` — «Sottotitoli a cura di QTSS, grazie per la visione, alla prossima.» viene scartata solo grazie alla divisione. Esito: ok.
- `tests/test_unit_voice_stt.py:1420` — richiesta con «disgrazie a voi». Esito: ok, passa.

**Prove eseguite**
- `tests/test_unit_voice_stt.py`: 181 passed. `-k telegram`: 101 passed.
- Mutanti con `-k "filtro2 or allucin"`:
  - uccisi: regola nuova tolta (2 failed), virgola tolta (2 failed), «:» tolto (1 failed), spazio tolto dalle chiusure (1 failed);
  - sopravvissuti:
    - «;» tolto: nessun test usa il punto e virgola (cosmetica);
    - fine frase cambiata in «contiene»: manca un test con la chiusura a metà frase (bassa, non ho aperto una riserva a parte);
    - spazio tolto davanti alla frase: equivalente, non cambia il comportamento.
- Dopo i mutanti `modules/voice/stt.py` è tornato identico alla versione in staging (`git diff` vuoto).

**Riserve**
- **R-775-1-M2 (BASSA)**: le chiusure con apostrofo non funzionano nel controllo di fine frase. Proposta: costruire `_CHIUSURE_LUNGHE` con `" ".join(_PAROLA.findall(f))`.
- **R-775-2-M2 (COSMETICA)**: nessun test per «;».
- R-774-1-M2 (BASSA) e R-774-4-M2 (COSMETICA) restano aperte; le hai accettate come riserve. Due esempi verificati ancora oggi: «Scarica i sottotitoli a cura di Rai, grazie mille.» e «Cerca chi ha fatto i sottotitoli a cura di Rai e digli grazie a tutti» vengono scartate.
- Restano aperte anche R-764-2-M2 (BASSA) e R-761-4 (COSMETICA).

**Non verificato**: il comportamento sull'audio reale di Groq Whisper e del server voce (servono microfono e rete). Non ho rilanciato le suite del server voce né dell'ascolto: il diff tocca solo la funzione `allucinazione()`.

**Memoria**: ho aggiunto in coda a /home/user/Gas-filtro2/.claude/agents/memoria_revisore.md la riga contatore #775-M2 e una lezione: le parole estratte da una regex che toglie l'apostrofo non combaciano con voci d'elenco scritte con l'apostrofo. Il file è in staging; non ho committato.

### Review #774-M2 (V-1 bot #373) — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Review #774-M2 sul diff in staging di /home/user/Gas-filtro2 (PR #373, filtro delle allucinazioni di Whisper). La correzione chiude la V-1 di gravità media del bot #373: «Sottotitoli a cura di QTSS, grazie per la visione.» e le altre 4 varianti nuove vengono scartate. Nessuna regola del Wall of Shame è violata (niente history, niente simulazione di tool) e nessun guardrail è toccato. Restano però falsi positivi nuovi, e i test non coprono la divisione su virgola e punteggiatura simile.

**Elementi del diff esaminati**
- `modules/voice/stt.py:123` — `_FINE_FRASE_STT` ora divide anche su `, ; :` seguiti da spazio. Rischio esaminato: richieste vere scartate in silenzio. Esito: **riserva**. Il tetto di 8 parole per le parti note ora vale per ogni pezzo tra due virgole, non per la frase intera:
  - «Scarica i sottotitoli a cura di Rai, grazie mille.» ora viene scartata. Prima passava (verificato col codice di HEAD).
  - «Sottotitoli, grazie.» e «Grazie mille, sottotitoli.» ora vengono scartate. Prima passavano.
  - Restano corrette: «Gas, cerca chi ha fatto i sottotitoli a cura di Rai, grazie.» passa, perché il pezzo «gas,» non è un'allucinazione. «Grazie: alla prossima riunione parliamo di Rossi.» passa. «1,5 grazie» passa (niente spazio dopo la virgola).
- `modules/voice/stt.py:138` — `" ".join(parole).endswith(_CHIUSURE_LUNGHE)`, con `_CHIUSURE_LUNGHE` definita in `modules/voice/stt.py:126` (16 chiusure di almeno 3 parole). Rischio esaminato: corrispondenze a metà parola e richieste lunghe che finiscono con un saluto. Esito: **riserva**.
  - «Cerca chi ha fatto i sottotitoli a cura di Rai e digli grazie a tutti» ora viene scartata. Prima passava.
  - Il confronto non controlla il confine di parola: «…disgrazie a voi» combacia con «grazie a voi».
  - Falso negativo cosmetico: «Sottotitoli a cura di QTSS grazie a tutti per la visione e alla prossima» passa ancora.
- `modules/voice/stt.py:135` — il tetto di 8 parole resta prima della regola nuova. Rischio esaminato: regressione della V-1 bot #369. Esito: ok sulla frase intera; il caso «Gas, cerca chi ha fatto i sottotitoli a cura di Rai per il film» passa ancora.
- `tests/test_unit_voice_stt.py:1392` e `tests/test_unit_voice_stt.py:1396` — casi scartati con virgola e punto e virgola. Rischio esaminato: se i test uccidono l'estensione del separatore. Esito: **riserva**. Il primo caso lo prende anche la regola `endswith`, il secondo il tetto di 8 parole sulla frase intera, quindi nessuno dei due dipende davvero dalla divisione su virgola.
- `tests/test_unit_voice_stt.py:1413` — richieste vere con virgola e due punti. Esito: ok, passano.

**Prove eseguite**
- `tests/test_unit_voice_stt.py`: 177 passed.
- `-k telegram`: 101 passed.
- Mutanti, tutti lanciati con `-k "filtro2 or allucin"`:
  - regola `endswith` sostituita da `if False:` → 2 failed, **ucciso**;
  - virgola tolta dalla regex → 66 passed, **sopravvive**;
  - «;» tolto → **sopravvive**;
  - «:» tolto → **sopravvive**;
  - soglia delle chiusure da 3 a 2 parole → **sopravvive**;
  - `endswith` sostituito da «contiene» → **sopravvive**.
- Ho controllato che la divisione su virgola abbia un'utilità reale: «Sottotitoli a cura di QTSS, grazie per la visione, alla prossima.» e «Grazie per la visione, sottotitoli a cura di QTSS.» vengono scartate solo grazie a lei.

**Riserve (da tracciare in stato_progetto.md)**
- **R-774-1-M2 (BASSA)**: con la divisione su virgola il tetto di 8 parole si applica a ogni pezzo. Una richiesta corta coi crediti, seguita da «, grazie mille», viene scartata in silenzio; idem «Sottotitoli, grazie.». Rischio pratico basso, perché Gas non gestisce sottotitoli.
- **R-774-2-M2 (BASSA)**: il controllo `endswith` va agganciato al confine di parola (`(" " + testo).endswith(" " + c)`). Inoltre oggi colpisce ogni frase lunga con una parte nota che finisce con un saluto.
- **R-774-3-M2 (BASSA, test)**: nessun test uccide l'estensione del separatore. Proposta: aggiungere «Sottotitoli a cura di QTSS, grazie per la visione, alla prossima.», che uccide il mutante «virgola tolta», e un caso con «:».
- **R-774-4-M2 (COSMETICA)**: «… QTSS grazie a tutti per la visione e alla prossima» passa.
- R-764-2-M2 (BASSA) e R-761-4 (COSMETICA) restano aperte.

**Non verificato**
- Il comportamento sull'audio reale di Groq Whisper e del server voce: richiede un microfono e la rete, non è riproducibile qui. Ho controllato solo la funzione `allucinazione()` e i test unitari.
- Non ho rilanciato le suite del server voce né dell'ascolto: il diff tocca solo la funzione pura.

**Memoria**
- Ho aggiunto in coda a /home/user/Gas-filtro2/.claude/agents/memoria_revisore.md la riga contatore #774-M2 e 2 lezioni nuove:
  1. allargare un separatore di frasi fa riapplicare i tetti per frase a ogni pezzo;
  2. `endswith` senza spazio iniziale combacia a metà parola.
- Il file è in staging in /home/user/Gas-filtro2. Non ho lanciato `commit_memoria_revisore.sh`, perché mi hai chiesto solo lo staging.
- Durante i mutanti un `>` nel testo di un `echo` ha creato per errore il file `in` nella radice del repo: l'ho cancellato. `modules/voice/stt.py` è tornato identico alla versione in staging (`git diff` vuoto).

### Review #769-M2 (seguito di #767-M2, R-767-1) — verdetto integrale

VERDETTO: APPROVATO

Review #769-M2 (segue la #767-M2) sul diff staged di /home/user/Gas-filtro2. R-767-1-M2 è chiusa: le allucinazioni composte (crediti + saluto) tornano a essere scartate e le richieste vere passano.

Le review #764, #766 e #767 le avevo già consegnate prima dei tuoi messaggi. In breve, tutte APPROVATO CON RISERVE:
- #764-M2: R-764-1 e R-764-2, entrambe BASSE.
- #766-M2: chiude R-764-1 e apre R-766-1 (BASSA).
- #767-M2: chiude R-766-1 e apre R-767-1 (MEDIA), ora chiusa da questo diff.

**Elementi del diff esaminati**
- `modules/voice/stt.py:124` — `_frase_allucinata` raccoglie le regole che prima valevano per tutta la trascrizione: nessuna parola, parti note col tetto di 8 parole, frasi intere con e senza punteggiatura interna, saluti con almeno un «grazie». Rischio: perdere una regola nello spostamento. Esito: ok, i casi di #764, #766 e #767 danno lo stesso risultato.
- `modules/voice/stt.py:121` — `_FINE_FRASE_STT` divide le frasi solo dove la punteggiatura di fine frase è seguita da uno spazio. Rischio: spezzare «amara.org». Esito: ok.
  - «amara.org» resta intera e la frase dei crediti viene scartata.
  - «Grazie.Grazie mille.» (senza spazio) viene scartata già dal controllo sulla frase intera.
- `modules/voice/stt.py:151` — divisa in frasi, la trascrizione è scartata solo se OGNI frase è un'allucinazione (`all`). Esito: ok.
  - Scartate, anche passando da `_motivo_incerta`: «Sottotitoli creati dalla comunità Amara.org. Grazie per la visione.», «Sottotitoli a cura di QTSS. Grazie a tutti per la visione.», «Grazie. Grazie mille. Alla prossima!», «Grazie! Ciao a tutti!».
  - Passano: «Grazie. Ora segna il lead Rossi.», «Grazie mille. Che ore sono?», «Grazie. Il prossimo.», «Segna il lead Rossi. …» (la frase fatta di soli puntini non trascina con sé quella vera), la richiesta lunga coi «sottotitoli a cura di Rai», «Chi ha fatto i sottotitoli a cura di Rai? Sottotitoli a cura di chi?».

**Test e mutanti**
- Suite voice_stt + voice_server + telegram_voce + voce_ascolto (`-k "audit or not browser"`): **751 passed**.
- Mutanti provati, entrambi fanno fallire i test (quindi i test li rilevano):
  - `all` → `any` nella riga `modules/voice/stt.py:151`: 2 test falliti;
  - «niente divisione in frasi» (`return False`): 3 test falliti.
- Ho ripristinato il file dopo ogni mutante: nessuna modifica rimasta fuori dallo staging.

Il diff non tocca la storia dei messaggi né `_get_window`, non simula l'output dei tool e non cambia i provider.

**Riserve ancora aperte da prima**: R-764-2-M2 BASSA (su Telegram un vocale «Grazie di cuore» ora riceve «non ho capito»), R-761-4 COSMETICA. Questo diff non ne aggiunge.

**Cosa non ho verificato**: come Whisper mette davvero punteggiatura e spazi tra le frasi su audio reale (per esempio crediti e saluto senza punto in mezzo). Serve la prova sul Mac.

**Memoria**: ho aggiunto la riga #769-M2 in /home/user/Gas-filtro2/.claude/agents/memoria_revisore.md, senza lezioni nuove, e l'ho messa in staging con `git -C /home/user/Gas-filtro2 add`. Non ho fatto commit.

### Review #767-M2 (seguito di #766-M2) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #767-M2 (segue la #766-M2) sul diff staged di /home/user/Gas-filtro2. Il problema dei saluti con la virgola (R-766-1) è chiuso, ma il nuovo limite di 8 parole lascia passare di nuovo alcune allucinazioni: è la riserva MEDIA R-767-1-M2 qui sotto.

**Elementi del diff esaminati**
- `modules/voice/stt.py:133` — le frasi intere ora si confrontano anche senza la punteggiatura interna, e l'elenco ha in più «grazie mille e alla prossima» e «grazie mille a tutti e alla prossima». Rischio esaminato: che il confronto senza punteggiatura scarti anche richieste vere. Prove: «Grazie, e alla prossima!», «Grazie mille, e alla prossima», «Grazie, per l'ascolto», «Iscriviti, al canale» vengono tutte scartate. Esito: ok, R-766-1-M2 chiusa.
- `modules/voice/stt.py:128` — le parti note (`_ALLUCINAZIONI_PARTI`) fanno scartare la frase solo se ha al massimo `_PARTI_MAX_PAROLE` = 8 parole. Il limite vale anche in `_motivo_incerta` (`modules/voice/stt.py:152`). «Gas, cerca chi ha fatto i sottotitoli a cura di Rai per il film» passa. Il problema: le allucinazioni COMPOSTE, cioè una riga di crediti più un saluto, superano le 8 parole e ora arrivano al cervello («Sottotitoli creati dalla comunità Amara.org. Grazie per la visione.», «Sottotitoli a cura di QTSS. Grazie a tutti per la visione.»). Esito: **riserva MEDIA R-767-1-M2**, non bloccante. Proposta: togliere la parte nota dal testo e scartare se quello che resta è vuoto o è a sua volta un'allucinazione.
- `tests/test_unit_voice_stt.py:1399` — il test con la richiesta lunga dei «sottotitoli a cura di Rai». Esito: ok, ma manca un test per la frase composta crediti + saluto.

**Test e mutante**: suite voice_stt + voice_server + telegram_voce + voce_ascolto: 746 passed. Mutante «tolto il limite di parole»: 1 test fallisce.

**Riserve aperte**: R-767-1-M2 (MEDIA); R-764-2-M2 (BASSA); R-761-4 (COSMETICA).

**Cosa non ho verificato**: quanto spesso Whisper produce davvero le frasi composte crediti + saluto. Serve audio reale sul Mac.

**Memoria**: riga #767-M2 e una lezione nuova (con un tetto di lunghezza a un filtro per sottostringa, provare l'unione di due frasi già nell'elenco), in staging.

### Review #766-M2 (seguito di #764-M2) — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Review #766-M2 (segue la #764-M2) sul diff staged di /home/user/Gas-filtro2 (branch fix/voce-filtro2-m2). R-764-1-M2 è chiusa. Ho controllato solo la parte nuova del diff.

**Elementi del diff esaminati**
- `modules/voice/stt.py:52`: l'elenco `_PAROLE_DEI_SALUTI` di oggi non contiene più «prossimo», «prossima», «ancora», «il», «video», «alla», «al». Restano «la», «per», «di», «l», «a», «e». «Grazie, la prossima.» passa lo stesso, perché «prossima» non è più nell'elenco. Esito: ok.
- `modules/voice/stt.py:61`: le chiusure tipiche ora sono frasi intere in `_ALLUCINAZIONI_INTERE`. Il confronto toglie la punteggiatura solo ai bordi. Restano scartate «Grazie a tutti e alla prossima.», «Alla prossima.», «Grazie per aver guardato il video.», «Grazie di cuore.», «Grazie, grazie.», «Grazie mille a tutti.»; passano «Grazie, il prossimo.», «Grazie, la prossima.», «Grazie, ancora.», «Grazie, il video.»; passano anche «Grazie, e alla prossima!» e «Grazie mille e alla prossima». Esito: **riserva BASSA R-766-1-M2**.
- `tests/test_unit_voice_stt.py:1395`: i 4 casi di R-764-1 stanno nel test delle richieste che devono passare. Esito: ok.

**Test e mutante**: `-k "filtro2 or allucin"`: 59 passed. Mutante «ancora rimesso in `_PAROLE_DEI_SALUTI`»: 1 test fallito.

**Riserve aperte**: R-766-1-M2 (BASSA); R-764-2-M2 (BASSA); R-761-4 (COSMETICA).

**Memoria**: riga #766-M2 in staging.

### Review #764-M2 — verdetto integrale

VERDETTO: APPROVATO CON RISERVE

Ho fatto la review #764-M2 sul diff staged di /home/user/Gas-filtro2 (branch fix/voce-filtro2-m2, head 8b11ba8). Prima ho letto CLAUDE.md (sez. 5), reports/stato_progetto.md (in modo mirato) e la memoria del revisore.

**Elementi del diff esaminati**
- `modules/voice/stt.py:121` — nuovo ramo di `allucinazione()`: la frase è scartata se contiene almeno un «grazie» e tutte le parole sono nell'elenco `_PAROLE_DEI_SALUTI`. Sonde: «Grazie Gas», «Grazie a te.», «Grazie, a domani», «Grazie, per oggi è tutto», «grazie e basta» passano; «Ciao» e «Buonanotte.» passano. Esito: **riserva** (R-764-1).
- `modules/voice/stt.py:67` — l'elenco `_PAROLE_DEI_SALUTI` contiene anche «il», «la», «per», «di», «prossimo/prossima», «ancora», «video». «Grazie, il prossimo.», «Grazie, la prossima.», «Grazie, ancora.» e «Grazie, il video.» risultano allucinazioni. Esito: **riserva BASSA R-764-1-M2**.
- `modules/voice/stt.py:59` — «ciao a tutti» e «ciao ciao a tutti» aggiunti; tolta «sottotitoli a cura di», che resta coperta dall'elenco delle frasi parziali. Esito: ok.
- `modules/voice/server.py:233` — `seguito_da_scartare` scarta le frasi fatte solo di intercalari (elenco `_INTERCALARI` a `modules/voice/server.py:220`). «Niente.» da solo era già scartato prima; cambiano solo le frasi di più intercalari. Scartare vuol dire chiudere il seguito senza turno (`modules/voice/server.py:802`). «Niente, annulla», «Allora sì» e «Boh, dimmi tu» passano. Esito: ok.
- Contesto: `modules/voice/stt.py:138` — `_motivo_incerta` chiama `allucinazione()`, quindi il filtro vale anche per il bot Telegram. Esito: **riserva BASSA R-764-2-M2**.

**Test e mutanti**: suite voice_stt + voice_server + telegram_voce: 429 passed. Mutanti: requisito «almeno un grazie» tolto (2 falliti), `all` → `any` (2 falliti), ramo degli intercalari tolto (5 falliti).

**Riserve**: R-764-1-M2 (BASSA), R-764-2-M2 (BASSA), R-761-4 COSMETICA.

Wall of Shame: il diff non tocca la history né `_get_window`, non simula output di tool e non cambia guardrail o provider.

**Cosa non ho verificato**: il comportamento dal vivo sul Mac con il microfono. Non ho provato nemmeno parole con accenti fuori dalla regex `_PAROLA`.

**Memoria**: riga #764-M2 in staging.

## §5 DELTA TEST DEL MOTORE

- Dopo 48b605f: `python -m pytest -q tests/test_unit_voice_server.py` 221 passed.
- gas.py non toccato dalla PR (dopo il merge coincide con main). Test nuovi: `test_filtro2_varianti_dei_saluti` (23 casi), `test_filtro2_le_richieste_passano` (19), `test_filtro2_seguito_solo_intercalari` (9).
- Dopo la correzione V-1 bot #373: `tests/test_unit_voice_stt.py` 177 passed (181 alla review #775); `tests/test_unit_telegram*.py` 74 passed.
- Dopo il merge di main: `tests/test_unit_voice_stt.py tests/test_unit_telegram*.py` 255 passed; `python tests/test_unit_kernel.py` 1134 PASS, 1 FAIL (T31g, fastembed assente in questo ambiente: lo stesso FAIL c'è su main). Il revisore #777 ha rieseguito voice_stt+voice_server+notte: 599 passed.
- Prima della correzione (2f31b66): suite voce `-k "audit or not browser"` 751 passed, 25 deselected (riprodotto dalla verifica esterna #373).

## §6 STATO CI

CI NON VERIFICATA con `gh` (non autenticato nel cloud).
- Head precedente 2f31b66: `handoff-check` success; `verifica-bot` failure (finding di gravità media, corretto in 789ade7); `unit-suite` in corso alla lettura.
- Head 4559e23: `verifica-bot` failure (V-1 di gravità media, corretta in 48b605f).
- Nuovi commit (48b605f e fine-task): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-764-1-M2 BASSA, R-766-1-M2 BASSA, R-767-1-M2 (gravità media): CHIUSE (438704b, review #766/#767/#769-M2).
- V-1 BASSA del bot su #369 (parti note in una richiesta lunga): CHIUSA per le richieste di oltre 8 parole; quelle di 8 o meno con una parte nota restano scartate (limite dichiarato, V-1/V-3 verifica esterna #373, non regressione).
- V-1 del bot #373 (gravità media): CHIUSA (789ade7, review #774/#775-M2). R-774-2-M2 BASSA, R-774-3-M2 BASSA: CHIUSE (review #775-M2).
- R-774-1-M2 BASSA: «Scarica i sottotitoli a cura di Rai, grazie mille.» scartata (vedi §0.3).
- R-775-1-M2 BASSA: le chiusure con apostrofo («grazie per l'ascolto») non contano nel controllo di fine frase.
- R-774-4-M2 COSMETICA, R-775-2-M2 COSMETICA (nessun test per «;»).
- R-764-2-M2 BASSA: su Telegram un vocale «Grazie di cuore» ora riceve «Non ho capito bene il vocale» (allarga R-761-1).
- R-761-4-M2 COSMETICA: «grazie» nell'elenco delle risposte brevi del seguito non viene più raggiunto.
- V-1 del bot #373 su 4559e23 (gravità media): CHIUSA (48b605f, review #780-M2). Nella review #764-M2 (sotto, integrale) la frase ««Niente.» da solo era già scartato prima» è FALSA: su main «Niente.» passava; ora passa di nuovo.
- Bot #373 su 4559e23, V-2 BASSA: il tetto di 8 parole vale per ogni frase dopo la divisione, quindi una richiesta divisa in frasi corte con parti note («Trovami i sottotitoli a cura di Rai. Poi i sottotitoli creati da Netflix.») viene scartata (estende R-774-1-M2).
- Verifica esterna #373: V-2 BASSA (nessun fix, coerente con l'intento), V-3 COSMETICA.
- Non verificato: come Whisper punteggia davvero le frasi su audio reale (prova sul Mac).
