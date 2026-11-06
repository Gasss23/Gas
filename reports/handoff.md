# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-06 — Bot di verifica: «ad alta voce» non è una gravità (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #342 (https://github.com/Gasss23/Gas/pull/342; numero e URL dalla risposta JSON di `create_pull_request`, `gh` nel cloud non è autenticato). Tocca `scripts/bot_esito.py` (macchina del bot): il check `verifica-bot` dà neutral e il merge lo decide l'operatore (CLAUDE.md §10). La fetta è stata approvata dall'operatore via M1 («fallo in una PR separata subito dopo la #339, con test sul testo vero»).

---

## §1 SCOPE & ESITO FETTE

- **Falso failure del bot su «ad alta voce»** (verdetto vero #339 su 312cd86, solo BASSE/COSMETICHE, dato come MEDIA): `FATTA` — `_ALTA_VOCE` in `scripts/bot_esito.py`, review #687-M2 APPROVATO CON RISERVE, #688-M2 APPROVATO (R-687-1-M2 chiusa).
- **Falso failure del bot sulla #342 su bf4a93b** (il verdetto cita «alta» e «R-xxx MEDIA …» tra virgolette; V-1 BASSA virgolette nel lookahead, V-2 COSMETICA numero PR): `FATTA` con la scelta (a)+(b) dell'operatore via M1 — 10b3cbc: citazioni «…» brevi non contano nelle regole a parole (parentesi e campo strutturato invariati), lookahead senza virgolette, numero della PR nei report; review #690-M2, #691-M2 (riserve chiuse), #692-M2 APPROVATO.
- **Altro falso failure su d9c09e9** (citazione «R-682-1-M2 MEDIA …» senza parentesi): `NON FATTA — fuori scope`: il difetto blocca invece di lasciar passare (direzione sicura); si evita scrivendo le riserve come «R-xxx (GRAVITÀ)».
- **Fetta 2 voce rapida**: `FATTA in locale` (commit 05b40ae sul branch locale voce-rapida-wip, review #689-M2 APPROVATO CON RISERVE): si pusha dopo il merge della #342 (ordine di M1). **Documento della fetta 3**: `DEFERITO — prossima fetta`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md               |   8 ++++
 reports/diff_sessione.md                         | n/d
 reports/handoff.md                               | n/d
 reports/ripartenza_m2.md                         | n/d
 reports/stato_progetto.md                        | n/d
 reports/ultimo_report.md                         | n/d
 scripts/bot_esito.py                             |  46 +++++++++++++++++++++-
 tests/dati_verifica_bot/verdetto_339_312cd86.txt |  22 +++++++++++
 tests/dati_verifica_bot/verdetto_342_bf4a93b.txt |  23 +++++++++++
 tests/test_unit_verifica_bot.py                  | 120 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — i report si riscrivono anche in questo commit di fine task, quindi i loro conteggi non sono misurabili mentre si scrivono; riga di totale tolta. Base: origin/main 3cde8a5 (merge della #339).

## §3 GIT LOG --ONELINE (sessione)

```
10b3cbc fix(bot): parole di gravità citate tra «…» non contano nelle regole a parole; «a voce alta» senza virgolette di chiusura (V-1 bot #342, scelta (b) dell'operatore via M1) (chat M2)
61e1725 chore(revisore): memoria review #692 — APPROVATO
041fe82 chore(revisore): memoria review #691 — APPROVATO CON RISERVE
18a99ae chore(revisore): memoria review #690 — APPROVATO CON RISERVE
23c13b8 chore(revisore): memoria review #689 — APPROVATO CON RISERVE
bf4a93b docs(bot): report di fine task — parser «ad alta voce» e merge della #339 (chat M2)
17f062d fix(bot): «ad alta voce» / «a voce alta» non è una gravità (falso failure del bot #339 su 312cd86) (chat M2)
4b525ce chore(revisore): memoria review #688 — APPROVATO
37f6eaa chore(revisore): memoria review #687 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #687-M2 sul primo stage di 17f062d (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #687-M2. Diff staged: `scripts/bot_esito.py`, `tests/test_unit_verifica_bot.py` e `tests/dati_verifica_bot/verdetto_339_312cd86.txt`. Prima della review ho letto CLAUDE.md (sezioni 5, 8 e 9), le parti di `reports/stato_progetto.md` su `bot_esito` e la coda della memoria.

**Cosa ho controllato nel diff**

1. `scripts/bot_esito.py:132`: la nuova regola `_ALTA_VOCE` riconosce il modo di dire «ad alta voce» / «a voce alta». Rischio cercato: che nasconda una gravità vera (cioè che un «no» diventi un «sì»). Esito: ok.
   - «alta» viene tolta solo se è scritta in minuscolo.
   - Tra le parole accetta solo spazi o tab. Un NBSP (spazio non separabile) o un a capo non vengono riconosciuti, quindi la riga resta bloccante.
   - Ho provato con una sonda:
     - «ad alta voce» dà MEDIA;
     - «a voce alta\tma alta» dà MEDIA;
     - «a  voce alta media» dà MEDIA;
     - «gravità alta: letto ad alta voce» dà MEDIA, perché la regola cerca su tutta la riga e trova anche l'altra «alta».
   - Con caratteri invisibili attaccati («ad ​alta voce», «ad alta​ voce», «a voce ⁠alta») il risultato è COMMENT: li ferma `_invisibili_su_gravita`, che a `scripts/bot_esito.py:408` scatta prima della pulizia.
2. `scripts/bot_esito.py:227`: la regola si applica solo alla ricerca della gravità scritta a parole, dopo `_GRAVITA_NEGATA` e `_BLOCCANTE_TECNICO`. Rischio cercato: che indebolisca anche le parole maiuscole o le gravità tra parentesi. Esito: ok.
   - La ricerca delle parole maiuscole (`_PAROLA_BLOCCANTE`) lavora su `finding`, non su `pulita`, quindi non cambia.
   - La ricerca tra parentesi (`_FINDING_GRAVITA`) lavora su `sezione`, quindi non cambia.
   - «V-1 — ad alta voce (MEDIA)» dà ancora MEDIA.
   - Sostituire il modo di dire con «voce» non può creare una gravità nuova, né far sparire l'id di un finding o una negazione.
3. `tests/test_unit_verifica_bot.py:1321`: test sul verdetto vero 312cd86 (APPROVE), 5 casi che devono restare bloccati e 3 casi del modo di dire. Rischio cercato: test che passano anche col codice sbagliato. Esito: ok.
   - Sul file intero: 591 passed.
   - Ho provato il codice sbagliato apposta (sostituzione tolta, in una copia): falliscono 4 test, il 339 e i 3 casi del modo di dire. Il quinto rosso, `test_invisibili_come_nel_gate`, dipende solo dal fatto che la copia sta fuori dal repo.
4. `tests/dati_verifica_bot/verdetto_339_312cd86.txt:10`: testo vero del bot, con «il testo viene letto ad alta voce». Esito: ok, corrisponde al caso del bug.

**Riserva**

- R-687-1-M2 (BASSA): «a voce alta» seguito da un nome viene tolto anche quando «alta» si riferisce al nome dopo. Esempio: «V-1 (BASSA) — comando a voce alta priorità» dà APPROVE. È un caso costruito apposta e resta il campo strutturato della gravità. Si può chiudere con un controllo che escluda le parole che seguono, ad esempio `(?![ \t]+(?:priorit|gravit|severit|rischi))`, oppure accettarlo dichiarandolo. Da tracciare in stato_progetto.md.

**Cosa NON ho verificato**

- Il comportamento nel workflow vero `verifica-bot` su GitHub: non si può riprodurre qui. Per questo la PR resta neutral (tocca la macchina del bot) e il merge spetta all'operatore.
- La nota fuori scope «R-682-1-M2 MEDIA … da decidere» senza parentesi: non toccata. È un difetto già esistente che blocca invece di lasciar passare, quindi non è pericoloso.

Memoria: riga #687-M2 aggiunta e committata (37f6eaa) con `scripts/commit_memoria_revisore.sh`.

File rilevanti:
- /home/user/Gas/scripts/bot_esito.py
- /home/user/Gas/tests/test_unit_verifica_bot.py
- /home/user/Gas/tests/dati_verifica_bot/verdetto_339_312cd86.txt
- /home/user/Gas/.claude/agents/memoria_revisore.md

Review #688-M2 (seconda review di #687-M2) sul commit 17f062d (verdetto integrale):

## VERDETTO: APPROVATO

Review #688-M2: seconda review della modifica #687-M2 sul diff staged (branch feat/voce-v12-m2). La riserva R-687-1-M2 è chiusa. Letture obbligatorie fatte: CLAUDE.md §5, la voce R-687 in reports/stato_progetto.md e la coda della memoria del revisore.

**Elementi del diff esaminati**
- `scripts/bot_esito.py:133` — `_ALTA_VOCE`: la seconda alternativa («a voce alta») ora viene tolta solo se dopo c'è un segno di punteggiatura o la fine della riga (`(?=[ \t]*(?:[.,;:)!?»"']|$))`, con re.M). Rischio esaminato: che re.M allarghi la prima alternativa, o che il filtro tolga una gravità vera. Prove fatte direttamente sulla regex:
  - re.M agisce solo su `^`/`$`, e la prima alternativa non li contiene: per lei non cambia nulla.
  - Restano bloccanti: «a voce alta priorità», «a voce alta — MEDIA» (il trattino non è nella lista, quindi resta bloccante: scelta prudente), «ad ALTA voce», «a voce altamente».
  - «a voce alta,gravità alta» diventa «voce,gravità alta», ma il secondo «alta» viene ancora preso dalla regola a parole, quindi resta bloccante.
  - «a voce alta\nMEDIA» → «voce\nMEDIA»: qui `$` con re.M scatta a fine riga, ma MEDIA resta visibile.
  - Esito: ok.
- `scripts/bot_esito.py:229` — il filtro si applica solo prima di `_FINDING_GRAVE_A_PAROLE` (la regola che cerca la gravità scritta a parole); le altre regole non cambiano. Esito: ok.
- `tests/test_unit_verifica_bot.py:1338` — il nuovo caso «comando a voce alta priorità» deve dare COMMENT (cioè bloccare); «Gas lo dice a voce alta, poi tace» deve dare APPROVE. Rischio esaminato: test che non distingue il codice giusto da quello sbagliato. Ho provato una versione sbagliata (mutante): tolto il lookahead, il caso «priorità» fallisce (1 failed, 592 passed). Codice poi ripristinato: lo staged è identico a prima. Esito: ok.
- `tests/dati_verifica_bot/verdetto_339_312cd86.txt:13` — il caso reale «letto ad alta voce» in V-1 (BASSA) passa ancora dalla prima alternativa, che non è cambiata. Esito: ok.

**Test:** `tests/test_unit_verifica_bot.py` dà 593 passed, rilanciato col venv indicato.

**Residuo accettato (nessuna riserva aperta):** il filtro toglie ancora «ad alta voce <nome>» e «"a voce alta" <nome>» tra virgolette (« o "), anche se un nome segue. Sono forme rare e innaturali in italiano, e la gravità strutturata del finding continua a contare.

**Rischio escluso:** non ho verificato il comportamento sul bot reale. Servirebbe il workflow `verifica-bot` su una PR con l'etichetta `verifica`, che non si riproduce in locale. Non ho nemmeno rilanciato le suite kernel/voce, perché il diff non tocca il motore runtime.

**Memoria:** riga #688-M2 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata a parte (4b525ce, «chore(revisore): memoria review #688 — APPROVATO»). Lo staged del diff è intatto: 3 file, +67/-1. Nessuna lezione nuova.

Review #690-M2 sul primo stage di 10b3cbc (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #690-M2: fix bot #342. Il diff staged è su feat/voce-v12-m2, con base bf4a93b e memoria 23c13b8. Tocca la macchina del bot, quindi la PR resta neutral e il merge lo decide l'operatore.

Ho letto CLAUDE.md (sezioni 5, 8, 9 e 10), lo stato del progetto (per la parte che riguarda bot_esito) e la memoria del revisore (#671–#689, lezioni sul parser del bot).

Elementi del diff esaminati:
- scripts/bot_esito.py:134 — toglie le virgolette (» " ') dal lookahead della seconda alternativa di `_ALTA_VOCE`. Rischio esaminato: che «a voce alta» seguito da una virgoletta di chiusura nasconda ancora «alta». Esito: ok. V-1 del bot è chiusa e il caso «comando a voce alta» priorità» è nel test di tests/test_unit_verifica_bot.py:1339.
- scripts/bot_esito.py:140 — `_CITAZIONE_BREVE` con la classe `[^«»\n]{1,80}`. Rischio esaminato: ReDoS. Esito: ok. La regex è lineare; con 5 passate dall'interno e uscita appena il testo non cambia più, 50k virgolette annidate impiegano 0,58 s, 100k aperte 0,36 s, 5000 citazioni 1,69 s (HEAD: 0,7 / 0,36 / 1,65 s). Secondo rischio: separatori di riga. Esito: riserva. La classe accetta \r, e CommonMark mostra \r come un a capo: `V-1 (BASSA) — «x\rV-2 — grave»` dà APPROVE (a HEAD dava COMMENT), mentre l'operatore vede una riga «V-2 — grave»». Diventa R-690-1-M2.
- scripts/bot_esito.py:238 e scripts/bot_esito.py:247 — l'esenzione delle citazioni vale solo per `_PAROLA_BLOCCANTE` (su `finding`) e per la regola a parole (su `pulita`). Rischio esaminato: che allenti anche le parentesi o il campo strutturato. Esito: ok. `_FINDING_GRAVITA` lavora ancora su `sezione` («V-1 (BASSA) — «V-2 (alta)»» resta COMMENT). In scripts/bot_esito.py:454 restano `gravita_strutturate`, `testo` e `grezzo`, e la sostituzione con «…» non crea gravità e non unisce righe.
- tests/test_unit_verifica_bot.py:1384 — 10 test avversari. Rischio esaminato: che i casi provino davvero le condizioni dell'operatore. Esito: ok. Una gravità fuori dalle virgolette blocca sempre: ho rifatto io la sonda «x» MEDIA «y», che dà COMMENT.
- tests/test_unit_verifica_bot.py:1390 — `test_media_strutturata_non_sfugge_per_una_citazione`. Esito: riserva cosmetica. Il test passa per il solo campo strutturato MEDIA (scripts/bot_esito.py:454) e non esercita la citazione. Risponde alla lettera alla condizione dell'operatore, ma non uccide nessun mutante della funzione.

Sonde che ho rifatto io (decidi sul file staged, confrontato con HEAD in una copia nella scratchpad):
- **Passano da NO (a HEAD) a sì, sempre con campo strutturato BASSA:**
  - `«V-1 — il difetto è grave»` come riga intera tra virgolette;
  - `«V-1 — ALTA — rompe tutto»`;
  - `V-1 (BASSA) — giudizio: «grave»`;
  - NBSP dentro la citazione;
  - citazione sbilanciata `«a «MEDIA» b`;
  - `V-2 «— grave»` su una riga di un finding assente dal campo strutturato.
- **Restano NO:** ZWSP dentro la citazione (`_invisibili_su_gravita`), `»MEDIA«` rovesciata, `«x» MEDIA «y»`, la parentesi citata.
- Suite: tests/test_unit_verifica_bot.py 610 passed sull'albero staged (che coincide con il worktree).

Giudizio sul residuo: è accettabile. L'operatore ha scelto che il campo strutturato sia l'unica fonte forte, e quel campo blocca sempre ALTA/MEDIA indipendentemente dal testo. Quello che si perde è il rilevatore di incoerenza «il testo dice grave, il campo dice BASSA», ma solo quando la gravità sta tra virgolette basse, su una riga, e in al massimo 80 caratteri. Il caso più debole è il bot che scrive il proprio giudizio tra virgolette («giudizio: «grave»») o l'intero finding tra virgolette: va dichiarato, non nascosto.

Riserve:
- **R-690-1-M2 (BASSA):** escludere \r dalla classe di `_CITAZIONE_BREVE` (scripts/bot_esito.py:140), cioè `[^«»\r\n]`, con un test `«x\rV-2 — grave»` che deve dare COMMENT.
- **R-690-2-M2 (BASSA):** una citazione che apre la riga (`^\W*«V-1 — grave»`) o che contiene il giudizio del finding fa sparire la gravità scritta a parole. Due strade:
  - non esentare la citazione a inizio riga: è un ripiego economico che non rompe il caso vero della #342, perché lì le citazioni stanno a metà frase;
  - oppure fissare il residuo accettato con un test documentato.
- **R-690-3-M2 (COSMETICA):** il test di tests/test_unit_verifica_bot.py:1390 non esercita le citazioni. Aggiungere un caso con gravità strutturata BASSA e la MEDIA vera fuori dalle virgolette nella stessa riga di una citazione: oggi è coperto solo in parte da :1384.

Rischi esplicitamente esclusi:
- Il comportamento reale del workflow verifica-bot sul prossimo verdetto del bot: si vede solo da un run vero su GitHub.
- La CI di questo diff: non ancora pushato.
- Il mutante «_senza_citazioni_brevi identità → 5 failed» dichiarato dall'agente: non l'ho rifatto, ho usato al suo posto le sonde staged/HEAD qui sopra.
- La forma esatta del testo che il bot genera nella pratica (frequenza delle virgolette basse, uso di \r): dipende dal modello, non si verifica dal repo.

Memoria: riga #690-M2 e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md e committate da sole (18a99ae, `scripts/commit_memoria_revisore.sh`). Il diff staged è intatto: 3 file, +96/-3.

Sonde: /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/sonde.py (file staged) e /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/sonde_head.py (HEAD).

Review #691-M2 (#690-M2 bis) sul secondo stage di 10b3cbc (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #691-M2 (è la #690-M2 bis). Diff staged su feat/voce-v12-m2, PR #342: scripts/bot_esito.py, tests/test_unit_verifica_bot.py, tests/dati_verifica_bot/verdetto_342_bf4a93b.txt. Lo sha256 del diff staged comincia con 2e71593fd9d8. Prima della review ho letto CLAUDE.md, stato_progetto e la memoria del revisore.

**Elementi del diff esaminati**
- scripts/bot_esito.py:142 — `_CITAZIONE_BREVE = «[^«»\r\n]{1,80}»`. Rischio: un \r dentro la citazione, che CommonMark mostra come a capo. Esito: ok, R-690-1-M2 chiusa. Il caso «x\rV-2 — grave» dà COMMENT, ed è in tests/test_unit_verifica_bot.py:1385 (gruppo parametrizzato).
- scripts/bot_esito.py:146 — `_cita_a_meta_riga`: cerca l'inizio riga con `rfind("\n")` e non esenta una citazione se prima, sulla stessa riga, non c'è nessuna lettera o cifra. Rischio: citazione che apre la riga. Esito: **riserva**. Funziona per «…» a inizio riga, per «- «…»» e per «**«…»**» (COMMENT). Però:
  - (a) «V-1 (BASSA) — x\r«V-2 — il difetto è grave»» dà APPROVE: si cerca solo \n, ma CommonMark tratta anche \r come fine riga;
  - (b) «1. «V-1 — il difetto è grave»» dà APPROVE: `\w` comprende le cifre dell'elenco numerato;
  - (c) costo quadratico: per ogni citazione rfind e slice ripartono dall'inizio della riga. Su una riga sola con 100k citazioni (400 KB) servono 3,4 s per passata. Il tetto è VERDETTO_MAX_BYTE = 1 MB e le chiamate sono circa 4 × 2 passate, quindi si arriva a minuti. Non va in crash, non c'è ReDoS e con testi normali non ci sono problemi (2000 citazioni 0,04 s; 20000 0,9 s in decidi).
- scripts/bot_esito.py:245 e scripts/bot_esito.py:254 — l'esenzione vale solo per le maiuscole e per la regola a parole; parentesi e campo strutturato restano invariati. Esito: ok. Una gravità fuori dalle virgolette accanto a una citazione («alta» ma MEDIA) dà COMMENT, quindi R-690-3-M2 è chiusa.
- tests/test_unit_verifica_bot.py:1403 — `test_residuo_accettato_giudizio_citato` fissa il residuo dichiarato: APPROVE se il campo strutturato è BASSA, COMMENT se è MEDIA. Esito: ok, è la documentazione chiesta da R-690-2-M2.
- tests/dati_verifica_bot/verdetto_342_bf4a93b.txt:1 — il verdetto vero del bot #342 dà ancora APPROVE (test_342). Esito: ok.

**Esecuzione**: ho rilanciato tests/test_unit_verifica_bot.py nel venv dello scratchpad: 615 passed. Sonde nello scratchpad, poi i tempi su righe lunghe (20k, 50k e 100k citazioni).

**Riserve** (da tracciare in stato_progetto.md)
- R-691-1-M2 BASSA: in `_cita_a_meta_riga` (scripts/bot_esito.py:146) l'inizio riga va cercato anche dopo \r, cioè l'ultima posizione tra rfind("\n") e rfind("\r"). Test: «x\r«V-2 — il difetto è grave»» → COMMENT.
- R-691-2-M2 BASSA: verificare che nel prefisso ci siano lettere (`[^\W\d_]`) invece di `\w`, così «1. «V-1 — il difetto è grave»» non viene più esentata. Test relativo.
- R-691-3-M2 BASSA: rendere lineare l'esenzione, lavorando riga per riga (split su \n/\r e sub per riga) invece di fare rfind+slice per ogni citazione.
- R-691-4-M2 COSMETICA: «x» «V-1 — il difetto è grave» dà APPROVE, perché la seconda citazione è a metà riga. È la stessa classe del residuo «giudizio: «grave»», ma va scritta nel commento o in un test. Il campo strutturato continua a bloccare.

Tutte le riserve sono BASSE perché il campo strutturato della gravità resta la fonte forte e blocca sempre, come aveva chiesto l'operatore.

**Rischio escluso**: non ho verificato il comportamento del workflow verifica-bot reale né la CI su GitHub. Non è riproducibile qui: si vede solo da un run vero sulla PR #342. Non ho fatto mutation testing sulle correzioni.

**Memoria**: aggiunta la riga #691-M2 e una lezione (in un filtro «inizio riga» su testo Markdown contano \n e \r, e le cifre degli elenchi numerati vanno trattate come marcatori). Committata da sola con scripts/commit_memoria_revisore.sh nel commit 041fe82. L'index staged non è cambiato.

File rilevanti:
- /home/user/Gas/scripts/bot_esito.py
- /home/user/Gas/tests/test_unit_verifica_bot.py
- /home/user/Gas/.claude/agents/memoria_revisore.md
- /tmp/claude-0/-home-user-Gas/62c50102-54a5-5454-8ce4-94a07d021191/scratchpad/sonda690b.py

Review #692-M2 sul commit 10b3cbc (verdetto integrale):

## VERDETTO: APPROVATO

Review #692-M2: diff staged su feat/voce-v12-m2 per la PR #342 (sha256 del diff staged 6a0e699582c920592d091b094b96a849cb7fb0300a18805bff74c4722d9d29e8). Tocca la macchina del bot: scripts/bot_esito.py, tests/test_unit_verifica_bot.py e tests/dati_verifica_bot/verdetto_342_bf4a93b.txt. Prima della review ho letto CLAUDE.md §5, la parte di reports/stato_progetto.md che riguarda questa fetta e le ultime righe di memoria (#688–#691-M2).

Elementi del diff esaminati:
- `scripts/bot_esito.py:145`: `_FINE_RIGA = (\r\n|\r|\n)` con gruppo di cattura, così `split` conserva i separatori e `_senza_citazioni_brevi` (scripts/bot_esito.py:164) ricompone il testo identico. Rischio: un \r non visto come fine riga (R-691-1), separatori persi o riordinati. Sonde: «x\r«V-2 — il difetto è grave»» e «x\r\n«V-2 — il difetto è grave»» danno COMMENT; «x\r«MEDIA»» dà COMMENT. Esito: ok.
- `scripts/bot_esito.py:154`: la soglia è la prima lettera della riga (`[^\W\d_]`) e una citazione è esentata solo se `m.start() > soglia`. Rischio: l'elenco numerato o un prefisso di simboli che esenta la citazione d'apertura (R-691-2), e la soglia che si sposta dopo le sostituzioni. Le sostituzioni avvengono solo dopo la soglia, quindi la soglia resta valida in tutte le 5 passate. Sonde: «1. «V-1 — ALTA — …»», «1)\t«V-1 — ALTA»», «> «V-1 — il difetto è grave»», «* «V-1 — MEDIA»», «  «V-2 — …»» e «**«V-1 — ALTA»**» danno tutte COMMENT, come a HEAD. Esito: ok.
- `scripts/bot_esito.py:255` e `scripts/bot_esito.py:264`: la nuova funzione sostituisce la vecchia nelle due sole regole a parole (maiuscole e `_FINDING_GRAVE_A_PAROLE`); parentesi e campo strutturato restano invariati. Rischio: l'esenzione che si estende ad altre regole. Ho controllato che `_senza_citazioni` (scripts/bot_esito.py:374), usata per i segreti, è un'altra funzione non toccata. Esito: ok.
- `tests/test_unit_verifica_bot.py:1389-1390`: aggiunge i casi \r e «1. «…»» al parametrico COMMENT. `tests/test_unit_verifica_bot.py:1406` fissa il residuo R-691-4 (BASSA → APPROVE, MEDIA strutturata → COMMENT). `tests/test_unit_verifica_bot.py:1421` controlla il tempo lineare. Rischio: test che passano anche col codice vecchio. I casi \r e «1. «V-1 — ALTA»» erano proprio quelli che a #691 davano APPROVE, quindi senza la correzione fallirebbero. Esito: ok.
- Suite rilanciata nel venv indicato: 618 passed in 4,03 s. Prestazioni: 1 MB di «x» su una sola riga in 0,10 s; 500k «« aperte in 0,01 s. La parte quadratica di R-691-3 è chiusa.

Sonde con esito diverso da HEAD (scelte, non regressioni):
- Un separatore di riga Unicode o un \x0c prima di «V-2 — il difetto è grave»: ora APPROVE, a HEAD COMMENT. CommonMark non li tratta come fine riga, quindi a schermo la citazione resta a metà riga. È la stessa classe del residuo già accettato dall'operatore (gravità solo tra virgolette a metà riga, la blocca il campo strutturato).
- «V-1 (BASSA) — «MEDIA»» e annidamenti profondi: APPROVE per scelta dell'operatore (Fix bot #342).
- «_«V-1 — il difetto è grave»_» dà APPROVE anche a HEAD, perché `^\W*` di `_FINDING_GRAVE_A_PAROLE` (scripts/bot_esito.py:125) non salta `_`. Il caso è vecchio e non lo introduce questa fetta. Vale lo stesso per «1. «V-1 — il difetto è grave»», come dichiarato dall'agente.

Riserve: nessuna. Wall of Shame: nessuno slicing della storia, nessuna simulazione di tool. Il diff non tocca gas.py né brains/.

Rischio escluso: non ho eseguito il workflow vero `.github/workflows/verifica-bot.yml` sulla PR #342 né la pubblicazione del check da parte della GitHub App. Non si può riprodurre in locale; ho verificato solo `decidi()` sui testi, compreso il verdetto vero #342, che passa nel test della suite. Non ho riletto per intero reports/stato_progetto.md (solo la parte rilevante, §11).

Memoria: riga #692-M2 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con scripts/commit_memoria_revisore.sh (commit 61e1725). Il diff staged sotto review è intatto (3 file, +144/−3).

## §5 DELTA TEST DEL MOTORE

Su 10b3cbc: tests/test_unit_verifica_bot.py `618 passed` (verdetto vero #342 → APPROVE; avversari: gravità fuori dalle virgolette, MEDIA strutturata, citazione a inizio riga, \r, elenco numerato, virgolette dritte/alte, > 80 caratteri; residuo dichiarato fissato; tempo lineare). Mutante «esenzione identità» → 5 failed.

Motore (gas.py, brains/, modules/) non toccato. `tests/test_unit_verifica_bot.py`: +11 test (verdetto vero 312cd86 → APPROVE; 6 casi che restano bloccati; 4 casi del modo di dire) — `593 passed` (prima 582). Mutanti: «sostituzione tolta» → 4 failed; «lookahead tolto» → 1 failed.

## §6 STATO CI

- bf4a93b: unit-suite success, handoff-check success, verifica-bot FAILURE (falso: verdetto testuale con sole V-1 BASSA e V-2 COSMETICA, parole di gravità citate tra virgolette); verifica esterna APPROVATO CON RISERVE (solo BASSE).
- 23c13b8, 18a99ae, 041fe82, 61e1725, 10b3cbc e commit di fine-task che contiene questo file: run non ancora disponibile (pushati insieme).

Storico: `gh` non autenticato nel cloud: check lette con l'integrazione GitHub. 37f6eaa, 4b525ce, 17f062d e il commit di fine-task che contiene questo file sono pushati insieme: run non ancora disponibile alla scrittura dell'handoff (la run testerà solo la testa). Su questa PR `verifica-bot` dà neutral (tocca la macchina del bot).

## §7 RISERVE APERTE

- Residuo dichiarato (scelta (b) dell'operatore): una gravità scritta SOLO tra virgolette basse a metà riga («giudizio: «grave»», «x» «il difetto è grave») non conta nel testo; la blocca il campo strutturato. Separatori di riga Unicode/\x0c non contano come fine riga (stessa classe).
- Nessuna riserva aperta di questa fetta (R-687-1-M2 chiusa in #688-M2). Residuo accettato dal revisore: «ad alta voce <nome>» e «"a voce alta" <nome>» tra virgolette vengono ancora tolti.
- Noto, fuori scope: una citazione di riserva senza parentesi («R-682-1-M2 MEDIA …») fa bloccare il bot (falso failure, direzione sicura).
