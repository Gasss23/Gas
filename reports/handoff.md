# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — R7 fetta 1: il compito in sottofondo riparte da solo dopo un crash (chat M3, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #364 (https://github.com/Gasss23/Gas/pull/364): contiene una correzione di SICUREZZA al cancello (`.gas_sottofondo/` mai scrivibile, dall'audit notturno di M1), quindi serve il sì dell'operatore via M1 anche col verdetto del bot APPROVATO. Revisore APPROVATO CON RISERVE (solo BASSA/COSMETICA); bot su a7eb3fc APPROVATA con riserve BASSE.

---

## §1 SCOPE & ESITO FETTE

- **Proposta R7** (`reports/proposta_r7_direttore.md`): `FATTA` — opzioni e raccomandazione, mandata a M1.
- **Fetta 1 — ripresa automatica del compito in sottofondo dopo un crash**: `FATTA` — `modules/sottofondo/__init__.py` (ripresa sotto lock, max `GAS_SOTTOFONDO_RIPRESE`, progressi `<id>.passi`), `gas.py` (`tool_res` porta `nome`). Review #736 → #737 → #738 APPROVATO CON RISERVE.
- **Bot #364 su dc6c25a (NON approvata, V-1 MEDIA + V-2 BASSA)**: `FATTA` — avviso a ogni ripresa, comando `python gas.py sottofondo-ferma` (segno `<id>.ferma` sotto il lock, kill solo del nostro figlio, compito «ko»), niente ripresa oltre la durata dalla prima creazione. Review #743 → #744 → #745 APPROVATO CON RISERVE (commit 47c8aa3).
- **Verifica esterna #364 (su dc6c25a)**: APPROVATO CON RISERVE, nessuna ALTA/MEDIA (https://github.com/Gasss23/Gas/pull/364#issuecomment-6755289640); V-1 BASSA tracciata in stato_progetto.
- **Bot #364 2° giro (a7eb3fc)**: APPROVATA (check verifica-bot success), riserve BASSE V-1 (avviso di ripresa e tetto notifiche) e V-2 (cartella di lancio di `sottofondo-ferma`), COSMETICA V-3 (descrizione PR, corretta). Verifica esterna 2° giro: APPROVATO CON RISERVE, nessuna ALTA/MEDIA (https://github.com/Gasss23/Gas/pull/364#issuecomment-6755522719). Riserve in stato_progetto.
- **Audit notturno (M1): `.gas_sottofondo/` scrivibile senza firma**: `FATTA` — denylist + livello 3 in `modules/gate/gate.py` (commit 1537f0c), test gate e kernel T6s. Review #746 APPROVATO CON RISERVE.
- **Merge di origin/main nel branch**: `FATTA` — #360 di M2 (review #739 APPROVATO), #362 di M4 (solo report e memoria del revisore, nessun codice), #361 (review #747 APPROVATO).
- **Ripresa al boot / piano scritto dal modello / lista dei lavori ricorrenti**: `DEFERITA` — fette successive della proposta.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  16 +
 gas.py                             |   8 +-
 modules/gate/gate.py               |   4 +
 modules/sottofondo/__init__.py     | 294 +-
 reports/diff_sessione.md           |  22 +-
 reports/handoff.md                 | n/d
 reports/proposta_r7_direttore.md   |  28 +
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  33 +-
 tests/test_unit_gate.py            |   7 +
 tests/test_unit_kernel.py          |  13 +
 tests/test_unit_sottofondo.py      | 358 +
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile al momento della scrittura; riga di totale tolta. BASE = 3f08352 (merge-base con origin/main dopo il merge della #361).

## §3 GIT LOG --ONELINE (sessione)

```
5c3af803 Merge origin/main (#361) in feat/r7-direttore-m3 — review #747
1537f0c7 fix(gate): .gas_sottofondo mai scrivibile né leggibile da Gas (audit notturno, R7, M3)
dd7b36c1 chore(revisore): memoria review #746 — APPROVATO CON RISERVE
a7eb3fc0 docs(fine-task): R7 fetta 1 — correzioni del bot #364 (avviso alla ripresa, sottofondo-ferma, tetto di tempo), merge della #362 (M3)
00499543 Merge origin/main (#362 di M4) in feat/r7-direttore-m3 — solo report e memoria del revisore
47c8aa3d fix(R7): bot #364 — avviso a ogni ripresa e comando sottofondo-ferma; tetto di tempo dalla prima creazione (M3)
30720bba chore(revisore): memoria review #745 — APPROVATO CON RISERVE
d4e78289 chore(revisore): memoria review #744 — APPROVATO CON RISERVE
aec71956 chore(revisore): memoria review #743 — APPROVATO CON RISERVE
dc6c25aa docs(fine-task): R7 fetta 1 — ripresa dei compiti in sottofondo dopo un crash (M3), PR #364
ef18a4ef Merge origin/main (#360 di M2) in feat/r7-direttore-m3 — review #739
3101011d feat(R7): fetta 1 — il compito in sottofondo riparte da solo dopo un crash (M3)
18523105 chore(revisore): memoria review #738 — APPROVATO CON RISERVE
525064c1 chore(revisore): memoria review #737 — APPROVATO CON RISERVE
9575467d chore(revisore): memoria review #736 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 3101011 (motore): tre giri, #736 → #737 → #738. Commit ef18a4e (merge): #739. Commit 47c8aa3 (correzioni bot #364): tre giri, #743 → #744 → #745. Il merge 0049954 (#362) non tocca il perimetro di codice. Commit 1537f0c (sicurezza, cancello): #746. Merge 5c3af80 (#361): #747. Verdetti integrali.

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

### Review #743

## VERDETTO: APPROVATO CON RISERVE

Review #743 (chat M3): 4° giro della R7 fetta 1, correzioni ai punti del bot sulla PR #364 (V-1 e V-2). Ho letto CLAUDE.md (sez. 5, 8 e 9), le voci R7 di reports/stato_progetto.md e la mia memoria. Nel diff non c'è nessuno degli antipattern vietati (niente taglio diretto della storia, niente output di tool inventati). Il tetto di 10 giri del loop e la funzione `_get_window()` non sono toccati. Ho lanciato `pytest tests/test_unit_sottofondo.py`: 109 passati.

**Elementi del diff esaminati**
- `modules/sottofondo/__init__.py:242` — nuova `ferma()`. Scrive `<id>.ferma` PRIMA di fermare il processo, e lo ferma solo se `_identita` è True; poi `annulla` e manda l'avviso. Rischio esaminato: corsa con un `controlla` di un altro processo che, morto il figlio, prova a riprendere il compito. Il segno c'è già quando `_riprendi` lo controlla sotto lock, quindi niente ripresa, il compito si chiude «ko» col motivo «fermato dall'operatore», e un solo avviso perché `annulla` scrive solo su un compito ancora aperto. Esito: ok.
- `modules/sottofondo/__init__.py:252` — `os.killpg` solo con `_identita(pid, ident) is True`. Rischio: pid riusato da un'app dell'operatore. Con False non uccide niente (provato da `tests/test_unit_sottofondo.py:1095` con un `sleep` estraneo). Con None (manca `ps`) però non ferma il processo, `annulla` libera comunque il posto e la frase dice «fermato: non riparte». Esito: riserva R-743-2.
- `modules/sottofondo/__init__.py:305` — V-2: niente ripresa se `_nel_futuro(job)` o se il tempo dal «creato» del COMPITO supera la durata massima. `accoda` scrive sempre «creato» nel compito (`modules/sottofondo/__init__.py:565`), quindi un «creato» mancante (vale 0) si ha solo su file alterati, e lì negare la ripresa è prudente. Test: `tests/test_unit_sottofondo.py:1110`. Esito: ok.
- `modules/sottofondo/__init__.py:325` — avviso Telegram a ogni ripresa con il comando per fermarla. Rischio: crash. `_avvisa` cattura e registra ogni errore (§9). Se poi il riavvio fallisce arrivano due avvisi («lo riprendo», poi «non è finito»), accettabile. Esito: ok.
- `modules/sottofondo/__init__.py:180` — `_ripulisci` usa il motivo «fermato dall'operatore» se c'è il segno, e «oltre la durata» vince giustamente su questo. `modules/sottofondo/__init__.py:476` — pulizia dei `.ferma` vecchi, solo se non sono del posto in corso. Esito: ok.
- `gas.py:6463` — comando `sottofondo-ferma`. `ferma` non lancia mai eccezioni (try/except che scrive in gas_debug.log), e la prova da riga di comando è in `tests/test_unit_sottofondo.py:1127`. Esce con 0 anche se l'arresto fallisce. Esito: riserva cosmetica (R-743-3).

**Riserve (da tracciare in stato_progetto.md)**
- **R-743-1 BASSA (corsa)**: `ferma` non prende il lock della ripresa, e `_esegui` non ricontrolla `.ferma`. Due finestre strette in cui il «ko» scritto da `ferma` viene sovrascritto e il compito gira lo stesso:
  - (a) `_riprendi` ha già superato il controllo di `_fermato` sotto lock e riscrive il compito «in_coda» partendo dalla sua copia letta prima;
  - (b) il figlio di una ripresa, partito col posto senza pid, ha già letto il compito «in_coda» e lo riscrive «in_corso» (`modules/sottofondo/__init__.py:660-662`). In questo caso `ferma` non lo uccide nemmeno, perché il pid letto era None.

  Correzione economica: `ferma` scrive il segno e chiude il compito sotto lo stesso `flock` di `_riprendi`, e `_esegui` ricontrolla `_fermato` dopo aver scritto «in_corso» (se c'è il segno, chiude «ko» senza eseguire). Finestra di millisecondi, non bloccante.
- **R-743-2 BASSA**: con `_identita` None (niente `ps`) il processo resta vivo, il posto viene liberato (può partire un secondo compito in parallelo) e la frase a terminale e l'avviso dicono «fermato». Serve un testo onesto («segnato come fermato, il processo potrebbe essere ancora attivo»), come già fa `_ripulisci` per la durata. Nessun test copre il caso None.
- **R-743-3 COSMETICA**: se il figlio scrive «ok» un attimo prima, `ferma` stampa comunque «Compito … fermato: non riparte» (l'avviso giustamente non parte). Inoltre `gas.py sottofondo-ferma` esce sempre con 0, anche su «Arresto non riuscito».

**Rischio escluso (non verificato)**: non ho provato processi veri. In particolare: SIGTERM a un figlio vero nel mezzo di un `run_turn`, `flock` fra processi distinti, nipoti rimasti vivi nel gruppo, consegna reale dell'avviso Telegram (tetto giornaliero compreso). Non sono riproducibili nei test unitari, che sostituiscono l'avvio. Non ho rilanciato la suite del kernel (1100 PASS dichiarati dall'agente). Non ho rivisto `reports/proposta_r7_direttore.md` (fuori dal perimetro di review).

Memoria aggiornata (riga #743 (chat M3), più una lezione sul lock condiviso fra chi scrive e chi legge il segno di arresto) e committata con `scripts/commit_memoria_revisore.sh` (commit aec71956, solo .claude/agents/memoria_revisore.md). Gli altri file del diff restano non committati.

### Review #744

## VERDETTO: APPROVATO CON RISERVE

Review #744, quinto giro di R7 fetta 1 (branch feat/r7-direttore-m3). Ho letto CLAUDE.md, lo stato del progetto (stato_progetto) e la mia memoria (memoria_revisore). Ho eseguito `pytest tests/test_unit_sottofondo.py`: 111 passed.

**Elementi del diff esaminati**
- `modules/sottofondo/__init__.py:280` — `ferma` prende il lock con `_lock_esclusivo`, scrive `<id>.ferma`, fa killpg solo se `_identita` è True, poi chiama `annulla` (`annulla` non prende il lock, quindi niente deadlock). L'avviso parte fuori dal lock. Rischio esaminato: R-743-1 (concorrenza con `_riprendi`). Esito: **ok** verso `_riprendi`, che ricontrolla `_fermato` sotto lo stesso lock (`modules/sottofondo/__init__.py:341`). Esito: **riserva** verso il figlio, vedi R-744-1.
- `modules/sottofondo/__init__.py:276` — `dati = _leggi(cartella / ATTIVO)` viene letto PRIMA del lock e prima di scrivere il segno, e il pid usato per il kill (riga 283) viene da quella lettura. Rischio esaminato: lettura vecchia del pid. Esito: **riserva** (R-744-1).
- `modules/sottofondo/__init__.py:702` — `_esegui`, dopo aver scritto «in_corso», ricontrolla `_fermato` e chiude «ko» senza mandare un secondo avviso. Rischio esaminato: il figlio di una ripresa che parte dopo l'arresto. Esito: **ok**. Il mutante `if False:` viene preso da `test_figlio_della_ripresa_fermato_non_esegue` (1 failed).
- `modules/sottofondo/__init__.py:292` — se il compito è già chiuso, la frase è «era già finito» e non parte nessun avviso. Con `nostro is None` la frase e l'avviso dicono «potrebbe essere ancora attivo». Rischio esaminato: R-743-2 e R-743-3. Esito: **ok**. Lo coprono `tests/test_unit_sottofondo.py:1097` e `tests/test_unit_sottofondo.py:1146`.
- `gas.py:6463` — il comando `sottofondo-ferma` stampa la frase ed esce con 1 se `ok` è False. Rischio esaminato: crash nel comando o codice di uscita sbagliato. Esito: **ok**. `ferma` cattura ogni eccezione (§9), e `test_comando_sottofondo_ferma` lancia il comando come processo vero.
- `modules/sottofondo/__init__.py:180` — in `_ripulisci` il segno cambia il motivo in «fermato dall'operatore». Il compito è già chiuso da `ferma`, quindi `annulla` lì ritorna False e non parte un doppio avviso. Esito: **ok**.

**Riserve**
- **R-744-1 BASSA** — la finestra di R-743-1 si è ristretta ma resta aperta. Sequenza: `ferma` legge ATTIVO con pid None (posto appena preso da accoda o ripresa). Poi il figlio scrive pid e «in_corso» e controlla il segno, che non c'è ancora, quindi esegue. Poi `ferma` scrive `.ferma`, non uccide niente (usa il pid vecchio), chiude «ko», libera il posto e dice «fermato: non riparte». Risultato: il compito gira fino in fondo in silenzio, l'esito finale viene ignorato perché lo stato è già «ko», e il posto è libero, quindi un secondo compito può partire insieme. L'ho riprodotto iniettando le scritture del figlio prima del lock: lo script è race.py nello scratchpad della sessione. Correzione: dentro il lock, rileggere ATTIVO e prendere il pid DOPO aver scritto `.ferma`. Così o il pid del figlio è già visibile (e lo si ferma), o il figlio scrive dopo il segno e lo vede.
- **R-744-2 BASSA** — nessun test prova che `ferma` usi il lock. Il mutante «`fd = None`» al posto di `_lock_esclusivo` (riga 280) dà 111 passed.
- Nota, nessuna nuova riserva: con `_identita` None, `annulla` libera il posto anche se il processo forse è vivo. Questo va contro la regola di `attivo()` («nel dubbio il posto resta occupato»). Ora almeno il caso viene dichiarato all'operatore.

**Rischio escluso**: non ho verificato il comportamento con processi figli veri e un vero `os.killpg` su macOS/VPS, né `fcntl` assente (lì `_lock_esclusivo` ritorna None e si procede senza lock). Le corse le ho provate solo con iniezione deterministica in un unico processo, non con concorrenza reale fra processi.

**Memoria**: aggiunta la riga #744 e una lezione in `.claude/agents/memoria_revisore.md`, committata con lo script (commit d4e78289). Il file del motore usato per i mutanti è stato ripristinato: il diff stat è identico a prima (90 righe).

### Review #745

## VERDETTO: APPROVATO CON RISERVE

Sesto giro sul branch feat/r7-direttore-m3 (`git diff -- gas.py modules/ tests/`, 3 file). Prima ho letto CLAUDE.md §5, stato_progetto.md (riga R7) e la memoria del revisore.

**Cosa ho controllato nel codice**
- `modules/sottofondo/__init__.py:280` — `ferma` prende `_lock_esclusivo` prima di scrivere il segno `<id>.ferma` e di chiudere il compito. Rischio: deadlock, perché `annulla` viene chiamato con il lock già preso. `annulla` non prende il lock (`modules/sottofondo/__init__.py:625`), quindi il rischio non c'è. Esito: ok.
- `modules/sottofondo/__init__.py:285` — dopo aver scritto il segno si rilegge ATTIVO, e il pid si usa solo se l'id è ancora lo stesso. Rischio: resta una finestra in cui il figlio lancia il compito senza che nessuno se ne accorga (R-744-1). L'ordine è l'inverso di `_esegui`, che scrive prima il pid e poi controlla `_fermato` (`modules/sottofondo/__init__.py:702-705`). Quindi o `ferma` vede il pid, o il figlio vede il segno. Ho controllato anche il caso in cui il figlio ricrea ATTIVO e scrive «in_corso» dopo che `annulla` ha già chiuso il compito: il figlio vede il segno, richiama `annulla` e il compito torna «ko» con il posto liberato. `annulla` non manda avvisi, quindi l'avviso resta uno solo. Esito: ok, R-744-1 chiusa.
- `modules/sottofondo/__init__.py:286` — controllo `id == ident`. Rischio: fermare il processo di un altro compito. È una difesa in più: `_identita(pid, ident)` controlla già il comando del processo (`modules/sottofondo/__init__.py:461`). Esito: riserva cosmetica, vedi sotto.
- `tests/test_unit_sottofondo.py:1176` — `test_ferma_usa_il_lock_e_rilegge_il_pid`. Rischio: un test che non distingue il codice giusto da quello sbagliato (R-744-2). Esito: ok, i risultati dei mutanti sono qui sotto.
- `gas.py:6463` — comando `sottofondo-ferma`: exit 0 o 1 e stampa della frase. Invariato rispetto alla #744. Esito: ok.

**Prove con codice volutamente rotto (mutanti), file ripristinato dopo ogni prova**
- Codice attuale: 112 passed.
- Mutante «fd = None» (niente lock): 1 failed, 111 passed. Preso.
- Mutante con la vecchia lettura (pid preso dalla prima lettura di ATTIVO): 1 failed, 111 passed. Preso.
- Mutante senza il controllo `id == ident`: 112 passed. Non preso.

**Riserve**
- R-745-1 (COSMETICA): nessun test copre il caso in cui l'id cambia fra la prima e la seconda lettura di ATTIVO. Il rischio pratico è basso perché `_identita` verifica comunque il comando del processo.
- Nota sul test: prova che il lock viene chiamato, non che copra davvero tutta la parte critica. Basta a prendere il mutante «lock tolto», ma non è una prova di mutua esclusione.

**Cosa non ho verificato e perché**
- Non ho provato processi veri: flock fra processi diversi, `killpg` su un figlio reale, eventuali nipoti rimasti vivi. Non si riproduce nei test unitari, che sostituiscono `_vivo`, `_identita` e `killpg`.
- Non ho controllato l'atomicità di `_scrivi_privato` (scrittura con rename): mi baso sulle review precedenti.
- Non ho fatto la caccia al Wall of Shame: il diff non contiene slicing della history (grep su `[-N:]` vuoto) né simulazione dell'output dei tool.

**Memoria**: ho aggiunto in .claude/agents/memoria_revisore.md la riga #745 e una lezione nuova (un test che registra solo la chiamata del lock non prova la mutua esclusione), poi ho lanciato `scripts/commit_memoria_revisore.sh` per committare solo quel file.

### Review #746 (sicurezza: `.gas_sottofondo` nel cancello)

## VERDETTO: APPROVATO CON RISERVE

Ho fatto le letture obbligatorie: CLAUDE.md (sezioni 5, 8 e 9), reports/stato_progetto.md con Grep mirato e la mia memoria `.claude/agents/memoria_revisore.md`. Ho applicato la lezione registrata nelle review #559-M1 e #498: ogni nuovo file di stato del kernel deve stare in tutte le liste sorelle e va provato col kernel vero.

**Elementi del diff esaminati**
- modules/gate/gate.py:132 — aggiunge `.gas_sottofondo` a `_DENY_PREFIXES`, la lista dei percorsi negati. Rischi esaminati: varianti di percorso e nuova cartella `.gas_sottofondo_old/`. Ho provato a mano 12 varianti: `./`, `.GAS_SOTTOFONDO`, `x/../`, punto o spazio finale, punto fullwidth, carattere invisibile U+200B nel nome, `dati/.gas_sottofondo/`. Tutte danno DENY sia in `write_file` sia in `read_file`. La nuova `.gas_sottofondo_old/` è negata anche lei, perché il confronto è per prefisso, come già per `.gas_notte`. Esito: ok.
- modules/gate/gate.py:316 — aggiunge `.gas_sottofondo` a `_LIVELLO3_PREFISSI`, i percorsi mai scrivibili. Di conseguenza entra anche in `_LETTURA_NEGATA` (modules/gate/gate.py:339), che è usata da `lettura_consentita` e da `run_command`. Rischio esaminato: la scrittura con firma e gli altri strumenti di lettura.
  - Nel cancello, `elenca_cartella`, `cerca_testo`, `conta_file`, `leggi_righe` e `run_command "cat .gas_sottofondo/a.json"` danno tutti DENY.
  - Nel kernel vero (in una cartella temporanea): `elenca_cartella` e `cerca_testo` sulla radice «.» saltano la cartella («5 voci protette omesse»). Il segreto scritto dentro non esce.
  - Un symlink dal nome innocuo `link` che punta a `.gas_sottofondo` viene negato in `read_file`, `leggi_righe` ed `elenca_cartella`. In `write_file` risponde «questo file non si scrive mai, nemmeno con firma»: lo ferma il ricontrollo sul percorso risolto in `_risolvi_lettura` (gas.py:2669).
  - Esito: ok.
- tests/test_unit_kernel.py:161 — test T6s: `write_file` con `firmata` False e True, controlla che il file non esista. Rischio esaminato: un test che passa anche senza la correzione. Ho tolto la correzione dal cancello: T6s dà 4 FAIL («Successo: File … aggiornato») e tests/test_unit_gate.py dà 10 failed. I test colpiscono davvero. Esito: ok.
- tests/test_unit_gate.py:359 — elenco con id del compito, `attivo.json`, `.passi`, `.ferma`, `.lock` e le varianti. Esito: ok.
- Citazione di contesto, modules/sottofondo/__init__.py:282 — il codice del kernel scrive `.ferma`, `.passi` e i compiti con `Path` diretto (`_scrivi_privato`), non tramite `write_file`/`read_file`. modules/voice/server.py:891 chiama `sottofondo.da_leggere(root)` in-process. Quindi il kernel non si rompe: con la correzione, 944 passed tra tests/test_unit_gate.py e tests/test_unit_sottofondo.py, e la suite del kernel dà 1104 PASS 0 FAIL, riprodotti. Esito: ok.

**Riserve**
- R-746-1 BASSA, problema che esisteva già: `run_command "grep -r … ."` o `ls -a` sulla radice resta IRREVERSIBLE, quindi esegue dopo il cancello. Dentro la sandbox bwrap, in sola lettura, la cartella è leggibile. Vale anche per `.gas_notte`, `.gas_memory.db` ecc.: nessun rischio di scrittura (montaggio in sola lettura), quindi il problema M1 non si riapre. Da tracciare come limite generale della denylist su `run_command`.
- R-746-2 COSMETICA, parità tra liste: `.gas_sottofondo` (come già `.gas_notte`) manca da `_SAFE_PATH_DENY_PREFIXES` (gas.py:2061). Il ricontrollo del livello sul percorso risolto la copre, come ho misurato col symlink. `.gitignore` la esclude già (riga 24).

**Rischi esclusi (non verificati)**
- Comportamento dentro bwrap reale su VPS o Mac: la prova di `run_command` è solo di classificazione del cancello.
- Hard link verso file dentro `.gas_sottofondo`: c'è un controllo già esistente su `st_nlink`, ma non l'ho provato per questa cartella.
- Il processo figlio in sottofondo: ho verificato solo che non usi `write_file` per la propria coda (grep), non l'ho eseguito.

Nessun antipattern della sezione 5 nel diff: nessuna simulazione di tool, nessun taglio della history. La riga contatore #746 è committata in `.claude/agents/memoria_revisore.md` (commit dd7b36c1), con una lezione nuova: le cartelle di stato vanno provate anche via symlink e via visita della cartella, non solo per nome.

File rilevanti: modules/gate/gate.py, tests/test_unit_gate.py, tests/test_unit_kernel.py, .claude/agents/memoria_revisore.md. Lo script della prova è prova.py nello scratchpad della sessione.

### Review #747 (merge di origin/main, #361)

## VERDETTO: APPROVATO

Il merge di origin/main 3f08352 (PR #361) in feat/r7-direttore-m3 è pulito. Tutti i controlli richiesti passano.

**Elementi esaminati:**
- modules/gate/gate.py:132 — `.gas_sottofondo` nelle cartelle mai scrivibili (e a :316 nel livello 3). Rischio: che il merge abbia toccato questa protezione. Esito: ok, `git diff --cached HEAD` non tocca modules/, gas.py né brains/, quindi il file è identico a HEAD, già revisionato in #746.
- modules/sottofondo/__init__.py:269 — `ferma()` con lock e seconda lettura del pid. Rischio: che il codice dei compiti in sottofondo e quello della voce (#361) si tocchino. Esito: ok, i due lati cambiano file diversi (#361 tocca solo clients/voice/ascolto.py, tests/test_unit_voce_ascolto.py, scripts/voce/LEGGIMI.md). Nessuna interazione.
- tests/test_unit_sottofondo.py:1176 — `test_ferma_usa_il_lock_e_rilegge_il_pid`, file invariato rispetto a HEAD. Esito: ok. `pytest tests/test_unit_voce_ascolto.py tests/test_unit_sottofondo.py -k "not browser"` dà **411 passed** (4 deselezionati).
- clients/voice/ascolto.py:452 — codice di #361 (`_sopra_finestra`). Rischio: arrivato diverso da main. Esito: ok, `git diff --cached MERGE_HEAD -- clients tests/test_unit_voce_ascolto.py scripts` è vuoto (0 righe).
- .claude/agents/memoria_revisore.md:1426 — il conflitto è risolto come unione dei due lati. Rispetto a HEAD +7 righe, rispetto a MERGE_HEAD +15, 0 righe tolte da nessun lato. Nessun marcatore di conflitto, `git ls-files -u` vuoto, `git diff --cached --check` pulito. Esito: ok.
- reports/stato_progetto.md:378 — rispetto a MERGE_HEAD aggiunge solo la voce «R7 fetta 1» di M3 (più una riga vuota). Rispetto a HEAD ha le modifiche di #361 (voce #359 aggiornata a MERGIATA e nuova voce «ascolto H24»). Esito: ok, ci sono entrambe le parti.

**Cosa non ho verificato:**
- La suite completa del kernel (tests/test_unit_kernel.py) non l'ho rieseguita. Il merge non tocca gas.py né modules/ rispetto a HEAD, quindi resta valido l'esito di #746 (1104/0).
- Il comportamento della voce sul Mac reale non è riproducibile qui.

**Cosa devi fare tu (contatore memoria):**
- Ho aggiunto in coda a .claude/agents/memoria_revisore.md la riga «#747 (chat M3) — 2026-11-10 — APPROVATO — …». Al momento non è in stage: va aggiunta da te.
- Non sono riuscito a metterla in stage né a lanciare scripts/commit_memoria_revisore.sh: l'hook del gate (PreToolUse) mi ha bloccato i comandi Bash perché `.claude/.review_ok` non corrisponde ancora al diff staged.
- Lo script comunque non funzionerebbe durante un merge, perché git non consente un commit parziale a merge in corso.
- Quindi fai `git add .claude/agents/memoria_revisore.md` (la riga #747 entra nel commit di merge), poi `bash scripts/segna_review_ok.sh` sul diff staged finale, poi committa il merge.

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_sottofondo.py`: 79 casi su main (base) → 112 casi alla fine, tutti passati (`112 passed`).
- `tests/test_unit_gate.py`: `832 passed` (10 failed senza la correzione di `.gas_sottofondo`).
- Suite kernel: 1100 PASS prima → dopo, rilanciata sull'albero del codice di 1537f0c (T6s nuovo, 4 check):

```
=== RIEPILOGO: 1104 PASS, 0 FAIL ===
```

Voce + notte + sottofondo, a metà sessione: `478 passed in 289.68s`; voce ascolto + sottofondo dopo il merge della #361 (dal revisore #747): `411 passed`.

## §6 STATO CI

Check della PR #364 letti con gli strumenti GitHub di sessione alla scrittura dell'handoff (head della PR a7eb3fc, prima del push di questo giro):
- run 42729901220 su a7eb3fc: `unit-suite` success, `handoff-check` success.
- run 42729904942 su a7eb3fc (bot di verifica): `smista`/`verifica`/`esito` success; check `verifica-bot` success (APPROVATA con riserve BASSE).
- run 42728191825 / 42728208340 su dc6c25a: CI success, `verifica-bot` failure (superata dalle correzioni in 47c8aa3).
- run 42727825423 su ef18a4e: `handoff-check` failure (handoff non ancora scritto allora).

Mappatura commit→run:
- a7eb3fc: run 42729901220 (CI) e 42729904942 (bot).
- dc6c25a: run 42728191825 (CI) e 42728208340 (bot).
- ef18a4e: run 42727825423.
- 3101011, 9575467, 525064c, 1852310, aec7195, d4e7828, 30720bb, 47c8aa3, 0049954, dd7b36c, 1537f0c, 5c3af80: nessuna run su questi SHA (1537f0c e 5c3af80 escono col push di questo giro).
- Commit di fine-task di questo giro: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-737-2** (BASSA): un parcheggio alla firma con testo diverso da «Azione in attesa…»/«Operazione negata…» lascia `cancello` None e risulta «fatto» nei progressi.
- **R-738-1** (COSMETICA): `test_posto_sparito_sotto_il_lock_compito_chiuso` prova solo il False di `_riprendi`.
- **R-745-1** (COSMETICA): nessun test sull'id cambiato fra le due letture di ATTIVO in `ferma`.
- **R-746-1** (BASSA, preesistente): `run_command` grep/ls sulla radice legge le cartelle di stato dentro bwrap in sola lettura.
- **R-746-2** (COSMETICA): `.gas_sottofondo`/`.gas_notte` mancano da `_SAFE_PATH_DENY_PREFIXES` (coperti dal ricontrollo sul percorso risolto).
- **Bot #364 2° giro V-1** (BASSA): l'avviso a ogni ripresa consuma il tetto giornaliero delle notifiche; **V-2** (BASSA): `sottofondo-ferma` usa la cartella corrente come radice.
- **Verifica esterna #364**: 1° giro V-1 (BASSA) compito mai partito ritentato fino a 2 volte; 2° giro V-2 (BASSA) arresto reale con `killpg` non provato, V-4 (COSMETICA) comando non in CLAUDE.md §3.
- Nota #744: senza `ps` `ferma` libera il posto anche se il processo forse è vivo (dichiarato nell'avviso).
- Non verificato: processi veri (flock fra processi, kill del figlio, nipoti rimasti vivi), cancello firme end-to-end su un compito ripreso, bwrap reale.
