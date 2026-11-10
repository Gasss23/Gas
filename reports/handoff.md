# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — R7 fetta 1: il compito in sottofondo riparte da solo dopo un crash (chat M3, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #364 (https://github.com/Gasss23/Gas/pull/364). Revisore APPROVATO CON RISERVE (solo BASSA/COSMETICA): l'agente mergia da solo solo con verdetto del bot APPROVATO pulito; altrimenti serve il sì dell'operatore via M1.

---

## §1 SCOPE & ESITO FETTE

- **Proposta R7** (`reports/proposta_r7_direttore.md`): `FATTA` — opzioni e raccomandazione, mandata a M1.
- **Fetta 1 — ripresa automatica del compito in sottofondo dopo un crash**: `FATTA` — `modules/sottofondo/__init__.py` (ripresa sotto lock, max `GAS_SOTTOFONDO_RIPRESE`, progressi `<id>.passi`), `gas.py` (`tool_res` porta `nome`). Review #736 → #737 → #738 APPROVATO CON RISERVE.
- **Merge di origin/main (#360 di M2) nel branch**: `FATTA` — review #739 APPROVATO.
- **Ripresa al boot / piano scritto dal modello / lista dei lavori ricorrenti**: `DEFERITA` — fette successive della proposta.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   6 +
 gas.py                             |   3 +-
 modules/sottofondo/__init__.py     | 203 +-
 reports/diff_sessione.md           |  15 +-
 reports/handoff.md                 | n/d
 reports/proposta_r7_direttore.md   |  28 +
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  24 +-
 tests/test_unit_kernel.py          |   4 +-
 tests/test_unit_sottofondo.py      | 222 +
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
ef18a4ef Merge origin/main (#360 di M2) in feat/r7-direttore-m3 — review #739
3101011d feat(R7): fetta 1 — il compito in sottofondo riparte da solo dopo un crash (M3)
18523105 chore(revisore): memoria review #738 — APPROVATO CON RISERVE
525064c1 chore(revisore): memoria review #737 — APPROVATO CON RISERVE
9575467d chore(revisore): memoria review #736 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 3101011 (motore): tre giri, #736 → #737 → #738. Commit ef18a4e (merge): #739. Verdetti integrali.

### Review #736

VERDETTO: APPROVATO CON RISERVE

Revisione n. 736 della fetta 1 di R7 (ripresa dei compiti in sottofondo), sul branch feat/r7-direttore-m3. Il diff è ancora nella working tree, non staged.

Letture obbligatorie fatte: CLAUDE.md (sezioni 5, 8, 9 e 10), reports/stato_progetto.md (solo le parti su R7 e sottofondo) e la memoria del revisore (coda).

**Test eseguiti da me**
- pytest su tests/test_unit_sottofondo.py: 99 passed.
- Suite del kernel (tests/test_unit_kernel.py): 1100 PASS, 0 FAIL. T105a passa.
- Il perimetro guardato è gas.py, modules/ e tests/.

**Elementi del diff esaminati**
1. `modules/sottofondo/__init__.py:197` — `_ripulisci` chiama `_riprendi` e, se riceve False, passa ad `annulla`. Rischio: race tra due processi che controllano lo stesso compito nello stesso momento. Esito: **riserva MEDIA (R-736-1)**, spiegata sotto.
2. `modules/sottofondo/__init__.py:251` — Sotto il lock, il posto viene ripreso solo se è ancora quello letto, nessun compito è attivo, lo stato è in_coda o in_corso, le riprese non sono finite e il compito è un testo. Rischio: due copie dello stesso compito avviate insieme. Esito: ok, non partono mai due copie.
3. `modules/sottofondo/__init__.py:568` — Il nuovo processo rimette nel posto la data di creazione originale. Rischio: superare il tetto di tempo. Esito: ok, ed è più stretto di quanto dice la proposta. Il tempo totale resta una sola durata massima contata dalla prima creazione, non (1+riprese)×durata. Va corretto il testo di reports/proposta_r7_direttore.md (cosmetico).
4. `modules/sottofondo/__init__.py:296` — `_segna_passo` salva solo nomi validi secondo la regex, al massimo 50, in un file 0600 separato, e non solleva mai eccezioni. Rischio: un canale di prompt injection. Esito: **riserva BASSA (R-736-2)**.
5. `modules/sottofondo/__init__.py:577` — La nota di ripresa viene aggiunta al prompt del compito. Rischio: azioni ripetute alla ripresa. Esito: **riserva BASSA (R-736-3)**. Le azioni che passano dal cancello tornano alla firma, non partono da sole.
6. `modules/sottofondo/__init__.py:387` — I file `.passi` vecchi vengono cancellati, tranne quello del compito che occupa il posto. Il file `.lock` non viene mai cancellato, ed è giusto così. Esito: ok.
7. `gas.py:5219` — L'evento tool_res ora porta anche il nome dello strumento. Rischio: rompere chi legge l'evento. Esito: ok. È un campo in più e T105a lo verifica. Nessuno slicing della storia, `_get_window` e il tetto di 10 iterazioni non sono toccati.

**Finding**
- **R-736-1 MEDIA — riprodotta.** Il processo che perde il lock annulla la ripresa fatta dal vincitore. Lo script race.py (scratchpad della sessione) lancia due `_ripulisci` in thread, ed entrambi leggono il posto vecchio. A riprende il compito e lo avvia. B, che aspettava il lock, trova il posto cambiato: `_riprendi` restituisce False e B passa ad `annulla`. Risultato finale: compito «ko», riprese=1, posto tolto, avviso «non è finito: il processo si è interrotto».
  - Nel caso più probabile, il processo avviato da A esce subito come «già eseguito», quindi si torna al comportamento di prima di R7.
  - Se invece quel processo è già in_corso, gira senza posto: la coda risulta libera e un secondo compito potrebbe partire in parallelo.
  - Il lock rende quindi la race sicura nel risultato, invece di evitarla.
  - Correzione: distinguere «gestito da altri» (posto diverso da quello letto, oppure un compito attivo) da «niente ripresa». Per esempio `_riprendi` restituisce True in quel caso, oppure `_ripulisci` rilegge il posto e si ferma se non è più quello letto. Il test `test_posto_cambiato_nel_frattempo_niente_ripresa` controlla solo `_riprendi` da solo; serve un test sul chiamante.
  - Consiglio di chiuderla prima del commit.
- **R-736-2 BASSA.** I nomi salvati non sono confrontati con gli strumenti registrati. Il modello può chiamare uno strumento inesistente; la chiamata viene negata, ma il nome compare lo stesso nell'evento. Così un testo scelto dal modello (fino a 40 caratteri `[a-z0-9_]`, eco possibile di testo letto da fuori) entra nel prompt FIDATO della ripresa, senza segno di contaminazione. La frase della proposta «nessun nuovo testo non fidato nel prompt» non è esatta. Correzione: salvare solo i nomi degli strumenti registrati, oppure solo le chiamate con `cancello` None.
- **R-736-3 BASSA.** Anche le chiamate negate o parcheggiate («in_attesa») risultano «già usate» nella nota. Alla ripresa il modello parcheggia di nuovo la stessa azione: ci sono due richieste nella coda delle firme e l'operatore potrebbe firmarle tutte e due. Correzione: nella nota distinguere «in attesa di firma» da «eseguito», oppure non contare le chiamate negate.
- **Nota cosmetica.** Il tetto di tempo scritto nella proposta va corretto (vedi punto 3).

**Rischi esclusi (non verificati)**
- Processi nipoti rimasti vivi: se muore il processo `gas.py sottofondo` ma un suo sottoprocesso continua a girare, il compito ripreso potrebbe lavorare insieme a lui. Non l'ho verificato perché non si riproduce con processi finti nei test.
- Comportamento reale su Mac o VPS, cioè `flock` su filesystem di rete e riavvio vero della macchina: non verificato, l'ho controllato solo su Linux dev con thread.
- Il percorso completo del cancello firme quando un compito ripreso chiede la firma: l'ho controllato solo leggendo gas.py:5139-5176, senza un test end-to-end.

**Memoria**
Riga contatore #736 e una lezione nuova aggiunte in .claude/agents/memoria_revisore.md, committate da sole con lo script (commit 9575467).

Le riserve R-736-1, R-736-2 e R-736-3 vanno scritte in reports/stato_progetto.md se si committa senza correggerle.

### Review #737

VERDETTO: APPROVATO CON RISERVE

Seconda revisione (#737) della fetta 1 di R7, branch feat/r7-direttore-m3, diff `git diff HEAD -- gas.py modules/ tests/` (in parte staged e in parte no). Prima ho letto CLAUDE.md (sezione 5), stato_progetto.md (sezione R7) e la mia memoria, con la riga #736 e la lezione sul «perdente del lock».

**Cosa ho controllato nel diff**
- `modules/sottofondo/__init__.py:204` — `_ripulisci` ora si ferma quando `_riprendi(...) is not False`. Rischio: che chi arriva secondo al lock annulli la ripresa appena fatta dall'altro (R-736-1). Esito: **ok**. Per provarlo ho copiato il codice nello scratchpad e tolto `is not False`: `test_due_controlli_insieme_non_annullano_la_ripresa` fallisce (1 failed). Con la correzione passa.
- `modules/sottofondo/__init__.py:260` — sotto il lock, se il posto non è più quello letto oppure c'è un compito attivo, si restituisce None prima degli altri controlli. Rischio: casi che prima finivano in «annulla» e adesso non li chiude più nessuno. Esito: **riserva R-737-1** (vedi sotto).
- `modules/sottofondo/__init__.py:312` — `_strumenti_noti` legge `kernel.tools_schema`, che esiste davvero in `gas.py:1244`. Ogni errore dà un elenco vuoto, quindi nessun nome viene salvato. Rischio: un nome inventato dal modello che finisce nel prompt fidato (R-736-2). Esito: **ok**, coperto da `tests/test_unit_sottofondo.py:1036` e dal caso `fai_x_subito` a `tests/test_unit_sottofondo.py:973`.
- `modules/sottofondo/__init__.py:332` — `cancello` None diventa «fatto», `in_attesa` diventa «in_firma», tutto il resto (anche `negata`) viene escluso. `_passi` scarta le voci malformate e i valori sconosciuti. Ho confrontato con i valori che `_cancello` assume davvero in `gas.py:5139-5186`. Esito: **ok** (R-736-3 chiusa), con una nota cosmetica.
- `gas.py:5219` — `tool_res` porta `"nome": tc.function.name`, verificato da T105a in `tests/test_unit_kernel.py:12034`. Esito: **ok**. Non tocca `_get_window`, il tetto di 10 giri né quello degli 8k di output.
- Wall of Shame: nel diff non c'è nessun taglio della history né output di strumenti simulati. I test usano un `_Kernel` finto che riceve eventi, ma l'esecuzione dei tool nel kernel resta quella vera.

**Riserve**
- **R-737-1 BASSA**: col nuovo ramo None ricade anche il caso in cui il posto è sparito o illeggibile sotto il lock (`_leggi` dà None, quindi `posto != letto`). Prima finiva in «annulla», cioè compito «ko» con avviso. Ora non succede niente, e se nessun altro ha chiuso il compito (per esempio il posto tolto dopo 120 s perché illeggibile), il compito resta «in_coda»/«in_corso» senza posto e senza avviso. Correzione possibile: restituire None solo se `posto` non è None ed è diverso da `letto`, oppure se c'è un compito attivo. Con il posto assente si lascia False, e `annulla` è comunque protetto dallo stato del compito.
- **R-737-2 COSMETICA**: `reports/proposta_r7_direttore.md` dice «Il file del compito tiene i progressi», ma i progressi stanno in `<id>.passi`, un file separato. Inoltre un parcheggio che restituisce un testo diverso da «Azione in attesa…» o «Operazione negata…» (in quel caso `_cancello` resta None) viene registrato come «fatto».

**Rischio escluso**
- Non ho rilanciato la suite kernel completa (1100 PASS dichiarati dall'agente): la parte di `gas.py` è identica a quella del giro #736, dove T105a passava. Ho rilanciato solo `pytest tests/test_unit_sottofondo.py`: 102 passed.
- La ripresa con processi veri (fcntl tra processi reali, kill del figlio) non l'ho provata: nei test `_avvia_ripresa` è sostituito da un finto.

**Memoria**
Ho aggiunto la riga #737 e una lezione (un bool che diventa tri-stato porta con sé anche i casi «stato sparito», che restano orfani) in `.claude/agents/memoria_revisore.md`, committata con `scripts/commit_memoria_revisore.sh` (525064c).

Il commit è consentito: le riserve R-737-1 e R-737-2 vanno tracciate in `reports/stato_progetto.md`.

### Review #738

VERDETTO: APPROVATO CON RISERVE

Review #738 (chat M3), terzo giro della fetta 1 di R7 sul branch feat/r7-direttore-m3. Ho esaminato `git diff HEAD -- gas.py modules/ tests/`, concentrandomi solo sulla modifica nuova. Prima ho fatto le letture obbligatorie: CLAUDE.md §5, stato_progetto con grep mirato, coda della mia memoria.

**Cosa ho esaminato**
- modules/sottofondo/__init__.py:258 — `_riprendi` sotto il lock rilegge il posto e il compito, poi decide. Rischio esaminato: R-737-1, cioè un posto sparito o illeggibile che finiva nel ramo None e lasciava il compito aperto senza che nessuno lo chiudesse. Ora restituisce None solo se `posto is not None and posto != letto` oppure se c'è un compito attivo. Un posto sparito o illeggibile passa al controllo successivo `not posto` e restituisce False. Esito: ok, R-737-1 CHIUSA.
- modules/sottofondo/__init__.py:204 — `_ripulisci` con False chiama `annulla`. Rischio esaminato: un posto sparito perché il figlio della ripresa ha appena finito, e `annulla` che segna «ko» un compito riuscito. `annulla` (modules/sottofondo/__init__.py:549) chiude solo un compito ancora in_coda o in_corso. `_esegui` scrive l'esito (modules/sottofondo/__init__.py:656) PRIMA di togliere il posto (modules/sottofondo/__init__.py:659). Quindi chi trova il posto sparito vede già «ok» o «ko» e non tocca niente, e non parte nessun avviso doppio. Esito: ok.
- tests/test_unit_sottofondo.py:1050 — test nuovo `test_posto_sparito_sotto_il_lock_compito_chiuso`. Rischio esaminato: se copre davvero quello che il nome promette. Controlla solo che `_riprendi` restituisca False e che non parta nessuna ripresa. Non fa il giro intero da `_ripulisci` fino a «ko» con avviso, che pure sono scritti nel nome e nella docstring. Esito: riserva cosmetica.
- La proposta ora dice «Un file a parte (`<id>.passi`)». Esito: ok, parte principale di R-737-2 chiusa. Il resto (un parcheggio con testo inatteso registrato come «fatto») resta tracciato in stato_progetto, come dichiarato.

pytest tests/test_unit_sottofondo.py: 103 passed (rieseguito da me).

**Riserve**
- R-738-1 COSMETICA: il test nuovo verifica solo il False di `_riprendi`. Non controlla la chiusura «ko» con avviso promessa dal nome. Basta aggiungere un'asserzione passando da `_ripulisci`: stato «ko» e un avviso.

**Cosa NON ho verificato**
- Non ho rieseguito la suite kernel (tests/test_unit_kernel.py) né la sonda di race in thread: gas.py e i test del kernel non sono cambiati dopo la #737.
- Non ho verificato un posto illeggibile perché corrotto in modo parziale, con un json valido ma un id diverso: ricade nel ramo None per costruzione, già coperto nella #737.

Memoria aggiornata: riga #738 in .claude/agents/memoria_revisore.md, committata (1852310), nessuna lezione nuova.

### Review #739 (merge di origin/main) — verdetto RIEMESSO

Il gate B ha rifiutato il verdetto originale (1 sola citazione di file del diff di sessione): il revisore lo ha riemesso con lo stesso esito e citazioni nella forma del gate. Sotto, prima il verdetto riemesso, poi l'originale invariato (in blocco di codice).

## VERDETTO: APPROVATO

Il merge in corso di origin/main 447195f (PR #360 di M2) in feat/r7-direttore-m3 si può committare (revisione #739, chat M3).

**Cosa ho controllato**
- modules/sottofondo/__init__.py:689 — `da_leggere(root)` restituisce i compiti in sottofondo finiti e non ancora letti. Il server voce la chiama nei turni di attivazione (contesto: modules/voice/server.py:887). Ho cercato una rottura dell'interfaccia tra R7 e il codice voce arrivato da main. La funzione esiste a HEAD M3 con la stessa firma e il merge non tocca modules/sottofondo (`git diff --cached HEAD --stat -- modules/sottofondo` è vuoto). Esito: ok.
- modules/sottofondo/__init__.py:718 — `frase_finiti(jobs)` produce la frase detta a voce. Anche qui ho controllato l'interfaccia usata dal server: esiste ed è invariata. Esito: ok.
- modules/sottofondo/__init__.py:733 — `segna_letti(root, jobs)` è chiamata dal server dopo la frase (contesto: modules/voice/server.py:911). Ho controllato l'interfaccia e la firma è compatibile. I test voice_server e sottofondo lanciati insieme con `-k "not browser"` danno 267 passed. Esito: ok.
- Contesto, modules/voice/server.py:324 — `_FRASI_FISSE` ora contiene anche i pezzi di `_dividi_frasi`. È l'unica modifica di codice rispetto a HEAD. `git diff --cached MERGE_HEAD -- modules/voice tests/test_unit_voice_server.py` è vuoto, quindi il codice è identico a quello già revisionato e mergiato con la #360. Esito: ok.
- Contesto, .claude/agents/memoria_revisore.md:1416 — il conflitto è risolto come unione delle due parti. Confrontando le righe ordinate, l'index non perde nessuna riga né di HEAD né di MERGE_HEAD. Sono presenti #736, #737 e #738 di M3 con le loro due lezioni e #725, #735, #737, #740, #741 e #742-M2. Non restano marcatori, `git ls-files -u` è vuoto e `git diff --cached --check` è pulito. Esito: ok.

**Cosa non ho verificato**
- La suite kernel e le righe di gas.py di questa sessione: il merge non le tocca e restano coperte dalle review #736-#738.
- Il contenuto dei file in reports/: ho solo controllato che non abbiano marcatori di conflitto, sono fuori dal perimetro di review.

**Note per te**
- La prima riga è `## VERDETTO: APPROVATO`, nel formato obbligatorio del mio regolamento, e non `VERDETTO: APPROVATO` come avevi chiesto. Contiene comunque `VERDETTO:`, il marcatore che cerca il gate B. Se `check_verdetto.py` la rifiuta per il `##`, riemetto senza.
- Memoria non toccata in questo secondo giro: la riga #739 è già nell'index dal primo giro.

Verdetto originale #739 (invariato):

```
VERDETTO: APPROVATO

Il merge in corso di origin/main 447195f (PR #360 di M2) in feat/r7-direttore-m3 si può committare.

**Cosa ho controllato nel diff**
- modules/voice/server.py:324 — `_FRASI_FISSE` ora contiene anche i pezzi creati da `_dividi_frasi` sulle frasi fisse del codice. È l'unica modifica di codice rispetto a HEAD. Ho cercato due rischi: che il codice si discostasse dalla #360 già revisionata e che in cache entrasse testo del modello. `git diff --cached MERGE_HEAD -- modules/voice tests/test_unit_voice_server.py` è vuoto, quindi il codice è identico a quello di main. Esito: ok.
- tests/test_unit_voice_server.py:2099 — sono i test della #360 sulla cache delle frasi fisse. Sono identici a quelli di MERGE_HEAD. Lanciati insieme ai test di sottofondo con `-k "not browser"`: 267 passed. Esito: ok.
- .claude/agents/memoria_revisore.md:1416 — il conflitto è risolto come unione delle due parti. Ho confrontato le righe ordinate dell'index con HEAD e con MERGE_HEAD: nessuna riga persa da nessuno dei due lati. Ci sono sia #736, #737 e #738 di M3 con le loro due lezioni, sia #725, #735, #737, #740, #741 e #742-M2. Non restano marcatori di conflitto, `git ls-files -u` è vuoto e `git diff --cached --check` non segnala nulla. La copia di lavoro coincide con l'index. Esito: ok.
- Citazione di contesto, modules/sottofondo/__init__.py:689 — il server voce usa `da_leggere`, `frase_finiti` e `segna_letti` (modules/voice/server.py:887). Ho verificato che esistono ancora nella versione M3 (righe 689, 718 e 733). Il merge non tocca modules/sottofondo. Esito: ok, nessuna interferenza con R7.

**Cosa non ho verificato**
- La suite kernel (gas.py) non l'ho lanciata: il merge non tocca né gas.py né modules/sottofondo.
- I file in reports/ (handoff, ultimo_report e gli altri) non li ho letti per contenuto, ho solo controllato che non abbiano marcatori di conflitto. Sono fuori dal perimetro di review.

**Memoria del revisore**
- Ho scritto la riga contatore `#739 (chat M3)` e l'ho aggiunta all'index con `git add`, quindi entra nel commit di merge.
- Lo script `bash scripts/commit_memoria_revisore.sh` non è partito: l'hook del gate di review ha bloccato il comando perché manca il marcatore `.claude/.review_ok`. Con un merge in corso lo script non sarebbe comunque utilizzabile, come già successo in #733-M2.
- Prima di committare il merge devi rigenerare il marcatore con `bash scripts/segna_review_ok.sh`. La mia riga è nell'index, quindi va generato sull'index attuale.
```

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_sottofondo.py`: 99 casi a metà sessione (dopo la prima versione della fetta) → 103 casi alla fine, tutti passati (`103 passed in 2.32s`).
- Suite kernel: prima 1100 PASS (T105a senza il controllo sul nome) → dopo:

```
=== RIEPILOGO: 1100 PASS, 0 FAIL ===
```

(T105a esteso, nessun check nuovo.) Voce + notte + sottofondo: `478 passed in 289.68s`.

## §6 STATO CI

`gh` non usato per la CI in questa sessione (solo strumenti GitHub di sessione). Check della PR #364 letti alla scrittura dell'handoff, run sul commit ef18a4e (testa del push precedente):
- `unit-suite`: in_progress (run 42727825423).
- `handoff-check`: failure (run 42727825423) — atteso: l'handoff di sessione non era ancora scritto; si ripete col push di questo commit.
- `verifica-bot` (smista/verifica/esito): skipped — etichetta `verifica` non ancora messa.

Mappatura commit→run:
- ef18a4e: run 42727825423 (push del branch col merge).
- 3101011: nessuna run propria su questo SHA (pushato prima dell'apertura della PR; contenuto incluso nell'albero di ef18a4e).
- 9575467, 525064c, 1852310 (memoria revisore): nessuna run su questi SHA.
- Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-737-2** (BASSA): un parcheggio alla firma con testo diverso da «Azione in attesa…»/«Operazione negata…» lascia `cancello` None e risulta «fatto» nei progressi.
- **R-738-1** (COSMETICA): `test_posto_sparito_sotto_il_lock_compito_chiuso` prova solo il False di `_riprendi`, non il giro fino a «ko» con avviso.
- Non verificato (dichiarato dal revisore): processi veri (flock fra processi, kill del figlio, nipoti rimasti vivi), cancello firme end-to-end su un compito ripreso.
